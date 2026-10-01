"""Plates for In the Blood's Transfusion segment, part tx2 (sprint 028): citrate, robertson-depot,
blood-banks and drew-plasma. See plates_for.py."""
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


def _bottle(cx, base, w, body, shoulder, neck_w, neck_h, n=10):
    """A bottle's outline in section, as one open polyline from the lip down the left side, across
    the foot and up the right: a cylinder `body` high, an elliptical shoulder `shoulder` high, and a
    neck. Returns the points."""
    hw, nw = w / 2, neck_w / 2
    top = base - body
    left = [(cx - nw, top - shoulder - neck_h), (cx - nw, top - shoulder)]
    # the shoulder: a quarter ellipse from the neck out to the body's wall
    for i in range(1, n + 1):
        t = math.pi / 2 * i / n
        left.append((cx - nw - (hw - nw) * math.sin(t), top - shoulder * math.cos(t)))
    left += [(cx - hw, base - 4), (cx - hw + 4, base)]
    right = [(2 * cx - x, y) for x, y in reversed(left)]
    return left + right


def _level(base, cc, per_cc):
    """The height of `cc` of fluid in a cylindrical body (y of its surface)."""
    return base - cc * per_cc


def robertson_depot():
    d = D()
    # Robertson's procedure (BMJ, 22 June 1918) in three bottles on one bench line, each in section.
    # 1. The two-litre bleeding bottle: 850 c.c. dextrose (mark A), 350 c.c. citrate added (mark B),
    #    500 c.c. of blood taken (mark C). Body height is proportional to volume.
    # 2. The same bottle after four to five days on ice: the cells settled, the clear fluid above,
    #    and the siphon that draws the fluid off. The sediment's height is a sketch, not a figure.
    # 3. The transfusion bottle, made up to 1,000 c.c. and warmed in a jar of water.
    base = 262
    per_cc = 0.085                        # px per c.c. in bottles 1 and 2
    b1, b2, b3 = 74, 200, 322
    w, body = 76, 1800 * per_cc           # a body holding 1,800 c.c. below the shoulder
    lvA, lvB, lvC = (_level(base, v, per_cc) for v in (850, 1200, 1700))
    sed = _level(base, 520, per_cc)       # top of the settled cells (sketch)
    d.group('thin')
    d.line((20, base), (380, base))                                   # the bench
    for y in (lvA, lvB, lvC):                                         # the marks carried across
        d.line((b1 - w / 2 - 14, y), (b2 + w / 2 + 8, y))
    d.line((b1 - w / 2 - 22, base), (b1 - w / 2 - 22, lvC))           # a volume scale
    for v in range(0, 1701, 250):
        y = _level(base, v, per_cc)
        d.line((b1 - w / 2 - 26, y), (b1 - w / 2 - 22, y))
    d.group()
    d.line(*_bottle(b1, base, w, body, 26, 22, 14))
    d.line(*_bottle(b2, base, w, body, 26, 22, 14))
    # the transfusion bottle: a wide-mouthed quart, in a glass jar of warm water
    w3, body3 = 64, 104
    d.line(*_bottle(b3, base - 6, w3, body3, 14, 34, 10))
    d.line((b3 - 48, base - 150), (b3 - 48, base), (b3 + 48, base), (b3 + 48, base - 150))
    d.group('mid')
    # bottle 1: the three fluids, the dextrose and citrate as dashed levels, the blood mixed in
    for y in (lvA, lvB):
        for x0 in range(int(b1 - w / 2 + 3), int(b1 + w / 2 - 6), 9):
            d.line((x0, y), (x0 + 5, y))
    d.line((b1 - w / 2, lvC), (b1 + w / 2, lvC))
    # stopper and the glass inlet tube down to below the fluid, out to the needle
    top1 = base - body - 26 - 14
    d.line((b1 - 11, top1 + 10), (b1 - 11, top1 - 2), (b1 + 11, top1 - 2), (b1 + 11, top1 + 10))
    d.line((b1 + 3, lvB + 8), (b1 + 3, top1 - 14), (b1 + 30, top1 - 22), (b1 + 50, top1 - 8))
    d.line((b1 - 5, top1 + 14), (b1 - 5, top1 - 12), (b1 - 28, top1 - 12), (b1 - 52, top1 + 6))
    d.ellipse(b1 - 52, top1 + 18, 6, 12)                              # the suction bulb
    d.line((b1 + 50, top1 - 8), (b1 + 58, top1 + 8))                  # the needle
    # bottle 2: the cell sediment hatched, the clear fluid line, the siphon
    for k, y in enumerate(range(int(sed) + 4, base - 2, 6)):
        d.line((b2 - w / 2 + 2 + (k % 2) * 4, y), (b2 + w / 2 - 2, y))
    d.line((b2 - w / 2, sed), (b2 + w / 2, sed))
    d.line((b2 - w / 2, lvC), (b2 + w / 2, lvC))
    top2 = base - body - 26 - 14
    d.line((b2 - 11, top2 + 10), (b2 - 11, top2 - 2), (b2 + 11, top2 - 2), (b2 + 11, top2 + 10))
    d.line((b2, sed - 4), (b2, top2 - 14), (b2 + 46, top2 - 14), (b2 + 46, top2 + 30))
    _arrow(d, (b2 + 46, top2 + 10), (b2 + 46, top2 + 30))
    # bottle 3: the 1,000 c.c. line, the water in the jar, the outlet tube to the vein
    lv3 = base - 6 - body3 * 0.78
    d.line((b3 - w3 / 2, lv3), (b3 + w3 / 2, lv3))
    for x0 in range(b3 - 46, b3 + 44, 8):
        d.line((x0, base - 128), (x0 + 4, base - 128))
    top3 = base - 6 - body3 - 14 - 10
    d.line((b3 + 6, base - 14), (b3 + 6, top3 - 10), (b3 + 40, top3 - 22), (b3 + 62, top3 - 8))
    _arrow(d, (b3 + 40, top3 - 22), (b3 + 62, top3 - 8))
    # arrows from one step to the next
    for xa, xb in ((b1 + w / 2 + 6, b2 - w / 2 - 6), (b2 + w / 2 + 14, b3 - 52)):
        d.line((xa, base - 40), (xb, base - 40))
        _arrow(d, (xa, base - 40), (xb, base - 40))
    d.group('mid')
    d.text(b1 + w / 2 + 3, lvA + 3, 'A', size=7, anchor='start')
    d.text(b1 + w / 2 + 3, lvB + 3, 'B', size=7, anchor='start')
    d.text(b1 + w / 2 + 3, lvC + 3, 'C', size=7, anchor='start')
    d.text(b1, (base + lvA) / 2 + 3, '850', size=7)
    d.text(b1, (lvA + lvB) / 2 + 3, '+350', size=7)
    d.text(b1, (lvB + lvC) / 2 + 3, '+500', size=7)
    d.text(b2, (lvC + sed) / 2 + 3, 'FLUID', size=7)
    d.text(b2, base + 14, 'ON ICE, 4–5 DAYS', size=7)
    d.text(b1, base + 14, 'BLEED 500 C.C.', size=7)
    d.text(b3, lv3 - 5, '1,000', size=7)
    d.text(b3, base + 14, '106 °F', size=7)
    return d


def _tube(d, cx, top, bottom, r):
    """A test tube in elevation: two walls and a round foot."""
    d.line((cx - r, top), (cx - r, bottom))
    d.arc(cx, bottom, r, 180, 0, n=12)
    d.line((cx + r, bottom), (cx + r, top))


def citrate():
    d = D()
    # Lewisohn's first experiment (Medical Record, 23 January 1915): ten tubes, each with 10 c.c. of
    # dog's blood and 0.1 to 1.0 c.c. of 10 per cent sodium citrate. The first clotted in about five
    # minutes like normal blood; the rest stayed liquid for over 48 hours. Beside the rack, a sketch of
    # citrate holding a calcium ion by its three carboxylate groups (schematic, not a structure).
    x0, dx, r = 26, 21, 6
    top, bottom, level = 96, 206, 128
    xs = [x0 + i * dx for i in range(10)]
    d.group('thin')
    d.line((14, 232), (238, 232))                                     # the bench
    d.line((14, level), (238, level))                                 # the fill line, carried across
    d.line((xs[0] + dx / 2, 96), (xs[0] + dx / 2, 240))               # the threshold, between 0.1 and 0.2
    cx, cy = 318, 150
    d.circle(cx, cy, 30)                                              # the reach of the three groups
    d.group()
    for x in xs:
        _tube(d, x, top, bottom, r)
    for y0, y1 in ((104, 112), (196, 204)):                           # the rack's two rails, broken by the tubes
        edges = [14] + [v for x in xs for v in (x - r - 1, x + r + 1)] + [238]
        d.lines([[(edges[i], y0), (edges[i + 1], y0)] for i in range(0, len(edges), 2)]
                + [[(edges[i], y1), (edges[i + 1], y1)] for i in range(0, len(edges), 2)])
        d.lines([[(14, y0), (14, y1)], [(238, y0), (238, y1)]])
    d.line((14, 112), (14, 232))
    d.line((238, 112), (238, 232))
    # citrate's carbon chain, and the calcium it holds
    c1, c2, c3 = (288, 196), (318, 206), (348, 196)
    d.line(c1, c2, c3)
    d.circle(cx, cy, 9)
    d.group('mid')
    # tube 1: clotted, hatched solid; tubes 2-10: liquid, a meniscus and a few level lines
    for k, y in enumerate(range(level + 4, bottom + 4, 5)):
        d.line((xs[0] - r + 1, y), (xs[0] + r - 1, y - 4))
    for x in xs[1:]:
        d.arc(x, level - 2, r, 0, 180, n=8, ry=2.5)
        for y in range(level + 14, bottom, 16):
            d.line((x - r + 2, y), (x + r - 2, y))
    # the carboxylate arms, each reaching to the calcium
    for c, a in ((c1, 150), (c2, 90), (c3, 30)):
        o = (cx + 22 * math.cos(math.radians(a)), cy + 22 * math.sin(math.radians(a)))
        d.line(c, o)
        d.circle(o[0], o[1], 3)
        p = (cx + 10 * math.cos(math.radians(a)), cy + 10 * math.sin(math.radians(a)))
        for t0 in (0.15, 0.55):
            d.line((o[0] + (p[0] - o[0]) * t0, o[1] + (p[1] - o[1]) * t0),
                   (o[0] + (p[0] - o[0]) * (t0 + 0.25), o[1] + (p[1] - o[1]) * (t0 + 0.25)))
    d.group('mid')
    for i, x in enumerate(xs):
        d.text(x, 248, f'{(i + 1) / 10:.1f}', size=7)
    d.text(xs[0], 88, 'CLOT', size=7)
    d.text((xs[1] + xs[-1]) / 2, 88, 'LIQUID AT 48 H', size=7)
    d.text(126, 266, 'C.C. OF 10% CITRATE IN 10 C.C.', size=7)
    d.text(cx, cy + 3, 'Ca', size=7)
    d.text(cx, 230, 'CITRATE', size=7)
    return d


def _flask(cx, base, w, h, neck_w, neck_h):
    """An Erlenmeyer flask in elevation: a cone with a rounded heel and a straight neck."""
    hw, nw = w / 2, neck_w / 2
    shoulder = base - h
    return [(cx - nw, shoulder - neck_h), (cx - nw, shoulder), (cx - hw + 3, base - 4), (cx - hw + 7, base),
            (cx + hw - 7, base), (cx + hw - 3, base - 4), (cx + nw, shoulder), (cx + nw, shoulder - neck_h)]


def _fill_y(base, w, h, neck_w, frac):
    """Height of a fill that is `frac` of a cone flask's body volume (frustum, solved numerically)."""
    r0, r1 = w / 2 - 3, neck_w / 2
    def vol(y):                                   # volume from the base up to height y (pi left out)
        n = 200
        return sum(((r0 + (r1 - r0) * (i + 0.5) / n * y / h) ** 2) * y / n for i in range(n))
    total, lo, hi = vol(h), 0.0, h
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if vol(mid) < frac * total else (lo, mid)
    return base - lo


def blood_banks():
    d = D()
    # Fantus's Cook County bank (JAMA, 10 July 1937) as a procedure: the deposit flask (500 c.c.,
    # 70 c.c. of 2.5% citrate at the bottom, two 5 c.c. tubes for typing and the Wassermann), the
    # refrigerator at 4-6 degrees C with flasks credited by service, and the ledger, deposits in and
    # withdrawals out. The flask's 70 c.c. line is computed for a cone; the ledger's rows are a sketch.
    base = 250
    fx, fw, fh = 64, 76, 92
    d.group('thin')
    d.line((16, base), (384, base))
    d.line((fx, base - fh - 40), (fx, base + 6))                       # the flask's axis
    y70 = _fill_y(base, fw, fh, 18, 70 / 500)
    y500 = _fill_y(base, fw, fh, 18, 1.0) + 2
    for y in (y70,):
        d.line((fx - fw / 2 - 10, y), (fx + fw / 2 + 10, y))
    # the ledger's ruling
    lx0, lx1, ly0, ly1 = 280, 376, 104, 236
    cols = [lx0, 320, 344, lx1]
    for x in cols[1:-1]:
        d.line((x, ly0), (x, ly1))
    for y in range(ly0 + 22, ly1, 16):
        d.line((lx0, y), (lx1, y))
    d.group()
    d.line(*_flask(fx, base, fw, fh, 18, 30))
    # the refrigerator: a box with two shelves and a door hinge
    rx0, rx1, ry0 = 132, 238, 92
    d.line((rx0, base), (rx0, ry0), (rx1, ry0), (rx1, base))
    d.line((rx0, 150), (rx1, 150))
    d.line((rx0, 204), (rx1, 204))
    # the ledger page
    d.line((lx0, ly0), (lx1, ly0), (lx1, ly1), (lx0, ly1), closed=True)
    d.group('mid')
    # the citrate in the flask, and the two test tubes tied to its neck
    d.line((fx - fw / 2 + 6, y70), (fx + fw / 2 - 6, y70))
    for k, y in enumerate(range(int(y70) + 4, base - 1, 4)):
        d.line((fx - fw / 2 + 5 + k, y), (fx + fw / 2 - 5 - k, y))
    for tx in (fx - 26, fx + 26):
        d.line((tx - 4, base - fh - 26), (tx - 4, base - fh + 14))
        d.arc(tx, base - fh + 14, 4, 180, 0, n=8)
        d.line((tx + 4, base - fh + 14), (tx + 4, base - fh - 26))
        d.line((tx + (4 if tx < fx else -4), base - fh - 20), (fx + (-9 if tx < fx else 9), base - fh - 30))
    # small flasks on the shelves, three to a shelf
    for sy in (150, 204, base):
        for k in range(3):
            cx = rx0 + 20 + k * 33
            d.line(*_flask(cx, sy - 1, 22, 26, 8, 10))
    # the thermometer on the door
    d.line((rx1 - 8, ry0 + 12), (rx1 - 8, ry0 + 44))
    d.circle(rx1 - 8, ry0 + 48, 3)
    # ledger entries: a tick in IN for a deposit, in OUT for a withdrawal
    rows = [(1, 0), (1, 0), (0, 1), (1, 0), (0, 1), (0, 1)]
    for i, (a, b) in enumerate(rows):
        y = ly0 + 22 + 16 * i + 10
        x = 328 if a else 356
        d.line((x, y), (x + 8, y - 6))
    # deposit and withdrawal arrows
    for (x0, y0), (x1, y1) in (((fx + fw / 2 + 2, 170), (rx0 - 4, 170)), ((rx1 + 6, 170), (lx0 - 6, 170))):
        d.line((x0, y0), (x1, y1))
        _arrow(d, (x0, y0), (x1, y1))
    d.group('mid')
    d.text(fx, base + 14, '500 C.C. FLASK', size=7)
    d.text(fx, base + 26, '70 C.C. CITRATE', size=7)
    d.text(fx, base - fh - 46, 'TYPING · WASSERMANN', size=7)
    d.text((rx0 + rx1) / 2, base + 14, '4–6 °C', size=7)
    d.text((rx0 + rx1) / 2, 84, 'CREDITED', size=7)
    d.text(cols[0] + 20, ly0 + 15, 'WARD', size=7)
    d.text(332, ly0 + 15, 'IN', size=7)
    d.text(358, ly0 + 15, 'OUT', size=7)
    d.text((lx0 + lx1) / 2, base + 14, 'LEDGER', size=7)
    d.text((fx + fw / 2 + rx0) / 2 - 2, 160, 'DEPOSIT', size=7)
    d.text((rx1 + lx0) / 2, 162, 'DRAW', size=7)
    return d


def drew_plasma():
    d = D()
    # Blood for Britain's pooling line (the Blood Transfusion Betterment Association's report of
    # 31 January 1941): settled donor bottles, plasma over cells; siphon lines through a three-way
    # stopcock and a 120-mesh steel filter into a two-litre pooling flask under a hood; a water trap
    # and cotton filter between the flask and the vacuum pump; then the Baxter bottle, 500 c.c. of
    # saline under vacuum with 500 c.c. of plasma run in. Not to scale.
    base = 258
    per = 0.05                                   # px per c.c. in the donor bottles
    xs = [34, 70, 106]
    bw, bh = 26, 600 * per + 40
    d.group('thin')
    d.line((16, base), (384, base))
    hood = [(150, 86), (176, 56), (264, 56), (290, 86)]
    d.line(*hood)                                                     # the hood's outline
    d.line((150, 86), (150, base))
    d.line((290, 86), (290, base))
    for x in xs:                                                      # the cell line in each donor bottle
        d.line((x - bw / 2 - 4, base - 260 * per - 10), (x + bw / 2 + 4, base - 260 * per - 10))
    d.group()
    for x in xs:
        d.line(*_bottle(x, base, bw, bh, 8, 8, 6, n=6))
    # the pooling flask: a two-litre bottle on the bench under the hood
    px = 220
    d.line(*_bottle(px, base, 58, 88, 16, 14, 10, n=8))
    # the water trap, outside the hood, and the line on to the pump
    tx = 316
    d.line(*_bottle(tx, base, 22, 34, 8, 8, 6, n=6))
    # the final Baxter bottle
    fx = 362
    d.line(*_bottle(fx, base, 34, 76, 12, 10, 8, n=6))
    d.group('mid')
    # donor bottles: cells hatched below the line, a siphon tube from each plasma layer
    cy = base - 260 * per - 10
    for x in xs:
        for k, y in enumerate(range(int(cy) + 4, base - 2, 4)):
            d.line((x - bw / 2 + 2, y), (x + bw / 2 - 2, y))
    sx, sy = 152, 132                                                 # the stopcock
    for x in xs:
        top = base - bh - 14
        d.line((x, cy - 6), (x, top - 8), (sx - 18, sy - 10 + (x - 70) / 6), (sx - 6, sy))
    d.circle(sx, sy, 6)
    d.line((sx - 4, sy - 4), (sx + 4, sy + 4))
    # the filter, then down into the pool
    d.line((sx + 6, sy), (176, sy))
    d.line((176, sy - 6), (184, sy - 6), (184, sy + 6), (176, sy + 6), closed=True)
    for k in range(3):
        d.line((178 + 2 * k, sy - 6), (178 + 2 * k, sy + 6))
    d.line((184, sy), (px - 4, sy), (px - 4, base - 30))
    _arrow(d, (px - 4, base - 60), (px - 4, base - 30))
    # the pooled plasma's level, and the vacuum line out to the trap and on
    pl = base - 40
    d.line((px - 27, pl), (px + 27, pl))
    d.line((px + 4, base - 100), (px + 4, sy), (tx, sy), (tx, base - 44))
    d.line((tx + 4, base - 56), (tx + 4, 112), (tx + 30, 112))
    _arrow(d, (tx + 4, 112), (tx + 30, 112))
    # Baxter bottle: saline to half, plasma above it
    d.line((fx - 15, base - 38), (fx + 15, base - 38))
    d.line((fx - 15, base - 74), (fx + 15, base - 74))
    for x0 in range(int(fx - 13), int(fx + 12), 6):
        d.line((x0, base - 56), (x0 + 3, base - 56))
    d.group('mid')
    d.text(70, base + 14, 'SETTLED · ×8', size=7)
    d.text(sx, sy + 18, 'STOPCOCK', size=7)
    d.text(px, base + 14, 'POOL 2 L', size=7)
    d.text(220, 50, 'HOOD · UV', size=7)
    d.text(tx, base + 14, 'TRAP', size=7)
    d.text(tx + 34, 108, 'PUMP', size=7, anchor='start')
    d.text(fx, base + 14, '500+500', size=7)
    d.text(px, pl - 6, '1:10,000', size=7)
    return d


PLATES = {'robertson-depot': robertson_depot, 'citrate': citrate, 'blood-banks': blood_banks,
          'drew-plasma': drew_plasma}
