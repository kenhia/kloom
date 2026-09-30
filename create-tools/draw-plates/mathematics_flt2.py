"""Plates for the Fermat's Last Theorem trail, part two (sprint 024): Kummer, modularity, Wiles."""
import math
from plates import D


def kummer_ideals():
    """The numbers a + b√−5 as a lattice in the plane, with the circles of norm a² + 5b².

    No lattice point lies on the circles of norm 2 and 3, so 2, 3 and 1 ± √−5 have no
    smaller factors, and 6 = 2 × 3 = (1 + √−5)(1 − √−5) factors two ways.
    """
    d = D()
    cx, cy, u = 200, 150, 25          # origin, and the length of 1
    v = u * math.sqrt(5)              # the length of √−5
    P = lambda a, b: (cx + a * u, cy - b * v)
    d.group('thin')
    # the axes, and the lattice's rows and columns
    d.line((cx - 7.6 * u, cy), (cx + 7.6 * u, cy))
    d.line((cx, cy - 2.5 * v), (cx, cy + 2.5 * v))
    rows = [[P(-7, b), P(7, b)] for b in (-2, -1, 1, 2)]
    cols = [[P(a, -2), P(a, 2)] for a in range(-7, 8) if a]
    d.lines(rows + cols)
    d.group('thin')
    # the empty circles: no a + b√−5 has norm 2 or 3
    for n in (2, 3):
        d.circle(cx, cy, u * math.sqrt(n))
    d.group()
    # the circles that the factors of 6 lie on: norm 4 (the 2s), 6 (1 ± √−5) and 9 (the 3s)
    for n in (4, 6, 9):
        d.circle(cx, cy, u * math.sqrt(n))
    d.group('mid')
    # every lattice point in view, small
    for a in range(-7, 8):
        for b in range(-2, 3):
            x, y = P(a, b)
            d.circle(x, y, 1.4)
    d.group()
    # the four factors, ringed
    for a, b in ((2, 0), (3, 0), (1, 1), (1, -1)):
        x, y = P(a, b)
        d.circle(x, y, 4.2)
    d.group('mid')
    d.text(P(2, 0)[0] + 3, cy + 16, '2', anchor='middle')
    d.text(P(3, 0)[0] + 8, cy + 16, '3', anchor='middle')
    d.text(P(1, 1)[0] + 8, P(1, 1)[1] - 8, '1+√−5', anchor='start')
    d.text(P(1, -1)[0] + 8, P(1, -1)[1] + 15, '1−√−5', anchor='start')
    # the norms, where each circle crosses the axis on the left
    # the norms, each where its circle crosses a ray to the lower left, fanned out to read
    for n, ang in ((2, 200), (3, 214), (4, 228), (6, 242), (9, 256)):
        r = u * math.sqrt(n)
        a = math.radians(ang)
        d.text(cx + r * math.cos(a) - 3, cy - r * math.sin(a) + 3, str(n), size=6, anchor='end')
    d.text(cx + 7.6 * u, 22, 'N = a² + 5b²', size=7, anchor='end')
    return d


def taniyama_shimura():
    """A Frey-shaped cubic, y² = x(x − 9)(x + 16), built from 3² + 4² = 5², with a chord.

    x and y are scaled differently; an affine map keeps lines lines and tangents tangent,
    so the construction on the drawing is the construction on the curve.
    """
    d = D()
    A, B = 9, 16
    f = lambda x: x * (x - A) * (x + B)
    sx, sy, ox, oy = 8.6, 1.15, 178, 150
    X = lambda x: ox + sx * x
    Y = lambda y: oy - sy * y
    # the egg, between the roots −16 and 0, and the branch from 9
    def branch(x0, x1, n=160):
        up, down = [], []
        for i in range(n + 1):
            # crowd the samples towards the roots, where the curve turns vertical
            t = i / n
            x = x0 + (x1 - x0) * (0.5 - 0.5 * math.cos(math.pi * t))
            y = math.sqrt(max(f(x), 0))
            up.append((X(x), Y(y)))
            down.append((X(x), Y(-y)))
        return up, down
    eu, ed = branch(-B, 0)
    xr = 21.5
    ru, rd = branch(A, xr)
    # a chord through P on the egg and Q on the branch (invented points); R is where it meets the curve again
    xp, xq = -14.0, 14.0
    yp, yq = math.sqrt(f(xp)), math.sqrt(f(xq))
    m = (yq - yp) / (xq - xp)
    # the three x's where the line meets the cubic sum to m² − (coefficient of x²) = m² − (B − A)
    xrr = m * m - (B - A) - xp - xq
    yrr = yp + m * (xrr - xp)
    d.group('thin')
    d.line((X(-18.5), Y(0)), (X(22.5), Y(0)))
    d.line((X(0), Y(-112)), (X(0), Y(112)))
    # the chord, run on past its three points, and the vertical through R to its mirror
    xs = sorted([xp, xq, xrr])
    d.line((X(xs[0] - 1.8), Y(yp + m * (xs[0] - 1.8 - xp))), (X(xs[2] + 1.8), Y(yp + m * (xs[2] + 1.8 - xp))))
    d.line((X(xrr), Y(yrr)), (X(xrr), Y(-yrr)))
    for x in (-B, A):
        d.line((X(x), Y(0) - 4), (X(x), Y(0) + 4))
    d.group()
    d.line(*eu, *reversed(ed[1:-1]), closed=True)
    d.line(*reversed(ru), *rd[1:])
    d.group('mid')
    for x, y in ((xp, yp), (xq, yq), (xrr, yrr)):
        d.circle(X(x), Y(y), 3)
    d.group()
    d.circle(X(xrr), Y(-yrr), 4.2)
    d.group('mid')
    d.text(X(xp) - 8, Y(yp) - 7, 'P', anchor='end')
    d.text(X(xq) + 8, Y(yq) + 4, 'Q', anchor='start')
    d.text(X(xrr) + 8, Y(yrr) + 4, 'R', anchor='start')
    d.text(X(xrr) + 8, Y(-yrr) + 4, 'P+Q', anchor='start')
    d.text(X(-B), Y(0) + 15, '−16', size=7)
    d.text(X(0) - 6, Y(0) + 15, '0', size=7)
    d.text(X(A) - 4, Y(0) + 15, '9', size=7)
    d.text(386, 24, 'y² = x(x − 9)(x + 16)', size=7, anchor='end')
    return d


def wiles():
    """The upper half-plane, tiled by the modular group, and the region that Γ₀(2) folds up.

    The shaded region runs from −½ to ½ above the circles |z ± ½| = ½: its edges are glued,
    the sides by z → z + 1 and the arcs by z → z/(2z + 1), and it closes up into a sphere.
    """
    d = D()
    ox, oy, s = 200, 262, 190          # 0 on the real axis, and the length of 1
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    def semicircle(c, r, a0=0, a1=180, n=64):
        return [(X(c + r * math.cos(math.radians(a0 + (a1 - a0) * i / n))),
                 Y(r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))) for i in range(n + 1)]
    top = 1.28
    d.group('thin')
    d.line((X(-1.02), Y(0)), (X(1.02), Y(0)))
    # the modular group's tiling: the unit circles about the integers, their images in
    # the circles on the Farey fractions, and the vertical lines x = ±½
    arcs = [semicircle(-1, 1, 0, 90), semicircle(0, 1), semicircle(1, 1, 90, 180)]
    for p, q in ((0, 1), (1, 2), (1, 3), (2, 3), (1, 4), (3, 4)):
        # the circle through two Farey neighbours p/q and p'/q' with qp' − pq' = 1
        for pp in range(0, 5):
            for qq in range(1, 6):
                if qq * p - pp * q == -1 and 0 <= pp / qq <= 1 and qq <= 4 and q <= 4:
                    a, b = p / q, pp / qq
                    arcs.append(semicircle((a + b) / 2, (b - a) / 2))
                    arcs.append(semicircle(-(a + b) / 2, (b - a) / 2))
    d.lines(arcs)
    d.lines([[(X(x), Y(0)), (X(x), Y(top))] for x in (-0.5, 0.5)])
    d.group('mid')
    # the modular group's own domain: |x| ≤ ½ above the unit circle
    d.line((X(-0.5), Y(top)), *semicircle(0, 1, 120, 60, 24), (X(0.5), Y(top)))
    d.group()
    # Γ₀(2)'s domain: |x| ≤ ½ above the two circles |z ± ½| = ½, down to the cusp at 0
    left = semicircle(-0.5, 0.5, 90, 0, 40)
    right = semicircle(0.5, 0.5, 180, 90, 40)
    d.line((X(-0.5), Y(top)), *left, *right[1:], (X(0.5), Y(top)))
    d.group('mid')
    for x, y in ((-0.5, 0.5), (0.5, 0.5)):
        d.circle(X(x), Y(y), 3)
    d.circle(X(0), Y(0), 3)
    d.group('mid')
    d.text(X(0), Y(0) + 16, '0', size=8)
    d.text(X(-0.5), Y(0) + 16, '−½', size=7)
    d.text(X(0.5), Y(0) + 16, '½', size=7)
    d.text(X(-1), Y(0) + 16, '−1', size=7)
    d.text(X(1), Y(0) + 16, '1', size=7)
    d.text(X(0.5) + 8, Y(0.5) + 3, '(1+i)/2', size=7, anchor='start')
    d.text(X(0), Y(top) + 12, '∞', size=9)
    d.text(X(0), Y(0.78), 'Γ₀(2)', size=8)
    return d


PLATES = {
    'kummer-ideals': kummer_ideals,
    'taniyama-shimura': taniyama_shimura,
    'wiles': wiles,
}
