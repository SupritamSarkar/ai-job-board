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

def scrape_remoteok_internships():
    """Scrape internships from RemoteOK API"""
    internships = []
    try:
        print("   [RemoteOK] Fetching internships...")
        response = requests.get(APIS["RemoteOK"], headers=HEADERS, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # First item is metadata, skip it
            job_list = data[1:] if len(data) > 1 else []
            
            # Filter for AI/ML internships
            keywords = ['intern', 'internship', 'trainee', 'graduate', 'junior', 'entry level']
            ai_keywords = ['ai', 'ml', 'machine learning', 'artificial intelligence', 'data', 'deep learning']
            
            for job in job_list:
                title = job.get('position', '').lower()
                tags = ' '.join(job.get('tags', [])).lower()
                
                # Must be an internship AND related to AI/ML/Data
                is_internship = any(kw in title for kw in keywords)
                is_ai_related = any(kw in title or kw in tags for kw in ai_keywords)
                
                if is_internship or (is_ai_related and 'junior' in title):
                    salary = job.get('salary_min', '')
                    if salary:
                        salary_max = job.get('salary_max', '')
                        salary = f"${salary:,}" + (f" - ${salary_max:,}" if salary_max else "") + "/yr"
                    else:
                        salary = "Not Disclosed"
                    
                    internships.append({
                        "Title": job.get('position', 'N/A'),
                        "Company": job.get('company', 'N/A'),
                        "Experience": "Internship",
                        "Location": job.get('location', 'Remote'),
                        "Description": job.get('description', 'See Link')[:200] + "..." if job.get('description') else "See Link",
                        "Salary": salary,
                        "Link": job.get('url', ''),
                        "Site": "RemoteOK",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
            
            print(f"   [RemoteOK] Found {len(internships)} internships")
        else:
            print(f"   [RemoteOK] HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   [RemoteOK] Error: {e}")
    
    return internships

def scrape_arbeitnow_internships():
    """Scrape internships from Arbeitnow API"""
    internships = []
    try:
        print("   [Arbeitnow] Fetching internships...")
        response = requests.get(APIS["Arbeitnow"], headers=HEADERS, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            job_list = data.get('data', [])
            
            # Filter for internships
            keywords = ['intern', 'internship', 'trainee', 'graduate', 'working student', 'werkstudent']
            ai_keywords = ['ai', 'ml', 'machine learning', 'data', 'software', 'developer', 'engineer']
            
            for job in job_list:
                title = job.get('title', '').lower()
                tags = ' '.join(job.get('tags', [])).lower()
                
                is_internship = any(kw in title for kw in keywords)
                is_tech = any(kw in title or kw in tags for kw in ai_keywords)
                
                if is_internship and is_tech:
                    internships.append({
                        "Title": job.get('title', 'N/A'),
                        "Company": job.get('company_name', 'N/A'),
                        "Experience": "Internship",
                        "Location": job.get('location', 'Remote'),
                        "Description": "See Link",
                        "Salary": "Not Disclosed",
                        "Link": job.get('url', ''),
                        "Site": "Arbeitnow",
                        "Last_Updated": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    })
            
            print(f"   [Arbeitnow] Found {len(internships)} internships")
        else:
            print(f"   [Arbeitnow] HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   [Arbeitnow] Error: {e}")
    
    return internships

def scrape_indeed_intern():
    """Scrape internships from free job APIs (replacing Indeed which blocks GitHub Actions)"""
    print(f"[{datetime.now()}] Starting Internship Scrape (Free APIs Mode)...")
    
    all_internships = []
    
    # Scrape from RemoteOK
    all_internships.extend(scrape_remoteok_internships())
    
    # Scrape from Arbeitnow
    all_internships.extend(scrape_arbeitnow_internships())
    
    print(f"   [Free APIs] Total Found: {len(all_internships)} internships.")
    return all_internships

if __name__ == "__main__":
    internships = scrape_indeed_intern()
    print(f"\nScraped {len(internships)} internships total")
    for intern in internships[:5]:
        print(f"  - {intern['Title']} at {intern['Company']} ({intern['Site']})")