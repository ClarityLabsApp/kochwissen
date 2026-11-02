"""Batch Welten II: dünne Welten auffüllen (Kaffee & Tee, Pasta, Geflügel, Fisch, Reis) und vier neue Welten
(Hülsenfrüchte, Obst, Kräuter & Gewürze, Pilze). Schreibt Deutsch und die englische Übersetzung.
Texte stehen als Paare L(deutsch, englisch); daraus entstehen der deutsche Eintrag und die Übersetzung."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class L(tuple):
    def __new__(cls, de, en):
        return tuple.__new__(cls, (de, en))


def res(o, i):
    if isinstance(o, L): return o[i]
    if isinstance(o, dict): return {k: res(v, i) for k, v in o.items()}
    if isinstance(o, list): return [res(v, i) for v in o]
    return o


MC = lambda de, en: {"titel": "Harold McGee: On Food and Cooking (2004)", "stelle": L(de, en)}


def U(titel, h, prinzip, warum, fix):
    return {"titel": titel, "haeufigkeit": h, "prinzip": prinzip, "warum": warum, "fix": fix}


def tree3(q1, q2):
    """Diagnose: q1 Ja → q2, Nein → Ursache 0; q2 Ja → Ursache 1, Nein → Ursache 2."""
    return {"q1": {"frage": q1, "antworten": [[L("Nein", "No"), "u0"], [L("Ja", "Yes"), "q2"]]},
            "q2": {"frage": q2, "antworten": [[L("Ja", "Yes"), "u1"], [L("Nein", "No"), "u2"]]},
            "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}}


E = []
add = E.append

# ---------------------------------------------------------------- Kaffee & Tee
add({"id": "extraktion", "typ": "begriff", "titel": L("Extraktion", "Extraction"),
     "synonyme": L(["herauslösen", "Auszug"], ["extracting", "brewing strength"]),
     "kurz": L("Wasser löst Aroma-, Säure- und Bitterstoffe aus Kaffee, Tee oder Gewürzen, zuerst die Säuren, zuletzt die Bitterstoffe.",
               "Water dissolves flavour, acid and bitter compounds out of coffee, tea or spices: the acids first, the bitter compounds last."),
     "links": ["kaffee-sauer-bitter", "tee-ziehen", "aroma-loeslichkeit"], "quellen": [MC("Kapitel Kaffee und Tee", "Chapter on coffee and tea")],
     "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "kaffee-sauer-bitter", "typ": "symptom", "titel": L("Kaffee schmeckt sauer oder bitter", "Coffee tastes sour or bitter"),
     "synonyme": L(["Kaffee sauer", "Kaffee bitter", "Espresso sauer"], ["sour coffee", "bitter coffee", "sour espresso"]),
     "kurz": L("Sauer heißt meist zu wenig herausgelöst, bitter zu viel: Mahlgrad, Brühzeit und Wassertemperatur entscheiden.",
               "Sour usually means too little was extracted, bitter too much: grind size, brewing time and water temperature decide."),
     "bild_im_kopf": L("Wie ein Teebeutel, den man zu früh oder zu spät herausnimmt: Dazwischen liegt der gute Moment.",
                       "Like a teabag taken out too early or too late: the good moment lies in between."),
     "ursachen": [
         U(L("Zu grob gemahlen oder zu kurz gebrüht", "Ground too coarse or brewed too briefly"), 3, "extraktion",
           L("Säuren lösen sich zuerst. Hört das Brühen zu früh auf, fehlen Süße und Körper, und die Säure sticht hervor.",
             "Acids dissolve first. If brewing stops too early, sweetness and body are missing and the acidity stands out."),
           [L("Feiner mahlen", "Grind finer"), L("Länger brühen", "Brew longer")]),
         U(L("Zu fein gemahlen oder zu lange gebrüht", "Ground too fine or brewed too long"), 3, "extraktion",
           L("Zuletzt lösen sich die Bitterstoffe. Zu feines Pulver oder zu lange Kontaktzeit holt sie heraus.",
             "The bitter compounds dissolve last. Too fine a grind or too long a contact time pulls them out."),
           [L("Gröber mahlen", "Grind coarser"), L("Kürzer brühen", "Brew for less time")]),
         U(L("Wasser zu kalt oder kochend", "Water too cool or boiling"), 2, "temperatur",
           L("Unter etwa 90 °C löst das Wasser zu wenig, sprudelnd kochendes Wasser holt rasch Bitteres heraus. Gut sind etwa 92–96 °C (Richtwert).",
             "Below about 90 °C the water dissolves too little; water at a rolling boil quickly pulls out bitterness. About 92–96 °C works well (as a guide)."),
           [L("Wasser kurz nach dem Kochen verwenden", "Use water just off the boil")]),
     ],
     "diagnose": tree3(L("Ist der Kaffee eher bitter als sauer?", "Is the coffee more bitter than sour?"),
                       L("Mahlst du sehr fein oder brühst du länger als üblich?", "Do you grind very fine or brew longer than usual?")),
     "links": ["extraktion", "w-kaffee", "temperatur"], "welten": ["w-kaffee"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "two cups of coffee side by side, one pale and thin, one very dark and oily, a hand grinder beside them"},
     "quellen": [MC("Kapitel Kaffee", "Chapter on coffee"), {"titel": "Specialty Coffee Association: Brewing Control Chart"}],
     "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "tee-ziehen", "typ": "technik", "titel": L("Tee richtig ziehen lassen", "Brewing tea properly"),
     "synonyme": L(["Tee aufgießen", "Grüntee Temperatur", "Tee bitter"], ["steeping tea", "green tea temperature", "bitter tea"]),
     "kurz": L("Temperatur und Zeit bestimmen, ob Tee duftet oder bitter wird: Grüntee will es kühler und kürzer als Schwarztee.",
               "Temperature and time decide whether tea is fragrant or bitter: green tea wants it cooler and shorter than black tea."),
     "bild_im_kopf": L("Wie eine Sanduhr: Ist die Zeit um, kippt der Geschmack.",
                       "Like an hourglass: once the time is up, the flavour tips over."),
     "was_passiert": L("Heißes Wasser löst zuerst die Duftstoffe und das Koffein, danach die herben Gerbstoffe. Je heißer und länger, desto mehr Gerbstoffe kommen dazu. Grüner Tee wird anders als Schwarztee nicht oxidiert und enthält empfindliche Stoffe, die bei kochendem Wasser schnell bitter schmecken.",
                       "Hot water dissolves the aroma compounds and caffeine first, then the astringent tannins. The hotter and longer, the more tannins join in. Green tea is not oxidised and contains delicate compounds that quickly taste bitter in boiling water."),
     "warum_wichtig": L("Der gleiche Tee kann mild oder bitter schmecken. Nicht die Sorte ist schuld, sondern Wasser und Uhr.",
                        "The same tea can taste mild or bitter. The fault lies not with the tea but with the water and the clock."),
     "schritte": L(["Grüntee: Wasser auf etwa 70–80 °C abkühlen lassen, 2–3 Minuten ziehen (Richtwert).",
                    "Schwarztee: sprudelnd heißes Wasser, 3–5 Minuten ziehen (Richtwert).",
                    "Kräutertee: kochendes Wasser, 5–10 Minuten, zugedeckt, damit die Duftstoffe bleiben.",
                    "Blätter oder Beutel danach herausnehmen, nicht im Wasser lassen."],
                   ["Green tea: let the water cool to about 70–80 °C, steep for 2–3 minutes (as a guide).",
                    "Black tea: water at a rolling boil, steep for 3–5 minutes (as a guide).",
                    "Herbal tea: boiling water, 5–10 minutes, covered so the aromas stay in.",
                    "Then remove the leaves or bag, do not leave them in the water."]),
     "faustregeln": L(["Für milden Grüntee: kein kochendes Wasser, sonst wird er bitter.",
                       "Tee zu bitter? Kürzer ziehen lassen statt weniger Tee nehmen."],
                      ["For mild green tea: no boiling water, or it turns bitter.",
                       "Tea too bitter? Steep it for less time rather than using less tea."]),
     "links": ["extraktion", "gerbstoffe", "w-kaffee", "x-tee-zitrone"], "welten": ["w-kaffee"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Tee", "Chapter on tea")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "milchschaum", "typ": "technik", "titel": L("Milch aufschäumen", "Frothing milk"),
     "synonyme": L(["Milchschaum", "Cappuccino Schaum", "Latte Art"], ["milk foam", "cappuccino foam", "steamed milk"]),
     "kurz": L("Milcheiweiß legt sich um eingeschlagene Luftbläschen und hält sie fest, am besten bei 55–65 °C (Richtwert).",
               "Milk proteins wrap around beaten-in air bubbles and hold them, best at 55–65 °C (as a guide)."),
     "bild_im_kopf": L("Wie Seifenblasen mit Eiweißhaut: Die Haut hält, solange sie nicht überhitzt.",
                       "Like soap bubbles with a protein skin: the skin holds as long as it does not overheat."),
     "was_passiert": L("Beim Aufschäumen wird Luft in die Milch geschlagen. Die Eiweiße der Milch legen sich um die Bläschen und bilden eine stabile Haut. Wird die Milch heißer als etwa 70 °C, verändern sich die Eiweiße zu stark: Der Schaum fällt zusammen und die Milch schmeckt gekocht.",
                       "Frothing beats air into the milk. The milk proteins gather around the bubbles and form a stable skin. If the milk gets hotter than about 70 °C, the proteins change too much: the foam collapses and the milk tastes cooked."),
     "warum_wichtig": L("Kalte, frische Milch schäumt am besten. Vollmilch gibt cremigeren Schaum, Magermilch mehr Volumen, aber trockener.",
                        "Cold, fresh milk froths best. Whole milk gives creamier foam, skimmed milk more volume but drier."),
     "schritte": L(["Kalte Milch in ein kaltes Kännchen füllen, höchstens ein Drittel voll.",
                    "Zuerst Luft einziehen, bis das Volumen etwa ein Drittel größer ist.",
                    "Dann tiefer eintauchen und die Milch wirbeln lassen, bis das Kännchen zu warm zum Anfassen wird.",
                    "Kurz aufklopfen und schwenken, damit große Blasen verschwinden."],
                   ["Pour cold milk into a cold jug, no more than a third full.",
                    "First draw in air until the volume has grown by about a third.",
                    "Then dip deeper and let the milk swirl until the jug is too hot to hold.",
                    "Tap and swirl briefly so large bubbles disappear."]),
     "faustregeln": L(["Für festen Schaum: kalte, frische Milch und nicht über etwa 65 °C erhitzen.",
                       "Schaum zerfällt sofort? Die Milch war zu heiß oder schon einmal erwärmt."],
                      ["For firm foam: cold, fresh milk, heated to no more than about 65 °C.",
                       "Foam collapses at once? The milk was too hot or had been heated before."]),
     "links": ["schaumbildung", "milch", "eiweiss-denaturierung", "w-kaffee"], "welten": ["w-kaffee", "w-milch"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Milch: Milchschaum", "Chapter on milk: milk foams")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "x-tee-zitrone", "typ": "experiment", "titel": L("Zitrone macht Schwarztee hell", "Lemon turns black tea pale"),
     "synonyme": L(["Tee Farbe Zitrone", "Tee Experiment"], ["tea colour lemon", "tea experiment"]),
     "kurz": L("Ein Spritzer Zitrone hellt Schwarztee sichtbar auf, eine Prise Natron macht ihn dunkler.",
               "A squeeze of lemon visibly lightens black tea; a pinch of baking soda makes it darker."),
     "bild_im_kopf": L("Wie eine Ampel im Glas: Die Farbe zeigt, ob es sauer oder basisch ist.",
                       "Like a traffic light in a glass: the colour shows whether it is acidic or alkaline."),
     "material": L(["Schwarztee, frisch aufgebrüht", "drei durchsichtige Gläser", "Zitronensaft", "eine Prise Natron"],
                   ["freshly brewed black tea", "three clear glasses", "lemon juice", "a pinch of baking soda"]),
     "schritte": L(["Tee gleichmäßig auf drei Gläser verteilen.",
                    "Ins erste Glas einen Teelöffel Zitronensaft geben, ins zweite eine Prise Natron, das dritte so lassen.",
                    "Umrühren und die Farben vergleichen."],
                   ["Divide the tea evenly between three glasses.",
                    "Add a teaspoon of lemon juice to the first, a pinch of baking soda to the second, leave the third as it is.",
                    "Stir and compare the colours."]),
     "beobachtung": L("Mit Zitrone wird der Tee hell orange, mit Natron dunkel rotbraun.",
                      "With lemon the tea turns light orange, with baking soda dark red-brown."),
     "erklaerung": L("Die roten und braunen Farbstoffe im Schwarztee ändern ihre Farbe mit dem pH-Wert, ähnlich wie Rotkohlsaft. Säure macht sie heller, eine Base dunkler.",
                     "The red and brown pigments in black tea change colour with the pH, much like red cabbage juice. Acid makes them lighter, a base darker."),
     "dauer": L("5 Minuten", "5 minutes"),
     "links": ["ph-wert", "indikator", "x-rotkohl-indikator", "tee-ziehen"], "welten": ["w-kaffee"],
     "visual": {"vorlage": "vergleich", "params": {"vorher": L("frischer Tee", "fresh tea"), "nachher": L("nach dem Umrühren", "after stirring"), "vergleich": [
         {"label": L("mit Zitrone", "with lemon"), "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#9a5a22"}, "nachher": {"farbe": "#d99a3e"}},
         {"label": L("ohne", "plain"), "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#9a5a22"}, "nachher": {"farbe": "#9a5a22"}},
         {"label": L("mit Natron", "with soda"), "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#9a5a22"}, "nachher": {"farbe": "#5a2a14"}}]},
         "illustration": "three glasses of black tea in different shades, light orange, amber and dark red-brown, a lemon half beside them"},
     "quellen": [MC("Kapitel Tee", "Chapter on tea")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "g-cold-brew", "typ": "gericht", "titel": L("Cold Brew", "Cold brew"),
     "synonyme": L(["kalt gebrühter Kaffee", "Cold Brew Kaffee"], ["cold brew coffee", "cold-brewed coffee"]),
     "kurz": L("Kaffee zieht viele Stunden in kaltem Wasser: Das löst weniger Säure und Bitterstoffe und schmeckt darum mild.",
               "Coffee steeps for many hours in cold water: this dissolves less acid and bitterness, so it tastes mild."),
     "bild_im_kopf": L("Wie langsames Gießen statt eines Wolkenbruchs: Es kommt weniger auf einmal, dafür sanfter.",
                       "Like slow watering instead of a cloudburst: less arrives at once, but more gently."),
     "schwierigkeit": "einsteiger",
     "schluesselmomente": [
         {"schritt": L("Kaffee grob mahlen, etwa 80–100 g auf einen Liter kaltes Wasser (Richtwert)", "Grind coffee coarsely, about 80–100 g per litre of cold water (as a guide)"),
          "warum": L("Grobes Pulver lässt sich gut abfiltern, und die lange Zeit gleicht die geringere Oberfläche aus.", "A coarse grind filters off easily, and the long time makes up for the smaller surface."), "prinzip": "extraktion"},
         {"schritt": L("12–24 Stunden im Kühlschrank ziehen lassen", "Steep in the fridge for 12–24 hours"),
          "warum": L("Kaltes Wasser löst Aromen langsam und lässt viele Säuren und Bitterstoffe zurück.", "Cold water dissolves flavours slowly and leaves many acids and bitter compounds behind."), "prinzip": "temperatur"},
         {"schritt": L("Durch einen Papierfilter abgießen", "Strain through a paper filter"),
          "warum": L("Feine Teilchen würden weiter ziehen und den Kaffee trüben.", "Fine particles would keep steeping and cloud the coffee."), "prinzip": "zeit"},
         {"schritt": L("Als Konzentrat mit Wasser oder Milch verdünnen", "Dilute the concentrate with water or milk"),
          "warum": L("Die Mischung ist stark. Verdünnt hält sie sich gekühlt etwa eine Woche (Richtwert).", "The brew is strong. Diluted, it keeps chilled for about a week (as a guide)."), "prinzip": "extraktion"}],
     "links": ["extraktion", "kaffee-sauer-bitter", "w-kaffee"], "welten": ["w-kaffee"],
     "visual": {"vorlage": "ablauf", "illustration": "a glass jar of cold brew coffee with a paper filter and a glass of iced coffee with milk"},
     "quellen": [MC("Kapitel Kaffee", "Chapter on coffee")], "status": "entwurf"})

# ---------------------------------------------------------------- Pasta
add({"id": "pasta-frisch", "typ": "technik", "titel": L("Frische Pasta machen", "Making fresh pasta"),
     "synonyme": L(["Nudelteig", "Pasta selber machen", "Eierteig"], ["pasta dough", "homemade pasta", "egg pasta"]),
     "kurz": L("Mehl und Ei werden geknetet, bis ein Glutennetz entsteht, dann ruht der Teig, damit er sich ausrollen lässt.",
               "Flour and egg are kneaded until a gluten network forms, then the dough rests so it can be rolled out."),
     "bild_im_kopf": L("Wie ein neuer Pullover, der nach dem Waschen erst entspannen muss, bevor er wieder passt.",
                       "Like a new jumper that has to relax after washing before it fits again."),
     "was_passiert": L("Beim Kneten verbinden sich die Eiweiße des Mehls zu Gluten, das Ei liefert Wasser, Fett und Farbe. Das Netz macht den Teig erst zäh und zurückschnurrend. In der Ruhezeit entspannt es sich, und das Mehl nimmt das Wasser ganz auf.",
                       "Kneading links the flour proteins into gluten; the egg provides water, fat and colour. At first the network makes the dough tough and springy. During resting it relaxes, and the flour fully absorbs the water."),
     "warum_wichtig": L("Ohne Ruhezeit reißt der Teig oder zieht sich zusammen. Frische Pasta gart in 2–4 Minuten, weil sie noch feucht ist.",
                        "Without resting, the dough tears or shrinks back. Fresh pasta cooks in 2–4 minutes because it is still moist."),
     "schritte": L(["100 g Mehl (Tipo 00 oder halb Hartweizengrieß) pro Ei abwiegen (Richtwert).",
                    "Ei in eine Mulde im Mehl geben und nach und nach einarbeiten.",
                    "8–10 Minuten kneten, bis der Teig glatt und elastisch ist.",
                    "In Folie gewickelt 30 Minuten ruhen lassen.",
                    "Dünn ausrollen, schneiden und in kräftig gesalzenem Wasser 2–4 Minuten kochen."],
                   ["Weigh 100 g flour (tipo 00 or half durum semolina) per egg (as a guide).",
                    "Put the egg into a well in the flour and work it in gradually.",
                    "Knead for 8–10 minutes until the dough is smooth and elastic.",
                    "Wrap in film and rest for 30 minutes.",
                    "Roll out thinly, cut and cook in well-salted water for 2–4 minutes."]),
     "faustregeln": L(["Teig zu trocken? Mit nassen Händen weiterkneten statt Wasser zugießen.",
                       "Teig zieht sich beim Ausrollen zurück: zugedeckt nochmals 10 Minuten ruhen lassen."],
                      ["Dough too dry? Keep kneading with wet hands rather than pouring in water.",
                       "Dough shrinks back when rolling: cover and rest for another 10 minutes."]),
     "links": ["glutenbildung", "ruhezeit", "teig-schnurrt", "w-pasta"], "welten": ["w-pasta"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Getreide: Pasta", "Chapter on grains: pasta")], "status": "entwurf", "schwierigkeit": "fortgeschritten"})

add({"id": "pasta-in-sauce", "typ": "technik", "titel": L("Pasta in der Sauce fertig garen", "Finishing pasta in the sauce"),
     "synonyme": L(["Pasta schwenken", "Pasta in der Pfanne"], ["tossing pasta", "pasta in the pan"]),
     "kurz": L("Pasta 1–2 Minuten vor dem Ende abgießen und mit etwas Nudelwasser in der Sauce fertig garen: So nimmt sie Geschmack auf und die Sauce haftet.",
               "Drain pasta 1–2 minutes early and finish it in the sauce with a little pasta water: it takes on flavour and the sauce clings."),
     "bild_im_kopf": L("Wie Brot, das man in die Suppe tunkt: Es nimmt auf, was zuletzt um es herum ist.",
                       "Like bread dipped in soup: it takes up whatever is around it last."),
     "was_passiert": L("In den letzten Minuten nimmt die Pasta noch Flüssigkeit auf. Gart sie in der Sauce statt im Wasser, saugt sie Sauce statt Wasser. Gleichzeitig gibt sie Stärke ab, die zusammen mit dem Nudelwasser Fett und Flüssigkeit zu einer sämigen Sauce bindet.",
                       "In the last minutes the pasta still absorbs liquid. If it cooks in the sauce rather than the water, it soaks up sauce rather than water. At the same time it releases starch which, together with the pasta water, binds fat and liquid into a silky sauce."),
     "warum_wichtig": L("Abgegossene Pasta mit Sauce obendrauf bleibt fade, und die Sauce rutscht ab.",
                        "Drained pasta with sauce spooned on top stays bland, and the sauce slides off."),
     "schritte": L(["Eine Tasse Nudelwasser aufheben.",
                    "Pasta 1–2 Minuten vor der Packungszeit abgießen.",
                    "In die heiße Sauce geben, einen Schuss Nudelwasser dazu.",
                    "Unter Schwenken 1–2 Minuten garen, bis die Sauce glänzt und an der Pasta haftet."],
                   ["Save a cup of pasta water.",
                    "Drain the pasta 1–2 minutes before the packet time.",
                    "Add it to the hot sauce with a splash of pasta water.",
                    "Toss and cook for 1–2 minutes until the sauce is glossy and clings to the pasta."]),
     "faustregeln": L(["Sauce zu dick? Mehr Nudelwasser. Zu dünn? Weiter schwenken, die Stärke bindet."],
                      ["Sauce too thick? More pasta water. Too thin? Keep tossing, the starch will bind it."]),
     "links": ["mantecare", "staerkeverkleisterung", "emulsion", "w-pasta"], "welten": ["w-pasta"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Getreide: Pasta", "Chapter on grains: pasta"), {"titel": "Serious Eats: The Food Lab, Pasta"}], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "pasta-zu-weich", "typ": "symptom", "titel": L("Pasta wird weich und matschig", "Pasta turns soft and mushy"),
     "synonyme": L(["Nudeln matschig", "Pasta verkocht", "Nudeln zu weich"], ["mushy pasta", "overcooked pasta", "soggy noodles"]),
     "kurz": L("Die Stärke ist zu weit aufgequollen: Die Pasta hat zu lange gekocht oder danach im Heißen weitergegart.",
               "The starch has swollen too far: the pasta cooked too long or kept cooking in the heat afterwards."),
     "bild_im_kopf": L("Wie ein Brötchen, das zu lange in der Suppe lag.", "Like a bread roll left too long in the soup."),
     "ursachen": [
         U(L("Zu lange gekocht", "Cooked too long"), 3, "staerkeverkleisterung",
           L("Die Stärke quillt weiter, bis der Kern keinen Biss mehr hat.", "The starch keeps swelling until the centre has no bite left."),
           [L("Eine Minute vor der Packungszeit probieren", "Taste a minute before the packet time")]),
         U(L("Nach dem Abgießen weitergegart", "Kept cooking after draining"), 2, "nachgaren",
           L("Heiße Pasta im Sieb oder in heißer Sauce gart weiter, auch ohne Herd.", "Hot pasta in a colander or in hot sauce keeps cooking even off the heat."),
           [L("Etwas früher abgießen", "Drain a little earlier"), L("Sofort mit der Sauce servieren", "Serve with the sauce straight away")]),
         U(L("Zu wenig sprudelndes Wasser", "Water not boiling enough"), 1, "staerke",
           L("Kommt Pasta in nur warmes Wasser, löst sich die Oberfläche, bevor sie fest wird, und wird schleimig.",
             "If pasta goes into merely hot water, the surface dissolves before it sets and turns slimy."),
           [L("Erst bei sprudelndem Kochen hineingeben", "Add only at a rolling boil")])],
     "diagnose": tree3(L("Hast du dich an die Kochzeit auf der Packung gehalten?", "Did you stick to the cooking time on the packet?"),
                       L("Stand die Pasta danach noch eine Weile im Sieb oder in der Sauce?", "Did the pasta then sit for a while in the colander or sauce?")),
     "links": ["al-dente", "pasta-in-sauce", "pasta-klebt", "w-pasta"], "welten": ["w-pasta"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "a bowl of overcooked, bloated, broken spaghetti looking soft and mushy"},
     "quellen": [MC("Kapitel Getreide: Pasta", "Chapter on grains: pasta")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "g-carbonara", "typ": "gericht", "titel": L("Spaghetti Carbonara", "Spaghetti carbonara"),
     "synonyme": L(["Carbonara", "Pasta Carbonara"], ["carbonara"]),
     "kurz": L("Eigelb, Käse und Speckfett werden mit Nudelwasser zu einer cremigen Sauce gebunden, ohne dass das Ei zu Rührei wird.",
               "Egg yolk, cheese and bacon fat are bound with pasta water into a creamy sauce without the egg turning into scrambled egg."),
     "bild_im_kopf": L("Wie Seiltanzen über einer Pfanne: Warm genug zum Binden, kühl genug, damit nichts gerinnt.",
                       "Like walking a tightrope over a pan: warm enough to bind, cool enough that nothing curdles."),
     "schwierigkeit": "fortgeschritten",
     "schluesselmomente": [
         {"schritt": L("Guanciale oder Speck langsam auslassen", "Render guanciale or bacon slowly"),
          "warum": L("Das Fett schmilzt aus und wird später Teil der Sauce, der Speck wird knusprig.", "The fat melts out and later becomes part of the sauce; the bacon turns crisp."), "prinzip": "fett-ausbraten"},
         {"schritt": L("Eigelb mit Pecorino und viel Pfeffer verrühren", "Mix egg yolks with pecorino and plenty of pepper"),
          "warum": L("Der Käse verteilt sich im Eigelb und bindet später mit.", "The cheese disperses in the yolk and helps bind later."), "prinzip": "emulsion"},
         {"schritt": L("Pasta mit etwas Nudelwasser zum Speck geben und die Pfanne vom Herd ziehen", "Add the pasta with a little pasta water to the bacon and take the pan off the heat"),
          "warum": L("Eigelb stockt ab etwa 65–70 °C. Abseits der Flamme bleibt die Sauce darunter.", "Egg yolk sets from about 65–70 °C. Off the flame the sauce stays below that."), "prinzip": "eiweiss-gerinnung"},
         {"schritt": L("Eimasse einrühren und kräftig schwenken, bis die Sauce glänzt", "Stir in the egg mixture and toss hard until the sauce is glossy"),
          "warum": L("Stärke aus dem Nudelwasser verbindet Fett, Ei und Käse zu einer Emulsion.", "Starch from the pasta water binds fat, egg and cheese into an emulsion."), "prinzip": "mantecare"}],
     "links": ["eiweiss-gerinnung", "mantecare", "emulsion", "pasta-in-sauce", "w-pasta"], "welten": ["w-pasta"],
     "visual": {"vorlage": "ablauf", "illustration": "a plate of spaghetti carbonara with glossy sauce, crisp guanciale and black pepper"},
     "quellen": [MC("Kapitel Eier", "Chapter on eggs")], "status": "entwurf"})

# ---------------------------------------------------------------- Geflügel
add({"id": "g-brathaehnchen", "typ": "gericht", "titel": L("Brathähnchen", "Roast chicken"),
     "synonyme": L(["Poulet im Ofen", "ganzes Huhn braten", "Güggeli"], ["whole roast chicken", "roasted chicken"]),
     "kurz": L("Knusprige Haut und saftiges Fleisch zugleich: Die Haut braucht Trockenheit und Hitze, die Brust darf nicht zu heiß werden.",
               "Crisp skin and juicy meat at once: the skin needs dryness and heat, the breast must not get too hot."),
     "bild_im_kopf": L("Wie ein Mantel und sein Träger: Der Mantel soll trocken und knusprig sein, der Träger warm, aber nicht verschwitzt.",
                       "Like a coat and its wearer: the coat should be dry and crisp, the wearer warm but not sweaty."),
     "schwierigkeit": "fortgeschritten",
     "schluesselmomente": [
         {"schritt": L("Am Vortag rundum salzen und unbedeckt im Kühlschrank lagern", "Salt all over the day before and store uncovered in the fridge"),
          "warum": L("Das Salz würzt bis innen und hält Saft im Fleisch, die Haut trocknet an der Luft.", "The salt seasons right through and keeps juice in the meat; the skin dries in the air."), "prinzip": "trockensalzen"},
         {"schritt": L("Bei 200–220 °C braten, nicht zudecken (Richtwert)", "Roast at 200–220 °C, uncovered (as a guide)"),
          "warum": L("Trockene Hitze lässt das Fett der Haut ausbraten und die Oberfläche bräunen.", "Dry heat renders the fat in the skin and browns the surface."), "prinzip": "maillard-reaktion"},
         {"schritt": L("Mit dem Thermometer messen: Brust mindestens 70 °C, Keule besser 75–80 °C", "Check with a thermometer: breast at least 70 °C, leg better at 75–80 °C"),
          "warum": L("Die Keule hat mehr Bindegewebe und wird mit etwas mehr Hitze zarter, die Brust bei zu viel trocken.", "The leg has more connective tissue and gets more tender with a little more heat; too much makes the breast dry."), "prinzip": "kerntemperatur"},
         {"schritt": L("10 Minuten ruhen lassen, dann zerlegen", "Rest for 10 minutes, then carve"),
          "warum": L("Der Saft verteilt sich wieder im Fleisch und läuft beim Schneiden weniger aus.", "The juices redistribute in the meat and run out less when carving."), "prinzip": "ruhen-lassen"}],
     "links": ["trockensalzen", "haut-nicht-knusprig", "kerntemperatur", "flach-aufschneiden", "w-gefluegel"], "welten": ["w-gefluegel"],
     "visual": {"vorlage": "ablauf", "illustration": "a golden roast chicken with crisp skin in a cast iron pan with lemon and thyme"},
     "quellen": [MC("Kapitel Fleisch: Geflügel", "Chapter on meat: poultry")], "status": "entwurf"})

add({"id": "haut-nicht-knusprig", "typ": "symptom", "titel": L("Geflügelhaut wird nicht knusprig", "Poultry skin won't crisp"),
     "synonyme": L(["Hähnchenhaut labbrig", "Pouletschenkel Haut weich", "Haut gummig"], ["flabby chicken skin", "rubbery skin", "soggy skin"]),
     "kurz": L("Die Haut ist zu feucht oder liegt im Dampf, darum kann ihr Fett nicht ausbraten.",
               "The skin is too moist or sits in steam, so its fat cannot render."),
     "bild_im_kopf": L("Wie Wäsche im Bad nach dem Duschen: In feuchter Luft wird nichts trocken.",
                       "Like washing hung in the bathroom after a shower: nothing dries in damp air."),
     "ursachen": [
         U(L("Haut feucht", "Skin wet"), 3, "verdampfen",
           L("Solange Wasser auf der Haut ist, bleibt sie bei 100 °C und bräunt nicht.", "As long as there is water on the skin, it stays at 100 °C and does not brown."),
           [L("Trocken tupfen", "Pat dry"), L("Über Nacht unbedeckt im Kühlschrank trocknen", "Dry uncovered in the fridge overnight")]),
         U(L("Im eigenen Dampf gegart", "Cooked in its own steam"), 2, "feuchtigkeit",
           L("Eine enge Form oder viel Gemüse drumherum gibt Dampf ab, der die Haut weich hält.", "A tight dish or lots of vegetables around it give off steam that keeps the skin soft."),
           [L("Auf einem Gitter oder mit Abstand garen", "Cook on a rack or with space around it"), L("Ohne Deckel", "No lid")]),
         U(L("Zu wenig Hitze am Schluss", "Too little heat at the end"), 2, "fett-ausbraten",
           L("Die Fettschicht unter der Haut muss ausbraten, sonst bleibt die Haut zäh.", "The fat layer under the skin must render, or the skin stays chewy."),
           [L("Zum Schluss 10 Minuten bei hoher Hitze oder Grill", "Finish for 10 minutes on high heat or under the grill")])],
     "diagnose": tree3(L("War die Haut vor dem Garen ganz trocken?", "Was the skin completely dry before cooking?"),
                       L("Lag das Geflügel eng in der Form oder zwischen viel Gemüse?", "Was the bird packed tightly in the dish or among lots of vegetables?")),
     "links": ["trocken-tupfen", "trockensalzen", "fett-ausbraten", "g-brathaehnchen", "w-gefluegel"], "welten": ["w-gefluegel"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "a pale chicken leg with flabby, wrinkled skin sitting in liquid in a crowded roasting dish"},
     "quellen": [MC("Kapitel Fleisch: Geflügel", "Chapter on meat: poultry")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "pouletbrust-trocken", "typ": "symptom", "titel": L("Pouletbrust wird trocken", "Chicken breast turns out dry"),
     "synonyme": L(["Hähnchenbrust trocken", "Hühnerbrust zäh", "Pouletbrüstli"], ["dry chicken breast", "tough chicken breast"]),
     "kurz": L("Die magere Brust verliert schnell Saft, wenn sie deutlich über 70 °C gart oder ungleich dick ist.",
               "The lean breast loses juice quickly if it cooks well beyond 70 °C or is uneven in thickness."),
     "bild_im_kopf": L("Wie ein Handtuch auf der Heizung: Eben noch feucht, Minuten später steif und trocken.", "Like a towel on the radiator: damp a moment ago, stiff and dry minutes later."),
     "ursachen": [
         U(L("Zu lange gegart", "Cooked too long"), 3, "eiweiss-denaturierung",
           L("Je heißer das Eiweiß wird, desto stärker zieht es sich zusammen und presst Saft heraus. Brust hat kaum Fett, das das ausgleicht.",
             "The hotter the protein gets, the more it contracts and squeezes out juice. Breast has hardly any fat to make up for it."),
           [L("Thermometer: bei 70 °C herausnehmen", "Thermometer: take it out at 70 °C")]),
         U(L("Ungleich dick", "Uneven thickness"), 2, "waermeleitung",
           L("Bis das dicke Ende gar ist, ist das dünne längst übergart.", "By the time the thick end is cooked, the thin end is long overcooked."),
           [L("Flach klopfen oder waagrecht halbieren", "Pound flat or slice in half horizontally")]),
         U(L("Nicht vorgesalzen", "Not salted ahead"), 1, "wasserbindung-salz",
           L("Salz, das eine Weile einwirkt, hilft dem Fleisch, Wasser zu halten.", "Salt given time to work helps the meat hold on to water."),
           [L("Einige Stunden vorher salzen oder kurz in Salzlake legen", "Salt a few hours ahead or brine briefly")])],
     "diagnose": tree3(L("Hast du die Temperatur gemessen und bei etwa 70 °C aufgehört?", "Did you measure the temperature and stop at about 70 °C?"),
                       L("War die Brust an einem Ende deutlich dicker?", "Was the breast much thicker at one end?")),
     "links": ["kerntemperatur", "fleisch-trocken", "lake", "w-gefluegel"], "welten": ["w-gefluegel"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "a sliced chicken breast, dry and fibrous, on a wooden board"},
     "quellen": [MC("Kapitel Fleisch: Geflügel", "Chapter on meat: poultry")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "flach-aufschneiden", "typ": "technik", "titel": L("Geflügel flach aufschneiden", "Spatchcocking poultry"),
     "synonyme": L(["Spatchcock", "Hähnchen flach", "Rückgrat entfernen"], ["spatchcock", "butterflied chicken", "removing the backbone"]),
     "kurz": L("Ohne Rückgrat liegt das Huhn flach: Es gart schneller und gleichmäßiger, und die ganze Haut liegt oben.",
               "Without its backbone the chicken lies flat: it cooks faster and more evenly, and all of the skin faces up."),
     "bild_im_kopf": L("Wie eine Landkarte, die man auf dem Tisch ausbreitet: Flach sieht man alles auf einmal.", "Like a map spread out on the table: laid flat, everything is in view at once."),
     "was_passiert": L("Ein ganzes Huhn ist rund und ungleich dick. Liegt es flach, sind Brust und Keulen ähnlich weit von der Hitze entfernt. Die Keulen werden gar, bevor die Brust austrocknet.",
                       "A whole chicken is round and uneven in thickness. Laid flat, breast and legs are a similar distance from the heat. The legs cook through before the breast dries out."),
     "warum_wichtig": L("Die Garzeit sinkt deutlich, ungefähr um ein Drittel (Richtwert), und die Haut wird überall knusprig.",
                        "Cooking time drops considerably, by roughly a third (as a guide), and the skin crisps all over."),
     "schritte": L(["Huhn mit der Brust nach unten hinlegen.",
                    "Mit einer Geflügelschere links und rechts entlang dem Rückgrat schneiden und es herausnehmen.",
                    "Umdrehen und mit dem Handballen kräftig auf das Brustbein drücken, bis es flach liegt.",
                    "Haut trocken tupfen, salzen und auf einem Blech braten."],
                   ["Lay the chicken breast side down.",
                    "With poultry shears, cut along both sides of the backbone and remove it.",
                    "Turn it over and press firmly on the breastbone with the heel of your hand until it lies flat.",
                    "Pat the skin dry, salt and roast on a tray."]),
     "faustregeln": L(["Rückgrat aufheben: Es gibt einen guten Fond."], ["Keep the backbone: it makes a good stock."]),
     "links": ["g-brathaehnchen", "gleichmaessig-gar", "fond", "w-gefluegel"], "welten": ["w-gefluegel"], "visual": {"vorlage": "ablauf"},
     "quellen": [{"titel": "Serious Eats: Spatchcocked Chicken"}], "status": "entwurf", "schwierigkeit": "fortgeschritten"})

# ---------------------------------------------------------------- Fisch
add({"id": "g-lachs-haut", "typ": "gericht", "titel": L("Lachs auf der Haut gebraten", "Pan-fried salmon, skin on"),
     "synonyme": L(["Lachs braten", "knusprige Fischhaut", "Lachsfilet"], ["crispy salmon skin", "pan-seared salmon", "salmon fillet"]),
     "kurz": L("Die Haut schützt das zarte Fleisch und wird knusprig, wenn der Fisch fast die ganze Zeit auf ihr brät.",
               "The skin protects the delicate flesh and turns crisp if the fish cooks on it for almost the whole time."),
     "bild_im_kopf": L("Wie ein Topflappen, der zugleich knusprig wird: Die Haut schützt und brät mit.",
                       "Like an oven glove that turns crisp: the skin protects and fries at the same time."),
     "schwierigkeit": "einsteiger",
     "schluesselmomente": [
         {"schritt": L("Haut trocken tupfen und mit dem Messerrücken abstreifen", "Pat the skin dry and scrape it with the back of a knife"),
          "warum": L("So wenig Wasser wie möglich auf der Haut: Sonst klebt sie und wird nicht knusprig.", "As little water on the skin as possible: otherwise it sticks and won't crisp."), "prinzip": "verdampfen"},
         {"schritt": L("In gut vorgeheiztes Öl legen und die ersten Sekunden leicht andrücken", "Lay it in well-heated oil and press lightly for the first few seconds"),
          "warum": L("Die Haut zieht sich in der Hitze zusammen und wölbt sich. Andrücken hält sie flach auf dem Pfannenboden.", "The skin contracts in the heat and curls. Pressing keeps it flat on the pan."), "prinzip": "pfanne-vorheizen"},
         {"schritt": L("Etwa drei Viertel der Zeit auf der Haut braten, bis das Fleisch von unten zur Hälfte hell geworden ist", "Fry about three quarters of the time skin side down, until the flesh has turned opaque halfway up"),
          "warum": L("Die Haut isoliert: Das Fleisch gart sanft von unten, während die Haut bräunt.", "The skin insulates: the flesh cooks gently from below while the skin browns."), "prinzip": "waermeleitung"},
         {"schritt": L("Nur kurz wenden und bei etwa 50 °C Kerntemperatur herausnehmen (Richtwert)", "Turn only briefly and take it off at about 50 °C core temperature (as a guide)"),
          "warum": L("Lachs bleibt so in der Mitte saftig und leicht glasig.", "That way salmon stays juicy and slightly translucent in the middle."), "prinzip": "kerntemperatur"}],
     "links": ["fisch-klebt", "fisch-garprobe", "pfanne-vorheizen", "w-fisch"], "welten": ["w-fisch"],
     "visual": {"vorlage": "ablauf", "illustration": "a salmon fillet with golden crisp skin in a steel pan, a lemon wedge beside it"},
     "quellen": [MC("Kapitel Fisch", "Chapter on fish")], "status": "entwurf"})

add({"id": "fisch-garprobe", "typ": "technik", "titel": L("Erkennen, wann Fisch gar ist", "Telling when fish is done"),
     "synonyme": L(["Fisch gar", "Garprobe Fisch", "Fisch Kerntemperatur"], ["is the fish cooked", "fish doneness", "fish core temperature"]),
     "kurz": L("Fisch ist gar, wenn das Fleisch von glasig zu hell wechselt und sich leicht in Lamellen teilen lässt, meist bei 50–60 °C im Kern (Richtwert).",
               "Fish is done when the flesh turns from translucent to opaque and separates easily into flakes, usually at 50–60 °C at the core (as a guide)."),
     "bild_im_kopf": L("Wie ein Stapel Spielkarten: Gar lässt er sich mit einem Fingerdruck in einzelne Blätter auffächern.", "Like a stack of playing cards: once cooked, a touch of the finger fans it into separate layers."),
     "was_passiert": L("Fischeiweiß verändert sich bei viel niedrigeren Temperaturen als Fleisch vom Land. Das Bindegewebe ist schwach und löst sich früh. Darum ist Fisch schnell gar und schnell übergart: Wenige Grad entscheiden zwischen saftig und trocken.",
                       "Fish protein changes at much lower temperatures than the meat of land animals. Its connective tissue is weak and gives way early. So fish is quickly cooked and quickly overcooked: a few degrees decide between juicy and dry."),
     "warum_wichtig": L("Weil Fisch nachgart, nimmt man ihn heraus, wenn er in der Mitte gerade noch leicht glasig ist.",
                        "Because fish keeps cooking, take it off when the middle is still just slightly translucent."),
     "schritte": L(["An der dicksten Stelle mit einer Gabel leicht hineindrücken.",
                    "Teilt sich das Fleisch in Lamellen und ist innen nur noch ein Hauch glasig, ist es fertig.",
                    "Mit Thermometer: Lachs bei etwa 50 °C, Weißfisch bei 55–60 °C (Richtwert)."],
                   ["Press gently into the thickest part with a fork.",
                    "If the flesh separates into flakes and is only a touch translucent inside, it is done.",
                    "With a thermometer: salmon at about 50 °C, white fish at 55–60 °C (as a guide)."]),
     "faustregeln": L(["Lieber eine Minute zu früh als zu spät: Fisch gart nach."], ["Better a minute too early than too late: fish keeps cooking."]),
     "links": ["kerntemperatur", "nachgaren", "fisch-zerfaellt", "g-lachs-haut", "w-fisch"], "welten": ["w-fisch"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Fisch", "Chapter on fish")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "fisch-riecht", "typ": "symptom", "titel": L("Fisch riecht stark", "Fish smells strong"),
     "synonyme": L(["Fischgeruch", "Fisch stinkt", "Fischgeruch entfernen"], ["fishy smell", "fish smells", "removing fishy smell"]),
     "kurz": L("Frischer Fisch riecht nach Meer. Der typische Fischgeruch entsteht erst, wenn Bakterien Stoffe im Fleisch abbauen.",
               "Fresh fish smells of the sea. The typical fishy smell only develops when bacteria break down substances in the flesh."),
     "bild_im_kopf": L("Wie Milch, die erst nach ein paar Tagen sauer riecht: Der Geruch zeigt das Alter.",
                       "Like milk that only smells sour after a few days: the smell shows the age."),
     "ursachen": [
         U(L("Nicht mehr frisch", "No longer fresh"), 3, "keimwachstum",
           L("Meeresfisch enthält einen geruchlosen Stoff, den Bakterien zu stark riechendem Trimethylamin abbauen. Je älter, desto mehr.",
             "Sea fish contains an odourless substance that bacteria break down into strong-smelling trimethylamine. The older the fish, the more of it."),
           [L("Frisch kaufen und am selben Tag zubereiten", "Buy fresh and cook the same day")]),
         U(L("Zu warm gelagert", "Stored too warm"), 2, "keimwachstum",
           L("Wärme lässt die Bakterien schneller arbeiten.", "Warmth makes the bacteria work faster."),
           [L("Im kältesten Fach auf Eis lagern", "Store on ice in the coldest part of the fridge")]),
         U(L("Geruch bleibt an Händen und Pfanne", "The smell clings to hands and pan"), 1, "saeure",
           L("Trimethylamin ist eine schwache Base. Säure wie Zitrone bindet es und mildert den Geruch.", "Trimethylamine is a weak base. Acid such as lemon binds it and softens the smell."),
           [L("Mit Zitronensaft beträufeln", "Sprinkle with lemon juice"), L("Hände mit Zitrone oder Essig waschen", "Wash hands with lemon or vinegar")])],
     "diagnose": tree3(L("Roch der Fisch schon beim Auspacken stark?", "Did the fish already smell strong when unwrapped?"),
                       L("Lag er länger als einen Tag im Kühlschrank?", "Was it in the fridge for more than a day?")),
     "links": ["saeure", "keimwachstum", "w-fisch"], "welten": ["w-fisch"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "a whole fish on crushed ice next to lemon halves and a small bowl of vinegar"},
     "quellen": [MC("Kapitel Fisch: Geruch", "Chapter on fish: odour")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "x-fisch-zitrone", "typ": "experiment", "titel": L("Säure gart Fisch ohne Hitze", "Acid cooks fish without heat"),
     "synonyme": L(["Ceviche Experiment", "Fisch in Zitrone"], ["ceviche experiment", "fish in lime juice"]),
     "kurz": L("Rohe Fischwürfel in Zitronen- oder Limettensaft werden in einer halben Stunde weiß und fest, wie gegart.",
               "Raw fish cubes in lemon or lime juice turn white and firm within half an hour, as if cooked."),
     "bild_im_kopf": L("Wie Eiweiß in der heißen Pfanne, nur ohne Pfanne: Die Säure übernimmt die Arbeit der Hitze.",
                       "Like egg white in a hot pan, but without the pan: the acid does the work of the heat."),
     "material": L(["ein Stück sehr frischer Weißfisch", "Zitronen- oder Limettensaft", "Wasser", "zwei kleine Schalen"],
                   ["a piece of very fresh white fish", "lemon or lime juice", "water", "two small bowls"]),
     "schritte": L(["Fisch in kleine Würfel schneiden.",
                    "Eine Hälfte mit Zitronensaft bedecken, die andere mit Wasser.",
                    "Zugedeckt 30 Minuten in den Kühlschrank stellen und dann vergleichen."],
                   ["Cut the fish into small cubes.",
                    "Cover one half with lemon juice and the other with water.",
                    "Cover and chill for 30 minutes, then compare."]),
     "beobachtung": L("Im Saft ist der Fisch außen weiß und fest, im Wasser glasig und weich geblieben.",
                      "In the juice the fish is white and firm on the outside; in the water it has stayed translucent and soft."),
     "erklaerung": L("Säure verändert die Eiweiße ähnlich wie Hitze: Sie entfalten sich und verbinden sich neu. Darum wirkt der Fisch gegart. Keime tötet Säure aber nicht so sicher wie Hitze.",
                     "Acid changes the proteins much as heat does: they unfold and link up anew. That is why the fish looks cooked. But acid does not kill germs as reliably as heat."),
     "sicherheit": L("Nur mit sehr frischem Fisch, für Kinder nur zum Anschauen. Nicht essen, wenn die Frische unsicher ist.",
                     "Only with very fresh fish; for children, for looking at only. Do not eat it if you are unsure how fresh it is."),
     "dauer": L("30 Minuten", "30 minutes"),
     "links": ["saeure-denaturierung", "eiweiss-denaturierung", "w-fisch"], "welten": ["w-fisch"],
     "visual": {"vorlage": "vergleich", "params": {"vorher": L("roh", "raw"), "nachher": L("nach 30 Minuten", "after 30 minutes"), "vergleich": [
         {"label": L("in Zitronensaft", "in lemon juice"), "gefaess": "schuessel", "inhalt": "scheiben", "vorher": {"farbe": "#f0c9c0"}, "nachher": {"farbe": "#f6f2ea"}},
         {"label": L("in Wasser", "in water"), "gefaess": "schuessel", "inhalt": "scheiben", "vorher": {"farbe": "#f0c9c0"}, "nachher": {"farbe": "#eec4ba"}}]},
         "illustration": "two small bowls of raw fish cubes, one turned white in lime juice, one translucent pink in water, lime halves beside them"},
     "quellen": [MC("Kapitel Fisch: Ceviche", "Chapter on fish: ceviche")], "status": "entwurf", "schwierigkeit": "einsteiger"})

# ---------------------------------------------------------------- Reis & Getreide
add({"id": "reis-quellmethode", "typ": "technik", "titel": L("Reis kochen mit der Quellmethode", "Cooking rice by absorption"),
     "synonyme": L(["Reis kochen", "Reis Wassermenge", "Reis Verhältnis"], ["how to cook rice", "rice water ratio", "absorption method"]),
     "kurz": L("Reis gart in genau so viel Wasser, wie er aufnehmen kann, und quillt danach zugedeckt fertig.",
               "Rice cooks in exactly as much water as it can absorb, then finishes swelling under the lid."),
     "bild_im_kopf": L("Wie ein Garten, den man genau so viel gießt, wie die Erde schlucken kann.", "Like a garden watered with exactly as much as the soil can drink."),
     "was_passiert": L("Die Stärke im Korn nimmt Wasser auf und verkleistert. Ist das Wasser aufgesogen, verteilt sich die Feuchtigkeit in der Ruhezeit gleichmäßig im Korn. Waschen spült losen Stärkestaub ab, der die Körner sonst verklebt.",
                       "The starch in the grain absorbs water and gelatinises. Once the water is taken up, the moisture spreads evenly through the grain during resting. Rinsing washes off loose starch dust that would otherwise glue the grains together."),
     "warum_wichtig": L("Kein Abgießen, keine verlorenen Nährstoffe, und der Reis wird locker statt matschig.",
                        "No draining, no lost nutrients, and the rice comes out fluffy rather than mushy."),
     "schritte": L(["Reis waschen, bis das Wasser fast klar ist.",
                    "Mit Wasser im Verhältnis von etwa 1 : 1,5 aufkochen, Basmati eher 1 : 1,25 (Richtwert).",
                    "Deckel drauf, auf kleinster Stufe 12–15 Minuten garen.",
                    "Vom Herd nehmen und 10 Minuten zugedeckt ruhen lassen, dann auflockern."],
                   ["Rinse the rice until the water runs almost clear.",
                    "Bring to the boil with water at a ratio of about 1 : 1.5, basmati more like 1 : 1.25 (as a guide).",
                    "Cover and cook on the lowest heat for 12–15 minutes.",
                    "Take off the heat and rest, covered, for 10 minutes, then fluff up."]),
     "faustregeln": L(["Für lockeren Reis: während des Garens den Deckel nicht heben, der Dampf gart mit."],
                      ["For fluffy rice: do not lift the lid while it cooks, the steam is part of the cooking."]),
     "links": ["staerkeverkleisterung", "reis-matschig", "quellen", "w-getreide"], "welten": ["w-getreide"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Getreide: Reis", "Chapter on grains: rice")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "g-polenta", "typ": "gericht", "titel": L("Polenta", "Polenta"),
     "synonyme": L(["Maisgrieß", "Bramata", "Ribelmais"], ["cornmeal porridge", "maize meal"]),
     "kurz": L("Maisgrieß quillt in viel Flüssigkeit langsam zu einem cremigen Brei: Rühren verhindert Klumpen, Zeit macht ihn weich.",
               "Cornmeal swells slowly in plenty of liquid into a creamy porridge: stirring prevents lumps, time makes it soft."),
     "bild_im_kopf": L("Wie trockene Erde nach einem langen Landregen: Sie wird weich und sämig.", "Like dry earth after a long steady rain: it turns soft and creamy."),
     "schwierigkeit": "einsteiger",
     "schluesselmomente": [
         {"schritt": L("Grieß unter Rühren in kochendes Salzwasser oder Brühe einrieseln, etwa 1 : 4 für weiche Polenta (Richtwert)", "Rain the cornmeal into boiling salted water or stock while stirring, about 1 : 4 for soft polenta (as a guide)"),
          "warum": L("Jedes Körnchen soll einzeln ins Wasser kommen. Ein Klumpen verkleistert außen und bleibt innen trocken.", "Each grain should enter the water separately. A lump gelatinises on the outside and stays dry inside."), "prinzip": "staerkeverkleisterung"},
         {"schritt": L("Bei kleiner Hitze 30–45 Minuten garen und ab und zu rühren", "Cook on low heat for 30–45 minutes, stirring now and then"),
          "warum": L("Grober Mais braucht Zeit, bis die Stärke im Inneren aufgequollen ist.", "Coarse maize needs time for the starch inside to swell."), "prinzip": "quellen"},
         {"schritt": L("Zum Schluss Butter und Käse einrühren", "Stir in butter and cheese at the end"),
          "warum": L("Fett und Käse machen die Polenta glatt und runden den Geschmack ab.", "Fat and cheese make the polenta smooth and round off the flavour."), "prinzip": "cremig"},
         {"schritt": L("Reste auf ein Blech streichen, fest werden lassen und anbraten", "Spread leftovers on a tray, let them set and fry them"),
          "warum": L("Beim Abkühlen ordnet sich die Stärke neu und wird fest.", "As it cools, the starch rearranges and sets."), "prinzip": "retrogradation"}],
     "links": ["staerkeverkleisterung", "quellen", "retrogradation", "w-getreide"], "welten": ["w-getreide"],
     "visual": {"vorlage": "ablauf", "illustration": "a copper pot of golden creamy polenta with a wooden spoon and grated cheese"},
     "quellen": [MC("Kapitel Getreide: Mais", "Chapter on grains: maize")], "status": "entwurf"})

add({"id": "g-milchreis", "typ": "gericht", "titel": L("Milchreis", "Rice pudding"),
     "synonyme": L(["Reisbrei", "Milchreis Rezept", "Risotto dolce"], ["creamy rice pudding", "stovetop rice pudding"]),
     "kurz": L("Rundkornreis gibt in Milch viel Stärke ab und bindet sie zu einem cremigen Brei, wenn er langsam gart.",
               "Short-grain rice releases plenty of starch into milk and binds it into a creamy pudding when it cooks slowly."),
     "bild_im_kopf": L("Wie ein Wollknäuel, das sich langsam in einer warmen Decke auflöst.", "Like a ball of wool slowly melting into a warm blanket."),
     "schwierigkeit": "einsteiger",
     "schluesselmomente": [
         {"schritt": L("Rundkornreis verwenden und nicht waschen", "Use short-grain rice and do not rinse it"),
          "warum": L("Rundkornreis hat viel Stärke, die leicht austritt. Genau sie macht die Milch cremig.", "Short-grain rice has a lot of starch that escapes easily. That is exactly what makes the milk creamy."), "prinzip": "staerkeverkleisterung"},
         {"schritt": L("Bei kleiner Hitze 30–40 Minuten köcheln und oft rühren", "Simmer gently for 30–40 minutes, stirring often"),
          "warum": L("Milcheiweiß und Milchzucker setzen sich am Boden ab und brennen bei starker Hitze leicht an.", "Milk proteins and lactose settle on the bottom and catch easily on high heat."), "prinzip": "milch"},
         {"schritt": L("Zucker erst gegen Ende zugeben", "Add the sugar towards the end"),
          "warum": L("Zucker bindet Wasser und bremst das Aufquellen der Stärke.", "Sugar binds water and slows the starch from swelling."), "prinzip": "zucker-feuchtigkeit"},
         {"schritt": L("Etwas flüssiger vom Herd nehmen, als er sein soll", "Take it off the heat a little runnier than it should be"),
          "warum": L("Beim Abkühlen dickt er deutlich nach.", "It thickens noticeably as it cools."), "prinzip": "retrogradation"}],
     "links": ["staerkeverkleisterung", "milch", "w-getreide", "w-suesses"], "welten": ["w-getreide", "w-suesses"],
     "visual": {"vorlage": "ablauf", "illustration": "a bowl of creamy rice pudding dusted with cinnamon sugar, with a spoon"},
     "quellen": [MC("Kapitel Getreide: Reis", "Chapter on grains: rice")], "status": "entwurf"})

# ---------------------------------------------------------------- Hülsenfrüchte (neue Welt)
add({"id": "w-huelsenfruechte", "typ": "welt", "titel": L("Hülsenfrüchte", "Pulses"),
     "synonyme": L(["Bohnen", "Linsen", "Kichererbsen", "Erbsen"], ["beans", "lentils", "chickpeas", "peas"]),
     "kurz": L("Getrocknete Bohnen, Linsen und Kichererbsen brauchen Wasser, Zeit und Hitze, bis Schale und Zellwände weich werden.",
               "Dried beans, lentils and chickpeas need water, time and heat before their skins and cell walls soften."),
     "bild_im_kopf": L("Wie ein Samen im Frühling: Erst Wasser, dann wird er wieder lebendig und weich.", "Like a seed in spring: first water, then it comes back to life and softens."),
     "was_passiert": L("Beim Einweichen nehmen die getrockneten Samen Wasser auf. Beim Kochen lösen sich die Kittstoffe zwischen den Zellen (Pektin), die Stärke verkleistert. Säure und Kalk halten die Zellwände fest, Natron und Salz machen sie weicher.",
                       "Soaking lets the dried seeds take up water. Cooking dissolves the glue between the cells (pectin) and gelatinises the starch. Acid and calcium keep the cell walls firm; baking soda and salt soften them."),
     "warum_wichtig": L("Wer weiß, was Hülsenfrüchte weich macht und was sie hart hält, braucht nie mehr stundenlang auf zähe Bohnen zu warten.",
                        "Knowing what softens pulses and what keeps them hard means never again waiting for hours on tough beans."),
     "faustregeln": L(["Bohnen und Kichererbsen einweichen, Linsen nicht.",
                       "Säure wie Tomate oder Wein erst zugeben, wenn sie weich sind.",
                       "Rote Bohnen immer mindestens 10 Minuten sprudelnd kochen."],
                      ["Soak beans and chickpeas, not lentils.",
                       "Add acid such as tomato or wine only once they are soft.",
                       "Always boil kidney beans hard for at least 10 minutes."]),
     "links": ["huelsenfruechte-einweichen", "bohnen-nicht-weich", "phasin", "g-hummus", "kalzium-pektin"],
     "visual": {"vorlage": "keine", "illustration": "small piles of dried beans, lentils and chickpeas in linen sacks and a wooden scoop"},
     "quellen": [MC("Kapitel Hülsenfrüchte", "Chapter on legumes")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "huelsenfruechte-einweichen", "typ": "technik", "titel": L("Hülsenfrüchte einweichen", "Soaking pulses"),
     "synonyme": L(["Bohnen einweichen", "Kichererbsen einweichen", "über Nacht einweichen"], ["soaking beans", "soaking chickpeas", "overnight soak"]),
     "kurz": L("Getrocknete Bohnen und Kichererbsen über Nacht in Salzwasser einweichen: Sie garen schneller, gleichmäßiger und platzen weniger.",
               "Soak dried beans and chickpeas overnight in salted water: they cook faster, more evenly and burst less."),
     "bild_im_kopf": L("Wie Rosinen im Rum: Sie werden prall, bevor die eigentliche Arbeit beginnt.", "Like raisins in rum: they plump up before the real work begins."),
     "was_passiert": L("Die getrockneten Samen nehmen beim Einweichen etwa ihr eigenes Gewicht an Wasser auf. Salz im Wasser tauscht Kalk in der Schale aus, dadurch wird sie weicher. Ein Teil der schwer verdaulichen Zucker geht ins Wasser über.",
                       "During soaking the dried seeds take up roughly their own weight in water. Salt in the water swaps out calcium in the skin, which softens it. Some of the hard-to-digest sugars pass into the water."),
     "warum_wichtig": L("Uneingeweichte Bohnen garen außen weich und bleiben innen hart, und die Schalen reißen.",
                        "Unsoaked beans turn soft on the outside but stay hard inside, and the skins split."),
     "schritte": L(["Hülsenfrüchte verlesen und abspülen.",
                    "In der dreifachen Menge Wasser mit etwa 1 TL Salz pro Liter einweichen, 8–12 Stunden (Richtwert).",
                    "Einweichwasser weggießen und mit frischem Wasser weich kochen.",
                    "Linsen und Spalterbsen brauchen kein Einweichen."],
                   ["Pick over the pulses and rinse them.",
                    "Soak in three times their volume of water with about 1 tsp salt per litre, for 8–12 hours (as a guide).",
                    "Pour off the soaking water and cook until soft in fresh water.",
                    "Lentils and split peas need no soaking."]),
     "faustregeln": L(["Hartes Wasser? Eine Prise Natron ins Einweichwasser."], ["Hard water? Add a pinch of baking soda to the soaking water."]),
     "mythos": {"behauptung": L("Salz macht Bohnen hart.", "Salt makes beans tough."),
                "richtig": L("Stimmt nicht. Salz im Einweichwasser macht die Schale sogar weicher. Hart halten sie Säure und Kalk.", "Not true. Salt in the soaking water actually softens the skin. What keeps them hard is acid and calcium.")},
     "links": ["bohnen-nicht-weich", "kalzium-pektin", "natron", "w-huelsenfruechte"], "welten": ["w-huelsenfruechte"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Hülsenfrüchte", "Chapter on legumes"), {"titel": "Serious Eats: The Food Lab, Beans"}], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "phasin", "typ": "begriff", "titel": L("Phasin", "Phasin"),
     "synonyme": L(["rohe Bohnen giftig", "Lektine"], ["raw beans toxic", "lectins"]),
     "kurz": L("Ein Eiweiß in rohen Bohnen, vor allem roten Kidneybohnen, das Übelkeit und Erbrechen auslöst. Mindestens 10 Minuten sprudelndes Kochen macht es unschädlich, Garen unter dem Siedepunkt reicht nicht.",
               "A protein in raw beans, especially red kidney beans, that causes nausea and vomiting. At least 10 minutes at a rolling boil makes it harmless; cooking below boiling point is not enough."),
     "links": ["w-huelsenfruechte", "bohnen-nicht-weich"], "quellen": [{"titel": "U.S. Food and Drug Administration: Bad Bug Book, Phytohaemagglutinin"}],
     "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "g-hummus", "typ": "gericht", "titel": L("Hummus", "Hummus"),
     "synonyme": L(["Kichererbsenpüree", "Hummus selber machen"], ["chickpea dip", "homemade hummus"]),
     "kurz": L("Sehr weich gekochte Kichererbsen, Sesampaste und Zitrone werden zu einer glatten, luftigen Emulsion.",
               "Very soft-cooked chickpeas, sesame paste and lemon become a smooth, airy emulsion."),
     "bild_im_kopf": L("Wie ein Daunenkissen aus Kichererbsen: Je feiner und luftiger, desto weicher.", "Like a down pillow made of chickpeas: the finer and airier, the softer."),
     "schwierigkeit": "einsteiger",
     "schluesselmomente": [
         {"schritt": L("Eingeweichte Kichererbsen mit einer Prise Natron kochen, bis sie fast zerfallen", "Cook soaked chickpeas with a pinch of baking soda until almost falling apart"),
          "warum": L("Natron löst die Zellwände und Schalen, die sonst körnig bleiben.", "Baking soda loosens the cell walls and skins, which would otherwise stay grainy."), "prinzip": "pektin-abbau"},
         {"schritt": L("Tahini mit Zitronensaft verrühren", "Mix tahini with lemon juice"),
          "warum": L("Die Sesampaste dickt erst ein und wird dann cremig: Wasser und Fett verbinden sich.", "The sesame paste first thickens, then turns creamy: water and fat combine."), "prinzip": "emulsion"},
         {"schritt": L("Noch warme Kichererbsen dazugeben und lange pürieren", "Add the chickpeas while still warm and blend for a long time"),
          "warum": L("Warm sind sie weicher und lassen sich feiner zerkleinern.", "Warm, they are softer and break down more finely."), "prinzip": "staerkeverkleisterung"},
         {"schritt": L("Mit etwas Eiswasser aufschlagen", "Whip with a little iced water"),
          "warum": L("Das Wasser lockert die Masse auf und macht sie hell und fluffig.", "The water loosens the mixture and makes it pale and fluffy."), "prinzip": "emulsion"}],
     "links": ["huelsenfruechte-einweichen", "natron", "emulsion", "w-huelsenfruechte"], "welten": ["w-huelsenfruechte"],
     "visual": {"vorlage": "ablauf", "illustration": "a shallow bowl of smooth hummus with a swirl of olive oil, paprika and whole chickpeas"},
     "quellen": [{"titel": "Serious Eats: The Food Lab, Hummus"}], "status": "entwurf"})

# ---------------------------------------------------------------- Obst (neue Welt)
add({"id": "w-obst", "typ": "welt", "titel": L("Obst & Früchte", "Fruit"),
     "synonyme": L(["Früchte", "Äpfel", "Beeren", "Bananen"], ["fruit", "apples", "berries", "bananas"]),
     "kurz": L("Obst reift, bräunt und geliert nach den gleichen Regeln: Reifegas, Enzyme, Säure und Pektin.",
               "Fruit ripens, browns and sets by the same rules: ripening gas, enzymes, acid and pectin."),
     "bild_im_kopf": L("Wie eine Zündschnur: Einmal angezündet, brennt sie auch nach dem Pflücken weiter.", "Like a fuse: once lit, it keeps burning even after picking."),
     "was_passiert": L("Viele Früchte reifen nach der Ernte weiter. Ein Gas namens Ethylen setzt das in Gang: Stärke wird zu Zucker, das Fruchtfleisch wird weich. Angeschnitten bräunen viele Früchte durch ein Enzym. Ihr Pektin lässt sich mit Zucker und Säure zu Konfitüre binden.",
                       "Many fruits keep ripening after harvest. A gas called ethylene sets this off: starch turns into sugar and the flesh softens. Once cut, many fruits brown through an enzyme. Their pectin can be set into jam with sugar and acid."),
     "warum_wichtig": L("Wer die Regeln kennt, lagert Obst länger, lässt es gezielt nachreifen und hält es hell.",
                        "Knowing the rules means storing fruit longer, ripening it on purpose and keeping it bright."),
     "faustregeln": L(["Äpfel getrennt von anderem Obst lagern, außer es soll nachreifen.",
                       "Angeschnittenes Obst mit Zitrone beträufeln."],
                      ["Store apples apart from other fruit, unless you want it to ripen.",
                       "Sprinkle cut fruit with lemon."]),
     "links": ["ethylen", "obst-lagern", "enzym-braeunung", "gelbildung-pektin", "g-apfelmus"],
     "visual": {"vorlage": "keine", "illustration": "a still life of apples, pears, a bunch of grapes and berries in a woven basket"},
     "quellen": [MC("Kapitel Früchte", "Chapter on fruit")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "ethylen", "typ": "begriff", "titel": L("Ethylen", "Ethylene"),
     "synonyme": L(["Reifegas"], ["ripening gas"]),
     "kurz": L("Ein Gas, das reifende Früchte wie Äpfel, Bananen, Avocados und Tomaten abgeben. Es lässt Früchte in der Nähe schneller reifen und welken.",
               "A gas given off by ripening fruit such as apples, bananas, avocados and tomatoes. It makes nearby fruit ripen and wilt faster."),
     "links": ["obst-lagern", "x-avocado-apfel", "w-obst"], "quellen": [MC("Kapitel Früchte: Reifung", "Chapter on fruit: ripening")],
     "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "obst-lagern", "typ": "technik", "titel": L("Obst richtig lagern", "Storing fruit properly"),
     "synonyme": L(["Obst Kühlschrank", "Bananen lagern", "Tomaten Kühlschrank"], ["fruit in the fridge", "storing bananas", "tomatoes in the fridge"]),
     "kurz": L("Manches Obst gehört in den Kühlschrank, manches nicht: Es kommt darauf an, ob es nachreift und wie kälteempfindlich es ist.",
               "Some fruit belongs in the fridge, some does not: it depends on whether it keeps ripening and how sensitive it is to cold."),
     "bild_im_kopf": L("Wie eine Wohngemeinschaft: Wer laut ist, braucht ein eigenes Zimmer.", "Like a shared flat: whoever is noisy needs a room of their own."),
     "was_passiert": L("Früchte atmen nach der Ernte weiter. Kälte bremst das, schadet aber Früchten aus warmen Gegenden: Bananen werden schwarz, Tomaten mehlig und fade. Äpfel und reife Bananen geben Ethylen ab und beschleunigen das Reifen ihrer Nachbarn.",
                       "Fruit keeps breathing after harvest. Cold slows this down but harms fruit from warm climates: bananas turn black, tomatoes mealy and bland. Apples and ripe bananas give off ethylene and speed up the ripening of their neighbours."),
     "warum_wichtig": L("Richtig gelagert hält Obst oft doppelt so lange und schmeckt besser.", "Stored properly, fruit often keeps twice as long and tastes better."),
     "schritte": L(["Kühlschrank: Beeren, Kirschen, Trauben und reife Äpfel, ungewaschen.",
                    "Raumtemperatur: Bananen, Tomaten, Avocados, Steinobst und Zitrusfrüchte, bis sie reif sind.",
                    "Äpfel getrennt lagern, damit sie anderes Obst nicht vorzeitig reifen lassen.",
                    "Beeren erst kurz vor dem Essen waschen."],
                   ["Fridge: berries, cherries, grapes and ripe apples, unwashed.",
                    "Room temperature: bananas, tomatoes, avocados, stone fruit and citrus until they are ripe.",
                    "Keep apples separate so they do not ripen other fruit too early.",
                    "Wash berries only just before eating."]),
     "faustregeln": L(["Tomaten nie in den Kühlschrank, wenn sie nach etwas schmecken sollen."],
                      ["Never put tomatoes in the fridge if you want them to taste of anything."]),
     "links": ["ethylen", "x-avocado-apfel", "w-obst"], "welten": ["w-obst"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Früchte: Lagerung", "Chapter on fruit: storage")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "x-avocado-apfel", "typ": "experiment", "titel": L("Ein Apfel lässt Avocados reifen", "An apple ripens avocados"),
     "synonyme": L(["Avocado nachreifen", "Ethylen Experiment", "Avocado Papiertüte"], ["ripening avocados", "ethylene experiment", "avocado paper bag"]),
     "kurz": L("Eine harte Avocado in einer Papiertüte mit einem Apfel wird ein bis zwei Tage früher weich als eine allein.",
               "A hard avocado in a paper bag with an apple softens a day or two sooner than one on its own."),
     "bild_im_kopf": L("Wie ein Gähnen, das ansteckt: Eine reife Frucht bringt die anderen auf Trab.", "Like a contagious yawn: one ripe fruit gets the others going."),
     "material": L(["zwei gleich harte Avocados", "ein Apfel", "eine Papiertüte"], ["two equally hard avocados", "an apple", "a paper bag"]),
     "schritte": L(["Eine Avocado mit dem Apfel in die Papiertüte geben und verschließen.",
                    "Die andere Avocado daneben offen liegen lassen.",
                    "Jeden Tag beide sanft drücken und vergleichen."],
                   ["Put one avocado in the paper bag with the apple and close it.",
                    "Leave the other avocado uncovered next to it.",
                    "Gently squeeze both each day and compare."]),
     "beobachtung": L("Die Avocado in der Tüte gibt nach ein bis drei Tagen deutlich früher nach.", "The avocado in the bag gives noticeably sooner, after one to three days."),
     "erklaerung": L("Der Apfel gibt das Reifegas Ethylen ab. In der Tüte sammelt es sich und setzt das Reifen der Avocado schneller in Gang.",
                     "The apple gives off the ripening gas ethylene. It collects in the bag and starts the avocado ripening sooner."),
     "dauer": L("1–3 Tage", "1–3 days"),
     "links": ["ethylen", "obst-lagern", "w-obst"], "welten": ["w-obst"],
     "visual": {"vorlage": "vergleich", "params": {"vorher": L("Tag 1", "day 1"), "nachher": L("nach 2 Tagen", "after 2 days"), "vergleich": [
         {"label": L("mit Apfel in der Tüte", "with apple in bag"), "gefaess": "teller", "inhalt": "keins", "vorher": {"farbe": "#5f7a34"}, "nachher": {"farbe": "#2f3a1e"}},
         {"label": L("allein", "on its own"), "gefaess": "teller", "inhalt": "keins", "vorher": {"farbe": "#5f7a34"}, "nachher": {"farbe": "#56702f"}}]},
         "illustration": "two avocados, one in a brown paper bag with a red apple, the other lying beside it"},
     "quellen": [MC("Kapitel Früchte: Reifung", "Chapter on fruit: ripening")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "g-apfelmus", "typ": "gericht", "titel": L("Apfelmus", "Apple sauce"),
     "synonyme": L(["Apfelkompott", "Apfelmus selber machen"], ["apple purée", "stewed apples"]),
     "kurz": L("Äpfel zerfallen in wenig Flüssigkeit zu Mus, weil Hitze das Pektin zwischen den Zellen löst.",
               "Apples collapse into sauce in a little liquid because heat dissolves the pectin between the cells."),
     "bild_im_kopf": L("Wie ein Wollpullover in der Kochwäsche: Die Maschen lösen sich, alles fällt in sich zusammen.", "Like a wool jumper on a hot wash: the stitches loosen and everything collapses."),
     "schwierigkeit": "einsteiger",
     "schluesselmomente": [
         {"schritt": L("Mürbe Sorten wie Boskoop nehmen, für Stücke eher feste Sorten", "Use soft varieties such as Bramley-style cookers; for chunks, firmer ones"),
          "warum": L("Sorten mit lockeren Zellen zerfallen leicht, feste behalten ihre Form.", "Varieties with loose cells break down easily; firm ones keep their shape."), "prinzip": "pektin-abbau"},
         {"schritt": L("Geschälte Stücke sofort mit etwas Zitronensaft mischen", "Toss peeled pieces with a little lemon juice straight away"),
          "warum": L("Säure bremst das Enzym, das die Schnittflächen braun färbt.", "Acid slows the enzyme that turns cut surfaces brown."), "prinzip": "enzym-braeunung"},
         {"schritt": L("Mit wenig Wasser zugedeckt weich dünsten", "Steam until soft with a little water under a lid"),
          "warum": L("Hitze löst das Pektin, die Äpfel geben selbst genug Saft ab.", "Heat dissolves the pectin, and the apples give off enough juice themselves."), "prinzip": "pektin-abbau"},
         {"schritt": L("Pürieren oder durch ein Sieb streichen, erst dann süßen", "Purée or press through a sieve, only then sweeten"),
          "warum": L("So lässt sich die Süße an die Säure der Äpfel anpassen.", "That way the sweetness can be matched to the apples' acidity."), "prinzip": "abschmecken-saeure"}],
     "links": ["pektin-abbau", "enzym-braeunung", "w-obst"], "welten": ["w-obst", "w-suesses"],
     "visual": {"vorlage": "ablauf", "illustration": "a bowl of homemade apple sauce with a cinnamon stick and two whole apples"},
     "quellen": [MC("Kapitel Früchte", "Chapter on fruit")], "status": "entwurf"})

# ---------------------------------------------------------------- Kräuter & Gewürze (neue Welt)
add({"id": "w-kraeuter-gewuerze", "typ": "welt", "titel": L("Kräuter & Gewürze", "Herbs & spices"),
     "synonyme": L(["Kräuter", "Gewürze", "Basilikum", "Pfeffer"], ["herbs", "spices", "basil", "pepper"]),
     "kurz": L("Kräuter und Gewürze tragen ihr Aroma in flüchtigen Duftstoffen: Hitze, Fett und Zeit entscheiden, wie viel davon im Essen ankommt.",
               "Herbs and spices carry their flavour in volatile aroma compounds: heat, fat and time decide how much of it reaches the food."),
     "bild_im_kopf": L("Wie Parfüm: Ein Hauch wirkt, offen stehen gelassen verfliegt es.", "Like perfume: a touch works wonders, left open it fades."),
     "was_passiert": L("Die Duftstoffe sitzen in kleinen Öldrüsen der Blätter und Samen. Viele lösen sich besser in Fett als in Wasser. Frische Kräuter verlieren sie beim langen Kochen, getrocknete Gewürze entfalten sie erst in Hitze und Fett.",
                       "The aroma compounds sit in tiny oil glands in leaves and seeds. Many dissolve better in fat than in water. Fresh herbs lose them with long cooking, while dried spices only release them in heat and fat."),
     "warum_wichtig": L("Wann und wie man würzt, macht oft mehr aus als die Menge.", "When and how you season often matters more than how much."),
     "faustregeln": L(["Harte Kräuter wie Rosmarin und Thymian früh, zarte wie Basilikum und Petersilie am Schluss.",
                       "Ganze Gewürze kurz in Fett rösten, bevor Flüssigkeit dazukommt."],
                      ["Woody herbs such as rosemary and thyme early, tender ones such as basil and parsley at the end.",
                       "Toast whole spices briefly in fat before liquid goes in."]),
     "links": ["aroma-loeslichkeit", "aroma-blooming", "gewuerze", "kraeuter-frisch-halten", "g-pesto"],
     "visual": {"vorlage": "keine", "illustration": "bunches of fresh basil, rosemary and parsley next to a mortar with peppercorns and star anise"},
     "quellen": [MC("Kapitel Kräuter und Gewürze", "Chapter on herbs and spices")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "kraeuter-frisch-halten", "typ": "technik", "titel": L("Frische Kräuter lagern", "Keeping fresh herbs"),
     "synonyme": L(["Kräuter frisch halten", "Basilikum lagern", "Petersilie aufbewahren"], ["storing fresh herbs", "keeping basil", "storing parsley"]),
     "kurz": L("Zarte Kräuter wie Blumen ins Wasser stellen, harte in ein feuchtes Tuch, und Basilikum nie in den Kühlschrank.",
               "Stand tender herbs in water like flowers, wrap woody ones in a damp cloth, and never put basil in the fridge."),
     "bild_im_kopf": L("Wie ein Blumenstrauß: Mit Wasser im Glas hält er Tage, ohne welkt er in Stunden.", "Like a bunch of flowers: in a glass of water it lasts days, without it wilts in hours."),
     "was_passiert": L("Geschnittene Kräuter verlieren Wasser und welken. Zarte Kräuter ziehen über die Stiele Wasser nach. Basilikum stammt aus warmen Gegenden: Unter etwa 10 °C werden seine Zellen geschädigt, und die Blätter färben sich schwarz.",
                       "Cut herbs lose water and wilt. Tender herbs draw water back up through their stems. Basil comes from warm climates: below about 10 °C its cells are damaged and the leaves turn black."),
     "warum_wichtig": L("Richtig gelagert halten Kräuter eine Woche statt zwei Tage.", "Stored properly, herbs last a week instead of two days."),
     "schritte": L(["Petersilie, Koriander und Dill: Stiele anschneiden und in ein Glas Wasser stellen, locker mit einem Beutel abdecken, in den Kühlschrank.",
                    "Basilikum: genauso, aber bei Raumtemperatur, nicht in der Sonne.",
                    "Rosmarin, Thymian, Salbei: in ein leicht feuchtes Tuch wickeln, in den Kühlschrank.",
                    "Erst kurz vor dem Gebrauch waschen und schneiden."],
                   ["Parsley, coriander and dill: trim the stems, stand them in a glass of water, cover loosely with a bag, refrigerate.",
                    "Basil: the same, but at room temperature, out of the sun.",
                    "Rosemary, thyme, sage: wrap in a slightly damp cloth and refrigerate.",
                    "Wash and chop only just before use."]),
     "faustregeln": L(["Mit scharfem Messer schneiden: Ein stumpfes quetscht die Blätter, sie werden dunkel."],
                      ["Cut with a sharp knife: a blunt one bruises the leaves and they darken."]),
     "links": ["kraeuter-schwarz", "enzym-braeunung", "w-kraeuter-gewuerze"], "welten": ["w-kraeuter-gewuerze"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Kräuter", "Chapter on herbs")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "kraeuter-schwarz", "typ": "symptom", "titel": L("Kräuter werden schwarz", "Herbs turn black"),
     "synonyme": L(["Basilikum schwarz", "Kräuter dunkel", "Pesto wird dunkel"], ["basil turns black", "herbs darken", "pesto turns dark"]),
     "kurz": L("Kälte, Quetschen oder Luft zerstören die Zellen der Blätter, und Enzyme färben sie dunkel.",
               "Cold, bruising or air damage the leaf cells, and enzymes turn them dark."),
     "bild_im_kopf": L("Wie ein blauer Fleck auf einem Apfel: Wo die Zellen verletzt sind, wird es dunkel.", "Like a bruise on an apple: where the cells are hurt, it turns dark."),
     "ursachen": [
         U(L("Zu kalt gelagert", "Stored too cold"), 3, "temperatur",
           L("Basilikum und andere Kräuter aus warmen Gegenden nehmen unter etwa 10 °C Schaden.", "Basil and other herbs from warm climates suffer damage below about 10 °C."),
           [L("Basilikum bei Raumtemperatur im Wasserglas", "Keep basil at room temperature in a glass of water")]),
         U(L("Mit stumpfem Messer geschnitten oder gehackt", "Cut or chopped with a blunt knife"), 2, "enzym-braeunung",
           L("Gequetschte Zellen setzen ein Enzym frei, das mit Sauerstoff braune Farbstoffe bildet.", "Bruised cells release an enzyme that forms brown pigments with oxygen."),
           [L("Scharfes Messer, nur einmal durchschneiden", "Sharp knife, cut through only once")]),
         U(L("Zu lange an der Luft", "Too long in the air"), 2, "enzym-braeunung",
           L("Geschnittene Kräuter und Pesto dunkeln an der Luft nach.", "Chopped herbs and pesto darken in the air."),
           [L("Erst kurz vor dem Servieren schneiden", "Chop just before serving"), L("Pesto mit Öl bedecken", "Cover pesto with oil")])],
     "diagnose": tree3(L("Lagen die Kräuter im Kühlschrank?", "Were the herbs in the fridge?"),
                       L("Wurden sie fein gehackt oder mit stumpfem Messer geschnitten?", "Were they finely chopped or cut with a blunt knife?")),
     "links": ["kraeuter-frisch-halten", "enzym-braeunung", "g-pesto", "w-kraeuter-gewuerze"], "welten": ["w-kraeuter-gewuerze"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "a sprig of basil with blackened, limp leaves on a cold plate"},
     "quellen": [MC("Kapitel Kräuter", "Chapter on herbs")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "g-pesto", "typ": "gericht", "titel": L("Pesto alla genovese", "Pesto alla genovese"),
     "synonyme": L(["Basilikumpesto", "Pesto selber machen"], ["basil pesto", "homemade pesto"]),
     "kurz": L("Basilikum, Pinienkerne, Käse und Öl werden zu einer grünen Paste: Je schonender man zerkleinert, desto grüner und duftender bleibt sie.",
               "Basil, pine nuts, cheese and oil become a green paste: the gentler the chopping, the greener and more fragrant it stays."),
     "bild_im_kopf": L("Wie Grünes im Sommerregen: Je weniger man es zerdrückt, desto frischer bleibt es.", "Like greenery in summer rain: the less it is crushed, the fresher it stays."),
     "schwierigkeit": "einsteiger",
     "schluesselmomente": [
         {"schritt": L("Pinienkerne ohne Fett goldbraun rösten", "Toast the pine nuts golden in a dry pan"),
          "warum": L("Röstaromen machen das Pesto runder.", "Roasted flavours make the pesto rounder."), "prinzip": "maillard-reaktion"},
         {"schritt": L("Basilikum im Mörser oder mit kurzen Mixer-Stößen zerkleinern", "Crush the basil in a mortar or with short pulses of the blender"),
          "warum": L("Ein lange laufender Mixer erwärmt die Blätter: Die Enzyme arbeiten schneller und das Pesto wird dunkel.", "A blender left running warms the leaves: the enzymes work faster and the pesto turns dark."), "prinzip": "enzym-braeunung"},
         {"schritt": L("Wer es leuchtend grün will: Blätter 10 Sekunden blanchieren und abschrecken", "For bright green: blanch the leaves for 10 seconds and refresh in iced water"),
          "warum": L("Die kurze Hitze schaltet die bräunenden Enzyme ab, das Grün bleibt.", "The brief heat switches off the browning enzymes, and the green stays."), "prinzip": "blanchieren"},
         {"schritt": L("Käse und Öl erst zum Schluss unterrühren und mit Öl bedecken", "Stir in cheese and oil at the end and cover with oil"),
          "warum": L("Die Ölschicht hält Luft fern und bremst das Nachdunkeln.", "The layer of oil keeps air out and slows darkening."), "prinzip": "oxidation-fett"}],
     "links": ["kraeuter-schwarz", "enzym-braeunung", "blanchieren", "w-kraeuter-gewuerze"], "welten": ["w-kraeuter-gewuerze", "w-saucen"],
     "visual": {"vorlage": "ablauf", "illustration": "a marble mortar filled with bright green basil pesto, pine nuts and basil leaves beside it"},
     "quellen": [MC("Kapitel Kräuter: Pesto", "Chapter on herbs: pesto")], "status": "entwurf"})

# ---------------------------------------------------------------- Pilze (neue Welt)
add({"id": "w-pilze", "typ": "welt", "titel": L("Pilze", "Mushrooms"),
     "synonyme": L(["Champignons", "Steinpilze", "Pilze braten"], ["button mushrooms", "porcini", "frying mushrooms"]),
     "kurz": L("Pilze bestehen zu rund 90 % aus Wasser und bringen viel Umami mit: Erst wenn das Wasser weg ist, werden sie braun und würzig.",
               "Mushrooms are around 90 % water and bring plenty of umami: only once the water has gone do they turn brown and savoury."),
     "bild_im_kopf": L("Wie ein Schwamm voller Brühe: Erst ausdrücken, dann rösten.", "Like a sponge full of broth: squeeze it out first, then roast."),
     "was_passiert": L("Pilze geben beim Erhitzen zuerst viel Wasser ab und schrumpfen. Solange sie im eigenen Saft liegen, garen sie bei 100 °C. Ist das Wasser verdampft, bräunen sie in Fett und entwickeln Röstaromen. Ihre Zellwände bleiben dabei fest, darum werden sie kaum matschig.",
                       "When heated, mushrooms first release a lot of water and shrink. As long as they sit in their own juice, they cook at 100 °C. Once the water has evaporated, they brown in fat and develop roasted flavours. Their cell walls stay firm, so they rarely turn mushy."),
     "warum_wichtig": L("Wer Pilze geduldig brät, bis das Wasser weg ist, bekommt Geschmack statt grauer Gummistücke.",
                        "Frying mushrooms patiently until the water is gone gives flavour instead of grey rubbery pieces."),
     "faustregeln": L(["Pilze in einer großen Pfanne mit Platz braten.", "Salz erst, wenn sie braun sind."],
                      ["Fry mushrooms in a large pan with room to spare.", "Salt only once they have browned."]),
     "links": ["pilze-braten", "pilze-waessrig", "umami", "verdampfen"],
     "visual": {"vorlage": "keine", "illustration": "a basket of mixed mushrooms, button mushrooms, porcini and chanterelles on a linen cloth"},
     "quellen": [MC("Kapitel Pilze", "Chapter on mushrooms")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "pilze-braten", "typ": "technik", "titel": L("Pilze braten", "Frying mushrooms"),
     "synonyme": L(["Champignons braten", "Pilze anbraten", "Pilze waschen"], ["frying button mushrooms", "sautéing mushrooms", "washing mushrooms"]),
     "kurz": L("Pilze erst ihr Wasser abgeben lassen, dann in Fett bräunen und zum Schluss salzen.",
               "Let mushrooms give up their water first, then brown them in fat and salt at the end."),
     "bild_im_kopf": L("Wie Pfützen nach dem Regen: Erst müssen sie verdunsten, dann wird der Boden warm.", "Like puddles after rain: they have to evaporate before the ground warms up."),
     "was_passiert": L("In der heißen Pfanne treten zuerst Wasser und Saft aus. Kocht dieser Saft weg, steigt die Temperatur und die Pilze bräunen. Zu viele Pilze auf einmal kühlen die Pfanne, und sie kochen im eigenen Saft.",
                       "In the hot pan, water and juice come out first. Once this juice boils away, the temperature rises and the mushrooms brown. Too many mushrooms at once cool the pan, and they stew in their own juice."),
     "warum_wichtig": L("Der Unterschied zwischen grau-gummigen und goldbraunen, würzigen Pilzen liegt nur in Platz, Hitze und Geduld.",
                        "The difference between grey, rubbery mushrooms and golden, savoury ones lies only in space, heat and patience."),
     "schritte": L(["Pilze kurz abbrausen oder abreiben und gut trocken tupfen.",
                    "In einer großen Pfanne bei hoher Hitze in einer Lage braten, notfalls in zwei Portionen.",
                    "Nicht ständig rühren: Erst wenden, wenn die Unterseite braun ist.",
                    "Zum Schluss Butter, Knoblauch, Kräuter und Salz zugeben."],
                   ["Rinse or wipe the mushrooms briefly and pat them dry well.",
                    "Fry in a single layer in a large pan over high heat, in two batches if needed.",
                    "Do not stir constantly: turn only once the underside is brown.",
                    "Add butter, garlic, herbs and salt at the end."]),
     "faustregeln": L(["Für braune Pilze: erst salzen, wenn sie gebräunt sind, sonst ziehen sie Wasser."],
                      ["For brown mushrooms: salt only once they have browned, otherwise they draw water."]),
     "mythos": {"behauptung": L("Pilze darf man nicht waschen, sie saugen sich voll.", "Never wash mushrooms, they soak up water."),
                "richtig": L("Stimmt kaum. Kurz abgebraust nehmen sie nur wenig Wasser auf. Wichtig ist, sie danach trocken zu tupfen.", "Hardly true. Rinsed briefly, they take up very little water. What matters is patting them dry afterwards.")},
     "links": ["pilze-waessrig", "osmose", "maillard-reaktion", "w-pilze"], "welten": ["w-pilze"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Pilze", "Chapter on mushrooms"), {"titel": "Serious Eats: The Food Lab, Mushrooms"}], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "pilze-waessrig", "typ": "symptom", "titel": L("Pilze werden wässrig und grau", "Mushrooms turn watery and grey"),
     "synonyme": L(["Champignons wässrig", "Pilze schwimmen im Saft", "Pilze gummig"], ["watery mushrooms", "mushrooms swimming in juice", "rubbery mushrooms"]),
     "kurz": L("Die Pilze kochen im eigenen Saft, weil die Pfanne zu voll, zu kühl oder zu früh gesalzen war.",
               "The mushrooms stew in their own juice because the pan was too full, too cool or salted too early."),
     "bild_im_kopf": L("Wie zu viele Leute in einer Sauna: Es wird feucht statt heiß.", "Like too many people in a sauna: it gets steamy instead of hot."),
     "ursachen": [
         U(L("Pfanne überfüllt", "Pan overcrowded"), 3, "verdampfen",
           L("Viele Pilze geben mehr Wasser ab, als auf einmal verdampfen kann.", "Lots of mushrooms give off more water than can evaporate at once."),
           [L("In einer Lage braten", "Fry in a single layer"), L("In Portionen arbeiten", "Work in batches")]),
         U(L("Zu früh gesalzen", "Salted too early"), 2, "osmose",
           L("Salz zieht Wasser aus den Pilzen, bevor sie bräunen können.", "Salt draws water out of the mushrooms before they can brown."),
           [L("Erst am Schluss salzen", "Salt only at the end")]),
         U(L("Zu wenig Hitze", "Not enough heat"), 2, "pfanne-vorheizen",
           L("In einer lauwarmen Pfanne tritt der Saft aus, verdampft aber nicht.", "In a lukewarm pan the juice comes out but does not evaporate."),
           [L("Pfanne richtig vorheizen", "Preheat the pan properly")])],
     "diagnose": tree3(L("Lagen die Pilze in einer einzigen Lage in der Pfanne?", "Were the mushrooms in a single layer in the pan?"),
                       L("Hast du gleich zu Beginn gesalzen?", "Did you salt right at the start?")),
     "links": ["pilze-braten", "osmose", "verdampfen", "w-pilze"], "welten": ["w-pilze"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "grey, shrunken sliced mushrooms swimming in liquid in a crowded frying pan"},
     "quellen": [MC("Kapitel Pilze", "Chapter on mushrooms")], "status": "entwurf", "schwierigkeit": "einsteiger"})

# ---------------------------------------------------------------- schreiben
NEW_W = {"w-huelsenfruechte": ["bohnen-nicht-weich", "x-bohnen-gruen", "kalzium-pektin"],
         "w-obst": ["enzym-braeunung", "x-apfel-braun", "g-konfituere", "l-apfelpektin", "gelbildung-pektin", "pektin"],
         "w-kraeuter-gewuerze": ["gewuerze", "gewuerze-roesten", "aroma-blooming", "aroma-loeslichkeit", "knoblauch", "schaerfe"],
         "w-pilze": ["umami", "glutamat"]}

if __name__ == "__main__":
    known = {f[:-5] for f in os.listdir(f"{ROOT}/content/entries")} | {e["id"] for e in E}
    ml = json.load(open(f"{ROOT}/content/master-list.json"))
    have = {m["id"] for m in ml["eintraege"]}
    for e in E:
        de = res(e, 0)
        miss = [l for l in de.get("links", []) if l not in known]
        if miss: print("Unbekannte Links in", de["id"], miss)
        de["links"] = [l for l in de.get("links", []) if l in known]
        json.dump(de, open(f"{ROOT}/content/entries/{de['id']}.json", "w"), ensure_ascii=False, indent=2)
        if de["id"] not in have:
            ml["eintraege"].append({"id": de["id"], "typ": de["typ"], "titel": de["titel"], "status": "entwurf", "pilot": False, "links": de["links"],
                                    "welten": de.get("welten", []), "synonyme": de.get("synonyme", []), "visual": {"vorlage": de.get("visual", {}).get("vorlage", "keine")}, "verlinkt_von": []})
    ml["anzahl"] = len(ml["eintraege"])
    json.dump(ml, open(f"{ROOT}/content/master-list.json", "w"), ensure_ascii=False, indent=2)
    # Englisch: Textfelder wie das Werkzeug sie herausziehen, Werte aus der englischen Fassung
    ids = [e["id"] for e in E]
    ex = json.loads(subprocess.check_output([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "extract", *ids], cwd=ROOT))
    def pick(shape, src):
        if isinstance(shape, dict) and "params" in src and "vorlage" in src:
            par = dict(src["params"])
            if "vergleich" in par: par["vergleich"] = [f["label"] for f in par["vergleich"]]
            src = {**src, **par}
        if isinstance(shape, dict): return {k: (src[k] if k == "synonyme" else pick(v, src[k])) for k, v in shape.items()}
        if isinstance(shape, list): return [pick(v, src[i]) for i, v in enumerate(shape)]
        return src[0] if isinstance(src, list) and isinstance(shape, str) else src
    batch = {e["id"]: pick(ex[e["id"]], res(e, 1)) for e in E}
    path = f"{ROOT}/content/en/_batch_welten2.json"
    json.dump(batch, open(path, "w"), ensure_ascii=False, indent=1)
    subprocess.check_call([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "apply", path], cwd=ROOT)
    os.remove(path)
    # Neue Welten auch bei passenden bestehenden Einträgen eintragen (hinten, die erste Welt bleibt)
    for w, ids2 in NEW_W.items():
        for i in ids2:
            p = f"{ROOT}/content/entries/{i}.json"
            if not os.path.exists(p): continue
            x = json.load(open(p))
            if w not in x.setdefault("welten", []):
                x["welten"].append(w)
                json.dump(x, open(p, "w"), ensure_ascii=False, indent=2); open(p, "a").write("\n")
    print(len(E), "Einträge geschrieben")
