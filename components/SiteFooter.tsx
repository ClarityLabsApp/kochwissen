"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { href, langOf, t } from "@/lib/i18n";
import { INSTAGRAM_URL } from "@/lib/site";

/** Fußzeile auf jeder Seite: Name, Impressum, Datenschutz. */
export default function SiteFooter() {
  const lang = langOf(usePathname() ?? "/"), T = t(lang);
  return (
    <div className="wrap wide" style={{ paddingTop: 0 }}>
      <nav className="footer-map mono" aria-label={T.hub.explore}>
        {(["probleme", "ziele", "verstehen", "ausprobieren"] as const).map((k) => <Link key={k} href={href(lang, `/${k}`)}>{T.hub[k][0]}</Link>)}
        <Link href={href(lang, "/pfad")}>{T.nav.paths}</Link>
        <Link href={href(lang, "/alle")}>{T.hub.azTitle}</Link>
      </nav>
      <footer className="site">
        <span className="mono">{T.home.footerA}</span>
        <span className="mono footer-links">
          <a href={INSTAGRAM_URL} target="_blank" rel="noopener noreferrer" className="ig" aria-label="Garum auf Instagram">
            <svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" strokeWidth="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" strokeWidth="2"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/></svg>
            Instagram
          </a>
          <Link href={href(lang, "/impressum")}>{lang === "en" ? "Legal notice" : "Impressum"}</Link>
          <Link href={href(lang, "/datenschutz")}>{lang === "en" ? "Privacy" : "Datenschutz"}</Link>
        </span>
      </footer>
    </div>
  );
}
