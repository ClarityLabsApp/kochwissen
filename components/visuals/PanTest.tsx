"use client";
import { useMemo, useState } from "react";

type Variant = "pfanne" | "backblech" | "fritteuse";

const mix = (a: string, b: string, t: number) => {
  const h = (s: string) => [1, 3, 5].map((i) => parseInt(s.slice(i, i + 2), 16));
  const A = h(a), B = h(b); t = Math.max(0, Math.min(1, t));
  return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * t).toString(16).padStart(2, "0")).join("");
};

interface State { temp: number; extra: string; result: string; tone: "good" | "mid" | "bad"; status: string; color: string; steam: number; juice: number }

const CFG = {
  pfanne: { label: "Stücke in der Pfanne", min: 1, max: 8, def: 2, wet: "Fleisch nass eingelegt", head: "Pfanne von oben · vorgeheizt auf 210 °C", extra: "Saft in der Pfanne" },
  backblech: { label: "Stücke auf dem Blech", min: 6, max: 36, def: 12, wet: "Nicht getrocknet", head: "Backblech von oben · Ofen 220 °C", extra: "Dampf zwischen den Stücken" },
  fritteuse: { label: "Portionen auf einmal", min: 1, max: 6, def: 2, wet: "Nass ins Öl", head: "Frittiertopf von oben · Öl 180 °C", extra: "Öl im Frittiergut" },
} as const;

function model(v: Variant, n: number, wet: boolean): State {
  if (v === "pfanne") {
    const temp = Math.round(210 - n * 16 - (wet ? 28 : 0));
    const juice = Math.max(0, Math.min(1, (165 - temp) / 70));
    if (temp >= 150) return { temp, extra: juice < 0.05 ? "keiner" : "etwas", result: "braun", tone: "good", color: mix("#a8662e", "#7a4523", (temp - 150) / 50), steam: 0.1, juice,
      status: wet ? "Nasses Fleisch kostet zusätzlich Hitze, aber es reicht noch: Die Oberfläche trocknet und bräunt." : "Genug Hitze übrig: Die Oberfläche trocknet schnell und bräunt." };
    if (temp >= 110) return { temp, extra: "etwas", result: "fleckig", tone: "mid", color: mix("#a39088", "#a8662e", (temp - 110) / 40), steam: 0.5, juice,
      status: "Grenzbereich: Saft tritt aus und verdampft nur langsam. Die Kruste wird fleckig." };
    return { temp, extra: "viel", result: "grau", tone: "bad", color: "#a39088", steam: 0.9, juice,
      status: "Die Pfanne fällt unter 110 °C. Der Saft sammelt sich, das Fleisch kocht grau." };
  }
  if (v === "backblech") {
    const crowd = Math.max(0, (n - 14) / 18);
    const steam = Math.min(1, crowd + (wet ? 0.35 : 0));
    const temp = Math.round(steam > 0.45 ? 100 : 160 - steam * 120);
    if (steam < 0.25) return { temp, extra: "wenig", result: "knusprig", tone: "good", color: mix("#e0ad3a", "#a8662e", 0.55), steam, juice: 0,
      status: "Mit Abstand kann der Dampf entweichen. Die Oberflächen trocknen und werden knusprig." };
    if (steam < 0.6) return { temp, extra: "mittel", result: "teils weich", tone: "mid", color: mix("#efd9a8", "#e0ad3a", 0.5), steam, juice: 0,
      status: wet ? "Das Wasser auf der Oberfläche muss erst verdampfen. Die Kruste kommt spät und bleibt ungleichmäßig." : "Es wird eng: Zwischen den Stücken staut sich Dampf, manche Seiten bleiben weich." };
    return { temp, extra: "viel", result: "weich", tone: "bad", color: "#efd9a8", steam, juice: 0,
      status: "Die Stücke dämpfen sich gegenseitig. Die Oberflächen hängen bei 100 °C fest und werden nicht knusprig." };
  }
  const temp = Math.round(180 - n * 9 - (wet ? 12 : 0));
  if (temp >= 160) return { temp, extra: "wenig", result: "knusprig", tone: "good", color: "#d9a441", steam: (temp - 100) / 100, juice: 0,
    status: "Das Öl bleibt heiß genug. Die Kruste bildet sich schnell und hält das Öl draußen." };
  if (temp >= 145) return { temp, extra: "mittel", result: "etwas fettig", tone: "mid", color: "#e3c27a", steam: (temp - 100) / 100, juice: 0,
    status: "Das Öl kühlt merklich ab. Die Kruste braucht länger, und mehr Öl dringt ein." };
  return { temp, extra: "viel", result: "fettig", tone: "bad", color: "#efd9a8", steam: Math.max(0.05, (temp - 100) / 100), juice: 0,
    status: "Zu viel auf einmal: Das Öl fällt unter 145 °C, das Frittiergut liegt lange darin und saugt sich voll." };
}

/** Steak-, Backblech- oder Fritteusen-Test: Menge und Nässe einstellen, Ergebnis sehen. */
export default function PanTest({ variant = "pfanne" }: { variant?: Variant }) {
  const c = CFG[variant];
  const [n, setN] = useState<number>(c.def);
  const [wet, setWet] = useState(false);
  const s = useMemo(() => model(variant, n, wet), [variant, n, wet]);

  // Positionen der Stücke
  const items = useMemo(() => {
    if (variant === "pfanne") {
      const P = [[170, 150], [120, 110], [220, 190], [220, 105], [115, 195], [170, 62], [170, 238], [88, 150]];
      return P.slice(0, n).map(([x, y], i) => ({ x, y, r: (i * 37) % 60 - 30 }));
    }
    if (variant === "backblech") {
      const cols = 6, cap = 18, out: { x: number; y: number; r: number }[] = [];
      for (let i = 0; i < n; i++) {
        const k = i % cap, layer = Math.floor(i / cap);
        out.push({ x: 62 + (k % cols) * 50 + layer * 14, y: 78 + Math.floor(k / cols) * 62 + layer * 12, r: (i * 53) % 40 - 20 });
      }
      return out;
    }
    const out: { x: number; y: number; r: number }[] = [];
    for (let i = 0; i < n * 7; i++) { const a = i * 2.39996, rr = 14 * Math.sqrt(i + 1); out.push({ x: 170 + Math.cos(a) * Math.min(rr, 95), y: 150 + Math.sin(a) * Math.min(rr, 95), r: (i * 47) % 180 }); }
    return out;
  }, [variant, n]);

  const gaugeY = (t: number) => 40 + ((210 - Math.max(90, Math.min(210, t))) / 120) * 90;
  const toneColor = s.tone === "good" ? "var(--crust)" : s.tone === "bad" ? "#8a7c76" : "var(--ink)";

  return (
    <div className="vis">
      <div className="vis-head"><span className="mono">{c.head}</span></div>
      <svg viewBox="0 0 400 300" role="img" aria-label={`${c.label}: ${n}, Ergebnis ${s.result}`}>
        {variant === "pfanne" && <>
          <rect x="296" y="142" width="104" height="16" rx="8" fill="#2f2b28" />
          <circle cx="170" cy="150" r="128" fill="#2f2b28" /><circle cx="170" cy="150" r="118" fill="#55504b" />
          {items.map((p, i) => <ellipse key={"j" + i} cx={p.x} cy={p.y} rx={34 + s.juice * 22} ry={24 + s.juice * 18} fill="#c9a07a" opacity={0.55 * Math.min(1, s.juice * 2)} />)}
          {items.map((p, i) => (
            <g key={i} transform={`translate(${p.x} ${p.y}) rotate(${p.r})`}>
              <ellipse rx="34" ry="24" fill={s.color} stroke="#efe4cf" strokeWidth="3" style={{ transition: "fill .4s" }} />
              <path d="M-20 -6 Q0 -12 20 -6 M-18 6 Q0 0 18 6" stroke="#efe4cf" strokeWidth="1.5" fill="none" opacity=".5" />
            </g>
          ))}
        </>}
        {variant === "backblech" && <>
          <rect x="22" y="36" width="318" height="240" rx="6" fill="#4a4642" />
          <rect x="30" y="44" width="302" height="224" rx="3" fill="#6d6863" />
          {items.map((p, i) => (
            <g key={i} transform={`translate(${p.x} ${p.y}) rotate(${p.r})`}>
              <path d="M-20 14 L0 -20 L20 14 Q0 22 -20 14 Z" fill={s.color} stroke="#c9a24a" strokeWidth="1.5" style={{ transition: "fill .4s" }} />
            </g>
          ))}
        </>}
        {variant === "fritteuse" && <>
          <circle cx="170" cy="150" r="128" fill="#2f2b28" /><circle cx="170" cy="150" r="116" fill="#c9a24a" opacity=".85" />
          {items.map((p, i) => (
            <rect key={i} x={p.x - 18} y={p.y - 4} width="36" height="8" rx="2" fill={s.color} stroke="#a8862e" strokeWidth="1"
              transform={`rotate(${p.r} ${p.x} ${p.y})`} style={{ transition: "fill .4s" }} />
          ))}
        </>}
        {/* Dampf oder Blasen */}
        <g fill="none" stroke={variant === "fritteuse" ? "#fff8e6" : "#efe4cf"} strokeWidth="1.6" strokeLinecap="round" opacity={Math.min(1, s.steam + 0.1)}>
          {Array.from({ length: Math.round(2 + s.steam * 8) }).map((_, i) => {
            const x = 60 + ((i * 71) % 230), y = 70 + ((i * 113) % 170);
            return variant === "fritteuse"
              ? <circle key={i} className="bubble" cx={x} cy={y} r={2 + (i % 3)} style={{ animationDelay: `${(i % 5) * 0.3}s` }} />
              : <path key={i} className="steam" d={`M${x} ${y} q-5 -8 0 -16 q5 -8 0 -16`} style={{ animationDelay: `${(i % 5) * 0.4}s` }} />;
          })}
        </g>
        {/* Thermometer */}
        <g fontFamily="JetBrains Mono, monospace" fontSize="8.5" fill="#7a5a3a">
          <rect x="356" y="40" width="10" height="90" fill="#e9dcc2" stroke="#d5c3a1" />
          <rect x="356" y="40" width="10" height="45" fill="#b4542a" opacity=".7" />
          <rect x="356" y="85" width="10" height="45" fill="#8fb8c9" opacity=".6" />
          <text x="346" y="32">°C</text>
          <path d={`M352 ${gaugeY(s.temp)} l-7 -4.5 v9 z`} fill="#2b2118" style={{ transition: "d .3s" }} />
        </g>
      </svg>
      <p className="vis-status">{s.status}</p>
      <div className="vis-readouts">
        <div><span className="mono">{variant === "backblech" ? "Oberfläche" : variant === "fritteuse" ? "Öl danach" : "Pfanne danach"}</span><b>{s.temp} °C</b></div>
        <div><span className="mono">{c.extra}</span><b>{s.extra}</b></div>
        <div><span className="mono">Ergebnis</span><b style={{ color: toneColor }}>{s.result}</b></div>
      </div>
      <div className="vis-row">
        <label style={{ flex: "1 1 220px", flexDirection: "column", alignItems: "stretch" }}>
          <span className="mono">{c.label} · {n}</span>
          <input type="range" min={c.min} max={c.max} value={n} onChange={(e) => setN(+e.target.value)} />
        </label>
        <label><input type="checkbox" checked={wet} onChange={(e) => setWet(e.target.checked)} />{c.wet}</label>
      </div>
      <span className="mono">Modell vereinfacht</span>
    </div>
  );
}
