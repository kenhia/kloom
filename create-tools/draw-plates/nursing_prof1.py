"""Plates for Keeping Watch's part prof1, the start of The modern profession (sprint 030). See plates_for.py."""
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


def _hour(h):
    """The angle of hour h on a 24-hour dial with midnight at the top."""
    return -90 + h * 15


def training_schools():
    d = D()
    # Left: two six-bed wards with the pupil's room between them, as Linda Richards describes the New
    # England Hospital in 1872-73 ("our beds, which were in little rooms between the wards"); a
    # schematic, not a survey. Right: her day on a 24-hour dial, midnight at the top: on the wards from
    # 5.30 a.m. to 9 p.m., and the afternoon off, 2 to 5, that came every second week.
    wy, wh, ww = 62, 176, 64
    xa, xb = 18, 18 + ww + 36                                             # the two wards' left edges
    d.group('thin')
    d.line((xa + ww / 2, wy - 8), (xa + ww / 2, wy + wh + 8))             # the wards' axes
    d.line((xb + ww / 2, wy - 8), (xb + ww / 2, wy + wh + 8))
    d.line((xa - 6, wy + wh / 2), (xb + ww + 6, wy + wh / 2))             # the line through the nurse's room
    cx, cy, R = 300, 150, 74
    d.circle(cx, cy, R + 12)
    d.line((cx - R - 18, cy), (cx + R + 18, cy))
    d.line((cx, cy - R - 18), (cx, cy + R + 18))
    for h in range(24):                                                   # the hour ticks
        d.line(_pt(cx, cy, R - (6 if h % 6 else 10), _hour(h)), _pt(cx, cy, R, _hour(h)))
    d.group()
    _box(d, xa, wy, ww, wh)
    _box(d, xb, wy, ww, wh)
    _box(d, xa + ww, wy + wh / 2 - 22, 36, 44)                            # the nurse's room between
    d.circle(cx, cy, R)
    d.arc(cx, cy, R + 7, _hour(5.5), _hour(21), n=96)                     # on the wards
    d.group('mid')
    for x in (xa, xb):                                                    # three beds on each wall
        for k in range(3):
            y = wy + 14 + k * 54
            _box(d, x + 3, y, 22, 12)
            _box(d, x + ww - 25, y, 22, 12)
            d.line((x + 8, y + 2), (x + 8, y + 10))                       # the pillow end
            d.line((x + ww - 8, y + 2), (x + ww - 8, y + 10))
    _box(d, xa + ww + 6, wy + wh / 2 - 8, 24, 11)                         # the pupil's own bed
    for x in (xa + ww, xb):                                               # the doors from her room
        d.line((x, wy + wh / 2 + 14), (x + (6 if x == xa + ww else -6), wy + wh / 2 + 20))
    d.arc(cx, cy, R - 16, _hour(14), _hour(17), n=24)                     # the afternoon off
    for h in (5.5, 21):
        d.line(_pt(cx, cy, R, _hour(h)), _pt(cx, cy, R + 12, _hour(h)))
    d.circle(cx, cy, 2.5)
    d.group('mid')
    d.text(xa + ww / 2, wy + wh + 20, '6 BEDS', size=7)
    d.text(xb + ww / 2, wy + wh + 20, '6 BEDS', size=7)
    d.text(xa + ww + 18, wy - 14, 'NURSE', size=7)
    d.text(cx, cy - R - 22, 'MIDNIGHT', size=7)
    x, y = _pt(cx, cy, R - 22, _hour(5.5))
    d.text(x - 4, y + 3, '5.30', size=7)
    x, y = _pt(cx, cy, R + 24, _hour(21))
    d.text(x - 6, y, '9 PM', size=7)
    x, y = _pt(cx, cy, R - 34, _hour(15.5))
    d.text(x + 4, y + 6, '2–5', size=7)
    d.text(cx, cy + R + 32, 'ON THE WARDS · 15½ H', size=7)
    return d


def henry_street():
    d = D()
    # The Henry Street visiting nurse's bag as Waters described it in 1909: leather, 14 inches long,
    # 6 wide and 7 1/2 high, with long handles and a soft flap; drawn in cabinet oblique (depth at 45
    # degrees, half scale), 12 px to the inch. Beside it, the removable lining's row of bottles and jars
    # in elevation: one 3-oz and five 1-oz bottles, two 2-oz and two 1-oz jars.
    s = 12
    L, W, H = 14 * s, 6 * s, 7.5 * s
    ox, oy = 26, 236                                                      # front bottom-left corner
    dx, dy = W / 2 * math.cos(math.radians(45)), -W / 2 * math.sin(math.radians(45))
    F = [(ox, oy), (ox + L, oy), (ox + L, oy - H), (ox, oy - H)]          # the front face
    B = [(x + dx, y + dy) for x, y in F]                                  # the back face
    d.group('thin')
    d.line(B[0], B[1])                                                    # the hidden back edges
    d.line(B[0], B[3])
    d.line(F[0], B[0])
    d.line((ox, oy + 16), (ox + L, oy + 16))                              # the dimension lines
    for x in (ox, ox + L):
        d.line((x, oy + 10), (x, oy + 22))
    d.line((ox - 12, oy), (ox - 12, oy - H))
    for y in (oy, oy - H):
        d.line((ox - 18, y), (ox - 6, y))
    d.line((F[1][0] + 12, F[1][1]), (B[1][0] + 12, B[1][1]))
    d.group()
    d.line(*F, closed=True)
    d.line(F[1], B[1], B[2], F[2])
    d.line(F[3], B[3], B[2])
    # the handles: two long loops rising from the top's front and back edges
    for (p, q) in ((F[3], F[2]), (B[3], B[2])):
        a = (p[0] + 0.28 * (q[0] - p[0]), p[1])
        b = (p[0] + 0.72 * (q[0] - p[0]), p[1])
        mx, top = (a[0] + b[0]) / 2, p[1] - 58
        d.curve(f'M{a[0]:.1f} {a[1]:.1f} C{a[0]:.1f} {top:.1f} {b[0]:.1f} {top:.1f} {b[0]:.1f} {b[1]:.1f}')
    d.group('mid')
    # the soft flap over the top, falling over the front
    d.curve(f'M{F[3][0] + 8:.1f} {F[3][1]:.1f} Q{F[3][0] + 6:.1f} {F[3][1] + 30:.1f} {F[3][0] + 20:.1f} {F[3][1] + 34:.1f}'
            f' L{F[2][0] - 20:.1f} {F[2][1] + 34:.1f} Q{F[2][0] - 6:.1f} {F[2][1] + 30:.1f} {F[2][0] - 8:.1f} {F[2][1]:.1f}')
    d.line((ox + L / 2 - 6, oy - H + 34), (ox + L / 2 + 6, oy - H + 34), (ox + L / 2 + 6, oy - H + 42),
           (ox + L / 2 - 6, oy - H + 42), closed=True)                    # the clasp
    # the lining's row of bottles and jars, in elevation, on its own base line
    bx, by = 262, 236
    d.line((bx - 6, by), (bx + 128, by))
    x = bx
    for kind, w, h in [('b', 14, 50)] + [('b', 10, 36)] * 5 + [('j', 14, 22)] * 2 + [('j', 11, 18)] * 2:
        if kind == 'b':                                                   # a bottle: body, shoulder, neck
            d.line((x, by), (x, by - h * 0.7), (x + w * 0.3, by - h * 0.85), (x + w * 0.3, by - h),
                   (x + w * 0.7, by - h), (x + w * 0.7, by - h * 0.85), (x + w, by - h * 0.7), (x + w, by))
        else:                                                             # a jar: body and lid
            _box(d, x, by - h, w, h)
            d.line((x - 1, by - h - 3), (x + w + 1, by - h - 3), (x + w + 1, by - h), (x - 1, by - h))
        x += w + 2
    d.group('mid')
    d.text(ox + L / 2, oy + 32, '14 IN', size=7)
    d.text(ox - 16, oy - H / 2 + 3, '7½', size=7, anchor='end')
    d.text(F[1][0] + 30, F[1][1] - 14, '6 IN', size=7)
    d.text(bx + 61, by + 16, 'BOTTLES AND JARS', size=7)
    d.text(bx + 61, by + 26, 'IN THE LINING', size=7)
    return d


def licensure():
    d = D()
    # North Carolina's act of March 1903, the first in the United States, as a mechanism: the state
    # medical society elects two physicians and the nurses' association three nurses to a board of five
    # (a quorum of three, one of them a physician); from 1904 the board examines in its subjects and
    # licenses ($5), and the clerk of the Superior Court registers the license (50 cents) in the county's
    # book; the holder may write R.N. Untrained nurses may still nurse: only the title is protected.
    cx, cy, R = 200, 112, 46
    d.group('thin')
    d.circle(cx, cy, R)                                                   # the board's table
    d.line((cx, 14), (cx, 290))                                           # the axis of the act
    d.group()
    _box(d, 20, 22, 112, 30)                                              # the two electing bodies
    _box(d, 268, 22, 112, 30)
    seats = [_pt(cx, cy, R, a) for a in (150, 195, 240, 285, 330)]
    for k, (x, y) in enumerate(seats):                                    # five seats round the table
        d.circle(x, y, 7)
        if k < 2:                                                         # a physician: a cross in the seat
            d.line((x - 4, y), (x + 4, y))
            d.line((x, y - 4), (x, y + 4))
    _box(d, 128, 172, 144, 28)                                            # the examination
    _box(d, 20, 236, 112, 30)                                             # the license
    _box(d, 268, 236, 112, 30)                                            # the county's register
    d.group('mid')
    for a, b in (((76, 52), seats[0]), ((76, 52), seats[1]), ((324, 52), seats[2]), ((324, 52), seats[3]), ((324, 52), seats[4])):
        q = (b[0] + 8 * (a[0] - b[0]) / math.dist(a, b), b[1] + 8 * (a[1] - b[1]) / math.dist(a, b))
        d.line(a, q)
        _arrow(d, a, q, 5)
    d.line((cx, cy + R), (cx, 172))
    _arrow(d, (cx, cy + R), (cx, 172), 6)
    d.line((cx, 200), (cx, 218), (76, 218), (76, 236))
    _arrow(d, (76, 218), (76, 236), 6)
    d.line((132, 251), (268, 251))
    _arrow(d, (132, 251), (268, 251), 6)
    for k in range(8):                                                    # the eight subjects, as ticks
        x = 140 + k * 17
        d.line((x, 192), (x + 10, 192))
    d.group('mid')
    d.text(76, 40, 'MEDICAL SOCIETY', size=7)
    d.text(324, 40, 'NURSES ASSOCIATION', size=7)
    d.text(cx, cy + 3, 'BOARD OF 5', size=7)
    d.text(cx, cy + 14, 'QUORUM 3', size=7)
    d.text(cx, 184, 'EXAMINATION', size=7)
    d.text(76, 254, 'LICENSE · $5', size=7)
    d.text(324, 254, 'REGISTER · 50¢', size=7)
    d.text(cx, 242, 'CLERK OF COURT', size=7)
    d.text(cx, 286, 'TITLE: R.N.', size=7)
    return d


def goldmark_report():
    d = D()
    # The Goldmark committee's proposal of 1923 against the course it found: above, the months of the
    # three-year hospital course and of the proposed 28 (a preliminary term of 4 months, then 24 of a
    # graded course, 2 of them vacation), on one scale, 9 px to the month; below, a student's week as
    # squares of an hour each: the median of 54 hours on duty in the 23 schools studied, against the
    # committee's limit of 48 (and preferably 44), class work included.
    x0, m = 36, 9
    d.group('thin')
    for k in range(37):                                                   # a tick each month
        x = x0 + k * m
        d.line((x, 40), (x, 44 if k % 12 else 48))
    d.line((x0, 44), (x0 + 36 * m, 44))
    for k in (0, 4, 28, 36):                                              # the course's divisions
        d.line((x0 + k * m, 48), (x0 + k * m, 128))
    gx, gy, c = 80, 150, 13                                               # the week's grids, a square an hour
    hx = 250
    for X in (gx, hx):
        for r in range(10):
            d.line((X, gy + r * c), (X + 6 * c, gy + r * c))
        for k in range(7):
            d.line((X + k * c, gy), (X + k * c, gy + 9 * c))
    d.group()
    _box(d, x0, 62, 36 * m, 18)                                           # the three-year course
    _box(d, x0, 100, 4 * m, 18)                                           # the preliminary term
    _box(d, x0 + 4 * m, 100, 24 * m, 18)                                  # the graded course
    for h in range(54):                                                   # 54 hours, in rows of 6
        r, k = divmod(h, 6)
        x, y = gx + k * c + 2, gy + r * c + 2
        _box(d, x, y, c - 4, c - 4)
    for h in range(48):                                                   # 48 hours, in rows of 6
        r, k = divmod(h, 6)
        x, y = hx + k * c + 2, gy + r * c + 2
        _box(d, x, y, c - 4, c - 4)
    d.group('mid')
    for k in range(2):                                                    # the two months of vacation, left open
        x = x0 + (26 + k) * m
        d.line((x, 100), (x, 118))
    d.group('mid')
    for k, lab in ((0, '0'), (12, '12'), (24, '24'), (36, '36 MONTHS')):
        d.text(x0 + k * m, 34, lab, size=7, anchor='start' if k == 0 else ('end' if k == 36 else 'middle'))
    d.text(x0 + 18 * m, 92, 'THE HOSPITAL COURSE · 3 YEARS', size=7)
    d.text(x0 + 16 * m, 132, 'PROPOSED · 4 + 24 = 28', size=7)
    d.text(gx + 3 * c, gy + 9 * c + 16, '54 H · MEDIAN', size=7)
    d.text(hx + 3 * c, gy + 9 * c + 16, '48 H · PROPOSED', size=7)
    return d


PLATES = {
    'training-schools': training_schools,
    'henry-street': henry_street,
    'licensure': licensure,
    'goldmark-report': goldmark_report,
}
