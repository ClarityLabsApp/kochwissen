"use client";
import Link from "next/link";
import { useEffect, useState } from "react";

export interface StepView { id: string; titel: string; typ: string; kurz: string; warum: string }
const KEY = (p: string) => `kochwissen:pfad:${p}`;
export function readDone(pfad: string): string[] { try { return JSON.parse(localStorage.getItem(KEY(pfad)) || "[]"); } catch { return []; } }
export function writeDone(pfad: string, ids: string[]) { try { localStorage.setItem(KEY(pfad), JSON.stringify(ids)); } catch { /* ohne Speicher geht es auch */ } }

/** Schritte eines Lernpfads zum Abhaken. Der Fortschritt bleibt im Browser gespeichert. */
export default function PathSteps({ pfad, steps }: { pfad: string; steps: StepView[] }) {
  const [done, setDone] = useState<string[]>([]);
  useEffect(() => setDone(readDone(pfad)), [pfad]);
  const toggle = (id: string) => { const n = done.includes(id) ? done.filter((d) => d !== id) : [...done, id]; setDone(n); writeDone(pfad, n); };
  const next = steps.find((s) => !done.includes(s.id));
  return (
    <>
      <div className="pfad-progress">
        <div className="bar"><i style={{ width: `${(done.length / steps.length) * 100}%` }} /></div>
        <span className="mono">{done.length} von {steps.length} erledigt</span>
        {next && <Link className="vis-btn" href={`/eintrag/${next.id}?pfad=${pfad}`}>{done.length ? "Weiter" : "Starten"}: {next.titel} →</Link>}
      </div>
      <ol className="pfad-steps">
        {steps.map((s, i) => (
          <li key={s.id} className={done.includes(s.id) ? "done" : ""}>
            <button type="button" className="check" aria-pressed={done.includes(s.id)} aria-label={`${s.titel} als erledigt markieren`} onClick={() => toggle(s.id)}>{done.includes(s.id) ? "✓" : i + 1}</button>
            <div>
              <Link href={`/eintrag/${s.id}?pfad=${pfad}`} className="t"><i style={{ background: `var(--t-${s.typ})` }} />{s.titel}</Link>
              <p>{s.warum}</p>
            </div>
          </li>
        ))}
      </ol>
    </>
  );
}
