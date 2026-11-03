"""Batch «Fermentation & Geschmack»: Garum (der Name der Seite), Koji, Edelschimmel, Proteolyse, Bitter, Süß,
Zusammenspiel der Geschmäcker, Geschmack und Nase, Flavor Pairing, Xanthan und zwei Experimente.
Deutsch und Englisch als Paare L(deutsch, englisch), wie in gen_batch_welten2.py."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_batch_welten2 import L, res, MC, ROOT  # noqa: E402

E = []
add = E.append

NOMA = {"titel": "René Redzepi, David Zilber: The Noma Guide to Fermentation (2018)", "stelle": L("Kapitel Koji und Garums", "Chapters on koji and garums")}
BRESLIN = {"titel": "Breslin, Beauchamp: Salt enhances flavour by suppressing bitterness. Nature 387 (1997)", "url": "https://www.nature.com/articles/42388"}
TALAVERA = {"titel": "Talavera et al.: Heat activation of TRPM5 underlies thermal sensitivity of sweet taste. Nature 438 (2005)", "url": "https://www.nature.com/articles/nature04248"}
AHN = {"titel": "Ahn et al.: Flavor network and the principles of food pairing. Scientific Reports 1 (2011)", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3240947"}


def P(id, titel, syn, kurz, bild, was, warum, regeln, stell, praxis, links, welten, illu, quellen, schw="einsteiger"):
    e = {"id": id, "typ": "prozess", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild, "was_passiert": was,
         "warum_wichtig": warum, "faustregeln": regeln, "stellschrauben": [{"id": a, "wirkung": b} for a, b in stell],
         "praxis": [{"welt": a, "text": b} for a, b in praxis], "links": links, "welten": welten,
         "quellen": quellen, "status": "entwurf", "schwierigkeit": schw, "visual": {"vorlage": "keine"}}
    if illu: e["visual"]["illustration"] = illu
    return e


# ---------------------------------------------------------------- Fermentation
add(P("garum", L("Garum: die römische Fischsauce", "Garum: the Roman fish sauce"),
      L(["Garum", "Liquamen", "Fischsauce", "römische Würzsauce", "Colatura di alici", "Woher kommt der Name Garum"], ["garum", "liquamen", "fish sauce", "Roman fish sauce", "colatura di alici"]),
      L("Garum war die Würzsauce der Römer: Fisch und viel Salz, monatelang stehen gelassen, bis die Enzyme des Fisches sein Eiweiß zu herzhaftem Umami zerlegt haben. Nach ihr ist diese Seite benannt.",
        "Garum was the seasoning sauce of the Romans: fish and lots of salt, left for months until the fish's own enzymes had broken its protein down into savoury umami. This site is named after it."),
      L("Wie ein Haus, das von innen abgebaut wird: Die Arbeiter wohnten schon darin, das Salz sperrt nur die Plünderer aus.",
        "Like a house dismantled from the inside: the workers already lived there, and the salt simply locks out the looters."),
      L("Die Römer schichteten kleine Fische oder Fischinnereien mit Salz in Becken und ließen sie in der Wärme stehen. Das viele Salz hält Fäulnisbakterien fern. Die Verdauungsenzyme im Fisch arbeiten aber weiter und zerlegen Eiweiß in seine Bausteine (Proteolyse). Darunter ist viel Glutamat, der Träger von Umami. Nach einigen Monaten wurde die klare, bernsteinfarbene Flüssigkeit abgeschöpft: das Garum.",
        "The Romans layered small fish or fish innards with salt in vats and left them in the warmth. The large amount of salt keeps putrefying bacteria away. The digestive enzymes in the fish keep working, though, and break protein down into its building blocks (proteolysis). Among them is plenty of glutamate, the carrier of umami. After a few months the clear, amber liquid was skimmed off: the garum."),
      L("Garum zeigt, dass Umami-Würze kein moderner Trick ist. Thailändische und vietnamesische Fischsauce, italienische Colatura di alici und Worcestershiresauce funktionieren nach demselben Prinzip. Moderne Spitzenküchen nennen heute jede so fermentierte Würze ein Garum, auch aus Fleisch, Pilzen oder Bienenbrot.",
        "Garum shows that umami seasoning is no modern trick. Thai and Vietnamese fish sauce, Italian colatura di alici and Worcestershire sauce work on the same principle. Modern high-end kitchens now call any seasoning fermented this way a garum, including ones made from meat, mushrooms or bee bread."),
      L(["Ein paar Tropfen Fischsauce in Tomatensauce, Schmorgericht oder Salatsauce geben Tiefe, ohne nach Fisch zu schmecken.",
         "Fischsauce ist sehr salzig: Erst würzen, dann nachsalzen.",
         "Fischsauce nicht selbst in der Sonne ansetzen: Ohne genaue Salzmenge und Kontrolle können gefährliche Keime wachsen. Gekaufte verwenden."],
        ["A few drops of fish sauce in tomato sauce, a braise or a dressing add depth without tasting of fish.",
         "Fish sauce is very salty: season with it first, then add salt.",
         "Do not ferment fish sauce yourself in the sun: without the right amount of salt and proper control, dangerous germs can grow. Use bought sauce."]),
      [("zeit", L("Je länger die Enzyme arbeiten, desto mehr Eiweiß wird zu Umami", "The longer the enzymes work, the more protein turns into umami")),
       ("salzgehalt", L("Viel Salz hält Fäulnis fern, zu wenig lässt sie zu", "Lots of salt keeps putrefaction away; too little lets it in"))],
      [("w-saucen", L("Ein Spritzer Fischsauce rundet eine Bolognese ab, wie früher das Garum die römische Küche.", "A splash of fish sauce rounds off a Bolognese, just as garum once did in Roman cooking.")),
       ("w-fisch", L("Colatura di alici aus Sardellen ist der direkte Nachfahre des Garums.", "Colatura di alici, made from anchovies, is the direct descendant of garum."))],
      ["umami", "glutamat", "proteolyse", "enzym", "fermentation", "wasseraktivitaet", "koji", "salz-geschmack", "w-fisch"], ["w-fisch", "w-saucen"],
      "an ancient Roman clay amphora with a small dish of amber fish sauce, a few anchovies and coarse salt crystals beside it",
      [{"titel": "Robert I. Curtis: Garum and Salsamenta. Production and Commerce in Materia Medica (1991)"},
       {"titel": "Mother Jones: How a smelly fish sauce helped solve one of ancient Rome's mysteries", "url": "https://www.motherjones.com/?p=503347"}, NOMA]))

add({"id": "proteolyse", "typ": "begriff", "titel": L("Proteolyse", "Proteolysis"),
     "synonyme": L(["Eiweißabbau", "Eiweißspaltung"], ["protein breakdown"]),
     "kurz": L("Das Zerlegen von Eiweiß durch Enzyme in kleinere Stücke bis zu einzelnen Bausteinen (Aminosäuren). Es macht gereiftes Fleisch zart, Käse würzig und Fischsauce herzhaft.",
               "The breaking down of protein by enzymes into smaller pieces, down to single building blocks (amino acids). It makes aged meat tender, cheese savoury and fish sauce rich."),
     "links": ["enzym", "garum", "fleischreifung", "umami"], "quellen": [MC("Kapitel Eiweiß und Enzyme", "Chapter on proteins and enzymes")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add(P("koji", L("Koji: der Schimmelpilz hinter Miso und Sojasauce", "Koji: the mould behind miso and soy sauce"),
      L(["Koji", "Aspergillus oryzae", "Kōji", "Miso", "Sojasauce", "Sake", "Edelpilz Reis"], ["koji", "Aspergillus oryzae", "miso", "soy sauce", "sake"]),
      L("Koji ist ein Schimmelpilz, der auf gedämpftem Reis oder Gerste wächst und Enzyme bildet: Sie machen aus Stärke Zucker und aus Eiweiß Umami.",
        "Koji is a mould that grows on steamed rice or barley and produces enzymes: they turn starch into sugar and protein into umami."),
      L("Wie eine Werkstatt voller Scheren: Der Pilz selbst schmeckt nach wenig, aber seine Werkzeuge zerschneiden alles in schmackhafte Stücke.",
        "Like a workshop full of scissors: the mould itself tastes of little, but its tools cut everything into tasty pieces."),
      L("Man impft gedämpften Reis mit Sporen und hält ihn etwa zwei Tage warm und feucht (Richtwert um 30 °C). Ein weißer, flaumiger Pilzrasen überzieht die Körner. Er gibt zwei Arten von Enzymen ab. Die einen zerlegen Stärke zu Zucker, das braucht man für Sake und süßen Reistrunk. Die anderen zerlegen Eiweiß zu Aminosäuren, daraus entsteht das Umami von Miso und Sojasauce.",
        "Steamed rice is inoculated with spores and kept warm and moist for about two days (as a guide, around 30 °C). A white, fluffy layer of mould covers the grains. It releases two kinds of enzymes. One kind breaks starch down into sugar, which is needed for sake and sweet rice drinks. The other breaks protein down into amino acids, which gives miso and soy sauce their umami."),
      L("Koji ist der Grund, warum die japanische Küche so viel Umami hat. Spitzenköche nutzen ihn heute auch für Garums, zum Reifen von Fleisch und für eigene Würzpasten.",
        "Koji is why Japanese cooking has so much umami. Top chefs now also use it for garums, for ageing meat and for their own seasoning pastes."),
      L(["Nur gekaufte Koji-Sporen oder fertigen Koji-Reis verwenden: Ein naher Verwandter des Pilzes bildet Gift.",
         "Miso erst am Schluss in die Suppe rühren und nicht mehr kochen: So bleibt das Aroma frisch.",
         "Ein Löffel Miso in Salatsauce, Butter oder Schmorgericht wirkt wie ein Umami-Verstärker."],
        ["Only use bought koji spores or ready-made koji rice: a close relative of this mould produces toxins.",
         "Stir miso into soup only at the end and do not boil it any more: that keeps the aroma fresh.",
         "A spoonful of miso in a dressing, butter or a braise acts like an umami booster."]),
      [("temperatur", L("Um 30 °C wächst der Pilz gut, deutlich wärmer stirbt er", "Around 30 °C the mould grows well; much warmer and it dies")),
       ("zeit", L("Nach etwa zwei Tagen hat er genug Enzyme gebildet", "After about two days it has produced enough enzymes"))],
      [("w-huelsenfruechte", L("Miso ist gekochte Soja, mit Koji und Salz monatelang gereift.", "Miso is cooked soya, aged for months with koji and salt.")),
       ("w-getreide", L("Für Sake zerlegt Koji die Reisstärke zu Zucker, den dann Hefe vergärt.", "For sake, koji breaks rice starch down into sugar, which yeast then ferments."))],
      ["fermentation", "enzym", "amylase", "proteolyse", "umami", "garum", "edelschimmel"], ["w-getreide", "w-huelsenfruechte"],
      "a wooden tray of steamed rice grains covered in fine white fluffy koji mould, a small bowl of miso beside it",
      [NOMA, MC("Kapitel Samen: Sojasauce und Miso", "Chapter on seeds: soy sauce and miso")], "fortgeschritten"))

add(P("edelschimmel", L("Edelschimmel: wenn Schimmel erwünscht ist", "Noble moulds: when mould is wanted"),
      L(["Edelschimmel", "Blauschimmel", "Weißschimmel", "Camembert Rinde", "Salami Schimmel", "Schimmel essen", "Schimmel abschneiden"], ["noble mould", "blue cheese mould", "white rind", "salami mould", "is mould safe to eat"]),
      L("Bestimmte Schimmelpilze werden gezielt eingesetzt: Sie machen Camembert cremig, Gorgonzola würzig und schützen Salami. Wilder Schimmel dagegen kann Gift bilden.",
        "Certain moulds are used on purpose: they make Camembert creamy, Gorgonzola savoury and protect salami. Wild mould, on the other hand, can produce toxins."),
      L("Wie ein Wachhund im Garten: Der eigene Hund besetzt den Platz, damit kein streunender hineinkommt.",
        "Like a guard dog in the garden: your own dog takes up the space so that no stray can get in."),
      L("Weißschimmel auf Camembert zerlegt Eiweiß und Fett von außen nach innen. Darum wird der Käse unter der Rinde zuerst weich. Blauschimmel wächst in Luftkanälen, die man in den Käse sticht, und bildet würzige, scharfe Aromen. Auf Salami besetzt ein weißer Edelschimmel die Oberfläche, bremst das Austrocknen und lässt anderen Schimmel nicht hin. Wilder Schimmel bildet dagegen oft Gifte (Mykotoxine), die man weder sieht noch wegkochen kann.",
        "White mould on Camembert breaks down protein and fat from the outside in. That is why the cheese softens under the rind first. Blue mould grows in air channels pierced into the cheese and creates savoury, sharp aromas. On salami, a white noble mould occupies the surface, slows drying and keeps other moulds out. Wild mould, by contrast, often produces toxins (mycotoxins) that you can neither see nor cook away."),
      L("Erklärt, warum man Blauschimmelkäse essen kann, aber verschimmeltes Brot nicht. Der Unterschied liegt nicht im Schimmel an sich, sondern darin, welcher Pilz es ist und wo sein Geflecht schon überall steckt.",
        "Explains why you can eat blue cheese but not mouldy bread. The difference is not mould as such, but which fungus it is and how far its network has already spread."),
      L(["Weiches und Feuchtes mit fremdem Schimmel ganz wegwerfen: Brot, Konfitüre, Joghurt, Obst, Weichkäse. Das Geflecht reicht weiter, als man sieht.",
         "Bei Hartkäse und Salami einzelne Stellen großzügig wegschneiden, mindestens einen Zentimeter (Richtwert).",
         "Camembert reift im Kühlschrank weiter: Je näher am Datum, desto cremiger."],
        ["Throw soft and moist foods with unwanted mould away completely: bread, jam, yoghurt, fruit, soft cheese. The network reaches further than you can see.",
         "On hard cheese and salami, cut away single spots generously, at least one centimetre (as a guide).",
         "Camembert keeps ripening in the fridge: the closer to its date, the creamier it is."]),
      [("zeit", L("Mit der Reifezeit dringt der Schimmel weiter ein und der Käse wird weicher und kräftiger", "With ripening time the mould penetrates further and the cheese turns softer and stronger")),
       ("feuchtigkeit", L("Feuchte Lebensmittel lassen fremden Schimmel tief hineinwachsen", "Moist foods let unwanted mould grow deep inside"))],
      [("w-milch", L("Gorgonzola, Roquefort und Camembert verdanken ihren Charakter einem gezielt zugesetzten Edelschimmel.", "Gorgonzola, Roquefort and Camembert owe their character to a deliberately added noble mould.")),
       ("w-fleisch", L("Der weiße Belag auf Salami ist gewollt und schützt die Wurst beim Trocknen.", "The white coating on salami is intentional and protects the sausage while it dries."))],
      ["kaese", "proteolyse", "fermentation", "koji", "keimwachstum", "w-milch"], ["w-milch", "w-fleisch"],
      "a wedge of blue-veined cheese, a round camembert with white rind and a salami with white mould coating on a wooden board",
      [MC("Kapitel Käse: Schimmelgereifte Käse", "Chapter on cheese: mould-ripened cheeses"),
       {"titel": "Stiftung Warentest: Schimmel auf Lebensmitteln", "url": "https://www.test.de/Lebensmittel-Schimmels-schlimme-Sporen-1133015-1134201/"}]))

# ---------------------------------------------------------------- Geschmack
add(P("bitter", L("Bitter: der Warnsensor, der zum Genuss wurde", "Bitter: the warning sensor that became a pleasure"),
      L(["bitter", "Bitterkeit", "Bitterstoffe", "zu bitter", "Bitterkeit mildern", "Chicorée bitter"], ["bitter", "bitterness", "too bitter", "reduce bitterness", "bitter compounds"]),
      L("Bitter warnt ursprünglich vor Gift. In kleinen Mengen gibt es Kaffee, Schokolade, Bier und Salaten Tiefe, und Salz kann es dämpfen.",
        "Bitterness originally warns of poison. In small amounts it gives depth to coffee, chocolate, beer and salads, and salt can tone it down."),
      L("Wie die Bassstimme im Chor: Allein klingt sie düster, im Zusammenspiel gibt sie Fundament.",
        "Like the bass voice in a choir: alone it sounds gloomy, in harmony it gives a foundation."),
      L("Die Zunge hat rund zwei Dutzend verschiedene Sensoren für Bitterstoffe. Viele Pflanzengifte schmecken bitter, darum reagieren wir empfindlich, Kinder noch stärker als Erwachsene. Wie stark jemand Bitteres wahrnimmt, ist zum Teil angeboren. Salz dämpft Bitterkeit nachweislich, Zucker und Fett überdecken sie.",
        "The tongue has around two dozen different sensors for bitter compounds. Many plant poisons taste bitter, so we are sensitive to it, children even more than adults. How strongly someone perceives bitterness is partly inborn. Salt demonstrably dampens bitterness; sugar and fat mask it."),
      L("Erklärt, warum Salz Grapefruit und Rosenkohl milder macht, warum Kinder Chicorée meiden und warum verbrannter Knoblauch ein Gericht kippen lässt.",
        "Explains why salt makes grapefruit and Brussels sprouts milder, why children avoid chicory and why burnt garlic can tip a dish over."),
      L(["Zu bitter: zuerst eine Prise Salz, dann etwas Süßes oder Fett.",
         "Bittere Salate wie Chicorée oder Radicchio mit süßer Frucht und salzigem Käse kombinieren.",
         "Knoblauch und Nüsse nicht zu dunkel rösten: Ab einem Punkt kippt Röstaroma in Bitterkeit."],
        ["Too bitter: first a pinch of salt, then something sweet or fatty.",
         "Combine bitter leaves such as chicory or radicchio with sweet fruit and salty cheese.",
         "Do not roast garlic and nuts too dark: past a certain point roasted flavour tips into bitterness."]),
      [("salzgehalt", L("Wenig Salz dämpft Bitterkeit spürbar", "A little salt noticeably dampens bitterness")),
       ("temperatur", L("Zu heiß Geröstetes wird bitter", "Anything roasted too hot turns bitter"))],
      [("w-kaffee", L("Zu feiner Mahlgrad oder zu lange Brühzeit löst mehr Bitterstoffe.", "Too fine a grind or too long a brew dissolves more bitter compounds.")),
       ("w-gemuese", L("Rosenkohl, Chicorée und Endivie mögen Salz, Fett und etwas Süße.", "Brussels sprouts, chicory and endive like salt, fat and a little sweetness."))],
      ["kaffee-sauer-bitter", "knoblauch-bitter", "salz-geschmack", "geschmack-balance", "x-salz-bitter", "suess"], ["w-kaffee", "w-gemuese"],
      "a halved grapefruit, a head of red radicchio and a cup of black coffee on a linen cloth",
      [BRESLIN, MC("Kapitel Geschmack und Aroma", "Chapter on taste and flavour")]))

add(P("suess", L("Süß: warum warm süßer schmeckt", "Sweet: why warm tastes sweeter"),
      L(["süß", "Süße", "zu süß", "Süße ausgleichen", "geschmolzene Glace zu süß", "warum schmeckt warm süßer"], ["sweet", "sweetness", "too sweet", "balance sweetness", "melted ice cream too sweet"]),
      L("Süße meldet der Zunge Energie. Wie süß etwas wirkt, hängt stark von der Temperatur ab: Warm schmeckt es deutlich süßer als kalt.",
        "Sweetness signals energy to the tongue. How sweet something seems depends strongly on temperature: warm, it tastes noticeably sweeter than cold."),
      L("Wie ein Radio, dessen Lautstärke mit der Wärme steigt: Derselbe Sender, aber kalt ist er leise gedreht.",
        "Like a radio whose volume rises with warmth: the same station, but cold it is turned down."),
      L("Zucker docken an einen Süß-Sensor auf der Zunge an. Ein Teil der Signalkette arbeitet bei Wärme viel stärker, bei Kälte schwächer. Darum schmeckt geschmolzene Glace pappsüß und warme Cola klebrig. Säure, Bitteres und Salz verändern die Süße zusätzlich: Eine Prise Salz hebt sie, Säure gleicht sie aus.",
        "Sugars dock onto a sweet sensor on the tongue. Part of the signal chain works much harder when warm and more weakly when cold. That is why melted ice cream tastes sickly sweet and warm cola sticky. Acid, bitterness and salt change sweetness further: a pinch of salt lifts it, acid balances it."),
      L("Wer das weiß, süßt kalte Desserts kräftiger und warme sparsamer. Und er rettet ein zu süßes Gericht mit Säure statt mit noch mehr von allem anderen.",
        "Knowing this, you sweeten cold desserts more strongly and warm ones more sparingly. And you rescue an overly sweet dish with acid rather than more of everything else."),
      L(["Glace- und Sorbetmasse warm abschmecken und etwas zu süß lassen: Gefroren wirkt sie deutlich weniger süß.",
         "Zu süß: ein paar Tropfen Zitrone oder eine Prise Salz.",
         "Eine Prise Salz gehört auch in süße Teige und Karamell, sie macht den Geschmack runder."],
        ["Taste ice cream and sorbet mixtures warm and leave them slightly too sweet: frozen, they seem much less sweet.",
         "Too sweet: a few drops of lemon or a pinch of salt.",
         "A pinch of salt also belongs in sweet doughs and caramel; it rounds out the flavour."]),
      [("temperatur", L("Warm schmeckt süßer, kalt weniger süß", "Warm tastes sweeter, cold less sweet")),
       ("zuckergehalt", L("Mehr Zucker macht nicht nur süßer, er bindet auch Wasser und verändert die Textur", "More sugar does not only sweeten, it also binds water and changes texture"))],
      [("w-suesses", L("Eine Glacemasse, die warm genau richtig schmeckt, ist gefroren zu fad.", "An ice cream mixture that tastes just right warm is too bland once frozen.")),
       ("w-obst", L("Erdbeeren mit einem Spritzer Zitrone schmecken fruchtiger, nicht saurer.", "Strawberries with a splash of lemon taste fruitier, not more sour."))],
      ["zucker", "saeure", "salz-geschmack", "geschmack-balance", "gefrierpunkt-senkung", "bitter"], ["w-suesses", "w-obst"],
      "a melting scoop of vanilla ice cream in a glass bowl next to a sugar bowl with a spoon",
      [TALAVERA, MC("Kapitel Zucker und Geschmack", "Chapter on sugars and taste")]))

add(P("geschmack-balance", L("Wie Geschmäcker sich gegenseitig verändern", "How tastes change one another"),
      L(["Geschmack ausgleichen", "abschmecken", "Balance süß sauer", "zu sauer", "zu salzig retten", "Grundgeschmäcker", "fünf Geschmacksrichtungen"], ["balancing flavours", "seasoning to taste", "sweet and sour balance", "too sour", "rescue too salty", "five basic tastes"]),
      L("Süß, sauer, salzig, bitter und umami wirken nicht einzeln: Sie dämpfen oder heben sich gegenseitig. Darauf beruht jedes Abschmecken.",
        "Sweet, sour, salty, bitter and umami do not act alone: they dampen or lift one another. All seasoning is based on this."),
      L("Wie ein Mischpult mit fünf Reglern: Dreht man einen hoch, klingen die anderen plötzlich anders.",
        "Like a mixing desk with five faders: turn one up and the others suddenly sound different."),
      L("Die fünf Grundgeschmäcker werden getrennt erkannt, aber im Gehirn verrechnet. Süß und sauer schwächen sich gegenseitig ab. Salz dämpft Bitterkeit und lässt Süßes runder wirken. Umami und Salz verstärken sich. Schärfe ist kein Geschmack, sondern ein Schmerzreiz, den Süße und Fett mildern.",
        "The five basic tastes are detected separately but combined in the brain. Sweet and sour weaken each other. Salt dampens bitterness and makes sweetness seem rounder. Umami and salt boost each other. Heat from chilli is not a taste but a pain signal, which sweetness and fat soften."),
      L("Fast jedes Problem beim Abschmecken lässt sich mit dem Gegenspieler lösen statt mit mehr Wasser. Nur zu viel Salz lässt sich nicht wirklich ausgleichen, sondern nur verdünnen.",
        "Almost every seasoning problem can be solved with the opposing taste rather than with more water. Only too much salt cannot really be balanced; it can only be diluted."),
      L(["Zu sauer: etwas Süßes oder Fett.",
         "Zu süß: Säure oder eine Prise Salz.",
         "Zu bitter: Salz, dann Süße oder Fett.",
         "Zu scharf: Joghurt, Sahne, Zucker oder Kokosmilch.",
         "Zu salzig: mit ungesalzener Zutat verdünnen. Säure lenkt nur etwas ab."],
        ["Too sour: something sweet or fatty.",
         "Too sweet: acid or a pinch of salt.",
         "Too bitter: salt, then sweetness or fat.",
         "Too hot: yoghurt, cream, sugar or coconut milk.",
         "Too salty: dilute with an unsalted ingredient. Acid only distracts a little."]),
      [("salzgehalt", L("Salz hebt Süßes und Umami, dämpft Bitteres", "Salt lifts sweetness and umami, dampens bitterness")),
       ("zuckergehalt", L("Süße gleicht Säure, Bitterkeit und Schärfe aus", "Sweetness balances acidity, bitterness and heat")),
       ("ph-wert", L("Säure macht Süßes frischer und Fettes leichter", "Acid makes sweet things fresher and fatty things lighter"))],
      [("w-saucen", L("Eine Tomatensauce braucht oft eine Prise Zucker gegen die Säure, eine Vinaigrette Salz gegen das Bittere im Öl.", "A tomato sauce often needs a pinch of sugar against the acidity; a vinaigrette needs salt against the bitterness in the oil.")),
       ("w-kraeuter-gewuerze", L("Ein Chiligericht wirkt mit etwas Zucker und Limette runder und weniger brennend.", "A chilli dish tastes rounder and burns less with a little sugar and lime."))],
      ["salz-geschmack", "saeure", "abschmecken-saeure", "umami", "bitter", "suess", "schaerfe", "essen-flach", "aroma-nase"], ["w-saucen", "w-kraeuter-gewuerze"],
      "five small ceramic bowls with salt, sugar, a lemon wedge, a piece of dark chocolate and a dab of miso, with a tasting spoon",
      [BRESLIN, MC("Kapitel Geschmack und Aroma", "Chapter on taste and flavour")]))

add(P("aroma-nase", L("Geschmack ist meistens Geruch", "Flavour is mostly smell"),
      L(["Geschmack und Geruch", "retronasal", "Aroma riechen", "Schnupfen schmeckt nichts", "Nase und Geschmack", "Aroma"], ["taste and smell", "retronasal smell", "aroma", "cold food tastes of nothing", "nose and flavour"]),
      L("Die Zunge erkennt nur fünf Grundgeschmäcker. Alles andere, von Erdbeere bis Zimt, riecht die Nase, auch von innen beim Kauen.",
        "The tongue only recognises five basic tastes. Everything else, from strawberry to cinnamon, is smelled by the nose, including from the inside while you chew."),
      L("Wie ein Kamin mit zwei Öffnungen: Der Duft kommt von vorne herein, aber auch von hinten aus dem Mund durch den Schacht nach oben.",
        "Like a chimney with two openings: the scent comes in at the front, but also from the back of the mouth up through the shaft."),
      L("Beim Kauen und Schlucken steigen Duftstoffe aus dem Mund hinten in die Nase hinauf (retronasal). Das Gehirn verlegt diesen Eindruck auf die Zunge, darum halten wir ihn für Geschmack. Mit verstopfter Nase bleiben nur süß, sauer, salzig, bitter und umami übrig. Duftstoffe sind flüchtig: Warme Speisen geben mehr davon ab als kalte.",
        "As you chew and swallow, aroma compounds rise from the back of the mouth into the nose (retronasal). The brain places this impression on the tongue, so we take it for taste. With a blocked nose, only sweet, sour, salty, bitter and umami remain. Aroma compounds are volatile: warm food releases more of them than cold."),
      L("Erklärt, warum Essen bei Schnupfen fad ist, warum kalte Speisen kräftiger gewürzt werden müssen und warum Kräuter erst am Schluss dazukommen.",
        "Explains why food tastes bland when you have a cold, why cold dishes need stronger seasoning and why herbs go in at the end."),
      L(["Kalt serviertes Essen kräftiger würzen und kalt abschmecken.",
         "Zarte Kräuter und Zitronenschale erst kurz vor dem Servieren: Ihre Duftstoffe verfliegen in der Hitze.",
         "Gewürze kurz in Fett rösten: Viele Duftstoffe lösen sich in Fett und werden so freigesetzt."],
        ["Season food served cold more strongly, and taste it cold.",
         "Add delicate herbs and lemon zest just before serving: their aroma compounds escape in the heat.",
         "Toast spices briefly in fat: many aroma compounds dissolve in fat and are released that way."]),
      [("temperatur", L("Wärme setzt mehr Duftstoffe frei, Kälte dämpft sie", "Warmth releases more aroma compounds; cold mutes them")),
       ("zeit", L("Langes Kochen treibt flüchtige Aromen aus", "Long cooking drives out volatile aromas"))],
      [("w-kraeuter-gewuerze", L("Basilikum, Koriander und Petersilie verlieren beim Mitkochen ihren frischen Duft.", "Basil, coriander and parsley lose their fresh scent when cooked along.")),
       ("w-kaffee", L("Frisch gemahlener Kaffee duftet stärker, weil die Duftstoffe noch nicht verflogen sind.", "Freshly ground coffee smells stronger because its aroma compounds have not yet escaped."))],
      ["aroma-loeslichkeit", "aroma-blooming", "geschmack-balance", "x-nase-zu", "flavor-pairing", "reduktion"], ["w-kraeuter-gewuerze", "w-kaffee"],
      "a nose-shaped wisp of aromatic steam rising from a cup of tea next to a halved strawberry and a cinnamon stick",
      [MC("Kapitel Geschmack und Aroma", "Chapter on taste and flavour"),
       {"titel": "Gordon M. Shepherd: Neurogastronomy. How the Brain Creates Flavor (2012)"}]))

add(P("flavor-pairing", L("Flavor Pairing: passen gleiche Aromen zusammen?", "Flavour pairing: do shared aromas go together?"),
      L(["Flavor Pairing", "Foodpairing", "Aromen kombinieren", "was passt zusammen", "Schokolade und Kaviar", "Aromapaare"], ["flavour pairing", "food pairing", "combining flavours", "what goes with what", "aroma pairs"]),
      L("Die Idee: Zutaten, die wichtige Duftstoffe teilen, passen gut zusammen. Das liefert gute Einfälle, ist aber kein Naturgesetz.",
        "The idea: ingredients that share key aroma compounds go well together. It produces good ideas, but it is not a law of nature."),
      L("Wie zwei Fremde im Zug, die merken, dass sie aus demselben Dorf kommen: Oft verstehen sie sich, aber manche der besten Freundschaften verbindet gar nichts.",
        "Like two strangers on a train who find out they come from the same village: they often get on, but some of the best friendships share nothing at all."),
      L("Jede Zutat riecht nach einer Mischung aus vielen Duftstoffen. Anfang der 2000er-Jahre fiel auf, dass überraschende Paare wie weiße Schokolade und Kaviar einige davon teilen. Eine Auswertung von rund 56 000 Rezepten zeigte: Westliche Küchen kombinieren tatsächlich gern Zutaten mit gemeinsamen Duftstoffen. Ostasiatische Küchen tun eher das Gegenteil und schmecken trotzdem hervorragend.",
        "Every ingredient smells of a blend of many aroma compounds. In the early 2000s it was noticed that surprising pairs such as white chocolate and caviar share some of them. An analysis of around 56,000 recipes showed that Western cuisines do tend to combine ingredients with shared aroma compounds. East Asian cuisines tend to do the opposite and still taste excellent."),
      L("Flavor Pairing hilft beim Erfinden neuer Kombinationen, etwa Erdbeere mit Basilikum oder Tomate mit Erdbeere. Ob ein Gericht gelingt, entscheiden aber auch Grundgeschmäcker, Textur, Temperatur und Gewohnheit.",
        "Flavour pairing helps when inventing new combinations, such as strawberry with basil or tomato with strawberry. Whether a dish works also depends on basic tastes, texture, temperature and habit."),
      L(["Für neue Ideen: eine Zutat wählen und eine zweite suchen, die ähnlich duftet.",
         "Gleiche Aromen verstärken sich, Gegensätze bringen Spannung: Beides kann funktionieren.",
         "Am Schluss immer die Grundgeschmäcker ausbalancieren, das Aroma allein reicht nicht."],
        ["For new ideas: pick one ingredient and look for a second that smells similar.",
         "Shared aromas reinforce each other, contrasts bring tension: both can work.",
         "Always balance the basic tastes at the end; aroma alone is not enough."]),
      [],
      [("w-obst", L("Erdbeere und Basilikum teilen fruchtig-grüne Duftnoten.", "Strawberry and basil share fruity, green aroma notes.")),
       ("w-kraeuter-gewuerze", L("Koriandersamen und Orangenschale teilen zitrusartige Duftstoffe.", "Coriander seed and orange peel share citrus-like aroma compounds."))],
      ["aroma-nase", "geschmack-balance", "aroma-loeslichkeit", "w-kraeuter-gewuerze"], ["w-obst", "w-kraeuter-gewuerze"],
      "a strawberry and a sprig of basil connected by a fine dotted ink line, with a few pieces of white chocolate",
      [AHN, MC("Kapitel Geschmack und Aroma", "Chapter on taste and flavour")], "fortgeschritten"))

add({"id": "xanthan", "typ": "begriff", "titel": L("Xanthan", "Xanthan gum"),
     "synonyme": L(["Xanthan", "Xanthangummi", "E 415"], ["xanthan", "xanthan gum", "E415"]),
     "kurz": L("Ein Bindemittel, das Bakterien aus Zucker bilden. Schon wenige Zehntelgramm pro 100 ml machen Flüssigkeiten kalt oder warm sämig, ohne Kochen, und es hält Salatsaucen stabil. Zu viel macht schleimig.",
               "A thickener that bacteria make from sugar. Just a few tenths of a gram per 100 ml make liquids silky, cold or hot, without cooking, and it keeps dressings stable. Too much turns slimy."),
     "links": ["abbinden-staerke", "agar-agar", "emulsion", "fermentation"], "quellen": [MC("Kapitel Saucen: Gummis und Verdickungsmittel", "Chapter on sauces: gums and thickeners")], "status": "entwurf", "schwierigkeit": "einsteiger"})

# ---------------------------------------------------------------- Experimente
add({"id": "x-nase-zu", "typ": "experiment", "titel": L("Mit zugehaltener Nase schmeckt man nur noch süß", "With your nose pinched, you only taste sweet"),
     "synonyme": L(["Geschmackstest Nase", "Gummibärchen Experiment", "Nase zuhalten schmecken"], ["nose pinch taste test", "jelly bean experiment"]),
     "kurz": L("Ein Gummibärchen mit zugehaltener Nase schmeckt nur süß. Lässt man los, ist plötzlich die Frucht da.",
               "A gummy bear eaten with your nose pinched only tastes sweet. Let go, and suddenly the fruit is there."),
     "bild_im_kopf": L("Wie ein Film ohne Ton: Man sieht, dass etwas passiert, aber erst der Ton erzählt die Geschichte.", "Like a film without sound: you can see something happening, but only the sound tells the story."),
     "material": L(["Gummibärchen in verschiedenen Farben", "eine zweite Person, die die Farbe auswählt"], ["gummy bears in different colours", "a second person who chooses the colour"]),
     "schritte": L(["Augen schließen und die Nase fest zuhalten.", "Die zweite Person gibt ein Gummibärchen in den Mund.", "Kauen und raten, welche Sorte es ist.", "Dann die Nase loslassen und weiterkauen."],
                   ["Close your eyes and pinch your nose firmly.", "The second person puts a gummy bear in your mouth.", "Chew and guess which flavour it is.", "Then let go of your nose and keep chewing."]),
     "beobachtung": L("Mit zugehaltener Nase schmeckt man nur süß und etwas sauer. Sobald die Nase frei ist, erkennt man Erdbeere, Zitrone oder Himbeere.",
                      "With your nose pinched you only taste sweet and a little sour. As soon as your nose is free, you recognise strawberry, lemon or raspberry."),
     "erklaerung": L("Die Zunge erkennt nur Grundgeschmäcker wie süß und sauer. Die Fruchtsorte ist ein Duft. Er steigt beim Kauen von hinten in die Nase, aber nur, wenn dort Luft strömen kann.",
                     "The tongue only recognises basic tastes such as sweet and sour. The fruit flavour is a scent. It rises into the nose from the back while you chew, but only if air can flow there."),
     "dauer": L("5 Minuten", "5 minutes"),
     "links": ["aroma-nase", "geschmack-balance", "suess"], "welten": ["w-suesses"],
     "visual": {"vorlage": "ablauf", "illustration": "a small glass bowl of colourful gummy bears and a clothes peg lying beside it"},
     "quellen": [MC("Kapitel Geschmack und Aroma", "Chapter on taste and flavour")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "x-salz-bitter", "typ": "experiment", "titel": L("Eine Prise Salz macht Grapefruit süßer", "A pinch of salt makes grapefruit sweeter"),
     "synonyme": L(["Salz gegen Bitterkeit", "Grapefruit mit Salz", "Salz im Kaffee"], ["salt against bitterness", "salted grapefruit", "salt in coffee"]),
     "kurz": L("Zwei Schnitze Grapefruit, einer mit einer winzigen Prise Salz: Der gesalzene schmeckt weniger bitter und süßer.",
               "Two segments of grapefruit, one with a tiny pinch of salt: the salted one tastes less bitter and sweeter."),
     "bild_im_kopf": L("Wie ein Vorhang, der vor eine grelle Lampe gezogen wird: Plötzlich sieht man die anderen Farben im Raum.", "Like a curtain drawn in front of a glaring lamp: suddenly you can see the other colours in the room."),
     "material": L(["eine Grapefruit", "Salz", "ein Glas Wasser zum Neutralisieren"], ["a grapefruit", "salt", "a glass of water to rinse"]),
     "schritte": L(["Zwei Schnitze herauslösen.", "Auf einen ganz wenig Salz streuen, gerade sichtbar.", "Zuerst den ungesalzenen probieren, Wasser trinken, dann den gesalzenen.", "Vergleichen: Wie bitter, wie süß, wie salzig?"],
                   ["Take out two segments.", "Sprinkle a very little salt on one, just visible.", "Taste the unsalted one first, drink some water, then the salted one.", "Compare: how bitter, how sweet, how salty?"]),
     "beobachtung": L("Der gesalzene Schnitz schmeckt kaum salzig, aber weniger bitter, und die Süße tritt hervor.",
                      "The salted segment hardly tastes salty, but it is less bitter and the sweetness comes forward."),
     "erklaerung": L("Salz dämpft die Wahrnehmung von Bitterstoffen. Weil das Bittere zurücktritt, schmeckt man die Süße stärker, obwohl kein Zucker dazugekommen ist.",
                     "Salt dampens the perception of bitter compounds. Because the bitterness recedes, you taste the sweetness more strongly, although no sugar has been added."),
     "dauer": L("5 Minuten", "5 minutes"),
     "links": ["bitter", "geschmack-balance", "salz-geschmack", "suess"], "welten": ["w-obst"],
     "visual": {"vorlage": "ablauf", "illustration": "two pink grapefruit segments on a small plate, one sprinkled with a few salt crystals, a pinch bowl of salt beside them"},
     "quellen": [BRESLIN], "status": "entwurf", "schwierigkeit": "einsteiger"})


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
    ids = [e["id"] for e in E]
    ex = json.loads(subprocess.check_output([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "extract", *ids], cwd=ROOT))

    def pick(shape, src):
        if isinstance(shape, dict): return {k: (src[k] if k == "synonyme" else pick(v, src[k])) for k, v in shape.items()}
        if isinstance(shape, list): return [pick(v, src[i]) for i, v in enumerate(shape)]
        if isinstance(src, dict): return src.get("wirkung", src.get("text"))
        return src
    batch = {e["id"]: pick(ex[e["id"]], res(e, 1)) for e in E}
    path = f"{ROOT}/content/en/_batch_geschmack.json"
    json.dump(batch, open(path, "w"), ensure_ascii=False, indent=1)
    subprocess.check_call([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "apply", path], cwd=ROOT)
    os.remove(path)
    print(len(E), "Einträge geschrieben")
