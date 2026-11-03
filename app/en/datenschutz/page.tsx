import type { Metadata } from "next";
import { DatenschutzView } from "@/components/views/LegalView";
export const metadata: Metadata = { title: "Privacy", alternates: { canonical: "/en/datenschutz", languages: { de: "/datenschutz", en: "/en/datenschutz" } } };
export default function Page() { return <DatenschutzView lang="en" />; }
