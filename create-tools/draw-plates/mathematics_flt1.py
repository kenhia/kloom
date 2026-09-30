"""Plates for the first half of the mathematics subject's Fermat's Last Theorem trail (sprint 024):
Fermat's margin, Euler's cubes and Sophie Germain."""
import math
from plates import D


def arrow_head(d, tip, frm, size=5):
    """Two short strokes at `tip`, pointing away from `frm`."""
    ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    pts = []
    for s in (-1, 1):
        a = ang + math.pi + s * 0.45
        pts.append([(tip[0] + size * math.cos(a), tip[1] + size * math.sin(a)), tip])
    d.lines(pts)


def fermats_margin():
    """Infinite descent, schematic: a right triangle whose area is assumed square
    yields a smaller one of the same kind, and that a smaller one, while the whole
    numbers below them have a floor at 1."""
    d = D()
    base = 246
    # four right triangles in the ratio 3 : 4 : 5, each about 0.56 of the one before
    scales = [30, 17, 9.5, 5.3]
    xs, x = [], 22
    for s in scales:
        xs.append(x)
        x += 3 * s + 26
    tri = [((x0, base), (x0 + 3 * s, base), (x0, base - 4 * s)) for x0, s in zip(xs, scales)]
    ladder_x, top, floor = 330, 40, base
    d.group('thin')
    d.line((14, base), (ladder_x - 18, base))
    # the ladder of whole numbers: one tick a unit, 1 at the floor
    step = (floor - top) / 20
    d.line((ladder_x, top - 6), (ladder_x, floor))
    d.lines([[(ladder_x - 4, floor - i * step), (ladder_x + 4, floor - i * step)] for i in range(1, 21)])
    # each triangle's hypotenuse carried across to the ladder, as its size
    for (a, b, c), s in zip(tri, scales):
        h = 5 * s / 150 * (floor - top)          # hypotenuse to the ladder's scale (not to size)
        d.line(c, (ladder_x - 8, floor - h))
    d.group()
    for a, b, c in tri:
        d.line(a, b, c, closed=True)
    d.line((ladder_x - 12, floor), (ladder_x + 30, floor))
    d.group('mid')
    # right-angle marks
    for (a, b, c), s in zip(tri, scales):
        m = min(7, s * 0.8)
        d.line((a[0] + m, a[1]), (a[0] + m, a[1] - m), (a[0], a[1] - m))
    # arcs from each triangle to the next: the descent
    for i in range(3):
        (a0, b0, c0), (a1, b1, c1) = tri[i], tri[i + 1]
        p0 = ((a0[0] + b0[0]) / 2 + 10, base - 4 * scales[i] * 0.45)
        p1 = (a1[0] + 1.5 * scales[i + 1], base - 4 * scales[i + 1] - 6)
        mx, my = (p0[0] + p1[0]) / 2, min(p0[1], p1[1]) - 24
        pts = [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * mx + t * t * p1[0],
                (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * my + t * t * p1[1]) for t in [k / 24 for k in range(25)]]
        d.line(*pts)
        arrow_head(d, pts[-1], pts[-3])
    # the chain of sizes falling down the ladder
    marks = [floor - 5 * s / 150 * (floor - top) for s in scales]
    for y0, y1 in zip(marks, marks[1:]):
        d.line((ladder_x + 10, y0), (ladder_x + 10, y1 + 3))
        arrow_head(d, (ladder_x + 10, y1 + 3), (ladder_x + 10, y0), 4)
    d.line((ladder_x + 10, marks[-1]), (ladder_x + 10, floor - 3))
    arrow_head(d, (ladder_x + 10, floor - 3), (ladder_x + 10, marks[-1]), 4)
    for y in marks:
        d.circle(ladder_x + 10, y, 2)
    d.group('mid')
    d.text(xs[0] + 12, base - 10, 'AREA = s²?', size=7, anchor='start')
    d.text(xs[0] + 45, base + 14, 'u', size=8)
    d.text(xs[0] - 8, base - 60, 'v', size=8)
    d.text(ladder_x - 8, floor + 14, '1', size=8)
    d.text(ladder_x + 16, top - 4, 'SIZE', size=7, anchor='start')
    d.text(ladder_x + 18, floor + 14, 'FLOOR', size=7, anchor='start')
    d.text(150, 280, 'EACH SOLUTION GIVES A SMALLER ONE', size=7)
    return d


def euler_cubes():
    """The numbers a + b√−3 as a lattice in the plane, and the six of them at
    distance 2 from 0: 4 = 2 × 2 = (1 + √−3)(1 − √−3)."""
    d = D()
    u = 32
    cx, cy = 168, 142
    r3 = math.sqrt(3)

    def pt(a, b):                       # a + b√−3
        return cx + a * u, cy - b * r3 * u

    d.group('thin')
    d.line((cx - 5 * u, cy), (cx + 5 * u, cy))
    d.line((cx, cy - 2.4 * r3 * u), (cx, cy + 2.4 * r3 * u))
    d.circle(cx, cy, 2 * u)
    # the Eisenstein integers that fill the holes: (a + ½) + (b + ½)√−3
    holes = []
    for a in range(-5, 5):
        for b in range(-3, 2):
            x, y = pt(a + 0.5, b + 0.5)
            if abs(x - cx) <= 4.6 * u and abs(y - cy) <= 2.3 * r3 * u:
                holes.append((x, y))
    for x, y in holes:
        d.circle(x, y, 1.6)
    d.group()
    # the lattice Z[√−3]
    for a in range(-4, 5):
        for b in range(-2, 3):
            x, y = pt(a, b)
            d.circle(x, y, 2.4)
    d.group('mid')
    # the numbers of norm 4, a² + 3b² = 4, and the rays to the three that matter
    six = [pt(2, 0), pt(-2, 0), pt(1, 1), pt(1, -1), pt(-1, 1), pt(-1, -1)]
    for x, y in six:
        d.circle(x, y, 5.5)
    d.lines([[(cx, cy), pt(2, 0)], [(cx, cy), pt(1, 1)], [(cx, cy), pt(1, -1)]])
    d.group('mid')
    x, y = pt(2, 0)
    d.text(x + 12, y + 14, '2', size=8)
    x, y = pt(1, 1)
    d.text(x + 10, y - 8, '1 + √−3', size=8, anchor='start')
    x, y = pt(1, -1)
    d.text(x + 10, y + 16, '1 − √−3', size=8, anchor='start')
    d.text(cx + 5 * u - 2, cy - 6, 'a', size=8, anchor='end')
    d.text(cx + 6, cy - 2.4 * r3 * u + 8, 'b√−3', size=8, anchor='start')
    d.text(200, 290, '4 = 2 × 2 = (1 + √−3)(1 − √−3)', size=8)
    return d


def sophie_germain():
    """Fifth powers modulo 11: every number not divisible by 11 lands on 1 or 10,
    two residues that are not neighbours, so 11 must divide x, y or z in any
    x⁵ + y⁵ = z⁵. Beside it, the chain 2, 5, 11, 23, 47, each twice the last plus one."""
    d = D()
    cx, cy, r = 138, 150, 98
    n = 11

    def at(k, rr=r):
        a = math.radians(-90 + 360 * k / n)
        return cx + rr * math.cos(a), cy + rr * math.sin(a)

    fifth = {k: pow(k, 5, n) for k in range(1, n)}
    d.group('thin')
    d.circle(cx, cy, r)
    d.lines([[(cx, cy), at(k, r - 6)] for k in range(n)])
    d.group()
    for k in range(n):
        x, y = at(k)
        d.circle(x, y, 7 if k in (1, 10) else 3.5)
    d.group('mid')
    # a chord from each k to k⁵ mod 11, bowed towards the centre, with an arrowhead
    for k, t in fifth.items():
        if k == t:
            continue
        p0, p1 = at(k, r - 5), at(t, r - 9)
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        mx, my = mx + (cx - mx) * 0.35, my + (cy - my) * 0.35
        pts = [((1 - s) ** 2 * p0[0] + 2 * (1 - s) * s * mx + s * s * p1[0],
                (1 - s) ** 2 * p0[1] + 2 * (1 - s) * s * my + s * s * p1[1]) for s in [i / 20 for i in range(21)]]
        d.line(*pts)
        arrow_head(d, pts[-1], pts[-3], 4)
    # the chain of Sophie Germain primes, each doubled and one added
    chain = [2, 5, 11, 23, 47]
    x0, ys = 330, [60 + 44 * i for i in range(5)]
    for y in ys:
        d.line((x0 - 16, y - 11), (x0 + 16, y - 11), (x0 + 16, y + 11), (x0 - 16, y + 11), closed=True)
    for y0, y1 in zip(ys, ys[1:]):
        d.line((x0, y0 + 12), (x0, y1 - 13))
        arrow_head(d, (x0, y1 - 13), (x0, y0 + 12), 4)
    d.group('mid')
    for k in range(n):
        x, y = at(k, r + 16)
        d.text(x, y + 3, str(k), size=8)
    for y, p in zip(ys, chain):
        d.text(x0, y + 3, str(p), size=9)
    d.text(x0 + 22, (ys[0] + ys[1]) / 2 + 3, '×2+1', size=7, anchor='start')
    d.text(cx, 290, 'k⁵ MOD 11', size=7)
    d.text(x0, 290, '2p + 1', size=7)
    return d


PLATES = {
    'fermats-margin': fermats_margin,
    'euler-cubes': euler_cubes,
    'sophie-germain': sophie_germain,
}
