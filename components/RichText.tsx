import { parseText, termInfo } from "@/lib/content";
import type { Lang } from "@/lib/i18n";
import Term from "./Term";

/** Text mit Glossar-Markierungen [[id]] oder [[id|Anzeige]]. */
export default function RichText({ text, lang = "de" }: { text: string; lang?: Lang }) {
  return (
    <>
      {parseText(text, lang).map((p, i) =>
        p.t === "text" ? <span key={i}>{p.v}</span> : <Term key={i} label={p.label} info={termInfo(p.id, lang)} lang={lang} />
      )}
    </>
  );
}
