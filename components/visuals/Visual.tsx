import type { Entry } from "@/lib/content";
import { getEntry, getMasterItem, titleOf, typOf } from "@/lib/content";
import TempScale, { type Mark } from "./TempScale";
import PanTest from "./PanTest";
import DotNet, { type NetNode } from "./DotNet";
import ParticleSim, { type Preset } from "./ParticleSim";
import Spectrum from "./Spectrum";
import MaillardSim from "./MaillardSim";

// Muss hier stehen: Funktionen aus Client-Modulen sind auf dem Server nicht aufrufbar.
const SIMS = new Set<string>(["emulsion", "osmose", "pektin-abbau", "reduktion", "hefegaerung", "chemische-lockerung", "waermeleitung", "schaumbildung", "diffusion", "zucker-kristallisation", "leidenfrost", "gelbildung-pektin", "chlorophyll-farbe", "eiweiss-denaturierung", "glutenbildung", "karamellisierung"]);
const hasSim = (id: string): id is Preset => SIMS.has(id);

/** Liest Temperatur-Schwellen aus visual.params, egal in welchem der bekannten Formate. */
export function marksOf(e: Entry): Mark[] {
  const p = (e.visual?.params ?? {}) as Record<string, unknown>;
  const out: Mark[] = [];
  const push = (arr: unknown) => {
    if (!Array.isArray(arr)) return;
    for (const m of arr) if (m && typeof m === "object" && "c" in m) out.push({ c: Number((m as { c: number }).c), name: String((m as Record<string, unknown>).name) });
  };
  push(p.skala); push(p.schwellen_c); push(p.fette);
  return out;
}

const TYPE_COLOR: Record<string, string> = {
  prozess: "#2f6f73", zutat: "#b8873a", stellschraube: "#7a5a3a", symptom: "#b4542a", ziel: "#6b3a1e", technik: "#8c2f2a", welt: "#3a3633", begriff: "#7fb0ac", gericht: "#9a6b2f", experiment: "#4f7a3a",
};
const short = (s: string, n = 20) => {
  const t = s.replace(/\s*\(.*?\)\s*/g, " ").replace(/:.*$/, "").trim();
  return t.length > n ? t.slice(0, n - 1).trimEnd() + "…" : t;
};
const node = (id: string, label?: string): NetNode => ({ id, label: short(label ?? titleOf(id)), full: label ?? titleOf(id), color: TYPE_COLOR[typOf(id) ?? "begriff"], href: `/eintrag/${id}` });
/** Alle Verweise eines Eintrags, ausgeschrieben oder aus der Masterliste. */
const refsOf = (id: string) => {
  const e = getEntry(id), m = getMasterItem(id);
  return new Set([...(e?.links ?? []), ...(e?.stellschrauben ?? []).map((s) => s.id), ...(e?.hebel ?? []), ...(m?.links ?? [])]);
};

/** Wählt die Grafik-Vorlage für einen Eintrag (außer Prototypen, die die Seite selbst einbettet). */
export default function Visual({ e }: { e: Entry }) {
  const p = (e.visual?.params ?? {}) as Record<string, unknown>;
  const blocks: React.ReactNode[] = [];

  if (e.id === "maillard-reaktion") blocks.push(<MaillardSim key="maillard" />);
  if (hasSim(e.id)) blocks.push(<ParticleSim key="sim" preset={e.id} />);

  if (e.typ === "symptom" && e.visual?.vorlage === "pfannentest") {
    const v = p.variante === "backblech" || p.variante === "fritteuse" ? p.variante : "pfanne";
    blocks.push(<PanTest key="pan" variant={v} />);
  }

  if (e.typ === "ziel" && e.hebel?.length) {
    const left = e.hebel.map((h) => node(h));
    const techs = [...new Set([...(e.links ?? []), ...(getMasterItem(e.id)?.links ?? [])])].filter((id) => typOf(id) === "technik");
    const right = techs.map((t) => node(t));
    const edges: [string, string][] = [];
    // Direkt verbunden, oder über einen Vorgang dazwischen (Technik → Prozess → Hebel).
    const linked = (t: string, h: string) => {
      const rt = refsOf(t);
      if (rt.has(h) || refsOf(h).has(t)) return true;
      return [...rt].some((mid) => typOf(mid) === "prozess" && refsOf(mid).has(h));
    };
    for (const t of techs) for (const h of e.hebel) if (linked(t, h)) edges.push([h, t]);
    if (right.length) blocks.push(<DotNet key="net" title={`Hebel und Techniken für „${e.titel}“`} leftTitle="Hebel" rightTitle="Techniken" left={left} right={right} edges={edges} />);
  }

  if (e.typ === "zutat" && e.rolle?.length) {
    const left = e.rolle.map((r, i) => ({ id: `r${i}`, label: short(r.rolle, 20), full: r.rolle, color: TYPE_COLOR.zutat }));
    const procs = [...new Set(e.rolle.map((r) => r.prozess))];
    const right = procs.map((id) => node(id));
    const edges = e.rolle.map((r, i) => [`r${i}`, r.prozess] as [string, string]);
    blocks.push(<DotNet key="net" title={`Was ${e.titel.split(" ")[0]} tut`} leftTitle="Rolle" rightTitle="Vorgang" left={left} right={right} edges={edges} />);
  }

  if (e.visual?.vorlage === "skala" && typeof p.links === "string" && typeof p.rechts === "string") {
    const colors = e.id === "anthocyan-farbe" ? ["#b8325a", "#7a3e8c", "#3f5fa8", "#3f8a7a"]
      : e.id === "feuchtigkeit" || e.id === "luftfeuchte-ofen" ? ["#8fb8c9", "#e0ad3a", "#b4542a"]
      : ["#e6d3ae", "#b8873a", "#6b3a1e"];
    blocks.push(<Spectrum key="spec" title={e.titel} left={p.links} mid={typeof p.mitte === "string" ? p.mitte : undefined} right={p.rechts} colors={colors} />);
  }

  const marks = marksOf(e);
  if (marks.length) {
    const title = e.typ === "technik" ? "Die Temperaturen" : e.id === "rauchpunkt" ? "Rauchpunkte im Vergleich" : "Temperatur-Schwellen";
    blocks.push(<TempScale key="temp" marks={marks} title={title} note={typeof p.hinweis === "string" ? p.hinweis : undefined} unitMax={e.id === "rauchpunkt" ? 260 : undefined} />);
  }

  return blocks.length ? <>{blocks}</> : null;
}

/** Entfernt Glossar-Markierungen für reine Textanzeigen in Grafiken. */
export const plain = (s: string) => s.replace(/\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]/g, (_, id, label) => label ?? id);
