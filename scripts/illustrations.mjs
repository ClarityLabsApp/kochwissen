// Erzeugt die Aquarell-Illustrationen für Welten und Zutaten über eine Bild-API.
// Jeder Eintrag mit visual.illustration bekommt ein Bild unter public/illustrationen/<id>.png.
// Danach freistellen, beschneiden und als WebP speichern (siehe CLAUDE.md, Illustrationen); die Seite zeigt nur .webp.
// Bereits vorhandene Bilder werden übersprungen (zum Neu-Erzeugen Datei löschen).
//
// Aufruf:
//   OPENAI_API_KEY=... node scripts/illustrations.mjs --test        # nur 4 Bilder zum Stil-Test
//   OPENAI_API_KEY=... node scripts/illustrations.mjs               # alle fehlenden
//   OPENAI_API_KEY=... node scripts/illustrations.mjs --only mehl,salz
//
// Optional: IMAGE_MODEL (Standard gpt-image-2.5-flare; gpt-image-1 wurde im Oktober 2026 abgeschaltet), IMAGE_QUALITY (low | medium | high, Standard medium).
// Der Stil-Prompt steht in DESIGN.md, Abschnitt 8. Hier gleich gehalten.
import { readFileSync, readdirSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const STYLE = "Vintage cookbook illustration, loose watercolor and fine ink line, warm cream paper texture, muted earthy palette (sepia, ochre, terracotta, sage), single subject centered with generous empty space, no text, no lettering, no background scene, soft natural light, hand-drawn feel, 19th-century kitchen ephemera style. Subject: ";

const key = process.env.OPENAI_API_KEY;
if (!key) { console.error("OPENAI_API_KEY fehlt."); process.exit(1); }
const model = process.env.IMAGE_MODEL || "gpt-image-2.5-flare";
const quality = process.env.IMAGE_QUALITY || "medium";
const args = process.argv.slice(2);
const only = args.includes("--only") ? args[args.indexOf("--only") + 1].split(",") : null;
const test = args.includes("--test");

const outDir = join(root, "public/illustrationen");
mkdirSync(outDir, { recursive: true });
const dir = join(root, "content/entries");
let jobs = readdirSync(dir).filter((f) => f.endsWith(".json"))
  .map((f) => JSON.parse(readFileSync(join(dir, f), "utf8")))
  .filter((e) => e.visual?.illustration)
  .filter((e) => !only || only.includes(e.id))
  .filter((e) => !existsSync(join(outDir, `${e.id}.webp`)) && !existsSync(join(outDir, `${e.id}.png`)));
if (test) jobs = jobs.filter((e) => ["w-brot", "mehl", "zwiebel", "schokolade"].includes(e.id)).slice(0, 4);

console.log(`${jobs.length} Illustration(en) zu erzeugen mit ${model} (${quality}).`);
for (const e of jobs) {
  const res = await fetch("https://api.openai.com/v1/images/generations", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model, prompt: STYLE + e.visual.illustration, size: "1024x1024", quality, n: 1 }),
  });
  if (!res.ok) { console.error(`✗ ${e.id}: ${res.status} ${await res.text()}`); continue; }
  const data = await res.json();
  const b64 = data.data?.[0]?.b64_json;
  if (!b64) { console.error(`✗ ${e.id}: keine Bilddaten in der Antwort`); continue; }
  writeFileSync(join(outDir, `${e.id}.png`), Buffer.from(b64, "base64"));
  console.log(`✓ ${e.id}`);
}
