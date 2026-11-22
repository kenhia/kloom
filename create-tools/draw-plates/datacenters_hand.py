"""Plates for The Cloud on the Ground's frames written by hand in sprint 059. See plates_for.py."""
import math
from plates import D, hatch


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def the_fight():
    """A campus at a property line, in plan: two data halls, a substation and its line, the setback,
    and the houses beyond. A schematic of the kind of site the fight is about, not any one site."""
    d = D()
    # parcel: 0..260 wide; the road along the south; houses to the east across the line
    px0, py0, px1, py1 = 24, 34, 262, 250
    line_x = 262           # the property line
    setback = 40           # the setback, in plate units
    d.group('thin')
    d.dashed((px0, py0), (px1, py0), (px1, py1), (px0, py1), (px0, py0), dash=5, gap=4)   # parcel
    d.line((line_x - setback, py0 + 10), (line_x - setback, py1 - 10))                   # setback line
    for y in (py0 + 22, py1 - 22):
        d.line((line_x - setback, y), (line_x, y))
        _arrow(d, (line_x - setback + 10, y), (line_x - setback, y), 4)
        _arrow(d, (line_x - 10, y), (line_x, y), 4)
    d.line((10, 272), (390, 272))                                                         # road edge
    d.line((10, 284), (390, 284))
    # grid for the halls: modules of 30 units
    for i in range(7):
        x = 40 + i * 30
        d.line((x, 52), (x, 58))

    d.group()
    # two data halls, each a row of modules
    for (x, y, w, h) in ((40, 60, 170, 64), (40, 150, 170, 64)):
        _box(d, x, y, w, h)
        for k in range(1, 5):
            d.line((x + k * w / 5, y), (x + k * w / 5, y + h))
    # substation, fenced, with a transmission line leaving north-west
    sx, sy = 36, 226
    _box(d, sx, sy, 46, 20)
    d.line((sx, sy + 10), (12, sy + 10), (12, 10))          # the line leaves west, then north
    for yy in (24, 74, 124, 174):
        d.line((6, yy), (18, yy))
    # houses across the property line, each a square with a pitched-roof ridge
    for (hx, hy) in ((292, 60), (334, 70), (300, 132), (346, 150), (296, 206), (340, 226)):
        _box(d, hx, hy, 26, 22)
        d.line((hx, hy + 11), (hx + 26, hy + 11))

    d.group('mid')
    # rooftop cooling units on the halls, as small circles in a row
    for (x, y) in ((40, 60), (40, 150)):
        for k in range(10):
            d.circle(x + 9 + k * 17, y + 8, 3.2)
    # generators in a row along each hall's south wall
    for (x, y) in ((40, 124), (40, 214)):
        for k in range(8):
            _box(d, x + 6 + k * 21, y + 3, 14, 6)
    # tree line along the setback
    for y in range(60, 246, 14):
        d.circle(line_x - 20, y, 5)
    hatch_poly = [(sx, sy), (sx + 46, sy), (sx + 46, sy + 20), (sx, sy + 20)]
    d.lines(hatch(hatch_poly, 5, 45))

    d.group('labels')
    d.text(125, 95, 'DATA HALL', size=7)
    d.text(125, 185, 'DATA HALL', size=7)
    d.text(sx + 23, sy + 31, 'SUBSTATION', size=7)
    d.text(16, 20, 'LINE', size=7, anchor='start')
    d.text(line_x - setback / 2, py0 + 16, 'SETBACK', size=7)
    d.text(line_x + 2, py1 + 12, 'PROPERTY LINE', size=7, anchor='start')
    d.text(330, 112, 'HOMES', size=7)
    d.text(200, 296, 'ROAD', size=7)
    return d


def inside_a_data_center():
    """A data hall in section: the cold aisle, the hot aisles, the air handler and its chilled-water
    loop to the roof, and the power chain from the grid through the UPS, with the generator beside it."""
    d = D()
    g = 252                       # ground
    fl = 232                      # raised floor
    ceil, roof = 120, 104         # return plenum ceiling, roof
    x0, x1 = 30, 286              # building walls
    racks = [(104, 124), (166, 186)]   # two rack rows, either side of the cold aisle
    d.group('thin')
    d.line((8, g), (392, g))
    for x in range(x0, x1 + 1, 16):                 # floor tiles' grid
        d.line((x, fl), (x, fl + 4))
    d.line((x0, ceil), (x1, ceil))                  # ceiling plenum
    d.line((90, 70), (330, 70))                     # datum for the roof plant

    d.group()
    d.line((x0, g), (x0, roof), (x1, roof), (x1, g))      # walls and roof
    d.line((x0, fl), (x1, fl))                            # raised floor
    for (a, b) in racks:                                  # racks, with server slots
        _box(d, a, ceil + 22, b - a, fl - ceil - 22)
        for y in range(int(ceil + 30), fl, 10):
            d.line((a + 3, y), (b - 3, y))
    _box(d, 42, 160, 30, fl - 160)                        # computer room air handler (CRAH)
    # roof: a cooling tower (or dry cooler) on the roof
    _box(d, 200, 76, 60, roof - 76)
    d.circle(230, 76, 12)
    # power: a transmission pylon, a transformer, the UPS and a generator
    d.line((358, g), (373, 150), (388, g))
    d.line((373, 150), (373, 132))
    d.line((362, 170), (384, 170)); d.line((356, 196), (390, 196))
    _box(d, 300, 206, 22, 16)                             # transformer
    _box(d, 250, 196, 26, 36)                             # UPS and batteries, inside
    _box(d, 302, 230, 40, 20)                             # generator, outside

    d.group('mid')
    # air: down the CRAH, along the floor void, up through the cold aisle's tiles, through the racks
    d.line((57, 168), (57, fl + 10), (145, fl + 10)); _arrow(d, (130, fl + 10), (145, fl + 10))
    d.line((145, fl + 10), (145, fl - 6)); _arrow(d, (145, fl + 4), (145, fl - 6))
    for y in (180, 200):
        d.line((130, y), (100, y)); _arrow(d, (110, y), (98, y))      # through the left row
        d.line((160, y), (190, y)); _arrow(d, (180, y), (192, y))     # through the right row
    d.line((92, 150), (92, ceil + 6), (60, ceil + 6), (60, 158)); _arrow(d, (60, 148), (60, 158))
    d.line((198, 150), (198, ceil + 6), (68, ceil + 6))
    # chilled-water loop from the CRAH to the roof plant
    d.dashed((46, 160), (46, 90), (205, 90), dash=4, gap=3)
    d.dashed((68, 160), (68, 96), (200, 96), dash=4, gap=3)
    # evaporation leaving the tower
    for k in (-8, 0, 8):
        d.curve(f'M{230 + k} 62 q 4 -6 0 -12 q -4 -6 0 -12')
    # power: pylon to transformer to UPS to racks; generator to the same bus
    d.line((373, 132), (373, 124), (311, 124), (311, 206))
    d.line((300, 214), (276, 214))
    d.line((250, 212), (186, 212))
    d.line((302, 240), (290, 240), (290, 214))

    d.group('labels')
    d.text(145, ceil + 16, 'COLD', size=7)
    d.text(145, ceil + 25, 'AISLE', size=7)
    d.text(88, 246, 'FLOOR VOID', size=7)
    d.text(57, 200, 'CRAH', size=7)
    d.text(230, 100, 'TOWER', size=7)
    d.text(263, 192, 'UPS', size=7)
    d.text(322, 262, 'GENERATOR', size=7)
    d.text(373, 116, 'GRID', size=7)
    d.text(160, 84, 'CHILLED WATER', size=7)
    d.text(212, 160, 'HOT', size=7)
    return d


PLATES = {'the-fight': the_fight, 'inside-a-data-center': inside_a_data_center}


def open_questions():
    """The six questions of the last frame as a sieve: six screens, each finer than the one above,
    with claims falling through. A schematic: the mesh sizes are drawn, not measured."""
    d = D()
    x0, x1 = 30, 236
    ys = [52, 88, 124, 160, 196, 232]
    labels = ['1 KIND · YEAR', '2 WHO PAID', '3 WITHDRAWN/CONSUMED', '4 PER TASK/TOTAL',
              '5 ANNOUNCED/BUILT', '6 COUNTRY/WATERSHED']
    d.group('thin')
    d.line((x0 - 16, 30), (x0 - 16, 262)); d.line((x1 + 16, 30), (x1 + 16, 262))
    for y in ys:
        d.line((x0 - 16, y), (x0, y)); d.line((x1, y), (x1 + 16, y))
    d.group()
    for i, y in enumerate(ys):                     # each screen: a frame with a mesh that tightens
        inset = i * 11
        d.line((x0 + inset, y), (x1 - inset, y))
        step = 26 - i * 3
        x = x0 + inset
        while x <= x1 - inset:
            d.line((x, y - 3), (x, y + 3)); x += step
    d.line((x0 + 66, 262), (x1 - 66, 262))           # the tray at the bottom
    d.line((x0 + 66, 262), (x0 + 66, 254)); d.line((x1 - 66, 262), (x1 - 66, 254))
    d.group('mid')
    import random
    rnd = random.Random(59)
    for i, y in enumerate(ys):                     # claims caught on each screen, fewer passing lower
        n = 7 - i
        inset = i * 11
        for k in range(n):
            cx = x0 + inset + 12 + k * (x1 - x0 - 2 * inset - 24) / max(n - 1, 1)
            d.circle(cx, y - 7, 2.2 + rnd.random() * 1.6)
    for k in range(3):                             # what passes all six
        d.circle(123 + k * 10, 256, 2.0)
    for (a, b) in ((133, 24), (133, 40)):
        d.line((a, b - 8), (a, b)); _arrow(d, (a, b - 8), (a, b), 4)
    d.group('labels')
    for y, t in zip(ys, labels):
        d.text(x1 + 22, y + 3, t, size=7, anchor='start')
    d.text(133, 16, 'CLAIMS', size=7)
    d.text(133, 280, 'WHAT BOTH SIDES CAN ARGUE FROM', size=7)
    return d


PLATES['open-questions'] = open_questions
