// Daten für die „Wein-Waage“: kein Naturgesetz, sondern die Regeln der Weinbegleitung, die eine
// nachvollziehbare Begründung haben (Gerbstoff ↔ Eiweiß/Fett, Säure ↔ Fett, Süße ↔ Süße, Salz, Alkohol ↔ Schärfe, Kraft ↔ Kraft).
// Werte 0–3 sind grobe Richtwerte für typische Vertreter.

type T2 = [string, string]; // [deutsch, englisch]

export interface Wine { id: string; name: T2; bsp: T2; saeure: number; tannin: number; suesse: number; alkohol: number; koerper: number }
export interface Dish { id: string; name: T2; fett: number; eiweiss: number; suesse: number; schaerfe: number; salz: number; saeure: number; kraft: number; fisch?: boolean }

export const WINES: Wine[] = [
  { id: "rot-kraeftig", name: ["Kräftiger Rotwein", "Bold red"], bsp: ["z. B. Cabernet, Syrah", "e.g. Cabernet, Syrah"], saeure: 2, tannin: 3, suesse: 0, alkohol: 3, koerper: 3 },
  { id: "rot-leicht", name: ["Leichter Rotwein", "Light red"], bsp: ["z. B. Pinot noir, Gamay", "e.g. Pinot noir, Gamay"], saeure: 2, tannin: 1, suesse: 0, alkohol: 1, koerper: 1 },
  { id: "weiss-frisch", name: ["Frischer Weißwein", "Crisp white"], bsp: ["z. B. Chasselas, Sauvignon blanc", "e.g. Chasselas, Sauvignon blanc"], saeure: 3, tannin: 0, suesse: 0, alkohol: 1, koerper: 1 },
  { id: "weiss-voll", name: ["Voller Weißwein", "Full-bodied white"], bsp: ["z. B. Chardonnay aus dem Holz", "e.g. oaked Chardonnay"], saeure: 1, tannin: 0, suesse: 0, alkohol: 2, koerper: 3 },
  { id: "schaum", name: ["Schaumwein", "Sparkling"], bsp: ["z. B. Prosecco, Champagner", "e.g. Prosecco, Champagne"], saeure: 3, tannin: 0, suesse: 1, alkohol: 1, koerper: 1 },
  { id: "suess", name: ["Süßer Dessertwein", "Sweet dessert wine"], bsp: ["z. B. Sauternes, Beerenauslese", "e.g. Sauternes, late harvest"], saeure: 2, tannin: 0, suesse: 3, alkohol: 2, koerper: 3 },
];

export const DISHES: Dish[] = [
  { id: "steak", name: ["Steak vom Grill", "Grilled steak"], fett: 2, eiweiss: 3, suesse: 0, schaerfe: 0, salz: 2, saeure: 0, kraft: 3 },
  { id: "lachs", name: ["Lachs mit Zitrone", "Salmon with lemon"], fett: 2, eiweiss: 2, suesse: 0, schaerfe: 0, salz: 1, saeure: 1, kraft: 2, fisch: true },
  { id: "rahm", name: ["Geschnetzeltes mit Rahmsauce", "Veal in cream sauce"], fett: 3, eiweiss: 2, suesse: 0, schaerfe: 0, salz: 1, saeure: 0, kraft: 2 },
  { id: "kaese", name: ["Käseplatte mit Blauschimmel", "Cheese board with blue cheese"], fett: 3, eiweiss: 2, suesse: 0, schaerfe: 0, salz: 3, saeure: 1, kraft: 3 },
  { id: "salat", name: ["Salat mit Vinaigrette", "Salad with vinaigrette"], fett: 1, eiweiss: 0, suesse: 0, schaerfe: 0, salz: 1, saeure: 3, kraft: 1 },
  { id: "curry", name: ["Scharfes Curry", "Hot curry"], fett: 1, eiweiss: 1, suesse: 1, schaerfe: 3, salz: 1, saeure: 0, kraft: 2 },
  { id: "dessert", name: ["Schokoladenkuchen", "Chocolate cake"], fett: 2, eiweiss: 0, suesse: 3, schaerfe: 0, salz: 0, saeure: 0, kraft: 2 },
];

export type Verdict = "gut" | "neutral" | "schlecht";
export interface Rule { id: string; left: T2; right: T2; v: Verdict; text: T2; weight: number }

/** Wertet die sechs Regeln für ein Paar aus. */
export function judge(w: Wine, d: Dish): Rule[] {
  const R: Rule[] = [];
  const add = (id: string, left: T2, right: T2, v: Verdict, text: T2, weight = 1) => R.push({ id, left, right, v, text, weight });

  const L1: T2 = ["Gerbstoffe", "Tannins"], R1: T2 = ["Eiweiß & Fett", "Protein & fat"];
  if (w.tannin >= 2) {
    if (d.fisch) add("tannin", L1, R1, "schlecht", ["Gerbstoffe und Fischöl schmecken zusammen metallisch.", "Tannins and fish oil taste metallic together."], 2);
    else if (d.eiweiss + d.fett >= 4) add("tannin", L1, R1, "gut", ["Gerbstoffe binden sich an Eiweiß und Fett: Der Wein wird weicher, das Essen wirkt leichter.", "Tannins bind to protein and fat: the wine softens and the food feels lighter."]);
    else add("tannin", L1, R1, "schlecht", ["Ohne Eiweiß und Fett bleiben die Gerbstoffe pelzig im Mund.", "Without protein and fat the tannins stay furry in the mouth."]);
  } else add("tannin", L1, R1, "neutral", ["Kaum Gerbstoffe: Hier spielt diese Regel keine Rolle.", "Hardly any tannins: this rule doesn't matter here."]);

  const L2: T2 = ["Säure", "Acidity"], R2: T2 = ["Fett & Säure", "Fat & acidity"];
  if (d.saeure > w.saeure) add("saeure", L2, R2, "schlecht", ["Das Essen ist saurer als der Wein: Er wirkt flach und dünn.", "The food is more acidic than the wine: it tastes flat and thin."]);
  else if (w.saeure >= 2 && d.fett >= 2) add("saeure", L2, R2, "gut", ["Die Säure schneidet durch das Fett und macht jeden Bissen leichter.", "The acidity cuts through the fat and makes every bite lighter."]);
  else if (d.fett >= 2 && w.saeure <= 1) add("saeure", L2, R2, "schlecht", ["Zu wenig Säure für so viel Fett: Beides wirkt schwer.", "Too little acidity for so much fat: both feel heavy."]);
  else add("saeure", L2, R2, "neutral", ["Säure und Fett halten sich die Waage.", "Acidity and fat are in balance."]);

  const L3: T2 = ["Süße", "Sweetness"], R3: T2 = ["Süße", "Sweetness"];
  if (d.suesse > w.suesse) add("suesse", L3, R3, "schlecht", ["Das Essen ist süßer als der Wein: Er schmeckt plötzlich sauer und bitter.", "The food is sweeter than the wine: it suddenly tastes sour and bitter."], 2);
  else if (d.suesse >= 2) add("suesse", L3, R3, "gut", ["Der Wein ist mindestens so süß wie das Essen: Beides bleibt rund.", "The wine is at least as sweet as the food: both stay rounded."]);
  else if (w.suesse >= 2 && d.salz >= 3) add("suesse", L3, R3, "gut", ["Süße und Salz ergänzen sich, wie bei Blauschimmelkäse mit Süßwein.", "Sweet and salt complement each other, as with blue cheese and sweet wine."]);
  else if (w.suesse >= 2) add("suesse", L3, R3, "schlecht", ["Süßer Wein zu herzhaftem Essen wirkt pappig.", "Sweet wine with savoury food tastes cloying."]);
  else add("suesse", L3, R3, "neutral", ["Weder Wein noch Essen sind süß.", "Neither wine nor food is sweet."]);

  const L4: T2 = ["Wein", "Wine"], R4: T2 = ["Salz", "Salt"];
  if (d.salz >= 2) add("salz", L4, R4, "gut", ["Salz macht Wein runder und weniger bitter.", "Salt makes wine rounder and less bitter."]);
  else add("salz", L4, R4, "neutral", ["Wenig Salz: kaum Einfluss.", "Little salt: hardly any effect."]);

  const L5: T2 = ["Alkohol", "Alcohol"], R5: T2 = ["Schärfe", "Chilli heat"];
  if (d.schaerfe >= 2) {
    if (w.alkohol >= 2) add("schaerfe", L5, R5, "schlecht", ["Alkohol verstärkt das Brennen von Chili.", "Alcohol intensifies the burn of chilli."]);
    else add("schaerfe", L5, R5, "gut", ["Leichter, frischer Wein kühlt, etwas Süße dämpft die Schärfe.", "A light, fresh wine cools, a touch of sweetness tames the heat."]);
  } else add("schaerfe", L5, R5, "neutral", ["Kaum Schärfe: Diese Regel spielt keine Rolle.", "Hardly any heat: this rule doesn't matter."]);

  const L6: T2 = ["Körper", "Body"], R6: T2 = ["Kraft", "Intensity"];
  const diff = w.koerper - d.kraft;
  if (Math.abs(diff) <= 1) add("kraft", L6, R6, "gut", ["Wein und Essen sind ähnlich kräftig, keiner überdeckt den anderen.", "Wine and food are similarly intense; neither drowns the other."]);
  else if (diff < 0) add("kraft", L6, R6, "schlecht", ["Der Wein geht neben dem kräftigen Essen unter.", "The wine gets lost next to the intense food."]);
  else add("kraft", L6, R6, "schlecht", ["Der Wein erdrückt das zarte Essen.", "The wine overwhelms the delicate food."]);
  return R;
}

export function overall(rules: Rule[]): "passt" | "geht" | "beisst" {
  const bad = rules.filter((r) => r.v === "schlecht").reduce((a, r) => a + r.weight, 0);
  const good = rules.filter((r) => r.v === "gut").length;
  if (bad >= 2) return "beisst";
  if (bad === 0 && good >= 2) return "passt";
  return "geht";
}

/** Alkohol, der beim Kochen im Gericht bleibt (USDA Nutrient Retention Factors, Release 6). */
export const ALKOHOL_REST: [T2, number][] = [
  [["Zugegeben, sofort vom Herd", "Added, taken straight off the heat"], 85],
  [["Flambiert", "Flambéed"], 75],
  [["15 Minuten geköchelt", "Simmered 15 minutes"], 40],
  [["30 Minuten", "30 minutes"], 35],
  [["1 Stunde", "1 hour"], 25],
  [["2 Stunden", "2 hours"], 10],
  [["2,5 Stunden", "2.5 hours"], 5],
];
