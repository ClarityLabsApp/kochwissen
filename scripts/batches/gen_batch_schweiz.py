"""Batch 13: Schweizer Gerichte. Dazu Bildmotive (visual.illustration) für Gerichte, Experimente und Labor-Rezepte."""
import json, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "content/entries")
QM = {"titel": "Harold McGee: On Food and Cooking (2004)"}
E = []
def gericht(id, titel, syn, kurz, bild, momente, links, welten, illu, schw="einsteiger"):
    E.append(dict(id=id, typ="gericht", titel=titel, synonyme=syn, kurz=kurz, bild_im_kopf=bild, schwierigkeit=schw, status="entwurf",
        schluesselmomente=[{"schritt": s, "warum": w, **({"prinzip": p} if p else {})} for s, w, p in momente],
        links=links, welten=welten, quellen=[QM], visual={"vorlage": "ablauf", "illustration": illu}))

gericht("g-aelplermagronen", "Älplermagronen", ["Älplermakkaroni", "Alpler Magronen", "Magronen"],
  "Älplermagronen werden cremig, weil Pasta und Kartoffeln im selben Wasser kochen und ihre Stärke die Sauce bindet.",
  "Wie ein Eintopf, der sich selbst die Sauce kocht: Was die Zutaten abgeben, hält am Ende alles zusammen.",
  [("Kartoffelwürfel und Hörnli im selben Topf kochen", "Beide geben Stärke ins Wasser. Ein Rest dieses Wassers bindet später Rahm und Käse.", "staerkeverkleisterung"),
   ("Zwiebelringe langsam in Butter goldbraun braten", "Langsam karamellisiert der Zucker der Zwiebel, schnell verbrennt sie außen.", "karamellisierung"),
   ("Abgießen, etwas Kochwasser behalten, mit Rahm und geriebenem Käse mischen", "Stärke aus dem Kochwasser hält Käsefett und Rahm zusammen, die Sauce bleibt cremig statt fettig.", "emulsion"),
   ("Mit Apfelmus servieren", "Die Säure des Apfels schneidet durch Fett und Käse und macht das schwere Gericht frischer.", "abschmecken-saeure")],
  ["staerkeverkleisterung", "emulsion", "kaese", "zwiebeln-verbrennen", "abschmecken-saeure", "g-kaesefondue"], ["w-pasta", "w-kartoffeln", "w-milch"],
  "a rustic Swiss dish of macaroni and potato cubes with melted cheese and golden fried onion rings in a cast iron pan, a small bowl of applesauce beside it")

gericht("g-zuercher-geschnetzeltes", "Zürcher Geschnetzeltes", ["Züri Gschnätzlets", "Geschnetzeltes", "Kalbsgeschnetzeltes"],
  "Zürcher Geschnetzeltes gelingt, wenn das Fleisch nur kurz scharf angebraten wird und erst ganz am Schluss zurück in die Sauce kommt.",
  "Wie ein Gast, der erst zum Dessert erscheint: Kommt das Fleisch zu früh in die Sauce, wird es zäh.",
  [("Fleisch trocken tupfen und portionsweise in sehr heißer Pfanne anbraten", "Zu viel Fleisch auf einmal kühlt die Pfanne, es kocht im eigenen Saft und wird grau.", "steak-grau"),
   ("Fleisch herausnehmen, Zwiebeln und Pilze im Bratsatz dünsten", "Die braunen Röststoffe am Pfannenboden sind die Grundlage der Sauce.", "maillard-reaktion"),
   ("Mit Weißwein ablöschen und einkochen, dann Rahm dazu", "Wein löst den Bratsatz, Einkochen konzentriert den Geschmack.", "deglacieren"),
   ("Sauce sämig einkochen, Fleisch nur noch kurz darin erwärmen", "Dünne Fleischstreifen sind schnell durch. Kochen sie in der Sauce, ziehen sich die Fasern zusammen und werden trocken.", "eiweiss-denaturierung")],
  ["steak-grau", "anbraten", "deglacieren", "reduktion", "eiweiss-denaturierung", "g-roesti"], ["w-fleisch", "w-saucen"],
  "Zurich-style sliced veal in a creamy mushroom sauce on a white plate with a golden rösti beside it")

gericht("g-birchermueesli", "Birchermüesli", ["Bircher Müsli", "Birchermüsli", "Overnight Oats"],
  "Im Birchermüesli quellen Haferflocken über Nacht in Milch oder Joghurt. Zitrone hält den geriebenen Apfel hell.",
  "Wie ein Schwamm, den man abends ins Wasser legt: Am Morgen ist er weich und voll.",
  [("Haferflocken mit Milch oder Joghurt mischen und über Nacht kühl stellen", "Die Flocken nehmen Flüssigkeit auf, ihre Stärke quillt auch kalt etwas: Das Müesli wird cremig.", "staerkeverkleisterung"),
   ("Apfel kurz vor dem Essen reiben und sofort mit Zitronensaft mischen", "An der Luft bräunt ein Enzym den Apfel. Säure bremst es.", "enzym-braeunung"),
   ("Nüsse erst am Schluss darüber streuen", "So bleiben sie knackig, statt Feuchtigkeit aufzusaugen.", None)],
  ["enzym-braeunung", "x-apfel-braun", "staerkeverkleisterung", "joghurt"], ["w-getreide", "w-milch"],
  "a glass bowl of Bircher muesli with grated apple, oats, yogurt, hazelnuts and a few berries on top")

gericht("g-raclette", "Raclette", ["Raclette", "Raclettekäse", "Gschwellti mit Käse"],
  "Raclette ist geschmolzener Käse auf Kartoffeln. Er wird cremig, wenn er gerade schmilzt, und fettig, wenn er zu heiß wird.",
  "Wie Schokolade in der Hand: Ein wenig Wärme macht sie weich, zu viel lässt sie auseinanderlaufen.",
  [("Kartoffeln in der Schale kochen (Gschwellti)", "Die Schale schützt: Die Kartoffel saugt kein Wasser auf und bleibt mehlig-fest.", "staerkeverkleisterung"),
   ("Käse nur so lange erhitzen, bis er Blasen wirft", "Erst schmilzt das Fett, dann wird das Eiweiß weich. Zu lange gehitzt ziehen sich die Eiweiße zusammen und pressen Fett heraus.", "eiweiss-gerinnung"),
   ("Mit sauren Gurken und Silberzwiebeln essen", "Säure hilft gegen das Gefühl der Schwere und macht jeden Bissen wieder frisch.", "abschmecken-saeure")],
  ["kaese", "eiweiss-gerinnung", "sauce-trennt-sich", "g-kaesefondue", "abschmecken-saeure"], ["w-milch", "w-kartoffeln"],
  "a wedge of raclette cheese melting onto boiled potatoes in their skins, with small pickles and pearl onions on a wooden board")

gericht("g-gerstensuppe", "Bündner Gerstensuppe", ["Gerstensuppe", "Bündner Suppe", "Graupensuppe"],
  "Bündner Gerstensuppe wird sämig, weil die Gerste beim langen Köcheln Stärke abgibt. Speck und Trockenfleisch bringen die Tiefe.",
  "Wie ein Feuer, das langsam Glut wird: Erst nach Stunden ist die volle Wärme da.",
  [("Speck und Gemüsewürfel in wenig Fett andünsten", "Das Fett aus dem Speck trägt die Aromen ins ganze Gericht.", "aroma-loeslichkeit"),
   ("Gerste dazugeben, mit Wasser oder Brühe auffüllen, 1–2 Stunden leise köcheln", "Die Gerstenkörner geben nach und nach Stärke ab und binden die Suppe.", "staerkeverkleisterung"),
   ("Bündnerfleisch oder Rauchfleisch mitkochen", "Gereiftes, getrocknetes Fleisch bringt viel Umami in die Brühe.", "umami"),
   ("Zum Schluss mit Rahm verfeinern und abschmecken", "Fett rundet ab. Erst am Ende salzen, weil die Suppe beim Kochen einkocht.", "reduktion")],
  ["staerkeverkleisterung", "umami", "aroma-loeslichkeit", "reduktion", "w-getreide"], ["w-getreide", "w-fleisch"],
  "a rustic bowl of creamy Swiss barley soup with vegetables and diced cured meat, a slice of dark bread beside it")

gericht("g-fotzelschnitten", "Fotzelschnitten", ["Fotzelschnitte", "Arme Ritter", "French Toast", "Pain perdu"],
  "Fotzelschnitten sind altbackenes Brot, getränkt in Eiermilch und goldbraun gebraten. Gerade weil das Brot alt ist, funktioniert es.",
  "Wie ein trockener Schwamm: Nur wer durstig ist, saugt sich richtig voll.",
  [("Altbackenes Brot oder Zopf in Scheiben schneiden", "Altes Brot ist fester, weil die Stärke sich neu geordnet hat. Es saugt Eiermilch auf, ohne zu zerfallen.", "retrogradation"),
   ("In Eiermilch mit etwas Zucker tränken", "Die Flüssigkeit zieht bis in die Mitte. Das Ei wird beim Braten fest und hält alles zusammen.", "eiweiss-gerinnung"),
   ("Bei mittlerer Hitze in Butter goldbraun braten", "Zucker, Ei und Milch bräunen schnell. Mittlere Hitze gibt dem Innern Zeit zu stocken.", "maillard-reaktion"),
   ("Mit Zimtzucker bestreuen", "Zimt und Zucker kleben an der warmen Butter.", None)],
  ["retrogradation", "brot-altbacken", "eiweiss-gerinnung", "maillard-reaktion", "g-zopf"], ["w-brot", "w-eier"],
  "golden fried slices of Swiss braided bread dusted with cinnamon sugar on a plate, with a small bowl of apple compote")

for e in E:
    p = os.path.join(OUT, e["id"] + ".json"); json.dump(e, open(p, "w"), ensure_ascii=False, indent=2); open(p, "a").write("\n")

# Bildmotive für bestehende Gerichte, Experimente, Labor-Rezepte
ILLU = {
  "g-roesti": "a golden crispy Swiss rösti in a cast iron pan, one wedge cut out",
  "g-wiener-schnitzel": "a large golden breaded Wiener schnitzel with a puffy wavy crust and a lemon wedge on a plate",
  "g-risotto": "a creamy saffron risotto in a shallow bowl with grated parmesan and a wooden spoon",
  "g-mayonnaise": "a glass bowl of thick homemade mayonnaise with a whisk, an egg yolk and a small bottle of oil beside it",
  "g-steak": "a seared steak with a deep brown crust resting on a board, sliced to show pink inside, with thyme and garlic",
  "g-pommes": "golden french fries in a paper cone with a small dish of salt",
  "g-hollandaise": "a small copper saucepan of glossy yellow hollandaise sauce with asparagus spears beside it",
  "g-creme-brulee": "a crème brûlée in a white ramekin with a caramelized cracked sugar top and a spoon",
  "g-pizza": "a Neapolitan-style pizza with a puffy charred crust, tomato, mozzarella and basil on a wooden peel",
  "g-zopf": "a shiny golden Swiss braided butter bread (Zopf) on a linen cloth",
  "g-kaesefondue": "a Swiss cheese fondue pot (caquelon) with melted cheese, a fork with a bread cube dipped in",
  "g-pancakes": "a stack of fluffy pancakes with butter and maple syrup dripping down",
  "g-meringue": "white crisp meringues with swirled peaks on a plate",
  "g-ofengemuese": "roasted vegetables on a baking sheet: carrots, squash, red onions, nicely browned",
  "g-konfituere": "jars of homemade strawberry and apricot jam with a spoon and fresh fruit",
  "x-rotkohl-indikator": "three glasses with red cabbage juice in pink, purple and blue-green colors, a red cabbage beside them",
  "x-backpulver-kalt-heiss": "two glasses of water, one with a few bubbles and one fizzing strongly, a small tin of baking powder",
  "x-eischnee-fett": "two bowls of beaten egg whites, one with stiff glossy peaks, one runny, a whisk between them",
  "x-tanzender-tropfen": "water droplets dancing as small beads on a hot steel pan",
  "x-kartoffelwasser": "a glass of cloudy water with a white starch layer at the bottom next to raw potato sticks",
  "x-apfel-braun": "three apple slices on plates, one browned, one with lemon juice, one in water",
  "x-butter-schuetteln": "a screw-top jar with a lump of fresh yellow butter and buttermilk",
  "x-gluten-auswaschen": "a stretchy ball of gluten being pulled apart by two hands above a bowl of milky water",
  "x-hefe-ballon": "a small bottle with foaming yeast and a red balloon inflated on top",
  "x-salz-gurke": "cucumber slices on a plate with salt and beads of water on them",
  "x-zuckerkristalle": "a glass jar with sugar crystals growing on a wooden skewer",
  "x-bohnen-gruen": "three small heaps of green beans in different shades: bright green, dull green, olive",
  "x-glace-beutel": "a zip bag with ice cubes and salt holding a smaller bag of vanilla ice cream, a pair of mittens beside",
  "x-ananas-gelatine": "three glasses of orange jelly, one liquid with fresh pineapple pieces, two set firm",
  "l-backpulver": "a small glass jar of homemade baking powder with a spoon, baking soda and cream of tartar beside",
  "l-butter": "a fresh block of homemade butter on parchment with a jug of buttermilk",
  "l-bratbutter": "a glass jar of golden clarified butter (ghee) with a small saucepan",
  "l-frischkaese": "a cheesecloth bundle of fresh paneer cheese pressed into a block, a lemon and a jug of milk",
  "l-joghurt": "glass jars of homemade natural yogurt with a spoon",
  "l-sauerteig": "a glass jar of bubbly active sourdough starter with a loose lid, a bag of flour behind",
  "l-creme-fraiche": "a small jar of thick crème fraîche with a spoon standing in it",
  "l-gebackenes-natron": "a baking tray with white baked soda powder and a few unbaked pretzels",
  "l-mascarpone": "a bowl of thick smooth mascarpone with a spatula, cocoa and ladyfingers beside",
  "l-vanilleextrakt": "a dark glass bottle of homemade vanilla extract with vanilla pods inside",
  "l-puderzucker": "a small heap of powdered sugar and a sieve, next to granulated sugar",
  "l-buttermilch-ersatz": "a measuring jug of milk with a lemon half beside it",
  "l-senf": "a small jar of homemade grainy mustard with yellow and brown mustard seeds",
  "l-sauerkraut": "a glass fermentation jar packed with shredded cabbage under brine, a weight on top",
  "l-brauner-zucker": "a bowl of soft brown sugar next to a small jar of dark molasses",
  "l-dulce-de-leche": "a jar of thick caramel-brown dulce de leche with a spoon",
  "l-apfelpektin": "a pot of simmering apple peels and cores and a jar of amber pectin liquid",
  "l-labneh": "a bowl of thick labneh drizzled with olive oil and za'atar, flatbread beside it",
}
miss = []
for id, motif in ILLU.items():
    p = os.path.join(OUT, id + ".json")
    if not os.path.exists(p): miss.append(id); continue
    e = json.load(open(p)); e.setdefault("visual", {"vorlage": "keine"})["illustration"] = motif
    json.dump(e, open(p, "w"), ensure_ascii=False, indent=2); open(p, "a").write("\n")
if miss: print("fehlt:", miss)

BACK = {"kaese": ["g-raclette", "g-aelplermagronen"], "g-kaesefondue": ["g-raclette", "g-aelplermagronen"], "steak-grau": ["g-zuercher-geschnetzeltes"],
        "deglacieren": ["g-zuercher-geschnetzeltes"], "enzym-braeunung": ["g-birchermueesli"], "x-apfel-braun": ["g-birchermueesli"],
        "retrogradation": ["g-fotzelschnitten"], "brot-altbacken": ["g-fotzelschnitten"], "g-zopf": ["g-fotzelschnitten"], "umami": ["g-gerstensuppe"],
        "w-getreide": ["g-gerstensuppe", "g-birchermueesli"], "w-pasta": ["g-aelplermagronen"], "g-roesti": ["g-zuercher-geschnetzeltes"]}
for id, ls in BACK.items():
    p = os.path.join(OUT, id + ".json")
    if not os.path.exists(p): print("fehlt", id); continue
    e = json.load(open(p))
    for l in ls:
        if l not in e.setdefault("links", []): e["links"].append(l)
    json.dump(e, open(p, "w"), ensure_ascii=False, indent=2); open(p, "a").write("\n")

mp = os.path.join(ROOT, "content/master-list.json"); M = json.load(open(mp)); by = {m["id"]: m for m in M["eintraege"]}
for e in E:
    if e["id"] not in by: M["eintraege"].append({"id": e["id"], "typ": "gericht", "titel": e["titel"], "status": "geplant", "pilot": False, "links": e["links"], "welten": e["welten"], "synonyme": e["synonyme"], "verlinkt_von": [], "visual": {"vorlage": "ablauf"}})
by = {m["id"]: m for m in M["eintraege"]}
for id, ls in BACK.items():
    if id in by:
        for l in ls:
            if l not in by[id]["links"]: by[id]["links"].append(l)
back = {i: set() for i in by}
for m in M["eintraege"]:
    for l in m["links"]:
        if l in back: back[l].add(m["id"])
for m in M["eintraege"]: m["verlinkt_von"] = sorted(back[m["id"]] - set(m["links"]))
M["anzahl"] = len(M["eintraege"]); json.dump(M, open(mp, "w"), ensure_ascii=False, indent=1)
print(len(E), "Gerichte,", len(ILLU) + len(E), "Bildmotive,", M["anzahl"], "in der Masterliste")
