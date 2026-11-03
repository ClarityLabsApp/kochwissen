import type { Metadata } from "next";
import { ImpressumView } from "@/components/views/LegalView";
export const metadata: Metadata = { title: "Impressum", alternates: { canonical: "/impressum", languages: { de: "/impressum", en: "/en/impressum" } } };
export default function Page() { return <ImpressumView lang="de" />; }
