import os
import sys
from pathlib import Path

def check_basic_imports():
    """Check if essential packages are available"""
    required_packages = ['groq', 'requests']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} missing")
    
    return len(missing) == 0

def load_environment():
    """Load environment variables"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment loaded")
        return True
    except ImportError:
        print("❌ python-dotenv not available, loading manually...")
        # Manual env loading
        env_path = Path('.env')
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
            print("✅ Environment loaded manually")
            return True
        return False

def validate_config():
    """Validate configuration"""
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key or 'your_groq_api_key' in groq_key:
        print("❌ GROQ_API_KEY not properly configured")
        return False
    
    email_pass = os.getenv('EMAIL_PASS')
    if not email_pass or 'your_app_password' in email_pass:
        print("⚠️  EMAIL_PASS needs to be configured with Gmail App Password")
    
    print("✅ Configuration validated")
    return True

def find_main_script():
    """Find the main application file"""
    possible_files = ['main.py', 'app.py', 'assistant.py', 'server.py']
    
    for filename in possible_files:
        if Path(filename).exists():
            return filename
    
    # Look for Python files containing 'main' or 'app'
    for py_file in Path('.').glob('*.py'):
        content = py_file.read_text(encoding='utf-8', errors='ignore')
        if 'if __name__ == "__main__"' in content:
            return py_file.name
    
    return None

def main():
    print("🤖 AI Assistant - Fixed Startup")
    print("=" * 40)
    
    # Check imports
    if not check_basic_imports():
        print("\n❌ Missing required packages. Run: python fix_environment.py")
        return
    
    # Load environment
    if not load_environment():
        print("❌ Could not load environment variables")
        return
    
    # Validate config
    if not validate_config():
        print("❌ Configuration validation failed")
        return
    
    # Find main script
    main_file = find_main_script()
    if not main_file:
        print("❌ Could not find main application file")
        print("Available Python files:")
        for py_file in Path('.').glob('*.py'):
            print(f"  - {py_file.name}")
        return
    
    print(f"✅ Found main file: {main_file}")
    print(f"🚀 Starting application...")
    
    try:
        # Execute the main file
        with open(main_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        exec(code, {'__name__': '__main__'})
        
    except Exception as e:
        print(f"❌ Error running {main_file}: {e}")
        print("\n🔍 Try running the main file directly:")
        print(f"python {main_file}")

if __name__ == "__main__":
    main()
