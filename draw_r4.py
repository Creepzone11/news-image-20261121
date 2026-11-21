#!/usr/bin/env python3
"""ONE DAY ON EARTH — round 4, Saturday 21 November 2026.

Draws the front page (1024x1024 PNG) with PIL. Fresh code for round 4:
scene-like art in every mid card, a de-collided numbered map, a fully dated
DATE CHECK, and the verified 35-story set from round 3 (same facts, no
19/20 Nov story promoted). Bitcoin keeps $58,810 — CoinGecko 01:30 UTC
21 Nov (verified by web search; the $58,983 in the top entries matches no
21 Nov snapshot).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (176, 30, 30)
DARKRED = (140, 20, 20)
NAVY = (13, 27, 58)
GREY = (110, 108, 100)
LIGHT = (233, 228, 214)

FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    try:
        return ImageFont.truetype(FD + name, size)
    except OSError:
        return ImageFont.truetype(FD + "DejaVuSans.ttf", size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

def rrect(x, y, w, h, r, fill=None, outline=None, width=1):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=width)

def badge(x, y, label, bg):
    f = SANS_B(11)
    w = d.textlength(label, font=f) + 12
    rrect(x, y, w, 16, 3, fill=bg)
    d.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return w

BADGE_BG = {"CONFIRMED": (34, 120, 60), "OFFICIAL": (31, 92, 168), "REPORTED": (176, 110, 20)}

# ---------------------------------------------------------------- top matter
d.rectangle([0, 0, W, 5], fill=RED)
text(14, 12, "ONE DAY ON EARTH", SANS_B(20), fill=RED)
text(1010, 14, "35 STORIES  \u00b7  7 REGIONS  \u00b7  13 PICTURED  \u00b7  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
     SANS_B(13), fill=INK, anchor="ra")
text(512, 34, "Saturday 21 November 2026", SERIF_B(62), anchor="ma")
text(512, 100, "COP31 runs into overtime  \u00b7  Three missiles downed over Riyadh  \u00b7  A 6.7 quake shakes Peru",
     SERIF_I(19), anchor="ma")
d.line([14, 122, 1010, 122], fill=INK, width=2)

# ---------------------------------------------------------------- numbers strip
NUMBERS = [
    ("13", "DAY OF COP31, MEANT TO\nCLOSE ON DAY 12"),
    ("5", "MISSILES SHOT DOWN OVER\nRIYADH AND JIZAN"),
    ("6.7", "MAGNITUDE OF\nTHE PERU QUAKE"),
    ("146", "PEOPLE SAFE AFTER\nTHE DAVAO LANDING"),
    ("$58,810", "BITCOIN EARLY SATURDAY,\nDOWN 4.1% IN A DAY"),
    ("124*", "K L RAHUL'S SCORE\nAT TEA IN WELLINGTON"),
]
cw = 996 / 6
for i, (num, lab) in enumerate(NUMBERS):
    x = 14 + i * cw
    if i:
        d.line([x - 3, 130, x - 3, 168], fill=(200, 195, 180), width=1)
    text(x + cw / 2, 124, num, SERIF_B(32), fill=RED, anchor="ma")
    for j, ln in enumerate(lab.split("\n")):
        text(x + cw / 2, 156 + j * 11, ln, SANS_B(10), anchor="ma")

# ---------------------------------------------------------------- region bar
# Widths proportional to counts, but with a floor so every label fits.
REGIONS = [("EUROPE 4", (31, 92, 168), 4), ("ASIA 10", (176, 30, 30), 10),
           ("MIDDLE EAST 5", (176, 130, 30), 5), ("AFRICA 1", (46, 125, 60), 1),
           ("AMERICAS 11", (110, 60, 140), 11), ("OCEANIA 3", (20, 130, 130), 3),
           ("GLOBAL 1", (110, 110, 110), 1)]
widths = [996 * n / 35 for _, _, n in REGIONS]
widths = [max(w, 64) if n <= 1 else max(w, 88) if n == 3 else w
          for w, (_, _, n) in zip(widths, REGIONS)]
excess = sum(widths) - 996
widths[4] -= excess * 0.6
widths[1] -= excess * 0.4
rx = 14
for (name, col, n), w in zip(REGIONS, widths):
    d.rectangle([rx, 180, rx + w - 1, 200], fill=col)
    text(rx + w / 2, 184, name, SANS_B(11), fill=(255, 255, 255), anchor="ma")
    rx += w

# ---------------------------------------------------------------- hero art
def art_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(207, 232, 228))
    # globe
    cx, cy, r = x + 52, y + 50, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 123, 213), outline=(30, 80, 160), width=2)
    d.ellipse([cx - 22, cy - 18, cx - 2, cy + 2], fill=(80, 180, 90))
    d.ellipse([cx - 6, cy + 8, cx + 20, cy + 26], fill=(80, 180, 90))
    d.ellipse([cx + 8, cy - 24, cx + 24, cy - 8], fill=(80, 180, 90))
    # fat thermometer
    tx = x + 150
    rrect(tx, y + 12, 18, 62, 9, fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([tx + 4, y + 34, tx + 14, y + 70], fill=(220, 40, 40))
    d.ellipse([tx - 6, y + 66, tx + 24, y + 96], fill=(220, 40, 40), outline=INK, width=2)
    text(tx + 26, y + 30, "1.5\u00b0C", SANS_B(13), fill=DARKRED)
    text(tx + 26, y + 46, "LIMIT", SANS_B(11), fill=INK)
    text(tx + 26, y + 60, "AT RISK", SANS_B(11), fill=INK)
    # clock with bold hands + DAY 13 tag
    kx, ky, kr = x + 262, y + 46, 30
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255), outline=INK, width=3)
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([kx + 24 * math.sin(a), ky - 24 * math.cos(a),
                kx + 28 * math.sin(a), ky - 28 * math.cos(a)], fill=INK, width=2)
    d.line([kx, ky, kx - 14, ky - 14], fill=INK, width=4)
    d.line([kx, ky, kx + 4, ky - 20], fill=INK, width=4)
    d.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=INK)
    rrect(kx - 30, y + 82, 60, 15, 3, fill=NAVY)
    text(kx, y + 84, "DAY 13", SANS_B(10), fill=(255, 255, 255), anchor="ma")

def art_riyadh(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # stars
    for sx, sy in [(30, 14), (90, 22), (150, 10), (210, 18), (280, 12), (60, 40), (180, 34)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 220))
    mx, my = x + 272, y + 22
    d.ellipse([mx - 14, my - 14, mx + 14, my + 14], fill=(255, 240, 180))
    d.ellipse([mx - 6, my - 16, mx + 20, my + 12], fill=NAVY)
    # skyline
    base = y + h
    for bx, bw, bh in [(0, 44, 34), (48, 36, 52), (88, 52, 42), (144, 40, 60),
                       (188, 46, 38), (238, 38, 54), (280, 46, 44)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(22, 41, 77))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(x + bx + 7, x + bx + bw - 6, 12):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
    # missile trails: dotted arcs to star bursts
    for (x0, y0, x1, y1) in [(40, 78, 120, 18), (150, 82, 220, 14), (240, 76, 300, 30)]:
        for t in range(0, 11):
            px = x + x0 + (x1 - x0) * t / 10
            py = y + y0 + (y1 - y0) * t / 10 - 14 * math.sin(math.pi * t / 10)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 200, 80))
        bx, by = x + x1, y + y1 - 6
        for a in range(8):
            ang = math.pi * a / 4
            d.line([bx, by, bx + 11 * math.cos(ang), by + 11 * math.sin(ang)], fill=(255, 210, 60), width=3)
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 230, 120))
    # count pill, top-left
    pill = "5 SHOT DOWN"
    f = SANS_B(11)
    pw = d.textlength(pill, font=f) + 14
    rrect(x + 8, y + 6, pw, 17, 8, fill=(255, 255, 255), outline=RED, width=1)
    d.text((x + 15, y + 8), pill, font=f, fill=RED)

def art_peru(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 192))
    # mountains
    d.polygon([(x, y + h), (x + 90, y + 22), (x + 180, y + h)], fill=(150, 120, 80))
    d.polygon([(x + 130, y + h), (x + 240, y + 30), (x + 326, y + h)], fill=(120, 95, 62))
    d.polygon([(x + 78, y + 34), (x + 90, y + 22), (x + 104, y + 36)], fill=(255, 255, 255))
    # seismograph line
    pts = []
    px = x + 8
    while px < x + w - 8:
        pts.append((px, y + 16 + (10 if (px // 14) % 2 else -8)))
        px += 7
    d.line(pts, fill=(200, 30, 30), width=3)
    # houses
    for hx in (x + 30, x + 140, x + 240):
        d.rectangle([hx, y + 66, hx + 52, y + 96], fill=(230, 200, 160), outline=(120, 80, 40), width=1)
        d.polygon([(hx - 4, y + 66), (hx + 26, y + 46), (hx + 56, y + 66)], fill=(176, 60, 30))
        d.rectangle([hx + 20, y + 80, hx + 32, y + 96], fill=(90, 60, 30))
    # pill
    pill = "00:09 UTC  \u00b7  108 KM DEEP"
    f = SANS_B(11)
    pw = d.textlength(pill, font=f) + 14
    rrect(x + 8, y + 6, pw, 17, 8, fill=(255, 255, 255), outline=RED, width=1)
    d.text((x + 15, y + 8), pill, font=f, fill=RED)

HEROES = [
    ("COP31: OVERTIME", "1  ANTALYA, T\u00dcRKIYE  \u00b7  CLIMATE",
     "Climate summit runs into overtime with no deal",
     "A draft with no mention of fossil fuels split nearly 200 countries after the Friday close; a third text is promised Saturday morning. (AP, Al Jazeera)",
     "CONFIRMED", art_cop31),
    ("SAUDI: MISSILES", "2  RIYADH  \u00b7  WAR",
     "Three Houthi missiles shot down over Riyadh",
     "Three ballistic missiles were destroyed over Riyadh before dawn and two more over Jizan, the coalition said, a day after it bombed Hodeidah port. (AFP, Reuters)",
     "OFFICIAL", art_riyadh),
    ("PERU: QUAKE 6.7", "3  CENTRAL PERU  \u00b7  EARTHQUAKE",
     "Magnitude 6.7 earthquake shakes central Peru",
     "The deep quake near Carhuamayo was felt in Lima and along the coast; the institute reported no deaths, damage or tsunami risk. (USGS, IGP)",
     "OFFICIAL", art_peru),
]
hy, hh_art = 206, 100
for i, (label, loc, head, body, bd, art) in enumerate(HEROES):
    x = 14 + i * 335
    w = 326
    art(x, hy, w, hh_art)
    d.rectangle([x, hy + hh_art, x + w, hy + hh_art + 22], fill=RED)
    text(x + 8, hy + hh_art + 3, label, SANS_B(13), fill=(255, 255, 255))
    # verification badge as a pill at the right end of the label bar
    bf = SANS_B(10)
    bw = d.textlength(bd, font=bf) + 12
    rrect(x + w - bw - 6, hy + hh_art + 4, bw, 14, 7, fill=BADGE_BG[bd], outline=(255, 255, 255), width=1)
    d.text((x + w - bw, hy + hh_art + 6), bd, font=bf, fill=(255, 255, 255))
    text(x, hy + hh_art + 26, loc, SANS_B(11), fill=RED)
    hl = wrap(head, SERIF_B(19), w)
    for j, ln in enumerate(hl[:2]):
        text(x, hy + hh_art + 42 + j * 22, ln, SERIF_B(19))
    bl = wrap(body, SERIF(12), w)
    for j, ln in enumerate(bl[:3]):
        text(x, hy + hh_art + 88 + j * 15, ln, SERIF(12))

# ---------------------------------------------------------------- mid-card art
# Every mid card gets a small PICTORIAL SCENE (not a bare glyph).

def art_kryvyi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 228, 232))
    # building
    d.rectangle([x + 58, y + 14, x + 132, y + h], fill=(140, 140, 145))
    d.rectangle([x + 58, y + 14, x + 132, y + 20], fill=(110, 110, 115))
    for wy in range(y + 24, y + h - 4, 9):
        for wx in range(x + 64, x + 128, 12):
            d.rectangle([wx, wy, wx + 6, wy + 5], fill=(60, 60, 70))
    # flames on the roof
    for fx, fh in [(66, 16), (82, 22), (98, 14), (114, 20)]:
        d.polygon([(x + fx, y + 14), (x + fx + 7, y + 14 - fh), (x + fx + 14, y + 14)],
                  fill=(240, 120, 20))
        d.polygon([(x + fx + 3, y + 14), (x + fx + 7, y + 14 - fh + 8), (x + fx + 11, y + 14)],
                  fill=(250, 200, 40))
    # smoke
    for sx, sy, sr in [(70, 2, 7), (86, -2, 9), (106, 0, 7)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr], fill=(120, 120, 125))
    # red casualty badge
    rrect(x + 8, y + h - 18, 120, 15, 3, fill=RED)
    text(x + 14, y + h - 16, "12 KILLED \u00b7 42 HURT", SANS_B(10), fill=(255, 255, 255))

def art_kyiv(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    # flag band
    d.rectangle([x, y, x + w, y + 12], fill=(0, 91, 187))
    d.rectangle([x, y + 12, x + w, y + 24], fill=(255, 213, 0))
    # person at a desk with a microphone
    d.ellipse([x + 88, y + 26, x + 106, y + 44], fill=(240, 200, 160))  # head
    d.polygon([(x + 78, y + 48), (x + 116, y + 48), (x + 122, y + h), (x + 72, y + h)],
              fill=(40, 60, 110))  # shoulders / suit
    d.rectangle([x + 40, y + h - 12, x + 154, y + h], fill=(120, 80, 50))  # desk
    d.line([x + 140, y + h - 12, x + 150, y + 30], fill=INK, width=2)  # mic stand
    d.ellipse([x + 146, y + 24, x + 156, y + 34], fill=INK)  # mic

def art_hormuz(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 222, 236))
    # sea
    d.rectangle([x, y + 34, x + w, y + h], fill=(70, 130, 180))
    d.arc([x + 10, y + 36, x + 50, y + 48], 180, 360, fill=(255, 255, 255), width=2)
    d.arc([x + 120, y + 38, x + 160, y + 50], 180, 360, fill=(255, 255, 255), width=2)
    # ship
    d.polygon([(x + 40, y + 30), (x + 150, y + 30), (x + 140, y + 44), (x + 52, y + 44)],
              fill=(40, 40, 50))
    for cx, col in [(58, (200, 60, 40)), (82, (40, 120, 200)), (106, (220, 170, 40))]:
        d.rectangle([x + cx, y + 16, x + cx + 20, y + 30], fill=col)
    d.rectangle([x + 132, y + 12, x + 148, y + 30], fill=(230, 230, 230))
    # drone above
    dx, dy = x + 168, y + 12
    d.ellipse([dx - 5, dy - 3, dx + 5, dy + 3], fill=(30, 30, 35))
    d.line([dx - 12, dy - 6, dx + 12, dy - 6], fill=(30, 30, 35), width=2)
    d.line([dx - 12, dy + 6, dx + 12, dy + 6], fill=(30, 30, 35), width=2)
    d.line([dx, dy - 6, dx, dy + 6], fill=(30, 30, 35), width=1)

def art_iran(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 214))
    # atom symbol: three rotated elliptical orbits + nucleus
    ax, ay = x + 158, y + 22
    for deg in (0, 60, 120):
        a = math.radians(deg)
        pts = []
        for t in range(0, 65):
            th = 2 * math.pi * t / 64
            ex, ey = 22 * math.cos(th), 9 * math.sin(th)
            rx = ex * math.cos(a) - ey * math.sin(a)
            ry = ex * math.sin(a) + ey * math.cos(a)
            pts.append((ax + rx, ay + ry))
        d.line(pts, fill=(31, 92, 168), width=2)
    d.ellipse([ax - 4, ay - 4, ax + 4, ay + 4], fill=(31, 92, 168))
    # podium + speaker
    d.ellipse([x + 62, y + 18, x + 80, y + 36], fill=(240, 200, 160))
    d.polygon([(x + 52, y + 40), (x + 90, y + 40), (x + 96, y + h), (x + 46, y + h)],
              fill=(60, 60, 70))
    d.polygon([(x + 30, y + 40), (x + 112, y + 40), (x + 106, y + h), (x + 36, y + h)],
              fill=(120, 85, 50))
    d.line([x + 100, y + 40, x + 110, y + 26], fill=INK, width=2)
    d.ellipse([x + 106, y + 21, x + 114, y + 29], fill=INK)

def art_trump(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 32, 64))
    # data-centre building with lit server rows
    d.rectangle([x + 18, y + 8, x + 130, y + h], fill=(38, 54, 96))
    for ry in range(y + 14, y + h - 6, 10):
        for rx in range(x + 26, x + 124, 12):
            col = (90, 220, 120) if (rx + ry) % 24 else (255, 200, 60)
            d.rectangle([rx, ry, rx + 6, ry + 5], fill=col)
    # big % badge
    d.ellipse([x + 140, y + 8, x + 186, y + 46], fill=RED, outline=(255, 255, 255), width=2)
    text(x + 163, y + 12, "%", SANS_B(26), fill=(255, 255, 255), anchor="ma")

def art_chinajapan(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 214))
    # China flag
    d.rectangle([x + 16, y + 10, x + 76, y + 34], fill=(222, 41, 16))
    for sx, sy in [(28, 16), (40, 14), (46, 22), (38, 28)]:
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 222, 0))
    d.line([x + 16, y + 10, x + 16, y + h], fill=INK, width=2)
    # Japan flag
    d.rectangle([x + 118, y + 10, x + 178, y + 34], fill=(255, 255, 255), outline=INK, width=1)
    d.ellipse([x + 138, y + 14, x + 158, y + 30], fill=(188, 0, 45))
    d.line([x + 178, y + 10, x + 178, y + h], fill=INK, width=2)
    # small podium between
    d.polygon([(x + 84, y + 36), (x + 110, y + 36), (x + 106, y + h), (x + 88, y + h)],
              fill=(120, 85, 50))

def art_davao(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 226, 240))
    # runway
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(90, 90, 95))
    for rx in range(x + 8, x + w - 8, 18):
        d.rectangle([rx, y + h - 6, rx + 9, y + h - 4], fill=(255, 255, 255))
    # plane
    px, py = x + 40, y + 22
    d.ellipse([px, py - 7, px + 90, py + 7], fill=(245, 245, 245), outline=(80, 80, 90), width=1)
    d.polygon([(px + 78, py - 6), (px + 108, py - 16), (px + 112, py - 6)], fill=(200, 40, 40))
    d.polygon([(px + 40, py + 4), (px + 62, py + 18), (px + 74, py + 4)], fill=(180, 180, 190))
    d.ellipse([px + 6, py - 3, px + 16, py + 3], fill=(70, 130, 180))
    # green check
    d.ellipse([x + 158, y + 6, x + 186, y + 34], fill=(34, 120, 60))
    d.line([x + 164, y + 20, x + 170, y + 27, x + 181, y + 13], fill=(255, 255, 255), width=3)

def art_canberra(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 214))
    # parliament building with columns
    d.rectangle([x + 52, y + 22, x + 142, y + h], fill=(245, 242, 230), outline=(150, 140, 120), width=1)
    d.polygon([(x + 46, y + 22), (x + 97, y + 6), (x + 148, y + 22)], fill=(200, 190, 160))
    for cx in (60, 78, 96, 114, 130):
        d.rectangle([x + cx, y + 26, x + cx + 6, y + h - 4], fill=(180, 170, 140))
    # flagpole + Australian flag
    d.line([x + 97, y + 6, x + 97, y - 6], fill=INK, width=2)
    d.rectangle([x + 97, y - 6, x + 117, y + 4], fill=(0, 40, 120))
    # small Chinese flag at the side
    d.rectangle([x + 158, y + 14, x + 182, y + 28], fill=(222, 41, 16))
    d.ellipse([x + 162, y + 18, x + 166, y + 22], fill=(255, 222, 0))
    d.line([x + 158, y + 14, x + 158, y + h], fill=INK, width=2)

def art_bitcoin(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 240, 200))
    # falling chart
    pts = [(x + 12, y + 12), (x + 40, y + 18), (x + 68, y + 16), (x + 96, y + 30),
           (x + 120, y + 38)]
    d.line(pts, fill=(200, 30, 30), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(200, 30, 30))
    # gold coin
    cx, cy, r = x + 158, y + 26, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 147, 26), outline=(180, 110, 10), width=2)
    text(cx, cy - 13, "\u20bf", SANS_B(24), fill=(255, 255, 255), anchor="ma")

def art_rahul(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 200))
    # pitch
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(190, 170, 120))
    # stumps
    for sx in (150, 156, 162):
        d.line([x + sx, y + 22, x + sx, y + h - 12], fill=(240, 200, 60), width=3)
    # red ball
    d.ellipse([x + 172, y + 30, x + 180, y + 38], fill=(200, 30, 30))
    # batsman: head, body, legs, bat
    d.ellipse([x + 62, y + 6, x + 78, y + 22], fill=(200, 150, 110))  # head + cap
    d.polygon([(x + 58, y + 22), (x + 82, y + 22), (x + 86, y + h - 14), (x + 54, y + h - 14)],
              fill=(30, 90, 160))  # blue shirt
    d.line([x + 64, y + h - 14, x + 58, y + h - 2], fill=(240, 240, 240), width=5)
    d.line([x + 76, y + h - 14, x + 84, y + h - 2], fill=(240, 240, 240), width=5)
    d.line([x + 84, y + 26, x + 108, y + 44], fill=(180, 130, 70), width=6)  # bat

MID = [
    ("KRYVYI RIH", "4  KRYVYI RIH  \u00b7  WAR", "Russian double strike kills 2, injures 42",
     "Two missiles hit a restaurant car park; drones struck again as rescuers worked. (Kyiv Indp.)", "REPORTED", art_kryvyi),
    ("KYIV WARNING", "5  KYIV  \u00b7  WAR", "Zelensky: Crimea bridge \u201cwill not stay\u201d",
     "He warns of double-tap strikes in an NBC interview. (NBC)", "REPORTED", art_kyiv),
    ("HORMUZ: DRONE", "6  STRAIT OF HORMUZ  \u00b7  WAR", "Iran says it downed a US drone",
     "Tehran claims the shootdown; Washington has not confirmed it. (IRIB)", "REPORTED", art_hormuz),
    ("IRAN: URANIUM", "7  TEHRAN  \u00b7  DIPLOMACY", "Iran: uranium stock stays at home",
     "Minister still seeks a \u201cfair solution\u201d. (ToI)", "OFFICIAL", art_iran),
    ("TRUMP: AI TAX", "8  WASHINGTON  \u00b7  TECHNOLOGY", "Trump vows tax on data centres abroad",
     "\u201cTremendous\u201d penalty promised; no details yet. (ABC)", "REPORTED", art_trump),
    ("CHINA\u2013JAPAN", "9  BEIJING  \u00b7  DIPLOMACY", "China tells Japan to \u201ccorrect\u201d Taiwan words",
     "Tokyo says its stance is unchanged. (Ministry, AFP)", "OFFICIAL", art_chinajapan),
    ("DAVAO: 146 SAFE", "10  DAVAO  \u00b7  AVIATION", "Jet lands safely after engine fire alert",
     "Air Niugini 767 diverts after midnight; all 146 aboard safe. (AP)", "OFFICIAL", art_davao),
    ("CANBERRA: AI", "11  CANBERRA  \u00b7  DIPLOMACY", "Australia and China agree AI talks",
     "Albanese ends an 11-day trip. (ABC)", "OFFICIAL", art_canberra),
    ("BITCOIN: $58,810", "12  WORLD  \u00b7  MARKETS", "Bitcoin slips below $59,000",
     "Down 4.1% in 24 hours; ether $1,619. (CoinGecko, 01:30 UTC)", "CONFIRMED", art_bitcoin),
    ("RAHUL: 124*", "13  WELLINGTON  \u00b7  CRICKET", "Rahul century puts India on top",
     "India 344 for 2 at tea, replying to 368. (AFP)", "OFFICIAL", art_rahul),
]
LABEL_BG = [(176, 30, 30), (31, 92, 168), (110, 60, 140), (46, 125, 60), (20, 32, 64),
            (176, 30, 30), (46, 125, 60), (31, 92, 168), (176, 130, 30), (20, 130, 130)]
for i, (label, loc, head, body, bd, art) in enumerate(MID):
    col = i % 5
    row = i // 5
    x = 14 + col * 200
    y0 = 460 + row * 140
    w = 194
    art(x, y0, w, 48)
    d.rectangle([x, y0 + 48, x + w, y0 + 65], fill=LABEL_BG[i])
    text(x + 5, y0 + 51, label, SANS_B(11), fill=(255, 255, 255))
    # verification badge as a small pill at the right end of the label bar
    bf = SANS_B(9)
    bw = d.textlength(bd, font=bf) + 10
    rrect(x + w - bw - 4, y0 + 51, bw, 12, 6, fill=BADGE_BG[bd], outline=(255, 255, 255), width=1)
    d.text((x + w - bw + 1, y0 + 52), bd, font=bf, fill=(255, 255, 255))
    text(x, y0 + 69, loc, SANS_B(9), fill=RED)
    hl = wrap(head, SERIF_B(13), w)
    for j, ln in enumerate(hl[:2]):
        text(x, y0 + 82 + j * 15, ln, SERIF_B(13))
    bl = wrap(body, SERIF(10), w)
    for j, ln in enumerate(bl[:2]):
        text(x, y0 + 112 + j * 12, ln, SERIF(10))

# ---------------------------------------------------------------- map + also list
text(14, 742, "WHERE IT HAPPENED", SANS_B(13), fill=RED)
text(360, 742, "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES", SANS_B(13), fill=RED)
# map
mx0, my0, mx1, my1 = 14, 760, 344, 908
d.rectangle([mx0, my0, mx1, my1], fill=(220, 232, 240), outline=(180, 190, 200), width=1)
LAND = (224, 211, 174)
d.polygon([(28, 772), (60, 762), (95, 766), (120, 772), (128, 790), (110, 806), (88, 812), (70, 830), (52, 822), (30, 800), (22, 784)], fill=LAND)
d.polygon([(128, 758), (142, 756), (146, 766), (134, 770)], fill=LAND)
d.polygon([(78, 836), (105, 832), (122, 846), (118, 872), (100, 896), (84, 884), (74, 858)], fill=LAND)
d.polygon([(168, 762), (196, 758), (210, 768), (204, 784), (188, 790), (172, 780)], fill=LAND)
d.polygon([(170, 796), (200, 792), (216, 806), (210, 836), (196, 862), (180, 856), (168, 826)], fill=LAND)
d.polygon([(214, 764), (280, 756), (322, 766), (330, 790), (310, 812), (280, 826), (250, 818), (228, 800), (214, 782)], fill=LAND)
d.polygon([(272, 868), (310, 862), (322, 874), (306, 890), (278, 886)], fill=LAND)
d.ellipse([158, 758, 166, 766], fill=LAND)
# numbered dots: (num, true_x, true_y, dot_x, dot_y)
DOTS = [(1, 222, 784, 222, 784), (2, 238, 800, 244, 806), (3, 92, 858, 92, 858),
        (4, 200, 770, 196, 762), (5, 196, 764, 180, 750), (6, 252, 796, 258, 790),
        (7, 242, 782, 240, 772), (8, 58, 782, 58, 782), (9, 292, 778, 292, 778),
        (10, 300, 838, 300, 838), (11, 304, 880, 304, 880), (12, None, None, 140, 898),
        (13, 326, 896, 326, 896)]
for num, tx, ty, dx, dy in DOTS:
    if tx is not None and (abs(tx - dx) > 4 or abs(ty - dy) > 4):
        d.line([dx, dy, tx, ty], fill=(120, 120, 120), width=1)
        d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=RED)
    d.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=RED, outline=(255, 255, 255), width=1)
    text(dx, dy - 6, str(num), SANS_B(10), fill=(255, 255, 255), anchor="ma")
text(14, 912, "Red numbers mark stories 1\u201313. No. 12 is Bitcoin \u2014 a global market.",
     SANS(10), fill=GREY)

ALSO = [
    (14, "Kryvyi Rih: strike kills 2, injures 42", "Kyiv Indp."),
    (15, "Copenhagen: Russian attach\u00e9 expelled", "Al Jazeera"),
    (16, "Antalya: EU warns COP31 risks a \u201cfossil summit\u201d", "AFP"),
    (17, "Antalya: Panama threatens to block climate text", "Al Jazeera"),
    (18, "Antalya: PLN signs six clean-power deals", "Antara"),
    (19, "Yemen: Houthis threaten Jeddah, Red Sea ports", "Al Jazeera"),
    (20, "Washington: Vance: Iran strikes were Trump\u2019s call", "Reuters"),
    (21, "Washington: lawmaker threatens SpaceX funding", "CNN"),
    (22, "Texas: execution of man, 70, takes 63 minutes", "ABC"),
    (23, "Los Angeles: jury convicts Palisades arsonist", "ABC"),
    (24, "Missouri: judge OKs $7.25bn Roundup settlement", "AFP"),
    (25, "Vancouver: Canada rests climate-trial defence", "AFP"),
    (26, "Pyongyang: Kim tours factories, no Trump talks", "AFP"),
    (27, "Sejong: freight train derails, no hurt", "Korea Herald"),
    (28, "Taipei: budget and cash payout passed", "Taipei Times"),
    (29, "Bangkok: arsenic plan for two rivers", "The Nation"),
    (30, "New Delhi: Pakistani minister joins SCO forum", "Dawn"),
    (31, "E. India: rain alerts as Akvan remnants move in", "ETV"),
    (32, "Myanmar: rights groups urge sanctions after ruling", "AP"),
    (33, "Port Louis: rating agency woos 15 states", "Al Jazeera"),
    (34, "Melbourne: Cummins keeps the Australian captaincy", "ABC"),
    (35, "Las Vegas: Verstappen sent to stewards after contact", "Autosport"),
]
for k, (num, head, src) in enumerate(ALSO):
    colx = 360 if k < 11 else 690
    y = 760 + (k % 11) * 14
    line = f"{num} {head} ({src})"
    f = SANS(11)
    if d.textlength(line, font=f) > 318:
        f = SANS(10)
    if d.textlength(line, font=f) > 318:
        f = SANS(9)
    d.text((colx, y), str(num), font=SANS_B(11), fill=RED)
    d.text((colx + 20, y), f"{head} ({src})", font=f, fill=INK)

# ---------------------------------------------------------------- DATE CHECK
d.rectangle([14, 922, 1010, 968], outline=RED, width=2)
dc = ("DATE CHECK \u2014 Left out as earlier news. Fri 20 Nov: the Russian barrage that hit Kyiv\u2019s bridges, "
      "a missile that landed in Poland, Wall Street\u2019s fall into a correction, the UK\u2013EU deal, Cyclone "
      "Akvan\u2019s landfall. Thu 19 Nov: the ICJ Myanmar genocide ruling, the Shenzhen summit. 18 Nov: Voyager 1\u2019s "
      "light-day. Not confirmed when drawn, so not shown: BepiColombo in Mercury orbit, a final COP31 text.")
for j, ln in enumerate(wrap(dc, SANS(11), 968)):
    text(22, 926 + j * 14, ln, SANS(11))

# ---------------------------------------------------------------- footer
text(14, 974, "Every story here happened, or was first reported, on Saturday 21 November 2026. Sources named beside each story. Original drawings.",
     SANS(10), fill=GREY)
text(1010, 974, "make.fun/r/kh987p5b", SANS_B(10), fill=GREY, anchor="ra")
text(14, 988, "HOW WE CHECKED: CONFIRMED = 2+ outlets  \u00b7  OFFICIAL = on the record  \u00b7  REPORTED = one outlet",
     SANS(10), fill=GREY)
text(1010, 988, "ONE DAY ON EARTH \u00b7 21 NOVEMBER 2026", SANS(10), fill=GREY, anchor="ra")

img.save("/home/hatch/workspace/makefun/news-image-20261121/entry-r4/entry.png")
import os
print("saved", os.path.getsize("/home/hatch/workspace/makefun/news-image-20261121/entry-r4/entry.png"), "bytes")
