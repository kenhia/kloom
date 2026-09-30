"""physics plates, segment "Light and motion" and the opening of "The new science" (sprint 021). See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _candle(d, x, base, h=34, w=7):
    """A candle standing on `base`, with its flame; returns the flame's centre."""
    d.line((x - w / 2, base), (x - w / 2, base - h), (x + w / 2, base - h), (x + w / 2, base), closed=True)
    d.line((x, base - h), (x, base - h - 3))
    fy = base - h - 9
    d.path(f'M{x:.1f} {base - h - 1:.1f} C{x - 6:.1f} {base - h - 5:.1f} {x - 3:.1f} {fy - 6:.1f} {x:.1f} {fy - 10:.1f} '
           f'C{x + 3:.1f} {fy - 6:.1f} {x + 6:.1f} {base - h - 5:.1f} {x:.1f} {base - h - 1:.1f}')
    return (x, fy)


def ibn_al_haytham():
    """Ibn al-Haytham's candles before a dark chamber (Book of Optics I).

    Three candles stand before a small aperture; each throws its own spot on
    the far wall, on the straight line from its flame through the aperture, so
    the spots come out in reverse order. A board shields the third candle, and
    only its spot is missing: light and colour do not mingle in the air."""
    d = D()
    ap = (205, 150)                          # the aperture in the front wall
    wall_x, back_x, top, bot = 205, 360, 62, 238
    candles = [(52, 118), (88, 176), (40, 236)]   # (x, base): three candles at different places
    flames = []
    # construction: the room's floor line and the straight lines through the aperture
    d.group('thin')
    d.line((20, 250), (380, 250))
    guides = []
    for x, base in candles:
        fx, fy = x, base - 34 - 9
        flames.append((fx, fy))
        # the line from the flame through the aperture to the back wall
        t = (back_x - fx) / (ap[0] - fx)
        guides.append((back_x, fy + t * (ap[1] - fy)))
    d.lines([[f, g] for f, g in zip(flames[:2], guides[:2])])
    # the dark chamber: front wall with its aperture, back wall, roof and floor
    d.group()
    d.line((wall_x, top), (wall_x, ap[1] - 4))
    d.line((wall_x, ap[1] + 4), (wall_x, bot))
    d.line((wall_x + 6, top), (wall_x + 6, ap[1] - 4))
    d.line((wall_x + 6, ap[1] + 4), (wall_x + 6, bot))
    d.line((wall_x, top), (back_x + 6, top), (back_x + 6, bot), (wall_x, bot))
    d.line((back_x, top + 6), (back_x, bot - 6))
    for x, base in candles:
        _candle(d, x, base)
    # the board that shields the third candle
    sx = 118
    t = (sx - flames[2][0]) / (ap[0] - flames[2][0])
    sy = flames[2][1] + t * (ap[1] - flames[2][1])
    d.line((sx, sy - 16), (sx, sy + 16), (sx + 4, sy + 16), (sx + 4, sy - 16), closed=True)
    # the light that gets through: two rays, and their spots on the back wall
    d.group('mid')
    for f, g in zip(flames[:2], guides[:2]):
        d.line(f, ap, g)
        _arrow(d, *g, math.atan2(g[1] - ap[1], g[0] - ap[0]), 5)
        d.lines([[(g[0] - 2, g[1] + k), (g[0] - 7, g[1] + k * 1.6)] for k in (-7, 0, 7)])
    d.line(flames[2], (sx, sy))
    # where the shielded candle's light would have gone, and the missing spot
    d.group('thin')
    g = guides[2]
    d.line((sx + 4, sy + 4 * (ap[1] - flames[2][1]) / (ap[0] - flames[2][0])), ap, g)
    d.circle(g[0] - 5, g[1], 4)
    # labels
    d.group()
    d.text(wall_x - 8, ap[1] - 10, 'APERTURE', size=7, anchor='end')
    d.text((wall_x + back_x) / 2 + 3, top - 8, 'DARK CHAMBER', size=7)
    d.text(sx + 2, sy + 28, 'SHIELDED', size=7)
    d.text(back_x - 12, g[1] + 3, 'NO SPOT', size=7, anchor='end')
    d.text(200, 290, 'LIGHT AND COLOUR DO NOT MINGLE IN THE AIR', size=8)
    return d


def merton_calculators():
    """Oresme's figure for the Merton rule: a uniformly difform motion from rest.

    Time runs along the base (the longitude), speed stands up from it (the
    latitude), so a speed that grows uniformly from nothing is a right triangle
    and the distance run is its area. The rectangle at the middle degree has
    the same area: the corner of the triangle above it fills the gap below,
    turned about the middle point. The two halves of the time hold one part
    and three parts of the distance."""
    d = D()
    x0, x1, yb, yt = 60, 330, 240, 60      # base from x0 to x1; the final speed reaches yt
    xm, ym = (x0 + x1) / 2, (yb + yt) / 2   # the middle instant and the middle degree
    speed = lambda x: yb - (yb - yt) * (x - x0) / (x1 - x0)
    # construction: the base's divisions and the middle instant
    d.group('thin')
    d.lines([[(x0 + (x1 - x0) * k / 8, yb), (x0 + (x1 - x0) * k / 8, yb + 5)] for k in range(9)])
    d.line((xm, yb + 12), (xm, yt - 14))
    d.line((x0, yt - 14), (x0, yb))
    # the latitudes: the speed at each instant, stood up on the base, as Oresme drew them
    d.group('mid')
    step = (x1 - x0) / 16
    d.lines([[(x0 + step * k, yb), (x0 + step * k, speed(x0 + step * k))] for k in range(1, 16)])
    # the figure: the triangle of the motion, and the rectangle at the middle degree
    d.group()
    d.line((x0, yb), (x1, yb), (x1, yt), closed=True)
    d.group('thin')
    d.line((x0, ym), (x1, ym))
    # the corner above the middle degree swings about the middle point into the gap below
    d.group('mid')
    r = 30
    d.arc(xm, ym, r, -30, -205, n=40)
    a = math.radians(-205)
    _arrow(d, xm + r * math.cos(a), ym + r * math.sin(a), a - math.pi / 2, 4.5)
    d.circle(xm, ym, 2.5)
    # labels
    d.group()
    d.text(x0 + (xm - x0) * 0.62, yb - 10, '1', size=11)
    d.text(xm + (x1 - xm) * 0.5, yb - 26, '3', size=11)
    d.text(x0 + 6, ym - 6, 'MIDDLE DEGREE', size=7, anchor='start')
    d.text(x0, yt - 20, 'SPEED', size=7)
    d.text(x1 + 6, yt + 4, 'FINAL', size=7, anchor='start')
    d.text(xm, yb + 22, 'TIME · FIRST HALF | SECOND HALF', size=7)
    d.text(200, 290, 'UNIFORMLY DIFFORM MOTION · AREA IS DISTANCE', size=8)
    return d


def copernicus():
    """Why Mars runs backwards, in Copernicus's arrangement.

    The planets' circles about the Sun, in Copernicus's order (Mercury, Venus,
    the Earth, Mars, Jupiter, Saturn; the Earth and Mars in their true ratio,
    the outer two only in order). Nine sight lines, twenty days apart, run from
    the Earth through Mars to the stars: as the faster Earth overtakes Mars,
    the line of sight swings back, and Mars seems to reverse."""
    d = D()
    sx, sy = 86, 150                        # the Sun
    RE, RM = 24, 24 * 1.524                  # the Earth's and Mars's circles, in true ratio
    others = [(9, 'MERCURY'), (17, 'VENUS'), (58, 'JUPITER'), (76, 'SATURN')]
    sky = 368                                # the stars, far off, drawn as a line
    days = list(range(-80, 81, 20))
    E, M, S = [], [], []
    for t in days:
        a = -2 * math.pi * t / 365.25
        b = -2 * math.pi * t / 686.98
        e = (sx + RE * math.cos(a), sy + RE * math.sin(a))
        m = (sx + RM * math.cos(b), sy + RM * math.sin(b))
        k = (sky - e[0]) / (m[0] - e[0])
        E.append(e); M.append(m); S.append((sky, e[1] + k * (m[1] - e[1])))
    # construction: the sight lines from the Earth through Mars to the stars
    d.group('thin')
    d.lines([[e, s] for e, s in zip(E, S)])
    # the circles about the Sun
    d.group()
    for r, _ in others[:2]:
        d.circle(sx, sy, r)
    d.circle(sx, sy, RE)
    d.circle(sx, sy, RM)
    for r, _ in others[2:]:
        d.circle(sx, sy, r)
    d.circle(sx, sy, 3.5)
    d.line((sky, 70), (sky, 230))
    # the positions: the Earth and Mars at each date, and where Mars appears among the stars
    d.group('mid')
    for e, m, s in zip(E, M, S):
        d.circle(*e, 1.6)
        d.circle(*m, 1.6)
        d.line((s[0] - 4, s[1]), (s[0] + 4, s[1]))
    # the apparent motion beside the star line: forward, back, forward
    ys = [s[1] for s in S]
    lo, hi = min(ys[:5]), max(ys[4:])
    d.line((sky + 12, ys[0]), (sky + 12, lo))
    _arrow(d, sky + 12, lo, -math.pi / 2, 4)
    d.line((sky + 20, lo), (sky + 20, hi))
    _arrow(d, sky + 20, hi, math.pi / 2, 4)
    d.line((sky + 28, hi), (sky + 28, ys[-1]))
    _arrow(d, sky + 28, ys[-1], -math.pi / 2, 4)
    # labels
    d.group()
    d.text(sx, sy + 13, 'SUN', size=6)
    d.text(E[0][0] - 2, E[0][1] + 10, 'EARTH', size=6)
    d.text(M[-1][0] + 2, M[-1][1] - 5, 'MARS', size=6, anchor='start')
    d.text(sx, sy - others[3][0] - 5, 'SATURN', size=6)
    d.text(sky, 62, 'THE STARS', size=7)
    d.text(sky - 8, S[4][1] + 3, '5', size=7, anchor='end')
    d.text(sky - 8, ys[0] + 3, '1', size=7, anchor='end')
    d.text(sky - 8, ys[-1] + 3, '9', size=7, anchor='end')
    d.text(200, 290, 'MARS SEEN FROM A MOVING EARTH · 20 DAYS APART', size=8)
    return d


PLATES = {'ibn-al-haytham': ibn_al_haytham, 'merton-calculators': merton_calculators, 'copernicus': copernicus}
