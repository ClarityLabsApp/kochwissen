"use client";
import Link from "next/link";
import { useMemo, useState } from "react";
import { href, type Lang } from "@/lib/i18n";

export interface ErsatzCard { id: string; gruppe: string; fehlt: string; statt: { wie: string; gut?: string }[]; warum: string; achtung?: string; pic: string | null; zu: { id: string; titel: string }[] }

const TX = {
  de: { filter: "Was fehlt dir?", ph: "z. B. Backpulver, Ei, Rahm", all: "Alle", instead: "Stattdessen", why: "Warum das geht", careful: "Achtung", more: "Mehr dazu", none: "Dafür gibt es hier noch keinen Ersatz." },
  en: { filter: "What are you missing?", ph: "e.g. baking powder, egg, cream", all: "All", instead: "Instead", why: "Why it works", careful: "Watch out", more: "More on this", none: "No substitute for that here yet." },
};
const norm = (s: string) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

export default function ErsatzList({ cards, gruppen, lang }: { cards: ErsatzCard[]; gruppen: { id: string; name: string }[]; lang: Lang }) {
  const X = TX[lang];
  const [q, setQ] = useState("");
  const [g, setG] = useState("");
  const list = useMemo(() => {
    const n = norm(q.trim());
    // Nur Wortanfänge im Namen der Zutat, damit „ei“ nicht auch „Weinstein“ findet; „Eier“ findet „Ei“.
    const hit = (text: string) => norm(text).split(/[^a-z0-9]+/).some((w) => w && (w.startsWith(n) || (n.length >= 3 && w.includes(n)) || (w.length >= 2 && n.startsWith(w) && n.length - w.length <= 2)));
    return cards.filter((c) => (!g || c.gruppe === g) && (!n || hit(c.fehlt)));
  }, [cards, q, g]);
  return (
    <>
      <div className="ers-tools">
        <label className="mono" htmlFor="ers-q">{X.filter}</label>
        <input id="ers-q" type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder={X.ph} autoComplete="off" />
        <div className="ers-chips" role="group">
          <button type="button" aria-pressed={!g} onClick={() => setG("")}>{X.all}</button>
          {gruppen.map((x) => <button key={x.id} type="button" aria-pressed={g === x.id} onClick={() => setG(g === x.id ? "" : x.id)}>{x.name}</button>)}
        </div>
      </div>
      {list.length === 0 && <p className="ers-none">{X.none}</p>}
      {gruppen.filter((gr) => list.some((c) => c.gruppe === gr.id)).map((gr) => (
        <section key={gr.id} className="ers-sec">
          <h2>{gr.name}</h2>
          <div className="ers-grid">
            {list.filter((c) => c.gruppe === gr.id).map((c) => (
              <article key={c.id} id={c.id} className="ers-card">
                <header>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  {c.pic && <img src={`/illustrationen/${c.pic}.webp`} alt="" width={56} height={56} loading="lazy" />}
                  <h3>{c.fehlt}</h3>
                </header>
                <span className="mono">{X.instead}</span>
                <ul>{c.statt.map((s) => <li key={s.wie}>{s.wie}{s.gut && <small>{s.gut}</small>}</li>)}</ul>
                <span className="mono">{X.why}</span>
                <p>{c.warum}</p>
                {c.achtung && <p className="ers-warn"><b>{X.careful}:</b> {c.achtung}</p>}
                <div className="ers-links"><span className="mono">{X.more}</span>{c.zu.map((z) => <Link key={z.id} href={href(lang, `/eintrag/${z.id}`)} className="chip">{z.titel}</Link>)}</div>
              </article>
            ))}
          </div>
        </section>
      ))}
    </>
  );
}
