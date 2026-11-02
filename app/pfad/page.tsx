import Link from "next/link";
import type { Metadata } from "next";
import { lernpfade } from "@/lib/content";

export const metadata: Metadata = { title: "Lernpfade" };

export default function Pfade() {
  return (
    <main className="wrap wide">
      <header style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <span className="mono">Lernpfade</span>
        <h1>Der Reihe nach <em>verstehen</em></h1>
        <p className="lede">Geführte Wege durch die Bibliothek. Jeder Schritt baut auf dem vorigen auf, und du kannst abhaken, was du schon gelesen hast.</p>
      </header>
      <div className="pfad-cards">
        {lernpfade().map((p) => (
          <Link key={p.id} href={`/pfad/${p.id}`} className="pfad-card">
            <span className="mono">{p.schritte.length} Schritte · {p.dauer}</span>
            <strong>{p.titel}</strong>
            <span className="k">{p.kurz}</span>
            <span className="f">{p.fuer}</span>
          </Link>
        ))}
      </div>
    </main>
  );
}
