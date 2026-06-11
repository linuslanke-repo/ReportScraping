import io
import browser_cookie3
import pandas as pd
import requests

# 1. Your original OneDrive/SharePoint URL
original_url = "https://pmgoperations-my.sharepoint.com/:x:/r/personal/sunil_lanke_globaldata_com/Documents/Report%20Download%20Test.xlsx?d=wf2496e9dbdb64f6cac9b0d0e17f36aef&csf=1&web=1&e=On89w6"

# 2. Correct API transformation for personal OneDrive/SharePoint paths
download_url = original_url.replace("/:x:/r/", "/:x:/i/").split("?")[0] + "?download=1"

# 3. Pull cookies from Chrome
try:
    cookies = browser_cookie3.chrome(domain_name="sharepoint.com")
except Exception as e:
    print(f"Error reading browser cookies: {e}")
    print("Ensure Chrome is open and you are logged into SharePoint.")
    exit()

# 4. Download file
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(download_url, cookies=cookies, headers=headers)

# 5. Safety check: Verify content type before parsing
content_type = response.headers.get('Content-Type', '')

if response.status_code == 200 and "html" not in content_type:
    # Successfully received a binary stream (Excel)
    df = pd.read_excel(io.BytesIO(response.content))
    print("--- Successfully loaded Excel Data ---")
    print(df.head())
else:
    print(f"Failed to fetch Excel file. Status code: {response.status_code}")
    print(f"Server returned content type: {content_type}")
    print("\n--- Raw response snippet (debugging text) ---")
    print(response.text[:500])  # Prints the error text/HTML from Microsoft
