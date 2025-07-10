# Prompt Examples for Metro-AI-RPG

## Quick Reference Prompts

### 1. Basic Faction Query
```
Load factions_core.json. What is the military strength of Metro-Garde (f01)?
Expected: 8
```

### 2. Relationship Check
```
Using factions_core.json, determine the relationship between Die Schatten (f02) and Die Wächter (f04).
Expected: -2 (hostile)
```

### 3. Territory Control
```
Which faction controls territory A2? Check factions_core.json.
Expected: Both f01 (Metro-Garde) and f03 (Händlergilde) - potential conflict zone
```

## Storytelling Prompts

### 4. Rich Faction Description
```
Load factions_core.json and factions_narrative.json. Create a detailed description of Metro-Garde (f01) including their culture and objectives.

Expected output should include:
- Mechanical stats (strength: 8, territories: A1, A2, B1)
- Cultural elements (motto: "Ordnung durch Stärke")
- Narrative objectives and founding story
```

### 5. Diplomatic Encounter
```
Load both core mechanics and narrative data. Generate a dialogue between representatives of Händlergilde (f03) and Die Wächter (f04). They are allies (+1 relationship).

Should reference:
- Their positive relationship (+1)
- Shared interests in stability
- Merchant guild's economic power (9) vs Wächter's security focus
```

## Combat Resolution Prompts

### 6. Simple Combat
```
Using only factions_core.json, resolve combat between Metro-Garde (f01) and Die Schatten (f02).

Process:
1. f01 military_strength: 8
2. f02 military_strength: 4  
3. f01 wins (8 > 4)
```

### 7. Territory Dispute
```
Load factions_core.json. Analyze potential conflict in territory A2 (controlled by both f01 and f03).

Expected analysis:
- f01: military_strength 8, current relations with f03: 0 (neutral)
- f03: military_strength 3, but economic_power 9
- Likely outcome: Economic agreement rather than military conflict
```

## Data Validation Prompts

### 8. Relationship Consistency
```
Load factions_core.json. Verify relationship symmetry:
- f01 → f02: Check if f02 → f01 matches
- Report any asymmetric relationships
```

### 9. Territory Coverage
```
Using factions_core.json, list all controlled territories and identify:
- Overlapping territories (potential conflicts)
- Uncontrolled territories (expansion opportunities)
```

## Advanced Integration Prompts

### 10. Dynamic Storytelling
```
Context: Player is negotiating between f02 (Die Schatten) and f04 (Die Wächter)
Load: factions_core.json + factions_narrative.json

Generate negotiation scene considering:
- Their hostile relationship (-2)
- Conflicting objectives (criminal vs law enforcement)
- Player's potential influence on the outcome
```

### 11. Economic Simulation
```
Load factions_core.json. Model trade relationships based on economic_power:
- f03 (Händlergilde): 9 - primary trader
- f02 (Die Schatten): 7 - black market
- f01 (Metro-Garde): 6 - military contracts
- f04 (Die Wächter): 4 - limited trade

Calculate potential trade volumes and dependencies.
```

## Token Efficiency Examples

### 12. Efficient Query Pattern
```
// Step 1: Load minimal data for quick check
Load: factions_core.json (500 tokens)
Query: "Is f01 stronger than f02?"
Answer: Yes (8 > 4)

// Step 2: Only load lore if detailed response needed
If user asks "Why is Metro-Garde stronger?"
Then load: factions_narrative.json (+700 tokens)
Provide detailed answer about military background and organization
```

### 13. Context Switching
```
Context: Combat → Diplomacy
Current: factions_core.json loaded (combat mechanics)
Switch to: factions_core.json + factions_narrative.json (diplomacy needs culture/objectives)

Prompt: "After the battle, how would f01 approach peace negotiations with f02?"
```

## Error Handling Prompts

### 14. Invalid ID Reference
```
Load factions_core.json. User asks about faction "f99".
Response: "Faction f99 not found. Available factions: f01, f02, f03, f04"
```

### 15. Missing Data Recovery
```
If factions_narrative.json fails to load:
Fallback to factions_core.json with note: "Limited to mechanical data only"
Still provide functional response with available information
```

## Performance Testing

### 16. Token Count Verification
```
Measure actual token usage:
- factions_core.json only: ~500 tokens
- factions_core.json + factions_narrative.json: ~1200 tokens
- Verify against estimates in loading_config.json
```

### 17. Response Time Optimization
```
Time different loading strategies:
1. Load all data at once
2. Load core first, add lore on demand
3. Cache frequently accessed data

Compare response quality vs token efficiency.
```