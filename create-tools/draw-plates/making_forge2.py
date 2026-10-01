"""Plates for How We Build's Metal by fire segment, part forge2 (sprint 026): wootz, the Japanese sword, Huntsman."""
import math, random
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _sword_half(u):
    """Half the thickness of a shinogi-zukuri blade, in mm, at `u` mm down from the back (30 mm wide, 7 thick)."""
    if u <= 1.6:                                   # the roof of the back (iori-mune)
        return 2.9 * u / 1.6
    if u <= 8:                                     # the flat between the back and the ridge (shinogi-ji)
        return 2.9 + 0.6 * (u - 1.6) / 6.4
    t = (u - 8) / 22                               # the face (hira), from the ridge to the edge, slightly full
    return 3.5 * (1 - t) * (1 + 0.35 * t)


def japanese_sword():
    d = D()
    s = 7.0                                        # px per mm in the section: a blade 30 mm wide and 7 mm thick
    cx, top = 86, 46                               # the section's axis and the top of its back
    W = 30
    us = [W * i / 120 for i in range(121)]
    right = [(cx + _sword_half(u) * s, top + u * s) for u in us]
    left = [(cx - _sword_half(u) * s, top + u * s) for u in us]
    outline = right + left[::-1]
    # the clay: thick (0.8 mm) over the back and flats, thinning to 0.2 mm over the edge, drawn at scale ×4
    def clay(u):
        k = min(1, max(0, (u - 17) / 6))
        return (0.8 * (1 - k) + 0.2 * k) * 4
    cr = [(cx + _sword_half(u) * s + clay(u) * s / 4 * 1.0, top + u * s) for u in us]
    cl = [(cx - _sword_half(u) * s - clay(u) * s / 4 * 1.0, top + u * s) for u in us]
    clay_out = [(cx, top - clay(0) * s / 4)] + cr + [(cx, top + W * s + clay(W) * s / 4)] + cl[::-1]
    # the core (shingane): a softer bar wrapped in the skin steel, ending well above the edge
    core = []
    for i in range(41):
        u = 2.2 + 16 * i / 40
        core.append((cx + (_sword_half(u) - 1.1) * s, top + u * s))
    core_l = [(2 * cx - x, y) for x, y in core]
    bottom = core[-1][1]
    core_path = core + [(cx, bottom + 10)] + core_l[::-1]
    # the hamon: where the edge's martensite meets the softer steel, about 7 mm in from the edge
    hy = top + 23 * s
    hx = _sword_half(23) * s

    d.group('thin')
    d.line((cx, top - 18), (cx, top + W * s + 14))                  # the section's axis
    d.line((cx - 40, top + 8 * s), (cx + 40, top + 8 * s))          # the ridge line (shinogi)
    d.line((cx - 40, hy), (cx + 40, hy))                            # the hamon's level
    # the width as a dimension line
    dx = cx - 52
    d.line((dx, top), (dx, top + W * s))
    d.lines([[(dx - 4, top), (dx + 4, top)], [(dx - 4, top + W * s), (dx + 4, top + W * s)]])

    d.group()
    d.line(*outline, closed=True)

    d.group('mid')
    d.line(*clay_out, closed=True)
    d.line(*core_path, closed=True)
    # the hardened edge, hatched below the hamon
    hatch = []
    for k in range(1, 12):
        y = hy + k * (W * s + top - hy) / 12
        w = _sword_half((y - top) / s) * s
        hatch.append([(cx - w + 1, y), (cx + w - 1, y)])
    d.lines(hatch)
    d.line((cx - hx, hy), (cx - hx / 3, hy - 3), (cx + hx / 3, hy + 2), (cx + hx, hy))

    # the blade in the water: Inoue's simulated sequence of bends, the curve exaggerated
    d.group('thin')
    x0, x1 = 196, 384
    rows = [(52, 0), (100, 1), (148, -1), (196, 0.6), (244, -1.4)]   # + bows the middle up (edge hollow), - down (true sori)
    for y, b in rows:
        d.line((x0 - 4, y - 3.5), (x1 + 4, y - 3.5))                # the chord along the straight back
    d.group()
    for y, b in rows:
        sag = 9 * b
        back, edge = [], []
        for i in range(61):
            t = i / 60
            x = x0 + (x1 - x0) * t
            off = -sag * 4 * t * (1 - t)                            # a parabola through both ends
            w = 7 if t < 0.94 else 7 * max(0.0, 1 - (t - 0.94) / 0.06) ** 0.6   # narrowing to the point
            back.append((x, y - 3.5 + off))
            edge.append((x, y - 3.5 + off + w))
        d.line(*back, *edge[::-1], closed=True)
    d.group('mid')
    # the hamon along the last blade, a gentle wave above the edge
    y, b = rows[-1]
    sag = 9 * b
    ham = []
    for i in range(55):
        t = 0.04 + 0.86 * i / 54
        x = x0 + (x1 - x0) * t
        off = -sag * 4 * t * (1 - t)
        ham.append((x, y - 3.5 + off + 4.6 + 0.8 * math.sin(t * 40)))
    d.line(*ham)
    # sori: the final curve's depth, measured from the chord
    xm = (x0 + x1) / 2
    d.line((xm, y - 3.5), (xm, y - 3.5 - sag))

    d.group('mid')
    d.text(cx, 20, 'SECTION', size=8)
    d.text(cx + 30, top + 4, 'CLAY ×4', size=8, anchor='start')
    d.text(cx + 32, top + 27 * s, 'THIN', size=8, anchor='start')
    d.text(cx, top + 12 * s, 'CORE', size=7)
    d.text(dx - 6, top + 15 * s, '30 mm', size=7, anchor='end')
    labels = ['HOT, STRAIGHT', '1 s: EDGE SHRINKS', 'MARTENSITE SWELLS', '3–4 s: BACK TURNS', 'COLD: SORI']
    for (y, b), lab in zip(rows, labels):
        d.text(x0, y - 14, lab, size=7, anchor='start')
    d.text(290, 284, 'IN THE WATER, BENDS EXAGGERATED', size=8)
    return d


PLATES = {'japanese-sword': japanese_sword}


def wootz():
    d = D()
    # left: a closed crucible in section, about 15 cm tall, with its charge and the cake it leaves
    cx, base = 82, 240
    H, R = 150, 34                                  # height and greatest half-width of the pot, px
    def half(u):                                    # an aubergine: narrow neck, full belly, round base
        return R * (0.42 + 0.58 * math.sin(math.pi * min(1, u * 1.15)) ** 0.8) if u < 0.87 else R * 0.42 * (1 - (u - 0.87) / 0.13 * 0.15)
    us = [i / 80 for i in range(81)]
    outer_r = [(cx + half(u) + 6, base - u * H) for u in us]
    outer_l = [(cx - half(u) - 6, base - u * H) for u in us]
    inner_r = [(cx + half(u), base - 6 - u * (H - 18)) for u in us]
    inner_l = [(cx - half(u), base - 6 - u * (H - 18)) for u in us]
    d.group('thin')
    d.line((cx, base + 14), (cx, base - H - 20))                # the pot's axis
    d.line((cx - 60, base), (cx + 60, base))                    # the furnace floor
    d.group()
    # the walls: outer skin closed over the base, then the bore, then the lid
    base_arc = [(cx + (half(0) + 6) * math.cos(math.radians(a)), base + 6 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    d.line(*outer_r[::-1], *base_arc, *outer_l)
    d.line(*inner_r[::-1], *inner_l)
    d.line((outer_l[-1][0] - 4, base - H), (outer_r[-1][0] + 4, base - H))       # the clay lid sealed on
    d.line((outer_l[-1][0] - 4, base - H - 7), (outer_r[-1][0] + 4, base - H - 7))
    d.group('mid')
    # the charge before melting: lumps of bloomery iron and leaves, high in the pot
    lumps = []
    for k, (x, y, r) in enumerate([(-14, 120, 7), (6, 112, 8), (15, 128, 6), (-6, 134, 6), (-18, 100, 5), (12, 96, 6)]):
        lumps.append([(cx + x + r * math.cos(math.radians(a + 20 * k)), base - y + r * 0.8 * math.sin(math.radians(a + 20 * k))) for a in range(0, 361, 45)])
    d.lines(lumps)
    d.lines([[(cx - 22 + 9 * k, base - 80 - 3 * (k % 2)), (cx - 16 + 9 * k, base - 86 + 2 * (k % 2))] for k in range(5)])
    # the cake, solidified in the bottom of the bore, with its dendrites suggested
    cake_top = base - 30
    d.line((cx - half(0.12) + 2, cake_top), (cx + half(0.12) - 2, cake_top))
    d.lines([[(cx - 16 + 8 * k, base - 8), (cx - 14 + 8 * k, cake_top + 4)] for k in range(5)])

    # right: the forging temperatures, cycle by cycle
    gx, gy, gw, gh = 176, 46, 206, 150              # the graph's box: 400 °C at the bottom, 1150 °C at the top
    T = lambda t: gy + gh * (1150 - t) / 750
    d.group('thin')
    d.line((gx, gy), (gx, gy + gh), (gx + gw, gy + gh))
    for t in (500, 750, 1000):
        d.line((gx - 3, T(t)), (gx, T(t)))
    acm = [(gx + 4 * k, T(1000)) for k in range(0, gw // 4, 2)]
    d.lines([[p, (p[0] + 4, p[1])] for p in acm])               # A_cm drawn dashed
    d.group()
    pts = [(gx, T(450)), (gx + 12, T(1080)), (gx + 22, T(1080)), (gx + 30, T(500))]  # first heat: above A_cm, all carbide dissolved
    x = gx + 30
    for k in range(7):                                          # then cycles that peak 50–100 °C below A_cm
        pts += [(x + 12, T(940)), (x + 16, T(940)), (x + 25, T(520))]
        x += 25
    d.line(*pts)
    d.group('mid')
    # carbides in section under the graph: scattered after the first heat, banded after the cycles
    for j, (bx, ordered) in enumerate(((gx + 12, False), (gx + gw - 70, True))):
        by = gy + gh + 22
        d.line((bx, by), (bx + 60, by), (bx + 60, by + 40), (bx, by + 40), closed=True)
        dots = []
        for i in range(36):
            if ordered:
                row = i % 3
                px = bx + 5 + (i // 3) * 4.6 + (row % 2) * 1.5
                py = by + 8 + row * 12 + math.sin(i * 2.3) * 1.2
            else:                                       # a fixed scatter from a small linear congruential sequence
                seed = (i * 1103515245 + 12345) % 2147483648
                px = bx + 5 + (seed % 5000) / 100
                py = by + 5 + (seed // 5000 % 3000) / 100
            dots.append([(px - 0.8, py), (px + 0.8, py)])
        d.lines(dots)
    d.group('mid')
    d.text(cx, 24, 'CRUCIBLE', size=8)
    d.text(cx + 46, base - 116, 'CHARGE', size=7, anchor='start')
    d.text(cx + 46, base - 18, 'CAKE', size=7, anchor='start')
    d.text(gx + gw, T(1000) - 5, 'Acm ≈ 1000 °C', size=7, anchor='end')
    d.text(gx - 6, T(500) + 3, '500', size=7, anchor='end')
    d.text(gx - 6, T(1000) + 3, '1000', size=7, anchor='end')
    d.text(gx + gw / 2, gy - 12, 'FORGING HEATS', size=8)
    d.text(gx + 42, gy + gh + 74, 'ERASED', size=7)
    d.text(gx + gw - 40, gy + gh + 74, 'BANDED', size=7)
    return d


PLATES['wootz'] = wootz


def huntsman_steel():
    d = D()
    floor = 92                                     # the casting-shop floor
    fx0, fx1 = 46, 150                             # the melting hole's walls
    grate = 236                                    # the fire bars, over the cellar
    d.group('thin')
    d.line((14, floor), (392, floor))
    d.line((14, grate + 30), (210, grate + 30))                        # the cellar floor
    d.line(((fx0 + fx1) / 2, floor - 40), ((fx0 + fx1) / 2, grate + 8))  # the hole's axis
    d.group()
    # the melting hole: a brick-lined box sunk below the floor, its top level with it, fire bars at the bottom
    wall = 12
    d.line((fx0 - wall, floor), (fx0 - wall, grate), (fx0, grate), (fx0, floor))
    d.line((fx1 + wall, floor), (fx1 + wall, grate), (fx1, grate), (fx1, floor))
    # the flue into the stack, out of the back wall near the top
    d.line((fx1 + wall, floor + 8), (fx1 + wall + 34, floor + 8), (fx1 + wall + 34, floor - 70))
    d.line((fx1 + wall, floor + 26), (fx1 + wall + 52, floor + 26), (fx1 + wall + 52, floor - 70))
    # the cover: a fire-brick quarry in an iron frame, with its handle
    d.line((fx0 - wall - 2, floor - 2), (fx1 + wall + 2, floor - 2))
    d.line((fx0 - wall - 2, floor - 10), (fx1 + wall + 2, floor - 10))
    d.line((fx0 - wall - 2, floor - 6), (fx0 - wall - 30, floor - 6))
    # the pot on its stand: a tapered clay crucible with a lid
    cx = (fx0 + fx1) / 2
    pb, pt = grate - 16, floor + 34                # bottom and top of the pot
    rb, rt = 20, 27
    d.line((cx - rt, pt), (cx - rb, pb), (cx + rb, pb), (cx + rt, pt))
    d.line((cx - rt - 3, pt - 4), (cx + rt + 3, pt - 4), (cx + rt + 3, pt), (cx - rt - 3, pt), closed=True)
    d.line((cx - rb + 2, pb), (cx - rb + 4, grate), (cx + rb - 4, grate), (cx + rb - 2, pb))   # the stand
    d.group('mid')
    # the fire bars, and the molten charge in the pot
    d.lines([[(fx0 + 6 + 12 * k, grate + 2), (fx0 + 6 + 12 * k, grate + 6)] for k in range(9)])
    d.line((fx0, grate + 4), (fx1, grate + 4))
    ml = pb - 34
    w = rb + (rt - rb) * (pb - ml) / (pb - pt)
    d.line((cx - w + 1, ml), (cx + w - 1, ml))
    # coke packed round the pot: small lumps
    lumps = []
    rng = random.Random(1742)                      # a fixed scatter, so the plate redraws the same
    for i in range(46):
        y = pt + 6 + rng.random() * (grate - pt - 12)
        side = -1 if i % 2 else 1
        inner = rb + (rt - rb) * (pb - y) / (pb - pt) + 4
        x = cx + side * (inner + rng.random() * (fx1 - cx - inner - 5))
        r = 2.2
        lumps.append([(x - r, y), (x, y - r), (x + r, y), (x, y + r), (x - r, y)])
    d.lines(lumps)
    # the teeming: the pot lifted out and tipped over a two-part cast-iron ingot mould
    mx, mtop, mbot = 290, 150, 262
    d.group()
    d.line((mx - 13, mtop), (mx - 13, mbot), (mx + 13, mbot), (mx + 13, mtop))
    d.line((mx - 5, mtop), (mx - 5, mbot - 4), (mx + 5, mbot - 4), (mx + 5, mtop))
    ang = math.radians(-62)                        # the pot tipped towards the mould
    def tip(x, y):
        ox, oy = mx + 34, mtop - 40
        return (ox + x * math.cos(ang) - y * math.sin(ang), oy + x * math.sin(ang) + y * math.cos(ang))
    pot = [tip(-rt, -40), tip(-rb, 40), tip(rb, 40), tip(rt, -40)]
    d.line(*pot)
    d.group('mid')
    for y in (mtop + 22, mbot - 26):                 # the rings and wedges that hold the mould's halves
        d.line((mx - 17, y), (mx + 17, y))
    lip = tip(-rt, -40)
    d.curve(f'M{lip[0]:.1f} {lip[1]:.1f} Q{mx - 2:.1f} {lip[1] + 6:.1f} {mx:.1f} {mtop + 4:.1f}')
    d.line((mx - 4, mtop + 40), (mx + 4, mtop + 40))                 # the steel rising in the mould
    # the teeming tongs, gripping the pot
    g0 = tip(0, 10)
    d.line(g0, (g0[0] + 44, g0[1] + 24))
    d.line(tip(0, -10), (g0[0] + 44, g0[1] + 16))
    d.group('mid')
    d.text(cx, floor - 18, 'COVER', size=7)
    d.text(cx, (pt + pb) / 2 + 3, 'POT', size=7)
    d.text(fx1 + wall + 43, floor - 76, 'FLUE', size=7)
    d.text(fx0 - wall - 4, grate - 40, 'COKE', size=7, anchor='end')
    d.text(cx, grate + 22, 'CELLAR', size=7)
    d.text(mx + 20, mbot - 60, 'MOULD', size=7, anchor='start')
    d.text(cx, 284, 'THE MELTING HOLE', size=8)
    d.text(mx, 284, 'TEEMING', size=8)
    return d


PLATES['huntsman-steel'] = huntsman_steel
