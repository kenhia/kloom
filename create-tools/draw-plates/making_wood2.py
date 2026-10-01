"""Plates for How We Build's Wood segment, part two (sprint 026): Hōryū-ji, Westminster Hall, the wind sawmill."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def horyuji():
    """A hinoki log split, not sawn: the end with its rings and the wedges' line, and the face with
    spiral grain at 1 in 10, crossed by a saw line and followed by a split; below, a spear plane's scallops."""
    d = D()
    cx, cy, r = 98, 112, 72                    # the log's end
    fx0, fx1, fy0, fy1 = 256, 372, 34, 262     # the log's face in elevation: 116 px across, 228 px long
    slope = 1 / 10                             # spiral grain: one across for ten along
    d.group('thin')
    # the end: the split line through the pith, and the quarter line it will take next
    d.line((cx, cy - r - 12), (cx, cy + r + 12))
    d.line((cx - r - 12, cy), (cx + r + 12, cy))
    # the face: centre line and the log's length
    d.line(((fx0 + fx1) / 2, fy0 - 10), ((fx0 + fx1) / 2, fy1 + 10))
    # the slope of grain as a triangle: 10 along, 1 across, on the right of the face
    tx, ty, tl = fx0 - 36, fy0 + 40, 150
    d.line((tx, ty), (tx, ty + tl), (tx + tl * slope, ty + tl))
    # the spear plane's stroke direction, and the datum the scallops are cut to
    d.line((22, 268), (186, 268))
    d.group()
    # the log end and its face
    d.circle(cx, cy, r)
    d.line((fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1), closed=True)
    d.group('mid')
    # growth rings: wider near the pith, closer towards the bark, a little off centre
    radii, rr, step = [], 6.0, 9.0
    while rr < r - 3:
        radii.append(rr)
        rr += step
        step *= 0.9
    for k, rr in enumerate(radii):
        d.circle(cx + 1.5 * (rr / r), cy - 1.0 * (rr / r), rr)
    # the grain on the face: parallel lines running one across in ten along
    span = fy1 - fy0
    segs = []
    for k in range(-4, 16):
        x0 = fx0 + k * 10
        x1 = x0 + span * slope
        # clip the line to the face
        a = (x0, fy0)
        b = (x1, fy1)
        if x1 < fx0 or x0 > fx1:
            continue
        if x0 < fx0:
            a = (fx0, fy0 + (fx0 - x0) / slope)
        if x1 > fx1:
            b = (fx1, fy0 + (fx1 - x0) / slope)
        segs.append([a, b])
    d.lines(segs)
    # the spear plane's work: a row of shallow concave scallops, each a circular arc, cut across the datum
    sc = []
    x = 26
    while x < 182:
        w = 18 + 4 * math.sin(x * 0.7)
        R = w * w / 8 / 2.6 + 2.6 / 2          # an arc w wide and 2.6 deep
        cxs, cys = x + w / 2, 260 - (R - 2.6)
        a0 = math.degrees(math.asin(w / 2 / R))
        sc.append([(cxs + R * math.sin(math.radians(t)), cys + R * math.cos(math.radians(t)))
                   for t in [-a0 + 2 * a0 * i / 10 for i in range(11)]])
        x += w
    d.lines(sc)
    d.group()
    # the wedges driven along the split line on the end, and the split opening
    for wy in (cy - 44, cy + 4, cy + 50):
        d.line((cx - 7, wy - 12), (cx + 7, wy - 12), (cx, wy + 8), closed=True)
    d.line((cx - 1.5, cy - r), (cx - 0.5, cy + r))
    # on the face: the saw's straight line, which crosses the grain, and the split, which follows it
    sx = (fx0 + fx1) / 2 - 2
    d.line((sx, fy0), (sx, fy1))
    spx = fx0 + 50
    d.line((spx, fy0), (spx + span * slope, fy1))
    d.group('mid')
    d.text(cx, cy + r + 26, 'THE END: WEDGES ON THE PITH', size=8)
    d.text(sx + 6, fy1 + 22, 'SAWN', size=8, anchor='start')
    d.text(spx - 4, fy0 - 8, 'SPLIT', size=8, anchor='end')
    d.text(tx + 8, ty + tl + 14, '1 IN 10', size=8)
    d.text(104, 288, 'YARIGANNA SCALLOPS', size=8)
    return d


PLATES = {'horyuji': horyuji}


def westminster_hall():
    """One truss of the roof in section, to scale from the 1911 Britannica's figures: a span of 20.8 m,
    7.77 m between the hammer beams' ends, hammer beams 12.19 m up, the collar 19.35 m up."""
    d = D()
    s = 9.2                                    # px per metre
    cx, floor = 200, 288
    half = 20.8 / 2
    hb_end = 7.77 / 2
    h_hb, h_col = 12.19, 19.35
    h_wall, wall_t = 13.6, 2.4                 # the wall head and the wall's thickness (drawn, not sourced)
    h_corbel = 6.6                             # the corbel the wall post stands on, about halfway down
    h_ridge = 27.4                             # about 90 ft to the ridge, as the 1914 scaffold measured

    def P(x, h):
        return cx + x * s, floor - h * s

    # the principal rafter: from the outer wall head to the ridge
    def rafter_h(x):                           # height of the rafter's underside at |x|
        x0 = half + wall_t
        return h_wall + (h_ridge - h_wall) * (x0 - abs(x)) / x0

    # where the hammer post meets the rafter
    h_hp = rafter_h(hb_end)
    # the arch rib: a pointed arch springing vertically from the wall post's foot, meeting at the collar
    # the arch rib: a circle through its springing at the corbel, a point halfway along the hammer beam,
    # and the collar's middle, where the two ribs meet in a point
    def circ(p1, p2, p3):
        (ax, ay), (bx, by), (qx, qy) = p1, p2, p3
        dd = 2 * (ax * (by - qy) + bx * (qy - ay) + qx * (ay - by))
        ux = ((ax * ax + ay * ay) * (by - qy) + (bx * bx + by * by) * (qy - ay) + (qx * qx + qy * qy) * (ay - by)) / dd
        uy = ((ax * ax + ay * ay) * (qx - bx) + (bx * bx + by * by) * (ax - qx) + (qx * qx + qy * qy) * (bx - ax)) / dd
        return ux, uy, math.hypot(ax - ux, ay - uy)
    spring = (half - 0.45, h_corbel)
    rcx, rch, R = circ(spring, ((half + hb_end) / 2 + 0.36, h_hb), (0, h_col))
    d.group('thin')
    d.line(P(-half - 4, 0), P(half + 4, 0))                         # the floor
    d.line(P(0, -0.5), P(0, h_ridge + 1.2))                         # centre line
    # dimension lines: the span, the opening between hammer-beam ends, and two heights
    d.line(P(-half, 2.2), P(half, 2.2))
    d.lines([[P(-half, 1.6), P(-half, 2.8)], [P(half, 1.6), P(half, 2.8)]])
    d.line(P(-hb_end, h_hb - 1.4), P(hb_end, h_hb - 1.4))
    d.lines([[P(-hb_end, h_hb - 1.0), P(-hb_end, h_hb - 1.8)], [P(hb_end, h_hb - 1.0), P(hb_end, h_hb - 1.8)]])
    d.line(P(half + wall_t + 1.6, 0), P(half + wall_t + 1.6, h_col))
    d.lines([[P(half + wall_t + 1.2, h_hb), P(half + wall_t + 2.0, h_hb)],
             [P(half + wall_t + 1.2, h_col), P(half + wall_t + 2.0, h_col)],
             [P(half + wall_t + 1.2, 0), P(half + wall_t + 2.0, 0)]])
    # the arch rib's centres, on the corbel line
    d.line(P(-half, h_corbel), P(half, h_corbel))
    d.group()
    for sg in (-1, 1):
        # the walls in section
        d.line(P(sg * half, 0), P(sg * half, h_wall), P(sg * (half + wall_t), h_wall), P(sg * (half + wall_t), 0))
        # the principal rafter, and the hammer beam projecting from the wall
        d.line(P(sg * (half + wall_t), h_wall), P(0, h_ridge))
        d.line(P(sg * (half + wall_t * 0.6), h_hb), P(sg * hb_end, h_hb))
        d.line(P(sg * (half + wall_t * 0.6), h_hb + 0.5), P(sg * hb_end, h_hb + 0.5))
        # the wall post, down the wall face to the corbel
        d.line(P(sg * (half - 0.45), h_hb), P(sg * (half - 0.45), h_corbel))
        # the hammer post, from the hammer beam's end up to the rafter
        d.line(P(sg * hb_end, h_hb + 0.5), P(sg * hb_end, h_hp))
    # the collar
    xc = (h_ridge - h_col) / (h_ridge - h_wall) * (half + wall_t)
    d.line(P(-xc, h_col), P(xc, h_col))
    d.group('mid')
    for sg in (-1, 1):
        # the arch rib: centre on the corbel line, R from the wall face, through the collar's middle
        a0 = math.atan2(spring[1] - rch, spring[0] - rcx)
        a1 = math.atan2(h_col - rch, 0 - rcx)
        pts = []
        for i in range(41):
            a = a0 + (a1 - a0) * i / 40
            pts.append(P(sg * (rcx + R * math.cos(a)), rch + R * math.sin(a)))
        d.line(*pts)
        # the hammer brace: a quarter curve from the wall post to the hammer beam's underside
        bx0, bh0 = sg * (half - 0.45), h_hb - 3.4
        rb = 3.4
        d.line(*[P(bx0 - sg * (rb - rb * math.cos(math.radians(t))), bh0 + rb * math.sin(math.radians(t)))
                 for t in range(0, 91, 6)])
        # the corbel
        d.line(P(sg * half, h_corbel), P(sg * (half - 0.9), h_corbel - 0.2), P(sg * half, h_corbel - 1.1))
        # struts from the hammer post to the collar, and a purlin's section on the rafter
        d.line(P(sg * hb_end, h_hp - 0.6), P(sg * xc * 0.55, h_col))
    # assembly marks at one joint, in the carpenters' Roman numerals
    d.group('mid')
    d.text(P(-half + 2.7, h_hb + 1.1)[0], P(-half + 2.7, h_hb + 1.1)[1], 'IIII', size=7)
    d.text(P(half - 2.7, h_hb + 1.1)[0], P(half - 2.7, h_hb + 1.1)[1], 'IIII', size=7)
    d.text(cx, P(0, 2.2)[1] - 4, '20.8 M', size=8)
    d.text(cx, P(0, h_hb - 1.4)[1] - 4, '7.77 M', size=8)
    x_lab = P(half + wall_t + 2.4, 0)[0]
    d.text(x_lab, P(0, h_hb)[1] + 3, '12.19', size=8, anchor='start')
    d.text(x_lab, P(0, h_col)[1] + 3, '19.35', size=8, anchor='start')
    d.text(cx, 14, 'ONE TRUSS OF THIRTEEN', size=8)
    return d


PLATES['westminster-hall'] = westminster_hall


def wind_sawmill():
    """The crankshaft's three throws at 120°, one crank and connecting rod driving a saw frame, the gang of
    blades set apart by spacers in a log, and the three frames' strokes plotted through one turn."""
    d = D()
    # crank and connecting rod, in elevation: shaft centre, throw r, rod length L (in px; drawn, not sourced)
    sx, sy, r, L = 92, 62, 20, 92
    th = 35                                    # the crank angle shown, from top dead centre
    px_, py_ = sx + r * math.sin(math.radians(th)), sy - r * math.cos(math.radians(th))
    # the rod's lower end slides on the vertical through the shaft centre
    fy = py_ + math.sqrt(L * L - (px_ - sx) ** 2)
    fw, fh = 64, 88                            # the saw frame
    # the strokes, plotted: x from 0 to 360 degrees
    gx0, gx1, gy = 200, 380, 262
    amp = 18
    d.group('thin')
    d.circle(sx, sy, r)                        # the crank pin's path
    d.line((sx, sy - r - 12), (sx, fy + fh + 14))  # the line of the stroke
    d.lines([[(sx - 40, fy), (sx - 34, fy)], [(sx - 40, fy + 2 * r), (sx - 34, fy + 2 * r)]])
    d.line((sx - 37, fy), (sx - 37, fy + 2 * r))
    # the plot's axes and the three phase marks
    d.line((gx0, gy), (gx1, gy))
    d.line((gx0, gy - amp - 8), (gx0, gy + amp + 8))
    for k in range(1, 4):
        x = gx0 + (gx1 - gx0) * k / 3
        d.line((x, gy - amp - 4), (x, gy + amp + 4))
    # the end view of the shaft: three throws
    ex, ey, er = 300, 64, 28
    d.circle(ex, ey, er)
    d.group()
    # the crank: shaft, web and pin; the connecting rod; the saw frame and its guides
    d.circle(sx, sy, 5)
    d.line((sx, sy), (px_, py_))
    d.circle(px_, py_, 3)
    d.line((px_, py_), (sx, fy))
    d.line((sx - fw / 2, fy), (sx + fw / 2, fy), (sx + fw / 2, fy + fh), (sx - fw / 2, fy + fh), closed=True)
    # the end view: three cranks at 120 degrees
    for k in range(3):
        a = -90 + th + 120 * k
        u = _dir(a)
        d.line((ex, ey), (ex + er * u[0], ey + er * u[1]))
        d.circle(ex + er * u[0], ey + er * u[1], 3.5)
    # the log in section, and its planks: a gang of five blades set apart by spacers
    lx, ly, lr = 300, 158, 38
    d.circle(lx, ly, lr)
    d.group('mid')
    # blades in the frame, with their spacers between them at the head
    n, gap = 5, 10
    xs = [sx + (k - (n - 1) / 2) * gap for k in range(n)]
    d.lines([[(x, fy + 6), (x, fy + fh - 6)] for x in xs])
    d.lines([[(xs[k] + 1.5, fy + 8), (xs[k + 1] - 1.5, fy + 8), (xs[k + 1] - 1.5, fy + 14), (xs[k] + 1.5, fy + 14), (xs[k] + 1.5, fy + 8)]
             for k in range(n - 1)])
    # teeth on the blades, pointing down, the cutting stroke
    teeth = []
    for x in xs:
        for j in range(8):
            y = fy + 20 + j * 8
            teeth.append([(x, y), (x + 2.5, y + 3), (x, y + 6)])
    d.lines(teeth)
    # the kerfs across the log, at the same spacing scaled up
    kg = 15
    kerfs = []
    for k in range(n):
        x = lx + (k - (n - 1) / 2) * kg
        hh = math.sqrt(max(lr * lr - (x - lx) ** 2, 0))
        kerfs.append([(x, ly - hh), (x, ly + hh)])
    d.lines(kerfs)
    # the three frames' positions through one turn of the shaft, as a crank and rod give them
    curves = []
    for k in range(3):
        pts = []
        for i in range(73):
            a = math.radians(i * 5 - 120 * k)
            yv = r * math.cos(a) + math.sqrt(L * L - (r * math.sin(a)) ** 2) - L
            pts.append((gx0 + (gx1 - gx0) * i / 72, gy - yv * amp / r))
        curves.append(pts)
    d.lines(curves)
    d.group('mid')
    d.text(sx, 18, 'CRANK, ROD AND FRAME', size=8)
    d.text(sx - 42, fy + r + 3, 'STROKE', size=7, anchor='end')
    d.text(ex, 18, 'THREE THROWS AT 120°', size=8)
    d.text(lx, ly + lr + 16, 'SPACERS SET THE PLANK', size=8)
    d.text(gx0, gy + amp + 12, '0°', size=7)
    d.text(gx0 + (gx1 - gx0) / 3, gy + amp + 12, '120°', size=7)
    d.text(gx0 + 2 * (gx1 - gx0) / 3, gy + amp + 12, '240°', size=7)
    d.text(gx1, gy + amp + 12, '360°', size=7)
    return d


PLATES['wind-sawmill'] = wind_sawmill
