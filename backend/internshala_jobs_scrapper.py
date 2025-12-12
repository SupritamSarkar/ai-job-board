"""
Internshala Jobs Scraper (Fresher Jobs)
FAST version - uses parallel processing to visit detail pages
"""

import time
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.page_load_strategy = 'eager'  # Don't wait for all resources
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.set_page_load_timeout(15)
    
    return driver


def extract_job_from_detail_page(url):
    """Extract job details from detail page - each call creates its own driver"""
    driver = None
    try:
        driver = get_driver()
        driver.get(url)
        time.sleep(1)  # Reduced wait time
        
        data = {
            "Title": "",
            "Company": "",
            "Location": "",
            "Salary": "Not Disclosed",
            "Experience": "Fresher",
            "Link": url
        }
        
        # Title
        try:
            title_elem = driver.find_element(By.CSS_SELECTOR, ".heading_4_5.profile_heading, h1.heading_4_5, .profile_heading")
            data["Title"] = title_elem.text.strip()
        except:
            try:
                title_elem = driver.find_element(By.CSS_SELECTOR, "h1")
                data["Title"] = title_elem.text.strip().replace(" - Job", "")
            except:
                pass
        
        # Company
        try:
            company_elem = driver.find_element(By.CSS_SELECTOR, ".company_name a, .company_name")
            data["Company"] = company_elem.text.strip()
        except:
            pass
        
        # Location
        try:
            loc_elem = driver.find_element(By.CSS_SELECTOR, "#location_names a, .location_link, [id*='location']")
            data["Location"] = loc_elem.text.strip()
        except:
            pass
        
        # Salary/CTC
        try:
            salary_elem = driver.find_element(By.CSS_SELECTOR, ".salary_container .salary, .salary, .stipend")
            data["Salary"] = salary_elem.text.strip()
        except:
            try:
                page_text = driver.find_element(By.TAG_NAME, "body").text
                salary_match = re.search(r'₹\s*[\d,]+\s*(?:-\s*[\d,]+)?\s*(?:/year|/month|LPA)?', page_text)
                if salary_match:
                    data["Salary"] = salary_match.group().strip()
            except:
                pass
        
        # Experience
        try:
            page_text = driver.find_element(By.TAG_NAME, "body").text
            exp_match = re.search(r'(\d+)\s*(?:-\s*(\d+))?\s*(?:year|years)', page_text, re.IGNORECASE)
            if exp_match:
                data["Experience"] = exp_match.group()
        except:
            pass
        
        return data
        
    except Exception as e:
        return {"Title": "", "Link": url}
    finally:
        if driver:
            driver.quit()


def scrape_internshala_jobs():
    """Scrape AI/ML/Tech jobs from Internshala - FAST parallel version"""
    print(f"[{datetime.now()}] Starting Internshala Jobs Scrape (FAST Mode)...")
    
    jobs = []
    driver = get_driver()
    
    job_urls = [
        ("Data Science", "https://internshala.com/fresher-jobs/data-science-jobs/"),
        ("Machine Learning", "https://internshala.com/fresher-jobs/machine-learning-jobs/"),
    ]
    
    try:
        # First, collect all job links (fast - single driver)
        all_links = []
        
        for category, base_url in job_urls:
            for page in range(1, 5):  # 4 pages
                if page == 1:
                    url = base_url
                else:
                    url = f"{base_url}page-{page}/"
                
                print(f"   [Internshala Jobs] Collecting {category} links from Page {page}...")
                driver.get(url)
                time.sleep(2)
                
                # Quick scroll
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                # Get all job links
                link_elems = driver.find_elements(By.CSS_SELECTOR, "a[href*='/job/detail/']")
                for elem in link_elems:
                    href = elem.get_attribute("href")
                    if href and href not in all_links:
                        all_links.append(href)
        
        driver.quit()
        print(f"\n   [Internshala Jobs] Found {len(all_links)} unique links. Starting parallel scrape...")
        
        # Parallel scraping with 5 workers
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(extract_job_from_detail_page, link): link for link in all_links}
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                if completed % 10 == 0:
                    print(f"   [Internshala Jobs] Processed {completed}/{len(all_links)}...")
                
                try:
                    data = future.result()
                    if data and data.get("Title"):
                        jobs.append({
                            "Title": data["Title"],
                            "Company": data.get("Company", "N/A"),
                            "Experience": data.get("Experience", "Fresher"),
                            "Location": data.get("Location", "N/A"),
                            "Description": "Fresher Job",
                            "Salary": data.get("Salary", "Not Disclosed"),
                            "Link": data["Link"],
                            "Site": "Internshala Jobs",
                            "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        })
                except:
                    continue
            
    except Exception as e:
        print(f"   [Internshala Jobs] Error: {e}")
        if driver:
            driver.quit()
    
    print(f"   [Internshala Jobs] Total Found: {len(jobs)} jobs.")
    return jobs


if __name__ == "__main__":
    import json
    jobs = scrape_internshala_jobs()
