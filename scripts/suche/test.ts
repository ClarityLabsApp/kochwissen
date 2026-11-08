// Prüft die Suche mit typischen Fragen: npx tsx scripts/suche/test.ts
import { readFileSync } from "node:fs";
import { libraryData, searchExtras } from "../../lib/content";
import { search } from "../../lib/search";
const F = JSON.parse(readFileSync(process.argv.find((a) => a.endsWith(".json")) ?? "scripts/suche/fragen.json", "utf8"));
let total = 0, top1 = 0, top3 = 0; const miss: string[] = [];
for (const lang of ["de", "en"] as const) {
  const items = libraryData(lang) as any[];
  const extras = process.argv.includes("--ohne") ? undefined : searchExtras(lang);
  for (const [q, want] of F[lang] as [string, string[]][]) {
    total++;
    const r = search(items, q, extras);
    const ids = r ? [...r.scores.entries()].sort((a, b) => b[1] - a[1]).map(([id]) => id) : [];
    const best = r?.best?.id ?? "";
    const ok = (id: string) => want.some((w) => (w.endsWith("-") ? id.startsWith(w) : id === w));
    if (ok(best)) top1++;
    if (ids.slice(0, 3).some(ok) || ok(best)) top3++; else miss.push(`${lang}: "${q}" → ${best} | ${ids.slice(0, 3).join(", ")} (erwartet ${want.join("/")})`);
    if (!ok(best) && process.argv.includes("-v")) console.log(`  1≠ ${lang} "${q}" → ${best}`);
  }
}
console.log(`Beste Antwort richtig: ${top1}/${total}, unter den ersten 3: ${top3}/${total}`);
for (const m of miss) console.log("  ✗", m);
