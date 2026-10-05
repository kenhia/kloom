"""Plates for Daily Bread's part table1 (sprint 051): the first restaurants, Fannie Farmer's level
measures and Escoffier's kitchen brigade. See plates_for.py."""
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


def _chair(d, x, y, r=3.2):
    d.circle(x, y, r)


def restaurant():
    d = D()
    # Two dining rooms in plan, drawn to one scale (a schematic, not a survey of any one house).
    # Left: the table d'hote of an inn or a traiteur, one long table laid for everyone at one hour.
    # Right: a restaurant of the 1780s as Diderot, Brillat-Savarin and Blagdon describe it: small
    # separate tables, the counter where the bill is paid by the door, and the kitchen behind a pass.
    lx0, lx1, rx0, rx1, y0, y1 = 18, 186, 214, 382, 46, 236

    d.group('thin')
    for x in range(lx0, lx1 + 1, 24):                                     # floor grid, 24-unit squares
        d.line((x, y0), (x, y1))
    for x in range(rx0, rx1 + 1, 24):
        d.line((x, y0), (x, y1))
    for y in range(y0 + 22, y1, 24):
        d.line((lx0, y), (lx1, y))
        d.line((rx0, y), (rx1, y))

    d.group()
    _box(d, lx0, y0, lx1 - lx0, y1 - y0)                                  # the two rooms
    _box(d, rx0, y0, rx1 - rx0, y1 - y0)
    d.line((rx0, 88), (rx0 + 64, 88))                                     # kitchen wall, with the pass
    d.line((rx0 + 104, 88), (rx1, 88))

    d.group('mid')
    # the long table: one board, sixteen places, the host at its head
    tx0, tx1, ty0, ty1 = 52, 152, 128, 148
    _box(d, tx0, ty0, tx1 - tx0, ty1 - ty0)
    for i in range(8):
        x = tx0 + 7 + i * (tx1 - tx0 - 14) / 7
        _chair(d, x, ty0 - 7)
        _chair(d, x, ty1 + 7)
    _chair(d, tx0 - 8, (ty0 + ty1) / 2, 4.2)                              # the host
    # the restaurant: six small tables for two, a cabinet, the counter
    for i, (cx, cy) in enumerate([(244, 124), (290, 124), (336, 124), (244, 176), (290, 176), (336, 176)]):
        d.circle(cx, cy, 8)
        _chair(d, cx - 13, cy)
        _chair(d, cx + 13, cy)
    _box(d, 352, 200, 26, 30)                                             # the counter by the door
    d.line((360, 92), (360, 112), (378, 112))                             # a cabinet's partition
    # the kitchen: the range along the back wall
    _box(d, rx0 + 10, y0 + 8, 92, 18)
    for i in range(4):
        d.circle(rx0 + 22 + i * 23, y0 + 17, 6)

    d.group('mid')
    # service: from the pass to two tables and back to the counter
    pass_pt = (rx0 + 84, 92)
    for tgt in [(290, 113), (336, 165)]:
        d.line(pass_pt, tgt)
        _arrow(d, pass_pt, tgt, 4)
    d.line((300, 186), (348, 214))
    _arrow(d, (300, 186), (348, 214), 4)

    d.group('mid')
    d.text((lx0 + lx1) / 2, 34, "TABLE D'HOTE", size=7)
    d.text((rx0 + rx1) / 2, 34, 'RESTAURANT', size=7)
    d.text((lx0 + lx1) / 2, 104, 'ONE TABLE', size=7)
    d.text((lx0 + lx1) / 2, 186, 'ONE HOUR · ONE DISH', size=7)
    d.text(rx0 + 10, 82, 'KITCHEN', size=7, anchor='start')
    d.text(rx0 + 84, 82, 'PASS', size=7)
    d.text(365, 196, 'COUNTER', size=7, anchor='middle')
    d.text(356, 101, 'CABINET', size=7, anchor='end')
    d.text(rx0 + 6, 153, 'ANY HOUR · THE CARTE', size=7, anchor='start')
    d.text(200, 262, 'TWO ROOMS IN PLAN · SCHEMATIC', size=7)
    d.text(200, 276, 'A SEAT AT A COMMON BOARD, OR A TABLE OF ONE\'S OWN', size=7)
    return d


def fannie_farmer():
    d = D()
    # Left: a tin half-pint measuring cup in elevation, divided in quarters on one side and thirds on the
    # other (Farmer 1896, p. 27), with a heaped cupful struck level by a case knife drawn across the rim.
    # Right: two tablespoons in section. Mrs. Lincoln's (1884) spoonful is "rounded over, or convex in the
    # same proportion as the spoon is concave"; Farmer's is level. The heap is the bowl reflected about the
    # rim, so the rounded spoonful holds twice the level one (our geometry, not a measurement).
    cx, rim, base, r_top, r_bot = 132, 92, 236, 50, 44                   # cup: 100 wide at the rim, 144 deep
    q = [base - (base - rim) * k / 4 for k in (1, 2, 3)]
    t = [base - (base - rim) * k / 3 for k in (1, 2)]
    d.group('thin')
    d.line((40, rim), (392, rim))                                         # the level line through the rim
    d.line((cx, 50), (cx, 250))                                           # the cup's axis
    for y in q:                                                           # quarter marks, carried out
        d.line((cx + r_top + 30, y), (cx + r_top + 42, y))
    for y in t:                                                           # third marks
        d.line((cx - r_top - 26, y), (cx - r_bot - 6, y))
    d.line((264, 206), (394, 206))                                        # the spoons' rim line

    d.group()
    # the cup: a slightly tapered tin cylinder with a rolled rim and a strap handle
    d.line((cx - r_top, rim), (cx - r_bot, base), (cx + r_bot, base), (cx + r_top, rim))
    d.arc(cx, rim, r_top, 180, 360, ry=6)
    d.arc(cx, rim, r_top, 0, 180, ry=6)
    d.arc(cx, base, r_bot, 0, 180, ry=5)
    hx = cx + r_top - 2
    d.line((hx, rim + 18), (hx + 22, rim + 22), (hx + 26, rim + 60), (hx - 3, rim + 78))
    # the knife, its blade laid across the rim, its handle off to the left
    d.line((cx - 62, rim - 2), (cx + 64, rim - 2), (cx + 70, rim + 1), (cx - 62, rim + 2), closed=True)
    d.line((cx - 62, rim - 3), (cx - 92, rim - 3), (cx - 92, rim + 3), (cx - 62, rim + 3))

    d.group('mid')
    for y in q:                                                           # graduations on the tin
        d.line((cx + 10, y), (cx + 30, y))
    for y in t:
        d.line((cx - 30, y), (cx - 10, y))
    # the heap above the rim, struck off: drawn dashed, as it was before the knife passed
    heap = [(cx - r_top + 2 + i * (2 * r_top - 4) / 24,
             rim - 3 - 22 * math.sin(math.pi * i / 24)) for i in range(25)]
    d.dashed(*heap, dash=3, gap=2.5)
    d.line((cx - 62, rim - 14), (cx - 34, rim - 14))
    _arrow(d, (cx - 62, rim - 14), (cx - 34, rim - 14), 4)

    d.group()
    # two tablespoon bowls in section: half-ellipses below the rim line, handles rising outward
    d.arc(300, 206, 20, 0, 180, ry=9)
    d.line((280, 206), (272, 203), (264, 199))
    d.arc(358, 206, 20, 0, 180, ry=9)
    d.line((378, 206), (386, 203), (394, 199))
    d.group('mid')
    d.arc(300, 206, 20, 180, 360, ry=9)                                  # Lincoln: the heap mirrors the bowl
    d.line((338, 206), (378, 206))                                        # Farmer: struck level

    d.group('mid')
    d.text(cx, 40, 'HALF-PINT CUP', size=7)
    for y, s in zip(q, ('1/4', '1/2', '3/4')):
        d.text(cx + r_top + 46, y + 3, s, size=7, anchor='start')
    for y, s in zip(t, ('1/3', '2/3')):
        d.text(cx - r_top - 30, y + 3, s, size=7, anchor='end')
    d.text(cx - 77, rim + 16, 'CASE KNIFE', size=7)
    d.text(300, 234, 'ROUNDED', size=7)
    d.text(300, 246, '1884', size=7)
    d.text(358, 234, 'LEVEL', size=7)
    d.text(358, 246, '1896', size=7)
    d.text(329, 180, 'TABLESPOONS', size=7)
    d.text(200, 272, 'A CUPFUL IS MEASURED LEVEL', size=7)
    return d


def escoffier():
    d = D()
    # The brigade as Escoffier organized it, after Mennell's five parties (cited by Mac Con Iomaire 2009),
    # with the order's path: from the dining room to the aboyeur at the pass, called to each partie, the
    # parts sent back to the pass, checked by the chef and carried to the table. An organization chart.
    parties = ['GARDE-MANGER', 'ENTREMETIER', 'ROTISSEUR', 'SAUCIER', 'PATISSIER']
    bw, gap, x0, py = 68, 7, 13, 132
    xs = [x0 + i * (bw + gap) for i in range(5)]
    mids = [x + bw / 2 for x in xs]

    d.group('thin')
    for y in (32, 66, py, py + 26, 212, 232):                             # the ranks, along the boxes' edges
        d.line((6, y), (394, y))

    d.group()
    _box(d, 160, 32, 80, 22)                                              # chef
    _box(d, 166, 66, 68, 18)                                              # sous-chef
    for x in xs:
        _box(d, x, py, bw, 26)
    _box(d, 30, 212, 340, 20)                                             # the pass, a long hot counter

    d.group('mid')
    d.line((200, 54), (200, 66))                                          # chef to sous-chef
    d.line((200, 84), (200, 104))
    d.line((mids[0], 104), (mids[-1], 104))                               # sous-chef to the five parties
    for m in mids:
        d.line((m, 104), (m, py))

    d.group('mid')
    # the order: in from the dining room, called up to each partie (dashed), the parts sent down
    d.line((392, 252), (330, 236))
    _arrow(d, (392, 252), (330, 236), 4)
    for m in mids:
        d.dashed((m - 6, 212), (m - 6, py + 28), dash=3, gap=2.5)
        _arrow(d, (m - 6, 190), (m - 6, py + 28), 3.5)
        d.line((m + 6, py + 28), (m + 6, 212))
        _arrow(d, (m + 6, py + 28), (m + 6, 212), 3.5)
    d.line((70, 236), (8, 252))
    _arrow(d, (70, 236), (8, 252), 4)

    d.group('mid')
    d.text(200, 46, 'CHEF', size=7)
    d.text(200, 78, 'SOUS-CHEF', size=7)
    for m, p in zip(mids, parties):
        d.text(m, py + 16, p, size=7)
    d.text(200, 225, 'THE PASS · ABOYEUR CALLS THE ORDER', size=7)
    d.text(392, 266, 'ORDER IN', size=7, anchor='end')
    d.text(8, 266, 'TO THE TABLE', size=7, anchor='start')
    d.text(mids[0] - 10, 184, 'CALLED', size=7, anchor='end')
    d.text(mids[-1] + 11, 184, 'SENT', size=7, anchor='start')
    d.text(200, 22, 'THE BRIGADE DE CUISINE', size=7)
    return d


PLATES = {'restaurant': restaurant, 'fannie-farmer': fannie_farmer, 'escoffier': escoffier}
