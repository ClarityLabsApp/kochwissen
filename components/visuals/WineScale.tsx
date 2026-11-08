"use client";
import { useState } from "react";
import type { Lang } from "@/lib/i18n";
import { DISHES, WINES, judge, overall, type Verdict } from "@/lib/wein";

const TX = {
  de: { title: "Wein-Waage", wine: "Wein", dish: "Essen", passt: "Passt", geht: "Geht, mit Abstrichen", beisst: "Beißt sich", note: "Ein Regelwerk mit Begründung, kein Naturgesetz: Geschmack und Gewohnheit entscheiden mit." },
  en: { title: "Wine balance", wine: "Wine", dish: "Food", passt: "Works", geht: "Works, with compromises", beisst: "Clashes", note: "A set of reasoned rules, not a law of nature: taste and habit have a say too." },
};
const COL: Record<Verdict, string> = { gut: "#4f7a3a", neutral: "#a89a86", schlecht: "#b4542a" };
const TILT: Record<Verdict, number> = { gut: 0, neutral: 0, schlecht: -9 };

/** Kleine Wippe: links der Wein, rechts das Essen; waagrecht = ausgeglichen, schief = beißt sich. */
function Seesaw({ v, left, right }: { v: Verdict; left: string; right: string }) {
  const c = COL[v];
  return (
    <svg viewBox="0 0 220 64" width="220" height="64" role="img" aria-label={`${left} – ${right}`} className="ww-saw">
      <text x="2" y="12" textAnchor="start" fontSize="10.5" fontFamily="var(--f-mono)" fill="currentColor">{left}</text>
      <text x="218" y="12" textAnchor="end" fontSize="10.5" fontFamily="var(--f-mono)" fill="currentColor">{right}</text>
      <polygon points="104,60 116,60 110,47" fill="#7a5a3a" />
      <g style={{ transform: `rotate(${TILT[v]}deg)`, transformOrigin: "110px 47px", transition: "transform .5s ease" }}>
        <rect x="20" y="44" width="180" height="5" rx="2" fill={c} />
        <circle cx="34" cy="37" r="8" fill={c} opacity={0.85} />
        <circle cx="186" cy="37" r="8" fill={c} opacity={0.85} />
      </g>
    </svg>
  );
}

export default function WineScale({ lang = "de" }: { lang?: Lang }) {
  const L = lang === "en" ? 1 : 0, X = TX[lang];
  const [w, setW] = useState("rot-kraeftig");
  const [d, setD] = useState("steak");
  const wine = WINES.find((x) => x.id === w)!, dish = DISHES.find((x) => x.id === d)!;
  const rules = judge(wine, dish), res = overall(rules);
  const resCol = res === "passt" ? COL.gut : res === "beisst" ? COL.schlecht : "#b8873a";
  return (
    <div className="vis ww">
      <div className="vis-head"><span className="mono">{X.title}</span></div>
      <div className="ww-pick">
        <div><span className="mono">{X.wine}</span>
          <div className="seg" role="group" aria-label={X.wine}>
            {WINES.map((x) => <button key={x.id} type="button" aria-pressed={x.id === w} onClick={() => setW(x.id)} title={x.bsp[L]}>{x.name[L]}</button>)}
          </div>
          <small className="ww-bsp">{wine.bsp[L]}</small>
        </div>
        <div><span className="mono">{X.dish}</span>
          <div className="seg" role="group" aria-label={X.dish}>
            {DISHES.map((x) => <button key={x.id} type="button" aria-pressed={x.id === d} onClick={() => setD(x.id)}>{x.name[L]}</button>)}
          </div>
        </div>
      </div>
      <p className="ww-res" aria-live="polite" style={{ borderColor: resCol }}><strong style={{ color: resCol }}>{X[res]}</strong> · {wine.name[L]} + {dish.name[L]}</p>
      <ul className="ww-rules">
        {rules.map((r) => (
          <li key={r.id} style={{ color: "var(--ink)" }}>
            <Seesaw v={r.v} left={r.left[L]} right={r.right[L]} />
            <span style={{ color: r.v === "neutral" ? "var(--sepia)" : undefined }}>{r.text[L]}</span>
          </li>
        ))}
      </ul>
      <p className="vis-note">{X.note}</p>
    </div>
  );
}
