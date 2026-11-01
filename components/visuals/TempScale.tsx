"use client";
import { useEffect, useMemo, useState } from "react";

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
export default function TempScale({ marks, title, note, unitMax }: { marks: Mark[]; title?: string; note?: string; unitMax?: number }) {
  const sorted = useMemo(() => [...marks].sort((a, b) => a.c - b.c), [marks]);
  const max = unitMax ?? Math.max(120, Math.ceil((sorted[sorted.length - 1]?.c ?? 100) * 1.15 / 10) * 10);
    const lo0 = Math.max(0, Math.floor(((sorted[0]?.c ?? 0) * 0.6) / 10) * 10);
  const [t, setT] = useState(lo0);
  const [touched, setTouched] = useState(false);

  // Einmaliger Durchlauf beim Laden, danach steuert der Regler.
  useEffect(() => {
    if (touched) return;
    if (typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches) { setT(sorted[Math.floor(sorted.length / 2)]?.c ?? max / 2); return; }
    let raf = 0; const start = performance.now(); const target = sorted[sorted.length - 1]?.c ?? max * 0.8;
    const step = (now: number) => {
      const p = Math.min(1, (now - start) / 3200);
      setT(Math.round(lo0 + (target - lo0) * (1 - Math.pow(1 - p, 3))));
      if (p < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [touched, sorted, max]);

  const lo = Math.max(0, Math.floor(((sorted[0]?.c ?? 0) * 0.6) / 10) * 10);
  const span = Math.max(1, max - lo);
  const pct = (c: number) => `${Math.max(0, Math.min(100, ((c - lo) / span) * 100))}%`;
  const reached = sorted.filter((m) => m.c <= t);
  const current = reached[reached.length - 1];
  const next = sorted.find((m) => m.c > t);
  const bands = [lo, 100, 140, 190, max].filter((v, i, a) => v >= lo && v <= max && (i === 0 || v > a[i - 1]));

  return (
    <div className="vis">
      <div className="vis-head"><span className="mono">{title ?? "Temperatur-Schwellen"}</span><span className="vis-val">{t} °C</span></div>
      <div className="tbar" role="img" aria-label={`Temperaturskala von ${lo} bis ${max} °C`}>
        {bands.slice(0, -1).map((b, i) => (
          <span key={b} className="tband" style={{ left: pct(b), width: `calc(${pct(bands[i + 1])} - ${pct(b)})`, background: zoneColor(b) }} />
        ))}
        <span className="tfill" style={{ width: pct(t), background: zoneColor(t) }} />
        {sorted.map((m) => (
          <span key={m.name + m.c} className={`ttick${m.c <= t ? " on" : ""}`} style={{ left: pct(m.c), background: m.c <= t ? zoneColor(m.c) : undefined }} />
        ))}
        <span className="tnow" style={{ left: pct(t) }} />
      </div>
      <div className="tends"><span className="mono">{lo} °C</span><span className="mono">{max} °C</span></div>
      <input type="range" min={lo} max={max} value={Math.max(lo, t)} aria-label="Temperatur wählen"
        onChange={(e) => { setTouched(true); setT(+e.target.value); }} />
      <ol className="tlist">
        {sorted.map((m) => (
          <li key={m.name + m.c} className={m.c <= t ? "on" : ""}>
            <i style={{ background: m.c <= t ? zoneColor(m.c) : undefined }} />
            <span className="tc">{m.c} °C</span><span>{m.name}</span>
          </li>
        ))}
      </ol>
      <p className="vis-status">
        {current ? <>Bei {t} °C: <strong>{current.name}</strong>.</> : <>Unter {sorted[0]?.c} °C passiert noch nichts davon.</>}
        {next ? <> Ab {next.c} °C: {next.name}.</> : null}
      </p>
      {note && <span className="mono">{note}</span>}
    </div>
  );
}
