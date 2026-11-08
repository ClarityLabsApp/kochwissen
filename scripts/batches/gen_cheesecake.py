"""Einzeleintrag: Cheesecake bekommt Risse (Wunsch von Phil, 8. November 2026)."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_batch_welten2 import L, res, MC, ROOT, U, tree3  # noqa: E402

E = []
add = E.append
ATK = {"titel": "America's Test Kitchen: Toning Down Tomato Sauce", "url": "https://www.americastestkitchen.com/how_tos/6605-toning-down-tomato-sauce"}

add({"id": "cheesecake-reisst", "typ": "symptom", "titel": L("Cheesecake bekommt Risse", "Cheesecake cracks on top"),
     "synonyme": L(["Käsekuchen reißt", "Cheesecake Risse", "Käsekuchen Risse oben", "Quarkkuchen reißt", "Cheesecake fällt zusammen", "Cheesecake Wasserbad"],
                   ["cracked cheesecake", "cheesecake cracking", "cheesecake sinks", "cheesecake water bath"]),
     "kurz": L("Cheesecake ist eine Eiercreme: Wird er zu heiß gebacken, zu schnell abgekühlt oder schaumig geschlagen, zieht sich das Ei zusammen und die Oberfläche reißt.",
               "Cheesecake is an egg custard: baked too hot, cooled too fast or beaten too airy, the egg contracts and the top cracks."),
     "bild_im_kopf": L("Wie eine Schlammpfütze in der Sonne: Sie trocknet aus, schrumpft und reißt in Schollen auf.",
                       "Like a mud puddle in the sun: it dries out, shrinks and cracks into plates."),
     "ursachen": [
         U(L("Zu heiß oder zu lange gebacken", "Baked too hot or too long"), 3, "eiweiss-gerinnung",
           L("Überhitztes Eiweiß wird steif und drückt Wasser hinaus. Die Masse kann nicht mehr nachgeben, wenn sie beim Abkühlen schrumpft.",
             "Overheated egg protein turns stiff and squeezes out water. The filling can no longer give way as it shrinks while cooling."),
           [L("Sanft backen, um 150 bis 160 °C (Richtwert)", "Bake gently, around 150 to 160 °C (as a guide)"),
            L("Herausnehmen, wenn der Rand fest ist und die Mitte noch wackelt: innen etwa 65 bis 70 °C", "Take it out when the edge is set and the centre still wobbles: about 65 to 70 °C inside"),
            L("Ein Wasserbad hält die Hitze sanft und gleichmäßig", "A water bath keeps the heat gentle and even")]),
         U(L("Zu schnell abgekühlt", "Cooled too quickly"), 2, "nachgaren",
           L("Beim Abkühlen schrumpft der Kuchen. Klebt der Rand an der Form oder kühlt er schlagartig ab, reißt die Mitte auseinander.",
             "The cake shrinks as it cools. If the edge sticks to the tin or it cools abruptly, the middle tears apart."),
           [L("Ofen ausschalten, Tür einen Spalt öffnen und den Kuchen darin auskühlen lassen", "Switch off the oven, open the door a crack and let the cake cool inside"),
            L("Gleich nach dem Backen mit einem Messer am Rand entlangfahren", "Run a knife around the edge straight after baking")]),
         U(L("Zu viel Luft eingerührt", "Too much air beaten in"), 2, "aufschlagen",
           L("Schaumig geschlagene Masse geht im Ofen auf wie ein Soufflé und fällt beim Abkühlen zusammen. Dabei reißt die Oberfläche.",
             "Batter beaten until foamy rises in the oven like a soufflé and collapses as it cools. The top cracks as it does."),
           [L("Frischkäse und Eier bei Raumtemperatur verwenden, dann glatt wird es auch ohne Schlagen", "Use cream cheese and eggs at room temperature; then it turns smooth without beating"),
            L("Auf niedriger Stufe nur verrühren, bis alles verbunden ist", "Mix on low speed only until everything is combined")])],
     "diagnose": tree3(L("War der Kuchen beim Herausnehmen schon in der Mitte ganz fest?", "Was the cake already completely firm in the centre when you took it out?"),
                       L("Ging er im Ofen hoch auf und sank beim Abkühlen wieder ein?", "Did it rise high in the oven and sink again as it cooled?")),
     "faustregeln": L(["Für eine glatte Oberfläche: Herausnehmen, solange die Mitte noch wackelt, weil sie beim Abkühlen nachgart und fest wird.",
                       "Langsam abkühlen lassen, erst im offenen Ofen, dann bei Raumtemperatur, erst danach in den Kühlschrank.",
                       "Ist er trotzdem gerissen: ganz auskühlen lassen und mit Früchten, Rahm oder gesüßtem Sauerrahm bedecken."],
                      ["For a smooth top: take it out while the centre still wobbles, because it carries on cooking and sets as it cools.",
                       "Cool it slowly, first in the open oven, then at room temperature, and only then in the fridge.",
                       "If it cracks anyway: let it cool completely and cover it with fruit, whipped cream or sweetened sour cream."]),
     "links": ["eiweiss-gerinnung", "wasserbad", "nachgaren", "kuchen-sinkt-ein", "kerntemperatur", "w-eier"], "welten": ["w-gebaeck", "w-eier"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "a round baked cheesecake in a springform pan with a long crack across its golden top, a wooden spoon and a kitchen thermometer beside it"},
     "quellen": [{"titel": "King Arthur Baking: Why did my cheesecake crack?", "url": "https://www.kingarthurbaking.com/blog/2024/05/09/why-did-my-cheesecake-crack"},
                 MC("Kapitel Eier: Eiercremes", "Chapter on eggs: custards")],
     "status": "entwurf", "schwierigkeit": "einsteiger"})


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
        if isinstance(src, list) and not isinstance(shape, list): return src[0]
        return src
    batch = {e["id"]: pick(ex[e["id"]], res(e, 1)) for e in E}
    path = f"{ROOT}/content/en/_batch_cheesecake.json"
    json.dump(batch, open(path, "w"), ensure_ascii=False, indent=1)
    subprocess.check_call([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "apply", path], cwd=ROOT)
    os.remove(path)
    print(len(E), "Einträge geschrieben")
