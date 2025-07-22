import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = ['groq', 'dotenv', 'flask', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies available!")
    return True

def validate_env():
    """Validate environment variables"""
    load_dotenv()
    
    groq_key = os.getenv('GROQ_API_KEY')
    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASS')
    
    if not groq_key or groq_key == "your_groq_api_key_here":
        print("❌ GROQ_API_KEY not properly set!")
        return False
    
    if not email_user:
        print("❌ EMAIL_USER not set!")
        return False
    
    if not email_pass or email_pass == "your_16_char_app_password":
        print("❌ EMAIL_PASS not properly set! Use Gmail App Password.")
        return False
    
    print("✅ Environment variables validated!")
    return True

def find_main_file():
    """Find the main application file"""
    possible_names = ['main.py', 'app.py', 'server.py', 'assistant.py']
    
    for name in possible_names:
        if Path(name).exists():
            return name
    
    # Look for any Python file with 'main' or 'app' in the name
    for file in Path('.').glob('*.py'):
        if 'main' in file.name.lower() or 'app' in file.name.lower():
            return file.name
    
    return None

def main():
    print("🤖 AI Assistant Startup Check...")
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Validate environment
    if not validate_env():
        return
    
    # Find main file
    main_file = find_main_file()
    if not main_file:
        print("❌ Could not find main application file!")
        print("Please run the main Python file manually.")
        return
    
    print(f"✅ Found main file: {main_file}")
    print(f"🚀 Starting application...")
    
    try:
        # Import and run the main file
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", main_file)
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        
    except Exception as e:
        print(f"❌ Error running application: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check if all dependencies are installed")
        print("2. Verify your .env file configuration")
        print("3. Check for any syntax errors in the code")

if __name__ == "__main__":
    main()
