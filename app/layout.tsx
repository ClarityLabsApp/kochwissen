import type { Metadata } from "next";
import "@fontsource-variable/fraunces/opsz.css";
import "@fontsource-variable/fraunces/opsz-italic.css";
import "@fontsource-variable/newsreader/opsz.css";
import "@fontsource-variable/newsreader/opsz-italic.css";
import "@fontsource/jetbrains-mono/400.css";
import "@fontsource/jetbrains-mono/600.css";
import "./globals.css";
import PrintHelper from "@/components/PrintHelper";
import SiteNav from "@/components/SiteNav";
import { worldList } from "@/lib/content";
import SiteFooter from "@/components/SiteFooter";
import { Analytics } from "@vercel/analytics/next";

import { SITE_URL } from "@/lib/site";
const site = SITE_URL;

export const metadata: Metadata = {
  metadataBase: new URL(site),
  title: { default: "Garum · Verstehen, warum Kochen funktioniert", template: "%s · Garum" },
  description: "Verstehen, warum Kochen und Backen funktionieren: einfach erklärt und sichtbar gemacht.",
  openGraph: { siteName: "Garum", locale: "de_CH", type: "website", images: [{ url: "/og-de.png", width: 1200, height: 630, alt: "Garum · Verstehen, warum Kochen funktioniert" }] },
  twitter: { card: "summary_large_image", images: ["/og-de.png"] },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="de">
      <body>
        <a href="#inhalt" className="skip">Zum Inhalt springen · Skip to content</a>
        <PrintHelper />
        <div className="wrap wide" style={{ paddingBottom: 0, gap: 0 }}>
          <SiteNav worlds={{ de: worldList("de"), en: worldList("en") }} />
        </div>
        <div id="inhalt">{children}</div>
        <SiteFooter />
        <Analytics />
      </body>
    </html>
  );
}
