# Metro-AI-RPG

AI-powered role-playing game set in a post-apocalyptic Metro setting, managed and guided by GPT/AI systems.

## Overview

Metro-AI-RPG is a modular, machine-readable system designed for AI-driven role-playing game management. The project creates a comprehensive framework where artificial intelligence can dynamically manage game worlds, characters, factions, and narrative progression in the atmospheric Metro universe.

## Goals

- Development of a modular, machine-readable system for AI-powered RPG management
- Creation of dynamic, evolving game worlds managed by AI game masters
- Establishment of consistent, cross-referenced data structures for complex narrative systems
- Implementation of robust template systems for expandable game content

## Project Structure

The repository is organized into the following main directories:

### Core Directories

- **`system/`** - Core engine files, AI behavior rules, metadata, and configuration
  - `gpt_behavior.json` - AI behavioral guidelines and system rules
  - `engine.json` - Core game engine configuration
  - `metadata.json` - System metadata and versioning
- **`actors/`** - Character definitions, NPCs, and actor-related data
- **`factions/`** - Faction systems, relationships, and organizational structures  
- **`world/`** - World geography, locations, sectors, and environmental data
  - `locations/` - Specific location definitions
  - `sectors.json` - Sector organization and relationships

### Additional Systems

- **`economy/`** - Economic systems, markets, and trade relationships
- **`items/`** - Item definitions, properties, and categorization
- **`crafting/`** - Crafting recipes and manufacturing systems
- **`missions/`** - Quest and mission templates
- **`events/`** - Dynamic event systems and triggers
- **`lore/`** - Background lore and narrative elements

### Template Architecture

This project employs a template-based approach for content management:

- **Templates are for development only** - Never include production game data in templates
- Templates serve as blueprints for creating game instances
- All templates are machine-readable and AI-manageable
- Runtime instances are created from templates for actual gameplay

### Cross-Reference and Consistency System

The system implements comprehensive cross-reference validation and redundancy checking:

- All file and ID references are automatically validated
- Consistency checks run on every system change
- See `gpt_behavior.json` and `RULESET.md` for detailed validation rules
- Automated logging and correction systems maintain data integrity

### Master Index

The `master_index.json` file provides a central registry of all system areas, their locations, indices, and current status.

## Important Notes

⚠️ **Template Data Warning**: Templates must never contain production game data. They are development blueprints only.

🔍 **Reference Validation**: All system modifications automatically trigger cross-reference and consistency validation (see `RULESET.md`).

🤖 **AI Management**: This system is designed to be managed by AI game masters with minimal human intervention during gameplay.

## Installation and Setup

### Requirements

- Python 3.8 or higher
- JSON-compatible text editor for data management
- Git for version control

### Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Panicgrinder/metro-ai-rpg.git
   cd metro-ai-rpg
   ```

2. **Installation**: No additional installation required - this is a data-driven system.

3. **Usage**: The system is designed for AI management. See `system/gpt_behavior.json` for AI behavioral guidelines.

4. **Setup validation**: Run the rule checker to validate system integrity:
   ```bash
   python system/todo/repo_rule_checker.py
   ```

## Contributing

### Beitrag leisten (German)

Wir freuen uns über Beiträge zu diesem Projekt! Bitte beachten Sie folgende Richtlinien:

- Lesen Sie die `RULESET.md` für detaillierte Entwicklungsrichtlinien
- Alle Systemdateien müssen auf Englisch verfasst werden
- Spieler-/Benutzerausgaben können auf Deutsch erfolgen
- Nutzen Sie GitHub Issues für Vorschläge und Fehlermeldungen
- Pull Requests benötigen mindestens eine Überprüfung
- Dokumentieren Sie Änderungen klar und verständlich

### Development Guidelines

- Follow the guidelines in `RULESET.md`
- Use the standardized ID schema defined in `docs/ID_SCHEMA.md`
- System files must be in English
- Maintain machine-readable JSON structure
- Ensure all references and IDs remain consistent
- Test cross-reference validation after changes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated**: 2025-07-10  
**Created by**: Panicgrinder