"""Plates for Sound and Score's part voice1 (sprint 058): the castrati, Jenny Lind's tour, García's laryngoscope.
See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def _glottis(d, cx, top, length, spread=0.36, width=0.13):
    """Vocal folds seen from above, as in a laryngeal mirror: the front (anterior commissure) at the
    top, the folds diverging to the arytenoids at the back. `length` in px; `spread` is the half-angle
    of the open glottis in radians; `width` the fold's thickness as a fraction of its length."""
    a = (cx, top)
    folds = []
    for s in (-1, 1):
        ang = math.pi / 2 + s * spread              # downward, opened by the spread
        tip = (cx + length * math.cos(ang), top + length * math.sin(ang))
        nx, ny = -math.sin(ang) * s, math.cos(ang) * s   # outward normal
        pts_in, pts_out = [], []
        for i in range(21):
            t = i / 20
            w = width * length * math.sin(math.pi * t) ** 0.7
            x = a[0] + t * (tip[0] - a[0]); y = a[1] + t * (tip[1] - a[1])
            pts_in.append((x, y))
            pts_out.append((x - nx * w, y - ny * w))
        folds.append((pts_in, pts_out, tip))
    return folds


def castrati():
    d = D()
    # Top: the vocal folds of an adult man, an adult woman and a child, seen from above as in a
    # laryngeal mirror, at 4 px a mm. Lengths are the ranges in Wikipedia's "Vocal cords" (men 17.5-25 mm,
    # women 12.5-17.5 mm, 8-16 mm by adolescence); each is drawn at its range's middle. A castrato's
    # larynx was spared puberty's growth; no castrato's has been measured, so his is not drawn as data.
    # Bottom: a keyboard from C3 to D6, with Farinelli's range as Quantz heard it in 1726 (A3 to D6)
    # and the F3 his own aria reaches.
    k = 4.0
    specs = [(70, 21.25, 'ADULT MAN', '17.5-25 MM'), (200, 15.0, 'ADULT WOMAN', '12.5-17.5 MM'),
             (330, 12.0, 'CHILD', '8-16 MM')]
    top = 40
    d.group('thin')
    for cx, mm, _, _ in specs:
        d.line((cx, top - 12), (cx, top + 25 * k + 6))                     # midline
    d.line((20, top), (380, top))                                          # the front, where the folds meet
    for mm in (5, 10, 15, 20, 25):
        y = top + mm * k * math.cos(0.36)
        d.line((16, y), (22, y))
    d.line((19, top), (19, top + 25 * k * math.cos(0.36)))

    d.group()
    for cx, mm, _, _ in specs:
        for pin, pout, tip in _glottis(d, cx, top, mm * k):
            d.line(*pin); d.line(*pout); d.line(pin[-1], pout[-1])
    d.group('mid')
    for cx, mm, _, _ in specs:
        # the ring of the larynx around the folds, a little larger than them
        L = mm * k
        d.ellipse(cx, top + L * 0.48, L * 0.62, L * 0.62)

    # the keyboard, C3 to D6: 31 white keys
    names = 'CDEFGAB'
    whites = []
    for octv in (3, 4, 5, 6):
        for n in names:
            whites.append((n, octv))
            if octv == 6 and n == 'D':
                break
        if octv == 6:
            break
    kx0, ky, kw, kh = 30, 214, 340 / len(whites), 30
    def wx(note):
        return kx0 + whites.index(note) * kw
    d.group('thin')
    for i in range(len(whites) + 1):
        d.line((kx0 + i * kw, ky), (kx0 + i * kw, ky + kh))
    d.group()
    _box(d, kx0, ky, kw * len(whites), kh)
    d.group('mid')
    for i, (n, o) in enumerate(whites[:-1]):
        if n in 'CDFGA':
            x = kx0 + (i + 1) * kw
            d.line((x - kw * 0.3, ky), (x - kw * 0.3, ky + kh * 0.6), (x + kw * 0.3, ky + kh * 0.6), (x + kw * 0.3, ky))
    # Farinelli: A3-D6 (Quantz, 1726), and down to F3 (his own aria)
    y = ky - 12
    a3, d6, f3 = wx(('A', 3)) + kw / 2, wx(('D', 6)) + kw / 2, wx(('F', 3)) + kw / 2
    d.group()
    d.line((a3, y), (d6, y))
    d.line((a3, y - 4), (a3, y + 4)); d.line((d6, y - 4), (d6, y + 4))
    d.group('mid')
    d.dashed((f3, y), (a3, y), dash=3, gap=3)
    c4 = wx(('C', 4)) + kw / 2
    d.circle(c4, ky + kh - 6, 2)

    d.group('mid')
    for cx, mm, label, rng in specs:
        d.text(cx, top + 25 * k * math.cos(0.36) + 18, label, size=7)
        d.text(cx, top + 25 * k * math.cos(0.36) + 28, rng, size=7)
    d.text(330, top + 25 * k * math.cos(0.36) + 38, "A CASTRATO'S STAYED NEAR", size=7)
    d.text(200, top - 18, 'VOCAL FOLDS FROM ABOVE · FRONT AT THE TOP · 4 PX A MM', size=7)
    d.text((a3 + d6) / 2, y - 8, 'FARINELLI · A3-D6, QUANTZ 1726 · F3 IN HIS OWN ARIA', size=7)
    d.text(c4, ky + kh + 12, 'MIDDLE C', size=7)
    d.text(kx0, ky + kh + 12, 'C3', size=7, anchor='start')
    d.text(kx0 + kw * len(whites), ky + kh + 12, 'D6', size=7, anchor='end')
    return d


CITIES = [  # (name, lon, lat, concerts under Barnum, from his recapitulation of 1869)
    ('NEW YORK', -74.01, 40.71, 35), ('BOSTON', -71.06, 42.36, 7), ('PROVIDENCE', -71.41, 41.82, 1),
    ('PHILADELPHIA', -75.16, 39.95, 8), ('BALTIMORE', -76.61, 39.29, 4), ('WASHINGTON', -77.04, 38.91, 2),
    ('RICHMOND', -77.44, 37.54, 1), ('CHARLESTON', -79.93, 32.78, 2), ('HAVANA', -82.38, 23.13, 3),
    ('NEW ORLEANS', -90.07, 29.95, 12), ('NATCHEZ', -91.40, 31.56, 1), ('MEMPHIS', -90.05, 35.15, 1),
    ('ST. LOUIS', -90.20, 38.63, 5), ('NASHVILLE', -86.78, 36.16, 2), ('LOUISVILLE', -85.76, 38.25, 3),
    ('MADISON', -85.38, 38.74, 1), ('CINCINNATI', -84.51, 39.10, 5), ('WHEELING', -80.72, 40.06, 1),
    ('PITTSBURGH', -80.00, 40.44, 1),
]


def jenny_lind():
    d = D()
    # The tour under Barnum as geometry: each city at its latitude and longitude on an equirectangular
    # grid (longitude shrunk by cos 33 degrees), a circle's area in proportion to the concerts Barnum lists
    # for it, and the route in the order of his recapitulation, back to New York and Philadelphia at the
    # end. No coastline: the grid and the cities are the map.
    lon0, lon1, lat0, lat1 = -94.0, -68.0, 21.5, 44.5
    s = 10.6
    c = math.cos(math.radians(33))
    x0, y0 = 70, 30
    def P(lon, lat):
        return (x0 + (lon - lon0) * s * c, y0 + (lat1 - lat) * s)
    d.group('thin')
    for lon in range(-90, -68, 5):
        d.line(P(lon, lat0), P(lon, lat1))
    for lat in range(25, 45, 5):
        d.line(P(lon0, lat), P(lon1, lat))
    d.group('mid')
    _box(d, *P(lon0, lat1), (lon1 - lon0) * s * c, (lat1 - lat0) * s)
    pts = {n: P(lo, la) for n, lo, la, _ in CITIES}
    order = [n for n, _, _, _ in CITIES] + ['NEW YORK', 'PHILADELPHIA']
    d.group()
    route = [pts[n] for n in order]
    d.dashed(*route, dash=3, gap=2.5)
    for n, lo, la, k in CITIES:
        r = 2.0 * math.sqrt(k)
        d.circle(*pts[n], r)
    d.group('mid')
    for n, _, _, _ in CITIES:
        d.circle(*pts[n], 0.8)
    d.group('mid')
    labels = {
        'NEW YORK': (8, 14, 'start', 'NEW YORK 35 · SEPT 1850'),
        'BOSTON': (8, -4, 'start', 'BOSTON 7'),
        'CHARLESTON': (8, 3, 'start', 'CHARLESTON 2'),
        'HAVANA': (8, 3, 'start', 'HAVANA 3 · JAN 1851'),
        'NEW ORLEANS': (10, 12, 'start', 'NEW ORLEANS 12'),
        'ST. LOUIS': (-8, -6, 'end', 'ST. LOUIS 5'),
        'CINCINNATI': (-2, -12, 'end', 'CINCINNATI 5'),
    }
    for n, (dx, dy, anc, txt) in labels.items():
        x, y = pts[n]
        d.text(x + dx, y + dy, txt, size=7, anchor=anc)
    for lon in (-90, -80, -70):
        x, y = P(lon, lat0)
        d.text(x, y + 10, f'{-lon} W', size=7)
    for lat in (25, 35):
        x, y = P(lon0, lat)
        d.text(x - 4, y + 3, f'{lat} N', size=7, anchor='end')
    d.text(200, 16, '95 CONCERTS UNDER BARNUM, 1850-51 · CIRCLE AREA BY CONCERTS', size=7)
    return d


def _reflect(v, n):
    """Reflect direction v in a mirror whose unit normal is n."""
    dot = v[0] * n[0] + v[1] * n[1]
    return (v[0] - 2 * dot * n[0], v[1] - 2 * dot * n[1])


def _unit(v):
    m = math.hypot(*v)
    return (v[0] / m, v[1] / m)


def laryngoscope():
    d = D()
    # García's self-examination in side section, schematic. Light: the sun on a hand mirror, into the
    # mouth onto the dental mirror at the uvula, down to the glottis. Image: back up from the glottis to
    # the dental mirror, out to the hand mirror, to the eye. Every reflection obeys the law of reflection,
    # computed here; the head and throat are drawn schematically.
    G = (128, 228)                     # glottis
    T = (130, 140)                     # dental mirror, against the uvula
    E = (196, 92)                      # the eye
    # hand mirror: a line through M0 at angle hm (from the x axis)
    M0, hm = (300, 125), math.radians(110)
    u = (math.cos(hm), math.sin(hm))
    nH = (-u[1], u[0])
    def refl_pt(p):                    # reflect a point across the hand mirror's line
        w = (p[0] - M0[0], p[1] - M0[1])
        dist = w[0] * nH[0] + w[1] * nH[1]
        return (p[0] - 2 * dist * nH[0], p[1] - 2 * dist * nH[1])
    def meet(p, q):                    # where segment p-q crosses the mirror's line
        w0 = (p[0] - M0[0], p[1] - M0[1]); dv = (q[0] - p[0], q[1] - p[1])
        t = -(w0[0] * nH[0] + w0[1] * nH[1]) / (dv[0] * nH[0] + dv[1] * nH[1])
        return (p[0] + t * dv[0], p[1] + t * dv[1])
    H2 = meet(T, refl_pt(E))          # where the image ray meets the hand mirror
    H1 = meet(T, (T[0] + 400 * 0.985, T[1] - 400 * 0.11))   # where the sunlight strikes it, above
    # dental mirror orientation: its normal bisects T->G and T->H2
    a, b = _unit((G[0] - T[0], G[1] - T[1])), _unit((H2[0] - T[0], H2[1] - T[1]))
    nT = _unit((a[0] + b[0], a[1] + b[1]))
    tT = (-nT[1], nT[0])
    # dental mirror orientation for the light, from H1: normal bisects T->G and T->H1 (nearly the same)
    # the sun's direction: the ray that leaves H1 toward T arrived along its reflection
    out = _unit((T[0] - H1[0], T[1] - H1[1]))
    inc = _reflect(out, nH)
    sun = (H1[0] - 150 * inc[0], H1[1] - 150 * inc[1])

    d.group('thin')
    # normals at both mirrors and the hand mirror's line extended
    d.line((T[0] - 18 * nT[0], T[1] - 18 * nT[1]), (T[0] + 22 * nT[0], T[1] + 22 * nT[1]))
    for H in (H1, H2):
        d.line((H[0] - 22 * nH[0], H[1] - 22 * nH[1]), (H[0] + 12 * nH[0], H[1] + 12 * nH[1]))
    d.line((M0[0] - 95 * u[0], M0[1] - 95 * u[1]), (M0[0] + 95 * u[0], M0[1] + 95 * u[1]))

    # the head in section, schematic: forehead, nose, lips, chin, neck; palate, tongue, pharynx, larynx
    d.group()
    face = [(150, 30), (178, 44), (192, 70), (194, 96), (214, 114), (198, 122), (200, 130),
            (186, 132), (184, 150), (200, 154), (198, 164), (184, 168), (190, 182), (176, 198),
            (150, 202), (150, 285)]
    d.line(*face)
    back = [(60, 40), (52, 100), (60, 160), (84, 200), (96, 285)]
    d.line(*back)
    d.line((150, 30), (100, 22), (60, 40))
    d.group('mid')
    d.line((184, 134), (150, 126), (128, 128), (114, 138))          # hard and soft palate to the uvula
    d.line((184, 150), (158, 156), (132, 160), (116, 176), (112, 205))  # tongue to the pharynx wall
    d.line((112, 205), (114, 220), (116, 285))                       # back of the larynx and trachea
    d.line((104, 146), (100, 200), (104, 285))                       # back wall of the pharynx
    d.line((132, 214), (138, 222), (140, 285))                       # front of the larynx
    d.line((116, 228), (126, 228)); d.line((130, 228), (140, 228))   # the vocal folds, a chink between
    d.circle(E[0] - 4, E[1], 4)                                       # the eye

    d.group()
    # the dental mirror, a small disc seen edge on, and its long handle
    m1 = (T[0] - 7 * tT[0], T[1] - 7 * tT[1]); m2 = (T[0] + 7 * tT[0], T[1] + 7 * tT[1])
    d.line(m1, m2)
    end = m2 if m2[0] > m1[0] else m1
    d.line(end, (164, 143), (240, 150))                               # the long handle, out of the mouth
    # the hand mirror
    p1 = (H1[0] - 18 * u[0], H1[1] - 18 * u[1]); p2 = (H2[0] + 14 * u[0], H2[1] + 14 * u[1])
    d.line(p1, p2)
    d.line(p2, (p2[0] + 30 * u[0], p2[1] + 30 * u[1]))                 # its grip

    d.group('mid')
    # sunlight: three parallel rays to the hand mirror, one carried on to the dental mirror and the glottis
    for off in (-8, 0, 8):
        q = (H1[0] + off * u[0], H1[1] + off * u[1])
        pstart = (q[0] - 120 * inc[0], q[1] - 120 * inc[1])
        d.line(pstart, q)
    _arrow(d, (H1[0] - 60 * inc[0], H1[1] - 60 * inc[1]), (H1[0] - 40 * inc[0], H1[1] - 40 * inc[1]), 4)
    d.line(H1, T, G)
    _arrow(d, H1, ((H1[0] + T[0]) / 2, (H1[1] + T[1]) / 2), 4)
    _arrow(d, T, ((T[0] + G[0]) / 2, (T[1] + G[1]) / 2 + 6), 4)
    # the image: glottis to dental mirror to hand mirror to the eye, dashed
    d.dashed(G, T, H2, E, dash=3, gap=2.5)
    _arrow(d, H2, ((H2[0] + E[0]) / 2, (H2[1] + E[1]) / 2), 4)

    d.group('mid')
    d.text(250, 30, 'SUNLIGHT', size=7, anchor='start')
    d.text(p2[0] + 10, p2[1] + 14, 'HAND MIRROR', size=7, anchor='start')
    d.text(226, 212, 'DENTAL MIRROR AT THE UVULA', size=7, anchor='start')
    d.text(226, 222, 'ON A LONG HANDLE', size=7, anchor='start')
    d.line((224, 210), (T[0] + 10, T[1] + 6))
    d.text(40, 240, 'GLOTTIS', size=7, anchor='start')
    d.line((76, 238), (114, 229))
    d.text(214, 84, 'EYE', size=7, anchor='start')
    d.text(200, 296, 'LIGHT SOLID · IMAGE DASHED · HEAD SCHEMATIC', size=7)
    return d


PLATES = {
    'castrati': castrati,
    'jenny-lind': jenny_lind,
    'laryngoscope': laryngoscope,
}
