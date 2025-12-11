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
    print(f"[{datetime.now()}] Starting Indeed Internship Scrape (Xvfb Mode)...")

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-popup-blocking")
    
    driver = uc.Chrome(options=options)

    all_internships = []

    try:
        for region_name, base_url in REGIONS:
            print(f"\n--- Switching to Indeed {region_name} (Internships) ---")
            
            for page in range(0, 1): 
                start_param = page * 10
                url = f"{base_url}&start={start_param}"
                
                print(f"   [Indeed {region_name}] Navigating to Page {page + 1}...")
                driver.get(url)

                # Increased sleep
                time.sleep(random.uniform(8, 12))

                if "challenge" in driver.title.lower() or "security" in driver.title.lower():
                    print("   !!! Cloudflare detected. Waiting extra time...")
                    time.sleep(15)

                try:
                    WebDriverWait(driver, 25).until(
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
                                except: pass

                                right_pane = driver.find_element(By.ID, "salaryInfoAndJobType").text
                                if any(s in right_pane.lower() for s in ['₹', '$', '€', '£', 'lacs', 'stipend']) or \
                                   (any(c.isdigit() for c in right_pane) and "month" in right_pane.lower()):
                                    salary = right_pane
                            except: pass

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
                    except: continue
            
    finally:
        try: driver.quit()
        except: pass

    print(f"   [Indeed] Total Found: {len(all_internships)} internships.")
    return all_internships

if __name__ == "__main__":
    scrape_indeed_intern()