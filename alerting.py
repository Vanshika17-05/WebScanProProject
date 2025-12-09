
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def send_email_alert(target, critical_count, findings):
    """
    Simulates sending an email alert. 
    In a real deployment, you would uncomment the SMTP lines.
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
    
    Top Threats:
    """
    
    for item in findings[:3]: # List top 3
        body += f"- {item['type']} at {item['url']}\n"
        
    body += "\nImmediate Action Required: Login to WebScanPro Console to investigate."

    # SIMULATION FOR DEMO (Safe for Project Presentation)
    print("------------------------------------------------")
    print(f"📧 [SIMULATION] SENDING EMAIL TO {receiver_email}")
    print(f"Subject: {subject}")
    print(body)
    print("------------------------------------------------")
    
    # Return success message for the UI
    return True