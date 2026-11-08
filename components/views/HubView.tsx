import Link from "next/link";
import type { Metadata } from "next";
import { hasPicture, libraryData, plainText, titleOf } from "@/lib/content";
import { href, t, type Lang } from "@/lib/i18n";
import { GROUPS, THEMES, THEME_PIC, type GroupKey } from "@/lib/nav";

type Item = ReturnType<typeof libraryData>[number];

const short = (s: string | null, lang: Lang, n = 110) => {
  if (!s) return "";
  const p = plainText(s, lang);
  return p.length <= n ? p : p.slice(0, p.lastIndexOf(" ", n)) + " …";
};
const written = (lang: Lang) => libraryData(lang).filter((e) => e.status !== "geplant");
const byTitle = (lang: Lang) => (a: Item, b: Item) => a.titel.localeCompare(b.titel, lang);

/** Brotkrumen: Garum › … */
export function Crumbs({ lang, trail }: { lang: Lang; trail: [string, string?][] }) {
  return (
    <nav className="crumbs" aria-label={lang === "en" ? "You are here" : "Du bist hier"}>
      <Link href={href(lang, "/")}>Garum</Link>
      {trail.map(([label, p]) => (
        <span key={label} style={{ display: "contents" }}>
          <span className="sep">›</span>
          {p ? <Link href={href(lang, p)}>{label}</Link> : <span>{label}</span>}
        </span>
      ))}
    </nav>
  );
}

/** Eine Zeile: Bild oder Farbpunkt, Titel, kurzer Satz. */
export function Row({ e, lang, tag }: { e: Item; lang: Lang; tag?: boolean }) {
  const T = t(lang);
  return (
    <li>
      <Link href={href(lang, `/eintrag/${e.id}`)}>
        {hasPicture(e.id)
          // eslint-disable-next-line @next/next/no-img-element
          ? <img src={`/illustrationen/${e.id}.webp`} alt="" width={40} height={40} loading="lazy" />
          : <span className="dot"><i style={{ background: `var(--t-${e.typ})` }} /></span>}
        <span>
          <strong>{e.titel}{tag && <span className="tg">{T.types[e.typ]?.[2]}</span>}</strong>
          {e.kurz && <span className="k">{short(e.kurz, lang)}</span>}
        </span>
      </Link>
    </li>
  );
}

function Tiles({ items, lang }: { items: Item[]; lang: Lang }) {
  return (
    <div className="hub-tiles">
      {items.map((e) => {
        const pic = hasPicture(e.id) ? e.id : (e.welten ?? []).find(hasPicture);
        return (
          <Link key={e.id} href={href(lang, `/eintrag/${e.id}`)} className="hub-tile">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            {pic ? <img src={`/illustrationen/${pic}.webp`} alt="" width={96} height={96} loading="lazy" /> : null}
            <span>{e.titel}</span>
          </Link>
        );
      })}
    </div>
  );
}

/** Einträge nach ihrer ersten Welt gruppieren: [Welt-id, Einträge], größte Gruppen zuerst, Rest am Ende. */
function byWorld(items: Item[]): [string, Item[]][] {
  const m = new Map<string, Item[]>();
  for (const e of items) { const w = e.welten?.[0] ?? ""; m.set(w, [...(m.get(w) ?? []), e]); }
  return [...m.entries()].sort((a, b) => (a[0] ? 0 : 1) - (b[0] ? 0 : 1) || b[1].length - a[1].length);
}

type Section = { id: string; title: string; pic?: string; n: number; body: React.ReactNode };

function Sections({ sections, lang }: { sections: Section[]; lang: Lang }) {
  const H = t(lang).hub;
  return (
    <>
      {sections.length > 1 && (
        <nav className="jump" aria-label={H.jump}>
          {sections.map((s) => (
            <a key={s.id} href={`#${s.id}`}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              {s.pic && <img src={`/illustrationen/${s.pic}.webp`} alt="" width={22} height={22} />}
              {s.title} <small>{s.n}</small>
            </a>
          ))}
        </nav>
      )}
      {sections.map((s) => (
        <section key={s.id} id={s.id} className="hub-sec">
          <h2>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            {s.pic && <img src={`/illustrationen/${s.pic}.webp`} alt="" width={42} height={42} />}
            {s.title}<small>{s.n}</small>
          </h2>
          {s.body}
        </section>
      ))}
    </>
  );
}

/** Die anderen Fragen und A–Z als Karten am Ende jeder Übersicht. */
export function MoreGroups({ lang, except }: { lang: Lang; except?: GroupKey }) {
  const H = t(lang).hub;
  const all = written(lang);
  return (
    <section className="hub-more" aria-label={H.explore}>
      <span className="mono">{H.explore}</span>
      <div className="hub-groups">
        {GROUPS.filter((g) => g.key !== except).map((g) => (
          <Link key={g.key} href={href(lang, `/${g.key}`)} className="hub-group" style={{ ["--c" as string]: `var(--t-${g.color})` }}>
            <strong>{H[g.key][0]}</strong><span>{H[g.key][1]}</span>
            <small>{all.filter((e) => g.types.includes(e.typ)).length} →</small>
          </Link>
        ))}
        <Link href={href(lang, "/alle")} className="hub-group" style={{ ["--c" as string]: "var(--t-welt)" }}>
          <strong>{H.azTitle}</strong><span>{H.az}</span><small>{all.length} →</small>
        </Link>
      </div>
    </section>
  );
}

export function groupMetadata(key: GroupKey, lang: Lang): Metadata {
  const H = t(lang).hub;
  return {
    title: H[key][0], description: H[key][1],
    alternates: { canonical: href(lang, `/${key}`), languages: { de: `/${key}`, en: `/en/${key}`, "x-default": `/${key}` } },
  };
}

export default function HubView({ group, lang }: { group: GroupKey; lang: Lang }) {
  const T = t(lang), H = T.hub;
  const g = GROUPS.find((x) => x.key === group)!;
  const items = written(lang).filter((e) => g.types.includes(e.typ)).sort(byTitle(lang));
  const list = (xs: Item[], tag = false) => <ul className="hub-list">{xs.map((e) => <Row key={e.id} e={e} lang={lang} tag={tag} />)}</ul>;
  const worldSections = (xs: Item[], tiles = false): Section[] => byWorld(xs).map(([w, r]) => ({
    id: w || "weitere", title: w ? titleOf(w, lang) : H.other, pic: w && hasPicture(w) ? w : undefined, n: r.length,
    body: tiles ? <Tiles items={r} lang={lang} /> : list(r),
  }));

  let sections: Section[] = [];
  if (group === "probleme") sections = worldSections(items);
  if (group === "ziele") sections = [{ id: "ziele", title: H.ziele[0], n: items.length, body: list(items) }];
  if (group === "ausprobieren") {
    sections = (["gericht", "experiment", "labor"] as const).map((typ) => {
      const r = items.filter((e) => e.typ === typ);
      return { id: typ, title: T.types[typ][0], pic: hasPicture(`cat-${typ}`) ? `cat-${typ}` : undefined, n: r.length, body: <><p className="hub-sub">{T.types[typ][1]}</p><Tiles items={r} lang={lang} /></> };
    });
  }
  if (group === "verstehen") {
    const proz = items.filter((e) => e.typ === "prozess");
    const seen = new Set(THEMES.flatMap((x) => x[3]));
    const themeBlocks = [...THEMES.map(([k, de, en, ids]) => [k, lang === "en" ? en : de, ids.map((id) => proz.find((e) => e.id === id)).filter(Boolean) as Item[]] as const),
      ["weitere", H.other, proz.filter((e) => !seen.has(e.id))] as const].filter(([, , r]) => r.length);
    const tech = items.filter((e) => e.typ === "technik");
    sections = [
      { id: "vorgaenge", title: H.vorgaenge, pic: "cat-prozess", n: proz.length,
        body: themeBlocks.map(([k, name, r]) => <div key={k}><h3>{name}</h3>{list(r)}</div>) },
      { id: "techniken", title: T.types.technik[0], pic: hasPicture("cat-technik") ? "cat-technik" : undefined, n: tech.length,
        body: byWorld(tech).map(([w, r]) => <div key={w || "x"}><h3>{w ? titleOf(w, lang) : H.other}</h3>{list(r)}</div>) },
      { id: "zutaten", title: T.types.zutat[0], pic: hasPicture("cat-zutat") ? "cat-zutat" : undefined, n: items.filter((e) => e.typ === "zutat").length,
        body: <Tiles items={items.filter((e) => e.typ === "zutat")} lang={lang} /> },
      { id: "stellschrauben", title: T.types.stellschraube[0], pic: hasPicture("cat-stellschraube") ? "cat-stellschraube" : undefined, n: items.filter((e) => e.typ === "stellschraube").length,
        body: list(items.filter((e) => e.typ === "stellschraube")) },
      { id: "begriffe", title: T.types.begriff[0], pic: hasPicture("cat-begriff") ? "cat-begriff" : undefined, n: items.filter((e) => e.typ === "begriff").length,
        body: <div className="hub-chips">{items.filter((e) => e.typ === "begriff").map((e) => <Link key={e.id} href={href(lang, `/eintrag/${e.id}`)} className="chip"><i style={{ background: "var(--t-begriff)" }} />{e.titel}</Link>)}</div> },
    ];
  }

  return (
    <main className="wrap" id="inhalt" lang={lang}>
      <Crumbs lang={lang} trail={[[H[group][0]]]} />
      <header className="hub-head">
        <span className="mono" style={{ color: `var(--t-${g.color})` }}>{items.length} {lang === "en" ? "entries" : "Einträge"}</span>
        <h1>{H[group][0]}</h1>
        <p>{H[group][1]}</p>
      </header>
      <Sections sections={sections} lang={lang} />
      <MoreGroups lang={lang} except={group} />
    </main>
  );
}

/** Alle Einträge von A bis Z, mit Buchstaben-Sprungleiste. */
export function AzView({ lang }: { lang: Lang }) {
  const H = t(lang).hub;
  const items = written(lang).sort(byTitle(lang));
  const letter = (s: string) => {
    const c = s.normalize("NFD").replace(/[̀-ͯ]/g, "")[0]?.toUpperCase() ?? "#";
    return /[A-Z]/.test(c) ? c : "#";
  };
  const groups = new Map<string, Item[]>();
  for (const e of items) groups.set(letter(e.titel), [...(groups.get(letter(e.titel)) ?? []), e]);
  return (
    <main className="wrap" id="inhalt" lang={lang}>
      <Crumbs lang={lang} trail={[[H.azTitle]]} />
      <header className="hub-head"><h1>{H.azTitle}</h1><p>{H.azLede(items.length)}</p></header>
      <nav className="jump az-letters" aria-label={H.jump}>{[...groups.keys()].map((l) => <a key={l} href={`#az-${l}`}>{l}</a>)}</nav>
      {[...groups.entries()].map(([l, r]) => (
        <section key={l} id={`az-${l}`} className="hub-sec">
          <h2>{l}<small>{r.length}</small></h2>
          <ul className="hub-list">{r.map((e) => <Row key={e.id} e={e} lang={lang} tag />)}</ul>
        </section>
      ))}
      <MoreGroups lang={lang} />
    </main>
  );
}
