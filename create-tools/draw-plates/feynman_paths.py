"""feynman plates, trail "Sum over histories" (sprint 014). See plates_for.py."""
import cmath, math, random

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _vector(d, x0, y0, x1, y1, size=4):
    """A line from (x0, y0) to (x1, y1) with an arrowhead at its end."""
    d.line((x0, y0), (x1, y1))
    _arrow(d, x1, y1, math.atan2(y1 - y0, x1 - x0), size)


def principle_of_least_action():
    """Fermat's least time: light from A in air to B under water, the paths it did not take, and the time each costs."""
    d = D()
    n = 1.33
    m = 70                    # pixels per metre
    ax, ay, wy = 40, 80, 150  # A, and the water's surface
    bx, by = ax + 2 * m, wy + m
    T = lambda x: math.sqrt(1 + x * x) + n * math.sqrt(1 + (2 - x) ** 2)  # time, in metres of vacuum
    lo, hi = 0.0, 2.0
    for _ in range(80):
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        lo, hi = (lo, b) if T(a) < T(b) else (a, hi)
    xs = (lo + hi) / 2        # the true crossing point, 1.27 m along
    px = ax + xs * m
    # the chart of time against crossing point, on the right
    cx0, cx1, cy0, cy1 = 232, 380, 232, 92
    tmin, tmax = 3.2, 4.0
    C = lambda x, t: (cx0 + (cx1 - cx0) * x / 2, cy0 - (cy0 - cy1) * (t - tmin) / (tmax - tmin))
    # construction: the surface, the normal at the crossing, the chart's grid, the crossings carried across
    d.group('thin')
    d.line((20, wy), (206, wy))
    d.line((px, wy - 72), (px, wy + 78))
    d.lines([[C(k / 4, tmin), C(k / 4, tmax)] for k in range(1, 9)])
    d.lines([[C(0, tmin + k * 0.2), C(2, tmin + k * 0.2)] for k in range(1, 5)])
    d.lines([[(ax + x * m, wy), (ax + x * m, wy + 6)] for x in (0.5, 1.0, 1.6, 2.0)])
    d.lines([[(20 + 12 * k, wy + 16 + 22 * j), (28 + 12 * k, wy + 16 + 22 * j)] for k in range(15) for j in range(3)
             if not (abs(20 + 12 * k - px) < 12 and j == 0)])
    # the paths it did not take: straight to the surface at other points, then straight on
    d.group('mid')
    for x in (0.5, 1.0, 1.6, 2.0):
        d.line((ax, ay), (ax + x * m, wy), (bx, by))
    # the true ray, and its ends
    d.group()
    d.line((ax, ay), (px, wy), (bx, by))
    d.circle(ax, ay, 3.5)
    d.circle(bx, by, 3.5)
    # the angles to the normal
    d.group('mid')
    t1 = math.atan2(px - ax, wy - ay)
    t2 = math.atan2(bx - px, by - wy)
    d.arc(px, wy, 26, -90 - math.degrees(t1), -90, n=24)
    d.arc(px, wy, 26, 90 - math.degrees(t2), 90, n=24)
    # the chart: the time of each crossing, least at the true one
    d.group()
    d.line(C(0, tmin), (cx1 + 6, cy0))
    d.line(C(0, tmin), (cx0, cy1 - 6))
    _arrow(d, cx1 + 6, cy0, 0)
    _arrow(d, cx0, cy1 - 6, -math.pi / 2)
    d.line(*[C(2 * i / 80, T(2 * i / 80)) for i in range(81)])
    d.group('mid')
    for x in (0.5, 1.0, 1.6, 2.0):
        d.circle(*C(x, T(x)), 2.5)
    d.circle(*C(xs, T(xs)), 4)
    d.line(C(xs, T(xs)), C(xs, tmin))
    d.group()
    d.text(210, 24, 'LIGHT TAKES THE PATH OF LEAST TIME', size=8)
    d.text(ax - 8, ay - 8, 'A', size=9)
    d.text(bx + 10, by + 4, 'B', size=9)
    d.text(26, wy - 6, 'AIR', size=7, anchor='start')
    d.text(26, wy + 64, 'WATER', size=7, anchor='start')
    d.text(px - 6, wy - 32, 'θ₁', size=8)
    d.text(px + 8, wy + 40, 'θ₂', size=8)
    d.text((cx0 + cx1) / 2, cy0 + 16, 'WHERE IT CROSSES', size=7)
    d.text(cx0 + 6, cy1 - 4, 'TIME', size=7, anchor='start')
    d.text(210, 284, 'sin θ₁ / sin θ₂ = 1.33', size=8)
    return d


def dirac_hint():
    """Dirac's kernel: the wave carried from one instant to the next, slice by slice, and a path threaded through the slices."""
    d = D()
    x0, x1 = 50, 300           # space runs across
    ys = [246 - 34 * k for k in range(7)]  # instants t, t+ε, ... running up
    # construction: the time slices and the space grid
    d.group('thin')
    d.lines([[(x0, y), (x1, y)] for y in ys])
    d.lines([[(x0 + 25 * k, ys[0]), (x0 + 25 * k, ys[-1])] for k in range(11)])
    # the kernel: from one point at t+2ε, links to every point at t+3ε, each weighted e^{iεL/ħ}
    d.group('mid')
    src = (x0 + 25 * 5, ys[2])
    d.lines([[src, (x0 + 25 * k, ys[3])] for k in range(1, 10)])
    # a second path, fainter
    random.seed(4)
    alt = [x0 + 25 * k for k in (2, 3, 5, 4, 6, 6, 8)]
    d.line(*[(alt[k], ys[k]) for k in range(7)])
    # the path: one position at each instant, joined
    d.group()
    xs = [x0 + 25 * k for k in (2, 4, 5, 7, 6, 7, 8)]
    d.line(*[(xs[k], ys[k]) for k in range(7)])
    d.circle(xs[0], ys[0], 3.5)
    d.circle(xs[-1], ys[-1], 3.5)
    d.group('mid')
    for k in range(1, 6):
        d.circle(xs[k], ys[k], 2.2)
    d.circle(*src, 3)
    # axes
    d.group()
    d.line((x0 - 14, ys[0] + 14), (x1 + 14, ys[0] + 14))
    _arrow(d, x1 + 14, ys[0] + 14, 0)
    d.line((x0 - 14, ys[0] + 14), (x0 - 14, ys[-1] - 18))
    _arrow(d, x0 - 14, ys[-1] - 18, -math.pi / 2)
    d.group()
    d.text(200, 24, 'K(x′, x) ∝ exp(iεL/ħ)', size=9)
    labels = ['t', 't+ε', 't+2ε', 't+3ε', 't+4ε', 't+5ε', 't+6ε']
    for k, y in enumerate(ys):
        d.text(x1 + 10, y + 3, labels[k], size=7, anchor='start')
    d.text(x1 + 10, ys[0] + 28, 'x', size=8, anchor='start')
    d.text(x0 - 22, ys[-1] - 22, 'TIME', size=7, anchor='start')
    d.text(src[0] - 8, src[1] + 13, 'x', size=8, anchor='end')
    d.text(x0 + 25 * 9 + 4, ys[3] - 6, 'x′', size=8, anchor='start')
    return d


def path_integral():
    """Paths from A to B in space-time, each bent differently, and the arrows e^{iS/ħ} they contribute, added head to tail."""
    d = D()
    ox, oy, w, h = 34, 150, 200, 110   # time runs right from A at (ox, oy) to B at (ox + w, oy)
    random.seed(1948)
    paths = []
    for k in range(9):
        amps = [random.uniform(-0.6, 0.6) / (j + 1) for j in range(1, 5)]
        paths.append(amps)
    paths.sort(key=lambda a: sum((j + 1) ** 2 * c * c for j, c in enumerate(a)))
    P = lambda t, amps, tilt=0.35: (ox + w * t, oy - h * (tilt * t + sum(c * math.sin((j + 1) * math.pi * t) for j, c in enumerate(amps))))
    # action of a free path relative to the straight one: sum of (mode number × amplitude)², scaled
    S = lambda amps: sum(((j + 1) * c) ** 2 for j, c in enumerate(amps))
    # construction: time grid, the endpoints' verticals
    d.group('thin')
    d.lines([[(ox + w * k / 8, oy + 40), (ox + w * k / 8, oy - h * 0.95)] for k in range(0, 9)])
    d.line((ox - 6, oy), (ox + w + 6, oy))
    # the other paths
    d.group('mid')
    for amps in paths[1:]:
        d.line(*[P(i / 60, amps) for i in range(61)])
    # the classical path, and A and B
    d.group()
    d.line(*[P(i / 60, []) for i in range(61)])
    d.circle(*P(0, []), 3.5)
    d.circle(*P(1, []), 3.5)
    # the arrows, one per path, in order of action: each turned by its phase, laid head to tail
    d.group()
    x, y = 262, 200
    scale = 16
    k = 7.0   # phase per unit of this plate's action, standing in for 1/ħ
    for amps in [[]] + paths[1:]:
        ph = k * S(amps)
        nx, ny = x + scale * math.cos(ph - math.pi / 2 + 0.0), y + scale * math.sin(ph - math.pi / 2)
        _vector(d, x, y, nx, ny, 3.5)
        x, y = nx, ny
    # the sum: from the first tail to the last head
    d.group('mid')
    d.line((262, 200), (x, y))
    _arrow(d, x, y, math.atan2(y - 200, x - 262), 5)
    d.group()
    d.text(200, 24, 'AMPLITUDE = Σ exp(iS/ħ) OVER EVERY PATH', size=8)
    d.text(ox - 4, oy + 16, 'A', size=9)
    d.text(ox + w + 4, P(1, [])[1] - 8, 'B', size=9)
    d.text(ox + w / 2, oy + 56, 'TIME →', size=7)
    d.text(322, 230, 'ONE ARROW PER PATH', size=7)
    return d


def every_path():
    """The double slit grown: screens with more and more holes between a source and a detector, and the routes through them."""
    d = D()
    sx, sy = 30, 130           # the source
    dx, dy = 360, 118          # the detector
    screens = [(110, 2), (180, 3), (250, 5)]
    top, bot = 40, 220
    holes = {}
    for x, n in screens:
        holes[x] = [top + (bot - top) * (i + 1) / (n + 1) for i in range(n)]
    # construction: the axis from source to detector, the hole centres carried across
    d.group('thin')
    d.line((sx, sy), (dx, dy))
    for x, n in screens:
        d.lines([[(x - 8, y), (x + 8, y)] for y in holes[x]])
    # the routes: every choice of one hole in each screen, a few of them drawn
    d.group('mid')
    random.seed(7)
    routes = []
    for a in holes[110]:
        for b in holes[180]:
            c = random.choice(holes[250])
            routes.append([(sx, sy), (110, a), (180, b), (250, c), (dx, dy)])
    for r in routes[1:]:
        d.line(*r)
    # the screens, drawn as walls with gaps
    d.group()
    gap = 5
    for x, n in screens:
        ys = [top] + [v for y in holes[x] for v in (y - gap, y + gap)] + [bot]
        d.lines([[(x, ys[i]), (x, ys[i + 1])] for i in range(0, len(ys), 2)])
    d.circle(sx, sy, 3.5)
    d.circle(dx, dy, 3.5)
    d.line(*routes[0])
    # the arrows at the detector for two slits: in step (bright) and opposed (dark)
    d.group('mid')
    bx, by = 60, 262
    _vector(d, bx, by, bx + 22, by, 3.5)
    _vector(d, bx + 22, by, bx + 44, by, 3.5)
    kx = 180
    _vector(d, kx, by, kx + 22, by, 3.5)
    _vector(d, kx + 22, by + 3, kx, by + 3, 3.5)
    d.group()
    d.text(200, 24, 'MORE SCREENS, MORE HOLES, UNTIL THERE IS NO SCREEN', size=8)
    d.text(sx, sy + 16, 'S', size=9)
    d.text(dx, dy + 16, 'D', size=9)
    d.text(bx + 22, by + 18, 'BRIGHT', size=7)
    d.text(kx + 11, by + 18, 'DARK', size=7)
    d.text(330, 266, 'SUM OF ARROWS', size=7)
    return d


def classical_limit():
    """The Cornu spiral: the arrows of a family of paths added head to tail, straight near the true path and curling away from it."""
    d = D()
    cx, cy, s = 200, 152, 158

    def fresnel(u, n=400):
        h = u / n
        z = sum(cmath.exp(1j * math.pi * ((i + 0.5) * h) ** 2 / 2) for i in range(n)) * h
        return z

    pts = {}
    us = [i / 40 for i in range(-200, 201)]
    for u in us:
        z = fresnel(u, n=max(40, int(abs(u) * 60)))
        pts[u] = (cx + s * z.real, cy - s * z.imag)
    e1, e2 = (cx + s * 0.5, cy - s * 0.5), (cx - s * 0.5, cy + s * 0.5)
    # construction: the axes through the middle, the eyes' centres
    d.group('thin')
    d.line((cx - 150, cy), (cx + 150, cy))
    d.line((cx, cy - 112), (cx, cy + 112))
    d.lines([[(e1[0] - 10, e1[1]), (e1[0] + 10, e1[1])], [(e1[0], e1[1] - 10), (e1[0], e1[1] + 10)],
             [(e2[0] - 10, e2[1]), (e2[0] + 10, e2[1])], [(e2[0], e2[1] - 10), (e2[0], e2[1] + 10)]])
    # the spiral: paths far from the true one, winding into the eyes
    d.group('mid')
    d.line(*[pts[u] for u in us if u <= -1])
    d.line(*[pts[u] for u in us if u >= 1])
    # the stretch from the paths near the true one: the arrows that agree
    d.group()
    d.line(*[pts[u] for u in us if -1 <= u <= 1])
    for u in (-1, -0.5, 0, 0.5):
        a, b = pts[u], pts[u + 0.5]
        _arrow(d, *b, math.atan2(b[1] - a[1], b[0] - a[0]), 4)
    # the total: from eye to eye
    d.group('mid')
    d.line(e2, e1)
    _arrow(d, *e1, math.atan2(e1[1] - e2[1], e1[0] - e2[0]), 6)
    d.circle(*pts[0], 3)
    d.group()
    d.text(200, 22, 'PHASE ∝ u² NEAR THE TRUE PATH', size=8)
    d.text(pts[0][0] + 8, pts[0][1] + 14, 'TRUE PATH', size=7, anchor='start')
    d.text(334, 58, 'FAR PATHS', size=7, anchor='start')
    d.text(334, 68, 'WIND UP', size=7, anchor='start')
    d.text(208, 272, 'AND CANCEL', size=7, anchor='start')
    d.text(386, 290, 'THE CORNU SPIRAL', size=7, anchor='end')
    return d


def path_integrals_today():
    """A space-time lattice in imaginary time: its sites and links, a Wilson loop, and a random walk along the links."""
    d = D()
    nx, ny, nz = 6, 4, 3
    a = 40
    ox, oy = 70, 230
    dxz, dyz = 0.62 * a * math.cos(math.radians(32)), 0.62 * a * math.sin(math.radians(32))
    Pt = lambda i, j, k: (ox + a * i + dxz * k, oy - a * j - dyz * k)
    # construction: every link of the lattice
    d.group('thin')
    segs = []
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                if i + 1 < nx:
                    segs.append([Pt(i, j, k), Pt(i + 1, j, k)])
                if j + 1 < ny:
                    segs.append([Pt(i, j, k), Pt(i, j + 1, k)])
                if k + 1 < nz:
                    segs.append([Pt(i, j, k), Pt(i, j, k + 1)])
    d.lines(segs)
    # the sites
    d.group('mid')
    for i in range(nx):
        for j in range(ny):
            d.circle(*Pt(i, j, 0), 1.6)
    # a random walk along the links of the front face, as in a Feynman-Kac sum over Brownian paths
    d.group()
    random.seed(1949)
    i, j = 0, 1
    walk = [Pt(i, j, 0)]
    while i < nx - 1:
        step = random.choice(['r', 'r', 'u', 'd'])
        if step == 'r':
            i += 1
        elif step == 'u' and j < ny - 1:
            j += 1
        elif step == 'd' and j > 0:
            j -= 1
        else:
            continue
        walk.append(Pt(i, j, 0))
    d.line(*walk)
    d.circle(*walk[0], 3.5)
    d.circle(*walk[-1], 3.5)
    # a Wilson loop: a closed rectangle of links on the top face, with its direction
    d.group('mid')
    loop = [Pt(1, ny - 1, 0), Pt(3, ny - 1, 0), Pt(3, ny - 1, 2), Pt(1, ny - 1, 2)]
    d.line(*loop, closed=True)
    for p, q in zip(loop, loop[1:] + loop[:1]):
        m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        _arrow(d, *m, math.atan2(q[1] - p[1], q[0] - p[0]), 4)
    # the lattice spacing
    d.group('thin')
    p, q = Pt(0, 0, 0), Pt(1, 0, 0)
    d.line((p[0], p[1] + 14), (q[0], q[1] + 14))
    d.lines([[(p[0], p[1] + 8), (p[0], p[1] + 18)], [(q[0], q[1] + 8), (q[0], q[1] + 18)]])
    d.group()
    d.text(200, 24, 'Z = ∫ DU exp(−S[U])  ·  SUMMED BY MONTE CARLO', size=8)
    d.text((p[0] + q[0]) / 2, p[1] + 28, 'a', size=8)
    d.text(Pt(nx - 1, 0, 0)[0], Pt(nx - 1, 0, 0)[1] + 28, 'IMAGINARY TIME →', size=7, anchor='end')
    lp = Pt(2, ny - 1, 2)
    d.text(lp[0], lp[1] - 12, 'WILSON LOOP', size=7)
    return d


PLATES = {
    'principle-of-least-action': principle_of_least_action,
    'dirac-hint': dirac_hint,
    'path-integral': path_integral,
    'every-path': every_path,
    'classical-limit': classical_limit,
    'path-integrals-today': path_integrals_today,
}
