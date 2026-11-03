"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { href, langOf, t } from "@/lib/i18n";

/** Fußzeile auf jeder Seite: Name, Impressum, Datenschutz. */
export default function SiteFooter() {
  const lang = langOf(usePathname() ?? "/"), T = t(lang);
  return (
    <div className="wrap wide" style={{ paddingTop: 0 }}>
      <footer className="site">
        <span className="mono">{T.home.footerA}</span>
        <span className="mono footer-links">
          <Link href={href(lang, "/impressum")}>{lang === "en" ? "Legal notice" : "Impressum"}</Link>
          <Link href={href(lang, "/datenschutz")}>{lang === "en" ? "Privacy" : "Datenschutz"}</Link>
        </span>
      </footer>
    </div>
  );
}
