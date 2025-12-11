"""
Multi-Source Internship Scraper using Selenium
Scrapes AI/ML internships from TimesJobs, Freshersworld, and Internshala
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
# 1. TimesJobs Internship Scraper
# ===========================================
def scrape_timesjobs_internships():
    """Scrape AI/ML internships from TimesJobs"""
    print("   [TimesJobs] Starting internship scrape...")
    internships = []
    
    driver = get_driver()
    
    try:
        url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeyword=ai+ml+intern&cboPresFuncArea=35"
        driver.get(url)
        
        time.sleep(random.uniform(3, 5))
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-bx"))
            )
        except:
            print("   [TimesJobs] Timeout waiting for internships")
            driver.quit()
            return internships
        
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
                
                # Location
                try:
                    location_list = card.find_elements(By.CSS_SELECTOR, "ul.top-jd-dtl li")
                    location = location_list[2].text.strip() if len(location_list) > 2 else "N/A"
                except:
                    location = "N/A"
                
                internships.append({
                    "Title": title,
                    "Company": company,
                    "Experience": "Internship",
                    "Location": location,
                    "Description": "See Link",
                    "Salary": "Not Disclosed",
                    "Link": link,
                    "Site": "TimesJobs"
                })
            except:
                continue
                
        print(f"   [TimesJobs] Found {len(internships)} internships")
        
    except Exception as e:
        print(f"   [TimesJobs] Error: {e}")
    finally:
        driver.quit()
    
    return internships


# ===========================================
# 2. Freshersworld Internship Scraper
# ===========================================
def scrape_freshersworld_internships():
    """Scrape AI/ML internships from Freshersworld"""
    print("   [Freshersworld] Starting internship scrape...")
    internships = []
    
    driver = get_driver()
    
    try:
        url = "https://www.freshersworld.com/jobs/category/internship-jobs"
        driver.get(url)
        
        time.sleep(random.uniform(3, 5))
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-container"))
            )
        except:
            print("   [Freshersworld] Timeout waiting for internships")
            driver.quit()
            return internships
        
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
                
                internships.append({
                    "Title": title,
                    "Company": company,
                    "Experience": "Internship",
                    "Location": location,
                    "Description": "See Link",
                    "Salary": "Not Disclosed",
                    "Link": link,
                    "Site": "Freshersworld"
                })
            except:
                continue
                
        print(f"   [Freshersworld] Found {len(internships)} internships")
        
    except Exception as e:
        print(f"   [Freshersworld] Error: {e}")
    finally:
        driver.quit()
    
    return internships


# ===========================================
# 3. Internshala Scraper
# ===========================================
def scrape_internshala():
    """Scrape AI/ML internships from Internshala"""
    print("   [Internshala] Starting scrape...")
    internships = []
    
    driver = get_driver()
    
    try:
        url = "https://internshala.com/internships/machine-learning-internship/"
        driver.get(url)
        
        time.sleep(random.uniform(3, 5))
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "internship_meta"))
            )
        except:
            print("   [Internshala] Timeout waiting for internships")
            driver.quit()
            return internships
        
        job_cards = driver.find_elements(By.CLASS_NAME, "internship_meta")
        
        for card in job_cards:
            try:
                # Title & Link
                title_elem = card.find_element(By.CSS_SELECTOR, "a.job-title-href")
                title = title_elem.text.strip()
                link = "https://internshala.com" + title_elem.get_attribute("href") if title_elem.get_attribute("href").startswith("/") else title_elem.get_attribute("href")
                
                # Company
                try:
                    company = card.find_element(By.CLASS_NAME, "company_name").text.strip()
                except:
                    company = "N/A"
                
                # Location
                try:
                    location = card.find_element(By.CSS_SELECTOR, "a.location_link").text.strip()
                except:
                    location = "N/A"
                
                # Stipend
                try:
                    stipend = card.find_element(By.CLASS_NAME, "stipend").text.strip()
                except:
                    stipend = "Not Disclosed"
                
                internships.append({
                    "Title": title,
                    "Company": company,
                    "Experience": "Internship",
                    "Location": location,
                    "Description": "See Link",
                    "Salary": stipend,
                    "Link": link,
                    "Site": "Internshala"
                })
            except:
                continue
                
        print(f"   [Internshala] Found {len(internships)} internships")
        
    except Exception as e:
        print(f"   [Internshala] Error: {e}")
    finally:
        driver.quit()
    
    return internships


# ===========================================
# MAIN SCRAPE FUNCTION
# ===========================================
def scrape_indeed_intern():
    """
    Multi-source internship scraper using Selenium
    Scrapes from: TimesJobs, Freshersworld, Internshala
    """
    print(f"[{datetime.now()}] Starting Multi-Source Internship Scrape (Selenium)...")
    
    all_internships = []
    
    # Scrape from all sources
    all_internships.extend(scrape_timesjobs_internships())
    time.sleep(2)
    all_internships.extend(scrape_freshersworld_internships())
    time.sleep(2)
    all_internships.extend(scrape_internshala())
    
    # Remove duplicates by link
    seen_links = set()
    unique_internships = []
    for intern in all_internships:
        if intern['Link'] not in seen_links:
            seen_links.add(intern['Link'])
            unique_internships.append(intern)
    
    print(f"   [Multi-Source] Total Found: {len(unique_internships)} unique internships.")
    return unique_internships


if __name__ == "__main__":
    internships = scrape_indeed_intern()
    print(f"\n=== Scraped {len(internships)} internships total ===")
    for intern in internships[:10]:
        print(f"  [{intern['Site']}] {intern['Title']} at {intern['Company']}")