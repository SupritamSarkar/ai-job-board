import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Internship Specific Regions
REGIONS = [
    ("India", "https://in.indeed.com/jobs?q=ai+ml+engineer+intern&l="),
    ("USA",   "https://www.indeed.com/jobs?q=ai+ml+intern&l=") 
]

def scrape_indeed_intern():
    print(f"[{datetime.now()}] Starting Indeed Internship Scrape...")

    options = uc.ChromeOptions()
    # CRITICAL FIX FOR GITHUB ACTIONS:
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-popup-blocking")
    
    # Remove strict version constraint for CI
    driver = uc.Chrome(options=options)

    all_internships = []

    try:
        for region_name, base_url in REGIONS:
            print(f"\n--- Switching to Indeed {region_name} (Internships) ---")
            
            for page in range(0, 6): 
                start_param = page * 10
                url = f"{base_url}&start={start_param}"
                
                print(f"   [Indeed {region_name}] Navigating to Page {page + 1}...")
                driver.get(url)

                time.sleep(random.uniform(4, 6))

                if "challenge" in driver.title.lower() or "security" in driver.title.lower():
                    print("   !!! Cloudflare Challenge detected. Waiting 10s...")
                    time.sleep(10)

                try:
                    WebDriverWait(driver, 15).until(
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
                            link = driver.current_url 

                        try: company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text
                        except: company = "N/A"

                        try: location = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text
                        except: location = "N/A"

                        salary = "Not Disclosed"

                        # A. Card Check
                        try:
                            metadata = card.find_elements(By.CLASS_NAME, "metadata")
                            for m in metadata:
                                text = m.text
                                if any(symbol in text for symbol in ['₹', '$', '€', '£', 'Lacs', 'stipend']):
                                    salary = text
                                    break
                        except: pass

                        # B. Right Pane Check
                        if salary == "Not Disclosed":
                            try:
                                card.click()
                                try:
                                    wait = WebDriverWait(driver, 5)
                                    wait.until(EC.text_to_be_present_in_element(
                                        (By.CSS_SELECTOR, "div.jobsearch-JobInfoHeader-title-container h2"), title
                                    ))
                                except:
                                    raise Exception("Right pane mismatch")

                                right_pane_text = driver.find_element(By.ID, "salaryInfoAndJobType").text
                                
                                currency_indicators = ['$', '₹', '€', '£', 'Lacs', 'stipend']
                                if any(symbol in right_pane_text.lower() for symbol in currency_indicators):
                                    salary = right_pane_text
                                elif any(char.isdigit() for char in right_pane_text) and \
                                     any(period in right_pane_text.lower() for period in ['year', 'month', 'pa']):
                                     salary = right_pane_text
                            except:
                                pass

                        all_internships.append({
                            "Title": title,
                            "Company": company,
                            "Experience": "Internship",
                            "Location": location,
                            "Description": "See Link",
                            "Salary": salary,
                            "Link": link,
                            "Site": f"Indeed ({region_name})", 
                            "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        })
                    except:
                        continue
            
    finally:
        try: driver.quit()
        except: pass

    print(f"   [Indeed] Total Found: {len(all_internships)} internships.")
    return all_internships

if __name__ == "__main__":
    scrape_indeed_intern()