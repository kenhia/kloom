"""Plates for Keeping Watch's Nightingale segment, second half (sprint 030, part night2). See plates_for.py."""
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


def _bezier(p0, p1, p2, p3, n=24):
    """Points on a cubic Bezier curve."""
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return pts


def notes_on_nursing():
    d = D()
    # A sick room in section, as Notes on Nursing's first chapter sets it up: "a good fire and an open
    # window", the door shut. Air enters at the window, crosses over the bed and leaves by the chimney,
    # which the fire draws. A schematic of her rule, not a survey of any room.
    x0, y0, x1, y1 = 40, 70, 330, 250                                     # the room's inside faces
    d.group('thin')
    d.line((x0 - 14, y1 + 8), (x1 + 40, y1 + 8))                          # the floor's datum
    for y in range(int(y0) + 20, int(y1), 20):                            # level lines across the room
        d.line((x0 + 4, y), (x1 - 4, y))
    d.group()
    # walls, floor and ceiling, with the chimney breast rising at the right
    d.line((x0 - 10, y0 - 10), (x1 + 10, y0 - 10))
    d.line((x0, y0), (x1, y0))
    d.line((x0 - 10, y1 + 8), (x1 + 10, y1 + 8))
    d.line((x0 - 10, y0 - 10), (x0 - 10, 110))                            # window wall, cut by the window
    d.line((x0 - 10, 170), (x0 - 10, y1 + 8))
    d.line((x0, y0), (x0, 110))
    d.line((x0, 170), (x0, y1))
    fx = 290                                                              # the fireplace and flue
    d.line((fx, y1), (fx, 200), (x1, 200))
    d.line((x1, y1), (x1, y0))
    d.line((fx + 14, 200), (fx + 14, 40), )
    d.line((x1 + 10, y1 + 8), (x1 + 10, 40))
    d.line((fx + 14, 40), (fx + 6, 30))
    d.line((x1 + 10, 40), (x1 + 18, 30))
    d.group('mid')
    # the window: a sash raised, its frames in section
    _box(d, x0 - 10, 110, 10, 6)
    _box(d, x0 - 10, 164, 10, 6)
    d.line((x0 - 5, 116), (x0 - 5, 132))
    # the bed: frame, mattress and pillow, the patient's outline
    _box(d, 110, 196, 130, 14)
    d.line((114, 210), (114, y1))
    d.line((236, 210), (236, y1))
    d.line((110, 180), (110, 210))
    d.curve('M 122 196 Q 130 182 146 186 Q 190 178 230 190 L 232 196')
    d.ellipse(126, 190, 9, 5)
    # the fire in the grate
    for k in range(3):
        d.arc(fx + 12 + k * 7, 238, 5, 180, 360, n=12)
    d.line((fx + 4, 243), (x1 - 4, 243))
    # the door, shut, drawn in the back wall
    _box(d, 60, 120, 34, 130)
    d.circle(88, 190, 2)
    d.group('mid')
    # the air: streamlines in at the window, over the bed, up the flue
    for k, dy in enumerate((-16, 0, 16)):
        pts = _bezier((x0 - 30, 140 + dy), (120, 140 + dy * 1.6), (230, 170 + dy), (fx + 2, 222 + k * 6))
        pts += [(fx + 18 + k * 6, 210), (fx + 18 + k * 6, 205)]
        pts += [(fx + 18 + k * 6, 205 - j * 20) for j in range(1, 9)]
        d.line(*pts)
        _arrow(d, pts[-2], pts[-1], 4)
    _arrow(d, (x0 - 40, 140), (x0 - 22, 140), 5)
    d.group('mid')
    d.text(x0 + 4, 100, 'WINDOW OPEN', size=7, anchor='start')
    d.text(77, 140, 'DOOR', size=7)
    d.text(77, 150, 'SHUT', size=7)
    d.text(fx + 25, 268, 'FIRE', size=7)
    d.text(175, 268, 'AS PURE AS THE AIR WITHOUT', size=7)
    d.text(175, 278, 'WITHOUT CHILLING HIM', size=7)
    return d


def nightingale_school():
    d = D()
    # The Monthly Sheet of Personal Character and Acquirements, laid out as a form: the five heads of the
    # moral record (Cook) and the first of the technical ones, against the twelve months of the year's
    # training, with the five grades in the key. The form's real layout is not reproduced in any source
    # read; this sets out its heads and grades, and no marks are filled in.
    rows = ['PUNCTUALITY', 'QUIETNESS', 'TRUSTWORTHINESS', 'NEATNESS', 'WARD MANAGEMENT',
            'DRESSINGS', 'LEECHES', 'HELPLESS PATIENTS', 'BANDAGING', 'OPERATIONS', 'SICK COOKERY',
            'VENTILATION', 'OBSERVATION']
    months = 'JASONDJFMAMJ'
    x0, y0, lw, cw, rh = 52, 52, 104, 18, 15
    xr = x0 + lw + 12 * cw
    yb = y0 + rh * (len(rows) + 1)
    d.group('thin')
    for i in range(len(rows) + 2):
        d.line((x0, y0 + i * rh), (xr, y0 + i * rh))
    for j in range(13):
        d.line((x0 + lw + j * cw, y0), (x0 + lw + j * cw, yb))
    d.group()
    _box(d, x0, y0, xr - x0, yb - y0)
    d.line((x0 + lw, y0), (x0 + lw, yb))
    d.line((x0, y0 + rh), (xr, y0 + rh))
    d.line((x0 - 6, y0 + rh * 6), (xr + 6, y0 + rh * 6))                  # moral | technical
    d.group('mid')
    # the key: the five grades as a scale of filled circles
    ky = 270
    for k in range(5):
        cx = 150 + k * 46
        for j in range(4 - k):                                            # rings: four for excellent, none for 0
            d.circle(cx, ky, 2 + 1.6 * j)
        d.circle(cx, ky, 9)
    d.group('mid')
    for i, s in enumerate(rows):
        d.text(x0 + 4, y0 + rh * (i + 1) + 11, s, size=7, anchor='start')
    for j, m in enumerate(months):
        d.text(x0 + lw + j * cw + cw / 2, y0 + 11, m, size=7)
    d.text(x0 + 4, y0 + 11, '1860–61', size=7, anchor='start')
    d.text(x0 - 8, y0 + rh * 3.6, 'MORAL', size=7, anchor='end')
    d.text(x0 - 8, y0 + rh * 10, 'TECH.', size=7, anchor='end')
    for k, g in enumerate(['EXC.', 'GOOD', 'MOD.', 'IMP.', '0']):
        d.text(150 + k * 46, ky + 18, g, size=7)
    d.text(80, ky + 4, 'GRADES', size=7)
    d.text(200, 38, 'MONTHLY SHEET · SOME HEADS · A SCHEMATIC', size=7)
    return d


def red_cross():
    d = D()
    # Left: the emblem on its construction, a cross of five equal squares on a three-by-three grid (the
    # convention fixes no shape; five squares is the movement's custom), inside the white field of a
    # flag. Right: the arm-badge of Article 7 on a forearm drawn as a cylinder, its band an ellipse
    # computed round the arm, with the same cross foreshortened on it.
    cx, cy, s = 120, 150, 30                                              # centre, square side
    d.group('thin')
    for k in range(4):
        d.line((cx - 1.5 * s + k * s, cy - 1.5 * s - 12), (cx - 1.5 * s + k * s, cy + 1.5 * s + 12))
        d.line((cx - 1.5 * s - 12, cy - 1.5 * s + k * s), (cx + 1.5 * s + 12, cy - 1.5 * s + k * s))
    d.circle(cx, cy, 1.5 * s * math.sqrt(2))
    d.group()
    _box(d, cx - 85, cy - 75, 170, 150)                                   # the white field
    h = s / 2
    d.line((cx - h, cy - 3 * h), (cx + h, cy - 3 * h), (cx + h, cy - h), (cx + 3 * h, cy - h),
           (cx + 3 * h, cy + h), (cx + h, cy + h), (cx + h, cy + 3 * h), (cx - h, cy + 3 * h),
           (cx - h, cy + h), (cx - 3 * h, cy + h), (cx - 3 * h, cy - h), (cx - h, cy - h), closed=True)
    d.line((cx - 85, cy - 75), (cx - 85, cy + 120))                       # the staff
    d.group('mid')
    d.line((cx - h, cy - h), (cx + h, cy - h), (cx + h, cy + h), (cx - h, cy + h), closed=True)
    # the arm: a cylinder, axis vertical, seen a little from above
    ax, r, ry = 300, 34, 10
    top, bot = 60, 250
    d.group()
    d.line((ax - r, top), (ax - r, bot))
    d.line((ax + r, top), (ax + r, bot))
    d.ellipse(ax, top, r, ry)
    d.arc(ax, bot, r, 0, 180, n=32, ry=ry)
    d.group('mid')
    by0, by1 = 120, 170                                                   # the band
    d.arc(ax, by0, r, 0, 180, n=32, ry=ry)
    d.arc(ax, by1, r, 0, 180, n=32, ry=ry)
    d.arc(ax, by0, r, 180, 360, n=32, ry=ry)
    # the cross on the band, foreshortened: x = r sin(theta) on the cylinder's face
    def px(u):
        return ax + r * math.sin(u / r)
    def py(u, v):
        return v + ry * math.cos(u / r)
    hh = 7
    outline = [(-hh, -3 * hh), (hh, -3 * hh), (hh, -hh), (3 * hh, -hh), (3 * hh, hh), (hh, hh), (hh, 3 * hh),
               (-hh, 3 * hh), (-hh, hh), (-3 * hh, hh), (-3 * hh, -hh), (-hh, -hh), (-hh, -3 * hh)]
    pts = []
    for (u0, v0), (u1, v1) in zip(outline, outline[1:]):
        for t in range(6):
            u = u0 + (u1 - u0) * t / 6
            v = v0 + (v1 - v0) * t / 6
            pts.append((px(u), py(u, (by0 + by1) / 2 + v)))
    pts.append(pts[0])
    d.line(*pts)
    d.group('mid')
    d.text(cx, cy + 92, 'A RED CROSS ON A WHITE GROUND', size=7)
    d.text(cx, cy + 102, 'FIVE SQUARES · BY CUSTOM', size=7)
    d.text(ax, bot + 26, 'ARM-BADGE · ART. 7', size=7)
    d.text(ax, 40, 'GENEVA · 1864', size=7)
    return d


def vital_signs():
    d = D()
    # Left: a clinical thermometer's scale, 95 to 110 °F in fifths with the arrow at normal, as Robb
    # (1906) describes it, its bulb and constriction in section. Right: a four-hourly temperature chart
    # worked with invented readings: a fever held near 103-104 °F that falls by crisis in half a day.
    tx, t0, t1 = 46, 40, 250                                              # stem x, top and bottom of scale
    def ty(f):
        return t1 - (f - 95) / 15 * (t1 - t0)
    d.group('thin')
    gx0, gx1, g0, g1 = 110, 380, 94.6, 105.4
    def gy(f):
        return 250 - (f - 97) / 8 * 200
    for f in range(97, 106):
        d.line((gx0, gy(f)), (gx1, gy(f)))
    for k in range(19):
        x = gx0 + k * (gx1 - gx0) / 18
        d.line((x, gy(97)), (x, gy(105)))
    d.group()
    # the thermometer: stem, bore, constriction and bulb
    d.line((tx - 6, t0 - 8), (tx - 6, t1 + 8))
    d.line((tx + 6, t0 - 8), (tx + 6, t1 + 8))
    d.arc(tx, t0 - 8, 6, 180, 360, n=16)
    d.arc(tx, t1 + 18, 10, -60, 240, n=32)
    d.line((tx - 6, t1 + 8), (tx - 5, t1 + 10))
    d.line((tx + 6, t1 + 8), (tx + 5, t1 + 10))
    _box(d, gx0, gy(105), gx1 - gx0, gy(97) - gy(105))
    d.group('mid')
    for k in range(76):                                                   # fifths of a degree
        f = 95 + k / 5
        w = 6 if k % 5 == 0 else 3
        d.line((tx + 6, ty(f)), (tx + 6 + w, ty(f)))
    d.line((tx - 1, t1 + 10), (tx - 1, ty(98.6)))                         # the mercury column, to normal
    _arrow(d, (tx + 26, ty(98.6)), (tx + 14, ty(98.6)), 4)
    d.line((gx0, gy(98.6)), (gx1, gy(98.6)))                              # the normal line on the chart
    # invented four-hourly readings: four days, crisis on the fourth
    temps = [103.2, 104.0, 103.6, 102.8, 103.4, 104.2, 103.4, 103.8, 103.0, 102.6, 103.6, 104.4,
             103.8, 103.2, 101.6, 99.8, 98.8, 98.4, 98.6]
    pts = [(gx0 + k * (gx1 - gx0) / 18, gy(t)) for k, t in enumerate(temps)]
    d.group()
    d.line(*pts)
    for p in pts:
        d.circle(p[0], p[1], 1.6)
    d.group('mid')
    for f in (96, 98, 100, 102, 104, 106, 108, 110):
        d.text(tx + 16, ty(f) + 3, str(f), size=7, anchor='start')
    for f in (97, 99, 101, 103, 105):
        d.text(gx0 - 4, gy(f) + 3, f'{f}', size=7, anchor='end')
    for k in range(3):
        d.text(gx0 + (6 * k + 3) * (gx1 - gx0) / 18, gy(105) - 6, f'DAY {k + 1}', size=7)
    d.text(gx0 + 4, gy(98.6) - 4, 'NORMAL 98.6', size=7, anchor='start')
    d.text(gx1 - 4, gy(101.4), 'CRISIS', size=7, anchor='end')
    d.text(245, 280, 'FOUR-HOURLY · INVENTED READINGS', size=7)
    return d


PLATES = {
    'notes-on-nursing': notes_on_nursing,
    'nightingale-school': nightingale_school,
    'red-cross': red_cross,
    'vital-signs': vital_signs,
}
