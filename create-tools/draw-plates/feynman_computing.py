"""feynman plates, trail "Computing" (sprint 014). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def physics_of_computation():
    """Mead's transistor: an n-channel MOS transistor in section, and its current against gate voltage
    on a log scale, exponential below threshold like a nerve membrane's channels."""
    d = D()
    surf = 150            # the silicon surface
    # construction: the surface carried across, depth marks, the plot's decade grid
    ox, oy, w, h = 236, 236, 146, 150
    decades = 6
    d.group('thin')
    d.line((18, surf), (212, surf))
    d.lines([[(22, surf + k * 20), (28, surf + k * 20)] for k in range(0, 6)])
    d.line((115, 78), (115, 258))
    d.lines([[(ox, oy - h * k / decades), (ox + w, oy - h * k / decades)] for k in range(1, decades + 1)])
    d.lines([[(ox + w * k / 6, oy), (ox + w * k / 6, oy - h)] for k in range(1, 7)])
    # the transistor in section: body, source and drain wells, oxide, gate
    d.group()
    d.line((30, surf), (30, 252), (200, 252), (200, surf))
    d.line((30, surf), (200, surf))
    for cx in (62, 168):
        d.arc(cx, surf, 32, 0, 180, ry=26)
    d.line((88, surf), (88, surf - 7), (142, surf - 7), (142, surf))
    d.line((88, surf - 7), (88, surf - 31), (142, surf - 31), (142, surf - 7))
    # detail: the terminals, the channel of electrons under the gate
    d.group('mid')
    d.line((62, surf), (62, 104), (48, 104))
    d.line((168, surf), (168, 104), (182, 104))
    d.line((115, surf - 31), (115, 92))
    d.line((108, 92), (122, 92))
    d.line((94, surf + 3), (136, surf + 3))
    for k in range(6):
        d.circle(95 + k * 8, surf + 7, 1.6)
    _arrow(d, 138, surf + 7, 0, 4)
    # the curve: log current against gate voltage (a smooth EKV-style interpolation)
    d.group()
    d.line((ox, oy), (ox + w + 6, oy))
    d.line((ox, oy), (ox, oy - h - 8))
    _arrow(d, ox + w + 6, oy, 0, 4)
    _arrow(d, ox, oy - h - 8, -math.pi / 2, 4)
    vt, slope = 0.62, 0.045   # threshold as a fraction of the axis; the subthreshold slope (in axis units per e-fold)
    pts = []
    for i in range(121):
        v = i / 120
        cur = math.log1p(math.exp((v - vt) / (2 * slope))) ** 2
        lg = math.log10(cur)            # from about -7 to +1
        y = (lg + 6.4) / 8.0
        pts.append((ox + w * v, oy - h * max(0.0, min(1.0, y))))
    d.line(*pts)
    d.group('thin')
    d.line((ox + w * vt, oy), (ox + w * vt, oy - h))
    # labels
    d.group()
    d.text(62, 98, 'S', size=9)
    d.text(115, 86, 'G', size=9)
    d.text(168, 98, 'D', size=9)
    d.text(62, surf + 16, 'n+', size=8)
    d.text(168, surf + 16, 'n+', size=8)
    d.text(115, 240, 'p-TYPE SILICON', size=7)
    d.text(ox + w * vt, oy - h - 4, 'THRESHOLD', size=7)
    d.text(ox + 4, oy - h - 12, 'LOG I', size=7, anchor='start')
    d.text(ox + 12, oy - h * 0.62, 'e^(qV/nkT)', size=7, anchor='start')
    d.text(ox + w, oy + 16, 'GATE VOLTAGE', size=7, anchor='end')
    d.text(200, 28, 'BELOW THRESHOLD A TRANSISTOR IS AN EXPONENTIAL, LIKE A NERVE', size=7)
    return d


def connection_machine():
    """The router's problem: a hypercube (four dimensions of the CM-1's twelve), a message corrected one
    address bit per dimension, and the five buffers per chip that Feynman's equations allowed."""
    d = D()
    # each node's 4-bit address, bit 0 across, bit 1 up, bit 2 into the page, bit 3 into the second cube
    ex = [(62, 0), (0, -62), (30, -26), (150, 20)]
    base = (40, 214)

    def pos(n):
        x, y = base
        for b in range(4):
            if n >> b & 1:
                x += ex[b][0]
                y += ex[b][1]
        return x, y

    edges = [(n, n ^ (1 << b)) for n in range(16) for b in range(4) if n < n ^ (1 << b)]
    route = [0b0000, 0b0001, 0b0011, 0b1011]
    route_edges = {tuple(sorted(p)) for p in zip(route, route[1:])}
    # construction: the fourth dimension's edges, joining the two cubes
    d.group('thin')
    d.lines([[pos(a), pos(b)] for a, b in edges if a ^ b == 8 and (a, b) not in route_edges])
    # the two cubes
    d.group('mid')
    d.lines([[pos(a), pos(b)] for a, b in edges if a ^ b != 8 and (a, b) not in route_edges])
    d.group()
    for n in range(16):
        d.circle(*pos(n), 3.2)
    # the route, dimension by dimension
    d.group()
    for a, b in zip(route, route[1:]):
        (x0, y0), (x1, y1) = pos(a), pos(b)
        ang = math.atan2(y1 - y0, x1 - x0)
        sx, sy = x0 + 5 * math.cos(ang), y0 + 5 * math.sin(ang)
        tx, ty = x1 - 5 * math.cos(ang), y1 - 5 * math.sin(ang)
        d.line((sx, sy), (tx, ty))
        _arrow(d, tx, ty, ang, 5)
    d.circle(*pos(0), 6)
    d.circle(*pos(0b1011), 6)
    # a router chip's buffers: five built, the two the discrete analysis wanted
    bx, by = 312, 60
    d.group('mid')
    d.line((bx - 14, by - 12), (bx + 58, by - 12), (bx + 58, by + 108), (bx - 14, by + 108), closed=True)
    for k in range(5):
        d.line((bx, by + k * 14), (bx + 44, by + k * 14), (bx + 44, by + k * 14 + 10), (bx, by + k * 14 + 10),
               closed=True)
    d.group('thin')
    for k in (5, 6):
        d.line((bx, by + k * 14), (bx + 44, by + k * 14), (bx + 44, by + k * 14 + 10), (bx, by + k * 14 + 10),
               closed=True)
        d.line((bx, by + k * 14 + 10), (bx + 44, by + k * 14))
    # labels
    d.group()
    x0, y0 = pos(0)
    d.text(x0, y0 + 18, '0000', size=8)
    x1, y1 = pos(0b1011)
    d.text(x1 + 10, y1 + 16, '1011', size=8, anchor='start')
    d.text(bx + 22, by - 18, 'ROUTER', size=7)
    d.text(bx + 64, by + 32, '5', size=9, anchor='start')
    d.text(bx + 64, by + 90, '7?', size=9, anchor='start')
    d.text(200, 276, 'FROM 0000 TO 1011 · ONE HOP PER 1 IN THE ADDRESS · 12 DIMENSIONS IN THE CM-1', size=7)
    return d


def quantum_computers():
    """Feynman's full adder of reversible gates (1985, fig. 5), and under it the line of program sites
    his cursor hops along, each hop applying the next gate: H = sum of q*(i+1) q(i) A(i+1) + c.c."""
    d = D()
    wires = {'a': 56, 'b': 84, 'c': 112, 'd': 140}
    x0, x1 = 60, 360
    cols = [110, 160, 210, 260, 310]
    gates = [('a', 'b', 'd'), ('a', None, 'b'), ('b', 'c', 'd'), ('b', None, 'c'), ('a', None, 'b')]
    sites_y = 236
    site_x = [85] + [(cols[i] + cols[i + 1]) / 2 for i in range(4)] + [335]
    # construction: each gate's column dropped to the hop that applies it
    d.group('thin')
    d.lines([[(x, 44), (x, sites_y - 22)] for x in cols])
    d.line((40, sites_y), (380, sites_y))
    # the register's four wires
    d.group()
    d.lines([[(x0, y), (x1, y)] for y in wires.values()])
    # the gates: controls as open circles, the target as Feynman's X
    d.group()
    for x, (c1, c2, t) in zip(cols, gates):
        ys = [wires[c1], wires[t]] + ([wires[c2]] if c2 else [])
        d.line((x, min(ys)), (x, max(ys)))
        for c in (c1, c2):
            if c:
                d.circle(x, wires[c], 4)
        ty = wires[t]
        d.lines([[(x - 5, ty - 5), (x + 5, ty + 5)], [(x - 5, ty + 5), (x + 5, ty - 5)]])
    # the cursor's line of program sites, the hops between them, and a wave packet riding along it
    d.group('mid')
    for x in site_x:
        d.circle(x, sites_y, 4)
    for a, b in zip(site_x, site_x[1:]):
        d.arc((a + b) / 2, sites_y - 6, (b - a) / 2 - 5, 190, 350, n=24, ry=10)
    env = []
    for i in range(141):
        x = 60 + 280 * i / 140
        env.append((x, sites_y + 26 - 18 * math.exp(-((x - 190) / 34) ** 2) * math.cos((x - 190) / 5.2)))
    d.line(*env)
    d.group()
    d.circle(site_x[2], sites_y, 7)
    # labels
    d.group()
    for name, y in wires.items():
        d.text(x0 - 6, y + 3, name if name != 'd' else 'd=0', size=8, anchor='end')
    for name, y in zip(('a', 'b', 'SUM', 'CARRY'), wires.values()):
        d.text(x1 + 6, y + 3, name, size=7, anchor='start')
    for i, x in enumerate(site_x):
        d.text(x, sites_y + 44, str(i), size=7)
    for i, x in enumerate(cols):
        d.text(x, 36, f'A{i + 1}', size=7)
    d.text(200, 180, 'H = Σ q*(i+1) q(i) A(i+1) + c.c.', size=8)
    d.text(40, sites_y - 10, 'CURSOR', size=7, anchor='start')
    return d


def lectures_on_computation():
    """The price of forgetting one bit: a single molecule in a cylinder, pushed into one half by a
    piston, and the work that takes along the isotherm, kT ln 2."""
    d = D()
    cx0, cx1, cy0, cy1 = 24, 190, 104, 176
    mid = (cx0 + cx1) / 2
    # construction: the cylinder's centreline, the half mark, the plot's grid
    ox, oy, w, h = 232, 234, 150, 150
    V = lambda v: ox + w * v          # volume, as a fraction of the axis
    P = lambda p: oy - h * p
    d.group('thin')
    d.line((14, (cy0 + cy1) / 2), (212, (cy0 + cy1) / 2))
    d.line((mid, cy0 - 26), (mid, cy1 + 26))
    d.lines([[(V(k / 6), oy), (V(k / 6), oy - h)] for k in range(1, 7)])
    d.lines([[(ox, P(k / 5)), (ox + w, P(k / 5))] for k in range(1, 6)])
    # the cylinder and its piston, pushed in to the half mark
    d.group()
    d.line((cx1, cy0), (cx0, cy0), (cx0, cy1), (cx1, cy1))
    d.line((mid, cy0 + 2), (mid, cy1 - 2))
    d.line((mid, (cy0 + cy1) / 2), (cx1 + 18, (cy0 + cy1) / 2))
    d.line((cx1 + 18, (cy0 + cy1) / 2 - 12), (cx1 + 18, (cy0 + cy1) / 2 + 12))
    # detail: the molecule, the path it wanders, where the piston started
    d.group('mid')
    d.circle(56, 132, 5)
    walk = [(56, 132), (38, 116), (80, 112), (98, 150), (44, 168), (70, 124), (92, 118)]
    d.line(*walk)
    d.lines([[(cx1 - 2, cy0 + 2), (cx1 - 2, cy1 - 2)]])
    _arrow(d, mid + 6, cy0 - 10, math.pi, 5)
    d.line((mid + 6, cy0 - 10), (cx1 - 2, cy0 - 10))
    # the isotherm p = kT/V from V/2 to V, and the work under it, hatched
    d.group()
    d.line((ox, oy), (ox + w + 6, oy))
    d.line((ox, oy), (ox, oy - h - 8))
    _arrow(d, ox + w + 6, oy, 0, 4)
    _arrow(d, ox, oy - h - 8, -math.pi / 2, 4)
    iso = [(V(v), P(0.19 / v)) for v in [0.2 + 0.8 * i / 80 for i in range(81)]]
    d.line(*iso)
    d.group('mid')
    d.lines([[(V(v), oy), (V(v), P(0.19 / v))] for v in [0.5 + 0.5 * k / 12 for k in range(13)]])
    # labels
    d.group()
    d.text((cx0 + mid) / 2, cy1 + 18, '0', size=9)
    d.text((mid + cx1) / 2, cy1 + 18, '1', size=9)
    d.text(V(0.5), oy + 14, 'V/2', size=7)
    d.text(V(1.0), oy + 14, 'V', size=7)
    d.text(ox + 4, oy - h - 12, 'PRESSURE', size=7, anchor='start')
    d.text(V(0.8), P(0.5), 'W = kT ln 2', size=8)
    d.text(107, cy0 - 30, 'ERASE: PUSH THE BIT INTO 0', size=7)
    d.text(200, 282, 'ONE MOLECULE · ONE BIT · THE LEAST HEAT TO FORGET IT', size=7)
    return d


def quantum_computing_now():
    """Error correction below threshold: a distance-7 surface code (49 data qubits, 48 measure qubits,
    the layout of Google's 2024 memory) and the logical error falling by a factor of about two per step in distance."""
    d = D()
    n = 7
    s = 26
    gx, gy = 24, 46           # the top-left data qubit
    Q = lambda i, j: (gx + j * s, gy + i * s)
    # construction: the data-qubit grid
    d.group('thin')
    d.lines([[Q(i, 0), Q(i, n - 1)] for i in range(n)])
    d.lines([[Q(0, j), Q(n - 1, j)] for j in range(n)])
    # the stabilizer tiles: X tiles hatched, Z tiles plain; half-disc tiles on the boundary
    d.group('mid')
    hatch = []
    for i in range(n - 1):
        for j in range(n - 1):
            if (i + j) % 2 == 0:
                x, y = Q(i, j)
                for k in range(1, 4):
                    t = k / 4
                    hatch.append([(x + s * t, y), (x, y + s * t)])
                    hatch.append([(x + s, y + s * t), (x + s * t, y + s)])
    d.lines(hatch)
    for j in range(n - 1):
        x, _ = Q(0, j)
        if j % 2 == 1:
            d.arc(x + s / 2, gy, s / 2, 180, 360, n=16)
        else:
            d.arc(x + s / 2, gy + (n - 1) * s, s / 2, 0, 180, n=16)
    for i in range(n - 1):
        _, y = Q(i, 0)
        if i % 2 == 0:
            d.arc(gx, y + s / 2, s / 2, 90, 270, n=16)
        else:
            d.arc(gx + (n - 1) * s, y + s / 2, s / 2, -90, 90, n=16)
    # the qubits: data qubits at the corners, a measure qubit in every tile
    d.group()
    for i in range(n):
        for j in range(n):
            d.circle(*Q(i, j), 3.6)
    d.group('mid')
    for i in range(n - 1):
        for j in range(n - 1):
            x, y = Q(i, j)
            d.circle(x + s / 2, y + s / 2, 1.6)
    for j in range(n - 1):
        x, _ = Q(0, j)
        d.circle(x + s / 2, gy - s / 4 if j % 2 == 1 else gy + (n - 1) * s + s / 4, 1.6)
    for i in range(n - 1):
        _, y = Q(i, 0)
        d.circle(gx - s / 4 if i % 2 == 0 else gx + (n - 1) * s + s / 4, y + s / 2, 1.6)
    # the logical error per cycle against distance, on a log scale (fit: Λ = 2.14, ε7 = 0.143%)
    ox, oy, w, h = 250, 226, 124, 150
    lg = lambda e: oy - h * (math.log10(e) + 3.3) / 1.6    # 10^-3.3 .. 10^-1.7 (in fraction)
    D_ = lambda dd: ox + w * (dd - 2) / 6
    eps = {7: 0.00143}
    eps[5] = eps[7] * 2.14
    eps[3] = eps[5] * 2.14
    d.group('thin')
    d.lines([[(ox, lg(10 ** e)), (ox + w, lg(10 ** e))] for e in (-3, -2.5, -2)])
    d.lines([[(D_(dd), oy), (D_(dd), oy - h)] for dd in (3, 5, 7)])
    d.group()
    d.line((ox, oy), (ox + w + 6, oy))
    d.line((ox, oy), (ox, oy - h - 8))
    _arrow(d, ox + w + 6, oy, 0, 4)
    _arrow(d, ox, oy - h - 8, -math.pi / 2, 4)
    d.line(*[(D_(dd), lg(eps[dd])) for dd in (3, 5, 7)])
    for dd in (3, 5, 7):
        d.circle(D_(dd), lg(eps[dd]), 3.5)
    # labels
    d.group()
    for dd in (3, 5, 7):
        d.text(D_(dd), oy + 14, f'd={dd}', size=7)
    d.text(ox + 4, oy - h - 12, 'LOGICAL ERROR / CYCLE', size=7, anchor='start')
    d.text(D_(5) + 8, lg(eps[5]) - 14, '÷ 2.14', size=8, anchor='start')
    d.text(gx + 3 * s, 16, 'DISTANCE 7 · 49 DATA + 48 MEASURE', size=7)
    d.text(200, 286, 'BELOW THRESHOLD: EACH STEP IN DISTANCE ROUGHLY HALVES THE ERRORS', size=7)
    return d


PLATES = {
    'physics-of-computation': physics_of_computation,
    'connection-machine': connection_machine,
    'quantum-computers': quantum_computers,
    'lectures-on-computation': lectures_on_computation,
    'quantum-computing-now': quantum_computing_now,
}
