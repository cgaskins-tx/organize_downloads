#!/usr/bin/env python3

# download_stats.py
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

def get_directory_stats(directory):
    """
    Recursively scans a directory and returns a dictionary of statistics:
    {
        'count': int,
        'size': int,
        'oldest_date': datetime,
        'newest_date': datetime,
        'oldest_file': str,
        'newest_file': str
    }
    """
    stats = {
        'count': 0,
        'size': 0,
        'oldest_date': None,
        'newest_date': None,
        'oldest_file': "N/A",
        'newest_file': "N/A"
    }

    try:
        # Recursive scan
        for item in directory.rglob('*'):
            # Filter: Ignore hidden system files
            if item.name.startswith('.'):
                continue

            if item.is_file():
                try:
                    f_stat = item.stat()
                    f_size = f_stat.st_size
                    
                    # Date logic
                    try:
                        created = f_stat.st_birthtime
                    except AttributeError:
                        created = f_stat.st_ctime
                    
                    # We use the modification time for "newest" activity usually, 
                    # but let's stick to the max of create/mod to be safe.
                    f_date = max(f_stat.st_mtime, created)
                    f_dt_object = datetime.fromtimestamp(f_date)

                    # Update Aggregates
                    stats['count'] += 1
                    stats['size'] += f_size

                    # Update Oldest
                    if stats['oldest_date'] is None or f_date < stats['oldest_date'].timestamp():
                        stats['oldest_date'] = f_dt_object
                        stats['oldest_file'] = item.name

                    # Update Newest
                    if stats['newest_date'] is None or f_date > stats['newest_date'].timestamp():
                        stats['newest_date'] = f_dt_object
                        stats['newest_file'] = item.name

                except (OSError, PermissionError):
                    continue
    except KeyboardInterrupt:
        pass

    return stats

def main():
    console = Console()
    
    if not SOURCE_DIR.exists():
        console.print(f"[bold red]Error:[/bold red] Directory {SOURCE_DIR} does not exist.")
        return

    with console.status(f"[bold green]Calculating statistics for {SOURCE_DIR}...[/bold green]"):
        
        # 1. Get Overall Stats (Recursive scan of the whole folder)
        total_stats = get_directory_stats(SOURCE_DIR)

        # 2. Get Stats for each immediate subdirectory
        subdirs_stats = []
        for item in SOURCE_DIR.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                d_stats = get_directory_stats(item)
                d_stats['name'] = item.name
                subdirs_stats.append(d_stats)

    # ================= OVERALL TABLE =================
    summary_table = Table(title="Downloads Overview", box=box.ROUNDED, show_header=True)
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="white")

    summary_table.add_row("Total Size", get_human_readable_size(total_stats['size']))
    summary_table.add_row("Total Files", str(total_stats['count']))
    
    if total_stats['oldest_date']:
        summary_table.add_row("Oldest File", f"{total_stats['oldest_file']} ([green]{total_stats['oldest_date'].strftime('%Y-%m-%d')}[/green])")
        summary_table.add_row("Newest File", f"{total_stats['newest_file']} ([green]{total_stats['newest_date'].strftime('%Y-%m-%d')}[/green])")
    else:
        summary_table.add_row("Oldest File", "N/A")
        summary_table.add_row("Newest File", "N/A")

    console.print(summary_table)
    console.print("") # Spacer

    # ================= SUBDIRECTORY BREAKDOWN =================
    # Sort by size (descending)
    subdirs_stats.sort(key=lambda x: x['size'], reverse=True)

    breakdown_table = Table(title="Directory Breakdown", box=box.ROUNDED)
    breakdown_table.add_column("Directory", style="bold yellow")
    breakdown_table.add_column("Files", justify="center", style="white")
    breakdown_table.add_column("Size", justify="right", style="cyan")
    breakdown_table.add_column("Oldest File (Date)", style="dim")
    breakdown_table.add_column("Newest File (Date)", style="green")

    for d in subdirs_stats:
        if d['count'] > 0:
            oldest_str = f"{d['oldest_date'].strftime('%Y-%m-%d')}"
            newest_str = f"{d['newest_date'].strftime('%Y-%m-%d')}"
        else:
            oldest_str = "-"
            newest_str = "-"

        breakdown_table.add_row(
            d['name'],
            str(d['count']),
            get_human_readable_size(d['size']),
            oldest_str,
            newest_str
        )

    console.print(breakdown_table)

if __name__ == "__main__":
    main()