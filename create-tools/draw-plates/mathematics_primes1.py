"""Plates for the mathematics subject's primes trail, part 1 (sprint 024):
the sieve of Eratosthenes, Gauss's seventeen-gon, and the zeta function on
Riemann's critical line."""
import cmath, math
from plates import D


def sieve_of_eratosthenes():
    """The numbers 1 to 100 in a ten-by-ten grid. Each prime up to 7 strikes
    its multiples from its own square on, with a stroke of its own slant;
    what no stroke touches is circled: the 25 primes below 100."""
    d = D()
    c, x0, y0 = 24, 72, 30
    strokes = {2: (-1, 1), 3: (1, 1), 5: (1, 0), 7: (0, 1)}  # a stroke's direction per prime

    def centre(n):
        i = n - 1
        return x0 + (i % 10 + 0.5) * c, y0 + (i // 10 + 0.5) * c

    struck = {}
    for p in strokes:
        for m in range(p * p, 101, p):
            struck.setdefault(m, []).append(p)
    primes = [n for n in range(2, 101) if n not in struck]
    d.group('thin')
    d.lines([[(x0 + i * c, y0), (x0 + i * c, y0 + 10 * c)] for i in range(11)] +
            [[(x0, y0 + i * c), (x0 + 10 * c, y0 + i * c)] for i in range(11)])
    # the squares each prime starts from, marked in their cells' corners
    for p in strokes:
        x, y = centre(p * p)
        d.line((x - c / 2 + 2, y - c / 2 + 7), (x - c / 2 + 2, y - c / 2 + 2), (x - c / 2 + 7, y - c / 2 + 2))
    d.group('mid')
    for p, (ux, uy) in strokes.items():
        k = 7.5 / math.hypot(ux, uy)
        segs = []
        for m, by in struck.items():
            if p in by:
                x, y = centre(m)
                y -= 2.5
                segs.append([(x - ux * k, y - uy * k), (x + ux * k, y + uy * k)])
        d.lines(segs)
    d.group()
    for n in primes:
        x, y = centre(n)
        d.circle(x, y - 2.5, 8.5)
    d.group('mid')
    # the key: each prime's stroke
    kx, ky = 345, 92
    for j, (p, (ux, uy)) in enumerate(strokes.items()):
        k = 6 / math.hypot(ux, uy)
        y = ky + j * 30
        d.line((kx - ux * k, y - uy * k), (kx + ux * k, y + uy * k))
    d.group('mid')
    for n in range(1, 101):
        x, y = centre(n)
        d.text(x, y, str(n), size=7)
    for j, p in enumerate(strokes):
        d.text(kx + 12, ky + j * 30 + 3, str(p), anchor='start')
        d.text(kx - 2, ky + j * 30 + 16, f'FROM {p * p}', size=6)
    d.text(kx + 6, ky - 22, 'STRIKE', size=7)
    return d


def disquisitiones():
    """Richmond's construction of the regular seventeen-gon (1893), on
    Gauss's result of 1796. With OA, OB perpendicular radii: OI a quarter of
    OB; angle OIE a quarter of OIA; F on AO produced with EIF = 45 degrees;
    the circle on AF cuts OB at K; the circle about E through K cuts the
    diameter at N3 and N5, and the ordinates there meet the circle at the
    third and fifth vertices."""
    d = D()
    ox, oy, r = 200, 152, 128
    P = lambda x, y: (ox + r * x, oy - r * y)       # unit coordinates, y up
    iy = 0.25
    a_oia = math.atan2(1, iy)                        # angle OIA, at I between IO and IA
    a_oie = a_oia / 4
    ex = iy * math.tan(a_oie)
    fx = -iy * math.tan(math.pi / 4 - a_oie)
    mx, mr = (1 + fx) / 2, (1 - fx) / 2              # the circle on AF
    ky = math.sqrt(mr * mr - mx * mx)
    er = math.hypot(ex, ky)                          # the circle about E through K
    n3, n5 = ex + er, ex - er
    assert abs(n3 - math.cos(3 * 2 * math.pi / 17)) < 1e-9
    assert abs(n5 - math.cos(5 * 2 * math.pi / 17)) < 1e-9
    verts = [P(math.cos(2 * math.pi * k / 17), math.sin(2 * math.pi * k / 17)) for k in range(17)]
    d.group('thin')
    d.circle(ox, oy, r)
    d.line(P(-1.08, 0), P(1.08, 0))
    d.line(P(0, -1.08), P(0, 1.08))
    d.line(P(0, iy), P(1, 0))                         # IA
    d.line(P(0, iy), P(iy * math.tan(a_oia / 2), 0))  # the bisector, on the way to a quarter
    d.line(P(0, iy), P(ex, 0))                        # IE
    d.line(P(0, iy), P(fx, 0))                        # IF
    d.circle(*P(mx, 0), mr * r)
    d.circle(*P(ex, 0), er * r)
    d.group()
    d.line(*verts, closed=True)
    d.group('mid')
    d.line(P(n3, 0), P(n3, math.sin(3 * 2 * math.pi / 17)))
    d.line(P(n5, 0), P(n5, math.sin(5 * 2 * math.pi / 17)))
    for x, y in [(0, 0), (0, iy), (ex, 0), (fx, 0), (0, ky), (n3, 0), (n5, 0), (1, 0), (0, 1)]:
        d.circle(*P(x, y), 1.8)
    d.circle(*verts[3], 3.2)
    d.circle(*verts[5], 3.2)
    d.group('mid')
    for (x, y), s, dx, dy in [((0, 0), 'O', -8, 12), ((0, iy), 'I', -8, -3), ((ex, 0), 'E', 3, 12),
                              ((fx, 0), 'F', -6, 12), ((0, ky), 'K', -9, -3), ((n3, 0), 'N3', 5, 12),
                              ((n5, 0), 'N5', -7, 12), ((1, 0), 'A', 12, 4), ((0, 1), 'B', 9, -6)]:
        px, py = P(x, y)
        d.text(px + dx, py + dy, s, size=8)
    d.text(verts[3][0] + 10, verts[3][1] - 6, 'P3', size=8)
    d.text(verts[5][0] - 12, verts[5][1] - 6, 'P5', size=8)
    d.text(ox + 150, 286, '17 SIDES', size=7)
    return d


BERNOULLI = [1 / 6, -1 / 30, 1 / 42, -1 / 30, 5 / 66, -691 / 2730, 7 / 6, -3617 / 510]


def zeta(s, n=30):
    """The Riemann zeta function by Euler-Maclaurin summation: good to many
    places for 0 < Re s < 1 and |Im s| up to about 60."""
    total = sum(k ** -s for k in range(1, n))
    total += n ** (1 - s) / (s - 1) + 0.5 * n ** -s
    rising, fact = s, 2.0
    for j, b in enumerate(BERNOULLI, start=1):
        total += b / fact * rising * n ** (-s - 2 * j + 1)
        rising *= (s + 2 * j - 1) * (s + 2 * j)
        fact *= (2 * j + 1) * (2 * j + 2)
    return total


def zeros(tmax):
    """The heights t of the zeros of zeta(1/2 + it) up to tmax, found as the
    minima of |zeta| and refined by golden-section search."""
    f = lambda t: abs(zeta(complex(0.5, t)))
    ts = [i * 0.05 for i in range(1, int(tmax / 0.05))]
    found = []
    for a, b, c in zip(ts, ts[1:], ts[2:]):
        if f(b) < f(a) and f(b) < f(c) and f(b) < 0.2:
            lo, hi = a, c
            for _ in range(60):
                m1, m2 = hi - (hi - lo) / 1.618, lo + (hi - lo) / 1.618
                if f(m1) < f(m2):
                    hi = m2
                else:
                    lo = m1
            found.append((lo + hi) / 2)
    return found


def riemann_hypothesis():
    """The critical strip, 0 < Re s < 1, with the line Re s = 1/2 and the first
    ten zeros on it; beside it, sharing the vertical axis of height t,
    |zeta(1/2 + it)| computed and plotted, touching zero at each of them."""
    d = D()
    tmax, y0, y1 = 52, 276, 24
    Y = lambda t: y0 - (y0 - y1) * t / tmax
    sx0, sx1 = 40, 100                                   # the strip, Re s from 0 to 1
    gx, gw, vmax = 150, 230, 4.0                          # the plot of |zeta|
    X = lambda v: gx + gw * min(v, vmax) / vmax
    zs = zeros(tmax)
    d.group('thin')
    d.line((sx0, y0), (sx0, y1))
    d.line((sx1, y0), (sx1, y1))
    d.line((sx0 - 10, y0), (sx1 + 10, y0))
    d.line((gx, y0), (gx + gw + 6, y0))
    d.line((gx, y0), (gx, y1 - 6))
    for v in (1, 2, 3, 4):
        d.line((X(v), y0), (X(v), y0 + 4))
    for t in range(10, tmax, 10):
        d.line((gx - 4, Y(t)), (gx, Y(t)))
    for t in zs:                                          # each zero carried across to the plot
        d.line(((sx0 + sx1) / 2 + 4, Y(t)), (gx, Y(t)))
    d.group()
    d.line(((sx0 + sx1) / 2, y0), ((sx0 + sx1) / 2, y1))
    pts = [(X(abs(zeta(complex(0.5, i * tmax / 520)))), Y(i * tmax / 520)) for i in range(521)]
    d.line(*pts)
    d.group('mid')
    for t in zs:
        d.circle((sx0 + sx1) / 2, Y(t), 2.4)
    d.group('mid')
    d.text(sx0, y0 + 12, '0', size=7)
    d.text((sx0 + sx1) / 2, y0 + 12, '1/2', size=7)
    d.text(sx1, y0 + 12, '1', size=7)
    d.text((sx0 + sx1) / 2, y1 - 8, 'Re s', size=7)
    for v in (1, 2, 3, 4):
        d.text(X(v), y0 + 13, str(v), size=7)
    for t in range(10, tmax, 10):
        d.text(gx - 7, Y(t) + 3, str(t), size=7, anchor='end')
    d.text(gx + gw, y0 - 8, '|ζ(1/2 + it)|', size=7, anchor='end')
    d.text(gx + 4, y1 - 8, 't', size=8, anchor='start')
    for t in zs[:3]:
        d.text(sx1 + 4, Y(t) - 3, f'{t:.2f}', size=6, anchor='start')
    return d


PLATES = {
    'sieve-of-eratosthenes': sieve_of_eratosthenes,
    'disquisitiones': disquisitiones,
    'riemann-hypothesis': riemann_hypothesis,
}

if __name__ == '__main__':
    print([round(t, 6) for t in zeros(52)])
    print(zeta(2), math.pi ** 2 / 6, zeta(complex(0.5, 14.134725141734693)))
