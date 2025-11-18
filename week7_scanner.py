import time
import datetime
import os
from week6_scanner import scan #<--- ADD THIS LINE 
 # Make sure you have imported os at the top of your file

def generate_report(all_findings):
    try:
        # 1. Get the directory and paths
        current_dir = os.path.dirname(__file__)
        template_path = os.path.join(current_dir, 'template.html')
        output_path = os.path.join(current_dir, 'report.html')

        # 2. Check if template exists. If not, create the FANCY one.
        if not os.path.exists(template_path):
            print("Creating a PRO template.html...")
            default_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>WebScanPro Security Report</title>
                <style>
                    body { font-family: 'Arial', sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 20px; }
                    .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                    h1 { text-align: center; color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }
                    .finding { background: #fff; border: 1px solid #ddd; border-left: 5px solid #333; margin-bottom: 15px; padding: 15px; border-radius: 4px; }
                    .finding h2 { margin-top: 0; color: #444; font-size: 18px; }
                    .detail-code p { margin: 5px 0; font-size: 14px; }
                    .severity-high { color: #d9534f; font-weight: bold; text-transform: uppercase; }
                    .severity-medium { color: #f0ad4e; font-weight: bold; text-transform: uppercase; }
                    .severity-low { color: #5cb85c; font-weight: bold; text-transform: uppercase; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>WebScanPro Security Report</h1>
                    <div class="content">{{ content }}</div>
                </div>
            </body>
            </html>
            """
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(default_html)

        # 3. Read the template
        with open(template_path, 'r', encoding='utf-8') as f:
            report_html = f.read()

        # 4. Build the HTML for findings
        report_content = ""
        for finding in all_findings:
            scanner = finding.get('scanner', 'Unknown')
            v_type = finding.get('type', 'Unknown')
            url = finding.get('url', 'Unknown')
            severity = finding.get('severity', 'low')

            # Determine color class
            if severity.lower() == 'high':
                severity_class = 'severity-high'
            elif severity.lower() == 'medium':
                severity_class = 'severity-medium'
            else:
                severity_class = 'severity-low'

            report_content += f"""
            <div class="finding">
                <h2>{v_type}</h2>
                <div class="detail-code">
                    <p><strong>Scanner:</strong> {scanner}</p>
                    <p><strong>Type:</strong> {v_type}</p>
                    <p><strong>URL:</strong> {url}</p>
                    <p><strong>Severity:</strong> <span class="{severity_class}">{severity}</span></p>
                </div>
            </div>
            """

        # 5. Insert content into template
        final_report = report_html.replace('{{ content }}', report_content)

        # 6. Write the final report file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_report)

        print(f"Report generated successfully at: {output_path}")

    except Exception as e:
        print(f"Error generating report: {e}")

        # --- PASTE THIS AT THE VERY BOTTOM (REAL MODE) ---
if __name__ == "__main__":
    # 1. Define the URL you want to test
    # (Make sure this matches the URL you used in previous weeks)
    target_url = "http://127.0.0.1/dvwa" 

    print(f"--- Starting Real Scan on {target_url} ---")
    
    # 2. Run the real scan
    # This calls the 'scan' function you imported from week 6
    findings = scan(target_url)

    # 3. Generate the report with REAL findings
    if findings:
        print(f"Scan complete! Found {len(findings)} vulnerabilities.")
        generate_report(findings)
    else:
        print("Scan complete. No vulnerabilities found.")
        # Generate an empty report just so you have the file to look at
        generate_report([])