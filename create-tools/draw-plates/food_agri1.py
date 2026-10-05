"""Plates for Daily Bread's part agri1 (sprint 051): seed-drill, four-course, enclosure. See plates_for.py."""
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


def seed_drill():
    d = D()
    # Left: Tull's wheat drill in side elevation, after his own plates (Horse-Hoing Husbandry, 1733, plates 2-5):
    # the hopper over the seed-box, the box riding on the axle of two wheels, the share (sheat) cutting the
    # channel with the funnel behind it, and the harrow trailing on its beams. Proportions are schematic.
    # Right: a section of the seed-box across the notched spindle, as in his Plate 3, Fig. 4-5: six equal notches,
    # the brass tongue lying across the box with its lip on the notches, its steel spring and the setting screw.
    ground = 238
    wx, wy, wr = 118, 196, 40                                            # near wheel, centre and radius
    d.group('thin')
    d.line((14, ground), (250, ground))                                   # the ground
    d.line((wx, wy - wr - 30), (wx, ground + 6))                          # the axle's vertical
    d.line((wx - wr - 8, wy), (wx + wr + 8, wy))                          # the axle's horizontal
    sx, sy, sr = 284, 128, 30                                             # spindle section
    d.line((sx - sr - 22, sy), (sx + sr + 22, sy))
    d.line((sx, sy - sr - 30), (sx, sy + sr + 26))

    d.group()
    d.circle(wx, wy, wr)                                                  # wheel rim and hub
    d.circle(wx, wy, 5)
    spokes = []
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        spokes.append([(wx + 5 * math.cos(a), wy + 5 * math.sin(a)), (wx + wr * math.cos(a), wy + wr * math.sin(a))])
    d.lines(spokes)
    box = (wx - 20, wy - 34, 40, 26)                                      # the seed-box, riding on the axle
    _box(d, *box)
    d.line((wx - 26, wy - 34), (wx - 34, wy - 66), (wx + 34, wy - 66), (wx + 26, wy - 34))   # the hopper
    d.line((wx - 20, wy - 14), (34, wy - 40), (16, wy - 46))              # a shaft forward, to the horse
    d.line((wx + 20, wy - 20), (226, wy - 20))                            # the plank and beam behind
    share_x = 176                                                         # the sheat and its share
    d.line((share_x, wy - 20), (share_x, ground + 12), (share_x - 14, ground + 6), (share_x - 4, ground - 4))
    d.line((wx + 6, wy - 8), (share_x + 8, ground - 6))                   # the funnel down behind the share
    d.line((wx + 13, wy - 8), (share_x + 14, ground - 8))
    d.line((226, wy - 20), (236, ground - 10))                            # the harrow on its beam
    tines = []
    for k in range(4):
        x = 206 + 12 * k
        tines.append([(x, ground - 12), (x + 4, ground + 3)])
    d.line((200, ground - 12), (250, ground - 12))
    d.lines(tines)

    d.group()
    # the spindle in section: a circle cut by six equal notches, each a radial side and a flat bottom
    n, depth = 6, 9
    pts = []
    for k in range(n):
        a0 = math.radians(k * 360 / n + 15)
        a1 = a0 + math.radians(360 / n * 0.55)                            # the notch's width
        a2 = a0 + math.radians(360 / n)
        r_in = sr - depth
        pts.append((sx + sr * math.cos(a0), sy + sr * math.sin(a0)))
        pts.append((sx + r_in * math.cos(a0), sy + r_in * math.sin(a0)))   # the side, along a radius
        pts.append((sx + r_in * math.cos(a1), sy + r_in * math.sin(a1)))   # the bottom
        pts.append((sx + sr * math.cos(a1), sy + sr * math.sin(a1)))
        for j in range(1, 7):                                             # the interval, an arc of the circle
            a = a1 + (a2 - a1) * j / 6
            pts.append((sx + sr * math.cos(a), sy + sr * math.sin(a)))
    d.line(*pts, closed=True)
    d.circle(sx, sy, 3)
    # the box's walls, the bevelled mortise the seed slides down to the spindle
    d.line((sx - 50, sy - 78), (sx - 33, sy - 12))
    # the tongue: a brass plate on a pin near its upper end, lying across the box with its lip on the notches
    tp = (sx + 50, sy - 66)
    ang = math.atan2(sy - 20 - tp[1], sx + 18 - tp[0])
    tq = (sx + sr * math.cos(math.radians(-48)) + 2, sy + sr * math.sin(math.radians(-48)) - 2)
    ang = math.atan2(tq[1] - tp[1], tq[0] - tp[0])
    nx, ny = math.cos(ang + math.pi / 2), math.sin(ang + math.pi / 2)
    d.line((tp[0] + 3 * nx, tp[1] + 3 * ny), (tq[0] + 3 * nx, tq[1] + 3 * ny),
           (tq[0] - 3 * nx, tq[1] - 3 * ny), (tp[0] - 3 * nx, tp[1] - 3 * ny), closed=True)
    d.circle(tp[0], tp[1], 2.5)                                           # its pin

    d.group('mid')
    # the steel spring, bowed along the tongue's back, and the setting screw that bears on its middle
    sp = []
    for i in range(13):
        u = i / 12
        bow = 5 * math.sin(math.pi * u)
        x = tp[0] + (tq[0] - tp[0]) * u - (5 + bow) * nx
        y = tp[1] + (tq[1] - tp[1]) * u - (5 + bow) * ny
        sp.append((x, y))
    d.line(*sp)
    mid = sp[6]
    d.line((mid[0] - 16 * nx, mid[1] - 16 * ny), (mid[0] - 11 * nx, mid[1] - 11 * ny))
    _box(d, mid[0] - 22 * nx - 3, mid[1] - 22 * ny - 3, 6, 6)
    # seed lying on the tongue, seed carried in the notches past its lip, and the passage out below
    for k in range(4):
        u = 0.25 + 0.18 * k
        d.circle(tp[0] + (tq[0] - tp[0]) * u + 6 * nx, tp[1] + (tq[1] - tp[1]) * u + 6 * ny, 2)
    for a in (8, 68):
        r = math.radians(a + 22)
        d.circle(sx + (sr - 4.5) * math.cos(r), sy + (sr - 4.5) * math.sin(r), 2)
    rot = [(sx + (sr + 12) * math.cos(math.radians(a)), sy + (sr + 12) * math.sin(math.radians(a)))
           for a in range(-30, 56, 8)]
    d.line(*rot)                                                          # the spindle turns with the wheels
    _arrow(d, rot[-2], rot[-1], size=4)
    d.line((sx + 14, sy + sr + 4), (sx + 14, sy + sr + 22))
    _arrow(d, (sx + 14, sy + sr + 4), (sx + 14, sy + sr + 22), size=4)
    # seed falling down the funnel into the channel
    for k in range(3):
        d.circle(share_x + 6 - 1.5 * k, ground - 2 - 9 * k, 1.3)

    d.group('mid')
    d.text(wx, wy - 72, 'HOPPER', size=7)
    d.text(wx + 40, wy - 50, 'SEED-BOX', size=7, anchor='start')
    d.text(share_x - 6, ground + 24, 'SHARE', size=7)
    d.text(232, ground + 24, 'HARROW', size=7)
    d.text(40, wy - 56, 'TO THE HORSE', size=7)
    d.text(sx + 14, sy + sr + 34, 'SEED TO THE FUNNEL', size=7)
    d.text(sx + 58, sy - 72, 'TONGUE', size=7, anchor='start')
    d.text(sx + 64, sy - 6, 'SPRING', size=7, anchor='start')
    d.text(sx + 64, sy + 6, 'AND SCREW', size=7, anchor='start')
    d.text(sx - sr - 8, sy + 46, 'SIX NOTCHES', size=7, anchor='end')
    d.text(300, 26, 'SEED-BOX IN SECTION', size=7)
    d.text(200, 286, "TULL'S DRILL · ELEVATION AND SECTION (SCHEMATIC)", size=7)
    return d


def _turnips(d, x, y, w, h):
    for r in range(3):
        for c in range(4):
            d.circle(x + w * (c + 0.5) / 4, y + h * (r + 0.5) / 3, 2.6)


def _barley(d, x, y, w, h):
    segs = []
    for r in range(3):
        for c in range(7):
            cx, cy = x + w * (c + 0.5) / 7, y + h * (r + 0.5) / 3
            segs.append([(cx, cy + 4), (cx, cy - 3), (cx + 2.5, cy - 6)])
    d.lines(segs)


def _clover(d, x, y, w, h):
    for r in range(2):
        for c in range(4):
            cx, cy = x + w * (c + 0.5) / 4, y + h * (r + 0.5) / 2
            for k in range(3):
                a = math.radians(-90 + 120 * k)
                d.circle(cx + 2.4 * math.cos(a), cy + 2.4 * math.sin(a), 1.9)


def _wheat(d, x, y, w, h):
    segs = []
    for r in range(2):
        for c in range(7):
            cx, cy = x + w * (c + 0.5) / 7, y + h * (r + 0.5) / 2
            segs.append([(cx, cy + 6), (cx, cy - 6)])
            segs.append([(cx - 1.8, cy - 4), (cx, cy - 2), (cx + 1.8, cy - 4)])
    d.lines(segs)


def four_course():
    d = D()
    # Four strips of one farm (rows) through four years (columns). Each year every strip moves one step through
    # the course Arthur Young recorded in Norfolk in 1771: turnips, barley, clover, wheat. So in every year the
    # farm grows all four crops, a quarter of its land in each, and no land lies in bare fallow. The textures are
    # signs, not counts: turnips as roots in hoed rows, barley as bent ears, clover as trefoils, wheat as upright ears.
    crops = [_turnips, _barley, _clover, _wheat]
    names = ['TURNIPS', 'BARLEY', 'CLOVER', 'WHEAT']
    x0, y0, cw, ch, gx, gy = 70, 46, 66, 36, 8, 10
    d.group('thin')
    for c in range(4):
        x = x0 + c * (cw + gx) + cw / 2
        d.line((x, y0 - 10), (x, y0 + 4 * (ch + gy) - gy + 4))
    for r in range(4):
        y = y0 + r * (ch + gy) + ch / 2
        d.line((x0 - 10, y), (x0 + 4 * (cw + gx) - gx + 6, y))

    d.group()
    for r in range(4):
        for c in range(4):
            _box(d, x0 + c * (cw + gx), y0 + r * (ch + gy), cw, ch)

    d.group('mid')
    for r in range(4):
        for c in range(4):
            k = (r + c) % 4
            crops[k](d, x0 + c * (cw + gx) + 4, y0 + r * (ch + gy) + 3, cw - 8, ch - 6)

    d.group('mid')
    # the course followed down one strip: an arrow from each year's cell to the next
    r = 0
    for c in range(3):
        p = (x0 + c * (cw + gx) + cw - 4, y0 + r * (ch + gy) + ch + 3)
        q = (x0 + (c + 1) * (cw + gx) + 4, y0 + r * (ch + gy) + ch + 3)
        d.line(p, q)
        _arrow(d, p, q, size=3.5)
    # the legend: one sign of each crop, and what its year did
    ly = 248
    roles = ['FEEDS STOCK', 'GRAIN', 'FIXES N', 'GRAIN']
    signs = [lambda x, y: d.circle(x, y, 2.6),
             lambda x, y: d.line((x, y + 4), (x, y - 3), (x + 2.5, y - 6)),
             lambda x, y: [d.circle(x + 2.4 * math.cos(math.radians(-90 + 120 * k)),
                                    y + 2.4 * math.sin(math.radians(-90 + 120 * k)), 1.9) for k in range(3)],
             lambda x, y: (d.line((x, y + 6), (x, y - 6)), d.line((x - 1.8, y - 4), (x, y - 2), (x + 1.8, y - 4)))]
    for k in range(4):
        signs[k](40 + 90 * k, ly + 1)
    d.group('mid')
    for c in range(4):
        d.text(x0 + c * (cw + gx) + cw / 2, y0 - 14, f'YEAR {c + 1}', size=7)
    for r in range(4):
        d.text(x0 - 12, y0 + r * (ch + gy) + ch / 2 + 3, f'STRIP {"ABCD"[r]}', size=7, anchor='end')
    for k in range(4):
        lx = 40 + 90 * k
        d.text(lx + 10, ly - 1, names[k], size=7, anchor='start')
        d.text(lx + 10, ly + 10, roles[k], size=7, anchor='start')
    d.text(200, 286, 'THE NORFOLK FOUR-COURSE ROTATION · NO BARE FALLOW', size=7)
    return d


def _clip(p, q, poly):
    """Clip segment p-q to a convex polygon (counter-clockwise vertices), Cyrus-Beck. None if outside."""
    t0, t1 = 0.0, 1.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]
        nx, ny = ey, -ex                                                  # outward normal for a CCW polygon (y down)
        num = nx * (p[0] - a[0]) + ny * (p[1] - a[1])
        den = nx * dx + ny * dy
        if abs(den) < 1e-12:
            if num > 0:
                return None
            continue
        t = -num / den
        if den > 0:
            t1 = min(t1, t)
        else:
            t0 = max(t0, t)
        if t0 > t1:
            return None
    return (p[0] + t0 * dx, p[1] + t0 * dy), (p[0] + t1 * dx, p[1] + t1 * dy)


def _outside(seg, c, r):
    """The parts of segment seg lying outside the circle of radius r about c."""
    (x0, y0), (x1, y1) = seg
    dx, dy = x1 - x0, y1 - y0
    fx, fy = x0 - c[0], y0 - c[1]
    a, b, cc = dx * dx + dy * dy, 2 * (fx * dx + fy * dy), fx * fx + fy * fy - r * r
    disc = b * b - 4 * a * cc
    if disc <= 0:
        return [seg]
    t1, t2 = (-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a)
    out = []
    if t1 > 0:
        out.append(((x0, y0), (x0 + dx * min(t1, 1), y0 + dy * min(t1, 1))))
    if t2 < 1:
        out.append(((x0 + dx * max(t2, 0), y0 + dy * max(t2, 0)), (x1, y1)))
    return [o for o in out if math.hypot(o[1][0] - o[0][0], o[1][1] - o[0][1]) > 0.5]


def _orient(poly):
    """Make a polygon's vertices run so that _clip's normals point outward."""
    area = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
               for i in range(len(poly)))
    return poly if area > 0 else poly[::-1]


def _sector(cx, cy, r, a0, a1, n=24):
    pts = [(cx, cy)] + [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                         cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return _orient(pts)


def _hatch(d, poly, angle, step, cx, cy, reach, hole=0):
    """Parallel lines at `angle` degrees, `step` apart, clipped to a convex polygon."""
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    segs = []
    k = -reach
    while k <= reach:
        p = (cx + vx * k - ux * reach, cy + vy * k - uy * reach)
        q = (cx + vx * k + ux * reach, cy + vy * k + uy * reach)
        s = _clip(p, q, poly)
        if s:
            segs.extend(list(o) for o in (_outside(s, (cx, cy), hole) if hole else [s]))
        k += step
    if segs:
        d.lines(segs)


def enclosure():
    d = D()
    # One imagined parish, drawn twice inside the same boundary. Before: the village at the centre, three great
    # open fields cut into furlongs of long narrow strips, each furlong's strips running its own way, and the
    # common waste beyond. After an enclosure award: compact closes ruled straight, hedged, with new straight
    # roads. The parish is invented; the layout follows the pattern the reading describes.
    R = 82
    L, Rt, cy = (102, 140), (298, 140), 140
    ring = lambda c: _orient([(c[0] + R * math.cos(2 * math.pi * i / 64), c[1] + R * math.sin(2 * math.pi * i / 64))
                              for i in range(64)])
    d.group('thin')
    for c in (L, Rt):
        d.line((c[0] - R - 6, cy), (c[0] + R + 6, cy))
        d.line((c[0], cy - R - 6), (c[0], cy + R + 6))
    d.line((L[0] + R + 8, cy), (Rt[0] - R - 8, cy))
    _arrow(d, (L[0] + R + 8, cy), (Rt[0] - R - 8, cy), size=4)

    d.group()
    d.circle(L[0], L[1], R)                                               # the parish boundaries
    d.circle(Rt[0], Rt[1], R)
    for a in (210, 330, 90, 150):                                         # the three fields' bounds, and the common
        d.line((L[0] + 12 * math.cos(math.radians(a)), cy + 12 * math.sin(math.radians(a))),
               (L[0] + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))))
    d.circle(L[0], L[1], 12)                                              # the village

    d.group('mid')
    # Before: each field split into two furlongs, each with strips running a different way
    fields = [(210, 270, 0), (270, 330, 60), (330, 30, 110), (30, 90, 160), (90, 150, 20)]
    for a0, a1, ang in fields:
        if a1 < a0:
            a1 += 360
        poly = _sector(L[0], cy, R - 1, a0 + 1, a1 - 1)
        _hatch(d, poly, ang, 4.2, L[0], cy, R, hole=15)
    # the common waste, from 150 to 210 degrees: scattered tufts of furze, not strips
    rng = random.Random(3)
    for i in range(22):
        a = math.radians(rng.uniform(156, 204))
        rr = rng.uniform(24, R - 8)
        x, y = L[0] + rr * math.cos(a), cy + rr * math.sin(a)
        if abs(x - (L[0] - 50)) < 20 and abs(y - (cy + 1)) < 8:            # keep the label clear
            continue
        d.line((x - 2.5, y + 1.5), (x, y - 2), (x + 2.5, y + 1.5))

    d.group()
    # After: new straight roads out from the village, and a grid of closes, clipped to the boundary
    rp = ring(Rt)
    segs = []
    for k, x in enumerate([-50, -18, 22, 52]):
        sg = _clip((Rt[0] + x + 6 * (k % 2), cy - R - 10), (Rt[0] + x - 6 * (k % 2), cy + R + 10), rp)
        if sg:
            segs.extend(_outside(sg, Rt, 18))
    for k, y in enumerate([-46, -12, 26, 58]):
        sg = _clip((Rt[0] - R - 10, cy + y - 5 * (k % 2)), (Rt[0] + R + 10, cy + y + 5 * (k % 2)), rp)
        if sg:
            segs.extend(_outside(sg, Rt, 18))
    d.lines([list(sg) for sg in segs])
    for a in (200, 15, 105):                                              # the roads, double lines
        ar = math.radians(a)
        p0 = (Rt[0] + 12 * math.cos(ar), cy + 12 * math.sin(ar))
        p1 = (Rt[0] + R * math.cos(ar), cy + R * math.sin(ar))
        nx, ny = -3 * math.sin(ar), 3 * math.cos(ar)
        d.line((p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny))
        d.line((p0[0] - nx, p0[1] - ny), (p1[0] - nx, p1[1] - ny))
    d.circle(Rt[0], Rt[1], 12)

    d.group('mid')
    # hedges: small bushes along the new boundaries
    for (p, q) in segs:
        length = math.hypot(q[0] - p[0], q[1] - p[1])
        nb = int(length // 14)
        for i in range(1, nb):
            u = i / nb
            d.circle(p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u, 1.6)

    d.group('mid')
    d.text(L[0], 40, 'BEFORE', size=7)
    d.text(Rt[0], 40, 'AFTER THE AWARD', size=7)
    d.text(L[0] - 50, cy + 4, 'COMMON', size=7)
    d.text(L[0], cy + R + 16, 'OPEN FIELDS IN STRIPS', size=7)
    d.text(Rt[0], cy + R + 16, 'HEDGED CLOSES, NEW ROADS', size=7)
    d.text(200, cy - 8, 'ACT', size=7)
    d.text(200, 286, 'ONE PARISH ENCLOSED (SCHEMATIC)', size=7)
    return d


PLATES = {'seed-drill': seed_drill, 'four-course': four_course, 'enclosure': enclosure}
