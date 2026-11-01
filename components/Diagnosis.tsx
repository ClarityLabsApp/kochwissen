"use client";
import Link from "next/link";
import { useState } from "react";

interface Ursache { titel: string; warum: string; fix: string[]; prinzip?: string }
interface Knoten { frage?: string; antworten?: [string, string][]; ursache?: number }

/** Diagnose in 2–4 Fragen, endet bei der wahrscheinlichsten Ursache. */
export default function Diagnosis({ tree, causes, principleTitles }: {
  tree: Record<string, Knoten>; causes: Ursache[]; principleTitles: Record<string, string>;
}) {
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
            <span className="mono">Frage {path.length}</span>
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
            <span className="cause-label">WAHRSCHEINLICHE URSACHE</span>
            <p className="cause-title">{cause.titel}</p>
            <p style={{ margin: 0 }}>{cause.warum}</p>
            <div className="block">
              <span className="mono">Nächstes Mal</span>
              <ul className="plain">{cause.fix.map((f) => <li key={f}>{f}</li>)}</ul>
            </div>
            {cause.prinzip && (
              <Link className="chip" href={`/eintrag/${cause.prinzip}`}>Prinzip dahinter: {principleTitles[cause.prinzip] ?? cause.prinzip}</Link>
            )}
            <button type="button" className="btn ghost" onClick={() => { setPath(["q1"]); setAnswers([]); }}>Nochmal von vorn</button>
          </>
        )}
      </div>
    </div>
  );
}
