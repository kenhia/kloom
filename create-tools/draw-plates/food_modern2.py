"""Plates for Daily Bread's part modern2 (sprint 051): the Dust Bowl and the Green Revolution. See plates_for.py."""
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


def _contour(cx, cy, r0, n=96):
    """A closed contour of a low hill: a circle of radius r0 bent by two low harmonics, so the
    contours are nested and never cross (the bend is a fixed fraction of r0)."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = r0 * (1 + 0.10 * math.sin(2 * t + 0.6) + 0.05 * math.cos(3 * t))
        pts.append((cx + 1.35 * r * math.cos(t), cy + 0.85 * r * math.sin(t)))
    return pts


def _clip(pts, x0, y0, x1, y1):
    """Split a closed polyline into the runs that lie inside a box."""
    runs, cur = [], []
    for p in pts + pts[:1]:
        if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
            cur.append(p)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return [r for r in runs if len(r) > 1]


def dust_bowl():
    d = D()
    # Left: a field on a low hill in plan, laid out as the Soil Conservation Service taught: every furrow
    # and strip follows a contour (Geib 1931, Rule 1937). Contours are computed, nested curves; strips of
    # close-growing crop (hatched) alternate with row-crop bands whose furrows run level around the slope.
    # Right: lister furrows in section trapping drifting soil (Rule 1937), and a shelterbelt in elevation
    # lifting the wind. Proportions are schematic.
    box = (14, 30, 236, 262)
    cx, cy = 128, 150
    radii = [16, 30, 44, 58, 72, 86, 100, 114]

    d.group('thin')
    _box(d, box[0], box[1], box[2] - box[0], box[3] - box[1])          # the field's edge
    for r in radii:                                                    # contour lines
        for run in _clip(_contour(cx, cy, r), *box):
            d.line(*run)
    d.line((262, 132), (390, 132))                                     # ground line of the section
    d.line((262, 252), (390, 252))                                     # ground line of the elevation

    d.group('mid')
    # row-crop bands: furrows between alternate pairs of contours, level around the slope
    for i in range(0, len(radii) - 1, 2):
        r0, r1 = radii[i], radii[i + 1]
        for k in (1, 2, 3):
            r = r0 + (r1 - r0) * k / 4
            for run in _clip(_contour(cx, cy, r), *box):
                d.line(*run)

    d.group()
    # close-growing strips: short ticks across the band between the other pairs of contours
    segs = []
    for i in range(1, len(radii) - 1, 2):
        r0, r1 = radii[i], radii[i + 1]
        inner, outer = _contour(cx, cy, r0 + 2, n=72), _contour(cx, cy, r1 - 2, n=72)
        for p, q in zip(inner, outer):
            if all(box[0] <= v[0] <= box[2] and box[1] <= v[1] <= box[3] for v in (p, q)):
                segs.append([p, q])
    d.lines(segs)
    # the hilltop
    d.circle(cx, cy, 3)

    d.group('mid')
    # downhill: the path water would take, straight across the contours, checked at each strip
    top, foot = (cx + 6, cy + 6), (cx + 92, cy + 100)
    d.dashed(top, foot, dash=4, gap=3)
    _arrow(d, top, foot)
    # the wind, from the southwest in spring, across the strips
    d.line((24, 286), (64, 254))
    _arrow(d, (24, 286), (64, 254))

    d.group()
    # lister furrows in section: ridges and troughs, with drifted soil caught in each trough
    xs = [262 + 16 * i for i in range(9)]
    ridge = []
    for i, x in enumerate(xs):
        ridge.append((x, 132 - (14 if i % 2 else 0)))
    d.line(*ridge)
    for i in range(0, len(xs) - 1, 2):
        x = xs[i]
        if i:
            w = 16 * 6 / 14                                            # the trough's half-width 6 units up
            d.line((x - w, 126), (x + w, 126))                         # soil caught in the trough
            for dx, dy in ((-2.5, 129), (1.5, 128.5), (0, 130.5)):
                d.circle(x + dx, dy, 0.7)
    # a shelterbelt: rows of trees rising from the field edge, tallest in the middle rows
    heights = [14, 22, 30, 34, 30, 22]
    for j, h in enumerate(heights):
        x = 294 + 13 * j
        d.line((x - 5, 252), (x, 252 - h), (x + 5, 252))

    d.group('mid')
    for y in (100, 108):                                                # wind over the furrows
        d.line((262, y), (300, y))
        _arrow(d, (262, y), (300, y))
    # the wind lifted over the belt and set down far beyond it
    pts = [(262 + t, 236 - 30 * math.exp(-((t - 70) / 38) ** 2)) for t in range(0, 129, 4)]
    d.line(*pts)
    _arrow(d, pts[-2], pts[-1])

    d.group('mid')
    d.text(125, 22, 'STRIPS AND FURROWS ON THE CONTOUR', size=7)
    d.text(cx + 84, cy + 98, 'DOWNHILL', size=7, anchor='end')
    d.text(70, 286, 'WIND', size=7, anchor='start')
    d.text(326, 22, 'LISTER FURROWS', size=7)
    d.text(326, 150, 'SOIL CAUGHT IN THE TROUGHS', size=7)
    d.text(326, 182, 'SHELTERBELT', size=7)
    d.text(326, 270, 'WIND LIFTED OVER THE TREES', size=7)
    return d


def _ear(d, base, ang, length, n, w):
    """An ear of wheat: a rachis from base along ang (radians from vertical, leaning right), with n pairs of
    spikelets set alternately either side, each a small ellipse drawn as a closed polyline."""
    ux, uy = math.sin(ang), -math.cos(ang)                             # along the rachis
    px, py = -uy, ux                                                   # across it
    tip = (base[0] + ux * length, base[1] + uy * length)
    d.line(base, tip)
    for i in range(n):
        s = length * (i + 0.6) / (n + 0.2)
        for side in (-1, 1):
            cx = base[0] + ux * s + px * side * w * 0.55
            cy = base[1] + uy * s + py * side * w * 0.55
            pts = []
            for k in range(12):
                a = 2 * math.pi * k / 12
                ex, ey = 0.5 * w * math.cos(a), 0.28 * w * math.sin(a)  # long axis tilted 35 degrees off the rachis
                ca, sa = math.cos(side * 0.6), math.sin(side * 0.6)
                lx, ly = ex * ca - ey * sa, ex * sa + ey * ca
                pts.append((cx + lx * px + ly * ux, cy + lx * py + ly * uy))
            d.line(*pts, closed=True)
    return tip


def green_revolution():
    d = D()
    # A tall wheat and a semi-dwarf side by side, to one scale (1 cm = 1.4 units): about 150 cm against
    # about 90 cm, the heights given for the old wheats and Norin 10's descendants (Wikipedia, "Norin 10
    # wheat"). The tall one is drawn lodged, bent over at the base, with its upright height as a ghost.
    # The semi-dwarf carries a bigger ear on a thicker stem. The lever: a push F on the ear at height h
    # bends the base with a moment F x h. Proportions of leaves and ears are schematic.
    g, k = 262, 1.4
    xt, xd = 70, 300
    ht, hd = 150 * k, 90 * k

    d.group('thin')
    d.line((20, g), (390, g))                                          # the ground
    d.line((34, g), (34, g - 150 * k))                                 # a scale, 0-150 cm
    for cm in (0, 50, 100, 150):
        d.line((30, g - cm * k), (38, g - cm * k))
    d.line((xt, g), (xt, g - ht))                                      # the tall plant's upright line
    d.line((xt - 20, g - ht), (xd + 30, g - ht))                       # height guides
    d.line((xd - 20, g - hd), (xd + 30, g - hd))
    d.line((xd + 30, g), (xd + 30, g - hd))                            # the lever arm h
    _arrow(d, (xd + 30, g - hd / 2), (xd + 30, g - hd), size=4)
    _arrow(d, (xd + 30, g - hd / 2), (xd + 30, g), size=4)

    d.group()
    # the tall wheat, lodged: a kink low on the stem, then a long straight lean
    pts, x, y = [(xt, g)], xt, g
    for i in range(1, 46):
        s = i * ht / 45
        ang = math.radians(66) * min(1.0, s / 34) ** 1.5
        x += math.sin(ang) * ht / 45
        y -= math.cos(ang) * ht / 45
        pts.append((x, y))
    d.line(*pts)
    # the semi-dwarf: a thicker stem, drawn as two walls
    d.line((xd - 1.6, g), (xd - 1.1, g - hd))
    d.line((xd + 1.6, g), (xd + 1.1, g - hd))

    d.group('mid')
    a_end = math.radians(66)
    _ear(d, pts[-1], a_end, 16, 6, 4)                                  # the tall plant's smaller ear
    _ear(d, (xd, g - hd), 0.0, 24, 9, 5.5)                             # the semi-dwarf's larger ear
    for frac in (0.3, 0.55, 0.78):                                     # leaves at the dwarf's nodes
        y0 = g - hd * frac
        d.line((xd + 1.2, y0), (xd + 14, y0 - 10), (xd + 22, y0 - 6))
        d.line((xd - 1.2, y0 - 6), (xd - 13, y0 - 15), (xd - 20, y0 - 10))
    for i in (12, 22, 32):                                             # and at the tall plant's
        px_, py_ = pts[i]
        d.line((px_, py_), (px_ + 10, py_ + 9), (px_ + 18, py_ + 8))
    # the push of wind and rain on each ear
    ear_d = (xd, g - hd - 12)
    d.line((xd - 46, ear_d[1]), (xd - 8, ear_d[1]))
    _arrow(d, (xd - 46, ear_d[1]), (xd - 8, ear_d[1]))
    d.arc(xd, g, 12, 200, 270, n=16)                                   # the bending moment at the base
    _arrow(d, (xd + 12 * math.cos(math.radians(260)), g + 12 * math.sin(math.radians(260))),
           (xd, g - 12), size=3.5)

    d.group('mid')
    for cm in (0, 50, 100, 150):
        d.text(28, g - cm * k + 3, f'{cm}', size=7, anchor='end')
    d.text(34, g - 150 * k - 8, 'CM', size=7)
    d.text(xt + 80, 280, 'TALL WHEAT, LODGED', size=7)
    d.text(xd, 280, 'SEMI-DWARF', size=7)
    d.text(xd - 50, ear_d[1] - 6, 'F', size=7, anchor='middle')
    d.text(xd + 36, g - hd / 2 + 3, 'h', size=7, anchor='start')
    d.text(xd - 18, g - 18, 'M = F × h', size=7, anchor='end')
    d.text(200, 22, 'SAME PUSH, SHORTER LEVER', size=7)
    return d


PLATES = {'dust-bowl': dust_bowl, 'green-revolution': green_revolution}
