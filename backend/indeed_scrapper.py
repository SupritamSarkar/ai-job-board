import requests
import json
import re
from datetime import datetime

# Indeed uses an internal API for job listings
# We'll scrape by mimicking mobile/API requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

# API endpoints for Indeed job search
REGIONS = [
    ("India", "https://in.indeed.com", "ai ml engineer"),
    ("USA", "https://www.indeed.com", "ai ml engineer"),
]

def extract_jobs_from_html(html_content, region_name, base_url):
    """Extract job data from Indeed HTML using regex patterns"""
    jobs = []
    
    # Try to find the job data in the page's JavaScript
    # Indeed embeds job data as JSON in script tags
    
    # Pattern 1: mosaic-provider-jobcards data
    pattern1 = r'window\.mosaic\.providerData\["mosaic-provider-jobcards"\]\s*=\s*(\{.*?\});'
    match = re.search(pattern1, html_content, re.DOTALL)
    
    if match:
        try:
            data = json.loads(match.group(1))
            if 'metaData' in data and 'mosaicProviderJobCardsModel' in data['metaData']:
                job_cards = data['metaData']['mosaicProviderJobCardsModel'].get('results', [])
                for job in job_cards:
                    jobs.append({
                        "Title": job.get('title', 'N/A'),
                        "Company": job.get('company', 'N/A'),
                        "Experience": "N/A",
                        "Location": job.get('formattedLocation', 'N/A'),
                        "Description": "See Link",
                        "Salary": job.get('salarySnippet', {}).get('text', 'Not Disclosed') if job.get('salarySnippet') else 'Not Disclosed',
                        "Link": f"{base_url}/viewjob?jk={job.get('jobkey', '')}",
                        "Site": f"Indeed ({region_name})",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
        except json.JSONDecodeError:
            pass
    
    # Pattern 2: Search for job cards in alternative JSON structure
    if not jobs:
        pattern2 = r'"jobResults":\s*\[(.*?)\]'
        match = re.search(pattern2, html_content, re.DOTALL)
        if match:
            try:
                # Try to parse individual job objects
                job_pattern = r'\{"jobkey":"([^"]+)".*?"title":"([^"]+)".*?"company":"([^"]+)".*?"formattedLocation":"([^"]+)"'
                for job_match in re.finditer(job_pattern, html_content):
                    jobkey, title, company, location = job_match.groups()
                    jobs.append({
                        "Title": title,
                        "Company": company,
                        "Experience": "N/A",
                        "Location": location,
                        "Description": "See Link",
                        "Salary": "Not Disclosed",
                        "Link": f"{base_url}/viewjob?jk={jobkey}",
                        "Site": f"Indeed ({region_name})",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
            except:
                pass
    
    # Pattern 3: Basic HTML parsing fallback
    if not jobs:
        # Look for job links with data attributes
        job_pattern = r'data-jk="([^"]+)".*?title="([^"]+)"'
        for match in re.finditer(job_pattern, html_content, re.DOTALL):
            jobkey, title = match.groups()
            jobs.append({
                "Title": title[:100],  # Truncate long titles
                "Company": "See Link",
                "Experience": "N/A",
                "Location": "See Link",
                "Description": "See Link",
                "Salary": "Not Disclosed",
                "Link": f"{base_url}/viewjob?jk={jobkey}",
                "Site": f"Indeed ({region_name})",
                "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            })
    
    return jobs

def scrape_indeed():
    print(f"[{datetime.now()}] Starting Indeed Scrape (HTTP Request Mode)...")
    
    all_jobs = []
    session = requests.Session()
    session.headers.update(HEADERS)
    
    for region_name, base_url, query in REGIONS:
        print(f"\n--- Switching to Indeed {region_name} ---")
        
        try:
            # Build search URL
            search_url = f"{base_url}/jobs?q={query.replace(' ', '+')}&l="
            print(f"   [Indeed {region_name}] Fetching: {search_url}")
            
            response = session.get(search_url, timeout=30)
            
            if response.status_code == 200:
                jobs = extract_jobs_from_html(response.text, region_name, base_url)
                print(f"   [Indeed {region_name}] Found {len(jobs)} jobs")
                all_jobs.extend(jobs)
            else:
                print(f"   [Indeed {region_name}] HTTP {response.status_code}")
                
        except requests.RequestException as e:
            print(f"   [Indeed {region_name}] Request failed: {e}")
            continue
    
    print(f"   [Indeed] Total Found: {len(all_jobs)} jobs.")
    return all_jobs

if __name__ == "__main__":
    jobs = scrape_indeed()
    print(f"\nScraped {len(jobs)} jobs total")
    for job in jobs[:3]:
        print(f"  - {job['Title']} at {job['Company']}")