"""Plates for western-civ's part mid2 (sprint 049): the Gothic cathedral, Aquinas, the Black Death. See plates_for.py."""
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


def _pointed(cx, a, h, ybase, s, n=24):
    """A two-centred pointed arch over half-span a (m) rising h (m) from ybase (px), s px per m.
    Each half is an arc whose centre lies on the springing line, d = (h^2 - a^2) / 2a beyond the axis."""
    dd = (h * h - a * a) / (2 * a)
    r = a + dd
    top = math.degrees(math.atan2(-h, -dd)) % 360                      # the apex, seen from the left half's centre
    left = [(cx + (dd + r * math.cos(math.radians(180 + (top - 180) * i / n))) * s,
             ybase + r * s * math.sin(math.radians(180 + (top - 180) * i / n))) for i in range(n + 1)]
    right = [(2 * cx - x, y) for x, y in reversed(left)]
    return left + right[1:], dd, r


def _arc_through(p, q, sag, n=16):
    """A circular arc from p to q whose middle stands sag pixels above the chord (an arch's underside)."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    if ny > 0:                                                            # the normal that points up the page
        nx, ny = -nx, -ny
    m = (mx + nx * sag, my + ny * sag)                                    # the arc's crown
    # the circle through p, m and q
    ax, ay = p
    bx, by = m
    qx, qy = q
    den = 2 * (ax * (by - qy) + bx * (qy - ay) + qx * (ay - by))
    ox = ((ax * ax + ay * ay) * (by - qy) + (bx * bx + by * by) * (qy - ay) + (qx * qx + qy * qy) * (ay - by)) / den
    oy = ((ax * ax + ay * ay) * (qx - bx) + (bx * bx + by * by) * (ax - qx) + (qx * qx + qy * qy) * (bx - ax)) / den
    r = math.hypot(ax - ox, ay - oy)
    a0, am, a1 = (math.atan2(y - oy, x - ox) for x, y in (p, m, q))
    def norm(t):
        while t - a0 > math.pi:
            t -= 2 * math.pi
        while t - a0 < -math.pi:
            t += 2 * math.pi
        return t
    am, a1 = norm(am), norm(a1)
    if not (min(a0, a1) <= am <= max(a0, a1)):                            # go the way round that passes the crown
        a1 += 2 * math.pi if a1 < a0 else -2 * math.pi
    return [(ox + r * math.cos(a0 + (a1 - a0) * i / n), oy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def gothic_cathedral():
    d = D()
    # A cross-section of the nave of Amiens Cathedral, to scale from the heights in its records: the high
    # vault 42.3 m above the floor, the aisle vaults 19.7 m, the arcade's columns 13.85 m, the aisles 8.65 m
    # between column axes, the roof's ridge at 56 m. The nave's span (14.6 m between pier axes), the springing
    # of the high vault (30 m), the buttress piers and the flyers are drawn to the usual proportions, not
    # measured. Each pointed arch is two-centred: its halves are arcs about centres on the springing line.
    s = 4.2                                                               # px per meter
    cx, g = 200, 272                                                      # the axis and the floor
    Y = lambda m: g - m * s
    X = lambda m: cx + m * s
    an, hv, spring = 7.3, 42.3 - 30.0, 30.0                               # nave half-span, rise, springing
    aw, ah, aspring = 8.65, 19.7 - 13.85, 13.85                           # aisle width, rise, springing
    wall = an + aw                                                        # the aisle's outer wall, from the axis
    bp0, bp1 = wall - 0.6, wall + 3.6                                     # the buttress pier
    nave_v, dd, r = _pointed(cx, an, hv, Y(spring), s)
    aisles = [_pointed(cx + sg * (an + aw / 2) * s, aw / 2, ah, Y(aspring), s) for sg in (-1, 1)]

    d.group('thin')
    d.line((cx, Y(58)), (cx, g + 6))                                      # the axis
    d.line((X(-wall - 6), g), (X(wall + 6), g))                           # the floor
    d.line((X(-an - 1), Y(spring)), (X(an + 1), Y(spring)))               # the high vault's springing line
    for sg in (-1, 1):                                                    # the centres of the high vault's two arcs
        ox = cx + sg * dd * s
        d.line((ox - 3, Y(spring)), (ox + 3, Y(spring)))
        d.line((ox, Y(spring) - 3), (ox, Y(spring) + 3))
    d.line((cx + dd * s, Y(spring)), (cx, Y(42.3)))                       # one radius, centre to apex
    xa = X(-wall - 4.5)                                                   # heights, dimensioned at the left
    for m in (0, 19.7, 42.3):
        d.line((xa - 4, Y(m)), (xa + 4, Y(m)))
    d.line((xa, Y(0)), (xa, Y(42.3)))
    d.line((X(-wall), Y(19.7)), (xa + 4, Y(19.7)))
    d.line((X(-an), Y(42.3)), (xa + 4, Y(42.3)))

    d.group()
    d.line(*nave_v)                                                       # the high vault
    for v, _, _ in aisles:                                                # the aisle vaults
        d.line(*v)
    for sg in (-1, 1):
        # the nave wall: arcade, triforium and clerestory, carried on the pier, up to the roof's foot
        x0, x1 = cx + sg * an * s, cx + sg * (an + 0.9) * s
        d.line((x0, g), (x0, Y(spring)))
        d.line((x1, g), (x1, Y(43)))
        # the aisle's outer wall and the buttress pier with its pinnacle
        xw = cx + sg * wall * s
        d.line((xw, Y(aspring)), (xw, g))
        xp0, xp1 = cx + sg * bp0 * s, cx + sg * bp1 * s
        d.line((xp0, g), (xp0, Y(33)), (xp1, Y(33)), (xp1, g))
        xm = (xp0 + xp1) / 2
        d.line((xp0 + sg * 2, Y(33)), (xm, Y(39)), (xp1 - sg * 2, Y(33)))
        # the timber roofs: over the nave to the ridge, and the aisle's lean-to
        d.line((x1, Y(43)), (cx, Y(56)))
        d.line((x1, Y(26)), (xp0, Y(21.5)))

    d.group('mid')
    for sg in (-1, 1):
        # two tiers of flyers, from the clerestory wall over the aisle roof to the pier
        x1 = cx + sg * (an + 0.9) * s
        xp0 = cx + sg * bp0 * s
        for top, low, sag in ((38.0, 31.5, 8), (31.0, 25.5, 7)):
            p, q = (x1, Y(top - 2.0)), (xp0, Y(low - 2.0))
            arc = _arc_through(p, q, sag)                                  # the flyer's arched underside
            d.line(*arc)
            d.line((x1, Y(top + 1.0)), (xp0, Y(low + 1.0)))                # and its straight, sloping top
        # the column of the arcade, and the aisle's springing
        d.line((cx + sg * (an + 0.9) * s, Y(aspring)), (cx + sg * wall * s, Y(aspring)))

    d.group('mid')
    # the thrust, on the left: from the vault's haunch along the lower flyer, down the pier to the ground
    hx, hy = X(-an + 1.2), Y(spring + 2.5)
    fx, fy = X(-bp0 + 1.0), Y(25.8)
    d.line((hx, hy), (fx, fy))
    _arrow(d, (hx, hy), (fx, fy), 6)
    px = X(-(bp0 + bp1) / 2)
    d.line((px, Y(24)), (px, g - 8))
    _arrow(d, (px, Y(24)), (px, g - 8), 6)

    d.group('mid')
    d.text(xa - 7, Y(42.3) + 3, '42.3', size=7, anchor='end')
    d.text(xa - 7, Y(19.7) + 3, '19.7', size=7, anchor='end')
    d.text(xa - 7, Y(0) + 3, '0 M', size=7, anchor='end')
    d.text(X(-(bp0 + bp1) / 2) - 8, Y(12), 'THRUST', size=7, anchor='end')
    d.text(X(bp1 + 1.5), Y(36), 'FLYING', size=7, anchor='start')
    d.text(X(bp1 + 1.5), Y(36) + 9, 'BUTTRESS', size=7, anchor='start')
    d.text(cx, g + 16, 'AMIENS · NAVE · SECTION', size=7)
    return d


def aquinas():
    d = D()
    # The structure of one article of the Summa theologiae, I, q. 2, a. 3, "Whether God exists?": two objections,
    # the authority "on the contrary", the answer with its five ways, and a reply to each objection. Each way is
    # drawn as a chain of causes that cannot go back forever, and the five converge on one first principle.
    def box(x, y, w, h):
        _box(d, x, y, w, h)

    title = (140, 12, 120, 30)
    sed = (150, 54, 100, 26)
    objs = [(16, 88, 96, 26), (16, 124, 96, 26)]
    reps = [(288, 88, 96, 26), (288, 124, 96, 26)]
    resp = (117, 160, 166, 122)
    rows = [178, 198, 218, 238, 258]
    first = (249, 218)

    d.group('thin')
    for (ox, oy, ow, oh), (rx, ry, rw, rh) in zip(objs, reps):           # each objection is answered by its reply
        d.line((ox + ow, oy + oh / 2), (rx, ry + rh / 2))
    d.line((200, 4), (200, 296))                                        # the axis
    for y in rows:                                                      # the five ways' guide lines
        d.line((resp[0] + 58, y), (first[0], y))

    d.group()
    box(*title)
    box(*sed)
    for b in objs + reps:
        box(*b)
    box(*resp)

    d.group('mid')
    tx, ty, tw, th = title
    for (x, y, w, h) in (objs[0], sed):                                 # the question opens onto its parts
        p0 = (tx + tw / 2 + (x + w / 2 - 200) * 0.45, ty + th)
        p1 = (x + w / 2, y)
        d.line(p0, p1)
        _arrow(d, p0, p1, 4)
    d.line((200, sed[1] + sed[3]), (200, resp[1]))                      # on the contrary, then the answer
    _arrow(d, (200, sed[1] + sed[3]), (200, resp[1]), 4)
    for (x, y, w, h) in reps:                                           # the answer grounds the replies
        p0 = (resp[0] + resp[2], resp[1] + 10)
        p1 = (x, y + h / 2)
        d.line(p0, p1)
        _arrow(d, p0, p1, 4)
    # five chains of causes, each running back to the first
    for y in rows:
        xs = [resp[0] + 60 + 14 * k for k in range(5)]
        for x in xs:
            d.circle(x, y, 2.6)
        for a, b in zip(xs, xs[1:]):
            d.line((a + 2.6, y), (b - 2.6, y))
        a = math.atan2(y - first[1], xs[-1] - first[0])
        d.line((xs[-1] + 2.6, y), (first[0] + 4 * math.cos(a), first[1] + 4 * math.sin(a)))
    d.circle(first[0], first[1], 4)

    d.group('mid')
    d.text(200, 25, 'Q. 2 · A. 3', size=7)
    d.text(200, 35, 'WHETHER GOD EXISTS', size=7)
    d.text(200, 70, 'ON THE CONTRARY', size=7)
    for (x, y, w, h), s1 in zip(objs, ('OBJECTION 1', 'OBJECTION 2')):
        d.text(x + w / 2, y + 16, s1, size=7)
    for (x, y, w, h), s1 in zip(reps, ('REPLY 1', 'REPLY 2')):
        d.text(x + w / 2, y + 16, s1, size=7)
    d.text(200, resp[1] + 12, 'I ANSWER THAT', size=7)
    for y, s1 in zip(rows, ('MOTION', 'CAUSE', 'NECESSITY', 'DEGREES', 'ENDS')):
        d.text(resp[0] + 6, y + 2.5, s1, size=7, anchor='start')
    d.text(first[0] + 9, first[1] + 2.5, 'FIRST', size=7, anchor='start')
    return d


def black_death():
    d = D()
    # The plague's arrival, place by place, on a plain latitude-longitude grid (equirectangular, longitude
    # scaled by cos 46 degrees), with no coastlines: each dot is a city at its real position, labeled with the
    # year of the first record of plague there. The places to Almeria and their dates, and the sea routes
    # drawn as arrows, are Wheelis's chronology (Emerging Infectious Diseases, 2002, figure 1); Weymouth,
    # London, Strasbourg, Bergen, Novgorod and Moscow are dated from the reading's other sources.
    k = math.cos(math.radians(46))
    s = 8.6
    lon0, lat0 = 17.0, 46.0
    P = lambda lon, lat: (200 + (lon - lon0) * k * s, 150 - (lat - lat0) * s)
    cities = {
        'caffa': (35.38, 45.03), 'constantinople': (28.98, 41.01), 'alexandria': (29.92, 31.20),
        'messina': (15.55, 38.19), 'genoa': (8.93, 44.41), 'venice': (12.33, 45.44),
        'marseille': (5.37, 43.30), 'ragusa': (18.09, 42.65), 'tunis': (10.18, 36.80),
        'barcelona': (2.17, 41.39), 'almeria': (-2.46, 36.84), 'weymouth': (-2.45, 50.61),
        'london': (-0.13, 51.50), 'strasbourg': (7.75, 48.58), 'bergen': (5.32, 60.39),
        'novgorod': (31.27, 58.52), 'moscow': (37.62, 55.75),
    }
    xy = {c: P(lon, lat) for c, (lon, lat) in cities.items()}
    routes = [('caffa', 'constantinople'), ('constantinople', 'messina'), ('constantinople', 'alexandria'),
              ('messina', 'genoa'), ('messina', 'marseille'), ('messina', 'tunis'), ('constantinople', 'ragusa'),
              ('ragusa', 'venice'), ('marseille', 'barcelona'), ('barcelona', 'almeria')]

    d.group('thin')
    for lon in range(-10, 45, 10):                                        # the graticule, every ten degrees
        d.line(P(lon, 29), P(lon, 63))
    for lat in range(30, 65, 10):
        d.line(P(-6, lat), P(42, lat))

    d.group()
    for c, (x, y) in xy.items():
        d.circle(x, y, 3.4 if c == 'caffa' else 2.3)

    d.group('mid')
    for a, b in routes:                                                   # the sea routes, by galley
        (x0, y0), (x1, y1) = xy[a], xy[b]
        L = math.hypot(x1 - x0, y1 - y0)
        q0 = (x0 + (x1 - x0) * 5 / L, y0 + (y1 - y0) * 5 / L)
        q1 = (x1 - (x1 - x0) * 4 / L, y1 - (y1 - y0) * 4 / L)
        d.line(q0, q1)
        _arrow(d, q0, q1, 4)

    d.group('mid')
    labels = {'caffa': ('CAFFA 1346', 7, 3, 'start'), 'constantinople': ('CONSTANTINOPLE 1347', 4, 17, 'start'),
              'alexandria': ('ALEXANDRIA 1347', -6, 3, 'end'), 'messina': ('MESSINA 1347', 6, 9, 'start'),
              'tunis': ('TUNIS 1348', -6, 3, 'end'), 'marseille': ('MARSEILLE 1348', -6, 3, 'end'),
              'venice': ('VENICE 1348', 4, -5, 'start'), 'almeria': ('ALMERÍA 1348', -6, 3, 'end'),
              'barcelona': ('1348', -6, 3, 'end'), 'weymouth': ('WEYMOUTH 1348', -6, 3, 'end'),
              'london': ('LONDON 1348', 6, 3, 'start'), 'strasbourg': ('STRASBOURG 1349', 6, 3, 'start'),
              'bergen': ('BERGEN 1349', 6, 3, 'start'), 'novgorod': ('NOVGOROD 1352', 6, 3, 'start'),
              'moscow': ('MOSCOW 1353', 6, 3, 'start')}
    for c, (t, dx, dy, an) in labels.items():
        x, y = xy[c]
        d.text(x + dx, y + dy, t, size=7, anchor=an)
    return d


PLATES = {'gothic-cathedral': gothic_cathedral, 'aquinas': aquinas, 'black-death': black_death}
