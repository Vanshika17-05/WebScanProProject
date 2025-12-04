import argparse
import sys
import time

# --- THESE IMPORTS ARE CRITICAL ---
# They tell main.py where to find the tools you built in previous weeks
from week6_scanner import scan
from week7_scanner import generate_report

def print_banner():
    print("""
    ==========================================
       W E B S C A N   P R O   -   v 1.0
    ==========================================
    [+] Automating Security Scanning
    [+] Vulnerability Report Generator
    ==========================================
    """)

def main():
    print_banner()

    # 1. Set up the Argument Parser
    # This allows you to type '-u' in the terminal
    parser = argparse.ArgumentParser(description="WebScanPro: A simple vulnerability scanner.")
    parser.add_argument("-u", "--url", help="The target URL to scan", required=True)
    
    args = parser.parse_args()
    target_url = args.url

    print(f"[*] Target defined: {target_url}")
    print("[*] Starting scan engine...")
    time.sleep(1)

    # 2. Run the Scanner
    try:
        # This calls the function from week6_scanner.py
        findings = scan(target_url)
    except Exception as e:
        print(f"\n[!] Critical Error during scan: {e}")
        sys.exit(1)

    # 3. Generate the Report
    if findings:
        print(f"\n[+] Scan finished. Found {len(findings)} vulnerabilities.")
        print("[*] Generating report...")
        generate_report(findings)
    else:
        print("\n[-] Scan finished. No vulnerabilities found.")
        generate_report([])

if __name__ == "__main__":
    main()
