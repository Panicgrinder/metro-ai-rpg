# Template Usage Examples

This document shows how to use the lore templates to create actual game content.

## Example: Creating a Faction using faction.template.json

Here's how to transform the faction template into an actual faction entry:

### Template → Actual Data

```json
// Original template placeholder:
"faction_id": "{{faction_id}}"

// Becomes:
"faction_id": "tech_alliance"
```

### Complete Example: Tech Alliance Faction

```json
{
  "is_template": false,
  "faction_id": "tech_alliance",
  "name": "Technology Alliance",
  "description": "A coalition of engineers, scientists, and technicians dedicated to preserving and advancing technology in the Metro world.",
  "home_sectors": ["D4", "D5"],
  "relations": {
    "allies": ["merchants"],
    "enemies": ["shadows"],
    "neutral": ["watcher", "enlightened"]
  },
  "influence_zones": ["industrial", "research"],
  "leadership": "CHAR_tech_director_01",
  "faction_flags": ["technology", "research", "innovation"],
  "ideology": "technological_progress",
  "founding_date": "Metro Year 7",
  "military_strength": "medium",
  "economic_power": "high",
  "technology_level": "advanced",
  "population": "moderate",
  "specializations": ["engineering", "computer_systems", "power_management"],
  "territory_control": {
    "primary_sectors": ["D4", "D5"],
    "contested_sectors": ["C4"],
    "influence_sectors": ["E4", "D3", "C5"]
  },
  "resources": {
    "controlled_resources": ["advanced_electronics", "rare_metals"],
    "trade_goods": ["computer_parts", "power_cells", "technical_services"],
    "military_assets": ["automated_defenses", "surveillance_systems"]
  },
  "meta": {
    "created_by": "AI-System",
    "created_at": "2025-07-10T19:30:00+00:00",
    "version": "1.0",
    "template_notes": "Example faction created using faction.template.json"
  }
}
```

## Template Validation Checklist

When creating content from templates:

- [ ] Replace ALL {{placeholder}} values
- [ ] Set `"is_template": false` for actual content
- [ ] Use consistent ID naming conventions
- [ ] Ensure cross-references point to existing entities
- [ ] Update timestamps and meta information
- [ ] Validate JSON syntax

## ID Naming Conventions

- **Faction IDs**: `snake_case` (e.g., `tech_alliance`, `merchant_guild`)
- **Character IDs**: `CHAR_` prefix + descriptive name (e.g., `CHAR_tech_director_01`)
- **Sector IDs**: Grid format `A1`-`J10`
- **Relation IDs**: `REL_` prefix + faction combination (e.g., `REL_tech_merchants`)

---

*This document will be updated as more examples are created and conventions are established.*