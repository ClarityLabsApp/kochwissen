"""Illustrationen freistellen: PNG mit Papierhintergrund -> WebP mit transparentem Hintergrund.

    python3 scripts/freistellen.py                      # alle PNGs in public/illustrationen
    CLOSE=12 python3 scripts/freistellen.py datei.png  # Umriss stärker schließen (z. B. bei hellen Gläsern)

Durchsichtig wird nur Papierfläche, die vom Bildrand her zusammenhängt. Helle Stellen im Motiv bleiben.
Danach PNG löschen."""
import glob, os, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
files = sys.argv[1:] or sorted(glob.glob("public/illustrationen/*.png"))
for p in files:
    im = Image.open(p).convert("RGB")
    small = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    rgb = np.asarray(small).astype(np.float32)
    border = np.concatenate([rgb[:6].reshape(-1,3), rgb[-6:].reshape(-1,3), rgb[:, :6].reshape(-1,3), rgb[:, -6:].reshape(-1,3)])
    bg = np.median(border, axis=0)
    # Papierstruktur glätten, dann Abstand zur Papierfarbe
    blur = nd.uniform_filter(rgb, size=(5, 5, 1))
    d = np.sqrt(((blur - bg) ** 2).sum(-1))
    paperlike = d < 22
    lab, n = nd.label(paperlike)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bgmask = np.isin(lab, edge[edge > 0])
    fg = ~bgmask
    # Krümel entfernen: nur große zusammenhängende Motivteile behalten
    fl, fn = nd.label(fg)
    if fn:
        sizes = nd.sum(fg, fl, range(1, fn + 1)); keep = np.zeros(fn + 1, bool); keep[1:] = sizes >= max(400, sizes.max() * 0.004)
        fg = keep[fl]
    fg = nd.binary_fill_holes(fg)
    fg = nd.binary_closing(fg, iterations=int(os.environ.get("CLOSE", "2")))
    fg = nd.binary_fill_holes(fg)
    # weicher Rand
    alpha = Image.fromarray((fg * 255).astype(np.uint8)).resize(im.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.6))
    o = im.convert("RGBA"); o.putalpha(alpha)
    bb = alpha.point(lambda v: 255 if v > 10 else 0).getbbox()
    if bb:
        m = 24; x0, y0, x1, y1 = bb
        o = o.crop((max(0, x0 - m), max(0, y0 - m), min(o.width, x1 + m), min(o.height, y1 + m)))
    a = np.asarray(o).copy(); a[a[..., 3] < 8, :3] = 0; o = Image.fromarray(a, "RGBA")
    o.thumbnail((800, 800), Image.LANCZOS)
    o.save(p[:-4] + ".webp", "WEBP", quality=82)
    print(os.path.basename(p), o.size, "Motiv", round(fg.mean(), 2))
