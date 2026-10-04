"""Plates for western-civ's part ind2 (sprint 049): unification, scramble-for-africa. See plates_for.py."""
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


def unification():
    d = D()
    # The Hall of Mirrors at Versailles, where the German Empire was proclaimed on 18 January 1871
    # (and the 1919 treaty signed). Top: plan, to scale: 73 m long, 10.5 m deep, 17 windows on the
    # garden side facing 17 mirrored arcades, the Salon of War at the north end and the Salon of Peace
    # at the south (drawn as squares the gallery's depth: schematic). Bottom: the mirror wall in
    # elevation, 12.3 m high, its 17 round-headed arcades on the same bays.
    s = 260 / 73                                   # units per meter
    x0, x1 = 70, 70 + 73 * s
    depth = 10.5 * s
    py0 = 70                                       # plan: garden wall
    py1 = py0 + depth                              # plan: mirror wall
    bay = 73 * s / 17
    sal = depth                                    # the salons, schematic squares

    ey1 = 262                                      # elevation: floor
    ey0 = ey1 - 12.3 * s                           # elevation: top of the vault
    cornice = ey1 - 8.6 * s

    d.group('thin')
    d.line((x0 - sal - 8, (py0 + py1) / 2), (x1 + sal + 8, (py0 + py1) / 2))    # the long axis
    for i in range(18):                                                      # the bays, plan to elevation
        x = x0 + i * bay
        d.line((x, py1 + 22), (x, ey1))
    d.line((x0, py0 - 16), (x1, py0 - 16))                                   # 73 m, dimensioned
    for x in (x0, x1):
        d.line((x, py0 - 20), (x, py0 - 12))
    d.line((x1 + sal + 8, py0), (x1 + sal + 8, py1))                         # 10.5 m
    for y in (py0, py1):
        d.line((x1 + sal + 4, y), (x1 + sal + 12, y))
    d.line((x0 - 10, ey0), (x0 - 10, ey1))                                   # 12.3 m
    for y in (ey0, ey1):
        d.line((x0 - 14, y), (x0 - 6, y))

    d.group()
    # the plan: the garden wall broken by 17 windows, the mirror wall solid; the salons at the ends
    w = bay * 0.5
    for i in range(17):
        xa = x0 + i * bay
        xc = xa + bay / 2
        d.line((xa, py0), (xc - w / 2, py0))
        d.line((xc + w / 2, py0), (xa + bay, py0))
    d.line((x0, py1), (x1, py1))
    _box(d, x0 - sal, py0, sal, sal)
    _box(d, x1, py0, sal, sal)
    # the elevation: floor, cornice and the curve of the vault
    d.line((x0, ey1), (x1, ey1))
    d.line((x0, cornice), (x1, cornice))
    d.line((x0, ey1), (x0, cornice))
    d.line((x1, ey1), (x1, cornice))
    d.line((x0, cornice), (x0 + 6, ey0), (x1 - 6, ey0), (x1, cornice))

    d.group('mid')
    # the mirrored arcades in plan (shallow recesses) and in elevation (round-headed panels)
    for i in range(17):
        xc = x0 + (i + 0.5) * bay
        hw = bay * 0.3
        d.line((xc - hw, py1), (xc - hw, py1 + 3), (xc + hw, py1 + 3), (xc + hw, py1))
        spring = cornice + hw + 3
        pts = [(xc - hw, ey1 - 2), (xc - hw, spring)]
        pts += [(xc + hw * math.cos(math.radians(a)), spring - hw * math.sin(math.radians(a)))
                for a in range(180, -1, -15)]
        pts += [(xc + hw, ey1 - 2)]
        d.line(*pts)
        # the panes: three rows across each arcade
        for k in (1, 2, 3):
            y = ey1 - 2 - (ey1 - 2 - spring) * k / 4
            d.line((xc - hw, y), (xc + hw, y))

    d.group('mid')
    d.text((x0 + x1) / 2, py0 - 20, '73 M', size=7)
    d.text(x1 + sal + 12, (py0 + py1) / 2 + 2, '10.5', size=7, anchor='start')
    d.text(x0 - 14, (ey0 + ey1) / 2 + 2, '12.3', size=7, anchor='end')
    d.text((x0 + x1) / 2, py0 - 30, 'GARDEN · 17 WINDOWS', size=7)
    d.text((x0 + x1) / 2, py1 + 15, '17 MIRRORED ARCADES', size=7)
    d.text(x0 - sal / 2, py1 + 12, 'WAR', size=7)
    d.text(x1 + sal / 2, py1 + 12, 'PEACE', size=7)
    d.text((x0 + x1) / 2, ey1 + 16, 'HALL OF MIRRORS · 18 I 1871 · 28 VI 1919', size=7)
    return d


# Africa's coast as (longitude, latitude), clockwise from Tangier: a schematic outline through
# some sixty coastal points, projected equirectangularly. Madagascar apart.
_COAST = [
    (-5.8, 35.8), (-2.0, 35.1), (3.0, 36.8), (9.8, 37.3), (11.0, 37.0), (10.6, 35.8), (10.1, 34.0),
    (11.1, 33.2), (13.2, 32.9), (15.2, 32.3), (19.6, 30.4), (20.1, 32.1), (22.6, 32.8), (25.1, 31.6),
    (29.9, 31.2), (32.3, 31.3), (32.5, 29.9), (33.8, 27.2), (35.5, 23.9), (37.2, 19.6), (39.5, 15.6),
    (43.3, 12.6), (43.1, 11.6), (45.0, 10.4), (51.3, 11.8), (51.0, 10.4), (48.5, 5.4), (45.3, 2.0),
    (42.5, -0.4), (39.7, -4.0), (39.3, -6.8), (40.2, -10.3), (40.7, -15.0), (36.9, -17.9), (34.8, -19.8),
    (35.4, -23.9), (32.6, -26.0), (32.4, -28.8), (31.0, -29.9), (27.9, -33.0), (25.6, -34.0),
    (20.0, -34.8), (18.5, -34.4), (18.4, -33.9), (18.1, -32.0), (16.5, -28.6), (15.1, -26.6),
    (14.5, -22.9), (11.8, -17.3), (12.2, -15.2), (13.4, -12.6), (13.2, -8.8), (12.3, -6.0),
    (11.8, -4.8), (8.7, -0.6), (9.4, 0.4), (9.9, 2.9), (9.7, 4.0), (8.5, 4.6), (6.0, 4.3), (4.5, 6.2),
    (3.4, 6.45), (1.2, 6.1), (-0.2, 5.55), (-2.0, 4.75), (-4.0, 5.2), (-7.6, 4.4), (-10.8, 6.3),
    (-13.2, 8.5), (-15.6, 11.9), (-16.8, 13.4), (-17.5, 14.7), (-16.5, 16.0), (-16.0, 18.1),
    (-17.05, 20.8), (-16.0, 23.7), (-14.5, 26.1), (-12.9, 27.9), (-9.6, 30.4), (-9.8, 31.5),
    (-7.6, 33.6), (-6.8, 34.0),
]
_MADAGASCAR = [
    (49.3, -12.0), (50.5, -15.5), (49.4, -17.8), (48.0, -22.0), (47.1, -24.9), (45.2, -25.6),
    (43.6, -23.4), (44.0, -20.0), (44.4, -16.2), (46.3, -15.7), (48.0, -13.5),
]


def _coast_x_at(lat, east=True):
    """Where the outline crosses a parallel, on its east (or west) side: interpolated."""
    best = None
    pts = _COAST + [_COAST[0]]
    for (a, b) in zip(pts, pts[1:]):
        if (a[1] - lat) * (b[1] - lat) <= 0 and a[1] != b[1]:
            lon = a[0] + (b[0] - a[0]) * (lat - a[1]) / (b[1] - a[1])
            if best is None or (lon > best if east else lon < best):
                best = lon
    return best


def scramble_for_africa():
    d = D()
    # Africa on its graticule, equirectangular, with three of the borders the powers drew along a
    # parallel or a meridian: Egypt and Sudan on 22 deg N (the condominium agreement of 1899), Egypt
    # and Libya on 25 deg E (1925), and German South West Africa's eastern edge on 20 deg E, from the
    # Orange River north to 22 deg S (the Heligoland-Zanzibar Treaty of 1890).
    k = 3.5                                                   # units per degree
    lon0, lat0 = -18, 37.5
    X = lambda lon: 34 + (lon - lon0) * k
    Y = lambda lat: 22 + (lat0 - lat) * k
    P = lambda p: (X(p[0]), Y(p[1]))

    d.group('thin')
    for lon in range(-10, 60, 10):                            # meridians every ten degrees
        d.line((X(lon), Y(37.5)), (X(lon), Y(-36)))
    for lat in range(-30, 40, 10):                            # parallels
        d.line((X(-18), Y(lat)), (X(53), Y(lat)))

    d.group()
    d.line(*[P(p) for p in _COAST], closed=True)
    d.line(*[P(p) for p in _MADAGASCAR], closed=True)

    d.group('mid')
    # 22 N from Gabal Uweinat (25 E) to the Red Sea
    d.line(P((25.0, 22.0)), P((_coast_x_at(22.0), 22.0)))
    # 25 E from 22 N north to about 29.5 N, where the line leaves the meridian for the coast at Sallum
    d.line(P((25.0, 22.0)), P((25.0, 29.5)), P((25.1, 31.6)))
    # 20 E from the Orange River north to 22 S
    d.line(P((20.0, -28.4)), P((20.0, -22.0)))
    for p in [(25.0, 22.0), (20.0, -28.4), (20.0, -22.0)]:
        d.circle(*P(p), 1.6)

    d.group('mid')
    d.text(X(29.5), Y(22.0) + 18, '22° N · 1899', size=7)
    d.text(X(25.0) - 4, Y(26.5), '25° E · 1925', size=7, anchor='end')
    d.text(X(20.0) - 5, Y(-25.5), '20° E · 1890', size=7, anchor='end')
    d.text(X(-18) - 3, Y(0) + 2.5, '0°', size=7, anchor='end')
    d.text(X(53) + 3, Y(30) + 2.5, '30° N', size=7, anchor='start')
    d.text(X(53) + 3, Y(-30) + 2.5, '30° S', size=7, anchor='start')
    d.text(330, 270, 'BORDERS ON', size=7)
    d.text(330, 281, 'THE GRATICULE', size=7)
    return d


PLATES = {'unification': unification, 'scramble-for-africa': scramble_for_africa}
