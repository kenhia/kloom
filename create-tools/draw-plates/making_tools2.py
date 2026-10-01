"""Plates for How We Build's Machines that make machines, part two (sprint 026):
the universal milling machine's dividing head, Johansson's gauge blocks and
Taylor's tool-life curve."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _gear(cx, cy, r, teeth, depth, start=-90):
    """A spur gear's outline: `teeth` flat-topped teeth of `depth` on a root circle of `r`."""
    pts = []
    for k in range(teeth):
        a0 = start + 360 * k / teeth
        step = 360 / teeth
        for frac, rr in ((0.0, r), (0.15, r + depth), (0.5, r + depth), (0.65, r)):
            u = _dir(a0 + frac * step)
            pts.append((cx + u[0] * rr, cy + u[1] * rr))
    return pts


def milling_machine():
    d = D()
    pcx, pcy, pr = 118, 156, 84            # the index plate, seen face on
    r27 = 68                               # the 27-hole circle
    r21 = 52                               # the 21-hole circle inside it
    wcx, wcy, wr = 304, 112, 54            # the 40-tooth worm wheel on the spindle
    gr = 28                                # the 27-tooth gear being cut, on the same spindle
    wy = wcy + wr + 12                     # the worm's axis, under the wheel
    d.group('thin')
    # centre lines of plate, spindle and worm shaft
    d.line((pcx - pr - 14, pcy), (pcx + pr + 14, pcy))
    d.line((pcx, pcy - pr - 14), (pcx, pcy + pr + 14))
    d.line((wcx - wr - 16, wcy), (wcx + wr + 16, wcy))
    d.line((wcx, wcy - wr - 16), (wcx, wy + 22))
    d.line((pcx, pcy), (wcx - 40, wy), (wcx + 40, wy))
    # the hole circles' pitch lines
    d.circle(pcx, pcy, r27)
    d.circle(pcx, pcy, r21)
    # radial lines to the gear's tooth spaces, every one of the 27
    segs = []
    for k in range(27):
        u = _dir(-90 + 360 * k / 27)
        segs.append([(wcx + u[0] * (gr - 6), wcy + u[1] * (gr - 6)), (wcx + u[0] * (wr - 4), wcy + u[1] * (wr - 4))])
    d.lines(segs[:1])
    d.group()
    # the index plate, the worm wheel and the worm
    d.circle(pcx, pcy, pr)
    d.circle(pcx, pcy, 10)
    d.line(*_gear(wcx, wcy, wr, 40, 4), closed=True)
    d.line((wcx - 38, wy - 7), (wcx + 38, wy - 7), (wcx + 38, wy + 7), (wcx - 38, wy + 7), closed=True)
    d.group('mid')
    # the holes: 27 on the outer circle, 21 on the inner
    for n, r, hr in ((27, r27, 2.6), (21, r21, 2.2)):
        for k in range(n):
            u = _dir(-90 + 360 * k / n)
            d.circle(pcx + u[0] * r, pcy + u[1] * r, hr)
    # the worm's thread, slanted at its lead angle
    d.lines([[(wcx - 34 + 7 * k, wy + 7), (wcx - 30 + 7 * k, wy - 7)] for k in range(10)])
    # the gear blank with its 27 tooth spaces, cut one by one
    d.line(*_gear(wcx, wcy, gr - 4, 27, 3), closed=True)
    d.circle(wcx, wcy, 5)
    # the crank: one turn and 13 holes of 27 from the hole it started in
    a13 = -90 + 360 * 13 / 27
    u = _dir(a13)
    d.line((pcx, pcy), (pcx + u[0] * (r27 + 22), pcy + u[1] * (r27 + 22)))
    d.circle(pcx + u[0] * r27, pcy + u[1] * r27, 5)
    d.circle(pcx + u[0] * (r27 + 22), pcy + u[1] * (r27 + 22), 6)
    # the sector arms spanning the 13 holes, and the arc of the move
    for a in (-90, a13):
        v = _dir(a)
        d.line((pcx + v[0] * 14, pcy + v[1] * 14), (pcx + v[0] * (r27 + 10), pcy + v[1] * (r27 + 10)))
    d.arc(pcx, pcy, r27 + 8, -90, a13, n=40)
    d.group('mid')
    d.text(pcx, 26, 'INDEX PLATE', size=8)
    d.text(wcx, 26, 'SPINDLE', size=8)
    d.text(pcx + 46, pcy - 70, '27', size=8, anchor='start')
    d.text(pcx + 4, pcy - 30, '21', size=8, anchor='start')
    d.text(wcx + wr + 18, wcy + 4, '40 T', size=8, anchor='start')
    d.text(wcx, wy + 26, 'WORM 40:1', size=8)
    d.text(pcx, 286, '40 ÷ 27 = 1 TURN + 13/27', size=8)
    d.text(wcx - wr - 10, wcy - wr + 4, 'GEAR, 27 T', size=8, anchor='end')
    return d


PLATES = {'milling-machine': milling_machine}


def gauge_blocks():
    d = D()
    s = 4.2                                   # px per mm
    base = 262                                # the surface plate's top
    stacks = [                                # bottom to top, each a list of block lengths in mm
        (96, [25, 14, 1.37, 1.008]),          # Johansson's 112-block set of 1909
        (204, [30, 7, 2.37, 2.008]),          # a modern 2 mm-based set
    ]
    w = 58
    d.group('thin')
    d.line((40, base + 12), (360, base + 12))
    top = base - 41.378 * s
    d.line((40, top), (290, top))             # the length reached, carried across both stacks
    dx = 52
    d.line((dx, base), (dx, top))
    d.lines([[(dx - 4, base), (dx + 4, base)], [(dx - 4, top), (dx + 4, top)]])
    d.group()
    d.line((30, base), (370, base), (370, base + 12), (30, base + 12), closed=True)
    for x, blocks in stacks:
        y = base
        for L in blocks:
            h = L * s
            d.line((x - w / 2, y), (x + w / 2, y), (x + w / 2, y - h), (x - w / 2, y - h), closed=True)
            y -= h
    d.group('mid')
    # the inset: two lapped faces wrung, the film between them magnified
    ix, iy = 330, 70
    d.line((ix - 34, iy - 26), (ix + 34, iy - 26))
    d.line((ix - 34, iy - 4), (ix + 34, iy - 4))
    d.line((ix - 34, iy + 4), (ix + 34, iy + 4))
    d.line((ix - 34, iy + 26), (ix + 34, iy + 26))
    rough = [(ix - 34 + 2 * k, iy - 4 + 1.2 * math.sin(k * 1.9)) for k in range(35)]
    d.line(*rough)
    d.circle(ix, iy, 42)
    # a leader from the inset down to the joint it magnifies
    d.line((ix - 30, iy + 30), (204 + w / 2 + 4, base - 30 * s))
    # the cruciform start of a wring, in plan, small
    cx, cy = 342, 196
    d.line((cx - 22, cy - 7), (cx + 22, cy - 7), (cx + 22, cy + 7), (cx - 22, cy + 7), closed=True)
    d.line((cx - 7, cy - 22), (cx + 7, cy - 22), (cx + 7, cy + 22), (cx - 7, cy + 22), closed=True)
    d.arc(cx, cy, 28, -70, -20, n=12)
    d.lines([[(cx + 23, cy - 21), (cx + 26, cy - 9), (cx + 15, cy - 14)]])
    d.group('mid')
    for x, blocks in stacks:
        y = base
        thin = 0
        for L in blocks:
            h = L * s
            if h > 12:
                d.text(x, y - h / 2 + 3, f'{L:g}', size=8)
            else:
                d.text(x + w / 2 + 6, y - h / 2 + 6 - 11 * thin, f'{L:g}', size=7, anchor='start')
                thin += 1
            y -= h
    d.text(96, base + 26, '1909 SET', size=8)
    d.text(204, base + 26, 'MODERN SET', size=8)
    d.text(dx - 6, top - 8, '41.378 mm', size=8, anchor='start')
    d.text(ix, iy + 54, 'FILM ≈ 10 nm', size=8)
    d.text(cx, cy + 36, 'WRING', size=8)
    return d


PLATES['gauge-blocks'] = gauge_blocks


def high_speed_steel():
    d = D()
    x0, y0 = 52, 238                          # the plot's origin
    sx, sy = 2.6, 2.3                         # px per minute, px per foot a minute
    tmax, vmax = 90, 80
    d.group('thin')
    for t in range(10, tmax + 1, 10):
        d.line((x0 + t * sx, y0), (x0 + t * sx, y0 - vmax * sy))
    for v in range(10, vmax + 1, 10):
        d.line((x0, y0 - v * sy), (x0 + tmax * sx, y0 - v * sy))
    d.group()
    d.line((x0, y0 - vmax * sy), (x0, y0), (x0 + tmax * sx, y0))
    # Taylor's curve for a high-speed tool, V = 90 / T^(1/8)
    d.line(*[(x0 + t * sx, y0 - 90 / t ** 0.125 * sy) for t in [5 + 0.5 * k for k in range(171)]])
    d.group('mid')
    # the 20- and 80-minute speeds carried to the axis: 61.9 and 52.0 ft/min, a ratio of 0.84
    for t in (20, 80):
        v = 90 / t ** 0.125
        d.line((x0 + t * sx, y0 - v * sy), (x0, y0 - v * sy))
    # Taylor's four test points, read from his Fig. 104
    for t, v in ((10, 67), (20, 62), (40, 55.5), (80, 52)):
        d.circle(x0 + t * sx, y0 - v * sy, 3)
    d.group('mid')
    # the tool, in side elevation, with its 6° clearance and 8° back slope
    tx, ty = 330, 120                         # the cutting corner
    L = 70
    top_end = (tx + L, ty - L * math.tan(math.radians(8)))
    d.line((tx, ty), top_end)
    face_end = (tx + 46 * math.tan(math.radians(6)), ty + 46)
    d.line((tx, ty), face_end)
    d.line(face_end, (tx + L, ty + 46), top_end)
    d.line((tx, ty), (tx, ty + 52))                     # the vertical, for the clearance angle
    d.line((tx, ty), (tx + L + 6, ty))                  # the horizontal, for the back slope
    d.arc(tx, ty, 30, 90 - 6, 90, n=8)
    d.arc(tx, ty, 40, -8, 0, n=8)
    # the work, turning past the tool
    d.arc(tx - 64, ty + 6, 64, -40, 40, n=24)
    d.group('mid')
    d.text(x0 + 45 * sx, y0 + 26, 'T, MINUTES BEFORE REGRINDING', size=8)
    d.text(x0 - 8, y0 - 80 * sy - 8, 'V, FT/MIN', size=8, anchor='start')
    for t in (20, 40, 80):
        d.text(x0 + t * sx, y0 + 12, str(t), size=7)
    for v in (20, 40, 60, 80):
        d.text(x0 - 6, y0 - v * sy + 3, str(v), size=7, anchor='end')
    d.text(x0 + 58 * sx, y0 - 66 * sy, 'VTⁿ = 90', size=8)
    d.text(x0 + 58 * sx, y0 - 30 * sy, 'n = 1/8', size=8)
    d.text(tx + 12, ty + 66, '6°', size=8)
    d.text(tx + 46, ty - 14, '8°', size=8)
    d.text(tx + 30, 40, 'THE TOOL', size=8)
    return d


PLATES['high-speed-steel'] = high_speed_steel
