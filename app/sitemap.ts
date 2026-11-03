import type { MetadataRoute } from "next";
import { allIds, isTranslated, lernpfade } from "@/lib/content";

import { SITE_URL } from "@/lib/site";
const site = SITE_URL;

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: `${site}/`, priority: 1 },
    { url: `${site}/pfad`, priority: 0.8 },
    ...lernpfade().map((p) => ({ url: `${site}/pfad/${p.id}`, priority: 0.7 })),
    ...allIds().map((id) => ({ url: `${site}/eintrag/${id}`, priority: 0.6, ...(isTranslated(id) ? { alternates: { languages: { en: `${site}/en/eintrag/${id}` } } } : {}) })),
    { url: `${site}/impressum`, priority: 0.1 },
    { url: `${site}/datenschutz`, priority: 0.1 },
    { url: `${site}/en`, priority: 0.9 },
    { url: `${site}/en/pfad`, priority: 0.7 },
    ...lernpfade("en").map((p) => ({ url: `${site}/en/pfad/${p.id}`, priority: 0.6 })),
    ...allIds().filter(isTranslated).map((id) => ({ url: `${site}/en/eintrag/${id}`, priority: 0.5 })),
  ];
}
