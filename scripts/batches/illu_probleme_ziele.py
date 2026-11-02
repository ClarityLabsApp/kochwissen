"""Bildbeschreibungen (Aquarell) für Probleme und Ziele. Setzt visual.illustration; Bilder erzeugt `npm run illustrationen`."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = {
 # Probleme: das misslungene Ergebnis, gut erkennbar
 "boden-durchgeweicht": "a slice of fruit tart lifted from the tin, its pastry base pale, soggy and damp underneath",
 "bohnen-nicht-weich": "a spoon holding hard, wrinkled chickpeas and beans above a pot, clearly still firm",
 "bratkartoffeln-kleben": "pan-fried potato slices torn and stuck to the bottom of a steel pan, a spatula scraping them",
 "brot-altbacken": "the dry, crumbly end of a stale loaf with a hard cut face and scattered crumbs",
 "brot-flach": "a flat, spread-out round loaf of bread that has run wide on a baking tray, barely risen",
 "brot-kruste-weich": "a crusty loaf whose crust has gone soft and wrinkled, slightly sagging",
 "brot-zu-dicht": "a sliced loaf showing a dense, heavy, tight crumb with almost no holes",
 "creme-klumpig": "a bowl of vanilla custard with visible lumps on a whisk",
 "eischnee-nicht-steif": "a copper bowl of runny, foamy egg whites that will not hold a peak, dripping off a whisk",
 "essen-flach": "a plain bowl of pale vegetable soup next to an untouched lemon half and salt cellar",
 "essen-versalzen": "a pot of stew with a salt shaker lying tipped over beside it, salt spilled on the table",
 "fisch-klebt": "a fish fillet with its skin torn and stuck to a pan, flakes left behind on the metal",
 "fisch-zerfaellt": "a cooked fish fillet broken into flakes on a spatula, falling apart",
 "fleisch-trocken": "a slice of overcooked grey pork roast, dry and fibrous, on a plate",
 "fleisch-zaeh": "a tough piece of stewed beef being pulled with a fork, stringy and resisting",
 "frittiertes-fettig": "limp, greasy fries on paper with dark oil stains soaking through",
 "gefrierbrand": "a frozen piece of meat with grey-white dry patches and ice crystals in an open freezer bag",
 "gemuese-grau": "a bowl of overcooked olive-grey green beans and broccoli, dull and drab",
 "gemuese-matschig": "mushy, collapsed cooked carrots and vegetables slumped in a bowl",
 "glace-koernig": "a scoop of ice cream with a coarse, icy, grainy texture and visible ice crystals",
 "hollandaise-flockt": "a small saucepan of broken hollandaise sauce, split into curds and butter",
 "karamell-kristallisiert": "a saucepan of grainy, cloudy crystallised sugar instead of clear caramel",
 "kekse-breit": "thin cookies spread flat and merged together on a baking tray",
 "knoblauch-bitter": "dark brown, burnt garlic slices in a small pan with a wisp of smoke",
 "kuchen-klitschig": "a cut slice of cake with a dense, wet, sticky streak at the bottom",
 "kuchen-sinkt-ein": "a round sponge cake with a deep sunken crater in the middle",
 "kuchen-trocken": "a crumbly dry slice of cake falling apart into crumbs on a plate",
 "marinade-matschig": "a piece of chicken breast with a pale, mushy, frayed surface after a long acidic marinade, lemon halves beside it",
 "mayo-gerinnt": "a bowl of split mayonnaise, oily and curdled, with a whisk",
 "muerbeteig-zaeh": "a hard, shrunken tart shell with a tough, cracked edge",
 "muffins-tunnel": "a muffin cut in half showing long tunnel-shaped holes in the crumb",
 "panade-faellt-ab": "a breaded schnitzel with its golden crumb coating peeling off in one sheet",
 "pasta-klebt": "a clump of spaghetti stuck together in a single tangled mass on a fork",
 "pfannkuchen-gummig": "a pale, rubbery pancake bending stiffly over a fork",
 "reis-matschig": "a bowl of sticky, mushy, overcooked rice clumped together",
 "ruehrei-waessrig": "scrambled eggs on a plate with a puddle of watery liquid around them",
 "saft-beim-schneiden": "a just-cut steak on a board with a large pool of red juice running out",
 "sahne-wird-butter": "over-whipped cream turned grainy and yellow with butter clumps and liquid in a bowl",
 "sauce-klumpig": "a white sauce with flour lumps clinging to a wooden spoon",
 "sauce-trennt-sich": "a pan sauce with pools of separated fat floating on top",
 "sauce-zu-duenn": "a thin, watery sauce running off a spoon like water",
 "schokolade-grau": "a chocolate bar with grey-white streaks and a dusty bloom on its surface",
 "schokolade-klumpt": "melted chocolate seized into a thick, dull, grainy lump in a bowl over water",
 "steak-grau": "a grey, pale steak sitting in its own juices in a crowded pan, no crust",
 "teig-klebt": "sticky bread dough clinging to hands and a wooden board in strings",
 "teig-schnurrt": "a rolled-out sheet of dough shrinking back from the rolling pin, edges pulling in",
 "wedges-nicht-knusprig": "soft, pale, limp potato wedges on a baking tray, not browned",
 "zu-scharf": "a bowl of red chili stew with fresh chilies and a glass of milk beside it",
 "zwiebeln-verbrennen": "onion rings charred black at the edges in a frying pan, some still raw",
 # Ziele: das gelungene Ergebnis
 "cremig": "a spoon lifting silky, creamy risotto from a pan",
 "farbe": "bright green beans, deep golden roasted potatoes and ruby red cabbage side by side",
 "fluffig": "a stack of tall, fluffy pancakes with an airy cut edge",
 "gebunden": "a glossy sauce coating the back of a spoon, a finger line staying clear",
 "gleichmaessig-gar": "a sliced roast beef evenly pink from edge to edge with a thin brown crust",
 "grosse-poren": "a sliced sourdough loaf with a open, glossy crumb full of large irregular holes",
 "knackig": "bright green snap peas and blanched broccoli being snapped in half, crisp",
 "knusprig": "golden crisp fries and roast potatoes with crackling edges",
 "laenger-frisch": "a loaf of bread wrapped in a linen cloth next to a bread box",
 "laenger-haltbar": "jars of jam, pickles and dried fruit on a wooden shelf",
 "luftig": "a tall sponge cake slice with a light, airy crumb and a bowl of whipped cream",
 "mehr-geschmack": "a pan with browned fond being deglazed with wine, herbs and parmesan beside it",
 "muerbe": "crumbly shortbread biscuits, one broken to show the tender short texture",
 "saftig": "a juicy roast chicken breast sliced, glistening, on a board",
 "zart": "a tender braised beef cheek pulling apart under a fork",
}
n = 0
for id, prompt in P.items():
    if not prompt: continue
    path = f"{ROOT}/content/entries/{id}.json"
    if not os.path.exists(path): print("fehlt", id); continue
    e = json.load(open(path))
    v = e.setdefault("visual", {"vorlage": "keine"})
    if v.get("illustration") != prompt:
        v["illustration"] = prompt; n += 1
        json.dump(e, open(path, "w"), ensure_ascii=False, indent=2); open(path, "a").write("\n")
print(n, "Bildbeschreibungen gesetzt")
