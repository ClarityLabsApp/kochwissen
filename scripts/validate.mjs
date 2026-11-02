// Prüft alle Einträge: Schema, Verknüpfungen, Diagnosebäume, Glossar-Markierungen.
// Läuft automatisch vor jedem Build (npm run build) und manuell mit npm run validate.
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import { findUnmarked } from "./glossar.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => JSON.parse(readFileSync(join(root, p), "utf8"));
const schema = read("content/schema.json");
const master = read("content/master-list.json").eintraege;
const files = readdirSync(join(root, "content/entries")).filter((f) => f.endsWith(".json"));
const entries = files.map((f) => ({ file: f, data: read(`content/entries/${f}`) }));

const known = new Set([...master.map((e) => e.id), ...entries.map((e) => e.data.id)]);
const masterTyp = Object.fromEntries(master.map((e) => [e.id, e.typ]));
const ajv = new Ajv2020({ allErrors: true, strict: false });
const validate = ajv.compile(schema);

const errors = [];
const warn = [];
const err = (file, msg) => errors.push(`${file}: ${msg}`);

const TERM = /\[\[([a-z0-9-]+)(?:\|[^\]]+)?\]\]/g;
const textFields = (e) => [
  e.kurz, e.bild_im_kopf, e.was_passiert, e.warum_wichtig, e.bedeutung,
  ...(e.faustregeln || []), ...(e.typische_fehler || []), ...(e.schritte || []),
  e.mythos?.behauptung, e.mythos?.richtig,
  ...(e.praxis || []).map((p) => p.text),
  ...(e.ursachen || []).flatMap((u) => [u.warum, ...(u.fix || [])]),
  ...(e.schluesselmomente || []).map((m) => m.warum), e.beobachtung, e.erklaerung, e.haltbarkeit, e.ergebnis, ...(e.verwendung || []),
].filter(Boolean);

for (const { file, data: e } of entries) {
  if (file !== `${e.id}.json`) err(file, `Dateiname passt nicht zur id "${e.id}"`);
  if (!validate(e)) for (const v of validate.errors) err(file, `Schema ${v.instancePath || "/"} ${v.message}`);
  if (!masterTyp[e.id] && e.typ !== "begriff") warn.push(`${file}: steht nicht in der Masterliste`);

  const refs = [
    ...(e.links || []), ...(e.welten || []), ...(e.hebel || []), ...(e.wirkt_auf || []),
    ...(e.stellschrauben || []).map((s) => s.id), ...(e.praxis || []).map((p) => p.welt),
    ...(e.rolle || []).map((r) => r.prozess), ...(e.ursachen || []).map((u) => u.prinzip).filter(Boolean),
    ...(e.schluesselmomente || []).map((m) => m.prinzip).filter(Boolean),
  ];
  for (const r of refs) if (!known.has(r)) err(file, `Verweis auf unbekannte id "${r}"`);
  for (const s of e.stellschrauben || []) if (masterTyp[s.id] && masterTyp[s.id] !== "stellschraube") err(file, `"${s.id}" ist keine Stellschraube`);

  if (e.diagnose) {
    for (const [k, n] of Object.entries(e.diagnose)) {
      for (const [, to] of n.antworten || []) if (!e.diagnose[to]) err(file, `Diagnose ${k} zeigt auf fehlenden Knoten "${to}"`);
      if (n.ursache !== undefined && !e.ursachen?.[n.ursache]) err(file, `Diagnose ${k} zeigt auf fehlende Ursache ${n.ursache}`);
    }
    if (!e.diagnose.q1) err(file, `Diagnose braucht einen Startknoten "q1"`);
  }
  for (const t of textFields(e)) for (const m of t.matchAll(TERM)) if (!known.has(m[1])) err(file, `Glossar-Markierung [[${m[1]}]] ohne Eintrag`);
}

const unmarked = findUnmarked(entries.map((x) => x.data), known);
if (unmarked.length) warn.push(`${unmarked.length} Fachwörter ohne Glossar-Link (Liste: npm run glossar, verlinken: npm run glossar -- --fix)`);
for (const w of warn) console.warn("Hinweis:", w);
if (errors.length) {
  console.error(`\n${errors.length} Fehler:\n` + errors.map((x) => "  - " + x).join("\n"));
  process.exit(1);
}
console.log(`Inhalte geprüft: ${entries.length} Einträge, ${master.length} in der Masterliste, keine Fehler.`);
