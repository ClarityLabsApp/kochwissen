"use client";
/** Druckt die Seite; die Druckansicht blendet Navigation und Regler aus. */
export default function PrintButton() {
  return <button type="button" className="linkbtn printbtn" onClick={() => window.print()}>Drucken</button>;
}
