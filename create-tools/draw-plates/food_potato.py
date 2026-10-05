"""Plates for Daily Bread's potato trail (part `potato`, sprint 051). See plates_for.py."""
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


def _star(d, cx, cy, r, n=5, rot=-90, inner=0.45):
    """A flower of n pointed petals: a star polygon about its centre."""
    pts = []
    for i in range(2 * n):
        a = math.radians(rot + 180 * i / n)
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.line(*pts, closed=True)


def chuno():
    d = D()
    # A rectangular qullqa in section, after the descriptions of Inca storehouses: a stone house with a thatched
    # gable roof, a channel under the floor letting air in and a gap under the thatch letting it out, roots packed
    # in layers of straw, built on a windy slope. Proportions are schematic, not measured.
    # Right: a row of storehouses in plan along a contour, as they stand on the hillsides.
    gx0, gy0, gx1, gy1 = 20, 252, 270, 232                                # the slope, falling to the left
    wl, wr, floor, top, peak = 92, 232, 214, 126, 66
    cx = (wl + wr) / 2

    d.group('thin')
    d.line((gx0, gy0), (gx1, gy1))                                        # hillside
    d.line((cx, peak - 12), (cx, gy1 + 6))                                # axis
    d.line((wl - 30, floor), (wr + 30, floor))                            # floor level
    for i in range(5):                                                    # contours for the plan
        y = 60 + i * 34
        d.line((292, y + 10), (388, y - 6))

    d.group()
    d.line((wl, 238), (wl, top), (wl - 14, top + 10))                     # walls and eaves
    d.line((wr, 238), (wr, top), (wr + 14, top + 10))
    d.line((wl - 18, top + 8), (cx, peak), (wr + 18, top + 8))            # thatch, outer
    d.line((wl + 6, top - 4), (cx, peak + 12), (wr - 6, top - 4))         # thatch, inner
    d.line((wl, floor), (wr, floor))                                      # floor slabs
    d.line((wl + 10, 226), (wr - 10, 226))                                # the channel under the floor
    d.line((wl - 26, 226), (wl, 226))
    d.line((wl - 26, 236), (wr - 10, 236), (wr - 10, 226))

    d.group('mid')
    for row in range(4):                                                  # roots in layers of straw
        y = 204 - row * 18
        d.line((wl + 6, y + 7), (wr - 6, y + 7))
        for k in range(9):
            d.ellipse(wl + 14 + k * 14.5, y, 5.5, 4)
    for x in range(wl + 14, wr - 8, 16):                                  # slots in the floor
        d.line((x, floor - 1), (x, 228))

    d.group('mid')
    _arrow(d, (wl - 50, 231), (wl - 2, 231))                              # air in through the channel
    d.line((wl - 50, 231), (wl - 2, 231))
    for x in (cx - 40, cx + 40):                                          # rising through the store
        d.line((x, 222), (x, 140))
        _arrow(d, (x, 222), (x, 140))
    for sx, ex in ((wl + 2, wl - 34), (wr - 2, wr + 34)):                 # out under the thatch
        d.line((sx, top + 2), (ex, top - 14))
        _arrow(d, (sx, top + 2), (ex, top - 14))
    d.line((20, 40), (70, 40))                                            # the wind on the slope
    _arrow(d, (20, 40), (70, 40))

    d.group()
    for i in range(3):                                                    # three storehouses in plan
        x, y = 304 + i * 26, 128 - i * 4.5
        _box(d, x, y, 20, 30)
        d.line((x + 10, y), (x + 10, y + 30))                             # ridge of the roof
    d.line((296, 196), (388, 180))                                        # the road below

    d.group('mid')
    d.text(cx, 52, 'QULLQA IN SECTION (SCHEMATIC)', size=7)
    d.text(45, 33, 'WIND', size=7)
    d.text(wl - 26, 248, 'AIR IN', size=7, anchor='start')
    d.text(cx + 20, 262, 'CHANNEL UNDER THE FLOOR', size=7)
    d.text(wr + 26, 104, 'VENT UNDER', size=7)
    d.text(wr + 26, 113, 'THE THATCH', size=7)
    d.text(cx, 116, 'CHUÑO IN STRAW', size=7)
    d.text(340, 218, 'A ROW ON THE', size=7)
    d.text(340, 228, 'HILLSIDE, IN PLAN', size=7)
    d.text(342, 202, 'ROAD', size=7)
    return d


def parmentier():
    d = D()
    # The potato plant in elevation: the flower of the nightshade family, five petals joined in a star round a
    # cone of anthers; the berry, or seed ball; pinnate leaves; and below ground the stolons, underground stems
    # whose tips swell into tubers, with the seed tuber the plant grew from. Drawn schematically.
    ground, sx = 170, 170

    d.group('thin')
    d.line((20, ground), (380, ground))                                   # soil surface
    d.line((sx, 20), (sx, 285))                                           # the plant's axis
    for y in range(184, 290, 14):                                         # soil, hatched
        d.line((20, y), (34, y - 10))
        d.line((366, y), (380, y - 10))

    d.group()
    d.line((sx, ground + 40), (sx, 52))                                   # the main stem
    branches = [((sx, 120), (120, 86)), ((sx, 104), (226, 70)), ((sx, 140), (232, 120)), ((sx, 150), (112, 132))]
    for p, q in branches:
        d.line(p, q)
    d.line((sx, 52), (156, 34))                                           # flower stalks
    d.line((sx, 52), (186, 30))
    d.line((sx, 52), (172, 22))
    # below ground: stolons and tubers
    d.ellipse(sx, 222, 18, 12)                                            # the seed tuber
    tubers = [(84, 214, 26, 15), (262, 230, 30, 17), (118, 262, 22, 13), (234, 270, 20, 12)]
    for tx, ty, rx, ry in tubers:
        d.curve(f'M{sx} 206 Q{(sx + tx) / 2} {ty - 30} {tx + (rx if tx > sx else -rx) * -1:.1f} {ty}')
        d.ellipse(tx, ty, rx, ry)

    d.group('mid')
    for p, q in branches:                                                 # pinnate leaves: leaflets along each rachis
        for k in (0.45, 0.7, 0.95):
            x, y = p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k
            a = math.atan2(q[1] - p[1], q[0] - p[0])
            for side in (-1, 1):
                ox, oy = 9 * math.cos(a + side * math.pi / 2), 9 * math.sin(a + side * math.pi / 2)
                d.ellipse(x + ox, y + oy, 6, 3.5)
        d.ellipse(q[0] + 6 * math.cos(math.atan2(q[1] - p[1], q[0] - p[0])),
                  q[1] + 6 * math.sin(math.atan2(q[1] - p[1], q[0] - p[0])), 7, 4.5)
    for fx, fy in ((156, 34), (186, 30)):                                 # two flowers and a berry
        _star(d, fx, fy, 11)
        d.circle(fx, fy, 2.5)
    d.circle(172, 18, 5)
    for tx, ty, rx, ry in tubers:                                         # eyes on the tubers, in a spiral
        for k in range(3):
            a = math.radians(200 + k * 70)
            d.arc(tx + rx * 0.6 * math.cos(a), ty + ry * 0.55 * math.sin(a), 2.2, 200, 340, n=8)

    d.group('mid')
    d.text(250, 26, 'FLOWER: NIGHTSHADE FAMILY', size=7, anchor='start')
    d.text(186, 13, 'BERRY (SEED BALL)', size=7, anchor='start')
    d.text(250, 98, 'PINNATE LEAF', size=7, anchor='start')
    d.text(300, 230, 'TUBER: A SWOLLEN', size=7, anchor='start')
    d.text(300, 240, 'UNDERGROUND STEM', size=7, anchor='start')
    d.text(40, 240, 'STOLON', size=7, anchor='start')
    d.text(sx + 22, 212, 'SEED TUBER', size=7, anchor='start')
    d.text(30, 162, 'SOIL', size=7, anchor='start')
    d.text(30, 26, 'SOLANUM TUBEROSUM', size=7, anchor='start')
    return d


def potato_blight():
    d = D()
    # The asexual cycle of Phytophthora infestans, as de Bary saw it in 1861 and as it is taught now: sporangia
    # borne on branches that grow out through the stomata of the leaf's underside; in cold water a sporangium
    # splits into swimming zoospores (de Bary counted six to ten); each settles, sprouts and pierces a leaf or a
    # tuber; mycelium spreads between the cells and fruits again in about five days. Off the cycle, the sexual
    # oospore formed where A1 and A2 mating types meet. Schematic, not to scale.
    cx, cy, R = 200, 152, 98
    st = {'top': (cx, cy - R), 'right': (cx + R + 10, cy), 'bottom': (cx, cy + R), 'left': (cx - R - 38, cy)}

    d.group('thin')
    d.circle(cx, cy, R)                                                   # the cycle's track
    d.line((cx - R - 40, cy), (cx + R + 40, cy))
    d.line((cx, cy - R - 30), (cx, cy + R + 30))

    d.group()
    # top: the leaf's lower surface in section, a stoma, and a branched sporangiophore growing out through it
    tx, ty = st['top']
    d.line((tx - 46, ty + 10), (tx - 5, ty + 10))
    d.line((tx + 5, ty + 10), (tx + 46, ty + 10))
    d.line((tx - 46, ty + 22), (tx + 46, ty + 22))
    d.line((tx, ty + 22), (tx, ty - 18))
    d.line((tx, ty - 6), (tx - 14, ty - 22))
    d.line((tx, ty - 10), (tx + 14, ty - 26))
    # right: a sporangium in water, its contents split into zoospores
    rx, ry = st['right']
    d.ellipse(rx, ry, 13, 18)
    # bottom: a settled spore sprouting into a leaf or tuber surface
    bx, by = st['bottom']
    d.line((bx - 40, by + 8), (bx + 40, by + 8))
    d.circle(bx, by - 4, 6)
    d.curve(f'M{bx + 4} {by + 1} Q{bx + 10} {by + 6} {bx + 6} {by + 18}')
    # left: mycelium between the cells of the leaf
    lx, ly = st['left']
    for i in range(3):
        for j in range(3):
            _box(d, lx - 24 + i * 16, ly - 24 + j * 16, 14, 14)

    d.group('mid')
    for sx, sy in ((tx - 14, ty - 26), (tx + 14, ty - 30), (tx, ty - 23)):  # lemon-shaped sporangia
        d.ellipse(sx, sy, 4, 5.5)
    for k in range(6):                                                    # six zoospores inside
        a = math.radians(90 + 60 * k)
        d.circle(rx + 6 * math.cos(a), ry + 9 * math.sin(a), 2.2)
    for k in range(3):                                                    # three freed, with flagella
        zx, zy = rx + 30, ry - 18 + k * 18
        d.ellipse(zx, zy, 3.5, 2.5)
        d.curve(f'M{zx + 3} {zy} q4 -4 8 0 t8 0')
    d.curve(f'M{rx - 22} {ry + 30} q6 -4 12 0 t12 0 t12 0 t12 0')       # water
    d.curve(f'M{lx - 30} {ly - 18} Q{lx - 10} {ly - 6} {lx - 9} {ly + 2} T{lx + 12} {ly + 10} T{lx + 30} {ly + 22}')
    for k in range(4):                                                    # arrows round the cycle, clockwise
        a0, a1 = -80 + 90 * k, -10 + 90 * k
        d.arc(cx, cy, R, a0, a1, n=16)
        p = (cx + R * math.cos(math.radians(a1 - 4)), cy + R * math.sin(math.radians(a1 - 4)))
        q = (cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1)))
        _arrow(d, p, q)
    d.dashed((rx - 8, ry + 22), (bx + 20, by - 14), dash=4, gap=3)        # direct germination
    _arrow(d, (rx - 8, ry + 22), (bx + 20, by - 14))
    ox, oy = 340, 262                                                     # the oospore, off the cycle
    d.circle(ox, oy, 9)
    d.circle(ox, oy, 6)
    d.line((ox - 40, oy - 10), (ox - 9, oy))
    d.line((ox + 40, oy - 10), (ox + 9, oy))

    d.group('mid')
    d.text(tx + 52, ty - 18, 'SPORANGIA ON BRANCHES', size=7, anchor='start')
    d.text(tx + 52, ty - 8, 'THROUGH A STOMA', size=7, anchor='start')
    d.text(rx - 2, ry + 46, 'IN COLD WATER:', size=7, anchor='start')
    d.text(rx - 2, ry + 56, 'ZOOSPORES SWIM', size=7, anchor='start')
    d.text(bx - 46, by + 22, 'SPORE SPROUTS, PIERCES', size=7, anchor='end')
    d.text(bx - 46, by + 32, 'LEAF OR TUBER', size=7, anchor='end')
    d.text(lx, ly + 38, 'MYCELIUM', size=7)
    d.text(lx, ly + 48, 'BETWEEN CELLS', size=7)
    d.text(cx, cy - 4, 'ASEXUAL CYCLE', size=7)
    d.text(cx, cy + 7, 'ABOUT FIVE DAYS', size=7)
    d.text(262, 222, 'OR SPROUTS DIRECTLY', size=7, anchor='end')
    d.text(ox, oy + 22, 'OOSPORE: A1 × A2', size=7)
    return d


def frozen_fries():
    d = D()
    # Top: the frozen fry's process line, from Henry Chase's patent of 1949 and the industrial chain reviewed by
    # van der Sman and Schenk (2024), which adds the par-fry. Bottom left: a fry in cross-section, 10 mm square,
    # its crust and its core of starch-filled cells (schematic). Bottom right: a temperature scale with the
    # patent's figures: freezing tunnels averaging -25 F, storage at 0 F, blanching steam at 210 to 250 F,
    # finish-frying at 375 F, given here in Celsius.
    steps = ['CONDITION', 'PEEL', 'CUT', 'BLANCH', 'DRY', 'PAR-FRY', 'FREEZE', 'FRY']
    w, h, gap = 72, 20, 22
    rows = [(28, 30), (28, 82)]
    boxes = []
    for i, s in enumerate(steps):
        x0, y0 = rows[i // 4]
        x = x0 + (i % 4) * (w + gap)
        boxes.append((x, y0, s))

    d.group('thin')
    d.line((20, 120), (380, 120))                                         # divides the two halves
    d.line((70, 262), (160, 262))                                         # the fry's 10 mm, dimensioned
    d.line((70, 257), (70, 267))
    d.line((160, 257), (160, 267))
    d.line((300, 136), (300, 286))                                        # temperature axis

    d.group()
    for x, y, _ in boxes:
        _box(d, x, y, w, h)
    for (x0, y0, _), (x1, y1, _) in zip(boxes, boxes[1:]):
        if y0 == y1:
            d.line((x0 + w, y0 + h / 2), (x1, y1 + h / 2))
            _arrow(d, (x0 + w, y0 + h / 2), (x1, y1 + h / 2), size=4)
        else:                                                             # wrap to the second row
            pts = [(x0 + w / 2, y0 + h), (x0 + w / 2, 66), (x1 + w / 2, 66), (x1 + w / 2, y1)]
            d.line(*pts)
            _arrow(d, pts[-2], pts[-1], size=4)
    fx, fy, fs = 70, 160, 90                                              # the fry, 10 mm square
    _box(d, fx, fy, fs, fs)

    d.group('mid')
    _box(d, fx + 7, fy + 7, fs - 14, fs - 14)                             # the crust's inner edge
    cell = 11
    for i in range(6):                                                    # core cells, in a staggered grid
        for j in range(6):
            x = fx + 12 + i * cell + (cell / 2 if j % 2 else 0)
            y = fy + 12 + j * cell
            if x + cell * 0.8 < fx + fs - 8:
                d.ellipse(x + 4, y + 4, 4.6, 4.6)
    ticks = [(-32, 'FREEZE −32'), (-18, 'STORE −18'), (99, 'BLANCH 99–121'), (191, 'FRY 191')]

    def ty(c):
        return 280 - (c + 40) * (140 / 240)                               # -40 to 200 C over 140 units

    for c, _ in ticks:
        d.line((294, ty(c)), (306, ty(c)))
    d.line((300, ty(99)), (310, ty(99)), (310, ty(121)), (300, ty(121)))  # the blanching band
    d.line((294, ty(0)), (300, ty(0)))

    d.group('mid')
    for x, y, s in boxes:
        d.text(x + w / 2, y + h / 2 + 2.5, s, size=7)
    d.text(fx + fs / 2, fy - 8, 'A FRY IN SECTION · 10 MM', size=7)
    d.text(fx + fs + 10, fy + 6, 'CRUST', size=7, anchor='start')
    d.text(fx + fs + 10, fy + 50, 'CORE: STARCH', size=7, anchor='start')
    d.text(fx + fs + 10, fy + 60, 'IN SWOLLEN CELLS', size=7, anchor='start')
    for c, s in ticks:
        d.text(314 if c != 99 else 316, ty(c) + 3 if c != 99 else ty(110) + 3, s, size=7, anchor='start')
    d.text(290, ty(0) + 3, '0 °C', size=7, anchor='end')
    d.text(300, 296, 'DEGREES C', size=7)
    d.text(200, 113, 'HENRY CHASE, 1949 · PAR-FRY ADDED LATER', size=7)
    return d


PLATES = {'chuno': chuno, 'parmentier': parmentier, 'potato-blight': potato_blight, 'frozen-fries': frozen_fries}
