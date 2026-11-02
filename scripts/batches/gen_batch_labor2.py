"""Batch 12: Labor-Rezepte II."""
import json, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "content/entries")
QM = {"titel": "Harold McGee: On Food and Cooking (2004)"}
Q = {
  "masc": {"titel": "Cheese Grotto: Homemade mascarpone with citric acid", "url": "https://cheesegrotto.com/blogs/journal/homemade-mascarpone-recipe-with-citric-acid"},
  "van": {"titel": "Vanilla Bean Kings: How many vanilla beans do you need for extract?", "url": "https://www.vanillabeankings.com/blogs/recipes/how-many-vanilla-beans-do-you-need-for-extract"},
  "senf": {"titel": "Popular Science: How to make mustard", "url": "https://www.popsci.com/diy/how-to-make-mustard/"},
  "kraut": {"titel": "University of New Hampshire Extension: Fermenting, safe food preservation", "url": "https://extension.unh.edu/node/22550"},
  "dulce": {"titel": "Great British Chefs: How to make dulce de leche sous vide", "url": "https://www.greatbritishchefs.com/how-to-cook/how-to-make-dulce-de-leche-sous-vide"},
  "pek": {"titel": "Nourish and Nestle: How to make apple pectin stock", "url": "https://nourishandnestle.com/how-to-make-apple-pectin-stock-for-jam-jelly/"},
}
E = []
def labor(id, titel, syn, kurz, bild, material, dauer, momente, ergebnis, haltbarkeit, verwendung, links, welten, quellen, sicherheit=None, vergleich=None, schw="einsteiger"):
    e = dict(id=id, typ="labor", titel=titel, synonyme=syn, kurz=kurz, bild_im_kopf=bild, material=material, dauer=dauer,
             schluesselmomente=[{"schritt": s, "warum": w, **({"prinzip": p} if p else {})} for s, w, p in momente],
             ergebnis=ergebnis, haltbarkeit=haltbarkeit, verwendung=verwendung, links=links, welten=welten, quellen=quellen,
             status="entwurf", schwierigkeit=schw, visual={"vorlage": "vergleich", "params": vergleich} if vergleich else {"vorlage": "keine"})
    if sicherheit: e["sicherheit"] = sicherheit
    E.append(e)
def vg(vorher, nachher, felder): return {"vorher": vorher, "nachher": nachher, "vergleich": felder}

labor("l-mascarpone", "Mascarpone selber machen", ["Mascarpone herstellen", "Mascarpone Ersatz", "Tiramisu Käse"],
  "Mascarpone ist Rahm, der mit etwas Säure in der Hitze eindickt und dann abtropft. Er braucht nur zwei Zutaten.",
  "Wie Schlagrahm in Zeitlupe: Ohne Schneebesen wird der Rahm allein durch Wärme und Säure dick.",
  ["500 ml Vollrahm", "½ TL Zitronensäure in 4 EL Wasser gelöst (oder 2 EL Zitronensaft)", "Topf, Thermometer", "Sieb mit feinem Tuch"], "8–9 Stunden, davon 10 Minuten Arbeit",
  [("Rahm langsam auf etwa 82 °C erwärmen", "Die Hitze bereitet das Milcheiweiß darauf vor, mit der Säure zu reagieren.", "eiweiss-denaturierung"),
   ("Säure einrühren, 2 Minuten auf dieser Temperatur halten", "Wie beim Frischkäse verlieren die Eiweißteilchen ihre Ladung. Weil Rahm aber so viel Fett hat, flockt nichts aus: Er dickt nur cremig ein.", "saeure-denaturierung"),
   ("Vom Herd nehmen und 30 Minuten ruhen lassen", "Beim Abkühlen festigt sich das Eiweißnetz zwischen den Fetttröpfchen.", "emulsion"),
   ("Im Tuch 6–8 Stunden im Kühlschrank abtropfen lassen", "Es tropft nur wenig Molke ab. Kälte lässt das Milchfett fest werden, so wird er streichfest.", "fett-kristallisation")],
  "Eine dicke, glatte Creme, etwas weniger als die Rahmmenge (Richtwert).",
  "Gekühlt 4–5 Tage.",
  ["Tiramisu, Cheesecake, Risotto zum Schluss statt Butter.", "Mit Zucker und Vanille als Füllung."],
  ["saeure-denaturierung", "sahne", "l-frischkaese", "g-risotto", "emulsion"], ["w-milch", "w-suesses"], [Q["masc"], QM],
  vergleich=vg("Rahm", "nach dem Abtropfen", [{"label": "im Tuch", "gefaess": "schuessel", "inhalt": "fluessig", "vorher": {"farbe": "#fbf7ec", "fuell": 0.6}, "nachher": {"farbe": "#f4f0e2", "fuell": 0.15, "klumpen": 1, "klumpenfarbe": "#fff8e8"}}]))

labor("l-vanilleextrakt", "Vanilleextrakt ansetzen", ["Vanilleextrakt selber machen", "Vanille in Wodka", "Vanilleessenz"],
  "Vanilleschoten geben ihr Aroma in Alkohol ab. Nach einigen Wochen ist daraus Vanilleextrakt geworden.",
  "Wie Teebeutel in kaltem Wasser: Es geht langsam, aber am Ende ist alles Aroma im Glas.",
  ["5–6 Vanilleschoten (etwa 30 g)", "250 ml Wodka oder anderer Schnaps mit mindestens 35 % Alkohol", "dunkle Glasflasche oder Schraubglas"], "mindestens 8 Wochen (Richtwert)",
  [("Schoten längs aufschneiden und klein schneiden", "Mehr offene Fläche heißt: Das Aroma findet schneller hinaus.", "diffusion"),
   ("Mit dem Alkohol übergießen, verschließen", "Vanillin und die übrigen Duftstoffe lösen sich gut in Alkohol, schlecht in Wasser.", "aroma-loeslichkeit"),
   ("Dunkel lagern, einmal pro Woche schütteln", "Schütteln bringt frischen Alkohol an die Schoten. Licht würde Aromen zerstören.", "diffusion"),
   ("Nach etwa 8 Wochen verwenden, die Schoten drin lassen", "Je länger, desto kräftiger. Man kann mit Alkohol nachfüllen.", None)],
  "Etwa 250 ml Vanilleextrakt, dunkelbraun und stark duftend.",
  "Dunkel und verschlossen jahrelang. Der Alkohol konserviert.",
  ["Kuchen, Cremen, Glace: etwa 1 TL ersetzt das Mark einer halben Schote (Richtwert).", "Als Geschenk in kleinen Flaschen."],
  ["aroma-loeslichkeit", "diffusion", "w-suesses"], ["w-suesses", "w-gebaeck"], [Q["van"], QM],
  sicherheit="Enthält Alkohol: Für Kinder nur im gebackenen Kuchen, nicht pur.",
  vergleich=vg("Tag 1", "nach 8 Wochen", [{"label": "Vanille in Wodka", "gefaess": "flasche", "inhalt": "fluessig", "vorher": {"farbe": "#f3efe2", "fuell": 0.7}, "nachher": {"farbe": "#6b3a1e", "fuell": 0.7}}]))

labor("l-puderzucker", "Puderzucker selber mahlen", ["Puderzucker herstellen", "Staubzucker", "Puderzucker Ersatz"],
  "Puderzucker ist nichts anderes als fein gemahlener Kristallzucker. Ein starker Mixer schafft das in einer Minute.",
  "Wie Kiesel, die zu Sand gemahlen werden: Es ist derselbe Stein, aber er verhält sich ganz anders.",
  ["100 g Kristallzucker", "1 TL Maisstärke (nach Wunsch)", "Hochleistungsmixer oder Gewürzmühle", "feines Sieb"], "5 Minuten",
  [("Zucker in kurzen Stößen fein mahlen", "Die Kristalle zerbrechen in winzige Splitter. Die Oberfläche wird tausendfach größer.", "oberflaeche"),
   ("Zwei Minuten warten, bevor der Deckel aufgeht", "Der feine Staub soll sich setzen.", None),
   ("Durch ein feines Sieb streichen", "Grobe Reste würden in Glasur knirschen.", None),
   ("Nach Wunsch Stärke untermischen", "Zuckerstaub zieht Feuchtigkeit an und verklebt. Stärke hält ihn rieselfähig.", "zucker-feuchtigkeit")],
  "Etwa 100 g Puderzucker.",
  "Luftdicht und trocken lange haltbar. Klumpen vor Gebrauch durchsieben.",
  ["Glasuren und Zuckerguss: Er löst sich sofort, ohne zu knirschen.", "Schlagrahm, Mürbeteig, zum Bestäuben."],
  ["oberflaeche", "zucker", "zucker-feuchtigkeit", "muerbe"], ["w-suesses", "w-gebaeck"], [QM],
  sicherheit="Feiner Zuckerstaub: Mixer erst öffnen, wenn er sich gesetzt hat.")

labor("l-buttermilch-ersatz", "Buttermilch-Ersatz aus Milch und Zitrone", ["Buttermilch Ersatz", "saure Milch", "Buttermilch selber machen"],
  "Milch mit etwas Zitronensaft wird in wenigen Minuten sauer und leicht dick. Zum Backen ersetzt sie Buttermilch.",
  "Wie ein Doppelgänger: Sieht nicht ganz gleich aus, spielt die Rolle im Teig aber genauso.",
  ["250 ml Milch", "1 EL Zitronensaft oder milder Essig"], "10 Minuten",
  [("Zitronensaft in ein Messglas geben, mit Milch auf 250 ml auffüllen", "Die Säure senkt den pH-Wert der Milch.", "ph-wert"),
   ("5–10 Minuten stehen lassen", "Das Milcheiweiß beginnt zu gerinnen, die Milch wird dicker und bildet feine Flocken.", "saeure-denaturierung"),
   ("Im Teig zusammen mit Natron verwenden", "Die Säure reagiert mit Natron zu Kohlendioxid: Pancakes und Scones gehen auf.", "chemische-lockerung")],
  "250 ml saure Milch.",
  "Frisch verwenden.",
  ["Pancakes, Scones, Zopf und Kuchen, die Buttermilch verlangen.", "Marinade für Poulet: Die milde Säure macht die Oberfläche zart."],
  ["chemische-lockerung", "saeure", "milch", "natron", "g-pancakes", "l-butter"], ["w-milch", "w-gebaeck"], [QM])

labor("l-senf", "Senf selber machen", ["Senf herstellen", "Senf aus Senfkörnern", "scharfer Senf", "milder Senf"],
  "Senfkörner sind erst scharf, wenn man sie zerkleinert und mit Wasser mischt. Ein Enzym bildet dann die Schärfe, und mit Essig legt man fest, wie scharf er bleibt.",
  "Wie eine Fotokamera: Wasser öffnet den Verschluss, Essig schließt ihn. Was dazwischen passiert, bleibt im Bild.",
  ["75 g Senfkörner (gelb für mild, braun für scharf)", "Wasser", "2–3 EL Weißwein- oder Apfelessig", "½ TL Salz, 1–2 EL Zucker oder Honig", "Mörser oder Mixer"], "2 Stunden plus 2–3 Tage ziehen",
  [("Körner einige Stunden in Wasser einweichen", "Sie quellen und lassen sich besser zerkleinern. Kaltes Wasser macht den Senf schärfer, warmes milder.", "schaerfe"),
   ("Abgießen und mit Salz und Zucker grob oder fein mahlen", "Beim Zerkleinern trifft ein [[enzym|Enzym]] in den Körnern auf seinen Partnerstoff. Gemeinsam bilden sie die scharfen Senföle.", "enzym"),
   ("Ein paar Minuten warten, dann Essig einrühren", "Säure stoppt das Enzym. Früher Essig gibt milden, später Essig scharfen Senf.", "saeure"),
   ("In ein Glas füllen und 2–3 Tage im Kühlschrank ziehen lassen", "Frisch ist er beißend und bitter. Mit der Zeit wird er runder und milder.", None)],
  "Etwa ein kleines Glas Senf.",
  "Gekühlt mehrere Monate. Essig und Salz konservieren ihn.",
  ["Zur Wurst, in die Vinaigrette, in die Mayonnaise als Helfer für die Emulsion.", "Grobkörnig zu Käse und Fleisch."],
  ["senf", "schaerfe", "enzym", "saeure", "emulgieren", "g-mayonnaise"], ["w-saucen"], [Q["senf"], QM],
  sicherheit="Beim Mahlen steigen scharfe Dämpfe auf: nicht direkt über den Mixer beugen.",
  vergleich=vg("Körner", "gemahlen und gezogen", [{"label": "Senfglas", "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#eaf1f4", "fuell": 0.4, "kristalle": 0}, "nachher": {"farbe": "#d9b23a", "fuell": 0.6}}]))

labor("l-sauerkraut", "Sauerkraut selber machen", ["Sauerkraut herstellen", "Kabis fermentieren", "Weißkohl einlegen", "Fermentieren"],
  "Kabis mit etwa 2 % Salz gärt in drei bis vier Wochen zu Sauerkraut. Milchsäurebakterien machen ihn sauer und haltbar.",
  "Wie eine Burg, die ihre eigenen Wächter ausbildet: Das Salz hält Fremde draußen, bis die Milchsäurebakterien das Tor übernehmen.",
  ["1 kg Weißkohl (Kabis)", "20 g Salz ohne Jod (etwa 2 % des Kohlgewichts)", "großes Glas oder Gärtopf", "Gewicht zum Beschweren, sauberes Tuch"], "3–4 Wochen",
  [("Kohl fein hobeln und mit dem Salz kräftig kneten", "Salz zieht Saft aus den Zellen. Nach einigen Minuten steht der Kohl in seiner eigenen Lake.", "osmose"),
   ("Fest ins Glas drücken, bis Lake darüber steht, beschweren", "Unter der Lake ist kein Sauerstoff: Schimmel kann nicht wachsen, Milchsäurebakterien schon.", "milchsaeuregaerung"),
   ("Bei etwa 21–24 °C stehen lassen, Kohl immer unter der Lake halten", "Die Bakterien bilden Milchsäure. Wärmer wird er weich, unter etwa 15 °C gärt er kaum.", "milchsaeuregaerung"),
   ("Nach 3–4 Wochen, wenn es nicht mehr blubbert, kühl stellen", "Die Säure ist jetzt so hoch, dass kaum ein Keim mehr wachsen kann.", "keimwachstum")],
  "Etwa 1 kg Sauerkraut.",
  "Gekühlt mehrere Monate.",
  ["Roh als Salat: voller lebender Bakterien.", "Gekocht zu Wurst, Speck und Kartoffeln."],
  ["milchsaeuregaerung", "osmose", "salz", "keimwachstum", "laenger-haltbar", "wasseraktivitaet"], ["w-gemuese"], [Q["kraut"], QM],
  sicherheit="Weißer Film auf der Lake (Kahmhefe) abschöpfen. Pelziger, farbiger Schimmel oder fauliger Geruch: wegwerfen.",
  vergleich=vg("eingelegt", "nach 3–4 Wochen", [{"label": "Gärglas", "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#dfe8c4", "fuell": 0.8, "blasen": 0}, "nachher": {"farbe": "#e7deb0", "fuell": 0.78, "blasen": 0.7}}]))

labor("l-brauner-zucker", "Brauner Zucker aus Zucker und Melasse", ["brauner Zucker selber machen", "Rohrzucker Ersatz", "Melasse Zucker", "Brown Sugar"],
  "Brauner Zucker ist weißer Zucker mit etwas Melasse. Die Melasse bringt Aroma, Feuchtigkeit und ein wenig Säure.",
  "Wie ein weißes Hemd, in Tee getaucht: Das Hemd bleibt dasselbe, aber es hat jetzt Farbe und Geschmack.",
  ["200 g Kristallzucker", "1 EL Melasse für hellen, 2 EL für dunklen Zucker", "Schüssel und Gabel, oder Küchenmaschine"], "5 Minuten",
  [("Melasse zum Zucker geben und mit der Gabel einarbeiten", "Die Melasse überzieht jeden Kristall mit einem dünnen Film.", None),
   ("So lange mischen, bis die Farbe gleichmäßig ist", "Melasse ist Zuckersirup mit Aromastoffen und Mineralien, die beim Raffinieren übrig bleiben.", None),
   ("Luftdicht aufbewahren", "Melasse zieht Feuchtigkeit an: Der Zucker bleibt weich und macht Gebäck saftiger.", "zucker-feuchtigkeit")],
  "Etwa 200 g brauner Zucker.",
  "Luftdicht lange haltbar. Hart geworden: über Nacht mit einem Stück Brot in die Dose legen.",
  ["Chewy Cookies und Brownies: Sie bleiben weicher.", "Mit Natron im Teig: Die leichte Säure der Melasse hilft beim Aufgehen."],
  ["zucker-feuchtigkeit", "zucker", "chemische-lockerung", "kekse-breit"], ["w-gebaeck", "w-suesses"], [QM])

labor("l-dulce-de-leche", "Dulce de leche aus Milch und Zucker", ["Dulce de leche", "Milchkaramell", "Karamellcreme", "Confiture de lait"],
  "Milch und Zucker werden stundenlang eingekocht, bis eine braune Karamellcreme entsteht. Eine Prise Natron beschleunigt die Bräunung.",
  "Wie ein Sonnenuntergang: Er kommt langsam, aber Schritt für Schritt wird alles goldener.",
  ["1 l Vollmilch", "300 g Zucker", "¼ TL Natron", "1 Vanilleschote nach Wunsch", "breiter Topf mit dickem Boden"], "2–3 Stunden (Richtwert)",
  [("Milch, Zucker und Vanille aufkochen, dann Natron einrühren", "Natron macht die Milch leicht basisch. Das beschleunigt die Bräunung und verhindert, dass die Milch gerinnt.", "basen-braeunung"),
   ("Offen leise köcheln lassen, regelmäßig rühren", "Wasser verdampft, Zucker und Milcheiweiß werden konzentriert.", "reduktion"),
   ("Zum Schluss häufiger rühren, bis sie karamellbraun und dick ist", "Milchzucker und Milcheiweiß reagieren: Farbe und Karamellaroma entstehen bei unter 100 °C, weil es so lange dauert.", "maillard-reaktion"),
   ("Heiß in saubere Gläser füllen", "Beim Abkühlen wird sie noch dicker.", None)],
  "Etwa 400 ml Dulce de leche.",
  "Gekühlt einige Wochen.",
  ["Aufs Brot, in Alfajores, zu Glace.", "Zwischen Tortenböden."],
  ["maillard-reaktion", "basen-braeunung", "reduktion", "milch", "karamellisierung"], ["w-milch", "w-suesses"], [Q["dulce"], QM],
  sicherheit="Geschlossene Kondensmilchdosen nie im Wasser kochen: Kocht der Topf trocken, kann die Dose platzen.",
  vergleich=vg("Start", "nach 2–3 Stunden", [{"label": "Topf", "gefaess": "schuessel", "inhalt": "fluessig", "vorher": {"farbe": "#fbf7ec", "fuell": 0.9}, "nachher": {"farbe": "#a0612a", "fuell": 0.4}}]))

labor("l-apfelpektin", "Pektin aus Apfelresten", ["Apfelpektin", "Pektin selber machen", "Geliermittel aus Äpfeln", "Gelierhilfe natürlich"],
  "Schalen und Kerngehäuse von sauren Äpfeln stecken voller Pektin. Ausgekocht und eingekocht wird daraus ein natürliches Geliermittel.",
  "Wie Kleister aus dem Bastelschrank: Unscheinbar flüssig, aber er hält zusammen, was allein nicht hält.",
  ["1–1,5 kg saure Äpfel oder Schalen und Kerngehäuse (z. B. vom Apfelkuchen, gesammelt im Tiefkühler)", "Wasser, bis alles knapp bedeckt ist", "Topf, Sieb, feines Tuch", "kalter Teller für die Probe"], "1 Tag, davon 1½ Stunden Arbeit",
  [("Äpfel grob schneiden, mit Wasser bedecken, 40–60 Minuten zugedeckt köcheln", "Hitze löst das [[pektin|Pektin]] aus den Zellwänden ins Wasser.", "pektin-abbau"),
   ("Über Nacht durch ein Tuch abtropfen lassen, nicht pressen", "Pressen macht den Saft trüb.", None),
   ("Den Saft offen auf die Hälfte einkochen", "Das Pektin wird konzentriert.", "reduktion"),
   ("Tellerprobe: einen Löffel mit etwas Zucker und Zitrone auf einem kalten Teller abkühlen lassen", "Wird er fest und runzelt beim Schieben, ist genug Pektin da. Sonst weiter einkochen.", "gelbildung-pektin")],
  "Etwa 500 ml Pektinsaft (Richtwert).",
  "Gekühlt eine Woche, eingefroren in Portionen viele Monate.",
  ["Für Konfitüre aus pektinarmen Früchten wie Erdbeeren, Kirschen oder Birnen: etwa 250 ml auf 1,5 kg Früchte (Richtwert).", "Für Gelee."],
  ["pektin", "gelbildung-pektin", "g-konfituere", "reduktion"], ["w-suesses"], [Q["pek"], QM],
  vergleich=vg("ausgekocht", "eingekocht", [{"label": "Pektinsaft", "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#f1e2b4", "fuell": 0.8}, "nachher": {"farbe": "#d9a54a", "fuell": 0.4}}]))

labor("l-labneh", "Labneh aus Joghurt", ["Labneh", "Joghurtkäse", "abgetropfter Joghurt", "griechischer Joghurt selber machen"],
  "Joghurt im Tuch abgetropft wird über Nacht zu einem cremigen Frischkäse: Labneh.",
  "Wie ein Schwamm, der ausgedrückt wird: Das Wasser geht, die Substanz bleibt.",
  ["500 g Naturjoghurt (Vollfett)", "½ TL Salz", "Sieb, sauberes Tuch, Schüssel"], "12–24 Stunden",
  [("Joghurt mit Salz verrühren", "Salz würzt und zieht zusätzlich Molke heraus.", "osmose"),
   ("Im Tuch über einer Schüssel im Kühlschrank abtropfen lassen", "Das Eiweißnetz des Joghurts hält Fett und Eiweiß fest, die Molke tropft hindurch.", None),
   ("Nach 6–8 Stunden: griechischer Joghurt. Nach 24 Stunden: streichfester Labneh", "Je mehr Molke weg ist, desto fester und haltbarer, weil weniger freies Wasser bleibt.", "wasseraktivitaet")],
  "Etwa 250 g Labneh und 250 ml Molke (Richtwert).",
  "Gekühlt etwa eine Woche. Zu Kugeln geformt in Olivenöl länger.",
  ["Mit Olivenöl, Za’atar und Brot.", "Statt Frischkäse auf Brot, in Dips und Saucen.", "Die Molke zum Brotbacken."],
  ["l-joghurt", "joghurt", "milchsaeuregaerung", "wasseraktivitaet"], ["w-milch"], [QM],
  vergleich=vg("Joghurt", "nach 24 Stunden", [{"label": "Tuch über Schüssel", "gefaess": "schuessel", "inhalt": "fluessig", "vorher": {"farbe": "#f6f1e3", "fuell": 0.1, "klumpen": 1, "klumpenfarbe": "#fbf7ec"}, "nachher": {"farbe": "#eef0d8", "fuell": 0.4, "klumpen": 0.55, "klumpenfarbe": "#fbf7ec"}}]))

for e in E:
    p = os.path.join(OUT, e["id"] + ".json"); json.dump(e, open(p, "w"), ensure_ascii=False, indent=2); open(p, "a").write("\n")

BACK = {"sahne": ["l-mascarpone"], "l-frischkaese": ["l-mascarpone"], "aroma-loeslichkeit": ["l-vanilleextrakt"], "zucker": ["l-puderzucker", "l-brauner-zucker"],
        "zucker-feuchtigkeit": ["l-brauner-zucker", "l-puderzucker"], "milch": ["l-buttermilch-ersatz", "l-dulce-de-leche"], "chemische-lockerung": ["l-buttermilch-ersatz"],
        "senf": ["l-senf"], "schaerfe": ["l-senf"], "enzym": ["l-senf"], "milchsaeuregaerung": ["l-sauerkraut", "l-labneh"], "w-gemuese": ["l-sauerkraut"],
        "laenger-haltbar": ["l-sauerkraut"], "basen-braeunung": ["l-dulce-de-leche"], "maillard-reaktion": ["l-dulce-de-leche"], "pektin": ["l-apfelpektin"],
        "gelbildung-pektin": ["l-apfelpektin"], "g-konfituere": ["l-apfelpektin"], "l-joghurt": ["l-labneh"], "joghurt": ["l-labneh"], "w-suesses": ["l-vanilleextrakt", "l-dulce-de-leche"],
        "w-milch": ["l-mascarpone", "l-labneh"], "g-pancakes": ["l-buttermilch-ersatz"]}
for id, ls in BACK.items():
    p = os.path.join(OUT, id + ".json")
    if not os.path.exists(p): print("fehlt", id); continue
    e = json.load(open(p))
    for l in ls:
        if l not in e.setdefault("links", []): e["links"].append(l)
    json.dump(e, open(p, "w"), ensure_ascii=False, indent=2); open(p, "a").write("\n")

mp = os.path.join(ROOT, "content/master-list.json"); M = json.load(open(mp)); by = {m["id"]: m for m in M["eintraege"]}
for e in E:
    if e["id"] not in by: M["eintraege"].append({"id": e["id"], "typ": "labor", "titel": e["titel"], "status": "geplant", "pilot": False, "links": e["links"], "welten": e["welten"], "synonyme": e["synonyme"], "verlinkt_von": [], "visual": {"vorlage": e["visual"]["vorlage"]}})
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
print(len(E), "Labor-Rezepte,", M["anzahl"], "in der Masterliste")
