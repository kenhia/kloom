"""Plates for In the Blood's trail Clotting, first part (sprint 028): royal-hemophilia, heparin,
prothrombin-time. See plates_for.py."""
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


def _hatch_rect(x0, y0, x1, y1, step=2.0):
    """Diagonal hatching (rising to the right) clipped to a rectangle."""
    segs = []
    w, h = x1 - x0, y1 - y0
    k = -h
    while k < w:
        # the line x - x0 = k + (y1 - y), clipped to the box
        a = (x0 + max(k, 0), y1 - max(-k, 0))
        b = (x0 + min(k + h, w), y1 - min(h, w - k))
        if a != b:
            segs.append([a, b])
        k += step
    return segs


def _hatch_circle(cx, cy, r, step=2.0, half=None):
    """Vertical hatching inside a circle; `half` = 'left' keeps only the left half."""
    segs = []
    x = cx - r + step / 2
    while x < cx + r:
        if half == 'left' and x > cx:
            break
        dy = math.sqrt(max(r * r - (x - cx) ** 2, 0))
        segs.append([(x, cy - dy), (x, cy + dy)])
        x += step
    return segs


# ---------------------------------------------------------------- royal-hemophilia

def royal_hemophilia():
    d = D()
    # Queen Victoria's pedigree, cut down to the lines that carried the gene: squares for men,
    # circles for women; a man with hemophilia hatched solid, a carrier hatched on her left half.
    # Spouses after the first generation are left out; every man drawn hatched is one of the nine.
    s = 5                                                        # half a symbol
    gy = [44, 110, 176, 242]                                     # the four generations
    people = {}

    def man(key, x, y, sick=False):
        people[key] = (x, y, 'm', sick)

    def woman(key, x, y, carrier=None):
        people[key] = (x, y, 'f', carrier)

    woman('victoria', 188, gy[0], True)
    man('albert', 212, gy[0])
    kids = [('vicky', 'f', None), ('edward', 'm', False), ('alice', 'f', True), ('alfred', 'm', False),
            ('helena', 'f', '?'), ('louise', 'f', None), ('arthur', 'm', False), ('leopold', 'm', True),
            ('beatrice', 'f', True)]
    xs = [40 + 40 * i for i in range(9)]
    for (k, sex, st), x in zip(kids, xs):
        (woman if sex == 'f' else man)(k, x, gy[1], st)
    woman('irene', 92, gy[2], True)
    man('friedrich', 120, gy[2], True)
    woman('alix', 148, gy[2], True)
    woman('alice-albany', 320, gy[2], True)
    woman('ena', 352, gy[2], True)
    man('leopold-m', 380, gy[2], True)
    man('waldemar', 80, gy[3], True)
    man('henry', 104, gy[3], True)
    man('alexei', 148, gy[3], True)
    man('rupert', 320, gy[3], True)
    man('alfonso', 340, gy[3], True)
    man('gonzalo', 364, gy[3], True)
    descent = [('victoria', ['vicky', 'edward', 'alice', 'alfred', 'helena', 'louise', 'arthur',
                             'leopold', 'beatrice'], (200, gy[0])),
               ('alice', ['irene', 'friedrich', 'alix'], None),
               ('leopold', ['alice-albany'], None),
               ('beatrice', ['ena', 'leopold-m'], None),
               ('irene', ['waldemar', 'henry'], None),
               ('alix', ['alexei'], None),
               ('alice-albany', ['rupert'], None),
               ('ena', ['alfonso', 'gonzalo'], None)]

    d.group('thin')
    for y in gy:                                                 # a rule for each generation
        d.line((26, y), (392, y))
    d.group('mid')
    # the lines of descent: down from the parent (or the couple's marriage line), across, and down
    d.line((188 + s, gy[0]), (212 - s, gy[0]))
    for parent, children, start in descent:
        px, py = start if start else people[parent][:2]
        bar = (py + people[children[0]][1]) / 2
        d.line((px, py + (0 if start else s)), (px, bar))
        cxs = [people[c][0] for c in children]
        if len(cxs) > 1 or cxs[0] != px:
            d.line((min(cxs + [px]), bar), (max(cxs + [px]), bar))
        for c in children:
            cx, cy = people[c][:2]
            d.line((cx, bar), (cx, cy - s))
    d.group()
    for k, (x, y, sex, st) in people.items():
        if sex == 'm':
            d.line((x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s), closed=True)
        else:
            d.circle(x, y, s)
    d.group('mid')
    for k, (x, y, sex, st) in people.items():
        if sex == 'm' and st:
            d.lines(_hatch_rect(x - s, y - s, x + s, y + s, step=2.0))
        elif sex == 'f' and st is True:
            d.lines(_hatch_circle(x, y, s, step=1.8, half='left'))
            d.line((x, y - s), (x, y + s))
        elif sex == 'f' and st == '?':
            d.text(x, y + 2.5, '?', size=7)
    d.group('mid')
    for i, y in enumerate(gy):
        d.text(14, y + 2.5, ['I', 'II', 'III', 'IV'][i], size=7)
    d.text(200, gy[0] - 12, 'VICTORIA · ALBERT', size=7)
    d.text(people['leopold'][0] + 4, gy[1] + 20, 'LEOPOLD', size=7, anchor='start')
    d.text(people['alexei'][0], gy[3] + 18, 'ALEXEI', size=7)
    d.text(people['alix'][0] + 10, gy[2] + 3, 'ALIX', size=7, anchor='start')
    d.text(260, 284, 'F9 IVS3-3A>G · HEMOPHILIA B', size=7)
    return d


# ---------------------------------------------------------------- heparin

def _tube(d, base, ang, length=96, r=9):
    """A test tube in outline, its closed end at `base`, its axis at `ang` degrees from straight up
    (positive leans right). Returns a function mapping (along, across) to page coordinates."""
    a = math.radians(ang)
    ux, uy = math.sin(a), -math.cos(a)                           # up the axis
    vx, vy = math.cos(a), math.sin(a)                            # across, to the right

    def at(t, c):
        return base[0] + ux * t + vx * c, base[1] + uy * t + vy * c

    wall_l = [at(length, -r), at(r, -r)]
    wall_r = [at(r, r), at(length, r)]
    bottom = [at(r - r * math.sin(math.radians(ph)), -r * math.cos(math.radians(ph)))
              for ph in range(0, 181, 10)]                      # the rounded end, a semicircle
    d.line(*wall_l, *bottom, *wall_r)
    d.line(at(length, -r - 2), at(length, -r))
    d.line(at(length, r), at(length, r + 2))
    return at


def heparin():
    d = D()
    # McLean's test of 1916, three tubes of 8 drops oxalated plasma + 3 drops serum + 3 drops of
    # the thing tested, tipped 50 degrees. A clot holds its surface square to the tube; a liquid
    # keeps its surface level. Water: a soft, sliding clot. Heart cephalin: solid. Cuorin: fluid.
    tilt = 50
    bases = [(70, 238), (186, 238), (302, 238)]
    fill = 40                                                    # the column's height when upright
    d.group('thin')
    d.line((24, 250), (380, 250))                                # the bench
    for bx, by in bases:
        d.line((bx, by + 10), (bx, by - 120))                    # the vertical each tube left
        d.arc(bx, by, 70, -90, -90 + tilt, n=16)                 # the angle it was tipped through
    d.group()
    r = 11
    ats = [_tube(d, (bx, by), tilt, length=104, r=r) for bx, by in bases]
    d.group('mid')
    # 1. control: the contents part set, part slid, so the surface is skewed between the two
    # 2. cephalin: solid, surface still square to the axis
    at = ats[1]
    d.line(at(fill, -r), at(fill, r))
    d.lines([[at(t, -r + 1), at(t, r - 1)] for t in range(12, fill, 5)])
    # 3. cuorin: liquid, surface level. The level is where the volume of the upright column fits:
    # for a tilted cylinder of radius r the level surface passes through the axis at height `fill`.
    for i, at in ((0, ats[0]), (2, ats[2])):
        a = math.radians(tilt)
        if i == 2:
            k = math.tan(a)                                       # level: across-offset per along
            p, q = at(fill - r * k, -r), at(fill + r * k, r)
        else:
            k = math.tan(a) * 0.5                                 # halfway: a clot sliding
            p, q = at(fill - r * k, -r), at(fill + r * k, r)
        d.line(p, q)
    d.lines([[ats[0](t, -r + 1), ats[0](t, r - 1)] for t in range(12, 30, 6)])
    d.group('mid')
    for (bx, by), name, t in zip(bases, ('WATER', 'HEART CEPHALIN', 'CUORIN'),
                                 ('SLIDING CLOT 9 MIN', 'SOLID CLOT 3 MIN', 'FLUID AT 6 H')):
        d.text(bx + 34, 268, name, size=7)
        d.text(bx + 34, 280, t, size=7)
    d.text(200, 26, '8 DROPS PLASMA · 3 SERUM · 3 TEST', size=7)
    d.text(bases[0][0] + 6, 112, '50°', size=7, anchor='start')
    return d


# ---------------------------------------------------------------- prothrombin-time

def prothrombin_time():
    d = D()
    # The one-stage prothrombin time by hand: a 37 °C water bath in section, a 13 x 100 mm tube
    # lifted out and tipped to see whether the plasma still flows, and the stopwatch started when
    # the calcium went in, stopped at the clot (23 s, Quick's normal plasma in 1935).
    bath = (34, 150, 190, 262)                                    # x0, y0, x1, y1
    water = 176
    sw = (300, 132, 62)                                          # the stopwatch: centre and radius
    stop_s = 23
    d.group('thin')
    d.line((bath[0] - 8, water), (bath[2] + 8, water))            # the water line, carried out
    d.circle(sw[0], sw[1], sw[2] + 8)
    d.line((sw[0], sw[1]), _pt(sw[0], sw[1], sw[2] + 8, -90))
    d.group()
    # the bath: an open tank
    d.line((bath[0], bath[1]), (bath[0], bath[3]), (bath[2], bath[3]), (bath[2], bath[1]))
    # tubes standing in a rack in the bath
    for x in (60, 84, 108):
        d.line((x - 5, 128), (x - 5, 236))
        d.arc(x, 236, 5, 180, 0, n=10)
        d.line((x + 5, 236), (x + 5, 128))
    # the stopwatch case, crown and dial
    d.circle(sw[0], sw[1], sw[2])
    d.line((sw[0] - 6, sw[1] - sw[2]), (sw[0] - 6, sw[1] - sw[2] - 10), (sw[0] + 6, sw[1] - sw[2] - 10),
           (sw[0] + 6, sw[1] - sw[2]))
    d.line((sw[0] - 9, sw[1] - sw[2] - 10), (sw[0] + 9, sw[1] - sw[2] - 10))
    # the tube lifted out and tipped 60 degrees: the clot holds its surface square to the tube
    at = _tube(d, (150, 112), 60, length=88, r=6)
    d.group('mid')
    d.lines([[(x, water + 2), (x + 8, water + 2)] for x in range(bath[0] + 4, bath[2] - 8, 16)])
    d.lines([[(x, water + 8), (x + 8, water + 8)] for x in range(bath[0] + 12, bath[2] - 8, 16)])
    for x in (60, 84, 108):                                       # plasma in each tube, level
        d.line((x - 5, 210), (x + 5, 210))
    d.line(at(30, -6), at(30, 6))
    d.lines([[at(t, -5), at(t, 5)] for t in range(8, 30, 5)])
    # the dial: 60 seconds, a long tick each 5
    ticks = []
    for i in range(60):
        a = -90 + 6 * i
        r0 = sw[2] - (9 if i % 5 == 0 else 5)
        ticks.append([_pt(sw[0], sw[1], r0, a), _pt(sw[0], sw[1], sw[2] - 2, a)])
    d.lines(ticks)
    d.group()
    hand = -90 + 6 * stop_s
    d.line(_pt(sw[0], sw[1], 10, hand + 180), _pt(sw[0], sw[1], sw[2] - 12, hand))
    d.circle(sw[0], sw[1], 2.5)
    d.group('mid')
    d.arc(sw[0], sw[1], sw[2] - 22, -90, hand, n=24)             # the time swept
    _arrow(d, _pt(sw[0], sw[1], sw[2] - 22, hand - 6), _pt(sw[0], sw[1], sw[2] - 22, hand), size=4)
    d.group('mid')
    d.text(sw[0], sw[1] + 26, '23 S', size=7)
    d.text(sw[0], sw[1] - sw[2] + 20, '0', size=7)
    d.text(112, 278, 'WATER BATH 37 °C', size=7)
    d.text(150, 52, 'TIP TO SEE IT HOLD', size=7)
    d.text(300, 230, '0.1 PLASMA · 0.1 THROMBOPLASTIN', size=7)
    d.text(300, 242, '+ CALCIUM CHLORIDE, M/40', size=7)
    return d


PLATES = {'royal-hemophilia': royal_hemophilia, 'heparin': heparin, 'prothrombin-time': prothrombin_time}
