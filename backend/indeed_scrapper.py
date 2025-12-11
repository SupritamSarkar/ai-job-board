import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Regions
REGIONS = [
    ("India", "https://in.indeed.com/jobs?q=ai+ml+engineer&l="),
    ("USA",   "https://www.indeed.com/jobs?q=ai+ml+engineer&l=") 
]

def scrape_indeed():
    print(f"[{datetime.now()}] Starting Indeed Scrape (Standard Selenium)...")

    # --- SETUP CHROME OPTIONS (Same as Naukri) ---
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-popup-blocking")
    
    # 1. Spoof User Agent to look like a real Windows PC
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # 2. Hide Selenium Automation Flags
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Initialize Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # 3. Patch navigator.webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    all_jobs = []

    try:
        for region_name, base_url in REGIONS:
            print(f"\n--- Switching to Indeed {region_name} ---")
            
            for page in range(0, 1): 
                start_param = page * 10
                url = f"{base_url}&start={start_param}"
                
                print(f"   [Indeed {region_name}] Navigating to Page {page + 1}...")
                driver.get(url)

                # Random sleep to behave like a human
                time.sleep(random.uniform(3, 5))

                # Check Title for Bot Detection
                if "challenge" in driver.title.lower() or "security" in driver.title.lower() or "cloudflare" in driver.title.lower():
                    print("   !!! Cloudflare/Security Challenge detected. Skipping page.")
                    continue

                try:
                    # Wait for job cards
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "mosaic-provider-jobcards"))
                    )
                except:
                    print(f"   Timeout on {region_name} page {page+1} (Possible blocking)")
                    continue

                job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
                print(f"   Found {len(job_cards)} cards. Processing...")

                for card in job_cards:
                    try:
                        # --- Basic Info ---
                        try:
                            title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
                            title = title_elem.text
                            link = title_elem.get_attribute("href")
                        except:
                            title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span")
                            title = title_elem.text
                            # Find parent 'a' tag or use current url
                            try: link = card.find_element(By.XPATH, ".//a").get_attribute("href")
                            except: link = driver.current_url

                        try: company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text
                        except: company = "N/A"

                        try: location = card.find_element(By.CSS_SELECTOR, "[data-testid='text-location']").text
                        except: location = "N/A"

                        # --- Salary Logic ---
                        salary = "Not Disclosed"

                        # A. Card Check
                        try:
                            metadata = card.find_elements(By.CLASS_NAME, "metadata")
                            for m in metadata:
                                text = m.text
                                if any(symbol in text for symbol in ['₹', '$', '€', '£', 'Lacs']):
                                    salary = text
                                    break
                        except: pass

                        # B. Right Pane Check (Click & Fetch)
                        if salary == "Not Disclosed":
                            try:
                                # Scroll into view to ensure clickability
                                driver.execute_script("arguments[0].scrollIntoView();", card)
                                try:
                                    card.click()
                                except:
                                    # Fallback js click if intercepted
                                    driver.execute_script("arguments[0].click();", card)
                                
                                # Wait briefly for right pane
                                time.sleep(2) 
                                
                                # Try to grab the right pane text
                                try:
                                    right_pane = driver.find_element(By.ID, "salaryInfoAndJobType")
                                    right_pane_text = right_pane.text
                                    
                                    currency_indicators = ['$', '₹', '€', '£', 'Lacs']
                                    if any(symbol in right_pane_text for symbol in currency_indicators):
                                        salary = right_pane_text
                                    elif any(char.isdigit() for char in right_pane_text) and \
                                         any(period in right_pane_text.lower() for period in ['year', 'month', 'pa']):
                                         salary = right_pane_text
                                except:
                                    pass
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
                    except Exception:
                        continue
            
    finally:
        driver.quit()

    print(f"   [Indeed] Total Found: {len(all_jobs)} jobs.")
    return all_jobs

if __name__ == "__main__":
    scrape_indeed()