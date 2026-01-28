import requests
from bs4 import BeautifulSoup
from datetime import datetime

# The URLs for the official status pages
SOURCES = {
    "Montgomery (MCPS)": "https://www.montgomeryschoolsmd.org/emergency/",
    "Howard (HCPSS)": "https://status.hcpss.org/"
}

def check_status():
    print(f"--- Update Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    for county, url in SOURCES.items():
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Logic for MCPS: Looks for the main alert box text
            if "Montgomery" in county:
                # MCPS often puts status in a div with id 'emergency-status'
                status_box = soup.find('div', id='emergency-status')
                status_text = status_box.get_text(strip=True) if status_box else "Check site manually"
            
            # Logic for Howard: Looks for the status message on their dedicated status page
            elif "Howard" in county:
                # HCPSS status page usually has a clear heading for current status
                status_box = soup.find('h2') 
                status_text = status_box.get_text(strip=True) if status_box else "No status found"

            print(f"{county}: {status_text}")
            
        except Exception as e:
            print(f"Error checking {county}: {e}")

if __name__ == "__main__":
    check_status()
