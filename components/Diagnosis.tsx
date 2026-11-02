"use client";
import Link from "next/link";
import { useState } from "react";
import { href, t, type Lang } from "@/lib/i18n";

interface Ursache { titel: string; warum: string; fix: string[]; prinzip?: string }
interface Knoten { frage?: string; antworten?: [string, string][]; ursache?: number }

/** Diagnose in 2–4 Fragen, endet bei der wahrscheinlichsten Ursache. */
export default function Diagnosis({ tree, causes, principleTitles, lang = "de" }: {
  tree: Record<string, Knoten>; causes: Ursache[]; principleTitles: Record<string, string>; lang?: Lang;
}) {
  const D = t(lang).diag;
  const [path, setPath] = useState<string[]>(["q1"]);
  const [answers, setAnswers] = useState<[string, string][]>([]);
  const id = path[path.length - 1];
  const node = tree[id];
  const cause = node?.ursache !== undefined ? causes[node.ursache] : null;

  return (
    <div className="diag" aria-live="polite">
      <div className="card">
        {answers.length > 0 && (
          <ol className="trail">{answers.map(([q, a], i) => <li key={i}>{q} <b>{a}</b></li>)}</ol>
        )}
        {node?.frage && (
          <>
            <span className="mono">{D.q(path.length)}</span>
            <p className="q">{node.frage}</p>
            <div className="answers">
              {node.antworten!.map(([label, to]) => (
                <button key={label} type="button" className="btn"
                  onClick={() => { setAnswers([...answers, [node.frage!, label]]); setPath([...path, to]); }}>
                  {label}
                </button>
              ))}
            </div>
          </>
        )}
        {cause && (
          <>
            <span className="cause-label">{D.cause}</span>
            <p className="cause-title">{cause.titel}</p>
            <p style={{ margin: 0 }}>{cause.warum}</p>
            <div className="block">
              <span className="mono">{D.next}</span>
              <ul className="plain">{cause.fix.map((f) => <li key={f}>{f}</li>)}</ul>
            </div>
            {cause.prinzip && (
              <Link className="chip" href={href(lang, `/eintrag/${cause.prinzip}`)}>{D.principle}: {principleTitles[cause.prinzip] ?? cause.prinzip}</Link>
            )}
            <button type="button" className="btn ghost" onClick={() => { setPath(["q1"]); setAnswers([]); }}>{D.again}</button>
          </>
        )}
      </div>
    </div>
  );
}
