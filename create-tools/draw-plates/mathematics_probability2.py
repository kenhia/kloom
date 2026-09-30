"""Plates for the mathematics subject's Probability segment, second part (sprint 024):
Markov chains, Brownian motion and Wiener's measure, Kolmogorov's axioms, Monte Carlo."""
import math, random
from plates import D, f


def _dots(pts, r):
    """Many small circles as one path."""
    return ' '.join(f'M{f(x - r)} {f(y)} a{f(r)} {f(r)} 0 1 0 {f(2 * r)} 0 a{f(r)} {f(r)} 0 1 0 {f(-2 * r)} 0'
                    for x, y in pts)


def _arrowhead(d, tip, frm, size=5):
    ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    a1, a2 = ang + math.radians(152), ang - math.radians(152)
    d.line((tip[0] + size * math.cos(a1), tip[1] + size * math.sin(a1)), tip,
           (tip[0] + size * math.cos(a2), tip[1] + size * math.sin(a2)))


def markov_chains():
    """Markov's two-state chain for Eugene Onegin, with his own counts, and the
    chance of a vowel settling to its stationary value from either start."""
    d = D()
    p1 = 1104 / 8638            # vowel after a vowel
    p0 = 7534 / 11362           # vowel after a consonant
    stat = p0 / (1 - p1 + p0)   # 0.432
    # the state diagram, upper left
    vx, cx, sy, r = 70, 200, 88, 24
    # the plot, lower half
    x0, x1, y0, y1 = 40, 370, 272, 152   # y0 is probability 0, y1 is probability 1
    n = 8
    X = lambda k: x0 + (x1 - x0) * k / n
    Y = lambda p: y0 + (y1 - y0) * p
    d.group('thin')
    # axes and grid of the plot
    d.line((x0, y1 - 4), (x0, y0), (x1 + 6, y0))
    d.lines([[(X(k), y0), (X(k), y0 + 4)] for k in range(n + 1)])
    d.lines([[(x0 - 4, Y(p)), (x0, Y(p))] for p in (0, 0.5, 1)])
    # the centres' baseline of the diagram
    d.line((vx - r - 14, sy), (cx + r + 14, sy))
    d.group()
    # the two states
    d.circle(vx, sy, r)
    d.circle(cx, sy, r)
    # transitions between them: arcs above (V to C) and below (C to V)
    def between(sign):
        pts = []
        for i in range(41):
            t = i / 40
            x = vx + (cx - vx) * t
            y = sy + sign * (r * 0.7 + 30 * math.sin(math.pi * t))
            pts.append((x, y))
        return pts
    top = between(-1)
    bot = between(1)
    top = [p for p in top if math.dist(p, (vx, sy)) > r + 2 and math.dist(p, (cx, sy)) > r + 2]
    bot = [p for p in bot if math.dist(p, (vx, sy)) > r + 2 and math.dist(p, (cx, sy)) > r + 2]
    d.line(*top)
    d.line(*bot)
    # self-loops, outward
    def loop(cx_, direction):
        lx = cx_ + direction * (r + 9)
        base = 0 if direction > 0 else 180
        pts = [(lx + 14 * math.cos(math.radians(base - direction * (160 - 320 * i / 64))),
                sy + 14 * math.sin(math.radians(base - direction * (160 - 320 * i / 64)))) for i in range(65)]
        return [p for p in pts if math.dist(p, (cx_, sy)) > r + 1.5]
    lv = loop(vx, -1)
    lc = loop(cx, 1)
    d.line(*lv)
    d.line(*lc)
    d.group('mid')
    _arrowhead(d, top[-1], top[-4])
    _arrowhead(d, bot[0], bot[3])
    _arrowhead(d, lv[-1], lv[-4])
    _arrowhead(d, lc[-1], lc[-4])
    # the stationary value, dashed across the plot
    segs, x = [], x0
    while x < x1:
        segs.append([(x, Y(stat)), (min(x + 5, x1), Y(stat))])
        x += 9
    d.lines(segs)
    d.group()
    # the chance of a vowel, k letters on, from a vowel and from a consonant
    for start in (1.0, 0.0):
        p, pts = start, [(X(0), Y(start))]
        for k in range(1, n + 1):
            p = p * p1 + (1 - p) * p0
            pts.append((X(k), Y(p)))
        d.line(*pts)
    d.group('mid')
    d.path(_dots([(X(k), Y(v)) for start in (1.0, 0.0)
                  for k, v in enumerate(_chain(start, p1, p0, n))], 1.6))
    d.group('mid')
    d.text(vx, sy + 3, 'V')
    d.text(cx, sy + 3, 'C')
    d.text((vx + cx) / 2, sy - r * 0.7 - 34, '.872', size=8)
    d.text((vx + cx) / 2, sy + r * 0.7 + 42, '.663', size=8)
    d.text(vx - r - 9, sy - 20, '.128', size=8)
    d.text(cx + r + 9, sy - 20, '.337', size=8)
    d.text(x1 + 4, Y(stat) - 5, '.432', size=8, anchor='end')
    d.text(x0 - 8, Y(1) + 3, '1', size=7, anchor='end')
    d.text(x0 - 8, Y(0) + 3, '0', size=7, anchor='end')
    for k in (0, 4, 8):
        d.text(X(k), y0 + 14, str(k), size=7)
    d.text(292, 60, 'V  VOWEL', size=7, anchor='start')
    d.text(292, 74, 'C  CONSONANT', size=7, anchor='start')
    d.text(292, 96, '20,000 LETTERS', size=7, anchor='start')
    d.text((x0 + x1) / 2, y0 + 26, 'LETTERS ON', size=7)
    return d


def _chain(start, p1, p0, n):
    p, out = start, [start]
    for _ in range(n):
        p = p * p1 + (1 - p) * p0
        out.append(p)
    return out


def wiener_measure():
    """One random walk of 4,096 steps, each of size 1/sqrt(4096), seen coarse
    (16 steps) and fine, inside its sqrt(t) envelopes; and a window of it
    magnified 16 times in time and 4 in height, as rough as the whole."""
    d = D()
    N = 4096
    rng = random.Random(1923)
    w = [0.0]
    for _ in range(N):
        w.append(w[-1] + (1 if rng.random() < 0.5 else -1) / math.sqrt(N))
    x0, x1, yc, s = 30, 250, 150, 78       # t from 0 to 1 across; s pixels per unit of W
    X = lambda t: x0 + (x1 - x0) * t
    Y = lambda v: yc - s * v
    # the window to magnify: 1/16 of the time
    k0 = 2304
    k1 = k0 + N // 16
    wx0, wx1 = 270, 385                      # the magnified panel
    wyc = 150
    base = w[k0]
    WX = lambda t: wx0 + (wx1 - wx0) * t
    WY = lambda v: wyc - s * 0.5 * v       # the panel's own scale, drawn half as tall
    d.group('thin')
    d.line((x0, Y(0)), (x1 + 6, Y(0)))
    d.line((x0, Y(1.6)), (x0, Y(-1.6)))
    for c in (1, 2):
        for sign in (1, -1):
            d.line(*[(X(t), Y(sign * c * math.sqrt(t))) for t in [i / 80 for i in range(81)] if abs(c * math.sqrt(t)) < 1.55])
    # the window on the path, and the panel it is drawn out into
    lo = min(w[k0:k1 + 1]) - 0.04
    hi = max(w[k0:k1 + 1]) + 0.04
    d.line((X(k0 / N), Y(hi)), (X(k1 / N), Y(hi)), (X(k1 / N), Y(lo)), (X(k0 / N), Y(lo)), closed=True)
    d.line((wx0, wyc - 95), (wx1, wyc - 95), (wx1, wyc + 95), (wx0, wyc + 95), closed=True)
    d.line((X(k1 / N), Y(hi)), (wx0, wyc - 95))
    d.line((X(k1 / N), Y(lo)), (wx0, wyc + 95))
    d.line((wx0, wyc), (wx1, wyc))
    d.group('mid')
    # the coarse walk: the same path seen every 256 steps
    d.line(*[(X(k / N), Y(w[k])) for k in range(0, N + 1, 256)])
    d.group()
    # the fine walk
    d.line(*[(X(k / N), Y(w[k])) for k in range(0, N + 1, 2)])
    # the window, magnified 16 times in time and 4 in height (sqrt 16), drawn at half scale
    d.line(*[(WX((k - k0) / (k1 - k0)), WY(4 * (w[k] - base))) for k in range(k0, k1 + 1)])
    d.group('mid')
    d.text(x1 + 8, Y(0) + 3, 't', size=8, anchor='start')
    d.text(X(1) - 2, Y(math.sqrt(1)) - 4, '√t', size=8, anchor='end')
    d.text(X(0.6) - 2, Y(2 * math.sqrt(0.6)) + 12, '2√t', size=8, anchor='end')
    d.text(x0 + 4, 272, '16 STEPS AND 4,096', size=7, anchor='start')
    d.text((wx0 + wx1) / 2, wyc + 110, '×16 IN TIME', size=7)
    d.text((wx0 + wx1) / 2, wyc + 121, '×4 IN HEIGHT', size=7)
    return d


def kolmogorov():
    """A field of probability drawn as area: the unit square E, two events A and B,
    their product AB hatched; and A taken as the whole, for P_A(B) = P(AB)/P(A)."""
    d = D()
    x0, y0, S = 30, 40, 200                 # the unit square E
    A = (x0 + 0.40 * S, y0 + 0.50 * S, 0.27 * S)
    B = (x0 + 0.64 * S, y0 + 0.45 * S, 0.22 * S)
    inA = lambda x, y: math.hypot(x - A[0], y - A[1]) <= A[2]
    inB = lambda x, y: math.hypot(x - B[0], y - B[1]) <= B[2]
    # the second panel: A alone, scaled up as the new whole
    ax, ay, ar = 330, 140, 56
    k = ar / A[2]
    d.group('thin')
    # a grid of tenths: area measured in hundredths
    d.lines([[(x0 + i * S / 10, y0), (x0 + i * S / 10, y0 + S)] for i in range(1, 10)] +
            [[(x0, y0 + i * S / 10), (x0 + S, y0 + i * S / 10)] for i in range(1, 10)])
    # projection from A to the second panel
    d.line((A[0], A[1] - A[2]), (ax, ay - ar))
    d.line((A[0], A[1] + A[2]), (ax, ay + ar))
    d.group()
    d.line((x0, y0), (x0 + S, y0), (x0 + S, y0 + S), (x0, y0 + S), closed=True)
    d.circle(*A)
    d.circle(*B)
    d.circle(ax, ay, ar)
    d.group('mid')
    # AB, hatched, in both panels: diagonal lines clipped to the intersection
    def hatch(inside, cxy, rad, step, tx=lambda x, y: (x, y)):
        segs = []
        for c in range(-int(2 * rad), int(2 * rad) + 1, step):
            run = []
            for i in range(0, 241):
                t = -rad + 2 * rad * i / 240
                x, y = cxy[0] + t, cxy[1] - t + c
                if inside(x, y):
                    run.append(tx(x, y))
                elif run:
                    if len(run) > 1:
                        segs.append([run[0], run[-1]])
                    run = []
            if len(run) > 1:
                segs.append([run[0], run[-1]])
        return segs
    both = lambda x, y: inA(x, y) and inB(x, y)
    d.lines(hatch(both, (A[0], A[1]), A[2], 5))
    to2 = lambda x, y: (ax + k * (x - A[0]), ay + k * (y - A[1]))
    d.lines(hatch(both, (A[0], A[1]), A[2], 3, to2))
    # B's arc inside the enlarged A
    arc = [to2(B[0] + B[2] * math.cos(t), B[1] + B[2] * math.sin(t))
           for t in [2 * math.pi * i / 120 for i in range(121)]]
    arc = [p for p in arc if math.hypot(p[0] - ax, p[1] - ay) <= ar + 0.5]
    # split where it leaves the disc
    runs, cur = [], []
    for i, p in enumerate(arc):
        if cur and math.dist(cur[-1], p) > 8:
            runs.append(cur)
            cur = []
        cur.append(p)
    runs.append(cur)
    d.lines(runs)
    d.group('mid')
    d.text(x0 + S - 8, y0 + 16, 'E', anchor='end')
    d.text(A[0] - A[2] * 0.55, A[1] + 3, 'A')
    d.text(B[0] + B[2] * 0.55, B[1] - B[2] * 0.3, 'B')
    d.text(ax - ar * 0.5, ay + 3, 'A')
    d.text(ax, ay + ar + 22, 'P(AB) / P(A)', size=8)
    d.text(x0, y0 + S + 18, 'P(E) = 1', size=8, anchor='start')
    return d


def monte_carlo():
    """Random points in the unit square, counted inside the quarter circle:
    the fraction inside is pi/4. The same kind of run as the reading's table."""
    d = D()
    x0, y0, S = 30, 262, 220                # the square's lower-left corner and side
    rng = random.Random(2026)
    pts = [(rng.random(), rng.random()) for _ in range(300)]
    P = lambda u, v: (x0 + S * u, y0 - S * v)
    d.group('thin')
    d.lines([[P(i / 5, 0), P(i / 5, 1)] for i in range(1, 5)] +
            [[P(0, i / 5), P(1, i / 5)] for i in range(1, 5)])
    # the running estimate's axes, right
    gx0, gx1, gy0, gy1 = 280, 385, 230, 60
    d.line((gx0, gy1), (gx0, gy0), (gx1, gy0))
    d.group()
    d.line(P(0, 0), P(1, 0), P(1, 1), P(0, 1), closed=True)
    d.line(*[P(math.cos(a), math.sin(a)) for a in [math.pi / 2 * i / 90 for i in range(91)]])
    d.group('mid')
    ins = [P(u, v) for u, v in pts if u * u + v * v <= 1]
    out = [P(u, v) for u, v in pts if u * u + v * v > 1]
    d.path(_dots(ins, 1.3))
    d.lines([[(x - 1.6, y - 1.6), (x + 1.6, y + 1.6)] for x, y in out] +
            [[(x - 1.6, y + 1.6), (x + 1.6, y - 1.6)] for x, y in out])
    # the running estimate of pi from the same points, on a log scale of n
    lo, hi = 2.6, 3.8
    GY = lambda v: gy0 + (gy1 - gy0) * (v - lo) / (hi - lo)
    GX = lambda n: gx0 + (gx1 - gx0) * math.log10(n) / math.log10(len(pts))
    segs, x = [], gx0
    while x < gx1:
        segs.append([(x, GY(math.pi)), (min(x + 4, gx1), GY(math.pi))])
        x += 7
    d.lines(segs)
    d.group()
    run, inside = [], 0
    for i, (u, v) in enumerate(pts, 1):
        inside += u * u + v * v <= 1
        if i >= 5:
            est = 4 * inside / i
            run.append((GX(i), GY(min(max(est, lo), hi))))
    d.line(*run)
    d.group('mid')
    d.text(x0 + S / 2, y0 + 16, '1', size=8)
    d.text(x0 - 10, y0 - S / 2 + 3, '1', size=8)
    d.text(x0 + S / 2, y0 - S - 8, 'INSIDE THE ARC: π/4 OF THE SQUARE', size=7)
    d.text(gx1, GY(math.pi) - 6, 'π', size=9, anchor='end')
    d.text(gx0, gy0 + 13, '5', size=7)
    d.text(gx1, gy0 + 13, '300', size=7)
    d.text((gx0 + gx1) / 2, gy0 + 26, 'POINTS', size=7)
    d.text((gx0 + gx1) / 2, gy1 - 10, '4 × INSIDE / ALL', size=7)
    return d


PLATES = {
    'markov-chains': markov_chains,
    'wiener-measure': wiener_measure,
    'kolmogorov': kolmogorov,
    'monte-carlo': monte_carlo,
}
