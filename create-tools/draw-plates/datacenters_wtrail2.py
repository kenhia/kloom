"""Plates for The Cloud on the Ground's frames by part wtrail2 (sprint 059): the end of the trail
Water, measured. See plates_for.py."""
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


def _wave(x0, x1, y, amp=2.0, period=18):
    """A river's surface as a sine path from x0 to x1."""
    pts = []
    n = int((x1 - x0) / 3)
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, y + amp * math.sin(2 * math.pi * (x - x0) / period)))
    return pts


def power_plant_water():
    """A thermal power station's condenser cooled two ways, as a schematic: once through, from a river
    and back to it (a large withdrawal, little evaporated), and by a recirculating loop through a
    natural-draft cooling tower (a small makeup withdrawal, most of it evaporated). The tower's profile
    is a hyperbola of revolution, throat at a third of its height."""
    d = D()
    river_y = 262
    # the tower: hyperbola x = a*sqrt(1 + ((y - y0)/b)^2), base radius 45 at y 236, throat 26 at y 112
    cx, y0, a = 318, 112, 26
    top, base = 62, 236
    b = (base - y0) / math.sqrt((45 / a) ** 2 - 1)

    def rad(y):
        return a * math.sqrt(1 + ((y - y0) / b) ** 2)

    d.group('thin')
    d.line((200, 30), (200, 250))                      # the panel divide
    d.line((cx, top - 6), (cx, base + 6))              # the tower's axis
    d.line((cx - a - 14, y0), (cx + a + 14, y0))       # the throat
    for x in (cx - rad(base), cx + rad(base)):
        d.line((x, base), (x, base + 8))
    d.line((8, river_y - 14), (392, river_y - 14))     # datum: the bank

    d.group()
    # once-through: turbine hall and condenser beside the river
    _box(d, 30, 120, 60, 34)                           # turbine and generator
    _box(d, 40, 178, 40, 30)                           # condenser
    d.line((60, 154), (60, 178))                       # exhaust steam down to the condenser
    d.line(*_wave(8, 192, river_y))
    d.line(*_wave(8, 192, river_y + 10))
    # recirculating: the same plant, its condenser looped to a tower
    _box(d, 214, 120, 60, 34)
    _box(d, 224, 178, 40, 30)
    d.line((244, 154), (244, 178))
    left = [(cx - rad(y), y) for y in range(top, base + 1, 4)]
    right = [(cx + rad(y), y) for y in range(top, base + 1, 4)]
    d.line(*left)
    d.line(*right)
    d.line(*_wave(208, 392, river_y))
    d.line(*_wave(208, 392, river_y + 10))

    d.group('mid')
    # once-through: a large intake and a warm discharge downstream
    for off in (0, 5):
        d.line((48 + off, river_y - 4), (48 + off, 208))
        d.line((72 + off, 208), (72 + off, river_y - 4))
    _arrow(d, (50, 238), (50, 222), 7)
    _arrow(d, (75, 222), (75, 238), 7)
    # recirculating: warm water up to a spray header inside the tower, cooled water back from its basin
    spray, basin = 200, 230
    d.line((264, 186), (cx - 8, 186), (cx - 8, spray))
    d.line((cx - rad(spray) + 4, spray), (cx + rad(spray) - 4, spray))
    for k in range(-24, 25, 8):
        d.line((cx + k, spray + 2), (cx + k, spray + 8))
    d.line((cx - rad(basin) + 3, basin), (cx + rad(basin) - 3, basin))
    d.line((cx + 8, basin), (cx + 8, 244), (254, 244), (254, 208))
    _arrow(d, (282, 186), (294, 186), 6)
    _arrow(d, (254, 226), (254, 214), 6)
    d.line((232, river_y - 4), (232, 208))
    _arrow(d, (232, 240), (232, 226), 6)
    # evaporation leaving the tower's mouth
    for k in (-14, 0, 14):
        d.curve(f'M{cx + k} {top - 6} q 5 -7 0 -14 q -5 -7 0 -14')
    # steam from boilers, a line into each turbine hall
    d.line((14, 137), (30, 137))
    d.line((198 + 6, 137), (214, 137))

    d.group('labels')
    d.text(100, 16, 'ONCE-THROUGH', size=7)
    d.text(300, 16, 'COOLING TOWER', size=7)
    d.text(60, 140, 'TURBINE', size=7)
    d.text(244, 140, 'TURBINE', size=7)
    d.text(86, 196, 'CONDENSER', size=7, anchor='start')
    d.text(100, 288, 'RIVER', size=7)
    d.text(300, 288, 'RIVER', size=7)
    d.text(228, 236, 'MAKEUP', size=7, anchor='end')
    d.text(cx + 24, top - 22, 'EVAPORATION', size=7, anchor='start')
    d.text(200, 298, 'SCHEMATIC', size=7)
    return d


# The estimates of water per prompt, in mL, with their source and scope (see water-per-prompt's reading).
ESTIMATES = [
    ('GOOGLE 2025', 'ON SITE · MEDIAN', 0.26),
    ('ALTMAN 2025', 'SCOPE NOT STATED', 0.32),
    ('LI ET AL.', 'SITE + POWER PLANT', 16.9),
    ('MISTRAL 2025', 'LIFE CYCLE', 45),
    ('THE POST 2024', '100-WORD EMAIL', 519),
]


def water_per_prompt():
    """The published estimates of water per chatbot response on a log axis from 0.1 mL to 1 L, each bar
    labeled with its source and what it counts. Li and colleagues' on-site share (2.2 of 16.9 mL, the
    U.S. average in their table 1) is marked on its bar."""
    d = D()
    x0, x1 = 150, 384          # 0.1 mL to 1000 mL: four decades
    lo, hi = -1, 3

    def X(v):
        return x0 + (math.log10(v) - lo) / (hi - lo) * (x1 - x0)

    rows = [62 + i * 44 for i in range(len(ESTIMATES))]
    h = 14
    d.group('thin')
    for e in range(lo, hi + 1):
        x = X(10 ** e)
        d.line((x, 40), (x, 272))
        for m in range(2, 10):                         # minor ticks within each decade
            if e < hi:
                xm = X(m * 10 ** e)
                d.line((xm, 268), (xm, 272))
    d.line((x0, 272), (x1, 272))

    d.group()
    for (src, scope, v), y in zip(ESTIMATES, rows):
        _box(d, x0, y - h / 2, X(v) - x0, h)

    d.group('mid')
    yl = rows[2]
    d.dashed((X(2.2), yl - h / 2 - 4), (X(2.2), yl + h / 2 + 4), dash=2, gap=2)

    d.group('labels')
    for (src, scope, v), y in zip(ESTIMATES, rows):
        d.text(8, y - 2, src, size=7, anchor='start')
        d.text(8, y + 7, scope, size=7, anchor='start')
        label = f'{v:g} ML'
        if X(v) + 6 + 4.2 * len(label) < 398:
            d.text(X(v) + 5, y + 2.5, label, size=7, anchor='start')
        else:
            d.text(X(v) - 5, y - h / 2 - 4, label, size=7, anchor='end')
    d.text(X(2.2), yl + h / 2 + 12, 'ON SITE 2.2', size=7)
    for e, lab in zip(range(lo, hi + 1), ('0.1', '1', '10', '100', '1000')):
        d.text(X(10 ** e), 284, lab, size=7)
    d.text((x0 + x1) / 2, 296, 'ML OF WATER PER RESPONSE · LOG SCALE', size=7)
    return d


PLATES = {'power-plant-water': power_plant_water, 'water-per-prompt': water_per_prompt}
