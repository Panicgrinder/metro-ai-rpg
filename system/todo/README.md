# Master Index Update Script

This directory contains the `update_master_index.py` script that automates the process of updating the `master_index.json` file.

## Purpose

The script scans all major project directories in the repository, compares them to the entries in `master_index.json`, and:
- Adds missing directories as new areas
- Updates existing directory/index paths if they've changed  
- Marks missing directories as inactive
- Updates metadata (last_modified timestamp and last_updated_by)

## Usage

From the repository root:
```bash
python system/todo/update_master_index.py
```

Or directly:
```bash
./system/todo/update_master_index.py
```

From any directory:
```bash
cd system/todo
python update_master_index.py
```

## What it does

1. **Scans directories**: Looks for all directories in the repository root (excluding system directories like `.git`, `system`, etc.)

2. **Detects index files**: For each directory, searches for common index file patterns:
   - `{directory_name}.json`
   - `index.json` 
   - `main.json`
   - Special cases (e.g., `market.json` for economy, `recipes.json` for crafting)

3. **Updates master index**: 
   - Preserves existing entries and updates them
   - Adds new directories that weren't previously indexed
   - Marks directories as inactive if they no longer exist
   - Updates the status based on whether index files exist

4. **Safe operation**: The script is idempotent - running it multiple times won't cause issues

## Output

The script provides detailed output showing what changes it's making:
- New areas being added
- Paths being updated
- Status changes (active/inactive)
- Final count of total areas

## Requirements

- Python 3.6+
- No additional dependencies (uses only standard library)