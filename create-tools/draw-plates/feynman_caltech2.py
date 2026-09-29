"""feynman plates, segment "Caltech", its last four frames (sprint 014). See feynman.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _vec(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def _norm(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def gweneth():
    """The globe in orthographic projection: the great circle from Geneva, where they met in 1958, to Pasadena, where she came in 1959."""
    d = D()
    cx, cy, R = 200, 150, 118
    gen, pas, rip = _vec(46.20, 6.15), _vec(34.15, -118.14), _vec(53.67, -1.94)
    # look from a point north of the route's midpoint, so its great circle opens into an ellipse
    mid = _norm(tuple(a + b for a, b in zip(gen, pas)))
    pole = _norm(_cross(gen, pas))
    centre = _norm(tuple(m + 0.45 * q for m, q in zip(mid, pole)))
    east = _norm(_cross((0, 0, 1), centre))
    north = _cross(centre, east)

    def proj(v):
        return cx + R * _dot(v, east), cy - R * _dot(v, north), _dot(v, centre)

    def curve(pts):
        """Split a run of 3-D points into the visible (front) polylines."""
        runs, cur = [], []
        for v in pts:
            x, y, z = proj(v)
            if z > 0:
                cur.append((x, y))
            elif cur:
                runs.append(cur)
                cur = []
        if cur:
            runs.append(cur)
        return runs

    # construction: the graticule, every 15 degrees, front hemisphere only
    d.group('thin')
    segs = []
    for lat in range(-75, 90, 15):
        segs += curve([_vec(lat, lo) for lo in range(-180, 181, 3)])
    for lon in range(-180, 180, 15):
        segs += curve([_vec(la, lon) for la in range(-90, 91, 3)])
    d.lines(segs)
    # the whole great circle through both cities, and the radii to them from the centre
    axis = _norm(_cross(gen, pas))
    b2 = _cross(axis, gen)
    full = [tuple(math.cos(t) * g + math.sin(t) * b for g, b in zip(gen, b2))
            for t in (2 * math.pi * i / 240 for i in range(241))]
    d.group('mid')
    d.lines(curve(full))
    gx, gy, _ = proj(gen)
    px, py, _ = proj(pas)
    d.lines([[(cx, cy), (gx, gy)], [(cx, cy), (px, py)]])
    # the angle between them at the earth's centre, as an arc of the same great circle
    ang = math.acos(_dot(gen, pas))
    arc = [tuple(0.3 * (math.cos(t) * g + math.sin(t) * b) for g, b in zip(gen, b2))
           for t in (ang * i / 40 for i in range(41))]
    d.line(*[(cx + R * _dot(v, east), cy - R * _dot(v, north)) for v in arc])
    # the globe and the route
    d.group()
    d.circle(cx, cy, R)
    route = [tuple(math.cos(t) * g + math.sin(t) * b for g, b in zip(gen, b2))
             for t in (ang * i / 80 for i in range(81))]
    d.line(*[proj(v)[:2] for v in route])
    # the places
    d.group('mid')
    for v in (gen, pas, rip):
        x, y, _ = proj(v)
        d.circle(x, y, 3.2)
    d.circle(cx, cy, 1.6)
    rx, ry, _ = proj(rip)
    d.group()
    d.text(gx - 4, gy + 14, 'GENEVA 1958', size=7, anchor='end')
    d.text(px - 6, py + 12, 'PASADENA 1959', size=7, anchor='end')
    d.text(rx - 5, ry - 7, 'RIPPONDEN', size=7, anchor='end')
    km = 6371 * ang
    d.text(cx, 290, f'{math.degrees(ang):.0f}° OF ARC · {round(km, -1):,.0f} KM BY THE GREAT CIRCLE', size=8)
    return d


def lectures():
    """Lecture 22, "Algebra": the complex plane, the unit circle, and e^(iθ) reached by many small steps."""
    d = D()
    cx, cy, R = 118, 196, 150
    n = 12                 # steps to a quarter turn
    eps = (math.pi / 2) / n
    # construction: axes, the unit circle's grid of angles
    d.group('thin')
    d.lines([[(cx - 30, cy), (cx + R + 40, cy)], [(cx, cy + 30), (cx, cy - R - 40)]])
    d.lines([[(cx, cy), (cx + (R + 24) * math.cos(k * eps), cy - (R + 24) * math.sin(k * eps))]
             for k in range(1, n)])
    # the steps: multiply by (1 + i eps) again and again; the points spiral slowly outward
    z = complex(1, 0)
    steps = [z]
    for _ in range(n):
        z *= complex(1, eps)
        steps.append(z)
    d.group('mid')
    d.line(*[(cx + R * w.real, cy - R * w.imag) for w in steps])
    for w in steps[1:n + 1]:
        d.circle(cx + R * w.real, cy - R * w.imag, 1.8)
    # the circle, e^(i theta) exactly, and one angle worked
    d.group()
    d.arc(cx, cy, R, 8, -98, n=80)
    th = math.radians(50)
    ex, ey = cx + R * math.cos(th), cy - R * math.sin(th)
    d.line((cx, cy), (ex, ey))
    d.circle(ex, ey, 3.5)
    d.group('mid')
    d.line((ex, ey), (ex, cy))
    d.line((ex, ey), (cx, ey))
    d.arc(cx, cy, 34, 0, -50, n=20)
    # the table: modulus after a quarter turn, for finer and finer steps
    d.group('thin')
    tx, ty = 286, 150
    d.lines([[(tx, ty + 6), (tx + 108, ty + 6)], [(tx + 44, ty - 10), (tx + 44, ty + 104)]])
    d.group()
    d.text(cx + 42, cy - 14, 'θ', size=9)
    d.text(ex + 8, ey - 6, 'e^iθ', size=9, anchor='start')
    d.text(ex + 4, cy + 12, 'cos θ', size=7, anchor='start')
    d.text(cx - 4, ey + 3, 'sin θ', size=7, anchor='end')
    d.text(cx + R, cy + 14, '1', size=8)
    d.text(cx - 10, cy - R + 4, 'i', size=8)
    d.text(tx + 22, ty, 'STEPS', size=7)
    d.text(tx + 76, ty, '|z| AT i', size=7)
    for k, m in enumerate((4, 12, 100, 1000)):
        e = (math.pi / 2) / m
        mod = abs(complex(1, e) ** m)
        d.text(tx + 22, ty + 22 + 20 * k, f'{m}', size=8)
        d.text(tx + 76, ty + 22 + 20 * k, f'{mod:.4f}', size=8)
    d.text(200, 290, 'e^iθ = cos θ + i sin θ  ·  VOL. I · CH. 22 · ALGEBRA', size=8)
    return d


def character_of_law():
    """The lost lecture: an orbit cut at equal angles about the sun, and its velocities, which lie on a circle."""
    d = D()
    e = 0.55
    # orbit: r = p / (1 + e cos theta), sun at the focus
    ox, oy, p = 150, 158, 54
    orbit = lambda t: (ox + p / (1 + e * math.cos(t)) * math.cos(t), oy - p / (1 + e * math.cos(t)) * math.sin(t))
    # velocity for a unit of GM/h: v = (-sin t, e + cos t); the hodograph is a circle centred at (0, e)
    hx, hy, hs = 308, 180, 58
    vel = lambda t: (-math.sin(t), e + math.cos(t))
    angles = [2 * math.pi * k / 12 for k in range(12)]
    # construction: equal angles at the sun; the axis; the hodograph's centre line
    d.group('thin')
    d.lines([[(ox, oy), orbit(t)] for t in angles])
    d.line((ox - p / (1 - e) - 10, oy), (ox + p / (1 + e) + 14, oy))
    hc = hy - e * hs   # the circle's centre: equal angles at the sun are equal angles here
    d.lines([[(hx, hc), (hx + hs * math.cos(t + math.pi / 2), hc - hs * math.sin(t + math.pi / 2))] for t in angles])
    d.line((hx, hy + hs + 10), (hx, hy - hs - e * hs - 14))
    # the orbit and the velocity circle
    d.group()
    d.line(*[orbit(2 * math.pi * i / 180) for i in range(181)])
    d.circle(ox, oy, 4)
    d.circle(hx, hy - e * hs, hs)
    # the velocities: short tangents on the orbit, and the same vectors drawn from one point
    d.group('mid')
    for t in angles:
        x, y = orbit(t)
        vx, vy = vel(t)
        sc = 13
        d.line((x, y), (x + sc * vx, y - sc * vy))
        _arrow(d, x + sc * vx, y - sc * vy, math.atan2(-vy, vx), 3.5)
        tx, ty = hx + hs * vx, hy - hs * vy
        d.line((hx, hy), (tx, ty))
        d.circle(tx, ty, 2)
    d.circle(hx, hy, 2.5)
    d.group()
    d.text(ox, oy + 16, 'SUN', size=7)
    d.text(ox - 30, 60, 'ORBIT · 12 EQUAL ANGLES', size=7)
    d.text(hx, 60, 'VELOCITIES · A CIRCLE', size=7)
    d.text(hx + 8, hy + 14, 'O', size=8, anchor='start')
    d.text(200, 290, 'EQUAL ANGLES AT THE SUN → EQUAL TURNS OF VELOCITY → AN ELLIPSE', size=8)
    return d


def nobel():
    """The Nobel lecture's dead end: paths on a space-time checkerboard, moving only at the speed of light, with an amplitude for each reversal."""
    d = D()
    x0, t0, s = 200, 262, 18     # the start, and one step of the lattice
    rows = 12

    def P(i, j):
        """Lattice point: i steps in space (right +), j steps in time (up)."""
        return x0 + s * i, t0 - s * j

    # construction: the light-speed lattice, both diagonals, bounded by the light cone from the start
    d.group('thin')
    segs = []
    for k in range(-rows, rows + 1):
        segs.append([P(k, 0), P(k + rows, rows)])
        segs.append([P(k, 0), P(k - rows, rows)])
    segs = [[a, b] for a, b in segs]
    # clip each diagonal to the drawing's band
    clipped = []
    for (ax, ay), (bx, by) in segs:
        pts = [(ax + (bx - ax) * u / 48, ay + (by - ay) * u / 48) for u in range(49)]
        pts = [q for q in pts if 60 <= q[0] <= 340]
        if len(pts) > 1:
            clipped.append([pts[0], pts[-1]])
    d.lines(clipped)
    # axes
    d.group('mid')
    d.line((52, t0), (352, t0))
    _arrow(d, 352, t0, 0)
    d.line((60, t0 + 8), (60, 28))
    _arrow(d, 60, 28, -math.pi / 2)
    # two paths from the same start to the same end: each a zigzag at the speed of light
    moves_a = [1, 1, -1, -1, -1, 1, 1, 1, -1, -1, 1, -1]   # 5 reversals
    moves_b = [-1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1]   # 3 reversals
    for moves, kind in ((moves_b, 'mid'), (moves_a, 'main')):
        d.group(kind)
        i, pts, turns = 0, [P(0, 0)], []
        for j, m in enumerate(moves):
            if j and m != moves[j - 1]:
                turns.append(P(i, j))
            i += m
            pts.append(P(i, j + 1))
        d.line(*pts)
        for q in turns:
            d.circle(q[0], q[1], 3 if kind == 'main' else 2.4)
    d.group()
    d.circle(*P(0, 0), 3.5)
    d.circle(*P(0, rows), 3.5)
    d.text(352, t0 + 14, 'x', size=8)
    d.text(52, 30, 't', size=8, anchor='end')
    d.text(x0 + 8, t0 + 14, 'A', size=8, anchor='start')
    d.text(x0 + 8, t0 - s * rows - 4, 'B', size=8, anchor='start')
    d.text(200, 16, 'AMPLITUDE OF A PATH = (iε)^R  ·  R = REVERSALS', size=8)
    d.text(200, 290, 'ONE SPACE DIMENSION: IT GIVES DIRAC. IN THREE, HE NEVER FOUND IT', size=8)
    return d


PLATES = {
    'gweneth': gweneth,
    'lectures': lectures,
    'character-of-law': character_of_law,
    'nobel': nobel,
}
