"""computing plates, segment "Engines of arithmetic" (sprint 015). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def pascaline():
    """The Pascaline's carry, simplified: two digit wheels, the units wheel's two carry pins,
    and the sautoir, a weighted lever swinging about the tens wheel's arbor. Turning the units
    wheel from 4 to 9 lifts it; at 9 to 0 it drops, and its pawl kicks the tens wheel one step (36°)."""
    d = D()
    L, R = (122, 168), (278, 168)  # tens and units arbors
    rim, pin_r = 64, 52
    lever = 128  # the sautoir's length from the tens arbor to its tail over the carry pins
    rest, lifted = 4, 21  # the sautoir's angle (degrees above horizontal) at rest and fully lifted
    # construction: the centre line, each arbor's cross, the sautoir's arc of travel, one step of 36°
    d.group('thin')
    d.line((40, L[1]), (360, R[1]))
    for cx, cy in (L, R):
        d.line((cx, cy - rim - 10), (cx, cy + rim + 10))
    d.arc(L[0], L[1], lever, -rest + 8, -lifted - 8, n=24)
    for deg in (90, 126):
        d.line(R, _polar(R[0], R[1], rim + 14, deg))
    d.arc(R[0], R[1], rim + 8, -90, -126, n=12)
    # the two wheels: rims, hubs and ten pins apiece
    d.group()
    for cx, cy in (L, R):
        d.circle(cx, cy, rim)
        d.circle(cx, cy, 9)
    d.group('mid')
    for cx, cy in (L, R):
        for k in range(10):
            px, py = _polar(cx, cy, pin_r, 90 + 36 * k)
            d.circle(px, py, 3.2)
        d.lines([[_polar(cx, cy, 9, 90 + 72 * k), _polar(cx, cy, pin_r - 5, 90 + 72 * k)] for k in range(5)])
    # the units wheel's two carry pins: the first sits just under the sautoir's tail, the second
    # 36° further round (the wheel turns clockwise), so the lift spans the turn from 4 to 9
    d.group()
    tx, ty = _polar(L[0], L[1], lever, rest)
    pr = math.dist(R, (tx, ty + 5.4))
    pa = math.degrees(math.atan2(-(ty + 5.4 - R[1]), tx - R[0]))
    carry = [_polar(R[0], R[1], pr, a) for a in (pa, pa + 36)]
    for px, py in carry:
        d.circle(px, py, 4.2)
    # the sautoir: lifted (thin, where the pins leave it) and at rest (full weight), with its weight and pawl
    d.group('thin')
    tip_up = _polar(L[0], L[1], lever, lifted)
    d.line(_polar(L[0], L[1], 14, lifted), tip_up)
    d.group()
    tip = _polar(L[0], L[1], lever, rest)
    base = _polar(L[0], L[1], 14, rest)
    d.line(base, tip)
    nx, ny = -math.sin(math.radians(rest)), -math.cos(math.radians(rest))  # the lever's upward normal
    d.line(tip, (tip[0] + 6 * nx - 8, tip[1] + 6 * ny))
    wx, wy = _polar(L[0], L[1], 80, rest)
    d.line((wx - 7, wy - 5), (wx + 7, wy - 7), (wx + 8, wy + 5), (wx - 6, wy + 7), closed=True)
    px0, py0 = _polar(L[0], L[1], 30, rest)
    pawl = _polar(L[0], L[1], pin_r - 1, rest + 14)
    d.line((px0, py0), pawl, (pawl[0] + 3, pawl[1] + 5))
    # details: gravity on the weight, the kick on the tens wheel, the lift under the tail
    d.group('mid')
    d.line((wx, wy + 12), (wx, wy + 34))
    _arrow(d, wx, wy + 34, math.pi / 2)
    kick = [_polar(L[0], L[1], pin_r + 9, a) for a in range(rest + 16, rest + 44, 4)]
    d.line(*kick)
    _arrow(d, kick[-1][0], kick[-1][1], math.atan2(kick[-1][1] - kick[-2][1], kick[-1][0] - kick[-2][0]))
    lx, ly = tip[0] + 4, tip[1] + 14
    d.line((lx, ly + 18), (lx, ly))
    _arrow(d, lx, ly, -math.pi / 2)
    # labels
    d.group()
    d.text(L[0], L[1] + rim + 22, 'TENS', size=8)
    d.text(R[0], R[1] + rim + 22, 'UNITS', size=8)
    d.text(wx + 4, wy + 46, 'g', size=8)
    d.text(tip_up[0] - 6, tip_up[1] - 10, 'SAUTOIR', size=8)
    d.text(R[0] - 12, R[1] - rim - 16, '36°', size=7, anchor='end')
    d.text(kick[-1][0] - 8, kick[-1][1] - 4, '+1', size=8, anchor='end')
    d.text(200, 32, '4 → 9 LIFTS IT · 9 → 0 DROPS IT · IT KICKS +1', size=8)
    d.text(200, 276, 'THE CARRY FALLS BY GRAVITY, SO EACH WHEEL CARRIES ALONE', size=7)
    return d


def jacquard_loom():
    """A Jacquard head in section, one card: eight needles, eight hooks, the griffe.
    Where the card has a hole the needle stays and its hook rides up on the griffe;
    where it is solid the needle is pushed back, its hook tips off the blade and stays down."""
    d = D()
    row = [1, 0, 1, 1, 0, 0, 1, 0]  # 1 = a hole in the card
    n = len(row)
    y0, dy = 104, 13  # the needles' heights
    ys = [y0 + dy * i for i in range(n)]
    xs = [172 + 20 * i for i in range(n)]  # each needle's hook
    card_x, push = 128, 9  # the card's face, and how far a solid card pushes a needle
    spring_x = 334
    griffe_y, lift = 62, 18  # the griffe blades at rest, and how far they rise
    grate_y = 244  # the hooks' feet rest on a grate: a pushed hook pivots there
    # construction: the needle rows, the hook lines, the griffe's rest and raised lines
    d.group('thin')
    d.lines([[(card_x - 24, y), (spring_x + 18, y)] for y in ys])
    d.lines([[(x, griffe_y - lift - 12), (x, grate_y + 8)] for x in xs])
    d.line((xs[0] - 12, griffe_y), (xs[-1] + 20, griffe_y))
    d.line((xs[0] - 12, griffe_y - lift), (xs[-1] + 20, griffe_y - lift))
    # the card cylinder, a square prism seen end on, pressed against the needles with the card between
    d.group()
    side = ys[-1] - ys[0] + 20
    cx1 = card_x - 4
    cy0 = ys[0] - 10
    d.line((cx1 - side, cy0), (cx1, cy0), (cx1, cy0 + side), (cx1 - side, cy0 + side), closed=True)
    # a hole in each face opposite each needle, for the needles the card lets through
    d.lines([[(cx1 - 7, y - 2.5), (cx1, y - 2.5)] for y in ys] + [[(cx1 - 7, y + 2.5), (cx1, y + 2.5)] for y in ys])
    segs = [[(card_x, cy0 - 6), (card_x, ys[0] - 4)], [(card_x, ys[-1] + 4), (card_x, cy0 + side + 6)]]
    for i in range(n - 1):
        segs.append([(card_x, ys[i] + 4), (card_x, ys[i + 1] - 4)])
    for i, y in enumerate(ys):
        if not row[i]:
            segs.append([(card_x, y - 4), (card_x, y + 4)])
    d.lines(segs)
    # the chain of cards: laced cards folding down from the prism
    d.group('mid')
    x_mid = cx1 - side / 2
    fold = []
    for k in range(6):
        yk = cy0 + side + 10 + 9 * k
        w = side / 2 + (4 if k % 2 else -2)
        fold.append((x_mid + (w if k % 2 else -w), yk))
    d.line((cx1 - side, cy0 + side), *fold)
    d.line((card_x, cy0 + side + 6), (cx1 + 4, cy0 + side + 10), (x_mid + side / 2 + 4, cy0 + side + 19))
    # the needles, pushed back where the card is solid, each with its eye round a hook
    d.group()
    for i, y in enumerate(ys):
        dx = 0 if row[i] else push
        tip = cx1 - 6 if row[i] else card_x + 1
        d.line((tip, y), (spring_x - 14 + dx, y))
        d.circle(xs[i] + dx, y, 2.6)
    # the springs that return the needles, in their box
    d.group('mid')
    for i, y in enumerate(ys):
        dx = 0 if row[i] else push
        x0, x1 = spring_x - 14 + dx, spring_x + 14
        d.line(*[(x0 + (x1 - x0) * k / 8, y + (2.5 if k % 2 else -2.5) * (0 < k < 8)) for k in range(9)])
    d.line((spring_x + 14, ys[0] - 8), (spring_x + 14, ys[-1] + 8))
    # the hooks: a hole leaves its hook upright, its crook over a griffe blade, and the griffe lifts it;
    # a solid card pushes the needle, which pushes the hook's crook off its blade, so the blade rises past it
    d.group()
    for i, x in enumerate(xs):
        up = row[i]
        rise = lift if up else 0
        foot = grate_y - rise
        yt = griffe_y - rise - 6
        eye_y = ys[i] - rise
        if up:
            d.line((x + 7, yt + 6), (x, yt), (x, foot))
        else:
            # the wire bends between its foot and the needle's eye; above the eye it is pushed back bodily
            d.line((x + 7 + push, yt + 6), (x + push, yt), (x + push, eye_y), (x, eye_y + 30), (x, foot))
    # the griffe blades, raised, and the neck cords down to the heddles and their weights
    d.group('mid')
    d.lines([[(x - 2, griffe_y - lift), (x + 11, griffe_y - lift)] for x in xs])
    for i, x in enumerate(xs):
        foot = grate_y - (lift if row[i] else 0)
        d.line((x, foot), (x, foot + 14))
        d.circle(x, foot + 18, 3.2)
        d.line((x - 3, foot + 24), (x + 3, foot + 24), (x + 3, foot + 30), (x - 3, foot + 30), closed=True)
    # labels
    d.group()
    d.text(x_mid, cy0 - 10, 'CYLINDER', size=7)
    d.text(card_x + 4, cy0 - 10, 'CARD', size=7, anchor='start')
    d.text(xs[0] - 14, griffe_y - lift - 4, 'GRIFFE', size=7, anchor='end')
    d.text(spring_x, ys[-1] + 22, 'NEEDLES', size=7)
    d.text(xs[0] - 14, grate_y - 4, 'HEDDLES', size=7, anchor='end')
    for i, x in enumerate(xs):
        d.text(x, grate_y + 46, str(row[i]), size=8)
    d.text(200, 22, 'ONE CARD, ONE PICK: A HOLE LIFTS ITS THREAD', size=8)
    return d


def difference_engine():
    """Three columns of figure wheels (table, first and second difference) set to tabulate
    n² + n + 41 at n = 4: 61, 10, 2. One turn adds the second difference into the first,
    and the first into the table: 71, 12, 2."""
    d = D()
    cols = [('TABLE', 61, 71), ('1ST DIFF.', 10, 12), ('2ND DIFF.', 2, 2)]
    xs = [96, 200, 304]
    digits = 3
    rx, ry, t = 34, 8, 16  # a figure wheel's radius, its foreshortening, and its thickness
    base, pitch = 196, 50  # the lowest wheel's top face, and the spacing between wheels
    tops = [base - pitch * k for k in range(digits)]  # units at the bottom, hundreds on top
    floor = base + t + ry + 16
    roof = tops[-1] - ry - 14
    # construction: the axes, the level of each wheel's face, the frame's floor
    d.group('thin')
    d.lines([[(x, roof - 8), (x, floor + 8)] for x in xs])
    d.lines([[(40, y + ry + t / 2), (360, y + ry + t / 2)] for y in tops])
    # the figure wheels, each a short cylinder in elevation
    d.group()
    for x in xs:
        for y in tops:
            d.ellipse(x, y, rx, ry)
            d.arc(x, y + t, rx, 0, 180, n=24, ry=ry)
            d.lines([[(x - rx, y), (x - rx, y + t)], [(x + rx, y), (x + rx, y + t)]])
    # the axes through the stacks, and the frame's top and bottom plates
    d.group('mid')
    for x in xs:
        d.line((x, roof), (x, tops[-1] - ry))
        d.line((x, base + t + ry), (x, floor))
    d.line((50, roof), (350, roof))
    d.line((50, floor), (350, floor))
    # the additions: each column is added into the one to its left
    d.group()
    y = floor + 22
    for a, b in ((xs[2], xs[1]), (xs[1], xs[0])):
        d.line((a - 10, y), (b + 10, y))
        _arrow(d, b + 10, y, math.pi)
    # labels: each wheel's digit on its front, the columns, the result of the turn
    d.group()
    for (name, now, nxt), x in zip(cols, xs):
        s = f'{now:0{digits}d}'
        for k, top in enumerate(tops):
            d.text(x, top + ry + t / 2 + 0.5, s[digits - 1 - k], size=10)
        d.text(x, roof - 14, name, size=7)
        d.text(x, floor + 50, f'THEN {nxt:0{digits}d}', size=8)
    d.text((xs[1] + xs[2]) / 2, y - 6, '+', size=9)
    d.text((xs[0] + xs[1]) / 2, y - 6, '+', size=9)
    d.text(200, 22, 'n² + n + 41 AT n = 4 · ONE TURN, BY ADDITION ALONE, GIVES n = 5', size=7)
    return d


PLATES = {'pascaline': pascaline, 'jacquard-loom': jacquard_loom, 'difference-engine': difference_engine}
