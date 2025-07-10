# Metro-AI-RPG Quick Reference

## 🚀 Fast Start for AI Systems

### Essential Files to Load
```
ALWAYS LOAD: data/mechanics/factions_core.json (361 tokens)
LOAD WHEN NEEDED: data/lore/factions_narrative.json (+828 tokens)
```

### Faction IDs
- `f01` - Metro-Garde (Military: 8, Economic: 6)
- `f02` - Die Schatten (Military: 4, Economic: 7) 
- `f03` - Händlergilde (Military: 3, Economic: 9)
- `f04` - Die Wächter (Military: 7, Economic: 4)

### Relationship Scale
- `+2` = Allied, `+1` = Friendly, `0` = Neutral, `-1` = Hostile, `-2` = Enemy

### Quick Queries

#### Combat Resolution
```javascript
const f01_str = mechanics.factions.f01.stats.military_strength; // 8
const f02_str = mechanics.factions.f02.stats.military_strength; // 4
// f01 wins (8 > 4)
```

#### Relationship Check
```javascript
const attitude = mechanics.factions.f01.relations.f02; // -1 (hostile)
```

#### Territory Control
```javascript
const territories = mechanics.factions.f01.territory; // ["A1", "A2", "B1"]
```

### Context Loading

| Context | Load | Tokens | Use For |
|---------|------|--------|---------|
| Combat | mechanics only | 361 | Battle resolution, stat checks |
| Trading | mechanics only | 361 | Economic calculations, relations |
| Dialogue | mechanics + lore | 1189 | Rich NPC interactions |
| Storytelling | mechanics + lore | 1189 | Immersive descriptions |

### Common Patterns

#### Efficient Query
```javascript
// Step 1: Quick mechanical check
if (mechanics.factions.f01.stats.military_strength > 6) {
  // Step 2: Add narrative only if needed
  const story = lore.lore_modules.f01_narrative;
  return `${mechanics.factions.f01.name} is powerful. ${story.detailed_description}`;
}
```

#### Relationship Narrative
```javascript
const relation_value = mechanics.factions.f01.relations.f02; // -1
const relation_story = lore.lore_modules.f01_narrative.relationships.f02;
// Provides both mechanical and narrative context
```

## 📁 File Locations

### Core Data (Always Load)
- `data/mechanics/factions_core.json` - Essential game mechanics

### Rich Content (Load on Demand)  
- `data/lore/factions_narrative.json` - Detailed storytelling content

### Legacy (Compatibility)
- `factions/f01.json` to `factions/f04.json` - Individual mechanics
- `lore/factions/f01_lore.json` to `f04_lore.json` - Individual lore

## 🔧 Validation
```bash
# Check data integrity
python3 system/todo/modular_validator.py

# General repository health  
python3 system/todo/repo_rule_checker.py
```

## 💡 Best Practices
1. **Start with mechanics** - Always load core data first
2. **Add lore conditionally** - Only when rich description needed
3. **Use numerical relations** - More efficient than text descriptions
4. **Validate cross-references** - Ensure mechanics/lore pairs exist
5. **Monitor token usage** - Aim for <400 tokens for basic operations

## 🎯 Example Usage

### Basic Combat
```
Load: mechanics only (361 tokens)
Query: f01 vs f02 military strength
Result: 8 vs 4, f01 wins
```

### Rich Diplomacy Scene
```
Load: mechanics + lore (1189 tokens)  
Context: f03 (Händlergilde) negotiating with f04 (Die Wächter)
Relation: +1 (allied)
Culture: Trade-focused vs Security-focused
Result: Detailed diplomatic interaction
```

This optimized structure provides **69.6% token efficiency** for basic operations while maintaining full narrative richness when needed.