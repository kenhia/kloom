"""Plates for western-civ's ancient-world frames of part ant2 (sprint 049): augustus, socrates, alexander.
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


def augustus():
    """The principate as a chart of powers against time, 31 BC to AD 14.

    One row per power, from Res Gestae 4-7, 34-35 and the Wikipedia article on Augustus: the consulship
    held every year 31-23 BC and again in 5 and 2 BC; the command of the provinces from January 27 BC;
    the greater command and the tribune's power from 23 BC, the second divided into its 37 annual
    renewals (Res Gestae 4: "the thirty-seventh year of my tribunician power"); first man of the Senate
    by 27 BC; pontifex maximus from 6 March 12 BC; Father of his Country from 5 February 2 BC.
    There is no year 0, so AD 1 follows 1 BC.
    """
    d = D()
    x0, x1 = 112, 384

    def t(year):                                                          # signed year -> continuous time
        return year if year < 0 else year - 1

    T0, T1 = t(-31), t(14) + 1                                            # from the start of 31 BC to the end of AD 14
    X = lambda year, frac=0.0: x0 + (t(year) + frac - T0) * (x1 - x0) / (T1 - T0)
    END = X(14, 0.63)                                                     # 19 August AD 14
    rows = ['CONSUL', 'PROVINCES', 'GREATER COMMAND', 'TRIBUNE', 'FIRST SENATOR', 'PONTIFEX', 'FATHER']
    y0, dy, h = 46, 29, 9
    Y = lambda i: y0 + i * dy
    axis_y = Y(len(rows) - 1) + 30

    d.group('thin')
    for x in [X(yr) for yr in (-31, -27, -23, -12, -2)] + [END]:        # the dates that change the shape of power
        d.line((x, y0 - 14), (x, axis_y))
    for i in range(len(rows)):                                            # each row's baseline
        d.line((x0, Y(i) + h / 2), (x1, Y(i) + h / 2))
    d.line((x0, axis_y), (x1, axis_y))                                    # the time axis, a tick every five years
    for yr in range(-30, 15, 5):
        if yr == 0:
            continue
        d.line((X(yr), axis_y), (X(yr), axis_y + 4))

    d.group()
    # consulships: one box a year, 31-23 BC, then 5 and 2 BC
    for yr in list(range(-31, -22)) + [-5, -2]:
        _box(d, X(yr) + 0.6, Y(0), X(yr, 1) - X(yr) - 1.2, h)
    # the long powers, each a bar from its grant to his death
    for i, yr in ((1, -27), (2, -23), (4, -27), (5, -12)):
        _box(d, X(yr), Y(i), END - X(yr), h)
    _box(d, X(-23), Y(3), END - X(-23), h)                           # the tribune's power
    # Father of his Country: a title, drawn as a diamond on its date
    cx, cy = X(-2, 0.1), Y(6) + h / 2
    d.line((cx, cy - 6), (cx + 6, cy), (cx, cy + 6), (cx - 6, cy), closed=True)

    d.group('mid')
    for k in range(1, 37):                                                # the 37 annual renewals of the tribune's power
        x = X(-23) + k * (END - X(-23)) / 37
        d.line((x, Y(3) + 1.5), (x, Y(3) + h - 1.5))
    for i, yr in ((1, -27), (2, -23), (4, -27), (5, -12), (3, -23)):       # the grants, as arrows into each bar
        _arrow(d, (X(yr), Y(i) - 9), (X(yr), Y(i) - 1), size=3.5)
        d.line((X(yr), Y(i) - 9), (X(yr), Y(i) - 1))

    d.group('mid')
    for i, s in enumerate(rows):
        d.text(x0 - 8, Y(i) + 7, s, size=7, anchor='end')
    for yr, s in ((-31, '31 BC'), (-27, '27'), (-23, '23'), (-12, '12'), (-2, '2 BC'), (14, 'AD 14')):
        d.text(END if yr == 14 else X(yr), axis_y + 14, s, size=7)
    d.text(X(-31), y0 - 18, 'ACTIUM', size=7)
    d.text(END, y0 - 18, 'DEATH', size=7)
    d.text(x0 + (x1 - x0) / 2, axis_y + 28, 'THE PRINCIPATE · POWERS BY YEAR', size=7)
    return d


PLATES = {'augustus': augustus}


def _pebbles(d, x, y_base, n, cols, pitch, r):
    """n pebbles stacked from y_base upward, `cols` to a row, as one path."""
    parts = []
    for k in range(n):
        cx = x + (k % cols + 0.5) * pitch
        cy = y_base - (k // cols + 0.5) * pitch
        parts.append(f'M{cx - r:.1f} {cy:.1f} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0')
    d.curve(' '.join(parts))


def socrates():
    """The two votes at the trial of Socrates, one pebble a juror, on a jury of 500.

    First vote: Apology 36a, "had thirty votes gone over to the other side, I should have been acquitted",
    which on a jury of 500 is 280 to 220. Second vote: Diogenes Laertius 2.42, death "with an accession of
    eighty fresh votes", so 360 to 140 by our arithmetic. The jury's size is not given in either source;
    500 (or 501) is the usual reading. A line in each pair marks the 251 votes a majority needed.
    """
    d = D()
    pitch, cols, r = 4.2, 14, 1.25
    w = cols * pitch
    base = 238
    urns = [(34, 280, 'GUILTY'), (102, 220, 'ACQUIT'), (238, 360, 'DEATH'), (306, 140, 'FINE')]
    maj_y = base - (251 / cols) * pitch

    d.group('thin')
    d.line((20, base), (190, base))                                       # each vote's floor
    d.line((224, base), (380, base))
    for x0, x1 in ((24, 186), (228, 376)):                                # the majority, 251 of 500
        d.line((x0, maj_y), (x1, maj_y))
    for x, n, _ in urns:                                                  # each column's height, ticked every 50
        for k in range(50, n + 1, 50):
            y = base - (k / cols) * pitch
            d.line((x - 6, y), (x - 3, y))

    d.group()
    for x, n, _ in urns:                                                  # the urns, open at the top
        top = base - (n / cols) * pitch - 6
        d.line((x - 2, top), (x - 2, base + 2), (x + w + 2, base + 2), (x + w + 2, top))

    d.group('mid')
    for x, n, _ in urns:
        _pebbles(d, x, base, n, cols, pitch, r)

    d.group('mid')
    for x, n, s in urns:
        d.text(x + w / 2, base + 16, s, size=7)
        d.text(x + w / 2, base + 27, str(n), size=7)
    d.text(105, 112, 'FIRST VOTE · THE VERDICT', size=7)
    d.text(302, 112, 'SECOND VOTE · THE PENALTY', size=7)
    d.text(207, maj_y - 4, '251', size=7)
    d.text(200, 286, 'ONE PEBBLE A JUROR · JURY OF 500', size=7)
    return d


PLATES['socrates'] = socrates


# Alexander's route through its main stations, from the coordinates Wikipedia gives each site (fetched
# 2026-10-03). Patala, whose site is unknown, is placed at Hyderabad, Sindh, one proposed site; Pura, in
# Gedrosia, at Bampur; the Hyphasis at the Beas's confluence. The legs are great circles; by our arithmetic
# they add up to about 14,500 km, far less than the roads the army marched.
ROUTE = [
    ('PELLA', 40.7547, 22.5211), ('GRANICUS', 40.3167, 27.2811), ('ISSUS', 36.7525, 36.1923),
    ('TYRE', 33.2708, 35.1961), ('MEMPHIS', 29.8497, 31.2543), ('ALEXANDRIA', 31.1975, 29.8925),
    ('SIWA', 29.2053, 25.5194), ('MEMPHIS', 29.8497, 31.2543), ('TYRE', 33.2708, 35.1961),
    ('GAUGAMELA', 36.56, 43.44), ('BABYLON', 32.5425, 44.4211), ('SUSA', 32.1906, 48.2578),
    ('PERSEPOLIS', 29.935, 52.89), ('ECBATANA', 34.8064, 48.5161), ('BACTRA', 36.7581, 66.8981),
    ('MARACANDA', 39.6506, 66.9653), ('ESCHATE', 40.2794, 69.6319), ('BACTRA', 36.7581, 66.8981),
    ('TAXILA', 33.7458, 72.7875), ('HYDASPES', 32.8278, 73.6389), ('HYPHASIS', 31.1544, 74.9753),
    ('HYDASPES', 32.8278, 73.6389), ('PATALA', 25.39, 68.37), ('PURA', 27.195, 60.4547),
    ('PERSEPOLIS', 29.935, 52.89), ('SUSA', 32.1906, 48.2578), ('ECBATANA', 34.8064, 48.5161),
    ('BABYLON', 32.5425, 44.4211),
]


def _gc_km(a, b):
    """Great-circle distance in kilometers between two (name, lat, lon) stations."""
    p1, l1, p2, l2 = map(math.radians, (a[1], a[2], b[1], b[2]))
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin((l2 - l1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def alexander():
    """Alexander's march, 334-323 BC: the route on a grid of longitude and latitude, and below it the
    same route unrolled as a strip of kilometers, with the battles marked where they fall."""
    d = D()
    lon0, lon1, lat0, lat1 = 20, 78, 24, 42
    kx = 368 / (lon1 - lon0)
    ky = kx / math.cos(math.radians(33))                                  # equal scale at 33 degrees north
    P = lambda lat, lon: (16 + (lon - lon0) * kx, 48 + (lat1 - lat) * ky)
    legs = [_gc_km(a, b) for a, b in zip(ROUTE, ROUTE[1:])]
    total = sum(legs)
    sx0, sx1, sy = 16, 384, 240
    S = lambda km: sx0 + km * (sx1 - sx0) / total

    d.group('thin')
    for lon in range(20, 80, 10):                                         # the graticule
        d.line(P(lat0, lon), P(lat1, lon))
    for lat in range(25, 45, 5):
        d.line(P(lat, lon0), P(lat, lon1))
    d.line((sx0, sy), (sx1, sy))                                          # the strip's axis, every 2,000 km
    for km in range(0, int(total) + 1, 2000):
        d.line((S(km), sy), (S(km), sy + 4))

    d.group()
    d.line(*[P(lat, lon) for _, lat, lon in ROUTE])

    d.group('mid')
    seen = set()
    for name, lat, lon in ROUTE:
        if name not in seen:
            seen.add(name)
            x, y = P(lat, lon)
            d.circle(x, y, 1.8)
    run = 0.0                                                             # each station on the strip
    for (name, _, _), leg in zip(ROUTE[1:], legs):
        run += leg
        d.line((S(run), sy - 4), (S(run), sy))
    d.line((sx0, sy - 4), (sx0, sy + 4))

    d.group('mid')
    for name, dx, dy, anchor in (('PELLA', -4, -6, 'end'), ('ALEXANDRIA', -3, -7, 'end'), ('BABYLON', 0, 13, 'middle'),
                                 ('PERSEPOLIS', 4, 12, 'start'), ('BACTRA', 0, 14, 'middle'), ('HYDASPES', -3, 17, 'end')):
        lat, lon = next((la, lo) for n, la, lo in ROUTE if n == name)
        x, y = P(lat, lon)
        d.text(x + dx, y + dy, name, size=7, anchor=anchor)
    run, marks = 0.0, {'GRANICUS': '334', 'ISSUS': '333', 'GAUGAMELA': '331', 'HYDASPES': '326'}
    for (name, _, _), leg in zip(ROUTE[1:], legs):
        run += leg
        if name in marks:
            d.text(S(run), sy - 9, marks.pop(name), size=7)
    d.text(sx1, sy - 9, '323', size=7, anchor='end')
    d.text(sx0, sy + 14, '0', size=7, anchor='start')
    d.text(sx1, sy + 14, f'{round(total, -2):,.0f} KM', size=7, anchor='end')
    d.text(200, 274, 'THE ROUTE UNROLLED · STRAIGHT LEGS · BY OUR ARITHMETIC', size=7)
    return d


PLATES['alexander'] = alexander
