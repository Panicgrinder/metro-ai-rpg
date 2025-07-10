#!/usr/bin/env python3
"""
Script to automatically update the master_index.json file.

This script scans all major project directories, compares them to the entries
in master_index.json, adds missing areas, updates directory/index paths,
and marks missing ones as inactive.

Usage: python update_master_index.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def find_index_file(directory_path):
    """
    Find the most likely index file for a given directory.

    Args:
        directory_path (Path): Path to the directory to search

    Returns:
        str or None: Relative path to the index file, or None if not found
    """
    if not directory_path.exists() or not directory_path.is_dir():
        return None

    directory_name = directory_path.name

    # Common index file patterns to search for
    patterns = [
        f"{directory_name}.json",
        "index.json",
        "main.json",
        f"{directory_name}s.json",  # plural form
    ]

    # Special cases for known directories
    special_cases = {
        "economy": ["market.json", "economy.json"],
        "crafting": ["recipes.json", "crafting.json"],
        "world": ["world.json", "locations.json", "sectors.json"],
    }

    if directory_name in special_cases:
        patterns = special_cases[directory_name] + patterns

    for pattern in patterns:
        index_file = directory_path / pattern
        if index_file.exists():
            return str(index_file.relative_to(directory_path.parent))

    return None


def scan_repository_directories(repo_root):
    """
    Scan the repository for major project directories.

    Args:
        repo_root (Path): Root path of the repository

    Returns:
        dict: Dictionary mapping directory names to their info
    """
    # Directories to exclude from scanning
    excluded_dirs = {
        '.git', '.github', 'system', '__pycache__', '.pytest_cache',
        'node_modules', '.venv', 'venv', 'env'
    }

    found_areas = {}

    for item in repo_root.iterdir():
        if (item.is_dir() and
            item.name not in excluded_dirs and
            not item.name.startswith('.')):

            # Look for index file
            index_file = find_index_file(item)

            # Determine status based on directory contents
            status = ("active" if index_file and
                      Path(repo_root / index_file).exists() else "inactive")

            found_areas[item.name] = {
                "key": item.name,
                "dir": f"{item.name}/",
                "index": index_file,
                "status": status
            }

    return found_areas


def load_master_index(master_index_path):
    """
    Load the existing master_index.json file.

    Args:
        master_index_path (Path): Path to the master_index.json file

    Returns:
        dict: Parsed master index data
    """
    try:
        with open(master_index_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {master_index_path} not found. Creating new index.")
        return {
            "areas": [],
            "meta": {
                "created_by": "AI-System",
                "last_updated_by": "AI-System"
            }
        }
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {master_index_path}: {e}")
        sys.exit(1)


def update_master_index(master_index, found_areas, repo_root):
    """
    Update the master index with found areas.

    Args:
        master_index (dict): Current master index data
        found_areas (dict): Areas found in the repository
        repo_root (Path): Root path of the repository

    Returns:
        dict: Updated master index data
    """
    # Create a map of existing areas by key for easy lookup
    existing_areas = {area["key"]: area for area in master_index["areas"]}
    updated_areas = []

    # Process existing areas
    for area in master_index["areas"]:
        key = area["key"]

        if key in found_areas:
            # Update existing area with current information
            found_area = found_areas[key]
            updated_area = area.copy()

            # Update paths if they've changed
            if updated_area["dir"] != found_area["dir"]:
                print(f"Updating directory path for '{key}': "
                      f"{updated_area['dir']} -> {found_area['dir']}")
                updated_area["dir"] = found_area["dir"]

            if updated_area["index"] != found_area["index"]:
                print(f"Updating index path for '{key}': "
                      f"{updated_area['index']} -> {found_area['index']}")
                updated_area["index"] = found_area["index"]

            # Update status based on current state
            if updated_area["status"] != found_area["status"]:
                print(f"Updating status for '{key}': "
                      f"{updated_area['status']} -> {found_area['status']}")
                updated_area["status"] = found_area["status"]

            updated_areas.append(updated_area)
            # Remove from found_areas since we've processed it
            del found_areas[key]
        else:
            # Area exists in master index but not found in repository
            if area["status"] != "inactive":
                print(f"Marking '{key}' as inactive (directory not found)")
                area["status"] = "inactive"
            updated_areas.append(area)

    # Add new areas that weren't in the existing master index
    for key, area_info in found_areas.items():
        print(f"Adding new area: '{key}'")
        updated_areas.append(area_info)

    # Update the master index
    master_index["areas"] = updated_areas

    # Update metadata
    master_index["meta"]["last_modified"] = (datetime.now().isoformat() +
                                             "+00:00")
    master_index["meta"]["last_updated_by"] = "AI-System"

    return master_index


def save_master_index(master_index, master_index_path):
    """
    Save the updated master index to file.

    Args:
        master_index (dict): Updated master index data
        master_index_path (Path): Path to save the master_index.json file
    """
    try:
        with open(master_index_path, 'w', encoding='utf-8') as f:
            json.dump(master_index, f, indent=2, ensure_ascii=False)
        print(f"Successfully updated {master_index_path}")
    except Exception as e:
        print(f"Error saving {master_index_path}: {e}")
        sys.exit(1)


def main():
    """Main function to update the master index."""
    # Determine repository root (two levels up from this script)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent.parent
    master_index_path = repo_root / "master_index.json"

    print(f"Repository root: {repo_root}")
    print(f"Master index path: {master_index_path}")
    print()

    # Load existing master index
    print("Loading existing master_index.json...")
    master_index = load_master_index(master_index_path)
    print(f"Found {len(master_index['areas'])} existing areas")
    print()

    # Scan repository for directories
    print("Scanning repository directories...")
    found_areas = scan_repository_directories(repo_root)
    print(f"Found {len(found_areas)} directories in repository")
    print()

    # Update master index
    print("Updating master index...")
    updated_master_index = update_master_index(master_index, found_areas, repo_root)
    print()

    # Save updated master index
    print("Saving updated master_index.json...")
    save_master_index(updated_master_index, master_index_path)
    print()

    print(f"Master index update complete! Total areas: {len(updated_master_index['areas'])}")


if __name__ == "__main__":
    main()