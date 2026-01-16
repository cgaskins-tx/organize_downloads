#!/usr/bin/env python3

# recent_downloads.py
# version: 1.0
# date: 16-January-2026
# author: Chris C. Gaskins
# github: https://github.com/cgaskins-tx/organize_downloads

import argparse
import os
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box

# Configuration
SOURCE_DIR = Path.home() / "Downloads"

def get_human_readable_size(size_in_bytes):
    """Converts bytes to human readable string (KB, MB, GB)."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"

def get_files_recursive(directory):
    """Scans directory and returns a list of file dictionaries."""
    file_list = []
    
    try:
        for item in directory.rglob('*'):
            # Filter: Ignore hidden system files (start with dot)
            if item.name.startswith('.'):
                continue

            if item.is_file():
                try:
                    stats = item.stat()
                    
                    # Size
                    size = stats.st_size
                    
                    # Date (Most recent of Modified or Created)
                    try:
                        created = stats.st_birthtime
                    except AttributeError:
                        created = stats.st_ctime
                        
                    date_timestamp = max(stats.st_mtime, created)
                    date_display = datetime.fromtimestamp(date_timestamp).strftime('%Y-%m-%d %H:%M')

                    # Relative Path (Location)
                    try:
                        relative_path = item.parent.relative_to(SOURCE_DIR)
                        if str(relative_path) == ".":
                            location = "/" # Root of Downloads
                        else:
                            location = str(relative_path)
                    except ValueError:
                        location = str(item.parent)

                    # URIs for clickable links
                    file_uri = item.absolute().as_uri()
                    folder_uri = item.parent.absolute().as_uri()

                    file_list.append({
                        "name": item.name,
                        "path": item,
                        "location": location,
                        "size": size,
                        "type": item.suffix.lower() or "None",
                        "date_display": date_display,
                        "timestamp": date_timestamp,
                        "file_uri": file_uri,
                        "folder_uri": folder_uri
                    })
                except (OSError, PermissionError):
                    continue
    except KeyboardInterrupt:
        pass

    return file_list

def main():
    # 1. Handle Arguments
    parser = argparse.ArgumentParser(description="Find most recent files in Downloads.")
    parser.add_argument('limit', type=int, nargs='?', default=10, 
                        help="Number of files to display (default: 10)")
    args = parser.parse_args()

    console = Console()
    
    if not SOURCE_DIR.exists():
        console.print(f"[bold red]Error:[/bold red] Directory {SOURCE_DIR} does not exist.")
        return

    with console.status(f"[bold green]Scanning {SOURCE_DIR}...[/bold green]"):
        files = get_files_recursive(SOURCE_DIR)

    # 2. Sort by Date (Descending / Newest First)
    files.sort(key=lambda x: x['timestamp'], reverse=True)

    # 3. Slice the top N
    top_files = files[:args.limit]

    # 4. Build Table
    table = Table(title=f"Top {len(top_files)} Most Recent Files in Downloads", box=box.ROUNDED)

    # Adjusted column order to prioritize Date
    table.add_column("Date", justify="center", style="green", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Size", justify="right", style="cyan")
    table.add_column("Type", justify="center", style="magenta")
    table.add_column("Location", style="yellow")

    for f in top_files:
        # Link Logic: [bold][link=file://...]filename[/link][/bold]
        name_display = f"[bold][link={f['file_uri']}]{f['name']}[/link][/bold]"
        location_display = f"[bold][link={f['folder_uri']}]{f['location']}[/link][/bold]"

        table.add_row(
            f['date_display'],
            name_display,
            get_human_readable_size(f['size']),
            f['type'],
            location_display
        )

    console.print(table)
    console.print("[dim]Tip: Cmd+Click filenames to open them. Cmd+Click Location to open folder.[/dim]")

if __name__ == "__main__":
    main()