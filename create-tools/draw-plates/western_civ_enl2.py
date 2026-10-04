"""Plates for western-civ's Reason and revolution frames by part enl2 (sprint 049). See plates_for.py."""
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


def french_revolution():
    d = D()
    # Left: a decimal clock dial of 1793-95. The day is ten hours of a hundred minutes; an inner ring
    # gives the old twenty-four hours for comparison, as dual dials of the period did. Midnight at the
    # top, noon (five decimal hours, twelve old ones) at the foot. The hands stand at 4 h 20, which is
    # about 10:05 by our arithmetic (4.2 / 10 x 24 = 10.08 hours).
    # Right: the Republican year as a grid: twelve months of thirty days, each cut into three
    # decades of ten, and five complementary days (six in a leap year) at the end. Three days the
    # reading names are ringed: 22 Prairial II, 9 Thermidor II and 18 Brumaire VIII.
    cx, cy, R = 100, 142, 84

    def at(frac, r):                                                  # a point on the dial
        a = math.radians(frac * 360 - 90)
        return (cx + r * math.cos(a), cy + r * math.sin(a))

    gx, gy, cw, gap, rh, pitch = 212, 44, 4.0, 3, 10, 15              # the calendar grid
    mx = lambda day: gx + day * cw + (day // 10) * gap                # left edge of day (0-based)
    gw = mx(30) - gap - gx

    d.group('thin')
    d.line((cx, cy - R - 8), (cx, cy + R + 8))
    d.line((cx - R - 8, cy), (cx + R + 8, cy))
    d.circle(cx, cy, R * 0.62)
    d.line(at(0, 0), at(0.1, R))                                      # one decimal hour = 2.4 old hours
    for k in range(1, 3):                                             # the decades' boundaries, carried down
        x = mx(10 * k) - gap / 2
        d.line((x, gy - 4), (x, gy + 12 * pitch + rh + 4))

    d.group()
    d.circle(cx, cy, R)
    d.circle(cx, cy, R * 0.86)
    for m in range(12):                                               # the months, three decades each
        y = gy + m * pitch
        for k in range(3):
            _box(d, mx(10 * k), y, 10 * cw, rh)
    y = gy + 12 * pitch
    _box(d, gx, y, 5 * cw, rh)                                        # the complementary days

    d.group('mid')
    ticks = []
    for i in range(100):                                              # a hundred minutes round the rim
        r0 = R * (0.86 if i % 10 == 0 else 0.93)
        ticks.append([at(i / 100, r0), at(i / 100, R)])
    for i in range(24):                                               # the old hours, inside
        r1 = R * (0.52 if i % 6 == 0 else 0.56)
        ticks.append([at(i / 24, r1), at(i / 24, R * 0.62)])
    d.lines(ticks)
    segs = []
    for m in range(12):                                               # each day of every month
        y = gy + m * pitch
        for day in range(30):
            if day % 10:
                x = mx(day)
                segs.append([(x, y), (x, y + rh)])
    y = gy + 12 * pitch
    for day in range(1, 5):
        segs.append([(gx + day * cw, y), (gx + day * cw, y + rh)])
    d.lines(segs)
    _box(d, gx + 5 * cw, y, cw, rh)                                   # the sixth day, in a leap year
    for month, day in ((8, 22), (10, 9), (1, 18)):                    # Prairial, Thermidor, Brumaire
        d.circle(mx(day - 1) + cw / 2, gy + month * pitch + rh / 2, 4.2)

    d.group()
    hh, mm = at(0.42, R * 0.46), at(0.2, R * 0.8)                     # 4 h 20, decimal
    d.line((cx, cy), hh)
    d.line((cx, cy), mm)
    d.circle(cx, cy, 2.5)

    d.group('mid')
    for h in range(1, 11):
        x, y = at(h / 10, R * 0.76)
        d.text(x, y + 2.5, str(h), size=7)
    for h, s in ((0, '24'), (6, '6'), (12, '12'), (18, '18')):
        x, y = at(h / 24, R * 0.43)
        d.text(x, y + 2.5, s, size=6)
    for m, s in enumerate('VBFNPVGFPMTF'):
        d.text(gx - 6, gy + m * pitch + 7.5, s, size=7)
    d.text(gx - 6, gy + 12 * pitch + 7.5, '+', size=7)
    labels = ((8, 22, '22 PRAIRIAL'), (10, 9, '9 THERMIDOR'), (1, 18, '18 BRUMAIRE'))
    for month, day, s in labels:
        d.text(gx + gw + 5, gy + month * pitch + 7.5, s, size=7, anchor='start')
    d.text(gx + gw / 2, gy - 12, '3 DECADES × 10 DAYS', size=7)
    d.text(gx + gw / 2, 268, '12 × 30 + 5 OR 6', size=7)
    d.text(cx, 268, '10 HOURS × 100 MINUTES', size=7)
    return d


def _pair(d, p, q, off=4, both=True):
    """Two parallel arrows between p and q, one each way, offset either side of the line."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * off, dx / n * off
    a, b = (p[0] + ox, p[1] + oy), (q[0] + ox, q[1] + oy)
    d.line(a, b)
    _arrow(d, a, b)
    if both:
        a, b = (q[0] - ox, q[1] - oy), (p[0] - ox, p[1] - oy)
        d.line(a, b)
        _arrow(d, a, b)


def american_revolution():
    d = D()
    # The Constitution of 1787 as boxes and arrows: Congress of two houses (the first House of 65
    # seats, Art. I sec. 2; a Senate of two members for each of 13 states, 26), the President and the
    # Supreme Court, with the checks the text gives each on the others, and the people below, who
    # elect the House directly and the President through electors. Senators were chosen by the
    # state legislatures until 1913, drawn as a dashed line.
    cg = (70, 26, 260, 62)                                            # Congress: x, y, w, h
    pr = (26, 186, 116, 44)                                           # President
    sc = (258, 186, 116, 44)                                          # Supreme Court
    house_c = (cg[0] + cg[2] * 0.25, cg[1] + cg[3])
    senate_c = (cg[0] + cg[2] * 0.75, cg[1] + cg[3])
    pr_top = (pr[0] + pr[2] / 2, pr[1])
    sc_top = (sc[0] + sc[2] / 2, sc[1])
    pr_r = (pr[0] + pr[2], pr[1] + pr[3] / 2)
    sc_l = (sc[0], sc[1] + sc[3] / 2)
    people_y = 272

    d.group('thin')
    d.line((cg[0] + cg[2] / 2, cg[1] + cg[3]), pr_top, sc_top, closed=True)   # the three powers' triangle
    d.line((8, people_y), (392, people_y))                           # the people, as a ground line
    d.line((200, 14), (200, people_y))

    d.group()
    for x, y, w, h in (cg, pr, sc):
        _box(d, x, y, w, h)
    d.line((cg[0] + cg[2] / 2, cg[1]), (cg[0] + cg[2] / 2, cg[1] + cg[3]))

    d.group('mid')
    _pair(d, (pr_top[0] - 6, pr_top[1]), (house_c[0] - 10, house_c[1]))          # veto / override
    _pair(d, (pr_r[0], pr_r[1]), (sc_l[0], sc_l[1]), both=False)                  # nominates
    d.line((senate_c[0] + 10, senate_c[1]), (sc_top[0] + 10, sc_top[1]))
    _arrow(d, (senate_c[0] + 10, senate_c[1]), (sc_top[0] + 10, sc_top[1]))      # confirms
    d.line((house_c[0] + 18, house_c[1]), (pr_top[0] + 22, pr_top[1]))
    _arrow(d, (house_c[0] + 18, house_c[1]), (pr_top[0] + 22, pr_top[1]))        # impeaches
    ex, ey = 12, cg[1] + cg[3] / 2                                                # the people elect the House
    d.line((ex, people_y), (ex, ey), (cg[0], ey))
    _arrow(d, (ex, ey), (cg[0], ey))
    x = pr_top[0] - 40
    d.line((x, people_y), (x, pr[1] + pr[3]))
    _arrow(d, (x, people_y), (x, pr[1] + pr[3]))                                  # through electors
    segs = []                                                                     # senators: by the states
    xs = 388
    y = people_y
    while y - 6 > ey:
        segs.append([(xs, y), (xs, y - 6)])
        y -= 10
    x = xs
    while x - 6 > cg[0] + cg[2]:
        segs.append([(x, ey), (x - 6, ey)])
        x -= 10
    d.lines(segs)
    _arrow(d, (cg[0] + cg[2] + 10, ey), (cg[0] + cg[2], ey))

    d.group('mid')
    d.text(house_c[0], cg[1] + 28, 'HOUSE', size=7)
    d.text(house_c[0], cg[1] + 40, '65 SEATS', size=7)
    d.text(senate_c[0], cg[1] + 28, 'SENATE', size=7)
    d.text(senate_c[0], cg[1] + 40, '26 SEATS', size=7)
    d.text(200, cg[1] - 4, 'CONGRESS · ARTICLE I', size=7)
    d.text(pr[0] + pr[2] / 2, pr[1] + 20, 'PRESIDENT', size=7)
    d.text(pr[0] + pr[2] / 2, pr[1] + 32, 'ARTICLE II', size=7)
    d.text(sc[0] + sc[2] / 2, sc[1] + 20, 'SUPREME COURT', size=7)
    d.text(sc[0] + sc[2] / 2, sc[1] + 32, 'ARTICLE III', size=7)
    d.text(92, 134, 'VETO', size=7, anchor='end')
    d.text(92, 144, '2/3 OVERRIDE', size=7, anchor='end')
    d.text(126, 120, 'IMPEACHES', size=7, anchor='start')
    d.text(200, pr_r[1] - 6, 'NOMINATES', size=7)
    d.text(senate_c[0] + 16, 140, 'CONFIRMS', size=7, anchor='start')
    d.text(200, people_y + 14, 'WE THE PEOPLE · ELECTORS · STATE LEGISLATURES', size=7)
    return d


def abolition():
    d = D()
    # The slave ship Brookes, from the admeasurement Captain Parrey laid before the Commons in 1788, as
    # Clarkson prints it (History, 1808, vol. 2): lower deck 100 ft long and 25 ft broad, 5 ft between
    # decks; the men's room 46 ft, the boys' 13 ft, the women's 28 ft 6 in, the gun-room 10 ft 6 in;
    # platforms (shelves) 6 ft broad along each side. The committee allowed each man 6 ft by 1 ft 4 in;
    # one such space is drawn, and no figures. The print gives 2 ft 7 in under the shelves.
    # Top: the lower deck in plan, stern at left. Bottom: a section amidships.
    s = 3.0                                                           # px per foot, plan
    x0, cy, half = 50, 92, 12.5
    X = lambda ft: x0 + ft * s

    def hw(ft):                                                       # half-breadth of the deck at ft from stern
        if ft <= 68:
            return half
        u = (ft - 68) / 32
        return half * math.sqrt(max(0.0, 1 - u * u))

    rooms = [(0, 10.5, 'GUN'), (10.5, 39, 'WOMEN 28\'6"'), (39, 52, 'BOYS 13\''), (52, 98, 'MEN 46\'')]
    shelf = 6.0

    d.group('thin')
    d.line((X(-4), cy), (X(104), cy))                                 # centre line
    for ft in (0, 100):                                               # length, dimensioned
        d.line((X(ft), cy - half * s - 14), (X(ft), cy - half * s - 4))
    d.line((X(0), cy - half * s - 9), (X(100), cy - half * s - 9))
    d.line((X(-8), cy - half * s), (X(-8), cy + half * s))            # breadth, dimensioned
    for y in (cy - half * s, cy + half * s):
        d.line((X(-11), y), (X(-5), y))

    d.group()
    top = [(X(f), cy - hw(f) * s) for f in [0] + [68 + i for i in range(0, 33)]]
    bot = [(X(f), cy + hw(f) * s) for f in [68 + i for i in range(32, -1, -1)] + [0]]
    d.line(*top, *bot, closed=True)

    d.group('mid')
    for a, b, _ in rooms[1:]:
        d.line((X(a), cy - hw(a) * s), (X(a), cy + hw(a) * s))       # bulkheads
    for a, b, _ in rooms[1:]:                                          # the shelves' inner edges
        segs = []
        for sign in (-1, 1):
            pts = []
            f = a
            while f <= b:
                w = hw(f) - shelf
                if w > 0.5:
                    pts.append((X(f), cy + sign * w * s))
                f += 1
            if len(pts) > 1:
                segs.append(pts)
        d.lines(segs)

    d.group()
    mx, my = X(53), cy - half * s                                     # one man's allowance, on the shelf
    _box(d, mx, my + 0.8, 1.333 * s, shelf * s - 1.6)

    # the section amidships
    t = 6.0                                                           # px per foot, section
    scx, deck_up, between, hold = 200, 176, 5.0, 10.0
    lower = deck_up + between * t
    under = 31 / 12                                                   # 2 ft 7 in under the shelves
    sh_y = lower - under * t

    d.group('thin')
    d.line((scx, deck_up - 8), (scx, lower + hold * t + 6))
    d.line((scx - 25 * t / 2 - 22, deck_up), (scx - 25 * t / 2 - 22, lower))
    for y in (deck_up, lower):
        d.line((scx - 25 * t / 2 - 26, y), (scx - 25 * t / 2 - 18, y))
    d.line((scx + 25 * t / 2 + 22, sh_y), (scx + 25 * t / 2 + 22, lower))
    for y in (sh_y, lower):
        d.line((scx + 25 * t / 2 + 18, y), (scx + 25 * t / 2 + 26, y))

    d.group()
    hullpts = []
    for i in range(0, 41):                                            # the hull, a half-ellipse below the deck
        a = math.pi * i / 40
        hullpts.append((scx - 25 * t / 2 * math.cos(a), lower + hold * t * math.sin(a) * 0.92))
    d.line((scx - 25 * t / 2, deck_up), *hullpts, (scx + 25 * t / 2, deck_up))
    d.line((scx - 25 * t / 2, deck_up), (scx + 25 * t / 2, deck_up))
    d.line((scx - 25 * t / 2, lower), (scx + 25 * t / 2, lower))

    d.group('mid')
    for sign in (-1, 1):
        xa, xb = scx + sign * 25 * t / 2, scx + sign * (25 / 2 - shelf) * t
        d.line((xa, sh_y), (xb, sh_y))
        d.line((xb, sh_y), (xb, lower))

    d.group('mid')
    for a, b, name in rooms:
        if name != 'GUN':
            d.text((X(a) + X(b)) / 2, cy + 3, name, size=7)
    d.text(X(50), cy - half * s - 13, "LOWER DECK · 100' × 25'", size=7)
    d.text(mx + 7, cy - 8, "ONE MAN 6' × 1'4\"", size=7, anchor='start')
    d.line((mx + 5, cy - 11), (mx + 2.5, my + shelf * s - 1))
    d.text(scx - 25 * t / 2 - 28, (deck_up + lower) / 2 + 2.5, "5'", size=7, anchor='end')
    d.text(scx + 25 * t / 2 + 28, (sh_y + lower) / 2 + 2.5, "2'7\"", size=7, anchor='start')
    d.text(scx, 290, 'SECTION AMIDSHIPS · SHELVES 6\' DEEP', size=7)
    return d


PLATES = {'french-revolution': french_revolution, 'american-revolution': american_revolution,
          'abolition': abolition}
