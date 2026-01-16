#!/usr/bin/env python3

# organize_downloads.py
# version: 1.0
# date: 16-January-2026
# author: Chris C. Gaskins
# github: https://github.com/cgaskins-tx/organize_downloads


import os
import shutil
import time
from pathlib import Path
from datetime import datetime, timedelta

# =================CONFIGURATION=================

# Source Directory (Default: ~/Downloads)
SOURCE_DIR = Path.home() / "Downloads"

# How old a file must be (in hours) before we touch it
AGE_THRESHOLD_HOURS = 24

# Explicitly ignore these system files (Exact filenames)
IGNORE_FILES = [
    ".DS_Store", 
    ".localized",
    "desktop.ini" # Common on Windows/Linux dual boots
]

# Category Map
# Keys = Folder Names, Values = List of Extensions (must be lowercase)
FILE_CATEGORIES = {
    "Documents": [
        ".txt", ".md", ".markdown", ".rtf", ".pdf", ".csv",
        ".doc", ".docx", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".key",
        ".epub", ".log", ".drawio", ".ics", ".vcf", ".x-vcard"
    ],
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".tif", ".tiff",
        ".svg", ".ico", ".icns", ".psd", ".ai", ".eps", ".xcf", ".ps", 
        ".design", ".dwg", ".tfw"
    ],
    "Audio": [
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"
    ],
    "Video": [
        ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".webm", ".m4v", ".3gp"
    ],
    "Code": [
        ".py", ".js", ".mjs", ".ts", ".java", ".c", ".cpp", ".php", ".rb", ".go", 
        ".rs", ".sh", ".html", ".css", ".json", ".xml", ".yaml", ".yml", ".sql", 
        ".plist", ".conf", ".ovpn", ".eslintrc", ".gitattributes", ".pod", ".trx", 
        ".nib", ".strings", ".dylib", ".car"
    ],
    "Installers": [
        ".dmg", ".pkg", ".rpm", ".deb", ".iso", ".msi", ".apk"
    ],
    "Executables": [
        ".exe"
        # Note: 'installerhelper' is handled by filename check below
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".tgz", ".bkp", ".wpress"
    ],
    "Fonts": [
        ".ttf", ".otf", ".woff", ".woff2"
    ]
}

# =================LOGIC=================

def get_file_age_hours(filepath):
    """Returns the age of the file in hours based on modification time."""
    stats = filepath.stat()
    # Use mtime (modification) to ensure we don't move files currently being written
    mtime = datetime.fromtimestamp(stats.st_mtime)
    now = datetime.now()
    duration = now - mtime
    return duration.total_seconds() / 3600

def make_unique_name(destination, filename):
    """
    If file exists in destination, append timestamp to make it unique.
    Returns the new full path.
    """
    dest_path = destination / filename
    if not dest_path.exists():
        return dest_path
    
    # Separation logic
    stem = dest_path.stem
    suffix = dest_path.suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"{stem}_{timestamp}{suffix}"
    return destination / new_name

def organize():
    # 1. Ensure Source Exists
    if not SOURCE_DIR.exists():
        print(f"Error: Source directory {SOURCE_DIR} does not exist.")
        return

    print(f"--- Running Organizer on {SOURCE_DIR} ---")
    print(f"--- Threshold: Files older than {AGE_THRESHOLD_HOURS} hours ---")

    # 2. Define Protected Folders (The Categories + Misc + Folders)
    protected_folders = list(FILE_CATEGORIES.keys()) + ["Misc", "Folders"]

    # 3. Iterate through items
    for item in SOURCE_DIR.iterdir():
        
        # SKIP: Protected Destination Folders
        if item.name in protected_folders:
            continue

        # SKIP: Ignored System Files
        if item.name in IGNORE_FILES:
            continue

        # SKIP: Files/Folders that are too new (< 24 hours)
        try:
            age = get_file_age_hours(item)
            if age < AGE_THRESHOLD_HOURS:
                # print(f"Skipping {item.name}: Too new ({age:.1f} hours)")
                continue
        except FileNotFoundError:
            continue # File was moved/deleted during processing

        # DEFINE TARGET
        target_category = "Misc"

        if item.is_dir():
            target_category = "Folders"
        else:
            # Handle Files
            # Special Case: Exact Filenames
            if item.name.lower() == "installerhelper":
                target_category = "Executables"
            else:
                # Check Extensions
                ext = item.suffix.lower()
                found = False
                for category, extensions in FILE_CATEGORIES.items():
                    if ext in extensions:
                        target_category = category
                        found = True
                        break
                if not found:
                    target_category = "Misc"

        # MOVE OPERATION
        dest_dir = SOURCE_DIR / target_category
        dest_dir.mkdir(exist_ok=True) # Create category folder if missing

        try:
            dest_path = make_unique_name(dest_dir, item.name)
            shutil.move(str(item), str(dest_path))
            print(f"Moved: {item.name} -> {target_category}")
        except Exception as e:
            print(f"Error moving {item.name}: {e}")

if __name__ == "__main__":
    organize()
