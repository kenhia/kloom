"""Plates for the chemistry subject's atoms2 part: chirality, structure-theory, karlsruhe (sprint 025)."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _offset(a, b, c, k=3.2):
    """A second, shorter line inside a double bond ab, on the side of point c (a ring's centre)."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = c[0] - mx, c[1] - my
    n = math.hypot(dx, dy)
    ox, oy = dx / n * k, dy / n * k
    t = 0.18
    return [(a[0] + (b[0] - a[0]) * t + ox, a[1] + (b[1] - a[1]) * t + oy),
            (a[0] + (b[0] - a[0]) * (1 - t) + ox, a[1] + (b[1] - a[1]) * (1 - t) + oy)]


# --- chirality ---------------------------------------------------------------------------------

def _hemihedral_crystal(half=(1.0, 0.62, 1.45), cut=(0.42, 0.3, 0.55), hand=1):
    """A rectangular prism with a small facet cut on the four corners whose signs multiply to `hand`:
    the hemihedral habit of sodium ammonium tartrate, reduced to its essentials. Returns faces as
    (outward normal, [3D points in order])."""
    a, b, c = half
    faces = []
    trunc = lambda s: s[0] * s[1] * s[2] == hand

    def cutpt(p, q):                         # the point on edge p→q where a facet at p cuts it
        axis = next(i for i in range(3) if p[i] != q[i])
        t = cut[axis] / abs(q[axis] - p[axis])
        return tuple(p[i] + (q[i] - p[i]) * t for i in range(3))

    for axis in range(3):
        for s in (-1, 1):
            others = [i for i in range(3) if i != axis]
            ring = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
            corners = []
            for u, v in ring:
                sg = [0, 0, 0]
                sg[axis], sg[others[0]], sg[others[1]] = s, u, v
                corners.append(tuple(sg))
            pts = []
            for k, sg in enumerate(corners):
                p = (sg[0] * a, sg[1] * b, sg[2] * c)
                if trunc(sg):
                    prv = corners[k - 1]
                    nxt = corners[(k + 1) % 4]
                    pts.append(cutpt(p, (prv[0] * a, prv[1] * b, prv[2] * c)))
                    pts.append(cutpt(p, (nxt[0] * a, nxt[1] * b, nxt[2] * c)))
                else:
                    pts.append(p)
            n = [0, 0, 0]
            n[axis] = s
            faces.append((tuple(n), pts))
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                if trunc((sx, sy, sz)):
                    p = (sx * a, sy * b, sz * c)
                    tri = [(p[0] - sx * cut[0], p[1], p[2]), (p[0], p[1] - sy * cut[1], p[2]),
                           (p[0], p[1], p[2] - sz * cut[2])]
                    faces.append(((sx / cut[0], sy / cut[1], sz / cut[2]), tri))
    return faces


def _view(p, turn=32, tilt=18):
    """Turn about the vertical (z) axis, then tip towards the viewer; returns (screen x, screen up, depth)."""
    t, f = math.radians(turn), math.radians(tilt)
    x, y, z = p
    x, y = x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t)
    y, z = y * math.cos(f) - z * math.sin(f), y * math.sin(f) + z * math.cos(f)
    return x, z, y


def _crystal_edges(faces, cx, cy, s):
    """Visible and hidden edges of a convex solid given as faces, projected at (cx, cy) with scale s."""
    vis, hid, seen = [], [], {}
    for n, pts in faces:
        facing = _view(n)[2] < 0            # the viewer looks along +depth
        for i in range(len(pts)):
            e = tuple(sorted((tuple(round(v, 6) for v in pts[i]), tuple(round(v, 6) for v in pts[(i + 1) % len(pts)]))))
            seen[e] = seen.get(e, False) or facing
    for (p, q), facing in seen.items():
        a, b = _view(p), _view(q)
        seg = [(cx + s * a[0], cy - s * a[1]), (cx + s * b[0], cy - s * b[1])]
        (vis if facing else hid).append(seg)
    return vis, hid


def chirality():
    """Two mirror-image crystals of sodium ammonium tartrate, and the polarimeter's two readings."""
    d = D()
    m, cy, s = 200, 112, 44
    right = _hemihedral_crystal(hand=1)
    vis, hid = _crystal_edges(right, m - 92, cy, s)
    mirror = lambda segs: [[(2 * m - x, y) for x, y in seg] for seg in segs]
    # the facets' own corners, to join each to its image across the mirror
    tips = []
    for n, pts in right:
        if len(pts) == 3:
            p = _view(pts[0])
            tips.append((m - 92 + s * p[0], cy - s * p[1]))
    d.group('thin')
    d.line((m, 22), (m, 212))
    d.lines([[(m - 6, y), (m + 6, y + 8)] for y in range(30, 205, 16)])
    d.lines([[t, (2 * m - t[0], t[1])] for t in tips[:2]])
    d.lines(hid + mirror(hid))
    d.group()
    d.lines(vis)
    d.lines(mirror(vis))
    # the polarimeter: plane of polarisation before (vertical) and after, turned right and left
    d.group('thin')
    r, py = 26, 252
    for x in (m - 92, m + 92):
        d.circle(x, py, r)
        d.line((x, py - r - 6), (x, py + r + 6))
    d.group('mid')
    for x, sgn in ((m - 92, 1), (m + 92, -1)):
        a = math.radians(24 * sgn)
        d.line((x - (r + 4) * math.sin(a), py + (r + 4) * math.cos(a)), (x + (r + 4) * math.sin(a), py - (r + 4) * math.cos(a)))
        d.arc(x, py, r - 8, -90, -90 + 24 * sgn, n=12)
    d.group('mid')
    d.text(m - 92, 236 - 20, 'TURNS RIGHT', size=7)
    d.text(m + 92, 236 - 20, 'TURNS LEFT', size=7)
    d.text(m - 92 + 42, py + 4, '+12°', size=8, anchor='start')
    d.text(m + 92 - 42, py + 4, '−12°', size=8, anchor='end')
    d.text(m, 16, 'MIRROR', size=7)
    d.text(m, 292, 'NaNH₄C₄H₄O₆·4H₂O', size=8)
    return d


# --- structure-theory ---------------------------------------------------------------------------

def _tree(d, nodes, edges, r=3.2):
    d.lines([[nodes[a], nodes[b]] for a, b in edges])


def structure_theory():
    """Kekulé's benzene, drawn from a regular hexagon, and Cayley's three carbon trees of C5H12."""
    d = D()
    O, L = (96, 128), 36
    ring = [_pt(O, -90 + 60 * k, L) for k in range(6)]
    hs = [_pt(O, -90 + 60 * k, L + 22) for k in range(6)]
    # the three trees, each a zigzag of bond length b; numbers are hydrogens on each carbon
    b = 24
    zx, zy = b * math.cos(math.radians(30)), b * math.sin(math.radians(30))
    t1x, t1y = 226, 64
    chain = [(t1x + i * zx, t1y + (zy if i % 2 else 0)) for i in range(5)]
    t2x, t2y = 238, 150
    iso = [(t2x + i * zx, t2y + (zy if i % 2 else 0)) for i in range(4)]
    iso.append((iso[1][0], iso[1][1] + b))
    nc = (292, 236)
    neo = [nc] + [_pt(nc, a, b) for a in (0, 90, 180, 270)]
    trees = [(chain, [(0, 1), (1, 2), (2, 3), (3, 4)], [3, 2, 2, 2, 3]),
             (iso, [(0, 1), (1, 2), (2, 3), (1, 4)], [3, 1, 2, 3, 3]),
             (neo, [(0, 1), (0, 2), (0, 3), (0, 4)], [0, 3, 3, 3, 3])]
    d.group('thin')
    d.circle(*O, L)
    d.circle(*O, L + 22)
    for k in range(3):
        d.line(ring[k], ring[k + 3])
    d.line((188, 22), (188, 278))
    d.group()
    d.line(*ring, closed=True)
    for nodes, edges, _ in trees:
        _tree(d, nodes, edges)
    d.group('mid')
    d.lines([_offset(ring[k], ring[(k + 1) % 6], O) for k in (0, 2, 4)])
    d.lines([[_pt(O, -90 + 60 * k, L + 3), _pt(O, -90 + 60 * k, L + 15)] for k in range(6)])
    for nodes, _, _ in trees:
        for p in nodes:
            d.circle(*p, 3)
    d.group('mid')
    for h in hs:
        d.text(h[0], h[1] + 3, 'H', size=8)
    below = {(0, 1), (0, 3), (1, 3)}                 # zigzag carbons in a trough take their count underneath
    for ti, (nodes, _, nh) in enumerate(trees):
        for ni, (p, n) in enumerate(zip(nodes, nh)):
            if not n:
                continue
            if (ti, ni) in below:
                d.text(p[0], p[1] + 15, str(n), size=7)
            elif (ti, ni) == (1, 1):
                d.text(p[0] + 7, p[1] + 11, str(n), size=7, anchor='start')
            elif (ti, ni) == (1, 4):
                d.text(p[0] + 8, p[1] + 3, str(n), size=7, anchor='start')
            else:
                d.text(p[0] + 7, p[1] - 5, str(n), size=7, anchor='start')
    d.text(O[0], 214, 'C₆H₆ · 1865', size=8)
    d.text(O[0], 30, 'BENZENE', size=8)
    d.text(296, 22, 'C₅H₁₂ · THREE TREES', size=8)
    return d


# --- karlsruhe ------------------------------------------------------------------------------------

def karlsruhe():
    """A vapour-density bulb in its bath, and Cannizzaro's carbon: every molecule holds a whole multiple of 12."""
    d = D()
    bx0, bx1, by0, by1 = 34, 176, 96, 236          # the bath, in section
    level = 112
    c, r = (100, 176), 34                          # the bulb
    na = math.radians(-128)                         # the neck leaves the bulb up and to the left
    n0 = (c[0] + r * math.cos(na), c[1] + r * math.sin(na))
    tip = (48, 40)
    d.group('thin')
    d.line((bx0 - 10, level), (bx1 + 10, level))
    d.line((c[0], by0 - 20), (c[0], by1 + 8))
    d.line((c[0] - r - 10, c[1]), (c[0] + r + 10, c[1]))
    d.group()
    d.line((bx0, by0), (bx0, by1), (bx1, by1), (bx1, by0))
    d.circle(*c, r)
    # the neck: two walls of a drawn-out tube, sealed at the tip once the bulb is full of vapour
    ux, uy = tip[0] - n0[0], tip[1] - n0[1]
    L = math.hypot(ux, uy)
    px, py = -uy / L * 2.2, ux / L * 2.2
    d.line((n0[0] + px, n0[1] + py), (tip[0] + px * 0.4, tip[1] + py * 0.4), (tip[0] - ux / L * 3, tip[1] - uy / L * 3),
           (tip[0] - px * 0.4, tip[1] - py * 0.4), (n0[0] - px, n0[1] - py))
    d.group('mid')
    # the thermometer beside the bulb, and the burner beneath the bath
    d.line((152, 58), (152, 214))
    d.line((158, 58), (158, 214))
    d.arc(155, 58, 3, 180, 360, n=8)
    d.circle(155, 220, 7)
    d.line((155, 213), (155, 130))
    d.lines([[(80, 262), (80, 250), (120, 250), (120, 262)], [(100, 250), (93, 243), (100, 238), (107, 243), (100, 250)]])
    d.lines([[(bx0 + 8 + 12 * k, level + 4), (bx0 + 14 + 12 * k, level + 4)] for k in range(12) if abs(bx0 + 11 + 12 * k - c[0]) > 40])
    # Cannizzaro's table: each molecule's weight (thin rule) and the carbon in it (bar), on one scale
    rows = [('CO', 28, 12), ('CO₂', 44, 12), ('CS₂', 76, 12), ('CH₄', 16, 12), ('C₂H₄', 28, 24), ('C₃H₆', 42, 36),
            ('C₄H₁₀O', 74, 48)]
    x0, s, y0, dy = 250, 1.7, 62, 26
    d.group('thin')
    for k in range(5):
        d.line((x0 + 12 * k * s, 46), (x0 + 12 * k * s, y0 + dy * 6 + 16))
    d.group('mid')
    for i, (f, m, cw) in enumerate(rows):
        y = y0 + dy * i
        d.line((x0, y), (x0 + m * s, y))
        d.line((x0 + m * s, y - 4), (x0 + m * s, y + 4))
    d.group()
    for i, (f, m, cw) in enumerate(rows):
        y = y0 + dy * i
        d.line((x0, y - 5), (x0 + cw * s, y - 5), (x0 + cw * s, y + 5), (x0, y + 5), closed=True)
    d.group('mid')
    for i, (f, m, cw) in enumerate(rows):
        d.text(x0 - 6, y0 + dy * i + 3, f, size=7, anchor='end')
    for k in range(1, 5):
        d.text(x0 + 12 * k * s, y0 + dy * 6 + 28, str(12 * k), size=7)
    d.text(318, 30, 'CARBON IN EACH MOLECULE', size=7)
    d.text(105, 284, 'VAPOUR DENSITY BULB', size=7)
    return d


PLATES = {'chirality': chirality, 'structure-theory': structure_theory, 'karlsruhe': karlsruhe}
