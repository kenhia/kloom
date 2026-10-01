"""computing plates, segment "Counting and gears" (sprint 015). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _span(d, x0, x1, y):
    """A horizontal dimension line from x0 to x1 at height y, arrowed at both ends."""
    d.line((x0, y), (x1, y))
    _arrow(d, x0, y, math.pi)
    _arrow(d, x1, y, 0)


def abacus():
    """A soroban (one bead above the beam, four below) set to 1,946, the year of the Tokyo contest."""
    d = D()
    value = '000001946'
    n = len(value)
    x0, pitch = 60, 35
    xs = [x0 + pitch * i for i in range(n)]
    top, beam, bottom = 58, 112, 236
    bw, bh = 13, 8  # a bead's half-width and half-height (the soroban's double cone, a diamond in elevation)
    # construction: rod centre lines carried below the frame, the bead rest lines, the beam line
    d.group('thin')
    d.lines([[(x, top - 10), (x, bottom + 22)] for x in xs])
    rest_up = beam - bh - 1              # a counted upper bead rests on the beam
    rest_up_off = top + bh + 1            # an uncounted one at the top rail
    lower_on = [beam + bh + 1 + 2 * bh * k for k in range(4)]
    lower_off = [bottom - bh - 1 - 2 * bh * (3 - k) for k in range(4)]
    d.lines([[(x0 - 30, y), (xs[-1] + 30, y)] for y in (rest_up, rest_up_off, lower_on[0], lower_off[-1])])
    # the frame and the beam
    d.group()
    d.line((x0 - 22, top - 6), (xs[-1] + 22, top - 6), (xs[-1] + 22, bottom + 6), (x0 - 22, bottom + 6), closed=True)
    d.line((x0 - 22, beam - 3), (xs[-1] + 22, beam - 3))
    d.line((x0 - 22, beam + 3), (xs[-1] + 22, beam + 3))
    # the rods
    d.group('mid')
    d.lines([[(x, top - 6), (x, beam - 3)] for x in xs] + [[(x, beam + 3), (x, bottom + 6)] for x in xs])
    # every third rod carries a unit dot on the beam, as a soroban does
    for i in range(n - 1, -1, -3):
        d.circle(xs[i], beam, 1.4)

    def bead(x, y):
        d.line((x - bw, y), (x, y - bh), (x + bw, y), (x, y + bh), closed=True)

    # the beads: a digit v has its upper bead down if v >= 5 and v % 5 lower beads up
    d.group()
    for x, ch in zip(xs, value):
        v = int(ch)
        bead(x, rest_up if v >= 5 else rest_up_off)
        k = v % 5
        for j in range(4):
            bead(x, lower_on[j] if j < k else lower_off[j])
    # labels: each rod's digit and place, and the key
    d.group()
    for i, (x, ch) in enumerate(zip(xs, value)):
        d.text(x, bottom + 34, ch, size=10)
    d.text(xs[-1], bottom + 48, '10⁰', size=7)
    d.text(xs[-4], bottom + 48, '10³', size=7)
    d.text(xs[-7], bottom + 48, '10⁶', size=7)
    d.text(x0 - 26, rest_up + 3, '5', size=8, anchor='end')
    d.text(x0 - 26, lower_on[0] + 3, '1', size=8, anchor='end')
    d.text(200, 30, 'SOROBAN · ONE BEAD OF FIVE, FOUR OF ONE', size=8)
    return d


def _gear_band(d, xc, y, r, h=6, tooth=3):
    """A gear seen edge-on: a band the width of its pitch diameter, its teeth standing past it at both ends."""
    d.line((xc - r, y - h), (xc + r, y - h), (xc + r, y + h), (xc - r, y + h), closed=True)
    for sgn in (-1, 1):
        x = xc + sgn * r
        d.lines([[(x, y + k), (x + sgn * tooth, y + k + 1), (x, y + k + 2)] for k in range(-h, h - 1, 3)])


def antikythera():
    """The Metonic train in elevation: b2 64 → l1 38, l2 53 → m1 96, m2 15 → n1 53, which is 5/19; and the spiral dial it drives."""
    d = D()
    m = 1.1  # pitch radius = m × teeth / 2
    r = {k: m * t / 2 for k, t in {'b2': 64, 'l1': 38, 'l2': 53, 'm1': 96, 'm2': 15, 'n1': 53}.items()}
    xa = 34 + r['b2']
    xb = xa + r['b2'] + r['l1']
    xc = xb + r['l2'] + r['m1']
    xd = xc + r['m2'] + r['n1']
    ya, yb, yc = 96, 140, 184  # the three planes: b2/l1, l2/m1, m2/n1
    # construction: the arbors' centre lines, the three planes, and the meshing points projected down
    d.group('thin')
    d.lines([[(x, 70), (x, 214)] for x in (xa, xb, xc, xd)])
    d.lines([[(20, y), (292, y)] for y in (ya, yb, yc)])
    d.lines([[(xa + r['b2'], ya - 12), (xa + r['b2'], ya + 12)], [(xb + r['l2'], yb - 12), (xb + r['l2'], yb + 12)],
             [(xc + r['m2'], yc - 12), (xc + r['m2'], yc + 12)]])
    # the arbors
    d.group('mid')
    d.line((xa, ya - 14), (xa, ya + 12))
    d.line((xb, ya - 14), (xb, yb + 12))
    d.line((xc, yb - 12), (xc, yc + 12))
    d.line((xd, yc - 12), (xd, yc + 26))
    # the gears, each a band as wide as its pitch circle
    d.group()
    _gear_band(d, xa, ya, r['b2'])
    _gear_band(d, xb, ya, r['l1'])
    _gear_band(d, xb, yb, r['l2'])
    _gear_band(d, xc, yb, r['m1'])
    _gear_band(d, xc, yc, r['m2'])
    _gear_band(d, xd, yc, r['n1'])
    # the Metonic dial: a five-turn spiral with its pointer, on the back plate
    d.group('mid')
    cx, cy = 346, 140
    turns, r0, r1 = 5, 12, 44
    pts = []
    for i in range(turns * 72 + 1):
        a = 2 * math.pi * i / 72
        rr = r0 + (r1 - r0) * i / (turns * 72)
        pts.append((cx + rr * math.cos(a - math.pi / 2), cy + rr * math.sin(a - math.pi / 2)))
    d.line(*pts)
    d.group()
    a = math.radians(-35)
    d.line((cx, cy), (cx + 38 * math.cos(a), cy + 38 * math.sin(a)))
    d.circle(cx, cy, 2.5)
    # labels: tooth counts, the ratio, the dial
    d.group()
    d.text(xa - r['b2'] + 2, ya - 10, '64', size=8, anchor='start')
    d.text(xb, ya - 18, '38', size=8)
    d.text(xb - r['l2'] + 2, yb - 10, '53', size=8, anchor='start')
    d.text(xc + r['m1'] - 2, yb - 10, '96', size=8, anchor='end')
    d.text(xc - r['m2'] - 6, yc + 3, '15', size=8, anchor='end')
    d.text(xd + r['n1'] - 2, yc + 17, '53', size=8, anchor='end')
    d.text(xa, 64, 'b', size=7)
    d.text(xb, 64, 'l', size=7)
    d.text(xc, 124, 'm', size=7)
    d.text(xd, 225, 'n', size=7)
    d.text(160, 260, '64/38 × 53/96 × 15/53 = 5/19', size=9)
    d.text(160, 274, 'FIVE TURNS OF THE DIAL IN NINETEEN YEARS', size=7)
    d.text(cx, 204, 'METONIC SPIRAL', size=7)
    d.text(cx, 216, '235 MONTHS', size=7)
    return d


def logarithms():
    """A slide rule set to multiply 2 × 3: the C scale's 1 over D's 2, the cursor at C 3 reads D 6."""
    d = D()
    x0, L = 36, 250
    X = lambda v, s=0: x0 + s + L * math.log10(v)
    shift = L * math.log10(2)
    yd = 176  # the line where the slide's C scale meets the stock's D scale
    # construction: the log of each whole number carried up as a projection line
    d.group('thin')
    d.lines([[(X(v), 40), (X(v), yd + 44)] for v in (1, 2, 6)])
    d.lines([[(X(3, shift), 96), (X(3, shift), yd)]])
    d.line((x0 - 16, yd), (x0 + L + 16, yd))
    # the stock and the slide
    d.group()
    d.line((x0 - 14, 124), (x0 + L + 14, 124), (x0 + L + 14, 228), (x0 - 14, 228), closed=True)
    d.line((x0 + shift - 10, 142), (x0 + shift + L + 10, 142), (x0 + shift + L + 10, yd), (x0 + shift - 10, yd), closed=True)
    # the scales: D on the stock, reading down; C on the slide, reading up
    d.group('mid')
    ticks_d, ticks_c = [], []
    for k in range(100, 1001):
        v = k / 100
        if k % (5 if v < 2 else 10 if v < 5 else 20):
            continue
        major = k % 100 == 0
        half = k % 50 == 0
        ln = 11 if major else (8 if half else 4)
        ticks_d.append([(X(v), yd), (X(v), yd + ln)])
        ticks_c.append([(X(v, shift), yd), (X(v, shift), yd - ln)])
    d.lines(ticks_d)
    d.lines(ticks_c)
    # the cursor, its hairline over C 3 and D 6
    d.group()
    xc = X(6)
    d.line((xc - 12, 114), (xc + 12, 114), (xc + 12, 238), (xc - 12, 238), closed=True)
    d.line((xc, 114), (xc, 238))
    # the logs, added as lengths
    d.group('mid')
    _span(d, X(1), X(2), 64)
    _span(d, X(2), X(6), 82)
    _span(d, X(1), X(6), 100)
    # labels
    d.group()
    for v in range(1, 11):
        d.text(X(v), yd + 22, str(v) if v < 10 else '1', size=8)
        d.text(X(v, shift), yd - 16, str(v) if v < 10 else '1', size=7)
    d.text(x0 - 22, yd + 22, 'D', size=8, anchor='end')
    d.text(x0 + shift - 16, yd - 16, 'C', size=8, anchor='end')
    d.text((X(1) + X(2)) / 2, 58, 'LOG 2', size=7)
    d.text((X(2) + X(6)) / 2, 76, 'LOG 3', size=7)
    d.text((X(1) + X(6)) / 2, 94, 'LOG 6', size=7)
    d.text(200, 268, 'LOG 2 + LOG 3 = LOG 6 · MULTIPLYING BY ADDING LENGTHS', size=8)
    return d


PLATES = {'abacus': abacus, 'antikythera': antikythera, 'logarithms': logarithms}
