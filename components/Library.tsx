"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { search } from "@/lib/search";
import { href, t, type Lang } from "@/lib/i18n";
import Contents from "./Contents";

export interface LibItem {
  id: string; typ: string; titel: string; status: string; pilot: boolean;
  links: string[]; verlinkt_von: string[]; synonyme: string[]; kurz: string | null; welten?: string[];
}

const TYPE_ORDER = ["ziel", "gericht", "experiment", "labor", "symptom", "prozess", "technik", "zutat", "stellschraube", "welt", "begriff"];
/** Die drei Einstiege: vom Problem, vom Ziel, vom Prinzip. */
const DOORS: { typ: "symptom" | "ziel" | "prozess"; ids: string[] }[] = [
  { typ: "symptom", ids: ["steak-grau", "sauce-zu-duenn", "mayo-gerinnt", "kuchen-sinkt-ein"] },
  { typ: "ziel", ids: ["knusprig", "saftig", "luftig", "cremig"] },
  { typ: "prozess", ids: ["maillard-reaktion", "emulsion", "glutenbildung", "staerkeverkleisterung"] },
];
/** Wie jede Kategorie als Liste erscheint: kurze Namen als Chips, mit Bild als Kacheln, sonst kompakte Zeilen in Gruppen. */
const AS_CHIPS = new Set<string>();
const AS_TILES = new Set(["gericht", "experiment", "labor", "welt", "zutat"]);
const THEMES: [string, string, string[]][] = [
  ["Hitze und Bräunung", "Heat and browning", ["maillard-reaktion", "karamellisierung", "basen-braeunung", "pyrolyse", "waermeleitung", "waermestrahlung", "konvektion", "verdampfen", "leidenfrost", "siedepunkt-druck", "rauchpunkt", "pochieren-proz", "dampflockerung"]],
  ["Wasser, Salz und Zucker", "Water, salt and sugar", ["osmose", "diffusion", "wasserbindung-salz", "poekeln", "wasseraktivitaet", "zucker-feuchtigkeit", "reduktion", "zucker-kristallisation", "eiskristalle", "gefrierpunkt-senkung"]],
  ["Eiweiß", "Protein", ["eiweiss-denaturierung", "eiweiss-gerinnung", "saeure-denaturierung", "kollagen-gelatine", "gelbildung-gelatine", "glutenbildung", "schaumbildung", "fleischreifung", "enzym-zartmachen"]],
  ["Stärke und Pflanzen", "Starch and plants", ["staerkeverkleisterung", "retrogradation", "amylase", "pektin-abbau", "kalzium-pektin", "gelbildung-pektin", "chlorophyll-farbe", "anthocyan-farbe", "enzym-braeunung"]],
  ["Fett und Aroma", "Fat and aroma", ["emulsion", "fett-ausbraten", "fett-kristallisation", "oxidation-fett", "aroma-loeslichkeit", "aroma-blooming"]],
  ["Gärung und Lockerung", "Fermentation and raising", ["hefegaerung", "milchsaeuregaerung", "chemische-lockerung", "keimwachstum"]],
  ["Geschmack", "Taste", ["umami", "salz-geschmack", "schaerfe"]],
];
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
  const [sub, setSub] = useState<string | null>(null);
  const [door, setDoor] = useState(0);
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
  // Die gewählte Kategorie steht in der Adresse (?k=prozess), damit „Zurück“ im Browser zum Molekül führt.
  const scrollLib = () => setTimeout(() => document.getElementById("bibliothek")?.scrollIntoView({ behavior: "smooth", block: "start" }), 50);
  const openType = (t: string) => {
    setActive(new Set([t])); setSub(null);
    const u = new URL(window.location.href); u.searchParams.set("k", t);
    window.history.pushState({ k: t }, "", u);
    scrollLib();
  };
  const closeType = () => {
    if (window.history.state?.k) window.history.back();
    else { setActive(new Set()); const u = new URL(window.location.href); u.searchParams.delete("k"); window.history.replaceState(null, "", u); scrollLib(); }
  };
  useEffect(() => {
    const sync = () => {
      const k = new URL(window.location.href).searchParams.get("k");
      setActive(k && T.types[k] ? new Set([k]) : new Set()); setSub(null);
      if (document.getElementById("bibliothek")) scrollLib();
    };
    const k0 = new URL(window.location.href).searchParams.get("k");
    if (k0 && T.types[k0]) { setActive(new Set([k0])); scrollLib(); }
    window.addEventListener("popstate", sync);
    return () => window.removeEventListener("popstate", sync);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const plain = (s: string) => s.replace(/\[\[[a-z0-9-]+\|([^\]]+)\]\]/g, "$1").replace(/\[\[([a-z0-9-]+)\]\]/g, (_, id) => byId.get(id)?.titel ?? id);

  const subgroups = (typ: string, g: LibItem[]): [string, LibItem[]][] => {
    if (typ === "prozess") {
      const out: [string, LibItem[]][] = THEMES.map(([de, en, ids]) => [lang === "en" ? en : de, ids.map((id) => g.find((e) => e.id === id)).filter(Boolean) as LibItem[]]);
      const seen = new Set(THEMES.flatMap((x) => x[2]));
      const rest = g.filter((e) => !seen.has(e.id));
      if (rest.length) out.push([lang === "en" ? "Other" : "Weitere", rest]);
      return out.filter(([, r]) => r.length);
    }
    const m = new Map<string, LibItem[]>();
    for (const e of g) { const w = e.welten?.[0] ?? ""; m.set(w, [...(m.get(w) ?? []), e]); }
    return [...m.entries()].sort((a, b) => (a[0] ? 0 : 1) - (b[0] ? 0 : 1) || b[1].length - a[1].length)
      .map(([w, r]) => [w ? (byId.get(w)?.titel ?? w) : (lang === "en" ? "Other" : "Weitere"), r]);
  };
  let list = items.filter((e) => (!active.size || active.has(e.typ)) && (!res || res.has(e.id)));
  if (res) list = [...list].sort((a, b) => res.get(b.id)! - res.get(a.id)!);
  const groups = res ? [["treffer", S.hits, S.byFit] as [string, string, string]] : TYPES;

  return (
    <>
      <div className="search">
        <label className="mono" htmlFor="q">{S.label}</label>
        <input id="q" type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder={S.placeholder} autoComplete="off" />
        <div className="examples">{EXAMPLES.slice(0, 4).map((x) => <button key={x} type="button" onClick={() => setQ(x)}>{x}</button>)}</div>
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
              <h2>{T.doors[d.typ][0]}</h2>
              <p>{T.doors[d.typ][1]}</p>
                <ul className="rows">
                  {d.ids.filter((id) => byId.has(id)).map((id) => (
                    <li key={id}><Link href={ln(`/eintrag/${id}`)} className={has.has(id) ? "with-pic" : ""}>
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      {has.has(id) && <img src={`/illustrationen/${id}.webp`} alt="" width={36} height={36} loading="lazy" />}
                      <strong>{byId.get(id)!.titel}</strong></Link></li>
                  ))}
                </ul>
              <div className="door-foot">
                <button type="button" className="linkbtn" onClick={() => openType(d.typ)}>{T.doors[d.typ][2]} ({items.filter((e) => e.typ === d.typ).length}) →</button>
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
      {!res && worlds.length > 0 && (
        <nav className="worlds" aria-label={lang === "en" ? "Food worlds" : "Lebensmittel-Welten"}>
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
      {!res && active.size > 0 && <button type="button" className="mol-back" onClick={closeType}>{T.mol.back}</button>}
      <h2 id="bibliothek" className={`libhead${!res && active.size > 0 ? " cat" : ""}`}>{res ? S.allHits : active.size ? T.types[[...active][0]][0] : S.whole}</h2>
      {!res && !active.size && (
        <>
          <Contents items={items} lang={lang} onOpen={openType} pics={has} />
          <div className="mol-terms">
            <button type="button" className="linkbtn" onClick={() => openType("begriff")}>{T.mol.terms} ({items.filter((e) => e.typ === "begriff").length}) →</button>
          </div>
        </>
      )}
      {(res || active.size > 0) && <>
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

      <div className={`groups${res ? "" : " solo"}`}>
        {groups.map(([t, name, subline]) => {
          const g = res ? list : list.filter((e) => e.typ === t);
          if (!g.length) return null;
          return (
            // Geschlossen beim Start; offen bei Suche oder gewähltem Typ. Der key setzt den Zustand bei Filterwechsel zurück.
            <details className={`group${!res ? " solo" : ""}`} key={`${t}-${res ? "s" : ""}-${active.has(t) ? "a" : ""}`} open={!!res || active.has(t)}>
              <summary><h3>{res && <>{name} </>}<small>{g.length} · {subline}</small></h3></summary>
              {res ? (
                <div className="grid">
                  {g.map((e) => (
                    <Link key={e.id} href={ln(`/eintrag/${e.id}`)} className={`cell${isWritten(e) ? "" : " dim"}`}>
                      <span className="t">{e.titel}</span>
                      <span className="m"><i style={{ background: `var(--t-${e.typ})` }} />{SING[e.typ]}{e.status === "geprueft" ? " · ✓" : ""}</span>
                    </Link>
                  ))}
                </div>
              ) : AS_CHIPS.has(t) ? (
                <div className="chips list-chips">
                  {g.map((e) => <Link key={e.id} href={ln(`/eintrag/${e.id}`)} className="chip"><i style={{ background: `var(--t-${e.typ})` }} />{e.titel}{e.status === "geprueft" ? " ✓" : ""}</Link>)}
                </div>
              ) : AS_TILES.has(t) ? (
                <div className="tiles2">
                  {g.map((e) => {
                    const pic = pictureOf(e, has);
                    return (
                      <Link key={e.id} href={ln(`/eintrag/${e.id}`)} className="tile2">
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        {pic ? <img src={`/illustrationen/${pic}.webp`} alt="" width={160} height={160} loading="lazy" /> : <span className="tile2-ph" style={{ background: `var(--t-${e.typ})` }} />}
                        <span>{e.titel}{e.status === "geprueft" ? " ✓" : ""}</span>
                      </Link>
                    );
                  })}
                </div>
              ) : (
                (() => {
                  const sg = subgroups(t, g), cur = sg.find(([n]) => n === sub) ?? sg[0];
                  return (
                    <div className="rowgroups">
                      {sg.length > 1 && <div className="typechips subchips" role="group">
                        {sg.map(([n, r]) => (
                          <button key={n} type="button" className="typechip" aria-pressed={cur[0] === n} onClick={() => setSub(n)}>{n}<span>{r.length}</span></button>
                        ))}
                      </div>}
                      <ul className="rows">
                        {cur[1].map((e) => (
                          <li key={e.id}><Link href={ln(`/eintrag/${e.id}`)}><strong>{e.titel}{e.status === "geprueft" ? " ✓" : ""}</strong></Link></li>
                        ))}
                      </ul>
                    </div>
                  );
                })()
              )}
            </details>
          );
        })}
        {!list.length && <p className="count">{S.none}</p>}
      </div>
      </>}
    </>
  );
}
