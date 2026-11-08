"use client";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { href, langOf, switchPath, t } from "@/lib/i18n";
import { useMemo2 } from "@/lib/memo";

type World = { id: string; titel: string };

/** Kopfzeile auf jeder Seite: Marke, Welten-Menü mit Bildern, die vier Fragen, Lernpfade, Suche, Merkliste, Sprache.
 *  Unter etwa 1000 px wird alles zu einem Menü-Knopf. Die Sprache folgt dem Pfad (/en/… = Englisch). */
export default function SiteNav({ worlds }: { worlds: Record<"de" | "en", World[]> }) {
  const path = usePathname() || "/";
  const router = useRouter();
  const lang = langOf(path), T = t(lang), H = T.hub, ln = (p: string) => href(lang, p);
  const merk = useMemo2("merk");
  const [open, setOpen] = useState<"" | "welten" | "menu" | "suche">("");
  const [q, setQ] = useState("");
  const box = useRef<HTMLDivElement>(null);
  const input = useRef<HTMLInputElement>(null);
  // Das Wurzel-Layout ist gemeinsam; die Sprache des Dokuments folgt hier dem Pfad.
  useEffect(() => { document.documentElement.lang = lang; }, [lang]);
  // Beim Seitenwechsel alles schließen.
  useEffect(() => { setOpen(""); }, [path]);
  // Klick daneben oder Escape schließt Menüs.
  useEffect(() => {
    if (!open) return;
    const off = (e: MouseEvent) => { if (box.current && !box.current.contains(e.target as Node)) setOpen(""); };
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(""); };
    document.addEventListener("mousedown", off); document.addEventListener("keydown", esc);
    return () => { document.removeEventListener("mousedown", off); document.removeEventListener("keydown", esc); };
  }, [open]);
  useEffect(() => { if (open === "suche") input.current?.focus(); }, [open]);

  const isHome = path === "/" || path === "/en";
  const toggleSearch = () => {
    // Auf der Startseite gibt es das große Suchfeld schon: dorthin springen.
    const big = document.getElementById("q") as HTMLInputElement | null;
    if (isHome && big) { big.scrollIntoView({ behavior: "smooth", block: "center" }); big.focus({ preventScroll: true }); setOpen(""); return; }
    setOpen(open === "suche" ? "" : "suche");
  };
  const submit = (e: React.FormEvent) => { e.preventDefault(); if (q.trim()) router.push(`${ln("/")}?q=${encodeURIComponent(q.trim())}`); };
  const W = worlds[lang] ?? [];
  const groups = [["probleme", H.navProbleme], ["ziele", H.navZiele], ["verstehen", H.navVerstehen], ["ausprobieren", H.navAusprobieren]] as const;
  const here = (p: string) => (path === ln(p) || path.startsWith(ln(p) + "/") ? "page" : undefined);

  const worldGrid = (
    <div className="nav-worlds">
      {W.map((w) => (
        <Link key={w.id} href={ln(`/eintrag/${w.id}`)} className="nav-world">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={`/illustrationen/${w.id}.webp`} alt="" width={64} height={64} loading="lazy" /><span>{w.titel}</span>
        </Link>
      ))}
    </div>
  );

  return (
    <div className="sitebar" ref={box}>
      <Link href={ln("/")} className="brand" aria-label="Garum">{/* eslint-disable-next-line @next/next/no-img-element */}<img src="/logo.svg" alt="" width={28} height={28} /><span>Gar<em>um</em></span></Link>
      <nav className="topnav" aria-label="Navigation">
        <div className="nav-full">
          <button type="button" className="nav-drop" aria-expanded={open === "welten"} onClick={() => setOpen(open === "welten" ? "" : "welten")}>{H.welten} <span aria-hidden>▾</span></button>
          {groups.map(([k, label]) => <Link key={k} href={ln(`/${k}`)} aria-current={here(`/${k}`)}>{label}</Link>)}
          <Link href={ln("/pfad")} aria-current={here("/pfad")}>{T.nav.paths}</Link>
        </div>
        <button type="button" className="nav-icon" aria-label={H.search} aria-expanded={open === "suche"} onClick={toggleSearch}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden><circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" /></svg>
        </button>
        <Link href={ln("/merkliste")} aria-current={here("/merkliste")} className="nav-icon nav-merk" aria-label={`${H.merk} (${merk.length})`}>
          <svg width="16" height="18" viewBox="0 0 16 20" fill={merk.length ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" aria-hidden><path d="M2 2h12v16l-6-4-6 4z" /></svg>
          {merk.length > 0 && <small>{merk.length}</small>}
        </Link>
        <span className="langs" role="group" aria-label="Sprache · Language">
          <Link href={switchPath(path, "de")} hrefLang="de" aria-current={lang === "de" ? "true" : undefined}>DE</Link>
          <Link href={switchPath(path, "en")} hrefLang="en" aria-current={lang === "en" ? "true" : undefined}>EN</Link>
        </span>
        <button type="button" className="nav-burger" aria-expanded={open === "menu"} onClick={() => setOpen(open === "menu" ? "" : "menu")}>{open === "menu" ? H.close : H.menu}</button>
      </nav>

      {open === "welten" && (
        <div className="nav-panel">
          <div className="nav-panel-head"><span className="mono">{H.welten}</span><span className="nav-panel-lede">{H.worldsLede}</span></div>
          {worldGrid}
        </div>
      )}
      {open === "suche" && (
        <form className="nav-panel nav-search" onSubmit={submit} role="search">
          <input ref={input} type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder={T.search.placeholder} aria-label={H.search} />
          <button type="submit" className="vis-btn">{H.search}</button>
        </form>
      )}
      {open === "menu" && (
        <div className="nav-panel nav-mobile">
          <ul className="nav-mlist">
            {groups.map(([k]) => <li key={k}><Link href={ln(`/${k}`)}><strong>{H[k][0]}</strong><span>{H[k][1]}</span></Link></li>)}
            <li><Link href={ln("/pfad")}><strong>{T.nav.paths}</strong></Link></li>
            <li><Link href={ln("/alle")}><strong>{H.az}</strong></Link></li>
          </ul>
          <span className="mono">{H.welten}</span>
          {worldGrid}
        </div>
      )}
    </div>
  );
}
