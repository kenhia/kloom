"""Plates for Daily Bread's trail The first drinks (part drink, sprint 051). See plates_for.py."""
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


def _spline(pts, n=10):
    """A Catmull-Rom curve through (h, r) points, n samples a span: a profile computed, not placed by hand."""
    ext = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t
                                    + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    out.append(pts[-1])
    return out


def first_wine():
    d = D()
    # Left: a Neolithic jar of the Shulaveri-Shomu culture, half in elevation and half in section. McGovern et al.
    # (2017) give the Khramis Didi-Gora jar as nearly 1 m tall and 1 m wide, its base a quarter of its widest
    # diameter, with clay globules near the rim read as grape clusters; the profile between those points is
    # interpolated. The base, where sediment settles, is the part sampled. Right: a qvevri in section, buried
    # to below its neck as UNESCO's inscription describes, the pomace settled in its pointed foot. Its size
    # varies from 20 to 10,000 litres; this one is drawn about 1.25 m tall at the same scale. Schematic.
    s = 140                                                               # units per metre
    jx, floor = 100, 250
    jar = [(0.0, 0.125), (0.08, 0.27), (0.25, 0.43), (0.5, 0.5), (0.75, 0.44), (0.92, 0.33), (1.0, 0.29)]
    prof = _spline(jar)
    qx, ground = 300, 92
    qv = [(0.0, 0.03), (0.15, 0.2), (0.45, 0.4), (0.75, 0.44), (1.0, 0.32), (1.17, 0.15), (1.25, 0.17)]
    qprof = _spline(qv)
    qbot = ground + 4 + 1.25 * s                                          # the foot, 1.25 m below the lip

    d.group('thin')
    d.line((jx, floor + 8), (jx, floor - 1.0 * s - 12))                   # the jar's axis
    d.line((jx - 0.5 * s - 10, floor - 0.5 * s), (jx + 0.5 * s + 10, floor - 0.5 * s))   # its widest diameter
    d.line((qx, ground - 14), (qx, qbot + 6))                             # the qvevri's axis
    d.line((200, 20), (200, 280))                                         # between the two
    d.line((20, floor), (190, floor))                                     # the house floor

    d.group()
    left = [(jx - r * s, floor - h * s) for h, r in prof]
    right = [(jx + r * s, floor - h * s) for h, r in prof]
    d.line(*reversed(left), (jx - 0.125 * s, floor), (jx + 0.125 * s, floor), *right)
    qleft = [(qx - r * s, qbot - h * s) for h, r in qprof]
    qright = [(qx + r * s, qbot - h * s) for h, r in qprof]
    d.line(*reversed(qleft), *qright)
    d.line((210, ground), (qx - 0.17 * s - 6, ground))                    # the ground, broken by the lid
    d.line((qx + 0.17 * s + 6, ground), (390, ground))

    d.group('mid')
    wall = 4
    inner = [(jx + r * s - wall, floor - h * s) for h, r in prof if h > 0.02]
    d.line((jx, floor - wall), (jx + 0.125 * s - wall, floor - wall), *inner)   # the section's inner face
    for i in range(6):                                                    # sediment hatched in the base
        y = floor - wall - 3 - i * 3
        h = (floor - y) / s
        (h0, r0), (h1, r1) = next((p, q) for p, q in zip(prof, prof[1:]) if p[0] <= h <= q[0])
        xin = jx + (r0 + (r1 - r0) * (h - h0) / (h1 - h0)) * s - wall
        d.line((jx + 2, y), (xin - 2, y))
    for k, ang in enumerate((-50, 50)):                                   # grape-cluster globules near the rim
        cx = jx + math.sin(math.radians(ang)) * 0.4 * s
        cy = floor - 0.9 * s
        for row in range(3):
            for col in range(3 - row):
                d.circle(cx - 5 + col * 4 + row * 2, cy - 4 + row * 4, 1.6)
    qin = [(qx + r * s - wall, qbot - h * s) for h, r in qprof if h > 0.04]
    qinl = [(qx - r * s + wall, qbot - h * s) for h, r in qprof if h > 0.04]
    d.line(*reversed(qinl), *qin)                                         # the qvevri's inner face
    level = qbot - 1.05 * s
    half = [r for h, r in qprof if abs(h - 1.05) < 0.03][0] * s - wall
    d.line((qx - half, level), (qx + half, level))                        # the wine's surface
    for i in range(14):                                                   # pomace in the foot
        a = i * 2.39996
        rho = 3 + 2.1 * math.sqrt(i)
        d.circle(qx + rho * math.cos(a), qbot - 18 + 0.6 * rho * math.sin(a), 1.4)
    d.line((qx - 0.2 * s, ground - 4), (qx + 0.2 * s, ground - 4))       # the lid
    for x in range(214, 390, 9):                                          # earth around it
        if abs(x - qx) > 0.5 * s:
            d.line((x, ground + 4), (x - 5, ground + 9))

    d.group('mid')
    d.line((30, 272), (30 + s, 272))                                      # a 1 m scale bar
    d.line((30, 268), (30, 276))
    d.line((30 + s, 268), (30 + s, 276))
    d.text(30 + s / 2, 285, '1 M', size=7)
    d.text(jx, 26, 'NEOLITHIC JAR · c. 5800 BC', size=7)
    d.text(jx + 50, floor - 18, 'BASE SAMPLED', size=7, anchor='start')
    d.text(qx, 26, 'QVEVRI · TODAY', size=7)
    d.text(392, ground - 6, 'GROUND', size=7, anchor='end')
    d.text(qx, qbot - 30, 'POMACE', size=7)
    return d


def ninkasi():
    d = D()
    # Left: the hymn's fermenting vat "placed appropriately on top of a large collector vat" (Civil 1964,
    # lines 41-44), the beer draining through a hole in its bottom, a vessel Damerow (2012) also reads from
    # the sign SIM. Right: a jar of unfiltered beer drunk through straws reaching below the layer of hulls
    # and yeast floating on top (Katz and Voigt 1986). Below: the hymn's steps in order. Proportions schematic.
    d.group('thin')
    d.line((100, 22), (100, 208))                                         # the vats' axis
    d.line((290, 22), (290, 208))                                         # the jar's axis
    d.line((20, 208), (380, 208))                                         # the floor

    d.group()
    coll = _spline([(0, 22), (20, 46), (45, 54), (65, 46), (78, 34)], 8)  # collector vat: (height, radius)
    d.line(*[(100 - r, 208 - h) for h, r in reversed(coll)], *[(100 + r, 208 - h) for h, r in coll])
    ferm = _spline([(0, 6), (12, 26), (40, 34), (66, 28), (78, 24)], 8)   # fermenting vat, on the mouth
    base = 208 - 72
    d.line(*[(100 - r, base - h) for h, r in reversed(ferm)], *[(100 + r, base - h) for h, r in ferm])
    jar = _spline([(0, 26), (25, 58), (70, 62), (110, 46), (128, 40)], 8)
    d.line(*[(290 - r, 208 - h) for h, r in reversed(jar)], *[(290 + r, 208 - h) for h, r in jar])

    d.group('mid')
    for i in range(4):                                                    # drips through the hole
        y = base + 6 + i * 9
        d.line((100, y), (100, y + 4))
    d.line((100 - 44, 208 - 40), (100 + 44, 208 - 40))                    # the filtered beer
    top = base - 60
    d.line((100 - 30, top), (100 + 30, top))                              # the fermenting wort
    for x in range(76, 126, 7):
        d.circle(x, top + 4, 1.2)
    surf = 208 - 100
    rs = [r for h, r in jar if abs(h - 100) < 3.5][0] - 3                 # the jar's inner radius there
    d.line((290 - rs, surf), (290 + rs, surf))                            # the beer's surface
    for i in range(int(2 * rs / 5) - 1):                                  # hulls and yeast floating on it
        x = 290 - rs + 4 + i * 5
        y = surf + 3 + (i * 7 % 5)
        d.line((x, y), (x + 3, y + 1))
    for x0, x1 in ((244, 272), (336, 308)):                               # two straws, through the mouth
        for off in (-2, 2):
            d.line((x0 + off, 28), (x1 + off, 160))
    d.line((232, surf - 14), (290 - rs + 8, surf + 3))                    # leader to the layer

    d.group()
    steps = ['BAPPIR', 'MALT', 'MASH', 'COOL', 'WORT', 'FERMENT', 'FILTER']
    xs = [34 + i * 55.3 for i in range(7)]
    for x in xs:
        _box(d, x - 24, 236, 48, 18)
    for a, b in zip(xs, xs[1:]):
        d.line((a + 24, 245), (b - 24, 245))
        _arrow(d, (a + 24, 245), (b - 24, 245), size=4)

    d.group('mid')
    for x, st in zip(xs, steps):
        d.text(x, 248, st, size=7)
    d.text(100, 18, 'FERMENTING VAT', size=7)
    d.text(100, 222, 'COLLECTOR VAT', size=7)
    d.text(290, 222, 'UNFILTERED BEER', size=7)
    d.text(230, surf - 16, 'HULLS AND YEAST', size=7, anchor='end')
    d.text(200, 274, 'THE HYMN TO NINKASI, LINES 13-48', size=7)
    return d


def reinheitsgebot():
    d = D()
    # A female hop cone in longitudinal section: bracts and bracteoles in pairs on a zigzag axis (the strig),
    # with the yellow lupulin glands at the bracteoles' bases, where the resins (humulone, lupulone) and the
    # oils are made. An enlarged gland beside it, and the change the boil makes: alpha acids isomerize to the
    # bitter iso-alpha acids (Köhler's plate, fig. 20, draws the glands; the chemistry is from the Hops article).
    cx, top, bot = 120, 36, 262
    n = 8

    def half_width(y):
        t = (y - top) / (bot - top)
        return 62 * math.sin(math.pi * min(1, max(0, t)) ** 0.8)

    d.group('thin')
    d.line((cx, top - 8), (cx, bot + 8))                                  # the cone's axis
    env = [(cx + half_width(top + (bot - top) * i / 40), top + (bot - top) * i / 40) for i in range(41)]
    d.line(*env)
    d.line(*[(2 * cx - x, y) for x, y in env])
    d.circle(300, 110, 62)                                                # the inset's field

    d.group()
    nodes = [top + 12 + i * (bot - top - 24) / (n - 1) for i in range(n)]
    zig = [(cx + (4 if i % 2 else -4), y) for i, y in enumerate(nodes)]
    d.line((cx, top + 2), *zig, (cx, bot - 2))                            # the strig
    for i, (x, y) in enumerate(zig):
        side = 1 if i % 2 == 0 else -1
        w = half_width(y + 10) - 2
        tip = (cx + side * w, y + 16)
        mid = (cx + side * w * 0.55, y - 4)
        d.curve(f'M{x:.1f} {y:.1f} Q{mid[0]:.1f} {mid[1]:.1f} {tip[0]:.1f} {tip[1]:.1f} '
                f'Q{cx + side * w * 0.5:.1f} {y + 18:.1f} {x:.1f} {y + 6:.1f}')

    d.group('mid')
    glands = []
    for i, (x, y) in enumerate(zig):
        side = 1 if i % 2 == 0 else -1
        if half_width(y + 5) < 24:
            continue
        for k in range(3):
            gx, gy = x + side * (7 + k * 5), y + 5 + k * 1.5
            d.circle(gx, gy, 1.6)
            glands.append((gx, gy))
    g = glands[13]
    d.dashed(g, (300 - 62 * math.cos(math.radians(25)), 110 + 62 * math.sin(math.radians(25))), dash=3, gap=3)
    # the enlarged gland: a cup on a short stalk, full of resin
    d.line((300, 160), (300, 146))
    d.arc(300, 120, 40, 0, 180, ry=26)                                    # the cup of secreting cells
    d.arc(300, 120, 40, 180, 360, ry=34)                                  # the cuticle, domed by resin
    for i in range(18):
        a = i * 2.39996
        rho = 4.2 * math.sqrt(i)
        d.circle(300 + 1.5 * rho * math.cos(a), 116 + 1.0 * rho * math.sin(a), 1.8)

    d.group()
    _box(d, 210, 226, 70, 18)
    _box(d, 302, 226, 92, 18)
    d.line((280, 235), (302, 235))
    _arrow(d, (280, 235), (302, 235), size=4)

    d.group('mid')
    d.text(245, 238, 'ALPHA ACIDS', size=7)
    d.text(348, 238, 'ISO-ALPHA ACIDS', size=7)
    d.text(293, 222, 'BOIL', size=7)
    d.text(348, 258, 'BITTER · KEEPS BEER', size=7)
    d.text(300, 188, 'LUPULIN GLAND, ENLARGED', size=7)
    d.text(cx, 284, 'HOP CONE IN SECTION', size=7)
    d.text(cx + 8, top - 10, 'STRIG', size=7, anchor='start')
    return d


PLATES = {'first-wine': first_wine, 'ninkasi': ninkasi, 'reinheitsgebot': reinheitsgebot}
