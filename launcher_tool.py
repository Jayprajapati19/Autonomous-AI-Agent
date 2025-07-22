import os
import webbrowser

def open_file_by_name(filename, search_path=None):
    if not search_path:
        # Search common user directories
        user_home = os.path.expanduser("~")
        search_dirs = [
            os.path.join(user_home, "Desktop"),
            os.path.join(user_home, "Documents"),
            os.path.join(user_home, "Downloads"),
        ]
    else:
        search_dirs = [search_path]

    matched_files = []
    
    for directory in search_dirs:
        for root, _, files in os.walk(directory):
            if filename in files:
                matched_files.append(os.path.join(root, filename))

    if not matched_files:
        return f"❌ File '{filename}' not found in Desktop/Documents/Downloads."

    file_to_open = matched_files[0]  # You can change this to pick interactively
    try:
        webbrowser.open(f"file://{os.path.abspath(file_to_open)}")
        return f"✅ Opened: {file_to_open}"
    except Exception as e:
        return f"❌ Failed to open file: {e}"
