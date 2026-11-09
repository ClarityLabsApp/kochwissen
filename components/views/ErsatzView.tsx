import type { Metadata } from "next";
import { hasPicture, titleOf } from "@/lib/content";
import { t, type Lang } from "@/lib/i18n";
import { ERSATZ, GRUPPEN } from "@/lib/ersatz";
import { Crumbs } from "@/components/views/HubView";
import ErsatzList, { type ErsatzCard } from "@/components/ErsatzList";

export function ersatzMetadata(lang: Lang): Metadata {
  const alt = { canonical: lang === "en" ? "/en/ersatz" : "/ersatz", languages: { de: "/ersatz", en: "/en/ersatz", "x-default": "/ersatz" } };
  return lang === "en"
    ? { title: "Ingredient substitutes", description: "Out of baking powder, buttermilk, eggs or wine? What to use instead, and why it works.", alternates: alt }
    : { title: "Zutaten ersetzen", description: "Backpulver, Buttermilch, Ei oder Wein fehlt? Was du stattdessen nimmst und warum das funktioniert.", alternates: alt };
}

export const ersatzTitle = (lang: Lang) => (lang === "en" ? "What if you're out of …?" : "Was tun, wenn … fehlt?");

/** Ersatz-Seite: häufige fehlende Zutaten, je mit Ersatz, Warum und Vorsicht. */
export default function ErsatzView({ lang }: { lang: Lang }) {
  const T = t(lang), L = lang === "en" ? 1 : 0;
  const cards: ErsatzCard[] = ERSATZ.map((x) => ({
    id: x.id, gruppe: x.gruppe, fehlt: x.fehlt[L],
    statt: x.statt.map((s) => ({ wie: s.wie[L], gut: s.gut?.[L] })),
    warum: x.warum[L], achtung: x.achtung?.[L],
    pic: x.zu.find((id) => hasPicture(id)) ?? null,
    zu: x.zu.map((id) => ({ id, titel: titleOf(id, lang) })),
  }));
  const gruppen = Object.entries(GRUPPEN).map(([k, v]) => ({ id: k, name: v[L] }));
  return (
    <main className="wrap" id="inhalt" lang={lang}>
      <Crumbs lang={lang} trail={[[T.hub.verstehen[0], "/verstehen"], [lang === "en" ? "Substitutes" : "Zutaten ersetzen"]]} />
      <header className="hub-head">
        <h1>{ersatzTitle(lang)}</h1>
        <p>{lang === "en"
          ? "Common gaps in the cupboard, what you can use instead, and why it works. Quantities are guide values."
          : "Häufige Lücken im Vorratsschrank, was du stattdessen nimmst und warum das funktioniert. Mengen sind Richtwerte."}</p>
      </header>
      <ErsatzList cards={cards} gruppen={gruppen} lang={lang} />
    </main>
  );
}
