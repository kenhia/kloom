"""Plates for The Story of Life's part time2 (sprint 055): Mary Anning's plesiosaur and Lyell's columns.
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


def _paddle(d, root, ang, length, width):
    """A paddle as a tapered blade from root, pointing at ang (degrees, 0 = +x, clockwise positive)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    pts_a, pts_b = [], []
    for k in range(13):
        t = k / 12
        w = width * math.sin(math.pi * min(1.0, 0.15 + t * 0.95)) * (1 - 0.55 * t)
        cx, cy = root[0] + ux * length * t, root[1] + uy * length * t
        pts_a.append((cx + nx * w / 2, cy + ny * w / 2))
        pts_b.append((cx - nx * w / 2, cy - ny * w / 2))
    d.line(*pts_a, *reversed(pts_b), closed=True)
    return ux, uy, nx, ny


def _phalanges(d, root, ang, length, width, digits):
    """Rows of small bones along a paddle: one row per digit, the bone counts Conybeare gave."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    for i, n in enumerate(digits):
        off = (i - (len(digits) - 1) / 2) * width * 0.16
        for k in range(n):
            t = 0.22 + 0.7 * k / max(1, n - 1) * (n / max(digits))
            taper = 1 - 0.55 * t
            x = root[0] + ux * length * t + nx * off * taper
            y = root[1] + uy * length * t + ny * off * taper
            d.circle(x, y, 0.9)


def mary_anning():
    d = D()
    # Plesiosaurus dolichodeirus in plan view, as Anning sketched it in December 1823 and Conybeare
    # described it on 20 February 1824. Conybeare's proportions: head 1, neck 5, body 4, tail 3, the
    # whole thirteen heads long. His count: 35 cervical vertebrae (with 6 anterior dorsals, 41 before
    # the forelimbs), 21 dorsal and lumbar, 2 sacral, about 26 caudal; about 90 in all. Paddle bone
    # counts per digit from his table (front 4,7,7,6,7; hind 4,8,10,9,7, the first hind digit's count
    # being illegible in the scan and taken as 4). Shapes of skull, ribs and paddles schematic.
    x0, x1 = 30, 370
    u = (x1 - x0) / 13
    xh, xn, xb, xt = x0 + u, x0 + 6 * u, x0 + 10 * u, x1          # ends of head, neck, body, tail
    base = 150

    def spine_y(x):
        if x < xn:                                                    # the neck lifts toward the head
            s = (xn - x) / (xn - x0)
            return base - 26 * s * s
        if x > xb:                                                    # the tail droops a little
            s = (x - xb) / (xt - xb)
            return base + 6 * s * s
        return base

    def normal(x):
        h = 0.5
        dy = (spine_y(x + h) - spine_y(x - h)) / (2 * h)
        n = math.hypot(1, dy)
        return -dy / n, 1 / n

    d.group('thin')
    for x in (x0, xh, xn, xb, xt):                                    # the four divisions
        d.line((x, 52), (x, 248))
    for k in range(14):                                               # a scale of thirteen head-lengths
        x = x0 + k * u
        d.line((x, 258), (x, 264))
    d.line((x0, 261), (x1, 261))
    pts = [(x, spine_y(x)) for x in [x0 + i * (x1 - x0) / 80 for i in range(81)]]
    d.dashed(*pts, dash=3, gap=3)                                     # the axis of the column

    d.group()
    # skull: a small pointed oval, about one thirteenth of the length
    hy = spine_y(x0 + u / 2)
    sk = []
    for k in range(25):
        t = math.pi * 2 * k / 24
        r = 1 - 0.45 * max(0.0, math.cos(t))                          # narrower toward the snout
        sk.append((x0 + u / 2 + (u / 2) * math.cos(t), hy + 6.5 * r * math.sin(t)))
    d.line(*sk, closed=True)
    d.circle(x0 + u * 0.62, hy - 1.5, 1.6)                             # orbit
    # vertebrae: 35 cervical in the neck
    for i in range(35):
        x = xh + (i + 0.5) * (xn - xh) / 35
        y = spine_y(x)
        nx, ny = normal(x)
        h = 3.0 + 2.2 * i / 34
        d.line((x - nx * h, y - ny * h), (x + nx * h, y + ny * h))
    # 6 anterior dorsal, 21 dorsal and lumbar, 2 sacral in the body
    nb = 6 + 21 + 2
    for i in range(nb):
        x = xn + (i + 0.5) * (xb - xn) / nb
        h = 6.0 if i >= 6 else 5.4
        _box(d, x - 1.2, base - h, 2.4, 2 * h)
    # about 26 caudal, shrinking
    for i in range(26):
        x = xb + (i + 0.5) * (xt - xb) / 26
        y = spine_y(x)
        h = 5.0 * (1 - i / 30)
        d.line((x, y - h), (x, y + h))
    # paddles: the fore pair at the shoulder, the hind pair at the hip
    fx, hx = xn + 1.6 * u, xb - 0.35 * u
    for side in (-1, 1):
        _paddle(d, (fx, base + side * 8), 55 * side, 78, 20)       # swept back from the shoulder
        _paddle(d, (hx, base + side * 8), 40 * side, 70, 18)       # and from the hip

    d.group('mid')
    for k in range(14):                                               # fourteen large ribs
        x = xn + 0.35 * u + k * (2.9 * u) / 13
        for side in (-1, 1):
            d.curve(f"M{x:.1f},{base + side * 6:.1f} Q{x + 9:.1f},{base + side * 26:.1f} {x + 4:.1f},{base + side * 42:.1f}")
    _phalanges(d, (fx, base - 8), -55, 78, 20, [4, 7, 7, 6, 7])
    _phalanges(d, (fx, base + 8), 55, 78, 20, [4, 7, 7, 6, 7])
    _phalanges(d, (hx, base - 8), -40, 70, 18, [4, 8, 10, 9, 7])
    _phalanges(d, (hx, base + 8), 40, 70, 18, [4, 8, 10, 9, 7])
    d.circle(fx, base, 3)                                             # shoulder and hip
    d.circle(hx, base, 3)

    d.group('mid')
    d.text((x0 + xh) / 2, 276, 'HEAD 1', size=7)
    d.text((xh + xn) / 2, 276, 'NECK 5', size=7)
    d.text((xn + xb) / 2, 276, 'BODY 4', size=7)
    d.text((xb + xt) / 2, 276, 'TAIL 3', size=7)
    d.text((xh + xn) / 2, 100, '35 CERVICAL', size=7)
    d.text((xn + xb) / 2, 44, '6 + 21 DORSAL · 2 SACRAL', size=7)
    d.text((xb + xt) / 2 + 8, 228, 'ABOUT 26 CAUDAL', size=7)
    d.text(200, 22, 'PLESIOSAURUS DOLICHODEIRUS · CONYBEARE, 1824 · ABOUT 90 VERTEBRAE', size=7)
    return d


def _borings(d, cx, w, y_lo, y_hi, seed):
    """Pear-shaped borings scattered over a band of a column: a fixed lattice, jittered by a hash."""
    rows = int((y_lo - y_hi) / 5)
    for r in range(rows):
        for c in range(4):
            h = (seed * 7919 + r * 104729 + c * 1299709) % 1000 / 1000
            x = cx - w / 2 + 2.5 + (c + (0.5 if r % 2 else 0)) * (w - 5) / 4 + (h - 0.5) * 1.6
            y = y_hi + 2.5 + r * 5 + (h - 0.5) * 1.4
            if cx - w / 2 + 1.5 < x < cx + w / 2 - 1.5:
                d.ellipse(x, y, 0.8 + 0.5 * h, 1.2 + 0.6 * h)


def lyell():
    d = D()
    # The three standing columns of the "Temple of Serapis" at Pozzuoli as Lyell measured them in 1828
    # (Principles of Geology I, 1830, pp. 453-54): 42 feet high; smooth for about 12 feet above the
    # pedestals; then a zone 12 feet high bored by the marine bivalve Lithodomus (Lithophaga); the
    # platform about 1 foot below high water; the top of the borings at least 23 feet above high water.
    # The lower part was protected by a fill of tuff and rubbish "ten or twelve feet" deep (p. 456).
    # Heights to scale, 5 units to the foot; the columns' width is schematic.
    ft = 5.0
    floor = 262

    def y(f):
        return floor - f * ft
    xs = [214, 270, 326]
    w = 20
    ped_h = 1.6                                                       # pedestal blocks, schematic
    left, right = 64, 352

    d.group('thin')
    d.line((left, floor), (right, floor))                             # the platform
    d.line((40, y(0)), (40, y(42)))                                   # height scale in feet
    for f in range(0, 43, 6):
        d.line((36, y(f)), (44, y(f)))
    for f in (12, 24, 42):                                            # the band's limits, across all three
        d.line((190, y(f)), (right, y(f)))

    d.group()
    for i, cx in enumerate(xs):
        _box(d, cx - w / 2 - 4, y(ped_h), w + 8, ped_h * ft)          # pedestal
        top = 42 - (0, 1.2, 0.4)[i]                                   # broken tops, a little uneven
        d.line((cx - w / 2, y(ped_h)), (cx - w / 2, y(top)), (cx - 3, y(top + 0.5)),
               (cx + 4, y(top - 0.3)), (cx + w / 2, y(top)), (cx + w / 2, y(ped_h)))

    d.group('mid')
    for i, cx in enumerate(xs):
        _borings(d, cx, w, y(12), y(24), i + 1)
    for k in range(0, 27):                                            # the fill that kept off the borers
        x = 190 + k * 6
        if x + 9 <= right:
            d.line((x, y(0)), (x + 9, y(11)))
    d.line((190, y(11)), (right, y(11)))

    d.group('mid')
    d.dashed((left, y(24)), (right, y(24)), dash=5, gap=3)            # the sea at its highest
    d.dashed((left, y(1)), (right, y(1)), dash=5, gap=3)              # high water when Lyell visited
    d.line((364, y(22)), (364, y(3)))                                 # sank, then rose
    _arrow(d, (364, y(22)), (364, y(3)), size=4)
    d.line((376, y(3)), (376, y(22)))
    _arrow(d, (376, y(3)), (376, y(22)), size=4)

    d.group('mid')
    for f in (0, 12, 24, 42):
        d.text(32, y(f) + 2.5, f'{f} FT', size=7, anchor='end')
    d.text(184, y(24) - 4, 'SEA AT ITS HIGHEST', size=7, anchor='end')
    d.text(184, y(18) + 2.5, 'BORED BY LITHOPHAGA', size=7, anchor='end')
    d.text(184, y(42) + 2.5, 'LYELL: 42 FEET HIGH', size=7, anchor='end')
    d.text(184, y(6) + 2.5, 'BURIED IN TUFF', size=7, anchor='end')
    d.text(184, y(1) - 3, 'HIGH WATER, 1828', size=7, anchor='end')
    d.text(370, y(24) - 6, 'SANK · ROSE', size=7)
    d.text(200, 16, 'TEMPLE OF SERAPIS, PUZZUOLI · AFTER LYELL, 1830', size=7)
    return d


PLATES = {'mary-anning': mary_anning, 'lyell': lyell}
