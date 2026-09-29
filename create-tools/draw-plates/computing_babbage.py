"""computing plates, trail "Babbage's engines" (sprint 015). See computing.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=3.5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _span(d, x0, y0, x1, y1):
    """A dimension line from (x0, y0) to (x1, y1), arrowed at both ends."""
    d.line((x0, y0), (x1, y1))
    ang = math.atan2(y1 - y0, x1 - x0)
    _arrow(d, x1, y1, ang)
    _arrow(d, x0, y0, ang + math.pi)


def _rect(d, x0, y0, x1, y1):
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)


def prony_tables():
    """Prony's three sections as a tree (5–6, 7–8, 60–80), and a folio page of differences filled by addition."""
    d = D()
    # the tree: each tier's members spaced evenly across the same width
    x0, x1 = 18, 176
    tiers = [(6, 70), (8, 128), (28, 196)]  # (members drawn, height); the third tier is drawn as 28 of its 60-80
    pts = [[(x0 + (x1 - x0) * (i + 0.5) / n, y) for i in range(n)] for n, y in tiers]
    d.group('thin')
    # tier rules and the fans between tiers: each member of a tier hands down to the nearest members below
    d.lines([[(x0 - 4, y), (x1 + 4, y)] for _, y in tiers])
    fan = []
    for upper, lower in ((pts[0], pts[1]), (pts[1], pts[2])):
        per = len(lower) / len(upper)
        for i, (ux, uy) in enumerate(upper):
            for j in range(int(round(i * per)), int(round((i + 1) * per))):
                lx, ly = lower[j]
                fan.append([(ux, uy + 4), (lx, ly - 4)])
    d.lines(fan)
    # the members: analysts as circles, calculateurs as squares, computers as short strokes
    d.group()
    for x, y in pts[0]:
        d.circle(x, y, 4)
    for x, y in pts[1]:
        _rect(d, x - 3.5, y - 3.5, x + 3.5, y + 3.5)
    d.lines([[(x, y - 4), (x, y + 4)] for x, y in pts[2]])
    # the folio page, and a second one behind it: the two ateliers did the same work
    px0, py0, cw, rh, ncol, nrow = 196, 62, 26, 13, 6, 14
    px1, py1 = px0 + cw * ncol, py0 + rh * nrow
    d.group('mid')
    d.line((px0 + 6, py0 - 6), (px1 + 6, py0 - 6), (px1 + 6, py1 - 6))
    d.lines([[(px1, py1 - 6), (px1 + 6, py1 - 6)]])
    d.group('thin')
    d.lines([[(px0 + cw * c, py0), (px0 + cw * c, py1)] for c in range(1, ncol)])
    d.lines([[(px0, py0 + rh * r), (px1, py0 + rh * r)] for r in range(1, nrow)])
    d.group()
    _rect(d, px0, py0, px1, py1)
    # pivot rows, computed exactly by the second section, every seventh row
    for r in (0, 7):
        d.line((px0, py0 + rh * (r + 1)), (px1, py0 + rh * (r + 1)))
    # the additions of one step: each entry is the one above plus its neighbour to the right, above
    d.group('mid')
    r = 3
    for c in range(ncol - 1):
        sx, sy = px0 + cw * (c + 1.5), py0 + rh * (r + 0.5)
        tx, ty = px0 + cw * (c + 0.5), py0 + rh * (r + 1.5)
        d.line((sx - 4, sy + 3), (tx + 4, ty - 3))
        _arrow(d, tx + 4, ty - 3, math.atan2(ty - sy - 6, tx - sx + 8))
        d.line((tx, ty - rh + 4), (tx, ty - 4))
    # labels
    d.group()
    d.text(97, 56, 'I · 5–6 ANALYSTS', size=7)
    d.text(97, 114, 'II · 7–8 CALCULATEURS', size=7)
    d.text(97, 214, 'III · 60–80 COMPUTERS', size=7)
    d.text(97, 226, '+ AND − ONLY', size=7)
    for c, lab in enumerate(['LOG', 'Δ¹', 'Δ²', 'Δ³', 'Δ⁴', 'Δ⁵']):
        d.text(px0 + cw * (c + 0.5), py0 - 12, lab, size=7)
    d.text(px1 + 10, py0 + rh * 1 - 3, 'PIVOT', size=6, anchor='start')
    d.text(px1 + 10, py0 + rh * 8 - 3, 'PIVOT', size=6, anchor='start')
    d.text((px0 + px1) / 2, py1 + 16, 'TWO ATELIERS, THE SAME PAGE', size=7)
    d.text(200, 272, 'LOGARITHMS MADE LIKE PINS · PARIS 1791–1801', size=8)
    return d


def clement_fragment():
    """Difference Engine No. 1's demonstration piece in elevation: three axes of six cages (second difference,
    first difference, table), sector wheels between, three bells over, the crank above."""
    d = D()
    cols = {'2ND DIFF': 108, '1ST DIFF': 200, 'TABLE': 292}
    xs = list(cols.values())
    top, cage, ncage = 64, 30, 6
    bottom = top + cage * ncage
    rw = 30  # half-width of a figure wheel in elevation
    # construction: axis centre lines carried past the frame, the cage plates extended, the frame's width
    d.group('thin')
    d.lines([[(x, top - 30), (x, bottom + 14)] for x in xs])
    d.lines([[(46, top + cage * k), (354, top + cage * k)] for k in range(ncage + 1)])
    d.lines([[((xs[i] + xs[i + 1]) / 2, top - 6), ((xs[i] + xs[i + 1]) / 2, bottom + 6)] for i in range(2)])
    # the frame: pillars and the cage plates
    d.group()
    d.line((58, top), (342, top))
    d.line((58, bottom), (342, bottom))
    d.lines([[(x, top), (x, bottom)] for x in (58, 154, 246, 342)])
    d.lines([[(62, top + cage * k), (338, top + cage * k)] for k in range(1, ncage)])
    # the figure wheels: a band in each cage, its ten digits as ticks across its face
    d.group('mid')
    for x in xs:
        for k in range(ncage):
            yc = top + cage * k + cage / 2
            _rect(d, x - rw, yc - 6, x + rw, yc + 6)
            # digits on the visible half of the wheel, spaced by the cosine of their angle
            d.lines([[(x + rw * math.sin(math.radians(a)), yc - 6), (x + rw * math.sin(math.radians(a)), yc + 6)]
                     for a in range(-72, 73, 36)])
    # the sector wheels between the axes, which carry each difference over to the column beside it
    d.group()
    for i in range(2):
        xm = (xs[i] + xs[i + 1]) / 2
        for k in range(ncage):
            yc = top + cage * k + cage / 2
            d.line((xm - 10, yc - 3), (xm + 10, yc - 3), (xm + 10, yc + 3), (xm - 10, yc + 3), closed=True)
    # three bells over the axes, and the crank lever across the top
    d.group('mid')
    for x in xs:
        d.arc(x, top - 8, 8, 180, 360, n=16)
        d.line((x - 9, top - 8), (x + 9, top - 8))
        d.line((x, top - 16), (x, top - 22))
    d.group()
    d.line((200, top - 22), (200, top - 34), (330, top - 34))
    d.circle(338, top - 34, 7)
    # labels
    d.group()
    for name, x in cols.items():
        d.text(x, bottom + 24, name, size=7)
    d.text(38, top + cage / 2 + 3, '10⁴', size=7, anchor='end')
    d.text(38, bottom - cage * 1.5 + 3, '10⁰', size=7, anchor='end')
    d.text(38, bottom - cage / 2 + 3, '—', size=7, anchor='end')
    d.text(200, 20, 'THREE AXES · SIX CAGES · A BELL EACH', size=7)
    d.text(200, 282, 'TABLE ← 1ST DIFF ← 2ND DIFF, EACH TURN OF THE HANDLE', size=8)
    return d


def mill_and_barrels():
    """A barrel with studs setting control levers (a microprogram word per vertical), its reducing sectors of
    1, 2 and 4 teeth; and the anticipating carriage's column of fixed and movable wires through nines."""
    d = D()
    # --- the barrel, in elevation: a cylinder whose verticals of studs turn to face the levers
    bx, by0, by1, br = 78, 52, 212, 30
    nlev = 9
    lever_y = [by0 + 14 + (by1 - by0 - 28) * i / (nlev - 1) for i in range(nlev)]
    # the stud pattern: verticals (columns) × levers (rows); 1 is a stud
    pattern = ['101100010', '010011001', '110001100', '001110010', '100100101', '011000110']
    angles = [-60, -36, -12, 12, 36, 60]  # where each vertical stands on the visible face
    d.group('thin')
    d.line((bx, by0 - 18), (bx, by1 + 18))
    d.lines([[(bx + br * math.sin(math.radians(a)), by0), (bx + br * math.sin(math.radians(a)), by1)] for a in angles])
    d.lines([[(bx - br - 6, y), (bx + br + 70, y)] for y in lever_y])
    d.group()
    d.line((bx - br, by0), (bx - br, by1))
    d.line((bx + br, by0), (bx + br, by1))
    d.ellipse(bx, by0, br, 6)
    d.arc(bx, by1, br, 0, 180, n=24, ry=6)
    # the studs, drawn on each vertical; the front vertical (the one acting this cycle) is the fourth
    d.group('mid')
    for a, word in zip(angles, pattern):
        x = bx + br * math.sin(math.radians(a))
        for y, bit in zip(lever_y, word):
            if bit == '1':
                d.circle(x, y, 2.2 * math.cos(math.radians(a)) + 0.6)
    # the control levers: the acting vertical's studs push theirs over (drawn tilted), the rest stand
    d.group()
    act_x = bx + br * math.sin(math.radians(12)) + 4
    for y, bit in zip(lever_y, pattern[3]):
        if bit == '1':
            d.line((act_x, y), (act_x + 58, y - 5))
        else:
            d.line((act_x + 8, y), (act_x + 58, y))
        d.circle(act_x + 60, y - (5 if bit == '1' else 0), 1.6)
    # the reducing apparatus under the barrel: sectors of one, two and four teeth
    d.group('mid')
    for i, teeth in enumerate((1, 2, 4)):
        cx, cy, r = 40 + 38 * i, 250, 12
        d.arc(cx, cy, r, 200, 340, n=12)
        for t in range(teeth):
            a = math.radians(-90 - 18 * (teeth - 1) / 2 + 18 * t)
            d.line((cx + r * math.cos(a - 0.12), cy + r * math.sin(a - 0.12)),
                   (cx + (r + 5) * math.cos(a), cy + (r + 5) * math.sin(a)),
                   (cx + r * math.cos(a + 0.12), cy + r * math.sin(a + 0.12)))
        d.circle(cx, cy, 2)
    # --- the anticipating carriage: a column of cages, digits 4 9 9 7 (+5 in the units makes a carry)
    cx0, top, cage = 292, 60, 36
    digits = [4, 9, 9, 7]  # thousands, hundreds, tens, units, top to bottom
    ys = [top + cage * k for k in range(len(digits) + 1)]
    d.group('thin')
    d.lines([[(cx0 - 60, y), (cx0 + 70, y)] for y in ys])
    d.line((cx0, top - 12), (cx0, ys[-1] + 4))
    d.line((cx0 + 34, top - 12), (cx0 + 34, ys[-1] + 4))
    d.group()
    for k, v in enumerate(digits):
        yc = ys[k] + cage / 2
        _rect(d, cx0 - 24, yc - 6, cx0 + 24, yc + 6)
    # fixed wires in every cage; a movable wire lies between them only where the wheel stands at 9
    d.group('mid')
    wx = cx0 + 34
    for k, v in enumerate(digits):
        y0, y1 = ys[k], ys[k + 1]
        d.line((wx - 3, y1 - 2), (wx - 3, y1 - 12))  # fixed wire, from the cage floor
        if v == 9:
            d.line((wx + 3, y1 - 12), (wx + 3, y0 + 4))  # movable wire, carried in the wheel's arm
    # the chain: the carry from the units lifts straight through the nines, in one unit of time
    d.group()
    ytop_chain = ys[1] + 2
    d.line((wx + 14, ys[-1] - 4), (wx + 14, ytop_chain))
    _arrow(d, wx + 14, ytop_chain, -math.pi / 2)
    # labels
    d.group()
    d.text(bx, 36, 'BARREL', size=7)
    d.text(bx + 64, 36, 'LEVERS', size=7)
    d.text(78, 282, 'STUDS 1 · 2 · 4', size=7)
    for k, v in enumerate(digits):
        d.text(cx0, ys[k] + cage / 2 + 3, str(v), size=9)
    d.text(cx0 - 30, ys[-1] - cage / 2 + 3, '+5', size=8, anchor='end')
    d.text(cx0 + 16, 36, 'CARRY', size=7)
    d.text(cx0 + 16, 214, '4997 + 5 = 5002', size=8)
    d.text(cx0 + 16, 228, 'ALL CARRIES AT ONCE', size=7)
    d.text(cx0 + 16, 282, 'THE MILL: MICROPROGRAM AND CARRY', size=7)
    return d


def scheutz_engine():
    """The Scheutz engine's number wheels as a 15 × 5 array (the table and four differences), the additions
    down the rows, and the eight type wheels that print the table row's leading figures."""
    d = D()
    ncol, nrow = 15, 5
    x0, pitch, y0, rp = 58, 16, 60, 32
    xs = [x0 + pitch * i for i in range(ncol)]
    ys = [y0 + rp * j for j in range(nrow)]
    r = 6
    d.group('thin')
    d.lines([[(x, y0 - 16), (x, ys[-1] + 14)] for x in xs])
    d.lines([[(x0 - 26, y), (xs[-1] + 14, y)] for y in ys])
    # the eight leading columns carried up to the type wheels
    d.lines([[(x, y0 - 16), (x, 30)] for x in xs[:8]])
    d.group()
    for y in ys:
        for x in xs:
            d.circle(x, y, r)
    # the frame round the array
    d.group('mid')
    _rect(d, x0 - 14, y0 - 14, xs[-1] + 14, ys[-1] + 14)
    # additions: each difference row is added into the row above it
    for j in range(nrow - 1, 0, -1):
        ya, yb = ys[j] - r - 2, ys[j - 1] + r + 2
        d.line((x0 - 22, ya), (x0 - 22, yb))
        _arrow(d, x0 - 22, yb, -math.pi / 2)
    # the type wheels and the strip they impress
    d.group()
    for x in xs[:8]:
        d.ellipse(x, 26, 7, 4)
    d.line((xs[0] - 12, 12), (xs[7] + 12, 12))
    # the printed lines: a table as the engine would set it, in 8 figures
    d.group('mid')
    tx = 316
    d.line((tx - 6, 30), (tx + 70, 30), (tx + 70, 196), (tx - 6, 196), closed=True)
    d.lines([[(tx, 44 + 12 * k), (tx + 64, 44 + 12 * k)] for k in range(13)])
    # labels
    d.group()
    for j, lab in enumerate(['T', 'Δ¹', 'Δ²', 'Δ³', 'Δ⁴']):
        d.text(x0 - 34, ys[j] + 3, lab, size=8, anchor='end')
    d.text((xs[0] + xs[7]) / 2, 8, '8 TYPE WHEELS', size=7)
    d.text((xs[0] + xs[-1]) / 2, ys[-1] + 34, '15 FIGURES × TABLE AND 4 DIFFERENCES', size=7)
    d.text(tx + 32, 210, 'STEREOTYPE', size=7)
    d.text(tx + 32, 222, 'MOULD', size=7)
    d.text(200, 272, 'STOCKHOLM 1853 · LONDON COPY 1859', size=8)
    return d


def difference_engine_2():
    """Difference Engine No. 2 in elevation, to scale (11 ft by 7 ft): output apparatus, eight columns of 31
    figure wheels (the table and seven differences), and the stack of 28 cams at the crank end."""
    d = D()
    s = 28  # px per foot
    L, H = 11 * s, 7 * s
    x0, y0 = 30, 36
    base = y0 + H
    out_x1 = x0 + 3.1 * s  # output apparatus
    cam_x0 = x0 + L - 1.6 * s  # cam stack and crank
    col_x = [out_x1 + 16 + (cam_x0 - out_x1 - 32) * i / 7 for i in range(8)]
    col_top, col_bot = y0 + 18, base - 36
    d.group('thin')
    _span(d, x0, base + 18, x0 + L, base + 18)
    _span(d, x0 + L + 16, y0, x0 + L + 16, base)
    d.lines([[(x, y0 + 6), (x, base + 8)] for x in col_x])
    d.lines([[(x0 - 8, y), (x0 + L + 8, y)] for y in (y0, base)])
    # the frame
    d.group()
    d.line((x0, base), (x0 + L, base))
    d.line((out_x1, y0 + 10), (cam_x0, y0 + 10))
    d.line((out_x1, base - 24), (cam_x0, base - 24))
    d.lines([[(x, y0 + 10), (x, base)] for x in (out_x1, cam_x0)])
    # the columns: 31 figure wheels each, drawn as short bars at their pitch
    d.group('mid')
    pitch = (col_bot - col_top) / 30
    wheels = []
    for x in col_x:
        wheels += [[(x - 7, col_top + pitch * k), (x + 7, col_top + pitch * k)] for k in range(31)]
    d.lines(wheels)
    d.group()
    d.lines([[(x, col_top - 6), (x, col_bot + 6)] for x in col_x])
    # the cam stack: 14 pairs of conjugate cams, each an ellipse seen edge-on
    d.group('mid')
    cx = cam_x0 + 0.8 * s
    cy0, cy1 = y0 + 30, base - 30
    for k in range(28):
        y = cy0 + (cy1 - cy0) * k / 27
        w = 13 if k % 2 == 0 else 10
        d.ellipse(cx, y, w, 2.2)
    d.line((cx, y0 + 16), (cx, base - 10))
    # the crank handle
    d.group()
    d.line((cx, y0 + 16), (cx + 22, y0 + 16), (cx + 22, y0 + 4))
    d.circle(cx + 22, y0 + 2, 3)
    # the output apparatus: print wheels over the paper roll, stereotype trays on a platform below
    d.group('mid')
    ox = x0 + 10
    d.line((ox, y0 + 40), (out_x1 - 8, y0 + 40), (out_x1 - 8, y0 + 110), (ox, y0 + 110), closed=True)
    d.circle(ox + 22, y0 + 128, 12)
    d.circle(ox + 64, y0 + 128, 12)
    d.lines([[(ox + 4, base - 30 - 6 * k), (out_x1 - 12, base - 30 - 6 * k)] for k in range(3)])
    d.lines([[(ox + 6 + 6 * k, y0 + 44), (ox + 6 + 6 * k, y0 + 106)] for k in range(13)])
    # labels
    d.group()
    for i, x in enumerate(col_x):
        d.text(x, y0 + 4, 'T' if i == 0 else f'Δ{"¹²³⁴⁵⁶⁷"[i - 1]}', size=7)
    d.text((x0 + L) / 2 + 18, base + 32, '11 FT', size=8)
    d.text(x0 + L + 22, (y0 + base) / 2, '7 FT', size=8, anchor='start')
    d.text((x0 + out_x1) / 2, y0 + 24, 'PRINTER', size=7)
    d.text(cx, base - 14, '28 CAMS', size=7)
    d.text(200, 292, '8 COLUMNS × 31 FIGURES · 8,000 PARTS · 5 TONNES', size=8)
    return d


PLATES = {
    'prony-tables': prony_tables,
    'clement-fragment': clement_fragment,
    'mill-and-barrels': mill_and_barrels,
    'scheutz-engine': scheutz_engine,
    'difference-engine-2': difference_engine_2,
}
