"use client";
import { t, type Lang } from "@/lib/i18n";
import type { LibItem } from "./Library";

/**
 * Die Bibliothek als Inhaltsverzeichnis eines alten Kochbuchs: drei Kapitel (Was passiert, Womit, Wofür),
 * jede Kategorie eine Zeile mit kleinem Aquarell, Punktlinie und Anzahl. Antippen öffnet die Liste.
 * Bild: eigenes Kategoriebild cat-<typ>.webp, sonst ein typischer Eintrag als Stellvertreter.
 */
const CHAPTERS: { key: "what" | "with" | "for"; types: string[] }[] = [
  { key: "what", types: ["prozess"] },
  { key: "with", types: ["zutat", "technik", "stellschraube"] },
  { key: "for", types: ["ziel", "symptom", "gericht", "labor", "experiment"] },
];
const STAND_IN: Record<string, string> = {
  prozess: "g-steak", zutat: "mehl", technik: "schaelen", stellschraube: "umluft-ober-unterhitze",
  ziel: "knusprig", symptom: "steak-grau", gericht: "g-roesti", labor: "l-butter", experiment: "x-rotkohl-indikator",
};

export default function Contents({ items, lang = "de", onOpen, pics }: { items: LibItem[]; lang?: Lang; onOpen: (typ: string) => void; pics: Set<string> }) {
  const T = t(lang);
  const pic = (typ: string) => (pics.has(`cat-${typ}`) ? `cat-${typ}` : pics.has(STAND_IN[typ]) ? STAND_IN[typ] : null);
  return (
    <div className="toc">
      {CHAPTERS.map((c, i) => (
        <section key={c.key} className="toc-ch">
          <h3><span className="mono">{["I", "II", "III"][i]}</span>{T.toc[c.key]}</h3>
          <ul>
            {c.types.map((typ) => {
              const p = pic(typ), n = items.filter((e) => e.typ === typ).length;
              return (
                <li key={typ}>
                  <button type="button" onClick={() => onOpen(typ)}>
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    {p ? <img src={`/illustrationen/${p}.webp`} alt="" width={44} height={44} loading="lazy" /> : <i style={{ background: `var(--t-${typ})` }} />}
                    <span className="nm">{T.types[typ][0]}<small>{T.types[typ][1]}</small></span>
                    <span className="lead" aria-hidden="true" />
                    <span className="ct">{n}</span>
                  </button>
                </li>
              );
            })}
          </ul>
        </section>
      ))}
    </div>
  );
}
