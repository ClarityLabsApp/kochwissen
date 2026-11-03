import type { Metadata } from "next";
import HomeView from "@/components/views/HomeView";
export const metadata: Metadata = {
  title: { absolute: "Garum · Understand why cooking works" },
  description: "Understand why cooking and baking work: simply explained and made visible.",
  alternates: { canonical: "/en", languages: { de: "/", en: "/en", "x-default": "/" } },
  openGraph: { locale: "en_GB", images: [{ url: "/og-en.png", width: 1200, height: 630, alt: "Garum · Understand why cooking works" }] },
  twitter: { card: "summary_large_image", images: ["/og-en.png"] },
};
export default function Home() { return <HomeView lang="en" />; }
