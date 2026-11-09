"""Geräte & Werkzeug (9. November 2026): neue Welt w-geraete mit Airfryer, Induktion, Mikrowelle, Schnellkochtopf,
Gusseisen, beschichteter Pfanne, Pizzastein und -stahl, Messer, Wok und dem Experiment Eis in der Mikrowelle.
Bestehende Geräte-Einträge bekommen die Welt dazu. Texte als Paare L(deutsch, englisch)."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_batch_welten2 import L, res, MC, ROOT  # noqa: E402

E = []
add = E.append

NOVA_AIR = {"titel": "PBS NOVA: How air fryers work, scientifically speaking", "url": "https://www.pbs.org/wgbh/nova/article/how-air-fryers-work-physics-convection"}
INDUKTION = {"titel": "Explain that Stuff: How do induction cooktops work?", "url": "https://www.explainthatstuff.com/induction-cooktops.html"}
MIKRO_SAFE = {"titel": "University of Nebraska–Lincoln: Microwave safety", "url": "https://food.unl.edu/article/microwave-safety/"}
DRUCK = {"titel": "Wikipedia: Pressure cooking", "url": "https://en.wikipedia.org/wiki/Pressure_cooking"}
VT_GUSS = {"titel": "Virginia Tech: Food scientist busts cast-iron myths (2024)", "url": "https://news.vt.edu/articles/2024/08/cast-iron-myths.html"}
ATK_GUSS = {"titel": "America's Test Kitchen: Busting cast-iron myths", "url": "https://www.americastestkitchen.com/lessons/articles/2355-busting-cast-iron-myths"}
PTFE = {"titel": "Poison Control (National Capital Poison Center): Teflon flu", "url": "https://www.poison.org/articles/teflon-flu"}
KA_STEEL = {"titel": "King Arthur Baking: Pizza steel vs. stone (2026)", "url": "https://www.kingarthurbaking.com/blog/2026/07/17/pizza-steel-vs-stone"}
ONION = {"titel": "Washington Times: Sharper blades could help reduce onion-slicing tears (Cornell-Studie, 2025)", "url": "https://www.washingtontimes.com/news/2025/may/21/sharper-blades-could-help-reduce-onion-slicing-tears-scientists/"}
HONE = {"titel": "Misen: Honing vs. sharpening", "url": "https://misen.com/blogs/news/honing-vs-sharpening"}
ATK_WOK = {"titel": "Cook's Illustrated: The science of stir-frying in a wok", "url": "https://www.americastestkitchen.com/cooksillustrated/articles/2189-the-science-of-stir-frying-in-a-wok"}
GERAET = MC("Kapitel Kochgeschirr und Wärmequellen", "Chapter on cookware and heat sources")


def T(id, titel, syn, kurz, bild, was, warum, schritte, regeln, links, illu, quellen, mythos=None, schw="einsteiger", welten=("w-geraete",)):
    e = {"id": id, "typ": "technik", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild, "was_passiert": was, "warum_wichtig": warum,
         "schritte": schritte, "faustregeln": regeln, "links": links, "welten": list(welten), "visual": {"vorlage": "ablauf", "illustration": illu},
         "quellen": quellen, "status": "entwurf", "schwierigkeit": schw}
    if mythos:  # L((behauptung, claim), (richtig, truth))
        claim, truth = res(mythos, 0), res(mythos, 1)  # je (deutsch, englisch)
        e["mythos"] = {"behauptung": L(*claim), "richtig": L(*truth)}
    return e


# ================================================================ Welt
add({"id": "w-geraete", "typ": "welt", "titel": L("Geräte & Werkzeug", "Equipment & tools"),
     "synonyme": L(["Küchengeräte", "Pfannen", "Töpfe", "Herd", "Backofen", "Kochgeschirr"], ["kitchen appliances", "pans", "pots", "stove", "oven", "cookware"]),
     "kurz": L("Jedes Gerät bringt die Wärme auf eigene Art ins Essen: durch Kontakt, heiße Luft, Strahlung, Dampf oder Mikrowellen. Wer das weiß, versteht, warum dasselbe Rezept anders herauskommt.",
               "Every appliance gets heat into food in its own way: by contact, hot air, radiation, steam or microwaves. Knowing this explains why the same recipe turns out differently."),
     "bild_im_kopf": L("Wie verschiedene Wege auf denselben Berg: Das Ziel ist gleich, aber Tempo und Aussicht unterscheiden sich.",
                       "Like different trails up the same mountain: the summit is the same, but pace and view differ."),
     "was_passiert": L("Eine Pfanne gibt Wärme durch direkten Kontakt weiter, ein Ofen über heiße Luft und Strahlung. Ein Dampfgarer nutzt kondensierenden Dampf, eine Mikrowelle erwärmt das Wasser im Essen selbst. Material und Masse entscheiden, wie viel Wärme ein Gerät speichert und wie schnell es sie abgibt.",
                       "A pan passes on heat by direct contact, an oven through hot air and radiation. A steamer uses condensing steam, a microwave heats the water inside the food itself. Material and mass decide how much heat a tool stores and how fast it releases it."),
     "warum_wichtig": L("Viele Fehler liegen nicht am Rezept, sondern am Gerät: Eine leichte Pfanne kühlt beim Anbraten ab, ein Airfryer bräunt schneller als der Ofen.",
                        "Many failures are not down to the recipe but to the equipment: a thin pan cools down when searing, an air fryer browns faster than the oven."),
     "faustregeln": L(["Für Kruste: viel Masse und viel Hitze, also schwere Pfanne, Pizzastahl oder heißes Gusseisen.",
                       "Für Zartes wie Eier und Fisch: eine Pfanne, die schnell reagiert und nicht klebt.",
                       "Rezepte für ein anderes Gerät als Startpunkt nehmen und früher nachschauen."],
                      ["For a crust: lots of mass and lots of heat, so a heavy pan, a pizza steel or hot cast iron.",
                       "For delicate things like eggs and fish: a pan that reacts fast and doesn't stick.",
                       "Treat recipes written for another appliance as a starting point and check earlier."]),
     "links": ["waermeleitung", "konvektion", "waermestrahlung", "pfannenmaterial"],
     "visual": {"vorlage": "keine", "illustration": "a heavy cast-iron skillet, a copper saucepan, a chef's knife and a wooden spoon arranged together"},
     "quellen": [GERAET], "status": "entwurf", "schwierigkeit": "einsteiger"})

# ================================================================ Airfryer
add(T("airfryer", L("Airfryer: Heißluft statt Fett", "Air fryer: hot air instead of fat"),
      L(["Heißluftfritteuse", "Air Fryer", "Airfryer Pommes", "Heissluftfritteuse", "Airfryer Temperatur"], ["air fryer", "air fryer chips", "air fryer fries", "air fryer temperature", "hot-air fryer"]),
      L("Ein Airfryer ist ein kleiner Umluftofen mit sehr starkem Gebläse. Die schnelle Luft trocknet die Oberfläche rasch, darum bräunt er schneller als der Backofen.",
        "An air fryer is a small convection oven with a very strong fan. The fast air dries the surface quickly, so it browns faster than a full oven."),
      L("Wie ein Föhn neben einem lauen Sommerwind: Gleich warme Luft, aber der Föhn trocknet die Haare viel schneller.",
        "Like a hairdryer next to a mild summer breeze: the air is equally warm, but the hairdryer dries hair much faster."),
      L("Ein Heizstab sitzt direkt über dem Korb, ein Ventilator jagt die heiße Luft schnell um das Essen. Schnelle Luft reißt die feuchte, kühle Schicht an der Oberfläche weg. So verdampft das Wasser außen rasch, und die Oberfläche wird heiß genug für die Maillard-Reaktion. Frittiert wird dabei nichts: Das Gargut liegt in Luft, nicht in Öl.",
        "A heating element sits right above the basket, and a fan drives the hot air rapidly around the food. Fast air strips away the moist, cool layer at the surface. Water evaporates quickly on the outside, and the surface gets hot enough for the Maillard reaction. Nothing is actually fried: the food sits in air, not in oil."),
      L("Weil der Airfryer stärker trocknet und bräunt als ein Backofen, verbrennen Ofenrezepte darin leicht außen, bevor sie innen gar sind. Ein Löffel Öl macht den Unterschied zwischen trocken-braun und knusprig.",
        "Because an air fryer dries and browns more strongly than an oven, oven recipes easily burn outside before they are done inside. A spoonful of oil makes the difference between dry-brown and crisp."),
      L(["Das Gargut trocken tupfen und mit wenig Öl rundum benetzen, etwa ein Teelöffel pro Portion.",
         "Nur eine Lage in den Korb geben, damit die Luft überall hinkommt.",
         "Ofenrezepte etwa 20 °C tiefer einstellen und nach zwei Dritteln der Zeit nachschauen.",
         "Zwischendurch den Korb schütteln oder wenden.",
         "Bei Pommes und Wedges: vorher kurz in Wasser vorkochen, dann im Airfryer fertig garen."],
        ["Pat the food dry and coat it all over with a little oil, about a teaspoon per portion.",
         "Put only one layer in the basket so the air can reach everywhere.",
         "Set oven recipes about 20 °C lower and check after two thirds of the time.",
         "Shake the basket or turn the food halfway through.",
         "For chips and wedges: par-boil them in water first, then finish in the air fryer."]),
      L(["Für knusprige Kartoffeln: vorkochen und wenig Öl, weil die Stärke außen eine Kruste bildet und das Öl die Wärme besser überträgt.",
         "Für flüssige Teige: nicht in den Korb, weil das Gebläse sie verbläst und sie durch das Gitter laufen.",
         "Für Saftiges wie Pouletbrust: Kerntemperatur messen, weil der Airfryer außen schneller ist als innen."],
        ["For crisp potatoes: par-boil and use a little oil, because the starch forms a crust and the oil transfers heat better.",
         "For runny batters: keep them out of the basket, because the fan blows them about and they run through the grate.",
         "For juicy things like chicken breast: measure the core temperature, because the air fryer works faster outside than inside."]),
      ["konvektion", "maillard-reaktion", "verdampfen", "umluft-ober-unterhitze", "wedges-nicht-knusprig", "g-pommes", "kerntemperatur"],
      "a small black air fryer with its basket pulled out, filled with golden potato wedges",
      [NOVA_AIR, GERAET],
      mythos=L(("Der Airfryer frittiert ohne Öl.", "An air fryer fries without oil."),
               ("Er backt mit sehr schneller heißer Luft. Das Ergebnis ähnelt guten Ofen-Pommes, nicht Frittiertem, und etwas Öl braucht es trotzdem.",
                "It bakes with very fast hot air. The result is like good oven chips, not deep-fried ones, and it still needs a little oil."))))

# ================================================================ Induktion
add(T("induktion", L("Induktion: Der Topf heizt sich selbst", "Induction: the pan heats itself"),
      L(["Induktionsherd", "Induktionskochfeld", "Induktion Pfanne", "Induktion Topf geht nicht", "Magnet Test Pfanne"], ["induction hob", "induction cooktop", "induction pan", "pan doesn't work on induction", "magnet test pan"]),
      L("Unter dem Glas erzeugt eine Spule ein wechselndes Magnetfeld. Es erzeugt im Topfboden elektrische Ströme, und der Boden erhitzt sich selbst. Das Kochfeld bleibt dabei fast kalt.",
        "Under the glass, a coil creates an alternating magnetic field. It induces electric currents in the base of the pan, and the base heats itself. The hob itself stays almost cold."),
      L("Wie eine Fernbedienung für Wärme: Das Kochfeld gibt nur den Befehl, heiß wird der Topf.",
        "Like a remote control for heat: the hob only gives the command, the pan is what gets hot."),
      L("Das Magnetfeld wechselt zehntausende Male pro Sekunde die Richtung. In einem Topfboden aus magnetischem Metall entstehen dadurch Wirbelströme, und der Widerstand des Metalls wandelt sie in Wärme um. Weil keine heiße Platte dazwischen liegt, reagiert die Hitze sofort auf den Regler. Die Wärme entsteht über der ringförmigen Spule, die Mitte großer Pfannen bleibt oft etwas kühler.",
        "The magnetic field changes direction tens of thousands of times a second. In a pan base made of magnetic metal, this creates eddy currents, and the resistance of the metal turns them into heat. With no hot plate in between, the heat responds to the dial immediately. Heat forms above the ring-shaped coil, so the centre of large pans often stays a little cooler."),
      L("Induktion ist schnell und genau wie Gas, aber eine leere Pfanne wird in Sekunden glühend heiß. Das kann Öl verbrennen und Beschichtungen beschädigen.",
        "Induction is as fast and precise as gas, but an empty pan gets scorching hot within seconds. That can burn oil and damage coatings."),
      L(["Mit einem Magneten am Topfboden prüfen: Bleibt er haften, funktioniert der Topf auf Induktion.",
         "Die Pfanne passend zur Kochzone wählen, nicht viel kleiner.",
         "Pfannen auf mittlerer Stufe vorheizen, nicht auf Booster.",
         "Bei großen Pfannen das Bratgut öfter verschieben, weil die Mitte etwas kühler bleibt.",
         "Zum Warmhalten früh herunterschalten: Die Hitze geht sofort zurück."],
        ["Test with a magnet on the base of the pan: if it sticks, the pan works on induction.",
         "Choose a pan to match the cooking zone, not much smaller.",
         "Preheat pans on a medium setting, not on boost.",
         "In large pans move the food around more often, because the centre stays a little cooler.",
         "To keep things warm, turn down early: the heat drops immediately."]),
      L(["Für beschichtete Pfannen: nie leer auf höchster Stufe heizen, weil sie in Sekunden über 260 °C kommen.",
         "Für gleichmäßiges Anbraten: einen dicken Boden mit Alukern wählen, weil Aluminium die Wärme von der Spule in die Fläche verteilt."],
        ["For non-stick pans: never heat them empty on the highest setting, because they go above 260 °C within seconds.",
         "For even searing: choose a thick base with an aluminium core, because aluminium spreads the heat from the coil across the surface."]),
      ["waermeleitung", "pfannenmaterial", "pfanne-vorheizen", "beschichtete-pfanne", "rauchpunkt"],
      "a stainless steel pan on a black glass induction hob with a small horseshoe magnet stuck to the pan base",
      [INDUKTION, GERAET],
      mythos=L(("Induktion ist ungesund wegen der Strahlung.", "Induction is unhealthy because of radiation."),
               ("Das Magnetfeld ist schwach und reicht nur wenige Zentimeter weit. Für den Alltag gilt es als unbedenklich, wenn der Topf richtig auf der Zone steht.",
                "The magnetic field is weak and reaches only a few centimetres. For everyday use it is considered safe when the pan sits properly on the zone."))))

# ================================================================ Mikrowelle
add(T("mikrowelle", L("Mikrowelle: Wärme von innen?", "Microwave: heat from the inside?"),
      L(["Mikrowelle aufwärmen", "Mikrowelle ungleichmäßig", "Mikrowelle kalte Stellen", "Mikrowelle auftauen", "Mikrowelle Metall"], ["microwave reheating", "microwave uneven", "microwave cold spots", "microwave defrosting", "metal in microwave"]),
      L("Mikrowellen bringen Wassermoleküle zum Hin- und Herdrehen, und das erzeugt Wärme. Sie dringen aber nur wenige Zentimeter ein. Den Rest übernimmt langsame Wärmeleitung, darum gibt es kalte Stellen.",
        "Microwaves make water molecules twist back and forth, and that creates heat. But they only penetrate a few centimetres. Slow conduction does the rest, which is why there are cold spots."),
      L("Wie Kompassnadeln, die einem kreisenden Magneten folgen: Das ständige Mitdrehen reibt und wärmt, aber nur, solange der Magnet nah genug ist.",
        "Like compass needles following a circling magnet: the constant turning rubs and warms, but only while the magnet is close enough."),
      L("Wassermoleküle haben eine Plus- und eine Minusseite. Das Feld der Mikrowelle kippt Milliarden Mal pro Sekunde, und die Moleküle drehen sich mit. Die Reibung untereinander wird zu Wärme. Im Innern des Garraums bilden sich Zonen mit viel und wenig Energie, deshalb dreht sich der Teller. Weil die Oberfläche feucht bleibt und nicht über 100 °C kommt, bräunt nichts.",
        "Water molecules have a plus side and a minus side. The microwave field flips billions of times a second, and the molecules turn with it. Their friction with one another becomes heat. Inside the oven there are zones with more and less energy, which is why the plate turns. Because the surface stays moist and does not exceed 100 °C, nothing browns."),
      L("Die Mikrowelle ist für Aufwärmen, Schmelzen und Gemüse ideal, aber ungleichmäßig. Bei Resten zählt das: Kalte Stellen können Keime überleben lassen.",
        "The microwave is ideal for reheating, melting and vegetables, but it is uneven. With leftovers that matters: cold spots can let germs survive."),
      L(["Das Essen flach und ringförmig verteilen, die Mitte frei lassen.",
         "Mit einem Teller oder Deckel abdecken, damit der Dampf mitgart.",
         "Nach der Hälfte der Zeit umrühren oder wenden.",
         "Nach dem Erhitzen ein bis zwei Minuten stehen lassen, damit sich die Wärme verteilt.",
         "Prüfen, ob es überall dampfend heiß ist, besonders in der Mitte."],
        ["Spread the food out flat in a ring, leaving the centre empty.",
         "Cover it with a plate or lid so the steam helps cook it.",
         "Stir or turn it halfway through.",
         "After heating, let it stand for one or two minutes so the heat evens out.",
         "Check that it is steaming hot everywhere, especially in the middle."]),
      L(["Für Reste: überall dampfend heiß erhitzen, weil kalte Stellen Keime überleben lassen.",
         "Für Gefrorenes: mit Auftaustufe arbeiten, weil Eis die Mikrowellen kaum aufnimmt und sonst die Ränder schon garen.",
         "Kein Metall mit Kanten oder Goldrand: An Spitzen sammelt sich das Feld und es funkt."],
        ["For leftovers: heat until steaming hot everywhere, because cold spots let germs survive.",
         "For frozen food: use the defrost setting, because ice hardly absorbs microwaves and the edges would cook first.",
         "No metal with edges or gold rims: the field concentrates at points and it sparks."]),
      ["waermeleitung", "verdampfen", "keimwachstum", "eiskristalle", "x-mikrowelle-eis", "daempfen"],
      "a white microwave oven with its door open and a covered bowl of soup on the glass turntable",
      [MIKRO_SAFE, GERAET],
      mythos=L(("Die Mikrowelle zerstört die Vitamine im Essen.", "The microwave destroys the vitamins in food."),
               ("Jede Hitze baut empfindliche Vitamine ab. Weil die Mikrowelle kurz und mit wenig Wasser gart, bleibt bei Gemüse oft sogar mehr erhalten als beim Kochen im Topf.",
                "Any heat breaks down delicate vitamins. Because the microwave cooks briefly with little water, vegetables often keep more of them than when boiled in a pot."))))

# ================================================================ Schnellkochtopf
add(T("schnellkochtopf", L("Schnellkochtopf: Kochen über 100 °C", "Pressure cooker: boiling above 100 °C"),
      L(["Dampfkochtopf", "Drucktopf", "Schnellkochtopf Zeiten", "Instant Pot", "Schnellkochtopf Bohnen"], ["pressure cooker", "instant pot", "pressure cooker times", "pressure cooking beans", "stovetop pressure cooker"]),
      L("Im dicht verschlossenen Topf steigt der Druck, und Wasser kocht erst bei etwa 120 °C. Diese 20 Grad mehr machen Schmorfleisch und Hülsenfrüchte etwa dreimal so schnell weich.",
        "In the tightly sealed pot the pressure rises, and water only boils at around 120 °C. Those extra 20 degrees make braising meat and pulses tender about three times as fast."),
      L("Wie ein Deckel auf der Siedegrenze: Der Dampf darf nicht entweichen, also klettert die Temperatur weiter.",
        "Like a lid on the boiling limit: the steam cannot escape, so the temperature keeps climbing."),
      L("Beim Kochen entsteht Dampf, der im geschlossenen Topf nicht entweichen kann. Der Druck steigt auf knapp das Doppelte, und damit der Siedepunkt auf rund 115 bis 120 °C. Bei dieser Temperatur löst sich Bindegewebe zu Gelatine viel schneller, und die Zellwände von Bohnen werden rascher weich. Bräunung gibt es im Topf trotzdem keine, weil alles feucht bleibt.",
        "Cooking makes steam that cannot escape from the sealed pot. The pressure rises to almost double, and with it the boiling point to around 115 to 120 °C. At this temperature connective tissue turns to gelatine much faster, and the cell walls of beans soften more quickly. There is still no browning in the pot, because everything stays moist."),
      L("Ein Ragout in 40 statt 120 Minuten, Kichererbsen ohne stundenlanges Köcheln: Das spart viel Zeit. Weil man nicht hineinschauen kann, braucht es aber verlässliche Zeiten und etwas Vorsicht.",
        "A ragout in 40 instead of 120 minutes, chickpeas without hours of simmering: that saves a lot of time. Because you cannot look inside, it needs reliable times and some care."),
      L(["Fleisch vorher in einer Pfanne oder im offenen Topf anbraten, weil unter Druck nichts bräunt.",
         "Topf höchstens zu zwei Dritteln füllen, bei Hülsenfrüchten und Reis nur bis zur Hälfte.",
         "Immer genug Flüssigkeit zugeben, mindestens so viel, wie die Anleitung nennt.",
         "Deckel schließen, auf Druck bringen, dann die Hitze herunterschalten und die Zeit ab erreichtem Druck messen.",
         "Den Druck ganz entweichen lassen, bevor man den Deckel öffnet."],
        ["Brown meat first in a pan or in the open pot, because nothing browns under pressure.",
         "Fill the pot no more than two thirds, and only half for pulses and rice.",
         "Always add enough liquid, at least as much as the instructions say.",
         "Close the lid, bring it up to pressure, then turn the heat down and time from the moment pressure is reached.",
         "Let the pressure release completely before opening the lid."]),
      L(["Für Hülsenfrüchte: wenig füllen und etwas Öl zugeben, weil ihr Schaum das Ventil verstopfen kann.",
         "Für zartes Gemüse und Fisch: lieber nicht, weil sie in Minuten zerfallen.",
         "Ventil und Dichtungsring regelmäßig prüfen und reinigen."],
        ["For pulses: fill it only partly and add a little oil, because their foam can block the valve.",
         "For delicate vegetables and fish: better not, because they fall apart within minutes.",
         "Check and clean the valve and sealing ring regularly."]),
      ["siedepunkt-druck", "kollagen-gelatine", "schmoren", "bohnen-nicht-weich", "fond"],
      "a stainless steel pressure cooker with a locked lid and a small valve releasing a wisp of steam",
      [DRUCK, MC("Kapitel Kochen mit Wasser: Druck und Siedepunkt", "Chapter on cooking with water: pressure and boiling point")],
      schw="fortgeschritten"))

# ================================================================ Gusseisen
add(T("gusseisen", L("Gusseisen einbrennen und pflegen", "Seasoning and caring for cast iron"),
      L(["Gusseisenpfanne", "Eisenpfanne einbrennen", "Pfanne einbrennen", "Gusseisen Seife", "Gusseisen rostet", "Patina Pfanne"], ["cast iron skillet", "seasoning a pan", "carbon steel pan", "cast iron soap", "cast iron rust", "pan patina"]),
      L("Die schwarze Schicht auf Gusseisen und Eisenpfannen ist kein Schmutz, sondern Öl, das bei großer Hitze zu einer harten, glatten Schicht verbunden wurde. Sie schützt vor Rost und lässt das Bratgut weniger kleben.",
        "The black layer on cast iron and carbon steel pans is not dirt but oil that was bonded into a hard, smooth layer at high heat. It protects against rust and makes food stick less."),
      L("Wie ein Lack, den man selbst einbrennt: Jede dünne Schicht macht die Oberfläche glatter.",
        "Like a varnish you bake on yourself: every thin coat makes the surface smoother."),
      L("Erhitzt man eine hauchdünne Ölschicht über ihren Rauchpunkt, verbinden sich die Fettmoleküle zu einem festen Netz, einer Art Kunststoff. Diese Patina haftet am Eisen und füllt seine Poren. Gusseisen ist schwer und leitet Wärme eher schlecht: Es heizt langsam und ungleich auf. Dafür speichert es viel Wärme und kühlt beim Anbraten kaum ab.",
        "When a very thin film of oil is heated past its smoke point, the fat molecules link up into a solid network, a kind of plastic. This patina bonds to the iron and fills its pores. Cast iron is heavy and conducts heat rather poorly: it heats slowly and unevenly. In return it stores a lot of heat and barely cools when searing."),
      L("Gut eingebrannt brät eine Eisenpfanne Steaks mit einer Kruste, die keine beschichtete Pfanne schafft, und hält ein Leben lang. Falsch gepflegt rostet sie und alles klebt.",
        "Well seasoned, an iron pan sears steaks with a crust no non-stick pan can match, and it lasts a lifetime. Badly cared for, it rusts and everything sticks."),
      L(["Die Pfanne waschen und auf dem Herd vollständig trocknen.",
         "Einen Teelöffel neutrales Öl einreiben und mit Küchenpapier fast alles wieder abwischen: Sie soll matt aussehen, nicht ölig.",
         "Kopfüber eine Stunde im Ofen bei 230 bis 250 °C erhitzen, dann im Ofen abkühlen lassen.",
         "Drei- bis viermal wiederholen.",
         "Nach dem Kochen heiß abspülen, auf dem Herd trocknen und hauchdünn einölen."],
        ["Wash the pan and dry it completely on the hob.",
         "Rub in a teaspoon of neutral oil and wipe almost all of it off with kitchen paper: it should look matt, not oily.",
         "Heat it upside down in the oven at 230 to 250 °C for an hour, then let it cool in the oven.",
         "Repeat three or four times.",
         "After cooking, rinse it hot, dry it on the hob and oil it very thinly."]),
      L(["Für eine glatte Patina: viele dünne Schichten statt einer dicken, weil dickes Öl klebrig bleibt.",
         "Vor dem Anbraten zehn Minuten auf mittlerer Hitze vorheizen, weil Gusseisen ungleich aufheizt.",
         "Lange saure Schmorgerichte mit Tomate oder Wein lieber im Emailtopf, weil Säure die Patina angreift."],
        ["For a smooth patina: many thin coats instead of one thick one, because thick oil stays sticky.",
         "Preheat for ten minutes on medium heat before searing, because cast iron heats unevenly.",
         "Cook long acidic braises with tomato or wine in an enamelled pot instead, because acid attacks the patina."]),
      ["pfannenmaterial", "rauchpunkt", "oxidation-fett", "pfanne-vorheizen", "maillard-reaktion", "waermeleitung"],
      "a black cast-iron skillet with a glossy seasoned surface, a small bottle of oil and a folded cloth",
      [VT_GUSS, ATK_GUSS, GERAET],
      mythos=L(("Gusseisen darf nie mit Spülmittel in Berührung kommen.", "Cast iron must never touch washing-up liquid."),
               ("Eine gut eingebrannte Patina ist fest verbunden und verträgt etwas Spülmittel. Schaden richten Einweichen und Nässe an, weil das Eisen dann rostet.",
                "A well-seasoned patina is firmly bonded and can take a little washing-up liquid. Soaking and leaving it wet do the damage, because the iron then rusts."))))

# ================================================================ Beschichtete Pfanne
add(T("beschichtete-pfanne", L("Beschichtete Pfanne richtig nutzen", "Using a non-stick pan properly"),
      L(["Teflonpfanne", "Antihaftpfanne", "Antihaft Beschichtung", "Pfanne Beschichtung kaputt", "Keramikpfanne"], ["non-stick pan", "Teflon pan", "nonstick coating", "ruined non-stick pan", "ceramic pan"]),
      L("Eine Antihaft-Beschichtung ist so glatt, dass Eiweiß kaum Halt findet. Sie ist ideal für Eier und Fisch, verträgt aber keine sehr große Hitze.",
        "A non-stick coating is so slick that protein can barely grip it. It is ideal for eggs and fish, but cannot take very high heat."),
      L("Wie Wassertropfen auf einer Lotusblüte: Nichts kann sich festhalten.",
        "Like water drops on a lotus leaf: nothing can get a hold."),
      L("Klassische Beschichtungen bestehen aus PTFE, einem Kunststoff, an dem fast nichts haftet. Ab etwa 260 °C beginnt er sich zu zersetzen, und es entstehen Dämpfe. Eine leere Pfanne erreicht diese Temperatur auf starker Flamme oder Induktion in wenigen Minuten, mit Essen darin kaum. Keramikbeschichtungen vertragen mehr Hitze, verlieren ihre Glätte aber schneller.",
        "Classic coatings are made of PTFE, a plastic that almost nothing sticks to. From about 260 °C it starts to break down and gives off fumes. An empty pan reaches that temperature on a strong flame or induction within minutes, but hardly ever with food in it. Ceramic coatings tolerate more heat but lose their slickness faster."),
      L("Für eine dunkle Kruste auf Steak braucht es mehr Hitze, als die Beschichtung mag. Wer das weiß, nimmt für jede Aufgabe die passende Pfanne, und die beschichtete hält viel länger.",
        "A dark crust on steak needs more heat than the coating likes. Knowing this, you use the right pan for each job, and the non-stick one lasts much longer."),
      L(["Fett oder Bratgut vor dem Erhitzen in die Pfanne geben, nie leer stark aufheizen.",
         "Höchstens mittlere bis mittelhohe Stufe verwenden.",
         "Mit Holz- oder Silikonwendern arbeiten, nicht mit Metall.",
         "Die Pfanne abkühlen lassen, bevor sie ins Wasser kommt.",
         "Von Hand mit weichem Schwamm spülen."],
        ["Put fat or food into the pan before heating, never heat it empty on high.",
         "Use medium to medium-high heat at most.",
         "Use wooden or silicone spatulas, not metal.",
         "Let the pan cool down before it goes into water.",
         "Wash it by hand with a soft sponge."]),
      L(["Für Eier, Pfannkuchen und Fisch: die beschichtete Pfanne, weil Eiweiß darauf nicht anhaftet.",
         "Für Steak und scharfes Anbraten: Eisen oder Edelstahl, weil die Kruste mehr Hitze braucht, als die Beschichtung verträgt.",
         "Ist die Beschichtung zerkratzt oder klebt alles, ersetzen."],
        ["For eggs, pancakes and fish: the non-stick pan, because protein doesn't stick to it.",
         "For steak and hard searing: iron or stainless steel, because the crust needs more heat than the coating can take.",
         "Replace it once the coating is scratched or everything sticks."]),
      ["pfannenmaterial", "induktion", "fisch-klebt", "pfanne-vorheizen", "gusseisen"],
      "a non-stick frying pan with a perfectly sliding fried egg and a silicone spatula beside it",
      [PTFE, GERAET],
      mythos=L(("Beschichtete Pfannen sind immer giftig.", "Non-stick pans are always toxic."),
               ("Bei normaler Kochhitze ist PTFE stabil. Problematisch wird es erst bei Überhitzung, typischerweise in einer leer aufgeheizten Pfanne.",
                "At normal cooking heat PTFE is stable. It only becomes a problem when overheated, typically in a pan heated empty."))))

# ================================================================ Pizzastein
add(T("pizzastein", L("Pizzastein und Pizzastahl", "Pizza stone and pizza steel"),
      L(["Pizzastein", "Pizzastahl", "Backstahl", "Backstein Ofen", "Pizza knusprig Boden"], ["pizza stone", "pizza steel", "baking steel", "baking stone", "crisp pizza base"]),
      L("Ein Pizzastein oder -stahl speichert Ofenhitze und gibt sie auf einen Schlag an den Teigboden ab. So geht der Rand schnell auf, und der Boden wird knusprig, bevor der Belag austrocknet.",
        "A pizza stone or steel stores oven heat and delivers it to the base of the dough in one go. The rim rises fast, and the base crisps before the topping dries out."),
      L("Wie ein Akku für Hitze: Er lädt sich lange auf und entlädt sich in wenigen Minuten.",
        "Like a battery for heat: it charges for a long time and discharges in a few minutes."),
      L("Ein Backblech ist dünn und kühlt ab, sobald kalter Teig darauf liegt. Ein Stein hat viel Masse und speichert entsprechend viel Wärme. Stahl speichert ähnlich viel, leitet sie aber rund zehnmal besser weiter und bräunt den Boden schneller. Der kräftige Wärmestoß lässt Wasser im Teig schlagartig verdampfen, und der Teig springt auf.",
        "A baking sheet is thin and cools as soon as cold dough lands on it. A stone has a lot of mass and stores a matching amount of heat. Steel stores a similar amount but passes it on about ten times better, so it browns the base faster. The strong burst of heat flashes the water in the dough to steam, and the dough springs up."),
      L("Ein Haushaltsofen schafft nur etwa 250 bis 280 °C, ein Pizzaofen über 400 °C. Ein heißer Stein oder Stahl gleicht einen Teil dieses Unterschieds aus, und auch Brot bekommt mehr Ofentrieb.",
        "A home oven reaches only about 250 to 280 °C, a pizza oven over 400 °C. A hot stone or steel makes up part of that gap, and bread gets more oven spring too."),
      L(["Stein oder Stahl in den kalten Ofen legen, im oberen Drittel.",
         "Den Ofen auf höchste Stufe stellen und 45 bis 60 Minuten aufheizen.",
         "Die Pizza auf einer bemehlten Schaufel oder Backpapier einschießen.",
         "Für die letzten ein bis zwei Minuten den Grill zuschalten, damit der Belag oben bräunt.",
         "Stein im Ofen abkühlen lassen, nicht mit Wasser abschrecken."],
        ["Put the stone or steel in the cold oven, in the upper third.",
         "Set the oven to its highest setting and preheat for 45 to 60 minutes.",
         "Slide the pizza on from a floured peel or baking paper.",
         "Switch on the grill for the last one or two minutes so the topping browns on top.",
         "Let the stone cool in the oven, do not quench it with water."]),
      L(["Für schnelle, dunkle Böden: Stahl, weil er die Wärme besser weiterleitet.",
         "Für dicke Teige und Brot: Stein, weil er sanfter abgibt und weniger verbrennt.",
         "Ein Stein bricht bei schnellem Temperaturwechsel: immer mit dem Ofen zusammen aufheizen und abkühlen."],
        ["For fast, dark bases: steel, because it passes the heat on better.",
         "For thick doughs and bread: stone, because it releases heat more gently and burns less.",
         "A stone cracks with sudden changes in temperature: always heat it up and cool it down with the oven."]),
      ["waermeleitung", "ofentrieb", "g-pizza", "dampflockerung", "boden-durchgeweicht"],
      "a round pizza with a blistered crust on a dark rectangular baking steel next to a wooden pizza peel",
      [KA_STEEL, GERAET]))

# ================================================================ Messer
add(T("messer", L("Scharfe Messer: Schneiden statt quetschen", "Sharp knives: cutting instead of crushing"),
      L(["Messer schärfen", "Wetzstahl", "Messer abziehen", "Zwiebeln schneiden weinen", "stumpfes Messer"], ["sharpening knives", "honing steel", "honing a knife", "onions crying", "blunt knife"]),
      L("Eine scharfe Klinge trennt Zellen sauber, eine stumpfe quetscht sie. Das merkt man an tränenden Augen bei Zwiebeln, an braunen Rändern bei Kräutern und an Saft auf dem Brett.",
        "A sharp blade cuts cells cleanly, a blunt one crushes them. You notice it in watering eyes over onions, brown edges on herbs and juice on the board."),
      L("Wie eine Schere und eine Zange: Beide trennen, aber nur eine lässt glatte Kanten.",
        "Like scissors and pliers: both separate things, but only one leaves clean edges."),
      L("Beim Schneiden mit stumpfem Messer muss man drücken, und der Druck zerreißt viele Zellen neben dem Schnitt. Ihr Inhalt tritt aus: Bei Zwiebeln entsteht daraus der Reizstoff, bei Kräutern bräunt die Schnittkante. Eine Studie zeigte 2025, dass stumpfe Klingen mehr feine Tröpfchen aus der Zwiebel sprühen. Mit der Zeit biegt sich die feine Schneide um. Der Wetzstahl richtet sie wieder auf, erst der Schleifstein trägt Metall ab und formt eine neue Schneide.",
        "Cutting with a blunt knife needs pressure, and the pressure tears many cells beside the cut. Their contents leak out: in onions this produces the irritant, in herbs the cut edge browns. A 2025 study showed that blunt blades spray more fine droplets from the onion. Over time the fine edge bends over. A honing steel straightens it again; only a whetstone removes metal and forms a new edge."),
      L("Ein scharfes Messer ist sicherer, weil es nicht abrutscht, und es macht Schnittgut schöner und haltbarer.",
        "A sharp knife is safer because it doesn't slip, and it makes cut food look better and keep longer."),
      L(["Vor dem Kochen die Klinge ein paar Mal pro Seite über den Wetzstahl ziehen, im flachen Winkel.",
         "Zieht das Messer nicht mehr durch eine Tomatenhaut, ist Schleifen fällig.",
         "Auf dem Schleifstein im gleichbleibenden Winkel von etwa 15 bis 20 Grad schleifen, erst grob, dann fein.",
         "Mit ziehender Bewegung schneiden statt nur zu drücken.",
         "Auf Holz oder Kunststoff schneiden, nicht auf Glas oder Stein."],
        ["Before cooking, draw the blade over the honing steel a few times on each side, at a shallow angle.",
         "If the knife no longer slices through a tomato skin, it needs sharpening.",
         "On a whetstone, sharpen at a constant angle of about 15 to 20 degrees, coarse first, then fine.",
         "Cut with a drawing motion instead of just pressing down.",
         "Cut on wood or plastic, not on glass or stone."]),
      L(["Für Zwiebeln: ein scharfes Messer, weil weniger zerstörte Zellen weniger Reizstoff freisetzen.",
         "Für Kräuter: mit einem Schnitt durch, nicht hacken, weil gequetschte Blätter schwarz werden.",
         "Nicht in die Spülmaschine: Hitze, Lauge und Anstoßen machen die Schneide stumpf."],
        ["For onions: a sharp knife, because fewer damaged cells release less irritant.",
         "For herbs: slice through in one cut rather than chopping, because crushed leaves turn black.",
         "Keep it out of the dishwasher: heat, detergent and knocks dull the edge."]),
      ["zwiebel", "kraeuter-schwarz", "enzym-braeunung", "saft-beim-schneiden"],
      "a chef's knife on a wooden board with neatly diced onion and a honing steel lying alongside",
      [ONION, HONE, MC("Kapitel Gemüse: Zwiebeln", "Chapter on vegetables: onions")]))

# ================================================================ Wok
add(T("wok", L("Wok: Große Hitze, kleine Mengen", "Wok: high heat, small batches"),
      L(["Wok braten", "Pfannenrühren", "Stir fry", "Wok Hei", "Wok auf Induktion", "Wokpfanne einbrennen"], ["stir-fry", "wok cooking", "wok hei", "wok on induction", "seasoning a wok"]),
      L("Im Wok brät man kleine Stücke sehr heiß und kurz, unter ständigem Bewegen. Zu viel auf einmal kühlt ihn ab, und dann dünstet das Gemüse statt zu braten.",
        "In a wok you fry small pieces very hot and fast, keeping them moving. Too much at once cools it down, and the vegetables steam instead of frying."),
      L("Wie eine Bühne mit einem Scheinwerfer: Wer im Licht steht, wird heiß, wer am Rand wartet, bleibt warm.",
        "Like a stage with one spotlight: whoever stands in the light gets hot, whoever waits at the edge stays warm."),
      L("Der dünne Stahl am Boden wird sehr heiß, die steilen Seiten bleiben kühler. Durch das Bewegen kommt jedes Stück kurz an den heißen Grund und dann wieder an den Rand. Auf einem starken Gasbrenner schlagen Flammen über den Rand, und verdampfende Öltröpfchen geben das typische rauchige Aroma, das Wok Hei. Auf dem Haushaltsherd fehlt diese Leistung, darum zählt die Menge umso mehr.",
        "The thin steel at the bottom gets very hot, the steep sides stay cooler. Tossing brings each piece briefly to the hot base and back to the edge. On a powerful gas burner flames lick over the rim, and vaporising oil droplets give the typical smoky aroma, called wok hei. A home hob lacks this power, so the batch size matters all the more."),
      L("Die meisten Wokgerichte zu Hause werden wässrig, weil zu viel auf einmal im Wok liegt. Wer in Portionen brät, bekommt Bräunung und Biss.",
        "Most home stir-fries turn watery because too much is in the wok at once. Frying in batches gives browning and bite."),
      L(["Alles vorher schneiden und bereitstellen: Während des Bratens bleibt keine Zeit.",
         "Den Wok heiß werden lassen, bis ein Wassertropfen tanzt, dann erst Öl hinein.",
         "Fleisch und Gemüse getrennt und in kleinen Portionen braten, jeweils herausnehmen.",
         "Zum Schluss alles zurück in den Wok, Sauce darüber und kurz durchschwenken.",
         "Auf Induktion oder Glaskeramik einen Wok mit flachem Boden nehmen."],
        ["Cut and lay out everything beforehand: there is no time once frying starts.",
         "Let the wok get hot until a drop of water dances, only then add oil.",
         "Fry meat and vegetables separately and in small batches, taking each out.",
         "At the end put everything back, add the sauce and toss briefly.",
         "On induction or ceramic hobs, use a wok with a flat base."]),
      L(["Für Bräunung am Haushaltsherd: höchstens zwei Handvoll pro Durchgang, weil mehr den Wok unter 100 °C drückt.",
         "Für Gemüse mit Biss: gut abgetrocknet hinein, weil nasses Gemüse die Hitze schluckt.",
         "Einen Stahlwok wie Gusseisen einbrennen und pflegen."],
        ["For browning on a home hob: no more than two handfuls per batch, because more pushes the wok below 100 °C.",
         "For crunchy vegetables: add them well dried, because wet vegetables swallow the heat.",
         "Season and care for a carbon steel wok like cast iron."]),
      ["leidenfrost", "maillard-reaktion", "verdampfen", "gusseisen", "rauchpunkt"],
      "a carbon steel wok tossing strips of vegetables and beef over a blue gas flame",
      [ATK_WOK, GERAET]))

# ================================================================ Experiment
add({"id": "x-mikrowelle-eis", "typ": "experiment", "titel": L("Eis bleibt in der Mikrowelle kalt", "Ice stays cold in the microwave"),
     "synonyme": L(["Mikrowelle Experiment", "Eiswürfel Mikrowelle", "Mikrowelle Eis schmilzt nicht", "Auftauen Mikrowelle warum"], ["microwave experiment", "ice cube microwave", "ice doesn't melt in microwave", "why microwave defrosting is uneven"]),
     "kurz": L("Ein Glas Wasser und ein Glas Eiswürfel, gleich lang in der Mikrowelle: Das Wasser wird heiß, das Eis schmilzt kaum. Darum taut Gefrorenes so ungleichmäßig auf.",
               "A glass of water and a glass of ice cubes, microwaved for the same time: the water gets hot, the ice barely melts. That is why frozen food thaws so unevenly."),
     "bild_im_kopf": L("Wie Tänzer in einem vollen Lift: Die Musik spielt, aber niemand kann sich drehen.",
                       "Like dancers in a crowded lift: the music plays, but nobody can turn."),
     "material": L(["zwei gleiche mikrowellenfeste Gläser", "Eiswürfel", "kaltes Wasser", "eine Mikrowelle", "ein Thermometer, falls vorhanden"],
                   ["two identical microwave-safe glasses", "ice cubes", "cold water", "a microwave", "a thermometer, if you have one"]),
     "schritte": L(["Ein Glas mit Eiswürfeln füllen, das andere gleich hoch mit kaltem Wasser.",
                    "Nur das Glas mit Wasser 30 Sekunden auf voller Stufe erhitzen und fühlen oder messen.",
                    "Dann nur das Glas mit Eis gleich lang erhitzen.",
                    "Vergleichen: Wie warm ist das Wasser, wie viel Eis ist geschmolzen?"],
                   ["Fill one glass with ice cubes and the other to the same height with cold water.",
                    "Heat only the glass of water for 30 seconds on full power, then feel or measure it.",
                    "Then heat only the glass of ice for the same time.",
                    "Compare: how warm is the water, and how much ice has melted?"]),
     "beobachtung": L("Das Wasser ist deutlich warm geworden. Vom Eis ist nur wenig geschmolzen, und das Schmelzwasser am Boden ist warm, während die Würfel kalt bleiben.",
                      "The water has become noticeably warm. Only a little of the ice has melted, and the meltwater at the bottom is warm while the cubes stay cold."),
     "erklaerung": L("Mikrowellen erwärmen, indem sie Wassermoleküle hin- und herdrehen. Im Eis sind die Moleküle in einem festen Gitter gefangen und können sich kaum drehen. Flüssiges Wasser nimmt die Energie viel besser auf. Sobald irgendwo ein wenig Eis schmilzt, wird genau diese Stelle schnell heiß. So garen beim Auftauen die Ränder, während die Mitte noch gefroren ist.",
                     "Microwaves heat by twisting water molecules back and forth. In ice the molecules are trapped in a rigid lattice and can barely turn. Liquid water absorbs the energy much better. As soon as a little ice melts somewhere, that very spot heats up fast. That is how the edges cook during defrosting while the centre is still frozen."),
     "dauer": L("5 Minuten", "5 minutes"),
     "links": ["mikrowelle", "eiskristalle", "waermeleitung"], "welten": ["w-geraete"],
     "visual": {"vorlage": "ablauf", "illustration": "two glasses side by side, one with steaming water and one with ice cubes, in front of a microwave"},
     "quellen": [MC("Kapitel Wärme und Garmethoden: Mikrowellen", "Chapter on heat and cooking methods: microwaves")], "status": "entwurf", "schwierigkeit": "einsteiger"})

# Bestehende Einträge, die zur neuen Welt gehören
NEW_W = {"w-geraete": ["pfannenmaterial", "pfanne-vorheizen", "umluft-ober-unterhitze", "sous-vide", "dampf-im-ofen", "kerntemperatur", "siedepunkt-druck", "daempfen"]}

if __name__ == "__main__":
    known = {f[:-5] for f in os.listdir(f"{ROOT}/content/entries")} | {e["id"] for e in E}
    ml = json.load(open(f"{ROOT}/content/master-list.json"))
    have = {m["id"] for m in ml["eintraege"]}
    for e in E:
        de = res(e, 0)
        miss = [l for l in de.get("links", []) if l not in known]
        if miss: print("Unbekannte Verweise in", de["id"], miss)
        de["links"] = [l for l in de.get("links", []) if l in known]
        json.dump(de, open(f"{ROOT}/content/entries/{de['id']}.json", "w"), ensure_ascii=False, indent=2)
        if de["id"] not in have:
            ml["eintraege"].append({"id": de["id"], "typ": de["typ"], "titel": de["titel"], "status": "entwurf", "pilot": False, "links": de["links"],
                                    "welten": de.get("welten", []), "synonyme": de.get("synonyme", []), "visual": {"vorlage": de.get("visual", {}).get("vorlage", "keine")}, "verlinkt_von": []})
    for w, ids2 in NEW_W.items():
        for i in ids2:
            p = f"{ROOT}/content/entries/{i}.json"
            if not os.path.exists(p): continue
            x = json.load(open(p))
            if w not in x.setdefault("welten", []):
                x["welten"].append(w)
                json.dump(x, open(p, "w"), ensure_ascii=False, indent=2)
            for m in ml["eintraege"]:
                if m["id"] == i and w not in m.setdefault("welten", []): m["welten"].append(w)
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
    path = f"{ROOT}/content/en/_batch_geraete.json"
    json.dump(batch, open(path, "w"), ensure_ascii=False, indent=1)
    subprocess.check_call([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "apply", path], cwd=ROOT)
    os.remove(path)
    print(len(E), "Einträge geschrieben")
