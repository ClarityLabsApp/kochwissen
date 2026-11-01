// Suche in Alltagssprache: gewichtete Volltextsuche mit Stammformen, Tippfehler-Toleranz
// und einem kleinen Küchen-Wörterbuch (Problem ↔ Ziel). Läuft komplett im Browser.

export interface SearchItem {
  id: string; typ: string; titel: string; synonyme: string[]; kurz: string | null;
  links: string[]; verlinkt_von: string[];
}

const STOP = new Set(("wie wird werden wurde meine mein meinen meiner mache machen macht ich kann koennen man was warum weshalb wieso "
  + "der die das den dem des ein eine einen einer eines und oder mit beim bei zu zum zur ist sind nicht noch mehr immer so viel "
  + "sehr auch nur wenn dann aber was wo von vom im in an am auf aus fuer ohne gibt es sich mir mich bekomme bekommen hin richtig").split(" "));

export const norm = (s: string) => s.toLowerCase()
  .replace(/\[\[[a-z0-9-]+\|([^\]]+)\]\]/g, "$1").replace(/\[\[([a-z0-9-]+)\]\]/g, (_, id) => id.replace(/-/g, " "))
  .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/é|è/g, "e").replace(/[^a-z0-9 ]/g, " ");

/** Grobe deutsche Stammform: häufige Endungen weg (knuspriger → knusprig, Kartoffeln → kartoffel). */
export function stem(w: string) {
  if (w.length <= 4) return w;
  for (const suf of ["ungen", "erer", "eren", "ern", "ere", "er", "en", "es", "em", "e", "n", "s"]) {
    if (w.endsWith(suf) && w.length - suf.length >= 4) return w.slice(0, -suf.length);
  }
  return w;
}

/** Wörter in der Küche, die dasselbe meinen oder das Gegenteil eines Ziels beschreiben. */
const THESAURUS: Record<string, string[]> = {
  knusprig: ["kross", "crispy", "knackig", "labbrig", "weich", "matschig", "pappig", "lasch"],
  saftig: ["trocken", "zaeh", "strohig", "saft"],
  zart: ["zaeh", "hart", "gummig", "weich"],
  luftig: ["fluffig", "locker", "flach", "kompakt", "dicht", "speckig", "schwer", "sitzenbleiben", "aufgehen"],
  cremig: ["glatt", "samtig", "klumpig", "griesig", "koernig"],
  braun: ["braeunen", "kruste", "roesten", "anbraten", "blass", "farbe", "goldbraun"],
  dick: ["binden", "andicken", "duenn", "waessrig", "flussig", "fluessig", "sauce"],
  gerinnt: ["geronnen", "trennt", "getrennt", "flockt", "griesig", "bricht"],
  gruen: ["grau", "oliv", "farbe", "chlorophyll"],
  versuch: ["experiment", "ausprobieren", "kinder", "test", "zeigen", "selber"],
  einsinken: ["sinkt", "eingefallen", "zusammenfallen", "faellt", "zusammengefallen", "zusammen", "einfallen"],
  rezept: ["gericht", "kochen", "zubereiten"],
  salz: ["salzen", "gesalzen", "versalzen"],
  zucker: ["suess", "karamell"],
  ei: ["eier", "eiweiss", "eigelb", "eischnee"],
  kartoffel: ["kartoffeln", "wedges", "pommes", "roesti", "erdapfel"],
  fleisch: ["steak", "braten", "schnitzel", "huhn", "poulet"],
  brot: ["teig", "backen", "kruste", "krume"],
};
const EXPAND = new Map<string, Set<string>>();
for (const [k, vs] of Object.entries(THESAURUS)) {
  const group = [k, ...vs].map(stem);
  for (const w of group) {
    if (!EXPAND.has(w)) EXPAND.set(w, new Set());
    for (const o of group) if (o !== w) EXPAND.get(w)!.add(o);
  }
}

/** Levenshtein-Distanz mit frühem Abbruch, für Tippfehler. */
function dist(a: string, b: string, max: number) {
  if (Math.abs(a.length - b.length) > max) return max + 1;
  let prev = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    const cur = [i]; let best = i;
    for (let j = 1; j <= b.length; j++) {
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
      best = Math.min(best, cur[j]);
    }
    if (best > max) return max + 1;
    prev = cur;
  }
  return prev[b.length];
}

/** Wie gut passt ein Suchwort zu einem Wort im Text? 1 = genau, darunter = ungefähr. */
function wordMatch(t: string, w: string, rawT = t): number {
  if (w === t) return 1;
  const sw = stem(w);
  if (sw === t) return 0.95;
  if (t.length >= 3 && w.startsWith(t)) return 0.85;          // Wortanfang: "knusp" → knusprig
  if (t.length >= 5 && w.includes(t)) return 0.7;            // Wortteil: "kruste" in "brotkruste"
  if (sw.length >= 5 && t.startsWith(sw)) return 0.75;
  const tol = t.length >= 8 ? 2 : 1;
  if (rawT.length >= 4 && w.length >= 4 && dist(rawT, w, tol) <= tol) return 0.6;   // Tippfehler: "pomes" → pommes
  if (t.length >= 4 && w.length >= 4 && dist(t, sw, tol) <= tol) return 0.45;       // Tippfehler in der Stammform
  return 0;
}

interface Indexed { e: SearchItem; fields: [string[], number][] }
const indexCache = new WeakMap<SearchItem[], Indexed[]>();
function index(items: SearchItem[]) {
  let ix = indexCache.get(items);
  if (!ix) {
    const words = (s: string) => norm(s).split(/\s+/).filter((w) => w.length > 1);
    ix = items.map((e) => ({ e, fields: [[words(e.titel), 3], [words(e.synonyme.join(" ")), 2.5], [words(e.kurz ?? ""), 1]] }));
    indexCache.set(items, ix);
  }
  return ix;
}

const TYPE_BONUS: Record<string, number> = { ziel: 0.4, symptom: 0.35, gericht: 0.3, experiment: 0.25, technik: 0.2, prozess: 0.15 };

export interface SearchResult { scores: Map<string, number>; best: SearchItem | null; terms: string[] }

export function search(items: SearchItem[], q: string): SearchResult | null {
  const raw = norm(q).split(/\s+/).filter((w) => w.length > 1 && !STOP.has(w));
  if (!raw.length) return null;
  const terms = raw.map(stem);
  const wantsExperiment = terms.some((t) => ["experiment", "versuch", "ausprobier", "kinder", "kind"].some((k) => t.startsWith(k)));
  const hits: [SearchItem, number][] = [];

  for (const { e, fields } of index(items)) {
    let s = 0, matched = 0;
    for (const [ti, t] of terms.entries()) {
      let best = 0;
      const alts = EXPAND.get(t);
      for (const [ws, weight] of fields) for (const w of ws) {
        best = Math.max(best, wordMatch(t, w, raw[ti]) * weight);
        if (alts && best < weight * 0.8) for (const a of alts) best = Math.max(best, wordMatch(a, w) * weight * 0.7);
      }
      if (best > 0) { matched++; s += best; }
    }
    if (!matched) continue;
    // Treffer auf alle Suchwörter zählen deutlich mehr als einzelne.
    s *= 0.5 + 0.5 * (matched / terms.length);
    s += TYPE_BONUS[e.typ] ?? 0;
    if (wantsExperiment && e.typ === "experiment") s += 1.5;
    hits.push([e, s]);
  }
  hits.sort((a, b) => b[1] - a[1]);

  // Nachbarn der besten Treffer mitnehmen: wer "Wedges knusprig" sucht, soll auch den Mechanismus sehen.
  const byId = new Map(items.map((e) => [e.id, e]));
  const seen = new Set(hits.map((h) => h[0].id));
  const top = hits.slice(0, 3);
  for (const [e, s] of top) for (const l of [...e.links, ...e.verlinkt_von]) {
    const n = byId.get(l);
    if (n && !seen.has(l)) { seen.add(l); hits.push([n, Math.min(s * 0.3, 0.9)]); }
  }
  hits.sort((a, b) => b[1] - a[1]);
  return { scores: new Map(hits.map(([e, s]) => [e.id, s])), best: hits[0]?.[0] ?? null, terms };
}
