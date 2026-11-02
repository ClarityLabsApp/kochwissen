"""Übersetzung der Einträge: Texte herausziehen und wieder einsetzen.

    python3 scripts/i18n/textfelder.py extract id1 id2 ...   > batch.json   # nur Texte, kompakt
    python3 scripts/i18n/textfelder.py apply batch.json                      # schreibt content/en/entries/<id>.json

Die kompakte Form enthält nur, was übersetzt wird. Beim Einsetzen kommen alle Verweise
(ids, Diagnose-Ziele, Häufigkeiten, Farben, Temperaturen) aus dem deutschen Eintrag.
So kann eine Übersetzung den Aufbau nicht verändern.
"""
import json, sys, copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DE = ROOT / "content/entries"
EN = ROOT / "content/en/entries"

PLAIN = ["titel", "kurz", "bild_im_kopf", "bedeutung", "was_passiert", "warum_wichtig",
         "beobachtung", "erklaerung", "dauer", "sicherheit", "ergebnis", "haltbarkeit"]
LISTS = ["synonyme", "faustregeln", "typische_fehler", "schritte", "material", "verwendung"]


def extract(e):
    o = {}
    for k in PLAIN:
        if e.get(k): o[k] = e[k]
    for k in LISTS:
        if e.get(k): o[k] = e[k]
    if e.get("stellschrauben"): o["stellschrauben"] = [s["wirkung"] for s in e["stellschrauben"]]
    if e.get("rolle"): o["rolle"] = [r["rolle"] for r in e["rolle"]]
    if e.get("praxis"): o["praxis"] = [p["text"] for p in e["praxis"]]
    if e.get("ursachen"): o["ursachen"] = [{"titel": u["titel"], "warum": u["warum"], "fix": u["fix"]} for u in e["ursachen"]]
    if e.get("schluesselmomente"): o["schluesselmomente"] = [{"schritt": m["schritt"], "warum": m["warum"]} for m in e["schluesselmomente"]]
    if e.get("mythos"): o["mythos"] = e["mythos"]
    if e.get("diagnose"):
        d = {}
        for k, n in e["diagnose"].items():
            if n.get("frage"): d[k] = {"frage": n["frage"], "antworten": [a[0] for a in n.get("antworten", [])]}
        o["diagnose"] = d
    p = (e.get("visual") or {}).get("params") or {}
    v = {}
    for k in ("vorher", "nachher", "links", "rechts", "mitte", "hinweis"):
        if isinstance(p.get(k), str): v[k] = p[k]
    if isinstance(p.get("vergleich"), list): v["vergleich"] = [f.get("label", "") for f in p["vergleich"]]
    for k in ("skala", "schwellen_c", "fette"):
        if isinstance(p.get(k), list) and p[k] and isinstance(p[k][0], dict) and "name" in p[k][0]:
            v[k] = [m["name"] for m in p[k]]
    if v: o["visual"] = v
    return o


def apply(e, t):
    """Kompakte Übersetzung t über den deutschen Eintrag e legen; nur Übersetztes kommt in die Datei."""
    out = {"id": e["id"]}
    def same_len(k, a, b):
        if len(a) != len(b): raise SystemExit(f"{e['id']}: {k} hat {len(a)} statt {len(b)} Elemente")
    for k in PLAIN + LISTS:
        if k in t:
            if k in LISTS: same_len(k, t[k], e.get(k, [])) if k != "synonyme" else None
            out[k] = t[k]
    if "stellschrauben" in t:
        same_len("stellschrauben", t["stellschrauben"], e["stellschrauben"])
        out["stellschrauben"] = [{**s, "wirkung": w} for s, w in zip(e["stellschrauben"], t["stellschrauben"])]
    if "rolle" in t:
        same_len("rolle", t["rolle"], e["rolle"])
        out["rolle"] = [{**r, "rolle": w} for r, w in zip(e["rolle"], t["rolle"])]
    if "praxis" in t:
        same_len("praxis", t["praxis"], e["praxis"])
        out["praxis"] = [{**p, "text": w} for p, w in zip(e["praxis"], t["praxis"])]
    if "ursachen" in t:
        same_len("ursachen", t["ursachen"], e["ursachen"])
        out["ursachen"] = []
        for u, w in zip(e["ursachen"], t["ursachen"]):
            same_len("ursachen.fix", w["fix"], u["fix"])
            out["ursachen"].append({**u, "titel": w["titel"], "warum": w["warum"], "fix": w["fix"]})
    if "schluesselmomente" in t:
        same_len("schluesselmomente", t["schluesselmomente"], e["schluesselmomente"])
        out["schluesselmomente"] = [{**m, "schritt": w["schritt"], "warum": w["warum"]} for m, w in zip(e["schluesselmomente"], t["schluesselmomente"])]
    if "mythos" in t: out["mythos"] = t["mythos"]
    if "diagnose" in t:
        d = copy.deepcopy(e["diagnose"])
        for k, w in t["diagnose"].items():
            n = d[k]
            same_len(f"diagnose.{k}", w["antworten"], n.get("antworten", []))
            n["frage"] = w["frage"]
            n["antworten"] = [[lbl, a[1]] for lbl, a in zip(w["antworten"], n["antworten"])]
        out["diagnose"] = d
    if "visual" in t:
        p = copy.deepcopy((e.get("visual") or {}).get("params") or {})
        w = t["visual"]
        for k in ("vorher", "nachher", "links", "rechts", "mitte", "hinweis"):
            if k in w: p[k] = w[k]
        if "vergleich" in w:
            same_len("visual.vergleich", w["vergleich"], p["vergleich"])
            for f, lbl in zip(p["vergleich"], w["vergleich"]): f["label"] = lbl
        for k in ("skala", "schwellen_c", "fette"):
            if k in w:
                same_len(f"visual.{k}", w[k], p[k])
                for m, name in zip(p[k], w[k]): m["name"] = name
        out["visual"] = {"params": p}
    return out


def main():
    cmd = sys.argv[1]
    if cmd == "extract":
        res = {}
        for i in sys.argv[2:]:
            res[i] = extract(json.loads((DE / f"{i}.json").read_text()))
        print(json.dumps(res, ensure_ascii=False, indent=1))
    elif cmd == "apply":
        EN.mkdir(parents=True, exist_ok=True)
        batch = json.loads(Path(sys.argv[2]).read_text())
        for i, t in batch.items():
            e = json.loads((DE / f"{i}.json").read_text())
            missing = [k for k in extract(e) if k not in t]
            if missing: print(f"Hinweis: {i} ohne Übersetzung für {', '.join(missing)}", file=sys.stderr)
            (EN / f"{i}.json").write_text(json.dumps(apply(e, t), ensure_ascii=False, indent=2) + "\n")
        print(f"{len(batch)} Übersetzungen geschrieben.")


if __name__ == "__main__":
    main()
