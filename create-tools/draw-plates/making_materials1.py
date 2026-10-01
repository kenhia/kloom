"""Plates for How We Build's Materials science trail, first part (sprint 026):
Galileo's beams, Sorby's microscope, the iron-carbon diagram and duralumin."""
import math
import random
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _hatch(d, x0, y0, x1, y1, step=8, slope=1.0):
    """Short diagonal strokes along a vertical edge from (x0, y0) to (x0, y1), drawn to the side x1."""
    segs = []
    y = y0
    while y < y1:
        segs.append([(x0, y), (x1, y + (x0 - x1) * slope)])
        y += step
    d.lines(segs)


def galileo_beams():
    d = D()
    # the cantilever: a wall, a beam let into it, a weight hung at its end (Galileo's figure 17)
    wx, top, h, L = 40, 64, 24, 168
    bot = top + h
    ex = wx + L
    d.group('thin')
    _hatch(d, wx, 30, wx - 12, 176)
    d.line((wx, bot), (ex + 18, bot))                      # the line of the lower face, produced: the lever
    d.line((wx, top - 14), (wx, bot + 14))
    d.line((ex - 4, bot + 6), (ex - 4, 150))               # the line of the load
    # dimension: L from the wall's lower edge to the load
    d.line((wx, bot + 24), (ex - 4, bot + 24))
    d.lines([[(wx, bot + 20), (wx, bot + 28)], [(ex - 4, bot + 20), (ex - 4, bot + 28)]])
    d.group()
    d.line((wx, 30), (wx, 176))                            # the wall's face
    d.line((wx, top), (ex, top), (ex, bot), (wx, bot))      # the beam
    d.line((ex - 14, 150), (ex + 6, 150), (ex + 9, 172), (ex - 17, 172), closed=True)  # the weight
    d.group('mid')
    d.line((ex - 4, bot), (ex - 4, 150))                   # its cord
    d.circle(wx, bot, 2.5)                                 # the fulcrum Galileo chose: the lower edge
    # two ways the section resists, drawn at the wall: Galileo's even pull about the lower edge,
    # and the elastic one, a pull above and a push below a neutral axis at mid-depth
    sy0, sy1 = 204, 264                                    # the section's top and bottom
    gx, ex2 = 74, 196
    d.group('thin')
    d.line((ex2, (sy0 + sy1) / 2), (ex2 + 46, (sy0 + sy1) / 2))   # the neutral axis
    d.line((gx - 30, sy1), (gx + 8, sy1))
    d.group()
    d.line((gx, sy0), (gx, sy1))
    d.line((ex2, sy0), (ex2, sy1))
    d.group('mid')
    # Galileo: equal arrows, each fibre pulling its full strength
    d.line((gx, sy0), (gx - 30, sy0), (gx - 30, sy1), (gx, sy1))
    d.lines([[(gx, y), (gx - 26, y)] for y in range(sy0 + 6, sy1, 9)])
    d.lines([[(gx - 22, y - 3), (gx - 27, y), (gx - 22, y + 3)] for y in range(sy0 + 6, sy1, 9)])
    d.circle(gx, sy1, 2.5)                                 # turning about the lower edge
    # elastic: a triangle of pull above, of push below
    mid = (sy0 + sy1) / 2
    d.line((ex2, sy0), (ex2 - 30, sy0), (ex2 + 30, sy1), (ex2, sy1))
    arrows = []
    for y in range(sy0 + 5, sy1, 8):
        s = (mid - y) / (mid - sy0) * 30                   # length of the arrow at this depth
        if abs(s) > 4:
            arrows.append([(ex2, y), (ex2 - s, y)])
    d.lines(arrows)
    # the two planks in section, the same plank laid flat and stood on edge
    px, w, t = 320, 96, 24
    d.group('thin')
    d.line((px, 34), (px, 270))
    d.line((px - w / 2, 102), (px + w / 2, 102))           # depth of the flat plank
    d.line((px + 22, 150), (px + 22, 246))                 # depth of the plank on edge
    d.lines([[(px + 18, 150), (px + 26, 150)], [(px + 18, 246), (px + 26, 246)]])
    d.lines([[(px - w / 2, 98), (px - w / 2, 106)], [(px + w / 2, 98), (px + w / 2, 106)]])
    d.group()
    d.line((px - w / 2, 58), (px + w / 2, 58), (px + w / 2, 58 + t), (px - w / 2, 58 + t), closed=True)
    d.line((px - t / 2, 150), (px + t / 2, 150), (px + t / 2, 246), (px - t / 2, 246), closed=True)
    d.group('mid')
    # the elastic neutral axis through each section, and the depth that carries the load
    d.line((px - w / 2 - 8, 58 + t / 2), (px + w / 2 + 8, 58 + t / 2))
    d.line((px - t / 2 - 8, 198), (px + t / 2 + 8, 198))
    d.text(wx + L / 2, bot + 38, 'L', size=9)
    d.text(gx - 14, 286, 'GALILEO', size=8)
    d.text(ex2 + 4, 286, 'ELASTIC', size=8)
    d.text(px, 46, 'FLAT  ×1', size=8)
    d.text(px, 272, 'ON EDGE  ×4', size=8)
    d.text(px + 30, 201, 'h', size=9, anchor='start')
    return d


PLATES = {'galileo-beams': galileo_beams}


def _clip(poly, a, b, c):
    """Clip a convex polygon to the half-plane a·x + b·y <= c (Sutherland-Hodgman)."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if fp * fq < 0:
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def _cells(cx, cy, r, seeds):
    """Voronoi cells of the seeds, each clipped to a polygon approximating the circle (cx, cy, r)."""
    ring = [(cx + r * math.cos(2 * math.pi * k / 72), cy + r * math.sin(2 * math.pi * k / 72)) for k in range(72)]
    cells = []
    for i, (sx, sy) in enumerate(seeds):
        poly = ring[:]
        for j, (tx, ty) in enumerate(seeds):
            if i == j:
                continue
            # points nearer seed i than seed j: (t - s)·x <= (|t|² - |s|²) / 2
            a, b = tx - sx, ty - sy
            c = (tx * tx + ty * ty - sx * sx - sy * sy) / 2
            poly = _clip(poly, a, b, c)
            if not poly:
                break
        cells.append(poly)
    return cells


def _lamellae(poly, angle, spacing):
    """Parallel chords across a convex polygon, at `angle` degrees, `spacing` apart."""
    ux, uy = _dir(angle)
    nx, ny = -uy, ux
    proj = [x * nx + y * ny for x, y in poly]
    lo, hi = min(proj), max(proj)
    segs = []
    k = lo + spacing / 2
    while k < hi:
        pts = []
        m = len(poly)
        for i in range(m):
            p, q = poly[i], poly[(i + 1) % m]
            fp, fq = p[0] * nx + p[1] * ny - k, q[0] * nx + q[1] * ny - k
            if fp * fq < 0:
                t = fp / (fp - fq)
                pts.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
        if len(pts) == 2:
            # pull each end back from the boundary a little, as an etched plate stops short of the grain edge
            (x0, y0), (x1, y1) = pts
            L = math.hypot(x1 - x0, y1 - y0)
            if L > 6:
                f = 1.8 / L
                segs.append([(x0 + (x1 - x0) * f, y0 + (y1 - y0) * f), (x1 - (x1 - x0) * f, y1 - (y1 - y0) * f)])
        k += spacing
    return segs


def sorby_microscope():
    d = D()
    # the microscope with a vertical illuminator, in section: light enters from the side, a glass at 45°
    # turns it down through the objective onto the polished face, and the reflection comes back up
    ax = 96                                    # the optical axis
    gy = 118                                   # the 45° glass
    sy = 244                                   # the specimen's polished face
    d.group('thin')
    d.line((ax, 20), (ax, sy + 26))
    d.line((14, gy), (ax + 34, gy))
    d.line((ax - 26, gy + 26), (ax + 26, gy - 26))          # the plane of the glass, produced
    d.group()
    # the tube, the side arm for the light, the objective and the eyepiece
    d.line((ax - 14, 26), (ax - 14, gy - 12), (ax - 46, gy - 12))
    d.line((ax - 46, gy + 12), (ax - 14, gy + 12), (ax - 14, 186), (ax - 9, 206), (ax + 9, 206), (ax + 14, 186), (ax + 14, 26))
    d.line((ax - 18, 26), (ax + 18, 26))
    d.line((ax - 40, sy), (ax + 40, sy), (ax + 40, sy + 18), (ax - 40, sy + 18), closed=True)   # the specimen
    d.group('mid')
    d.line((ax - 12, gy + 12), (ax + 12, gy - 12))          # the glass
    d.ellipse(ax, 196, 10, 3)                               # the objective's front lens
    d.ellipse(ax, 34, 13, 3)                                # the eyepiece lens
    d.circle(18, gy, 7)                                     # the lamp
    # rays: in from the lamp, down to the specimen, back up to the eye
    d.lines([[(27, gy - 4), (ax - 4, gy - 4)], [(27, gy + 4), (ax + 4, gy + 4)]])
    d.lines([[(ax - 4, gy - 4), (ax - 4, sy)], [(ax + 4, gy + 4), (ax + 4, sy)]])
    d.lines([[(ax - 7, 140), (ax - 4, 146), (ax - 1, 140)], [(ax + 1, 160), (ax + 4, 154), (ax + 7, 160)]])
    # the field of view: grains of pearlite, each a colony of plates at its own angle, and a few of ferrite
    cx, cy, r = 284, 150, 100
    rnd = random.Random(1863)
    seeds = []
    while len(seeds) < 14:
        x, y = cx + rnd.uniform(-r, r), cy + rnd.uniform(-r, r)
        if math.hypot(x - cx, y - cy) < r * 0.92 and all(math.hypot(x - a, y - b) > 38 for a, b in seeds):
            seeds.append((x, y))
    cells = _cells(cx, cy, r, seeds)
    d.group('thin')
    d.line((ax + 20, sy + 9), (cx - r * 0.9, cy + r * 0.45))  # from the specimen to the enlarged field
    d.line((ax + 20, gy), (cx - r, cy - 8))
    d.group()
    d.circle(cx, cy, r)
    for poly in cells:
        d.line(*poly, closed=True)
    d.group('mid')
    ferrite = {2, 7, 11}                                    # three grains left plain: free iron
    segs = []
    for i, poly in enumerate(cells):
        if i in ferrite or len(poly) < 3:
            continue
        segs += _lamellae(poly, rnd.uniform(0, 180), 5.2)
    d.lines(segs)
    d.group('mid')
    d.text(18, gy - 14, 'LAMP', size=8)
    d.text(ax, 284, 'POLISHED, ETCHED', size=8)
    d.text(cx, cy + r + 18, '× 650', size=8)
    d.text(cx, 30, 'PEARLITE AND FERRITE', size=8)
    return d


PLATES['sorby-microscope'] = sorby_microscope


def iron_carbon():
    d = D()
    # the iron-iron carbide diagram, plotted from present-day values: carbon by weight across, temperature up
    x0, x1, c1 = 46, 386, 6.67
    y0, y1, t0, t1 = 268, 24, 400, 1600

    def P(c, t):
        return x0 + (x1 - x0) * c / c1, y0 - (y0 - y1) * (t - t0) / (t1 - t0)

    A, B, C, Dp = (0, 1538), (0.53, 1495), (4.30, 1147), (6.67, 1227)
    H, J, N = (0.09, 1495), (0.17, 1495), (0, 1394)
    E, F, G = (2.14, 1147), (6.67, 1147), (0, 912)
    S, Pp, K, Q = (0.76, 727), (0.022, 727), (6.67, 727), (0.005, 400)
    d.group('thin')
    # the axes and a grid of every 200 °C and every 1 per cent carbon
    d.lines([[P(0, t), P(c1, t)] for t in range(400, 1601, 200)])
    d.lines([[P(c, t0), P(c, t1)] for c in range(1, 7)])
    # the steel the reading cools: 0.4 per cent carbon, straight down from the melt
    d.line(P(0.4, 1560), P(0.4, 440))
    d.group()
    d.line(P(0, t1), P(0, t0), P(c1, t0), P(c1, t1))
    d.line(P(*A), P(*B), P(*C), P(*Dp))                     # liquidus
    d.line(P(*A), P(*H))                                    # solidus of delta iron
    d.line(P(*H), P(*B))                                    # the peritectic line
    d.line(P(*J), P(*E))                                    # solidus of austenite
    d.line(P(*E), P(*F))                                    # the eutectic line
    d.line(P(*N), P(*H))
    d.line(P(*N), P(*J))
    d.line(P(*G), P(*S))                                    # A3
    d.line(P(*S), P(*E))                                    # Acm
    d.line(P(*Pp), P(*K))                                   # A1, the eutectoid line
    d.line(P(*G), P(*Pp), P(*Q))
    d.group('mid')
    # where the 0.4 per cent steel crosses each line as it cools
    liq = 1538 + (1495 - 1538) * 0.4 / 0.53                # on AB
    a3 = 912 + (727 - 912) * 0.4 / 0.76                    # on GS
    for t in (liq, a3, 727):
        d.circle(*P(0.4, t), 2.6)
    d.circle(*P(*S), 3.2)
    d.circle(*P(*C), 3.2)
    d.group('mid')
    for t in (400, 800, 1200, 1600):
        x, y = P(0, t)
        d.text(x - 5, y + 3, str(t), size=7, anchor='end')
    for c in range(0, 7):
        x, y = P(c, t0)
        d.text(x, y + 12, str(c), size=7)
    d.text(*P(3.4, 1400), 'L', size=9)
    d.text(*P(1.0, 1000), 'γ', size=9)
    d.text(*P(3.6, 560), 'α + Fe₃C', size=8)
    sx, sy = P(*S)
    d.text(sx + 8, sy + 13, '0.76% · 727 °C', size=7, anchor='start')
    cx, cy = P(*C)
    d.text(cx, cy - 8, '4.3%', size=7)
    d.text(x1, 290, '% CARBON', size=7, anchor='end')
    d.text(x0 - 30, 16, '°C', size=7, anchor='start')
    return d


PLATES['iron-carbon'] = iron_carbon


def duralumin():
    d = D()
    # top: the heat treatment, temperature against time; bottom: hardness rising as the quenched metal ages,
    # read by eye from Merica, Waltenberg and Scott's Fig. 1 (alloy C11, quenched from 500 °C and from 295 °C)
    gx0, gx1 = 52, 384
    # top panel: temperature, 0-600 °C
    ty0, ty1 = 128, 26

    def T(x, t):
        return x, ty0 - (ty0 - ty1) * t / 600

    # bottom panel: scleroscope hardness 15-35 against days of ageing on a square-root scale (0-30)
    hy0, hy1 = 268, 168

    def H(day, hard):
        return gx0 + (gx1 - gx0) * math.sqrt(day / 30), hy0 - (hy0 - hy1) * (hard - 15) / 20

    d.group('thin')
    d.lines([[T(gx0, t), T(gx1, t)] for t in (20, 505)])
    d.line(T(gx0, 520), T(gx1, 520))                       # the eutectic: above this the metal burns
    d.lines([[H(0, h), H(30, h)] for h in (20, 25, 30, 35)])
    d.lines([[H(dd, 15), H(dd, 35)] for dd in (1, 4, 9, 16, 25)])
    d.group()
    d.line(T(gx0, 600), T(gx0, 0), T(gx1, 0))
    d.line(H(0, 35), H(0, 15), H(30, 15))
    # the cycle: heat to 505 °C, hold a quarter of an hour, quench to 20 °C, then wait
    d.line(T(gx0, 20), T(96, 505), T(150, 505), T(156, 20), T(gx1, 20))
    d.group('mid')
    a = [(0, 16), (0.9, 28.9), (2, 29.9), (2.85, 31), (4.8, 32.9), (5.85, 32.7), (30, 33.9)]
    b = [(0, 16), (0.1, 19), (0.9, 21.9), (3.9, 21.9), (5.85, 23), (30, 24)]
    d.line(*[H(*p) for p in a])
    d.line(*[H(*p) for p in b])
    for p in a[1:]:
        d.circle(*H(*p), 2.2)
    for p in b[2:]:
        x, y = H(*p)
        d.line((x - 2.2, y - 2.2), (x + 2.2, y - 2.2), (x + 2.2, y + 2.2), (x - 2.2, y + 2.2), closed=True)
    # the quench, an arrow down
    qx, qy = T(153, 260)
    d.lines([[(qx - 4, qy - 6), (qx, qy), (qx + 4, qy - 6)]])
    d.group('mid')
    d.text(*T(gx1, 532), '520 °C: THE METAL BURNS', size=7, anchor='end')
    d.text(123, T(0, 505)[1] + 13, '505 °C', size=7)
    d.text(*T(170, 270), 'QUENCH', size=7, anchor='start')
    d.text(*T(290, 50), 'AGE AT 20 °C', size=7)
    d.text(*H(30, 33.9 + 1.6), 'FROM 500 °C', size=7, anchor='end')
    d.text(*H(30, 24 + 1.6), 'FROM 295 °C', size=7, anchor='end')
    for dd in (0, 1, 4, 9, 16, 30):
        x, y = H(dd, 15)
        d.text(x, y + 12, str(dd), size=7)
    d.text(gx1, 294, 'DAYS', size=7, anchor='end')
    d.text(gx0 - 6, H(0, 35)[1] + 3, '35', size=7, anchor='end')
    d.text(gx0 - 6, H(0, 15)[1] + 3, '15', size=7, anchor='end')
    d.text(gx0 - 6, T(0, 600)[1] + 3, '600', size=7, anchor='end')
    d.text(gx0 - 6, T(0, 0)[1] + 3, '0', size=7, anchor='end')
    return d


PLATES['duralumin'] = duralumin
