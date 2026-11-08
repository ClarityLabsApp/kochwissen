import type { Metadata } from "next";
import MerkView from "@/components/views/MerkView";

export const metadata: Metadata = { title: "Saved entries", robots: { index: false }, alternates: { canonical: "/en/merkliste", languages: { de: "/merkliste", en: "/en/merkliste" } } };
export default function Page() { return <MerkView lang="en" />; }
