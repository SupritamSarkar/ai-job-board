import os
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# URL to scrape
SEARCH_URL = "https://www.naukri.com/ai-ml-engineer-jobs?k=ai%20ml%20engineer"

def run_scraper():
    print(f"[{datetime.now()}] Starting Scrape...")
    
    # 1. Setup Chrome Options
    chrome_options = Options()
    # Headless mode is critical for GitHub Actions (no screen to display)
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # 2. Initialize Driver
    # This automatically handles the ChromeDriver installation on both your PC and GitHub
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    all_jobs = []

    try:
        # 3. Scraping Loop (Pages 1 to 6)
        for page in range(1, 8):
            url = SEARCH_URL if page == 1 else SEARCH_URL.replace("?", f"-{page}?")
            print(f"   Scraping Page {page}...")
            
            driver.get(url)
            driver.implicitly_wait(5)
            
            # Find the job cards
            job_cards = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")
            
            for card in job_cards:
                try:
                    # Title & Link
                    title_elem = card.find_element(By.CSS_SELECTOR, "a.title")
                    link = title_elem.get_attribute("href")
                    title = title_elem.text
                    
                    # Company
                    company = card.find_element(By.CSS_SELECTOR, "a.comp-name").text
                    
                    # Experience
                    try: 
                        experience = card.find_element(By.CSS_SELECTOR, "span.expwdth").text
                    except: 
                        experience = "N/A"
                        
                    # Location
                    try: 
                        location = card.find_element(By.CSS_SELECTOR, "span.locWdth").text
                    except: 
                        location = "N/A"
                        
                    # Description
                    try: 
                        description = card.find_element(By.CSS_SELECTOR, "span.job-desc").text
                    except: 
                        description = "N/A"

                    all_jobs.append({
                        "Title": title,
                        "Company": company,
                        "Experience": experience,
                        "Location": location,
                        "Description": description,
                        "Link": link,
                        "Last_Updated": str(datetime.now().date())
                    })
                except Exception as e:
                    # Skip this specific card if critical info is missing
                    continue
                    
    finally:
        driver.quit()

    # 4. Save to JSON (The Critical Fix)
    if all_jobs:
        # Determine where THIS script file is located (e.g., .../backend/)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Navigate UP one level, then DOWN into frontend/src/
        output_path = os.path.join(script_dir, "..", "frontend", "src", "jobs.json")
        
        # Create the directory if it doesn't exist (safety measure)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_jobs, f, indent=2)
            
        print(f"Scrape Complete. {len(all_jobs)} jobs saved to: {output_path}")
    else:
        print("No jobs found.")

if __name__ == "__main__":
    run_scraper()