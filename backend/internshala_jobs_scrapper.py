"""
Internshala Jobs Scraper (Fresher Jobs)
Scrapes AI/ML/Tech jobs from Internshala's Jobs section (7 pages)
Since Internshala internship scraper works, this should work too!
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


def scrape_internshala_jobs():
    """Scrape AI/ML/Tech jobs from Internshala Jobs section (7 pages)"""
    print(f"[{datetime.now()}] Starting Internshala Jobs Scrape...")
    
    jobs = []
    driver = get_driver()
    
    # URLs for different job categories on Internshala
    job_urls = [
        ("Data Science", "https://internshala.com/fresher-jobs/data-science-jobs/"),
        ("Machine Learning", "https://internshala.com/fresher-jobs/machine-learning-jobs/"),
        ("Software Development", "https://internshala.com/fresher-jobs/software-development-jobs/"),
    ]
    
    try:
        for category, base_url in job_urls:
            for page in range(1, 8):  # 7 pages per category
                if page == 1:
                    url = base_url
                else:
                    url = f"{base_url}page-{page}/"
                
                print(f"   [Internshala Jobs] Scraping {category} - Page {page}...")
                driver.get(url)
                
                time.sleep(random.uniform(2, 4))
                
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "individual_job"))
                    )
                except:
                    # Try alternate class name
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "job-tile"))
                        )
                    except:
                        print(f"   [Internshala Jobs] Timeout on {category} page {page}")
                        continue
                
                # Try multiple selectors for job cards
                job_cards = driver.find_elements(By.CLASS_NAME, "individual_job")
                if not job_cards:
                    job_cards = driver.find_elements(By.CLASS_NAME, "job-tile")
                if not job_cards:
                    job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-listing-card")
                
                for card in job_cards:
                    try:
                        # Title & Link
                        try:
                            title_elem = card.find_element(By.CSS_SELECTOR, "a.job-title-href")
                        except:
                            try:
                                title_elem = card.find_element(By.CSS_SELECTOR, "a.job_title")
                            except:
                                title_elem = card.find_element(By.CSS_SELECTOR, "h3 a")
                        
                        title = title_elem.text.strip()
                        href = title_elem.get_attribute("href")
                        link = "https://internshala.com" + href if href.startswith("/") else href
                        
                        # Company
                        try:
                            company = card.find_element(By.CLASS_NAME, "company_name").text.strip()
                        except:
                            try:
                                company = card.find_element(By.CSS_SELECTOR, ".company-name").text.strip()
                            except:
                                company = "N/A"
                        
                        # Location
                        try:
                            location = card.find_element(By.CSS_SELECTOR, "a.location_link").text.strip()
                        except:
                            try:
                                location = card.find_element(By.CLASS_NAME, "location").text.strip()
                            except:
                                location = "N/A"
                        
                        # Salary
                        try:
                            salary = card.find_element(By.CLASS_NAME, "salary").text.strip()
                        except:
                            try:
                                salary = card.find_element(By.CSS_SELECTOR, ".stipend").text.strip()
                            except:
                                salary = "Not Disclosed"
                        
                        # Experience
                        try:
                            experience = card.find_element(By.CLASS_NAME, "experience").text.strip()
                        except:
                            experience = "Fresher"
                        
                        if title and link:
                            jobs.append({
                                "Title": title,
                                "Company": company,
                                "Experience": experience,
                                "Location": location,
                                "Description": f"Category: {category}",
                                "Salary": salary,
                                "Link": link,
                                "Site": "Internshala Jobs",
                                "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            })
                    except:
                        continue
                
                print(f"   [Internshala Jobs] Page {page}: {len(job_cards)} jobs found")
                
    except Exception as e:
        print(f"   [Internshala Jobs] Error: {e}")
    finally:
        driver.quit()
    
    # Remove duplicates
    seen_links = set()
    unique_jobs = []
    for job in jobs:
        if job['Link'] not in seen_links:
            seen_links.add(job['Link'])
            unique_jobs.append(job)
    
    print(f"   [Internshala Jobs] Total Found: {len(unique_jobs)} jobs.")
    return unique_jobs


if __name__ == "__main__":
    jobs = scrape_internshala_jobs()
    print(f"\n=== Scraped {len(jobs)} jobs ===")
    for job in jobs[:5]:
        print(f"  - {job['Title']} at {job['Company']} ({job['Salary']})")
