import type { Entry } from "@/lib/content";
import TempScale, { type Mark } from "./TempScale";

/** Liest Temperatur-Schwellen aus visual.params, egal in welchem der bekannten Formate. */
export function marksOf(e: Entry): Mark[] {
  const p = (e.visual?.params ?? {}) as Record<string, unknown>;
  const out: Mark[] = [];
  const push = (arr: unknown, nameKey = "name") => {
    if (!Array.isArray(arr)) return;
    for (const m of arr) if (m && typeof m === "object" && "c" in m) out.push({ c: Number((m as { c: number }).c), name: String((m as Record<string, unknown>)[nameKey]) });
  };
  push(p.skala); push(p.schwellen_c); push(p.fette);
  return out;
}

/** Wählt die Grafik-Vorlage für einen Eintrag (außer Prototypen, die die Seite selbst einbettet). */
export default function Visual({ e }: { e: Entry }) {
  const marks = marksOf(e);
  if (!marks.length) return null;
  const p = (e.visual?.params ?? {}) as Record<string, unknown>;
  const title = e.typ === "technik" ? "Die Temperaturen" : e.id === "rauchpunkt" ? "Rauchpunkte im Vergleich" : "Temperatur-Schwellen";
  return <TempScale marks={marks} title={title} note={typeof p.hinweis === "string" ? p.hinweis : undefined} unitMax={e.id === "rauchpunkt" ? 260 : undefined} />;
}

/** Entfernt Glossar-Markierungen für reine Textanzeigen in Grafiken. */
export const plain = (s: string) => s.replace(/\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]/g, (_, id, label) => label ?? id);
