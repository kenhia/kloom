"""Plates for The Story of Life's part beagle1 (sprint 055): the voyage, Punta Alta, the Galápagos.
See plates_for.py. Coastlines and island outlines are coarse, entered by hand from approximate
coordinates; the route and the ports are placed by their latitude and longitude."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _densify(pts, n=8):
    out = []
    for (a, b), (c, e) in zip(pts, pts[1:]):
        for i in range(n):
            out.append((a + (c - a) * i / n, b + (e - b) * i / n))
    out.append(pts[-1])
    return out


SAMERICA = [(12, -72), (10, -62), (5, -52), (-2, -44), (-5, -35), (-8, -35), (-13, -38), (-23, -42),
            (-28, -48), (-34, -53), (-36, -57), (-39, -62), (-41, -63), (-42, -64), (-47, -66), (-50, -68.5),
            (-52.4, -68.4), (-54, -66), (-55, -66.5), (-55.5, -68), (-55, -71), (-53, -74), (-50, -75.5),
            (-46, -75), (-44, -73.5), (-42, -74), (-38, -73.5), (-30, -71.5), (-18, -70.3), (-14, -76.3),
            (-5, -81), (1, -80), (7, -78), (9, -76)]
FALKLANDS = [(-51.2, -61), (-51.4, -58), (-52.1, -58.4), (-52.3, -60), (-51.8, -61.2)]
CHILOE = [(-41.8, -73.9), (-42.3, -73.4), (-43.3, -73.7), (-42.6, -74.2)]


def beagle_voyage():
    d = D()
    # Above, the world on a plain latitude-longitude grid, 1 px to the degree, from 160° W to 200° E so
    # that only the Pacific crossing runs off one edge and on at the other. Coastlines are coarse,
    # entered by hand; ports are placed by latitude and longitude. Below, the same five years as a
    # time line, day by day, cut where the itinerary in Darwin's ornithological notes puts the ship.
    w0, wlon, wlat, ws, top = 20, -160.0, 60.0, 1.0, 28

    def wp(lat, lon):
        return (w0 + (lon - wlon) * ws, top + (wlat - lat) * ws)

    def seg(coords, closed=False, n=6):
        pts = list(coords) + ([coords[0]] if closed else [])
        return [wp(*q) for q in _densify(pts, n)]

    d.group('thin')
    for lo in range(-150, 200, 30):
        d.line(wp(wlat, lo), wp(-60, lo))
    for la in (30, -30):
        d.line(wp(la, wlon), wp(la, 200))

    d.group()
    x0, y0 = wp(wlat, wlon)
    x1, y1 = wp(-60, 200)
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)
    d.line(wp(0, wlon), wp(0, 200))

    d.group('mid')
    namerica = [(9, -76), (15, -83), (18, -88), (21, -87), (21, -90), (19, -96), (26, -97), (30, -89),
                (30, -84), (25, -81), (30, -81), (35, -76), (41, -72), (45, -66), (47, -60), (52, -56), (60, -64)]
    pacific_na = [(9, -79), (8, -83), (13, -88), (16, -95), (20, -105), (23, -110), (32, -117), (40, -124),
                  (48, -125), (58, -136), (60, -147)]
    africa = [(35, -6), (37, 10), (32, 20), (31, 32), (22, 37), (12, 44), (11, 51), (2, 45), (-5, 39),
              (-15, 40), (-25, 35), (-34, 26), (-34, 18), (-28, 15), (-17, 12), (-9, 13), (-1, 9), (4, 7),
              (5, -2), (4, -8), (8, -13), (13, -17), (21, -17), (28, -13), (33, -9)]
    europe = [(36, -9), (43, -9), (44, -1), (48, -5), (51, 2), (54, 8), (57, 8), (59, 11), (60, 5)]
    britain = [(50, -5.7), (50.8, 0), (51.4, 1.4), (53, 1.7), (57.5, -1.8), (58.6, -3), (58.5, -5),
               (56, -5.5), (54.5, -3.4), (53.3, -4.6), (51.7, -5.2), (51.4, -3.2)]
    asia = [(31, 32), (36, 36), (37, 27), (41, 29), (41, 41), (31, 48), (26, 56), (24, 67), (20, 73),
            (8, 77), (13, 80), (21, 87), (16, 95), (10, 98), (1, 104), (10, 106), (21, 108), (30, 122),
            (40, 122), (39, 128), (45, 135), (55, 137), (60, 150)]
    australia = [(-11, 142), (-17, 140), (-12, 136), (-12, 131), (-15, 129), (-14, 126), (-20, 119),
                 (-22, 114), (-26, 113), (-32, 115), (-35, 117), (-34, 123), (-32, 128), (-32, 133),
                 (-35, 136), (-38, 140), (-39, 146), (-37, 150), (-33, 152), (-28, 153), (-24, 152),
                 (-19, 147), (-15, 145)]
    tasmania = [(-41, 145), (-41, 148), (-43.5, 147), (-43.5, 146)]
    nz_n = [(-34.5, 172.7), (-37, 175.5), (-37.6, 178.5), (-41.5, 175.2), (-39.5, 174)]
    nz_s = [(-40.5, 173), (-41.6, 174.3), (-44, 173), (-46.6, 169), (-46, 166.5), (-43, 170.2)]
    madagascar = [(-12, 49.3), (-16, 50.3), (-25, 47.1), (-25, 44), (-16, 44.4)]
    borneo = [(7, 117), (1, 119), (-4, 116), (-3, 111), (1, 109), (4, 114)]
    sumatra = [(5.5, 95.3), (-3, 102), (-6, 105.8), (-4, 103), (2, 98)]
    segs = []
    for c, closed in ((SAMERICA, False), (namerica, False), (pacific_na, False), (africa, True),
                      (europe, False), (britain, True), (asia, False), (australia, True), (tasmania, True),
                      (nz_n, True), (nz_s, True), (madagascar, True), (borneo, True), (sumatra, True),
                      (FALKLANDS, True)):
        segs.append(seg(c, closed))
    d.lines(segs)

    d.group()
    P = {'plymouth': (50.4, -4.1), 'praya': (14.9, -23.5), 'bahia': (-13.0, -38.5), 'rio': (-22.9, -43.2),
         'montevideo': (-34.9, -56.2), 'bahia-blanca': (-38.8, -62.3), 'fuego': (-55.1, -68.2),
         'falklands': (-51.6, -58.0), 'valparaiso': (-33.0, -71.8), 'callao': (-12.1, -77.3),
         'galapagos': (-0.9, -89.6), 'tahiti': (-17.5, -149.6), 'new-zealand': (-35.2, 174.1),
         'sydney': (-33.9, 151.2), 'hobart': (-42.9, 147.3), 'king-george': (-35.0, 117.9),
         'keeling': (-12.1, 96.9), 'mauritius': (-20.2, 57.5), 'cape': (-34.2, 18.4),
         'st-helena': (-15.9, -5.7), 'ascension': (-7.9, -14.4), 'azores': (38.6, -27.2), 'falmouth': (50.2, -5.1)}
    out = [P['plymouth'], (28, -19), P['praya'], P['bahia'], P['rio'], P['montevideo'], P['bahia-blanca'],
           (-50, -64), P['fuego'], P['falklands'], (-57, -66), (-50, -77), (-40, -75.5), P['valparaiso'],
           P['callao'], P['galapagos'], P['tahiti'], (-26, -160)]
    back = [(-30, 200), P['new-zealand'], P['sydney'], P['hobart'], (-40, 131), P['king-george'], P['keeling'],
            P['mauritius'], (-36, 30), P['cape'], P['st-helena'], P['ascension'], P['bahia'], (-4, -33),
            P['azores'], P['falmouth']]
    d.lines([seg(out), seg(back)])

    d.group('mid')
    for k, (la, lo) in P.items():
        if k != 'falmouth':
            d.circle(*wp(la, lo), 1.6)

    # the time line: day 0 is December 27, 1831, the last is October 2, 1836
    from datetime import date
    t0, t1 = date(1831, 12, 27), date(1836, 10, 2)
    tl, tr, ty = 20, 380, 222

    def tx(y, m_, dd):
        return tl + (tr - tl) * (date(y, m_, dd) - t0).days / (t1 - t0).days

    cuts = [(1832, 2, 28), (1834, 6, 28), (1835, 9, 15), (1835, 10, 20)]
    d.group('thin')
    for yr in range(1832, 1837):
        x = tx(yr, 1, 1)
        d.line((x, ty + 10), (x, ty + 16))
    d.group()
    d.line((tl, ty - 8), (tr, ty - 8), (tr, ty + 8), (tl, ty + 8), closed=True)
    for c in cuts:
        x = tx(*c)
        d.line((x, ty - 8), (x, ty + 8))
    d.group('mid')
    for yr in range(1832, 1837):
        d.text(tx(yr, 1, 1), ty + 25, str(yr), size=7)
    spans = [((1831, 12, 27), (1832, 2, 28), 'ATLANTIC', -22), ((1832, 2, 28), (1834, 6, 28), 'EAST COAST AND TIERRA DEL FUEGO', -14),
             ((1834, 6, 28), (1835, 9, 15), 'CHILE AND PERU', -14), ((1835, 9, 15), (1835, 10, 20), 'GALÁPAGOS', -22),
             ((1835, 10, 20), (1836, 10, 2), 'HOME, WESTWARD', -14)]
    for a, b, s_, dy in spans:
        xm = (tx(*a) + tx(*b)) / 2
        d.text(xm, ty + dy, s_, size=7)
    d.group('mid')
    def wl(k, dx, dy, s, anchor='start'):
        x, y = wp(*P[k])
        d.text(x + dx, y + dy, s, size=7, anchor=anchor)
    wl('plymouth', -5, 2, 'PLYMOUTH', anchor='end')
    wl('tahiti', 3, 12, 'TAHITI')
    wl('sydney', -4, -5, 'SYDNEY', anchor='end')
    wl('cape', 0, 11, 'CAPE TOWN', anchor='middle')
    wl('galapagos', -4, -5, 'GALÁPAGOS', anchor='end')
    wl('bahia-blanca', 6, 2, 'PUNTA ALTA')
    d.text(*wp(2, 197), 'EQUATOR', size=7, anchor='end')
    d.text(200, 292, 'THE BEAGLE · DECEMBER 1831 TO OCTOBER 1836', size=7)
    return d


def _bone(d, p, q, w):
    """A long bone: a shaft of width w between two knuckled ends."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
    d.line((p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny))
    d.line((p[0] - nx, p[1] - ny), (q[0] - nx, q[1] - ny))
    d.circle(p[0], p[1], w * 0.6)
    d.circle(q[0], q[1], w * 0.55)


def patagonia_fossils():
    d = D()
    # Megatherium americanum, about 6 m from snout to tail, standing on all fours as the Madrid
    # skeleton was mounted, beside a three-toed sloth (head and body about 45 cm) hanging from a
    # branch, both at one scale: 46 px to the meter. The skeleton is schematic: spine, ribs,
    # limb bones and skull placed by eye on that scale, not traced from a specimen.
    s, gx, gy = 46.0, 30, 236

    def m(x, y):
        return (gx + x * s, gy - y * s)

    d.group('thin')
    d.line(m(-0.3, 0), m(7.5, 0))                                         # ground
    for k in range(0, 7):                                                # meter lines
        d.line(m(k, 0), m(k, 3.2))
    for h in (1, 2, 3):
        d.line(m(-0.3, h), m(-0.1, h))
    d.line(m(0, 3.75), m(6, 3.75))                                       # dimension line, 6 m
    _arrow(d, m(3, 3.75), m(0, 3.75), size=4)
    _arrow(d, m(3, 3.75), m(6, 3.75), size=4)

    d.group()
    # the spine, from the back of the skull over the shoulders and hips into the tail
    spine = [(0.85, 1.55), (1.2, 1.75), (1.6, 1.9), (2.2, 1.92), (2.8, 1.9), (3.3, 2.0), (3.75, 2.05),
             (4.2, 1.85), (4.8, 1.5), (5.4, 1.0), (6.0, 0.42)]
    d.curve('M' + ' L'.join(f'{m(*p)[0]:.1f} {m(*p)[1]:.1f}' for p in spine))
    # skull and jaw
    sk = [(0.0, 1.3), (0.15, 1.5), (0.55, 1.62), (0.85, 1.55), (0.8, 1.3), (0.5, 1.1), (0.25, 1.05), (0.05, 1.15)]
    d.line(*[m(*p) for p in sk], closed=True)
    d.line(m(0.15, 1.08), m(0.35, 0.82), m(0.62, 0.9), m(0.75, 1.15))       # the deep lower jaw
    # ribs, hanging from the spine
    for i in range(9):
        x = 1.55 + i * 0.2
        top = 1.86 + (0.04 if i > 6 else 0)
        L = 1.0 - abs(i - 3.5) * 0.08
        d.curve(f"M{m(x, top)[0]:.1f},{m(x, top)[1]:.1f} Q{m(x - 0.25, top - L * 0.5)[0]:.1f},"
                f"{m(x - 0.25, top - L * 0.5)[1]:.1f} {m(x + 0.05, top - L)[0]:.1f},{m(x + 0.05, top - L)[1]:.1f}")
    # pelvis
    d.ellipse(*m(3.7, 1.75), 0.48 * s, 0.38 * s)
    # forelimb and hindlimb, with the great claws curled under
    _bone(d, m(1.55, 1.55), m(1.4, 0.85), 0.16 * s)
    _bone(d, m(1.4, 0.85), m(1.5, 0.18), 0.13 * s)
    _bone(d, m(3.6, 1.5), m(3.45, 0.85), 0.24 * s)
    _bone(d, m(3.45, 0.85), m(3.55, 0.18), 0.18 * s)

    d.group('mid')
    for x0 in (1.5, 3.55):                                               # feet and claws
        d.line(m(x0 - 0.35, 0), m(x0 + 0.25, 0))
        for k in range(3):
            cx_, cy_ = m(x0 - 0.3 + k * 0.12, 0.12)
            d.arc(cx_, cy_, 0.09 * s, 90, 250, n=12)
    for i in range(14):                                                  # vertebrae along the tail
        t = i / 13
        x = 4.15 + t * 1.8
        y = 1.85 - t * 1.35 - 0.12 * math.sin(t * math.pi)
        d.circle(*m(x, y), (0.1 - 0.06 * t) * s)
    d.circle(*m(0.5, 1.35), 0.08 * s)                                    # the orbit
    # the three-toed sloth, hanging under a branch at 1.2 m, 0.45 m head and body
    bx0, bx1, by = 6.35, 7.35, 1.2
    d.line(m(bx0, by), m(bx1, by))
    d.line(m(7.3, by), m(7.3, 0))                                        # the trunk it hangs from
    scx, scy = 6.85, by - 0.17
    d.ellipse(*m(scx, scy), 0.22 * s, 0.08 * s)
    d.circle(*m(scx - 0.27, scy + 0.01), 0.055 * s)
    for dx in (-0.15, -0.05, 0.08, 0.18):
        d.line(m(scx + dx, scy + 0.04), m(scx + dx + 0.02, by))

    d.group('mid')
    d.text(*m(3.0, 3.95), '6 M', size=7)
    d.text(*m(1.6, -0.35), 'MEGATHERIUM AMERICANUM', size=7)
    d.text(*m(6.85, -0.35), 'THREE-TOED SLOTH', size=7)
    d.text(*m(6.85, 0.62), '0.45 M', size=7)
    for h in (1, 2, 3):
        d.text(m(-0.35, h)[0], m(-0.35, h)[1] + 2.5, f'{h}', size=7, anchor='end')
    d.text(200, 290, 'ONE SCALE · METERS', size=7)
    return d


def galapagos():
    d = D()
    # The central and southern Galápagos on a plain latitude-longitude grid (110 px to the degree),
    # with the four islands where Darwin landed and the number of the mockingbird he took on each,
    # from his ornithological notes. Island outlines are coarse polygons from approximate
    # coordinates; the dashed track is the order of his landings, September 17 to October 17, 1835.
    k, lon_w, lat_n, ox, oy = 110.0, -92.0, 0.45, 40, 40

    def p(lat, lon):
        return (ox + (lon - lon_w) * k, oy + (lat_n - lat) * k)

    def ell(lat, lon, rlon, rlat, rot=0.0, n=24):
        c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        out = []
        for i in range(n):
            t = 2 * math.pi * i / n
            x, y = rlon * math.cos(t), rlat * math.sin(t)
            out.append(p(lat + x * s_ + y * c, lon + x * c - y * s_))
        return out

    d.group('thin')
    for lo in (-91.5, -91.0, -90.5, -90.0, -89.5):
        d.line(p(lat_n, lo), p(-1.6, lo))
    for la in (-0.5, -1.0, -1.5):
        d.line(p(la, lon_w), p(la, -89.2))

    d.group()
    d.line(p(0, lon_w), p(0, -89.2))                                     # the equator
    isabela = [(0.17, -91.33), (0.05, -91.20), (-0.15, -91.10), (-0.35, -90.98), (-0.55, -90.88),
               (-0.75, -90.82), (-0.93, -90.88), (-0.98, -91.05), (-1.02, -91.25), (-0.97, -91.45),
               (-0.85, -91.50), (-0.70, -91.34), (-0.55, -91.25), (-0.40, -91.24), (-0.27, -91.37),
               (-0.12, -91.50), (-0.03, -91.62), (0.05, -91.55), (0.12, -91.45)]
    d.line(*[p(*q) for q in isabela], closed=True)                       # Albemarle (Isabela)
    d.line(*ell(-1.28, -90.43, 0.11, 0.09), closed=True)                 # Charles (Floreana)
    d.line(*ell(-0.83, -89.47, 0.27, 0.09, rot=35), closed=True)         # Chatham (San Cristóbal)
    d.line(*ell(-0.23, -90.74, 0.17, 0.12, rot=-20), closed=True)        # James (Santiago)

    d.group('mid')
    d.line(*ell(-0.37, -91.55, 0.13, 0.13), closed=True)                 # Fernandina
    d.line(*ell(-0.63, -90.37, 0.2, 0.16), closed=True)                  # Santa Cruz
    d.line(*ell(-1.38, -89.70, 0.11, 0.045, rot=-10), closed=True)       # Española
    d.line(*ell(-0.60, -90.67, 0.04, 0.035), closed=True)                # Pinzón
    d.circle(*p(-0.42, -90.37), 2.2)                                     # Daphne Major
    track = [(-0.92, -89.62), (-1.18, -89.95), (-1.22, -90.43), (-1.12, -90.95), (-1.12, -91.45),
             (-0.95, -91.62), (-0.62, -91.40), (-0.30, -91.40), (-0.22, -91.55), (-0.10, -91.78),
             (0.22, -91.70), (0.30, -91.15), (0.10, -90.85), (-0.15, -90.80)]
    d.dashed(*[p(*q) for q in track], dash=4, gap=3)

    d.group('mid')
    for la, lo in ((-0.90, -89.62), (-1.24, -90.48), (-0.27, -91.37), (-0.17, -90.82)):
        d.circle(*p(la, lo), 3)
    def t(la, lo, s_, dx=0, dy=0, anchor='middle'):
        x, y = p(la, lo)
        d.text(x + dx, y + dy, s_, size=7, anchor=anchor)
    t(-0.90, -89.62, 'CHATHAM 3307', -6, -8, 'end')
    t(-1.24, -90.48, 'CHARLES 3306', -8, 12, 'end')
    t(-0.27, -91.37, '3349', 6, 3, 'start')
    t(-0.77, -91.12, 'ALBEMARLE')
    t(-0.17, -90.82, 'JAMES 3350', 32, -2, 'start')
    t(-0.42, -90.37, 'DAPHNE MAJOR', 6, 2.5, 'start')
    t(0, -89.25, 'EQUATOR', 0, -4, 'end')
    d.text(200, 290, "DARWIN'S MOCKINGBIRDS BY ISLAND · 1835", size=7)
    return d


PLATES = {'beagle-voyage': beagle_voyage, 'patagonia-fossils': patagonia_fossils, 'galapagos': galapagos}
