"""Plates for the chemistry subject's chemical revolution, part 2: oxygen, Lavoisier, Davy (sprint 025)."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _along(p, u, s):
    return (p[0] + u[0] * s, p[1] + u[1] * s)


def oxygen():
    """Priestley's twelve-inch lens (focus twenty inches) on red calx in an inverted tube of mercury, 1 August 1774,
    and the mass balance of 2 HgO -> 2 Hg + O2."""
    d = D()
    s = 5.0                                    # px per inch: the lens is 12 in across, its focus 20 in away
    a = math.radians(30)                       # the axis falls from the sun towards the tube
    u = (math.cos(a), math.sin(a))             # along the axis
    v = (-math.sin(a), math.cos(a))            # across it
    tx, crown, tr = 188, 128, 11               # the tube's axis, the top of its closed end, its radius
    F = (tx, crown + tr + 4)                   # the focus, on the calx at the top of the tube
    L = _along(F, u, -20 * s)                  # the lens's centre
    h = 6 * s                                  # half the aperture
    by, bw, level, gas = 250, 70, 236, 176     # basin floor, half-width; mercury in the basin; in the tube
    d.group('thin')
    # the optical axis, the lens's plane, the focal distance marked off, and the ground
    d.line(_along(L, u, -60), _along(F, u, 14))
    d.line(_along(L, v, -h - 12), _along(L, v, h + 12))
    d.lines([[_along(L, v, -h - 16), _along(F, v, -h - 16)],
             [_along(L, v, -h - 12), _along(L, v, -h - 20)], [_along(F, v, -h - 12), _along(F, v, -h - 20)]])
    d.line((tx, crown - 14), (tx, by + 10))
    d.line((20, by + 6), (380, by + 6))
    d.group()
    # the lens in section: two circular arcs meeting at the rim
    t = 5.0
    R = (h * h + t * t) / (2 * t)              # the radius that gives a sag of t over the half-aperture
    half = math.degrees(math.asin(h / R))
    for side in (1, -1):
        c = _along(L, u, -side * (R - t))
        base = math.degrees(math.atan2(u[1], u[0])) + (0 if side == 1 else 180)
        d.line(*[_pt(c, base + half * (2 * i / 24 - 1), R) for i in range(25)])
    # the tube, closed at the top, standing in the basin of mercury
    d.arc(tx, crown + tr, tr, 180, 360, n=16)
    d.line((tx - tr, crown + tr), (tx - tr, level + 8))
    d.line((tx + tr, crown + tr), (tx + tr, level + 8))
    d.line((tx - bw, level - 16), (tx - bw, by), (tx + bw, by), (tx + bw, level - 16))
    d.group('mid')
    # five rays of sunlight, parallel until the lens, then bent to the focus
    rays = []
    for k in (-1, -0.5, 0, 0.5, 1):
        p = _along(L, v, k * h * 0.9)
        rays.append([_along(p, u, -58), p, F])
    d.lines(rays)
    # the mercury: its surface in the basin, and lower in the tube where the new air has pushed it down
    d.lines([[(tx - bw + 2, level), (tx - tr, level)], [(tx + tr, level), (tx + bw - 2, level)],
             [(tx - tr, gas), (tx + tr, gas)]])
    hatch = []
    for x in range(int(tx - bw + 8), int(tx + bw - 4), 10):
        if abs(x - tx) > tr + 3:
            hatch.append([(x, by - 2), (x + 6, level + 4)])
    for y in range(gas + 8, level + 6, 10):
        hatch.append([(tx - tr + 2, y + 5), (tx + tr - 2, y - 1)])
    d.lines(hatch)
    # the red calx floating at the crown, and bubbles of the air rising off it
    d.line((tx - 7, crown + tr + 6), (tx - 3, crown + tr + 2), (tx + 4, crown + tr + 3), (tx + 7, crown + tr + 6))
    for yy, xx in ((152, tx - 3), (160, tx + 4), (168, tx - 2)):
        d.circle(xx, yy, 1.6)
    # the mass balance: 100 of calx splits into 92.6 of mercury and 7.4 of oxygen
    x0, x1, y0 = 256, 380, 60
    split = x0 + (x1 - x0) * 92.6 / 100
    d.group()
    d.line((x0, y0), (x1, y0), (x1, y0 + 12), (x0, y0 + 12), closed=True)
    d.line((x0, y0 + 36), (split - 2, y0 + 36), (split - 2, y0 + 48), (x0, y0 + 48), closed=True)
    d.line((split + 2, y0 + 36), (x1, y0 + 36), (x1, y0 + 48), (split + 2, y0 + 48), closed=True)
    d.group('thin')
    d.lines([[(x0, y0 + 14), (x0, y0 + 34)], [(split, y0 + 14), (split, y0 + 34)], [(x1, y0 + 14), (x1, y0 + 34)]])
    d.group('mid')
    d.text((x0 + x1) / 2, y0 - 6, '100 HgO', size=8)
    d.text((x0 + split) / 2, y0 + 62, '92.6 Hg', size=8)
    d.text(x1, y0 + 62, '7.4 O₂', size=8, anchor='end')
    d.text(*_along(_along(L, u, 10 * s), v, -h - 24), "20 IN", size=8)
    d.text(tx + bw + 8, level + 3, 'MERCURY', size=7, anchor='start')
    d.text(200, 284, '2 HgO → 2 Hg + O₂')
    return d


def lavoisier():
    """The Traite's Experiment Third in section: water boiled in a retort, its steam passed through a red-hot tube
    packed with a coil of iron, the water that survives condensed in a worm, and the gas collected over water."""
    d = D()
    gy = 252                                    # the ground
    E, F = (104, 150), (292, 170)               # the tube's two ends; it falls gently towards the worm
    dx, dy = F[0] - E[0], F[1] - E[1]
    n = math.hypot(dx, dy)
    u, v = (dx / n, dy / n), (-dy / n, dx / n)
    r = 5                                       # the tube's half-bore
    fx0, fx1 = 138, 256                         # the long furnace
    wx, wy0, wy1 = 322, 128, 214                # the worm tub's axis, top and bottom
    jx = 368                                    # the bell jar's axis
    on = lambda x: (x, E[1] + (x - E[0]) * dy / dx)
    d.group('thin')
    d.line((14, gy), (392, gy))
    d.line(_along(E, u, -30), _along(F, u, 20))
    d.lines([[(58, 150), (58, gy + 6)], [(wx, wy0 - 12), (wx, gy + 6)], [(jx, 168), (jx, gy + 6)],
             [((fx0 + fx1) / 2, 118), ((fx0 + fx1) / 2, gy + 6)]])
    d.group()
    # the retort A on its furnace, its neck rising to the tube
    d.arc(58, 190, 22, 0, 360, n=48)
    d.line(_pt((58, 190), -40, 22), _along(E, v, -r))
    d.line(_pt((58, 190), -12, 22), _along(E, v, r))
    d.line((32, 214), (32, gy), (84, gy), (84, 214))
    d.line((28, 214), (88, 214))
    # the tube EF, two walls, through the long furnace
    d.line(_along(E, v, -r), _along(F, v, -r))
    d.line(_along(E, v, r), _along(F, v, r))
    d.line((fx0, 128), (fx1, 128), (fx1, gy), (fx0, gy), closed=True)
    d.line((fx0 + 6, 134), (fx1 - 6, 134), (fx1 - 6, gy), (fx0 + 6, gy))
    # the worm tub, the worm's coil, the bottle H under it
    d.line((wx - 26, wy0), (wx - 26, wy1), (wx + 26, wy1), (wx + 26, wy0))
    d.line(_along(F, v, -r), (wx - 14, F[1] - r))
    d.line(_along(F, v, r), (wx - 14, F[1] + r))
    coil = []
    for i in range(121):
        t = i / 120 * 5 * 2 * math.pi
        coil.append((wx + 16 * math.cos(t + math.pi), 178 + t / (5 * 2 * math.pi) * 28 + 3 * math.sin(t + math.pi)))
    d.line(*coil)
    d.line((wx, 206), (wx, 222))
    d.arc(wx, 236, 13, -70, 250, n=36)
    # the gas pipe from the bottle's neck to the bell jar over the trough
    d.line((wx + 6, 226), (344, 226), (344, 244), (jx - 4, 244), (jx - 4, 214))
    d.line((jx - 20, 250), (jx - 20, 196), (jx - 14, 184), (jx + 14, 184), (jx + 20, 196), (jx + 20, 250))
    d.line((340, 212), (340, gy), (394, gy), (394, 212))
    d.group('mid')
    # water in the retort and in the trough, the gas space in the jar, the fire under both furnaces
    d.line(_pt((58, 190), 160, 22), _pt((58, 190), 20, 22))
    d.lines([[(340, 220), (jx - 20, 220)], [(jx + 20, 220), (394, 220)], [(jx - 20, 232), (jx + 20, 232)]])
    d.lines([[(44 + 8 * k, 244), (48 + 8 * k, 232), (52 + 8 * k, 244)] for k in range(4)])
    d.lines([[(fx0 + 16 + 14 * k, 244), (fx0 + 21 + 14 * k, 226), (fx0 + 26 + 14 * k, 244)] for k in range(7)])
    # the coil of iron inside the tube, from end to end of the furnace
    iron = []
    for i in range(161):
        x = fx0 + 8 + (fx1 - fx0 - 16) * i / 160
        c = on(x)
        iron.append((c[0], c[1] + (r - 1.5) * math.sin(i / 160 * 22 * math.pi)))
    d.line(*iron)
    # the balance sheet in grains: the water lost equals the iron's gain and the gas's weight
    x0, x1, y0 = 96, 304, 36
    split = x0 + (x1 - x0) * 85 / 100
    d.group()
    d.line((x0, y0), (x1, y0), (x1, y0 + 10), (x0, y0 + 10), closed=True)
    d.line((x0, y0 + 34), (split - 2, y0 + 34), (split - 2, y0 + 44), (x0, y0 + 44), closed=True)
    d.line((split + 2, y0 + 34), (x1, y0 + 34), (x1, y0 + 44), (split + 2, y0 + 44), closed=True)
    d.group('thin')
    d.lines([[(x, y0 + 12), (x, y0 + 32)] for x in (x0, split, x1)])
    d.group('mid')
    d.text(x1 + 8, y0 + 8, '100 WATER', size=8, anchor='start')
    d.text((x0 + split) / 2, y0 + 58, '85 INTO THE IRON', size=8)
    d.text(x1 + 8, y0 + 42, '15 GAS', size=8, anchor='start')
    d.text(58, 140, 'WATER', size=8)
    d.text((fx0 + fx1) / 2, 116, 'IRON, RED HOT', size=8)
    d.text(jx, 176, 'GAS', size=8)
    d.text(200, 280, 'GRAINS · TRAITÉ, EXPERIMENT THIRD', size=7)
    return d


def davy_electrolysis():
    """A voltaic pile in elevation, and Davy's experiment of October 1807: damp potash on a platinum disc made
    negative, a platinum wire made positive touching its top; metal at the disc, oxygen at the wire."""
    d = D()
    px, pw = 70, 30                             # the pile's axis and half-width
    top, cells, ch = 52, 12, 15                 # its top, its cells, each cell's height
    base = top + cells * ch
    cx, dy_, drx = 268, 206, 52                 # the platinum disc: centre, and its half-width seen edge-on
    wire_y = 52                                 # the positive lead
    d.group('thin')
    d.line((px, top - 12), (px, base + 14))
    d.line((cx, wire_y - 8), (cx, 262))
    d.line((16, 262), (384, 262))
    d.group()
    # the pile: from the bottom, copper, zinc, brine-soaked cloth, and again, twelve times
    for i in range(cells):
        y = base - i * ch
        d.line((px - pw, y), (px + pw, y), (px + pw, y - 5), (px - pw, y - 5), closed=True)          # copper
        d.line((px - pw, y - 5), (px + pw, y - 5), (px + pw, y - 10), (px - pw, y - 10), closed=True)  # zinc
    d.lines([[(px - pw - 6, base + 2), (px + pw + 6, base + 2)], [(px - pw - 6, base + 2), (px - pw - 6, 262)],
             [(px + pw + 6, base + 2), (px + pw + 6, 262)]])
    # the stand of glass and the platinum disc on it
    d.ellipse(cx, dy_, drx, 9)
    d.line((cx - drx, dy_), (cx - drx, dy_ + 4))
    d.line((cx + drx, dy_), (cx + drx, dy_ + 4))
    d.arc(cx, dy_ + 4, drx, 0, 180, n=40, ry=9)
    d.line((cx - 6, dy_ + 13), (cx - 6, 262))
    d.line((cx + 6, dy_ + 13), (cx + 6, 262))
    d.line((cx - 30, 262), (cx - 20, 252), (cx + 20, 252), (cx + 30, 262))
    # the lump of potash, fusing where the current enters it
    lump = [(cx - 34, dy_ - 2), (cx - 38, dy_ - 22), (cx - 24, dy_ - 44), (cx - 4, dy_ - 52), (cx + 18, dy_ - 46),
            (cx + 34, dy_ - 30), (cx + 36, dy_ - 6), (cx + 28, dy_)]
    d.line(*lump)
    # the leads: positive from the top of the pile to a wire touching the lump; negative from the bottom to the disc
    d.line((px, top - 10), (px, wire_y - 22), (cx, wire_y - 22), (cx, dy_ - 52))
    d.line((px + pw, base - 2), (330, base - 2), (330, dy_), (cx + drx, dy_))
    d.group('mid')
    # the cloth between the pairs, hatched
    hatch = []
    for i in range(cells - 1):
        y = base - i * ch - 10
        for k in range(6):
            x = px - pw + 4 + k * 10
            hatch.append([(x, y), (x + 4, y - 5)])
    d.lines(hatch)
    # oxygen fizzing off at the wire; globules of potassium at the disc
    for x, y, rr in ((cx - 6, dy_ - 58, 2.2), (cx + 7, dy_ - 62, 1.8), (cx - 2, dy_ - 70, 1.6), (cx + 4, dy_ - 76, 1.4)):
        d.circle(x, y, rr)
    for x, rr in ((-22, 3.2), (-9, 2.4), (5, 3.6), (19, 2.6)):
        d.circle(cx + x, dy_ - 6, rr)
    d.group('mid')
    d.text(px - pw - 10, top - 2, '+', size=11, anchor='end')
    d.text(px - pw - 10, base + 2, '−', size=11, anchor='end')
    d.text(cx + 44, dy_ - 36, 'POTASH', size=8, anchor='start')
    d.text(cx - drx - 8, dy_ + 3, 'PLATINUM', size=8, anchor='end')
    d.text(cx - 10, 118, '4 OH⁻ → O₂ + 2 H₂O + 4 e⁻', size=8, anchor='end')
    d.text(cx, 284, 'K⁺ + e⁻ → K', size=9)
    return d


PLATES = {'oxygen': oxygen, 'lavoisier': lavoisier, 'davy-electrolysis': davy_electrolysis}
