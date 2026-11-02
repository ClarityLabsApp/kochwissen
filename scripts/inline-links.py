"""Verlinkt verwandte Einträge direkt im Text: erstes Vorkommen des Titels wird zu [[id|Wort]].
Die Chip-Liste „Verwandte Einträge“ blendet so verlinkte Einträge aus (EntryView).
Aufruf: python3 scripts/inline-links.py [--dry]"""
import json, glob, os, re, sys

DRY = "--dry" in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERM = re.compile(r"\[\[[a-z0-9-]+(?:\|[^\]]+)?\]\]")
L = "A-Za-zÄÖÜäöüß"

de = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f"{ROOT}/content/entries/*.json")}
en = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f"{ROOT}/content/en/entries/*.json")}

def phrases(e):
    t = e.get("titel", "")
    out = {t, re.sub(r"\s*\(.*?\)", "", t).strip()}
    m = re.search(r"\((.*?)\)", t)
    if m and len(m.group(1)) >= 5 and "," not in m.group(1) and de.get(e.get("id", ""), e).get("typ") in ("prozess", "technik"): out.add(m.group(1))
    return sorted((p for p in out if len(p) >= 4), key=len, reverse=True)

def fields(e):
    """(Pfad, Text) in Lesereihenfolge; nur Fließtexte."""
    for k in ["was_passiert", "warum_wichtig", "erklaerung", "beobachtung", "bedeutung"]:
        if isinstance(e.get(k), str): yield (k,), e[k]
    for i, s in enumerate(e.get("faustregeln") or []):
        if isinstance(s, str): yield ("faustregeln", i), s
    for i, s in enumerate(e.get("schluesselmomente") or []):
        if isinstance(s, dict) and isinstance(s.get("warum"), str): yield ("schluesselmomente", i, "warum"), s["warum"]

def setp(e, path, val):
    o = e
    for p in path[:-1]: o = o[p]
    o[path[-1]] = val

def link_once(text, pat, rid):
    spans = [(m.start(), m.end()) for m in TERM.finditer(text)]
    for m in pat.finditer(text):
        if any(a <= m.start() < b for a, b in spans): continue
        return text[:m.start()] + f"[[{rid}|{m.group(0)}]]" + text[m.end():]
    return None

total = 0
for lang, store, titles in (("de", de, de), ("en", en, en)):
    for eid, e in store.items():
        base = de[eid]
        rel = [r for r in (base.get("links") or []) if r != eid]
        if not rel: continue
        changed = False
        blob = json.dumps(e, ensure_ascii=False)
        for rid in rel:
            if f"[[{rid}" in blob: continue
            src = titles.get(rid) or (de.get(rid) if lang == "de" else None)
            if not src: continue
            for ph in phrases(src):
                pat = re.compile(rf"(?<![{L}]){re.escape(ph)}(?:e|en|n|s|es)?(?![{L}])", re.I)
                done = False
                for path, txt in fields(e):
                    new = link_once(txt, pat, rid)
                    if new:
                        setp(e, path, new); changed = done = True; total += 1
                        if DRY: print(lang, eid, "→", rid, ":", re.search(r"\[\[" + rid + r"\|[^\]]+\]\]", new).group(0))
                        break
                if done: break
            blob = json.dumps(e, ensure_ascii=False)
        if changed and not DRY:
            path = f"{ROOT}/content/entries/{eid}.json" if lang == "de" else f"{ROOT}/content/en/entries/{eid}.json"
            json.dump(e, open(path, "w"), ensure_ascii=False, indent=2); open(path, "a").write("\n")
print("Links gesetzt:", total)
