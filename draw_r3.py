#!/usr/bin/env python3
"""Round 3 — ONE DAY ON EARTH, Saturday 21 November 2026.
Draws a 1024x1024 newspaper front page with PIL. Own design; lessons from the
top-5 study (correct hero facts/dates, legible numbers strip, pictorial hero
art, complete also-list, real wire sources only, verification badges).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------- palette ----------
PAPER   = (250, 246, 236)   # warm cream
INK     = (20, 20, 20)
RED     = (178, 34, 34)
DARKRED = (140, 20, 20)
NAVY    = (18, 32, 62)
TEAL    = (210, 232, 225)
SKY     = (200, 222, 235)
SAND    = (232, 220, 196)
MAPSEA  = (205, 225, 235)
MAPLAND = (222, 205, 165)
GREY    = (90, 90, 90)
RULE    = (60, 60, 60)

# ---------- fonts (Liberation = Times-like newspaper feel) ----------
FDIR = "/usr/share/fonts/truetype/liberation"
def F(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)

SERIF_B  = lambda s: F("LiberationSerif-Bold.ttf", s)
SERIF    = lambda s: F("LiberationSerif-Regular.ttf", s)
SERIF_I  = lambda s: F("LiberationSerif-Italic.ttf", s)
SANS     = lambda s: F("LiberationSans-Regular.ttf", s)
SANS_B   = lambda s: F("LiberationSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

MX = 22                      # side margin
CW = W - 2 * MX              # content width = 980

def text_w(s, font):
    return d.textlength(s, font=font)

def wrap(s, font, maxw):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def rule(y, wdt=2, color=RULE):
    d.line([(MX, y), (W - MX, y)], fill=color, width=wdt)

def center(s, y, font, color=INK):
    d.text(((W - text_w(s, font)) / 2, y), s, font=font, fill=color)

def badge(x, y, label, color):
    """small verification badge; returns width used"""
    f = SANS_B(8)
    w = int(text_w(label, f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 12], radius=2, fill=color)
    d.text((x + 5, y + 1), label, font=f, fill=(255, 255, 255))
    return w

# ============================================================ top
# red rule + kicker
d.rectangle([0, 0, W, 4], fill=RED)
d.text((MX, 12), "ONE DAY ON EARTH", font=SANS_B(15), fill=RED)
rk = "35 STORIES  •  7 REGIONS  •  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
d.text((W - MX - text_w(rk, SANS_B(11)), 14), rk, font=SANS_B(11), fill=INK)
rule(34)

# masthead
center("Saturday 21 November 2026", 40, SERIF_B(62), INK)
# subtitle
center("COP31 runs into overtime  •  Three missiles downed over Riyadh  •  A 6.7 quake shakes Peru",
       112, SERIF_I(16), INK)
rule(134)

# ============================================================ numbers strip (6 numbers)
nums = [
    ("13", "DAY OF COP31, MEANT TO CLOSE ON DAY 12"),
    ("3", "MISSILES SHOT DOWN OVER RIYADH"),
    ("6.7", "MAGNITUDE OF THE PERU QUAKE"),
    ("146", "PEOPLE SAFE AFTER THE DAVAO LANDING"),
    ("$58,810", "BITCOIN EARLY SATURDAY, DOWN 4.1% IN A DAY"),
    ("124*", "K L RAHUL'S SCORE AT TEA IN WELLINGTON"),
]
ny0, ny1 = 140, 196
colw = CW / 6
for i, (n, lab) in enumerate(nums):
    x0 = MX + i * colw
    if i:
        d.line([(x0, ny0 + 4), (x0, ny1 - 4)], fill=(180, 170, 150), width=1)
    cx = x0 + colw / 2
    d.text((cx - text_w(n, SERIF_B(30)) / 2, ny0), n, font=SERIF_B(30), fill=RED)
    for j, ln in enumerate(wrap(lab, SANS_B(8), colw - 14)):
        d.text((cx - text_w(ln, SANS_B(8)) / 2, ny0 + 34 + j * 10), ln,
               font=SANS_B(8), fill=INK)
rule(200)

# ============================================================ region bar
# proportional widths, but a minimum segment width so every label stays legible
regs = [("EUROPE", 4, (30, 90, 160)), ("ASIA", 10, (178, 34, 34)),
        ("MIDDLE EAST", 5, (150, 110, 20)), ("AFRICA", 1, (40, 120, 70)),
        ("AMERICAS", 11, (110, 60, 140)), ("OCEANIA", 3, (20, 120, 120)),
        ("GLOBAL", 1, (110, 110, 110))]
# hand-tuned widths (sum = CW): small regions get a floor of 56px, taken from
# the two largest segments, so "AFRICA 1" and "GLOBAL 1" are never clipped.
regw = [112, 252, 140, 56, 280, 84, 56]
rx = MX
ry0, ry1 = 204, 224
for (name, cnt, col), segw in zip(regs, regw):
    d.rectangle([rx, ry0, rx + segw - 1, ry1], fill=col)
    lab = f"{name} {cnt}"
    f = SANS_B(10)
    d.text((rx + (segw - text_w(lab, f)) / 2, ry0 + 4), lab, font=f, fill=(255, 255, 255))
    rx += segw
rule(228)

# ============================================================ heroes (3 cards)
heroes = [
    dict(
        label="COP31: OVERTIME", place="1  ANTALYA, TURKIYE  •  CLIMATE",
        head="Climate summit runs into overtime with no deal",
        body="COP31 missed its Friday close; a draft with no mention of fossil fuels split nearly 200 countries. A third text is promised Saturday morning. (AP, Al Jazeera)",
        badge=("CONFIRMED", (20, 120, 60)), art="cop31"),
    dict(
        label="SAUDI: MISSILES", place="2  RIYADH  •  WAR",
        head="Three Houthi missiles shot down over Riyadh",
        body="The Saudi-led coalition said three ballistic missiles were destroyed before dawn, a day after it bombed Hodeidah port. (AFP, Reuters)",
        badge=("OFFICIAL", (30, 90, 160)), art="riyadh"),
    dict(
        label="PERU: QUAKE 6.7", place="3  CENTRAL PERU  •  EARTHQUAKE",
        head="Magnitude 6.7 earthquake shakes central Peru",
        body="The deep quake near Carhuamayo was felt in Lima and along the coast; the institute reported no deaths, damage or tsunami risk. (USGS, IGP)",
        badge=("OFFICIAL", (30, 90, 160)), art="peru"),
]

def art_cop31(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=TEAL)
    # globe
    cx, cy, r = x0 + 62, y0 + 68, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 200))
    d.ellipse([cx - 26, cy - 30, cx + 6, cy - 2], fill=(90, 180, 90))
    d.ellipse([cx - 4, cy + 8, cx + 30, cy + 34], fill=(90, 180, 90))
    d.ellipse([cx - 30, cy + 14, cx - 8, cy + 32], fill=(90, 180, 90))
    # thermometer
    tx = x0 + 150
    d.rectangle([tx, y0 + 22, tx + 14, y0 + 92], fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([tx + 3, y0 + 58, tx + 11, y0 + 90], fill=RED)
    d.ellipse([tx - 6, y0 + 88, tx + 20, y0 + 112], fill=RED, outline=INK, width=2)
    d.text((tx - 8, y0 + 118), "1.5°C", font=SANS_B(13), fill=RED)
    # clock (overtime)
    kx, ky, kr = x0 + 240, y0 + 62, 34
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255), outline=INK, width=2)
    d.line([(kx, ky), (kx, ky - 22)], fill=INK, width=3)
    d.line([(kx, ky), (kx + 16, ky + 8)], fill=INK, width=3)
    d.text((kx - 26, y0 + 108), "DAY 13", font=SANS_B(12), fill=INK)

def art_riyadh(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    # moon
    d.ellipse([x0 + w - 52, y0 + 14, x0 + w - 22, y0 + 44], fill=(240, 235, 200))
    # skyline
    import random
    random.seed(7)
    bx = x0
    while bx < x0 + w - 30:
        bw = random.randint(26, 44)
        bh = random.randint(38, 88)
        d.rectangle([bx, y0 + h - bh, bx + bw, y0 + h], fill=(10, 18, 40))
        for wy in range(y0 + h - bh + 8, y0 + h - 6, 12):
            for wx in range(bx + 5, bx + bw - 4, 10):
                if random.random() < 0.5:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
        bx += bw + 4
    # missile trails: dotted arcs + bursts
    for (sx, sy, ex, ey) in [(x0 + 30, y0 + h - 10, x0 + 120, y0 + 22),
                             (x0 + 150, y0 + h - 10, x0 + 230, y0 + 30)]:
        for t in range(0, 11):
            px = sx + (ex - sx) * t / 10
            py = sy + (ey - sy) * t / 10 - 18 * (t / 10) * (1 - t / 10) * 4
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 220, 120))
        # burst
        bx2, by2 = ex, ey
        for dx, dy in [(0, -9), (0, 9), (-9, 0), (9, 0), (-6, -6), (6, 6), (-6, 6), (6, -6)]:
            d.line([(bx2, by2), (bx2 + dx, by2 + dy)], fill=(255, 220, 120), width=2)
    d.text((x0 + 10, y0 + 8), "3 SHOT DOWN", font=SANS_B(12), fill=(255, 255, 255))

def art_peru(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(245, 225, 190))
    # mountains
    d.polygon([(x0, y0 + h), (x0 + 80, y0 + 28), (x0 + 160, y0 + h)], fill=(150, 120, 90))
    d.polygon([(x0 + 120, y0 + h), (x0 + 210, y0 + 40), (x0 + 300, y0 + h)], fill=(120, 95, 70))
    # houses
    for hx in (x0 + 30, x0 + 120, x0 + 215):
        d.rectangle([hx, y0 + h - 42, hx + 52, y0 + h - 8], fill=(200, 90, 60))
        d.polygon([(hx - 4, y0 + h - 42), (hx + 26, y0 + h - 62), (hx + 56, y0 + h - 42)],
                  fill=(90, 60, 40))
        d.rectangle([hx + 20, y0 + h - 26, hx + 32, y0 + h - 8], fill=(60, 40, 30))
    # seismograph trace
    pts = []
    import math
    for i in range(0, w, 6):
        x = x0 + i
        y = y0 + 26 + (14 * math.sin(i / 9) if 40 < i < 90 or 200 < i < 250 else 3 * math.sin(i / 5))
        pts.append((x, y))
    d.line(pts, fill=RED, width=3)
    d.text((x0 + 10, y0 + 6), "00:09 UTC  •  108 KM DEEP", font=SANS_B(11), fill=INK)

ART = {"cop31": art_cop31, "riyadh": art_riyadh, "peru": art_peru}

hy0 = 234
cardw = (CW - 18) // 3
for i, hs in enumerate(heroes):
    x0 = MX + i * (cardw + 9)
    x1 = x0 + cardw
    # illustration
    ART[hs["art"]](x0, hy0, cardw, 132)
    # red label bar
    ly = hy0 + 132
    d.rectangle([x0, ly, x1, ly + 20], fill=RED)
    d.text((x0 + 8, ly + 4), hs["label"], font=SANS_B(12), fill=(255, 255, 255))
    # place line
    py = ly + 24
    d.text((x0, py), hs["place"], font=SANS_B(9), fill=RED)
    # headline
    hy = py + 14
    hl = wrap(hs["head"], SERIF_B(20), cardw)
    for j, ln in enumerate(hl[:3]):
        d.text((x0, hy + j * 23), ln, font=SERIF_B(20), fill=INK)
    by = hy + len(hl[:3]) * 23 + 2
    bl = wrap(hs["body"], SANS(11), cardw)
    for j, ln in enumerate(bl[:3]):
        d.text((x0, by + j * 13), ln, font=SANS(11), fill=INK)
    # badge bottom-right of card
    badge(x1 - 78, hy0 + 132 + 20 + 14 + len(hl[:3]) * 23 + len(bl[:3]) * 13 + 2,
          hs["badge"][0], hs["badge"][1])
rule(516)

# ============================================================ secondary grid (10 cards, 5x2)
secs = [
    ("KRYVYI RIH", "4  KRYVYI RIH  •  WAR", "Russian double strike kills 2, injures 42",
     "Two missiles hit a restaurant car park; drones struck again as rescuers worked. (Kyiv Independent)", "CONFIRMED", (20, 120, 60), "kryvyi"),
    ("KYIV WARNING", "5  KYIV  •  WAR", "Zelensky: Crimea bridge \u201cwill not stay\u201d",
     "He warns of double-tap strikes in an NBC interview. (NBC)", "REPORTED", (180, 120, 30), "kyiv"),
    ("HORMUZ: DRONE", "6  STRAIT OF HORMUZ  •  WAR", "Iran says it downed a US drone",
     "Tehran claims the shootdown; Washington has not confirmed it. (IRIB)", "REPORTED", (180, 120, 30), "drone"),
    ("IRAN: URANIUM", "7  TEHRAN  •  DIPLOMACY", "Iran: uranium stock stays at home",
     "Minister still seeks a \u201cfair solution\u201d. (ToI)", "OFFICIAL", (30, 90, 160), "atom"),
    ("TRUMP: AI TAX", "8  WASHINGTON  •  TECHNOLOGY", "Trump vows tax on data centres abroad",
     "\u201cTremendous\u201d penalty promised; no details yet. (ABC)", "REPORTED", (180, 120, 30), "pct"),
    ("CHINA\u2013JAPAN", "9  BEIJING  •  DIPLOMACY", "China tells Japan to \u201ccorrect\u201d Taiwan words",
     "Tokyo says its stance is unchanged. (Ministry, AFP)", "OFFICIAL", (30, 90, 160), "flags"),
    ("DAVAO: 146 SAFE", "10  DAVAO  •  AVIATION", "Jet lands safely after engine fire alert",
     "Air Niugini 767 diverts after midnight; all 146 aboard safe. (AP)", "OFFICIAL", (30, 90, 160), "plane"),
    ("CANBERRA: AI", "11  CANBERRA  •  DIPLOMACY", "Australia and China agree to AI talks",
     "Albanese ends an 11-day trip. (ABC)", "OFFICIAL", (30, 90, 160), "talks"),
    ("BITCOIN: $58,810", "12  WORLD  •  MARKETS", "Bitcoin slips below $59,000",
     "Down 4.1% in 24 hours; ether $1,619. (CoinGecko)", "CONFIRMED", (20, 120, 60), "btc"),
    ("RAHUL: 124*", "13  WELLINGTON  •  CRICKET", "Rahul century puts India on top",
     "India 344 for 2 at tea, replying to 368. (AFP)", "CONFIRMED", (20, 120, 60), "cricket"),
]

def mini(x0, y0, w, h, kind):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(235, 228, 210))
    if kind == "kryvyi":
        d.rectangle([x0 + 14, y0 + 18, x0 + 44, y0 + h - 4], fill=(90, 90, 90))
        d.rectangle([x0 + 52, y0 + 26, x0 + 78, y0 + h - 4], fill=(120, 120, 120))
        for fy in (y0 + 6, y0 + 12):
            d.polygon([(x0 + 26, fy), (x0 + 32, fy + 12), (x0 + 20, fy + 12)], fill=(255, 120, 0))
            d.polygon([(x0 + 62, fy), (x0 + 68, fy + 12), (x0 + 56, fy + 12)], fill=(255, 80, 0))
    elif kind == "kyiv":
        d.rectangle([x0, y0 + 8, x0 + w, y0 + h // 2], fill=(40, 110, 200))
        d.rectangle([x0, y0 + h // 2, x0 + w, y0 + h - 8], fill=(255, 210, 60))
        d.ellipse([x0 + w - 30, y0 + 6, x0 + w - 8, y0 + 28], fill=(60, 60, 60))
        d.rectangle([x0 + w - 20, y0 + 28, x0 + w - 18, y0 + h - 6], fill=(60, 60, 60))
    elif kind == "drone":
        d.rectangle([x0, y0 + h - 16, x0 + w, y0 + h], fill=(70, 140, 180))
        cx, cy = x0 + w // 2, y0 + h // 2 - 4
        d.ellipse([cx - 16, cy - 6, cx + 16, cy + 6], fill=(50, 50, 50))
        d.line([(cx - 26, cy - 8), (cx + 26, cy - 8)], fill=(50, 50, 50), width=3)
        d.line([(cx - 26, cy + 8), (cx + 26, cy + 8)], fill=(50, 50, 50), width=3)
        d.ellipse([cx - 4, cy - 14, cx + 4, cy - 6], fill=RED)
    elif kind == "atom":
        cx, cy = x0 + w // 2, y0 + h // 2
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        for a in (0, 60, 120):
            import math
            pts = []
            for t in range(0, 360, 10):
                r = math.radians(t)
                px = cx + 26 * math.cos(r) * math.cos(math.radians(a)) - 12 * math.sin(r) * math.sin(math.radians(a))
                py = cy + 26 * math.cos(r) * math.sin(math.radians(a)) + 12 * math.sin(r) * math.cos(math.radians(a))
                pts.append((px, py))
            d.line(pts, fill=(30, 90, 160), width=2)
    elif kind == "pct":
        d.text((x0 + w // 2 - 18, y0 + 4), "%", font=SERIF_B(34), fill=(30, 90, 160))
        d.rectangle([x0 + 12, y0 + h - 12, x0 + w - 12, y0 + h - 6], fill=(90, 90, 90))
    elif kind == "flags":
        d.rectangle([x0 + 12, y0 + 8, x0 + w // 2 - 2, y0 + h - 10], fill=(200, 30, 30))
        for sx, sy in [(x0 + 18, y0 + 13), (x0 + 28, y0 + 17), (x0 + 18, y0 + 22)]:
            d.polygon([(sx, sy - 3), (sx + 2, sy + 2), (sx - 3, sy + 1), (sx + 3, sy + 1), (sx - 2, sy + 2)],
                      fill=(255, 220, 60))
        d.rectangle([x0 + w // 2 + 2, y0 + 8, x0 + w - 12, y0 + h - 10], fill=(255, 255, 255), outline=INK, width=1)
        d.ellipse([x0 + w // 2 + 14, y0 + h // 2 - 9, x0 + w // 2 + 32, y0 + h // 2 + 9], fill=(200, 30, 30))
    elif kind == "plane":
        d.rectangle([x0, y0 + h - 14, x0 + w, y0 + h], fill=(120, 180, 220))
        cx, cy = x0 + w // 2, y0 + h // 2
        d.polygon([(cx - 34, cy), (cx + 30, cy - 6), (cx + 40, cy), (cx + 30, cy + 6)], fill=(40, 60, 90))
        d.polygon([(cx - 6, cy - 4), (cx + 4, cy - 18), (cx + 12, cy - 4)], fill=(40, 60, 90))
        d.polygon([(cx - 6, cy + 4), (cx + 4, cy + 16), (cx + 12, cy + 4)], fill=(40, 60, 90))
    elif kind == "talks":
        d.rectangle([x0 + 20, y0 + 10, x0 + w - 20, y0 + h - 12], fill=(210, 200, 170))
        d.polygon([(x0 + 20, y0 + 10), (x0 + w // 2, y0 - 2), (x0 + w - 20, y0 + 10)], fill=(140, 40, 40))
        for wx in range(x0 + 28, x0 + w - 28, 12):
            d.rectangle([wx, y0 + 20, wx + 6, y0 + 32], fill=(60, 60, 60))
    elif kind == "btc":
        cx, cy = x0 + w // 2 - 18, y0 + h // 2
        d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(240, 180, 40), outline=(150, 100, 0), width=2)
        d.text((cx - 8, cy - 13), "B", font=SERIF_B(24), fill=(255, 255, 255))
        pts = [(x0 + w - 34, y0 + 8), (x0 + w - 22, y0 + 20), (x0 + w - 12, y0 + 16),
               (x0 + w - 2, y0 + 34)]
        d.line(pts, fill=RED, width=3)
    elif kind == "cricket":
        d.line([(x0 + 16, y0 + h - 10), (x0 + w - 40, y0 + 12)], fill=(150, 110, 60), width=7)
        d.ellipse([x0 + w - 34, y0 + 8, x0 + w - 16, y0 + 26], fill=(200, 40, 40))
        d.text((x0 + 14, y0 + h - 20), "124*", font=SANS_B(13), fill=RED)

sy0 = 522
sgw = (CW - 24) // 5
sgh = 128
for idx, (lab, place, head, body, bdg, bcol, kind) in enumerate(secs):
    r, c = divmod(idx, 5)
    x0 = MX + c * (sgw + 6)
    y0 = sy0 + r * (sgh + 6)
    x1 = x0 + sgw
    mini(x0, y0, sgw, 46, kind)
    ly = y0 + 46
    d.rectangle([x0, ly, x1, ly + 15], fill=RED)
    d.text((x0 + 5, ly + 2), lab, font=SANS_B(9), fill=(255, 255, 255))
    py = ly + 18
    d.text((x0, py), place, font=SANS_B(8), fill=RED)
    hy = py + 11
    hl = wrap(head, SERIF_B(13), sgw)
    for j, ln in enumerate(hl[:2]):
        d.text((x0, hy + j * 15), ln, font=SERIF_B(13), fill=INK)
    by = hy + len(hl[:2]) * 15 + 1
    bl = wrap(body, SANS(9), sgw)
    for j, ln in enumerate(bl[:2]):
        d.text((x0, by + j * 11), ln, font=SANS(9), fill=INK)
rule(790)

# ============================================================ bottom: map + also list
by0 = 796
d.text((MX, by0), "WHERE IT HAPPENED", font=SANS_B(12), fill=RED)
d.text((MX + 352, by0), "ALSO ON SATURDAY 21 NOVEMBER  —  22 MORE STORIES", font=SANS_B(12), fill=RED)
mapx, mapy, mapw, maph = MX, by0 + 18, 336, 152
d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=MAPSEA, outline=RULE, width=1)
# continents (rough polygons)
land = [
    [(22, 28), (62, 18), (102, 24), (112, 44), (92, 58), (72, 74), (46, 68), (26, 54)],   # N America
    [(76, 86), (106, 86), (116, 106), (100, 132), (80, 126), (70, 100)],                    # S America
    [(166, 30), (186, 24), (196, 40), (180, 56), (166, 50)],                                 # Europe
    [(166, 62), (196, 62), (206, 86), (190, 116), (170, 106), (160, 80)],                   # Africa
    [(202, 26), (282, 20), (312, 36), (300, 62), (270, 76), (230, 70), (210, 50)],           # Asia
    [(272, 106), (302, 106), (306, 126), (276, 126)],                                        # Australia
]
for poly in land:
    d.polygon([(mapx + px, mapy + py) for px, py in poly], fill=MAPLAND, outline=(150, 130, 95))
# numbered dots for stories 1-11 and 13 (12 = Bitcoin, global, no dot)
dots = {1: (196, 46), 2: (216, 70), 3: (82, 100), 4: (182, 38), 5: (184, 32),
        6: (226, 68), 7: (232, 60), 8: (96, 46), 9: (276, 46), 10: (286, 86),
        11: (292, 116), 13: (314, 130)}
for n, (px, py) in dots.items():
    x, y = mapx + px, mapy + py
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=RED, outline=(255, 255, 255), width=1)
    d.text((x - 4 if n < 10 else x - 7, y - 6), str(n), font=SANS_B(9), fill=(255, 255, 255))
d.text((MX, by0 + 18 + maph + 4), "Red numbers mark stories 1\u201313. No. 12 is Bitcoin \u2014 a global market.",
       font=SANS(8), fill=GREY)

# also list, two columns
also = [
    (14, "Kryvyi Rih: strike kills 2, injures 42", "Kyiv Indp."),
    (15, "Copenhagen: Russian attache expelled", "Al Jazeera"),
    (16, "Antalya: EU warns COP31 risks \u201cfossil summit\u201d", "AFP"),
    (17, "Antalya: Panama may block climate text", "Al Jazeera"),
    (18, "Antalya: PLN signs 6 clean-power deals", "Antara"),
    (19, "Yemen: Houthis threaten Jeddah, Red Sea", "Al Jazeera"),
    (20, "Washington: Vance: Iran strikes Trump's call", "Reuters"),
    (21, "Washington: lawmaker threatens SpaceX funds", "CNN"),
    (22, "Texas: execution of man, 70, takes 63 min", "ABC"),
    (23, "Los Angeles: jury convicts Palisades arsonist", "ABC"),
    (24, "Missouri: judge OKs $7.25bn Roundup deal", "AFP"),
    (25, "Vancouver: Canada rests climate-trial defence", "AFP"),
    (26, "Pyongyang: Kim tours factories, no Trump talks", "AFP"),
    (27, "Sejong: freight train derails, no one hurt", "Korea Herald"),
    (28, "Taipei: budget and cash payout passed", "Taipei Times"),
    (29, "Bangkok: arsenic plan for two rivers", "The Nation"),
    (30, "New Delhi: Pakistani minister joins SCO forum", "Dawn"),
    (31, "E. India: rain alerts as Akvan remnants move in", "ETV"),
    (32, "Myanmar: groups urge sanctions after ruling", "AP"),
    (33, "Port Louis: rating agency talks to 15 states", "Al Jazeera"),
    (34, "Melbourne: Cummins keeps Australia captaincy", "ABC"),
    (35, "Las Vegas: Verstappen to stewards after contact", "Autosport"),
]
lx0 = MX + 352
col2w = 318
for i, (n, t, src) in enumerate(also):
    col = 0 if i < 11 else 1
    row = i if i < 11 else i - 11
    x = lx0 + col * (col2w + 8)
    y = by0 + 18 + row * 14
    d.text((x, y), str(n), font=SANS_B(9), fill=RED)
    line = f"{t} ({src})"
    f = SANS(9)
    if text_w(line, f) > col2w - 18:
        f = SANS(8)
    d.text((x + 18, y), line, font=f, fill=INK)

# ============================================================ DATE CHECK + footer
dy0 = 978
d.rectangle([MX, dy0, W - MX, dy0 + 30], outline=RED, width=2)
d.text((MX + 8, dy0 + 3), "DATE CHECK", font=SANS_B(11), fill=RED)
dc = ("Left out as earlier news: ICJ Myanmar genocide ruling (Thu 19 Nov)  •  FBI NCIC breach, first reported Fri 20 Nov (CNN)  •  "
      "Friday's Kyiv barrage  •  AI sell-off close  •  Riemann claim  •  Nikhil Gupta verdict  •  Shenzhen summit  •  Egypt IMF deal.")
for j, ln in enumerate(wrap(dc, SANS(9), CW - 110)):
    d.text((MX + 92, dy0 + 3 + j * 11), ln, font=SANS(9), fill=INK)
d.text((MX, 1012), "Every story here happened, or was first reported, on Saturday 21 November 2026. Sources named beside each story. Original drawings.",
       font=SANS(8), fill=GREY)
d.text((W - MX - text_w("HOW WE CHECKED: CONFIRMED = 2+ outlets  •  OFFICIAL = on the record  •  REPORTED = one outlet", SANS(8)), 1012),
       "HOW WE CHECKED: CONFIRMED = 2+ outlets  •  OFFICIAL = on the record  •  REPORTED = one outlet",
       font=SANS(8), fill=GREY)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
