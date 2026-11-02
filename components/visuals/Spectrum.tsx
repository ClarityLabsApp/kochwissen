"use client";
import { t as ui, type Lang } from "@/lib/i18n";
import { useEffect, useRef, useState } from "react";
import { useInView, readMs, tour } from "./useInView";

/**
 * Skala-Vorlage für Stellschrauben: ein Verlauf von links nach rechts, den man direkt ziehen kann.
 * Beim Sichtbarwerden wandert der Knopf einmal durch alle Bereiche und hält jeweils so lange, wie der Text zum Lesen braucht.
 */
export default function Spectrum({ title, left, mid, right, colors, lang = "de" }: { title: string; left: string; mid?: string; right: string; colors: string[]; lang?: Lang }) {
  const V = ui(lang).vis;
  const [v, setV] = useState(0);
  const [touched, setTouched] = useState(false);
  const [run, setRun] = useState(0);
  const root = useRef<HTMLDivElement>(null);
  const seen = useInView(root);
  useEffect(() => {
    if (touched || !seen) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { setV(50); return; }
    const zones = mid ? [[8, left], [50, mid], [92, right]] as const : [[10, left], [90, right]] as const;
    return tour(0, zones.map(([z, txt]) => ({ v: z, hold: readMs(txt) })), (x) => setV(Math.round(x)), 1800);
  }, [touched, seen, run, left, mid, right]);
  const zone = mid ? (v < 34 ? left : v < 67 ? mid : right) : (v < 50 ? left : right);
  return (
    <div className="vis" ref={root}>
      <div className="vis-head"><span className="mono">{title}</span></div>
      <div className="trk">
        <div className="spec" style={{ background: `linear-gradient(90deg, ${colors.join(", ")})` }}>
          <span className="spec-knob" style={{ left: `${v}%` }} />
        </div>
        <input type="range" className="trk-input" min={0} max={100} value={v} aria-label={title} onChange={(e) => { setTouched(true); setV(+e.target.value); }} />
      </div>
      <div className="spec-ends"><span>{left.split(":")[0]}</span>{mid && <span>{mid.split(":")[0]}</span>}<span>{right.split(":")[0]}</span></div>
      <p className="vis-status">{zone}</p>
      <div className="vis-row"><span className="mono">{V.drag}</span><button type="button" className="vis-btn" style={{ marginLeft: "auto" }} onClick={() => { setTouched(false); setV(0); setRun((r) => r + 1); }}>{V.again}</button></div>
    </div>
  );
}
