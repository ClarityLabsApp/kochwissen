"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { href, t, type Lang } from "@/lib/i18n";

export interface QuizFrage { frage: string; antworten: string[]; richtig: number; erklaerung: string; eintrag: string; eintragTitel: string }
const KEY = (p: string) => `kochwissen:quiz:${p}`;

/** Kleines Quiz am Ende eines Lernpfads: eine Frage nach der anderen, mit Auflösung und Erklärung. */
export default function Quiz({ pfad, fragen, lang = "de" }: { pfad: string; fragen: QuizFrage[]; lang?: Lang }) {
  const Q = t(lang).quiz;
  const [i, setI] = useState(0);
  const [wahl, setWahl] = useState<number | null>(null);
  const [punkte, setPunkte] = useState(0);
  const [fertig, setFertig] = useState(false);
  const [best, setBest] = useState<number | null>(null);
  useEffect(() => { try { const v = localStorage.getItem(KEY(pfad)); if (v) setBest(Number(v)); } catch { /* ohne Speicher */ } }, [pfad]);

  const f = fragen[i];
  const antworten = (n: number) => { if (wahl !== null) return; setWahl(n); if (n === f.richtig) setPunkte((p) => p + 1); };
  const weiter = () => {
    if (i + 1 < fragen.length) { setI(i + 1); setWahl(null); return; }
    setFertig(true);
    try { if (best === null || punkte > best) { localStorage.setItem(KEY(pfad), String(punkte)); setBest(punkte); } } catch { /* ohne Speicher */ }
  };
  const neu = () => { setI(0); setWahl(null); setPunkte(0); setFertig(false); };

  if (fertig) {
    const anteil = punkte / fragen.length;
    const satz = anteil === 1 ? Q.all : anteil >= 0.6 ? Q.good : Q.low;
    return (
      <div className="quiz">
        <span className="mono">{Q.result}</span>
        <strong className="quiz-score">{Q.score(punkte, fragen.length)}</strong>
        <p>{satz}</p>
        <button type="button" className="vis-btn" onClick={neu}>{Q.again}</button>
      </div>
    );
  }

  return (
    <div className="quiz">
      <div className="quiz-head"><span className="mono">{Q.q(i + 1, fragen.length)}</span>{best !== null && <span className="mono">{Q.best(best, fragen.length)}</span>}</div>
      <p className="quiz-frage">{f.frage}</p>
      <div className="quiz-antworten" role="group" aria-label={Q.answers}>
        {f.antworten.map((a, n) => {
          const state = wahl === null ? "" : n === f.richtig ? " richtig" : n === wahl ? " falsch" : " aus";
          return <button key={a} type="button" className={`quiz-a${state}`} onClick={() => antworten(n)} disabled={wahl !== null} aria-pressed={wahl === n}>{a}</button>;
        })}
      </div>
      {wahl !== null && (
        <div className={`quiz-aufloesung${wahl === f.richtig ? " ok" : ""}`} aria-live="polite">
          <strong>{wahl === f.richtig ? Q.right : Q.wrong}</strong> {f.erklaerung}
          <div className="quiz-foot">
            <Link href={href(lang, `/eintrag/${f.eintrag}?pfad=${pfad}`)} className="linkbtn">{Q.more}: {f.eintragTitel} →</Link>
            <button type="button" className="vis-btn" onClick={weiter}>{i + 1 < fragen.length ? Q.nextQ : Q.show}</button>
          </div>
        </div>
      )}
    </div>
  );
}
