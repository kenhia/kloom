"""Plates for The Cloud on the Ground's part rooms2 (sprint 059): carrier-hotel, google-dalles,
open-compute. See plates_for.py."""
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


def carrier_hotel():
    """A meet-me room in plan, as a schematic: carriers' cages around the walls, the cross-connect
    frame in the middle, each cage's fiber run along the overhead tray to the frame, one cross-connect
    patched between two carriers, and the fiber entering from the street through two vaults."""
    d = D()
    x0, y0, x1, y1 = 30, 30, 370, 262          # the room
    fx, fy, fw, fh = 150, 118, 100, 56         # the cross-connect frame
    # cages: four along the top wall, four along the bottom, two on each side
    top = [(46 + i * 80, 40, 66, 44) for i in range(4)]
    bot = [(46 + i * 80, 208, 66, 44) for i in range(4)]
    left = [(40, 100, 44, 40), (40, 152, 44, 40)]
    right = [(316, 100, 44, 40), (316, 152, 44, 40)]
    cages = top + bot + left + right

    d.group('thin')
    # the overhead tray: a ring around the frame, at which each cage's run turns
    ring = (118, 96, 282, 196)
    d.dashed((ring[0], ring[1]), (ring[2], ring[1]), (ring[2], ring[3]), (ring[0], ring[3]),
             (ring[0], ring[1]), dash=3, gap=3)
    for x in range(int(x0), int(x1) + 1, 20):    # floor grid ticks along the walls
        d.line((x, y1), (x, y1 + 4))
    d.line((x0 - 10, y1 + 16), (x1 + 10, y1 + 16))   # the street

    d.group()
    _box(d, x0, y0, x1 - x0, y1 - y0)                 # walls
    for (x, y, w, h) in cages:
        _box(d, x, y, w, h)
    _box(d, fx, fy, fw, fh)                           # the frame

    d.group('mid')
    # cage mesh: a few vertical bars in each cage, and a rack inside
    for (x, y, w, h) in cages:
        for k in range(1, 4):
            d.line((x + k * w / 4, y), (x + k * w / 4, y + 4))
        _box(d, x + w / 2 - 7, y + h / 2 - 9, 14, 18)
    # the frame's port panels: a grid of ports
    for i in range(10):
        for j in range(4):
            d.circle(fx + 9 + i * 9.1, fy + 10 + j * 12, 1.6)
    # each cage's fiber run: from the cage to the tray ring, then along it to the frame
    def run(cx, cy, tx, ty, px, py):
        d.line((cx, cy), (tx, ty), (px, py))
    for (x, y, w, h) in top:
        cx = x + w / 2
        run(cx, y + h, cx, ring[1], cx if fx < cx < fx + fw else min(max(cx, fx + 4), fx + fw - 4), fy)
    for (x, y, w, h) in bot:
        cx = x + w / 2
        run(cx, y, cx, ring[3], cx if fx < cx < fx + fw else min(max(cx, fx + 4), fx + fw - 4), fy + fh)
    for (x, y, w, h) in left:
        cy = y + h / 2
        run(x + w, cy, ring[0], cy, fx, cy)
    for (x, y, w, h) in right:
        cy = y + h / 2
        run(x, cy, ring[2], cy, fx + fw, cy)
    # fiber from the street: two vaults, two conduits into the room
    for vx in (96, 304):
        d.circle(vx, y1 + 16, 4)
        d.dashed((vx, y1 + 12), (vx, y1), dash=2, gap=2)

    d.group()
    # one cross-connect: a patch cord across the frame between two carriers' ports
    a = (fx + 9 + 1 * 9.1, fy + 10 + 1 * 12)
    b = (fx + 9 + 8 * 9.1, fy + 10 + 2 * 12)
    d.curve(f'M{a[0]:.1f} {a[1]:.1f} C {a[0]:.1f} {a[1] + 20:.1f} {b[0]:.1f} {b[1] + 20:.1f} {b[0]:.1f} {b[1]:.1f}')

    d.group('labels')
    d.text(200, 112, 'CROSS-CONNECT FRAME', size=7)
    d.text(200, 186, 'PATCH', size=7)
    d.text(79, 36, 'CARRIER CAGE', size=7)
    d.text(ring[2] - 2, ring[1] - 4, 'OVERHEAD TRAY', size=7, anchor='end')
    d.text(200, y1 + 28, 'FIBER FROM THE STREET', size=7)
    d.text(x1, y0 - 6, 'MEET-ME ROOM · SCHEMATIC', size=7, anchor='end')
    return d


def google_dalles():
    """The campus at the river, in plan, as a schematic not to scale: the Columbia flowing west, the
    dam upstream of the town with its powerhouse, the transmission line to the campus substation, two
    data halls with their rows of cooling towers, and the city's fiber loop."""
    d = D()
    # the river: two banks, gently curved, flowing right to left (west)
    def bank(y0, amp):
        pts = []
        for i in range(0, 41):
            x = 10 + i * 9.5
            pts.append((x, y0 + amp * math.sin((x - 10) / 380 * math.pi * 1.3)))
        return pts
    north = bank(40, 10)
    south = bank(92, 12)

    d.group('thin')
    # the townsite's street grid, between the campus and the dam
    for i in range(6):
        d.line((190 + i * 14, 150), (190 + i * 14, 222))
    for j in range(6):
        d.line((190, 150 + j * 14.4), (260, 150 + j * 14.4))
    # flow lines in the river
    for y in (58, 74):
        d.line((300, y + 6), (230, y + 4))
    _arrow(d, (240, 78), (226, 78))

    d.group()
    d.line(*north)
    d.line(*south)
    # the dam: a line across the river, with the powerhouse block on the south end
    dx = 330
    yn = 40 + 10 * math.sin((dx - 10) / 380 * math.pi * 1.3)
    ys = 92 + 12 * math.sin((dx - 10) / 380 * math.pi * 1.3)
    d.line((dx, yn), (dx + 8, ys))
    _box(d, dx + 2, ys - 18, 16, 14)
    # the campus: two halls, west of the town
    halls = [(40, 150, 110, 30), (40, 200, 110, 30)]
    for (x, y, w, h) in halls:
        _box(d, x, y, w, h)
    # substation, fenced
    _box(d, 160, 248, 24, 16)

    d.group('mid')
    # cooling towers: a row of cells along the north side of each hall
    for (x, y, w, h) in halls:
        for k in range(6):
            d.circle(x + 12 + k * 17.5, y - 6, 4.2)
    # hall modules
    for (x, y, w, h) in halls:
        for k in range(1, 5):
            d.line((x + k * w / 5, y), (x + k * w / 5, y + h))
    # the transmission line: from the powerhouse south and west to the substation, towers as ticks
    line_pts = [(dx + 10, ys - 4), (dx + 10, 270), (184, 270), (184, 256)]
    d.line(*line_pts)
    for x in range(200, int(dx + 10), 26):
        d.line((x, 266), (x, 274))
    for y in range(120, 270, 26):
        d.line((dx + 6, y), (dx + 14, y))
    d.line((160, 256), (150, 256), (150, 230))       # feeder to the halls
    # the city's fiber loop: a dashed ring through the town to the campus
    d.dashed((96, 236), (96, 244), (230, 244), (230, 226), dash=3, gap=3)

    d.group('labels')
    d.text(120, 70, 'COLUMBIA RIVER', size=7)
    d.text(233, 96 + 14, 'FLOW', size=7)
    d.text(dx + 4, yn - 6, 'DAM', size=7)
    d.text(95, 134, 'COOLING TOWERS', size=7)
    d.text(70, 260, 'DATA HALLS', size=7)
    d.text(225, 140, 'TOWN', size=7)
    d.text(260, 284, 'TRANSMISSION LINE', size=7)
    d.text(200, 252, 'FIBER', size=7)
    d.text(390, 16, 'SCHEMATIC · NOT TO SCALE', size=7, anchor='end')
    return d


def open_compute():
    """The Prineville airflow in section, after the Open Compute data center specification of 2011
    (its figure 2 and section 5.3.2): outside air in through louvers in the penthouse, through the
    filters, the misting room and the mist eliminator, pushed by the fan wall straight down into the
    cold aisle, through the racks into the contained hot aisles, up into the return plenum, and then
    back to the intake to mix or out through the relief. A schematic: proportions are not the site's."""
    d = D()
    g = 270                  # ground: the data hall's floor
    roof = 40
    pfloor = 130             # penthouse floor
    ceil = 150               # data hall ceiling; the return plenum lies between
    x0, x1 = 20, 380
    cold = (180, 220)        # the cold aisle, under the fan room
    hots = [(100, 140), (260, 300)]
    racks = [(140, 180), (220, 260)]
    rooms = [60, 100, 150, 165, 235, 345]   # walls: intake | filters | misting | eliminator | fans | (return) | relief

    d.group('thin')
    d.line((5, g), (395, g))
    for x in rooms:
        d.line((x, roof), (x, pfloor))
    for x in (40, 60):                        # the return-air opening into the intake corridor
        d.line((x, pfloor), (x, ceil))

    d.group()
    d.line((x0, g), (x0, roof), (x1, roof), (x1, g))            # the building
    # penthouse floor, open over the cold aisle and over the return opening and the relief shaft
    d.line((x0, pfloor), (40, pfloor)); d.line((60, pfloor), (cold[0], pfloor))
    d.line((cold[1], pfloor), (345, pfloor))
    # hall ceiling, open over the hot aisles and the cold aisle
    d.line((x0, ceil), (hots[0][0], ceil)); d.line((hots[0][1], ceil), (cold[0], ceil))
    d.line((cold[1], ceil), (hots[1][0], ceil)); d.line((hots[1][1], ceil), (x1, ceil))
    # the supply shaft: the fan room's floor drops straight to the cold aisle
    d.line((cold[0], pfloor), (cold[0], ceil)); d.line((cold[1], pfloor), (cold[1], ceil))
    # hot-aisle containment
    for (a, b) in hots:
        d.line((a, ceil), (a, g)); d.line((b, ceil), (b, g))
    # rack rows facing the cold aisle
    for (a, b) in racks:
        _box(d, a, 172, b - a, g - 172)
    # louvers on the penthouse's outer wall
    for y in range(roof + 8, pfloor - 4, 9):
        d.line((x0 - 6, y + 4), (x0 + 6, y - 2))
    # filter bank, a pleated zigzag
    d.line(*[(80 + (5 if k % 2 else -5), roof + 16 + k * 7) for k in range(11)])
    # mist eliminator, chevrons
    for y in range(roof + 16, pfloor - 8, 9):
        d.line((154, y), (160, y + 4.5), (154, y + 9))
    # the fan wall, over the shaft
    for x in (186, 214):
        d.circle(x, 112, 9)

    d.group('mid')
    # misting nozzles
    for i in range(4):
        for j in range(6):
            d.circle(110 + i * 11, roof + 22 + j * 11, 1.3)
    # server slots
    for (a, b) in racks:
        for y in range(180, g, 9):
            d.line((a + 3, y), (b - 3, y))
    # air: in through the louvers, along the penthouse to the fans
    yA = 84
    d.line((2, yA), (52, yA)); _arrow(d, (40, yA), (52, yA))
    d.line((66, yA), (74, yA)); _arrow(d, (68, yA), (74, yA))
    d.line((88, yA), (102, yA)); _arrow(d, (95, yA), (102, yA))
    d.line((166, yA), (200, yA), (200, 100)); _arrow(d, (200, 92), (200, 100))
    # down the shaft into the cold aisle
    d.line((200, 124), (200, 176)); _arrow(d, (200, 166), (200, 176))
    # through the racks into the hot aisles
    for y in (205, 235):
        d.line((192, y), (134, y)); _arrow(d, (145, y), (134, y))
        d.line((208, y), (266, y)); _arrow(d, (255, y), (266, y))
    # up the hot aisles into the plenum
    for x in (120, 280):
        d.line((x, 250), (x, 142)); _arrow(d, (x, 152), (x, 142))
    # return: back along the plenum to the intake, or out through the relief
    d.dashed((112, 140), (50, 140), (50, 104), dash=3, gap=3); _arrow(d, (50, 112), (50, 104))
    d.dashed((288, 140), (362, 140), (362, 22), dash=3, gap=3); _arrow(d, (362, 32), (362, 22))

    d.group('labels')
    d.text(x0, roof - 8, 'OUTSIDE AIR', size=7, anchor='start')
    d.text(80, roof + 10, 'FILTERS', size=7)
    d.text(126, roof + 10, 'MIST', size=7)
    d.text(200, roof + 10, 'FANS', size=7)
    d.text(200, g - 4, 'COLD', size=7)
    d.text(120, g - 4, 'HOT', size=7)
    d.text(280, g - 4, 'HOT', size=7)
    d.text(228, 143, 'RETURN', size=7, anchor='start')
    d.text(362, 14, 'RELIEF', size=7)
    return d


PLATES = {'carrier-hotel': carrier_hotel, 'google-dalles': google_dalles, 'open-compute': open_compute}
