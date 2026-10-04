"""Plates for western-civ's part ref1 (sprint 049): valladolid, westphalia. See plates_for.py."""
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


def valladolid():
    """The population of the Americas in 1492, as scholars have estimated it, on a log scale, and below
    it the loss within a century on a linear one. Totals from the estimates table in Wikipedia's
    "Population history of the Indigenous peoples of the Americas" (Kroeber, Rosenblat, Dobyns,
    Denevan) and from Koch et al. 2019 (60.5 million, interquartile range 44.8-78.2; 90 percent lost
    within a century, so about 6 million by 1600)."""
    d = D()
    x0, x1 = 120, 380                       # the log axis, 5 to 150 million
    lo, hi = math.log10(5), math.log10(150)

    def X(m):
        return x0 + (x1 - x0) * (math.log10(m) - lo) / (hi - lo)

    rows = [  # label, low, high (high None for a single figure), central figure
        ('KROEBER 1939', 8.4, None, 8.4),
        ('ROSENBLAT 1954', 13.38, None, 13.38),
        ('DOBYNS 1966', 90.04, 112.55, None),
        ('DENEVAN 1992', 53.9, None, 53.9),
        ('KOCH 2019', 44.8, 78.2, 60.5),
    ]
    ys = [40 + 28 * i for i in range(len(rows))]
    axis_y = ys[-1] + 24

    d.group('thin')
    for m in (5, 10, 20, 50, 100, 150):                                    # gridlines
        d.line((X(m), ys[0] - 14), (X(m), axis_y))
    for y in ys:                                                           # each estimate's line
        d.line((x0, y), (x1, y))
    # the linear scale for the loss, 0 to 60.5 million across the same width
    by0, by1 = 232, 262
    d.line((x0, by0 - 12), (x0, by1 + 10))
    for m in range(0, 61, 10):
        x = x0 + (x1 - x0) * m / 65
        d.line((x, by1 + 6), (x, by1 + 10))
    d.line((x0, by1 + 8), (x0 + (x1 - x0) * 60 / 65, by1 + 8))

    d.group()
    d.line((x0, axis_y), (x1, axis_y))                                     # the log axis
    for m in (5, 10, 20, 50, 100, 150):
        d.line((X(m), axis_y), (X(m), axis_y + 5))
    for (label, a, b, c), y in zip(rows, ys):
        if b is not None:                                                  # a range, capped
            d.line((X(a), y), (X(b), y))
            d.line((X(a), y - 5), (X(a), y + 5))
            d.line((X(b), y - 5), (X(b), y + 5))
        if c is not None:
            d.circle(X(c), y, 3.2)
    # the loss: the 1492 figure and what was left by 1600, to one linear scale
    w = x1 - x0
    _box(d, x0, by0 - 6, w * 60.5 / 65, 10)
    _box(d, x0, by1 - 10, w * 6.05 / 65, 10)

    d.group('mid')
    for i in range(1, 9):                                                  # the lost nine tenths, hatched
        x = x0 + w * 6.05 / 65 + (w * 60.5 / 65 - w * 6.05 / 65) * i / 9
        d.line((x, by0 - 6), (x, by0 + 4))
    d.line((x0 + w * 6.05 / 65, by0 + 4), (x0 + w * 6.05 / 65, by1 - 10))

    d.group('mid')
    for (label, *_), y in zip(rows, ys):
        d.text(x0 - 8, y + 2.5, label, size=7, anchor='end')
    for m, s in ((5, '5'), (10, '10'), (20, '20'), (50, '50'), (100, '100'), (150, '150')):
        d.text(X(m), axis_y + 14, s, size=7)
    d.text(x0 - 8, by0 + 2, '1492', size=7, anchor='end')
    d.text(x0 - 8, by1 - 3, 'BY 1600', size=7, anchor='end')
    d.text(x0 + w * 60.5 / 65 + 4, by0 + 2, '60.5 M', size=7, anchor='start')
    d.text(x0 + w * 6.05 / 65 + 4, by1 - 3, '6 M', size=7, anchor='start')
    d.text(x0 - 8, by1 + 10, '0', size=7, anchor='end')
    d.text(250, 18, 'THE AMERICAS IN 1492 · MILLIONS', size=7)
    return d


def westphalia():
    """The two congress towns on their true bearing, to scale (2.2 units a kilometer), each with its
    demilitarized ring, and beside each the parties that negotiated there: at Munster the emperor and
    France through the papal nuncio and the Venetian envoy, and Spain with the Dutch; at Osnabruck the
    emperor and Sweden face to face, with the Empire's estates. Coordinates of the town centers from
    their Wikipedia articles; the straight-line distance, about 46 km, is our arithmetic."""
    d = D()
    k = 2.2                                                                # units per kilometer
    ms = (51.9625, 7.6256)                                                 # Munster
    os_ = (52.2833, 8.05)                                                   # Osnabruck
    mx, my = 175, 210
    coslat = math.cos(math.radians((ms[0] + os_[0]) / 2))

    def P(lat, lon):
        return (mx + (lon - ms[1]) * 111.32 * coslat * k, my - (lat - ms[0]) * 111.2 * k)

    M, O = P(*ms), P(*os_)

    d.group('thin')
    for lat in (52.0, 52.25):                                              # graticule
        y = P(lat, 0)[1]
        d.line((150, y), (300, y))
    for lon in (7.75, 8.0):
        x = P(0, lon)[0]
        d.line((x, 90), (x, 240))
    for c in (M, O):                                                       # demilitarized rings
        d.circle(c[0], c[1], 12)
    d.line((250, 262), (250 + 20 * k, 262))                                # a 20 km scale
    for x in (250, 250 + 10 * k, 250 + 20 * k):
        d.line((x, 259), (x, 265))
    d.line((40, 70), (40, 40))                                             # north
    _arrow(d, (40, 70), (40, 40))

    d.group()
    d.line(M, O)                                                           # the road between them
    d.circle(M[0], M[1], 5)
    d.circle(O[0], O[1], 5)

    d.group('mid')
    # Munster's congress, left of the town
    _box(d, 10, 138, 136, 96)
    d.line((146, 200), (M[0] - 12, M[1]))
    emp, fra, med = (15, 150, 46, 16), (95, 150, 46, 16), (38, 180, 80, 16)
    spa, dut = (15, 210, 46, 16), (95, 210, 46, 16)
    for b in (emp, fra, med, spa, dut):
        _box(d, *b)
    for b in (emp, fra):
        p = (b[0] + b[2] / 2, b[1] + b[3])
        q = (med[0] + med[2] / 2 + (-14 if b is emp else 14), med[1])
        d.line(p, q)
        _arrow(d, p, q, 4)
    d.line((61, 218), (95, 218))
    # Osnabruck's congress, right of the town
    _box(d, 258, 40, 134, 76)
    d.line((258, 100), (O[0] + 12, O[1]))
    emp2, swe, est = (266, 52, 46, 16), (338, 52, 46, 16), (300, 88, 52, 16)
    for b in (emp2, swe, est):
        _box(d, *b)
    d.line((312, 60), (338, 60))
    _arrow(d, (325, 60), (312, 60), 4)
    _arrow(d, (325, 60), (338, 60), 4)
    d.line((289, 68), (314, 88))
    d.line((361, 68), (338, 88))

    d.group('mid')
    for (x, y, w, h), s in ((emp, 'EMPEROR'), (fra, 'FRANCE'), (med, 'NUNCIO · VENICE'), (spa, 'SPAIN'),
                            (dut, 'DUTCH'), (emp2, 'EMPEROR'), (swe, 'SWEDEN'), (est, 'ESTATES')):
        d.text(x + w / 2, y + h / 2 + 2.5, s, size=7)
    d.text(M[0] + 16, M[1] + 16, 'MÜNSTER', size=7, anchor='start')
    d.text(O[0] - 16, O[1] - 14, 'OSNABRÜCK', size=7, anchor='end')
    mid = ((M[0] + O[0]) / 2, (M[1] + O[1]) / 2)
    d.text(mid[0] + 8, mid[1] + 4, '46 KM', size=7, anchor='start')
    d.text(250 + 10 * k, 276, '20 KM', size=7)
    d.text(40, 32, 'N', size=7)
    return d


PLATES = {'valladolid': valladolid, 'westphalia': westphalia}
