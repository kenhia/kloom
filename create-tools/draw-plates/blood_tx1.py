"""Plates for In the Blood's Transfusion segment, part tx1 (sprint 028): the first transfusions,
Blundell's Gravitator and Landsteiner's groups. See plates_for.py."""
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


def _tube(d, pts, w):
    """A tube of width w along a polyline: its two walls, offset either side of the centre line."""
    def offset(sign):
        out = []
        for i, p in enumerate(pts):
            a = pts[max(i - 1, 0)]
            b = pts[min(i + 1, len(pts) - 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]
            n = math.hypot(dx, dy) or 1
            out.append((p[0] - sign * w / 2 * dy / n, p[1] + sign * w / 2 * dx / n))
        return out
    d.line(*offset(1))
    d.line(*offset(-1))


def abo():
    d = D()
    # Landsteiner's three groups as a grid of hanging drops: serum of each group (rows) on the
    # cells of each group (columns). Cells clumped where the serum carries the agglutinin the
    # cells are sensitive to; evenly spread where not. Group C's cells are clumped by no serum.
    groups = ['A', 'B', 'C']
    xs, ys, r = [150, 230, 310], [78, 158, 238], 31
    clumps = {('A', 'B'), ('B', 'A'), ('C', 'A'), ('C', 'B')}       # (serum, cells)
    rnd = random.Random(1901)
    d.group('thin')
    for x in xs:
        d.line((x, 44), (x, 280))
    for y in ys:
        d.line((70, y), (350, y))
    d.line((110, 44), (110, 280))                                    # the serum column's rule
    d.group()
    for y in ys:
        for x in xs:
            d.circle(x, y, r)
    d.group('mid')
    for i, sg in enumerate(groups):
        for j, cg in enumerate(groups):
            cx, cy = xs[j], ys[i]
            if (sg, cg) in clumps:
                # three or four clumps, each a packed rosette of cells
                centres = [_pt(cx, cy, 15.5, a) for a in (rnd.uniform(0, 360) + k * 120 for k in range(3))]
                for (px, py) in centres:
                    d.circle(px, py, 2.1)
                    for a in range(0, 360, 60):
                        qx, qy = _pt(px, py, 4.3, a + rnd.uniform(-8, 8))
                        d.circle(qx, qy, 2.1)
            else:
                # cells spread evenly: a jittered lattice inside the drop
                for gx in range(-24, 25, 9):
                    for gy in range(-24, 25, 9):
                        px, py = cx + gx + rnd.uniform(-2.5, 2.5), cy + gy + rnd.uniform(-2.5, 2.5)
                        if math.hypot(px - cx, py - cy) < r - 5:
                            d.circle(px, py, 2.1)
    d.group('mid')
    d.text(230, 18, 'CELLS OF GROUP', size=7)
    for x, g in zip(xs, groups):
        d.text(x, 38, g, size=7)
    d.text(90, 38, 'SERUM', size=7)
    for y, g in zip(ys, groups):
        d.text(90, y + 3, g, size=7)
    return d


def early_transfusion():
    d = D()
    # Lower's method of 1666 in plan: the donor dog's carotid artery, tied above and held by a
    # running knot below, opened onto a quill; the recipient's jugular vein opened onto two quills,
    # one carrying the donor's blood down towards the heart, one letting the recipient's own blood
    # out from the head into a dish. Quills joined end to end bridge the gap. Not to scale.
    art_y, vein_y = 92, 212
    d.group('thin')
    d.line((20, 150), (380, 150))                                   # the line between the two dogs
    for x in (96, 128, 268, 300, 334):
        d.line((x, 40), (x, 270))
    d.group()
    # the carotid artery of the donor (above), running left to right towards the donor's heart
    _tube(d, [(30, art_y), (230, art_y)], 12)
    # the recipient's jugular vein (below): head on the left, heart on the right
    _tube(d, [(30, vein_y), (370, vein_y)], 14)
    # the quill from the artery, bent down to the vein's lower (heart-ward) quill
    quill = [(128, art_y), (128, 120), (150, 150), (268, 180), (268, vein_y)]
    _tube(d, quill, 5)
    # the second quill in the vein, from the head-ward part, out into a dish
    out = [(96, vein_y), (96, 240), (110, 262)]
    _tube(d, out, 5)
    d.arc(132, 268, 28, 0, 180, n=24, ry=10)
    d.line((104, 268), (160, 268))
    d.group('mid')
    # ligatures: a fast tie on the artery above (left), a running knot below; two on the vein
    for x, kind in ((96, 'fast'), (160, 'run'), (232, 'run'), (300, 'run')):
        y = art_y if x < 200 else vein_y
        h = 9 if x < 200 else 10
        d.line((x - 3, y - h), (x + 3, y + h))
        d.line((x + 3, y - h), (x - 3, y + h))
        if kind == 'run':
            d.circle(x, y - h - 3, 2.5)
    # joints between quills, where one is pushed into the next
    for p in ((150, 150), (209, 165)):
        d.circle(p[0], p[1], 4.5)
    # the flow
    _arrow(d, (190, art_y), (222, art_y))
    _arrow(d, (310, vein_y), (350, vein_y))
    _arrow(d, (268, 186), (268, 204))
    _arrow(d, (60, vein_y), (84, vein_y))
    d.group('mid')
    d.text(30, art_y - 14, 'DONOR: CAROTID ARTERY', size=7, anchor='start')
    d.text(370, vein_y + 24, 'RECIPIENT: JUGULAR VEIN', size=7, anchor='end')
    d.text(214, 140, 'QUILLS', size=7)
    d.text(132, 290, 'OWN BLOOD OUT', size=7)
    d.text(370, vein_y - 14, 'TO HEART', size=7, anchor='end')
    d.text(30, vein_y - 14, 'FROM HEAD', size=7, anchor='start')
    return d


def blundell():
    d = D()
    # The Gravitator in elevation (The Lancet, 13 June 1829): the donor's blood runs from his arm
    # into a cone-shaped receiver, through a stop-cock and a flexible canula to a silver tubule in
    # the patient's vein. Gravity drives it; the height h of the receiver above the arm, and the
    # cock, set the rate. A line in the receiver marks two fluid ounces. Not to scale.
    arm_y = 250
    rx, ry = 150, 70                                                  # the receiver's rim centre
    d.group('thin')
    d.line((40, arm_y), (370, arm_y))                                 # the level of the patient's vein
    d.line((rx, ry + 62), (rx, arm_y))
    d.line((rx - 70, ry), (370, ry))
    # the head h, dimensioned
    d.line((60, ry + 62), (60, arm_y))
    _arrow(d, (60, 160), (60, ry + 62), 4)
    _arrow(d, (60, 160), (60, arm_y), 4)
    d.group()
    # the receiver: a cone, rim at ry, apex at ry + 54, a short stem to the cock
    d.line((rx - 30, ry), (rx, ry + 54), (rx + 30, ry))
    d.arc(rx, ry, 30, 180, 360, n=24, ry=6)
    d.arc(rx, ry, 30, 0, 180, n=24, ry=6)
    d.line((rx, ry + 54), (rx, ry + 62))
    # the stop-cock: a barrel with its key
    d.circle(rx, ry + 67, 5)
    d.line((rx - 9, ry + 67), (rx + 9, ry + 67))
    # the flexible canula: a falling curve from the cock to the tubule over the vein
    pts = []
    for i in range(41):
        t = i / 40
        x = rx + 140 * t
        y = ry + 72 + (arm_y - 16 - ry - 72) * (t * t * (3 - 2 * t))
        pts.append((x + 8 * math.sin(math.pi * t), y))
    _tube(d, pts, 4)
    # the silver tubule entering the vein at a slant, and the patient's arm in section
    d.line((290, arm_y - 16), (306, arm_y - 2), (330, arm_y + 2))
    d.ellipse(320, arm_y + 4, 50, 14)
    # the flexible arm-support, clamped to a chair back (right), holding the receiver
    d.line((rx + 30, ry + 8), (240, ry + 22), (330, ry + 8), (360, ry + 40))
    d.line((350, ry + 40), (370, ry + 40), (370, ry + 70), (350, ry + 70), closed=True)
    d.group('mid')
    # the two-ounce line inside the cone, and the blood standing below it
    d.line((rx - 14, ry + 29), (rx + 14, ry + 29))
    for k in range(5):
        y = ry + 34 + k * 4
        half = 30 * (ry + 54 - y) / 54
        d.line((rx - half + 1, y), (rx + half - 1, y))
    # the donor's arm above the receiver, a stream falling into it
    d.ellipse(118, 26, 44, 9)
    d.line((132, 34), (138, 50), (142, ry - 2))
    _arrow(d, (138, 50), (142, ry - 2), 4)
    _arrow(d, (rx + 60, 160), (rx + 74, 178), 4)
    d.group('mid')
    d.text(rx + 36, ry - 8, 'RECEIVER', size=7, anchor='start')
    d.text(rx - 20, ry + 31, '2 OZ', size=7, anchor='end')
    d.text(rx - 10, ry + 70, 'COCK', size=7, anchor='end')
    d.text(66, 165, 'h', size=7, anchor='start')
    d.text(370, arm_y + 32, 'PATIENT\'S VEIN', size=7, anchor='end')
    d.text(40, 18, 'DONOR', size=7, anchor='start')
    return d


PLATES = {'early-transfusion': early_transfusion, 'blundell': blundell, 'abo': abo}
