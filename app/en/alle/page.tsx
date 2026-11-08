import type { Metadata } from "next";
import { AzView } from "@/components/views/HubView";

export const metadata: Metadata = { title: "All entries", alternates: { canonical: "/en/alle", languages: { de: "/alle", en: "/en/alle", "x-default": "/alle" } } };
export default function Page() { return <AzView lang="en" />; }
