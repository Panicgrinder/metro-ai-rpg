# Metro-AI-RPG

An AI-powered role-playing game set in a post-apocalyptic Metro universe, guided and managed by GPT/AI systems.

## Project Goals

Development of a modular, machine-readable system for RPG management through AI. The system provides:

- Dynamic game world management through AI game masters
- Modular data structures for scalable content
- Consistent cross-referencing and validation systems
- Template-based approach for reproducible game instances

## Project Structure

### Main Directories

- **`/system/`** - Core game engine files, AI behavior rules, and system configuration
- **`/actors/`** - Character definitions, NPCs, and player entities
- **`/factions/`** - Political groups, organizations, and their relationships
- **`/world/`** - Locations, sectors, and geographical game world data
- **`/lore/`** - Background stories, history, and narrative content
- **`/economy/`** - Trading systems, resources, and economic mechanics
- **`/items/`** - Equipment, consumables, and item definitions
- **`/missions/`** - Quests, objectives, and storyline progressions

### Template Approach

This repository follows a strict template-based architecture:

- **No productive game data in templates** - Templates serve as blueprints only
- **Template immutability during gameplay** - Live game instances work with copies
- **Version-controlled templates** - All template changes are tracked and reviewed

## Cross-References and Consistency

All IDs and references within the system are:

- **Unique and sequential** - Managed automatically by the AI system
- **Regularly validated** - Consistency checks run on every change
- **Cross-referenced** - All relationships between entities are maintained
- **Logged** - Changes and validations are recorded (see `gpt_behavior.json` and `RULESET.md`)

The system implements automatic reference checking and redundancy prevention as defined in the project ruleset.

## Contributing

**For questions and contributions, please use Issues or Pull Requests.**

*Für Fragen und Beiträge bitte Issues oder Pull Requests nutzen. Alle Systemdateien werden auf Englisch verfasst, Beitragshinweise können auf Deutsch ergänzt werden.*

### Development Guidelines

- Follow the rules defined in `RULESET.md`
- System files must use English language
- Maintain modular and machine-readable code structure
- Document all changes affecting game mechanics

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.