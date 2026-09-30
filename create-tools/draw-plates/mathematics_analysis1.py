"""Plates for the mathematics subject's Analysis segment, part one (sprint 024):
complex numbers, Fourier series and the rigour of analysis."""
import math
from plates import D


def complex_numbers():
    """Multiplication by i as a quarter turn: 3 + 2i turned four times about 0."""
    d = D()
    ox, oy, s = 200, 150, 30              # the origin, and 30 units to 1
    z = (3, 2)
    pts = []
    w = z
    for _ in range(4):
        pts.append(w)
        w = (-w[1], w[0])                 # i(a + bi) = -b + ai
    P = lambda p: (ox + s * p[0], oy - s * p[1])
    r = math.hypot(*z) * s
    d.group('thin')
    # the axes, a unit grid of ticks, the unit circle and the circle through the four points
    d.line((ox - 170, oy), (ox + 170, oy))
    d.line((ox, oy - 140), (ox, oy + 140))
    ticks = []
    for k in range(-5, 6):
        if k:
            ticks.append([(ox + k * s, oy - 3), (ox + k * s, oy + 3)])
        if k and abs(k) <= 4:
            ticks.append([(ox - 3, oy - k * s), (ox + 3, oy - k * s)])
    d.lines(ticks)
    d.circle(ox, oy, s)
    d.circle(ox, oy, r)
    # the coordinates of the first point, dropped to the axes
    x1, y1 = P(z)
    d.lines([[(x1, y1), (x1, oy)], [(x1, y1), (ox, y1)]])
    d.group('mid')
    # the four radii
    d.lines([[(ox, oy), P(p)] for p in pts])
    d.group()
    # the square the four points make: each is the last turned a quarter
    d.line(*[P(p) for p in pts], closed=True)
    d.group('mid')
    # the quarter-turn arcs, each with an arrowhead, and right-angle marks at the origin
    a0 = math.degrees(math.atan2(z[1], z[0]))
    ra = 0.62 * r
    for k in range(4):
        start, end = a0 + 90 * k + 8, a0 + 90 * (k + 1) - 8
        d.arc(ox, oy, ra, -start, -end, n=30)
        t = math.radians(end)
        ex, ey = ox + ra * math.cos(t), oy - ra * math.sin(t)
        tx, ty = -math.sin(t), -math.cos(t)       # tangent, in screen coordinates, direction of travel
        nx, ny = math.cos(t), -math.sin(t)
        d.line((ex - 6 * tx + 3 * nx, ey - 6 * ty + 3 * ny), (ex, ey), (ex - 6 * tx - 3 * nx, ey - 6 * ty - 3 * ny))
    for k in range(4):
        t1, t2 = math.radians(a0 + 90 * k), math.radians(a0 + 90 * (k + 1))
        m = 12
        p1 = (ox + m * math.cos(t1), oy - m * math.sin(t1))
        p2 = (ox + m * math.cos(t2), oy - m * math.sin(t2))
        c = (p1[0] + p2[0] - ox, p1[1] + p2[1] - oy)
        d.line(p1, c, p2)
    d.group('mid')
    names = ['3+2i', '-2+3i', '-3-2i', '2-3i']
    for p, n in zip(pts, names):
        x, y = P(p)
        ux, uy = (x - ox) / r, (y - oy) / r
        d.text(x + 18 * ux, y + 18 * uy + 3, n.replace('-', '−'))
    d.text(ox + s + 6, oy + 13, '1', size=7)
    d.text(ox - 7, oy - s - 4, 'i', size=7)
    d.text(ox - s - 7, oy + 13, '−1', size=7)
    d.text(ox + 8, oy + s + 12, '−i', size=7)
    d.text(ox + 172, oy - 6, 'RE', size=7, anchor='end')
    d.text(ox + 6, oy - 132, 'IM', size=7, anchor='start')
    d.text(ox + ra * 0.72 * math.cos(math.radians(a0 + 45)) + 2,
           oy - ra * 0.72 * math.sin(math.radians(a0 + 45)) + 3, '×i', size=8)
    return d


def fourier():
    """Fourier's own series for his square wave (Théorie analytique, art. 177):
    π/4 = cos x − cos 3x/3 + cos 5x/5 − …, its first terms, and their sums."""
    d = D()
    x0, x1 = 30, 370                       # x from −π to 2π across the plate
    X = lambda x: x0 + (x + math.pi) / (3 * math.pi) * (x1 - x0)
    top, low = 95, 235                     # the axes of the two panels
    ky, kl = 62, 30                        # vertical scales
    def partial(x, n):
        return sum((-1) ** k * math.cos((2 * k + 1) * x) / (2 * k + 1) for k in range(n))
    xs = [-math.pi + 3 * math.pi * i / 300 for i in range(301)]
    q = math.pi / 4
    d.group('thin')
    d.line((x0, top), (x1, top))
    d.line((x0, low), (x1, low))
    # graph-paper verticals at every half π, the level ±π/4, and the jumps' projection lines
    grid = []
    for k in range(-2, 5):
        x = X(k * math.pi / 2)
        grid.append([(x, top - ky * 1.2), (x, top + ky * 1.2)])
        grid.append([(x, low - kl * 1.4), (x, low + kl * 1.4)])
    grid.append([(x0, top - ky * q), (x1, top - ky * q)])
    grid.append([(x0, top + ky * q), (x1, top + ky * q)])
    d.lines(grid)
    d.group('mid')
    # the limit Fourier describes: straight lines at ±π/4 joined by perpendiculars
    segs = []
    for k in range(-2, 5):
        a, b = k * math.pi / 2, (k + 1) * math.pi / 2
        if b <= -math.pi or a >= 2 * math.pi:
            continue
        # sign of the limit between a and b: + on (−π/2, π/2) mod 2π
        mid = (a + b) / 2
        sign = 1 if math.cos(mid) > 0 else -1
        segs.append([(X(max(a, -math.pi)), top - sign * ky * q), (X(min(b, 2 * math.pi)), top - sign * ky * q)])
    for k in (-1, 1, 3):
        x = X(k * math.pi / 2)
        segs.append([(x, top - ky * q), (x, top + ky * q)])
    d.lines(segs)
    # the three waves taken separately, in the lower panel
    for n in range(3):
        c = (-1) ** n / (2 * n + 1)
        d.line(*[(X(x), low - kl * c * math.cos((2 * n + 1) * x) / (1 / 1)) for x in xs])
    d.group()
    # their sum, three terms; and eleven terms, overshooting at each jump
    d.line(*[(X(x), top - ky * partial(x, 3)) for x in xs])
    xs2 = [-math.pi + 3 * math.pi * i / 900 for i in range(901)]
    d.line(*[(X(x), top - ky * partial(x, 11)) for x in xs2])
    d.group('mid')
    for k, lab in [(-2, '−π'), (0, '0'), (2, 'π'), (4, '2π')]:
        d.text(X(k * math.pi / 2), top + ky * 1.2 + 11, lab, size=7)
    d.text(X(-math.pi) + 4, top - ky * q - 5, 'π/4', size=7, anchor='start')
    d.text(x1, top - ky * 1.2 + 2, '3 AND 11 TERMS', size=7, anchor='end')
    d.text(x1, low - kl * 1.4 + 2, 'cos x   −cos 3x/3   cos 5x/5', size=7, anchor='end')
    return d


def weierstrass(x, n, a=0.5, b=13):
    """The first n terms of the series. The whole plate can show three (the third is
    169 waves across it); the enlargement, a thirteenth of the width, shows four."""
    return sum(a ** k * math.cos(b ** k * math.pi * x) for k in range(n))


def rigour():
    """Weierstrass's function (1872) with a = 1/2, b = 13 (ab > 1 + 3π/2, his condition),
    and a thirteenfold enlargement of a thirteenth of it, as rough as the whole."""
    d = D()
    ux0, ux1, uy, us = 40, 360, 80, 30
    lx0, lx1, ly = 40, 360, 222
    c, h = 0.3, 1 / 13
    N = 1200
    up = [(-1 + 2 * i / N) for i in range(N + 1)]
    lo = [(c - h + 2 * h * i / N) for i in range(N + 1)]
    UX = lambda x: ux0 + (x + 1) / 2 * (ux1 - ux0)
    LX = lambda x: lx0 + (x - (c - h)) / (2 * h) * (lx1 - lx0)
    wl = [weierstrass(x, 4) for x in lo]
    lo_min, lo_max = min(wl), max(wl)
    mid = (lo_min + lo_max) / 2
    ls = 54 / ((lo_max - lo_min) / 2)
    d.group('thin')
    d.line((ux0, uy), (ux1, uy))
    d.line((lx0, ly - ls * (0 - mid)), (lx1, ly - ls * (0 - mid)))
    # the window, and the lines that carry it down to the enlargement
    bx0, bx1 = UX(c - h), UX(c + h)
    by0, by1 = uy - us * lo_max - 4, uy - us * lo_min + 4
    d.line((bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1), closed=True)
    d.line((bx0, by1), (lx0, ly - 60))
    d.line((bx1, by1), (lx1, ly - 60))
    d.line((lx0, ly - 60), (lx1, ly - 60), (lx1, ly + 60), (lx0, ly + 60), closed=True)
    d.lines([[(UX(x), uy - 3), (UX(x), uy + 3)] for x in (-1, -0.5, 0, 0.5, 1)])
    d.group()
    d.line(*[(UX(x), uy - us * weierstrass(x, 3)) for x in up])
    d.group()
    d.line(*[(LX(x), ly - ls * (w - mid)) for x, w in zip(lo, wl)])
    d.group('mid')
    d.text(UX(-1), uy - 50, '−1', size=7)
    d.text(UX(1), uy - 50, '1', size=7)
    d.text(lx1, ly + 74, '×13', size=7, anchor='end')
    d.text(lx0, 16, 'W(x) = Σ (1/2)ⁿ cos(13ⁿπx)', size=8, anchor='start')
    return d


PLATES = {
    'complex-numbers': complex_numbers,
    'fourier': fourier,
    'rigour': rigour,
}
