"""feynman plates, segment "MIT and Princeton" (sprint 014). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _ray_crossing(f, cx, cy, ang, level, rmax, step=0.5):
    """Walk out from (cx, cy) along `ang` until f first drops below `level`; return that point."""
    ux, uy = math.cos(ang), math.sin(ang)
    r0 = 0.0
    while r0 < rmax:
        r1 = r0 + step
        if f(cx + r1 * ux, cy + r1 * uy) < level:
            lo, hi = r0, r1
            for _ in range(30):
                mid = (lo + hi) / 2
                if f(cx + mid * ux, cy + mid * uy) < level:
                    hi = mid
                else:
                    lo = mid
            return cx + lo * ux, cy + lo * uy
        r0 = r1
    return cx + rmax * ux, cy + rmax * uy


def forces_in_molecules():
    """A diatomic molecule: the electron density's contours, the plane his thesis cut through the bond,
    the pulls on each nucleus, and the energy curve whose slope they equal."""
    d = D()
    ax_, bx_, y0 = 150, 250, 112  # the two nuclei on the bond axis
    a = 32.0                      # the orbital's decay length, in pixels

    def rho(x, y):
        ra = math.hypot(x - ax_, y - y0)
        rb = math.hypot(x - bx_, y - y0)
        return (math.exp(-ra / a) + math.exp(-rb / a)) ** 2  # a bonding orbital, squared

    mid = ((ax_ + bx_) / 2, y0)
    levels = [2.2, 1.2, 0.62, 0.3, 0.12, 0.05]

    # construction: the bond axis, the plane through the middle, the nuclear separation
    d.group('thin')
    d.line((24, y0), (376, y0))
    d.line((mid[0], 22), (mid[0], 196))
    d.lines([[(ax_, y0 + 6), (ax_, 200)], [(bx_, y0 + 6), (bx_, 200)]])
    d.line((ax_, 194), (bx_, 194))
    _arrow(d, ax_, 194, math.pi, 4)
    _arrow(d, bx_, 194, 0, 4)
    # the energy curve's axes, below
    ex0, ey0, ew, eh = 60, 280, 300, 60
    d.line((ex0, ey0 - eh), (ex0, ey0), (ex0 + ew, ey0))
    d.line((ex0, ey0 - eh * 0.75), (ex0 + ew, ey0 - eh * 0.75))

    # the electron density: contours computed from the orbital, merged or around each nucleus
    d.group('mid')
    for lv in levels:
        if rho(*mid) > lv:
            pts = [_ray_crossing(rho, mid[0], mid[1], 2 * math.pi * k / 180, lv, 190) for k in range(181)]
            d.line(*pts)
        else:
            for cx in (ax_, bx_):
                pts = [_ray_crossing(rho, cx, y0, 2 * math.pi * k / 120, lv, 60, 0.25) for k in range(121)]
                d.line(*pts)

    # the nuclei, and the forces on them: the cloud pulls in, the other nucleus pushes out
    d.group()
    for cx in (ax_, bx_):
        d.circle(cx, y0, 4)
    for cx, s in ((ax_, 1), (bx_, -1)):
        d.line((cx + s * 8, y0 - 14), (cx + s * 44, y0 - 14))
        _arrow(d, cx + s * 44, y0 - 14, 0 if s > 0 else math.pi, 5)
        d.line((cx - s * 8, y0 + 14), (cx - s * 44, y0 + 14))
        _arrow(d, cx - s * 44, y0 + 14, math.pi if s > 0 else 0, 5)

    # the energy of the molecule against the nuclei's separation (a Morse curve), and its slope
    De, re_, k = 1.0, 0.36, 7.5
    E = lambda r: De * (1 - math.exp(-k * (r - re_))) ** 2 - De
    P = lambda r, e: (ex0 + ew * r, ey0 - eh * 0.75 - eh * 0.72 * e)
    r_in = re_ - math.log(1 + math.sqrt(1.3)) / k  # where the curve climbs to E = +0.3
    curve = [P(r_in + (1 - r_in) * i / 120, E(r_in + (1 - r_in) * i / 120)) for i in range(121)]
    d.line(*curve)
    r1 = 0.52
    h = 1e-4
    slope = (E(r1 + h) - E(r1 - h)) / (2 * h)
    d.line(P(r1 - 0.12, E(r1) - 0.12 * slope), P(r1 + 0.12, E(r1) + 0.12 * slope))
    d.circle(*P(r1, E(r1)), 2.5)

    d.group()
    d.text(mid[0], 16, 'F = −∂E/∂R  ·  THE PULL OF THE CLOUD', size=8)
    d.text(mid[0], 206, 'R', size=8)
    d.text(ax_ - 6, y0 - 8, 'A', size=8, anchor='end')
    d.text(bx_ + 6, y0 - 8, 'B', size=8, anchor='start')
    d.text(ex0 + ew, ey0 + 12, 'R', size=7, anchor='end')
    d.text(ex0 - 4, ey0 - eh + 4, 'E', size=7, anchor='end')
    return d


def princeton():
    """The gun director's problem he met at Frankford Arsenal in 1941: where to aim at a plane that will have
    moved on, and a pair of the non-circular gears whose drawings he checked."""
    d = D()
    G = (44, 262)               # the gun
    P0 = (352, 58)              # the aircraft now
    v = 17.0                    # its speed, px per second, flying left
    s = 52.0                    # the shell's mean speed, px per second
    # solve |P0 + v t (−1, 0) − G| = s t for the time of flight t
    dx, dy = P0[0] - G[0], P0[1] - G[1]
    A_ = v * v - s * s
    B_ = -2 * v * dx
    C_ = dx * dx + dy * dy
    t = (-B_ - math.sqrt(B_ * B_ - 4 * A_ * C_)) / (2 * A_)
    F = (P0[0] - v * t, P0[1])

    # construction: the track with a tick for each second, the line of sight, the range circle it closes on
    d.group('thin')
    d.line((20, P0[1]), (384, P0[1]))
    d.lines([[(P0[0] - v * k, P0[1] - 4), (P0[0] - v * k, P0[1] + 4)] for k in range(0, int(t) + 2)])
    d.line(G, P0)
    rF = math.hypot(F[0] - G[0], F[1] - G[1])
    a0 = math.degrees(math.atan2(F[1] - G[1], F[0] - G[0]))
    d.arc(G[0], G[1], rF, a0 - 6, a0 + 22)

    # the object: the gun, the path to the meeting point, the plane's travel meanwhile
    d.group()
    d.line((G[0] - 14, G[1] + 8), (G[0] + 14, G[1] + 8))
    d.arc(G[0], G[1] + 2, 8, 180, 360)
    d.line(G, F)
    _arrow(d, *F, math.atan2(F[1] - G[1], F[0] - G[0]), 6)
    d.line(P0, F)
    _arrow(d, *F, math.pi, 6)
    d.circle(*P0, 3.5)
    d.circle(*F, 3.5)

    # the lead angle between sight and aim
    d.group('mid')
    ang_sight = math.degrees(math.atan2(P0[1] - G[1], P0[0] - G[0]))
    ang_aim = math.degrees(math.atan2(F[1] - G[1], F[0] - G[0]))
    d.arc(G[0], G[1], 70, ang_aim, ang_sight)

    # a pair of elliptical gears, each pivoted at a focus, rolling on the line of centres
    ga, ge = 30.0, 0.5
    gc, gb = ga * ge, ga * math.sqrt(1 - ge * ge)
    O1 = (222, 238)
    O2 = (O1[0] + 2 * ga, O1[1])
    d.group('thin')
    d.line((O1[0] - 42, O1[1]), (O2[0] + 60, O1[1]))
    d.lines([[(O1[0], O1[1] - 36), (O1[0], O1[1] + 36)], [(O2[0], O2[1] - 36), (O2[0], O2[1] + 36)]])
    d.group('mid')
    for O in (O1, O2):
        d.ellipse(O[0] + gc, O[1], ga, gb)
        d.circle(O[0], O[1], 2.2)
        d.circle(O[0] + 2 * gc, O[1], 1.2)
    d.circle(O1[0] + ga + gc, O1[1], 1.8)

    d.group()
    d.text(P0[0], P0[1] - 10, 'NOW', size=7)
    d.text(F[0], F[1] - 10, 'THEN', size=7)
    d.text((P0[0] + F[0]) / 2, P0[1] + 16, f'{t:.1f} S OF FLIGHT', size=7)
    d.text(G[0] + 78, G[1] - 38, 'LEAD', size=7, anchor='start')
    d.text(O1[0] + ga, O1[1] + 50, 'NON-CIRCULAR GEARS', size=7)
    d.text(200, 20, 'FRANKFORD ARSENAL · SUMMER 1941', size=8)
    return d


def absorber_theory():
    """Wheeler and Feynman's ten-light-second example in a spacetime diagram: the source's half-retarded and
    half-advanced waves, the absorber's advanced reply, and the test charge where they cancel and add."""
    d = D()
    ox, oy, k = 200, 150, 11.0  # the source's event at the origin; k px per light-second and per second
    P = lambda x, t: (ox + k * x, oy - k * t)

    # construction: the time axis and the present, a tick each second, the absorber's extent
    d.group('thin')
    d.line(P(-12.5, 0), P(12.5, 0))
    d.lines([[P(-12.5, tt), P(-12.1, tt)] for tt in range(-12, 13, 2)])
    d.lines([[P(x, 12.3), P(x, 11.9)] for x in range(-12, 13, 2)])
    for w in (-1, 1):
        d.lines([[P(w * 10, tt), P(w * 11.2, tt + 1.2)] for tt in range(-12, 11)])

    # the world lines: the source, the test charge one light-second away, the absorbing walls
    d.group()
    d.line(P(0, -12.5), P(0, 12.5))
    d.line(P(10, -12.5), P(10, 12.5))
    d.line(P(-10, -12.5), P(-10, 12.5))
    d.group('mid')
    d.line(P(1, -12.5), P(1, 12.5))

    # the source's field: half retarded (up the cone), half advanced (down it)
    d.group('mid')
    d.lines([[P(0, 0), P(10, 10)], [P(0, 0), P(-10, 10)]])
    d.lines([[P(0, 0), P(10, -10)], [P(0, 0), P(-10, -10)]])

    # the absorber's reply at t = +10, by advanced waves, reaching the source at t = 0 and the test charge at ±1
    d.group()
    d.line(P(10, 10), P(0, 0))
    d.line(P(-10, 10), P(1, -1))
    d.circle(*P(0, 0), 3.5)
    d.circle(*P(1, -1), 2.8)
    d.circle(*P(1, 1), 2.8)
    d.circle(*P(10, 10), 2.4)
    d.circle(*P(-10, 10), 2.4)

    d.group()
    d.text(*P(-10.6, -12.2), 'ABSORBER', size=7, anchor='end')
    d.text(*P(10.6, -12.2), 'ABSORBER', size=7, anchor='start')
    d.text(*P(2.2, -1.6), 't = −1  CANCEL', size=7, anchor='start')
    d.text(*P(2.2, 1.2), 't = +1  ADD', size=7, anchor='start')
    d.text(*P(-0.5, 0.6), 'SOURCE', size=7, anchor='end')
    d.text(*P(0, -13.4), '½ RETARDED + ½ ADVANCED', size=8)
    return d


def _meet(xa, ta, xb, sign, lo, hi):
    """The time on world line xb(t) that a light signal from (xa, ta) reaches (sign +1) or left (−1)."""
    g = lambda tb: abs(xb(tb) - xa) - sign * (tb - ta)
    for _ in range(60):
        mid = (lo + hi) / 2
        if (g(lo) > 0) == (g(mid) > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def thesis():
    """The problem his thesis took on: two charges whose action couples each moment of one path to two moments of
    the other, one earlier and one later, along light cones, so that no single instant holds the state."""
    d = D()
    ox, oy = 200, 272
    xa = lambda t: -46 + 12 * math.sin(t / 34.0)
    xb = lambda t: 46 + 10 * math.sin(t / 26.0 + 1.3)
    P = lambda x, t: (ox + x, oy - t)
    T = 240
    now = 120

    # construction: a stack of time slices, and the present one heavier
    d.group('thin')
    d.lines([[P(-150, tt), P(150, tt)] for tt in range(20, T + 1, 24)])
    d.line(P(-176, 0), P(176, 0))
    d.line(P(-176, now), P(176, now))

    # the two world lines
    d.group()
    d.line(*[P(xa(t), t) for t in range(0, T + 1, 2)])
    d.line(*[P(xb(t), t) for t in range(0, T + 1, 2)])

    # from moments on A, the light-cone links to B: one retarded (later on B), one advanced (earlier)
    d.group('mid')
    for ta in (104, 120, 138):
        tr = _meet(xa(ta), ta, xb, +1, ta, ta + 200)
        tv = _meet(xa(ta), ta, xb, -1, ta - 200, ta)
        d.lines([[P(xa(ta), ta), P(xb(tr), tr)], [P(xa(ta), ta), P(xb(tv), tv)]])
    d.group()
    for ta in (104, 120, 138):
        tr = _meet(xa(ta), ta, xb, +1, ta, ta + 200)
        tv = _meet(xa(ta), ta, xb, -1, ta - 200, ta)
        d.circle(*P(xa(ta), ta), 3)
        d.circle(*P(xb(tr), tr), 2.2)
        d.circle(*P(xb(tv), tv), 2.2)

    d.group()
    d.text(200, 16, 'S = −Σ m∫ds + ½ ΣΣ eᵢeⱼ ∫∫ δ(I²ᵢⱼ) dxᵢ·dxⱼ', size=8)
    d.text(*P(xa(T) - 6, T - 4), 'A', size=8, anchor='end')
    d.text(*P(xb(T) + 6, T - 4), 'B', size=8, anchor='start')
    d.text(*P(-176, now + 5), 'NOW', size=7, anchor='start')
    d.text(*P(176, -14), 'TIME ↑  ·  SPACE →', size=7, anchor='end')
    return d


def _hav_miles(p, q):
    la1, lo1, la2, lo2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 3958.8 * math.asin(math.sqrt(h))


PLACES = {
    'FAR ROCKAWAY': (40.6054, -73.7551),
    'PRINCETON': (40.3487, -74.6590),
    'STATEN ISLAND': (40.6437, -74.0736),
    'DEBORAH HOSPITAL': (39.9775, -74.5850),
}


def arline():
    """Where the story happened, on a plane chart: Far Rockaway, Princeton, the Staten Island wedding,
    Deborah Hospital in the Pine Barrens, and the distances between them as the crow flies."""
    d = D()
    lat0 = 40.3
    kx = 290 * math.cos(math.radians(lat0))  # px per degree of longitude
    ky = 290                                  # px per degree of latitude
    lon_c, lat_c = -74.2, 40.3
    P = lambda la, lo: (200 + kx * (lo - lon_c), 150 - ky * (la - lat_c))
    pt = {n: P(*ll) for n, ll in PLACES.items()}

    # construction: the graticule every quarter degree
    d.group('thin')
    for i in range(-4, 5):
        lo = -74.25 + 0.25 * i
        d.line(P(39.85, lo), P(40.78, lo))
    for j in range(0, 4):
        la = 40.0 + 0.25 * j
        d.line(P(la, -75.0), P(la, -73.55))

    # the journey on the wedding day: from her home, to the wedding, to the hospital
    d.group()
    d.line(pt['FAR ROCKAWAY'], pt['STATEN ISLAND'], pt['DEBORAH HOSPITAL'])
    for n in PLACES:
        d.circle(*pt[n], 3.2)

    # his weekend trip, Princeton to Deborah
    d.group('mid')
    d.line(pt['PRINCETON'], pt['DEBORAH HOSPITAL'])

    # a ten-mile scale bar and a north arrow
    d.group('mid')
    mi10 = 10 / 69.0 * ky
    sx, sy = 262, 256
    d.line((sx, sy), (sx + mi10, sy))
    d.lines([[(sx, sy - 4), (sx, sy + 4)], [(sx + mi10, sy - 4), (sx + mi10, sy + 4)],
             [(sx + mi10 / 2, sy - 3), (sx + mi10 / 2, sy + 3)]])
    d.line((362, 70), (362, 34))
    _arrow(d, 362, 34, -math.pi / 2, 6)

    d.group()
    d.text(pt['FAR ROCKAWAY'][0] - 6, pt['FAR ROCKAWAY'][1] - 10, 'FAR ROCKAWAY', size=7, anchor='middle')
    d.text(pt['PRINCETON'][0] - 8, pt['PRINCETON'][1] + 3, 'PRINCETON', size=7, anchor='end')
    d.text(pt['STATEN ISLAND'][0] + 2, pt['STATEN ISLAND'][1] - 10, 'STATEN ISLAND', size=7, anchor='middle')
    d.text(pt['DEBORAH HOSPITAL'][0] + 8, pt['DEBORAH HOSPITAL'][1] + 3, 'DEBORAH', size=7, anchor='start')
    m1 = _hav_miles(PLACES['PRINCETON'], PLACES['DEBORAH HOSPITAL'])
    mp = ((pt['PRINCETON'][0] + pt['DEBORAH HOSPITAL'][0]) / 2, (pt['PRINCETON'][1] + pt['DEBORAH HOSPITAL'][1]) / 2)
    d.text(mp[0] - 8, mp[1], f'{m1:.0f} MI', size=7, anchor='end')
    d.text(sx + mi10 / 2, sy + 14, '10 MI', size=7)
    d.text(362, 84, 'N', size=7)
    d.text(200, 292, 'AS THE CROW FLIES · 29 JUNE 1942', size=8)
    return d


PLATES = {
    'forces-in-molecules': forces_in_molecules,
    'princeton': princeton,
    'absorber-theory': absorber_theory,
    'thesis': thesis,
    'arline': arline,
}
