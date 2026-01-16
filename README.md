# Downloads Folder Organizer

A lightweight, zero-dependency Python script designed to automatically organize your chaotic Downloads folder.

It sorts files into logical categories (Documents, Images, Code, etc.) based on file extensions, but only touches files that are older than a specific time threshold (default: 24 hours). This ensures that files you are currently working with remain in the root directory, while older clutter gets filed away.

**Works on macOS and Linux.**

## 🚀 Key Features

* **Time-Based Logic:** Only processes files older than **24 hours** (configurable). Active downloads remain untouched.
* **Safe Moves:** Never overwrites files. If a file with the same name exists in the destination, a timestamp is appended to the new file (e.g., `resume.pdf` -> `resume_20231027_103000.pdf`).
* **Smart Categorization:** Extensive mapping of file extensions to categories (see below).
* **Folder Handling:** Moves sub-directories into a dedicated `Folders/` directory to keep the root clean.
* **Cross-Platform:** Uses Python's `pathlib` for compatibility with macOS and Linux file systems.
* **System Safe:** Automatically ignores system files like `.DS_Store`, `.localized`, and `desktop.ini`.

## 📂 Category Mapping

The script automatically creates these directories if they don't exist and sorts files based on the following rules:

| Category | Description | Common Extensions |
| :--- | :--- | :--- |
| **Documents** | Text, Office, PDFs, Logs | `.pdf`, `.docx`, `.xlsx`, `.txt`, `.md`, `.csv`, `.epub`, `.ics` |
| **Images** | Photos, Vectors, Design files | `.jpg`, `.png`, `.svg`, `.heic`, `.psd`, `.ai`, `.dwg` |
| **Audio** | Music, Sound clips | `.mp3`, `.wav`, `.flac`, `.m4a` |
| **Video** | Movies, Recordings | `.mp4`, `.mov`, `.mkv`, `.avi` |
| **Code** | Source code, Web, Configs | `.py`, `.js`, `.html`, `.css`, `.json`, `.yaml`, `.sql`, `.xml`, `.sh` |
| **Installers** | Packages, Disk Images | `.dmg`, `.pkg`, `.deb`, `.rpm`, `.iso`, `.apk`, `.msi` |
| **Executables** | Binaries | `.exe`, `installerhelper` |
| **Archives** | Compressed files | `.zip`, `.tar`, `.gz`, `.rar`, `.7z` |
| **Fonts** | Font files | `.ttf`, `.otf`, `.woff` |
| **Folders** | Sub-directories | Any directory found in root |
| **Misc** | Everything else | Any extension not explicitly defined above |

## 🛠️ Companion Utilities

This repository includes three additional utility scripts to help you analyze and manage your Downloads folder. These scripts use the `rich` library for beautiful terminal output.

### Prerequisites for Utilities
Install the required library:

    pip3 install rich

### 1. Find Largest Files (`find_largest.py`)
Scans the Downloads folder (recursively) to find space hogs.
* **Default:** Shows the top 10 largest files.
* **Custom:** Pass a number to see more (e.g., `find_largest.py 20`).
* **Features:** Displays size, type, date, and sub-folder location.

**Usage:**

    ./find_largest.py      # Top 10
    ./find_largest.py 50   # Top 50

### 2. Find Recent Files (`find_recent.py`)
Quickly find the files you just downloaded, even if they are buried in sub-folders.
* **Default:** Shows the top 10 most recent files.
* **Features:** Sorted by newest first. Includes clickable links (see below).

**Usage:**

    ./find_recent.py

### 3. Download Stats (`download_stats.py`)
A dashboard for your Downloads folder.
* **Overview:** Displays total size, file count, and the oldest/newest files in the directory.
* **Breakdown:** Shows a table of every sub-directory (Documents, Images, etc.) with their individual sizes and file counts.

**Usage:**

    ./download_stats.py

## 💡 Pro Tip: Interactive Terminal Links

The `find_largest.py` and `find_recent.py` scripts generate **clickable hyperlinks** for filenames and locations.

* **Clicking a Filename:** Opens the file in its default application.
* **Clicking a Location:** Opens that specific folder in Finder (macOS) or File Manager.

**Requirements:**
1.  **Terminal Support:** Works best in **iTerm2** (macOS) or modern terminals that support the hyperlink escape sequence.
2.  **How to Click:** In most terminals, hold **Command (⌘)** (or Ctrl on Linux) while clicking the link.

## ⚙️ Configuration

Open the `organize_downloads.py` script to adjust the configuration variables found at the top of the file:

* **SOURCE_DIR**: The directory to organize. Defaults to `Path.home() / "Downloads"`.
* **AGE_THRESHOLD_HOURS**: Time in hours before a file is moved. Defaults to **24**.
* **FILE_CATEGORIES**: The dictionary mapping folder names to file extensions.

## 📥 Installation & Usage

### Prerequisites
* Python 3 installed (`python3 --version`).

### Manual Run
1.  Clone this repository or download the script.
2.  Open your terminal.
3.  Run the script:

    python3 organize_downloads.py

## ⏱️ Automating with Cron (Nightly Run)

The best way to use this script is to set it and forget it.

### 1. Edit Crontab
Open your crontab config:

    crontab -e

### 2. Add the Job
Add the following line to run the script every night at **3:00 AM**.

*Note: Replace `/path/to/` with the actual path where you saved the script.*

    0 3 * * * /usr/bin/python3 /path/to/organize_downloads.py >> /tmp/download_organizer.log 2>&1

### 3. macOS Specific Security (Important!)
If you are running this on macOS (Catalina or newer), the operating system will block Cron from moving files out of your Downloads folder unless you grant it permission.

1.  Open **System Settings** > **Privacy & Security** > **Full Disk Access**.
2.  Click the `+` button.
3.  Press `Cmd` + `Shift` + `G` and type: `/usr/sbin/cron`
4.  Select `cron` and ensure the toggle is turned **ON**.

## 📄 License

This project is open source. Feel free to modify and distribute it as needed.