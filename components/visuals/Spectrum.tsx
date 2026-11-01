"use client";
import { useEffect, useState } from "react";

/**
 * Skala-Vorlage für Stellschrauben: ein Verlauf von links nach rechts mit Regler.
 * Beim Öffnen gleitet der Regler einmal über die ganze Skala.
 */
export default function Spectrum({ title, left, mid, right, colors }: { title: string; left: string; mid?: string; right: string; colors: string[] }) {
  const [v, setV] = useState(0);
  const [touched, setTouched] = useState(false);
  useEffect(() => {
    if (touched || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    let raf = 0; const start = performance.now();
    const run = (now: number) => { const p = Math.min(1, (now - start) / 3000); setV(Math.round(100 * (0.5 - 0.5 * Math.cos(p * Math.PI)))); if (p < 1) raf = requestAnimationFrame(run); };
    raf = requestAnimationFrame(run);
    return () => cancelAnimationFrame(raf);
  }, [touched]);
  const zone = mid ? (v < 34 ? left : v < 67 ? mid : right) : (v < 50 ? left : right);
  return (
    <div className="vis">
      <div className="vis-head"><span className="mono">{title}</span></div>
      <div className="spec" style={{ background: `linear-gradient(90deg, ${colors.join(", ")})` }}>
        <span className="spec-knob" style={{ left: `${v}%` }} />
      </div>
      <input type="range" min={0} max={100} value={v} aria-label={title} onChange={(e) => { setTouched(true); setV(+e.target.value); }} />
      <div className="spec-ends"><span>{left.split(":")[0]}</span>{mid && <span>{mid.split(":")[0]}</span>}<span>{right.split(":")[0]}</span></div>
      <p className="vis-status">{zone}</p>
    </div>
  );
}
