"""Plates for The Cloud on the Ground's water1 frames (sprint 059). See plates_for.py."""
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


def _fans(d, x, y, w, n, r):
    """n fan rings evenly along a top edge from x to x + w, at height y."""
    for k in range(n):
        cx = x + w * (k + 0.5) / n
        d.circle(cx, y, r)
        d.line((cx - r * 0.7, y), (cx + r * 0.7, y))


def _vcoil(d, x, y, w, h, n):
    """A V-bank coil seen from the side: n vees between x and x + w."""
    pts = []
    for k in range(n + 1):
        pts.append((x + w * k / n, y if k % 2 == 0 else y + h))
    d.line(*pts)


def where_water_goes():
    """The heat path as a flow: chip, the closed indoor loop, the heat exchanger at the wall, then three
    alternative ways to give the heat to the outside air, each with what it uses. A schematic."""
    d = D()
    wall = 200                    # the building's wall: inside to the left, outside to the right
    rows = (62, 150, 238)         # the three outdoor alternatives' center lines
    hx = (150, 118, 32, 64)       # heat exchanger: x, y, w, h
    d.group('thin')
    d.dashed((wall, 18), (wall, 286), dash=5, gap=4)
    for y in rows:                                        # center lines of the three alternatives
        d.line((236, y), (352, y))
    d.line((20, 150), (184, 150))                         # the loop's axis
    for y in (100, 200):                                  # the rack's datum lines
        d.line((14, y), (26, y))

    d.group()
    # a rack, its servers, and one chip with its cold plate
    _box(d, 26, 100, 52, 100)
    for y in range(108, 196, 11):
        d.line((30, y), (74, y))
    _box(d, 40, 140, 24, 20)                              # the chip's cold plate
    # the heat exchanger at the wall: a box with its plates
    x, y, w, h = hx
    _box(d, x, y, w, h)
    for k in range(1, 6):
        d.line((x + w * k / 6, y + 6), (x + w * k / 6, y + h - 6))
    # the three outdoor alternatives
    # 1 cooling tower: a cell with its fan stack, fill and basin
    tx, ty, tw, th = 262, 40, 64, 40
    d.line((tx, ty + th), (tx + 6, ty), (tx + tw - 6, ty), (tx + tw, ty + th), closed=True)
    d.line((tx + 22, ty), (tx + 26, ty - 8), (tx + 38, ty - 8), (tx + 42, ty))
    # 2 dry cooler: a box of V coils under fans
    dx, dy, dw, dh = 256, 136, 76, 28
    _box(d, dx, dy, dw, dh)
    # 3 adiabatic cooler: the same box, with wetted pads on its sides
    ax, ay, aw, ah = 256, 224, 76, 28
    _box(d, ax, ay, aw, ah)
    _box(d, ax - 8, ay + 2, 8, ah - 4)
    _box(d, ax + aw, ay + 2, 8, ah - 4)

    d.group('mid')
    # the closed indoor loop: supply out along the top, return along the bottom
    d.line((64, 146), (110, 146), (110, 128), (hx[0], 128))
    _arrow(d, (hx[0] - 14, 128), (hx[0], 128))
    d.line((hx[0], 172), (110, 172), (110, 154), (64, 154))
    _arrow(d, (78, 154), (64, 154))
    # the outdoor side: from the exchanger to each alternative, dashed, since a site chooses
    ox = hx[0] + hx[2]
    for y in rows:
        d.dashed((ox, 150), (212, 150), (212, y), (252, y), dash=4, gap=3)
        _arrow(d, (240, y), (252, y), 4)
    # tower: fill in the cell, vapor leaving, make-up water coming in
    d.lines(hatch([(tx + 6, ty + 14), (tx + tw - 6, ty + 14), (tx + tw - 3, ty + 30), (tx + 3, ty + 30)], 5, 60))
    for k in (-8, 0, 8):
        d.curve(f'M{tx + 32 + k} {ty - 12} q 4 -5 0 -10 q -4 -5 0 -10')
    d.line((370, ty + th + 6), (tx + tw - 4, ty + th + 6))
    _arrow(d, (tx + tw + 10, ty + th + 6), (tx + tw - 4, ty + th + 6), 4)
    # dry cooler: V coils and fans, air rising
    _vcoil(d, dx + 4, dy + 4, dw - 8, dh - 8, 8)
    _fans(d, dx, dy - 4, dw, 3, 7)
    for k in (0.2, 0.5, 0.8):
        d.line((dx + dw * k, dy - 14), (dx + dw * k, dy - 24))
        _arrow(d, (dx + dw * k, dy - 18), (dx + dw * k, dy - 25), 3)
    # adiabatic: V coils, fans, and droplets on the pads
    _vcoil(d, ax + 4, ay + 4, aw - 8, ah - 8, 8)
    _fans(d, ax, ay - 4, aw, 3, 7)
    for side in (ax - 4, ax + aw + 4):
        for yy in range(ay + 6, ay + ah - 4, 6):
            d.line((side, yy), (side, yy + 2))
    d.line((370, ay + ah + 8), (ax + aw + 4, ay + ah + 8), (ax + aw + 4, ay + ah - 2))
    _arrow(d, (ax + aw + 4, ay + ah + 4), (ax + aw + 4, ay + ah - 2), 4)

    d.group('labels')
    d.text(52, 92, 'RACK', size=7)
    d.text(52, 214, 'CHIP', size=7)
    d.text(110, 118, 'CLOSED LOOP', size=7)
    d.text(166, 200, 'HEAT', size=7)
    d.text(166, 209, 'EXCHANGER', size=7)
    d.text(wall - 4, 28, 'INSIDE', size=7, anchor='end')
    d.text(wall + 4, 28, 'OUTSIDE', size=7, anchor='start')
    d.text(300, 100, 'TOWER: WATER LEAVES AS VAPOR', size=7)
    d.text(300, 184, 'DRY COOLER: NO WATER, MORE POWER', size=7)
    d.text(300, 272, 'ADIABATIC: WATER ON HOT DAYS', size=7)
    d.text(372, ty + th + 2, 'MAKE-UP', size=7, anchor='end')
    return d


def _band(d, x0, y0a, y0b, x1, y1a, y1b, cls=None):
    """A flow band from the span y0a..y0b at x0 to y1a..y1b at x1, its edges cubic curves."""
    m = (x0 + x1) / 2
    d.curve(f'M{x0} {y0a} C{m} {y0a} {m} {y1a} {x1} {y1a} L{x1} {y1b} C{m} {y1b} {m} {y0b} {x0} {y0b} Z', cls)


def water_totals():
    """Google's data centers' water in 2025 as a flow drawn to scale (the company's own figures, in
    million gallons): three sources in, withdrawal, then what was consumed and what was discharged."""
    sources = (('POTABLE', 10949), ('NON-POTABLE', 1695), ('RECLAIMED', 918))
    withdrawn, consumed, discharged = 13562, 10523, 3039
    k = 170 / withdrawn           # plate units per million gallons
    trunk_top = 66
    d = D()
    d.group('thin')
    d.line((150, 40), (150, 262))                  # where the sources join: the meter
    d.line((236, 40), (236, 262))                  # where the water parts
    for x in (150, 236):
        d.line((x - 4, trunk_top - 8), (x + 4, trunk_top - 8))
    d.line((24, 280), (24 + 5000 * k, 280))         # scale rule: 5,000 million gallons
    d.line((24, 276), (24, 284)); d.line((24 + 5000 * k, 276), (24 + 5000 * k, 284))

    d.group()
    # sources, spread at the left and gathered into one trunk
    y_left, y_trunk = 44, trunk_top
    for name, v in sources:
        h = v * k
        _band(d, 36, y_left, y_left + h, 150, y_trunk, y_trunk + h)
        y_left += h + 18
        y_trunk += h
    d.line((150, trunk_top), (236, trunk_top))
    d.line((150, trunk_top + withdrawn * k), (236, trunk_top + withdrawn * k))
    # the parting: consumed rises to the air, discharged falls to the sewer
    hc, hd = consumed * k, discharged * k
    _band(d, 236, trunk_top, trunk_top + hc, 330, 34, 34 + hc)
    _band(d, 236, trunk_top + hc, trunk_top + hc + hd, 330, 220, 220 + hd)

    d.group('mid')
    # vapor leaving the consumed band, a drain under the discharged one
    for y in range(52, int(34 + hc) - 10, 22):
        d.curve(f'M336 {y} q 6 -4 12 0 q 6 4 12 0')
    d.line((334, 220 + hd / 2), (360, 220 + hd / 2))
    _arrow(d, (350, 220 + hd / 2), (362, 220 + hd / 2), 4)
    # a meter where withdrawal is measured
    d.circle(193, trunk_top - 18, 8)
    d.line((193, trunk_top - 10), (193, trunk_top))
    d.line((193, trunk_top - 18), (198, trunk_top - 22))

    d.group('labels')
    y_left = 44
    for name, v in sources:
        h = v * k
        d.text(40, y_left + min(h / 2, 8) + 3 if h > 14 else y_left + h + 9, name, size=7, anchor='start')
        y_left += h + 18
    d.text(24, 22, 'GOOGLE DATA CENTERS, 2025, MILLION GALLONS', size=7, anchor='start')
    d.text(193, trunk_top + withdrawn * k / 2, 'WITHDRAWN', size=7)
    d.text(193, trunk_top + withdrawn * k / 2 + 9, f'{withdrawn:,}', size=7)
    d.text(368, 30, 'CONSUMED', size=7, anchor='end')
    d.text(300, 34 + hc / 2 + 6, f'{consumed:,}', size=7)
    d.text(376, 216, 'DISCHARGED', size=7, anchor='end')
    d.text(300, 220 + hd / 2 + 3, f'{discharged:,}', size=7)
    d.text(24, 272, 'SCALE: 5,000 MILLION GALLONS', size=7, anchor='start')
    return d


PLATES = {'where-water-goes': where_water_goes, 'water-totals': water_totals}
