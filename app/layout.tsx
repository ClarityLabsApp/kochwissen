import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Kochwissen", template: "%s · Kochwissen" },
  description: "Verstehen, warum Kochen und Backen funktionieren – einfach erklärt und sichtbar gemacht.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="de">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        {/* eslint-disable-next-line @next/next/no-page-custom-font */}
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Newsreader:opsz,wght@6..72,400;6..72,500&family=JetBrains+Mono:wght@400;600&display=swap"
        />
      </head>
      <body>
        <div className="wrap wide" style={{ paddingBottom: 0, gap: 0 }}>
          <div className="sitebar">
            <Link href="/" className="brand">Koch<em>wissen</em></Link>
            <nav className="topnav"><Link href="/">Bibliothek</Link><Link href="/pfad">Lernpfade</Link></nav>
          </div>
        </div>
        {children}
      </body>
    </html>
  );
}
