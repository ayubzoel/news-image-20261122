#!/usr/bin/env python3
"""The World in One Day -- Sunday, 22 November 2026.

One 1024x1024 newspaper poster drawn from scratch with Pillow.
Every story comes from the 22 Nov 2026 research file; nothing is
photographed, nothing is copied from an earlier poster.
Run:  python3 poster.py   -> writes entry.png next to this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24
CREAM = (247, 242, 231)
PAPER = (252, 249, 240)
INK = (17, 17, 17)
SOFT = (74, 72, 66)
RED = (178, 28, 28)
BLUE = (29, 68, 140)
NAVY = (16, 34, 64)
LAND = (216, 208, 186)
LANDLINE = (148, 140, 112)
OCEAN = (232, 238, 242)
RULE = (17, 17, 17)

DJ = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(DJ + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def fit_line(draw, text, fnt, width):
    """Shorten with an ellipsis so a one-liner never spills its column."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1].rstrip()
    return text + "\u2026"

def centred(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)

# ---------------------------------------------------------------- stories
TOP = [
    ("COP31 COLLAPSES", "No deal in Antalya after 44 hours overtime; fossil-fuel text dropped."),
    ("IRAN HITS BAHRAIN", "Strike on a civilian site in Sitra; 2 hurt, one critical."),
    ("HOUTHI FIRE AT SAUDI", "Drone toward Riyadh and a missile toward Mecca intercepted."),
    ("DRONE HITS FLATS NEAR KYIV", "14 missing in Dymer; 3 killed in a separate strike."),
    ("CANDY FACTORY FIRE", "Cikande, Indonesia: 3 dead, 36 missing; 300 at work."),
    ("BEPICOLOMBO AT MERCURY", "In orbit after 8 years; thruster glitch under study."),
    ("$1.94 TRILLION WIPED OUT", "Friday rout: Nasdaq-100 -5.61%; Nvidia -14.01%."),
    ("LIVERPOOL 4-0 MAN UTD", "Pochettino's debut ruined at Anfield; 10 men from 8'."),
    ("SETTLERS TORCH CARS", "12 vehicles burned near Ramallah; Israel opens inquiry."),
    ("BOAT CAPSIZES IN NIGERIA", "24 dead on the way to a funeral."),
    ("SHURI CASTLE RESTORED", "Okinawa celebrates 7 years after the 2019 fire."),
    ("PAOLO BULGARI DIES", "Jeweller who built a global luxury house, aged 89."),
    ("VIETNAM ENDS DEATH PENALTY", "For drug dealing, in a legal reform."),
    ("FRANCE PROTESTS, WEEK 6", "Socialist marches continue; numbers falling."),
    ("MALAYSIA ENDS 27-YEAR WAIT", "Hong Kong Open men's doubles title."),
]

ALSO = [
    "Russian ship Sparta II still burning in Gulf of Finland",
    "Rohingya welcome ICJ verdict, want to go home",
    "Zelensky: Shenzhen summit a failure for Putin",
    "Hull 2-0 Brighton \u2014 McBurnie late double",
    "ATP Finals: Alcaraz vs Zverev in the final",
    "F1: Antonelli takes Las Vegas pole",
    "Drones hit Khartoum, damage UN building",
    "Trump: Iran wants a deal; Tehran's door open",
    "Yemen army kills 86 Houthi rebels",
    "Ex-Italian police chief dies by suicide in mafia probe",
    "Lithuania denies role in Kaliningrad drone strike",
    "Vietnam speeds up land seizures",
    "Denmark pushes EU curbs on Russians",
    "Spain heads to 29 Nov election amid uncertainty",
    "Trafalgar tree felled in Norway, 69 ft",
    "Awami League properties torched in Bangladesh",
    "Anthropic lists at $83 a share, ~$1.5T value",
    "90+ nations sign COP31 electrification pledge",
    "Two tankers hit near Oman",
    "Eisenkot invites Likud to coalition talks",
]

NUMBERS = [
    ("$1.94T", "market value wiped out in one Friday session"),
    ("-14.01%", "Nvidia in a day, its 6th straight fall"),
    ("194", "COP31 delegations \u2014 and no deal"),
    ("3 dead, 36 missing", "Cikande candy-factory fire"),
    ("14 missing", "Dymer apartment drone strike"),
    ("8 years", "BepiColombo's trip to Mercury"),
]

# (number, lat, lon) for all 35 stories, real coordinates.
PINS = [
    (1, 36.90, 30.71), (2, 26.22, 50.59), (3, 24.71, 46.68),
    (4, 50.78, 30.31), (5, -6.22, 106.34), (6, 49.87, 8.65),
    (7, 40.71, -74.01), (8, 53.43, -2.96), (9, 31.90, 35.20),
    (10, 9.08, 7.50), (11, 26.22, 127.68), (12, 41.90, 12.50),
    (13, 21.03, 105.85), (14, 48.86, 2.35), (15, 22.32, 114.17),
    (16, 59.90, 25.00), (17, 21.44, 91.97), (18, 50.45, 30.52),
    (19, 53.74, -0.34), (20, 45.07, 7.69), (21, 36.11, -115.17),
    (22, 15.60, 32.53), (23, 38.91, -77.04), (24, 15.37, 44.19),
    (25, 41.90, 12.50), (26, 54.69, 25.28), (27, 21.03, 105.85),
    (28, 55.68, 12.57), (29, 40.42, -3.70), (30, 59.91, 10.75),
    (31, 23.81, 90.41), (32, 37.77, -122.42), (33, 36.90, 30.71),
    (34, 24.50, 58.50), (35, 31.77, 35.21),
]

# Rough continent outlines as (lon, lat) rings, coarse but recognisable.
NORTH_AMERICA = [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-130, 54),
    (-125, 49), (-124, 40), (-120, 34), (-114, 29), (-110, 24), (-105, 20),
    (-97, 16), (-90, 14), (-83, 9), (-79, 9), (-82, 13), (-88, 18),
    (-90, 21), (-96, 19), (-97, 26), (-93, 30), (-84, 30), (-81, 26),
    (-80, 32), (-76, 35), (-74, 40), (-70, 42), (-65, 44), (-60, 47),
    (-55, 47), (-60, 50), (-65, 50), (-68, 52), (-72, 55), (-78, 58),
    (-85, 60), (-90, 63), (-95, 66), (-110, 68), (-125, 70), (-140, 70),
    (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-45, 60), (-40, 64), (-32, 68),
    (-25, 70), (-20, 74), (-30, 76), (-45, 76), (-58, 74), (-60, 70)]
SOUTH_AMERICA = [(-80, 9), (-77, 4), (-72, 12), (-64, 11), (-60, 8),
    (-55, 6), (-52, 5), (-50, 0), (-44, -3), (-38, -5), (-35, -8),
    (-40, -20), (-48, -27), (-52, -33), (-58, -38), (-62, -41),
    (-66, -47), (-68, -52), (-70, -55), (-73, -50), (-73, -44),
    (-73, -37), (-72, -30), (-70, -20), (-75, -15), (-80, -6), (-81, 0),
    (-80, 5)]
AFRICA = [(-6, 33), (-10, 30), (-15, 26), (-17, 20), (-17, 15), (-15, 11),
    (-12, 8), (-8, 5), (-4, 5), (0, 6), (6, 4), (9, 4), (9, 0), (12, -2),
    (12, -6), (13, -10), (12, -17), (14, -22), (16, -28), (18, -33),
    (20, -35), (26, -34), (32, -29), (35, -24), (40, -16), (40, -10),
    (41, -4), (43, -1), (48, 2), (51, 11), (48, 11), (44, 13), (40, 15),
    (38, 18), (37, 22), (34, 27), (32, 31), (30, 31), (25, 32), (20, 32),
    (15, 32), (11, 33), (10, 35), (5, 35), (0, 34)]
EURASIA = [(-9, 37), (-9, 43), (-2, 44), (-2, 48), (-5, 48), (-1, 50),
    (2, 51), (5, 53), (8, 57), (10, 57), (12, 56), (18, 56), (21, 55),
    (24, 58), (21, 60), (18, 62), (12, 64), (10, 64), (5, 60), (5, 58),
    (8, 58), (10, 59), (12, 61), (18, 64), (25, 71), (32, 70), (40, 68),
    (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 76),
    (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
    (170, 66), (178, 65), (170, 60), (162, 56), (156, 51), (142, 50),
    (140, 44), (135, 43), (132, 43), (128, 38), (126, 35), (122, 32),
    (120, 28), (115, 23), (110, 20), (108, 18), (106, 10), (104, 8),
    (100, 6), (98, 10), (97, 15), (94, 17), (92, 21), (90, 22), (86, 20),
    (82, 17), (80, 13), (77, 8), (74, 14), (72, 20), (68, 23), (66, 25),
    (61, 25), (57, 26), (54, 27), (50, 29), (48, 30), (44, 29), (43, 12),
    (39, 21), (35, 29), (34, 31), (36, 38), (30, 38), (27, 39), (23, 38),
    (22, 39), (19, 41), (15, 44), (12, 44), (8, 44), (3, 43), (0, 39),
    (-2, 37), (-6, 36)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
    (1, 51), (-2, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37),
    (141, 40), (143, 42), (145, 44), (142, 45), (140, 40), (138, 36),
    (134, 34), (131, 33)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
    (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
    (142, -39), (145, -38), (147, -39), (150, -37), (153, -32),
    (153, -27), (150, -23), (146, -19), (142, -11), (141, -13),
    (136, -12), (132, -12), (130, -13), (126, -14), (122, -17),
    (118, -20)]
NEW_ZEALAND = [(167, -45), (170, -43), (173, -41), (175, -38),
    (177, -38), (178, -38), (175, -41), (172, -43), (168, -46)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (48, -22), (45, -25),
    (43, -21)]
BORNEO = [(109, 1), (111, 3), (114, 5), (117, 7), (119, 1), (118, -3),
    (115, -4), (112, -6), (110, -3)]
SUMATRA = [(95, 5), (98, 3), (100, 0), (102, -3), (104, -5), (106, -6),
    (104, -4), (101, 1), (97, 4)]
NEW_GUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9),
    (146, -8), (141, -8), (136, -5), (132, -3)]
ICELAND = [(-22, 64), (-18, 63), (-14, 64), (-15, 66), (-20, 66),
    (-24, 65)]
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EURASIA,
    BRITAIN, JAPAN, AUSTRALIA, NEW_ZEALAND, MADAGASCAR, BORNEO, SUMATRA,
    NEW_GUINEA, ICELAND]

# Map window: lon -125..145, lat -55..75, drawn at 2x then downscaled.
MAP_X0, MAP_X1 = 24, 1000
MAP_Y0, MAP_Y1 = 436, 600
LON_A, LON_B = -170.0, 190.0
LAT_A, LAT_B = -55.0, 75.0
SCALE = 2

def project(lon, lat, w, h):
    x = (lon - LON_A) / (LON_B - LON_A) * w
    y = (LAT_A - lat) / (LAT_A - LAT_B) * h
    return x, y

def spread(points, min_gap):
    """Push overlapping pin centres apart so numbers stay readable."""
    pts = [list(p) for p in points]
    for _ in range(60):
        moved = False
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[j][0] - pts[i][0]
                dy = pts[j][1] - pts[i][1]
                d = math.hypot(dx, dy)
                if 0 < d < min_gap:
                    push = (min_gap - d) / 2 + 0.5
                    ux, uy = dx / d, dy / d
                    pts[i][0] -= ux * push
                    pts[i][1] -= uy * push
                    pts[j][0] += ux * push
                    pts[j][1] += uy * push
                    moved = True
                elif d == 0:
                    pts[j][0] += min_gap
                    moved = True
        if not moved:
            break
    return [(p[0], p[1]) for p in pts]

def draw_map(base):
    """Render the world layer at 2x, then paste it downscaled (LANCZOS)."""
    mw = (MAP_X1 - MAP_X0) * SCALE
    mh = (MAP_Y1 - MAP_Y0) * SCALE
    layer = Image.new("RGB", (mw, mh), OCEAN)
    d = ImageDraw.Draw(layer)
    for lon in range(-120, 151, 30):
        x, _ = project(lon, LAT_A, mw, mh)
        d.line([(x, 0), (x, mh)], fill=(214, 222, 228), width=1)
    for lat in range(-30, 85, 30):
        _, y = project(LON_A, lat, mw, mh)
        d.line([(0, y), (mw, y)], fill=(214, 222, 228), width=1)
    for ring in CONTINENTS:
        pts = [project(lon, lat, mw, mh) for lon, lat in ring]
        d.polygon(pts, fill=LAND, outline=LANDLINE, width=2)
    small = layer.resize((MAP_X1 - MAP_X0, MAP_Y1 - MAP_Y0),
                         Image.LANCZOS)
    base.paste(small, (MAP_X0, MAP_Y0))
    draw = ImageDraw.Draw(base)
    w = MAP_X1 - MAP_X0
    h = MAP_Y1 - MAP_Y0
    draw.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], outline=INK, width=2)
    true_xy = [project(lon, lat, w, h) for _, lat, lon in PINS]
    true_xy = [(MAP_X0 + x, MAP_Y0 + y) for x, y in true_xy]
    shown = spread(true_xy, 20.0)
    num_font = SANS_B(9)
    for (num, _, _), (tx, ty), (sx, sy) in zip(PINS, true_xy, shown):
        sx = min(max(sx, MAP_X0 + 9), MAP_X1 - 9)
        sy = min(max(sy, MAP_Y0 + 9), MAP_Y1 - 9)
        if math.hypot(sx - tx, sy - ty) > 3:
            draw.line([(tx, ty), (sx, sy)], fill=SOFT, width=1)
            draw.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=INK)
        r = 8 if num >= 10 else 7
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        label = str(num)
        tw = draw.textlength(label, font=num_font)
        draw.text((sx - tw / 2, sy - 6.5), label, font=num_font,
                  fill=(255, 255, 255))
    return draw

def draw_hero(draw):
    """Hero band: headline left, procedural Antalya scene right."""
    x0, y0, x1, y1 = 640, 118, 1000, 308
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    # Cracked-earth globe.
    cx, cy, r = 820, 205, 62
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 122, 190),
                 outline=(255, 255, 255), width=2)
    draw.ellipse([cx - 42, cy - 30, cx - 8, cy - 6], fill=(74, 160, 96))
    draw.ellipse([cx + 2, cy + 12, cx + 38, cy + 38], fill=(74, 160, 96))
    draw.ellipse([cx - 20, cy + 28, cx + 6, cy + 48], fill=(74, 160, 96))
    crack = [(cx - 55, cy - 40), (cx - 28, cy - 12), (cx - 38, cy + 8),
             (cx - 6, cy + 22), (cx + 12, cy + 2), (cx + 30, cy + 26),
             (cx + 52, cy + 44)]
    draw.line(crack, fill=(232, 72, 48), width=4, joint="curve")
    draw.line(crack, fill=(255, 214, 90), width=1, joint="curve")
    # Delegate rows beneath the globe.
    for row in range(2):
        for i in range(9):
            px = x0 + 18 + i * 38
            py = y1 - 46 + row * 20
            draw.rectangle([px, py, px + 26, py + 12],
                           fill=(120, 150, 200) if i % 2 else (200, 170, 90))
    centred(draw, 820, y0 + 8, "ANTALYA, TURKIYE", SANS_B(11),
            fill=(255, 214, 90))
    # Small flags: Turkiye red crescent, EU blue stars ring.
    fx, fy = x0 + 16, y0 + 30
    draw.rectangle([fx, fy, fx + 34, fy + 22], fill=(200, 30, 30))
    draw.ellipse([fx + 8, fy + 4, fx + 22, fy + 18], fill=(255, 255, 255))
    draw.ellipse([fx + 11, fy + 4, fx + 24, fy + 18], fill=(200, 30, 30))
    ex = x1 - 52
    draw.rectangle([ex, fy, ex + 34, fy + 22], fill=(30, 60, 150))
    for k in range(8):
        ang = 2 * math.pi * k / 8
        sx = ex + 17 + 9 * math.cos(ang)
        sy = fy + 11 + 7 * math.sin(ang)
        draw.ellipse([sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5],
                     fill=(255, 214, 90))
    # Headline text, left of the panel.
    draw.text((MARGIN, 122), "COP31", font=SERIF_B(64), fill=RED)
    draw.text((MARGIN, 186), "COLLAPSES", font=SERIF_B(64), fill=INK)
    draw.text((MARGIN, 256), "No deal as fossil fuels split the world",
              font=SERIF_B(20), fill=INK)
    draw.text((MARGIN, 286),
              "Antalya talks end after 44 hours overtime \u2014 the draft pact",
              font=SANS(14), fill=SOFT)
    draw.text((MARGIN, 304),
              "dropped any mention of fossil fuels; 90+ nations still sign on.",
              font=SANS(14), fill=SOFT)

def section_head(draw, y, text):
    draw.text((MARGIN, y), text, font=SANS_B(15), fill=INK)
    draw.line([(MARGIN, y + 22), (W - MARGIN, y + 22)], fill=INK, width=2)

def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    # Masthead.
    centred(draw, W // 2, 10, "THE WORLD IN ONE DAY", SERIF_B(56))
    draw.line([(MARGIN, 78), (W - MARGIN, 78)], fill=RULE, width=3)
    centred(draw, W // 2, 86, "SUNDAY, 22 NOVEMBER 2026", SANS_B(24),
            fill=RED)
    draw.line([(MARGIN, 114), (W - MARGIN, 114)], fill=RULE, width=1)
    draw_hero(draw)
    # Numbers strip.
    section_head(draw, 320, "THE DAY IN NUMBERS")
    cell_w = (W - 2 * MARGIN) / 6
    for i, (big, label) in enumerate(NUMBERS):
        cx = MARGIN + cell_w * i
        draw.line([(cx, 350), (cx, 398)], fill=(190, 184, 168), width=1)
        size = 21
        while size > 13 and draw.textlength(big, font=SANS_B(size)) > cell_w - 8:
            size -= 1
        centred(draw, cx + cell_w / 2, 350, big, SANS_B(size), fill=RED)
        for k, line in enumerate(wrap(draw, label, SANS(11), cell_w - 14)):
            centred(draw, cx + cell_w / 2, 376 + k * 13, line, SANS(11),
                    fill=SOFT)
    # Map.
    section_head(draw, 408, "THE WORLD TODAY  \u2014  35 STORIES, ONE MAP")
    draw_map(img)
    draw = ImageDraw.Draw(img)
    # Top stories, two columns.
    section_head(draw, 606, "TOP STORIES")
    col_w = (W - 2 * MARGIN - 24) / 2
    for idx, (title, fact) in enumerate(TOP):
        col = 0 if idx < 8 else 1
        row = idx if idx < 8 else idx - 8
        x = MARGIN + col * (col_w + 24)
        y = 634 + row * 25
        draw.ellipse([x, y + 2, x + 15, y + 17], fill=RED)
        num = str(idx + 1)
        tw = draw.textlength(num, font=SANS_B(10))
        draw.text((x + 7.5 - tw / 2, y + 4), num, font=SANS_B(10),
                  fill=(255, 255, 255))
        draw.text((x + 21, y), title, font=SANS_B(12), fill=INK)
        draw.text((x + 21, y + 13), fact, font=SANS(11), fill=SOFT)
    # Also today, three columns, one line each.
    section_head(draw, 842, "ALSO TODAY")
    acol_w = (W - 2 * MARGIN - 2 * 20) / 3
    for idx, item in enumerate(ALSO):
        col = idx // 7
        row = idx % 7
        x = MARGIN + col * (acol_w + 20)
        y = 870 + row * 19
        draw.text((x, y), f"{idx + 16}.", font=SANS_B(11), fill=RED)
        draw.text((x + 24, y), fit_line(draw, item, SANS(11), acol_w - 24),
                  font=SANS(11), fill=INK)
    draw.line([(MARGIN, 1006), (W - MARGIN, 1006)], fill=RULE, width=1)
    centred(draw, W // 2, 1010,
            "Sources: AP, Reuters, CNN, AFP, Le Monde \u2014 all stories from Sunday 22 November 2026",
            SANS(10), fill=SOFT)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)

if __name__ == "__main__":
    main()
