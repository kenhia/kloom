"""Plates for the mathematics subject's Infinity trail (sprint 024)."""
import math
from plates import D


def zeno():
    d = D()
    x0, x1, y = 40, 360, 118              # the course, 0 to 1
    L = x1 - x0
    runs = 12
    marks = [1 - 0.5 ** k for k in range(0, runs + 1)]   # 0, 1/2, 3/4, ...
    # the rectangle below, halved again and again: a half, then a quarter, ...
    rx, ry, rw, rh = 40, 160, 320, 116
    d.group('thin')
    d.line((x0 - 10, y), (x1 + 10, y))
    # projection lines from the first cuts of the course to the rectangle's top
    d.lines([[(x0 + L * m, y + 6), (x0 + L * m, ry - 4)] for m in marks[1:5]] +
            [[(x0, y + 6), (x0, ry - 4)], [(x1, y + 6), (x1, ry - 4)]])
    d.group()
    # the runs: an arc over each stage, each half the one before
    for a, b in zip(marks, marks[1:]):
        xa, xb = x0 + L * a, x0 + L * b
        r = (xb - xa) / 2
        if r < 0.4:
            break
        d.arc((xa + xb) / 2, y, r, 180, 360, n=max(8, int(r)))
    d.line((rx, ry), (rx + rw, ry), (rx + rw, ry + rh), (rx, ry + rh), closed=True)
    d.group('mid')
    # ticks at each stage of the course
    d.lines([[(x0 + L * m, y - 4), (x0 + L * m, y + 4)] for m in marks[:9]] +
            [[(x1, y - 6), (x1, y + 6)]])
    # the rectangle's cuts: alternately vertical and horizontal, each taking half of what is left
    cx, cy, cw, ch = rx, ry, rw, rh
    cuts, pieces = [], []
    for k in range(9):
        if k % 2 == 0:
            cuts.append([(cx + cw / 2, cy), (cx + cw / 2, cy + ch)])
            pieces.append((cx + cw / 4, cy + ch / 2))
            cx, cw = cx + cw / 2, cw / 2
        else:
            cuts.append([(cx, cy + ch / 2), (cx + cw, cy + ch / 2)])
            pieces.append((cx + cw / 2, cy + ch / 4))
            cy, ch = cy + ch / 2, ch / 2
    d.lines(cuts)
    d.group('mid')
    for (px, py), s, size in zip(pieces, ['1/2', '1/4', '1/8', '1/16'], [9, 8, 7, 6]):
        d.text(px, py + 3, s, size=size)
    for m, s in zip(marks[:4], ['0', '1/2', '3/4', '7/8']):
        d.text(x0 + L * m, y + 18, s, size=7)
    d.text(x1, y + 18, '1', size=7)
    d.text(200, 26, '1/2 + 1/4 + 1/8 + ... = 1', size=8)
    return d


def galileos_paradox():
    d = D()
    n = 10
    tx0, tstep, ty = 52, 33, 64            # the numbers, evenly spaced
    bx0, bx1, by = 40, 360, 222            # a number line from 0 to 100
    u = (bx1 - bx0) / 100
    top = [(tx0 + (k - 1) * tstep, ty) for k in range(1, n + 1)]
    bot = [(bx0 + k * k * u, by) for k in range(1, n + 1)]
    d.group('thin')
    d.line((tx0 - 20, ty), (top[-1][0] + 20, ty))
    # every whole number on the line below, the squares among them marked later
    d.lines([[(bx0 + i * u, by - 2), (bx0 + i * u, by + 2)] for i in range(0, 101)])
    d.group()
    d.line((bx0, by), (bx1, by))
    # the pairing: each number to its own square
    for (x, y), (X, Y) in zip(top, bot):
        d.line((x, y + 5), (X, Y - 5))
    d.group('mid')
    for x, y in top:
        d.circle(x, y, 3)
    d.lines([[(X, by - 7), (X, by + 7)] for X, _ in bot])
    # the share of squares thinning out: 10 in 100 below the line
    d.lines([[(bx0, by + 24), (bx1, by + 24)], [(bx0, by + 20), (bx0, by + 28)], [(bx1, by + 20), (bx1, by + 28)]])
    d.group('mid')
    for k, (x, y) in enumerate(top, start=1):
        d.text(x, y - 10, str(k), size=8)
    for k, (X, Y) in enumerate(bot, start=1):
        if k >= 3:
            d.text(X, Y + 17, str(k * k), size=7)
    d.text(bx0, by + 17, '1', size=6)
    d.text(bx0 + 4 * u + 3, by + 17, '4', size=6)
    d.text(200, by + 44, '10 SQUARES IN 100', size=7)
    d.text(24, ty + 3, 'n', size=8)
    d.text(24, by + 3, 'n²', size=8)
    return d


def _scatter(seed, n):
    """Deterministic points, uniform in the unit disc."""
    pts, s = [], seed
    while len(pts) < n:
        s = (s * 1103515245 + 12345) % 2147483648
        a = s / 2147483648
        s = (s * 1103515245 + 12345) % 2147483648
        b = s / 2147483648
        pts.append((math.sqrt(a), 2 * math.pi * b))
    return pts


def _marks(d, cx, cy, r, sectors, pts_per=26):
    """Five kinds of mark, one for each piece, scattered through the sectors named."""
    for piece, (a0, a1) in sectors:
        segs = []
        for k, (rho, _t) in enumerate(_scatter(17 + piece * 31, pts_per)):
            t = math.radians(a0 + (a1 - a0) * ((k * 0.618) % 1))
            x, y = cx + 0.92 * r * rho * math.cos(t), cy + 0.92 * r * rho * math.sin(t)
            s = 1.6
            if piece == 0:
                segs.append([(x - s, y), (x + s, y)])
            elif piece == 1:
                segs.append([(x, y - s), (x, y + s)])
            elif piece == 2:
                segs.append([(x - s, y - s), (x + s, y + s)])
            elif piece == 3:
                segs.append([(x - s, y + s), (x + s, y - s)])
            else:
                segs.append([(x - s, y), (x, y - s), (x + s, y), (x, y + s), (x - s, y)])
        d.lines(segs)


def _ball(d, cx, cy, r):
    d.circle(cx, cy, r)


def _wire(d, cx, cy, r):
    d.ellipse(cx, cy, r, r * 0.28)
    d.ellipse(cx, cy, r * 0.45, r)
    d.line((cx - r - 6, cy), (cx + r + 6, cy))


def banach_tarski():
    d = D()
    L = (100, 150, 66)                     # the ball
    A, B = (300, 82, 50), (300, 218, 50)   # the two balls it becomes
    five = [(i, (90 + 72 * i, 90 + 72 * (i + 1))) for i in range(5)]
    d.group('thin')
    for cx, cy, r in (L, A, B):
        _wire(d, cx, cy, r)
    # the ball's five sectors, a schematic of the pieces
    cx, cy, r = L
    d.lines([[(cx, cy), (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))]
             for _, (a, _b) in five])
    d.group()
    for cx, cy, r in (L, A, B):
        _ball(d, cx, cy, r)
    d.group('mid')
    _marks(d, *L, five)
    # pieces 1 and 2, turned, fill one ball; pieces 3, 4 and 5 the other
    _marks(d, *A, [(0, (0, 180)), (1, (180, 360))], pts_per=40)
    _marks(d, *B, [(2, (0, 120)), (3, (120, 240)), (4, (240, 360))], pts_per=34)
    d.group('mid')
    # the moves: arcs with arrowheads, and a turn about each new centre
    for (ex, ey), bend in (((246, 92), -1), ((246, 208), 1)):
        sx, sy = 172, 150 + bend * 22
        mx, my = (sx + ex) / 2, (sy + ey) / 2 + bend * -18
        pts = [((1 - t) ** 2 * sx + 2 * (1 - t) * t * mx + t * t * ex,
                (1 - t) ** 2 * sy + 2 * (1 - t) * t * my + t * t * ey) for t in [i / 20 for i in range(21)]]
        d.line(*pts)
        (px, py), (qx, qy) = pts[-2], pts[-1]
        a = math.atan2(qy - py, qx - px)
        d.line((qx - 7 * math.cos(a - 0.4), qy - 7 * math.sin(a - 0.4)), (qx, qy),
               (qx - 7 * math.cos(a + 0.4), qy - 7 * math.sin(a + 0.4)))
    for cx, cy, r in (A, B):
        d.arc(cx, cy, r + 9, -60, 20, n=24)
    d.group('mid')
    d.text(L[0], L[1] + L[2] + 20, 'ONE BALL · FIVE PIECES', size=7)
    d.text(A[0] + 58, A[1] - 44, 'A', size=8)
    d.text(B[0] + 58, B[1] + 50, 'B', size=8)
    d.text(L[0], 40, 'SCHEMATIC', size=6)
    return d


def continuum_hypothesis():
    d = D()
    x0, x1, y0, dy, depth = 40, 360, 34, 36, 5
    W = x1 - x0
    path = [1, 0, 1, 1, 0]                 # the set {1, 3, 4}, as binary digits

    def node(k, i):
        return x0 + (i + 0.5) * W / 2 ** k, y0 + k * dy

    ly = y0 + depth * dy + 34              # the line [0, 1]
    d.group('thin')
    # the tree's leaves dropped to their intervals, and the dyadic ticks of the line
    d.lines([[node(depth, i), (node(depth, i)[0], ly - 6)] for i in range(2 ** depth)])
    d.lines([[(x0 + j * W / 32, ly - 3), (x0 + j * W / 32, ly + 3)] for j in range(33)])
    d.group('mid')
    edges = []
    for k in range(depth):
        for i in range(2 ** k):
            p = node(k, i)
            edges.append([p, node(k + 1, 2 * i)])
            edges.append([p, node(k + 1, 2 * i + 1)])
    d.lines(edges)
    d.group()
    d.line((x0, ly), (x1, ly))
    pts, i = [node(0, 0)], 0
    for k, bit in enumerate(path, start=1):
        i = 2 * i + bit
        pts.append(node(k, i))
    target = x0 + W * 11 / 16
    pts.append((target, ly))
    d.line(*pts)
    d.group('mid')
    d.lines([[(target, ly - 8), (target, ly + 8)], [(x0, ly - 8), (x0, ly + 8)], [(x1, ly - 8), (x1, ly + 8)],
             [(x0 + W / 2, ly - 6), (x0 + W / 2, ly + 6)]])
    for k in range(depth + 1):
        x, y = pts[k]
        d.circle(x, y, 2.2)
    d.group('mid')
    for k, bit in enumerate(path):
        (xa, ya), (xb, yb) = pts[k], pts[k + 1]
        d.text((xa + xb) / 2 + (-9 if bit == 0 else 9), (ya + yb) / 2 + 2, str(bit), size=7)
    d.text(x0, ly + 16, '0', size=7)
    d.text(x0 + W / 2, ly + 16, '1/2', size=7)
    d.text(x1, ly + 16, '1', size=7)
    d.text(target, ly + 16, '11/16', size=7)
    d.text(x0 + 12, y0 + 3, '{1, 3, 4}', size=7, anchor='start')
    return d


PLATES = {
    'zeno': zeno,
    'galileos-paradox': galileos_paradox,
    'banach-tarski': banach_tarski,
    'continuum-hypothesis': continuum_hypothesis,
}
