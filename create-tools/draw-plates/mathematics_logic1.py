"""Plates for the mathematics subject's Logic and foundations segment, part logic1 (sprint 024):
Boole's algebra, Cantor's diagonal, Russell's paradox."""
import math
from plates import D


def cantor():
    """The diagonal argument of 1891, in Cantor's own two characters m and w.

    The first three rows are the three elements Cantor wrote out as examples;
    the rest are invented. The diagonal is ringed, and each of its characters,
    swapped, drops to the new row E0, which differs from every row in one place.
    """
    rows = [
        'mmmmmmm',          # Cantor's E_I
        'wwwwwww',          # E_II
        'mwmwmwm',          # E_III
        'wmmwwmw',          # invented from here on
        'mmwwmmw',
        'wmwmmwm',
        'mwwmwmw',
    ]
    n = len(rows)
    x0, y0, cw, ch = 83, 26, 32, 24          # grid origin, cell width and height
    ny = y0 + n * ch + 38                     # the new row's top
    cx = lambda j: x0 + (j + 0.5) * cw
    cy = lambda i: y0 + (i + 0.5) * ch
    right = x0 + (n + 1) * cw                 # one column more, for the dots
    d = D()
    d.group('thin')
    # the table's rulings, left open on the right (each row runs on for ever)
    d.lines([[(x0, y0 + i * ch), (right, y0 + i * ch)] for i in range(n + 1)] +
            [[(x0 + j * cw, y0), (x0 + j * cw, y0 + n * ch)] for j in range(n + 1)] +
            [[(x0, ny), (right, ny)], [(x0, ny + ch), (right, ny + ch)]] +
            [[(x0 + j * cw, ny), (x0 + j * cw, ny + ch)] for j in range(n + 1)])
    # and the drop from each diagonal place to the new row
    d.lines([[(cx(k), y0 + n * ch + 4), (cx(k), ny - 2)] for k in range(n)])
    d.group()
    # the diagonal: a ring on each of its places, joined corner to corner
    r = 9
    for k in range(n):
        d.circle(cx(k), cy(k), r)
    u = r / math.hypot(cw, ch)
    d.lines([[(cx(k) + cw * u, cy(k) + ch * u), (cx(k + 1) - cw * u, cy(k + 1) - ch * u)] for k in range(n - 1)])
    d.group('mid')
    # arrowheads where the drops land
    d.lines([[(cx(k) - 3, ny - 7), (cx(k), ny - 2), (cx(k) + 3, ny - 7)] for k in range(n)])
    d.group('mid')
    for i, r in enumerate(rows):
        d.text(x0 - 22, cy(i) + 3, f'E{i + 1}')
        for j, c in enumerate(r):
            d.text(cx(j), cy(i) + 3, c)
        d.text(cx(n), cy(i) + 3, '…')
    d.text(x0 - 22, ny + ch / 2 + 3, 'E0')
    for k in range(n):
        d.text(cx(k), ny + ch / 2 + 3, 'w' if rows[k][k] == 'm' else 'm')
    d.text(cx(n), ny + ch / 2 + 3, '…')
    d.text(cx(n), (y0 + n * ch + ny) / 2 + 3, 'm ↔ w', size=7)
    d.text(x0 + n * cw / 2, ny + ch + 14, 'DIFFERS FROM EVERY ROW', size=7)
    return d


def _switch(d, x0, x1, y, lift=24):
    """An open knife switch between contacts at x0 and x1 on a wire at height y."""
    d.circle(x0, y, 2.5)
    d.circle(x1, y, 2.5)
    a = math.radians(lift)
    L = (x1 - x0) * 1.05
    d.line((x0 + 2.5 * math.cos(a), y - 2.5 * math.sin(a)), (x0 + L * math.cos(a), y - L * math.sin(a)))


def _battery(d, x, y):
    """Cells on a vertical wire: a long plate and a short one, twice."""
    d.lines([[(x - 10, y - 6), (x + 10, y - 6)], [(x - 5, y - 2), (x + 5, y - 2)],
             [(x - 10, y + 2), (x + 10, y + 2)], [(x - 5, y + 6), (x + 5, y + 6)]])


def _lamp(d, x, y, r=9):
    d.circle(x, y, r)
    k = r / math.sqrt(2)
    d.lines([[(x - k, y - k), (x + k, y + k)], [(x - k, y + k), (x + k, y - k)]])


def boole():
    """Two switches in series (x·y) and in parallel (x + y − xy), each in a loop
    with a battery and a lamp: the lamp lights when the product, or the sum, is 1."""
    d = D()
    L, R = 40, 360
    t1, b1 = 40, 100                       # the series loop's top and bottom rails
    sx = [(130, 170), (230, 270)]
    t2, b2 = 188, 256                      # the parallel loop's rails
    n1, n2, u, v = 110, 290, 164, 214       # branch nodes and the two branches
    px = (180, 220)
    d.group('thin')
    # construction: the switches' contact lines carried through both loops, and the loops' centre lines
    d.lines([[(x, t1 - 14), (x, b1 + 4)] for pair in sx for x in pair] +
            [[(x, u - 14), (x, v + 8)] for x in px])
    d.lines([[(L - 14, (t1 + b1) / 2), (R + 14, (t1 + b1) / 2)], [(L - 14, (t2 + b2) / 2), (R + 14, (t2 + b2) / 2)]])
    d.group()
    # the series loop: battery up the left side, lamp down the right, switches on the top rail
    m1 = (t1 + b1) / 2
    d.line((L, m1 - 6), (L, t1), (sx[0][0] - 2.5, t1))
    d.line((sx[0][1] + 2.5, t1), (sx[1][0] - 2.5, t1))
    d.line((sx[1][1] + 2.5, t1), (R, t1), (R, m1 - 9))
    d.line((R, m1 + 9), (R, b1), (L, b1), (L, m1 + 6))
    # the parallel loop: the top rail splits into two branches, one switch on each
    m2 = (t2 + b2) / 2
    d.line((L, m2 - 6), (L, t2), (n1, t2))
    d.line((n1, u), (n1, v))
    d.line((n1, u), (px[0] - 2.5, u))
    d.line((n1, v), (px[0] - 2.5, v))
    d.line((px[1] + 2.5, u), (n2, u), (n2, v), (px[1] + 2.5, v))
    d.line((n2, t2), (R, t2), (R, m2 - 9))
    d.line((R, m2 + 9), (R, b2), (L, b2), (L, m2 + 6))
    d.group('mid')
    for x0, x1 in sx:
        _switch(d, x0, x1, t1)
    for y in (u, v):
        _switch(d, px[0], px[1], y)
    _battery(d, L, m1)
    _battery(d, L, m2)
    _lamp(d, R, m1)
    _lamp(d, R, m2)
    d.circle(n1, t2, 1.5)
    d.circle(n2, t2, 1.5)
    d.group('mid')
    d.text(150, t1 - 20, 'x')
    d.text(250, t1 - 20, 'y')
    d.text(200, u - 20, 'x')
    d.text(200, v - 20, 'y')
    d.text(200, b1 + 18, 'SERIES  ·  x y', size=8)
    d.text(200, b2 + 20, 'PARALLEL  ·  x + y − x y', size=8)
    return d



def frege_russell():
    """Frege's own statement of the contradiction (Grundgesetze II, 1903, p. 253): the class
    of men is not a man, so it belongs to K, the class of classes that do not belong to
    themselves. K itself can be put neither inside K nor outside it; the loop is why."""
    d = D()
    cx, cy, r = 150, 150, 100                # K, the class of classes not members of themselves
    d.group('thin')
    d.line((cx - r - 16, cy), (cx + r + 60, cy))           # the centre line through K and its copy
    d.line((cx, cy - r - 12), (cx, cy + r + 12))
    d.group()
    d.circle(cx, cy, r)
    # normal classes inside K: the class of men, and two others
    inner = [(112, 112, 30), (190, 104, 22), (128, 196, 24)]
    for x, y, rr in inner:
        d.circle(x, y, rr)
    # K's own copy, straddling its edge: neither in nor out
    kx, ky, kr = cx + r, cy, 24
    d.circle(kx, ky, kr)
    d.group('mid')
    # members: men as dots in the first class, and a few in the others
    pts = []
    for i in range(7):
        a = 2 * math.pi * i / 7 + 0.3
        pts.append((112 + 16 * math.cos(a), 112 + 16 * math.sin(a)))
    pts += [(186, 100), (196, 110), (122, 192), (134, 202), (128, 186)]
    for x, y in pts:
        d.circle(x, y, 1.6)
    # the copy's own miniature classes, a scale drawing of K inside K
    s = kr / r
    for x, y, rr in inner:
        d.circle(kx + (x - cx) * s, ky + (y - cy) * s, rr * s)
    d.group('mid')
    # the loop: if K is in K, it is not; if it is not, it is
    bx, t, b = 330, 92, 208
    d.line((bx - 32, t - 12), (bx + 32, t - 12), (bx + 32, t + 12), (bx - 32, t + 12), closed=True)
    d.line((bx - 32, b - 12), (bx + 32, b - 12), (bx + 32, b + 12), (bx - 32, b + 12), closed=True)
    d.arc(bx, (t + b) / 2, 40, -72, 72, n=24, ry=(b - t) / 2 - 12)
    d.arc(bx, (t + b) / 2, 40, 108, 252, n=24, ry=(b - t) / 2 - 12)
    ya = (t + b) / 2
    d.lines([[(bx + 34, ya - 6), (bx + 40, ya), (bx + 46, ya - 6)],
             [(bx - 46, ya + 6), (bx - 40, ya), (bx - 34, ya + 6)]])
    d.group('mid')
    d.text(112, 76, 'MEN', size=7)
    d.text(kx + 4, ky + kr + 16, 'K ?', size=8)
    d.text(cx, cy + r + 26, 'K = { x : x ∉ x }', size=9)
    d.text(bx, t + 3, 'K ∈ K')
    d.text(bx, b + 3, 'K ∉ K')
    return d


PLATES = {
    'boole': boole,
    'cantor': cantor,
    'frege-russell': frege_russell,
}
