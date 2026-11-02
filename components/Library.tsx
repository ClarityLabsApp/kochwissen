"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { search } from "@/lib/search";
import { href, t, type Lang } from "@/lib/i18n";

export interface LibItem {
  id: string; typ: string; titel: string; status: string; pilot: boolean;
  links: string[]; verlinkt_von: string[]; synonyme: string[]; kurz: string | null; welten?: string[];
}

const TYPE_ORDER = ["ziel", "gericht", "experiment", "labor", "symptom", "prozess", "technik", "zutat", "stellschraube", "welt", "begriff"];
/** Die drei Einstiege: vom Problem, vom Ziel, vom Prinzip. */
const DOORS: { typ: "symptom" | "ziel" | "prozess"; ids: string[]; pfad?: string }[] = [
  { typ: "symptom", ids: ["steak-grau", "wedges-nicht-knusprig", "sauce-zu-duenn", "mayo-gerinnt", "kuchen-sinkt-ein", "fleisch-trocken"] },
  { typ: "ziel", ids: ["knusprig", "saftig", "zart", "luftig", "cremig", "knackig"] },
  { typ: "prozess", ids: ["maillard-reaktion", "emulsion", "glutenbildung", "staerkeverkleisterung", "eiweiss-denaturierung"], pfad: "grundprinzipien" },
];
const DAILY = new Set(["prozess", "gericht", "experiment", "labor"]);
export interface PfadCard { id: string; titel: string; n: number; dauer: string; fuer: string }

/** Bild für einen Eintrag: das eigene, sonst das seiner Welt. */
function pictureOf(e: LibItem, has: Set<string>): string | null {
  if (has.has(e.id)) return e.id;
  return (e.welten ?? []).find((w) => has.has(w)) ?? null;
}

export default function Library({ items, illus = [], pfade = [], lang = "de" }: { items: LibItem[]; illus?: string[]; pfade?: PfadCard[]; lang?: Lang }) {
  const T = t(lang), S = T.search, ln = (p: string) => href(lang, p);
  const TYPES: [string, string, string][] = TYPE_ORDER.map((k) => [k, T.types[k][0], T.types[k][1]]);
  const SING: Record<string, string> = Object.fromEntries(TYPE_ORDER.map((k) => [k, T.types[k][2]]));
  const EXAMPLES = S.examples;
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
  const groups = res ? [["treffer", S.hits, S.byFit] as [string, string, string]] : TYPES;

  return (
    <>
      <div className="search">
        <label className="mono" htmlFor="q">{S.label}</label>
        <input id="q" type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder={S.placeholder} autoComplete="off" />
        <div className="examples">{EXAMPLES.map((x) => <button key={x} type="button" onClick={() => setQ(x)}>{x}</button>)}</div>
      </div>
      {best && (
        <Link href={ln(`/eintrag/${best.id}`)} className={`bestcard${pictureOf(best, has) ? " pic" : ""}`}>
          {pictureOf(best, has) && (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={`/illustrationen/${pictureOf(best, has)}.webp`} alt="" width={160} height={160} />
          )}
          <span className="mono"><i style={{ background: `var(--t-${best.typ})` }} />{S.best} · {SING[best.typ]}</span>
          <strong>{best.titel}</strong>
          {best.kurz && <span className="k">{plain(best.kurz)}</span>}
          <span className="go">{S.open}</span>
        </Link>
      )}
      {!res && (
        <section className="doors" aria-label="Einstiege">
          {DOORS.map((d) => (
            <div key={d.typ} className="door" style={{ borderTopColor: `var(--t-${d.typ})` }}>
              <h2>{T.doors[d.typ][0]}</h2>
              <p>{T.doors[d.typ][1]}</p>
              <div className="chips">
                {d.ids.filter((id) => byId.has(id)).map((id) => (
                  <Link key={id} href={ln(`/eintrag/${id}`)} className="chip"><i style={{ background: `var(--t-${d.typ})` }} />{byId.get(id)!.titel}</Link>
                ))}
              </div>
              <div className="door-foot">
                <button type="button" className="linkbtn" onClick={() => openType(d.typ)}>{T.doors[d.typ][2]} ({items.filter((e) => e.typ === d.typ).length}) →</button>
                {d.pfad && <Link href={ln(`/pfad/${d.pfad}`)} className="linkbtn">{T.doors.pathLink} →</Link>}
              </div>
            </div>
          ))}
        </section>
      )}
      {!res && daily && (
        <Link href={ln(`/eintrag/${daily.id}`)} className={`bestcard daily${pictureOf(daily, has) ? " pic" : ""}`}>
          {pictureOf(daily, has) && (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={`/illustrationen/${pictureOf(daily, has)}.webp`} alt="" width={160} height={160} />
          )}
          <span className="mono"><i style={{ background: `var(--t-${daily.typ})` }} />{T.daily} · {SING[daily.typ]}</span>
          <strong>{daily.titel}</strong>
          {daily.kurz && <span className="k">{plain(daily.kurz)}</span>}
          <span className="go">{T.read}</span>
        </Link>
      )}
      {!res && pfade.length > 0 && (
        <section className="block" aria-label="Lernpfade">
          <span className="mono">{T.pathsRow}</span>
          <div className="pfad-row">
            {pfade.map((p) => (
              <Link key={p.id} href={ln(`/pfad/${p.id}`)} className="pfad-card">
                <span className="mono">{T.steps(p.n)} · {p.dauer}</span>
                <strong>{p.titel}</strong>
                <span className="f">{p.fuer}</span>
              </Link>
            ))}
          </div>
        </section>
      )}
      {!res && worlds.length > 0 && (
        <nav className="worlds" aria-label="Lebensmittel-Welten">
          <span className="mono">{T.worlds}</span>
          <div className="worlds-row">
            {worlds.map((w) => (
              <Link key={w.id} href={ln(`/eintrag/${w.id}`)} className="world">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={`/illustrationen/${w.id}.webp`} alt="" width={120} height={120} loading="lazy" />
                <span>{w.titel}</span>
              </Link>
            ))}
          </div>
        </nav>
      )}
      <h2 id="bibliothek" className="libhead">{res ? S.allHits : S.whole}</h2>
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
        {S.onlyWritten(list.length, items.length)}
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
                  <Link key={e.id} href={ln(`/eintrag/${e.id}`)} className={`cell${isWritten(e) ? "" : " dim"}`}>
                    <span className="t">{e.titel}</span>
                    <span className="m"><i style={{ background: `var(--t-${e.typ})` }} />{SING[e.typ]}{isWritten(e) ? ` · ${T.status[e.status] ?? e.status}` : ` · ${T.status.geplant}`}</span>
                  </Link>
                ))}
              </div>
            </details>
          );
        })}
        {!list.length && <p className="count">{S.none}</p>}
      </div>
    </>
  );
}
