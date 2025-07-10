# Metro-AI-RPG ID Schema Reference

## Übersicht

Dieses Dokument definiert das standardisierte ID-System für alle Entitäten im Metro-AI-RPG Repository. Das System gewährleistet maschinenlesbare IDs für KI-gestützte Automatisierung und klare Strukturierung.

## ID-Format Standards

### Grundprinzipien
- **Kurz und maschinenlesbar**: 2-4 Zeichen Präfix + fortlaufende Nummer
- **Konsistentes Format**: Kleinbuchstaben-Präfix + nullaufgefüllte Nummern  
- **Skalierbar**: Unterstützt 999+ Entitäten pro Typ
- **Menschenlesbar**: Präfix zeigt Entitätstyp an

### Entitätstyp-Mapping

| Entitätstyp | Präfix | Format | Beispiel | Bereich |
|-------------|--------|--------|----------|---------|
| **Fraktionen** | `f` | f## | f01, f02, f03 | f01-f999 |
| **Akteure/NPCs** | `a` | a## | a01, a02, a03 | a01-a999 |
| **Gegenstände** | `i` | i## | i01, i02, i03 | i01-i999 |
| **Missionen** | `m` | m## | m01, m02, m03 | m01-m999 |
| **Events** | `e` | e## | e01, e02, e03 | e01-e999 |
| **Orte** | `l` | l## | l01, l02, l03 | l01-l999 |
| **Monster** | `mon` | mon## | mon01, mon02 | mon01-mon99 |
| **Quests** | `q` | q## | q01, q02, q03 | q01-q999 |
| **Ressourcen** | `r` | r## | r01, r02, r03 | r01-r999 |
| **Sektoren** | `s` | s## | s01, s02, s03 | s01-s999 |

### Spezialfälle
- **Spielercharakter**: `player` (fest)
- **System-Entitäten**: `sys_` Präfix für systemgenerierte Inhalte
- **Templates**: `.template.json` Suffix für Template-Dateien

## Feldnamen-Konventionen

### Primäre Identifier
```json
{
  "id": "f01"
}
```

### Querverweise  
```json
{
  "faction_id": "f01",
  "location_id": "l01",
  "actor_id": "a01"
}
```

## Verzeichnisstruktur

### Mechanik-Dateien (Hauptverzeichnisse)
```
factions/
├── f01.json          # Metro-Garde Mechanik
├── f02.json          # Die Schatten Mechanik
└── f03.json          # Händlergilde Mechanik

actors/
├── a01.template.json
└── a02.json

items/
├── i01.template.json
└── i02.json
```

### Lore-Dateien (lore/ Unterverzeichnisse)
```
lore/
├── factions/
│   ├── f01_lore.json # Metro-Garde Lore
│   ├── f02_lore.json # Die Schatten Lore
│   └── f03_lore.json # Händlergilde Lore
├── actors/
│   └── a01_lore.json
└── items/
    └── i01_lore.json
```

## Aktuelle Implementierung

### ✅ Umgesetzt
- **Fraktionen**: f01-f04 mit separaten Lore-Dateien
- **Template-Dateien**: Für alle Hauptentitätstypen erstellt
- **RULESET.md**: Aktualisiert mit neuen Standards
- **Verzeichnisstruktur**: lore/ Unterordner erstellt

### 🔄 In Arbeit  
- Migration bestehender Dateien auf neues Schema
- Aktualisierung aller Querverweise
- Validierung der Konsistenz

## Migrationsrichtlinien

### Datei-Umbenennung
```bash
# Alt → Neu
faction_shadows.json → f02.json
EVT-001.json → e01.template.json  
LOC-3001.json → l01.template.json
```

### Cross-Reference Updates
```json
// Alt
{
  "relations": {
    "faction_haendler": "neutral"
  }
}

// Neu
{
  "relations": {
    "f03": "neutral"
  }
}
```

## Validierung

### JSON-Format
```bash
# Alle JSON-Dateien validieren
find . -name "*.json" -exec python3 -m json.tool {} \;
```

### ID-Eindeutigkeit
- Keine doppelten IDs innerhalb eines Entitätstyps
- Alle Querverweise verweisen auf existierende IDs
- Template-Dateien enthalten `{{placeholder}}` für variable Werte

## Wartung

- **Neue Entitäten**: Fortlaufende Nummerierung verwenden
- **Löschungen**: IDs nicht wiederverwenden
- **Änderungen**: Alle Querverweise aktualisieren
- **Dokumentation**: Dieses Dokument bei Schema-Änderungen aktualisieren

---

**Letzte Aktualisierung**: 2025-07-10  
**Version**: 1.0  
**Autor**: AI-System