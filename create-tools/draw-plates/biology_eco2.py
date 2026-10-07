"""Plates for The Story of Life's part eco2 (food-chain, silent-spring), sprint 055. See plates_for.py."""
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


def _hatch(d, x0, x1, y0, y1, step=6):
    """Diagonal hatching inside a box, for energy lost as heat."""
    segs = []
    h = y1 - y0
    k = x0 - h
    while k < x1:
        a = (max(k, x0), y1 - (max(k, x0) - k))
        b = (min(k + h, x1), y1 - (min(k + h, x1) - k))
        if b[0] > a[0]:
            segs.append([a, b])
        k += step
    d.lines(segs)


def food_chain():
    d = D()
    # Lindeman's Cedar Bog Lake (Ecology 23, 1942, table II), in g-cal per cm2 per year, drawn to one
    # linear scale. Each level's total is split into what it grew, burned in respiration, lost to decay,
    # and had eaten by the level above; the eaten part is exactly the next level's income, so each bar
    # stands on the eaten segment of the one below.
    k = 330 / 111.3                                                       # pixels per g-cal/cm2/yr
    x0 = 35
    levels = [  # (label, total, [(part, value)] in drawing order, y top, height)
        ('PLANTS', 111.3, [('EATEN', 14.8), ('DECAY', 2.8), ('RESPIRATION', 23.4), ('GROWTH', 70.4)], 196, 40),
        ('HERBIVORES', 14.8, [('EATEN', 3.1), ('DECAY', 0.3), ('RESPIRATION', 4.4), ('GROWTH', 7.0)], 138, 40),
        ('CARNIVORES', 3.1, [('RESPIRATION', 1.8), ('GROWTH', 1.3)], 80, 40),
    ]

    d.group('thin')
    d.line((x0, 52), (x0, 262))                                           # the common edge
    base = levels[0][3] + levels[0][4]
    for v in (0, 25, 50, 75, 100):                                        # the scale
        x = x0 + v * k
        d.line((x, base + 30), (x, base + 36))
    d.line((x0, base + 33), (x0 + 100 * k, base + 33))
    # the eaten segment of each level, carried up to the next as construction
    for i in range(2):
        y_top = levels[i][3]
        eaten = levels[i][2][0][1]
        y_next = levels[i + 1][3] + levels[i + 1][4]
        d.line((x0 + eaten * k, y_top), (x0 + eaten * k, y_next))

    d.group()
    for _, total, parts, y, h in levels:
        _box(d, x0, y, total * k, h)
        x = x0
        for _, v in parts[:-1]:
            x += v * k
            d.line((x, y), (x, y + h))

    d.group('mid')
    for _, total, parts, y, h in levels:                                  # heat lost in respiration
        x = x0
        for p, v in parts:
            if p == 'RESPIRATION':
                _hatch(d, x + 0.5, x + v * k - 0.5, y + 0.5, y + h - 0.5, step=5)
            x += v * k
    sun = (340, 50)
    d.line(sun, (340, 192))
    _arrow(d, sun, (340, 192), size=5)
    for a in range(0, 360, 45):
        r = math.radians(a)
        d.line((sun[0] + 7 * math.cos(r), sun[1] - 14 + 7 * math.sin(r)),
               (sun[0] + 11 * math.cos(r), sun[1] - 14 + 11 * math.sin(r)))
    d.circle(sun[0], sun[1] - 14, 4.5)

    d.group('mid')
    py, ph = levels[0][3], levels[0][4]
    d.text(x0 + (14.8 + 2.8 + 23.4 + 35.2) * k, py + ph / 2 + 2.5, 'GROWTH 70.4', size=7)
    d.text(x0 + (14.8 + 2.8 + 11.7) * k, py + ph + 11, 'BURNED 23.4', size=7)
    d.text(x0 + 7.4 * k, py + ph + 11, 'EATEN 14.8', size=7)
    d.text(x0 + (14.8 + 1.4) * k, py + ph + 21, 'DECAY 2.8', size=7)
    d.text(330, py - 6, 'PLANTS 111.3 · 0.10% OF THE SUN', size=7, anchor='end')
    d.text(x0 + 14.8 * k + 8, levels[1][3] + 17, 'HERBIVORES 14.8', size=7, anchor='start')
    d.text(x0 + 14.8 * k + 8, levels[1][3] + 28, '13.3% OF THE PLANTS', size=7, anchor='start')
    d.text(x0 + 3.1 * k + 8, levels[2][3] + 17, 'CARNIVORES 3.1', size=7, anchor='start')
    d.text(x0 + 3.1 * k + 8, levels[2][3] + 28, '22.3% OF THE HERBIVORES', size=7, anchor='start')
    d.text(330, 40, 'SUNLIGHT 118,872', size=7, anchor='end')
    for v in (0, 50, 100):
        d.text(x0 + v * k, base + 47, str(v), size=7)
    d.text(200, 292, 'CEDAR BOG LAKE · G-CAL PER CM² A YEAR · LINDEMAN 1942', size=7)
    return d


def silent_spring():
    d = D()
    # Clear Lake, California, after the DDD treatments of 1949-57: concentrations in parts per million,
    # each level a band whose half-width is proportional to log10(ppm / 0.01), so the bands widen as the
    # poison climbs the food chain: an inverted pyramid on a log scale. Water from the dilution of
    # 1 part in 50 million; plankton from Carson's account; fish flesh and grebe fat from Hunt and
    # Bischoff (1960), tables 3 and 4. Ranges are drawn from their low to their high value.
    cx = 200
    per = 27                                                              # half-width per decade
    floor = 0.01
    bands = [  # (label, low, high, y)
        ('LAKE WATER 0.02', 0.02, 0.02, 236),
        ('PLANKTON ABOUT 5', 5, 5, 194),
        ('PLANKTON-EATING FISH, FLESH 7–20', 7, 20.4, 152),
        ('BASS, FLESH 5–138', 5, 138, 110),
        ('GREBE FAT 723–1,600', 723, 1600, 68),
    ]
    h = 18

    def hw(v):
        return per * math.log10(v / floor)

    d.group('thin')
    d.line((cx, 40), (cx, 262))
    for dec in range(0, 7):                                               # decade lines, both sides
        w = per * dec
        for s in (-1, 1):
            d.line((cx + s * w, 52), (cx + s * w, 258))
    d.line((cx - per * 6, 258), (cx + per * 6, 258))

    d.group()
    for _, lo, hi, y in bands:
        w = max(hw(lo), 1.2)
        _box(d, cx - w, y, 2 * w, h)

    d.group('mid')
    for _, lo, hi, y in bands:                                            # the range up to the high value
        if hi > lo:
            w0, w1 = hw(lo), hw(hi)
            for s in (-1, 1):
                d.line((cx + s * w0, y + h / 2), (cx + s * w1, y + h / 2))
                d.line((cx + s * w1, y + 4), (cx + s * w1, y + h - 4))
    for (_, _, _, y), (_, _, _, y2) in zip(bands, bands[1:]):            # up the chain
        d.line((cx, y - 13), (cx, y2 + h + 2))
        _arrow(d, (cx, y - 13), (cx, y2 + h + 2), size=3)

    d.group('mid')
    for label, _, _, y in bands:
        d.text(cx, y - 4, label, size=7)
    for dec, lab in ((0, '0.01'), (2, '1'), (4, '100'), (6, '10,000')):
        d.text(cx + per * dec, 270, lab, size=7)
    d.text(cx - per * 6, 270, 'PPM', size=7, anchor='start')
    d.text(200, 292, 'CLEAR LAKE, CALIFORNIA · DDD UP THE FOOD CHAIN · LOG SCALE', size=7)
    return d


PLATES = {'food-chain': food_chain, 'silent-spring': silent_spring}
