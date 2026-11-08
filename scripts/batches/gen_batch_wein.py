"""Wein: Wein beim Kochen (Alkohol-Balken), Warum Wein zu Essen passt (Wein-Waage), Sauce schmeckt nach Wein (8. November 2026)."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_batch_welten2 import L, res, MC, ROOT, U, tree3  # noqa: E402

E = []
add = E.append

ATK_SQUID = {"titel": "America's Test Kitchen: Why and how you should cook with squid", "url": "https://www.americastestkitchen.com/articles/why-and-how-you-should-cook-with-squid"}
ATK_EGGS = {"titel": "Cook's Illustrated: Easy-peel hard-cooked eggs", "url": "https://www.americastestkitchen.com/cooksillustrated/articles/168-easy-peel-hard-cooked-eggs"}
ATK_BEANS = {"titel": "America's Test Kitchen: How to brine beans", "url": "https://www.americastestkitchen.com/articles/7720-how-to-brine-beans"}
LIVESCI = {"titel": "Live Science: Why do cooked lobsters turn red?", "url": "https://livescience.com/66093-why-cooked-lobsters-turn-red.html"}
MUSSELS = {"titel": "Tasting Table: The rule about not eating closed mussels is actually complicated", "url": "https://www.tastingtable.com/1348663/rule-not-eating-closed-mussels-complicated/"}
VZ_PILZE = {"titel": "Verbraucherzentrale: Pilze aufwärmen", "url": "https://www.verbraucherzentrale.de/wissen/lebensmittel/lebensmittelproduktion/pilze-sammeln-zubereiten-und-aufwaermen-darauf-sollten-sie-achten-12279"}


def T(id, titel, syn, kurz, bild, was, warum, schritte, regeln, links, welten, illu, quellen, mythos=None, schw="einsteiger"):
    e = {"id": id, "typ": "technik", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild, "was_passiert": was, "warum_wichtig": warum,
         "schritte": schritte, "faustregeln": regeln, "links": links, "welten": welten, "visual": {"vorlage": "ablauf", "illustration": illu},
         "quellen": quellen, "status": "entwurf", "schwierigkeit": schw}
    if mythos:  # L((behauptung, richtig), (claim, truth))
        de, en = res(mythos, 0), res(mythos, 1)
        e["mythos"] = {"behauptung": L(de[0], en[0]), "richtig": L(de[1], en[1])}
    return e


def S(id, titel, syn, kurz, bild, ursachen, q1, q2, regeln, links, welten, illu, quellen):
    return {"id": id, "typ": "symptom", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild, "ursachen": ursachen,
            "diagnose": tree3(q1, q2), "faustregeln": regeln, "links": links, "welten": welten,
            "visual": {"vorlage": "entscheidungsbaum", "illustration": illu}, "quellen": quellen, "status": "entwurf", "schwierigkeit": "einsteiger"}


def P(id, titel, syn, kurz, bild, was, warum, regeln, stell, links, welten, illu, quellen, praxis=(), schw="einsteiger"):
    return {"id": id, "typ": "prozess", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild, "was_passiert": was, "warum_wichtig": warum,
            "faustregeln": regeln, "stellschrauben": [{"id": a, "wirkung": b} for a, b in stell], "praxis": [{"welt": a, "text": b} for a, b in praxis],
            "links": links, "welten": welten, "visual": {"vorlage": "keine", "illustration": illu}, "quellen": quellen, "status": "entwurf", "schwierigkeit": schw}


def G(id, titel, syn, kurz, bild, schritte, links, welten, illu, quellen, schw="einsteiger"):
    return {"id": id, "typ": "gericht", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild, "schwierigkeit": schw,
            "schluesselmomente": [{"schritt": a, "warum": b, "prinzip": c} for a, b, c in schritte],
            "links": links, "welten": welten, "visual": {"vorlage": "ablauf", "illustration": illu}, "quellen": quellen, "status": "entwurf"}


USDA = {"titel": "USDA Table of Nutrient Retention Factors, Release 6 (2007): Alkohol", "url": "https://www.ars.usda.gov/ARSUserFiles/80400525/Data/retn/retn06.pdf"}
GACHONS = {"titel": "Peyrot des Gachons et al.: Opponency of astringent and fat sensations. Current Biology 22 (2012)", "url": "https://www.sciencedaily.com/releases/2012/10/121008134215.htm"}

wk = P("wein-kochen", L("Wein beim Kochen: Was im Topf bleibt", "Cooking with wine: what stays in the pot"),
      L(["Kochen mit Wein", "welcher Wein zum Kochen", "Wein ablöschen", "Kochwein", "Alkohol verkocht", "Wein Sauce", "Weißwein oder Rotwein kochen", "Alkohol Kinder Sauce"],
        ["cooking with wine", "which wine for cooking", "deglazing with wine", "cooking wine", "does alcohol cook off", "wine sauce"]),
      L("Beim Kochen verfliegen feine Aromen und ein Teil des Alkohols, Säure und Gerbstoffe werden stärker: Beim Kochwein zählt der Stil mehr als der Preis.",
        "When cooking, delicate aromas and part of the alcohol escape while acidity and tannins intensify: with cooking wine, style matters more than price."),
      L("Wie ein Konzert durch die Wand: Die feinen Geigen hört man nicht mehr, Bass und Trommeln kommen deutlich an.",
        "Like a concert heard through a wall: the delicate violins are gone, the bass and drums come through clearly."),
      L("Wein besteht vor allem aus Wasser, Alkohol, Säure, etwas Zucker, Gerbstoffen und Duftstoffen. Beim Einkochen verdampfen Wasser, ein Teil des Alkohols und die meisten flüchtigen Fruchtaromen. Säure, Zucker und Gerbstoffe verdampfen nicht und werden konzentrierter. Der Alkohol verschwindet langsamer als gedacht: Nach einer Stunde Köcheln bleibt etwa ein Viertel (Richtwert).",
        "Wine is mostly water, alcohol, acid, a little sugar, tannins and aroma compounds. When reduced, water, part of the alcohol and most of the volatile fruit aromas evaporate. Acid, sugar and tannins do not evaporate and become more concentrated. The alcohol disappears more slowly than expected: after an hour of simmering about a quarter remains (as a guide)."),
      L("Ein teurer Wein lohnt sich im Topf kaum, ein schlechter verdirbt die Sauce aber zuverlässig. Wer für Kinder oder Menschen kocht, die keinen Alkohol trinken, sollte wissen, dass er nicht ganz verkocht.",
        "An expensive wine is hardly worth it in the pot, but a bad one reliably spoils the sauce. Anyone cooking for children or people who don't drink alcohol should know it doesn't fully cook off."),
      L(["Nur Wein verwenden, den man auch trinken würde: Fehler wie Kork oder Oxidation werden beim Einkochen stärker.",
         "Für Rahmsaucen, Fisch und Risotto: trockener, frischer Weißwein, weil seine Säure das Fett leichter macht.",
         "Für Schmorgerichte: fruchtiger, eher milder Rotwein; stark gerbstoffhaltige oder im Holz ausgebaute Weine werden eingekocht bitter.",
         "Wein zuerst um mindestens die Hälfte einkochen, dann erst Fond oder Rahm dazu, sonst schmeckt die Sauce roh und spitz.",
         "Gesalzenen Kochwein meiden: Er bringt unkontrolliert Salz in die Sauce."],
        ["Only use wine you would also drink: faults such as cork taint or oxidation get stronger when reduced.",
         "For cream sauces, fish and risotto: a dry, crisp white wine, because its acidity lightens the fat.",
         "For braises: a fruity, rather soft red; very tannic or oaked wines turn bitter when reduced.",
         "Reduce the wine by at least half before adding stock or cream, otherwise the sauce tastes raw and sharp.",
         "Avoid salted cooking wine: it adds salt to the sauce uncontrollably."]),
      [("zeit", L("Je länger gekocht, desto weniger Alkohol und desto konzentrierter Säure und Gerbstoffe", "The longer it cooks, the less alcohol and the more concentrated acidity and tannins")),
       ("temperatur", L("Sprudelnd kochen treibt Alkohol und Aromen schneller aus als sanftes Köcheln", "A rolling boil drives off alcohol and aromas faster than gentle simmering"))],
      ["wein", "deglacieren", "reduktion", "gerbstoffe", "sauce-wein", "wein-essen", "w-saucen"], ["w-saucen", "w-fleisch"],
      "a bottle of red and a bottle of white wine beside a small pot of reducing dark wine sauce with a wooden spoon",
      [USDA, MC("Kapitel Wein, Bier und Spirituosen: Kochen mit Wein", "Chapter on wine, beer and spirits: cooking with wine")],
      praxis=[("w-saucen", L("Für eine Rotweinsauce den Wein mit Schalotten fast sirupartig einkochen, dann Fond dazu und zum Schluss kalte Butter einrühren.", "For a red wine sauce, reduce the wine with shallots until almost syrupy, then add stock and finally stir in cold butter.")),
              ("w-fleisch", L("Beim Schmoren gart der Wein stundenlang mit: Ein milder Rotwein bleibt rund, ein sehr herber wird bitter.", "When braising, the wine cooks for hours: a soft red stays rounded, a very tannic one turns bitter."))])
wk["visual"]["vorlage"] = "alkoholrest"
add(wk)

we = P("wein-essen", L("Warum Wein zu Essen passt", "Why wine goes with food"),
      L(["Weinbegleitung", "welcher Wein passt zu", "Wein zum Essen", "Rotwein zu Fisch", "Wein zu Käse", "Wein zu Dessert", "Wein zu scharfem Essen", "Food Pairing Wein"],
        ["wine pairing", "which wine goes with", "wine with food", "red wine with fish", "wine with cheese", "wine with dessert", "wine with spicy food"]),
      L("Ob Wein und Essen zusammenpassen, ist zum Teil Gewohnheit, zum Teil Chemie: Gerbstoffe, Säure, Süße und Alkohol verändern, wie Fett, Salz und Schärfe schmecken.",
        "Whether wine and food go together is partly habit, partly chemistry: tannins, acidity, sweetness and alcohol change how fat, salt and heat taste."),
      L("Wie ein Tanzpaar: Der eine führt, der andere folgt, und beide sollten etwa gleich viel Schwung haben.",
        "Like a dancing couple: one leads, the other follows, and both should have about the same energy."),
      L("Gerbstoffe binden sich an Eiweiß und Fett. Zum Steak wirkt ein kräftiger Rotwein darum weicher, allein pelzig. Säure schneidet durch Fett, wie die Essiggurke zum Braten. Süßes Essen lässt trockenen Wein sauer und bitter schmecken, Salz macht ihn runder. Alkohol verstärkt das Brennen von Chili.",
        "Tannins bind to protein and fat. With steak a bold red therefore feels softer, on its own furry. Acidity cuts through fat, like a gherkin with a roast. Sweet food makes dry wine taste sour and bitter, salt makes it rounder. Alcohol intensifies the burn of chilli."),
      L("Diese wenigen Regeln erklären die meisten Klassiker und die meisten Fehlgriffe. Wer sie kennt, braucht keine Tabelle, sondern fragt: Was hat das Essen viel, und was bringt der Wein dagegen mit?",
        "These few rules explain most classic pairings and most mistakes. Knowing them, you need no chart, just the question: what does the food have a lot of, and what does the wine bring to balance it?"),
      L(["Zu fettem, eiweißreichem Fleisch: Rotwein mit Gerbstoffen.",
         "Zu Fisch keine gerbstoffreichen Rotweine: Gerbstoffe und Fischöl schmecken zusammen metallisch.",
         "Zu Fettem und Rahmigem: Wein mit viel Säure, er macht jeden Bissen leichter.",
         "Zum Dessert: Der Wein muss mindestens so süß sein wie das Essen.",
         "Zu Scharfem: leichte, eher süße Weine mit wenig Alkohol."],
        ["With fatty, protein-rich meat: a red wine with tannins.",
         "No tannic reds with fish: tannins and fish oil taste metallic together.",
         "With rich and creamy dishes: a high-acid wine, it makes every bite lighter.",
         "With dessert: the wine must be at least as sweet as the food.",
         "With spicy food: light, slightly sweet wines low in alcohol."]),
      [],
      ["gerbstoffe", "mundgefuehl", "kontraste", "geschmack-balance", "salz-geschmack", "schaerfe", "suess", "wein-kochen", "flavor-pairing"], ["w-fleisch", "w-milch"],
      "a glass of red wine beside a seared steak on a board and a glass of white wine beside a piece of salmon, drawn like a balance",
      [GACHONS, MC("Kapitel Wein: Wein und Essen", "Chapter on wine: wine and food")], schw="fortgeschritten")
we["visual"]["vorlage"] = "weinwaage"
add(we)

add(S("sauce-wein", L("Sauce schmeckt nach Wein: sauer, bitter oder roh", "Sauce tastes of wine: sour, bitter or raw"),
      L(["Weinsauce bitter", "Rotweinsauce bitter", "Sauce zu sauer Wein", "Sauce schmeckt nach Alkohol", "Weißweinsauce sauer"], ["wine sauce bitter", "red wine sauce bitter", "sauce tastes of alcohol", "white wine sauce too sour"]),
      L("Eine roh, sauer oder bitter schmeckende Weinsauce ist meist zu wenig eingekocht, mit zu herbem Wein gemacht oder ohne Ausgleich durch Fett.",
        "A wine sauce that tastes raw, sour or bitter is usually under-reduced, made with too tannic a wine or lacks balancing fat."),
      L("Wie Tee, der zu lange gezogen hat: Was kurz angenehm herb ist, wird mit der Zeit pelzig und bitter.",
        "Like tea that has steeped too long: what is pleasantly brisk at first turns furry and bitter over time."),
      [U(L("Zu wenig eingekocht", "Not reduced enough"), 3, "reduktion",
         L("Wird Fond oder Rahm zu früh dazugegeben, bleibt der Wein roh: spitze Säure und ein Hauch Alkohol.",
           "If stock or cream goes in too early, the wine stays raw: sharp acidity and a hint of alcohol."),
         [L("Wein zuerst um mindestens die Hälfte einkochen", "Reduce the wine by at least half first"), L("Die Sauce danach noch einige Minuten köcheln", "Then simmer the sauce for a few more minutes")]),
       U(L("Zu herber oder holziger Rotwein", "Too tannic or oaky a red"), 2, "gerbstoffe",
         L("Gerbstoffe verdampfen nicht. Eingekocht werden sie stärker und schmecken bitter und pelzig.",
           "Tannins don't evaporate. Reduced, they get stronger and taste bitter and furry."),
         [L("Fruchtigen, milden Rotwein nehmen", "Use a fruity, soft red"), L("Retten: ein Stück kalte Butter oder ein Schuss Rahm bindet die Gerbstoffe", "Rescue: a knob of cold butter or a splash of cream binds the tannins")]),
       U(L("Säure ohne Ausgleich", "Acidity without balance"), 2, "geschmack-balance",
         L("Weißwein bringt viel Säure. Ohne Fett, Salz und eine Spur Süße bleibt sie spitz.",
           "White wine brings a lot of acidity. Without fat, salt and a trace of sweetness it stays sharp."),
         [L("Kalte Butter einrühren, salzen und abschmecken", "Stir in cold butter, salt and taste"), L("Bei Bedarf eine Prise Zucker oder ein Löffel Rahm", "If needed, a pinch of sugar or a spoonful of cream")])],
      L("Hast du den Wein um mindestens die Hälfte eingekocht, bevor Fond oder Rahm dazukamen?", "Did you reduce the wine by at least half before adding stock or cream?"),
      L("War es ein kräftiger, gerbstoffreicher oder im Holz ausgebauter Rotwein?", "Was it a bold, tannic or oaked red?"),
      L(["Für eine runde Weinsauce: einkochen, dann mit Fond verlängern und mit kalter Butter binden.",
         "Bitter gewordene Sauce nicht mit noch mehr Wein retten, sondern mit Fett und einer Prise Süße."],
        ["For a rounded wine sauce: reduce, then extend with stock and bind with cold butter.",
         "Don't rescue a bitter sauce with more wine, but with fat and a pinch of sweetness."]),
      ["wein-kochen", "reduktion", "montieren", "gerbstoffe", "deglacieren", "w-saucen"], ["w-saucen"],
      "a small saucepan of dark red wine sauce with a tasting spoon, a knob of butter and a half-empty wine glass",
      [MC("Kapitel Saucen: Weinsaucen", "Chapter on sauces: wine sauces")]))


if __name__ == "__main__":
    known = {f[:-5] for f in os.listdir(f"{ROOT}/content/entries")} | {e["id"] for e in E}
    ml = json.load(open(f"{ROOT}/content/master-list.json"))
    have = {m["id"] for m in ml["eintraege"]}
    for e in E:
        de = res(e, 0)
        miss = [l for l in de.get("links", []) if l not in known]
        miss += [u["prinzip"] for u in de.get("ursachen", []) if u.get("prinzip") not in known]
        miss += [s["prinzip"] for s in de.get("schluesselmomente", []) if s.get("prinzip") not in known]
        miss += [s["id"] for s in de.get("stellschrauben", []) if s["id"] not in known]
        if miss: print("Unbekannte Verweise in", de["id"], miss)
        de["links"] = [l for l in de.get("links", []) if l in known]
        json.dump(de, open(f"{ROOT}/content/entries/{de['id']}.json", "w"), ensure_ascii=False, indent=2)
        if de["id"] not in have:
            ml["eintraege"].append({"id": de["id"], "typ": de["typ"], "titel": de["titel"], "status": "entwurf", "pilot": False, "links": de["links"],
                                    "welten": de.get("welten", []), "synonyme": de.get("synonyme", []), "visual": {"vorlage": de.get("visual", {}).get("vorlage", "keine")}, "verlinkt_von": []})
    ml["anzahl"] = len(ml["eintraege"])
    json.dump(ml, open(f"{ROOT}/content/master-list.json", "w"), ensure_ascii=False, indent=2)
    ids = [e["id"] for e in E]
    ex = json.loads(subprocess.check_output([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "extract", *ids], cwd=ROOT))

    def pick(shape, src):
        if isinstance(shape, dict): return {k: (src[k] if k == "synonyme" else pick(v, src[k])) for k, v in shape.items()}
        if isinstance(shape, list): return [pick(v, src[i]) for i, v in enumerate(shape)]
        if isinstance(src, dict): return src.get("wirkung", src.get("text"))
        if isinstance(src, list) and not isinstance(shape, list): return src[0]
        return src
    batch = {e["id"]: pick(ex[e["id"]], res(e, 1)) for e in E}
    path = f"{ROOT}/content/en/_batch_wein.json"
    json.dump(batch, open(path, "w"), ensure_ascii=False, indent=1)
    subprocess.check_call([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "apply", path], cwd=ROOT)
    os.remove(path)
    print(len(E), "Einträge geschrieben")
