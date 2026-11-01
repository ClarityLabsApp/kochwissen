import Link from "next/link";

export default function NotFound() {
  return (
    <main className="wrap">
      <h1>Diesen Eintrag gibt es nicht</h1>
      <p className="lede">Vielleicht ist er noch nicht geplant. <Link href="/">Zur Bibliothek</Link></p>
    </main>
  );
}
