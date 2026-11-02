import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import PathSteps from "@/components/PathSteps";
import { getEntry, getPfad, lernpfade, plainText, titleOf, typOf } from "@/lib/content";

type Params = { params: Promise<{ id: string }> };
export function generateStaticParams() { return lernpfade().map((p) => ({ id: p.id })); }
export async function generateMetadata({ params }: Params): Promise<Metadata> { const { id } = await params; return { title: getPfad(id)?.titel ?? "Lernpfad" }; }

export default async function PfadPage({ params }: Params) {
  const { id } = await params;
  const p = getPfad(id);
  if (!p) notFound();
  const steps = p.schritte.map((s) => ({ id: s.id, titel: titleOf(s.id), typ: typOf(s.id) ?? "begriff", kurz: plainText(getEntry(s.id)?.kurz ?? ""), warum: s.warum }));
  return (
    <main className="wrap">
      <article className="entry">
        <div className="eyebrow"><Link href="/pfad" className="tag" style={{ background: "var(--crust)", textDecoration: "none" }}>Lernpfad</Link><span className="mono">{p.schritte.length} Schritte · {p.dauer}</span></div>
        <h1>{p.titel}</h1>
        <p className="kurz">{p.kurz}</p>
        <p className="syn">{p.fuer}</p>
        <PathSteps pfad={p.id} steps={steps} />
      </article>
    </main>
  );
}
