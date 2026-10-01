"""Plates for How We Build's second segment, Clay and glass (sprint 026, part clay-glass)."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _spin_arrow(d, cx, cy, rx, ry, a0, a1, n=30):
    """An arc of an ellipse (a disc seen in perspective) with an arrowhead at its end."""
    d.arc(cx, cy, rx, a0, a1, n=n, ry=ry)
    ex, ey = cx + rx * math.cos(math.radians(a1)), cy + ry * math.sin(math.radians(a1))
    # the tangent at the end, in screen space
    tx, ty = -rx * math.sin(math.radians(a1)), ry * math.cos(math.radians(a1))
    k = math.hypot(tx, ty)
    tx, ty = tx / k * (1 if a1 > a0 else -1), ty / k * (1 if a1 > a0 else -1)
    nx, ny = -ty, tx
    d.lines([[(ex - tx * 7 + nx * 3.5, ey - ty * 7 + ny * 3.5), (ex, ey), (ex - tx * 7 - nx * 3.5, ey - ty * 7 - ny * 3.5)]])


def potters_wheel():
    """A kick wheel in elevation, and the clay in section at the three stages of throwing."""
    d = D()
    ax = 96                                   # the wheel's axis
    head_y, fly_y = 92, 236                   # wheelhead and flywheel levels
    rh, rf, persp = 50, 72, 0.22              # radii and the ellipse ratio of a disc seen from above
    d.group('thin')
    d.line((ax, 30), (ax, 274))                                        # the axis of rotation
    d.line((14, 262), (190, 262))                                      # the floor
    # dimension of the flywheel's radius, and the radius at which a kick lands
    d.line((ax, fly_y + 24), (ax + rf, fly_y + 24))
    d.lines([[(ax, fly_y + 20), (ax, fly_y + 28)], [(ax + rf, fly_y + 20), (ax + rf, fly_y + 28)]])
    # the three section stations on the right, each on its own axis
    stations = (238, 296, 356)
    for sx in stations:
        d.line((sx, 40), (sx, 168))
    d.line((210, 150), (390, 150))                                     # the wheelhead in section, across all three
    d.group()
    # the wheelhead: a disc seen slightly from above, with its thickness
    d.ellipse(ax, head_y, rh, rh * persp)
    d.line((ax - rh, head_y), (ax - rh, head_y + 7))
    d.line((ax + rh, head_y), (ax + rh, head_y + 7))
    d.arc(ax, head_y + 7, rh, 0, 180, n=30, ry=rh * persp)
    # the shaft
    d.line((ax - 4, head_y + 7 + rh * persp), (ax - 4, fly_y - rf * persp))
    d.line((ax + 4, head_y + 7 + rh * persp), (ax + 4, fly_y - rf * persp))
    # the flywheel: a heavier, thicker disc
    d.ellipse(ax, fly_y, rf, rf * persp)
    d.line((ax - rf, fly_y), (ax - rf, fly_y + 14))
    d.line((ax + rf, fly_y), (ax + rf, fly_y + 14))
    d.arc(ax, fly_y + 14, rf, 0, 180, n=36, ry=rf * persp)
    d.line((ax - 6, fly_y + 14 + rf * persp), (ax - 6, 262), (ax + 6, 262), (ax + 6, fly_y + 14 + rf * persp))
    # the clay in section at three stages: centred, opened, pulled up
    base = 150
    # 1. centred: a low dome, symmetric about its axis
    sx = stations[0]
    dome = [(sx + 22 * math.cos(math.radians(a)), base - 30 * math.sin(math.radians(a)) ** 0.8) for a in range(0, 181, 6)]
    d.line(*dome)
    # 2. opened: a thick ring with a floor, the hole made by the thumbs
    sx = stations[1]
    d.line((sx - 24, base), (sx - 24, base - 30), (sx - 20, base - 34), (sx - 10, base - 32), (sx - 9, base - 9),
           (sx + 9, base - 9), (sx + 10, base - 32), (sx + 20, base - 34), (sx + 24, base - 30), (sx + 24, base))
    # 3. pulled: a tall thin cylinder, the same volume drawn upward
    sx = stations[2]
    d.line((sx - 19, base), (sx - 19, base - 96), (sx - 15, base - 98), (sx - 13, base - 96), (sx - 13, base - 7),
           (sx + 13, base - 7), (sx + 13, base - 96), (sx + 15, base - 98), (sx + 19, base - 96), (sx + 19, base))
    d.group('mid')
    # the spin of the wheelhead and the kick at the flywheel's rim
    _spin_arrow(d, ax, head_y, rh + 12, (rh + 12) * persp, 20, 160)
    _spin_arrow(d, ax, fly_y, rf + 10, (rf + 10) * persp, 30, 120)
    # the potter's pressure at each stage: arrows towards the clay
    sx = stations[0]
    d.lines([[(sx - 40, base - 14), (sx - 26, base - 14)], [(sx - 30, base - 18), (sx - 26, base - 14), (sx - 30, base - 10)]])
    d.lines([[(sx, base - 52), (sx, base - 36)], [(sx - 4, base - 40), (sx, base - 36), (sx + 4, base - 40)]])
    sx = stations[1]
    d.lines([[(sx, base - 52), (sx, base - 16)], [(sx - 4, base - 20), (sx, base - 16), (sx + 4, base - 20)]])
    sx = stations[2]
    # fingers inside and outside the wall, moving up together
    for side in (-1, 1):
        x_in, x_out = sx + side * 10, sx + side * 23
        d.lines([[(x_in, base - 40), (x_in, base - 70)], [(x_in - 3, base - 66), (x_in, base - 70), (x_in + 3, base - 66)]])
        d.lines([[(x_out, base - 40), (x_out, base - 70)], [(x_out - 3, base - 66), (x_out, base - 70), (x_out + 3, base - 66)]])
    # the rilling a thrown pot keeps: faint rings inside the pulled wall
    d.lines([[(sx - 12, base - 20 - 14 * k), (sx + 12, base - 20 - 14 * k)] for k in range(5)])
    d.group('mid')
    d.text(stations[0], 186, 'CENTRE', size=8)
    d.text(stations[1], 186, 'OPEN', size=8)
    d.text(stations[2], 186, 'PULL', size=8)
    d.text(ax + rf / 2, fly_y + 38, 'r', size=9)
    d.text(ax + rh + 18, head_y - 14, 'ω', size=10, anchor='start')
    d.text(300, 226, 'E = ½ I ω²', size=9)
    d.text(300, 244, 'I ∝ m r²', size=9)
    d.text(ax, 20, 'KICK WHEEL', size=8)
    return d


PLATES = {'potters-wheel': potters_wheel}


def glassblowing():
    """The gather blown on the pipe, in three stages, and the annealing curve below."""
    d = D()
    py = 66                                    # the blowpipe's line
    d.group('thin')
    d.line((14, py), (392, py))                                        # the pipe's axis produced
    # the annealing plot's axes
    ox, oy, pw, ph = 52, 270, 320, 118         # origin, width, height
    d.line((ox, oy), (ox + pw, oy))
    d.line((ox, oy), (ox, oy - ph))
    # temperature levels: working heat, annealing point, strain point (schematic, not to scale below 1000)
    tmax = 1100
    def ty(t):
        return oy - ph * t / tmax
    for t in (1000, 545, 500):
        d.line((ox, ty(t)), (ox + pw, ty(t)))
    d.group()
    # three stations along the pipe: gather, marvered, blown
    for k, x0 in enumerate((24, 140, 256)):
        # the pipe: two lines, ending in the nose
        d.line((x0, py - 2.5), (x0 + 54, py - 2.5))
        d.line((x0, py + 2.5), (x0 + 54, py + 2.5))
        cx = x0 + 54
        if k == 0:
            # the gather: a lump of honey-like glass round the nose, sagging a little
            pts = [(cx + 6 + 20 * math.cos(math.radians(a)), py + 3 + 17 * math.sin(math.radians(a))) for a in range(-160, 161, 8)]
            d.line(*pts)
        elif k == 1:
            # marvered: rolled into a cylinder with a rounded end, a small bubble begun inside
            d.line((cx, py - 14), (cx + 32, py - 14))
            d.line((cx, py + 14), (cx + 32, py + 14))
            d.arc(cx + 32, py, 14, -90, 90, n=20)
            d.line((cx, py - 14), (cx, py + 14))
            d.ellipse(cx + 16, py, 8, 4)
        else:
            # blown: a thin-walled bubble, the paraison, with its air space
            r = 34
            d.arc(cx + r, py, r, -160, 160, n=48)
            d.arc(cx + r, py, r - 3, -155, 155, n=48)
            d.line((cx, py - 2.5), (cx + r * (1 + math.cos(math.radians(160))), py + r * math.sin(math.radians(-160))))
            d.line((cx, py + 2.5), (cx + r * (1 + math.cos(math.radians(160))), py + r * math.sin(math.radians(160))))
    # the annealing curve: worked hot, into the lehr, held at the annealing point, cooled slowly past the strain point, then faster
    sched = [(0, 1000), (0.10, 1000), (0.17, 545), (0.40, 545), (0.62, 500), (1.0, 40)]
    pts = []
    for (u0, t0), (u1, t1) in zip(sched, sched[1:]):
        for i in range(12):
            u = u0 + (u1 - u0) * i / 12
            t = t0 + (t1 - t0) * i / 12
            if (u0, t0) == (0.62, 500):        # the last cooling falls away like an exponential
                s = i / 12
                t = 40 + 460 * math.exp(-3.2 * s)
            pts.append((ox + pw * u, ty(t)))
    pts.append((ox + pw, ty(40 + 460 * math.exp(-3.2))))
    d.line(*pts)
    d.group('mid')
    # breath: arrows along the pipe into each bubble
    for x0 in (140, 256):
        d.lines([[(x0 + 6, py), (x0 + 30, py)], [(x0 + 25, py - 4), (x0 + 30, py), (x0 + 25, py + 4)]])
    # the turning of the pipe, which keeps the glass from sagging
    for x0 in (24, 140, 256):
        d.arc(x0 + 12, py, 9, -60, 240, n=20, ry=5)
    # the marver under the second station
    d.line((178, py + 22), (240, py + 22))
    d.lines([[(178 + 6 * k, py + 22), (174 + 6 * k, py + 28)] for k in range(11)])
    d.group('mid')
    d.text(84, 30, 'GATHER', size=8)
    d.text(200, 30, 'MARVER', size=8)
    d.text(344, 20, 'BLOW', size=8)
    d.text(ox - 4, ty(1000) + 3, '1000', size=7, anchor='end')
    d.text(ox + pw, ty(545) - 4, 'ANNEALING POINT', size=7, anchor='end')
    d.text(ox + pw, ty(500) + 10, 'STRAIN POINT', size=7, anchor='end')
    d.text(ox + pw / 2, oy + 14, 'TIME IN THE LEHR →', size=7)
    d.text(ox - 4, oy - ph - 6, '°C', size=7, anchor='end')
    return d


PLATES['glassblowing'] = glassblowing


def float_glass():
    """The float line in long section, and the pool of glass on tin in cross-section."""
    d = D()
    ty0 = 112                                  # the tin's surface
    d.group('thin')
    # the long section: temperature stations along the bath
    xs = {'furnace': 18, 'spout': 96, 'bath0': 104, 'bath1': 330, 'lehr': 396}
    for x, t in ((112, '1050'), (322, '600')):
        d.line((x, 40), (x, ty0 + 30))
    d.line((14, ty0), (392, ty0))
    # the cross-section's construction: the equilibrium thickness and the tin level
    cy = 232                                   # tin level in the cross-section
    d.line((40, cy), (360, cy))
    d.line((200, cy - 40), (200, cy + 40))
    d.group()
    # the furnace: a melting tank with its crown
    d.line((xs['furnace'], ty0 - 30), (xs['furnace'], ty0 + 26), (88, ty0 + 26), (88, ty0 - 4))
    d.arc(53, ty0 - 30, 35, 180, 360, n=24, ry=18)
    d.line((88, ty0 - 30), (88, ty0 - 16))
    # the molten glass in the tank, and the stream over the spout lip onto the tin
    d.line((xs['furnace'], ty0 - 4), (92, ty0 - 4), (100, ty0 - 2), (104, ty0 - 4))
    # the bath: a long shallow tank of tin, roofed, with the ribbon on it
    d.line((104, ty0 - 34), (330, ty0 - 34))                          # the roof, holding the atmosphere
    d.line((104, ty0 - 34), (104, ty0 + 20), (330, ty0 + 20), (330, ty0 - 34))
    # the ribbon: thick where it lands, spreading to its equilibrium thickness, then a constant sheet
    top = []
    for i in range(60):
        x = 104 + (330 - 104) * i / 59
        u = (x - 104) / 60.0
        h = 3.2 + 7 * math.exp(-u * 3)                                  # height above the tin, in px
        top.append((x, ty0 - h * 0.64))
    d.line(*top)
    # the lehr: the ribbon leaves on rollers into a long cooling tunnel
    d.line((330, ty0 - 2), (396, ty0 - 2))
    d.line((340, ty0 - 24), (396, ty0 - 24))
    for x in range(338, 396, 12):
        d.circle(x, ty0 + 2, 3)
    # the cross-section: a pool of glass floating on tin, flat on top, its edges rounded
    T = 30                                     # the drawn equilibrium thickness, px
    sub = T * 2.4 / 6.5                        # the part below the tin level, by density (glass ~2.4, tin 6.5 g/cm³)
    left, right = 92, 308
    # build the pool outline explicitly: top flat, rounded ends meeting the tin line at a contact angle
    outline = [(left - 10, cy)]
    outline += [(left - 10 + 10 * (1 - math.cos(math.radians(a))), cy - (T - sub) * math.sin(math.radians(a))) for a in range(0, 91, 10)]
    outline += [(right + 10 - 10 * (1 - math.cos(math.radians(a))), cy - (T - sub) * math.sin(math.radians(a))) for a in range(90, -1, -10)]
    outline += [(right + 10 - 14 * (1 - math.cos(math.radians(a))), cy + sub * math.sin(math.radians(a))) for a in range(0, 91, 10)]
    outline += [(left - 10 + 14 * (1 - math.cos(math.radians(a))), cy + sub * math.sin(math.radians(a))) for a in range(90, -1, -10)]
    d.line(*outline, closed=True)
    d.line((40, cy), (left - 10, cy))
    d.line((right + 10, cy), (360, cy))
    d.group('mid')
    # the dimension of T, at the centre
    d.line((200, cy - (T - sub)), (200, cy + sub))
    d.lines([[(196, cy - (T - sub)), (204, cy - (T - sub))], [(196, cy + sub), (204, cy + sub)]])
    # the tin below, hatched
    d.lines([[(60 + 14 * k, cy + 26), (52 + 14 * k, cy + 36)] for k in range(22)])
    d.lines([[(110 + 12 * k, ty0 + 10), (104 + 12 * k, ty0 + 18)] for k in range(19)])
    # the travel of the ribbon
    d.lines([[(200, ty0 - 46), (250, ty0 - 46)], [(244, ty0 - 50), (250, ty0 - 46), (244, ty0 - 42)]])
    d.group('mid')
    for x, t in ((112, '1050'), (322, '600')):
        d.text(x, 34, t + ' °C', size=7)
    d.text(53, ty0 + 40, 'FURNACE', size=7)
    d.text(217, ty0 + 34, 'MOLTEN TIN', size=7)
    d.text(368, ty0 + 18, 'LEHR', size=7)
    d.text(208, cy - 2, 'T', size=9, anchor='start')
    d.text(214, cy - T + 4, 'Sg', size=8, anchor='start')
    d.text(370, cy + 4, 'St', size=8, anchor='start')
    d.text(214, cy + sub + 2, 'Sgt', size=8, anchor='start')
    d.text(128, cy - T + 4, 'GLASS', size=7)
    d.text(200, 292, 'T² = (Sg + Sgt − St) · 2ρt ÷ gρg(ρt − ρg)', size=8)
    return d


PLATES['float-glass'] = float_glass
