"""Plates for the mathematics subject's Geometry segment, part two: topology,
the Poincaré conjecture and fractals (sprint 024)."""
import math
from plates import D


# a torus, seen in orthographic projection ---------------------------------

def _torus(R, r, tilt):
    """Point and unit normal of a torus (tube radius r about a circle of radius R),
    tipped towards the viewer by `tilt` radians about the x axis. The viewer looks
    down the +z axis; y is up the page once flipped."""
    ct, st = math.cos(tilt), math.sin(tilt)

    def rotx(x, y, z):
        return x, y * ct - z * st, y * st + z * ct

    def point(u, v):
        w = R + r * math.cos(v)
        return rotx(w * math.cos(u), w * math.sin(u), r * math.sin(v))

    def normal(u, v):
        return rotx(math.cos(v) * math.cos(u), math.cos(v) * math.sin(u), math.sin(v))

    def inside(p):
        # undo the tilt and test the torus's implicit equation
        x, y, z = p
        y0, z0 = y * ct + z * st, -y * st + z * ct
        return (math.hypot(x, y0) - R) ** 2 + z0 ** 2 < r * r

    def visible(u, v):
        # front-facing, and nothing of the torus between the point and the viewer
        n = normal(u, v)
        if n[2] < -0.02:
            return False
        p = point(u, v)
        q = [p[i] + 0.8 * n[i] for i in range(3)]
        for k in range(1, 90):
            t = k * (2.4 * (R + r)) / 90
            if inside((q[0], q[1], q[2] + t)):
                return False
        return True

    return point, normal, visible


def _visible_runs(pts_vis):
    """Split a sampled curve into the runs of consecutive visible points."""
    runs, cur = [], []
    for p, ok in pts_vis:
        if ok:
            cur.append(p)
        else:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


def _torus_drawing(cx, cy, R, r, tilt, meridians, parallels, n=120):
    """Visible grid lines and outline of a torus, in page coordinates."""
    point, normal, visible = _torus(R, r, tilt)
    page = lambda p: (cx + p[0], cy - p[1])
    grid = []
    for i in range(meridians):            # circles around the tube, half a step off the edge-on ones
        u = 2 * math.pi * (i + 0.5) / meridians
        pts = [(page(point(u, 2 * math.pi * k / n)), visible(u, 2 * math.pi * k / n)) for k in range(n + 1)]
        grid += _visible_runs(pts)
    for j in range(parallels):            # circles around the hole
        v = 2 * math.pi * j / parallels
        pts = [(page(point(2 * math.pi * k / n, v)), visible(2 * math.pi * k / n, v)) for k in range(n + 1)]
        grid += _visible_runs(pts)
    # the outline: where the surface turns edge-on to the viewer (n_z = 0)
    ct, st = math.cos(tilt), math.sin(tilt)
    outline = []
    for branch in (0, 1):
        pts = []
        for k in range(2 * n + 1):
            u = 2 * math.pi * k / (2 * n)
            a, b = math.sin(u) * st, ct        # n_z = a cos v + b sin v
            v = math.atan2(-a, b) + branch * math.pi
            pts.append((page(point(u, v)), visible(u, v)))
        outline += _visible_runs(pts)
    return grid, outline, point, visible, page


# topology -------------------------------------------------------------------

def topology():
    d = D()
    m, k = 12, 6                          # the grid: 12 around the hole, 6 around the tube
    # the flat square whose opposite edges are glued to make the torus
    x0, y0, s = 34, 96, 108
    grid, outline, point, visible, page = _torus_drawing(278, 150, 76, 30, math.radians(62), m, k)
    d.group('thin')
    d.lines([[(x0 + s * i / m, y0), (x0 + s * i / m, y0 + s)] for i in range(1, m)] +
            [[(x0, y0 + s * j / k), (x0 + s, y0 + s * j / k)] for j in range(1, k)])
    # construction: the torus's centre circle and axis, and the gluing arrows between the drawings
    cc = []
    ct, st = math.cos(math.radians(62)), math.sin(math.radians(62))
    for i in range(121):
        t = 2 * math.pi * i / 120
        x, y = 76 * math.cos(t), 76 * math.sin(t)
        cc.append((278 + x, 150 - y * ct))
    d.line(*cc)
    d.line((278, 150 - 30 - 76 * ct - 22), (278, 150 + 30 + 76 * ct + 22))
    d.line((148, 157), (166, 157))
    d.line((162, 154), (166, 157), (162, 160))
    d.group()
    d.line((x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s), closed=True)
    d.lines(outline)
    d.group('mid')
    d.lines(grid)
    # the gluing marks: one chevron on the edges glued top to bottom, two on those glued side to side
    def chevron(x, y, dx, dy, w=4):
        return [(x - dx * w - dy * w, y - dy * w + dx * w), (x, y), (x - dx * w + dy * w, y - dy * w - dx * w)]
    marks = [chevron(x0 + s / 2 + 2, y0, 1, 0), chevron(x0 + s / 2 + 2, y0 + s, 1, 0),
             chevron(x0, y0 + s / 2 - 4, 0, -1), chevron(x0, y0 + s / 2 + 2, 0, -1),
             chevron(x0 + s, y0 + s / 2 - 4, 0, -1), chevron(x0 + s, y0 + s / 2 + 2, 0, -1)]
    d.lines(marks)
    d.group('mid')
    d.text(x0 + s / 2, y0 + s + 18, 'V 72  E 144  F 72', size=7)
    d.text(x0 + s / 2, y0 - 12, 'GLUE THE EDGES', size=7)
    d.text(278, 262, 'V − E + F = 0')
    d.text(278, 40, 'TORUS', size=7)
    return d


# the Poincaré conjecture --------------------------------------------------

def poincare_conjecture():
    d = D()
    # a sphere, tipped so that its north pole leans towards the viewer
    sx, sy, sr = 104, 148, 76
    tilt = math.radians(28)
    ct, st = math.cos(tilt), math.sin(tilt)

    def sph(theta, phi):              # colatitude, longitude -> page point and depth
        x = sr * math.sin(theta) * math.cos(phi)
        y = sr * math.cos(theta)
        z = sr * math.sin(theta) * math.sin(phi)
        y, z = y * ct - z * st, y * st + z * ct
        return (sx + x, sy - y), z

    def latitude(theta, n=96):
        pts = [sph(theta, 2 * math.pi * i / n) for i in range(n + 1)]
        return _visible_runs([(p, z >= 0) for p, z in pts]), _visible_runs([(p, z < 0) for p, z in pts])

    grid, outline, point, visible, page = _torus_drawing(298, 150, 62, 25, math.radians(58), 1, 1)
    d.group('thin')
    # the sphere's hidden halves of its equator and a meridian, and the torus's centre circle
    eq_front, eq_back = latitude(math.pi / 2)
    d.lines(eq_back)
    d.lines(eq_front)
    mer = [sph(math.pi * i / 96, 0) for i in range(97)] + [sph(math.pi - math.pi * i / 96, math.pi) for i in range(97)]
    d.lines(_visible_runs([(p, z >= 0) for p, z in mer]))
    cc = []
    c2 = math.cos(math.radians(58))
    for i in range(121):
        t = 2 * math.pi * i / 120
        cc.append((298 + 62 * math.cos(t), 150 - 62 * math.sin(t) * c2))
    d.line(*cc)
    d.group()
    d.circle(sx, sy, sr)
    d.lines(outline)
    d.group('mid')
    # the loop on the sphere, shown at four moments as it slides up and shrinks to a point
    for theta in (72, 52, 32, 14):
        front, back = latitude(math.radians(theta))
        d.lines(front)
    d.group()
    pole, _ = sph(0, 0)
    d.circle(pole[0], pole[1], 1.6)
    # on the torus, one loop around the tube and one around the hole: neither can shrink
    tp, _, vis = _torus(62, 25, math.radians(58))
    u0 = math.radians(-70)
    tube = [(page(tp(u0, 2 * math.pi * k / 120)), vis(u0, 2 * math.pi * k / 120)) for k in range(121)]
    d.lines(_visible_runs(tube))
    hole = [(page(tp(2 * math.pi * k / 160, math.radians(90))), vis(2 * math.pi * k / 160, math.radians(90))) for k in range(161)]
    d.lines(_visible_runs(hole))
    d.group('mid')
    d.text(sx, 262, 'EVERY LOOP SHRINKS', size=7)
    d.text(298, 262, 'THESE CANNOT', size=7)
    d.text(sx, 40, 'SPHERE', size=7)
    d.text(298, 40, 'TORUS', size=7)
    return d


# fractals ---------------------------------------------------------------------

def _koch(a, b, n):
    """The Koch curve of order n from point a to point b (bump on the left of a→b,
    which is up the page when a is left of b)."""
    if n == 0:
        return [a, b]
    (ax, ay), (bx, by) = a, b
    dx, dy = (bx - ax) / 3, (by - ay) / 3
    p1 = (ax + dx, ay + dy)
    p2 = (ax + 2 * dx, ay + 2 * dy)
    # the apex: the middle third turned through 60° (page y runs down, so turn the other way)
    c, s = math.cos(-math.pi / 3), math.sin(-math.pi / 3)
    apex = (p1[0] + dx * c - dy * s, p1[1] + dx * s + dy * c)
    out = []
    for p, q in ((a, p1), (p1, apex), (apex, p2), (p2, b)):
        seg = _koch(p, q, n - 1)
        out += seg if not out else seg[1:]
    return out


def fractals():
    d = D()
    # three small stages across the top, the fourth stage large below
    small = [(28, 100), (148, 100), (268, 100)]
    w = 104
    bx0, bx1, by = 30, 370, 250
    L = bx1 - bx0
    h = L / 3 * math.sqrt(3) / 2
    d.group('thin')
    # construction: the base divided in thirds, and the first triangle raised on the middle third
    d.line((bx0, by), (bx1, by))
    for i in (1, 2):
        d.line((bx0 + L * i / 3, by - 5), (bx0 + L * i / 3, by + 5))
    d.line((bx0 + L / 3, by), (bx0 + L / 2, by - h), (bx0 + 2 * L / 3, by))
    d.group('mid')
    for n, (x, y) in enumerate(small):
        d.line(*_koch((x, y), (x + w, y), n))
    d.group()
    d.line(*_koch((bx0, by), (bx1, by), 4))
    d.group('mid')
    for n, (x, y) in enumerate(small):
        d.text(x + w / 2, y + 22, f'n = {n}', size=7)
    d.text(bx0 + L / 2, 272, 'n = 4 · 256 SEGMENTS OF 1/81', size=7)
    d.text(200, 40, 'LENGTH × 4/3 AT EVERY STEP', size=7)
    return d


PLATES = {
    'topology': topology,
    'poincare-conjecture': poincare_conjecture,
    'fractals': fractals,
}
