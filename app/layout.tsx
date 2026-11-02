import type { Metadata } from "next";
import "./globals.css";
import PrintHelper from "@/components/PrintHelper";
import SiteNav from "@/components/SiteNav";

import { SITE_URL } from "@/lib/site";
const site = SITE_URL;

export const metadata: Metadata = {
  metadataBase: new URL(site),
  title: { default: "Garum · Verstehen, warum Kochen funktioniert", template: "%s · Garum" },
  description: "Verstehen, warum Kochen und Backen funktionieren: einfach erklärt und sichtbar gemacht.",
  openGraph: { siteName: "Garum", locale: "de_CH", type: "website", images: [{ url: "/illustrationen/w-brot.webp", width: 800, height: 800 }] },
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
        <a href="#inhalt" className="skip">Zum Inhalt springen · Skip to content</a>
        <PrintHelper />
        <div className="wrap wide" style={{ paddingBottom: 0, gap: 0 }}>
          <SiteNav />
        </div>
        <div id="inhalt">{children}</div>
      </body>
    </html>
  );
}
