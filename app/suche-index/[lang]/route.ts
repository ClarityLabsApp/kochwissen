import { searchExtras } from "@/lib/content";

export const dynamic = "force-static";
export function generateStaticParams() { return [{ lang: "de" }, { lang: "en" }]; }

/** Zusätzliche Suchwörter, als statische JSON-Datei gebaut und erst beim ersten Tippen geladen. */
export async function GET(_: Request, { params }: { params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  return Response.json(searchExtras(lang === "en" ? "en" : "de"));
}
