"""Digital studies for the three landscape plates of "Movement, Water, Connection":
i. Movement (Vale Carapito), ii. Water (Paul de Toirões), iii. Connection (Côa
gorge and Penascosa). Same surface, line and colour as digital_plates.py.

The landscapes are schematic, as an Iron Age engraver might set them down:
hill lines, fishbone trees (the rare arboriform motif, Reis 2013), animals in
profile with parallel-stroke bodies, water as broken wavy lines.

These are digital studies, not the hand-made plates.

Run from the repo root:  conda run -n coa python scripts/digital_landscapes.py
Writes img/digital-studies/digital-study-{movement,water,connection}.jpg; copy them to
img/movement.jpg, img/water.jpg and img/connection.jpg to update the page.
"""
import numpy as np
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union

from digital_plates import CREDIT, OUT, Plate, ellipse, schist, smooth

BOX = (0, 0, 1000, 1250)  # figure units for a full 4:5 landscape


# ---------------------------------------------------------------------------
# Motifs, in local units (feet on y = 0, facing right), placed at (x, y) with scale s
# ---------------------------------------------------------------------------
def place(pts, x, y, s, face=1):
    pts = np.asarray(pts, float)
    return np.column_stack([x + face * s * pts[:, 0], y + s * pts[:, 1]])


def clear_of(line, avoid):
    """The parts of a line that stay clear of the figures, so lines never run through them."""
    if avoid is None:
        return [np.asarray(line)]
    rest = LineString(line).difference(avoid)
    return [np.asarray(g.coords) for g in getattr(rest, "geoms", [rest]) if not g.is_empty and g.length > 8]


def body_lines(p, outline, angle=80, spacing=9, s=1.0):
    p.grid(Polygon(outline).buffer(-2.5 * s), spacing=spacing * s, angles=(angle,), width=1.4)


def legs(p, x, y, s, face, pairs, width=2.2):
    for top, bottom in pairs:
        p.cut(place([top, bottom], x, y, s, face), width, overshoot=3)


def horse(p, x, y, s=1.0, face=1, rider=False):
    """Long body, small head, single-line legs: the Iron Age horse of the Côa."""
    body = smooth(place([(-44, 60), (-10, 66), (26, 64), (40, 64), (50, 80), (58, 88), (72, 80), (80, 70),
                         (72, 66), (58, 72), (50, 58), (44, 46), (18, 40), (-22, 40), (-46, 46)], x, y, s, face),
                  closed=True, lump=1.5 * s)
    p.outline(body, 2.4)
    body_lines(p, body, s=s)
    p.cut(place([(57, 88), (56, 97)], x, y, s, face), 1.8, overshoot=2)                   # ear
    for k in range(3):                                                                      # mane
        p.cut(place([(42 + 4 * k, 68 + 6 * k), (36 + 4 * k, 75 + 6 * k)], x, y, s, face), 1.4, passes=1)
    legs(p, x, y, s, face, [((-36, 42), (-40, 0)), ((-26, 40), (-22, 0)), ((30, 42), (34, 0)), ((40, 46), (46, 0))])
    p.cut(smooth(place([(-44, 58), (-56, 34), (-52, 14)], x, y, s, face), lump=1), 2.2)   # tail
    if rider:
        p.cut(place([(10, 66), (12, 104)], x, y, s, face), 2.2)
        p.outline(ellipse(*place([(12, 112)], x, y, s, face)[0], 6 * s, 7 * s, 30), 2.0)
        p.cut(place([(12, 94), (40, 108)], x, y, s, face), 1.8)                            # spear arm
        p.cut(place([(30, 96), (60, 128)], x, y, s, face), 1.6)                            # spear


def tauros(p, x, y, s=1.0, face=1):
    """Heavy body, lowered head, lyre horns."""
    body = smooth(place([(-48, 56), (0, 62), (34, 62), (48, 68), (62, 58), (74, 46), (78, 36), (68, 32),
                         (56, 38), (44, 30), (0, 26), (-46, 30), (-52, 44)], x, y, s, face), closed=True, lump=1.5 * s)
    p.outline(body, 2.6)
    body_lines(p, body, s=s)
    p.cut(smooth(place([(62, 56), (70, 70), (84, 74)], x, y, s, face), lump=0.5), 2.0)
    p.cut(smooth(place([(58, 58), (60, 74), (72, 82)], x, y, s, face), lump=0.5), 2.0)
    legs(p, x, y, s, face, [((-40, 30), (-42, 0)), ((-28, 28), (-26, 0)), ((30, 30), (32, 0)), ((40, 32), (44, 0))])
    p.cut(smooth(place([(-52, 50), (-58, 26), (-56, 10)], x, y, s, face), lump=1), 1.8)
    p.cut(place([(-60, 12), (-52, 6)], x, y, s, face), 2.0, passes=1)                   # tail tuft


def wolf(p, x, y, s=1.0, face=1):
    body = smooth(place([(-34, 40), (0, 44), (30, 46), (42, 52), (52, 60), (56, 70), (61, 60), (66, 68), (68, 56),
                         (86, 48), (72, 42), (56, 40), (38, 30), (0, 26), (-34, 28)], x, y, s, face),
                  closed=True, lump=1.2 * s)
    p.outline(body, 2.4)
    body_lines(p, body, s=s)
    legs(p, x, y, s, face, [((-28, 28), (-34, 0)), ((-18, 27), (-14, 0)), ((30, 30), (34, 0)), ((38, 34), (44, 0))])
    tail = smooth(place([(-34, 38), (-50, 30), (-60, 10), (-52, 8), (-44, 22), (-32, 30)], x, y, s, face),
                  closed=True, lump=0.8 * s)
    p.outline(tail, 2.0)


def heron(p, x, y, s=1.0, face=1):
    body = smooth(place([(-24, 70), (0, 84), (26, 82), (32, 74), (12, 62), (-22, 62)], x, y, s, face),
                  closed=True, lump=1 * s)
    p.outline(body, 2.4)
    body_lines(p, body, angle=20, s=s)
    p.cut(smooth(place([(26, 80), (34, 96), (24, 108), (30, 122)], x, y, s, face), lump=0.5), 2.4)
    p.outline(ellipse(*place([(36, 124)], x, y, s, face)[0], 7 * s, 5 * s, 30), 2.0)
    p.cut(place([(42, 124), (68, 118)], x, y, s, face), 2.0, overshoot=2)                # beak
    p.cut(place([(34, 128), (14, 132)], x, y, s, face), 1.4, passes=1)                   # crest
    legs(p, x, y, s, face, [((4, 62), (2, 0)), ((12, 62), (18, 0))], width=1.8)
    p.cut(place([(-22, 66), (-40, 58)], x, y, s, face), 1.6, passes=1)


def duck(p, x, y, s=1.0, face=1):
    body = smooth(place([(-18, 2), (16, 2), (24, 10), (16, 16), (20, 26), (28, 26), (34, 22), (28, 18), (22, 14),
                         (-6, 14), (-20, 10)], x, y, s, face), closed=True, lump=0.8 * s)
    p.outline(body, 2.0)


def bird_flying(p, x, y, s=1.0):
    p.cut(smooth(place([(-20, 4), (-10, 10), (0, 0)], x, y, s), lump=0.5), 1.8, passes=2)
    p.cut(smooth(place([(0, 0), (10, 10), (20, 4)], x, y, s), lump=0.5), 1.8, passes=2)


def vulture(p, x, y, s=1.0):
    wing = [(-90, 6), (-60, 14), (-20, 10), (0, 4), (20, 10), (60, 14), (90, 6)]
    p.cut(smooth(place(wing, x, y, s), lump=1), 2.4)
    for k in range(-80, 90, 18):                                                         # primaries
        p.cut(place([(k, 8), (k + 4 * np.sign(k), -4)], x, y, s), 1.4, passes=1, overshoot=2)
    p.outline(smooth(place([(-10, 6), (0, 12), (10, 6), (6, -14), (-6, -14)], x, y, s), closed=True, lump=0.5), 2.0)


def tree(p, x, y, s=1.0):
    """Fishbone tree: a trunk with paired upward branches."""
    h = 90 * s
    p.cut([(x, y), (x + p.rng.normal(0, 2), y + h)], 2.4, overshoot=4)
    for k in range(5):
        yy = y + h * (0.35 + 0.13 * k)
        ln = (30 - 5 * k) * s
        p.cut([(x, yy), (x - ln, yy + ln * 0.7)], 1.7, passes=1, overshoot=3)
        p.cut([(x, yy), (x + ln, yy + ln * 0.7)], 1.7, passes=1, overshoot=3)


def shrub(p, x, y, s=1.0):
    p.cut(smooth([(x - 18 * s, y), (x - 10 * s, y + 18 * s), (x + 4 * s, y + 22 * s), (x + 18 * s, y)], lump=1), 1.8)
    for k in (-8, 0, 8):
        p.cut([(x + k * s, y), (x + k * 1.4 * s, y + 14 * s)], 1.3, passes=1, overshoot=2)


def reeds(p, x0, x1, y, rng, n=14, h=80):
    for x in np.linspace(x0, x1, n) + rng.normal(0, 6, n):
        hh = h * rng.uniform(0.6, 1.2)
        lean = rng.normal(0, 6)
        p.cut([(x, y), (x + lean, y + hh)], 1.6, passes=1, overshoot=3)
        if rng.random() < 0.5:   # seed head
            p.outline(ellipse(x + lean, y + hh + 7, 3, 9, 20), 1.6)


def grass(p, x0, x1, y, rng, n=20):
    for x in rng.uniform(x0, x1, n):
        p.cut([(x, y), (x + rng.normal(0, 3), y + rng.uniform(8, 18))], 1.3, passes=1, overshoot=2)


def hills(p, ys, rng, amp=40):
    for i, y in enumerate(ys):
        xs = np.linspace(-20, 1020, 9)
        pts = np.column_stack([xs, y + amp * np.sin(xs / (180 + 60 * i) + i * 1.7) + rng.normal(0, 8, len(xs))])
        p.outline(smooth(pts, lump=4), 2.6 - 0.3 * i)


def water(p, y0, y1, rng, x0=60, x1=940, rows=9, avoid=None):
    """Open water: broken wavy lines, shorter and fainter towards the far bank."""
    for i, y in enumerate(np.linspace(y0, y1, rows)):
        x = x0 + rng.uniform(0, 60)
        while x < x1:
            ln = rng.uniform(60, 160)
            xs = np.linspace(x, min(x + ln, x1), 12)
            for piece in clear_of(np.column_stack([xs, y + 5 * np.sin(xs / 18 + i)]), avoid):
                p.cut(piece, 1.9 - 0.08 * i, passes=1, overshoot=0)
            x += ln + rng.uniform(15, 50)


# ---------------------------------------------------------------------------
# i. Movement: Vale Carapito, herbivores and a predator in an open mosaic
# ---------------------------------------------------------------------------
def movement():
    p = Plate(seed=41, box=BOX)
    r = p.rng
    hills(p, [1020, 930], r, amp=35)
    for x, y, s in [(90, 900, 1.0), (180, 880, 0.8), (820, 850, 1.1), (900, 870, 0.8), (560, 860, 0.7)]:
        tree(p, x, y, s)
    for x, y in [(300, 860), (690, 840), (420, 520), (860, 560), (120, 380)]:
        shrub(p, x, y, 1.0)
    horse(p, 200, 620, 1.9)
    horse(p, 470, 640, 1.6, rider=False)
    horse(p, 790, 600, 1.4, face=-1)
    tauros(p, 330, 360, 2.0)
    tauros(p, 640, 330, 1.7, face=-1)
    wolf(p, 860, 160, 1.5, face=-1)
    for y in (600, 330, 140):
        grass(p, 30, 970, y, r, n=18)
    for x, y in [(380, 1120), (420, 1150), (460, 1128)]:
        bird_flying(p, x, y, 1.2)
    return p


# ---------------------------------------------------------------------------
# ii. Water: Paul de Toirões, a wetland coming back after drainage and damming
# ---------------------------------------------------------------------------
def wetland():
    p = Plate(seed=53, box=BOX)
    r = p.rng
    hills(p, [1060, 980], r, amp=28)
    p.outline(smooth([(-20, 880), (300, 900), (640, 870), (1020, 890)], lump=3), 2.4)         # far bank
    p.outline(smooth([(-20, 420), (260, 440), (600, 410), (1020, 430)], lump=3), 2.4)         # near bank
    heron(p, 560, 470, 2.0)
    ducks = [(300, 700), (370, 680), (430, 712)]
    for x, y in ducks:
        duck(p, x, y, 1.4)
    reeds(p, 20, 250, 520, r, n=15, h=150)
    reeds(p, 770, 990, 540, r, n=13, h=140)
    # open water, kept clear of the reed beds, the heron and the ducks
    avoid = unary_union([box(0, 500, 280, 760), box(745, 520, 1000, 780),
                         box(498, 545, 648, 735), box(600, 690, 712, 742)]
                        + [box(x - 32, y - 10, x + 52, y + 46) for x, y in ducks])
    water(p, 470, 850, r, rows=11, avoid=avoid)
    # the old drainage below the near bank: straight ditches, cut once and left to fade
    for k, y in enumerate([340, 280, 220]):
        x = 380
        while x < 960 - 110 * k:
            p.cut([(x, y), (x + 50, y)], 1.6, passes=1, overshoot=0)
            x += 50 + 20 + 22 * k
    p.cut([(360, 370), (360, 190)], 2.2)                                                     # sluice post
    p.cut([(330, 370), (390, 370)], 2.2)
    reeds(p, 40, 300, 160, r, n=12, h=120)                                                   # reeds taking the fields back
    grass(p, 380, 960, 140, r, n=24)
    for x, y in [(200, 1170), (240, 1200), (280, 1180), (700, 1150), (740, 1130)]:
        bird_flying(p, x, y, 1.3)
    return p


# ---------------------------------------------------------------------------
# iii. Connection: the Côa gorge, Penascosa, terraces and 25,000 years of people
# ---------------------------------------------------------------------------
def gorge():
    p = Plate(seed=67, box=BOX)
    # the rims stay outside the river all the way down, so each wall is one clean shape
    left = smooth([(-20, 1080), (100, 960), (230, 760), (330, 520), (400, 300), (440, 140)], lump=4)
    right = smooth([(1020, 1060), (900, 960), (780, 780), (690, 560), (640, 320), (610, 140)], lump=4)
    river = smooth([(522, 120), (502, 260), (548, 420), (520, 560), (560, 720), (540, 900)], lump=1.5)
    bank_l, bank_r = river - [16, 0], river + [16, 0]
    p.outline(left, 2.8)
    p.outline(right, 2.8)
    p.outline(bank_l, 2.4)
    p.outline(bank_r, 2.4)
    for t_ in np.linspace(0.1, 0.9, 6):                                                    # current
        i = int(t_ * (len(river) - 1))
        p.cut([river[i] - [9, 0], river[i] + [9, 0]], 1.4, passes=1, overshoot=0)
    # rim from the top down, then the bank from the gorge floor back up: one ring per wall
    wall_l = Polygon(np.vstack([left, bank_l])).buffer(0)
    wall_r = Polygon(np.vstack([right, bank_r])).buffer(0)
    # the Penascosa panel on the left wall: a tilted slab with a small engraved horse
    slab = np.array([(356, 520), (480, 544), (486, 628), (362, 610)], float)
    p.outline(np.vstack([slab, slab[:1]]), 2.4)
    horse(p, 420, 550, 0.52)
    # terraces where the right wall opens out: the long human history of the slopes
    terr = []
    for k in range(4):
        y = 900 - 50 * k
        x0 = 600 + 10 * k
        for piece in [g for g in [LineString([(x0, y), (x0 + 120, y + 4), (x0 + 260, y - 2)]).intersection(wall_r.buffer(-16))]
                      if not g.is_empty]:
            for g in getattr(piece, "geoms", [piece]):
                c = np.asarray(g.coords)
                p.cut(c, 2.0, passes=2, overshoot=0)
                for vx in np.linspace(c[0][0] + 12, c[-1][0] - 12, max(2, int((c[-1][0] - c[0][0]) / 26))):
                    p.cut([(vx, y + 3), (vx, y + 16)], 1.3, passes=1, overshoot=2)       # vines
                terr.append(box(c[0][0] - 10, y - 12, c[-1][0] + 10, y + 26))
    # strata on the gorge walls, dipping with the schist, kept clear of the panel and the terraces
    keep_clear = unary_union([Polygon(slab).buffer(14)] + terr)
    p.grid(wall_l.buffer(-10).difference(keep_clear), spacing=24, angles=(-24,), width=1.5)
    p.grid(wall_r.buffer(-10).difference(keep_clear), spacing=24, angles=(24,), width=1.5)
    # a walker on the path above the gorge, and a vulture in the updraught
    path = smooth([(40, 1110), (200, 1070), (360, 1100)], lump=2)
    p.cut(path, 1.8, passes=2)
    p.cut([(230, 1082), (230, 1132)], 2.2)                                                 # walker
    p.outline(ellipse(230, 1142, 6, 7, 30), 1.8)
    p.cut([(230, 1122), (248, 1106)], 1.6)
    p.cut([(248, 1106), (252, 1076)], 1.6)                                                 # staff
    p.cut([(230, 1082), (220, 1064)], 1.6)
    p.cut([(230, 1082), (240, 1064)], 1.6)
    vulture(p, 640, 1180, 1.4)
    tree(p, 880, 1040, 0.9)
    tree(p, 960, 1050, 0.7)
    return p


LANDSCAPES = [
    (movement, 404, "movement", {"name": "i. Movement · Vale Carapito",
                                 "line": "Large herbivores and predators keep the valley open and alive."}),
    (wetland, 505, "water", {"name": "ii. Water · Paul de Toirões",
                             "line": "Wetlands recovering after decades of drainage and damming."}),
    (gorge, 606, "connection", {"name": "iii. Connection · Côa gorge and Penascosa",
                                "line": "Valleys, habitats and 25,000 years of human history, working together."}),
]

if __name__ == "__main__":
    for draw, stone_seed, name, caption in LANDSCAPES:
        plate = draw()
        plate.render(schist(stone_seed), {**caption, "credit": CREDIT}, OUT / f"digital-study-{name}.jpg")
