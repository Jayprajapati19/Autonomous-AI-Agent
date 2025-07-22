"""
Test script for email functionality
"""

import os
from dotenv import load_dotenv
from tools.email_tool import send_email, test_email_connection

def main():
    """Test email sending"""
    print("🧪 Testing Email Configuration")
    print("=" * 40)
    
    # Load environment
    load_dotenv()
    
    # Check environment variables
    email_user = os.getenv('EMAIL_USER', '').strip('"\'')
    email_pass = os.getenv('EMAIL_PASS', '').strip('"\'')
    
    print(f"📧 Email User: {email_user}")
    print(f"🔑 Password Length: {len(email_pass) if email_pass else 0}")
    print(f"🔑 Password Preview: {email_pass[:4]}****{email_pass[-4:] if len(email_pass) > 8 else '****'}")
    
    # Test connection
    print("\n🔗 Testing Connection...")
    result = test_email_connection()
    print(result)
    
    if "✅" in result:
        # Send test email
        print("\n📤 Sending Test Email...")
        test_result = send_email(
            subject="Test Email from AI Assistant",
            body="This is a test email to verify the email functionality is working correctly.",
            to_email=email_user  # Send to yourself
        )
        print(test_result)
    
    print("\n" + "=" * 40)
    print("✅ Email test completed!")

if __name__ == "__main__":
    main()
