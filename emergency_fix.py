import subprocess
import sys
import os

def run_cmd(cmd):
    """Run command and show output"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Success")
        return True
    else:
        print(f"❌ Error: {result.stderr}")
        return False

def emergency_fix():
    """Emergency fix for setuptools and groq installation"""
    print("🚨 Emergency Environment Fix")
    print("=" * 50)
    
    # Step 1: Force reinstall pip and setuptools
    print("\n1. Fixing pip and setuptools...")
    run_cmd(f"{sys.executable} -m pip install --force-reinstall pip")
    run_cmd(f"{sys.executable} -m pip install --force-reinstall setuptools>=68.0.0")
    run_cmd(f"{sys.executable} -m pip install --force-reinstall wheel")
    
    # Step 2: Install groq with specific method
    print("\n2. Installing groq package...")
    # Try different installation methods
    methods = [
        f"{sys.executable} -m pip install --no-cache-dir groq",
        f"{sys.executable} -m pip install --user groq",
        f"{sys.executable} -m pip install groq==0.8.0",
    ]
    
    groq_installed = False
    for method in methods:
        print(f"Trying: {method}")
        if run_cmd(method):
            groq_installed = True
            break
    
    if not groq_installed:
        print("❌ Could not install groq. Trying alternative...")
        run_cmd(f"{sys.executable} -m pip install --pre groq")
    
    # Step 3: Install other essentials
    print("\n3. Installing essential packages...")
    essentials = [
        "python-dotenv",
        "requests", 
        "flask",
        "beautifulsoup4"
    ]
    
    for package in essentials:
        run_cmd(f"{sys.executable} -m pip install --no-cache-dir {package}")
    
    # Step 4: Test installations
    print("\n4. Testing installations...")
    test_packages = ['groq', 'dotenv', 'requests', 'flask']
    all_good = True
    
    for package in test_packages:
        try:
            __import__(package)
            print(f"✅ {package} works")
        except ImportError:
            print(f"❌ {package} failed")
            all_good = False
    
    if all_good:
        print("\n🎉 All packages installed successfully!")
    else:
        print("\n⚠️  Some packages still have issues")
    
    return all_good

if __name__ == "__main__":
    emergency_fix()
