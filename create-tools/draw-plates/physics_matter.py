"""physics plates, segment "The quantum": QED, solids, superconductivity and quantum computing (sprint 021). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def qed():
    """Vacuum polarisation: a bare charge screened by virtual pairs, and the charge that runs.

    Left, an electron at the centre of rings of short-lived electron-positron
    pairs, each pair a small dipole turned with its positive end inward, so a
    probe far away sees less charge than one close in. Right, alpha against
    the log of the energy: 137.036 at low energy and 127.93 at the Z boson's
    91 GeV (the PDG's values); the line between is drawn straight, as the
    running is roughly logarithmic, and is a schematic, not a calculation."""
    d = D()
    cx, cy = 118, 150
    rings = [(34, 8), (56, 12), (80, 16), (104, 20)]
    # construction: the rings the pairs sit on, and the two probe distances
    d.group('thin')
    for r, _ in rings:
        d.circle(cx, cy, r)
    d.line((cx, cy), (cx + 22 * math.cos(math.radians(-35)), cy + 22 * math.sin(math.radians(-35))))
    d.line((cx, cy), (cx + 112 * math.cos(math.radians(35)), cy + 112 * math.sin(math.radians(35))))
    # the bare charge
    d.group()
    d.circle(cx, cy, 7)
    d.line((cx - 3.5, cy), (cx + 3.5, cy))
    # the virtual pairs: each a short dipole along the radius, + end toward the centre
    d.group('mid')
    for r, n in rings:
        for k in range(n):
            a = 2 * math.pi * (k + 0.5 * (r % 2)) / n + r * 0.013
            ux, uy = math.cos(a), math.sin(a)
            px, py = cx + (r - 5) * ux, cy + (r - 5) * uy     # positive end, inward
            qx, qy = cx + (r + 5) * ux, cy + (r + 5) * uy     # negative end, outward
            d.line((px, py), (qx, qy))
            d.circle(px, py, 1.6)
    # the probes
    d.group()
    for dist, ang in ((22, -35), (112, 35)):
        x, y = cx + dist * math.cos(math.radians(ang)), cy + dist * math.sin(math.radians(ang))
        d.circle(x, y, 2.5)
    # right: 1/alpha against energy, on log axes
    x0, x1, y0, y1 = 262, 380, 222, 78       # plot box: x log10(E/eV) from 5 to 12, y 1/alpha from 139 to 126
    def px(logE):
        return x0 + (logE - 5) / 7 * (x1 - x0)
    def py(inv):
        return y0 + (inv - 139) / (126 - 139) * (y1 - y0)
    d.group('thin')
    for inv in (128, 131, 134, 137):
        d.line((x0, py(inv)), (x1, py(inv)))
    for le in (6, 8, 10):
        d.line((px(le), y0), (px(le), y1))
    d.group()
    d.line((x0, y1 - 6), (x0, y0), (x1 + 6, y0))
    _arrow(d, x0, y1 - 6, -math.pi / 2, 4)
    _arrow(d, x1 + 6, y0, 0, 4)
    lo = (px(5.7), py(137.036))                   # the electron's mass, 0.511 MeV
    hi = (px(math.log10(91.19e9)), py(127.93))  # the Z boson, 91.19 GeV
    d.line((x0, lo[1]), lo, hi)
    d.circle(*lo, 3)
    d.circle(*hi, 3)
    d.group()
    d.text(cx, 282, 'A CHARGE SCREENED BY VIRTUAL PAIRS', size=7)
    d.text(cx + 30, cy - 22, 'NEAR', size=7, anchor='start')
    d.text(cx + 98, cy + 80, 'FAR', size=7, anchor='start')
    d.text(lo[0] + 4, lo[1] + 14, '1/137.036', size=7, anchor='start')
    d.text(hi[0], hi[1] - 9, '1/127.93', size=7, anchor='end')
    d.text((x0 + x1) / 2, y0 + 16, 'ENERGY (LOG) →', size=7)
    d.text(x0 - 4, y1 - 12, 'α', size=8, anchor='start')
    d.text((x0 + x1) / 2, 282, 'THE CHARGE RUNS', size=7)
    return d


def solids():
    """Bands and gaps: nearly-free electrons in a one-dimensional lattice, and the three kinds of solid.

    Left, the energy of an electron against its wave number k, folded into the
    first Brillouin zone: free-electron parabolas (construction) split by a
    weak periodic potential into bands with gaps at the zone centre and edge
    (the central equation on seven plane waves, with a potential of two
    Fourier components, diagonalised). Right, the
    band filling of a metal, a semiconductor and an insulator."""
    d = D()
    ox, oy, W, H = 40, 250, 170, 200        # plot origin and size: k from -pi/a to pi/a, E from 0 to Emax
    G = 2 * math.pi                        # reciprocal lattice vector, with a = 1
    Emax = 5.6 * (G / 2) ** 2              # in units where E = k^2
    V = 0.2 * (G / 2) ** 2
    def P(k, E):
        return (ox + (k / (G / 2) + 1) * W / 2, oy - E / Emax * H)
    ks = [-G / 2 + G * i / 120 for i in range(121)]
    # construction: the free-electron parabolas, folded; the zone edges
    d.group('thin')
    for n in (-2, -1, 0, 1, 2):
        pts = [P(k, (k + n * G) ** 2) for k in ks if (k + n * G) ** 2 <= Emax]
        if len(pts) > 1:
            d.line(*pts)
    d.line(P(-G / 2, 0), P(-G / 2, Emax))
    d.line(P(G / 2, 0), P(G / 2, Emax))
    # the bands: the central equation on plane waves k + nG (n = -3..3), coupled by V, diagonalised
    def bands(k):
        n = 7
        A = [[0.0] * n for _ in range(n)]
        for i in range(n):
            A[i][i] = (k + (i - 3) * G) ** 2
            if i + 1 < n:
                A[i][i + 1] = A[i + 1][i] = V
            if i + 2 < n:
                A[i][i + 2] = A[i + 2][i] = 0.8 * V   # a second Fourier component, which opens the gap at the centre
        for _ in range(60):                     # cyclic Jacobi sweeps
            for p in range(n):
                for q in range(p + 1, n):
                    if abs(A[p][q]) < 1e-12:
                        continue
                    t = (A[q][q] - A[p][p]) / (2 * A[p][q])
                    t = (1 if t >= 0 else -1) / (abs(t) + math.sqrt(t * t + 1))
                    c = 1 / math.sqrt(t * t + 1)
                    sn = t * c
                    for r in range(n):
                        arp, arq = A[r][p], A[r][q]
                        A[r][p], A[r][q] = c * arp - sn * arq, sn * arp + c * arq
                    for r in range(n):
                        apr, aqr = A[p][r], A[q][r]
                        A[p][r], A[q][r] = c * apr - sn * aqr, sn * apr + c * aqr
        return sorted(A[i][i] for i in range(n))
    d.group()
    table = [(k, bands(k)) for k in ks]
    for i in range(4):
        pts = [P(k, e[i]) for k, e in table if e[i] <= Emax]
        if len(pts) > 1:
            d.line(*pts)
    d.line((ox, oy - H - 6), (ox, oy), (ox + W + 6, oy))
    _arrow(d, ox, oy - H - 6, -math.pi / 2, 4)
    # the gaps: at the zone edge between bands 1 and 2, at the centre between 2 and 3, at the edge between 3 and 4
    d.group('mid')
    for i, k in ((0, G / 2), (1, 0.0), (2, G / 2)):
        e = bands(k)
        if e[i + 1] <= Emax:
            x = P(k, 0)[0] - (10 if k else 0)
            d.lines([[(x - 6, P(k, e[i])[1]), (x + 6, P(k, e[i])[1])], [(x - 6, P(k, e[i + 1])[1]), (x + 6, P(k, e[i + 1])[1])],
                     [(x, P(k, e[i])[1]), (x, P(k, e[i + 1])[1])]])
    # right: three solids, bands as boxes, filled part hatched
    d.group()
    cols = [('METAL', [(0, 50, 30), (58, 110, 0)]),
            ('SEMI-', [(0, 60, 60), (72, 120, 0)]),
            ('INSULATOR', [(0, 40, 40), (98, 140, 0)])]
    bx, by, bw = 250, 230, 34
    for j, (name, bs) in enumerate(cols):
        x = bx + j * 48
        for lo, hi, filled in bs:
            d.line((x, by - lo), (x + bw, by - lo), (x + bw, by - hi), (x, by - hi), closed=True)
    d.group('mid')
    for j, (name, bs) in enumerate(cols):
        x = bx + j * 48
        for lo, hi, filled in bs:
            if filled:
                d.lines([[(x, by - y), (x + bw, by - y)] for y in range(lo + 4, lo + filled, 4)])
    d.group()
    d.text(ox + W / 2, 282, 'ENERGY AGAINST WAVE NUMBER', size=7)
    d.text(ox - 3, oy + 12, '−π/a', size=7, anchor='start')
    d.text(ox + W, oy + 12, 'π/a', size=7, anchor='end')
    d.text(ox + 4, oy - H - 4, 'E', size=8, anchor='start')
    for j, (name, bs) in enumerate(cols):
        d.text(bx + j * 48 + bw / 2, by + 14, name, size=6)
    d.text(bx + 48 + bw / 2, by + 23, 'CONDUCTOR', size=6)
    d.text(bx + 72, 282, 'BANDS · GAPS · FILLING', size=7)
    return d


def superconductivity():
    """Two signatures of a superconductor: resistance that vanishes, and a field that is pushed out.

    Left, the resistance of mercury against temperature in the manner of the
    Leiden plot of 26 October 1911: falling gently, then dropping at 4.2 K to
    nothing measurable (the gentle part is a schematic). Right, magnetic field
    lines round a superconducting cylinder in a uniform field, computed as the
    streamlines of flow round a cylinder, psi = y (1 - a^2 / r^2): the Meissner
    effect."""
    d = D()
    # left: R against T
    x0, x1, y0, y1 = 36, 176, 226, 70
    T0, T1 = 4.0, 4.4
    def P(T, R):
        return (x0 + (T - T0) / (T1 - T0) * (x1 - x0), y0 - R / 0.15 * (y0 - y1))
    d.group('thin')
    for T in (4.1, 4.2, 4.3):
        d.line(P(T, 0), P(T, 0.15))
    for R in (0.05, 0.1):
        d.line(P(T0, R), P(T1, R))
    d.group()
    d.line((x0, y1 - 6), (x0, y0), (x1 + 6, y0))
    _arrow(d, x0, y1 - 6, -math.pi / 2, 4)
    _arrow(d, x1 + 6, y0, 0, 4)
    Tc = 4.2
    pts = [P(T0, 0.0), P(Tc - 0.002, 0.0), P(Tc + 0.006, 0.105)]
    pts += [P(Tc + 0.006 + 0.194 * i / 20, 0.105 + 0.02 * (i / 20) ** 1.3) for i in range(1, 21)]
    d.line(*pts)
    d.group('mid')
    for T in (4.05, 4.1, 4.15, 4.19):
        d.circle(*P(T, 0.0), 1.8)
    for T in (4.22, 4.26, 4.32, 4.38):
        d.circle(*P(T, 0.105 + 0.02 * ((T - Tc - 0.006) / 0.194) ** 1.3), 1.8)
    # right: field lines round a cylinder
    cx, cy, a = 292, 148, 34
    d.group('thin')
    d.circle(cx, cy, a + 6)
    d.line((cx - 92, cy), (cx - a - 8, cy))
    d.line((cx + a + 8, cy), (cx + 92, cy))
    d.group()
    d.circle(cx, cy, a)
    d.group('mid')
    for c in (-44, -30, -18, -8, 8, 18, 30, 44):
        pts = []
        for i in range(81):
            x = -92 + 184 * i / 80
            # solve y (1 - a^2 / (x^2 + y^2)) = c for y, by bisection away from the cylinder
            lo, hi = (c, c + 60) if c > 0 else (c - 60, c)
            f = lambda y: y * (1 - a * a / (x * x + y * y)) - c
            if c > 0:
                lo, hi = max(1e-3, c), c + 80
            else:
                lo, hi = c - 80, min(-1e-3, c)
            for _ in range(60):
                m = (lo + hi) / 2
                if (f(lo) < 0) == (f(m) < 0):
                    lo = m
                else:
                    hi = m
            y = (lo + hi) / 2
            if x * x + y * y >= a * a:
                pts.append((cx + x, cy + y))
        d.line(*pts)
        _arrow(d, *pts[-1], 0, 3)
    d.group()
    d.text((x0 + x1) / 2, y0 + 14, 'T · KELVIN', size=7)
    d.text(P(Tc, 0)[0], y0 + 26, '4.2', size=7)
    d.text(x0 + 4, y1 - 4, 'R', size=8, anchor='start')
    d.text((x0 + x1) / 2, 282, 'MERCURY, 1911', size=7)
    d.text(cx, 282, 'FIELD PUSHED OUT, 1933', size=7)
    d.text(cx, cy + 3, 'S', size=9)
    return d


def quantum_computing():
    """A qubit and a two-qubit circuit.

    Left, the Bloch sphere: |0> at the north pole, |1> at the south, and a
    state at polar angle 60 degrees and azimuth 50 degrees, with the
    construction of its angles. Right, the circuit that makes an entangled
    Bell pair: a Hadamard gate on the first qubit, a controlled NOT onto the
    second, and a measurement of each."""
    d = D()
    cx, cy, R = 108, 150, 82
    th, ph = math.radians(60), math.radians(50)
    az, el = math.radians(-30), math.radians(18)     # the view: turned a little, and from a little above
    def P3(x, y, z):
        """Orthographic projection of a point on or in the unit sphere."""
        xr = x * math.cos(az) - y * math.sin(az)
        yr = x * math.sin(az) + y * math.cos(az)     # depth: positive is away from the viewer
        return (cx + R * xr, cy - R * (z * math.cos(el) + yr * math.sin(el)))
    d.group('thin')
    d.line(P3(-1.15, 0, 0), P3(1.15, 0, 0))
    d.line(P3(0, -1.15, 0), P3(0, 1.15, 0))
    d.line(P3(0, 0, -1.15), P3(0, 0, 1.15))
    sx, sy, sz = math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)
    d.line(P3(0, 0, 0), P3(sx, sy, 0), P3(sx, sy, sz))
    # the azimuth arc in the equator, and the polar arc to the state
    d.line(*[P3(0.35 * math.cos(t), 0.35 * math.sin(t), 0) for t in [ph * i / 20 for i in range(21)]])
    d.line(*[P3(0.3 * math.sin(t) * math.cos(ph), 0.3 * math.sin(t) * math.sin(ph), 0.3 * math.cos(t)) for t in [th * i / 20 for i in range(21)]])
    d.group()
    d.circle(cx, cy, R)                       # an orthographic sphere's outline is a circle
    d.line(*[P3(math.cos(t), math.sin(t), 0) for t in [2 * math.pi * i / 96 for i in range(97)]])
    d.group('mid')
    d.line(*[P3(math.sin(t), 0, math.cos(t)) for t in [2 * math.pi * i / 96 for i in range(97)]])
    d.group()
    tip = P3(sx, sy, sz)
    d.line(P3(0, 0, 0), tip)
    ang = math.atan2(tip[1] - P3(0, 0, 0)[1], tip[0] - P3(0, 0, 0)[0])
    _arrow(d, *tip, ang, 5)
    d.circle(*P3(0, 0, 1), 2.5)
    d.circle(*P3(0, 0, -1), 2.5)
    # right: the Bell-pair circuit
    xa, xb, y0, y1 = 222, 384, 118, 178
    d.group('thin')
    d.lines([[(xa, y0), (xb - 30, y0)], [(xa, y1), (xb - 30, y1)]])
    d.group()
    hx = 250
    d.line((hx - 11, y0 - 11), (hx + 11, y0 - 11), (hx + 11, y0 + 11), (hx - 11, y0 + 11), closed=True)
    d.lines([[(hx - 5, y0 - 6), (hx - 5, y0 + 6)], [(hx + 5, y0 - 6), (hx + 5, y0 + 6)], [(hx - 5, y0), (hx + 5, y0)]])
    tx = 300
    d.circle(tx, y0, 3.5)
    d.line((tx, y0), (tx, y1 + 9))
    d.circle(tx, y1, 9)
    d.line((tx - 9, y1), (tx + 9, y1))
    for y in (y0, y1):
        mx = xb - 18
        d.line((mx - 14, y - 11), (mx + 14, y - 11), (mx + 14, y + 11), (mx - 14, y + 11), closed=True)
        d.line(*[(mx + 9 * math.cos(math.pi + math.pi * i / 16), y + 5 + 9 * math.sin(math.pi + math.pi * i / 16)) for i in range(17)])
        d.line((mx, y + 5), (mx + 7, y - 6))
    d.group()
    d.text(*(lambda p: (p[0] + 6, p[1] - 5))(P3(0, 0, 1)), '|0⟩', size=8, anchor='start')
    d.text(*(lambda p: (p[0] + 6, p[1] + 10))(P3(0, 0, -1)), '|1⟩', size=8, anchor='start')
    d.text(tip[0] + 6, tip[1] - 2, 'ψ', size=9, anchor='start')
    d.text(xa - 4, y0 + 3, 'q0', size=7, anchor='end')
    d.text(xa - 4, y1 + 3, 'q1', size=7, anchor='end')
    d.text(cx, 282, 'ONE QUBIT: THE BLOCH SPHERE', size=7)
    d.text(303, 282, 'TWO: AN ENTANGLED PAIR', size=7)
    d.text(303, 212, '(|00⟩ + |11⟩)/√2', size=7)
    return d


PLATES = {'qed': qed, 'solids': solids, 'superconductivity': superconductivity,
          'quantum-computing': quantum_computing}
