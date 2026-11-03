import type { Metadata } from "next";
import { PfadeView } from "@/components/views/PfadViews";
export const metadata: Metadata = { title: "Lernpfade", description: "Kochen Schritt für Schritt verstehen: kurze Lernpfade mit Quiz am Ende.", alternates: { canonical: "/pfad", languages: { de: "/pfad", en: "/en/pfad", "x-default": "/pfad" } } };
export default function Page() { return <PfadeView lang="de" />; }
