# Repository Ruleset für Zusammenarbeit mit GitHub Copilot und KI-Tools

## 1. Ziele
- Dieses Repository dient der Entwicklung eines KI-basierten Rollenspiels, das von einer AI (z.B. GPT) geführt wird.
- Ziel ist es, gemeinsam zu lernen und offen für neue Ansätze in Python und AI-Management zu bleiben.

## 2. Coding Guidelines
- Schreibe Code möglichst klar, gut kommentiert und maschinenlesbar.
- Halte dich an die offiziellen [PEP8 Python Coding Standards](https://www.python.org/dev/peps/pep-0008/).
- Nutze docstrings für Funktionen und Klassen.
- Schreibe Funktionen kurz, modular und mit klaren Verantwortlichkeiten.
- Vermeide redundanten Code und setze stattdessen auf Wiederverwendbarkeit.

## 3. Zusammenarbeit mit Copilot/KI
- Vorschläge von Copilot und anderen KI-Tools sind willkommen, aber immer kritisch zu prüfen.
- Übernehme Code-Snippets von Copilot nur, wenn du sie verstehst und sie zur Code-Qualität beitragen.
- Bei Unsicherheiten nachfragen, recherchieren oder einen Issue eröffnen.
- Erkläre wichtige Entscheidungen im Pull Request oder als Kommentar im Code.
- Nutze Copilot als Lernhilfe, nicht als alleinige Quelle.

## 4. Rollenspiel- und KI-Logik
- KI-gesteuerte Logik und Regelwerke sind transparent zu dokumentieren (`/docs/`-Ordner).
- Änderungen an zentralen Spielmechaniken müssen im Team diskutiert werden (Issue oder Pull Request).
- Experimentiere, aber dokumentiere Experimente klar als solche (z.B. im Branch-Namen oder Kommentar).

### 4.1 Standardisierte ID-Vergabe
- **Einheitliches Schema**: Alle Entitäten verwenden ein standardisiertes ID-Format für maschinelle Verarbeitung.
- **Format**: `[prefix][nummer]` mit 2-4 Zeichen Präfix + fortlaufende Nummer (z.B. `f01`, `a01`, `i01`).
- **Präfixe nach Entitätstyp**:
  - Fraktionen: `f##` (f01, f02, f03...)
  - Akteure/NPCs: `a##` (a01, a02, a03...)
  - Gegenstände: `i##` (i01, i02, i03...)
  - Missionen: `m##` (m01, m02, m03...)
  - Events: `e##` (e01, e02, e03...)
  - Orte: `l##` (l01, l02, l03...)
  - Monster: `mon##` (mon01, mon02...)
  - Quests: `q##` (q01, q02, q03...)
  - Ressourcen: `r##` (r01, r02, r03...)
  - Sektoren: `s##` (s01, s02, s03...)
- **Feldnamen**: Hauptfeld immer `"id"`, Querverweise als `"[entitätstyp]_id"`.
- **Trennung von Mechanik und Lore**: Mechanikdateien in Hauptverzeichnissen, Lore-Dateien unter `lore/[typ]/`.

### 4.2 Referenz- und Redundanzprüfung
- **Regelmäßige Validierung**: Alle Referenzen zwischen Dateien und IDs müssen regelmäßig auf Gültigkeit und Eindeutigkeit geprüft werden.
- **Dokumentationspflicht**: Jede Prüfung von Querverweisen und Redundanzen ist zu dokumentieren und zu protokollieren.
- **Automatische Kontrollen**: Das System führt automatische Konsistenzprüfungen durch (siehe `gpt_behavior.json`).
- **Manuelle Überprüfung**: Zusätzlich zu automatischen Checks sind manuelle Validierungen in regelmäßigen Abständen durchzuführen.
- **Korrekturpflicht**: Identifizierte Inkonsistenzen müssen zeitnah behoben und dokumentiert werden.

## 5. Issues & Pull Requests
- Jeder neue Vorschlag oder Fehler wird als Issue angelegt.
- Pull Requests benötigen mindestens eine Überprüfung durch eine zweite Person (Review).
- Beschreibe im PR-Titel/Kommentar klar, was geändert wurde und warum.
- Füge relevante Links, Screenshots oder Beispielcode hinzu.

## 6. Dokumentation
- Änderungen an der Spiel- oder KI-Logik sind zeitnah in der Dokumentation zu ergänzen (`README.md`, `/docs/`).
- Halte die Dokumentation so einfach, dass auch Anfänger sie verstehen.

## 7. Kommunikation & Feedback
- Fragen und Vorschläge sind immer willkommen.
- Konstruktives Feedback ist erwünscht – respektvoller Umgang ist Pflicht.
- Bei Unklarheiten lieber nachfragen, auch bei scheinbar „dummen“ Fragen.

---

**Letzte Aktualisierung:** 2025-07-10  
**Erstellt von:** Panicgrinder & Copilot
