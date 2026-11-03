/** Öffentliche Adresse der Seite. Lokal und in Vorschauen die jeweilige URL, in Produktion garum.guide. */
export const SITE_NAME = "Garum";
export const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL ??
  (process.env.VERCEL_ENV === "production" ? "https://garum.guide"
    : process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "http://localhost:3000");

/** Kontakt für Impressum und Datenschutz (Weiterleitung, im Domain-Anbieter eingerichtet). */
export const CONTACT_EMAIL = "hallo@garum.guide";
export const OWNER = { name: "Philipp Sidler", place: "Luzern, Schweiz", placeEn: "Lucerne, Switzerland" };
