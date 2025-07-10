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
        # Store master index configuration for intelligent validation
        self.master_index = {}

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
            if (normalized_path.startswith(area_dir) or
                    area_dir.startswith(normalized_path)):
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

        def scan_directory(current_path: Path,
                           relative_path: str = "") -> Dict[str, Any]:
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
                        if (item.name not in excluded_dirs and
                                not item.name.startswith('.')):
                            structure["total_directories"] += 1
                            self.scanned_directories.append(item_relative)
                            dir_info["subdirectories"][item.name] = scan_directory(
                                item, item_relative)

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
                            "modified": datetime.fromtimestamp(
                                item.stat().st_mtime).isoformat()
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
                                "message": (f"Duplicate ID '{id_value}' found in "
                                           f"{file_info} (also in {self.id_registry[id_value]})")
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
            id_fields = ['id', 'key', 'actor_id', 'faction_id', 'item_id',
                         'event_id', 'mission_id']

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
        Check language compliance for technical documentation.

        This is a German RPG project, so German content is expected in game files.
        Only technical files like scripts and core documentation should be checked.

        Returns:
            List[Dict[str, Any]]: List of language compliance violations
        """
        violations = []

        # For a German RPG project, be more lenient with language checks
        # Only flag README files that are completely missing English sections
        for file_info in self.checked_files:
            file_path = self.repo_root / file_info

            # Only check main README for accessibility
            if file_info == 'README.md':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()

                    # Check if it's completely missing English technical terms
                    english_terms = ['install', 'usage', 'setup', 'requirements', 'getting started', 'installation']
                    has_english = any(term in content for term in english_terms)

                    if not has_english and len(content) > 100:
                        violations.append({
                            "rule": "language_en",
                            "type": "missing_english_documentation",
                            "severity": "low",
                            "file": file_info,
                            "message": f"Technical documentation {file_info} should include English sections for broader accessibility"
                        })

                except Exception:
                    # Skip files that can't be read
                    pass

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


def create_summary_report(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a clean, actionable summary report.

    Args:
        results (Dict[str, Any]): The complete results dictionary

    Returns:
        Dict[str, Any]: Clean summary report focused on actionable items
    """
    # Group violations by type and file for easier action
    actionable_violations = {}
    pep8_summary = {"files_affected": 0, "quick_fixes": 0, "total_issues": 0}

    for violation in results['violations']:
        rule = violation.get('rule')
        severity = violation.get('severity')
        file_path = violation.get('file')

        # Skip low-priority PEP8 violations, just summarize them
        if rule == 'pep8_compliance' and severity == 'low':
            pep8_summary["total_issues"] += 1
            if violation.get('type') in ['trailing_whitespace', 'missing_final_newline']:
                pep8_summary["quick_fixes"] += 1
            continue

        # Group other violations by file
        if file_path not in actionable_violations:
            actionable_violations[file_path] = []
        actionable_violations[file_path].append({
            "rule": rule,
            "type": violation.get('type'),
            "severity": severity,
            "message": violation.get('message'),
            "line": violation.get('line') if 'line' in violation else None,
            "reference": violation.get('reference') if 'reference' in violation else None
        })

    # Count PEP8-affected files
    pep8_files = set()
    for violation in results['violations']:
        if violation.get('rule') == 'pep8_compliance':
            pep8_files.add(violation.get('file'))
    pep8_summary["files_affected"] = len(pep8_files)

    return {
        "scan_info": {
            "timestamp": results['scan_info']['timestamp'],
            "total_files_checked": results['scan_info']['total_files_checked'],
            "total_violations": results['scan_info']['total_violations'],
            "status": results['compliance_status']['overall']
        },
        "priority_violations": {
            "high_severity": results['compliance_status']['high_severity_issues'],
            "medium_severity": results['compliance_status']['medium_severity_issues'],
            "actionable_files": actionable_violations
        },
        "pep8_summary": pep8_summary,
        "violation_breakdown": results['violation_summary']
    }


def save_results(results: Dict[str, Any], output_path: Path) -> None:
    """
    Save both detailed and summary results.

    Args:
        results (Dict[str, Any]): The complete results dictionary
        output_path (Path): Path where to save the JSON results file
    """
    try:
        # Save streamlined detailed results
        streamlined_results = {
            "scan_info": results['scan_info'],
            "compliance_status": results['compliance_status'],
            "violations": results['violations'],
            "violation_summary": results['violation_summary']
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(streamlined_results, f, indent=2, ensure_ascii=False)

        # Save clean summary report
        summary_path = output_path.parent / "rule_check_summary.json"
        summary_results = create_summary_report(results)
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary_results, f, indent=2, ensure_ascii=False)

        print(f"Results saved to {output_path}")
        print(f"Summary saved to {summary_path}")
    except Exception as e:
        print(f"Error saving results: {e}")
        sys.exit(1)


def print_summary(results: Dict[str, Any], output_path: Path) -> None:
    """
    Print a clean, actionable summary to the console.

    Args:
        results (Dict[str, Any]): The complete results dictionary
        output_path (Path): Path where the detailed results were saved
    """
    print("=" * 60)
    print("🔍 REPOSITORY RULE CHECK SUMMARY")
    print("=" * 60)

    # Overall status
    status_icon = "✅" if results['compliance_status']['overall'] == 'PASS' else "❌"
    print(f"{status_icon} Overall Status: {results['compliance_status']['overall']}")
    print(f"📁 Files Scanned: {results['scan_info']['total_files_checked']}")
    print(f"📊 Total Issues: {results['scan_info']['total_violations']}")

    # Priority issues
    high_issues = results['compliance_status']['high_severity_issues']
    medium_issues = results['compliance_status']['medium_severity_issues']
    low_issues = results['compliance_status']['low_severity_issues']

    if high_issues > 0:
        print(f"\n🚨 HIGH PRIORITY: {high_issues} issues require immediate attention")
    if medium_issues > 0:
        print(f"⚠️  MEDIUM PRIORITY: {medium_issues} issues should be addressed")
    if low_issues > 0:
        print(f"💡 LOW PRIORITY: {low_issues} minor issues (mostly code style)")

    if results['scan_info']['total_violations'] == 0:
        print("\n🎉 No violations found! Repository is compliant.")
        return

    # Actionable violations summary
    print(f"\n{'='*60}")
    print("🎯 ACTIONABLE ISSUES (excluding minor PEP8)")
    print("=" * 60)

    actionable_count = 0
    pep8_count = 0

    # Group violations by file for cleaner display
    file_violations = {}
    for violation in results['violations']:
        if violation.get('rule') == 'pep8_compliance' and violation.get('severity') == 'low':
            pep8_count += 1
            continue

        file_path = violation.get('file', 'unknown')
        if file_path not in file_violations:
            file_violations[file_path] = []
        file_violations[file_path].append(violation)
        actionable_count += 1

    if actionable_count == 0:
        print("✅ No high-priority actionable issues found!")
    else:
        for file_path, violations in file_violations.items():
            print(f"\n📄 {file_path}")
            for v in violations:
                severity_icon = "🚨" if v.get('severity') == 'high' else "⚠️" if v.get('severity') == 'medium' else "💡"
                line_info = f" (line {v.get('line')})" if v.get('line') else ""
                ref_info = f" → {v.get('reference')}" if v.get('reference') else ""
                print(f"   {severity_icon} {v.get('type', 'unknown')}{line_info}{ref_info}")
                print(f"      {v.get('message', 'No message')}")

    # PEP8 summary
    if pep8_count > 0:
        pep8_files = set()
        quick_fixes = 0
        for violation in results['violations']:
            if violation.get('rule') == 'pep8_compliance':
                pep8_files.add(violation.get('file'))
                if violation.get('type') in ['trailing_whitespace', 'missing_final_newline']:
                    quick_fixes += 1

        print(f"\n{'='*60}")
        print("🎨 PEP8 CODE STYLE SUMMARY")
        print("=" * 60)
        print(f"📝 {pep8_count} style issues in {len(pep8_files)} files")
        print(f"⚡ {quick_fixes} quick fixes (whitespace/newlines)")
        print(f"🔧 To auto-fix: autopep8 --in-place --aggressive --aggressive <file>")

    print(f"\n{'='*60}")
    print("📋 REPORTS GENERATED")
    print("=" * 60)
    print(f"📄 Detailed report: {output_path}")
    print(f"📄 Summary report: {output_path.parent / 'rule_check_summary.json'}")
    print(f"💡 Focus on summary report for actionable items")


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
    print_summary(results, output_path)


if __name__ == "__main__":
    main()