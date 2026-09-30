"""Plates for the mathematics subject's first segment, Counting (sprint 024)."""
import math
from plates import D


def ishango_bone():
    d = D()
    cols = [('G', [11, 13, 17, 19]), ('M', [3, 6, 4, 8, 10, 5, 5, 7]), ('D', [11, 21, 19, 9])]
    x0, step, gap = 52, 4.2, 2
    rows = [128, 188, 248]
    # the bone: a gently curved, tapering rod; its centre line bows up
    def centre(t):
        return 40 + 300 * t, 62 - 10 * math.sin(math.pi * t)
    def half(t):
        return 10 - 4 * t
    ts = [i / 60 for i in range(61)]
    d.group('thin')
    # projection lines from the bone's ends to the unrolled strips, and the strips' baselines
    d.line((40, 72), (40, 262))
    d.line((340, 66), (340, 262))
    for y in rows:
        d.line((40, y), (340, y))
    d.lines([[centre(t) for t in ts]])
    d.group()
    top = [(centre(t)[0], centre(t)[1] - half(t)) for t in ts]
    bot = [(centre(t)[0], centre(t)[1] + half(t)) for t in ts]
    d.line(*top, *reversed(bot), closed=True)
    d.group('mid')
    # the quartz chip at the left end
    d.line((40, 55), (24, 50), (18, 60), (26, 70), (40, 68))
    # notches on the bone itself, in its three bands
    segs = []
    for k in range(40):
        t = 0.08 + 0.86 * k / 39
        x, y = centre(t)
        h = half(t)
        segs.append([(x - 1.2, y - h + 1.5), (x + 1.2, y - h * 0.35)])
        if k % 2 == 0:
            segs.append([(x + 1, y + h * 0.35), (x - 1, y + h - 1.5)])
    d.lines(segs)
    d.group()
    # the three columns unrolled, one tick per notch
    labels = []
    for (name, groups), y in zip(cols, rows):
        x = x0
        segs = []
        for g in groups:
            start = x
            for i in range(g):
                segs.append([(x, y - 12), (x, y)])
                x += step
            labels.append((start + (x - step - start) / 2, y + 12, str(g)))
            x += gap * step
        d.lines(segs)
    d.group('mid')
    for (name, groups), y in zip(cols, rows):
        d.text(30, y - 2, name)
        d.text(366, y - 2, f'{sum(groups)}', anchor='start')
    for x, y, s in labels:
        d.text(x, y, s, size=7)
    d.text(366, 112, 'SUM', size=7, anchor='start')
    return d


def ybc_7289():
    d = D()
    cx, cy, r = 150, 140, 100
    x0, y0, side = 90, 80, 120            # the square, sides level as a scribe drew it
    diag = side * math.sqrt(2)
    d.group('thin')
    # the tablet's outline, the base line produced, and the compass swing of the diagonal
    d.circle(cx, cy, r)
    d.line((x0, y0 + side), (x0 + diag + 25, y0 + side))
    d.arc(x0, y0 + side, diag, -45, 0, n=60)
    d.line((x0 + side, y0 + side - 6), (x0 + side, y0 + side + 6))
    d.line((x0 + diag, y0 + side - 6), (x0 + diag, y0 + side + 6))
    d.group()
    d.line((x0, y0), (x0 + side, y0), (x0 + side, y0 + side), (x0, y0 + side), closed=True)
    d.lines([[(x0, y0), (x0 + side, y0 + side)], [(x0 + side, y0), (x0, y0 + side)]])
    d.group('mid')
    # the four sexagesimal places of the root, in boxes
    bx, by, bw, bh = 250, 60, 34, 22
    for i in range(4):
        d.line((bx + i * bw, by), (bx + (i + 1) * bw, by), (bx + (i + 1) * bw, by + bh), (bx + i * bw, by + bh), closed=True)
    d.group('mid')
    for i, (dig, pl) in enumerate(zip(['1', '24', '51', '10'], ['1', '1/60', '/3600', '/216000'])):
        d.text(bx + i * bw + bw / 2, by + 15, dig)
        d.text(bx + i * bw + bw / 2, by + bh + 12, pl, size=6)
    d.text(x0 + side / 2, y0 - 8, '30')
    d.text(x0 + side / 2, y0 + side / 2 - 22, '1 24 51 10')
    d.text(x0 + side / 2, y0 + side / 2 + 30, '42 25 35')
    d.text(x0 + side, y0 + side + 18, '1')
    d.text(x0 + diag, y0 + side + 18, '1.414213')
    d.text(bx + 2 * bw, by - 10, 'THE DIAGONAL', size=7)
    return d


def rhind_papyrus():
    d = D()
    c, x0, y0 = 21, 40, 55                 # a nine-by-nine grid of khet
    cx, cy, r = x0 + 4.5 * c, y0 + 4.5 * c, 4.5 * c
    d.group('thin')
    d.lines([[(x0 + i * c, y0), (x0 + i * c, y0 + 9 * c)] for i in range(10)] +
            [[(x0, y0 + i * c), (x0 + 9 * c, y0 + i * c)] for i in range(10)])
    # problem 56: a pyramid's section, half the base against the height
    px, py, k = 300, 230, 0.3
    d.line((px - 180 * k - 10, py), (px + 180 * k + 10, py))
    d.line((px, py), (px, py - 250 * k - 8))
    d.group()
    d.circle(cx, cy, r)
    d.line((px - 180 * k, py), (px, py - 250 * k), (px + 180 * k, py))
    d.group('mid')
    s8 = 8 * c
    d.line((cx - s8 / 2, cy - s8 / 2), (cx + s8 / 2, cy - s8 / 2), (cx + s8 / 2, cy + s8 / 2),
           (cx - s8 / 2, cy + s8 / 2), closed=True)
    # the seked: the run of the face (half the base) set out against its rise
    d.line((px, py + 6), (px + 180 * k, py + 6))
    d.line((px + 180 * k, py + 3), (px + 180 * k, py + 9))
    d.group('mid')
    d.text(cx, y0 - 8, '9')
    d.text(cx, cy + s8 / 2 - 6, '8')
    d.text(cx, cy + 4, '64')
    d.text(px + 180 * k / 2, py + 18, '180')
    d.text(px - 20, py - 250 * k / 2 + 3, '250')
    d.text(px, py - 250 * k - 16, 'SEKED', size=7)
    d.text(px, 262, '5 1/25 PALMS', size=7)
    d.text(cx, 272, 'PROBLEM 50', size=7)
    d.text(px, 272, 'PROBLEM 56', size=7)
    return d


PLATES = {
    'ishango-bone': ishango_bone,
    'ybc-7289': ybc_7289,
    'rhind-papyrus': rhind_papyrus,
}
