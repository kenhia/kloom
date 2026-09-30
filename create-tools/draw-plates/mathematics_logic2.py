"""Plates for the mathematics subject's Logic and foundations segment, part two (sprint 024):
Hilbert's problems, Gödel's incompleteness theorems and the Entscheidungsproblem."""
import math
from plates import D


def _arrow(d, x0, y0, x1, y1, head=5):
    """A straight arrow from (x0, y0) to (x1, y1), its head drawn as two short strokes."""
    a = math.atan2(y1 - y0, x1 - x0)
    d.lines([[(x0, y0), (x1, y1)],
             [(x1 - head * math.cos(a - 0.45), y1 - head * math.sin(a - 0.45)), (x1, y1),
              (x1 - head * math.cos(a + 0.45), y1 - head * math.sin(a + 0.45))]])


def hilbert_problems():
    """Problem 10's kind of question: x² − 2y² = 1 on the integer lattice, with the
    whole-number points the curve passes through circled."""
    d = D()
    ox, oy, s = 40, 272, 18            # origin and one unit, the same on both axes
    X, Y = 18, 13
    P = lambda x, y: (ox + s * x, oy - s * y)
    d.group('thin')
    # the integer lattice, and the axes
    d.lines([[P(i, 0), P(i, Y)] for i in range(1, X + 1)] + [[P(0, j), P(X, j)] for j in range(1, Y + 1)])
    d.group('mid')
    d.lines([[P(0, 0), P(X + 0.6, 0)], [P(0, 0), P(0, Y + 0.6)]])
    # projection lines from the solutions to the axes
    d.group('thin')
    for x, y in [(3, 2), (17, 12)]:
        d.lines([[P(x, 0), P(x, y)], [P(0, y), P(x, y)]])
    d.group()
    # the hyperbola x = √(1 + 2y²), from its vertex (1, 0) up to the edge of the lattice
    ymax = math.sqrt((X ** 2 - 1) / 2)
    pts = [P(math.sqrt(1 + 2 * y * y), y) for y in [ymax * i / 90 for i in range(91)]]
    d.line(*pts)
    d.group('mid')
    for x, y in [(1, 0), (3, 2), (17, 12)]:
        d.circle(*P(x, y), 4)
    d.group('mid')
    d.text(*P(4.1, 1.55), '(3, 2)', size=8, anchor='start')
    d.text(*P(15.6, 12.2), '(17, 12)', size=8, anchor='end')
    d.text(*P(1.2, -0.95), '(1, 0)', size=8)
    d.text(*P(9.5, 9.0), 'x² − 2y² = 1', anchor='end')
    d.text(*P(X + 0.6, -0.95), 'x', size=8)
    d.text(*P(-0.9, Y + 0.3), 'y', size=8)
    return d


def godel():
    """Gödel numbering: the signs of 'ff0' coded as 3, 3, 1, set as exponents of the
    primes 2, 3, 5 to give 1080; the number factored back into its signs; and the
    sentence that speaks of its own number."""
    d = D()
    bx, by, bw, bh = 34, 36, 30, 26
    signs, codes, primes = ['f', 'f', '0'], [3, 3, 1], [2, 3, 5]
    cx = [bx + bw * i + bw / 2 for i in range(3)]
    d.group('thin')
    # each sign read down to its code and its prime power, then gathered into one number
    for x in cx:
        d.line((x, by + bh), (x, 122))
    for x in cx:
        d.line((x, 132), (cx[1], 162))
    # the factor ladder's guide: one step per division
    lx, ly, step = 236, 34, 30
    d.group()
    for i in range(3):
        d.line((bx + bw * i, by), (bx + bw * (i + 1), by), (bx + bw * (i + 1), by + bh), (bx + bw * i, by + bh), closed=True)
    d.line((cx[1] - 26, 162), (cx[1] + 26, 162), (cx[1] + 26, 182), (cx[1] - 26, 182), closed=True)
    # the ladder: 1080 divided by its least prime until one prime is left
    n, x, y, rungs = 1080, lx, ly, []
    while True:
        p = next(q for q in range(2, n + 1) if n % q == 0)
        if p == n:
            break
        rungs.append((x, y, n, p))
        n //= p
        x, y = x + 18, y + step
    last = (x, y, n)
    segs = []
    for rx, ry, rn, rp in rungs:
        segs.append([(rx, ry + 4), (rx - 16, ry + step - 10)])
        segs.append([(rx, ry + 4), (rx + 16, ry + step - 10)])
    d.lines(segs)
    # the sentence G and its number g, and the loop by which G speaks of g
    gx, gy = 60, 262
    d.line((gx - 22, gy - 13), (gx + 22, gy - 13), (gx + 22, gy + 13), (gx - 22, gy + 13), closed=True)
    d.circle(gx + 120, gy, 14)
    d.group('mid')
    _arrow(d, gx + 24, gy, gx + 104, gy)
    # the loop back: from the top of g over to the top of G
    mx, rx, ry = gx + 60, 60, 34
    arc = [(mx + rx * math.cos(math.radians(a)), gy - 14 - ry * math.sin(math.radians(a)))
           for a in [i * 180 / 40 for i in range(41)]]
    d.line(*arc)
    _arrow(d, arc[-3][0], arc[-3][1], arc[-1][0], arc[-1][1] + 1)
    d.group('mid')
    for x, s in zip(cx, signs):
        d.text(x, by + 17, s, size=10)
    for x, c, p in zip(cx, codes, primes):
        d.text(x, 88, str(c))
        d.text(x, 116, f'{p}' + '⁰¹²³⁴⁵⁶⁷⁸⁹'[c], size=10)
    d.text(cx[1], 176, '1080')
    for rx, ry, rn, rp in rungs:
        d.text(rx, ry, str(rn), size=8)
        d.text(rx - 18, ry + step - 2, str(rp), size=8)
    d.text(last[0], last[1], str(last[2]), size=8)
    d.text(gx, gy + 3, 'G')
    d.text(gx + 120, gy + 3, 'g')
    d.text(gx + 60, gy - 54, 'NOT PROVABLE', size=7)
    d.text(bx + 3 * bw + 10, by + 16, 'SIGNS', size=7, anchor='start')
    d.text(bx + 3 * bw + 10, 88, 'CODES', size=7, anchor='start')
    d.text(bx + 3 * bw + 10, 116, 'POWERS', size=7, anchor='start')
    return d


def entscheidungsproblem():
    """The diagonal argument for halting: programs down, inputs across, each cell
    'halts' (a bar) or 'runs forever' (a ring), with invented entries. The diagonal is
    boxed, and the program D below it does the opposite of each diagonal cell."""
    d = D()
    n, cell, x0, y0 = 7, 28, 62, 34
    # an invented table: True where program i halts on input j
    table = [[((i * 5 + j * 3 + i * j) % 7) not in (0, 3, 5) for j in range(n)] for i in range(n)]
    dy = y0 + n * cell + 22                      # the row for D
    C = lambda i, j: (x0 + j * cell + cell / 2, y0 + i * cell + cell / 2)
    d.group('thin')
    d.lines([[(x0 + j * cell, y0), (x0 + j * cell, y0 + n * cell)] for j in range(n + 1)] +
            [[(x0, y0 + i * cell), (x0 + n * cell, y0 + i * cell)] for i in range(n + 1)])
    # each diagonal cell dropped to D's row
    for k in range(n):
        x, y = C(k, k)
        d.line((x, y + cell / 2), (x, dy - 2))
    d.group('mid')
    d.lines([[(x0, dy - 1), (x0 + n * cell, dy - 1)], [(x0, dy + cell - 1), (x0 + n * cell, dy + cell - 1)]] +
            [[(x0 + j * cell, dy - 1), (x0 + j * cell, dy + cell - 1)] for j in range(n + 1)])

    def mark(x, y, halts):
        if halts:
            d.line((x, y - 7), (x, y + 7))
        else:
            d.circle(x, y, 5.5)
    for i in range(n):
        for j in range(n):
            if i != j:
                mark(*C(i, j), table[i][j])
    d.group()
    # the diagonal, boxed, and D's row, the diagonal flipped
    for k in range(n):
        x, y = C(k, k)
        d.line((x - cell / 2 + 2, y - cell / 2 + 2), (x + cell / 2 - 2, y - cell / 2 + 2),
               (x + cell / 2 - 2, y + cell / 2 - 2), (x - cell / 2 + 2, y + cell / 2 - 2), closed=True)
        mark(x, y, table[k][k])
    for k in range(n):
        x, _ = C(k, k)
        mark(x, dy + cell / 2 - 1, not table[k][k])
    d.group('mid')
    for k in range(n):
        d.text(x0 - 12, y0 + k * cell + cell / 2 + 3, f'P{k + 1}', size=8, anchor='end')
        d.text(x0 + k * cell + cell / 2, y0 - 8, str(k + 1), size=8)
    d.text(x0 - 12, dy + cell / 2 + 2, 'D', anchor='end')
    d.text(x0 + n * cell / 2, y0 - 22, 'INPUT', size=7)
    d.text(x0 + n * cell + 16, dy + cell / 2 + 2, 'D DOES THE OPPOSITE', size=7, anchor='start')
    lx = x0 + n * cell + 26
    d.text(lx + 12, y0 + 2 * cell + 3, 'HALTS', size=7, anchor='start')
    d.text(lx + 12, y0 + 3 * cell + 3, 'RUNS FOREVER', size=7, anchor='start')
    d.group('mid')
    mark(lx, y0 + 2 * cell, True)
    mark(lx, y0 + 3 * cell, False)
    return d


PLATES = {
    'hilbert-problems': hilbert_problems,
    'godel': godel,
    'entscheidungsproblem': entscheidungsproblem,
}
