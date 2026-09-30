"""Plates for part atoms3 of the chemistry subject (sprint 025): the periodic table,
the tetrahedral carbon atom and Gibbs's free energy."""
import math
from plates import D, rot


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _arrow(d, a, b, head=5, gap=0):
    """A line from a to b (shortened by `gap` at both ends) with an open head at b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    a2 = (a[0] + ux * gap, a[1] + uy * gap)
    b2 = (b[0] - ux * gap, b[1] - uy * gap)
    ang = math.degrees(math.atan2(uy, ux))
    d.lines([[a2, b2], [_pt(b2, ang + 155, head), b2, _pt(b2, ang - 155, head)]])


def periodic_table():
    """Groups II to VI of Mendeleev's 1871 table, the eka-silicon gap and its four neighbours,
    and the atomic volumes along its row, from which its density follows."""
    d = D()
    rows = ['Be B C N O', 'Mg Al Si P S', 'Ca Eb Ti V Cr', 'Zn Ea Es As Se',
            'Sr Yt Zr Nb Mo', 'Cd In Sn Sb Te']
    gaps = {'Eb', 'Ea', 'Es'}
    x0, y0, w, h = 22, 52, 34, 30                 # the table's corner and one cell
    cell = {}
    for r, row in enumerate(rows):
        for c, sym in enumerate(row.split()):
            cell[sym] = (x0 + c * w + w / 2, y0 + r * h + h / 2)
    # construction: the grid, and the ruled lines of the plot
    d.group('thin')
    d.lines([[(x0, y0 + r * h), (x0 + 5 * w, y0 + r * h)] for r in range(7)])
    d.lines([[(x0 + c * w, y0), (x0 + c * w, y0 + 6 * h)] for c in range(6)])
    px0, px1, py0, py1 = 238, 384, 232, 72           # the plot: atomic weight 64..80, volume 8..20
    X = lambda wt: px0 + (wt - 64) / 16 * (px1 - px0)
    Y = lambda v: py0 - (v - 8) / 12 * (py0 - py1)
    d.lines([[(px0, Y(v)), (px1, Y(v))] for v in (10, 12, 14, 16, 18, 20)])
    d.lines([[(X(wt), py0), (X(wt), py1)] for wt in (68, 72, 76, 80)])
    # the object: known elements as solid marks, the three gaps as open cells, eka-silicon boxed
    d.group()
    for sym, (cx, cy) in cell.items():
        if sym not in gaps:
            d.circle(cx, cy, 3)
    es = cell['Es']
    d.line((es[0] - w / 2 + 3, es[1] - h / 2 + 3), (es[0] + w / 2 - 3, es[1] - h / 2 + 3),
           (es[0] + w / 2 - 3, es[1] + h / 2 - 3), (es[0] - w / 2 + 3, es[1] + h / 2 - 3), closed=True)
    # the plot's axes and Mendeleev's atomic volumes along the row: Zn 9, Ea 11.5, Es 13, As 14, Se 18
    d.line((px0, py1 - 6), (px0, py0), (px1 + 6, py0))
    vols = [('Zn', 65, 9), ('Ea', 68, 11.5), ('Es', 72, 13), ('As', 75, 14), ('Se', 79, 18)]
    d.line(*[(X(wt), Y(v)) for _, wt, v in vols])
    d.group('mid')
    for sym in ('Eb', 'Ea'):
        cx, cy = cell[sym]
        d.line((cx - 7, cy - 7), (cx + 7, cy - 7), (cx + 7, cy + 7), (cx - 7, cy + 7), closed=True)
    # atomic analogy: the four neighbours that fix eka-silicon (Si and Sn skip the even rows' Ti and Zr)
    for n in ('Si', 'Sn', 'Ea', 'As'):
        _arrow(d, cell[n], es, head=4, gap=9)
    for sym, wt, v in vols:
        if sym in ('Ea', 'Es'):
            d.circle(X(wt), Y(v), 4)
        else:
            d.circle(X(wt), Y(v), 2.2)
    # reading eka-silicon off the plot
    d.lines([[(X(72), Y(13)), (px0, Y(13))], [(X(72), Y(13)), (X(72), py0)]])
    d.group('mid')
    for sym in ('Si', 'Sn', 'As'):
        cx, cy = cell[sym]
        d.text(cx + 11, cy - 5, sym, size=7, anchor='start')
    d.text(es[0], es[1] + 3, 'Es', size=9)
    d.text(cell['Ea'][0], cell['Ea'][1] + 19, 'Ea', size=7)
    d.text(x0 + 2.5 * w, y0 - 12, 'GROUPS II–VI · 1871', size=7)
    for sym, wt, v in vols:
        if sym != 'Es':
            d.text(X(wt), Y(v) - 8, sym, size=7)
    for v in (9, 13, 18):
        d.text(px0 - 5, Y(v) + 3, str(v), size=7, anchor='end')
    d.text(X(72), py0 + 12, '72', size=7)
    d.text((px0 + px1) / 2, py0 + 26, 'ATOMIC WEIGHT', size=7)
    d.text(px0 + 4, py1 - 12, 'ATOMIC VOLUME', size=7, anchor='start')
    d.text(200, 282, 'Es = 72 · 72 ÷ 13 = 5.5 g/cm³', size=9)
    return d


def _proj(p, ax, ay, cx, cy, s):
    x, y, z = rot(p, ax, ay)
    return (cx + s * x, cy - s * y), z


def _marker(d, p, kind, r=4.2):
    """Four different groups on the corners: a ring, a square, a triangle and a cross."""
    x, y = p
    if kind == 0:
        d.circle(x, y, r)
    elif kind == 1:
        d.line((x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r), closed=True)
    elif kind == 2:
        d.line((x, y - r * 1.2), (x + r * 1.1, y + r * 0.8), (x - r * 1.1, y + r * 0.8), closed=True)
    else:
        d.lines([[(x - r, y - r), (x + r, y + r)], [(x - r, y + r), (x + r, y - r)]])


def tetrahedral_carbon():
    """The tetrahedral carbon in its cube, with the 109.47 degree angle between two bonds,
    and a carbon with four different groups beside its mirror image."""
    d = D()
    ax, ay = math.radians(-26), math.radians(42)
    cx, cy, s = 112, 138, 54
    cube = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    tet = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    P = {v: _proj(v, ax, ay, cx, cy, s)[0] for v in cube}
    O = (cx, cy)
    d.group('thin')
    edges = [(a, b) for a in cube for b in cube if a < b and sum(abs(i - j) for i, j in zip(a, b)) == 2]
    d.lines([[P[a], P[b]] for a, b in edges])
    d.group()
    # the tetrahedron: six face diagonals of the cube
    d.lines([[P[a], P[b]] for i, a in enumerate(tet) for b in tet[i + 1:]])
    d.group('mid')
    # the four bonds from the carbon at the centre
    d.lines([[O, P[v]] for v in tet])
    d.circle(*O, 4)
    d.circle(*O, 1.6)
    for v in tet:
        d.circle(*P[v], 3)
    # the angle between two bonds, drawn along the arc between them: the pair that opens widest in the view
    def opening(pair):
        (x1, y1), (x2, y2) = [(P[v][0] - cx, P[v][1] - cy) for v in pair]
        return math.acos((x1 * x2 + y1 * y2) / math.hypot(x1, y1) / math.hypot(x2, y2))
    pa, pb = max(((u, v) for i, u in enumerate(tet) for v in tet[i + 1:]), key=opening)
    a, b = [x / math.sqrt(3) for x in pa], [x / math.sqrt(3) for x in pb]
    th = math.acos(sum(i * j for i, j in zip(a, b)))
    arc = []
    for k in range(25):
        u = k / 24
        w1, w2 = math.sin((1 - u) * th) / math.sin(th), math.sin(u * th) / math.sin(th)
        q = tuple(0.6 * (w1 * i + w2 * j) for i, j in zip(a, b))
        arc.append(_proj(q, ax, ay, cx, cy, s)[0])
    d.line(*arc)
    lab = arc[12]
    lab = (cx + (lab[0] - cx) * 1.25 - 26, cy + (lab[1] - cy) * 1.25 + 12)
    # the mirror pair: a carbon with four different groups, and its reflection across a mirror
    mx, my, ms = 302, 138, 40
    d.group('thin')
    d.lines([[(mx, my - 80), (mx, my + 78)]])
    tr = [tuple(c / math.sqrt(3) for c in v) for v in tet]
    bx, by = math.radians(-27), math.radians(42)

    def place(sign):
        c = (mx + sign * 52, my)
        pts = []
        for v in tr:
            x, y, z = rot(v, bx, by)
            pts.append((c[0] + sign * ms * x, c[1] - ms * y))
        return c, pts
    d.group()
    for sign in (-1, 1):
        c, pts = place(sign)
        d.lines([[pts[i], pts[j]] for i in range(4) for j in range(i + 1, 4)])
    d.group('mid')
    for sign in (-1, 1):
        c, pts = place(sign)
        d.lines([[c, p] for p in pts])
        d.circle(*c, 3)
        for k, p in enumerate(pts):
            _marker(d, p, k)
    d.group('mid')
    d.text(lab[0], lab[1] + 3, '109.47°', size=8)
    d.text(cx, 262, 'cos θ = −1/3', size=9)
    d.text(mx, 262, 'MIRROR', size=8)
    d.text(mx, 278, '24 ÷ 12 = 2', size=9)
    return d


def gibbs_free_energy():
    """Limestone's decomposition: the heat it needs (dH, flat) against the entropy term (T dS, rising),
    with dG = dH - T dS as the gap between them, which closes at 1,109 K."""
    d = D()
    dH, dS = 178.5, 0.161                      # kJ/mol and kJ/(mol K), from standard values at 298 K
    x0, x1, y0, y1 = 52, 372, 236, 44            # T from 0 to 1,600 K; energy from 0 to 260 kJ
    X = lambda T: x0 + T / 1600 * (x1 - x0)
    Y = lambda E: y0 - E / 260 * (y0 - y1)
    Tx = dH / dS
    d.group('thin')
    d.lines([[(x0, Y(E)), (x1, Y(E))] for E in (50, 100, 150, 200, 250)])
    d.lines([[(X(T), y0), (X(T), y1)] for T in (400, 800, 1200, 1600)])
    d.lines([[(X(298), y0), (X(298), Y(dH) - 10)], [(X(1273), y0), (X(1273), Y(1273 * dS) - 10)]])
    d.group()
    d.line((x0, y1 - 6), (x0, y0), (x1 + 6, y0))
    d.line((X(0), Y(dH)), (X(1600), Y(dH)))
    Tmax = 260 / dS
    d.line((X(0), Y(0)), (X(min(1600, Tmax)), Y(min(1600, Tmax) * dS)))
    d.group('mid')
    # the gap dG, hatched: above the rising line while dG > 0, below it once dG < 0
    hatch = []
    for T in range(50, 1600, 40):
        a, b = dH, T * dS
        if abs(a - b) > 3 and not (470 < T < 650 or 1320 < T < 1480):
            hatch.append([(X(T), Y(a)), (X(T), Y(min(b, 260)))])
    d.lines(hatch)
    d.circle(X(Tx), Y(dH), 4)
    d.line((X(Tx), Y(dH) + 4), (X(Tx), y0))
    d.group('mid')
    d.text(x0 - 6, Y(dH) + 3, 'ΔH', size=8, anchor='end')
    d.text(X(1480), Y(1480 * dS) - 10, 'TΔS', size=8, anchor='end')
    for E in (100, 200):
        d.text(x0 - 6, Y(E) + 3, str(E), size=7, anchor='end')
    d.text(X(560), Y(135), 'ΔG > 0', size=8)
    d.text(X(1400), Y(200), 'ΔG < 0', size=8)
    d.text(X(Tx), y0 + 12, '1,109 K', size=8)
    d.text(X(298), y0 + 12, '298', size=7)
    d.text(X(1600), y0 + 12, 'T', size=8)
    d.text(x0 + 4, y1 - 10, 'kJ/mol', size=7, anchor='start')
    d.text(212, 282, 'CaCO₃ → CaO + CO₂ · ΔG = ΔH − TΔS', size=9)
    return d


PLATES = {'periodic-table': periodic_table, 'tetrahedral-carbon': tetrahedral_carbon, 'gibbs-free-energy': gibbs_free_energy}
