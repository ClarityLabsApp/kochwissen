import type { Metadata } from "next";
import { PfadeView } from "@/components/views/PfadViews";
export const metadata: Metadata = { title: "Lernpfade", alternates: { languages: { de: "/pfad", en: "/en/pfad" } } };
export default function Page() { return <PfadeView lang="de" />; }
