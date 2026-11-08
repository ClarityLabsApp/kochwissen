"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { search } from "@/lib/search";
import { href, t, type Lang } from "@/lib/i18n";
import { GROUPS, groupOfType } from "@/lib/nav";
import { DOORS } from "@/lib/home";
import { useMemo2 } from "@/lib/memo";

export interface LibItem {
  id: string; typ: string; titel: string; status: string; pilot: boolean;
  links: string[]; verlinkt_von: string[]; synonyme: string[]; kurz: string | null; welten?: string[];
}

const TYPE_ORDER = ["symptom", "ziel", "prozess", "technik", "zutat", "gericht", "experiment", "labor", "stellschraube", "welt", "begriff"];
const DAILY = new Set(["prozess", "gericht", "experiment", "labor"]);
export interface PfadCard { id: string; titel: string; n: number; dauer: string; fuer: string; pics?: string[] }

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
  const [door, setDoor] = useState(0);
  const gelesen = useMemo2("read");
  const readSet = useMemo(() => new Set(gelesen), [gelesen]);
  // Zusätzliche Suchwörter (Ursachen, Faustregeln, andere Sprache) erst laden, wenn jemand sucht.
  const [extras, setExtras] = useState<Record<string, string> | undefined>();
  const wantExtras = q.trim().length > 0;
  useEffect(() => {
    if (!wantExtras || extras) return;
    fetch(`/suche-index/${lang}`).then((r) => (r.ok ? r.json() : undefined)).then((x) => x && setExtras(x)).catch(() => {});
  }, [wantExtras, extras, lang]);
  const found = useMemo(() => (q.trim() ? search(items, q, extras) : null), [items, q, extras]);
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
  // Alte Adressen mit ?k=typ führen auf die neuen Übersichtsseiten; ?q= füllt die Suche (aus dem Menü auf anderen Seiten).
  useEffect(() => {
    const u = new URL(window.location.href);
    const k = u.searchParams.get("k");
    const g = k ? groupOfType(k) : undefined;
    if (g) { window.location.replace(ln(`/${g}`)); return; }
    const q0 = u.searchParams.get("q");
    if (q0) { setQ(q0); setTimeout(() => document.getElementById("q")?.scrollIntoView({ block: "start" }), 50); }
    // Alte geteilte Merklisten-Links (?merk=) führen zur Merkliste.
    const m = u.searchParams.get("merk");
    if (m) { window.location.replace(`${ln("/merkliste")}?merk=${encodeURIComponent(m)}`); return; }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const typing = (v: string) => {
    setQ(v);
    const u = new URL(window.location.href);
    if (v.trim()) u.searchParams.set("q", v); else u.searchParams.delete("q");
    window.history.replaceState(window.history.state, "", u);
  };
  const plain = (s: string) => s.replace(/\[\[[a-z0-9-]+\|([^\]]+)\]\]/g, "$1").replace(/\[\[([a-z0-9-]+)\]\]/g, (_, id) => byId.get(id)?.titel ?? id);

  let list = items.filter((e) => (!active.size || active.has(e.typ)) && (!res || res.has(e.id)));
  if (res) list = [...list].sort((a, b) => res.get(b.id)! - res.get(a.id)!);

  return (
    <>
      <div className="search">
        <label className="mono" htmlFor="q">{S.label}</label>
        <input id="q" type="search" value={q} onChange={(e) => typing(e.target.value)} placeholder={S.placeholder} autoComplete="off" />
        <div className="examples">{EXAMPLES.slice(0, 4).map((x) => <button key={x} type="button" onClick={() => typing(x)}>{x}</button>)}</div>
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
        <section className="doors" aria-label={lang === "en" ? "Ways in" : "Einstiege"}>
          <div className="door-tabs" role="tablist">
            {DOORS.map((d, i) => (
              <button key={d.typ} type="button" role="tab" aria-selected={door === i} onClick={() => setDoor(i)} style={{ ["--c" as string]: `var(--t-${d.typ})` }}>{T.doors.tab[i]}</button>
            ))}
          </div>
          {DOORS.map((d, i) => (
            <div key={d.typ} className={`door${door === i ? "" : " door-off"}`} style={{ borderTopColor: `var(--t-${d.typ})` }}>
              <h2>{T.doors[d.typ as "symptom"][0]}</h2>
              <p>{T.doors[d.typ as "symptom"][1]}</p>
                <ul className="rows">
                  {d.ids.filter((id) => byId.has(id)).map((id) => (
                    <li key={id}><Link href={ln(`/eintrag/${id}`)} className={has.has(id) ? "with-pic" : ""}>
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      {has.has(id) && <img src={`/illustrationen/${id}.webp`} alt="" width={36} height={36} loading="lazy" />}
                      <strong>{byId.get(id)!.titel}</strong>{readSet.has(id) && <small className="read">{T.memo.read}</small>}</Link></li>
                  ))}
                </ul>
              <div className="door-foot">
                <Link className="linkbtn" href={ln(`/${d.group}`)}>{T.doors[d.typ as "symptom"][2]} ({items.filter((e) => GROUPS.find((g) => g.key === d.group)!.types.includes(e.typ)).length}) →</Link>
              </div>
            </div>
          ))}
        </section>
      )}
      {!res && worlds.length > 0 && (
        <nav className="worlds" id="welten" aria-label={lang === "en" ? "Food worlds" : "Lebensmittel-Welten"}>
          <div className="worlds-head"><span className="mono">{T.worlds}</span><span className="nav-panel-lede">{T.hub.worldsLede}</span></div>
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
      {!res && pfade.length > 0 && (
        <section className="block" aria-label={lang === "en" ? "Learning paths" : "Lernpfade"}>
          <span className="mono">{T.pathsRow}</span>
          <div className="pfad-row">
            {pfade.map((p) => (
              <Link key={p.id} href={ln(`/pfad/${p.id}`)} className="pfad-card">
                {p.pics?.length ? <span className="pfad-pics">{p.pics.map((x) => (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img key={x} src={`/illustrationen/${x}.webp`} alt="" width={52} height={52} loading="lazy" />
                ))}</span> : null}
                <span className="mono">{T.steps(p.n)} · {p.dauer}</span>
                <strong>{p.titel}</strong>
                <span className="f">{p.fuer}</span>
              </Link>
            ))}
          </div>
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
      {res && <h2 id="bibliothek" className="libhead">{S.allHits}</h2>}
      {res && <>
      {res && <div className="typechips" role="group" aria-label={lang === "en" ? "Entry type" : "Eintragstyp"}>
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
      </div>}

      <div className="groups">
        {list.length > 0 && (
          <div className="group">
            <h3>{S.hits} <small>{list.length} · {S.byFit}</small></h3>
            <div className="grid">
              {list.map((e) => (
                <Link key={e.id} href={ln(`/eintrag/${e.id}`)} className={`cell${isWritten(e) ? "" : " dim"}`}>
                  <span className="t">{e.titel}</span>
                  <span className="m"><i style={{ background: `var(--t-${e.typ})` }} />{SING[e.typ]}</span>
                </Link>
              ))}
            </div>
          </div>
        )}
        {!list.length && <p className="count">{S.none}</p>}
      </div>
      </>}
    </>
  );
}
