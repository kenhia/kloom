"""Plates for the mathematics subject's segment The new mathematics (sprint 024)."""
import math
from plates import D


def _offset(pts, d):
    """A polyline offset sideways by d (left of the direction of travel)."""
    out = []
    for i, (x, y) in enumerate(pts):
        x0, y0 = pts[max(i - 1, 0)]
        x1, y1 = pts[min(i + 1, len(pts) - 1)]
        dx, dy = x1 - x0, y1 - y0
        n = math.hypot(dx, dy) or 1
        out.append((x - dy / n * d, y + dx / n * d))
    return out


def _bezier(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]


def cardano_cubic():
    """x³ = 15x + 4: the cube and the line cross three times; Cardano's dissected cube beside."""
    d = D()
    ox, oy, sx, sy = 212, 158, 38, 1.15          # origin and scale: x in [-4.6, 4.6], y in [-100, 100]
    P = lambda x, y: (ox + sx * x, oy - sy * y)
    roots = [4, -2 + math.sqrt(3), -2 - math.sqrt(3)]
    d.group('thin')
    d.line(P(-4.8, 0), P(4.8, 0))
    d.line(P(0, -108), P(0, 110))
    ticks = [[P(k, 0), (P(k, 0)[0], P(k, 0)[1] + 3)] for k in range(-4, 5) if k]
    d.lines(ticks)
    # the roots dropped to the axis
    d.lines([[P(r, r ** 3), P(r, 0)] for r in roots])
    d.group()
    xs = [-4.55 + i * 9.05 / 120 for i in range(121)]
    d.line(*[P(x, x ** 3) for x in xs])
    d.group('mid')
    d.line(P(-4.4, 15 * -4.4 + 4), P(4.55, 15 * 4.55 + 4))
    # Cardano's cube, cut at a and b on every edge: a³ + b³ and six solids
    cx, cy, s, a = 72, 58, 42, 0.62
    iso = lambda x, y, z: (cx + (x - y) * s * 0.866, cy + (x + y) * s * 0.5 - z * s)
    edges = [((0, 0, 1), (1, 0, 1)), ((1, 0, 1), (1, 1, 1)), ((1, 1, 1), (0, 1, 1)), ((0, 1, 1), (0, 0, 1)),
             ((1, 0, 1), (1, 0, 0)), ((1, 1, 1), (1, 1, 0)), ((0, 1, 1), (0, 1, 0)),
             ((1, 0, 0), (1, 1, 0)), ((1, 1, 0), (0, 1, 0))]
    d.group()
    d.lines([[iso(*p), iso(*q)] for p, q in edges])
    d.group('mid')
    cuts = [[iso(a, 0, 1), iso(a, 1, 1)], [iso(0, a, 1), iso(1, a, 1)],       # top face
            [iso(1, a, 1), iso(1, a, 0)], [iso(1, 0, 1 - a), iso(1, 1, 1 - a)],  # right face
            [iso(a, 1, 1), iso(a, 1, 0)], [iso(0, 1, 1 - a), iso(1, 1, 1 - a)]]  # front face
    d.lines(cuts)
    for r in roots:
        x, y = P(r, r ** 3)
        d.circle(x, y, 3)
    d.group('mid')
    d.text(P(4, 0)[0], P(4, 0)[1] + 14, '4')
    d.text(P(roots[1], 0)[0] + 22, P(0, 0)[1] + 14, '-2+√3', size=7)
    d.text(P(roots[2], 0)[0], P(0, 0)[1] - 8, '-2-√3', size=7)
    d.text(P(3.2, 45)[0] - 8, P(3.2, 45)[1] - 22, 'x³', anchor='end')
    d.text(P(2.0, 34)[0], P(2.0, 34)[1] - 10, '15x+4', anchor='end')
    d.text(cx, cy + 58, '(a+b)³ = a³+b³+3ab(a+b)', size=7)
    d.text(ox, 290, 'x³ = 15x + 4', size=7)
    return d


def descartes_geometry():
    """La Géométrie's first two figures: multiplying lengths, and a square root."""
    d = D()
    u = 38                                   # the unit, AB and FG
    # Fig. 1: B at the vertex, A and D along one line, C and E along another
    B = (40, 250)
    t1, t2 = math.radians(0), math.radians(-58)
    r1 = lambda k: (B[0] + k * u * math.cos(t1), B[1] + k * u * math.sin(t1))
    r2 = lambda k: (B[0] + k * u * math.cos(t2), B[1] + k * u * math.sin(t2))
    A, Dp = r1(1), r1(2)                     # AB = 1, BD = 2
    C, E = r2(1.5), r2(3)                    # BC = 1.5, so BE = 3
    d.group('thin')
    d.line(B, r1(3.9))
    d.line(B, r2(3.8))
    # Fig. 2: F G H on a line, FG = 1, GH = 4; the circle on FH; GI upright at G
    v = 30
    F = (208, 250)
    G = (F[0] + v, F[1])
    H = (G[0] + 4 * v, F[1])
    K = ((F[0] + H[0]) / 2, F[1])
    R = (H[0] - F[0]) / 2
    I = (G[0], F[1] - math.sqrt(R * R - (G[0] - K[0]) ** 2))
    d.line((F[0] - 8, F[1]), (H[0] + 8, F[1]))
    d.line(K, I)
    d.group()
    d.line(A, C)
    d.line(Dp, E)
    d.arc(K[0], K[1], R, 180, 360, n=72)
    d.line(G, I)
    d.group('mid')
    for p in (A, Dp, C, E, B, F, G, H, K, I):
        d.circle(p[0], p[1], 1.8)
    # tick marks for the unit on each figure
    d.lines([[(A[0], A[1] - 4), (A[0], A[1] + 4)], [(G[0], G[1] - 4), (G[0], G[1] + 4)]])
    d.group('mid')
    lab = lambda p, s, dx, dy: d.text(p[0] + dx, p[1] + dy, s)
    lab(B, 'B', -8, 12); lab(A, 'A', 0, 14); lab(Dp, 'D', 0, 14); lab(C, 'C', -9, 0); lab(E, 'E', -9, 0)
    lab(F, 'F', 0, 14); lab(G, 'G', 0, 14); lab(H, 'H', 0, 14); lab(K, 'K', 0, 14); lab(I, 'I', 0, -7)
    d.text((B[0] + A[0]) / 2, B[1] - 5, '1', size=7)
    d.text((F[0] + G[0]) / 2, F[1] - 5, '1', size=7)
    d.text((G[0] + H[0]) / 2 + 20, F[1] - 5, '4', size=7)
    d.text(G[0] + 5, (G[1] + I[1]) / 2, '2', size=7, anchor='start')
    d.text(E[0] + 10, E[1] + 4, 'BE = BD·BC', size=7, anchor='start')
    d.text(B[0] + 70, 285, 'FIG. 1 · MULTIPLICATION', size=7)
    d.text(K[0], 285, 'FIG. 2 · SQUARE ROOT', size=7)
    return d


def calculus():
    """The area under y = x² grows at the rate x²: the area curve's slope is the curve's height."""
    d = D()
    x0l, sx = 70, 140                         # x from 0 to 2 across 280 px
    ya, ka = 132, 36                          # top panel: A = x³/3
    yb, kb = 268, 28                          # bottom panel: y = x²
    X = lambda x: x0l + sx * x
    top = lambda x, v: (X(x), ya - ka * v)
    bot = lambda x, v: (X(x), yb - kb * v)
    a = 1.5
    d.group('thin')
    d.line(top(0, 0), top(2.1, 0)); d.line(top(0, 0), top(0, 3.1))
    d.line(bot(0, 0), bot(2.1, 0)); d.line(bot(0, 0), bot(0, 4.3))
    # the rectangles of the sum under the curve, and the instant x = a through both panels
    n = 12
    strips = []
    for i in range(n):
        xl, xr = a * i / n, a * (i + 1) / n
        strips.append([bot(xl, 0), bot(xl, xl * xl), bot(xr, xl * xl), bot(xr, 0)])
    d.lines(strips)
    d.line(top(a, 0), bot(a, 0))
    d.group()
    xs = [2 * i / 80 for i in range(81)]
    d.line(*[top(x, x ** 3 / 3) for x in xs])
    d.line(*[bot(x, x * x) for x in xs])
    d.group('mid')
    # the tangent to the area curve at a, and its slope triangle: run 1/2, rise a²/2
    A0 = a ** 3 / 3
    d.line(top(a - 0.4, A0 - 0.4 * a * a), top(a + 0.5, A0 + 0.5 * a * a))
    d.line(top(a, A0), top(a + 0.5, A0), top(a + 0.5, A0 + 0.5 * a * a))
    # the curve's height at a, marked beside the instant
    d.line(bot(a + 0.04, 0), bot(a + 0.04, a * a))
    d.lines([[bot(a + 0.01, a * a), bot(a + 0.07, a * a)]])
    d.circle(*top(a, A0), 2.2)
    d.circle(*bot(a, a * a), 2.2)
    d.group('mid')
    d.text(*top(2.0, 3.0), 'x³/3', anchor='end')
    d.text(*bot(1.62, 4.1), 'x²', anchor='end')
    d.text(X(a + 0.25), top(0, A0)[1] + 12, 'SLOPE 2.25', size=7)
    d.text(bot(a + 0.08, 0)[0], bot(0, a * a / 2)[1] + 3, 'HEIGHT 2.25', size=7, anchor='start')
    d.text(X(a), yb + 13, 'x = 1.5', size=7)
    d.text(X(0.7), top(0, 2.6)[1], 'AREA', size=7)
    d.text(X(0.75), bot(0, 3.4)[1], 'CURVE', size=7)
    return d


def konigsberg():
    """Euler's seven bridges: the river, the island and the bridges, and the graph drawn later beside them."""
    d = D()
    w = 7                                         # half the channel's width
    # river centre lines (after Euler's Fig. 1): one river from the west splits round the island A,
    # a cross channel east of A, and two branches running off to the north-east and south-east
    north = _bezier((20, 150), (70, 62), (190, 92))
    south = _bezier((20, 150), (70, 238), (190, 208))
    cross = [(190, 92), (190, 208)]
    ne = _bezier((190, 92), (215, 80), (245, 40), n=12)
    se = _bezier((190, 208), (215, 220), (245, 260), n=12)
    west = [(-4, 150), (20, 150)]
    d.group('thin')
    d.lines([north, south, cross, ne, se, west])
    d.group()
    banks = []
    for c in (north, south, ne, se, west, cross):
        banks += [_offset(c, w), _offset(c, -w)]
    d.lines(banks)
    # bridges: two short rails across the channel at a point of a centre line
    def bridge(pts, i):
        (x0, y0), (x1, y1) = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        dx, dy = x1 - x0, y1 - y0
        n = math.hypot(dx, dy)
        tx, ty, nx, ny = dx / n, dy / n, -dy / n, dx / n
        x, y = pts[i]
        return [[(x + tx * s - nx * (w + 3), y + ty * s - ny * (w + 3)),
                 (x + tx * s + nx * (w + 3), y + ty * s + ny * (w + 3))] for s in (-3, 3)]
    crossv = [(190, 92 + 116 * i / 20) for i in range(21)]
    spots = {'c': (north, 9), 'd': (north, 17), 'a': (south, 9), 'b': (south, 17),
             'e': (crossv, 10), 'g': (ne, 5), 'f': (se, 5)}
    d.group('mid')
    rails = []
    for k, (pts, i) in spots.items():
        rails += bridge(pts, i)
    d.lines(rails)
    # the graph: a vertex for each land, an edge for each bridge
    V = {'A': (300, 150), 'C': (348, 58), 'B': (348, 242), 'D': (388, 150)}
    d.group()
    edges = [_bezier(V['A'], (312, 94), V['C']), _bezier(V['A'], (336, 114), V['C']),
             _bezier(V['A'], (312, 206), V['B']), _bezier(V['A'], (336, 186), V['B']),
             [V['A'], V['D']], [V['C'], V['D']], [V['B'], V['D']]]
    d.lines(edges)
    d.group('mid')
    for p in V.values():
        d.circle(p[0], p[1], 3.5)
    d.group('mid')
    for k, (x, y) in {'A': (108, 154), 'C': (108, 42), 'B': (108, 266), 'D': (228, 154)}.items():
        d.text(x, y, k)
    for k, (pts, i) in spots.items():
        x, y = pts[i]
        off = {'c': (0, -14), 'd': (0, -13), 'a': (0, 20), 'b': (0, 19), 'e': (-14, 3), 'g': (-12, -6), 'f': (-12, 12)}[k]
        d.text(x + off[0], y + off[1], k, size=7)
    deg = {'A': 5, 'B': 3, 'C': 3, 'D': 3}
    for k, (x, y) in V.items():
        dx, dy = {'A': (-12, 4), 'C': (0, -9), 'B': (0, 17), 'D': (0, -9)}[k]
        d.text(x + dx, y + dy, f'{k}{deg[k]}', size=7)
    return d


PLATES = {
    'cardano-cubic': cardano_cubic,
    'descartes-geometry': descartes_geometry,
    'calculus': calculus,
    'konigsberg': konigsberg,
}
