"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { href, t, type Lang } from "@/lib/i18n";

export interface StepView { id: string; titel: string; typ: string; kurz: string; warum: string }
const KEY = (p: string) => `kochwissen:pfad:${p}`;
export function readDone(pfad: string): string[] { try { return JSON.parse(localStorage.getItem(KEY(pfad)) || "[]"); } catch { return []; } }
export function writeDone(pfad: string, ids: string[]) { try { localStorage.setItem(KEY(pfad), JSON.stringify(ids)); } catch { /* ohne Speicher geht es auch */ } }

/** Schritte eines Lernpfads zum Abhaken. Der Fortschritt bleibt im Browser gespeichert. */
export default function PathSteps({ pfad, steps, lang = "de" }: { pfad: string; steps: StepView[]; lang?: Lang }) {
  const P = t(lang).path, ln = (p: string) => href(lang, p);
  const [done, setDone] = useState<string[]>([]);
  useEffect(() => setDone(readDone(pfad)), [pfad]);
  const toggle = (id: string) => { const n = done.includes(id) ? done.filter((d) => d !== id) : [...done, id]; setDone(n); writeDone(pfad, n); };
  const next = steps.find((s) => !done.includes(s.id));
  return (
    <>
      <div className="pfad-progress">
        <div className="bar"><i style={{ width: `${(done.length / steps.length) * 100}%` }} /></div>
        <span className="mono">{P.done(done.length, steps.length)}</span>
        {next && <Link className="vis-btn" href={ln(`/eintrag/${next.id}?pfad=${pfad}`)}>{done.length ? P.cont : P.start}: {next.titel} →</Link>}
      </div>
      <ol className="pfad-steps">
        {steps.map((s, i) => (
          <li key={s.id} className={done.includes(s.id) ? "done" : ""}>
            <button type="button" className="check" aria-pressed={done.includes(s.id)} aria-label={P.mark(s.titel)} onClick={() => toggle(s.id)}>{done.includes(s.id) ? "✓" : i + 1}</button>
            <div>
              <Link href={ln(`/eintrag/${s.id}?pfad=${pfad}`)} className="t"><i style={{ background: `var(--t-${s.typ})` }} />{s.titel}</Link>
              <p>{s.warum}</p>
            </div>
          </li>
        ))}
      </ol>
    </>
  );
}
