"""Plates for the mathematics subject's Algebra segment, part two (sprint 024):
matrices and the Monster."""
import math
from plates import D, SOLIDS, rot, wire


def _arrow(d, p, q, head=5):
    """A line from p to q with an open arrowhead at q."""
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    a1, a2 = ang + math.radians(155), ang - math.radians(155)
    d.line(p, q)
    d.line((q[0] + head * math.cos(a1), q[1] + head * math.sin(a1)), q,
           (q[0] + head * math.cos(a2), q[1] + head * math.sin(a2)))


def matrices():
    """The unit square carried by a shear S and a quarter turn R, in both orders:
    RS (shear, then turn) and SR (turn, then shear) land it in different places."""
    d = D()
    S = ((1, 1), (0, 1))
    R = ((0, -1), (1, 0))

    def mul(A, B):
        return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))

    def apply(M, p):
        return (M[0][0] * p[0] + M[0][1] * p[1], M[1][0] * p[0] + M[1][1] * p[1])

    u = 42                                  # pixels per unit
    panels = [((110, 190), mul(R, S), 'S, THEN R', '0 −1', '1  1'),
              ((290, 190), mul(S, R), 'R, THEN S', '1 −1', '1  0')]
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]

    def to_px(o, p):
        return (o[0] + u * p[0], o[1] - u * p[1])

    d.group('thin')
    # a lattice in each panel, x from -2 to 2 and y from -1 to 2.4
    for o, *_ in panels:
        segs = [[to_px(o, (x, -1)), to_px(o, (x, 2.4))] for x in range(-2, 3)]
        segs += [[to_px(o, (-2, y)), to_px(o, (2, y))] for y in range(-1, 3)]
        d.lines(segs)
    d.group('thin')
    # the unit square before the map, hatched so that it reads against the lattice
    for o, *_ in panels:
        hatch = []
        for k in range(1, 8):
            t = k / 8
            hatch.append([to_px(o, (t, 0)), to_px(o, (0, t))])
            hatch.append([to_px(o, (1, t)), to_px(o, (t, 1))])
        hatch.append([to_px(o, (1, 0)), to_px(o, (0, 1))])
        d.lines(hatch)
    d.group()
    # the square's image under each product
    for o, M, *_ in panels:
        d.line(*[to_px(o, apply(M, p)) for p in square], closed=True)
    d.group('mid')
    # where the two unit arrows go: the columns of the matrix
    for o, M, *_ in panels:
        for e in ((1, 0), (0, 1)):
            _arrow(d, to_px(o, (0, 0)), to_px(o, apply(M, e)))
    d.group('thin')
    for o, *_ in panels:
        bx, by = o[0], 252
        for sg in (-1, 1):
            x = bx + sg * 26
            d.line((x - sg * 4, by - 10), (x, by - 10), (x, by + 15), (x - sg * 4, by + 15))
    d.group('mid')
    for o, M, name, r1, r2 in panels:
        d.text(o[0], 74, name, size=7)
        # the product matrix, two rows between brackets
        d.text(o[0], 252, r1)
        d.text(o[0], 264, r2)
    d.text(200, 258, '≠')
    return d


def monster():
    """The icosahedron's rotations, the smallest simple group that is not a prime
    cycle: an axis of each kind, and the class sizes that make it simple."""
    d = D()
    phi = (1 + 5 ** 0.5) / 2
    verts = SOLIDS['icosa']
    ax, ay, az = -1.3, -0.6, 0      # chosen so that all three axes lie nearly flat in the view
    cx, cy, s = 132, 152, 48

    def proj(p):
        x, y, z = rot(p, ax, ay, az)
        return (cx + s * x, cy - s * y)

    def scale(p, k):
        return tuple(k * c for c in p)

    # one axis of each kind: through opposite vertices (5-fold), face centres (3-fold)
    # and edge midpoints (2-fold); the faces and edges are found from the solid itself
    v5 = (0, 1, phi)
    near = sorted(verts, key=lambda w: math.dist(w, v5))
    m = math.dist(near[1], v5)
    nb = [w for w in verts if abs(math.dist(w, v5) - m) < 1e-6]
    a, b = nb[0], [w for w in nb[1:] if abs(math.dist(w, nb[0]) - m) < 1e-6][0]
    face = tuple((v5[i] + a[i] + b[i]) / 3 for i in range(3))
    # an edge's midpoint, chosen so that its axis stands clear of the other two
    edge_mid = (-phi / 2, -0.5, -1 / (2 * phi))
    axes = []
    for p, label in ((v5, '5'), (face, '3'), (edge_mid, '2')):
        n = math.sqrt(sum(c * c for c in p))
        u = scale(p, 1 / n)
        axes.append((proj(scale(u, 2.3)), proj(scale(u, -2.3)), proj(scale(u, 2.6)), label))

    d.group('thin')
    d.circle(cx, cy, s * math.sqrt(1 + phi * phi))        # the circumscribed sphere, seen as a circle
    for p, q, _, _ in axes:
        d.line(p, q)
    d.group()
    wire(d, verts, cx, cy, s, ax, ay, az)
    d.group('mid')
    # a small turning arrow round the top of each axis
    for p, q, _, _ in axes:
        ang = math.degrees(math.atan2(p[1] - cy, p[0] - cx))
        d.arc(p[0], p[1], 9, ang + 40, ang + 320, n=24, ry=4.5)

    # the class equation, as a column of tallies on the right
    rows = [('1', 1, 'IDENTITY'), ('12', 12, '72°'), ('12', 12, '144°'), ('20', 20, '120°'), ('15', 15, '180°')]
    x0, y0, step = 268, 70, 34
    d.group('mid')
    for i, (_, n, _) in enumerate(rows):
        y = y0 + i * step
        d.lines([[(x0 + 4 * k, y - 8), (x0 + 4 * k, y + 2)] for k in range(n)])
    d.group('thin')
    d.line((x0 - 4, y0 + 5 * step - 18), (x0 + 84, y0 + 5 * step - 18))
    d.group('mid')
    for i, (label, _, kind) in enumerate(rows):
        y = y0 + i * step
        d.text(x0 - 10, y + 1, label, anchor='end')
        d.text(x0, y + 14, kind, size=6, anchor='start')
    d.text(x0 - 10, y0 + 5 * step - 2, '60', anchor='end')
    d.text(x0, y0 + 5 * step - 2, 'ROTATIONS', size=7, anchor='start')
    for p, q, lab_pt, label in axes:
        d.text(lab_pt[0], lab_pt[1] + 3, label)
    return d


PLATES = {
    'matrices': matrices,
    'monster': monster,
}
