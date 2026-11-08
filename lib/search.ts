// Suche in Alltagssprache (Deutsch und Englisch): gewichtete Volltextsuche mit Stammformen, Tippfehler-Toleranz,
// Seltenheits-Gewichtung (seltene Wörter zählen mehr), einem Küchen-Wörterbuch (Problem ↔ Ziel) und
// zusätzlichen Suchwörtern je Eintrag (Ursachen, Faustregeln, andere Sprache), die beim ersten Tippen nachgeladen werden.
// Läuft komplett im Browser. Test: npx tsx scripts/suche/test.ts

export interface SearchItem {
  id: string; typ: string; titel: string; synonyme: string[]; kurz: string | null;
  links: string[]; verlinkt_von: string[];
}

const STOP = new Set(("wie wird werden wurde wurden meine mein meinen meiner mache machen macht ich kann koennen man was warum weshalb wieso "
  + "der die das den dem des ein eine einen einer eines und oder mit beim bei zu zum zur ist sind nicht noch mehr immer so viel "
  + "sehr auch nur wenn dann aber wo von vom im in an am auf aus fuer ohne gibt es sich mir mich bekomme bekommen hin richtig "
  + "soll sollte muss mal kein keine schon ganz etwas dabei damit dass da wieder lange nach einem einer einen tag tage tagen stunden "
  + "why is are was were my the a an to of in on for how do does did it its can i you too not won t don doesn isn get gets "
  + "what when with and or at by from be should my me make makes made keep").split(" "));

/** Wörter, die auf ein Problem hindeuten: dann zählen Einträge vom Typ „Problem“ etwas mehr. */
const PROBLEM = new Set(("nicht zu kein keine warum wieso weshalb hilfe problem kaputt misslungen schief retten "
  + "not too won t doesn why help problem fix ruined").split(" "));

export const norm = (s: string) => s.toLowerCase()
  .replace(/\[\[[a-z0-9-]+\|([^\]]+)\]\]/g, "$1").replace(/\[\[([a-z0-9-]+)\]\]/g, (_, id) => id.replace(/-/g, " "))
  .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/é|è|ê/g, "e").replace(/à|â/g, "a")
  .replace(/[^a-z0-9 ]/g, " ");

/** Grobe Stammform für Deutsch und Englisch: häufige Endungen weg (knuspriger → knusprig, Kartoffeln → kartoffel, softening → soft). */
export function stem(w: string) {
  if (w.length <= 4) return w;
  for (const suf of ["ungen", "ening", "ing", "ied", "ies", "erer", "eren", "ern", "ere", "ed", "er", "en", "es", "em", "e", "n", "s"]) {
    if (w.endsWith(suf) && w.length - suf.length >= 4) return w.slice(0, -suf.length);
  }
  return w;
}

/** Wörter in der Küche, die dasselbe meinen oder das Gegenteil eines Ziels beschreiben. */
const THESAURUS: Record<string, string[]> = {
  knusprig: ["kross", "crispy", "crisp", "crunchy", "knackig", "labbrig", "weich", "matschig", "pappig", "lasch", "soggy"],
  saftig: ["trocken", "zaeh", "strohig", "saft", "juicy", "dry"],
  zart: ["zaeh", "hart", "gummig", "tender", "tough", "chewy"],
  luftig: ["fluffig", "locker", "flach", "kompakt", "dicht", "speckig", "schwer", "sitzenbleiben", "aufgehen", "fluffy", "dense", "flat", "rise"],
  cremig: ["glatt", "samtig", "klumpig", "griesig", "koernig", "creamy", "smooth", "grainy", "lumpy"],
  braun: ["braeunen", "kruste", "roesten", "anbraten", "blass", "farbe", "goldbraun", "brown", "browning", "sear", "crust", "grey", "gray", "grau"],
  dick: ["binden", "andicken", "duenn", "waessrig", "flussig", "fluessig", "thicken", "thin", "runny", "watery"],
  gerinnt: ["geronnen", "trennt", "getrennt", "flockt", "griesig", "bricht", "split", "curdle", "curdled", "broken", "separate"],
  klumpig: ["klumpt", "klumpen", "lumpy", "lumps"],
  gruen: ["grau", "oliv", "farbe", "chlorophyll", "green"],
  versuch: ["experiment", "ausprobieren", "kinder", "test", "zeigen", "selber", "kids", "children"],
  scharf: ["schaerfe", "chili", "brennt", "pfeffer", "capsaicin", "spicy", "hot"],
  glace: ["eis", "sorbet", "gefroren", "einfrieren", "tiefkuehl", "gefrier", "ice", "cream", "frozen"],
  haltbar: ["konservieren", "verderben", "schimmel", "aufbewahren", "vorrat", "reste", "kuehlschrank", "leftovers", "fridge", "keep"],
  berg: ["hoehe", "berghuette", "siedepunkt", "dampfkochtopf", "schnellkochtopf", "altitude"],
  herzhaft: ["umami", "wuerzig", "tiefe", "glutamat", "savoury", "savory"],
  bohne: ["kichererbse", "linse", "huelsenfrucht", "beans", "chickpea", "lentil"],
  einsinken: ["sinkt", "eingefallen", "zusammenfallen", "faellt", "zusammengefallen", "zusammen", "einfallen", "sink", "sinks", "collapse"],
  selbermachen: ["selber", "selbst", "herstellen", "hausgemacht", "diy", "homemade"],
  rezept: ["gericht", "kochen", "zubereiten", "recipe"],
  salz: ["salzen", "gesalzen", "versalzen", "salty", "salt"],
  zucker: ["suess", "karamell", "sugar", "sweet"],
  sauer: ["saeure", "saeuerlich", "acidic", "sour", "acid", "sauerkeit"],
  tomate: ["tomaten", "tomatensauce", "sugo", "pelati", "passata", "tomato"],
  reissen: ["risse", "riss", "gerissen", "reisst", "crack", "cracks", "cracked"],
  cheesecake: ["kaesekuchen", "quarkkuchen"],
  altbacken: ["hart", "trocken", "stale", "alt", "retrogradation"],
  schnurren: ["zusammenziehen", "zieht", "schrumpft", "shrinks", "springs"],
  ei: ["eier", "eiweiss", "eigelb", "eischnee", "egg", "eggs"],
  kartoffel: ["kartoffeln", "wedges", "pommes", "roesti", "erdapfel", "potato", "potatoes", "fries", "chips"],
  fleisch: ["steak", "braten", "schnitzel", "huhn", "poulet", "meat"],
  poulet: ["huhn", "haehnchen", "haehnchenbrust", "chicken", "gefluegel", "pouletbrust"],
  pasta: ["nudeln", "spaghetti", "teigwaren", "noodles"],
  mayo: ["mayonnaise", "mayonaise"],
  brot: ["teig", "backen", "kruste", "krume", "bread", "loaf"],
  panade: ["panieren", "breading", "crumb", "coating"],
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
  if (t.length >= 5 && w.includes(t)) return 0.75;           // Wortteil: "tomate" in "tomatensauce", "kruste" in "brotkruste"
  if (sw.length >= 5 && t.startsWith(sw)) return 0.75;
  if (t.length >= 6 && sw.length >= 4 && t.includes(sw) && (t.endsWith(sw) || sw.length >= t.length * 0.45)) return 0.55; // Zusammensetzung: "kaesekuchen" ↔ "kuchen"
  const tol = t.length >= 8 ? 2 : 1;
  if (rawT.length >= 4 && w.length >= 4 && dist(rawT, w, tol) <= tol) return 0.6;   // Tippfehler: "pomes" → pommes
  if (t.length >= 4 && w.length >= 4 && dist(t, sw, tol) <= tol) return 0.45;       // Tippfehler in der Stammform
  return 0;
}

type Field = [string[], number];
interface Indexed { e: SearchItem; fields: Field[]; phrases: string[][] }
const indexCache = new WeakMap<SearchItem[], { extras: Record<string, string> | undefined; ix: Indexed[] }>();
const words = (s: string) => [...new Set(norm(s).split(/\s+/).filter((w) => w.length > 1 && !STOP.has(w)))];
function index(items: SearchItem[], extras?: Record<string, string>) {
  const c = indexCache.get(items);
  if (c && c.extras === extras) return c.ix;
  const ix = items.map((e) => ({ e, fields: [
    [words(e.titel), 3], [words(e.synonyme.join(" ")), 2.5], [words(e.kurz ?? ""), 1], [words(extras?.[e.id] ?? ""), 0.8],
  ] as Field[], phrases: [e.titel, ...e.synonyme].map(words) }));
  indexCache.set(items, { extras, ix });
  return ix;
}

const TYPE_BONUS: Record<string, number> = { ziel: 0.4, symptom: 0.35, gericht: 0.3, experiment: 0.25, labor: 0.3, technik: 0.2, prozess: 0.15 };

export interface SearchResult { scores: Map<string, number>; best: SearchItem | null; terms: string[] }

/** Sucht in den Einträgen. `extras`: zusätzliche Suchwörter je id (optional, siehe /suche-index/<lang>). */
export function search(items: SearchItem[], q: string, extras?: Record<string, string>): SearchResult | null {
  const all = norm(q).split(/\s+/).filter(Boolean);
  const raw = [...new Set(all.filter((w) => w.length > 1 && !STOP.has(w)))];
  if (!raw.length) return null;
  const terms = raw.map(stem);
  const isProblem = all.some((w) => PROBLEM.has(w));
  const wantsExperiment = terms.some((t) => ["experiment", "versuch", "ausprobier", "kinder", "kind", "kid", "children"].some((k) => t.startsWith(k)));
  const wantsLab = terms.some((t) => ["selb", "hausgemacht", "herstell", "homemade", "diy"].some((k) => t.startsWith(k)));
  const ix = index(items, extras);

  // 1. Für jedes Suchwort und jeden Eintrag: beste Übereinstimmung über alle Felder.
  const per: { e: SearchItem; b: number[]; strong: number }[] = [];
  const df = terms.map(() => 0);
  for (const { e, fields, phrases } of ix) {
    const b = terms.map(() => 0); let strong = 0;
    for (const [ti, t] of terms.entries()) {
      const alts = EXPAND.get(t);
      for (const [fi, [ws, weight]] of fields.entries()) for (const w of ws) {
        let m = wordMatch(t, w, raw[ti]) * weight;
        if (alts && m < weight * 0.8) for (const a of alts) m = Math.max(m, wordMatch(a, w) * weight * 0.7);
        if (m > b[ti]) { b[ti] = m; if (fi < 2 && m >= weight * 0.7) strong |= 1 << ti; }
      }
      if (b[ti] > 0) df[ti]++;
    }
    // Alle Suchwörter in einem einzigen Titel oder Synonym ("Tomaten Säure") zählen extra.
    const phrase = terms.length > 1 && phrases.some((ws) => terms.every((t, i) => ws.some((w) => wordMatch(t, w, raw[i]) >= 0.7)));
    if (b.some((x) => x > 0)) per.push({ e, b, strong: phrase ? -1 : strong });
  }
  if (!per.length) return { scores: new Map(), best: null, terms };

  // 2. Seltene Wörter zählen mehr ("cheesecake" mehr als "sauce"), gemittelt auf 1.
  const N = items.length;
  const idf = df.map((d) => Math.log(1 + N / Math.max(1, d)));
  const mean = idf.reduce((a, c) => a + c, 0) / idf.length;
  const wgt = idf.map((x) => x / mean);

  const hits: [SearchItem, number][] = [];
  for (const { e, b, strong } of per) {
    let s = 0, cov = 0;
    for (let i = 0; i < terms.length; i++) if (b[i] > 0) { s += b[i] * wgt[i]; cov += wgt[i]; }
    const share = cov / terms.length;                       // gewichteter Anteil der getroffenen Suchwörter
    s *= 0.3 + 0.7 * share * share;                          // alle Suchwörter getroffen zählt deutlich mehr
    if (strong === -1) s += 2;                                             // alles in einem Titel oder Synonym
    else if (terms.length > 1 && strong === (1 << terms.length) - 1) s += 1.2;   // alles im Titel oder in den Synonymen
    s += TYPE_BONUS[e.typ] ?? 0;
    if (isProblem && e.typ === "symptom") s += 0.6;
    if (wantsExperiment && e.typ === "experiment") s += 1.5;
    if (wantsLab && e.typ === "labor") s += 1.5;
    hits.push([e, s]);
  }
  hits.sort((a, b) => b[1] - a[1]);

  // 3. Nachbarn der besten Treffer mitnehmen: wer "Wedges knusprig" sucht, soll auch den Mechanismus sehen.
  const byId = new Map(items.map((e) => [e.id, e]));
  const seen = new Set(hits.map((h) => h[0].id));
  for (const [e, s] of hits.slice(0, 3)) for (const l of [...e.links, ...e.verlinkt_von]) {
    const n = byId.get(l);
    if (n && !seen.has(l)) { seen.add(l); hits.push([n, Math.min(s * 0.3, 0.9)]); }
  }
  hits.sort((a, b) => b[1] - a[1]);
  return { scores: new Map(hits.map(([e, s]) => [e.id, s])), best: hits[0]?.[0] ?? null, terms };
}
