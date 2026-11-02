import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { existsSync } from "node:fs";
import type { Lang } from "./i18n";

export type Typ = "prozess" | "zutat" | "stellschraube" | "symptom" | "ziel" | "technik" | "welt" | "begriff" | "gericht" | "experiment" | "labor";

export interface Ursache { titel: string; warum: string; fix: string[]; haeufigkeit?: 1 | 2 | 3; prinzip?: string }
export interface DiagnoseKnoten { frage?: string; antworten?: [string, string][]; ursache?: number }

export interface Entry {
  id: string; typ: Typ; titel: string; status: string; kurz: string;
  synonyme?: string[]; schwierigkeit?: string;
  bild_im_kopf?: string; was_passiert?: string; warum_wichtig?: string; bedeutung?: string;
  faustregeln?: string[]; stellschrauben?: { id: string; wirkung: string }[];
  typische_fehler?: string[]; mythos?: { behauptung: string; richtig: string };
  praxis?: { welt: string; text: string; aroma?: string[] }[];
  visual?: { vorlage: string; ebenen?: { name: string; massstab: string }[]; params?: Record<string, unknown>; illustration?: string };
  links?: string[]; welten?: string[]; quellen?: { titel: string; url?: string; stelle?: string }[];
  ursachen?: Ursache[]; diagnose?: Record<string, DiagnoseKnoten>;
  hebel?: string[]; schritte?: string[]; wirkt_auf?: string[]; rolle?: { rolle: string; prozess: string }[];
  schluesselmomente?: { schritt: string; warum: string; prinzip?: string }[];
  material?: string[]; beobachtung?: string; erklaerung?: string; dauer?: string; sicherheit?: string;
  haltbarkeit?: string; verwendung?: string[]; ergebnis?: string;
}

export interface MasterItem {
  id: string; typ: Typ; titel: string; status: string; pilot: boolean;
  links: string[]; welten: string[]; synonyme: string[]; verlinkt_von: string[];
  visual: { vorlage: string };
}

const root = process.cwd();
let cache: { entries: Map<string, Entry>; master: Map<string, MasterItem>; en: Map<string, Partial<Entry>> } | null = null;

function load() {
  if (cache) return cache;
  const dir = join(root, "content/entries");
  const entries = new Map<string, Entry>();
  for (const f of readdirSync(dir).filter((f) => f.endsWith(".json"))) {
    const e = JSON.parse(readFileSync(join(dir, f), "utf8")) as Entry;
    entries.set(e.id, e);
  }
  const masterList = JSON.parse(readFileSync(join(root, "content/master-list.json"), "utf8")).eintraege as MasterItem[];
  const master = new Map(masterList.map((m) => [m.id, m]));
  // Englische Übersetzungen: nur Textfelder, sie liegen über dem deutschen Eintrag
  const en = new Map<string, Partial<Entry>>();
  const enDir = join(root, "content/en/entries");
  if (existsSync(enDir)) for (const f of readdirSync(enDir).filter((f) => f.endsWith(".json"))) {
    const e = JSON.parse(readFileSync(join(enDir, f), "utf8")) as Partial<Entry>;
    en.set(f.replace(/\.json$/, ""), e);
  }
  cache = { entries, master, en };
  return cache;
}

/** Eintrag in der gewünschten Sprache. Englisch: Übersetzung über dem deutschen Original, fehlende Felder bleiben deutsch. */
export function getEntry(id: string, lang: Lang = "de"): Entry | undefined {
  const de = load().entries.get(id);
  if (!de || lang === "de") return de;
  const en = load().en.get(id);
  return en ? ({ ...de, ...en, visual: en.visual ? { ...de.visual, ...en.visual, params: { ...(de.visual?.params ?? {}), ...(en.visual.params ?? {}) } } as Entry["visual"] : de.visual } as Entry) : de;
}
export const isTranslated = (id: string) => load().en.has(id);
export const getMasterItem = (id: string) => load().master.get(id);
export const allIds = () => [...new Set([...load().master.keys(), ...load().entries.keys()])];

/** Titel einer id, egal ob ausgeschrieben oder nur geplant. */
export function titleOf(id: string, lang: Lang = "de") {
  return (lang === "en" ? load().en.get(id)?.titel : undefined) ?? getEntry(id)?.titel ?? getMasterItem(id)?.titel ?? id;
}
export function typOf(id: string): Typ | undefined {
  return getEntry(id)?.typ ?? getMasterItem(id)?.typ;
}

/** Daten für die Bibliothek: Masterliste plus Status der ausgeschriebenen Einträge. */
export function libraryData(lang: Lang = "de") {
  const { master, entries, en } = load();
  const tr = (id: string) => (lang === "en" ? en.get(id) : undefined);
  const items = [...master.values()].map((m) => ({
    ...m,
    titel: tr(m.id)?.titel ?? m.titel,
    synonyme: tr(m.id)?.synonyme ?? m.synonyme,
    status: entries.has(m.id) ? entries.get(m.id)!.status : m.status,
    kurz: tr(m.id)?.kurz ?? entries.get(m.id)?.kurz ?? null,
  }));
  for (const e of entries.values()) if (!master.has(e.id)) {
    items.push({ id: e.id, typ: e.typ, titel: tr(e.id)?.titel ?? e.titel, status: e.status, pilot: false, links: e.links ?? [], welten: e.welten ?? [],
      synonyme: tr(e.id)?.synonyme ?? e.synonyme ?? [], verlinkt_von: [], visual: { vorlage: e.visual?.vorlage ?? "keine" }, kurz: tr(e.id)?.kurz ?? e.kurz });
  }
  return items;
}

/** Kurzinfos für Glossar-Popups. */
export function termInfo(id: string, lang: Lang = "de") {
  const e = getEntry(id, lang);
  return { id, titel: titleOf(id, lang), kurz: e?.kurz ? plainText(e.kurz, lang) : null, typ: typOf(id) ?? "begriff", ausgeschrieben: !!e };
}

export type TextPart = { t: "text"; v: string } | { t: "term"; id: string; label: string };
const TERM = /\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]/g;
/** Zerlegt Text mit [[id]] oder [[id|Anzeige]] in Teile. */
export function parseText(s: string, lang: Lang = "de"): TextPart[] {
  const out: TextPart[] = [];
  let last = 0;
  for (const m of s.matchAll(TERM)) {
    if (m.index! > last) out.push({ t: "text", v: s.slice(last, m.index) });
    out.push({ t: "term", id: m[1], label: m[2] ?? titleOf(m[1], lang) });
    last = m.index! + m[0].length;
  }
  if (last < s.length) out.push({ t: "text", v: s.slice(last) });
  return out;
}

/** Interaktive Prototypen, bis die Simulationen als Komponenten portiert sind. */
export const PROTOTYPES: Record<string, string> = {
};

export const TYP_NAME: Record<Typ, string> = {
  prozess: "Prozess", ziel: "Ziel", technik: "Technik", symptom: "Symptom", zutat: "Zutat",
  stellschraube: "Stellschraube", welt: "Welt", begriff: "Begriff", gericht: "Gericht", experiment: "Experiment", labor: "Labor",
};

/* ---------- Lernpfade ---------- */
export interface Pfad { id: string; titel: string; kurz: string; fuer: string; dauer: string; schritte: { id: string; warum: string }[]; quiz?: { frage: string; antworten: string[]; richtig: number; erklaerung: string; eintrag: string }[] }
const pfadCache: Partial<Record<Lang, Pfad[]>> = {};
export function lernpfade(lang: Lang = "de"): Pfad[] {
  if (!pfadCache[lang]) {
    const de = JSON.parse(readFileSync(join(root, "content/lernpfade.json"), "utf8")) as Pfad[];
    const enFile = join(root, "content/en/lernpfade.json");
    if (lang === "en" && existsSync(enFile)) {
      const en = JSON.parse(readFileSync(enFile, "utf8")) as Pfad[];
      pfadCache.en = de.map((p) => { const e = en.find((x) => x.id === p.id); return e ? { ...p, ...e } : p; });
    } else pfadCache[lang] = de;
  }
  return pfadCache[lang]!;
}
export const getPfad = (id: string, lang: Lang = "de") => lernpfade(lang).find((p) => p.id === id);
/** Klartext ohne Glossar-Markierungen, für Listen und Popups. */
export const plainText = (s: string, lang: Lang = "de") => s.replace(/\[\[[a-z0-9-]+\|([^\]]+)\]\]/g, "$1").replace(/\[\[([a-z0-9-]+)\]\]/g, (_, id: string) => titleOf(id, lang));
