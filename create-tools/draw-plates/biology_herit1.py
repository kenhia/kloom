"""Plates for The Story of Life's Inheritance frames written by part herit1 in sprint 055.
See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


# ------------------------------------------------------------------ mendel-peas

def _quad(p0, p1, p2, n=16):
    """Points along a quadratic Bezier."""
    out = []
    for i in range(n + 1):
        t = i / n
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    return out


def mendel_peas():
    d = D()
    # A pea flower in side section, three times: the bud with its keel closed round the stamens and the
    # stigma; the keel removed and the stamens drawn out with forceps; the bare stigma dusted with pollen
    # from another plant (Mendel 1866, in Bateson's 1902 translation). Proportions schematic.
    s = 1.05
    cxs = [70, 198, 326]
    cy = 150

    def P(cx, x, y):
        return (cx + x * s, cy + y * s)

    d.group('thin')
    for x in (134, 262):                                                  # panel rules
        d.line((x, 60), (x, 244))
    for cx in cxs:
        d.line(P(cx, -58, 30), P(cx, 62, 30))                             # the flower's axis
    for cx in cxs[1:]:                                                    # where the keel was
        d.dashed(*[P(cx, *p) for p in _quad((-14, 16), (24, 8), (42, -4))], dash=3, gap=3)
        d.dashed(*[P(cx, *p) for p in _quad((-14, 46), (36, 50), (42, -4))], dash=3, gap=3)

    d.group()
    for i, cx in enumerate(cxs):
        # calyx
        d.line(P(cx, -14, 8), P(cx, -22, 16), P(cx, -50, 23), P(cx, -50, 37), P(cx, -22, 44), P(cx, -14, 52))
        # ovary, the pod to be, with its ovules
        d.line(P(cx, -30, 26), P(cx, 18, 26), P(cx, 22, 30), P(cx, 18, 34), P(cx, -30, 34), closed=True)
        # style, curving up to the stigma
        d.line(*[P(cx, *p) for p in _quad((22, 30), (36, 30), (36, 8))])
        d.circle(*P(cx, 36, 5.5), 2.6 * s)
        if i == 0:
            # the keel, closed round the stamens and the stigma
            d.line(*[P(cx, *p) for p in _quad((-14, 16), (24, 8), (42, -4))])
            d.line(*[P(cx, *p) for p in _quad((-14, 46), (36, 50), (42, -4))])

    d.group('mid')
    for i, cx in enumerate(cxs):
        for k in range(6):                                                # ovules
            d.circle(*P(cx, -24 + k * 8, 30), 2.2 * s)
        if i == 0:
            # the stamens: a sheath round the ovary, the filaments curving up, anthers at the stigma
            d.line(P(cx, -30, 22), P(cx, 16, 22))
            d.line(P(cx, -30, 38), P(cx, 20, 38))
            for ax, ay in ((28, 10), (31, 1), (42, 2), (44, 11)):
                d.line(*[P(cx, *p) for p in _quad((20, 36 if ax > 36 else 24), (ax, 28), (ax, ay + 4))])
                d.ellipse(*P(cx, ax, ay), 2.2 * s, 3.4 * s)
        if i == 1:
            # forceps lifting the stamens out
            d.line(P(cx, 46, -66), P(cx, 44, -12))
            d.line(P(cx, 54, -64), P(cx, 50, -11))
            for ax, ay in ((44, -20), (50, -17), (52, -26)):
                d.ellipse(*P(cx, ax, ay), 2.2 * s, 3.4 * s)
            d.line(P(cx, 32, -6), P(cx, 40, -34))
            _arrow(d, P(cx, 32, -6), P(cx, 40, -34), size=4)
        if i == 2:
            # an anther from another plant, its pollen falling on the stigma
            d.ellipse(*P(cx, 52, -42), 3 * s, 4.6 * s)
            for k, (px, py) in enumerate(((49, -32), (46, -24), (43, -16), (41, -9), (52, -30), (48, -21), (44, -12))):
                d.circle(*P(cx, px, py), 0.9)
            d.line(P(cx, 60, -34), P(cx, 46, -6))
            _arrow(d, P(cx, 60, -34), P(cx, 46, -6), size=4)

    d.group('mid')
    d.text(200, 34, 'CROSSING PEAS · MENDEL 1866', size=7)
    caps = [('1 THE BUD', 'KEEL SHUT'), ('2 KEEL OFF', 'STAMENS PULLED'), ('3 STIGMA DUSTED', 'FOREIGN POLLEN')]
    for cx, (a, b) in zip(cxs, caps):
        d.text(cx, 232, a, size=7)
        d.text(cx, 242, b, size=7)
    c = cxs[0]
    d.text(*P(c, -4, 56), 'OVARY', size=7)
    d.text(*P(c, -10, 4), 'KEEL', size=7)
    d.text(*P(c, 38, -16), 'ANTHERS', size=7)
    d.text(*P(cxs[1], 28, 8), 'STIGMA', size=7, anchor='end')
    d.text(*P(cxs[1], 40, -70), 'FORCEPS', size=7, anchor='end')
    return d


# ------------------------------------------------------------------ rediscovery

def _seed(d, cx, cy, r, round_):
    """A pea in outline: a circle if round, a lobed, dented outline if wrinkled."""
    if round_:
        d.circle(cx, cy, r)
        return
    pts = []
    for k in range(36):
        a = 2 * math.pi * k / 36
        rr = r * (0.86 + 0.12 * math.cos(7 * a) + 0.05 * math.sin(3 * a))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.line(*pts, closed=True)


def _hatch(d, cx, cy, r, gap=3.2):
    """Horizontal chords across a seed: green."""
    segs = []
    y = -r + gap
    while y < r - 1:
        half = math.sqrt(r * r - y * y) * 0.82
        segs.append(((cx - half, cy + y), (cx + half, cy + y)))
        y += gap
    d.lines(segs)


def rediscovery():
    d = D()
    # Mendel's dihybrid cross, round yellow by wrinkled green, as a 4 x 4 square: the hybrid's four kinds
    # of pollen (columns) meet its four kinds of egg (rows). R round over r wrinkled, Y yellow over y green.
    # A seed is drawn wrinkled when it has no R, and hatched (green) when it has no Y. Right: the four
    # kinds as 9:3:3:1, beside Mendel's counts of 556 seeds.
    gam = [('R', 'Y'), ('R', 'y'), ('r', 'Y'), ('r', 'y')]
    x0, y0, c = 52, 74, 44
    cells = []
    for i, g in enumerate(gam):
        for j, h in enumerate(gam):
            rnd = 'R' in (g[0], h[0])
            yel = 'Y' in (g[1], h[1])
            cells.append((x0 + j * c + c / 2, y0 + i * c + c / 2, rnd, yel))

    d.group('thin')
    for k in range(5):
        d.line((x0 + k * c, y0), (x0 + k * c, y0 + 4 * c))
        d.line((x0, y0 + k * c), (x0 + 4 * c, y0 + k * c))
    d.line((x0 - 30, y0 - 22), (x0, y0))                                  # the corner's diagonal
    rows = [(96, True, True, '9', 'ROUND YELLOW', '315'), (140, False, True, '3', 'WRINKLED YELLOW', '101'),
            (184, True, False, '3', 'ROUND GREEN', '108'), (228, False, False, '1', 'WRINKLED GREEN', '32')]
    for y, *_ in rows:
        d.line((262, y + 16), (392, y + 16))

    d.group()
    for cx, cy, rnd, yel in cells:
        _seed(d, cx, cy, 12, rnd)
    for y, rnd, yel, *_ in rows:
        _seed(d, 274, y, 10, rnd)

    d.group('mid')
    for cx, cy, rnd, yel in cells:
        if not yel:
            _hatch(d, cx, cy, 12 if rnd else 10)
    for y, rnd, yel, *_ in rows:
        if not yel:
            _hatch(d, 274, y, 10 if rnd else 8.5)

    d.group('mid')
    d.text(200, 28, 'TWO CHARACTERS AT ONCE · RrYy SELFED', size=7)
    d.text(x0 + 2 * c, y0 - 22, 'POLLEN', size=7)
    d.text(x0 - 26, y0 - 6, 'EGGS', size=7)
    for k, g in enumerate(gam):
        d.text(x0 + k * c + c / 2, y0 - 8, ''.join(g), size=7)
        d.text(x0 - 12, y0 + k * c + c / 2 + 2.5, ''.join(g), size=7)
    d.text(392, 66, 'EXPECTED · SEEN', size=7, anchor='end')
    for y, rnd, yel, n, name, seen in rows:
        d.text(292, y - 2, n + ' ' + name, size=7, anchor='start')
        d.text(392, y + 10, seen, size=7, anchor='end')
    d.text(392, 268, '556 SEEDS · MENDEL 1866', size=7, anchor='end')
    return d


# ------------------------------------------------------------------ hardy-weinberg

def hardy_weinberg():
    d = D()
    # Genotype shares under random mating against p, the share of allele A: p^2 for AA, 2pq for Aa,
    # q^2 = (1 - p)^2 for aa. Computed, 0 <= p <= 1. The dashed line is the reading's worked example,
    # p = 0.3 (AA 0.09, Aa 0.42, aa 0.49); the top of the parabola, 2pq = 0.5 at p = 0.5.
    x0, y0, w, h = 70, 250, 290, 200

    def X(p):
        return x0 + w * p

    def Y(v):
        return y0 - h * v

    n = 60
    ps = [i / n for i in range(n + 1)]

    d.group('thin')
    for k in range(5):                                                    # grid at quarters
        v = k / 4
        d.line((X(0), Y(v)), (X(1), Y(v)))
        d.line((X(v), Y(0)), (X(v), Y(1)))

    d.group()
    d.line((X(0), Y(1)), (X(0), Y(0)), (X(1), Y(0)))                     # axes
    d.line(*[(X(p), Y(p * p)) for p in ps])
    d.line(*[(X(p), Y((1 - p) ** 2)) for p in ps])
    d.line(*[(X(p), Y(2 * p * (1 - p))) for p in ps])

    d.group('mid')
    d.dashed((X(0.3), Y(0)), (X(0.3), Y(0.49)), dash=3, gap=3)
    for v in (0.09, 0.42, 0.49):
        d.circle(X(0.3), Y(v), 2.6)
    d.circle(X(0.5), Y(0.5), 2.6)
    for k in range(5):                                                    # ticks
        v = k / 4
        d.line((X(v), Y(0)), (X(v), Y(0) + 4))
        d.line((X(0) - 4, Y(v)), (X(0), Y(v)))

    d.group('mid')
    for k, lab in enumerate(('0', '.25', '.5', '.75', '1')):
        d.text(X(k / 4), Y(0) + 14, lab, size=7)
        d.text(X(0) - 8, Y(k / 4) + 2.5, lab, size=7, anchor='end')
    d.text(X(0.5), Y(0) + 26, 'p, THE SHARE OF ALLELE A', size=7)
    d.text(X(0.9) + 4, Y(0.81) - 6, 'AA = p²', size=7, anchor='end')
    d.text(X(0.1) - 2, Y(0.81) - 6, 'aa = q²', size=7, anchor='start')
    d.text(X(0.5), Y(0.5) - 9, 'Aa = 2pq', size=7)
    d.text(X(0.3) - 6, Y(0.42) + 3, '.42', size=7, anchor='end')
    d.text(X(0.3) + 6, Y(0.49) - 3, '.49', size=7, anchor='start')
    d.text(X(0.3) + 6, Y(0.09) + 3, '.09', size=7, anchor='start')
    d.text(200, 28, 'GENOTYPES UNDER RANDOM MATING · HARDY 1908 · WEINBERG 1908', size=7)
    return d


PLATES = {'mendel-peas': mendel_peas, 'rediscovery': rediscovery, 'hardy-weinberg': hardy_weinberg}
