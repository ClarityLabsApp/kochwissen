import EN from "./sim-en.json";
import type { Lang } from "./i18n";

/**
 * Texte der Animationen übersetzen. Die Simulationen sind auf Deutsch geschrieben;
 * für Englisch wird jeder angezeigte Text hier nachgeschlagen: zuerst wörtlich,
 * dann über Muster für Texte mit Zahlen. Unbekanntes bleibt unverändert.
 */
const DICT = EN as Record<string, string>;
const PAT: [RegExp, (m: RegExpMatchArray, t: (s: string) => string) => string][] = [
  [/^(.+) Tage$/, (m) => `${m[1]} days`],
  [/^(.+) Monate$/, (m) => `${m[1]} months`],
  [/^Tag (\d+)$/, (m) => `Day ${m[1]}`],
  [/^VOLUMEN × (.+)$/, (m) => `VOLUME × ${m[1]}`],
  [/^PFANNE · (.+)$/, (m) => `PAN · ${m[1]}`],
  [/^Pfanne (\d.*)$/, (m) => `Pan ${m[1]}`],
  [/^Wasser (.+) · kocht bei (.+)$/, (m) => `Water ${m[1]} · boils at ${m[2]}`],
  [/^raucht ab etwa (.+)$/, (m) => `smokes from about ${m[1]}`],
  [/^(.+) verträgt diese Hitze noch\.$/, (m, t) => `${t(m[1])} can still take this heat.`],
  [/^(.+): Das Wasser kocht bei (.+) und wird nicht heißer, egal wie stark die Flamme ist\.$/, (m, t) => `${t(m[1])}: the water boils at ${m[2]} and gets no hotter, however strong the flame.`],
  [/^(.+): Weniger Luftdruck, das Wasser kocht schon bei (.+)\. Pasta und Eier brauchen länger, mehr Hitze ändert nichts\.$/, (m, t) => `${t(m[1])}: lower air pressure, so the water already boils at ${m[2]}. Pasta and eggs take longer; more heat changes nothing.`],
  [/^(.+): (.+), Ergebnis (.+)$/, (m, t) => `${t(m[1])}: ${m[2]}, result ${t(m[3])}`],
  [/^(\S+) und (\S+)$/, (m, t) => `${t(m[1])} and ${t(m[2])}`],
];

export function simTr(lang: Lang): (s: string) => string {
  if (lang === "de") return (s) => s;
  const t = (s: string): string => {
    if (!s) return s;
    const hit = DICT[s];
    if (hit) return hit;
    for (const [re, f] of PAT) { const m = s.match(re); if (m) return f(m, t); }
    // Zahlen mit Dezimalkomma (z. B. „≈ 0,05 mm“, „1,5 h“)
    return s.replace(/(\d),(\d)/g, "$1.$2");
  };
  return t;
}
