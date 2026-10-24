"""Digital studies for the three plates: European rabbit, European wildcat and
Mediterranean pond turtle, after the Iron Age fine-line engravings of the Côa
Valley (preprint §8). Burnt sienna lines on a greyscale schist surface.

The stone is procedural, not a photograph: schist foliation and fractures run
NNE-SSW, as on the Côa panels (Aubry et al., 2012; Fernandes, 2009), with the
small pits seen at Penascosa. The line grammar follows the Iron Age descriptors
(Botica et al., 2022): rough incised lines in repeated strokes, profile figures,
bodies filled with parallel strokes (rabbit, wildcat) or a grid (turtle shell).

These are digital studies, not the plates of step (iv), which are cut by hand.

Run from the repo root:  conda run -n coa python scripts/digital_plates.py
Writes img/digital-studies/digital-study-plate-*.jpg. Needs numpy, scipy, shapely and Pillow.
Source copy and history: coa-connectivity-lab/Solo-field-illustrator-project-for-Rewilding-Portugal,
research/rewilding-dynamics/scripts/digital_plates.py
"""
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from scipy.interpolate import splev, splprep
from shapely import affinity
from shapely.geometry import LineString, Point, Polygon

OUT = Path(__file__).resolve().parent.parent / "img" / "digital-studies"
FONT = Path.home() / ".cache" / "coa-plates" / "Exo2-400.ttf"
FONT_URL = "https://cdn.jsdelivr.net/fontsource/fonts/exo-2@5.0.20/latin-400-normal.ttf"  # SIL OFL
LOGO = Path(__file__).resolve().parent.parent / "img" / "gam-logo-white.png"  # GAM comms kit, not in this repo

if not FONT.exists():
    FONT.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(FONT_URL, FONT)

W, H = 1600, 2000          # 4:5, as the site's plate slots
SS = 2                     # supersampling for clean lines
BAND = 210                 # caption band at the foot of the plate
SIENNA = np.array([138, 54, 27]) / 255   # burnt sienna
OUT.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Schist surface
# ---------------------------------------------------------------------------
def noise(shape, sigma, rng):
    n = ndimage.gaussian_filter(rng.standard_normal(shape), sigma)
    return (n - n.mean()) / (n.std() + 1e-9)


def schist(seed):
    rng = np.random.default_rng(seed)
    h, w = H * SS, W * SS
    big = int(1.5 * max(h, w))
    angle = 18  # foliation NNE-SSW, degrees from vertical

    # anisotropic grain: stretched along the foliation, then rotated
    layers = []
    for amp, factor, sig in [(0.45, 8, 3.0), (0.5, 4, 2.0), (0.55, 2, 1.4), (0.6, 1, 0.8)]:
        n = ndimage.gaussian_filter(rng.standard_normal((big // factor, big // factor)), (sig * 5, sig))
        n = ndimage.zoom(n, factor, order=1)[:big, :big]
        layers.append(amp * (n - n.mean()) / n.std())
    grain = ndimage.rotate(sum(layers), angle, reshape=False, order=1)
    oy, ox = (big - h) // 2, (big - w) // 2
    grain = grain[oy:oy + h, ox:ox + w]

    # cleavage planes: thin light and dark bands across the foliation
    yy, xx = np.mgrid[0:h, 0:w]
    u = (xx * np.cos(np.radians(angle)) + yy * np.sin(np.radians(angle))).astype(int)
    u -= u.min()
    bands = ndimage.gaussian_filter1d(rng.standard_normal(u.max() + 1), 1.2)
    bands = np.where(np.abs(bands) > 1.6, bands, bands * 0.25)
    cleave = bands[u]

    # weathering: broad patches of patina and paler, washed rock
    patina = noise((h // 16, w // 16), 6, rng)
    patina = ndimage.zoom(patina, 16, order=1)[:h, :w]

    stone = 0.55 + 0.035 * grain + 0.04 * cleave + 0.05 * patina
    # pale speckle (quartz)
    speck = rng.random((h, w))
    stone[speck > 0.9993] += 0.14
    stone = ndimage.gaussian_filter(stone, 0.5)
    # pits, as on the Penascosa panels: small dark hollows with a lit upper rim
    pits = np.zeros((h, w))
    rims = np.zeros((h, w))
    n_pits = int(h * w / 9000)
    py, px = rng.integers(0, h, n_pits), rng.integers(0, w, n_pits)
    pits[py, px] = rng.uniform(0.5, 1.0, n_pits)
    rims[np.clip(py - 3 * SS, 0, h - 1), px] = 0.6
    sig = 2.0 * SS
    stone -= 0.22 * ndimage.gaussian_filter(pits, sig) * 2 * np.pi * sig ** 2       # peak depth ~0.1-0.2
    stone += 0.10 * ndimage.gaussian_filter(rims, 1.2 * SS) * 2 * np.pi * (1.2 * SS) ** 2

    # fractures: a few long cracks, roughly along the strike, with a lit edge
    img = Image.fromarray(np.zeros((h, w), np.uint8))
    lit = Image.fromarray(np.zeros((h, w), np.uint8))
    d, dl = ImageDraw.Draw(img), ImageDraw.Draw(lit)
    for _ in range(rng.integers(3, 6)):
        x, y = rng.uniform(0, w), rng.uniform(-0.1 * h, 0.3 * h)
        drift = np.tan(np.radians(angle + rng.normal(0, 8)))  # follows the strike, with some wander
        pts = [(x, y)]
        while y <= h and len(pts) < 600:
            drift += rng.normal(0, 0.03)
            x, y = x - 9 * drift + rng.normal(0, 2), y + 9
            pts.append((x, y))
        width = int(rng.integers(2, 5))
        d.line(pts, fill=255, width=width)
        dl.line([(px - 2 * SS, py - 1) for px, py in pts], fill=255, width=max(1, width // 2))
    crack = ndimage.gaussian_filter(np.asarray(img, float) / 255, 1.0)
    edge = ndimage.gaussian_filter(np.asarray(lit, float) / 255, 1.2)
    stone = stone - 0.28 * crack + 0.08 * edge

    # vignette, as light falls across a panel
    vy = np.linspace(-1, 1, h)[:, None]
    vx = np.linspace(-1, 1, w)[None, :]
    stone *= 1 - 0.16 * (vx ** 2 + vy ** 2)
    stone = np.clip(stone, 0, 1)
    return np.repeat(stone[..., None], 3, axis=2)


# ---------------------------------------------------------------------------
# Line grammar
# ---------------------------------------------------------------------------
LUMP = np.random.default_rng(5)


def smooth(points, closed=False, n=300, lump=7):
    """A spline through control points nudged by hand: outlines come out lumpy, not geometric."""
    pts = np.asarray(points, float) + LUMP.normal(0, lump, (len(points), 2))
    if closed:
        pts = np.vstack([pts, pts[:1]])
    tck, _ = splprep(pts.T, s=0, per=closed, k=3 if len(pts) > 3 else len(pts) - 1)
    x, y = splev(np.linspace(0, 1, n), tck)
    return np.column_stack([x, y])


def ellipse(cx, cy, rx, ry, n=120):
    t = np.linspace(0, 2 * np.pi, n)
    return np.column_stack([cx + rx * np.cos(t), cy + ry * np.sin(t)])


def hatch(poly, spacing, angle, rng=None):
    """Roughly parallel lines clipped to a polygon: one direction of the grid infill.
    With rng, spacing and angle wander line by line, and lines stop short or run over."""
    minx, miny, maxx, maxy = poly.bounds
    diag = np.hypot(maxx - minx, maxy - miny)
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    lines = []
    k = -diag
    while k < diag:
        a = angle + (rng.normal(0, 5) if rng is not None else 0)
        seg = affinity.rotate(LineString([(cx - diag, cy + k), (cx + diag, cy + k)]), a, origin=(cx, cy))
        cut = seg.intersection(poly)
        for g in [] if cut.is_empty else getattr(cut, "geoms", [cut]):
            if g.length > spacing * 0.6:
                c = np.asarray(g.coords)
                if rng is not None:
                    d = (c[-1] - c[0]) / np.linalg.norm(c[-1] - c[0])
                    c = np.vstack([c[0] - d * rng.uniform(-0.25, 0.12) * spacing * 2,
                                   c[-1] + d * rng.uniform(-0.25, 0.12) * spacing * 2])
                lines.append(c)
        k += spacing * (rng.uniform(0.7, 1.35) if rng is not None else 1)
    return lines


class Plate:
    """Strokes in figure units (x 0-1000, y up), mapped onto the stone."""

    def __init__(self, seed, box=(0, 0, 1000, 800)):
        self.rng = np.random.default_rng(seed)
        self.strokes = []   # (points, width)
        x0, y0, x1, y1 = box
        self.scale = (W * SS * 0.86) / (x1 - x0)
        self.ox = W * SS * 0.07 - x0 * self.scale
        self.oy = (H - BAND) * SS * 0.5 + (y0 + y1) / 2 * self.scale

    def to_px(self, pts):
        pts = np.asarray(pts, float)
        return np.column_stack([self.ox + pts[:, 0] * self.scale, self.oy - pts[:, 1] * self.scale])

    def cut(self, pts, width=2.2, passes=None, overshoot=14):
        """One incised line, cut in two to four rough strokes with a hand-held point:
        the point wanders and chatters, skips now and then, and runs past the ends."""
        pts = np.asarray(pts, float)
        seg = np.hypot(*np.diff(pts, axis=0).T)
        L = seg.sum()
        if L == 0:
            return
        t = np.concatenate([[0], np.cumsum(seg)])
        s = np.linspace(0, L, max(4, int(L / 2.5)))
        base = np.column_stack([np.interp(s, t, pts[:, 0]), np.interp(s, t, pts[:, 1])])
        d0 = base[min(3, len(base) - 1)] - base[0]
        d1 = base[-1] - base[max(-4, -len(base))]
        for _ in range(passes or self.rng.integers(2, 5)):
            wander = ndimage.gaussian_filter1d(self.rng.normal(0, 1, (len(s), 2)), 9, axis=0) * 9
            chatter = ndimage.gaussian_filter1d(self.rng.normal(0, 1, (len(s), 2)), 1.5, axis=0) * 1.6
            line = base + wander + chatter
            # overshoot or stop short at each end
            o0, o1 = self.rng.uniform(-6, max(-6, overshoot), 2) if overshoot > -6 else (-6, -6)
            n0 = d0 / (np.linalg.norm(d0) + 1e-9)
            n1 = d1 / (np.linalg.norm(d1) + 1e-9)
            line = np.vstack([line[:1] - n0 * o0, line, line[-1:] + n1 * o1])
            # the point skips: the stroke breaks into pieces, each with its own pressure
            breaks = np.flatnonzero(self.rng.random(len(line)) < 0.012)
            start = 0
            for b in list(breaks) + [len(line)]:
                if b - start > 3:
                    self.strokes.append((line[start:b], width * self.rng.uniform(0.75, 1.45)))
                start = b + int(self.rng.integers(1, 4))

    def outline(self, pts, width=2.6, overshoot=14):
        self.cut(pts, width, overshoot=overshoot)

    def grid(self, poly, spacing=20, angles=(58, -58), width=1.9):
        for ang in angles:
            for line in hatch(poly, spacing, ang + self.rng.normal(0, 4), self.rng):
                self.cut(line, width, passes=self.rng.integers(1, 3))

    def render(self, stone, caption, path):
        h, w = stone.shape[:2]
        core = Image.new("L", (w, h), 0)
        shade = Image.new("L", (w, h), 0)
        light = Image.new("L", (w, h), 0)
        dc, ds, dl = ImageDraw.Draw(core), ImageDraw.Draw(shade), ImageDraw.Draw(light)
        for pts, width in self.strokes:
            px = [tuple(p) for p in self.to_px(pts)]
            wpx = max(1, int(round(width * SS * 1.7)))
            ds.line([(x + 1.6 * SS, y + 1.6 * SS) for x, y in px], fill=255, width=wpx + SS, joint="curve")
            dl.line([(x - 1.2 * SS, y - 1.2 * SS) for x, y in px], fill=255, width=max(1, wpx // 2), joint="curve")
            dc.line(px, fill=255, width=wpx, joint="curve")
        c = ndimage.gaussian_filter(np.asarray(core, float) / 255, 0.7 * SS)[..., None]
        s = ndimage.gaussian_filter(np.asarray(shade, float) / 255, 1.1 * SS)[..., None]
        li = ndimage.gaussian_filter(np.asarray(light, float) / 255, 0.9 * SS)[..., None]
        img = stone * (1 - 0.22 * s)                       # the cut's shadow side
        img = img + 0.10 * li * (1 - c)                     # the lit lip of the cut
        pigment = stone * (0.55 + 0.45 * SIENNA) * SIENNA * 1.9
        img = img * (1 - 0.92 * c) + np.clip(pigment, 0, 1) * 0.92 * c
        img = np.clip(img, 0, 1)

        im = Image.fromarray((img * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
        draw = ImageDraw.Draw(im)
        draw.rectangle([0, H - BAND, W, H], fill=(34, 31, 29))
        title = ImageFont.truetype(str(FONT), 46)
        body = ImageFont.truetype(str(FONT), 25)
        draw.text((70, H - BAND + 34), caption["name"], font=title, fill=(214, 120, 84))
        draw.text((70, H - BAND + 98), caption["line"], font=body, fill=(226, 222, 214))
        small = ImageFont.truetype(str(FONT), 21)
        draw.text((70, H - BAND + 142), caption["credit"], font=small, fill=(160, 155, 148))
        # Global Artivism Month participant mark, white version from the GAM comms kit (skipped if absent)
        if LOGO.exists():
            logo = Image.open(LOGO)
            logo = logo.resize((int(logo.width * (BAND - 70) / logo.height), BAND - 70), Image.LANCZOS)
            im.paste(logo, (W - logo.width - 60, H - BAND + 35), logo)
        im.save(path, quality=86, optimize=True, progressive=True)
        print("wrote", path, f"{path.stat().st_size / 1024:.0f} KB")


CREDIT = ("New work after the Iron Age fine-line engravings of the Côa Valley, not an ancient motif.\n"
          "Digital study, Linda Angulo Lopez, 2026.")


# ---------------------------------------------------------------------------
# European rabbit: the ears and the short tail
# ---------------------------------------------------------------------------
def rabbit():
    p = Plate(seed=11, box=(120, 180, 900, 860))
    body = smooth([(250, 300), (215, 385), (255, 470), (380, 535), (520, 545), (600, 525), (645, 560),
                   (705, 562), (765, 522), (790, 488), (755, 458), (695, 440), (645, 400), (622, 330),
                   (560, 292), (400, 282), (300, 284)], closed=True)
    p.outline(body, 2.8)
    # hind leg: its own shape, kept out of the body strokes so the lines don't cross it
    thigh = smooth([(300, 300), (338, 385), (430, 408), (476, 330), (455, 300)], lump=3)
    thigh_poly = Polygon(np.vstack([thigh, [(300, 300)]]))
    trunk = Polygon(body).difference(Point(715, 500).buffer(85)).difference(thigh_poly.buffer(12)).buffer(-10)
    p.grid(trunk, spacing=24, angles=(78,))   # parallel strokes only, no cross-hatch
    # ears, laid back, the diagnostic feature
    p.outline(smooth([(640, 560), (598, 690), (566, 805), (584, 818), (628, 725), (682, 565)]), 2.6)
    p.outline(smooth([(668, 562), (668, 712), (684, 815), (704, 808), (714, 700), (708, 560)]), 2.6)
    p.cut([(600, 700), (580, 780)], 1.4, passes=1)
    # short, round tail
    p.outline(ellipse(212, 405, 30, 30), 2.4)
    p.grid(Point(212, 405).buffer(26), spacing=10, angles=(78,), width=1.3)
    # hind leg, with its own strokes at another angle, and the long foot as a separate line below
    p.outline(thigh, 2.6)
    p.grid(thigh_poly.buffer(-9), spacing=20, angles=(20,), width=1.7)
    p.outline([(258, 262), (488, 256)], 2.6)
    # forelegs end on their paws: separate lines that meet, no overshoot
    p.outline(smooth([(622, 334), (630, 290), (636, 250)], lump=2), 2.4, overshoot=0)
    p.outline(smooth([(596, 318), (598, 280), (594, 252)], lump=2), 2.4, overshoot=0)
    p.cut([(640, 244), (672, 240)], 2.2, overshoot=0)
    p.cut([(598, 246), (628, 242)], 2.2, overshoot=0)
    # eye and nose
    p.outline(ellipse(728, 506, 11, 9, 40), 2.0)
    p.cut([(786, 488), (770, 470)], 1.6, passes=1)
    return p


# ---------------------------------------------------------------------------
# European wildcat: the blunt, ringed tail
# ---------------------------------------------------------------------------
def wildcat():
    p = Plate(seed=23, box=(30, 150, 860, 640))
    body = smooth([(190, 430), (320, 456), (470, 460), (600, 450), (662, 472), (690, 470), (662, 420),
                   (650, 362), (600, 332), (450, 322), (320, 326), (232, 336), (192, 382)], closed=True)
    p.outline(body, 2.8)
    p.grid(Polygon(body).buffer(-9), spacing=26, angles=(82,))   # parallel strokes only, no cross-hatch
    # head in profile: crown, two ears set back, forehead, short muzzle, chin
    head = smooth([(662, 470), (700, 515), (712, 586), (738, 530), (752, 548), (770, 582), (780, 526),
                   (806, 502), (834, 478), (850, 462), (836, 444), (806, 432), (760, 418), (700, 418)],
                  closed=True, lump=4)
    p.outline(head, 2.8)
    p.cut([(846, 456), (880, 466)], 1.4, passes=1)   # whiskers, two light strokes
    p.cut([(844, 448), (882, 444)], 1.4, passes=1)
    p.outline(smooth([(782, 488), (794, 496), (808, 490), (794, 482)], closed=True, n=60, lump=1.5), 2.0)
    # legs as paired lines
    for top, bottom in [((612, 338), (622, 182)), ((578, 330), (574, 182)), ((262, 334), (250, 182)),
                        ((298, 328), (292, 182))]:
        dx = 15
        p.outline([top, bottom], 2.4)
        p.outline([(top[0] + dx, top[1] - 6), (bottom[0] + dx, bottom[1])], 2.4)
        p.cut([(bottom[0] - 4, bottom[1]), (bottom[0] + dx + 12, bottom[1] - 2)], 2.4)
    # tail: thick, blunt, with rings and a dark tip, the diagnostic feature
    upper = [(192, 425), (130, 395), (82, 340), (62, 268)]
    lower = [(98, 262), (112, 322), (156, 372), (198, 392)]
    tail = smooth(upper + lower, closed=True)
    p.outline(tail, 2.8)
    spine = smooth([(195, 408), (140, 382), (98, 330), (80, 266)], n=200)
    tail_poly = Polygon(tail)
    for k in [0.18, 0.36, 0.54, 0.72]:
        i = int(k * (len(spine) - 1))
        (x0, y0), (x1, y1) = spine[i], spine[min(i + 4, len(spine) - 1)]
        nx, ny = -(y1 - y0), (x1 - x0)
        nrm = np.hypot(nx, ny)
        ring = LineString([(x0 - 60 * nx / nrm, y0 - 60 * ny / nrm), (x0 + 60 * nx / nrm, y0 + 60 * ny / nrm)])
        cut = ring.intersection(tail_poly)
        for g in getattr(cut, "geoms", [cut]):
            if not g.is_empty:
                band = g.buffer(7)
                p.grid(band.intersection(tail_poly), spacing=5, angles=(30,), width=1.2)
    tip = tail_poly.intersection(Point(80, 266).buffer(30))
    p.grid(tip, spacing=5, angles=(30,), width=1.2)
    return p


# ---------------------------------------------------------------------------
# Mediterranean pond turtle: the low shell and the striped neck
# ---------------------------------------------------------------------------
def turtle():
    p = Plate(seed=37, box=(150, 120, 990, 600))
    top = smooth([(240, 312), (300, 400), (420, 462), (560, 472), (690, 424), (770, 336)], n=300)
    shell = np.vstack([top, [(770, 312), (240, 300)]])
    p.outline(top, 3.0)
    p.outline([(236, 306), (774, 314)], 2.8)          # plastron
    p.outline([(250, 290), (762, 296)], 2.0)          # lower rim, a second line below
    shell_poly = Polygon(shell)
    inner = affinity.scale(shell_poly, 0.78, 0.7, origin=(505, 312))
    p.outline(np.asarray(inner.exterior.coords)[:-1][: len(top)], 2.0)
    # scutes: a grid of curved divisions over a low dome
    for x in [330, 420, 505, 590, 680]:
        cutline = smooth([(x - 10, 312), (x, 380), (x + 8, 480)], n=60)
        part = LineString(cutline).intersection(shell_poly)
        for g in getattr(part, "geoms", [part]):
            if not g.is_empty:
                p.cut(np.asarray(g.coords), 2.0)
    for line in hatch(inner, 16, 0, p.rng):
        p.cut(line, 1.2, passes=1)
    # neck with stripes, the diagnostic feature
    neck_up = smooth([(764, 342), (820, 372), (880, 400)], n=80)
    neck_lo = smooth([(774, 318), (836, 338), (890, 360)], n=80)
    p.outline(neck_up, 2.6)
    p.outline(neck_lo, 2.6)
    for f in [0.3, 0.55, 0.8]:
        p.cut(neck_lo + f * (neck_up - neck_lo), 1.4)
    head = ellipse(918, 384, 46, 28)
    p.outline(head, 2.6)
    p.cut(smooth([(880, 384), (920, 392), (960, 380)], n=40), 1.4)   # stripe along the head
    p.outline(ellipse(932, 394, 6, 5, 30), 1.6)
    p.cut([(958, 374), (966, 370)], 1.6, passes=1)
    # legs and tail
    p.outline(smooth([(690, 300), (712, 254), (744, 236)]), 2.6)
    p.outline(smooth([(660, 300), (680, 250), (708, 230)]), 2.4)
    for dx in (0, 12, 24):
        p.cut([(712 + dx * 0.8, 234), (724 + dx, 220)], 1.6, passes=1)
    p.outline(smooth([(330, 296), (300, 252), (262, 238)]), 2.6)
    p.outline(smooth([(360, 296), (336, 248), (300, 228)]), 2.4)
    p.outline(smooth([(240, 304), (206, 296), (176, 284)]), 2.2)
    return p


PLATES = [
    (rabbit, 101, "plate-rabbit", {"name": "European rabbit · Oryctolagus cuniculus",
                                   "line": "The keystone prey of the Iberian Peninsula, Endangered in its native range."}),
    (wildcat, 202, "plate-wildcat", {"name": "European wildcat · Felis silvestris",
                                     "line": "The valley's mid-sized predator, which depends on the rabbit."}),
    (turtle, 303, "plate-pond-turtle", {"name": "Mediterranean pond turtle · Mauremys leprosa",
                                        "line": "The animal that holds on in the river's summer pools."}),
]

for draw, stone_seed, name, caption in PLATES:
    plate = draw()
    plate.render(schist(stone_seed), {**caption, "credit": CREDIT}, OUT / f"digital-study-{name}.jpg")
