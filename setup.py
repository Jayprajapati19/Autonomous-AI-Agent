import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found!")
        return False
    
    required_vars = ["GROQ_API_KEY", "EMAIL_USER", "EMAIL_PASS"]
    with open(env_path) as f:
        content = f.read()
        
    for var in required_vars:
        if var not in content:
            print(f"❌ Missing {var} in .env file!")
            return False
    
    print("✅ Environment variables configured!")
    return True

def main():
    print("🚀 Setting up AI Assistant project...")
    
    if not check_env_file():
        print("\n📝 Please configure your .env file first!")
        return
    
    if not install_requirements():
        return
    
    print("\n✅ Setup complete! You can now run the project.")
    print("\n📋 Next steps:")
    print("1. Make sure your Gmail App Password is set in .env")
    print("2. Run: python main.py (or the main file)")

if __name__ == "__main__":
    main()
