"""feynman plates, segment "Cornell" (sprint 014). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians, page coordinates)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _mid_arrow(d, a, b, size=5, at=0.55):
    """An arrowhead part-way along the segment a→b, pointing from a to b."""
    x, y = a[0] + (b[0] - a[0]) * at, a[1] + (b[1] - a[1]) * at
    _arrow(d, x, y, math.atan2(b[1] - a[1], b[0] - a[0]), size)


def _wave(a, b, amp=4.0, waves=5, n=120):
    """A photon line: a sine wiggle from a to b with a whole number of waves, so it meets both ends."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    return [(a[0] + dx * i / n + px * amp * math.sin(2 * math.pi * waves * i / n),
             a[1] + dy * i / n + py * amp * math.sin(2 * math.pi * waves * i / n)) for i in range(n + 1)]


def _wave_arc(cx, cy, r, a0, a1, amp=3.0, waves=6, n=120):
    """A photon line wiggling along a circular arc (angles in degrees, page coordinates)."""
    pts = []
    for i in range(n + 1):
        t = math.radians(a0 + (a1 - a0) * i / n)
        rr = r + amp * math.sin(2 * math.pi * waves * i / n)
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    return pts


# --- cornell: the journey east, and the offers that followed him ----------------------------

PLACES = {
    'LOS ALAMOS': (35.88, -106.30),
    'AMES': (42.03, -93.62),
    'ITHACA': (42.44, -76.50),
    'BERKELEY': (37.87, -122.27),
    'LOS ANGELES': (34.07, -118.44),
    'PRINCETON': (40.35, -74.66),
}


def _km(p, q):
    """Great-circle distance in kilometres between two (lat, lon) points."""
    la1, lo1, la2, lo2 = map(math.radians, (*p, *q))
    c = math.sin(la1) * math.sin(la2) + math.cos(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return 6371 * math.acos(max(-1, min(1, c)))


def cornell():
    """Los Alamos to Ithaca by way of Iowa State, autumn 1945, and the offers that came after him to Ithaca."""
    d = D()
    lat0, lon0, lat1, lon1 = 30, -126, 48, -70
    k = math.cos(math.radians(39))  # an equirectangular map, true to scale along 39° N
    sx = 360 / ((lon1 - lon0) * k)
    P = lambda lat, lon: (20 + (lon - lon0) * k * sx, 232 - (lat - lat0) * sx)
    # construction: the graticule, every five degrees
    d.group('thin')
    d.lines([[P(lat0, lon), P(lat1, lon)] for lon in range(-125, -69, 5)])
    d.lines([[P(lat, lon0), P(lat, lon1)] for lat in range(30, 49, 5)])
    # the journey: Los Alamos, a talk at Iowa State in Ames, then the train to Ithaca
    d.group()
    la, am, it = P(*PLACES['LOS ALAMOS']), P(*PLACES['AMES']), P(*PLACES['ITHACA'])
    d.line(la, am, it)
    _mid_arrow(d, la, am, 6)
    _mid_arrow(d, am, it, 6)
    for p in (la, am):
        d.circle(*p, 3.5)
    d.circle(*it, 6)
    d.circle(*it, 2.5)
    # the offers he turned down, drawn from where they came to where he was
    d.group('mid')
    for name in ('BERKELEY', 'LOS ANGELES', 'PRINCETON'):
        a = P(*PLACES[name])
        d.circle(*a, 3)
        ang = math.atan2(it[1] - a[1], it[0] - a[0])
        end = (it[0] - 9 * math.cos(ang), it[1] - 9 * math.sin(ang))
        d.line(a, end)
        _arrow(d, *end, ang, 4)
    # labels
    d.group()
    d.text(200, 22, 'LOS ALAMOS → IOWA STATE → ITHACA · AUTUMN 1945', size=8)
    d.text(la[0], la[1] + 16, 'LOS ALAMOS', size=7)
    d.text(am[0], am[1] + 16, 'AMES', size=7)
    d.text(it[0] + 2, it[1] - 14, 'ITHACA', size=7)
    b, l, p = P(*PLACES['BERKELEY']), P(*PLACES['LOS ANGELES']), P(*PLACES['PRINCETON'])
    d.text(b[0] + 6, b[1] - 8, 'BERKELEY', size=7, anchor='start')
    d.text(l[0] + 6, l[1] + 14, 'UCLA', size=7, anchor='start')
    d.text(p[0], p[1] + 16, 'IAS', size=7)
    d1 = _km(PLACES['LOS ALAMOS'], PLACES['AMES'])
    d2 = _km(PLACES['AMES'], PLACES['ITHACA'])
    m1 = ((la[0] + am[0]) / 2, (la[1] + am[1]) / 2)
    m2 = ((am[0] + it[0]) / 2, (am[1] + it[1]) / 2)
    d.text(m1[0] + 8, m1[1] + 14, f'{round(d1, -1):,.0f} KM', size=7, anchor='start')
    d.text(m2[0] - 6, m2[1] + 16, f'{round(d2, -1):,.0f} KM', size=7)
    d.text(200, 268, 'STRAIGHT LEGS, NOT THE RAILWAY · THIN LINES: OFFERS HE REFUSED', size=7)
    return d


# --- wobbling-plate: a thin disc, its axis coning round the angular momentum ------------------

def _proj(p, az=math.radians(-25), el=math.radians(24), s=100, cx=196, cy=196):
    x, y, z = p
    xr = x * math.cos(az) - y * math.sin(az)
    yr = x * math.sin(az) + y * math.cos(az)
    return (cx + s * xr, cy - s * (z * math.cos(el) - yr * math.sin(el)))


def wobbling_plate():
    """A thin disc spinning torque-free: its axis cones round the fixed angular momentum twice for each turn of the seal."""
    d = D()
    th = math.radians(14)  # the tilt, exaggerated to be seen; the 2:1 ratio holds as it goes to zero
    n = (math.sin(th), 0.0, math.cos(th))
    e1 = (math.cos(th), 0.0, -math.sin(th))
    e2 = (0.0, 1.0, 0.0)
    disc = lambda r, t: (r * (math.cos(t) * e1[0] + math.sin(t) * e2[0]),
                         r * (math.cos(t) * e1[1] + math.sin(t) * e2[1]),
                         r * (math.cos(t) * e1[2] + math.sin(t) * e2[2]))
    ring = lambda r, z, a0=0, a1=360: [_proj((r * math.cos(math.radians(a)), r * math.sin(math.radians(a)), z))
                                       for a in range(int(a0), int(a1) + 1, 4)]
    L = 1.18   # drawn length of the angular momentum and of the disc's axis
    # construction: the plane square to L, its axis, the cone the disc's axis sweeps, the line of nodes
    d.group('thin')
    d.line(*ring(1.0, 0))
    d.line(_proj((0, 0, -0.35)), _proj((0, 0, 0)))
    d.line(_proj((0, -1.25, 0)), _proj((0, 1.25, 0)))
    d.line(*ring(L * math.sin(th), L * math.cos(th)))
    d.line(_proj((0, 0, 0)), _proj((-L * math.sin(th), 0, L * math.cos(th))))
    # the plate: its rim and its well
    d.group()
    d.line(*[_proj(disc(1.0, math.radians(a))) for a in range(0, 361, 3)])
    d.group('mid')
    d.line(*[_proj(disc(0.64, math.radians(a))) for a in range(0, 361, 3)])
    # the seal on the rim, and the way it goes round
    sa = math.radians(250)
    sc = disc(0.86, sa)
    d.line(*[_proj(tuple(sc[i] + 0.07 * (math.cos(t) * e1[i] + math.sin(t) * e2[i]) for i in range(3)))
             for t in [2 * math.pi * j / 36 for j in range(37)]])
    arc = [_proj(disc(1.1, math.radians(a))) for a in range(214, 250, 3)]
    d.line(*arc)
    _arrow(d, *arc[-1], math.atan2(arc[-1][1] - arc[-2][1], arc[-1][0] - arc[-2][0]), 4)
    # the vectors: L fixed and vertical, the disc's axis, and ω on the far side of L
    d.group()
    o = _proj((0, 0, 0))
    top = _proj((0, 0, L + 0.12))
    d.line(o, top)
    _arrow(d, *top, -math.pi / 2, 6)
    ax = _proj(tuple(L * c for c in n))
    d.line(o, ax)
    _arrow(d, *ax, math.atan2(ax[1] - o[1], ax[0] - o[0]), 6)
    w = (2 / math.cos(th) * 0 - n[0], 0.0, 2 / math.cos(th) - n[2])
    wl = math.sqrt(sum(c * c for c in w))
    wt = _proj(tuple(1.12 * c / wl for c in w))
    d.line(o, wt)
    _arrow(d, *wt, math.atan2(wt[1] - o[1], wt[0] - o[0]), 5)
    # the wobble's direction on the cone
    cone = ring(L * math.sin(th) + 0.1, L * math.cos(th), 100, 190)
    d.group('mid')
    d.line(*cone)
    _arrow(d, *cone[-1], math.atan2(cone[-1][1] - cone[-2][1], cone[-1][0] - cone[-2][0]), 4)
    th_arc = [_proj((0.5 * math.sin(math.radians(a)), 0, 0.5 * math.cos(math.radians(a)))) for a in range(0, 15, 2)]
    d.line(*th_arc)
    # labels
    d.group()
    d.text(top[0] + 7, top[1] + 4, 'L', size=9, anchor='start')
    d.text(ax[0] + 10, ax[1] + 12, 'AXIS', size=7, anchor='start')
    d.text((o[0] + wt[0]) / 2 - 8, (o[1] + wt[1]) / 2, 'ω', size=9, anchor='end')
    d.text(th_arc[-1][0] + 6, th_arc[-1][1] - 2, 'θ', size=8, anchor='start')
    d.text(cone[-1][0] - 10, cone[-1][1] - 4, 'WOBBLE 2', size=7, anchor='end')
    d.text(arc[0][0] - 4, arc[0][1] + 16, 'SEAL 1', size=7, anchor='end')
    d.text(200, 24, 'THIN DISC · I₃ = 2 I₁ · WOBBLE : SPIN = 2 : 1', size=8)
    d.text(200, 276, 'TILT DRAWN AT 14° · THE RATIO IS FOR A SMALL TILT', size=7)
    return d


# --- pocono: what he showed, and the piece he could not yet do --------------------------------

def pocono():
    """Three space-time pictures from Feynman's Pocono talk: the self-energy, the N-shaped path of a pair, the closed loop."""
    d = D()
    t0, t1 = 238, 62  # early at the bottom, late at the top
    # construction: moments of time across all three, and the time axis
    d.group('thin')
    d.lines([[(44, y), (384, y)] for y in range(t1, t0 + 1, 22)])
    d.lines([[(157, t0 + 6), (157, t1 - 6)], [(271, t0 + 6), (271, t1 - 6)]])
    # I: an electron that emits a quantum and absorbs it again
    d.group()
    a, b = (72, t0), (126, t1)
    d.line(a, b)
    p3 = (a[0] + (b[0] - a[0]) * 0.3, a[1] + (b[1] - a[1]) * 0.3)
    p4 = (a[0] + (b[0] - a[0]) * 0.72, a[1] + (b[1] - a[1]) * 0.72)
    _mid_arrow(d, a, p3, 5, 0.5)
    _mid_arrow(d, p4, b, 5, 0.6)
    # II: the N in time: forward, back (a positron), forward again, turned at two kicks from a potential
    s, k1, k2, e = (180, t0), (238, 118), (190, 182), (250, t1)
    d.line(s, k1, k2, e)
    _mid_arrow(d, s, k1, 5, 0.4)
    _mid_arrow(d, k1, k2, 5)
    _mid_arrow(d, k2, e, 5, 0.6)
    # III: a quantum makes a pair that closes on itself: vacuum polarisation
    cx, cy, rx, ry = 328, 150, 20, 32
    d.ellipse(cx, cy, rx, ry)
    _arrow(d, cx + rx, cy, math.pi / 2, 5)
    _arrow(d, cx - rx, cy, -math.pi / 2, 5)
    # the quanta, wiggling
    d.group('mid')
    mx, my = (p3[0] + p4[0]) / 2, (p3[1] + p4[1]) / 2
    r = math.dist(p3, p4) / 2
    ang = math.degrees(math.atan2(p3[1] - my, p3[0] - mx))
    d.line(*_wave_arc(mx, my, r, ang, ang + 180, amp=3, waves=7))
    d.line(*_wave((cx, t0), (cx, cy + ry), amp=3.5, waves=5))
    d.line(*_wave((cx, cy - ry), (cx, t1), amp=3.5, waves=5))
    for p in (k1, k2):
        d.lines([[(p[0] - 4, p[1] - 4), (p[0] + 4, p[1] + 4)], [(p[0] - 4, p[1] + 4), (p[0] + 4, p[1] - 4)]])
    for p in (p3, p4):
        d.circle(*p, 2.2)
    # the time axis and labels
    d.group()
    d.line((26, t0), (26, t1 - 8))
    _arrow(d, 26, t1 - 8, -math.pi / 2, 5)
    d.text(200, 26, 'POCONO MANOR · 30 MARCH–1 APRIL 1948', size=8)
    d.text(34, t1 - 10, 'TIME', size=7, anchor='start')
    d.text(100, 258, 'SELF-ENERGY', size=7)
    d.text(214, 258, 'PAIR: N IN TIME', size=7)
    d.text(328, 258, 'CLOSED LOOP', size=7)
    d.text(100, 272, 'DONE', size=7)
    d.text(214, 272, 'DONE', size=7)
    d.text(328, 272, 'NOT YET', size=7)
    return d


# --- diagrams: Fig. 1 of "Space-Time Approach to Quantum Electrodynamics" (1949) -------------

def diagrams():
    """Fig. 1 of the 1949 paper: two electrons exchange one quantum, each line a factor of the amplitude."""
    d = D()
    p = {1: (112, 236), 5: (142, 176), 3: (104, 62), 2: (298, 236), 6: (258, 128), 4: (296, 62)}
    # construction: time lines, and the light cones through the two events
    d.group('thin')
    d.lines([[(40, y), (372, y)] for y in range(62, 237, 29)])
    for q in (5, 6):
        x, y = p[q]
        d.lines([[(x - 44, y - 44), (x + 44, y + 44)], [(x - 44, y + 44), (x + 44, y - 44)]])
    # the two electrons
    d.group()
    for a, b, c in ((1, 5, 3), (2, 6, 4)):
        d.line(p[a], p[b], p[c])
        _mid_arrow(d, p[a], p[b])
        _mid_arrow(d, p[b], p[c], 5, 0.5)
    # the virtual quantum between 5 and 6
    d.group('mid')
    d.line(*_wave(p[5], p[6], amp=4, waves=6))
    for q in (5, 6):
        d.circle(*p[q], 2.4)
    # the time axis and labels: each line names its factor
    d.group()
    d.line((24, 236), (24, 58))
    _arrow(d, 24, 58, -math.pi / 2, 5)
    d.text(32, 58, 'TIME', size=7, anchor='start')
    d.text(200, 22, 'PHYS. REV. 76, 772 · FIG. 1 · ONE QUANTUM EXCHANGED', size=8)
    for q, (dx, dy) in {1: (-8, 4), 2: (8, 4), 3: (-8, 0), 4: (8, 0), 5: (-9, 2), 6: (9, 6)}.items():
        d.text(p[q][0] + dx, p[q][1] + dy, str(q), size=8, anchor='end' if dx < 0 else 'start')
    d.text(134, 212, 'K₊(5,1)', size=7, anchor='start')
    d.text(130, 118, 'K₊(3,5)', size=7, anchor='start')
    d.text(284, 188, 'K₊(6,2)', size=7, anchor='start')
    d.text(284, 100, 'K₊(4,6)', size=7, anchor='start')
    d.text(204, 138, 'δ₊(s²₅₆)', size=7)
    d.text(150, 196, 'γμ', size=7, anchor='start')
    d.text(250, 148, 'γμ', size=7, anchor='end')
    d.text(200, 262, 'K(3,4;1,2) = −ie² ∫∫ K₊(3,5) K₊(4,6) γμ γμ', size=7)
    d.text(200, 276, '× δ₊(s²₅₆) K₊(5,1) K₊(6,2) dτ₅ dτ₆', size=7)
    return d


PLATES = {
    'cornell': cornell,
    'wobbling-plate': wobbling_plate,
    'pocono': pocono,
    'diagrams': diagrams,
}
