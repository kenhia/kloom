"""Plates for How We Build's Materials science trail, part two: cracks, dislocations, carbon fibre (sprint 026)."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def griffith_cracks():
    """A plate in tension with a central crack, the stress along the crack's line, and Griffith's curve."""
    d = D()
    # the plate, in plan
    px0, px1, py0, py1 = 30, 190, 70, 250
    cx, cy = (px0 + px1) / 2, (py0 + py1) / 2
    a = 34                                       # half the crack's length
    d.group('thin')
    d.line((px0 - 10, cy), (px1 + 10, cy))       # the crack's line produced
    d.line((cx, py0 - 30), (cx, py1 + 30))
    # the stress along the crack's line ahead of a tip: σ x / √(x² − a²), the Westergaard solution, drawn above it
    sig, k = 10, 1.0                             # the far stress, in px, drawn upwards from the line
    pts = []
    for i in range(1, 60):
        x = a + (px1 - cx - a) * (i / 59) ** 2
        s = sig * x / math.sqrt(x * x - a * a)
        pts.append((cx + x, cy - min(s, 70)))
    d.line(*pts)
    d.line(*[(2 * cx - x, y) for x, y in pts])
    d.line((px0, cy - sig), (px1, cy - sig))     # the far stress, for comparison
    # dimension line for the crack, below it
    d.line((cx - a, cy + 16), (cx + a, cy + 16))
    d.lines([[(cx - a, cy + 12), (cx - a, cy + 20)], [(cx + a, cy + 12), (cx + a, cy + 20)]])
    d.group()
    d.line((px0, py0), (px1, py0), (px1, py1), (px0, py1), closed=True)
    # the crack: a very thin ellipse
    d.line(*[(cx + a * math.cos(math.radians(t)), cy + 1.6 * math.sin(math.radians(t))) for t in range(0, 361, 10)])
    d.group('mid')
    # the load: arrows pulling the top and bottom edges apart
    arrows = []
    for i in range(6):
        x = px0 + 14 + i * (px1 - px0 - 28) / 5
        arrows.append([(x, py0 - 6), (x, py0 - 26)])
        arrows.append([(x - 3, py0 - 21), (x, py0 - 26), (x + 3, py0 - 21)])
        arrows.append([(x, py1 + 6), (x, py1 + 26)])
        arrows.append([(x - 3, py1 + 21), (x, py1 + 26), (x + 3, py1 + 21)])
    d.lines(arrows)
    # Griffith's curve: the breaking stress against the crack's half-length, σ ∝ 1/√a
    gx0, gy0, gw, gh = 236, 250, 140, 170       # origin and size of the axes
    d.group('thin')
    a1, a2 = 0.25, 0.5                           # two half-lengths, as fractions of the axis
    s1 = 0.22 / math.sqrt(a1)
    s2 = 0.22 / math.sqrt(a2)
    for av, sv in ((a1, s1), (a2, s2)):
        x, y = gx0 + av * gw, gy0 - sv * gh
        d.line((x, gy0), (x, y), (gx0, y))
    d.group()
    d.line((gx0, gy0 - gh - 6), (gx0, gy0), (gx0 + gw + 6, gy0))
    curve = []
    for i in range(81):
        av = 0.06 + 0.94 * i / 80
        curve.append((gx0 + av * gw, gy0 - min(0.22 / math.sqrt(av), 1) * gh))
    d.line(*curve)
    d.group('mid')
    d.text(cx, cy + 30, '2a', size=8)
    d.text(cx, py0 - 34, 'σ', size=9)
    d.text(cx, cy - 40, 'TIP STRESS', size=7)
    d.text(gx0 + a1 * gw, gy0 + 12, 'a', size=8)
    d.text(gx0 + a2 * gw, gy0 + 12, '2a', size=8)
    d.text(gx0 - 5, gy0 - s1 * gh + 3, '1', size=8, anchor='end')
    d.text(gx0 - 5, gy0 - s2 * gh + 3, '0.71', size=8, anchor='end')
    d.text(gx0 + gw / 2 + 14, gy0 - gh - 10, 'BREAKING STRESS', size=7)
    d.text(gx0 + gw - 2, gy0 + 24, 'CRACK', size=7, anchor='end')
    d.text(cx, 290, 'A CRACKED PLATE IN TENSION', size=8)
    return d


PLATES = {'griffith-cracks': griffith_cracks}


def _edge_displacement(x, y, b, nu=0.33):
    """The displacement of a point (x, y) from an edge dislocation at the origin, Burgers vector b along x (Volterra's solution)."""
    r2 = x * x + y * y
    if r2 < 1e-9:
        return 0, 0
    th = math.atan2(y, x)
    ux = b / (2 * math.pi) * (th + x * y / (2 * (1 - nu) * r2))
    uy = -b / (2 * math.pi) * ((1 - 2 * nu) / (4 * (1 - nu)) * math.log(r2) + (x * x - y * y) / (4 * (1 - nu) * r2))
    return ux, uy


def dislocations():
    """An edge dislocation in a square lattice, its atoms placed by the elastic solution, and the ruck in a rug."""
    d = D()
    s = 17                                       # the lattice spacing, px
    ox, oy = 130, 150                            # the dislocation's core, on the slip plane
    rows = range(-4, 6)
    # atoms: above the slip plane there is one extra half column (index 0 lies on the core's line);
    # rows above (j > 0) carry columns at i, rows below at i + ½ so the half plane ends at the core.
    # each atom is a perfect-lattice site moved by the elastic field (b = one spacing, y measured upwards);
    # the angle term opens a slip of one spacing along the half plane x < 0, so the top half holds one extra column
    atoms = {}
    lim = 6.3 * s
    for j in rows:
        yc = (j - 0.5) * s                       # rows sit half a spacing off the slip plane, y down
        for i in range(-8, 9):
            x0 = i * s + 0.01
            ux, uy = _edge_displacement(x0, -yc, s)
            x, y = x0 + ux, yc - uy
            if abs(x) <= lim:
                atoms[(i, j)] = (ox + x, oy + y)
    d.group('thin')
    d.line((ox - 6.8 * s, oy), (ox + 6.6 * s, oy))   # the slip plane
    # the lattice planes: each column of atoms joined top to bottom; the extra half plane stops at the core
    segs = []
    for i in range(-8, 9):
        segs.append([atoms[(i, j)] for j in rows if j > 0 and (i, j) in atoms])
        segs.append([atoms[(i, j)] for j in rows if j <= 0 and (i, j) in atoms])
    d.lines(segs)
    d.group()
    # the atoms
    for p in atoms.values():
        d.circle(p[0], p[1], 3.1)
    d.group('mid')
    # the extra half plane, drawn heavier, ending at the core
    half = [atoms[(0, j)] for j in rows if j <= 0 and (0, j) in atoms]
    d.line(*half)
    # the core's symbol: ⊥
    d.line((ox - 7, oy + 2), (ox + 7, oy + 2))
    d.line((ox, oy + 2), (ox, oy - 10))
    # the shear that drives it: arrows above and below
    ytop, ybot = oy - 4.5 * s - 14, oy + 5.5 * s + 12
    d.lines([[(ox - 60, ytop), (ox + 20, ytop)], [(ox + 14, ytop - 4), (ox + 20, ytop), (ox + 14, ytop + 4)],
             [(ox + 60, ybot), (ox - 20, ybot)], [(ox - 14, ybot - 4), (ox - 20, ybot), (ox - 14, ybot + 4)]])
    # the rug and its ruck, beside the lattice: a floor, a rug with a hump, and the arrow it moves along
    rx0, ry = 268, 210
    d.group('thin')
    d.line((rx0 - 6, ry + 3), (rx0 + 122, ry + 3))
    d.group()
    rug = []
    for i in range(61):
        x = rx0 + 116 * i / 60
        h = 12 * math.exp(-((x - (rx0 + 52)) / 9) ** 2)
        rug.append((x, ry - h))
    d.line(*rug)
    d.group('mid')
    d.lines([[(rx0 + 40, ry - 26), (rx0 + 76, ry - 26)], [(rx0 + 70, ry - 30), (rx0 + 76, ry - 26), (rx0 + 70, ry - 22)]])
    d.text(ox, 22, 'AN EDGE DISLOCATION', size=8)
    d.text(ox + 6.5 * s + 4, oy + 3, 'SLIP PLANE', size=7, anchor='start')
    d.text(rx0 + 58, ry + 20, 'A RUCK IN A RUG', size=7)
    d.text(rx0 + 58, ry - 34, 'ONE STEP AT A TIME', size=7)
    return d


PLATES['dislocations'] = dislocations


def _iso(x, y, z, ox, oy, k=1.0):
    """A cabinet oblique projection: x to the right, y receding up and to the right, z up."""
    return ox + (x - 0.55 * y) * k, oy + (0.5 * y) * k - z * k


def _clip_line(p, u, half):
    """Clip the line through p along u to the square |x|, |y| ≤ half; return its two ends or None."""
    ts = []
    for axis in (0, 1):
        if abs(u[axis]) > 1e-9:
            for b in (-half, half):
                t = (b - p[axis]) / u[axis]
                q = (p[0] + u[0] * t, p[1] + u[1] * t)
                if abs(q[1 - axis]) <= half + 1e-6:
                    ts.append(t)
    if len(ts) < 2:
        return None
    t0, t1 = min(ts), max(ts)
    if t1 - t0 < 1e-6:
        return None
    return (p[0] + u[0] * t0, p[1] + u[1] * t0), (p[0] + u[0] * t1, p[1] + u[1] * t1)


def carbon_fibre():
    """Four plies of a quasi-isotropic laminate, exploded, and the stiffness of one ply and of the stack by direction."""
    d = D()
    half = 40                                    # half a ply's side, in ply units
    ox, oy = 108, 54                             # where the top ply's centre projects
    gap = 64                                     # the explosion between plies
    plies = [0, 45, -45, 90]
    d.group('thin')
    # the stacking axis through the centres
    d.line(_iso(0, 0, 30, ox, oy), _iso(0, 0, -gap * 3 - 20, ox, oy))
    d.group()
    for k, ang in enumerate(plies):
        z = -gap * k
        corners = [(-half, -half), (half, -half), (half, half), (-half, half)]
        d.line(*[_iso(x, y, z, ox, oy) for x, y in corners], closed=True)
    d.group('mid')
    for k, ang in enumerate(plies):
        z = -gap * k
        u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
        n = (-u[1], u[0])
        segs = []
        for m in range(-9, 10):
            p = (n[0] * m * 7.5, n[1] * m * 7.5)
            e = _clip_line(p, u, half - 1)
            if e:
                segs.append([_iso(e[0][0], e[0][1], z, ox, oy), _iso(e[1][0], e[1][1], z, ox, oy)])
        d.lines(segs)
    # the stiffness of a unidirectional ply against direction, and of the quasi-isotropic stack (a circle),
    # from classical lamination theory with the NASA RP-1351 ply (E1 138, E2 8.97, G12 6.90 GPa, ν12 0.3)
    E1, E2, G, v12 = 138.0, 8.97, 6.90, 0.3
    pcx, pcy, sc = 318, 150, 0.5                 # the polar plot's centre and px per GPa
    d.group('thin')
    for r in (50, 100, 140):
        d.circle(pcx, pcy, r * sc)
    for t in (0, 45, 90, 135):
        u = _dir(t)
        d.line((pcx - u[0] * 74, pcy - u[1] * 74), (pcx + u[0] * 74, pcy + u[1] * 74))
    d.group()
    ud = []
    for i in range(361):
        t = math.radians(i)
        c, s = math.cos(t), math.sin(t)
        inv = c ** 4 / E1 + (1 / G - 2 * v12 / E1) * s * s * c * c + s ** 4 / E2
        e = 1 / inv
        ud.append((pcx + e * sc * c, pcy - e * sc * s))
    d.line(*ud)
    d.group('mid')
    d.circle(pcx, pcy, 54.7 * sc)
    for k, ang in enumerate(plies):
        lx, ly = _iso(half, -half, -gap * k, ox, oy)
        d.text(lx + 10, ly + 3, {0: '0°', 45: '+45°', -45: '−45°', 90: '90°'}[ang], size=8, anchor='start')
    d.text(ox, 284, '[0/±45/90]s, HALF SHOWN', size=8)
    d.text(pcx, pcy - 80, 'STIFFNESS BY DIRECTION', size=7)
    d.text(pcx + 58, pcy - 14, 'ONE PLY', size=7)
    d.text(pcx, pcy + 44, 'THE STACK', size=7)
    return d


PLATES['carbon-fibre'] = carbon_fibre
