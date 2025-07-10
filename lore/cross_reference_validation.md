# Cross-Reference Validation Guide

*Guidelines for maintaining data integrity across the lore system*

## Overview

The Metro-AI-RPG lore system implements a comprehensive cross-reference system where different entities (factions, characters, sectors, relations) reference each other through consistent IDs. This document outlines validation requirements and best practices.

## ID Reference Patterns

### Faction References
- **Faction ID Format**: `snake_case` (e.g., `watcher`, `tech_alliance`)
- **Referenced in**: Character affiliations, faction relations, sector control, trade agreements

### Character References  
- **Character ID Format**: `CHAR_` prefix + descriptive identifier (e.g., `CHAR_watcher_commander_01`)
- **Referenced in**: Faction leadership, character relationships, diplomatic contacts

### Sector References
- **Sector ID Format**: Grid coordinates `A1`-`J10` 
- **Referenced in**: Faction territories, character locations, trade routes, faction relations

### Relation References
- **Relation ID Format**: `REL_` prefix + faction combination (e.g., `REL_watcher_merchants`)
- **Referenced in**: Diplomatic history, trade agreements, conflict records

## Validation Requirements

### 1. Reference Integrity
All references must point to existing entities:
```json
// ✅ Valid - references existing faction
"faction_affiliation": "watcher"

// ❌ Invalid - references non-existent faction  
"faction_affiliation": "unknown_faction"
```

### 2. Bidirectional Consistency
Relationships must be consistent in both directions:
```json
// Faction A lists B as ally
"allies": ["faction_b"]

// Faction B must also list A as ally
"allies": ["faction_a"]
```

### 3. Hierarchy Validation
Leadership and control structures must be logically consistent:
```json
// Faction leadership must reference existing character
"leadership": "CHAR_watcher_commander_01"

// Character must be affiliated with that faction
"faction_affiliation": "watcher"
```

## Automated Validation Checks

### Required Validations
1. **ID Uniqueness**: No duplicate IDs within each category
2. **Reference Resolution**: All referenced IDs must exist
3. **Relationship Symmetry**: Bidirectional relationships must match
4. **Territory Consistency**: Sector control claims must align
5. **Template Compliance**: All entities must follow template structure

### Validation Tools
```bash
# Check JSON syntax for all lore files
find lore/ -name "*.json" -exec python3 -m json.tool {} \;

# Future: Automated cross-reference checker
# python3 validate_lore_references.py

# Future: Relationship symmetry checker  
# python3 check_faction_relations.py
```

## Common Issues and Solutions

### Issue: Orphaned References
**Problem**: References to deleted or renamed entities
**Solution**: Update all references when changing IDs

### Issue: Asymmetric Relations
**Problem**: Faction A lists B as ally, but B lists A as neutral
**Solution**: Ensure relationship updates are applied to both parties

### Issue: Territory Conflicts  
**Problem**: Multiple factions claim control of same sector
**Solution**: Use contested_sectors field or resolve through lore updates

## Best Practices

### 1. Consistent Naming
- Use descriptive, stable IDs that won't need frequent changes
- Follow established naming conventions strictly
- Avoid abbreviations that might be unclear

### 2. Reference Documentation
- Comment complex references in meta sections
- Document reason for relationship changes
- Track reference updates in commit messages

### 3. Incremental Validation
- Validate references after each entity creation/modification
- Test cross-references before committing changes
- Use examples as validation baselines

## Example Cross-Reference Chain

```
Sector A5 (Central Command District)
├─ Controlled by: watcher (faction)
├─ Leader: CHAR_watcher_commander_01 (character)
├─ Connected to: B5, A4, A6 (adjacent sectors)
└─ Relations: REL_watcher_merchants (faction relation)

Character CHAR_watcher_commander_01
├─ Faction: watcher
├─ Location: A5
├─ Allies: CHAR_merchant_liaison
└─ Enemies: CHAR_shadow_infiltrator

Faction watcher  
├─ Leader: CHAR_watcher_commander_01
├─ Territory: A5, B5 (primary sectors)
├─ Allies: merchants (faction)
└─ Relations: REL_watcher_merchants
```

## Implementation Notes

This validation system follows the existing project guidelines in `RULESET.md` and integrates with the AI behavior rules in `gpt_behavior.json`. Regular validation ensures the lore system remains consistent and machine-readable for AI management.

---

**Future Enhancements:**
- Automated validation scripts
- Real-time reference checking
- Visual relationship mapping
- Conflict detection algorithms