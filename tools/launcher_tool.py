"""
File launcher functionality for opening files and applications
"""

import os
import subprocess
import platform
from pathlib import Path

def open_file_by_name(filename):
    """
    Open a file by searching for it in common directories
    
    Args:
        filename (str): Name of the file to open
        
    Returns:
        str: Result message
    """
    try:
        # Common search directories
        search_dirs = [
            Path.home() / "Desktop",
            Path.home() / "Documents", 
            Path.home() / "Downloads",
            Path.home(),
            Path("C:/") if platform.system() == "Windows" else Path("/"),
        ]
        
        found_files = []
        
        # Search for the file
        for directory in search_dirs:
            if directory.exists():
                for file_path in directory.rglob(filename):
                    if file_path.is_file():
                        found_files.append(file_path)
        
        if not found_files:
            return f"❌ File '{filename}' not found in common directories"
        
        # Open the first found file
        file_to_open = found_files[0]
        
        # Platform-specific file opening
        if platform.system() == "Windows":
            os.startfile(str(file_to_open))
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", str(file_to_open)])
        else:  # Linux
            subprocess.run(["xdg-open", str(file_to_open)])
        
        return f"✅ Successfully opened: {file_to_open}"
        
    except Exception as e:
        return f"❌ Error opening file: {str(e)}"

def open_application(app_name):
    """
    Open an application by name
    
    Args:
        app_name (str): Name of the application
        
    Returns:
        str: Result message
    """
    try:
        if platform.system() == "Windows":
            subprocess.run(["start", app_name], shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", "-a", app_name])
        else:  # Linux
            subprocess.run([app_name])
        
        return f"✅ Successfully launched: {app_name}"
        
    except Exception as e:
        return f"❌ Error launching application: {str(e)}"
