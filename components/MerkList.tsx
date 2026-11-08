"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { href, t, type Lang } from "@/lib/i18n";
import { addMerk, toggleMerk, useMemo2 } from "@/lib/memo";

export interface MerkItem { id: string; typ: string; titel: string; kurz: string; pic: string | null }

export default function MerkList({ items, lang }: { items: MerkItem[]; lang: Lang }) {
  const T = t(lang), M = T.memo, ln = (p: string) => href(lang, p);
  const merk = useMemo2("merk");
  const byId = useMemo(() => new Map(items.map((e) => [e.id, e])), [items]);
  const list = merk.map((id) => byId.get(id)).filter(Boolean) as MerkItem[];
  const [ready, setReady] = useState(false);
  const [incoming, setIncoming] = useState<string[]>([]);
  const [copied, setCopied] = useState(false);
  useEffect(() => {
    setReady(true);
    const m = new URL(window.location.href).searchParams.get("merk");
    if (m) setIncoming(m.split(",").filter((id) => byId.has(id)).slice(0, 200));
  }, [byId]);
  const clearIncoming = () => { setIncoming([]); const u = new URL(window.location.href); u.searchParams.delete("merk"); window.history.replaceState(window.history.state, "", u); };
  const share = async () => {
    const url = `${window.location.origin}${ln("/merkliste")}?merk=${merk.join(",")}`;
    try {
      if (navigator.share) { await navigator.share({ title: "Garum", url }); return; }
      await navigator.clipboard.writeText(url); setCopied(true); setTimeout(() => setCopied(false), 2500);
    } catch { /* abgebrochen */ }
  };
  const SING = (k: string) => T.types[k]?.[2] ?? k;
  return (
    <>
      <header className="hub-head"><h1>{M.list}</h1>
        <p>{ready && list.length ? M.count(list.length) : M.lede}</p>
      </header>
      {incoming.length > 0 && (
        <div className="merk-in">
          <p>{M.shared(incoming.length)}</p>
          <div className="vis-row">
            <button type="button" className="vis-btn" onClick={() => { addMerk(incoming); clearIncoming(); }}>{M.take}</button>
            <button type="button" className="linkbtn" onClick={clearIncoming}>{M.dismiss}</button>
          </div>
        </div>
      )}
      {ready && list.length === 0 && incoming.length === 0 && (
        <div className="merk-empty">
          <p>{M.empty}</p>
          <Link className="linkbtn" href={ln("/")}>{M.browse} →</Link>
        </div>
      )}
      {list.length > 0 && (
        <>
          <div className="merk-head"><span className="mono merk-hint">{M.hint}</span>
            <button type="button" className="linkbtn" onClick={share}>{copied ? M.copied : `${M.share} →`}</button></div>
          <ul className="merk-grid">
            {list.map((e) => (
              <li key={e.id}>
                <Link href={ln(`/eintrag/${e.id}`)}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  {e.pic ? <img src={`/illustrationen/${e.pic}.webp`} alt="" width={88} height={88} loading="lazy" /> : <span className="tile2-ph" style={{ background: `var(--t-${e.typ})` }} />}
                  <span className="mg-txt">
                    <span className="mono"><i style={{ background: `var(--t-${e.typ})` }} />{SING(e.typ)}</span>
                    <strong>{e.titel}</strong>
                    {e.kurz && <span className="k">{e.kurz}</span>}
                  </span>
                </Link>
                <button type="button" className="mg-x" aria-label={`${M.remove}: ${e.titel}`} title={M.remove} onClick={() => toggleMerk(e.id)}>×</button>
              </li>
            ))}
          </ul>
        </>
      )}
    </>
  );
}
