"""Plates for The Story of Life's frames written by hand in sprint 055. See plates_for.py."""
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


def aristotle_animals():
    d = D()
    # Aristotle's "great genera" (History of Animals I.6, IV.1), as a bracket tree: the blooded genera
    # (enhaima) and the bloodless (anhaima), each leaf beside the modern group it roughly matches.
    # The tree is a reading of his text, not a diagram he drew; the leaf spacing is even.
    blooded = [('FOUR-FOOTED, LIVE YOUNG', 'MAMMALS'), ('FOUR-FOOTED, EGGS', 'REPTILES'),
               ('SNAKES', 'SNAKES'), ('BIRDS', 'BIRDS'), ('FISHES', 'FISHES'), ('CETACEANS', 'WHALES')]
    bloodless = [('SOFT-BODIED', 'CEPHALOPODS'), ('SOFT-SHELLED', 'CRUSTACEANS'),
                 ('SHELL-SKINNED', 'SNAILS, CLAMS'), ('INSECTS', 'ARTHROPODS')]
    step, top = 21, 48
    ys_a = [top + i * step for i in range(len(blooded))]
    ys_b = [ys_a[-1] + 2 * step + i * step for i in range(len(bloodless))]
    root = (40, (ys_a[0] + ys_b[-1]) / 2)
    na = (112, sum(ys_a) / len(ys_a))
    nb = (112, sum(ys_b) / len(ys_b))
    spine_x, leaf_x = 162, 176

    d.group('thin')
    for y in ys_a + ys_b:                                                 # rules under each row
        d.line((leaf_x + 6, y + 5), (392, y + 5))
    d.line((spine_x, ys_a[0] - 10), (spine_x, ys_b[-1] + 10))
    d.line((root[0], 30), (root[0], 270))

    d.group()
    for n in (na, nb):                                                    # root to the two genera
        d.line(root, (76, root[1]), (76, n[1]), n)
    d.circle(*root, 5)
    for n, ys in ((na, ys_a), (nb, ys_b)):
        d.circle(*n, 4)
        d.line(n, (spine_x, n[1]))
        d.line((spine_x, ys[0]), (spine_x, ys[-1]))
        for y in ys:
            d.line((spine_x, y), (leaf_x, y))

    d.group('mid')
    for y in ys_a + ys_b:
        d.circle(leaf_x + 3, y, 2.5)

    d.group('mid')
    d.text(root[0], root[1] + 18, 'ANIMALS', size=7)
    d.text(na[0], na[1] - 9, 'BLOODED', size=7)
    d.text(nb[0], nb[1] - 9, 'BLOODLESS', size=7)
    d.text(leaf_x + 10, 30, 'ARISTOTLE', size=7, anchor='start')
    d.text(392, 30, 'TODAY, ROUGHLY', size=7, anchor='end')
    for (a, m), y in zip(blooded + bloodless, ys_a + ys_b):
        d.text(leaf_x + 10, y + 2.5, a, size=7, anchor='start')
        d.text(392, y + 2.5, m, size=7, anchor='end')
    d.text(200, 288, 'THE GREAT GENERA · HISTORY OF ANIMALS I.6', size=7)
    return d


def _branch(d, x, y, ang, length, depth, spread, shrink):
    """A recursive two-way branch from (x, y), angle in degrees from vertical."""
    a = math.radians(ang)
    x2, y2 = x + length * math.sin(a), y - length * math.cos(a)
    d.line((x, y), (x2, y2))
    if depth > 1:
        for s in (-spread, spread):
            _branch(d, x2, y2, ang + s, length * shrink, depth - 1, spread, shrink)


def theophrastus():
    d = D()
    # The four classes of Enquiry into Plants I.3, each drawn from its definition: a tree, one stem with
    # knots and branches; a shrub, many branches from the root; an under-shrub, many stems and many
    # branches; a herb, leaves from the root and no main stem, the seed borne on a stalk. Schematic.
    ground = 222
    xs = [62, 160, 252, 342]

    d.group('thin')
    d.line((20, ground), (390, ground))
    for x in xs:
        d.line((x, ground + 4), (x, 62))                                  # each plant's axis
    for h in range(0, 161, 40):                                           # a height scale
        d.line((22, ground - h), (28, ground - h))

    d.group()
    # tree: a single knotted stem, then branches
    t = xs[0]
    d.line((t - 4, ground), (t - 3, 140), (t, 120))
    d.line((t + 4, ground), (t + 3, 140), (t, 120))
    for y in (190, 162):                                                  # knots
        d.ellipse(t, y, 3.5, 2)
    for s in (-26, 26):
        _branch(d, t, 124, s, 30, 3, 24, 0.68)
    # shrub: many branches from the root
    for ang in (-40, -22, -6, 8, 24, 40):
        _branch(d, xs[1], ground, ang, 52, 2, 18, 0.55)
    # under-shrub: many stems, each with many short branches
    for i, dx in enumerate((-18, -6, 6, 18)):
        x0 = xs[2] + dx
        top = ground - 70 - (i % 2) * 10
        d.line((x0, ground), (x0 + dx * 0.4, top))
        for k in range(1, 5):
            y = ground - k * (ground - top) / 5
            xm = x0 + dx * 0.4 * k / 5
            side = 1 if k % 2 else -1
            d.line((xm, y), (xm + side * 9, y - 7))
    # herb: blades from the root, no main stem, a seed stalk
    h = xs[3]
    for ang in (-50, -32, -16, 16, 32, 50):
        a = math.radians(ang)
        tip = (h + 62 * math.sin(a), ground - 62 * math.cos(a) * 0.8)
        mid = (h + 30 * math.sin(a) * 0.6, ground - 40)
        d.curve(f"M{h},{ground} Q{mid[0]:.1f},{mid[1]:.1f} {tip[0]:.1f},{tip[1]:.1f}")
    d.line((h, ground), (h + 2, 112))

    d.group('mid')
    for k in range(7):                                                    # the ear on the herb's stalk
        y = 118 + k * 6
        d.ellipse(h - 2.5, y, 2.2, 3.2)
        d.ellipse(h + 4.5, y + 3, 2.2, 3.2)
    for x in xs:                                                          # roots
        for s in (-1, 0, 1):
            d.line((x, ground), (x + s * 12, ground + 14), (x + s * 18, ground + 20))

    d.group('mid')
    names = [('TREE', 'OLIVE · FIG'), ('SHRUB', 'BRAMBLE'), ('UNDER-SHRUB', 'SAVORY · RUE'), ('HERB', 'CORN')]
    for x, (n, ex) in zip(xs, names):
        d.text(x, ground + 36, n, size=7)
        d.text(x, ground + 47, ex, size=7)
    d.text(xs[0], 52, 'ONE STEM', size=7)
    d.text(xs[1], 52, 'MANY BRANCHES', size=7)
    d.text(xs[2], 52, 'MANY STEMS', size=7)
    d.text(xs[3], 52, 'NO MAIN STEM', size=7)
    d.text(200, 26, 'THE FOUR CLASSES · ENQUIRY INTO PLANTS I.3', size=7)
    return d


def _leaf(d, cx, cy, s, flip=1):
    """An asymmetric leaf on a curved stalk, mirrored when flip is -1, to show the reversal."""
    pts = []
    for k in range(13):
        t = k / 12
        w = math.sin(math.pi * t) * 9 * s
        pts.append((cx + flip * w, cy - 22 * s + 36 * s * t))
    back = [(cx - flip * math.sin(math.pi * (k / 12)) * 4 * s, cy - 22 * s + 36 * s * (k / 12)) for k in range(12, -1, -1)]
    d.line(*pts, *back, closed=True)
    d.curve(f"M{cx:.1f},{cy + 14 * s:.1f} Q{cx + flip * 6 * s:.1f},{cy + 22 * s:.1f} {cx + flip * 14 * s:.1f},{cy + 24 * s:.1f}")
    d.line((cx, cy - 18 * s), (cx, cy + 14 * s))


def herbals():
    d = D()
    # Top: the drawing, reversed onto the block, printed the right way round again.
    # Below: a relief woodblock in section, the lines left standing at the printing surface and the
    # ground between them cut away, ink on the lines only, the paper pressed down. Proportions schematic.
    top, cut, base = 168, 186, 246
    x0, x1 = 64, 316
    ridges = [92, 112, 132, 176, 196, 240, 260, 288]                     # where lines stand, as across a leaf
    half, bevel = 2.5, 5

    d.group('thin')
    d.line((x0 - 6, top), (x1 + 8, top))                                  # the printing surface
    d.line((x0 - 6, cut), (x1 + 8, cut))                                  # the depth of the cut
    for x in (76, 200, 324):
        d.line((x, 30), (x, 92))
    d.line((x0 - 14, top), (x0 - 14, base))                               # block height
    d.line((x0 - 18, top), (x0 - 10, top))
    d.line((x0 - 18, base), (x0 - 10, base))

    d.group()
    out = [(x0, top), (x0 + 8, top), (x0 + 8 + bevel, cut)]
    for r in ridges:
        out += [(r - half - bevel, cut), (r - half, top), (r + half, top), (r + half + bevel, cut)]
    out += [(x1 - 8 - bevel, cut), (x1 - 8, top), (x1, top), (x1, base), (x0, base)]
    d.line(*out, closed=True)
    for x, label in ((76, 'DRAWING'), (200, 'ON THE BLOCK'), (324, 'PRINT')):
        _box(d, x - 34, 34, 68, 54)
    _leaf(d, 76, 60, 1)
    _leaf(d, 200, 60, 1, flip=-1)
    _leaf(d, 324, 60, 1)

    d.group('mid')
    for r in ridges:                                                      # ink on the standing lines
        d.line((r - half, top - 1.5), (r + half, top - 1.5))
    d.line((x0, top - 6), (x1, top - 6))                                  # the paper
    for x in (100, 190, 280):                                             # pressure
        d.line((x, 112), (x, top - 10))
        _arrow(d, (x, 112), (x, top - 10), size=4)
    for a, b in ((110, 166), (234, 290)):
        d.line((a, 61), (b, 61))
        _arrow(d, (a, 61), (b, 61), size=4)
    for k in range(6):                                                    # wood grain
        y = 200 + k * 8
        d.line((x0 + 6, y), (x1 - 6, y + (k % 2) * 2))

    d.group('mid')
    for x, label in ((76, 'DRAWING'), (200, 'ON THE BLOCK'), (324, 'PRINT')):
        d.text(x, 102, label, size=7)
    d.text(x1 + 12, top - 6 + 2.5, 'PAPER', size=7, anchor='start')
    d.text(x1 + 12, top + 6, 'INKED LINE', size=7, anchor='start')
    d.text(x1 + 12, cut + 2.5, 'CUT AWAY', size=7, anchor='start')
    d.text(145, 140, 'PRESSED', size=7)
    d.text(x0 - 18, (top + base) / 2 + 3, 'BLOCK', size=7, anchor='end')
    d.text(200, 272, 'A RELIEF WOODCUT IN SECTION · BASEL, 1542', size=7)
    return d


PLATES = {'aristotle-animals': aristotle_animals, 'theophrastus': theophrastus, 'herbals': herbals}
