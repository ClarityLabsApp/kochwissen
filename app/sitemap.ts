import type { MetadataRoute } from "next";
import { allIds, isTranslated, lernpfade } from "@/lib/content";
import { SITE_URL } from "@/lib/site";

const site = SITE_URL;
const lastModified = new Date();

/** Eintrag mit Sprachvarianten (hreflang) in beide Richtungen. */
function pair(path: string, priority: number, en = true): MetadataRoute.Sitemap {
  const de = `${site}${path === "/" ? "/" : path}`;
  const enUrl = `${site}/en${path === "/" ? "" : path}`;
  const alternates = en ? { languages: { de, en: enUrl, "x-default": de } } : undefined;
  return [
    { url: de, lastModified, priority, alternates },
    ...(en ? [{ url: enUrl, lastModified, priority: Math.max(0.1, priority - 0.1), alternates }] : []),
  ];
}

export default function sitemap(): MetadataRoute.Sitemap {
  const enPaths = new Set(lernpfade("en").map((p) => p.id));
  return [
    ...pair("/", 1),
    ...pair("/pfad", 0.8),
    ...lernpfade().flatMap((p) => pair(`/pfad/${p.id}`, 0.7, enPaths.has(p.id))),
    ...allIds().flatMap((id) => pair(`/eintrag/${id}`, 0.6, isTranslated(id))),
    ...pair("/impressum", 0.1),
    ...pair("/datenschutz", 0.1),
  ];
}
