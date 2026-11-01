"""Batch 7: Desserts, Milch & Schokolade. Schreibt nach content/entries/ im Repo."""
import json, sys, os
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/kochwissen-app/content/entries"

QM = {"titel": "Harold McGee: On Food and Cooking (2004)", "stelle": "Kapitel Milch, Zucker, Schokolade"}
QT = {"titel": "Thermapen: The ultimate guide to tempering chocolate", "url": "https://thermapen.co.uk/blogs/inspiration/tempering-chocolate-guide"}
QG = {"titel": "Johnson & Wales University: Baking Science – Thickening and Gelling", "url": "https://jwu.pressbooks.pub/bakingsciencethickeningandgelling/?p=62"}
QS = {"titel": "America’s Test Kitchen: How to fix seized chocolate", "url": "https://www.americastestkitchen.com/how_tos/5712-how-to-fix-seized-chocolate"}

E = []
def add(**k):
    k.setdefault("status", "entwurf"); k.setdefault("schwierigkeit", "einsteiger"); E.append(k)
def sym(welt, **k): add(typ="symptom", welten=[welt], visual={"vorlage": "entscheidungsbaum"}, **k)

add(id="w-suesses", typ="welt", titel="Desserts & Süßes", synonyme=["Dessert", "Nachtisch", "Pudding", "Mousse", "Konfitüre", "Schokolade"],
    kurz="Süßspeisen leben von Kristallen, Gelen und Schäumen: Zucker, der kristallisiert oder karamellisiert, Gelatine und Pektin, die gelieren, Eier und Sahne, die eindicken oder Luft halten.",
    bild_im_kopf="Wie eine Werkstatt für Strukturen: fest, cremig, luftig oder knackig, und jede braucht ihr eigenes Werkzeug.",
    was_passiert="Zucker kann glasig, körnig oder karamellisiert sein, je nachdem wie er erhitzt und abgekühlt wird. Gelatine und Pektin bilden Netze, die Flüssigkeit festhalten. Schokolade bekommt Glanz und Knack nur mit den richtigen Fettkristallen.",
    warum_wichtig="Desserts verzeihen wenig, weil wenige Grad entscheiden. Wer die Strukturen versteht, kann retten statt neu anfangen.",
    faustregeln=["Thermometer für Zucker und Schokolade.", "Eiercremes nie kochen lassen.", "Gelatine nie kochen, nur auflösen."],
    links=["karamellisierung", "zucker-kristallisation", "gelbildung-gelatine", "fett-kristallisation", "schaumbildung", "eiweiss-gerinnung"],
    visual={"vorlage": "keine", "illustration": "a glass coupe with chocolate mousse and a spoon"},
    quellen=[QM])

add(id="w-milch", typ="welt", titel="Milch & Käse", synonyme=["Milchprodukte", "Rahm", "Sahne", "Joghurt", "Käse", "Butter"],
    kurz="Milch ist Wasser mit Fetttröpfchen, Eiweiß und Milchzucker. Je nachdem, was man mit diesen Teilen macht, entstehen Sahne, Butter, Joghurt oder Käse.",
    bild_im_kopf="Wie ein Baukasten mit drei Teilen: Fett, Eiweiß, Zucker. Jedes Milchprodukt nutzt einen anderen Teil.",
    was_passiert="Sahne ist das abgetrennte Fett und lässt sich schlagen. Bakterien säuern Milchzucker zu Milchsäure, die das Eiweiß eindickt: Joghurt. Lab oder Säure bringen das Eiweiß zum Gerinnen: Käse.",
    warum_wichtig="Erklärt, warum Sahne zu Butter wird, warum Milch anbrennt und warum manche Käse schmelzen und andere nicht.",
    faustregeln=["Milch nicht stark kochen lassen, sie brennt an und kocht über.", "Sahne zum Schlagen gut gekühlt.", "Käse zum Schmelzen fein reiben und nicht zu heiß werden lassen."],
    links=["schaumbildung", "milchsaeuregaerung", "eiweiss-gerinnung", "emulsion"],
    visual={"vorlage": "keine", "illustration": "a glass milk bottle beside a wedge of alpine cheese"},
    quellen=[QM])

add(id="zucker-kristallisation", typ="prozess", titel="Zucker kristallisiert", schwierigkeit="fortgeschritten",
    synonyme=["Zucker wird körnig", "auskristallisieren", "Fondant", "Fudge"],
    kurz="Gelöster Zucker will wieder Kristalle bilden. Schon ein einziges Körnchen kann eine Kettenreaktion auslösen.",
    bild_im_kopf="Wie Dominosteine: Fällt einer, fallen alle. Ein Zuckerkristall am Topfrand reicht als erster Stein.",
    was_passiert="In heißem Sirup ist viel mehr Zucker gelöst, als er im Kalten halten kann. Beim Abkühlen oder durch Rühren lagern sich die Zuckermoleküle an jedes vorhandene Kristall an, und der Sirup wird körnig. Säure, Honig oder Glukosesirup stören die Kristallbildung und halten Karamell glatt.",
    warum_wichtig="Erklärt, warum Karamell plötzlich sandig wird, und warum man bei Fudge gerade das Kristallisieren gezielt steuert.",
    faustregeln=["Nicht rühren, solange Zucker kocht. Schwenken statt rühren.", "Kristalle am Topfrand mit einem nassen Pinsel herunterwaschen.", "Ein Löffel Glukosesirup oder etwas Zitronensaft verhindert Körnigkeit."],
    stellschrauben=[{"id": "mechanik", "wirkung": "rühren → Kristalle"}, {"id": "temperatur", "wirkung": "Abkühlen → Kristallisation"}],
    links=["karamell-kristallisiert", "zucker-karamellisieren", "karamellisierung", "zucker"],
    welten=["w-suesses"],
    visual={"vorlage": "zoom3-simulation"},
    quellen=[QM])

add(id="fett-kristallisation", typ="prozess", titel="Fett kristallisiert (Temperieren)", schwierigkeit="profi",
    synonyme=["Kakaobutter", "Schokolade temperieren", "Kristallform", "Glanz und Knack"],
    kurz="Kakaobutter kann in mehreren Kristallformen fest werden. Nur eine davon gibt Schokolade Glanz und Knack.",
    bild_im_kopf="Wie Soldaten, die in Reih und Glied stehen (glänzend, knackt) oder wild durcheinander (matt, bröselig).",
    was_passiert="Beim Abkühlen bilden sich verschiedene Fettkristalle. Die gewünschte Form (Form V) entsteht nur in einem engen Temperaturfenster. Beim Temperieren schmilzt man alle Kristalle, kühlt ab, damit sich stabile Kristalle bilden, und erwärmt leicht, um instabile wieder zu schmelzen.",
    warum_wichtig="Erklärt, warum geschmolzene und wieder fest gewordene Schokolade matt und streifig wird und warum Pralinés ohne Temperieren nicht glänzen.",
    faustregeln=["Dunkle Schokolade: auf etwa 45 °C schmelzen, auf 29 °C abkühlen, bei etwa 31,5 °C verarbeiten.",
                 "Milch- und weiße Schokolade liegen jeweils etwa 1 °C tiefer.", "Kein Wasser in die Nähe."],
    stellschrauben=[{"id": "temperatur", "wirkung": "ein Grad zu viel → Kristalle schmelzen"}],
    links=["temperieren", "schokolade", "schokolade-grau"],
    welten=["w-suesses"],
    visual={"vorlage": "temperaturskala", "params": {"skala": [{"c": 29, "name": "abkühlen: stabile Kristalle bilden sich"}, {"c": 31, "name": "verarbeiten (dunkel ca. 31,5 °C)"}, {"c": 34, "name": "darüber schmelzen die guten Kristalle"}, {"c": 45, "name": "schmelzen: alle Kristalle weg"}]}},
    quellen=[QT, QM])

add(id="gelbildung-gelatine", typ="prozess", titel="Gelieren mit Gelatine", synonyme=["Gelatine", "Gelee", "Panna cotta", "fest werden"],
    kurz="Gelatine löst sich in warmer Flüssigkeit und bildet beim Abkühlen ein Netz, das die Flüssigkeit festhält. Im Mund schmilzt es wieder.",
    bild_im_kopf="Wie ein Fischernetz, das sich im Kalten zusammenzieht und das Wasser in seinen Maschen hält.",
    was_passiert="Gelatine besteht aus langen Eiweißketten. Warm schwimmen sie frei, beim Abkühlen verbinden sie sich zu einem Netz. Weil es bei Körpertemperatur wieder schmilzt, zergeht Panna cotta auf der Zunge. Kochen schwächt die Gelatine, und Enzyme in roher Ananas oder Kiwi zerschneiden das Netz.",
    warum_wichtig="Erklärt, warum Gelatine nie kochen darf, warum Desserts Zeit im Kühlschrank brauchen und warum Ananasgelee nicht fest wird.",
    faustregeln=["Blattgelatine in kaltem Wasser einweichen, ausdrücken, in warmer (nicht kochender) Flüssigkeit auflösen.",
                 "Mehrere Stunden kühlen.", "Rohe Ananas, Kiwi, Papaya vorher erhitzen oder aus der Dose verwenden."],
    stellschrauben=[{"id": "temperatur", "wirkung": "warm → löst, kalt → geliert"}, {"id": "zeit", "wirkung": "länger kühl → fester"}],
    links=["gelatine", "kollagen-gelatine", "gelbildung-pektin"],
    welten=["w-suesses"],
    visual={"vorlage": "temperaturskala", "params": {"hinweis": "Richtwerte", "skala": [{"c": 10, "name": "Kühlschrank: Netz wird fest"}, {"c": 30, "name": "beginnt zu gelieren / schmilzt im Mund"}, {"c": 43, "name": "vollständig gelöst"}, {"c": 100, "name": "kochen schwächt die Gelatine"}]}},
    quellen=[QG, QM])

add(id="gelbildung-pektin", typ="prozess", titel="Gelieren mit Pektin", synonyme=["Konfitüre", "Marmelade", "Gelierzucker", "Pektin"],
    kurz="Pektin aus Früchten bildet ein Gel, aber nur mit genug Zucker und Säure. Darum braucht Konfitüre beides.",
    bild_im_kopf="Wie ein Schloss mit drei Schlüsseln: Pektin, Zucker und Säure. Fehlt einer, bleibt es flüssig.",
    was_passiert="Pektin sind lange Ketten aus Fruchtzellwänden. Zucker entzieht ihnen das Wasser, Säure nimmt ihnen die Ladung, die sie abstößt. Dann können sie sich zu einem Netz verbinden. Äpfel, Quitten und Johannisbeeren haben viel Pektin, Erdbeeren wenig.",
    warum_wichtig="Erklärt, warum Konfitüre mit wenig Zucker nicht fest wird und warum Zitronensaft hinein gehört.",
    faustregeln=["Gelierprobe: Ein Klecks auf einem kalten Teller soll nach einer Minute eine Haut bilden.", "Pektinarme Früchte mit Äpfeln oder Gelierzucker kombinieren.", "Zitronensaft hilft bei milden Früchten."],
    stellschrauben=[{"id": "zuckergehalt", "wirkung": "zu wenig → bleibt flüssig"}, {"id": "ph-wert", "wirkung": "sauer → geliert besser"}],
    links=["pektin", "pektin-abbau", "zucker", "saeure"],
    welten=["w-suesses"],
    visual={"vorlage": "zoom3-simulation"},
    quellen=[QM])

add(id="temperieren", typ="technik", titel="Schokolade temperieren", schwierigkeit="profi", synonyme=["temperieren", "Kuvertüre temperieren", "Impfmethode"],
    kurz="Schokolade so schmelzen und abkühlen, dass sie mit Glanz und Knack fest wird.",
    bild_im_kopf="Wie einer Gruppe das Aufstellen beibringen: erst alle auflösen, dann die richtigen Vorbilder hinzufügen.",
    was_passiert="Die einfachste Methode ist das Impfen: Zwei Drittel schmelzen, ein Drittel fein gehackte, temperierte Schokolade einrühren. Die festen Stücke bringen die richtigen Kristalle mit, an denen sich die geschmolzene Schokolade ausrichtet.",
    schritte=["Zwei Drittel der Schokolade im Wasserbad auf etwa 45 °C schmelzen.", "Ein Drittel fein gehackt einrühren, bis es geschmolzen ist.",
              "Auf Arbeitstemperatur bringen (dunkel ca. 31,5 °C, Milch ca. 30,5 °C, weiß ca. 30 °C).", "Test: Ein Messer eintauchen, nach wenigen Minuten soll die Schokolade glänzend und fest sein.",
              "Bei Arbeitstemperatur halten und zügig verarbeiten."],
    wirkt_auf=["farbe"],
    links=["fett-kristallisation", "schokolade", "wasserbad", "schokolade-grau"],
    welten=["w-suesses"],
    visual={"vorlage": "ablauf"},
    quellen=[QT])

sym("w-suesses", id="creme-klumpig", titel="Creme oder Pudding klumpt", synonyme=["Vanillecreme geronnen", "Pudding Klümpchen", "Crème brûlée grieselig"],
    kurz="Entweder ist das Ei geronnen oder die Stärke hat Klümpchen gebildet.",
    bild_im_kopf="Wie Rührei in der Vanillesauce.",
    ursachen=[{"titel": "Zu heiß, Ei geronnen", "haeufigkeit": 3, "prinzip": "eiweiss-gerinnung", "warum": "Über etwa 80 °C gerinnt das Eigelb zu Krümeln.", "fix": ["Sofort durch ein Sieb in eine kalte Schüssel gießen und mit dem Mixstab glätten", "Nächstes Mal im Wasserbad und ständig rühren"]},
              {"titel": "Stärke nicht verteilt", "haeufigkeit": 2, "prinzip": "staerkeverkleisterung", "warum": "Stärke direkt in heiße Milch bildet Klumpen.", "fix": ["Stärke in etwas kalter Milch anrühren", "Mit dem Schneebesen einrühren"]},
              {"titel": "Nicht gerührt", "haeufigkeit": 1, "prinzip": "eiweiss-gerinnung", "warum": "Am Topfboden wird es heißer und gerinnt zuerst.", "fix": ["Ständig rühren, auch über den Boden"]}],
    diagnose={"q1": {"frage": "Ist Stärke oder Puddingpulver im Rezept?", "antworten": [["Ja", "q2"], ["Nein, nur Eier", "u0"]]},
              "q2": {"frage": "Sind es weiche Körnchen oder trockene Mehlklümpchen?", "antworten": [["Weiche Körnchen", "u2"], ["Trockene Klümpchen", "u1"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["eiweiss-gerinnung", "staerkeverkleisterung", "wasserbad"], quellen=[QM])

sym("w-suesses", id="karamell-kristallisiert", titel="Karamell wird körnig", synonyme=["Karamell sandig", "Zucker kristallisiert", "Karamell bröselig"],
    kurz="Ein Zuckerkristall hat eine Kettenreaktion ausgelöst. Der Sirup wird zu Sand.",
    bild_im_kopf="Wie ein umgestoßener Dominostein.",
    ursachen=[{"titel": "Gerührt", "haeufigkeit": 3, "prinzip": "zucker-kristallisation", "warum": "Rühren bringt Kristalle in Bewegung und schafft Ansatzpunkte.", "fix": ["Nur schwenken", "Mit etwas Wasser neu auflösen und vorsichtiger kochen"]},
              {"titel": "Kristalle am Topfrand", "haeufigkeit": 2, "prinzip": "zucker-kristallisation", "warum": "Ein ungelöstes Körnchen fällt zurück und startet die Kristallisation.", "fix": ["Rand mit nassem Pinsel abwaschen", "Deckel kurz auflegen, damit Dampf die Kristalle löst"]},
              {"titel": "Kein Störstoff", "haeufigkeit": 1, "prinzip": "zucker-kristallisation", "warum": "Reiner Zucker kristallisiert leichter.", "fix": ["Ein Löffel Glukosesirup oder ein paar Tropfen Zitronensaft"]}],
    diagnose={"q1": {"frage": "Hast du gerührt, während der Zucker kochte?", "antworten": [["Ja", "u0"], ["Nein", "q2"]]},
              "q2": {"frage": "Waren Zuckerkristalle am Topfrand?", "antworten": [["Ja", "u1"], ["Nein", "u2"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["zucker-kristallisation", "zucker-karamellisieren"], quellen=[QM])

sym("w-milch", id="sahne-wird-butter", titel="Sahne wird zu Butter", synonyme=["Rahm wird Butter", "Sahne flockig", "Schlagrahm körnig"],
    kurz="Zu lange geschlagen: Die Fetttröpfchen sind zusammengeklebt und haben sich von der Flüssigkeit getrennt.",
    bild_im_kopf="Wie ein Schneeball, der zu lange gerollt wurde und zu einem Klumpen geworden ist.",
    ursachen=[{"titel": "Zu lange geschlagen", "haeufigkeit": 3, "prinzip": "schaumbildung", "warum": "Die Fetthüllen reißen, die Tröpfchen verkleben zu Butterkörnern.", "fix": ["Ein paar Löffel flüssige Sahne vorsichtig unterheben", "Ganz zu Butter schlagen und weiterverwenden"]},
              {"titel": "Sahne zu warm", "haeufigkeit": 2, "prinzip": "schaumbildung", "warum": "Warmes Fett ist weich und klebt schneller zusammen.", "fix": ["Sahne, Schüssel und Schneebesen kühlen"]}],
    diagnose={"q1": {"frage": "War die Sahne direkt aus dem Kühlschrank?", "antworten": [["Nein", "u1"], ["Ja", "u0"]]}, "u0": {"ursache": 0}, "u1": {"ursache": 1}},
    links=["schaumbildung", "sahne", "aufschlagen"], quellen=[QM])

sym("w-suesses", id="schokolade-grau", titel="Schokolade wird grau und streifig", synonyme=["Fettreif", "Zuckerreif", "Schokolade weiß angelaufen", "Bloom"],
    kurz="Die Fettkristalle haben sich falsch angeordnet (Fettreif) oder Feuchtigkeit hat Zucker an die Oberfläche geholt (Zuckerreif).",
    bild_im_kopf="Wie Raureif auf einer Scheibe: Etwas wandert an die Oberfläche und kristallisiert dort.",
    ursachen=[{"titel": "Nicht temperiert", "haeufigkeit": 3, "prinzip": "fett-kristallisation", "warum": "Geschmolzene Schokolade wird ohne Temperieren in instabilen Kristallen fest.", "fix": ["Temperieren", "Für Saucen und Kuchen ist es egal"]},
              {"titel": "Zu warm gelagert", "haeufigkeit": 2, "prinzip": "fett-kristallisation", "warum": "Wärme schmilzt Kakaobutter, die an der Oberfläche neu kristallisiert.", "fix": ["Kühl und trocken lagern, nicht im Kühlschrank"]},
              {"titel": "Feuchtigkeit", "haeufigkeit": 1, "prinzip": "zucker-kristallisation", "warum": "Kondenswasser löst Zucker, der beim Trocknen weiß auskristallisiert.", "fix": ["Nicht direkt aus dem Kühlschrank in die warme Küche", "Gut verpacken"]}],
    diagnose={"q1": {"frage": "Hast du die Schokolade selbst geschmolzen und fest werden lassen?", "antworten": [["Ja", "u0"], ["Nein, gekaufte Tafel", "q2"]]},
              "q2": {"frage": "Fühlt sich der Belag fettig oder eher rau und trocken an?", "antworten": [["Fettig", "u1"], ["Rau", "u2"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["fett-kristallisation", "temperieren", "schokolade"], quellen=[QT, QM])

sym("w-suesses", id="schokolade-klumpt", titel="Schokolade klumpt beim Schmelzen", synonyme=["Schokolade wird fest", "Schokolade grieselig", "seized chocolate"],
    kurz="Ein paar Tropfen Wasser haben den Zucker in Sirup verwandelt, der die Kakaoteilchen zusammenklebt.",
    bild_im_kopf="Wie Sand, auf den ein paar Regentropfen fallen: Plötzlich klumpt alles.",
    ursachen=[{"titel": "Wenig Wasser oder Dampf", "haeufigkeit": 3, "prinzip": "zucker-kristallisation", "warum": "Schon ein Tropfen macht den Zucker klebrig, die Kakaoteilchen verklumpen.", "fix": ["Löffelweise kochendes Wasser einrühren, bis sie glatt ist", "Dann für Sauce oder heiße Schokolade verwenden"]},
              {"titel": "Zu heiß", "haeufigkeit": 2, "prinzip": "pyrolyse", "warum": "Überhitzte Schokolade wird dick und bröselig.", "fix": ["Im Wasserbad sanft schmelzen", "Mikrowelle nur in kurzen Stößen"]}],
    diagnose={"q1": {"frage": "Kann Wasser oder Dampf an die Schokolade gekommen sein?", "antworten": [["Ja", "u0"], ["Nein", "u1"]]}, "u0": {"ursache": 0}, "u1": {"ursache": 1}},
    links=["schokolade", "wasserbad", "temperieren"], quellen=[QS])

# ---------------- ZUTATEN
def zut(**k): add(typ="zutat", visual={"vorlage": "punktmatrix"}, **k)
zut(id="gelatine", titel="Gelatine", synonyme=["Blattgelatine", "Gelatinepulver"],
    kurz="Gelatine ist gereinigtes Kollagen. Sie löst sich in Wärme und lässt Flüssigkeiten beim Abkühlen gelieren.",
    bild_im_kopf="Wie ein Netz in Pulverform.",
    rolle=[{"rolle": "lässt Flüssigkeit fest werden", "prozess": "gelbildung-gelatine"}, {"rolle": "macht Saucen sämig", "prozess": "kollagen-gelatine"}],
    was_passiert="Gelatine stammt aus Bindegewebe. Eingeweicht und gelöst bildet sie beim Abkühlen ein Netz, das bei Körpertemperatur wieder schmilzt.",
    faustregeln=["Nie kochen.", "Agar-Agar ist eine pflanzliche Alternative, muss aber kochen und wird fester."],
    links=["gelbildung-gelatine", "kollagen-gelatine"], welten=["w-suesses"], quellen=[QG])
zut(id="pektin", titel="Pektin", synonyme=["Gelierzucker", "Apfelpektin"],
    kurz="Pektin ist der Kitt in Pflanzenzellen. Mit Zucker und Säure bildet es Gele, beim Kochen von Gemüse löst es sich.",
    bild_im_kopf="Derselbe Mörtel, der Gemüse zusammenhält, macht Konfitüre fest.",
    rolle=[{"rolle": "lässt Konfitüre gelieren", "prozess": "gelbildung-pektin"}, {"rolle": "hält Gemüse fest", "prozess": "pektin-abbau"}],
    was_passiert="In Früchten und Gemüse verbindet Pektin die Zellen. Herausgelöst und mit viel Zucker und Säure gekocht, bildet es ein Gel.",
    faustregeln=["Gelierzucker enthält schon Pektin und Säure."],
    links=["gelbildung-pektin", "pektin-abbau"], welten=["w-suesses"], quellen=[QM])
zut(id="sahne", titel="Sahne", synonyme=["Rahm", "Vollrahm", "Halbrahm", "Schlagrahm", "Doppelrahm"],
    kurz="Sahne ist Milch mit viel Fett. Mit genug Fett lässt sie sich schlagen, kochen, ohne zu gerinnen, und macht Saucen rund.",
    bild_im_kopf="Wie Milch mit Extraportion Fetttröpfchen.",
    rolle=[{"rolle": "lässt sich zu Schaum schlagen", "prozess": "schaumbildung"}, {"rolle": "bindet und rundet Saucen", "prozess": "emulsion"}, {"rolle": "schützt Eiercremes vor Gerinnen", "prozess": "eiweiss-gerinnung"}],
    was_passiert="Beim Schlagen verbinden sich teilweise geöffnete Fetttröpfchen zu einem Gerüst um Luftblasen. Dafür braucht es genug Fett (Vollrahm) und Kälte. Viel Fett schützt auch vor dem Gerinnen beim Kochen.",
    faustregeln=["Zum Schlagen Vollrahm, gut gekühlt.", "Zum Kochen Vollrahm oder Doppelrahm: Halbrahm kann ausflocken."],
    links=["schaumbildung", "sahne-wird-butter", "emulsion"], welten=["w-milch", "w-saucen"], quellen=[QM])
zut(id="milch", titel="Milch", synonyme=["Vollmilch", "Magermilch"],
    kurz="Milch bringt Eiweiß, Fett, Zucker und Wasser. Sie bräunt Gebäck, bindet mit Stärke und kann anbrennen und gerinnen.",
    bild_im_kopf="Ein Allrounder mit Neigung zum Überkochen.",
    rolle=[{"rolle": "bräunt Teige durch Milchzucker", "prozess": "maillard-reaktion"}, {"rolle": "kann ausflocken", "prozess": "eiweiss-gerinnung"}, {"rolle": "wird mit Stärke zu Béchamel", "prozess": "staerkeverkleisterung"}],
    was_passiert="Beim Erhitzen bildet Milch eine Haut aus Eiweiß, und am Boden brennt Eiweiß leicht an. Säure lässt sie ausflocken.",
    faustregeln=["Bei mittlerer Hitze erwärmen und rühren.", "Topf vorher mit kaltem Wasser ausspülen: Milch brennt weniger an."],
    links=["eiweiss-gerinnung", "maillard-reaktion", "mehlschwitze"], welten=["w-milch"], quellen=[QM])
zut(id="joghurt", titel="Joghurt", synonyme=["Naturjoghurt", "griechischer Joghurt", "Buttermilch"],
    kurz="Joghurt ist von Milchsäurebakterien gesäuerte Milch. Die Säure dickt ein, macht frisch und aktiviert Natron.",
    bild_im_kopf="Milch, der Bakterien eine neue Form gegeben haben.",
    rolle=[{"rolle": "säuert und dickt ein", "prozess": "milchsaeuregaerung"}, {"rolle": "aktiviert Natron im Teig", "prozess": "chemische-lockerung"}, {"rolle": "macht Marinaden mild", "prozess": "marinieren"}],
    was_passiert="Bakterien wandeln Milchzucker in Milchsäure um. Die Säure lässt das Milcheiweiß zu einem zarten Gel eindicken.",
    faustregeln=["Joghurt in heiße Saucen erst am Schluss einrühren, sonst flockt er aus.", "Mit Natron im Teig: schöne Lockerung."],
    links=["milchsaeuregaerung", "chemische-lockerung", "marinieren"], welten=["w-milch"], quellen=[QM])
zut(id="kaese", titel="Käse", synonyme=["Gruyère", "Emmentaler", "Parmesan", "Raclette", "Mozzarella"],
    kurz="Käse ist geronnenes Milcheiweiß mit Fett. Ob er cremig schmilzt oder Fäden zieht und Fett absondert, hängt von Alter, Feuchtigkeit und Säure ab.",
    bild_im_kopf="Wie ein Netz aus Eiweiß, in dem Fett und Wasser gefangen sind.",
    rolle=[{"rolle": "schmilzt zu einer Emulsion", "prozess": "emulsion"}, {"rolle": "gibt Umami und Würze", "prozess": "mehr-geschmack"}],
    was_passiert="Beim Schmelzen lockert sich das Eiweißnetz. Junge, feuchte Käse schmelzen cremig. Sehr alte, trockene Käse geben eher Fett ab. Zu viel Hitze lässt das Eiweiß zusammenziehen: gummiartig mit Fettpfützen.",
    faustregeln=["Fein reiben und bei mittlerer Hitze schmelzen.", "Für Fondue Weißwein und etwas Stärke: Säure und Stärke halten die Emulsion.", "Parmesan in Pasta erst bei mittlerer Hitze einrühren."],
    links=["emulsion", "mantecare", "eiweiss-gerinnung"], welten=["w-milch", "w-pasta"], quellen=[QM])
zut(id="schokolade", titel="Schokolade & Kakao", synonyme=["Kuvertüre", "Kakaopulver", "dunkle Schokolade", "Milchschokolade"],
    kurz="Schokolade ist Kakaomasse, Kakaobutter und Zucker. Die Kakaobutter bestimmt Glanz und Knack, Wasser ist ihr größter Feind.",
    bild_im_kopf="Wie ein feines Kristallgitter, das sowohl Hitze als auch Wasser aus der Fassung bringt.",
    rolle=[{"rolle": "braucht Temperieren für Glanz", "prozess": "fett-kristallisation"}, {"rolle": "klumpt mit wenig Wasser", "prozess": "zucker-kristallisation"}],
    was_passiert="Kakaobutter schmilzt knapp unter Körpertemperatur, darum zergeht Schokolade im Mund. Etwas Wasser lässt sie klumpen, viel Flüssigkeit macht eine glatte Ganache.",
    faustregeln=["Entweder gar kein Wasser oder genug, mindestens ein Viertel des Schokoladengewichts (Richtwert).", "Sanft schmelzen, Wasserbad oder kurze Mikrowellenstöße."],
    links=["temperieren", "fett-kristallisation", "schokolade-klumpt", "schokolade-grau"], welten=["w-suesses"], quellen=[QT, QS])

os.makedirs(OUT, exist_ok=True)
n = 0
for e in E:
    if e is None: continue
    json.dump(e, open(os.path.join(OUT, e["id"] + ".json"), "w"), ensure_ascii=False, indent=2); n += 1
print(n, "Einträge geschrieben")
