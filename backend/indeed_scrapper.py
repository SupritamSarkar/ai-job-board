import time
import random
import undetected_chromedriver as uc
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
    print(f"[{datetime.now()}] Starting Indeed Scrape...")

    options = uc.ChromeOptions()
    # options.add_argument("--headless") # Headless OFF for Indeed
    options.add_argument("--disable-popup-blocking")

    # Force Version 142
    driver = uc.Chrome(options=options, version_main=142)

    all_jobs = []

    try:
        for region_name, base_url in REGIONS:
            print(f"\n--- Switching to Indeed {region_name} ---")
            
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
                        # --- 1. Basic Info ---
                        try:
                            title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
                            title = title_elem.text
                            link = title_elem.get_attribute("href")
                        except:
                            # Fallback
                            title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span")
                            title = title_elem.text
                            link = driver.current_url 

                        try: company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text
                        except: company = "N/A"

                        try: location = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text
                        except: location = "N/A"

                        # --- 2. Salary Strategy ---
                        salary = "Not Disclosed"

                        # A. Try Card Metadata First (Fastest)
                        try:
                            metadata = card.find_elements(By.CLASS_NAME, "metadata")
                            for m in metadata:
                                text = m.text
                                # FIX 1: Direct Currency Check on Card
                                if any(symbol in text for symbol in ['₹', '$', '€', '£', 'Lacs']):
                                    salary = text
                                    break
                        except: pass

                        # B. Right Pane Strategy (If card fails)
                        if salary == "Not Disclosed":
                            try:
                                card.click()
                                
                                # Prevent Stale Data: Wait for Right Pane Title to match Card Title
                                try:
                                    wait = WebDriverWait(driver, 5)
                                    wait.until(EC.text_to_be_present_in_element(
                                        (By.CSS_SELECTOR, "div.jobsearch-JobInfoHeader-title-container h2"), title
                                    ))
                                except:
                                    # If title doesn't match, the click probably failed or pane didn't load
                                    raise Exception("Right pane mismatch")

                                # Extract text from the shared Salary/JobType container
                                right_pane_text = driver.find_element(By.ID, "salaryInfoAndJobType").text
                                
                                # FIX 2: The Logic You Requested
                                # If the text contains '$' or '₹', we FORCE it to be the salary.
                                # This captures "$150,000 - $230,000 - Full Time" perfectly.
                                currency_indicators = ['$', '₹', '€', '£', 'Lacs']
                                
                                if any(symbol in right_pane_text for symbol in currency_indicators):
                                    salary = right_pane_text
                                # Fallback: If no symbol, but has digits + "Year"/"Month" (e.g. "60,000 a year")
                                elif any(char.isdigit() for char in right_pane_text) and \
                                     any(period in right_pane_text.lower() for period in ['year', 'month', 'pa']):
                                     salary = right_pane_text
                                     
                            except:
                                pass

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
                    except:
                        continue
            
    finally:
        try:
            driver.quit()
        except:
            pass

    print(f"   [Indeed] Total Found: {len(all_jobs)} jobs.")
    return all_jobs

if __name__ == "__main__":
    scrape_indeed()