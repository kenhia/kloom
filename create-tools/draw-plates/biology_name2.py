"""Plates for The Story of Life's part name2 (sprint 055): John Ray and Linnaeus. See plates_for.py."""
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


def _blade(d, x0, y0, x1, y1, w, bend=0.0, n=16):
    """A narrow leaf blade from base (x0, y0) to tip (x1, y1), widest a third of the way up."""
    left, right = [], []
    for k in range(n + 1):
        t = k / n
        x = x0 + (x1 - x0) * t + bend * math.sin(math.pi * t)
        y = y0 + (y1 - y0) * t
        half = w * (1 - t) ** 0.9 * min(1.0, 3 * t + 0.25)
        left.append((x - half, y))
        right.append((x + half, y))
    d.line(*left, *reversed(right), closed=True)


def _rot_ellipse(d, cx, cy, rx, ry, ang, n=40):
    """An ellipse turned by ang degrees."""
    a = math.radians(ang)
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    d.line(*pts, closed=True)


def ray_species():
    d = D()
    # Two seedlings in section, from Ray's discourse of 1674: corn, whose seed holds the young plant at
    # one end of a "pulp" that feeds it, coming up as one blade on a tuft of fibrous roots; and a kidney
    # bean, whose two seed leaves are the two lobes of the seed and are lifted above the ground. Below,
    # each seed cut open. Proportions schematic.
    ground = 168
    gx, bx = 104, 292                                                     # the two seedlings' axes

    d.group('thin')
    d.line((18, ground), (382, ground))
    d.line((200, 34), (200, 286))                                         # the divide
    for x in (gx, bx):
        d.line((x, 40), (x, 232))
    for k in range(5):                                                    # a depth scale in the soil
        y = ground + 12 * k
        d.line((22, y), (28, y))
    for k in range(9):                                                    # soil hatching
        x = 30 + 40 * k
        if abs(x - 200) > 10:
            d.line((x, ground + 6), (x - 8, ground + 14))

    d.group()
    # corn: the grain under the ground, the blade, the fibres
    gy = ground + 22
    d.ellipse(gx + 10, gy, 15, 8)
    _blade(d, gx, gy - 6, gx - 8, 56, 7.5, bend=-5)
    for k, ang in enumerate((-62, -40, -18, 6, 30, 54)):                  # six fibres, as Ray saw in barley
        a = math.radians(90 + ang)
        ln = 48 + 8 * (k % 2)
        x1, y1 = gx + ln * math.cos(a), gy + 4 + ln * math.sin(a)
        mx, my = gx + 0.5 * ln * math.cos(a) + 4, gy + 4 + 0.5 * ln * math.sin(a)
        d.curve(f"M{gx},{gy + 4} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}")
    # kidney bean: the arched stalk, the two seed leaves above ground, the first true leaves, the root
    top = 92
    d.curve(f"M{bx},{ground + 4} C{bx - 2},{ground - 30} {bx + 3},{top + 30} {bx},{top}")
    for s in (-1, 1):                                                     # the two seed leaves, spread
        _rot_ellipse(d, bx + s * 24, top + 3, 23, 9.5, s * 12)
    for s in (-1, 1):                                                     # the plumule between them
        d.curve(f"M{bx},{top} Q{bx + s * 4},{top - 18} {bx + s * 16},{top - 30}")
        d.ellipse(bx + s * 20, top - 34, 8, 5)
    d.line((bx, ground + 4), (bx + 1, 248))                               # the taproot
    for k, y in enumerate((ground + 18, ground + 34, ground + 52, ground + 66)):
        s = 1 if k % 2 else -1
        d.curve(f"M{bx},{y} q{s * 10},4 {s * (22 - 3 * k)},{12 - k}")

    d.group('mid')
    # the grain cut open: the embryo at one end, the pulp hatched; the bean seed cut open: two lobes
    ex, ey = 70, 262
    d.ellipse(ex, ey, 26, 13)
    d.ellipse(ex - 17, ey, 6, 7)                                          # the young plant
    for k in range(6):                                                    # the pulp, hatched inside the coat
        x = ex - 8 + 6 * k
        h = 13 * math.sqrt(max(0.0, 1 - ((x + 3 - ex) / 26) ** 2)) - 3
        d.line((x, ey - h), (x + 6, ey + h))
    sx, sy = 328, 262
    d.line((sx - 22, sy), (sx + 22, sy))                                  # the halves clapped together
    d.arc(sx, sy, 22, 180, 360, ry=12)
    d.arc(sx, sy, 22, 0, 180, ry=12)
    d.ellipse(sx - 24, sy, 4, 3)                                          # the radicle, hinging both

    d.group('mid')
    d.text(gx, 28, 'BARLEY · ONE BLADE', size=7)
    d.text(bx, 28, 'KIDNEY BEAN · TWO SEED LEAVES', size=7)
    d.text(gx + 32, gy + 3, 'GRAIN', size=7, anchor='start')
    d.text(bx + 30, top + 26, 'SEED LEAVES', size=7, anchor='start')
    d.text(bx + 8, 230, 'ROOT', size=7, anchor='start')
    d.text(ex + 32, ey + 2.5, 'PULP', size=7, anchor='start')
    d.text(sx - 30, sy + 22, 'TWO LOBES', size=7, anchor='start')
    d.text(30, ground - 4, 'GROUND', size=7, anchor='start')
    d.text(200, 296, 'SEEDLINGS IN SECTION · RAY, 1674', size=7)
    return d


def _flower(d, cx, cy, stamens, pistils=1, r=19):
    """A flower seen from above, as a key draws it: the corolla, the stamens around, the pistils inside."""
    d.circle(cx, cy, r)
    for k in range(stamens):
        a = math.radians(-90 + 360 * k / stamens)
        sx, sy = cx + 0.62 * r * math.cos(a), cy + 0.62 * r * math.sin(a)
        d.line((cx + 0.28 * r * math.cos(a), cy + 0.28 * r * math.sin(a)), (sx, sy))
        d.circle(sx, sy, 2.2)
    if pistils == 1:
        d.circle(cx, cy, 3.2)
    else:
        for k in range(pistils):
            a = math.radians(90 + 360 * k / pistils)
            d.circle(cx + 3.5 * math.cos(a), cy + 3.5 * math.sin(a), 1.8)


def linnaeus():
    d = D()
    # Top: the first six classes of Linnaeus's sexual system, flowers keyed by their number of stamens
    # (1735). Below: one plant placed in his nested ranks, the cutleaf groundcherry of Species Plantarum
    # (1753), p. 183: kingdom, class by stamens, order by pistils, genus, species.
    names = ['MONANDRIA', 'DIANDRIA', 'TRIANDRIA', 'TETRANDRIA', 'PENTANDRIA', 'HEXANDRIA']
    xs = [42 + 63.2 * k for k in range(6)]
    cy = 56

    d.group('thin')
    d.line((14, cy), (386, cy))
    for x in xs:
        d.line((x, 26), (x, 86))
    # nested ranks: each box inside the last, stepped to the right
    boxes = [(14, 120, 372, 164), (60, 138, 318, 138), (106, 156, 264, 112), (152, 174, 210, 86), (198, 192, 156, 60)]

    d.group()
    for k, x in enumerate(xs):
        _flower(d, x, cy, k + 1)
    for x, y, w, h in boxes:
        _box(d, x, y, w, h)

    d.group('mid')
    _flower(d, 316, 222, 5, 1, r=17)                                       # the groundcherry's flower
    d.line((xs[4], 108), (xs[4], 136))                                     # Pentandria leads to the class
    _arrow(d, (xs[4], 126), (xs[4], 136), size=4)

    d.group('mid')
    for k, (x, n) in enumerate(zip(xs, names)):
        d.text(x, 93, str(k + 1), size=7)
        d.text(x, 103, n, size=6)
    labels = ['KINGDOM · VEGETABILE', 'CLASS · PENTANDRIA · 5 STAMENS', 'ORDER · MONOGYNIA · 1 PISTIL',
              'GENUS · PHYSALIS', 'SPECIES · ANGULATA']
    for (x, y, w, h), s in zip(boxes, labels):
        d.text(x + 4, y + 10, s, size=7, anchor='start')
    d.text(200, 20, 'CLASSES BY STAMENS · SYSTEMA NATURAE, 1735', size=7)
    d.text(200, 296, 'PHYSALIS ANGULATA · SPECIES PLANTARUM, 1753', size=7)
    return d


PLATES = {'ray-species': ray_species, 'linnaeus': linnaeus}
