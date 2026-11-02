"use client";
import { useEffect, useRef, useState } from "react";

/* Punkt-Sprache laut DESIGN.md */
const C = { water: "#8fb8c9", waterRim: "#5f8fa3", fat: "#f0d27a", fatRim: "#c9a24a", lab: "#2f6f73", salt: "#ffffff", sepia: "#7a5a3a",
  ink: "#2b2118", roast: "#6b3a1e", nut: "#b8873a", caramel: "#d9822b", meat: "#c97b72", meatRim: "#a9564e", cell: "#c8d9a8", cellRim: "#7f9a5a", sugar: "#e0ad3a" };

export type Preset = "emulsion" | "osmose" | "pektin-abbau" | "reduktion" | "hefegaerung" | "chemische-lockerung" | "waermeleitung" | "schaumbildung" | "diffusion" | "zucker-kristallisation" | "leidenfrost" | "gelbildung-pektin" | "chlorophyll-farbe" | "eiweiss-denaturierung" | "glutenbildung" | "karamellisierung" | "eiskristalle" | "siedepunkt-druck" | "enzym-zartmachen" | "verdampfen" | "staerkeverkleisterung" | "kollagen-gelatine" | "konvektion" | "dampflockerung" | "milchsaeuregaerung";

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

/* ---------------- Wärmeleitung: Hitze wandert durch ein Steak ---------------- */
const doneColor = (tmax: number) => {
  const mix2 = (a: string, b: string, t: number) => { const h = (s: string) => [1, 3, 5].map((i) => parseInt(s.slice(i, i + 2), 16)); const A = h(a), B = h(b); t = Math.max(0, Math.min(1, t)); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * t).toString(16).padStart(2, "0")).join(""); };
  if (tmax < 45) return "#b8494f";
  if (tmax < 57) return mix2("#b8494f", "#d98a86", (tmax - 45) / 12);
  if (tmax < 70) return mix2("#d98a86", "#a39088", (tmax - 57) / 13);
  if (tmax < 140) return "#a39088";
  return mix2("#a8662e", "#5a3018", (tmax - 140) / 60);
};
const waerme: Sim = {
  title: "Ebene 2 · Querschnitt durch ein Steak", scale: "≈ 3 cm",
  controls: { slider: { label: "Pfannentemperatur", min: 100, max: 260, step: 5, def: 220, fmt: (v) => `${Math.round(v)} °C` }, toggle: { label: "Dickes Stück (4 cm statt 2 cm)", def: false }, reset: true },
  init() { const N = 40; return { T: Array(N).fill(5), Tmax: Array(N).fill(5), time: 0, flip: false }; },
  step(s, dt, c) {
    const N = s.T.length, thick = c.b ? 2 : 1, k = 4 / (thick * thick);
    s.time += dt;
    for (let sub = 0; sub < 6; sub++) {
      const T = s.T, nT = T.slice();
      for (let i = 1; i < N - 1; i++) nT[i] = Math.min(100, T[i] + k * (dt / 6) * (T[i - 1] - 2 * T[i] + T[i + 1]) * N * N / 400); // Wasser im Fleisch hält das Innere unter 100 °C
      nT[0] = c.a; nT[N - 1] = T[N - 1] + (25 - T[N - 1]) * 0.02;
      s.T = nT;
    }
    for (let i = 0; i < N; i++) s.Tmax[i] = Math.max(s.Tmax[i], s.T[i]);
  },
  draw(g, s, c, W, H) {
    const N = s.T.length, thick = c.b ? 1 : 0.6, x0 = 20, x1 = W - 70, h = (H - 50) * thick, y0 = 20 + ((H - 50) - h) / 2;
    g.fillStyle = "#4a4642"; g.fillRect(x0 - 6, y0 + h, x1 - x0 + 12, 10);
    for (let i = 0; i < N; i++) { const y = y0 + h - (i + 1) * (h / N); g.fillStyle = doneColor(s.Tmax[i]); g.fillRect(x0, y, x1 - x0, h / N + 0.6); }
    g.strokeStyle = C.ink; g.lineWidth = 1; g.strokeRect(x0, y0, x1 - x0, h);
    // Thermometer am Kern
    const core = s.T[Math.floor(N / 2)], cy = y0 + h / 2;
    g.fillStyle = C.ink; g.beginPath(); g.moveTo(x1 + 6, cy); g.lineTo(x1 + 14, cy - 5); g.lineTo(x1 + 14, cy + 5); g.fill();
    g.font = '600 11px "JetBrains Mono", monospace'; g.fillText(`${Math.round(core)} °C`, x1 + 18, cy + 4);
    g.font = '600 9px "JetBrains Mono", monospace'; g.fillStyle = C.sepia; g.fillText("KERN", x1 + 18, cy - 10); g.fillText("PFANNE", x0, y0 + h + 22); g.fillText("LUFT", x0, y0 - 6);
  },
  status(s) {
    const N = s.T.length, core = s.T[Math.floor(N / 2)], grey = s.Tmax.filter((t: number) => t >= 68 && t < 140).length;
    if (core < 30) return "Die Hitze kriecht langsam von unten nach oben. Die Mitte ist noch kalt.";
    if (core < 54) return grey > 6 ? "Die Mitte ist noch nicht rosa, aber unten wächst schon ein breiter grauer Ring." : "Unten bildet sich die Kruste, die Hitze wandert Schicht für Schicht nach innen.";
    if (core < 62) return "Der Kern ist rosa: Jetzt herausnehmen. Wie breit der graue Ring ist, hängt von der Pfannenhitze ab.";
    return "Der Kern ist durch. Je heißer die Pfanne, desto mehr ist darunter längst übergart.";
  },
  readouts(s) { const N = s.T.length; const grey = s.Tmax.filter((t: number) => t >= 68 && t < 140).length; return [["Kern", `${Math.round(s.T[Math.floor(N / 2)])} °C`], ["Grauer Rand", `${Math.round(grey / N * 100)} %`]]; },
};

/* ---------------- Schaumbildung: Luft einschlagen ---------------- */
const schaum: Sim = {
  title: "Ebene 2 · Eiweiß wird zu Schaum", scale: "≈ 1 mm",
  controls: { slider: { label: "Schlagen", min: 0, max: 1, step: 0.01, def: 0.7, fmt: (v) => (v < 0.05 ? "aus" : v < 0.4 ? "langsam" : v < 0.8 ? "kräftig" : "volle Stufe") }, toggle: { label: "Eine Spur Eigelb (Fett) im Eiweiß", def: false }, reset: true },
  init() { return { b: [] as any[], work: 0, water: 0 }; },
  step(s, dt, c, W, H) {
    const sp = c.a;
    s.work += sp * dt;
    const over = s.work > 26;
    if (sp > 0.05 && s.b.length < 170 && Math.random() < sp * dt * 14) s.b.push({ x: rnd(20, W - 20), y: rnd(H * 0.35, H - 20), r: rnd(9, 15) * (1.2 - Math.min(1, s.work / 18) * 0.6), coat: 0, life: 0 });
    for (const p of s.b) {
      p.life += dt; p.coat = Math.min(1, p.coat + dt * 0.5 * (c.b ? 0.15 : 1));
      if (sp > 0.05 && p.r > 4 && Math.random() < sp * dt * 0.5) p.r *= 0.85;   // Schlagen macht Blasen kleiner
      p.x += Math.sin(p.y / 30 + performance.now() / 500) * sp * 30 * dt; p.y += rnd(-1, 1) * 10 * dt;
      p.x = Math.max(p.r, Math.min(W - p.r, p.x)); p.y = Math.max(H * 0.2, Math.min(H - p.r, p.y));
    }
    const popRate = c.b ? 0.9 : over ? 0.35 : 0.02;
    s.b = s.b.filter((p: any) => !(p.coat < 0.6 && p.life > 0.6 && Math.random() < popRate * dt) && !(over && Math.random() < 0.1 * dt));
    if (over) s.water = Math.min(1, s.water + dt * 0.05);
  },
  draw(g, s, c, W, H) {
    const vol = s.b.length / 170, top = H - 20 - (H - 60) * (0.25 + vol * 0.75);
    g.fillStyle = "rgba(246,238,221,.9)"; g.fillRect(14, top, W - 28, H - 20 - top);
    if (s.water > 0) { g.fillStyle = "rgba(143,184,201,.45)"; g.fillRect(14, H - 20 - s.water * 30, W - 28, s.water * 30); }
    for (const p of s.b) {
      dot(g, p.x, Math.max(top + p.r, p.y), p.r, "rgba(255,255,255,.85)", "#c9b083", 1);
      if (p.coat > 0.2) { g.strokeStyle = C.lab; g.globalAlpha = p.coat; g.lineWidth = 1.6 + (s.work > 26 ? 2 : 0); g.beginPath(); g.arc(p.x, Math.max(top + p.r, p.y), p.r + 1.5, 0, Math.PI * 2); g.stroke(); g.globalAlpha = 1; }
    }
    g.strokeStyle = C.ink; g.lineWidth = 1.2; g.beginPath(); g.moveTo(14, 20); g.lineTo(14, H - 20); g.lineTo(W - 14, H - 20); g.lineTo(W - 14, 20); g.stroke();
  },
  status(s, c) {
    const v = s.b.length / 170;
    if (c.b) return "Schon eine Spur Fett stört die Eiweißhaut um die Blasen: Sie platzen gleich wieder, der Schnee wird nicht steif.";
    if (s.work > 26) return "Zu lange geschlagen: Die Eiweißhüllen werden zu fest, reißen, und Wasser tritt aus. Der Schnee wird krümelig.";
    if (v < 0.25) return "Schlagen bringt Luft hinein. Die Eiweiße entfalten sich und legen sich um jede Blase.";
    if (v < 0.7) return "Weiche Spitzen: Jetzt ist der richtige Moment für den Zucker.";
    return "Steif und glänzend: viele kleine, gut umhüllte Blasen. Jetzt aufhören.";
  },
  readouts(s) { const v = s.b.length / 170; return [["Volumen", `× ${(1 + v * 6).toFixed(1)}`], ["Zustand", s.work > 26 ? "krümelig" : v < 0.25 ? "flüssig" : v < 0.7 ? "weich" : "steif"]]; },
};

/* ---------------- Diffusion: Salz wandert, Aromen bleiben außen ---------------- */
const diffusion: Sim = {
  title: "Ebene 2 · Marinade auf dem Fleisch", scale: "≈ 2 cm",
  controls: { slider: { label: "Zeit", min: 0, max: 1, step: 0.005, def: 0, fmt: (v) => { const h = Math.pow(v, 2) * 48; return h < 1 ? `${Math.round(h * 60)} min` : `${Math.round(h)} h`; } } },
  init(W) { return { salt: Array.from({ length: 70 }, () => ({ x: rnd(16, W - 16), d: Math.random(), ph: rnd(0, 6) })), aroma: Array.from({ length: 14 }, () => ({ x: rnd(16, W - 16), d: Math.random(), ph: rnd(0, 6) })) }; },
  step() {},
  draw(g, s, c, W, H, t) {
    const top = H * 0.24, bot = H - 14, depth = (frac: number) => top + frac * (bot - top);
    g.fillStyle = "#e8b2a8"; g.fillRect(0, top, W, bot - top);
    g.strokeStyle = C.meatRim; g.globalAlpha = .3; for (let y = top + 18; y < bot; y += 22) { g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(W * .3, y - 5, W * .6, y + 5, W, y - 2); g.stroke(); } g.globalAlpha = 1;
    g.fillStyle = "rgba(201,162,74,.35)"; g.fillRect(0, top - 14, W, 14);
    const reach = Math.sqrt(c.a) * 0.95; // Eindringtiefe wächst mit der Wurzel der Zeit
    for (const p of s.salt) dot(g, p.x + Math.sin(t + p.ph) * 1.2, depth(p.d * reach) - (reach < 0.02 ? 7 : 0), 2.6, C.salt, C.sepia, .8);
    for (const a of s.aroma) dot(g, a.x + Math.sin(t * .8 + a.ph) * 1.2, depth(a.d * reach * 0.06) - 6, 4.5, C.caramel, C.sepia, .8);
    g.font = '600 9px "JetBrains Mono", monospace'; g.fillStyle = C.sepia; g.fillText("MARINADE", 8, top - 18); g.fillText("FLEISCH", 8, bot - 6);
  },
  status(_s, c) {
    if (c.a < 0.05) return "Salz (weiß) und Aromen (orange) liegen auf der Oberfläche.";
    if (c.a < 0.35) return "Das kleine Salz beginnt einzuwandern. Die großen Aromastoffe bleiben fast ganz außen.";
    if (c.a < 0.75) return "Nach vielen Stunden ist das Salz tief im Fleisch. Die Aromen der Marinade haften weiterhin vor allem an der Oberfläche.";
    return "Nach ein bis zwei Tagen ist das Salz überall. Aromen aus Kräutern und Öl sind kaum tiefer gekommen: Marinaden würzen die Oberfläche.";
  },
  readouts(_s, c) { return [["Salz", c.a < 0.1 ? "außen" : c.a < 0.6 ? "auf halbem Weg" : "überall"], ["Aromen", "außen"]]; },
};

/* ---------------- Zucker kristallisiert: Kettenreaktion ---------------- */
const kristall: Sim = {
  title: "Ebene 3 · Zuckersirup beim Abkühlen", scale: "≈ 0,1 mm",
  controls: { toggle: { label: "Rühren", def: true }, slider: { label: "Glukosesirup oder Zitrone (Störstoff)", min: 0, max: 1, step: 1, def: 0, fmt: (v) => (v > 0.5 ? "drin" : "keiner") }, reset: true },
  init(W, H) { return { m: Array.from({ length: 150 }, () => ({ x: rnd(10, W - 10), y: rnd(10, H - 10), vx: rnd(-1, 1), vy: rnd(-1, 1), fixed: false })), cryst: 0, seeded: false }; },
  step(s, dt, c, W, H) {
    const inhib = c.a > 0.5, stir = c.b;
    if (!s.seeded && stir && Math.random() < dt * (inhib ? 0.03 : 0.5)) { const p = s.m[Math.floor(Math.random() * s.m.length)]; p.fixed = true; s.seeded = true; }
    const fixed = s.m.filter((p: any) => p.fixed);
    for (const p of s.m) {
      if (p.fixed) continue;
      const sp = stir ? 70 : 25;
      p.vx += rnd(-1, 1) * dt * 3; p.vy += rnd(-1, 1) * dt * 3; const n = Math.hypot(p.vx, p.vy) || 1; p.vx /= n; p.vy /= n;
      p.x += p.vx * sp * dt; p.y += p.vy * sp * dt;
      if (p.x < 6 || p.x > W - 6) p.vx *= -1; if (p.y < 6 || p.y > H - 6) p.vy *= -1;
      p.x = Math.max(6, Math.min(W - 6, p.x)); p.y = Math.max(6, Math.min(H - 6, p.y));
      for (const f of fixed) if (Math.abs(f.x - p.x) < 9 && Math.abs(f.y - p.y) < 9 && Math.random() < (inhib ? 0.15 : 0.9)) {
        const dir = Math.floor(Math.random() * 4); p.x = f.x + [8, -8, 0, 0][dir]; p.y = f.y + [0, 0, 8, -8][dir]; p.fixed = true; break;
      }
    }
    s.cryst = fixed.length / s.m.length;
  },
  draw(g, s) {
    for (const p of s.m) {
      if (p.fixed) { g.fillStyle = "#ffffff"; g.strokeStyle = C.sepia; g.lineWidth = 1; g.fillRect(p.x - 4, p.y - 4, 8, 8); g.strokeRect(p.x - 4, p.y - 4, 8, 8); }
      else dot(g, p.x, p.y, 3, C.sugar, C.sepia, .7);
    }
  },
  status(s, c) {
    if (!s.seeded) return c.b ? "Gerührt wird: Jeden Moment kann sich ein erster Kristall bilden." : "Ohne Rühren bleibt der Sirup glatt. Die Zuckermoleküle schwimmen frei.";
    if (s.cryst < 0.25) return "Ein erster Kristall ist da. Jedes Zuckermolekül, das ihn berührt, lagert sich an.";
    if (c.a > 0.5) return "Der Störstoff bremst: Die Moleküle haften viel schlechter an, der Sirup bleibt länger glatt.";
    return "Kettenreaktion: Der Kristall wächst immer schneller. Das Karamell wird körnig wie Sand.";
  },
  readouts(s) { return [["Kristallisiert", `${Math.round(s.cryst * 100)} %`], ["Sirup", s.cryst < 0.1 ? "glatt" : s.cryst < 0.5 ? "wird körnig" : "sandig"]]; },
};

/* ---------------- Leidenfrost: Tropfen auf der heißen Pfanne ---------------- */
const leiden: Sim = {
  title: "Ebene 1 · Wassertropfen auf der Pfanne", scale: "≈ 5 cm",
  controls: { slider: { label: "Pfannentemperatur", min: 60, max: 300, step: 5, def: 230, fmt: (v) => `${Math.round(v)} °C` } },
  init(W) { return { d: [] as any[], t: 0, born: 0 }; },
  step(s, dt, c, W, H) {
    s.t += dt;
    if (s.d.length < 3 && s.t - s.born > 1.2) { s.d.push({ x: rnd(W * .25, W * .75), r: rnd(9, 13), vx: rnd(-40, 40), life: 0 }); s.born = s.t; }
    const T = c.a;
    for (const d of s.d) {
      d.life += dt;
      const lev = T >= 200;
      const rate = T < 100 ? 0.05 : lev ? 0.12 : 0.6 + (T - 100) / 100 * 1.2;
      d.r -= rate * dt * 3;
      if (lev) { d.x += d.vx * dt; if (d.x < 30 || d.x > W - 30) d.vx *= -1; }
    }
    s.d = s.d.filter((d: any) => d.r > 1.5);
  },
  draw(g, s, c, W, H, t) {
    const T = c.a, py = H * 0.68;
    g.fillStyle = T > 200 ? "#5a4a42" : "#55504b"; g.fillRect(16, py, W - 32, 14); g.fillRect(W - 24, py + 2, 40, 6);
    for (const d of s.d) {
      const lev = T >= 200, y = py - d.r - (lev ? 4 + Math.sin(t * 20 + d.x) * 1 : 0);
      if (lev) { g.fillStyle = "rgba(255,255,255,.55)"; g.fillRect(d.x - d.r, py - 4, d.r * 2, 3); }
      g.beginPath(); g.ellipse(d.x, y, d.r * (lev ? 1 : 1.25), d.r * (lev ? 1 : 0.7), 0, 0, Math.PI * 2); g.fillStyle = C.water; g.fill(); g.strokeStyle = C.waterRim; g.stroke();
      if (T >= 100 && T < 200) for (let i = 0; i < 5; i++) { const a = rnd(Math.PI * 1.1, Math.PI * 1.9); dot(g, d.x + Math.cos(a) * d.r * 1.6, py - 4 + Math.sin(a) * d.r * 1.2, 1.6, "#ffffff"); }
    }
    g.font = '600 10px "JetBrains Mono", monospace'; g.fillStyle = C.sepia; g.fillText(`${Math.round(T)} °C`, 18, py + 32);
  },
  status(_s, c) {
    const T = c.a;
    if (T < 100) return "Unter 100 °C verdunstet der Tropfen nur langsam. Zum Anbraten viel zu kalt.";
    if (T < 200) return "Der Tropfen zischt und verdampft in Sekunden. Die Pfanne ist warm, aber noch nicht heiß genug für Edelstahl.";
    return "Der Tropfen schwebt auf seinem eigenen Dampfpolster und tanzt umher. Jetzt ist die Pfanne bereit.";
  },
  readouts(_s, c) { const T = c.a; return [["Tropfen", T < 100 ? "liegt" : T < 200 ? "zischt weg" : "tanzt"], ["Zum Anbraten", T >= 200 ? "bereit" : "zu kalt"]]; },
};

/* ---------------- Pektin-Gel: Zucker und Säure verbinden die Ketten ---------------- */
const pektinGel: Sim = {
  title: "Ebene 3 · Pektinketten in Fruchtsaft", scale: "≈ 10 nm",
  controls: { toggle: { label: "Genug Zucker", def: true }, slider: { label: "Säure (Zitrone)", min: 0, max: 1, step: 1, def: 1, fmt: (v) => (v > 0.5 ? "drin" : "keine") }, reset: true },
  init(W, H) { return { ch: Array.from({ length: 12 }, () => { const x = rnd(30, W - 30), y = rnd(30, H - 30), a = rnd(0, Math.PI); return { x, y, a, vx: rnd(-10, 10), vy: rnd(-10, 10) }; }), bonds: [] as [number, number][] }; },
  step(s, dt, c, W, H) {
    const gel = c.b && c.a > 0.5;
    for (const k of s.ch) { const m = gel ? 0.25 : 1; k.x += k.vx * dt * m; k.y += k.vy * dt * m; k.a += rnd(-1, 1) * dt * m; if (k.x < 20 || k.x > W - 20) k.vx *= -1; if (k.y < 20 || k.y > H - 20) k.vy *= -1; }
    if (gel && s.bonds.length < 22 && Math.random() < dt * 3) {
      const i = Math.floor(Math.random() * s.ch.length); let best = -1, bd = 1e9;
      s.ch.forEach((k: any, j: number) => { if (j === i || s.bonds.some(([a, b]: number[]) => (a === i && b === j) || (a === j && b === i))) return; const d = Math.hypot(k.x - s.ch[i].x, k.y - s.ch[i].y); if (d < bd) { bd = d; best = j; } });
      if (best >= 0 && bd < 150) s.bonds.push([i, best]);
    }
    if (!gel && s.bonds.length && Math.random() < dt * 4) s.bonds.shift();
  },
  draw(g, s) {
    for (const [a, b] of s.bonds) { const A = s.ch[a], B = s.ch[b]; g.strokeStyle = C.caramel; g.lineWidth = 2; g.setLineDash([3, 3]); g.beginPath(); g.moveTo(A.x, A.y); g.lineTo(B.x, B.y); g.stroke(); g.setLineDash([]); }
    for (const k of s.ch) for (let i = -3; i <= 3; i++) dot(g, k.x + Math.cos(k.a) * i * 9, k.y + Math.sin(k.a) * i * 9 + Math.sin(i) * 3, 3.6, C.cellRim, "#4f6a33", .8);
  },
  status(s, c) {
    if (!c.b && c.a <= 0.5) return "Ohne Zucker und Säure stoßen sich die Pektinketten ab und schwimmen frei. Es bleibt flüssig.";
    if (!c.b) return "Säure allein reicht nicht: Ohne genug Zucker bleiben die Ketten von Wasser umgeben und finden nicht zusammen.";
    if (c.a <= 0.5) return "Zucker allein reicht nicht: Ohne Säure stoßen sich die Ketten weiter ab.";
    return s.bonds.length > 12 ? "Zucker und Säure zusammen: Die Ketten verbinden sich zu einem Netz. Die Konfitüre geliert." : "Die Ketten beginnen sich zu verbinden.";
  },
  readouts(s) { return [["Verbindungen", String(s.bonds.length)], ["Konfitüre", s.bonds.length > 12 ? "geliert" : s.bonds.length > 4 ? "dickt ein" : "flüssig"]]; },
};

/* ---------------- Chlorophyll: Grün wird olivgrün ---------------- */
const gruen: Sim = {
  title: "Ebene 1 · Bohnen im kochenden Wasser", scale: "≈ 10 cm",
  controls: { slider: { label: "Kochzeit", min: 0, max: 12, step: 0.1, def: 0, fmt: (v) => `${v.toFixed(1)} min` }, toggle: { label: "Säure im Wasser (Zitrone, Tomate)", def: false } },
  init(W, H) { return { beans: Array.from({ length: 9 }, (_, i) => ({ x: 40 + (i % 3) * ((W - 80) / 2), y: 50 + Math.floor(i / 3) * ((H - 90) / 2), a: rnd(-0.6, 0.6), ph: rnd(0, 6) })) }; },
  step() {},
  draw(g, s, c, W, H, t) {
    const min = c.a, acid = c.b ? 2.5 : 1;
    const bright = Math.min(1, min / 1.2), olive = Math.max(0, Math.min(1, ((min - 2) * acid) / 7));
    const mix2 = (a: number[], b: number[], k: number) => `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * k)).join(",")})`;
    const base = [104, 150, 74], vivid = [52, 168, 70], dull = [138, 134, 66];
    const col = olive > 0 ? mix2(vivid, dull, olive) : mix2(base, vivid, bright);
    g.fillStyle = "rgba(143,184,201,.25)"; g.fillRect(8, 8, W - 16, H - 16);
    for (const b of s.beans) {
      g.save(); g.translate(b.x + Math.sin(t * 2 + b.ph) * 2, b.y + Math.cos(t * 2 + b.ph) * 2); g.rotate(b.a);
      g.beginPath(); (g as any).roundRect ? (g as any).roundRect(-38, -8, 76, 16, 8) : g.rect(-38, -8, 76, 16); g.fillStyle = col; g.fill(); g.strokeStyle = "rgba(0,0,0,.25)"; g.stroke(); g.restore();
    }
    for (let i = 0; i < 10; i++) { const x = 20 + ((i * 53 + t * 40) % (W - 40)), y = H - 16 - ((t * 60 + i * 37) % (H - 30)); dot(g, x, y, 2, "rgba(255,255,255,.7)"); }
  },
  status(_s, c) {
    const m = c.a;
    if (m < 0.2) return "Rohe Bohnen: mattgrün, weil Luft im Gewebe das Grün verschleiert.";
    if (m < 2) return "In den ersten Minuten entweicht die Luft: Das Grün leuchtet. Jetzt abgießen und in Eiswasser abschrecken.";
    if (c.b) return "Mit Säure im Wasser kippt das Grün viel schneller ins Olivgrüne.";
    return m < 6 ? "Säuren aus den Zellen beginnen, das Chlorophyll zu verändern: Das Grün wird trüber." : "Lange gekocht: olivgrün und weich.";
  },
  readouts(_s, c) { const m = c.a, olive = Math.max(0, ((m - 2) * (c.b ? 2.5 : 1)) / 7); return [["Farbe", m < 0.3 ? "mattgrün" : olive < 0.15 ? "leuchtend" : olive < 0.6 ? "trüber" : "olivgrün"], ["Biss", m < 3 ? "knackig" : m < 7 ? "weich" : "sehr weich"]]; },
};

/* ---------------- Eiweiß-Denaturierung: Fasern pressen Saft aus ---------------- */
const eiweiss: Sim = {
  title: "Ebene 3 · Eiweißfäden im Muskel", scale: "≈ 10 nm",
  controls: { slider: { label: "Kerntemperatur", min: 20, max: 85, step: 1, def: 20, fmt: (v) => `${Math.round(v)} °C` } },
  init(W, H) { return { strands: Array.from({ length: 7 }, (_, i) => ({ y: 30 + i * ((H - 60) / 6), ph: rnd(0, 6) })), water: Array.from({ length: 60 }, () => ({ x: rnd(20, W - 20), y: rnd(30, H - 30), out: rnd(0, 1), ph: rnd(0, 6) })) }; },
  step() {},
  draw(g, s, c, W, H, t) {
    const T = c.a, unfold = Math.max(0, Math.min(1, (T - 45) / 15)), squeeze = Math.max(0, Math.min(1, (T - 64) / 12));
    const x0 = 20 + squeeze * 30, x1 = W - 20 - squeeze * 30;
    for (const st of s.strands) {
      g.beginPath(); g.strokeStyle = squeeze > 0.3 ? "#8c5a50" : C.lab; g.lineWidth = 3;
      for (let x = x0; x <= x1; x += 3) { const amp = 9 * (1 - unfold) + 2, y = st.y + Math.sin(x / (8 + unfold * 10) + st.ph) * amp; if (x === x0) g.moveTo(x, y); else g.lineTo(x, y); }
      g.stroke();
    }
    for (const w of s.water) {
      const gone = w.out < squeeze;
      const x = gone ? (w.x < W / 2 ? 10 + w.out * 10 : W - 10 - w.out * 10) : w.x + Math.sin(t + w.ph) * 2;
      g.globalAlpha = gone ? 0.6 : 1; dot(g, x, w.y + Math.cos(t + w.ph) * 2, 3, C.water, C.waterRim, .7); g.globalAlpha = 1;
    }
  },
  status(_s, c) {
    const T = c.a;
    if (T < 45) return "Roh: Die Eiweißfäden sind gefaltet, Wasser sitzt zwischen ihnen.";
    if (T < 60) return "Ab etwa 50 °C entfalten sich die ersten Eiweiße. Das Fleisch wird gar, bleibt aber saftig.";
    if (T < 66) return "Das saftige Fenster geht zu Ende. Noch hält das Fleisch den größten Teil seines Wassers.";
    return "Über etwa 66 °C ziehen sich die Fasern stark zusammen und pressen Wasser heraus: Das Fleisch wird fest und trocken.";
  },
  readouts(_s, c) { const sq = Math.max(0, Math.min(1, (c.a - 64) / 12)); return [["Saft gehalten", `${Math.round(100 - sq * 45)} %`], ["Garstufe", c.a < 50 ? "roh" : c.a < 58 ? "rosa" : c.a < 66 ? "medium" : "durch"]]; },
};


/* ---------------- Glutenbildung: Kneten verknüpft Eiweiße zu einem Netz, das Gas hält ---------------- */
const gluten: Sim = {
  title: "Ebene 3 · Eiweiße im Teig", scale: "≈ 0,01 mm",
  controls: { slider: { label: "Kneten", min: 0, max: 1, step: 0.01, def: 0, fmt: (v) => (v < 0.05 ? "nur verrührt" : v < 0.35 ? "kurz" : v < 0.7 ? "einige Minuten" : "lange geknetet") }, toggle: { label: "Butter im Teig", def: false }, reset: true },
  init(W, H) {
    const P = [] as any[];
    for (let i = 0; i < 64; i++) P.push({ x: rnd(16, W - 16), y: rnd(16, H - 16), vx: 0, vy: 0, k: i % 2 ? "glia" : "glut", n: 0 });
    return { P, B: [] as [number, number][], bub: 6, held: 0, pops: 0, fat: Array.from({ length: 18 }, () => ({ x: rnd(10, W - 10), y: rnd(10, H - 10) })) };
  },
  step(s, dt, c, W, H) {
    const P = s.P as any[], B = s.B as [number, number][];
    const strength = c.a * (c.b ? 0.45 : 1);
    const target = Math.round(strength * 96);
    if (B.length < target && Math.random() < dt * 30) {
      // nächstes freies Paar verbinden
      const i = Math.floor(Math.random() * P.length), a = P[i];
      if (a.n < 3) {
        let best = -1, bd = 1e9;
        for (let j = 0; j < P.length; j++) { if (j === i || P[j].n >= 3 || B.some(([x, y]) => (x === i && y === j) || (x === j && y === i))) continue; const d = (P[j].x - a.x) ** 2 + (P[j].y - a.y) ** 2; if (d < bd) { bd = d; best = j; } }
        if (best >= 0 && bd < 70 * 70) { B.push([i, best]); a.n++; P[best].n++; }
      }
    }
    while (B.length > target) { const [x, y] = B.pop()!; P[x].n--; P[y].n--; }
    // Bewegung: zittern, Bindungen ziehen wie Federn, Kneten dehnt in Längsrichtung
    const cx = W / 2, cy = H / 2;
    for (const p of P) { p.vx += rnd(-1, 1) * 40 * dt + Math.sin(p.y / 30 + performance.now() / 700) * c.a * 30 * dt; p.vy += rnd(-1, 1) * 40 * dt; }
    for (const [i, j] of B) { const a = P[i], b = P[j], dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy) || 1, f = (d - 30) * 0.9 * dt; a.vx += (dx / d) * f; a.vy += (dy / d) * f; b.vx -= (dx / d) * f; b.vy -= (dy / d) * f; }
    // Gasblase in der Mitte drückt die Eiweiße weg
    for (const p of P) {
      const dx = p.x - cx, dy = p.y - cy, d = Math.hypot(dx, dy) || 1;
      if (d < s.bub + 10) { const push = (s.bub + 10 - d) * 3 * dt; p.vx += (dx / d) * push; p.vy += (dy / d) * push; }
      p.vx *= 0.9; p.vy *= 0.9; p.x = Math.max(8, Math.min(W - 8, p.x + p.vx)); p.y = Math.max(8, Math.min(H - 8, p.y + p.vy));
    }
    // Blase wächst; ein schwaches Netz lässt sie entweichen
    const net = B.length / 96;
    s.bub += dt * 10;
    const limit = 18 + net * Math.min(W, H) * 0.42;
    if (s.bub > limit) { if (net < 0.55) { s.bub = 6; s.pops++; s.held = 0; } else { s.bub = limit; s.held = Math.min(1, s.held + dt); } }
  },
  draw(g, s, c, W, H) {
    if (c.b) for (const f of s.fat) dot(g, f.x, f.y, 5, C.fat, C.fatRim, .8);
    const P = s.P as any[];
    g.strokeStyle = C.lab; g.lineWidth = 2;
    for (const [i, j] of s.B as [number, number][]) { g.beginPath(); g.moveTo(P[i].x, P[i].y); g.lineTo(P[j].x, P[j].y); g.stroke(); }
    const cx = W / 2, cy = H / 2;
    g.beginPath(); g.arc(cx, cy, s.bub, 0, Math.PI * 2); g.fillStyle = "rgba(255,255,255,.55)"; g.fill(); g.strokeStyle = "rgba(43,33,24,.35)"; g.lineWidth = 1; g.stroke();
    g.fillStyle = C.ink; g.font = "10px JetBrains Mono, monospace"; if (s.bub > 22) g.fillText("Gas", cx - 10, cy + 3);
    for (const p of P) dot(g, p.x, p.y, 4.5, p.k === "glut" ? C.lab : C.nut);
  },
  status(s, c) {
    const net = s.B.length / 96;
    if (c.a < 0.05) return "Mehl und Wasser sind nur verrührt: Die beiden Eiweiße (Glutenin und Gliadin) liegen lose nebeneinander. Das Gas entweicht.";
    if (c.b && net < 0.55) return "Butter legt sich zwischen die Eiweiße und verhindert lange Verbindungen. Das Netz bleibt kurz: zart, aber es hält wenig Gas (darum heißt es Mürbeteig).";
    if (net < 0.55) return "Kneten verbindet die Eiweiße zu ersten Strängen. Das Netz ist noch zu löchrig: Die Gasblase platzt immer wieder.";
    return "Ein dehnbares Netz aus Gluten: Es gibt nach, wenn die Gasblase wächst, und hält sie fest. So geht ein Brot auf.";
  },
  readouts(s) { const net = s.B.length / 96; return [["Verbindungen", String(s.B.length)], ["Netz", net < 0.15 ? "keins" : net < 0.55 ? "locker" : net < 0.8 ? "dehnbar" : "elastisch"], ["Gasblase", net < 0.55 ? "entweicht" : "hält"]]; },
};

/* ---------------- Karamellisierung: Zucker schmilzt und zerfällt in neue Stoffe ---------------- */
const karamell: Sim = {
  title: "Ebene 3 · Zucker in der Pfanne", scale: "≈ 0,1 mm",
  controls: { slider: { label: "Temperatur", min: 100, max: 210, step: 1, def: 120, fmt: (v) => `${Math.round(v)} °C` }, reset: true },
  init(W, H) {
    const X = [] as any[];
    for (let i = 0; i < 46; i++) X.push({ x: rnd(16, W - 16), y: rnd(H * 0.35, H - 16), vx: 0, vy: 0, ph: rnd(0, 6), a: rnd(0, 1), frag: [] as any[] });
    return { X, bits: [] as any[] };
  },
  step(s, dt, c, W, H) {
    const T = c.a, melt = Math.max(0, Math.min(1, (T - 150) / 16));
    for (const x of s.X) {
      const m = melt;
      x.vx += rnd(-1, 1) * (8 + m * 60) * dt; x.vy += rnd(-1, 1) * (8 + m * 60) * dt; x.vx *= 0.92; x.vy *= 0.92;
      x.x = Math.max(10, Math.min(W - 10, x.x + x.vx)); x.y = Math.max(H * 0.3, Math.min(H - 10, x.y + x.vy));
    }
    // ab ~165 °C zerfallen Zuckermoleküle in kleinere, farbige und duftende Bruchstücke
    const rate = T > 165 ? (T - 165) / 30 * 10 : 0;
    if (Math.random() < rate * dt && s.bits.length < 160) {
      const x = s.X[Math.floor(Math.random() * s.X.length)];
      const kind = T > 195 ? "bitter" : T > 182 ? (Math.random() < 0.5 ? "roast" : "caramel") : Math.random() < 0.7 ? "caramel" : "nut";
      for (let k = 0; k < 2; k++) s.bits.push({ x: x.x, y: x.y, vx: rnd(-30, 30), vy: rnd(-40, 10), kind, up: kind !== "bitter" && Math.random() < 0.35, life: 0 });
    }
    for (const b of s.bits) { b.life += dt; b.x += b.vx * dt; b.y += (b.vy - (b.up ? 30 : 0)) * dt; b.vx *= 0.97; b.vy *= 0.97; if (!b.up) b.y = Math.max(H * 0.3, Math.min(H - 6, b.y)); }
    s.bits = s.bits.filter((b: any) => !(b.up && b.y < -10));
  },
  draw(g, s, c, W, H, t) {
    const T = c.a, melt = Math.max(0, Math.min(1, (T - 150) / 16)), browned = Math.max(0, Math.min(1, (T - 163) / 32));
    // Schmelze als Fläche, Farbe von klar über gold zu dunkel
    if (melt > 0) {
      const col = browned < 0.4 ? `rgba(224,173,58,${0.15 + browned})` : browned < 0.75 ? "rgba(217,130,43,.75)" : "rgba(107,58,30,.85)";
      g.fillStyle = col; g.fillRect(4, H * 0.3 - 6, W - 8, H * 0.7);
    }
    g.fillStyle = "#3a3633"; g.fillRect(0, H - 4, W, 4);
    for (const x of s.X) {
      g.save(); g.translate(x.x, x.y); g.rotate(x.a + t * melt * 0.5);
      const r = 6 - melt * 2.5; g.fillStyle = melt < 1 ? "#fbf3e2" : C.sugar; g.strokeStyle = "rgba(201,162,74,.8)";
      if (melt < 0.6) { g.fillRect(-r, -r, r * 2, r * 2); g.strokeRect(-r, -r, r * 2, r * 2); } else { g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.fill(); g.stroke(); }
      g.restore();
    }
    const KC: Record<string, string> = { caramel: C.caramel, nut: C.nut, roast: C.roast, bitter: "#3a3633" };
    for (const b of s.bits) dot(g, b.x, b.y, b.up ? 3 : 3.5, KC[b.kind]);
  },
  status(s, c) {
    const T = c.a;
    if (T < 150) return "Unter etwa 150 °C bleiben die Zuckerkristalle fest. Es passiert noch nichts.";
    if (T < 165) return "Der Zucker schmilzt zu einer klaren Flüssigkeit. Noch keine Farbe, noch kein Karamellaroma.";
    if (T < 182) return "Die Zuckermoleküle zerbrechen in hunderte neue Stoffe: goldene Farbe und Karamellduft steigen auf.";
    if (T < 195) return "Bernstein bis dunkel: kräftiges Aroma, die Süße nimmt ab. Jetzt vom Herd nehmen.";
    return "Zu heiß: Es entstehen bittere, dunkle Stoffe. Der Karamell verbrennt.";
  },
  readouts(s, c) { const T = c.a; return [["Zustand", T < 150 ? "Kristalle" : T < 165 ? "flüssig" : "Karamell"], ["Farbe", T < 165 ? "klar" : T < 175 ? "golden" : T < 188 ? "bernstein" : T < 196 ? "dunkel" : "schwarz"], ["Geschmack", T < 165 ? "süß" : T < 188 ? "karamellig" : T < 196 ? "kräftig" : "bitter"]]; },
};

/* ---------------- Eiskristalle: langsam = wenige große, schnell oder gerührt = viele kleine ---------------- */
const eis: Sim = {
  title: "Ebene 3 · Wasser beim Gefrieren", scale: "≈ 0,1 mm",
  controls: { slider: { label: "Gefriertempo", min: 0, max: 1, step: 0.01, def: 0.2, fmt: (v) => (v < 0.3 ? "langsam" : v < 0.7 ? "mittel" : "schnell") }, toggle: { label: "rühren", def: false }, reset: true },
  init(W, H) { return { K: [] as any[], frozen: 0, cells: Array.from({ length: 140 }, () => ({ x: rnd(8, W - 8), y: rnd(8, H - 8), f: false })) }; },
  step(s, dt, c, W, H) {
    const nucRate = (0.6 + c.a * c.a * 25) * (c.b ? 3 : 1);
    if (s.frozen < 0.98 && Math.random() < nucRate * dt) s.K.push({ x: rnd(10, W - 10), y: rnd(10, H - 10), r: 2, a: rnd(0, Math.PI), max: c.b ? 9 : 200 });
    for (const k of s.K) if (k.r < k.max) k.r += 16 * dt;
    if (c.b) for (const k of s.K) { k.x += rnd(-1, 1) * 30 * dt; k.y += rnd(-1, 1) * 30 * dt; }
    let f = 0; for (const p of s.cells) { if (!p.f) p.f = s.K.some((k: any) => (k.x - p.x) ** 2 + (k.y - p.y) ** 2 < k.r * k.r); if (p.f) f++; }
    s.frozen = f / s.cells.length;
    if (c.b && s.frozen > 0.97 && s.K.length < 60) for (let i = 0; i < 4; i++) s.K.push({ x: rnd(10, W - 10), y: rnd(10, H - 10), r: 2, a: rnd(0, Math.PI), max: 9 });
  },
  draw(g, s, _c, W, H) {
    g.fillStyle = "rgba(143,184,201,.18)"; g.fillRect(0, 0, W, H);
    g.save(); g.beginPath(); g.rect(0, 0, W, H); g.clip();
    for (const k of s.K) {
      g.save(); g.translate(k.x, k.y); g.rotate(k.a); g.beginPath();
      for (let i = 0; i < 6; i++) { const a = (i / 6) * Math.PI * 2; g.lineTo(Math.cos(a) * k.r, Math.sin(a) * k.r); }
      g.closePath(); g.fillStyle = "rgba(240,248,252,.9)"; g.fill(); g.strokeStyle = "#5f8fa3"; g.lineWidth = 1; g.stroke();
      if (k.r > 14) { g.strokeStyle = "rgba(95,143,163,.5)"; for (let i = 0; i < 3; i++) { const a = (i / 3) * Math.PI; g.beginPath(); g.moveTo(-Math.cos(a) * k.r * .8, -Math.sin(a) * k.r * .8); g.lineTo(Math.cos(a) * k.r * .8, Math.sin(a) * k.r * .8); g.stroke(); } }
      g.restore();
    }
    g.restore();
  },
  status(s, c) {
    const n = s.K.length, avg = n ? s.K.reduce((a: number, k: any) => a + k.r, 0) / n : 0;
    if (s.frozen < 0.3) return "Die ersten Kristallkeime entstehen. Wie viele es werden, entscheidet über die Struktur.";
    if (c.b || avg < 16) return "Viele kleine Kristalle: Die Masse wird fein und cremig, Zellwände bleiben heil.";
    return "Wenige Kristalle wachsen lange und werden groß: Glace wird körnig, Gemüse wird beim Auftauen matschig.";
  },
  readouts(s) { const n = s.K.length, avg = n ? s.K.reduce((a: number, k: any) => a + k.r, 0) / n : 0; return [["Kristalle", String(n)], ["Größe", n === 0 ? "–" : avg < 12 ? "fein" : avg < 26 ? "mittel" : "grob"], ["gefroren", `${Math.round(s.frozen * 100)} %`]]; },
};

/* ---------------- Siedepunkt: Druck bestimmt, wann Wasser kocht ---------------- */
const SIEDE: [number, string, number][] = [[0.33, "Mount Everest", 71], [0.7, "auf 3000 m", 90], [0.95, "Luzern", 98], [1, "Meereshöhe", 100], [2, "Dampfkochtopf", 120]];
const siede: Sim = {
  title: "Ebene 1 · Topf mit kochendem Wasser", scale: "≈ 20 cm",
  controls: { slider: { label: "Luftdruck", min: 0, max: 4, step: 1, def: 3, fmt: (v) => SIEDE[Math.round(v)][1] } },
  init(W, H) { return { B: [] as any[], T: 20 }; },
  step(s, dt, c, W, H) {
    const [, , boil] = SIEDE[Math.round(c.a)];
    s.T = s.T < boil ? Math.min(boil, s.T + dt * 30) : boil;
    const boiling = s.T >= boil - 0.5;
    if (boiling && Math.random() < dt * 30) s.B.push({ x: rnd(W * 0.25, W * 0.75), y: H * 0.82, r: rnd(2, 5) });
    for (const b of s.B) { b.y -= (40 + b.r * 10) * dt; b.r += dt * 2; }
    s.B = s.B.filter((b: any) => b.y > H * 0.36);
  },
  draw(g, s, c, W, H, t) {
    const [p, , boil] = SIEDE[Math.round(c.a)];
    const L = W * 0.2, R = W * 0.8, top = H * 0.3, bot = H * 0.86;
    g.fillStyle = "rgba(143,184,201,.45)"; g.fillRect(L, top + 10, R - L, bot - top - 10);
    g.strokeStyle = "#2b2118"; g.lineWidth = 3; g.beginPath(); g.moveTo(L, top); g.lineTo(L, bot); g.lineTo(R, bot); g.lineTo(R, top); g.stroke();
    if (p > 1.5) { g.fillStyle = "#3a3633"; g.fillRect(L - 6, top - 10, R - L + 12, 10); g.fillRect(W / 2 - 4, top - 22, 8, 12); }
    for (const b of s.B) dot(g, b.x, b.y, b.r, "rgba(255,255,255,.85)", "rgba(95,143,163,.7)", .8);
    // Luftdruck als Pfeile von oben
    const n = Math.max(1, Math.round(p * 3)); g.strokeStyle = "rgba(43,33,24,.45)"; g.lineWidth = 1.5;
    for (let i = 0; i < n; i++) { const x = L + ((i + 0.5) / n) * (R - L), y0 = 6, y1 = top - (p > 1.5 ? 26 : 8); g.beginPath(); g.moveTo(x, y0); g.lineTo(x, y1); g.lineTo(x - 4, y1 - 6); g.moveTo(x, y1); g.lineTo(x + 4, y1 - 6); g.stroke(); }
    g.fillStyle = "#2b2118"; g.font = "12px JetBrains Mono, monospace"; g.textAlign = "center"; g.fillText(`Wasser ${Math.round(s.T)} °C · kocht bei ${boil} °C`, W / 2, bot + 18); g.textAlign = "left";
    void t;
  },
  status(s, c) {
    const [p, place, boil] = SIEDE[Math.round(c.a)];
    if (s.T < boil - 0.5) return "Das Wasser erwärmt sich. Es kocht, sobald sein Dampf so stark drückt wie die Luft darüber.";
    if (p < 0.9) return `${place}: Weniger Luftdruck, das Wasser kocht schon bei ${boil} °C. Pasta und Eier brauchen länger, mehr Hitze ändert nichts.`;
    if (p > 1.5) return "Der Deckel hält den Dampf zurück, der Druck steigt: Das Wasser wird etwa 120 °C heiß, alles gart viel schneller.";
    return `${place}: Das Wasser kocht bei ${boil} °C und wird nicht heißer, egal wie stark die Flamme ist.`;
  },
  readouts(s, c) { const [p, , boil] = SIEDE[Math.round(c.a)]; return [["Druck", `${p.toFixed(1).replace(".", ",")} bar`], ["kocht bei", `${boil} °C`], ["Garzeit", boil >= 110 ? "≈ ⅓" : boil >= 99 ? "normal" : boil >= 88 ? "länger" : "viel länger"]]; },
};

/* ---------------- Enzyme zerschneiden Eiweißketten (Ananas, Kiwi, Papaya) ---------------- */
const enzymSchere: Sim = {
  title: "Ebene 3 · Eiweißnetz mit Enzymen", scale: "≈ 10 nm",
  controls: { slider: { label: "Zeit", min: 0, max: 1, step: 0.01, def: 0, fmt: (v) => `${Math.round(v * 120)} min` }, toggle: { label: "Ananas vorher gekocht", def: false }, reset: true },
  init(W, H) {
    const P = [] as any[], B = [] as any[]; const cols = 9, rows = 5;
    for (let r = 0; r < rows; r++) for (let q = 0; q < cols; q++) P.push({ x: 20 + q * ((W - 40) / (cols - 1)), y: 20 + r * ((H - 40) / (rows - 1)) });
    for (let r = 0; r < rows; r++) for (let q = 0; q < cols; q++) { const i = r * cols + q; if (q < cols - 1) B.push({ a: i, b: i + 1, cut: 1 }); if (r < rows - 1) B.push({ a: i, b: i + cols, cut: 1 }); }
    return { P, B, S: Array.from({ length: 7 }, () => ({ x: rnd(10, W - 10), y: rnd(10, H - 10), vx: rnd(-1, 1), vy: rnd(-1, 1) })) };
  },
  step(s, dt, c, W, H) {
    if (c.b) return; // gekocht: Enzyme abgeschaltet
    for (const e of s.S) { e.x += e.vx * 50 * dt; e.y += e.vy * 50 * dt; if (e.x < 6 || e.x > W - 6) e.vx *= -1; if (e.y < 6 || e.y > H - 6) e.vy *= -1; }
    const target = Math.round(c.a * s.B.length * 0.9); let cut = s.B.filter((b: any) => !b.cut).length;
    if (cut < target) {
      for (const e of s.S) {
        let best: any = null, bd = 1e9;
        for (const b of s.B) { if (!b.cut) continue; const mx = (s.P[b.a].x + s.P[b.b].x) / 2, my = (s.P[b.a].y + s.P[b.b].y) / 2, d = (mx - e.x) ** 2 + (my - e.y) ** 2; if (d < bd) { bd = d; best = b; } }
        if (best && bd < 900 && cut < target) { best.cut = 0; cut++; }
      }
      if (cut < target && Math.random() < dt * 8) { const open = s.B.filter((b: any) => b.cut); if (open.length) { open[Math.floor(Math.random() * open.length)].cut = 0; } }
    }
    if (cut > target) for (const b of s.B) if (!b.cut && cut > target) { b.cut = 1; cut--; }
  },
  draw(g, s, c) {
    g.lineWidth = 2.5; g.strokeStyle = C.lab;
    for (const b of s.B) if (b.cut) { g.beginPath(); g.moveTo(s.P[b.a].x, s.P[b.a].y); g.lineTo(s.P[b.b].x, s.P[b.b].y); g.stroke(); }
    for (const p of s.P) dot(g, p.x, p.y, 3.2, C.lab);
    for (const e of s.S) {
      if (c.b) { dot(g, e.x, e.y, 6, "#bdb3a4"); continue; }
      g.save(); g.translate(e.x, e.y); g.strokeStyle = "#d9822b"; g.lineWidth = 2.2;
      g.beginPath(); g.moveTo(-6, -6); g.lineTo(6, 6); g.moveTo(-6, 6); g.lineTo(6, -6); g.stroke();
      dot(g, -6, -6, 2.5, "#d9822b"); dot(g, -6, 6, 2.5, "#d9822b"); g.restore();
    }
  },
  status(s, c) {
    const share = s.B.filter((b: any) => !b.cut).length / s.B.length;
    if (c.b) return "Gekocht: Die Hitze hat die Enzyme abgeschaltet. Das Eiweißnetz bleibt ganz, Gelatine wird fest.";
    if (share < 0.08) return "Die Enzyme aus der rohen Frucht (orange Scheren) suchen sich Eiweißketten.";
    if (share < 0.45) return "Erste Ketten sind zerschnitten: Fleisch wird an der Oberfläche mürbe, Gelatine bleibt weich.";
    return "Das Netz zerfällt: Fleisch wird mehlig, Gelatine wird nie fest, Kiwi-Quark wird bitter.";
  },
  readouts(s, c) { const share = s.B.filter((b: any) => !b.cut).length / s.B.length; return [["Enzyme", c.b ? "abgeschaltet" : "aktiv"], ["Netz", share < 0.1 ? "ganz" : share < 0.45 ? "gelockert" : "zerfallen"]]; },
};

const clamp = (v: number, a: number, b: number) => Math.max(a, Math.min(b, v));

/* ---------------- Verdampfen: Die Oberfläche hängt bei 100 °C, bis das Wasser weg ist ---------------- */
const verdampf: Sim = {
  title: "Ebene 2 · Fleischoberfläche in der Pfanne", scale: "≈ 1 mm",
  controls: { slider: { label: "Pfanne", min: 120, max: 240, step: 5, def: 200, fmt: (v) => `${Math.round(v)} °C` }, toggle: { label: "vorher trocken getupft", def: false }, reset: true },
  init(W) { return { wet: 1, T: 20, t: 0, drops: Array.from({ length: 14 }, (_, i) => ({ x: 14 + i * ((W - 60) / 13), r: rnd(4, 7) })), steam: [] as any[], started: false }; },
  step(s, dt, c, W, H) {
    if (s.lastB !== c.b) { s.wet = c.b ? 0.15 : 1; s.T = 20; s.t = 0; s.lastB = c.b; } // Umschalten startet neu
    s.t += dt;
    const pan = c.a;
    if (s.wet > 0) { s.T = Math.min(100, s.T + dt * 60); if (s.T >= 99.5) s.wet = Math.max(0, s.wet - ((pan - 100) / 140) * 0.12 * dt); }
    else s.T += (Math.min(pan - 30, 200) - s.T) * dt * 0.6;
    if (s.wet > 0 && s.T >= 99.5 && Math.random() < dt * 25) { const left = Math.random() < 0.5; s.steam.push({ x: left ? rnd(2, 10) : rnd(W - 64, W - 50), y: H * 0.7, life: 0 }); }
    for (const q of s.steam) { q.y -= 40 * dt; q.x += Math.sin(q.life * 4) * 0.4; q.life += dt; }
    s.steam = s.steam.filter((q: any) => q.life < 1.6);
  },
  draw(g, s, _c, W, H) {
    const base = H * 0.74, gapH = 10 * Math.sqrt(s.wet), top = H * 0.4, bottom = base - 2 - gapH, brown = clamp((s.T - 140) / 60, 0, 1);
    g.fillStyle = "#3a3633"; g.fillRect(0, base, W - 46, H - base);
    g.fillStyle = "#c97b72"; g.fillRect(0, top, W - 46, bottom - top);
    g.fillStyle = `rgb(${Math.round(201 - brown * 90)},${Math.round(123 - brown * 60)},${Math.round(114 - brown * 70)})`; g.fillRect(0, bottom - 8, W - 46, 8);
    for (const d of s.drops) { const r = Math.min(d.r, 5) * Math.sqrt(s.wet); if (r > 0.6) dot(g, d.x, base - 1 - r, r, C.water, C.waterRim, .8); }
    for (const q of s.steam) { g.strokeStyle = `rgba(143,184,201,${1 - q.life / 1.6})`; g.lineWidth = 1.5; g.beginPath(); g.moveTo(q.x, q.y); g.quadraticCurveTo(q.x - 4, q.y - 6, q.x, q.y - 12); g.stroke(); }
    g.fillStyle = C.ink; g.font = "10px JetBrains Mono, monospace"; g.fillText("Fleisch", 8, top + 16); g.fillStyle = "#f3e7d3"; g.fillText("Pfanne", 8, base + 16);
    const tx = W - 24, t0 = 14, t1 = base - 6, y = t1 - (clamp(s.T, 0, 220) / 220) * (t1 - t0);
    g.strokeStyle = C.ink; g.lineWidth = 1; g.strokeRect(tx - 5, t0, 10, t1 - t0);
    g.fillStyle = s.T > 139 ? "#b4542a" : "#8fb8c9"; g.fillRect(tx - 4, y, 8, t1 - y);
    for (const [c, l] of [[100, "100"], [140, "140"]] as const) { const yy = t1 - (c / 220) * (t1 - t0); g.beginPath(); g.moveTo(tx - 9, yy); g.lineTo(tx - 5, yy); g.stroke(); g.fillStyle = C.ink; g.font = "10px JetBrains Mono, monospace"; g.fillText(l, tx - 32, yy + 3); }
  },
  status(s) {
    if (s.T < 99) return "Die Oberfläche erwärmt sich.";
    if (s.wet > 0.02) return "Das Wasser verdampft. Solange noch ein Tropfen da ist, bleibt die Oberfläche bei 100 °C hängen, egal wie heiß die Pfanne ist.";
    if (s.T < 140) return "Das Wasser ist weg. Jetzt steigt die Temperatur über 100 °C.";
    return "Trocken und über 140 °C: Jetzt bräunt die Oberfläche.";
  },
  readouts(s) { return [["Oberfläche", `${Math.round(s.T)} °C`], ["Wasser", `${Math.round(s.wet * 100)} %`], ["Zeit", `${Math.round(s.t)} s`]]; },
};

/* ---------------- Stärkeverkleisterung: Körner nehmen Wasser auf, quellen und platzen ---------------- */
const staerke: Sim = {
  title: "Ebene 3 · Stärkekörner in Wasser", scale: "≈ 0,05 mm",
  controls: { slider: { label: "Temperatur", min: 20, max: 98, step: 1, def: 20, fmt: (v) => `${Math.round(v)} °C` } },
  init(W, H) { return { G: Array.from({ length: 9 }, (_, i) => ({ x: 40 + (i % 3) * ((W - 80) / 2), y: 40 + Math.floor(i / 3) * ((H - 80) / 2), a: rnd(0, 3), ph: rnd(0, 6) })), Wd: Array.from({ length: 90 }, () => ({ x: rnd(6, W - 6), y: rnd(6, H - 6), ph: rnd(0, 6) })) }; },
  step() {},
  draw(g, s, c, W, H, t) {
    const T = c.a, swell = clamp((T - 58) / 22, 0, 1), burst = clamp((T - 82) / 12, 0, 1);
    const free = Math.round(s.Wd.length * (1 - swell * 0.7));
    s.Wd.slice(0, free).forEach((w: any) => dot(g, w.x + Math.sin(t + w.ph) * 2, w.y + Math.cos(t * 1.3 + w.ph) * 2, 2.3, C.water, C.waterRim, .6));
    for (const k of s.G) {
      const rx = 10 + swell * 16, ry = 7 + swell * 13;
      g.save(); g.translate(k.x, k.y); g.rotate(k.a);
      if (burst > 0) { g.strokeStyle = `rgba(184,154,106,${0.4 + burst * 0.5})`; g.lineWidth = 1.4;
        for (let j = 0; j < 7; j++) { const a = (j / 7) * Math.PI * 2 + k.ph; g.beginPath(); g.moveTo(Math.cos(a) * rx * 0.6, Math.sin(a) * ry * 0.6);
          g.bezierCurveTo(Math.cos(a) * rx * (1 + burst), Math.sin(a + 0.6) * ry * (1 + burst), Math.cos(a + 0.4) * rx * (1.2 + burst * 1.4), Math.sin(a) * ry * (1.2 + burst * 1.4), Math.cos(a + 0.8) * rx * (1.3 + burst * 1.8), Math.sin(a + 0.3) * ry * (1.3 + burst * 1.8)); g.stroke(); } }
      g.beginPath(); g.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2); g.fillStyle = `rgba(230,211,174,${1 - burst * 0.45})`; g.fill(); g.strokeStyle = "#b89a6a"; g.lineWidth = 1.2; g.stroke();
      if (swell > 0.1) for (let j = 0; j < Math.round(swell * 6); j++) dot(g, Math.cos(j * 1.7) * rx * 0.5, Math.sin(j * 2.3) * ry * 0.5, 1.8, C.water);
      g.restore();
    }
  },
  status(_s, c) {
    const T = c.a;
    if (T < 58) return "Kalt passiert fast nichts: Die Stärkekörner schwimmen hart und dicht gepackt im Wasser.";
    if (T < 82) return "Ab etwa 60 °C saugen die Körner Wasser auf und quellen. Die Flüssigkeit wird spürbar dicker.";
    return "Die Körner platzen und geben lange Stärkeketten frei. Sie verhaken sich: Die Sauce bindet, der Pudding wird fest.";
  },
  readouts(_s, c) { const T = c.a, sw = clamp((T - 58) / 22, 0, 1); return [["Körner", T < 58 ? "hart" : T < 82 ? "quellen" : "geplatzt"], ["Konsistenz", sw < 0.1 ? "dünn" : sw < 0.8 ? "sämig" : "dick"]]; },
};

/* ---------------- Kollagen wird zu Gelatine: Zeit statt Hitze ---------------- */
const kollagen: Sim = {
  title: "Ebene 3 · Bindegewebe im Schmorfleisch", scale: "≈ 100 nm",
  controls: { slider: { label: "Schmorzeit", min: 0, max: 4, step: 0.05, def: 0, fmt: (v) => `${v.toFixed(1).replace(".", ",")} h` }, toggle: { label: "sprudelnd kochen statt leise simmern", def: false } },
  init(W, H) { return { H: Array.from({ length: 5 }, (_, i) => ({ y: 34 + i * ((H - 68) / 4), ph: rnd(0, 6) })) }; },
  step() {},
  draw(g, s, c, W, H, t) {
    const prog = clamp(c.a / 3, 0, 1), squeeze = c.b ? clamp(c.a / 2, 0, 1) : clamp(c.a / 6, 0, 0.3);
    for (const h of s.H) {
      for (let k = 0; k < 3; k++) {
        g.beginPath(); g.strokeStyle = prog > 0.6 ? "rgba(224,173,58,.9)" : ["#b4542a", "#c97b72", "#8c2f2a"][k]; g.lineWidth = 2.2;
        for (let x = 16; x <= W - 16; x += 3) {
          const tight = (1 - prog) * 7, loose = prog * 16;
          const y = h.y + Math.sin(x / 9 + (k * Math.PI * 2) / 3) * tight + Math.sin(x / (22 + k * 7) + h.ph + k + t * 0.6 * prog) * loose;
          if (x === 16) g.moveTo(x, y); else g.lineTo(x, y);
        }
        g.stroke();
      }
    }
    for (let i = 0; i < 26; i++) { const out = i / 26 < squeeze; const x = out ? (i % 2 ? 8 : W - 8) : 24 + ((i * 53) % (W - 48)); const y = 20 + ((i * 37) % (H - 40)); g.globalAlpha = out ? 0.4 : 0.9; dot(g, x, y, 2.6, C.water, C.waterRim, .6); g.globalAlpha = 1; }
  },
  status(_s, c) {
    const prog = clamp(c.a / 3, 0, 1);
    if (prog < 0.15) return "Bindegewebe besteht aus fest gedrehten Eiweiß-Strängen (Kollagen). Darum ist ein rohes Schmorstück zäh.";
    if (c.b && c.a > 1) return "Die Stränge lösen sich, aber Sprudeln presst gleichzeitig den Saft aus den Muskelfasern: zart, aber trocken und faserig.";
    if (prog < 0.6) return "Feuchte Hitze lockert die Stränge langsam auf. Das braucht Zeit, mehr Hitze beschleunigt es kaum.";
    return "Die Stränge sind zu Gelatine geworden. Sie bindet Wasser: Das Fleisch zerfällt zart, die Sauce wird sämig.";
  },
  readouts(_s, c) { const prog = clamp(c.a / 3, 0, 1), sq = c.b ? clamp(c.a / 2, 0, 1) : clamp(c.a / 6, 0, 0.3); return [["Zartheit", prog < 0.3 ? "zäh" : prog < 0.7 ? "weicher" : "zerfällt"], ["Saftigkeit", sq < 0.35 ? "saftig" : sq < 0.7 ? "trockener" : "trocken"]]; },
};

/* ---------------- Konvektion: Umluft trägt die Hitze schneller heran ---------------- */
const konv: Sim = {
  title: "Ebene 1 · Luft im Backofen", scale: "≈ 40 cm",
  controls: { toggle: { label: "Umluft (Ventilator an)", def: false }, reset: true },
  init(W, H) { return { A: Array.from({ length: 70 }, () => ({ x: rnd(16, W - 16), y: rnd(16, H - 16), a: rnd(0, 6) })), T: 20, t: 0 }; },
  step(s, dt, c, W, H) {
    s.t += dt; const fan = c.b, cx = W / 2, cy = H / 2;
    for (const p of s.A) {
      if (fan) { const dx = p.x - cx, dy = p.y - cy, r = Math.hypot(dx, dy) || 1; p.x += (-dy / r * 120 + rnd(-20, 20)) * dt; p.y += (dx / r * 120 + rnd(-20, 20)) * dt; }
      else { p.y += (p.x < cx ? -1 : 1) * 14 * dt * (p.y > 24 && p.y < H - 24 ? 1 : 0) + rnd(-8, 8) * dt; p.x += (p.y < 30 ? 1 : p.y > H - 30 ? -1 : 0) * 14 * dt + rnd(-8, 8) * dt; }
      p.x = clamp(p.x, 12, W - 12); p.y = clamp(p.y, 12, H - 12);
    }
    s.T += ((180 - s.T) * (fan ? 0.09 : 0.045)) * dt;
  },
  draw(g, s, c, W, H) {
    g.strokeStyle = C.ink; g.lineWidth = 2; g.strokeRect(6, 6, W - 12, H - 12);
    g.strokeStyle = "#b4542a"; g.lineWidth = 3; g.beginPath(); for (let x = 20; x < W - 20; x += 12) g.lineTo(x, H - 14 - (x % 24 ? 4 : 0)); g.stroke();
    if (c.b) { g.save(); g.translate(W - 22, H / 2); g.rotate(s.t * 8); g.strokeStyle = C.ink; g.lineWidth = 2; for (let i = 0; i < 4; i++) { g.rotate(Math.PI / 2); g.beginPath(); g.moveTo(0, 0); g.lineTo(0, 10); g.stroke(); } g.restore(); }
    for (const p of s.A) dot(g, p.x, p.y, 2.2, "rgba(217,130,43,.65)");
    const w = 90, h = 34, x = W / 2 - w / 2, y = H / 2 - h / 2, layer = c.b ? 4 : 13;
    g.fillStyle = "rgba(143,184,201,.35)"; g.fillRect(x - layer, y - layer, w + 2 * layer, h + 2 * layer);
    const k = clamp((s.T - 20) / 160, 0, 1);
    g.fillStyle = `rgb(${Math.round(230 - k * 70)},${Math.round(200 - k * 80)},${Math.round(150 - k * 90)})`; g.fillRect(x, y, w, h);
  },
  status(_s, c) { return c.b ? "Der Ventilator bläst die kühle Luftschicht um das Gargut weg. Heiße Luft trifft direkt auf die Oberfläche: Es wird schneller warm und trocknet schneller." : "Ohne Ventilator steigt warme Luft nur langsam auf. Um das Gargut bleibt eine kühle Luftschicht (blau), die die Hitze bremst."; },
  readouts(s, c) { return [["Oberfläche", `${Math.round(s.T)} °C`], ["Luftschicht", c.b ? "dünn" : "dick"], ["Zeit", `${Math.round(s.t)} s`]]; },
};

/* ---------------- Dampflockerung: Blätterteig hebt sich durch Dampf zwischen den Schichten ---------------- */
const blaetter: Sim = {
  title: "Ebene 2 · Blätterteig im Ofen", scale: "≈ 2 mm",
  controls: { slider: { label: "Backzeit", min: 0, max: 1, step: 0.01, def: 0, fmt: (v) => `${Math.round(v * 15)} min` }, toggle: { label: "Butter war zu warm (verschmiert)", def: false } },
  init() { return {}; },
  step() {},
  draw(g, _s, c, W, H, t) {
    const n = 8, rise = clamp(c.a / 0.5, 0, 1) * (c.b ? 0.25 : 1), brown = clamp((c.a - 0.55) / 0.45, 0, 1);
    const baseY = H - 14, layerH = 6, gap = 4 + rise * 16;
    g.fillStyle = "#3a3633"; g.fillRect(0, baseY, W, 6);
    for (let i = 0; i < n; i++) {
      const y = baseY - (i + 1) * (layerH + (c.b ? 1 : gap));
      g.fillStyle = `rgb(${Math.round(233 - brown * 50)},${Math.round(211 - brown * 70)},${Math.round(166 - brown * 90)})`; g.fillRect(16, y, W - 32, layerH);
      if (i < n - 1) {
        if (c.b) { g.fillStyle = "rgba(240,210,122,.6)"; g.fillRect(16, y - 1, W - 32, 1); }
        else if (rise < 0.05) { g.fillStyle = C.fat; g.fillRect(16, y - 3, W - 32, 3); }
        else for (let k = 0; k < 6; k++) { const x = 30 + k * ((W - 60) / 5); g.strokeStyle = `rgba(143,184,201,${0.8 - brown * 0.5})`; g.lineWidth = 1.2; g.beginPath(); g.arc(x + Math.sin(t * 3 + k + i) * 2, y - gap / 2, Math.max(1.5, gap / 2.6), 0, Math.PI * 2); g.stroke(); }
      }
    }
  },
  status(_s, c) {
    if (c.b) return "War die Butter zu warm, hat sie sich mit dem Teig vermischt. Es gibt keine getrennten Schichten mehr, der Dampf entweicht: Der Teig bleibt flach und zäh.";
    if (c.a < 0.05) return "Hauchdünne Teigschichten, getrennt durch Butter. Im Teig steckt Wasser.";
    if (c.a < 0.55) return "Im heißen Ofen wird das Wasser zu Dampf. Die Butter hält die Schichten getrennt, der Dampf drückt sie auseinander.";
    return "Die Schichten sind fest und gebräunt, die Hohlräume bleiben: blättrig und knusprig.";
  },
  readouts(_s, c) { const rise = clamp(c.a / 0.5, 0, 1) * (c.b ? 0.25 : 1); return [["Höhe", `${Math.round(100 + rise * 250)} %`], ["Schichten", c.b ? "verklebt" : "getrennt"]]; },
};

/* ---------------- Milchsäuregärung: Bakterien machen aus Zucker Säure ---------------- */
const milchsaeure: Sim = {
  title: "Ebene 3 · Milch mit Joghurtbakterien", scale: "≈ 0,01 mm",
  controls: { slider: { label: "Temperatur", min: 4, max: 52, step: 1, def: 43, fmt: (v) => `${Math.round(v)} °C` }, reset: true },
  init(W, H) { return { B: Array.from({ length: 8 }, () => ({ x: rnd(10, W - 10), y: rnd(10, H - 10), a: rnd(0, 6) })), S: Array.from({ length: 60 }, () => ({ x: rnd(6, W - 6), y: rnd(6, H - 6), acid: false })), pH: 6.6, t: 0 }; },
  step(s, dt, c, W, H) {
    const T = c.a, dead = T > 48, rate = dead ? 0 : T < 10 ? 0.05 : clamp(1 - Math.abs(T - 43) / 30, 0.1, 1);
    s.t += dt;
    for (const b of s.B) { b.a += rnd(-1, 1) * dt * 2; b.x = clamp(b.x + Math.cos(b.a) * 18 * dt * (dead ? 0 : 1), 8, W - 8); b.y = clamp(b.y + Math.sin(b.a) * 18 * dt * (dead ? 0 : 1), 8, H - 8); }
    if (!dead && s.B.length < 40 && Math.random() < rate * dt * 2.5) { const p = s.B[Math.floor(Math.random() * s.B.length)]; s.B.push({ x: p.x + 6, y: p.y, a: rnd(0, 6) }); }
    for (const b of s.B) for (const q of s.S) if (!q.acid && Math.random() < rate * dt * 0.35 && (q.x - b.x) ** 2 + (q.y - b.y) ** 2 < 1600) q.acid = true;
    const share = s.S.filter((q: any) => q.acid).length / s.S.length;
    s.pH = 6.6 - share * 2.3;
  },
  draw(g, s, c, W, H) {
    const gel = clamp((5.0 - s.pH) / 0.6, 0, 1);
    if (gel > 0) { g.strokeStyle = `rgba(47,111,115,${gel * 0.35})`; g.lineWidth = 1; for (let i = 0; i < 14; i++) { g.beginPath(); g.moveTo((i * 37) % W, 0); g.lineTo((i * 71 + 40) % W, H); g.stroke(); } }
    for (const q of s.S) dot(g, q.x, q.y, 2.6, q.acid ? "#b4542a" : C.sugar);
    for (const b of s.B) { g.save(); g.translate(b.x, b.y); g.rotate(b.a); g.fillStyle = c.a > 48 ? "#9a948c" : "#4f7a3a"; g.beginPath(); (g as any).roundRect ? (g as any).roundRect(-6, -2.2, 12, 4.4, 2.2) : g.rect(-6, -2.2, 12, 4.4); g.fill(); g.restore(); }
  },
  status(s, c) {
    if (c.a > 48) return "Zu heiß: Über etwa 48 °C sterben die Joghurtbakterien. Die Milch bleibt flüssig.";
    if (c.a < 10) return "Im Kühlschrank arbeiten die Bakterien kaum noch. Darum stellt man fertigen Joghurt kalt.";
    if (s.pH > 5.2) return "Die Bakterien (grün) vermehren sich und verwandeln Milchzucker (gelb) in Milchsäure (rot).";
    if (s.pH > 4.7) return "Die Säure steigt. Das Milcheiweiß beginnt, sich zu einem Netz zu verbinden.";
    return "Sauer genug: Das Milcheiweiß ist zu einem Gel gestockt. Aus Milch ist Joghurt geworden.";
  },
  readouts(s) { return [["pH-Wert", s.pH.toFixed(1).replace(".", ",")], ["Bakterien", String(s.B.length)], ["Milch", s.pH > 5.2 ? "flüssig" : s.pH > 4.7 ? "dickt ein" : "Joghurt"]]; },
};

const PRESETS: Record<Preset, Sim> = { emulsion, osmose, "pektin-abbau": pektin, reduktion, hefegaerung: hefe, "chemische-lockerung": lockerung, waermeleitung: waerme, schaumbildung: schaum, diffusion, "zucker-kristallisation": kristall, leidenfrost: leiden, "gelbildung-pektin": pektinGel, "chlorophyll-farbe": gruen, "eiweiss-denaturierung": eiweiss, glutenbildung: gluten, karamellisierung: karamell, eiskristalle: eis, "siedepunkt-druck": siede, "enzym-zartmachen": enzymSchere, verdampfen: verdampf, staerkeverkleisterung: staerke, "kollagen-gelatine": kollagen, konvektion: konv, dampflockerung: blaetter, milchsaeuregaerung: milchsaeure };

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
    if (!["osmose", "reduktion", "chemische-lockerung", "diffusion", "chlorophyll-farbe", "eiweiss-denaturierung", "glutenbildung", "karamellisierung", "enzym-zartmachen", "staerkeverkleisterung", "kollagen-gelatine", "dampflockerung"].includes(preset)) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    let raf = 0; const start = performance.now(); const [from, to] = preset === "osmose" || preset === "diffusion" ? [0, 1] : preset === "reduktion" ? [1, 0.35] : preset === "chlorophyll-farbe" ? [0, 8] : preset === "eiweiss-denaturierung" ? [20, 80] : preset === "glutenbildung" ? [0, 0.85] : preset === "karamellisierung" ? [120, 190] : preset === "enzym-zartmachen" || preset === "dampflockerung" ? [0, 1] : preset === "staerkeverkleisterung" ? [20, 95] : preset === "kollagen-gelatine" ? [0, 3.5] : [20, 180];
    const dur = preset === "chemische-lockerung" || preset === "karamellisierung" ? 12000 : 9000;
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
        {(sim.controls.reset || ["osmose", "reduktion", "diffusion", "chlorophyll-farbe", "eiweiss-denaturierung"].includes(preset)) && <button type="button" className="vis-btn" onClick={() => setReset((r) => r + 1)}>Neu starten</button>}
      </div>
      <span className="mono">Modell vereinfacht</span>
    </div>
  );
}
