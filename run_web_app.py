import subprocess
import sys
import os
from pathlib import Path

def run_streamlit_app():
    """Launch the Streamlit web application"""
    print("🚀 Starting AI Assistant Web App...")
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is available")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Check if streamlit_app.py exists
    app_file = Path("streamlit_app.py")
    if not app_file.exists():
        print("❌ streamlit_app.py not found!")
        return
    
    print("✅ Found streamlit_app.py")
    print("🌐 Starting web server...")
    print("📱 The app will open in your default browser")
    print("🔗 Default URL: http://localhost:8501")
    print("\n" + "="*50)
    print("🛑 Press Ctrl+C to stop the server")
    print("="*50)
    
    try:
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n✅ Web server stopped")
    except Exception as e:
        print(f"❌ Error starting web app: {e}")

if __name__ == "__main__":
    run_streamlit_app()
