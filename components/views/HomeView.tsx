import { readdirSync } from "node:fs";
import { join } from "node:path";
import Library from "@/components/Library";
import { appearsIn, hasPicture, libraryData, lernpfade } from "@/lib/content";
import { t, type Lang } from "@/lib/i18n";

/** Bis zu drei Bilder für einen Lernpfad: eigene Bilder der Schritte, sonst Bilder, bei denen die Schritte vorkommen. */
export function pfadPics(ids: string[]) {
  const own = ids.filter(hasPicture);
  const more = ids.flatMap((id) => appearsIn(id, 3));
  return [...new Set([...own, ...more])].slice(0, 3);
}

export default function HomeView({ lang }: { lang: Lang }) {
  const T = t(lang);
  const items = libraryData(lang);
  let illus: string[] = [];
  try { illus = readdirSync(join(process.cwd(), "public/illustrationen")).filter((f) => f.endsWith(".webp")).map((f) => f.slice(0, -5)); } catch { /* noch keine Bilder */ }
  return (
    <main className="wrap wide" lang={lang}>
      <header style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <h1>{T.home.h1a}<em>{T.home.h1b}</em></h1>
        <p className="lede">{T.home.lede}</p>
      </header>
      <Library items={items} illus={illus} lang={lang} pfade={lernpfade(lang).map((p) => ({ id: p.id, titel: p.titel, n: p.schritte.length, dauer: p.dauer, fuer: p.fuer, pics: pfadPics(p.schritte.map((x) => x.id)) }))} />
      <footer className="site"><span className="mono">{T.home.footerA}</span><span className="mono">{T.home.footerB}</span></footer>
    </main>
  );
}
