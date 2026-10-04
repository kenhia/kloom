"""Plates for western-civ's part mod1 (sprint 049): the modern world. See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


# The refrain of the Sacrificial Dance, bars 1-33, in sixteenths, as the 1921 score bars it
# (Smirnov 2004; bars 1-13 checked against the score, B. & H. 16333, p. 112). 2/8 is 4, 3/8 is 6.
SACRALE = [3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 3, 5, 4, 3, 4, 5, 5, 4, 5, 4, 3, 2, 3, 4, 6, 3, 2, 3, 4, 2, 3, 3, 4]
# The first outburst of the Augurs of Spring: eighth notes between accents (Roger Nichols).
AUGURS = [9, 2, 6, 3, 4, 5, 3]


def rite_of_spring():
    d = D()
    # Top: the 33 bars drawn to scale, one unit a sixteenth, broken into rows at bar lines.
    # Bottom: the 32 even eighth notes of the Augurs' first outburst, with Nichols's accents.
    u = 8.6                                    # width of a sixteenth
    x0, y0, bh, gap = 34, 40, 26, 50
    rows, row, n = [], [], 0
    for i, v in enumerate(SACRALE):
        if n + v > 40 and row:
            rows.append(row)
            row, n = [], 0
        row.append((i + 1, v))
        n += v
    rows.append(row)

    d.group('thin')
    for r, row in enumerate(rows):                       # the sixteenth grid under each row
        y = y0 + r * gap
        total = sum(v for _, v in row)
        d.line((x0, y + bh + 6), (x0 + total * u, y + bh + 6))
        for k in range(total + 1):
            d.line((x0 + k * u, y + bh + 4), (x0 + k * u, y + bh + 8))
    ya = 232
    d.line((x0, ya + 12), (x0 + 32 * 10.5, ya + 12))      # the chord's time line, 32 eighths
    for k in range(0, 33, 8):
        d.line((x0 + k * 10.5, ya + 9), (x0 + k * 10.5, ya + 15))

    d.group()
    for r, row in enumerate(rows):                       # the bars
        y = y0 + r * gap
        x = x0
        for _, v in row:
            _box(d, x, y, v * u, bh)
            x += v * u

    d.group('mid')
    for r, row in enumerate(rows):                       # sixteenths inside each bar
        y = y0 + r * gap
        x = x0
        for _, v in row:
            for k in range(1, v):
                d.line((x + k * u, y + bh - 5), (x + k * u, y + bh))
            x += v * u
    # the chord's 32 even strokes, the accented ones long
    accents, k = set(), 0
    for g in AUGURS:
        accents.add(k)
        k += g
    for k in range(32):
        x = x0 + k * 10.5 + 5.25
        if k in accents:
            d.line((x, ya - 8), (x, ya + 8))
            d.line((x - 3, ya - 18), (x + 3, ya - 15), (x - 3, ya - 12))   # an accent sign
        else:
            d.line((x, ya - 3), (x, ya + 3))

    d.group('mid')
    for r, row in enumerate(rows):
        y = y0 + r * gap
        d.text(x0 - 6, y + bh / 2 + 3, str(row[0][0]), size=7, anchor='end')
        x = x0
        for _, v in row:
            d.text(x + v * u / 2, y - 4, f'{v}', size=7)
            x += v * u
    d.text(x0, 20, 'DANSE SACRALE · BARS 1–33 · IN SIXTEENTHS', size=7, anchor='start')
    d.text(x0, 204, 'AUGURS OF SPRING · ACCENTS 9 2 6 3 4 5 3', size=7, anchor='start')
    d.text(x0, 262, 'E♭7 OVER F♭ · ONE STROKE AN EIGHTH', size=7, anchor='start')
    return d


def great_war():
    d = D()
    # The trench system to the British General Staff's Notes for Infantry Officers on Trench
    # Warfare (1916; US War Department Document 582, 1917). Top: three bays of a fire trench at
    # 3 units a foot: bays 18-30 ft (24 here) between traverses 9-12 ft thick (10 here), which
    # overlap the trench's width by at least 2 ft; firing step 18 in and bottom about 2 ft 6 in,
    # so the trench is drawn 4 ft wide. Bottom: a sector of the system at 1.1 units a yard: the
    # support line 70-100 yd behind (85 here), one communication trench behind every second
    # traverse, and the reserve line 400-600 yd behind, past a break.
    f = 3.0                                    # detail: units per foot
    w, bay, trav, back = 4 * f, 24 * f, 10 * f, 6 * f
    dx0, F = 47, 46                            # detail origin; the front wall's line
    s = 1.1                                    # system: units per yard
    x0, x1 = 22, 378
    yw, yf = 136, 150
    ys = yf + 85 * s
    yb, yr = 262, 280
    pb, pt, pst = 8 * s, 10 / 3 * s, 2.2 * s   # the system's bay, traverse and step

    front, rear, blocks, x = [(dx0 - 20, F)], [(dx0 - 20, F + w)], [], dx0
    for k in range(3):
        x += bay if k else 0
        front += [(x, F), (x, F + back), (x + trav, F + back), (x + trav, F)]
        rear += [(x - w, F + w), (x - w, F + back + w), (x + trav + w, F + back + w), (x + trav + w, F + w)]
        blocks.append(x)
        x += trav
    front.append((x + bay, F))
    rear.append((x + bay, F + w))

    sysp, tx, x = [(x0, yf)], [], x0
    while x + pb + pt < x1:
        x += pb
        sysp += [(x, yf), (x, yf + pst)]
        tx.append(x)
        x += pt
        sysp += [(x, yf + pst), (x, yf)]
    sysp.append((x1, yf))
    sup, x = [(x0, ys)], x0
    while x + 3 * pb + pt < x1:
        x += 3 * pb
        sup += [(x, ys), (x, ys + pst)]
        x += pt
        sup += [(x, ys + pst), (x, ys)]
    sup.append((x1, ys))

    d.group('thin')
    b0 = blocks[0]                             # dimensions on the detail: a bay and a traverse
    for xx in (b0 + trav, blocks[1], blocks[1] + trav):
        d.line((xx, F - 6), (xx, F - 16))
    d.line((b0 + trav, F - 11), (blocks[1], F - 11))
    d.line((blocks[1], F - 11), (blocks[1] + trav, F - 11))
    for y in (yf, ys):                         # the support line's distance
        d.line((x1 - 30, y), (x1 - 18, y))
    d.line((x1 - 24, yf + 2), (x1 - 24, ys - 2))
    for xa, xb in ((x0, x0 + 40), (x1 - 40, x1)):   # the break
        d.line((xa, yb - 3), (xb, yb - 3))
        d.line((xa, yb + 3), (xb, yb + 3))
    d.line((x0, 118), (x1, 118))               # between detail and system

    d.group()
    d.line(*front)
    d.line(*rear)
    d.line(*sysp)
    d.line(*sup)
    d.line((x0 + 40, yr), (x1 - 40, yr))

    d.group('mid')
    for b in blocks:                           # the traverses: earth, revetted
        _box(d, b, F - 3, trav, back - 0 + 3)
        d.line((b, F - 3), (b + trav, F + back))
        d.line((b + trav, F - 3), (b, F + back))
    edges = [dx0 - 20] + [v for bk in blocks for v in (bk, bk + trav)] + [front[-1][0]]
    for xa, xb in zip(edges[::2], edges[1::2]):   # the firing step's edge, in each bay
        d.line((xa, F + w * 0.4), (xb, F + w * 0.4))
    for k, x in enumerate(tx):                 # communication trenches behind every second traverse
        if k % 4 != 1:
            continue
        cx = x + pt / 2
        zz, y, side = [(cx, yf + pst)], yf + pst, 1
        while y + 8 < ys:
            y += 8
            zz.append((cx + side * 3.5, y))
            side = -side
        zz.append((cx, ys))
        d.line(*zz)
        if k % 8 == 1:
            d.line((cx, ys + pst), (cx + 3, ys + 10), (cx - 3, ys + 18), (cx, yb - 6))
    x = x0 + 4
    while x < x1:                              # the wire
        d.line((x - 2.5, yw - 2.5), (x + 2.5, yw + 2.5))
        d.line((x - 2.5, yw + 2.5), (x + 2.5, yw - 2.5))
        x += 8
    d.line((360, 30), (360, 12))
    _arrow(d, (360, 30), (360, 12), 5)

    d.group('mid')
    d.text(352, 20, 'ENEMY', size=7, anchor='end')
    d.text((b0 + trav + blocks[1]) / 2, F - 15, 'BAY 24 FT', size=7)
    d.text(blocks[1] + trav / 2 + 2, F - 15, '10 FT', size=7, anchor='start')
    d.text(dx0 - 20, 102, 'FIRE TRENCH · TRAVERSES', size=7, anchor='start')
    d.text(x0, yw - 6, 'WIRE', size=7, anchor='start')
    d.text(x0, ys - 6, 'SUPPORT LINE', size=7, anchor='start')
    d.text(x1 - 28, (yf + ys) / 2 + 3, '85 YD', size=7, anchor='end')
    d.text(200, yb + 3, '400–600 YD', size=7)
    d.text(x0 + 40, yr - 6, 'RESERVE LINE', size=7, anchor='start')
    return d

# Combat aircraft built, thousands a year, 1939-1944 (Harrison 1998, table 1-6); None before a
# power was at war in the count. 1945 is left off: its months differ from power to power.
AIRCRAFT = {
    'USA': [None, None, 1.4, 24.9, 54.1, 74.1],
    'USSR': [None, None, 8.2, 21.7, 29.9, 33.2],
    'UK': [1.3, 8.6, 13.2, 17.7, 21.2, 22.7],
    'GERMANY': [2.3, 6.6, 8.4, 11.6, 19.3, 34.1],
    'JAPAN': [0.7, 2.2, 3.2, 6.3, 13.4, 21.0],
}


def second_world_war():
    d = D()
    # A chart drawn as a plate: combat aircraft built each year by the five great powers.
    gx0, gx1, gy0, gy1 = 56, 318, 252, 40      # plot area: left, right, bottom, top
    vmax = 80

    def X(i):
        return gx0 + (gx1 - gx0) * i / 5

    def Y(v):
        return gy0 - (gy0 - gy1) * v / vmax

    d.group('thin')
    for v in (0, 20, 40, 60, 80):
        d.line((gx0, Y(v)), (gx1, Y(v)))
    for i in range(6):
        d.line((X(i), gy0), (X(i), gy0 + 5))

    d.group()
    d.line((gx0, gy1 - 6), (gx0, gy0), (gx1 + 6, gy0))
    for name, vals in AIRCRAFT.items():
        pts = [(X(i), Y(v)) for i, v in enumerate(vals) if v is not None]
        d.line(*pts)

    d.group('mid')
    for name, vals in AIRCRAFT.items():        # the year's marks
        for i, v in enumerate(vals):
            if v is not None:
                d.circle(X(i), Y(v), 2.2)
    # Germany's 1944 and America's, compared
    d.line((X(5) + 8, Y(74.1)), (X(5) + 14, Y(74.1)))
    d.line((X(5) + 8, Y(34.1)), (X(5) + 14, Y(34.1)))
    d.line((X(5) + 11, Y(74.1)), (X(5) + 11, Y(34.1)))

    d.group('mid')
    for v in (0, 20, 40, 60, 80):
        d.text(gx0 - 6, Y(v) + 3, str(v), size=7, anchor='end')
    for i, yr in enumerate(range(1939, 1945)):
        d.text(X(i), gy0 + 16, str(yr), size=7)
    ends = {'USA': 74.1, 'USSR': 36.5, 'UK': 25.4, 'GERMANY': 31.0, 'JAPAN': 18.0}
    for name, v in ends.items():
        d.text(X(5) + 20, Y(v) + 3, name, size=7, anchor='start')
    d.text(gx0, 24, 'COMBAT AIRCRAFT BUILT · THOUSANDS A YEAR', size=7, anchor='start')
    d.text(X(5) + 20, Y(54) + 3, '× 2.2', size=7, anchor='start')
    return d


PLATES = {'rite-of-spring': rite_of_spring, 'great-war': great_war, 'second-world-war': second_world_war}
