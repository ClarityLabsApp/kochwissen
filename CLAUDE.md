# Kochwissen – Arbeitsanleitung für Claude

Kochwissen ist eine visuelle Bibliothek, die erklärt, **warum** Kochen und Backen funktionieren. Kein Rezeptbuch: Wer die Vorgänge versteht, kocht freier. Besitzer: Phil (Luzern). Sprache der Inhalte: Deutsch.

Lies vor jeder Arbeit auch **`DESIGN.md`** (Bildsprache, Farben, Vorlagen). Was dort steht, gilt.

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| `content/schema.json` | JSON-Schema für jeden Eintrag |
| `content/master-list.json` | Alle geplanten Einträge mit Typ, Links, Synonymen (Gerüst des Buchs) |
| `content/entries/<id>.json` | Ausgeschriebene Einträge, eine Datei pro Eintrag, Dateiname = id |
| `scripts/validate.mjs` | Prüft Schema, Verknüpfungen, Diagnosebäume, Glossar. Läuft vor jedem Build |
| `lib/content.ts` | Lädt Inhalte, zerlegt Glossar-Markierungen |
| `app/` | Next.js App Router: Bibliothek `/`, Eintrag `/eintrag/[id]` |
| `components/` | Library (Suche), Diagnosis, Term (Glossar-Popup), RichText |
| `public/prototypen/` | Die drei interaktiven HTML-Prototypen (Maillard, Gluten, Steak grau) |

Befehle: `npm run dev` · `npm run validate` · `npm run build`

## Eintragstypen

`prozess` (was passiert) · `ziel` (was will ich erreichen) · `technik` (welcher Handgriff) · `symptom` (was ist schiefgelaufen) · `zutat` (was tut eine Zutat) · `stellschraube` (woran drehe ich) · `welt` (Lebensmittel-Welt) · `begriff` (Glossar).

Drei Einstiege müssen immer funktionieren: vom Problem (Symptom), vom Ziel („Wie werden Wedges knuspriger?“) und vom Prinzip (Prozess). Darum: **jeder Eintrag verlinkt in alle Richtungen**, die Sinn ergeben.

## Schreibleitfaden

Gilt für jeden Text in einem Eintrag.

1. **Erster Satz trifft den Kern.** `kurz` ist ein einziger Satz, verständlich ohne Vorwissen.
2. **Alltagssprache.** Sätze unter 25 Wörtern. Fachwort nur in Klammern hinter dem Alltagswort: „Eiweiß verändert sich (Denaturierung)“.
3. **Jeder Eintrag hat ein `bild_im_kopf`.** Eine Analogie aus dem Alltag, die man sich merken kann (Lagerfeuer mit nassem Holz, Kaugummi-Netz, Mörtel zwischen Ziegeln). Keine Analogie zweimal verwenden.
4. **Was passiert → warum wichtig → woran drehen.** In dieser Reihenfolge denken.
5. **Faustregeln sind handfest.** Etwas, das man morgen in der Küche anders macht. Höchstens fünf.
6. **Zahlen nur, wenn sie stimmen.** Temperaturen und Mengen mit Quelle, sonst als Richtwert kennzeichnen.
7. **Fachbegriffe markieren.** Jedes Wort, das ein Hobbykoch nicht sicher kennt, beim ersten Vorkommen als `[[id]]` oder `[[id|Anzeigetext]]`. Fehlt der Begriff, einen `begriff`-Eintrag anlegen (ein Satz in `kurz`). Beispiel: `[[arosieren|Arosieren]]`.
8. **Mythen nur, wenn sie wirklich verbreitet sind.** Behauptung, dann die Richtigstellung in einem Satz.
9. **Schweizer Küche ist willkommen** (Ruchmehl, HOLL-Rapsöl, Bratbutter), Text bleibt Hochdeutsch mit ß.
10. **Kein Werbeton.** Keine Ausrufezeichen, keine Emojis, kein „ganz einfach“, kein „Geheimtipp“.

Vorbild für Ton und Tiefe: die 20 Einträge des Pilot-Batches (Kartoffeln & Knusprig) in `content/entries/`.

## Fakten und Quellen

- Jeder Eintrag hat mindestens eine Quelle in `quellen`. Bevorzugt: Harold McGee *On Food and Cooking*, Fachartikel, seriöse Kochwissenschaft (Serious Eats, America's Test Kitchen), Hersteller- und Verbandsseiten.
- Was nur aus allgemeinem Wissen stammt und nicht nachgeschlagen wurde, wird beim Review-Status als `entwurf` belassen und in der Zusammenfassung des Batches genannt.
- `status`: `geplant` (nur Masterliste) → `entwurf` (geschrieben) → `geprueft` (von Phil abgenommen). Nie selbst auf `geprueft` setzen.

## Arbeitsablauf für einen Batch

1. Einträge aus der Masterliste wählen, die zusammengehören (eine Welt oder ein Ziel, 15–25 Stück).
2. Für Zahlen und Behauptungen Quellen nachschlagen.
3. Pro Eintrag `content/entries/<id>.json` schreiben. Neue Begriffe als `begriff`-Einträge.
4. `npm run validate` muss fehlerfrei laufen. Erst dann committen.
5. Kurz zusammenfassen: welche Einträge, welche Aussagen unsicher, welche neuen Einträge der Masterliste fehlen.

Neue Einträge, die beim Schreiben auffallen, in `content/master-list.json` ergänzen (mit Typ, Links, Synonymen) statt sie wegzulassen.

## Grafiken

Grafiken kommen **immer aus Vorlagen** (`visual.vorlage` plus `params`), nie als Einzelbild pro Eintrag. Siehe `DESIGN.md`, Abschnitt 6. Die drei Prototypen in `public/prototypen/` sind die Referenz für Prozess-Simulation und Pfannentest.

## Grafik-Vorlagen (Stand)

In `components/visuals/`, ausgewählt in `Visual.tsx`:
- `TempScale` – Temperaturskala aus `visual.params.skala` / `schwellen_c` / `fette` (`[{c, name}]`)
- `StepFlow` – Ablauf für alle Einträge mit `schritte`
- `PanTest` – Symptome mit `vorlage: pfannentest`, `params.variante`: pfanne | backblech | fritteuse
- `DotNet` – Ziele (Hebel ↔ Techniken) und Zutaten (Rolle ↔ Vorgang)
- `Spectrum` – Skala für Stellschrauben und Anthocyane (`params.links`, `mitte`, `rechts`)
- `ParticleSim` – Canvas-Simulationen pro Prozess (emulsion, osmose, pektin-abbau, reduktion, hefegaerung, chemische-lockerung, waermeleitung, schaumbildung, diffusion, zucker-kristallisation, leidenfrost, gelbildung-pektin, chlorophyll-farbe, eiweiss-denaturierung). Neue Presets dort anlegen und in `SIMS` in `Visual.tsx` eintragen
- Prototypen in `public/prototypen/` (Maillard, Gluten, Steak grau) werden per iframe eingebettet

## Offene Aufgaben

- [ ] Weitere Simulationen: Glutenbildung als Komponente, Eiweiß-Denaturierung, Schaumbildung, Karamellisierung
- [ ] Maillard und Gluten-Prototyp als echte React-Komponenten portieren (statt iframe)
- [x] Alle 197 Einträge der Masterliste als Entwurf geschrieben (1. November 2026)
- [ ] Review durch Phil: Status von `entwurf` auf `geprueft`
- [ ] Masterliste erweitern (neue Gerichte, Techniken, Begriffe)
- [ ] Semantische Suche (z. B. Supabase pgvector), aktuelle Wortsuche ersetzen
- [ ] Aquarell-Illustrationen erzeugen: `OPENAI_API_KEY=… npm run illustrationen -- --test`, dann ohne `--test`. Motive in `visual.illustration` (Welten und Zutaten, 45 Stück), Ausgabe `public/illustrationen/<id>.png`, Anzeige automatisch im Seitenkopf
- [ ] Prüfung für unmarkierte Fachbegriffe im Validator
