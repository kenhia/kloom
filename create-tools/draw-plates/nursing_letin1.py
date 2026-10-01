"""Plates for Keeping Watch's trail Who was let in, first part (sprint 030): Mary Mahoney, the Mills
School and the NACGN. See plates_for.py."""
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


def _bed(d, x, y, w=30, h=13, head='left'):
    """A ward bed in plan: the frame and the pillow line at its head."""
    _box(d, x, y, w, h)
    hx = x + 6 if head == 'left' else x + w - 6
    d.line((hx, y + 2), (hx, y + h - 2))


def mary_mahoney():
    d = D()
    # The New England Hospital's course as its reports of 1875-1879 set it out, drawn to scale in
    # months: two weeks on probation, a year on the wards (medical, surgical, children's,
    # confinement and night nursing, in an order the reports do not give), four months to prove
    # competence; the weekly allowance of $1, $2 and $3 beneath. Below, the ward of six beds that
    # each pupil had charge of, as a schematic.
    x0, x1, ty = 52, 372, 92                                              # 16 months, 20 px a month
    m = (x1 - x0) / 16
    d.group('thin')
    for k in range(17):                                                   # the month ticks
        d.line((x0 + k * m, ty - 4), (x0 + k * m, ty + 4))
    for k in (0, 6, 12, 16):                                              # the allowance changes
        d.line((x0 + k * m, ty + 6), (x0 + k * m, ty + 30))
    d.line((x0 - m / 2, ty - 10), (x0 - m / 2, ty + 4))                   # probation starts
    d.line((200, 150), (200, 284))                                        # the ward's axis
    d.group()
    d.line((x0 - m / 2, ty), (x1, ty))                                    # the course
    _box(d, x0 - m / 2, ty - 3, m / 2, 6)                                 # two weeks' probation
    # the year on the wards and the four months, bracketed above
    d.line((x0, ty - 14), (x0, ty - 20), (x0 + 12 * m, ty - 20), (x0 + 12 * m, ty - 14))
    d.line((x0 + 12 * m + 2, ty - 14), (x0 + 12 * m + 2, ty - 20), (x1, ty - 20), (x1, ty - 14))
    # the ward of six beds: walls, door, beds on both walls, the nurse's table on the axis
    wx, wy, ww, wh = 120, 156, 160, 116
    d.line((wx + 64, wy + wh), (wx, wy + wh), (wx, wy), (wx + ww, wy), (wx + ww, wy + wh), (wx + 96, wy + wh))
    d.group('mid')
    for k, s in enumerate(('MEDICAL', 'SURGICAL', "CHILDREN'S", 'CONFINEMENT', 'NIGHT')):
        cx = x0 + (k + 0.5) * 12 * m / 5                                 # five services, order not given
        d.circle(cx, ty - 52, 4)
        d.line((cx, ty - 48), (cx, ty - 36))
    for k in range(3):
        y = wy + 14 + k * 34
        _bed(d, wx + 4, y, w=40, h=18, head='left')
        _bed(d, wx + ww - 44, y, w=40, h=18, head='right')
    _box(d, 188, 200, 24, 16)                                             # the nurse's table
    d.arc(wx + 64, wy + wh, 32, 270, 360, n=16)                           # the door's swing
    d.group('mid')
    d.text(x0 - m / 4, ty - 24, 'PROBATION', size=7)
    d.text(x0 + 6 * m, ty - 25, 'A YEAR ON THE WARDS', size=7)
    d.text(x0 + 14 * m, ty - 25, 'FOUR TO PROVE', size=7)
    for k, s in enumerate(('MED', 'SURG', 'CHILD', 'CONF', 'NIGHT')):
        d.text(x0 + (k + 0.5) * 12 * m / 5, ty - 60, s, size=7)
    d.text(x0 + 3 * m, ty + 22, '$1 A WEEK', size=7)
    d.text(x0 + 9 * m, ty + 22, '$2 A WEEK', size=7)
    d.text(x0 + 14 * m, ty + 22, '$3', size=7)
    d.text(x0, ty + 40, '0', size=7)
    d.text(x0 + 12 * m, ty + 40, '12', size=7)
    d.text(x1, ty + 40, '16 MONTHS', size=7, anchor='end')
    d.text(200, 292, 'ONE PUPIL · ONE WARD · SIX BEDS', size=7)
    return d


def mills_school():
    d = D()
    # The Mills School's terms from its report of 1892. Left, a pupil's day on a 24-hour dial: duty
    # from 8 a.m. to 8 p.m. Right, the two-year course on probation, then a first year at $12 a month
    # and a second at $15. Below, the wards: the five medical wards the school took over in 1888, and
    # the eight medical, ten surgical and one prison ward it had by 1892, one square a ward.
    cx, cy, R = 92, 112, 62
    d.group('thin')
    d.circle(cx, cy, R + 8)
    for h in range(24):                                                   # an hour a tick, midnight at top
        a = h * 15 - 90
        d.line(_pt(cx, cy, R, a), _pt(cx, cy, R + (8 if h % 6 == 0 else 4), a))
    d.line((cx, cy - R - 12), (cx, cy + R + 12))
    x0, x1, ty = 196, 376, 92                                             # 24 months and one of probation
    m = (x1 - x0) / 25
    for k in range(26):
        d.line((x0 + k * m, ty - 3), (x0 + k * m, ty + 3))
    for k in (1, 13, 25):
        d.line((x0 + k * m, ty + 4), (x0 + k * m, ty + 26))
    d.group()
    d.circle(cx, cy, R)
    d.arc(cx, cy, R - 12, 8 * 15 - 90, 20 * 15 - 90, n=48)               # 8 a.m. to 8 p.m.
    d.line(_pt(cx, cy, R - 18, 8 * 15 - 90), _pt(cx, cy, R - 6, 8 * 15 - 90))
    d.line(_pt(cx, cy, R - 18, 20 * 15 - 90), _pt(cx, cy, R - 6, 20 * 15 - 90))
    d.line((x0, ty), (x1, ty))
    _box(d, x0, ty - 4, m, 8)                                             # a month on probation
    d.group('mid')
    # the wards, one square each: 5 in 1888, 19 by 1892 (8 medical, 10 surgical, 1 prison)
    s, gap, y88, y92 = 13, 4, 214, 258
    for k in range(5):
        _box(d, 64 + k * (s + gap), y88, s, s)
    for k in range(19):
        x = 64 + k * (s + gap)
        _box(d, x, y92, s, s)
        if k >= 8 and k < 18:                                             # surgical wards: a cross
            d.line((x + 3, y92 + s / 2), (x + s - 3, y92 + s / 2))
            d.line((x + s / 2, y92 + 3), (x + s / 2, y92 + s - 3))
        if k == 18:                                                       # the prison ward: bars
            for j in (4, 6.5, 9):
                d.line((x + j, y92 + 2), (x + j, y92 + s - 2))
    d.group('mid')
    d.text(cx, cy + 4, 'ON DUTY', size=7)
    d.text(cx, cy - R - 16, 'MIDNIGHT', size=7)
    d.text(cx + R + 20, cy + 3, '6', size=7)
    d.text(cx - R - 20, cy + 3, '18', size=7)
    d.text(cx, cy + R + 20, 'NOON', size=7)
    d.text(x0 + m / 2, ty - 10, 'PROBATION', size=7)
    d.text(x0 + 7 * m, ty + 20, '$12 A MONTH', size=7)
    d.text(x0 + 19 * m, ty + 20, '$15 A MONTH', size=7)
    d.text(x0 + 13 * m, ty - 10, 'TWO YEARS', size=7)
    d.text(28, y88 + 10, '1888', size=7)
    d.text(28, y92 + 10, '1892', size=7)
    d.text(64 + 4 * (s + gap) + 60, y88 + 10, '5 MEDICAL WARDS', size=7)
    d.text(64 + 13 * (s + gap) - 2, y92 + 30, '8 MEDICAL · 10 SURGICAL · 1 PRISON', size=7)
    return d


def nacgn():
    d = D()
    # Membership as a mechanism. From 1916 a nurse joined the ANA only through her state
    # association (the alumnae route, open before, is drawn faint); where the state association
    # refused Black nurses, the path stopped at its gate. The NACGN, from 1908, took any graduate of a
    # recognized two-year school. The ANA's individual membership of 1948 is the dashed bypass, and
    # the NACGN's dissolution into the ANA in 1951 the last arrow.
    nx, ny = 46, 150                                                      # the graduate nurse
    sx, sy = 196, 150                                                     # the state association
    ax, ay = 340, 150                                                     # the ANA
    kx, ky = 196, 248                                                     # the NACGN
    d.group('thin')
    d.line((20, ny), (380, ny))                                           # the main axis
    d.line((nx, ny + 24), (nx, ky), (kx - 40, ky))                        # the NACGN's branch line
    d.line((sx, 40), (sx, 270))
    d.line((nx, ny - 24), (nx, 64), (sx - 44, 64))                        # the old alumnae route
    d.line((sx + 44, 64), (ax, 64), (ax, ay - 24))
    _box(d, sx - 44, 50, 88, 28)
    d.group()
    d.circle(nx, ny, 22)                                                  # the nurse
    _box(d, sx - 44, sy - 22, 88, 44)                                     # state association
    d.circle(ax, ay, 26)                                                  # the ANA
    _box(d, kx - 40, ky - 18, 80, 36)                                     # the NACGN
    d.line((nx + 22, ny), (sx - 62, ny))                                  # nurse to the gate
    _arrow(d, (nx + 22, ny), (sx - 62, ny))
    d.group('mid')
    # the gate: two posts and a barred leaf across the path
    for y in (ny - 16, ny + 16):
        d.line((sx - 58, y - 6), (sx - 58, y + 6))
    d.line((sx - 58, ny - 16), (sx - 52, ny + 16))
    d.line((sx - 52, ny - 16), (sx - 58, ny + 16))
    d.line((sx + 44, ny), (ax - 26, ny))                                  # state to the ANA
    _arrow(d, (sx + 44, ny), (ax - 26, ny))
    _arrow(d, (nx, ky - 30), (nx, ky - 4))
    d.line((nx, ky), (kx - 40, ky))
    _arrow(d, (nx, ky), (kx - 40, ky))
    # 1948: individual membership, a dashed bypass over the gate
    pts = [(nx + 16, ny - 16)] + [(nx + 16 + (ax - nx - 34) * t, ny - 16 - 48 * math.sin(math.pi * t))
                                  for t in [k / 24 for k in range(1, 25)]]
    for k in range(0, len(pts) - 1, 2):
        d.line(pts[k], pts[k + 1])
    _arrow(d, pts[-2], pts[-1])
    # 1951: the NACGN into the ANA
    d.line((kx + 40, ky), (ax, ky), (ax, ay + 26))
    _arrow(d, (ax, ky), (ax, ay + 26))
    d.group('mid')
    d.text(nx, ny + 3, 'NURSE', size=7)
    d.text(sx, sy - 2, 'STATE', size=7)
    d.text(sx, sy + 8, 'ASSOCIATION', size=7)
    d.text(ax, ay + 3, 'ANA', size=7)
    d.text(kx, ky + 3, 'NACGN · 1908', size=7)
    d.text(sx, 67, 'ALUMNAE, TO 1916', size=7)
    d.text(sx - 55, ny + 34, 'GATE · 1916', size=7)
    d.text(294, 86, '1948 · INDIVIDUAL', size=7)
    d.text(ax + 2, ky + 16, '1951', size=7)
    return d


PLATES = {
    'mary-mahoney': mary_mahoney,
    'mills-school': mills_school,
    'nacgn': nacgn,
}
