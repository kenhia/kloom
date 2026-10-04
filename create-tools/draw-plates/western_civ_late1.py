"""Plates for western-civ's late-antiquity frames written in sprint 049 (part late1). See plates_for.py."""
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


def early_christianity():
    d = D()
    # Paul's world on a latitude-longitude grid (an equirectangular projection, longitudes
    # shortened by cos 37 degrees, the map's middle latitude). City positions are their
    # coordinates; three letters whose places of writing are well attested are drawn as
    # arrows: 1 Thessalonians from Corinth (c. 49-51), 1 Corinthians from Ephesus (c. 53-54),
    # Romans from Corinth (c. 55-57). Jerusalem to Antioch is the movement's first step out.
    lon0, lon1, lat0, lat1 = 11.0, 38.0, 30.0, 44.0
    k = 352 / ((lon1 - lon0) * math.cos(math.radians(37)))
    x0, y0 = 24, 34

    def P(lat, lon):
        return (x0 + (lon - lon0) * k * math.cos(math.radians(37)), y0 + (lat1 - lat) * k)

    cities = {
        'ROME': (41.89, 12.49), 'CORINTH': (37.91, 22.88), 'THESSALONICA': (40.64, 22.94),
        'PHILIPPI': (41.01, 24.29), 'EPHESUS': (37.94, 27.34), 'TARSUS': (36.92, 34.89),
        'ANTIOCH': (36.20, 36.16), 'JERUSALEM': (31.78, 35.22),
    }

    d.group('thin')
    for lon in range(15, 38, 5):                                          # meridians every 5 degrees
        d.line(P(lat1, lon), P(lat0, lon))
    for lat in range(30, 45, 5):                                          # parallels every 5 degrees
        d.line(P(lat, lon0), P(lat, lon1))
    sx, sy = P(31.0, 12.0)                                                # 500 km scale: 4.5 degrees of latitude
    d.line((sx, sy), (sx + 4.5 * k, sy))
    for t in (0, 2.25, 4.5):
        d.line((sx + t * k, sy - 3), (sx + t * k, sy + 3))

    d.group()
    for name, (lat, lon) in cities.items():                               # the cities
        x, y = P(lat, lon)
        d.circle(x, y, 3.2)

    d.group('mid')
    def letter(a, b, bend):
        (ax, ay), (bx, by) = P(*cities[a]), P(*cities[b])
        mx, my = (ax + bx) / 2, (ay + by) / 2
        nx, ny = -(by - ay), bx - ax                                      # a gentle arc to one side
        n = math.hypot(nx, ny)
        cx, cy = mx + bend * nx / n, my + bend * ny / n
        pts = []
        for i in range(31):
            t = i / 30
            pts.append(((1 - t) ** 2 * ax + 2 * (1 - t) * t * cx + t * t * bx,
                        (1 - t) ** 2 * ay + 2 * (1 - t) * t * cy + t * t * by))
        # stop short of the city's circle
        while math.hypot(pts[-1][0] - bx, pts[-1][1] - by) < 6:
            pts.pop()
        d.line(*pts)
        _arrow(d, pts[-3], pts[-1], 5)
        return pts[len(pts) // 2]

    m_rom = letter('CORINTH', 'ROME', 22)
    m_cor = letter('EPHESUS', 'CORINTH', 14)
    m_th = letter('CORINTH', 'THESSALONICA', -16)
    # the first step out: Jerusalem to Antioch, dashed
    (jx, jy), (ax_, ay_) = P(*cities['JERUSALEM']), P(*cities['ANTIOCH'])
    n = 9
    for i in range(n):
        if i % 2 == 0:
            t0, t1 = i / n, (i + 1) / n
            d.line((jx + (ax_ - jx) * t0, jy + (ay_ - jy) * t0), (jx + (ax_ - jx) * t1, jy + (ay_ - jy) * t1))

    d.group('mid')
    offs = {'ROME': (0, -8, 'middle'), 'CORINTH': (-6, 12, 'end'), 'THESSALONICA': (-6, -6, 'end'),
            'PHILIPPI': (6, -6, 'start'), 'EPHESUS': (6, 10, 'start'), 'TARSUS': (-6, -6, 'end'),
            'ANTIOCH': (6, 3, 'start'), 'JERUSALEM': (6, 3, 'start')}
    for name, (lat, lon) in cities.items():
        x, y = P(lat, lon)
        dx, dy, anc = offs[name]
        d.text(x + dx, y + dy, name, size=7, anchor=anc)
    d.text(m_rom[0] - 2, m_rom[1] + 12, 'ROMANS', size=7)
    d.text(m_cor[0] + 12, m_cor[1] + 14, '1 COR', size=7)
    d.text(m_th[0] + 30, m_th[1] + 2, '1 THESS', size=7)
    d.text(sx + 2.25 * k, sy - 6, '500 KM', size=7)
    return d


def constantine():
    d = D()
    # Old St. Peter's in cross-section, schematic: five aisles under timber roofs, the nave
    # carried on king-post trusses. The nave's clear span, 23.7 m, is Ulrich's (Roman
    # Woodworking, 2007, via Wikipedia's list of ancient roofs); its roof stood about 30 m
    # high at the ridge. The aisles' widths and heights are not from a survey: the transept,
    # 63 m long, gives the whole width, and the two aisles each side share what the nave leaves.
    s = 4.6                                                               # units per meter
    cx, ground = 200, 266
    span, ridge, eave = 23.7, 30.0, 25.5
    aisle = (63 - span) / 4
    inner_hi, inner_lo = 18.0, 15.5
    outer_hi, outer_lo = 13.0, 10.5
    col_h = 9.5

    def X(m):
        return cx + m * s

    def Y(m):
        return ground - m * s

    hn = span / 2
    xs = [-hn - 2 * aisle, -hn - aisle, -hn, hn, hn + aisle, hn + 2 * aisle]

    d.group('thin')
    d.line((cx, Y(ridge) - 10), (cx, ground + 8))                         # the axis
    d.line((X(xs[0]) - 8, ground), (X(xs[-1]) + 8, ground))               # the ground
    yd = ground + 14                                                      # the span, dimensioned
    d.line((X(-hn), yd), (X(hn), yd))
    for x in (-hn, hn):
        d.line((X(x), yd - 4), (X(x), yd + 4))
    xh = X(xs[-1]) + 14                                                   # the height, dimensioned
    d.line((xh, ground), (xh, Y(ridge)))
    for y in (0, ridge):
        d.line((xh - 4, Y(y)), (xh + 4, Y(y)))
    d.line((X(hn), Y(ridge)), (xh, Y(ridge)))
    d.line((X(-hn - 3), Y(eave - 3 * (ridge - eave) / hn)), (cx, Y(ridge)), (X(hn + 3), Y(eave - 3 * (ridge - eave) / hn)))

    d.group()
    # the outline of the section: outer walls, stepped aisle roofs, clerestory, nave roof
    left = [(X(xs[0]), ground), (X(xs[0]), Y(outer_lo)), (X(xs[1]), Y(outer_hi)),
            (X(xs[1]), Y(inner_lo)), (X(xs[2]), Y(inner_hi)), (X(xs[2]), Y(eave)), (cx, Y(ridge))]
    right = [(2 * cx - x, y) for x, y in reversed(left[:-1])]
    d.line(*left, *right)

    d.group('mid')
    # the nave's king-post truss: tie beam, king post, struts
    d.line((X(-hn), Y(eave)), (X(hn), Y(eave)))
    d.line((cx, Y(eave)), (cx, Y(ridge)))
    for sgn in (-1, 1):
        d.line((cx, Y(eave)), (X(sgn * hn / 2), Y(eave + (ridge - eave) / 2)))
    # the aisle rafters' ties
    for a, b, hi in ((xs[0], xs[1], outer_lo), (xs[1], xs[2], inner_lo)):
        for sgn in (1, -1):
            d.line((X(sgn * a), Y(hi)), (X(sgn * b), Y(hi)))
    # columns on the four colonnades, with an entablature over the nave's
    for x in (xs[1], xs[2], xs[3], xs[4]):
        d.line((X(x), ground), (X(x), Y(col_h)))
        d.line((X(x) - 3, Y(col_h)), (X(x) + 3, Y(col_h)))
        d.line((X(x) - 3, ground), (X(x) + 3, ground - 0))
    for x in (xs[2], xs[3]):                                              # nave walls above the columns
        d.line((X(x), Y(col_h)), (X(x), Y(inner_hi)))
    for x in (xs[2], xs[3]):                                              # clerestory windows
        _box(d, X(x) - 2, Y(eave - 1.5), 4, 3.0 * s)
    # the apse at the far end, seen through the nave: a half-round arch
    d.arc(cx, Y(8), 7 * s, 180, 360, n=36)
    d.line((cx - 7 * s, Y(8)), (cx - 7 * s, ground))
    d.line((cx + 7 * s, Y(8)), (cx + 7 * s, ground))

    d.group('mid')
    d.text(cx, yd + 12, 'NAVE · TRUSS SPAN 23.7 M', size=7)
    d.text(xh + 4, Y(ridge / 2), '≈30 M', size=7, anchor='start')
    d.text(X(-hn - aisle), Y(outer_hi) - 18, 'AISLES', size=7)
    d.text(cx, 18, "OLD ST. PETER'S · SECTION", size=7)
    return d


PLATES = {'early-christianity': early_christianity, 'constantine': constantine}
