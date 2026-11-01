import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

export type Typ = "prozess" | "zutat" | "stellschraube" | "symptom" | "ziel" | "technik" | "welt" | "begriff" | "gericht" | "experiment";

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
}

export interface MasterItem {
  id: string; typ: Typ; titel: string; status: string; pilot: boolean;
  links: string[]; welten: string[]; synonyme: string[]; verlinkt_von: string[];
  visual: { vorlage: string };
}

const root = process.cwd();
let cache: { entries: Map<string, Entry>; master: Map<string, MasterItem> } | null = null;

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
  cache = { entries, master };
  return cache;
}

export const getEntry = (id: string) => load().entries.get(id);
export const getMasterItem = (id: string) => load().master.get(id);
export const allIds = () => [...new Set([...load().master.keys(), ...load().entries.keys()])];

/** Titel einer id, egal ob ausgeschrieben oder nur geplant. */
export function titleOf(id: string) {
  return getEntry(id)?.titel ?? getMasterItem(id)?.titel ?? id;
}
export function typOf(id: string): Typ | undefined {
  return getEntry(id)?.typ ?? getMasterItem(id)?.typ;
}

/** Daten für die Bibliothek: Masterliste plus Status der ausgeschriebenen Einträge. */
export function libraryData() {
  const { master, entries } = load();
  const items = [...master.values()].map((m) => ({
    ...m,
    status: entries.has(m.id) ? entries.get(m.id)!.status : m.status,
    kurz: entries.get(m.id)?.kurz ?? null,
  }));
  for (const e of entries.values()) if (!master.has(e.id)) {
    items.push({ id: e.id, typ: e.typ, titel: e.titel, status: e.status, pilot: false, links: e.links ?? [], welten: e.welten ?? [],
      synonyme: e.synonyme ?? [], verlinkt_von: [], visual: { vorlage: e.visual?.vorlage ?? "keine" }, kurz: e.kurz });
  }
  return items;
}

/** Kurzinfos für Glossar-Popups. */
export function termInfo(id: string) {
  const e = getEntry(id);
  return { id, titel: titleOf(id), kurz: e?.kurz ? e.kurz.replace(/\[\[[a-z0-9-]+\|([^\]]+)\]\]/g, "$1").replace(/\[\[([a-z0-9-]+)\]\]/g, (_, x: string) => titleOf(x)) : null, typ: typOf(id) ?? "begriff", ausgeschrieben: !!e };
}

export type TextPart = { t: "text"; v: string } | { t: "term"; id: string; label: string };
const TERM = /\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]/g;
/** Zerlegt Text mit [[id]] oder [[id|Anzeige]] in Teile. */
export function parseText(s: string): TextPart[] {
  const out: TextPart[] = [];
  let last = 0;
  for (const m of s.matchAll(TERM)) {
    if (m.index! > last) out.push({ t: "text", v: s.slice(last, m.index) });
    out.push({ t: "term", id: m[1], label: m[2] ?? titleOf(m[1]) });
    last = m.index! + m[0].length;
  }
  if (last < s.length) out.push({ t: "text", v: s.slice(last) });
  return out;
}

/** Interaktive Prototypen, bis die Simulationen als Komponenten portiert sind. */
export const PROTOTYPES: Record<string, string> = {
  "steak-grau": "/prototypen/steak-grau.html",
};

export const TYP_NAME: Record<Typ, string> = {
  prozess: "Prozess", ziel: "Ziel", technik: "Technik", symptom: "Symptom", zutat: "Zutat",
  stellschraube: "Stellschraube", welt: "Welt", begriff: "Begriff", gericht: "Gericht", experiment: "Experiment",
};
