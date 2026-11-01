"use client";
import { useEffect, useRef, useState } from "react";

/* Vorher-Nachher-Vergleich für Experimente. Jedes Feld ist ein Gefäß mit Inhalt;
   ein Regler (und ein automatischer Durchlauf) blendet vom Vorher- in den Nachher-Zustand. */

export interface Zustand {
  farbe?: string;      // Flüssigkeit oder Gegenstand
  fuell?: number;      // Füllhöhe 0..1 (Gläser, Flaschen, Schüsseln)
  trueb?: number;      // milchige Trübung 0..1
  schaum?: number;     // Schaumhöhe 0..1
  blasen?: number;     // aufsteigende Bläschen 0..1
  ballon?: number;     // Ballongröße 0..1
  kristalle?: number;  // Kristalle am Spieß 0..1
  tropfen?: number;    // Wassertropfen auf der Oberfläche 0..1
  klumpen?: number;    // fester Klumpen 0..1
  klumpenfarbe?: string;
  bodensatz?: number;  // weiße Schicht am Boden 0..1
  tanzen?: number;     // Tropfen schweben und gleiten (Leidenfrost) 0..1
}
export interface Feld { label: string; gefaess: "glas" | "flasche" | "schuessel" | "teller" | "pfanne"; inhalt?: "fluessig" | "apfel" | "bohnen" | "scheiben" | "keins"; spiess?: boolean; vorher: Zustand; nachher: Zustand }

const hex = (h: string) => { const n = parseInt(h.replace("#", ""), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
const mixC = (a = "#ffffff", b = a, t: number) => { const A = hex(a), B = hex(b); return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * t)).join(",")})`; };
const lerp = (a = 0, b = a, t: number) => a + (b - a) * t;
const ease = (t: number) => t * t * (3 - 2 * t);

const INK = "#2b2118", GLASS = "rgba(43,33,24,.55)";

function Panel({ f, t, clock }: { f: Feld; t: number; clock: number }) {
  const k = ease(t);
  const z = (key: keyof Zustand) => lerp(f.vorher[key] as number | undefined, f.nachher[key] as number | undefined, k);
  const col = mixC(f.vorher.farbe ?? "#ffffff", f.nachher.farbe ?? f.vorher.farbe ?? "#ffffff", k);
  const fuell = z("fuell") || (f.inhalt === "fluessig" ? 0.7 : 0);
  const trueb = z("trueb"), schaum = z("schaum"), blasen = z("blasen"), ballon = z("ballon"), krist = z("kristalle"), tropfen = z("tropfen"), klumpen = z("klumpen"), boden = z("bodensatz"), tanzen = z("tanzen");
  const klCol = mixC(f.vorher.klumpenfarbe ?? f.nachher.klumpenfarbe ?? "#e8d6a8", f.nachher.klumpenfarbe ?? f.vorher.klumpenfarbe ?? "#e8d6a8", k);
  const els: React.ReactNode[] = [];
  const seed = (i: number) => ((Math.sin(i * 12.9898) * 43758.5453) % 1 + 1) % 1;

  if (f.gefaess === "glas" || f.gefaess === "flasche") {
    const top = f.gefaess === "flasche" ? 84 : 30, bot = 136, L = 30, R = 90;
    const ly = bot - fuell * (bot - top - 6);
    els.push(<rect key="liq" x={L + 2} y={ly} width={R - L - 4} height={bot - ly - 2} fill={col} opacity={0.9} />);
    if (trueb > 0.01) els.push(<rect key="tr" x={L + 2} y={ly} width={R - L - 4} height={bot - ly - 2} fill="#ece6d8" opacity={trueb * 0.9} />);
    if (boden > 0.01) els.push(<rect key="bs" x={L + 2} y={bot - 2 - boden * 10} width={R - L - 4} height={boden * 10} fill="#fbfaf6" stroke="#d9d2c4" strokeWidth={0.6} />);
    if (schaum > 0.01) els.push(<path key="sch" d={`M${L + 2} ${ly} q7 ${-schaum * 22} 14 0 q7 ${-schaum * 26} 14 0 q7 ${-schaum * 20} 14 0 q7 ${-schaum * 24} 14 0 q2 ${-schaum * 10} 0 0 Z`} fill="#fffdf6" stroke="#d9d2c4" strokeWidth={0.8} />);
    for (let i = 0; i < Math.round(blasen * 14); i++) { const x = L + 6 + seed(i) * (R - L - 12), ph = (clock * (0.5 + seed(i + 3)) + seed(i + 7)) % 1, y = bot - 4 - ph * (bot - ly - 6); els.push(<circle key={`b${i}`} cx={x} cy={y} r={1.6 + seed(i + 1) * 1.6} fill="#ffffff" stroke={GLASS} strokeWidth={0.5} />); }
    if (klumpen > 0.01) els.push(<ellipse key="kl" cx={60} cy={ly + 2 - klumpen * 6} rx={8 + klumpen * 12} ry={5 + klumpen * 8} fill={klCol} stroke="rgba(0,0,0,.25)" />);
    if (f.spiess) {
      els.push(<line key="sp" x1={60} y1={14} x2={60} y2={bot - 14} stroke="#a07a4a" strokeWidth={2} />);
      for (let i = 0; i < Math.round(krist * 16); i++) { const y = 60 + seed(i) * (bot - 80), s = 2 + seed(i + 2) * 3.5 * (0.5 + krist); els.push(<rect key={`k${i}`} x={60 - s / 2 + (seed(i + 5) - 0.5) * 8} y={y} width={s} height={s} fill="#fbf3e2" stroke="#c9a24a" strokeWidth={0.6} transform={`rotate(${seed(i + 9) * 90} 60 ${y})`} />); }
    }
    if (f.gefaess === "flasche") {
      els.push(<path key="g" d={`M${L} 136 L${L} 92 Q${L} 78 48 72 L48 56 L72 56 L72 72 Q${R} 78 ${R} 92 L${R} 136 Z`} fill="none" stroke={GLASS} strokeWidth={1.5} />);
      const r = 5 + ballon * 20; els.push(<g key="bal"><ellipse cx={60} cy={54 - r * 0.95} rx={r * 0.85} ry={r} fill="#c8564a" opacity={0.9} /><rect x={53} y={50} width={14} height={8} fill="#a8443a" /></g>);
    } else els.push(<path key="g" d={`M${L - 2} 28 L${L} 136 L${R} 136 L${R + 2} 28`} fill="none" stroke={GLASS} strokeWidth={1.5} />);
  }

  if (f.gefaess === "schuessel") {
    const ly = 128 - fuell * 34;
    els.push(<path key="liq" d={`M24 ${ly} L96 ${ly} Q92 132 60 134 Q28 132 24 ${ly} Z`} fill={col} opacity={0.9} />);
    if (trueb > 0.01) els.push(<path key="tr" d={`M24 ${ly} L96 ${ly} Q92 132 60 134 Q28 132 24 ${ly} Z`} fill="#f4efe6" opacity={trueb * 0.75} />);
    if (schaum > 0.01) els.push(<path key="sch" d={`M24 ${ly} q9 ${-schaum * 34} 18 -${schaum * 6} q9 ${-schaum * 44} 18 0 q9 ${-schaum * 30} 18 -${schaum * 4} q9 ${-schaum * 36} 18 ${schaum * 6} Z`} fill="#fffdf6" stroke="#d9d2c4" strokeWidth={0.8} />);
    if (klumpen > 0.01) els.push(<ellipse key="kl" cx={60} cy={ly + 4} rx={6 + klumpen * 16} ry={4 + klumpen * 8} fill={klCol} stroke="rgba(0,0,0,.25)" />);
    els.push(<path key="g" d="M18 92 Q20 136 60 138 Q100 136 102 92" fill="none" stroke={INK} strokeWidth={1.6} />);
  }

  if (f.gefaess === "teller" || f.gefaess === "pfanne") {
    if (f.gefaess === "teller") els.push(<ellipse key="t" cx={60} cy={118} rx={50} ry={14} fill="#fbf7ef" stroke={INK} strokeWidth={1.2} />);
    else els.push(<g key="p"><rect x={10} y={116} width={86} height={8} rx={3} fill="#3a3633" /><rect x={96} y={117} width={22} height={4} fill="#3a3633" /></g>);
    if (f.inhalt === "apfel") for (let i = 0; i < 2; i++) { const x = 40 + i * 40; els.push(<g key={`a${i}`}><path d={`M${x - 20} 118 Q${x - 20} 74 ${x} 74 Q${x + 20} 74 ${x + 20} 118 Z`} fill={col} stroke="#b33a2a" strokeWidth={3} /><path d={`M${x - 4} 98 q4 -8 8 0 q-4 8 -8 0`} fill="none" stroke="rgba(90,58,26,.5)" strokeWidth={1} /><circle cx={x} cy={98} r={1.6} fill="#5a3a1a" /></g>); }
    if (f.inhalt === "bohnen") for (let i = 0; i < 4; i++) els.push(<rect key={`bo${i}`} x={22 + (i % 2) * 38} y={100 + Math.floor(i / 2) * 9} width={34} height={7} rx={3.5} fill={col} stroke="rgba(0,0,0,.25)" transform={`rotate(${(i - 1.5) * 5} 60 110)`} />);
    if (f.inhalt === "scheiben") for (let i = 0; i < 3; i++) { const x = 32 + i * 28; els.push(<g key={`s${i}`}><ellipse cx={x} cy={110} rx={12} ry={6} fill={col} stroke="#4f7a3a" strokeWidth={2} /><ellipse cx={x} cy={110} rx={6} ry={2.6} fill="#e8f0d0" opacity={0.7} /></g>); }
    for (let i = 0; i < Math.round(tropfen * 9); i++) { const x = 22 + seed(i) * 76, y = 102 + seed(i + 4) * 12; els.push(<circle key={`d${i}`} cx={x} cy={y} r={1.6 + seed(i + 2) * 1.8} fill="#8fb8c9" stroke="#5f8fa3" strokeWidth={0.5} />); }
    if (f.gefaess === "pfanne") {
      // Tropfen auf der heißen Pfanne: flach und zischend, oder als Kügelchen tanzend
      for (let i = 0; i < 5; i++) {
        const base = 22 + i * 15, x = base + (tanzen > 0.5 ? Math.sin(clock * 3 + i * 2) * 8 * tanzen : 0), lift = tanzen * 3;
        if (tanzen < 0.5) els.push(<ellipse key={`pt${i}`} cx={x} cy={114} rx={5 * (1 - tanzen)} ry={1.6} fill="#8fb8c9" opacity={1 - tanzen} />);
        else els.push(<circle key={`pt${i}`} cx={x} cy={110 - lift} r={3.6} fill="#8fb8c9" stroke="#5f8fa3" strokeWidth={0.6} />);
      }
      if (tanzen < 0.5) for (let i = 0; i < 4; i++) { const ph = (clock + i * 0.25) % 1; els.push(<path key={`st${i}`} d={`M${28 + i * 18} ${110 - ph * 30} q-4 -5 0 -10`} stroke="rgba(143,184,201,.7)" fill="none" strokeWidth={1.4} />); }
    }
  }

  return (
    <figure className="xp-panel">
      <svg viewBox="0 0 120 150" role="img" aria-label={f.label}>{els}</svg>
      <figcaption>{f.label}</figcaption>
    </figure>
  );
}

export default function ExperimentCompare({ felder, vorher = "Vorher", nachher = "Nachher" }: { felder: Feld[]; vorher?: string; nachher?: string }) {
  const [t, setT] = useState(0);
  const [clock, setClock] = useState(0);
  const [run, setRun] = useState(0);
  const root = useRef<HTMLDivElement>(null);

  // Einmal von selbst durchlaufen, sobald die Grafik sichtbar ist
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { setT(1); return; }
    let raf = 0, started = 0;
    const go = () => { const s = performance.now(); const step = (now: number) => { const p = Math.min(1, (now - s) / 3500); setT(p); if (p < 1) raf = requestAnimationFrame(step); }; raf = requestAnimationFrame(step); };
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting && !started) { started = 1; setTimeout(go, 400); } }, { threshold: 0.4 });
    if (root.current) io.observe(root.current);
    return () => { io.disconnect(); cancelAnimationFrame(raf); };
  }, [run]);

  // Uhr für Bläschen und Dampf
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    let raf = 0; const tick = (now: number) => { setClock(now / 1000); raf = requestAnimationFrame(tick); }; raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  return (
    <div className="vis" ref={root}>
      <div className="vis-head"><span className="mono">Vorher · Nachher</span><span className="mono">{t < 0.5 ? vorher : nachher}</span></div>
      <div className="xp-grid" style={{ gridTemplateColumns: `repeat(${felder.length}, minmax(0, 1fr))` }}>
        {felder.map((f) => <Panel key={f.label} f={f} t={t} clock={clock} />)}
      </div>
      <div className="vis-row">
        <label style={{ flex: "1 1 220px", flexDirection: "column", alignItems: "stretch" }}>
          <span className="mono">{vorher} ↔ {nachher}</span>
          <input type="range" min={0} max={1} step={0.01} value={t} onChange={(e) => setT(+e.target.value)} aria-label="Vorher oder Nachher" />
        </label>
        <button type="button" className="vis-btn" onClick={() => { setT(0); setRun((r) => r + 1); }}>Nochmal</button>
      </div>
      <span className="mono">Schematisch</span>
    </div>
  );
}
