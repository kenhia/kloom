"""Plates for Daily Bread's part keep1 (sprint 051): salt, lind-scurvy, appert-canning. See plates_for.py."""
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


def _split_cod(cx, cy, length, width, flip=False):
    """Outline of a cod split along the back and laid open flat, seen from above: a broad,
    roughly symmetric blade tapering to the tail, the head cut off square. Points computed
    from a half-width profile along the length."""
    pts_top, pts_bot = [], []
    n = 24
    for i in range(n + 1):
        t = i / n                                                        # 0 at the nape, 1 at the tail
        if t < 0.8:
            hw = width / 2 * (0.82 + 0.18 * math.sin(math.pi * t / 0.8)) * (1 - 0.55 * t)
        else:
            hw = width / 2 * 0.56 * (1 - (t - 0.8) / 0.2 * 0.75)
        x = cx - length / 2 + t * length
        if flip:
            x = cx + length / 2 - t * length
        pts_top.append((x, cy - hw))
        pts_bot.append((x, cy + hw))
    tail = pts_top[-1][0] + (10 if not flip else -10)
    return pts_top + [(tail, cy - width * 0.28), (tail - (4 if not flip else -4), cy), (tail, cy + width * 0.28)] + pts_bot[::-1]


def salt():
    d = D()
    # Left, above: a cod split and laid open, the line where the splitter took out the backbone dashed.
    # Left, below: a kench in section, split fish laid flesh up and head to tail with salt between, the
    # pickle running off (Stevenson 1899, pp. 392-393). Proportions are schematic.
    # Right: Stevenson's weights for 100 lb of cod as it comes from the sea (p. 397), bars to scale,
    # 1 lb = 1.9 units: dressed 66.9 lb (53 water, 1 salt) and dry-salted 38.8 lb (18.9 water, 7.2 salt).
    base, k = 262, 1.9
    xs = [262, 312, 362]
    d.group('thin')
    d.line((20, 98), (215, 98))                                          # the fish's axis
    d.line((248, base), (392, base))                                     # baseline of the bars
    for lb in (25, 50, 75, 100):
        d.line((234, base - lb * k), (238, base - lb * k))
    d.line((236, base), (236, base - 100 * k))

    d.group()
    d.line(*_split_cod(112, 98, 170, 74), closed=True)
    # the kench: four split fish in section, each a shallow lens, alternating head and tail
    for i in range(4):
        y = 238 - i * 14
        x0, x1 = 30 + (i % 2) * 8, 196 - ((i + 1) % 2) * 8
        top = [(x0 + (x1 - x0) * j / 12, y - 5 * math.sin(math.pi * j / 12)) for j in range(13)]
        d.line(*top, (x1, y), (x0, y), closed=True)
    d.line((22, 244), (206, 244))                                        # the floor of the pen
    # the bars
    bars = [(100, None, None), (66.9, 53, 1), (38.8, 18.9, 7.2)]
    for x, (total, water, salt_) in zip(xs, bars):
        _box(d, x - 16, base - total * k, 32, total * k)

    d.group('mid')
    d.dashed((44, 98), (186, 98), dash=4, gap=3)                         # where the backbone was
    for i in range(4):                                                   # salt between the layers
        y = 230 - i * 14
        for j in range(16):
            x = 40 + j * 10 + (i % 2) * 5
            d.line((x - 1.5, y - 1), (x + 1.5, y - 1))
    for x in (60, 110, 160):                                             # pickle running off
        d.line((x, 247), (x, 256))
        _arrow(d, (x, 247), (x, 256), size=3)
    for x, (total, water, salt_) in zip(xs, bars):
        if water is None:
            continue
        yw = base - water * k
        ys = yw - salt_ * k
        d.line((x - 16, yw), (x + 16, yw))
        d.line((x - 16, ys), (x + 16, ys))
        for h in range(int(water * k) // 6):                             # water, hatched
            y = base - 3 - h * 6
            d.line((x - 13, y), (x + 13, y))

    d.group('mid')
    d.text(112, 52, 'SPLIT, BACKBONE OUT', size=7)
    d.text(112, 154, 'A KENCH, IN SECTION', size=7)
    d.text(112, 272, 'PICKLE RUNS OFF', size=7)
    d.text(362, base - (18.9 + 3.6) * k + 2.5, 'SALT', size=7)
    for x, s in zip(xs, ('100', '66.9', '38.8')):
        d.text(x, base + 12, s, size=7)
    d.text(262, base + 23, 'CAUGHT', size=7)
    d.text(312, base + 23, 'DRESSED', size=7)
    d.text(362, base + 23, 'CURED', size=7)
    d.text(312, 36, 'POUNDS · WATER HATCHED', size=7)
    return d


def lind_scurvy():
    d = D()
    # Lind's trial, 20 May 1747 (Treatise, 1753, pp. 191-196): twelve men on one common diet, six
    # pairs, each pair given one remedy. Each row is a pair, two circles; the bar is how long the
    # course ran on a scale of days (a fortnight for five pairs; six days for the oranges and lemon,
    # until the fruit ran out); the mark at its end is Lind's outcome.
    x0, xd = 120, 14                                                      # day 0, units per day
    rows = [
        ('CIDER', 14, 'abated'),
        ('ELIXIR OF VITRIOL', 14, 'none'),
        ('VINEGAR', 14, 'none'),
        ('SEA WATER', 14, 'none'),
        ('2 ORANGES, 1 LEMON', 6, 'fit'),
        ('ELECTUARY', 14, 'none'),
    ]
    y0, dy = 62, 32
    d.group('thin')
    for day in range(0, 15, 2):
        x = x0 + day * xd
        d.line((x, y0 - 16), (x, y0 + 5 * dy + 14))
    d.line((26, y0 - 8), (26, y0 + 5 * dy + 8))                           # the common diet

    d.group()
    for i, (name, days, out) in enumerate(rows):
        y = y0 + i * dy
        d.circle(40, y, 5)
        d.circle(54, y, 5)
        d.line((x0, y - 4), (x0 + days * xd, y - 4), (x0 + days * xd, y + 4), (x0, y + 4), closed=True)

    d.group('mid')
    for i, (name, days, out) in enumerate(rows):
        y = y0 + i * dy
        d.line((26, y), (34, y))
        x = x0 + days * xd + 10
        if out == 'fit':                                                  # an arrow up: recovered
            d.line((x, y + 8), (x + 10, y - 8))
            _arrow(d, (x, y + 8), (x + 10, y - 8), size=5)
        elif out == 'abated':                                             # a short rise
            d.line((x, y + 3), (x + 10, y - 2))
        else:                                                             # level: no change
            d.line((x, y), (x + 10, y))

    d.group('mid')
    for i, (name, days, out) in enumerate(rows):
        y = y0 + i * dy
        d.text(x0, y - 8, name, size=7, anchor='start')
    d.text(x0 + 6 * xd + 26, y0 + 4 * dy + 3, 'FIT FOR DUTY IN 6 DAYS', size=7, anchor='start')
    d.text(x0 + 14 * xd, y0 - 8, 'SOMEWHAT ABATED', size=7, anchor='end')
    for day in (0, 6, 14):
        d.text(x0 + day * xd, y0 + 5 * dy + 26, str(day), size=7)
    d.text(x0 + 7 * xd, y0 + 5 * dy + 38, 'DAYS ON THE REMEDY', size=7)
    d.text(30, y0 + 5 * dy + 26, 'ONE DIET', size=7, anchor='start')
    d.text(200, 24, 'HMS SALISBURY · 20 MAY 1747 · SIX PAIRS', size=7)
    return d


def appert_canning():
    d = D()
    # Left: Appert's water bath in section (L'Art de conserver, 1810, § VI): bottles upright in a boiler,
    # cold water to their necks, the lid resting on the bottles and sealed with wet linen, fire below.
    # Each bottle is corked, with two iron wires crossed over the cork. Proportions are schematic.
    # Right: the bath's temperature through one operation for small green peas, as Appert times it:
    # brought to the boil, held at 100 °C for an hour and a half (cool season), fire out, water let out a
    # quarter of an hour later. The heating and cooling curves are schematic; the plateau is his.
    bx0, bx1, by0, by1 = 20, 200, 104, 236                               # the boiler
    water = 132
    d.group('thin')
    d.line((bx0 - 8, water), (bx1 + 8, water))                           # the water line
    for x in (60, 110, 160):
        d.line((x, 52), (x, by1 + 6))                                    # bottle axes
    gx0, gx1, gy0, gy1 = 252, 388, 236, 80                               # graph box: 0-4 h, 0-110 °C

    def gx(h):
        return gx0 + (gx1 - gx0) * h / 4

    def gy(c):
        return gy0 - (gy0 - gy1) * c / 110

    for c in (20, 40, 60, 80, 100):
        d.line((gx0, gy(c)), (gx1, gy(c)))

    d.group()
    d.line((bx0, by0), (bx0, by1), (bx1, by1), (bx1, by0))               # the boiler
    d.line((bx0 - 6, 84), (bx1 + 6, 84))                                 # the lid, resting on the corks
    d.line((bx0 - 6, 84), (bx0 - 6, 98))
    d.line((bx1 + 6, 84), (bx1 + 6, 98))
    for x in (60, 110, 160):                                             # bottles: body, shoulder, neck
        d.line((x - 7, 96), (x - 7, 108), (x - 18, 124), (x - 18, by1 - 4), (x + 18, by1 - 4),
               (x + 18, 124), (x + 7, 108), (x + 7, 96))
    d.line((gx0, gy1 - 6), (gx0, gy0), (gx1 + 4, gy0))                    # graph axes

    d.group('mid')
    for x in (60, 110, 160):                                             # corks and crossed wires
        _box(d, x - 6, 84, 12, 13)
        d.line((x - 9, 104), (x + 2, 86))
        d.line((x + 9, 104), (x - 2, 86))
    for x in range(30, 196, 12):                                         # flames
        d.line((x, 262), (x + 4, 248), (x + 8, 262))
    d.line((bx0 + 4, by1 + 4), (bx1 - 4, by1 + 4))                       # the grate
    curve = [(0, 15)]
    for i in range(1, 11):                                               # heating, schematic
        t = 0.75 * i / 10
        curve.append((t, 15 + 85 * (1 - math.exp(-4 * t)) / (1 - math.exp(-3))))
    curve = [(t, min(c, 100)) for t, c in curve]
    curve += [(0.75, 100), (2.25, 100)]                                  # held at the boil 1 1/2 h
    for i in range(1, 8):                                                # cooling, schematic
        t = 2.25 + 1.5 * i / 7
        curve.append((t, 100 - 40 * (1 - math.exp(-1.5 * (t - 2.25)))))
    d.line(*[(gx(t), gy(c)) for t, c in curve])
    d.dashed((gx(2.25), gy(100)), (gx(2.25), gy0), dash=3, gap=3)
    d.dashed((gx(2.5), gy(95)), (gx(2.5), gy0), dash=3, gap=3)

    d.group('mid')
    d.text(110, 30, 'CORKED, WIRED, IN A WATER BATH', size=7)
    d.text(bx1 + 10, water + 3, 'WATER', size=7, anchor='start')
    d.text(110, 280, 'FIRE', size=7)
    d.text(gx0 - 4, gy(100) + 3, '100 °C', size=7, anchor='end')
    d.text(gx0 - 4, gy(20) + 3, '20', size=7, anchor='end')
    d.text((gx(0.75) + gx(2.25)) / 2, gy(100) - 6, 'BOIL 1½ H', size=7)
    d.text(gx(2.25) - 3, gy0 - 8, 'FIRE OUT', size=7, anchor='end')
    d.text(gx(2.5) + 3, gy0 - 20, 'DRAIN', size=7, anchor='start')
    for h in (0, 2, 4):
        d.text(gx(h), gy0 + 12, f'{h} H', size=7)
    d.text((gx0 + gx1) / 2, 60, 'SMALL GREEN PEAS', size=7)
    return d


PLATES = {'salt': salt, 'lind-scurvy': lind_scurvy, 'appert-canning': appert_canning}
