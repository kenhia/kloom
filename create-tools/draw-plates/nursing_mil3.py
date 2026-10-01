"""Plates for Keeping Watch's Nurses at war, part mil3 (sprint 030): flight nurses, the MASH, Vietnam.
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


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def flight_nurses():
    d = D()
    # A transport's cabin in cross-section, a schematic after the Pacific Wing's C-54s (1944): litters
    # four high on each side of the aisle, held outboard on wall brackets and inboard on webbing straps
    # from ceiling to floor. The Wing loaded the patients needing least attention top and bottom and those
    # needing most in the two middle tiers, within the nurse's reach. Scale about 1.5 cm to the unit.
    cx, cy, R = 200, 140, 112
    floor = cy + 72                                                       # the cabin floor's chord
    half = math.sqrt(R * R - (floor - cy) ** 2)
    tiers = [floor - 14, floor - 44, floor - 74, floor - 104]             # litter heights, bottom to top
    inL, inR = 154, 246                                                   # the inboard straps
    d.group('thin')
    d.circle(cx, cy, R)
    d.line((cx, cy - R - 10), (cx, tiers[3] - 8))                         # the centreline
    d.line((cx, tiers[3] + 8), (cx, floor + 30))
    d.line((cx - 6, cy), (cx + 6, cy))
    for y in tiers:                                                       # tier levels, carried across
        d.line((cx - R - 18, y), (cx + R + 18, y))
    d.line((cx + R + 12, tiers[0]), (cx + R + 12, tiers[-1]))            # the tier spacing, dimensioned
    for y in tiers:
        d.line((cx + R + 8, y), (cx + R + 16, y))
    d.group()
    # the fuselage skin: an arc above the floor, and the belly below it
    a0 = math.degrees(math.asin((floor - cy) / R))
    d.arc(cx, cy, R, 180 - a0, 360 + a0, n=72)                            # cabin wall and roof
    d.arc(cx, cy, R, a0, 180 - a0, n=36)                                  # the belly under the floor
    d.line((cx - half, floor), (cx + half, floor))                        # the floor
    d.line((cx - half + 6, floor + 6), (cx + half - 6, floor + 6))        # the floor beams
    # the inboard straps, ceiling to floor
    top = cy - math.sqrt(R * R - (inL - cx) ** 2)
    d.line((inL, top), (inL, floor))
    d.line((inR, top), (inR, floor))
    d.group('mid')
    # each litter seen end-on: two poles and the canvas sagging between them
    for i, y in enumerate(tiers):
        for x0, x1 in ((inL - 44, inL - 2), (inR + 2, inR + 44)):
            d.circle(x0 + 2, y, 2.4)
            d.circle(x1 - 2, y, 2.4)
            hw = (x1 - x0) / 2 - 2                                        # canvas from pole to pole
            sag = math.degrees(math.atan2(14, hw))
            d.arc((x0 + x1) / 2, y - 14, math.hypot(hw, 14), sag, 180 - sag, n=16)
            wall = x0 if x0 < cx else x1                                  # the wall bracket
            d.line((wall, y), (wall - 5 if x0 < cx else wall + 5, y - 5))
    d.group()
    # the two middle tiers, where the nurse could reach: a patient's outline on each, drawn heavier
    for y in tiers[1:3]:
        for x0, x1 in ((inL - 44, inL - 2), (inR + 2, inR + 44)):
            d.ellipse((x0 + x1) / 2, y + 2, 15, 4)
    # the oxygen cylinder standing in the aisle
    d.line((cx - 7, floor), (cx - 7, floor - 40))
    d.line((cx + 7, floor), (cx + 7, floor - 40))
    d.arc(cx, floor - 40, 7, 180, 360, n=12)
    d.line((cx, floor - 47), (cx, floor - 53), (cx + 8, floor - 53))
    d.group('mid')
    d.text(cx - R - 22, tiers[0] + 3, 'LEAST', size=7, anchor='end')
    d.text(cx - R - 22, tiers[1] + 3, 'MOST', size=7, anchor='end')
    d.text(cx - R - 22, tiers[2] + 3, 'MOST', size=7, anchor='end')
    d.text(cx - R - 22, tiers[3] + 3, 'LEAST', size=7, anchor='end')
    d.text(cx + R + 20, (tiers[0] + tiers[-1]) / 2 + 3, '4 HIGH', size=7, anchor='start')
    d.text(cx + 12, floor - 50, 'OXYGEN', size=7, anchor='start')
    d.text(cx, (tiers[2] + tiers[3]) / 2 + 3, 'AISLE', size=7)
    d.text(cx, 290, 'CABIN IN SECTION · A SCHEMATIC', size=7)
    return d


def _tent(d, x, y, w, h, poles=3):
    """A ward tent in plan: the walls, the ridge down its length, and its poles."""
    _box(d, x, y, w, h)
    d.line((x, y + h / 2), (x + w, y + h / 2))


def mash():
    d = D()
    # A MASH in plan, a schematic after the 1948 table's sections (Cowdrey, The Medics' War): the casualty
    # comes by helicopter or ambulance into preoperative and shock, to the operating tent, to postoperative,
    # to the holding ward, and out by road to the train or the airstrip. X-ray and pharmacy serve them all.
    road = 268
    hp = (52, 78)
    pre = (96, 52, 92, 56)
    ort = (206, 46, 66, 68)
    post = (290, 52, 92, 56)
    hold = (290, 160, 92, 56)
    xr = (142, 172, 54, 34)
    ph = (212, 172, 54, 34)
    d.group('thin')
    d.line((20, road), (380, road))                                       # the road's edge
    d.line((20, 150), (380, 150))                                         # the compound's axis
    d.line((hp[0] - 34, hp[1]), (hp[0] + 34, hp[1]))
    d.line((hp[0], hp[1] - 34), (hp[0], hp[1] + 34))
    d.circle(*hp, 30)                                                     # the pad's clear circle
    d.group()
    d.circle(*hp, 18)                                                     # the helipad
    d.line((hp[0] - 7, hp[1] - 9), (hp[0] - 7, hp[1] + 9))
    d.line((hp[0] + 7, hp[1] - 9), (hp[0] + 7, hp[1] + 9))
    d.line((hp[0] - 7, hp[1]), (hp[0] + 7, hp[1]))
    for t in (pre, ort, post, hold, xr, ph):
        _tent(d, *t)
    d.line((20, road + 6), (380, road + 6))                               # the road
    d.group('mid')
    # tent poles along each ridge, and guy lines at the corners
    for (x, y, w, h) in (pre, ort, post, hold, xr, ph):
        for k in range(3):
            d.circle(x + w * (k + 0.5) / 3, y + h / 2, 1.6)
        for (px, py, sx, sy) in ((x, y, -1, -1), (x + w, y, 1, -1), (x, y + h, -1, 1), (x + w, y + h, 1, 1)):
            d.line((px, py), (px + 5 * sx, py + 5 * sy))
    # litters in preop and postop, and in the holding ward
    for (x, y, w, h) in (pre, post, hold):
        for k in range(4):
            lx = x + 8 + k * 21
            _box(d, lx, y + 5, 7, 18)
            _box(d, lx, y + h - 23, 7, 18)
    # the operating tent's three tables, each under a lamp
    for k in range(3):
        tx = ort[0] + 12 + k * 18
        _box(d, tx, ort[1] + 18, 6, 32)
        d.circle(tx + 3, ort[1] + 34, 7)
    d.group()
    # the patient's path
    path = [((hp[0] + 20, hp[1]), (pre[0] - 2, hp[1])),
            ((pre[0] + pre[2] + 2, 80), (ort[0] - 2, 80)),
            ((ort[0] + ort[2] + 2, 80), (post[0] - 2, 80)),
            ((post[0] + post[2] / 2, post[1] + post[3] + 2), (post[0] + post[2] / 2, hold[1] - 2)),
            ((hold[0] + hold[2] / 2, hold[1] + hold[3] + 2), (hold[0] + hold[2] / 2, road - 3))]
    for p, q in path:
        d.line(p, q)
        _arrow(d, p, q)
    amb = ((pre[0] + 20, road - 3), (pre[0] + 20, pre[1] + pre[3] + 2))   # the ambulances' way in
    d.line(*amb)
    _arrow(d, *amb)
    d.group('mid')
    d.text(hp[0], hp[1] + 44, 'HELICOPTER', size=7)
    d.text(pre[0] + pre[2] / 2, pre[1] - 6, 'PREOP · SHOCK', size=7)
    d.text(ort[0] + ort[2] / 2, ort[1] - 6, 'OPERATING', size=7)
    d.text(post[0] + post[2] / 2, post[1] - 6, 'POSTOP', size=7)
    d.text(hold[0] + hold[2] / 2 + 8, hold[1] - 6, 'HOLDING', size=7, anchor='start')
    d.text(xr[0] + xr[2] / 2, xr[1] + xr[3] + 11, 'X-RAY', size=7)
    d.text(ph[0] + ph[2] / 2, ph[1] + ph[3] + 11, 'PHARMACY', size=7)
    d.text(pre[0] + 26, road - 8, 'AMBULANCE', size=7, anchor='start')
    d.text(hold[0] + hold[2] / 2 - 8, road - 8, 'TO TRAIN OR AIRSTRIP', size=7, anchor='end')
    d.text(200, 292, 'A MASH IN PLAN · A SCHEMATIC', size=7)
    return d


def vietnam_nurses():
    d = D()
    # A triage area laid out as Emergency War Surgery (1975) asks: one open room beside the helicopter pad,
    # a frame for every litter with a bottle of fluid hanging over each, the triage officer standing where
    # he sees the whole room at a glance, X-ray and the blood bank adjoining, and the way out to preop and
    # the operating rooms. A schematic, not a survey of any one hospital.
    room = (92, 86, 216, 150)
    x0, y0, w, h = room
    officer = (x0 + 22, y0 + h / 2)
    frames = []
    for row, fy in enumerate((y0 + 22, y0 + h - 52)):
        for k in range(5):
            frames.append((x0 + 64 + k * 30, fy))
    d.group('thin')
    for fx, fy in frames:                                                 # the officer's sightlines
        d.line(officer, (fx + 6, fy + 15))
    d.circle(*officer, 12)
    d.line((x0, y0 + h / 2), (x0 + w, y0 + h / 2))                        # the room's axis
    d.group()
    _box(d, *room)                                                        # the triage room
    _box(d, x0 + 40, y0 - 44, 70, 44)                                     # X-ray, adjoining
    _box(d, x0 + 130, y0 - 44, 70, 44)                                    # the blood bank, adjoining
    _box(d, x0 + w, y0 + 40, 70, 70)                                      # to preop and the OR
    d.circle(46, y0 + h / 2, 26)                                          # the helicopter pad
    d.line((40, y0 + h / 2 - 9), (40, y0 + h / 2 + 9))
    d.line((52, y0 + h / 2 - 9), (52, y0 + h / 2 + 9))
    d.line((40, y0 + h / 2), (52, y0 + h / 2))
    d.group('mid')
    for fx, fy in frames:                                                 # litter frames and their bottles
        _box(d, fx, fy, 12, 30)
        d.line((fx - 3, fy), (fx - 3, fy + 30))
        d.line((fx + 15, fy), (fx + 15, fy + 30))
        by = fy - 9 if fy < y0 + h / 2 else fy + 39
        d.line((fx + 6, fy if fy < y0 + h / 2 else fy + 30), (fx + 6, by))
        d.ellipse(fx + 6, by - (3 if fy < y0 + h / 2 else -3), 3, 4)
    for k in range(4):                                                    # open shelves round the walls
        d.line((x0 + 4, y0 + 8 + k * 6), (x0 + 30, y0 + 8 + k * 6))
    d.circle(*officer, 3)
    d.group()
    door_in = ((72, y0 + h / 2), (x0 - 2, y0 + h / 2))
    d.line(*door_in)
    _arrow(d, *door_in)
    door_out = ((x0 + w - 4, y0 + 75), (x0 + w + 18, y0 + 75))
    d.line(*door_out)
    _arrow(d, *door_out)
    d.group('mid')
    d.text(46, y0 + h / 2 + 40, 'HELIPAD', size=7)
    d.text(x0 + 75, y0 - 18, 'X-RAY', size=7)
    d.text(x0 + 165, y0 - 18, 'BLOOD BANK', size=7)
    d.text(x0 + w + 35, y0 + 60, 'PREOP', size=7)
    d.text(x0 + w + 35, y0 + 98, 'TO OR', size=7)
    d.text(officer[0] - 10, officer[1] + 24, 'TRIAGE', size=7, anchor='start')
    d.text(officer[0] - 10, officer[1] + 33, 'OFFICER', size=7, anchor='start')
    d.text(200, 292, 'A TRIAGE AREA, AFTER THE 1975 HANDBOOK · A SCHEMATIC', size=7)
    return d


PLATES = {
    'flight-nurses': flight_nurses,
    'mash': mash,
    'vietnam-nurses': vietnam_nurses,
}
