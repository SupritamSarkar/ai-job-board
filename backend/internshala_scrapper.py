"""
Internshala Internship Scraper
Scrapes AI/ML internships from Internshala (7 pages)
Updated CSS selectors to match current Internshala HTML structure
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
            
            time.sleep(random.uniform(3, 5))
            
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".individual_internship, .internship_meta, .internship-heading"))
                )
            except:
                print(f"   [Internshala] Timeout on page {page}")
                continue
            
            # Try multiple selectors for job cards
            job_cards = driver.find_elements(By.CSS_SELECTOR, ".individual_internship")
            if not job_cards:
                job_cards = driver.find_elements(By.CSS_SELECTOR, ".internship_meta")
            if not job_cards:
                job_cards = driver.find_elements(By.CSS_SELECTOR, "[class*='internship']")
            
            page_count = 0
            for card in job_cards:
                try:
                    # Title - Try multiple selectors
                    title = ""
                    try:
                        title = card.find_element(By.CSS_SELECTOR, ".job-internship-name a").text.strip()
                    except:
                        try:
                            title = card.find_element(By.CSS_SELECTOR, "h3 a").text.strip()
                        except:
                            try:
                                title = card.find_element(By.CSS_SELECTOR, ".profile a").text.strip()
                            except:
                                try:
                                    title = card.find_element(By.CSS_SELECTOR, "a.job-title-href").text.strip()
                                except:
                                    try:
                                        title = card.find_element(By.CSS_SELECTOR, ".heading_4_5 a").text.strip()
                                    except:
                                        pass
                    
                    # Link
                    link = ""
                    try:
                        link_elem = card.find_element(By.CSS_SELECTOR, ".job-internship-name a, h3 a, .profile a, a.job-title-href, .heading_4_5 a")
                        link = link_elem.get_attribute("href")
                        if link and link.startswith("/"):
                            link = "https://internshala.com" + link
                    except:
                        try:
                            link_elem = card.find_element(By.TAG_NAME, "a")
                            link = link_elem.get_attribute("href")
                            if link and link.startswith("/"):
                                link = "https://internshala.com" + link
                        except:
                            continue
                    
                    # Skip if no title or link
                    if not title and not link:
                        continue
                    
                    # If no title but have link, extract from link
                    if not title and link:
                        # Extract title from URL: /internship/detail/work-from-home-machine-learning-internship-at-...
                        try:
                            parts = link.split("/detail/")[1].split("-at-")[0]
                            title = parts.replace("-", " ").title()
                        except:
                            title = "See Link"
                    
                    # Company
                    company = ""
                    try:
                        company = card.find_element(By.CSS_SELECTOR, ".company_name a, .company-name a, .company a").text.strip()
                    except:
                        try:
                            company = card.find_element(By.CSS_SELECTOR, ".company_name, .company-name, .company").text.strip()
                        except:
                            try:
                                company = card.find_element(By.CSS_SELECTOR, "p.company_name").text.strip()
                            except:
                                # Try to extract from link
                                try:
                                    parts = link.split("-at-")[1].split("1")[0]
                                    company = parts.replace("-", " ").title()
                                except:
                                    company = "N/A"
                    
                    # Clean company name
                    if company:
                        company = company.replace("\nActively hiring", "").strip()
                    
                    # Location
                    location = ""
                    try:
                        location = card.find_element(By.CSS_SELECTOR, ".location_link, .locations a, .location a").text.strip()
                    except:
                        try:
                            location = card.find_element(By.CSS_SELECTOR, "#location_names span, .location span").text.strip()
                        except:
                            try:
                                location = card.find_element(By.CSS_SELECTOR, "[class*='location']").text.strip()
                            except:
                                location = "Remote"
                    
                    # Stipend
                    stipend = ""
                    try:
                        stipend = card.find_element(By.CSS_SELECTOR, ".stipend, .salary, .stipend_container_text").text.strip()
                    except:
                        try:
                            stipend = card.find_element(By.CSS_SELECTOR, "[class*='stipend']").text.strip()
                        except:
                            stipend = "Not Disclosed"
                    
                    # Duration
                    duration = ""
                    try:
                        duration = card.find_element(By.CSS_SELECTOR, ".duration, [class*='duration']").text.strip()
                    except:
                        duration = "N/A"
                    
                    internships.append({
                        "Title": title if title else "See Link",
                        "Company": company if company else "N/A",
                        "Experience": "Internship",
                        "Location": location if location else "Remote",
                        "Description": f"Duration: {duration}" if duration else "See Link",
                        "Salary": stipend if stipend else "Not Disclosed",
                        "Link": link,
                        "Site": "Internshala",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
                    page_count += 1
                except Exception as e:
                    continue
            
            print(f"   [Internshala] Page {page}: {page_count} internships found")
                
    except Exception as e:
        print(f"   [Internshala] Error: {e}")
    finally:
        driver.quit()
    
    # Remove duplicates and entries without links
    seen_links = set()
    unique_internships = []
    for intern in internships:
        if intern['Link'] and intern['Link'] not in seen_links:
            seen_links.add(intern['Link'])
            unique_internships.append(intern)
    
    print(f"   [Internshala] Total Found: {len(unique_internships)} internships.")
    return unique_internships


if __name__ == "__main__":
    internships = scrape_internshala()
    print(f"\n=== Scraped {len(internships)} internships ===")
    for intern in internships[:5]:
        print(f"  - {intern['Title']} at {intern['Company']} ({intern['Salary']})")
