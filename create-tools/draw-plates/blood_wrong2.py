"""Plates for In the Blood's trail What we got wrong, its second half (sprint 028). See plates_for.py."""
import math
from plates import D


def _pt(cx, cy, r, a):
    """The point at `a` degrees on a circle (clockwise from +x; SVG's y runs down)."""
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _tube(d, x, top, h=38, w=14):
    """A small test tube in section: straight sides and a round foot, open at the top."""
    r = w / 2
    d.line((x - r, top), (x - r, top + h - r))
    d.arc(x, top + h - r, r, 180, 0, n=16)
    d.line((x + r, top + h - r), (x + r, top))


# The Hirszfelds' Table II (Lancet, 18 October 1919, p. 677): A, B and AB per cent, for the sixteen
# peoples in the order they printed them. The index is (A + AB) / (B + AB), by our arithmetic.
HIRSZFELD = [
    ('English', 43.4, 7.2, 3.0), ('French', 42.6, 11.2, 3.0), ('Italians', 38.0, 11.0, 3.8),
    ('Germans', 43.0, 12.0, 5.0), ('Austrians', 40.0, 10.0, 8.0), ('Serbs', 41.8, 15.6, 4.6),
    ('Greeks', 41.6, 16.2, 4.0), ('Bulgarians', 40.6, 14.2, 6.2), ('Arabs', 32.4, 19.0, 5.0),
    ('Turks', 38.0, 18.6, 6.6), ('Russians', 31.2, 21.8, 6.3), ('Jews', 33.0, 23.2, 5.0),
    ('Malagasies', 26.2, 23.7, 4.5), ('Senegalese', 22.6, 29.2, 5.0), ('Annamese', 22.4, 28.4, 7.2),
    ('Indians', 19.0, 41.2, 8.5),
]


def race_serology():
    d = D()
    # Left: the typing as the Hirszfelds did it, a drop of citrated blood with a drop of each test
    # serum in a small tube, read after half an hour. Four rows, one per group: clumps where the
    # serum's antibody meets its antigen, an even suspension where it does not.
    # Right: their race index for the sixteen peoples, on a log scale, in the order they printed
    # them: a slope, with no gap where their "types" were drawn.
    rows = [('O', False, False), ('A', True, False), ('B', False, True), ('AB', True, True)]
    ys = [52, 112, 172, 232]
    xa, xb = 84, 132
    x0, x1 = 222, 378                      # the log axis, index 0.4 to 5
    lo, hi = math.log(0.4), math.log(5.0)

    def ix(v):
        return x0 + (math.log(v) - lo) / (hi - lo) * (x1 - x0)

    py = [48 + k * 13.5 for k in range(len(HIRSZFELD))]
    d.group('thin')
    for y in ys:                                                   # each row's baseline
        d.line((40, y + 44), (156, y + 44))
    for v in (0.5, 1, 2, 4):                                       # gridlines of the log axis
        d.line((ix(v), 40), (ix(v), 262))
    d.line((x0, 262), (x1, 262))
    d.line((190, 30), (190, 280))                                  # the two halves
    d.group()
    for y in ys:
        _tube(d, xa, y)
        _tube(d, xb, y)
    # the index of each people, joined in the printed order
    pts = []
    for (name, a, b, ab), y in zip(HIRSZFELD, py):
        pts.append((ix((a + ab) / (b + ab)), y))
    d.line(*pts)
    d.group('mid')
    for (label, clumps_a, clumps_b), y in zip(rows, ys):
        for x, clumps in ((xa, clumps_a), (xb, clumps_b)):
            if clumps:                                             # agglutinated: clumps on the foot
                for dx, dy, r in ((-3, 30, 2.4), (2.5, 31, 2.0), (0, 26, 1.8), (-1, 21, 1.4), (3, 24, 1.2)):
                    d.circle(x + dx, y + dy, r)
            else:                                                  # even suspension: level hatching
                for k in range(5):
                    yy = y + 12 + k * 5
                    d.line((x - 5, yy), (x + 5, yy))
            d.line((x - 5, y + 9), (x + 5, y + 9))                 # the meniscus
    for x, y in pts:
        d.circle(x, y, 1.8)
    d.group('mid')
    d.text(xa, 40, 'ANTI-A', size=7)
    d.text(xb, 40, 'ANTI-B', size=7)
    for (label, _, _), y in zip(rows, ys):
        d.text(56, y + 26, label, size=7, anchor='end')
    for v, s in ((0.5, '0.5'), (1, '1'), (2, '2'), (4, '4')):
        d.text(ix(v), 274, s, size=7)
    d.text(300, 290, 'INDEX (A+AB)÷(B+AB)', size=7)
    d.text(pts[0][0] - 6, pts[0][1] + 3, 'ENGLISH', size=7, anchor='end')
    d.text(pts[-1][0] + 6, pts[-1][1] + 3, 'INDIANS', size=7, anchor='start')
    return d


def _bottle(d, x, top, w=16, h=26):
    """A donor bottle in elevation: a body, shoulders and a neck."""
    r = w / 2
    d.line((x - 3, top), (x - 3, top + 5), (x - r, top + 9), (x - r, top + h), (x + r, top + h),
           (x + r, top + 9), (x + 3, top + 5), (x + 3, top))


def segregated_blood():
    d = D()
    # Two pooling rigs side by side, identical in every part: donor bottles, a manifold, a pool,
    # the bottles of plasma that leave it. A wall between them, and a tag on one rig's bottle:
    # the only difference the policy made was where a donor's blood went and what its label said.
    # Pools of six to sixty donors are Kendrick's figures; the four bottles here are a sketch.
    d.group('thin')
    d.line((200, 24), (200, 280))                                  # the centre line, later the wall
    for cx in (100, 300):
        d.line((cx, 24), (cx, 280))                                # each rig's axis
        d.line((cx - 80, 92), (cx + 80, 92))                       # the manifold's line
    d.group()
    for cx in (100, 300):
        tops = [cx - 60, cx - 20, cx + 20, cx + 60]
        for x in tops:
            _bottle(d, x, 34)
        d.line((cx - 60, 92), (cx + 60, 92))                       # the manifold
        for x in tops:
            d.line((x, 60), (x, 92))                               # a line from each bottle
        d.line((cx, 92), (cx, 120))
        d.ellipse(cx, 148, 30, 26)                                 # the pool flask
        d.line((cx, 174), (cx, 194))
        d.line((cx - 40, 194), (cx + 40, 194))
        for x in (cx - 40, cx, cx + 40):
            d.line((x, 194), (x, 208))
            _bottle(d, x, 208, w=18, h=40)                         # plasma out, bottled
    d.group('mid')
    for k in range(13):                                            # the wall, dashed
        y = 28 + k * 19
        d.line((200, y), (200, y + 10))
    for cx in (100, 300):
        for k in range(5):                                         # the pooled plasma, level
            y = 140 + k * 6
            half = math.sqrt(max(0.0, 1 - ((y - 148) / 26) ** 2)) * 30 - 3
            d.line((cx - half, y), (cx + half, y))
        for x in (cx - 60, cx - 20, cx + 20, cx + 60):
            _arrow(d, (x, 70), (x, 84), size=4)
        _arrow(d, (cx, 100), (cx, 116), size=4)
    # the tag tied to one rig's bottle
    d.line((350, 228), (360, 220), (388, 220), (388, 236), (360, 236), (350, 228))
    d.circle(356, 228, 1.5)
    d.group('mid')
    d.text(100, 22, 'DONORS', size=7)
    d.text(300, 22, 'DONORS', size=7)
    d.text(134, 128, 'POOL', size=7, anchor='start')
    d.text(334, 128, 'POOL', size=7, anchor='start')
    d.text(374, 231, 'LABEL', size=6)
    d.text(200, 292, 'SAME GROUPING, SAME TESTS: TWO POOLS', size=7)
    return d


PLATES = {'race-serology': race_serology, 'segregated-blood': segregated_blood}
