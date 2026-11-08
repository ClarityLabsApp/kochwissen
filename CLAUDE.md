# Garum (Projektordner: kochwissen) – Arbeitsanleitung für Claude

Kochwissen ist eine visuelle Bibliothek, die erklärt, **warum** Kochen und Backen funktionieren. Kein Rezeptbuch: Wer die Vorgänge versteht, kocht freier. Besitzer: Phil (Luzern). Sprache der Inhalte: Deutsch.

Lies vor jeder Arbeit auch **`DESIGN.md`** (Bildsprache, Farben, Vorlagen). Was dort steht, gilt.

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| `content/schema.json` | JSON-Schema für jeden Eintrag |
| `content/master-list.json` | Alle geplanten Einträge mit Typ, Links, Synonymen (Gerüst des Buchs) |
| `content/entries/<id>.json` | Ausgeschriebene Einträge, eine Datei pro Eintrag, Dateiname = id |
| `scripts/validate.mjs` | Prüft Schema, Verknüpfungen, Diagnosebäume, Glossar, Lernpfade und den Schreibleitfaden (Analogien einmalig, Sätze ≤ 25 Wörter, kein Werbeton) als Hinweise. Läuft vor jedem Build |
| `lib/content.ts` | Lädt Inhalte, zerlegt Glossar-Markierungen |
| `app/` | Next.js App Router: Bibliothek `/`, Eintrag `/eintrag/[id]` |
| `lib/search.ts` | Suche (Deutsch und Englisch): Titel 3, Synonyme 2.5, Kurz 1, Zusatzwörter 0.8 (Ursachen, Faustregeln, andere Sprache; `searchExtras` in `lib/content.ts`, als statische Datei `/suche-index/<lang>` erst beim Tippen geladen). Seltene Wörter zählen mehr, alle Suchwörter in einem Titel oder Synonym geben Extrapunkte, Problemwörter („nicht“, „zu“, „won't“) bevorzugen Probleme. Stammformen, Zusammensetzungen, Tippfehler, Wörterbuch `THESAURUS`. Test: `npx tsx scripts/suche/test.ts` (Fragen in `scripts/suche/fragen.json`, Kontrolle `fragen-kontrolle.json`). Neue Einträge: gute Alltags-Synonyme sind der wichtigste Hebel |
| `content/lernpfade.json` | Lernpfade: geführte Reihen von Einträgen (`id`, `titel`, `kurz`, `fuer`, `dauer`, `schritte[{id, warum}]`, `quiz[{frage, antworten, richtig, erklaerung, eintrag}]`). Seiten `/pfad`, `/pfad/[id]`; auf Eintragsseiten Navigation mit `?pfad=…`, Fortschritt im Browser |
| `components/` | Library (Startseite: Suche, drei Einstiege, Merkliste, Welten, Lernpfade, Eintrag des Tages), SiteNav (Menü auf jeder Seite: Welten mit Bildern, die vier Fragen, Lernpfade, Suche, Merkliste; unter 1000 px ein Menü-Knopf), views/HubView (Übersichtsseiten, Brotkrumen `Crumbs`, Zeilen `Row`, `MoreGroups`), PathSteps, PathNav, Diagnosis, Term (Glossar-Popup), RichText |
| `lib/nav.ts` | Ordnung für Besucher: vier Fragen `GROUPS` (probleme = symptom, ziele = ziel, verstehen = prozess/technik/zutat/stellschraube/begriff, ausprobieren = gericht/experiment/labor), `THEMES` für Vorgänge, `DOORS` der Startseite. Die elf Typen bleiben intern und erscheinen nur als Etikett |
| `public/prototypen/` | Die drei ursprünglichen HTML-Prototypen, nur noch als Referenz (alle als Komponenten nachgebaut) |

Seiten: `/probleme`, `/ziele`, `/verstehen`, `/ausprobieren`, `/alle` (A–Z), je auch unter `/en/…`. Welt-Einträge (`/eintrag/w-…`) zeigen oben „Alles zu …“, nach den vier Fragen geordnet. Jeder Eintrag hat Brotkrumen (Garum › Frage › Welt), ein anklickbares Typ-Etikett und unten „Wie weiter?“ (drei Karten: verstehen, warum · mehr aus der Welt · passt dazu). Suche auch über `/?q=…`; alte Links `/?k=typ` leiten auf die Frage-Seite weiter.

Befehle: `npm run dev` · `npm run validate` · `npm run build`

## Eintragstypen

`prozess` (was passiert) · `ziel` (was will ich erreichen) · `technik` (welcher Handgriff) · `symptom` (was ist schiefgelaufen) · `zutat` (was tut eine Zutat) · `stellschraube` (woran drehe ich) · `welt` (Lebensmittel-Welt) · `begriff` (Glossar) · `gericht` (warum funktioniert ein Rezept: `schluesselmomente` mit `schritt`, `warum`, `prinzip`) · `experiment` (zum Ausprobieren, auch mit Kindern: `material`, `schritte`, `beobachtung`, `erklaerung`, `dauer`, `sicherheit`). `labor` (Grundzutat selber herstellen: `material`, `dauer`, `sicherheit`, `schluesselmomente` als Schritte mit Prinzip, `ergebnis`, `haltbarkeit`, `verwendung`). IDs: Gerichte `g-…`, Experimente `x-…`, Labor `l-…`.

Drei Einstiege müssen immer funktionieren: vom Problem (Symptom), vom Ziel („Wie werden Wedges knuspriger?“) und vom Prinzip (Prozess). Darum: **jeder Eintrag verlinkt in alle Richtungen**, die Sinn ergeben.

## Schreibleitfaden

Gilt für jeden Text in einem Eintrag.

1. **Erster Satz trifft den Kern.** `kurz` ist ein einziger Satz, verständlich ohne Vorwissen.
2. **Alltagssprache.** Sätze unter 25 Wörtern. Fachwort nur in Klammern hinter dem Alltagswort: „Eiweiß verändert sich (Denaturierung)“.
3. **Jeder Eintrag hat ein `bild_im_kopf`.** Eine Analogie aus dem Alltag, die man sich merken kann (Lagerfeuer mit nassem Holz, Kaugummi-Netz, Mörtel zwischen Ziegeln). Keine Analogie zweimal verwenden.
   Absolute Wörter (nichts, nie, immer, alles, jede) nur, wenn sie wirklich ausnahmslos stimmen; Temperaturen sind Bereiche, ab denen etwas spürbar schnell läuft, keine Schalter.
4. **Was passiert → warum wichtig → woran drehen.** In dieser Reihenfolge denken.
5. **Faustregeln sind handfest.** Etwas, das man morgen in der Küche anders macht. Höchstens fünf.
6. **Zahlen nur, wenn sie stimmen.** Temperaturen und Mengen mit Quelle, sonst als Richtwert kennzeichnen.
7. **Fachbegriffe markieren.** Nach dem Schreiben `npm run glossar` laufen lassen. Jedes Wort, das ein Hobbykoch nicht sicher kennt, beim ersten Vorkommen als `[[id]]` oder `[[id|Anzeigetext]]`. Fehlt der Begriff, einen `begriff`-Eintrag anlegen (ein Satz in `kurz`). Beispiel: `[[arosieren|Arosieren]]`.
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
- `ParticleSim` – Canvas-Simulationen, eine für **jeden** Prozess (Preset-id = Eintrags-id). Regler: `slider`, `toggle`, `ph` (sauer/neutral/basisch) oder `seg` (eigene Optionen), `reset`. Automatischer Ablauf beim Öffnen: Liste `AUTO`. Neue Presets dort anlegen und in `SIMS` in `Visual.tsx` eintragen
- `MaillardSim` – Maillard-Reaktion in drei Zoomstufen (Gericht, Oberfläche, Moleküle), ersetzt den alten Prototyp
- `ExperimentCompare` – Vorher-Nachher für Experimente: `vorlage: vergleich`, `params.vergleich` = Felder mit `gefaess` (glas, flasche, schuessel, teller, pfanne), `inhalt`, `vorher`/`nachher` (farbe, fuell, trueb, schaum, blasen, ballon, kristalle, tropfen, klumpen, bodensatz, tanzen)
- Kein Prototyp mehr per iframe: `PROTOTYPES` in `lib/content.ts` ist leer, „Steak grau“ nutzt `PanTest`

## Verlinkung und Tempo

- Verwandte Einträge werden direkt im Text verlinkt: `python3 scripts/inline-links.py` setzt beim ersten Vorkommen eines Titels `[[id|Wort]]` (Deutsch und Englisch). Was im Text verlinkt ist, erscheint nicht mehr in „Verwandte Einträge“. Nach neuen Einträgen erneut laufen lassen.
- Animationen richten ihr Tempo nach dem Text: `readMs(text)` und `tour()` in `components/visuals/useInView.ts`. Jeder neue Text bleibt so lange stehen, wie man zum Lesen braucht.
- Skalen (Temperatur, Stellschrauben) haben nur einen Balken, den man direkt zieht, plus „Nochmal“.
- Faustregeln nennen das Ziel und den Grund („Für X: tu Y, weil Z“), besonders wenn sie gängigem Küchenwissen widersprechen.

## Name und Adresse

- Die Seite heisst **Garum** (Wortspiel mit „warum“ und „gar“), Adresse **garum.guide**. Untertitel: „Verstehen, warum Kochen funktioniert“ / „Understand why cooking works“.
- Adresse zentral in `lib/site.ts` (in Produktion https://garum.guide).

- Impressum und Datenschutz: `/impressum`, `/datenschutz` (und `/en/…`), Texte in `components/views/LegalView.tsx`, Kontakt `CONTACT_EMAIL` in `lib/site.ts` (Weiterleitung über den Domain-Anbieter). Fußzeile `components/SiteFooter.tsx` auf jeder Seite.
- Merkliste und „gelesen“ ohne Konto: `lib/memo.ts` (localStorage), Knopf `components/MerkButton.tsx` auf Eintragsseiten, Bereich „Deine Merkliste“ auf der Startseite, teilbar als Link `/?merk=id1,id2`.
- Schriften werden selbst ausgeliefert (`@fontsource…` in `app/layout.tsx`), keine Verbindung zu Google Fonts. Keine Cookies, kein Tracking.

## Englische Version

- Deutsch unter `/`, Englisch unter `/en/…`. Sprachauswahl DE | EN in `components/SiteNav.tsx`; die Sprache folgt dem Pfad (`langOf`, `switchPath` in `lib/i18n.ts`).
- Alle Bedientexte stehen im Wörterbuch `UI` in `lib/i18n.ts` (de und en). Neue Knöpfe oder Überschriften immer dort eintragen, nie fest in Komponenten.
- Einträge: `content/en/entries/<id>.json` enthält **nur** übersetzte Textfelder und liegt über dem deutschen Eintrag (`getEntry(id, "en")`). Fehlt die Datei, zeigt die englische Seite den deutschen Text mit Hinweis und `noindex`.
- Werkzeug: `python3 scripts/i18n/textfelder.py extract id1 id2 > batch.json` zieht die Texte heraus, `… apply batch.json` setzt die Übersetzung wieder in den deutschen Aufbau ein (Verweise, Diagnose-Ziele, Temperaturen kommen immer aus dem Deutschen).
- Wird ein deutscher Eintrag geändert, die englische Datei mit anpassen. Der Validator prüft, dass Aufbau und Verweise übereinstimmen.
- Lernpfade und Quiz: `content/en/lernpfade.json`.
- Animationen bleiben auf Deutsch geschrieben. `lib/simText.ts` übersetzt jeden angezeigten Text (auch Beschriftungen im Canvas) über `lib/sim-en.json` und Muster für Texte mit Zahlen. Neue Animationstexte dort ergänzen.
- Englisch ist britisch (colour, flavour, yoghurt), Schweizer Begriffe werden erklärt (Zopf, Rösti, Älplermagronen).

## Offene Aufgaben

- [x] Simulationen Gluten-Netz und Karamellisierung, Maillard als React-Komponente (2. November 2026)
- [x] Alle drei Prototypen als Komponenten (Maillard → `MaillardSim`, Gluten → Preset `glutenbildung`, Steak grau → `PanTest`)
- [x] Alle 197 Einträge der Masterliste als Entwurf geschrieben (1. November 2026)
- [x] Zahlen gegen Quellen geprüft, Korrekturen und offene Richtwerte in `content/PRUEFUNG.md` (2. November 2026)
- [x] Sicherheitsupdate auf Next.js 16 / React 19, `npm audit` sauber. Seitenparameter sind asynchron (`await params`)
- [x] Alle 372 Einträge auf `geprueft` gesetzt (3. November 2026, auf Phils Anweisung nach zwei externen KI-Prüfungen; Korrekturen: Temperaturskala-Text ohne absolutes „nichts“, Maillard „rasch ab etwa 140 °C“, Einkochen und flüchtige Aromen, Gelatine/Saft, Backpulver „die meisten“, Saucen „die meisten“). Neue Einträge starten weiter als `entwurf`. Review durch Phil: Prüfliste unter `/pruefen` (versteckt, noindex): Phil markiert «Passt» oder schreibt Anmerkungen und fügt das kopierte Ergebnis in den Chat; dann `status` der genannten ids auf `geprueft` setzen und Anmerkungen einarbeiten
- [x] Besuchsstatistik: Vercel Web Analytics (`@vercel/analytics`, ohne Cookies), in der Datenschutzerklärung beschrieben; im Vercel-Projekt unter Analytics aktivieren
- [x] 15 Gerichte und 12 Experimente ergänzt (Generator `scripts/batches/gen_batch_gerichte_experimente.py`)
- [x] Batch Grundlagen-Chemie II: Geschmack, Kälte, Haltbarkeit, Enzyme, Druck, Basen, Zucker (30 Einträge, `scripts/batches/gen_batch_chemie2.py`)
- [x] Kategorie „Labor“ mit 8 Rezepten (Backpulver, Butter, Bratbutter/Ghee, Frischkäse, Joghurt, Sauerteig, Crème fraîche, gebackenes Natron), `scripts/batches/gen_batch_labor.py`
- [x] Labor II: Mascarpone, Vanilleextrakt, Puderzucker, Buttermilch-Ersatz, Senf, Sauerkraut, brauner Zucker, Dulce de leche, Apfelpektin, Labneh (`scripts/batches/gen_batch_labor2.py`)
- [ ] Weitere Labor-Rezepte (z. B. Essig-Mutter, Ricotta aus Molke, Kräutersalz, Kimchi). Keine Rezepte mit Botulismus-Risiko (Knoblauch- oder Kräuteröl ungekühlt, Einkochen säurearmer Lebensmittel)
- [x] Startseite mit drei Einstiegen (Problem, Ziel, Verstehen), Eintrag des Tages, 5 Lernpfade, 6 Schweizer Gerichte (`gen_batch_schweiz.py`)
- [x] Bilder für 53 Gerichte, Experimente und Labor-Rezepte (2. November 2026). Neue Motive: `visual.illustration` setzen, `npm run illustrationen` erzeugt PNG, dann `python3 scripts/freistellen.py` (WebP, transparent, beschnitten), PNG löschen
- [x] Google: Seitentitel mit Zusatz je Typ (`TITLE_SUFFIX` in `EntryView.tsx`, z. B. „Ursachen und Lösung“), strukturierte Daten (Article/DefinedTerm + BreadcrumbList je Eintrag, WebSite + Organization auf der Startseite), hreflang de/en/x-default in Sitemap und Metadaten (3. November 2026). Search Console: Phil bestätigt die Domain per DNS-TXT bei Namecheap
- [x] Seitenbeschreibungen, Vorschaubilder (Open Graph), Sitemap, robots.txt; Druckansicht mit Knopf bei Experimenten und Labor; Sprunglink zum Inhalt
- [x] Quiz am Ende jedes Lernpfads (29 Fragen), 6 neue Simulationen (Verdampfen, Stärke, Kollagen, Konvektion, Blätterteig, Milchsäuregärung)
- [x] Alle 54 Prozesse haben eine Animation (2. November 2026)
- [ ] Weitere Gerichte und Experimente (Vorher-Nachher-Grafik steht, neue Experimente brauchen `params.vergleich`)
- [ ] Semantische Suche (z. B. pgvector) als Ergänzung; bis dahin fehlende Alltagswörter in `THESAURUS` nachtragen
- [x] 45 Aquarell-Illustrationen (Welten und Zutaten) in `public/illustrationen/<id>.webp`, Anzeige im Seitenkopf. Neue Motive: `visual.illustration` setzen, `npm run illustrationen -- --only id1,id2` (schreibt WebP mit transparentem Hintergrund; ältere Bilder wurden per Skript freigestellt und beschnitten)
- [x] Startseite: Bibliothek als illustriertes Inhaltsverzeichnis (`components/Contents.tsx`, Kapitel Was passiert / Womit / Wofür) statt Kategorienliste; das Molekül wurde wieder entfernt. Kategoriebilder `cat-<typ>` aus `content/illustrationen-extra.json`, bis dahin Stellvertreterbilder. „Symptome“ heissen jetzt „Probleme“ (2. November 2026)
- [x] Englische Version: Gerüst, alle 286 Einträge, Lernpfade mit Quiz, Animationstexte (2. November 2026)
- [x] Glossar-Prüfung: `npm run glossar` (Bericht), `npm run glossar -- --fix` (verlinkt erstes Vorkommen), `-- --en` für die Übersetzungen. Fachwörter und Ausnahmen in `scripts/glossar.mjs`, weitere Muster (Deutsch und Englisch) in `content/glossar-muster.json`
- [x] Welten II: 37 Einträge für Kaffee & Tee, Pasta, Geflügel, Fisch, Reis und die neuen Welten Hülsenfrüchte, Obst & Früchte, Kräuter & Gewürze, Pilze (`scripts/batches/gen_batch_welten2.py`, 2. November 2026). Texte als Paare L(deutsch, englisch), daraus Eintrag und Übersetzung
- [x] Weihnachtsbatch: 15 Einträge (Mailänderli, Spitzbuben, Zimtsterne, Brunsli, Chräbeli, Grittibänz, Lebkuchen, Glühwein, Guetzli hart, Teig bröckelt, Teig kühlen, Guetzli lagern, Hirschhornsalz, Pottasche, Apfel-Experiment) und Lernpfad `weihnachtsbaeckerei` mit Quiz (`scripts/batches/gen_batch_weihnachten.py`, 3. November 2026)
- [x] Fermentation & Geschmack: 12 Einträge (Garum, Koji, Edelschimmel, Proteolyse, Bitter, Süß, Zusammenspiel der Geschmäcker, Geschmack und Nase, Flavor Pairing, Xanthan, Experimente Nase zu und Salz gegen Bitterkeit), `scripts/batches/gen_batch_geschmack.py`, 3. November 2026. Startseite verlinkt unter dem Einleitungstext auf `garum` („Warum Garum?“)
- [x] Welten III: 19 Einträge gegen Lücken in den Welten (Meeresfrüchte: Muscheln, Crevetten, Tintenfisch, Krustentiere rot, Jakobsmuscheln, Moules; Pilze: getrocknete Pilze, Aufwärmen, Rahmpilze; Hülsenfrüchte: Linsen, Salzwasser, Blähungen, Tofu, Falafel; Eier: grüner Rand, Schälen; Obst: Früchte sinken, Mazerieren; Getreide: Quinoa), `scripts/batches/gen_batch_welten3.py`, 8. November 2026
- [x] Wahrnehmung: 7 Einträge (Mundgefühl, Temperatur und Geschmack, Kontraste, Richtig abschmecken, Augen und Ohren essen mit, Experimente Farbe täuscht und warme Limonade) und Lernpfad `schmecken-lernen` (`scripts/batches/gen_batch_wahrnehmung.py`). Auf `/verstehen` eigener Bereich „Geschmack und Wahrnehmung“ (`WAHRNEHMUNG` in `lib/nav.ts`, quer über die Typen) und oben der Kasten „Die Grundregeln der Küche“ aus dem Lernpfad `grundprinzipien` (8. November 2026)
- [x] Glossar II: 32 neue Begriffe aus Biologie, Chemie und Küchensprache, 43 insgesamt (`scripts/batches/gen_begriffe2.py`, 2. November 2026)
