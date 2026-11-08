// Die Ordnung der Seite für Besucher: vier Fragen statt elf Eintragstypen, plus Welten (Lebensmittel).
// Die Typen bleiben intern und erscheinen nur als kleines Etikett.
export type GroupKey = "probleme" | "ziele" | "verstehen" | "ausprobieren";

export const GROUPS: { key: GroupKey; types: string[]; color: string }[] = [
  { key: "probleme", types: ["symptom"], color: "symptom" },
  { key: "ziele", types: ["ziel"], color: "ziel" },
  { key: "verstehen", types: ["prozess", "technik", "zutat", "stellschraube", "begriff"], color: "prozess" },
  { key: "ausprobieren", types: ["gericht", "experiment", "labor"], color: "gericht" },
];
export const groupOfType = (typ: string): GroupKey | undefined => GROUPS.find((g) => g.types.includes(typ))?.key;

/** Vorgänge nach Themen (für „Verstehen“). */
export const THEMES: [string, string, string, string[]][] = [
  ["hitze", "Hitze und Bräunung", "Heat and browning", ["maillard-reaktion", "karamellisierung", "basen-braeunung", "pyrolyse", "waermeleitung", "waermestrahlung", "konvektion", "verdampfen", "leidenfrost", "siedepunkt-druck", "rauchpunkt", "pochieren-proz", "dampflockerung"]],
  ["wasser", "Wasser, Salz und Zucker", "Water, salt and sugar", ["osmose", "diffusion", "wasserbindung-salz", "poekeln", "wasseraktivitaet", "zucker-feuchtigkeit", "reduktion", "zucker-kristallisation", "eiskristalle", "gefrierpunkt-senkung"]],
  ["eiweiss", "Eiweiß", "Protein", ["eiweiss-denaturierung", "eiweiss-gerinnung", "saeure-denaturierung", "kollagen-gelatine", "gelbildung-gelatine", "glutenbildung", "schaumbildung", "fleischreifung", "enzym-zartmachen", "proteolyse"]],
  ["staerke", "Stärke und Pflanzen", "Starch and plants", ["staerkeverkleisterung", "retrogradation", "amylase", "pektin-abbau", "kalzium-pektin", "gelbildung-pektin", "chlorophyll-farbe", "anthocyan-farbe", "enzym-braeunung"]],
  ["fett", "Fett und Aroma", "Fat and aroma", ["emulsion", "fett-ausbraten", "fett-kristallisation", "oxidation-fett", "aroma-loeslichkeit", "aroma-blooming"]],
  ["gaerung", "Gärung und Lockerung", "Fermentation and raising", ["hefegaerung", "milchsaeuregaerung", "chemische-lockerung", "keimwachstum", "garum", "koji", "edelschimmel"]],
];
export const THEME_PIC: Record<string, string> = { hitze: "cat-prozess", wasser: "salz", eiweiss: "eiweiss", staerke: "staerke", fett: "oel", gaerung: "hefe", geschmack: "gewuerze" };

/** Einstiegsbeispiele auf der Startseite. */
export const DOORS = [
  { typ: "symptom", group: "probleme" as GroupKey, ids: ["steak-grau", "sauce-zu-duenn", "mayo-gerinnt", "kuchen-sinkt-ein"] },
  { typ: "ziel", group: "ziele" as GroupKey, ids: ["knusprig", "saftig", "luftig", "cremig"] },
  { typ: "prozess", group: "verstehen" as GroupKey, ids: ["maillard-reaktion", "emulsion", "glutenbildung", "staerkeverkleisterung"] },
];

/** Geschmack und Wahrnehmung: eigener Bereich auf „Verstehen“, quer über die Typen (Vorgänge, Techniken, Experimente). */
export const WAHRNEHMUNG: [string, string, string[]][] = [
  ["Was wir schmecken", "What we taste", ["umami", "salz-geschmack", "saeure", "suess", "bitter", "schaerfe", "geschmack-balance"]],
  ["Wie wir wahrnehmen", "How we perceive", ["aroma-nase", "mundgefuehl", "temperatur-geschmack", "kontraste", "augen-ohren", "flavor-pairing"]],
  ["Abschmecken", "Seasoning", ["abschmecken", "abschmecken-saeure", "essen-flach", "mehr-geschmack", "essen-versalzen", "zu-scharf"]],
  ["Selbst ausprobieren", "Try it yourself", ["x-nase-zu", "x-salz-bitter", "x-farbe-taeuscht", "x-temperatur-cola"]],
];
export const WAHRNEHMUNG_PFAD = "schmecken-lernen";
export const PRINZIPIEN_PFAD = "grundprinzipien";
