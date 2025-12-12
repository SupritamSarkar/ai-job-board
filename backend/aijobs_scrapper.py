"""
AIJobs.ai Job Scraper
Scrapes AI/ML jobs from AIJobs.ai (7 pages)
Updated with correct CSS selectors from HTML structure
"""

import time
import random
import re
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
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver


def scrape_aijobs():
    """Scrape AI/ML jobs from AIJobs.ai (7 pages)"""
    print(f"[{datetime.now()}] Starting AIJobs.ai Scrape...")
    
    jobs = []
    driver = get_driver()
    base_url = "https://aijobs.ai/united-states"
    
    try:
        for page in range(1, 8):  # 7 pages
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}?page={page}"
            
            print(f"   [AIJobs] Scraping page {page}...")
            
            driver.get(url)
            time.sleep(random.uniform(2, 3))
            
            # Wait for job cards to load
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/job/']"))
                )
            except:
                print(f"   [AIJobs] Timeout on page {page}")
                continue
            
            # Scroll to load all content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Find job cards - each card is wrapped in an anchor tag
            # From HTML: <a href="https://aijobs.ai/job/sr-mlai-software-eng" class="tw-h-full card...">
            job_cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/job/'].tw-h-full, a.jobcardStyle1")
            
            if not job_cards:
                # Fallback - find all job links
                job_cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/job/']")
            
            processed_urls = set()
            page_jobs = 0
            
            for card in job_cards:
                try:
                    href = card.get_attribute("href")
                    
                    if not href or '/job/' not in href or href in processed_urls:
                        continue
                    if '/company/' in href or '/tag/' in href:
                        continue
                    
                    processed_urls.add(href)
                    
                    # Get card text for extraction
                    card_text = card.text
                    
                    # === TITLE ===
                    # From HTML: <div class="tw text-[#18191C] tw text-lg tw font-medium">Sr ML/AI Software Eng</div>
                    title = ""
                    try:
                        title_elem = card.find_element(By.CSS_SELECTOR, "[class*='font-medium'][class*='text-lg'], [class*='tw-card-title']")
                        title = title_elem.text.strip()
                    except:
                        # Fallback: first line of card text
                        lines = [l.strip() for l in card_text.split('\n') if l.strip()]
                        if lines:
                            title = lines[0]
                    
                    if not title or len(title) < 3:
                        continue
                    
                    # === COMPANY ===
                    # From HTML: <span class="tw-text-base tw-font-medium tw-text-[#18191C] tw-card-title">PlayStation Global</span>
                    company = "N/A"
                    try:
                        company_elem = card.find_element(By.CSS_SELECTOR, ".tw-card-title, .iconbox-content [class*='font-medium']")
                        company = company_elem.text.strip()
                    except:
                        # Fallback: look in lines
                        lines = [l.strip() for l in card_text.split('\n') if l.strip()]
                        for line in lines[1:]:  # Skip title
                            if line and line != title and '$' not in line and 'Full Time' not in line and not line.endswith('D'):
                                company = line
                                break
                    
                    # === LOCATION ===
                    # From HTML: <span class="tw-location">United States</span>
                    location = "N/A"
                    try:
                        loc_elem = card.find_element(By.CSS_SELECTOR, ".tw-location, [class*='location']")
                        location = loc_elem.text.strip()
                    except:
                        # Fallback: search in text
                        for line in card_text.split('\n'):
                            line = line.strip()
                            if any(loc in line.lower() for loc in ['united states', 'remote', 'usa', 'india', 'canada', 'uk', 'germany']):
                                location = line
                                break
                    
                    # === SALARY (CRITICAL) ===
                    # From HTML: <span class="tw-text-sm tw-text-[#767F8C]">" Salary: $177,300 - $265,900 "</span>
                    salary = "Not Disclosed"
                    try:
                        # Look for salary in card text - contains "$" and "Salary:"
                        salary_match = re.search(r'Salary:\s*\$[\d,]+\s*-\s*\$[\d,]+', card_text)
                        if salary_match:
                            salary = salary_match.group().replace('Salary:', '').strip()
                        else:
                            # Alternative: just $ amounts
                            salary_match = re.search(r'\$[\d,]+\s*-\s*\$[\d,]+', card_text)
                            if salary_match:
                                salary = salary_match.group().strip()
                    except:
                        pass
                    
                    # === JOB TYPE ===
                    # From HTML: <span class="tw-text-[#00A02C] tw-text-[12px]...">Full Time</span>
                    job_type = "Full Time"
                    try:
                        job_type_elem = card.find_element(By.CSS_SELECTOR, "[class*='#00A02C'], [class*='rounded']")
                        type_text = job_type_elem.text.strip()
                        if type_text in ['Full Time', 'Part Time', 'Contract', 'Internship']:
                            job_type = type_text
                    except:
                        if 'Part Time' in card_text:
                            job_type = "Part Time"
                        elif 'Contract' in card_text:
                            job_type = "Contract"
                    
                    # Check if remote
                    if 'remote' in card_text.lower():
                        if job_type == "Full Time":
                            job_type = "Full Time, Remote"
                        else:
                            job_type += ", Remote"
                    
                    # === POSTED DATE ===
                    # From HTML: <div class="tw-text-sm tw-text-[#767F8C] mt-1 tw-pl-3">5D</div>
                    posted_date = ""
                    try:
                        date_match = re.search(r'(\d+)D', card_text)
                        if date_match:
                            posted_date = f"{date_match.group(1)} days ago"
                        else:
                            date_match = re.search(r'(\d+)W', card_text)
                            if date_match:
                                posted_date = f"{date_match.group(1)} weeks ago"
                            else:
                                date_match = re.search(r'(\d+)H', card_text)
                                if date_match:
                                    posted_date = f"{date_match.group(1)} hours ago"
                    except:
                        pass
                    
                    jobs.append({
                        "Title": title,
                        "Company": company,
                        "Experience": job_type,
                        "Location": location,
                        "Description": f"Posted: {posted_date}" if posted_date else "AI/ML Job",
                        "Salary": salary,
                        "Link": href,
                        "Site": "AIJobs.ai",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
                    page_jobs += 1
                    
                except Exception as e:
                    continue
            
            print(f"   [AIJobs] Page {page}: Found {page_jobs} jobs")
            
    except Exception as e:
        print(f"   [AIJobs] Error: {e}")
    finally:
        driver.quit()
    
    # Remove duplicates
    seen_links = set()
    unique_jobs = []
    for job in jobs:
        if job['Link'] not in seen_links:
            seen_links.add(job['Link'])
            unique_jobs.append(job)
    
    print(f"   [AIJobs] Total Unique Jobs Found: {len(unique_jobs)}")
    return unique_jobs


if __name__ == "__main__":
    import json
    jobs = scrape_aijobs()
