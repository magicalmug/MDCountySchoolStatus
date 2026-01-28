import requests
from bs4 import BeautifulSoup
from datetime import datetime

# The URLs for the official status pages
SOURCES = {
    "Montgomery (MCPS)": "https://www.montgomeryschoolsmd.org/emergency/",
    "Howard (HCPSS)": "https://status.hcpss.org/"
}

def check_status():
    results = []
    headers = {'User-Agent': 'Mozilla/5.0'} # Pretend to be a browser

    for county, url in SOURCES.items():
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Initial assumption
            status = "Normal Operations"

            if "Montgomery" in county:
                # 1. Look for the specific box
                alert = soup.find('div', class_='emergency-msg') or soup.find('div', id='emergency-status')
                if alert:
                    status = alert.get_text(strip=True)
                else:
                    # 2. Safety Net: Search the whole page for keywords
                    page_text = soup.get_text().lower()
                    if "code red" in page_text or "closed" in page_text:
                        status = "CLOSED (Detected in text)"

            elif "Howard" in county:
                # HCPSS uses <h2> for their status page headline
                alert = soup.find('h2')
                if alert:
                    status = alert.get_text(strip=True)

            # Ensure 'status' is always passed to results
            results.append({"county": county, "status": status})
            
        except Exception as e:
            results.append({"county": county, "status": f"Error: {str(e)}"})

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
