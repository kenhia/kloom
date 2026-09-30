"""physics plates, the trail "Heat and information", part "information" (sprint 021). See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _h(p):
    """The entropy of a two-way choice, in bits."""
    if p <= 0 or p >= 1:
        return 0.0
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def shannon_entropy():
    """Shannon's figure 7: the entropy of a choice between two possibilities, H(p), in bits.

    The curve is computed. It peaks at one bit when the two are equally
    likely, and falls to 0.081 bits at p = 0.99, the figure in Shannon's own
    example of a channel that gets one symbol in a hundred wrong."""
    d = D()
    x0, y0, w, h = 70, 250, 280, 200        # the axes' origin and size: p from 0 to 1, H from 0 to 1 bit
    X = lambda p: x0 + w * p
    Y = lambda v: y0 - h * v
    # construction: a grid in tenths
    d.group('thin')
    d.lines([[(X(i / 10), y0), (X(i / 10), Y(1))] for i in range(1, 11)])
    d.lines([[(x0, Y(i / 10)), (X(1), Y(i / 10))] for i in range(1, 11)])
    # the axes
    d.group()
    d.line((x0, Y(1.08)), (x0, y0), (X(1.05), y0))
    _arrow(d, x0, Y(1.08), -math.pi / 2, 4)
    _arrow(d, X(1.05), y0, 0, 4)
    # the curve
    d.group()
    d.line(*[(X(i / 200), Y(_h(i / 200))) for i in range(201)])
    # details: the peak, and Shannon's noisy channel at p = 0.99
    d.group('mid')
    d.line((X(0.5), y0), (X(0.5), Y(1)))
    d.circle(X(0.5), Y(1), 3)
    p = 0.99
    d.line((X(p), y0), (X(p), Y(_h(p))), (X(0.78), Y(_h(p))))
    d.circle(X(p), Y(_h(p)), 2.5)
    d.circle(X(0.11), Y(_h(0.11)), 2.5)
    d.line((X(0.11), Y(_h(0.11))), (X(0.11), y0))
    # labels
    d.group()
    d.text(x0 - 8, Y(1) + 3, '1', size=8, anchor='end')
    d.text(x0 - 8, Y(0.5) + 3, '½', size=8, anchor='end')
    d.text(x0 - 8, y0 + 3, '0', size=8, anchor='end')
    d.text(X(0.5), y0 + 14, '½', size=8)
    d.text(X(1), y0 + 14, '1', size=8)
    d.text(X(0.11), y0 + 14, '0.11', size=7)
    d.text(x0 - 6, Y(1.08) - 6, 'H · BITS', size=7, anchor='start')
    d.text(X(1.05) + 4, y0 + 3, 'p', size=9, anchor='start')
    d.text(X(0.5), Y(1) - 10, 'ONE BIT', size=7)
    d.text(X(0.77), Y(_h(p)) + 3, '0.081 AT p = 0.99', size=7, anchor='end')
    d.text(X(0.11) + 6, Y(_h(0.11)) + 16, '½ BIT', size=7, anchor='start')
    d.text(200, 290, 'H = −p log₂ p − (1 − p) log₂ (1 − p)', size=8)
    return d


def landauer():
    """Landauer's bistable well (his figure 1) and the erasure the Lyon experiment ran on it.

    Above, the well that holds one bit, the particle in either minimum. Below,
    four steps of RESTORE TO ZERO, as Bérut and colleagues did it with a bead
    in an optical trap: lower the barrier, tilt the well, raise the barrier.
    The bead ends in 0 whichever side it started, and the bit is gone."""
    d = D()

    def well(cx, cy, sx, sy, barrier=1.0, tilt=0.0, n=80):
        # U(x) = x⁴ − 2·barrier·x² + tilt·x, on x in [−1.6, 1.6]
        pts = []
        for i in range(n + 1):
            x = -1.6 + 3.2 * i / n
            u = x ** 4 - 2 * barrier * x * x + tilt * x
            pts.append((cx + sx * x, cy - sy * u))
        return pts

    def u_at(x, barrier=1.0, tilt=0.0):
        return x ** 4 - 2 * barrier * x * x + tilt * x

    # construction: the axes of the large well, and the baseline under the steps
    d.group('thin')
    cx, cy, sx, sy = 200, 130, 70, 22
    d.line((cx, cy - sy * 3.3), (cx, cy + sy * 1.4))
    d.line((cx - sx * 1.75, cy + sy * 1.2), (cx + sx * 1.75, cy + sy * 1.2))
    d.lines([[(cx - sx, cy + sy * 1.2 - 3), (cx - sx, cy + sy * 1.2 + 3)],
             [(cx + sx, cy + sy * 1.2 - 3), (cx + sx, cy + sy * 1.2 + 3)]])
    steps = [(1.0, 0.0), (0.18, 0.0), (0.18, 1.6), (1.0, 0.0)]
    bx = [62, 154, 246, 338]
    by, bsx, bsy = 262, 26, 6
    d.line((30, by + 14), (370, by + 14))
    # the large well
    d.group()
    d.line(*[p for p in well(cx, cy, sx, sy) if p[1] > cy - sy * 3.1])
    # the steps of the erasure
    d.group()
    for (b, t), x in zip(steps, bx):
        pts = [p for p in well(x, by, bsx, bsy, b, t) if p[1] > by - 30]
        d.line(*pts)
    d.group('mid')
    # the particle: in either well above; where it may be at each step below
    for s in (-1, 1):
        d.circle(cx + sx * s, cy - sy * u_at(s) - 6, 5)
    for (b, t), x, where in zip(steps, bx, [(-1, 1), (0,), (-0.95,), (-1,)]):
        for xm in where:
            xm2 = xm if b > 0.5 else xm
            d.circle(x + bsx * xm2, by - bsy * u_at(xm2, b, t) - 3.5, 3)
    for x0, x1 in zip(bx, bx[1:]):
        d.line((x0 + 36, by - 38), (x1 - 36, by - 38))
        _arrow(d, x1 - 36, by - 38, 0, 3.5)
    # labels
    d.group()
    d.text(cx - sx, cy + sy * 1.2 + 14, '0', size=9)
    d.text(cx + sx, cy + sy * 1.2 + 14, '1', size=9)
    d.text(cx + 6, cy - sy * 3.3 + 4, 'V', size=8, anchor='start')
    d.text(cx + sx * 1.75 + 4, cy + sy * 1.2 + 3, 'x', size=8, anchor='start')
    d.text(200, 24, 'ONE BIT: A PARTICLE IN A DOUBLE WELL', size=8)
    for x, s in zip(bx, ['EITHER', 'LOWER', 'TILT', 'RAISE: 0']):
        d.text(x, by + 28, s, size=7)
    d.text(200, 200, 'RESTORE TO ZERO · HEAT ≥ kT ln 2', size=8)
    return d


def reversible_computing():
    """Bennett's reversible Turing machine of 1973: three tapes at four moments.

    Compute, saving a history of every step; copy the answer to a blank
    output tape; then retrace the steps backwards, erasing the history and
    the working, until only the input and the answer are left."""
    d = D()
    cell, n = 12, 5
    left = 70
    colw = n * cell
    gap = (392 - left - 4 * colw) / 3
    cols = [left + i * (colw + gap) for i in range(4)]
    rows = [100, 145, 190]           # WORK, HISTORY, OUTPUT
    # what each tape holds at each moment: 'i' input, 'g' working or history, 'o' answer, '' blank
    state = [
        [['i', 'i', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']],
        [['i', 'i', 'g', 'o', 'o'], ['g', 'g', 'g', 'g', 'g'], ['', '', '', '', '']],
        [['i', 'i', 'g', 'o', 'o'], ['g', 'g', 'g', 'g', 'g'], ['o', 'o', '', '', '']],
        [['i', 'i', '', '', ''], ['', '', '', '', ''], ['o', 'o', '', '', '']],
    ]
    # construction: a time line under the moments, and verticals through each column's centre
    d.group('thin')
    d.line((cols[0], 238), (cols[3] + colw, 238))
    d.lines([[(c + colw / 2, 70), (c + colw / 2, 244)] for c in cols])
    # the tapes
    d.group()
    for c in cols:
        for y in rows:
            d.line((c, y), (c + colw, y), (c + colw, y + cell), (c, y + cell), closed=True)
            d.lines([[(c + k * cell, y), (c + k * cell, y + cell)] for k in range(1, n)])
    # what the cells hold
    d.group('mid')
    for c, tapes in zip(cols, state):
        for y, tape in zip(rows, tapes):
            for k, s in enumerate(tape):
                x = c + k * cell + cell / 2
                yc = y + cell / 2
                if s == 'i':
                    d.circle(x, yc, 3)
                elif s == 'o':
                    d.line((x - 3, yc - 3), (x + 3, yc - 3), (x + 3, yc + 3), (x - 3, yc + 3), closed=True)
                elif s == 'g':
                    d.lines([[(x - 3.5, yc + 3.5), (x + 3.5, yc - 3.5)], [(x - 3.5, yc - 0.5), (x - 0.5, yc - 3.5)],
                             [(x + 0.5, yc + 3.5), (x + 3.5, yc + 0.5)]])
    # a key to the cells
    d.circle(120, 284, 3)
    d.line((197, 281), (203, 281), (203, 287), (197, 287), closed=True)
    d.lines([[(276.5, 287.5), (283.5, 280.5)], [(276.5, 283.5), (279.5, 280.5)], [(280.5, 287.5), (283.5, 284.5)]])
    # the three stages between the moments
    for a, b in zip(cols, cols[1:]):
        x0, x1 = a + colw + 5, b - 5
        d.line((x0, 60), (x1, 60))
        _arrow(d, x1, 60, 0, 3.5)
    # labels
    d.group()
    for y, s in zip(rows, ['WORK', 'HISTORY', 'OUTPUT']):
        d.text(left - 8, y + 9, s, size=7, anchor='end')
    for a, b, s in zip(cols, cols[1:], ['COMPUTE', 'COPY', 'RETRACE']):
        d.text((a + colw + b) / 2, 52, s, size=7)
    for c, s in zip(cols, ['START', '', '', 'END']):
        if s:
            d.text(c + colw / 2, 256, s, size=7)
    d.text(200, 22, 'BENNETT 1973 · A REVERSIBLE TURING MACHINE', size=8)
    for x, s in [(120, 'INPUT'), (200, 'ANSWER'), (280, 'WORKING')]:
        d.text(x + 8, 287, s, size=7, anchor='start')
    return d


PLATES = {
    'shannon-entropy': shannon_entropy,
    'landauer': landauer,
    'reversible-computing': reversible_computing,
}
