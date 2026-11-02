import type { Metadata } from "next";
import { PfadeView } from "@/components/views/PfadViews";
export const metadata: Metadata = { title: "Learning paths", description: "Understand cooking step by step: short learning paths with a quiz at the end.", alternates: { canonical: "/en/pfad", languages: { de: "/pfad", en: "/en/pfad" } } };
export default function Page() { return <PfadeView lang="en" />; }
