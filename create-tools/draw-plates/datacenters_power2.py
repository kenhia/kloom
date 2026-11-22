"""Plates for The Cloud on the Ground's gas and nuclear frames (sprint 059, part power2). See plates_for.py."""
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


def _turbine(d, x0, x1, yc, h0, h1):
    """A turbine or compressor in side view: a trapezoid from height h0 at x0 to h1 at x1."""
    d.line((x0, yc - h0 / 2), (x1, yc - h1 / 2), (x1, yc + h1 / 2), (x0, yc + h0 / 2), closed=True)


def _blades(d, x0, x1, yc, h0, h1, n):
    """Blade rows across a trapezoid, as vertical strokes spaced evenly."""
    for i in range(1, n + 1):
        t = i / (n + 1)
        x = x0 + (x1 - x0) * t
        h = h0 + (h1 - h0) * t
        d.line((x, yc - h / 2 + 2), (x, yc + h / 2 - 2))


def _generator(d, x, yc, w=26, h=26):
    _box(d, x, yc - h / 2, w, h)
    d.circle(x + w / 2, yc, h / 2 - 5)


def _hyperboloid(d, cx, base, top, r_base, r_waist, r_top, waist):
    """A cooling tower's outline: a hyperbola r(y) = a * sqrt(1 + ((y - waist) / b)^2), fitted through
    the base, the waist and the top radii (the top fitted by the same b only approximately)."""
    a = r_waist
    b = (base - waist) / math.sqrt((r_base / a) ** 2 - 1)
    left, right = [], []
    steps = 24
    for i in range(steps + 1):
        y = top + (base - top) * i / steps
        r = a * math.sqrt(1 + ((y - waist) / b) ** 2)
        left.append((cx - r, y))
        right.append((cx + r, y))
    d.line(*left)
    d.line(*right)
    return left, right


def gas_plants():
    """A combined-cycle plant in schematic: the gas turbine, its exhaust through a heat-recovery steam
    generator to the stack, the steam turbine and condenser, and the share of the fuel's heat each
    turns into power. Efficiencies are round figures from the Wikipedia article the frame cites."""
    d = D()
    yc = 92                 # the gas turbine's shaft line
    ys = 214                # the steam turbine's shaft line
    d.group('thin')
    d.line((14, yc), (176, yc))                       # gas train centreline
    d.line((150, ys), (300, ys))                      # steam train centreline
    d.line((10, 268), (390, 268))                     # ground
    for x in range(200, 280, 12):                     # HRSG tube banks, as construction
        d.line((x, 44), (x, 150))

    d.group()
    # gas turbine: compressor (narrowing), combustor, turbine (widening)
    _turbine(d, 24, 70, yc, 54, 26)
    _box(d, 70, yc - 17, 22, 34)
    _turbine(d, 92, 136, yc, 30, 58)
    _generator(d, 142, yc)
    # exhaust duct to the heat-recovery steam generator, and the stack
    d.line((136, yc - 29), (190, 40), (282, 40), (282, 6))
    d.line((136, yc + 29), (190, 156), (300, 156), (300, 6))
    # steam turbine, its generator, and the condenser beneath
    _turbine(d, 190, 250, ys, 26, 56)
    _generator(d, 254, ys)
    _box(d, 196, 238, 54, 22)

    d.group('mid')
    _blades(d, 24, 70, yc, 54, 26, 5)
    _blades(d, 92, 136, yc, 30, 58, 4)
    _blades(d, 190, 250, ys, 26, 56, 5)
    # steam from the HRSG to the steam turbine, water back from the condenser by a pump
    d.line((204, 156), (204, 180), (176, 180), (176, ys), (190, ys))
    _arrow(d, (180, ys), (190, ys))
    d.line((223, 260), (223, 278), (362, 278), (362, 172), (290, 172), (290, 156))
    _arrow(d, (290, 166), (290, 156))
    d.circle(270, 278, 5)                             # feedwater pump
    # air in, fuel in, exhaust up the stack
    d.line((4, yc), (20, yc)); _arrow(d, (8, yc), (20, yc))
    d.line((81, 40), (81, yc - 17)); _arrow(d, (81, 56), (81, yc - 17))
    for k in (-6, 0, 6):
        d.curve(f'M{291 + k} 4 q 3 -4 0 -8')
    # cooling water through the condenser
    d.line((166, 249), (196, 249)); _arrow(d, (184, 249), (196, 249))
    d.line((250, 249), (276, 249)); _arrow(d, (264, 249), (276, 249))
    # the efficiency bars: share of the fuel's heat turned into electricity
    bx, by, bw = 22, 160, 100                      # 100% = 100 units
    _box(d, bx, by, bw * 0.40, 10)
    _box(d, bx, by + 26, bw * 0.60, 10)
    d.line((bx, by - 4), (bx, by + 42))

    d.group('labels')
    d.text(47, yc + 40, 'COMPRESSOR', size=7)
    d.text(81, yc + 29, 'BURNER', size=7)
    d.text(114, yc + 42, 'GAS TURBINE', size=7)
    d.text(92, 44, 'GAS', size=7, anchor='start')
    d.text(10, yc - 8, 'AIR', size=7, anchor='start')
    d.text(236, 32, 'HEAT-RECOVERY BOILER', size=7)
    d.text(306, 20, 'STACK', size=7, anchor='start')
    d.text(286, ys + 3, 'STEAM TURBINE', size=7, anchor='start')
    d.text(223, 254, 'CONDENSER', size=7)
    d.text(bx, by - 8, 'SHARE OF FUEL HEAT TO POWER', size=7, anchor='start')
    d.text(bx + bw * 0.40 + 4, by + 8, 'GAS TURBINE ~40%', size=7, anchor='start')
    d.text(bx + bw * 0.60 + 4, by + 34, 'COMBINED CYCLE ~60%', size=7, anchor='start')
    return d


def nuclear_deals():
    """A pressurized-water reactor's three loops in schematic: the core and its primary loop to the
    steam generator inside the containment, the secondary loop through the turbine and condenser, and
    the cooling-water loop to a hyperbolic tower. Below, Crane's output (835 MW, DOE) against Amazon's
    contract at Susquehanna (1,920 MW, Talen) as bars to one scale."""
    d = D()
    g = 212                       # ground
    cx, dome_r = 70, 46           # containment: a cylinder with a hemispherical dome
    wall_top = 120
    d.group('thin')
    d.line((8, g), (392, g))
    d.line((cx, wall_top - dome_r - 6), (cx, g))      # containment axis
    # bar scale: 0 to 2,000 MW over 300 units
    sx0, sy = 60, 252
    scale = 300 / 2000
    for mw in (0, 500, 1000, 1500, 2000):
        x = sx0 + mw * scale
        d.line((x, sy - 6), (x, sy + 34))

    d.group()
    # containment
    d.line((cx - dome_r, g), (cx - dome_r, wall_top))
    d.line((cx + dome_r, g), (cx + dome_r, wall_top))
    d.arc(cx, wall_top, dome_r, 180, 360)
    # reactor vessel with its core, and the steam generator
    _box(d, 42, 150, 22, 50)
    _box(d, 92, 120, 16, 64)
    # turbine hall: turbine and generator; condenser beneath
    _turbine(d, 168, 222, 132, 22, 48)
    _generator(d, 228, 132, 24, 24)
    _box(d, 172, 168, 48, 20)
    # cooling tower, its hyperbolic shell computed
    _hyperboloid(d, 330, g, 74, 38, 24, 25, 104)
    d.line((292, g), (368, g))

    d.group('mid')
    # core: fuel assemblies
    for x in range(46, 62, 4):
        d.line((x, 172), (x, 196))
    # primary loop: vessel to steam generator and back (inside containment)
    d.line((64, 160), (92, 160)); _arrow(d, (80, 160), (92, 160))
    d.line((92, 178), (64, 178)); _arrow(d, (76, 178), (64, 178))
    # secondary loop: steam to the turbine, water back from the condenser
    d.line((104, 120), (104, 104), (150, 104), (150, 132), (168, 132)); _arrow(d, (158, 132), (168, 132))
    d.line((196, 188), (196, 200), (130, 200), (130, 176), (108, 176)); _arrow(d, (118, 176), (108, 176))
    # cooling-water loop: condenser to tower and back
    d.line((220, 172), (300, 172)); _arrow(d, (288, 172), (300, 172))
    d.line((304, 204), (240, 204), (240, 184), (220, 184)); _arrow(d, (230, 184), (220, 184))
    # vapor over the tower
    for k in (-10, 0, 10):
        d.curve(f'M{330 + k} 68 q 5 -7 0 -14 q -5 -7 0 -14')
    # the bars
    _box(d, sx0, sy, 835 * scale, 10)
    _box(d, sx0, sy + 18, 1920 * scale, 10)

    d.group('labels')
    d.text(53, 146, 'CORE', size=7)
    d.text(88, 116, 'STEAM GEN.', size=7, anchor='end')
    d.text(cx, 62, 'CONTAINMENT', size=7)
    d.text(195, 112, 'TURBINE', size=7)
    d.text(196, 196, 'CONDENSER', size=7)
    d.text(330, 30, 'COOLING TOWER', size=7)
    d.text(sx0 - 4, sy + 8, 'CRANE', size=7, anchor='end')
    d.text(sx0 + 835 * scale + 4, sy + 8, 'OUTPUT 835 MW', size=7, anchor='start')
    d.text(sx0 - 4, sy + 26, 'AWS', size=7, anchor='end')
    d.text(sx0 + 1920 * scale / 2, sy + 42, 'SUSQUEHANNA CONTRACT 1,920 MW', size=7)
    return d


PLATES = {'gas-plants': gas_plants, 'nuclear-deals': nuclear_deals}
