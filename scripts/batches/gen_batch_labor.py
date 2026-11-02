"""Batch 11: Labor-Rezepte. Grundzutaten selber herstellen, jeder Schritt mit dem Prinzip dahinter."""
import json, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "content/entries")
QM = {"titel": "Harold McGee: On Food and Cooking (2004)"}
Q = {
  "bp": {"titel": "Smitten Kitchen: Make your own baking powder", "url": "https://smittenkitchen.com/2009/08/make-your-own-baking-powder/"},
  "jog": {"titel": "Leite’s Culinaria: How to make homemade yogurt", "url": "https://leitesculinaria.com/print/how-to-make-homemade-yogurt"},
  "pan": {"titel": "Dassana’s Veg Recipes: How to make paneer", "url": "https://www.vegrecipesofindia.com/how-to-make-paneer-homemade-paneer/"},
  "cf": {"titel": "America’s Test Kitchen: Crème fraîche", "url": "https://www.americastestkitchen.com/recipes/8069-creme-fraiche"},
  "sd": {"titel": "King Arthur Baking: Sourdough starter", "url": "https://www.kingarthurbaking.com/recipes/sourdough-starter-recipe"},
  "na": {"titel": "America’s Test Kitchen: Professional-quality soft pretzels at home", "url": "https://www.americastestkitchen.com/how_tos/6399-professional-quality-soft-pretzels-at-home"},
  "rp": {"titel": "Verbraucherzentrale Südtirol: Welches Öl zum Braten?", "url": "https://www.consumer.bz.it/de/print/pdf/node/16745"},
}
E = []
def labor(id, titel, syn, kurz, bild, material, dauer, momente, ergebnis, haltbarkeit, verwendung, links, welten, quellen, sicherheit=None, vergleich=None, schw="einsteiger"):
    e = dict(id=id, typ="labor", titel=titel, synonyme=syn, kurz=kurz, bild_im_kopf=bild, material=material, dauer=dauer,
             schluesselmomente=[{"schritt": s, "warum": w, **({"prinzip": p} if p else {})} for s, w, p in momente],
             ergebnis=ergebnis, haltbarkeit=haltbarkeit, verwendung=verwendung, links=links, welten=welten, quellen=quellen,
             status="entwurf", schwierigkeit=schw, visual={"vorlage": "vergleich", "params": vergleich} if vergleich else {"vorlage": "keine"})
    if sicherheit: e["sicherheit"] = sicherheit
    E.append(e)

labor("l-backpulver", "Backpulver selber mischen", ["Backpulver selber machen", "Backpulver Ersatz", "Natron Weinstein"],
  "Backpulver ist eine Mischung aus einer Base, einer Säure und etwas Stärke. Aus Natron und Weinstein lässt es sich in einer Minute selbst mischen.",
  "Wie ein Feuerwerk mit getrennt verpackter Zündschnur: Erst wenn Wasser dazukommt, geht es los.",
  ["1 TL Natron", "2 TL Weinsteinpulver (Weinsteinsäure oder Weinsteinbackpulver-Säure)", "1 TL Maisstärke", "ein trockenes Schraubglas"], "5 Minuten",
  [("Natron, Weinstein und Stärke trocken mischen", "Natron ist die Base, Weinstein die Säure. Trocken reagieren sie nicht miteinander.", "chemische-lockerung"),
   ("Stärke nicht weglassen", "Sie nimmt Luftfeuchtigkeit auf, bevor Säure und Base es tun, und hält die Mischung rieselfähig.", "staerke"),
   ("Im Teig mit Flüssigkeit verrühren und gleich backen", "Mit Wasser reagieren Säure und Base und bilden Kohlendioxid. Diese Mischung legt sofort los, darum nicht warten.", "chemische-lockerung"),
   ("Frische testen: ein wenig in heißes Wasser streuen", "Schäumt es kräftig, ist es noch aktiv.", None)],
  "Etwa 4 TL Backpulver, so viel wie ein Päckchen. 1 TL ersetzt 1 TL gekauftes Backpulver.",
  "Trocken und luftdicht einige Wochen. Feuchtigkeit startet die Reaktion zu früh.",
  ["Kuchen, Muffins und Pancakes, wenn das Päckchen fehlt.", "Für Leute, die phosphatfreies Backpulver wollen."],
  ["chemische-lockerung", "backpulver", "natron", "x-backpulver-kalt-heiss", "g-pancakes"], ["w-gebaeck"], [Q["bp"], QM],
  vergleich={"vorher": "trocken", "nachher": "mit Wasser", "vergleich": [{"label": "Mischung im Wasser", "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#eaf1f4", "blasen": 0}, "nachher": {"farbe": "#eaf1f4", "blasen": 1, "schaum": 0.5}}]})

labor("l-butter", "Butter selber machen", ["Butter herstellen", "Butter aus Rahm", "Buttermilch selber"],
  "Butter entsteht, wenn man Rahm so lange schlägt, bis die Fetttröpfchen zusammenkleben. Übrig bleibt Buttermilch.",
  "Wie eine Menschenmenge, die sich nach dem Konzert zu Grüppchen sammelt: Aus vielen Einzelnen werden wenige große Klumpen.",
  ["500 ml Vollrahm, kalt", "Mixer oder Handrührgerät", "Sieb, Schüssel mit Eiswasser", "Prise Salz nach Wunsch"], "20 Minuten",
  [("Kalten Rahm schlagen, über Schlagrahm hinaus", "Erst schließt das Schlagen Luft ein. Dann reißen die Hüllen der Fetttröpfchen, und das Fett beginnt zu verkleben.", "schaumbildung"),
   ("Weiterschlagen, bis es plötzlich spritzt", "Die Emulsion kippt: Aus Fett in Wasser wird ein Fettklumpen, Buttermilch trennt sich ab.", "emulsion"),
   ("Buttermilch abgießen und aufheben", "Sie ist die wässrige Phase mit Milcheiweiß und Milchzucker.", None),
   ("Butter in Eiswasser kneten, bis das Wasser klar bleibt", "Reste von Buttermilch würden schnell sauer werden und die Butter verderben.", "keimwachstum"),
   ("Nach Wunsch salzen und formen", "Salz würzt und macht die Butter haltbarer.", "wasseraktivitaet")],
  "Aus 500 ml Rahm etwa 200 g Butter und gut 250 ml Buttermilch (Richtwert).",
  "Gut gewaschen und gekühlt etwa eine Woche, gesalzen länger. Eingefroren einige Monate.",
  ["Aufs Brot, zum Backen, zum [[arosieren|Arosieren]].", "Die Buttermilch für Pancakes oder Zopf."],
  ["sahne-wird-butter", "x-butter-schuetteln", "butter", "emulsion", "l-bratbutter"], ["w-milch"], [QM],
  vergleich={"vorher": "Rahm", "nachher": "geschlagen", "vergleich": [{"label": "Rührschüssel", "gefaess": "schuessel", "inhalt": "fluessig", "vorher": {"farbe": "#fbf7ec", "fuell": 0.7, "klumpen": 0, "klumpenfarbe": "#f2d36b"}, "nachher": {"farbe": "#f4f1e6", "fuell": 0.35, "klumpen": 1, "klumpenfarbe": "#f2d36b"}}]})

labor("l-bratbutter", "Bratbutter und Ghee selber machen", ["Bratbutter", "Butterschmalz", "Ghee", "geklärte Butter", "Butter klären"],
  "Bratbutter ist Butter ohne Wasser und Milcheiweiß. Ohne die Teile, die verbrennen, verträgt sie viel mehr Hitze.",
  "Wie Goldwaschen: Man spült alles weg, was nicht glänzt, und behält das Reine.",
  ["250 g Butter", "kleiner Topf", "Löffel oder Schaumkelle", "Sieb mit Küchenpapier oder feinem Tuch", "sauberes Glas"], "30 Minuten",
  [("Butter bei kleiner Hitze schmelzen und leise köcheln lassen", "Das Wasser in der Butter verdampft. Es knistert, solange noch Wasser da ist.", "verdampfen"),
   ("Schaum von der Oberfläche abschöpfen", "Der Schaum ist Milcheiweiß, das aufsteigt.", None),
   ("Warten, bis es still wird und sich am Boden helle Flocken absetzen", "Ist kein Wasser mehr da, hört das Knistern auf. Das restliche Eiweiß sinkt zu Boden.", "verdampfen"),
   ("Für Ghee weiter erhitzen, bis die Flocken goldbraun sind", "Das Milcheiweiß bräunt und gibt ein nussiges Aroma ab.", "maillard-reaktion"),
   ("Durch das Tuch in ein sauberes Glas abgießen", "Ohne Wasser und Eiweiß raucht das Fett erst bei etwa 200 °C, Butter schon bei etwa 150 °C.", "rauchpunkt")],
  "Aus 250 g Butter etwa 200 g Bratbutter, denn Butter besteht zu rund vier Fünfteln aus Fett (Richtwert).",
  "Kühl und dunkel mehrere Monate. Ohne Wasser finden Keime kaum etwas zum Leben.",
  ["Schnitzel, Rösti und Bratkartoffeln bei hoher Hitze.", "Ghee für Currys und zum Anrösten von Gewürzen."],
  ["rauchpunkt", "butter", "g-roesti", "g-wiener-schnitzel", "aroma-blooming", "l-butter"], ["w-milch", "w-fleisch"], [Q["rp"], QM],
  sicherheit="Heißes Fett: Kinder nur zuschauen lassen, kein Wasser in die Nähe.",
  vergleich={"vorher": "Butter geschmolzen", "nachher": "geklärt", "vergleich": [{"label": "Topfinhalt", "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#f2d36b", "fuell": 0.6, "trueb": 0.6, "schaum": 0.5}, "nachher": {"farbe": "#e8b93a", "fuell": 0.5, "trueb": 0, "bodensatz": 0.6}}]})

labor("l-frischkaese", "Frischkäse mit Zitrone (Paneer)", ["Paneer", "Frischkäse selber machen", "Ricotta selber machen", "Käse aus Milch und Zitrone", "Hüttenkäse"],
  "Heiße Milch mit etwas Zitronensaft gerinnt in Sekunden zu Flocken. Abgetropft und gepresst wird daraus ein fester Frischkäse.",
  "Wie ein Fischernetz, das man durch den Teich zieht: Das Feste bleibt hängen, das Wasser läuft durch.",
  ["1 l Vollmilch", "2–4 TL Zitronensaft oder Essig", "Sieb, Gazetuch oder sauberes Küchentuch", "Teller und etwas Schweres zum Pressen"], "1 Stunde",
  [("Milch unter Rühren aufkochen", "Hitze lockert das Milcheiweiß (Kasein), damit es gleich vollständig ausflockt.", "eiweiss-denaturierung"),
   ("Hitze aus, Zitronensaft löffelweise einrühren", "Die Säure nimmt den Eiweißteilchen ihre Ladung. Sie stoßen sich nicht mehr ab und verklumpen.", "saeure-denaturierung"),
   ("Warten, bis die Molke klar und grünlich ist", "Dann ist alles Eiweiß ausgeflockt. Ist sie milchig, noch etwas Säure dazu.", "eiweiss-gerinnung"),
   ("In das Tuch abgießen und kurz mit Wasser spülen", "Spülen entfernt den Zitronengeschmack.", None),
   ("Einschlagen und 30–40 Minuten pressen", "Pressen drückt Molke heraus: kurz gepresst bleibt er weich wie Ricotta, lange gepresst wird er schnittfest.", None)],
  "Aus 1 l Vollmilch etwa 200 g Frischkäse.",
  "Gekühlt und abgedeckt 2–3 Tage.",
  ["Paneer in Würfeln für Currys: Er schmilzt nicht, weil er mit Säure statt mit Lab gemacht ist.", "Weich gepresst als Ricotta-Ersatz für Pasta und Kuchen.", "Die Molke zum Brotbacken."],
  ["saeure-denaturierung", "eiweiss-gerinnung", "milch", "kaese", "saeure"], ["w-milch"], [Q["pan"], QM],
  sicherheit="Kochende Milch kocht leicht über: Erwachsene übernehmen das Erhitzen.",
  vergleich={"vorher": "heiße Milch", "nachher": "mit Zitrone", "vergleich": [{"label": "Topf", "gefaess": "schuessel", "inhalt": "fluessig", "vorher": {"farbe": "#fbf9f2", "fuell": 0.8, "klumpen": 0, "klumpenfarbe": "#fffaf0"}, "nachher": {"farbe": "#e4ead0", "fuell": 0.8, "klumpen": 1, "klumpenfarbe": "#fffaf0"}}]})

labor("l-joghurt", "Joghurt selber machen", ["Joghurt herstellen", "Naturjoghurt", "Joghurt im Ofen", "Joghurt ohne Maschine"],
  "Milchsäurebakterien verwandeln warme Milch über Nacht in Joghurt. Ein paar Löffel gekaufter Joghurt reichen als Starter.",
  "Wie Hefe im Teig, nur für Milch: Ein paar Arbeiter genügen, über Nacht werden es Milliarden.",
  ["1 l Milch", "2 EL Naturjoghurt mit lebenden Kulturen", "Topf, Thermometer", "saubere Gläser", "Ofen mit Licht oder eine Wärmflasche in einer Kühlbox"], "6–12 Stunden",
  [("Milch auf 85–90 °C erhitzen und etwa 10 Minuten halten", "Die Hitze verändert das Molkeneiweiß. Es bindet später mehr Wasser, der Joghurt wird dicker.", "eiweiss-denaturierung"),
   ("Auf 43–46 °C abkühlen lassen", "In diesem Bereich arbeiten die Joghurtbakterien am besten. Über etwa 48 °C sterben sie.", None),
   ("Etwas Milch mit dem Joghurt glatt rühren, dann alles mischen", "So verteilen sich die Bakterien gleichmäßig.", None),
   ("Abgefüllt 4–12 Stunden warm halten, nicht bewegen", "Die Bakterien machen aus Milchzucker Milchsäure. Die Säure lässt das Milcheiweiß zu einem Gel stocken.", "milchsaeuregaerung"),
   ("Sobald er fest ist, in den Kühlschrank", "Kälte bremst die Bakterien: Je länger warm, desto saurer.", "keimwachstum")],
  "Etwa 1 l Joghurt. Abgetropft in einem Tuch wird daraus griechischer Joghurt oder Labneh.",
  "Gekühlt etwa eine Woche. Zwei Löffel davon sind der Starter für die nächste Portion.",
  ["Zum Frühstück, für Raita gegen Schärfe, für Marinaden.", "Abgetropft als Labneh mit Olivenöl."],
  ["milchsaeuregaerung", "joghurt", "milch", "schaerfe", "eiweiss-denaturierung"], ["w-milch"], [Q["jog"], QM],
  sicherheit="Sauber arbeiten. Riecht der Joghurt faulig, ist er rosa oder schimmelig: wegwerfen.",
  vergleich={"vorher": "warme Milch", "nachher": "nach der Nacht", "vergleich": [{"label": "Glas", "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#fbf9f2", "fuell": 0.75}, "nachher": {"farbe": "#f6f1e3", "fuell": 0.75, "trueb": 0.4, "klumpen": 0.8, "klumpenfarbe": "#fbf7ec"}}]})

labor("l-sauerteig", "Sauerteig ansetzen", ["Sauerteig selber machen", "Sauerteig-Starter", "Anstellgut", "Levain"],
  "Aus Mehl und Wasser entsteht in rund einer Woche ein Sauerteig: Wilde Hefen und Milchsäurebakterien aus dem Mehl vermehren sich, wenn man sie regelmäßig füttert.",
  "Wie ein Garten aus Samen, die schon in der Erde liegen: Man sät nichts, man gießt nur und jätet.",
  ["Vollkorn-Weizen- oder Roggenmehl für den Start", "Weißmehl zum Füttern", "Wasser", "Glas mit lockerem Deckel", "Waage"], "5–7 Tage",
  [("Tag 1: 50 g Vollkornmehl und 50 g Wasser mischen, 24 Stunden stehen lassen", "Im Mehl leben wilde Hefen und Milchsäurebakterien. Vollkorn bringt besonders viele mit.", "milchsaeuregaerung"),
   ("Tag 2: alles bis auf 50 g wegwerfen, mit 50 g Mehl und 50 g Wasser füttern", "Wegwerfen hält die Menge klein, frisches Mehl liefert neues Futter.", None),
   ("Ab Tag 3 zweimal täglich so füttern, warm bei etwa 21–26 °C", "Die Säure der Bakterien verdrängt unerwünschte Keime, die Hefen werden stärker.", "milchsaeuregaerung"),
   ("Bereit, wenn er sich 6–8 Stunden nach dem Füttern verdoppelt", "Dann sind genug Hefen da, um ein Brot zu heben.", "hefegaerung")],
  "Ein aktiver Sauerteig, der angenehm säuerlich riecht und voller Blasen ist.",
  "Im Kühlschrank aufbewahren und etwa einmal pro Woche füttern. Grauer Wasserfilm oben ist Hunger, kein Verderb: abgießen und füttern.",
  ["Für Sauerteigbrot, Pizza und Zopf mit Sauerteig.", "Die Reste beim Füttern für Pancakes oder Cracker."],
  ["sauerteig", "milchsaeuregaerung", "hefegaerung", "w-brot", "vorteig"], ["w-brot"], [Q["sd"], QM],
  sicherheit="Riecht er faulig, ist er rosa, orange oder hat er pelzigen Schimmel: neu beginnen.",
  vergleich={"vorher": "frisch gefüttert", "nachher": "nach 6–8 Stunden", "vergleich": [{"label": "Anstellgut", "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#e9dcc0", "fuell": 0.3, "blasen": 0.1}, "nachher": {"farbe": "#e9dcc0", "fuell": 0.68, "blasen": 0.9}}]})

labor("l-creme-fraiche", "Crème fraîche selber machen", ["Crème fraîche", "Sauerrahm selber", "Creme fraiche herstellen"],
  "Rahm mit einem Schuss Buttermilch wird bei Raumtemperatur über Nacht dick und mild säuerlich.",
  "Wie ein Gast, der seine Freunde mitbringt: Ein Löffel Buttermilch bringt die Bakterien, die den ganzen Rahm verwandeln.",
  ["250 ml Vollrahm", "2 EL Buttermilch mit lebenden Kulturen", "sauberes Glas"], "12–24 Stunden",
  [("Rahm und Buttermilch im Glas verrühren", "Die Buttermilch bringt Milchsäurebakterien mit.", None),
   ("Abgedeckt bei Raumtemperatur 12–24 Stunden stehen lassen", "Die Bakterien bilden Milchsäure, die das Eiweiß im Rahm eindickt, und typische buttrige Aromen.", "milchsaeuregaerung"),
   ("Wenn sie dick ist, kalt stellen", "Kälte bremst die Bakterien und macht sie noch fester.", None)],
  "Etwa 250 ml Crème fraîche.",
  "Gekühlt bis etwa einen Monat.",
  ["Für Saucen: Sie gerinnt beim Kochen nicht, weil sie so viel Fett hat.", "Auf Flammkuchen, zu Suppen, zu Desserts."],
  ["milchsaeuregaerung", "sahne", "sauce-trennt-sich", "w-saucen"], ["w-milch", "w-saucen"], [Q["cf"], QM])

labor("l-gebackenes-natron", "Gebackenes Natron für Laugengebäck", ["Natron backen", "Laugenersatz", "Brezel ohne Lauge", "Natriumcarbonat", "Waschsoda Küche"],
  "Im Ofen gebackenes Natron wird zu Soda, einer stärkeren Base. Damit werden Brezeln fast so braun wie mit echter Lauge, ohne deren Gefahr.",
  "Wie Kaffee, der beim Rösten kräftiger wird: Dieselbe Bohne, aber eine Stufe stärker.",
  ["etwa 200 g Natron", "Backblech mit Backpapier (kein Aluminium)", "Schraubglas", "Handschuhe für das Tauchbad"], "2 Stunden",
  [("Natron auf dem Blech verteilen, 2 Stunden bei 120 °C backen", "Hitze treibt Wasser und Kohlendioxid aus. Aus Natron wird Soda (Natriumcarbonat), die Base wird stärker: pH etwa 11 statt 8.", "basen-braeunung"),
   ("Abkühlen lassen und trocken in ein Glas füllen, beschriften", "Soda sieht aus wie Natron, ist aber reizender. Darum beschriften.", None),
   ("Zum Tauchen etwa 150 g in knapp 500 ml warmem Wasser lösen", "Die Lauge muss kräftig sein, damit die Oberfläche genug Base aufnimmt (Menge nach America’s Test Kitchen).", None),
   ("Brezeln kurz eintauchen, abspülen, salzen und heiß backen", "Die basische Oberfläche bräunt schnell und glänzt.", "maillard-reaktion")],
  "Rund 130 g Soda aus 200 g Natron, denn beim Backen geht Gewicht als Wasser und Kohlendioxid verloren (Richtwert).",
  "Trocken und verschlossen fast unbegrenzt.",
  ["Laugenbrezeln, Laugenbrötchen, Laugenzopf.", "Eine Prise im Kochwasser für chinesische Nudeln mit Biss."],
  ["laugen", "basen-braeunung", "natron", "maillard-reaktion", "w-brot"], ["w-brot"], [Q["na"], QM],
  sicherheit="Soda reizt Haut und Augen: Handschuhe tragen, nicht ins Gesicht bringen, außer Reichweite von Kindern aufbewahren.", schw="fortgeschritten")

for e in E:
    p = os.path.join(OUT, e["id"] + ".json"); json.dump(e, open(p, "w"), ensure_ascii=False, indent=2); open(p, "a").write("\n")

# Laugen-Technik an die geprüften Mengen anpassen
p = os.path.join(OUT, "laugen.json"); t = json.load(open(p))
t["schritte"] = ["Gebackenes Natron herstellen (siehe Labor-Rezept): 2 Stunden bei 120 °C.", "Etwa 150 g davon in knapp 500 ml warmem Wasser lösen.", "Geformte Brezeln kurz eintauchen, kurz abspülen, abtropfen lassen.", "Mit grobem Salz bestreuen und heiß backen."]
if "l-gebackenes-natron" not in t["links"]: t["links"].append("l-gebackenes-natron")
t["quellen"] = [Q["na"], QM]
json.dump(t, open(p, "w"), ensure_ascii=False, indent=2); open(p, "a").write("\n")

BACK = {"backpulver": ["l-backpulver"], "chemische-lockerung": ["l-backpulver"], "butter": ["l-butter", "l-bratbutter"], "sahne-wird-butter": ["l-butter"], "x-butter-schuetteln": ["l-butter"],
        "rauchpunkt": ["l-bratbutter"], "milch": ["l-frischkaese", "l-joghurt"], "kaese": ["l-frischkaese"], "joghurt": ["l-joghurt"], "milchsaeuregaerung": ["l-joghurt", "l-sauerteig", "l-creme-fraiche"],
        "sauerteig": ["l-sauerteig"], "w-brot": ["l-sauerteig", "l-gebackenes-natron"], "natron": ["l-gebackenes-natron", "l-backpulver"], "basen-braeunung": ["l-gebackenes-natron"], "sahne": ["l-creme-fraiche"],
        "w-milch": ["l-butter", "l-frischkaese", "l-joghurt", "l-creme-fraiche"], "saeure-denaturierung": ["l-frischkaese"]}
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
for id, ls in list(BACK.items()) + [("laugen", ["l-gebackenes-natron"])]:
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
