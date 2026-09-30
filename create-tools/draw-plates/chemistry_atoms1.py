"""Plates for the chemistry subject's Atoms and the table segment, part atoms1 (sprint 025):
Dalton's atomic theory, Wöhler's urea, and Faraday's laws of electrolysis."""
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


def _trim(a, b, g0, g1=None):
    """The segment ab, shortened by g0 at a and g1 at b, so a bond stops short of its atoms' letters."""
    g1 = g0 if g1 is None else g1
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    return (a[0] + dx / n * g0, a[1] + dy / n * g0), (b[0] - dx / n * g1, b[1] - dy / n * g1)


def dalton():
    """Dalton's compound atoms for the three oxides of azote, and the oxygen each holds per 100 of azote."""
    d = D()
    r, step = 11, 24                                  # an atom's circle, and the spacing of atoms in a compound
    rows = [('N₂O', 'NON', 57.5), ('NO', 'NO', 114.6), ('NO₂', 'ONO', 239.0)]
    ys = [92, 152, 212]
    mx = 92                                            # the molecules' centre line
    x0, x1, base, k = 196, 384, 252, 0.72              # the chart: its left and right, its baseline, px per unit
    bars = [236, 290, 344]
    unit = 57.5
    d.group('thin')
    # the ideal whole multiples of the first oxide's oxygen, 1, 2 and 4, and the chart's frame
    for m in (1, 2, 4):
        y = base - k * unit * m
        d.line((x0, y), (x1, y))
    d.line((x0, base), (x0, base - k * 250))
    d.line((mx, 62), (mx, 238))
    for y in ys:
        d.line((mx - 62, y), (mx + 62, y))
    d.group()
    # the atoms: azote a circle with an upright bar, oxygen a plain circle, as Dalton marked them
    for (name, atoms, _), y in zip(rows, ys):
        n = len(atoms)
        for i, a in enumerate(atoms):
            cx = mx + (i - (n - 1) / 2) * step
            d.circle(cx, y, r)
    d.line((x0, base), (x1, base))
    for x, (_, _, v) in zip(bars, rows):
        h = k * v
        d.line((x - 13, base), (x - 13, base - h), (x + 13, base - h), (x + 13, base))
    d.group('mid')
    for (name, atoms, _), y in zip(rows, ys):
        n = len(atoms)
        for i, a in enumerate(atoms):
            cx = mx + (i - (n - 1) / 2) * step
            if a == 'N':
                d.line((cx, y - r), (cx, y + r))
    d.group('mid')
    for (name, _, _), y in zip(rows, ys):
        d.text(mx, y + 26, name, size=8)
    for x, (name, _, v) in zip(bars, rows):
        d.text(x, base + 12, name, size=8)
        d.text(x, base - k * v - 5, f'{v:g}', size=8)
    for m in (1, 2, 4):
        d.text(x0 - 4, base - k * unit * m + 3, f'×{m}', size=7, anchor='end')
    d.text(mx, 44, "DALTON'S SYMBOLS", size=8)
    d.text(290, 26, 'OXYGEN PER 100 AZOTE', size=8)
    d.text(290, 282, 'BY WEIGHT · DAVY, IN DALTON 1810', size=7)
    return d


def wohler_urea():
    """Ammonium cyanate and urea: the same atoms, CH4N2O, joined two ways."""
    d = D()
    L = 26                                             # a bond's length
    g = 6.5                                            # the gap a bond leaves around an atom's letter
    # ammonium cyanate: the ion NH4+ (its tetrahedron seen from above) beside O=C=N-
    n1 = (74, 104)
    hs = [_pt(n1, a, L) for a in (45, 135, 225, 315)]
    cy = 196
    o, c, n2 = (46, cy), (46 + L, cy), (46 + 2 * L, cy)
    # urea: a flat molecule about its carbon, bonds at 120 degrees
    uc = (292, 150)
    uo = _pt(uc, -90, L)
    un = [_pt(uc, 30, L), _pt(uc, 150, L)]
    uh = [[_pt(un[0], -30, L * 0.8), _pt(un[0], 90, L * 0.8)],
          [_pt(un[1], 210, L * 0.8), _pt(un[1], 90, L * 0.8)]]
    d.group('thin')
    # construction: the tetrahedron's square shadow, the 120-degree rays and circles about urea's C and Ns
    d.line(*hs, closed=True)
    d.circle(*uc, L)
    for a in (-90, 30, 150):
        d.line(uc, _pt(uc, a, L + 14))
    for p in un:
        d.circle(*p, L * 0.8)
    d.line((20, cy), (150, cy))
    d.line((200, 250), (200, 50))
    d.group()
    for h in hs:
        d.line(*_trim(n1, h, g, 4))
    d.lines(_parallel(*_trim(o, c, g), k=3.6))
    d.lines(_parallel(*_trim(c, n2, g), k=3.6))
    d.lines(_parallel(*_trim(uc, uo, g), k=3.6))
    for p in un:
        d.line(*_trim(uc, p, g))
    for p, hh in zip(un, uh):
        for h in hh:
            d.line(*_trim(p, h, g, 4))
    d.group('mid')
    # the ions' brackets and the arrow of warming
    d.line((44, 72), (40, 72), (40, 136), (44, 136))
    d.line((104, 72), (108, 72), (108, 136), (104, 136))
    d.line((168, 150), (220, 150))
    d.line((213, 146), (220, 150), (213, 154))
    d.group('mid')
    d.text(n1[0], n1[1] + 3.5, 'N', size=10)
    for h in hs:
        d.text(h[0], h[1] + 3.5, 'H', size=9)
    d.text(114, 72, '+', size=9)
    for p, s in ((o, 'O'), (c, 'C'), (n2, 'N')):
        d.text(p[0], p[1] + 3.5, s, size=10)
    d.text(n2[0] + 12, cy - 8, '−', size=9)
    for p, s in ((uc, 'C'), (uo, 'O')):
        d.text(p[0], p[1] + 3.5, s, size=10)
    for p, hh in zip(un, uh):
        d.text(p[0], p[1] + 3.5, 'N', size=10)
        for h in hh:
            d.text(h[0], h[1] + 3.5, 'H', size=9)
    d.text(194, 142, 'WARM', size=7)
    d.text(84, 250, 'AMMONIUM CYANATE', size=8)
    d.text(84, 262, 'NH₄⁺ OCN⁻', size=8)
    d.text(292, 250, 'UREA', size=8)
    d.text(292, 262, '(NH₂)₂CO', size=8)
    d.text(200, 284, 'BOTH CH₄N₂O', size=9)
    return d


def faraday_electrolysis():
    """A silver cell in section, and the straight line of silver laid down against charge passed."""
    d = D()
    # the cell
    lx, rx, top, bot, lev = 34, 170, 112, 236, 132    # the vessel's walls, rim, floor and the liquid's level
    ax, cx, e0, e1 = 66, 138, 92, 212                  # anode and cathode, and their tops and bottoms
    # the chart: 0-100 coulombs across, 0-120 mg of silver up
    gx0, gx1, gy0, gy1 = 222, 384, 240, 64
    sx, sy = (gx1 - gx0) / 100, (gy0 - gy1) / 120
    z = 107.8682 / 96485.33212 * 1000                  # mg of silver per coulomb, 1.118
    d.group('thin')
    d.line((lx - 10, lev), (rx + 10, lev))
    for q in (20, 40, 60, 80, 100):
        d.line((gx0 + q * sx, gy0), (gx0 + q * sx, gy1))
    for m in (40, 80, 120):
        d.line((gx0, gy0 - m * sy), (gx1, gy0 - m * sy))
    qf = 96.485
    d.line((gx0 + qf * sx, gy0), (gx0 + qf * sx, gy0 - qf * z * sy), (gx0, gy0 - qf * z * sy))
    d.group()
    # the vessel, its electrodes, the wires and the battery above them
    d.line((lx, top), (lx, bot - 10))
    d.arc(lx + 10, bot - 10, 10, 180, 90, n=8)
    d.line((lx + 10, bot), (rx - 10, bot))
    d.arc(rx - 10, bot - 10, 10, 90, 0, n=8)
    d.line((rx, bot - 10), (rx, top))
    d.line((ax - 4, e0), (ax + 4, e0), (ax + 4, e1), (ax - 4, e1), closed=True)
    d.line((cx - 3, e0), (cx + 3, e0), (cx + 3, e1), (cx - 3, e1), closed=True)
    d.line((ax, e0), (ax, 48), (92, 48))
    d.line((cx, e0), (cx, 48), (112, 48))
    d.lines([[(92, 36), (92, 60)], [(100, 42), (100, 54)], [(104, 36), (104, 60)], [(112, 42), (112, 54)]])
    d.line((gx0, gy0), (gx1, gy0))
    d.line((gx0, gy0), (gx0, gy1))
    d.line((gx0, gy0), (gx0 + 100 * sx, gy0 - 100 * z * sy))
    d.group('mid')
    # silver ions drifting to the cathode, nitrate to the anode, and the silver grown on the cathode
    for i, (x, y) in enumerate([(90, 182), (104, 202), (92, 222), (114, 168)]):
        d.circle(x, y, 4.5)
        d.line((x + 7, y), (x + 17, y))
        d.line((x + 13, y - 3), (x + 17, y), (x + 13, y + 3))
    for x, y in [(104, 150), (124, 192)]:
        d.circle(x, y, 3)
        d.line((x - 6, y), (x - 16, y))
        d.line((x - 12, y - 3), (x - 16, y), (x - 12, y + 3))
    for i in range(12):
        y = e0 + 44 + i * 6
        d.line((cx - 3, y), (cx - 6.5, y + 3), (cx - 3, y + 6))
    for q in (20, 40, 60, 80):
        d.circle(gx0 + q * sx, gy0 - q * z * sy, 2)
    d.group('mid')
    d.text(ax, e1 + 32, 'ANODE', size=7)
    d.text(cx, e1 + 32, 'CATHODE', size=7)
    d.text(81, 170, 'Ag⁺', size=7)
    d.text(110, 153, 'NO₃⁻', size=7, anchor='start')
    d.text(102, 28, 'e⁻', size=8)
    for q in (0, 50, 100):
        d.text(gx0 + q * sx, gy0 + 12, str(q), size=7)
    for m in (40, 80, 120):
        d.text(gx0 - 4, gy0 - m * sy + 3, str(m), size=7, anchor='end')
    d.text(303, 268, 'CHARGE, COULOMBS', size=7)
    d.text(gx0, gy1 - 8, 'SILVER, mg', size=7, anchor='start')
    d.text(gx0 + 6, gy0 - qf * z * sy + 11, '96.5 C → 107.9 mg', size=7, anchor='start')
    d.text(303, 286, '1.118 mg OF SILVER A COULOMB', size=8)
    return d


PLATES = {'dalton': dalton, 'wohler-urea': wohler_urea, 'faraday-electrolysis': faraday_electrolysis}
