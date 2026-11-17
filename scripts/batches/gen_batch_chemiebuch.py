"""Abgleich mit „Chemistry of Cooking“ (Rodriguez-Velazquez, LibreTexts, 17. November 2026).
Neue Einträge für Lücken: Roggenmehl, Mehltypen, Milch erhitzen, Ei-Schwimmtest, Gelier- und Verdickungsmittel,
Glutenfrei backen, Zuckerersatz beim Backen. Dazu das Buch als ergänzende Quelle bei passenden Einträgen.
Texte als Paare L(deutsch, englisch)."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_batch_welten2 import L, res, MC, ROOT  # noqa: E402

BOOK = "https://chem.libretexts.org/Bookshelves/Biological_Chemistry/Chemistry_of_Cooking_(Rodriguez-Velazquez)/"


def CB(kapitel, pfad):
    return {"titel": f"Rodriguez-Velazquez: Chemistry of Cooking, {kapitel} (LibreTexts, CC BY-NC-SA 4.0)", "url": BOOK + pfad}


E = []
add = E.append


def Z(id, titel, syn, kurz, bild, rolle, was, warum, regeln, links, welten, illu, quellen, mythos=None, schw="einsteiger"):
    e = {"id": id, "typ": "zutat", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild,
         "rolle": [{"rolle": r, "prozess": p} for r, p in rolle], "was_passiert": was, "warum_wichtig": warum,
         "faustregeln": regeln, "links": links, "welten": welten, "visual": {"vorlage": "punktmatrix", "illustration": illu},
         "quellen": quellen, "status": "entwurf", "schwierigkeit": schw}
    if mythos:  # L((behauptung, claim), (richtig, truth))
        claim, truth = res(mythos, 0), res(mythos, 1)
        e["mythos"] = {"behauptung": L(*claim), "richtig": L(*truth)}
    return e


def T(id, titel, syn, kurz, bild, was, warum, schritte, regeln, links, welten, illu, quellen, mythos=None, schw="einsteiger"):
    e = {"id": id, "typ": "technik", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild, "was_passiert": was,
         "warum_wichtig": warum, "schritte": schritte, "faustregeln": regeln, "links": links, "welten": welten,
         "visual": {"vorlage": "ablauf", "illustration": illu}, "quellen": quellen, "status": "entwurf", "schwierigkeit": schw}
    if mythos:
        claim, truth = res(mythos, 0), res(mythos, 1)
        e["mythos"] = {"behauptung": L(*claim), "richtig": L(*truth)}
    return e


# ================================================================ Roggenmehl
add(Z("roggenmehl", L("Roggenmehl: Warum Roggenbrot Säure braucht", "Rye flour: why rye bread needs acid"),
      L(["Roggen", "Roggenbrot", "Roggenbrot klitschig", "Roggenteig klebt", "Roggensauerteig", "Pentosane"], ["rye", "rye bread", "gummy rye bread", "sticky rye dough", "rye sourdough", "pentosans"]),
      L("Roggenmehl bildet kaum ein tragfähiges Klebernetz. Sein Teig hält durch Schleimstoffe, die viel Wasser binden, und er braucht Säure, damit die Krume nicht klitschig wird.",
        "Rye flour forms hardly any usable gluten network. Its dough holds together through gums that bind a lot of water, and it needs acid so the crumb doesn't turn gummy."),
      L("Wie Kleister statt Gummiband: Er klebt und hält zusammen, aber er federt nicht.",
        "Like paste instead of a rubber band: it sticks and holds together, but it doesn't spring back."),
      [(L("bindet viel Wasser", "binds a lot of water"), "staerkeverkleisterung"), (L("bringt aktive Enzyme mit", "brings active enzymes"), "amylase"), (L("braucht Säure", "needs acid"), "sauerteig")],
      L("Roggen enthält Eiweiß, aber es bildet kein elastisches Netz wie beim Weizen. Dafür hat er viele Schleimstoffe (Pentosane), die ein Vielfaches ihres Gewichts an Wasser binden und den Teig klebrig machen. Roggenmehl bringt außerdem viele stärkeabbauende Enzyme (Amylasen) mit. Sie arbeiten im Ofen weiter, bis die Stärke fest wird, und können sie zu Zucker zerlegen. Säure aus dem Sauerteig bremst diese Enzyme.",
        "Rye contains protein, but it doesn't form an elastic network like wheat. Instead it has a lot of gums (pentosans) that bind many times their weight in water and make the dough sticky. Rye flour also brings plenty of starch-splitting enzymes (amylases). They keep working in the oven until the starch sets, and can break it down to sugar. Acid from sourdough slows these enzymes."),
      L("Wer Roggen wie Weizen behandelt, bekommt einen klebrigen Teig und ein Brot, das innen feucht und speckig bleibt. Mit Sauerteig, kurzem Kneten und Geduld nach dem Backen wird es saftig und schnittfest.",
        "Treat rye like wheat and you get a sticky dough and a loaf that stays damp and gummy inside. With sourdough, brief mixing and patience after baking it turns moist and sliceable."),
      L(["Für Brote mit viel Roggen: den Großteil des Roggens als Sauerteig ansetzen, weil die Säure die Enzyme bremst.",
         "Roggenteig nur kurz mischen statt lange kneten: Es gibt kein Klebernetz, das man aufbauen könnte.",
         "Mit nassen Händen oder einem Teigschaber arbeiten, nicht mit zusätzlichem Mehl.",
         "Roggenbrot nach dem Backen mindestens einen Tag ruhen lassen, weil sich die Krume erst beim Abkühlen festigt."],
        ["For breads with a lot of rye: make most of the rye into sourdough, because the acid slows the enzymes.",
         "Mix rye dough briefly rather than kneading for long: there is no gluten network to build.",
         "Work with wet hands or a dough scraper, not with extra flour.",
         "Let rye bread rest for at least a day after baking, because the crumb only firms up as it cools."]),
      ["mehl", "mehltyp", "glutenbildung", "sauerteig", "l-sauerteig", "amylase", "brot-zu-dicht", "staerkeverkleisterung"],
      ["w-brot", "w-getreide"],
      "a dark round rye loaf with a cracked floury crust next to a small sack of grey rye flour and a few rye ears",
      [CB("2.9 Rye Flour", "02%3A_Flour/2.09%3A_Rye_Flour"), {"titel": "The Fresh Loaf: Rye flour", "url": "https://www.thefreshloaf.com/handbook/rye-flour"},
       MC("Kapitel Brot: Roggen", "Chapter on bread: rye")],
      schw="fortgeschritten"))

# ================================================================ Mehltypen
add(Z("mehltyp", L("Mehltypen: Was die Zahl auf der Packung bedeutet", "Flour types: what the number on the packet means"),
      L(["Mehltype", "Type 405", "Type 550", "Type 1050", "Weissmehl", "Halbweissmehl", "Ruchmehl", "Vollkornmehl", "Ausmahlgrad", "Mehl Unterschied"],
        ["flour type", "type 405", "type 550", "German flour types", "Swiss flour", "Ruchmehl", "extraction rate", "wholemeal flour", "flour difference"]),
      L("Die Typenzahl misst, wie viele Mineralstoffe im Mehl stecken, also wie viel vom äußeren Korn mitgemahlen wurde. Je höher die Zahl, desto dunkler, kräftiger und durstiger ist das Mehl.",
        "The type number measures how much mineral matter is in the flour, so how much of the outer grain was milled in. The higher the number, the darker, more flavourful and thirstier the flour."),
      L("Wie beim Schälen eines Apfels: Je dicker man schält, desto heller bleibt, was übrig ist.",
        "Like peeling an apple: the thicker you peel, the paler what's left."),
      [(L("bestimmt die Wasseraufnahme", "decides water absorption"), "staerkeverkleisterung"), (L("Kleber für die Struktur", "gluten for structure"), "glutenbildung")],
      L("Das Innere des Korns ist fast reine Stärke mit Eiweiß und arm an Mineralstoffen. Die äußeren Schichten und die Schale sind reich an Mineralstoffen, Fasern und Aroma. Verbrennt man Mehl, bleibt Asche übrig: In Deutschland gibt die Typenzahl an, wie viele Milligramm Asche 100 g Mehl (in der Trockenmasse) hinterlassen. Type 405 enthält also rund 0,4 % Mineralstoffe. In der Schweiz heißen die Stufen Weissmehl, Halbweissmehl, Ruchmehl und Vollkornmehl.",
        "The inside of the grain is almost pure starch with protein and low in minerals. The outer layers and the bran are rich in minerals, fibre and flavour. Burn flour and ash remains: in Germany the type number states how many milligrams of ash 100 g of flour (in dry matter) leave behind. Type 405 therefore contains about 0.4 % minerals. In Switzerland the grades are called Weissmehl, Halbweissmehl, Ruchmehl and Vollkornmehl."),
      L("Dunkleres Mehl nimmt mehr Wasser auf, macht Teige kompakter und schmeckt kräftiger. Wer in einem Rezept die Mehlsorte wechselt, muss deshalb oft die Wassermenge anpassen.",
        "Darker flour absorbs more water, makes doughs denser and tastes stronger. If you swap the flour in a recipe, you often have to adjust the amount of water."),
      L(["Ungefähre Entsprechungen: Weissmehl ≈ Type 405 bis 550, Halbweissmehl ≈ Type 812, Ruchmehl ≈ Type 1050, Vollkornmehl = ganzes Korn.",
         "Für feine Kuchen und Guetzli: helles Mehl, weil es wenig Schale enthält und zart bleibt.",
         "Für Brot mit viel Geschmack: Halbweiss- oder Ruchmehl, mit etwas mehr Wasser als beim Weissmehl.",
         "Bei Vollkornmehl den Teig 20 bis 30 Minuten quellen lassen, damit die Schale Wasser aufnimmt."],
        ["Rough equivalents: Swiss Weissmehl ≈ German type 405 to 550, Halbweissmehl ≈ type 812, Ruchmehl ≈ type 1050, wholemeal = whole grain.",
         "For delicate cakes and biscuits: pale flour, because it contains little bran and stays tender.",
         "For bread with lots of flavour: half-white or Ruchmehl, with a little more water than for white flour.",
         "With wholemeal flour let the dough soak for 20 to 30 minutes so the bran can take up water."]),
      ["mehl", "roggenmehl", "glutenbildung", "brot-zu-dicht", "teig-klebt"],
      ["w-brot", "w-getreide", "w-gebaeck"],
      "four small heaps of flour in a row from bright white to speckled brown wholemeal, with a wheat ear",
      [CB("2.4 Flour Streams and Types of Wheat Flour", "02%3A_Flour/2.04%3A_Flour_Streams_and_Types_of_Wheat_Flour"),
       {"titel": "Cuisine Helvetica: Swiss flour types", "url": "https://cuisinehelvetica.com/swiss-flour-types/"},
       MC("Kapitel Getreide und Mehl", "Chapter on grains and flour")]))

# ================================================================ Milch erhitzen
add(T("milch-erhitzen", L("Pasteurisiert, UHT, Rohmilch: Was Hitze mit Milch macht", "Pasteurised, UHT, raw: what heat does to milk"),
      L(["pasteurisieren", "Pasteurisierung", "UHT-Milch", "H-Milch", "Rohmilch", "Rohmilch abkochen", "Milch homogenisiert", "Kochgeschmack Milch"],
        ["pasteurisation", "pasteurised milk", "UHT milk", "long-life milk", "raw milk", "boiling raw milk", "homogenised milk", "cooked taste milk"]),
      L("Milch wird erhitzt, um Krankheitserreger abzutöten. Je heißer, desto länger hält sie, aber umso mehr schmeckt sie gekocht.",
        "Milk is heated to kill pathogens. The hotter, the longer it keeps, but the more it tastes cooked."),
      L("Wie ein Thermostat für Haltbarkeit: Jeder Grad mehr kauft Zeit und kostet etwas Frische.",
        "Like a thermostat for shelf life: every extra degree buys time and costs a little freshness."),
      L("Beim Pasteurisieren wird Milch kurz auf 72 bis 75 °C erhitzt, für 15 bis 30 Sekunden. Das tötet Krankheitserreger, aber nicht alle Keime, darum gehört sie in den Kühlschrank. UHT-Milch wird für wenige Sekunden über 135 °C erhitzt und keimfrei abgefüllt: Sie hält ungeöffnet monatelang. Dabei reagieren Milchzucker und Eiweiß ein wenig miteinander, und Schwefelstoffe aus dem Eiweiß werden frei. Daher kommt der leichte Kochgeschmack.",
        "To pasteurise, milk is briefly heated to 72 to 75 °C for 15 to 30 seconds. That kills pathogens but not all bacteria, so it belongs in the fridge. UHT milk is heated above 135 °C for a few seconds and packed sterile: unopened it keeps for months. In the process, milk sugar and protein react a little with each other, and sulphur compounds are released from the protein. That is where the slight cooked taste comes from."),
      L("Für Joghurt, Frischkäse oder Käse zählt, wie die Milch behandelt wurde: Stark erhitztes Eiweiß gerinnt anders. Und Rohmilch vom Hof kann Krankheitserreger enthalten.",
        "For yoghurt, fresh cheese or cheese it matters how the milk was treated: strongly heated protein curdles differently. And raw milk from the farm can contain pathogens."),
      L(["Rohmilch vom Hof oder Milchautomaten vor dem Trinken aufkochen.",
         "Dabei ständig rühren und die Hitze mittel halten, damit nichts am Topfboden anbrennt.",
         "Abgekochte Milch rasch abkühlen und im Kühlschrank aufbewahren.",
         "Für selbst gemachten Joghurt pasteurisierte oder UHT-Milch nehmen, nicht rohe."],
        ["Bring raw milk from a farm or milk vending machine to the boil before drinking it.",
         "Stir constantly and keep the heat medium so nothing catches on the bottom of the pan.",
         "Cool boiled milk quickly and keep it in the fridge.",
         "For homemade yoghurt use pasteurised or UHT milk, not raw."]),
      L(["Für Rohmilch: vor dem Trinken aufkochen, weil sie Krankheitserreger enthalten kann.",
         "Für Frischkäse und Käse: keine UHT-Milch, weil ihr stark erhitztes Eiweiß nur weich und brüchig gerinnt.",
         "Homogenisiert heißt: Das Fett wurde in winzige Tröpfchen zerteilt, darum rahmt die Milch nicht mehr auf."],
        ["For raw milk: bring it to the boil before drinking, because it can contain pathogens.",
         "For fresh cheese and cheese: no UHT milk, because its strongly heated protein curdles only soft and crumbly.",
         "Homogenised means the fat has been broken into tiny droplets, so the cream no longer rises."]),
      ["milch", "kasein", "keimwachstum", "maillard-reaktion", "l-joghurt", "l-frischkaese", "emulsion"],
      ["w-milch"],
      "a glass milk bottle, a small saucepan of steaming milk and a carton of long-life milk side by side",
      [{"titel": "Verbraucherzentrale: Rund um die Milch", "url": "https://www.verbraucherzentrale.de/wissen/lebensmittel/lebensmittelproduktion/rund-um-die-milch-erzeugung-verarbeitung-und-angebote-12775"},
       CB("6.2 Milk", "06%3A_Dairy_Products/6.02%3A_Milk"), MC("Kapitel Milch und Milchprodukte", "Chapter on milk and dairy products")]))

# ================================================================ Ei-Schwimmtest
add({"id": "x-ei-schwimmtest", "typ": "experiment", "titel": L("Wie alt ist das Ei? Der Schwimmtest", "How old is the egg? The float test"),
     "synonyme": L(["Ei frisch testen", "Ei schwimmt", "Eier Frischetest", "Ei Wasserglas", "Luftkammer Ei"], ["egg freshness test", "egg floats", "egg float test", "egg in water glass", "egg air cell"]),
     "kurz": L("Ein frisches Ei liegt flach am Boden eines Wasserglases, ein älteres stellt sich auf, ein sehr altes schwimmt. Der Grund ist die Luftblase im Ei, die mit jedem Tag wächst.",
               "A fresh egg lies flat at the bottom of a glass of water, an older one stands up, a very old one floats. The reason is the air pocket in the egg, which grows every day."),
     "bild_im_kopf": L("Wie eine Schwimmweste, die sich langsam selbst aufbläst.", "Like a life jacket that slowly inflates itself."),
     "material": L(["ein hohes Glas mit kaltem Wasser", "Eier mit verschiedenem Datum, wenn vorhanden", "ein Löffel"],
                   ["a tall glass of cold water", "eggs with different dates, if you have them", "a spoon"]),
     "schritte": L(["Das Glas mit kaltem Wasser füllen.", "Ein Ei mit dem Löffel vorsichtig hineinlegen.", "Beobachten, wie es liegt: flach, schräg, aufrecht oder schwimmend.", "Mit den anderen Eiern wiederholen und das Datum auf der Packung vergleichen."],
                   ["Fill the glass with cold water.", "Gently lower an egg in with the spoon.", "Watch how it settles: flat, tilted, upright or floating.", "Repeat with the other eggs and compare the dates on the packs."]),
     "beobachtung": L("Ganz frische Eier liegen flach. Nach ein bis zwei Wochen hebt sich das stumpfe Ende, nach mehreren Wochen steht das Ei aufrecht oder treibt nach oben.",
                      "Very fresh eggs lie flat. After one or two weeks the blunt end lifts, after several weeks the egg stands upright or rises."),
     "erklaerung": L("Die Eierschale hat Tausende winzige Poren. Durch sie verdunstet Wasser, und Kohlendioxid entweicht aus dem Eiweiß. An ihrer Stelle dringt Luft ein und sammelt sich am stumpfen Ende in der Luftkammer. Je größer sie wird, desto mehr Auftrieb hat das Ei. Weil das Kohlendioxid entweicht, wird das Eiweiß mit der Zeit basischer und dünnflüssiger, darum lassen sich ältere Eier leichter schälen.",
                     "The eggshell has thousands of tiny pores. Water evaporates through them, and carbon dioxide escapes from the white. Air takes their place and collects in the air pocket at the blunt end. The bigger it gets, the more the egg floats. As the carbon dioxide escapes, the white becomes more alkaline and runnier over time, which is why older eggs are easier to peel."),
     "sicherheit": L("Der Test zeigt das Alter, nicht ob ein Ei verdorben ist. Ein Ei, das nach dem Aufschlagen auffällig riecht, gehört weg, egal wie es im Wasser lag.",
                     "The test shows age, not whether an egg has gone off. An egg that smells odd when cracked should be thrown away, however it behaved in the water."),
     "dauer": L("5 Minuten", "5 minutes"),
     "links": ["ei", "eier-schaelen", "eiweiss", "ph-wert"], "welten": ["w-eier"],
     "visual": {"vorlage": "ablauf", "illustration": "three tall glasses of water with eggs: one lying flat at the bottom, one standing upright, one floating near the top"},
     "quellen": [MC("Kapitel Eier: Qualität und Alter", "Chapter on eggs: quality and age"), CB("7.5 Storing Eggs", "07%3A_Eggs/7.05%3A_Storing_Eggs")],
     "status": "entwurf", "schwierigkeit": "einsteiger"})

# ================================================================ Gelier- und Verdickungsmittel
add(Z("geliermittel", L("Agar, Alginat, Carrageen: Gelieren ohne Gelatine", "Agar, alginate, carrageenan: setting without gelatine"),
      L(["Hydrokolloide", "Geliermittel vegan", "Agar-Agar", "Alginat", "Natriumalginat", "Carrageen", "Gellan", "Johannisbrotkernmehl", "Guarkernmehl", "Sphärifikation", "Molekularküche"],
        ["hydrocolloids", "vegan gelling agent", "agar", "alginate", "sodium alginate", "carrageenan", "gellan", "locust bean gum", "guar gum", "spherification", "molecular gastronomy"]),
      L("Viele Gelier- und Verdickungsmittel kommen aus Algen, Samen oder Bakterien. Es sind lange Zuckerketten, die Wasser einfangen, und jede hat eigene Regeln: Manche brauchen Hitze, manche Kalzium, manche vertragen keine Säure.",
        "Many gelling and thickening agents come from seaweed, seeds or bacteria. They are long sugar chains that trap water, and each has its own rules: some need heat, some need calcium, some can't take acid."),
      L("Wie verschiedene Schlüssel für dasselbe Schloss: Alle sperren Wasser ein, aber jeder dreht anders.",
        "Like different keys for the same lock: all of them lock water in, but each one turns differently."),
      [(L("bindet Wasser zu einem Gel", "binds water into a gel"), "gelbildung-gelatine"), (L("braucht Kalzium (Alginat)", "needs calcium (alginate)"), "kalzium-pektin")],
      L("Gelatine ist Eiweiß aus Kollagen und schmilzt schon bei Körpertemperatur. Agar aus Rotalgen muss kochen, wird um 40 °C fest und schmilzt erst wieder um 85 °C. Alginat aus Braunalgen geliert kalt, sobald es auf Kalzium trifft. Ein Tropfen in Kalziumwasser bekommt so eine dünne Haut (Sphärifikation). Carrageen gibt es in festen und weichen Sorten, Johannisbrot- und Guarkernmehl verdicken, ohne fest zu werden.",
        "Gelatine is protein from collagen and melts at body temperature. Agar from red seaweed has to boil, sets at around 40 °C and only melts again around 85 °C. Alginate from brown seaweed sets cold as soon as it meets calcium. A drop in calcium water gets a thin skin this way (spherification). Carrageenan comes in firm and soft types, while locust bean and guar gum thicken without setting."),
      L("Wer weiß, was ein Mittel braucht, kann Gelatine vegetarisch ersetzen oder warm servierbare Gelees machen. Und man versteht, warum ein Rezept mit Ananas oder Zitronensaft nicht fest wurde.",
        "Knowing what each agent needs lets you replace gelatine with a vegetarian option or make jellies you can serve warm. And you understand why a recipe with pineapple or lemon juice didn't set."),
      L(["Für warm servierte Gelees: Agar, weil es erst um 85 °C wieder schmilzt.",
         "Agar mindestens zwei Minuten sprudelnd kochen, sonst geliert es nicht.",
         "Für Sphärifikation: rund 0,5 % Alginat in der Flüssigkeit und ein Bad mit etwa 0,5 % Calciumchlorid, Richtwerte aus der Molekularküche.",
         "Sehr saure Flüssigkeiten gelieren mit Alginat schlecht, weil es unter einem pH-Wert von etwa 3,6 ausflockt.",
         "Mengen variieren je nach Produkt stark: Packungsangabe hat Vorrang."],
        ["For jellies served warm: agar, because it only melts again around 85 °C.",
         "Boil agar for at least two minutes, otherwise it won't set.",
         "For spherification: about 0.5 % alginate in the liquid and a bath of about 0.5 % calcium chloride, guide values from modernist cooking.",
         "Very acidic liquids set poorly with alginate, because it clumps below a pH of about 3.6.",
         "Amounts vary a lot between products: the packet instructions come first."]),
      ["gelbildung-gelatine", "gelatine", "agar-agar", "xanthan", "pektin", "kalzium-pektin", "ph-wert"],
      ["w-suesses"],
      "small glass bowls with a clear amber jelly cube, tiny orange spheres like caviar on a spoon, and a little dish of white powder",
      [CB("1.5 Gelatinization", "01%3A_Thickening_and_Concentrating_Flavors/1.05%3A_Gelatinization"),
       CB("1.7 Non-traditional thickeners", "01%3A_Thickening_and_Concentrating_Flavors/1.07%3A_Non-traditional_thickeners"),
       {"titel": "HarvardX Science & Cooking: Spherification how-to", "url": "https://courses.edx.org/asset-v1:HarvardX+SPU27x+2015_Q2+type@asset+block/Spherification_how-to.pdf"}],
      schw="fortgeschritten"))

# ================================================================ Glutenfrei backen
add(T("glutenfrei-backen", L("Glutenfrei backen: Was den Kleber ersetzt", "Gluten-free baking: what replaces gluten"),
      L(["glutenfrei", "glutenfreies Brot", "glutenfreies Mehl", "ohne Gluten backen", "Flohsamenschalen", "Xanthan backen", "glutenfreier Kuchen bröselt"],
        ["gluten-free", "gluten-free bread", "gluten-free flour", "baking without gluten", "psyllium husk", "xanthan baking", "gluten-free cake crumbles"]),
      L("Ohne Gluten fehlt dem Teig das dehnbare Netz, das Gas festhält und das Gebäck zusammenhält. Andere Stoffe übernehmen seine Aufgaben: Stärke gibt Gerüst, Bindemittel wie Xanthan oder Flohsamenschalen halten Wasser und Gas.",
        "Without gluten, the dough lacks the stretchy network that holds gas and keeps the bake together. Other ingredients take over its jobs: starch provides structure, binders like xanthan or psyllium husk hold water and gas."),
      L("Wie ein Zelt ohne Gestänge: Die Plane allein steht nicht, man braucht andere Stangen.",
        "Like a tent without poles: the canvas alone won't stand, you need other supports."),
      L("Weizenkleber macht drei Dinge: Er bindet, er ist dehnbar und er wird im Ofen fest. Glutenfreie Mehle wie Reis, Mais, Buchweizen oder Hirse liefern Stärke, aber kein Netz. Bindemittel wie Xanthan oder Flohsamenschalen bilden mit Wasser ein zähes Gel, das Gasbläschen umschließt. Eier helfen, weil ihr Eiweiß beim Backen fest wird. Darum sind glutenfreie Brotteige eher ein dicker Brei als ein Teig.",
        "Wheat gluten does three things: it binds, it stretches and it sets in the oven. Gluten-free flours such as rice, maize, buckwheat or millet supply starch but no network. Binders like xanthan or psyllium husk form a thick gel with water that surrounds gas bubbles. Eggs help because their protein sets during baking. That is why gluten-free bread doughs are more like a thick batter than a dough."),
      L("Wer Weizenmehl einfach 1:1 durch glutenfreies Mehl ersetzt, bekommt bröselige Kuchen und flache, feuchte Brote. Mit Mischung, Bindemittel und mehr Wasser gelingt es.",
        "Simply swapping wheat flour 1:1 for gluten-free flour gives crumbly cakes and flat, damp breads. With a blend, a binder and more water it works."),
      L(["Mehle mischen: ein Teil mit Geschmack und Eiweiß (Buchweizen, Hirse, Hafer glutenfrei) und ein Teil Stärke (Mais, Kartoffel, Reis).",
         "Ein Bindemittel zugeben, wenn die Mischung keines enthält: Xanthan oder Flohsamenschalen, in kleinen Mengen nach Packung.",
         "Für Brot deutlich mehr Wasser nehmen als bei Weizen: Der Teig soll weich und klebrig sein.",
         "Den Teig 15 bis 30 Minuten quellen lassen, bevor er geformt wird.",
         "Lange und gut durchbacken, Brot vollständig auskühlen lassen, bevor man es anschneidet."],
        ["Blend flours: some with flavour and protein (buckwheat, millet, gluten-free oats) and some starch (maize, potato, rice).",
         "Add a binder if the blend doesn't contain one: xanthan or psyllium husk, in small amounts as the packet says.",
         "For bread use clearly more water than with wheat: the dough should be soft and sticky.",
         "Let the dough soak for 15 to 30 minutes before shaping.",
         "Bake long and thoroughly, and let bread cool completely before cutting."]),
      L(["Für luftiges Brot: Flohsamenschalen, weil ihr Gel Gas besonders gut festhält.",
         "Für Kuchen und Muffins: Xanthan und Eier, weil sie binden, ohne zäh zu machen.",
         "Für Zöliakie zählt auch die Küche: eigene Bretter, Siebe und Backformen, und auf zertifiziert glutenfreie Produkte achten."],
        ["For airy bread: psyllium husk, because its gel holds gas especially well.",
         "For cakes and muffins: xanthan and eggs, because they bind without making things tough.",
         "For coeliac disease the kitchen matters too: separate boards, sieves and tins, and look for certified gluten-free products."]),
      ["glutenbildung", "mehl", "xanthan", "staerkeverkleisterung", "ei", "brot-zu-dicht", "mehltyp"],
      ["w-brot", "w-gebaeck", "w-getreide"],
      "a sliced gluten-free loaf with an open crumb beside small bowls of buckwheat flour, rice flour and psyllium husk",
      [{"titel": "America's Test Kitchen: Gluten-free binders and leaveners", "url": "https://americastestkitchen.com/guides/gluten-free/gluten-free-binders-and-leaveners"},
       CB("2.10 Other Grains and Flours", "02%3A_Flour/2.10%3A_Other_Grains_and_Flours"), MC("Kapitel Brot: Gluten", "Chapter on bread: gluten")],
      schw="fortgeschritten"))

# ================================================================ Zuckerersatz
add(Z("zuckerersatz", L("Zuckerersatz beim Backen", "Sugar substitutes in baking"),
      L(["Süßstoff", "Süßstoff backen", "Erythrit", "Xylit", "Stevia", "Sucralose", "Aspartam", "Zuckeralkohol", "zuckerfrei backen", "Birkenzucker"],
        ["sweetener", "baking with sweetener", "erythritol", "xylitol", "stevia", "sucralose", "aspartame", "sugar alcohol", "sugar-free baking", "birch sugar"]),
      L("Zucker süßt nicht nur, er gibt Gebäck auch Masse, Bräune, Feuchtigkeit und Zartheit. Süßstoffe ersetzen meist nur die Süße, darum klappt ein Tausch 1:1 selten.",
        "Sugar doesn't just sweeten, it also gives bakes bulk, browning, moisture and tenderness. Sweeteners usually replace only the sweetness, which is why a 1:1 swap rarely works."),
      L("Wie ein Schauspieler, der fünf Rollen spielt: Ein Ersatz übernimmt meist nur eine davon.",
        "Like an actor playing five parts: a stand-in usually covers only one of them."),
      [(L("gibt Masse und Zartheit", "gives bulk and tenderness"), "zucker-feuchtigkeit"), (L("bräunt", "browns"), "karamellisierung")],
      L("Zucker löst sich im Teig, bindet Wasser, stört die Bildung des Klebers und bräunt im Ofen. Intensive Süßstoffe wie Stevia oder Sucralose sind hundertfach süßer, man braucht nur Spuren und hat keine Masse. Aspartam verliert in der Hitze an Süße. Zuckeralkohole wie Erythrit und Xylit bringen Masse mit. Erythrit ist etwas weniger süß, kühlt im Mund und kann wieder auskristallisieren. Xylit süßt etwa wie Zucker, ist aber für Hunde giftig.",
        "Sugar dissolves in the dough, binds water, gets in the way of gluten forming and browns in the oven. Intense sweeteners like stevia or sucralose are hundreds of times sweeter, so you need only traces and get no bulk. Aspartame loses sweetness in the heat. Sugar alcohols such as erythritol and xylitol do bring bulk. Erythritol is a little less sweet, cools in the mouth and can recrystallise. Xylitol sweetens about as much as sugar but is poisonous to dogs."),
      L("Wer weiß, welche Rolle der Zucker im Rezept spielt, wählt den passenden Ersatz und rechnet damit, dass sich Farbe, Volumen und Biss ändern.",
        "Knowing what role the sugar plays in a recipe lets you choose the right substitute and expect changes in colour, volume and texture."),
      L(["Für Kuchen und Guetzli: einen Zuckeralkohol oder eine Mischung mit Masse wählen, nicht reinen Süßstoff, weil Zucker dort Volumen gibt.",
         "Mit Ersatz gebackenes bräunt oft schwächer: nach Zeit und Garprobe gehen, nicht nach Farbe.",
         "Bei Teigen mit Hefe etwas Zucker drinlassen, weil die Hefe ihn als Futter braucht.",
         "Xylit und damit Gebackenes für Hunde unerreichbar aufbewahren."],
        ["For cakes and biscuits: choose a sugar alcohol or a blend with bulk, not pure sweetener, because sugar gives volume there.",
         "Bakes made with substitutes often brown less: go by time and a skewer test, not by colour.",
         "In yeast doughs leave in a little sugar, because the yeast needs it as food.",
         "Keep xylitol and anything baked with it out of reach of dogs."]),
      ["zucker", "zucker-feuchtigkeit", "karamellisierung", "maillard-reaktion", "hefegaerung", "suess", "zucker-kristallisation"],
      ["w-gebaeck", "w-suesses"],
      "a sugar bowl beside small jars of white erythritol crystals and green stevia leaves, with a muffin",
      [{"titel": "National Geographic: Baking with sugar substitutes (2013)", "url": "https://www.nationalgeographic.com/science/article/130717-sugar-substitutes-nutrasweet-splenda-stevia-baking"},
       CB("4.8 Sugar Substitutes", "04%3A_Sugar/4.08%3A_Sugar_Substitutes_(ADD_US)"), CB("4.3 The Application of Sugar", "04%3A_Sugar/4.03%3A_The_Application_of_Sugar")]))

# Bestehende Einträge: Buch als ergänzende Quelle
QUELLE_DAZU = {
    "staerkeverkleisterung": CB("1.5 Gelatinization", "01%3A_Thickening_and_Concentrating_Flavors/1.05%3A_Gelatinization"),
    "eiweiss-gerinnung": CB("1.4 Coagulation", "01%3A_Thickening_and_Concentrating_Flavors/1.04%3A_Coagulation"),
    "kasein": CB("1.4 Coagulation", "01%3A_Thickening_and_Concentrating_Flavors/1.04%3A_Coagulation"),
    "zucker-kristallisation": CB("1.6 Crystallization", "01%3A_Thickening_and_Concentrating_Flavors/1.06%3A_Crystallization"),
    "fett-kristallisation": CB("1.6 Crystallization", "01%3A_Thickening_and_Concentrating_Flavors/1.06%3A_Crystallization"),
    "xanthan": CB("1.7 Non-traditional thickeners", "01%3A_Thickening_and_Concentrating_Flavors/1.07%3A_Non-traditional_thickeners"),
    "mehl": CB("2.8 Flour in Baking", "02%3A_Flour/2.08%3A_Flour_in_Baking"),
    "fett": CB("3.1 Understanding Fats and Oils", "03%3A_Fat/3.01%3A_Understanding_Fats_and_Oils"),
    "butter": CB("3.3 Major Fats and Oils Used in Bakeries", "03%3A_Fat/3.03%3A_Major_Fats_and_Oils_Used_in_Bakeries"),
    "zucker": CB("4.3 The Application of Sugar", "04%3A_Sugar/4.03%3A_The_Application_of_Sugar"),
    "honig": CB("4.5 Honey", "04%3A_Sugar/4.05%3A_Honey"),
    "malz": CB("4.6 Malt", "04%3A_Sugar/4.06%3A_Malt"),
    "glukosesirup": CB("4.9 Glucose/Dextrose", "04%3A_Sugar/4.09%3A_GlucoseDextrose"),
    "hefe": CB("5.2 Yeast", "05%3A_Leavening_Agents/5.02%3A_Yeast"),
    "hefegaerung": CB("5.4 Using Yeast in Baking", "05%3A_Leavening_Agents/5.04%3A_Using_Yeast_in_Baking"),
    "backpulver": CB("5.5 Baking Powder", "05%3A_Leavening_Agents/5.05%3A_Baking_Powder"),
    "natron": CB("5.6 Sodium Bicarbonate", "05%3A_Leavening_Agents/5.06%3A_Sodium_Bicarbonate"),
    "hirschhornsalz": CB("5.7 Ammonium Bicarbonate", "05%3A_Leavening_Agents/5.07%3A_Ammonium_Bicarbonate"),
    "milch": CB("6.2 Milk", "06%3A_Dairy_Products/6.02%3A_Milk"),
    "milchzucker": CB("6.6 Lactose", "06%3A_Dairy_Products/6.06%3A_Lactose"),
    "kaese": CB("6.7 Cheese", "06%3A_Dairy_Products/6.07%3A_Cheese"),
    "ei": CB("7.4 The Function of Eggs", "07%3A_Eggs/7.04%3A_The_Function_of_Eggs"),
    "schokolade": CB("8.1 From the Cocoa Bean to the Finished Chocolate", "08%3A_Chocolate/8.01%3A_From_the_Cocoa_Bean_to_the_Finished_Chocolate"),
    "kakaobutter": CB("8.3 Couverture", "08%3A_Chocolate/8.03%3A_Couverture"),
    "salz": CB("9.5 Using Salt in Fermented Doughs", "09%3A_Spices/9.05%3A_Using_Salt_in_Fermented_Doughs"),
}

if __name__ == "__main__":
    known = {f[:-5] for f in os.listdir(f"{ROOT}/content/entries")} | {e["id"] for e in E}
    ml = json.load(open(f"{ROOT}/content/master-list.json"))
    have = {m["id"] for m in ml["eintraege"]}
    for e in E:
        de = res(e, 0)
        miss = [l for l in de.get("links", []) if l not in known]
        if miss: print("Unbekannte Verweise in", de["id"], miss)
        de["links"] = [l for l in de.get("links", []) if l in known]
        for r in de.get("rolle", []):
            if r["prozess"] not in known: print("Unbekannter Prozess", de["id"], r["prozess"])
        json.dump(de, open(f"{ROOT}/content/entries/{de['id']}.json", "w"), ensure_ascii=False, indent=2)
        if de["id"] not in have:
            ml["eintraege"].append({"id": de["id"], "typ": de["typ"], "titel": de["titel"], "status": "entwurf", "pilot": False, "links": de["links"],
                                    "welten": de.get("welten", []), "synonyme": de.get("synonyme", []), "visual": {"vorlage": de.get("visual", {}).get("vorlage", "keine")}, "verlinkt_von": []})
    for i, q in QUELLE_DAZU.items():
        p = f"{ROOT}/content/entries/{i}.json"
        if not os.path.exists(p): print("fehlt:", i); continue
        x = json.load(open(p))
        if not any(s.get("url") == q["url"] for s in x.setdefault("quellen", [])):
            x["quellen"].append(q)
            json.dump(x, open(p, "w"), ensure_ascii=False, indent=2)
    ml["anzahl"] = len(ml["eintraege"])
    json.dump(ml, open(f"{ROOT}/content/master-list.json", "w"), ensure_ascii=False, indent=2)
    ids = [e["id"] for e in E]
    ex = json.loads(subprocess.check_output([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "extract", *ids], cwd=ROOT))

    def pick(shape, src):
        if isinstance(shape, dict): return {k: (src[k] if k == "synonyme" else pick(v, src[k])) for k, v in shape.items()}
        if isinstance(shape, list): return [pick(v, src[i]) for i, v in enumerate(shape)]
        if isinstance(src, dict): return src.get("wirkung", src.get("text", src.get("rolle")))
        if isinstance(src, list) and not isinstance(shape, list): return src[0]
        return src
    batch = {e["id"]: pick(ex[e["id"]], res(e, 1)) for e in E}
    path = f"{ROOT}/content/en/_batch_chemiebuch.json"
    json.dump(batch, open(path, "w"), ensure_ascii=False, indent=1)
    subprocess.check_call([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "apply", path], cwd=ROOT)
    os.remove(path)
    print(len(E), "Einträge geschrieben,", len(QUELLE_DAZU), "Quellen ergänzt")
