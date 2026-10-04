"""Plates for western-civ's trail Rome, from Republic to Byzantium (sprint 049, part rome). See plates_for.py."""
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


def twelve_tables():
    d = D()
    # Top: the twelve tables as twelve bronze tablets in two rows, I and III (procedure, and the
    # execution of judgment) drawn at full weight. Bottom: Table III as a time line in days, to
    # scale: thirty days to pay, then the creditor lays hands on the debtor, then up to sixty days
    # in bonds, with three market days (nundinae, every eighth day) at the end of them, after
    # which he was put to death or sold across the Tiber (Gellius 20.1.45-49).
    tw, th, gap = 40, 46, 8
    x0 = 200 - (6 * tw + 5 * gap) / 2
    rows = (24, 24 + th + 12)
    tabs = [(x0 + (i % 6) * (tw + gap), rows[i // 6]) for i in range(12)]
    ax0, ax1, ay = 40, 300, 222                                        # the day axis
    days = 90
    sx = (ax1 - ax0) / days

    def X(day):
        return ax0 + day * sx

    d.group('thin')
    d.line((x0 - 10, rows[0] - 6), (x0 + 6 * tw + 5 * gap + 10, rows[0] - 6))   # the rostra's line
    for day in range(0, days + 1, 10):                                 # a tick every ten days
        d.line((X(day), ay - 3), (X(day), ay + 3))
    for day in (0, 30, 90):                                            # construction up to the tablets
        d.line((X(day), ay - 34), (X(day), ay + 14))

    d.group('mid')
    for i, (x, y) in enumerate(tabs):
        if i in (0, 2):
            continue
        _box(d, x, y, tw, th)
        for k in range(5):                                             # ruled lines of text
            yy = y + 9 + k * 7
            d.line((x + 6, yy), (x + tw - 6, yy))

    d.group()
    for i in (0, 2):                                                   # Tables I and III
        x, y = tabs[i]
        _box(d, x, y, tw, th)
        for k in range(5):
            yy = y + 9 + k * 7
            d.line((x + 6, yy), (x + tw - 6 - (k % 2) * 6, yy))
    d.line((ax0, ay), (ax1, ay))                                       # the axis
    # the thirty days, then sixty in bonds, drawn as brackets above the axis
    d.line((X(0), ay - 18), (X(0), ay - 24), (X(30), ay - 24), (X(30), ay - 18))
    d.line((X(30), ay - 30), (X(30), ay - 36), (X(90), ay - 36), (X(90), ay - 30))
    for md in (74, 82, 90):                                            # three market days
        d.circle(X(md), ay, 3.2)
    # the two ends after the third market day
    d.line((X(90), ay), (X(90) + 14, ay + 24))
    d.line((X(90), ay), (X(90) + 14, ay - 4))
    _arrow(d, (X(90), ay), (X(90) + 14, ay + 24), 4)
    _arrow(d, (X(90), ay), (X(90) + 14, ay - 4), 4)
    # where hand is laid on: a hand's mark at day 30
    d.line((X(30), ay - 8), (X(30), ay + 8))

    d.group('mid')
    for i, (x, y) in enumerate(tabs):
        d.text(x + tw / 2, y + th + 9, ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
                                        'XI', 'XII'][i], size=7)
    d.text(X(15), ay - 28, '30 DAYS TO PAY', size=7)
    d.text(X(60), ay - 40, '60 DAYS IN BONDS', size=7)
    d.text(X(30), ay + 20, 'HAND LAID ON', size=7)
    d.text(X(80), ay + 20, '3 MARKET DAYS', size=7)
    d.text(X(0), ay + 20, 'JUDGMENT', size=7)
    d.text(X(90) + 18, ay - 4, 'DEATH', size=7, anchor='start')
    d.text(X(90) + 18, ay + 28, 'SOLD', size=7, anchor='start')
    d.text(X(90) + 18, ay + 37, 'ACROSS TIBER', size=7, anchor='start')
    d.text(200, 282, 'TABLE III · DAYS FROM JUDGMENT', size=7)
    return d


def cicero():
    d = D()
    # The assembly of centuries as Livy and Dionysius describe its first form: 193 voting centuries
    # in the order they were called, the knights (18) first, then the first class (80, with 2
    # centuries of engineers), then classes II-V (20, 20, 20, 30), then 2 of musicians and 1 of
    # the proletarii. A majority is 97 of 193, so the voting stopped inside the first class whenever
    # the rich agreed. Below: the assembly of tribes, 35 votes, 18 to carry.
    groups = [('EQ', 18), ('I', 82), ('II', 20), ('III', 20), ('IV', 20), ('V', 30), ('', 3)]
    cols, cell = 20, 13
    gx0, gy0 = 200 - cols * cell / 2, 46
    n = sum(c for _, c in groups)                                      # 193

    def pos(i):
        return gx0 + (i % cols) * cell, gy0 + (i // cols) * cell

    majority = n // 2 + 1                                              # 97

    d.group('thin')
    rows = math.ceil(n / cols)
    for r in range(rows + 1):                                          # the grid's frame
        d.line((gx0, gy0 + r * cell), (gx0 + cols * cell, gy0 + r * cell))
    for c in range(cols + 1):
        d.line((gx0 + c * cell, gy0), (gx0 + c * cell, gy0 + rows * cell))

    d.group()
    for i in range(majority):                                          # the centuries that decide
        x, y = pos(i)
        _box(d, x + 2, y + 2, cell - 4, cell - 4)

    d.group('mid')
    for i in range(majority, n):                                       # the centuries seldom called
        x, y = pos(i)
        d.line((x + 3, y + cell - 3), (x + cell - 3, y + 3))
    # where each group begins, a stroke on the cell's left
    start = 0
    starts = []
    for name, c in groups:
        starts.append((name, start, c))
        x, y = pos(start)
        d.line((x, y - 3), (x, y + cell + 3))
        start += c

    d.group()
    # the majority: a heavy mark after the 97th century
    x, y = pos(majority - 1)
    d.line((x + cell, y - 6), (x + cell, y + cell + 6))
    # the tribes: 35 cells, the first 18 drawn whole
    ty = gy0 + rows * cell + 40
    tcell = 9
    tx0 = 200 - 35 * tcell / 2
    for i in range(35):
        if i < 18:
            _box(d, tx0 + i * tcell + 1.5, ty + 1.5, tcell - 3, tcell - 3)
    d.line((tx0 + 18 * tcell, ty - 5), (tx0 + 18 * tcell, ty + tcell + 5))

    d.group('thin')
    d.line((tx0, ty), (tx0 + 35 * tcell, ty), (tx0 + 35 * tcell, ty + tcell), (tx0, ty + tcell),
           closed=True)
    for i in range(1, 35):
        d.line((tx0 + i * tcell, ty), (tx0 + i * tcell, ty + tcell))

    d.group('mid')
    for name, s0, c in starts:
        x, y = pos(s0)
        if not name:                                                   # musicians and proletarii
            d.text(x + 2, y + cell + 10, '+3', size=7, anchor='start')
        elif s0 % cols == 0 and s0:                                    # a class that starts a row
            d.text(gx0 - 5, y + cell / 2 + 3, name, size=7, anchor='end')
        else:                                                          # the first row
            d.text(x + 2, y - 5, name, size=7, anchor='start')
    x, y = pos(majority - 1)
    d.text(gx0 + cols * cell + 5, y + cell / 2 + 3, '97 OF 193', size=7, anchor='start')
    d.text(200, 30, 'CENTURIES · IN VOTING ORDER', size=7)
    d.text(200, ty - 9, 'TRIBES · 18 OF 35', size=7)
    d.text(200, ty + tcell + 16, 'ONE VOTE A UNIT · A MAJORITY OF UNITS DECIDES', size=7)
    return d


def fall_of_constantinople():
    d = D()
    # The Theodosian land walls in section, west (the attackers' side) to east (the city), to scale
    # from the dimensions in Wikipedia's "Walls of Constantinople": moat over 20 m wide and up to
    # 10 m deep with a 1.5 m breastwork on its inner lip; a terrace about 20 m wide (the
    # parateichion); the outer wall, 2 m thick at its base, 8.5-9 m high, its towers 12-14 m;
    # the peribolos (no width given there: drawn 15 m and not dimensioned); the inner wall,
    # 4.5-6 m thick and 12 m high, its towers 15-20 m. A ball's path comes in from the left.
    s = 4.6                                                            # px per meter
    gy = 190                                                           # ground level
    x = 24
    moat0, moat1 = x, x + 20 * s
    para1 = moat1 + 20 * s
    ow0, ow1 = para1, para1 + 2 * s
    peri1 = ow1 + 15 * s
    iw0, iw1 = peri1, peri1 + 5 * s
    city1 = 390

    def Y(m):
        return gy - m * s

    d.group('thin')
    for m in range(0, 21, 5):                                          # height lines every 5 m
        d.line((14, Y(m)), (city1, Y(m)))
    d.line((14, Y(-10)), (moat1 + 6, Y(-10)))
    # dimension lines
    d.line((moat0, Y(-14)), (moat1, Y(-14)))
    for xx in (moat0, moat1):
        d.line((xx, Y(-12)), (xx, Y(-16)))
    d.line((moat0 - 8, Y(0)), (moat0 - 8, Y(-10)))
    d.line((ow0 - 10, Y(0)), (ow0 - 10, Y(8.5)))
    d.line((iw1 + 10, Y(0)), (iw1 + 10, Y(12)))

    d.group()
    # the ground, the moat cut into it, the breastwork on its inner lip
    d.line((14, Y(0)), (moat0, Y(0)), (moat0 + 2 * s, Y(-10)), (moat1 - 2 * s, Y(-10)), (moat1, Y(0)),
           (moat1, Y(1.5)), (moat1 + 0.8 * s, Y(1.5)), (moat1 + 0.8 * s, Y(0)), (ow0, Y(0)))
    # the outer wall, battlemented
    d.line((ow0, Y(0)), (ow0, Y(8.5)), (ow0 + 0.6 * s, Y(8.5)), (ow0 + 0.6 * s, Y(9.2)),
           (ow0 + 1.4 * s, Y(9.2)), (ow0 + 1.4 * s, Y(8.5)), (ow1, Y(8.5)), (ow1, Y(0)))
    d.line((ow1, Y(0)), (iw0, Y(0)))                                   # the peribolos
    # the inner wall, thicker and higher
    d.line((iw0, Y(0)), (iw0, Y(12)), (iw0 + 1.0 * s, Y(12)), (iw0 + 1.0 * s, Y(12.8)),
           (iw0 + 2.0 * s, Y(12.8)), (iw0 + 2.0 * s, Y(12)), (iw0 + 3.0 * s, Y(12)),
           (iw0 + 3.0 * s, Y(12.8)), (iw0 + 4.0 * s, Y(12.8)), (iw0 + 4.0 * s, Y(12)),
           (iw1, Y(12)), (iw1, Y(0)))
    d.line((iw1, Y(0)), (city1, Y(0)))

    d.group('mid')
    # the towers behind, in outline: outer 13 m, inner 18 m
    d.line((ow0 - 1 * s, Y(8.5)), (ow0 - 1 * s, Y(13)), (ow1 + 2 * s, Y(13)), (ow1 + 2 * s, Y(8.5)))
    d.line((iw0 - 2 * s, Y(12)), (iw0 - 2 * s, Y(18)), (iw1 + 3 * s, Y(18)), (iw1 + 3 * s, Y(12)))
    # brick bands in the inner wall
    for m in (3, 6, 9):
        d.line((iw0, Y(m)), (iw1, Y(m)))
    # a ball's path, a parabola from off the plate to the outer wall's face
    pts = []
    for k in range(0, 41):
        t = k / 40
        px = 14 + t * (ow0 - 14)
        py = Y(5) - 70 * 4 * t * (1 - t) * 0.5
        pts.append((px, py))
    d.line(*pts)
    _arrow(d, pts[-2], pts[-1], 5)

    d.group('mid')
    d.text((moat0 + moat1) / 2, Y(-14) + 11, 'MOAT 20 M', size=7)
    d.text(moat0 - 11, Y(-5) + 3, '10', size=7, anchor='end')
    d.text(ow0 - 13, Y(4.25) + 3, '8.5', size=7, anchor='end')
    d.text(iw1 + 13, Y(6) + 3, '12', size=7, anchor='start')
    d.text((ow0 + ow1) / 2, Y(-4), 'OUTER', size=7)
    d.text((iw0 + iw1) / 2, Y(-4), 'INNER', size=7)
    d.text((ow1 + iw0) / 2, Y(2), 'PERIBOLOS', size=7)
    d.text(30, 40, 'WEST', size=7, anchor='start')
    d.text(380, 40, 'CITY', size=7, anchor='end')
    d.text(200, 282, 'THEODOSIAN LAND WALLS · SECTION · METERS', size=7)
    return d


PLATES = {
    'twelve-tables': twelve_tables,
    'cicero': cicero,
    'fall-of-constantinople': fall_of_constantinople,
}
