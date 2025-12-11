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

SEARCH_URL = "https://www.naukri.com/ai-ml-engineer-jobs?k=ai%20ml%20engineer"

def scrape_naukri():
    print(f"[{datetime.now()}] Starting Naukri Scrape...")
    
    chrome_options = Options()
    # comment out headless if you want to debug visually, but it should work with the UA string below
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # IMPORTANT: Real User Agent to bypass basic bot detection
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Disable automation flags
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Script to hide selenium property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    all_jobs = []

    try:
        for page in range(1, 7):
            url = SEARCH_URL if page == 1 else SEARCH_URL.replace("?", f"-{page}?")
            print(f"   [Naukri] Scraping Page {page}...")
            
            driver.get(url)
            
            # Explicit wait for the job list container
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
                )
            except:
                print(f"   [Naukri] Timeout waiting for jobs on page {page}")
                continue
            
            # Small random sleep to mimic human behavior
            time.sleep(random.uniform(2, 4))
            
            job_cards = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")
            
            for card in job_cards:
                try:
                    # Title & Link
                    title_elem = card.find_element(By.CSS_SELECTOR, "a.title")
                    title = title_elem.text
                    link = title_elem.get_attribute("href")
                    
                    # Company
                    try: company = card.find_element(By.CSS_SELECTOR, "a.comp-name").text
                    except: company = "N/A"
                    
                    # Experience
                    try: experience = card.find_element(By.CSS_SELECTOR, "span.expwdth").text
                    except: experience = "N/A"
                        
                    # Location
                    try: location = card.find_element(By.CSS_SELECTOR, "span.locWdth").text
                    except: location = "N/A"
                    
                    # Salary - Updated logic
                    salary = "Not Disclosed"
                    try:
                        salary_elem = card.find_element(By.CSS_SELECTOR, "span.sal-wrap")
                        salary = salary_elem.text
                        if "Not disclosed" in salary or not salary:
                            # Try getting title attribute if text is hidden
                            salary = salary_elem.find_element(By.TAG_NAME, "span").get_attribute("title")
                    except:
                        pass

                    all_jobs.append({
                        "Title": title,
                        "Company": company,
                        "Experience": experience,
                        "Location": location,
                        "Description": "See Link", # Naukri descriptions are often hidden now
                        "Salary": salary,
                        "Link": link,
                        "Site": "Naukri",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
                except Exception as e:
                    continue
                    
    except Exception as e:
        print(f"   [Naukri] Error: {e}")
    finally:
        driver.quit()
        
    print(f"   [Naukri] Found {len(all_jobs)} jobs.")
    return all_jobs

if __name__ == "__main__":
    scrape_naukri()