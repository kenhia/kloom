"""Plates for Daily Bread's part farm2 (sprint 051): catalhoyuk, maize, rice. See plates_for.py."""
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


def catalhoyuk():
    d = D()
    # A Çatalhöyük house, schematic, after the excavators' descriptions (Wikipedia's Çatalhöyük; Larsen et al.
    # 2019; Bogaard et al. 2009): entered through a roof hatch by a ladder on the south side, oven and hearth
    # under it, plastered platforms with burials beneath on the north, a storeroom with bins through a low
    # opening, neighbours wall to wall with no street, and each house rebuilt on the stumps of the one before.
    # Left: a section north to south. Right: the plan, south at the bottom. Proportions are not measured.
    floor, roof, wall = 196, 118, 7
    n0, s0 = 44, 176                                                      # inner faces of the north and south walls
    d.group('thin')
    d.line((14, floor), (206, floor))                                     # this house's floor level
    d.dashed((14, 236), (206, 236), dash=3, gap=3)                        # the older house below
    for x in (n0 - wall, s0 + wall):                                      # the older walls, under the rubble
        d.line((x, floor + 2), (x, 236))
    d.line((n0 - wall - 30, floor - 12), (n0 - wall, floor - 12))         # neighbour to the north, set higher
    d.line((s0 + wall, floor + 8), (s0 + wall + 30, floor + 8))           # neighbour to the south, set lower
    d.line((150, 60), (150, 236))                                         # the hatch's axis
    # plan: the street that is not there, construction lines through the neighbours
    d.line((226, 96), (392, 96))
    d.line((226, 204), (392, 204))
    d.line((236, 86), (236, 214))
    d.line((332, 86), (332, 214))

    d.group()
    # section: walls, roof with its hatch, floor
    d.line((n0 - wall, floor), (n0 - wall, roof - 6), (n0, roof - 6), (n0, floor))
    d.line((s0, floor), (s0, roof - 6), (s0 + wall, roof - 6), (s0 + wall, floor))
    d.line((n0, roof), (140, roof))
    d.line((n0, roof - 6), (140, roof - 6))
    d.line((160, roof), (s0, roof))
    d.line((160, roof - 6), (s0, roof - 6))
    d.line((140, roof - 6), (140, roof))
    d.line((160, roof - 6), (160, roof))
    d.line((n0 - wall - 30, roof - 12), (n0 - wall, roof - 12))           # the neighbours' roofs, stepped
    d.line((s0 + wall, roof + 6), (s0 + wall + 30, roof + 6))
    # plan: main room and storeroom, double walls
    for (x0, y0, x1, y1) in ((240, 100, 328, 200), (336, 100, 380, 150)):
        _box(d, x0, y0, x1 - x0, y1 - y0)
        _box(d, x0 - 4, y0 - 4, x1 - x0 + 8, y1 - y0 + 8)

    d.group('mid')
    # section: the ladder from the hatch to the floor
    top, foot = (156, roof - 6), (128, floor)
    for off in (0, 7):
        d.line((top[0] + off, top[1]), (foot[0] + off, foot[1]))
    for i in range(1, 8):
        t = i / 8
        x = top[0] + (foot[0] - top[0]) * t
        y = top[1] + (foot[1] - top[1]) * t
        d.line((x, y), (x + 7, y))
    d.arc(s0, floor, 14, 180, 270)                                        # the oven's dome against the south wall
    d.line((s0 - 14, floor), (s0, floor))
    d.line((100, floor), (100, floor - 3), (114, floor - 3), (114, floor))  # the hearth
    d.line((n0, floor - 10), (88, floor - 10), (88, floor))               # the north platform
    d.ellipse(66, floor + 12, 15, 6)                                      # a burial beneath it
    d.line((150, roof + 20), (150, roof - 22))                            # smoke out, people in
    _arrow(d, (150, roof + 20), (150, roof - 22))
    # plan: hatch, ladder, oven, hearth, platforms, low door, bins
    _box(d, 296, 166, 18, 16)
    d.line((300, 182), (300, 198))
    d.line((310, 182), (310, 198))
    d.arc(316, 200, 10, 180, 360)
    d.circle(278, 186, 6)
    _box(d, 244, 104, 80, 16)
    _box(d, 244, 120, 18, 44)
    d.line((328, 118), (336, 118))                                        # the low opening, through both walls
    d.line((328, 130), (336, 130))
    for i in range(3):
        _box(d, 344 + i * 11, 106, 8, 12)
    d.line((384, 74), (384, 56))
    _arrow(d, (384, 74), (384, 56), size=4)

    d.group('mid')
    d.text(150, 52, 'HATCH', size=7)
    d.text(126, 150, 'LADDER', size=7, anchor='end')
    d.text(176, 216, 'OVEN', size=7, anchor='end')
    d.text(66, 178, 'PLATFORM', size=7)
    d.text(66, 228, 'BURIAL', size=7)
    d.text(110, 250, 'OLDER HOUSE IN THE RUBBLE', size=7)
    d.text(110, 276, 'SECTION · NORTH TO SOUTH', size=7)
    d.text(358, 166, 'BINS', size=7)
    d.text(284, 228, 'NO STREET', size=7)
    d.text(310, 276, 'PLAN · SCHEMATIC', size=7)
    d.text(384, 50, 'N', size=7)
    return d


def maize():
    d = D()
    # Teosinte against maize (Hake and Ross-Ibarra 2015; Wang et al. 2005; Doebley et al. 1997). Left: a
    # teosinte ear in elevation, a chain of fruitcases in two ranks that falls apart when ripe, and one
    # fruitcase in section, its kernel shut in a cupule of the rachis by a hard glume. Right: a maize ear in
    # section, kernels naked around a cob in 16 rows, each on a small soft glume. Not to scale.
    tx, ty0, h, n = 78, 34, 17, 8
    cx, cy, rc, rk = 300, 128, 30, 78
    d.group('thin')
    d.line((tx, ty0 - 8), (tx, ty0 + n * h + 8))                        # the teosinte ear's axis
    d.line((tx - 46, 236), (tx + 46, 236))                                # the fruitcase section's axes
    d.line((tx, 196), (tx, 280))
    d.line((cx - rk - 12, cy), (cx + rk + 12, cy))                        # the maize section's axes
    d.line((cx, cy - rk - 12), (cx, cy + rk + 12))
    d.circle(cx, cy, rk)
    for i in range(16):                                                   # row centers
        a = math.radians(i * 22.5 + 11.25)
        d.line((cx + rc * math.cos(a), cy + rc * math.sin(a)), (cx + (rk + 6) * math.cos(a), cy + (rk + 6) * math.sin(a)))

    d.group()
    # teosinte ear: segments alternating left and right, each a trapezoid with its glume's face
    for i in range(n):
        y = ty0 + i * h
        s = -1 if i % 2 else 1
        w0, w1 = 9 - i * 0.4, 7 - i * 0.4
        d.line((tx - w0, y), (tx + w0, y), (tx + w1, y + h), (tx - w1, y + h), closed=True)
        d.curve(f'M{tx:.1f} {y + 2:.1f} Q{tx + s * (w0 + 5):.1f} {y + h / 2:.1f} {tx:.1f} {y + h - 2:.1f}')
    # one fruitcase in section: the cupule, a U of the rachis
    d.curve(f'M{tx - 30} 214 L{tx - 30} 256 Q{tx} 272 {tx + 30} 256 L{tx + 30} 214')
    d.curve(f'M{tx - 22} 214 L{tx - 22} 250 Q{tx} 262 {tx + 22} 250 L{tx + 22} 214')
    d.curve(f'M{tx - 30} 214 Q{tx} 192 {tx + 30} 214')                    # the hard glume, closing it
    d.curve(f'M{tx - 22} 214 Q{tx} 199 {tx + 22} 214')
    # maize: the cob and its woody ring
    d.circle(cx, cy, rc)
    d.circle(cx, cy, rc - 9)
    for i in range(16):
        a = math.radians(i * 22.5 + 11.25)
        da = math.radians(9)
        r0, r1 = rc + 4, rk - 2
        pts = [(cx + r0 * math.cos(a - da * 0.6), cy + r0 * math.sin(a - da * 0.6)),
               (cx + r1 * math.cos(a - da), cy + r1 * math.sin(a - da)),
               (cx + (r1 + 3) * math.cos(a), cy + (r1 + 3) * math.sin(a)),
               (cx + r1 * math.cos(a + da), cy + r1 * math.sin(a + da)),
               (cx + r0 * math.cos(a + da * 0.6), cy + r0 * math.sin(a + da * 0.6))]
        d.line(*pts, closed=True)

    d.group('mid')
    d.ellipse(tx, 236, 14, 17)                                            # the hidden kernel
    for i in range(n):                                                    # kernels hidden in the chain
        d.ellipse(tx, ty0 + i * h + h / 2, 3, 5)
    for i in range(16):                                                   # small soft glumes at each kernel's foot
        a = math.radians(i * 22.5 + 11.25)
        d.arc(cx + (rc + 2) * math.cos(a), cy + (rc + 2) * math.sin(a), 4, math.degrees(a) - 90, math.degrees(a) + 90, n=10)
    d.line((132, 128), (196, 128))                                        # from one to the other
    _arrow(d, (132, 128), (196, 128))

    d.group('mid')
    d.text(tx, 22, 'TEOSINTE EAR', size=7)
    d.text(tx, 292, 'ONE FRUITCASE', size=7)
    d.text(tx + 36, 204, 'HARD GLUME', size=7, anchor='start')
    d.text(tx + 36, 250, 'CUPULE', size=7, anchor='start')
    d.text(164, 120, 'TB1 · TGA1', size=7)
    d.text(cx, 30, 'MAIZE EAR IN SECTION', size=7)
    d.text(cx, cy + 3, 'COB', size=7)
    d.text(cx, cy + rk + 26, '16 ROWS · NAKED KERNELS', size=7)
    d.text(cx, 270, 'NOT TO SCALE', size=7)
    return d


def rice():
    d = D()
    # Top: a paddy field in section, schematic: an earth bund at each side, water held a few centimeters
    # deep over puddled soil, seedlings set out in rows, water let in from a channel and drained before
    # harvest (Wikipedia, Rice and Paddy field; Zong et al. 2007 on bunding at Kuahuqiao).
    # Bottom: two rice spikelet bases, enlarged (Zheng et al. 2016; Fuller et al. 2009): the wild one parts at
    # an abscission layer and leaves a smooth round scar; the domesticated one is torn off its stalk.
    soil, water = 128, 116
    d.group('thin')
    d.line((14, soil), (386, soil))                                       # the field's floor
    d.line((14, 150), (386, 150))                                         # the plow pan below
    d.line((200, 184), (200, 292))                                        # between the two bases
    for cx in (110, 290):
        d.line((cx, 186), (cx, 256))

    d.group()
    # the bunds, trapezoids of earth; the channel outside the left one
    d.line((14, 96), (34, 96), (54, soil), (14, soil))
    d.line((386, 96), (366, 96), (346, soil), (386, soil))
    # spikelets: a husk on its base
    for cx in (110, 290):
        d.curve(f'M{cx - 14} 236 C{cx - 22} 210 {cx - 10} 196 {cx} 188 C{cx + 10} 196 {cx + 22} 210 {cx + 14} 236 Z')
        d.line((cx - 14, 236), (cx + 14, 236))

    d.group('mid')
    d.line((54 + (water - soil) * 0, water), (346, water))                # the water's surface
    d.dashed((40, 143), (360, 143), dash=4, gap=3)                        # drained, below the surface
    for x in range(72, 340, 18):                                          # seedlings in rows
        d.line((x, soil), (x - 4, 94))
        d.line((x, soil), (x, 90))
        d.line((x, soil), (x + 4, 94))
    d.line((336, water), (336, soil))                                     # the depth
    _arrow(d, (336, soil), (336, water), size=3)
    _arrow(d, (336, water), (336, soil), size=3)
    d.line((2, 100), (24, 108))                                           # water in
    _arrow(d, (2, 100), (24, 108), size=4)
    # wild: smooth scar, a clean disc at the base
    d.ellipse(110, 244, 12, 4)
    d.ellipse(110, 244, 4, 1.5)
    # domesticated: a ragged break and a stub of stalk
    pts = [(276 + i * 2.8, 244 + (3 if i % 2 else -2)) for i in range(11)]
    d.line((276, 236), *pts, (304, 236))
    d.line((286, 246), (288, 268), (292, 268), (294, 246))

    d.group('mid')
    d.text(34, 84, 'BUND', size=7)
    d.text(372, 84, 'BUND', size=7)
    d.text(336, 78, 'A FEW CM', size=7, anchor='end')
    d.text(200, 162, 'DRAINED BEFORE HARVEST', size=7)
    d.text(110, 266, 'SMOOTH SCAR', size=7)
    d.text(110, 280, 'WILD · SHATTERS', size=7)
    d.text(290, 280, 'TORN · DOMESTICATED', size=7)
    d.text(200, 30, 'A PADDY FIELD IN SECTION · SCHEMATIC', size=7)
    d.text(200, 178, 'SPIKELET BASES', size=7)
    return d


PLATES = {'catalhoyuk': catalhoyuk, 'maize': maize, 'rice': rice}
