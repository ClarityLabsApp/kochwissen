import type { Metadata } from "next";
import { AzView } from "@/components/views/HubView";

export const metadata: Metadata = { title: "Alle Einträge", alternates: { canonical: "/alle", languages: { de: "/alle", en: "/en/alle", "x-default": "/alle" } } };
export default function Page() { return <AzView lang="de" />; }
