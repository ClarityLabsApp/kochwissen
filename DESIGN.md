# Kochwissen – DESIGN.md

Bildsprache und Bauregeln für alle Seiten der Kochwissen-Bibliothek. Jede neue Seite, jede Vorlage und jede Session hält sich an dieses Dokument. Abgeleitet aus den Prototypen *Maillard-Reaktion* (P-001), *Glutenbildung* (P-002) und *Steak wird grau statt braun* (S-001).

---

## 1. Haltung

Kochwissen ist ein altes Kochbuch, in dem jemand ein Labor eingerichtet hat.

- **Wärme wie ein Kochbuch:** Papier, Tinte, Geschichten, Vertrauen. Man liest gern darin.
- **Klarheit wie ein Laborinstrument:** Messwerte, Raster, Maßstäbe. Man versteht, was passiert.
- **Einfachheit wie eine Punktgrafik:** Jeder Stoff ist ein Punkt mit fester Farbe. Keine Formeln, keine Strukturformeln.

Drei Regeln, die über allem stehen:

1. **Verstehen vor Rezept.** Jede Seite beantwortet: Was passiert? Warum ist das wichtig? Woran kann ich drehen?
2. **Zeigen vor Erklären.** Was sich bewegen, verändern oder vergleichen lässt, wird interaktiv gezeigt, nicht beschrieben.
3. **Daten statt Einzelgrafiken.** Grafiken entstehen aus Vorlagen plus Parametern aus der Datenbank. Nie eine Grafik von Hand nur für einen Eintrag.

---

## 2. Farben

Eine einzige, warme Papierwelt. Kein Dark Mode (bewusste Entscheidung), Hintergrund und alle Farben sind immer explizit gesetzt.

### Grundfarben

| Token | Hex | Verwendung |
| --- | --- | --- |
| `--paper` | `#efe4cf` | Seitenhintergrund |
| `--paper-2` | `#f6eedd` | Flächen: Bühne, Karten, Messwerte |
| `--ink` | `#2b2118` | Text, aktive Zustände, starke Rahmen |
| `--sepia` | `#7a5a3a` | Beschriftungen, Nebentext, Labels |
| `--rule` | `#d5c3a1` | Linien, Raster, ruhige Rahmen |
| `--crust` | `#b4542a` | Akzent: Handlungsaufforderung, Zoom-Linse, Markierung, Mythos-Stempel |
| `--lab` | `#2f6f73` | Wissenschaft: Eiweiß, Messbalken, „bestanden“ |

**Regel:** `--crust` ist der einzige Akzent. Pro Bildschirm höchstens eine dominante Stelle in `--crust`.

### Punkt-Sprache

Jeder Stoff hat überall dieselbe Farbe. Auf Ebene 3 (Moleküle), in Legenden, in Praxis-Karten und Aromaprofilen.

| Stoff / Eigenschaft | Hex | Form |
| --- | --- | --- |
| Eiweiß-Baustein, Glutenin | `#2f6f73` | Punkt, mittel |
| Gliadin | `#7fb0ac` | Punkt, klein |
| Zucker | `#e0ad3a` | Punkt, mittel |
| Wasser | `#8fb8c9` | Punkt, klein, dunklerer Rand `#5f8fa3` |
| Fett, Butter | `#f0d27a` | Punkt, groß, Rand `#c9a24a` |
| Stärke | `#e6d3ae` | Ellipse, Rand `#b89a6a` |
| Salz | `#ffffff` | Punkt, klein, Rand Sepia |
| Aroma röstig | `#6b3a1e` | Punkt, variabel |
| Aroma nussig | `#b8873a` | Punkt, variabel |
| Aroma karamellig | `#d9822b` | Punkt, variabel |
| Aroma fleischig | `#8c2f2a` | Punkt, variabel |
| Aroma bitter, verbrannt | `#3a3633` | Punkt, variabel |

Neue Stoffe bekommen eine Farbe erst, wenn sie hier eingetragen sind.

### Lebensmittelfarben (Zustände)

Für gebratene und gebackene Oberflächen gibt es eine feste Bräunungsrampe. Zwischenwerte werden linear gemischt.

`roh #c46a6a → gar/grau #a39088 → goldbraun #c08a45 → braun #7a4523 → dunkel #3d2416 → verbrannt #1f1a17`

### Eintragstypen

| Typ | Farbe |
| --- | --- |
| Prozess | `#2f6f73` |
| Zutat | `#b8873a` |
| Stellschraube | `#7a5a3a` |
| Symptom | `#b4542a` |
| Ziel | `#6b3a1e` |
| Technik | `#8c2f2a` |
| Welt | `#3a3633` |

### Temperaturzonen (Thermometer, Skalen)

| Zone | Farbe |
| --- | --- |
| unter 100 °C (Wasser) | `#8fb8c9` |
| 100–140 °C | `#e0ad3a` |
| 140–190 °C (Bräunung) | `#b4542a` |
| über 190 °C (verbrennt) | `#3a3633` |

---

## 3. Typografie

| Rolle | Schrift | Verwendung |
| --- | --- | --- |
| Display | **Fraunces** (600, kursiv 400) | Titel, Abschnitte, Statuszeile, „Bild im Kopf“ |
| Text | **Newsreader** (400, 500) | Fließtext |
| Labor | **JetBrains Mono** (400, 600) | Labels, Messwerte, HUD, Chips, Buttons |

Fallbacks: `Georgia, serif` und `ui-monospace, Menlo, monospace`.

**Größen:** Titel `clamp(40px, 8vw, 68px)` · Abschnitt 26px · Karten-Titel 21px · Fließtext 18px (Handy 17px) · Lead 21px · Labels 11px, Großbuchstaben, Sperrung `.08em`.

**Titel-Regel:** Ein Wort im Titel kursiv in `--crust` setzen, nämlich das Wort, um das es geht (*Reaktion*, *bildung*). Bei Symptomen: Fehlerwort grau kursiv, Zielwort fett in `--crust` („wird *grau* statt **braun**“).

Zahlen immer mit `font-variant-numeric: tabular-nums`. Fließtext maximal ca. 62 Zeichen breit.

---

## 4. Layout

- Eine Spalte, maximal **820px** breit. Seitenrand `max(16px, env(safe-area-inset-left))`.
- Abstände über `gap` in Flex/Grid, nicht über Margins. Hauptrhythmus 28px zwischen Blöcken.
- Hintergrund: Papier mit feinem Punktraster (`radial-gradient`, 6px, Sepia 6 %).
- Kacheln aneinander statt Karten mit Schatten: Gitter mit `gap: 1px` auf `--rule`-Hintergrund. **Keine Schatten, keine großen Rundungen** (Radius 2px, Chips voll rund).
- Handy zuerst denken: Bühne wird unter 640px quadratisch, Messwerte gehen auf 2–3 Spalten, Zweispalter stapeln.

---

## 5. Die Bühne und die drei Ebenen

Das Herz jeder Prozessseite. Eine Fläche in `--paper-2` mit 40px-Laborraster und leichter Vignette, Seitenverhältnis 4:3 (Handy 1:1).

### Zoom-Grammatik

| Ebene | Name | Maßstab | Darstellung | Technik |
| --- | --- | --- | --- | --- |
| 1 | Das Gericht | ≈ 20 cm | Gegenstand in der Küche, vereinfacht illustriert | SVG |
| 2 | Die Oberfläche / Struktur | ≈ 1–2 mm | Querschnitt oder Ausschnitt, mit Messgerät | SVG |
| 3 | Die Moleküle | ≈ 1–10 nm | Punkt-Sprache, Partikel in Bewegung | Canvas |

**Regeln:**

- Jede Ebene zeigt **denselben Zustand** derselben Simulation. Ein Regler wirkt auf alle drei.
- Hineinzoomen über eine **Linse**: gestrichelter Kreis in `--crust`, langsam rotierend (14s), Label „ZOOM“. Sie sitzt genau dort, wo die nächste Ebene spielt.
- Zusätzlich Zoom-Leiste über der Bühne: „1 · Gericht ≈ 20 cm“ usw. Aktive Stufe in `--ink` gefüllt.
- HUD in der Bühne oben: links Ebene und Name, rechts Hinweis oder Maßstab. Mono, 10px, Sepia.
- Maßstabsangaben sind echte Größenordnungen, keine Deko.

### Übergänge

| Bewegung | Wert |
| --- | --- |
| Zoom hinein | alte Ebene skaliert auf 3.2 und blendet aus, neue kommt von 0.35 auf 1 |
| Zoom heraus | umgekehrt |
| Dauer | Transform 700ms, Deckkraft 550ms |
| Kurve | `cubic-bezier(.6, .05, .2, 1)` |
| Ursprung | `transform-origin` = Position der Linse |

Mausrad und Tasten (Enter/Leertaste auf der Linse) zoomen ebenfalls. Bei `prefers-reduced-motion` nur kurzes Überblenden.

### Unter der Bühne, immer in dieser Reihenfolge

1. **Statuszeile:** Fraunces kursiv 20px, ein bis zwei Sätze. Sagt in Worten, was gerade passiert und warum („Wasser verdampft. Die Oberfläche hängt bei 100 °C fest.“). `aria-live="polite"`.
2. **Messwerte:** 4–5 Kacheln, Label in Mono 9.5px, Wert in Mono 18px, optional dünner Balken (3px).
3. **Regler und Knöpfe:** Hauptregler mit Wert im Label. Primärknopf gefüllt in `--crust`, zweiter Knopf mit `--ink`-Rahmen.
4. **Legende** der Punkt-Sprache, nur die Stoffe, die auf Ebene 3 vorkommen.

---

## 6. Vorlagen nach Eintragstyp

| Typ | Vorlage | Bühne | Besonderheit |
| --- | --- | --- | --- |
| Prozess | `zoom3-simulation` | 3 Ebenen | Simulation mit 1–3 Stellschrauben |
| Symptom | `pfannentest` + `entscheidungsbaum` | 1 Ebene, Test | Diagnose in 2–3 Fragen, Punktbaum zeigt den Weg |
| Ziel | `punktmatrix` | Hebel × Techniken | Einstieg für Suche „Wie wird X knuspriger?“ |
| Technik | `ablauf` | Schritte als Abfolge | Jeder Schritt verweist auf den Mechanismus |
| Zutat | `punktmatrix` | Rollen der Zutat | Welche Prozesse sie auslöst oder bremst |
| Stellschraube | `skala` | Regler mit Wirkungen | z. B. pH: sauer ↔ basisch |
| Welt | – | Übersicht | Sammelt alle Einträge einer Welt |

Simulationen bleiben **bewusst vereinfacht** und sagen das im Fuß: „Modell vereinfacht · Zeit beschleunigt“. Schwellenwerte (100 °C, 140 °C, Fenstertest) stimmen aber.

Die erste Ansicht ist nie leer: Die Simulation startet in einem lehrreichen Zustand und läuft ein paar Sekunden vor.

---

## 7. Bausteine des Eintrags

In dieser Reihenfolge unter der Bühne:

1. **Kurz gesagt** – ein Satz, 20px, „Kurz gesagt:“ fett.
2. **Bild im Kopf** – Kasten in `--paper-2` mit `--rule`-Rahmen, Label in Mono, Text in Fraunces 21px. Pflicht für jeden Eintrag.
3. **Faustregeln** (nummeriert, Ziffern in `--crust`) und **Stellschrauben** (Liste: Name links, Wirkung rechts in Mono) nebeneinander.
4. **Mythos** – Stempel „MYTHOS“ in `--crust`, Rahmen 1.5px, um −4° gedreht. Behauptung in Anführungszeichen, dann die Richtigstellung.
5. **In der Praxis** – Kacheln je Lebensmittel-Welt. Titel mit kleinem Aromaprofil in Punkt-Sprache (3 Punkte, Größe = Anteil) oder Netzstärke (5 Punkte gefüllt/leer).
6. **Verwandte Einträge** – Chips, voll gerundet, mit „→“ in `--crust`.

Symptomseiten: Pfannentest → Diagnose → alle Ursachen nach Häufigkeit (3-Punkte-Skala) → Bild im Kopf → **Prinzip-Karte** (starker `--ink`-Rahmen, Punktmarke, Verweis auf den Prozess).

Kopf jeder Seite: Augenbraue in Mono (`Kochwissen · Prozess · Nr. 001 · Einsteiger`, Symptome mit Etikett auf `--crust`), Titel, Lead-Satz. Fuß: `Kochwissen` links, Modellhinweis rechts.

---

## 8. Illustrationen (KI-generiert)

Für Wärme auf Ebene 1, Welt-Seiten und Zutaten. **Eine Illustration pro Zutat oder Welt, nie pro Eintrag.** In Batches über eine Bild-API, immer mit demselben Stil-Prompt:

> Vintage cookbook illustration, loose watercolor and fine ink line, warm cream paper texture, muted earthy palette (sepia, ochre, terracotta, sage), single subject centered with generous empty space, no text, no lettering, no background scene, soft natural light, hand-drawn feel, 19th-century kitchen ephemera style

Ergänzt nur durch das Motiv („a single russet potato cut into wedges“). Freistellbar, quadratisch, ausreichend Rand. Keine Personen, keine Marken, keine bekannten Figuren.

Illustrationen und Diagramme mischen sich nicht in einem Bild: Ebene 1 darf illustriert sein, Ebenen 2 und 3 sind immer gezeichnete Vektoren in der Punkt-Sprache.

---

## 9. Sprache

- Deutsch, Alltagssprache, Sätze unter 25 Wörtern. Fachwort nur in Klammern: „Eiweiß verändert sich (Denaturierung)“.
- Schweizer Kontext ist willkommen (Ruchmehl, Halbweissmehl), aber Hochdeutsch im Text.
- Jede Erklärung hat eine Analogie aus dem Alltag.
- Knöpfe sagen, was passiert („Trocken getupft einlegen“, „Nochmal von vorn“).
- Keine Ausrufezeichen, keine Emojis, keine Werbesprache.

---

## 10. Technik und Zugänglichkeit

- Grafiken aus Code: SVG für Ebenen 1–2, Canvas für Ebene 3. Keine Bilddateien für Diagramme.
- Jede Linse ist per Tastatur erreichbar (`tabindex="0"`, `role="button"`). Sichtbarer Fokus: 2px `--crust`.
- `prefers-reduced-motion`: keine rotierenden Linsen, kein Dampf, nur Überblenden.
- Statuszeile und Diagnosekarte mit `aria-live="polite"`.
- Seiten funktionieren ab 360px Breite ohne seitliches Scrollen.

---

## 11. Nicht tun

- Keine Fotos.
- Keine Schatten, keine Verläufe als Schmuck, keine großen abgerundeten Karten.
- Keine zweite Akzentfarbe neben `--crust`.
- Keine chemischen Strukturformeln oder Molekülmodelle. Moleküle sind Punkte.
- Keine nummerierten Marker (01, 02 …), wenn es keine echte Reihenfolge gibt.
- Keine Grafik, die nur für einen Eintrag existiert und nicht aus einer Vorlage kommt.
