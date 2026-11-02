import type { Metadata } from "next";
import HomeView from "@/components/views/HomeView";
export const metadata: Metadata = {
  title: { absolute: "Garum · Understand why cooking works" },
  description: "Understand why cooking and baking work: simply explained and made visible.",
  alternates: { canonical: "/en", languages: { de: "/", en: "/en" } },
  openGraph: { locale: "en_GB" },
};
export default function Home() { return <HomeView lang="en" />; }
