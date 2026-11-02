"use client";
import { t as ui, type Lang } from "@/lib/i18n";
import { useEffect, useMemo, useRef, useState } from "react";
import { useInView, readMs, tour } from "./useInView";

export interface Mark { c: number; name: string }

/** Zonenfarben laut DESIGN.md (Temperaturzonen). */
function zoneColor(c: number) {
  if (c < 100) return "#8fb8c9";
  if (c < 140) return "#e0ad3a";
  if (c < 190) return "#b4542a";
  return "#3a3633";
}

/**
 * Interaktive Temperaturskala: Schwellen aus den Daten, ein Regler,
 * und eine Zeile, die sagt, was bei dieser Temperatur gerade passiert.
 * Läuft beim Öffnen einmal von kalt nach heiß durch.
 */
export default function TempScale({ marks, title, note, unitMax, lang = "de" }: { marks: Mark[]; title?: string; note?: string; unitMax?: number; lang?: Lang }) {
  const V = ui(lang).vis;
  const sorted = useMemo(() => [...marks].sort((a, b) => a.c - b.c), [marks]);
  const max = unitMax ?? Math.max(120, Math.ceil((sorted[sorted.length - 1]?.c ?? 100) * 1.15 / 10) * 10);
    const lo0 = Math.max(0, Math.floor(((sorted[0]?.c ?? 0) * 0.6) / 10) * 10);
  const [t, setT] = useState(lo0);
  const [touched, setTouched] = useState(false);
  const [run, setRun] = useState(0);
  const root = useRef<HTMLDivElement>(null);
  const seen = useInView(root);

  // Einmaliger Durchlauf beim Sichtbarwerden: an jeder Schwelle so lange halten, wie der Text zum Lesen braucht.
  useEffect(() => {
    if (touched || !seen) return;
    if (typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches) { setT(sorted[Math.floor(sorted.length / 2)]?.c ?? max / 2); return; }
    const stops = [{ v: lo0, hold: readMs(V.below(sorted[0]?.c ?? 0)) },
      ...sorted.map((m, i) => ({ v: m.c, hold: readMs(m.name + (sorted[i + 1]?.name ?? "")) }))];
    return tour(lo0, stops, (v) => setT(Math.round(v)), 1800);
  }, [touched, sorted, max, seen, run]);

  const lo = Math.max(0, Math.floor(((sorted[0]?.c ?? 0) * 0.6) / 10) * 10);
  const span = Math.max(1, max - lo);
  const pct = (c: number) => `${Math.max(0, Math.min(100, ((c - lo) / span) * 100))}%`;
  const reached = sorted.filter((m) => m.c <= t);
  const current = reached[reached.length - 1];
  const next = sorted.find((m) => m.c > t);
  const bands = [lo, 100, 140, 190, max].filter((v, i, a) => v >= lo && v <= max && (i === 0 || v > a[i - 1]));

  return (
    <div className="vis" ref={root}>
      <div className="vis-head"><span className="mono">{title ?? V.thresholds}</span><span className="vis-val">{t} °C</span></div>
      <div className="trk">
      <div className="tbar" role="img" aria-label={lang === "en" ? `Temperature scale from ${lo} to ${max} °C` : `Temperaturskala von ${lo} bis ${max} °C`}>
        {bands.slice(0, -1).map((b, i) => (
          <span key={b} className="tband" style={{ left: pct(b), width: `calc(${pct(bands[i + 1])} - ${pct(b)})`, background: zoneColor(b) }} />
        ))}
        <span className="tfill" style={{ width: pct(t), background: zoneColor(t) }} />
        {sorted.map((m) => (
          <span key={m.name + m.c} className={`ttick${m.c <= t ? " on" : ""}`} style={{ left: pct(m.c), background: m.c <= t ? zoneColor(m.c) : undefined }} />
        ))}
        <span className="tknob" style={{ left: pct(t) }} />
      </div>
      <input type="range" className="trk-input" min={lo} max={max} value={Math.max(lo, t)} aria-label={V.pickTemp}
        onChange={(e) => { setTouched(true); setT(+e.target.value); }} />
      </div>
      <div className="tends"><span className="mono">{lo} °C</span><span className="mono hint">{V.drag}</span><span className="mono">{max} °C</span></div>
      <ol className="tlist">
        {sorted.map((m) => (
          <li key={m.name + m.c} className={m.c <= t ? "on" : ""}>
            <i style={{ background: m.c <= t ? zoneColor(m.c) : undefined }} />
            <span className="tc">{m.c} °C</span><span>{m.name}</span>
          </li>
        ))}
      </ol>
      <p className="vis-status">
        {current ? <>{V.at(t)} <strong>{current.name}</strong>.</> : <>{V.below(sorted[0]?.c ?? 0)}</>}
        {next ? <> {V.from(next.c)} {next.name}.</> : null}
      </p>
      <div className="vis-row">{note && <span className="mono">{note}</span>}<button type="button" className="vis-btn" style={{ marginLeft: "auto" }} onClick={() => { setTouched(false); setT(lo); setRun((r) => r + 1); }}>{V.again}</button></div>
    </div>
  );
}
