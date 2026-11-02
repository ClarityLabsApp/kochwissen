// Findet Fachwörter, die im Text stehen, aber nicht als [[id]] verlinkt sind.
// npm run glossar          → Bericht
// npm run glossar -- --fix → setzt beim ersten Vorkommen pro Eintrag einen Link
// Der Validator nutzt findUnmarked() und gibt eine Zusammenfassung als Hinweis aus.
import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

/** Fachwort → Eintrag. Muster sind Wortanfänge (Groß-/Kleinschreibung egal). Neue Fachwörter hier ergänzen. */
export const FACHWOERTER = {
  "maillard-reaktion": ["Maillard"],
  karamellisierung: ["karamellisier", "Karamellisation"],
  staerkeverkleisterung: ["verkleister", "Verkleisterung"],
  retrogradation: ["Retrogradation", "retrogradier"],
  "eiweiss-denaturierung": ["Denaturierung", "denaturier"],
  emulsion: ["Emulsion"],
  emulgator: ["Emulgator", "Lecithin"],
  osmose: ["Osmose"],
  glutenbildung: ["Gluten"],
  "anthocyan-farbe": ["Anthocyan"],
  "chlorophyll-farbe": ["Chlorophyll"],
  leidenfrost: ["Leidenfrost"],
  blanchieren: ["blanchier"],
  enzym: ["Enzym"],
  "ph-wert": ["pH-Wert", "pH "],
  diffusion: ["Diffusion"],
  "kollagen-gelatine": ["Kollagen"],
  deglacieren: ["deglacier", "ablösch"],
  legieren: ["legier"],
  montieren: ["montier"],
  mantecare: ["Mantecare", "mantecat"],
  temperieren: ["temperier"],
  "sous-vide": ["Sous-vide", "Sous vide"],
  pektin: ["Pektin"],
  arosieren: ["arosier"],
  kerntemperatur: ["Kerntemperatur"],
  nachgaren: ["nachgar", "Nachgaren"],
  fenstertest: ["Fenstertest"],
  ofentrieb: ["Ofentrieb"],
  hydration: ["Hydration", "Teigausbeute"],
  glutamat: ["Glutamat"],
  capsaicin: ["Capsaicin"],
  sublimation: ["Sublimation", "sublimier"],
  umami: ["Umami"],
  amylase: ["Amylase"],
  wasseraktivitaet: ["Wasseraktivität"],
};

// Weitere Muster (Glossar II) und englische Muster: content/glossar-muster.json
const extra = JSON.parse(readFileSync(join(root, "content/glossar-muster.json"), "utf8"));
for (const [id, stems] of Object.entries(extra.de)) FACHWOERTER[id] = [...(FACHWOERTER[id] ?? []), ...stems];
/** Englische Muster: nur für die Übersetzungen in content/en/entries (npm run glossar -- --en). */
export const FACHWOERTER_EN = extra.en;

/** Stellen, an denen ein Wort etwas anderes meint: Fachwort-id → Einträge, die übersprungen werden. */
export const AUSNAHMEN = {
  temperieren: ["emulsion", "legieren"], // dort: Zutaten angleichen, nicht Schokolade
};

/** Felder, die als RichText dargestellt werden: nur dort darf ein Link stehen. */
function fields(e) {
  const out = [];
  const add = (get, set) => { const v = get(); if (typeof v === "string") out.push({ get, set }); };
  for (const k of ["kurz", "bild_im_kopf", "bedeutung", "was_passiert", "warum_wichtig", "beobachtung", "erklaerung"]) add(() => e[k], (v) => (e[k] = v));
  for (const k of ["faustregeln", "typische_fehler", "schritte"]) (e[k] || []).forEach((_, i) => add(() => e[k][i], (v) => (e[k][i] = v)));
  (e.schluesselmomente || []).forEach((m) => add(() => m.warum, (v) => (m.warum = v)));
  (e.ursachen || []).forEach((u) => add(() => u.warum, (v) => (u.warum = v)));
  if (e.mythos) add(() => e.mythos.richtig, (v) => (e.mythos.richtig = v));
  (e.praxis || []).forEach((p) => add(() => p.text, (v) => (p.text = v)));
  return out;
}

const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
// Wortanfang, ganzes Wort bis zum Ende mitnehmen; nicht innerhalb von [[...]]
const patternFor = (stems) => new RegExp(`(?<![\\p{L}\\[|])(?:${stems.map(esc).join("|")})[\\p{L}-]*`, "iu");

/** Entfernt bestehende Markierungen, damit Wörter darin nicht doppelt zählen. */
const masked = (s) => s.replace(/\[\[[^\]]+\]\]/g, (m) => " ".repeat(m.length));

export function findUnmarked(entries, known, dict = FACHWOERTER) {
  const hits = [];
  for (const e of entries) {
    const fs = fields(e);
    const all = fs.map((f) => f.get()).join("\n");
    for (const [id, stems] of Object.entries(dict)) {
      if (id === e.id || !known.has(id) || AUSNAHMEN[id]?.includes(e.id)) continue;
      if (all.includes(`[[${id}`)) continue; // schon irgendwo verlinkt
      for (const f of fs) {
        const m = patternFor(stems).exec(masked(f.get()));
        if (m) { hits.push({ entry: e.id, id, word: f.get().substr(m.index, m[0].length), field: f, index: m.index }); break; }
      }
    }
  }
  return hits;
}

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (isMain) {
  const en = process.argv.includes("--en");
  const deDir = join(root, "content/entries"), dir = en ? join(root, "content/en/entries") : deDir;
  const files = readdirSync(dir).filter((f) => f.endsWith(".json"));
  const entries = files.map((f) => JSON.parse(readFileSync(join(dir, f), "utf8")));
  const known = new Set(readdirSync(deDir).filter((f) => f.endsWith(".json")).map((f) => f.slice(0, -5)));
  const hits = findUnmarked(entries, known, en ? FACHWOERTER_EN : FACHWOERTER);
  const fix = process.argv.includes("--fix");
  if (fix) {
    // Pro Feld von hinten nach vorne ersetzen, damit die Positionen stimmen.
    const byField = new Map();
    for (const h of hits) { if (!byField.has(h.field)) byField.set(h.field, []); byField.get(h.field).push(h); }
    for (const [f, hs] of byField) {
      let s = f.get();
      for (const h of hs.sort((a, b) => b.index - a.index)) s = s.slice(0, h.index) + `[[${h.id}|${h.word}]]` + s.slice(h.index + h.word.length);
      f.set(s);
    }
    const touched = new Set(hits.map((h) => h.entry));
    for (const e of entries) if (touched.has(e.id)) writeFileSync(join(dir, `${e.id}.json`), JSON.stringify(e, null, 2) + "\n");
    console.log(`${hits.length} Links gesetzt in ${touched.size} Einträgen.`);
  } else {
    for (const h of hits) console.log(`${h.entry}: „${h.word}“ → [[${h.id}]]`);
    console.log(`\n${hits.length} unverlinkte Fachwörter. Mit --fix automatisch verlinken.`);
  }
}
