"""Plates for Daily Bread's famine1 part (sprint 051): the Great Famine of 1315 and India's famine of 1876-78.
See plates_for.py."""
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


# Rogers, A History of Agriculture and Prices in England, vol. 1 (1866), p. 230: the yearly average
# price of a quarter of wheat, in shillings and pence, converted to decimal shillings.
ROGERS_WHEAT = [
    (1312, 4, 11.375), (1313, 5, 6.375), (1314, 8, 4.375), (1315, 14, 10.875), (1316, 15, 11.875),
    (1317, 8, 3.5), (1318, 4, 6.5), (1319, 5, 9.625), (1320, 6, 5), (1321, 11, 7.75),
    (1322, 8, 11.875), (1323, 7, 5.375), (1324, 7, 4.625), (1325, 5, 8.375),
]


def great_famine_1315():
    d = D()
    # The price of wheat in England, 1312-1325, by Rogers's yearly averages, on a linear axis of
    # shillings a quarter, with the rainy summers (1314-16, Baek et al. 2020) and the cattle plague
    # (1319-20) marked as bands.
    x0, x1, y0, y1 = 62, 372, 236, 48                                     # plot box: 1311.5-1325.5, 0-18 s.
    smax = 18

    def px(year):
        return x0 + (x1 - x0) * (year - 1311.5) / 14

    def py(s):
        return y0 - (y0 - y1) * s / smax

    pts = [(px(y), py(s + p / 12)) for y, s, p in ROGERS_WHEAT]

    d.group('thin')
    for s in range(0, smax + 1, 3):                                       # grid
        d.line((x0, py(s)), (x1, py(s)))
    for y, *_ in ROGERS_WHEAT:
        d.line((px(y), y0), (px(y), y0 + 4))
    base = sum(s + p / 12 for y, s, p in ROGERS_WHEAT[:2]) / 2            # 1312-13 mean, the dashed level
    d.dashed((x0, py(base)), (x1, py(base)), dash=4, gap=3)

    d.group('mid')
    for a, b in ((1314, 1316), (1319, 1320)):                             # the bands
        l, r = px(a) - 9, px(b) + 9
        d.line((l, y1), (l, y0))
        d.line((r, y1), (r, y0))

    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))                                  # the axes
    d.line(*pts)

    d.group('mid')
    for x, y in pts:
        d.circle(x, y, 2.4)
    peak = pts[4]
    d.circle(peak[0], peak[1], 5)

    d.group('mid')
    for s in range(0, smax + 1, 6):
        d.text(x0 - 6, py(s) + 3, f'{s}s.', size=7, anchor='end')
    for y in (1312, 1315, 1318, 1321, 1324):
        d.text(px(y), y0 + 14, str(y), size=7)
    d.text(peak[0], peak[1] - 10, '15s. 11⅞d.', size=7)
    d.text((px(1314) + px(1316)) / 2, y1 - 6, 'WET SUMMERS', size=7)
    d.text((px(1319) + px(1320)) / 2, y1 - 6, 'CATTLE PLAGUE', size=7)
    d.text(px(1323), py(base) + 12, '1312–13 LEVEL', size=7)
    d.text((x0 + x1) / 2, 22, 'WHEAT IN ENGLAND · SHILLINGS A QUARTER · ROGERS 1866', size=7)
    d.text((x0 + x1) / 2, y0 + 30, 'YEARLY AVERAGES FROM MANORIAL ACCOUNTS', size=7)
    return d


def famine_1876():
    d = D()
    # The Provisional Famine Code of 1883 as a flow: the signs that are reported, the Commissioner's
    # report of scarcity, the register of the poor, and the three kinds of relief, with the code's
    # daily flour for a man under each (sections 2, 22-23, 107, 127-129). Below, the scale of those
    # rations against the Temple wage of 1877 (1 lb of grain), in ounces.
    d.group('thin')
    d.line((200, 6), (200, 22))                                           # centre line of the flow
    d.line((200, 176), (200, 196))
    for x in (66, 200, 334):
        d.line((x, 120), (x, 136))

    d.group()
    _box(d, 4, 22, 146, 34)                                               # signs
    _box(d, 250, 22, 146, 34)
    _box(d, 140, 66, 120, 30)                                             # report
    _box(d, 6, 136, 120, 40)                                              # relief
    _box(d, 140, 136, 120, 40)
    _box(d, 274, 136, 120, 40)

    d.group('mid')
    for p, q in (((150, 46), (170, 66)), ((250, 46), (230, 66)), ((200, 96), (200, 112))):
        d.line(p, q)
        _arrow(d, p, q, size=4)
    d.line((66, 120), (334, 120))
    for x in (66, 200, 334):
        _arrow(d, (x, 126), (x, 136), size=4)
    d.line((200, 112), (200, 120))

    d.group('mid')
    d.text(77, 36, 'VILLAGE OFFICER', size=7)
    d.text(77, 48, 'CROPS · GRAIN · CATTLE', size=7)
    d.text(323, 36, 'POLICE', size=7)
    d.text(323, 48, 'CRIME · WANDERING · DEATHS', size=7)
    d.text(200, 79, 'SCARCITY REPORTED', size=7)
    d.text(200, 90, 'REGISTER OF THE POOR', size=7)
    d.text(66, 150, 'RELIEF WORKS', size=7)
    d.text(66, 162, 'WAGE BUYS A RATION', size=7)
    d.text(200, 150, 'VILLAGE DOLE', size=7)
    d.text(200, 162, 'FOR THOSE UNFIT', size=7)
    d.text(334, 150, 'POOR-HOUSE', size=7)
    d.text(334, 162, 'FOR THOSE WHO REFUSE', size=7)

    # the ration scale: a man's daily flour or grain, in ounces, as bars from a common base
    bars = [('FULL', 24), ('MINIMUM', 16), ('TEMPLE 1877', 16), ('PENAL', 14)]
    bx0, by0 = 92, 286                                                    # 8.5 units an ounce
    d.group('thin')
    for oz in range(0, 25, 4):
        d.line((bx0 + oz * 8.5, 200), (bx0 + oz * 8.5, by0 - 8))

    d.group()
    for i, (name, oz) in enumerate(bars):
        y = 206 + i * 18
        _box(d, bx0, y, oz * 8.5, 10)

    d.group('mid')
    for i, (name, oz) in enumerate(bars):
        y = 206 + i * 18
        d.text(bx0 - 6, y + 8, name, size=7, anchor='end')
        d.text(bx0 + oz * 8.5 + 6, y + 8, f'{oz} OZ', size=7, anchor='start')
    d.text(200, by0 + 4, "A MAN'S DAILY FLOUR · FAMINE CODE 1883", size=7)
    return d


PLATES = {'great-famine-1315': great_famine_1315, 'famine-1876': famine_1876}
