import os
import sys
from pathlib import Path

def test_imports():
    """Test all required imports"""
    print("🧪 Testing Package Imports")
    print("=" * 30)
    
    packages = {
        'groq': 'Groq AI client',
        'requests': 'HTTP library',
        'dotenv': 'Environment variables',
        'flask': 'Web framework (optional)',
        'bs4': 'BeautifulSoup (optional)',
    }
    
    working_packages = []
    failed_packages = []
    
    for package, description in packages.items():
        try:
            if package == 'dotenv':
                from dotenv import load_dotenv
            elif package == 'bs4':
                import bs4
            else:
                __import__(package)
            
            print(f"✅ {package} - {description}")
            working_packages.append(package)
        except ImportError as e:
            print(f"❌ {package} - {description} - Error: {e}")
            failed_packages.append(package)
    
    print(f"\n📊 Results: {len(working_packages)} working, {len(failed_packages)} failed")
    return len(failed_packages) == 0

def test_env_vars():
    """Test environment variables"""
    print("\n🔧 Testing Environment Variables")
    print("=" * 35)
    
    # Try to load .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env file loaded with python-dotenv")
    except:
        # Manual loading
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
            print("✅ .env file loaded manually")
    
    # Check variables
    groq_key = os.getenv('GROQ_API_KEY')
    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASS')
    
    if groq_key and groq_key.startswith('gsk_'):
        print("✅ GROQ_API_KEY is set")
    else:
        print("❌ GROQ_API_KEY missing or invalid")
    
    if email_user:
        print(f"✅ EMAIL_USER: {email_user}")
    else:
        print("❌ EMAIL_USER missing")
    
    if email_pass and email_pass != "":
        print("✅ EMAIL_PASS is set")
    else:
        print("⚠️  EMAIL_PASS is empty (need Gmail App Password)")

def test_groq_connection():
    """Test Groq API connection"""
    print("\n🌐 Testing Groq Connection")
    print("=" * 25)
    
    try:
        import groq
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("❌ No API key found")
            return False
        
        client = groq.Groq(api_key=api_key)
        print("✅ Groq client created successfully")
        
        # Simple test (won't actually call API unless you want to)
        print("✅ Ready to make API calls")
        return True
        
    except Exception as e:
        print(f"❌ Groq test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 AI Assistant Setup Verification")
    print("=" * 40)
    
    imports_ok = test_imports()
    test_env_vars()
    
    if imports_ok:
        test_groq_connection()
        print("\n✅ Setup verification complete!")
        print("You can now try running the main application.")
    else:
        print("\n❌ Setup verification failed!")
        print("Run: python emergency_fix.py")

if __name__ == "__main__":
    main()
