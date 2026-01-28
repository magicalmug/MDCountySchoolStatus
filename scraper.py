import requests
from bs4 import BeautifulSoup
from datetime import datetime

# The URLs for the official status pages
SOURCES = {
    "Montgomery (MCPS)": "https://www.montgomeryschoolsmd.org/emergency/",
    "Howard (HCPSS)": "https://status.hcpss.org/"
}

def check_status():
    results = [] # We need this to store the data
    
    for county, url in SOURCES.items():
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
     if "Montgomery" in county:
        # 1. Try to find the common emergency alert containers
        # MCPS frequently uses 'emergency-msg' or a banner at the top
        alert = soup.find('div', class_='emergency-msg') or soup.find('div', id='emergency-status')
    
        if alert:
            status = alert.get_text(strip=True)
        else:
            # 2. Backup: Look for specific keywords in the whole page text
            # (This catches it even if they change the ID name)
            page_text = soup.get_text().lower()
            if "code red" in page_text or "closed" in page_text:
                status = "System Closed (Detected in Text)"
            else:
            status = "Green: Normal Operations"
            elif "Howard" in county:
                status_box = soup.find('h2') 
                status_text = status_box.get_text(strip=True) if status_box else "No status found"

            results.append({"county": county, "status": status_text})
            
        except Exception as e:
            results.append({"county": county, "status": "Error fetching data"})

    return results

def save_to_html(data):
    # This is the part that actually creates the index.html file
    timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    
    html_content = f"""
    <html>
    <head><title>School Status</title></head>
    <body style="font-family: sans-serif; text-align: center;">
        <h1>Live School Status</h1>
        <p>Last Updated: {timestamp}</p>
        <hr>
        {"".join([f"<div><h2>{item['county']}</h2><p>{item['status']}</p></div>" for item in data])}
    </body>
    </html>
    """
    
    with open("index.html", "w") as f:
        f.write(html_content)
    print("Successfully created index.html!")

if __name__ == "__main__":
    status_data = check_status()
    save_to_html(status_data)
