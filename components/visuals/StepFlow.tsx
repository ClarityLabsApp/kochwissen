"use client";
import { useEffect, useRef, useState } from "react";
import { t, type Lang } from "@/lib/i18n";
import { useInView, readMs } from "./useInView";

/**
 * Ablauf-Vorlage für Techniken: die Schritte als Punktlinie,
 * die sich von selbst Schritt für Schritt füllt (jeder Schritt so lange, wie sein Text zum Lesen braucht). Antippen springt, Pause hält an.
 */
export default function StepFlow({ steps, chips, lang = "de" }: { steps: string[]; chips?: string[]; lang?: Lang }) {
  const V = t(lang).vis;
  const [i, setI] = useState(0);
  const [play, setPlay] = useState(true);
  const [progress, setProgress] = useState(0);
  const ref = useRef<HTMLDivElement>(null);
  const seen = useInView(ref);
  const DUR = readMs(steps[i] ?? "");

  useEffect(() => {
    if (typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches) setPlay(false);
  }, []);

  useEffect(() => {
    if (!play || !seen) return;
    let raf = 0; const start = performance.now() - progress * DUR;
    const tick = (now: number) => {
      const p = (now - start) / DUR;
      if (p >= 1) { setProgress(0); setI((k) => (k + 1) % steps.length); return; }
      setProgress(p); raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [play, i, steps.length, seen]);

  const n = steps.length;
  const W = Math.max(240, n * 72), H = 64, L = 22, R = 22;
  const x = (k: number) => (n === 1 ? W / 2 : L + (k / (n - 1)) * (W - L - R));
  const fillTo = n === 1 ? x(0) : x(i) + (i < n - 1 ? (x(i + 1) - x(i)) * progress : 0);

  return (
    <div className="vis" ref={ref}>
      <div className="vis-head">
        <span className="mono">{V.flow} · {V.step(i + 1, n)}</span>
        <button type="button" className="vis-btn" onClick={() => setPlay((p) => !p)}>{play ? V.pause : V.play}</button>
      </div>
      <div className="vis-scroll">
        <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={V.stepsIn(n)}>
          <line x1={x(0)} x2={x(n - 1)} y1={30} y2={30} stroke="#d5c3a1" strokeWidth={3} />
          <line x1={x(0)} x2={fillTo} y1={30} y2={30} stroke="#b4542a" strokeWidth={3} />
          {steps.map((_, k) => (
            <g key={k} style={{ cursor: "pointer" }} onClick={() => { setI(k); setProgress(0); }}>
              <circle cx={x(k)} cy={30} r={k === i ? 13 : 10} fill={k < i ? "#b4542a" : k === i ? "#2b2118" : "#f6eedd"} stroke="#2b2118" strokeWidth={1.4} style={{ transition: "r .25s, fill .25s" }} />
              <text x={x(k)} y={34} textAnchor="middle" fontFamily="JetBrains Mono, monospace" fontSize={11} fontWeight={600} fill={k <= i ? "#f6eedd" : "#2b2118"}>{k + 1}</text>
            </g>
          ))}
        </svg>
      </div>
      <p className="vis-step" key={i}>{steps[i]}</p>
      {chips && chips.length > 0 && <div className="chips">{chips.map((c) => <span key={c} className="chip">{c}</span>)}</div>}
    </div>
  );
}
