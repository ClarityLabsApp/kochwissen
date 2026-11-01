"""Batch 9: Gerichte und Experimente. Schreibt Einträge und ergänzt die Masterliste."""
import json, sys, os
ROOT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/kochwissen-app"
OUT = os.path.join(ROOT, "content/entries")
QM = {"titel": "Harold McGee: On Food and Cooking (2004)"}

E = []
def add(**k):
    k.setdefault("status", "entwurf"); k.setdefault("schwierigkeit", "einsteiger"); k.setdefault("quellen", [QM]); E.append(k)

def gericht(id, titel, syn, kurz, bild, momente, links, welten, schw="einsteiger"):
    add(id=id, typ="gericht", titel=titel, synonyme=syn, kurz=kurz, bild_im_kopf=bild, schwierigkeit=schw,
        schluesselmomente=[{"schritt": s, "warum": w, "prinzip": p} for s, w, p in momente],
        links=links, welten=welten, visual={"vorlage": "ablauf"})

def experiment(id, titel, syn, kurz, material, schritte, beob, erkl, links, welten, dauer, sicher=None):
    k = dict(id=id, typ="experiment", titel=titel, synonyme=syn, kurz=kurz, material=material, schritte=schritte,
             beobachtung=beob, erklaerung=erkl, links=links, welten=welten, dauer=dauer, visual={"vorlage": "ablauf"})
    if sicher: k["sicherheit"] = sicher
    add(**k)

# ======================= GERICHTE =======================
gericht("g-roesti", "Rösti", ["Röschti", "Kartoffelrösti", "Bratkartoffeln gerieben"],
    "Rösti wird knusprig, wenn die Stärke richtig mitspielt: gekochte Kartoffeln vom Vortag, heiße Pfanne, Geduld.",
    "Wie ein Kuchen aus Kartoffelfäden, den die Stärke zusammenklebt und die Hitze außen verkrustet.",
    [("Kartoffeln am Vortag in der Schale kochen und abkühlen lassen", "Abgekühlte Stärke wird fester. Die Raspel zerfallen nicht und kleben nicht zu Brei.", "retrogradation"),
     ("Grob raffeln und salzen, erst kurz vor dem Braten", "Salz zieht Wasser. Zu früh gesalzen werden die Raspel nass.", "osmose"),
     ("In heißer Butter oder Bratbutter flach andrücken", "Kontakt mit der heißen Fläche und Fett: Die Unterseite bräunt gleichmäßig.", "maillard-reaktion"),
     ("Nicht bewegen, bis sich der Rand löst, dann wenden", "Die Kruste löst sich von selbst, wenn sie fertig ist. Vorher reißt sie.", "knusprig")],
    ["retrogradation", "staerkeverkleisterung", "maillard-reaktion", "bratkartoffeln-kleben", "knusprig"], ["w-kartoffeln"])

gericht("g-wiener-schnitzel", "Wiener Schnitzel", ["Schnitzel", "paniertes Schnitzel", "Kalbsschnitzel"],
    "Die soufflierte Panade entsteht, weil Dampf aus dem Fleisch die Panade abhebt, während sie im heißen Fett knusprig wird.",
    "Wie ein Zelt, das sich über dem Fleisch aufbläht.",
    [("Dünn klopfen", "Dünnes Fleisch ist gar, bevor die Panade verbrennt.", "waermeleitung"),
     ("Mehl, Ei, Paniermehl, nicht andrücken", "Lose Panade kann sich vom Fleisch heben und Wellen werfen.", "panieren"),
     ("In reichlich heißem Fett schwimmend backen und die Pfanne schwenken", "Heißes Fett läuft über die Oberseite. Dampf aus dem Fleisch bläht die Panade auf.", "verdampfen"),
     ("Auf Küchenpapier oder Gitter kurz abtropfen", "Abtropfen verhindert, dass die Panade Fett nachzieht.", "frittiertes-fettig")],
    ["panieren", "panade-faellt-ab", "verdampfen", "knusprig"], ["w-fleisch", "w-frittieren"])

gericht("g-risotto", "Risotto", ["Risotto alla milanese", "Safranrisotto"],
    "Risotto wird cremig ohne Sahne: Rühren löst Stärke vom Reiskorn, und am Schluss bindet Butter und Käse alles zu einer Emulsion.",
    "Wie Perlen, die ihren eigenen Kleister abgeben.",
    [("Reis in Fett glasig anschwitzen", "Die Körner werden außen versiegelt und kochen gleichmäßiger.", "staerkeverkleisterung"),
     ("Heiße Brühe nach und nach zugeben und rühren", "Reibung löst Stärke von der Oberfläche, die die Flüssigkeit bindet.", "staerkeverkleisterung"),
     ("Wenn der Kern noch leicht Biss hat, vom Herd nehmen", "Der Reis gart in der Hitze weiter.", "zeit"),
     ("Kalte Butter und Parmesan kräftig einrühren (mantecare)", "Fett, Stärke und Käse verbinden sich zu einer cremigen Emulsion.", "emulsion")],
    ["mantecare", "staerkeverkleisterung", "cremig", "emulsion"], ["w-getreide"], "fortgeschritten")

gericht("g-mayonnaise", "Mayonnaise", ["Mayo", "Aioli"],
    "Mayonnaise ist eine Emulsion: Ein Eigelb kann eine ganze Schüssel Öl in feinen Tröpfchen halten, wenn das Öl langsam kommt.",
    "Wie viele Gäste, die einzeln durch eine Tür kommen, statt alle auf einmal.",
    [("Eigelb, Senf, Säure und Salz verrühren", "Eigelb und Senf bringen die Emulgatoren mit.", "emulsion"),
     ("Öl zuerst tropfenweise einschlagen", "Am Anfang ist wenig Wasser da, um Tröpfchen aufzunehmen.", "emulgieren"),
     ("Wenn sie dick wird, Öl im dünnen Strahl", "Die stabile Emulsion nimmt jetzt schneller Öl auf.", "emulsion"),
     ("Zu dick? Ein paar Tropfen Wasser", "Wasser gibt den Tröpfchen wieder Platz.", "mayo-gerinnt")],
    ["emulsion", "emulgieren", "mayo-gerinnt", "eigelb"], ["w-saucen", "w-eier"])

gericht("g-steak", "Steak aus der Pfanne", ["Rindssteak", "Entrecôte", "Ribeye braten"],
    "Ein gutes Steak braucht zwei Dinge gleichzeitig: eine trockene, sehr heiße Oberfläche für die Kruste und ein sanft erwärmtes Inneres.",
    "Außen Grill, innen Badewanne.",
    [("Am Vortag salzen und unbedeckt kühlen", "Salz zieht ein und hält Wasser, die Oberfläche trocknet.", "trockensalzen"),
     ("Trocken tupfen, Pfanne stark vorheizen", "Nur eine trockene Oberfläche in heißer Pfanne bräunt.", "maillard-reaktion"),
     ("Wenden, sobald es sich löst, mit Thermometer garen", "Die Kerntemperatur entscheidet über saftig oder trocken.", "eiweiss-denaturierung"),
     ("Am Ende Butter, Knoblauch, Thymian zum Arosieren", "Schäumende Butter bringt Aroma und bräunt nach.", "arosieren"),
     ("Kurz ruhen lassen und quer zur Faser schneiden", "Weniger Saft läuft aus, kürzere Fasern wirken zarter.", "ruhen-lassen")],
    ["maillard-reaktion", "steak-grau", "eiweiss-denaturierung", "rueckwaerts-garen", "anbraten"], ["w-fleisch"])

gericht("g-pommes", "Pommes frites", ["Pommes", "Fritten", "French Fries"],
    "Knusprige Pommes entstehen in zwei Bädern: erst garen, dann trocknen und bräunen.",
    "Erst Grundierung, dann Lack.",
    [("Schneiden und kalt wässern", "Spült losen Stärkefilm ab, der klebt und zu früh bräunt.", "kaltwasserbad"),
     ("Sehr gut trocknen", "Wasser auf der Oberfläche kostet Hitze und spritzt.", "verdampfen"),
     ("Bei etwa 160 °C hell vorfrittieren und abkühlen lassen", "Das Innere gart, eine dünne Haut bildet sich.", "staerkeverkleisterung"),
     ("Bei etwa 190 °C goldbraun frittieren", "Die Haut trocknet schnell aus und wird knusprig.", "zweimal-frittieren")],
    ["zweimal-frittieren", "kaltwasserbad", "knusprig", "frittiertes-fettig"], ["w-kartoffeln", "w-frittieren"])

gericht("g-hollandaise", "Sauce hollandaise", ["Hollandaise", "Béarnaise"],
    "Hollandaise ist eine warme Emulsion mit Eigelb, die zwischen zwei Fehlern balanciert: zu kalt trennt sie sich, zu heiß gerinnt das Ei.",
    "Wie ein Seiltanz zwischen Rührei und Butterlache.",
    [("Eigelb mit etwas Wasser und Säure über dem Wasserbad aufschlagen", "Das Eigelb dickt sanft ein und schließt Luft ein.", "eiweiss-gerinnung"),
     ("Immer wieder vom Wasserbad nehmen", "Über etwa 70 °C wird das Eigelb krümelig.", "wasserbad"),
     ("Warme, flüssige Butter langsam einschlagen", "Die Eigelbcreme emulgiert die Butter in feinen Tröpfchen.", "emulsion"),
     ("Warm, nicht heiß servieren", "Zu heiß gerinnt sie, zu kalt wird die Butter fest.", "hollandaise-flockt")],
    ["emulsion", "eiweiss-gerinnung", "hollandaise-flockt", "wasserbad"], ["w-saucen"], "fortgeschritten")

gericht("g-creme-brulee", "Crème brûlée", ["Creme brulee", "gebrannte Creme"],
    "Crème brûlée verbindet zwei Prinzipien: eine Eiercreme, die nur sanft stocken darf, und eine Zuckerschicht, die blitzschnell karamellisiert.",
    "Weich und knackig in einer Schale: unten Pudding, oben Glas.",
    [("Sahne, Eigelb und Zucker verrühren, nicht schaumig schlagen", "Luftblasen würden in der Creme sichtbar bleiben.", "eiweiss-gerinnung"),
     ("Im Wasserbad bei niedriger Ofentemperatur stocken lassen", "Das Wasser hält die Temperatur sanft und gleichmäßig.", "wasserbad"),
     ("Gut durchkühlen", "Die Creme wird fest, die Oberfläche trocken.", "eiweiss-gerinnung"),
     ("Dünn Zucker darüber und abflämmen", "Der Zucker karamellisiert in Sekunden, die Creme darunter bleibt kalt.", "karamellisierung")],
    ["eiweiss-gerinnung", "karamellisierung", "wasserbad", "creme-klumpig"], ["w-suesses"], "fortgeschritten")

gericht("g-pizza", "Pizza", ["Pizzateig", "Pizza napoletana"],
    "Eine gute Pizza braucht einen dehnbaren Teig mit Geschmack und einen Ofen, der so heiß ist wie möglich.",
    "Ein Ballon, der in Sekunden aufbläht und fest wird.",
    [("Teig lange und kühl gehen lassen", "Mehr Aroma, dehnbareres Netz.", "kalte-gare"),
     ("Vor dem Ausziehen temperieren und ruhen lassen", "Entspanntes Gluten schnurrt nicht zurück.", "teig-schnurrt"),
     ("Von Hand ausziehen, Rand nicht flach drücken", "Die Gasblasen im Rand machen den luftigen Cornicione.", "grosse-poren"),
     ("Auf vorgeheiztem Stein oder Stahl so heiß wie möglich backen", "Starke Hitze von unten gibt Ofentrieb und Kruste, bevor der Belag austrocknet.", "waermeleitung")],
    ["glutenbildung", "kalte-gare", "teig-schnurrt", "maillard-reaktion"], ["w-brot"])

gericht("g-zopf", "Zopf", ["Butterzopf", "Sonntagszopf", "Hefezopf"],
    "Der Zopf ist ein reicher Hefeteig: Butter und Milch machen ihn zart und goldbraun, bremsen aber die Hefe.",
    "Ein Brot im Sonntagsgewand: weicher, süßer, glänzender.",
    [("Teig gut kneten, bis er glatt ist", "Butter schwächt das Netz, darum braucht es Kneten, damit er trotzdem aufgeht.", "glutenbildung"),
     ("Etwas länger gehen lassen als Brot", "Butter und Zucker bremsen die Hefe.", "hefegaerung"),
     ("Flechten und nochmals kurz gehen lassen", "Die Stränge entspannen und gehen auf.", "ruhezeit"),
     ("Mit Ei bestreichen und backen", "Eiweiß und Zucker bräunen und glänzen.", "maillard-reaktion")],
    ["hefegaerung", "glutenbildung", "maillard-reaktion"], ["w-brot", "w-gebaeck"])

gericht("g-kaesefondue", "Käsefondue", ["Fondue", "Moitié-moitié"],
    "Fondue ist eine Käse-Emulsion. Wein und Stärke halten sie zusammen, zu viel Hitze lässt sie in Fett und Fäden zerfallen.",
    "Wie eine Sauce, die nur in ihrem Wohlfühlbereich zusammenhält.",
    [("Käse fein reiben und mit etwas Maisstärke mischen", "Stärke umhüllt das Eiweiß und verhindert Klumpen.", "staerkeverkleisterung"),
     ("Weißwein erhitzen, Käse portionsweise einrühren", "Die Säure im Wein hält das Käseeiweiß geschmeidig.", "saeure"),
     ("Nur leise köcheln, ständig rühren (Achterform)", "Zu viel Hitze zieht das Eiweiß zusammen, Fett tritt aus.", "eiweiss-gerinnung"),
     ("Trennt es sich: Spritzer Zitrone und etwas angerührte Stärke", "Säure und Stärke bringen die Emulsion zurück.", "emulsion")],
    ["kaese", "emulsion", "saeure", "sauce-trennt-sich"], ["w-milch"])

gericht("g-pancakes", "Pancakes", ["amerikanische Pfannkuchen", "fluffige Pfannkuchen"],
    "Pancakes werden fluffig durch Backpulver und einen kaum gerührten Teig.",
    "Kleine Kuchen, die in der Pfanne aufgehen.",
    [("Trockene und nasse Zutaten getrennt vorbereiten", "So muss man am Ende nur noch kurz mischen.", "glutenbildung"),
     ("Nur kurz zusammenrühren, Klümpchen bleiben", "Wenig Gluten, zarter Pancake.", "pfannkuchen-gummig"),
     ("Teig ein paar Minuten stehen lassen", "Das Backpulver beginnt zu arbeiten, das Mehl quillt.", "chemische-lockerung"),
     ("Bei mittlerer Hitze backen, wenden wenn Blasen platzen", "Die Hitze treibt das Gas aus, die Unterseite bräunt.", "maillard-reaktion")],
    ["chemische-lockerung", "fluffig", "pfannkuchen-gummig"], ["w-gebaeck"])

gericht("g-meringue", "Meringue", ["Baiser", "Meringues", "Schaumgebäck"],
    "Meringue ist getrockneter Eischnee: Zucker stabilisiert den Schaum, niedrige Hitze trocknet ihn, ohne ihn zu bräunen.",
    "Wie gefrorene Wolken aus Zucker und Luft.",
    [("Eiweiß in fettfreier Schüssel aufschlagen", "Fett verhindert stabilen Schaum.", "schaumbildung"),
     ("Zucker nach und nach einrieseln lassen", "Gelöster Zucker macht die Blasenwände stabil und glänzend.", "schaumbildung"),
     ("Bei etwa 100 °C lange trocknen (Richtwert)", "Das Wasser verdampft langsam, der Schaum wird fest, ohne zu bräunen.", "verdampfen"),
     ("Im Ofen auskühlen lassen", "Schneller Temperaturwechsel lässt sie reißen oder kleben.", "zeit")],
    ["schaumbildung", "aufschlagen", "eischnee-nicht-steif"], ["w-eier", "w-suesses"], "fortgeschritten")

gericht("g-ofengemuese", "Ofengemüse", ["geröstetes Gemüse", "Blechgemüse"],
    "Ofengemüse wird süß und gebräunt statt gedämpft, wenn es trocken, mit Abstand und heiß in den Ofen kommt.",
    "Wäsche aufhängen statt auf einem Haufen trocknen.",
    [("Gleich große Stücke schneiden", "Alles wird gleichzeitig gar.", "oberflaeche"),
     ("Trocknen und dünn mit Öl mischen", "Öl leitet Hitze in jede Ecke, Wasser würde bremsen.", "oel"),
     ("Mit Abstand auf das vorgeheizte Blech", "Dampf kann entweichen, die Unterseite bräunt sofort.", "roesten-ofen"),
     ("Bei 220 °C rösten, einmal wenden", "Maillard und Karamellisierung machen das Gemüse süß und aromatisch.", "maillard-reaktion")],
    ["roesten-ofen", "maillard-reaktion", "knusprig"], ["w-gemuese"])

gericht("g-konfituere", "Konfitüre", ["Marmelade", "Erdbeerkonfitüre", "Aprikosenkonfitüre"],
    "Konfitüre geliert, wenn Pektin, Zucker und Säure zusammenkommen und genug Wasser verkocht ist.",
    "Drei Schlüssel für ein Schloss.",
    [("Früchte mit Zucker mischen und ziehen lassen", "Der Zucker zieht Saft aus den Früchten.", "osmose"),
     ("Zitronensaft zugeben", "Säure hilft dem Pektin zu gelieren und hält die Farbe frisch.", "gelbildung-pektin"),
     ("Sprudelnd kochen, bis die Gelierprobe gelingt", "Wasser verdampft, Zucker und Pektin werden konzentriert.", "reduktion"),
     ("Heiß abfüllen", "Heiß gefüllt und verschlossen hält sie länger.", "gelbildung-pektin")],
    ["gelbildung-pektin", "pektin", "zucker"], ["w-suesses"])

# ======================= EXPERIMENTE =======================
experiment("x-rotkohl-indikator", "Rotkohl als Farbzauber", ["Rotkohl Experiment", "Säuretest", "pH Experiment Kinder"],
    "Rotkohlsaft zeigt mit seiner Farbe, ob etwas sauer oder basisch ist.",
    ["ein paar Blätter Rotkohl", "heißes Wasser", "drei Gläser", "Essig oder Zitronensaft", "Natron"],
    ["Rotkohl klein schneiden, mit heißem Wasser übergießen, 10 Minuten ziehen lassen.", "Den violetten Saft auf drei Gläser verteilen.",
     "In ein Glas Essig geben, in eines eine Messerspitze Natron, das dritte bleibt so.", "Farben vergleichen."],
    "Mit Essig wird der Saft pink bis rot, mit Natron blau bis grün, ohne Zusatz bleibt er violett.",
    "Die Farbstoffe im Rotkohl (Anthocyane) ändern ihre Form mit dem pH-Wert. Darum gehört Apfel oder Essig in Rotkohl, wenn er rot bleiben soll.",
    ["anthocyan-farbe", "ph-wert", "saeure", "natron"], ["w-gemuese"], "15 Minuten", "Heißes Wasser: Erwachsene übergießen.")
experiment("x-backpulver-kalt-heiss", "Backpulver: kalt gegen heiß", ["Backpulver Experiment", "Triebmittel testen"],
    "Backpulver sprudelt zweimal: einmal, wenn es nass wird, und noch einmal in der Hitze.",
    ["Backpulver", "zwei Gläser", "kaltes Wasser", "heißes Wasser"],
    ["In beide Gläser je einen Teelöffel Backpulver geben.", "Ins erste kaltes Wasser gießen, ins zweite heißes.", "Beobachten, wo es stärker sprudelt."],
    "Im kalten Glas sprudelt es leicht, im heißen deutlich stärker.",
    "Backpulver enthält zwei Säuren: Eine reagiert schon mit Wasser, die andere erst bei Hitze. So geht der Kuchen genau im Ofen richtig auf.",
    ["chemische-lockerung", "backpulver"], ["w-gebaeck"], "5 Minuten", "Heißes Wasser: Erwachsene gießen.")
experiment("x-eischnee-fett", "Eischnee mit und ohne Fett", ["Eischnee Experiment", "warum wird Eischnee nicht steif"],
    "Ein winziger Tropfen Eigelb verhindert, dass Eiweiß steif wird.",
    ["2 Eiweiß", "ein Tropfen Eigelb oder Öl", "zwei saubere Schüsseln", "Schneebesen oder Handmixer"],
    ["Je ein Eiweiß in eine Schüssel geben.", "In eine Schüssel einen winzigen Tropfen Eigelb oder Öl geben.", "Beide gleich lange schlagen.", "Vergleichen."],
    "Ohne Fett entsteht steifer, glänzender Schnee. Mit dem Tropfen Fett bleibt es flüssig oder schaumig weich.",
    "Die Eiweiße bilden eine Haut um die Luftblasen. Fett schiebt sich dazwischen, und die Blasen platzen.",
    ["schaumbildung", "eischnee-nicht-steif", "aufschlagen"], ["w-eier"], "10 Minuten")
experiment("x-tanzender-tropfen", "Der tanzende Wassertropfen", ["Leidenfrost Experiment", "Wassertropfen Pfanne"],
    "Auf einer sehr heißen Pfanne schwebt ein Wassertropfen und tanzt, statt zu verdampfen.",
    ["Edelstahl- oder Eisenpfanne", "ein paar Tropfen Wasser"],
    ["Pfanne leer bei mittlerer Hitze erwärmen und ab und zu ein paar Tropfen Wasser hineinspritzen.", "Beobachten, wie sich die Tropfen verhalten, während die Pfanne heißer wird."],
    "Erst zischen die Tropfen und verdampfen schnell. Ab einer bestimmten Hitze bilden sie Kügelchen, die umhergleiten und länger halten.",
    "Unter dem Tropfen bildet sich eine Dampfschicht, auf der er schwebt (Leidenfrost-Effekt). Genau dann ist die Pfanne heiß genug zum Anbraten.",
    ["leidenfrost", "pfanne-vorheizen"], ["w-fleisch"], "5 Minuten", "Heiße Pfanne: nur mit Erwachsenen, keine beschichtete Pfanne leer überhitzen.")
experiment("x-kartoffelwasser", "Trübes Kartoffelwasser", ["Kartoffelstärke sichtbar machen", "Stärke Experiment"],
    "Geschnittene Kartoffeln geben Stärke ins Wasser ab, und man kann sie sogar sehen.",
    ["eine Kartoffel", "Schüssel mit kaltem Wasser", "ein Glas"],
    ["Kartoffel in Stifte schneiden und ins Wasser legen.", "Nach 30 Minuten die Stifte herausnehmen.", "Das Wasser in ein Glas gießen und eine Stunde stehen lassen."],
    "Das Wasser ist trüb, und am Boden des Glases setzt sich eine weiße Schicht ab.",
    "Das ist Stärke, die beim Schneiden aus den Zellen gefallen ist. Abgespült klebt sie nicht mehr an der Oberfläche, darum werden gewässerte Pommes knuspriger.",
    ["kaltwasserbad", "staerke", "staerkeverkleisterung"], ["w-kartoffeln"], "1½ Stunden")
experiment("x-apfel-braun", "Warum wird der Apfel braun?", ["Apfel braun Experiment", "Zitrone Apfel"],
    "Apfelschnitze werden an der Luft braun, außer man schützt sie.",
    ["ein Apfel", "Zitronensaft", "ein Glas Wasser", "drei Teller"],
    ["Apfel in Schnitze schneiden.", "Einen Schnitz mit Zitronensaft beträufeln, einen ins Wasser legen, einen so liegen lassen.", "Nach 30 Minuten vergleichen."],
    "Der unbehandelte Schnitz ist braun, die anderen beiden bleiben hell.",
    "Ein Enzym im Apfel reagiert mit dem Sauerstoff der Luft und bildet braune Farbstoffe. Säure bremst das Enzym, Wasser hält die Luft fern.",
    ["enzym-braeunung", "saeure"], ["w-gemuese"], "30 Minuten")
experiment("x-butter-schuetteln", "Butter selber schütteln", ["Butter machen Kinder", "Sahne schütteln"],
    "Aus Sahne wird Butter, wenn man lange genug schüttelt.",
    ["200 ml kalte Vollrahm", "ein Schraubglas", "eine Prise Salz"],
    ["Sahne ins Glas füllen und gut verschließen.", "Kräftig schütteln, etwa 10–15 Minuten. Abwechseln!", "Wenn sich ein Klumpen und Flüssigkeit trennen, die Flüssigkeit abgießen.", "Butter mit kaltem Wasser spülen und salzen."],
    "Erst wird die Sahne schaumig, dann fest, dann trennt sie sich plötzlich in einen gelben Klumpen und weiße Buttermilch.",
    "Schütteln reißt die Hüllen der Fetttröpfchen auf, sie verkleben zu immer größeren Klumpen. Genau das passiert, wenn Schlagrahm zu lange geschlagen wird.",
    ["sahne-wird-butter", "schaumbildung", "sahne"], ["w-milch"], "20 Minuten")
experiment("x-gluten-auswaschen", "Gluten sichtbar machen", ["Gluten auswaschen", "Kleber Experiment"],
    "Wäscht man einen Teigball unter Wasser aus, bleibt das Glutennetz übrig: ein zäher, gummiartiger Klumpen.",
    ["100 g Weißmehl", "60 ml Wasser", "eine Schüssel Wasser"],
    ["Mehl und Wasser zu einem Teig kneten, 20 Minuten ruhen lassen.", "Den Teigball in der Schüssel Wasser kneten und drücken.", "Das trübe Wasser wechseln, bis es fast klar bleibt."],
    "Das Wasser wird milchig weiß. Übrig bleibt ein kleiner, sehr dehnbarer, gummiartiger Klumpen.",
    "Das Milchige ist ausgewaschene Stärke, der Klumpen ist reines Gluten. Ziehe ihn auseinander: So hält er im Brot die Gasblasen fest.",
    ["glutenbildung", "mehl", "staerke"], ["w-brot"], "40 Minuten")
experiment("x-hefe-ballon", "Hefe bläst einen Ballon auf", ["Hefe Experiment Kinder", "Hefe Ballon Flasche"],
    "Hefe produziert so viel Gas, dass sie einen Luftballon aufblasen kann.",
    ["ein Päckchen Trockenhefe", "2 TL Zucker", "lauwarmes Wasser", "eine kleine Flasche", "ein Luftballon"],
    ["Hefe und Zucker in die Flasche geben, etwa ein Drittel lauwarmes Wasser dazu.", "Schwenken, dann den Ballon über den Flaschenhals ziehen.", "An einen warmen Ort stellen und warten."],
    "Nach 20–40 Minuten schäumt es in der Flasche, und der Ballon richtet sich auf und bläht sich.",
    "Die Hefe frisst den Zucker und gibt Kohlendioxid ab. Dasselbe Gas bläst im Brotteig die Poren auf. Mit kaltem Wasser dauert es deutlich länger.",
    ["hefegaerung", "hefe"], ["w-brot"], "45 Minuten")
experiment("x-salz-gurke", "Salz zieht Wasser", ["Osmose Experiment", "Gurke salzen Experiment"],
    "Salz zieht Wasser aus Gemüse, und man kann zusehen.",
    ["eine Gurke oder Zucchini", "Salz", "zwei Teller"],
    ["Gemüse in gleich dicke Scheiben schneiden, auf zwei Teller verteilen.", "Einen Teller salzen, den anderen nicht.", "15 Minuten warten."],
    "Auf den gesalzenen Scheiben stehen Wassertropfen, auf dem Teller sammelt sich Flüssigkeit, und die Scheiben werden biegsam.",
    "Wasser wandert dorthin, wo mehr Salz ist (Osmose). Darum ist frisch gesalzenes Fleisch nass und sollte man es entweder sofort oder viel später braten.",
    ["osmose", "salz", "auberginen-salzen"], ["w-gemuese"], "15 Minuten")
experiment("x-zuckerkristalle", "Zuckerkristalle züchten", ["Kandiszucker selber machen", "Kristalle Experiment"],
    "Aus einer heißen Zuckerlösung wachsen über Tage Zuckerkristalle an einem Faden.",
    ["250 g Zucker", "100 ml Wasser", "ein sauberes Glas", "ein Holzspieß oder Baumwollfaden"],
    ["Wasser aufkochen und den Zucker darin vollständig auflösen.", "Etwas abkühlen lassen und ins Glas gießen.", "Den Spieß oder Faden eintauchen, ohne den Boden zu berühren.", "Einige Tage ruhig stehen lassen."],
    "Am Spieß wachsen glitzernde Kristalle, jeden Tag ein Stück größer.",
    "Heißes Wasser kann viel mehr Zucker lösen als kaltes. Beim Abkühlen will der Zucker wieder fest werden und lagert sich an den Spieß an. Genau das macht Karamell körnig.",
    ["zucker-kristallisation", "zucker"], ["w-suesses"], "einige Tage", "Heißer Zuckersirup: nur Erwachsene kochen und gießen.")
experiment("x-bohnen-gruen", "Grüne Bohnen: grün oder grau?", ["Chlorophyll Experiment", "Gemüse Farbe Experiment"],
    "Dieselben Bohnen werden leuchtend grün oder olivgrau, je nach Kochzeit und Säure.",
    ["eine Handvoll grüne Bohnen", "zwei Töpfe Wasser", "Zitronensaft", "eine Schüssel Eiswasser"],
    ["Beide Töpfe zum Kochen bringen, in einen einen Schuss Zitronensaft.", "Bohnen auf beide Töpfe verteilen.", "Nach 2 Minuten je einige Bohnen ins Eiswasser legen, die übrigen 10 Minuten weiterkochen.", "Alle vergleichen."],
    "Nach 2 Minuten leuchten die Bohnen. Nach 10 Minuten sind sie trüber, im sauren Topf deutlich olivgrün.",
    "Kurzes Kochen treibt Luft aus dem Gewebe, das Grün leuchtet. Längeres Kochen und Säure verwandeln das Chlorophyll in einen olivbraunen Farbstoff.",
    ["chlorophyll-farbe", "blanchieren", "gemuese-grau"], ["w-gemuese"], "20 Minuten", "Kochendes Wasser: nur mit Erwachsenen.")

os.makedirs(OUT, exist_ok=True)
for e in E:
    json.dump(e, open(os.path.join(OUT, e["id"] + ".json"), "w"), ensure_ascii=False, indent=2)

# Masterliste ergänzen
mp = os.path.join(ROOT, "content/master-list.json"); M = json.load(open(mp))
have = {m["id"] for m in M["eintraege"]}
for e in E:
    if e["id"] in have: continue
    M["eintraege"].append({"id": e["id"], "typ": e["typ"], "titel": e["titel"], "status": "geplant", "pilot": False,
        "links": e["links"], "welten": e["welten"], "synonyme": e["synonyme"], "verlinkt_von": [], "visual": {"vorlage": e["visual"]["vorlage"]}})
ids = {m["id"] for m in M["eintraege"]}; back = {i: set() for i in ids}
for m in M["eintraege"]:
    for l in m["links"]:
        if l in back: back[l].add(m["id"])
for m in M["eintraege"]: m["verlinkt_von"] = sorted(back[m["id"]] - set(m["links"]))
M["anzahl"] = len(M["eintraege"]); M["stand"] = "2026-11-01"
json.dump(M, open(mp, "w"), ensure_ascii=False, indent=1)
print(len(E), "Einträge,", M["anzahl"], "in der Masterliste")
