// Sprachen und feste Texte der Oberfläche. Inhalte (Einträge, Lernpfade) liegen in content/ und content/en/.
export type Lang = "de" | "en";
export const LANGS: Lang[] = ["de", "en"];

/** Pfad in der gewünschten Sprache: Deutsch ohne Präfix, Englisch unter /en. */
export function href(lang: Lang, p: string) {
  if (lang === "de") return p;
  return p === "/" ? "/en" : `/en${p}`;
}
/** Sprache aus einem Pfad ablesen. */
export const langOf = (pathname: string): Lang => (pathname === "/en" || pathname.startsWith("/en/") ? "en" : "de");
/** Derselbe Pfad in der anderen Sprache. */
export function switchPath(pathname: string, to: Lang) {
  const base = langOf(pathname) === "en" ? pathname.replace(/^\/en/, "") || "/" : pathname;
  return href(to, base);
}

const de = {
  nav: { library: "Bibliothek", paths: "Lernpfade", skip: "Zum Inhalt springen" },
  home: {
    eyebrow: (n: number, m: number) => `Die Bibliothek · ${n} von ${m} Einträgen geschrieben`,
    h1a: "Verstehen, warum es ", h1b: "funktioniert",
    lede: "Kein Rezeptbuch, sondern die Vorgänge dahinter: einfach erklärt und sichtbar gemacht. Wer weiß, warum etwas passiert, kocht freier.",
    footerA: "Garum · warum Kochen funktioniert", footerB: "Inhalte im Aufbau",
  },
  search: {
    label: "Suche · Alltagssprache funktioniert", placeholder: "z. B. Wie werden meine Wedges knuspriger?",
    examples: ["Wie werden meine Wedges knuspriger?", "Fleisch wird trocken", "Sauce zu dünn", "Rösti", "Experiment für Kinder", "Mayo gerinnt"],
    best: "Beste Antwort", open: "Eintrag öffnen →", none: "Nichts gefunden. Versuche ein anderes Wort, z. B. „saftig“, „Sauce“ oder „Experiment“.",
    hits: "Treffer", byFit: "sortiert nach Passung", allHits: "Alle Treffer", whole: "Die ganze Bibliothek",
    onlyWritten: (a: number, b: number) => `Nur ausgeschriebene Einträge · ${a} von ${b}`,
  },
  doors: {
    symptom: ["Etwas ist schiefgegangen", "Finde heraus, warum, und wie es nächstes Mal klappt.", "Alle Probleme"],
    ziel: ["Ich will, dass es … wird", "Knuspriger, saftiger, luftiger: die Hebel dafür.", "Alle Ziele"],
    prozess: ["Ich will verstehen", "Was in Pfanne, Ofen und Teig wirklich passiert.", "Alle Prozesse"],
    tab: ["Schiefgelaufen", "Mein Ziel", "Verstehen"],
    pathLink: "Lernpfad: Die 10 wichtigsten Prinzipien",
  },
  daily: "Eintrag des Tages", read: "Lesen →", worlds: "Stöbern nach Welt", pathsRow: "Lernpfade · der Reihe nach verstehen",
  steps: (n: number) => `${n} Schritte`,
  types: {
    ziel: ["Ziele", "Was will ich erreichen?", "Ziel"], gericht: ["Gerichte", "Warum funktioniert dieses Rezept?", "Gericht"],
    experiment: ["Experimente", "Zum Ausprobieren in der Küche", "Experiment"], labor: ["Labor", "Grundzutaten selber herstellen", "Labor-Rezept"],
    symptom: ["Probleme", "Was ist schiefgelaufen?", "Problem"], prozess: ["Prozesse", "Was passiert beim Kochen?", "Prozess"],
    technik: ["Techniken", "Welcher Handgriff hilft?", "Technik"], zutat: ["Zutaten", "Was tut eine Zutat?", "Zutat"],
    stellschraube: ["Stellschrauben", "Woran kann ich drehen?", "Stellschraube"], welt: ["Lebensmittel-Welten", "Wo begegnet mir das?", "Welt"],
    begriff: ["Begriffe", "Was heißt das Wort?", "Begriff"],
  } as Record<string, [string, string, string]>,
  status: { entwurf: "entwurf", geprueft: "geprüft", geplant: "geplant", prototyp: "Prototyp" } as Record<string, string>,
  level: { einsteiger: "einsteiger", fortgeschritten: "fortgeschritten", profi: "profi" } as Record<string, string>,
  entry: {
    syn: "Auch gesucht als", short: "Kurz gesagt:", picture: "Bild im Kopf", means: (t: string) => `Was ${t} bedeutet`, happens: "Was passiert", why: "Warum wichtig",
    moments: "Die entscheidenden Momente", labSteps: "Schritt für Schritt: was dabei passiert", need: "Du brauchst", print: "Drucken",
    diag: "Was ist bei dir passiert?", levers: "Die Hebel", role: "Was die Zutat tut", how: "So geht’s", allSteps: "Alle Schritte als Liste",
    rules: "Faustregeln", knobs: "Stellschrauben", mistakes: "Typische Fehler", causes: "Alle Ursachen, nach Häufigkeit", nextTime: "Nächstes Mal",
    see: "Was du siehst", whyHappens: "Warum das passiert", result: "Ergebnis", keeps: "Haltbarkeit", use: "Wofür verwenden", myth: "MYTHOS",
    practice: "In der Praxis", seenIn: "Kommt vor bei", related: "Verwandte Einträge", sources: "Quellen", template: "Grafik-Vorlage", planned: "Dieser Eintrag ist geplant, aber noch nicht geschrieben.",
    notTranslated: "", tagPath: "Lernpfad",
  },
  diag: { q: (n: number) => `Frage ${n}`, cause: "WAHRSCHEINLICHE URSACHE", next: "Nächstes Mal", principle: "Prinzip dahinter", again: "Nochmal von vorn" },
  term: { soon: "Erklärung folgt.", go: "Zum Eintrag →" },
  path: {
    eyebrow: "Lernpfade", h1a: "Der Reihe nach ", h1b: "verstehen", lede: "Geführte Wege durch die Bibliothek. Jeder Schritt baut auf dem vorigen auf, und du kannst abhaken, was du schon gelesen hast.",
    done: (a: number, b: number) => `${a} von ${b} erledigt`, start: "Starten", cont: "Weiter", mark: (t: string) => `${t} als erledigt markieren`,
    nav: (t: string, i: number, n: number) => `Lernpfad · ${t} · Schritt ${i} von ${n}`, finished: "Geschafft. Jetzt zum Quiz →", test: "Teste dich",
  },
  quiz: {
    q: (i: number, n: number) => `Quiz · Frage ${i} von ${n}`, best: (a: number, n: number) => `Bestes Ergebnis: ${a} von ${n}`, result: "Quiz · Ergebnis",
    score: (a: number, n: number) => `${a} von ${n} richtig`, all: "Alles richtig. Du hast verstanden, worum es geht.", good: "Gut gemacht. Bei den anderen lohnt ein zweiter Blick in den Eintrag.",
    low: "Ein guter Anfang. Lies die Schritte noch einmal und versuch es dann wieder.", again: "Nochmal versuchen", right: "Richtig.", wrong: "Nicht ganz.", more: "Mehr dazu", nextQ: "Nächste Frage", show: "Ergebnis zeigen", answers: "Antworten",
  },
  toc: { what: "Was passiert", with: "Womit", for: "Wofür" },
  mol: { label: "Die Bibliothek als Molekül", head: (n: number) => `Die Bibliothek · ${n} Einträge`, tap: "Antippen", core: "Kern: Was passiert", inner: "Innen: Womit", outer: "Außen: Wofür", entries: (n: number) => `${n} Einträge`, all: (n: number, name: string) => `Alle ${n} ${name} →`, back: "← Zurück zur Übersicht", terms: "Begriffe" },
  vis: { model: "Modell vereinfacht", restart: "Neu starten", schematic: "Schematisch", again: "Nochmal", beforeAfter: "Vorher · Nachher", before: "Vorher", after: "Nachher", pause: "Pause", play: "Abspielen", flow: "Ablauf", step: (i: number, n: number) => `Schritt ${i} von ${n}`, pickTemp: "Temperatur wählen", netGoal: (t: string) => `Hebel und Techniken für „${t}“`, levers: "Hebel", techs: "Techniken", netIng: (t: string) => `Was ${t} tut`, role: "Rolle", proc: "Vorgang", stepsIn: (n: number) => `Ablauf in ${n} Schritten`, temps: "Die Temperaturen", at: (t: number) => `Bei ${t} °C:`, below: (c: number) => `Unter ${c} °C passiert noch nichts davon.`, from: (c: number) => `Ab ${c} °C:`, smoke: "Rauchpunkte im Vergleich", thresholds: "Temperatur-Schwellen", drag: "Ziehen zum Ausprobieren", smokeAt: (t: number) => `Bei ${t} °C raucht bereits:`, smokeBelow: (c: number) => `Unter ${c} °C raucht noch keines dieser Fette.`, smokeFrom: (c: number) => `Ab ${c} °C raucht auch:`, smokeFirst: (c: number) => `Ab ${c} °C raucht:` },
};

type Dict = typeof de;
const en: Dict = {
  nav: { library: "Library", paths: "Learning paths", skip: "Skip to content" },
  home: {
    eyebrow: (n, m) => `The library · ${n} of ${m} entries written`,
    h1a: "Understand why it ", h1b: "works",
    lede: "Not a recipe book, but the processes behind it: simply explained and made visible. If you know why something happens, you cook more freely.",
    footerA: "Garum · why cooking works", footerB: "Work in progress",
  },
  search: {
    label: "Search · everyday language works", placeholder: "e.g. How do I make my wedges crispier?",
    examples: ["How do I make my wedges crispier?", "Meat turns out dry", "Sauce too thin", "Rösti", "Experiment for kids", "Mayo splits"],
    best: "Best answer", open: "Open entry →", none: "Nothing found. Try another word, e.g. “juicy”, “sauce” or “experiment”.",
    hits: "Results", byFit: "sorted by relevance", allHits: "All results", whole: "The whole library",
    onlyWritten: (a, b) => `Only written entries · ${a} of ${b}`,
  },
  doors: {
    symptom: ["Something went wrong", "Find out why, and how to get it right next time.", "All problems"],
    ziel: ["I want it to be …", "Crispier, juicier, lighter: the levers for it.", "All goals"],
    prozess: ["I want to understand", "What really happens in the pan, the oven and the dough.", "All processes"],
    tab: ["Went wrong", "My goal", "Understand"],
    pathLink: "Learning path: The 10 key principles",
  },
  daily: "Entry of the day", read: "Read →", worlds: "Browse by food world", pathsRow: "Learning paths · understand step by step",
  steps: (n) => `${n} steps`,
  types: {
    ziel: ["Goals", "What do I want to achieve?", "Goal"], gericht: ["Dishes", "Why does this recipe work?", "Dish"],
    experiment: ["Experiments", "To try in the kitchen", "Experiment"], labor: ["Kitchen lab", "Make basic ingredients yourself", "Lab recipe"],
    symptom: ["Problems", "What went wrong?", "Problem"], prozess: ["Processes", "What happens when cooking?", "Process"],
    technik: ["Techniques", "Which technique helps?", "Technique"], zutat: ["Ingredients", "What does an ingredient do?", "Ingredient"],
    stellschraube: ["Levers", "What can I adjust?", "Lever"], welt: ["Food worlds", "Where do I meet this?", "World"],
    begriff: ["Terms", "What does the word mean?", "Term"],
  },
  status: { entwurf: "draft", geprueft: "reviewed", geplant: "planned", prototyp: "Prototype" },
  level: { einsteiger: "beginner", fortgeschritten: "intermediate", profi: "advanced" },
  entry: {
    syn: "Also searched as", short: "In short:", picture: "Picture it", means: (t) => `What ${t} means`, happens: "What happens", why: "Why it matters",
    moments: "The decisive moments", labSteps: "Step by step: what happens", need: "You need", print: "Print",
    diag: "What happened in your kitchen?", levers: "The levers", role: "What the ingredient does", how: "How it’s done", allSteps: "All steps as a list",
    rules: "Rules of thumb", knobs: "Levers", mistakes: "Common mistakes", causes: "All causes, by frequency", nextTime: "Next time",
    see: "What you see", whyHappens: "Why it happens", result: "Result", keeps: "Keeps for", use: "What to use it for", myth: "MYTH",
    practice: "In practice", seenIn: "Where you meet it", related: "Related entries", sources: "Sources", template: "Graphic template", planned: "This entry is planned but not yet written.",
    notTranslated: "This entry has not been translated yet. You are reading the German original.", tagPath: "Learning path",
  },
  diag: { q: (n) => `Question ${n}`, cause: "MOST LIKELY CAUSE", next: "Next time", principle: "The principle behind it", again: "Start again" },
  term: { soon: "Explanation coming soon.", go: "Go to entry →" },
  path: {
    eyebrow: "Learning paths", h1a: "Understand it ", h1b: "step by step", lede: "Guided routes through the library. Each step builds on the one before, and you can tick off what you have already read.",
    done: (a, b) => `${a} of ${b} done`, start: "Start", cont: "Continue", mark: (t) => `Mark ${t} as done`,
    nav: (t, i, n) => `Learning path · ${t} · Step ${i} of ${n}`, finished: "Done. On to the quiz →", test: "Test yourself",
  },
  quiz: {
    q: (i, n) => `Quiz · Question ${i} of ${n}`, best: (a, n) => `Best score: ${a} of ${n}`, result: "Quiz · Result",
    score: (a, n) => `${a} of ${n} correct`, all: "All correct. You have understood what it is about.", good: "Well done. For the others, it is worth another look at the entry.",
    low: "A good start. Read the steps again and then try once more.", again: "Try again", right: "Correct.", wrong: "Not quite.", more: "More on this", nextQ: "Next question", show: "Show result", answers: "Answers",
  },
  toc: { what: "What happens", with: "With what", for: "What for" },
  mol: { label: "The library as a molecule", head: (n) => `The library · ${n} entries`, tap: "Tap an atom", core: "Core: what happens", inner: "Inner: with what", outer: "Outer: what for", entries: (n) => `${n} entries`, all: (n, name) => `All ${n} ${name.toLowerCase()} →`, back: "← Back to the overview", terms: "Terms" },
  vis: { model: "Simplified model", restart: "Restart", schematic: "Schematic", again: "Again", beforeAfter: "Before · After", before: "Before", after: "After", pause: "Pause", play: "Play", flow: "Sequence", step: (i, n) => `Step ${i} of ${n}`, pickTemp: "Choose temperature", netGoal: (t) => `Levers and techniques for “${t}”`, levers: "Levers", techs: "Techniques", netIng: (t) => `What ${t} does`, role: "Role", proc: "Process", stepsIn: (n) => `Sequence in ${n} steps`, temps: "The temperatures", at: (t) => `At ${t} °C:`, below: (c) => `Below ${c} °C none of this happens yet.`, from: (c) => `From ${c} °C:`, smoke: "Smoke points compared", thresholds: "Temperature thresholds", drag: "Drag to try", smokeAt: (t) => `At ${t} °C these already smoke:`, smokeBelow: (c) => `Below ${c} °C none of these fats smokes yet.`, smokeFrom: (c) => `From ${c} °C, so does:`, smokeFirst: (c) => `From ${c} °C, this smokes:` },
};

export const UI: Record<Lang, Dict> = { de, en };
export const t = (lang: Lang) => UI[lang];
