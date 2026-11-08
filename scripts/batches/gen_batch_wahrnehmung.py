"""Wahrnehmung: Mundgefühl, Temperatur und Geschmack, Kontraste, Abschmecken, Augen und Ohren essen mit,
Experiment Farbe täuscht, plus Lernpfad «Schmecken lernen» (8. November 2026). Hilfsfunktionen aus gen_batch_welten3."""
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


def P(id, titel, syn, kurz, bild, was, warum, regeln, stell, links, welten, illu, quellen, praxis=()):
    return {"id": id, "typ": "prozess", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild, "was_passiert": was, "warum_wichtig": warum,
            "faustregeln": regeln, "stellschrauben": [{"id": a, "wirkung": b} for a, b in stell], "praxis": [{"welt": a, "text": b} for a, b in praxis],
            "links": links, "welten": welten, "visual": {"vorlage": "keine", "illustration": illu}, "quellen": quellen, "status": "entwurf", "schwierigkeit": "einsteiger"}


def G(id, titel, syn, kurz, bild, schritte, links, welten, illu, quellen, schw="einsteiger"):
    return {"id": id, "typ": "gericht", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild, "schwierigkeit": schw,
            "schluesselmomente": [{"schritt": a, "warum": b, "prinzip": c} for a, b, c in schritte],
            "links": links, "welten": welten, "visual": {"vorlage": "ablauf", "illustration": illu}, "quellen": quellen, "status": "entwurf"}


RMS = {"titel": "Rolls et al.: Sensory specific satiety in man. Physiology & Behavior 27 (1981)", "url": "https://doi.org/10.1016/0031-9384(81)90310-3"}
TAL = {"titel": "Talavera et al.: Heat activation of TRPM5 underlies thermal sensitivity of sweet taste. Nature 438 (2005)", "url": "https://www.nature.com/articles/nature04248"}
MORROT = {"titel": "Morrot, Brochet, Dubourdieu: The color of odors. Brain and Language 79 (2001)", "url": "https://doi.org/10.1006/brln.2001.2493"}
ZAMPINI = {"titel": "Zampini, Spence: The role of auditory cues in modulating the perceived crispness and staleness of potato chips. Journal of Sensory Studies 19 (2004)", "url": "https://doi.org/10.1111/j.1745-459x.2004.080403.x"}

add(P("mundgefuehl", L("Mundgefühl: wie sich Essen im Mund anfühlt", "Mouthfeel: how food feels in the mouth"),
      L(["Mundgefühl", "Textur", "adstringierend", "pelzig im Mund", "Tannine", "Gerbstoffe", "Wein trocken im Mund", "Fett macht rund"], ["mouthfeel", "texture", "astringent", "furry mouth", "tannins", "why fat feels rich"]),
      L("Neben Geschmack und Duft spüren Zunge und Gaumen auch Textur, Fett und Zusammenziehen: Dieses Mundgefühl entscheidet oft mehr als das Aroma, ob uns etwas schmeckt.",
        "Besides taste and smell, tongue and palate also feel texture, fat and dryness: this mouthfeel often decides more than the aroma whether we like something."),
      L("Wie Stoff auf der Haut: Dieselbe Farbe fühlt sich als Seide ganz anders an als als Sackleinen.",
        "Like fabric on the skin: the same colour feels quite different as silk than as sackcloth."),
      L("Der Mund spürt, ob etwas dick oder dünn, glatt oder körnig, knusprig oder weich ist. Fett legt sich als Film auf die Zunge, wirkt rund und hält Aromen länger fest. Gerbstoffe (Tannine) in Rotwein, Schwarztee oder unreifen Früchten verbinden sich mit Eiweiß im Speichel: Der Mund fühlt sich trocken und pelzig an (adstringierend).",
        "The mouth senses whether something is thick or thin, smooth or grainy, crisp or soft. Fat forms a film on the tongue, feels rounded and holds aromas longer. Tannins in red wine, black tea or unripe fruit bind with protein in saliva: the mouth feels dry and furry (astringent)."),
      L("Viele Küchentricks verändern gar nicht den Geschmack, sondern das Mundgefühl: Butter in der Sauce, Milch im Tee, ein Löffel Rahm in der Suppe.",
        "Many kitchen tricks change not the taste but the mouthfeel: butter in a sauce, milk in tea, a spoonful of cream in soup."),
      L(["Wirkt eine Sauce dünn und spitz, fehlt oft Fett: ein Stück kalte Butter rundet sie ab.",
         "Milch im Schwarztee mildert das Pelzige, weil ihr Eiweiß die Gerbstoffe abfängt.",
         "Für glatte Cremes und Saucen: lieber passieren oder mixen, Körnchen stören mehr als ein schwacher Geschmack."],
        ["If a sauce tastes thin and sharp, it often lacks fat: a knob of cold butter rounds it out.",
         "Milk in black tea softens the furriness because its protein captures the tannins.",
         "For smooth creams and sauces: strain or blend, grains bother us more than a weak flavour."]),
      [("fettgehalt", L("Mehr Fett wirkt runder und trägt Aromen länger", "More fat feels rounder and carries aromas longer"))],
      ["aroma-loeslichkeit", "cremig", "montieren", "kontraste", "geschmack-balance", "w-milch"], ["w-saucen", "w-kaffee"],
      "a spoon dripping glossy butter sauce next to a cup of black tea with a splash of milk swirling in",
      [MC("Kapitel Geschmack und Aroma; Wein und Tee: Gerbstoffe", "Chapter on taste and flavour; wine and tea: tannins")],
      praxis=[("w-kaffee", L("Ein Schuss Milch macht starken Schwarztee weicher, weil das Milcheiweiß die Gerbstoffe bindet.", "A splash of milk makes strong black tea softer because milk protein binds the tannins."))]))

add(P("temperatur-geschmack", L("Temperatur verändert den Geschmack", "Temperature changes taste"),
      L(["kalt schmeckt anders", "kaltes Essen würzen", "warm schmeckt süßer", "Temperatur Geschmack", "Gazpacho würzen", "kalt servieren"], ["cold food tastes bland", "seasoning cold food", "warm tastes sweeter", "temperature and taste"]),
      L("Kälte dämpft Süße und Duft, Wärme verstärkt beides: Kalt serviertes Essen braucht darum kräftigere Würze.",
        "Cold dulls sweetness and aroma, warmth strengthens both: food served cold therefore needs stronger seasoning."),
      L("Wie eine Stimme im Nebel: Bei Kälte kommt dasselbe nur gedämpft an.",
        "Like a voice in fog: in the cold the same message arrives only muffled."),
      L("Ein Teil der Signalkette für Süß arbeitet bei Wärme deutlich stärker. Duftstoffe sind flüchtig: Warmes Essen gibt viel mehr davon ab als kaltes. Sehr heißes Essen dagegen überdeckt feine Nuancen, weil die Hitze selbst im Vordergrund steht.",
        "Part of the signal chain for sweetness works much harder when warm. Aroma compounds are volatile: warm food releases far more of them than cold. Very hot food, on the other hand, masks fine nuances because the heat itself takes centre stage."),
      L("Erklärt, warum Kartoffelsalat am nächsten Tag fad wirkt, Glacemasse warm zu süß schmeckt und eine heiße Suppe nach dem Abkühlen plötzlich versalzen.",
        "Explains why potato salad tastes bland the next day, ice cream base tastes too sweet when warm and a hot soup suddenly seems oversalted once it cools."),
      L(["Kalt serviertes Essen kalt abschmecken und kräftiger würzen.",
         "Suppen und Saucen nicht kochend heiß abschmecken: einen Löffel kurz abkühlen lassen.",
         "Käse und Rotwein nicht eiskalt servieren, sonst bleibt ihr Aroma stumm."],
        ["Taste food served cold while cold and season it more strongly.",
         "Don't taste soups and sauces boiling hot: let a spoonful cool briefly.",
         "Don't serve cheese and red wine ice-cold, or their aroma stays silent."]),
      [("temperatur", L("Wärmer schmeckt süßer und duftet stärker, kälter gedämpfter", "Warmer tastes sweeter and smells stronger, colder more muted"))],
      ["suess", "aroma-nase", "abschmecken", "essen-flach", "x-temperatur-cola"], [],
      "two bowls of the same soup, one steaming hot and one cold with ice cubes in a glass beside it, a tasting spoon",
      [TAL, MC("Kapitel Geschmack und Aroma", "Chapter on taste and flavour")]))

add(P("kontraste", L("Kontraste: warum Gegensätze Spannung bringen", "Contrast: why opposites add excitement"),
      L(["Kontrast", "knusprig und cremig", "Textur kombinieren", "warm und kalt", "Gericht langweilig", "Spannung im Gericht"], ["contrast in food", "crunchy and creamy", "combining textures", "hot and cold", "boring dish"]),
      L("Derselbe Eindruck nutzt sich beim Essen schnell ab: Ein Gegensatz in Textur, Temperatur oder Geschmack hält jeden Bissen interessant.",
        "The same sensation wears off quickly while eating: a contrast in texture, temperature or taste keeps every bite interesting."),
      L("Wie Musik mit nur einem Ton: Auch ein schöner Ton wird nach einer Minute langweilig, erst der Wechsel macht eine Melodie.",
        "Like music with a single note: even a beautiful note gets boring after a minute, only change makes a melody."),
      L("Unsere Sinne gewöhnen sich rasch an einen gleichbleibenden Reiz. Die Freude an genau diesem Eindruck sinkt, schon während man isst (sensorisch-spezifische Sättigung). Ein Gegenreiz setzt die Aufmerksamkeit wieder zurück: Knuspriges zu Cremigem, Säure zu Fett, Kaltes zu Warmem.",
        "Our senses quickly get used to a steady stimulus. The pleasure in exactly that sensation drops even while eating (sensory-specific satiety). A counter-stimulus resets attention: crunchy with creamy, acid with fat, cold with warm."),
      L("Viele Klassiker leben davon: Affogato, Pommes mit Mayonnaise, Risotto mit knusprigem Parmesan, Gurkensalat zum fetten Braten.",
        "Many classics live on this: affogato, chips with mayonnaise, risotto with crisp Parmesan, cucumber salad with a rich roast."),
      L(["Wirkt ein Gericht eintönig: etwas Knuspriges darüber, geröstete Nüsse, Brösel oder Zwiebeln.",
         "Zu Fettem etwas Saures servieren: Essiggurke, Zitrone, eingelegtes Gemüse.",
         "Warm und kalt kombinieren: Glace auf warmem Kuchen, kalter Joghurt zu scharfem Curry."],
        ["If a dish feels monotonous: add something crunchy on top, toasted nuts, crumbs or onions.",
         "Serve something sour with rich food: gherkins, lemon, pickled vegetables.",
         "Combine warm and cold: ice cream on warm cake, cold yoghurt with a hot curry."]),
      [],
      ["knusprig", "cremig", "mundgefuehl", "geschmack-balance", "saeure"], [],
      "a scoop of vanilla ice cream melting on a warm slice of apple crumble with crisp crumbs",
      [RMS, MC("Kapitel Geschmack und Aroma", "Chapter on taste and flavour")]))

add(T("abschmecken", L("Richtig abschmecken", "How to season to taste"),
      L(["abschmecken", "was fehlt", "Essen schmeckt nach nichts", "würzen lernen", "nachwürzen", "Geschmack prüfen"], ["seasoning to taste", "what's missing", "food tastes of nothing", "learning to season", "adjusting seasoning"]),
      L("Abschmecken heißt fragen, was fehlt, und in einer festen Reihenfolge nachwürzen: zuerst Salz, dann Säure, dann Süße, Schärfe und Umami, zuletzt Frisches.",
        "Seasoning to taste means asking what is missing and adjusting in a set order: salt first, then acid, then sweetness, heat and umami, fresh things last."),
      L("Wie ein Instrument stimmen: zuerst den Grundton, erst dann die feinen Saiten.",
        "Like tuning an instrument: the base note first, only then the fine strings."),
      L("Salz verstärkt alle anderen Geschmäcker, darum kommt es zuerst. Säure macht ein Gericht lebendig und leichter. Süße, Fett und Umami runden ab und geben Tiefe. Kräuter, Zitronenschale und Pfeffer liefern Duft, der in der Hitze verfliegt, darum kommen sie zuletzt.",
        "Salt boosts all other tastes, so it comes first. Acid makes a dish lively and lighter. Sweetness, fat and umami round off and add depth. Herbs, lemon zest and pepper bring aroma that escapes in the heat, so they come last."),
      L("Der Schritt vom Rezept zum eigenen Kochen: Wer abschmecken kann, rettet fade, flache oder zu scharfe Gerichte, auch ohne Rezept.",
        "The step from following recipes to cooking for yourself: knowing how to season rescues bland, flat or overly hot dishes, even without a recipe."),
      L(["Bei der Temperatur probieren, mit der serviert wird.",
         "Fad, schmeckt nach wenig: eine Prise Salz, kurz rühren, erneut probieren.",
         "Schwer, flach, müde: ein paar Tropfen Zitrone oder Essig.",
         "Spitz, zu sauer oder zu scharf: etwas Süße oder Fett, etwa Honig, Butter oder Rahm.",
         "Fehlt Tiefe: Umami, etwa Parmesan, Sojasauce, Tomatenmark oder Miso. Ganz am Schluss Kräuter, Zitronenschale oder Pfeffer."],
        ["Taste at the temperature it will be served.",
         "Bland, tastes of little: a pinch of salt, stir briefly, taste again.",
         "Heavy, flat, tired: a few drops of lemon or vinegar.",
         "Sharp, too sour or too hot: a little sweetness or fat, such as honey, butter or cream.",
         "Lacks depth: umami, such as Parmesan, soy sauce, tomato paste or miso. At the very end herbs, lemon zest or pepper."]),
      L(["In kleinen Schritten würzen und nach jedem Schritt probieren: Was drin ist, bekommt man nicht mehr heraus.",
         "Unsicher, ob etwas passt: zuerst nur einen Löffel davon würzen und vergleichen.",
         "Nach dem Einkochen nochmals probieren, weil sich Salz dabei konzentriert."],
        ["Season in small steps and taste after each one: what is in cannot be taken out.",
         "Unsure whether something fits: season just one spoonful first and compare.",
         "Taste again after reducing, because salt concentrates as it does."]),
      ["geschmack-balance", "salz-geschmack", "abschmecken-saeure", "umami", "temperatur-geschmack", "essen-flach", "essen-versalzen"], ["w-saucen"],
      "a wooden tasting spoon over a pot of soup with small bowls of salt, lemon, honey and grated Parmesan around it",
      [MC("Kapitel Geschmack und Aroma", "Chapter on taste and flavour")]))

add(P("augen-ohren", L("Augen und Ohren essen mit", "We eat with our eyes and ears"),
      L(["Farbe und Geschmack", "Aussehen Geschmack", "Geräusch knusprig", "Erwartung beim Essen", "Anrichten", "Teller anrichten Wirkung"], ["colour and taste", "appearance and flavour", "crunch sound", "expectation when eating", "plating"]),
      L("Was wir sehen und hören, verändert, was wir schmecken: Farbe weckt Erwartungen, und das Knacken beim Beißen lässt Chips frischer wirken.",
        "What we see and hear changes what we taste: colour raises expectations, and the crunch when biting makes crisps seem fresher."),
      L("Wie eine Filmmusik: Dieselbe Szene wirkt mit fröhlicher Musik heiter, mit düsterer bedrohlich.",
        "Like a film score: the same scene feels cheerful with happy music and menacing with dark music."),
      L("Das Gehirn setzt Geschmack aus allen Sinnen zusammen und füllt Lücken mit Erwartungen. In einem bekannten Versuch beschrieben Weinkenner rot gefärbten Weißwein mit Begriffen für Rotwein. In einem anderen wirkten Chips knuspriger und frischer, wenn das Knacken lauter über Kopfhörer kam.",
        "The brain builds taste from all the senses and fills gaps with expectations. In a well-known study, wine experts described white wine dyed red using terms for red wine. In another, crisps seemed crisper and fresher when the crunch sounded louder through headphones."),
      L("Erklärt, warum blasses Fleisch weniger würzig wirkt, warum Anrichten nicht nur Dekoration ist und warum matschige Pommes enttäuschen, auch wenn sie gut schmecken.",
        "Explains why pale meat seems less flavoursome, why plating is more than decoration and why soggy chips disappoint even when they taste fine."),
      L(["Farbe ist Geschmack: gut bräunen lohnt sich doppelt, für Aroma und Erwartung.",
         "Knuspriges erst kurz vor dem Servieren auf das Gericht, damit es hörbar knackt.",
         "Frische Kräuter und ein Spritzer Farbe am Schluss lassen ein Gericht lebendiger wirken."],
        ["Colour is flavour: browning well pays off twice, for aroma and for expectation.",
         "Add crunchy things just before serving so they audibly crunch.",
         "Fresh herbs and a splash of colour at the end make a dish seem livelier."]),
      [],
      ["farbe", "maillard-reaktion", "knusprig", "kontraste", "x-farbe-taeuscht", "aroma-nase"], [],
      "a glass of white wine and a glass of the same wine tinted red side by side, a bowl of crisps and headphones",
      [MORROT, ZAMPINI]))

add({"id": "x-farbe-taeuscht", "typ": "experiment", "titel": L("Farbe täuscht den Geschmack", "Colour fools the taste"),
     "synonyme": L(["Farbe Geschmack Experiment", "Lebensmittelfarbe Test", "Geschmackstest Farbe"], ["colour taste experiment", "food colouring test", "taste test colour"]),
     "kurz": L("Drei Gläser mit demselben Getränk, nur anders gefärbt: Die meisten schmecken plötzlich Kirsche, Zitrone oder Apfel.",
               "Three glasses of the same drink, only coloured differently: most people suddenly taste cherry, lemon or apple."),
     "bild_im_kopf": L("Wie ein Etikett auf einer Flasche: Wir schmecken oft, was draufsteht, nicht was drin ist.", "Like a label on a bottle: we often taste what it says, not what is inside."),
     "material": L(["heller Traubensaft oder Zuckerwasser mit etwas Zitrone", "rote, gelbe und grüne Lebensmittelfarbe", "drei gleiche Gläser", "eine Person, die probiert, und eine, die eingießt"],
                   ["pale grape juice or sugar water with a little lemon", "red, yellow and green food colouring", "three identical glasses", "one person to taste and one to pour"]),
     "schritte": L(["In drei Gläser dasselbe Getränk gießen, ohne dass die probierende Person zusieht.",
                    "Jedes Glas mit einem Tropfen einer anderen Farbe färben.",
                    "Probieren lassen und fragen: Nach welcher Frucht schmeckt es?",
                    "Erst danach verraten, dass alle drei gleich sind."],
                   ["Pour the same drink into three glasses without the taster watching.",
                    "Colour each glass with a drop of a different colour.",
                    "Let them taste and ask: which fruit does it taste of?",
                    "Only then reveal that all three are the same."]),
     "beobachtung": L("Das rote Glas schmeckt vielen nach Kirsche oder Erdbeere, das gelbe nach Zitrone, das grüne nach Apfel oder Limette.",
                      "To many, the red glass tastes of cherry or strawberry, the yellow of lemon, the green of apple or lime."),
     "erklaerung": L("Das Gehirn setzt Geschmack aus allen Sinnen zusammen. Die Farbe weckt eine Erwartung, und die Nase findet im schwachen Duft, was sie sucht.",
                     "The brain builds taste from all the senses. The colour raises an expectation, and the nose finds what it is looking for in the faint aroma."),
     "dauer": L("10 Minuten", "10 minutes"),
     "links": ["augen-ohren", "aroma-nase", "x-nase-zu"], "welten": [],
     "visual": {"vorlage": "ablauf", "illustration": "three identical glasses of drink tinted red, yellow and green with a small bottle of food colouring"},
     "quellen": [MORROT], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "x-temperatur-cola", "typ": "experiment", "titel": L("Warme Limonade schmeckt süßer", "Warm lemonade tastes sweeter"),
     "synonyme": L(["Temperatur Süße Experiment", "warme Cola süß", "Geschmackstest Temperatur"], ["temperature sweetness experiment", "warm cola sweeter", "taste test temperature"]),
     "kurz": L("Dieselbe Limonade, einmal eiskalt und einmal zimmerwarm: Die warme schmeckt deutlich süßer, obwohl gleich viel Zucker drin ist.",
               "The same lemonade, once ice-cold and once at room temperature: the warm one tastes noticeably sweeter, although it contains the same sugar."),
     "bild_im_kopf": L("Wie ein Lautstärkeregler, den die Kälte herunterdreht.", "Like a volume knob that the cold turns down."),
     "material": L(["eine Flasche Limonade oder Apfelsaft", "zwei Gläser", "Eiswürfel"], ["a bottle of lemonade or apple juice", "two glasses", "ice cubes"]),
     "schritte": L(["Ein Glas mit Eis kühlen, das andere zimmerwarm lassen.",
                    "In beide gleich viel Limonade gießen, das kalte Glas einige Minuten kühlen lassen, Eis entfernen.",
                    "Abwechselnd probieren, dazwischen Wasser trinken.",
                    "Vergleichen: Welches schmeckt süßer?"],
                   ["Chill one glass with ice and leave the other at room temperature.",
                    "Pour the same amount of lemonade into each, let the cold one chill for a few minutes, remove the ice.",
                    "Taste them in turn, drinking water in between.",
                    "Compare: which tastes sweeter?"]),
     "beobachtung": L("Die zimmerwarme Limonade schmeckt deutlich süßer und klebriger, die kalte frischer und weniger süß.",
                      "The room-temperature lemonade tastes much sweeter and stickier, the cold one fresher and less sweet."),
     "erklaerung": L("Der Süß-Sensor auf der Zunge arbeitet bei Wärme stärker. Darum enthalten kalte Getränke und Glace viel Zucker, den man kaum merkt.",
                     "The sweet sensor on the tongue works harder when warm. That is why cold drinks and ice cream contain a lot of sugar you barely notice."),
     "dauer": L("10 Minuten", "10 minutes"),
     "links": ["temperatur-geschmack", "suess", "x-nase-zu"], "welten": ["w-suesses"],
     "visual": {"vorlage": "ablauf", "illustration": "two glasses of golden lemonade, one frosty with ice cubes and one plain, on a small tray"},
     "quellen": [TAL], "status": "entwurf", "schwierigkeit": "einsteiger"})

PFAD = {
    "id": "schmecken-lernen", "titel": L("Schmecken lernen", "Learning to taste"),
    "kurz": L("Was die Zunge spürt, was die Nase riecht und warum Salz, Säure und Kontraste ein Gericht lebendig machen: der Weg vom Rezept zum eigenen Abschmecken.",
              "What the tongue senses, what the nose smells and why salt, acid and contrast bring a dish to life: the path from following recipes to seasoning by yourself."),
    "fuer": L("Für alle, die nicht nur nachkochen, sondern selber abschmecken wollen", "For anyone who wants to season by themselves, not just follow recipes"),
    "dauer": L("etwa 45 Minuten, mit drei kleinen Selbstversuchen", "about 45 minutes, with three small self-experiments"),
    "schritte": [
        ("aroma-nase", L("Zuerst die Überraschung: Das meiste, was wir Geschmack nennen, riecht die Nase.", "First the surprise: most of what we call taste is smelled by the nose.")),
        ("x-nase-zu", L("Selbst ausprobieren: ein Gummibärchen mit zugehaltener Nase.", "Try it yourself: a gummy bear with your nose pinched.")),
        ("salz-geschmack", L("Salz macht nicht nur salzig, es hebt alles andere.", "Salt doesn't only make things salty, it lifts everything else.")),
        ("saeure", L("Säure macht ein Gericht lebendig und leichter.", "Acid makes a dish lively and lighter.")),
        ("umami", L("Der herzhafte fünfte Geschmack und wo er steckt.", "The savoury fifth taste and where it hides.")),
        ("bitter", L("Bitter: warum wenig davon Tiefe gibt.", "Bitter: why a little of it adds depth.")),
        ("x-salz-bitter", L("Selbst ausprobieren: Salz auf Grapefruit.", "Try it yourself: salt on grapefruit.")),
        ("temperatur-geschmack", L("Warum kalt anders schmeckt als warm.", "Why cold tastes different from warm.")),
        ("mundgefuehl", L("Was sich im Mund anfühlt, zählt so viel wie der Geschmack.", "What we feel in the mouth counts as much as the taste.")),
        ("kontraste", L("Gegensätze halten jeden Bissen spannend.", "Contrasts keep every bite exciting.")),
        ("augen-ohren", L("Augen und Ohren essen mit.", "Eyes and ears eat too.")),
        ("geschmack-balance", L("Wie sich die Geschmäcker gegenseitig dämpfen und heben.", "How tastes dampen and lift one another.")),
        ("abschmecken", L("Alles zusammen: in welcher Reihenfolge man nachwürzt.", "All together: the order in which to adjust seasoning.")),
    ],
    "quiz": [
        (L("Warum schmeckt Essen bei Schnupfen fad?", "Why does food taste bland when you have a cold?"),
         [L("Die Zunge ist geschwollen", "The tongue is swollen"), L("Die Nase riecht den Duft beim Kauen nicht mehr", "The nose can no longer smell the aroma while chewing"), L("Der Speichel fehlt", "There is no saliva")], 1,
         L("Fast alle Aromen riecht die Nase, auch von innen beim Kauen. Die Zunge allein erkennt nur fünf Grundgeschmäcker.", "The nose smells almost all aromas, including from inside while chewing. The tongue alone only recognises five basic tastes."), "aroma-nase"),
        (L("Ein Eintopf schmeckt schwer und müde. Was hilft meist am schnellsten?", "A stew tastes heavy and tired. What usually helps fastest?"),
         [L("Ein paar Tropfen Zitrone oder Essig", "A few drops of lemon or vinegar"), L("Mehr Wasser", "More water"), L("Länger kochen", "Cook it longer")], 0,
         L("Säure macht Gerichte lebendiger und leichter, besonders fette und lange gekochte.", "Acid makes dishes livelier and lighter, especially rich and long-cooked ones."), "saeure"),
        (L("Warum braucht Kartoffelsalat am nächsten Tag oft mehr Würze?", "Why does potato salad often need more seasoning the next day?"),
         [L("Das Salz zerfällt über Nacht", "The salt breaks down overnight"), L("Kälte dämpft Geschmack und Duft", "Cold dulls taste and aroma"), L("Kartoffeln werden bitter", "Potatoes turn bitter")], 1,
         L("Kalt gibt Essen weniger Duft ab, und Süße wirkt schwächer. Darum kalt abschmecken.", "Cold food releases less aroma and sweetness seems weaker. So taste it cold."), "temperatur-geschmack"),
        (L("Was gehört beim Abschmecken zuerst ins Gericht?", "What goes into the dish first when seasoning?"),
         [L("Kräuter", "Herbs"), L("Zucker", "Sugar"), L("Salz", "Salt")], 2,
         L("Salz verstärkt alle anderen Geschmäcker. Erst danach lässt sich beurteilen, was sonst noch fehlt.", "Salt boosts all other tastes. Only then can you judge what else is missing."), "abschmecken"),
        (L("Warum wirkt ein Risotto mit knusprigem Parmesan oben spannender?", "Why does a risotto topped with crisp Parmesan seem more exciting?"),
         [L("Der Kontrast hält die Sinne wach", "The contrast keeps the senses alert"), L("Knuspriges enthält mehr Salz", "Crisp things contain more salt"), L("Parmesan ist bitter", "Parmesan is bitter")], 0,
         L("Ein gleichbleibender Eindruck nutzt sich ab. Ein Gegensatz setzt die Aufmerksamkeit zurück.", "An unchanging sensation wears off. A contrast resets attention."), "kontraste"),
    ],
}


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
    path = f"{ROOT}/content/en/_batch_wahrnehmung.json"
    json.dump(batch, open(path, "w"), ensure_ascii=False, indent=1)
    subprocess.check_call([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "apply", path], cwd=ROOT)
    os.remove(path)
    # Lernpfad Deutsch und Englisch
    for lang, file in ((0, "content/lernpfade.json"), (1, "content/en/lernpfade.json")):
        p = json.load(open(f"{ROOT}/{file}"))
        p = [x for x in p if x["id"] != PFAD["id"]]
        p.append({"id": PFAD["id"], "titel": PFAD["titel"][lang], "kurz": PFAD["kurz"][lang], "fuer": PFAD["fuer"][lang], "dauer": PFAD["dauer"][lang],
                  "schritte": [{"id": i, "warum": w[lang]} for i, w in PFAD["schritte"]],
                  "quiz": [{"frage": f[lang], "antworten": [a[lang] for a in an], "richtig": r, "erklaerung": er[lang], "eintrag": ei} for f, an, r, er, ei in PFAD["quiz"]]})
        json.dump(p, open(f"{ROOT}/{file}", "w"), ensure_ascii=False, indent=1)
    print(len(E), "Einträge und Lernpfad geschrieben")
