import type { Metadata } from "next";
import { getEntry, libraryData, titleOf } from "@/lib/content";
import { t, type Lang } from "@/lib/i18n";
import { BUCKETS } from "@/lib/fehlersuche";
import { Crumbs } from "@/components/views/HubView";
import Troubleshooter, { type TsProblem } from "@/components/Troubleshooter";

export function fehlersucheMetadata(lang: Lang): Metadata {
  return lang === "en"
    ? { title: "Troubleshooting", description: "Something is going wrong right now? Three clicks to the cause and the fix.", alternates: { canonical: "/en/fehlersuche", languages: { de: "/fehlersuche", en: "/en/fehlersuche", "x-default": "/fehlersuche" } } }
    : { title: "Fehlersuche", description: "Gerade geht etwas schief? In drei Klicks zur Ursache und zur Rettung.", alternates: { canonical: "/fehlersuche", languages: { de: "/fehlersuche", en: "/en/fehlersuche", "x-default": "/fehlersuche" } } };
}

/** Fehlersuche: Was kochst du? → Was ist passiert? → häufigste Ursache mit Handgriff, dann die Diagnose. */
export default function FehlersucheView({ lang }: { lang: Lang }) {
  const T = t(lang);
  const syms = libraryData(lang).filter((e) => e.typ === "symptom" && e.status !== "geplant");
  const problems: TsProblem[] = [];
  for (const s of syms) {
    const e = getEntry(s.id, lang);
    if (!e?.ursachen?.length || !e.diagnose) continue;
    const buckets = BUCKETS.filter((b) => (e.welten ?? []).some((w) => b.welten.includes(w)) || b.extra?.includes(e.id)).map((b) => b.id);
    const principles = Object.fromEntries(e.ursachen.filter((u) => u.prinzip).map((u) => [u.prinzip!, titleOf(u.prinzip!, lang)]));
    problems.push({ id: e.id, titel: e.titel, buckets, ursachen: e.ursachen, diagnose: e.diagnose, principles });
  }
  problems.sort((a, b) => a.titel.localeCompare(b.titel, lang));
  const buckets = BUCKETS.map((b) => ({ id: b.id, name: b.name[lang === "en" ? 1 : 0], pic: b.pic, n: problems.filter((p) => p.buckets.includes(b.id)).length }));
  return (
    <main className="wrap" id="inhalt" lang={lang}>
      <Crumbs lang={lang} trail={[[T.hub.probleme[0], "/probleme"], [lang === "en" ? "Troubleshooting" : "Fehlersuche"]]} />
      <Troubleshooter buckets={buckets} problems={problems} lang={lang} />
    </main>
  );
}
