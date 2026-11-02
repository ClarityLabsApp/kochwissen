import type { Metadata } from "next";
import EntryView, { entryMetadata } from "@/components/views/EntryView";
import { allIds } from "@/lib/content";

type Params = { params: Promise<{ id: string }> };
export function generateStaticParams() { return allIds().map((id) => ({ id })); }
export async function generateMetadata({ params }: Params): Promise<Metadata> { return entryMetadata((await params).id, "de"); }
export default async function Page({ params }: Params) { return <EntryView id={(await params).id} lang="de" />; }
