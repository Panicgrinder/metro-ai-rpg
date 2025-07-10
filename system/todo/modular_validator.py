#!/usr/bin/env python3
"""
Modular Data Validation Tool

Validates the new modular data structure for token efficiency and consistency.
Designed to complement the existing rule checker with specific validation
for the mechanics/lore separation and modular loading system.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set, Any


def validate_modular_structure(repo_root: Path) -> Dict[str, Any]:
    """
    Validate the modular data structure for consistency and efficiency.
    
    Returns:
        Dict with validation results
    """
    results = {
        "valid": True,
        "warnings": [],
        "errors": [],
        "token_estimates": {},
        "cross_references": {}
    }
    
    # Paths to check
    mechanics_path = repo_root / "data" / "mechanics" / "factions_core.json"
    lore_path = repo_root / "data" / "lore" / "factions_narrative.json"
    config_path = repo_root / "data" / "modules" / "loading_config.json"
    
    # Validate file existence
    if not mechanics_path.exists():
        results["errors"].append("Missing core mechanics file: data/mechanics/factions_core.json")
        results["valid"] = False
        return results
    
    if not lore_path.exists():
        results["errors"].append("Missing lore file: data/lore/factions_narrative.json")
        results["valid"] = False
        return results
    
    if not config_path.exists():
        results["warnings"].append("Missing loading config: data/modules/loading_config.json")
    
    try:
        # Load and validate mechanics data
        with open(mechanics_path, 'r', encoding='utf-8') as f:
            mechanics_data = json.load(f)
        
        with open(lore_path, 'r', encoding='utf-8') as f:
            lore_data = json.load(f)
        
        # Validate structure
        results.update(validate_mechanics_structure(mechanics_data))
        results.update(validate_lore_structure(lore_data))
        results.update(validate_cross_references(mechanics_data, lore_data))
        
        # Estimate token usage
        results["token_estimates"] = estimate_token_usage(mechanics_data, lore_data)
        
        # Validate loading config if it exists
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            results.update(validate_loading_config(config_data))
        
    except json.JSONDecodeError as e:
        results["errors"].append(f"JSON parsing error: {e}")
        results["valid"] = False
    except Exception as e:
        results["errors"].append(f"Validation error: {e}")
        results["valid"] = False
    
    return results


def validate_mechanics_structure(data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate mechanics data structure for purity and efficiency."""
    warnings = []
    errors = []
    
    if "factions" not in data:
        errors.append("Mechanics data missing 'factions' key")
        return {"warnings": warnings, "errors": errors}
    
    factions = data["factions"]
    
    for faction_id, faction_data in factions.items():
        # Check required mechanical fields
        required_fields = ["id", "name", "territory", "stats", "relations", "abilities", "type"]
        for field in required_fields:
            if field not in faction_data:
                errors.append(f"Faction {faction_id} missing required field: {field}")
        
        # Check for narrative contamination in mechanics
        narrative_fields = ["description", "history", "culture", "objectives", "motto"]
        for field in narrative_fields:
            if field in faction_data:
                warnings.append(f"Faction {faction_id} contains narrative field '{field}' in mechanics data")
        
        # Validate numerical relations
        if "relations" in faction_data:
            for target, value in faction_data["relations"].items():
                if not isinstance(value, (int, float)) or value < -2 or value > 2:
                    errors.append(f"Faction {faction_id} has invalid relation value for {target}: {value}")
        
        # Validate stats structure
        if "stats" in faction_data:
            expected_stats = ["military_strength", "economic_power", "territory_control", "population"]
            for stat in expected_stats:
                if stat not in faction_data["stats"]:
                    warnings.append(f"Faction {faction_id} missing recommended stat: {stat}")
                elif not isinstance(faction_data["stats"][stat], (int, float)):
                    errors.append(f"Faction {faction_id} has non-numeric stat {stat}")
    
    return {"warnings": warnings, "errors": errors}


def validate_lore_structure(data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate lore data structure for completeness and organization."""
    warnings = []
    errors = []
    
    if "lore_modules" not in data:
        errors.append("Lore data missing 'lore_modules' key")
        return {"warnings": warnings, "errors": errors}
    
    lore_modules = data["lore_modules"]
    
    for module_id, module_data in lore_modules.items():
        # Check required lore fields
        required_fields = ["faction_id", "detailed_description", "founding_story", "culture", "objectives"]
        for field in required_fields:
            if field not in module_data:
                warnings.append(f"Lore module {module_id} missing recommended field: {field}")
        
        # Check for mechanical contamination in lore
        mechanical_fields = ["stats", "abilities", "type"]
        for field in mechanical_fields:
            if field in module_data:
                warnings.append(f"Lore module {module_id} contains mechanical field '{field}' in lore data")
    
    return {"warnings": warnings, "errors": errors}


def validate_cross_references(mechanics: Dict[str, Any], lore: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate cross-references between mechanics and lore data."""
    warnings = []
    errors = []
    cross_refs = {}
    
    if "factions" not in mechanics or "lore_modules" not in lore:
        return {"warnings": warnings, "errors": errors, "cross_references": cross_refs}
    
    mechanic_factions = set(mechanics["factions"].keys())
    lore_faction_refs = set()
    
    # Extract faction references from lore modules
    for module_id, module_data in lore["lore_modules"].items():
        if "faction_id" in module_data:
            lore_faction_refs.add(module_data["faction_id"])
    
    # Check for missing cross-references
    missing_lore = mechanic_factions - lore_faction_refs
    missing_mechanics = lore_faction_refs - mechanic_factions
    
    for faction_id in missing_lore:
        warnings.append(f"Faction {faction_id} has mechanics but no lore module")
    
    for faction_id in missing_mechanics:
        errors.append(f"Lore references faction {faction_id} that doesn't exist in mechanics")
    
    cross_refs["mechanics_count"] = len(mechanic_factions)
    cross_refs["lore_count"] = len(lore_faction_refs)
    cross_refs["complete_pairs"] = len(mechanic_factions & lore_faction_refs)
    
    return {"warnings": warnings, "errors": errors, "cross_references": cross_refs}


def validate_loading_config(config: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate loading configuration for consistency."""
    warnings = []
    errors = []
    
    if "load_contexts" not in config:
        errors.append("Loading config missing 'load_contexts'")
        return {"warnings": warnings, "errors": errors}
    
    # Check that referenced files exist
    for context_name, context_data in config["load_contexts"].items():
        if "modules" in context_data:
            for module_path in context_data["modules"]:
                # Convert relative path to absolute for checking
                full_path = Path(__file__).parent.parent.parent / module_path
                if not full_path.exists():
                    warnings.append(f"Loading config references non-existent file: {module_path}")
    
    return {"warnings": warnings, "errors": errors}


def estimate_token_usage(mechanics: Dict[str, Any], lore: Dict[str, Any]) -> Dict[str, int]:
    """Estimate token usage for different loading scenarios."""
    # Simple estimation: ~4 characters per token
    mechanics_size = len(json.dumps(mechanics, separators=(',', ':')))
    lore_size = len(json.dumps(lore, separators=(',', ':')))
    
    return {
        "mechanics_only": mechanics_size // 4,
        "lore_only": lore_size // 4,
        "combined": (mechanics_size + lore_size) // 4,
        "mechanics_chars": mechanics_size,
        "lore_chars": lore_size
    }


def print_validation_report(results: Dict[str, Any]) -> None:
    """Print a human-readable validation report."""
    print("=" * 60)
    print("🔍 MODULAR DATA VALIDATION REPORT")
    print("=" * 60)
    
    # Overall status
    status_icon = "✅" if results["valid"] else "❌"
    print(f"{status_icon} Overall Status: {'VALID' if results['valid'] else 'INVALID'}")
    
    # Errors
    if results["errors"]:
        print(f"\n🚨 ERRORS ({len(results['errors'])})")
        for error in results["errors"]:
            print(f"   ❌ {error}")
    else:
        print("\n✅ No errors found")
    
    # Warnings
    if results["warnings"]:
        print(f"\n⚠️  WARNINGS ({len(results['warnings'])})")
        for warning in results["warnings"]:
            print(f"   ⚠️  {warning}")
    
    # Token estimates
    if "token_estimates" in results:
        print(f"\n📊 TOKEN USAGE ESTIMATES")
        estimates = results["token_estimates"]
        print(f"   🔧 Mechanics only: ~{estimates['mechanics_only']} tokens")
        print(f"   📚 Lore only: ~{estimates['lore_only']} tokens") 
        print(f"   🔄 Combined: ~{estimates['combined']} tokens")
        print(f"   💡 Efficiency ratio: {estimates['mechanics_only'] / estimates['combined']:.1%} mechanics")
    
    # Cross-references
    if "cross_references" in results:
        cross_refs = results["cross_references"]
        if cross_refs:
            print(f"\n🔗 CROSS-REFERENCE STATUS")
            print(f"   📄 Factions with mechanics: {cross_refs.get('mechanics_count', 0)}")
            print(f"   📖 Factions with lore: {cross_refs.get('lore_count', 0)}")
            print(f"   ✅ Complete pairs: {cross_refs.get('complete_pairs', 0)}")
    
    print("\n" + "=" * 60)


def main():
    """Main validation function."""
    # Get repository root (three levels up from this script)
    repo_root = Path(__file__).resolve().parent.parent.parent
    
    print(f"Modular Data Validation")
    print(f"Repository root: {repo_root}")
    print(f"Checking modular data structure...")
    
    results = validate_modular_structure(repo_root)
    print_validation_report(results)
    
    # Save results
    output_path = repo_root / "system" / "todo" / "modular_validation.json"
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Detailed results saved to: {output_path}")
    except Exception as e:
        print(f"\n❌ Error saving results: {e}")


if __name__ == "__main__":
    main()