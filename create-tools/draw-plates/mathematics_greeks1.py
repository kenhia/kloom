"""Plates for the mathematics subject's Greeks, part 1 (sprint 024):
the incommensurable diagonal, Euclid's Elements, Archimedes' circle."""
import math
from plates import D


def _meet(p, d, q, e):
    """Where the line p + t·d meets the line q + s·e."""
    det = d[0] * -e[1] - d[1] * -e[0]
    t = ((q[0] - p[0]) * -e[1] - (q[1] - p[1]) * -e[0]) / det
    return p[0] + t * d[0], p[1] + t * d[1]


def euclid_elements():
    """Proposition I.1 (the two circles and the equilateral triangle), and
    beside it the fifth postulate: two lines cut by a third, meeting on the
    side where the inner angles fall short of two right angles."""
    d = D()
    ax, bx, y, r = 95, 170, 165, 75
    cy = y - math.sqrt(r * r - (r / 2) ** 2)
    cx = (ax + bx) / 2
    # postulate 5: transversal g through two lines h, k that lean together
    g0, g1 = (296, 70), (306, 250)
    h0, hd = (262, 130), (1, 0.30)
    k0, kd = (262, 200), (1, -0.25)
    gd = (g1[0] - g0[0], g1[1] - g0[1])
    P = _meet(g0, gd, h0, hd)
    Q = _meet(g0, gd, k0, kd)
    S = _meet(h0, hd, k0, kd)
    d.group('thin')
    # the given line produced, and the two circles of the construction
    d.line((ax - r - 8, y), (bx + r + 8, y))
    d.circle(ax, y, r)
    d.circle(bx, y, r)
    # the two lines produced until they meet
    d.line(P, S)
    d.line(Q, S)
    d.group()
    d.line((ax, y), (bx, y), (cx, cy), closed=True)
    d.line(g0, g1)
    d.line(h0, (P[0] + 22, P[1] + 22 * hd[1]))
    d.line(k0, (Q[0] + 22, Q[1] + 22 * kd[1]))
    d.group('mid')
    # the inner angles on the right of the transversal
    ga = math.degrees(math.atan2(gd[1], gd[0]))
    ha = math.degrees(math.atan2(hd[1], hd[0]))
    ka = math.degrees(math.atan2(kd[1], kd[0]))
    d.arc(P[0], P[1], 13, ha, ga, n=16)
    d.arc(Q[0], Q[1], 13, ka, ga - 180, n=16)
    # points of the construction
    for px, py in [(ax, y), (bx, y), (cx, cy), (ax - r, y), (bx + r, y), S]:
        d.circle(px, py, 1.8)
    d.group('mid')
    d.text(ax - 6, y + 14, 'A')
    d.text(bx + 6, y + 14, 'B')
    d.text(cx, cy - 8, 'C')
    d.text(ax - r - 10, y - 6, 'D')
    d.text(bx + r + 10, y - 6, 'E')
    d.text(S[0], S[1] - 8, 'S')
    d.text(P[0] + 22, P[1] + 20, 'α', size=8)
    d.text(Q[0] + 20, Q[1] - 12, 'β', size=8)
    d.text(cx, 272, 'I.1', size=7)
    d.text(325, 272, 'POSTULATE 5', size=7)
    return d


def _descent(A, B, C, steps):
    """Apostol's descent: triangles (apex, right-angle vertex) sharing the
    far vertex C. Swing the leg from the apex onto the hypotenuse (point D),
    raise the perpendicular at D to meet the other leg (point F); FDC is the
    next, smaller triangle. Returns [(apex, right, D, F)] for each step."""
    out = []
    P, R = A, B
    for _ in range(steps):
        leg = math.dist(P, R)
        hyp = math.dist(P, C)
        u = ((C[0] - P[0]) / hyp, (C[1] - P[1]) / hyp)
        Dp = (P[0] + leg * u[0], P[1] + leg * u[1])
        # F on RC with FD perpendicular to PC: F = C + t(R - C), |CF| = |CD|·√2
        cd = hyp - leg
        v = ((R[0] - C[0]) / math.dist(R, C), (R[1] - C[1]) / math.dist(R, C))
        F = (C[0] + cd * math.sqrt(2) * v[0], C[1] + cd * math.sqrt(2) * v[1])
        out.append((P, R, Dp, F))
        P, R = F, Dp
    return out


def _clip(pts, cx, cy, r, step=0.5):
    """The runs of a polyline that lie inside a circle, found by sampling."""
    runs, cur = [], []
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(math.dist(a, b) / step))
        for i in range(n + 1):
            q = (a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n)
            if math.dist(q, (cx, cy)) <= r:
                cur.append(q)
            elif cur:
                runs.append(cur)
                cur = []
    if cur:
        runs.append(cur)
    return [run for run in runs if len(run) > 1]


def incommensurable():
    """Apostol's proof that √2 is irrational: a right isosceles triangle,
    its leg swung onto the hypotenuse, leaves a smaller triangle of the
    same shape at the far corner, and so on without end; an inset magnifies
    the corner."""
    d = D()
    A, B, C = (60, 60), (60, 260), (260, 260)
    steps = _descent(A, B, C, 8)
    Z = (C[0] - 13, C[1] - 5)                  # the corner at C, magnified in an inset
    ix, iy, ir, zr = 318, 100, 66, 16.5
    k = ir / zr
    def z(p):
        return ix + (p[0] - Z[0]) * k, iy + (p[1] - Z[1]) * k
    def arc_pts(P, R, Dp, n=24):
        r = math.dist(P, R)
        a0 = math.atan2(R[1] - P[1], R[0] - P[0])
        a1 = math.atan2(Dp[1] - P[1], Dp[0] - P[0])
        return [(P[0] + r * math.cos(a0 + (a1 - a0) * i / n), P[1] + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    def inset(pts):
        return _clip([z(q) for q in pts], ix, iy, ir)
    d.group('thin')
    # the compass swings, the detail circle at C, and its leader to the inset
    for P, R, Dp, F in steps[:2]:
        d.line(*arc_pts(P, R, Dp))
    d.lines([run for P, R, Dp, F in steps for run in inset(arc_pts(P, R, Dp))])
    d.circle(Z[0], Z[1], zr)
    d.circle(ix, iy, ir)
    ang = math.atan2(iy - Z[1], ix - Z[0])
    d.line((Z[0] + zr * math.cos(ang), Z[1] + zr * math.sin(ang)),
           (ix - ir * math.cos(ang), iy - ir * math.sin(ang)))
    d.group()
    d.line(A, B, C, closed=True)
    d.lines(inset([A, C]) + inset([B, C]))
    d.group('mid')
    # each new triangle's perpendicular, full size and magnified
    d.lines([[Dp, F] for P, R, Dp, F in steps[:3]])
    d.lines([run for P, R, Dp, F in steps for run in inset([Dp, F])])
    # right-angle marks at B and at the first D
    s = 8
    d.line((B[0], B[1] - s), (B[0] + s, B[1] - s), (B[0] + s, B[1]))
    P, R, Dp, F = steps[0]
    u = ((C[0] - Dp[0]) / math.dist(C, Dp), (C[1] - Dp[1]) / math.dist(C, Dp))
    w = ((F[0] - Dp[0]) / math.dist(F, Dp), (F[1] - Dp[1]) / math.dist(F, Dp))
    d.line((Dp[0] + s * u[0], Dp[1] + s * u[1]), (Dp[0] + s * (u[0] + w[0]), Dp[1] + s * (u[1] + w[1])),
           (Dp[0] + s * w[0], Dp[1] + s * w[1]))
    d.group('mid')
    d.text(A[0] - 10, A[1] + 3, 'A')
    d.text(B[0] - 10, B[1] + 3, 'B')
    d.text(C[0] + 8, C[1] + 12, 'C')
    d.text(Dp[0] + 9, Dp[1] - 4, 'D')
    d.text(F[0], F[1] + 14, 'F')
    d.text(ix, iy + ir + 16, '×4', size=7)
    return d


def archimedes_circle():
    """Measurement of a Circle, Proposition 3: the circle between inscribed
    and circumscribed regular polygons of 6, 12 and 24 sides, with the
    radii that bisect the angle at the centre; beside it the two bounds,
    computed for 6 to 96 sides, closing on π."""
    d = D()
    cx, cy, r = 140, 150, 105
    def poly(n, R, rot=-90):
        return [(cx + R * math.cos(math.radians(rot + 360 * i / n)),
                 cy + R * math.sin(math.radians(rot + 360 * i / n))) for i in range(n)]
    # the plot of the bounds: x by doublings, y by value
    ns = [6, 12, 24, 48, 96]
    px0, px1, py0, py1 = 285, 385, 250, 60
    lo, hi = 2.98, 3.48
    def X(i):
        return px0 + (px1 - px0) * i / 4
    def Y(v):
        return py0 + (py1 - py0) * (v - lo) / (hi - lo)
    ins = [n * math.sin(math.pi / n) for n in ns]
    out = [n * math.tan(math.pi / n) for n in ns]
    d.group('thin')
    # the angle at the centre: a radius to a side's midpoint, halved again and again
    base = -90
    segs = []
    for k in range(5):
        a = math.radians(base + 30 / 2 ** k)
        segs.append([(cx, cy), (cx + r / math.cos(math.radians(30 / 2 ** k)) * math.cos(a),
                                cy + r / math.cos(math.radians(30 / 2 ** k)) * math.sin(a))])
    d.lines(segs)
    d.line((cx, cy), (cx, cy - r))
    # the plot's axes and the line of π
    d.line((px0, py1 - 6), (px0, py0), (px1 + 6, py0))
    d.line((px0, Y(math.pi)), (px1 + 6, Y(math.pi)))
    d.lines([[(X(i), py0), (X(i), py0 + 4)] for i in range(5)])
    d.group()
    d.circle(cx, cy, r)
    d.group('mid')
    for n in (6, 12, 24):
        d.line(*poly(n, r, -90 + 180 / n), closed=True)
        d.line(*poly(n, r / math.cos(math.pi / n), -90 + 180 / n), closed=True)
    d.line(*[(X(i), Y(v)) for i, v in enumerate(ins)])
    d.line(*[(X(i), Y(v)) for i, v in enumerate(out)])
    for i in range(5):
        d.circle(X(i), Y(ins[i]), 1.6)
        d.circle(X(i), Y(out[i]), 1.6)
    d.group('mid')
    d.text(cx, cy + 4, 'O', size=7)
    for i, n in enumerate(ns):
        d.text(X(i), py0 + 14, str(n), size=7)
    d.text(px1 + 10, Y(math.pi) + 3, 'π', anchor='start')
    d.text((px0 + px1) / 2, 276, 'SIDES', size=7)
    return d


PLATES = {
    'archimedes-circle': archimedes_circle,
    'incommensurable': incommensurable,
    'euclid-elements': euclid_elements,
}
