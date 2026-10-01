"""Plates for In the Blood's trail Blood at war, its first three frames (sprint 028, part war1).
See plates_for.py."""
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


def _dashed(d, p, q, dash=5, gap=4):
    """A dashed straight line from p to q, as one stroke of many short segments."""
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    segs, s = [], 0.0
    while s < L:
        e = min(s + dash, L)
        segs.append([(p[0] + ux * s, p[1] + uy * s), (p[0] + ux * e, p[1] + uy * e)])
        s = e + gap
    d.lines(segs)


def whole_blood_wwii():
    d = D()
    # Left: the 1,000-mL airlift bottle in section, 500 mL of Alsever's solution and 500 mL of
    # blood, with its stopper's two tubes clamped. Right: one bottle's 21-day life laid out on a
    # day scale, with the unrefrigerated crossing dashed. The days to France are a sketch drawn
    # from Kendrick's figures (3 days hoped for; 6 1/2 days on one winter trip), not a record.
    bx0, bx1, btop, bbase = 44, 112, 96, 262          # the bottle's body
    y500 = bbase - (bbase - btop) * 0.5               # the 500-mL line, halfway up a straight body
    sx0, sx1, sy = 160, 372, 236                      # the day scale
    day = (sx1 - sx0) / 21
    d.group('thin')
    for k, y in enumerate((bbase, y500, btop + 6)):  # graduation lines carried out from the bottle
        d.line((bx0 - 10, y), (bx1 + 14, y))
    d.line((sx0, sy), (sx1, sy))
    for k in range(22):
        h = 7 if k % 7 == 0 else 3
        d.line((sx0 + k * day, sy - h), (sx0 + k * day, sy + h))
    d.group()
    # the bottle: shoulders, neck and a rounded foot
    d.line((bx0, btop), (bx0, bbase - 8))
    d.arc((bx0 + bx1) / 2, bbase - 8, (bx1 - bx0) / 2, 180, 0, n=20, ry=8)
    d.line((bx1, bbase - 8), (bx1, btop))
    d.line((bx0, btop), (66, 74), (66, 58))
    d.line((bx1, btop), (90, 74), (90, 58))
    d.line((62, 58), (94, 58), (94, 46), (62, 46), closed=True)        # the rubber stopper
    # the inlet and airway tubes through the stopper, cut and clamped
    d.line((72, 46), (72, 34))
    d.line((84, 46), (84, 30))
    # the route above the scale: donor centre, Prestwick, France, as a flown arc
    pts = [(sx0 + t * (sx1 - sx0), 120 - 46 * math.sin(math.pi * t)) for t in [i / 40 for i in range(41)]]
    d.group('mid')
    # the contents, blood and preservative mixed, hatched to the fill line
    for y in range(btop + 12, bbase - 6, 7):
        d.line((bx0 + 4, y), (bx1 - 4, y - 5))
    d.line((bx0, y500), (bx1, y500))
    d.line((bx0, btop + 6), (bx1, btop + 6))                             # the 1,000-mL fill line
    d.lines([[(68, 36), (76, 36)], [(80, 32), (88, 32)]])               # the spring clamps
    # the unrefrigerated crossing, dashed, then the rest of the route
    for i in range(0, 26, 2):
        d.line(pts[i], pts[i + 1])
    d.line(*pts[26:])
    for i in (0, 26, 40):
        d.circle(*pts[i], 2.5)
    # the bottle's life on the day scale: cold store, the flight, cold again to expiry
    d.line((sx0, sy - 14), (sx0 + 1 * day, sy - 14))
    _dashed(d, (sx0 + 1 * day, sy - 14), (sx0 + 2 * day, sy - 14), dash=3, gap=2)
    d.line((sx0 + 2 * day, sy - 14), (sx1, sy - 14))
    _arrow(d, (sx1 - 10, sy - 14), (sx1, sy - 14))
    d.line((sx0 + 6.5 * day, sy + 12), (sx0 + 6.5 * day, sy + 24))
    d.group('mid')
    d.text(bx1 + 18, y500 + 3, '500 mL', size=7, anchor='start')
    d.text(bx1 + 18, btop + 9, '1,000 mL', size=7, anchor='start')
    d.text((bx0 + bx1) / 2, bbase + 18, 'ALSEVER + BLOOD', size=7)
    d.text(pts[0][0], pts[0][1] + 14, 'US', size=7)
    d.text(pts[13][0], pts[13][1] - 8, 'FLIGHT, NO ICE', size=7)
    d.text(pts[26][0] + 4, pts[26][1] - 8, 'PRESTWICK', size=7, anchor='start')
    d.text(pts[40][0], pts[40][1] + 14, 'FRANCE', size=7)
    d.text(sx0, sy + 20, 'DAY 0', size=7)
    d.text(sx0 + 14 * day, sy + 20, '14', size=7)
    d.text(sx1, sy + 20, '21', size=7)
    d.text(sx0 + 6.5 * day, sy + 34, 'ONE WINTER TRIP', size=7)
    return d


def korea_blood():
    d = D()
    # Left: the Hollinger trunk of 1951 in plan: a plywood shell, two inches of Styrofoam, two wire
    # racks of twelve 500-mL bottles either side of a central ice can. Right: one bottle in
    # elevation, stood upside down so the red cells settle into its neck, the end it is drawn from.
    # Proportions are a sketch; Kendrick gives the parts and counts, not the dimensions.
    x0, y0, x1, y1 = 24, 60, 254, 250                 # the shell, outside
    t = 14                                            # the insulation's thickness, drawn
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = 10                                            # a bottle's radius in plan
    ice_r = 24
    racks = []
    for side in (-1, 1):
        for i in range(3):
            for j in range(4):
                racks.append((cx + side * (ice_r + 16 + i * 2 * (r + 1)), cy + (j - 1.5) * 2 * (r + 3)))
    bx, top, neck, base = 330, 70, 218, 250            # the bottle in elevation, neck down
    d.group('thin')
    d.line((cx, y0 - 12), (cx, y1 + 12))
    d.line((x0 - 12, cy), (x1 + 12, cy))
    d.line((bx, top - 14), (bx, base + 12))
    d.line((300, neck - 40), (372, neck - 40))      # the level the cells have settled to
    d.group()
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)
    d.line((x0 + t, y0 + t), (x1 - t, y0 + t), (x1 - t, y1 - t), (x0 + t, y1 - t), closed=True)
    d.circle(cx, cy, ice_r)
    # the bottle, upside down: a flat base at the top, shoulders and neck below, the stopper last
    d.line((bx - 24, top), (bx + 24, top), (bx + 24, neck - 26), (bx + 8, neck), (bx + 8, base - 12),
           (bx - 8, base - 12), (bx - 8, neck), (bx - 24, neck - 26), closed=True)
    d.line((bx - 10, base - 12), (bx + 10, base - 12), (bx + 10, base), (bx - 10, base), closed=True)
    d.group('mid')
    for (x, y) in racks:
        d.circle(x, y, r)
    for k in range(6):                               # the insulation, hatched
        u = x0 + t + 6 + k * (x1 - x0 - 2 * t - 12) / 5
        d.line((u, y0 + 3), (u + 8, y0 + t - 3))
        d.line((u, y1 - t + 3), (u + 8, y1 - 3))
    for a in range(0, 360, 45):                       # ice in the can
        d.line(_pt(cx, cy, 6, a), _pt(cx, cy, 16, a + 20))
    # the settled cells, hatched in the neck and lower shoulder
    for y in range(int(neck - 36), int(base - 14), 6):
        hw = 24 if y < neck - 26 else (8 if y > neck else 8 + 16 * (neck - y) / 26)
        d.line((bx - hw + 2, y), (bx + hw - 2, y + 4))
    d.group('mid')
    d.text(cx, cy + ice_r + 14, 'ICE', size=7)
    d.text(cx, y0 - 16, '12 + 12 BOTTLES', size=7)
    d.text(x0, y1 + 22, 'STYROFOAM 2 IN', size=7, anchor='start')
    d.text(bx + 30, top + 40, 'PLASMA', size=7, anchor='start')
    d.text(bx + 30, neck - 18, 'CELLS', size=7, anchor='start')
    d.text(bx, top - 20, 'BOTTLE INVERTED', size=7)
    return d


def asbp():
    d = D()
    # The Armed Services Blood Program's chain as the 2011 Joint Blood Program Handbook draws it:
    # donor centre, processing laboratory, by air to a theatre transshipment centre, a blood supply
    # unit, the treatment facility. Frozen red cells wait in a depot below and join the chain when
    # a war begins. Blood flows right (solid); the daily blood reports flow back left (dashed).
    names = ['DONOR', 'ASWBPL', 'EBTC', 'BSU', 'MTF']
    xs = [42 + i * 79 for i in range(5)]
    y, w, h = 160, 54, 34
    dep = (xs[2] + 40, 248)                           # the frozen-blood depot, between EBTC and BSU
    d.group('thin')
    d.line((14, y), (386, y))                         # the chain's axis
    d.line((14, 92), (386, 92))                       # the reports' axis
    for x in xs:
        d.line((x, 84), (x, 266))
    d.group()
    for x in xs:
        d.line((x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), closed=True)
    d.line((dep[0] - 34, dep[1] - 16), (dep[0] + 34, dep[1] - 16), (dep[0] + 34, dep[1] + 16), (dep[0] - 34, dep[1] + 16), closed=True)
    # the flow of blood, box to box; the ocean crossing as an arc
    for i in range(4):
        a, b = (xs[i] + w / 2, y), (xs[i + 1] - w / 2, y)
        if i == 1:
            pts = [(a[0] + t * (b[0] - a[0]), y - 18 * math.sin(math.pi * t)) for t in [k / 16 for k in range(17)]]
            d.line(*pts)
            _arrow(d, pts[-2], pts[-1])
        else:
            d.line(a, b)
            _arrow(d, a, b)
    # frozen stock up to the chain
    d.line((dep[0] - 20, dep[1] - 16), (xs[2] + 6, y + h / 2))
    _arrow(d, (dep[0] - 20, dep[1] - 16), (xs[2] + 6, y + h / 2))
    d.line((dep[0] + 20, dep[1] - 16), (xs[3] - 6, y + h / 2))
    _arrow(d, (dep[0] + 20, dep[1] - 16), (xs[3] - 6, y + h / 2))
    d.group('mid')
    # the daily reports, dashed, from each box back up the chain
    for i in range(4, 0, -1):
        a, b = (xs[i], 92), (xs[i - 1], 92)
        _dashed(d, a, b, dash=4, gap=3)
        _arrow(d, a, b, size=4)
        d.line((xs[i], y - h / 2), (xs[i], 96))
    # a snowflake on the depot, six arms with barbs
    sx, sy = dep[0] - 22, dep[1]
    for a in range(0, 360, 60):
        p = _pt(sx, sy, 8, a)
        d.line((sx, sy), p)
        d.line(_pt(sx, sy, 5, a), _pt(*_pt(sx, sy, 5, a), 3, a + 50))
    d.group('mid')
    for x, n in zip(xs, names):
        d.text(x, y + 3, n, size=7)
    d.text(dep[0] + 6, dep[1] + 3, 'DEPOT', size=7)
    d.text((xs[1] + xs[2]) / 2, y - 26, 'BY AIR', size=7)
    d.text(200, 80, 'DAILY BLOOD REPORTS', size=7)
    d.text(xs[4], y + 36, '1–6 °C', size=7)
    d.text(dep[0] + 46, dep[1] + 3, '−65 °C', size=7, anchor='start')
    return d


PLATES = {'asbp': asbp, 'whole-blood-wwii': whole_blood_wwii, 'korea-blood': korea_blood}
