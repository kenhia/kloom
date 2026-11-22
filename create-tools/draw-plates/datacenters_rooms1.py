"""Plates for The Cloud on the Ground's part rooms1 (sprint 059): ENIAC's room, a SAGE direction
center, and the mainframe machine room. See plates_for.py."""
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


def eniac_room():
    """ENIAC in plan: forty panels in a U (16, 8 and 16, in the order Wikipedia gives from the
    1946 report), each about 2 ft wide and 1 ft deep, in a room of 30 by 50 ft, with the air
    drawn off the tops of the panels to blowers and out, and the power fed from the separate
    power panels along a trough at the panels' feet. Drawn to scale as a schematic: where the
    blowers and power panels stood is not recorded here."""
    d = D()
    s = 6.2                                   # plate units per foot
    rx0, ry0 = 40, 56                         # room's corner
    rw, rh = 50 * s, 30 * s                   # 50 by 30 feet
    pw, pd = 2 * s, 1 * s                     # a panel: 2 ft wide, 1 ft deep
    bx = rx0 + 3 * s                          # back row's outer face, 3 ft off the wall
    top = ry0 + 7 * s                         # top row's outer face
    inner_w = 8 * pw                          # the back row's 8 panels
    bot = top + pd + inner_w                  # bottom row's inner face
    side_x0 = bx + pd                         # the side rows start inside the back row
    side_x1 = side_x0 + 16 * pw               # 16 panels each

    d.group('thin')
    # a 5 ft grid on the floor
    for k in range(1, 10):
        x = rx0 + k * 5 * s
        d.line((x, ry0 + rh - 3), (x, ry0 + rh + 3))
    for k in range(1, 6):
        y = ry0 + k * 5 * s
        d.line((rx0 - 3, y), (rx0 + 3, y))
    # dimension lines
    d.line((rx0, ry0 + rh + 14), (rx0 + rw, ry0 + rh + 14))
    for x in (rx0, rx0 + rw):
        d.line((x, ry0 + rh + 10), (x, ry0 + rh + 18))
    d.line((rx0 + rw + 12, ry0), (rx0 + rw + 12, ry0 + rh))
    for y in (ry0, ry0 + rh):
        d.line((rx0 + rw + 8, y), (rx0 + rw + 16, y))

    d.group()
    _box(d, rx0, ry0, rw, rh)                                     # the room
    # the U of panels, with a tick between panels
    _box(d, bx, top, pd, pd + inner_w + pd)                      # back row (with corners)
    for k in range(1, 8):
        y = top + pd + k * pw
        d.line((bx, y), (bx + pd, y))
    _box(d, side_x0, top, side_x1 - side_x0, pd)                  # top row
    _box(d, side_x0, bot, side_x1 - side_x0, pd)                  # bottom row
    for k in range(1, 16):
        x = side_x0 + k * pw
        d.line((x, top), (x, top + pd))
        d.line((x, bot), (x, bot + pd))
    # three function tables on wheels inside the U
    for k in range(3):
        _box(d, side_x0 + 30 + k * 46, top + pd + 30 + (k % 2) * 16, 22, 10)
    # power equipment, apart from the machine: seven panels in a row
    px, py = rx0 + 34 * s, ry0 + rh - 3 * s
    _box(d, px, py, 7 * pw * 0.8, pd)
    for k in range(1, 7):
        d.line((px + k * pw * 0.8, py), (px + k * pw * 0.8, py + pd))
    # blowers: two drums against the far wall
    for (cx, cy) in ((rx0 + rw - 16, top + 6), (rx0 + rw - 16, bot - 6)):
        d.circle(cx, cy, 8)

    d.group('mid')
    # air: from inside the U through the panels to ducts along their tops (dashed), then to the blowers
    for y0, y1 in ((top + pd + 14, top - 2), (bot - 14, bot + pd + 2)):
        for x in (side_x0 + 3 * pw, side_x0 + 8 * pw, side_x0 + 13 * pw):
            d.line((x, y0), (x, y1))
            _arrow(d, (x, y0), (x, y1), 4)
    d.dashed((bx - 4, top - 5), (side_x1 + 4, top - 5), (rx0 + rw - 24, top - 5), (rx0 + rw - 24, top + 6), dash=4, gap=3)
    d.dashed((bx - 4, bot + pd + 5), (side_x1 + 4, bot + pd + 5), (rx0 + rw - 24, bot + pd + 5), (rx0 + rw - 24, bot - 6), dash=4, gap=3)
    d.dashed((bx - 4, top - 5), (bx - 4, bot + pd + 5), dash=4, gap=3)
    # out through the wall
    for cy in (top + 6, bot - 6):
        d.line((rx0 + rw - 8, cy), (rx0 + rw + 6, cy))
        _arrow(d, (rx0 + rw - 8, cy), (rx0 + rw + 6, cy), 4)
    # the power trough along the panels' inner feet, fed from the power panels
    tx0, tx1 = side_x0 + 3, side_x1 - 3
    d.line((px + 2.8 * pw, py), (px + 2.8 * pw, bot + pd + 12), (tx1, bot + pd + 12))
    d.line((tx1, bot - 3), (tx0, bot - 3), (bx + pd + 3, bot - 3), (bx + pd + 3, top + pd + 3), (tx1, top + pd + 3))
    d.line((tx1, bot + pd + 12), (tx1 + 6, bot + pd + 12), (tx1 + 6, bot - 3), (tx1, bot - 3))

    d.group('labels')
    d.text(rx0 + rw / 2, ry0 + rh + 26, '50 FT', size=7)
    d.text(rx0 + rw + 22, ry0 + rh / 2 + 3, '30 FT', size=7, anchor='start')
    d.text((side_x0 + side_x1) / 2, top - 11, '16 PANELS · DUCTS ON TOP', size=7)
    d.text(bx + pd + 6, (top + bot) / 2 + 3, '8 PANELS', size=7, anchor='start')
    d.text((side_x0 + side_x1) / 2, top + pd + 82, 'FUNCTION TABLES', size=7)
    d.text(px + 7 * pw * 0.4, py + pd + 10, 'POWER SUPPLIES', size=7)
    d.text(rx0 + rw - 16, ry0 + rh / 2 + 3, 'BLOWERS', size=7)
    d.text(tx1 - 40, bot - 7, 'POWER TROUGH', size=7)
    d.text(rx0, 30, 'ENIAC IN PLAN · SCHEMATIC', size=7, anchor='start')
    return d


def sage_blockhouse():
    """A SAGE direction center in section, to the widths in IBM's 1959 manual: the blockhouse
    150 ft square and four stories, joined by a 22 ft bay to the one-story power and
    air-conditioning building, 110 ft square and about 21 ft high, with the cooling tower and
    buried fuel tank the manual's site drawing shows beside it. Heights are drawn at about twice
    the horizontal scale, with a schematic 17 ft storey."""
    d = D()
    s = 1.12                         # plate units per foot, across
    v = 2.4                          # plate units per foot, up
    g = 236                          # ground
    x0 = 18
    dc_w, bay_w, pb_w = 150 * s, 22 * s, 110 * s
    fl = 17 * v                      # a schematic 17 ft storey
    dc_x1 = x0 + dc_w
    pb_x0 = dc_x1 + bay_w
    pb_x1 = pb_x0 + pb_w
    pb_top = g - 21 * v
    top = g - 4 * fl
    wall = 4

    def floor_top(k):                # the k-th floor's ceiling line, k = 1 at the bottom
        return g - k * fl

    d.group('thin')
    d.line((6, g), (394, g))
    for k in range(1, 4):
        y = floor_top(k)
        d.line((x0 - 10, y), (x0 - 4, y))
    dim = g + 28
    d.line((x0, dim), (dc_x1, dim))
    for x in (x0, dc_x1):
        d.line((x, dim - 4), (x, dim + 4))
    d.line((pb_x0, dim), (pb_x1, dim))
    for x in (pb_x0, pb_x1):
        d.line((x, dim - 4), (x, dim + 4))
    d.lines(hatch([(6, g), (394, g), (394, g + 8), (6, g + 8)], 6, 45))

    d.group()
    d.line((x0, g), (x0, top), (dc_x1, top), (dc_x1, g))
    d.line((x0 + wall, g), (x0 + wall, top + wall), (dc_x1 - wall, top + wall), (dc_x1 - wall, g))
    for k in range(1, 4):
        y = floor_top(k)
        d.line((x0 + wall, y), (dc_x1 - wall, y))
    d.line((dc_x1, g - 14 * v), (pb_x0, g - 14 * v))                 # the bay's roof
    d.line((pb_x0, g), (pb_x0, pb_top), (pb_x1, pb_top), (pb_x1, g))
    tx = pb_x1 + 8
    d.line((tx, g), (tx + 4, g - 44), (tx + 24, g - 44), (tx + 28, g))  # cooling tower
    d.ellipse(pb_x0 + 34, g + 16, 16, 4.5)                             # fuel tank, buried

    d.group('mid')
    # the duplex computers on the second floor: two rows of cabinets, A and B
    y2 = floor_top(2)
    for k in range(5):
        _box(d, x0 + 12 + k * 14, y2 + 16, 10, fl - 18)
        _box(d, x0 + 94 + k * 14, y2 + 16, 10, fl - 18)
    # air handlers on the first floor, with air rising to the computers
    for k in range(3):
        ax = x0 + 22 + k * 50
        _box(d, ax, g - 22, 28, 20)
        d.line((ax + 14, g - 22), (ax + 14, floor_top(1) - 4))
        _arrow(d, (ax + 14, g - 22), (ax + 14, floor_top(1) - 4), 4)
    # consoles on the floors above
    for k in range(7):
        cx = x0 + 16 + k * 21
        _box(d, cx, floor_top(2) - 12, 9, 10)
        _box(d, cx + 4, floor_top(3) - 12, 9, 10)
    # generators and a chiller in the power building
    for k in range(3):
        d.circle(pb_x0 + 16 + k * 22, g - 14, 8)
    _box(d, pb_x0 + 80, g - 26, 30, 22)
    # power across the bay to the computers
    d.line((pb_x0 + 16, g - 22), (pb_x0 + 16, g - 40), (dc_x1 - 10, g - 40), (dc_x1 - 10, y2 + 24))
    # chilled water to the air handlers
    d.dashed((pb_x0 + 95, g - 4), (dc_x1 - 18, g - 4), (dc_x1 - 18, g - 12), (x0 + 22 + 2 * 50 + 28, g - 12), dash=4, gap=3)
    # condenser water to the tower, and its plume
    d.dashed((pb_x0 + 104, g - 26), (pb_x0 + 104, pb_top - 8), (tx + 14, pb_top - 8), (tx + 14, g - 44), dash=4, gap=3)
    for k in (-6, 0, 6):
        d.curve(f'M{tx + 14 + k} {g - 48} q 3 -5 0 -10 q -3 -5 0 -10')

    d.group('labels')
    cx = x0 + dc_w / 2
    d.text(cx, floor_top(4) + 10, 'OPERATIONS', size=7)
    d.text(cx, floor_top(3) + 10, 'OPERATIONS', size=7)
    d.text(cx, floor_top(2) + 10, 'COMPUTERS A AND B', size=7)
    d.text(cx, floor_top(1) + 10, 'AIR HANDLERS', size=7)
    d.text(x0 + dc_w / 2, dim + 12, '150 FT', size=7)
    d.text((pb_x0 + pb_x1) / 2, dim + 12, '110 FT', size=7)
    d.text((pb_x0 + pb_x1) / 2, pb_top - 16, 'POWER AND AIR', size=7)
    d.text(tx + 14, g - 80, 'TOWER', size=7)
    d.text(x0, top - 10, 'DIRECTION CENTER IN SECTION · HEIGHTS SCHEMATIC', size=7, anchor='start')
    return d


def machine_room():
    """A mainframe machine room in section, after IBM's System/360 planning manual: a raised
    floor 12 in above the slab, the air conditioner pushing cooled air into the void, out
    through perimeter registers and the cable holes under each machine, and back through
    ceiling registers above them; beside it, a thermal conduction module of the IBM 3081
    in section (chips, pistons, helium-filled cap, water-cooled cold plate) and its water loop
    to a coolant distribution unit and the building's water."""
    d = D()
    slab, fl, ceil = 250, 222, 120     # the building's slab, the raised floor, the ceiling
    x0, x1 = 16, 238                   # the room's walls

    d.group('thin')
    d.line((6, slab), (250, slab))
    for x in range(x0 + 12, x1, 14):                 # pedestals under the floor
        d.line((x, fl + 3), (x, slab))
    d.line((x1 + 8, fl), (x1 + 8, slab))              # the floor's height, dimensioned
    d.line((x1 + 4, fl), (x1 + 12, fl))
    d.line((x1 + 4, slab), (x1 + 12, slab))
    # module's construction: centre lines of the chips
    for k in range(5):
        cx = 278 + k * 22
        d.line((cx, 84), (cx, 156))

    d.group()
    d.line((x0, slab), (x0, ceil - 16), (x1, ceil - 16), (x1, slab))   # walls and roof
    d.line((x0, ceil), (x1, ceil))                                      # ceiling
    d.line((x0, fl), (x1, fl))                                           # raised floor
    d.line((x0, fl + 3), (x1, fl + 3))
    # air conditioner against the left wall, standing on the floor
    _box(d, x0 + 6, fl - 62, 30, 62)
    # two machine frames and a console
    for (mx, mw, mh) in ((92, 44, 70), (156, 44, 70)):
        _box(d, mx, fl - mh, mw, mh)
    _box(d, 210, fl - 26, 22, 26)
    # the thermal conduction module, in section: substrate, chips, pistons, cap, cold plate
    mx0, mx1 = 264, 380
    _box(d, mx0, 140, mx1 - mx0, 12)                       # ceramic substrate
    for k in range(5):
        cx = 278 + k * 22
        _box(d, cx - 6, 134, 12, 6)                         # a chip
        d.line((cx, 134), (cx, 104))                        # the piston's rod
        _box(d, cx - 4, 116, 8, 18)                         # the piston
    d.line((mx0, 140), (mx0, 100), (mx1, 100), (mx1, 140))  # the cap
    _box(d, mx0, 80, mx1 - mx0, 20)                         # the cold plate
    # the coolant distribution unit below
    _box(d, 300, 200, 50, 34)

    d.group('mid')
    # air: down the conditioner, along the void, up at the perimeter and through cable holes
    d.line((x0 + 21, fl - 6), (x0 + 21, fl + 14), (220, fl + 14))
    _arrow(d, (200, fl + 14), (220, fl + 14))
    for x in (114, 178):
        d.line((x, fl + 14), (x, fl - 10))
        _arrow(d, (x, fl + 2), (x, fl - 10), 4)
    d.line((228, fl + 14), (228, fl - 12))
    _arrow(d, (228, fl), (228, fl - 12), 4)
    # warm air up out of the frames, to ceiling registers, back to the conditioner
    for x in (114, 178):
        d.line((x, fl - 74), (x, ceil + 2))
        _arrow(d, (x, fl - 84), (x, ceil + 2), 4)
    d.line((178, ceil - 6), (x0 + 21, ceil - 6), (x0 + 21, fl - 64))
    _arrow(d, (x0 + 21, fl - 80), (x0 + 21, fl - 64), 4)
    # helium (dotted fill as short dashes) and water channels in the cold plate
    for k in range(2):
        d.dashed((mx0 + 8, 106 + k * 6), (mx1 - 8, 106 + k * 6), dash=1.5, gap=5)
    d.dashed((mx0 + 6, 90), (mx1 - 6, 90), dash=4, gap=3)
    # the water loop: cold plate to the CDU and back; the CDU to the building's water
    d.line((mx1, 86), (392, 86), (392, 210), (350, 210))
    _arrow(d, (392, 190), (392, 200), 4)
    d.line((300, 210), (252, 210), (252, 94), (mx0, 94))
    _arrow(d, (252, 104), (252, 98), 4)
    d.dashed((325, 234), (325, 262), dash=4, gap=3)
    d.dashed((315, 234), (315, 262), dash=4, gap=3)

    d.group('labels')
    d.text(x0 + 21, fl - 34, 'AIR', size=7)
    d.text(x0 + 21, fl - 25, 'COND.', size=7)
    d.text(130, fl + 25, 'FLOOR VOID', size=7)
    d.text(x1 + 14, (fl + slab) / 2 + 3, '12 IN', size=7, anchor='start')
    d.text(146, ceil + 12, 'RETURN', size=7)
    d.text(146, fl - 30, 'MACHINES', size=7)
    d.text(322, 72, 'COLD PLATE · WATER', size=7)
    d.text(322, 164, 'HELIUM CAP · CHIPS', size=7)
    d.text(325, 220, 'CDU', size=7)
    d.text(325, 274, 'BUILDING WATER', size=7)
    d.text(x0, 92, 'RAISED FLOOR · 1964', size=7, anchor='start')
    d.text(322, 46, 'IBM 3081 MODULE · 1980', size=7)
    return d


PLATES = {
    'eniac-room': eniac_room,
    'sage-blockhouse': sage_blockhouse,
    'machine-room': machine_room,
}
