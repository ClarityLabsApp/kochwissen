"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { readDone, writeDone } from "./PathSteps";

export interface PathInfo { id: string; titel: string; schritte: { id: string; titel: string }[] }

/** Zeigt auf einer Eintragsseite, wo man im Lernpfad steht, und führt zum nächsten Schritt. Aktiv nur mit ?pfad=… */
export default function PathNav({ entry, paths }: { entry: string; paths: PathInfo[] }) {
  const [pfad, setPfad] = useState<PathInfo | null>(null);
  useEffect(() => {
    const id = new URLSearchParams(window.location.search).get("pfad");
    const p = paths.find((x) => x.id === id) ?? null;
    setPfad(p);
    if (p) { const d = readDone(p.id); if (!d.includes(entry)) writeDone(p.id, [...d, entry]); }
  }, [entry, paths]);
  if (!pfad) return null;
  const i = pfad.schritte.findIndex((s) => s.id === entry);
  const prev = pfad.schritte[i - 1], next = pfad.schritte[i + 1];
  return (
    <nav className="pathnav" aria-label="Lernpfad">
      <Link href={`/pfad/${pfad.id}`} className="mono">Lernpfad · {pfad.titel} · Schritt {i + 1} von {pfad.schritte.length}</Link>
      <div className="row">
        {prev ? <Link href={`/eintrag/${prev.id}?pfad=${pfad.id}`}>← {prev.titel}</Link> : <span />}
        {next ? <Link href={`/eintrag/${next.id}?pfad=${pfad.id}`} className="next">{next.titel} →</Link> : <Link href={`/pfad/${pfad.id}`} className="next">Geschafft. Zurück zum Lernpfad →</Link>}
      </div>
    </nav>
  );
}
