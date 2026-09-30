"""Plates for the mathematics subject's Probability segment, part 1 (sprint 024):
the problem of points, the law of large numbers, the normal distribution and Bayes."""
import math, random
from fractions import Fraction
from plates import D


def problem_of_points():
    """Pascal's unfinished game: first to three points, 64 pistoles staked.
    Each state (a, b) is a score; its value is the first player's fair share,
    the mean of the two states one throw later (Pascal's rule, computed here).
    The thin lattice is Fermat's fiction: the game played on to five throws."""
    d = D()
    N, S = 3, 64
    x0, y0, dx, dy = 200, 34, 38, 46

    def at(a, b):
        return x0 + (a - b) * dx, y0 + (a + b) * dy

    def value(a, b):
        if a == N:
            return Fraction(S)
        if b == N:
            return Fraction(0)
        return (value(a + 1, b) + value(a, b + 1)) / 2

    live = [(a, b) for a in range(N) for b in range(N)]
    ends = [(N, b) for b in range(N)] + [(a, N) for a in range(N)]
    def edge(p, q, r0=11, r1=11):
        (x1, y1), (x2, y2) = p, q
        l = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / l, (y2 - y1) / l
        return [(x1 + r0 * ux, y1 + r0 * uy), (x2 - r1 * ux, y2 - r1 * uy)]

    drawn = set(live + ends)
    d.group('thin')
    # Fermat's fiction: the game played on to five throws, whether or not it is already over
    segs = []
    for a in range(6):
        for b in range(6 - a):
            if a + b < 5 and (a, b) not in live:
                for q in ((a + 1, b), (a, b + 1)):
                    segs.append(edge(at(a, b), at(*q), 11 if (a, b) in drawn else 0, 11 if q in drawn else 0))
    d.lines(segs)
    d.group()
    # the real game: from each unfinished score, one throw either way
    segs = []
    for a, b in live:
        segs.append(edge(at(a, b), at(a + 1, b)))
        segs.append(edge(at(a, b), at(a, b + 1)))
    d.lines(segs)
    d.group('mid')
    for a, b in live + ends:
        x, y = at(a, b)
        d.circle(x, y, 11)
    d.group('mid')
    for a, b in live + ends:
        x, y = at(a, b)
        d.text(x, y + 3, str(value(a, b)), size=8)
    x, y = at(0, 0)
    d.text(x, y - 18, '0 : 0', size=7)
    for a, b in [(1, 0), (2, 0), (2, 1)]:
        x, y = at(a, b)
        d.text(x + 15, y - 8, f'{a} : {b}', size=7, anchor='start')
    d.text(x0 + 4 * dx + 20, y0 + 1.5 * dy, 'FIRST TO 3', size=7)
    d.text(x0 + 4 * dx + 20, y0 + 1.5 * dy + 12, 'STAKE 64', size=7)
    return d


def large_numbers():
    """Five runs of a fair coin, the share of heads after each toss, on a log scale
    of tosses: they wander early and are squeezed later between 1/2 ± 1/√n
    (two standard deviations). Computed with a seeded generator."""
    d = D()
    L, R, T, B = 52, 372, 26, 246
    n_max = 100000
    lo, hi = 0.2, 0.8

    def X(n):
        return L + (R - L) * (math.log10(n) - 1) / (math.log10(n_max) - 1)

    def Y(p):
        return B - (B - T) * (p - lo) / (hi - lo)

    d.group('thin')
    d.line((L, T), (L, B), (R, B))
    d.lines([[(X(10 ** k), B), (X(10 ** k), B + 4)] for k in range(1, 6)])
    d.lines([[(L - 4, Y(p)), (L, Y(p))] for p in (0.25, 0.5, 0.75)])
    d.line((L, Y(0.5)), (R, Y(0.5)))
    ns = [10 ** (i / 40) for i in range(40, 201)]
    for sgn in (1, -1):
        pts = [(X(n), Y(min(hi, max(lo, 0.5 + sgn / math.sqrt(n))))) for n in ns]
        d.line(*pts)
    d.group()
    rng = random.Random(1713)
    marks = sorted({round(10 ** (i / 40)) for i in range(40, 201)})
    for run in range(5):
        h, pts, m = 0, [], 0
        for n in range(1, n_max + 1):
            h += rng.random() < 0.5
            if n == marks[m]:
                pts.append((X(n), Y(min(hi, max(lo, h / n)))))
                m += 1
                if m == len(marks):
                    break
        d.line(*pts)
    d.group('mid')
    # Bernoulli's band, one fiftieth either side of the true share
    d.lines([[(L, Y(0.52)), (R, Y(0.52))], [(L, Y(0.48)), (R, Y(0.48))]])
    d.group('mid')
    for k, s in enumerate(['10', '100', '1,000', '10,000', '100,000'], start=1):
        d.text(X(10 ** k), B + 15, s, size=7)
    d.text(L - 8, Y(0.5) + 3, '1/2', size=7, anchor='end')
    d.text(L - 8, Y(0.75) + 3, '3/4', size=7, anchor='end')
    d.text(L - 8, Y(0.25) + 3, '1/4', size=7, anchor='end')
    d.text((L + R) / 2, B + 30, 'TOSSES', size=7)
    d.text(R, Y(0.52) - 5, '1/2 + 1/50', size=7, anchor='end')
    d.text(X(60), Y(0.5 + 1 / math.sqrt(60)) - 6, '1/2 + 1/√n', size=7, anchor='start')
    return d


def normal_distribution():
    """A Galton board of ten rows: the pegs in quincunx, one shot's path, the
    columns of shot in the eleven bins in proportion to the binomial
    coefficients C(10, k), and the normal curve of the same mean and spread."""
    d = D()
    rows, s = 10, 17
    cx, top = 200, 58
    h = s * math.sqrt(3) / 2
    base = 276
    col_max = 72
    peg = lambda i, j: (cx + (j - i / 2) * s, top + i * h)
    bin_x = lambda k: cx + (k - rows / 2) * s
    floor = top + rows * h + 6
    d.group('thin')
    # the quincunx's envelope, the bin walls and the centre line
    d.line(peg(0, 0), (bin_x(-0.5), floor))
    d.line(peg(0, 0), (bin_x(rows + 0.5), floor))
    d.lines([[(bin_x(k - 0.5), floor), (bin_x(k - 0.5), base)] for k in range(rows + 2)])
    d.line((cx, 20), (cx, base))
    d.group()
    # funnel and frame
    d.line((cx - 60, 14), (cx - 5, top - 14), (cx - 5, top - 8))
    d.line((cx + 60, 14), (cx + 5, top - 14), (cx + 5, top - 8))
    d.line((bin_x(-0.5) - 6, floor - 4), (bin_x(-0.5) - 6, base), (bin_x(rows + 0.5) + 6, base),
           (bin_x(rows + 0.5) + 6, floor - 4))
    d.group('mid')
    for i in range(rows):
        for j in range(i + 1):
            x, y = peg(i, j)
            d.circle(x, y, 1.6)
    d.group()
    # the columns of shot, in proportion to C(10, k)
    peak = math.comb(rows, rows // 2)
    for k in range(rows + 1):
        hh = col_max * math.comb(rows, k) / peak
        if hh >= 1:
            x = bin_x(k)
            d.line((x - s / 2 + 2, base), (x - s / 2 + 2, base - hh), (x + s / 2 - 2, base - hh), (x + s / 2 - 2, base))
    d.group('mid')
    # the normal curve, mean 5, standard deviation √10/2, scaled to the columns
    sig = math.sqrt(rows) / 2
    scale = col_max / (peak / 2 ** rows)
    pts = []
    for i in range(0, 241):
        k = -1 + (rows + 2) * i / 240
        pdf = math.exp(-((k - rows / 2) ** 2) / (2 * sig * sig)) / (sig * math.sqrt(2 * math.pi))
        pts.append((bin_x(k), base - scale * pdf))
    d.line(*pts)
    # one shot's path: a step left or right at every peg
    rng = random.Random(1889)
    j, path = 0, [(cx, top - 8)]
    for i in range(rows):
        x, y = peg(i, j)
        path.append((x, y - 3))
        j += rng.random() < 0.5
        nx = cx + (j - (i + 1) / 2) * s
        path.append(((x + nx) / 2, y + h / 2))
    path.append((bin_x(j), floor))
    d.line(*path)
    d.group('mid')
    for k in range(rows + 1):
        d.text(bin_x(k), base + 11, str(math.comb(rows, k)), size=6)
    return d


def bayes():
    """Our invented screening test, drawn as natural frequencies: 100,000 people,
    1 in 1,000 with the condition, the test finding 99% of them and flagging 5%
    of the rest. Below, the same sum in Turing's decibans on a log-odds line."""
    d = D()
    root = (200, 26)
    have, havenot = (104, 82), (296, 82)
    leaves = [(62, 138), (146, 138), (254, 138), (338, 138)]
    d.group('thin')
    # the deciban line and its ticks, and the bracket's guide
    ax_y, L, R = 236, 40, 360
    dbx = lambda db: L + (db + 40) * (R - L) / 50
    d.line((L, ax_y), (R, ax_y))
    d.lines([[(dbx(v), ax_y - 4), (dbx(v), ax_y + 4)] for v in range(-40, 11, 10)])
    d.lines([[(dbx(v), ax_y - 2), (dbx(v), ax_y + 2)] for v in range(-40, 11, 2)])
    d.line((62, 150), (62, 168), (254, 168), (254, 150))
    d.group()
    down = lambda p, q: [(p[0], p[1] + 9), (q[0], q[1] - 9)]
    d.lines([down(root, have), down(root, havenot), down(have, leaves[0]), down(have, leaves[1]),
             down(havenot, leaves[2]), down(havenot, leaves[3])])
    d.group('mid')
    for x, y in [root, have, havenot] + leaves:
        d.line((x - 30, y - 9), (x + 30, y - 9), (x + 30, y + 9), (x - 30, y + 9), closed=True)
    # the evidence as hops along the log-odds line: prior, one positive test, a second
    prior = 10 * math.log10(1 / 999)
    factor = 10 * math.log10(0.99 / 0.05)
    stops = [prior, prior + factor, prior + 2 * factor]
    for a, b in zip(stops, stops[1:]):
        xa, xb = dbx(a), dbx(b)
        r = (xb - xa) / 2
        d.arc((xa + xb) / 2, ax_y - 6, r, 180, 360, n=30, ry=18)
        d.line((xb - 4, ax_y - 12), (xb, ax_y - 6), (xb + 3, ax_y - 12))
    d.lines([[(dbx(v), ax_y - 7), (dbx(v), ax_y + 7)] for v in stops])
    d.group('mid')
    for (x, y), s in zip([root, have, havenot] + leaves,
                         ['100,000', '100', '99,900', '99 +', '1 −', '4,995 +', '94,905 −']):
        d.text(x, y + 3, s, size=8)
    d.text(158, 182, '99 OF 5,094 POSITIVES', size=7)
    for v in range(-40, 11, 10):
        d.text(dbx(v), ax_y + 16, f'{v:+d}' if v else '0', size=7)
    d.text(dbx(0), ax_y + 27, 'EVENS', size=6)
    d.text(dbx(prior), ax_y - 32, 'PRIOR', size=6)
    for a, b in zip(stops, stops[1:]):
        d.text((dbx(a) + dbx(b)) / 2, ax_y - 29, f'+{factor:.0f}', size=7)
    d.text(R, ax_y + 38, 'DECIBANS', size=7, anchor='end')
    return d


PLATES = {
    'problem-of-points': problem_of_points,
    'large-numbers': large_numbers,
    'normal-distribution': normal_distribution,
    'bayes': bayes,
}
