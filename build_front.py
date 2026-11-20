#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page (1024x1024 JPEG).

Written fresh for make.fun news-image-20261120. Every story was verified
from reports first published on Friday 20 November 2026 (or, for late
19 Nov UTC wires, first reported on 20 Nov in Asian time zones).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (24, 24, 28)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
GOLD = (197, 141, 28)
GREEN = (34, 110, 60)
BLUE = (36, 84, 160)
GREY = (90, 90, 92)
LIGHT = (255, 255, 255)
CREAM = (255, 248, 235)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def f(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = f(FD + "DejaVuSerif-Bold.ttf", 52)
SANS_B = lambda s: f(FL + "LiberationSans-Bold.ttf", s)
SANS = lambda s: f(FL + "LiberationSans-Regular.ttf", s)

FEATURES = [
    # num, region, kicker, headline, deck, art
    (1, "ASIA", "CYCLONE AKVAN",
     "AKVAN HITS ODISHA AT NOON",
     "Severe storm crosses near Gopalpur, winds to 110 km/h — 300,000 evacuated to shelters.",
     "storm"),
    (2, "WORLD", "COP31 · ANTALYA",
     "CLIMATE TALKS CLOSE TODAY",
     "Draft: $120bn a year for adaptation.",
     "globe"),
    (3, "AMERICAS", "NEW YORK · MARKETS",
     "ANTHROPIC ENDS FIRST DAY UP 17%",
     "The Claude maker opens at $111.50, closes at $97.17; record $81.3bn offering closes today.",
     "candles"),
    (4, "WORLD", "CULTURE · GAMING",
     "GTA VI'S FIRST FULL DAY",
     "Est. $1.84bn, ~19m copies on day one.",
     "vicecity"),
    (5, "WORLD", "CRICKET · WELLINGTON",
     "NZ 317/6: PHILLIPS 118",
     "NZ 317/6 at lunch; Nicholls 146*.",
     "cricket"),
    (6, "AMERICAS", "SENATE · IRAN",
     "SENATE BLOCKS WAR CURB",
     "Kills the Iran war-powers bid, 51–48.",
     "vote"),
    (7, "MIDDLE EAST", "IRAN · WASHINGTON",
     "TRUMP: NO RUSH ON IRAN",
     "New strikes wait until after Jan 1.",
     "capitol"),
    (8, "EUROPE", "KYIV · WAR",
     "STRIKES HIT KYIV EMBASSIES",
     "One killed; embassies and a cathedral hit.",
     "embassy"),
    (9, "ASIA", "SHENZHEN · DIPLOMACY",
     "LEADERS ISSUE PEACE DECLARATION",
     "Published hours after the trilateral meeting.",
     "flags3"),
    (10, "AMERICAS", "CALIFORNIA · TECH",
     "STATE PROBES NVIDIA",
     "California subpoenas Nvidia over China chips.",
     "chip"),
    (11, "WORLD", "SENEGAL · MIGRATION",
     "MIGRANT BOAT SINKS OFF SENEGAL",
     "Four bodies found; dozens missing, 50–100 aboard.",
     "boat"),
    (12, "WORLD", "TONGA · PACIFIC",
     "DROUGHT EMERGENCY IN TONGA",
     "Kingdom declares an emergency as El Niño bites.",
     "drought"),
    (13, "AMERICAS", "WASHINGTON · SPORT",
     "TRUMP PARDONS PETE ROSE",
     "The late slugger is pardoned after his death.",
     "baseball"),
]

BRIEFS = [
    ("MIDDLE EAST", "Iran war cost US $48bn+ since Feb, Pentagon says"),
    ("AMERICAS", "Netanyahu pressed Trump for a new Iran strike"),
    ("MIDDLE EAST", "Trump: Iran wants a deal — wait till after Jan 1"),
    ("EUROPE", "Putin: US “insistently” asks Europe into peace talks"),
    ("EUROPE", "Zelenskyy: pressure needed, Europe ready to act"),
    ("EUROPE", "Macron: rethink Ukraine's NATO accession"),
    ("ASIA", "Akvan: midnight meet; temple shut till 21 Nov"),
    ("ASIA", "Akvan: 2,523 relief camps; surge of 0.5–1 m warned"),
    ("WORLD", "COP31: 83 developing nations filed adaptation plans"),
    ("WORLD", "COP31: 17 nations back Antalya carbon-markets deal"),
    ("WORLD", "COP31: AI pledge fails to draw major US tech firms"),
    ("WORLD", "S&P −2.02%, Nasdaq −2.25%, Dow 49,097 −2.19%"),
    ("WORLD", "Gold $3,652 −2.39%, a 14-month low; silver $45.30"),
    ("WORLD", "Brent $92.74 +0.86%; WTI $83.16; IEA sees surplus"),
    ("WORLD", "Dollar 103.94, near 19-month high; yield over 5%"),
    ("WORLD", "Bitcoin $63,384 −2%; ether $1,802 as crypto slides"),
    ("MIDDLE EAST", "IAEA presses Iran on inspections"),
    ("WORLD", "Voyager 1: one light-day out, NASA confirms"),
]

NUMBERS = [
    ("300,000", "AKVAN EVACUATED"),
    ("$97.17", "ANTHROPIC FIRST CLOSE"),
    ("118", "PHILLIPS' CENTURY"),
    ("51–48", "SENATE VOTE"),
    ("99", "GTA VI METACRITIC"),
    ("$120bn", "COP31 ADAPTATION"),
]

REGION_ORDER = ["ASIA", "AMERICAS", "EUROPE", "MIDDLE EAST", "WORLD"]
REGION_COLOR = {"ASIA": (178, 34, 34), "AMERICAS": (36, 84, 160),
                "EUROPE": (34, 110, 60), "MIDDLE EAST": (150, 90, 10),
                "WORLD": (90, 60, 140)}

DATE_CHECK = ("DATE CHECK — NOT TODAY, LEFT OUT: ICJ's Myanmar genocide ruling · "
              "Trump–Xi–Putin trilateral meeting itself · Fed minutes · "
              "Houthi missile at Riyadh · Fiji disaster declaration · Gemini 4 Neon launch.")


def wrap(text, font, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, font, width, max_lines):
    """Wrap and assert it fits in max_lines; return lines."""
    lines = wrap(text, font, width)
    assert len(lines) <= max_lines, f"OVERFLOW ({len(lines)}>{max_lines}): {text!r}"
    return lines


# ---------------- flat art panels ----------------

def art_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for i in range(40):
        d.ellipse([x + 8 + i * 9, y + 8 + (i % 3) * 4, x + 12 + i * 9, y + 12 + (i % 3) * 4],
                  fill=(255, 255, 255))
    cx = x + w // 2
    d.polygon([(cx - 40, y + h), (cx - 40, y + h - 58), (cx - 24, y + h - 82),
               (cx - 12, y + h - 90), (cx, y + h - 102), (cx + 12, y + h - 90),
               (cx + 24, y + h - 82), (cx + 40, y + h - 58), (cx + 40, y + h)],
              fill=(240, 234, 220))
    d.line([cx, y + h - 102, cx, y + h - 116], fill=(240, 234, 220), width=2)
    d.polygon([(cx, y + h - 116), (cx + 12, y + h - 112), (cx, y + h - 108)],
              fill=RED)
    d.rectangle([cx - 66, y + h - 14, cx + 66, y + h], fill=(200, 190, 170))
    for dx in (-44, -22, 22, 44):
        d.rectangle([cx + dx - 5, y + h - 58, cx + dx + 5, y + h - 14],
                    fill=(240, 234, 220))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=RED)
    d.text((x + 10, y + h - 24), "WASHINGTON", font=SANS_B(13), fill=LIGHT)


def art_gate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 240))
    d.ellipse([x + w - 52, y + 8, x + w - 12, y + 48], fill=(0, 51, 153))
    for i, a in enumerate(range(0, 360, 30)):
        sx = x + w - 32 + 13 * math.cos(math.radians(a))
        sy = y + 28 + 13 * math.sin(math.radians(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    cx = x + w // 2
    d.polygon([(cx - 78, y + 52), (cx, y + 34), (cx + 78, y + 52)], fill=(196, 164, 110))
    for i in range(6):
        px = cx - 65 + i * 26
        d.rectangle([px - 5, y + 54, px + 5, y + h - 30], fill=(222, 196, 142))
    d.rectangle([cx - 82, y + h - 30, cx + 82, y + h - 20], fill=(196, 164, 110))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(0, 0, 0))
    d.rectangle([x, y + h - 20, x + w // 3, y + h - 13], fill=RED)
    d.rectangle([x, y + h - 13, x + w // 3, y + h - 6], fill=(255, 204, 0))
    d.text((x + w // 3 + 8, y + h - 19), "BERLIN", font=SANS_B(13), fill=LIGHT)


def art_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 90, 110))
    cx, cy = x + w // 2, y + h // 2 - 6
    for r in (58, 44, 30, 17):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=560,
              fill=(255, 255, 255), width=5)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 190, 60))
    for i in range(14):
        rx = x + 12 + (i * 23) % (w - 24)
        ry = y + 12 + (i * 17) % (h - 40)
        d.line([rx, ry, rx - 6, ry + 12], fill=(180, 220, 235), width=2)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(232, 148, 52))
    d.text((x + 10, y + h - 24), "GOPALPUR · NOON", font=SANS_B(13), fill=(24, 24, 28))


def art_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 96, 58))
    cx, cy = x + w // 2, y + h // 2 - 4
    for i in range(12):
        a = math.radians(i * 30)
        d.line([cx, cy, cx + 78 * math.cos(a), cy + 78 * math.sin(a)],
               fill=(120, 190, 130), width=2)
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=(120, 200, 150))
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], outline=(255, 255, 255), width=3)
    d.polygon([(cx - 40, cy - 20), (cx - 10, cy - 34), (cx + 8, cy - 12),
               (cx - 6, cy + 6), (cx - 30, cy + 22), (cx - 44, cy + 4)],
              fill=(30, 96, 58))
    d.polygon([(cx + 12, cy + 8), (cx + 38, cy - 6), (cx + 44, cy + 18),
               (cx + 22, cy + 34), (cx + 6, cy + 26)], fill=(30, 96, 58))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 10, y + h - 24), "ANTALYA · 9–20 NOV", font=SANS_B(13), fill=INK)


def art_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    base = y + h - 34
    vals = [0.92, 0.78, 0.84, 0.62, 0.68, 0.44, 0.30]
    bw = (w - 24) // len(vals)
    for i, v in enumerate(vals):
        bx = x + 12 + i * bw
        bh = int((h - 52) * v)
        d.rectangle([bx + 2, base - bh, bx + bw - 3, base], fill=RED)
    pts = [(x + 12 + i * bw + bw // 2, base - int((h - 52) * v)) for i, v in enumerate(vals)]
    d.line(pts, fill=INK, width=3)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=INK)
    d.text((x + 10, y + h - 24), "WALL ST · 6TH DAY DOWN", font=SANS_B(13), fill=LIGHT)


def art_senate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 216))
    cx = x + w // 2
    d.polygon([(cx - 70, y + 40), (cx, y + 22), (cx + 70, y + 40)], fill=(180, 170, 150))
    for i in range(5):
        px = cx - 56 + i * 28
        d.rectangle([px - 5, y + 42, px + 5, y + h - 34], fill=(255, 255, 255),
                    outline=(160, 150, 130))
    d.rectangle([cx - 76, y + h - 34, cx + 76, y + h - 26], fill=(180, 170, 150))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=RED)
    d.text((x + 10, y + h - 24), "BLOCKED", font=SANS_B(13), fill=LIGHT)


def art_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 26))
    for i in range(46):
        sx = x + 8 + (i * 37) % (w - 16)
        sy = y + 8 + (i * 53) % (h - 40)
        r = 1 + (i % 3 == 0)
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    cx, cy = x + w // 2 + 18, y + h // 2 - 8
    d.line([cx - 52, cy + 34, cx - 8, cy + 6], fill=(200, 170, 90), width=3)
    d.pieslice([cx - 34, cy - 34, cx + 34, cy + 34], start=200, end=340,
               fill=(232, 196, 110))
    d.line([cx, cy, cx + 46, cy - 30], fill=(200, 170, 90), width=3)
    d.ellipse([cx + 42, cy - 34, cx + 50, cy - 26], fill=(255, 255, 255))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(255, 190, 60))
    d.text((x + 10, y + h - 24), "25.9 BILLION KM", font=SANS_B(13), fill=INK)


def art_atom(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 244))
    cx, cy = x + w // 2, y + h // 2 - 6
    for a in (0, 60, 120):
        d.arc([cx - 46, cy - 20, cx + 46, cy + 20], start=a, end=a + 180,
              fill=BLUE, width=3)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=BLUE)
    d.text((x + 10, y + h - 24), "VIENNA", font=SANS_B(13), fill=LIGHT)


def art_trade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 240))
    for i, col in enumerate([(178, 34, 34), (255, 255, 255), (36, 84, 160)]):
        d.rectangle([x + 18 + i * 34, y + 26, x + 44 + i * 34, y + h - 44], fill=col,
                    outline=(120, 120, 120))
    d.line([x + 18, y + h - 44, x + w - 18, y + 26], fill=INK, width=4)
    d.polygon([(x + w - 34, y + 22), (x + w - 14, y + 30), (x + w - 34, y + 38)],
              fill=INK)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=INK)
    d.text((x + 10, y + h - 24), "OTTAWA", font=SANS_B(13), fill=LIGHT)


def art_bank(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 224))
    cx = x + w // 2
    d.rectangle([cx - 52, y + 30, cx + 52, y + 44], fill=(120, 110, 90))
    for i in range(4):
        px = cx - 40 + i * 27
        d.rectangle([px - 4, y + 46, px + 4, y + h - 36], fill=(255, 255, 255),
                    outline=(140, 130, 110))
    d.rectangle([cx - 58, y + h - 36, cx + 58, y + h - 28], fill=(120, 110, 90))
    d.text((cx - 12, y + 62), "€", font=SANS_B(30), fill=GOLD)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=GOLD)
    d.text((x + 10, y + h - 24), "FRANKFURT", font=SANS_B(13), fill=INK)


def art_flag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 244, 238))
    d.rectangle([x + 16, y + 24, x + w - 16, y + h - 40], fill=(0, 140, 60))
    d.polygon([(x + w // 2, y + 30), (x + w - 24, y + h // 2),
               (x + w // 2, y + h - 46), (x + 24, y + h // 2)], fill=(255, 220, 0))
    d.ellipse([x + w // 2 - 16, y + h // 2 - 22, x + w // 2 + 16, y + h // 2 + 10],
              fill=(0, 40, 140))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(0, 140, 60))
    d.text((x + 10, y + h - 24), "BRASÍLIA", font=SANS_B(13), fill=LIGHT)


def art_pin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.ellipse([x + w // 2 - 26, y + 22, x + w // 2 + 26, y + 74], fill=RED)
    d.ellipse([x + w // 2 - 12, y + 34, x + w // 2 + 12, y + 58], fill=LIGHT)
    d.polygon([(x + w // 2 - 18, y + 66), (x + w // 2 + 18, y + 66),
               (x + w // 2, y + h - 34)], fill=RED)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=RED)
    d.text((x + 10, y + h - 24), "GEORGETOWN", font=SANS_B(13), fill=LIGHT)


def art_pill(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.rounded_rectangle([x + 14, y + 40, x + w - 14, y + h - 44], radius=16,
                        fill=(255, 255, 255), outline=RED, width=3)
    d.rounded_rectangle([x + 14, y + 40, x + w // 2, y + h - 44], radius=16, fill=RED)
    d.rectangle([x + w // 2 - 8, y + 40, x + w // 2, y + h - 44], fill=RED)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=RED)
    d.text((x + 10, y + h - 24), "ZURICH", font=SANS_B(13), fill=LIGHT)


def art_candles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 22, 44))
    base = y + h - 40
    # candlesticks: open/close bodies with wicks, last one a tall green close
    sticks = [(0.30, 0.55, 1), (0.55, 0.38, 0), (0.38, 0.62, 1),
              (0.62, 0.45, 0), (0.45, 0.78, 1), (0.78, 0.60, 1)]
    bw = (w - 24) // len(sticks)
    for i, (o, c, up) in enumerate(sticks):
        cx = x + 16 + i * bw + bw // 2
        top = base - int((h - 56) * max(o, c))
        bot = base - int((h - 56) * min(o, c))
        d.line([cx, base - int((h - 56) * o) - 8, cx, base - int((h - 56) * c) + 8],
               fill=(200, 200, 200), width=2)
        d.rectangle([cx - bw // 3, top, cx + bw // 3, bot],
                    fill=(34, 160, 90) if up else (200, 60, 60))
    d.text((x + 10, y + 8), "$97.17", font=SANS_B(22), fill=(255, 210, 90))
    d.text((x + 118, y + 14), "+17%", font=SANS_B(16), fill=(90, 220, 130))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(255, 210, 90))
    d.text((x + 10, y + h - 24), "NASDAQ · FIRST CLOSE", font=SANS_B(13), fill=INK)


def art_vicecity(d, x, y, w, h):
    for i, col in enumerate([(255, 120, 60), (255, 90, 120), (150, 60, 160),
                             (90, 40, 130)]):
        d.rectangle([x, y + i * (h - 26) // 4, x + w, y + (i + 1) * (h - 26) // 4],
                    fill=col)
    cx, cy = x + w // 2, y + 58
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(255, 210, 110))
    for bx, bh in [(0, 52), (34, 70), (74, 44), (116, 78), (160, 58),
                   (200, 84), (238, 50), (272, 66)]:
        d.rectangle([x + bx, y + h - 26 - bh, x + bx + 28, y + h - 26],
                    fill=(30, 16, 50))
    for px, lean in [(52, -14), (250, 12)]:
        d.line([x + px, y + h - 26, x + px + lean, y + h - 78], fill=(30, 16, 50),
               width=4)
        for a in (-50, -20, 10, 40):
            ex = x + px + lean + int(20 * math.cos(math.radians(a - 90)))
            ey = y + h - 78 + int(20 * math.sin(math.radians(a - 90)))
            d.line([x + px + lean, y + h - 78, ex, ey], fill=(30, 16, 50), width=3)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(255, 210, 110))
    d.text((x + 10, y + h - 24), "VICE CITY", font=SANS_B(13), fill=INK)


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 130, 70))
    d.rectangle([x + 30, y + 18, x + w - 30, y + h - 30], fill=(214, 186, 130))
    d.line([x + 30, y + 34, x + w - 30, y + 34], fill=LIGHT, width=2)
    d.line([x + 30, y + h - 46, x + w - 30, y + h - 46], fill=LIGHT, width=2)
    # stumps at each end
    for sx in (x + 62, x + w - 62):
        for dx in (-8, 0, 8):
            d.rectangle([sx + dx - 2, y + 40, sx + dx + 2, y + 62], fill=(255, 220, 60))
    # batsman: head, body, bat; red ball mid-pitch
    bx, by = x + w // 2 - 30, y + 66
    d.ellipse([bx - 9, by - 26, bx + 9, by - 8], fill=(20, 20, 24))
    d.line([bx, by - 8, bx - 2, by + 22], fill=(20, 20, 24), width=8)
    d.line([bx - 2, by + 22, bx - 14, by + 40], fill=(20, 20, 24), width=5)
    d.line([bx - 2, by + 22, bx + 10, by + 40], fill=(20, 20, 24), width=5)
    d.line([bx + 8, by - 2, bx + 34, by + 26], fill=(220, 190, 130), width=6)
    d.ellipse([x + w // 2 + 22, y + 74, x + w // 2 + 32, y + 84], fill=RED)
    d.text((x + w - 78, y + 8), "317/6", font=SANS_B(20), fill=LIGHT)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=LIGHT)
    d.text((x + 10, y + h - 24), "WELLINGTON · DAY 2", font=SANS_B(13), fill=INK)


def art_vote(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 216))
    d.text((x + 12, y + 8), "51–48", font=SANS_B(26), fill=INK)
    d.text((x + 118, y + 16), "WAR-POWERS VOTE", font=SANS_B(13), fill=GREY)
    d.rectangle([x + 12, y + 48, x + 12 + 158, y + 72], fill=RED)
    d.text((x + 18, y + 52), "51  AGAINST", font=SANS_B(15), fill=LIGHT)
    d.rectangle([x + 12, y + 78, x + 12 + 148, y + 102], fill=BLUE)
    d.text((x + 18, y + 82), "48  FOR", font=SANS_B(15), fill=LIGHT)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=RED)
    d.text((x + 10, y + h - 24), "SENATE · 51–48", font=SANS_B(13), fill=LIGHT)


def art_embassy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 214, 228))
    cx = x + w // 2
    d.polygon([(cx - 70, y + 52), (cx, y + 34), (cx + 70, y + 52)], fill=(150, 140, 120))
    for i in range(5):
        px = cx - 56 + i * 28
        d.rectangle([px - 5, y + 54, px + 5, y + h - 34], fill=(240, 236, 224),
                    outline=(120, 110, 90))
    d.rectangle([cx - 76, y + h - 34, cx + 76, y + h - 26], fill=(150, 140, 120))
    # Dutch flag (red-white-blue) and Austrian flag (red-white-red) on poles
    for fx, bands in [(x + 14, [(178, 34, 34), LIGHT, (36, 84, 160)]),
                      (x + w - 54, [(178, 34, 34), LIGHT, (178, 34, 34)])]:
        d.line([fx, y + 12, fx, y + 52], fill=INK, width=2)
        for j, col in enumerate(bands):
            d.rectangle([fx, y + 12 + j * 10, fx + 40, y + 22 + j * 10], fill=col)
    # strike flash
    sx, sy = x + w - 84, y + 66
    d.polygon([(sx, sy - 14), (sx + 5, sy - 4), (sx + 15, sy - 6), (sx + 7, sy + 2),
               (sx + 10, sy + 12), (sx, sy + 6), (sx - 10, sy + 12), (sx - 7, sy + 2),
               (sx - 15, sy - 6), (sx - 5, sy - 4)], fill=(255, 190, 60))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=BLUE)
    d.text((x + 10, y + h - 24), "KYIV", font=SANS_B(13), fill=LIGHT)


def art_flags3(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    # US flag
    fx = x + 16
    for j in range(7):
        d.rectangle([fx, y + 24 + j * 9, fx + 72, y + 33 + j * 9],
                    fill=RED if j % 2 == 0 else LIGHT)
    d.rectangle([fx, y + 24, fx + 30, y + 51], fill=(36, 60, 140))
    # China flag
    fx = x + 114
    d.rectangle([fx, y + 24, fx + 72, y + 87], fill=(222, 40, 30))
    d.ellipse([fx + 12, y + 32, fx + 28, y + 48], fill=(255, 220, 60))
    # Russia flag
    fx = x + 212
    for j, col in enumerate([LIGHT, (36, 84, 160), RED]):
        d.rectangle([fx, y + 24 + j * 21, fx + 72, y + 45 + j * 21], fill=col)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=RED)
    d.text((x + 10, y + h - 24), "SHENZHEN", font=SANS_B(13), fill=LIGHT)


def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 26, 48))
    cx, cy = x + w // 2, y + h // 2 - 8
    for i in range(5):
        px = cx - 44 + i * 22
        d.line([px, cy - 58, px, cy - 40], fill=(120, 200, 130), width=3)
        d.line([px, cy + 40, px, cy + 58], fill=(120, 200, 130), width=3)
        py = cy - 44 + i * 22
        d.line([cx - 58, py, cx - 40, py], fill=(120, 200, 130), width=3)
        d.line([cx + 40, py, cx + 58, py], fill=(120, 200, 130), width=3)
    d.rectangle([cx - 40, cy - 40, cx + 40, cy + 40], fill=(34, 160, 90),
                outline=(120, 220, 140), width=2)
    d.rectangle([cx - 24, cy - 24, cx + 24, cy + 24], fill=(20, 90, 55))
    d.text((cx - 13, cy - 13), "AI", font=SANS_B(24), fill=LIGHT)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(34, 160, 90))
    d.text((x + 10, y + h - 24), "CALIFORNIA", font=SANS_B(13), fill=LIGHT)


def art_boat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 90, 130))
    cx, cy = x + w // 2, y + h // 2 - 4
    d.ellipse([cx + 62, cy - 52, cx + 96, cy - 18], fill=(255, 210, 110))
    d.polygon([(cx - 92, cy + 6), (cx + 92, cy + 6), (cx + 66, cy + 30),
               (cx - 66, cy + 30)], fill=(150, 100, 50))
    d.line([cx - 6, cy + 6, cx - 6, cy - 34], fill=(120, 80, 40), width=4)
    d.polygon([(cx - 6, cy - 34), (cx + 34, cy + 2), (cx - 6, cy + 2)],
              fill=(240, 234, 220))
    for wy in (cy + 40, cy + 52):
        for wx in range(x + 8, x + w - 8, 34):
            d.arc([wx, wy, wx + 30, wy + 16], start=200, end=340,
                  fill=(200, 230, 245), width=3)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(255, 210, 110))
    d.text((x + 10, y + h - 24), "YENNE · SENEGAL", font=SANS_B(13), fill=INK)


def art_drought(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 190, 120))
    d.ellipse([x + w - 78, y + 10, x + w - 18, y + 70], fill=(255, 150, 40))
    for i in range(8):
        a = math.radians(i * 45)
        d.line([x + w - 48 + 34 * math.cos(a), y + 40 + 34 * math.sin(a),
                x + w - 48 + 46 * math.cos(a), y + 40 + 46 * math.sin(a)],
               fill=(255, 150, 40), width=3)
    # cracked dry earth
    for (x1, y1, x2, y2) in [(30, 96, 90, 78), (90, 78, 150, 96), (150, 96, 210, 80),
                             (210, 80, 268, 98), (90, 78, 110, 108),
                             (150, 96, 140, 114), (210, 80, 232, 108)]:
        d.line([x + x1, y + y1, x + x2, y + y2], fill=(120, 70, 30), width=3)
    # dry tree
    d.line([x + 52, y + 96, x + 52, y + 56], fill=(110, 70, 40), width=5)
    d.line([x + 52, y + 72, x + 30, y + 52], fill=(110, 70, 40), width=3)
    d.line([x + 52, y + 66, x + 74, y + 46], fill=(110, 70, 40), width=3)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(200, 110, 40))
    d.text((x + 10, y + h - 24), "TONGA", font=SANS_B(13), fill=LIGHT)


def art_baseball(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 130, 70))
    cx, cy = x + w // 2, y + h // 2 + 6
    d.polygon([(cx, cy - 52), (cx + 52, cy), (cx, cy + 28), (cx - 52, cy)],
              fill=(214, 186, 130))
    for dx, dy in [(0, -52), (52, 0), (0, 28), (-52, 0)]:
        d.rectangle([cx + dx - 6, cy + dy - 6, cx + dx + 6, cy + dy + 6],
                    fill=LIGHT, outline=GREY)
    bx, by = cx + 88, cy - 46
    d.ellipse([bx - 22, by - 22, bx + 22, by + 22], fill=LIGHT, outline=GREY)
    d.arc([bx - 16, by - 16, bx + 16, by + 16], start=300, end=60, fill=RED, width=3)
    d.arc([bx - 16, by - 16, bx + 16, by + 16], start=120, end=240, fill=RED, width=3)
    d.text((x + 12, y + 8), "4,256", font=SANS_B(22), fill=LIGHT)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=LIGHT)
    d.text((x + 10, y + h - 24), "CINCINNATI", font=SANS_B(13), fill=INK)


ART = {"capitol": art_capitol, "gate": art_gate, "storm": art_storm,
       "globe": art_globe, "chart": art_chart, "senate": art_senate,
       "space": art_space, "atom": art_atom, "trade": art_trade,
       "bank": art_bank, "flag": art_flag, "pin": art_pin, "pill": art_pill,
       "candles": art_candles, "vicecity": art_vicecity,
       "cricket": art_cricket, "vote": art_vote, "embassy": art_embassy,
       "flags3": art_flags3, "chip": art_chip, "boat": art_boat,
       "drought": art_drought, "baseball": art_baseball}


# ---------------- world map ----------------
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-150, 60)],
    [(-58, 64), (-45, 60), (-32, 68), (-22, 70), (-30, 76), (-58, 76)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -40), (-70, -52), (-73, -37), (-80, -20), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -25), (28, -33), (18, -35),
     (12, -18), (9, 4), (-8, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (18, 56),
     (21, 55), (28, 59), (30, 70), (40, 68), (55, 69), (70, 73), (90, 75),
     (110, 76), (130, 72), (150, 70), (170, 66), (178, 65), (162, 60),
     (158, 52), (142, 50), (140, 40), (135, 35), (130, 33), (127, 35),
     (122, 38), (120, 32), (110, 20), (105, 10), (100, 8), (97, 16),
     (92, 21), (88, 22), (80, 13), (76, 8), (72, 20), (66, 25), (60, 25),
     (57, 26), (52, 28), (48, 30), (43, 29), (39, 21), (35, 29), (34, 31),
     (30, 36), (26, 40), (23, 36), (19, 42), (12, 44), (8, 44), (3, 43),
     (-2, 37), (-9, 37)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
     (135, -12), (132, -12), (126, -14), (122, -17)],
    [(95, 5), (100, 0), (104, -2), (110, -7), (114, -8), (119, -5), (122, 0),
     (120, 10), (115, 5), (105, 2), (100, 8)],
    # Britain, Japan, New Zealand (small but recognisable at this scale)
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 57), (1, 51), (-3, 50)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (141, 44), (143, 42), (140, 38), (136, 35), (132, 32)],
    [(167, -45), (170, -42), (174, -39), (177, -38), (175, -41), (172, -43),
     (168, -46)],
]
# feature number -> (lon, lat) pin.
# PIN_DX: badge offset in px from the true spot (leader line) where pins
# would otherwise overlap — the US east coast (3, 6, 7, 13) and Miami (4).
# A small dot marks the true spot; the numbered badge sits at the end of
# the leader line.
PINS = {1: (85, 19), 2: (30.7, 36.9), 3: (-74, 41), 4: (-80, 26),
        5: (174.8, -41.3), 6: (-77, 39), 7: (-77, 39), 8: (30.5, 50.4),
        9: (114, 22.5), 10: (-122, 37), 11: (-17.4, 14.7), 12: (-175, -21),
        13: (-84.5, 39.1)}
PIN_DX = {2: (30, 18), 3: (20, -16), 4: (-4, 20), 6: (-28, 12), 7: (26, 12),
          8: (-28, -16), 12: (44, -18), 13: (-26, -16)}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 220, 232))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)

    def px(lon, lat):
        return (x + 4 + (lon + 170) / 360.0 * (w - 8),
                y + 4 + (78 - lat) / 136.0 * (h - 8))

    # graticule, every 30 degrees
    for lon in range(-150, 181, 30):
        gx, _ = px(lon, 0)
        d.line([gx, y + 1, gx, y + h - 1], fill=(175, 198, 212), width=1)
    for lat in (-60, -30, 0, 30, 60):
        _, gy = px(0, lat)
        d.line([x + 1, gy, x + w - 1, gy], fill=(175, 198, 212), width=1)
    for poly in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in poly], fill=(222, 196, 142),
                  outline=(160, 130, 90))
    # ocean + continent labels (small caps, out of the pins' way)
    lab_ocean = SANS_B(10)
    for (lon, lat), text in [((-150, 0), "PACIFIC"), ((-30, 10), "ATLANTIC"),
                             ((80, -25), "INDIAN OCEAN")]:
        lx, ly = px(lon, lat)
        d.text((lx - lab_ocean.getlength(text) / 2, ly - 5), text,
               font=lab_ocean, fill=(96, 124, 148))
    lab_land = SANS_B(10)
    for (lon, lat), text in [((-140, 65), "NORTH AMERICA"), ((20, 5), "AFRICA"),
                             ((90, 45), "ASIA"), ((134, -25), "AUSTRALIA"),
                             ((-75, -20), "S. AMERICA")]:
        lx, ly = px(lon, lat)
        d.text((lx - lab_land.getlength(text) / 2, ly - 5), text,
               font=lab_land, fill=(148, 122, 82))
    fnum = SANS_B(11)
    for n, (lon, lat) in PINS.items():
        cx, cy = px(lon, lat)
        # keep the true-spot dot inside the map (Tonga sits past its edge)
        cx = max(x + 10, min(x + w - 10, cx))
        cy = max(y + 10, min(y + h - 10, cy))
        dx, dy = PIN_DX.get(n, (0, 0))
        if dx or dy:
            bx, by = cx + dx, cy + dy
            d.line([cx, cy, bx, by], fill=RED, width=1)
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
            cx, cy = bx, by
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=LIGHT, width=1)
        tw = fnum.getlength(str(n))
        d.text((cx - tw / 2, cy - 6), str(n), font=fnum, fill=LIGHT)
    d.text((x + 8, y + h - 15), "PINS MARK THE 13 FEATURE STORIES · POSITIONS APPROXIMATE",
           font=SANS(10), fill=(40, 60, 80))


# ---------------- page ----------------

def feature_card(d, x, y, w, h, feat, headline_size=17, deck_size=12, art=True,
                 art_frac=0.52, deck_lines=2, art_caption=True):
    num, region, kicker, headline, deck, artkey = feat
    d.rectangle([x, y, x + w, y + h], fill=LIGHT, outline=(200, 200, 200), width=1)
    if art:
        ah = int(h * art_frac)
        # draw the flat art on a fixed logical canvas, then scale to the box
        tmp = Image.new("RGB", (300, 140), PAPER)
        td = ImageDraw.Draw(tmp)
        ART[artkey](td, 0, 0, 300, 140)
        if not art_caption:
            # drop the art's own caption band (the kicker below already
            # names the place): crop to the scene, then scale.
            tmp = tmp.crop((0, 0, 300, 114))
        tmp = tmp.resize((w - 2, ah), Image.LANCZOS)
        d._image.paste(tmp, (x + 1, y + 1))
        ty = y + ah + 8
    else:
        d.rectangle([x, y, x + w, y + 6], fill=REGION_COLOR[region])
        ty = y + 12
    d.text((x + 8, ty), f"{num}. {kicker}", font=SANS_B(11),
           fill=REGION_COLOR[region])
    ty += 16
    hl = fit_lines(headline, SANS_B(headline_size), w - 16, 2)
    for ln in hl:
        d.text((x + 8, ty), ln, font=SANS_B(headline_size), fill=INK)
        ty += headline_size + 4
    ty += 1
    for ln in fit_lines(deck, SANS(deck_size), w - 16, deck_lines):
        d.text((x + 8, ty), ln, font=SANS(deck_size), fill=(60, 60, 64))
        ty += deck_size + 4
    assert ty <= y + h - 2, f"card {num} overflows by {ty - (y + h)}px"


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.text((16, 8), "THE WORLD TODAY", font=SERIF_B, fill=LIGHT)
    d.text((16, 62), "FRIDAY 20 NOVEMBER 2026", font=SANS_B(20), fill=(255, 190, 60))
    sub = "Akvan hits Odisha  ·  Anthropic's first close  ·  GTA VI's first full day"
    tw = SANS(15).getlength(sub)
    d.text((W - 16 - tw, 64), sub, font=SANS(15), fill=(210, 220, 235))
    d.rectangle([0, 88, W, 92], fill=RED)

    # --- region strip ---
    counts = {r: 0 for r in REGION_ORDER}
    for _, r, *_ in FEATURES:
        counts[r] += 1
    for r, _ in BRIEFS:
        counts[r] += 1
    assert sum(counts.values()) == 31, counts
    y = 92
    x = 16
    d.text((x, y + 7), "31 STORIES ·", font=SANS_B(15), fill=INK)
    x += SANS_B(15).getlength("31 STORIES · ") + 6
    for r in REGION_ORDER:
        label = f"{r} {counts[r]}"
        fw = SANS_B(14).getlength(label) + 18
        d.rounded_rectangle([x, y + 3, x + fw, y + 25], radius=11,
                            fill=REGION_COLOR[r])
        d.text((x + 9, y + 7), label, font=SANS_B(14), fill=LIGHT)
        x += fw + 8
    d.text((x + 2, y + 7), "ONE PAGE", font=SANS_B(15), fill=INK)

    # --- hero row: features 1-3 ---
    y = 118
    hw, gap = 325, 8
    for i in range(3):
        feature_card(d, 16 + i * (hw + gap), y, hw, 190, FEATURES[i],
                     headline_size=18, deck_size=12, art_frac=0.46)
    y = 308

    # --- numbers strip ---
    nw = (W - 32 - 5 * 8) // 6
    for i, (num, label) in enumerate(NUMBERS):
        nx = 16 + i * (nw + 8)
        d.rectangle([nx, y, nx + nw, y + 52], fill=LIGHT,
                    outline=(200, 200, 200), width=1)
        d.rectangle([nx, y, nx + nw, y + 5], fill=RED)
        nf = SANS_B(25)
        tw = nf.getlength(num)
        d.text((nx + (nw - tw) / 2, y + 10), num, font=nf, fill=INK)
        lf = SANS_B(10)
        tw = lf.getlength(label)
        d.text((nx + (nw - tw) / 2, y + 38), label, font=lf, fill=GREY)
    y = 368

    # --- feature row A: features 4-7 ---
    fw4 = (W - 32 - 3 * 8) // 4
    for i in range(4):
        feature_card(d, 16 + i * (fw4 + 8), y, fw4, 124, FEATURES[3 + i],
                     headline_size=14, deck_size=11, art_frac=0.44, deck_lines=1)
    y = 500

    # --- feature row B: features 8-13 (illustrated like the rest now) ---
    fw6 = (W - 32 - 5 * 8) // 6
    for i in range(6):
        feature_card(d, 16 + i * (fw6 + 8), y, fw6, 160, FEATURES[7 + i],
                     headline_size=12, deck_size=10, art=True, art_frac=0.44,
                     art_caption=False)
    y = 668

    # --- map ---
    draw_map(d, 16, y, W - 32, 92)
    y = 760

    # --- briefs header ---
    d.text((16, y), "THE DAY IN BRIEF", font=SANS_B(14), fill=INK)
    d.line([16, y + 20, W - 16, y + 20], fill=INK, width=1)
    y += 26

    # --- briefs: 3 columns, 8 rows each ---
    cols = [BRIEFS[i::3] for i in range(3)]
    bf = SANS(13)
    cw = (W - 32 - 2 * 16) // 3
    max_lines = max(len(c) for c in cols)
    for ci, col in enumerate(cols):
        cx = 16 + ci * (cw + 16)
        by = y
        for region, text in col:
            line = "• " + text
            assert bf.getlength(line) <= cw, f"BRIEF TOO LONG: {line!r}"
            d.text((cx, by), "•", font=bf, fill=REGION_COLOR[region])
            d.text((cx + 13, by), text, font=bf, fill=INK)
            by += 20
    y += max_lines * 20 + 4

    # --- date check box ---
    d.rectangle([16, y, W - 16, y + 34], outline=RED, width=2)
    d.text((24, y + 4), "DATE CHECK", font=SANS_B(12), fill=RED)
    rest = DATE_CHECK[len("DATE CHECK — "):]
    lines = fit_lines(rest, SANS(11), W - 32 - SANS_B(12).getlength("DATE CHECK  ") - 8, 2)
    ly = y + 3
    d.text((24 + SANS_B(12).getlength("DATE CHECK  "), ly), lines[0],
           font=SANS(11), fill=INK)
    if len(lines) > 1:
        d.text((24, ly + 14), lines[1], font=SANS(11), fill=INK)
    y += 42

    # --- footer ---
    d.rectangle([0, y, W, H], fill=NAVY)
    d.text((16, y + 6),
           "31 STORIES · FIVE REGIONS · ONE PAGE — Every story verified from reports of Friday 20 November 2026",
           font=SANS_B(12), fill=LIGHT)
    d.text((16, y + 22), "Sources: Reuters · BBC · AP · IMD · UN News · make.fun news-image-20261120",
           font=SANS(11), fill=(180, 195, 215))
    assert y + 40 <= H, f"page overflow: footer ends {y + 40}"
    return img


if __name__ == "__main__":
    im = build()
    im.save("entry.png", "JPEG", quality=88)
    print("saved entry.png", im.size)
