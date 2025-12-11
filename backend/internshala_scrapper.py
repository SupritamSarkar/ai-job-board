"""
Internshala Internship Scraper
Scrapes AI/ML internships from Internshala (7 pages)
Updated with correct CSS selectors from actual HTML structure
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
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".individual_internship_details"))
                )
            except:
                print(f"   [Internshala] Timeout on page {page}")
                continue
            
            # Get all internship cards - based on the HTML structure
            job_cards = driver.find_elements(By.CSS_SELECTOR, ".individual_internship")
            if not job_cards:
                job_cards = driver.find_elements(By.CSS_SELECTOR, ".internship_meta")
            
            page_count = 0
            for card in job_cards:
                try:
                    # Title - from the profile/heading section
                    title = ""
                    try:
                        title = card.find_element(By.CSS_SELECTOR, ".profile h3 a").text.strip()
                    except:
                        try:
                            title = card.find_element(By.CSS_SELECTOR, ".heading_4_5 a").text.strip()
                        except:
                            try:
                                title = card.find_element(By.CSS_SELECTOR, "h3 a").text.strip()
                            except:
                                pass
                    
                    # Link
                    link = ""
                    try:
                        link_elem = card.find_element(By.CSS_SELECTOR, ".profile h3 a, .heading_4_5 a, h3 a")
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
                    
                    if not link:
                        continue
                    
                    # If no title, extract from URL
                    if not title and link:
                        try:
                            parts = link.split("/detail/")[1].split("-at-")[0]
                            title = parts.replace("-", " ").title()
                            # Clean up common prefixes
                            title = title.replace("Work From Home ", "")
                            title = title.replace("Part Time ", "")
                        except:
                            title = "See Link"
                    
                    # Company - from p.company-name (as shown in screenshot)
                    company = ""
                    try:
                        company = card.find_element(By.CSS_SELECTOR, "p.company-name").text.strip()
                    except:
                        try:
                            company = card.find_element(By.CSS_SELECTOR, ".heading_6.company_name p").text.strip()
                        except:
                            try:
                                company = card.find_element(By.CSS_SELECTOR, ".company_and_premium p").text.strip()
                            except:
                                # Extract from URL
                                try:
                                    parts = link.split("-at-")[1].split("1")[0]
                                    company = parts.replace("-", " ").title()
                                except:
                                    company = "N/A"
                    
                    # Location - from .row-1-item.locations span a
                    location = ""
                    try:
                        location = card.find_element(By.CSS_SELECTOR, ".row-1-item.locations span a").text.strip()
                    except:
                        try:
                            location = card.find_element(By.CSS_SELECTOR, ".locations a").text.strip()
                        except:
                            try:
                                location = card.find_element(By.CSS_SELECTOR, "#location_names a").text.strip()
                            except:
                                location = "Remote"
                    
                    # Stipend - from .individual_internship_details .row-1-item span.stipend
                    stipend = ""
                    try:
                        # Try the exact path from HTML structure
                        stipend = card.find_element(By.CSS_SELECTOR, ".individual_internship_details span.stipend").text.strip()
                    except:
                        try:
                            stipend = card.find_element(By.CSS_SELECTOR, ".row-1-item span.stipend").text.strip()
                        except:
                            try:
                                stipend = card.find_element(By.CSS_SELECTOR, "span.stipend").text.strip()
                            except:
                                try:
                                    stipend = card.find_element(By.CSS_SELECTOR, ".stipend").text.strip()
                                except:
                                    try:
                                        # Try getting from row-1-item that contains money icon
                                        row_items = card.find_elements(By.CSS_SELECTOR, ".row-1-item")
                                        for item in row_items:
                                            try:
                                                if item.find_element(By.CSS_SELECTOR, ".ic-16-money"):
                                                    stipend = item.find_element(By.CSS_SELECTOR, "span").text.strip()
                                                    break
                                            except:
                                                continue
                                    except:
                                        stipend = "Not Disclosed"
                    
                    # Duration - from the duration section
                    duration = ""
                    try:
                        # Duration is in row-1-item after stipend
                        duration_elem = card.find_elements(By.CSS_SELECTOR, ".row-1-item")
                        if len(duration_elem) >= 3:
                            duration = duration_elem[2].text.strip()
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
    
    # Remove duplicates
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
