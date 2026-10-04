"""Plates for western-civ's frames of part ant1 (sprint 049): the Hebrew Bible, Athenian democracy
and Greek tragedy. See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def hebrew_bible():
    d = D()
    # Top: the Great Isaiah Scroll (1QIsa-a) to scale, 7.34 m long and about 0.26 m high, 17 sheets,
    # 54 columns (Wikipedia, Isaiah Scroll). The sheets are drawn of equal width, a simplification.
    # Below: a time axis from 700 BC to AD 1100 with the dates the reading gives, and the thousand
    # years between the scroll (c. 125 BC; radiocarbon 356-103 BC) and the codices of the 10th century.
    x0, x1 = 30, 370
    s = (x1 - x0) / 7.34                                               # units per meter
    sh = 0.26 * s
    sy = 58

    def tx(year):                                                      # year (negative BC) to x
        return x0 + (year + 700) / 1800 * (x1 - x0)

    ay = 250                                                           # the time axis

    d.group('thin')
    d.line((x0, sy - 14), (x1, sy - 14))                               # the scroll's length, dimensioned
    for x in (x0, x1):
        d.line((x, sy - 18), (x, sy - 4))
    for m in range(0, 8):                                              # a meter scale under the scroll
        x = x0 + m * s
        d.line((x, sy + sh + 4), (x, sy + sh + 8))
    d.line((x0, sy + sh + 6), (x0 + 7 * s, sy + sh + 6))
    d.line((x0, ay), (x1, ay))                                         # the time axis
    for y in range(-700, 1101, 100):
        d.line((tx(y), ay), (tx(y), ay + (6 if y % 500 == 0 or y == 0 else 3)))
    d.line((tx(-125), sy + sh + 12), (tx(-125), 196))                  # the scroll down to its date

    d.group()
    # the scroll, open, its two ends rolled
    _box(d, x0, sy, x1 - x0, sh)
    for x in (x0, x1):
        d.ellipse(x, sy + sh / 2, 3, sh / 2 + 2)
    # the bands of time
    bands = [(-587, -539, 'EXILE', 112), (-450, -350, 'TORAH FINISHED', 136),
             (-250, 70, 'QUMRAN SCROLLS', 160)]
    for a, b, _, y in bands:
        _box(d, tx(a), y, tx(b) - tx(a), 10)
    for yr, y in ((930, 196), (1008, 196)):                            # the codices
        d.circle(tx(yr), y, 3)
    d.circle(tx(-125), 196, 3)                                          # the Isaiah Scroll

    d.group('mid')
    # 17 sheets and 54 columns
    for i in range(1, 17):
        x = x0 + i * (x1 - x0) / 17
        d.line((x, sy), (x, sy + sh))
    cols = []
    for i in range(54):
        x = x0 + (i + 0.5) * (x1 - x0) / 54
        cols.append([(x - 1.6, sy + 2.5), (x + 1.6, sy + 2.5)])
        cols.append([(x - 1.6, sy + sh - 2.5), (x + 1.6, sy + sh - 2.5)])
    d.lines(cols)
    # the radiocarbon range of the Isaiah Scroll, and the thousand years to the codices
    d.line((tx(-356), 186), (tx(-103), 186))
    for x in (tx(-356), tx(-103)):
        d.line((x, 183), (x, 189))
    d.line((tx(-125) + 6, 214), (tx(930) - 6, 214))
    _arrow(d, (tx(-125) + 20, 214), (tx(-125) + 4, 214))
    _arrow(d, (tx(930) - 20, 214), (tx(930) - 4, 214))

    d.group('mid')
    d.text((x0 + x1) / 2, sy - 18, '7.34 M · 17 SHEETS · 54 COLUMNS', size=7)
    d.text(x0, sy + sh + 18, '0', size=7)
    d.text(x0 + 7 * s, sy + sh + 18, '7 M', size=7)
    d.text((x0 + x1) / 2, 32, 'THE ISAIAH SCROLL · 1QISA-A', size=7)
    for a, b, lab, y in bands:
        if lab.startswith('TORAH'):
            d.text(tx(a) - 5, y + 8, lab, size=7, anchor='end')
        else:
            d.text(tx(b) + 5, y + 8, lab, size=7, anchor='start')
    d.text(tx(-356) - 4, 189, 'C. 125 BC', size=7, anchor='end')
    d.text(tx(969), 186, 'CODICES', size=7)
    d.text((tx(-125) + tx(930)) / 2, 228, 'ABOUT 1,000 YEARS', size=7)
    for y, lab in ((-500, '500 BC'), (0, 'BC | AD'), (500, 'AD 500'), (1000, 'AD 1000')):
        d.text(tx(y), ay + 16, lab, size=7)
    return d


def athenian_democracy():
    d = D()
    # A kleroterion in elevation, after the Agora fragment I 3967: 0.73 m wide (drawn to scale),
    # eleven columns of slots, the tube fixed at the left (Agora excavations' record). Its rows are
    # drawn at an even pitch; the count of rows is schematic. Dice fall from the funnel down the tube,
    # and each die decides one row, from the top: white chooses it, black passes it (Constitution of
    # the Athenians 64). Black dice are drawn hatched, white ones open.
    s = 210 / 0.73                                                    # units per meter
    w, h = 0.73 * s, 0.588 * s
    x0, y0 = 110, 62
    cols, rows = 11, 16
    mx, my = 12, 12
    pitch_x = (w - 2 * mx) / cols
    pitch_y = (h - 2 * my) / rows
    tube_x = x0 - 22
    dice = 'WBWWBWBBWWBWBWWB'                                          # one die per row, top first

    def row_y(r):
        return y0 + my + (r + 0.5) * pitch_y

    d.group('thin')
    for c in range(cols + 1):                                          # the column grid
        x = x0 + mx + c * pitch_x
        d.line((x, y0 + 4), (x, y0 + h - 4))
    for r in range(rows):                                              # each die to its row
        d.line((tube_x + 6, row_y(r)), (x0 + mx, row_y(r)))
    d.line((x0, y0 + h + 12), (x0 + w, y0 + h + 12))                    # width, dimensioned
    for x in (x0, x0 + w):
        d.line((x, y0 + h + 6), (x, y0 + h + 18))

    d.group()
    _box(d, x0, y0, w, h)                                              # the slab
    d.line((tube_x - 5, y0 - 30), (tube_x - 5, y0 + h))                 # the tube, with its funnel
    d.line((tube_x + 5, y0 - 30), (tube_x + 5, y0 + h))
    d.line((tube_x - 5, y0 - 30), (tube_x - 16, y0 - 48))
    d.line((tube_x + 5, y0 - 30), (tube_x + 16, y0 - 48))
    d.line((tube_x - 5, y0 + h), (tube_x + 5, y0 + h))

    d.group('mid')
    slots = []
    for c in range(cols):
        for r in range(rows):
            cx = x0 + mx + (c + 0.5) * pitch_x
            slots.append([(cx - 4.5, row_y(r)), (cx + 4.5, row_y(r))])
    d.lines(slots)
    hatch = []
    for r, k in enumerate(dice):
        d.circle(tube_x, row_y(r), 3.6)
        if k == 'B':
            hatch.append([(tube_x - 2.5, row_y(r) - 2.5), (tube_x + 2.5, row_y(r) + 2.5)])
            hatch.append([(tube_x - 2.5, row_y(r) + 2.5), (tube_x + 2.5, row_y(r) - 2.5)])
    d.lines(hatch)

    d.group()
    for r, k in enumerate(dice):                                       # the rows the white dice choose
        if k == 'W':
            y = row_y(r)
            d.line((x0 + w + 6, y - 3), (x0 + w + 10, y), (x0 + w + 6, y + 3))

    d.group('mid')
    d.text(x0 + w / 2, y0 + h + 30, '0.73 M · AGORA I 3967', size=7)
    d.text(x0 + w / 2, y0 - 10, 'ELEVEN COLUMNS OF TICKETS', size=7)
    d.text(tube_x, y0 - 54, 'DICE', size=7)
    d.text(x0 + w + 16, row_y(0) + 3, 'WHITE DIE:', size=7, anchor='start')
    d.text(x0 + w + 16, row_y(0) + 13, 'ROW CHOSEN', size=7, anchor='start')
    d.text(x0 + w + 16, row_y(4) + 3, 'BLACK DIE:', size=7, anchor='start')
    d.text(x0 + w + 16, row_y(4) + 13, 'ROW PASSED', size=7, anchor='start')
    d.text(tube_x - 10, y0 + h + 30, 'TUBE', size=7)
    return d


def greek_tragedy():
    d = D()
    # A Greek theater laid out by Vitruvius's rule (On Architecture V.7, Morgan's translation): three
    # squares inscribed in the orchestra circle; the side of one square nearest the stage fixes the
    # front of the stage (A-B); a parallel line tangent to the circle fixes the front of the skene;
    # through the center, parallel to the stage, the diameter E-F, from whose ends arcs of radius
    # E-F swing down to the stage. The stairways of the lower seats rise from the squares' corners,
    # and above the cross-aisle (diazoma) further stairways are set midway between them.
    cx, cy, r = 200, 170, 44
    r_in, r_dia, r_out = r * 1.12, r * 2.0, r * 2.85

    def pt(a, rad):
        return (cx + rad * math.cos(math.radians(a)), cy + rad * math.sin(math.radians(a)))

    seat_a0, seat_a1 = 165, 375                                        # the seats, round the top
    corners = [15 + 30 * k for k in range(12)]
    lower = [a for a in range(165, 376, 30)]                           # corners on the seating side
    upper = sorted(set(lower) | {a + 15 for a in lower[:-1]})

    d.group('thin')
    d.circle(cx, cy, r)                                                # the orchestra circle
    for k in range(3):                                                 # three inscribed squares
        d.line(*[pt(45 + 30 * k + 90 * j, r) for j in range(4)], closed=True)
    e, f_ = (cx - r, cy), (cx + r, cy)
    d.line((e[0] - 30, cy), (f_[0] + 30, cy))                          # the line E-F through the center
    a_y = cy + r * math.cos(math.radians(45))                          # the stage front, A-B
    d.line((cx - 2.2 * r, a_y), (cx + 2.2 * r, a_y))
    d.line((cx - 2.2 * r, cy + r), (cx + 2.2 * r, cy + r))              # the skene front, C-D
    # arcs of radius E-F (= 2r) from each end, swinging down to the stage line
    def swing(c0, sgn):
        dy = a_y - cy
        a_end = math.degrees(math.asin(dy / (2 * r)))
        pts = []
        for i in range(25):
            a = a_end * i / 24
            pts.append((c0[0] + sgn * 2 * r * math.cos(math.radians(a)), cy + 2 * r * math.sin(math.radians(a))))
        d.line(*pts)
    swing(f_, -1)
    swing(e, 1)

    d.group()
    d.arc(cx, cy, r_in, seat_a0, seat_a1, n=70)                        # the front row
    d.arc(cx, cy, r_dia, seat_a0, seat_a1, n=70)                       # the cross-aisle
    d.arc(cx, cy, r_dia + 10, seat_a0, seat_a1, n=70)
    d.arc(cx, cy, r_out, seat_a0, seat_a1, n=70)                       # the back wall
    for a in (seat_a0, seat_a1):                                       # the retaining walls
        d.line(pt(a, r_in), pt(a, r_out))
    _box(d, cx - 2.2 * r, cy + r, 4.4 * r, 0.62 * r)                   # the skene
    d.line((cx - 1.8 * r, a_y), (cx - 1.8 * r, cy + r))                # the stage, A-B to C-D
    d.line((cx + 1.8 * r, a_y), (cx + 1.8 * r, cy + r))

    d.group('mid')
    rows = []
    rad = r_in + 6
    while rad < r_out - 3:
        if not (r_dia - 3 < rad < r_dia + 13):
            rows.append([pt(seat_a0 + (seat_a1 - seat_a0) * i / 60, rad) for i in range(61)])
        rad += 6
    d.lines(rows)
    stairs = [[pt(a, r_in), pt(a, r_dia)] for a in lower]
    stairs += [[pt(a, r_dia + 10), pt(a, r_out)] for a in upper]
    d.lines(stairs)
    for a in corners:                                                  # the twelve corners
        x, y = pt(a, r)
        d.circle(x, y, 1.6)

    d.group('mid')
    d.text(cx, cy + 3, 'ORCHESTRA', size=7)
    d.text(cx, cy + r + 0.31 * r + 3, 'SKENE', size=7)
    d.text(e[0] + 5, cy - 4, 'E', size=7, anchor='start')
    d.text(f_[0] - 5, cy - 4, 'F', size=7, anchor='end')
    d.text(cx + 2.2 * r + 4, a_y + 3, 'A–B', size=7, anchor='start')
    d.text(cx, cy - r_dia - 2.5, 'DIAZOMA', size=7)
    d.text(cx, 272, 'AFTER VITRUVIUS V.7 · THREE SQUARES IN THE CIRCLE', size=7)
    return d


PLATES = {'greek-tragedy': greek_tragedy, 'hebrew-bible': hebrew_bible, 'athenian-democracy': athenian_democracy}
