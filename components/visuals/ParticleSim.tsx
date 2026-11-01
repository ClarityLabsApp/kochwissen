"use client";
import { useEffect, useRef, useState } from "react";

/* Punkt-Sprache laut DESIGN.md */
const C = { water: "#8fb8c9", waterRim: "#5f8fa3", fat: "#f0d27a", fatRim: "#c9a24a", lab: "#2f6f73", salt: "#ffffff", sepia: "#7a5a3a",
  ink: "#2b2118", roast: "#6b3a1e", nut: "#b8873a", caramel: "#d9822b", meat: "#c97b72", meatRim: "#a9564e", cell: "#c8d9a8", cellRim: "#7f9a5a" };

export type Preset = "emulsion" | "osmose" | "pektin-abbau" | "reduktion" | "hefegaerung" | "chemische-lockerung";

interface Ctl { a: number; b: boolean; ph: number }
interface Sim {
  title: string; scale: string;
  controls: { slider?: { label: string; min: number; max: number; step: number; def: number; fmt: (v: number) => string }; toggle?: { label: string; def: boolean }; ph?: boolean; reset?: boolean };
  init(W: number, H: number, c: Ctl): unknown;
  step(s: any, dt: number, c: Ctl, W: number, H: number): void;
  draw(g: CanvasRenderingContext2D, s: any, c: Ctl, W: number, H: number, t: number): void;
  status(s: any, c: Ctl): string;
  readouts(s: any, c: Ctl): [string, string][];
}

const rnd = (a: number, b: number) => a + Math.random() * (b - a);
const dot = (g: CanvasRenderingContext2D, x: number, y: number, r: number, fill: string, rim?: string, lw = 1) => {
  g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fillStyle = fill; g.fill(); if (rim) { g.strokeStyle = rim; g.lineWidth = lw; g.stroke(); }
};

/* ---------------- Emulsion: Tröpfchen zerteilen, mit oder ohne Emulgator ---------------- */
const emulsion: Sim = {
  title: "Ebene 3 · Fetttröpfchen im Wasser", scale: "≈ 0,05 mm",
  controls: { slider: { label: "Schlagen", min: 0, max: 1, step: 0.01, def: 0.6, fmt: (v) => (v < 0.05 ? "aus" : v < 0.4 ? "sanft" : v < 0.75 ? "kräftig" : "Mixer") }, toggle: { label: "Emulgator (Eigelb, Senf)", def: true }, reset: true },
  init(W, H) { return { d: Array.from({ length: 4 }, (_, i) => ({ x: W * (0.2 + i * 0.2), y: rnd(H * .3, H * .7), r: rnd(30, 40), vx: 0, vy: 0 })), water: Array.from({ length: 70 }, () => ({ x: rnd(0, W), y: rnd(0, H) })) }; },
  step(s, dt, c, W, H) {
    const shear = c.a, d = s.d as any[];
    const target = 26 - shear * 21; // Zielgröße der Tröpfchen
    for (const p of d) {
      const swirl = Math.sin(p.y / 40 + performance.now() / 600) * shear * 120;
      p.vx += (rnd(-1, 1) * 70 + swirl - p.vx) * Math.min(1, dt * 3);
      p.vy += (rnd(-1, 1) * 70 + (shear < 0.05 ? -p.r * 1.6 : 0) - p.vy) * Math.min(1, dt * 3); // ohne Schlagen steigt Fett auf
      p.x += p.vx * dt; p.y += p.vy * dt;
      if (p.x < p.r) { p.x = p.r; p.vx = Math.abs(p.vx); } if (p.x > W - p.r) { p.x = W - p.r; p.vx = -Math.abs(p.vx); }
      if (p.y < p.r) { p.y = p.r; p.vy = Math.abs(p.vy) * .3; } if (p.y > H - p.r) { p.y = H - p.r; p.vy = -Math.abs(p.vy); }
    }
    if (shear > 0.05 && d.length < 140) for (const p of [...d]) if (p.r > target && Math.random() < shear * dt * 4) {
      const r2 = p.r / Math.SQRT2; p.r = r2; d.push({ x: p.x + rnd(-4, 4), y: p.y + rnd(-4, 4), r: r2, vx: rnd(-40, 40), vy: rnd(-40, 40) });
    }
    if (!c.b) { // ohne Emulgator fließen sich berührende Tröpfchen zusammen
      for (let i = 0; i < d.length; i++) for (let j = i + 1; j < d.length; j++) {
        const a = d[i], b = d[j]; const dd = Math.hypot(a.x - b.x, a.y - b.y);
        if (dd < (a.r + b.r) * 0.9 && Math.random() < dt * 6) { const r = Math.sqrt(a.r * a.r + b.r * b.r); a.x = (a.x * a.r + b.x * b.r) / (a.r + b.r); a.y = (a.y * a.r + b.y * b.r) / (a.r + b.r); a.r = Math.min(r, 70); d.splice(j, 1); j--; }
      }
    }
    for (const w of s.water) { w.x = (w.x + rnd(-1, 1) * 20 * dt + W) % W; w.y = (w.y + rnd(-1, 1) * 20 * dt + H) % H; }
  },
  draw(g, s, c) {
    for (const w of s.water) dot(g, w.x, w.y, 2.2, C.water);
    for (const p of s.d) {
      dot(g, p.x, p.y, p.r, C.fat, C.fatRim, 1.2);
      if (c.b) { const n = Math.max(6, Math.round(p.r * 0.9)); for (let k = 0; k < n; k++) { const a = (k / n) * Math.PI * 2; dot(g, p.x + Math.cos(a) * (p.r + 2.5), p.y + Math.sin(a) * (p.r + 2.5), 1.8, C.lab); } }
    }
  },
  status(s, c) {
    const n = s.d.length, avg = s.d.reduce((a: number, p: any) => a + p.r, 0) / n;
    if (c.a < 0.05 && !c.b && n < 6) return "Ohne Emulgator und ohne Bewegung fließen die Tröpfchen zusammen und steigen auf: Die Sauce trennt sich.";
    if (c.a < 0.05 && c.b) return "Die Hülle aus Emulgator hält die Tröpfchen getrennt, auch wenn niemand mehr schlägt: Die Emulsion bleibt stabil.";
    if (!c.b) return "Schlagen zerteilt das Fett, aber ohne Emulgator fließen die Tröpfchen gleich wieder zusammen.";
    return avg < 9 ? "Viele winzige, umhüllte Tröpfchen, dicht gepackt: Die Sauce wird dick und cremig." : "Schlagen zerteilt das Fett in immer kleinere Tröpfchen, der Emulgator umhüllt jedes einzelne.";
  },
  readouts(s) { const n = s.d.length; const avg = s.d.reduce((a: number, p: any) => a + p.r, 0) / n; return [["Tröpfchen", String(n)], ["Größe", avg < 9 ? "winzig" : avg < 18 ? "mittel" : "groß"]]; },
};

/* ---------------- Osmose: Salz zieht Wasser, später zieht Salzlake ein ---------------- */
const osmose: Sim = {
  title: "Ebene 3 · Fleischoberfläche mit Salz", scale: "≈ 1 mm",
  controls: { slider: { label: "Zeit nach dem Salzen", min: 0, max: 1, step: 0.005, def: 0, fmt: (v) => { const m = Math.round(Math.pow(v, 2.2) * 1440); return m < 60 ? `${m} min` : `${Math.round(m / 60)} h`; } } },
  init(W, H) {
    const top = H * 0.32, water = [], salt = [];
    for (let i = 0; i < 70; i++) water.push({ hx: rnd(10, W - 10), hy: rnd(top + 18, H - 10), sx: rnd(10, W - 10), sy: top - rnd(2, 16), ph: rnd(0, 6) });
    for (let i = 0; i < 26; i++) salt.push({ sx: 12 + (i / 25) * (W - 24) + rnd(-4, 4), sy: top - 8, ix: rnd(10, W - 10), iy: rnd(top + 14, H - 10), ph: rnd(0, 6) });
    return { top, water, salt, auto: true };
  },
  step() {},
  draw(g, s, c, W, H, t) {
    const v = c.a, top = s.top;
    g.fillStyle = "#e8b2a8"; g.fillRect(0, top, W, H - top);
    g.strokeStyle = C.meatRim; g.globalAlpha = .35; g.lineWidth = 1;
    for (let y = top + 20; y < H; y += 26) { g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(W * .3, y - 6, W * .6, y + 6, W, y - 2); g.stroke(); }
    g.globalAlpha = 1; g.fillStyle = C.ink; g.fillRect(0, top - 1, W, 1.5);
    const out = Math.sin(Math.min(1, v / 0.55) * Math.PI) * (v < 0.55 ? 1 : 0);   // Wasser draußen: Spitze früh
    const dissolve = Math.min(1, v / 0.25);                                          // Salz löst sich
    const inward = Math.max(0, Math.min(1, (v - 0.35) / 0.6));                      // Salzlake zieht ein
    s.water.forEach((w: any, i: number) => {
      const f = i < 45 ? out : 0, jx = Math.sin(t * 1.4 + w.ph) * 2, jy = Math.cos(t * 1.2 + w.ph) * 2;
      dot(g, w.hx + (w.sx - w.hx) * f + jx, w.hy + (w.sy - w.hy) * f + jy, 3, C.water, C.waterRim, .8);
    });
    s.salt.forEach((p: any) => {
      const jx = Math.sin(t + p.ph) * 1.5;
      if (dissolve < 1) { const sz = 7 * (1 - dissolve) + 2; g.fillStyle = C.salt; g.strokeStyle = C.sepia; g.lineWidth = 1; g.fillRect(p.sx - sz / 2, p.sy - sz / 2, sz, sz); g.strokeRect(p.sx - sz / 2, p.sy - sz / 2, sz, sz); }
      if (dissolve > 0.2) { const x = p.sx + (p.ix - p.sx) * inward + jx, y = p.sy + (p.iy - p.sy) * inward; dot(g, x, y, 2.4, C.salt, C.sepia, .8); }
    });
    g.font = '600 10px "JetBrains Mono", monospace'; g.fillStyle = C.sepia; g.fillText("OBERFLÄCHE", 10, top - 24); g.fillText("FLEISCH", 10, H - 10);
  },
  status(_s, c) {
    const v = c.a;
    if (v < 0.03) return "Das Salz liegt auf der trockenen Oberfläche.";
    if (v < 0.5) return "Das Salz zieht Wasser aus dem Fleisch an die Oberfläche und löst sich darin. Jetzt ist sie nass: kein guter Moment zum Braten.";
    if (v < 0.75) return "Die salzige Lösung zieht langsam wieder ins Fleisch ein. Die Oberfläche trocknet ab.";
    return "Das Salz ist tief im Fleisch angekommen und hält dort beim Garen Wasser fest. Die Oberfläche ist trocken: ideal zum Braten.";
  },
  readouts(_s, c) { const v = c.a; return [["Oberfläche", v < 0.03 ? "trocken" : v < 0.6 ? "nass" : "trocken"], ["Salz", v < 0.4 ? "außen" : v < 0.75 ? "wandert ein" : "innen"]]; },
};

/* ---------------- Pektin-Abbau: Zellen lösen sich voneinander ---------------- */
const pektin: Sim = {
  title: "Ebene 2 · Pflanzenzellen und ihr Kitt", scale: "≈ 0,1 mm",
  controls: { slider: { label: "Temperatur", min: 20, max: 100, step: 1, def: 95, fmt: (v) => `${v} °C` }, ph: true, reset: true },
  init(W, H) {
    const cols = 6, rows = 4, cw = (W - 30) / cols, ch = (H - 40) / rows, cells = [], bonds = [];
    for (let r = 0; r < rows; r++) for (let k = 0; k < cols; k++) cells.push({ hx: 15 + k * cw + cw / 2, hy: 26 + r * ch + ch / 2, x: 0, y: 0, ox: 0, oy: 0, w: cw * 0.8, h: ch * 0.78 });
    for (const c of cells) { c.x = c.hx; c.y = c.hy; }
    for (let r = 0; r < rows; r++) for (let k = 0; k < cols; k++) { const i = r * cols + k; if (k < cols - 1) bonds.push({ a: i, b: i + 1, s: 1 }); if (r < rows - 1) bonds.push({ a: i, b: i + cols, s: 1 }); }
    return { cells, bonds, time: 0 };
  },
  step(s, dt, c) {
    s.time += dt;
    const heat = Math.max(0, (c.a - 60) / 40), phF = c.ph === 0 ? 0.25 : c.ph === 1 ? 1 : 3;
    for (const b of s.bonds) if (b.s > 0) b.s = Math.max(0, b.s - heat * phF * dt * 0.06 * rnd(0.5, 1.5));
    for (const cell of s.cells) {
      const free = 1 - s.bonds.filter((b: any) => (b.a === s.cells.indexOf(cell) || b.b === s.cells.indexOf(cell))).reduce((m: number, b: any) => Math.max(m, b.s), 0);
      cell.ox += (rnd(-1, 1) * free * 30 - cell.ox * 0.4) * dt; cell.oy += (rnd(-1, 1) * free * 30 - cell.oy * 0.4) * dt;
      cell.x = cell.hx + cell.ox * free * 6; cell.y = cell.hy + cell.oy * free * 6;
    }
  },
  draw(g, s) {
    for (const b of s.bonds) if (b.s > 0.02) { const A = s.cells[b.a], B = s.cells[b.b]; g.strokeStyle = C.caramel; g.globalAlpha = b.s; g.lineWidth = 2 + b.s * 5; g.beginPath(); g.moveTo(A.x, A.y); g.lineTo(B.x, B.y); g.stroke(); }
    g.globalAlpha = 1;
    for (const c of s.cells) {
      g.beginPath(); (g as any).roundRect ? (g as any).roundRect(c.x - c.w / 2, c.y - c.h / 2, c.w, c.h, 8) : g.rect(c.x - c.w / 2, c.y - c.h / 2, c.w, c.h);
      g.fillStyle = C.cell; g.fill(); g.strokeStyle = C.cellRim; g.lineWidth = 1.4; g.stroke();
      dot(g, c.x, c.y, 3, C.cellRim);
    }
  },
  status(s, c) {
    const avg = s.bonds.reduce((a: number, b: any) => a + b.s, 0) / s.bonds.length;
    if (c.a < 60) return "Unter etwa 60 °C bleibt der Kitt zwischen den Zellen intakt: Das Gemüse bleibt fest.";
    if (avg > 0.7) return c.ph === 0 ? "In saurer Umgebung löst sich der Kitt nur sehr langsam. Darum bleiben Kartoffeln in Tomatensauce lange fest." : "Die Hitze beginnt, den Kitt zwischen den Zellen zu lösen.";
    if (avg > 0.3) return "Die Zellen lösen sich voneinander: Das Gemüse wird weich.";
    return c.ph === 2 ? "In basischer Umgebung zerfällt der Kitt besonders schnell. Die Zellen fallen auseinander: matschig." : "Kaum noch Kitt übrig: Das Gemüse zerfällt.";
  },
  readouts(s) { const avg = s.bonds.reduce((a: number, b: any) => a + b.s, 0) / s.bonds.length; return [["Kitt", `${Math.round(avg * 100)} %`], ["Biss", avg > 0.7 ? "fest" : avg > 0.35 ? "weich" : "zerfällt"]]; },
};

/* ---------------- Reduktion: Wasser geht, Geschmack bleibt ---------------- */
const reduktion: Sim = {
  title: "Ebene 2 · Sauce im Topf", scale: "≈ 10 cm",
  controls: { slider: { label: "Eingekocht auf", min: 0.25, max: 1, step: 0.01, def: 1, fmt: (v) => `${Math.round(v * 100)} %` } },
  init(W, H) { return { water: Array.from({ length: 90 }, (_, i) => ({ u: Math.random(), v: Math.random(), ph: rnd(0, 6), k: i / 90 })), taste: Array.from({ length: 22 }, () => ({ u: Math.random(), v: Math.random(), ph: rnd(0, 6), c: [C.roast, C.nut, C.caramel][Math.floor(rnd(0, 3))] })), auto: 1 }; },
  step() {},
  draw(g, s, c, W, H, t) {
    const lvl = c.a, x0 = W * 0.12, x1 = W * 0.88, bottom = H - 18, full = H * 0.2, top = bottom - (bottom - full) * lvl;
    g.fillStyle = "#3f3b38"; g.fillRect(x0 - 8, full - 6, 8, bottom - full + 14); g.fillRect(x1, full - 6, 8, bottom - full + 14); g.fillRect(x0 - 8, bottom, x1 - x0 + 16, 8);
    g.fillStyle = "rgba(143,184,201,.18)"; g.fillRect(x0, top, x1 - x0, bottom - top);
    g.setLineDash([4, 4]); g.strokeStyle = C.sepia; g.beginPath(); g.moveTo(x0, full); g.lineTo(x1, full); g.stroke(); g.setLineDash([]);
    g.font = '600 10px "JetBrains Mono", monospace'; g.fillStyle = C.sepia; g.fillText("START", x1 - 44, full - 6);
    const P = (p: any) => [x0 + 8 + p.u * (x1 - x0 - 16) + Math.sin(t + p.ph) * 3, top + 8 + p.v * (bottom - top - 16) + Math.cos(t * 1.3 + p.ph) * 3];
    s.water.forEach((p: any) => { if (p.k < lvl) { const [x, y] = P(p); dot(g, x, y, 2.6, C.water, C.waterRim, .7); } });
    // aufsteigender Dampf
    for (let i = 0; i < 6; i++) { const x = x0 + 20 + i * ((x1 - x0 - 40) / 5), y = top - 10 - ((t * 30 + i * 17) % 50); g.globalAlpha = 1 - ((t * 30 + i * 17) % 50) / 50; dot(g, x, y, 2.4, C.water); }
    g.globalAlpha = 1;
    s.taste.forEach((p: any) => { const [x, y] = P(p); dot(g, x, y, 4.2, p.c); });
  },
  status(_s, c) {
    const v = c.a;
    if (v > 0.95) return "Die Sauce kocht offen. Wasser verdampft, Geschmack bleibt im Topf.";
    if (v > 0.6) return "Weniger Wasser, gleich viel Geschmack: Die Sauce wird kräftiger.";
    if (v > 0.35) return "Konzentriert und sämig, vor allem mit gelatinehaltigem Fond. Jetzt abschmecken.";
    return "Sehr stark eingekocht: intensiv, sirupartig. Wer am Anfang gesalzen hat, hat jetzt eine versalzene Sauce.";
  },
  readouts(_s, c) { return [["Wasser", `${Math.round(c.a * 100)} %`], ["Geschmack", `× ${(1 / c.a).toFixed(1)}`]]; },
};


/* ---------------- Hefegärung: Teig geht je nach Temperatur auf ---------------- */
const yeastRate = (T: number) => (T >= 55 ? 0 : T <= 2 ? 0 : T < 30 ? Math.pow((T - 2) / 28, 1.6) : Math.max(0, 1 - (T - 30) / 25));
const hefe: Sim = {
  title: "Ebene 2 · Teig mit Hefe und Gasblasen", scale: "≈ 2 cm",
  controls: { slider: { label: "Temperatur", min: 4, max: 65, step: 1, def: 27, fmt: (v) => `${v} °C` }, reset: true },
  init(W, H) {
    return { yeast: Array.from({ length: 24 }, () => ({ a: rnd(0, Math.PI * 2), r: Math.sqrt(Math.random()), dead: false, ph: rnd(0, 6) })),
             bubbles: [] as { a: number; r: number; s: number }[], gas: 0, collapsed: false, time: 0 };
  },
  step(s, dt, c) {
    const T = c.a, rate = yeastRate(T);
    s.time += dt;
    if (T >= 55) for (const y of s.yeast) y.dead = true;
    if (!s.collapsed && rate > 0) {
      s.gas += rate * dt * 0.06;
      if (Math.random() < rate * dt * 5 && s.bubbles.length < 160) s.bubbles.push({ a: rnd(0, Math.PI * 2), r: Math.sqrt(Math.random()) * 0.92, s: rnd(1.5, 3) });
      for (const b of s.bubbles) b.s = Math.min(9, b.s + rate * dt * 0.6);
    }
    if (s.gas > 2.4 && !s.collapsed) s.collapsed = true; // Übergare: Netz reißt
    if (s.collapsed) { s.gas = Math.max(1.1, s.gas - dt * 0.4); for (const b of s.bubbles) b.s = Math.max(2, b.s - dt * 2); }
  },
  draw(g, s, c, W, H, t) {
    const vol = 1 + Math.min(s.gas, 2.4) * 0.55, cx = W / 2, base = H - 22;
    const rx = Math.min(W * 0.42, 70 * Math.sqrt(vol) * 1.25), ry = Math.min(H * 0.8, 46 * vol * (s.collapsed ? 0.75 : 1));
    g.fillStyle = "#4a4642"; g.fillRect(cx - W * 0.44, base, W * 0.88, 8);
    g.beginPath(); g.ellipse(cx, base, rx, ry, 0, Math.PI, 0); g.closePath(); g.fillStyle = "#f3e2bd"; g.fill(); g.strokeStyle = "#c9b083"; g.lineWidth = 1.5; g.stroke();
    const P = (a: number, r: number) => [cx + Math.cos(a) * r * rx * 0.9, base - Math.abs(Math.sin(a)) * r * ry * 0.9 - 4];
    for (const b of s.bubbles) { const [x, y] = P(b.a, b.r); dot(g, x, y, b.s, "#fffaf0", "#c9b083", .8); }
    for (const y of s.yeast) { const [x0, y0] = P(y.a, y.r); const j = y.dead ? 0 : 1.5; dot(g, x0 + Math.sin(t * 2 + y.ph) * j, y0 + Math.cos(t * 2 + y.ph) * j, 3, y.dead ? "#9a948e" : "#b8873a", y.dead ? "#6e6863" : "#7a5a3a", .8); }
    g.font = '600 10px "JetBrains Mono", monospace'; g.fillStyle = C.sepia; g.fillText(`VOLUMEN × ${vol.toFixed(1)}`, 10, 16);
  },
  status(s, c) {
    const T = c.a;
    if (s.collapsed) return "Zu lange gegangen: Das Glutennetz ist überdehnt und reißt, der Teig fällt zusammen (Übergare).";
    if (T >= 55) return "Ab etwa 55–60 °C stirbt die Hefe. Im Ofen ist das gewollt: Der Trieb endet, die Form wird fest.";
    if (T < 8) return "Im Kühlschrank arbeitet die Hefe kaum. Der Teig geht sehr langsam, dafür entstehen mehr Aromen.";
    if (T < 22) return "Kühl: Die Hefe arbeitet gemächlich. Gut für Geschmack und einen flexiblen Zeitplan.";
    if (T <= 35) return "Die Hefe ist sehr aktiv. Sie frisst Zucker und bläst Gas in das Glutennetz: Der Teig geht auf.";
    return "Zu warm für eine angenehme Gare: Die Hefe wird langsamer und bildet weniger feine Aromen.";
  },
  readouts(s, c) {
    const T = c.a, r = yeastRate(T);
    return [["Hefe", T >= 55 ? "tot" : r < 0.1 ? "schläft fast" : r < 0.6 ? "aktiv" : "sehr aktiv"], ["Volumen", `× ${(1 + Math.min(s.gas, 2.4) * 0.55).toFixed(1)}`]];
  },
};

/* ---------------- Chemische Lockerung: Backpulver reagiert zweimal ---------------- */
const lockerung: Sim = {
  title: "Ebene 3 · Backpulver im Teig", scale: "≈ 1 mm",
  controls: { slider: { label: "Temperatur", min: 20, max: 180, step: 1, def: 20, fmt: (v) => `${Math.round(v)} °C` }, toggle: { label: "Teig nass (Flüssigkeit eingerührt)", def: true }, reset: true },
  init(W, H) {
    const P = (n: number) => Array.from({ length: n }, () => ({ x: rnd(14, W - 14), y: rnd(H * .35, H - 24), used: false, slow: Math.random() < 0.4 }));
    return { base: P(28), acid: P(28), bubbles: [] as { x: number; y: number; r: number }[], rise: 0, set: false };
  },
  step(s, dt, c, W, H) {
    const wet = c.b, T = c.a;
    if (T >= 110) s.set = true; // Teig wird fest, Trieb endet
    if (wet && !s.set) {
      const fast = T >= 60 ? 1 : 0;
      for (let i = 0; i < s.base.length; i++) {
        const b = s.base[i], a = s.acid[i];
        if (b.used) continue;
        const ready = a.slow ? fast : 1;            // „langsame“ Säure reagiert erst in der Hitze
        if (ready && Math.random() < dt * (a.slow ? 0.6 : 0.12)) { b.used = a.used = true; s.bubbles.push({ x: (b.x + a.x) / 2, y: (b.y + a.y) / 2, r: 2 }); }
      }
    }
    for (const bb of s.bubbles) { bb.r = Math.min(s.set ? bb.r : 9, bb.r + dt * (2 + c.a / 60)); }
    const target = s.bubbles.length / 28;
    if (!s.set) s.rise += (target - s.rise) * Math.min(1, dt * 2);
  },
  draw(g, s, c, W, H, t) {
    const lift = s.rise * H * 0.22, top = H * 0.32 - lift;
    g.fillStyle = s.set ? "#e6c38a" : "#f3e2bd"; g.fillRect(10, top, W - 20, H - 18 - top);
    g.strokeStyle = "#c9b083"; g.lineWidth = 1.5; g.strokeRect(10, top, W - 20, H - 18 - top);
    g.fillStyle = "#4a4642"; g.fillRect(4, H - 18, W - 8, 8);
    const yMap = (y: number) => top + ((y - H * .35) / (H - 24 - H * .35)) * (H - 30 - top) + 6;
    for (const bb of s.bubbles) dot(g, bb.x, yMap(bb.y), bb.r, "#fffaf0", "#c9b083", .8);
    s.base.forEach((b: any) => { if (!b.used) dot(g, b.x + Math.sin(t + b.x) * 1.2, yMap(b.y), 3, "#ffffff", C.sepia, .8); });
    s.acid.forEach((a: any) => { if (!a.used) dot(g, a.x + Math.cos(t + a.y) * 1.2, yMap(a.y), 3, a.slow ? C.caramel : C.fat, C.sepia, .8); });
  },
  status(s, c) {
    if (!c.b) return "Trockenes Backpulver ruht: Natron und Säure reagieren erst, wenn Flüssigkeit dazukommt.";
    if (s.set) return "Ab gut 100 °C wird der Teig fest. Die Gasblasen sind eingeschlossen, der Kuchen bleibt luftig.";
    if (c.a >= 60) return "In der Hitze reagiert die zweite Säure: Viele neue Blasen, der Teig geht im Ofen richtig auf.";
    return "Nass reagiert ein Teil schon jetzt: erste Blasen. Die zweite Säure wartet auf die Ofenhitze.";
  },
  readouts(s) { const left = s.base.filter((b: any) => !b.used).length; return [["Gasblasen", String(s.bubbles.length)], ["Teig", s.set ? "fest" : "weich"], ["Backpulver übrig", `${Math.round(left / 28 * 100)} %`]]; },
};

const PRESETS: Record<Preset, Sim> = { emulsion, osmose, "pektin-abbau": pektin, reduktion, hefegaerung: hefe, "chemische-lockerung": lockerung };

/** Punkt-Simulation für einen Prozess. Läuft auf Canvas, mit Reglern aus dem Preset. */
export default function ParticleSim({ preset }: { preset: Preset }) {
  const sim = PRESETS[preset];
  const ref = useRef<HTMLCanvasElement>(null);
  const [a, setA] = useState(sim.controls.slider?.def ?? 0);
  const [b, setB] = useState(sim.controls.toggle?.def ?? false);
  const [ph, setPh] = useState(1);
  const [tick, setTick] = useState(0);
  const [reset, setReset] = useState(0);
  const ctl = useRef<Ctl>({ a, b, ph });
  ctl.current = { a, b, ph };
  const stateRef = useRef<any>(null);

  // Osmose läuft beim Öffnen einmal von selbst durch
  useEffect(() => {
    if (preset !== "osmose" && preset !== "reduktion" && preset !== "chemische-lockerung") return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    let raf = 0; const start = performance.now(); const [from, to] = preset === "osmose" ? [0, 1] : preset === "reduktion" ? [1, 0.35] : [20, 180];
    const dur = preset === "chemische-lockerung" ? 12000 : 9000;
    const run = (now: number) => { const p = Math.min(1, (now - start) / dur); setA(from + (to - from) * p); if (p < 1) raf = requestAnimationFrame(run); };
    raf = requestAnimationFrame(run);
    return () => cancelAnimationFrame(raf);
  }, [preset, reset]);

  useEffect(() => {
    const cv = ref.current!; const g = cv.getContext("2d")!;
    let W = 360, H = 240, raf = 0, last = performance.now();
    const size = () => { const dpr = Math.min(2, window.devicePixelRatio || 1); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; g.setTransform(dpr, 0, 0, dpr, 0, 0); };
    size(); stateRef.current = sim.init(W, H, ctl.current);
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let n = 0;
    const frame = (now: number) => {
      const dt = Math.min(0.05, (now - last) / 1000); last = now;
      if (!reduce) sim.step(stateRef.current, dt, ctl.current, W, H);
      g.clearRect(0, 0, W, H); sim.draw(g, stateRef.current, ctl.current, W, H, now / 1000);
      if (++n % 15 === 0) setTick((x) => x + 1);
      raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    const ro = new ResizeObserver(() => { size(); stateRef.current = sim.init(W, H, ctl.current); });
    ro.observe(cv);
    return () => { cancelAnimationFrame(raf); ro.disconnect(); };
  }, [sim, reset]);

  const s = stateRef.current;
  const ro = s ? sim.readouts(s, ctl.current) : [];
  const sl = sim.controls.slider;
  void tick;
  return (
    <div className="vis">
      <div className="vis-head"><span className="mono">{sim.title}</span><span className="mono">{sim.scale}</span></div>
      <canvas ref={ref} className="sim-canvas" aria-label={sim.title} />
      <p className="vis-status">{s ? sim.status(s, ctl.current) : " "}</p>
      {ro.length > 0 && <div className="vis-readouts" style={{ gridTemplateColumns: `repeat(${ro.length}, minmax(0,1fr))` }}>{ro.map(([k, v]) => <div key={k}><span className="mono">{k}</span><b>{v}</b></div>)}</div>}
      <div className="vis-row">
        {sl && <label style={{ flex: "1 1 220px", flexDirection: "column", alignItems: "stretch" }}>
          <span className="mono">{sl.label} · {sl.fmt(a)}</span>
          <input type="range" min={sl.min} max={sl.max} step={sl.step} value={a} onChange={(e) => setA(+e.target.value)} />
        </label>}
        {sim.controls.toggle && <label><input type="checkbox" checked={b} onChange={(e) => setB(e.target.checked)} />{sim.controls.toggle.label}</label>}
        {sim.controls.ph && <div className="seg" role="group" aria-label="pH-Wert">
          {["sauer", "neutral", "basisch"].map((l, i) => <button key={l} type="button" aria-pressed={ph === i} onClick={() => setPh(i)}>{l}</button>)}
        </div>}
        {(sim.controls.reset || preset === "osmose" || preset === "reduktion") && <button type="button" className="vis-btn" onClick={() => setReset((r) => r + 1)}>Neu starten</button>}
      </div>
      <span className="mono">Modell vereinfacht</span>
    </div>
  );
}
