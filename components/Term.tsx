"use client";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { href, t, type Lang } from "@/lib/i18n";

export interface TermData { id: string; titel: string; kurz: string | null; ausgeschrieben: boolean }

/** Fachbegriff im Text: Antippen zeigt die Kurzerklärung, der Link führt zum Eintrag. */
export default function Term({ label, info, lang = "de" }: { label: string; info: TermData; lang?: Lang }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    if (!open) return;
    const close = (e: MouseEvent) => { if (!ref.current?.contains(e.target as Node)) setOpen(false); };
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    document.addEventListener("click", close);
    document.addEventListener("keydown", esc);
    return () => { document.removeEventListener("click", close); document.removeEventListener("keydown", esc); };
  }, [open]);
  return (
    <span className="term" ref={ref}>
      <button type="button" aria-expanded={open} onClick={() => setOpen((o) => !o)}>{label}</button>
      {open && (
        <span className="pop" role="dialog" aria-label={info.titel}>
          <span className="mono">{info.titel}</span>
          <span>{info.kurz ?? t(lang).term.soon}</span>
          <Link href={href(lang, `/eintrag/${info.id}`)}>{t(lang).term.go}</Link>
        </span>
      )}
    </span>
  );
}
