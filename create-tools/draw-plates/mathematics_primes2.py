"""Plates for the primes trail, part 2: the prime number theorem, RSA and bounded gaps (sprint 024)."""
import math
from plates import D


def _primes(n):
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = [False] * len(s[i * i::i])
    return s


def _li(x):
    """The logarithmic integral, by Ramanujan's series (good to many places for x > 2)."""
    g = 0.5772156649015329
    L = math.log(x)
    tot, term, inner = 0.0, 1.0, 0.0
    for n in range(1, 120):
        term *= L / n
        if n % 2 == 1:
            inner += 1.0 / n
        tot += (-1) ** (n - 1) * term / 2 ** (n - 1) * inner
    return g + math.log(L) + math.sqrt(x) * tot


def prime_number_theorem():
    """pi(x) as a staircase against x/ln x and li(x), for x up to 400."""
    d = D()
    X, Y = 400, 90
    x0, y0, w, h = 40, 262, 300, 220
    sx, sy = w / X, h / Y
    P = lambda x, y: (x0 + x * sx, y0 - y * sy)
    d.group('thin')
    # the axes' grid: every 100 along x, every 20 up
    d.lines([[P(x, 0), P(x, Y)] for x in range(100, X + 1, 100)] +
            [[P(0, y), P(X, y)] for y in range(20, Y + 1, 20)])
    d.group('mid')
    d.line(P(0, Y), P(0, 0), P(X, 0))
    d.lines([[P(x, 0), (P(x, 0)[0], y0 + 4)] for x in range(100, X + 1, 100)] +
            [[P(0, y), (x0 - 4, P(0, y)[1])] for y in range(20, Y + 1, 20)])
    d.group()
    # pi(x): one step up at each prime
    s = _primes(X)
    pts, c = [P(2, 0)], 0
    for n in range(2, X + 1):
        if s[n]:
            pts.append(P(n, c))
            c += 1
            pts.append(P(n, c))
    pts.append(P(X, c))
    d.line(*pts)
    d.group('mid')
    # the two smooth approximations, computed
    d.line(*[P(x, x / math.log(x)) for x in range(3, X + 1, 4)])
    d.line(*[P(x, _li(x)) for x in range(3, X + 1, 4)])
    d.group('mid')
    for x in range(100, X + 1, 100):
        d.text(P(x, 0)[0], y0 + 14, str(x), size=7)
    for y in range(20, Y + 1, 20):
        d.text(x0 - 8, P(0, y)[1] + 3, str(y), size=7, anchor='end')
    d.text(P(X, _li(X))[0] + 4, P(X, _li(X))[1] + 3, 'li(x)', size=8, anchor='start')
    d.text(P(X, c)[0] + 4, P(X, c)[1] + 4, 'π(x)', size=8, anchor='start')
    d.text(P(X, X / math.log(X))[0] + 4, P(X, X / math.log(X))[1] + 4, 'x/ln x', size=8, anchor='start')
    d.text(x0 + w / 2, 290, 'PRIMES UP TO x', size=7)
    return d


def rsa():
    """Encryption as a shuffle: each M in 0..32 sent to M^3 mod 33, and C^7 mod 33 bringing it home."""
    d = D()
    n, e, dd = 33, 3, 7
    x0, x1 = 36, 364
    step = (x1 - x0) / (n - 1)
    ys = [70, 150, 230]
    X = lambda m: x0 + m * step
    d.group('thin')
    for y in ys:
        d.line((x0 - 8, y), (x1 + 8, y))
    d.lines([[(X(m), ys[0]), (X(m), ys[0] - 5)] for m in range(n)] +
            [[(X(m), ys[1] - 3), (X(m), ys[1] + 3)] for m in range(n)] +
            [[(X(m), ys[2]), (X(m), ys[2] + 5)] for m in range(n)])
    d.group()
    # encrypt: M on the top line to M^e mod n on the middle one
    d.lines([[(X(m), ys[0]), (X(pow(m, e, n)), ys[1])] for m in range(n)])
    d.group('mid')
    # decrypt: C to C^d mod n, which lands under the M it came from
    d.lines([[(X(c), ys[1]), (X(pow(c, dd, n)), ys[2])] for c in range(n)])
    d.group('mid')
    for m in (0, 8, 16, 24, 32):
        d.text(X(m), ys[0] - 10, str(m), size=7)
        d.text(X(m), ys[2] + 15, str(m), size=7)
    d.text(x0 - 12, ys[0] + 3, 'M', size=8, anchor='end')
    d.text(x0 - 12, ys[1] + 3, 'C', size=8, anchor='end')
    d.text(x0 - 12, ys[2] + 3, 'M', size=8, anchor='end')
    d.text(200, 22, '33 = 3 × 11', size=7)
    d.text(200, 272, 'C = M³ mod 33 · M = C⁷ mod 33', size=7)
    return d


# The admissible 50-tuple of Polymath8b, width 246 (Research in the Mathematical Sciences 1:12, 2014, fig. 1).
TUPLE_50 = [0, 4, 6, 16, 30, 34, 36, 46, 48, 58, 60, 64, 70, 78, 84, 88, 90, 94, 100, 106, 108, 114, 118, 126,
            130, 136, 144, 148, 150, 156, 160, 168, 174, 178, 184, 190, 196, 198, 204, 210, 214, 216, 220, 226,
            228, 234, 238, 240, 244, 246]


def twin_primes():
    """The admissible 50-tuple behind the bound 246, with the residue class it leaves empty for p = 3 to 13."""
    d = D()
    x0, x1 = 26, 374
    sx = (x1 - x0) / 246
    X = lambda v: x0 + v * sx
    ytup = 70
    lanes = [3, 5, 7, 11, 13]
    ylane = {p: 120 + 30 * i for i, p in enumerate(lanes)}
    missing = {p: next(r for r in range(p) if all(h % p != r for h in TUPLE_50)) for p in lanes}
    d.group('thin')
    d.line((x0, ytup), (x1, ytup))
    d.lines([[(X(v), ytup + 2), (X(v), ytup + 6)] for v in range(0, 247, 10)])
    for p in lanes:
        d.line((x0, ylane[p]), (x1, ylane[p]))
    # plumb lines from each member of the tuple down through the lanes
    d.lines([[(X(h), ytup), (X(h), ylane[lanes[-1]])] for h in TUPLE_50])
    d.group()
    d.lines([[(X(h), ytup - 14), (X(h), ytup)] for h in TUPLE_50])
    d.group('mid')
    # each lane: a small circle on every offset in the class the tuple misses, so no plumb line meets one
    for p in lanes:
        for v in range(missing[p], 247, p):
            d.circle(X(v), ylane[p], 1.1)
    d.group('mid')
    d.text(X(0), ytup - 20, '0', size=7)
    d.text(X(246), ytup - 20, '246', size=7)
    d.text(200, 32, '50 OFFSETS, NONE COVERING EVERY CLASS', size=7)
    for p in lanes:
        d.text(x0 - 6, ylane[p] + 3, str(p), size=7, anchor='end')
    d.text(200, 280, 'THE CLASS EACH PRIME LEAVES EMPTY', size=7)
    return d


PLATES = {
    'prime-number-theorem': prime_number_theorem,
    'rsa': rsa,
    'twin-primes': twin_primes,
}
