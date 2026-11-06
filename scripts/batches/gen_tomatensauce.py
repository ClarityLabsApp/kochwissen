"""Einzeleintrag: Tomatensauce schmeckt sauer (Wunsch von Phil, 6. November 2026)."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_batch_welten2 import L, res, MC, ROOT, U, tree3  # noqa: E402

E = []
add = E.append
ATK = {"titel": "America's Test Kitchen: Toning Down Tomato Sauce", "url": "https://www.americastestkitchen.com/how_tos/6605-toning-down-tomato-sauce"}

add({"id": "tomatensauce-sauer", "typ": "symptom", "titel": L("Tomatensauce schmeckt sauer", "Tomato sauce tastes sour"),
     "synonyme": L(["Tomatensugo sauer", "Sugo zu sauer", "Dosentomaten sauer", "Tomaten Säure", "Tomatensauce Säure neutralisieren", "Tomatensauce Natron", "Tomatensauce Zucker", "Pelati sauer"],
                   ["tomato sauce too acidic", "sour tomato sauce", "canned tomatoes acidic", "reduce acidity tomato sauce", "baking soda tomato sauce"]),
     "kurz": L("Tomaten enthalten viel Säure, Dosentomaten oft zusätzlich Zitronensäure: Süße, Fett und Röstaromen gleichen sie aus, eine Prise Natron neutralisiert sie.",
               "Tomatoes contain a lot of acid, and canned tomatoes often have added citric acid: sweetness, fat and roasted flavours balance it, and a pinch of baking soda neutralises it."),
     "bild_im_kopf": L("Wie ein zu helles Licht im Zimmer: Man kann es dimmen (Natron) oder warme Lampen dazustellen (Zucker, Fett), dann blendet es nicht mehr.",
                       "Like a light that is too bright in a room: you can dim it (baking soda) or add warm lamps around it (sugar, fat), and then it no longer glares."),
     "ursachen": [
         U(L("Zu kurz gekocht, Tomatenmark nicht angeröstet", "Cooked too briefly, tomato paste not roasted"), 3, "geschmack-balance",
           L("Die Säure verkocht nicht. Aber angeröstetes Tomatenmark und langes Köcheln bringen Süße und Röstaromen, die die Säure runder wirken lassen.",
             "The acid does not cook away. But roasted tomato paste and long simmering add sweetness and roasted flavours that make the acid seem rounder."),
           [L("Tomatenmark in Öl anrösten, bis es dunkelrot wird", "Fry the tomato paste in oil until it turns dark red"),
            L("Die Sauce mindestens 20 bis 30 Minuten leise köcheln lassen", "Simmer the sauce gently for at least 20 to 30 minutes")]),
         U(L("Saure Tomaten oder zugesetzte Zitronensäure", "Sour tomatoes or added citric acid"), 3, "saeure",
           L("Viele Dosentomaten enthalten Zitronensäure (E 330) für die Haltbarkeit. Auch unreife Tomaten sind saurer.",
             "Many canned tomatoes contain citric acid (E330) to keep them safe. Underripe tomatoes are also more acidic."),
           [L("Eine Prise Zucker, eine geriebene Karotte oder etwas Ketchup: Sie überdecken die Säure mit Süße", "A pinch of sugar, a grated carrot or a little ketchup: they cover the acid with sweetness"),
            L("Oder eine Messerspitze Natron pro Dose: Es neutralisiert die Säure und schäumt kurz auf", "Or a knife tip of baking soda per tin: it neutralises the acid and briefly fizzes"),
            L("Beim Einkauf Dosen ohne Zitronensäure wählen", "When shopping, choose tins without citric acid")]),
         U(L("Zu wenig Fett und Salz", "Too little fat and salt"), 2, "salz-geschmack",
           L("Fett und Salz dämpfen den spitzen Eindruck der Säure. Ohne sie steht die Säure allein im Vordergrund.",
             "Fat and salt soften the sharp impression of acid. Without them the acid stands alone in the foreground."),
           [L("Am Schluss ein Stück Butter oder einen Schuss Olivenöl einrühren", "Stir in a knob of butter or a splash of olive oil at the end"),
            L("Salzen und erneut probieren, bevor man Zucker nimmt", "Salt and taste again before reaching for sugar")])],
     "diagnose": tree3(L("Hast du Tomatenmark angeröstet und die Sauce mindestens 20 Minuten gekocht?", "Did you roast tomato paste and simmer the sauce for at least 20 minutes?"),
                       L("Steht auf der Dose Zitronensäure oder E 330, oder waren die Tomaten unreif?", "Does the tin list citric acid or E330, or were the tomatoes underripe?")),
     "faustregeln": L(["Zucker und Karotte überdecken die Säure, Natron entfernt sie: Natron nur in kleinsten Mengen, zu viel schmeckt seifig und macht die Sauce flach.",
                       "Ketchup bringt Zucker und Umami, aber auch Essig: Bei sehr saurer Sauce lieber Zucker oder Karotte nehmen.",
                       "Immer in kleinen Schritten nachwürzen und probieren: Was drin ist, bekommt man nicht mehr heraus."],
                      ["Sugar and carrot cover the acid, baking soda removes it: use baking soda only in tiny amounts, too much tastes soapy and makes the sauce flat.",
                       "Ketchup brings sugar and umami, but also vinegar: for a very sour sauce, sugar or carrot is the better choice.",
                       "Always adjust in small steps and taste: what is in cannot be taken out again."]),
     "links": ["saeure", "natron", "geschmack-balance", "abschmecken-saeure", "suess", "salz-geschmack", "w-saucen"], "welten": ["w-saucen", "w-gemuese"],
     "visual": {"vorlage": "entscheidungsbaum", "illustration": "an open tin of peeled tomatoes next to a small pot of red tomato sauce, a carrot, a sugar bowl and a small dish of baking soda"},
     "quellen": [ATK, {"titel": "The Takeout: The fix for acidic canned tomatoes", "url": "https://thetakeout.com/1695996/fix-acidic-canned-tomatoes-baking-soda"},
                 MC("Kapitel Früchte und Gemüse: Tomaten", "Chapter on fruits and vegetables: tomatoes")],
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
    path = f"{ROOT}/content/en/_batch_tomate.json"
    json.dump(batch, open(path, "w"), ensure_ascii=False, indent=1)
    subprocess.check_call([sys.executable, f"{ROOT}/scripts/i18n/textfelder.py", "apply", path], cwd=ROOT)
    os.remove(path)
    print(len(E), "Einträge geschrieben")
