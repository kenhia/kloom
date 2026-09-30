"""Plates for the mathematics subject's Algebra segment, part one (sprint 024):
the quintic, groups and Emmy Noether."""
import math
from plates import D


def quintic():
    d = D()
    # left: the roots of x^4 - 2 in the complex plane, a = 2^(1/4)
    cx, cy, s = 110, 145, 62
    a = 2 ** 0.25
    r = a * s
    roots = [(cx + r, cy), (cx, cy - r), (cx - r, cy), (cx, cy + r)]   # a, ia, -a, -ia
    # right: y = x^5 - x - 1, whose one real root is not a radical expression
    x0, x1 = -1.3, 1.45
    gx0, gx1 = 232, 384
    kx = (gx1 - gx0) / (x1 - x0)
    oy, ky = 150, 26
    ox = gx0 - x0 * kx
    f = lambda x: x ** 5 - x - 1
    root = 1.1673039782614187
    d.group('thin')
    # axes of the complex plane, the circle of radius 2^(1/4), the two diagonal mirrors
    d.line((cx - 95, cy), (cx + 95, cy))
    d.line((cx, cy - 95), (cx, cy + 95))
    d.circle(cx, cy, r)
    e = 80 / math.sqrt(2)
    d.line((cx - e, cy + e), (cx + e, cy - e))
    d.line((cx - e, cy - e), (cx + e, cy + e))
    # the graph's axes, and the root dropped to the x-axis
    d.line((gx0 - 4, oy), (gx1 + 4, oy))
    d.line((ox, 40), (ox, 262))
    d.line((ox + root * kx, oy - 10), (ox + root * kx, oy + 10))
    d.group()
    d.line(*roots, closed=True)
    pts = []
    n = 160
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = f(x)
        if -4.4 <= y <= 4.3:
            pts.append((ox + x * kx, oy - y * ky))
    d.line(*pts)
    d.group('mid')
    # the quarter turn that carries a to ia, with its arrowhead
    rr = r + 14
    d.arc(cx, cy, rr, -8, -82, n=30)
    tip = (cx + rr * math.cos(math.radians(-82)), cy + rr * math.sin(math.radians(-82)))
    d.line((tip[0] + 6, tip[1] - 4), tip, (tip[0] + 5, tip[1] + 5))
    for (x, y) in roots:
        d.circle(x, y, 3)
    d.circle(ox + root * kx, oy, 3)
    d.group('mid')
    d.text(roots[0][0] + 8, roots[0][1] + 14, 'a', anchor='start')
    d.text(roots[1][0] - 8, roots[1][1] - 6, 'ia', anchor='end')
    d.text(roots[2][0] - 8, roots[2][1] + 14, '−a', anchor='end')
    d.text(roots[3][0] + 8, roots[3][1] + 12, '−ia', anchor='start')
    d.text(cx, 272, 'x⁴ − 2', size=8)
    d.text(ox + 36, 272, 'x⁵ − x − 1', size=8)
    d.text(ox + root * kx - 7, oy - 8, '1.1673', size=7, anchor='end')
    return d


def _tri_moves():
    """The six symmetries of an equilateral triangle, as maps of the plane (y up)."""
    def rot(k):
        t = math.radians(120 * k)
        return lambda p: (p[0] * math.cos(t) - p[1] * math.sin(t), p[0] * math.sin(t) + p[1] * math.cos(t))
    def flip(k):
        t = math.radians(90 + 120 * k)          # the mirror through corner k + 1
        c, s = math.cos(2 * t), math.sin(2 * t)
        return lambda p: (p[0] * c + p[1] * s, p[0] * s - p[1] * c)
    return [('e', rot(0)), ('r', rot(1)), ('r²', rot(2)), ('a', flip(0)), ('b', flip(1)), ('c', flip(2))]


def groups():
    d = D()
    cx, cy, R = 112, 150, 90
    corner = lambda k, R=R: (math.cos(math.radians(90 + 120 * k)), math.sin(math.radians(90 + 120 * k)))
    scr = lambda p, x, y, k: (x + k * p[0], y - k * p[1])
    flag = [(-0.05, 0.62), (-0.05, 0.3), (-0.3, 0.38)]       # an asymmetric mark near corner 1
    moves = _tri_moves()
    small = [(252, 92), (310, 92), (368, 92), (252, 200), (310, 200), (368, 200)]
    d.group('thin')
    d.circle(cx, cy, R)
    for k in range(3):
        c = corner(k)
        d.line(scr((c[0] * 1.12, c[1] * 1.12), cx, cy, R), scr((-c[0] * 0.62, -c[1] * 0.62), cx, cy, R))
    for x, y in small:
        d.circle(x, y, 24)
    d.group()
    d.line(*[scr(corner(k), cx, cy, R) for k in range(3)], closed=True)
    for (name, m), (x, y) in zip(moves, small):
        d.line(*[scr(corner(k), x, y, 24) for k in range(3)], closed=True)
    d.group('mid')
    d.line(*[scr(p, cx, cy, R) for p in flag])
    for (name, m), (x, y) in zip(moves, small):
        d.line(*[scr(m(p), x, y, 24) for p in flag])
    # the turn r, a third of the way round, with its arrowhead
    rr = R + 12
    pts = [(cx + rr * math.cos(math.radians(a)), cy - rr * math.sin(math.radians(a))) for a in range(100, 201, 4)]
    d.line(*pts)
    t = math.radians(200)
    tip = pts[-1]
    tx, ty = -math.sin(t), -math.cos(t)          # screen direction of travel
    nx, ny = -ty, tx
    d.line((tip[0] - 7 * tx + 4 * nx, tip[1] - 7 * ty + 4 * ny), tip, (tip[0] - 7 * tx - 4 * nx, tip[1] - 7 * ty - 4 * ny))
    d.group('mid')
    for k in range(3):
        x, y = scr(corner(k), cx, cy, R + 16)
        d.text(x, y + 3, str(k + 1), size=8)
    d.text(cx - 88, cy - 70, 'r', size=9)
    for (name, m), (x, y) in zip(moves, small):
        d.text(x, y + 40, name, size=8)
    return d


def noether():
    d = D()
    # Kepler's second law as rotational symmetry at work: an orbit of eccentricity 0.6,
    # marked at twelve equal intervals of time (Kepler's equation M = E - e sin E)
    e, A = 0.6, 150
    B = A * math.sqrt(1 - e * e)
    cx, cy = 215, 150
    fx, fy = cx + A * e, cy                      # the sun at the right-hand focus
    def pos(E):
        return cx + A * math.cos(E), cy - B * math.sin(E)
    def ecc(M):
        E = M
        for _ in range(60):
            E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        return E
    N = 12
    marks = [pos(ecc(2 * math.pi * k / N)) for k in range(N)]
    d.group('thin')
    # the sun's pull is the same in every direction: circles of equal pull about it
    for r in (22, 50, 92):
        d.circle(fx, fy, r)
    for r in (140, 190):
        t = math.degrees(math.asin(min(1, 128 / r)))
        d.arc(fx, fy, r, 180 - t, 180 + t, n=60)
    d.line((cx - A - 12, cy), (fx + 20, cy))
    d.line((cx, cy - B - 8), (cx, cy + B + 8))
    d.group()
    d.line(*[pos(2 * math.pi * i / 180) for i in range(180)], closed=True)
    d.circle(fx, fy, 5)
    d.group('mid')
    # the radius to every mark, and two equal-time sectors, one near and one far
    d.lines([[(fx, fy), m] for m in marks])
    for k in (0, 6):
        E0, E1 = ecc(2 * math.pi * k / N), ecc(2 * math.pi * (k + 1) / N)
        arc = [pos(E0 + (E1 - E0) * i / 20) for i in range(21)]
        d.line((fx, fy), *arc, (fx, fy))
    for (x, y) in marks:
        d.circle(x, y, 2.2)
    d.group('mid')
    d.text(fx + 2, fy + 20, 'SUN', size=7)
    d.text(cx - 40, 280, 'EQUAL TIMES · EQUAL AREAS', size=7)
    return d


PLATES = {
    'quintic': quintic,
    'groups': groups,
    'noether': noether,
}
