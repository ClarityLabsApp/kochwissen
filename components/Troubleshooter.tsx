"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { href, type Lang } from "@/lib/i18n";
import Diagnosis from "@/components/Diagnosis";

interface Ursache { titel: string; warum: string; fix: string[]; prinzip?: string; haeufigkeit?: number }
export interface TsProblem { id: string; titel: string; buckets: string[]; ursachen: Ursache[]; diagnose: Record<string, { frage?: string; antworten?: [string, string][]; ursache?: number }>; principles: Record<string, string> }
export interface TsBucket { id: string; name: string; pic: string; n: number }

const TX = {
  de: { title: "Fehlersuche", lede: "Gerade geht etwas schief? In drei Klicks zur Ursache und zur Rettung.", s1: "Was kochst du?", s2: "Was ist passiert?", most: "Meistens liegt es daran", now: "Das hilft", sure: "Nicht sicher, ob es das ist? Zwei, drei Fragen klären es:", full: "Ganzer Eintrag mit Erklärung", back: "Zurück", restart: "Neu anfangen", all: "Nicht dabei? Alle Probleme", problems: (n: number) => `${n} Probleme` },
  en: { title: "Troubleshooting", lede: "Something is going wrong right now? Three clicks to the cause and the fix.", s1: "What are you cooking?", s2: "What happened?", most: "Most often it's this", now: "What helps", sure: "Not sure that's it? Two or three questions will tell:", full: "Full entry with explanation", back: "Back", restart: "Start over", all: "Not listed? All problems", problems: (n: number) => `${n} problems` },
};

export default function Troubleshooter({ buckets, problems, lang }: { buckets: TsBucket[]; problems: TsProblem[]; lang: Lang }) {
  const X = TX[lang], ln = (p: string) => href(lang, p);
  const [b, setB] = useState<string | null>(null);
  const [p, setP] = useState<string | null>(null);
  // Zustand in der Adresse (?b=…&p=…), damit „Zurück“ im Browser funktioniert und man Links teilen kann.
  useEffect(() => {
    const read = () => { const u = new URL(window.location.href); setB(u.searchParams.get("b")); setP(u.searchParams.get("p")); };
    read(); window.addEventListener("popstate", read); return () => window.removeEventListener("popstate", read);
  }, []);
  const go = (nb: string | null, np: string | null) => {
    const u = new URL(window.location.href);
    u.search = ""; if (nb) u.searchParams.set("b", nb); if (np) u.searchParams.set("p", np);
    window.history.pushState(null, "", u); setB(nb); setP(np);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };
  const bucket = buckets.find((x) => x.id === b) ?? null;
  const prob = problems.find((x) => x.id === p) ?? null;
  const list = bucket ? problems.filter((x) => x.buckets.includes(bucket.id)) : [];
  const top = prob ? [...prob.ursachen].sort((a, c) => (c.haeufigkeit ?? 0) - (a.haeufigkeit ?? 0))[0] : null;
  const step = prob ? 3 : bucket ? 2 : 1;

  return (
    <div className="ts">
      <header className="hub-head"><h1>{X.title}</h1><p>{X.lede}</p></header>
      <ol className="ts-steps" aria-label={X.title}>
        <li className={step === 1 ? "on" : "done"}>{step > 1 ? <button type="button" onClick={() => go(null, null)}>{bucket?.name}</button> : X.s1}</li>
        <li className={step === 2 ? "on" : step > 2 ? "done" : ""}>{step > 2 ? <button type="button" onClick={() => go(b, null)}>{prob?.titel}</button> : X.s2}</li>
        <li className={step === 3 ? "on" : ""}>{X.now}</li>
      </ol>

      {step === 1 && (
        <section aria-label={X.s1}>
          <h2 className="ts-q">{X.s1}</h2>
          <div className="ts-buckets">
            {buckets.map((x) => (
              <button key={x.id} type="button" className="ts-bucket" onClick={() => go(x.id, null)}>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={`/illustrationen/${x.pic}.webp`} alt="" width={84} height={84} />
                <strong>{x.name}</strong><small className="mono">{X.problems(x.n)}</small>
              </button>
            ))}
          </div>
        </section>
      )}

      {step === 2 && bucket && (
        <section aria-label={X.s2}>
          <h2 className="ts-q">{X.s2}</h2>
          <div className="ts-probs">
            {list.map((x) => <button key={x.id} type="button" className="ts-prob" onClick={() => go(b, x.id)}>{x.titel}<span aria-hidden>→</span></button>)}
          </div>
          <div className="ts-foot">
            <button type="button" className="linkbtn" onClick={() => go(null, null)}>← {X.back}</button>
            <Link className="linkbtn" href={ln("/probleme")}>{X.all} →</Link>
          </div>
        </section>
      )}

      {step === 3 && prob && top && (
        <section aria-label={prob.titel}>
          <h2 className="ts-q">{prob.titel}</h2>
          <div className="ts-fix">
            <span className="mono">{X.most}</span>
            <p className="ts-cause">{top.titel}</p>
            <span className="mono">{X.now}</span>
            <ul>{top.fix.map((f) => <li key={f}>{f}</li>)}</ul>
            <p className="ts-why">{top.warum}</p>
          </div>
          {prob.ursachen.length > 1 && (
            <>
              <p className="ts-sure">{X.sure}</p>
              <Diagnosis key={prob.id} tree={prob.diagnose} causes={prob.ursachen} principleTitles={prob.principles} lang={lang} />
            </>
          )}
          <div className="ts-foot">
            <button type="button" className="linkbtn" onClick={() => go(b, null)}>← {X.back}</button>
            <Link className="linkbtn" href={ln(`/eintrag/${prob.id}`)}>{X.full} →</Link>
            <button type="button" className="linkbtn" onClick={() => go(null, null)}>↺ {X.restart}</button>
          </div>
        </section>
      )}
    </div>
  );
}
