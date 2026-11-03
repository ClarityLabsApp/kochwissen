import type { Metadata } from "next";
import { ImpressumView } from "@/components/views/LegalView";
export const metadata: Metadata = { title: "Legal notice", alternates: { canonical: "/en/impressum", languages: { de: "/impressum", en: "/en/impressum" } } };
export default function Page() { return <ImpressumView lang="en" />; }
