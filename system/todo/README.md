# System TODO Scripts

This directory contains automation scripts for maintaining and validating the repository.

## Scripts

### 1. Master Index Update Script (`update_master_index.py`)

This script automates the process of updating the `master_index.json` file.

#### Purpose

The script scans all major project directories in the repository, compares them to the entries in `master_index.json`, and:
- Adds missing directories as new areas
- Updates existing directory/index paths if they've changed  
- Marks missing directories as inactive
- Updates metadata (last_modified timestamp and last_updated_by)

#### Usage

From the repository root:
```bash
python system/todo/update_master_index.py
```

Or directly:
```bash
system/todo/update_master_index.py
```

From any directory:
```bash
cd system/todo
python update_master_index.py
```

#### What it does

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

### 2. Repository Rule Checker (`repo_rule_checker.py`)

This script recursively scans the entire repository and validates compliance with rules defined in `system/gpt_behavior.json` and `RULESET.md`.

#### Purpose

The script provides comprehensive rule checking functionality:
- Scans all files and directories recursively
- Validates ID uniqueness across JSON files
- Checks file references and cross-references
- Validates PEP8 compliance for Python files
- Checks language compliance (English for system files)
- Generates detailed JSON reports with violations and statistics

#### Usage

From the repository root:
```bash
python system/todo/repo_rule_checker.py
```

Or directly:
```bash
system/todo/repo_rule_checker.py
```

#### Features

1. **Rule Loading**: Automatically loads rules from:
   - `system/gpt_behavior.json` - System behavior rules
   - `RULESET.md` - Repository guidelines

2. **Repository Scanning**: Recursively scans all files and directories (excluding `.git`, `node_modules`, etc.)

3. **Rule Validation**:
   - **ID Management**: Checks for duplicate IDs across JSON files
   - **Cross-reference Validation**: Verifies file references and paths
   - **PEP8 Compliance**: Basic Python code style checking
   - **Language Compliance**: Ensures system files use English

4. **Extensible Design**: Easy to add new rules and checks

5. **Comprehensive Reporting**: Generates detailed JSON output with:
   - Complete repository structure
   - All violations with severity levels
   - Summary statistics
   - ID registry
   - Compliance status

#### Output

The script generates:
- Console output with summary statistics
- `rule_check_results.json` - Detailed JSON report with all findings

#### Violation Severity Levels

- **High**: Critical issues (duplicate IDs, broken references)
- **Medium**: Important issues (tabs in Python, non-English system files)
- **Low**: Style issues (long lines, trailing whitespace)

## Requirements

- Python 3.6+
- No additional dependencies (uses only standard library)

## File Output

Both scripts generate/update files in the repository:
- `update_master_index.py` → Updates `master_index.json`
- `repo_rule_checker.py` → Creates `system/todo/rule_check_results.json`