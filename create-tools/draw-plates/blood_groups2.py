"""Plates for the end of In the Blood's trail Beyond ABO (sprint 028): more-antigens, bombay, hla.
See plates_for.py."""
import math
import random
from plates import D


def _pt(cx, cy, r, a):
    """The point at `a` degrees on a circle (clockwise from +x; SVG's y runs down)."""
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _blob(cx, cy, r, rng, n=9):
    """An irregular closed outline about (cx, cy): a clump of agglutinated cells."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (0.65 + 0.5 * rng.random())
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def more_antigens():
    d = D()
    # The reading's invented panel, its Duffy and Kidd columns turned on their side: one column per
    # panel cell, a ring where the cell carries the antigen and a dash where it does not; under each
    # column the cell's tube after the antiglobulin phase and spin. Clumps where it reacted (2+),
    # specks for the weak reactions of the single-dose cells, a smooth button where it did not.
    rows = ['FYa', 'FYb', 'JKa', 'JKb']
    grid = [
        [1, 0, 1, 0, 1, 0, 1, 1],   # Fya
        [0, 1, 1, 1, 0, 1, 1, 0],   # Fyb
        [1, 0, 1, 1, 0, 1, 0, 1],   # Jka
        [0, 1, 0, 1, 1, 0, 1, 1],   # Jkb
    ]
    result = ['2+', '0', '2+', 'W', '0', '2+', '0', 'W']
    x0, dx = 124, 33
    xs = [x0 + i * dx for i in range(8)]
    ys = [46, 66, 86, 106]
    top, bot, w = 138, 252, 8
    rng = random.Random(1946)
    d.group('thin')
    for y in ys:                                             # the antigram's rows
        d.line((96, y + 10), (xs[-1] + 16, y + 10))
    d.line((96, ys[0] - 10), (xs[-1] + 16, ys[0] - 10))
    for x in xs:                                             # its columns, carried down to the tubes
        d.line((x - 16, ys[0] - 10), (x - 16, ys[-1] + 10))
        d.line((x, ys[-1] + 14), (x, top - 6))
    d.line((xs[-1] + 16, ys[0] - 10), (xs[-1] + 16, ys[-1] + 10))
    d.line((40, 200), (370, 200))                            # the level of the saline in every tube
    d.group()
    for x in xs:                                             # eight tubes, round-bottomed
        d.line((x - w - 2, top - 4), (x - w, top), (x - w, bot))
        d.arc(x, bot, w, 180, 0, n=16)
        d.line((x + w, bot), (x + w, top), (x + w + 2, top - 4))
    d.group('mid')
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v:
                d.circle(xs[c], ys[r], 4)
            else:
                d.line((xs[c] - 3, ys[r]), (xs[c] + 3, ys[r]))
    for x, res in zip(xs, result):                          # the cells at the foot of each tube
        if res == '2+':
            for (bx, by, br) in ((x - 3, bot + 2, 4), (x + 3, bot - 4, 3.5), (x - 2, bot - 11, 3), (x + 2, bot - 18, 2.5)):
                d.line(*_blob(bx, by, br, rng), closed=True)
        elif res == 'W':
            for k in range(7):
                sx = x - 5 + rng.random() * 10
                sy = bot + 3 - k * 6 - rng.random() * 3
                d.line(*_blob(sx, sy, 1.3, rng, n=6), closed=True)
            d.ellipse(x, bot + 4, 5, 2)
        else:
            d.ellipse(x, bot + 4, 6, 2.5)
    # Kidd's row: the one antigen every reacting cell carries and every quiet cell lacks
    d.line((98, ys[2] - 9), (xs[-1] + 14, ys[2] - 9), (xs[-1] + 14, ys[2] + 9), (98, ys[2] + 9), closed=True)
    d.group('mid')
    for r, name in enumerate(rows):
        d.text(90, ys[r] + 3, name, size=7, anchor='end')
    for i, x in enumerate(xs):
        d.text(x, 28, str(i + 1), size=7)
        d.text(x, 286, result[i], size=7)
    d.text(90, 286, 'AHG', size=7, anchor='end')
    d.text(90, 203, 'SALINE', size=7, anchor='end')
    return d


def bombay():
    d = D()
    # Four sugar chains on a red cell's membrane, read from the membrane up. The precursor ends in
    # galactose (circle) on N-acetylglucosamine (square). FUT1's enzyme adds fucose (triangle) to make
    # H, the antigen of group O; the A enzyme adds N-acetylgalactosamine (square with a bar) to H, and
    # the B enzyme a second galactose. A Bombay (hh) cell stops at the precursor: no fucose, so no
    # H for A or B to be built on. Symbols follow the usual glycan notation, drawn in outline.
    cx, cy, R = 200, 1060, 820                               # the membrane, an arc of a large circle
    chains = [(64, 'O (H)', 'H'), (152, 'A', 'A'), (240, 'B', 'B'), (328, 'BOMBAY (hh)', 'h')]
    s = 9                                                    # half the size of a symbol

    def ybase(x):
        return cy - math.sqrt(R * R - (x - cx) ** 2)

    d.group('thin')
    for x, _, _ in chains:                                   # each chain's axis
        d.line((x, ybase(x) - 2), (x, 62))
    d.line((24, 40), (376, 40))
    d.group()
    pts_out = [_pt(cx, cy, R, a) for a in [270 + t * 0.25 for t in range(-56, 57)]]
    pts_in = [_pt(cx, cy, R + 10, a) for a in [270 + t * 0.25 for t in range(-56, 57)]]
    d.line(*pts_out)
    d.line(*pts_in)
    for x, _, kind in chains:
        yb = ybase(x)
        y_glc = yb - 40                                      # GlcNAc, the square
        y_gal = y_glc - 30                                   # Gal, the circle
        d.line((x, yb), (x, y_glc + s))
        d.line((x - s, y_glc - s), (x + s, y_glc - s), (x + s, y_glc + s), (x - s, y_glc + s), closed=True)
        d.line((x, y_glc - s), (x, y_gal + s))
        d.circle(x, y_gal, s)
        if kind != 'h':                                      # fucose on the galactose, to the side
            fx, fy = x + 26, y_gal
            d.line((x + s, y_gal), (fx - s, fy))
            d.line((fx - s, fy + s * 0.8), (fx + s, fy + s * 0.8), (fx, fy - s), closed=True)
        if kind in ('A', 'B'):
            ty = y_gal - 30
            d.line((x, y_gal - s), (x, ty + s))
            if kind == 'A':
                d.line((x - s, ty - s), (x + s, ty - s), (x + s, ty + s), (x - s, ty + s), closed=True)
            else:
                d.circle(x, ty, s)
    # the key, in the symbols' own shapes
    k = 4
    d.line((44 - k, 286 - k), (44 + k, 286 - k), (44 + k, 286 + k), (44 - k, 286 + k), closed=True)
    d.circle(124, 286, k)
    d.line((190 - k, 286 + k * 0.8), (190 + k, 286 + k * 0.8), (190, 286 - k), closed=True)
    d.line((258 - k, 286 - k), (258 + k, 286 - k), (258 + k, 286 + k), (258 - k, 286 + k), closed=True)
    d.line((258 - k, 286 + k), (258 + k, 286 - k))
    d.group('mid')
    for x, _, kind in chains:
        yb = ybase(x)
        y_gal = yb - 70
        if kind == 'A':                                      # the bar that marks GalNAc's square
            ty = y_gal - 30
            d.line((x - s, ty + s), (x + s, ty - s))
        if kind == 'h':                                      # where the fucose would go: dashed, empty
            fx = x + 26
            for k in range(4):
                d.line((x + s + 2 + k * 5, y_gal), (x + s + 4 + k * 5, y_gal))
            d.lines([[(fx - 6, y_gal - 6), (fx + 6, y_gal + 6)], [(fx - 6, y_gal + 6), (fx + 6, y_gal - 6)]])
        for k in range(-3, 4):                                # the membrane's thickness, hatched
            hx = x + k * 6
            d.line((hx, ybase(hx) + 1), (hx - 3, ybase(hx) + 9))
    d.group('mid')
    for x, label, _ in chains:
        d.text(x, 54, label, size=7)
    d.text(200, 28, 'SUGAR CHAINS ON THE RED CELL', size=7)
    for lx, name in ((44, 'GLCNAC'), (124, 'GAL'), (190, 'FUC'), (258, 'GALNAC')):
        d.text(lx + 8, 289, name, size=7, anchor='start')
    return d


def hla():
    d = D()
    # Left: a Terasaki tray in plan, 6 rows of 10 wells, one well picked out. Right: that well in
    # section, its drop of serum, cells and complement sitting under oil. Below: the reading under
    # phase contrast, a living lymphocyte bright and round, a killed one dark, flat and stained.
    # Proportions are a sketch, not a measurement.
    tx0, ty0, pitch = 30, 52, 16
    d.group('thin')
    d.line((tx0 - 12, ty0 - 12), (tx0 + 9 * pitch + 12, ty0 - 12), (tx0 + 9 * pitch + 12, ty0 + 5 * pitch + 12),
           (tx0 - 12, ty0 + 5 * pitch + 12), closed=True)
    sel = (tx0 + 6 * pitch, ty0 + 2 * pitch)
    d.line((sel[0] + 7, sel[1] - 4), (250, 60))             # leader from the chosen well to its section
    d.line((sel[0] + 7, sel[1] + 4), (250, 160))
    wx, wtop, wbot = 300, 60, 160                           # the well in section
    d.line((222, wtop), (378, wtop))
    d.group()
    for r in range(6):                                       # the tray's wells
        for c in range(10):
            d.circle(tx0 + c * pitch, ty0 + r * pitch, 5)
    d.line((tx0 - 16, ty0 - 16), (tx0 + 9 * pitch + 16, ty0 - 16), (tx0 + 9 * pitch + 16, ty0 + 5 * pitch + 16),
           (tx0 - 16, ty0 + 5 * pitch + 16), closed=True)
    # the well: a cone cut off at a flat floor, set in the tray's plastic
    d.line((236, wtop), (wx - 44, wtop), (wx - 14, wbot), (wx + 14, wbot), (wx + 44, wtop), (364, wtop))
    d.line((236, wtop), (236, wbot + 22), (364, wbot + 22), (364, wtop))
    # the drop, a lens on the floor of the well
    d.arc(wx, wbot, 22, 180, 360, n=24, ry=18)
    d.group('mid')
    for k in range(1, 6):                                    # oil filling the well above the drop
        y = wtop + k * 14
        if y > wbot - 22:
            break
        half = 44 - (y - wtop) * 30 / (wbot - wtop)
        d.line((wx - half + 3, y), (wx + half - 3, y))
    for xh in range(240, 362, 10):                           # the plastic below the floor, hatched
        d.line((xh, wbot + 22), (xh + 8, wbot + 14))
    rng = random.Random(1964)
    for k in range(9):                                       # cells in the drop
        a = rng.uniform(200, 340)
        rr = rng.uniform(4, 15)
        cxp, cyp = wx + rr * math.cos(math.radians(a)) * 1.2, wbot - 3 + rr * math.sin(math.radians(a)) * 0.7
        d.circle(cxp, cyp, 1.8)
    d.circle(sel[0], sel[1], 8)
    # the two cells as the microscope shows them
    lx, dxc, ly = 110, 290, 238
    d.group()
    d.circle(lx, ly, 18)
    d.line(*_blob(dxc, ly + 3, 24, random.Random(7), n=11), closed=True)
    d.group('mid')
    d.circle(lx, ly, 23)                                     # the bright halo of a living cell
    d.circle(lx + 4, ly - 3, 8)
    for k in range(-5, 6):                                   # the dead cell, flooded with stain
        y = ly + k * 4
        half = math.sqrt(max(0, 18 * 18 - (k * 4) ** 2))
        d.line((dxc - half, y + 3), (dxc + half, y + 3))
    d.group('mid')
    d.text(tx0 + 4.5 * pitch, ty0 + 5 * pitch + 30, 'TRAY, 60 WELLS', size=7)
    d.text(wx, wtop - 8, 'OIL', size=7)
    d.text(wx, wbot + 36, 'DROP', size=7)
    d.text(lx, ly + 38, 'LIVING: ROUND, BRIGHT', size=7)
    d.text(dxc, ly + 38, 'KILLED: DARK, FLAT', size=7)
    return d


PLATES = {'more-antigens': more_antigens, 'bombay': bombay, 'hla': hla}
