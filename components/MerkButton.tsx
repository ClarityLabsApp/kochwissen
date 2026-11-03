"use client";
import { useEffect } from "react";
import { markRead, toggleMerk, useMemo2 } from "@/lib/memo";
import { t, type Lang } from "@/lib/i18n";

/** Lesezeichen auf der Eintragsseite. Markiert den Eintrag zugleich als gelesen. */
export default function MerkButton({ id, lang = "de" }: { id: string; lang?: Lang }) {
  const M = t(lang).memo, merk = useMemo2("merk"), on = merk.includes(id);
  useEffect(() => { markRead(id); }, [id]);
  return (
    <button type="button" className={`merk${on ? " on" : ""}`} aria-pressed={on} onClick={() => toggleMerk(id)}>
      <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M6 3h12v18l-6-4.5L6 21z" fill={on ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinejoin="round" /></svg>
      {on ? M.saved : M.save}
    </button>
  );
}
