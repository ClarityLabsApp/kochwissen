import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Garum · Verstehen, warum Kochen funktioniert",
    short_name: "Garum",
    description: "Verstehen, warum Kochen und Backen funktionieren: einfach erklärt und sichtbar gemacht.",
    start_url: "/",
    display: "standalone",
    background_color: "#efe4cf",
    theme_color: "#2b2118",
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
  };
}
