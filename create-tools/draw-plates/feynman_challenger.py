"""feynman plates, the frame "challenger" and the trail "The commission" (sprint 014). See feynman.py."""
import math

from plates import D



def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _rot(pts, cx, cy, deg):
    """Rotate points about (cx, cy) by `deg` degrees (positive turns clockwise on screen)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def _rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def challenger():
    """The demonstration of 11 February 1986: a C-clamp squeezing O-ring rubber in a glass of ice water,
    and beside it the recovery the rubber has to make, warm and cold (schematic: the report's 'five times')."""
    d = D()
    cx = 104
    top, bot = 74, 252          # the tumbler's rim and base
    rt, rb = 58, 46             # its half-widths at rim and base
    water = 104
    half = lambda y: rt + (rb - rt) * (y - top) / (bot - top)
    # construction: the glass's axis, the water line carried across, the graph's grid
    gx0, gy0, gw, gh = 228, 236, 150, 150
    d.group('thin')
    d.line((cx, 40), (cx, bot + 12))
    d.line((cx - half(water) - 14, water), (cx + half(water) + 14, water))
    d.lines([[(gx0 + gw * k / 5, gy0), (gx0 + gw * k / 5, gy0 - gh)] for k in range(1, 6)])
    d.lines([[(gx0, gy0 - gh * k / 4), (gx0 + gw, gy0 - gh * k / 4)] for k in range(1, 5)])
    # the glass: a tumbler in elevation, its rim and base as ellipses, the water surface
    d.group()
    d.line((cx - rt, top), (cx - rb, bot))
    d.line((cx + rt, top), (cx + rb, bot))
    d.ellipse(cx, top, rt, 7)
    d.arc(cx, bot, rb, 0, 180, ry=6)
    d.ellipse(cx, water, half(water), 6)
    # the C-clamp: its frame, the screw through the upper arm, the handle above the rim
    sx = cx - 14                 # the screw's axis
    spine = cx + 30
    d.line((sx - 8, 132), (spine, 132), (spine, 222), (sx - 8, 222))
    d.line((sx - 8, 132), (sx - 8, 140), (spine - 8, 140), (spine - 8, 214), (sx - 8, 214), (sx - 8, 222))
    d.line((sx - 3, 48), (sx - 3, 192))
    d.line((sx + 3, 48), (sx + 3, 192))
    d.line((sx - 9, 192), (sx + 9, 192), (sx + 9, 197), (sx - 9, 197), closed=True)  # the pad
    d.line((sx - 22, 48), (sx + 22, 48))  # the tommy bar
    # the rubber: a short length of O-ring, squashed between pad and jaw, its section an ellipse
    d.group('mid')
    d.ellipse(sx, 205.5, 13, 8.5)
    d.lines([[(sx - 13 + 26 * k / 5, 197.5), (sx - 13 + 26 * k / 5 + 3, 213.5)] for k in range(1, 5)])
    # the screw thread, and ice: cubes turned at computed angles on the surface
    d.lines([[(sx - 3, y), (sx + 3, y + 3)] for y in range(56, 188, 8)])
    for (ix, iy, a, sz) in ((cx - 38, water + 6, 18, 13), (cx + 44, water + 12, -24, 12), (cx - 34, water + 40, 40, 11)):
        c = [(ix - sz / 2, iy - sz / 2), (ix + sz / 2, iy - sz / 2), (ix + sz / 2, iy + sz / 2), (ix - sz / 2, iy + sz / 2)]
        d.line(*_rot(c, ix, iy, a), closed=True)
    # the graph: how much of its squeeze the rubber gives back, against time, warm and cold
    d.group()
    d.line((gx0, gy0), (gx0 + gw + 6, gy0))
    d.line((gx0, gy0), (gx0, gy0 - gh - 8))
    _arrow(d, gx0 + gw + 6, gy0, 0)
    _arrow(d, gx0, gy0 - gh - 8, -math.pi / 2)
    tau = 0.5                       # seconds, warm; cold is five times slower
    T = 5.0
    for t_c in (tau, 5 * tau):
        d.line(*[(gx0 + gw * (T * i / 100) / T, gy0 - gh * (1 - math.exp(-(T * i / 100) / t_c))) for i in range(101)])
    d.group('mid')
    t_gap = 0.6                     # the joint's gap opens in about 600 ms
    d.line((gx0 + gw * t_gap / T, gy0), (gx0 + gw * t_gap / T, gy0 - gh - 4))
    d.group()
    d.text(gx0 + gw * 0.22, gy0 - gh * 0.99 - 6, '75°F', size=8, anchor='start')
    d.text(gx0 + gw * 0.70, gy0 - gh * 0.55 + 14, '32°F', size=8, anchor='start')
    d.text(gx0 + gw / 2, gy0 + 16, 'TIME · SECONDS', size=7)
    d.text(gx0 + 6, gy0 - gh - 14, 'SPRING-BACK', size=7, anchor='start')
    d.text(gx0 + gw * t_gap / T + 3, gy0 - 8, 'GAP OPENS', size=6, anchor='start')
    d.text(cx, 282, 'C-CLAMP · O-RING · ICE WATER', size=8)
    return d


def rogers_commission():
    """February 1986 as a calendar: the days of his first two weeks on the commission, joined in order."""
    d = D()
    x0, y0, cw, ch = 46, 72, 44, 38
    cell = lambda col, row: (x0 + cw * (col + 0.5), y0 + ch * (row + 0.5))
    # Saturday 1 February 1986 falls in the first row's last column (28 January was a Tuesday)
    pos = lambda day: (((day + 5) % 7), (day + 5) // 7)   # day of February; January as day - 31
    d.group('thin')
    d.lines([[(x0 + cw * c, y0), (x0 + cw * c, y0 + ch * 5)] for c in range(8)])
    d.lines([[(x0, y0 + ch * r), (x0 + cw * 7, y0 + ch * r)] for r in range(6)])
    # the grid's frame and the header
    d.group()
    d.line(*_rect(x0, y0 - 18, x0 + cw * 7, y0 + ch * 5), closed=True)
    d.line((x0, y0), (x0 + cw * 7, y0))
    # the days: each event a mark, the path through them in order
    days = [(-3, 'X'), (0, 'o'), (3, 'O'), (4, 'o'), (5, 'o'), (6, 'O'), (8, 'o'), (9, 'o'), (10, 'O'), (11, 'B'), (13, 'o'),
            (14, 'o'), (25, 'o'), (26, 'o'), (27, 'o')]
    pts = []
    d.group('mid')
    for day, kind in days:
        c, r = pos(day)
        px, py = cell(c, r)
        pts.append((px, py))
        if kind == 'X':
            d.lines([[(px - 9, py - 9), (px + 9, py + 9)], [(px - 9, py + 9), (px + 9, py - 9)]])
        elif kind == 'O':
            d.circle(px, py, 11)
        elif kind == 'o':
            d.circle(px, py, 5)
    d.group()
    d.line(*pts)
    c, r = pos(11)
    d.circle(*cell(c, r), 15)
    d.circle(*cell(c, r), 11)
    d.group()
    for k, w in enumerate('SMTWTFS'):
        d.text(x0 + cw * (k + 0.5), y0 - 5, w, size=8)
    d.text(x0 + cw * 3.5, 44, 'FEBRUARY 1986', size=9)
    for day, _ in days:
        c, r = pos(day)
        px, py = cell(c, r)
        d.text(px + cw / 2 - 4, py - ch / 2 + 9, str(day if day > 0 else day + 31), size=6, anchor='end')
    c, r = pos(11)
    px, py = cell(c, r)
    d.text(px, py + ch / 2 + 20, 'ICE WATER', size=7)
    d.text(x0 + cw * 7, 282, 'EO 12546 · 3 FEB', size=7, anchor='end')
    return d


def _joint(redesign=False):
    """A solid rocket booster field joint in section: outside to the left, the propellant to the right.
    Dimensions in inches at `s` pixels an inch; the original design, or the 1988 redesign."""
    d = D()
    s = 66.0
    xo = 170.0                        # outer surface of the case wall
    tw, lo, li, clr = 0.50, 0.32, 0.46, 0.02   # tang, outer leg, inner leg, clearance
    yc = 58.0                         # top of the clevis
    yb = yc + 2.8 * s                 # bottom of the slot
    X = lambda inch: xo + inch * s
    Y = lambda inch: yc + inch * s
    t0, t1 = X(0), X(tw)              # the tang's faces
    il0, il1 = X(tw + clr), X(tw + clr + li)   # the inner leg's faces
    ol0 = X(-lo)                      # the outer leg's outside
    lip0, lip1 = X(tw + clr + li + clr), X(tw + clr + li + clr + 0.30)   # the capture lip (redesign)
    wall1 = lip1 if redesign else t1
    y1, y2 = Y(0.55), Y(1.00)         # O-ring centres
    yp = Y(2.00)                      # pin centre
    r_o = 0.28 / 2 * s                # O-ring section radius
    # construction: centre lines of the O-rings and pin carried across, the case's outer line
    d.group('thin')
    for y in (y1, y2, yp):
        d.line((ol0 - 30, y), (il1 + 90, y))
    d.line((xo, 12), (xo, 290))
    if redesign:
        d.line((lip0 - 20, Y(1.22)), (lip1 + 60, Y(1.22)))
    # the metal: upper segment (wall and tang, and the capture lip), lower segment (clevis)
    d.group()
    lip_bot = Y(1.35)
    if redesign:
        d.line((t0, 12), (t0, yb - 3), (t1, yb - 3), (t1, yc - 8), (lip0, yc - 8), (lip0, lip_bot),
               (lip1, lip_bot), (lip1, 12))
    else:
        d.line((t0, 12), (t0, yb - 3), (t1, yb - 3), (t1, 12))
    base = yb + 0.25 * s
    d.line((il0, yc), (il0, yb), (t0 - clr * s, yb), (t0 - clr * s, yc), (ol0, yc), (ol0, base),
           (t0, base + 0.5 * s), (t0, 292))
    d.line((il0, yc), (il1, yc), (il1, base), (t1, base + 0.5 * s), (t1, 292))
    # the seals: grooves in the inner leg's face and the O-rings in them; the pin
    d.group('mid')
    g = 0.34 * s / 2
    for y in (y1, y2):
        d.line((il0, y - g), (il0 + 0.2 * s, y - g), (il0 + 0.2 * s, y + g), (il0, y + g))
        d.circle(il0 + r_o - 1.5, y, r_o)
    d.line(*_rect(ol0 - 4, yp - 0.2 * s, il0 + 0.22 * s, yp + 0.2 * s), closed=True)
    d.line(*_rect(ol0 - 12, yp - 0.4 * s, ol0 - 4, yp + 0.4 * s), closed=True)   # the retainer band
    if redesign:
        y3 = Y(1.10)
        d.line((lip0, y3 - g), (lip0 + 0.18 * s, y3 - g), (lip0 + 0.18 * s, y3 + g), (lip0, y3 + g))
        d.circle(lip0 + r_o - 1.5, y3, r_o)
        # the heater: a band round the outside of the joint, its element zigzag
        hx0, hx1 = ol0 - 34, ol0 - 18
        d.line(*_rect(hx0, yc - 0.1 * s, hx1, Y(2.6)), closed=True)
        zz = [(hx0 + 3 + (10 if k % 2 else 0), yc - 0.1 * s + 6 + k * 8) for k in range(int((Y(2.6) - yc) / 8))]
        d.line(*zz)
    # insulation and propellant on the inside, the putty in the gap, and the gas path
    d.group('mid')
    ins = 0.42 * s
    d.line((wall1, yc - 8), (wall1 + ins, yc - 8), (wall1 + ins, 12))
    lo_x = (lip1 if redesign else il1)
    d.line((il1 if not redesign else lip1, yc + (0 if not redesign else lip_bot - yc)), (lo_x + ins, yc + (0 if not redesign else lip_bot - yc)), (lo_x + ins, 292))
    d.line((wall1 + ins + 36, 12), (wall1 + ins + 36, 292))
    if not redesign:
        # zinc chromate putty packed into the gap between the insulation, and the hot gas pushing through it
        wav = [(t1 + 2 + (il1 + ins - t1 - 4) * i / 24, yc - 4 + 2.2 * math.sin(i * 1.3)) for i in range(25)]
        d.line(*wav)
        d.line((il1 + ins + 60, yc - 4), (il0 + 4, yc - 4), (il0 - 2, y1 - r_o - 2))
        _arrow(d, il0 - 2, y1 - r_o - 2, math.atan2(y1 - r_o - 2 - (yc - 4), -6))
    # joint rotation: the inner leg bent away from the tang under pressure, exaggerated, and the gap
    if not redesign:
        d.group('thin')
        leg = [(il0, yc), (il1, yc), (il1, base), (il0, base)]
        ghost = _rot(leg, (il0 + il1) / 2, base, 3.2)
        d.line(ghost[0], ghost[3], ghost[2], ghost[1], closed=True)
        gx = ghost[0][0] + (ghost[3][0] - ghost[0][0]) * (y1 - ghost[0][1]) / (ghost[3][1] - ghost[0][1])
        d.line((t1, y1), (gx, y1))
    # labels
    d.group()
    d.text(ol0 - 30, 22, 'OUTSIDE', size=7, anchor='end')
    d.text(wall1 + ins + 50, 26, 'PROPELLANT', size=7, anchor='start')
    d.text(t0 - 8, 44, 'TANG', size=8, anchor='end')
    d.text(ol0 - 6 - (40 if redesign else 0), yb + 26, 'CLEVIS', size=8, anchor='end')
    d.text(il1 + ins + 44, y1 + 3, 'PRIMARY', size=7, anchor='start')
    d.text(il1 + ins + 44, y2 + 3, 'SECONDARY', size=7, anchor='start')
    d.text(il1 + ins + 44, yp + 3, 'PIN', size=7, anchor='start')
    if redesign:
        d.text(lip1 + ins + 44 - (lip1 - il1), Y(1.22) + 3, 'CAPTURE', size=7, anchor='start')
        d.text(ol0 - 26, Y(2.6) + 14, 'HEATER', size=7, anchor='middle')
    else:
        d.text(il1 + ins + 44, yc - 1, 'PUTTY', size=7, anchor='start')
        d.text(il0 + 14, y1 - 16, 'GAP', size=7, anchor='start')
    return d


def the_joint():
    """The field joint as flown on Challenger: tang in clevis, two O-rings, putty, the pin; and joint rotation."""
    return _joint(False)


def return_to_flight():
    """The redesigned field joint of 1988: a capture lip, a third O-ring, and a heater round the outside."""
    return _joint(True)


def teleconference():
    """The three ends of the call of 27 January 1986, placed by latitude and longitude, and its hours on a clock."""
    d = D()
    lon0, lon1, lat0, lat1 = -122.0, -74.0, 24.0, 46.0
    k = math.cos(math.radians(36))
    sx = 230 / (lon1 - lon0)
    P = lambda lat, lon: (22 + (lon - lon0) * sx, 40 + (lat1 - lat) * sx / k)
    sites = {'WASATCH': (41.6, -112.5), 'MARSHALL': (34.65, -86.67), 'KENNEDY': (28.57, -80.65)}
    # construction: a graticule every five degrees
    d.group('thin')
    for lon in range(-120, -73, 5):
        d.line(P(lat0, lon), P(lat1, lon))
    for lat in range(25, 46, 5):
        d.line(P(lat, lon0), P(lat, lon1))
    # the links: each pair of sites joined by a gentle arc (the great circle, as it bows on this projection)
    d.group()
    names = list(sites)
    for i in range(3):
        for j in range(i + 1, 3):
            a, b = sites[names[i]], sites[names[j]]
            pts = []
            for t in range(41):
                u = t / 40
                lat = a[0] + (b[0] - a[0]) * u + 2.2 * math.sin(math.pi * u) * (abs(a[1] - b[1]) / 30)
                pts.append(P(lat, a[1] + (b[1] - a[1]) * u))
            d.line(*pts)
    for name, (lat, lon) in sites.items():
        d.circle(*P(lat, lon), 5)
    d.group('mid')
    for name, (lat, lon) in sites.items():
        d.circle(*P(lat, lon), 10)
    # the clock: 8:45 to 11:15 p.m. swept out as an arc, and the thermometer: 53°F and 36°F
    cx, cy, r = 330, 84, 40
    d.group('thin')
    d.lines([[(cx + (r - 5) * math.sin(math.radians(30 * h)), cy - (r - 5) * math.cos(math.radians(30 * h))),
              (cx + r * math.sin(math.radians(30 * h)), cy - r * math.cos(math.radians(30 * h)))] for h in range(12)])
    d.group()
    d.circle(cx, cy, r)
    a0, a1 = (8.75 % 12) * 30, (11.25 % 12) * 30
    d.arc(cx, cy, r - 12, a0 - 90, a1 - 90)
    d.line((cx, cy), (cx + 22 * math.sin(math.radians(a1)), cy - 22 * math.cos(math.radians(a1))))
    d.line((cx, cy), (cx + 14 * math.sin(math.radians(11.25 * 30)), cy - 14 * math.cos(math.radians(11.25 * 30))))
    tx, tb, tt = 330, 262, 150
    F = lambda f: tb - (f - 20) * (tb - tt) / 60   # 20°F to 80°F
    d.line((tx - 5, F(80)), (tx - 5, tb - 6))
    d.line((tx + 5, F(80)), (tx + 5, tb - 6))
    d.arc(tx, F(80), 5, 180, 360)
    d.circle(tx, tb + 2, 9)
    d.group('mid')
    d.lines([[(tx + 5, F(f)), (tx + (12 if f % 10 == 0 else 9), F(f))] for f in range(20, 81, 5)])
    d.line((tx, tb - 6), (tx, F(36)))
    d.line((tx - 5, F(53)), (tx - 22, F(53)))
    d.line((tx - 5, F(36)), (tx - 22, F(36)))
    d.group()
    for name, (lat, lon) in sites.items():
        x, y = P(lat, lon)
        dx, dy, anc = {'WASATCH': (0, 24, 'middle'), 'MARSHALL': (-14, 4, 'end'), 'KENNEDY': (14, 16, 'start')}[name]
        d.text(x + dx, y + dy, name, size=7, anchor=anc)
    d.text(cx, cy + r + 14, '8:45–11:15 PM', size=7)
    d.text(tx - 25, F(53) + 3, '53°F', size=7, anchor='end')
    d.text(tx - 25, F(36) + 3, '36°F', size=7, anchor='end')
    d.text(22, 282, '27 JANUARY 1986 · TELECONFERENCE', size=8, anchor='start')
    return d


def reliability():
    """How likely a run of clean flights is, at three rates of failure: (1 − p)^n for n up to 135 flights."""
    d = D()
    ox, oy, w, h = 48, 244, 318, 190
    N = 135
    P = lambda n, q: (ox + w * n / N, oy - h * q)
    d.group('thin')
    d.lines([[P(n, 0), P(n, 1.04)] for n in range(25, N + 1, 25)])
    d.lines([[P(0, q / 4), P(N, q / 4)] for q in range(1, 5)])
    d.group()
    d.line(P(0, 0), P(N + 5, 0))
    d.line(P(0, 0), P(0, 1.1))
    _arrow(d, *P(N + 5, 0), 0)
    _arrow(d, *P(0, 1.1), -math.pi / 2)
    curves = {}
    for p in (1e-5, 1 / 100, 1 / 25):
        pts = [P(n, (1 - p) ** n) for n in range(N + 1)]
        curves[p] = pts
        d.line(*pts)
    d.group('mid')
    d.line(P(25, 0), P(25, 1.08))
    for p in (1 / 100, 1 / 25):
        d.circle(*P(25, (1 - p) ** 25), 3.5)
    d.circle(*P(25, (1 - 1e-5) ** 25), 3.5)
    d.group()
    d.text(*P(N, 1.0 + 0.05), '1 IN 100,000', size=7, anchor='end')
    d.text(P(N, (1 - 1 / 100) ** N)[0], P(N, (1 - 1 / 100) ** N)[1] - 16, '1 IN 100', size=7, anchor='end')
    d.text(P(62, (1 - 1 / 25) ** 62)[0] + 8, P(62, (1 - 1 / 25) ** 62)[1] + 2, '1 IN 25', size=7, anchor='start')
    d.text(P(25, 0)[0], oy + 12, '25', size=7)
    d.text(ox + w * 0.62, oy + 20, 'FLIGHTS FLOWN', size=7)
    d.text(P(N, 0)[0], oy + 12, str(N), size=7)
    d.text(ox + 6, oy - h * 1.12, 'P(NO LOSS YET)', size=7, anchor='start')
    return d


def appendix_f():
    """The orbiter's avionics as Appendix F describes them: four sensors to each of four computers, a vote, and a fifth."""
    d = D()
    sx, cx, vx, ax = 50, 170, 272, 350
    ys = [70, 110, 150, 190]
    # construction: every sensor copy wired to every computer
    d.group('thin')
    d.lines([[(sx + 16, y0), (cx - 22, y1)] for y0 in ys for y1 in ys])
    d.lines([[(cx + 22, y), (vx - 16, 130)] for y in ys])
    # the sensors, the four computers, the vote
    d.group()
    for y in ys:
        d.circle(sx, y, 9)
        d.line(*_rect(cx - 22, y - 12, cx + 22, y + 12), closed=True)
    vote = [(vx - 16, 130), (vx, 112), (vx + 16, 130), (vx, 148)]
    d.line(*vote, closed=True)
    d.line((vx + 16, 130), (ax - 14, 130))
    _arrow(d, ax - 14, 130, 0)
    d.circle(ax, 130, 12)
    # the fifth computer, loaded only with ascent and descent, standing by
    d.group('mid')
    d.line(*_rect(cx - 22, 236, cx + 22, 260), closed=True)
    d.lines([[(sx + 16, y), (cx - 22, 248)] for y in ys])
    d.line((cx + 22, 248), (vx, 248), (vx, 148))
    # a disagreeing computer, voted out: a cross through the third box
    d.line((cx - 16, ys[2] - 8), (cx + 16, ys[2] + 8))
    d.line((cx - 16, ys[2] + 8), (cx + 16, ys[2] - 8))
    d.group()
    d.text(sx, 40, 'SENSORS', size=7)
    d.text(cx, 40, 'FOUR GPC', size=7)
    d.text(vx, 104, 'VOTE', size=7)
    d.text(ax, 104, 'ACT', size=7)
    d.text(cx, 278, 'BACKUP', size=7)
    d.text(200, 22, 'FOUR COMPUTERS · ONE VOTE · A FIFTH IN RESERVE', size=7)
    return d


PLATES = {
    'challenger': challenger,
    'rogers-commission': rogers_commission,
    'the-joint': the_joint,
    'teleconference': teleconference,
    'reliability': reliability,
    'appendix-f': appendix_f,
    'return-to-flight': return_to_flight,
}
