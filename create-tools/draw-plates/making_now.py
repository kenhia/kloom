"""Plates for How We Build's last segment, Making now (sprint 026)."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def euv():
    """The EUV light source in section, and a Mo/Si multilayer mirror reflecting in step."""
    d = D()
    ay = 140                                   # the optical axis
    f1x, f2x = 78, 238                         # the plasma (first focus) and the intermediate focus
    cx = (f1x + f2x) / 2
    c = (f2x - f1x) / 2
    a = 104
    b = math.sqrt(a * a - c * c)

    def ell(t):
        return cx + a * math.cos(math.radians(t)), ay + b * math.sin(math.radians(t))

    # the collector: the part of the ellipse round the first focus, with a hole on the axis for the laser
    upper = [ell(t) for t in range(118, 171, 2)]
    lower = [ell(t) for t in range(190, 243, 2)]
    d.group('thin')
    d.line((14, ay), (262, ay))                                   # the axis
    d.line(*[ell(t) for t in range(-60, 61, 4)])                  # the rest of the ellipse, faint
    for x in (f1x, f2x):
        d.line((x, ay - 6), (x, ay + 6))
    d.line((f1x, 26), (f1x, 112))                                 # the droplets' path
    d.group()
    d.line(*upper)
    d.line(*lower)
    # the intermediate focus: a narrow aperture in a wall
    d.line((f2x, ay - 52), (f2x, ay - 4))
    d.line((f2x, ay + 4), (f2x, ay + 52))
    d.group('mid')
    # rays from the plasma to the collector and on to the intermediate focus: exact, by the ellipse's foci
    rays = []
    for t in (124, 140, 156, 204, 220, 236):
        px, py = ell(t)
        rays.append([(f1x, ay), (px, py), (f2x, ay)])
        # and a little beyond, opening out towards the illuminator
        ux, uy = f2x - px, ay - py
        n = math.hypot(ux, uy)
        rays.append([(f2x, ay), (f2x + ux / n * 26, ay + uy / n * 26)])
    d.lines(rays)
    # the laser, coming in along the axis through the hole in the collector
    d.lines([[(16, ay - 3), (f1x - 8, ay - 3)], [(16, ay + 3), (f1x - 8, ay + 3)]])
    d.lines([[(f1x - 14, ay - 7), (f1x - 8, ay - 3), (f1x - 14, ay + 1)]])
    # tin droplets falling, then the pancake the pre-pulse makes, then the plasma
    for k in range(5):
        d.circle(f1x, 34 + k * 17, 2.2)
    d.ellipse(f1x, ay - 13, 6, 1.6)
    for k in range(8):
        u = _dir(k * 45)
        d.line((f1x + u[0] * 3, ay + u[1] * 3), (f1x + u[0] * 7, ay + u[1] * 7))
    d.group()
    # the multilayer mirror in section: alternating layers, light coming in and going out in step
    mx0, mx1, my = 286, 392, 172
    period = 9
    layers = 8
    for k in range(layers + 1):
        y = my + k * period
        d.line((mx0, y), (mx1, y))
    d.group('mid')
    for k in range(layers):
        y = my + k * period + period * 0.38                      # the molybdenum, thinner than the silicon
        d.line((mx0, y), (mx1, y))
    # incoming rays, a few degrees off normal, each reflected from a deeper boundary
    inc = 8                                                    # degrees from the normal
    ux, uy = math.sin(math.radians(inc)), math.cos(math.radians(inc))
    rays = []
    for k in range(4):
        hx = 316 + k * 10
        hy = my + k * period * 2
        top = (hx - ux * (hy - 60), 60)
        rays.append([top, (hx, hy)])
        rays.append([(hx, hy), (hx + ux * (hy - 60), 60)])
    d.lines(rays)
    d.group('thin')
    # the period, dimensioned at the side
    dx = mx1 + 2
    d.line((mx0 - 10, my), (mx0 - 10, my + 2 * period))
    d.lines([[(mx0 - 14, my), (mx0 - 6, my)], [(mx0 - 14, my + 2 * period), (mx0 - 6, my + 2 * period)]])
    d.group('mid')
    d.text(f1x, 18, 'TIN', size=8)
    d.text(30, ay - 10, 'LASER', size=8)
    d.text(f2x, ay + 66, 'IF', size=8)
    d.text(cx - 10, 268, 'THE SOURCE IN SECTION', size=8)
    d.text(339, 52, '13.5 nm', size=8)
    d.text(mx0 - 16, my + 2 * period + 14, '2d', size=8, anchor='end')
    d.text(339, my + layers * period + 22, 'Mo / Si, d ≈ 6.8 nm', size=8)
    return d


PLATES = {'euv': euv}


def where_making_is():
    """A logarithmic rule of the precision of making, from a cylinder's error to a layer's overlay."""
    d = D()
    x0, x1, ry = 24, 380, 186                 # the rule runs from 10 mm (left) to 0.1 nm (right)
    dec0, dec1 = 1, -7                         # decades of millimetres: 10¹ down to 10⁻⁷ (0.1 nm)

    def X(mm):
        return x0 + (dec0 - math.log10(mm)) / (dec0 - dec1) * (x1 - x0)

    d.group('thin')
    d.line((x0, ry - 70), (x1, ry - 70))
    for k in range(dec1, dec0 + 1):
        x = X(10 ** k)
        d.line((x, ry - 74), (x, ry + 10))
    d.group()
    # the rule: a bar with decade ticks long and log-spaced minor ticks short
    d.line((x0, ry), (x1, ry), (x1, ry + 22), (x0, ry + 22), closed=True)
    ticks = []
    for k in range(dec1, dec0):
        for m in range(1, 10):
            x = X(m * 10 ** k)
            h = 12 if m == 1 else (8 if m == 5 else 5)
            ticks.append([(x, ry), (x, ry + h)])
    ticks.append([(X(10 ** dec0), ry), (X(10 ** dec0), ry + 12)])
    d.lines(ticks)
    d.group('mid')
    # the frames' precisions as pointers above the rule, with their years
    marks = [
        (1.2, '1776'),       # Wilkinson's 50-inch cylinder: an old shilling
        (0.0254, '1800s'),   # Maudslay's Lord Chancellor, read to a thousandth of an inch (Nasmyth)
        (0.001, '1909'),     # Johansson's blocks, in steps of a micrometre
        (0.005, '2011'),      # Lego's moulds, within five micrometres
        (0.0000009, '2024'),  # ASML's NXE:3800E, matched overlay 0.9 nm
    ]
    for k, (mm, year) in enumerate(marks):
        x = X(mm)
        top = ry - 30 - (0, 0, 0, 1, 0)[k] * 18     # label heights chosen so neighbours do not touch
        d.line((x, top), (x, ry - 3))
        d.line((x - 3, ry - 9), (x, ry - 3), (x + 3, ry - 9))
        d.text(x, top - 5, year, size=8)
    # at left, a bore out of round, exaggerated; at right, two layers that do not quite align
    bx, by = 60, 64
    d.line(*[(bx + (24 + 3 * math.cos(2 * math.radians(t))) * math.cos(math.radians(t)),
              by + (24 + 3 * math.cos(2 * math.radians(t))) * math.sin(math.radians(t))) for t in range(0, 361, 6)])
    d.group('thin')
    d.circle(bx, by, 24)
    d.lines([[(bx - 30, by), (bx + 30, by)], [(bx, by - 30), (bx, by + 30)]])
    d.group('mid')
    ox, oy = 322, 52
    for k in range(4):
        d.line((ox + k * 12, oy), (ox + k * 12 + 6, oy), (ox + k * 12 + 6, oy + 26), (ox + k * 12, oy + 26), closed=True)
        d.line((ox + k * 12 + 2, oy + 4), (ox + k * 12 + 8, oy + 4), (ox + k * 12 + 8, oy + 30),
               (ox + k * 12 + 2, oy + 30), closed=True)
    d.group('mid')
    for mm, s in ((1, '1 mm'), (0.001, '1 µm'), (0.000001, '1 nm')):
        d.text(X(mm), ry + 38, s, size=8)
    d.text(bx, by + 44, 'BORE', size=8)
    d.text(ox + 22, oy + 46, 'OVERLAY', size=8)
    d.text(200, 286, 'THE ERROR, MILLIMETRES TO NANOMETRES, LOG SCALE', size=8)
    return d


PLATES['where-making-is'] = where_making_is
