#!/usr/bin/env python3
"""
Repository Rule Checker Script

This script recursively scans the entire repository for files and directories,
reads and applies rules from system/gpt_behavior.json and system/ruleset.md,
and generates a comprehensive JSON report of rule compliance and violations.

The script is designed to be extensible for future rules and is written
to be beginner-friendly with clear documentation.

Usage: python repo_rule_checker.py
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple


class RuleChecker:
    """
    Main class for repository rule checking functionality.
    
    This class handles loading rules from configuration files, scanning
    the repository structure, and validating compliance with defined rules.
    """
    
    def __init__(self, repo_root: Path):
        """
        Initialize the RuleChecker with repository root path.
        
        Args:
            repo_root (Path): Root directory of the repository
        """
        self.repo_root = repo_root
        self.rules = {}
        self.violations = []
        self.checked_files = []
        self.scanned_directories = []
        self.id_registry = {}  # Track all IDs found in the repository
        self.file_references = {}  # Track file references and cross-references
        self.master_index = {}  # Store master index configuration for intelligent validation
        
    def load_gpt_behavior_rules(self) -> Dict[str, Any]:
        """
        Load and parse rules from system/gpt_behavior.json.
        
        Returns:
            Dict[str, Any]: Parsed GPT behavior rules
        """
        gpt_behavior_path = self.repo_root / "system" / "gpt_behavior.json"
        
        try:
            with open(gpt_behavior_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {gpt_behavior_path} not found.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {gpt_behavior_path}: {e}")
            return {}
    
    def load_master_index(self) -> Dict[str, Any]:
        """
        Load and parse master_index.json for intelligent path validation.
        
        Returns:
            Dict[str, Any]: Parsed master index configuration
        """
        master_index_path = self.repo_root / "master_index.json"
        
        try:
            with open(master_index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {master_index_path} not found.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {master_index_path}: {e}")
            return {}
    
    def get_area_status(self, path: str) -> str:
        """
        Get the status of an area from master_index.json.
        
        Args:
            path (str): Directory or file path to check
            
        Returns:
            str: Status of the area ('active', 'inactive', 'unknown')
        """
        if not self.master_index or 'areas' not in self.master_index:
            return 'unknown'
        
        # Normalize path for comparison
        normalized_path = path.rstrip('/') + '/'
        
        for area in self.master_index['areas']:
            area_dir = area.get('dir', '')
            if normalized_path.startswith(area_dir) or area_dir.startswith(normalized_path):
                return area.get('status', 'unknown')
        
        return 'unknown'
    
    def load_ruleset_md_rules(self) -> List[str]:
        """
        Load and parse rules from RULESET.md.
        
        Returns:
            List[str]: List of rules extracted from the markdown file
        """
        ruleset_path = self.repo_root / "RULESET.md"
        rules = []
        
        try:
            with open(ruleset_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract rules from markdown sections
            # Look for bullet points and numbered lists that contain guidelines
            rule_patterns = [
                r'^- (.+)$',  # Bullet points
                r'^\d+\. (.+)$',  # Numbered lists
                r'^\*\* (.+) \*\*',  # Bold statements
            ]
            
            for line in content.split('\n'):
                line = line.strip()
                for pattern in rule_patterns:
                    match = re.match(pattern, line)
                    if match:
                        rule_text = match.group(1).strip()
                        if len(rule_text) > 10:  # Filter out very short matches
                            rules.append(rule_text)
                            
        except FileNotFoundError:
            print(f"Warning: {ruleset_path} not found.")
            
        return rules
    
    def scan_repository_structure(self) -> Dict[str, Any]:
        """
        Recursively scan the entire repository structure.
        
        Returns:
            Dict[str, Any]: Complete repository structure with file metadata
        """
        structure = {
            "total_files": 0,
            "total_directories": 0,
            "file_types": {},
            "directory_tree": {},
            "files": []
        }
        
        # Directories to exclude from scanning
        excluded_dirs = {
            '.git', '.github', '__pycache__', '.pytest_cache',
            'node_modules', '.venv', 'venv', 'env', '.idea', '.vscode'
        }
        
        def scan_directory(current_path: Path, relative_path: str = "") -> Dict[str, Any]:
            """Recursively scan a directory and return its structure."""
            dir_info = {
                "name": current_path.name,
                "path": relative_path,
                "subdirectories": {},
                "files": []
            }
            
            try:
                for item in current_path.iterdir():
                    item_relative = str(item.relative_to(self.repo_root))
                    
                    if item.is_dir():
                        if item.name not in excluded_dirs and not item.name.startswith('.'):
                            structure["total_directories"] += 1
                            self.scanned_directories.append(item_relative)
                            dir_info["subdirectories"][item.name] = scan_directory(item, item_relative)
                    
                    elif item.is_file():
                        structure["total_files"] += 1
                        file_ext = item.suffix.lower()
                        
                        # Track file types
                        if file_ext in structure["file_types"]:
                            structure["file_types"][file_ext] += 1
                        else:
                            structure["file_types"][file_ext] = 1
                        
                        # Store file information
                        file_info = {
                            "name": item.name,
                            "path": item_relative,
                            "size": item.stat().st_size,
                            "extension": file_ext,
                            "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                        }
                        
                        dir_info["files"].append(file_info)
                        structure["files"].append(file_info)
                        self.checked_files.append(item_relative)
                        
            except PermissionError:
                print(f"Warning: Permission denied accessing {current_path}")
                
            return dir_info
        
        # Start scanning from repository root
        structure["directory_tree"] = scan_directory(self.repo_root)
        
        return structure
    
    def check_id_uniqueness(self) -> List[Dict[str, Any]]:
        """
        Check for ID uniqueness across all JSON files.
        
        Returns:
            List[Dict[str, Any]]: List of ID uniqueness violations
        """
        violations = []
        
        # Scan all JSON files for IDs
        for file_info in self.checked_files:
            file_path = self.repo_root / file_info
            
            # Skip the rule_check_results.json file as it's a report file, not a data file
            if file_info == "system/todo/rule_check_results.json":
                continue
            
            if file_path.suffix.lower() == '.json':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                    
                    # Extract IDs from various JSON structures
                    ids_in_file = self._extract_ids_from_json(content, file_info)
                    
                    for id_value in ids_in_file:
                        if id_value in self.id_registry:
                            violations.append({
                                "rule": "id_management",
                                "type": "duplicate_id",
                                "severity": "high",
                                "file": file_info,
                                "other_file": self.id_registry[id_value],
                                "id": id_value,
                                "message": f"Duplicate ID '{id_value}' found in {file_info} (also in {self.id_registry[id_value]})"
                            })
                        else:
                            self.id_registry[id_value] = file_info
                            
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Skip files that can't be parsed as JSON
                    continue
                except Exception as e:
                    violations.append({
                        "rule": "id_management",
                        "type": "file_read_error",
                        "severity": "medium",
                        "file": file_info,
                        "message": f"Error reading file {file_info}: {e}"
                    })
        
        return violations
    
    def _extract_ids_from_json(self, data: Any, file_path: str) -> List[str]:
        """
        Extract ID values from JSON data structures.
        
        Args:
            data: JSON data to analyze
            file_path: Path to the file being analyzed
            
        Returns:
            List[str]: List of ID values found
        """
        ids = []
        
        if isinstance(data, dict):
            # Look for common ID fields
            id_fields = ['id', 'key', 'actor_id', 'faction_id', 'item_id', 'event_id', 'mission_id']
            
            for field in id_fields:
                if field in data and isinstance(data[field], (str, int)):
                    ids.append(str(data[field]))
            
            # Recursively check nested objects
            for value in data.values():
                ids.extend(self._extract_ids_from_json(value, file_path))
                
        elif isinstance(data, list):
            # Check each item in the list
            for item in data:
                ids.extend(self._extract_ids_from_json(item, file_path))
        
        return ids
    
    def check_file_references(self) -> List[Dict[str, Any]]:
        """
        Check for broken file references and cross-references.
        
        Returns:
            List[Dict[str, Any]]: List of file reference violations
        """
        violations = []
        
        for file_info in self.checked_files:
            file_path = self.repo_root / file_info
            
            # Skip the rule_check_results.json file as it's a report file, not a data file
            if file_info == "system/todo/rule_check_results.json":
                continue
            
            try:
                if file_path.suffix.lower() == '.json':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_text = f.read()
                    
                    # Skip template files that contain invalid JSON with comments
                    if '"is_template": true' in content_text and '//' in content_text:
                        continue
                    
                    try:
                        content = json.loads(content_text)
                    except json.JSONDecodeError:
                        # Skip files that can't be parsed as valid JSON
                        continue
                    
                    # Check for file path references in JSON
                    references = self._extract_file_references(content)
                    
                    for ref in references:
                        # Skip template placeholders (anything with {{ and }})
                        if '{{' in ref and '}}' in ref:
                            continue
                            
                        # Handle relative paths - resolve relative to the file's directory
                        if ref.startswith('/'):
                            # Absolute path from repo root
                            ref_path = self.repo_root / ref.lstrip('/')
                        else:
                            # Relative path - resolve relative to the file's directory
                            file_dir = file_path.parent
                            ref_path = file_dir / ref
                        
                        if not ref_path.exists():
                            # Determine severity based on area status
                            area_status = self.get_area_status(ref)
                            
                            # For inactive areas, treat missing files as low severity
                            if area_status == 'inactive':
                                severity = 'low'
                                message_suffix = f" (area marked as '{area_status}' in master_index.json)"
                            else:
                                severity = 'high'
                                message_suffix = ""
                            
                            violations.append({
                                "rule": "crossref_redundancy_check",
                                "type": "broken_file_reference",
                                "severity": severity,
                                "file": file_info,
                                "reference": ref,
                                "area_status": area_status,
                                "message": f"Broken file reference '{ref}' in {file_info}{message_suffix}"
                            })
                
                elif file_path.suffix.lower() == '.md':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for markdown file references
                    md_references = re.findall(r'\[.*?\]\(([^)]+)\)', content)
                    
                    for ref in md_references:
                        if not ref.startswith(('http://', 'https://', '#')):
                            ref_path = self.repo_root / ref
                            if not ref_path.exists():
                                violations.append({
                                    "rule": "crossref_redundancy_check",
                                    "type": "broken_markdown_reference",
                                    "severity": "medium",
                                    "file": file_info,
                                    "reference": ref,
                                    "message": f"Broken markdown reference '{ref}' in {file_info}"
                                })
                
            except Exception as e:
                violations.append({
                    "rule": "crossref_redundancy_check",
                    "type": "file_analysis_error",
                    "severity": "low",
                    "file": file_info,
                    "message": f"Error analyzing file {file_info}: {e}"
                })
        
        return violations
    
    def _extract_file_references(self, data: Any) -> List[str]:
        """
        Extract file path references from JSON data.
        
        Args:
            data: JSON data to analyze
            
        Returns:
            List[str]: List of file references found
        """
        references = []
        
        if isinstance(data, dict):
            # Look for common file reference fields
            file_fields = ['index', 'file', 'path', 'dir', 'icon', 'image', 'script']
            
            for field in file_fields:
                if field in data and isinstance(data[field], str):
                    ref = data[field]
                    if '/' in ref or ref.endswith(('.json', '.md', '.py', '.txt', '.png', '.jpg')):
                        references.append(ref)
            
            # Recursively check nested objects
            for value in data.values():
                references.extend(self._extract_file_references(value))
                
        elif isinstance(data, list):
            for item in data:
                references.extend(self._extract_file_references(item))
        
        return references
    
    def check_pep8_compliance(self) -> List[Dict[str, Any]]:
        """
        Basic PEP8 compliance checking for Python files.
        
        Returns:
            List[Dict[str, Any]]: List of PEP8 violations
        """
        violations = []
        
        for file_info in self.checked_files:
            file_path = self.repo_root / file_info
            
            if file_path.suffix.lower() == '.py':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # Basic PEP8 checks
                    for line_num, line in enumerate(lines, 1):
                        # Check line length (PEP8 recommends max 79 characters)
                        if len(line.rstrip()) > 79:
                            violations.append({
                                "rule": "pep8_compliance",
                                "type": "line_too_long",
                                "severity": "low",
                                "file": file_info,
                                "line": line_num,
                                "message": f"Line {line_num} exceeds 79 characters ({len(line.rstrip())} chars)"
                            })
                        
                        # Check for tabs (PEP8 requires spaces)
                        if '\t' in line:
                            violations.append({
                                "rule": "pep8_compliance",
                                "type": "tab_usage",
                                "severity": "medium",
                                "file": file_info,
                                "line": line_num,
                                "message": f"Line {line_num} uses tabs instead of spaces"
                            })
                        
                        # Check for trailing whitespace
                        if line.endswith(' \n') or line.endswith(' \r\n'):
                            violations.append({
                                "rule": "pep8_compliance",
                                "type": "trailing_whitespace",
                                "severity": "low",
                                "file": file_info,
                                "line": line_num,
                                "message": f"Line {line_num} has trailing whitespace"
                            })
                
                except Exception as e:
                    violations.append({
                        "rule": "pep8_compliance",
                        "type": "file_analysis_error",
                        "severity": "low",
                        "file": file_info,
                        "message": f"Error analyzing Python file {file_info}: {e}"
                    })
        
        return violations
    
    def check_language_compliance(self) -> List[Dict[str, Any]]:
        """
        Check language compliance (English for system files).
        
        Returns:
            List[Dict[str, Any]]: List of language compliance violations
        """
        violations = []
        
        # German keywords that might indicate non-English content
        german_keywords = [
            'und', 'oder', 'der', 'die', 'das', 'eine', 'einen', 'einem',
            'für', 'mit', 'von', 'zu', 'auf', 'in', 'bei', 'nach',
            'über', 'unter', 'zwischen', 'während', 'wegen'
        ]
        
        for file_info in self.checked_files:
            file_path = self.repo_root / file_info
            
            # Only check system files for English compliance
            if file_info.startswith('system/'):
                try:
                    if file_path.suffix.lower() in ['.json', '.md', '.txt']:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                        
                        # Simple keyword-based detection
                        german_words_found = []
                        for keyword in german_keywords:
                            if f' {keyword} ' in content or f'"{keyword}"' in content:
                                german_words_found.append(keyword)
                        
                        if german_words_found:
                            violations.append({
                                "rule": "language_en",
                                "type": "non_english_content",
                                "severity": "medium",
                                "file": file_info,
                                "words": german_words_found,
                                "message": f"System file {file_info} may contain non-English content: {', '.join(german_words_found)}"
                            })
                
                except Exception as e:
                    violations.append({
                        "rule": "language_en",
                        "type": "file_analysis_error",
                        "severity": "low",
                        "file": file_info,
                        "message": f"Error analyzing language in {file_info}: {e}"
                    })
        
        return violations
    
    def run_all_checks(self) -> Dict[str, Any]:
        """
        Run all rule checks and compile results.
        
        Returns:
            Dict[str, Any]: Complete rule checking results
        """
        print("Loading master index for intelligent validation...")
        self.master_index = self.load_master_index()
        
        print("Loading GPT behavior rules...")
        gpt_rules = self.load_gpt_behavior_rules()
        
        print("Loading RULESET.md rules...")
        ruleset_rules = self.load_ruleset_md_rules()
        
        print("Scanning repository structure...")
        repository_structure = self.scan_repository_structure()
        
        print("Checking ID uniqueness...")
        id_violations = self.check_id_uniqueness()
        
        print("Checking file references...")
        reference_violations = self.check_file_references()
        
        print("Checking PEP8 compliance...")
        pep8_violations = self.check_pep8_compliance()
        
        print("Checking language compliance...")
        language_violations = self.check_language_compliance()
        
        # Compile all violations
        all_violations = (id_violations + reference_violations + 
                         pep8_violations + language_violations)
        
        # Generate summary statistics
        violation_summary = {}
        for violation in all_violations:
            rule = violation.get('rule', 'unknown')
            severity = violation.get('severity', 'unknown')
            
            if rule not in violation_summary:
                violation_summary[rule] = {'total': 0, 'high': 0, 'medium': 0, 'low': 0}
            
            violation_summary[rule]['total'] += 1
            violation_summary[rule][severity] += 1
        
        # Compile final results
        results = {
            "scan_info": {
                "timestamp": datetime.now().isoformat(),
                "repository_root": str(self.repo_root),
                "total_files_checked": len(self.checked_files),
                "total_directories_scanned": len(self.scanned_directories),
                "total_violations": len(all_violations),
                "master_index_loaded": bool(self.master_index)
            },
            "rules_loaded": {
                "gpt_behavior_rules": len(gpt_rules.get('rules', [])),
                "ruleset_md_rules": len(ruleset_rules),
                "gpt_rules_source": "system/gpt_behavior.json",
                "ruleset_rules_detail": ruleset_rules
            },
            "repository_structure": repository_structure,
            "violations": all_violations,
            "violation_summary": violation_summary,
            "id_registry": self.id_registry,
            "compliance_status": {
                "overall": "PASS" if len(all_violations) == 0 else "FAIL",
                "high_severity_issues": sum(1 for v in all_violations if v.get('severity') == 'high'),
                "medium_severity_issues": sum(1 for v in all_violations if v.get('severity') == 'medium'),
                "low_severity_issues": sum(1 for v in all_violations if v.get('severity') == 'low')
            },
            "master_index_areas": self.master_index.get('areas', []) if self.master_index else []
        }
        
        return results


def save_results(results: Dict[str, Any], output_path: Path) -> None:
    """
    Save the rule checking results to a JSON file.
    
    Args:
        results (Dict[str, Any]): Rule checking results
        output_path (Path): Path to save the results file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {output_path}")
    except Exception as e:
        print(f"Error saving results to {output_path}: {e}")
        sys.exit(1)


def main():
    """Main function to run the repository rule checker."""
    # Determine repository root (three levels up from this script)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent.parent
    
    print(f"Repository Rule Checker")
    print(f"Repository root: {repo_root}")
    print("=" * 50)
    
    # Initialize rule checker
    checker = RuleChecker(repo_root)
    
    # Run all checks
    results = checker.run_all_checks()
    
    # Save results
    output_path = repo_root / "system" / "todo" / "rule_check_results.json"
    save_results(results, output_path)
    
    # Print summary
    print("\n" + "=" * 50)
    print("RULE CHECK SUMMARY")
    print("=" * 50)
    print(f"Files checked: {results['scan_info']['total_files_checked']}")
    print(f"Directories scanned: {results['scan_info']['total_directories_scanned']}")
    print(f"Total violations: {results['scan_info']['total_violations']}")
    print(f"Overall status: {results['compliance_status']['overall']}")
    
    if results['scan_info']['total_violations'] > 0:
        print(f"- High severity: {results['compliance_status']['high_severity_issues']}")
        print(f"- Medium severity: {results['compliance_status']['medium_severity_issues']}")
        print(f"- Low severity: {results['compliance_status']['low_severity_issues']}")
        
        print("\nViolations by rule:")
        for rule, stats in results['violation_summary'].items():
            print(f"- {rule}: {stats['total']} violations")
    
    print(f"\nDetailed results saved to: {output_path}")


if __name__ == "__main__":
    main()