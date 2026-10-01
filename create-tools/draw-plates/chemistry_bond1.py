"""Plates for the chemistry subject's The chemical bond segment, part bond1 (sprint 025):
crystallography, electron-pair, quantum-chemistry."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _along(p, u, t):
    return (p[0] + u[0] * t, p[1] + u[1] * t)


def _foot(p, a, u):
    """The foot of the perpendicular from point p to the line through a with unit direction u."""
    t = (p[0] - a[0]) * u[0] + (p[1] - a[1]) * u[1]
    return (a[0] + u[0] * t, a[1] + u[1] * t)


def crystallography():
    """Bragg reflection of copper K-alpha X-rays from the (200) planes of rock salt, in section."""
    d = D()
    s = 30                                        # 2.82 angstroms between neighbouring planes, to scale
    th = math.degrees(math.asin(1.5406 / (2 * 2.8201)))   # the Bragg angle, 15.85 degrees
    ox, oy, cols, rows = 50, 150, 11, 4           # the lattice's first atom, and its size
    atoms = [(ox + i * s, oy + j * s, (i + j) % 2) for i in range(cols) for j in range(rows)]
    p0 = (ox + 5 * s, oy)                         # where the upper ray reflects, and the lower one below it
    p1 = (p0[0], oy + s)
    u = (math.cos(math.radians(th)), math.sin(math.radians(th)))    # incoming, down and to the right
    v = (u[0], -u[1])                                                # reflected, up and to the right
    a0, b0 = _along(p0, u, -130), _along(p0, v, 120)
    # the lower ray starts and ends on the same wavefronts as the upper one
    a1 = _along(p1, u, (a0[0] - p1[0]) * u[0] + (a0[1] - p1[1]) * u[1])
    b1 = _along(p1, v, (b0[0] - p1[0]) * v[0] + (b0[1] - p1[1]) * v[1])
    fa, fb = _foot(p0, p1, u), _foot(p0, p1, v)   # the wavefronts: perpendiculars from the upper point
    d.group('thin')
    # the reflecting planes, the normal through both reflection points, and the wavefronts
    for j in range(rows):
        d.line((ox - 14, oy + j * s), (ox + (cols - 1) * s + 14, oy + j * s))
    d.line((p0[0], oy - 70), (p0[0], oy + (rows - 1) * s + 12))
    d.line(p0, fa)
    d.line(p0, fb)
    d.group()
    # the ions: chlorine large, sodium small, alternating along every row and column
    for x, y, k in atoms:
        d.circle(x, y, 9 if k == 0 else 4.5)
    d.group('mid')
    # two rays of one wavelength: the lower travels the extra 2d sin(theta), drawn heavy
    d.line(a0, p0, b0)
    d.line(a1, p1, b1)
    d.line(fa, p1, fb)
    d.group('mid')
    # the glancing angle at the lower reflection, and arrowheads
    d.arc(p1[0], p1[1], 42, 180, 180 + th, n=16)
    d.arc(p1[0], p1[1], 42, 360 - th, 360, n=16)
    for tip, w in ((b0, v), (b1, v)):
        d.line(_pt(tip, math.degrees(math.atan2(w[1], w[0])) + 150, 8), tip,
               _pt(tip, math.degrees(math.atan2(w[1], w[0])) - 150, 8))
    # the dimension of d, beside the lattice
    xr = ox + (cols - 1) * s + 22
    d.line((xr, oy), (xr, oy + s))
    d.lines([[(xr - 4, oy), (xr + 4, oy)], [(xr - 4, oy + s), (xr + 4, oy + s)]])
    d.group('mid')
    q = _pt(p1, 180 + th / 2, 56)
    d.text(q[0] - 4, q[1] + 3.5, 'θ', size=10)
    d.text(xr + 6, oy + s / 2 + 3, 'd', size=10, anchor='start')
    d.text(p0[0] + 4, oy + (rows - 1) * s + 28, 'Cl⁻ LARGE · Na⁺ SMALL · (200) PLANES', size=8)
    d.text(200, 34, 'nλ = 2d sin θ', size=11)
    d.text(200, 52, 'Cu Kα 1.5406 Å · d 2.820 Å · θ 15.85°', size=8)
    return d


def _cube(o, e, k):
    """Corners of a cube of edge e at o, in oblique projection: x right, y up, z back at 30 degrees."""
    def P(x, y, z):
        return (o[0] + e * (x + k * z * math.cos(math.radians(30))), o[1] - e * (y + k * z * math.sin(math.radians(30))))
    return P


def electron_pair():
    """Lewis's cubical atoms: two chlorine cubes sharing an edge, and dot structures by counting."""
    d = D()
    e, k = 62, 0.55
    P = _cube((70, 150), e, k)
    cubes = [(0, 0, 0), (1, 0, 1)]              # the second cube shares the edge x = 1, z = 1 of the first
    edges = []
    corners = set()
    for cx, cy, cz in cubes:
        for x in (0, 1):
            for y in (0, 1):
                for z in (0, 1):
                    corners.add((cx + x, cy + y, cz + z))
        for a in range(8):
            ax, ay, az = a & 1, (a >> 1) & 1, (a >> 2) & 1
            for b in (1, 2, 4):
                if not a & b:
                    bx, by, bz = (a | b) & 1, ((a | b) >> 1) & 1, ((a | b) >> 2) & 1
                    edges.append([P(cx + ax, cy + ay, cz + az), P(cx + bx, cy + by, cz + bz)])
    shared = [(1, 0, 1), (1, 1, 1)]
    d.group('thin')
    d.lines(edges)
    # the two kernels at the cubes' centres, and the line of the bond through the shared edge
    c0, c1 = P(0.5, 0.5, 0.5), P(1.5, 0.5, 1.5)
    d.line(c0, c1)
    d.group()
    for c in sorted(corners):
        x, y = P(*c)
        d.circle(x, y, 4.2)
    d.group('mid')
    for c in (c0, c1):
        d.circle(*c, 7)
    m = P(1, 0.5, 1)
    d.ellipse(m[0], m[1], 11, e / 2 + 11)
    # dot structures below: every atom's shell counted to eight, hydrogen's to two
    y0 = 252
    dots = []

    def shell(cx, cy, sides, gap=5.5, r=11):
        for side in sides:
            a = {'n': -90, 's': 90, 'e': 0, 'w': 180}[side]
            for sgn in (-1, 1):
                p = _pt((cx, cy), a, r)
                q = _pt(p, a + 90, sgn * gap / 2)
                dots.append(q)

    # H:O:H with two lone pairs on oxygen
    shell(70, y0, 'news')
    # NH3: three bonding pairs and one lone pair on nitrogen
    shell(200, y0, 'news')
    # O::C::O: two pairs between each oxygen and carbon, two lone pairs on each oxygen
    shell(300, y0, 'ew', gap=5.5, r=11)
    shell(300, y0, 'ew', gap=11, r=11)
    for ox in (270, 330):
        shell(ox, y0, 'ns')
    shell(270, y0, 'w')
    shell(330, y0, 'e')
    d.group()
    for x, y in dots:
        d.circle(x, y, 1.6)
    d.group('mid')
    d.text(c0[0], c0[1] + 3.5, 'Cl', size=9)
    d.text(c1[0], c1[1] + 3.5, 'Cl', size=9)
    d.text(m[0] - 16, P(1, 0, 1)[1] + 26, 'SHARED PAIR', size=8, anchor='start')
    for x, s in ((70, 'O'), (48, 'H'), (92, 'H'), (200, 'N'), (178, 'H'), (222, 'H'), (200, y0 + 22),
                 (270, 'O'), (300, 'C'), (330, 'O')):
        if isinstance(s, str):
            d.text(x, y0 + 3.5, s, size=10)
        else:
            d.text(200, s + 3.5, 'H', size=10)
    d.text(200, 212, 'EACH SHELL COUNTED TO EIGHT · H TO TWO', size=7)
    return d


def _morse(De, re, nu):
    """A Morse curve from a well depth (eV), a bond length (angstrom) and a vibration (cm^-1)."""
    mu = 0.50391 * 1.66054e-27                   # reduced mass of H2, kg
    omega = 2 * math.pi * 2.99792458e10 * nu      # rad/s
    k = mu * omega ** 2                           # N/m
    a = math.sqrt(k / (2 * De * 1.602177e-19)) * 1e-10   # per angstrom
    return lambda r: De * (1 - math.exp(-a * (r - re))) ** 2 - De


def quantum_chemistry():
    """H2's potential well: Heitler-London-Sugiura against experiment, as Morse curves from Pauling and Wilson's table."""
    d = D()
    X0, X1, Y0 = 60, 370, 110                    # plot left, right, and the zero of energy
    rx = lambda r: X0 + (r - 0.3) / (3.0 - 0.3) * (X1 - X0)
    ey = lambda E: Y0 - E * 34                    # 34 px per electronvolt, energy down
    hl = _morse(3.14, 0.80, 4800)
    ex = _morse(4.72, 0.7395, 4317.9)
    d.group('thin')
    d.line((X0, Y0 - 50), (X0, ey(-5.2)))
    d.line((X0, Y0), (X1, Y0))
    ticks = []
    for r in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        ticks.append([(rx(r), Y0 - 3), (rx(r), Y0 + 3)])
    for E in (-1, -2, -3, -4, -5):
        ticks.append([(X0 - 3, ey(E)), (X0 + 3, ey(E))])
    d.lines(ticks)
    d.line((rx(0.80), ey(-3.14)), (rx(0.80), Y0))
    d.line((rx(0.7395), ey(-4.72)), (rx(0.7395), Y0))
    for r, De, x in ((0.80, 3.14, rx(2.2)), (0.7395, 4.72, rx(2.75))):
        d.line((rx(r) + 6, ey(-De)), (x - 6, ey(-De)))
    d.group()

    def curve(f):
        pts = []
        for i in range(0, 241):
            r = 0.36 + i * (3.0 - 0.36) / 240
            E = f(r)
            if E < 1.4:
                pts.append((rx(r), ey(E)))
        return pts
    d.line(*curve(ex))
    d.group('mid')
    d.line(*curve(hl))
    # the two well depths as dimension lines
    for De, x in ((3.14, rx(2.2)), (4.72, rx(2.75))):
        d.line((x, Y0), (x, ey(-De)))
        d.lines([[(x - 4, Y0), (x + 4, Y0)], [(x - 4, ey(-De)), (x + 4, ey(-De))]])
    # a key: the calculated curve at mid weight, the measured one at full
    d.line((282, 34), (302, 34))
    d.group()
    d.line((282, 50), (302, 50))
    # two hydrogen atoms at the measured distance, their 1s clouds overlapping, drawn at a larger scale
    hx, hy, sc = 180, 52, 70
    for sgn in (-1, 1):
        c = (hx + sgn * 0.7395 / 2 * sc, hy)
        d.circle(*c, 0.529 * sc)
        d.circle(*c, 1.8)
    d.group('mid')
    d.text(rx(2.2) + 6, ey(-1.57) + 3, '3.14 eV', size=8, anchor='start')
    d.text(rx(2.75) + 6, ey(-2.36) + 3, '4.72', size=8, anchor='start')
    d.text(308, 37, 'CALCULATED, 1927', size=7, anchor='start')
    d.text(308, 53, 'MEASURED, 1935', size=7, anchor='start')
    d.text(X1, Y0 - 8, 'R / Å', size=8, anchor='end')
    d.text(X0 + 6, Y0 - 44, 'E / eV', size=8, anchor='start')
    for r in (1.0, 2.0, 3.0):
        d.text(rx(r), Y0 + 14, f'{r:.0f}', size=8)
    d.text(X0 - 8, ey(-5) + 3, '−5', size=8, anchor='end')
    d.text(X0 - 8, Y0 + 3, '0', size=8, anchor='end')
    d.text(hx, hy - 44, 'H₂ · TWO 1s ORBITALS', size=7)
    return d


PLATES = {'crystallography': crystallography, 'electron-pair': electron_pair, 'quantum-chemistry': quantum_chemistry}
