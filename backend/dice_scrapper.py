"""
Dice.com Job Scraper
Scrapes Machine Learning jobs from Dice.com
Updated with correct CSS selectors
"""

import time
import random
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    """Create and return a configured Chrome driver with anti-detection"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.page_load_strategy = 'eager'
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver


def scrape_dice():
    """Scrape Machine Learning jobs from Dice.com"""
    print(f"[{datetime.now()}] Starting Dice.com Scrape...")
    
    jobs = []
    driver = get_driver()
    
    try:
        for page in range(1, 8):  # 7 pages
            url = f"https://www.dice.com/jobs?q=machine+learning&page={page}"
            print(f"   [Dice] Scraping page {page}...")
            
            driver.get(url)
            time.sleep(random.uniform(3, 5))
            
            # Scroll to load all content
            for i in range(5):
                driver.execute_script(f"window.scrollTo(0, {400 * (i + 1)});")
                time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Find title links - these have text-xl and font-semibold class
            # Selector: a[href*='/job-detail/'][class*='text-xl']
            title_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/job-detail/'][class*='text-xl'], a[href*='/job-detail/'][class*='font-semibold']")
            
            if not title_links:
                # Fallback to any job-detail links
                title_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/job-detail/']")
            
            print(f"   [Dice] Found {len(title_links)} job links")
            
            processed_urls = set()
            page_jobs = 0
            
            for link in title_links:
                try:
                    href = link.get_attribute("href")
                    
                    if not href or href in processed_urls:
                        continue
                    
                    processed_urls.add(href)
                    
                    # === TITLE ===
                    title = link.text.strip()
                    
                    if not title or len(title) < 5 or title.lower() in ['apply', 'view', 'easy apply']:
                        continue
                    
                    # Get parent card for more info
                    card = link
                    card_text = ""
                    for _ in range(8):
                        try:
                            card = card.find_element(By.XPATH, "..")
                            card_text = card.text
                            # Stop when we have enough content
                            if 'USD' in card_text or 'per year' in card_text.lower() or len(card_text) > 200:
                                break
                        except:
                            break
                    
                    lines = [l.strip() for l in card_text.split('\n') if l.strip()]
                    
                    # === COMPANY ===
                    # Company link: a[href*='/company-profile/'] p
                    company = "N/A"
                    try:
                        company_elem = card.find_element(By.CSS_SELECTOR, "a[href*='/company-profile/'] p, a[href*='/company-profile/']")
                        company = company_elem.text.strip()
                    except:
                        # Fallback: find company from text
                        for line in lines:
                            if line != title and 'USD' not in line and '$' not in line and 'per year' not in line.lower():
                                if len(line) > 2 and len(line) < 50 and not line[0].isdigit():
                                    company = line
                                    break
                    
                    # === LOCATION ===
                    location = "N/A"
                    for line in lines:
                        # US states pattern
                        states = ['California', 'New York', 'Texas', 'Virginia', 'Washington', 'Florida', 
                                 'Illinois', 'Massachusetts', 'Colorado', 'Georgia', 'Arizona', 'Ohio',
                                 'Pennsylvania', 'North Carolina', 'Oregon', 'New Jersey', 'Minnesota']
                        if any(state in line for state in states):
                            location = line.split('•')[0].strip() if '•' in line else line.strip()
                            break
                        if 'Remote' in line:
                            location = "Remote"
                            break
                    
                    # === SALARY (CRITICAL) ===
                    salary = "Not Disclosed"
                    for line in lines:
                        # Pattern: "USD 193,400.00 - 220,700.00 per year"
                        if 'USD' in line and 'per year' in line.lower():
                            salary = line.strip()
                            break
                        # Pattern: "$X - $Y per hour/year"
                        if '$' in line and ('per year' in line.lower() or 'per hour' in line.lower()):
                            salary = line.strip()
                            break
                        if 'Depends on Experience' in line:
                            salary = "Depends on Experience"
                            break
                    
                    # === EMPLOYMENT TYPE ===
                    employment_type = "Full-time"
                    card_lower = card_text.lower()
                    if 'contract' in card_lower:
                        employment_type = "Contract"
                    elif 'third party' in card_lower:
                        employment_type = "Third Party"
                    elif 'part-time' in card_lower:
                        employment_type = "Part-time"
                    
                    jobs.append({
                        "Title": title,
                        "Company": company,
                        "Experience": employment_type,
                        "Location": location,
                        "Description": "Machine Learning Job from Dice.com",
                        "Salary": salary,
                        "Link": href,
                        "Site": "Dice",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
                    page_jobs += 1
                    
                except Exception as e:
                    continue
            
            print(f"   [Dice] Page {page}: Found {page_jobs} jobs")
            
    except Exception as e:
        print(f"   [Dice] Error: {e}")
    finally:
        driver.quit()
    
    # Remove duplicates
    seen_links = set()
    unique_jobs = []
    for job in jobs:
        if job['Link'] not in seen_links:
            seen_links.add(job['Link'])
            unique_jobs.append(job)
    
    print(f"   [Dice] Total Unique Jobs Found: {len(unique_jobs)}")
    return unique_jobs


if __name__ == "__main__":
    jobs = scrape_dice()