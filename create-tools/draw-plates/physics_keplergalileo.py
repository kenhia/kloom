"""physics plates, part "keplergalileo": Kepler and Galileo (sprint 021). See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _kepler_E(M, e):
    """Solve Kepler's equation M = E - e sin E for the eccentric anomaly E."""
    E = M
    for _ in range(30):
        E -= (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    return E


def kepler():
    """Mars's orbit as Kepler found it: an ellipse of eccentricity 0.093 with the Sun at one focus.

    The auxiliary circle and the empty focus are construction; two sectors
    swept in equal times (a twelfth of Mars's year each), one about
    perihelion and one about aphelion, have equal areas; ticks on the orbit
    mark twelve equal intervals of time, closer together near aphelion."""
    d = D()
    a, e = 118, 0.0934
    b = a * math.sqrt(1 - e * e)
    cx, cy = 200, 150
    c = a * e
    sun = (cx + c, cy)            # perihelion to the right
    empty = (cx - c, cy)

    def pos(M):
        E = _kepler_E(M, e)
        return (cx + a * math.cos(E), cy - b * math.sin(E))

    # construction: the major and minor axes, the auxiliary circle, the empty focus
    d.group('thin')
    d.line((cx - a - 14, cy), (cx + a + 14, cy))
    d.line((cx, cy - a - 8), (cx, cy + a + 8))
    d.circle(cx, cy, a)
    d.lines([[(empty[0] - 3, empty[1] - 3), (empty[0] + 3, empty[1] + 3)],
             [(empty[0] - 3, empty[1] + 3), (empty[0] + 3, empty[1] - 3)]])
    # the orbit
    d.group()
    d.line(*[pos(2 * math.pi * k / 240) for k in range(241)], closed=True)
    # two equal-time sectors, each a twelfth of the year
    d.group('mid')
    w = 2 * math.pi / 12
    for M0 in (0.0, math.pi):
        arc = [pos(M0 - w / 2 + w * k / 24) for k in range(25)]
        d.line(sun, *arc, closed=True)
    # ticks at twelve equal times round the orbit
    ticks = []
    for k in range(12):
        M = 2 * math.pi * (k + 0.5) / 12
        x, y = pos(M)
        ux, uy = x - cx, y - cy
        n = math.hypot(ux / a ** 2, uy / b ** 2)
        nx, ny = ux / a ** 2 / n, uy / b ** 2 / n
        ticks.append([(x - 4 * nx, y - 4 * ny), (x + 4 * nx, y + 4 * ny)])
    d.lines(ticks)
    # the Sun and the planet
    d.group()
    d.circle(sun[0], sun[1], 5)
    d.lines([[(sun[0] + 7 * math.cos(t), sun[1] + 7 * math.sin(t)),
              (sun[0] + 10 * math.cos(t), sun[1] + 10 * math.sin(t))]
             for t in [k * math.pi / 4 for k in range(8)]])
    mx, my = pos(2 * math.pi * 0.3)
    d.circle(mx, my, 3.5)
    # labels
    d.group()
    d.text(sun[0] + 6, sun[1] + 20, 'SUN', size=7, anchor='start')
    d.text(empty[0] - 4, empty[1] + 14, 'EMPTY FOCUS', size=7, anchor='end')
    d.text(cx + a + 4, cy + 14, 'PERIHELION', size=7, anchor='start')
    d.text(cx - a - 4, cy + 14, 'APHELION', size=7, anchor='end')
    d.text(mx - 8, my - 6, 'MARS', size=7, anchor='end')
    d.text(200, 18, 'EQUAL AREAS IN EQUAL TIMES', size=8)
    d.text(200, 292, 'MARS · e 0.093 · SUN AT A FOCUS', size=8)
    return d


def _phase(d, x, y, r, alpha, toward):
    """A planet's disc as seen from the Earth, at phase angle `alpha`, lit on the side `toward` (+1 right, -1 left).

    The lit limb is a semicircle; the terminator a half-ellipse whose half-width
    is r cos(alpha), bulging towards the dark side while more than half is lit."""
    lim = [(x + toward * r * math.sin(t), y - r * math.cos(t)) for t in [math.pi * k / 24 for k in range(25)]]
    k = math.cos(alpha)
    term = [(x - toward * r * k * math.sin(t), y + r * math.cos(t)) for t in [math.pi * j / 24 for j in range(25)]]
    d.line(*lim, *term[1:], closed=True)


def galileo_telescope():
    """The phases of Venus, which Galileo saw in 1610: Venus on its orbit round the Sun, and its disc as the Earth sees it.

    Far beyond the Sun, Venus is small and nearly full; near the Earth it is
    large and a thin crescent. Each disc is drawn at a size inversely as
    Venus's distance, with the lit part its phase angle gives. In Ptolemy's
    arrangement Venus stays between the Earth and the Sun and could never
    show the full, small discs."""
    d = D()
    au = 96
    sx, sy = 200, 168
    rv = 0.7233 * au
    ex, ey = sx, sy + au              # the Earth, below the Sun
    thetas = [25, 70, 106, 145, 165]    # Venus's angle round the Sun from superior conjunction, east of the Sun
    # construction: Venus's orbit, the Earth–Sun line, and sight lines from the Earth
    d.group('thin')
    d.circle(sx, sy, rv)
    d.line((ex, ey), (sx, sy - rv - 12))
    venus = []
    for th in thetas:
        t = math.radians(th)
        vx, vy = sx + rv * math.sin(t), sy - rv * math.cos(t)
        venus.append((vx, vy))
    d.lines([[(ex, ey), v] for v in venus])
    # the Sun and the Earth
    d.group()
    d.circle(sx, sy, 7)
    d.lines([[(sx + 9 * math.cos(t), sy + 9 * math.sin(t)), (sx + 13 * math.cos(t), sy + 13 * math.sin(t))]
             for t in [k * math.pi / 4 for k in range(8)]])
    d.circle(ex, ey, 4.5)
    # Venus at each place on its orbit: a small disc lit on the Sun's side
    d.group('mid')
    for vx, vy in venus:
        d.circle(vx, vy, 3.2)
        ang = math.atan2(sy - vy, sx - vx)
        d.line((vx + 3.2 * math.cos(ang + math.pi / 2), vy + 3.2 * math.sin(ang + math.pi / 2)),
               (vx + 3.2 * math.cos(ang - math.pi / 2), vy + 3.2 * math.sin(ang - math.pi / 2)))
    # the discs as seen from the Earth, in a row, sized as 1 / distance
    d.group()
    xs = [40, 92, 150, 222, 318]
    for i, ((vx, vy), x) in enumerate(zip(venus, xs)):
        dist = math.hypot(vx - ex, vy - ey) / au
        r = 6.5 / dist
        a1 = math.atan2(sy - vy, sx - vx)
        a2 = math.atan2(ey - vy, ex - vx)
        alpha = abs((a1 - a2 + math.pi) % (2 * math.pi) - math.pi)
        _phase(d, x, 36, r, alpha, -1)   # east of the Sun, lit on the side towards it (west, left)
    d.group('thin')
    for i, x in enumerate(xs):
        d.line((x, 62), (x, 68))
    # labels
    d.group()
    for i, (x, (vx, vy)) in enumerate(zip(xs, venus)):
        d.text(x, 78, str(i + 1), size=7)
        d.text(vx + 9, vy + 3, str(i + 1), size=7, anchor='start')
    d.text(sx - 16, sy + 3, 'SUN', size=7, anchor='end')
    d.text(ex - 9, ey + 3, 'EARTH', size=7, anchor='end')
    d.text(200, 292, 'VENUS AS THE EARTH SEES IT · SIZE AS 1 ÷ DISTANCE', size=8)
    return d


def falling_bodies():
    """Galileo's two laws of fall, as Two New Sciences sets them out.

    Down the inclined plane, a ball released from rest covers distances of
    1, 4, 9 and 16 units in equal times, so the spaces in successive times
    go as the odd numbers 1, 3, 5, 7. Off the edge of the table it keeps its
    even horizontal speed while it falls by the same squares, and the path
    is a semi-parabola."""
    d = D()
    top, foot = (28, 44), (168, 132)
    L = math.hypot(foot[0] - top[0], foot[1] - top[1])
    ux, uy = (foot[0] - top[0]) / L, (foot[1] - top[1]) / L
    k = L / 16.5
    edge = (236, 132)
    ground = 282
    step, g = 30, 9.0
    # construction: the ground, the table's legs, the drop grid for the semi-parabola
    d.group('thin')
    d.line((14, ground), (392, ground))
    xs = [edge[0] + step * i for i in range(1, 5)]
    ys = [edge[1] + g * i * i for i in range(1, 5)]
    d.lines([[(x, edge[1]), (x, ground)] for x in xs])
    d.lines([[(edge[0], y), (xs[-1] + 8, y)] for y in ys])
    d.line(edge, (xs[-1] + 8, edge[1]))
    # the ramp, the table and the ball's two paths
    d.group()
    d.line(top, foot, (foot[0], ground), (top[0], ground), closed=True)
    d.line(foot, edge)
    d.line((edge[0], edge[1]), (edge[0], ground))
    d.line(*[(edge[0] + step * t, edge[1] + g * t * t) for t in [j / 10 for j in range(0, 51)] if edge[1] + g * t * t <= ground])
    # the ball at equal times: down the ramp (1, 4, 9, 16) and off the table
    d.group('mid')
    for n in (0, 1, 4, 9, 16):
        px, py = top[0] + ux * k * n, top[1] + uy * k * n
        d.circle(px + 4.2 * uy, py - 4.2 * ux, 3.2)
    for x, y in zip(xs, ys):
        d.circle(x, y, 3.2)
    # tick marks across the ramp between the positions, for the odd-number spaces
    d.group('thin')
    d.lines([[(top[0] + ux * k * n - 7 * uy, top[1] + uy * k * n + 7 * ux),
              (top[0] + ux * k * n + 12 * uy, top[1] + uy * k * n - 12 * ux)] for n in (0, 1, 4, 9, 16)])
    # labels
    d.group()
    for a, b, lab in ((0, 1, '1'), (1, 4, '3'), (4, 9, '5'), (9, 16, '7')):
        m = (a + b) / 2
        d.text(top[0] + ux * k * m - 13 * uy, top[1] + uy * k * m + 13 * ux + 3, lab, size=8)
    for i, (x, y) in enumerate(zip(xs, ys)):
        d.text(xs[-1] + 14, y + 3, str((i + 1) ** 2), size=7, anchor='start')
    d.text(edge[0] + 2, edge[1] - 8, 'EVEN ACROSS', size=7, anchor='start')
    d.text(96, 162, 'SPACES 1 : 3 : 5 : 7', size=7)
    d.text(200, 20, 'SPACES AS THE SQUARES OF THE TIMES', size=8)
    return d


PLATES = {'kepler': kepler, 'galileo-telescope': galileo_telescope, 'falling-bodies': falling_bodies}
