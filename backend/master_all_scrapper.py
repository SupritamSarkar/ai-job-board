import os
import json
import time
import random
from datetime import datetime, timedelta

# --- IMPORT ALL SCRAPERS ---
# Ensure these files exist in the same directory
from naukri_scrapper import scrape_naukri
from indeed_scrapper import scrape_indeed
from naukri_intern_scrapper import scrape_naukri_intern
from indeed_intern_scrapper import scrape_indeed_intern

def is_recent(date_str):
    """
    Checks if a date string is within the last 7 days.
    """
    try:
        # Try full timestamp format first
        job_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            # Fallback to simple date format (legacy data)
            job_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False
            
    seven_days_ago = datetime.now() - timedelta(days=7)
    return job_date > seven_days_ago

def update_database(new_items, filename):
    """
    Reusable function to:
    1. Read existing JSON
    2. Remove old entries (>7 days)
    3. Merge new entries (updating duplicates)
    4. Save back to file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "..", "frontend", "src", filename)
    
    existing_items = []
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_items = json.load(f)
        except:
            existing_items = []

    data_map = {}

    # A. Process EXISTING items (Keep only recent)
    kept_count = 0
    expired_count = 0
    
    for item in existing_items:
        link = item.get('Link')
        date_str = item.get('Last_Updated', '')
        
        if is_recent(date_str):
            data_map[link] = item
            kept_count += 1
        else:
            expired_count += 1

    # B. Process NEW items (Merge/Update)
    for item in new_items:
        data_map[item['Link']] = item

    final_list = list(data_map.values())
    random.shuffle(final_list)

    # C. Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    return len(final_list), kept_count, expired_count, output_path

def main():
    print("==========================================")
    print(f"===   STARTING MASTER ALL SCRAPER      ===")
    print(f"===   Time: {datetime.now()}   ===")
    print("==========================================\n")
    
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ==========================================
    # PHASE 1: FULL-TIME JOBS (Naukri + Indeed)
    # ==========================================
    print("--- [PHASE 1] SCRAPING JOBS ---")
    
    # 1.1 Naukri Jobs
    try:
        naukri_jobs = scrape_naukri()
    except Exception as e:
        print(f"Error in Naukri Job Scraper: {e}")
        naukri_jobs = []

    # 1.2 Indeed Jobs
    try:
        time.sleep(2)
        indeed_jobs = scrape_indeed()
    except Exception as e:
        print(f"Error in Indeed Job Scraper: {e}")
        indeed_jobs = []

    # Combine & Timestamp
    new_jobs = naukri_jobs + indeed_jobs
    for job in new_jobs:
        job['Last_Updated'] = current_timestamp

    print(f"> Fresh Jobs Found: {len(new_jobs)}")

    # Update jobs.json
    total_j, kept_j, del_j, path_j = update_database(new_jobs, "jobs.json")
    print(f"> Database Updated: {total_j} Total Jobs (Kept {kept_j} old, Removed {del_j} expired)")
    print(f"> Saved to: {path_j}\n")


    # ==========================================
    # PHASE 2: INTERNSHIPS (Naukri + Indeed)
    # ==========================================
    print("--- [PHASE 2] SCRAPING INTERNSHIPS ---")

    # 2.1 Naukri Internships
    try:
        naukri_interns = scrape_naukri_intern()
    except Exception as e:
        print(f"Error in Naukri Intern Scraper: {e}")
        naukri_interns = []

    # 2.2 Indeed Internships
    try:
        time.sleep(2)
        indeed_interns = scrape_indeed_intern()
    except Exception as e:
        print(f"Error in Indeed Intern Scraper: {e}")
        indeed_interns = []

    # Combine & Timestamp
    new_interns = naukri_interns + indeed_interns
    for item in new_interns:
        item['Last_Updated'] = current_timestamp

    print(f"> Fresh Internships Found: {len(new_interns)}")

    # Update intern.json
    total_i, kept_i, del_i, path_i = update_database(new_interns, "intern.json")
    print(f"> Database Updated: {total_i} Total Internships (Kept {kept_i} old, Removed {del_i} expired)")
    print(f"> Saved to: {path_i}\n")

    print("==========================================")
    print("===          ALL TASKS COMPLETE        ===")
    print("==========================================")

if __name__ == "__main__":
    main()