"use client";
import Link from "next/link";
import { useMemo, useState } from "react";
import { search } from "@/lib/search";

export interface LibItem {
  id: string; typ: string; titel: string; status: string; pilot: boolean;
  links: string[]; verlinkt_von: string[]; synonyme: string[]; kurz: string | null; welten?: string[];
}

const TYPES: [string, string, string][] = [
  ["ziel", "Ziele", "Was will ich erreichen?"],
  ["gericht", "Gerichte", "Warum funktioniert dieses Rezept?"],
  ["experiment", "Experimente", "Zum Ausprobieren in der Küche"],
  ["symptom", "Symptome", "Was ist schiefgelaufen?"],
  ["prozess", "Prozesse", "Was passiert beim Kochen?"],
  ["technik", "Techniken", "Welcher Handgriff hilft?"],
  ["zutat", "Zutaten", "Was tut eine Zutat?"],
  ["stellschraube", "Stellschrauben", "Woran kann ich drehen?"],
  ["welt", "Lebensmittel-Welten", "Wo begegnet mir das?"],
  ["begriff", "Begriffe", "Was heißt das Wort?"],
];
const SING: Record<string, string> = { prozess: "Prozess", ziel: "Ziel", technik: "Technik", symptom: "Symptom", zutat: "Zutat", stellschraube: "Stellschraube", welt: "Welt", begriff: "Begriff", gericht: "Gericht", experiment: "Experiment" };
const EXAMPLES = ["Wie werden meine Wedges knuspriger?", "Fleisch wird trocken", "Sauce zu dünn", "Rösti", "Experiment für Kinder", "Mayo gerinnt"];
/** Bild für einen Eintrag: das eigene, sonst das seiner Welt. */
function pictureOf(e: LibItem, has: Set<string>): string | null {
  if (has.has(e.id)) return e.id;
  return (e.welten ?? []).find((w) => has.has(w)) ?? null;
}

export default function Library({ items, illus = [] }: { items: LibItem[]; illus?: string[] }) {
  const has = useMemo(() => new Set(illus), [illus]);
  const worlds = items.filter((e) => e.typ === "welt" && has.has(e.id));
  const [q, setQ] = useState("");
  const [active, setActive] = useState<Set<string>>(new Set());
  const [onlyWritten, setOnlyWritten] = useState(false);
  const found = useMemo(() => (q.trim() ? search(items, q) : null), [items, q]);
  const res = found?.scores ?? null;
  const best = (found?.best ?? null) as LibItem | null;
  const isWritten = (e: LibItem) => e.status !== "geplant";

  let list = items.filter((e) => (!active.size || active.has(e.typ)) && (!onlyWritten || isWritten(e)) && (!res || res.has(e.id)));
  if (res) list = [...list].sort((a, b) => res.get(b.id)! - res.get(a.id)!);
  const groups = res ? [["treffer", "Treffer", "sortiert nach Passung"] as [string, string, string]] : TYPES;

  return (
    <>
      <div className="search">
        <label className="mono" htmlFor="q">Suche · Alltagssprache funktioniert</label>
        <input id="q" type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="z. B. Wie werden meine Wedges knuspriger?" autoComplete="off" />
        <div className="examples">{EXAMPLES.map((x) => <button key={x} type="button" onClick={() => setQ(x)}>{x}</button>)}</div>
      </div>
      {best && (
        <Link href={`/eintrag/${best.id}`} className={`bestcard${pictureOf(best, has) ? " pic" : ""}`}>
          {pictureOf(best, has) && (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={`/illustrationen/${pictureOf(best, has)}.webp`} alt="" width={160} height={160} />
          )}
          <span className="mono"><i style={{ background: `var(--t-${best.typ})` }} />Beste Antwort · {SING[best.typ]}</span>
          <strong>{best.titel}</strong>
          {best.kurz && <span className="k">{best.kurz.replace(/\[\[[a-z0-9-]+\|([^\]]+)\]\]/g, "$1").replace(/\[\[([a-z0-9-]+)\]\]/g, (_, id) => id.replace(/-/g, " "))}</span>}
          <span className="go">Eintrag öffnen →</span>
        </Link>
      )}
      {!res && worlds.length > 0 && (
        <nav className="worlds" aria-label="Lebensmittel-Welten">
          <span className="mono">Stöbern nach Welt</span>
          <div className="worlds-row">
            {worlds.map((w) => (
              <Link key={w.id} href={`/eintrag/${w.id}`} className="world">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={`/illustrationen/${w.id}.webp`} alt="" width={120} height={120} loading="lazy" />
                <span>{w.titel}</span>
              </Link>
            ))}
          </div>
        </nav>
      )}
      <div className="typechips" role="group" aria-label="Eintragstyp">
        {TYPES.map(([t, name]) => {
          const n = items.filter((e) => e.typ === t).length;
          if (!n) return null;
          return (
            <button key={t} type="button" className="typechip" aria-pressed={active.has(t)}
              onClick={() => { const s = new Set(active); s.has(t) ? s.delete(t) : s.add(t); setActive(s); }}>
              <i style={{ background: `var(--t-${t})` }} />{name}<span>{n}</span>
            </button>
          );
        })}
      </div>
      <label className="count" style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input type="checkbox" checked={onlyWritten} onChange={(e) => setOnlyWritten(e.target.checked)} />
        Nur ausgeschriebene Einträge · {list.length} von {items.length}
      </label>
      <div className="groups">
        {groups.map(([t, name, sub]) => {
          const g = res ? list : list.filter((e) => e.typ === t);
          if (!g.length) return null;
          return (
            // Geschlossen beim Start; offen bei Suche oder gewähltem Typ. Der key setzt den Zustand bei Filterwechsel zurück.
            <details className="group" key={`${t}-${res ? "s" : ""}-${active.has(t) ? "a" : ""}`} open={!!res || active.has(t)}>
              <summary><h3>{name} <small>{g.length} · {sub}</small></h3></summary>
              <div className="grid">
                {g.map((e) => (
                  <Link key={e.id} href={`/eintrag/${e.id}`} className={`cell${isWritten(e) ? "" : " dim"}`}>
                    <span className="t">{e.titel}</span>
                    <span className="m"><i style={{ background: `var(--t-${e.typ})` }} />{SING[e.typ]}{isWritten(e) ? ` · ${e.status}` : " · geplant"}</span>
                  </Link>
                ))}
              </div>
            </details>
          );
        })}
        {!list.length && <p className="count">Nichts gefunden. Versuche ein anderes Wort, z. B. „saftig“, „Sauce“ oder „Experiment“.</p>}
      </div>
    </>
  );
}
