"""Plates for In the Blood's trail Clotting, part clot2: warfarin, hemophilia-hiv, recombinant-factor (sprint 028).

See plates_for.py. `_pt` and `_arrow` are copied from blood_belief.py, as the brief asks.
"""
import math
from plates import D


def _pt(cx, cy, r, a):
    """The point at `a` degrees on a circle (clockwise from +x; SVG's y runs down)."""
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _inner(p, q, c, k=0.18):
    """A double bond's second line: the edge p-q pulled toward the ring centre c and shortened."""
    def towards(a):
        return a[0] + (c[0] - a[0]) * k, a[1] + (c[1] - a[1]) * k
    p2, q2 = towards(p), towards(q)
    t = 0.14
    return ((p2[0] + (q2[0] - p2[0]) * t, p2[1] + (q2[1] - p2[1]) * t),
            (q2[0] + (p2[0] - q2[0]) * t, q2[1] + (p2[1] - q2[1]) * t))


def _offset(p, q, dist):
    """The segment p-q moved sideways by `dist`."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * dist, dx / n * dist
    return (p[0] + ox, p[1] + oy), (q[0] + ox, q[1] + oy)


def warfarin():
    d = D()
    # Dicumarol, 3,3'-methylenebis(4-hydroxycoumarin), as Huebner worked it out in 1940: two
    # 4-hydroxycoumarin units (a benzene ring fused to a lactone ring) joined at C3 by a CH2 bridge.
    # Pointy-topped hexagons of side s; the right unit is the left one mirrored about the bridge.
    s = 26
    h = s * math.sqrt(3) / 2
    cy = 150
    # left unit: benzene ring A, lactone ring B fused on A's right edge
    ax = 200 - 4 * h                                                 # so the bridge sits on x = 200
    bx = ax + 2 * h
    hexa = lambda cx: [_pt(cx, cy, s, a) for a in (-90, -30, 30, 90, 150, 210)]
    A, B = hexa(ax), hexa(bx)
    # ring B's atoms: top C4, upper-right C3, lower-right C2, bottom O1, lower-left C8a, upper-left C4a
    c4, c3, c2, o1 = B[0], B[1], B[2], B[3]
    bridge = (c3[0] + s * math.cos(math.radians(-30)), c3[1] + s * math.sin(math.radians(-30)))
    mx = bridge[0]
    mirror = lambda p: (2 * mx - p[0], p[1])
    oh = (c4[0], c4[1] - s * 0.9)                                     # C4's OH, straight up
    # C2=O, kept short: drawn flat, the two carbonyls point at each other across the bridge
    co = (c2[0] + s * 0.5 * math.cos(math.radians(30)), c2[1] + s * 0.5 * math.sin(math.radians(30)))
    d.group('thin')
    d.line((20, cy), (2 * mx - 20, cy))                               # the axis through the ring centres
    d.line((mx, 56), (mx, 196))                                       # the mirror line through the bridge
    for cx in (ax, bx, 2 * mx - bx, 2 * mx - ax):
        d.circle(cx, cy, s, cls=None)                                 # each ring's circumscribed circle
    d.group()
    for ring in (A, B):
        d.line(*ring, closed=True)
        d.line(*[mirror(p) for p in ring], closed=True)
    for p, q in ((c3, bridge), (c4, oh), (c2, co)):
        d.line(p, q)
        d.line(mirror(p), mirror(q))
    d.group('mid')
    # double bonds: three alternating in each benzene ring, C3=C4 in each lactone ring, C2=O outside
    for i in (0, 2, 4):
        p, q = _inner(A[i], A[(i + 1) % 6], (ax, cy))
        d.line(p, q)
        d.line(mirror(p), mirror(q))
    p, q = _inner(c4, c3, (bx, cy))
    d.line(p, q)
    d.line(mirror(p), mirror(q))
    p, q = _offset(c2, co, 3.2)
    d.line(p, q)
    d.line(mirror(p), mirror(q))
    # below, the vitamin K cycle in plan: the liver uses reduced vitamin K to finish the clotting
    # factors (top arc), and the enzyme VKOR recycles the epoxide (bottom arc); dicumarol and
    # warfarin block VKOR, struck through.
    kx, ky, kr = 200, 236, 20
    d.group('mid')
    d.arc(kx, ky, kr, 196, 344, n=24)
    d.arc(kx, ky, kr, 16, 164, n=24)
    _arrow(d, _pt(kx, ky, kr, 330), _pt(kx, ky, kr, 344))
    _arrow(d, _pt(kx, ky, kr, 150), _pt(kx, ky, kr, 164))
    d.lines([[(kx - 6, ky + kr - 6), (kx + 6, ky + kr + 6)], [(kx - 6, ky + kr + 6), (kx + 6, ky + kr - 6)]])
    d.group('mid')
    d.text(o1[0], o1[1] + 11, 'O', size=7)
    d.text(mirror(o1)[0], o1[1] + 11, 'O', size=7)
    d.text(co[0] + 1, co[1] + 9, 'O', size=7)
    d.text(mirror(co)[0] - 1, co[1] + 9, 'O', size=7)
    d.text(oh[0], oh[1] - 4, 'OH', size=7)
    d.text(mirror(oh)[0], oh[1] - 4, 'HO', size=7)
    d.text(mx, bridge[1] - 7, 'CH₂', size=7)
    d.text(mx, 44, 'DICUMAROL  C₁₉H₁₂O₆', size=7)
    d.text(kx - kr - 8, ky + 3, 'VITAMIN K', size=7, anchor='end')
    d.text(kx + kr + 8, ky + 3, 'K EPOXIDE', size=7, anchor='start')
    d.text(kx, ky - kr - 8, 'CLOTTING FACTORS', size=7)
    d.text(kx, ky + kr + 16, 'VKOR', size=7)
    return d


def hemophilia_hiv():
    d = D()
    # The funnel of a plasma pool: a grid of single donations (each circle stands for many) drains
    # into one pooling tank, and the tank fills one lot of vials. One infected donation, crossed,
    # reaches the tank and so every vial of the lot. Not to scale.
    cols, rows = 6, 12
    gx0, gy0, gdx, gdy, r = 28, 46, 11, 18, 3.2
    donors = [(gx0 + i * gdx, gy0 + j * gdy) for j in range(rows) for i in range(cols)]
    bad = donors[(rows - 1) * cols + 2]
    tx0, tx1, ttop, tbot = 166, 234, 100, 214                       # the tank, in section
    inlet, outlet = (tx0, 118), (200, tbot + 14)
    vcols, vrows = 5, 4
    vx0, vy0, vdx, vdy = 286, 78, 20, 46
    vials = [(vx0 + i * vdx, vy0 + j * vdy) for j in range(vrows) for i in range(vcols)]
    d.group('thin')
    # construction: the funnel from the grid's corners to the inlet, and from the outlet to the lot
    gx1, gy1 = donors[-1]
    for y in (gy0 - 8, gy1 + 8):
        d.line((gx1 + 10, y), inlet)
    for v in (vials[0], vials[vcols - 1], vials[-vcols], vials[-1]):
        d.line((262, 160), (v[0], v[1] + 8))
    d.line((14, 160), (386, 160))                                    # the axis of the flow
    d.group()
    for x, y in donors:
        d.circle(x, y, r)
    # the tank: a cylinder with a dished foot, a lid, a stirrer and the level of the pooled plasma
    d.ellipse((tx0 + tx1) / 2, ttop, (tx1 - tx0) / 2, 7)
    d.line((tx0, ttop), (tx0, tbot))
    d.line((tx1, ttop), (tx1, tbot))
    d.arc((tx0 + tx1) / 2, tbot, (tx1 - tx0) / 2, 0, 180, n=24, ry=12)
    d.line(inlet, (tx0 - 22, inlet[1]))
    d.line((200, tbot + 12), (200, 246), (262, 246), (262, 160))     # the outlet to the filling line
    # the vials of one lot: a body and a neck each
    for x, y in vials:
        d.line((x - 6, y), (x - 6, y + 22), (x + 6, y + 22), (x + 6, y), (x + 3, y - 3), (x + 3, y - 7),
               (x - 3, y - 7), (x - 3, y - 3), closed=True)
    d.group('mid')
    d.line((tx0 + 4, 132), (tx1 - 4, 132))                           # the liquid level
    d.line((200, ttop - 7), (200, 192))                              # the stirrer's shaft
    d.line((186, 186), (214, 198))
    d.line((186, 198), (214, 186))
    # the one infected donation, crossed, and its path to the tank and into every vial
    d.lines([[(bad[0] - r, bad[1] - r), (bad[0] + r, bad[1] + r)], [(bad[0] - r, bad[1] + r), (bad[0] + r, bad[1] - r)]])
    d.circle(bad[0], bad[1], r + 3)
    _arrow(d, (tx0 - 22, inlet[1]), inlet)
    _arrow(d, (262, 200), (262, 160))
    for x, y in vials:
        d.lines([[(x - 2.5, y + 8.5), (x + 2.5, y + 13.5)], [(x - 2.5, y + 13.5), (x + 2.5, y + 8.5)]])
    d.group('mid')
    d.text(gx0 - 4, 26, 'DONATIONS 1,000–30,000', size=7, anchor='start')
    d.text(gx0 - 4, bad[1] + 22, 'ONE INFECTED', size=7, anchor='start')
    d.text(200, 84, 'POOL', size=7)
    d.text(386, 56, 'ONE LOT · EVERY VIAL', size=7, anchor='end')
    return d


def recombinant_factor():
    d = D()
    # Prophylaxis with factor VIII, computed: 25 IU/kg (a rise of 50 IU/dL, at 2 IU/dL per IU/kg)
    # on Monday, Wednesday and Friday, and Monday again, each dose decaying with a half-life of
    # 12 hours, on a log scale where each fall is a straight line. The patient's own level is taken
    # as nil. The long weekend gap falls below 1 IU/dL, the line between severe and moderate.
    x0, x1, yb, yt = 52, 372, 250, 54
    tmax, vmin, vmax = 192, 0.5, 100
    doses, rise, half = (0, 48, 96, 168), 50, 12
    X = lambda t: x0 + (x1 - x0) * t / tmax
    Y = lambda v: yb - (yb - yt) * (math.log10(v) - math.log10(vmin)) / (math.log10(vmax) - math.log10(vmin))
    d.group('thin')
    for v in (10, 100):                                              # decades of the log scale
        d.line((x0, Y(v)), (x1, Y(v)))
    for v in (2, 5, 20, 50):                                         # and ticks between them
        d.line((x0, Y(v)), (x0 + 5, Y(v)))
    for t in range(0, tmax + 1, 24):                                 # a tick a day
        d.line((X(t), yb), (X(t), yb - 5))
    d.group()
    d.line((x0, yt - 6), (x0, yb), (x1 + 6, yb))                     # the axes
    # the level, computed hour by hour: a jump at each dose, an exponential fall between
    pts, level, t = [], 0.0, 0
    for t in range(0, tmax + 1):
        if t in doses:
            if pts:
                pts.append((X(t), Y(max(level, vmin))))
            level += rise
        pts.append((X(t), Y(max(level, vmin))))
        level *= 0.5 ** (1 / half)
    d.line(*pts)
    d.group('mid')
    for k in range(int((x1 - x0) / 8)):                              # 1 IU/dL, dashed
        xa = x0 + k * 8
        d.line((xa, Y(1)), (min(xa + 4, x1), Y(1)))
    for t in doses:
        _arrow(d, (X(t), yt - 14), (X(t), yt - 4), size=4)
    d.group('mid')
    for v, s in ((1, '1'), (10, '10'), (100, '100')):
        d.text(x0 - 6, Y(v) + 3, s, size=7, anchor='end')
    d.text(x0 - 6, yt - 10, 'IU/DL', size=7, anchor='end')
    for t, s in zip(doses, ('MON', 'WED', 'FRI', 'MON')):
        d.text(X(t), yb + 14, s, size=7)
    d.text(X(60), yt - 18, '25 IU/KG = +50 IU/DL', size=7, anchor='start')
    d.text(X(5), Y(72), 'HALF-LIFE 12 H', size=7, anchor='start')
    d.text(X(162), Y(1) + 13, 'UNDER 1 IU/DL', size=7, anchor='end')
    return d


PLATES = {'warfarin': warfarin, 'hemophilia-hiv': hemophilia_hiv, 'recombinant-factor': recombinant_factor}
