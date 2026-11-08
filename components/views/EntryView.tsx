import Link from "next/link";
import { notFound } from "next/navigation";
import { existsSync } from "node:fs";
import { join } from "node:path";
import type { Metadata } from "next";
import RichText from "@/components/RichText";
import Diagnosis from "@/components/Diagnosis";
import Visual, { plain } from "@/components/visuals/Visual";
import StepFlow from "@/components/visuals/StepFlow";
import PathNav from "@/components/PathNav";
import PrintButton from "@/components/PrintButton";
import MerkButton from "@/components/MerkButton";
import { appearsIn, getEntry, getMasterItem, hasPicture, isTranslated, lernpfade, libraryData, plainText, titleOf, typOf, type Typ } from "@/lib/content";
import { GROUPS, groupOfType } from "@/lib/nav";
import { Crumbs, Row } from "./HubView";
import { href, t, type Lang } from "@/lib/i18n";
import { CONTACT_EMAIL, OWNER, SITE_URL } from "@/lib/site";

/** Seitentitel, Beschreibung und Vorschaubild eines Eintrags. */
/** Suchfreundlicher Zusatz zum Seitentitel je nach Typ (nur <title>, nicht die Überschrift). */
const TITLE_SUFFIX: Record<Lang, Partial<Record<Typ, string>>> = {
  de: { symptom: "Ursachen und Lösung", prozess: "einfach erklärt", begriff: "Bedeutung in der Küche", technik: "so funktioniert es", ziel: "so gelingt es", gericht: "warum das Rezept funktioniert", experiment: "Küchenexperiment", labor: "selber machen", zutat: "was sie beim Kochen tut", stellschraube: "wie sie das Ergebnis verändert", welt: "Kochwissen" },
  en: { symptom: "causes and fixes", prozess: "explained simply", begriff: "meaning in cooking", technik: "how it works", ziel: "how to get it right", gericht: "why the recipe works", experiment: "kitchen experiment", labor: "make it yourself", zutat: "what it does in cooking", stellschraube: "how it changes the result", welt: "cooking science" },
};

/** Strukturierte Daten (schema.org) für Google: Artikel und Brotkrumen. */
function entryJsonLd(id: string, lang: Lang) {
  const e = getEntry(id, lang);
  if (!e) return null;
  const typ = e.typ as Typ;
  const url = SITE_URL + href(lang, `/eintrag/${id}`);
  const home = SITE_URL + href(lang, "/");
  const cat = t(lang).types[typ]?.[0] ?? typ;
  const pic = hasPicture(id) ? SITE_URL + `/illustrationen/${id}.webp` : undefined;
  const brand = { "@type": "Organization", name: "Garum", url: SITE_URL, logo: SITE_URL + "/icon-512.png" };
  return [
    {
      "@context": "https://schema.org", "@type": typ === "begriff" ? "DefinedTerm" : "Article",
      ...(typ === "begriff"
        ? { name: e.titel, description: plainText(e.kurz, lang), url, inDefinedTermSet: home }
        : { headline: e.titel, description: plainText(e.kurz, lang), url, mainEntityOfPage: url, inLanguage: lang === "en" ? "en-GB" : "de-CH", image: pic, author: { "@type": "Person", name: OWNER.name }, publisher: brand, dateModified: BUILD_DATE, citation: (e.quellen ?? []).map((q: { titel: string; url?: string }) => q.url ?? q.titel) }),
    },
    {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Garum", item: home },
        { "@type": "ListItem", position: 2, name: groupOfType(typ) ? t(lang).hub[groupOfType(typ)!][0] : cat, item: SITE_URL + href(lang, groupOfType(typ) ? `/${groupOfType(typ)}` : "/") },
        { "@type": "ListItem", position: 3, name: e.titel, item: url },
      ],
    },
  ];
}
const BUILD_DATE = new Date().toISOString().slice(0, 10);

export function entryMetadata(id: string, lang: Lang): Metadata {
  const e = getEntry(id, lang);
  const title = titleOf(id, lang);
  const suffix = e ? TITLE_SUFFIX[isTranslated(id) ? lang : "de"][e.typ as Typ] : undefined;
  const description = e?.kurz ? plainText(e.kurz, lang) : lang === "en" ? `${title}: understand why it works in the kitchen.` : `${title}: verstehen, warum es in der Küche funktioniert.`;
  const img = existsSync(join(process.cwd(), "public/illustrationen", `${id}.webp`)) ? [{ url: `/illustrationen/${id}.webp`, width: 800, height: 800 }] : [{ url: `/og-${lang}.png`, width: 1200, height: 630 }];
  const tr = isTranslated(id);
  return {
    title: suffix ? `${title}: ${suffix}` : title, description,
    // Nicht übersetzte englische Seiten zeigen den deutschen Text: nicht indexieren, Original als kanonisch.
    ...(lang === "en" && !tr ? { robots: { index: false, follow: true } } : {}),
    alternates: { canonical: lang === "en" && !tr ? `/eintrag/${id}` : href(lang, `/eintrag/${id}`), languages: tr ? { de: `/eintrag/${id}`, en: `/en/eintrag/${id}` } : { de: `/eintrag/${id}` } },
    openGraph: { title, description, type: "article", url: href(lang, `/eintrag/${id}`), images: img, locale: lang === "en" ? "en_GB" : "de_CH" },
  };
}

function Chips({ ids, lang, max = 6 }: { ids: string[]; lang: Lang; max?: number }) {
  const chip = (id: string) => (
    <Link key={id} href={href(lang, `/eintrag/${id}`)} className={`chip${getEntry(id) ? "" : " planned"}`}>
      {hasPicture(id)
        // eslint-disable-next-line @next/next/no-img-element
        ? <img className="chip-img" src={`/illustrationen/${id}.webp`} alt="" width={22} height={22} loading="lazy" />
        : <i style={{ background: `var(--t-${typOf(id)})` }} />}{titleOf(id, lang)}
    </Link>
  );
  const rest = ids.slice(max);
  return (
    <div className="chips">
      {ids.slice(0, max).map(chip)}
      {rest.length > 0 && (
        <details className="chips-more"><summary className="chip">+ {rest.length}</summary><div className="chips">{rest.map(chip)}</div></details>
      )}
    </div>
  );
}

export default function EntryView({ id, lang }: { id: string; lang: Lang }) {
  const T = t(lang), L = T.entry;
  const e = getEntry(id, lang);
  const m = getMasterItem(id);
  if (!e && !m) notFound();
  const typ = (e?.typ ?? m!.typ) as Typ;
  const R = ({ text }: { text: string }) => <RichText text={text} lang={lang} />;
  const ln = (p: string) => href(lang, p);

  const hasIllu = existsSync(join(process.cwd(), "public/illustrationen", `${id}.webp`));
  const H = T.hub, grp = groupOfType(typ);
  const w0 = typ === "welt" ? undefined : (e?.welten ?? m?.welten ?? [])[0];
  const crumbs = <Crumbs lang={lang} trail={typ === "welt" ? [[H.welten, "/#welten"]] : [...(grp ? [[H[grp][0], `/${grp}`] as [string, string]] : []), ...(w0 ? [[titleOf(w0, lang), `/eintrag/${w0}`] as [string, string]] : [])]} />;
  const head = (
    <div className={`ehead${hasIllu ? " with-illu" : ""}`}>
      <div className="ehead-text">
        <div className="eyebrow">
          {groupOfType(typ)
            ? <Link className="tag" href={ln(`/${groupOfType(typ)}`)} style={{ background: `var(--t-${typ})` }}>{T.types[typ]?.[2] ?? typ}</Link>
            : <span className="tag" style={{ background: `var(--t-${typ})` }}>{T.types[typ]?.[2] ?? typ}</span>}
          {e?.schwierigkeit && <span className="mono">{T.level[e.schwierigkeit] ?? e.schwierigkeit}</span>}
          <span className="mono">{T.status[e ? e.status : "geplant"] ?? e?.status}</span>
          {e && <MerkButton id={id} lang={lang} />}
        </div>
        <h1>{e?.titel ?? titleOf(id, lang)}</h1>
        {(e?.synonyme ?? m?.synonyme)?.length ? <p className="syn">{L.syn}: {(e?.synonyme ?? m!.synonyme).join(", ")}</p> : null}
      </div>
      {hasIllu && (
        // eslint-disable-next-line @next/next/no-img-element
        <img className="illu" src={`/illustrationen/${id}.webp`} alt="" width={1024} height={1024} />
      )}
    </div>
  );

  if (!e) {
    const related = [...new Set([...(m!.links ?? []), ...(m!.verlinkt_von ?? [])])];
    return (
      <main className="wrap" lang={lang}>
        <article className="entry">
          {crumbs}
          {head}
          <p className="planned-note">{L.planned}</p>
          {related.length > 0 && <div className="block"><span className="mono">{L.related}</span><Chips ids={related} lang={lang} /></div>}
        </article>
      </main>
    );
  }

  const paths = lernpfade(lang).filter((p) => p.schritte.some((s) => s.id === id)).map((p) => ({ id: p.id, titel: p.titel, schritte: p.schritte.map((s) => ({ id: s.id, titel: titleOf(s.id, lang) })) }));
  const causesSorted = [...(e.ursachen ?? [])].sort((a, b) => (b.haeufigkeit ?? 0) - (a.haeufigkeit ?? 0));
  const principleTitles = Object.fromEntries((e.ursachen ?? []).filter((u) => u.prinzip).map((u) => [u.prinzip!, titleOf(u.prinzip!, lang)]));
  const rules = e.faustregeln?.length ? (
    <div className="block"><h2>{L.rules}</h2><ol className="rules">{e.faustregeln.map((r) => <li key={r}><R text={r} /></li>)}</ol></div>
  ) : null;
  const knobs = e.stellschrauben?.length ? (
    <details className="sec"><summary><h2>{L.knobs}</h2><small>{e.stellschrauben.length}</small></summary>
      <div className="knobs">{e.stellschrauben.map((s) => <div key={s.id}><Link href={ln(`/eintrag/${s.id}`)}>{titleOf(s.id, lang)}</Link><span>{s.wirkung}</span></div>)}</div>
    </details>
  ) : null;
  const untranslated = lang === "en" && !isTranslated(id);
  // Einträge ohne eigenes Bild zeigen, bei welchen Gerichten, Zutaten und Rezepten man ihnen begegnet.
  const seen = hasIllu || ["gericht", "labor", "experiment", "zutat", "welt"].includes(typ) ? [] : appearsIn(id);
  const seenStrip = seen.length >= 2 ? (
    <div className="block"><span className="mono">{L.seenIn}</span>
      <div className="seen">{seen.map((x) => (
        <Link key={x} href={ln(`/eintrag/${x}`)} className="seen-item">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={`/illustrationen/${x}.webp`} alt="" width={96} height={96} loading="lazy" />
          <span>{titleOf(x, lang)}</span>
        </Link>
      ))}</div>
    </div>
  ) : null;

  return (
    <main className="wrap" lang={untranslated ? "de" : lang}>
      {!untranslated && <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(entryJsonLd(id, lang)).replace(/</g, "\\u003c") }} />}
      <article className="entry">
        {crumbs}
        {head}
        {untranslated && <p className="untranslated" lang="en">{L.notTranslated}</p>}
        <PathNav entry={e.id} paths={paths} lang={lang} />
        <p className="kurz"><strong>{L.short}</strong> <R text={e.kurz} /></p>
        {typ === "welt" && <WorldHub id={id} titel={e.titel} lang={lang} />}
        {e.bild_im_kopf && <div className="box"><span className="mono">{L.picture}</span><p><R text={e.bild_im_kopf} /></p></div>}
        <Visual e={e} lang={lang} />
        {e.bedeutung && <div className="block"><h2>{L.means(e.titel)}</h2><div className="prose"><p><R text={e.bedeutung} /></p></div></div>}
        {e.was_passiert && <div className="block"><h2>{L.happens}</h2><div className="prose"><p><R text={e.was_passiert} /></p></div></div>}
        {e.warum_wichtig && <div className="block"><h2>{L.why}</h2><div className="prose"><p><R text={e.warum_wichtig} /></p></div></div>}
        {seenStrip}
        {(e.typ === "experiment" || e.typ === "labor") && e.material?.length ? (
          <div className="exp"><div className="exp-head"><span className="mono">{L.need}{e.dauer ? ` · ${e.dauer}` : ""}</span><PrintButton label={L.print} /></div>
            <ul className="plain">{e.material.map((x) => <li key={x}>{x}</li>)}</ul>
            {e.sicherheit && <p className="safety">{e.sicherheit}</p>}
          </div>
        ) : null}
        {e.schluesselmomente?.length ? (
          <div className="block"><h2>{e.typ === "labor" ? L.labSteps : L.moments}</h2>
            <ol className="moments">{e.schluesselmomente.map((x, i) => (
              <li key={x.schritt}><span className="n">{i + 1}</span><div>
                <strong>{x.schritt}</strong><p><R text={x.warum} /></p>
                {x.prinzip && <Link className="chip" href={ln(`/eintrag/${x.prinzip}`)}><i style={{ background: `var(--t-${typOf(x.prinzip)})` }} />{titleOf(x.prinzip, lang)}</Link>}
              </div></li>
            ))}</ol>
          </div>
        ) : null}
        {e.ursachen && e.diagnose && (
          <div className="block"><h2>{L.diag}</h2><Diagnosis tree={e.diagnose} causes={e.ursachen} principleTitles={principleTitles} lang={lang} /></div>
        )}
        {e.hebel?.length ? <div className="block"><h2>{L.levers}</h2><Chips ids={e.hebel} lang={lang} /></div> : null}
        {e.rolle?.length ? (
          <div className="block"><h2>{L.role}</h2>
            <div className="knobs">{e.rolle.map((r) => <div key={r.rolle}><span>{r.rolle}</span><Link href={ln(`/eintrag/${r.prozess}`)} className="mono">{titleOf(r.prozess, lang)}</Link></div>)}</div>
          </div>
        ) : null}
        {e.schritte?.length ? (
          <div className="block"><h2>{L.how}</h2>
            <StepFlow steps={e.schritte.map(plain)} lang={lang} />
            <details className="more"><summary className="mono">{L.allSteps}</summary>
              <ol className="steps">{e.schritte.map((s) => <li key={s}><R text={s} /></li>)}</ol>
            </details>
          </div>
        ) : null}
        {rules}{knobs}
        {e.typische_fehler?.length ? <details className="sec"><summary><h2>{L.mistakes}</h2><small>{e.typische_fehler.length}</small></summary><ul className="plain">{e.typische_fehler.map((f) => <li key={f}><R text={f} /></li>)}</ul></details> : null}
        {causesSorted.length > 0 && (
          <details className="sec"><summary><h2>{L.causes}</h2><small>{causesSorted.length}</small></summary>
            <ul className="causes">{causesSorted.map((u) => (
              <li key={u.titel}>
                <div className="head"><strong>{u.titel}</strong><span className="freq">{[1, 2, 3].map((n) => <i key={n} className={n <= (u.haeufigkeit ?? 0) ? "f" : ""} />)}</span></div>
                <p className="why"><R text={u.warum} /></p>
                <p className="fix">{L.nextTime}: {u.fix.join(" · ")}</p>
              </li>
            ))}</ul>
          </details>
        )}
        {e.beobachtung && <div className="block"><h2>{L.see}</h2><div className="prose"><p><R text={e.beobachtung} /></p></div></div>}
        {e.erklaerung && <div className="box"><span className="mono">{L.whyHappens}</span><p><R text={e.erklaerung} /></p></div>}
        {e.ergebnis || e.haltbarkeit ? (
          <div className="cols lab-result">
            {e.ergebnis && <div className="block"><h2>{L.result}</h2><div className="prose"><p><R text={e.ergebnis} /></p></div></div>}
            {e.haltbarkeit && <div className="block"><h2>{L.keeps}</h2><div className="prose"><p><R text={e.haltbarkeit} /></p></div></div>}
          </div>
        ) : null}
        {e.verwendung?.length ? <div className="block"><h2>{L.use}</h2><ul className="plain">{e.verwendung.map((v) => <li key={v}><R text={v} /></li>)}</ul></div> : null}
        {e.mythos && <div className="myth"><span className="stamp">{L.myth}</span><p>{lang === "en" ? "“" : "„"}{e.mythos.behauptung}{lang === "en" ? "”" : "“"} <R text={e.mythos.richtig} /></p></div>}
        {e.praxis?.length ? (
          <details className="sec"><summary><h2>{L.practice}</h2><small>{e.praxis.length}</small></summary>
            <div className="tiles">{e.praxis.map((p) => (
              <div className="tile" key={p.welt}>
                <h3>{titleOf(p.welt, lang)}{p.aroma && <span className="dots">{p.aroma.map((a) => <i key={a} style={{ background: `var(--a-${a})` }} />)}</span>}</h3>
                <p><R text={p.text} /></p>
              </div>
            ))}</div>
          </details>
        ) : null}
        {(() => {
          // Was schon im Text verlinkt ist, steht nicht noch einmal als Chip darunter.
          const inText = new Set([...JSON.stringify(e).matchAll(/\[\[([a-z0-9-]+)/g)].map((m) => m[1]));
          const rest = (e.links ?? []).filter((id) => !inText.has(id) && !seen.includes(id));
          return rest.length ? <div className="block"><span className="mono">{L.related}</span><Chips ids={rest} lang={lang} /></div> : null;
        })()}
        {typ !== "welt" && <NextBlock id={id} lang={lang} />}
        {(() => {
          // Rückmeldung zum Eintrag: öffnet eine E-Mail mit Titel und Link im Betreff
          const url = `${SITE_URL}${href(lang, `/eintrag/${e.id}`)}`;
          const mail = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(`Garum: ${e.titel}`)}&body=${encodeURIComponent(`${url}\n\n`)}`;
          return <p className="feedback"><span>{L.feedbackQ}</span> <a href={mail}>{L.feedbackA}</a></p>;
        })()}
        {e.quellen?.length ? (
          <details className="sec small"><summary><span className="mono">{L.sources} · {e.quellen.length}</span></summary>
            <ul className="sources">{e.quellen.map((q) => <li key={q.titel}>{q.url ? <a href={q.url} target="_blank" rel="noopener noreferrer">{q.titel}</a> : q.titel}{q.stelle ? `, ${q.stelle}` : ""}</li>)}</ul>
          </details>
        ) : null}
        <PathNav entry={e.id} paths={paths} lang={lang} />
      </article>
    </main>
  );
}


type LibEntry = ReturnType<typeof libraryData>[number];
const writtenItems = (lang: Lang) => libraryData(lang).filter((x) => x.status !== "geplant");

/** Welt-Seite: alles zu diesem Lebensmittel, nach den vier Fragen geordnet. */
function WorldHub({ id, titel, lang }: { id: string; titel: string; lang: Lang }) {
  const H = t(lang).hub;
  const inWorld = writtenItems(lang).filter((x) => x.welten?.includes(id) && x.id !== id);
  const cols = GROUPS.map((g) => [g, inWorld.filter((x) => g.types.includes(x.typ)).sort((a, b) => a.titel.localeCompare(b.titel, lang))] as const).filter(([, r]) => r.length);
  if (!inWorld.length) return null;
  const MAX = 6;
  return (
    <section className="world-hub" aria-label={H.inWorld(titel)}>
      <h2>{H.inWorld(titel)}</h2>
      <p>{H.inWorldLede(inWorld.length)}</p>
      <div className="world-cols">
        {cols.map(([g, r]) => (
          <div key={g.key} className="world-col">
            <h3 className="mono"><i style={{ background: `var(--t-${g.color})` }} />{H[g.key][0]} · {r.length}</h3>
            <ul className="hub-list">{r.slice(0, MAX).map((x) => <Row key={x.id} e={x} lang={lang} />)}</ul>
            {r.length > MAX && (
              <details><summary>{H.showAll(r.length)} ↓</summary><ul className="hub-list">{r.slice(MAX).map((x) => <Row key={x.id} e={x} lang={lang} />)}</ul></details>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

/** „Wie weiter?“: drei Karten am Ende eines Eintrags, damit man nicht in einer Sackgasse landet. */
function NextBlock({ id, lang }: { id: string; lang: Lang }) {
  const H = t(lang).hub, T = t(lang);
  const all = writtenItems(lang);
  const byId = new Map(all.map((x) => [x.id, x]));
  const e = getEntry(id, lang);
  if (!e) return null;
  const links = [...(e.ursachen ?? []).map((u) => u.prinzip).filter(Boolean) as string[], ...(e.schluesselmomente ?? []).map((x) => x.prinzip).filter(Boolean) as string[], ...(e.links ?? [])]
    .filter((x) => x !== id && byId.has(x));
  const used = new Set<string>([id]);
  const pick = (cands: string[]) => { const x = cands.find((c) => !used.has(c)); if (x) used.add(x); return x; };
  const why = e.typ === "prozess"
    ? pick(links.filter((x) => ["technik", "ziel", "symptom"].includes(byId.get(x)!.typ)))
    : pick(links.filter((x) => byId.get(x)!.typ === "prozess"));
  const w0 = e.welten?.[0];
  const hash = [...id].reduce((a, c) => a + c.charCodeAt(0), 0);
  const sameWorld = w0 ? all.filter((x) => x.welten?.includes(w0) && x.typ !== "welt" && x.id !== id && x.typ !== "begriff") : [];
  const rotated = [...sameWorld.filter((x) => hasPicture(x.id)), ...sameWorld.filter((x) => !hasPicture(x.id))];
  const off = rotated.length ? hash % rotated.length : 0;
  const world = pick([...rotated.slice(off), ...rotated.slice(0, off)].map((x) => x.id));
  const rel = pick([...links.filter((x) => hasPicture(x)), ...links]);
  const cards = [[why, H.nextWhy], [world, w0 ? H.nextWorld(titleOf(w0, lang)) : H.nextRelated], [rel, H.nextRelated]].filter(([x]) => x) as [string, string][];
  if (!cards.length) return null;
  return (
    <section className="next-block" aria-label={H.next}>
      <h2>{H.next}</h2>
      <div className="next-cards">
        {cards.map(([x, label]) => {
          const it = byId.get(x)!;
          const pic = hasPicture(x) ? x : (it.welten ?? []).find(hasPicture);
          return (
            <Link key={x} href={href(lang, `/eintrag/${x}`)} className="next-card" style={{ ["--c" as string]: `var(--t-${it.typ})` }}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              {pic ? <img src={`/illustrationen/${pic}.webp`} alt="" width={64} height={64} loading="lazy" /> : <span className="ph" style={{ background: `var(--t-${it.typ})` }} />}
              <span><span className="mono">{label} · {T.types[it.typ]?.[2]}</span><strong>{it.titel}</strong></span>
            </Link>
          );
        })}
      </div>
    </section>
  );
}
