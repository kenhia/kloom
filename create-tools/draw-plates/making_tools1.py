"""Plates for How We Build's Machines that make machines, part tools1 (sprint 026):
Wilkinson's boring mill, Maudslay's screw-cutting lathe and Whitworth's three plates."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _gear(cx, cy, r, n, h=3.2, phase=0.0):
    """A spur gear's outline: n trapezoidal teeth of depth h about the pitch circle r."""
    pts = []
    for i in range(n):
        a0 = 360 * i / n + phase
        step = 360 / n
        for frac, rr in ((0.0, r - h / 2), (0.18, r + h / 2), (0.5, r + h / 2), (0.68, r - h / 2)):
            u = _dir(a0 + frac * step)
            pts.append((cx + u[0] * rr, cy + u[1] * rr))
    return pts


def _thread(x0, x1, y, r, p, depth):
    """The two edges of a V thread seen from the side: crests at radius r, roots at r - depth, pitch p."""
    top, bot = [], []
    n = int((x1 - x0) / (p / 2))
    for i in range(n + 1):
        x = x0 + i * p / 2
        rr = r if i % 2 == 0 else r - depth
        top.append((x, y - rr))
        # the far side of the thread is half a pitch along: a helix, not rings
        rb = r - depth if i % 2 == 0 else r
        bot.append((x, y + rb))
    return top, bot


def maudslay():
    d = D()
    wy, wr = 104, 15                       # the work's axis and radius
    ly, lr = 196, 7                        # the lead screw's axis and radius
    p = 12                                 # one pitch, the same on both: equal wheels
    xt0, xt1 = 196, 316                    # the threaded length of the work
    hx0, hx1 = 92, 120                     # the headstock
    tx0, tx1 = 322, 346                    # the tailstock
    gs, gl = (64, wy), (64, ly)            # spindle wheel and lead-screw wheel, 24 teeth each
    rg, ri = 22, 26
    dy = (ly - wy) / 2
    gi = (64 - math.sqrt((rg + ri) ** 2 - dy ** 2), wy + dy)   # the idler, meshing both
    d.group('thin')
    d.line((40, wy), (372, wy))                                 # the line of centres
    d.line((40, ly), (372, ly))                                 # the lead screw's axis
    # a crest of the lead screw projected up to a crest of the work: one pitch for one turn
    for k in range(0, 11, 2):
        x = xt0 + k * p / 2
        d.line((x, ly - lr - 4), (x, wy + wr + 4))
    # the pitch, dimensioned over the work
    d.line((xt0 + 2 * p, wy - wr - 12), (xt0 + 3 * p, wy - wr - 12))
    d.lines([[(xt0 + 2 * p, wy - wr - 16), (xt0 + 2 * p, wy - wr - 8)],
             [(xt0 + 3 * p, wy - wr - 16), (xt0 + 3 * p, wy - wr - 8)]])
    # one pitch of the lead screw, dimensioned under it
    d.line((84 + 4 * p, ly + 16), (84 + 5 * p, ly + 16))
    d.lines([[(84 + 4 * p, ly + 12), (84 + 4 * p, ly + 20)], [(84 + 5 * p, ly + 12), (84 + 5 * p, ly + 20)]])
    # the helix angle: a thread unrolled, one circumference along and one pitch up
    ux, uy, ub, uh = 248, 50, 110, 22
    d.line((ux, uy), (ux + ub, uy), (ux + ub, uy - uh), closed=True)
    d.line((ux - 6, uy), (ux, uy))
    d.group()
    # the bed: two bars, front and back, on cast feet
    d.line((30, 228), (380, 228))
    d.line((30, 238), (380, 238))
    d.line((44, 238), (36, 268), (76, 268), (68, 238))
    d.line((334, 238), (326, 268), (366, 268), (358, 238))
    # headstock and tailstock, with their centres
    d.line((hx0, 228), (hx0, wy - 26), (hx1, wy - 26), (hx1, 228))
    d.line((tx0, 228), (tx0, wy - 16), (tx1, wy - 16), (tx1, 228))
    d.line((hx1, wy - 6), (hx1 + 10, wy), (hx1, wy + 6))
    d.line((tx0, wy - 6), (tx0 - 8, wy), (tx0, wy + 6))
    # the work: plain, then threaded
    d.line((hx1 + 10, wy - wr), (xt0, wy - wr))
    d.line((hx1 + 10, wy + wr), (xt0, wy + wr))
    d.line((hx1 + 10, wy - wr), (hx1 + 10, wy + wr))
    top, bot = _thread(xt0, xt1, wy, wr, p, 4)
    d.line(*top)
    d.line(*bot)
    d.line((xt1, wy - wr), (xt1, wy + wr))
    d.line((xt1, wy), (tx0 - 8, wy))
    # the lead screw, its whole length threaded, in bearings at both ends
    top, bot = _thread(84, 330, ly, lr, p, 3)
    d.line(*top)
    d.line(*bot)
    d.line((64, ly), (84, ly))
    d.lines([[(80, ly - 12), (80, ly + 12)], [(334, ly - 12), (334, ly + 12)]])
    # the gear train: spindle wheel, idler, lead-screw wheel
    d.line(*_gear(*gs, rg, 24), closed=True)
    d.line(*_gear(*gl, rg, 24, phase=7.5), closed=True)
    d.line(*_gear(*gi, ri, 28, phase=3), closed=True)
    d.line((gs[0], wy), (hx0, wy))
    d.group('mid')
    for c, r in ((gs, rg), (gl, rg), (gi, ri)):
        d.circle(*c, 3)
        d.circle(*c, r - 7)
    # the slide rest: saddle on the bars, a half nut on the lead screw, the tool at the work
    sx = xt0 + 10 * p / 2                 # the tool's point sits at the end of the cut so far
    d.line((sx - 30, 228), (sx - 30, 212), (sx + 30, 212), (sx + 30, 228))
    d.lines([[(sx - 14, ly + lr + 2), (sx - 14, 212)], [(sx + 14, ly + lr + 2), (sx + 14, 212)]])
    d.line((sx - 14, ly + lr + 2), (sx - 14, ly - lr - 8), (sx + 14, ly - lr - 8), (sx + 14, ly + lr + 2))
    d.line((sx - 22, ly - 18), (sx - 22, wy + 40), (sx + 22, wy + 40), (sx + 22, ly - 18))
    d.line((sx - 6, wy + 40), (sx - 6, wy + 28), (sx, wy + wr - 2), (sx + 6, wy + 28), (sx + 6, wy + 40))
    d.line((sx + 22, wy + 52), (sx + 40, wy + 52))
    d.circle(sx + 44, wy + 52, 4)
    # the helix angle marked
    d.arc(ux, uy, 26, -math.degrees(math.atan2(uh, ub)), 0, n=10)
    d.group('mid')
    d.text(xt0 + 2.5 * p, wy - wr - 18, 'p', size=8)
    d.text(84 + 4.5 * p, ly + 26, 'p', size=8)
    d.text(ux + ub / 2, uy + 12, 'πd', size=8)
    d.text(ux + ub + 6, uy - uh / 2 + 3, 'p', size=8, anchor='start')
    d.text(ux + 30, uy - 3, 'θ', size=8, anchor='start')
    d.text(ux + ub / 2, 20, 'tan θ = p ÷ πd', size=8)
    d.text(gs[0], wy - rg - 10, '24 : 24', size=8)
    d.text(220, ly + 22, 'LEAD SCREW', size=8, anchor='end')
    d.text(250, 288, 'ONE TURN OF THE WORK, ONE PITCH OF THE TOOL', size=8)
    return d


PLATES = {'maudslay': maudslay}


def wilkinson_boring():
    d = D()
    ay = 104                                  # the bar's axis
    rb, rh = 8, 3                             # the bar's radius and its central hole
    c0, c1 = 118, 282                         # the cylinder's ends
    rbore, rwall = 38, 48                     # finished bore and outside of the casting
    hx = 228                                  # the cutter head: bored to its left, rough to its right
    b0, b1 = 74, 318                          # the two bearings
    d.group('thin')
    d.line((20, ay), (384, ay))
    d.lines([[(c0, ay - rbore), (c1 + 10, ay - rbore)], [(c0, ay + rbore), (c1 + 10, ay + rbore)]])
    d.line((hx, ay - rwall - 14), (hx, ay + rwall + 14))
    for x in (b0, b1):
        d.line((x, ay - 30), (x, ay + 60))
    # the inset's baselines
    L = 140
    for x0 in (30, 226):
        d.line((x0, 238), (x0 + L, 238))
    d.group()
    # the casting in section: two walls, the bore finished behind the head and rough ahead of it
    for sgn in (-1, 1):
        d.line((c0, ay + sgn * rwall), (c1, ay + sgn * rwall))
        rough = [(hx + 2, ay + sgn * rbore)]
        for i in range(1, 27):
            x = hx + 2 + i * (c1 - hx - 2) / 26
            r = rbore - 3.5 - 1.6 * math.sin(i * 1.9) - 1.1 * math.sin(i * 0.7 + sgn)
            rough.append((x, ay + sgn * r))
        d.line((c0, ay + sgn * rbore), (hx - 2, ay + sgn * rbore))
        d.line(*rough)
        d.line((c0, ay + sgn * rbore), (c0, ay + sgn * rwall))
        d.line((c1, ay + sgn * (rbore - 4)), (c1, ay + sgn * rwall))
    # the bar, right through, in its two bearings
    d.line((30, ay - rb), (350, ay - rb))
    d.line((30, ay + rb), (350, ay + rb))
    for x in (b0, b1):
        d.line((x - 10, ay - rb - 4), (x + 10, ay - rb - 4), (x + 10, ay + rb + 4), (x - 10, ay + rb + 4), closed=True)
        d.line((x - 8, ay + rb + 4), (x - 18, ay + 62), (x + 18, ay + 62), (x + 8, ay + rb + 4))
    # the cradles under the casting
    for x in (c0 + 26, c1 - 26):
        d.line((x - 16, ay + rwall), (x - 20, ay + 62), (x + 20, ay + 62), (x + 16, ay + rwall))
    d.line((10, ay + 62), (390, ay + 62))
    # the driving wheel on the bar's end
    d.line(*_gear(36, ay, 22, 22), closed=True)
    d.group('mid')
    d.lines([[(30, ay - rh), (350, ay - rh)], [(30, ay + rh), (350, ay + rh)]])     # the hole down the bar
    d.circle(36, ay, 13)
    # the cutter head: a sleeve on the bar carrying cutters to the bore
    d.line((hx - 7, ay - rbore + 6), (hx + 7, ay - rbore + 6), (hx + 7, ay + rbore - 6), (hx - 7, ay + rbore - 6), closed=True)
    for sgn in (-1, 1):
        y = ay + sgn * (rbore - 6)
        d.line((hx - 3, y), (hx + 1, ay + sgn * rbore), (hx + 5, y))
    # the feed: a rod inside the bar, out to a rack, a pinion and a weighted lever
    d.line((hx, ay), (366, ay))
    d.line((350, ay + 4), (384, ay + 4))
    d.lines([[(352 + 4 * k, ay + 4), (354 + 4 * k, ay + 8)] for k in range(8)])
    d.circle(368, ay + 15, 6)
    d.line((368, ay + 15), (330, ay + 44))
    d.circle(326, ay + 47, 5)
    # the inset: the same bar and force, overhung and held at both ends, sag exaggerated alike
    k = 30 / (L ** 3 / 3)                    # scale so the overhung bar's tip sags 30 px
    x0 = 30
    cant = [(x0 + x, 238 + k * x * x * (3 * L - x) / 6) for x in range(0, L + 1, 5)]
    d.line(*cant)
    d.line((x0, 222), (x0, 254))
    d.lines([[(x0 - 6, 222 + 6 * i), (x0, 228 + 6 * i)] for i in range(5)])
    d.line((x0 + L, 238 + 30 - 18), (x0 + L, 238 + 30 - 2))
    d.line((x0 + L - 3, 238 + 30 - 7), (x0 + L, 238 + 30 - 2), (x0 + L + 3, 238 + 30 - 7))
    x0 = 226
    ss = []
    for x in range(0, L + 1, 5):
        u = x if x <= L / 2 else L - x
        ss.append((x0 + x, 238 + k * u * (3 * L * L - 4 * u * u) / 48))
    d.line(*ss)
    for xs in (x0, x0 + L):
        d.line((xs, 238), (xs - 6, 248), (xs + 6, 248), closed=True)
    d.line((x0 + L / 2, 238 - 18), (x0 + L / 2, 238 - 2))
    d.line((x0 + L / 2 - 3, 238 - 7), (x0 + L / 2, 238 - 2), (x0 + L / 2 + 3, 238 - 7))
    d.group('mid')
    d.text(30 + L / 2, 288, 'OVERHUNG: FL³ ÷ 3EI', size=8)
    d.text(226 + L / 2, 288, 'BOTH ENDS: FL³ ÷ 48EI', size=8)
    d.text(30 + L + 8, 262, 'F', size=8, anchor='start')
    d.text(226 + L / 2 + 6, 224, 'F', size=8, anchor='start')
    d.text(hx, ay - rwall - 20, 'CUTTER HEAD', size=8)
    d.text((c0 + hx) / 2, ay - rwall - 8, 'BORED', size=8)
    d.text((hx + c1) / 2, ay - rwall - 8, 'AS CAST', size=8)
    d.text(36, ay - 32, 'DRIVE', size=8)
    d.text(368, ay + 40, 'FEED', size=8)
    return d


PLATES['wilkinson-boring'] = wilkinson_boring


def _face(cx, y, hw, sag, n=40):
    """A plate's working face in section, half-width hw: sag > 0 bows it upward (convex up)."""
    return [(cx + hw * (2 * i / n - 1), y - sag * (1 - (2 * i / n - 1) ** 2)) for i in range(n + 1)]


def _plate(d, cx, y, hw, sag, up=True, t=10):
    """A plate in section whose face lies on y (bowed by sag); its body lies below if up, above if not."""
    face = _face(cx, y, hw, sag)
    b = y + t if up else y - t
    d.line(*face, (cx + hw, b), (cx - hw, b), closed=True)
    # ribs on the back
    for k in (-0.6, 0, 0.6):
        x = cx + k * hw
        d.line((x - 3, b), (x - 3, b + (5 if up else -5)), (x + 3, b + (5 if up else -5)), (x + 3, b))


def whitworth():
    d = D()
    hw, s = 54, 5                    # half-width of a plate and the bow, much exaggerated
    rows = (66, 150, 236)
    cols = (100, 290)
    d.group('thin')
    for y in rows:
        d.line((20, y), (380, y))    # where a true face would lie
    for x in cols:
        d.line((x, 30), (x, 268))
    d.group()
    g = 1.5                          # a hair between plates that fit, to show there are two
    # 1st: Nos. 2 and 3 scraped to fit No. 1, which is convex; each comes out hollow to match
    for cx in cols:
        _plate(d, cx, rows[0] - s - g, hw, -s, up=False)     # No. 1, face down, bowed down: convex
        _plate(d, cx, rows[0] - s + g, hw, -s, up=True)      # No. 2 or 3, face up, hollow to fit
    # 2nd: Nos. 2 and 3 face to face: both hollow, so they touch at the edges and gape by 2s
    cx = cols[0]
    _plate(d, cx, rows[1] - s, hw, -s, up=True)
    _plate(d, cx, rows[1] - s, hw, s, up=False)
    # beside it, a plate from behind on its three feet
    px, py = cols[1], rows[1] + 6
    d.line((px - hw, py - 10), (px + hw, py - 10), (px + hw, py), (px - hw, py), closed=True)
    for x in (px - hw + 8, px, px + hw - 8):
        d.line((x - 4, py), (x, py + 10), (x + 4, py))
    # 3rd: after the rounds, every pair fits flat
    for cx in cols:
        _plate(d, cx, rows[2] - g, hw, 0, up=False)
        _plate(d, cx, rows[2] + g, hw, 0, up=True)
    d.group('mid')
    # the doubled gap dimensioned at the middle
    cx = cols[0]
    d.lines([[(cx + 6, rows[1] - 2 * s), (cx + hw + 16, rows[1] - 2 * s)],
             [(cx + 6, rows[1]), (cx + hw + 16, rows[1])]])
    d.line((cx + hw + 12, rows[1] - 2 * s - 6), (cx + hw + 12, rows[1] + 6))
    d.group('mid')
    d.text(cols[0], 22, '2 TO 1', size=8)
    d.text(cols[1], 22, '3 TO 1', size=8)
    d.text(cols[0] + hw + 18, rows[1] - s + 3, '2s', size=8, anchor='start')
    d.text(cols[0] - hw - 8, rows[1] - 3, '2 ON 3', size=8, anchor='end')
    d.text(cols[1], rows[1] + 30, 'THREE FEET', size=8)
    d.text(200, 286, 'EVERY PAIR FITS: ALL THREE FLAT', size=8)
    return d


PLATES['whitworth'] = whitworth
