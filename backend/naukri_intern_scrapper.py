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

# Internship Specific URL
SEARCH_URL = "https://www.naukri.com/ai-ml-engineer-internship-jobs?k=ai%20ml%20engineer%20internship&qproductJobSource=2&qinternshipFlag=true&naukriCampus=true&experience=0"

def scrape_naukri_intern():
    print(f"[{datetime.now()}] Starting Naukri Internship Scrape...")
    
    chrome_options = Options()
    # Use headless=new for better stability
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    all_internships = []

    try:
        # Scrape 6 pages for internships
        for page in range(1, 8):  # 7 pages
            # Logic to handle pagination in the URL
            url = SEARCH_URL if page == 1 else SEARCH_URL.replace("?", f"-{page}?")
            print(f"   [Naukri Intern] Scraping Page {page}...")
            
            driver.get(url)
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
                )
            except:
                print(f"   [Naukri Intern] Timeout on page {page}")
                continue
            
            time.sleep(random.uniform(2, 4))
            
            job_cards = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")
            
            for card in job_cards:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, "a.title")
                    title = title_elem.text
                    link = title_elem.get_attribute("href")
                    
                    try: company = card.find_element(By.CSS_SELECTOR, "a.comp-name").text
                    except: company = "N/A"
                    
                    try: location = card.find_element(By.CSS_SELECTOR, "span.locWdth").text
                    except: location = "N/A"
                    
                    salary = "Not Disclosed"
                    try:
                        salary_elem = card.find_element(By.CSS_SELECTOR, "span.sal-wrap")
                        salary = salary_elem.text
                        if "Not disclosed" in salary or not salary:
                            salary = salary_elem.find_element(By.TAG_NAME, "span").get_attribute("title")
                    except:
                        pass

                    all_internships.append({
                        "Title": title,
                        "Company": company,
                        "Experience": "Internship", # Hardcoded for clarity
                        "Location": location,
                        "Description": "See Link",
                        "Salary": salary,
                        "Link": link,
                        "Site": "Naukri",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
                except Exception:
                    continue
                    
    except Exception as e:
        print(f"   [Naukri Intern] Error: {e}")
    finally:
        driver.quit()
        
    print(f"   [Naukri Intern] Found {len(all_internships)} internships.")
    return all_internships

if __name__ == "__main__":
    scrape_naukri_intern()