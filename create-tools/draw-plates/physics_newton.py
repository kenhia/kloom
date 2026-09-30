"""physics plates, part "newton" (sprint 021): the prism, the Principia and Coulomb. See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _refract(v, n, n1, n2):
    """Refract unit direction v at a surface with unit normal n (pointing into medium 2), Snell's law."""
    cos_i = -(v[0] * n[0] + v[1] * n[1])
    if cos_i < 0:
        n = (-n[0], -n[1])
        cos_i = -cos_i
    r = n1 / n2
    k = 1 - r * r * (1 - cos_i * cos_i)
    c = r * cos_i - math.sqrt(k)
    return (r * v[0] + c * n[0], r * v[1] + c * n[1])


def _hit(p, v, a, b):
    """Where the ray p + t v meets the line through a and b."""
    ex, ey = b[0] - a[0], b[1] - a[1]
    den = v[0] * ey - v[1] * ex
    t = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / den
    return (p[0] + t * v[0], p[1] + t * v[1])


def prism():
    """Newton's first prism experiment of 1666, with his own numbers from the 1672 letter.

    A prism of 63° 12' set at minimum deviation for glass of index 31/20 turns a
    beam from the window hole through about 45°. Red (index 68/44) and violet
    (69/44) leave it about 2° 18' apart, so the Sun's round image is drawn out on
    the wall into a band five times as long as it is broad. The rays are traced
    by Snell's law; only the room is foreshortened."""
    d = D()
    A = math.radians(63 + 12 / 60)
    n_mean, n_red, n_violet = 31 / 20, 68 / 44, 69 / 44
    D_min = 2 * math.asin(n_mean * math.sin(A / 2)) - A
    # the prism, apex down, base horizontal at the top; the ray inside runs parallel to the base
    cx, cy, side = 150, 150, 92
    h = side * math.cos(A / 2)
    apex = (cx, cy + h * 0.55)
    left = (cx - side * math.sin(A / 2), apex[1] - h)
    right = (cx + side * math.sin(A / 2), apex[1] - h)
    # outward normals of the two faces (the base is up, so bending is upward)
    def unit(x, y):
        m = math.hypot(x, y)
        return (x / m, y / m)
    nl = unit(-(apex[1] - left[1]), apex[0] - left[0])      # left face, pointing out (left-down)
    if nl[0] > 0:
        nl = (-nl[0], -nl[1])
    nr = unit(apex[1] - right[1], -(apex[0] - right[0]))
    if nr[0] < 0:
        nr = (-nr[0], -nr[1])
    # the incoming beam: descending at D/2, meeting the left face at its middle
    vin = (math.cos(D_min / 2), math.sin(D_min / 2))
    entry = ((left[0] + apex[0]) / 2, (left[1] + apex[1]) / 2 - 6)
    entry = _hit((entry[0] - 200 * vin[0], entry[1] - 200 * vin[1]), vin, left, apex)
    shutter_x = 38
    t0 = (shutter_x - entry[0]) / vin[0]
    hole = (shutter_x, entry[1] + t0 * vin[1])
    wall_x = 372

    def trace(n):
        v1 = _refract(vin, (-nl[0], -nl[1]), 1, n)
        p1 = _hit(entry, v1, right, apex)
        v2 = _refract(v1, nr, n, 1)
        p2 = (wall_x, p1[1] + (wall_x - p1[0]) / v2[0] * v2[1])
        return p1, p2, v2
    pr1, pr2, vr = trace(n_red)
    pv1, pv2, vv = trace(n_violet)
    pm1, pm2, vm = trace(n_mean)
    # construction: the normals at the two faces, the undeviated line, the deviation arc
    d.group('thin')
    for p, n in ((entry, nl), (pm1, nr)):
        d.line((p[0] - 26 * n[0], p[1] - 26 * n[1]), (p[0] + 26 * n[0], p[1] + 26 * n[1]))
    far = (entry[0] + 190 * vin[0], entry[1] + 190 * vin[1])
    d.line(entry, far)
    d.line((cx, left[1] - 12), (cx, apex[1] + 12))
    r_arc = 150
    a0 = math.degrees(math.atan2(vin[1], vin[0]))
    a1 = math.degrees(math.atan2(vm[1], vm[0]))
    d.arc(pm1[0], pm1[1], r_arc, a1, a0 - 0.0, n=30)
    # the object: the shutter with its hole, the prism, the wall
    d.group()
    d.line((shutter_x, 16), (shutter_x, hole[1] - 3))
    d.line((shutter_x, hole[1] + 3), (shutter_x, 150))
    d.line(left, right, apex, closed=True)
    d.line((wall_x, 16), (wall_x, 196))
    # the light: the beam in, the path inside, and the fan of colours out to the wall
    d.group('mid')
    d.line(hole, entry)
    _arrow(d, (hole[0] + entry[0]) / 2, (hole[1] + entry[1]) / 2, math.atan2(vin[1], vin[0]))
    d.line(entry, pm1)
    d.line(pr1, pr2)
    d.line(pv1, pv2)
    d.lines([[(wall_x - 4, pr2[1]), (wall_x + 4, pr2[1])], [(wall_x - 4, pv2[1]), (wall_x + 4, pv2[1])]])
    # on the wall, seen face on: the band Newton measured against the circle he expected
    d.group()
    bx, by, L, B = 250, 256, 13.25, 2.625
    s = 9.2                                   # plate units per inch
    rr = B * s / 2
    x0, x1 = bx - (L - B) * s / 2, bx + (L - B) * s / 2
    d.path(f'M{x0:.1f} {by - rr:.1f} L{x1:.1f} {by - rr:.1f} A{rr:.1f} {rr:.1f} 0 0 1 {x1:.1f} {by + rr:.1f} '
           f'L{x0:.1f} {by + rr:.1f} A{rr:.1f} {rr:.1f} 0 0 1 {x0:.1f} {by - rr:.1f} Z')
    d.group('thin')
    d.circle(bx - (L - B) * s / 2 - rr - 34, by, rr)
    d.lines([[(x0 - rr, by + rr + 6), (x0 - rr, by + rr + 10)], [(x1 + rr, by + rr + 6), (x1 + rr, by + rr + 10)],
             [(x0 - rr, by + rr + 8), (x1 + rr, by + rr + 8)]])
    # labels
    d.group()
    d.text(shutter_x + 5, hole[1] - 8, 'HOLE', size=7, anchor='start')
    d.text(cx, left[1] - 16, "63° 12'", size=7)
    d.text(pm1[0] + r_arc + 4, pm1[1] + 26, '45°', size=7, anchor='start')
    d.text(wall_x - 5, pv2[1] - 8, 'VIOLET', size=7, anchor='end')
    d.text(wall_x - 5, pr2[1] + 13, 'RED', size=7, anchor='end')
    d.text(wall_x - 5, 210, 'WALL · 22 FT', size=7, anchor='end')
    d.text(bx - (L - B) * s / 2 - rr - 34, by - rr - 7, 'EXPECTED', size=7)
    d.text(bx, by - rr - 7, 'FOUND · 13¼ × 2⅝ IN', size=7)
    return d


def _conic(cx, cy, r0, e, R, top=-math.pi / 2, n=240):
    """A body launched level from height r0 above (cx, cy) with apoapsis there and eccentricity e.

    Returns the points of its path, clockwise, until it meets the sphere of radius R."""
    a = r0 / (1 + e)
    p = a * (1 - e * e)
    pts = []
    for i in range(n + 1):
        f = math.pi * 2 * i / n          # angle travelled from the apoapsis
        r = p / (1 - e * math.cos(f)) if e < 1 else r0
        if r < R and i > 0:
            # close the gap to the surface
            pts.append((cx + R * math.cos(top + f), cy + R * math.sin(top + f)))
            break
        pts.append((cx + r * math.cos(top + f), cy + r * math.sin(top + f)))
    return pts


def principia():
    """Newton's cannonball and the Moon test (Principia, Book III, Proposition IV).

    From a mountain, bodies thrown level ever faster fall on ellipses with a focus
    at the Earth's centre, until one falls all the way round. The Moon, 60 Earth
    radii out, is such a body: in a minute it falls from its tangent 15 Paris feet,
    what a stone falls at the surface in a second, since 60 × 60 minutes-squared make
    a second-squared's worth at 1/3600 the force. The Moon's distance and its fall
    are not to scale."""
    d = D()
    ex, ey, R = 84, 180, 40
    top = -math.pi / 2
    r0 = R + 24
    # construction: the Earth's centre lines, and the Moon's radius and orbit
    d.group('thin')
    mang = math.radians(-24)
    RM = 262
    moon = (ex + RM * math.cos(mang), ey + RM * math.sin(mang))
    d.line((ex, ey), moon)
    d.line((ex, ey), (ex, ey - r0))
    d.arc(ex, ey, RM, -38, -8, n=40)
    # tangent at the Moon, and the fall from it
    tang = (-math.sin(mang), math.cos(mang))        # direction of motion (clockwise in SVG = increasing angle)
    step = 58
    t_end = (moon[0] + step * tang[0], moon[1] + step * tang[1])
    d.line((moon[0] - 20 * tang[0], moon[1] - 20 * tang[1]), t_end)
    a_after = mang + step / RM
    on_orbit = (ex + RM * math.cos(a_after), ey + RM * math.sin(a_after))
    # the object: the Earth and its mountain
    d.group()
    d.circle(ex, ey, R)
    d.line((ex - 12, ey - R + 2), (ex, ey - r0), (ex + 12, ey - R + 2))
    d.circle(moon[0], moon[1], 7)
    # the throws: faster and faster, the last one never landing
    d.group('mid')
    for e in (0.55, 0.36, 0.2):
        pts = _conic(ex, ey, r0, e, R, top)
        d.line(*pts)
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        _arrow(d, x2, y2, math.atan2(y2 - y1, x2 - x1), 3.5)
    d.circle(ex, ey, r0)
    # the Moon's fall in one minute, drawn exaggerated
    d.line(t_end, on_orbit)
    _arrow(d, on_orbit[0], on_orbit[1], math.atan2(on_orbit[1] - t_end[1], on_orbit[0] - t_end[0]), 3.5)
    # an apple's fall in one second at the surface
    ax, ay0 = ex + 28, ey - R - 22
    ay1 = ey - math.sqrt(R * R - 28 * 28) - 1
    d.line((ax, ay0 + 3), (ax, ay1))
    _arrow(d, ax, ay1, math.pi / 2, 3)
    d.circle(ax, ay0, 3)
    # labels
    d.group()
    d.text(ex, ey + 4, 'EARTH', size=7)
    d.text(moon[0] + 11, moon[1] - 4, 'MOON', size=7, anchor='start')
    mid = (ex + 0.72 * (moon[0] - ex), ey + 0.72 * (moon[1] - ey))
    d.text(mid[0] - 4, mid[1] - 9, '60 EARTH RADII', size=7, anchor='end')
    d.text(on_orbit[0] - 8, on_orbit[1] + 4, '15 FT IN A MINUTE', size=7, anchor='end')
    d.text(ax + 7, ay0 - 4, '15 FT IN A SECOND', size=7, anchor='start')
    d.text(200, 292, 'GRAVITY AT THE MOON · 1/60² OF GRAVITY HERE', size=8)
    return d


def coulomb():
    """Coulomb's torsion balance in plan, with his three readings of 1785.

    The needle's ball is pushed from the fixed ball by the repulsion and held by the
    twist of the wire: at 36° with no twist at the head, at 18° with the head turned
    126° (144° in all), at 8½° with it turned 567° (575½°). Half the distance, four
    times the twist. The micrometer head's two turns are drawn as a spiral."""
    d = D()
    cx, cy, Rv = 150, 160, 118                   # the glass vessel, 12 inches across
    rn = Rv * 4 / 6                              # the needle's ball, 4 inches from the wire
    base = -90                                   # the fixed ball, at the scale's zero
    readings = [(36, 0, 36), (18, 126, 144), (8.5, 567, 575.5)]
    P = lambda r, a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    # construction: the scale round the vessel, with ticks every 2 degrees near zero, and radii
    d.group('thin')
    d.lines([[P(Rv, base + a), P(Rv - (7 if a % 10 == 0 else 3.5), base + a)] for a in range(-40, 62, 2)])
    d.arc(cx, cy, Rv - 7, base - 40, base + 60, n=60)
    d.lines([[(cx, cy), P(Rv, base + a)] for a, _, _ in readings] + [[(cx, cy), P(Rv, base)]])
    # the vessel and the wire
    d.group()
    d.circle(cx, cy, Rv)
    d.circle(cx, cy, 3)
    fixed = P(rn, base)
    d.circle(fixed[0], fixed[1], 5)
    # the needle at its three positions: the first two light, the last full
    d.group('mid')
    for a, _, _ in readings[:2]:
        b = P(rn, base + a)
        tail = P(rn * 0.8, base + a + 180)
        d.line(tail, b)
        d.circle(b[0], b[1], 4.5)
    # the separations, arcs at the needle's radius
    for k, (a, _, _) in enumerate(readings):
        rr = rn + 8 + 9 * k
        d.arc(cx, cy, rr, base, base + a, n=24)
    d.group()
    a = readings[2][0]
    b = P(rn, base + a)
    d.line(P(rn * 0.8, base + a + 180), b)
    d.circle(b[0], b[1], 4.5)
    # the micrometer head, seen from above: the twist given at each reading
    hx, hy, hr = 330, 108, 34
    d.group('thin')
    d.circle(hx, hy, hr)
    d.lines([[(hx + hr * math.cos(math.radians(t)), hy + hr * math.sin(math.radians(t))),
              (hx + (hr - 4) * math.cos(math.radians(t)), hy + (hr - 4) * math.sin(math.radians(t)))]
             for t in range(0, 360, 30)])
    d.group('mid')
    for k, (_, twist, _) in enumerate(readings[1:]):
        r_start = 10 + 6 * k
        pts = []
        steps = max(8, int(twist / 6))
        for i in range(steps + 1):
            t = twist * i / steps
            rr = r_start + 14 * t / 720
            pts.append((hx + rr * math.cos(math.radians(-90 + t)), hy + rr * math.sin(math.radians(-90 + t))))
        d.line(*pts)
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        _arrow(d, x2, y2, math.atan2(y2 - y1, x2 - x1), 3)
    # labels
    d.group()
    for k, (a, _, tot) in enumerate(readings):
        rr = rn + 8 + 9 * k
        lab = P(rr, base + a + 2)
        d.text(lab[0] + 2, lab[1] + 3, f'{a:g}°'.replace('8.5', '8½'), size=7, anchor='start')
    d.text(fixed[0] - 8, fixed[1] + 3, 'FIXED', size=7, anchor='end')
    d.text(hx, hy + hr + 13, 'HEAD TURNED', size=7)
    d.text(hx, hy + hr + 23, "126° · 567°", size=7)
    d.text(330, 206, 'TWIST IN ALL', size=7)
    d.text(330, 217, '36 · 144 · 575½', size=7)
    d.text(200, 292, 'HALF THE DISTANCE · FOUR TIMES THE FORCE', size=8)
    return d


PLATES = {'prism': prism, 'principia': principia, 'coulomb': coulomb}
