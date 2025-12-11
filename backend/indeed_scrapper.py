import requests
from datetime import datetime

# Free Job APIs that work without authentication
APIS = {
    "RemoteOK": "https://remoteok.com/api",
    "Arbeitnow": "https://www.arbeitnow.com/api/job-board-api"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

def scrape_remoteok():
    """Scrape jobs from RemoteOK API"""
    jobs = []
    try:
        print("   [RemoteOK] Fetching jobs...")
        response = requests.get(APIS["RemoteOK"], headers=HEADERS, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # First item is metadata, skip it
            job_list = data[1:] if len(data) > 1 else []
            
            # Filter for AI/ML related jobs
            keywords = ['ai', 'ml', 'machine learning', 'artificial intelligence', 'data science', 'deep learning', 'nlp', 'computer vision']
            
            for job in job_list:
                title = job.get('position', '').lower()
                tags = ' '.join(job.get('tags', [])).lower()
                
                if any(kw in title or kw in tags for kw in keywords):
                    salary = job.get('salary_min', '')
                    if salary:
                        salary_max = job.get('salary_max', '')
                        salary = f"${salary:,}" + (f" - ${salary_max:,}" if salary_max else "") + "/yr"
                    else:
                        salary = "Not Disclosed"
                    
                    jobs.append({
                        "Title": job.get('position', 'N/A'),
                        "Company": job.get('company', 'N/A'),
                        "Experience": "N/A",
                        "Location": job.get('location', 'Remote'),
                        "Description": job.get('description', 'See Link')[:200] + "..." if job.get('description') else "See Link",
                        "Salary": salary,
                        "Link": job.get('url', ''),
                        "Site": "RemoteOK",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
            
            print(f"   [RemoteOK] Found {len(jobs)} AI/ML jobs")
        else:
            print(f"   [RemoteOK] HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   [RemoteOK] Error: {e}")
    
    return jobs

def scrape_arbeitnow():
    """Scrape jobs from Arbeitnow API"""
    jobs = []
    try:
        print("   [Arbeitnow] Fetching jobs...")
        response = requests.get(APIS["Arbeitnow"], headers=HEADERS, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            job_list = data.get('data', [])
            
            # Filter for AI/ML related jobs
            keywords = ['ai', 'ml', 'machine learning', 'artificial intelligence', 'data science', 'deep learning', 'nlp', 'computer vision', 'engineer']
            
            for job in job_list:
                title = job.get('title', '').lower()
                description = job.get('description', '').lower()
                tags = ' '.join(job.get('tags', [])).lower()
                
                if any(kw in title or kw in tags for kw in keywords):
                    jobs.append({
                        "Title": job.get('title', 'N/A'),
                        "Company": job.get('company_name', 'N/A'),
                        "Experience": "N/A",
                        "Location": job.get('location', 'Remote'),
                        "Description": "See Link",
                        "Salary": "Not Disclosed",
                        "Link": job.get('url', ''),
                        "Site": "Arbeitnow",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
            
            print(f"   [Arbeitnow] Found {len(jobs)} AI/ML jobs")
        else:
            print(f"   [Arbeitnow] HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   [Arbeitnow] Error: {e}")
    
    return jobs

def scrape_indeed():
    """Scrape jobs from free job APIs (replacing Indeed which blocks GitHub Actions)"""
    print(f"[{datetime.now()}] Starting Job Scrape (Free APIs Mode)...")
    
    all_jobs = []
    
    # Scrape from RemoteOK
    all_jobs.extend(scrape_remoteok())
    
    # Scrape from Arbeitnow
    all_jobs.extend(scrape_arbeitnow())
    
    print(f"   [Free APIs] Total Found: {len(all_jobs)} jobs.")
    return all_jobs

if __name__ == "__main__":
    jobs = scrape_indeed()
    print(f"\nScraped {len(jobs)} jobs total")
    for job in jobs[:5]:
        print(f"  - {job['Title']} at {job['Company']} ({job['Site']})")