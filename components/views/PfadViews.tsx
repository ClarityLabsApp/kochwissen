import Link from "next/link";
import { notFound } from "next/navigation";
import PathSteps from "@/components/PathSteps";
import Quiz from "@/components/Quiz";
import { getEntry, getPfad, lernpfade, plainText, titleOf, typOf } from "@/lib/content";
import { href, t, type Lang } from "@/lib/i18n";
import { pfadPics } from "./HomeView";

export function PfadeView({ lang }: { lang: Lang }) {
  const P = t(lang).path;
  return (
    <main className="wrap wide" lang={lang}>
      <header style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <span className="mono">{P.eyebrow}</span>
        <h1>{P.h1a}<em>{P.h1b}</em></h1>
        <p className="lede">{P.lede}</p>
      </header>
      <div className="pfad-cards">
        {lernpfade(lang).map((p) => (
          <Link key={p.id} href={href(lang, `/pfad/${p.id}`)} className="pfad-card">
            <span className="pfad-pics">{pfadPics(p.schritte.map((x) => x.id)).map((x) => (
              // eslint-disable-next-line @next/next/no-img-element
              <img key={x} src={`/illustrationen/${x}.webp`} alt="" width={52} height={52} loading="lazy" />
            ))}</span>
            <span className="mono">{t(lang).steps(p.schritte.length)} · {p.dauer}</span>
            <strong>{p.titel}</strong>
            <span className="k">{p.kurz}</span>
            <span className="f">{p.fuer}</span>
          </Link>
        ))}
      </div>
    </main>
  );
}

export function PfadView({ id, lang }: { id: string; lang: Lang }) {
  const p = getPfad(id, lang);
  if (!p) notFound();
  const P = t(lang).path;
  const steps = p.schritte.map((s) => ({ id: s.id, titel: titleOf(s.id, lang), typ: typOf(s.id) ?? "begriff", kurz: plainText(getEntry(s.id, lang)?.kurz ?? "", lang), warum: s.warum }));
  return (
    <main className="wrap" lang={lang}>
      <article className="entry">
        <div className="eyebrow"><Link href={href(lang, "/pfad")} className="tag" style={{ background: "var(--crust)", textDecoration: "none" }}>{t(lang).entry.tagPath}</Link><span className="mono">{t(lang).steps(p.schritte.length)} · {p.dauer}</span></div>
        <h1>{p.titel}</h1>
        <p className="kurz">{p.kurz}</p>
        <p className="syn">{p.fuer}</p>
        <PathSteps pfad={p.id} steps={steps} lang={lang} />
        {p.quiz?.length ? (
          <section className="block" id="quiz">
            <h2>{P.test}</h2>
            <Quiz pfad={p.id} fragen={p.quiz.map((q) => ({ ...q, eintragTitel: titleOf(q.eintrag, lang) }))} lang={lang} />
          </section>
        ) : null}
      </article>
    </main>
  );
}
