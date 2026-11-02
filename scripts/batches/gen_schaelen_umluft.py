"""Zwei Einträge aus Phils Fragen: Schälen oder nicht, Umluft oder Ober- und Unterhitze (DE + EN)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MC = {"titel": "Harold McGee: On Food and Cooking (2004)"}
DE = [
 {"id": "schaelen", "typ": "technik", "titel": "Schälen oder nicht", "schwierigkeit": "einsteiger",
  "synonyme": ["Karotten schälen", "Kartoffeln mit Schale", "Apfel schälen", "Schale mitessen", "Nährstoffe in der Schale"],
  "kurz": "Viele Pflanzenstoffe sitzen in und direkt unter der Schale, darum schält man nur, wenn sie zäh, bitter, schmutzig oder grün ist.",
  "bild_im_kopf": "Wie die Rinde eines Baums: Sie schützt die Pflanze, darum sammelt sie dort ihre Abwehrstoffe.",
  "was_passiert": "Die Schale ist die Schutzschicht der Pflanze. In ihr und direkt darunter sammeln sich Farb- und Abwehrstoffe (Polyphenole) sowie Ballaststoffe. Bei Karotten steckt ein großer Teil der Polyphenole in der äußeren Schicht, obwohl sie nur wenig vom Gewicht ausmacht. Vitamine und Carotin verteilen sich dagegen über die ganze Rübe. Beim Kochen wandern wasserlösliche Vitamine (C und B) ins Wasser, Carotin kaum, denn es löst sich in Fett.",
  "warum_wichtig": "Wer bürstet statt schält, behält mehr Pflanzenstoffe und Ballaststoffe. Wer ganz kocht und erst danach schält, verliert weniger ans Kochwasser, denn die Schale hält alles zusammen. Rückstände von Pflanzenschutzmitteln sitzen vor allem außen: Waschen und Bürsten entfernt einen Teil, Schälen mehr.",
  "schritte": [
   "Junge Karotten, neue Kartoffeln, Äpfel und Gurken nur gründlich waschen und mit einer Bürste abreiben.",
   "Grüne Stellen und Keime bei Kartoffeln immer großzügig wegschneiden: Dort sitzt das giftige Solanin.",
   "Alte, dicke oder bittere Schalen dünn mit dem Sparschäler abziehen.",
   "Für Salat oder Püree Kartoffeln und Karotten ganz kochen und erst danach schälen.",
   "Gemüsekochwasser für Suppe oder Sauce weiterverwenden: Darin stecken die ausgelaugten Vitamine."
  ],
  "faustregeln": [
   "Für mehr Nährstoffe: bürsten statt schälen, wo die Schale zart ist.",
   "Wenn du schälst, dann dünn: Ein Sparschäler nimmt weniger weg als ein Messer.",
   "Ganz kochen, danach schälen: Die Schale hält Geschmack und Vitamine im Gemüse.",
   "Grüne Kartoffelschale immer weg, auch wenn du sonst mit Schale isst."
  ],
  "mythos": {"behauptung": "Die meisten Vitamine stecken in der Schale.", "richtig": "Nur zum Teil. In der Schale sitzen vor allem Pflanzenstoffe und Ballaststoffe, die meisten Vitamine verteilen sich über das ganze Fruchtfleisch."},
  "links": ["w-gemuese", "w-kartoffeln", "fond", "blanchieren", "enzym-braeunung", "pektin-abbau"],
  "welten": ["w-gemuese", "w-kartoffeln"],
  "visual": {"vorlage": "ablauf", "illustration": "three carrots on a wooden board, one scrubbed with a brush, one thinly peeled with a vegetable peeler, peel curls beside them"},
  "quellen": [dict(MC, stelle="Kapitel Gemüse und Früchte"),
   {"titel": "Zhang, Hamauzu (2004): Phenolic compounds and their antioxidant properties in different tissues of carrots. Journal of Food, Agriculture & Environment 2(1)"},
   {"titel": "Newcastle University (2009): Studie zu ganz gekochten Karotten (Brandt et al.)"}],
  "status": "entwurf"},
 {"id": "umluft-ober-unterhitze", "typ": "technik", "titel": "Umluft oder Ober- und Unterhitze", "schwierigkeit": "einsteiger",
  "synonyme": ["Umluft", "Heißluft", "Ober- und Unterhitze", "Backofen Einstellung", "welche Ofenstufe"],
  "kurz": "Umluft bläst heiße Luft über das Essen und gart schneller und trockener, Ober- und Unterhitze heizt sanfter und feuchter.",
  "bild_im_kopf": "Wie Pusten auf heiße Suppe: Bewegte Luft tauscht Wärme viel schneller aus als stille. Im Ofen bringt sie die Hitze schneller ans Essen.",
  "was_passiert": "Bei Ober- und Unterhitze heizen zwei Heizstäbe oben und unten. Die Luft steht fast still, um das Essen bildet sich eine Hülle aus kühlerer, feuchter Luft. Bei Umluft bläst ein Ventilator die heiße Luft ständig darüber und reißt diese Hülle weg. Darum kommt mehr Wärme an, und die Oberfläche trocknet schneller (Konvektion).",
  "warum_wichtig": "Schnell und trocken heißt: knusprig und braun. Sanft und feucht heißt: Teige können aufgehen, bevor sich eine feste Kruste bildet.",
  "faustregeln": [
   "Umluft: etwa 20 °C weniger als im Rezept für Ober- und Unterhitze (Richtwert).",
   "Mehrere Bleche gleichzeitig: Umluft, sonst backt jedes Blech anders.",
   "Rührkuchen, Biskuit, Soufflé und Käsekuchen: Ober- und Unterhitze. Umluft bildet zu früh eine Kruste, der Kuchen reißt oder wölbt sich.",
   "Für einen knusprigen Boden bei Pizza oder Wähe: unten im Ofen backen, Unterhitze betonen.",
   "Zum Überbacken am Schluss: Oberhitze oder Grill."
  ],
  "links": ["konvektion", "waermestrahlung", "knusprig", "luftfeuchte-ofen", "boden-durchgeweicht", "w-gebaeck", "w-brot"],
  "welten": ["w-gebaeck", "w-brot", "w-gemuese"],
  "visual": {"vorlage": "skala", "params": {
   "links": "Ober- und Unterhitze: sanft und feucht. Für Kuchen, Biskuit, Soufflé, Käsekuchen und Brot in den ersten Minuten.",
   "rechts": "Umluft: schnell und trocken. Für Ofengemüse, Pommes, knusprige Geflügelhaut und mehrere Bleche gleichzeitig."},
   "illustration": "an old enamel kitchen oven with its door open, a sponge cake on the lower rack and a tray of roast vegetables on the upper rack"},
  "quellen": [dict(MC, stelle="Kapitel Garmethoden: Ofen und Wärmeübertragung"),
   {"titel": "Serious Eats: Convection vs. conventional ovens"}],
  "status": "entwurf"},
]
EN = {
 "schaelen": {"titel": "To peel or not to peel", "synonyme": ["peeling carrots", "potatoes with skin", "peeling apples", "eating the skin", "nutrients in the peel"],
  "kurz": "Many plant compounds sit in and just under the skin, so peel only when it is tough, bitter, dirty or green.",
  "bild_im_kopf": "Like the bark of a tree: it protects the plant, so that is where it stores its defences.",
  "was_passiert": "The skin is the plant's protective layer. In it and just beneath it, colour and defence compounds (polyphenols) and fibre collect. In carrots a large share of the polyphenols sits in the outer layer, even though it makes up little of the weight. Vitamins and carotene, by contrast, are spread through the whole root. When boiling, water-soluble vitamins (C and B) move into the water; carotene hardly does, because it dissolves in fat.",
  "warum_wichtig": "Scrubbing instead of peeling keeps more plant compounds and fibre. Boiling whole and peeling afterwards loses less to the cooking water, because the skin holds everything together. Pesticide residues sit mainly on the outside: washing and scrubbing remove some, peeling more.",
  "schritte": ["Young carrots, new potatoes, apples and cucumbers: just wash them well and scrub with a brush.",
   "Always cut away green patches and sprouts on potatoes generously: that is where the toxic solanine sits.",
   "Peel old, thick or bitter skins thinly with a vegetable peeler.",
   "For salad or mash, boil potatoes and carrots whole and peel them afterwards.",
   "Reuse vegetable cooking water for soup or sauce: it holds the vitamins that leached out."],
  "faustregeln": ["For more nutrients: scrub instead of peeling where the skin is tender.",
   "If you peel, peel thinly: a vegetable peeler takes off less than a knife.",
   "Boil whole, peel afterwards: the skin keeps flavour and vitamins in the vegetable.",
   "Always remove green potato skin, even if you usually eat the skin."],
  "mythos": {"behauptung": "Most of the vitamins are in the skin.", "richtig": "Only partly. The skin holds mainly plant compounds and fibre; most vitamins are spread through the whole flesh."},
  "visual": {"illustration": "three carrots on a wooden board, one scrubbed with a brush, one thinly peeled with a vegetable peeler, peel curls beside them"},
  "quellen": [{"titel": "Harold McGee: On Food and Cooking (2004)", "stelle": "Chapter on vegetables and fruits"},
   {"titel": "Zhang, Hamauzu (2004): Phenolic compounds and their antioxidant properties in different tissues of carrots. Journal of Food, Agriculture & Environment 2(1)"},
   {"titel": "Newcastle University (2009): study on carrots cooked whole (Brandt et al.)"}]},
 "umluft-ober-unterhitze": {"titel": "Fan oven or conventional heat", "synonyme": ["fan oven", "convection", "top and bottom heat", "conventional oven", "which oven setting"],
  "kurz": "A fan oven blows hot air over the food and cooks faster and drier; top and bottom heat is gentler and moister.",
  "bild_im_kopf": "Like blowing on hot soup: moving air exchanges heat much faster than still air. In the oven it brings the heat to the food faster.",
  "was_passiert": "With top and bottom heat, two elements heat from above and below. The air is almost still, and a layer of cooler, moist air forms around the food. With the fan, hot air is blown over it constantly and strips this layer away. So more heat arrives, and the surface dries faster (convection).",
  "warum_wichtig": "Fast and dry means crisp and brown. Gentle and moist means doughs can rise before a firm crust forms.",
  "faustregeln": ["Fan oven: about 20 °C lower than a recipe written for conventional heat (as a guide).",
   "Several trays at once: use the fan, otherwise each tray bakes differently.",
   "Butter cakes, sponge, soufflé and cheesecake: conventional heat. The fan forms a crust too early, so the cake cracks or domes.",
   "For a crisp base on pizza or a tart: bake low in the oven and favour bottom heat.",
   "For browning a gratin at the end: top heat or the grill."],
  "visual": {"params": {"links": "Conventional heat: gentle and moist. For cakes, sponge, soufflé, cheesecake and bread in the first minutes.",
   "rechts": "Fan oven: fast and dry. For roast vegetables, chips, crisp poultry skin and several trays at once."},
   "illustration": "an old enamel kitchen oven with its door open, a sponge cake on the lower rack and a tray of roast vegetables on the upper rack"},
  "quellen": [{"titel": "Harold McGee: On Food and Cooking (2004)", "stelle": "Chapter on cooking methods: the oven and heat transfer"},
   {"titel": "Serious Eats: Convection vs. conventional ovens"}]},
}
for e in DE:
    json.dump(e, open(f"{ROOT}/content/entries/{e['id']}.json", "w"), ensure_ascii=False, indent=2)
ml = json.load(open(f"{ROOT}/content/master-list.json"))
have = {m["id"] for m in ml["eintraege"]}
for e in DE:
    if e["id"] not in have:
        ml["eintraege"].append({"id": e["id"], "typ": e["typ"], "titel": e["titel"], "status": "entwurf", "pilot": False, "links": e["links"], "welten": e["welten"], "synonyme": e["synonyme"], "visual": {"vorlage": e["visual"]["vorlage"]}, "verlinkt_von": []})
ml["anzahl"] = len(ml["eintraege"])
json.dump(ml, open(f"{ROOT}/content/master-list.json", "w"), ensure_ascii=False, indent=2)
print("ok")
