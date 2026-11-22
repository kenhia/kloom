"""Plates for The Cloud on the Ground's Water section, part water2 (sprint 059): dry places, small water
systems and zero-water cooling. See plates_for.py."""
import math
from plates import D

# The Central Arizona Project canal (Lake Havasu to its end south-west of Tucson) and the Colorado River
# below Lake Havasu, as (lon, lat): OpenStreetMap's ways (waterway=canal named "Central Arizona Project";
# waterway=river named "Colorado River"), fetched through the Overpass API on 2026-11-22, joined end to
# end and simplified (Douglas-Peucker, 0.008 degrees). OpenStreetMap data is (c) OpenStreetMap
# contributors, ODbL; the plate says so.
_CAP = [(-114.104, 34.289), (-114.04, 34.142), (-113.996, 34.072), (-113.936, 34.013), (-113.915, 33.952), (-113.864, 33.921), (-113.822, 33.919), (-113.831, 33.858), (-113.788, 33.761), (-113.642, 33.599), (-113.601, 33.611), (-113.548, 33.605), (-113.496, 33.568), (-113.423, 33.565), (-113.371, 33.586), (-113.169, 33.587), (-113.064, 33.533), (-112.907, 33.595), (-112.819, 33.591), (-112.712, 33.643), (-112.678, 33.675), (-112.576, 33.69), (-112.54, 33.724), (-112.486, 33.747), (-112.266, 33.784), (-112.222, 33.771), (-112.176, 33.734), (-112.116, 33.748), (-112.057, 33.694), (-112.001, 33.664), (-111.873, 33.627), (-111.854, 33.604), (-111.764, 33.549), (-111.721, 33.551), (-111.68, 33.502), (-111.675, 33.454), (-111.615, 33.417), (-111.538, 33.341), (-111.506, 33.231), (-111.43, 33.093), (-111.394, 33.077), (-111.335, 33.086), (-111.31, 33.076), (-111.388, 33.01), (-111.439, 32.934), (-111.444, 32.879), (-111.43, 32.822), (-111.401, 32.811), (-111.425, 32.758), (-111.414, 32.744), (-111.424, 32.708), (-111.401, 32.676), (-111.341, 32.667), (-111.33, 32.588), (-111.268, 32.587), (-111.244, 32.515), (-111.162, 32.434), (-111.167, 32.409), (-111.203, 32.406), (-111.192, 32.373), (-111.224, 32.357), (-111.256, 32.305), (-111.242, 32.3), (-111.244, 32.263), (-111.21, 32.242), (-111.167, 32.174), (-111.131, 32.162)]
_COLORADO = [(-114.487, 34.717), (-114.47, 34.711), (-114.451, 34.667), (-114.458, 34.657), (-114.424, 34.61), (-114.436, 34.593), (-114.381, 34.526), (-114.382, 34.451), (-114.331, 34.447), (-114.227, 34.365), (-114.183, 34.354), (-114.138, 34.305), (-114.131, 34.262), (-114.165, 34.259), (-114.225, 34.204), (-114.229, 34.187), (-114.29, 34.168), (-114.321, 34.139), (-114.42, 34.105), (-114.434, 34.087), (-114.439, 34.022), (-114.466, 34.011), (-114.458, 33.994), (-114.523, 33.955), (-114.535, 33.934), (-114.508, 33.904), (-114.526, 33.9), (-114.505, 33.866), (-114.531, 33.853), (-114.505, 33.761), (-114.512, 33.732), (-114.494, 33.711), (-114.531, 33.673), (-114.514, 33.658), (-114.533, 33.652), (-114.522, 33.612), (-114.542, 33.584), (-114.525, 33.553), (-114.591, 33.5), (-114.634, 33.423), (-114.693, 33.414), (-114.709, 33.397), (-114.699, 33.332), (-114.682, 33.314), (-114.667, 33.261), (-114.681, 33.239), (-114.68, 33.159), (-114.708, 33.094), (-114.689, 33.084), (-114.664, 33.034), (-114.645, 33.049), (-114.616, 33.027), (-114.574, 33.036), (-114.515, 33.026), (-114.493, 32.971), (-114.468, 32.97), (-114.481, 32.933), (-114.463, 32.902), (-114.49, 32.827), (-114.532, 32.793), (-114.527, 32.751), (-114.543, 32.725), (-114.592, 32.722), (-114.701, 32.746), (-114.72, 32.719)]


# Places, from their Wikipedia articles' coordinates (prop=coordinates), as (lon, lat).
_PLACES = {
    'PHOENIX': (-112.0739, 33.4483), 'MESA': (-111.8228, 33.4222), 'CHANDLER': (-111.8333, 33.3),
    'GOODYEAR': (-112.3665, 33.2540), 'EL MIRAGE': (-112.3244, 33.6131), 'TUCSON': (-110.9714, 32.2219),
    'LAKE HAVASU': (-114.3833, 34.4833),
}


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def dry_places():
    """The Central Arizona Project canal from the Colorado River to Tucson, in an equirectangular
    projection true at 33.3 degrees N, with the Phoenix-area cities that host data center campuses."""
    d = D()
    k = math.cos(math.radians(33.3))
    s = 100                                   # plate units per degree of latitude
    w0, n0 = -114.75, 34.65
    X = lambda lon: 22 + (lon - w0) * s * k
    Y = lambda lat: 18 + (n0 - lat) * s
    d.group('thin')
    for lat in (33, 34):                      # graticule
        d.dashed((X(-114.6), Y(lat)), (X(-110.7), Y(lat)), dash=2, gap=4)
    for lon in (-114, -113, -112, -111):
        d.dashed((X(lon), Y(34.6)), (X(lon), Y(32.05)), dash=2, gap=4)
    # scale bar: 50 km along the parallel of 32.3 degrees
    km = 50 / (111.32 * math.cos(math.radians(32.3)))
    bx, by = X(-114.5), Y(32.3)
    d.line((bx, by - 3), (bx, by), (bx + km * s * k, by), (bx + km * s * k, by - 3))
    # north arrow
    d.line((X(-110.85), Y(34.15)), (X(-110.85), Y(34.5)))
    _arrow(d, (X(-110.85), Y(34.3)), (X(-110.85), Y(34.5)), 5)

    d.group()
    d.line(*[(X(lo), Y(la)) for lo, la in _COLORADO])
    d.line(*[(X(lo), Y(la)) for lo, la in _CAP])

    d.group('mid')
    for name, (lo, la) in _PLACES.items():
        if name == 'LAKE HAVASU':
            d.ellipse(X(lo), Y(la), 5, 9)
        elif name == 'TUCSON':
            d.circle(X(lo), Y(la), 3.5)
        else:
            _box(d, X(lo) - 2.5, Y(la) - 2.5, 5, 5)

    d.group('labels')
    d.text(X(-114.3) + 8, Y(34.48) + 3, 'LAKE HAVASU', size=7, anchor='start')
    d.text(X(-114.62), Y(33.2), 'COLORADO R.', size=7, anchor='start')
    d.text(X(-113.35), Y(33.72), 'CAP CANAL', size=7)
    d.text(X(-112.07), Y(33.45) + 12, 'PHOENIX', size=7)
    d.text(X(-111.82) + 6, Y(33.42) - 6, 'MESA', size=7, anchor='start')
    d.text(X(-111.83) + 6, Y(33.3) + 8, 'CHANDLER', size=7, anchor='start')
    d.text(X(-112.37) - 6, Y(33.25) + 9, 'GOODYEAR', size=7, anchor='end')
    d.text(X(-112.32) - 6, Y(33.61) - 4, 'EL MIRAGE', size=7, anchor='end')
    d.text(X(-110.97) - 6, Y(32.22) + 12, 'TUCSON', size=7, anchor='end')
    d.text(bx + km * s * k / 2, by + 10, '50 KM', size=7)
    d.text(X(-110.85), Y(34.15) + 10, 'N', size=7)
    d.text(X(-110.7), Y(32.05) + 10, 'CANAL, RIVER: OPENSTREETMAP', size=7, anchor='end')
    return d


def small_water_systems():
    """A schematic, not any town's data: a summer of a town's daily water demand under its plant's capacity,
    and the same days with a campus's evaporative cooling added, which rises with the heat and crosses
    the ceiling on the hottest days. The curves are computed from invented seasonal terms."""
    d = D()
    x0, x1, yb, yt = 40, 372, 252, 40          # plot box: 122 days, June 1 to September 30
    days = 122
    X = lambda i: x0 + (x1 - x0) * i / (days - 1)
    Y = lambda v: yb - (yb - yt) * (v - 0.3) / 0.62   # the plotted range is 0.3 to 0.92 of a full scale

    def heat(i):                                # a smooth summer with two heat waves, 0..1
        season = math.sin(math.pi * i / (days - 1))
        waves = 0.35 * math.exp(-((i - 48) / 6) ** 2) + 0.45 * math.exp(-((i - 79) / 5) ** 2)
        wiggle = 0.06 * math.sin(i * 1.7) + 0.04 * math.sin(i * 0.63 + 1)
        return max(0.0, min(1.0, 0.55 * season + waves + wiggle))

    town = [0.42 + 0.22 * heat(i) for i in range(days)]
    campus = [0.03 + 0.20 * heat(i) ** 2 for i in range(days)]     # evaporation climbs faster than heat
    total = [a + b for a, b in zip(town, campus)]
    cap = 0.80

    d.group('thin')
    d.line((x0, yt - 8), (x0, yb), (x1 + 6, yb))                   # axes
    for m in (30, 61, 92):                                            # month boundaries
        d.line((X(m), yb), (X(m), yb + 4))
    for v in (0.4, 0.5, 0.6, 0.7):
        d.dashed((x0, Y(v)), (x1, Y(v)), dash=2, gap=4)

    d.group()
    d.line(*[(X(i), Y(v)) for i, v in enumerate(town)])
    d.line((x0, Y(cap)), (x1, Y(cap)))                               # the plant's capacity

    d.group('mid')
    d.dashed(*[(X(i), Y(v)) for i, v in enumerate(total)], dash=3, gap=2)
    for i in range(days):                                            # hot days over the ceiling
        if total[i] > cap:
            d.line((X(i), Y(cap)), (X(i), Y(total[i])))

    d.group('labels')
    d.text(x1, Y(cap) + 10, 'PLANT CAPACITY', size=7, anchor='end')
    d.text(X(6), Y(0.36), 'TOWN', size=7, anchor='start')
    d.text(X(6), Y(0.61), 'TOWN + CAMPUS', size=7, anchor='start')
    for m, name in ((15, 'JUN'), (45, 'JUL'), (76, 'AUG'), (107, 'SEP')):
        d.text(X(m), yb + 14, name, size=7)
    d.text(x0 + 4, yt - 10, 'DAILY DEMAND', size=7, anchor='start')
    d.text(x1, yt - 10, 'SCHEMATIC', size=7, anchor='end')
    return d


def _cold_plate(d, cx, y):
    """A chip on its board with a cold plate on it, in section: the plate's channels as a row of cells."""
    d.line((cx - 40, y + 22), (cx + 40, y + 22))                     # the board
    _box(d, cx - 16, y + 14, 32, 8)                                   # the chip
    _box(d, cx - 24, y, 48, 14)                                       # the cold plate
    for k in range(1, 6):
        d.line((cx - 24 + k * 8, y + 3), (cx - 24 + k * 8, y + 11))


def zero_water():
    """Two ways to reject the same chip's heat, in section. Left, the evaporative version: the cold
    plate's loop goes to a heat exchanger and a cooling tower, which takes in makeup water and loses
    vapor and blowdown. Right, the zero-water version: the same loop goes to a dry cooler on the roof,
    where fans pass air over finned coils, and no water line crosses the building's wall."""
    d = D()
    g, roof = 262, 150
    panels = ((18, 190), (210, 382))
    d.group('thin')
    d.line((8, g), (392, g))
    d.dashed((200, 24), (200, g + 10), dash=3, gap=4)                 # the divide between the two
    for (a, b) in panels:
        d.line((a, roof), (a, g))
        d.line((b, roof), (b, g))
        d.line((a, roof), (b, roof))

    d.group()
    for (a, b) in panels:
        _cold_plate(d, (a + b) / 2, 214)
    # left: a cooling tower on the roof, a trapezoid with a fan stack
    L = 104
    d.line((L - 38, roof), (L - 28, roof - 62), (L + 28, roof - 62), (L + 38, roof))
    _box(d, L - 18, roof - 74, 36, 12)
    # right: a dry cooler, two V-shaped coil banks on legs with fans along the top
    R = 296
    for cx in (R - 30, R + 30):
        d.line((cx - 24, roof - 60), (cx, roof - 14), (cx + 24, roof - 60))
        d.line((cx - 24, roof - 60), (cx + 24, roof - 60))
        d.line((cx - 10, roof - 14), (cx - 10, roof))
        d.line((cx + 10, roof - 14), (cx + 10, roof))

    d.group('mid')
    # the closed loops: supply and return from the cold plate up to the roof plant
    for (a, b), top in ((panels[0], roof - 6), (panels[1], roof - 14)):
        cx = (a + b) / 2
        d.line((cx - 20, 214), (cx - 20, 186), (cx - 50, 186), (cx - 50, top))
        d.line((cx + 20, 214), (cx + 20, 194), (cx + 50, 194), (cx + 50, top))
        _arrow(d, (cx + 50, top + 16), (cx + 50, top + 4), 4)
        _arrow(d, (cx - 50, top + 4), (cx - 50, top + 16), 4)
    # tower fill as hatching, its fan, and vapor leaving
    for k in range(5):
        y = roof - 50 + k * 9
        d.line((L - 30 + k * 1.6, y), (L + 30 - k * 1.6, y))
    d.circle(L, roof - 80, 6)
    for k in (-10, 0, 10):
        d.curve(f'M{L + k} {roof - 90} q 4 -6 0 -12 q -4 -6 0 -12')
    # makeup water in from the ground, blowdown out to the drain
    d.dashed((20, g - 8), (L - 46, g - 8), (L - 46, roof + 10), (L - 36, roof - 2), dash=4, gap=3)
    _arrow(d, (L - 44, roof + 2), (L - 36, roof - 2), 4)
    d.dashed((L + 36, roof + 2), (L + 60, roof + 24), (L + 60, g - 8), (188, g - 8), dash=4, gap=3)
    _arrow(d, (178, g - 8), (188, g - 8), 4)
    # dry cooler: fans on top and air passing through the coils
    for cx in (R - 30, R + 30):
        d.circle(cx, roof - 66, 6)
        d.line((cx, roof - 76), (cx, roof - 98))
        _arrow(d, (cx, roof - 88), (cx, roof - 98), 4)
        d.line((cx - 40, roof - 36), (cx - 22, roof - 36))
        _arrow(d, (cx - 30, roof - 36), (cx - 22, roof - 36), 4)

    d.group('labels')
    d.text(104, 18, 'EVAPORATIVE', size=7)
    d.text(296, 18, 'ZERO-WATER', size=7)
    d.text(L + 26, roof - 98, 'VAPOR', size=7, anchor='start')
    d.text(L - 42, roof - 30, 'TOWER', size=7, anchor='end')
    d.text(R, roof - 106, 'DRY COOLER', size=7)
    d.text(30, g + 12, 'MAKEUP WATER', size=7, anchor='start')
    d.text(188, g + 12, 'BLOWDOWN', size=7, anchor='end')
    d.text(296, 248, 'COLD PLATE ON CHIP', size=7)
    d.text(104, 248, 'COLD PLATE ON CHIP', size=7)
    d.text(R, g + 12, 'NO WATER IN OR OUT', size=7)
    return d


PLATES = {'dry-places': dry_places, 'small-water-systems': small_water_systems, 'zero-water': zero_water}
