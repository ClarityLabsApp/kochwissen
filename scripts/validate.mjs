// Prüft alle Einträge: Schema, Verknüpfungen, Diagnosebäume, Glossar-Markierungen.
// Läuft automatisch vor jedem Build (npm run build) und manuell mit npm run validate.
import { existsSync, readFileSync, readdirSync } from "node:fs";
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
// Schreibleitfaden: jede Analogie nur einmal, Sätze unter 25 Wörtern, kein Werbeton
const plainT = (s) => s.replace(/\[\[[a-z0-9-]+\|([^\]]+)\]\]/g, "$1").replace(/\[\[([a-z0-9-]+)\]\]/g, "$1");
const bik = new Map();
for (const { data: e } of entries) {
  if (e.bild_im_kopf) {
    const key = plainT(e.bild_im_kopf).toLowerCase().split(/[:,]/)[0].trim().slice(0, 40);
    if (bik.has(key)) warn.push(`${e.id}: Analogie „${key}“ schon in ${bik.get(key)}`); else bik.set(key, e.id);
  } else if (e.typ !== "begriff") warn.push(`${e.id}: kein bild_im_kopf`);
  for (const t of [...textFields(e), e.titel]) {
    const s = plainT(t);
    if (/!|ganz einfach|Geheimtipp|perfekt|ultimativ|kinderleicht/i.test(s)) warn.push(`${e.id}: Werbeton in „${s.slice(0, 60)}…“`);
    for (const satz of s.split(/(?<=[.?!])\s+/)) if (satz.split(/\s+/).length > 25) warn.push(`${e.id}: Satz mit ${satz.split(/\s+/).length} Wörtern: „${satz.slice(0, 60)}…“`);
  }
}
const pfade = read("content/lernpfade.json");
for (const p of pfade) {
  for (const s of p.schritte) if (!known.has(s.id)) errors.push(`lernpfade.json: ${p.id} verweist auf unbekannte id "${s.id}"`);
  for (const q of p.quiz || []) {
    if (!known.has(q.eintrag)) errors.push(`lernpfade.json: Quiz in ${p.id} verweist auf unbekannte id "${q.eintrag}"`);
    if (!(q.richtig >= 0 && q.richtig < q.antworten.length)) errors.push(`lernpfade.json: Quiz in ${p.id}: richtige Antwort fehlt bei „${q.frage}“`);
  }
}

// Englische Übersetzungen: nur Textfelder, Aufbau und Verweise müssen dem deutschen Eintrag gleichen.
const FIXED = ["typ", "status", "links", "hebel", "welten", "schwierigkeit", "quellen"];
const enDir = join(root, "content/en/entries");
let enCount = 0;
if (existsSync(enDir)) {
  const de = Object.fromEntries(entries.map((x) => [x.data.id, x.data]));
  for (const f of readdirSync(enDir).filter((f) => f.endsWith(".json"))) {
    const file = `en/${f}`, t = read(`content/en/entries/${f}`), id = f.replace(/\.json$/, ""), o = de[id];
    enCount++;
    if (!o) { err(file, "kein deutscher Eintrag mit dieser id"); continue; }
    if (t.id && t.id !== id) err(file, "id passt nicht zum Dateinamen");
    for (const k of FIXED) if (k in t && JSON.stringify(t[k]) !== JSON.stringify(o[k])) err(file, `"${k}" darf in der Übersetzung nicht abweichen`);
    for (const [k, v] of Object.entries(t)) {
      if (k === "synonyme" || !Array.isArray(v) || !Array.isArray(o[k])) continue;
      if (v.length !== o[k].length) { err(file, `"${k}" hat ${v.length} statt ${o[k].length} Elemente`); continue; }
      v.forEach((x, i) => {
        for (const ref of ["id", "prozess", "prinzip", "welt", "haeufigkeit"]) if (x && typeof x === "object" && JSON.stringify(x[ref]) !== JSON.stringify(o[k][i][ref])) err(file, `"${k}[${i}].${ref}" weicht ab`);
      });
    }
    if (t.diagnose) {
      const a = Object.keys(o.diagnose ?? {}).sort().join(), b = Object.keys(t.diagnose).sort().join();
      if (a !== b) err(file, "diagnose hat andere Knoten");
      for (const [k, n] of Object.entries(t.diagnose)) {
        const on = o.diagnose?.[k]; if (!on) continue;
        if (n.ursache !== on.ursache) err(file, `diagnose.${k}.ursache weicht ab`);
        if (JSON.stringify((n.antworten ?? []).map((x) => x[1])) !== JSON.stringify((on.antworten ?? []).map((x) => x[1]))) err(file, `diagnose.${k}: Antwortziele weichen ab`);
      }
    }
    const merged = { ...o, ...t, visual: t.visual ? { ...o.visual, ...t.visual, params: { ...(o.visual?.params ?? {}), ...(t.visual.params ?? {}) } } : o.visual };
    if (!validate(merged)) err(file, ajv.errorsText(validate.errors));
    for (const txt of textFields(t)) for (const [, ref] of txt.matchAll(TERM)) if (!known.has(ref)) err(file, `Glossar verweist auf unbekannte id "${ref}"`);
  }
}
const enPfade = join(root, "content/en/lernpfade.json");
if (existsSync(enPfade)) {
  const byId = Object.fromEntries(pfade.map((p) => [p.id, p]));
  for (const p of read("content/en/lernpfade.json")) {
    const o = byId[p.id];
    if (!o) { errors.push(`en/lernpfade.json: unbekannter Pfad "${p.id}"`); continue; }
    if (p.schritte && JSON.stringify(p.schritte.map((s) => s.id)) !== JSON.stringify(o.schritte.map((s) => s.id))) errors.push(`en/lernpfade.json: ${p.id} hat andere Schritte`);
    if (p.quiz) {
      if (p.quiz.length !== (o.quiz ?? []).length) errors.push(`en/lernpfade.json: ${p.id} hat ${p.quiz.length} statt ${(o.quiz ?? []).length} Quizfragen`);
      p.quiz.forEach((q, i) => { const oq = o.quiz?.[i]; if (oq && (q.richtig !== oq.richtig || q.eintrag !== oq.eintrag || q.antworten.length !== oq.antworten.length)) errors.push(`en/lernpfade.json: Quizfrage ${i + 1} in ${p.id} weicht im Aufbau ab`); });
    }
  }
}
for (const w of warn) console.warn("Hinweis:", w);
if (errors.length) {
  console.error(`\n${errors.length} Fehler:\n` + errors.map((x) => "  - " + x).join("\n"));
  process.exit(1);
}
console.log(`Inhalte geprüft: ${entries.length} Einträge (${enCount} auf Englisch), ${master.length} in der Masterliste, keine Fehler.`);
