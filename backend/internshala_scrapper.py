"""
Internshala Internship Scraper
Scrapes AI/ML internships from Internshala (7 pages)
"""

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


def get_driver():
    """Create and return a configured Chrome driver"""
    chrome_options = Options()
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
    
    return driver


def scrape_internshala():
    """Scrape AI/ML internships from Internshala (7 pages)"""
    print(f"[{datetime.now()}] Starting Internshala Internship Scrape...")
    
    internships = []
    driver = get_driver()
    
    try:
        for page in range(1, 8):  # 7 pages
            if page == 1:
                url = "https://internshala.com/internships/machine-learning-internship/"
            else:
                url = f"https://internshala.com/internships/machine-learning-internship/page-{page}/"
            
            print(f"   [Internshala] Scraping Page {page}...")
            driver.get(url)
            
            time.sleep(random.uniform(2, 4))
            
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "internship_meta"))
                )
            except:
                print(f"   [Internshala] Timeout on page {page}")
                continue
            
            job_cards = driver.find_elements(By.CLASS_NAME, "internship_meta")
            
            for card in job_cards:
                try:
                    # Title & Link
                    title_elem = card.find_element(By.CSS_SELECTOR, "a.job-title-href")
                    title = title_elem.text.strip()
                    href = title_elem.get_attribute("href")
                    link = "https://internshala.com" + href if href.startswith("/") else href
                    
                    # Company
                    try:
                        company = card.find_element(By.CLASS_NAME, "company_name").text.strip()
                    except:
                        company = "N/A"
                    
                    # Location
                    try:
                        location = card.find_element(By.CSS_SELECTOR, "a.location_link").text.strip()
                    except:
                        try:
                            location = card.find_element(By.CSS_SELECTOR, ".location").text.strip()
                        except:
                            location = "N/A"
                    
                    # Stipend
                    try:
                        stipend = card.find_element(By.CLASS_NAME, "stipend").text.strip()
                    except:
                        stipend = "Not Disclosed"
                    
                    # Duration
                    try:
                        duration = card.find_element(By.CLASS_NAME, "duration").text.strip()
                    except:
                        duration = "N/A"
                    
                    internships.append({
                        "Title": title,
                        "Company": company,
                        "Experience": "Internship",
                        "Location": location,
                        "Description": f"Duration: {duration}",
                        "Salary": stipend,
                        "Link": link,
                        "Site": "Internshala",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
                except:
                    continue
            
            print(f"   [Internshala] Page {page}: {len(job_cards)} internships found")
                
    except Exception as e:
        print(f"   [Internshala] Error: {e}")
    finally:
        driver.quit()
    
    print(f"   [Internshala] Total Found: {len(internships)} internships.")
    return internships


if __name__ == "__main__":
    internships = scrape_internshala()
    print(f"\n=== Scraped {len(internships)} internships ===")
    for intern in internships[:5]:
        print(f"  - {intern['Title']} at {intern['Company']} ({intern['Salary']})")
