"""Batch 8: Fisch, Geflügel, Pasta, Reis, Frittiertes, Kaffee, Hitze und Geschmack. Schreibt nach content/entries/ im Repo."""
import json, sys, os
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/kochwissen-app/content/entries"

QM = {"titel": "Harold McGee: On Food and Cooking (2004)"}
QF = {"titel": "Fine Dining Lovers: The science of French fries", "url": "https://www.finedininglovers.com/explore/articles/science-french-fries"}
QT = {"titel": "ThermoWorks: How Meat Cooks – Heat’s Effects on Muscle Fibers", "url": "https://blog.thermoworks.com/coming-heat-effects-muscle-fibers-meat/"}

E = []
def add(**k):
    k.setdefault("status", "entwurf"); k.setdefault("schwierigkeit", "einsteiger"); k.setdefault("quellen", [QM]); E.append(k)
def welt(**k): add(typ="welt", visual={"vorlage": "keine", "illustration": k.pop("ill")}, **k)
def proz(**k): add(typ="prozess", **k)
def tech(**k): add(typ="technik", visual={"vorlage": "ablauf"}, **k)
def sym(w, **k): add(typ="symptom", welten=w, visual={"vorlage": "entscheidungsbaum"}, **k)
def zut(**k): add(typ="zutat", visual={"vorlage": "punktmatrix"}, **k)
def schraube(**k): add(typ="stellschraube", **k)

# ================= WELTEN =================
welt(id="w-fisch", titel="Fisch & Meeresfrüchte", synonyme=["Fisch", "Lachs", "Egli", "Felchen", "Crevetten"], ill="a whole trout on a wooden board with a lemon wedge",
     kurz="Fischfleisch ist zarter als Fleisch von Landtieren: kurze Muskelfasern, wenig Bindegewebe, Eiweiß, das schon bei niedrigen Temperaturen gart.",
     bild_im_kopf="Wie ein Buch aus dünnen Seiten, die nur lose zusammenkleben: Bei zu viel Hitze fällt es auseinander.",
     was_passiert="Fisch muss nicht gegen die Schwerkraft arbeiten, darum hat er wenig Bindegewebe. Das Eiweiß gart schon ab etwa 50 °C und wird bei zu viel Hitze schnell trocken und bröselig.",
     warum_wichtig="Fisch verzeiht wenig Übergaren. Sanfte Hitze und eine heiße, trockene Pfanne für die Haut sind die zwei Werkzeuge.",
     faustregeln=["Lieber zu früh als zu spät vom Herd.", "Haut trocken tupfen und auf der Hautseite braten.", "Säure ganz am Schluss."],
     links=["eiweiss-denaturierung", "fisch-klebt", "fisch-zerfaellt", "pochieren", "saeure-denaturierung"], quellen=[QM, QT])
welt(id="w-gefluegel", titel="Geflügel", synonyme=["Poulet", "Huhn", "Hähnchen", "Ente", "Truthahn"], ill="a roast chicken with crisp golden skin on a platter",
     kurz="Geflügel hat zwei Herausforderungen: magere Brust, die schnell austrocknet, und Haut, die knusprig werden soll.",
     bild_im_kopf="Zwei Gäste mit verschiedenen Wünschen am selben Tisch: Die Brust will sanft, die Keule will länger, die Haut will trocken und heiß.",
     was_passiert="Brustfleisch ist mager und wird über etwa 65 °C schnell trocken. Keulen haben mehr Bindegewebe und vertragen mehr Hitze. Die Haut wird erst knusprig, wenn ihr Wasser verdampft und das Fett ausgelassen ist.",
     warum_wichtig="Trockensalzen, unbedeckt antrocknen lassen und ein Thermometer lösen fast alle Geflügelprobleme.",
     faustregeln=["Über Nacht trocken salzen und unbedeckt kühlen.", "Thermometer in den dicksten Teil der Brust.", "Entenhaut kalt in der Pfanne ansetzen."],
     links=["trockensalzen", "knusprig", "fett-ausbraten", "kalt-ansetzen", "fleisch-trocken"])
welt(id="w-getreide", titel="Reis & Getreide", synonyme=["Reis", "Risotto", "Polenta", "Couscous", "Quinoa"], ill="a bowl of white rice with a wooden spoon",
     kurz="Getreide ist vor allem Stärke. Ob Reis locker oder cremig wird, hängt davon ab, wie viel Stärke sich löst.",
     bild_im_kopf="Wie Perlen in Kleister: Bleibt der Kleister an den Perlen, kleben sie, wird er gelöst, wird es cremig.",
     was_passiert="Beim Kochen quillt die Stärke im Korn. Stärke an der Oberfläche löst sich ins Wasser und macht klebrig oder cremig. Langkornreis hat Stärke, die eher locker bleibt, Risottoreis gibt viel Stärke ab.",
     warum_wichtig="Für lockeren Reis spült man Stärke ab, für Risotto rührt man sie bewusst heraus.",
     faustregeln=["Für lockeren Reis waschen, bis das Wasser klar ist.", "Nach dem Kochen zugedeckt ruhen lassen.", "Für Bratreis Reis vom Vortag."],
     links=["staerkeverkleisterung", "retrogradation", "reis-matschig", "cremig", "mantecare"])
welt(id="w-pasta", titel="Pasta", synonyme=["Nudeln", "Spaghetti", "Teigwaren", "frische Pasta"], ill="a nest of fresh tagliatelle dusted with flour",
     kurz="Pasta ist Glutennetz mit Stärke. Das Netz gibt Biss, die Stärke im Kochwasser hilft der Sauce zu haften.",
     bild_im_kopf="Wie ein Netz voller Kleister: außen gibt es Stärke ab, innen hält das Netz.",
     was_passiert="Beim Kochen quillt die Stärke, das Glutennetz hält die Form. Ein Teil der Stärke geht ins Wasser, das darum wertvoll für die Sauce ist.",
     warum_wichtig="Biss und eine gebundene Sauce entstehen in den letzten zwei Minuten: in der Pfanne mit Nudelwasser.",
     faustregeln=["Kochwasser salzen, aber nicht versalzen.", "Kurz vor al dente abgießen und in der Sauce fertig garen.", "Eine Tasse Nudelwasser aufheben."],
     links=["glutenbildung", "mantecare", "pasta-klebt", "staerkeverkleisterung"])
welt(id="w-frittieren", titel="Frittiertes", synonyme=["Frittieren", "Fritteuse", "Pommes", "Tempura", "Schnitzel"], ill="a paper cone of golden french fries",
     kurz="Frittieren ist Trocknen in heißem Öl: Das Wasser an der Oberfläche verdampft blitzschnell und hinterlässt eine knusprige Kruste.",
     bild_im_kopf="Wie ein Dampfkessel im Kleinformat: Solange es blubbert, drückt Dampf von innen gegen das Öl.",
     was_passiert="Heißes Öl überträgt Hitze schnell. Wasser an der Oberfläche verdampft, die Kruste trocknet und bräunt. Der austretende Dampf hält das Öl zunächst draußen. Ist das Öl zu kalt, bildet sich die Kruste langsam und das Frittiergut saugt Öl.",
     warum_wichtig="Temperatur, Portionsgröße und Abtropfen entscheiden zwischen knusprig und fettig.",
     faustregeln=["Thermometer: meist 160–190 °C.", "Kleine Portionen.", "Auf einem Gitter abtropfen."],
     links=["verdampfen", "zweimal-frittieren", "frittiertes-fettig", "rauchpunkt", "panieren", "knusprig"], quellen=[QF, QM])
welt(id="w-kaffee", titel="Kaffee & Tee", synonyme=["Kaffee", "Espresso", "Tee", "Rösten", "Brühen"], ill="a stovetop espresso pot and a small cup",
     kurz="Kaffee und Tee sind Extraktion: Heißes Wasser löst Aromen aus Bohnen oder Blättern. Röstung, Mahlgrad, Temperatur und Zeit bestimmen, was herauskommt.",
     bild_im_kopf="Wie Teebeutel und Geduld: Zu kurz schmeckt dünn, zu lange bitter.",
     was_passiert="Beim Rösten entstehen durch Maillard-Reaktion und Karamellisierung die Aromen. Beim Brühen lösen sich zuerst Säuren und Fruchtaromen, später Süße, zuletzt Bitterstoffe.",
     warum_wichtig="Saurer Kaffee ist meist zu kurz oder zu grob extrahiert, bitterer zu lange oder zu fein.",
     faustregeln=["Sauer: feiner mahlen oder länger brühen.", "Bitter: gröber mahlen oder kürzer brühen.", "Grüntee mit etwa 70–80 °C, nicht kochend (Richtwert)."],
     links=["maillard-reaktion", "karamellisierung", "diffusion"])

# ================= PROZESSE =================
proz(id="waermeleitung", titel="Wärmeleitung", synonyme=["Hitze wandert", "Hitze nach innen", "durchgaren"],
     kurz="Hitze wandert langsam von außen nach innen. Darum ist der Rand längst gar, wenn die Mitte noch kalt ist.",
     bild_im_kopf="Wie eine Nachricht, die in einer Menschenkette weitergeflüstert wird: Bis sie in der Mitte ankommt, dauert es.",
     was_passiert="In Lebensmitteln gibt jedes Teilchen die Wärme an seine Nachbarn weiter. Das geht langsam: Doppelt so dicke Stücke brauchen ungefähr viermal so lange, bis die Mitte warm ist. Je heißer außen, desto größer der Unterschied zwischen Rand und Mitte.",
     warum_wichtig="Erklärt graue Ränder bei Steaks, rohe Kerne bei dicken Braten und warum Rückwärtsgaren funktioniert.",
     faustregeln=["Dicke Stücke sanft garen, dünne scharf.", "Dicke halbieren heißt Garzeit ungefähr vierteln (Richtwert)."],
     stellschrauben=[{"id": "temperatur", "wirkung": "heißer außen → größerer Unterschied"}, {"id": "oberflaeche", "wirkung": "dünner → viel schneller"}, {"id": "pfannenmaterial", "wirkung": "Gusseisen speichert, Alu leitet schnell"}],
     links=["gleichmaessig-gar", "rueckwaerts-garen", "pfannenmaterial", "konvektion", "waermestrahlung"], welten=["w-fleisch"], visual={"vorlage": "zoom3-simulation"})
proz(id="konvektion", titel="Konvektion (Umluft, Kochen)", synonyme=["Umluft", "Heißluft", "strömende Hitze"],
     kurz="Bewegte Luft oder Flüssigkeit trägt Hitze viel schneller heran als stehende. Darum gart Umluft schneller und trocknet stärker.",
     bild_im_kopf="Wie Wind an einem kalten Tag: Bei gleicher Temperatur fühlt es sich viel kälter an, weil die Luft die Wärme wegträgt.",
     was_passiert="Ruhende Luft bildet um das Essen eine isolierende Schicht. Strömende Luft oder sprudelndes Wasser reißen sie weg. Umluft gart darum schneller und trocknet Oberflächen stärker.",
     warum_wichtig="Umluft ist ideal für Knusprigkeit und mehrere Bleche, aber weniger gut für Brot in der Dampfphase und empfindliche Kuchen.",
     faustregeln=["Bei Umluft etwa 20 °C weniger als bei Ober- und Unterhitze (Richtwert).", "Für Knusprigkeit Umluft, für Brot am Anfang ausschalten."],
     stellschrauben=[{"id": "temperatur", "wirkung": "bei Umluft niedriger einstellen"}, {"id": "luftfeuchte-ofen", "wirkung": "Umluft trocknet"}],
     links=["roesten-ofen", "dampf-im-ofen", "waermeleitung", "daempfen"], welten=["w-gebaeck", "w-kartoffeln"], visual={"vorlage": "zoom3-simulation"})
proz(id="waermestrahlung", titel="Wärmestrahlung (Grill, Oberhitze)", synonyme=["Grill", "Oberhitze", "Salamander", "Infrarot"],
     kurz="Glut und Heizspiralen strahlen Hitze direkt auf die Oberfläche, wie die Sonne. Das bräunt schnell, gart aber kaum nach innen.",
     bild_im_kopf="Wie Sonne auf der Haut: Die Oberfläche wird heiß, darunter bleibt es kühl.",
     was_passiert="Strahlung braucht keine Luft. Sie trifft die Oberfläche und heizt sie stark auf. Je näher an der Quelle, desto intensiver, im doppelten Abstand nur noch etwa ein Viertel.",
     warum_wichtig="Grill und Oberhitze sind ideal zum Gratinieren und für Kruste, aber dicke Stücke brauchen zusätzlich indirekte Hitze.",
     faustregeln=["Abstand zur Hitzequelle ist der Regler.", "Dicke Stücke: erst indirekt, dann direkt."],
     stellschrauben=[{"id": "temperatur", "wirkung": "näher → viel heißer"}],
     links=["grillen", "maillard-reaktion", "waermeleitung"], welten=["w-fleisch"], visual={"vorlage": "zoom3-simulation"})
proz(id="leidenfrost", titel="Leidenfrost-Effekt", synonyme=["tanzender Wassertropfen", "Wassertropfen-Test"],
     kurz="Auf einer sehr heißen Pfanne schwebt ein Wassertropfen auf seinem eigenen Dampfpolster und tanzt umher.",
     bild_im_kopf="Wie ein Airhockey-Puck auf einem Luftkissen.",
     was_passiert="Bei mittlerer Hitze verdampft ein Tropfen zischend. Ist die Pfanne deutlich heißer, verdampft die Unterseite so schnell, dass ein Dampfkissen entsteht, auf dem der Tropfen gleitet. Er lebt dann sogar länger.",
     warum_wichtig="Der einfachste Test, ob eine Edelstahlpfanne heiß genug für Fleisch oder Fisch ist.",
     faustregeln=["Tanzt der Tropfen als Kugel, ist die Pfanne bereit.", "Bei beschichteten Pfannen nicht leer überhitzen."],
     stellschrauben=[{"id": "temperatur", "wirkung": "erst ab hoher Hitze"}],
     links=["pfanne-vorheizen", "fisch-klebt", "steak-grau"], welten=["w-fleisch"], visual={"vorlage": "zoom3-simulation"})
proz(id="pyrolyse", titel="Verbrennen (Pyrolyse)", synonyme=["angebrannt", "verkohlt", "bitter", "schwarz"],
     kurz="Wird es zu heiß, zerfallen Zucker, Eiweiß und Fett zu bitteren, schwarzen Stoffen. Aus Röstaroma wird Brandgeschmack.",
     bild_im_kopf="Wie ein Toast, der einen Moment zu lang im Toaster war.",
     was_passiert="Nach der Maillard-Reaktion und der Karamellisierung kommt die Zersetzung: Die Moleküle brechen auseinander, es entstehen Kohlenstoff, Rauch und bittere Stoffe. Kleine, trockene, zuckerreiche Stücke wie Knoblauch, Nüsse oder Gewürze verbrennen am schnellsten.",
     warum_wichtig="Erklärt, warum Knoblauch spät in die Pfanne gehört und warum schwarzer Bratensatz nicht in die Sauce soll.",
     faustregeln=["Kleine Stücke spät und bei mittlerer Hitze.", "Riecht es scharf und beißend, ist es zu spät.", "Verbranntes wegschneiden, nicht wegwürzen."],
     stellschrauben=[{"id": "temperatur", "wirkung": "zu heiß → bitter"}, {"id": "zeit", "wirkung": "zu lange → bitter"}],
     links=["maillard-reaktion", "karamellisierung", "knoblauch-bitter", "zwiebeln-verbrennen"], welten=["w-fleisch", "w-gemuese"],
     visual={"vorlage": "temperaturskala", "params": {"hinweis": "Richtwerte", "skala": [{"c": 140, "name": "Bräunung beginnt"}, {"c": 170, "name": "kräftig gebräunt"}, {"c": 200, "name": "beginnt zu verbrennen"}]}})
proz(id="diffusion", titel="Diffusion: Geschmack wandert", synonyme=["durchziehen", "Marinade zieht ein", "einziehen"],
     kurz="Gelöste Stoffe wandern von selbst dorthin, wo weniger von ihnen ist. Aber nur langsam, wenige Millimeter in Stunden.",
     bild_im_kopf="Wie ein Tropfen Tinte in Wasser, der sich langsam ausbreitet, nur viel langsamer, weil Fleisch kein Wasser ist.",
     was_passiert="Salz, Zucker und Aromen bewegen sich von der Oberfläche ins Innere. Kleine Moleküle wie Salz schaffen das in Stunden bis Tagen, große Aromen und Öl dringen kaum ein. Darum würzen Marinaden vor allem die Oberfläche.",
     warum_wichtig="Erklärt, warum Salz einzieht, Marinadenaromen aber außen bleiben, und warum Schmorgerichte am nächsten Tag besser schmecken.",
     faustregeln=["Salz braucht Zeit, Aromen bleiben außen.", "Dünnere Stücke ziehen schneller durch.", "Eintopf vom Vortag: Die Aromen hatten Zeit, sich zu verteilen."],
     stellschrauben=[{"id": "zeit", "wirkung": "länger → tiefer"}, {"id": "salzgehalt", "wirkung": "mehr → schneller"}, {"id": "oberflaeche", "wirkung": "dünner → schneller durch"}],
     links=["marinieren", "trockensalzen", "osmose"], welten=["w-fleisch", "w-kaffee"], visual={"vorlage": "zoom3-simulation"})
proz(id="fett-ausbraten", titel="Fett ausbraten (Auslassen)", synonyme=["Fett auslassen", "Speck auslassen", "Entenhaut knusprig", "rendern"],
     kurz="Bei sanfter Hitze schmilzt Fett aus Haut und Speck heraus. Zurück bleibt eine dünne Schicht, die knusprig wird.",
     bild_im_kopf="Wie Kerzenwachs, das langsam schmilzt und den Docht freilegt.",
     was_passiert="Fett sitzt in Zellen eingeschlossen. Bei langsamer Hitze schmelzen sie und das Fett läuft aus. Ist die Hitze zu stark, schließt sich die Oberfläche zu früh, und unter einer dunklen Kruste bleibt eine dicke, weiche Fettschicht.",
     warum_wichtig="Entenbrust, Speck, Schweinebauch und Pouletkeulen brauchen zuerst Geduld und erst am Ende starke Hitze.",
     faustregeln=["Kalt in die Pfanne legen, dann langsam erhitzen.", "Haut vorher einschneiden, ohne ins Fleisch zu schneiden.", "Ausgelassenes Fett aufheben: ideal für Bratkartoffeln."],
     stellschrauben=[{"id": "temperatur", "wirkung": "sanft → mehr Fett läuft aus"}, {"id": "zeit", "wirkung": "länger → dünnere, knusprigere Haut"}],
     links=["kalt-ansetzen", "knusprig", "w-gefluegel"], welten=["w-fleisch", "w-gefluegel"], visual={"vorlage": "zoom3-simulation"})
proz(id="oxidation-fett", titel="Fett wird ranzig (Oxidation)", synonyme=["ranzig", "alt riechendes Öl", "Nüsse ranzig"],
     kurz="Sauerstoff, Licht und Wärme zerlegen Fette mit der Zeit in unangenehm riechende Stoffe.",
     bild_im_kopf="Wie Rost an Metall, nur bei Fett.",
     was_passiert="Ungesättigte Fette, wie sie in Nüssen, Vollkornmehl und vielen Ölen stecken, reagieren langsam mit Sauerstoff. Licht und Wärme beschleunigen das. Es entstehen Stoffe, die nach Farbe oder Karton riechen.",
     warum_wichtig="Erklärt, warum Nüsse, Vollkornmehl und Leinöl kühl und dunkel gelagert werden sollten.",
     faustregeln=["Öle dunkel und kühl lagern.", "Nüsse und Vollkornmehl in Maßen kaufen oder einfrieren.", "Riechen statt nach Datum gehen."],
     stellschrauben=[{"id": "temperatur", "wirkung": "kühler → langsamer"}, {"id": "zeit", "wirkung": "länger → ranziger"}],
     links=["oel", "fett"], welten=["w-milch"], visual={"vorlage": "zoom3-simulation"})
proz(id="saeure-denaturierung", titel="Säure gart Eiweiß", schwierigkeit="fortgeschritten", synonyme=["Ceviche", "Fisch in Limette", "Säure gart"],
     kurz="Starke Säure verändert Eiweiß ähnlich wie Hitze: Roher Fisch in Limettensaft wird fest und undurchsichtig.",
     bild_im_kopf="Wie Hitze ohne Feuer.",
     was_passiert="Säure entfaltet die Eiweißketten, sie verbinden sich neu und werden fest und weiß. Anders als Hitze tötet Säure aber nicht alle Keime ab, darum braucht Ceviche sehr frischen Fisch.",
     warum_wichtig="Erklärt Ceviche und warum zu lange Säure-Marinaden Fleisch und Fisch mehlig machen.",
     faustregeln=["Ceviche nur mit sehr frischem Fisch.", "Fisch nicht stundenlang in Säure marinieren, sonst wird er mehlig."],
     stellschrauben=[{"id": "ph-wert", "wirkung": "saurer → schneller fest"}, {"id": "zeit", "wirkung": "zu lange → mehlig"}],
     links=["eiweiss-denaturierung", "saeure", "marinieren"], welten=["w-fisch"], visual={"vorlage": "zoom3-simulation"})
proz(id="aroma-blooming", titel="Gewürze entfalten sich in Fett", synonyme=["Blooming", "Gewürze anschwitzen", "Tadka", "Tempering Spices"],
     kurz="Viele Aromen lösen sich besser in Fett als in Wasser. Gewürze kurz in heißem Fett anzuschwitzen, macht sie viel intensiver.",
     bild_im_kopf="Wie einen Schlüssel ins richtige Schloss stecken: Fett öffnet die Aromen.",
     was_passiert="Die Duftstoffe in Gewürzen sind oft fettlöslich. In heißem Öl lösen sie sich, verteilen sich im ganzen Gericht und rösten leicht an. In Wasser bleiben sie stumpfer.",
     warum_wichtig="Erklärt, warum Curry mit angeschwitzten Gewürzen anders schmeckt als mit eingerührtem Pulver.",
     faustregeln=["Ganze Gewürze zuerst, gemahlene kurz danach.", "Nur Sekunden bis eine Minute, bis es duftet.", "Bei Rauch ist es zu spät."],
     stellschrauben=[{"id": "temperatur", "wirkung": "zu heiß → bitter"}, {"id": "fettgehalt", "wirkung": "Fett trägt die Aromen"}],
     links=["gewuerze-roesten", "gewuerze", "pyrolyse"], welten=["w-saucen"], visual={"vorlage": "zoom3-simulation"})

# ================= STELLSCHRAUBEN =================
schraube(id="pfannenmaterial", titel="Pfanne & Wärmespeicher", synonyme=["Gusseisen", "Edelstahl", "beschichtete Pfanne", "Eisenpfanne"],
         kurz="Schwere Pfannen speichern viel Hitze und kühlen beim Einlegen kaum ab. Leichte reagieren schnell, verlieren aber schnell Hitze.",
         bild_im_kopf="Wie ein großer gegen einen kleinen Akku.",
         was_passiert="Gusseisen und dicke Eisenpfannen speichern viel Wärme und sind ideal zum scharfen Anbraten. Edelstahl mit Sandwichboden verteilt Hitze gleichmäßig. Beschichtete Pfannen verzeihen klebrige Speisen, vertragen aber keine sehr hohe Hitze.",
         faustregeln=["Scharf anbraten: Gusseisen oder Eisen.", "Eier und Fisch: beschichtet oder gut vorgeheizter Edelstahl.", "Saucen mit Säure: Edelstahl."],
         links=["steak-grau", "waermeleitung", "pfanne-vorheizen"],
         visual={"vorlage": "skala", "params": {"links": "dünn und leicht: reagiert schnell, kühlt stark ab", "rechts": "schwer, Gusseisen: speichert Hitze, ideal zum Anbraten"}})
schraube(id="salzgehalt", titel="Salzmenge", synonyme=["salzen", "Salz", "weniger Salz"],
         kurz="Salz verstärkt Geschmack, zieht Wasser, hält Wasser im Fleisch und strafft Teig. Die richtige Menge hängt vom Zeitpunkt ab.",
         bild_im_kopf="Ein Regler mit schmalem Sweetspot: zu wenig fad, zu viel ungenießbar.",
         was_passiert="Wenig Salz hebt Aromen und dämpft Bitterkeit. Mehr Salz zieht Wasser und würzt durch. Zu viel überdeckt alles. Eingekochte Saucen werden mit der Zeit salziger.",
         faustregeln=["Früh wenig, am Schluss abschmecken.", "Nudelwasser deutlich salzen, Saucen erst am Ende."],
         links=["salz", "osmose", "wasserbindung-salz", "essen-versalzen", "essen-flach"],
         visual={"vorlage": "skala", "params": {"links": "zu wenig: fad", "mitte": "richtig: Aromen leuchten", "rechts": "zu viel: salzig, überdeckt alles"}})
schraube(id="zeit", titel="Zeit", synonyme=["Garzeit", "Dauer", "lange garen", "Geduld"],
         kurz="Zeit verändert alles: Bindegewebe löst sich, Teig entwickelt Geschmack, Salz zieht ein, Eiweiß wird fester.",
         bild_im_kopf="Die unsichtbare Zutat, die in jedem Rezept steht.",
         was_passiert="Manche Vorgänge brauchen Zeit statt Hitze: Bindegewebe, Gärung, Salzen, Aromen verteilen. Bei anderen ist Zeit der Feind: Eiweiß wird trocken, Grün wird grau, Schaum fällt zusammen.",
         faustregeln=["Zähes Fleisch, Brotteig, Marinaden: mehr Zeit.", "Fisch, grünes Gemüse, Eier: weniger Zeit."],
         links=["kollagen-gelatine", "hefegaerung", "trockensalzen", "chlorophyll-farbe"],
         visual={"vorlage": "skala", "params": {"links": "kurz: knackig, saftig, frisch", "rechts": "lang: zart, durchgezogen, entwickelt"}})

# ================= ZIEL =================
add(id="mehr-geschmack", typ="ziel", titel="Mehr Geschmack", synonyme=["würziger", "intensiver", "Umami", "schmeckt nach mehr", "Tiefe"],
    kurz="Mehr Geschmack entsteht durch Röstaromen, Konzentration, Säure und Salz im richtigen Verhältnis, nicht durch mehr Gewürz.",
    bild_im_kopf="Wie ein Mischpult: Salz, Säure, Süße, Bitterkeit und Umami müssen zueinander passen.",
    bedeutung="Geschmack hat mehrere Ebenen: Röstaromen aus der Maillard-Reaktion, Konzentration durch Einkochen, Würze aus Salz, Frische aus Säure und Tiefe aus Umami (Käse, Tomate, Fond, Pilze).",
    hebel=["maillard-reaktion", "reduktion", "salzgehalt", "ph-wert", "zeit"],
    was_passiert="Ein flaches Gericht braucht oft eher Säure als Salz. Röstaromen entstehen beim Anbraten, nicht beim Kochen. Einkochen konzentriert alles.",
    faustregeln=["Kräftig anbraten und den Bratensatz lösen.", "Zum Schluss mit Säure und Salz abschmecken.", "Gewürze in Fett anschwitzen."],
    links=["anbraten", "deglacieren", "reduzieren", "abschmecken-saeure", "gewuerze-roesten", "essen-flach"],
    welten=["w-saucen", "w-fleisch"], visual={"vorlage": "punktmatrix"})

# ================= TECHNIKEN =================
tech(id="abschmecken-saeure", titel="Mit Säure abschmecken", synonyme=["Zitrone zum Schluss", "Spritzer Essig", "abschmecken"],
     kurz="Ein paar Tropfen Zitrone oder Essig ganz am Schluss lassen ein Gericht frischer und kräftiger schmecken.",
     bild_im_kopf="Wie das Licht einschalten in einem dunklen Raum.",
     was_passiert="Säure gleicht Fett, Süße und Schwere aus. Sie macht andere Aromen deutlicher wahrnehmbar, ähnlich wie Salz. Am Ende zugegeben bleibt sie frisch.",
     schritte=["Gericht probieren.", "Wenige Tropfen Zitrone, Essig oder Wein dazugeben.", "Umrühren, erneut probieren.", "Erst danach entscheiden, ob noch Salz fehlt."],
     wirkt_auf=["mehr-geschmack"], links=["saeure", "essen-flach", "mehr-geschmack"], welten=["w-saucen"])
tech(id="gewuerze-roesten", titel="Gewürze rösten", synonyme=["Gewürze anrösten", "trocken rösten", "Kreuzkümmel rösten"],
     kurz="Ganze Gewürze kurz in einer trockenen Pfanne rösten. Sie duften stärker und schmecken tiefer.",
     bild_im_kopf="Wie Kaffeebohnen rösten im Kleinformat.",
     was_passiert="Hitze setzt flüchtige Duftstoffe frei und erzeugt neue Röstaromen. Weil Gewürze klein und trocken sind, verbrennen sie schnell.",
     schritte=["Ganze Gewürze in eine trockene Pfanne geben.", "Bei mittlerer Hitze schwenken, 1–3 Minuten.", "Sobald es duftet, sofort herausnehmen.", "Abkühlen lassen und mahlen."],
     wirkt_auf=["mehr-geschmack"], links=["aroma-blooming", "maillard-reaktion", "pyrolyse", "gewuerze"], welten=["w-saucen"])
tech(id="grillen", titel="Grillen", synonyme=["Barbecue", "BBQ", "direkt grillen", "indirekt grillen"],
     kurz="Starke Strahlungshitze von unten gibt Kruste und Rauchgeschmack. Mit einer heißen und einer kühlen Zone gelingen auch dicke Stücke.",
     bild_im_kopf="Wie Sonne und Schatten auf dem Rost.",
     was_passiert="Über der Glut ist die Hitze sehr stark und bräunt schnell. Daneben ist es sanfter, dort gart das Innere ohne zu verbrennen. Tropfendes Fett verbrennt in der Glut und erzeugt Rauch.",
     schritte=["Glut auf eine Seite schieben: heiße und kühle Zone.", "Rost gut vorheizen und reinigen.", "Dünne Stücke direkt grillen.", "Dicke Stücke erst indirekt auf Temperatur, dann direkt bräunen.", "Mit Thermometer prüfen."],
     wirkt_auf=["mehr-geschmack", "farbe"], links=["waermestrahlung", "maillard-reaktion", "rueckwaerts-garen"], welten=["w-fleisch", "w-gemuese"])
tech(id="kalt-ansetzen", titel="Kalt ansetzen (Entenhaut, Speck)", synonyme=["kalte Pfanne", "Ente braten", "Speck braten"],
     kurz="Fettes Fleisch mit der Haut nach unten in die kalte Pfanne legen und langsam erhitzen. Das Fett läuft aus, die Haut wird dünn und knusprig.",
     bild_im_kopf="Wie Schnee, der langsam schmilzt, statt schlagartig zu verdampfen.",
     was_passiert="Die langsam steigende Hitze schmilzt das Fett unter der Haut, bevor sich außen eine Kruste bildet. Erst am Ende wird die Hitze erhöht.",
     schritte=["Haut rautenförmig einschneiden, ohne ins Fleisch zu schneiden.", "Salzen und mit der Haut nach unten in die kalte Pfanne legen.",
              "Bei mittlerer bis kleiner Hitze 10–15 Minuten Fett auslassen.", "Fett zwischendurch abgießen.", "Am Ende Hitze erhöhen, bis die Haut knusprig ist, dann kurz auf der Fleischseite garen."],
     wirkt_auf=["knusprig"], links=["fett-ausbraten", "knusprig", "w-gefluegel"], welten=["w-gefluegel", "w-fleisch"])
tech(id="marinieren", titel="Marinieren", synonyme=["Marinade", "einlegen", "Joghurtmarinade"],
     kurz="Eine Marinade würzt vor allem die Oberfläche. Salz darin zieht tiefer ein, Säure und Öl bleiben außen.",
     bild_im_kopf="Wie Farbe auf Holz: Sie bleibt an der Oberfläche, nur Salz zieht wie eine Beize tiefer.",
     was_passiert="Aromen und Öl dringen kaum ein. Salz wandert langsam ins Innere und macht saftiger. Säure verändert die Oberfläche und kann sie bei zu langer Zeit mehlig machen. Joghurt ist mild und eignet sich gut für längere Marinaden.",
     schritte=["Marinade mit Salz, Aromen, etwas Öl und wenig Säure anrühren.", "Fleisch darin wenden, gekühlt ziehen lassen.",
              "Säurebetonte Marinaden nur wenige Stunden.", "Vor dem Braten abstreifen und trocken tupfen."],
     wirkt_auf=["mehr-geschmack", "saftig"], typische_fehler=["Nass aus der Marinade in die Pfanne: kocht statt brät."],
     links=["diffusion", "saeure", "joghurt", "trocken-tupfen", "steak-grau"], welten=["w-fleisch"])
tech(id="panieren", titel="Panieren", synonyme=["Panade", "Schnitzel panieren", "Mehl Ei Paniermehl"],
     kurz="Mehl, Ei, Paniermehl: drei Schichten, die eine knusprige Hülle bilden und das Fleisch schützen.",
     bild_im_kopf="Wie Grundierung, Kleber und Belag.",
     was_passiert="Mehl trocknet die Oberfläche und gibt dem Ei Halt. Ei ist der Kleber. Paniermehl bildet die Kruste, die im heißen Fett trocknet und bräunt. Für eine leicht abstehende Panade wird das Schnitzel im Fett geschwenkt.",
     schritte=["Fleisch trocken tupfen und würzen.", "In Mehl wenden, überschüssiges abklopfen.", "Durch verquirltes Ei ziehen, abtropfen lassen.",
              "In Paniermehl wenden, nicht andrücken.", "In reichlich heißem Fett (etwa 170 °C, Richtwert) ausbacken und die Pfanne schwenken."],
     wirkt_auf=["knusprig"], links=["panade-faellt-ab", "knusprig", "w-frittieren"], welten=["w-fleisch", "w-fisch", "w-frittieren"])
tech(id="sous-vide", titel="Sous-vide", schwierigkeit="fortgeschritten", synonyme=["Vakuumgaren", "Niedertemperatur im Wasserbad"],
     kurz="Vakuumiertes Fleisch oder Fisch im Wasserbad genau auf Zieltemperatur garen. Von Rand zu Rand gleich, dann kurz anbraten.",
     bild_im_kopf="Wie ein Thermostat statt eines Lagerfeuers.",
     was_passiert="Das Wasser ist genau so warm wie die gewünschte Kerntemperatur. Das Essen kann darum nicht übergaren, nur länger werden. Danach braucht es eine sehr heiße Pfanne für die Kruste.",
     schritte=["Fleisch würzen und vakuumieren.", "Wasserbad auf Zieltemperatur bringen, z. B. 55 °C für rosa Rind (Richtwert).",
              "Je nach Dicke 1–3 Stunden garen.", "Herausnehmen, trocken tupfen.", "In sehr heißer Pfanne 1 Minute pro Seite anbraten."],
     wirkt_auf=["gleichmaessig-gar", "saftig"], links=["gleichmaessig-gar", "eiweiss-denaturierung", "anbraten", "kerntemperatur"], welten=["w-fleisch", "w-fisch"])

# ================= SYMPTOME =================
sym([], id="essen-flach", titel="Essen schmeckt flach", synonyme=["fad", "langweilig", "es fehlt etwas", "schmeckt nach nichts"],
    kurz="Meist fehlt Säure, manchmal Salz, manchmal Röstaroma. Selten fehlen Gewürze.",
    bild_im_kopf="Wie ein Foto ohne Kontrast.",
    ursachen=[{"titel": "Säure fehlt", "haeufigkeit": 3, "prinzip": "mehr-geschmack", "warum": "Ohne Säure wirken Gerichte schwer und dumpf.", "fix": ["Ein paar Tropfen Zitrone oder Essig", "Ein Schluck Wein beim Kochen"]},
              {"titel": "Salz fehlt", "haeufigkeit": 2, "prinzip": "mehr-geschmack", "warum": "Salz hebt alle anderen Aromen hervor.", "fix": ["Prisenweise nachsalzen und probieren"]},
              {"titel": "Keine Röstaromen", "haeufigkeit": 2, "prinzip": "maillard-reaktion", "warum": "Nur gekocht statt angebraten fehlt die Tiefe.", "fix": ["Zutaten erst kräftig anbraten", "Bratensatz ablöschen"]}],
    diagnose={"q1": {"frage": "Wird es besser, wenn du einen Löffel davon mit einem Tropfen Zitrone probierst?", "antworten": [["Ja", "u0"], ["Nein", "q2"]]},
              "q2": {"frage": "Und mit einer Prise Salz?", "antworten": [["Ja", "u1"], ["Nein", "u2"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["abschmecken-saeure", "mehr-geschmack", "salzgehalt", "anbraten"])
sym([], id="essen-versalzen", titel="Essen ist versalzen", synonyme=["zu salzig", "versalzen retten"],
    kurz="Zu viel Salz lässt sich kaum herausholen, nur verdünnen oder ausgleichen.",
    bild_im_kopf="Wie zu laute Musik: Leiser drehen geht nicht, man kann nur mehr Raum schaffen.",
    ursachen=[{"titel": "Früh gesalzen, dann eingekocht", "haeufigkeit": 3, "prinzip": "reduktion", "warum": "Beim Einkochen bleibt das Salz, das Wasser geht.", "fix": ["Mit ungesalzener Flüssigkeit verdünnen", "Nächstes Mal erst am Schluss salzen"]},
              {"titel": "Zu viel auf einmal", "haeufigkeit": 2, "prinzip": "salzgehalt", "warum": "Salz löst sich und verteilt sich erst mit der Zeit.", "fix": ["Mehr von den ungesalzenen Zutaten dazugeben", "Säure, Süße oder Sahne dämpfen den Eindruck etwas"]}],
    diagnose={"q1": {"frage": "Wurde die Sauce oder Suppe nach dem Salzen lange eingekocht?", "antworten": [["Ja", "u0"], ["Nein", "u1"]]}, "u0": {"ursache": 0}, "u1": {"ursache": 1}},
    links=["salz", "salzgehalt", "reduktion"])
sym(["w-fisch"], id="fisch-klebt", titel="Fisch klebt an der Pfanne", synonyme=["Fischhaut klebt", "Fisch reißt beim Wenden"],
    kurz="Die Pfanne war nicht heiß genug oder der Fisch wurde zu früh bewegt. Eiweiß verbindet sich mit dem Metall.",
    bild_im_kopf="Wie ein Pflaster, das man zu früh abreißt.",
    ursachen=[{"titel": "Pfanne zu kalt", "haeufigkeit": 3, "prinzip": "leidenfrost", "warum": "In lauwarmer Pfanne verbindet sich Eiweiß mit dem Metall, bevor sich eine Kruste bildet.", "fix": ["Pfanne richtig vorheizen", "Wassertropfen-Test"]},
              {"titel": "Zu früh gewendet", "haeufigkeit": 2, "prinzip": "maillard-reaktion", "warum": "Ist die Kruste fertig, löst sich der Fisch von selbst.", "fix": ["Liegen lassen, bis er sich löst"]},
              {"titel": "Haut nass", "haeufigkeit": 2, "prinzip": "verdampfen", "warum": "Wasser verhindert die Kruste.", "fix": ["Haut gründlich trocken tupfen", "Mit einem Messerrücken abstreifen"]}],
    diagnose={"q1": {"frage": "Hat es beim Einlegen deutlich gezischt?", "antworten": [["Nein", "u0"], ["Ja", "q2"]]},
              "q2": {"frage": "Hast du in den ersten Minuten versucht zu wenden?", "antworten": [["Ja", "u1"], ["Nein", "u2"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["leidenfrost", "pfanne-vorheizen", "trocken-tupfen"])
sym(["w-fisch"], id="fisch-zerfaellt", titel="Fisch zerfällt", synonyme=["Fisch bröselig", "Fisch trocken", "Fisch fällt auseinander"],
    kurz="Zu viel Hitze: Das wenige Bindegewebe hat sich gelöst, und die Fasern sind ausgetrocknet.",
    bild_im_kopf="Wie ein Buch, dessen Bindung sich gelöst hat.",
    ursachen=[{"titel": "Übergart", "haeufigkeit": 3, "prinzip": "eiweiss-denaturierung", "warum": "Fisch ist schon bei niedrigen Temperaturen gar.", "fix": ["Früher vom Herd nehmen", "Glasiger Kern ist oft perfekt"]},
              {"titel": "Sprudelnd gekocht", "haeufigkeit": 2, "prinzip": "pochieren-proz", "warum": "Bewegtes Wasser reißt die zarten Lamellen auseinander.", "fix": ["Nur garziehen lassen, nicht kochen"]},
              {"titel": "Zu oft gewendet", "haeufigkeit": 1, "prinzip": "eiweiss-denaturierung", "warum": "Gegarter Fisch bricht leicht.", "fix": ["Nur einmal wenden, mit breitem Fischwender"]}],
    diagnose={"q1": {"frage": "War der Fisch gebraten oder in Flüssigkeit gegart?", "antworten": [["Gebraten", "q2"], ["In Flüssigkeit", "u1"]]},
              "q2": {"frage": "Hast du ihn mehrmals gewendet?", "antworten": [["Ja", "u2"], ["Nein", "u0"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["eiweiss-denaturierung", "pochieren", "w-fisch"])
sym(["w-fleisch", "w-fisch"], id="panade-faellt-ab", titel="Panade fällt ab", synonyme=["Panade löst sich", "Schnitzel Panade ab"],
    kurz="Feuchtigkeit oder zu wenig Haftung zwischen den Schichten. Manchmal auch zu wenig Fett.",
    bild_im_kopf="Wie Tapete auf einer feuchten Wand.",
    ursachen=[{"titel": "Fleisch nass", "haeufigkeit": 3, "prinzip": "verdampfen", "warum": "Dampf zwischen Fleisch und Panade drückt sie ab.", "fix": ["Trocken tupfen", "Mehl dünn auftragen und abklopfen"]},
              {"titel": "Zu wenig Fett, zu kühl", "haeufigkeit": 2, "prinzip": "verdampfen", "warum": "Die Panade wird nicht schnell genug fest und saugt sich voll.", "fix": ["Reichlich Fett, gut erhitzt", "Schnitzel schwimmen lassen"]},
              {"titel": "Zu oft gewendet oder angestochen", "haeufigkeit": 1, "prinzip": "verdampfen", "warum": "Die Kruste reißt, bevor sie fest ist.", "fix": ["Mit Zange oder Wender, einmal wenden"]}],
    diagnose={"q1": {"frage": "Hast du das Fleisch vor dem Mehl trocken getupft?", "antworten": [["Nein", "u0"], ["Ja", "q2"]]},
              "q2": {"frage": "Schwamm das Schnitzel im Fett?", "antworten": [["Nein, wenig Fett", "u1"], ["Ja", "u2"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["panieren", "trocken-tupfen", "frittiertes-fettig"])
sym(["w-pasta"], id="pasta-klebt", titel="Pasta klebt zusammen", synonyme=["Nudeln kleben", "Spaghetti verklebt"],
    kurz="Die Stärke an der Oberfläche hat die Nudeln verklebt, meist in den ersten Minuten oder nach dem Abgießen.",
    bild_im_kopf="Wie Briefmarken, die feucht aufeinanderliegen.",
    ursachen=[{"titel": "Am Anfang nicht umgerührt", "haeufigkeit": 3, "prinzip": "staerkeverkleisterung", "warum": "In den ersten Minuten ist die Oberfläche am klebrigsten.", "fix": ["In den ersten zwei Minuten mehrmals umrühren"]},
              {"titel": "Nach dem Abgießen stehen gelassen", "haeufigkeit": 2, "prinzip": "staerkeverkleisterung", "warum": "Abkühlende Stärke klebt.", "fix": ["Sofort mit Sauce mischen", "Etwas Nudelwasser dazugeben"]},
              {"titel": "Wasser nicht sprudelnd", "haeufigkeit": 1, "prinzip": "staerkeverkleisterung", "warum": "Ohne Bewegung liegen die Nudeln aneinander.", "fix": ["Wasser kräftig kochen lassen, bevor die Pasta hineinkommt"]}],
    diagnose={"q1": {"frage": "Klebten die Nudeln schon im Topf?", "antworten": [["Ja", "q2"], ["Nein, erst danach", "u1"]]},
              "q2": {"frage": "Kochte das Wasser sprudelnd, als die Pasta hineinkam?", "antworten": [["Nein", "u2"], ["Ja", "u0"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["staerkeverkleisterung", "mantecare", "w-pasta"])
sym(["w-getreide"], id="reis-matschig", titel="Reis wird matschig", synonyme=["Reis klebrig", "Reis breiig", "Reis pappig"],
    kurz="Zu viel Wasser oder zu viel lose Stärke, manchmal auch zu viel Rühren.",
    bild_im_kopf="Wie Perlen, die in zu viel Kleister schwimmen.",
    ursachen=[{"titel": "Zu viel Wasser", "haeufigkeit": 3, "prinzip": "staerkeverkleisterung", "warum": "Das Korn quillt über und platzt auf.", "fix": ["Wasser abmessen, z. B. etwa 1,5 Teile Wasser auf 1 Teil Langkornreis (Richtwert)"]},
              {"titel": "Nicht gewaschen", "haeufigkeit": 2, "prinzip": "staerkeverkleisterung", "warum": "Lose Stärke an der Oberfläche macht klebrig.", "fix": ["Reis waschen, bis das Wasser klar ist"]},
              {"titel": "Umgerührt", "haeufigkeit": 1, "prinzip": "staerkeverkleisterung", "warum": "Rühren löst Stärke, wie beim Risotto.", "fix": ["Zugedeckt nicht rühren", "Nach dem Kochen ruhen lassen, dann auflockern"]}],
    diagnose={"q1": {"frage": "Hast du das Wasser abgemessen?", "antworten": [["Nein", "u0"], ["Ja", "q2"]]},
              "q2": {"frage": "Hast du den Reis vorher gewaschen?", "antworten": [["Nein", "u1"], ["Ja", "u2"]]},
              "u0": {"ursache": 0}, "u1": {"ursache": 1}, "u2": {"ursache": 2}},
    links=["staerkeverkleisterung", "w-getreide", "retrogradation"])

# ================= ZUTATEN =================
zut(id="gewuerze", titel="Gewürze", synonyme=["Pfeffer", "Kreuzkümmel", "Paprika", "Curry", "Zimt"],
    kurz="Gewürze sind konzentrierte Duftstoffe. Viele lösen sich in Fett, verflüchtigen sich in Hitze und verbrennen schnell.",
    bild_im_kopf="Wie Parfumflakons: offen verfliegen sie, richtig erwärmt entfalten sie sich.",
    rolle=[{"rolle": "entfalten sich in Fett", "prozess": "aroma-blooming"}, {"rolle": "rösten und werden tiefer", "prozess": "maillard-reaktion"}, {"rolle": "verbrennen schnell", "prozess": "pyrolyse"}],
    was_passiert="Gemahlene Gewürze verlieren ihr Aroma schneller als ganze, weil ihre Oberfläche größer ist. Hitze setzt Aromen frei, zu viel Hitze zerstört sie.",
    faustregeln=["Ganze Gewürze kaufen und frisch mahlen.", "Kühl, dunkel, luftdicht lagern."],
    links=["aroma-blooming", "gewuerze-roesten", "pyrolyse"], welten=["w-saucen"])
zut(id="wasser", titel="Wasser", synonyme=["Leitungswasser", "Kochwasser", "Dampf"],
    kurz="Wasser ist in fast jedem Lebensmittel die Hauptzutat. Es begrenzt die Temperatur auf 100 °C, löst Stoffe und lässt Stärke quellen.",
    bild_im_kopf="Der stille Hauptdarsteller: Wo Wasser ist, wird es nicht heißer als 100 °C.",
    rolle=[{"rolle": "begrenzt die Temperatur auf 100 °C", "prozess": "verdampfen"}, {"rolle": "lässt Stärke quellen", "prozess": "staerkeverkleisterung"}, {"rolle": "bildet mit Mehl das Glutennetz", "prozess": "glutenbildung"}],
    was_passiert="Solange Wasser da ist, bleibt die Temperatur beim Siedepunkt. Erst wenn es weg ist, kann es bräunen. Es löst Salz, Zucker und Aromen und lässt Stärke und Gluten entstehen.",
    faustregeln=["Für Kruste: Wasser weg. Für Zartheit: Wasser behalten.", "In der Höhe kocht Wasser bei weniger als 100 °C, Garzeiten werden länger."],
    links=["verdampfen", "staerkeverkleisterung", "glutenbildung", "hydration"], welten=["w-brot"])
zut(id="wein", titel="Wein", synonyme=["Weißwein", "Rotwein", "Kochwein"],
    kurz="Wein bringt Säure, Aromen und etwas Süße in Saucen und Schmorgerichte. Der Alkohol löst Aromen und verdampft größtenteils.",
    bild_im_kopf="Wie ein Gewürz in flüssiger Form.",
    rolle=[{"rolle": "löst den Bratensatz", "prozess": "deglacieren"}, {"rolle": "gibt Säure", "prozess": "mehr-geschmack"}, {"rolle": "wird beim Einkochen konzentriert", "prozess": "reduktion"}],
    was_passiert="Die Säure im Wein macht Saucen lebendig. Beim Einkochen konzentrieren sich Säure, Aromen und Gerbstoffe. Ein Teil des Alkohols bleibt auch nach längerem Kochen erhalten.",
    faustregeln=["Nur Wein verwenden, den man auch trinken würde.", "Rotwein gut einkochen, sonst schmeckt er roh und herb."],
    links=["deglacieren", "reduktion", "saeure"], welten=["w-saucen"])

os.makedirs(OUT, exist_ok=True)
for e in E:
    json.dump(e, open(os.path.join(OUT, e["id"] + ".json"), "w"), ensure_ascii=False, indent=2)
print(len(E), "Einträge geschrieben")
