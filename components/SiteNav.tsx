"use client";
import Link from "next/link";
import { useEffect } from "react";
import { usePathname } from "next/navigation";
import { href, langOf, switchPath, t } from "@/lib/i18n";

/** Kopfzeile: Marke, Navigation und Sprachauswahl. Die Sprache folgt dem Pfad (/en/… = Englisch). */
export default function SiteNav() {
  const path = usePathname() || "/";
  const lang = langOf(path), T = t(lang);
  // Das Wurzel-Layout ist gemeinsam; die Sprache des Dokuments folgt hier dem Pfad.
  useEffect(() => { document.documentElement.lang = lang; }, [lang]);
  return (
    <div className="sitebar">
      <Link href={href(lang, "/")} className="brand">Koch<em>wissen</em></Link>
      <nav className="topnav" aria-label="Navigation">
        <Link href={href(lang, "/")}>{T.nav.library}</Link>
        <Link href={href(lang, "/pfad")}>{T.nav.paths}</Link>
        <span className="langs" role="group" aria-label="Sprache · Language">
          <Link href={switchPath(path, "de")} hrefLang="de" aria-current={lang === "de" ? "true" : undefined}>DE</Link>
          <Link href={switchPath(path, "en")} hrefLang="en" aria-current={lang === "en" ? "true" : undefined}>EN</Link>
        </span>
      </nav>
    </div>
  );
}
