"use client";
import Link from "next/link";
import { useMemo, useState } from "react";
import { href, t, type Lang } from "@/lib/i18n";
import type { LibItem } from "./Library";

/**
 * Die Bibliothek als Molekül: Prozesse im Kern, innen womit man sie auslöst (Zutaten, Techniken, Stellschrauben),
 * außen wofür man sie braucht (Ziele, Probleme, Gerichte, Labor, Experimente). Antippen zeigt Beispiele.
 */
type Atom = { typ: string; ring: 0 | 1 | 2; ang: number; ex: string[] };
const ATOMS: Atom[] = [
  { typ: "prozess", ring: 0, ang: 0, ex: ["maillard-reaktion", "emulsion", "glutenbildung", "staerkeverkleisterung", "eiweiss-denaturierung"] },
  { typ: "zutat", ring: 1, ang: 205, ex: ["butter", "eigelb", "natron", "salz", "zucker"] },
  { typ: "technik", ring: 1, ang: 325, ex: ["anbraten", "blanchieren", "rueckwaerts-garen", "montieren", "dehnen-falten"] },
  { typ: "stellschraube", ring: 1, ang: 85, ex: ["temperatur", "zeit", "ph-wert", "salzgehalt", "feuchtigkeit"] },
  { typ: "ziel", ring: 2, ang: 282, ex: ["knusprig", "saftig", "zart", "luftig", "cremig"] },
  { typ: "symptom", ring: 2, ang: 12, ex: ["steak-grau", "wedges-nicht-knusprig", "mayo-gerinnt", "kuchen-sinkt-ein", "sauce-zu-duenn"] },
  { typ: "gericht", ring: 2, ang: 228, ex: ["g-roesti", "g-kaesefondue", "g-risotto", "g-zopf", "g-steak"] },
  { typ: "labor", ring: 2, ang: 165, ex: ["l-butter", "l-joghurt", "l-sauerteig", "l-backpulver", "l-bratbutter"] },
  { typ: "experiment", ring: 2, ang: 112, ex: ["x-rotkohl-indikator", "x-hefe-ballon", "x-butter-schuetteln", "x-tanzender-tropfen", "x-glace-beutel"] },
];
const BONDS: [string, string][] = [["prozess", "zutat"], ["prozess", "technik"], ["prozess", "stellschraube"], ["prozess", "experiment"],
  ["zutat", "labor"], ["zutat", "gericht"], ["technik", "gericht"], ["technik", "ziel"], ["technik", "symptom"], ["stellschraube", "symptom"], ["stellschraube", "experiment"]];
const R = [0, 84, 140], CX = 180, CY = 172;

export default function Molecule({ items, lang = "de", onAll }: { items: LibItem[]; lang?: Lang; onAll: (typ: string) => void }) {
  const T = t(lang), M = T.mol, ln = (p: string) => href(lang, p);
  const [sel, setSel] = useState("prozess");
  const byId = useMemo(() => new Map(items.map((e) => [e.id, e])), [items]);
  const count = (typ: string) => items.filter((e) => e.typ === typ).length;
  const pos = useMemo(() => Object.fromEntries(ATOMS.map((a) => {
    const rad = (a.ang * Math.PI) / 180, n = items.filter((e) => e.typ === a.typ).length;
    return [a.typ, { x: CX + Math.cos(rad) * R[a.ring], y: CY + Math.sin(rad) * R[a.ring], r: 6 + 3.1 * Math.sqrt(Math.max(1, n)), n }];
  })), [items]);
  const near = new Set([sel, ...BONDS.filter(([a, b]) => a === sel || b === sel).flat()]);
  const atom = ATOMS.find((a) => a.typ === sel)!;
  const examples = atom.ex.map((id) => byId.get(id)).filter(Boolean) as LibItem[];

  return (
    <>
      <section className="mol" aria-label={M.label}>
        <div className="mol-head"><span className="mono">{M.tap}</span></div>
        <svg viewBox="0 0 360 360" role="group" aria-label={M.label}>
          {BONDS.map(([a, b]) => {
            const on = a === sel || b === sel;
            return <line key={a + b} className={`bond${on ? " hi" : " lo"}`} x1={pos[a].x} y1={pos[a].y} x2={pos[b].x} y2={pos[b].y} />;
          })}
          {ATOMS.map((a, i) => {
            const p = pos[a.typ], below = p.y + p.r + 15 < 352;
            return (
              <g key={a.typ} className={`atom${a.typ === sel ? " sel" : ""}${near.has(a.typ) ? "" : " lo"}`} tabIndex={0} role="button"
                aria-pressed={a.typ === sel} aria-label={`${T.types[a.typ][0]}, ${M.entries(p.n)}`}
                onClick={() => setSel(a.typ)} onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setSel(a.typ); } }}>
                <g className="float" style={{ animationDelay: `${-i * 0.7}s` }}>
                  <circle className="halo" cx={p.x} cy={p.y} r={p.r + 6} />
                  <circle className="core" cx={p.x} cy={p.y} r={p.r} style={{ fill: `var(--t-${a.typ})` }} />
                  <circle cx={p.x - p.r * 0.35} cy={p.y - p.r * 0.35} r={p.r * 0.28} fill="rgba(255,248,234,.28)" />
                  <text className="n" x={p.x} y={p.y}>{p.n}</text>
                  <text className="lbl" x={p.x} y={below ? p.y + p.r + 15 : p.y - p.r - 7}>{T.types[a.typ][0]}</text>
                </g>
              </g>
            );
          })}
        </svg>
        <div className="mol-legend"><span className="mono">● {M.core}</span><span className="mono">{M.inner}</span><span className="mono">{M.outer}</span></div>
      </section>
      <section className="mol-panel" style={{ ["--c" as string]: `var(--t-${sel})` }} aria-live="polite">
        <h3>{T.types[sel][0]} <small>{M.entries(count(sel))}</small></h3>
        <p className="q">{T.types[sel][1]}</p>
        <ul>{examples.map((e) => <li key={e.id}><Link href={ln(`/eintrag/${e.id}`)}>{e.titel}</Link></li>)}</ul>
        <button type="button" className="mol-all" onClick={() => onAll(sel)}>{M.all(count(sel), T.types[sel][0])}</button>
      </section>
    </>
  );
}
