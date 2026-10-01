"""Plates for How We Build's Metal by fire segment, part forge3 (sprint 026):
coalbrookdale, steam-hammer and arc-welding."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _circle_pts(cx, cy, r, a0, a1, n=48):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def coalbrookdale():
    """The Iron Bridge in elevation, to scale (span 30.6 m, a semicircular lower rib), with one
    rib-to-radial blind dovetail and one wedged mortise and tenon drawn out beside it."""
    d = D()
    s = 220 / 30.6                       # px per metre: the 100 ft 6 in span drawn 220 px wide
    cx, gy = 150, 232                    # the arch's centre, on the springing line
    R1 = 15.3 * s                        # the lower rib: a semicircle on the span
    R2, R3 = R1 + 1.5 * s, R1 + 3.0 * s  # middle and outer ribs, concentric (spacing drawn, not surveyed)
    deck = gy - R1 - 0.9 * s             # the deck, just over the crown
    xo = cx + R1 + 2.6 * s               # the outer verticals, at the abutment faces
    d.group('thin')
    # the springing line and the river, the centre line, the radius, the span dimension
    d.line((cx - R1 - 26, gy), (cx + R1 + 26, gy))
    d.line((cx, deck - 22), (cx, gy + 10))
    u = _dir(-58)
    d.line((cx, gy), (cx + u[0] * R1, gy + u[1] * R1))
    yd = gy + 22
    d.line((cx - R1, yd), (cx + R1, yd))
    d.lines([[(cx - R1, yd - 4), (cx - R1, yd + 4)], [(cx + R1, yd - 4), (cx + R1, yd + 4)]])
    for k in range(7):
        x0 = cx - R1 + 22 + k * 34
        d.line((x0, gy + 8), (x0 + 12, gy + 8))
    d.group()
    # the lower rib, the inner and outer verticals, the deck
    d.line(*_circle_pts(cx, gy, R1, 180, 360, 72))
    d.lines([[(cx - R1, gy), (cx - R1, deck)], [(cx + R1, gy), (cx + R1, deck)]])
    d.lines([[(cx - xo + cx, gy), (cx - xo + cx, deck)], [(xo, gy), (xo, deck)]])
    d.line((cx - xo + cx - 6, deck), (xo + 6, deck))
    d.group('mid')
    # middle and outer ribs: arcs from the inner vertical up to where they meet the deck
    for R in (R2, R3):
        a_top = math.degrees(math.asin((gy - deck) / R))           # where the arc meets the deck
        a_side = math.degrees(math.acos(R1 / R))                    # where it meets the inner vertical
        d.line(*_circle_pts(cx, gy, R, 180 + a_side, 180 + a_top, 24))
        d.line(*_circle_pts(cx, gy, R, 360 - a_top, 360 - a_side, 24))
    # radials tying the ribs together, on rays from the centre
    segs = []
    for a in (214, 236, 258, 282, 304, 326):
        p, q = _dir(a), _dir(a)
        segs.append([(cx + p[0] * R1, gy + p[1] * R1), (cx + q[0] * min(R3, (gy - deck) / -q[1] if q[1] < 0 else R3),
                                                      gy + q[1] * min(R3, (gy - deck) / -q[1] if q[1] < 0 else R3))])
    d.lines(segs)
    # the decorative circles in the spandrels, between the outer vertical and the ribs
    for side in (-1, 1):
        x = cx + side * (R1 + 1.3 * s)
        d.circle(x, deck + 0.0 + 18, 9)
    d.group('mid')
    # detail 1: a blind dovetail, the radial drawn out of its socket in the rib
    bx, by = 338, 100
    d.line((bx - 36, by), (bx + 36, by), (bx + 36, by + 20), (bx - 36, by + 20), closed=True)      # the rib
    t = 9                                                                                           # tail half-width at the root
    d.line((bx - t, by), (bx - t - 4, by + 12), (bx + t + 4, by + 12), (bx + t, by))                # the socket
    oy = -30                                                                                        # drawn out by this much
    d.line((bx - t, by + oy - 30), (bx - t, by + oy), (bx - t - 4, by + oy + 12),
           (bx + t + 4, by + oy + 12), (bx + t, by + oy), (bx + t, by + oy - 30))                  # the radial and its tail
    d.lines([[(bx + 22, by + oy + 4), (bx + 22, by - 4)], [(bx + 19, by - 9), (bx + 22, by - 4), (bx + 25, by - 9)]])
    # detail 2: a mortise and tenon through an upright, locked by a wedge
    mx, my = 338, 210
    d.line((mx - 9, my - 52), (mx - 9, my + 52))
    d.line((mx + 9, my - 52), (mx + 9, my + 52))                                                    # the upright
    d.line((mx - 9, my - 6), (mx + 9, my - 6))
    d.line((mx - 9, my + 6), (mx + 9, my + 6))                                                      # the mortise
    d.line((mx - 40, my - 6), (mx + 22, my - 6), (mx + 22, my + 6), (mx - 40, my + 6))               # rib and tenon, through
    d.line((mx + 14, my - 14), (mx + 18, my - 14), (mx + 17, my + 14), (mx + 15, my + 14), closed=True)  # the wedge
    d.group('mid')
    d.text(cx, gy + 36, '30.6 M', size=8)
    d.text(cx + u[0] * R1 * 0.55 + 10, gy + u[1] * R1 * 0.55 - 2, 'R 15.3', size=8, anchor='start')
    d.text(bx, by + 36, 'BLIND DOVETAIL', size=8)
    d.text(mx, my + 66, 'WEDGED TENON', size=8)
    d.text(cx, 18, 'ONE OF FIVE RIBS, ELEVATION', size=8)
    return d


PLATES = {'coalbrookdale': coalbrookdale}


def steam_hammer():
    """Nasmyth's hammer in elevation, after his sketch of 24 November 1839: an inverted cylinder on
    two legs, the piston rod fixed to the block, the anvil, and the fall h. Beside it, a square bar
    in section under the dies: a light blow works only the metal near the dies, a heavy one works
    through to the core (the forging cross)."""
    d = D()
    cx = 140                             # the hammer's centre line
    ay = 238                             # top of the anvil block
    d.group('thin')
    d.line((cx, 14), (cx, 280))
    d.line((20, 270), (262, 270))                                            # the floor
    # the fall: block's face at the top of its stroke, and the work's top face
    top_face, work_top = 128, 204
    d.lines([[(cx + 40, top_face), (cx + 92, top_face)], [(cx + 40, work_top), (cx + 92, work_top)]])
    d.line((cx + 84, top_face), (cx + 84, work_top))
    d.lines([[(cx + 80, top_face + 6), (cx + 84, top_face), (cx + 88, top_face + 6)],
             [(cx + 80, work_top - 6), (cx + 84, work_top), (cx + 88, work_top - 6)]])
    d.group()
    # the two legs: curved standards from the floor up to the cylinder's base plate
    for side in (-1, 1):
        leg = []
        for i in range(25):
            u = i / 24
            x = cx + side * (96 - 66 * math.sin(math.pi / 2 * u) ** 1.4)
            leg.append((x, 270 - u * (270 - 70)))
        d.line(*leg)
        outer = [(cx + side * (abs(x - cx) + 14), y) for x, y in leg]
        d.line(*outer)
    d.line((cx - 50, 70), (cx + 50, 70))                                     # the base plate
    d.line((cx - 20, 70), (cx - 20, 22), (cx + 20, 22), (cx + 20, 70))       # the cylinder
    # the anvil block on the floor and the work on it
    d.line((cx - 42, 270), (cx - 42, ay), (cx + 42, ay), (cx + 42, 270))
    d.line((cx - 30, ay), (cx - 30, work_top), (cx + 30, work_top), (cx + 30, ay))
    # the hammer block at the top of its stroke, hung on the piston rod
    d.line((cx - 26, top_face), (cx - 26, 96), (cx + 26, 96), (cx + 26, top_face), closed=True)
    d.group('mid')
    d.line((cx, 96), (cx, 40))                                               # the piston rod
    d.line((cx - 18, 40), (cx + 18, 40))                                     # the piston
    d.lines([[(cx - 26, 104), (cx - 31, 104)], [(cx + 26, 104), (cx + 31, 104)]])  # guides
    d.line((cx + 20, 30), (cx + 44, 30), (cx + 44, 60), (cx + 20, 60))        # the slide valve chest
    d.line((cx + 44, 45), (cx + 70, 45))                                     # the steam pipe
    # glowing work: a few heat lines
    d.lines([[(cx - 22 + 11 * k, work_top + 8), (cx - 18 + 11 * k, work_top + 26)] for k in range(5)])
    d.group('mid')
    # the bar in section, twice: light blow and heavy blow
    for k, heavy in enumerate((False, True)):
        bx, by, h = 330, 70 + k * 120, 52
        d.line((bx - h / 2, by), (bx + h / 2, by), (bx + h / 2, by + h), (bx - h / 2, by + h), closed=True)
        d.lines([[(bx - 36, by - 4), (bx + 36, by - 4)], [(bx - 36, by + h + 4), (bx + 36, by + h + 4)]])  # the dies
        if heavy:
            # the forging cross: shear bands from corner to corner, meeting at the core
            d.lines([[(bx - h / 2 + 4, by + 4), (bx + h / 2 - 4, by + h - 4)],
                     [(bx + h / 2 - 4, by + 4), (bx - h / 2 + 4, by + h - 4)]])
        else:
            # only lenses of worked metal under each die
            for yy, sgn in ((by, 1), (by + h, -1)):
                d.line(*[(bx - 20 + 40 * i / 16, yy + sgn * 9 * math.sin(math.pi * i / 16)) for i in range(17)])
    d.group('mid')
    d.text(cx + 98, (top_face + work_top) / 2 + 3, 'h', size=9, anchor='start')
    d.text(330, 140, 'LIGHT BLOW', size=8)
    d.text(330, 260, 'HEAVY BLOW', size=8)
    d.text(cx - 26, 50, 'CYLINDER', size=8, anchor='end')
    d.text(cx, 288, 'ANVIL', size=8)
    return d


PLATES['steam-hammer'] = steam_hammer


def arc_welding():
    """Shielded metal arc welding. Left, along the joint: the coated electrode tilted 10 degrees
    towards travel, an arc gap equal to its core's diameter, the pool under the arc and the bead
    behind it under its slag, inside the coating's gas shield. Right, across the joint: a 60-degree
    V groove filled bead by bead."""
    d = D()
    py = 196                              # top of the plate along the joint
    tx = 150                              # the electrode's tip, over the pool
    core = 6                              # the core wire's diameter, px
    gap = core                            # arc length about the electrode's diameter (TM 9-2852)
    tilt = 10                             # degrees from vertical, leaning towards travel (+x)
    ax, ay = math.sin(math.radians(tilt)), -math.cos(math.radians(tilt))   # up the electrode
    nx, ny = -ay, ax                      # across it
    tip = (tx, py - gap)
    L = 150
    d.group('thin')
    d.line((tx, py), (tx, 22))                                                 # the vertical
    d.line(tip, (tip[0] + ax * (L + 20), tip[1] + ay * (L + 20)))              # the electrode's axis
    d.arc(tx, py - gap, 70, -90 - 0.01, -90 + tilt, n=10)
    d.line((20, py + 52), (262, py + 52))                                      # the plate's underside
    d.lines([[(tx + 18, py - gap), (tx + 30, py - gap)], [(tx + 18, py), (tx + 30, py)]])
    d.group()
    # the plate, the frozen bead behind the arc, the pool under it
    d.line((20, py), (tx - 92, py))
    bead = [(tx - 92 + i * 2.0, py - 7 * math.sin(math.pi / 2 * min(1, i / 6, (42 - i) / 5))) for i in range(43)]
    d.line(*bead)
    pool = [(tx - 8 + 16 * i / 12, py + 6 * math.sin(math.pi * i / 12)) for i in range(13)]
    d.line(*pool)
    d.line((tx + 8, py), (262, py))
    # the electrode: core wire inside its coating, the coating standing a little proud at the tip
    for off, back in ((core / 2, 4), (-core / 2, 4), (core / 2 + 3.5, 0), (-core / 2 - 3.5, 0)):
        a = (tip[0] + nx * off + ax * back, tip[1] + ny * off + ay * back)
        b = (tip[0] + nx * off + ax * L, tip[1] + ny * off + ay * L)
        d.line(a, b)
    d.group('mid')
    # the arc, drops crossing it, the gas shield, the slag over the bead, the travel arrow
    d.lines([[(tip[0] - 2, tip[1] + 2), (tx - 3, py + 1)], [(tip[0] + 2, tip[1] + 2), (tx + 3, py + 1)]])
    d.lines([[(tx - 1, py - 4), (tx + 1, py - 3)]])
    shield = [(tx + 26 * math.cos(math.radians(a)), py - 4 + 26 * math.sin(math.radians(a))) for a in range(190, 351, 10)]
    d.line(*shield)
    slag = [(x, y - 3) for x, y in bead[2:36]]
    d.line(*slag)
    d.lines([[(196, 100), (236, 100)], [(230, 96), (236, 100), (230, 104)]])
    d.group('mid')
    # across the joint: two plates with a 60-degree V and a root gap, filled in three passes
    vx, vy, th = 330, 150, 52
    half = math.tan(math.radians(30)) * th
    rg = 3
    d.line((vx - 58, vy), (vx - rg - half, vy), (vx - rg, vy + th), (vx - 58, vy + th), closed=True)
    d.line((vx + 58, vy), (vx + rg + half, vy), (vx + rg, vy + th), (vx + 58, vy + th), closed=True)
    for k, f in enumerate((0.3, 0.65, 1.0)):
        y = vy + th - f * th
        w = rg + half * f
        d.line((vx - w, y), *[(vx + w * math.cos(math.radians(a)), y - 6 * math.sin(math.radians(a))) for a in range(180, -1, -15)][1:])
    d.group('mid')
    d.text(tx - 6, 18, 'ELECTRODE', size=8, anchor='end')
    d.text(tx + 34, py - 1, 'GAP = d', size=8, anchor='start')
    d.text(tx - 5, 128, '10°', size=8, anchor='end')
    d.text(tx - 46, py + 24, 'BEAD', size=8)
    d.text(216, 92, 'TRAVEL', size=8)
    d.text(vx, vy + th + 22, '60° V, 3 PASSES', size=8)
    return d


PLATES['arc-welding'] = arc_welding
