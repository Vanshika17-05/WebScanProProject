import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin # Used for joining relative links

# --- CONFIGURATION ---
# Set your starting URL here
START_URL = "http://example.com" 

# --- FUNCTIONS ---

def login_dvwa():
    """
    Placeholder function for your login logic.
    Add your code to log into DVWA here.
    """
    print("[*] Attempting to log in...")
    # Example: You might use requests.post() here
    # For now, we'll just pretend it worked.
    print("[+] Login successful (placeholder).")
    return True

def crawl(url):
    """
    Recursive function to crawl a single page.
    """
    try:
        print(f"[+] Crawling: {url}")
        # You can add your requests.get() and BeautifulSoup logic here
        # response = requests.get(url)
        # soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find links (example)
        # for link in soup.find_all('a'):
        #     href = link.get('href')
        #     if href:
        #         full_url = urljoin(url, href)
        #         # Add logic here to avoid re-crawling or going off-site
        #         # crawl(full_url) 

    except requests.exceptions.RequestException as e:
        print(f"[!] Warning: Could not crawl {url}. Error: {e}")

# --- MAIN EXECUTION ---

# This is the correct way to make your script runnable.
# This block only runs when you execute: python week2_crawler.py
if __name__ == "_main_":
    
    # Try to log in first
    if login_dvwa():
        print(f"\n--- STARTING CRAWL AT {START_URL} ---")
        
        # Start the crawl
        crawl(START_URL)
        
        print("\n--- CRAWL FINISHED ---")
        # You can print your results here
        # print(f"[*] Total Links Found: {len(your_links_list)}")
        # print(f"[*] Total Forms Found: {len(your_forms_list)}")
    
    else:
        print("[!] Login failed. Exiting crawl.")
