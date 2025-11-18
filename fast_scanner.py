import requests
import concurrent.futures
import time

# --- CONFIGURATION ---
# We pretend to be a real browser so websites don't block us
HEADERS = {'User-Agent': 'Mozilla/5.0 (WebScanPro/1.0)'}

# A list of common vulnerabilities to check (SQL Injection patterns)
PAYLOADS = ["'", "\"", "admin' --", "' OR '1'='1"]

def scan_url(url):
    """
    Scans a SINGLE URL.
    """
    print(f"🔍 Scanning: {url}")
    vulnerabilities = []
    
    try:
        # 1. Check normal connection
        response = requests.get(url, headers=HEADERS, timeout=3)
        
        # 2. Inject payloads to see if the site breaks
        for payload in PAYLOADS:
            target = f"{url}{payload}"
            # We check the response text for specific SQL errors
            req = requests.get(target, headers=HEADERS, timeout=3)
            
            if "syntax error" in req.text.lower() or "mysql" in req.text.lower():
                vulnerabilities.append(f"❌ Possible SQL Injection found at: {target}")
                
    except requests.exceptions.RequestException:
        return f"⚠ Could not reach {url}"

    if vulnerabilities:
        return "\n".join(vulnerabilities)
    else:
        return f"✅ {url} seems safe."

def run_fast_scan(target_urls):
    """
    The 'Pro' Engine: Scans multiple URLs at the same time.
    """
    print(f"\n🚀 Starting High-Speed Scan on {len(target_urls)} URLs...")
    start_time = time.time()

    # --- THIS IS THE LEVEL 1 UPGRADE ---
    # ThreadPoolExecutor runs 5 scans AT THE SAME TIME.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(scan_url, target_urls)

    # Print all results
    for result in results:
        print(result)

    end_time = time.time()
    print(f"\n Total time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    # Test Data: A mix of vulnerable test sites and big real sites
    test_urls = [
        "http://testphp.vulnweb.com/artists.php?artist=1", 
        "http://testphp.vulnweb.com/listproducts.php?cat=1",
        "https://www.google.com",
        "https://www.bing.com",
        "https://www.yahoo.com"
    ]
    
    run_fast_scan(test_urls)
