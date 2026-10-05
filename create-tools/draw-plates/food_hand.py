"""Plates for Daily Bread's frames written by hand in sprint 051. See plates_for.py."""
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


def cooking():
    d = D()
    # Feeding time against body mass, both on log axes (Organ et al. 2011). The primate line is schematic:
    # it is drawn through the two values the paper gives, the 48% predicted for a primate of human size and
    # the chimpanzee's 37%; the human point is the 4.7% observed. Body masses are placed, not measured.
    x0, x1, y0, y1 = 70, 370, 250, 40                                     # plot box: 1-100 kg, 1-100 %

    def px(kg):
        return x0 + (x1 - x0) * math.log10(kg) / 2

    def py(pct):
        return y0 - (y0 - y1) * math.log10(pct) / 2

    d.group('thin')
    for k in (1, 2, 5, 10, 20, 50, 100):                                  # log grid
        d.line((px(k), y0), (px(k), y1))
    for p in (1, 2, 5, 10, 20, 50, 100):
        d.line((x0, py(p)), (x1, py(p)))

    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))                                  # the axes
    chimp, human = (40, 37), (60, 48)
    slope = (math.log10(human[1]) - math.log10(chimp[1])) / (math.log10(human[0]) - math.log10(chimp[0]))

    def line_pct(kg):
        return human[1] * (kg / human[0]) ** slope

    d.dashed((px(15), py(line_pct(15))), (px(100), py(line_pct(100))), dash=5, gap=3)

    d.group('mid')
    d.circle(px(chimp[0]), py(chimp[1]), 3.5)
    d.circle(px(human[0]), py(human[1]), 3.5)
    d.circle(px(human[0]), py(4.7), 4.5)
    d.circle(px(human[0]), py(4.7), 1.5)
    top, bottom = (px(human[0]) + 14, py(human[1]) + 4), (px(human[0]) + 14, py(4.7) - 4)
    d.line(top, bottom)
    _arrow(d, top, bottom)

    d.group('mid')
    d.text(px(chimp[0]) - 8, py(chimp[1]) + 3, 'CHIMPANZEE 37%', size=7, anchor='end')
    d.text(px(human[0]) - 8, py(human[1]) - 6, 'PREDICTED 48%', size=7, anchor='end')
    d.text(px(human[0]) - 9, py(4.7) + 3, 'US 4.7%', size=7, anchor='end')
    d.text(top[0] - 6, (top[1] + bottom[1]) / 2 + 10, 'TEN TIMES', size=7, anchor='end')
    d.text(top[0] - 6, (top[1] + bottom[1]) / 2 + 21, 'LESS', size=7, anchor='end')
    d.text(px(15) - 5, py(line_pct(15)) + 3, 'PRIMATE TREND (SCHEMATIC)', size=7, anchor='end')
    for k in (1, 10, 100):
        d.text(px(k), y0 + 12, str(k), size=7)
    for p in (1, 10, 100):
        d.text(x0 - 6, py(p) + 3, f'{p}%', size=7, anchor='end')
    d.text((x0 + x1) / 2, y0 + 26, 'BODY MASS · KG · LOG', size=7)
    d.text((x0 + x1) / 2, 24, 'SHARE OF THE DAY SPENT FEEDING', size=7)
    return d


def foragers():
    d = D()
    # Left: the Ohalo II grinding slab in section, a basalt slab set on small pebbles like an anvil
    # (Weiss et al. 2004), with a hand stone and its stroke. Proportions are schematic.
    # Right: a composite sickle, flint bladelets set in a straight haft, with the band of gloss that
    # semi-green cereal stems leave on the cutting edge (Groman-Yaroslavski et al. 2016).
    ground = 232
    d.group('thin')
    d.line((20, ground), (215, ground))                                   # hut floor
    d.line((118, 60), (118, ground + 10))                                 # the stroke's axis
    d.line((248, 150), (388, 150))                                        # the sickle's axis

    d.group()
    # the slab: a thick, slightly dished block
    sx0, sx1, st, sb = 40, 196, 186, 214
    dish = [(sx0 + (sx1 - sx0) * i / 20,
             st + 5 * math.sin(math.pi * i / 20)) for i in range(21)]
    d.line((sx0, sb), *dish, (sx1, sb), closed=True)
    # pebbles under it
    for i, x in enumerate(range(50, 192, 16)):
        r = 5 + (i * 7 % 4)
        d.circle(x, ground - r + 1, r)
    # the hand stone, a rounded loaf of stone
    d.ellipse(118, 166, 34, 14)

    d.group('mid')
    for x in range(56, 182, 9):                                           # grains on the slab
        y = st + 5 * math.sin(math.pi * (x - sx0) / (sx1 - sx0)) - 2
        d.ellipse(x, y, 3, 1.4)
    left, right = (70, 140), (166, 140)                                   # the stroke, both ways
    d.line(left, right)
    _arrow(d, right, left)
    _arrow(d, left, right)

    d.group()
    # the haft and five bladelets set along its edge
    d.line((250, 146), (386, 146), (386, 154), (250, 154), closed=True)
    for i in range(5):
        x = 262 + i * 22
        d.line((x, 146), (x + 4, 128), (x + 20, 128), (x + 20, 146))

    d.group('mid')
    d.line((262, 132), (366, 132))                                        # the gloss band
    d.line((262, 135), (366, 135))

    d.group('mid')
    d.text(118, 252, 'BASALT SLAB ON PEBBLES', size=7)
    d.text(118, 115, 'HAND STONE', size=7)
    d.text(318, 112, 'GLOSS', size=7)
    d.text(318, 176, 'FLINT IN A WOODEN HAFT', size=7)
    d.text(318, 190, 'COMPOSITE SICKLE', size=7)
    d.text(200, 282, 'OHALO II · c. 23,000 YEARS AGO', size=7)
    return d


def _voids(rng, r_field, dmin, dmax, cover, scale):
    """Non-overlapping circular voids in a disc of radius r_field (units), diameters dmin-dmax mm."""
    target = cover * math.pi * r_field ** 2
    voids, area, tries = [], 0.0, 0
    while area < target and tries < 200000:
        tries += 1
        r = rng.uniform(dmin, dmax) * scale / 2
        a, rho = rng.uniform(0, 2 * math.pi), math.sqrt(rng.random()) * (r_field - r - 1)
        x, y = rho * math.cos(a), rho * math.sin(a)
        if all(math.hypot(x - vx, y - vy) > r + vr + 0.8 for vx, vy, vr in voids):
            voids.append((x, y, r))
            area += math.pi * r * r
    return voids


def oldest_bread():
    d = D()
    # Four magnified crumbs, each a field 3 mm across, with voids drawn to the sizes and shares of the
    # surface in Arranz-Otaegui et al. (2018): charred dough 0.5-0.8 mm voids over 30%; flat bread
    # 0.05-0.25 mm over 5-10%; leavened bread over 1 mm over 40-70%; Shubayqa 1 averaging 0.15 mm over 16%.
    # The positions are random (the first seed whose layout reaches the share); the sizes and shares are the paper's.
    rf = 40                                                               # 3 mm field
    scale = 2 * rf / 3                                                    # units per mm
    cy = 118
    crumbs = [
        (55, 'DOUGH', '0.5–0.8 MM', 0.5, 0.8, 0.32),
        (150, 'FLAT BREAD', '0.05–0.25 MM', 0.05, 0.25, 0.08),
        (245, 'LEAVENED', 'OVER 1 MM', 1.0, 1.15, 0.4),
        (340, 'SHUBAYQA 1', 'AVG 0.15 MM', 0.08, 0.22, 0.16),
    ]
    d.group('thin')
    for cx, *_ in crumbs:
        d.line((cx - rf - 6, cy), (cx + rf + 6, cy))
        d.line((cx, cy - rf - 6), (cx, cy + rf + 6))

    d.group()
    for cx, *_ in crumbs:
        d.circle(cx, cy, rf)

    d.group('mid')
    for cx, _, _, dmin, dmax, cover in crumbs:
        seed = 0
        while True:                                                       # a layout that reaches the share
            vs = _voids(random.Random(seed), rf, dmin, dmax, cover, scale)
            if sum(math.pi * r * r for _, _, r in vs) >= 0.9 * cover * math.pi * rf ** 2:
                break
            seed += 1
        for x, y, r in vs:
            d.circle(cx + x, cy + y, r)

    d.group()
    steps = ['DEHUSK', 'GRIND', 'SIEVE', 'MIX', 'BAKE']
    xs = [56, 128, 200, 272, 344]
    for x in xs:
        _box(d, x - 28, 216, 56, 20)
    for a, b in zip(xs, xs[1:]):
        d.line((a + 28, 226), (b - 28, 226))
        _arrow(d, (a + 28, 226), (b - 28, 226), size=4)

    d.group('mid')
    for cx, name, size, *_ in crumbs:
        d.text(cx, cy + rf + 16, name, size=7)
        d.text(cx, cy + rf + 27, size, size=7)
    for x, s in zip(xs, steps):
        d.text(x, 229, s, size=7)
    d.line((300, 270), (300 + scale, 270))                                # a 1 mm scale bar
    d.line((300, 266), (300, 274))
    d.line((300 + scale, 266), (300 + scale, 274))
    d.text(300 + scale + 6, 273, '1 MM', size=7, anchor='start')
    d.text(200, 46, 'VOIDS IN THE CRUMB, A FIELD 3 MM ACROSS', size=7)
    d.text(150, 273, 'BAKED ON A HOT STONE OR IN ASHES', size=7)
    return d


PLATES = {'cooking': cooking, 'foragers': foragers, 'oldest-bread': oldest_bread}
