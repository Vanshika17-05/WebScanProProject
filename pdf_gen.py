from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'WebScanPro | Security Audit Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(target_url, findings, server_info):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # 1. Executive Summary
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "1. Executive Summary", 0, 1)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, f"Target Scanned: {target_url}", 0, 1)
    pdf.cell(0, 10, f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
    pdf.cell(0, 10, f"Server Technology: {server_info}", 0, 1)
    pdf.cell(0, 10, f"Total Vulnerabilities: {len(findings)}", 0, 1)
    pdf.ln(5)

    # 2. Detailed Findings
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "2. Detailed Technical Findings", 0, 1)
    pdf.set_font("Arial", size=10)

    if not findings:
        pdf.cell(0, 10, "No vulnerabilities detected.", 0, 1)
    else:
        for idx, item in enumerate(findings):
            # Vulnerability Title
            pdf.set_font("Arial", 'B', 11)
            pdf.set_text_color(200, 0, 0) # Red color
            pdf.cell(0, 10, f"{idx+1}. {item['type']} ({item['severity'].upper()})", 0, 1)
            
            # Details
            pdf.set_text_color(0, 0, 0) # Reset color
            pdf.set_font("Arial", size=9)
            pdf.multi_cell(0, 6, f"Scanner Module: {item['scanner']}")
            pdf.multi_cell(0, 6, f"Payload/URL: {item['url']}")
            
            # Remediation Advice
            pdf.set_font("Arial", 'I', 9)
            advice = "Recommendation: Update software and use prepared statements (for SQLi) or input sanitization (for XSS)."
            pdf.multi_cell(0, 6, advice)
            pdf.ln(5)

    # 3. Save
    filename = "security_audit_report.pdf"
    pdf.output(filename)
    return filename