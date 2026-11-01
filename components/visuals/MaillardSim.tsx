"use client";
import { useEffect, useRef, useState } from "react";

/* Maillard-Reaktion in drei Zoomstufen. Nachbau des HTML-Prototyps als React-Komponente.
   Kernidee: Solange Wasser auf der Oberfläche ist, hängt sie bei 100 °C fest. Erst trocken und über ~140 °C bräunt sie. */

type Zoom = 1 | 2 | 3;
interface State { pan: number; wet: number; gar: number; brown: number; t: number }
const COL = { amino: "#2f6f73", sugar: "#e0ad3a", water: "#8fb8c9", waterRim: "#5f8fa3", roast: "#6b3a1e", nut: "#b8873a", caramel: "#d9822b", meat: "#8c2f2a", bitter: "#3a3633", busy: "#b4542a", ink: "#2b2118", pan: "#3a3633" };
const AROMAS = ["roast", "roast", "nut", "caramel", "meat"] as const;

const surfaceT = (S: State) => (S.wet > 0.02 && S.pan > 100 ? 100 : S.pan);
function stepState(S: State, dt: number) {
  S.t += dt;
  const T = surfaceT(S);
  if (S.pan > 100 && S.wet > 0) S.wet = Math.max(0, S.wet - ((S.pan - 100) / 100) * 0.09 * dt);
  if (T >= 60) S.gar = Math.min(1, S.gar + ((T - 50) / 60) * 0.25 * dt);
  if (S.wet <= 0.02 && T > 140) S.brown = Math.min(1.45, S.brown + ((T - 140) / 60) * 0.05 * (T > 190 ? 1.6 : 1) * dt);
}

const hex = (h: string) => { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
const mix = (a: string, b: string, t: number) => { const A = hex(a), B = hex(b), k = Math.max(0, Math.min(1, t)); return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * k)).join(",")})`; };
function crust(S: State) {
  const b = S.brown;
  if (b < 0.05) return mix("#c46a6a", "#a39088", S.gar);
  if (b < 0.5) return mix("#a39088", "#c08a45", (b - 0.05) / 0.45);
  if (b < 1) return mix("#c08a45", "#7a4523", (b - 0.5) / 0.5);
  if (b < 1.2) return mix("#7a4523", "#3d2416", (b - 1) / 0.2);
  return mix("#3d2416", "#1f1a17", (b - 1.2) / 0.25);
}
const brownWord = (b: number) => (b < 0.05 ? "keine" : b < 0.4 ? "leicht" : b < 0.85 ? "goldbraun" : b < 1.2 ? "tiefbraun" : "verbrannt");
function statusText(S: State) {
  const T = surfaceT(S);
  if (S.pan <= 100) return "Zu kühl: Das Fleisch gart, aber nichts bräunt.";
  if (S.wet > 0.02) return "Wasser verdampft. Die Oberfläche hängt bei 100 °C fest, noch keine Bräunung.";
  if (T < 140) return "Trocken, aber unter 140 °C: Die Bräunung kommt kaum in Gang.";
  if (S.brown >= 1.2) return "Zu weit: Die Kruste verbrennt und schmeckt bitter.";
  if (S.brown >= 0.85) return "Tiefbraune Kruste. Jetzt wenden oder die Hitze reduzieren.";
  return "Maillard läuft: Eiweiß und Zucker bilden Röstaromen und braune Farbe.";
}

interface P { type: "amino" | "sugar" | "water" | "busy"; x: number; y: number; vx: number; vy: number; r: number; leaving?: boolean }
interface A { x: number; y: number; r: number; R: number; kind: string; vx: number; vy: number }
interface M { a: P; b: P; t: number; done?: boolean }

function makeMol(W: number, H: number) {
  const mk = (type: P["type"]): P => ({ type, x: Math.random() * W, y: H * 0.15 + Math.random() * H * 0.7, vx: Math.random() - 0.5, vy: Math.random() - 0.5, r: type === "water" ? 4 : 5.5 });
  const P: P[] = [];
  for (let i = 0; i < 24; i++) P.push(mk("amino"), mk("sugar"));
  for (let i = 0; i < 40; i++) P.push(mk("water"));
  return { P, A: [] as A[], M: [] as M[], mk };
}

export default function MaillardSim() {
  const ref = useRef<HTMLCanvasElement>(null);
  const S = useRef<State>({ pan: 200, wet: 1, gar: 0, brown: 0, t: 0 });
  const mol = useRef<ReturnType<typeof makeMol> | null>(null);
  const zoomRef = useRef<Zoom>(1);
  const [zoom, setZoom] = useState<Zoom>(1);
  const [pan, setPan] = useState(200);
  const [, setTick] = useState(0);
  zoomRef.current = zoom;
  S.current.pan = pan;

  const start = (wet: boolean) => {
    Object.assign(S.current, { wet: wet ? 1 : 0.15, gar: 0, brown: 0, t: 0 });
    const cv = ref.current; if (cv) mol.current = makeMol(cv.clientWidth, cv.clientHeight);
  };

  useEffect(() => {
    const cv = ref.current!; const g = cv.getContext("2d")!;
    let W = 360, H = 240, raf = 0, last = performance.now(), n = 0;
    const size = () => { const dpr = Math.min(2, window.devicePixelRatio || 1); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; g.setTransform(dpr, 0, 0, dpr, 0, 0); };
    size(); mol.current = makeMol(W, H);
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const drawDish = (s: State, t: number) => {
      // Ebene 1: Steak in der Pfanne, seitlich
      const cx = W / 2, py = H * 0.72;
      g.fillStyle = COL.pan; g.fillRect(W * 0.08, py, W * 0.84, 10); g.fillRect(W * 0.9, py - 4, W * 0.1, 6);
      const w = Math.min(W * 0.56, 300), h = 42;
      g.fillStyle = mix("#d27a76", "#9c7a72", s.gar * 0.5);
      g.beginPath(); (g as any).roundRect ? (g as any).roundRect(cx - w / 2, py - h, w, h, 16) : g.rect(cx - w / 2, py - h, w, h); g.fill();
      const ch = 6 + Math.min(1, s.brown) * 4; g.fillStyle = crust(s); g.fillRect(cx - w / 2 + 4, py - ch, w - 8, ch);
      const boiling = s.wet > 0.02 && s.pan > 100;
      if (boiling) { g.strokeStyle = `rgba(143,184,201,${Math.min(1, s.wet * 1.4 + 0.2)})`; g.lineWidth = 2;
        for (let i = 0; i < 5; i++) { const x = cx - w / 2 + 20 + i * (w - 40) / 4, ph = (t * 1.2 + i * 0.37) % 1; g.beginPath(); g.moveTo(x, py - h - 6 - ph * 30); g.quadraticCurveTo(x - 6, py - h - 14 - ph * 30, x, py - h - 22 - ph * 30); g.stroke(); } }
      if (s.brown > 1.1) { g.fillStyle = `rgba(58,54,51,${Math.min(0.5, (s.brown - 1.1) * 1.5)})`; for (let i = 0; i < 6; i++) { const ph = (t * 0.6 + i / 6) % 1; g.beginPath(); g.arc(cx - w / 3 + i * w / 8, py - h - ph * 70, 6 + ph * 10, 0, Math.PI * 2); g.fill(); } }
      g.fillStyle = COL.ink; g.font = "12px JetBrains Mono, monospace"; g.fillText(`Pfanne ${s.pan} °C`, W * 0.08, py + 28);
    };

    const drawSurface = (s: State, t: number) => {
      // Ebene 2: Schnitt durch die Oberfläche mit Wassertropfen und Thermometer
      const base = H * 0.78, T = surfaceT(s);
      g.fillStyle = COL.pan; g.fillRect(0, base, W, H - base); g.fillStyle = "#f3e7d3"; g.font = "11px JetBrains Mono, monospace"; g.fillText(`PFANNE · ${s.pan} °C`, 10, base + 16);
      const ch = 4 + Math.min(1.45, s.brown) * 12;
      g.fillStyle = mix("#c46a6a", "#a39088", s.gar * 0.75); g.fillRect(0, base - ch - 70, W - 50, 70);
      if (s.gar > 0.05) { g.fillStyle = `rgba(163,144,136,${s.gar * 0.8})`; g.fillRect(0, base - ch - 22 * s.gar, W - 50, 22 * s.gar); }
      g.fillStyle = crust(s); g.fillRect(0, base - ch, W - 50, ch);
      for (let i = 0; i < 9; i++) { const r = Math.max(0, s.wet * (5 + (i % 3))); if (r > 0.3) { g.beginPath(); g.arc(14 + i * (W - 80) / 8, base - 3, r, 0, Math.PI * 2); g.fillStyle = COL.water; g.fill(); g.strokeStyle = COL.waterRim; g.stroke(); } }
      if (s.wet > 0.02 && s.pan > 100) { g.strokeStyle = "rgba(143,184,201,.8)"; g.lineWidth = 1.5; for (let i = 0; i < 9; i += 2) { const x = 14 + i * (W - 80) / 8, ph = (t + i * 0.2) % 1; g.beginPath(); g.moveTo(x, base - ch - 74 - ph * 20); g.quadraticCurveTo(x - 4, base - ch - 80 - ph * 20, x, base - ch - 86 - ph * 20); g.stroke(); } }
      // Thermometer der Oberfläche
      const tx = W - 26, top = 16, bot = base - 8, y = bot - (Math.min(220, T) / 220) * (bot - top);
      g.strokeStyle = COL.ink; g.lineWidth = 1; g.strokeRect(tx - 5, top, 10, bot - top);
      g.fillStyle = T > 140 ? "#b4542a" : "#8fb8c9"; g.fillRect(tx - 4, y, 8, bot - y);
      for (const [c, lab] of [[100, "100"], [140, "140"]] as const) { const yy = bot - (c / 220) * (bot - top); g.beginPath(); g.moveTo(tx - 9, yy); g.lineTo(tx - 5, yy); g.stroke(); g.fillStyle = COL.ink; g.font = "10px JetBrains Mono, monospace"; g.fillText(lab, tx - 32, yy + 3); }
      if (s.gar > 0.4) { g.fillStyle = COL.ink; g.font = "11px JetBrains Mono, monospace"; g.fillText("graue Zone", 10, base - ch - 22 * s.gar - 6); }
    };

    const drawMol = (s: State, dt: number) => {
      const m = mol.current!; const T = surfaceT(s), speed = 20 + T * 0.35;
      if (!reduce) {
        const wantW = Math.round(40 * s.wet), waters = m.P.filter((p) => p.type === "water" && !p.leaving);
        if (waters.length > wantW) waters[0].leaving = true;
        for (const p of m.P) {
          p.vx += (Math.random() - 0.5) * 0.6; p.vy += (Math.random() - 0.5) * 0.6; const k = Math.hypot(p.vx, p.vy) || 1; p.vx /= k; p.vy /= k;
          p.x += p.vx * speed * dt; p.y += p.vy * speed * dt - (p.leaving ? 90 * dt : 0);
          if (p.x < 8) { p.x = 8; p.vx = Math.abs(p.vx); } if (p.x > W - 8) { p.x = W - 8; p.vx = -Math.abs(p.vx); }
          if (!p.leaving) { if (p.y < 20) { p.y = 20; p.vy = Math.abs(p.vy); } if (p.y > H - 20) { p.y = H - 20; p.vy = -Math.abs(p.vy); } }
        }
        m.P = m.P.filter((p) => !(p.leaving && p.y < -10));
        const rate = s.wet <= 0.02 && T > 140 ? ((T - 140) / 60) * 6 : 0;
        if (Math.random() < rate * dt) {
          const am = m.P.filter((p) => p.type === "amino"), su = m.P.filter((p) => p.type === "sugar");
          if (am.length && su.length) {
            const a = am[Math.floor(Math.random() * am.length)]; let best = su[0], bd = 1e9;
            for (const x of su) { const d = (x.x - a.x) ** 2 + (x.y - a.y) ** 2; if (d < bd) { bd = d; best = x; } }
            a.type = "busy"; best.type = "busy"; m.M.push({ a, b: best, t: 0 });
          }
        }
        for (const q of m.M) {
          q.t += dt * 1.6; const mx = (q.a.x + q.b.x) / 2, my = (q.a.y + q.b.y) / 2, k = Math.min(1, dt * 5);
          q.a.x += (mx - q.a.x) * k; q.a.y += (my - q.a.y) * k; q.b.x += (mx - q.b.x) * k; q.b.y += (my - q.b.y) * k;
          if (q.t >= 1) {
            m.A.push({ x: mx, y: my, r: 0, R: 6 + Math.random() * 6, kind: s.brown > 1.15 ? "bitter" : AROMAS[Math.floor(Math.random() * AROMAS.length)], vx: (Math.random() - 0.5) * 6, vy: (Math.random() - 0.5) * 6 });
            m.P = m.P.filter((p) => p !== q.a && p !== q.b); m.P.push(m.mk("amino"), m.mk("sugar")); q.done = true;
          }
        }
        m.M = m.M.filter((q) => !q.done);
        for (const a of m.A) { a.r += (a.R - a.r) * Math.min(1, dt * 4); a.x += a.vx * dt; a.y += a.vy * dt; }
        if (m.A.length > 70) m.A.splice(0, m.A.length - 70);
      }
      g.globalAlpha = 0.85; for (const a of m.A) { g.fillStyle = (COL as any)[a.kind]; g.beginPath(); g.arc(a.x, a.y, a.r, 0, Math.PI * 2); g.fill(); } g.globalAlpha = 1;
      g.strokeStyle = COL.busy; g.lineWidth = 1.5; g.setLineDash([3, 3]); for (const q of m.M) { g.beginPath(); g.moveTo(q.a.x, q.a.y); g.lineTo(q.b.x, q.b.y); g.stroke(); } g.setLineDash([]);
      for (const p of m.P) { g.fillStyle = (COL as any)[p.type]; g.beginPath(); g.arc(p.x, p.y, p.r, 0, Math.PI * 2); g.fill(); if (p.type === "water") { g.strokeStyle = COL.waterRim; g.lineWidth = 0.8; g.stroke(); } }
    };

    const frame = (now: number) => {
      const dt = Math.min(0.05, (now - last) / 1000); last = now;
      if (!reduce) stepState(S.current, dt);
      g.clearRect(0, 0, W, H);
      const z = zoomRef.current;
      if (z === 1) drawDish(S.current, now / 1000); else if (z === 2) drawSurface(S.current, now / 1000); else drawMol(S.current, dt);
      if (++n % 10 === 0) setTick((x) => x + 1);
      raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    const ro = new ResizeObserver(() => { size(); mol.current = makeMol(W, H); }); ro.observe(cv);
    return () => { cancelAnimationFrame(raf); ro.disconnect(); };
  }, []);

  const s = S.current, T = surfaceT(s);
  const ZOOMS: [Zoom, string, string][] = [[1, "1 · Gericht", "≈ 10 cm"], [2, "2 · Oberfläche", "≈ 1 mm"], [3, "3 · Moleküle", "≈ 1 nm"]];
  return (
    <div className="vis">
      <div className="seg" role="group" aria-label="Zoomstufe">
        {ZOOMS.map(([z, l]) => <button key={z} type="button" aria-pressed={zoom === z} onClick={() => setZoom(z)}>{l}</button>)}
      </div>
      <div className="vis-head"><span className="mono">Ebene {zoom} · {zoom === 1 ? "Steak in der Pfanne" : zoom === 2 ? "Schnitt durch die Oberfläche" : "Eiweiß, Zucker und Wasser"}</span><span className="mono">{ZOOMS[zoom - 1][2]}</span></div>
      <canvas ref={ref} className="sim-canvas" aria-label="Maillard-Reaktion" />
      {zoom === 3 && <div className="legend mono"><span><i style={{ background: COL.amino }} />Eiweiß</span><span><i style={{ background: COL.sugar }} />Zucker</span><span><i style={{ background: COL.water }} />Wasser</span><span><i style={{ background: COL.roast }} />Röstaroma</span></div>}
      <p className="vis-status">{statusText(s)}</p>
      <div className="vis-readouts" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))" }}>
        <div><span className="mono">Oberfläche</span><b>{Math.round(T)} °C</b></div>
        <div><span className="mono">Wasser</span><b>{Math.round(s.wet * 100)} %</b></div>
        <div><span className="mono">Bräunung</span><b>{brownWord(s.brown)}</b></div>
        <div><span className="mono">Zeit</span><b>{Math.floor(s.t)} s</b></div>
      </div>
      <div className="vis-row">
        <label style={{ flex: "1 1 220px", flexDirection: "column", alignItems: "stretch" }}>
          <span className="mono">Pfanne · {pan} °C</span>
          <input type="range" min={20} max={240} step={5} value={pan} onChange={(e) => setPan(+e.target.value)} />
        </label>
        <button type="button" className="vis-btn" onClick={() => start(true)}>Nass einlegen</button>
        <button type="button" className="vis-btn" onClick={() => start(false)}>Trocken getupft einlegen</button>
      </div>
      <span className="mono">Modell vereinfacht · Richtwerte</span>
    </div>
  );
}
