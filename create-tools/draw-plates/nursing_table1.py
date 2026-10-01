"""Plates for Keeping Watch's trail At the table, first part: the scrub, the mask and the instrument
table (sprint 030). See plates_for.py."""
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


def _along(p, q, t, off=0.0):
    """The point a fraction t from p to q, moved `off` to the left of the line."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    return p[0] + t * dx - off * dy / n, p[1] + t * dy + off * dx / n


def surgical_scrub():
    d = D()
    # Left: a scrubbed forearm held up, hand above elbow, as every text from 1888 to 2009 has it: the
    # axis from elbow to fingertip at 62 degrees, the arm's outline built off that axis, the forearm cut
    # into the three-inch lengths an Army subcourse scrubs one at a time, the line two inches above the
    # elbow where the scrub stops, and water running from the fingertips down to the elbow.
    # Right: five scrubs on one time scale, from the texts, 12 px a minute: Fürbringer 1888 (a minute each
    # of soap, alcohol, sublimate), Price 1938 (seven minutes' scrub, three in alcohol), the Navy 1939
    # (fifteen minutes' scrub, then alcohol), the Army's Letterman manual 1943 (two three-minute brushings,
    # then alcohol, all to a ten-minute hourglass: the open end runs to ten) and WHO 2009 (two to five minutes, as the maker says).
    elbow, tip = (70, 252), (70 + 196 * math.cos(math.radians(62)), 252 - 196 * math.sin(math.radians(62)))
    wrist_t, palm_t = 0.62, 0.80                                          # fractions of the axis
    d.group('thin')
    d.line(_along(elbow, tip, -0.12), _along(elbow, tip, 1.08))           # the arm's axis
    for k in range(1, 4):                                                 # three-inch lengths of the forearm
        t = 0.08 + k * wrist_t / 3.4
        d.line(_along(elbow, tip, t, 22), _along(elbow, tip, t, -22))
    d.line(_along(elbow, tip, -0.07, 30), _along(elbow, tip, -0.07, -30))  # two inches above the elbow
    x0, x1, y0 = 196, 376, 46                                             # the time scale
    for m in range(0, 16):
        d.line((x0 + 12 * m, y0), (x0 + 12 * m, y0 + 190 if m % 5 == 0 else y0 + 6))
    d.group()
    # the arm: forearm tapering from 17 to 11 px each side of the axis, then the hand
    w_el, w_wr = 17, 11
    left = [_along(elbow, tip, t, w_el + (w_wr - w_el) * t / wrist_t) for t in (-0.1, 0.0, 0.2, 0.4, wrist_t)]
    right = [_along(elbow, tip, t, -(w_el + (w_wr - w_el) * t / wrist_t)) for t in (-0.1, 0.0, 0.2, 0.4, wrist_t)]
    hand_l = [_along(elbow, tip, t, o) for t, o in ((0.70, 15), (0.80, 14), (0.93, 9), (1.0, 4))]
    hand_r = [_along(elbow, tip, t, -o) for t, o in ((0.70, 15), (0.80, 13), (0.93, 8), (1.0, 3))]
    d.line(*left, *hand_l, *reversed(hand_r), *reversed(right))
    thumb = [_along(elbow, tip, 0.68, 15), _along(elbow, tip, 0.78, 27), _along(elbow, tip, 0.86, 25),
             _along(elbow, tip, 0.80, 14)]
    d.line(*thumb)
    # the elbow's bend: the upper arm going down and back
    d.line(left[0], (left[0][0] - 10, 298))
    d.line(right[0], (right[0][0] - 2, 298))
    d.group('mid')
    for k in range(1, 4):                                                 # the fingers' lines
        a = _along(elbow, tip, 0.86, 9 - 6 * k)
        b = _along(elbow, tip, 0.99, 6 - 4 * k)
        d.line(a, b)
    for t in (0.95, 0.55, 0.15):                                          # water running down to the elbow
        p = _along(elbow, tip, t, -26)
        q = _along(elbow, tip, t - 0.14, -26)
        d.line(p, q)
        _arrow(d, p, q, 4)
    # the five scrubs, each a bar of segments on the time scale
    rows = [  # year, segments as (minutes, kind); kind 0 soap and brush, 1 alcohol, 2 mercury, 3 open
        ('1888', [(1, 0), (1, 1), (1, 2)]),
        ('1938', [(7, 0), (3, 1)]),
        ('1939', [(15, 0), (0.6, 3)]),
        ('1943', [(3, 0), (3, 0), (4, 3)]),
        ('2009', [(2, 0), (3, 3)]),
    ]
    for i, (_, segs) in enumerate(rows):
        y = y0 + 22 + 36 * i
        x = x0
        for mins, kind in segs:
            w = 12 * mins
            if kind == 3:                                                 # an open end: a length not set
                d.line((x, y), (x + w, y))
                d.line((x, y + 10), (x + w, y + 10))
            else:
                _box(d, x, y, w, 10)
                if kind == 1:                                             # alcohol: hatched
                    for k in range(1, int(w // 4)):
                        d.line((x + 4 * k, y + 10), (x + 4 * k + 3, y))
                if kind == 2:                                             # mercury: cross-hatched
                    d.line((x, y), (x + w, y + 10))
                    d.line((x, y + 10), (x + w, y))
            x += w
    d.group('mid')
    d.text(24, 30, 'HANDS ABOVE ELBOWS', size=7, anchor='start')
    for i, (year, _) in enumerate(rows):
        d.text(x0 - 6, y0 + 30 + 36 * i, year, size=7, anchor='end')
    for m in (0, 5, 10, 15):
        d.text(x0 + 12 * m, y0 + 204, str(m), size=7)
    d.text(x0 + 90, y0 + 222, 'MINUTES · HATCHED: ALCOHOL', size=7)
    return d


def surgical_mask():
    d = D()
    # Left: Hübener's test of 1898 in elevation. A head bent over four agar plates set about 50 cm below
    # the mouth; droplets thrown from the lips on speaking, as parabolas launched at 6 to 34 degrees
    # below level at one speed under gravity (scaled), landing on plates 1 to 4; the mask in section,
    # a wire frame from the bridge of the nose round the chin, with its two layers of gauze, stopping
    # them. Right: the mask's wire frame from the front, after Esmarch's chloroform mask: a bell over the
    # nose, a ring round the mouth and chin, a crossbar, a centre wire and two spectacle earpieces.
    mouth = (113, 93)
    table_y = 232                                                         # 50 cm below the mouth, at 2.8 px/cm
    plates = [(132, 232), (162, 232), (192, 232), (222, 232)]
    mc, mr = (104, 92), 20                                                # the mask's section: centre, inner radius
    d.group('thin')
    d.line((40, table_y + 6), (250, table_y + 6))                         # the table top
    d.line((246, mouth[1]), (246, table_y))                               # the 50 cm, dimensioned
    d.line((240, mouth[1]), (252, mouth[1]))
    d.line((240, table_y), (252, table_y))
    d.line((124, mouth[1]), (246, mouth[1]))
    G = 90                                                                # droplets that would land on 1..4:
    for px, py in plates:                                                 # parabolas under one gravity,
        vx, vy = px - mouth[0], (py - mouth[1]) - G / 2                   # reaching each plate at t = 1
        d.line(*[(mouth[0] + vx * t, mouth[1] + vy * t + G * t * t / 2) for t in [i / 30 for i in range(31)]])
    d.group()
    # the head in profile, leaning a little over the plates: skull, brow, nose, lips, chin, neck
    d.arc(70, 66, 40, 150, 380, n=40)
    d.line((105, 54), (108, 68), (118, 80), (110, 84), (113, 89), (110, 93), (113, 98), (104, 108), (88, 112))
    d.line((70, 106), (64, 128), (60, 150))
    d.line((92, 112), (96, 132), (100, 150))
    # the mask in section: the wire frame from the bridge of the nose round under the chin, two gauze layers
    for off in (0, 3.2):
        d.arc(mc[0], mc[1], mr + off, -62, 92, n=30)
    # the same droplets stopped: each path from the mouth to where it meets the inner layer of gauze
    for px, py in plates:
        vx, vy = px - mouth[0], (py - mouth[1]) - G / 2
        pts = []
        for i in range(0, 300):
            t = i / 300
            x, y = mouth[0] + vx * t, mouth[1] + vy * t + G * t * t / 2
            pts.append((x, y))
            if math.hypot(x - mc[0], y - mc[1]) >= mr - 0.5:
                break
        d.line(*pts)
        d.circle(pts[-1][0], pts[-1][1], 1.2)
    d.group('mid')
    for x, y in plates:                                                   # the four agar plates in perspective
        d.ellipse(x, y, 13, 4)
        d.ellipse(x, y - 3, 13, 4)
    d.line((96, 74), (60, 66))                                            # the frame's earpiece
    # the wire frame, from the front
    cx, cy, r = 335, 178, 46
    d.group()
    a0, a1 = -58, 238                                                     # the ring's arc, open at the top
    d.arc(cx, cy, r, a0, a1, n=60)
    p0, p1 = _pt(cx, cy, r, a0), _pt(cx, cy, r, a1)
    top = (cx, 64)
    d.curve(f'M{p1[0]:.1f} {p1[1]:.1f} C{cx - 34:.1f} 112 {cx - 22:.1f} 60 {top[0]:.1f} {top[1]:.1f}')
    d.curve(f'M{p0[0]:.1f} {p0[1]:.1f} C{cx + 34:.1f} 112 {cx + 22:.1f} 60 {top[0]:.1f} {top[1]:.1f}')
    d.line(p1, p0)                                                        # the crossbar
    d.line((cx, p0[1]), (cx, cy + r))                                     # the centre wire
    d.line((p1[0], p1[1]), (p1[0] - 26, p1[1] - 2))                       # the earpieces' stems
    d.line((p0[0], p0[1]), (p0[0] + 26, p0[1] - 2))
    d.group('mid')
    d.arc(p1[0] - 26, p1[1] + 6, 8, 180, 270, n=10)                       # the earpieces' bows
    d.arc(p0[0] + 26, p0[1] + 6, 8, 270, 360, n=10)
    d.group('mid')
    for i, (x, y) in enumerate(plates):
        d.text(x, y + 16, str(i + 1), size=7)
    d.text(252, (mouth[1] + table_y) / 2 + 3, '50 CM', size=7, anchor='start')
    d.text(140, 270, 'COUNTING ALOUD, 10 MINUTES', size=7)
    d.text(cx, 254, 'WIRE FRAME · TWO LAYERS', size=7)
    d.text(cx, 266, 'OF GAUZE SEWN OVER IT', size=7)
    return d


def _hemostat(d, x, y, length=16, ang=-90):
    """A ring-handled instrument lying on the tray: two finger rings and the shanks to the jaws."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    for s in (-1, 1):
        d.circle(x + s * 2.4 * px, y + s * 2.4 * py, 2)
    d.line((x + 2.4 * px + 2 * ux, y + 2.4 * py + 2 * uy), (x + length * ux, y + length * uy),
           (x - 2.4 * px + 2 * ux, y - 2.4 * py + 2 * uy))


def instrument_table():
    d = D()
    # A plan of the sterile field for an appendectomy, as the Navy's handbook of 1959 photographed it and the
    # Army's subcourse describes it: the operating table with the patient draped, the Mayo stand raised over
    # the patient's legs with the instruments for the opening, the back table and ring stand at right angles
    # to the operating table, closing the sterile circle; the surgeon at the incision with the assistant across
    # the table and the scrub beside him, the anesthetist at the head, the circulator outside the circle.
    # Inset: the Mayo tray, with the instruments in the rows of the Navy's figure 182: hemostats in front,
    # then forceps, scissors and scalpels; clamps and large hemostats at the back. Not to scale.
    tx, ty, tw, th = 150, 40, 52, 196                                     # the operating table
    cx = tx + tw / 2
    d.group('thin')
    d.circle(150, 178, 110)                                               # the sterile circle
    d.line((cx, ty - 8), (cx, ty + th + 8))                               # the table's axis
    d.line((tx - 18, 112), (tx + tw + 18, 112))                           # the line of the incision
    d.group()
    _box(d, tx, ty, tw, th)                                               # the table, draped
    d.arc(cx, ty + 30, 30, 200, 340, n=24)                                # the anesthesia screen
    d.line((cx, 102), (cx, 122))                                          # the incision
    _box(d, 122, 150, 108, 34)                                            # the Mayo tray across the table
    _box(d, 28, 226, 124, 42)                                             # the back table, across the table's axis
    d.circle(48, 188, 12)                                                 # the ring stand: two basins
    d.circle(76, 188, 9)
    d.group('mid')
    d.circle(242, 167, 5)                                                 # the Mayo stand's foot, off the table
    d.line((230, 167), (237, 167))
    for x, y in ((128, 112), (224, 112), (110, 160), (cx, 24), (330, 238)):  # surgeon, assistant, scrub,
        d.circle(x, y, 8)                                                 # anesthetist, circulator
    for k in range(6):                                                    # instruments on the back table
        _hemostat(d, 40 + 9 * k, 260, 12)
    _box(d, 100, 236, 20, 14)                                             # sponges
    _box(d, 126, 236, 18, 24)                                             # the basin for sutures
    # inset: the Mayo tray, with the Navy's rows
    ix, iy, iw, ih = 262, 30, 128, 92
    d.group()
    _box(d, ix, iy, iw, ih)
    d.group('mid')
    for k in range(10):                                                   # front row: hemostats
        _hemostat(d, ix + 10 + 6.5 * k, iy + ih - 8, 16)
    for k in range(4):                                                    # forceps, scissors, scalpels
        x = ix + 82 + 11 * k
        d.line((x, iy + ih - 8), (x + 1, iy + ih - 30))
        if k in (1, 2):
            d.circle(x, iy + ih - 6, 2)
    for k in range(10):                                                   # back row: clamps, large hemostats
        _hemostat(d, ix + 12 + 11 * k, iy + 10, 20, 90)
    d.line((ix + 8, iy + 46), (ix + iw - 8, iy + 46))                     # the rolled towel
    d.line((ix + 8, iy + 50), (ix + iw - 8, iy + 50))
    d.group('mid')
    d.text(ix + iw / 2, iy + ih + 12, 'MAYO TRAY', size=7)
    d.text(250, 170, 'MAYO STAND', size=7, anchor='start')
    d.text(90, 284, 'BACK TABLE', size=7)
    d.text(62, 170, 'RING STAND', size=7)
    d.text(116, 98, 'SURGEON', size=7, anchor='end')
    d.text(224, 97, 'ASSISTANT', size=7)
    d.text(96, 146, 'SCRUB', size=7, anchor='end')
    d.text(330, 260, 'CIRCULATOR', size=7)
    return d


PLATES = {
    'surgical-scrub': surgical_scrub,
    'surgical-mask': surgical_mask,
    'instrument-table': instrument_table,
}
