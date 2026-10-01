"""Plates for the middle of Keeping Watch's modern profession: polio-icu, nurse-practitioner, hospice
(sprint 030, part prof2). See plates_for.py."""
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


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def _rbox(d, x, y, w, h, r):
    """A box with rounded corners, as one path."""
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        pts += [_pt(cx, cy, r, a0 + 90 * i / 6) for i in range(7)]
    d.line(*pts, closed=True)


def polio_icu():
    d = D()
    # Two ways to breathe for a paralysed patient, after the papers that describe them. Above, the
    # Drinker tank (Drinker and Shaw, 1929) in elevation: the body sealed in a cylinder, the head out
    # through a rubber collar, the pump at the foot lowering and raising the pressure round the chest.
    # Below, the Copenhagen circuit of 1952 (Lassen; Ibsen; Andersen and Ibsen, 1954): a cuffed tube
    # through a tracheotomy, a soda-lime canister, the rubber bag squeezed by hand, a valve, and a
    # cylinder of half oxygen and half nitrogen. Proportions are schematic.
    ax = 88                                                               # the tank's axis
    x0, x1, R = 118, 330, 38                                              # lid, foot, radius
    d.group('thin')
    d.line((60, ax), (372, ax))                                           # the axis
    d.line((20, 168), (380, 168))                                         # the line between the two
    d.line((60, 196), (60, 290))                                          # the trachea's axis
    d.group()
    # the tank: a cylinder in elevation, closed by a domed foot, open to the lid at the head
    d.line((x0, ax - R), (x1, ax - R))
    d.line((x0, ax + R), (x1, ax + R))
    d.arc(x1, ax, 12, -90, 90, n=24, ry=R)
    d.line((x0, ax - R - 4), (x0, ax + R + 4))                            # the lid
    d.line((x0 - 4, ax - R - 4), (x0 - 4, ax + R + 4))
    # the collar, the head through it on its rest
    d.line((x0 - 4, ax - 8), (x0 - 14, ax - 7), (x0 - 14, ax + 7), (x0 - 4, ax + 8))
    d.circle(x0 - 30, ax - 2, 14)
    d.line((x0 - 56, ax + 16), (x0 - 4, ax + 16))                         # the head rest
    d.line((x0 - 50, ax + 16), (x0 - 50, ax + 34))
    # the stand and its wheels
    for x in (x0 + 30, x1 - 30):
        d.line((x, ax + R), (x, ax + R + 6))
        d.circle(x, ax + R + 10, 4)
    # the pump at the foot, joined by a hose
    _box(d, 346, 112, 34, 26)
    d.line((x1 + 12, ax + 4), (352, ax + 4), (352, 112))
    d.group('mid')
    # the body inside, and the portholes along the side
    d.ellipse(x0 + 48, ax + 2, 34, 15)                                    # chest
    d.line((x0 + 82, ax - 6), (x1 - 20, ax - 4))
    d.line((x0 + 82, ax + 10), (x1 - 20, ax + 8))
    d.line((x0 - 14, ax), (x0 + 14, ax))                                  # neck
    for x in (x0 + 112, x0 + 152, x0 + 192):
        d.circle(x, ax - R + 14, 7)
    for s in (-1, 1):                                                     # the chest drawn out as the pressure falls
        _arrow(d, (x0 + 48, ax + 2 + s * 17), (x0 + 48, ax + 2 + s * 27), 4)
    # below: the trachea in section, the tube through the tracheotomy, its cuff sealing the airway
    d.group()
    tx, ty = 60, 212
    d.line((tx - 9, 196), (tx - 9, 290))
    d.line((tx + 9, 196), (tx + 9, 207))
    d.line((tx + 9, 219), (tx + 9, 290))
    d.line((tx + 30, ty - 4), (tx + 3, ty - 4), (tx - 3, ty + 4), (tx - 3, 270))
    d.line((tx + 30, ty + 4), (tx + 9, ty + 4))
    d.line((tx + 3, ty + 8), (tx + 3, 270))
    d.ellipse(tx, 252, 9, 7)                                              # the cuff
    # the canister of soda lime, the bag at one end, the valve at the other
    cx0, cy0 = 150, 200
    _rbox(d, cx0, cy0, 70, 24, 5)
    d.line((tx + 30, ty), (cx0 - 14, ty), (cx0 - 14, cy0 + 12), (cx0, cy0 + 12))
    d.ellipse(cx0 + 112, cy0 + 12, 30, 15)                                # the bag
    d.line((cx0 + 70, cy0 + 12), (cx0 + 82, cy0 + 12))
    d.circle(cx0 - 14, cy0 - 6, 5)                                         # the valve
    d.line((cx0 - 14, cy0 - 1), (cx0 - 14, cy0 + 12))
    # the cylinder of oxygen and nitrogen, with its flowmeter, feeding the canister
    _rbox(d, 330, 196, 30, 90, 10)
    _box(d, 337, 178, 16, 18)
    d.line((337, 187), (318, 187), (318, 236), (cx0 + 35, 236), (cx0 + 35, cy0 + 24))
    d.group('mid')
    for i in range(5):                                                    # the soda-lime granules
        for j in range(2):
            d.circle(cx0 + 10 + 12.5 * i, cy0 + 7 + 10 * j, 2.2)
    for k in range(4):                                                    # the bag's folds
        x = cx0 + 96 + 10 * k
        h = 15 * math.sqrt(max(0, 1 - ((x - cx0 - 112) / 30) ** 2)) - 3
        d.line((x, cy0 + 12 - h), (x, cy0 + 12 + h))
    _arrow(d, (cx0 + 112, cy0 - 14), (cx0 + 112, cy0 - 4), 4)            # the squeeze
    _arrow(d, (cx0 + 112, cy0 + 38), (cx0 + 112, cy0 + 28), 4)
    _arrow(d, (cx0 + 58, 236), (cx0 + 45, 236), 4)                        # fresh gas in
    d.group('mid')
    d.text(224, 30, 'TANK · PRESSURE ROUND THE BODY', size=7)
    d.text(224, ax + R + 30, 'UP TO ±60 CM WATER · 10–40 A MINUTE', size=7)
    d.text(x0 - 30, ax + 50, 'COLLAR', size=7)
    d.text(363, 150, 'PUMP', size=7)
    d.text(214, 184, 'BAG · PRESSURE INTO THE TRACHEA', size=7)
    d.text(tx + 4, 296, 'CUFF', size=7)
    d.text(cx0 + 35, 260, 'SODA LIME', size=7)
    d.text(cx0 + 112, 260, 'BAG', size=7)
    d.text(345, 298, 'O₂ 50 · N₂ 50', size=7)
    d.text(cx0 + 35, 274, '5–6 L/MIN', size=7)
    return d


def nurse_practitioner():
    d = D()
    # Above, the Colorado course of 1965 on its time line (Silver, Ford and Stearly, 1967, as Hoekelman
    # summarises it): four months at the Medical Center, then twenty in practice in the community, one
    # tick a month. Below, the visit as the 1967 paper divides the work: the nurse examines the child and
    # sorts what she finds three ways; what needs a physician goes to one. A schematic, not a protocol.
    x0, x1, y = 40, 360, 64
    m = (x1 - x0) / 24
    d.group('thin')
    for k in range(25):
        d.line((x0 + k * m, y - 4), (x0 + k * m, y + 4))
    d.line((x0, y + 26), (x1, y + 26))
    for k in (0, 4, 24):
        d.line((x0 + k * m, y + 20), (x0 + k * m, y + 32))
    d.line((40, 120), (360, 120))
    d.group()
    d.line((x0, y), (x1, y))
    _box(d, x0, y - 14, 4 * m, 10)
    _box(d, x0 + 4 * m, y - 14, 20 * m, 10)
    # the visit: the child, the examination, the sorting, three outcomes and the physician
    cy = 210
    d.circle(56, cy, 16)
    d.circle(56, cy - 5, 5)
    d.arc(56, cy + 9, 9, 200, 340, n=12)
    _rbox(d, 92, cy - 16, 70, 32, 5)
    sx = 200
    d.line((sx, cy - 22), (sx + 22, cy), (sx, cy + 22), (sx - 22, cy), closed=True)
    ys = (cy - 58, cy, cy + 58)
    for yy in ys:
        _rbox(d, 250, yy - 13, 74, 26, 5)
    _rbox(d, 340, cy + 20, 50, 70, 5)                                     # the physician
    d.group('mid')
    _arrow(d, (72, cy), (92, cy), 4)
    d.line((72, cy), (92, cy))
    d.line((162, cy), (178, cy))
    _arrow(d, (162, cy), (178, cy), 4)
    for yy in ys:
        d.line((sx + 22, cy), (232, cy), (232, yy), (250, yy))
        _arrow(d, (232, yy), (250, yy), 4)
    for yy in ys[1:]:
        d.line((324, yy), (332, yy), (332, cy + 40), (340, cy + 40))
        _arrow(d, (332, cy + 40), (340, cy + 40), 4)
    d.group('mid')
    d.text(x0 + 2 * m, y - 20, '4 MONTHS', size=7)
    d.text(x0 + 14 * m, y - 20, '20 MONTHS', size=7)
    d.text(x0 + 2 * m, y + 44, 'MEDICAL CENTER', size=7)
    d.text(x0 + 14 * m, y + 44, 'IN PRACTICE IN THE COMMUNITY', size=7)
    d.text(200, 26, 'COLORADO · 1965', size=7)
    d.text(56, cy + 30, 'CHILD', size=7)
    d.text(127, cy - 2, 'HISTORY', size=7)
    d.text(127, cy + 8, 'EXAMINE', size=7)
    d.text(sx, cy + 36, 'SORT', size=7)
    d.text(287, ys[0] + 3, 'WELL CHILD', size=7)
    d.text(287, ys[1] + 3, 'APPRAISE', size=7)
    d.text(287, ys[2] + 3, 'EMERGENCY', size=7)
    d.text(365, cy + 58, 'MD', size=7)
    d.text(287, ys[0] - 20, 'SHE CARES FOR IT', size=7)
    return d


def _level(t, doses, k):
    """A schematic drug level at hour t: each dose adds 1 and decays exponentially at rate k."""
    return sum(math.exp(-k * (t - t0)) for t0 in doses if t >= t0)


def hospice():
    d = D()
    # Saunders's rule drawn on its axes, with invented numbers: one drug, one dose, a half-life of
    # three hours. By the clock (a dose every four hours, from 06:00) the level never
    # falls to the line where pain returns. On demand, a dose is given only once the pain is back and
    # has been asked for, an hour after the level crosses the line, so the patient lives on a sawtooth
    # with an hour of pain in every cycle. Above it, the day's six doses on a clock face.
    k = math.log(2) / 3.0
    x0, x1, yb, ys = 60, 380, 270, 60                                     # 24 hours across; level 0 at yb
    def X(t):
        return x0 + (x1 - x0) * t / 24
    def Y(v):
        return yb - ys * v
    thr = 0.35
    clock = [0, 4, 8, 12, 16, 20]
    demand = [0]
    t = 0.0
    while t < 24:                                                         # the next dose an hour after the line is crossed
        t += 0.02
        if _level(t, demand, k) < thr and t - demand[-1] > 0.5:
            cross = t
            demand.append(round(cross + 1.0, 2))
            t = demand[-1]
    demand = [x for x in demand if x < 24]
    d.group('thin')
    d.line((x0, yb), (x1, yb))
    d.line((x0, yb), (x0, yb - 120))
    for h in range(0, 25, 4):
        d.line((X(h), yb), (X(h), yb + 5))
    d.line((x0, Y(thr)), (x1, Y(thr)))                                    # where pain returns
    for h in clock:
        d.line((X(h), yb), (X(h), Y(2.0)))
    # the clock face, with the doses every four hours
    cx, cy, r = 220, 58, 34
    d.circle(cx, cy, r + 6)
    d.group()
    d.circle(cx, cy, r)
    for h in range(24):
        a = h * 15 - 90
        d.line(_pt(cx, cy, r, a), _pt(cx, cy, r - (5 if h % 6 else 9), a))
    for h in (6, 10, 14, 18, 22, 2):
        a = h * 15 - 90
        d.circle(*_pt(cx, cy, r + 6, a), 2.5)
    d.line(_pt(cx, cy, 0, 0), _pt(cx, cy, r - 12, 6 * 15 - 90))
    # the two curves: by the clock (full weight), on demand (mid)
    pts = [(X(i / 20), Y(_level(i / 20, clock, k))) for i in range(0, 24 * 20 + 1)]
    d.line(*pts)
    d.group('mid')
    pts = [(X(i / 20), Y(_level(i / 20, demand, k))) for i in range(0, 24 * 20 + 1)]
    d.line(*pts)
    d.group('mid')
    d.text(cx, cy + r + 18, 'EVERY 4 HOURS · 06 10 14 18 22 02', size=7)
    d.text(x1 - 4, Y(thr) + 12, 'PAIN RETURNS', size=7, anchor='end')
    for h in range(0, 25, 8):
        d.text(X(h), yb + 14, f'{(h + 6) % 24:02d}:00', size=7)
    d.text(X(12), yb + 26, 'ONE DAY · SCHEMATIC, INVENTED NUMBERS', size=7)
    d.text(x0 - 4, yb - 112, 'LEVEL', size=7, anchor='end')
    d.text(X(1.2), Y(2.15), 'BY THE CLOCK', size=7, anchor='start')
    d.text(X(1.2), Y(thr) + 12, 'ON DEMAND', size=7, anchor='start')
    return d


PLATES = {
    'polio-icu': polio_icu,
    'nurse-practitioner': nurse_practitioner,
    'hospice': hospice,
}
