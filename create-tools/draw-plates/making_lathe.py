"""Plates for How We Build's Lathe work trail (sprint 026, part `lathe`)."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _gear(d, cx, cy, teeth, module, phase=0.0):
    """A spur gear's outline, its teeth drawn as trapezoids on the pitch circle (module in px)."""
    rp = teeth * module / 2                  # pitch radius
    ra, rf = rp + module, rp - 1.25 * module  # addendum and dedendum circles
    pts = []
    for k in range(teeth):
        a0 = phase + 360 * k / teeth
        step = 360 / teeth
        for frac, r in ((0.0, rf), (0.12, rf), (0.27, ra), (0.48, ra), (0.63, rf), (1.0, rf)):
            u = _dir(a0 + frac * step)
            pts.append((cx + r * u[0], cy + r * u[1]))
    d.line(*pts, closed=True)
    return rp


# ---------------------------------------------------------------- pole lathe

def pole_lathe():
    d = D()
    gy = 270                                  # the floor
    bx0, bx1, by = 96, 236, 176               # the bed (cheeks) of the lathe
    ax = 132                                  # the work's axis height
    lp, rp = 128, 204                         # the two puppets, carrying the pikes (centres)
    wx0, wx1, wr = lp + 6, rp - 6, 13         # the billet between the pikes
    gx = wx0 + 18                             # the groove the cord runs in
    # the pole: a cantilever pinned at the ceiling, its free end over the work
    px0, py0 = 20, 26
    L = gx - px0                              # its free end hangs over the groove
    def pole(defl):
        pts = []
        for i in range(41):
            x = L * i / 40
            y = defl * (3 * L * x * x - x ** 3) / (2 * L ** 3)   # end-loaded cantilever
            pts.append((px0 + x, py0 + 4 + y))
        return pts
    rest, drawn = pole(0), pole(34)
    # the treadle: hinged on the floor behind, its fore end tied to the cord
    hx, tl = 40, 196
    def treadle(a):
        u = _dir(-a)
        return (hx, gy), (hx + tl * u[0], gy + tl * u[1])
    t_up, t_down = treadle(13), treadle(3)
    d.group('thin')
    d.line((10, gy), (390, gy))
    d.line((px0 - 10, py0), (px0 + 70, py0))                     # the ceiling timber
    d.line((wx0 - 22, ax), (wx1 + 22, ax))                        # the axis through the pikes
    d.line(*rest)                                                 # the pole at rest
    d.line(*t_up)                                                 # the treadle raised
    d.line((gx, ax - wr), (gx, 14))                               # the cord's line, produced
    d.group()
    # legs and cheeks
    d.lines([[(bx0 + 6, by), (bx0 + 6, gy)], [(bx1 - 6, by), (bx1 - 6, gy)]])
    d.line((bx0, by), (bx1, by), (bx1, by + 10), (bx0, by + 10), closed=True)
    # puppets with their pikes
    for x, sgn in ((lp, 1), (rp, -1)):
        d.line((x - 6, by), (x - 6, ax - 12), (x + 6, ax - 12), (x + 6, by))
        d.line((x + sgn * 6, ax - 2), (x + sgn * 12, ax), (x + sgn * 6, ax + 2))
    # the billet
    d.line((wx0, ax - wr), (wx1, ax - wr), (wx1, ax + wr), (wx0, ax + wr), closed=True)
    # the pole drawn down, and the treadle trodden down
    d.line(*drawn)
    d.line(*t_down)
    d.group('mid')
    # the groove and the cord: from the pole's end, once round the billet, down to the treadle's end
    d.lines([[(gx - 5, ax - wr), (gx - 5, ax + wr)], [(gx + 5, ax - wr), (gx + 5, ax + wr)]])
    end = drawn[-1]
    d.line((end[0], end[1]), (gx + 3, ax - wr))
    d.line((gx - 3, ax - wr), (gx + 3, ax + wr))
    d.line((gx - 3, ax + wr), t_down[1])
    # the rest, and the gouge on it, cutting on the down stroke
    d.line((wx0 + 30, ax + wr + 10), (wx1, ax + wr + 10))
    d.line((wx1 - 34, ax + wr + 9), (wx1 - 10, ax + wr + 40), (wx1 - 6, ax + wr + 37), (wx1 - 30, ax + wr + 6))
    # rotation arrows on the billet's end
    d.arc(wx1 + 30, ax, 14, 200, 340, n=20)
    d.lines([[(wx1 + 30 + 14 * math.cos(math.radians(340)) - 5, ax + 14 * math.sin(math.radians(340)) - 3),
              (wx1 + 30 + 14 * math.cos(math.radians(340)), ax + 14 * math.sin(math.radians(340))),
              (wx1 + 30 + 14 * math.cos(math.radians(340)) - 1, ax + 14 * math.sin(math.radians(340)) - 7)]])
    d.arc(wx1 + 30, ax, 22, 20, 160, n=20)
    d.lines([[(wx1 + 30 + 22 * math.cos(math.radians(160)) + 6, ax + 22 * math.sin(math.radians(160)) + 2),
              (wx1 + 30 + 22 * math.cos(math.radians(160)), ax + 22 * math.sin(math.radians(160))),
              (wx1 + 30 + 22 * math.cos(math.radians(160)) + 2, ax + 22 * math.sin(math.radians(160)) - 6)]])
    d.group('mid')
    # the cut in section: the billet's end, the gouge's edge a little above the axis, the shaving
    sx, sy, sr = 316, 196, 30
    d.circle(sx, sy, sr)
    d.line((sx - 4, sy), (sx + 4, sy))
    d.line((sx, sy - 4), (sx, sy + 4))
    d.group('thin')
    d.line((sx - sr - 14, sy), (sx + sr + 30, sy))
    d.line((sx + sr + 2, sy - 9), (sx + sr + 50, sy - 9))
    d.group()
    # the gouge, its edge at the surface 9 px (a quarter inch at this scale) above the axis
    ey = sy - 9
    ex = sx + math.sqrt(sr * sr - 9 * 9)
    d.line((ex, ey), (ex + 40, ey + 12), (ex + 40, ey + 18), (ex + 2, ey + 5), closed=True)
    d.arc(sx, sy, sr + 5, -38, -14, n=8)                    # the shaving lifting off
    d.group('mid')
    d.text(px0 + 60, py0 + 20, 'POLE', size=8)
    d.text(hx + 110, gy - 8, 'TREADLE', size=8)
    d.text(wx1 + 30, ax - 28, 'CUT', size=8)
    d.text(wx1 + 30, ax + 36, 'RETURN', size=8)
    d.text(sx, sy + sr + 18, 'GOUGE ABOVE THE AXIS', size=8)
    d.text(sx + sr + 30, ey - 5, '¼ in', size=8)
    return d


PLATES = {'pole-lathe': pole_lathe}


# ---------------------------------------------------------- between centres

def between_centres():
    d = D()
    ax = 128                                  # the axis
    hx = 70                                   # the headstock centre's point
    tx = 300                                  # the tailstock centre's point
    half = math.tan(math.radians(30))         # a 60° centre: 30° either side of the axis
    d.group('thin')
    d.line((14, ax), (386, ax))
    # the 60° included angle, set out at the tailstock centre
    for s in (1, -1):
        d.line((tx, ax), (tx + 60, ax + s * 60 * half))
    d.arc(tx, ax, 30, -30, 30, n=16)
    # projection lines from the two diameters down to the section
    d.lines([[(150, ax - 26), (150, 222)], [(236, ax - 18), (236, 222)]])
    d.group()
    # headstock: spindle nose and driver plate
    d.line((14, ax - 30), (40, ax - 30), (40, ax + 30), (14, ax + 30))
    d.line((40, ax - 58), (48, ax - 58), (48, ax + 58), (40, ax + 58), closed=True)
    # the live centre: a 60° cone in the spindle
    d.line((48, ax - 12), (hx - 12 / half * half, ax - 12), (hx, ax), (hx - 12, ax + 12), (48, ax + 12))
    # the work: two diameters on one axis, centre holes at both ends
    w0, w1 = 76, 294
    r1, r2 = 26, 18
    d.line((w0, ax - r1), (196, ax - r1), (196, ax - r2), (w1, ax - r2), (w1, ax + r2),
           (196, ax + r2), (196, ax + r1), (w0, ax + r1), closed=True)
    # tailstock: barrel, and the dead centre's cone
    d.line((tx, ax), (tx + 14, ax - 9), (336, ax - 9), (336, ax - 16), (386, ax - 16))
    d.line((tx, ax), (tx + 14, ax + 9), (336, ax + 9), (336, ax + 16), (386, ax + 16))
    d.group('mid')
    # centre holes drilled into the work's ends
    for x0, s in ((w0, 1), (w1, -1)):
        d.line((x0, ax - 6), (x0 + s * 6 / half * 0.5, ax - 1.5), (x0 + s * 9, ax - 1.5),
               (x0 + s * 9, ax + 1.5), (x0 + s * 6 / half * 0.5, ax + 1.5), (x0, ax + 6))
    # the dog clamped on the work, its tail in the driver plate's slot
    d.line((84, ax - r1 - 8), (100, ax - r1 - 8), (100, ax + r1 + 8), (84, ax + r1 + 8), closed=True)
    d.line((92, ax - r1 - 8), (92, ax - 50), (50, ax - 50))
    d.line((92, ax - r1 - 8), (92, ax - r1 - 18))
    d.circle(92, ax + r1 + 14, 4)
    # the slide rest and the tool, at the larger diameter, feeding towards the headstock
    d.line((150, ax + r1 + 2), (162, ax + r1 + 14), (162, ax + r1 + 48), (138, ax + r1 + 48), (138, ax + r1 + 14), closed=True)
    d.line((118, ax + r1 + 48), (182, ax + r1 + 48), (182, ax + r1 + 60), (118, ax + r1 + 60), closed=True)
    d.line((130, ax + r1 + 72), (110, ax + r1 + 72))
    d.lines([[(110, ax + r1 + 72), (116, ax + r1 + 68)], [(110, ax + r1 + 72), (116, ax + r1 + 76)]])
    d.group('mid')
    # the section through the work: the two diameters as circles on one centre
    sx, sy = 193, 256
    d.circle(sx, sy, 26 * 0.9)
    d.circle(sx, sy, 18 * 0.9)
    d.lines([[(sx - 30, sy), (sx + 30, sy)], [(sx, sy - 30), (sx, sy + 30)]])
    d.group('mid')
    d.text(hx - 10, ax - 66, 'LIVE', size=8)
    d.text(tx + 40, ax - 26, 'DEAD', size=8)
    d.text(tx + 36, ax + 40, '60°', size=8)
    d.text(108, ax - r1 - 14, 'DOG', size=8, anchor='start')
    d.text(150, ax + r1 + 94, 'FEED', size=8, anchor='end')
    d.text(sx + 40, sy + 4, 'ONE AXIS', size=8, anchor='start')
    d.text(200, 22, 'n = 1000 v ÷ π d', size=9)
    return d


PLATES['between-centres'] = between_centres


# ------------------------------------------------------------ screw cutting

def screw_cutting():
    d = D()
    m = 1.25                                  # px per module: a 127-tooth gear is about 160 px across
    # gear centres: spindle (60 T) above, idler between, lead screw (127 T) below
    s_c = (82, 70)
    r_s = 60 * m / 2
    r_l = 127 * m / 2
    r_i = 40 * m / 2
    l_c = (s_c[0] + 22, 0)
    # place the lead-screw gear so that it is below and the idler meshes both
    l_c = (s_c[0] + 30, 196)
    # the idler's centre: at distance r_s + r_i from the spindle gear and r_l + r_i from the lead-screw gear
    dx, dy = l_c[0] - s_c[0], l_c[1] - s_c[1]
    dist = math.hypot(dx, dy)
    a, b = r_s + r_i, r_l + r_i
    t = (a * a - b * b + dist * dist) / (2 * dist)
    h = math.sqrt(max(a * a - t * t, 0))
    ix = s_c[0] + t * dx / dist + h * dy / dist
    iy = s_c[1] + t * dy / dist - h * dx / dist
    d.group('thin')
    d.line(s_c, (ix, iy), l_c)                                     # the line of centres
    for c, r in ((s_c, r_s), ((ix, iy), r_i), (l_c, r_l)):
        d.circle(c[0], c[1], r)                                    # pitch circles
    ly = l_c[1]
    d.line((l_c[0], ly), (392, ly))                                # the lead screw's axis
    wy = 52
    d.line((s_c[0], wy + 18), (s_c[0], s_c[1]))
    d.line((150, wy), (392, wy))                                   # the work's axis
    d.group()
    _gear(d, s_c[0], s_c[1], 60, m)
    _gear(d, ix, iy, 40, m, phase=4.5)
    _gear(d, l_c[0], l_c[1], 127, m, phase=1.4)
    d.group('mid')
    # the lead screw: a square thread drawn along its axis, 8 to the inch at 6.4 px a pitch
    p = 6.4
    x = 196
    top, bot = ly - 7, ly + 7
    zz = []
    while x < 390:
        zz += [(x, top), (x + p / 2, top), (x + p / 2, bot), (x + p, bot)]
        x += p
    d.line(*zz)
    d.line((196, ly - 4), (390, ly - 4))
    d.line((196, ly + 4), (390, ly + 4))
    # the half-nut closed on it, and the carriage above carrying the tool to the work
    d.line((276, ly - 10), (304, ly - 10), (304, ly - 18), (276, ly - 18), closed=True)
    d.line((276, ly + 10), (304, ly + 10), (304, ly + 18), (276, ly + 18), closed=True)
    d.line((290, ly - 18), (290, wy + 26))
    d.line((280, wy + 26), (300, wy + 26), (290, wy + 12), closed=True)  # the 60° tool
    # the work: a thread of 1.5 mm pitch, 60° flanks, drawn at 4 px a pitch
    q = 4.0
    x = 160
    zz = []
    while x < 384:
        zz += [(x, wy - 10), (x + q / 2, wy - 10 + q / 2 / math.tan(math.radians(30)) * 0.9)]
        x += q / 2
        zz += [(x + q / 2, wy - 10)]
        x += q / 2
    d.line(*zz)
    d.line((160, wy + 10), (384, wy + 10))
    d.line((160, wy - 10), (160, wy + 10))
    # the thread dial, meshing the lead screw
    dc = (352, ly - 46)
    d.circle(dc[0], dc[1], 14)
    for k in range(8):
        u = _dir(45 * k - 90)
        d.line((dc[0] + 10 * u[0], dc[1] + 10 * u[1]), (dc[0] + 14 * u[0], dc[1] + 14 * u[1]))
    d.line((dc[0], dc[1] + 14), (dc[0], ly - 7))
    d.group('mid')
    d.text(s_c[0], s_c[1] + 3, '60', size=9)
    d.text(ix, iy + 3, 'IDLER', size=7)
    d.text(l_c[0], l_c[1] + 3, '127', size=9)
    d.text(240, ly + 32, 'LEAD SCREW 8 TPI', size=8, anchor='start')
    d.text(240, wy - 18, 'P = 1.5 mm', size=8, anchor='start')
    d.text(272, ly - 22, 'HALF-NUT', size=8, anchor='end')
    d.text(dc[0] + 18, dc[1] - 10, 'DIAL', size=8, anchor='start')
    return d


PLATES['screw-cutting'] = screw_cutting


# ------------------------------------------------------- ornamental turning

def ornamental_turning():
    d = D()
    # the rosette and its rubber, left: r = R + a cos(N θ)
    rx, ry, R, a, N = 74, 150, 52, 6, 12
    def rose(cx, cy, r0, amp, n, shift=0.0, steps=240):
        return [(cx + (r0 + amp * math.cos(n * (t - shift))) * math.cos(t),
                 cy + (r0 + amp * math.cos(n * (t - shift))) * math.sin(t))
                for t in (2 * math.pi * i / steps for i in range(steps + 1))]
    d.group('thin')
    d.circle(rx, ry, R)                                           # the mean circle
    d.circle(rx, ry, R + a)
    d.circle(rx, ry, R - a)
    d.lines([[(rx - R - 22, ry), (rx + R + 34, ry)], [(rx, ry - R - 22), (rx, ry + R + 22)]])
    # the rocking headstock's pivot, far below, and its arc of swing
    pvx, pvy = rx, 292
    d.line((pvx, pvy), (rx, ry))
    d.arc(pvx, pvy, pvy - ry, -96, -84, n=10)
    d.group()
    d.line(*rose(rx, ry, R, a, N))
    # the rubber: a roller held still, pressed against the rosette's edge by a spring
    gx = rx + R + a + 10
    d.circle(gx, ry, 10)
    d.line((gx + 10, ry), (gx + 30, ry))
    zz = [(gx + 30, ry)]
    for k in range(6):
        zz.append((gx + 34 + 4 * k, ry + (-5 if k % 2 == 0 else 5)))
    zz.append((gx + 60, ry))
    d.line(*zz)
    d.line((gx + 60, ry - 10), (gx + 60, ry + 10))
    d.group('mid')
    # the work, right: barleycorn, each cut shifted half a wave and taken a little nearer the centre
    wx, wy = 312, 150
    n2, amp2, r_out, dr = 24, 3.0, 76, 2.9
    for k in range(18):
        d.line(*rose(wx, wy, r_out - k * dr, amp2, n2, shift=(k % 2) * math.pi / n2, steps=288))
    d.group('thin')
    d.lines([[(wx - 96, wy), (wx + 96, wy)], [(wx, wy - 96), (wx, wy + 96)]])
    # one wave's angle, 360 ÷ 24 = 15°, set out from the centre
    for ang in (-90, -75):
        u = _dir(ang)
        d.line((wx, wy), (wx + 92 * u[0], wy + 92 * u[1]))
    d.group('mid')
    d.text(rx, 30, 'ROSETTE', size=8)
    d.text(gx + 4, ry + 26, 'RUBBER', size=8)
    d.text(pvx + 12, pvy - 6, 'PIVOT', size=8, anchor='start')
    d.text(wx, 30, 'THE WORK', size=8)
    d.text(wx + 30, wy - 98, '15°', size=8, anchor='start')
    d.text(wx, 282, 'SHIFT ½ WAVE · IN 0.025 in', size=8)
    return d


PLATES['ornamental-turning'] = ornamental_turning
