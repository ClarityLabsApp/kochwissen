"""Batch 10: Grundlagen-Chemie II. Geschmack, Kälte, Haltbarkeit, Enzyme, Druck, Basen, Zucker.
Schreibt Einträge, ergänzt die Masterliste und verlinkt bestehende Einträge zurück."""
import json, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "content/entries")
QM = {"titel": "Harold McGee: On Food and Cooking (2004)"}
Q = {
  "umami": {"titel": "America’s Test Kitchen: The science of umami", "url": "https://www.americastestkitchen.com/articles/5545-the-science-of-umami"},
  "milch": {"titel": "Penn State: Proteins in dairy and plant milks reduce oral burn from capsaicin", "url": "https://pure.psu.edu/en/publications/more-than-fat-proteins-in-dairy-and-plant-milks-contribute-to-the/"},
  "keime": {"titel": "Kantonales Laboratorium Basel-Stadt: Merkblatt Erhitzen, Warmhalten, Abkühlen, Auftauen (2026)", "url": "https://media.bs.ch/original_file/3149e56eb6c16426bc56ce1407d0c9b45657e304/260521-merkblatt-erhitzen-warmhalten-abkuehlen-auftauen.pdf"},
  "aw": {"titel": "Clemson University: Available moisture in foods", "url": "https://hgic.clemson.edu/available-moisture-in-foods/"},
  "siede": {"titel": "Küchenfibel: Warum kocht Wasser in der Höhe langsamer?", "url": "https://www.kuechenfibel.de/faq/warum-kocht-wasser-in-der-hohe-langsamer"},
  "bfr": {"titel": "BfR: Hygieneregeln helfen, Geflügel sicher zuzubereiten", "url": "https://www.bfr.bund.de/presseinformation/mehr-salmonellen-infektionen-in-europa-hygieneregeln-helfen-gefluegel-sicher-zuzubereiten/"},
}
E = []
def add(**k):
    k.setdefault("status", "entwurf"); k.setdefault("schwierigkeit", "einsteiger"); k.setdefault("quellen", [QM]); k.setdefault("visual", {"vorlage": "keine"}); E.append(k)

# =========================== PROZESSE ===========================
add(id="umami", typ="prozess", titel="Umami: der herzhafte Geschmack", synonyme=["Umami", "herzhaft", "würzig", "Glutamat", "fünfter Geschmack", "Tiefe im Geschmack"],
  kurz="Umami ist der fünfte Grundgeschmack: herzhaft und rund. Er entsteht durch [[glutamat|Glutamat]] und wird stark, wenn zwei Partner zusammenkommen.",
  bild_im_kopf="Wie ein Duett: Glutamat singt allein ordentlich, mit seinem Partner zusammen füllt es den ganzen Saal.",
  was_passiert="Die Zunge hat eigene Sensoren für Glutamat, einen Baustein von Eiweiß. Frei wird es, wenn Eiweiß reift, gärt oder lange kocht: in Parmesan, Tomaten, Pilzen, Sojasauce. Ein zweiter Stoff aus Fleisch, Fisch oder getrockneten Pilzen verändert den Sensor so, dass er viel stärker anspricht. Kommen beide zusammen, schmeckt es um ein Vielfaches herzhafter.",
  warum_wichtig="Erklärt, warum Parmesan auf Tomatensauce, Sardellen im Schmorgericht oder Pilze in der Brühe so viel Tiefe geben, ohne nach sich selbst zu schmecken.",
  faustregeln=["Fehlt einem Gericht Tiefe statt Salz: etwas Parmesan, Tomatenmark, Sojasauce oder Sardelle.", "Zwei Umami-Quellen kombinieren, etwa Tomate mit Fleisch oder Pilze mit Käse.", "Tomatenmark kurz anrösten, das verstärkt sein Aroma."],
  stellschrauben=[{"id": "zeit", "wirkung": "Reifen, Gären und langes Kochen setzen mehr Glutamat frei"}, {"id": "salzgehalt", "wirkung": "Salz und Umami verstärken sich gegenseitig"}],
  praxis=[{"welt": "w-saucen", "text": "Ein Teelöffel Sojasauce oder etwas Parmesanrinde in der Sauce macht sie runder.", "aroma": ["umami"]}, {"welt": "w-fleisch", "text": "Fleisch bringt den Partnerstoff mit: Darum passt Tomate so gut zu Hackfleisch."}],
  links=["mehr-geschmack", "essen-flach", "kaese", "salz-geschmack", "fond", "reduktion"], welten=["w-saucen", "w-fleisch", "w-milch"], quellen=[Q["umami"], QM])

add(id="salz-geschmack", typ="prozess", titel="Salz verstärkt Aromen und dämpft Bitterkeit", synonyme=["Geschmack verstärken", "Salz und Bitterkeit", "Prise Salz", "Salz im Dessert"],
  kurz="Salz schmeckt nicht nur salzig. In kleinen Mengen hebt es andere Aromen hervor und unterdrückt Bitterkeit.",
  bild_im_kopf="Wie das Licht in einem Museum: Richtig eingestellt sieht man jedes Bild besser, zu grell blendet es.",
  was_passiert="Salz wirkt auf die Geschmackswahrnehmung selbst. Unter der Schwelle, ab der etwas salzig schmeckt, lässt es Süße und Aromen voller wirken. Gleichzeitig dämpft es die Wahrnehmung von Bitterkeit, etwa bei Kaffee, Grapefruit, Rosenkohl oder dunkler Schokolade. Zu viel Salz überdeckt dagegen alles andere.",
  warum_wichtig="Erklärt die Prise Salz im Kuchen, im Karamell und in der Schokoladenmousse, und warum ungesalzenes Essen flach wirkt.",
  faustregeln=["Jede süße Speise bekommt eine Prise Salz.", "Bitteres Gemüse zuerst salzen, bevor man Zucker nimmt.", "In kleinen Schritten salzen und dazwischen probieren."],
  stellschrauben=[{"id": "salzgehalt", "wirkung": "wenig hebt hervor, viel überdeckt"}],
  praxis=[{"welt": "w-suesses", "text": "Salzkaramell und Schokolade mit Fleur de Sel: Das Salz macht die Süße tiefer."}, {"welt": "w-gemuese", "text": "Rosenkohl und Chicorée wirken mit genug Salz deutlich weniger bitter."}],
  links=["salz", "mehr-geschmack", "essen-flach", "essen-versalzen", "umami", "abschmecken-saeure"], welten=["w-suesses", "w-gemuese"])

add(id="aroma-loeslichkeit", typ="prozess", titel="Aromen lösen sich in Fett, Wasser oder Alkohol", synonyme=["fettlöslich", "Aroma lösen", "Aroma in Öl", "warum Fett Geschmack trägt"],
  kurz="Viele Aromastoffe lösen sich besser in Fett als in Wasser. Fett trägt darum Geschmack, und Gewürze entfalten sich in Öl stärker.",
  bild_im_kopf="Wie Gäste, die nur mit dem richtigen Taxi nach Hause kommen: Manche Aromen steigen nur ins Fett, andere nur ins Wasser.",
  was_passiert="Aromastoffe sind winzige, oft flüchtige Moleküle. Ein großer Teil davon ist fettliebend: In Öl oder Butter lösen sie sich gut und bleiben länger im Mund. Andere lösen sich in Wasser oder in Alkohol. Wärme macht Aromen flüchtig, darum riecht Warmes stärker, und langes Kochen treibt Duftstoffe aus.",
  warum_wichtig="Erklärt, warum fettarme Varianten flacher schmecken, warum man Gewürze in Öl anröstet und warum Wein in der Sauce andere Aromen löst als Wasser.",
  faustregeln=["Trockene Gewürze kurz in Fett anrösten, nicht ins Wasser streuen.", "Frische Kräuter erst am Ende zugeben, ihre Duftstoffe verfliegen.", "Ein Schuss Wein oder Schnaps löst Aromen, die Wasser nicht erreicht."],
  stellschrauben=[{"id": "fettgehalt", "wirkung": "mehr Fett → mehr Aroma bleibt im Mund"}, {"id": "temperatur", "wirkung": "wärmer → riecht stärker, verfliegt schneller"}],
  praxis=[{"welt": "w-saucen", "text": "Ein Stück kalte Butter am Schluss bindet nicht nur, es trägt auch die Aromen."}],
  links=["aroma-blooming", "gewuerze-roesten", "fett", "mehr-geschmack", "schaerfe"], welten=["w-saucen", "w-gemuese"])

add(id="schaerfe", typ="prozess", titel="Schärfe: Chili, Pfeffer und Senf", synonyme=["scharf", "Chili", "Capsaicin", "brennt im Mund", "Schärfe mildern"],
  kurz="Schärfe ist kein Geschmack, sondern ein Hitze- und Schmerzreiz. Bei Chili löst ihn [[capsaicin|Capsaicin]] aus, das sich in Fett, nicht in Wasser löst.",
  bild_im_kopf="Wie ein falscher Feueralarm: Kein Feuer, aber die Sensoren melden Hitze.",
  was_passiert="Capsaicin aus Chili dockt an Nervenenden an, die normalerweise Hitze melden. Darum fühlt sich Chili heiß an. Weil Capsaicin fettliebend ist, spült Wasser es kaum weg. Milch hilft am besten: Studien zeigen, dass vor allem ihr Eiweiß die Schärfe mildert, nicht nur das Fett. Pfeffer, Senf, Meerrettich und Wasabi nutzen andere Stoffe, die teils in die Nase steigen.",
  warum_wichtig="Erklärt, warum Wasser gegen Chili nichts bringt, Joghurt und Milch aber schon, und wie man ein zu scharfes Gericht rettet.",
  faustregeln=["Zu scharf: Joghurt, Sahne, Kokosmilch oder Milch dazu, nicht Wasser.", "Die meiste Schärfe sitzt in den hellen Scheidewänden der Chili, nicht in den Kernen allein.", "Senf und Meerrettich verlieren beim Kochen an Schärfe, Chili nicht."],
  stellschrauben=[{"id": "fettgehalt", "wirkung": "Fett und Milcheiweiß mildern Chili"}, {"id": "zeit", "wirkung": "langes Ziehen in Öl macht es schärfer"}],
  praxis=[{"welt": "w-milch", "text": "Raita oder ein Klecks Joghurt neben dem Curry ist kein Zufall: Milcheiweiß nimmt Capsaicin auf."}],
  links=["zu-scharf", "gewuerze", "aroma-loeslichkeit", "joghurt", "milch"], welten=["w-gemuese", "w-milch"], quellen=[Q["milch"], QM])

add(id="eiskristalle", typ="prozess", titel="Eiskristalle: schnell gefroren ist feiner", synonyme=["Gefrieren", "Einfrieren", "Eiskristalle", "Glace cremig", "Kristallgröße"],
  kurz="Beim Gefrieren wird Wasser zu Kristallen. Schnelles Gefrieren und Rühren machen sie klein, langsames Gefrieren macht sie groß und grob.",
  bild_im_kopf="Wie Schnee und Hagel: Viele kleine Flocken sind weich, wenige große Körner sind hart und knirschen.",
  was_passiert="Gefriert Wasser langsam, wachsen wenige Kristalle lange und werden groß. Gefriert es schnell oder wird dabei gerührt, entstehen viele Keime gleichzeitig, und alle bleiben klein. Große Kristalle machen Glace körnig und stechen beim Einfrieren durch Zellwände: Das Gemüse wird beim Auftauen weich und lässt Saft. Schwankt die Temperatur im Tiefkühler, wachsen kleine Kristalle mit der Zeit zu großen zusammen.",
  warum_wichtig="Erklärt, warum Glace beim Rühren cremig wird, warum man flach und schnell einfriert und warum aufgetaute Erdbeeren matschig sind.",
  faustregeln=["Flach einfrieren, nicht im dicken Block.", "Glace-Masse vorkühlen und beim Gefrieren rühren.", "Tiefkühler nicht oft öffnen, Temperaturschwankungen vergröbern die Kristalle."],
  stellschrauben=[{"id": "temperatur", "wirkung": "kälter und schneller → kleinere Kristalle"}, {"id": "mechanik", "wirkung": "Rühren hält Kristalle klein"}, {"id": "zuckergehalt", "wirkung": "mehr Zucker → weniger Eis, weicher"}],
  praxis=[{"welt": "w-suesses", "text": "Eine Glacemaschine friert und rührt gleichzeitig: Darum wird sie feiner als Glace aus dem Tiefkühler."}, {"welt": "w-gemuese", "text": "Beeren einzeln auf einem Blech vorfrieren, dann erst in den Beutel."}],
  links=["gefrierpunkt-senkung", "glace-koernig", "gefrierbrand", "einfrieren", "zucker-kristallisation"], welten=["w-suesses", "w-gemuese"], visual={"vorlage": "zoom3-simulation"})

add(id="gefrierpunkt-senkung", typ="prozess", titel="Zucker, Salz und Alkohol senken den Gefrierpunkt", synonyme=["Gefrierpunkt", "Glace bleibt weich", "Salz auf Eis", "warum Glace nicht hart wird"],
  kurz="Gelöster Zucker, Salz oder Alkohol stören das Wasser beim Gefrieren. Es friert erst bei tieferen Temperaturen, und ein Teil bleibt flüssig.",
  bild_im_kopf="Wie eine Tanzfläche voller Leute: Je mehr Fremde dazwischenstehen, desto schwerer finden die Paare zusammen.",
  was_passiert="Wassermoleküle müssen sich zu einem Gitter ordnen, um zu gefrieren. Gelöste Teilchen stehen dabei im Weg, darum friert die Lösung erst unter 0 °C. In Glace bleibt so immer ein Teil flüssig, und sie bleibt löffelbar. Umgekehrt schmilzt Salz Eis: Eis mit Salz wird zu einer Lake, die bis etwa minus 21 °C kalt werden kann.",
  warum_wichtig="Erklärt, warum zuckerarme Glace steinhart wird, warum ein Schuss Alkohol Sorbet weich hält und wie man Glace im Beutel mit Eis und Salz macht.",
  faustregeln=["Glace und Sorbet brauchen genug Zucker, sonst werden sie hart.", "Ein Esslöffel Schnaps hält Sorbet weicher, zu viel verhindert das Gefrieren.", "Eis mit Salz kühlt schneller und tiefer als Eis allein."],
  stellschrauben=[{"id": "zuckergehalt", "wirkung": "mehr → weicher, friert später"}, {"id": "salzgehalt", "wirkung": "Salz auf Eis → eiskalte Lake"}],
  praxis=[{"welt": "w-suesses", "text": "Sorbet aus sehr süßen Früchten wird von selbst weicher als eines aus Zitrone."}],
  links=["eiskristalle", "glace-koernig", "zucker", "salz", "x-glace-beutel"], welten=["w-suesses"], visual={"vorlage": "temperaturskala", "params": {"hinweis": "Richtwerte", "skala": [{"c": -21, "name": "Eis mit Salz: so kalt kann die Lake werden"}, {"c": -18, "name": "Tiefkühler"}, {"c": -5, "name": "süße Glace bleibt löffelbar"}, {"c": 0, "name": "reines Wasser gefriert"}]}})

add(id="wasseraktivitaet", typ="prozess", titel="Haltbarkeit: Salz und Zucker binden das Wasser", synonyme=["Konservieren", "haltbar machen", "Wasseraktivität", "warum Honig nicht schimmelt", "Einsalzen"],
  kurz="Keime brauchen freies Wasser. Salz, Zucker und Trocknen binden es, darum verderben Honig, Konfitüre, Salami und Dörrobst so langsam.",
  bild_im_kopf="Wie eine Oase, in der jeder Tropfen schon vergeben ist: Wer neu ankommt, findet nichts mehr zu trinken.",
  was_passiert="Nicht der Wassergehalt allein zählt, sondern wie viel Wasser frei verfügbar ist (Wasseraktivität). Salz und Zucker binden Wasser an sich, Trocknen entfernt es. Die meisten gefährlichen Bakterien brauchen sehr viel freies Wasser, Schimmel und manche Hefen kommen mit weniger aus. Darum kann Konfitüre schimmeln, Honig aber kaum.",
  warum_wichtig="Erklärt, warum Konfitüre genug Zucker braucht, warum Salami ohne Kühlschrank hält und warum zuckerreduzierte Konfitüre in den Kühlschrank gehört.",
  faustregeln=["Zuckerreduzierte Konfitüre nach dem Öffnen kühl lagern.", "Dörrobst und Nüsse trocken und verschlossen aufbewahren.", "Salz, Zucker und Trocknen ersetzen nicht die Hygiene, sie bremsen Keime nur."],
  stellschrauben=[{"id": "salzgehalt", "wirkung": "bindet Wasser"}, {"id": "zuckergehalt", "wirkung": "bindet Wasser"}, {"id": "feuchtigkeit", "wirkung": "trockener → haltbarer"}],
  praxis=[{"welt": "w-suesses", "text": "Konfitüre mit viel Zucker hält ungeöffnet lange, Honig fast unbegrenzt."}, {"welt": "w-fleisch", "text": "Rohschinken und Salami werden durch Salz und Trocknen haltbar."}],
  links=["keimwachstum", "osmose", "zucker", "salz", "laenger-haltbar", "g-konfituere"], welten=["w-suesses", "w-fleisch"], quellen=[Q["aw"], QM],
  visual={"vorlage": "skala", "params": {"links": "viel freies Wasser: Fleisch, Milch, Brot", "mitte": "Konfitüre, Salami, Hartkäse", "rechts": "kaum freies Wasser: Honig, Dörrobst"}})

add(id="keimwachstum", typ="prozess", titel="Bakterien und Temperatur: die Gefahrenzone", synonyme=["Lebensmittelsicherheit", "Gefahrenzone", "Bakterien", "Essen warm halten", "Reste abkühlen", "Salmonellen"],
  kurz="Bakterien vermehren sich am schnellsten zwischen etwa 10 und 50 °C. Kälte bremst sie, gründliches Erhitzen tötet die meisten ab.",
  bild_im_kopf="Wie Unkraut im Frühling: Bei mildem Wetter wächst es über Nacht, im Frost und in der Hitze ruht es.",
  was_passiert="Bakterien teilen sich bei angenehmer Wärme alle paar Minuten bis Stunden. Der Kühlschrank bremst sie stark, tötet sie aber nicht. Erst ausreichende Hitze macht Fleisch und Reste sicher: Behörden empfehlen mindestens 70 °C im Kern. Gekochtes soll den warmen Bereich schnell durchlaufen, beim Abkühlen höchstens etwa zwei Stunden.",
  warum_wichtig="Erklärt, warum Geflügel durchgegart wird, warum Reste nicht stundenlang auf dem Herd stehen sollen und warum Warmhalten heiß sein muss.",
  faustregeln=["Geflügel, Hackfleisch und Reste auf mindestens 70 °C im Kern erhitzen.", "Warmhalten bei mindestens 65 °C, sonst rasch abkühlen.", "Reste in flachen Gefäßen innerhalb von zwei Stunden in den Kühlschrank.", "Im Kühlschrank auftauen, nicht auf der Küchenablage."],
  stellschrauben=[{"id": "temperatur", "wirkung": "10–50 °C: Bakterien wachsen am schnellsten"}, {"id": "zeit", "wirkung": "je länger im warmen Bereich, desto mehr Keime"}],
  praxis=[{"welt": "w-gefluegel", "text": "Poulet immer durchgaren: mindestens 70 °C im Kern, zwei Minuten lang."}, {"welt": "w-getreide", "text": "Gekochten Reis nicht lange warm stehen lassen, sondern schnell kühlen."}],
  links=["kerntemperatur", "w-gefluegel", "wasseraktivitaet", "einfrieren", "sous-vide"], welten=["w-gefluegel", "w-fleisch", "w-getreide"], quellen=[Q["keime"], Q["bfr"]],
  visual={"vorlage": "temperaturskala", "params": {"hinweis": "Richtwerte der Lebensmittelkontrolle", "skala": [{"c": 5, "name": "Kühlschrank: Bakterien stark gebremst"}, {"c": 10, "name": "ab hier: schnelles Wachstum"}, {"c": 50, "name": "bis hier: schnelles Wachstum"}, {"c": 65, "name": "Warmhalten mindestens"}, {"c": 70, "name": "Erhitzen: mindestens im Kern"}]}})

add(id="poekeln", typ="prozess", titel="Pökeln: Salz und Nitrit", synonyme=["Pökeln", "Schinken rosa", "Nitritpökelsalz", "Rohschinken", "Speck"],
  kurz="Beim Pökeln konserviert Salz das Fleisch. Nitrit im Pökelsalz hält es zusätzlich rosa und schützt vor gefährlichen Keimen.",
  bild_im_kopf="Wie ein Konservator im Museum: Er hält das Bild frisch und die Farbe leuchtend, aber er ändert, wie es aussieht.",
  was_passiert="Salz zieht Wasser und bremst Keime. Im Pökelsalz steckt zusätzlich etwas Nitrit. Es verbindet sich mit dem roten Muskelfarbstoff, der dadurch auch beim Kochen rosa bleibt: Darum ist Kochschinken rosa, ein Braten aber grau. Nitrit hemmt außerdem gefährliche Bakterien und gibt den typischen Schinkengeschmack.",
  warum_wichtig="Erklärt, warum Schinken und Wienerli rosa sind, Braten aber nicht, und warum Pökelsalz nicht wie Kochsalz verwendet wird.",
  faustregeln=["Pökelsalz nur nach Rezept dosieren, nicht als Ersatz für Kochsalz verwenden.", "Gepökeltes nicht stark anbraten oder grillen, bei sehr hoher Hitze können unerwünschte Stoffe entstehen.", "Rosa Farbe bei Gepökeltem heißt nicht roh."],
  stellschrauben=[{"id": "salzgehalt", "wirkung": "mehr Salz → haltbarer, salziger"}, {"id": "zeit", "wirkung": "länger → zieht tiefer ein"}],
  praxis=[{"welt": "w-fleisch", "text": "Kochschinken ist gepökelt und gegart, darum rosa. Ein ungepökelter Schweinebraten wird bei gleicher Temperatur grau."}],
  links=["wasseraktivitaet", "osmose", "lake", "salz", "w-fleisch"], welten=["w-fleisch"], schwierigkeit="fortgeschritten")

add(id="enzym-zartmachen", typ="prozess", titel="Ananas, Kiwi und Papaya zerschneiden Eiweiß", synonyme=["Fleisch zart machen", "Ananas Gelatine", "Bromelain", "Papain", "Kiwi Quark bitter", "Marinade Ananas"],
  kurz="Rohe Ananas, Kiwi, Papaya und Feigen enthalten [[enzym|Enzyme]], die Eiweiß zerschneiden. Sie machen Fleisch mürbe, verhindern aber auch, dass Gelatine fest wird.",
  bild_im_kopf="Wie winzige Scheren, die durch ein Netz schneiden: Ein paar Schnitte machen es weich, zu viele lassen es zerfallen.",
  was_passiert="Die Enzyme spalten lange Eiweißketten in Stücke. Auf Fleisch lockert das die Oberfläche, wird aber schnell mehlig und matschig, weil die Enzyme kaum ins Innere gelangen. Gelatine ist ebenfalls Eiweiß: Mit roher Ananas wird sie nie fest. In Quark mit Kiwi entstehen bittere Bruchstücke. Hitze schaltet die Enzyme ab, darum funktioniert Ananas aus der Dose.",
  warum_wichtig="Erklärt, warum Ananas-Götterspeise flüssig bleibt, warum Kiwi-Quark bitter wird und warum Ananas-Marinaden nur kurz wirken sollen.",
  faustregeln=["Für Gelatine-Desserts Ananas, Kiwi und Papaya kurz aufkochen oder aus der Dose nehmen.", "Ananas-Marinade höchstens eine halbe bis eine Stunde, sonst wird das Fleisch mehlig.", "Kiwi erst kurz vor dem Servieren unter Quark oder Joghurt mischen."],
  stellschrauben=[{"id": "temperatur", "wirkung": "Kochen schaltet die Enzyme ab"}, {"id": "zeit", "wirkung": "länger → mehr zerschnitten, schnell zu viel"}],
  praxis=[{"welt": "w-suesses", "text": "Panna cotta mit frischer Ananas bleibt flüssig, mit Dosen-Ananas wird sie fest."}, {"welt": "w-fleisch", "text": "Asiatische Marinaden mit Ananas oder Papaya wirken an der Oberfläche, nicht im Kern."}],
  links=["enzym", "gelbildung-gelatine", "gelatine", "marinieren", "marinade-matschig", "x-ananas-gelatine"], welten=["w-suesses", "w-fleisch"], visual={"vorlage": "zoom3-simulation"})

add(id="fleischreifung", typ="prozess", titel="Fleischreifung: warum gereiftes Fleisch zarter ist", synonyme=["Dry Aging", "abhängen", "gereiftes Fleisch", "Fleisch reifen lassen", "Wet Aging"],
  kurz="Nach dem Schlachten bauen fleischeigene [[enzym|Enzyme]] die Fasern langsam ab. Das Fleisch wird zarter und, beim Trockenreifen, auch würziger.",
  bild_im_kopf="Wie ein neues Paar Lederschuhe, das mit der Zeit weich wird: Am Anfang steif, nach Wochen bequem.",
  was_passiert="Direkt nach dem Schlachten ist Muskelfleisch steif. In den folgenden Tagen und Wochen lockern Enzyme im Fleisch selbst die Fasern. Beim Trockenreifen am Knochen verdunstet zusätzlich Wasser, der Geschmack konzentriert sich, und es entstehen nussige, käsige Aromen. Die äußere, ausgetrocknete Schicht wird weggeschnitten.",
  warum_wichtig="Erklärt, warum gereiftes Rindfleisch teurer und zarter ist und warum frisches Fleisch vom Bauernhof manchmal zäh ausfällt.",
  faustregeln=["Für Kurzgebratenes vom Rind gereiftes Fleisch wählen.", "Dry Aging zu Hause nur mit eigenem Kühlschrank und großen Stücken, nicht mit Steaks.", "Im Vakuum gereiftes Fleisch wird zarter, aber nicht würziger."],
  stellschrauben=[{"id": "zeit", "wirkung": "länger → zarter, würziger, mehr Verlust"}, {"id": "feuchtigkeit", "wirkung": "trocken gereift → konzentrierter Geschmack"}],
  praxis=[{"welt": "w-fleisch", "text": "Ein Entrecôte mit drei bis vier Wochen Reifung ist spürbar zarter als ein frisches."}],
  links=["enzym", "fleisch-zaeh", "zart", "umami", "w-fleisch"], welten=["w-fleisch"], schwierigkeit="fortgeschritten")

add(id="amylase", typ="prozess", titel="Amylase: Stärke wird zu Zucker", synonyme=["Amylase", "Malz", "Backmalz", "Stärke abbauen", "Teig süßer", "Süßkartoffel süß"],
  kurz="Amylase ist ein [[enzym|Enzym]], das Stärke in Zucker zerlegt. Es füttert die Hefe, bräunt die Kruste und macht Süßkartoffeln süß.",
  bild_im_kopf="Wie ein Bäcker, der lange Brotlaibe in Scheiben schneidet: Erst in kleinen Stücken kann jeder etwas davon essen.",
  was_passiert="Stärke besteht aus langen Ketten von Zuckerbausteinen. Amylase schneidet sie in kurze Stücke. Im Mehl steckt etwas davon, Malz enthält viel. Im Teig liefert sie der Hefe Futter und lässt Zucker für eine braune Kruste übrig. Süßkartoffeln enthalten selbst Amylase: Langsam gegart, arbeitet sie länger und macht sie süßer.",
  warum_wichtig="Erklärt, warum Bäcker Backmalz verwenden, warum lange geführte Teige eine dunklere Kruste bekommen und warum Süßkartoffeln aus dem Ofen süßer schmecken als gekochte.",
  faustregeln=["Für eine kräftige Kruste: lange, kühle Teigführung oder etwas Backmalz.", "Süßkartoffeln langsam im Ofen garen, nicht schnell kochen.", "Kauen startet Amylase im Speichel: Brot schmeckt nach langem Kauen süßlich."],
  stellschrauben=[{"id": "zeit", "wirkung": "länger → mehr Zucker"}, {"id": "temperatur", "wirkung": "warm arbeitet sie, Kochen stoppt sie"}],
  praxis=[{"welt": "w-brot", "text": "Kalte Gare über Nacht gibt der Amylase Zeit: mehr Zucker, braunere Kruste."}, {"welt": "w-kartoffeln", "text": "Süßkartoffeln eine Stunde bei mittlerer Hitze im Ofen werden fast karamellig."}],
  links=["enzym", "staerkeverkleisterung", "hefegaerung", "maillard-reaktion", "kalte-gare", "mehl"], welten=["w-brot", "w-kartoffeln", "w-getreide"], schwierigkeit="fortgeschritten")

add(id="siedepunkt-druck", typ="prozess", titel="Siedepunkt: Druck und Höhe", synonyme=["Siedepunkt", "Dampfkochtopf", "Kochen in den Bergen", "Wasser kocht bei 90 Grad", "Schnellkochtopf"],
  kurz="Wasser kocht nur auf Meereshöhe bei 100 °C. In den Bergen kocht es früher, im Dampfkochtopf erst bei etwa 120 °C.",
  bild_im_kopf="Wie ein Deckel auf einem vollen Saal: Drückt er stark, kommt niemand hinaus, bis es richtig heiß wird.",
  was_passiert="Wasser kocht, wenn sein Dampf so stark drückt wie die Luft darüber. Weniger Luftdruck in der Höhe heißt: Es kocht schon bei tieferer Temperatur, etwa 1 °C weniger pro 300 Höhenmeter. Auf 3000 m kocht Wasser bei rund 90 °C. Der Dampfkochtopf macht es umgekehrt: Er hält den Dampf zurück, der Druck steigt, und Wasser wird etwa 120 °C heiß. Höhere Temperatur heißt kürzere Garzeit.",
  warum_wichtig="Erklärt, warum Pasta und Eier in der Berghütte länger brauchen und warum der Dampfkochtopf Bohnen und Schmorfleisch in einem Bruchteil der Zeit gart.",
  faustregeln=["In den Bergen Garzeiten verlängern, Hitze erhöhen hilft nicht.", "Dampfkochtopf für Hülsenfrüchte, Fond und Schmorgerichte: etwa ein Drittel der Zeit.", "Dampfkochtopf erst öffnen, wenn der Druck ganz abgebaut ist."],
  stellschrauben=[{"id": "temperatur", "wirkung": "mehr Druck → heißeres Wasser"}],
  praxis=[{"welt": "w-eier", "text": "Ein 6-Minuten-Ei auf 2000 m ist weicher als im Unterland, weil das Wasser kühler kocht."}, {"welt": "w-fleisch", "text": "Rindsvoressen im Dampfkochtopf wird in rund einer Stunde zart."}],
  links=["dampfkochtopf", "verdampfen", "wasser", "kollagen-gelatine", "bohnen-nicht-weich", "temperatur"], welten=["w-eier", "w-fleisch", "w-getreide"], quellen=[Q["siede"], QM],
  visual={"vorlage": "temperaturskala", "params": {"hinweis": "Richtwerte", "skala": [{"c": 71, "name": "Mount Everest"}, {"c": 90, "name": "auf rund 3000 m"}, {"c": 98, "name": "Luzern (rund 435 m)"}, {"c": 100, "name": "Meereshöhe"}, {"c": 120, "name": "Dampfkochtopf"}]}})

add(id="basen-braeunung", typ="prozess", titel="Basen beschleunigen die Bräunung", synonyme=["Lauge", "Laugenbrezel", "Natron bräunt", "basisch", "Brezel braun"],
  kurz="In basischer Umgebung läuft die [[maillard-reaktion|Maillard-Reaktion]] viel schneller. Darum werden Laugenbrezeln tiefbraun und Zwiebeln mit einer Prise Natron schneller dunkel.",
  bild_im_kopf="Wie Rückenwind beim Velofahren: Der Weg ist derselbe, aber man kommt viel schneller ans Ziel.",
  was_passiert="Die Bräunungsreaktion hängt vom [[ph-wert|pH-Wert]] ab. Säure bremst sie, Basen wie Natron oder Lauge beschleunigen sie stark. Laugengebäck wird vor dem Backen kurz in eine Lauge getaucht: Die Oberfläche bräunt dann tief, glänzt und schmeckt typisch. Eine Prise Natron lässt Zwiebeln schneller braun und weich werden, zu viel schmeckt seifig.",
  warum_wichtig="Erklärt die Farbe von Brezeln und Laugenbrötchen und warum ein Hauch Natron beim Anbraten Zeit spart.",
  faustregeln=["Für Zwiebeln eine Messerspitze Natron, nicht mehr.", "Säure wie Zitrone oder Wein bremst die Bräunung, also erst später zugeben.", "Echte Backlauge ist ätzend: Handschuhe, Brille, nichts aus Aluminium."],
  stellschrauben=[{"id": "ph-wert", "wirkung": "basisch → schneller braun, sauer → langsamer"}],
  praxis=[{"welt": "w-brot", "text": "Laugenbrezel: kurz in Lauge getaucht, dann gebacken. Mit gebackenem Natron geht es zu Hause milder."}, {"welt": "w-gemuese", "text": "Natron-Zwiebeln werden in der Hälfte der Zeit goldbraun."}],
  links=["maillard-reaktion", "ph-wert", "natron", "natron-zwiebeln", "laugen"], welten=["w-brot", "w-gemuese"])

add(id="zucker-feuchtigkeit", typ="prozess", titel="Zucker hält Feuchtigkeit fest", synonyme=["Kuchen saftig", "Zucker bindet Wasser", "hygroskopisch", "Kuchen bleibt frisch", "Honig im Teig"],
  kurz="Zucker zieht Wasser an und hält es fest. Kuchen mit genug Zucker bleiben länger saftig, Kekse mit Honig werden weich.",
  bild_im_kopf="Wie ein Schwamm im Teig: Er saugt Feuchtigkeit auf und gibt sie nur langsam wieder ab.",
  was_passiert="Zucker bindet Wasser (er ist hygroskopisch). Im Teig hält er es fest, sodass beim Backen weniger verdunstet und der Kuchen danach langsamer austrocknet. Er bremst auch das Altbackenwerden der Stärke. Honig und Sirup ziehen sogar Feuchtigkeit aus der Luft: Kekse damit werden in der Dose weich, reine Zuckerkekse bleiben knusprig.",
  warum_wichtig="Erklärt, warum zuckerreduzierte Kuchen trockener sind und warum Honiglebkuchen mit der Zeit weich werden.",
  faustregeln=["Zucker nicht mehr als um ein Viertel reduzieren, sonst wird der Kuchen trocken und blass.", "Für weiche Kekse etwas Honig oder braunen Zucker verwenden, für knusprige weißen Zucker.", "Knusprige und weiche Kekse getrennt aufbewahren."],
  stellschrauben=[{"id": "zuckergehalt", "wirkung": "mehr → saftiger, länger frisch"}, {"id": "feuchtigkeit", "wirkung": "Honig zieht Wasser aus der Luft"}],
  praxis=[{"welt": "w-gebaeck", "text": "Lebkuchen mit Honig werden nach ein paar Tagen in der Dose weich und besser."}],
  links=["zucker", "honig", "kuchen-trocken", "laenger-frisch", "retrogradation", "wasseraktivitaet"], welten=["w-gebaeck", "w-suesses"])

add(id="kalzium-pektin", typ="prozess", titel="Kalk und Säure halten Gemüse fest", synonyme=["hartes Wasser", "Kalk", "Bohnen bleiben hart", "Gemüse bleibt fest", "Tomaten Bohnen"],
  kurz="Kalk aus hartem Wasser und Säure festigen den Kitt zwischen Pflanzenzellen. Hülsenfrüchte und Gemüse werden dann langsamer weich.",
  bild_im_kopf="Wie Klammern in einem Ordner: Mit Klammern hält der Stapel zusammen, ohne fällt er auseinander.",
  was_passiert="Pflanzenzellen kleben über [[pektin|Pektin]] aneinander. Kalzium verbindet die Pektinketten zusätzlich wie Klammern. In hartem Wasser oder mit Tomaten und Wein bleibt Gemüse darum länger fest, Hülsenfrüchte werden manchmal gar nicht richtig weich. Natron macht das Wasser basisch und weicher: Bohnen und Kichererbsen garen schneller.",
  warum_wichtig="Erklärt, warum Bohnen im Tomatensugo hart bleiben, warum Kichererbsen mit Natron weicher werden und wie man Bratkartoffeln fest hält.",
  faustregeln=["Hülsenfrüchte erst weich kochen, dann zu Tomate oder Wein geben.", "Bei hartem Wasser eine Prise Natron ins Einweichwasser.", "Für feste Bratkartoffeln einen Schuss Essig ins Kochwasser."],
  stellschrauben=[{"id": "ph-wert", "wirkung": "sauer → bleibt fest, basisch → wird weich"}],
  praxis=[{"welt": "w-gemuese", "text": "Kichererbsen mit einer Prise Natron gekocht werden für Hummus besonders glatt."}],
  links=["pektin-abbau", "pektin", "natron", "saeure", "bohnen-nicht-weich", "gemuese-matschig"], welten=["w-gemuese"])

# =========================== SYMPTOME ===========================
def symptom(id, titel, syn, kurz, bild, ursachen, diag, links, welten, quellen=None):
    add(id=id, typ="symptom", titel=titel, synonyme=syn, kurz=kurz, bild_im_kopf=bild, ursachen=ursachen, diagnose=diag, links=links, welten=welten, visual={"vorlage": "entscheidungsbaum"}, **({"quellen": quellen} if quellen else {}))

symptom("glace-koernig", "Glace wird körnig oder steinhart", ["Glace hart", "Eis körnig", "Sorbet hart", "Glace eisig"],
  "Große Eiskristalle machen Glace körnig, zu wenig Zucker macht sie hart.",
  "Wie Schnee, der getaut und wieder gefroren ist: Aus Pulver wird verharschte Kruste.",
  [{"titel": "Zu langsam gefroren, nicht gerührt", "haeufigkeit": 3, "prinzip": "eiskristalle", "warum": "Ohne Rühren wachsen wenige große Kristalle.", "fix": ["Masse gut vorkühlen", "Im Tiefkühler alle 30 Minuten kräftig durchrühren, oder eine Glacemaschine nehmen"]},
   {"titel": "Zu wenig Zucker", "haeufigkeit": 2, "prinzip": "gefrierpunkt-senkung", "warum": "Zucker hält einen Teil flüssig. Fehlt er, friert alles fest.", "fix": ["Zucker nicht stark reduzieren", "Ein Esslöffel Schnaps oder etwas Glukosesirup hält weicher"]},
   {"titel": "Angetaut und wieder gefroren", "haeufigkeit": 2, "prinzip": "eiskristalle", "warum": "Beim Antauen schmelzen kleine Kristalle, beim Gefrieren wachsen die großen weiter.", "fix": ["Glace nicht lange draußen stehen lassen", "Folie direkt auf die Oberfläche legen"]}],
  {"q1": {"frage": "Ist sie eher körnig oder eher steinhart?", "antworten": [["Körnig, knirscht", "q2"], ["Steinhart", "u1"]]}, "q2": {"frage": "Wurde sie schon einmal angetaut?", "antworten": [["Nein", "u0"], ["Ja", "u2"]]}, "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
  ["eiskristalle", "gefrierpunkt-senkung", "einfrieren", "cremig"], ["w-suesses"])

symptom("bohnen-nicht-weich", "Bohnen und Kichererbsen werden nicht weich", ["Hülsenfrüchte hart", "Kichererbsen hart", "Linsen bleiben hart", "Bohnen bleiben hart"],
  "Hülsenfrüchte bleiben hart, wenn sie alt sind, in hartem Wasser kochen oder zu früh Säure bekommen.",
  "Wie ein alter Schwamm, der kein Wasser mehr aufnehmen will.",
  [{"titel": "Säure zu früh zugegeben", "haeufigkeit": 3, "prinzip": "kalzium-pektin", "warum": "Tomate, Wein oder Essig festigen den Kitt zwischen den Zellen.", "fix": ["Erst weich kochen, dann Säure zugeben"]},
   {"titel": "Hartes Wasser", "haeufigkeit": 2, "prinzip": "kalzium-pektin", "warum": "Kalk verklammert das Pektin.", "fix": ["Eine Prise Natron ins Einweich- und Kochwasser", "Oder im Dampfkochtopf garen"]},
   {"titel": "Alte, sehr trockene Hülsenfrüchte", "haeufigkeit": 2, "prinzip": "pektin-abbau", "warum": "Lang gelagerte Bohnen nehmen kaum noch Wasser auf.", "fix": ["Über Nacht einweichen", "Frische Ware kaufen, länger kochen"]}],
  {"q1": {"frage": "War Tomate, Wein oder Essig von Anfang an im Topf?", "antworten": [["Ja", "u0"], ["Nein", "q2"]]}, "q2": {"frage": "Hast du kalkhaltiges Wasser?", "antworten": [["Ja oder weiß nicht", "u1"], ["Nein", "u2"]]}, "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
  ["kalzium-pektin", "siedepunkt-druck", "natron", "dampfkochtopf"], ["w-gemuese"])

symptom("gefrierbrand", "Gefrierbrand: graue, trockene Stellen", ["Gefrierbrand", "Fleisch tiefgekühlt grau", "Eis im Beutel", "trockene Stellen gefroren"],
  "Gefrierbrand sind ausgetrocknete Stellen: Eis ist direkt aus dem Lebensmittel verdunstet.",
  "Wie Wäsche, die im Winter draußen gefroren trocknet: Das Eis verschwindet, ohne zu schmelzen.",
  [{"titel": "Luft im Beutel", "haeufigkeit": 3, "prinzip": "eiskristalle", "warum": "Eis verdunstet in die Luft und setzt sich als Reif im Beutel ab ([[sublimation|Sublimation]]).", "fix": ["Luft aus dem Beutel drücken oder vakuumieren", "Gut verschließen"]},
   {"titel": "Zu lange gelagert oder Temperaturschwankungen", "haeufigkeit": 2, "prinzip": "eiskristalle", "warum": "Jeder Wechsel treibt mehr Feuchtigkeit aus.", "fix": ["Datum notieren, innerhalb einiger Monate aufbrauchen", "Tiefkühler selten öffnen"]}],
  {"q1": {"frage": "War viel Luft im Beutel oder Behälter?", "antworten": [["Ja", "u0"], ["Nein", "u1"]]}, "u0": {"ursache": 0}, "u1": {"ursache": 1}},
  ["eiskristalle", "einfrieren", "sublimation"], ["w-fleisch", "w-fisch"])

symptom("zu-scharf", "Das Essen ist zu scharf", ["zu scharf", "Chili zu viel", "Curry zu scharf", "Schärfe retten"],
  "Zu viel Chili lässt sich nicht herauskochen, aber mildern: mit Milchprodukten, Fett, Säure und mehr Masse.",
  "Wie ein zu lautes Instrument im Orchester: Man kann es nicht leiser machen, aber die anderen lauter.",
  [{"titel": "Zu viel Chili oder Chilischoten mit Scheidewänden", "haeufigkeit": 3, "prinzip": "schaerfe", "warum": "Capsaicin löst sich nicht in Wasser, Verdünnen mit Wasser hilft kaum.", "fix": ["Joghurt, Sahne, Kokosmilch oder Milch einrühren", "Mehr von den anderen Zutaten dazugeben", "Etwas Zucker und Säure gleichen aus"]},
   {"titel": "Chili zu lange in Öl gezogen", "haeufigkeit": 1, "prinzip": "aroma-loeslichkeit", "warum": "Im Fett löst sich besonders viel Capsaicin.", "fix": ["Chili kürzer anbraten oder erst später zugeben"]}],
  {"q1": {"frage": "Hast du die Chili am Anfang lange in Öl angebraten?", "antworten": [["Ja", "u1"], ["Nein", "u0"]]}, "u0": {"ursache": 0}, "u1": {"ursache": 1}},
  ["schaerfe", "aroma-loeslichkeit", "joghurt"], ["w-gemuese", "w-saucen"], quellen=[Q["milch"], QM])

symptom("marinade-matschig", "Fleisch aus der Marinade ist mehlig oder matschig", ["Marinade matschig", "Fleisch mehlig", "Ananas Marinade zu lange", "Fleisch zerfällt Marinade"],
  "Enzyme aus Ananas, Kiwi oder Papaya und starke Säure greifen die Oberfläche an. Zu lange mariniert, wird sie mehlig.",
  "Wie ein Pullover, der zu heiß gewaschen wurde: Die Oberfläche ist danach nicht mehr dieselbe.",
  [{"titel": "Ananas, Kiwi oder Papaya roh in der Marinade", "haeufigkeit": 3, "prinzip": "enzym-zartmachen", "warum": "Die Enzyme zerschneiden Eiweiß an der Oberfläche immer weiter.", "fix": ["Höchstens eine halbe bis eine Stunde marinieren", "Oder die Frucht vorher kurz aufkochen"]},
   {"titel": "Zu viel Säure zu lange", "haeufigkeit": 2, "prinzip": "saeure-denaturierung", "warum": "Säure gart die Oberfläche chemisch, sie wird weiß und krümelig.", "fix": ["Säure sparsam, Marinade eher ölig und würzig", "Säure erst kurz vor dem Braten"]}],
  {"q1": {"frage": "War Ananas, Kiwi oder Papaya in der Marinade?", "antworten": [["Ja", "u0"], ["Nein", "u1"]]}, "u0": {"ursache": 0}, "u1": {"ursache": 1}},
  ["enzym-zartmachen", "saeure-denaturierung", "marinieren"], ["w-fleisch"])

# =========================== ZIEL ===========================
add(id="laenger-haltbar", typ="ziel", titel="Länger haltbar machen", synonyme=["haltbar", "konservieren", "Vorrat", "länger aufbewahren", "Reste aufbewahren"],
  kurz="Lebensmittel halten länger, wenn Keime kein freies Wasser, keine Wärme oder keine Zeit bekommen.",
  bild_im_kopf="Wie ein Haus gegen Einbrecher: Abschließen, Licht an, Wachhund. Jede Maßnahme allein hilft, zusammen am besten.",
  hebel=["temperatur", "salzgehalt", "zuckergehalt", "feuchtigkeit", "ph-wert"],
  faustregeln=["Reste rasch abkühlen und in den Kühlschrank.", "Flach einfrieren und luftdicht verpacken.", "Salz, Zucker, Säure und Trocknen machen haltbar, ersetzen aber keine Hygiene."],
  links=["keimwachstum", "wasseraktivitaet", "einfrieren", "poekeln", "milchsaeuregaerung", "g-konfituere", "lake"], welten=["w-suesses", "w-fleisch", "w-gemuese"], visual={"vorlage": "punktmatrix", "params": {"zeilen": "hebel", "spalten": "techniken"}})

# =========================== TECHNIKEN ===========================
add(id="einfrieren", typ="technik", titel="Richtig einfrieren und auftauen", synonyme=["einfrieren", "tiefkühlen", "auftauen", "Schockfrosten", "Vorrat einfrieren"],
  kurz="Schnell, flach und luftdicht einfrieren, langsam im Kühlschrank auftauen: So bleiben Struktur und Geschmack erhalten.",
  bild_im_kopf="Wie ein Foto mit kurzer Belichtung: Je schneller der Moment festgehalten wird, desto schärfer bleibt das Bild.",
  schritte=["Gekochtes zuerst abkühlen lassen, nicht warm in den Tiefkühler.", "Flach in Beutel füllen, Luft herausdrücken, beschriften.", "Beeren und Teigstücke einzeln auf einem Blech vorfrieren.", "Im Kühlschrank auftauen, Fleisch auf einem Teller.", "Aufgetautes rasch verwenden und nicht wieder roh einfrieren."],
  faustregeln=["Flach friert schneller als ein Block.", "Luftdicht verpacken gegen Gefrierbrand.", "Gemüse vorher kurz blanchieren, das stoppt Enzyme."],
  links=["eiskristalle", "gefrierbrand", "keimwachstum", "blanchieren", "laenger-haltbar"], welten=["w-gemuese", "w-fleisch", "w-suesses"], quellen=[Q["keime"], QM])

add(id="dampfkochtopf", typ="technik", titel="Mit dem Dampfkochtopf garen", synonyme=["Dampfkochtopf", "Schnellkochtopf", "Druckkochtopf", "Kukident", "Duromatic"],
  kurz="Der Dampfkochtopf hält den Dampf zurück. Unter Druck wird das Wasser etwa 120 °C heiß, und alles gart viel schneller.",
  bild_im_kopf="Wie eine Abkürzung über den Berg: gleiche Strecke, aber viel weniger Zeit.",
  schritte=["Mindestens die angegebene Flüssigkeitsmenge einfüllen, höchstens zu zwei Dritteln füllen.", "Deckel schließen, auf hoher Stufe erhitzen, bis der Druck anzeigt.", "Hitze reduzieren, sodass der Druck gerade gehalten wird, Garzeit ab jetzt rechnen.", "Druck abbauen lassen oder nach Anleitung ablassen, erst dann öffnen."],
  faustregeln=["Etwa ein Drittel der normalen Garzeit, Richtwert.", "Hülsenfrüchte und Getreide schäumen: nur halb füllen.", "Nie mit Gewalt öffnen."],
  links=["siedepunkt-druck", "schmoren", "bohnen-nicht-weich", "kollagen-gelatine", "fond"], welten=["w-fleisch", "w-gemuese", "w-getreide"], quellen=[Q["siede"], QM])

add(id="laugen", typ="technik", titel="Laugengebäck: mit Natron statt Lauge", synonyme=["Laugenbrezel", "Laugenbrötchen", "Laugengebäck", "gebackenes Natron", "Brezel selber machen"],
  kurz="Laugengebäck bekommt Farbe und Geschmack durch ein basisches Bad. Zu Hause gelingt das milder mit gebackenem Natron.",
  bild_im_kopf="Wie eine Grundierung vor dem Malen: Der kurze Tauchgang entscheidet, wie die Farbe später wird.",
  schritte=["Natron auf einem Blech etwa eine Stunde bei 120–150 °C backen, das macht es stärker basisch (Richtwert).", "Etwa 2 Esslöffel davon in einem Liter heißem Wasser lösen.", "Geformte Brezeln 20–30 Sekunden eintauchen, abtropfen lassen.", "Mit grobem Salz bestreuen und heiß backen."],
  faustregeln=["Gebackenes Natron ist reizend: nicht ins Gesicht, Hände danach waschen.", "Kein Aluminiumblech und keine Aluminiumschüssel verwenden.", "Echte Backlauge (Natronlauge) gibt mehr Farbe, ist aber ätzend: nur mit Handschuhen und Schutzbrille."],
  links=["basen-braeunung", "natron", "maillard-reaktion", "w-brot"], welten=["w-brot"], schwierigkeit="fortgeschritten")

# =========================== BEGRIFFE ===========================
def begriff(id, titel, syn, kurz, links):
    add(id=id, typ="begriff", titel=titel, synonyme=syn, kurz=kurz, links=links)
begriff("glutamat", "Glutamat", ["Glutaminsäure", "MSG", "Mononatriumglutamat"], "Ein Baustein von Eiweiß, der den herzhaften Umami-Geschmack auslöst. Frei kommt er in Parmesan, Tomaten, Pilzen und Sojasauce vor.", ["umami"])
begriff("capsaicin", "Capsaicin", ["Capsaicinoide"], "Der Stoff in Chili, der Schärfe auslöst. Er reizt Nerven, die sonst Hitze melden, und löst sich in Fett, nicht in Wasser.", ["schaerfe"])
begriff("sublimation", "Sublimation", ["sublimieren"], "Wenn Eis direkt zu Dampf wird, ohne vorher zu schmelzen. So trocknet Gefriergut aus und Wäsche im Winterfrost.", ["gefrierbrand", "eiskristalle"])

# =========================== EXPERIMENTE ===========================
add(id="x-glace-beutel", typ="experiment", titel="Glace im Beutel schütteln", synonyme=["Eis selber machen Kinder", "Glace ohne Maschine", "Salz Eis Experiment"],
  kurz="Mit Eiswürfeln, Salz und zwei Beuteln wird Milch in zehn Minuten zu Glace.",
  material=["250 ml Milch oder halb Milch, halb Rahm", "2 EL Zucker, etwas Vanillezucker", "ein kleiner und ein großer Gefrierbeutel mit Verschluss", "2 Handvoll Eiswürfel", "4 EL grobes Salz", "Handschuhe oder ein Küchentuch"],
  schritte=["Milch und Zucker in den kleinen Beutel füllen, Luft herausdrücken, gut verschließen.", "Eis und Salz in den großen Beutel geben.", "Den kleinen Beutel hineinlegen, den großen verschließen.", "Mit Handschuhen 5–10 Minuten kräftig schütteln und kneten.", "Zum Vergleich einen zweiten Versuch mit Eis ohne Salz machen."],
  beobachtung="Mit Salz wird die Milch nach einigen Minuten fest und cremig, der große Beutel wird außen eiskalt und beschlägt. Ohne Salz bleibt die Milch flüssig.",
  erklaerung="Salz lässt das Eis schmelzen und senkt den Gefrierpunkt der entstehenden Lake weit unter 0 °C. Diese Lake zieht der Milch Wärme ab, bis sie gefriert. Das Schütteln hält die Eiskristalle klein, darum wird die Glace cremig.",
  dauer="15 Minuten", sicherheit="Die Salzlake wird sehr kalt: nicht mit bloßen Händen lange festhalten.",
  links=["gefrierpunkt-senkung", "eiskristalle", "salz"], welten=["w-suesses"],
  visual={"vorlage": "vergleich", "params": {"vorher": "Start", "nachher": "nach 10 Minuten Schütteln", "vergleich": [
    {"label": "Eis mit Salz", "gefaess": "schuessel", "inhalt": "fluessig", "vorher": {"farbe": "#fbf7ec", "fuell": 0.5, "klumpen": 0, "klumpenfarbe": "#fffaf0"}, "nachher": {"farbe": "#eaf1f4", "fuell": 0.5, "klumpen": 1, "klumpenfarbe": "#fffaf0"}},
    {"label": "Eis ohne Salz", "gefaess": "schuessel", "inhalt": "fluessig", "vorher": {"farbe": "#fbf7ec", "fuell": 0.5}, "nachher": {"farbe": "#fbf7ec", "fuell": 0.5, "klumpen": 0.1, "klumpenfarbe": "#fffaf0"}}]}})

add(id="x-ananas-gelatine", typ="experiment", titel="Warum Ananas die Götterspeise verhindert", synonyme=["Ananas Gelatine Experiment", "Götterspeise flüssig", "Wackelpudding Ananas"],
  kurz="Mit frischer Ananas bleibt Gelatine flüssig, mit gekochter Ananas wird sie fest.",
  material=["1 Päckchen Götterspeise oder Gelatine mit Saft", "frische Ananas", "Ananas aus der Dose", "drei Gläser"],
  schritte=["Götterspeise nach Packung zubereiten und auf drei Gläser verteilen.", "Ins erste Glas Stücke frischer Ananas geben, ins zweite Dosen-Ananas, das dritte bleibt ohne.", "Alles einige Stunden in den Kühlschrank stellen.", "Gläser kippen und vergleichen."],
  beobachtung="Ohne Ananas und mit Dosen-Ananas wird die Götterspeise fest. Mit frischer Ananas bleibt sie flüssig oder wird nur rund um die Stücke weich.",
  erklaerung="Frische Ananas enthält ein Enzym, das Eiweiß zerschneidet. Gelatine ist Eiweiß, ihr Netz wird zerlegt, bevor es fest werden kann. Beim Herstellen von Dosen-Ananas wird die Frucht erhitzt, das schaltet das Enzym ab.",
  dauer="einige Stunden", sicherheit="Heißes Wasser für die Götterspeise: Erwachsene übernehmen das Erhitzen.",
  links=["enzym-zartmachen", "gelbildung-gelatine", "gelatine", "enzym"], welten=["w-suesses"],
  visual={"vorlage": "vergleich", "params": {"vorher": "eingefüllt", "nachher": "nach einigen Stunden", "vergleich": [
    {"label": "frische Ananas", "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#e9b13c", "fuell": 0.6}, "nachher": {"farbe": "#e9b13c", "fuell": 0.6, "blasen": 0.15}},
    {"label": "Dosen-Ananas", "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#e9b13c", "fuell": 0.6}, "nachher": {"farbe": "#d99a24", "fuell": 0.6, "klumpen": 1, "klumpenfarbe": "#d99a24"}},
    {"label": "ohne Ananas", "gefaess": "glas", "inhalt": "fluessig", "vorher": {"farbe": "#e9b13c", "fuell": 0.6}, "nachher": {"farbe": "#d99a24", "fuell": 0.6, "klumpen": 1, "klumpenfarbe": "#d99a24"}}]}})

# =========================== Schreiben ===========================
for e in E:
    json.dump(e, open(os.path.join(OUT, e["id"] + ".json"), "w"), ensure_ascii=False, indent=2)
    open(os.path.join(OUT, e["id"] + ".json"), "a").write("\n")

# Bestehende Einträge zurückverlinken
BACK = {
  "salz": ["salz-geschmack", "wasseraktivitaet", "gefrierpunkt-senkung"], "zucker": ["zucker-feuchtigkeit", "gefrierpunkt-senkung", "wasseraktivitaet"],
  "natron": ["basen-braeunung", "kalzium-pektin", "laugen"], "mehr-geschmack": ["umami", "salz-geschmack", "aroma-loeslichkeit"],
  "essen-flach": ["umami", "salz-geschmack"], "kaese": ["umami"], "gelatine": ["enzym-zartmachen"], "gelbildung-gelatine": ["enzym-zartmachen", "x-ananas-gelatine"],
  "marinieren": ["enzym-zartmachen", "marinade-matschig"], "fleisch-zaeh": ["fleischreifung"], "zart": ["fleischreifung", "enzym-zartmachen"],
  "w-fleisch": ["fleischreifung", "poekeln", "keimwachstum"], "w-suesses": ["eiskristalle", "gefrierpunkt-senkung", "x-glace-beutel"],
  "w-gefluegel": ["keimwachstum"], "temperatur": ["siedepunkt-druck", "keimwachstum"], "wasser": ["siedepunkt-druck"], "verdampfen": ["siedepunkt-druck"],
  "gewuerze": ["schaerfe", "aroma-loeslichkeit"], "kuchen-trocken": ["zucker-feuchtigkeit"], "laenger-frisch": ["zucker-feuchtigkeit", "laenger-haltbar"],
  "honig": ["zucker-feuchtigkeit", "wasseraktivitaet"], "saeure": ["kalzium-pektin"], "gemuese-matschig": ["kalzium-pektin"], "pektin-abbau": ["kalzium-pektin"],
  "natron-zwiebeln": ["basen-braeunung"], "maillard-reaktion": ["basen-braeunung"], "ph-wert": ["basen-braeunung", "kalzium-pektin"],
  "mehl": ["amylase"], "w-getreide": ["amylase"], "kalte-gare": ["amylase"], "w-brot": ["amylase", "laugen"], "enzym": ["enzym-zartmachen", "fleischreifung", "amylase"],
  "schmoren": ["dampfkochtopf"], "kollagen-gelatine": ["dampfkochtopf"], "kerntemperatur": ["keimwachstum"], "sous-vide": ["keimwachstum"],
  "joghurt": ["schaerfe"], "milch": ["schaerfe"], "aroma-blooming": ["aroma-loeslichkeit"], "lake": ["poekeln"], "osmose": ["wasseraktivitaet"],
  "zucker-kristallisation": ["eiskristalle"], "cremig": ["glace-koernig"], "blanchieren": ["einfrieren"], "milchsaeuregaerung": ["laenger-haltbar"], "g-konfituere": ["wasseraktivitaet"],
}
for id, add_links in BACK.items():
    p = os.path.join(OUT, id + ".json")
    if not os.path.exists(p): print("fehlt:", id); continue
    e = json.load(open(p)); e.setdefault("links", [])
    for l in add_links:
        if l not in e["links"]: e["links"].append(l)
    json.dump(e, open(p, "w"), ensure_ascii=False, indent=2); open(p, "a").write("\n")

# Masterliste
mp = os.path.join(ROOT, "content/master-list.json"); M = json.load(open(mp))
by = {m["id"]: m for m in M["eintraege"]}
for e in E:
    if e["typ"] == "begriff": continue
    if e["id"] not in by:
        M["eintraege"].append({"id": e["id"], "typ": e["typ"], "titel": e["titel"], "status": "geplant", "pilot": False, "links": e["links"], "welten": e.get("welten", []), "synonyme": e["synonyme"], "verlinkt_von": [], "visual": {"vorlage": e["visual"]["vorlage"]}})
by = {m["id"]: m for m in M["eintraege"]}
for id, add_links in BACK.items():
    if id in by:
        for l in add_links:
            if l in by and l not in by[id]["links"]: by[id]["links"].append(l)
ids = set(by); back = {i: set() for i in ids}
for m in M["eintraege"]:
    for l in m["links"]:
        if l in back: back[l].add(m["id"])
for m in M["eintraege"]: m["verlinkt_von"] = sorted(back[m["id"]] - set(m["links"]))
M["anzahl"] = len(M["eintraege"]); M["stand"] = "2026-11-02"
json.dump(M, open(mp, "w"), ensure_ascii=False, indent=1)
print(len(E), "neue Einträge,", M["anzahl"], "in der Masterliste")
