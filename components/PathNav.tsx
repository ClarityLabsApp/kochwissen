"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { readDone, writeDone } from "./PathSteps";
import { href, t, type Lang } from "@/lib/i18n";

export interface PathInfo { id: string; titel: string; schritte: { id: string; titel: string }[] }

/** Zeigt auf einer Eintragsseite, wo man im Lernpfad steht, und führt zum nächsten Schritt. Aktiv nur mit ?pfad=… */
export default function PathNav({ entry, paths, lang = "de" }: { entry: string; paths: PathInfo[]; lang?: Lang }) {
  const P = t(lang).path, ln = (p: string) => href(lang, p);
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
      <Link href={ln(`/pfad/${pfad.id}`)} className="mono">{P.nav(pfad.titel, i + 1, pfad.schritte.length)}</Link>
      <div className="row">
        {prev ? <Link href={ln(`/eintrag/${prev.id}?pfad=${pfad.id}`)}>← {prev.titel}</Link> : <span />}
        {next ? <Link href={ln(`/eintrag/${next.id}?pfad=${pfad.id}`)} className="next">{next.titel} →</Link> : <Link href={ln(`/pfad/${pfad.id}#quiz`)} className="next">{P.finished}</Link>}
      </div>
    </nav>
  );
}
