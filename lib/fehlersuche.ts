// Fehlersuche: Probleme nach dem, was man gerade kocht. Eimer = Gruppen von Welten, plus feste Zusätze.
export const BUCKETS: { id: string; name: [string, string]; pic: string; welten: string[]; extra?: string[] }[] = [
  { id: "saucen", name: ["Sauce", "Sauce"], pic: "w-saucen", welten: ["w-saucen"] },
  { id: "fleisch", name: ["Fleisch & Geflügel", "Meat & poultry"], pic: "w-fleisch", welten: ["w-fleisch", "w-gefluegel"], extra: ["frittiertes-fettig"] },
  { id: "fisch", name: ["Fisch & Meeresfrüchte", "Fish & seafood"], pic: "w-fisch", welten: ["w-fisch"] },
  { id: "gemuese", name: ["Gemüse & Kartoffeln", "Vegetables & potatoes"], pic: "w-gemuese", welten: ["w-gemuese", "w-kartoffeln", "w-pilze", "w-huelsenfruechte", "w-frittieren"] },
  { id: "eier", name: ["Eier & Milch", "Eggs & dairy"], pic: "w-eier", welten: ["w-eier", "w-milch"] },
  { id: "pasta", name: ["Pasta & Reis", "Pasta & rice"], pic: "w-pasta", welten: ["w-pasta", "w-getreide"] },
  { id: "kuchen", name: ["Kuchen & Guetzli", "Cakes & cookies"], pic: "w-gebaeck", welten: ["w-gebaeck"] },
  { id: "brot", name: ["Brot & Teig", "Bread & dough"], pic: "w-brot", welten: ["w-brot"] },
  { id: "suesses", name: ["Desserts & Schokolade", "Desserts & chocolate"], pic: "w-suesses", welten: ["w-suesses", "w-obst"] },
  { id: "geschmack", name: ["Es schmeckt nicht", "It doesn't taste right"], pic: "w-kraeuter-gewuerze", welten: ["w-kraeuter-gewuerze", "w-kaffee"],
    extra: ["essen-flach", "essen-versalzen", "zu-scharf", "tomatensauce-sauer", "knoblauch-bitter", "sauce-wein"] },
];
