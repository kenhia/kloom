"""Plates for Daily Bread's part trade1 (sprint 051): spice-routes, banda-nutmeg. See plates_for.py."""
import math
import random
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def spice_routes():
    d = D()
    # Left: the western Indian Ocean on an equirectangular grid, 5 units a degree, 30-80 E and 6 S-33 N.
    # Ports are placed from their coordinates (Wikipedia; Muziris at Pattanam, Guardafui, Ras Fartak and
    # Massawa from the standard gazetteer values). The coasts are schematic: straight runs between those
    # points, enough to show which water is which, not a chart.
    # Right: the year as a dial, one arrow a month for the wind over the Arabian Sea: south-west from June to
    # September, north-east from November to February, light and variable between (Pliny NH 6.26; Periplus 57).
    lon0, lat0, k = 30, 33, 5
    ox, oy = 14, 26

    def p(lat, lon):
        return (ox + (lon - lon0) * k, oy + (lat0 - lat) * k)

    d.group('thin')
    for lon in range(30, 81, 10):                                         # graticule
        d.line(p(33, lon), p(-6, lon))
    for lat in (30, 20, 10, 0):
        d.line(p(lat, 30), p(lat, 80))

    africa = [(29.97, 32.55), (23.91, 35.47), (15.61, 39.45), (12.58, 43.33), (11.59, 43.15),
              (11.82, 51.28), (2.04, 45.34), (-3.22, 40.13), (-6, 39.3)]
    arabia = [(29.97, 32.55), (21.54, 39.17), (12.58, 43.33), (12.8, 45.03), (14.03, 48.34),
              (15.63, 52.24), (22.52, 59.77), (23.59, 58.41), (27.07, 56.46), (24.86, 67.01),
              (20.72, 70.99), (19.08, 72.88), (15.5, 73.83), (11.25, 75.78), (10.15, 76.22),
              (8.09, 77.54), (9.5, 79.2), (13.0, 80.0)]
    egypt = [(31.2, 29.89), (31.4, 30.42), (30.04, 31.24), (29.97, 32.55)]
    d.group('mid')
    d.dashed(*[p(*q) for q in africa], dash=3, gap=2)
    d.dashed(*[p(*q) for q in arabia], dash=3, gap=2)
    d.dashed(*[p(*q) for q in egypt], dash=2, gap=2)                      # the Nile road, schematic

    berenice, ocelis, muziris = p(23.91, 35.47), p(12.77, 43.65), p(10.15, 76.22)
    malindi, calicut, anjediva = p(-3.22, 40.13), p(11.25, 75.78), p(14.76, 74.11)
    alexandria = p(31.2, 29.89)
    d.group()
    d.line(berenice, (berenice[0] + 18, berenice[1] + 26), ocelis)        # down the Red Sea
    out = [ocelis, (130, 112), muziris]                                   # across on the SW monsoon
    d.line(*out)
    _arrow(d, out[1], muziris, 6)
    d.line(malindi, calicut)                                              # da Gama, 24 April-18 May 1498
    _arrow(d, malindi, calicut, 6)

    d.group('mid')
    back = [anjediva, p(2.04, 45.34)]                                     # home, Oct 1498-Jan 1499
    d.dashed(*back, dash=4, gap=3)
    _arrow(d, back[0], back[1], 5)
    for q in (alexandria, berenice, ocelis, muziris, malindi, calicut):
        d.circle(*q, 2.4)

    # the wind dial
    cx, cy, r = 334, 122, 40
    d.group('thin')
    d.circle(cx, cy, r + 10)
    for m in range(12):
        a = math.radians(-90 + 30 * m)
        d.line((cx + (r + 6) * math.cos(a), cy + (r + 6) * math.sin(a)),
               (cx + (r + 14) * math.cos(a), cy + (r + 14) * math.sin(a)))
    d.group()
    d.circle(cx, cy, r + 10)
    wind = {5: 'sw', 6: 'sw', 7: 'sw', 8: 'sw', 10: 'ne', 11: 'ne', 0: 'ne', 1: 'ne'}
    d.group('mid')
    for m in range(12):
        a = math.radians(-90 + 30 * m + 15)
        mx, my = cx + (r - 13) * math.cos(a), cy + (r - 13) * math.sin(a)
        if m in wind:
            # an arrow of the wind's heading: SW monsoon blows toward the north-east, NE toward the south-west
            h = math.radians(-45) if wind[m] == 'sw' else math.radians(135)
            t = (mx + 7 * math.cos(h), my + 7 * math.sin(h))
            s = (mx - 7 * math.cos(h), my - 7 * math.sin(h))
            d.line(s, t)
            _arrow(d, s, t, 4)
        else:
            d.circle(mx, my, 1.5)

    d.group('mid')
    for m, name in enumerate('JFMAMJJASOND'):
        a = math.radians(-90 + 30 * m + 15)
        d.text(cx + (r + 22) * math.cos(a), cy + (r + 22) * math.sin(a) + 2.5, name, size=7)
    d.text(cx, cy + r + 40, 'WIND OVER THE', size=7)
    d.text(cx, cy + r + 50, 'ARABIAN SEA', size=7)
    d.text(cx, cy - 4, 'NE', size=7)
    d.text(cx, cy + 10, 'SW', size=7)
    d.text(p(31.2, 29.89)[0] + 6, p(31.2, 29.89)[1] - 4, 'ALEXANDRIA', size=7, anchor='start')
    d.text(berenice[0] + 6, berenice[1] + 3, 'BERENICE', size=7, anchor='start')
    d.text(ocelis[0] - 4, ocelis[1] + 11, 'OCELIS', size=7, anchor='end')
    d.text(muziris[0] - 4, muziris[1] + 14, 'MUZIRIS', size=7, anchor='end')
    d.text(calicut[0] + 4, calicut[1] - 8, 'CALICUT', size=7, anchor='start')
    d.text(malindi[0] + 5, malindi[1] + 10, 'MALINDI', size=7, anchor='start')
    d.text(130, 104, 'ROME · 40 DAYS', size=7)
    d.text(178, 184, 'OUT · 23 DAYS', size=7)
    d.text(116, 150, 'BACK ·', size=7)
    d.text(116, 159, '~3 MONTHS', size=7)
    d.text(140, 288, 'COASTS SCHEMATIC · 10° GRID', size=7)
    return d


def banda_nutmeg():
    d = D()
    # Left: a ripe nutmeg fruit, its husk (pericarp) split along the suture and opened to show the seed
    # wrapped in its red aril, the mace. Right: the seed cut through: the hard shell (testa) and the kernel,
    # the nutmeg, whose dark folds of seed coat run into the pale endosperm ("ruminate"). Proportions follow
    # the botanical descriptions (fruit 6-9 cm long; Miske 2025 after Rumphius); the mace's lacing and the
    # folds are drawn from a seeded pattern, not traced.
    rng = random.Random(7)
    fx, fy = 120, 150                                                     # fruit centre
    a, b = 70, 84                                                         # husk half-width, half-height

    def husk(t, s=1.0):
        # a slightly pear-shaped outline: wider below the middle
        x = a * s * math.cos(t) * (1 + 0.08 * math.sin(t))
        y = b * s * math.sin(t)
        return (fx + x, fy - y)

    d.group('thin')
    d.line((fx, fy - b - 18), (fx, fy + b + 14))                          # the suture's axis
    d.line((fx - a - 14, fy), (fx + a + 14, fy))
    sx, sy = 300, 150
    d.line((sx, sy - 76), (sx, sy + 76))
    d.line((sx - 66, sy), (sx + 66, sy))

    d.group()
    # the two halves of the husk, opened a little apart at the suture
    gap = 10
    left = [husk(math.radians(t)) for t in range(90, 271, 6)]
    right = [husk(math.radians(t)) for t in range(-90, 91, 6)]
    d.line(*[(x - gap, y) for x, y in left])
    d.line(*[(x + gap, y) for x, y in right])
    # husk thickness, the inner face
    inner_l = [husk(math.radians(t), 0.8) for t in range(100, 261, 8)]
    inner_r = [husk(math.radians(t), 0.8) for t in range(-80, 81, 8)]
    d.line(*[(x - gap, y) for x, y in inner_l])
    d.line(*[(x + gap, y) for x, y in inner_r])
    d.line((fx, fy - b - 6), (fx + 3, fy - b - 16))                       # stalk
    # the seed
    d.ellipse(fx, fy + 4, 34, 42)

    d.group('mid')
    # the mace: strands rising from the base of the seed and branching over it
    for i in range(9):
        t0 = -1.0 + 2.0 * i / 8
        pts = []
        for j in range(15):
            s = j / 14
            y = fy + 44 - 86 * s
            half = 34 * math.sqrt(max(0.0, 1 - ((y - fy - 4) / 42) ** 2))
            x = fx + half * t0 * (0.96 - 0.1 * s) + 3 * math.sin(6 * s + i)
            pts.append((x, y))
        d.line(*pts)

    d.group()
    # the seed in section: shell and kernel
    d.ellipse(sx, sy, 50, 62)
    d.ellipse(sx, sy, 44, 56)

    d.group('mid')
    # rumination: folds of the seed coat running in from the edge of the kernel
    for i in range(22):
        t = 2 * math.pi * i / 22 + rng.uniform(-0.08, 0.08)
        depth = rng.uniform(0.35, 0.8)
        pts = []
        for j in range(9):
            s = j / 8
            rr = 1 - depth * s
            w = 0.18 * math.sin(3 * s * math.pi) * s
            pts.append((sx + 44 * rr * math.cos(t + w), sy + 56 * rr * math.sin(t + w)))
        d.line(*pts)

    d.group('mid')
    d.line((fx - a - 24, fy - b), (fx - a - 24, fy + b))                  # a dimension line, 6-9 cm
    _arrow(d, (fx - a - 24, fy), (fx - a - 24, fy - b), 4)
    _arrow(d, (fx - a - 24, fy), (fx - a - 24, fy + b), 4)
    d.text(fx - a - 24, fy - b - 8, '6–9 CM', size=7)
    d.text(fx, 22, 'HUSK SPLIT · SEED IN ITS MACE', size=7)
    d.text(fx + a + 4, fy - b + 6, 'HUSK', size=7, anchor='start')
    d.text(fx + 40, fy + 66, 'MACE', size=7, anchor='start')
    d.text(sx, 22, 'SEED IN SECTION', size=7)
    d.text(sx + 54, sy - 54, 'SHELL', size=7, anchor='start')
    d.text(sx, sy + 82, 'NUTMEG · THE KERNEL', size=7)
    d.text(200, 288, 'MYRISTICA FRAGRANS', size=7)
    return d


PLATES = {'spice-routes': spice_routes, 'banda-nutmeg': banda_nutmeg}
