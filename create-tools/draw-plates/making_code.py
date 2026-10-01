"""Plates for How We Build's segment Code and machine (sprint 026, part `code`)."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def numerical_control():
    """A quarter circle cut as chords; a detail of one chord with the sagitta it
    leaves and the staircase of X and Y pulses along it; and the tape."""
    d = D()
    cx, cy, R = 40, 270, 200                   # the arc's centre, low left; a quarter circle up and right
    n = 5                                      # chords over the quarter: few, so they show
    angs = [-90 * k / n for k in range(n + 1)]
    pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in angs]
    # the detail: one chord drawn large, its arc on a radius chosen so the sagitta reads
    dx, dy, dr = 318, 92, 62                    # the detail circle
    half = 52                                   # half the chord in the detail
    Rd = 150                                    # the detail's arc radius: sagitta = Rd - sqrt(Rd^2 - half^2)
    sag = Rd - math.sqrt(Rd * Rd - half * half)
    ccx, ccy = dx, dy + 14 + Rd - sag           # the detail arc's centre, far below
    chord_y = dy + 14
    d.group('thin')
    d.line((cx - 10, cy), (cx + R + 20, cy))
    d.line((cx, cy + 10), (cx, cy - R - 20))
    d.lines([[(cx, cy), p] for p in pts[1:-1]])
    d.arc(cx, cy, R, 0, -90, n=90)
    d.circle(dx, dy, dr)
    # a leader from the chord the detail enlarges to the detail circle
    m = ((pts[2][0] + pts[3][0]) / 2, (pts[2][1] + pts[3][1]) / 2)
    ang = math.atan2(m[1] - dy, m[0] - dx)
    d.line(m, (dx + dr * math.cos(ang), dy + dr * math.sin(ang)))
    d.group()
    d.line(*pts)
    d.line((dx - half, chord_y), (dx + half, chord_y))
    d.group('mid')
    # the detail's true arc, and the sagitta from the chord's middle up to it
    a = math.degrees(math.asin(half / Rd))
    d.arc(ccx, ccy, Rd, -90 - a, -90 + a, n=40)
    d.line((dx, chord_y), (dx, chord_y - sag))
    d.lines([[(dx - 4, chord_y - sag), (dx + 4, chord_y - sag)]])
    # the director's pulses along the chord: equal steps on both axes, a staircase
    x0, y0, x1, y1 = dx - half, chord_y + 18, dx + half, chord_y + 30
    steps = 8
    stair = [(x0, y0)]
    for k in range(1, steps + 1):
        x = x0 + (x1 - x0) * k / steps
        stair += [(x, stair[-1][1]), (x, y0 + (y1 - y0) * k / steps)]
    d.line(*stair)
    # the tape: seven tracks, holes punched in rows, a sprocket row of small holes
    tx, ty, tw, th = 262, 196, 124, 62
    d.line((tx, ty), (tx + tw, ty))
    d.line((tx, ty + th), (tx + tw, ty + th))
    pattern = [0b1010011, 0b0110101, 0b1100110, 0b0011011, 0b1001101, 0b0101110,
               0b1110001, 0b0010111, 0b1011010, 0b0111001, 0b1100011, 0b0001111, 0b1000110]
    for r, bits in enumerate(pattern):
        x = tx + 8 + r * 9
        d.circle(x, ty + 30, 0.8)
        for t in range(7):
            if bits >> t & 1:
                d.circle(x, ty + 7 + t * 7 + (4 if t >= 3 else 0), 2.1)
    d.group('mid')
    d.text(cx + R * 0.45, cy - R * 0.17, 'R', size=9)
    d.text(dx + 8, chord_y - sag / 2 + 3, 's', size=9, anchor='start')
    d.text(dx, dy - dr - 8, 'ONE CHORD', size=8)
    d.text(x1 + 6, y1 + 3, 'X, Y', size=8, anchor='start')
    d.text(tx + tw / 2, ty - 8, 'SEVEN-TRACK TAPE', size=8)
    return d


PLATES = {'numerical-control': numerical_control}


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def bezier_curves():
    """De Casteljau's construction for a cubic at t = 1/2, on the reading's invented control points."""
    d = D()
    # the reading's points, (0, 0) (20, 60) (90, 80) (120, 20), drawn at 2.6 px a unit with y up
    s, ox, oy = 2.6, 44, 262
    P = [(0, 0), (20, 60), (90, 80), (120, 20)]
    pt = lambda p: (ox + p[0] * s, oy - p[1] * s)
    Q = [pt(p) for p in P]
    t = 0.5
    L1 = [_lerp(Q[i], Q[i + 1], t) for i in range(3)]
    L2 = [_lerp(L1[i], L1[i + 1], t) for i in range(2)]
    M = _lerp(L2[0], L2[1], t)
    curve = []
    for i in range(121):
        u = i / 120
        a = [_lerp(Q[k], Q[k + 1], u) for k in range(3)]
        b = [_lerp(a[k], a[k + 1], u) for k in range(2)]
        curve.append(_lerp(b[0], b[1], u))
    d.group('thin')
    # the grid the points are given on, every 20 units
    for gx in range(0, 141, 20):
        d.line(pt((gx, -6)), pt((gx, 90)))
    for gy in range(0, 81, 20):
        d.line(pt((-6, gy)), pt((140, gy)))
    d.group('mid')
    # the control polygon
    d.line(*Q)
    d.group('mid')
    # the first and second levels of interpolation, each a half-way point
    d.line(*L1)
    d.line(*L2)
    for p in L1 + L2:
        d.circle(p[0], p[1], 2.2)
    d.group()
    # the curve, and the point the construction lands on
    d.line(*curve)
    d.circle(M[0], M[1], 3.6)
    for p in Q:
        d.circle(p[0], p[1], 3)
    d.group('mid')
    for i, (p, (dx, dy, anc)) in enumerate(zip(Q, [(-8, 14, 'end'), (-8, -6, 'end'), (0, -12, 'middle'), (10, 4, 'start')])):
        d.text(p[0] + dx, p[1] + dy, f'P{i}', size=9, anchor=anc)
    d.text(M[0], M[1] + 18, 't = ½', size=9)
    return d


PLATES['bezier-curves'] = bezier_curves


def g_code():
    """The reading's invented program in plan and elevation: the cut, the rapids,
    and the arc's centre found from its start by I and J."""
    d = D()
    s, ox, oy = 4.0, 84, 176                    # 4 px a millimetre; the work origin in plan, y up
    pt = lambda x, y: (ox + x * s, oy - y * s)
    ez = 250                                    # the elevation: Z 0, the work's top face, at this height
    ep = lambda x, z: (ox + x * s, ez - z * s)
    arc = [pt(40 + 10 * math.cos(math.radians(a)), 10 + 10 * math.sin(math.radians(a))) for a in range(-90, 91, 6)]
    d.group('thin')
    # plan: the axes from the origin and a 10 mm grid; elevation: the top face and the block
    d.line(pt(-12, 0), pt(66, 0))
    d.line(pt(0, -10), pt(0, 34))
    for gx in range(10, 61, 10):
        d.line(pt(gx, -3), pt(gx, 30))
    for gy in (10, 20, 30):
        d.line(pt(-3, gy), pt(62, gy))
    d.line(ep(-12, 0), ep(66, 0))
    d.line(ep(-8, 0), ep(-8, -8), ep(62, -8), ep(62, 0))
    # projectors from plan to elevation at the start and the far point of the arc
    d.lines([[pt(0, -10), ep(0, 7)], [pt(50, 0), ep(50, 7)]])
    # the rapids, G0: in to Z 5 above the start, and back up at the end
    d.line(ep(-12, 14), ep(0, 5))
    d.line(ep(0, 5), ep(0, 0))
    d.group()
    # the cut, G1 and G3 at Z -2: in plan the outline, in elevation the feed down and along
    d.line(pt(0, 0), pt(40, 0), *arc, pt(0, 20), pt(0, 0))
    d.line(ep(0, 0), ep(0, -2), ep(50, -2))
    d.group('mid')
    # I and J: the offsets from the arc's start to its centre; the 6 mm cutter at the arc's far point
    c = pt(40, 10)
    d.line(pt(40, 0), c)
    d.circle(c[0], c[1], 1.8)
    tip = pt(50, 10)
    d.circle(tip[0], tip[1], 3 * s)
    d.group('mid')
    d.text(*pt(20, -5), 'N60 G1', size=8)
    d.text(pt(50, 19)[0] + 4, pt(50, 19)[1], 'N70 G3', size=8, anchor='start')
    d.text(*pt(20, 22.5), 'N80 G1', size=8)
    d.text(pt(0, 10)[0] - 6, pt(0, 10)[1] + 3, 'N90', size=8, anchor='end')
    d.text(pt(40, 5)[0] - 5, pt(40, 5)[1] + 3, 'J10', size=8, anchor='end')
    d.text(pt(0, 0)[0] - 5, pt(0, 0)[1] + 12, 'X0 Y0', size=8, anchor='end')
    d.text(ep(0, 5)[0] + 5, ep(0, 5)[1] - 3, 'Z5', size=8, anchor='start')
    d.text(ep(50, -2)[0] + 6, ep(50, -2)[1] + 3, 'Z-2', size=8, anchor='start')
    d.text(ep(62, 0)[0] + 4, ep(62, 0)[1] - 22, 'ELEVATION', size=8, anchor='end')
    d.text(pt(62, 30)[0] + 4, pt(62, 30)[1] - 10, 'PLAN', size=8, anchor='end')
    return d


PLATES['g-code'] = g_code
