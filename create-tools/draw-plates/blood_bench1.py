"""Plates for In the Blood's bench segment, first half (sprint 028): the hand methods. See plates_for.py."""
import math
import random
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


def _blob(d, cx, cy, r, rng, n=9):
    """A rough closed clump of radius about r."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (0.75 + 0.5 * rng.random())
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.line(*pts, closed=True)


def hemocytometer():
    d = D()
    # The improved Neubauer ruling, 3 mm square, drawn at 76 px to the millimetre (TM 8-227, 1951):
    # four corner squares of 16 for white cells, the centre millimetre in 25 squares between triple
    # lines, each of 16 small squares (1/400 mm²); red cells are counted in A–E. Beside it, the
    # chamber in section: the platform 0.1 mm below the cover glass (the gap drawn far deeper).
    s, x0, y0 = 76, 20, 30
    X = lambda mm: x0 + s * mm
    Y = lambda mm: y0 + s * mm
    d.group('thin')
    # small squares across the centre millimetre (0.05 mm)
    for i in range(1, 20):
        if i % 4:
            t = 1 + i / 20
            d.line((X(t), Y(1)), (X(t), Y(2)))
            d.line((X(1), Y(t)), (X(2), Y(t)))
    # dimension line for one millimetre, under the grid
    d.line((X(0), Y(3) + 10), (X(1), Y(3) + 10))
    d.line((X(0), Y(3) + 6), (X(0), Y(3) + 14))
    d.line((X(1), Y(3) + 6), (X(1), Y(3) + 14))
    # section construction: the slide's top and the cover's underside carried across
    sx0, sx1 = 266, 384
    d.line((sx0 - 4, 214), (sx1 + 14, 214))
    d.line((sx0 - 4, 222), (sx1 + 14, 222))
    d.group()
    # the 3 mm grid and its millimetre lines
    d.line((X(0), Y(0)), (X(3), Y(0)), (X(3), Y(3)), (X(0), Y(3)), closed=True)
    for k in (1, 2):
        d.line((X(k), Y(0)), (X(k), Y(3)))
        d.line((X(0), Y(k)), (X(3), Y(k)))
    # the section: slide with its two shoulders and moats, the counting platform, the cover glass
    d.line((sx0, 214), (284, 214), (284, 228), (296, 228), (296, 222), (354, 222), (354, 228),
           (366, 228), (366, 214), (sx1, 214), (sx1, 250), (sx0, 250), closed=True)
    d.line((sx0 + 6, 208), (sx1 - 6, 208), (sx1 - 6, 214), (sx0 + 6, 214), closed=True)
    d.group('mid')
    # corner squares in quarters of a millimetre
    for cx, cy in ((0, 0), (2, 0), (0, 2), (2, 2)):
        for j in (0.25, 0.5, 0.75):
            d.line((X(cx + j), Y(cy)), (X(cx + j), Y(cy + 1)))
            d.line((X(cx), Y(cy + j)), (X(cx + 1), Y(cy + j)))
    # the centre millimetre: triple lines every 0.2 mm
    for i in range(6):
        t = 1 + i / 5
        for o in (-0.012, 0, 0.012):
            if 1 <= t + o <= 2:
                d.line((X(t + o), Y(1)), (X(t + o), Y(2)))
                d.line((X(1), Y(t + o)), (X(2), Y(t + o)))
    # the diluted blood under the cover: dots of cells on the platform
    rng = random.Random(1852)
    for _ in range(26):
        x = rng.uniform(298, 352)
        d.circle(x, 219, 0.9)
    d.line((396, 202), (396, 214))
    _arrow(d, (396, 202), (396, 214), 4)
    d.line((396, 234), (396, 222))
    _arrow(d, (396, 234), (396, 222), 4)
    d.group('mid')
    for name, (cx, cy) in zip('ABCDE', ((1, 1), (1.8, 1), (1.4, 1.4), (1, 1.8), (1.8, 1.8))):
        d.text(X(cx + 0.1), Y(cy + 0.1) + 3, name, size=7)
    for cx, cy in ((0.5, 0.5), (2.5, 0.5), (0.5, 2.5), (2.5, 2.5)):
        d.text(X(cx), Y(cy) + 3, 'W', size=7)
    d.text(X(0.5), Y(3) + 24, '1 MM', size=7)
    d.text(X(2), Y(3) + 24, '1/400 MM² EACH', size=7)
    d.text(331, 200, 'COVER GLASS', size=7)
    d.text(380, 262, 'GAP 0.1 MM', size=7, anchor='end')
    d.text(380, 274, 'NOT TO SCALE', size=7, anchor='end')
    d.text(331, 92, '× 5 AREA', size=7)
    d.text(331, 106, '× 10 DEPTH', size=7)
    d.text(331, 120, '× 200 DILUTION', size=7)
    d.text(331, 140, 'A–E: RED CELLS', size=7)
    d.text(331, 154, 'W: WHITE CELLS', size=7)
    return d


def stained_film():
    d = D()
    # Above, the wedge film being pulled: a spreader slide held at 30° on a flat slide, pushed toward
    # the far end, the drop spread along its edge. Below, the film in plan, thick end to feathered
    # edge, with the path a differential count takes back and forth across the thin part.
    d.group('thin')
    d.line((20, 98), (380, 98))                                   # bench line
    ax, ay = 150, 86                                              # where the spreader meets the slide
    d.arc(ax, ay, 26, 180, 210, n=12)                             # the 30° angle, opening back
    d.line((ax, ay), (ax - 34, ay))
    # the counting path's lane, the thin zone, ruled off
    d.line((236, 150), (236, 270))
    d.line((330, 150), (330, 270))
    d.group()
    # the slide in elevation, and the spreader at 30° leaning back over the drop
    d.line((40, 86), (360, 86), (360, 98), (40, 98), closed=True)
    L = 96
    tip = (ax, ay)
    back = (ax - L * math.cos(math.radians(30)), ay - L * math.sin(math.radians(30)))
    n = (6 * math.sin(math.radians(30)), -6 * math.cos(math.radians(30)))   # the slide's thickness
    d.line(tip, back, (back[0] + n[0], back[1] + n[1]), (tip[0] + n[0], tip[1] + n[1]), closed=True)
    # the film in plan: a tongue, wide and square at the drop end, rounding to a feathered edge
    top, bot, xa = 160, 260, 60
    pts = [(xa, top)]
    for i in range(0, 41):
        a = -90 + 180 * i / 40
        pts.append((250 + 90 * math.cos(math.radians(a)), 210 + 50 * math.sin(math.radians(a))))
    pts.append((xa, bot))
    d.line(*pts, closed=True)
    d.line((30, 150), (370, 150), (370, 270), (30, 270), closed=True)   # the slide in plan
    d.group('mid')
    # the drop smeared along the spreader's edge, and the push
    d.ellipse(ax + 4, 83, 6, 2.5)
    d.line((176, 70), (230, 70))
    _arrow(d, (176, 70), (230, 70))
    # thickness: hatching that thins out toward the feathered edge
    for k, x in enumerate(range(70, 236, 12)):
        gap = 4 + k * 1.1
        y = top + 6
        while y < bot - 4:
            d.line((x, y), (x + 3, y + 3))
            y += gap
    # the counting path: back and forth across the thin zone, stepping toward the edge
    path, x, down = [], 242, True
    while x <= 324:
        half = 50 * math.sqrt(max(0.0, 1 - ((x - 250) / 90) ** 2)) if x > 250 else 50
        ylo, yhi = 210 - half + 8, 210 + half - 8
        path += [(x, ylo), (x, yhi)] if down else [(x, yhi), (x, ylo)]
        x += 12
        down = not down
    d.line(*path)
    d.group('mid')
    d.text(ax - 44, ay - 4, '30°', size=7, anchor='end')
    d.text(203, 62, 'PUSH', size=7)
    d.text(60, 116, 'SPREADER ON SLIDE, IN ELEVATION', size=7, anchor='start')
    d.text(60, 286, 'THICK END', size=7, anchor='start')
    d.text(283, 286, 'COUNT 100 CELLS HERE', size=7)
    d.text(352, 140, 'FEATHERED EDGE', size=7, anchor='end')
    return d


def hematocrit():
    d = D()
    # The Wintrobe tube after its spin, drawn 20 px to the centimetre (its bore much widened): two
    # scales, 0–10 down for sedimentation and 0–10 up for packed cells; an invented reading of 4.5
    # (45%) under a thin white layer. Beside it the centrifuge head in plan, 9 cm to each cup's
    # centre, at 3,000 rpm. Proportions of the cups are a sketch.
    cm = 20
    tx0, tx1 = 92, 116                     # the tube's walls
    yb = 262                               # the bottom of the bore
    Y = lambda c: yb - c * cm              # height above the bottom, in cm
    d.group('thin')
    for k in range(0, 11):
        d.line((tx0 - 14, Y(k)), (tx0 - 4, Y(k)))
        d.line((tx1 + 4, Y(k)), (tx1 + 14, Y(k)))
        if k < 10:
            for m in range(1, 10):
                h = Y(k + m / 10)
                w = 6 if m == 5 else 3
                d.line((tx0 - 4 - w, h), (tx0 - 4, h))
                d.line((tx1 + 4, h), (tx1 + 4 + w, h))
    cx, cy, R = 290, 150, 90
    d.circle(cx, cy, R)
    d.line((cx - R - 10, cy), (cx + R + 10, cy))
    d.line((cx, cy - R - 10), (cx, cy + R + 10))
    d.group()
    # the tube: sealed flat at the foot, open and lipped at the top, 11 cm long
    d.line((tx0 - 3, Y(10.6)), (tx0, Y(10.5)), (tx0, yb + 4), (tx1, yb + 4), (tx1, Y(10.5)),
           (tx1 + 3, Y(10.6)))
    d.line((tx0, Y(10)), (tx1, Y(10)))                            # the plasma meniscus at 10
    d.line((tx0, Y(4.55)), (tx1, Y(4.55)))                        # top of the white layer
    d.line((tx0, Y(4.5)), (tx1, Y(4.5)))                          # top of the red cells
    # the head: a hub, four arms and four swinging cups
    d.circle(cx, cy, 14)
    for a in (45, 135, 225, 315):
        p0 = _pt(cx, cy, 14, a)
        p1 = _pt(cx, cy, R - 12, a)
        d.line(p0, p1)
        c = _pt(cx, cy, R, a)
        d.circle(c[0], c[1], 12)
    d.group('mid')
    # packed red cells, hatched
    y = Y(4.5) + 5
    while y < yb:
        d.line((tx0 + 2, y + 3), (tx1 - 2, y - 3))
        y += 5
    # the radius and the rotation
    d.line((cx, cy), _pt(cx, cy, R, -45))
    arc = [_pt(cx, cy, R + 18, a) for a in range(-150, -100, 5)]
    d.line(*arc)
    _arrow(d, arc[-2], arc[-1])
    d.group('mid')
    d.text(tx0 - 18, Y(0) + 3, '10', size=7, anchor='end')
    d.text(tx0 - 18, Y(10) + 3, '0', size=7, anchor='end')
    d.text(tx1 + 18, Y(10) + 3, '10', size=7, anchor='start')
    d.text(tx1 + 18, Y(0) + 3, '0', size=7, anchor='start')
    d.text(tx1 + 18, Y(4.5) + 3, '4.5 → 45%', size=7, anchor='start')
    d.text(tx0 - 18, Y(7.3) + 3, 'PLASMA', size=7, anchor='end')
    d.text(tx0 - 18, Y(2.2) + 3, 'RED CELLS', size=7, anchor='end')
    d.text(tx1 + 18, Y(5.2) + 3, 'WHITE LAYER', size=7, anchor='start')
    d.text(104, 22, 'ESR ↓   PCV ↑', size=7)
    p = _pt(cx, cy, R / 2, -45)
    d.text(p[0] + 8, p[1] + 10, 'R = 9 CM', size=7, anchor='start')
    d.text(cx, cy + R + 30, '3,000 RPM · 30 MIN', size=7)
    return d


def tube_typing():
    d = D()
    # The grading scale as a rack of seven tubes, each after its spin and a gentle shake, from one
    # solid clump (4+) to a smooth suspension (0), and H, hemolysis, its supernatant tinted; above
    # them, the phases of a full crossmatch in order. Clumps are drawn from a seeded random, not data.
    rng = random.Random(1951)
    n, x0, gap, w = 7, 40, 52, 26
    top, bot = 120, 248
    d.group('thin')
    d.line((20, bot + 18), (380, bot + 18))                       # the rack's floor
    d.line((20, top + 22), (380, top + 22))                       # the rack's upper rail
    d.line((20, 66), (380, 66))                                   # the phase line
    for i in range(5):
        d.line((44 + 78 * i, 62), (44 + 78 * i, 70))
    d.group()
    xs = [x0 + gap * i for i in range(n)]
    for x in xs:
        d.line((x, top), (x, bot - w / 2))
        d.arc(x + w / 2, bot - w / 2, w / 2, 180, 0, n=16)
        d.line((x + w, bot - w / 2), (x + w, top))
        d.line((x + 2, top + 40), (x + w - 2, top + 40))         # the liquid's surface
    d.group('mid')
    # contents: the reaction graded by eye
    specs = [('4+', [(1, 9)]), ('3+', [(3, 6)]), ('2+', [(6, 4)]), ('1+', [(12, 2.2)]),
             ('W+', [(18, 1.3)]), ('0', []), ('H', [])]
    for x, (g, groups) in zip(xs, specs):
        cx = x + w / 2
        for count, r in groups:
            for _ in range(count):
                px = cx + rng.uniform(-w / 2 + r + 2, w / 2 - r - 2)
                py = rng.uniform(top + 52 + r, bot - 6 - r)
                _blob(d, px, py, r, rng)
        if g in ('1+', 'W+', '0'):                                # free cells in suspension
            for _ in range(22 if g == '0' else 12):
                d.circle(cx + rng.uniform(-w / 2 + 3, w / 2 - 3), rng.uniform(top + 46, bot - 6), 0.7)
        if g == 'H':                                              # hemolysis: the fluid itself tinted
            for k in range(6):
                y = top + 54 + 12 * k
                d.line((x + 3, y + 5), (x + w - 3, y - 1))
    # the phases, with an arrow running through them
    d.line((44, 66), (360, 66))
    _arrow(d, (340, 66), (362, 66))
    d.group('mid')
    for x, (g, _) in zip(xs, specs):
        d.text(x + w / 2, bot + 34, g, size=7)
    for i, lab in enumerate(('IMMEDIATE SPIN', '37 °C ALBUMIN', 'WASH ×3', 'AHG', 'CHECK CELLS')):
        d.text(44 + 78 * i, 54 if i % 2 == 0 else 86, lab, size=7)
    d.text(200, 292, 'GRADED BY EYE AFTER THE SPIN', size=7)
    return d


PLATES = {
    'hemocytometer': hemocytometer,
    'stained-film': stained_film,
    'hematocrit': hematocrit,
    'tube-typing': tube_typing,
}
