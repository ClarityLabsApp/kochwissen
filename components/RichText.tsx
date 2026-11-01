import { parseText, termInfo } from "@/lib/content";
import Term from "./Term";

/** Text mit Glossar-Markierungen [[id]] oder [[id|Anzeige]]. */
export default function RichText({ text }: { text: string }) {
  return (
    <>
      {parseText(text).map((p, i) =>
        p.t === "text" ? <span key={i}>{p.v}</span> : <Term key={i} label={p.label} info={termInfo(p.id)} />
      )}
    </>
  );
}
