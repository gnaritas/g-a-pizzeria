#!/usr/bin/env python3
"""og.png 1200x630 — G&A Pizzeria: plate-rim gold ring on ink, New Yorks stamp motif.
Opening badge (November 2026), NAP line. Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

INK = (35, 25, 17); CREAM = (247, 241, 228); GOLD = (201, 151, 63); GOLD_L = (229, 197, 141)
TOMATO = (184, 53, 42); FAINT = (213, 190, 152)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

serif = lambda s: font(["Iowan Old Style.ttc", "Palatino.ttc", "Georgia.ttf", "Times New Roman.ttf"], s)
sans = lambda s: font(["Futura.ttc", "HelveticaNeve.ttc", "HelveticaNeue.ttc", "Arial.ttf"], s)

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img, "RGBA")

# vertical warm wash
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(INK[0] + int(22 * (1 - t)), INK[1] + int(15 * (1 - t)), INK[2] + int(9 * (1 - t))))
d.ellipse((-360, -320, 520, 560), fill=(TOMATO[0], TOMATO[1], TOMATO[2], 36))
d.ellipse((760, 300, 1460, 1000), fill=(GOLD[0], GOLD[1], GOLD[2], 30))

# double rule frame (menu-card)
d.rectangle((26, 26, W - 26, H - 26), outline=GOLD_L, width=2)
d.rectangle((36, 36, W - 36, H - 36), outline=GOLD, width=1)

# right plate: double-ring plate with slice silhouette
cx, cy, r = 952, 315, 178
d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD, width=3)
d.ellipse((cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16), outline=GOLD_L, width=2)
# slice wedge (apex at plate center, arc along inner ring)
ri = r - 40
a0, a1 = math.radians(-32), math.radians(38)
pts = [(cx, cy)]
steps = 42
for i in range(steps + 1):
    a = a0 + (a1 - a0) * i / steps
    pts.append((int(cx + ri * math.cos(a)), int(cy + ri * math.sin(a))))
d.polygon(pts, fill=(TOMATO[0], TOMATO[1], TOMATO[2], 210))
# crust arc on outer inner-ring
d.arc((cx - ri, cy - ri, cx + ri, cy + ri), start=-32, end=38, fill=GOLD_L, width=14)
# pepperoni dots on wedge
for (ang, rr) in [(-14, 0.55), (4, 0.72), (22, 0.5), (12, 0.3), (-4, 0.42)]:
    a = math.radians(ang); rad = ri * rr
    px, py = cx + rad * math.cos(a), cy + rad * math.sin(a)
    d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=(140, 32, 24, 235))

# left text block
tx = 96
d.text((tx, 108), "O P E N I N G   N O V E M B E R   2 0 2 6", font=sans(21), fill=GOLD)
d.text((tx, 146), "G&A", font=serif(128), fill=CREAM)
d.text((tx, 292), "PIZZERIA", font=sans(52), fill=TOMATO)
d.text((tx, 372), "A new pizzeria from the chef and owner", font=serif(29), fill=CREAM)
d.text((tx, 410), "of Stefano's Ristorante — in the former", font=serif(29), fill=CREAM)
d.text((tx, 448), "Nino's Pizza & Pasta building.", font=serif(29), fill=CREAM)
d.line([(tx, 502), (tx + 500, 502)], fill=GOLD, width=3)
d.text((tx, 520), "840 N PARK ROAD", font=sans(22), fill=FAINT)
d.text((tx, 550), "WYOMISSING, PENNSYLVANIA 19610", font=sans(22), fill=FAINT)

# tomato badge bottom-right of text column — sign wording verbatim
bw, bh = 250, 74
badge = Image.new("RGBA", (bw + 24, bh + 24), (0, 0, 0, 0))
bd = ImageDraw.Draw(badge)
bd.rounded_rectangle((12, 12, 12 + bw, 12 + bh), radius=16, fill=TOMATO)
bd.text((bw // 2 + 12, bh // 2 + 12 - 14), "C O M I N G", font=sans(20), fill=(247, 241, 228, 200), anchor="mm")
bd.text((bw // 2 + 12, bh // 2 + 12 + 12), "S O O N", font=sans(30), fill=(247, 241, 228, 255), anchor="mm")
badge = badge.rotate(-2.5, expand=True, resample=Image.BICUBIC)
bw2, bh2 = badge.size
img.paste(badge, (888, 462), badge.convert("RGBA"))

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")
