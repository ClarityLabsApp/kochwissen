import Library from "@/components/Library";
import { readdirSync } from "node:fs";
import { join } from "node:path";
import { libraryData } from "@/lib/content";

export default function Home() {
  const items = libraryData();
  let illus: string[] = [];
  try { illus = readdirSync(join(process.cwd(), "public/illustrationen")).filter((f) => f.endsWith(".webp")).map((f) => f.slice(0, -5)); } catch { /* noch keine Bilder */ }
  const written = items.filter((e) => e.status !== "geplant").length;
  return (
    <main className="wrap wide">
      <header style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <span className="mono">Die Bibliothek · {written} von {items.length} Einträgen geschrieben</span>
        <h1>Verstehen, warum es <em>funktioniert</em></h1>
        <p className="lede">Kein Rezeptbuch, sondern die Vorgänge dahinter: einfach erklärt und sichtbar gemacht. Wer weiß, warum etwas passiert, kocht freier.</p>
      </header>
      <Library items={items} illus={illus} />
      <footer className="site"><span className="mono">Kochwissen</span><span className="mono">Inhalte im Aufbau</span></footer>
    </main>
  );
}
