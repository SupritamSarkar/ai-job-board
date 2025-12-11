"""
Indeed Job Scraper - Replaced by Internshala Jobs
Indeed blocks scraping from GitHub Actions, so we use Internshala Jobs instead.
This file now imports and calls the Internshala Jobs scraper.
"""

from datetime import datetime
from internshala_jobs_scrapper import scrape_internshala_jobs

def scrape_indeed():
    """
    Replacement for Indeed scraper.
    Uses Internshala Jobs since Indeed blocks all scraping attempts from GitHub Actions.
    """
    print(f"[{datetime.now()}] Starting Indeed replacement (Internshala Jobs)...")
    return scrape_internshala_jobs()

if __name__ == "__main__":
    jobs = scrape_indeed()
    print(f"\n=== Scraped {len(jobs)} jobs ===")