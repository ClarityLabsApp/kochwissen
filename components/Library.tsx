"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { search } from "@/lib/search";

export interface LibItem {
  id: string; typ: string; titel: string; status: string; pilot: boolean;
  links: string[]; verlinkt_von: string[]; synonyme: string[]; kurz: string | null; welten?: string[];
}

const TYPES: [string, string, string][] = [
  ["ziel", "Ziele", "Was will ich erreichen?"],
  ["gericht", "Gerichte", "Warum funktioniert dieses Rezept?"],
  ["experiment", "Experimente", "Zum Ausprobieren in der Küche"],
  ["labor", "Labor", "Grundzutaten selber herstellen"],
  ["symptom", "Symptome", "Was ist schiefgelaufen?"],
  ["prozess", "Prozesse", "Was passiert beim Kochen?"],
  ["technik", "Techniken", "Welcher Handgriff hilft?"],
  ["zutat", "Zutaten", "Was tut eine Zutat?"],
  ["stellschraube", "Stellschrauben", "Woran kann ich drehen?"],
  ["welt", "Lebensmittel-Welten", "Wo begegnet mir das?"],
  ["begriff", "Begriffe", "Was heißt das Wort?"],
];
const SING: Record<string, string> = { prozess: "Prozess", ziel: "Ziel", technik: "Technik", symptom: "Symptom", zutat: "Zutat", stellschraube: "Stellschraube", welt: "Welt", begriff: "Begriff", gericht: "Gericht", experiment: "Experiment", labor: "Labor-Rezept" };
const EXAMPLES = ["Wie werden meine Wedges knuspriger?", "Fleisch wird trocken", "Sauce zu dünn", "Rösti", "Experiment für Kinder", "Mayo gerinnt"];
/** Die drei Einstiege: vom Problem, vom Ziel, vom Prinzip. */
const DOORS: { typ: string; titel: string; frage: string; ids: string[]; alle: string; pfad?: [string, string] }[] = [
  { typ: "symptom", titel: "Etwas ist schiefgegangen", frage: "Finde heraus, warum, und wie es nächstes Mal klappt.", ids: ["steak-grau", "wedges-nicht-knusprig", "sauce-zu-duenn", "mayo-gerinnt", "kuchen-sinkt-ein", "fleisch-trocken"], alle: "Alle Probleme" },
  { typ: "ziel", titel: "Ich will, dass es … wird", frage: "Knuspriger, saftiger, luftiger: die Hebel dafür.", ids: ["knusprig", "saftig", "zart", "luftig", "cremig", "knackig"], alle: "Alle Ziele" },
  { typ: "prozess", titel: "Ich will verstehen", frage: "Was in Pfanne, Ofen und Teig wirklich passiert.", ids: ["maillard-reaktion", "emulsion", "glutenbildung", "staerkeverkleisterung", "eiweiss-denaturierung"], alle: "Alle Prozesse", pfad: ["grundprinzipien", "Lernpfad: Die 10 wichtigsten Prinzipien"] },
];
const DAILY = new Set(["prozess", "gericht", "experiment", "labor"]);
export interface PfadCard { id: string; titel: string; n: number; dauer: string; fuer: string }

/** Bild für einen Eintrag: das eigene, sonst das seiner Welt. */
function pictureOf(e: LibItem, has: Set<string>): string | null {
  if (has.has(e.id)) return e.id;
  return (e.welten ?? []).find((w) => has.has(w)) ?? null;
}

export default function Library({ items, illus = [], pfade = [] }: { items: LibItem[]; illus?: string[]; pfade?: PfadCard[] }) {
  const has = useMemo(() => new Set(illus), [illus]);
  const worlds = items.filter((e) => e.typ === "welt" && has.has(e.id));
  const [q, setQ] = useState("");
  const [active, setActive] = useState<Set<string>>(new Set());
  const [onlyWritten, setOnlyWritten] = useState(false);
  const found = useMemo(() => (q.trim() ? search(items, q) : null), [items, q]);
  const res = found?.scores ?? null;
  const best = (found?.best ?? null) as LibItem | null;
  const isWritten = (e: LibItem) => e.status !== "geplant";
  const byId = useMemo(() => new Map(items.map((e) => [e.id, e])), [items]);
  // Eintrag des Tages: erst im Browser bestimmen, damit er jeden Tag wechselt (die Seite ist statisch gebaut).
  const [daily, setDaily] = useState<LibItem | null>(null);
  useEffect(() => {
    const pool = items.filter((e) => DAILY.has(e.typ) && e.status !== "geplant" && e.kurz);
    const day = Math.floor(Date.now() / 86400000);
    setDaily(pool.length ? pool[(day * 7919) % pool.length] : null);
  }, [items]);
  const openType = (t: string) => {
    setActive(new Set([t]));
    setTimeout(() => document.getElementById("bibliothek")?.scrollIntoView({ behavior: "smooth", block: "start" }), 50);
  };
  const plain = (s: string) => s.replace(/\[\[[a-z0-9-]+\|([^\]]+)\]\]/g, "$1").replace(/\[\[([a-z0-9-]+)\]\]/g, (_, id) => byId.get(id)?.titel ?? id);

  let list = items.filter((e) => (!active.size || active.has(e.typ)) && (!onlyWritten || isWritten(e)) && (!res || res.has(e.id)));
  if (res) list = [...list].sort((a, b) => res.get(b.id)! - res.get(a.id)!);
  const groups = res ? [["treffer", "Treffer", "sortiert nach Passung"] as [string, string, string]] : TYPES;

  return (
    <>
      <div className="search">
        <label className="mono" htmlFor="q">Suche · Alltagssprache funktioniert</label>
        <input id="q" type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="z. B. Wie werden meine Wedges knuspriger?" autoComplete="off" />
        <div className="examples">{EXAMPLES.map((x) => <button key={x} type="button" onClick={() => setQ(x)}>{x}</button>)}</div>
      </div>
      {best && (
        <Link href={`/eintrag/${best.id}`} className={`bestcard${pictureOf(best, has) ? " pic" : ""}`}>
          {pictureOf(best, has) && (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={`/illustrationen/${pictureOf(best, has)}.webp`} alt="" width={160} height={160} />
          )}
          <span className="mono"><i style={{ background: `var(--t-${best.typ})` }} />Beste Antwort · {SING[best.typ]}</span>
          <strong>{best.titel}</strong>
          {best.kurz && <span className="k">{plain(best.kurz)}</span>}
          <span className="go">Eintrag öffnen →</span>
        </Link>
      )}
      {!res && (
        <section className="doors" aria-label="Einstiege">
          {DOORS.map((d) => (
            <div key={d.typ} className="door" style={{ borderTopColor: `var(--t-${d.typ})` }}>
              <h2>{d.titel}</h2>
              <p>{d.frage}</p>
              <div className="chips">
                {d.ids.filter((id) => byId.has(id)).map((id) => (
                  <Link key={id} href={`/eintrag/${id}`} className="chip"><i style={{ background: `var(--t-${d.typ})` }} />{byId.get(id)!.titel}</Link>
                ))}
              </div>
              <div className="door-foot">
                <button type="button" className="linkbtn" onClick={() => openType(d.typ)}>{d.alle} ({items.filter((e) => e.typ === d.typ).length}) →</button>
                {d.pfad && <Link href={`/pfad/${d.pfad[0]}`} className="linkbtn">{d.pfad[1]} →</Link>}
              </div>
            </div>
          ))}
        </section>
      )}
      {!res && daily && (
        <Link href={`/eintrag/${daily.id}`} className={`bestcard daily${pictureOf(daily, has) ? " pic" : ""}`}>
          {pictureOf(daily, has) && (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={`/illustrationen/${pictureOf(daily, has)}.webp`} alt="" width={160} height={160} />
          )}
          <span className="mono"><i style={{ background: `var(--t-${daily.typ})` }} />Eintrag des Tages · {SING[daily.typ]}</span>
          <strong>{daily.titel}</strong>
          {daily.kurz && <span className="k">{plain(daily.kurz)}</span>}
          <span className="go">Lesen →</span>
        </Link>
      )}
      {!res && pfade.length > 0 && (
        <section className="block" aria-label="Lernpfade">
          <span className="mono">Lernpfade · der Reihe nach verstehen</span>
          <div className="pfad-row">
            {pfade.map((p) => (
              <Link key={p.id} href={`/pfad/${p.id}`} className="pfad-card">
                <span className="mono">{p.n} Schritte · {p.dauer}</span>
                <strong>{p.titel}</strong>
                <span className="f">{p.fuer}</span>
              </Link>
            ))}
          </div>
        </section>
      )}
      {!res && worlds.length > 0 && (
        <nav className="worlds" aria-label="Lebensmittel-Welten">
          <span className="mono">Stöbern nach Welt</span>
          <div className="worlds-row">
            {worlds.map((w) => (
              <Link key={w.id} href={`/eintrag/${w.id}`} className="world">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={`/illustrationen/${w.id}.webp`} alt="" width={120} height={120} loading="lazy" />
                <span>{w.titel}</span>
              </Link>
            ))}
          </div>
        </nav>
      )}
      <h2 id="bibliothek" className="libhead">{res ? "Alle Treffer" : "Die ganze Bibliothek"}</h2>
      <div className="typechips" role="group" aria-label="Eintragstyp">
        {TYPES.map(([t, name]) => {
          const n = items.filter((e) => e.typ === t).length;
          if (!n) return null;
          return (
            <button key={t} type="button" className="typechip" aria-pressed={active.has(t)}
              onClick={() => { const s = new Set(active); s.has(t) ? s.delete(t) : s.add(t); setActive(s); }}>
              <i style={{ background: `var(--t-${t})` }} />{name}<span>{n}</span>
            </button>
          );
        })}
      </div>
      <label className="count" style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input type="checkbox" checked={onlyWritten} onChange={(e) => setOnlyWritten(e.target.checked)} />
        Nur ausgeschriebene Einträge · {list.length} von {items.length}
      </label>
      <div className="groups">
        {groups.map(([t, name, sub]) => {
          const g = res ? list : list.filter((e) => e.typ === t);
          if (!g.length) return null;
          return (
            // Geschlossen beim Start; offen bei Suche oder gewähltem Typ. Der key setzt den Zustand bei Filterwechsel zurück.
            <details className="group" key={`${t}-${res ? "s" : ""}-${active.has(t) ? "a" : ""}`} open={!!res || active.has(t)}>
              <summary><h3>{name} <small>{g.length} · {sub}</small></h3></summary>
              <div className="grid">
                {g.map((e) => (
                  <Link key={e.id} href={`/eintrag/${e.id}`} className={`cell${isWritten(e) ? "" : " dim"}`}>
                    <span className="t">{e.titel}</span>
                    <span className="m"><i style={{ background: `var(--t-${e.typ})` }} />{SING[e.typ]}{isWritten(e) ? ` · ${e.status}` : " · geplant"}</span>
                  </Link>
                ))}
              </div>
            </details>
          );
        })}
        {!list.length && <p className="count">Nichts gefunden. Versuche ein anderes Wort, z. B. „saftig“, „Sauce“ oder „Experiment“.</p>}
      </div>
    </>
  );
}
