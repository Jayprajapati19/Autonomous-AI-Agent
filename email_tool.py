# tools/email_tool.py
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email(subject, body, to_email):
    msg = EmailMessage()
    
    # Remove newlines from subject to avoid crash
    safe_subject = subject.replace('\n', ' ').strip()
    
    msg["Subject"] = safe_subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
    
    return "✅ Email sent successfully."
