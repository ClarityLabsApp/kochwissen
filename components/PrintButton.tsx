"use client";
/** Druckt die Seite; die Druckansicht blendet Navigation und Regler aus. */
export default function PrintButton({ label = "Drucken" }: { label?: string }) {
  return <button type="button" className="linkbtn printbtn" onClick={() => window.print()}>{label}</button>;
}
