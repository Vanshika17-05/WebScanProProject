import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(target, critical_count, findings):
    """
    Simulates sending an email alert.
    """
    sender_email = "security_bot@webscanpro.ai"
    receiver_email = "admin@company.com"
    
    subject = f"🚨 CRITICAL ALERT: {critical_count} Threats Detected on {target}"
    
    body = f"""
    SECURITY BREACH REPORT
    ----------------------
    Target: {target}
    Severity: CRITICAL
    Total Vulnerabilities: {len(findings)}
    """
    
    # SIMULATION PRINT (Safe for Project Presentation)
    print("\n" + "="*50)
    print(f"📧 [SIMULATION] SENDING EMAIL TO {receiver_email}")
    print(f"Subject: {subject}")
    print(body)
    print("="*50 + "\n")
    
    return True