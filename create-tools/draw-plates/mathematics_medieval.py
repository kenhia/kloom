"""Plates for the mathematics subject's Beyond Greece segment, part `medieval` (sprint 024):
Brahmagupta's zero, al-Khwarizmi's square, Fibonacci's sequence and Madhava's series."""
import math
from plates import D


def brahmagupta_zero():
    """Fortunes and debts on a line, with zero at its centre; above, the Gwalior 270 in its places."""
    d = D()
    y0, u, x0 = 190, 26, 200            # the line, its unit, and zero
    X = lambda k: x0 + u * k
    d.group('thin')
    # the line's ticks produced up and down, and the three place columns above
    d.lines([[(X(k), y0 - 5), (X(k), y0 + 5)] for k in range(-6, 7) if k])
    d.lines([[(X(k), y0 - 60), (X(k), y0 + 60)] for k in (-5, -4, -2, 3, 4)])
    bx, by, bw, bh = 146, 34, 36, 30
    d.line((bx, by + bh + 12), (bx + 3 * bw, by + bh + 12))
    d.group()
    d.line((X(-6.6), y0), (X(6.6), y0))
    d.circle(x0, y0, 6)                  # zero, written as a small circle, as at Gwalior
    for i in range(3):
        d.line((bx + i * bw, by), (bx + (i + 1) * bw, by), (bx + (i + 1) * bw, by + bh), (bx + i * bw, by + bh), closed=True)
    d.group('mid')
    # a fortune of 3 and a debt of 5: forward three, back five, a debt of 2
    d.arc((X(0) + X(3)) / 2, y0, (X(3) - X(0)) / 2, 180, 360, n=40)
    d.arc((X(3) + X(-2)) / 2, y0, (X(3) - X(-2)) / 2, 0, -180, n=60)
    # a debt of 4 taken from zero becomes a fortune of 4: reflected through zero, below the line
    d.arc(x0, y0, 4 * u, 180, 0, n=80, ry=2.2 * u)
    d.group('mid')
    for k in (-6, -4, -2, 2, 4, 6):
        d.text(X(k), y0 + 17, f'{abs(k)}', size=7)
    d.text(X(-2), y0 - 40, '−2', size=8)
    d.text(X(4), y0 + 72, '4', size=8)
    d.text(X(-4.2), y0 + 72, '−4', size=8)
    d.text(X(-4.6), y0 - 12, 'DEBT', size=7)
    d.text(X(4.9), y0 - 12, 'FORTUNE', size=7)
    d.text(x0, y0 - 88, '3 + (−5) = −2', size=8)
    d.text(x0, 290, '0 − (−4) = 4', size=8)
    for i, (dig, pl) in enumerate(zip(['2', '7', '0'], ['100', '10', '1'])):
        d.text(bx + i * bw + bw / 2, by + 20, dig, size=11)
        d.text(bx + i * bw + bw / 2, by + bh + 24, pl, size=7)
    d.text(bx + 3 * bw + 16, by + 20, 'HASTAS', size=7, anchor='start')
    return d


def al_khwarizmi():
    """His two figures for x² + 10x = 39: a square, the ten roots laid round it, the corners that complete it."""
    d = D()
    s = 19                               # one unit
    # figure 1: the square x·x with four strips 2½ wide, and four corners of 2½·2½
    ax, ay = 24, 58
    big = 8 * s
    q = 2.5 * s
    # figure 2: the square with two strips 5 wide, and one corner of 5·5
    bx, by = 222, 58
    d.group('thin')
    d.line((ax, ay), (ax + big, ay), (ax + big, ay + big), (ax, ay + big), closed=True)
    d.line((bx, by), (bx + big, by), (bx + big, by + big), (bx, by + big), closed=True)
    d.lines([[(ax + q, ay - 8), (ax + q, ay + big + 8)], [(ax + big - q, ay - 8), (ax + big - q, ay + big + 8)],
             [(ax - 8, ay + q), (ax + big + 8, ay + q)], [(ax - 8, ay + big - q), (ax + big + 8, ay + big - q)]])
    d.lines([[(bx + 3 * s, by - 8), (bx + 3 * s, by + big + 8)], [(bx - 8, by + 3 * s), (bx + big + 8, by + 3 * s)]])
    d.group()
    # the unknown square and the roots
    d.line((ax + q, ay + q), (ax + big - q, ay + q), (ax + big - q, ay + big - q), (ax + q, ay + big - q), closed=True)
    d.line((ax + q, ay), (ax + big - q, ay), (ax + big - q, ay + q))
    d.line((ax + big, ay + q), (ax + big, ay + big - q), (ax + big - q, ay + big - q))
    d.line((ax + big - q, ay + big), (ax + q, ay + big), (ax + q, ay + big - q))
    d.line((ax, ay + big - q), (ax, ay + q), (ax + q, ay + q))
    d.line((bx, by), (bx + 3 * s, by), (bx + 3 * s, by + 3 * s), (bx, by + 3 * s), closed=True)
    d.line((bx + 3 * s, by), (bx + big, by), (bx + big, by + 3 * s), (bx + 3 * s, by + 3 * s))
    d.line((bx, by + 3 * s), (bx, by + big), (bx + 3 * s, by + big), (bx + 3 * s, by + 3 * s))
    d.group('mid')
    # the corners that complete the square, hatched
    def hatch(x, y, w, h, step=5):
        segs = []
        for k in range(1, int((w + h) / step)):
            t = k * step
            p0 = (x + min(t, w), y + max(0, t - w))
            p1 = (x + max(0, t - h), y + min(t, h))
            segs.append([p0, p1])
        d.lines(segs)
    for cx, cy in ((ax, ay), (ax + big - q, ay), (ax, ay + big - q), (ax + big - q, ay + big - q)):
        hatch(cx, cy, q, q)
    hatch(bx + 3 * s, by + 3 * s, 5 * s, 5 * s, step=6)
    d.group('mid')
    d.text(ax + big / 2, ay + big / 2 + 3, 'x²')
    d.text(ax + big / 2, ay + q / 2 + 3, '2½x', size=7)
    d.text(ax + big / 2, ay + big - q / 2 + 3, '2½x', size=7)
    d.text(bx + 1.5 * s, by + 1.5 * s + 3, 'x²')
    d.text(bx + 5.5 * s, by + 1.5 * s + 3, '5x', size=8)
    d.text(bx + 1.5 * s, by + 5.5 * s + 3, '5x', size=8)
    d.text(bx + 5.5 * s, by + 5.5 * s + 3, '25', size=8)
    d.text(ax + big / 2, ay - 16, '8', size=8)
    d.text(bx + big / 2, by - 16, '8', size=8)
    d.text(ax + big / 2, 262, '39 + 4 × 6¼ = 64', size=8)
    d.text(bx + big / 2, 262, '39 + 25 = 64', size=8)
    d.text(200, 284, 'x = 8 − 5 = 3', size=8)
    return d


def fibonacci():
    """Squares on the sequence's numbers tile a rectangle; below, the ratios closing on the golden ratio."""
    d = D()
    F = [1, 1, 2, 3, 5, 8, 13, 21]
    u = 7.2
    ox, oy = 200 - 34 * u / 2, 18
    # place the squares spiralling outwards: right, down, left, up
    x0, y0, x1, y1 = 0, 0, 1, 1            # bounding box in units, after the first square
    squares = [(0, 0, 1)]
    dirs = ['right', 'down', 'left', 'up']
    for i, f in enumerate(F[1:]):
        dr = dirs[i % 4]
        if dr == 'right':
            sq = (x1, y0, f); x1 += f
        elif dr == 'down':
            sq = (x0, y1, f); y1 += f
        elif dr == 'left':
            sq = (x0 - f, y0, f); x0 -= f
        else:
            sq = (x0, y0 - f, f); y0 -= f
        squares.append(sq)
    P = lambda x, y: (ox + (x - x0) * u, oy + (y - y0) * u)
    d.group('thin')
    # the ratio plot's frame and the golden ratio's line
    px0, px1, py = 60, 340, 240
    phi = (1 + 5 ** 0.5) / 2
    Y = lambda r: py - (r - phi) * 60
    d.line((px0, Y(phi)), (px1, Y(phi)))
    d.line((px0, Y(1)), (px0, Y(2.05)))
    d.lines([[(px0 - 4, Y(v)), (px0, Y(v))] for v in (1, 1.5, 2)])
    d.group()
    for x, y, f in squares:
        a, b = P(x, y), P(x + f, y + f)
        d.line(a, (b[0], a[1]), b, (a[0], b[1]), closed=True)
    d.group('mid')
    # the quarter arcs through each square, corner to corner
    corners = {'right': (0, 1, 270, 360), 'down': (0, 0, 0, 90), 'left': (1, 0, 90, 180), 'up': (1, 1, 180, 270)}
    for i, (x, y, f) in enumerate(squares):
        dr = dirs[(i - 1) % 4] if i else 'up'
        cxu, cyu, a0, a1 = corners[dr]
        cx, cy = P(x + cxu * f, y + cyu * f)
        d.arc(cx, cy, f * u, a0, a1, n=max(8, 4 * f))
    ratios = [F[i + 1] / F[i] for i in range(len(F) - 1)] + [34 / 21, 55 / 34, 89 / 55]
    pts = [(px0 + 20 + i * (px1 - px0 - 30) / (len(ratios) - 1), Y(r)) for i, r in enumerate(ratios)]
    d.line(*pts)
    d.group('mid')
    for x, y, f in squares:
        if f >= 3:
            c = P(x + f / 2, y + f / 2)
            d.text(c[0], c[1] + 3, str(f), size=8 if f < 13 else 9)
    d.text(px1 + 4, Y(phi) + 3, 'φ', anchor='start')
    d.text(px0 - 7, Y(1) + 3, '1', size=7, anchor='end')
    d.text(px0 - 7, Y(2) + 3, '2', size=7, anchor='end')
    d.text(pts[-1][0], Y(phi) + 16, '89/55', size=7)
    d.text(pts[0][0] + 6, Y(1) + 3, '1/1', size=7, anchor='start')
    return d


def madhava():
    """π/4 = 1 − 1/3 + 1/5 − …: the partial sums swinging about π, and the corrected sums on it."""
    d = D()
    N = 14
    x0, x1 = 44, 368
    X = lambda n: x0 + (n - 1) * (x1 - x0) / (N - 1)
    top, bot = 26, 262
    lo, hi = 2.6, 4.05
    Y = lambda v: bot - (v - lo) * (bot - top) / (hi - lo)
    sums, fixed = [], []
    s = 0
    for n in range(1, N + 1):
        s += 4 * (-1) ** (n - 1) / (2 * n - 1)
        sums.append(s)
        fixed.append(s + (-1) ** n * 4 * n / (4 * n * n + 1))
    d.group('thin')
    d.line((x0 - 10, Y(math.pi)), (x1 + 10, Y(math.pi)))
    d.lines([[(X(n), bot + 4), (X(n), Y(sums[n - 1]))] for n in range(1, N + 1)])
    d.line((x0 - 10, bot + 4), (x1 + 10, bot + 4))
    # the envelope the swings shrink inside: π ± 4/(2n)
    d.line(*[(X(n), Y(math.pi + 2 / n)) for n in range(3, N + 1)])
    d.line(*[(X(n), Y(math.pi - 2 / n)) for n in range(4, N + 1)])
    d.group()
    d.line(*[(X(n), Y(v)) for n, v in enumerate(sums, 1)])
    d.group('mid')
    for n, v in enumerate(fixed, 1):
        d.circle(X(n), Y(v), 2.6)
    d.group('mid')
    d.text(x1 + 14, Y(math.pi) + 3, 'π', size=10, anchor='start')
    for n in (1, 2, 3, 4, 7, 10, 14):
        d.text(X(n), bot + 16, str(n), size=7)
    d.text(X(1) + 8, Y(4) + 3, '4', size=7, anchor='start')
    d.text(X(2) + 8, Y(sums[1]) + 3, '2.67', size=7, anchor='start')
    d.text(X(3) + 8, Y(sums[2]) + 3, '3.47', size=7, anchor='start')
    d.text((x0 + x1) / 2, bot + 32, 'TERMS', size=7)
    return d


PLATES = {
    'brahmagupta-zero': brahmagupta_zero,
    'al-khwarizmi': al_khwarizmi,
    'fibonacci': fibonacci,
    'madhava': madhava,
}
