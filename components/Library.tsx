"use client";
import Link from "next/link";
import { useMemo, useState } from "react";

export interface LibItem {
  id: string; typ: string; titel: string; status: string; pilot: boolean;
  links: string[]; verlinkt_von: string[]; synonyme: string[]; kurz: string | null;
}

const TYPES: [string, string, string][] = [
  ["ziel", "Ziele", "Was will ich erreichen?"],
  ["symptom", "Symptome", "Was ist schiefgelaufen?"],
  ["prozess", "Prozesse", "Was passiert beim Kochen?"],
  ["technik", "Techniken", "Welcher Handgriff hilft?"],
  ["zutat", "Zutaten", "Was tut eine Zutat?"],
  ["stellschraube", "Stellschrauben", "Woran kann ich drehen?"],
  ["welt", "Lebensmittel-Welten", "Wo begegnet mir das?"],
  ["begriff", "Begriffe", "Was heißt das Wort?"],
];
const SING: Record<string, string> = { prozess: "Prozess", ziel: "Ziel", technik: "Technik", symptom: "Symptom", zutat: "Zutat", stellschraube: "Stellschraube", welt: "Welt", begriff: "Begriff" };
const EXAMPLES = ["Wie werden meine Wedges knuspriger?", "Fleisch wird trocken", "Sauce zu dünn", "Brot luftiger", "Gemüse bleibt grün"];
const STOP = new Set("wie wird werden meine mein mache machen ich kann man was warum der die das den dem ein eine einen und oder mit beim bei zu zum zur ist sind nicht noch mehr immer so viel".split(" "));
const norm = (s: string) => s.toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/[^a-z0-9 ]/g, " ");
const stem = (w: string) => (w.length > 5 ? w.slice(0, Math.max(5, w.length - 3)) : w);

/** Einfache Wortsuche mit Stammformen. Später: semantische Suche (pgvector). */
function search(items: LibItem[], q: string): Map<string, number> | null {
  const terms = norm(q).split(/\s+/).filter((w) => w.length > 2 && !STOP.has(w)).map(stem);
  if (!terms.length) return null;
  const byId = new Map(items.map((e) => [e.id, e]));
  const hits: [LibItem, number][] = [];
  for (const e of items) {
    const words = norm([e.titel, ...e.synonyme].join(" ")).split(/\s+/).filter(Boolean);
    let s = 0;
    for (const t of terms) if (words.some((w) => w.startsWith(t) || (t.length >= 5 && w.length >= 4 && t.startsWith(stem(w))))) s++;
    if (s) hits.push([e, s + (e.typ === "ziel" || e.typ === "technik" ? 0.3 : 0) + (e.typ === "symptom" ? 0.2 : 0)]);
  }
  hits.sort((a, b) => b[1] - a[1]);
  const best = hits[0]?.[1] ?? 0;
  const seen = new Set(hits.map((h) => h[0].id));
  for (const [e, s] of [...hits]) if (s >= best - 0.01) for (const l of [...e.links, ...e.verlinkt_von]) {
    const n = byId.get(l);
    if (n && !seen.has(l)) { seen.add(l); hits.push([n, 0.5]); }
  }
  return new Map(hits.map(([e, s]) => [e.id, s]));
}

export default function Library({ items }: { items: LibItem[] }) {
  const [q, setQ] = useState("");
  const [active, setActive] = useState<Set<string>>(new Set());
  const [onlyWritten, setOnlyWritten] = useState(false);
  const res = useMemo(() => (q.trim() ? search(items, q) : null), [items, q]);
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
            <section className="group" key={t}>
              <h3>{name} <small>{g.length} · {sub}</small></h3>
              <div className="grid">
                {g.map((e) => (
                  <Link key={e.id} href={`/eintrag/${e.id}`} className={`cell${isWritten(e) ? "" : " dim"}`}>
                    <span className="t">{e.titel}</span>
                    <span className="m"><i style={{ background: `var(--t-${e.typ})` }} />{SING[e.typ]}{isWritten(e) ? ` · ${e.status}` : " · geplant"}</span>
                  </Link>
                ))}
              </div>
            </section>
          );
        })}
        {!list.length && <p className="count">Nichts gefunden. Versuche ein anderes Wort, z. B. „saftig“ oder „Sauce“.</p>}
      </div>
    </>
  );
}
