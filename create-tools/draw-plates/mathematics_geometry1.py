"""Plates for the mathematics subject's Geometry segment, part one (sprint 024):
perspective, non-Euclidean geometry and Riemann's curved spaces."""
import math
from plates import D


def _meet(p1, p2, p3, p4):
    """Where line p1p2 meets line p3p4."""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    return x1 + t * (x2 - x1), y1 + t * (y2 - y1)


def _beyond(p, q, s):
    """The point s of the way from p past q (s > 1 runs beyond q)."""
    return p[0] + s * (q[0] - p[0]), p[1] + s * (q[1] - p[1])


def perspective():
    """Desargues' theorem. Two triangles in perspective from a point O: the
    rays Oa, Ob, Oc pass through A, B, C. The big triangle is constructed
    from the small one and a chosen axis (A on Oa, B where the line from
    ab's meeting point to A cuts Ob, C likewise), and the third pair of
    sides is then checked to meet on the same axis, which is the theorem."""
    d = D()
    O = (36, 34)
    Y = 266                                        # the axis of perspectivity
    a, b, c = (125.9, 128.3), (66.6, 94.5), (69.5, 54.5)
    L1, L2 = (0, Y), (400, Y)
    Pab, Pbc, Pca = _meet(a, b, L1, L2), _meet(b, c, L1, L2), _meet(c, a, L1, L2)
    k = 2.167
    A = (O[0] + k * (a[0] - O[0]), O[1] + k * (a[1] - O[1]))
    B = _meet(Pab, A, O, b)
    C = _meet(Pbc, B, O, c)
    check = _meet(C, A, L1, L2)
    assert abs(check[0] - Pca[0]) < 1e-6, 'Desargues failed'
    d.group('thin')
    # the three rays from the centre of perspectivity, run on past the big triangle
    d.lines([[O, _beyond(O, P, 1.12)] for P in (A, B, C)])
    # each pair of corresponding sides produced to the axis
    d.lines([[a, Pab], [A, Pab], [b, Pbc], [B, Pbc], [c, Pca], [A, Pca]])
    d.group('mid')
    d.line((28, Y), (392, Y))
    d.group()
    d.line(a, b, c, closed=True)
    d.line(A, B, C, closed=True)
    d.group('mid')
    for p in (O, Pab, Pbc, Pca):
        d.circle(p[0], p[1], 2.2)
    d.group('mid')
    d.text(O[0] - 10, O[1] - 4, 'O')
    for s, p, dx, dy in (('a', a, 8, 4), ('b', b, -9, 2), ('c', c, -8, -2),
                         ('A', A, 9, 6), ('B', B, -10, 4), ('C', C, 8, -5)):
        d.text(p[0] + dx, p[1] + dy, s)
    d.text(392, Y - 8, 'AXIS', size=7, anchor='end')
    return d


def _geodesic(p, q, n=60):
    """The hyperbolic straight line from p to q in the unit disc (complex
    numbers): an arc of the circle through p and q that meets the boundary
    at right angles, or a diameter."""
    pi = 1 / p.conjugate()
    ax, ay, bx, by, cx, cy = p.real, p.imag, q.real, q.imag, pi.real, pi.imag
    den = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(den) < 1e-12:
        return [p + (q - p) * i / n for i in range(n + 1)], None
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / den
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / den
    centre = complex(ux, uy)
    r = abs(p - centre)
    a0, a1 = math.atan2((p - centre).imag, (p - centre).real), math.atan2((q - centre).imag, (q - centre).real)
    da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi          # the short way round
    return [centre + r * complex(math.cos(a0 + da * i / n), math.sin(a0 + da * i / n)) for i in range(n + 1)], (centre, r)


def _tangent(p, q):
    pts, _ = _geodesic(p, q, n=400)
    t = pts[1] - pts[0]
    return t / abs(t)


def non_euclidean():
    """The Poincaré disc. Two equilateral triangles, Euclidean radius 0.2 and
    0.6 about the centre, whose angles are computed from the arcs (56.1° and
    30.4°); and a line with two parallels through a point off it, the limiting
    lines that meet it only at the boundary."""
    d = D()
    cx, cy, R = 138, 150, 124
    to = lambda z: (cx + R * z.real, cy - R * z.imag)
    tri = lambda r: [r * complex(math.cos(math.pi / 2 + 2 * math.pi * k / 3), math.sin(math.pi / 2 + 2 * math.pi * k / 3)) for k in range(3)]
    big, small = tri(0.6), tri(0.2)
    # a line with its ends on the boundary, and a point off it
    e1 = complex(math.cos(math.radians(-118)), math.sin(math.radians(-118))) * 0.99999
    e2 = complex(math.cos(math.radians(-62)), math.sin(math.radians(-62))) * 0.99999
    e1i, e2i = e1, e2
    P = complex(0, -0.37)
    d.group('thin')
    # construction: the radii to the vertices, 0.2 and 0.6 of the disc's
    d.lines([[to(0), to(v)] for v in big])
    d.group()
    d.circle(cx, cy, R)
    d.group()
    for t in (big, small):
        pts = []
        for i in range(3):
            seg, _ = _geodesic(t[i], t[(i + 1) % 3])
            pts += seg[:-1]
        d.line(*[to(z) for z in pts], closed=True)
    d.group('mid')
    seg, _ = _geodesic(e1i, e2i, n=80)
    d.line(*[to(z) for z in seg])
    for e in (e1i, e2i):
        seg, _ = _geodesic(P, e, n=60)
        d.line(*[to(z) for z in seg])
    d.circle(*to(P), 2)
    # the big triangle's angles, as small arcs at its vertices
    d.group('mid')
    for i in range(3):
        v = big[i]
        t1, t2 = _tangent(v, big[(i + 1) % 3]), _tangent(v, big[(i - 1) % 3])
        a1, a2 = math.atan2(-t1.imag, t1.real), math.atan2(-t2.imag, t2.real)
        da = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
        x, y = to(v)
        d.line(*[(x + 11 * math.cos(a1 + da * j / 12), y + 11 * math.sin(a1 + da * j / 12)) for j in range(13)])
    d.group('mid')
    x, y = to(big[0])
    d.text(x + 10, y + 2, '30.4°', anchor='start')
    x, y = to(small[0])
    d.text(x + 8, y + 2, '56.1°', size=7, anchor='start')
    d.text(to(P)[0] + 9, to(P)[1] + 3, 'P', size=8)
    d.text(338, 110, 'ANGLE SUMS', size=7)
    d.text(338, 134, 'SMALL 168.3°')
    d.text(338, 152, 'LARGE  91.2°')
    d.text(338, 176, 'EUCLID: 180°', size=7)
    return d


def _globe_point(lat, lon, view_lat, view_lon):
    """Orthographic projection: (x right, y up, z towards the viewer) of a point on the unit sphere."""
    la, lo = math.radians(lat), math.radians(lon - view_lon)
    x, y, z = math.cos(la) * math.sin(lo), math.sin(la), math.cos(la) * math.cos(lo)
    vl = math.radians(view_lat)
    y, z = y * math.cos(vl) - z * math.sin(vl), y * math.sin(vl) + z * math.cos(vl)
    return x, y, z


def riemann_geometry():
    """Left: a triangle on a sphere with three right angles, from the pole to
    the equator at 0° and 90° of longitude (angle sum 270°, the excess 90° =
    its area on a sphere of radius 1 in radians, one eighth of 4π). Right:
    Gauss's great triangle of the Hanover survey, Hoher Hagen, Brocken and
    Inselsberg, laid out from their latitudes and longitudes, north up."""
    d = D()
    cx, cy, R = 128, 152, 102
    vlat, vlon = 24, 45
    proj = lambda lat, lon: (lambda p: (cx + R * p[0], cy - R * p[1], p[2]))(_globe_point(lat, lon, vlat, vlon))

    def curve(pts):
        """Visible runs of a curve on the sphere, as polylines."""
        runs, cur = [], []
        for x, y, z in pts:
            if z >= -1e-9:
                cur.append((x, y))
            elif cur:
                runs.append(cur)
                cur = []
        if cur:
            runs.append(cur)
        return runs
    d.group('thin')
    segs = []
    for lon in range(0, 360, 30):
        segs += curve([proj(lat, lon) for lat in range(-90, 91, 3)])
    for lat in (-60, -30, 30, 60):
        segs += curve([proj(lat, lon) for lon in range(0, 361, 3)])
    d.lines(segs)
    d.group('mid')
    d.circle(cx, cy, R)
    d.lines(curve([proj(0, lon) for lon in range(0, 361, 3)]))
    d.group()
    tri = [proj(lat, 0) for lat in range(90, -1, -2)] + [proj(0, lon) for lon in range(0, 91, 2)] + \
          [proj(lat, 90) for lat in range(0, 91, 2)]
    d.line(*[(x, y) for x, y, _ in tri], closed=True)
    d.group('mid')
    # right-angle marks at the three corners, drawn on the sphere
    s = 9
    d.line(*[proj(s, 0)[:2], proj(s, s)[:2], proj(0, s)[:2]])
    d.line(*[proj(s, 90)[:2], proj(s, 90 - s)[:2], proj(0, 90 - s)[:2]])
    d.line(*[proj(90 - s * 1.3, lon)[:2] for lon in range(0, 91, 6)])
    # Gauss's triangle, to scale beside it: km from Hoher Hagen, north up
    places = {'HOHER HAGEN': (51.4797, 9.7967), 'BROCKEN': (51.7991, 10.6156), 'INSELSBERG': (50.8522, 10.4681)}
    lat0, lon0 = places['HOHER HAGEN']
    km = lambda la, lo: (111.2 * math.cos(math.radians(lat0)) * (lo - lon0), 111.2 * (la - lat0))
    scale, ox, oy = 1.05, 262, 150
    g = {k: (ox + scale * km(*v)[0], oy - scale * km(*v)[1]) for k, v in places.items()}
    d.group()
    d.line(g['HOHER HAGEN'], g['BROCKEN'], g['INSELSBERG'], closed=True)
    d.group('mid')
    for p in g.values():
        d.circle(p[0], p[1], 2)
    d.group('mid')
    top = proj(90, 0)
    d.text(top[0] + 22, top[1] - 16, '90°', size=8)
    d.text(cx, cy + R + 16, '90° + 90° + 90° = 270°', size=8)
    d.text(g['HOHER HAGEN'][0] - 6, g['HOHER HAGEN'][1] + 3, 'HOHER HAGEN', size=6, anchor='end')
    d.text(g['BROCKEN'][0] + 4, g['BROCKEN'][1] - 7, 'BROCKEN', size=6)
    d.text(g['INSELSBERG'][0] + 4, g['INSELSBERG'][1] + 13, 'INSELSBERG', size=6)
    d.text(318, 268, '180° + 14.85″', size=8)
    return d


PLATES = {
    'perspective': perspective,
    'non-euclidean': non_euclidean,
    'riemann-geometry': riemann_geometry,
}
