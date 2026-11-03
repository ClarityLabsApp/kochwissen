"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import type { ReviewItem } from "@/lib/content";

type State = Record<string, { ok?: boolean; note?: string }>;
const KEY = "garum:pruefung";
const TYP: Record<string, string> = { prozess: "Prozess", symptom: "Problem", ziel: "Ziel", technik: "Technik", zutat: "Zutat", stellschraube: "Stellschraube", welt: "Welt", begriff: "Begriff", gericht: "Gericht", experiment: "Experiment", labor: "Labor" };

/** Prüfliste: „Passt“ oder Anmerkung pro Eintrag, gespeichert im Browser, Ergebnis als Text zum Kopieren. */
export default function Review({ items }: { items: ReviewItem[] }) {
  const [st, setSt] = useState<State>({});
  const [view, setView] = useState<"offen" | "erledigt" | "alle">("offen");
  const [typ, setTyp] = useState<string | null>(null);
  const [open, setOpen] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  useEffect(() => { try { setSt(JSON.parse(localStorage.getItem(KEY) || "{}")); } catch { /* leer */ } }, []);
  const put = (id: string, v: { ok?: boolean; note?: string }) => setSt((s) => {
    const n = { ...s, [id]: { ...s[id], ...v } };
    if (!n[id].ok && !n[id].note) delete n[id];
    try { localStorage.setItem(KEY, JSON.stringify(n)); } catch { /* ohne Speicher */ }
    return n;
  });
  const done = (id: string) => !!st[id]?.ok || !!st[id]?.note;
  const list = useMemo(() => items.filter((e) => (!typ || e.typ === typ) && (view === "alle" || (view === "offen" ? !done(e.id) : done(e.id)))),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [items, typ, view, st]);
  const nOk = items.filter((e) => st[e.id]?.ok).length, nNote = items.filter((e) => st[e.id]?.note).length;
  const types = [...new Set(items.map((e) => e.typ))];
  const result = () => {
    const ok = items.filter((e) => st[e.id]?.ok && !st[e.id]?.note).map((e) => e.id);
    const notes = items.filter((e) => st[e.id]?.note).map((e) => `- ${e.id} (${e.titel}): ${st[e.id]!.note!.trim()}`);
    return `Prüfung Garum\n\nGEPRÜFT (${ok.length}): ${ok.join(", ")}\n\nANMERKUNGEN (${notes.length}):\n${notes.join("\n")}`;
  };
  const copy = async () => { try { await navigator.clipboard.writeText(result()); setCopied(true); setTimeout(() => setCopied(false), 2500); } catch { window.prompt("Text kopieren:", result()); } };

  return (
    <div className="review">
      <div className="review-bar">
        <div className="review-prog"><span><b>{nOk}</b> geprüft · <b>{nNote}</b> mit Anmerkung · <b>{items.length - nOk - nNote}</b> offen</span>
          <span className="review-meter"><i style={{ width: `${((nOk + nNote) / Math.max(1, items.length)) * 100}%` }} /></span></div>
        <button type="button" className="vis-btn" onClick={copy}>{copied ? "Kopiert ✓" : "Ergebnis kopieren"}</button>
      </div>
      <div className="typechips">
        {(["offen", "erledigt", "alle"] as const).map((v) => <button key={v} type="button" className="typechip" aria-pressed={view === v} onClick={() => setView(v)}>{v[0].toUpperCase() + v.slice(1)}</button>)}
        <span style={{ width: 12 }} />
        <button type="button" className="typechip" aria-pressed={!typ} onClick={() => setTyp(null)}>Alle Typen</button>
        {types.map((t) => <button key={t} type="button" className="typechip" aria-pressed={typ === t} onClick={() => setTyp(t)}><i style={{ background: `var(--t-${t})` }} />{TYP[t] ?? t}</button>)}
      </div>
      <ol className="review-list">
        {list.slice(0, 60).map((e) => (
          <li key={e.id} className={st[e.id]?.ok ? "ok" : st[e.id]?.note ? "noted" : ""}>
            <div className="rv-head">
              <span className="mono"><i style={{ background: `var(--t-${e.typ})` }} />{TYP[e.typ] ?? e.typ}{e.grund ? ` · ${e.grund}` : ""}</span>
              <Link href={`/eintrag/${e.id}`} target="_blank" className="rv-title">{e.titel} ↗</Link>
              <p>{e.kurz}</p>
            </div>
            <div className="rv-act">
              <button type="button" className={`btn${st[e.id]?.ok ? " on" : ""}`} onClick={() => put(e.id, { ok: !st[e.id]?.ok })}>{st[e.id]?.ok ? "Passt ✓" : "Passt"}</button>
              <button type="button" className="btn ghost" onClick={() => setOpen(open === e.id ? null : e.id)}>{st[e.id]?.note ? "Anmerkung ✎" : "Anmerkung"}</button>
            </div>
            {(open === e.id || st[e.id]?.note) && (
              <textarea rows={2} placeholder="Was stimmt nicht oder fehlt?" value={st[e.id]?.note ?? ""} onChange={(ev) => put(e.id, { note: ev.target.value, ok: false })} />
            )}
          </li>
        ))}
      </ol>
      {list.length > 60 && <p className="mono">Die nächsten {Math.min(60, list.length - 60)} erscheinen, sobald diese erledigt sind.</p>}
    </div>
  );
}
