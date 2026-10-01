"""physics plates, segment "Particles" and the first half of the Standard Model trail (sprint 021). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def antimatter():
    """Dirac's hole theory beside Anderson's evidence.

    Left: the electron's energy levels, a continuum above +mc² and the filled
    sea below −mc², with the gap of 2mc² between. A gamma ray lifts one
    electron out of the sea; the hole it leaves is the anti-electron.
    Right: a cloud chamber with its lead plate, and a track that crosses the
    plate upward, curving more tightly above it, as in Anderson's photograph
    of 2 August 1932 (63 MeV below the plate and 23 MeV above; the radius of
    curvature is proportional to momentum, so the arcs are in that ratio)."""
    d = D()
    x0, x1 = 40, 210                  # the energy diagram's width
    top, up, lo, bot = 34, 118, 182, 268   # +mc² at y=up, −mc² at y=lo
    # construction: the energy axis, zero, and the dimension of the gap
    d.group('thin')
    d.line((28, bot + 6), (28, top - 8))
    _arrow(d, 28, top - 8, -math.pi / 2, 4)
    d.line((24, 150), (x1 + 4, 150))
    d.lines([[(x1 + 6, up), (x1 + 20, up)], [(x1 + 6, lo), (x1 + 20, lo)], [(x1 + 14, up + 2), (x1 + 14, lo - 2)]])
    _arrow(d, x1 + 14, up + 2, -math.pi / 2, 3)
    _arrow(d, x1 + 14, lo - 2, math.pi / 2, 3)
    # the object: the edges of the two continua, and their levels
    d.group()
    d.line((x0, up), (x1, up))
    d.line((x0, lo), (x1, lo))
    d.group('mid')
    d.lines([[(x0, y), (x1, y)] for y in range(up - 14, top, -14)])
    d.lines([[(x0, y), (x1, y)] for y in range(lo + 14, bot + 1, 14)])
    # the sea: every level below −mc² holds electrons (small circles), but one
    hole = (150, lo + 28)
    for y in range(lo + 14, bot + 1, 14):
        for x in range(x0 + 12, x1 - 5, 22):
            if (x, y) == hole:
                continue
            d.circle(x, y - 4, 2.2)
    # one electron lifted to positive energy, and the gamma ray that lifted it
    d.group()
    e = (150, up - 28)
    d.circle(e[0], e[1] - 4, 3)
    d.circle(hole[0], hole[1] - 4, 5)
    d.line((hole[0] - 3, hole[1] - 4), (hole[0] + 3, hole[1] - 4))
    d.line((hole[0], hole[1] - 7), (hole[0], hole[1] - 1))
    d.line((hole[0], hole[1] - 11), (e[0], e[1] + 1))
    _arrow(d, e[0], e[1] + 1, -math.pi / 2, 4)
    wave = [(x0 + 2 + t, 150 - 14 + 4 * math.sin(t / 3.2)) for t in range(0, 92, 2)]
    d.line(*wave)
    _arrow(d, *wave[-1], 0, 4)
    # right: Anderson's chamber, its lead plate, and the track
    cx, cy, R = 318, 150, 64
    d.group('thin')
    d.circle(cx, cy, R)
    d.line((cx - R - 6, cy), (cx + R + 6, cy))
    d.group()
    d.line((cx - R + 4, cy - 3), (cx + R - 4, cy - 3), (cx + R - 4, cy + 3), (cx - R + 4, cy + 3), closed=True)
    # the track crosses the plate at P heading up and slightly left; it bends to the left
    # (a positive charge in the chamber's field), with radius in the ratio 63 : 23
    P = (cx + 6, cy)
    r_lo, r_hi = 150, 150 * 23 / 63
    h = math.radians(-100)              # heading at the plate (up, a little left)
    def arc(r, s0, s1, sign):
        # centre to the left of the direction of travel
        nx, ny = math.cos(h - sign * math.pi / 2), math.sin(h - sign * math.pi / 2)
        ccx, ccy = P[0] + r * nx, P[1] + r * ny
        a0 = math.atan2(P[1] - ccy, P[0] - ccx)
        pts = []
        for i in range(41):
            s = s0 + (s1 - s0) * i / 40
            a = a0 - s / r
            pts.append((ccx + r * math.cos(a), ccy + r * math.sin(a)))
        return pts
    below = [p for p in arc(r_lo, -80, 0, 1) if math.dist(p, (cx, cy)) < R - 2]
    above = [p for p in arc(r_hi, 0, 80, 1) if math.dist(p, (cx, cy)) < R - 2]
    d.line(*below)
    d.line(*above)
    # labels
    d.group()
    d.text(x0, top - 6, 'E', size=8, anchor='start')
    d.text(x1 - 2, up + 11, '+mc²', size=7, anchor='end')
    d.text(x1 - 2, lo - 5, '−mc²', size=7, anchor='end')
    d.text(x1 + 22, 153, '2mc²', size=7, anchor='start')
    d.text(x0 + 58, 150 - 22, 'γ', size=9, anchor='start')
    d.text(x1 + 6, hole[1] - 1, 'HOLE', size=7, anchor='start')
    d.text(cx, cy + R + 16, 'LEAD PLATE · 6 MM', size=7)
    d.text(cx, cy - R - 10, '23 MEV', size=7)
    d.text(cx + R - 4, cy + R - 10, '63 MEV', size=7, anchor='end')
    d.text(125, 292, 'THE FILLED SEA · DIRAC 1931', size=8)
    d.text(cx, 292, 'PASADENA 1932', size=8)
    return d


# masses in MeV, from the Standard Model and W and Z bosons articles (the quarks'
# are their MS-bar masses); None for the massless and for the neutrinos, whose
# masses are known only to be tiny
SM = [
    [('u', 1.9), ('c', 1320), ('t', 173500), ('g', None)],
    [('d', 4.4), ('s', 87), ('b', 4240), ('γ', None)],
    [('e', 0.511), ('μ', 105.7), ('τ', 1780), ('Z', 91188)],
    [('νe', 0), ('νμ', 0), ('ντ', 0), ('W', 80369)],
]


def standard_model():
    """The particles of the Standard Model in their usual table, three
    generations of quarks and leptons, the force carriers and the Higgs, each
    drawn as a circle whose radius grows with the logarithm of its mass
    (r = 3 + 2.8 log₁₀(m / 0.1 MeV), our scale). The massless photon and gluon
    are crosses; the neutrinos, whose masses are below an electronvolt, dots."""
    d = D()
    x0, y0, dx, dy = 62, 58, 68, 58
    col = [x0 + dx * i for i in range(4)]
    row = [y0 + dy * j for j in range(4)]
    hx = col[3] + dx + 10
    def radius(m):
        return 3 + 2.8 * math.log10(m / 0.1)
    # construction: the grid of the table and the brackets of its families
    d.group('thin')
    d.lines([[(x - dx / 2, y0 - dy / 2 - 6), (x - dx / 2, row[3] + dy / 2)] for x in col[:3] + [col[3]]])
    d.line((col[2] + dx / 2, y0 - dy / 2 - 6), (col[2] + dx / 2, row[3] + dy / 2))
    d.lines([[(col[0] - dx / 2, y - dy / 2), (col[3] + dx / 2, y - dy / 2)] for y in row] +
            [[(col[0] - dx / 2, row[3] + dy / 2), (col[3] + dx / 2, row[3] + dy / 2)]])
    d.lines([[(col[0] - dx / 2 - 8, row[0] - dy / 2 + 4), (col[0] - dx / 2 - 12, row[0] - dy / 2 + 4),
              (col[0] - dx / 2 - 12, row[1] + dy / 2 - 4), (col[0] - dx / 2 - 8, row[1] + dy / 2 - 4)],
             [(col[0] - dx / 2 - 8, row[2] - dy / 2 + 4), (col[0] - dx / 2 - 12, row[2] - dy / 2 + 4),
              (col[0] - dx / 2 - 12, row[3] + dy / 2 - 4), (col[0] - dx / 2 - 8, row[3] + dy / 2 - 4)]])
    d.circle(hx, row[1] + dy / 2, 36)
    # the object: the particles
    d.group()
    labels = []
    for j, r in enumerate(SM):
        for i, (name, m) in enumerate(r):
            x, y = col[i], row[j] - 4
            if m is None:
                d.lines([[(x - 5, y - 5), (x + 5, y + 5)], [(x - 5, y + 5), (x + 5, y - 5)]])
            elif m == 0:
                d.circle(x, y, 1.2)
            else:
                d.circle(x, y, radius(m))
            labels.append((x, row[j] + dy / 2 - 5, name))
    d.circle(hx, row[1] + dy / 2 - 4, radius(125090))
    labels.append((hx, row[1] + dy / 2 + 32, 'H'))
    # the scale: rings for 1 MeV, 1 GeV and 100 GeV
    d.group('mid')
    x = hx - 30
    for m in (1, 1000, 100000):
        x += radius(m)
        d.circle(x, row[3] + 8, radius(m))
        x += radius(m) + 3
    # labels
    d.group()
    for x, y, s in labels:
        d.text(x, y, s, size=8)
    d.text(col[0], 20, 'I', size=7)
    d.text(col[1], 20, 'II', size=7)
    d.text(col[2], 20, 'III', size=7)
    d.text(col[3], 20, 'FORCE', size=7)
    d.text(hx, row[1] - 30, 'HIGGS', size=7)
    d.text(col[0] - dx / 2 - 16, row[0] + dy / 2 + 3, 'Q', size=7, anchor='end')
    d.text(col[0] - dx / 2 - 16, row[2] + dy / 2 + 3, 'L', size=7, anchor='end')
    d.text(hx, row[3] + 44, '1 MEV · 1 GEV · 100 GEV', size=6)
    d.text(200, 292, 'THREE GENERATIONS · FOUR CARRIERS · ONE SCALAR', size=7)
    return d


def neutrino():
    """The beta spectrum that needed the neutrino.

    If a nucleus emitted only an electron, every electron would carry the same
    energy Q (the line at the right). Measured, the electrons come out with
    every energy from zero to Q (the curve, the allowed shape
    N(T) ∝ p E (Q − T)², with T and Q in units of the electron's rest energy;
    Q = 2 is our choice). Inset: two bodies fly apart back to back; three
    close a triangle of momenta."""
    d = D()
    ox, oy, w, h = 46, 250, 240, 190
    Q = 2.0
    def n(T):
        E = T + 1
        p = math.sqrt(E * E - 1)
        return p * E * (Q - T) ** 2
    Ts = [Q * i / 120 for i in range(121)]
    peak = max(n(T) for T in Ts)
    pts = [(ox + w * T / Q, oy - 0.62 * h * n(T) / peak) for T in Ts]
    # construction: axes, and the mean energy's line
    d.group('thin')
    d.line((ox, oy - h - 6), (ox, oy), (ox + w + 16, oy))
    _arrow(d, ox + w + 16, oy, 0, 4)
    _arrow(d, ox, oy - h - 6, -math.pi / 2, 4)
    mean = sum(T * n(T) for T in Ts) / sum(n(T) for T in Ts)
    d.line((ox + w * mean / Q, oy), (ox + w * mean / Q, oy - 0.62 * h * n(mean) / peak))
    d.lines([[(ox + w * T / Q, oy), (ox + w * T / Q, oy + 4)] for T in (0.5, 1, 1.5)])
    # the object: the measured continuum
    d.group()
    d.line(*pts)
    # the two-body expectation: one sharp line at Q
    d.group('mid')
    d.line((ox + w, oy), (ox + w, oy - h + 8))
    d.line((ox + w - 3, oy - h + 8), (ox + w + 3, oy - h + 8))
    # inset: momenta, two bodies and three
    bx, by = 346, 70
    d.group('thin')
    d.circle(bx, by, 2)
    d.circle(bx, by + 100, 2)
    d.group()
    d.line((bx, by), (bx - 30, by))
    _arrow(d, bx - 30, by, math.pi, 4)
    d.line((bx, by), (bx + 30, by))
    _arrow(d, bx + 30, by, 0, 4)
    A, B, C = (bx, by + 100), (bx - 34, by + 84), (bx + 26, by + 72)
    d.line(A, B)
    _arrow(d, *B, math.atan2(B[1] - A[1], B[0] - A[0]), 4)
    d.line(A, C)
    _arrow(d, *C, math.atan2(C[1] - A[1], C[0] - A[0]), 4)
    D3 = (3 * A[0] - B[0] - C[0], 3 * A[1] - B[1] - C[1])
    d.group('mid')
    d.line(A, D3)
    _arrow(d, *D3, math.atan2(D3[1] - A[1], D3[0] - A[0]), 4)
    # labels
    d.group()
    d.text(ox + 6, oy - h - 2, 'ELECTRONS', size=7, anchor='start')
    d.text(ox + w, oy + 14, 'Q', size=8)
    d.text(ox, oy + 14, '0', size=8)
    d.text(ox + w - 6, oy - h + 4, 'IF TWO BODIES', size=7, anchor='end')
    d.text(ox + w * mean / Q + 4, oy - 20, 'MEAN', size=7, anchor='start')
    d.text(bx - 30, by - 8, 'NUCLEUS', size=6, anchor='middle')
    d.text(bx + 30, by - 8, 'e', size=8)
    d.text(B[0] - 4, B[1] - 6, 'NUCLEUS', size=6, anchor='middle')
    d.text(C[0] + 4, C[1] - 6, 'e', size=8)
    d.text(D3[0] + 8, D3[1] + 4, 'ν', size=9, anchor='start')
    d.text(ox + w / 2, 292, 'ELECTRON ENERGY · BETA DECAY', size=8)
    return d


def quarks():
    """The baryon decuplet of the Eightfold Way, drawn as a triangle.

    Charge runs along each row and strangeness down the rows, with each row
    about 150 MeV heavier than the one above; the apex, strangeness −3, was
    empty when Gell-Mann drew it in 1962. Each node carries its three quarks."""
    d = D()
    cx, top, s = 200, 50, 60             # spacing between nodes
    rowh = s * math.sqrt(3) / 2
    rows = [
        ['ddd', 'udd', 'uud', 'uuu'],
        ['dds', 'uds', 'uus'],
        ['dss', 'uss'],
        ['sss'],
    ]
    pos = {}
    for j, r in enumerate(rows):
        y = top + j * rowh
        for i, q in enumerate(r):
            x = cx + (i - (len(r) - 1) / 2) * s
            pos[(j, i)] = (x, y)
    # construction: the triangular lattice and the strangeness axis
    d.group('thin')
    A, B, C = pos[(0, 0)], pos[(0, 3)], pos[(3, 0)]
    d.line(A, B, C, closed=True)
    d.lines([[pos[(j, 0)], pos[(j, len(rows[j]) - 1)]] for j in (1, 2)])
    d.lines([[pos[(0, i)], pos[(3 - i, i)]] for i in (1, 2)] +
            [[pos[(0, k)], pos[(k, 0)]] for k in (1, 2)])
    d.line((36, top - 10), (36, top + 3 * rowh + 10))
    d.lines([[(32, top + j * rowh), (40, top + j * rowh)] for j in range(4)])
    # the object: the ten particles
    d.group()
    for (j, i), (x, y) in pos.items():
        if j == 3:
            continue
        d.circle(x, y, 13)
    ox, oy = pos[(3, 0)]
    d.circle(ox, oy, 13)
    d.group('mid')
    d.circle(ox, oy, 18)
    # labels
    d.group()
    for (j, i), (x, y) in pos.items():
        d.text(x, y + 3, rows[j][i], size=7)
    names = ['Δ', 'Σ*', 'Ξ*', 'Ω⁻']
    for j in range(4):
        d.text(28, top + j * rowh + 3, str(-j), size=7, anchor='end')
        x = pos[(j, len(rows[j]) - 1)][0] + 26
        d.text(x, top + j * rowh + 3, names[j], size=9, anchor='start')
    d.text(36, top - 18, 'S', size=7)
    d.text(ox + 26, oy + 18, 'PREDICTED 1962', size=7, anchor='start')
    d.text(ox + 26, oy + 28, 'FOUND 1964', size=7, anchor='start')
    d.text(200, 292, 'THE BARYON DECUPLET · SPIN 3/2', size=8)
    return d


PLATES = {
    'antimatter': antimatter,
    'standard-model': standard_model,
    'neutrino': neutrino,
    'quarks': quarks,
}
