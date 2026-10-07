"""Plates for The Story of Life's part small3 (sprint 055): Pasteur's flasks and Cajal's neuron. See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _bezier(p0, p1, p2, p3, n=40):
    """Points along a cubic Bezier curve."""
    pts = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return pts


def _offset(pts, w):
    """A polyline offset sideways by w, along the normals of the centerline."""
    out = []
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1
        out.append((x - w * dy / n, y + w * dx / n))
    return out


def _bulb(d, cx, cy, r, neck_half, level):
    """A round-bottomed flask's bulb in section, open at the neck, with its broth level."""
    a0 = math.asin(neck_half / r)                                       # where the neck meets the sphere
    pts = []
    for k in range(73):
        a = -math.pi / 2 + a0 + (2 * math.pi - 2 * a0) * k / 72
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(*pts)
    half = math.sqrt(r * r - (level - cy) ** 2)                         # the broth's surface, a chord
    d.line((cx - half, level), (cx + half, level))
    return pts[0], pts[-1]


def swan_neck_flask():
    d = D()
    # Pasteur's memoir of 1862 (Ann. chim. phys. 64, pp. 66-68): broth boiled in a flask whose neck is drawn
    # out and bent, left open; dust settles in the moist bends and the broth stays clear. Beside it the same
    # flask with the neck cut off by a file: dust falls straight in and the broth clouds in one or two days.
    # Proportions schematic; the neck's centerline is a cubic Bezier, its walls offset from it.
    ground = 256
    r, nh = 44, 4
    lc = (100, ground - r - 6)                                          # left flask's center
    rc = (305, ground - r - 6)
    level = lc[1] + 14
    top = lc[1] - r + 2
    neck = (_bezier((lc[0], top), (lc[0], top - 80), (lc[0] + 46, top - 92), (lc[0] + 56, top - 40), 30)
            + _bezier((lc[0] + 56, top - 40), (lc[0] + 61, top - 12), (lc[0] + 86, top - 2), (lc[0] + 100, top - 22), 20)[1:]
            + _bezier((lc[0] + 100, top - 22), (lc[0] + 110, top - 37), (lc[0] + 120, top - 70), (lc[0] + 136, top - 92), 20)[1:])
    trough = max(neck[30:50], key=lambda p: p[1])                       # the low point of the bend
    d.group('thin')
    d.line((20, ground), (380, ground))
    for c in (lc, rc):
        d.line((c[0] - 8, c[1]), (c[0] + 8, c[1]))
        d.line((c[0], c[1] - 8), (c[0], c[1] + 8))
        d.line((c[0], c[1] + r + 6), (c[0], ground))
    d.dashed(*neck[::2], dash=3, gap=3)                                 # the neck's centerline
    d.line((trough[0] - 26, trough[1] + 6), (trough[0] + 26, trough[1] + 6))

    d.group()
    for c in (lc, rc):
        _bulb(d, c[0], c[1], r, nh, level)
        d.line((c[0] - 22, c[1] + r + 6), (c[0] + 22, c[1] + r + 6))   # the stand
        d.line((c[0] - 16, c[1] + r - 4), (c[0] - 22, c[1] + r + 6))
        d.line((c[0] + 16, c[1] + r - 4), (c[0] + 22, c[1] + r + 6))
    d.line(*_offset(neck, nh))
    d.line(*_offset(neck, -nh))
    stub = rc[1] - r - 12                                               # the cut-off neck
    d.line((rc[0] - nh, rc[1] - r + 2), (rc[0] - nh, stub))
    d.line((rc[0] + nh, rc[1] - r + 2), (rc[0] + nh, stub + 2))
    d.line((rc[0] - nh, stub), (rc[0] - 1, stub - 2), (rc[0] + 1, stub + 1), (rc[0] + nh, stub + 2))

    d.group('mid')
    tx, ty = trough
    for k, (dx, dy) in enumerate(((-9, 1), (-5, 2.5), (-1, 3), (3, 2.6), (7, 1.6), (11, 0.4), (-13, -0.4))):
        d.circle(tx + dx, ty + dy, 0.9 + (k % 3) * 0.35)               # dust caught in the bend
    for k in range(5):                                                  # moisture along the bend
        p = neck[30 + k * 3]
        d.circle(p[0], p[1] + 1.5, 0.6)
    tip = neck[-1]
    for k in range(3):                                                  # air drawn slowly in at the tip
        y = tip[1] - 22 + k * 9
        d.line((tip[0] + 30, y), (tip[0] + 10, y + 8))
        _arrow(d, (tip[0] + 30, y), (tip[0] + 10, y + 8), size=3.5)
    for k in range(9):                                                  # dust falling into the cut neck
        x = rc[0] - 10 + (k * 7) % 20
        y = 40 + k * 10
        d.circle(x, y, 1 + (k % 2) * 0.4)
    d.line((rc[0] + 22, 44), (rc[0] + 22, stub - 8))
    _arrow(d, (rc[0] + 22, 44), (rc[0] + 22, stub - 8), size=4)
    for k in range(16):                                                 # the clouded broth
        a = k * 2.399
        rr = 6 + 30 * math.sqrt((k + 0.5) / 16)
        x, y = rc[0] + rr * math.cos(a), level + 6 + abs(rr * math.sin(a)) * 0.55
        if (x - rc[0]) ** 2 + (y - rc[1]) ** 2 < (r - 4) ** 2:
            d.circle(x, y, 1.1)

    d.group('mid')
    d.text(tx + 6, ty + 22, 'DUST CAUGHT IN THE BEND', size=7)
    d.text(tip[0] - 8, tip[1] - 6, 'OPEN TIP', size=7, anchor='end')
    d.text(lc[0], ground + 14, 'BROTH STAYS CLEAR', size=7)
    d.text(rc[0], ground + 14, 'CLOUDY IN 1–2 DAYS', size=7)
    d.text(rc[0] + 28, 64, 'DUST FALLS IN', size=7, anchor='start')
    d.text(rc[0] + 14, stub + 4, 'NECK CUT OFF', size=7, anchor='start')
    d.text(200, 290, 'THE SWAN-NECK FLASK IN SECTION · PARIS, 1860', size=7)
    return d


def _branch(d, x, y, ang, length, depth, spread, shrink, ends):
    """A branching tree from (x, y), angle in degrees from straight up; its tips are collected in ends."""
    a = math.radians(ang)
    x2, y2 = x + length * math.sin(a), y - length * math.cos(a)
    d.line((x, y), (x2, y2))
    if depth > 1:
        for s in (-spread, spread * 0.8):
            _branch(d, x2, y2, ang + s, length * shrink, depth - 1, spread, shrink, ends)
    else:
        ends.append((x2, y2))


def neuron_doctrine():
    d = D()
    # A neuron after Cajal's drawings of the cerebellum: a cell body, a dendritic tree, an axon that ends
    # in free branches on the body of a second cell, with a gap between them. Arrows give the direction of
    # the impulse in Cajal's law of dynamic polarization (1891): dendrites and body toward the axon, and on
    # to the next cell. The tree is a computed binary branching, not traced; proportions schematic.
    soma = (150, 150)
    soma2 = (290, 238)

    d.group('thin')
    d.line((soma[0], 40), (soma[0], 280))                               # the cell's axis
    for c, rad in ((soma, 26), (soma2, 22)):
        d.circle(c[0], c[1], rad)
    d.line((soma2[0] - 30, soma2[1] - 30), (soma2[0] + 30, soma2[1] - 30))

    d.group()
    d.ellipse(soma[0], soma[1], 11, 13)                                 # the first cell
    ends = []
    for ang in (-34, -12, 12, 34):                                      # its dendritic tree
        _branch(d, soma[0] + ang * 0.15, soma[1] - 11, ang, 30, 4, 17, 0.72, ends)
    axon = [(soma[0], soma[1] + 13)]
    for k in range(1, 21):                                              # the axon, curving down and over
        t = k / 20
        axon.append((soma[0] + 104 * t ** 2, soma[1] + 13 + 58 * math.sin(t * math.pi / 2)))
    d.line(*axon)
    d.ellipse(soma2[0], soma2[1], 10, 12)                               # the second cell
    for ang in (-30, 0, 30):
        a = math.radians(ang)
        d.line((soma2[0] + 6 * math.sin(a), soma2[1] - 12), (soma2[0] + 40 * math.sin(a), soma2[1] - 44))

    d.group('mid')
    end = axon[-1]
    gap = 4
    for k, th in enumerate((150, 185, 220, 255)):                       # free terminal branches around the
        a = math.radians(th)                                            # next cell, stopping short of it
        tx = soma2[0] + (10 + gap) * math.cos(a)
        ty = soma2[1] + (12 + gap) * math.sin(a)
        mx = (end[0] + tx) / 2 + 6 * math.cos(a)
        my = (end[1] + ty) / 2 + 6 * math.sin(a)
        d.curve(f"M{end[0]:.1f},{end[1]:.1f} Q{mx:.1f},{my:.1f} {tx:.1f},{ty:.1f}")
        d.circle(tx, ty, 1.4)
    for x, y in ends:                                                   # spines at the tips
        d.circle(x, y, 1)

    d.group('mid')
    for p, q in (((soma[0] - 40, 64), (soma[0] - 16, 120)), ((soma[0] + 40, 64), (soma[0] + 16, 120))):
        d.line(p, q)                                                    # into the cell body
        _arrow(d, p, q, size=4)
    p, q = axon[6], axon[11]
    d.line((p[0] - 10, p[1] + 10), (q[0] - 10, q[1] + 10))
    _arrow(d, (p[0] - 10, p[1] + 10), (q[0] - 10, q[1] + 10), size=4)
    d.line((soma2[0] - 52, soma2[1] + 26), (soma2[0] - 22, soma2[1] + 18))
    _arrow(d, (soma2[0] - 52, soma2[1] + 26), (soma2[0] - 22, soma2[1] + 18), size=4)

    d.group('mid')
    d.text(soma[0], 30, 'DENDRITES', size=7)
    d.text(soma[0] - 16, soma[1] + 4, 'BODY', size=7, anchor='end')
    d.text(axon[12][0] + 8, axon[12][1] - 6, 'AXON', size=7, anchor='start')
    d.text(soma2[0] + 16, soma2[1] + 4, 'NEXT CELL', size=7, anchor='start')
    d.text(soma2[0] - 30, soma2[1] + 40, 'CONTACT, NOT CONTINUITY', size=7)
    d.text(200, 290, 'DYNAMIC POLARIZATION · CAJAL, 1891', size=7)
    return d


PLATES = {'swan-neck-flask': swan_neck_flask, 'neuron-doctrine': neuron_doctrine}
