"""Plates for In the Blood's trail Blood at war, its last three frames (sprint 028, part war2). See plates_for.py."""
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


def _xyz(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def _great_circle(a, b, n=40):
    """Points (lat, lon east, 0..360) along the great circle from a to b, by spherical interpolation."""
    p, q = _xyz(*a), _xyz(*b)
    w = math.acos(max(-1, min(1, sum(i * j for i, j in zip(p, q)))))
    out = []
    for k in range(n + 1):
        t = k / n
        s0, s1 = math.sin((1 - t) * w) / math.sin(w), math.sin(t * w) / math.sin(w)
        x, y, z = (s0 * i + s1 * j for i, j in zip(p, q))
        out.append((math.degrees(math.asin(z)), math.degrees(math.atan2(y, x)) % 360))
    return out


def vietnam_blood():
    d = D()
    # The route of a unit of blood in 1966-70, from McGuire AFB by Elmendorf and Yokota to Camp Zama
    # and on to Cam Ranh Bay, as great circles on an equirectangular grid (east longitude 100-290),
    # and below it a unit's 21 days of life, with the 4-7 days it took to reach Vietnam (Neel 1973).
    lon0, lon1, x0, x1 = 100, 290, 30, 370
    k = (x1 - x0) / (lon1 - lon0)

    def px(lat, lon):
        return x0 + (lon % 360 - lon0) * k, 160 - lat * k

    stations = [('MCGUIRE', 40.02, 285.4), ('ELMENDORF', 61.25, 210.2),
                ('ZAMA', 35.5, 139.4), ('CAM RANH', 11.95, 109.2)]
    d.group('thin')
    for lat in (0, 20, 40, 60):                                    # parallels
        d.line(px(lat, lon0), px(lat, lon1))
    for lon in range(120, 291, 30):                                # meridians
        d.line(px(0, lon), px(70, lon))
    # the day scale: one tick a day for 21 days
    t0, t1, ty = 40, 360, 236
    day = (t1 - t0) / 21
    for i in range(22):
        h = 7 if i % 7 == 0 else 3
        d.line((t0 + i * day, ty), (t0 + i * day, ty - h))
    d.group()
    # the route, leg by leg, each a great circle
    legs = list(zip(stations, stations[1:]))
    for (_, la0, lo0), (_, la1, lo1) in legs:
        pts = [px(la, lo) for la, lo in _great_circle((la0, lo0), (la1, lo1))]
        d.line(*pts)
    # a unit's life: the bar of 21 days
    d.line((t0, ty), (t1, ty))
    d.line((t0, ty + 10), (t1, ty + 10))
    d.line((t0, ty), (t0, ty + 10))
    d.line((t1, ty), (t1, ty + 10))
    d.group('mid')
    for (_, la0, lo0), (_, la1, lo1) in legs:                      # arrowheads near each landing
        g = _great_circle((la0, lo0), (la1, lo1))
        _arrow(d, px(*g[-4]), px(*g[-1]))
    for _, la, lo in stations:
        x, y = px(la, lo)
        d.circle(x, y, 3)
    # the arrival window, 4 to 7 days, hatched; the days in Vietnam to the end
    for i in range(12):
        x = t0 + 4 * day + i * 3 * day / 12
        d.line((x, ty + 10), (x + 4, ty))
    d.line((t0 + 4 * day, ty + 18), (t0 + 7 * day, ty + 18))
    d.line((t0 + 4 * day, ty + 14), (t0 + 4 * day, ty + 22))
    d.line((t0 + 7 * day, ty + 14), (t0 + 7 * day, ty + 22))
    d.group('mid')
    for name, la, lo in stations:
        x, y = px(la, lo)
        anchor = 'end' if name == 'MCGUIRE' else 'start'
        dx = -6 if anchor == 'end' else 6
        dy = -6 if name == 'ELMENDORF' else 12
        d.text(x + dx, y + dy, name, size=7, anchor=anchor)
    d.text(*px(1.5, 182), '180°', size=7)
    d.text(t0, ty - 11, 'DAY 0', size=7)
    d.text(t1, ty - 11, '21', size=7)
    d.text(t0 + 5.5 * day, ty + 30, 'ARRIVES 4–7', size=7)
    d.text(t1, ty + 30, 'OUTDATED', size=7, anchor='end')
    return d


def walking_blood_bank():
    d = D()
    # A field collection on a trip scale: the bag hangs from one arm of a beam pivoted on a post, a
    # counterweight set to 585 g on the other; when the bag reaches 585 g (450 mL of blood with its
    # anticoagulant) the beam tips. Below, the sample tubes drawn with it: two red-top, four purple-top
    # (JTS CPG 21, 2018, appendix C). Not to scale.
    piv = (200, 92)
    tilt = math.radians(5)                                        # the bag side has just tipped down
    arm = 112

    def on_beam(s):
        return piv[0] + s * math.cos(tilt), piv[1] - s * math.sin(tilt)

    left, right = on_beam(-arm), on_beam(arm)
    d.group('thin')
    d.line((piv[0] - arm - 14, piv[1]), (piv[0] + arm + 14, piv[1]))     # the level line
    d.arc(piv[0], piv[1], 60, 175, 180, n=8)                             # the angle it tipped through
    for s in (-arm, arm):                                                # equal arms, dimensioned
        x = piv[0] + s
        d.line((x, piv[1] - 22), (x, piv[1] - 14))
    d.line((piv[0] - arm, piv[1] - 18), (piv[0] + arm, piv[1] - 18))
    d.line((piv[0], piv[1] - 22), (piv[0], piv[1] - 14))
    d.group()
    # the post and its base
    d.line((piv[0] - 50, 200), (piv[0] + 50, 200))
    d.line((piv[0] - 6, 200), (piv[0] - 4, piv[1] + 6), (piv[0] + 4, piv[1] + 6), (piv[0] + 6, 200))
    d.circle(piv[0], piv[1], 4)
    # the beam
    d.line(left, right)
    # the bag, hung from the left end: a rounded pouch
    bx, by, bw, bh = left[0], left[1] + 22, 64, 78
    d.line((bx, left[1]), (bx, by - 6))
    d.line((bx - bw / 2 + 8, by), (bx + bw / 2 - 8, by))
    d.arc(bx + bw / 2 - 8, by + 8, 8, -90, 0, n=8)
    d.line((bx + bw / 2, by + 8), (bx + bw / 2, by + bh - 10))
    d.arc(bx + bw / 2 - 10, by + bh - 10, 10, 0, 90, n=8)
    d.line((bx + bw / 2 - 10, by + bh), (bx - bw / 2 + 10, by + bh))
    d.arc(bx - bw / 2 + 10, by + bh - 10, 10, 90, 180, n=8)
    d.line((bx - bw / 2, by + bh - 10), (bx - bw / 2, by + 8))
    d.arc(bx - bw / 2 + 8, by + 8, 8, 180, 270, n=8)
    # the counterweight on the right arm
    cx, cy = right
    d.line((cx - 10, cy + 4), (cx + 10, cy + 4), (cx + 10, cy + 26), (cx - 10, cy + 26), closed=True)
    d.line((cx, cy), (cx, cy + 4))
    d.group('mid')
    # the blood's level in the bag, and the donor line leaving it with a clamp on it
    d.line((bx - bw / 2 + 4, by + 22), (bx + bw / 2 - 4, by + 22))
    for i in range(7):
        y = by + 30 + i * 7
        d.line((bx - bw / 2 + 6, y), (bx + bw / 2 - 6, y))
    tube = [(bx - 12, by), (bx - 26, by - 14), (bx - 50, by - 6), (bx - 66, by + 40), (bx - 70, by + 96)]
    d.line(*tube)
    d.line((bx - 74, by + 60), (bx - 62, by + 64))                       # a hemostat across the line
    # the sample tubes: two red-top, four purple-top
    for i in range(6):
        x = 196 + i * 30
        d.line((x - 6, 222), (x - 6, 270))
        d.arc(x, 270, 6, 180, 0, n=10)
        d.line((x + 6, 270), (x + 6, 222))
        d.line((x - 8, 214), (x + 8, 214), (x + 8, 222), (x - 8, 222), closed=True)
        if i < 2:                                                        # red top: plain cap
            d.line((x - 8, 218), (x + 8, 218))
        else:                                                            # purple top: cross-hatched cap
            d.line((x - 6, 214), (x - 2, 222))
            d.line((x + 2, 214), (x + 6, 222))
    d.group('mid')
    d.text(bx, by + bh + 14, '450 mL', size=7)
    d.text(cx, cy + 40, '585 g', size=7)
    d.text(bx - 70, by + 112, 'TO DONOR', size=7, anchor='start')
    d.text(211, 286, '2 RED', size=7)
    d.text(301, 286, '4 PURPLE', size=7)
    return d


def whole_blood_returns():
    d = D()
    # A titration of a group O donor's plasma against group A1 red cells, as a rack of ten tubes:
    # doubling dilutions in saline from 1 in 1 to 1 in 512, each with the cells added, spun at once
    # and read for clumping. The grades are invented for the example: the last tube graded 1+ is
    # 1 in 64, so the titre is 64, under a threshold of 256. Not to scale.
    dil = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    grade = [4, 4, 3, 3, 2, 2, 1, 0.5, 0, 0]
    xs = [34 + i * 37 for i in range(10)]
    top, bot = 96, 210
    d.group('thin')
    d.line((18, 118), (382, 118))                                  # the rack's top rail
    d.line((18, 232), (382, 232))                                  # its base
    for i in range(9):                                             # the transfers, tube to tube
        x0, x1 = xs[i], xs[i + 1]
        d.arc((x0 + x1) / 2, top - 8, (x1 - x0) / 2, 180, 360, n=14, ry=14)
    tx = (xs[7] + xs[8]) / 2                                       # the threshold, between 128 and 256
    for y in range(64, 248, 8):
        d.line((tx, y), (tx, y + 4))
    d.group()
    for x in xs:                                                   # the tubes
        d.line((x - 10, top), (x - 10, bot - 10))
        d.arc(x, bot - 10, 10, 180, 0, n=14)
        d.line((x + 10, bot - 10), (x + 10, top))
    d.group('mid')
    for i in range(9):
        x1 = xs[i + 1]
        _arrow(d, (x1 - 3, top - 15), (x1, top - 8), size=4)
    # what each tube shows after the spin, read against the light
    for x, g in zip(xs, grade):
        cy = bot - 16
        if g >= 4:                                                 # one solid clump
            d.circle(x, cy, 6)
            d.circle(x, cy, 3)
        elif g >= 3:                                               # a few large clumps
            for a in (0, 120, 240):
                px, py = _pt(x, cy, 4, a)
                d.circle(px, py, 3)
        elif g >= 2:                                               # medium clumps
            for a in range(0, 360, 72):
                px, py = _pt(x, cy, 5, a)
                d.circle(px, py, 1.8)
        elif g >= 1:                                               # small clumps
            for r, n in ((3, 5), (7, 8)):
                for j in range(n):
                    px, py = _pt(x, cy, r, j * 360 / n)
                    d.circle(px, py, 0.9)
        elif g > 0:                                                # barely granular: specks on a smooth haze
            d.line((x - 7, cy + 2), (x + 7, cy + 2))
            for j in range(5):
                d.circle(x - 6 + j * 3, cy - 2, 0.5)
        else:                                                      # no clumping: cells evenly suspended
            for y in range(top + 40, bot - 4, 8):
                d.line((x - 7, y), (x + 7, y))
    d.group('mid')
    for x, n in zip(xs, dil):
        d.text(x, top - 26, str(n), size=7)
    labels = ['4+', '4+', '3+', '3+', '2+', '2+', '1+', 'w+', '0', '0']
    for x, s in zip(xs, labels):
        d.text(x, 248, s, size=7)
    d.text(18, top - 40, '1 IN', size=7, anchor='start')
    d.text(xs[6], 266, 'TITRE 64', size=7)
    d.text(tx + 4, 56, 'LOW < 256', size=7, anchor='start')
    return d


PLATES = {'vietnam-blood': vietnam_blood, 'walking-blood-bank': walking_blood_bank,
          'whole-blood-returns': whole_blood_returns}
