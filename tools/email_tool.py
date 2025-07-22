"""
Email functionality using SMTP
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email(subject, body, to_email, from_email=None, password=None):
    """
    Send email using Gmail SMTP
    
    Args:
        subject (str): Email subject
        body (str): Email body content
        to_email (str): Recipient email address
        from_email (str): Sender email (optional, uses ENV var)
        password (str): Email password (optional, uses ENV var)
        
    Returns:
        str: Success or error message
    """
    try:
        # Get email credentials from environment variables
        sender_email = from_email or os.getenv('EMAIL_USER')
        sender_password = password or os.getenv('EMAIL_PASS')
        
        # Remove quotes if present
        if sender_email:
            sender_email = sender_email.strip('"\'')
        if sender_password:
            sender_password = sender_password.strip('"\'')
        
        print(f"Debug: sender_email = {sender_email}")
        print(f"Debug: password length = {len(sender_password) if sender_password else 0}")
        
        if not sender_email or not sender_password:
            return "❌ Email credentials not found. Please check your .env file."
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = subject
        
        # Add body to email
        message.attach(MIMEText(body, "plain"))
        
        # Gmail SMTP configuration
        print("📧 Connecting to Gmail SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable encryption
        
        print("🔐 Logging in...")
        server.login(sender_email, sender_password)
        
        # Send email
        print("📤 Sending email...")
        text = message.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        return f"Email sent successfully to {to_email}!"
        
    except smtplib.SMTPAuthenticationError as e:
        return f"❌ Authentication failed. Please check your Gmail App Password: {str(e)}"
    except smtplib.SMTPException as e:
        return f"❌ SMTP error: {str(e)}"
    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"

def send_simple_email(to_email, subject, message):
    """
    Simplified email sending function
    
    Args:
        to_email (str): Recipient email
        subject (str): Email subject  
        message (str): Email message
        
    Returns:
        str: Success or error message
    """
    return send_email(subject, message, to_email)

def test_email_connection():
    """
    Test email configuration
    
    Returns:
        str: Test result
    """
    try:
        sender_email = os.getenv('EMAIL_USER', '').strip('"\'')
        sender_password = os.getenv('EMAIL_PASS', '').strip('"\'')
        
        if not sender_email or not sender_password:
            return "❌ Email credentials missing"
        
        # Test connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.quit()
        
        return "✅ Email configuration is working!"
        
    except Exception as e:
        return f"❌ Email test failed: {str(e)}"
