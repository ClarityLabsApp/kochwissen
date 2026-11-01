import Link from "next/link";
import { notFound } from "next/navigation";
import { existsSync } from "node:fs";
import { join } from "node:path";
import type { Metadata } from "next";
import RichText from "@/components/RichText";
import Diagnosis from "@/components/Diagnosis";
import Visual, { plain } from "@/components/visuals/Visual";
import StepFlow from "@/components/visuals/StepFlow";
import { allIds, getEntry, getMasterItem, titleOf, typOf, PROTOTYPES, TYP_NAME, type Typ } from "@/lib/content";

export function generateStaticParams() {
  return allIds().map((id) => ({ id }));
}

export function generateMetadata({ params }: { params: { id: string } }): Metadata {
  return { title: titleOf(params.id) };
}

function Chips({ ids }: { ids: string[] }) {
  return (
    <div className="chips">
      {ids.map((id) => {
        const typ = typOf(id);
        const written = !!getEntry(id) || !!PROTOTYPES[id];
        return (
          <Link key={id} href={`/eintrag/${id}`} className={`chip${written ? "" : " planned"}`}>
            <i style={{ background: `var(--t-${typ})` }} />{titleOf(id)}
          </Link>
        );
      })}
    </div>
  );
}

export default function EntryPage({ params }: { params: { id: string } }) {
  const e = getEntry(params.id);
  const m = getMasterItem(params.id);
  if (!e && !m) notFound();
  const typ = (e?.typ ?? m!.typ) as Typ;
  const proto = PROTOTYPES[params.id];

  const head = (
    <>
      <div className="eyebrow">
        <span className="tag" style={{ background: `var(--t-${typ})` }}>{TYP_NAME[typ]}</span>
        {e?.schwierigkeit && <span className="mono">{e.schwierigkeit}</span>}
        <span className="mono">{e ? e.status : proto ? "Prototyp" : "geplant"}</span>
      </div>
      {existsSync(join(process.cwd(), "public/illustrationen", `${params.id}.png`)) && (
        // eslint-disable-next-line @next/next/no-img-element
        <img className="illu" src={`/illustrationen/${params.id}.png`} alt="" width={1024} height={1024} />
      )}
      <div>
        <h1>{e?.titel ?? m!.titel}</h1>
        {(e?.synonyme ?? m?.synonyme)?.length ? <p className="syn">Auch gesucht als: {(e?.synonyme ?? m!.synonyme).join(", ")}</p> : null}
      </div>
    </>
  );

  // Noch nicht ausgeschrieben: Gerüst aus der Masterliste, ggf. mit Prototyp
  if (!e) {
    const related = [...new Set([...(m!.links ?? []), ...(m!.verlinkt_von ?? [])])];
    return (
      <main className="wrap">
        <article className="entry">
          {head}
          {proto ? (
            <div className="proto">
              <span className="mono">Interaktiver Prototyp · wird noch als Vorlage portiert</span>
              <iframe src={proto} title={m!.titel} loading="lazy" />
            </div>
          ) : (
            <p className="planned-note">Dieser Eintrag ist geplant, aber noch nicht geschrieben.</p>
          )}
          {related.length > 0 && <div className="block"><span className="mono">Verwandte Einträge</span><Chips ids={related} /></div>}
        </article>
      </main>
    );
  }

  const causesSorted = [...(e.ursachen ?? [])].sort((a, b) => (b.haeufigkeit ?? 0) - (a.haeufigkeit ?? 0));
  const principleTitles = Object.fromEntries((e.ursachen ?? []).filter((u) => u.prinzip).map((u) => [u.prinzip!, titleOf(u.prinzip!)]));
  const rules = e.faustregeln?.length ? (
    <div className="block"><h2>Faustregeln</h2><ol className="rules">{e.faustregeln.map((r) => <li key={r}><RichText text={r} /></li>)}</ol></div>
  ) : null;
  const knobs = e.stellschrauben?.length ? (
    <div className="block"><h2>Stellschrauben</h2>
      <div className="knobs">{e.stellschrauben.map((s) => <div key={s.id}><Link href={`/eintrag/${s.id}`}>{titleOf(s.id)}</Link><span>{s.wirkung}</span></div>)}</div>
    </div>
  ) : null;

  return (
    <main className="wrap">
      <article className="entry">
        {head}
        <p className="kurz"><strong>Kurz gesagt:</strong> <RichText text={e.kurz} /></p>
        {proto && (
          <div className="proto">
            <span className="mono">Interaktiver Prototyp</span>
            <iframe src={proto} title={e.titel} loading="lazy" />
          </div>
        )}
        {e.bild_im_kopf && <div className="box"><span className="mono">Bild im Kopf</span><p><RichText text={e.bild_im_kopf} /></p></div>}
        {!proto && <Visual e={e} />}
        {e.bedeutung && <div className="block"><h2>Was {e.titel} bedeutet</h2><div className="prose"><p><RichText text={e.bedeutung} /></p></div></div>}
        {e.was_passiert && <div className="block"><h2>Was passiert</h2><div className="prose"><p><RichText text={e.was_passiert} /></p></div></div>}
        {e.warum_wichtig && <div className="block"><h2>Warum wichtig</h2><div className="prose"><p><RichText text={e.warum_wichtig} /></p></div></div>}
        {e.ursachen && e.diagnose && (
          <div className="block"><h2>Was ist bei dir passiert?</h2><Diagnosis tree={e.diagnose} causes={e.ursachen} principleTitles={principleTitles} /></div>
        )}
        {e.hebel?.length ? <div className="block"><h2>Die Hebel</h2><Chips ids={e.hebel} /></div> : null}
        {e.rolle?.length ? (
          <div className="block"><h2>Was die Zutat tut</h2>
            <div className="knobs">{e.rolle.map((r) => <div key={r.rolle}><span>{r.rolle}</span><Link href={`/eintrag/${r.prozess}`} className="mono">{titleOf(r.prozess)}</Link></div>)}</div>
          </div>
        ) : null}
        {e.schritte?.length ? (
          <div className="block"><h2>So geht’s</h2>
            <StepFlow steps={e.schritte.map(plain)} />
            <details className="more"><summary className="mono">Alle Schritte als Liste</summary>
              <ol className="steps">{e.schritte.map((s) => <li key={s}><RichText text={s} /></li>)}</ol>
            </details>
          </div>
        ) : null}
        {rules && knobs ? <div className="cols">{rules}{knobs}</div> : (rules ?? knobs)}
        {e.typische_fehler?.length ? <div className="block"><h2>Typische Fehler</h2><ul className="plain">{e.typische_fehler.map((f) => <li key={f}><RichText text={f} /></li>)}</ul></div> : null}
        {causesSorted.length > 0 && (
          <div className="block"><h2>Alle Ursachen, nach Häufigkeit</h2>
            <ul className="causes">{causesSorted.map((u) => (
              <li key={u.titel}>
                <div className="head"><strong>{u.titel}</strong><span className="freq">{[1, 2, 3].map((n) => <i key={n} className={n <= (u.haeufigkeit ?? 0) ? "f" : ""} />)}</span></div>
                <p className="why">{u.warum}</p>
                <p className="fix">Nächstes Mal: {u.fix.join(" · ")}</p>
              </li>
            ))}</ul>
          </div>
        )}
        {e.mythos && <div className="myth"><span className="stamp">MYTHOS</span><p>„{e.mythos.behauptung}“ <RichText text={e.mythos.richtig} /></p></div>}
        {e.praxis?.length ? (
          <div className="block"><h2>In der Praxis</h2>
            <div className="tiles">{e.praxis.map((p) => (
              <div className="tile" key={p.welt}>
                <h3>{titleOf(p.welt)}{p.aroma && <span className="dots">{p.aroma.map((a) => <i key={a} style={{ background: `var(--a-${a})` }} />)}</span>}</h3>
                <p><RichText text={p.text} /></p>
              </div>
            ))}</div>
          </div>
        ) : null}
        {e.links?.length ? <div className="block"><span className="mono">Verwandte Einträge</span><Chips ids={e.links} /></div> : null}
        {e.quellen?.length ? (
          <div className="block"><span className="mono">Quellen</span>
            <ul className="sources">{e.quellen.map((q) => <li key={q.titel}>{q.url ? <a href={q.url} target="_blank" rel="noopener noreferrer">{q.titel}</a> : q.titel}{q.stelle ? `, ${q.stelle}` : ""}</li>)}</ul>
          </div>
        ) : null}
        <div className="meta"><span>id · {e.id}</span><span>Grafik-Vorlage · {e.visual?.vorlage ?? "–"}</span></div>
      </article>
    </main>
  );
}
