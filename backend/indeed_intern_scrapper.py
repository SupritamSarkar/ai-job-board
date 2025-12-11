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

# NEW IMPORT
from selenium_stealth import stealth

REGIONS = [
    ("India", "https://in.indeed.com/jobs?q=ai+ml+engineer+intern&l="),
    ("USA",   "https://www.indeed.com/jobs?q=ai+ml+intern&l=") 
]

def scrape_indeed_intern():
    print(f"[{datetime.now()}] Starting Indeed Internship Scrape (Stealth Mode)...")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # --- ACTIVATE STEALTH MODE ---
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    all_internships = []

    try:
        for region_name, base_url in REGIONS:
            print(f"\n--- Switching to Indeed {region_name} (Internships) ---")
            
            for page in range(0, 1): 
                start_param = page * 10
                url = f"{base_url}&start={start_param}"
                
                print(f"   [Indeed {region_name}] Navigating to Page {page + 1}...")
                driver.get(url)

                time.sleep(random.uniform(4, 7))

                if "challenge" in driver.title.lower() or "security" in driver.title.lower():
                    print("   !!! Cloudflare detected. Skipping.")
                    continue

                try:
                    WebDriverWait(driver, 10).until(
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
                            try:
                                title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span")
                                title = title_elem.text
                                link = card.find_element(By.XPATH, ".//a").get_attribute("href")
                            except: continue

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
                                if any(symbol in text for symbol in ['₹', '$', '€', '£', 'Lacs', 'stipend']):
                                    salary = text
                                    break
                        except: pass

                        # Click Check
                        if salary == "Not Disclosed":
                            try:
                                driver.execute_script("arguments[0].scrollIntoView();", card)
                                driver.execute_script("arguments[0].click();", card)
                                time.sleep(2)
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
        driver.quit()

    print(f"   [Indeed] Total Found: {len(all_internships)} internships.")
    return all_internships

if __name__ == "__main__":
    scrape_indeed_intern()