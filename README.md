# Kochwissen

Eine visuelle Bibliothek, die erklärt, warum Kochen und Backen funktionieren: Prozesse, Ziele, Techniken, Symptome und Zutaten, verknüpft und sichtbar gemacht.

## Starten

```bash
npm install
npm run dev        # http://localhost:3000
npm run validate   # Inhalte prüfen
npm run build      # prüft Inhalte und baut die Seite
```

## Inhalte

- `content/master-list.json` – alle geplanten Einträge (Gerüst)
- `content/entries/` – ausgeschriebene Einträge, eine JSON-Datei pro Eintrag
- `content/schema.json` – Aufbau eines Eintrags

Arbeitsregeln und Schreibleitfaden: `CLAUDE.md`. Bildsprache: `DESIGN.md`.

## Deployment

Repository bei Vercel importieren, keine weiteren Einstellungen nötig.
