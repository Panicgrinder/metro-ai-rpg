# Lore Development To-Do Liste

*Aufgaben und Fortschrittsverfolgung für die Entwicklung der Metro-AI-RPG Lore und Storyline*

## ✅ Abgeschlossene Aufgaben

- [x] Grundstruktur für Lore-Einträge entworfen
  - [x] Markdown-Template für Fließtext-Lore erstellt (`00_intro.md`)
  - [x] JSON-Templates für maschinenlesbare Lore-Objekte erstellt
- [x] Template-Verzeichnis `lore/templates/` angelegt
- [x] JSON-Templates erstellt:
  - [x] `faction.template.json` - Template für Fraktionen
  - [x] `character.template.json` - Template für wichtige Charaktere
  - [x] `faction_relation.template.json` - Template für Fraktionsbeziehungen  
  - [x] `sector.template.json` - Template für Sektoraufteilung (10x10 Grid)
- [x] Entstehungsgeschichte dokumentiert (`00_intro.md`)
  - [x] Die Entstehung der Metro-Welt
  - [x] Entstehung der ersten Fraktionen
  - [x] Übergang zum aktuellen Stand
- [x] To-Do-Liste als `TODO.md` erstellt

## 🚧 In Bearbeitung

- [ ] Aktualisierung des `lore.json` Index-Files
- [ ] Integration in `master_index.json`
- [ ] Validierung der Template-Konsistenz mit bestehendem System

## 📋 Noch zu erledigende Aufgaben

### Hohe Priorität

- [ ] **Fraktions-Details ausarbeiten:**
  - [ ] Detaillierte Hintergrundgeschichten für bestehende Fraktionen
  - [ ] Führungspersönlichkeiten für jede Fraktion definieren
  - [ ] Spezifische Territorien und Einflusszonen festlegen
  - [ ] Wirtschaftliche und militärische Stärken dokumentieren

- [ ] **Sektor-System implementieren:**
  - [ ] 10x10 Grid-System vollständig definieren (A1-J10)
  - [ ] Wichtige Sektoren mit Details ausstatten
  - [ ] Ressourcenverteilung über das Grid planen
  - [ ] Verbindungen zwischen Sektoren dokumentieren

- [ ] **Charakterentwicklung:**
  - [ ] Fraktionsführer für jede Hauptfraktion erstellen
  - [ ] Wichtige NPCs für Handlungsverläufe definieren
  - [ ] Beziehungsnetze zwischen Charakteren aufbauen

### Mittlere Priorität

- [ ] **Erweiterte Lore-Inhalte:**
  - [ ] Detaillierte Geschichte der ersten Jahre nach dem Kollaps
  - [ ] Technologische Entwicklungen im Metro-System
  - [ ] Kulturelle Entwicklungen und Traditionen
  - [ ] Religiöse oder philosophische Bewegungen

- [ ] **Fraktionsbeziehungen:**
  - [ ] Diplomatische Geschichte zwischen Fraktionen
  - [ ] Handelsbeziehungen und Wirtschaftsverträge
  - [ ] Militärische Allianzen und Konflikte
  - [ ] Aktuelle Spannungen und Potentiale für Konflikte

- [ ] **Weltbau-Details:**
  - [ ] Spezielle Orte und Sehenswürdigkeiten
  - [ ] Geheimnisvolle oder gefährliche Bereiche
  - [ ] Wichtige Infrastruktur und deren Kontrolle
  - [ ] Handelsrouten und deren Sicherheit

### Niedrige Priorität

- [ ] **Narrative Struktur:**
  - [ ] Aufbau von Haupthandlungsbögen
  - [ ] Nebenquests und lokale Geschichten
  - [ ] Zufällige Ereignisse und deren Auswirkungen
  - [ ] Langzeit-Storylines für Fraktionsentwicklung

- [ ] **Technische Implementierung:**
  - [ ] Automatische Validierung von Lore-Konsistenz
  - [ ] Tools für procedural content generation
  - [ ] KI-Integration für dynamische Storytelling
  - [ ] Cross-Reference-System für komplexe Beziehungen

## 🎯 Spezifische nächste Schritte

1. **Sofort (nächste Session):**
   - `lore.json` Index-File aktualisieren
   - `master_index.json` um Lore-Bereich erweitern
   - Template-Konsistenz mit bestehendem System validieren

2. **Diese Woche:**
   - Erste Fraktionsführer mit dem Character-Template erstellen
   - Wichtigste Sektoren (A1-A3, E5, J7) detailliert ausarbeiten
   - Beziehungsmatrix zwischen Hauptfraktionen erstellen

3. **Nächste Woche:**
   - Erweiterte Hintergrundgeschichten für jede Fraktion
   - Vollständige Sektoraufteilung des 10x10 Grids
   - Erste Handlungsbögen und Konfliktpotentiale definieren

## 📝 Entwicklungsrichtlinien

### Für neue Lore-Inhalte beachten:

- **Konsistenz**: Alle neuen Inhalte müssen mit der Grundgeschichte und bestehenden Fraktionen konsistent sein
- **Maschinenlesbarkeit**: JSON-Strukturen verwenden wo möglich für KI-Integration
- **Modularität**: Inhalte so gestalten, dass sie unabhängig editiert und erweitert werden können
- **Template-Konformität**: Neue Einträge müssen den vorgegebenen Template-Strukturen folgen
- **Cross-Referencing**: IDs und Referenzen zwischen verschiedenen Lore-Elementen konsequent verwenden

### Sprache und Stil:

- **Dokumentation**: Englisch für alle System-Files und Templates
- **Fließtext-Lore**: Englisch für narrative Inhalte
- **Entwicklungs-Notizen**: Deutsch für interne To-Dos und Entwicklungshinweise
- **Kommentare**: Zweisprachig wo hilfreich für Verständnis

## 🔄 Regelmäßige Reviews

- **Wöchentlich**: Fortschritt auf dieser To-Do-Liste überprüfen
- **Monatlich**: Konsistenz der gesamten Lore-Struktur validieren
- **Bei größeren Änderungen**: Cross-Reference-Checks mit anderen System-Bereichen

---

**Last Updated**: Initial creation  
**Next Review**: Nach Implementierung der Grundstruktur  
**Verantwortlich**: AI-System mit menschlicher Überwachung