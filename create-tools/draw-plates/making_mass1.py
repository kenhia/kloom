"""Plates for How We Build's Making many segment, part mass1 (sprint 026):
the Portsmouth block mills, interchangeable parts and Ford's moving line."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _rect(cx, cy, w, h):
    return [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]


def _chamfered(cx, cy, w, h, c):
    """A rectangle with its corners cut off at 45°, `c` along each edge."""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    return [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)]


def _shaped(cx, cy, w, h, c, bulge, n=10):
    """The chamfered outline with each long face swept to a shallow curve, as the shaping engine left it."""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    pts = [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c)]
    # the right face, bowed outwards by `bulge` at its middle
    for i in range(1, n):
        t = i / n
        pts.append((x1 + bulge * math.sin(math.pi * t), y0 + c + (h - 2 * c) * t))
    pts += [(x1, y1 - c), (x1 - c, y1), (x0 + c, y1), (x0, y1 - c)]
    for i in range(1, n):
        t = i / n
        pts.append((x0 - bulge * math.sin(math.pi * t), y1 - c - (h - 2 * c) * t))
    pts.append((x0, y0 + c))
    return pts


def block_mills():
    """A block shell through the six machines, in elevation, with the working points carried through every
    stage; below, the four parts of a finished block exploded along the pin's axis."""
    d = D()
    w, h = 40, 58                               # the shell's face, in the plate's units
    cy = 74                                     # the row's centre line
    xs = [42 + 63 * k for k in range(6)]        # six stages, left to right
    wp = cy + h / 2 - 7                         # the working points: two marks pressed in by the boring machine
    d.group('thin')
    d.line((14, cy), (386, cy))                                          # the centre line of the row
    d.line((14, wp), (386, wp))                                          # the line of the working points
    for x in xs:
        d.line((x, cy - h / 2 - 12), (x, cy + h / 2 + 12))
    # the exploded block's axis and the projectors from its parts
    ay = 214
    d.line((40, ay), (370, ay))
    d.group()
    # 1 the sawn blank
    d.line(*_rect(xs[0], cy, w, h), closed=True)
    # 2 bored: the same blank with the pin hole and the holes that start the mortise
    d.line(*_rect(xs[1], cy, w, h), closed=True)
    # 3 mortised: the slot for the sheave cut through
    d.line(*_rect(xs[2], cy, w, h), closed=True)
    # 4 the corners sawn off
    d.line(*_chamfered(xs[3], cy, w, h, 7), closed=True)
    # 5 and 6 shaped: each face swept to a curve
    d.line(*_shaped(xs[4], cy, w, h, 7, 3.5), closed=True)
    d.line(*_shaped(xs[5], cy, w, h, 7, 3.5), closed=True)
    d.group('mid')
    for k, x in enumerate(xs):
        if k >= 1:
            d.circle(x, cy, 3.2)                                         # the pin hole
        if k == 1:
            d.circle(x, cy - 16, 3), d.circle(x, cy + 16, 3)             # holes to start the mortise
        if k >= 2:
            # the mortise, a slot with rounded ends, around the pin hole
            sw, sh = 7, 40
            d.line((x - sw / 2, cy - sh / 2 + 3.5), (x - sw / 2, cy + sh / 2 - 3.5))
            d.line((x + sw / 2, cy - sh / 2 + 3.5), (x + sw / 2, cy + sh / 2 - 3.5))
            d.arc(x, cy - sh / 2 + 3.5, sw / 2, 180, 360, n=10)
            d.arc(x, cy + sh / 2 - 3.5, sw / 2, 0, 180, n=10)
        if k == 5:
            # the score: a groove for the strop, over the ends of the shell
            d.lines([[(x - 4, cy - h / 2 - 1), (x - 4, cy - h / 2 + 5), (x + 4, cy - h / 2 + 5), (x + 4, cy - h / 2 - 1)],
                     [(x - 4, cy + h / 2 + 1), (x - 4, cy + h / 2 - 5), (x + 4, cy + h / 2 - 5), (x + 4, cy + h / 2 + 1)]])
        if k >= 1:
            # the working points, a small cross either side, at the same height in every stage
            for sx in (x - w / 2 + 6, x + w / 2 - 6):
                d.lines([[(sx - 2.5, wp), (sx + 2.5, wp)], [(sx, wp - 2.5), (sx, wp + 2.5)]])
        if k < 5:
            # an arrow on to the next machine
            ax0, ax1 = x + w / 2 + 5, xs[k + 1] - w / 2 - 5
            d.line((ax0, cy - h / 2 - 8), (ax1, cy - h / 2 - 8))
            d.line((ax1 - 4, cy - h / 2 - 11), (ax1, cy - h / 2 - 8), (ax1 - 4, cy - h / 2 - 5))
    d.group()
    # the finished block exploded along the pin: shell in section, sheave, coak, pin
    sx = 92                                     # the shell, cut through the mortise, seen from the side
    d.line((sx - 30, ay - 40), (sx + 30, ay - 40), (sx + 36, ay - 34), (sx + 36, ay + 34), (sx + 30, ay + 40),
           (sx - 30, ay + 40), (sx - 36, ay + 34), (sx - 36, ay - 34), closed=True)
    d.line((sx - 6, ay - 32), (sx + 6, ay - 32), (sx + 6, ay + 32), (sx - 6, ay + 32), closed=True)  # the mortise
    hx = 196                                    # the sheave, face on, with its groove
    d.circle(hx, ay, 31)
    d.circle(hx, ay, 26)
    cx_ = 268                                   # the coak, a flanged bush
    d.circle(cx_, ay, 12)
    d.circle(cx_, ay, 5)
    px = 330                                    # the pin, end on and along
    d.line((px - 22, ay - 4), (px + 26, ay - 4), (px + 26, ay + 4), (px - 22, ay + 4), closed=True)
    d.line((px - 28, ay - 6), (px - 22, ay - 6), (px - 22, ay + 6), (px - 28, ay + 6), closed=True)  # its square end
    d.group('mid')
    d.circle(hx, ay, 12)                        # the seat in the sheave the coak fills
    for a in range(0, 360, 60):                 # rivets through the coak's flange
        u = _dir(a)
        d.circle(cx_ + u[0] * 9, ay + u[1] * 9, 1.1)
    d.group('mid')
    for k, x in enumerate(xs):
        d.text(x, cy + h / 2 + 24, str(k + 1), size=9)
    d.text(200, cy + h / 2 + 42, '+ WORKING POINTS, THE SAME IN EVERY STAGE', size=7)
    d.text(sx, ay + 58, 'SHELL', size=8)
    d.text(hx, ay + 58, 'SHEAVE', size=8)
    d.text(cx_, ay + 58, 'COAK', size=8)
    d.text(px, ay + 58, 'PIN', size=8)
    d.text(200, 18, 'SAW · BORE · MORTISE · CORNER · SHAPE · SCORE', size=8)
    return d


PLATES = {'block-mills': block_mills}


def interchangeable_parts():
    """A part in its fixture, its holes dimensioned from one datum; and a hole in section with its
    go and no-go plugs, the tolerance drawn far larger than life."""
    d = D()
    # the part: a flat bar with three holes, held against a datum face and a stop
    px0, py0, pw, ph = 30, 70, 196, 64
    s = 2.9                                      # plate units per millimetre: holes at 20, 40, 60 mm
    holes = [px0 + 20 * s, px0 + 40 * s, px0 + 60 * s]
    hy = py0 + ph / 2
    d.group('thin')
    d.line((px0, py0 - 34), (px0, py0 + ph + 52))                       # the datum face, produced
    for x in holes:
        d.line((x, py0 - 30), (x, hy + 10))
    # baseline dimensions: every hole from the datum
    for k, x in enumerate(holes):
        y = py0 - 8 - 9 * k
        d.line((px0, y), (x, y))
        d.lines([[(x - 3, y - 2), (x, y), (x - 3, y + 2)]])
    # the hole section's centre line, and the two limits produced across it
    gx, gy = 316, 196                            # the hole's axis and the face of the part
    lo, hi = 22, 30                              # half the smallest and largest hole allowed (much exaggerated)
    d.line((gx, 40), (gx, 286))
    d.line((gx - hi, 44), (gx - hi, gy + 84))
    d.line((gx + hi, 44), (gx + hi, gy + 84))
    d.line((gx - lo, 128), (gx - lo, gy + 84))
    d.line((gx + lo, 128), (gx + lo, gy + 84))
    d.group()
    # the fixture: a base and a datum block the part sits against
    d.line((px0 - 14, py0 + ph + 10), (px0 + pw + 14, py0 + ph + 10), (px0 + pw + 14, py0 + ph + 26),
           (px0 - 14, py0 + ph + 26), closed=True)
    d.line((px0 - 14, py0 + ph + 10), (px0 - 14, py0 - 4), (px0, py0 - 4), (px0, py0 + ph + 10))
    # the part
    d.line(*_rect(px0 + pw / 2, hy, pw, ph), closed=True)
    # the part in section at the hole, cut by the gauge's axis
    d.line((gx - 74, gy), (gx - 26, gy), (gx - 26, gy + 80), (gx - 74, gy + 80))
    d.line((gx + 74, gy), (gx + 26, gy), (gx + 26, gy + 80), (gx + 74, gy + 80))
    d.group('mid')
    for x in holes:
        d.circle(x, hy, 7)
    # the clamp pressing the part to the base
    d.line((px0 + pw - 10, py0 - 4), (px0 + pw - 10, py0 - 22), (px0 + pw + 14, py0 - 22))
    d.line((px0 + pw - 16, py0 - 4), (px0 + pw - 4, py0 - 4))
    # hatching of the cut part in section
    for k in range(9):
        y = gy + 6 + k * 9
        d.line((gx - 72, y + 6), (gx - 64, y - 2))
        d.line((gx + 64, y + 6), (gx + 72, y - 2))
    d.group()
    # the gauge: a handle, the go end in the hole, the no-go end above it
    d.line((gx - 6, 78), (gx + 6, 78), (gx + 6, 128), (gx - 6, 128), closed=True)          # the handle
    d.line((gx - lo + 1, 128), (gx + lo - 1, 128), (gx + lo - 1, gy + 44), (gx - lo + 1, gy + 44), closed=True)  # GO, down in the hole
    d.line((gx - hi - 2, 78), (gx + hi + 2, 78), (gx + hi + 2, 52), (gx - hi - 2, 52), closed=True)  # NO GO, too big to enter
    d.group('mid')
    d.text(px0 + 4, py0 + ph + 64, 'DATUM', size=8, anchor='start')
    for k, (x, v) in enumerate(zip(holes, (20, 40, 60))):
        d.text(x + 4, py0 - 11 - 9 * k, str(v), size=7, anchor='start')
    d.text(gx + 42, 68, 'NO GO', size=8, anchor='start')
    d.text(gx + 36, 160, 'GO', size=8, anchor='start')
    d.text(gx, 300 - 4, 'LIMITS', size=7)
    d.text(128, 24, 'ONE DATUM', size=8)
    d.text(316, 24, 'TWO LIMITS', size=8)
    return d


PLATES['interchangeable-parts'] = interchangeable_parts


def assembly_line():
    """The line in plan, chassis drawn along it past five stations; below, the stations' work against the
    cycle time, as first divided and rebalanced (the invented times of the reading's table)."""
    d = D()
    y0, y1 = 44, 76                              # the rails of the line, in plan
    stations = [60 + 70 * k for k in range(5)]
    d.group('thin')
    for x in stations:
        d.line((x, 26), (x, 104))
    # the time diagram's axes: seconds up the side, 10 s a grid line
    bx0, by = 40, 266
    sc = 1.9                                     # plate units per second
    d.line((bx0, by), (390, by))
    d.line((bx0, by), (bx0, by - 70 * sc))
    for t in range(10, 71, 10):
        d.line((bx0 - 3, by - t * sc), (bx0, by - t * sc))
    d.group()
    d.line((20, y0), (390, y0))
    d.line((20, y1), (390, y1))
    # chassis frames on the line, one at each station, each a ladder of two rails and cross members
    for x in stations:
        d.line((x - 22, y0 + 6), (x + 22, y0 + 6), (x + 22, y1 - 6), (x - 22, y1 - 6), closed=True)
    # the station times as bars
    times = [40, 55, 48, 62, 45]
    for k, t in enumerate(times):
        x = stations[k]
        d.line((x - 14, by), (x - 14, by - t * sc), (x + 14, by - t * sc), (x + 14, by))
    d.group('mid')
    for x in stations:
        d.lines([[(x - 22, y0 + 6 + 20 * j / 2), (x + 22, y0 + 6 + 20 * j / 2)] for j in (1,)] +
                [[(x - 12, y0 + 6), (x - 12, y1 - 6)], [(x + 12, y0 + 6), (x + 12, y1 - 6)]])
        d.circle(x - 16, y1 + 16, 5)             # a man on each side of his station
        d.circle(x + 16, y0 - 16, 5)
    # the chain's links between the rails' centres
    d.lines([[(20 + 10 * k, (y0 + y1) / 2 - 2), (26 + 10 * k, (y0 + y1) / 2 + 2)] for k in range(37)
             if all(abs(23 + 10 * k - x) > 26 for x in stations)])
    # direction of travel
    d.line((18, 128), (58, 128))
    d.line((52, 124), (58, 128), (52, 132))
    # the cycle lines: 62 s as divided, 52 s rebalanced
    d.line((bx0, by - 62 * sc), (390, by - 62 * sc))
    d.line((bx0, by - 52 * sc), (390, by - 52 * sc))
    # each station's idle time, a dotted drop from its bar to the cycle line
    for k, t in enumerate(times):
        x = stations[k]
        if t < 62:
            d.lines([[(x, by - t * sc - 2 - 5 * j), (x, by - t * sc - 4 - 5 * j)] for j in range(int((62 - t) * sc / 5))])
    d.group('mid')
    for k, x in enumerate(stations):
        d.text(x, 116, str(k + 1), size=9)
        d.text(x, by - times[k] * sc + 12, str(times[k]), size=7)
    d.text(66, 131, 'TRAVEL', size=7, anchor='start')
    d.text(392, by - 62 * sc - 4, '62 s', size=7, anchor='end')
    d.text(392, by - 52 * sc + 10, '52 s', size=7, anchor='end')
    d.text(bx0, by + 14, 'SECONDS OF WORK PER STATION', size=7, anchor='start')
    d.text(200, 16, 'THE LINE IN PLAN', size=8)
    return d


PLATES['assembly-line'] = assembly_line
