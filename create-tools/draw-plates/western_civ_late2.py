"""Plates for western-civ's part late2 (sprint 049): the fall of the West and Justinian. See plates_for.py."""
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


def fall_of_the_west():
    d = D()
    # Two lines of emperors on one time scale, AD 380-570: the West ends in 476 (Romulus Augustulus),
    # with Julius Nepos holding Dalmatia until 480; the East goes on. The regalia go east in 476,
    # and Justinian's armies come back west: Africa 533-534, Italy 535-554.
    y0, y1 = 380, 570
    x0, x1 = 34, 376

    def X(year):
        return x0 + (x1 - x0) * (year - y0) / (y1 - y0)

    west, east, axis = 112, 196, 250
    band = 7                                                              # half-height of a reign band

    d.group('thin')
    d.line((x0, axis), (x1, axis))                                        # the time scale
    for yr in range(400, 571, 25):
        d.line((X(yr), axis - 4), (X(yr), axis + 4))
        d.line((X(yr), 52), (X(yr), axis - 8))                            # a faint grid of quarter-centuries
    for yr in (410, 476):                                                 # the two dates, carried down
        d.line((X(yr), west + band + 2), (X(yr), axis))

    d.group()
    # the West: a band from 395 (the division under Theodosius' sons) to 476
    _box(d, X(395), west - band, X(476) - X(395), 2 * band)
    d.line((X(476), west), (X(480), west))                                # Nepos in Dalmatia, 476-480
    # the East: a band from 395 that runs on off the scale
    d.line((X(395), east - band), (x1, east - band))
    d.line((X(395), east + band), (x1, east + band))
    d.line((X(395), east - band), (X(395), east + band))
    _arrow(d, (x1 - 10, east), (x1 + 4, east), size=6)

    d.group('mid')
    # 476: the regalia sent east
    _arrow(d, (X(476), west + band), (X(476) + 10, east - band - 2))
    d.line((X(476), west + band), (X(476) + 10, east - band - 2))
    # Justinian's reconquest, Africa 533-534 and Italy 535-554: one arrow back up to the West's line
    d.line((X(533), east - band), (X(533), west + band + 4))
    _arrow(d, (X(533), east - band), (X(533), west + band + 4))
    d.line((X(533), west + band + 4), (X(554), west + band + 4))
    d.line((X(554), west + band + 1), (X(554), west + band + 7))
    # 410 marked on the West's band
    d.line((X(410), west - band - 6), (X(410), west + band))
    # Augustine writing the City of God, 413-426, as a bracket above the West
    d.line((X(413), 70), (X(413), 64), (X(426), 64), (X(426), 70))

    d.group('mid')
    d.text(x0, west - 12, 'WEST', size=7, anchor='start')
    d.text(x0, east - 12, 'EAST', size=7, anchor='start')
    d.text((X(413) + X(426)) / 2, 58, 'CITY OF GOD', size=7)
    d.text(X(410), west - band - 10, '410', size=7)
    d.text(X(480) + 4, west + 3, '480 NEPOS', size=7, anchor='start')
    d.text(X(476) + 14, (west + east) / 2 + 12, 'REGALIA', size=7, anchor='start')
    d.text((X(533) + X(554)) / 2, west + band - 2, 'RECONQUEST', size=7)
    d.text(X(560), east + 20, 'CONSTANTINOPLE', size=7)
    for yr in range(400, 571, 50):
        d.text(X(yr), axis + 16, str(yr), size=7)
    d.text(X(476), axis + 16, '476', size=7)
    d.text(X(533), axis + 16, '533', size=7)
    return d


def justinian():
    d = D()
    # Hagia Sophia's dome on pendentives. Left: a north-south section through the center, to scale
    # (Wikipedia, Hagia Sophia rev. 2026-10: the dome about 31 m across, its crown 55.6 m above the
    # floor since Isidore the Younger raised it 6.25 m in 558-562). The bay is a square of side a = 31 m;
    # its four arches spring at the impost h0 and rise a/2 to their crowns, where the 40-windowed dome
    # sits. The pendentives are what is left of one sphere of radius a/sqrt(2), centered on the bay at
    # the impost, after the four vertical planes of the square's sides have cut it (Procopius' "four
    # triangles"). Right: the same bay in plan, with the pendentives' horizontal courses as arcs.
    a = 31.0
    R = a / math.sqrt(2)
    crown = 41.0                                                          # arch crowns, m (dome base)
    h0 = crown - a / 2                                                    # the impost
    top = 55.6
    f_now, f_old = top - crown, top - 6.25 - crown                        # rise of the dome, now and in 537
    s = 3.6                                                               # px per meter
    cx, gy = 122, 272                                                     # section's axis and floor

    def P(x, y):
        return (cx + x * s, gy - y * s)

    def cap(f):                                                           # a dome of rise f on radius a/2
        rho = ((a / 2) ** 2 + f ** 2) / (2 * f)
        c = crown + f - rho
        return rho, c

    d.group('thin')
    # the pendentive sphere, whole, and its center; the impost and crown levels; the axis
    d.circle(*P(0, h0), R * s)
    d.line(P(-a / 2 - 9, h0), P(a / 2 + 9, h0))
    d.line(P(-a / 2 - 9, crown), P(a / 2 + 9, crown))
    d.line(P(0, -1.5), P(0, top + 4))
    d.line(P(0, h0), P(a / 2 * math.cos(math.radians(30)), h0 + a / 2 * math.sin(math.radians(30))))
    # the dome of 537, flatter by 6.25 m, which fell in 558
    rho, c = cap(f_old)
    p0 = math.degrees(math.acos((crown - c) / rho))
    d.arc(*P(0, c), rho * s, -90 - p0, -90 + p0)
    # dimension of the height
    d.line(P(-a / 2 - 11, 0), P(-a / 2 - 11, top))
    for y in (0, top):
        d.line(P(-a / 2 - 13, y), P(-a / 2 - 9, y))

    d.group()
    pw = 4.5                                                              # piers, schematically
    d.line(P(-a / 2 - 10, 0), P(a / 2 + 10, 0))                           # the floor
    for sx in (-1, 1):
        x_in, x_out = sx * a / 2, sx * (a / 2 + pw)
        d.line(P(x_in, 0), P(x_in, h0), P(x_out, h0), P(x_out, 0))
    d.arc(*P(0, h0), a / 2 * s, 180, 360)                                 # the arch in the section's far wall
    d.arc(*P(0, h0), (a / 2 + 2) * s, 180, 360)
    rho, c = cap(f_now)                                                   # the dome since 562
    p0 = math.degrees(math.acos((crown - c) / rho))
    d.arc(*P(0, c), rho * s, -90 - p0, -90 + p0)
    d.line(P(-a / 2 - 2, crown), P(a / 2 + 2, crown))

    d.group('mid')
    # the ribs of the dome, 40 of them, as meridians seen in elevation (the near half: 20)
    phimax = math.acos((crown - c) / rho)
    for k in range(20):
        th = math.pi * (k + 0.5) / 20
        pts = []
        for i in range(13):
            ph = phimax * i / 12
            pts.append(P(rho * math.sin(ph) * math.cos(th), c + rho * math.cos(ph)))
        d.line(*pts)
    # the windows between the ribs at the dome's foot
    for k in range(20):
        th = math.pi * k / 20
        x = (a / 2) * math.cos(th)
        d.line(P(x, crown + 0.4), P(x, crown + 2.2))

    d.group()
    # the plan: the square bay, the dome's circle inscribed, the pendentive sphere circumscribed
    q = 3.6
    px, py = 312, 150

    def Q(x, y):
        return (px + x * q, py - y * q)

    h = a / 2
    d.line(Q(-h, -h), Q(h, -h), Q(h, h), Q(-h, h), closed=True)
    d.circle(px, py, h * q)
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):                   # the piers at the corners
        _box(d, *Q(sx * h - (pw if sx < 0 else 0), sy * h + (0 if sy < 0 else pw)), pw * q, pw * q)

    d.group('thin')
    d.circle(px, py, R * q)
    d.line(Q(-h, -h), Q(h, h))
    d.line(Q(-h, h), Q(h, -h))

    d.group('mid')
    # the pendentives' horizontal courses: circles of the sphere between radius a/2 and a/sqrt(2),
    # kept where they lie inside the square, so near each corner
    for i in range(1, 6):
        r = h + (R - h) * i / 6
        lo = math.degrees(math.acos(h / r))
        hi = 90 - lo
        for quad in range(4):
            a0, a1 = quad * 90 + lo, quad * 90 + hi
            d.arc(px, py, r * q, a0, a1, n=12)

    d.group('mid')
    d.text(*P(-a / 2 - 12, top + 2.5), '55.6 M', size=7, anchor='start')
    d.text(*P(0, top + 6), '562', size=7)
    d.text(*P(a / 2 + 6, crown + 4.5), '537', size=7, anchor='start')
    d.text(*P(0, -4), 'SECTION · BAY 31 M', size=7)
    d.text(px, py + R * q + 14, 'PLAN · R = A/√2', size=7)
    d.text(px, py - R * q - 8, 'FOUR PENDENTIVES', size=7)
    return d


PLATES = {'fall-of-the-west': fall_of_the_west, 'justinian': justinian}
