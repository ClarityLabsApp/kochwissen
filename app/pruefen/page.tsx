import type { Metadata } from "next";
import Review from "@/components/Review";
import { DOORS } from "@/lib/home";
import { reviewList } from "@/lib/content";

export const metadata: Metadata = { title: "Prüfliste", robots: { index: false, follow: false } };

/** Versteckte Prüfseite: nicht verlinkt, nicht in der Sitemap, nicht indexiert. */
export default function Page() {
  const items = reviewList(DOORS.flatMap((d) => d.ids));
  return (
    <main className="wrap wide">
      <header style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <span className="mono">Intern · nicht verlinkt</span>
        <h1>Prüfliste</h1>
        <p className="lede">Wichtigstes zuerst. Pro Eintrag lesen, dann «Passt» oder eine Anmerkung. Alles bleibt in diesem Browser gespeichert. Zum Schluss «Ergebnis kopieren» und in den Chat mit Claude einfügen.</p>
      </header>
      <Review items={items} />
    </main>
  );
}
