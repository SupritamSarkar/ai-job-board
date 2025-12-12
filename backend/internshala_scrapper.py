"""
Internshala Internship Scraper
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


def extract_internship_from_detail_page(url):
    """Extract internship details from detail page - each call creates its own driver"""
    driver = None
    try:
        driver = get_driver()
        driver.get(url)
        time.sleep(1)  # Reduced wait time
        
        data = {
            "Title": "",
            "Company": "",
            "Location": "",
            "Stipend": "Not Disclosed",
            "Duration": "N/A",
            "Link": url
        }
        
        # Title
        try:
            title_elem = driver.find_element(By.CSS_SELECTOR, ".heading_4_5.profile_heading, h1.heading_4_5, .profile_heading")
            data["Title"] = title_elem.text.strip()
        except:
            try:
                title_elem = driver.find_element(By.CSS_SELECTOR, "h1")
                data["Title"] = title_elem.text.strip().replace(" - Internship", "")
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
        
        # Stipend
        try:
            stipend_elem = driver.find_element(By.CSS_SELECTOR, ".stipend_container_outer .stipend, .stipend")
            data["Stipend"] = stipend_elem.text.strip()
        except:
            try:
                page_text = driver.find_element(By.TAG_NAME, "body").text
                stipend_match = re.search(r'₹\s*[\d,]+\s*(?:-\s*[\d,]+)?\s*/month', page_text)
                if stipend_match:
                    data["Stipend"] = stipend_match.group().strip()
            except:
                pass
        
        # Duration
        try:
            page_text = driver.find_element(By.TAG_NAME, "body").text
            duration_match = re.search(r'(\d+)\s*(?:Month|Months|Week|Weeks)', page_text, re.IGNORECASE)
            if duration_match:
                data["Duration"] = duration_match.group()
        except:
            pass
        
        return data
        
    except Exception as e:
        return {"Title": "", "Link": url}
    finally:
        if driver:
            driver.quit()


def scrape_internshala():
    """Scrape AI/ML internships from Internshala - FAST parallel version"""
    print(f"[{datetime.now()}] Starting Internshala Internship Scrape (FAST Mode)...")
    
    internships = []
    driver = get_driver()
    
    try:
        # First, collect all internship links (fast - single driver)
        all_links = []
        
        for page in range(1, 6):  # 5 pages
            if page == 1:
                url = "https://internshala.com/internships/machine-learning-internship/"
            else:
                url = f"https://internshala.com/internships/machine-learning-internship/page-{page}/"
            
            print(f"   [Internshala] Collecting links from Page {page}...")
            driver.get(url)
            time.sleep(2)
            
            # Quick scroll
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Get all internship links
            link_elems = driver.find_elements(By.CSS_SELECTOR, "a[href*='/internship/detail/']")
            for elem in link_elems:
                href = elem.get_attribute("href")
                if href and href not in all_links:
                    all_links.append(href)
        
        driver.quit()
        print(f"\n   [Internshala] Found {len(all_links)} unique links. Starting parallel scrape...")
        
        # Parallel scraping with 5 workers
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(extract_internship_from_detail_page, link): link for link in all_links}
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                if completed % 10 == 0:
                    print(f"   [Internshala] Processed {completed}/{len(all_links)}...")
                
                try:
                    data = future.result()
                    if data and data.get("Title"):
                        internships.append({
                            "Title": data["Title"],
                            "Company": data.get("Company", "N/A"),
                            "Experience": "Internship",
                            "Location": data.get("Location", "Remote"),
                            "Description": f"Duration: {data.get('Duration', 'N/A')}",
                            "Salary": data.get("Stipend", "Not Disclosed"),
                            "Link": data["Link"],
                            "Site": "Internshala",
                            "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        })
                except:
                    continue
            
    except Exception as e:
        print(f"   [Internshala] Error: {e}")
        if driver:
            driver.quit()
    
    print(f"   [Internshala] Total Found: {len(internships)} internships.")
    return internships


if __name__ == "__main__":
    import json
    internships = scrape_internshala()
