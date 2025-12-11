"""
Multi-Source Job Scraper using Selenium
Scrapes AI/ML jobs from TimesJobs, Shine.com, and Freshersworld
Uses same approach as Naukri scraper (Selenium with headless Chrome)
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


# ===========================================
# 1. TimesJobs Scraper
# ===========================================
def scrape_timesjobs():
    """Scrape AI/ML jobs from TimesJobs"""
    print("   [TimesJobs] Starting scrape...")
    jobs = []
    
    driver = get_driver()
    
    try:
        url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personal498&from=submit&txtKeyword=ai+ml+engineer&cboPresFuncArea=35"
        driver.get(url)
        
        time.sleep(random.uniform(3, 5))
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-bx"))
            )
        except:
            print("   [TimesJobs] Timeout waiting for jobs")
            driver.quit()
            return jobs
        
        job_cards = driver.find_elements(By.CLASS_NAME, "job-bx")
        
        for card in job_cards:
            try:
                # Title & Link
                title_elem = card.find_element(By.CSS_SELECTOR, "h2 a")
                title = title_elem.text.strip()
                link = title_elem.get_attribute("href")
                
                # Company
                try:
                    company = card.find_element(By.CLASS_NAME, "joblist-comp-name").text.strip()
                except:
                    company = "N/A"
                
                # Experience
                try:
                    exp_list = card.find_elements(By.CSS_SELECTOR, "ul.top-jd-dtl li")
                    experience = exp_list[0].text.strip() if exp_list else "N/A"
                except:
                    experience = "N/A"
                
                # Location
                try:
                    location_list = card.find_elements(By.CSS_SELECTOR, "ul.top-jd-dtl li")
                    location = location_list[2].text.strip() if len(location_list) > 2 else "N/A"
                except:
                    location = "N/A"
                
                jobs.append({
                    "Title": title,
                    "Company": company,
                    "Experience": experience,
                    "Location": location,
                    "Description": "See Link",
                    "Salary": "Not Disclosed",
                    "Link": link,
                    "Site": "TimesJobs"
                })
            except:
                continue
                
        print(f"   [TimesJobs] Found {len(jobs)} jobs")
        
    except Exception as e:
        print(f"   [TimesJobs] Error: {e}")
    finally:
        driver.quit()
    
    return jobs


# ===========================================
# 2. Shine.com Scraper
# ===========================================
def scrape_shine():
    """Scrape AI/ML jobs from Shine.com"""
    print("   [Shine] Starting scrape...")
    jobs = []
    
    driver = get_driver()
    
    try:
        url = "https://www.shine.com/job-search/ai-ml-engineer-jobs"
        driver.get(url)
        
        time.sleep(random.uniform(3, 5))
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobCard"))
            )
        except:
            print("   [Shine] Timeout waiting for jobs")
            driver.quit()
            return jobs
        
        job_cards = driver.find_elements(By.CLASS_NAME, "jobCard")
        
        for card in job_cards:
            try:
                # Title & Link
                title_elem = card.find_element(By.CSS_SELECTOR, "a.title")
                title = title_elem.text.strip()
                link = title_elem.get_attribute("href")
                
                # Company
                try:
                    company = card.find_element(By.CLASS_NAME, "companyName").text.strip()
                except:
                    company = "N/A"
                
                # Experience
                try:
                    experience = card.find_element(By.CLASS_NAME, "exp").text.strip()
                except:
                    experience = "N/A"
                
                # Location
                try:
                    location = card.find_element(By.CLASS_NAME, "loc").text.strip()
                except:
                    location = "N/A"
                
                # Salary
                try:
                    salary = card.find_element(By.CLASS_NAME, "salary").text.strip()
                except:
                    salary = "Not Disclosed"
                
                jobs.append({
                    "Title": title,
                    "Company": company,
                    "Experience": experience,
                    "Location": location,
                    "Description": "See Link",
                    "Salary": salary,
                    "Link": link,
                    "Site": "Shine"
                })
            except:
                continue
                
        print(f"   [Shine] Found {len(jobs)} jobs")
        
    except Exception as e:
        print(f"   [Shine] Error: {e}")
    finally:
        driver.quit()
    
    return jobs


# ===========================================
# 3. Freshersworld Scraper
# ===========================================
def scrape_freshersworld():
    """Scrape AI/ML jobs from Freshersworld"""
    print("   [Freshersworld] Starting scrape...")
    jobs = []
    
    driver = get_driver()
    
    try:
        url = "https://www.freshersworld.com/jobs/category/ai-ml-jobs"
        driver.get(url)
        
        time.sleep(random.uniform(3, 5))
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-container"))
            )
        except:
            print("   [Freshersworld] Timeout waiting for jobs")
            driver.quit()
            return jobs
        
        job_cards = driver.find_elements(By.CLASS_NAME, "job-container")
        
        for card in job_cards:
            try:
                # Title & Link
                title_elem = card.find_element(By.CSS_SELECTOR, "a.job-title")
                title = title_elem.text.strip()
                link = title_elem.get_attribute("href")
                
                # Company
                try:
                    company = card.find_element(By.CLASS_NAME, "company-name").text.strip()
                except:
                    company = "N/A"
                
                # Location
                try:
                    location = card.find_element(By.CLASS_NAME, "job-location").text.strip()
                except:
                    location = "N/A"
                
                jobs.append({
                    "Title": title,
                    "Company": company,
                    "Experience": "Fresher",
                    "Location": location,
                    "Description": "See Link",
                    "Salary": "Not Disclosed",
                    "Link": link,
                    "Site": "Freshersworld"
                })
            except:
                continue
                
        print(f"   [Freshersworld] Found {len(jobs)} jobs")
        
    except Exception as e:
        print(f"   [Freshersworld] Error: {e}")
    finally:
        driver.quit()
    
    return jobs


# ===========================================
# MAIN SCRAPE FUNCTION
# ===========================================
def scrape_indeed():
    """
    Multi-source job scraper using Selenium
    Scrapes from: TimesJobs, Shine.com, Freshersworld
    """
    print(f"[{datetime.now()}] Starting Multi-Source Job Scrape (Selenium)...")
    
    all_jobs = []
    
    # Scrape from all sources
    all_jobs.extend(scrape_timesjobs())
    time.sleep(2)
    all_jobs.extend(scrape_shine())
    time.sleep(2)
    all_jobs.extend(scrape_freshersworld())
    
    # Remove duplicates by link
    seen_links = set()
    unique_jobs = []
    for job in all_jobs:
        if job['Link'] not in seen_links:
            seen_links.add(job['Link'])
            unique_jobs.append(job)
    
    print(f"   [Multi-Source] Total Found: {len(unique_jobs)} unique jobs.")
    return unique_jobs


if __name__ == "__main__":
    jobs = scrape_indeed()
    print(f"\n=== Scraped {len(jobs)} jobs total ===")
    for job in jobs[:10]:
        print(f"  [{job['Site']}] {job['Title']} at {job['Company']}")