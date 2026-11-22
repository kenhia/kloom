"""Plates for The Cloud on the Ground's part case1 (sprint 059): what runs in a data center, and
the efficiency argument. See plates_for.py."""
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


def what_runs_there():
    """A schematic of one request: users' devices, through the network's routers, to a data hall in
    section holding the three kinds of machine the Berkeley report counts (conventional servers,
    storage, AI servers), and the answer back. A schematic, not any one site."""
    d = D()
    g = 262                                   # ground
    hx0, hx1, roof = 226, 386, 70             # the building
    racks = [  # (x, kind): two conventional rows, one storage, two AI rows
        (238, 'cpu'), (262, 'cpu'), (290, 'disk'), (322, 'gpu'), (350, 'gpu')]
    rtop, rbot = 128, 240
    routers = [(118, 150), (156, 118), (178, 176), (204, 140)]

    d.group('thin')
    d.line((8, g), (392, g))
    for x in range(hx0, hx1 + 1, 16):         # floor grid of the hall
        d.line((x, rbot + 4), (x, rbot + 8))
    d.line((hx0, rbot + 4), (hx1, rbot + 4))  # raised floor datum
    d.line((hx0 - 6, roof), (hx0 - 6, g))     # height dimension
    for y in (roof, g):
        d.line((hx0 - 10, y), (hx0 - 2, y))
    for x in (60, 160, 306):                  # three zones' centre lines
        d.line((x, 34), (x, 44))

    d.group()
    # the building in section
    d.line((hx0, g), (hx0, roof), (hx1, roof), (hx1, g))
    d.line((hx0, rbot), (hx1, rbot))
    # racks: conventional servers in shallow slots, storage as drive bays, AI servers as deep trays
    for x, kind in racks:
        _box(d, x, rtop, 18, rbot - rtop)
    # users: a phone, a laptop and a desk terminal
    _box(d, 30, 112, 14, 26)
    d.line((22, 186), (56, 186), (62, 196), (16, 196), closed=True)   # laptop base
    _box(d, 24, 162, 30, 24)                                         # laptop screen
    _box(d, 70, 214, 34, 24)                                         # terminal screen
    d.line((78, 238), (78, 248)); d.line((96, 238), (96, 248)); d.line((70, 248), (104, 248))
    # the network: routers joined by links
    for (x, y) in routers:
        d.circle(x, y, 8)
    for a, b in ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)):
        d.line(routers[a], routers[b])

    d.group('mid')
    for x, kind in racks:
        if kind == 'cpu':
            for y in range(rtop + 6, rbot, 8):
                d.line((x + 3, y), (x + 15, y))
        elif kind == 'disk':
            for y in range(rtop + 6, rbot - 4, 12):
                for c in (x + 5, x + 13):
                    d.line((c, y), (c, y + 8))
        else:
            for y in range(rtop + 8, rbot, 18):
                _box(d, x + 3, y, 12, 12)
            d.line((x + 9, rtop), (x + 9, rtop - 18), (x + 9 + (14 if x < 350 else -14), rtop - 18))
    # the request (solid) and the answer (dashed), each through the network
    d.line((46, 132), (109, 153)); _arrow(d, (95, 148), (109, 153))
    d.line((212, 140), (220, 140), (220, 112), (300, 112)); _arrow(d, (290, 112), (300, 112))
    d.dashed((247, rtop), (247, 96), (170, 96), (161, 110), dash=4, gap=3)
    _arrow(d, (166, 103), (161, 110))
    d.dashed((110, 144), (46, 122), dash=4, gap=3)
    _arrow(d, (56, 125), (46, 122))
    for (x, y) in routers:                    # router cross-marks
        d.line((x - 4, y), (x + 4, y)); d.line((x, y - 4), (x, y + 4))

    d.group('labels')
    d.text(60, 28, 'USERS', size=7)
    d.text(160, 28, 'NETWORK', size=7)
    d.text(306, 28, 'DATA HALL', size=7)
    d.text(256, 254, 'SERVERS', size=7)
    d.text(299, 276, 'STORAGE', size=7)
    d.text(345, 254, 'AI SERVERS', size=7)
    d.text(208, 90, 'ANSWER', size=7)
    d.text(262, 107, 'REQUEST', size=7)
    d.line((299, 268), (299, 244))
    return d


# Masanet, Shehabi, Lei, Smith and Koomey, Science 367 (2020), first figure: each driver's value in
# 2018 divided by its value in 2010. Energy is 205 / 194 TWh.
_FACTORS = [
    ('STORAGE CAPACITY', 26, 'mid'),
    ('IP TRAFFIC', 11, 'mid'),
    ('COMPUTE INSTANCES', 6.5, 'main'),
    ('ENERGY USE', 205 / 194, 'main'),
    ('PUE', 0.75, 'mid'),
    ('SERVER Wh PER COMPUTATION', 0.24, 'mid'),
    ('DRIVE kWh PER TB', 0.11, 'mid'),
]


def efficiency_case():
    """The decade 2010-2018 on a log axis: each driver of global data center energy use as a
    multiple of its 2010 value, from the paper's first figure, with energy use itself nearly flat."""
    d = D()
    x0, x1 = 66, 196                           # 2010 and 2018
    y1 = 168                                   # the 2010 value, x1
    per_dec = 70                               # units per factor of ten

    def y(f):
        return y1 - per_dec * math.log10(f)

    d.group('thin')
    for k in (-1, 0, 1, 2):
        yy = y(10 ** k)
        d.line((x0 - 10, yy), (x1 + 4, yy))
        for m in range(2, 10):                 # minor log ticks
            if k < 2:
                ym = y(m * 10 ** k)
                d.line((x0 - 6, ym), (x0 - 2, ym))
    d.line((x0, y(100) - 8), (x0, y(0.1) + 8))
    d.line((x1, y(100) - 8), (x1, y(0.1) + 8))

    d.group()
    for name, f, w in _FACTORS:
        if w == 'main':
            d.line((x0, y1), (x1, y(f)))
            d.circle(x1, y(f), 2.5)
    d.circle(x0, y1, 3)

    d.group('mid')
    for name, f, w in _FACTORS:
        if w == 'mid':
            d.line((x0, y1), (x1, y(f)))
            d.circle(x1, y(f), 1.8)

    d.group('labels')
    for k, lab in ((-1, '0.1'), (0, '1'), (1, '10'), (2, '100')):
        d.text(x0 - 14, y(10 ** k) + 2.5, lab, size=7, anchor='end')
    d.text(x0, y(0.1) + 20, '2010', size=7)
    d.text(x1, y(0.1) + 20, '2018', size=7)
    for name, f, w in _FACTORS:
        val = f'{f:.2f}'.rstrip('0').rstrip('.') if f < 10 else f'{f:g}'
        d.text(x1 + 8, y(f) + 2.5, f'{name} x{val}', size=7, anchor='start')
    d.text(200, 14, '2018 AS A MULTIPLE OF 2010 · LOG SCALE', size=7)
    d.text(200, 286, 'MASANET ET AL., SCIENCE, 2020: MODELED', size=7)
    return d


PLATES = {'what-runs-there': what_runs_there, 'efficiency-case': efficiency_case}
