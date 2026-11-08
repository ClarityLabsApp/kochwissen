import type { Lang } from "@/lib/i18n";
import { ALKOHOL_REST } from "@/lib/wein";

/** Wie viel Alkohol nach dem Kochen bleibt: Balken nach USDA-Messwerten (Richtwerte). */
export default function AlcoholChart({ lang = "de" }: { lang?: Lang }) {
  const L = lang === "en" ? 1 : 0;
  const title = lang === "en" ? "How much alcohol stays in the dish" : "Wie viel Alkohol im Gericht bleibt";
  const note = lang === "en" ? "Guide values from USDA measurements; they depend on pot size, heat and whether the pot is covered." : "Richtwerte nach Messungen des US-Landwirtschaftsministeriums; sie hängen von Topfgröße, Hitze und Deckel ab.";
  return (
    <div className="vis">
      <div className="vis-head"><span className="mono">{title}</span></div>
      <ul className="alk">
        {ALKOHOL_REST.map(([label, pct]) => (
          <li key={label[0]}>
            <span className="alk-l">{label[L]}</span>
            <span className="alk-bar"><i style={{ width: `${pct}%` }} /></span>
            <span className="alk-v mono">{pct} %</span>
          </li>
        ))}
      </ul>
      <p className="vis-note">{note}</p>
    </div>
  );
}
