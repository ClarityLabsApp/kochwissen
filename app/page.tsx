import HomeView from "@/components/views/HomeView";
export const metadata = { title: { absolute: "Garum · Verstehen, warum Kochen funktioniert" }, alternates: { canonical: "/", languages: { de: "/", en: "/en", "x-default": "/" } } };
import { SITE_URL, OWNER, INSTAGRAM_URL } from "@/lib/site";
const LD = { "@context": "https://schema.org", "@graph": [
  { "@type": "WebSite", "@id": SITE_URL + "/#site", name: "Garum", alternateName: "garum.guide", url: SITE_URL + "/", inLanguage: ["de-CH", "en-GB"], description: "Verstehen, warum Kochen und Backen funktionieren: einfach erklärt und sichtbar gemacht.", publisher: { "@id": SITE_URL + "/#org" } },
  { "@type": "Organization", "@id": SITE_URL + "/#org", name: "Garum", url: SITE_URL + "/", logo: SITE_URL + "/icon-512.png", sameAs: [INSTAGRAM_URL], founder: { "@type": "Person", name: OWNER.name } },
] };
export default function Home() { return <><script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(LD) }} /><HomeView lang="de" /></>; }
