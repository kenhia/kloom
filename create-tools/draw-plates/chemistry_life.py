"""Plates for the chemistry subject's segment The chemistry of life (sprint 025, part `life`)."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _parallel(a, b, k=3.2):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * k, dx / n * k
    return [[(a[0] + ox / 2, a[1] + oy / 2), (b[0] + ox / 2, b[1] + oy / 2)],
            [(a[0] - ox / 2, a[1] - oy / 2), (b[0] - ox / 2, b[1] - oy / 2)]]


def _dashes(a, b, n=5, fill=0.55):
    """A dashed line from a to b as n short strokes (hydrogen bonds)."""
    out = []
    for i in range(n):
        t0, t1 = i / n, (i + fill) / n
        out.append([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                    (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)])
    return out


def _base_pair(c, L, purine_subs, pyrimidine_subs):
    """A purine and a pyrimidine facing each other, Watson-Crick fashion, from regular rings.

    The purine's six-ring is flat-topped with N1 pointing at the pyrimidine's N3; its five-ring
    is fused on the C4-C5 edge. Returns the rings, the exocyclic bonds, the hydrogen-bond pairs
    and the two glycosidic bond ends (where the sugars would be)."""
    pu = c
    py = (c[0] + 4.1 * L, c[1])
    hexa = {a: _pt(pu, a, L) for a in (0, 60, 120, 180, 240, 300)}       # N1 C2 N3 C4 C5 C6
    hexb = {a: _pt(py, a, L) for a in (0, 60, 120, 180, 240, 300)}       # C6 N1 C2 N3 C4 C5
    # the five-ring on the purine's C4 (180) - C5 (240) edge, outward toward 210 degrees
    r5 = L / (2 * math.sin(math.radians(36)))
    p5 = _pt(pu, 210, L * math.cos(math.radians(30)) + r5 * math.cos(math.radians(36)))
    a4 = math.degrees(math.atan2(hexa[180][1] - p5[1], hexa[180][0] - p5[0]))
    a5 = math.degrees(math.atan2(hexa[240][1] - p5[1], hexa[240][0] - p5[0]))
    step = 72 if (a5 - a4) % 360 > 180 else -72                          # walk away from C5
    pent = [_pt(p5, a4 + step * k, r5) for k in range(5)]                # C4 N9 C8 N7 C5
    n9 = pent[1]
    a9 = math.degrees(math.atan2(n9[1] - p5[1], n9[0] - p5[0]))
    rings = [[hexa[a] for a in (0, 60, 120, 180, 240, 300, 0)], pent + [pent[0]],
             [hexb[a] for a in (0, 60, 120, 180, 240, 300, 0)]]
    stubs, ends = [], {}
    for a, kind in purine_subs:                                           # exocyclic groups, radial
        e = _pt(hexa[a], a, L)
        stubs.append((hexa[a], e, kind))
        ends[('pu', a)] = e
    for a, kind in pyrimidine_subs:
        e = _pt(hexb[a], a, L)
        stubs.append((hexb[a], e, kind))
        ends[('py', a)] = e
    sugar_pu = _pt(n9, a9, L)
    sugar_py = _pt(hexb[60], 60, L)
    return dict(pu=pu, py=py, p5=p5, r5=r5, rings=rings, stubs=stubs, ends=ends,
                n1=hexa[0], n3=hexb[180], sugars=(n9, sugar_pu, hexb[60], sugar_py))


def dna_chemistry():
    """Chargaff's ratios and the pairs they point to: A with T, G with C, and his numbers as bars."""
    d = D()
    L = 16
    at = _base_pair((66, 84), L, [(300, 'N')], [(240, 'O'), (120, 'O'), (300, 'C')])
    gc = _base_pair((66, 190), L, [(300, 'O'), (60, 'N')], [(240, 'N'), (120, 'O')])
    # the bars: two of Chargaff's DNAs, moles of each base per mole of phosphorus (Experientia, 1950)
    groups = [(252, 'HUMAN SPERM', (0.29, 0.31, 0.18, 0.18)), (330, 'TUBERCLE BACILLI', (0.12, 0.11, 0.28, 0.26))]
    base_y, k, w, gap = 236, 380, 11, 16
    d.group('thin')
    for bp in (at, gc):
        d.circle(*bp['p5'], bp['r5'])
        d.circle(*bp['pu'], L)
        d.circle(*bp['py'], L)
        s1, s2 = bp['sugars'][1], bp['sugars'][3]
        d.line(s1, s2)                                                    # sugar to sugar: the same span
    d.line((230, base_y), (392, base_y))
    for gx, name, vals in groups:
        for pair in ((0, 1), (2, 3)):                                     # A level with T, G level with C
            y = base_y - k * (vals[pair[0]] + vals[pair[1]]) / 2
            d.line((gx - 4 + pair[0] * gap, y), (gx + w + 4 + pair[1] * gap, y))
    d.group()
    for bp in (at, gc):
        for ring in bp['rings']:
            d.line(*ring)
        for a, b, kind in bp['stubs']:
            if kind == 'O':
                d.lines(_parallel(a, b))
            else:
                d.line(a, b)
        n9, s1, n1, s2 = bp['sugars']
        d.line(n9, s1)
        d.line(n1, s2)
    for gx, name, vals in groups:
        for i, v in enumerate(vals):
            x = gx + i * gap
            d.line((x, base_y), (x, base_y - k * v), (x + w, base_y - k * v), (x + w, base_y))
    d.group('mid')
    # hydrogen bonds: two between A and T, three between G and C
    hb = _dashes(at['n1'], at['n3']) + _dashes(at['ends'][('pu', 300)], at['ends'][('py', 240)])
    hb += _dashes(gc['n1'], gc['n3']) + _dashes(gc['ends'][('pu', 300)], gc['ends'][('py', 240)])
    hb += _dashes(gc['ends'][('pu', 60)], gc['ends'][('py', 120)])
    d.lines(hb)
    d.group('mid')
    for bp, (l1, l2) in ((at, ('A', 'T')), (gc, ('G', 'C'))):
        d.text(bp['pu'][0], bp['pu'][1] + 3.5, l1, size=10)
        d.text(bp['py'][0], bp['py'][1] + 3.5, l2, size=10)
    for gx, name, vals in groups:
        for i, s in enumerate('ATGC'):
            d.text(gx + i * gap + w / 2, base_y + 11, s, size=8)
        d.text(gx + 1.5 * gap + w / 2, base_y + 24, name, size=6)
    d.text(311, 40, 'MOLES PER MOLE P', size=7)
    d.text(311, 270, 'CHARGAFF 1950', size=7)
    d.text(118, 262, 'A = T · G = C', size=9)
    return d


def protein_structure():
    """The alpha helix: 3.6 residues a turn, 1.5 A rise, 5.4 A pitch, each C=O bonded to the N-H four on."""
    d = D()
    s = 11.5                                    # pixels per angstrom
    R, rise, turn = 2.3, 1.5, 100.0             # C-alpha radius, rise per residue, degrees per residue
    cx, y0, n = 118, 262, 15
    tilt = 0.16                                 # a little perspective: the helix seen slightly from above

    def at(t):                                  # t in residues
        phi = math.radians(turn * t)
        return (cx + R * s * math.cos(phi), y0 - rise * s * t - tilt * R * s * math.sin(phi)), math.sin(phi)

    ca = [at(i)[0] for i in range(n)]
    d.group('thin')
    d.line((cx, y0 + 16), (cx, y0 - rise * s * (n - 1) - 18))            # the helix axis
    for side in (-1, 1):
        d.line((cx + side * R * s, y0 + 4), (cx + side * R * s, y0 - rise * s * (n - 1) - 4))
    # pitch: one full turn, 3.6 residues, measured beside the helix
    xd = cx + R * s + 26
    p0y = at(0)[0][1]
    p1y = p0y - 5.4 * s
    d.line((xd, p0y), (xd, p1y))
    d.lines([[(xd - 4, p0y), (xd + 4, p0y)], [(xd - 4, p1y), (xd + 4, p1y)]])
    d.lines([[(ca[0][0] + 3, p0y), (xd - 5, p0y)]])
    # rise: one residue, 1.5 A
    xr = cx - R * s - 22
    r0 = y0 - rise * s * 4
    d.line((xr, r0), (xr, r0 - rise * s))
    d.lines([[(xr - 4, r0), (xr + 4, r0)], [(xr - 4, r0 - rise * s), (xr + 4, r0 - rise * s)]])
    # the helical wheel, seen down the axis: 100 degrees a residue
    wx, wy, wr = 300, 92, 44
    d.circle(wx, wy, wr)
    d.line((wx - wr - 10, wy), (wx + wr + 10, wy))
    d.line((wx, wy - wr - 10), (wx, wy + wr + 10))
    d.line((wx, wy), _pt((wx, wy), -90, wr))
    d.line((wx, wy), _pt((wx, wy), 10, wr))
    d.group('mid')
    # the back of the helix, behind the axis, drawn lighter
    back, front, seg = [], [], []
    for j in range(0, 10 * (n - 1) + 1):
        p, sn = at(j / 10)
        (back if sn > 0 else front).append((p, j))
    def runs(pts):
        out, cur, last = [], [], None
        for p, j in pts:
            if last is not None and j != last + 1:
                out.append(cur)
                cur = []
            cur.append(p)
            last = j
        if cur:
            out.append(cur)
        return out
    d.lines(runs(back))
    d.group()
    d.lines(runs(front))
    for i, p in enumerate(ca):
        d.circle(p[0], p[1], 2.6 if at(i)[1] <= 0 else 1.8)
    # the wheel's residues
    for i in range(8):
        q = _pt((wx, wy), -90 + turn * i, wr)
        d.circle(q[0], q[1], 3)
    d.arc(wx, wy, 16, -90, 10, n=24)
    d.group('mid')
    # hydrogen bonds, residue i to residue i + 4, nearly parallel to the axis
    hb = []
    for i in range(n - 4):
        a, b = ca[i], ca[i + 4]
        if at(i)[1] <= 0.2:
            hb += _dashes((a[0] + 2, a[1] - 4), (b[0] + 2, b[1] + 4), n=4)
    d.lines(hb)
    d.group('mid')
    d.text(xd + 6, (p0y + p1y) / 2 + 3, '5.4 Å', anchor='start', size=8)
    d.text(xr - 5, r0 - rise * s / 2 + 3, '1.5 Å', anchor='end', size=8)
    d.text(ca[0][0] + 6, ca[0][1] + 14, 'i', size=8, anchor='start')
    d.text(ca[4][0] + 6, ca[4][1] + 4, 'i+4', size=8, anchor='start')
    for i in range(8):
        q = _pt((wx, wy), -90 + turn * i, wr + 11)
        d.text(q[0], q[1] + 3, str(i + 1), size=7)
    d.text(wx + 13, wy - 14, '100°', size=7, anchor='start')
    d.text(wx, 172, '3.6 RESIDUES A TURN', size=8)
    d.text(wx, 188, '3.6 × 1.5 Å = 5.4 Å', size=8)
    d.text(wx, 232, 'C=O (i) ··· H–N (i+4)', size=8)
    d.text(wx, 250, 'PAULING · COREY · BRANSON', size=7)
    d.text(wx, 263, '1951', size=7)
    return d


def miller_urey():
    """Miller's apparatus in elevation: boiling flask, 5-litre spark flask, condenser and U-trap."""
    d = D()
    bx, by, br = 78, 214, 30            # the boiling flask
    fx, fy, fr = 262, 96, 58            # the five-litre flask
    top = 16                            # the vapour line across the top
    cxl, cy0, cy1 = fx, 170, 226        # the condenser, below the big flask
    ground = 268
    d.group('thin')
    d.line((20, ground), (390, ground))
    d.line((bx, by - br - 16), (bx, ground))
    d.line((fx, fy - fr - 8), (fx, ground))
    d.line((fx - fr - 20, fy), (fx + fr + 20, fy))
    d.circle(bx, by, br + 6)
    d.circle(fx, fy, fr + 6)
    d.group()
    # the boiling flask and its neck, rising to the vapour line
    t0 = math.degrees(math.asin(5 / br))
    d.arc(bx, by, br, -90 + t0, 270 - t0, n=60)
    tf = math.degrees(math.asin(5 / fr))
    ft = fy - fr * math.cos(math.radians(tf))
    # the vapour line: up from the boiling flask, across, and down into the big flask
    d.line(_pt((bx, by), -90 - t0, br), (bx - 5, top), (fx + 5, top), (fx + 5, ft))
    d.line(_pt((bx, by), -90 + t0, br), (bx + 5, top + 10), (fx - 5, top + 10), (fx - 5, ft))
    # the big flask, open at top and bottom
    d.arc(fx, fy, fr, -90 + tf, 90 - tf, n=60)
    d.arc(fx, fy, fr, 90 + tf, 270 - tf, n=60)
    # the outlet down through the condenser to the trap
    ob = fy + fr * math.cos(math.radians(tf))
    d.line((fx - 5, ob), (fx - 5, 250), )
    d.line((fx + 5, ob), (fx + 5, 250))
    d.arc(fx - 20, 250, 25, 0, 180, n=24)
    d.arc(fx - 20, 250, 15, 0, 180, n=24)
    d.line((fx - 45, 250), (fx - 45, 232))
    d.line((fx - 35, 250), (fx - 35, 242))
    # back to the boiling flask along a sloping return
    ra = _pt((bx, by), 25, br)
    d.line((fx - 45, 232), (ra[0] + 4, ra[1] - 5))
    d.line((fx - 35, 242), (ra[0] + 4, ra[1] + 5))
    d.group('mid')
    # the condenser jacket, with water in and out
    d.line((cxl - 13, cy0), (cxl + 13, cy0), (cxl + 13, cy1), (cxl - 13, cy1), closed=True)
    d.line((cxl + 13, cy1 - 8), (cxl + 26, cy1 - 8))
    d.line((cxl - 13, cy0 + 8), (cxl - 26, cy0 + 8))
    # the water in the boiling flask, and the heat under it
    wl = by + 8
    hw = math.sqrt(br * br - (wl - by) ** 2)
    d.line((bx - hw, wl), (bx + hw, wl))
    d.lines([[(bx - 16, ground - 8), (bx - 10, by + br + 8)], [(bx, ground - 8), (bx, by + br + 6)],
             [(bx + 16, ground - 8), (bx + 10, by + br + 8)]])
    d.group()
    # the tungsten electrodes, and the spark between them
    g = 7
    d.lines(_parallel((fx - fr - 22, fy), (fx - g, fy), 3))
    d.lines(_parallel((fx + g, fy), (fx + fr + 22, fy), 3))
    zig = [(fx - g, fy)]
    for i, yy in enumerate((-4, 4, -4, 4)):
        zig.append((fx - g + (i + 1) * 2 * g / 5, fy + yy))
    zig.append((fx + g, fy))
    d.line(*zig)
    d.group('mid')
    d.text(fx, fy - 26, 'CH₄ · NH₃ · H₂', size=8)
    d.text(fx, fy + 30, 'SPARK', size=7)
    d.text(bx, by + 3, 'H₂O', size=8)
    d.text(cxl + 30, cy0 + 26, 'CONDENSER', size=7, anchor='start')
    d.text(fx - 20, 286, 'TRAP', size=7)
    d.text(fx + fr + 4, fy - fr + 2, '5 L', size=8, anchor='start')
    d.text(170, top + 22, 'STEAM', size=7)
    return d


PLATES = {'dna-chemistry': dna_chemistry, 'protein-structure': protein_structure, 'miller-urey': miller_urey}
