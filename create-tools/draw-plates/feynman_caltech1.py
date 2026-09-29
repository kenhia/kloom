"""feynman plates, segment "Caltech", first five frames (sprint 014). See feynman.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _unit(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def _slerp(a, b, t):
    """A point a fraction t along the great circle from unit vector a to b, as (lat, lon)."""
    om = math.acos(max(-1, min(1, sum(p * q for p, q in zip(a, b)))))
    s = math.sin(om)
    v = [(math.sin((1 - t) * om) * p + math.sin(t * om) * q) / s for p, q in zip(a, b)]
    return math.degrees(math.asin(v[2])), math.degrees(math.atan2(v[1], v[0]))


def caltech():
    """The Americas on an orthographic globe: Ithaca, Pasadena and Rio, and the great circles between them."""
    d = D()
    cx, cy, r = 176, 150, 128
    lat0, lon0 = math.radians(8), math.radians(-78)

    def proj(lat, lon):
        la, lo = math.radians(lat), math.radians(lon)
        x = math.cos(la) * math.sin(lo - lon0)
        y = math.cos(lat0) * math.sin(la) - math.sin(lat0) * math.cos(la) * math.cos(lo - lon0)
        c = math.sin(lat0) * math.sin(la) + math.cos(lat0) * math.cos(la) * math.cos(lo - lon0)
        return cx + r * x, cy - r * y, c > 0

    def poly(coords, n=6):
        segs, cur = [], []
        dense = []
        for (a, b), (c, e) in zip(coords, coords[1:]):
            dense += [(a + (c - a) * i / n, b + (e - b) * i / n) for i in range(n)]
        dense.append(coords[-1])
        for la, lo in dense:
            x, y, vis = proj(la, lo)
            if vis:
                cur.append((x, y))
            elif cur:
                segs.append(cur)
                cur = []
        if cur:
            segs.append(cur)
        return segs

    # construction: the graticule every 15 degrees
    d.group('thin')
    segs = []
    for la in range(-75, 90, 15):
        segs += poly([(la, lo) for lo in range(-180, 181, 5)], 1)
    for lo in range(-180, 180, 15):
        segs += poly([(la, lo) for la in range(-90, 91, 5)], 1)
    d.lines(segs)
    # the limb
    d.group()
    d.circle(cx, cy, r)
    # the coasts of the Americas, coarsely
    d.group('mid')
    namerica = [(60, -140), (58, -136), (54, -131), (48, -124), (42, -124), (38, -123), (34, -120), (33, -117),
                (30, -116), (23, -110), (26, -112), (31, -114), (28, -111), (23, -106), (19, -105), (16, -98),
                (15, -93), (13, -88), (11, -86), (9, -84), (8, -80), (9, -78)]
    east = [(9, -78), (10, -76), (15, -83), (18, -88), (21, -87), (21, -90), (19, -96), (26, -97), (29, -94),
            (30, -89), (30, -84), (25, -81), (27, -80), (30, -81), (35, -76), (39, -74), (41, -72), (42, -70),
            (44, -69), (45, -66), (47, -60), (52, -56), (58, -62), (60, -64)]
    samerica = [(9, -78), (7, -78), (1, -80), (-5, -81), (-14, -76), (-18, -70), (-30, -71), (-38, -73),
                (-47, -75), (-54, -72), (-55, -68), (-52, -69), (-47, -66), (-42, -64), (-39, -57), (-34, -53),
                (-28, -48), (-23, -42), (-13, -38), (-8, -35), (-5, -35), (-2, -44), (5, -52), (10, -62),
                (11, -72), (10, -76)]
    d.lines(poly(namerica) + poly(east) + poly(samerica))
    # the moves: Ithaca to Pasadena, Pasadena to Rio and back
    places = {'ITHACA': (42.44, -76.50), 'PASADENA': (34.15, -118.14), 'RIO': (-22.91, -43.17)}
    d.group()
    for a, b in (('ITHACA', 'PASADENA'), ('PASADENA', 'RIO')):
        ua, ub = _unit(*places[a]), _unit(*places[b])
        d.lines(poly([_slerp(ua, ub, i / 60) for i in range(61)], 1))
    for name, (la, lo) in places.items():
        x, y, _ = proj(la, lo)
        d.circle(x, y, 3.2)
    # detail: arrowheads at the arrivals
    d.group('mid')
    for a, b in (('ITHACA', 'PASADENA'), ('PASADENA', 'RIO')):
        ua, ub = _unit(*places[a]), _unit(*places[b])
        p1 = proj(*_slerp(ua, ub, 0.9))
        p2 = proj(*_slerp(ua, ub, 0.93))
        _arrow(d, p2[0], p2[1], math.atan2(p2[1] - p1[1], p2[0] - p1[0]), 6)
    # labels
    d.group()
    for name, (la, lo) in places.items():
        x, y, _ = proj(la, lo)
        d.text(x + (-7 if name == 'PASADENA' else 7), y - 6, name, size=8, anchor='end' if name == 'PASADENA' else 'start')
    d.text(334, 60, '1950', size=9)
    d.text(334, 74, 'CORNELL → CALTECH', size=7)
    d.text(334, 214, '1951–52', size=9)
    d.text(334, 228, 'A YEAR IN RIO', size=7)
    d.text(cx, 293, 'ORTHOGRAPHIC · GRATICULE 15°', size=7)
    return d


def brazil():
    """Brewster's angle at the bay: sunlight reflected off water is polarised, so a Polaroid turned the right way darkens it."""
    d = D()
    sx, sy = 200, 196        # the point of reflection on the water
    n = 1.33                 # water
    tb = math.atan(n)        # Brewster's angle from the normal, 53.1 degrees
    tr = math.asin(math.sin(tb) / n)
    L = 150
    inc = (sx - L * math.sin(tb), sy - L * math.cos(tb))
    ref = (sx + L * math.sin(tb), sy - L * math.cos(tb))
    trn = (sx + 90 * math.sin(tr), sy + 90 * math.cos(tr))
    # construction: the normal, the angle arcs, the right angle between reflected and refracted rays
    d.group('thin')
    d.line((sx, sy - 170), (sx, sy + 96))
    d.arc(sx, sy, 44, -90 - math.degrees(tb), -90, 32)
    d.arc(sx, sy, 50, -90, -90 + math.degrees(tb), 32)
    d.arc(sx, sy, 38, 90 - math.degrees(tr), 90, 24)
    ang_r = math.atan2(ref[1] - sy, ref[0] - sx)
    ang_t = math.atan2(trn[1] - sy, trn[0] - sx)
    k = 14
    p1 = (sx + k * math.cos(ang_r), sy + k * math.sin(ang_r))
    p3 = (sx + k * math.cos(ang_t), sy + k * math.sin(ang_t))
    d.line(p1, (p1[0] + p3[0] - sx, p1[1] + p3[1] - sy), p3)
    # the water surface and the rays
    d.group()
    d.line((20, sy), (380, sy))
    d.line(inc, (sx, sy), ref)
    d.line((sx, sy), trn)
    for (x0, y0), (x1, y1) in ((inc, (sx, sy)), ((sx, sy), ref), ((sx, sy), trn)):
        mx, my = x0 + 0.55 * (x1 - x0), y0 + 0.55 * (y1 - y0)
        _arrow(d, mx, my, math.atan2(y1 - y0, x1 - x0), 6)
    # detail: polarisation marks. Incident: both (dots and strokes); reflected: dots only (perpendicular)
    d.group('mid')
    ux, uy = (sx - inc[0]) / L, (sy - inc[1]) / L
    for t in (0.18, 0.32, 0.46):
        px, py = inc[0] + t * L * ux, inc[1] + t * L * uy
        d.line((px - 6 * uy, py + 6 * ux), (px + 6 * uy, py - 6 * ux))
        d.circle(px + 3 * ux, py + 3 * uy, 1.4)
    vx, vy = (ref[0] - sx) / L, (ref[1] - sy) / L
    for t in (0.3, 0.45, 0.6, 0.75):
        d.circle(sx + t * L * vx, sy + t * L * vy, 1.6)
    # the Polaroid across the reflected ray, its transmission axis in the plane of incidence
    px, py = sx + 0.9 * L * vx, sy + 0.9 * L * vy
    w = 22
    d.line((px - w * vy, py + w * vx), (px + w * vy, py - w * vx))
    d.line((px - w * vy + 3 * vx, py + w * vx + 3 * vy), (px + w * vy + 3 * vx, py - w * vx + 3 * vy))
    d.lines([[(px - (w - 6 * i) * vy, py + (w - 6 * i) * vx), (px - (w - 6 * i) * vy + 3 * vx, py + (w - 6 * i) * vx + 3 * vy)]
             for i in range(8)])
    # waves below the surface
    d.lines([[(30 + 58 * i + 6 * j, sy + 40 + 18 * (i % 2)) for j in range(0, 5)] for i in range(6) if i != 3])
    # labels
    d.group()
    d.text(sx - 26, sy - 50, 'θB', size=8)
    d.text(sx + 30, sy - 58, 'θB', size=8)
    d.text(sx + 12, sy + 52, 'θt', size=8, anchor='start')
    d.text(sx + 24, sy + 24, '90°', size=7, anchor='start')
    d.text(inc[0] - 2, inc[1] - 8, 'SUNLIGHT', size=7, anchor='start')
    d.text(px + 26, py + 8, 'POLAROID', size=7, anchor='start')
    d.text(370, sy - 6, 'AIR', size=7, anchor='end')
    d.text(370, sy + 14, 'WATER · n = 1.33', size=7, anchor='end')
    d.text(200, 292, 'tan θB = n · θB = 53.1° · REFLECTED LIGHT POLARISED', size=7)
    return d


def superfluid_helium():
    """The Feynman relation: the liquid's structure factor S(k), and the excitation curve E(k) = h²k²/2mS(k) it implies."""
    d = D()
    # a model structure factor (illustrative): linear at small k, a diffraction peak near 2 per angstrom
    def S(k):
        base = (0.33 * k + 0.045 * k ** 6) / (1 + 0.045 * k ** 6)
        return base + 0.42 * math.exp(-((k - 2.0) / 0.28) ** 2 / 2) - 0.06 * math.exp(-((k - 2.8) / 0.4) ** 2 / 2)
    free = lambda k: 6.06 * k * k     # h-bar^2 k^2 / 2m for a helium atom, in kelvin, k in 1/angstrom
    ks = [0.02 + i * 3.18 / 159 for i in range(160)]
    ox, w = 52, 320
    X = lambda k: ox + w * k / 3.2
    # upper panel S(k); lower panel E(k)
    sy0, sh = 116, 80
    ey0, eh = 270, 132
    Y1 = lambda s: sy0 - sh * s / 1.5
    Y2 = lambda e: ey0 - eh * e / 40
    d.group('thin')
    d.lines([[(X(k), sy0), (X(k), sy0 - sh - 4)] for k in (0.5, 1, 1.5, 2, 2.5, 3)])
    d.lines([[(X(k), ey0), (X(k), ey0 - eh - 4)] for k in (0.5, 1, 1.5, 2, 2.5, 3)])
    d.line((ox, Y1(1)), (ox + w, Y1(1)))
    d.lines([[(ox, Y2(e)), (ox + w, Y2(e))] for e in (10, 20, 30, 40)])
    kmin = min((k for k in ks if 1.6 < k < 2.6), key=lambda k: free(k) / S(k))
    d.line((X(kmin), sy0 - sh - 4), (X(kmin), ey0))
    # axes
    d.group()
    d.line((ox, sy0 - sh - 6), (ox, sy0), (ox + w + 6, sy0))
    d.line((ox, ey0 - eh - 6), (ox, ey0), (ox + w + 6, ey0))
    _arrow(d, ox + w + 6, sy0, 0, 4)
    _arrow(d, ox + w + 6, ey0, 0, 4)
    # the curves
    d.group()
    d.line(*[(X(k), Y1(S(k))) for k in ks])
    d.line(*[(X(k), Y2(min(free(k) / S(k), 41))) for k in ks if free(k) / S(k) < 41])
    # detail: the phonon line, the free-atom parabola, the roton minimum
    d.group('mid')
    d.line((X(0), Y2(0)), (X(1.9), Y2(18.3 * 1.9)))
    d.line(*[(X(k), Y2(free(k))) for k in ks if free(k) < 41])
    emin = free(kmin) / S(kmin)
    d.circle(X(kmin), Y2(emin), 3)
    d.group()
    d.text(ox - 6, Y1(1) + 3, '1', size=7, anchor='end')
    d.text(ox + 6, sy0 - sh - 8, 'S(k)', size=8, anchor='start')
    d.text(ox + 6, ey0 - eh - 8, 'E(k) = ħ²k²/2mS(k)', size=8, anchor='start')
    d.text(X(kmin) + 6, sy0 - sh + 6, 'DIFFRACTION PEAK', size=7, anchor='start')
    d.text(X(kmin) + 8, Y2(emin) + 14, 'ROTON', size=7, anchor='start')
    d.text(X(0.55), Y2(15), 'PHONONS', size=7, anchor='end')
    d.text(X(1.72), Y2(40) + 2, 'FREE ATOM', size=7, anchor='end')
    d.text(ox + w, ey0 + 14, 'k (Å⁻¹)', size=7, anchor='end')
    for k in (1, 2):
        d.text(X(k), ey0 + 14, str(k), size=7)
    d.text(ox - 6, Y2(20) + 3, '20 K', size=7, anchor='end')
    d.text(ox - 6, Y2(40) + 3, '40 K', size=7, anchor='end')
    return d


def weak_force():
    """The Wu experiment and its mirror image: cobalt-60 nuclei spin-aligned by a coil, electrons emitted against the spin."""
    d = D()
    mx = 200
    a = 0.6   # the asymmetry, electrons favour the direction opposite the nuclear spin (illustrative)
    def lobe(cx, cy, sgn, R=58):
        pts = []
        for i in range(181):
            th = 2 * math.pi * i / 180
            rr = R * (1 - a * math.cos(th)) / (1 + a)
            # th measured from the spin direction, sgn = +1 spin up
            pts.append((cx + rr * math.sin(th), cy - sgn * rr * math.cos(th)))
        return pts
    L, R_ = (100, 150), (300, 150)
    # construction: the mirror, the spin axes, the reference circle of an isotropic source
    d.group('thin')
    d.lines([[(mx, 12 + 12 * i), (mx, 18 + 12 * i)] for i in range(22)])
    d.line((L[0], 40), (L[0], 262))
    d.line((R_[0], 40), (R_[0], 262))
    d.circle(*L, 58 / (1 + a) * 1.0)
    d.circle(*R_, 58 / (1 + a) * 1.0)
    # the coils: current loops seen in perspective
    d.group()
    for cx, cy in (L, R_):
        d.ellipse(cx, cy + 4, 46, 11)
        d.ellipse(cx, cy - 4, 46, 11)
        d.circle(cx, cy, 5)
    # the emission patterns: both lobes point down, because a mirror parallel to the spin axis leaves up and down alone
    d.group('mid')
    d.line(*lobe(*L, +1))
    d.line(*lobe(*R_, +1))
    # the spins: up on the left; in the mirror the current runs the other way, so the spin points down
    d.group()
    d.line((L[0], L[1] - 8), (L[0], L[1] - 44))
    _arrow(d, L[0], L[1] - 44, -math.pi / 2, 7)
    d.line((R_[0], R_[1] + 8), (R_[0], R_[1] + 44))
    _arrow(d, R_[0], R_[1] + 44, math.pi / 2, 7)
    # current arrows on the front of each coil, opposite senses
    _arrow(d, L[0] + 10, L[1] + 15, 0, 5)
    _arrow(d, R_[0] - 10, R_[1] + 15, math.pi, 5)
    # electrons, drawn as short rays in the favoured direction
    d.group('mid')
    for cx, cy in (L, R_):
        d.lines([[(cx + 70 * math.sin(t), cy + 70 * math.cos(t)), (cx + 84 * math.sin(t), cy + 84 * math.cos(t))]
                 for t in (-0.35, 0, 0.35)])
    d.group()
    d.text(L[0], 24, 'THE EXPERIMENT', size=8)
    d.text(R_[0], 24, 'ITS MIRROR IMAGE', size=8)
    d.text(L[0] + 8, L[1] - 50, 'SPIN', size=7, anchor='start')
    d.text(R_[0] + 8, R_[1] + 52, 'SPIN', size=7, anchor='start')
    d.text(L[0] - 10, 262, 'e⁻', size=8, anchor='end')
    d.text(R_[0] - 10, 262, 'e⁻', size=8, anchor='end')
    d.text(mx, 290, '⁶⁰Co · 0.01 K · ELECTRONS AGAINST THE SPIN', size=7)
    return d


def plenty_of_room():
    """A scale of lengths on a logarithmic axis, from a pinhead down to an atom, with Feynman's numbers on it."""
    d = D()
    ox, w, ay = 26, 344, 150
    top, bot = -2.5, -10         # log10 metres at the left and right ends
    X = lambda lg: ox + w * (top - lg) / (top - bot)
    items = [
        ('PINHEAD', 1.5875e-3, '1/16 IN'),
        ('MOTOR', 3.97e-4, '1/64 IN'),
        ('ALL BOOKS', 1.27e-4, '1/200 IN'),
        ('A PAGE ÷ 25,000', 6.1e-6, '≈ 6 µm'),
        ('HALFTONE DOT', 8e-9, '80 Å'),
        ('ATOM', 2.5e-10, '≈ 2.5 Å'),
    ]
    side = lambda i: -1 if i % 2 == 0 else 1     # above the axis, then below
    ypos = lambda i: ay - 112 if i == 2 else ay + side(i) * 58   # where each object sits
    # construction: decades, minor ticks, and a leader from each mark to its object
    d.group('thin')
    d.lines([[(X(lg), ay - 7), (X(lg), ay + 7)] for lg in range(bot, -2)])
    d.lines([[(X(lg + math.log10(m)), ay - 3), (X(lg + math.log10(m)), ay + 3)]
             for lg in range(bot, -3) for m in range(2, 10)])
    ox2 = 50                                    # the books' cube stands off to the right, out of the crowd
    for i, (_, s, _) in enumerate(items):
        x = X(math.log10(s))
        if i == 2:
            d.line((x, ay), (x, ay - 10), (x + ox2, ypos(i) + 12))
        else:
            d.line((x, ay), (x, ypos(i) - side(i) * 22))
    # the axis
    d.group()
    d.line((ox, ay), (ox + w, ay))
    _arrow(d, ox + w, ay, 0, 5)
    for i, (_, s, _) in enumerate(items):
        d.circle(X(math.log10(s)), ay, 2.2)
    # the objects: a pin, two cubes, a page, a dot, a row of atoms
    d.group('mid')
    x, y = X(math.log10(items[0][1])), ypos(0)
    d.circle(x, y - 6, 12)
    d.line((x - 1.2, y + 6), (x - 1.2, y + 24))
    d.line((x + 1.2, y + 6), (x + 1.2, y + 24))
    for j, s in ((1, 16), (2, 9)):
        x, y = X(math.log10(items[j][1])) + (ox2 if j == 2 else 0), ypos(j) - s / 2
        d.line((x - s / 2, y), (x + s / 2, y), (x + s / 2, y + s), (x - s / 2, y + s), closed=True)
        d.line((x - s / 2, y), (x - s / 2 + s * 0.4, y - s * 0.3), (x + s / 2 + s * 0.4, y - s * 0.3), (x + s / 2, y))
        d.line((x + s / 2 + s * 0.4, y - s * 0.3), (x + s / 2 + s * 0.4, y + s * 0.7), (x + s / 2, y + s))
    x, y = X(math.log10(items[3][1])), ypos(3) - 12
    d.line((x - 8, y), (x + 8, y), (x + 8, y + 24), (x - 8, y + 24), closed=True)
    d.lines([[(x - 5, y + 5 + 3 * i), (x + 5 - (3 if i % 3 == 2 else 0), y + 5 + 3 * i)] for i in range(6)])
    x, y = X(math.log10(items[4][1])), ypos(4)
    d.circle(x, y, 7)
    x, y = X(math.log10(items[5][1])), ypos(5)
    for i in range(3):
        d.circle(x - 14 + 7 * i, y, 3.4)
    # labels: the name beyond the object, the size beyond the name
    d.group()
    for i, (name, s, dim) in enumerate(items):
        x = X(math.log10(s))
        if i in (0, 2):                   # crowded at the left: labels beside the object
            bx, by = x + (16 if i == 0 else 14 + ox2), ypos(i) - (4 if i == 0 else 2)
            d.text(bx, by, name, size=7, anchor='start')
            d.text(bx, by + 11, dim, size=7, anchor='start')
            continue
        anchor = 'end' if i == 5 else 'middle'
        dx = 6 if i == 5 else 0
        yn = ypos(i) + side(i) * 38
        d.text(x + dx, yn + (3 if side(i) > 0 else 0), name, size=7, anchor=anchor)
        d.text(x + dx, yn + side(i) * 12 + (3 if side(i) > 0 else 0), dim, size=7, anchor=anchor)
    for lg, lab in ((-3, '1 mm'), (-6, '1 µm'), (-9, '1 nm')):
        d.text(X(lg) + 4, ay + 18, lab, size=7, anchor='start')
    d.text(200, 293, 'LOG SCALE · TICKS AT EACH POWER OF TEN', size=7)
    return d


PLATES = {
    'caltech': caltech,
    'brazil': brazil,
    'superfluid-helium': superfluid_helium,
    'weak-force': weak_force,
    'plenty-of-room': plenty_of_room,
}
