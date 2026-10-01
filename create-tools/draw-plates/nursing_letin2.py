"""Plates for Keeping Watch's trail Who was let in, its last three frames (sprint 030). See plates_for.py."""
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


def cadet_nurse_corps():
    d = D()
    # The cadet's course as the Public Health Service laid it out (PHS Publication 38, pp. 18-19,
    # 35-36): the usual 36-month course above, the Corps' below, compressed into 30 months of study
    # (9 as a pre-cadet, 21 as a junior cadet) and 6 of full-time service as a senior cadet. Over it,
    # the monthly allowance as a step graph: $15, $20, then at least $30 from the hospital served.
    # At right, the argument for it: three students for two graduates, drawn as one area cut both ways.
    x0, x1 = 34, 286
    mo = (x1 - x0) / 36                                                   # pixels a month
    X = lambda m: x0 + m * mo
    yb, ys = 112, 52                                                      # the graph's $0 and $30 lines
    Y = lambda dollars: yb - (yb - ys) * dollars / 30
    d.group('thin')
    for m in range(0, 37, 3):                                             # month ticks, every quarter
        d.line((X(m), 124), (X(m), 132 if m % 12 else 136))
    d.line((x0, 128), (x1, 128))
    for v in (0, 10, 20, 30):                                             # the dollar grid
        d.line((x0, Y(v)), (x1, Y(v)))
    for m in (9, 30):                                                     # the stage boundaries, carried down
        d.line((X(m), ys - 8), (X(m), 232))
    d.line((x0, 222), (x1, 222))                                          # dimension line
    for m in (0, 9, 30, 36):
        d.line((X(m), 216), (X(m), 228))
    d.group()
    _box(d, x0, 146, x1 - x0, 18)                                         # the usual course
    _box(d, x0, 182, X(9) - x0, 18)                                       # pre-cadet
    _box(d, X(9), 182, X(30) - X(9), 18)                                  # junior cadet
    _box(d, X(30), 182, X(36) - X(30), 18)                                # senior cadet
    d.line((x0, Y(0)), (x0, Y(15)), (X(9), Y(15)), (X(9), Y(20)), (X(30), Y(20)), (X(30), Y(30)), (X(36), Y(30)))
    # the area argument: a 3-by-2 block of work, cut into three student columns or two graduate rows
    bx, by, bw, bh = 316, 66, 60, 66
    _box(d, bx, by, bw, bh)
    _box(d, bx, by + bh + 34, bw, bh)                                    # the same area of work
    d.group('mid')
    for k in (1, 2):
        d.line((bx + k * bw / 3, by), (bx + k * bw / 3, by + bh))         # three students
    d.line((bx + bw / 2, by + bh + 34), (bx + bw / 2, by + 2 * bh + 34))  # two graduates
    for k in range(1, 6):                                                 # senior cadet: hatched as service
        x = X(30) + k * (X(36) - X(30)) / 6
        d.line((x - 4, 200), (x + 2, 182))
    for m in (9, 30):
        _arrow(d, (X(m) - 12, 222), (X(m), 222), 4)
        _arrow(d, (X(m) + 12, 222), (X(m), 222), 4)
    d.group('mid')
    d.text(x0 - 4, Y(30) + 3, '$30', size=7, anchor='end')
    d.text(x0 - 4, Y(20) + 3, '$20', size=7, anchor='end')
    d.text(x0 - 4, Y(10) + 3, '$10', size=7, anchor='end')
    d.text((x0 + X(9)) / 2, Y(15) - 5, '$15', size=7)
    d.text((X(9) + X(30)) / 2, Y(20) - 5, '$20 A MONTH', size=7)
    d.text((X(30) + X(36)) / 2, Y(30) - 5, '$30+', size=7)
    d.text((x0 + x1) / 2, 160, 'THE USUAL COURSE · 36 MONTHS', size=7)
    d.text((x0 + X(9)) / 2, 213, 'PRE · 9', size=7)
    d.text((X(9) + X(30)) / 2, 213, 'JUNIOR CADET · 21', size=7)
    d.text((X(30) + X(36)) / 2, 213, 'SR · 6', size=7)
    d.text((x0 + X(30)) / 2, 246, 'STUDY · 30 MONTHS', size=7)
    d.text((X(30) + X(36)) / 2, 246, 'SERVICE', size=7)
    d.text(bx + bw / 2, by - 8, '3 STUDENTS', size=7)
    d.text(bx + bw / 2, by + 2 * bh + 48, '2 GRADUATES', size=7)
    d.text(bx + bw / 2, by + bh + 21, '=', size=9)
    d.text(160, 276, 'THE CADET’S COURSE · MONTHS', size=7)
    return d


def staupers():
    d = D()
    # The arithmetic of the Army's first quota on Black nurses (1940): wards for Black patients only,
    # eight at each of the two posts with the most Black soldiers, Fort Bragg and Camp Livingston,
    # staffed with 28 nurses at each hospital (Lee, The Employment of Negro Troops, pp. 197-198).
    # Each post drawn as a schematic of a cantonment hospital's ward block: a covered corridor with
    # four ward wings on each side; under it the 28 nurses as dots; 2 x 28 = 56, the quota.
    posts = [(28, 'FORT BRAGG, N.C.'), (212, 'CAMP LIVINGSTON, LA.')]
    w = 160
    d.group('thin')
    for x0, _ in posts:
        d.line((x0 - 6, 110), (x0 + w + 6, 110))                         # the corridor's axis
        for k in range(4):
            cx = x0 + 22 + k * 38
            d.line((cx, 50), (cx, 170))                                   # each wing's axis
        for r in range(4):                                                # the nurses' grid
            d.line((x0 + 38, 196 + r * 12), (x0 + 38 + 6 * 14, 196 + r * 12))
    d.line((200, 40), (200, 258))                                         # between the posts
    d.group()
    for x0, _ in posts:
        d.line((x0, 106), (x0 + w, 106))
        d.line((x0, 114), (x0 + w, 114))
        for k in range(4):
            cx = x0 + 22 + k * 38
            _box(d, cx - 12, 56, 24, 50)                                  # ward above the corridor
            _box(d, cx - 12, 114, 24, 50)                                 # and below it
    d.group('mid')
    for x0, _ in posts:
        for k in range(4):
            cx = x0 + 22 + k * 38
            for j in range(5):                                            # beds along each ward wall
                for y0 in (60, 118):
                    y = y0 + 4 + j * 8.5
                    d.line((cx - 10, y), (cx - 5, y))
                    d.line((cx + 5, y), (cx + 10, y))
        for r in range(4):
            for c in range(7):
                d.circle(x0 + 38 + c * 14, 196 + r * 12, 2.2)
    d.group('mid')
    for x0, name in posts:
        d.text(x0 + w / 2, 42, name, size=7)
        d.text(x0 + w / 2, 182, '8 WARDS', size=7)
        d.text(x0 + w / 2, 250, '28 NURSES', size=7)
    d.text(200, 278, '2 × 28 = 56 · THE QUOTA OF 1940', size=7)
    return d


def men_commissioned():
    d = D()
    # Who the law let in, as a plan: a wall along a scale of years for each corps, closed from the
    # founding acts that made each corps women only (Army 1901, Navy 1908), and doors drawn as an
    # architect draws them, a leaf and its swing, where men came in: the Army's reserve in 1955
    # (Public Law 294) and its regular corps in 1966 (Public Law 89-609); the Navy's first men in its
    # reserve in 1965 and its regular corps in 1968 (NHHC).
    y0, y1 = 1898, 1972
    xa, xb = 26, 374
    X = lambda yr: xa + (yr - y0) * (xb - xa) / (y1 - y0)
    lanes = [(110, 'ARMY NURSE CORPS', 1901, [(1955, 'RESERVE'), (1966, 'REGULAR')]),
             (196, 'NAVY NURSE CORPS', 1908, [(1965, 'RESERVE'), (1968, 'REGULAR')])]
    dw = 9                                                                # a door's width
    d.group('thin')
    d.line((xa, 252), (xb, 252))                                          # the scale
    for yr in range(1900, 1971):
        d.line((X(yr), 252), (X(yr), 256 if yr % 10 else 262))
    d.line((X(1901), 110), (X(1901), 252))                                # dates carried down to the scale
    d.line((X(1908), 196), (X(1908), 252))
    for yr in (1955, 1966):
        d.line((X(yr), 56 if yr == 1955 else 70), (X(yr), 252))
    d.group()
    for y, _, start, doors in lanes:
        xs = [X(start)] + [v for yr, _ in doors for v in (X(yr), X(yr) + dw)] + [X(1970)]
        for k in range(0, len(xs), 2):                                    # wall runs between the doors
            for dy in (-3, 3):
                d.line((xs[k], y + dy), (xs[k + 1], y + dy))
            d.line((xs[k], y - 3), (xs[k], y + 3))
            d.line((xs[k + 1], y - 3), (xs[k + 1], y + 3))
    d.group('mid')
    for y, _, _, doors in lanes:
        for yr, _ in doors:
            hx = X(yr)                                                    # the hinge
            d.line((hx, y - 3), (hx, y - 3 - dw))                         # the leaf, open
            d.arc(hx, y - 3, dw, -90, 0, n=12)                            # its swing
            d.line((hx + dw / 2, y + 22), (hx + dw / 2, y + 7))
            _arrow(d, (hx + dw / 2, y + 22), (hx + dw / 2, y + 7), 5)
    d.group('mid')
    for yr in range(1900, 1971, 10):
        d.text(X(yr), 272, str(yr), size=7)
    for y, name, start, doors in lanes:
        d.text(xa, y - 30, name, size=7, anchor='start')
        d.text(X(start) + 2, y - 10, f'{start} · WOMEN ONLY', size=7, anchor='start')
        for i, (yr, label) in enumerate(doors):
            d.text(X(yr) + (dw if i else 0) - 2, y + 34 + 12 * i, f'{yr} · {label}', size=7, anchor='end')
    d.text(X(1955) - 2, 62, 'PUBLIC LAW 294', size=7, anchor='end')
    d.text(X(1966) - 2, 76, 'PUBLIC LAW 89-609', size=7, anchor='end')
    return d


PLATES = {
    'cadet-nurse-corps': cadet_nurse_corps,
    'staupers': staupers,
    'men-commissioned': men_commissioned,
}
