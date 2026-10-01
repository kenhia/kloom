"""feynman plates, segment "Los Alamos" and trail "The Hill" (sprint 014). See plates_for.py."""
import math
import random

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _dashed_circle(d, cx, cy, r, n=36, fill=0.55):
    """A circle drawn as n dashes, for a limit that is not a surface."""
    segs = []
    for k in range(n):
        a0 = 2 * math.pi * k / n
        a1 = a0 + 2 * math.pi * fill / n
        segs.append([(cx + r * math.cos(a0 + (a1 - a0) * i / 4), cy + r * math.sin(a0 + (a1 - a0) * i / 4))
                     for i in range(5)])
    d.lines(segs)


def _dashed_line(d, p0, p1, n=12, fill=0.55):
    segs = []
    for k in range(n):
        t0, t1 = k / n, (k + fill) / n
        segs.append([(p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t) for t in (t0, t1)])
    d.lines(segs)


# seven-segment digits, for figures drawn rather than typeset
_SEG = {
    '0': 'abcdef', '1': 'bc', '2': 'abged', '3': 'abgcd', '4': 'fgbc',
    '5': 'afgcd', '6': 'afgedc', '7': 'abc', '8': 'abcdefg', '9': 'abcdfg',
}


def _digit(d, x, y, w, h, ch):
    """A seven-segment digit with its top-left corner at (x, y)."""
    m = h / 2
    seg = {
        'a': [(x, y), (x + w, y)], 'b': [(x + w, y), (x + w, y + m)], 'c': [(x + w, y + m), (x + w, y + h)],
        'd': [(x, y + h), (x + w, y + h)], 'e': [(x, y + m), (x, y + h)], 'f': [(x, y), (x, y + m)],
        'g': [(x, y + m), (x + w, y + m)],
    }
    d.lines([seg[s] for s in _SEG[ch]])


def los_alamos():
    """A section through the Pajarito Plateau: the river, the cliffs, the finger mesas and their canyons, the Jemez behind."""
    d = D()
    base = 262
    # the ground profile, left to right: river valley, cliff, mesa fingers cut by canyons, the mountains
    prof = [(14, 236), (40, 238), (58, 240), (70, 236), (84, 228), (92, 204), (96, 170), (100, 146),
            (108, 138), (132, 134), (150, 132), (156, 150), (160, 176), (166, 178), (170, 150),
            (176, 128), (214, 124), (232, 122), (238, 142), (242, 160), (248, 161), (252, 142),
            (258, 118), (294, 112), (318, 104), (336, 86), (350, 64), (362, 48), (372, 42), (386, 46)]
    top = 124  # the mesa top where the laboratory stood: 7,300 ft
    # construction: the mesa-top level, the datum, and the beds of tuff beneath the profile
    d.group('thin')
    d.line((14, top), (386, top))
    d.line((14, base), (386, base))
    def ground(x):
        for (x0, y0), (x1, y1) in zip(prof, prof[1:]):
            if x0 <= x <= x1:
                return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return base
    # strata: level beds of tuff, cut off where the canyons and the valley have eroded them
    strata = []
    for y in range(140, base, 12):
        run = []
        for x in range(15, 386, 2):
            if ground(x) < y - 3:
                run.append((x, y))
            elif run:
                if len(run) > 1:
                    strata.append(run)
                run = []
        if len(run) > 1:
            strata.append(run)
    d.lines([[r[0], r[-1]] for r in strata])
    # the ground itself
    d.group()
    d.line(*prof)
    d.line((14, base), (14, 236))
    d.line((386, base), (386, 46))
    # detail: the river, the switchback road up the cliff, the laboratory and its fence on the mesa
    d.group('mid')
    d.lines([[(44, 238), (48, 243), (54, 238)], [(52, 238), (56, 243), (62, 238)]])
    road = [(72, 234), (90, 222), (80, 214), (93, 198), (84, 188), (96, 172), (90, 160), (100, 148), (110, 138)]
    d.line(*road)
    for bx in (184, 196, 208, 220):
        d.line((bx, 124), (bx, 116), (bx + 8, 116), (bx + 8, 124))
    d.line((186, 116), (190, 112), (194, 116))
    fence = [(178, 124), (178, 110), (230, 110), (230, 122)]
    d.line(*fence)
    d.lines([[(x - 2, 108), (x + 2, 112)] for x in range(180, 230, 8)])
    d.lines([[(x - 2, 112), (x + 2, 108)] for x in range(180, 230, 8)])
    for tx in (118, 126, 140, 268, 280, 300, 312):
        g = ground(tx)
        d.line((tx, g), (tx, g - 9))
        d.line((tx - 3, g - 4), (tx, g - 11), (tx + 3, g - 4))
    # labels
    d.group()
    d.text(46, 256, 'RIO GRANDE', size=7)
    d.text(204, 100, 'LOS ALAMOS', size=8)
    d.text(204, 146, '7,300 FT', size=7)
    d.text(160, 194, 'CANYON', size=7)
    d.text(250, 178, 'CANYON', size=7)
    d.text(352, 34, 'JEMEZ', size=7)
    d.text(200, 286, 'PAJARITO PLATEAU · SECTION · NOT TO SCALE', size=8)
    return d


def arline_death():
    """A clock whose numbers turn on drums: the drums and their carry, and the window reading 9:22."""
    d = D()
    cy = 106
    drums = [(92, 12, 44, '9'), (200, 6, 30, '2'), (290, 10, 38, '2')]  # centre x, faces, radius, digit shown
    # construction: each drum's centre lines and the rays to its faces
    d.group('thin')
    d.line((40, cy), (360, cy))
    for cx, n, r, _ in drums:
        d.line((cx, cy - r - 14), (cx, cy + r + 14))
        d.lines([[(cx, cy), (cx + r * math.cos(-math.pi / 2 + 2 * math.pi * (k + 0.5) / n),
                            cy + r * math.sin(-math.pi / 2 + 2 * math.pi * (k + 0.5) / n))] for k in range(n)])
    d.lines([[(cx, cy - r), (cx, 196)] for cx, n, r, _ in drums])
    # the drums in end view: a polygon of faces, the face uppermost read through the window
    d.group()
    for cx, n, r, _ in drums:
        pts = [(cx + r * math.cos(-math.pi / 2 + 2 * math.pi * (k + 0.5) / n),
                cy + r * math.sin(-math.pi / 2 + 2 * math.pi * (k + 0.5) / n)) for k in range(n)]
        d.line(*pts, closed=True)
        d.circle(cx, cy, 4)
    # detail: the carry pins that turn the next drum once a revolution, and the shaft
    d.group('mid')
    for (cx, n, r, _), (nx, nn, nr, _) in zip(drums, drums[1:]):
        mx = (cx + r + nx - nr) / 2
        d.circle(mx, cy + 18, 7)
        d.lines([[(mx + 7 * math.cos(2 * math.pi * k / 6), cy + 18 + 7 * math.sin(2 * math.pi * k / 6)),
                  (mx + 11 * math.cos(2 * math.pi * k / 6), cy + 18 + 11 * math.sin(2 * math.pi * k / 6))]
                 for k in range(6)])
    # the front of the case, with the window and the digits it shows
    d.group()
    d.line((50, 196), (350, 196), (350, 262), (50, 262), closed=True)
    d.line((78, 206), (322, 206), (322, 252), (78, 252), closed=True)
    for cx, n, r, ch in drums:
        _digit(d, cx - 10, 214, 20, 30, ch)
    d.circle(146, 220, 2.2)
    d.circle(146, 238, 2.2)
    # labels
    d.group()
    d.text(92, 42, 'HOURS', size=7)
    d.text(200, 42, 'TENS', size=7)
    d.text(290, 42, 'MINUTES', size=7)
    d.text(200, 284, 'A CLOCK OF TURNING NUMBERS · STOPPED AT 9:22', size=8)
    return d


def trinity():
    """Plan of the Trinity site: ground zero, the three shelters, base camp and Compania Hill, with the time sound took to reach each."""
    d = D()
    gx, gy = 238, 152
    k = 3.7  # pixels per kilometre
    c = 0.34  # the speed of sound, km/s, a round figure
    rings = [(9.14, 'S'), (16.1, 'S'), (32.2, 'S')]
    # construction: range rings and the compass cross through ground zero
    d.group('thin')
    for km, _ in rings:
        d.circle(gx, gy, km * k)
    d.line((gx - 32.2 * k - 8, gy), (gx + 32.2 * k + 8, gy))
    d.line((gx, gy - 32.2 * k - 8), (gx, gy + 32.2 * k + 8))
    ang = math.radians(225)
    d.line((gx, gy), (gx + 32.2 * k * math.cos(ang), gy + 32.2 * k * math.sin(ang)))
    # the tower and the observers' posts
    d.group()
    d.line((gx - 4, gy + 4), (gx, gy - 6), (gx + 4, gy + 4), closed=True)
    posts = {
        'N': (gx, gy - 9.14 * k), 'W': (gx - 9.14 * k, gy), 'S': (gx, gy + 9.14 * k),
    }
    for (x, y) in posts.values():
        d.line((x - 3, y - 3), (x + 3, y - 3), (x + 3, y + 3), (x - 3, y + 3), closed=True)
    bx, by = gx, gy + 16.1 * k
    d.circle(bx, by, 3.5)
    hx, hy = gx + 32.2 * k * math.cos(ang), gy + 32.2 * k * math.sin(ang)
    d.line((hx - 5, hy + 3), (hx, hy - 5), (hx + 5, hy + 3), closed=True)
    # detail: the blast front leaving ground zero, and the sight line from the hill
    d.group('mid')
    for r in (10, 16, 22):
        d.arc(gx, gy, r, -150, -30, n=24)
    d.line((hx + 6, hy + 6), (gx - 8, gy - 8))
    _arrow(d, gx - 8, gy - 8, math.atan2(gy - hy, gx - hx), 5)
    # labels: each post and the seconds its sound took
    d.group()
    d.text(gx + 8, gy + 14, 'GROUND ZERO', size=7, anchor='start')
    d.text(gx + 6, gy - 9.14 * k - 4, f'N-10,000 · {9.14 / c:.0f} S', size=7, anchor='start')
    d.text(gx + 6, gy + 9.14 * k + 4, f'S-10,000 · {9.14 / c:.0f} S', size=7, anchor='start')
    d.text(gx + 8, by + 3, f'BASE CAMP · {16.1 / c:.0f} S', size=7, anchor='start')
    d.text(hx - 2, hy - 10, f'COMPANIA HILL · {32.2 / c:.0f} S', size=7)
    d.text(gx + 32.2 * k * 0.72, gy - 32.2 * k * 0.72 - 4, '20 MI', size=7, anchor='start')
    d.text(200, 292, 'SOUND AT 340 M/S · 16 JULY 1945 · 5:29 AM', size=8)
    return d


def bethe_feynman():
    """A bare sphere at critical, at firing and at second critical, and the growth rate falling to zero as it expands."""
    d = D()
    cx, cy, s = 104, 150, 8.0  # pixels per centimetre
    rc, r0, r2 = 8.4 * s, 10.0 * s, 11.0 * s  # Lestone and Rosen's illustrative 80 kg sphere
    ox, oy, w, h = 222, 236, 150, 150  # the graph
    x0, x2 = ox + w * 0.18, ox + w * 0.86
    # construction: centre lines, the critical radius dashed, the graph's grid
    d.group('thin')
    d.line((cx - r2 - 10, cy), (cx + r2 + 10, cy))
    d.line((cx, cy - r2 - 10), (cx, cy + r2 + 10))
    _dashed_circle(d, cx, cy, rc, n=40)
    d.lines([[(ox + w * i / 6, oy), (ox + w * i / 6, oy - h)] for i in range(1, 7)])
    d.lines([[(ox, oy - h * j / 5), (ox + w, oy - h * j / 5)] for j in range(1, 6)])
    # the sphere as fired, and as it has grown when the chain reaction stops
    d.group()
    d.circle(cx, cy, r0)
    d.circle(cx, cy, r2)
    # the graph: growth rate against radius, falling in proportion to the expansion
    d.line((ox, oy), (ox + w + 6, oy))
    d.line((ox, oy), (ox, oy - h - 6))
    _arrow(d, ox + w + 6, oy, 0)
    _arrow(d, ox, oy - h - 6, -math.pi / 2)
    d.line((x0, oy - h * 0.8), (x2, oy))
    # detail: expansion arrows, the radii dimensioned, the area under the fall
    d.group('mid')
    for a in range(0, 360, 45):
        t = math.radians(a + 22.5)
        p, q = (cx + (r0 + 1) * math.cos(t), cy + (r0 + 1) * math.sin(t)), (cx + (r2 - 1) * math.cos(t), cy + (r2 - 1) * math.sin(t))
        d.line(p, q)
        _arrow(d, *q, t, 3)
    for rr, a in ((rc, 200), (r0, 160), (r2, 120)):
        t = math.radians(a)
        d.line((cx, cy), (cx + rr * math.cos(t), cy + rr * math.sin(t)))
    d.lines([[(x, oy), (x, oy - h * 0.8 * (x2 - x) / (x2 - x0))] for x in [x0 + (x2 - x0) * i / 12 for i in range(1, 12)]])
    d.line((x0, oy), (x0, oy - h * 0.8))
    # labels
    d.group()
    d.text(cx - 58, cy + 40, 'RC', size=7)
    d.text(cx - 76, cy - 18, 'R0', size=7)
    d.text(cx - 50, cy - 84, 'R2', size=7)
    d.text(x0, oy + 12, 'R0', size=7)
    d.text(x2, oy + 12, 'R2', size=7)
    d.text(ox + w + 4, oy + 12, 'R', size=7)
    d.text(ox - 8, oy - h * 0.8 + 3, 'α0', size=7, anchor='end')
    d.text(ox + 4, oy - h - 10, 'α', size=7, anchor='start')
    d.text(200, 22, 'Y ∝ M · R0² · α0² · δ     δ = R2/R0 − 1', size=8)
    d.text(cx, 272, '80 KG · 10 CM → 11 CM', size=7)
    return d


def punched_cards():
    """The machine room as a ring the decks travel round, three problems out of phase; below, an error spreading through a deck."""
    d = D()
    cx, cy, rx, ry = 200, 88, 150, 58
    machines = ['513', '075', '601', '601', '601', '405', '077']
    angs = [-90 + 360 * i / len(machines) for i in range(len(machines))]
    # construction: the ring's ellipse and the rays to each machine
    d.group('thin')
    d.ellipse(cx, cy, rx, ry)
    d.lines([[(cx, cy), (cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))] for a in angs])
    # the machines, as boxes on the ring
    d.group()
    for a in angs:
        x, y = cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))
        d.line((x - 17, y - 10), (x + 17, y - 10), (x + 17, y + 10), (x - 17, y + 10), closed=True)
    # detail: the direction of travel, and three decks between machines, each marked its own way
    d.group('mid')
    for a in angs:
        m = a + 360 / len(machines) / 2
        t = math.radians(m)
        x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
        tang = math.atan2(ry * math.cos(t), -rx * math.sin(t))
        _arrow(d, x, y, tang, 4)
    for i, a in enumerate((-90 + 360 * 0.5 / 7 + 8, -90 + 360 * 2.5 / 7 + 8, -90 + 360 * 4.5 / 7 + 8)):
        t = math.radians(a)
        x, y = cx + (rx - 26) * math.cos(t), cy + (ry - 18) * math.sin(t)
        for j in range(3):
            d.line((x - 8 + j * 1.5, y - 5 - j * 1.5), (x + 8 + j * 1.5, y - 5 - j * 1.5),
                   (x + 8 + j * 1.5, y + 5 - j * 1.5), (x - 8 + j * 1.5, y + 5 - j * 1.5), closed=True)
        if i == 1:
            d.line((x - 6, y + 3), (x + 6, y - 3))
        if i == 2:
            d.lines([[(x - 4, y), (x - 3, y)], [(x, y), (x + 1, y)], [(x + 4, y), (x + 5, y)]])
    # below: a deck of 30 cards over six cycles, an error on one card widening by a card each side per cycle
    n, bx, by, cw, ch, gap = 30, 50, 176, 10, 12, 4
    err = 21
    d.group('thin')
    for row in range(6):
        y = by + row * (ch + gap)
        d.lines([[(bx + i * cw, y), (bx + i * cw, y + ch)] for i in range(n + 1)])
        d.line((bx, y), (bx + n * cw, y))
        d.line((bx, y + ch), (bx + n * cw, y + ch))
    d.group()
    for row in range(6):
        y = by + row * (ch + gap)
        lo, hi = err - row, err + row
        d.line((bx + lo * cw, y), (bx + (hi + 1) * cw, y), (bx + (hi + 1) * cw, y + ch), (bx + lo * cw, y + ch), closed=True)
        d.lines([[(bx + i * cw + 2, y + ch - 2), (bx + i * cw + cw - 2, y + 2)] for i in range(lo, hi + 1)])
    # the small repair deck, running beside the big one
    d.group('mid')
    y = by + 5 * (ch + gap)
    d.line((bx + (err - 7) * cw, y - 3), (bx + (err + 8) * cw, y - 3))
    d.line((bx + (err - 7) * cw, y - 6), (bx + (err - 7) * cw, y))
    d.line((bx + (err + 8) * cw, y - 6), (bx + (err + 8) * cw, y))
    d.group()
    d.text(cx, cy + 3, 'ONE CYCLE = ONE TIME STEP', size=7)
    for a, m in zip(angs, machines):
        x, y = cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))
        d.text(x, y + 3, m, size=7)
    d.text(bx - 6, by + 9, '1', size=7, anchor='end')
    d.text(bx - 6, by + 5 * (ch + gap) + 9, '6', size=7, anchor='end')
    d.text(200, 294, 'AN ERROR SPREADS A CARD EACH SIDE PER CYCLE', size=8)
    return d


def oak_ridge():
    """A neutron slowed by water in a drum of solution; beside it, a store room's boxes and the wall that does not stop neutrons."""
    d = D()
    # left: a drum in section, its solution level, a neutron's path shortening as it slows
    dx0, dx1, dy0, dy1 = 30, 150, 60, 250
    level = 92
    rng = random.Random(1945)
    path = [(dx0 + 16, dy1 - 14)]
    step, ang = 46.0, -1.2
    for _ in range(13):
        ang += rng.uniform(-1.9, 1.9)
        x = path[-1][0] + step * math.cos(ang)
        y = path[-1][1] + step * math.sin(ang)
        if x < dx0 + 8 or x > dx1 - 8:
            ang = math.pi - ang
            x = path[-1][0] + step * math.cos(ang)
        if y < level + 8 or y > dy1 - 8:
            ang = -ang
            y = path[-1][1] + step * math.sin(ang)
        path.append((min(max(x, dx0 + 8), dx1 - 8), min(max(y, level + 8), dy1 - 8)))
        step *= 0.8
    # right: the plan of two rooms sharing a wall
    rx0, rx1, ry0, ry1, wall = 186, 380, 60, 250, 283
    d.group('thin')
    d.line((dx0 - 10, level), (dx1 + 10, level))
    d.lines([[(x, ry0), (x, ry1)] for x in range(rx0 + 16, rx1, 16)])
    d.lines([[(rx0, y), (rx1, y)] for y in range(ry0 + 16, ry1, 16)])
    d.group()
    d.line((dx0, dy0), (dx0, dy1), (dx1, dy1), (dx1, dy0))
    d.ellipse((dx0 + dx1) / 2, dy0, (dx1 - dx0) / 2, 8)
    d.line((rx0, ry0), (rx1, ry0), (rx1, ry1), (rx0, ry1), closed=True)
    d.line((wall, ry0), (wall, ry1))
    # the boxes: spaced out in the left room; crowded against the same wall in the right
    d.group('mid')
    for gx in range(rx0 + 12, wall - 12, 32):
        for gy in range(ry0 + 14, ry1 - 12, 32):
            d.line((gx, gy), (gx + 12, gy), (gx + 12, gy + 12), (gx, gy + 12), closed=True)
    for gx in range(wall + 4, wall + 44, 13):
        for gy in range(ry0 + 60, ry0 + 140, 13):
            d.line((gx, gy), (gx + 11, gy), (gx + 11, gy + 11), (gx, gy + 11), closed=True)
    _dashed_circle(d, wall, ry0 + 100, 52, n=32)
    d.line(*path)
    for (x, y) in path[1:]:
        d.circle(x, y, 1.6)
    ex, ey = path[-1]
    d.lines([[(ex, ey), (ex + 9 * math.cos(t), ey + 9 * math.sin(t))] for t in [2 * math.pi * k / 6 for k in range(6)]])
    # a dimension between two boxes in the safe room
    d.group('thin')
    d.line((rx0 + 24, ry0 + 36), (rx0 + 44, ry0 + 36))
    _arrow(d, rx0 + 24, ry0 + 36, math.pi, 3)
    _arrow(d, rx0 + 44, ry0 + 36, 0, 3)
    d.group()
    d.text(90, 48, 'URANIUM IN WATER', size=7)
    d.text(dx0 + 16, dy1 - 8, 'FAST', size=7, anchor='start')
    d.text(ex - 14, ey + 20, 'SLOW', size=7)
    d.text((rx0 + wall) / 2, 48, 'SPACED', size=7)
    d.text((wall + rx1) / 2, 48, 'STACKED', size=7)
    d.text(wall, ry1 + 12, 'ONE WALL', size=7)
    d.text(200, 286, 'MODERATION · SEPARATION · Y-12, 1944', size=8)
    return d


def safecracking():
    """A combination dial of 100 numbers in bands of five, and the three wheels behind it with their gates lined up under the fence."""
    d = D()
    cx, cy, r = 118, 150, 92
    # construction: the dial's centre lines and the bands of five that one try covers
    d.group('thin')
    d.line((cx - r - 12, cy), (cx + r + 12, cy))
    d.line((cx, cy - r - 12), (cx, cy + r + 12))
    d.lines([[(cx + (r - 30) * math.cos(math.radians(-90 + 3.6 * (k * 5 - 2.5))),
               cy + (r - 30) * math.sin(math.radians(-90 + 3.6 * (k * 5 - 2.5)))),
              (cx + r * math.cos(math.radians(-90 + 3.6 * (k * 5 - 2.5))),
               cy + r * math.sin(math.radians(-90 + 3.6 * (k * 5 - 2.5))))] for k in range(20)])
    # the dial: rim, a hundred graduations, the knob
    d.group()
    d.circle(cx, cy, r)
    d.circle(cx, cy, 24)
    ticks = []
    for k in range(100):
        a = math.radians(-90 + 3.6 * k)
        l = 12 if k % 10 == 0 else (8 if k % 5 == 0 else 4)
        ticks.append([(cx + r * math.cos(a), cy + r * math.sin(a)), (cx + (r - l) * math.cos(a), cy + (r - l) * math.sin(a))])
    d.lines(ticks)
    d.line((cx - 5, cy - r - 12), (cx, cy - r - 3), (cx + 5, cy - r - 12))
    # detail: the wheel pack in side view, each wheel with its gate, and the fence that drops into them
    wx, wy = 250, 70
    d.group('mid')
    for i in range(3):
        x = wx + i * 34
        d.line((x, wy), (x + 12, wy), (x + 12, wy + 160), (x, wy + 160), closed=True)
    d.line((wx - 10, wy + 80), (wx + 3 * 34 + 10, wy + 80))
    d.group()
    for i in range(3):
        x = wx + i * 34
        d.line((x - 1, wy + 8), (x + 13, wy + 8), (x + 13, wy + 20), (x - 1, wy + 20), closed=True)
    d.line((wx - 14, wy + 2), (wx + 3 * 34 + 14, wy + 2), (wx + 3 * 34 + 14, wy + 14), (wx - 14, wy + 14), closed=True)
    d.line((wx + 3 * 34 + 14, wy + 8), (wx + 3 * 34 + 34, wy + 8))
    # labels
    d.group()
    for k in range(0, 100, 10):
        a = math.radians(-90 + 3.6 * k)
        d.text(cx + (r - 22) * math.cos(a), cy + (r - 22) * math.sin(a) + 3, str(k), size=7)
    for i in range(3):
        d.text(wx + i * 34 + 6, wy + 176, str(i + 1), size=7)
    d.text(wx + 51, wy - 8, 'FENCE', size=7)
    d.text(wx + 51, wy + 196, 'WHEELS', size=7)
    d.text(200, 22, '100 ÷ 5 = 20 PER WHEEL · 20³ = 8,000', size=8)
    return d


def censorship():
    """The repeating decimal of 1/243 set round a circle in groups of three, each 111 more than the last, with the one step that carries."""
    d = D()
    cx, cy, r = 200, 150, 92
    digits = []
    rem = 1
    for _ in range(27):
        rem *= 10
        digits.append(rem // 243)
        rem %= 243
    triples = [''.join(str(x) for x in digits[i:i + 3]) for i in range(0, 27, 3)]
    n = len(triples)
    pos = [(cx + r * math.cos(math.radians(-90 + 360 * i / n)), cy + r * math.sin(math.radians(-90 + 360 * i / n)))
           for i in range(n)]
    # construction: the circle of the period and the spokes to each group
    d.group('thin')
    d.circle(cx, cy, r)
    d.lines([[(cx, cy), p] for p in pos])
    # a box for each group of three digits
    d.group()
    for x, y in pos:
        d.line((x - 20, y - 9), (x + 20, y - 9), (x + 20, y + 9), (x - 20, y + 9), closed=True)
    # detail: arrows from each group to the next; the step that differs is drawn twice
    d.group('mid')
    for i in range(n):
        a0 = -90 + 360 * i / n + 13
        a1 = -90 + 360 * (i + 1) / n - 13
        d.arc(cx, cy, r + 24, a0, a1, n=16)
        t = math.radians(a1)
        _arrow(d, cx + (r + 24) * math.cos(t), cy + (r + 24) * math.sin(t), t + math.pi / 2, 4)
        diff = (int(triples[(i + 1) % n]) - int(triples[i])) % 1000
        if diff != 111:
            d.arc(cx, cy, r + 29, a0, a1, n=16)
    # labels
    d.group()
    for (x, y), t in zip(pos, triples):
        d.text(x, y + 3, t, size=8)
    for i in range(n):
        am = math.radians(-90 + 360 * (i + 0.5) / n)
        diff = (int(triples[(i + 1) % n]) - int(triples[i])) % 1000
        d.text(cx + (r + 40) * math.cos(am), cy + (r + 40) * math.sin(am) + 3, f'+{diff}', size=7)
    d.text(cx, cy - 4, '1/243', size=9)
    d.text(cx, cy + 10, '0.004115226…', size=7)
    return d


PLATES = {
    'los-alamos': los_alamos,
    'arline-death': arline_death,
    'trinity': trinity,
    'bethe-feynman': bethe_feynman,
    'punched-cards': punched_cards,
    'oak-ridge': oak_ridge,
    'safecracking': safecracking,
    'censorship': censorship,
}
