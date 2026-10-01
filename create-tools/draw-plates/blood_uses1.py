"""Plates for In the Blood's What we do with blood, part uses1 (sprint 028). See plates_for.py."""
import math
from plates import D


def _pt(cx, cy, r, a):
    """The point at `a` degrees on a circle (clockwise from +x; SVG's y runs down)."""
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _bag(x0, y0, w, h, r=6, n=6):
    """A plastic blood bag's outline: a rectangle with rounded corners, as a closed point list."""
    pts = []
    for cx, cy, a0 in ((x0 + w - r, y0 + r, -90), (x0 + w - r, y0 + h - r, 0),
                       (x0 + r, y0 + h - r, 90), (x0 + r, y0 + r, 180)):
        for i in range(n + 1):
            pts.append(_pt(cx, cy, r, a0 + 90 * i / n))
    return pts


def cryoprecipitate():
    d = D()
    # Pool's closed-bag procedure as the Fort Knox blood bank ran it in 1972, in four stations:
    # spin the unit and express the plasma; freeze the satellite bag at -60 C; thaw it overnight at
    # 2-4 C and spin cold; hang it upside down and drain the plasma, leaving the precipitate.
    # A temperature trace runs under the stations. Proportions are a sketch.
    xs = [20, 115, 210, 305]                                        # left edge of each station
    base = 214
    d.group('thin')
    for x in xs:                                                    # station frames
        d.line((x, 40), (x + 80, 40))
        d.line((x, base + 6), (x + 80, base + 6))
    # the temperature trace: +4 C, -60 C, +4 C, +4 C (higher is warmer)
    y4, y60 = 244, 284
    d.line((40, y4), (392, y4))
    d.line((40, y60), (392, y60))
    d.group()
    # station 1: the primary bag (cells settled low) joined to the empty satellite bag by tubing
    p1 = _bag(26, 70, 34, 120)
    d.line(*p1, closed=True)
    s1 = _bag(70, 120, 24, 70)
    d.line(*s1, closed=True)
    d.curve('M43 70 C43 50 82 50 82 120')
    # station 2: the satellite bag in a bath of ethanol and dry ice
    d.line(*_bag(143, 104, 26, 76), closed=True)
    d.line((122, 112), (122, base), (190, base), (190, 112))       # the bath
    # station 3: the thawed bag, spun cold; the rotor's swing seen as an arc above
    d.line(*_bag(236, 104, 28, 86), closed=True)
    d.arc(250, 104, 34, 200, 340, n=24)
    # station 4: hung upside down from a hook; the plasma runs down the tube to the red-cell bag
    d.line((345, 48), (345, 58))
    d.arc(345, 62, 4, -90, 180, n=12)
    d.line(*_bag(330, 66, 30, 78), closed=True)
    d.line((345, 144), (345, 166))
    d.line(*_bag(328, 166, 34, 44), closed=True)
    d.group('mid')
    # contents: settled red cells hatched in the primary bag, plasma lines above them
    for y in range(140, 188, 6):
        d.line((30, y), (56, y - 6))
    d.line((26, 136), (60, 136))
    # frozen plasma: a lattice in the satellite bag; the bath's surface
    for y in range(112, 176, 10):
        d.line((147, y), (165, y + 6))
        d.line((147, y + 6), (165, y))
    d.line((124, 120), (188, 120))
    # the precipitate, pale flecks gathered at the bottom of the thawed bag after the spin
    for i in range(9):
        x = 242 + (i * 7) % 18
        y = 178 + (i * 5) % 9
        d.line((x, y), (x + 3, y + 1))
    # in the hung bag the paste clings to what was the bottom, now on top
    for i in range(7):
        x = 336 + (i * 6) % 18
        y = 70 + (i * 4) % 7
        d.line((x, y), (x + 3, y + 1))
    for y in (150, 157):                                            # drops in the tube
        d.line((345, y), (345, y + 3))
    d.line((332, 196), (358, 196))                                  # plasma returned over the cells
    # arrows between stations, and the trace itself
    for x in xs[:-1]:
        d.line((x + 82, 30), (x + 93, 30))
        _arrow(d, (x + 82, 30), (x + 93, 30))
    d.line((40, y4), (100, y4), (120, y60), (190, y60), (210, y4), (385, y4))
    d.group('mid')
    for x, s in zip(xs, ('SPIN · EXPRESS', 'FREEZE', 'THAW · SPIN', 'DRAIN')):
        d.text(x + 40, 22, s, size=7)
    d.text(36, y4 + 3, '+4 °C', size=7, anchor='end')
    d.text(36, y60 + 3, '−60 °C', size=7, anchor='end')
    d.text(155, y60 - 10, 'DRY ICE BATH', size=7)
    d.text(296, y4 - 6, '2–4 °C OVERNIGHT · 4–8 °C SPIN', size=7)
    return d


def fractionation():
    d = D()
    # Cohn's Method 6 as a cascade: plasma passes left to right through five precipitations; at each
    # the dials are set, a precipitate is spun down (below), and the liquid goes on. Under the
    # vessels, the ethanol (per cent, solid) and pH (dashed) at each step, to scale.
    xs = [52, 124, 196, 268, 340]
    names = ['I', 'II+III', 'IV-1', 'IV-4', 'V']
    eth = [8, 25, 18, 40, 40]
    ph = [7.2, 6.8, 5.2, 5.8, 4.8]
    top, vb = 40, 104                                               # vessel top and bottom
    g0, g1 = 280, 200                                               # chart: y of 0 and of the top
    ey = lambda e: g0 - (g1 - g0) * -e / 40                         # ethanol 0-40 per cent
    py = lambda v: g0 - (g0 - g1) * (v - 4) / 4                     # pH 4-8
    d.group('thin')
    d.line((24, g0), (376, g0))
    d.line((24, g1), (376, g1))
    d.line((24, (g0 + g1) / 2), (376, (g0 + g1) / 2))
    for x in xs:
        d.line((x, 176), (x, g0))                                   # each step dropped to the chart
    d.group()
    for x in xs:                                                    # the vessels: a beaker with a lip
        d.line((x - 20, top - 3), (x - 18, top), (x - 18, vb), (x + 18, vb), (x + 18, top), (x + 20, top - 3))
    for x in xs:                                                    # the precipitate spun off below
        d.ellipse(x, 150, 11, 5)
    d.group('mid')
    for x in xs[:-1]:                                               # the liquid passed on, step to step
        d.line((x + 20, 62), (x + 52, 62))
        _arrow(d, (x + 20, 62), (x + 52, 62))
    for x in xs:
        d.line((x, vb + 4), (x, 140))
        _arrow(d, (x, vb + 4), (x, 140))
        d.line((x - 14, 78), (x + 14, 78))                          # the liquid's surface
    for i, x in enumerate(xs):                                      # deposited flecks, more for more protein
        for k in range(3 + i % 2):
            d.line((x - 10 + 6 * k, vb - 4), (x - 7 + 6 * k, vb - 6))
    # the two traces
    epts, ppts = [], []
    for x, e, v in zip(xs, eth, ph):
        epts += [(x - 30, ey(e)), (x + 30, ey(e))]
        ppts += [(x - 30, py(v)), (x + 30, py(v))]
    d.line(*epts)
    for a, b in zip(ppts[::2], ppts[1::2]):
        for k in range(0, 60, 8):
            d.line((a[0] + k, a[1]), (min(a[0] + k + 4, b[0]), b[1]))
    d.group('mid')
    for x, n in zip(xs, names):
        d.text(x, 168, n, size=7)
    d.text(xs[0] - 34, 34, 'PLASMA 0 °C', size=7, anchor='start')
    d.text(xs[-1], 34, '−5 °C', size=7)
    d.text(376, g1 - 4, '40% · pH 8', size=7, anchor='end')
    d.text(376, g0 + 10, '0% · pH 4', size=7, anchor='end')
    d.text(24, g1 - 4, 'ETHANOL —  pH - -', size=7, anchor='start')
    return d


def bone_marrow():
    d = D()
    # The 1958 twin procedure in plan: the donor's pelvis seen from behind, an aspiration needle in
    # the posterior iliac crest; the marrow drawn into a syringe, passed through a steel screen into a
    # flask, and run into the recipient's vein. A dose scale above the recipient's arm marks the
    # whole-body radiation given first (850 and 1,140 r). Pelvis proportions are a sketch.
    cx, cy = 92, 168
    d.group('thin')
    d.line((cx, 70), (cx, 270))                                     # the spine's axis
    d.line((20, cy), (176, cy))
    for r in (40, 60):
        d.arc(cx, cy, r, 200, 340, n=24)
    # dose scale, 0 to 1,200 r
    sx0, sx1, sy = 262, 368, 56
    d.line((sx0, sy), (sx1, sy))
    for k in range(0, 1201, 200):
        x = sx0 + (sx1 - sx0) * k / 1200
        d.line((x, sy - 3), (x, sy + 3))
    d.group()
    # the pelvis from behind: two wings (ilia) either side of the sacrum, outline computed as arcs
    for s in (-1, 1):
        pts = []
        for i in range(25):
            a = math.radians(-160 + 140 * i / 24)
            rx, ry = 62, 50
            x = cx + s * (18 + rx * (1 + math.cos(a)) / 2 * 1.2)
            y = cy - 6 + ry * math.sin(a)
            pts.append((x, y))
        d.line(*pts)
        d.line(pts[-1], (cx + s * 22, cy + 46), (cx + s * 12, cy + 70))
        d.line(pts[0], (cx + s * 16, cy + 10))
    d.line((cx - 16, cy - 30), (cx + 16, cy - 30), (cx + 8, cy + 40), (cx - 8, cy + 40), closed=True)   # sacrum
    # the needle into the right posterior crest, and the syringe
    nx, ny = cx + 52, cy - 44
    d.line((nx, ny), (nx + 30, ny - 40))
    d.line((nx + 26, ny - 44), (nx + 34, ny - 36))                  # hub
    d.line((nx + 30, ny - 40), (nx + 44, ny - 58))
    d.line((nx + 38, ny - 62), (nx + 62, ny - 94), (nx + 70, ny - 88), (nx + 46, ny - 56), closed=True)  # barrel
    # the screen and the flask
    fx, fy = 262, 128
    d.line((fx - 22, fy), (fx + 22, fy))
    d.line((fx - 14, fy + 8), (fx - 14, fy + 26), (fx - 30, fy + 70), (fx + 30, fy + 70), (fx + 14, fy + 26), (fx + 14, fy + 8))
    # the drip to the recipient's arm, a vein along it
    d.line((fx, fy + 70), (fx, fy + 92), (330, 232))
    d.curve('M300 244 C330 236 360 236 388 240')
    d.curve('M300 262 C330 256 360 256 388 258')
    d.group('mid')
    for k in range(-18, 20, 6):                                      # the steel screen's mesh
        d.line((fx + k, fy - 4), (fx + k + 4, fy + 4))
    d.line((fx - 26, fy + 56), (fx + 26, fy + 56))                  # marrow in the flask
    d.curve('M306 251 C330 246 360 246 386 249')                     # the vein
    d.line((nx + 76, ny - 92), (fx - 4, fy - 14))
    _arrow(d, (nx + 76, ny - 92), (fx - 4, fy - 14))
    for k in (850, 1140):                                            # the two doses of 1959
        x = sx0 + (sx1 - sx0) * k / 1200
        d.line((x, sy - 10), (x, sy - 3))
        _arrow(d, (x, sy - 14), (x, sy - 3), size=4)
    d.group('mid')
    d.text(cx, cy + 88, 'DONOR TWIN · PELVIS FROM BEHIND', size=7)
    d.text(fx + 26, fy + 2, 'SCREEN', size=7, anchor='start')
    d.text(344, 280, 'RECIPIENT · VEIN', size=7)
    d.text(sx0, sy + 14, '0', size=7)
    d.text(sx1, sy + 14, '1,200 r', size=7)
    d.text(315, sy + 26, 'WHOLE-BODY DOSE', size=7)
    d.text(315, sy - 20, '850 · 1,140 r', size=7)
    return d


def apheresis():
    d = D()
    # The 1965 continuous-flow centrifuge in section, after Freireich, Judson and Levin: blood enters
    # at the top of a spinning vertical annulus and settles outward as it falls, red cells at the
    # outer wall, plasma at the inner, the buffy coat between; three ports draw each off through its
    # own roller pump. Red cells and plasma rejoin and return to the donor's other arm. Not to scale.
    ax, top, bot = 150, 60, 240
    ri, ro = 22, 74                                                  # inner and outer radii of the annulus
    d.group('thin')
    d.line((ax, 30), (ax, 270))                                      # the axis of spin
    for s in (-1, 1):
        d.line((ax + s * ri, top - 10), (ax + s * ri, bot + 10))
    d.arc(ax, 36, 30, 200, 340, n=20)                                # the sense of rotation
    d.group()
    for s in (-1, 1):                                                # the bowl walls
        d.line((ax + s * ri, top), (ax + s * ri, bot))
        d.line((ax + s * ro, top), (ax + s * ro, bot))
    d.line((ax - ro, bot), (ax - ri, bot))
    d.line((ax + ri, bot), (ax + ro, bot))
    # pump heads, three on the right, level with their ports
    pumps = [(300, 100), (300, 160), (300, 220)]
    for px, py in pumps:
        d.circle(px, py, 13)
    # the two arms: out and back
    d.curve('M14 248 C40 240 70 240 96 244')
    d.curve('M14 266 C40 258 70 258 96 262')
    d.curve('M304 268 C330 260 360 260 390 264')
    d.curve('M304 286 C330 278 360 278 390 282')
    d.group('mid')
    # the layers, by depth: red cells hatched against the outer wall, buffy coat a band, plasma open
    for s in (-1, 1):
        for y in range(top + 30, bot, 8):
            x0 = ax + s * (ro - 14 - (y - top) * 0.06)
            d.line((x0, y), (ax + s * ro, y - 4))
        bx = ax + s * (ro - 18)
        d.line((bx, top + 26), (bx - s * 4, bot))
        d.line((bx - s * 3, top + 26), (bx - s * 7, bot))
    # inflow at the top, from the donor through the anticoagulant pump
    d.line((40, 248), (40, 20), (ax + 50, 20), (ax + 50, top + 4))
    _arrow(d, (ax + 50, 20), (ax + 50, top + 4))
    # the three ports, each a tube from its layer straight to its pump
    ports = [(ax + ri + 3, 100), (ax + ro - 17, 160), (ax + ro - 3, 220)]
    for (qx, qy), (px, py) in zip(ports, pumps):
        d.line((qx, qy), (px - 13, py))
        d.circle(qx, qy, 2)
    for px, py in pumps:                                             # rollers
        for a in (0, 120, 240):
            x, y = _pt(px, py, 8, a)
            d.circle(x, y, 2.5)
    # white cells up to the collection bag; plasma and red cells rejoin and go back
    d.line((313, 160), (360, 160), (360, 122))
    d.line((348, 92), (372, 92), (376, 122), (344, 122), closed=True)
    d.line((313, 100), (334, 100), (334, 220))
    d.line((313, 220), (334, 220), (334, 262))
    _arrow(d, (334, 246), (334, 262))
    d.group('mid')
    d.text(ax, bot + 28, 'BOWL · 850 rpm · 190 mL', size=7)
    d.text(254, 96, 'PLASMA', size=7)
    d.text(254, 156, 'BUFFY COAT', size=7)
    d.text(254, 216, 'RED CELLS', size=7)
    d.text(360, 86, 'WHITE CELLS', size=7)
    d.text(56, 238, 'ARM OUT', size=7)
    d.text(366, 258, 'ARM BACK', size=7)
    d.text(46, 14, 'BLOOD + ACD', size=7, anchor='start')
    return d


PLATES = {'apheresis': apheresis, 'bone-marrow': bone_marrow, 'cryoprecipitate': cryoprecipitate, 'fractionation': fractionation}
