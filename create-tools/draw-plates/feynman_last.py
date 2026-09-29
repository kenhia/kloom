"""feynman plates, segments "The last years" and "Afterlife" (sprint 014). See feynman.py."""
import math
import random

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _wavy(pts, amp=3.2, waves=None, per=9.0):
    """A photon line: a sine wiggle laid along the polyline `pts`, `waves` whole periods (or one per `per` px)."""
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(seg)
    n = waves or max(2, round(total / per))
    out = []
    steps = n * 16
    for s in range(steps + 1):
        u = total * s / steps
        i, acc = 0, 0.0
        while i < len(seg) - 1 and acc + seg[i] < u:
            acc += seg[i]
            i += 1
        t = (u - acc) / seg[i] if seg[i] else 0
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        dx, dy = (x1 - x0) / seg[i], (y1 - y0) / seg[i]
        off = amp * math.sin(2 * math.pi * n * s / steps)
        out.append((x0 + (x1 - x0) * t - dy * off, y0 + (y1 - y0) * t + dx * off))
    return out


def last_days():
    """The last thing on his list: a ring of twelve spins with one flipped, the Heisenberg chain the Bethe ansatz solves, and the wave the flip travels as."""
    d = D()
    cx, cy, r, N = 118, 150, 84, 12
    flipped = 3
    site = lambda n: (cx + r * math.cos(2 * math.pi * n / N - math.pi / 2), cy + r * math.sin(2 * math.pi * n / N - math.pi / 2))
    # construction: the ring's centre, its radii to each site, and the plot's grid
    d.group('thin')
    d.lines([[(cx, cy), site(n)] for n in range(N)])
    d.circle(cx, cy, r + 26)
    d.lines([[(cx - 6, cy), (cx + 6, cy)], [(cx, cy - 6), (cx, cy + 6)]])
    px, py, pw, ph = 244, 150, 138, 56  # the plot: site n across, amplitude up and down
    d.lines([[(px + pw * n / N, py - ph), (px + pw * n / N, py + ph)] for n in range(N + 1)])
    d.lines([[(px, py - ph), (px + pw, py - ph)], [(px, py + ph), (px + pw, py + ph)]])
    # the chain: the ring that joins neighbours, and the spins, each an arrow, all up but one
    d.group()
    d.circle(cx, cy, r)
    for n in range(N):
        x, y = site(n)
        up = n != flipped
        y0, y1 = (y + 11, y - 11) if up else (y - 11, y + 11)
        d.line((x, y0), (x, y1))
        _arrow(d, x, y1, -math.pi / 2 if up else math.pi / 2, 5)
    # detail: the flipped spin ringed; the exchange coupling between two neighbours
    d.group('mid')
    d.circle(*site(flipped), 17)
    a, b = site(7), site(8)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    nx, ny = (mx - cx) / r, (my - cy) / r
    d.line((mx + nx * 14, my + ny * 14), (mx + nx * 30, my + ny * 30))
    # the plot: the flip is not at one site but spread round the ring as a wave, e^{ikn} with k = 2π·2/12
    d.group()
    d.line((px, py), (px + pw + 8, py))
    _arrow(d, px + pw + 8, py, 0, 4)
    k = 2 * math.pi * 2 / N
    d.line(*[(px + pw * t / 120, py - ph * 0.8 * math.cos(k * N * t / 120)) for t in range(121)])
    d.group('mid')
    for n in range(N + 1):
        d.circle(px + pw * n / N, py - ph * 0.8 * math.cos(k * n), 2.2)
    # labels
    d.group()
    d.text(200, 26, 'TO LEARN: BETHE ANSATZ', size=9)
    d.text(cx, cy + r + 44, 'N = 12 SPINS · ONE FLIPPED', size=7)
    d.text(mx + nx * 30 - 4, my + ny * 30 + 12, 'J', size=8, anchor='end')
    d.text(px + pw / 2, py - ph - 10, 'ψ(n) = e^(ikn)', size=8)
    d.text(px + pw / 2, py + ph + 16, 'k = 2πm/N · m = 2', size=7)
    d.text(px + pw + 10, py + 12, 'n', size=8, anchor='start')
    return d


def the_legend():
    """How a saying finds its author: three attributions traced along the years, each arriving after 1988."""
    d = D()
    x0, x1, y0, y1 = 34, 380, 1950, 2020
    X = lambda yr: x0 + (x1 - x0) * (yr - y0) / (y1 - y0)
    axis = 262
    rows = {'orn': 74, 'shut': 142, 'tech': 210}
    # construction: the years, a tick each five, a line each decade, and his death
    d.group('thin')
    d.lines([[(X(yr), 44), (X(yr), axis)] for yr in range(1950, 2021, 10)])
    d.lines([[(X(yr), axis), (X(yr), axis + 4)] for yr in range(1950, 2021, 5)])
    d.lines([[(x0, y), (x1, y)] for y in rows.values()])
    # the axis and the year he died, at full weight
    d.group()
    d.line((x0, axis), (x1 + 6, axis))
    _arrow(d, x1 + 6, axis, 0, 4)
    d.line((X(1988), 36), (X(1988), axis))
    # the three stemmata: who said it first, who passed it on, where his name was attached
    rnd = random.Random(1988)
    d.group('mid')
    chains = [
        ('orn', [1955, 1987, 1998], 1999),   # Newman; Weinberg, anonymous; Kitcher, 'perhaps apocryphal'
        ('shut', [1989, 2004], 1995),        # Mermin coins it; attributed to Feynman; Mermin traces it in 2004
        ('tech', [2011], 2012),              # Young names the technique
    ]
    fans = []
    for key, years, fan_from in chains:
        y = rows[key]
        for a, b in zip(years, years[1:]):
            d.line((X(a) + 4, y), (X(b) - 4, y))
            _arrow(d, X(b) - 4, y, 0, 4)
        for yr in years:
            d.circle(X(yr), y, 4)
        # the fan: the saying copied onward, each copy carrying his name
        src = (X(fan_from), y)
        for i in range(6):
            yr = fan_from + 3 + rnd.uniform(0, 2020 - fan_from - 5)
            dy = 4 + i * 4.5 + rnd.uniform(-1.5, 1.5)  # downward, clear of the names above the row
            fans.append((src, (X(yr), y + dy)))
    d.group('thin')
    d.lines([[a, b] for a, b in fans])
    d.group('mid')
    for _, (x, y) in fans:
        d.circle(x, y, 1.6)
    # labels
    d.group()
    d.text(X(1988) + 4, 30, 'D. 1988', size=7, anchor='start')
    for yr in range(1950, 2021, 10):
        d.text(X(yr), axis + 14, str(yr), size=7)
    d.text(X(1955), rows['orn'] - 10, 'NEWMAN', size=7)
    d.text(X(1987) - 2, rows['orn'] - 10, 'WEINBERG', size=7, anchor='end')
    d.text(X(1998) + 2, rows['orn'] - 12, 'KITCHER', size=7, anchor='start')
    d.text(x0, rows['orn'] + 22, '“ORNITHOLOGY … BIRDS”', size=7, anchor='start')
    d.text(X(1989) - 6, rows['shut'] - 10, 'MERMIN', size=7, anchor='end')
    d.text(X(2004) + 6, rows['shut'] - 10, 'MERMIN', size=7, anchor='start')
    d.text(x0, rows['shut'] + 22, '“SHUT UP AND CALCULATE”', size=7, anchor='start')
    d.text(X(2011) - 6, rows['tech'] - 10, 'YOUNG', size=7, anchor='end')
    d.text(x0, rows['tech'] + 22, '“THE FEYNMAN TECHNIQUE”', size=7, anchor='start')
    return d


def legacy():
    """Two tools still in daily use: the path integral summed on a lattice of spacetime points, and the one-loop diagram for the electron's magnetism."""
    d = D()
    # left panel: a spacetime lattice, time up, space across
    lx, ly, cols, rows_, step = 30, 50, 8, 9, 22
    P = lambda i, j: (lx + i * step, ly + (rows_ - j) * step)
    rnd = random.Random(1948)
    d.group('thin')
    d.lines([[P(i, 0), P(i, rows_)] for i in range(cols + 1)])
    d.lines([[P(0, j), P(cols, j)] for j in range(rows_ + 1)])
    # sampled paths: one lattice point on every time slice, from A at the bottom to B at the top
    a_i, b_i = 3, 5
    d.group('mid')
    for _ in range(5):
        path = [a_i]
        for j in range(1, rows_ + 1):
            left = rows_ - j  # steps still to take: stay within reach of B
            ok = [i for i in (path[-1] - 1, path[-1], path[-1] + 1) if 0 <= i <= cols and abs(i - b_i) <= left]
            path.append(rnd.choice(ok))
        d.line(*[P(i, j) for j, i in enumerate(path)])
    d.group()
    d.line(*[P(a_i + (b_i - a_i) * j / rows_, j) for j in range(rows_ + 1)])
    d.circle(*P(a_i, 0), 3.5)
    d.circle(*P(b_i, rows_), 3.5)
    # right panel: the vertex correction, electron in and out, a photon absorbed, one virtual photon across
    vx, vy = 296, 104
    ein, eout = (232, 250), (360, 250)
    d.group('thin')
    d.lines([[(236, vy), (384, vy)], [(vx, 44), (vx, 262)]])
    d.group()
    d.line(ein, (vx, vy))
    d.line((vx, vy), eout)
    for (xa, ya), (xb, yb) in ((ein, (vx, vy)), ((vx, vy), eout)):
        mx, my = (xa + xb) / 2, (ya + yb) / 2
        _arrow(d, mx, my, math.atan2(yb - ya, xb - xa), 5)
    d.line(*_wavy([(vx, 40), (vx, vy)], waves=4))
    # the virtual photon, emitted on the way in and reabsorbed on the way out
    t = 0.62
    pa = (ein[0] + (vx - ein[0]) * t, ein[1] + (vy - ein[1]) * t)
    pb = (eout[0] + (vx - eout[0]) * t, eout[1] + (vy - eout[1]) * t)
    arc = [(pa[0] + (pb[0] - pa[0]) * s / 24, pa[1] + (pb[1] - pa[1]) * s / 24 + 22 * math.sin(math.pi * s / 24))
           for s in range(25)]
    d.group('mid')
    d.line(*_wavy(arc, amp=2.6, waves=6))
    d.circle(*pa, 2.2)
    d.circle(*pb, 2.2)
    d.circle(vx, vy, 2.6)
    # labels
    d.group()
    d.text(lx + cols * step / 2, 34, 'Σ OVER PATHS', size=8)
    d.text(P(a_i, 0)[0] - 8, P(a_i, 0)[1] + 4, 'A', size=8, anchor='end')
    d.text(P(b_i, rows_)[0] + 8, P(b_i, rows_)[1] + 4, 'B', size=8, anchor='start')
    d.text(lx - 10, P(0, rows_ / 2)[1], 't', size=8, anchor='end')
    d.text(lx + cols * step / 2, 266, 'SPACE · A LATTICE', size=7)
    d.text(vx + 8, 48, 'γ', size=9, anchor='start')
    d.text(ein[0] - 4, ein[1] + 12, 'e', size=9)
    d.text(eout[0] + 4, eout[1] + 12, 'e', size=9)
    d.text(300, 280, 'a = α/2π + …', size=8)
    return d


PLATES = {
    'last-days': last_days,
    'the-legend': the_legend,
    'legacy': legacy,
}
