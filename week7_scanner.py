import time
import datetime
import os
import sys

# ---
# !! IMPORT YOUR REAL SCANNERS HERE !!
# ---
try:
    # Try importing scanners from previous weeks
    from week5_scanner import xss_scanner
    from week6_scanner import sql_injection_scanner
    print("[*] Successfully imported real scanners from week5/week6.")
except ImportError:
    print("[!] Could not import real scanners. Using built-in dummy scanners for demonstration.")
    
    # Dummy scanners that simulate finding DVWA vulnerabilities
    def xss_scanner(url, cookies=None):
        print(f"  (Dummy) Scanning {url} for XSS with cookies: {cookies}...")
        # Simulate finding a Reflected XSS in DVWA
        return [{
            'scanner': 'XSS Scanner', 
            'type': 'Reflected XSS', 
            'url': f"{url}?name=<script>alert(1)</script>", 
            'severity': 'high'
        }]
        
    def sql_injection_scanner(url, cookies=None):
        print(f"  (Dummy) Scanning {url} for SQL Injection with cookies: {cookies}...")
        # Simulate finding SQLi in DVWA
        return [{
            'scanner': 'SQL Injection', 
            'type': 'Boolean-based Blind', 
            'url': f"{url}?id=1' OR '1'='1", 
            'severity': 'critical'
        }]

# ==========================================================
#  GENERATE REPORT FUNCTION (Beautiful Tables)
# ==========================================================
def generate_report(all_findings):
    print("Generating HTML report...")
    
    # CSS for the report
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>DVWA Vulnerability Report</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; }
            .container { width: 90%; max-width: 1100px; margin: 40px auto; background: #fff; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-radius: 8px; }
            h1 { text-align: center; color: #2c3e50; margin-bottom: 5px; }
            .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; }
            
            .summary-box { display: flex; justify-content: space-around; background: #ecf0f1; padding: 15px; border-radius: 5px; margin-bottom: 25px; border-left: 5px solid #3498db; }
            .summary-item strong { display: block; font-size: 1.2em; color: #2c3e50; }
            .summary-item span { font-size: 0.9em; color: #7f8c8d; }

            table { width: 100%; border-collapse: collapse; margin-top: 10px; overflow: hidden; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.05); }
            th, td { padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #34495e; color: white; text-transform: uppercase; font-size: 0.85em; letter-spacing: 0.05em; }
            tr:hover { background-color: #f9f9f9; }
            
            .badge { padding: 6px 12px; border-radius: 20px; color: white; font-weight: bold; font-size: 0.75em; text-align: center; display: inline-block; min-width: 70px; }
            .critical { background-color: #721c24; }
            .high { background-color: #e74c3c; }
            .medium { background-color: #f39c12; }
            .low { background-color: #27ae60; }
            
            .footer { text-align: center; margin-top: 40px; font-size: 0.8em; color: #aaa; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>WebScanPro Security Report</h1>
            <p class="subtitle">Target: DVWA (Damn Vulnerable Web App)</p>
            
            <div class="summary-box">
                <div class="summary-item"><strong>{timestamp}</strong><span>Scan Date</span></div>
                <div class="summary-item"><strong>{count}</strong><span>Vulnerabilities Found</span></div>
            </div>
    """

    # Dynamic Data
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = html_content.replace("{timestamp}", timestamp)
    html_content = html_content.replace("{count}", str(len(all_findings)))

    if not all_findings:
        html_content += "<h3 style='text-align:center; color: #27ae60;'>No vulnerabilities found. System is secure (or authentication failed).</h3>"
    else:
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>Scanner</th>
                    <th>Vulnerability</th>
                    <th>Payload / URL</th>
                    <th>Severity</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for finding in all_findings:
            scanner = finding.get('scanner', 'Unknown')
            v_type = finding.get('type', 'N/A')
            url = finding.get('url', 'N/A')
            severity = finding.get('severity', 'low').lower()
            
            if severity == 'critical': badge = 'critical'
            elif severity == 'high': badge = 'high'
            elif severity == 'medium': badge = 'medium'
            else: badge = 'low'
            
            html_content += f"""
                <tr>
                    <td>{scanner}</td>
                    <td><strong>{v_type}</strong></td>
                    <td style="font-family: monospace; color: #c0392b;">{url}</td>
                    <td><span class="badge {badge}">{severity.upper()}</span></td>
                </tr>
            """
        
        html_content += "</tbody></table>"

    html_content += """
            <div class="footer">
                <p>Generated by WebScanPro | Automated DVWA Scanner</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Save file
    try:
        filename = 'dvwa_report.html'
        with open(filename, 'w') as f:
            f.write(html_content)
        print(f"\n[+] Report generated successfully: {filename}")
        print(f"[+] Open {filename} in your browser to view results.")
    except Exception as e:
        print(f"Error saving report: {e}")

# ==========================================================
#  MAIN FUNCTION
# ==========================================================
def main():
    all_findings = []
    
    # 1. SETUP DVWA CONNECTION
    print("--- Configuring DVWA Connection ---")
    
    # --- CONFIGURATION START ---
    # Change this to your local DVWA URL
    target_url = "http://localhost/dvwa/vulnerabilities/" 
    
    # IMPORTANT: Update this with your real PHPSESSID from your browser
    # (Right-click > Inspect > Application > Cookies)
    dvwa_cookies = {
        'PHPSESSID': 'PASTE_YOUR_PHPSESSID_HERE', 
        'security': 'low'  # DVWA security level
    }
    # --- CONFIGURATION END ---

    print(f"[*] Target: {target_url}")
    print(f"[*] Security Level: {dvwa_cookies['security']}")
    print("--- Starting Scan ---")

    start_time = time.time()

    # List of scanners to run
    scanners_to_run = [
        ("XSS Scanner", xss_scanner),
        ("SQL Injection", sql_injection_scanner)
    ]

    for name, scan_function in scanners_to_run:
        print(f"[*] Running {name}...")
        try:
            # 2. SMART SCANNER CALL
            # Try passing cookies (for DVWA authentication)
            try:
                results = scan_function(target_url, cookies=dvwa_cookies)
            except TypeError:
                # Fallback: If scanner doesn't support cookies, just pass URL
                # print(f"    (Note: {name} does not accept cookies, sending URL only)")
                results = scan_function(target_url)

            if results:
                print(f"    [!] Found {len(results)} vulnerabilities!")
                all_findings.extend(results)
            else:
                print(f"    [-] No vulnerabilities found.")
                
        except Exception as e:
            print(f"    [!] Error running {name}: {e}")

    end_time = time.time()
    
    # Generate Report
    generate_report(all_findings)
    
    print("\n--- Scan Complete ---")
    print(f"Total time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
