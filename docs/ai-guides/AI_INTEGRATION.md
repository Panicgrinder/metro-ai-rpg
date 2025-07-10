# AI Integration Guide for Metro-AI-RPG

## Overview

This repository is specifically designed for AI-driven game management with optimized token efficiency and machine-readable data structures.

## Key Principles

### 1. Mechanics vs Lore Separation
- **Mechanics Files**: Contain only numerical data, IDs, and machine-readable game rules
- **Lore Files**: Contain narrative content, descriptions, and storytelling elements
- **Load Strategy**: Always load mechanics first, add lore only when needed

### 2. Modular Data Loading
Use the modular data system in `/data/` for token-efficient loading:

```json
// For basic faction checks
Load: data/mechanics/factions_core.json (500 tokens)

// For rich storytelling
Load: data/mechanics/factions_core.json + data/lore/factions_narrative.json (1200 tokens)
```

### 3. ID Schema Consistency
All entities use standardized IDs:
- Factions: `f01`, `f02`, `f03`, `f04`
- Actors: `a01`, `a02`, etc.
- Items: `i01`, `i02`, etc.
- Locations: `l01`, `l02`, etc.

## AI Usage Examples

### Example 1: Faction Combat Resolution
```javascript
// Load only core mechanics (efficient)
const factionData = loadModule("data/mechanics/factions_core.json");
const f01_strength = factionData.factions.f01.stats.military_strength; // 8
const f02_strength = factionData.factions.f02.stats.military_strength; // 4
// Result: f01 wins combat
```

### Example 2: Rich Storytelling
```javascript
// Load mechanics + narrative (when description needed)
const mechanics = loadModule("data/mechanics/factions_core.json");
const narrative = loadModule("data/lore/factions_narrative.json");

const faction = mechanics.factions.f01;
const story = narrative.lore_modules.f01_narrative;

// Generate rich description using both
const description = `${faction.name} (${story.motto}) controls territories ${faction.territory.join(", ")} with military strength ${faction.stats.military_strength}. ${story.detailed_description}`;
```

### Example 3: Relationship Checks
```javascript
// Quick relationship lookup (mechanics only)
const f01_relations = factionData.factions.f01.relations;
const attitude_to_f02 = f01_relations.f02; // -1 (hostile)

// Rich relationship context (with lore)
const relationship_context = narrative.lore_modules.f01_narrative.relationships?.f02;
// Provides detailed reasoning for the hostility
```

## Token Optimization Strategies

### 1. Context-Aware Loading
```javascript
// Game context determines what to load
switch(gameContext) {
  case "combat":
    load("data/mechanics/factions_core.json"); // 500 tokens
    break;
  case "dialogue":
    load("data/mechanics/factions_core.json", "data/lore/factions_narrative.json"); // 1200 tokens
    break;
}
```

### 2. Just-in-Time Lore Loading
```javascript
// Load mechanics first for all operations
const mechanics = loadModule("data/mechanics/factions_core.json");

// Only load lore when generating descriptions
if (needsDescription) {
  const lore = loadModule("data/lore/factions_narrative.json");
}
```

### 3. Selective Data Access
```javascript
// Access only needed faction data
const targetFaction = mechanics.factions[factionId];
const targetLore = lore.lore_modules[`${factionId}_narrative`];
```

## File Structure Reference

```
metro-ai-rpg/
├── data/
│   ├── mechanics/           # Core game mechanics (always load)
│   │   └── factions_core.json
│   ├── lore/               # Narrative content (load when needed)
│   │   └── factions_narrative.json
│   └── modules/            # Loading configurations
│       └── loading_config.json
├── factions/               # Legacy individual files (use data/ instead)
├── lore/                  # Legacy lore structure (use data/ instead)
└── docs/ai-guides/        # This documentation
```

## Best Practices for AI

1. **Always start with mechanics**: Load `data/mechanics/` files first
2. **Add lore conditionally**: Only load `data/lore/` when generating descriptions
3. **Use modular loading**: Refer to `data/modules/loading_config.json` for context-appropriate loading
4. **Respect the ID schema**: Use standardized IDs for all cross-references
5. **Validate relationships**: Check numerical relations (-2 to +2) in mechanics before adding narrative context

## Migration Notes

- Legacy files in `/factions/` and `/lore/factions/` still exist for compatibility
- New AI systems should prefer the modular `/data/` structure
- The rule checker validates both old and new structures