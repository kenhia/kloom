"""Plates for The Cloud on the Ground's frames by part neigh1 (sprint 059): noise and
diesel-generators. See plates_for.py."""
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


def noise():
    """Sound level against distance from a campus wall, on a doubling (log) distance axis: a straight
    fall of 6 dB per doubling (inverse-square spreading, our arithmetic), a 200-foot setback and a house
    at 600 feet marked, and at the house's wall the drop indoors, 25 dB at 1,000 Hz but 15 dB at 63 Hz
    (Nelson Acoustics' table for a wood-frame house). The starting level is invented: a schematic."""
    d = D()
    x0, x1 = 60, 330            # plot: 25 m to 800 m on a log2 axis
    y_top, y_bot = 40, 250      # 75 dB to 20 dB
    r0, r1 = 25.0, 800.0
    lv_top, lv_bot = 75.0, 20.0

    def X(r):
        return x0 + (x1 - x0) * math.log2(r / r0) / math.log2(r1 / r0)

    def Y(lv):
        return y_bot - (y_bot - y_top) * (lv - lv_bot) / (lv_top - lv_bot)

    L0 = 70.0                   # invented level at 25 m

    def level(r):
        return L0 - 20 * math.log10(r / r0)

    setback = 200 * 0.3048      # 200 feet, Fairfax's rule
    house = 600 * 0.3048        # 600 feet, Great Oak's distance

    d.group('thin')
    for r in (25, 50, 100, 200, 400, 800):          # doubling ticks and grid
        d.line((X(r), y_top), (X(r), y_bot))
    for lv in range(20, 80, 10):
        d.line((x0, Y(lv)), (x1, Y(lv)))
    # the 6 dB step between two doublings, drawn as a construction triangle
    a, b = 50, 100
    d.line((X(a), Y(level(a))), (X(b), Y(level(a))), (X(b), Y(level(b))))

    d.group()
    d.line((x0, y_top), (x0, y_bot), (x1, y_bot))                      # axes
    d.line((32, 60), (32, y_bot))                                       # the campus wall
    d.lines(hatch([(24, 60), (32, 60), (32, y_bot), (24, y_bot)], 6, 45))
    pts = [(X(r), Y(level(r))) for r in (25, house)]
    d.line(*pts)                                                        # the fall with distance
    # the house: a small elevation standing on the axis at 600 feet
    hx = X(house)
    d.line((hx - 9, y_bot), (hx - 9, y_bot - 14), (hx, y_bot - 22), (hx + 9, y_bot - 14),
           (hx + 9, y_bot))

    d.group('mid')
    d.dashed((X(setback), y_top + 6), (X(setback), y_bot), dash=4, gap=3)  # the setback line
    d.dashed(pts[1], (X(r1), Y(level(r1))), dash=4, gap=3)                 # beyond the house
    # indoors: the two bands' drops at the house's wall
    lh = level(house)
    for dx, drop in ((14, 25), (36, 15)):
        top, bot = (hx + dx, Y(lh)), (hx + dx, Y(lh - drop))
        d.line(top, bot)
        _arrow(d, (bot[0], bot[1] - 8), bot, 4)
        d.line((bot[0] - 5, bot[1]), (bot[0] + 5, bot[1]))
    d.line((hx, Y(lh)), (hx + 42, Y(lh)))
    d.circle(X(25), Y(L0), 2.5)

    d.group('labels')
    for r in (25, 50, 100, 200, 400, 800):
        d.text(X(r), y_bot + 12, f'{r}', size=7)
    d.text((x0 + x1) / 2, y_bot + 24, 'METERS FROM THE WALL, EACH STEP A DOUBLING', size=7)
    for lv in range(20, 80, 10):
        d.text(x0 - 4, Y(lv) + 2.5, f'{lv}', size=7, anchor='end')
    d.text(x0 - 4, y_top - 8, 'DB', size=7, anchor='end')
    d.text(X(b) + 3, Y((level(a) + level(b)) / 2) + 2.5, '-6 DB', size=7, anchor='start')
    d.text(X(setback) + 3, y_top + 2, 'SETBACK 200 FT', size=7, anchor='start')
    d.text(hx + 19, Y(lh - 25) + 2.5, '1 KHZ', size=7, anchor='start')
    d.text(hx + 41, Y(lh - 15) + 2.5, '63 HZ', size=7, anchor='start')
    d.text(hx + 12, y_bot - 4, 'HOUSE, 600 FT', size=7, anchor='start')
    d.text(hx + 25, Y(lh) - 5, 'INDOORS', size=7)
    d.text(200, 22, 'SCHEMATIC · INVENTED STARTING LEVEL', size=7)
    return d


def diesel_generators():
    """A containerized standby generator set in section: engine, alternator on the same shaft,
    radiator and its fan at the end, the exhaust through a silencer to a catalyst and particulate
    filter on the roof, a urea tank for the catalyst, and the fuel tank beneath the skid."""
    d = D()
    cx0, cx1 = 30, 370          # container walls
    cy0, cy1 = 84, 210          # roof and floor of the enclosure
    tank_y1 = 246               # base of the sub-base fuel tank
    ground = 252

    d.group('thin')
    d.line((8, ground), (392, ground))
    shaft_y = 168
    d.dashed((60, shaft_y), (290, shaft_y), dash=6, gap=3)            # the shaft's center line
    for x in (110, 236):                                              # engine and alternator centers
        d.line((x, 120), (x, 214))
    d.line((cx0, 258), (cx0, 278)); d.line((cx1, 258), (cx1, 278))   # overall length, dimension
    d.line((cx0, 270), (cx1, 270))
    _arrow(d, (cx0 + 10, 270), (cx0, 270), 4); _arrow(d, (cx1 - 10, 270), (cx1, 270), 4)

    d.group()
    _box(d, cx0, cy0, cx1 - cx0, cy1 - cy0)                           # the enclosure
    _box(d, cx0, cy1, cx1 - cx0, tank_y1 - cy1)                       # sub-base fuel tank
    d.line((cx0 + 6, tank_y1), (cx0 + 6, ground)); d.line((cx1 - 6, tank_y1), (cx1 - 6, ground))
    # the engine: a block with a V of cylinders above the crankshaft
    _box(d, 64, 140, 92, 52)
    for k in range(4):
        x = 72 + k * 22
        d.line((x, 140), (x - 6, 118), (x + 8, 112), (x + 14, 134))
    # the alternator: a drum on the shaft, with its windings' end rings
    _box(d, 196, 138, 80, 60)
    d.line((156, shaft_y), (196, shaft_y))                            # coupling
    # the radiator at the end, its core and its fan
    _box(d, 322, 96, 22, 108)
    d.circle(308, 150, 22)
    # exhaust: up from the engine through the silencer to the aftertreatment on the roof
    d.line((90, 112), (90, 96), (120, 96))
    _box(d, 120, 88, 70, 18)                                          # silencer
    d.line((190, 97), (206, 97), (206, cy0), (206, 66))
    _box(d, 196, 46, 104, 20)                                         # SCR and particulate filter
    d.line((300, 56), (318, 56), (318, 26))                           # stack

    d.group('mid')
    # radiator core fins and fan blades
    for y in range(102, 200, 8):
        d.line((326, y), (340, y))
    for k in range(5):
        a = math.radians(k * 72)
        d.line((308, 150), (308 + 20 * math.cos(a), 150 + 20 * math.sin(a)))
    # alternator windings
    for x in range(204, 272, 8):
        d.line((x, 142), (x, 194))
    # fuel in the tank, hatched, and its feed to the engine
    for (a, b) in ((cx0 + 2, 160), (240, cx1 - 2)):
        d.lines(hatch([(a, 214), (b, 214), (b, tank_y1 - 2), (a, tank_y1 - 2)], 7, 45))
    d.line((70, 210), (70, 192))
    # urea tank feeding the catalyst
    _box(d, 238, 104, 28, 22)
    d.line((252, 104), (252, 66))
    # air: in through the louvers, out through the radiator
    for y in (110, 150, 190):
        d.line((10, y), (cx0 - 2, y)); _arrow(d, (10, y), (cx0 - 2, y), 4)
        d.line((cx1 + 2, y), (390, y)); _arrow(d, (cx1 + 2, y), (390, y), 4)

    d.group('labels')
    d.text(110, 204, 'ENGINE', size=7)
    d.text(236, 206, 'ALTERNATOR', size=7)
    d.text(333, 93, 'RADIATOR', size=7)
    d.text(155, 100, 'SILENCER', size=7)
    d.text(248, 40, 'SCR + PARTICULATE FILTER', size=7)
    d.text(252, 118, 'UREA', size=7)
    d.text(200, 238, 'FUEL TANK', size=7)
    d.text(200, 286, '40-FOOT CONTAINER', size=7)
    return d


PLATES = {'noise': noise, 'diesel-generators': diesel_generators}
