"use client";
import type { Lang } from "@/lib/i18n";
import Link from "next/link";
import { useState } from "react";

export interface NetNode { id: string; label: string; color: string; href?: string; full?: string }

/**
 * Punktnetz: links die Hebel (oder Rollen), rechts die Techniken (oder Prozesse),
 * dazwischen Verbindungen. Antippen hebt alle Verbindungen eines Punktes hervor.
 */
/** Zwei Zeilen à etwa n Zeichen; erst danach wird gekürzt. */
function wrap(s: string, n = 22): string[] {
  const words = s.split(" "); const lines: string[] = [""];
  for (const w of words) { const cur = lines[lines.length - 1]; if (!cur || (cur + " " + w).length <= n) lines[lines.length - 1] = cur ? cur + " " + w : w; else lines.push(w); }
  if (lines.length > 2) { lines.length = 2; lines[1] = lines[1].replace(/\s*\S*$/, "") + "…"; }
  return lines.map((l) => (l.length > n + 4 ? l.slice(0, n + 3) + "…" : l));
}

export default function DotNet({ title, leftTitle, rightTitle, left, right, edges, lang = "de" }: {
  title: string; leftTitle: string; rightTitle: string; left: NetNode[]; right: NetNode[]; edges: [string, string][]; lang?: Lang;
}) {
  const [sel, setSel] = useState<string | null>(null);
  const rowH = 40, top = 30;
  const H = top + Math.max(left.length, right.length) * rowH + 6;
  const W = 360, xl = 14, xr = W - 14;
  const yL = (i: number) => top + i * rowH + rowH / 2 + (Math.max(0, right.length - left.length) * rowH) / 2;
  const yR = (i: number) => top + i * rowH + rowH / 2 + (Math.max(0, left.length - right.length) * rowH) / 2;
  const li = Object.fromEntries(left.map((n, i) => [n.id, i]));
  const ri = Object.fromEntries(right.map((n, i) => [n.id, i]));
  const active = (a: string, b: string) => !sel || sel === a || sel === b;
  const connected = new Set(sel ? edges.filter(([a, b]) => a === sel || b === sel).flat() : []);
  const selNode = [...left, ...right].find((n) => n.id === sel);

  return (
    <div className="vis">
      <div className="vis-head"><span className="mono">{title}</span>{sel && <button type="button" className="vis-btn" onClick={() => setSel(null)}>{lang === "en" ? "Show all" : "Alle zeigen"}</button>}</div>
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${leftTitle} ${lang === "en" ? "and" : "und"} ${rightTitle}`}>
        <text x={xl} y={16} fontFamily="JetBrains Mono, monospace" fontSize="10" fill="#7a5a3a" letterSpacing="1">{leftTitle.toUpperCase()}</text>
        <text x={xr} y={16} textAnchor="end" fontFamily="JetBrains Mono, monospace" fontSize="10" fill="#7a5a3a" letterSpacing="1">{rightTitle.toUpperCase()}</text>
        {edges.map(([a, b]) => {
          if (li[a] === undefined || ri[b] === undefined) return null;
          const y1 = yL(li[a]), y2 = yR(ri[b]), x1 = W / 2 - 32, x2 = W / 2 + 32;
          const on = active(a, b);
          return <path key={a + b} d={`M${x1} ${y1} C${W / 2} ${y1} ${W / 2} ${y2} ${x2} ${y2}`} fill="none"
            stroke={on && sel ? "#b4542a" : "#b89a6a"} strokeWidth={on && sel ? 2.4 : 1.5} opacity={on ? 1 : 0.25} style={{ transition: "all .25s" }} />;
        })}
        {left.map((n, i) => {
          const dim = sel && !connected.has(n.id) && sel !== n.id;
          return (
            <g key={n.id} onClick={() => setSel(sel === n.id ? null : n.id)} style={{ cursor: "pointer", transition: "opacity .25s" }} opacity={dim ? 0.3 : 1}>
              <rect x={0} y={yL(i) - rowH / 2 + 2} width={W / 2 - 34} height={rowH - 4} fill="transparent" />
              <text x={W / 2 - 44} y={yL(i) + 4} textAnchor="end" fontFamily="Newsreader, Georgia, serif" fontSize="12.5" fill="#2b2118">{wrap(n.full ?? n.label).map((l, k, all) => <tspan key={k} x={W / 2 - 44} dy={k === 0 ? (all.length - 1) * -7 : 14}>{l}</tspan>)}</text>
              <circle cx={W / 2 - 32} cy={yL(i)} r={sel === n.id ? 8 : 6} fill={n.color} stroke="#2b2118" strokeWidth="1" />
            </g>
          );
        })}
        {right.map((n, i) => {
          const dim = sel && !connected.has(n.id) && sel !== n.id;
          return (
            <g key={n.id} onClick={() => setSel(sel === n.id ? null : n.id)} style={{ cursor: "pointer", transition: "opacity .25s" }} opacity={dim ? 0.3 : 1}>
              <rect x={W / 2 + 34} y={yR(i) - rowH / 2 + 2} width={W / 2 - 34} height={rowH - 4} fill="transparent" />
              <circle cx={W / 2 + 32} cy={yR(i)} r={sel === n.id ? 8 : 6} fill={n.color} stroke="#2b2118" strokeWidth="1" />
              <text x={W / 2 + 44} y={yR(i) + 4} fontFamily="Newsreader, Georgia, serif" fontSize="12.5" fill="#2b2118">{wrap(n.full ?? n.label).map((l, k, all) => <tspan key={k} x={W / 2 + 44} dy={k === 0 ? (all.length - 1) * -7 : 14}>{l}</tspan>)}</text>
            </g>
          );
        })}
      </svg>
      <p className="vis-status">
        {selNode ? <>{selNode.full ?? selNode.label}{selNode.href && <> · <Link href={selNode.href}>{lang === "en" ? "open" : "öffnen"}</Link></>}</> : <>{lang === "en" ? "Tap a dot to see its connections." : "Tippe einen Punkt an, um seine Verbindungen zu sehen."}</>}
      </p>
    </div>
  );
}
