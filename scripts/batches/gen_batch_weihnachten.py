"""Weihnachtsbatch: Guetzli, Grittibänz, Lebkuchen, Glühwein, Triebsalze, Lagern, plus Lernpfad «Weihnachtsbäckerei verstehen».
Deutsch und Englisch als Paare L(deutsch, englisch), wie in gen_batch_welten2.py."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_batch_welten2 import L, res, MC, U, tree3, ROOT  # noqa: E402

E = []
add = E.append
GEB = ["w-gebaeck", "w-suesses"]


def G(id, titel, syn, kurz, bild, schwierigkeit, schritte, links, welten, illu, quellen=None):
    """Gericht mit Schlüsselmomenten [(schritt, warum, prinzip)]."""
    return {"id": id, "typ": "gericht", "titel": titel, "synonyme": syn, "kurz": kurz, "bild_im_kopf": bild, "schwierigkeit": schwierigkeit,
            "schluesselmomente": [{"schritt": a, "warum": b, "prinzip": c} for a, b, c in schritte],
            "links": links, "welten": welten, "visual": {"vorlage": "ablauf", "illustration": illu},
            "quellen": quellen or [MC("Kapitel Teige und Gebäck", "Chapter on doughs and pastry")], "status": "entwurf"}


add(G("g-mailaenderli", L("Mailänderli", "Mailänderli (Swiss butter biscuits)"), L(["Mailänderli backen", "Butterguetzli", "Weihnachtsguetzli"], ["Swiss Christmas biscuits", "butter cookies", "Mailänderli"]),
      L("Mürbe Butterguetzli, die beim Ausstechen die Form halten und mit Eigelb golden glänzen: kalter Teig und wenig Kneten sind das Geheimnis.",
        "Short butter biscuits that hold their shape when cut and shine golden with egg yolk: cold dough and little kneading do the trick."),
      L("Wie Sand am Strand: Locker zusammengedrückt hält er die Form, zu fest geknetet wird er zäh.", "Like sand on the beach: pressed together loosely it holds its shape, kneaded too hard it turns tough."),
      "einsteiger",
      [(L("Weiche Butter mit Zucker hell rühren, Eier und Zitronenschale dazu", "Cream soft butter with sugar until pale, add eggs and lemon zest"),
        L("Das Rühren schlägt etwas Luft ein, die Guetzli werden zart statt hart.", "Creaming beats in a little air, so the biscuits turn tender rather than hard."), "luftig"),
       (L("Mehl nur kurz untermischen, bis kein Mehl mehr sichtbar ist", "Mix in the flour only briefly, until no dry flour is visible"),
        L("Je weniger geknetet wird, desto weniger Gluten entsteht. Darum bleiben die Guetzli mürbe.", "The less it is kneaded, the less gluten forms. That keeps the biscuits short."), "glutenbildung"),
       (L("Teig mindestens eine Stunde kühlen, dann etwa 7 mm dick auswallen und ausstechen (Richtwert)", "Chill the dough for at least an hour, then roll out about 7 mm thick and cut out (as a guide)"),
        L("Kalte Butter ist fest: Der Teig klebt nicht, und die Formen zerlaufen im Ofen nicht.", "Cold butter is firm: the dough does not stick and the shapes do not spread in the oven."), "teig-kuehlen"),
       (L("Zweimal mit Eigelb bestreichen, bei etwa 200 °C 8–10 Minuten backen (Richtwert)", "Brush twice with egg yolk, bake at about 200 °C for 8–10 minutes (as a guide)"),
        L("Eiweiß und Zucker im Eigelb bräunen schnell und geben den goldenen Glanz.", "The protein and sugar in the yolk brown quickly and give the golden sheen."), "maillard-reaktion")],
      ["muerbe", "glutenbildung", "teig-kuehlen", "guetzli-lagern", "w-gebaeck"], GEB,
      "golden glazed Swiss Mailänderli butter biscuits in heart and star shapes on a baking tray with cookie cutters"))

add(G("g-spitzbuben", L("Spitzbuben", "Spitzbuben (jam-filled biscuits)"), L(["Spitzbuben backen", "Linzer Guetzli", "Konfitüreguetzli"], ["jam sandwich biscuits", "Linzer cookies"]),
      L("Zwei dünne, mürbe Böden mit Konfitüre dazwischen: Hell gebacken bleiben sie zart, und aufgekochte Konfitüre klebt sie zusammen.",
        "Two thin, short biscuits with jam in between: baked pale they stay tender, and boiled-up jam glues them together."),
      L("Wie ein Sandwich mit eingebautem Fenster: Unten der Boden, oben der Rahmen, dazwischen leuchtet die Konfitüre.", "Like a sandwich with a built-in window: the base below, the frame above, the jam glowing in between."),
      "fortgeschritten",
      [(L("Mürbeteig mit Puderzucker machen und kühlen", "Make a shortcrust with icing sugar and chill it"),
        L("Puderzucker löst sich schnell und macht den Teig fein und zart.", "Icing sugar dissolves quickly and makes the dough fine and tender."), "muerbe"),
       (L("Dünn auswallen, ausstechen, bei der Hälfte ein Loch ausstechen", "Roll out thinly, cut out, and cut a hole in half of them"),
        L("Dünne Böden backen schnell durch, bevor sie bräunen.", "Thin rounds bake through quickly, before they brown."), "waermeleitung"),
       (L("Bei etwa 200 °C nur 6–8 Minuten backen, bis sie hell sind (Richtwert)", "Bake at about 200 °C for only 6–8 minutes, until still pale (as a guide)"),
        L("Spitzbuben sollen hell bleiben: Mehr Bräunung macht sie hart und bitter.", "Spitzbuben should stay pale: more browning makes them hard and bitter."), "maillard-reaktion"),
       (L("Konfitüre kurz aufkochen, auf die Böden streichen, Deckel mit Loch darauf", "Bring the jam briefly to the boil, spread on the bases, add the tops with the hole"),
        L("Heiße Konfitüre ist flüssig und verteilt sich gut. Beim Abkühlen geliert das Pektin wieder und klebt die Hälften fest.", "Hot jam is runny and spreads well. As it cools, the pectin sets again and glues the halves together."), "gelbildung-pektin")],
      ["muerbe", "gelbildung-pektin", "teig-kuehlen", "w-gebaeck"], GEB,
      "Swiss Spitzbuben jam-filled biscuits dusted with icing sugar, red jam showing through heart-shaped windows"))

add(G("g-zimtsterne", L("Zimtsterne", "Cinnamon stars (Zimtsterne)"), L(["Zimtsterne backen", "Zimtstern Glasur"], ["cinnamon star cookies", "German cinnamon stars"]),
      L("Mandeln, Zucker und Eischnee ohne Mehl: Die weiße Glasur bleibt nur weiß, wenn der Ofen kühl genug ist.",
        "Almonds, sugar and whisked egg white, no flour: the white glaze stays white only if the oven is cool enough."),
      L("Wie Schnee auf einem Dach: Er bleibt liegen, solange die Sonne nicht zu stark scheint.", "Like snow on a roof: it stays as long as the sun is not too strong."),
      "fortgeschritten",
      [(L("Eiweiß mit Puderzucker steif schlagen, einen Teil als Glasur beiseitestellen", "Whisk egg white with icing sugar until stiff, set some aside for the glaze"),
        L("Zucker stabilisiert den Schaum. Er wird fest und glänzend und trocknet später zu einer Glasur.", "Sugar stabilises the foam. It turns firm and glossy and later dries into a glaze."), "schaumbildung"),
       (L("Den Rest mit gemahlenen Mandeln und Zimt zu einem Teig verarbeiten", "Work the rest into a dough with ground almonds and cinnamon"),
        L("Ohne Mehl hält das Eiweiß den Teig zusammen. Die Mandeln bringen Fett und Biss.", "Without flour, the egg white holds the dough together. The almonds bring fat and bite."), "eiweiss-gerinnung"),
       (L("Ausstechen, glasieren und einige Stunden trocknen lassen", "Cut out, glaze and leave to dry for a few hours"),
        L("Die Glasur bekommt eine trockene Haut und reißt im Ofen weniger.", "The glaze forms a dry skin and cracks less in the oven."), "verdampfen"),
       (L("Bei etwa 150 °C nur wenige Minuten backen (Richtwert)", "Bake at about 150 °C for just a few minutes (as a guide)"),
        L("Bei höherer Hitze bräunen Eiweiß und Zucker, und die Glasur wird gelblich. Innen sollen die Sterne weich bleiben.", "At higher heat, protein and sugar brown and the glaze turns yellowish. Inside, the stars should stay soft."), "maillard-reaktion")],
      ["schaumbildung", "g-meringue", "guetzli-lagern", "w-gebaeck"], GEB,
      "star-shaped cinnamon cookies with bright white meringue glaze, a cinnamon stick and almonds beside them"))

add(G("g-brunsli", L("Basler Brunsli", "Basler Brunsli (chocolate almond biscuits)"), L(["Brunsli backen", "Schokoladeguetzli ohne Mehl"], ["Swiss chocolate almond cookies", "flourless chocolate cookies"]),
      L("Mandeln, Schokolade, Zucker und Eiweiß ohne Mehl: Kurz und heiß gebacken bleiben sie innen weich und werden außen leicht fest.",
        "Almonds, chocolate, sugar and egg white without flour: baked short and hot they stay soft inside and turn slightly firm outside."),
      L("Wie eine Praline im Mantel: Außen eine dünne Kruste, innen weich wie Marzipan.", "Like a chocolate with a coat: a thin crust outside, soft as marzipan inside."),
      "einsteiger",
      [(L("Mandeln, Zucker, Kakao oder geschmolzene Schokolade und Eiweiß zu einem Teig kneten", "Knead almonds, sugar, cocoa or melted chocolate and egg white into a dough"),
        L("Das Eiweiß bindet, der Zucker hält Feuchtigkeit fest. Ohne Mehl entsteht kein Gluten, der Teig bleibt zart.", "The egg white binds, the sugar holds moisture. Without flour no gluten forms, and the dough stays tender."), "zucker-feuchtigkeit"),
       (L("Auf Zucker auswallen und ausstechen", "Roll out on sugar and cut out"),
        L("Zucker statt Mehl verhindert Kleben und gibt eine feine, knusprige Oberfläche.", "Sugar instead of flour stops sticking and gives a fine, crisp surface."), "zucker"),
       (L("Einige Stunden oder über Nacht antrocknen lassen", "Leave to dry for a few hours or overnight"),
        L("Die Oberfläche trocknet zu einer Haut, die im Ofen die Form hält.", "The surface dries into a skin that holds the shape in the oven."), "verdampfen"),
       (L("Bei hoher Hitze, etwa 250 °C, nur 3–5 Minuten backen (Richtwert)", "Bake at high heat, about 250 °C, for just 3–5 minutes (as a guide)"),
        L("Die kurze, starke Hitze festigt nur die Außenseite. Länger gebacken würden sie hart.", "The short, strong heat only firms the outside. Baked longer, they would turn hard."), "waermeleitung")],
      ["zucker-feuchtigkeit", "guetzli-lagern", "w-gebaeck"], GEB,
      "dark chocolate almond Basler Brunsli biscuits in heart and clover shapes, coated with sugar"))

add(G("g-chraebeli", L("Chräbeli", "Chräbeli (Swiss aniseed biscuits)"), L(["Anisguetzli", "Chräbeli Füsschen", "Anisbrötli"], ["aniseed cookies", "Swiss anise biscuits", "Springerle-style biscuits"]),
      L("Anisguetzli, die über Nacht antrocknen und im Ofen kleine Füßchen bekommen: Die trockene Haut oben hält, der weiche Teig drückt unten heraus.",
        "Aniseed biscuits that dry overnight and grow little feet in the oven: the dry skin on top holds, and the soft dough pushes out underneath."),
      L("Wie ein Topf mit Deckel, der überkocht: Oben ist zu, also quillt es unten heraus.", "Like a pot with a lid boiling over: the top is shut, so it bubbles out underneath."),
      "fortgeschritten",
      [(L("Eier und Zucker lange schaumig schlagen, Anis und Mehl unterheben", "Whisk eggs and sugar for a long time until foamy, fold in aniseed and flour"),
        L("Viel eingeschlagene Luft macht den Teig später leicht und lässt ihn im Ofen aufgehen.", "Lots of beaten-in air makes the dough light later and lets it rise in the oven."), "schaumbildung"),
       (L("Rollen formen, schräg einschneiden und leicht biegen", "Shape into rolls, cut diagonally and bend slightly"),
        L("Die Einschnitte öffnen sich beim Backen zu den typischen Krallen.", "The cuts open into the typical claws during baking."), "mechanik"),
       (L("Bei Raumtemperatur 24 Stunden trocknen lassen", "Leave to dry at room temperature for 24 hours"),
        L("Die Oberfläche trocknet zu einer festen Zuckerhaut, das Innere bleibt feucht.", "The surface dries into a firm sugar skin; the inside stays moist."), "verdampfen"),
       (L("Bei niedriger Hitze, etwa 140–150 °C, backen (Richtwert)", "Bake at low heat, about 140–150 °C (as a guide)"),
        L("Das Innere dehnt sich mit Dampf aus. Die Haut oben gibt nicht nach, also quillt der Teig unten heraus: Das sind die Füßchen.", "The inside expands with steam. The skin on top does not give, so the dough swells out at the bottom: those are the feet."), "dampflockerung")],
      ["dampflockerung", "schaumbildung", "guetzli-lagern", "w-gebaeck"], GEB,
      "pale Swiss Chräbeli aniseed biscuits with little feet and claw-shaped cuts, a few star anise beside them"))

add(G("g-grittibaenz", L("Grittibänz", "Grittibänz (Swiss bread man)"), L(["Grittibänz backen", "Grättimaa", "Elggermaa", "Samichlaus"], ["Swiss St Nicholas bread", "bread man", "Grättimaa"]),
      L("Der Hefeteigmann zum Samichlaus ist ein Zopfteig in Form: Kneten baut das Netz, Ruhe lässt ihn aufgehen, Eigelb macht ihn glänzend braun.",
        "The yeast-dough man for St Nicholas Day is a Zopf dough in a shape: kneading builds the network, rest lets it rise, egg yolk makes it shiny and brown."),
      L("Wie ein Ballon, der eine Form bekommt: Das Gas bläst ihn auf, die Hülle bestimmt die Figur.", "Like a balloon given a shape: the gas inflates it, the skin decides the figure."),
      "einsteiger",
      [(L("Mehl, Milch, Butter, Hefe, Zucker und Salz 10 Minuten kneten", "Knead flour, milk, butter, yeast, sugar and salt for 10 minutes"),
        L("Das Kneten baut das Glutennetz, das später das Gas der Hefe hält.", "Kneading builds the gluten network that will later hold the yeast's gas."), "glutenbildung"),
       (L("Zugedeckt aufs doppelte Volumen gehen lassen", "Leave covered until doubled in size"),
        L("Die Hefe bildet Gas und Aromen. Milch und Butter machen den Teig weich und die Kruste zart.", "The yeast produces gas and flavour. Milk and butter make the dough soft and the crust tender."), "hefegaerung"),
       (L("Figur formen, Arme und Beine einschneiden, nochmals kurz gehen lassen", "Shape the figure, cut arms and legs, leave to rise briefly again"),
        L("Die zweite kurze Gare entspannt den Teig, sonst reißen die Einschnitte unschön auf.", "The second short proof relaxes the dough; otherwise the cuts tear open untidily."), "ruhezeit"),
       (L("Mit Eigelb bestreichen, bei etwa 200 °C 20–25 Minuten backen (Richtwert)", "Brush with egg yolk, bake at about 200 °C for 20–25 minutes (as a guide)"),
        L("Eigelb, Milchzucker und Butter bräunen schnell zu einer glänzenden Kruste.", "Egg yolk, lactose and butter brown quickly into a glossy crust."), "maillard-reaktion")],
      ["g-zopf", "hefegaerung", "glutenbildung", "w-brot"], ["w-brot", "w-gebaeck"],
      "a golden glazed Swiss Grittibänz bread man with raisin eyes and a small clay pipe, on a wooden board"))

add(G("g-lebkuchen", L("Lebkuchen", "Gingerbread (Lebkuchen)"), L(["Lebkuchen backen", "Honiglebkuchen", "Biber", "Lebkuchenteig"], ["honey gingerbread", "Lebkuchen", "Swiss Biber"]),
      L("Honig hält Lebkuchen weich, und besondere Triebmittel lockern den schweren Teig: Hirschhornsalz und Pottasche.",
        "Honey keeps gingerbread soft, and special raising agents lighten the heavy dough: baker's ammonia and potash."),
      L("Wie ein Schwammtuch in der Küche: Honig zieht Feuchtigkeit an und gibt sie nicht mehr her.", "Like a kitchen sponge cloth: honey draws in moisture and won't let go of it."),
      "fortgeschritten",
      [(L("Honig und Zucker erwärmen, Gewürze dazu, abkühlen lassen", "Warm honey and sugar, add spices, leave to cool"),
        L("Warm löst sich alles gut, und die Gewürze geben ihr Aroma an den Honig ab.", "Warm, everything dissolves easily and the spices release their aroma into the honey."), "aroma-loeslichkeit"),
       (L("Mehl und aufgelöstes Hirschhornsalz oder Pottasche einarbeiten", "Work in flour and dissolved baker's ammonia or potash"),
        L("Hefe käme gegen viel Honig und Zucker kaum an. Diese Triebsalze bilden erst im Ofen Gas.", "Yeast could hardly cope with so much honey and sugar. These raising salts only release gas in the oven."), "triebmittel"),
       (L("Den Teig mindestens über Nacht, traditionell länger, ruhen lassen", "Rest the dough at least overnight, traditionally longer"),
        L("Mehl nimmt die Feuchtigkeit ganz auf, und die Aromen verbinden sich.", "The flour fully absorbs the moisture and the flavours come together."), "ruhezeit"),
       (L("Backen und danach luftdicht lagern, wenn nötig mit einem Apfelschnitz", "Bake, then store airtight, with an apple slice if needed"),
        L("Honig zieht Feuchtigkeit an. In der Dose bleibt sie im Lebkuchen, und er wird über die Tage sogar weicher.", "Honey draws in moisture. In the tin it stays in the gingerbread, which even gets softer over the days."), "zucker-feuchtigkeit")],
      ["hirschhornsalz", "pottasche", "honig", "guetzli-lagern", "w-gebaeck"], GEB,
      "honey gingerbread hearts and a Swiss Biber with almond decoration, a jar of honey beside them"))

add(G("g-gluehwein", L("Glühwein", "Mulled wine (Glühwein)"), L(["Glühwein machen", "Glühwein Alkohol", "Punsch"], ["mulled wine", "Glühwein", "hot spiced wine"]),
      L("Wein mit Gewürzen sanft erhitzt, nicht gekocht: So bleiben Aroma und auch der meiste Alkohol drin.",
        "Wine with spices heated gently, not boiled: that keeps the aroma, and most of the alcohol too."),
      L("Wie ein Teebeutel aus Gewürzen in warmem Wein: Ziehen lassen ja, kochen nein.", "Like a teabag of spices in warm wine: steep it, yes; boil it, no."),
      "einsteiger",
      [(L("Rotwein mit Zimt, Nelken, Sternanis, Orangenschale und Zucker erwärmen", "Warm red wine with cinnamon, cloves, star anise, orange peel and sugar"),
        L("Viele Duftstoffe der Gewürze lösen sich in Alkohol besser als in Wasser.", "Many aroma compounds in the spices dissolve better in alcohol than in water."), "aroma-loeslichkeit"),
       (L("Auf etwa 70 °C bringen und nicht kochen lassen (Richtwert)", "Bring to about 70 °C and do not let it boil (as a guide)"),
        L("Alkohol siedet schon bei rund 78 °C. Kocht der Wein, verfliegen mit dem Alkohol auch Aromen, und er schmeckt flach.", "Alcohol boils at around 78 °C. If the wine boils, aromas escape along with the alcohol and it tastes flat."), "siedepunkt-druck"),
       (L("20–30 Minuten ziehen lassen, dann Gewürze entfernen", "Let it steep for 20–30 minutes, then remove the spices"),
        L("Länger ziehende Nelken und Zimtrinde geben bittere, herbe Stoffe ab.", "Cloves and cinnamon bark steeped too long release bitter, astringent compounds."), "extraktion"),
       (L("Für Kinder: Traubensaft statt Wein", "For children: grape juice instead of wine"),
        L("Auch langes Köcheln entfernt Alkohol nicht vollständig. Nach 15 Minuten ist noch rund 40 % davon da (Richtwert).", "Even long simmering does not remove the alcohol completely. After 15 minutes around 40 % of it is still there (as a guide)."), "verdampfen")],
      ["aroma-loeslichkeit", "wein", "extraktion"], ["w-suesses"],
      "a glass mug of steaming mulled wine with an orange slice, cinnamon sticks, cloves and star anise",
      quellen=[MC("Kapitel Wein und Alkohol", "Chapter on wine and alcohol"), {"titel": "USDA: Table of Nutrient Retention Factors, Release 6 (Alkohol beim Kochen)"}]))

# Probleme
add({"id": "guetzli-hart", "typ": "symptom", "titel": L("Guetzli werden steinhart", "Christmas biscuits turn rock hard"),
     "synonyme": L(["Kekse hart", "Plätzchen hart", "Lebkuchen hart", "Guetzli trocken"], ["hard cookies", "biscuits gone hard", "hard gingerbread"]),
     "kurz": L("Zu lange gebacken oder offen gelagert: Die Guetzli verlieren Feuchtigkeit, und der Zucker darin wird fest.",
               "Baked too long or stored open: the biscuits lose moisture, and the sugar in them sets hard."),
     "bild_im_kopf": L("Wie ein Brot, das man offen liegen lässt: Am nächsten Tag ist es ein Ziegel.", "Like bread left out uncovered: the next day it is a brick."),
     "ursachen": [
         U(L("Zu lange gebacken", "Baked too long"), 3, "verdampfen",
           L("Guetzli sind dünn. Schon eine Minute zu viel treibt das letzte Wasser hinaus.", "Biscuits are thin. Even a minute too long drives out the last of the water."),
           [L("Herausnehmen, wenn die Ränder gerade fest sind", "Take out when the edges have just set"), L("Auf dem Blech noch nachgaren lassen", "Let them finish on the tray")]),
         U(L("Offen oder in einer Dose mit trockenem Gebäck gelagert", "Stored open or in a tin with dry biscuits"), 3, "zucker-feuchtigkeit",
           L("Weiche Guetzli geben Feuchtigkeit an die Luft oder an trockene Nachbarn ab.", "Soft biscuits give up moisture to the air or to dry neighbours."),
           [L("Luftdicht und nach Sorten getrennt lagern", "Store airtight and by type"), L("Einen Apfelschnitz in die Dose legen", "Put an apple slice in the tin")]),
         U(L("Zu viel Mehl beim Auswallen", "Too much flour when rolling out"), 1, "mehl",
           L("Zusätzliches Mehl macht den Teig trockener und das Gebäck härter.", "Extra flour makes the dough drier and the biscuits harder."),
           [L("Zwischen zwei Backpapieren auswallen", "Roll out between two sheets of baking paper")])],
     "diagnose": tree3(L("Waren die Guetzli schon frisch aus dem Ofen hart?", "Were the biscuits already hard straight out of the oven?"),
                       L("Lagen sie offen oder zusammen mit anderen Sorten in der Dose?", "Were they stored open or in a tin with other kinds?")),
     "links": ["guetzli-lagern", "zucker-feuchtigkeit", "g-lebkuchen", "w-gebaeck"], "welten": ["w-gebaeck"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "an open tin of dry, cracked, hard Christmas biscuits next to a hammer-like rolling pin, crumbs around"},
     "quellen": [MC("Kapitel Teige und Gebäck", "Chapter on doughs and pastry")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "teig-broeckelt", "typ": "symptom", "titel": L("Guetzliteig bröckelt beim Auswallen", "Biscuit dough crumbles when rolled out"),
     "synonyme": L(["Mürbeteig bricht", "Teig reißt", "Plätzchenteig bröselig"], ["shortcrust cracks", "dough breaks apart", "crumbly cookie dough"]),
     "kurz": L("Der Teig ist zu kalt, zu trocken oder zu wenig zusammengedrückt: Die Butter hält die Krümel nicht zusammen.",
               "The dough is too cold, too dry or not pressed together enough: the butter does not hold the crumbs together."),
     "bild_im_kopf": L("Wie ein Schneeball aus Pulverschnee: Zu kalt und zu trocken, er hält nicht.", "Like a snowball made of powder snow: too cold and too dry, it will not hold."),
     "ursachen": [
         U(L("Direkt aus dem Kühlschrank zu kalt", "Too cold straight from the fridge"), 3, "temperatur",
           L("Ganz kalte Butter ist spröde und bricht statt nachzugeben.", "Very cold butter is brittle and breaks rather than giving."),
           [L("10 Minuten bei Raumtemperatur stehen lassen", "Leave at room temperature for 10 minutes"), L("Kurz mit den Händen durchkneten", "Work it briefly with your hands")]),
         U(L("Zu wenig Flüssigkeit", "Not enough liquid"), 2, "wasser",
           L("Ohne genug Ei oder Wasser verbinden sich Mehl und Fett nicht zu einem Teig.", "Without enough egg or water, flour and fat do not bind into a dough."),
           [L("Einen Esslöffel kaltes Wasser oder Eiweiß einarbeiten", "Work in a tablespoon of cold water or egg white")]),
         U(L("Zu wenig zusammengedrückt", "Not pressed together enough"), 1, "mechanik",
           L("Mürbeteig soll kaum geknetet werden, aber er muss einmal fest zusammengedrückt sein.", "Shortcrust should barely be kneaded, but it must be pressed firmly together once."),
           [L("Zu einer Kugel drücken, flach in Folie kühlen", "Press into a ball, chill flat in film")])],
     "diagnose": tree3(L("Kam der Teig direkt aus dem Kühlschrank?", "Did the dough come straight from the fridge?"),
                       L("Ist er auch nach dem Anwärmen trocken und krümelig?", "Is it dry and crumbly even after warming up?")),
     "links": ["muerbe", "teig-kuehlen", "muerbeteig-zaeh", "w-gebaeck"], "welten": ["w-gebaeck"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "a sheet of cracked, crumbling shortcrust dough under a wooden rolling pin with star cookie cutters"},
     "quellen": [MC("Kapitel Teige: Mürbeteig", "Chapter on doughs: shortcrust")], "status": "entwurf", "schwierigkeit": "einsteiger"})

# Techniken
add({"id": "teig-kuehlen", "typ": "technik", "titel": L("Guetzliteig kühlen", "Chilling biscuit dough"),
     "synonyme": L(["Teig kalt stellen", "Mürbeteig kühlen", "Teig ruhen lassen"], ["chilling dough", "resting cookie dough"]),
     "kurz": L("Butterteig vor dem Auswallen kühlen: Er klebt nicht, lässt sich sauber ausstechen und zerläuft im Ofen nicht.",
               "Chill butter dough before rolling: it does not stick, cuts out cleanly and does not spread in the oven."),
     "bild_im_kopf": L("Wie eine Tafel Schokolade im Sommer: Aus dem Kühlschrank bricht sie sauber, warm verbiegt sie sich.", "Like a chocolate bar in summer: from the fridge it snaps cleanly, warm it bends."),
     "was_passiert": L("Im Kühlschrank wird die Butter im Teig fest. Gleichzeitig nimmt das Mehl die Feuchtigkeit ganz auf, und das wenige Gluten entspannt sich. Kommen die ausgestochenen Formen kalt in den Ofen, ist der Rand schon fest, bevor die Butter schmilzt.",
                       "In the fridge the butter in the dough sets firm. At the same time the flour fully absorbs the moisture and what little gluten there is relaxes. If the cut shapes go into the oven cold, the edges set before the butter melts."),
     "warum_wichtig": L("Warmer Teig klebt am Wallholz, die Formen verziehen sich und laufen beim Backen breit.", "Warm dough sticks to the rolling pin, the shapes warp and spread during baking."),
     "schritte": L(["Teig flach drücken und in Folie mindestens eine Stunde kühlen.",
                    "Zum Auswallen 5–10 Minuten antauen lassen, wenn er bröckelt.",
                    "Zwischen zwei Backpapieren auswallen, so braucht es kein zusätzliches Mehl.",
                    "Ausgestochene Guetzli auf dem Blech nochmals 10 Minuten kühlen, dann backen."],
                   ["Press the dough flat and chill in film for at least an hour.",
                    "If it crumbles, let it soften for 5–10 minutes before rolling.",
                    "Roll out between two sheets of baking paper, so no extra flour is needed.",
                    "Chill the cut biscuits on the tray for another 10 minutes, then bake."]),
     "faustregeln": L(["Für scharfe Konturen: Guetzli kalt in den heißen Ofen."], ["For sharp outlines: cold biscuits into a hot oven."]),
     "links": ["muerbe", "kekse-breit", "teig-broeckelt", "w-gebaeck"], "welten": ["w-gebaeck"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Teige: Mürbeteig", "Chapter on doughs: shortcrust")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "guetzli-lagern", "typ": "technik", "titel": L("Guetzli richtig lagern", "Storing Christmas biscuits"),
     "synonyme": L(["Kekse aufbewahren", "Plätzchen lagern", "Guetzlidose"], ["storing cookies", "biscuit tin", "keeping biscuits fresh"]),
     "kurz": L("Knusprige und weiche Guetzli getrennt und luftdicht lagern: Feuchtigkeit wandert immer vom Feuchten zum Trockenen.",
               "Store crisp and soft biscuits separately and airtight: moisture always moves from moist to dry."),
     "bild_im_kopf": L("Wie zwei Zimmer mit offener Tür: Die Feuchtigkeit verteilt sich, bis beide gleich sind.", "Like two rooms with the door open: the moisture spreads until both are the same."),
     "was_passiert": L("Zucker zieht Feuchtigkeit an. Liegen weiche und knusprige Guetzli zusammen, geben die weichen Wasser ab: Sie werden hart, die knusprigen weich. Eine luftdichte Dose hält die Feuchtigkeit, wo sie ist.",
                       "Sugar draws in moisture. If soft and crisp biscuits share a tin, the soft ones give up water: they turn hard and the crisp ones turn soft. An airtight tin keeps the moisture where it is."),
     "warum_wichtig": L("Richtig gelagert halten die meisten Guetzli zwei bis drei Wochen, Lebkuchen deutlich länger (Richtwert).", "Stored properly, most biscuits keep two to three weeks, gingerbread considerably longer (as a guide)."),
     "schritte": L(["Guetzli ganz auskühlen lassen, sonst kondensiert Dampf in der Dose.",
                    "Jede Sorte in eine eigene, gut schließende Dose.",
                    "Weiche Guetzli und Lebkuchen mit einem Apfelschnitz lagern, ihn alle paar Tage wechseln.",
                    "Kühl lagern, aber nicht im Kühlschrank."],
                   ["Let biscuits cool completely, or steam condenses in the tin.",
                    "Each kind in its own tight-fitting tin.",
                    "Store soft biscuits and gingerbread with an apple slice, changing it every few days.",
                    "Keep somewhere cool, but not in the fridge."]),
     "faustregeln": L(["Knusprige zu knusprigen, weiche zu weichen."], ["Crisp with crisp, soft with soft."]),
     "links": ["zucker-feuchtigkeit", "guetzli-hart", "x-guetzli-apfel", "w-gebaeck"], "welten": ["w-gebaeck"], "visual": {"vorlage": "ablauf"},
     "quellen": [MC("Kapitel Zucker", "Chapter on sugar")], "status": "entwurf", "schwierigkeit": "einsteiger"})

# Begriffe
add({"id": "hirschhornsalz", "typ": "begriff", "titel": L("Hirschhornsalz", "Baker's ammonia (Hirschhornsalz)"),
     "synonyme": L(["Ammoniumhydrogencarbonat", "ABC-Trieb"], ["ammonium bicarbonate", "hartshorn"]),
     "kurz": L("Ein Triebmittel, das im Ofen zu Gas, Wasser und Ammoniak zerfällt. Es eignet sich nur für flaches, trockenes Gebäck wie Lebkuchen, weil das Ammoniak sonst nicht entweicht.",
               "A raising agent that breaks down in the oven into gas, water and ammonia. It suits only flat, dry baked goods such as gingerbread, because otherwise the ammonia cannot escape."),
     "links": ["g-lebkuchen", "triebmittel", "chemische-lockerung"], "quellen": [MC("Kapitel Brot: chemische Triebmittel", "Chapter on bread: chemical leaveners")], "status": "entwurf", "schwierigkeit": "einsteiger"})

add({"id": "pottasche", "typ": "begriff", "titel": L("Pottasche", "Potash (Pottasche)"),
     "synonyme": L(["Kaliumcarbonat"], ["potassium carbonate"]),
     "kurz": L("Ein altes Triebmittel für Honig- und Lebkuchenteige. Es braucht Säure aus dem Honig und eine lange Teigruhe und lässt Gebäck eher in die Breite als in die Höhe gehen.",
               "An old raising agent for honey and gingerbread doughs. It needs acid from the honey and a long rest, and makes baked goods spread rather than rise."),
     "links": ["g-lebkuchen", "triebmittel", "hirschhornsalz"], "quellen": [MC("Kapitel Brot: chemische Triebmittel", "Chapter on bread: chemical leaveners")], "status": "entwurf", "schwierigkeit": "einsteiger"})

# Experiment
add({"id": "x-guetzli-apfel", "typ": "experiment", "titel": L("Ein Apfelschnitz macht Lebkuchen weich", "An apple slice softens gingerbread"),
     "synonyme": L(["Lebkuchen weich machen", "Kekse weich Apfel"], ["soften gingerbread", "apple in the cookie tin"]),
     "kurz": L("Zwei gleiche Lebkuchen, einer mit Apfelschnitz in der Dose: Nach zwei Tagen ist er spürbar weicher.",
               "Two identical gingerbreads, one in a tin with an apple slice: after two days it is noticeably softer."),
     "bild_im_kopf": L("Wie ein Luftbefeuchter in einer kleinen Kammer.", "Like a humidifier in a little room."),
     "material": L(["zwei gleiche, etwas harte Lebkuchen oder Guetzli", "zwei Dosen oder Gläser mit Deckel", "ein Apfelschnitz"],
                   ["two identical, slightly hard gingerbreads or biscuits", "two tins or jars with lids", "an apple slice"]),
     "schritte": L(["In jede Dose einen Lebkuchen legen.", "In eine Dose zusätzlich den Apfelschnitz legen.", "Beide verschließen und nach zwei Tagen vergleichen: drücken und probieren."],
                   ["Put one gingerbread in each tin.", "Add the apple slice to one tin.", "Close both and compare after two days: press and taste."]),
     "beobachtung": L("Der Lebkuchen mit Apfel ist weich, der andere hart geblieben. Der Apfelschnitz ist runzlig geworden.",
                      "The gingerbread with the apple is soft, the other has stayed hard. The apple slice has gone wrinkly."),
     "erklaerung": L("Der Apfel gibt Wasser an die Luft in der Dose ab. Honig und Zucker im Lebkuchen ziehen diese Feuchtigkeit an und halten sie fest.",
                     "The apple gives off water into the air in the tin. The honey and sugar in the gingerbread draw in this moisture and hold on to it."),
     "dauer": L("2 Tage", "2 days"),
     "links": ["zucker-feuchtigkeit", "guetzli-lagern", "hygroskopisch", "g-lebkuchen"], "welten": ["w-gebaeck"],
     "visual": {"vorlage": "vergleich", "params": {"vorher": L("Tag 1", "day 1"), "nachher": L("nach 2 Tagen", "after 2 days"), "vergleich": [
         {"label": L("mit Apfelschnitz", "with apple slice"), "gefaess": "teller", "inhalt": "keins", "vorher": {"farbe": "#a0622c"}, "nachher": {"farbe": "#7a4a22"}},
         {"label": L("ohne", "without"), "gefaess": "teller", "inhalt": "keins", "vorher": {"farbe": "#a0622c"}, "nachher": {"farbe": "#b0743a", "kristalle": True}}]},
         "illustration": "two glass jars with gingerbread hearts, one also containing an apple slice"},
     "quellen": [MC("Kapitel Zucker", "Chapter on sugar")], "status": "entwurf", "schwierigkeit": "einsteiger"})

# Lernpfad
PFAD = {
    "id": "weihnachtsbaeckerei", "titel": L("Weihnachtsbäckerei verstehen", "Understanding Christmas baking"),
    "kurz": L("Vom Mürbeteig bis zum Lebkuchen: warum Guetzli zart, glänzend, weich oder knusprig werden, und wie sie es bleiben.",
              "From shortcrust to gingerbread: why biscuits turn tender, glossy, soft or crisp, and how they stay that way."),
    "fuer": L("Für alle, die im Advent backen, auch mit Kindern", "For anyone baking in Advent, children included"),
    "dauer": L("etwa 1 Stunde lesen, dann backen", "about 1 hour of reading, then bake"),
    "schritte": [
        ("muerbe", L("Fast alle Guetzli sind Mürbeteig: Fett zwischen dem Mehl macht sie zart.", "Almost all biscuits are shortcrust: fat between the flour makes them tender.")),
        ("glutenbildung", L("Warum man Guetzliteig kaum knetet, Brotteig aber lange.", "Why biscuit dough is barely kneaded but bread dough for a long time.")),
        ("teig-kuehlen", L("Kalter Teig hält die Form: der wichtigste Handgriff beim Ausstechen.", "Cold dough holds its shape: the most important step when cutting out.")),
        ("g-mailaenderli", L("Alles zusammen im Klassiker, mit Eigelb-Glanz.", "All of it together in the classic, with an egg-yolk sheen.")),
        ("g-spitzbuben", L("Hell backen und mit Pektin kleben.", "Bake pale and glue with pectin.")),
        ("schaumbildung", L("Eischnee als Baustoff: für Glasuren und Gebäck ohne Mehl.", "Whisked egg white as a building material: for glazes and flourless biscuits.")),
        ("g-zimtsterne", L("Warum die Glasur nur bei kühlem Ofen weiß bleibt.", "Why the glaze stays white only in a cool oven.")),
        ("g-brunsli", L("Kurz und heiß: außen fest, innen weich.", "Short and hot: firm outside, soft inside.")),
        ("g-chraebeli", L("Eine trockene Haut und Dampf ergeben die Füßchen.", "A dry skin plus steam makes the feet.")),
        ("triebmittel", L("Was Teige außer Hefe noch lockert.", "What else besides yeast lightens doughs.")),
        ("g-lebkuchen", L("Honig, Hirschhornsalz und lange Ruhe.", "Honey, baker's ammonia and a long rest.")),
        ("guetzli-lagern", L("Damit die Arbeit bis Weihnachten hält.", "So the work lasts until Christmas.")),
        ("g-grittibaenz", L("Zum Schluss Hefeteig für den Samichlaus.", "To finish: yeast dough for St Nicholas Day.")),
    ],
    "quiz": [
        (L("Warum knetet man Guetzliteig nur kurz?", "Why is biscuit dough kneaded only briefly?"),
         [L("Damit die Butter nicht schmilzt", "So the butter does not melt"), L("Damit wenig Gluten entsteht und die Guetzli mürbe bleiben", "So little gluten forms and the biscuits stay short"), L("Damit der Zucker sich nicht auflöst", "So the sugar does not dissolve")], 1,
         L("Kneten baut das Glutennetz. Bei Brot ist das erwünscht, bei Guetzli macht es sie zäh.", "Kneading builds the gluten network. Good for bread, but it makes biscuits tough."), "glutenbildung"),
        (L("Warum kühlt man ausgestochene Guetzli vor dem Backen nochmals?", "Why chill cut-out biscuits again before baking?"),
         [L("Damit der Rand fest wird, bevor die Butter schmilzt", "So the edges set before the butter melts"), L("Damit sie schneller backen", "So they bake faster"), L("Damit sie dunkler werden", "So they turn darker")], 0,
         L("Kalte Butter schmilzt im Ofen langsamer, die Formen bleiben scharf.", "Cold butter melts more slowly in the oven, so the shapes stay sharp."), "teig-kuehlen"),
        (L("Warum backt man Zimtsterne bei niedriger Temperatur?", "Why are cinnamon stars baked at a low temperature?"),
         [L("Damit die Mandeln nicht schmelzen", "So the almonds do not melt"), L("Damit die Glasur aus Eiweiß und Zucker nicht bräunt", "So the egg-white and sugar glaze does not brown"), L("Damit der Zimt nicht verbrennt", "So the cinnamon does not burn")], 1,
         L("Eiweiß und Zucker bräunen bei Hitze. Kühl gebacken bleibt die Glasur weiß.", "Protein and sugar brown in heat. Baked cool, the glaze stays white."), "g-zimtsterne"),
        (L("Woher haben Chräbeli ihre Füßchen?", "Where do Chräbeli get their feet?"),
         [L("Von Backpulver im Teig", "From baking powder in the dough"), L("Die trockene Haut oben hält, der Teig quillt unten heraus", "The dry skin on top holds, and the dough swells out underneath"), L("Vom Einschneiden", "From the cuts")], 1,
         L("Über Nacht trocknet oben eine Zuckerhaut. Im Ofen dehnt sich das Innere aus und kann nur unten entweichen.", "Overnight a sugar skin dries on top. In the oven the inside expands and can only escape underneath."), "g-chraebeli"),
        (L("Warum hält ein Apfelschnitz Lebkuchen weich?", "Why does an apple slice keep gingerbread soft?"),
         [L("Der Apfel gibt Feuchtigkeit ab, Honig und Zucker nehmen sie auf", "The apple gives off moisture, and honey and sugar take it up"), L("Die Säure im Apfel löst den Zucker", "The acid in the apple dissolves the sugar"), L("Der Apfel kühlt die Dose", "The apple cools the tin")], 0,
         L("Honig und Zucker ziehen Feuchtigkeit an. Der Apfel liefert sie in der geschlossenen Dose.", "Honey and sugar draw in moisture. The apple supplies it in the closed tin."), "x-guetzli-apfel"),
    ],
}

if __name__ == "__main__":
    known = {f[:-5] for f in os.listdir(f"{ROOT}/content/entries")} | {e["id"] for e in E}
    ml = json.load(open(f"{ROOT}/content/master-list.json"))
    have = {m["id"] for m in ml["eintraege"]}
    for e in E:
        de = res(e, 0)
        miss = [l for l in de.get("links", []) if l not in known]
        if miss: print("Unbekannte Links in", de["id"], miss)
        de["links"] = [l for l in de.get("links", []) if l in known]
        for m in de.get("schluesselmomente", []):
            if m.get("prinzip") and m["prinzip"] not in known: print("Unbekanntes Prinzip", de["id"], m["prinzip"])
        json.dump(de, open(f"{ROOT}/content/entries/{de['id']}.json", "w"), ensure_ascii=False, indent=2)
        if de["id"] not in have:
            ml["eintraege"].append({"id": de["id"], "typ": de["typ"], "titel": de["titel"], "status": "entwurf", "pilot": False, "links": de["links"],
                                    "welten": de.get("welten", []), "synonyme": de.get("synonyme", []), "visual": {"vorlage": de.get("visual", {}).get("vorlage", "keine")}, "verlinkt_von": []})
    ml["anzahl"] = len(ml["eintraege"])
    json.dump(ml, open(f"{ROOT}/content/master-list.json", "w"), ensure_ascii=False, indent=2)
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
    path = f"{ROOT}/content/en/_batch_weihnachten.json"
    json.dump(batch, open(path, "w"), ensure_ascii=False, indent=1)
    subprocess.check_call([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "apply", path], cwd=ROOT)
    os.remove(path)
    # Lernpfad Deutsch und Englisch
    for lang, file in ((0, "content/lernpfade.json"), (1, "content/en/lernpfade.json")):
        p = json.load(open(f"{ROOT}/{file}"))
        p = [x for x in p if x["id"] != PFAD["id"]]
        p.append({"id": PFAD["id"], "titel": PFAD["titel"][lang], "kurz": PFAD["kurz"][lang], "fuer": PFAD["fuer"][lang], "dauer": PFAD["dauer"][lang],
                  "schritte": [{"id": i, "warum": w[lang]} for i, w in PFAD["schritte"]],
                  "quiz": [{"frage": f[lang], "antworten": [a[lang] for a in an], "richtig": r, "erklaerung": er[lang], "eintrag": ei} for f, an, r, er, ei in PFAD["quiz"]]})
        json.dump(p, open(f"{ROOT}/{file}", "w"), ensure_ascii=False, indent=1)
    print(len(E), "Einträge und Lernpfad geschrieben")
