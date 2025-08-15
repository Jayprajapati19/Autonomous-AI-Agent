import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {command}")
        print(f"Error output: {e.stderr}")
        return False

def fix_environment():
    """Fix the Python environment issues"""
    print("🔧 Fixing Python environment...")
    
    # Update pip first
    print("\n1. Updating pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Update setuptools and wheel
    print("\n2. Updating build tools...")
    run_command(f"{sys.executable} -m pip install --upgrade setuptools wheel")
    
    # Install essential packages first
    print("\n3. Installing essential packages...")
    essential_packages = [
        "python-dotenv",
        "requests",
        "beautifulsoup4",
        "lxml"
    ]
    
    for package in essential_packages:
        run_command(f"{sys.executable} -m pip install {package}")
    
    # Install groq specifically
    print("\n4. Installing Groq...")
    run_command(f"{sys.executable} -m pip install groq")
    
    # Install remaining packages one by one
    print("\n5. Installing additional packages...")
    additional_packages = [
        "flask",
        "duckduckgo-search",
        "wikipedia",
        "openai"
    ]
    
    for package in additional_packages:
        print(f"Installing {package}...")
        run_command(f"{sys.executable} -m pip install {package}")
    
    print("\n✅ Environment setup complete!")
    
    # Test imports
    print("\n🧪 Testing package imports...")
    test_packages = ['groq', 'dotenv', 'requests', 'flask']
    
    for package in test_packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ {package} import failed: {e}")

if __name__ == "__main__":
    fix_environment()
