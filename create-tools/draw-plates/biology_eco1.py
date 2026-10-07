"""Plates for The Story of Life, part eco1 (sprint 055): humboldt, haeckel-ecology, predator-prey.
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


# --- humboldt ------------------------------------------------------------------------------------

def humboldt():
    d = D()
    # Chimborazo in section, after the Tableau physique of the Essai sur la geographie des plantes
    # (1807): heights to scale (vertical only, as Humboldt's own), the zones at the heights his text
    # gives (palms to 1,000 m, cinchona to 2,900 m, trees cease at 3,500 m, grasses 4,100-4,600 m,
    # snow from 4,795 m), and beside it his table of mean temperatures by 1,000 m band (p. 81).
    # The profile is a computed dome, h = H(1 - (dx/w)^p), steeper on the Amazon side; not a survey.
    base, top_y, top_m = 262, 40, 6500
    k = (base - top_y) / top_m

    def y_of(m):
        return base - m * k

    H, c, wl, wr, p = 6263, 196, 150, 118, 1.7
    lowland = 300                                                         # the Amazon side's floor, m

    def h_at(x):
        if x <= c:
            t = min(1, (c - x) / wl)
            return max(0, H * (1 - t ** p))
        t = min(1, (x - c) / wr)
        return max(lowland, H * (1 - t ** p))

    def span(m):
        """The two x where the slope crosses height m."""
        xl = c - wl * (1 - m / H) ** (1 / p)
        xr = c + wr * (1 - m / H) ** (1 / p) if m >= lowland else c + wr
        return xl, xr

    xs = [c - wl + i for i in range(0, wl + wr + 1, 2)]
    prof = [(x, y_of(h_at(x))) for x in xs]

    d.group('thin')
    d.line((40, base), (40, top_y))                                       # height scale
    for m in range(0, 6001, 1000):
        d.line((36, y_of(m)), (44, y_of(m)))
    for m in range(0, 6001, 1000):                                        # height rules across
        d.dashed((48, y_of(m)), (318, y_of(m)), dash=2, gap=4)
    d.line((326, base), (392, base))                                      # temperature axis
    d.line((326, base), (326, top_y))
    tx = lambda t: 340 + t * 1.6                                          # -5..30 C
    for t in (0, 10, 20, 30):
        d.line((tx(t), base), (tx(t), base + 4))

    d.group()
    d.line((30, base), (392 - 74, base))                                  # sea level and lowland
    d.line(*prof)
    # Cotopaxi behind, a cone of 5,752 m by the Essai's measure
    cx2, w2 = 290, 30
    cone = [(cx2 - w2, y_of(3300)), (cx2 - 3, y_of(5752)), (cx2 + 3, y_of(5752)), (cx2 + w2, y_of(3300))]
    seen, run = [], []                                                    # only what shows above the dome
    for (x0, y0), (x1, y1) in zip(cone, cone[1:]):
        for i in range(41):
            x, y = x0 + (x1 - x0) * i / 40, y0 + (y1 - y0) * i / 40
            if y < y_of(h_at(x)) - 0.5:
                run.append((x, y))
            elif len(run) > 1:
                seen.append(run)
                run = []
            else:
                run = []
    if len(run) > 1:
        seen.append(run)
    d.lines(seen)

    d.group('mid')
    for m in (1000, 2900, 3500, 4100, 4600):                              # zone boundaries
        xl, xr = span(m)
        d.line((xl, y_of(m)), (xr, y_of(m)))
    xl, xr = span(4795)                                                   # the snow line, heavier
    d.line((xl, y_of(4795)), (xr, y_of(4795)))
    for i in range(7):                                                    # snow hatching on the dome
        m = 4900 + i * 190
        if m < H:
            a, b = span(m)
            d.line((a + 3, y_of(m)), (b - 3, y_of(m)))
    # vegetation glyphs along the left slope: palms, trees, grass tufts
    for m, kind in ((180, 'palm'), (520, 'palm'), (850, 'palm'), (1400, 'tree'), (1900, 'tree'),
                    (2500, 'tree'), (3100, 'tree'), (3700, 'shrub'), (4250, 'grass'), (4450, 'grass')):
        x0, _ = span(m)
        x0 += 9
        y0 = y_of(m)
        if kind == 'palm':
            d.line((x0, y0), (x0 + 1, y0 - 9))
            for a in (-60, -25, 25, 60):
                r = math.radians(a)
                d.line((x0 + 1, y0 - 9), (x0 + 1 + 5 * math.sin(r), y0 - 9 + 3 * math.cos(r) - 2))
        elif kind == 'tree':
            d.line((x0, y0), (x0, y0 - 5))
            d.circle(x0, y0 - 8, 3)
        elif kind == 'shrub':
            d.circle(x0 - 2, y0 - 2.5, 2.2)
            d.circle(x0 + 2, y0 - 2.5, 2.2)
        else:
            for dx in (-2, 0, 2):
                d.line((x0 + dx, y0), (x0 + dx * 1.6, y0 - 4))
    d.curve(f"M{cx2:.1f},{y_of(5752) - 2:.1f} C{cx2 - 6:.1f},{y_of(6100):.1f} {cx2 + 10:.1f},{y_of(6250):.1f} {cx2 + 4:.1f},{y_of(6550):.1f}")
    # Humboldt's mean temperatures, band midpoints
    means = [(500, 25.3), (1500, 21.2), (2500, 18.7), (3500, 9.0), (4500, 3.7), (5500, -2)]
    pts = [(tx(t), y_of(m)) for m, t in means]
    d.line(*pts)
    for x, y in pts:
        d.circle(x, y, 1.8)

    d.group('mid')
    for m in range(0, 6001, 2000):
        d.text(32, y_of(m) + 2.5, f'{m // 1000}' if m else '0', size=7, anchor='end')
    d.text(40, top_y - 6, 'KM', size=7)
    for t in (0, 10, 20, 30):
        d.text(tx(t), base + 12, f'{t}', size=7)
    d.text(366, base + 22, 'MEAN °C', size=7)
    labels = [(500, 'PALMS'), (1950, 'CINCHONA'), (3200, 'TREES END'), (4350, 'GRASSES')]
    for m, s in labels:
        a, b = span(m)
        d.text((a + b) / 2 + 6, y_of(m) + 2.5, s, size=7)
    d.text(c, y_of(H) - 6, 'CHIMBORAZO', size=7)
    d.text(90, y_of(4795) + 2.5, 'SNOW 4,795', size=7)
    d.text(180, 290, 'THE ANDES IN SECTION · ESSAI, 1807', size=7)
    return d


# --- haeckel-ecology -----------------------------------------------------------------------------

def haeckel_ecology():
    d = D()
    # Circogonia icosahedra (Haeckel, Challenger Report, 1887; Kunstformen der Natur, plate 1, fig. 1):
    # a lattice shell on the regular icosahedron, a radial tube at each of its twelve corners. The
    # solid is computed (vertices (0, +-1, +-phi) and their cyclic shifts), turned, and projected;
    # hidden edges are thin. The pores are drawn on the faces that face the viewer. Schematic.
    from plates import SOLIDS, rot
    verts = SOLIDS['icosa']
    ax, ay = 0.42, 0.33
    P = [rot(v, ax, ay) for v in verts]
    cx, cy, s = 168, 152, 47
    pr = lambda q: (cx + s * q[0], cy - s * q[1])
    n = len(verts)
    m = min(math.dist(verts[i], verts[j]) for i in range(n) for j in range(i + 1, n))
    adj = lambda i, j: abs(math.dist(verts[i], verts[j]) - m) < 1e-3
    faces = [(i, j, k) for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n)
             if adj(i, j) and adj(j, k) and adj(i, k)]
    front = []
    for f in faces:                                                       # outward normal toward the viewer?
        a, b, c = (P[i] for i in f)
        u = [b[t] - a[t] for t in range(3)]
        v = [c[t] - a[t] for t in range(3)]
        nz = u[0] * v[1] - u[1] * v[0]
        cen = [(a[t] + b[t] + c[t]) / 3 for t in range(3)]
        nrm = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], nz)
        if sum(nrm[t] * cen[t] for t in range(3)) < 0:
            nrm = tuple(-x for x in nrm)
        if nrm[2] > 0:
            front.append(f)
    edges = {(min(i, j), max(i, j)) for f in faces for i, j in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2]))}
    seen = {(min(i, j), max(i, j)) for f in front for i, j in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2]))}
    R = math.sqrt(1 + ((1 + 5 ** 0.5) / 2) ** 2) * s

    d.group('thin')
    d.circle(cx, cy, R)                                                   # the circumscribed sphere
    d.line((cx - R - 30, cy), (cx + R + 30, cy))
    d.line((cx, cy - R - 30), (cx, cy + R + 30))
    for i, j in sorted(edges - seen):                                     # hidden edges
        d.dashed(pr(P[i]), pr(P[j]), dash=2.5, gap=2.5)

    d.group()
    d.lines([[pr(P[i]), pr(P[j])] for i, j in sorted(seen)])

    d.group('mid')
    for i in range(n):                                                    # twelve radial tubes
        q = P[i]
        if q[2] < -0.6:
            continue
        r0 = math.hypot(q[0], q[1]) or 1
        ux, uy = q[0] / r0, q[1] / r0
        x0, y0 = pr(q)
        ln = 20 + 10 * (q[2] + 2) / 4
        x1, y1 = x0 + ux * ln, y0 - uy * ln
        d.line((x0, y0), (x1, y1))
        for sgn in (-1, 1):                                               # a forked tip
            a = math.atan2(-uy, ux) + sgn * 0.6
            d.line((x1, y1), (x1 + 6 * math.cos(a), y1 + 6 * math.sin(a)))
    for f in front:                                                       # lattice pores on the near faces
        a, b, c = (P[i] for i in f)
        for wa, wb, wc in ((4, 1, 1), (1, 4, 1), (1, 1, 4), (1, 1, 1)):
            w = wa + wb + wc
            q = [(wa * a[t] + wb * b[t] + wc * c[t]) / w for t in range(3)]
            x, y = pr(q)
            d.circle(x, y, 2.2)

    d.group('mid')
    d.text(cx, 18, 'CIRCOGONIA ICOSAHEDRA', size=7)
    d.text(318, 112, '20 FACES', size=7, anchor='start')
    d.text(318, 124, '30 EDGES', size=7, anchor='start')
    d.text(318, 136, '12 CORNERS', size=7, anchor='start')
    d.text(318, 148, '12 RADIAL TUBES', size=7, anchor='start')
    d.text(200, 292, 'A RADIOLARIAN SKELETON ON THE ICOSAHEDRON', size=7)
    return d


# --- predator-prey -------------------------------------------------------------------------------

def _lv_run(x, y, a=1.0, b=0.1, g=1.0, dl=0.025, h=0.005, T=7.0):
    """The Lotka-Volterra equations stepped by fourth-order Runge-Kutta; the reading's invented constants."""
    f = lambda x, y: (a * x - b * x * y, dl * x * y - g * y)
    out = [(0.0, x, y)]
    for i in range(int(T / h)):
        k1 = f(x, y)
        k2 = f(x + h / 2 * k1[0], y + h / 2 * k1[1])
        k3 = f(x + h / 2 * k2[0], y + h / 2 * k2[1])
        k4 = f(x + h * k3[0], y + h * k3[1])
        x += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        out.append(((i + 1) * h, x, y))
    return out


def predator_prey():
    d = D()
    # Left: the predator-prey plane, after Volterra's Fig. 2 (Nature, 1926), three closed orbits about
    # the equilibrium (gamma/delta, alpha/beta) = (40, 10), computed. Right: the outer orbit's run in
    # time, prey and predators on one axis (predators x4), the predator peak lagging the prey's.
    px0, py0, pw, ph = 46, 250, 176, 190                                 # plane: prey 0-80, predators 0-20
    X = lambda v: px0 + v / 80 * pw
    Y = lambda v: py0 - v / 20 * ph
    runs = [_lv_run(40, y0) for y0 in (5, 6.5, 8)]

    tx0, ty0, tw, th = 252, 250, 140, 190                                # time: 0-7 years; 0-80
    TX = lambda t: tx0 + t / 7 * tw
    TY = lambda v: ty0 - v / 80 * th

    d.group('thin')
    d.line((px0, py0 - ph - 6), (px0, py0), (px0 + pw + 6, py0))
    d.line((tx0, ty0 - th - 6), (tx0, ty0), (tx0 + tw + 6, ty0))
    d.dashed((X(40), py0), (X(40), Y(10)), (px0, Y(10)), dash=2, gap=3)
    for v in (20, 40, 60, 80):
        d.line((X(v), py0), (X(v), py0 + 3))
    for v in (5, 10, 15, 20):
        d.line((px0 - 3, Y(v)), (px0, Y(v)))
    for t in range(8):
        d.line((TX(t), ty0), (TX(t), ty0 + 3))

    d.group()
    for r in runs:
        d.line(*[(X(x), Y(y)) for _, x, y in r[::4]])
    outer = runs[0]
    d.line(*[(TX(t), TY(x)) for t, x, _ in outer[::4]])

    d.group('mid')
    d.dashed(*[(TX(t), TY(4 * y)) for t, _, y in outer[::4]], dash=3, gap=2)
    d.circle(X(40), Y(10), 2.5)
    for r in runs:                                                        # direction of travel
        i = len(r) // 9
        (_, x0, y0), (_, x1, y1) = r[i], r[i + 6]
        _arrow(d, (X(x0), Y(y0)), (X(x1), Y(y1)), size=5)
    ip = max(range(len(outer)), key=lambda i: outer[i][1])
    iq = max(range(len(outer)), key=lambda i: outer[i][2])
    for i, v in ((ip, outer[ip][1]), (iq, 4 * outer[iq][2])):
        d.line((TX(outer[i][0]), TY(v) - 3), (TX(outer[i][0]), ty0))

    d.group('mid')
    d.text(px0 + pw / 2, py0 + 14, 'PREY', size=7)
    d.text(px0 - 6, py0 - ph - 10, 'PREDATORS', size=7, anchor='start')
    d.text(X(40) + 4, py0 - 6, 'EQUILIBRIUM', size=7, anchor='start')
    for v in (40, 80):
        d.text(X(v), py0 + 24, f'{v}', size=7)
    for v in (10, 20):
        d.text(px0 - 5, Y(v) + 2.5, f'{v}', size=7, anchor='end')
    d.text(tx0 + tw / 2, ty0 + 14, 'YEARS', size=7)
    for t in (0, 7):
        d.text(TX(t), ty0 + 24, f'{t}', size=7)
    d.text(TX(outer[ip][0]) + 4, TY(outer[ip][1]) - 4, 'PREY', size=7, anchor='start')
    d.text(TX(outer[iq][0]) + 4, TY(4 * outer[iq][2]) - 6, 'PREDATORS ×4', size=7, anchor='start')
    d.text(200, 22, 'LOTKA-VOLTERRA · INVENTED CONSTANTS', size=7)
    return d


PLATES = {'humboldt': humboldt, 'haeckel-ecology': haeckel_ecology, 'predator-prey': predator_prey}
