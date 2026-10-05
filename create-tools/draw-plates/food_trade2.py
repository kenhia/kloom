"""Plates for Daily Bread's Spice, tea and trade frames written by part trade2 in sprint 051:
chocolate, coffeehouse and tea-and-opium. See plates_for.py."""
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


def chocolate():
    d = D()
    # Left: a cacao pod in elevation, about 20 cm long (the Cocoa bean article gives 17 to 20 cm), its
    # ten ridges drawn as five visible lines at fixed fractions of the half-width. Right: the pod cut
    # across, a ribbed rind round a white pulp, with the seeds in five rows radiating from the
    # central placenta (30 to 40 seeds a pod). Below: a metate, the sloping grinding slab on three
    # legs, with its mano and the little fire Gage says was kept under the stone. Proportions are
    # schematic; the pod's outline is computed, w(x) = W (1 - (x/L)^2)^0.65.
    cx, cy, L, W = 115, 112, 92, 40

    def half(x):
        return W * max(0.0, 1 - (x / L) ** 2) ** 0.65

    sx, sy, R = 305, 112, 58                                              # the cross-section

    d.group('thin')
    d.line((cx - L - 10, cy), (cx + L + 10, cy))                          # the pod's axis
    d.line((cx, cy - W - 12), (cx, cy + W + 12))
    for k in range(5):                                                     # the five rows' axes
        a = math.radians(-90 + 72 * k)
        d.line((sx, sy), (sx + (R + 10) * math.cos(a), sy + (R + 10) * math.sin(a)))
    d.circle(sx, sy, R + 10)

    d.group()
    xs = [-L + 2 * L * i / 60 for i in range(61)]
    top = [(cx + x, cy - half(x)) for x in xs]
    bot = [(cx + x, cy + half(x)) for x in reversed(xs)]
    d.line(*top, *bot, closed=True)
    ring = [(sx + (R + 2.5 * math.cos(10 * t)) * math.cos(t), sy + (R + 2.5 * math.cos(10 * t)) * math.sin(t))
            for t in [2 * math.pi * i / 200 for i in range(200)]]
    d.line(*ring, closed=True)                                             # the ribbed rind
    d.circle(sx, sy, R - 12)                                               # rind's inner face

    d.group('mid')
    for k in (-0.75, -0.38, 0.38, 0.75):                                  # the ridges in elevation
        d.line(*[(cx + x, cy + k * half(x)) for x in xs[3:-3]])
    d.line((cx - L, cy), (cx - L - 9, cy - 4))                            # the stalk
    for k in range(5):                                                     # seeds, two to a row in section
        a = math.radians(-90 + 72 * k)
        for r in (12, 25, 38):
            ex, ey = sx + r * math.cos(a), sy + r * math.sin(a)
            # an ellipse turned to point along its row
            pts = [(ex + 6.5 * math.cos(t) * math.cos(a) - 4.5 * math.sin(t) * math.sin(a),
                    ey + 6.5 * math.cos(t) * math.sin(a) + 4.5 * math.sin(t) * math.cos(a))
                   for t in [2 * math.pi * i / 36 for i in range(36)]]
            d.line(*pts, closed=True)
    d.circle(sx, sy, 5)                                                    # the placenta

    d.group()
    # the metate: a slab sloping toward the grinder, on three legs, a mano across it
    m0, m1, mt0, mt1 = (60, 238), (210, 222), (60, 246), (210, 230)
    d.line(m0, m1, mt1, mt0, closed=True)
    d.line((70, 245), (64, 268))
    d.line((200, 230), (206, 268))
    d.line((135, 238), (135, 268))
    d.ellipse(150, 238 - 16 * 90 / 150 - 6, 26, 6)                        # the mano, resting on the slab

    d.group('mid')
    for i, x in enumerate(range(112, 172, 12)):                            # the little fire under the stone
        h = 10 + 6 * math.sin(i * 1.7)
        d.line((x, 266), (x + 4, 266 - h), (x + 8, 266))
    d.line((100, 268), (180, 268))

    d.group('mid')
    d.text(cx, cy + W + 26, 'POD · ABOUT 20 CM', size=7)
    d.text(sx, sy + R + 24, "IN SECTION", size=7)
    d.text(sx + R + 2, sy - R - 4, 'RIND', size=7, anchor='start')
    d.text(sx + 26, sy - 30, 'PULP', size=7)
    d.text(sx, sy + R + 36, '30–40 SEEDS A POD', size=7)
    d.text(300, 240, 'METATE AND MANO', size=7)
    d.text(300, 252, 'A LITTLE FIRE BENEATH', size=7)
    return d


def coffeehouse():
    d = D()
    # Left: the coffee cherry cut across, as Laborie describes it in The Coffee Planter of Saint
    # Domingo (1798): "a red and shining skin", "a whitish clammy luscious pulp" enclosing two seeds
    # whose flat faces lie together, each with its fissure, each wrapped in the "parchment" and,
    # inside that, a thin "silver-coloured membrane". Right: the dry-in-parchment method he gives
    # as best, step by step, as a flow. Proportions are schematic.
    cx, cy, rx, ry = 112, 128, 78, 66

    def bean(sign):
        """One seed, a half-ellipse whose flat face lies on the center line."""
        bx, bry, brx = cx + sign * 4, 50, 34
        arc = [(bx + sign * brx * math.sin(t), cy - bry * math.cos(t))
               for t in [math.pi * i / 40 for i in range(41)]]
        return arc

    d.group('thin')
    d.line((cx - rx - 12, cy), (cx + rx + 12, cy))
    d.line((cx, cy - ry - 12), (cx, cy + ry + 12))
    d.ellipse(cx, cy, rx - 12, ry - 10)                                    # the pulp's inner face

    d.group()
    d.ellipse(cx, cy, rx, ry)                                              # skin
    for s in (-1, 1):
        d.line(*bean(s), closed=True)

    d.group('mid')
    for s in (-1, 1):                                                      # parchment, offset outward
        bx = cx + s * 4
        pts = [(bx + s * 39 * math.sin(t), cy - 55 * math.cos(t)) for t in [math.pi * i / 40 for i in range(41)]]
        d.line(*pts)
        d.line(pts[0], pts[-1])
        # the fissure: an S-curve in the flat face, seen in section as a fold
        f0 = cx + s * 4
        d.line((f0, cy - 20), (f0 + s * 10, cy - 8), (f0 + s * 4, cy), (f0 + s * 10, cy + 8), (f0, cy + 20))
    d.line((cx - 4, cy - 44), (cx - 4, cy + 44))                          # silver skin along the faces
    d.line((cx + 4, cy - 44), (cx + 4, cy + 44))

    d.group()
    steps = ['PICK RIPE CHERRY', 'GRATE OFF THE SKIN', 'SOAK AND WASH 24 H', 'DRAIN',
             'DRY ON PLATFORMS', 'MILL OFF PARCHMENT', 'WINNOW', 'PICK OVER BY HAND']
    bx, bw, bh, y0, gap = 250, 132, 18, 30, 30
    for i in range(len(steps)):
        _box(d, bx, y0 + i * gap, bw, bh)
    for i in range(len(steps) - 1):
        p, q = (bx + bw / 2, y0 + i * gap + bh), (bx + bw / 2, y0 + (i + 1) * gap)
        d.line(p, q)
        _arrow(d, p, q, size=4)

    d.group('mid')
    for i, s in enumerate(steps):
        d.text(bx + bw / 2, y0 + i * gap + 12, s, size=7)
    d.text(cx, cy - ry - 18, 'COFFEE CHERRY IN SECTION', size=7)
    d.text(cx + rx + 4, cy - 44, 'SKIN', size=7, anchor='start')
    d.text(cx - rx - 4, cy - 44, 'PULP', size=7, anchor='end')
    d.text(cx, cy + ry + 22, 'TWO SEEDS IN PARCHMENT', size=7)
    d.text(cx, cy + ry + 34, 'FLAT FACES TOGETHER', size=7)
    return d


def tea_and_opium():
    d = D()
    # The trade's triangle in the 1830s as a diagram, not a map: London, Calcutta and Canton at the
    # corners of an equilateral triangle on its circumscribed circle. Each flow is an arc bowed off
    # its chord by a fixed fraction of the chord's length, outward for the long-haul trades and
    # inward for the returns. Heavy arcs are the two that carried the trade, tea and opium; the
    # weights show roles, not quantities.
    ox, oy, rr = 200, 158, 112
    pos = {}
    for name, deg in (('london', -90), ('calcutta', 150), ('canton', 30)):
        a = math.radians(deg)
        pos[name] = (ox + rr * math.cos(a), oy + rr * math.sin(a))
    lon_, cal, can = pos['london'], pos['calcutta'], pos['canton']

    def bow(p, q, k, n=40):
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        dx, dy = q[0] - p[0], q[1] - p[1]
        c = (mx - k * dy, my + k * dx)                                     # control point off the chord
        return [((1 - t) ** 2 * p[0] + 2 * (1 - t) * t * c[0] + t * t * q[0],
                 (1 - t) ** 2 * p[1] + 2 * (1 - t) * t * c[1] + t * t * q[1])
                for t in [i / n for i in range(n + 1)]]

    def flow(p, q, k, cut=16, size=5):
        pts = [pt for pt in bow(p, q, k) if math.dist(pt, p) > cut and math.dist(pt, q) > cut]
        d.line(*pts)
        _arrow(d, pts[-2], pts[-1], size=size)
        return pts[len(pts) // 2]

    d.group('thin')
    d.circle(ox, oy, rr)
    d.line(lon_, cal, can, closed=True)
    for p in (lon_, cal, can):
        d.line((ox, oy), p)

    d.group()
    for p in (lon_, cal, can):
        d.circle(*p, 9)

    d.group()
    tea = flow(can, lon_, 0.2, size=6)
    opium = flow(cal, can, 0.2, size=6)

    d.group('mid')
    silver1 = flow(lon_, can, 0.08)
    silver2 = flow(can, cal, 0.08)
    cloth = flow(lon_, cal, 0.2)

    d.group('mid')
    d.text(lon_[0], lon_[1] - 16, 'LONDON', size=7)
    d.text(cal[0], cal[1] + 22, 'CALCUTTA', size=7)
    d.text(can[0], can[1] + 22, 'CANTON', size=7)
    d.text(tea[0] + 8, tea[1] - 2, 'TEA', size=7, anchor='start')
    d.text(opium[0], opium[1] + 16, 'OPIUM', size=7)
    d.text(silver1[0] - 6, silver1[1] + 10, 'SILVER', size=7, anchor='end')
    d.text(silver2[0], silver2[1] - 8, 'SILVER', size=7)
    d.text(cloth[0] - 8, cloth[1] - 2, 'CLOTH', size=7, anchor='end')
    d.text(200, 296, 'HEAVY ARCS CARRIED THE TRADE · NOT TO SCALE', size=7)
    return d


PLATES = {'chocolate': chocolate, 'coffeehouse': coffeehouse, 'tea-and-opium': tea_and_opium}
