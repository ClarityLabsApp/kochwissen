"""Batch 6: Welt Kuchen & Gebäck. Schreibt nach content/entries/ im Repo."""
import json, sys, os
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/kochwissen-app/content/entries"

QM = {"titel": "Harold McGee: On Food and Cooking (2004)", "stelle": "Kapitel Kuchen, Gebäck, Zucker"}
QB = {"titel": "America’s Test Kitchen: Baking powder vs. baking soda", "url": "https://www.americastestkitchen.com/cooksillustrated/articles/6262-what-is-the-difference-between-baking-powder-and-baking-soda-ask-paul"}
QK = {"titel": "KitchenAid: Why did my cake sink in the middle?", "url": "https://www.kitchenaid.com/pinch-of-help/stand-mixers/why-did-my-cake-sink-in-the-middle.html"}
QC = {"titel": "The Bake School: Why chill cookie dough", "url": "https://bakeschool.com/why-chill-cookie-dough/"}

E = []
def add(**k):
    k.setdefault("status", "entwurf"); k.setdefault("schwierigkeit", "einsteiger"); E.append(k)

add(id="w-gebaeck", typ="welt", titel="Kuchen & Gebäck", synonyme=["Kuchen", "Muffins", "Kekse", "Guetzli", "Mürbeteig", "Biskuit", "Tarte"],
    kurz="Gebäck ist ein Gleichgewicht: Mehl und Ei geben Halt, Zucker und Fett machen zart und saftig, Luft macht leicht.",
    bild_im_kopf="Wie ein Haus aus zwei Mannschaften: Die einen bauen Wände (Mehl, Ei), die anderen machen es gemütlich (Zucker, Fett). Zu viel von einer Seite, und es wird zäh oder stürzt ein.",
    was_passiert="Luft kommt durch Backpulver, Natron, eingeschlagene Luft oder Dampf in den Teig. Im Ofen dehnt sie sich aus, bis Eiweiß und Stärke fest werden und die Form halten. Zucker und Fett bremsen das Glutennetz, darum bleiben Kuchen zart.",
    warum_wichtig="Backen verzeiht weniger als Kochen, weil Mengen und Reihenfolge die Struktur bestimmen. Wer die Rollen kennt, kann trotzdem anpassen.",
    faustregeln=["Abwiegen statt abmessen.", "Zutaten auf Raumtemperatur bringen, wenn Butter schaumig gerührt wird.", "Den Ofen nicht öffnen, bevor der Teig fest ist."],
    links=["chemische-lockerung", "glutenbildung", "schaumbildung", "fluffig", "muerbe", "kuchen-sinkt-ein", "kekse-breit"],
    visual={"vorlage": "keine", "illustration": "a slice of simple sponge cake on a vintage plate with a fork"},
    quellen=[QM])

add(id="chemische-lockerung", typ="prozess", titel="Chemische Lockerung",
    synonyme=["Backpulver", "Natron", "Triebmittel", "Kuchen geht auf", "Treibmittel"],
    kurz="Backpulver und Natron bilden mit Säure und Feuchtigkeit Gasblasen. Im Ofen dehnen sie sich aus, bis der Teig fest wird.",
    bild_im_kopf="Wie eine Brausetablette im Wasser: Base und Säure treffen sich und sprudeln.",
    was_passiert="Natron ist eine Base. Trifft es auf Säure und Wasser, entsteht Kohlendioxid. Backpulver bringt die Säure gleich mit: Ein Teil reagiert schon beim Anrühren, ein zweiter Teil erst in der Ofenhitze. So geht der Kuchen genau dann auf, wenn er im Ofen ist. Wird der Teig fest, bleiben die Blasen eingeschlossen.",
    warum_wichtig="Erklärt, warum Natron Buttermilch oder Joghurt braucht, warum Teig nicht ewig stehen soll und warum zu viel Triebmittel den Kuchen einfallen lässt.",
    faustregeln=["Natron nur mit Säure im Rezept (Buttermilch, Joghurt, Zitrone, Honig).", "Teig mit Backpulver bald backen.",
                 "Zu viel Triebmittel schmeckt seifig und lässt den Kuchen zusammenfallen."],
    stellschrauben=[{"id": "temperatur", "wirkung": "Hitze löst die zweite Reaktion aus"}, {"id": "ph-wert", "wirkung": "Natron braucht Säure"}, {"id": "zeit", "wirkung": "lange stehen → Gas entweicht"}],
    mythos={"behauptung": "Mehr Backpulver gibt einen höheren Kuchen.", "richtig": "Nur bis zu einem Punkt. Zu viel Gas lässt den Teig schneller steigen, als er fest wird, und er fällt zusammen."},
    praxis=[{"welt": "w-gebaeck", "text": "Muffins, Rührkuchen, Pancakes: Backpulver. Buttermilch-Scones und Lebkuchen: oft Natron."},
            {"welt": "w-brot", "text": "Irisches Soda Bread geht ganz ohne Hefe nur mit Natron und Buttermilch auf."}],
    links=["backpulver", "natron", "saeure", "kuchen-sinkt-ein", "fluffig"],
    welten=["w-gebaeck"],
    visual={"vorlage": "zoom3-simulation"},
    quellen=[QB, QM])

add(id="karamellisierung", typ="prozess", titel="Karamellisierung", synonyme=["Karamell", "Zucker bräunen", "karamellisieren"],
    kurz="Wird reiner Zucker sehr heiß, zerfällt er in hunderte neue Stoffe: braune Farbe, Karamellaroma und am Ende Bitterkeit.",
    bild_im_kopf="Wie ein Sonnenuntergang im Topf: von farblos über gold und bernstein zu dunkelbraun. Kurz danach wird es Nacht, also bitter.",
    was_passiert="Anders als die Maillard-Reaktion braucht Karamellisierung kein Eiweiß, nur Zucker und hohe Hitze. Haushaltszucker beginnt ungefähr bei 160 °C zu karamellisieren. Je dunkler, desto weniger süß und desto bitterer.",
    warum_wichtig="Gibt Crème brûlée, Karamellsauce, gebrannten Mandeln und gerösteten Zwiebeln ihre Tiefe. Fast immer läuft sie zusammen mit der Maillard-Reaktion.",
    faustregeln=["Topf mit hellem Boden, damit man die Farbe sieht.", "Nicht rühren, eher schwenken, sonst kristallisiert der Zucker.",
                 "Bernsteinfarben ist meist ideal. Ein Schluck kaltes Wasser oder Sahne stoppt die Bräunung."],
    stellschrauben=[{"id": "temperatur", "wirkung": "heißer → dunkler"}, {"id": "zeit", "wirkung": "länger → bitterer"}],
    praxis=[{"welt": "w-suesses", "text": "Karamellsauce: Zucker bernsteinfarben schmelzen, dann warme Sahne und Butter einrühren."},
            {"welt": "w-gemuese", "text": "Bei Zwiebeln und Karotten laufen Karamellisierung und Maillard gemeinsam."}],
    links=["maillard-reaktion", "zucker", "zucker-karamellisieren", "karamell-kristallisiert"],
    welten=["w-suesses", "w-gemuese", "w-kaffee"],
    visual={"vorlage": "temperaturskala", "params": {"hinweis": "Richtwerte für Haushaltszucker",
            "skala": [{"c": 160, "name": "Zucker schmilzt und wird golden"}, {"c": 170, "name": "bernstein: Karamellaroma"}, {"c": 180, "name": "dunkel: kräftig, weniger süß"}, {"c": 200, "name": "verbrannt und bitter"}]}},
    quellen=[QM])

add(id="dampflockerung", typ="prozess", titel="Dampf lockert (Brandteig, Blätterteig)", schwierigkeit="fortgeschritten",
    synonyme=["Blätterteig", "Brandteig", "Windbeutel", "Dampf als Triebmittel"],
    kurz="Wasser im Teig wird im heißen Ofen zu Dampf und bläst Hohlräume auf. Blätterteig und Windbeutel gehen ganz ohne Backpulver auf.",
    bild_im_kopf="Wie ein Popcorn-Korn: Das Wasser darin wird zu Dampf und sprengt es auf.",
    was_passiert="Wasser dehnt sich beim Verdampfen enorm aus. Bei Blätterteig steckt es in dünnen Butter- und Teigschichten, der Dampf drückt die Schichten auseinander. Bei Brandteig bildet sich eine Hülle, die der Dampf wie einen Ballon aufbläst.",
    warum_wichtig="Erklärt, warum diese Teige sehr heiß gebacken werden müssen und warum Windbeutel zusammenfallen, wenn man den Ofen zu früh öffnet.",
    faustregeln=["Sehr heiß starten, damit schnell viel Dampf entsteht.", "Blätterteig kalt halten, damit die Butterschichten getrennt bleiben.", "Ofen erst öffnen, wenn das Gebäck fest und gebräunt ist."],
    stellschrauben=[{"id": "temperatur", "wirkung": "heißer → mehr Dampf, mehr Volumen"}],
    links=["verdampfen", "butter", "w-gebaeck"],
    welten=["w-gebaeck"],
    visual={"vorlage": "zoom3-simulation"},
    quellen=[QM])

# ---------------- ZIELE
add(id="fluffig", typ="ziel", titel="Fluffig", synonyme=["locker", "luftig", "fluffiger", "leicht", "Pancakes fluffig"],
    kurz="Fluffig heißt: viele kleine Gasblasen, die im Ofen festgehalten werden, und ein Teig, der zart genug ist, um nicht zäh zu sein.",
    bild_im_kopf="Wie ein Schwamm mit tausend kleinen Löchern statt ein Ziegelstein.",
    bedeutung="Gas kommt von Backpulver, Hefe, Eischnee oder Dampf. Fluffig wird es, wenn das Gas im richtigen Moment entsteht und der Teig fest wird, bevor es entweicht. Wenig Glutennetz hält das Ergebnis zart.",
    hebel=["chemische-lockerung", "schaumbildung", "hefegaerung", "glutenbildung", "mechanik"],
    was_passiert="Zu viel Rühren macht zäh und treibt Luft wieder hinaus. Zu wenig Triebmittel oder zu langes Stehen lässt den Teig flach bleiben.",
    faustregeln=["Trockene und nasse Zutaten nur kurz vermengen.", "Eischnee vorsichtig unterheben.", "Teig mit Backpulver nicht lange stehen lassen."],
    praxis=[{"welt": "w-gebaeck", "text": "Pancakes: Klümpchen im Teig sind in Ordnung. Glatt gerührt werden sie gummiartig."},
            {"welt": "w-eier", "text": "Soufflé und Omelette soufflé leben nur vom Eischnee."}],
    links=["unterheben", "aufschlagen", "chemische-lockerung", "pfannkuchen-gummig", "muffins-tunnel"],
    welten=["w-gebaeck", "w-eier"],
    visual={"vorlage": "punktmatrix"},
    quellen=[QB, QM])

add(id="luftig", typ="ziel", titel="Luftig", synonyme=["Volumen", "Mousse", "schaumig", "leicht"],
    kurz="Luftig heißt: Viel Luft wird eingeschlagen und festgehalten, durch Eischnee, geschlagene Sahne oder schaumig gerührte Butter.",
    bild_im_kopf="Wie Wolken: fast nur Luft, aber sie halten ihre Form.",
    bedeutung="Mechanisch eingeschlagene Luft braucht eine Hülle, die sie hält: Eiweiß, Fett oder Gelatine. Wird die Hülle zu schwer belastet oder zu lange bearbeitet, entweicht die Luft wieder.",
    hebel=["schaumbildung", "mechanik", "temperatur"],
    was_passiert="Butter und Zucker schaumig rühren schließt winzige Luftbläschen ein, die Backpulver später vergrößert. Eischnee und Sahne tragen Mousse und Biskuit.",
    faustregeln=["Butter zum Schaumigrühren weich, aber nicht geschmolzen.", "Sahne gut gekühlt schlagen.", "Schwere Massen zuerst mit etwas Schaum lockern, dann den Rest unterheben."],
    links=["aufschlagen", "unterheben", "schaumbildung"],
    welten=["w-gebaeck", "w-suesses"],
    visual={"vorlage": "punktmatrix"},
    quellen=[QM])

add(id="muerbe", typ="ziel", titel="Mürbe", synonyme=["krümelig", "Mürbeteig", "zart", "kurz"],
    kurz="Mürbe heißt: Der Teig bricht zart und zerfällt im Mund, weil kaum ein Glutennetz entstanden ist.",
    bild_im_kopf="Wie Sand, der nur locker zusammenklebt, statt wie Kaugummi.",
    bedeutung="Fett umhüllt das Mehl, bevor Wasser dazukommt. So können sich die Eiweiße kaum verbinden. Wenig Wasser, kalte Butter und kurzes Arbeiten halten den Teig mürbe.",
    hebel=["glutenbildung", "fettgehalt", "mechanik", "temperatur"],
    was_passiert="Jede Minute Kneten und jeder Schluck Wasser zu viel stärkt das Netz und macht den Teig zäh. Ruhen im Kühlschrank entspannt ihn und festigt die Butter.",
    faustregeln=["Kalte Butter, kurz zusammendrücken, nicht kneten.", "So wenig Wasser wie möglich.", "Vor dem Ausrollen kalt stellen."],
    links=["muerbeteig-zaeh", "glutenbildung", "fett", "blindbacken"],
    welten=["w-gebaeck"],
    visual={"vorlage": "punktmatrix"},
    quellen=[QM])

# ---------------- TECHNIKEN
add(id="blindbacken", typ="technik", titel="Blindbacken", synonyme=["vorbacken", "Boden vorbacken", "mit Hülsenfrüchten backen"],
    kurz="Den Tarteboden vorbacken, bevor die Füllung hineinkommt. So wird er knusprig statt durchgeweicht.",
    bild_im_kopf="Wie einen Regenschirm aufspannen, bevor es regnet.",
    was_passiert="Ein roher Boden unter einer nassen Füllung kann nie richtig trocknen und bräunen. Vorgebacken ist er schon fest und trocken. Gewichte wie getrocknete Hülsenfrüchte verhindern, dass er Blasen wirft und der Rand zusammenrutscht.",
    schritte=["Teig in die Form legen, mit einer Gabel einstechen, kalt stellen.", "Mit Backpapier auslegen und mit getrockneten Hülsenfrüchten füllen.",
              "Bei etwa 180–200 °C rund 15 Minuten backen.", "Papier und Gewichte entfernen, 5–10 Minuten weiterbacken, bis der Boden trocken und leicht golden ist.",
              "Dann füllen und fertig backen."],
    wirkt_auf=["knusprig", "muerbe"],
    links=["boden-durchgeweicht", "muerbe", "verdampfen"],
    welten=["w-gebaeck"],
    visual={"vorlage": "ablauf"},
    quellen=[QM])

add(id="zucker-karamellisieren", typ="technik", titel="Zucker karamellisieren", schwierigkeit="fortgeschritten", synonyme=["Karamell machen", "Karamellsauce", "trockenes Karamell"],
    kurz="Zucker schmelzen und bräunen, bis er bernsteinfarben ist. Mit oder ohne Wasser.",
    bild_im_kopf="Wie ein Ampelsignal: golden heißt los, bernstein heißt jetzt, dunkelbraun heißt sofort stoppen.",
    was_passiert="Beim trockenen Karamell schmilzt Zucker direkt. Beim nassen Karamell löst man ihn erst in Wasser, das verdampft, dann bräunt der Zucker gleichmäßiger. Rühren kann ungelösten Zucker an die Wand bringen und Kristalle auslösen.",
    schritte=["Zucker in einen Topf mit hellem Boden geben, nach Wunsch mit etwas Wasser.", "Bei mittlerer Hitze schmelzen, nicht rühren, nur schwenken.",
              "Zuckerkristalle am Rand mit einem nassen Pinsel lösen.", "Bei Bernsteinfarbe vom Herd nehmen.", "Vorsichtig warme Sahne oder Butter einrühren, es spritzt."],
    wirkt_auf=["mehr-geschmack", "farbe"],
    links=["karamellisierung", "zucker-kristallisation", "karamell-kristallisiert"],
    welten=["w-suesses"],
    visual={"vorlage": "ablauf"},
    quellen=[QM])

# ---------------- ZUTATEN
add(id="zucker", typ="zutat", titel="Zucker", synonyme=["Kristallzucker", "Puderzucker", "Rohzucker", "brauner Zucker"],
    kurz="Zucker süßt nicht nur. Er hält Kuchen saftig, macht Teig zart, bräunt die Kruste und stabilisiert Eischnee.",
    bild_im_kopf="Wie ein Schwamm im Teig: Er hält Wasser fest und lässt den Kuchen langsamer austrocknen.",
    rolle=[{"rolle": "hält Wasser, macht saftig", "prozess": "saftig"},
           {"rolle": "bremst das Glutennetz, macht zart", "prozess": "glutenbildung"},
           {"rolle": "bräunt und karamellisiert", "prozess": "karamellisierung"},
           {"rolle": "stabilisiert Eischnee", "prozess": "schaumbildung"},
           {"rolle": "lässt Kekse breit laufen", "prozess": "kekse-breit"}],
    was_passiert="Zucker löst sich im Teigwasser und hält es fest. Er schiebt sich zwischen Eiweiße und Stärke und macht Gebäck dadurch zarter. Im Ofen bräunt er die Oberfläche.",
    faustregeln=["Zucker im Rezept zu stark reduzieren macht Kuchen trocken und zäh, nicht nur weniger süß.", "Brauner Zucker hält mehr Feuchtigkeit: saftigere, weichere Kekse."],
    links=["karamellisierung", "kuchen-trocken", "kekse-breit", "schaumbildung"],
    welten=["w-gebaeck", "w-suesses"],
    visual={"vorlage": "punktmatrix"},
    quellen=[QM, QC])

add(id="honig", typ="zutat", titel="Honig & Sirup", synonyme=["Honig", "Ahornsirup", "Zuckersirup", "Melasse"],
    kurz="Honig und Sirup sind flüssiger Zucker mit etwas Säure. Sie bräunen schneller und halten Gebäck feuchter als Kristallzucker.",
    bild_im_kopf="Wie Zucker im Feuchtigkeitsmantel.",
    rolle=[{"rolle": "bräunt schneller", "prozess": "maillard-reaktion"},
           {"rolle": "hält Gebäck weich", "prozess": "saftig"},
           {"rolle": "bringt Säure für Natron", "prozess": "chemische-lockerung"}],
    was_passiert="Honig enthält viel Fruchtzucker und etwas Säure. Fruchtzucker bräunt bei niedrigerer Temperatur und zieht Feuchtigkeit an.",
    faustregeln=["Mit Honig gebackenes etwas kühler backen, es bräunt schneller.", "Lebkuchen bleiben dank Honig lange weich."],
    links=["zucker", "maillard-reaktion", "chemische-lockerung"],
    welten=["w-gebaeck"],
    visual={"vorlage": "punktmatrix"},
    quellen=[QM])

add(id="backpulver", typ="zutat", titel="Backpulver", synonyme=["Triebmittel", "Backtriebmittel", "Weinsteinbackpulver"],
    kurz="Backpulver ist Natron mit eingebauter Säure und etwas Stärke. Es reagiert einmal beim Anrühren und noch einmal in der Ofenhitze.",
    bild_im_kopf="Wie ein Brausepulver mit Zeitzünder.",
    rolle=[{"rolle": "bildet Gas beim Anrühren", "prozess": "chemische-lockerung"},
           {"rolle": "bildet mehr Gas in der Hitze", "prozess": "chemische-lockerung"}],
    was_passiert="Die Stärke hält Natron und Säure trocken getrennt. Mit Flüssigkeit beginnt die erste Reaktion, die zweite Säure reagiert erst bei Hitze. Altes oder feucht gelagertes Backpulver verliert seine Kraft.",
    faustregeln=["Test: Ein Teelöffel in heißem Wasser muss kräftig sprudeln.", "Trocken und gut verschlossen lagern."],
    links=["chemische-lockerung", "natron", "kuchen-sinkt-ein"],
    welten=["w-gebaeck"],
    visual={"vorlage": "punktmatrix"},
    quellen=[QB])

add(id="fett", typ="zutat", titel="Fett allgemein", synonyme=["Butter", "Öl", "Margarine", "Schmalz"],
    kurz="Fett macht Gebäck zart, weil es das Mehl umhüllt, hält es saftig und trägt Geschmack. Welches Fett, entscheidet über die Textur.",
    bild_im_kopf="Wie ein Regenmantel ums Mehl: Wasser kommt schlechter heran, das Netz bleibt schwach.",
    rolle=[{"rolle": "umhüllt Mehl, macht mürbe", "prozess": "glutenbildung"},
           {"rolle": "schaumig gerührt: hält Luft", "prozess": "schaumbildung"},
           {"rolle": "schmilzt und lässt Kekse breit laufen", "prozess": "kekse-breit"}],
    was_passiert="Festes Fett wie kalte Butter bleibt in Stückchen und gibt Schichten. Weiche Butter lässt sich mit Zucker schaumig rühren und hält Luft. Öl macht Kuchen besonders saftig, kann aber keine Luft halten.",
    faustregeln=["Kalte Butter für Mürbeteig und Blätterteig, weiche für Rührkuchen, Öl für saftige Kuchen."],
    links=["glutenbildung", "muerbe", "kekse-breit", "butter", "oel"],
    welten=["w-gebaeck", "w-fleisch"],
    visual={"vorlage": "punktmatrix"},
    quellen=[QM, QC])

# ---------------- STELLSCHRAUBEN
add(id="zuckergehalt", typ="stellschraube", titel="Zuckermenge", synonyme=["weniger Zucker", "mehr Zucker", "Süße"],
    kurz="Mehr Zucker heißt nicht nur süßer: Gebäck wird zarter, feuchter, dunkler und läuft breiter.",
    bild_im_kopf="Ein Regler zwischen Brot und Bonbon.",
    was_passiert="Zucker bindet Wasser, bremst Gluten und Eiweißgerinnung und bräunt. Weniger Zucker macht Gebäck fester, trockener und heller.",
    faustregeln=["Zucker um höchstens ein Viertel reduzieren, sonst leidet die Textur.", "Mehr Zucker in Cremes lässt sie später gerinnen."],
    links=["zucker", "kuchen-trocken", "kekse-breit", "eiweiss-gerinnung"],
    visual={"vorlage": "skala", "params": {"links": "wenig Zucker: fester, trockener, heller", "rechts": "viel Zucker: zarter, feuchter, dunkler, läuft breiter"}},
    quellen=[QM])

add(id="fettgehalt", typ="stellschraube", titel="Fettmenge", synonyme=["weniger Fett", "mehr Butter"],
    kurz="Mehr Fett macht zarter, saftiger und reicher, aber auch weicher und breiter laufend.",
    bild_im_kopf="Ein Regler zwischen Brötchen und Butterkeks.",
    was_passiert="Fett umhüllt Mehl und bremst das Glutennetz. Es hält Feuchtigkeit und trägt Aromen. Zu viel Fett lässt Gebäck auseinanderlaufen oder fettig werden.",
    faustregeln=["Fett ersetzen ist heikel: Apfelmus statt Butter macht Kuchen zäher und gummiger."],
    links=["fett", "muerbe", "glutenbildung", "kekse-breit"],
    visual={"vorlage": "skala", "params": {"links": "wenig Fett: fester, zäher, trockener", "rechts": "viel Fett: zart, mürbe, reich"}},
    quellen=[QM])

add(id="mechanik", typ="stellschraube", titel="Mechanik (kneten, schlagen, rühren)", synonyme=["kneten", "rühren", "schlagen", "mixen"],
    kurz="Wie viel und wie kräftig du bearbeitest, entscheidet über Netz, Luft und Emulsion.",
    bild_im_kopf="Ein Regler zwischen Streicheln und Durchkneten.",
    was_passiert="Kneten stärkt das Glutennetz, Schlagen bringt Luft hinein und zerteilt Fett in feine Tröpfchen. Zu viel davon macht Kuchen zäh, Eischnee krümelig und Sahne zu Butter.",
    faustregeln=["Brot: viel. Kuchen: wenig. Eischnee: bis glänzend steif, dann aufhören."],
    links=["glutenbildung", "schaumbildung", "emulsion", "muffins-tunnel"],
    visual={"vorlage": "skala", "params": {"links": "wenig: zart, wenig Netz", "rechts": "viel: starkes Netz, viel Luft, Gefahr zu überarbeiten"}},
    quellen=[QM])

add(id="ph-wert", typ="stellschraube", titel="pH-Wert (sauer – basisch)", synonyme=["sauer", "basisch", "alkalisch", "Säure"],
    kurz="Ob eine Umgebung sauer oder basisch ist, verändert Bräunung, Farbe, Biss und Triebkraft.",
    bild_im_kopf="Eine Waage zwischen Zitrone und Natron.",
    was_passiert="Basisch beschleunigt Bräunung und macht Gemüse weich. Sauer hält Gemüse fest, färbt Rotkohl rot und stoppt das Braunwerden von Äpfeln. Natron braucht Säure, um Gas zu bilden.",
    faustregeln=["Für schnellere Bräunung eine Prise Natron.", "Für festes Gemüse und frischen Geschmack etwas Säure."],
    links=["natron", "saeure", "maillard-reaktion", "pektin-abbau", "anthocyan-farbe"],
    visual={"vorlage": "skala", "params": {"links": "sauer: fest, rot, frisch", "mitte": "neutral", "rechts": "basisch: bräunt schnell, weich, blau"}},
    quellen=[QM])

# ---------------- SYMPTOME
def sym(**k): add(typ="symptom", welten=["w-gebaeck"], visual={"vorlage": "entscheidungsbaum"}, **k)

sym(id="kuchen-sinkt-ein", titel="Kuchen sinkt ein", synonyme=["Kuchen fällt zusammen", "Delle in der Mitte", "Kuchen eingefallen"],
    kurz="Der Kuchen ist schneller gestiegen, als er fest werden konnte, oder er kam zu früh aus dem Ofen.",
    bild_im_kopf="Wie ein Zelt, das man aufbaut, bevor die Stangen eingerastet sind.",
    ursachen=[{"titel": "Nicht durchgebacken", "haeufigkeit": 3, "prinzip": "eiweiss-gerinnung", "warum": "Die Mitte war noch flüssig und konnte das Gas nicht halten.", "fix": ["Stäbchenprobe in der Mitte", "Ofentemperatur mit einem Thermometer prüfen"]},
              {"titel": "Ofen zu früh geöffnet", "haeufigkeit": 2, "prinzip": "chemische-lockerung", "warum": "Kalte Luft lässt das Gas schrumpfen, bevor der Teig fest ist.", "fix": ["Erst nach zwei Dritteln der Backzeit öffnen", "Tür sanft schließen"]},
              {"titel": "Zu viel Triebmittel", "haeufigkeit": 2, "prinzip": "chemische-lockerung", "warum": "Zu viel Gas lässt den Teig zu schnell steigen, dann fällt er zusammen.", "fix": ["Backpulver genau abwiegen", "Nicht nach Gefühl nachgeben"]},
              {"titel": "Zu viel geschlagen", "haeufigkeit": 1, "prinzip": "schaumbildung", "warum": "Zu viel Luft ohne genug Struktur.", "fix": ["Nach Zugabe des Mehls nur noch kurz rühren"]}],
    diagnose={"q1": {"frage": "Ist die eingesunkene Stelle innen klitschig oder roh?", "antworten": [["Ja", "u0"], ["Nein, durchgebacken", "q2"]]},
              "q2": {"frage": "Hast du den Ofen in der ersten Hälfte der Backzeit geöffnet?", "antworten": [["Ja", "u1"], ["Nein", "q3"]]},
              "q3": {"frage": "Hast du das Backpulver genau abgewogen?", "antworten": [["Nicht genau", "u2"], ["Ja", "u3"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}, "u3": {"ursache": 3}},
    links=["chemische-lockerung", "backpulver", "eiweiss-gerinnung", "unterheben"], quellen=[QK, QM])

sym(id="kuchen-trocken", titel="Kuchen ist trocken", synonyme=["Kuchen bröselig", "Kuchen strohig", "trockener Kuchen"],
    kurz="Meist zu lange gebacken. Manchmal fehlt Zucker oder Fett, die Feuchtigkeit halten.",
    bild_im_kopf="Wie ein Schwamm, der zu lange in der Sonne lag.",
    ursachen=[{"titel": "Zu lange oder zu heiß gebacken", "haeufigkeit": 3, "prinzip": "verdampfen", "warum": "Jede Minute zu viel verdampft Wasser aus der Krume.", "fix": ["Früher prüfen", "Stäbchen darf feuchte Krümel haben, keinen nassen Teig"]},
              {"titel": "Zu viel Mehl", "haeufigkeit": 2, "prinzip": "staerkeverkleisterung", "warum": "Abgemessene Tassen enthalten oft deutlich mehr Mehl als gedacht.", "fix": ["Mehl abwiegen"]},
              {"titel": "Zucker oder Fett reduziert", "haeufigkeit": 1, "prinzip": "saftig", "warum": "Beide halten Wasser im Kuchen.", "fix": ["Höchstens ein Viertel weniger Zucker", "Etwas Joghurt oder Öl im Teig"]}],
    diagnose={"q1": {"frage": "Hast du dich genau an die Backzeit gehalten?", "antworten": [["Eher länger", "u0"], ["Ja", "q2"]]},
              "q2": {"frage": "Hast du das Mehl abgewogen?", "antworten": [["Nein, abgemessen", "u1"], ["Ja", "u2"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["zucker", "fett", "saftig", "zuckergehalt"], quellen=[QM])

sym(id="kuchen-klitschig", titel="Kuchen ist klitschig", synonyme=["speckig", "nicht durch", "klebrige Schicht", "Kuchen roh"],
    kurz="Ein Teil des Teigs ist nicht durchgebacken oder wieder zusammengefallen. Die Stärke ist nicht richtig verkleistert.",
    bild_im_kopf="Wie Pudding in einem Kuchenmantel.",
    ursachen=[{"titel": "Zu kurz gebacken", "haeufigkeit": 3, "prinzip": "staerkeverkleisterung", "warum": "Die Mitte erreicht nicht die Temperatur, bei der Stärke fest wird.", "fix": ["Länger backen, mit Alufolie abdecken, wenn die Oberfläche zu dunkel wird"]},
              {"titel": "Zu viel Flüssigkeit oder Obst", "haeufigkeit": 2, "prinzip": "verdampfen", "warum": "Saftiges Obst gibt Wasser ab und macht den Teig darunter nass.", "fix": ["Obst trocken tupfen und in etwas Mehl wenden", "Etwas länger backen"]},
              {"titel": "Ofen zu heiß", "haeufigkeit": 1, "prinzip": "waermeleitung", "warum": "Außen fertig, innen noch roh.", "fix": ["10–20 °C weniger, dafür länger"]}],
    diagnose={"q1": {"frage": "War Obst oder viel Flüssigkeit im Teig?", "antworten": [["Ja", "u1"], ["Nein", "q2"]]},
              "q2": {"frage": "War die Oberfläche schon dunkel, als du ihn herausgenommen hast?", "antworten": [["Ja", "u2"], ["Nein", "u0"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["staerkeverkleisterung", "kuchen-sinkt-ein"], quellen=[QM])

sym(id="muffins-tunnel", titel="Muffins haben Tunnel", synonyme=["Löcher im Muffin", "Muffins zäh", "Muffins spitz"],
    kurz="Der Teig wurde zu lange gerührt. Das Glutennetz ist zu stark, Gas sammelt sich in langen Kanälen.",
    bild_im_kopf="Wie Maulwurfsgänge im Rasen.",
    ursachen=[{"titel": "Zu lange gerührt", "haeufigkeit": 3, "prinzip": "glutenbildung", "warum": "Langes Rühren baut ein zähes Netz, das Gas in Tunneln führt.", "fix": ["Nur rühren, bis das Mehl verschwunden ist", "Klümpchen sind in Ordnung"]},
              {"titel": "Ofen zu heiß", "haeufigkeit": 1, "prinzip": "chemische-lockerung", "warum": "Außen fest, bevor innen das Gas verteilt ist: spitze Kuppel und Risse.", "fix": ["Temperatur prüfen"]}],
    diagnose={"q1": {"frage": "Hast du den Teig glatt gerührt?", "antworten": [["Ja", "u0"], ["Nein, nur kurz", "u1"]]}, "u0": {"ursache": 0}, "u1": {"ursache": 1}},
    links=["glutenbildung", "mechanik", "fluffig"], quellen=[QM])

sym(id="muerbeteig-zaeh", titel="Mürbeteig wird zäh", synonyme=["Mürbeteig hart", "Teig schrumpft", "Tarteboden zäh"],
    kurz="Zu viel Wasser, zu warme Butter oder zu viel Kneten haben ein Glutennetz aufgebaut.",
    bild_im_kopf="Wie Sand, der zu Beton geworden ist.",
    ursachen=[{"titel": "Zu viel geknetet", "haeufigkeit": 3, "prinzip": "glutenbildung", "warum": "Kneten verbindet die Eiweiße.", "fix": ["Nur kurz zusammendrücken"]},
              {"titel": "Zu viel Wasser", "haeufigkeit": 2, "prinzip": "glutenbildung", "warum": "Mit mehr Wasser bildet sich mehr Netz.", "fix": ["Wasser löffelweise, nur bis der Teig gerade hält"]},
              {"titel": "Butter zu warm", "haeufigkeit": 2, "prinzip": "glutenbildung", "warum": "Weiche Butter vermischt sich, statt das Mehl in Stückchen zu umhüllen.", "fix": ["Kalte Butter, kalte Hände, Teig zwischendurch kühlen"]}],
    diagnose={"q1": {"frage": "Hast du den Teig richtig geknetet?", "antworten": [["Ja", "u0"], ["Nein, nur kurz", "q2"]]},
              "q2": {"frage": "War die Butter weich oder der Teig sehr feucht?", "antworten": [["Butter weich", "u2"], ["Teig feucht", "u1"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["glutenbildung", "muerbe", "fett"], quellen=[QM])

sym(id="boden-durchgeweicht", titel="Boden ist durchgeweicht", synonyme=["Tarteboden nass", "matschiger Boden", "soggy bottom"],
    kurz="Die nasse Füllung hat den rohen Teig durchfeuchtet, bevor er backen konnte.",
    bild_im_kopf="Wie ein Pappteller unter nasser Suppe.",
    ursachen=[{"titel": "Nicht vorgebacken", "haeufigkeit": 3, "prinzip": "verdampfen", "warum": "Roher Teig unter feuchter Füllung trocknet nie richtig.", "fix": ["Blindbacken"]},
              {"titel": "Zu wenig Hitze von unten", "haeufigkeit": 2, "prinzip": "waermeleitung", "warum": "Der Boden bekommt in der Mitte des Ofens zu wenig Hitze.", "fix": ["Unterste Schiene", "Auf einem vorgeheizten Blech backen"]},
              {"titel": "Sehr flüssige Füllung", "haeufigkeit": 1, "prinzip": "verdampfen", "warum": "Viel Saft weicht jeden Boden auf.", "fix": ["Obst mit etwas Stärke oder gemahlenen Nüssen binden", "Boden mit Ei bestreichen und kurz backen"]}],
    diagnose={"q1": {"frage": "Hast du den Boden vorgebacken?", "antworten": [["Nein", "u0"], ["Ja", "q2"]]},
              "q2": {"frage": "Auf welcher Schiene hast du gebacken?", "antworten": [["Mitte oder oben", "u1"], ["Unten", "u2"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["blindbacken", "muerbe"], quellen=[QM])

sym(id="kekse-breit", titel="Kekse laufen breit", synonyme=["Guetzli zerlaufen", "Cookies flach", "Kekse zu dünn"],
    kurz="Die Butter ist geschmolzen, bevor die Ränder fest wurden.",
    bild_im_kopf="Wie ein Schneemann in der Sonne: Wenn er schneller schmilzt, als er friert, wird er flach.",
    ursachen=[{"titel": "Teig zu warm", "haeufigkeit": 3, "prinzip": "fettgehalt", "warum": "Butter schmilzt bei etwa 35 °C. Warmer Teig zerläuft sofort.", "fix": ["Teig vor dem Backen kalt stellen", "Blech zwischen den Durchgängen abkühlen lassen"]},
              {"titel": "Viel Zucker oder zu wenig Mehl", "haeufigkeit": 2, "prinzip": "glutenbildung", "warum": "Zucker verflüssigt sich im Ofen, Mehl gibt Halt.", "fix": ["Mehl abwiegen", "Etwas weniger Zucker oder etwas mehr Mehl"]},
              {"titel": "Ofen zu kühl", "haeufigkeit": 1, "prinzip": "waermeleitung", "warum": "Die Ränder brauchen zu lange, um fest zu werden.", "fix": ["Ofen ganz vorheizen", "Temperatur mit Thermometer prüfen"]}],
    diagnose={"q1": {"frage": "Kam der Teig direkt aus dem Kühlschrank?", "antworten": [["Nein", "u0"], ["Ja", "q2"]]},
              "q2": {"frage": "War der Ofen ganz vorgeheizt?", "antworten": [["Nicht sicher", "u2"], ["Ja", "u1"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["fett", "zucker", "zuckergehalt"], quellen=[QC])

sym(id="pfannkuchen-gummig", titel="Pfannkuchen werden gummig", synonyme=["Pancakes zäh", "Crêpes gummig", "Omeletten zäh"],
    kurz="Der Teig wurde zu lange gerührt und nicht geruht. Das Glutennetz ist zu stark.",
    bild_im_kopf="Wie ein Radiergummi statt ein Kissen.",
    ursachen=[{"titel": "Zu lange gerührt", "haeufigkeit": 3, "prinzip": "glutenbildung", "warum": "Rühren baut ein zähes Netz.", "fix": ["Nur kurz vermischen, Klümpchen sind in Ordnung"]},
              {"titel": "Nicht geruht", "haeufigkeit": 2, "prinzip": "glutenbildung", "warum": "Frisch gerührter Teig ist gespannt.", "fix": ["Crêpe-Teig 30 Minuten ruhen lassen"]},
              {"titel": "Zu wenig Hitze", "haeufigkeit": 1, "prinzip": "chemische-lockerung", "warum": "In der lauwarmen Pfanne entweicht das Gas, bevor der Teig fest ist.", "fix": ["Pfanne mittelheiß vorheizen"]}],
    diagnose={"q1": {"frage": "War der Teig ganz glatt gerührt?", "antworten": [["Ja", "u0"], ["Nein", "q2"]]},
              "q2": {"frage": "Hat der Teig geruht?", "antworten": [["Nein", "u1"], ["Ja", "u2"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["glutenbildung", "ruhezeit", "fluffig"], quellen=[QM])

os.makedirs(OUT, exist_ok=True)
for e in E:
    if e is None: continue
    json.dump(e, open(os.path.join(OUT, e["id"] + ".json"), "w"), ensure_ascii=False, indent=2)
print(len([e for e in E if e]), "Einträge geschrieben")
