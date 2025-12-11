import time
import random
from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Regions
REGIONS = [
    ("India", "https://in.indeed.com/jobs?q=ai+ml+engineer&l="),
    ("USA",   "https://www.indeed.com/jobs?q=ai+ml+engineer&l=") 
]

def scrape_indeed():
    print(f"[{datetime.now()}] Starting Indeed Scrape (SeleniumBase UC Mode)...")

    all_jobs = []

    try:
        # Use SeleniumBase with UC (Undetected Chrome) mode
        with SB(uc=True, headless=False) as sb:
            driver = sb.driver

            for region_name, base_url in REGIONS:
                print(f"\n--- Switching to Indeed {region_name} ---")
                
                for page in range(0, 1): 
                    start_param = page * 10
                    url = f"{base_url}&start={start_param}"
                    
                    print(f"   [Indeed {region_name}] Navigating to Page {page + 1}...")
                    
                    try:
                        # Use SeleniumBase's uc_open_with_reconnect for better anti-bot handling
                        sb.uc_open_with_reconnect(url, reconnect_time=5)
                    except Exception as e:
                        print(f"   Error opening URL: {e}")
                        driver.get(url)

                    # Random delay to appear more human-like
                    time.sleep(random.uniform(8, 15))

                    # Handle potential Cloudflare challenge
                    if "challenge" in driver.title.lower() or "security" in driver.title.lower():
                        print("   !!! Cloudflare/Security Challenge detected. Waiting extra time...")
                        time.sleep(20)
                        try:
                            sb.uc_gui_click_captcha()  # Try to solve captcha if present
                        except:
                            pass

                    try:
                        # Increased wait to 30s
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.ID, "mosaic-provider-jobcards"))
                        )
                    except:
                        print(f"   Timeout on {region_name} page {page+1}")
                        continue

                    job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
                    print(f"   Found {len(job_cards)} cards. Processing...")

                    for card in job_cards:
                        try:
                            try:
                                title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
                                title = title_elem.text
                                link = title_elem.get_attribute("href")
                            except:
                                title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span")
                                title = title_elem.text
                                try: link = card.find_element(By.XPATH, ".//a").get_attribute("href")
                                except: link = driver.current_url

                            try: company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text
                            except: company = "N/A"

                            try: location = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text
                            except: location = "N/A"

                            salary = "Not Disclosed"

                            # Metadata Check
                            try:
                                metadata = card.find_elements(By.CLASS_NAME, "metadata")
                                for m in metadata:
                                    text = m.text
                                    if any(symbol in text for symbol in ['₹', '$', '€', '£', 'Lacs']):
                                        salary = text
                                        break
                            except: pass

                            # Right Pane Check
                            if salary == "Not Disclosed":
                                try:
                                    card.click()
                                    try:
                                        wait = WebDriverWait(driver, 5)
                                        wait.until(EC.text_to_be_present_in_element(
                                            (By.CSS_SELECTOR, "div.jobsearch-JobInfoHeader-title-container h2"), title
                                        ))
                                    except: pass

                                    right_pane = driver.find_element(By.ID, "salaryInfoAndJobType").text
                                    if any(s in right_pane for s in ['₹', '$', '€', '£', 'Lacs']) or \
                                       (any(c.isdigit() for c in right_pane) and "year" in right_pane.lower()):
                                        salary = right_pane
                                except: pass

                            all_jobs.append({
                                "Title": title,
                                "Company": company,
                                "Experience": "N/A",
                                "Location": location,
                                "Description": "See Link",
                                "Salary": salary,
                                "Link": link,
                                "Site": f"Indeed ({region_name})", 
                                "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            })
                        except: continue

    except Exception as e:
        print(f"   [Indeed] Error during scraping: {e}")

    print(f"   [Indeed] Total Found: {len(all_jobs)} jobs.")
    return all_jobs

if __name__ == "__main__":
    scrape_indeed()