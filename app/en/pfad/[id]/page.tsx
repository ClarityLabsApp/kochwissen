import type { Metadata } from "next";
import { PfadView } from "@/components/views/PfadViews";
import { getPfad, lernpfade } from "@/lib/content";

type Params = { params: Promise<{ id: string }> };
export function generateStaticParams() { return lernpfade().map((p) => ({ id: p.id })); }
export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const { id } = await params; const p = getPfad(id, "en");
  return { title: p ? `${p.titel} · Learning path` : "Learning path", description: p?.kurz, alternates: { canonical: "/en/pfad/" + id, languages: { de: `/pfad/${id}`, en: `/en/pfad/${id}`, "x-default": `/pfad/${id}` } } };
}
export default async function Page({ params }: Params) { return <PfadView id={(await params).id} lang="en" />; }
