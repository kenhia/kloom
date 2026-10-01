"""Plates for the end of the chemistry trail Finding the elements (sprint 025):
technetium, the transuranium elements and the superheavy elements."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _arrow(d, a, b, head=4.5):
    """A straight arrow from a to b, its head drawn as two short strokes."""
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    d.line(a, b)
    d.lines([[_pt(b, ang + 155, head), b, _pt(b, ang - 155, head)]])


def technetium():
    """Lawrence's cyclotron in plan, its deflector carrying the molybdenum foil; and technetium-99m's decay."""
    d = D()
    c, R, gap = (104, 132), 76, 5                 # the chamber's centre, the dees' radius, half the gap
    # the ion's path: a radius growing as the square root of the half-turns (energy gained at each crossing)
    n = 11
    path = []
    for k in range(n):
        r = R * 0.88 * math.sqrt((k + 1) / n)
        a0 = 90 if k % 2 == 0 else 270
        cx = c[0] - gap if k % 2 == 0 else c[0] + gap
        for i in range(19):
            a = a0 + 180 * i / 18
            path.append((cx + r * math.cos(math.radians(a)), c[1] - r * math.sin(math.radians(a))))
    d.group('thin')
    d.line((c[0], c[1] - R - 16), (c[0], c[1] + R + 16))
    d.line((c[0] - R - 16, c[1]), (c[0] + R + 16, c[1]))
    d.circle(*c, R + 10)
    d.group()
    # the two dees, each a half disc, facing across the gap
    for s in (-1, 1):
        x = c[0] + s * gap
        a0, a1 = (90, 270) if s < 0 else (-90, 90)
        d.arc(x, c[1], R, a0, a1, n=48)
        d.line((x, c[1] - R), (x, c[1] + R))
    d.group('mid')
    d.line(*path)
    # the deflector: a curved plate at the rim, with the foil on its face, and the beam led out
    rim = R * 0.88
    d.arc(c[0] + gap, c[1], rim + 6, -60, -20, n=16)
    d.arc(c[0] + gap, c[1], rim + 9, -60, -20, n=16)
    out0 = _pt((c[0] + gap, c[1]), -20, rim + 3)
    _arrow(d, out0, (out0[0] + 26, out0[1] + 9))
    # technetium-99m's decay: fraction left against hours, halving every six
    ox, oy, w, h = 232, 236, 140, 150              # the graph's origin and size (24 h across, 1 up)
    d.group('thin')
    d.line((ox, oy - h - 6), (ox, oy), (ox + w + 8, oy))
    for i in range(1, 5):
        x = ox + w * i / 4
        y = oy - h * 0.5 ** i
        d.line((x, oy), (x, y), (ox, y))
    d.group()
    pts = [(ox + w * t / 24, oy - h * 0.5 ** (t / 6.0066)) for t in [i * 0.25 for i in range(97)]]
    d.line(*pts)
    d.group('mid')
    for i in range(0, 5):
        d.circle(ox + w * i / 4, oy - h * 0.5 ** i, 2)
    d.group('mid')
    d.text(c[0], 36, 'CYCLOTRON · PLAN', size=8)
    d.text(c[0] + 58, c[1] - 60, 'Mo FOIL', size=7, anchor='start')
    for i, lab in enumerate(('0', '6', '12', '18', '24 h')):
        d.text(ox + w * i / 4, oy + 12, lab, size=7)
    d.text(ox - 5, oy - h + 3, '1', size=7, anchor='end')
    d.text(ox - 5, oy - h / 2 + 3, '1/2', size=7, anchor='end')
    d.text(ox + w + 6, oy - h / 16 - 5, '1/16', size=7, anchor='start')
    d.text(ox + w / 2, 70, '⁹⁹ᵐTc LEFT', size=8)
    d.text(200, 280, '⁹⁶Mo + ²H → ⁹⁷Tc + n', size=9)
    return d


# the periodic table's outline: for each row, the columns (1–18) it fills
ROWS = [[1, 18], list(range(1, 3)) + list(range(13, 19)), list(range(1, 3)) + list(range(13, 19))] + [list(range(1, 19))] * 4


def transuranium():
    """The periodic table with Seaborg's actinide row, and the chain from uranium-238 to plutonium-239."""
    d = D()
    s, x0, y0 = 16, 56, 30                          # a cell's side, the table's corner
    fx, fy = x0 + 2 * s, y0 + 8 * s + 10            # the corner of the two f-block rows below
    cell = lambda col, row: (x0 + (col - 1) * s, y0 + row * s)
    d.group('thin')
    for r, cols in enumerate(ROWS):
        for col in cols:
            x, y = cell(col, r)
            d.line((x, y), (x + s, y), (x + s, y + s), (x, y + s), closed=True)
    for r in range(2):
        for k in range(15):
            x, y = fx + k * s, fy + r * s
            d.line((x, y), (x + s, y), (x + s, y + s), (x, y + s), closed=True)
    d.group()
    # the actinide row, 89 to 103, in full, and the old places of Th, Pa and U under Hf, Ta and W
    d.line((fx, fy + s), (fx + 15 * s, fy + s), (fx + 15 * s, fy + 2 * s), (fx, fy + 2 * s), closed=True)
    d.group('mid')
    for col in (4, 5, 6):
        x, y = cell(col, 6)
        d.lines([[(x + 3, y + 3), (x + s - 3, y + s - 3)], [(x + s - 3, y + 3), (x + 3, y + s - 3)]])
    _arrow(d, (cell(5, 6)[0] + s / 2, cell(5, 6)[1] + s + 2), (fx + 3.5 * s, fy + s - 2))
    # U, Np and Pu, 92 to 94, the fourth to sixth cells of the actinide row: the chain drawn above them
    ux = [fx + (k + 0.5) * s for k in (3, 4, 5)]
    yb = fy + 2 * s + 16
    d.group()
    for a, b in zip(ux, ux[1:]):
        d.arc((a + b) / 2, yb - 4, (b - a) / 2, 20, 160, n=16)
        _arrow(d, _pt(((a + b) / 2, yb - 4), 25, (b - a) / 2), (b - 0.5, yb - 6.5), head=3)
    d.group('mid')
    d.text(x0 + 9 * s, y0 - 10, 'THE TABLE AFTER 1944', size=8)
    for k, sym in zip((3, 4, 5), ('U', 'Np', 'Pu')):
        d.text(fx + (k + 0.5) * s, fy + 1.5 * s + 3, sym, size=7)
    d.text(fx + 15 * s + 6, fy + 1.5 * s + 3, 'ACTINIDES', size=7, anchor='start')
    d.text(cell(7, 6)[0] + 2, cell(7, 6)[1] + s + 10, 'Th Pa U, BEFORE', size=7, anchor='start')
    for a, b in zip(ux, ux[1:]):
        d.text((a + b) / 2, yb + 12, 'β⁻', size=7)
    d.text(200, 286, '²³⁸U + n → ²³⁹U → ²³⁹Np → ²³⁹Pu', size=9)
    return d


def superheavy():
    """A corner of the chart of nuclides: oganesson-294's decay chain, and the island of stability beyond it."""
    d = D()
    x0, y0, sx, sy = 44, 250, 7, 11               # N = 150 and Z = 100 at (x0, y0); pixels per neutron, per proton
    X = lambda n: x0 + (n - 150) * sx
    Y = lambda z: y0 - (z - 100) * sy
    d.group('thin')
    d.line((X(150), Y(100)), (X(192), Y(100)))
    d.line((X(150), Y(100)), (X(150), Y(121)))
    for n in range(150, 191, 10):
        d.line((X(n), Y(100)), (X(n), Y(100) + 4))
    for z in range(100, 121, 5):
        d.line((X(150), Y(z)), (X(150) - 4, Y(z)))
    # the magic numbers: the deformed shells at N = 162 and Z = 108, the predicted closed shell at N = 184
    d.line((X(162), Y(100)), (X(162), Y(120)))
    d.line((X(150), Y(108)), (X(172), Y(108)))
    d.line((X(184), Y(100)), (X(184), Y(121)))
    d.line((X(150), Y(114)), (X(192), Y(114)))
    d.group('mid')
    # the island: nested contours about N = 184, Z = 114, drawn as ellipses of rising stability
    for k, (rx, ry) in enumerate(((5, 2.6), (9, 4.4), (13, 6.2))):
        d.ellipse(X(184), Y(114), rx * sx, ry * sy)
    # the rock of the deformed shell near N = 162, Z = 108
    d.ellipse(X(162), Y(108), 4 * sx, 2.4 * sy)
    d.group()
    # oganesson-294 (Z 118, N 176) decays by alpha to 290Lv and 286Fl, which splits in two
    chain = [(176, 118), (174, 116), (172, 114)]
    for n, z in chain:
        x, y = X(n), Y(z)
        d.line((x - 4, y - 5), (x + 4, y - 5), (x + 4, y + 5), (x - 4, y + 5), closed=True)
    for (n1, z1), (n2, z2) in zip(chain, chain[1:]):
        _arrow(d, (X(n1) - 4, Y(z1) + 5), (X(n2) + 4.5, Y(z2) - 5.5), head=3.5)
    xf, yf = X(172), Y(114)
    d.lines([[(xf - 6, yf + 9), (xf - 14, yf + 20)], [(xf + 6, yf + 9), (xf + 14, yf + 20)]])
    d.group('mid')
    for n in range(150, 191, 10):
        d.text(X(n), Y(100) + 13, str(n), size=7)
    for z in range(100, 121, 5):
        d.text(X(150) - 7, Y(z) + 3, str(z), size=7, anchor='end')
    d.text(X(192), Y(100) - 5, 'N', size=8, anchor='end')
    d.text(X(150) + 5, Y(121) + 4, 'Z', size=8, anchor='start')
    d.text(X(176) + 7, Y(118) + 3, 'Og', size=8, anchor='start')
    d.text(X(172) - 22, Y(114) + 26, 'FISSION', size=7)
    d.text(X(184) + 4, Y(121) + 4, 'N = 184', size=7, anchor='start')
    d.text(X(184), Y(114) + 3, 'ISLAND?', size=7)
    d.text(200, 286, '²⁴⁹Cf + ⁴⁸Ca → ²⁹⁴Og + 3n', size=9)
    return d


PLATES = {'technetium': technetium, 'transuranium': transuranium, 'superheavy': superheavy}
