"""Plates for The Story of Life's part eco3 (sprint 055): island biogeography and the biodiversity
crisis. See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _cross(f, g, lo=0.0, hi=1.0):
    """Where f(n) - g(n) changes sign on [lo, hi], by bisection."""
    for _ in range(60):
        mid = (lo + hi) / 2
        if (f(lo) - g(lo)) * (f(mid) - g(mid)) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def island_biogeography():
    d = D()
    # MacArthur and Wilson's equilibrium model (Evolution 1963, figs. 4 and 5): against the number of
    # species present, N, the rate of immigration of new species falls to zero at P, the size of the
    # pool, and is lower for a far island; the rate of extinction rises, and is higher for a small
    # island. Each crossing is an equilibrium number. The curve shapes are schematic: immigration
    # concave, as they argued, I0 (1 - N/P)^2; extinction k (N/P)^1.6.
    x0, y0, x1, ytop = 52, 246, 350, 40
    w, h = x1 - x0, y0 - ytop

    def X(n):
        return x0 + n * w

    def Y(r):
        return y0 - r * h

    imm = {'NEAR': 0.92, 'FAR': 0.52}
    ext = {'SMALL': 1.25, 'LARGE': 0.55}

    def I(i0):
        return lambda n: i0 * (1 - n) ** 2

    def E(k):
        return lambda n: k * n ** 1.6

    eq = {(a, b): _cross(I(i0), E(k)) for a, i0 in imm.items() for b, k in ext.items()}

    d.group('thin')
    for (a, b), n in eq.items():                                          # drop lines to the axis
        r = E(ext[b])(n)
        d.dashed((X(n), Y(r)), (X(n), y0), dash=3, gap=3)
    d.line((X(1), y0 + 4), (X(1), y0 - 8))                                # P, the pool
    for k in range(1, 5):
        d.line((x0 - 3, Y(k / 5)), (x0, Y(k / 5)))

    d.group()
    d.line((x0, ytop - 6), (x0, y0), (x1 + 22, y0))                       # axes
    _arrow(d, (x0, y0), (x0, ytop - 6), size=5)
    _arrow(d, (x0, y0), (x1 + 22, y0), size=5)
    for i0 in imm.values():
        f = I(i0)
        d.line(*[(X(t / 60), Y(f(t / 60))) for t in range(61)])
    for k in ext.values():
        g = E(k)
        top = min(1.0, (0.98 / k) ** (1 / 1.6))
        d.line(*[(X(top * t / 60), Y(g(top * t / 60))) for t in range(61)])

    d.group('mid')
    for (a, b), n in eq.items():
        d.circle(X(n), Y(E(ext[b])(n)), 3)

    d.group('mid')
    d.text(x0 + 6, ytop - 4, 'RATE', size=7, anchor='start')
    d.text(x1 + 22, y0 + 26, 'SPECIES PRESENT, N', size=7, anchor='end')
    d.text(X(1), y0 + 14, 'P', size=7)
    d.text(X(0) + 6, Y(imm['NEAR']) - 4, 'IMMIGRATION, NEAR', size=7, anchor='start')
    d.text(X(0) + 6, Y(imm['FAR']) - 4, 'FAR', size=7, anchor='start')
    ks = ext['SMALL']
    ns = (0.98 / ks) ** (1 / 1.6)
    d.text(X(ns) - 4, Y(0.98) + 2, 'EXTINCTION, SMALL', size=7, anchor='end')
    nl = 0.98
    d.text(X(nl) + 4, Y(E(ext['LARGE'])(nl)) - 6, 'LARGE', size=7, anchor='end')
    n_ln, n_fs = eq[('NEAR', 'LARGE')], eq[('FAR', 'SMALL')]
    d.text(X(n_ln), y0 + 14, 'MOST', size=7)
    d.text(X(n_fs), y0 + 14, 'FEWEST', size=7)
    d.text(200, 292, 'WHERE THE CURVES CROSS · MACARTHUR AND WILSON, 1963', size=7)
    return d


def biodiversity_now():
    d = D()
    # The species-area relationship run backward, as IPBES (2019, SPM A5) used it: habitat integrity
    # cut by 30 per cent leaves about 91 per cent of species, which on log-log axes is a line of
    # slope z = ln 0.91 / ln 0.7, about 0.26. Fainter lines at z = 0.15 and 0.35 bracket the slopes
    # usually measured. Axes: habitat left, 10 to 100 per cent; species kept, 50 to 100 per cent.
    x0, x1, y0, y1 = 70, 350, 246, 46
    lo_s = math.log10(0.5)
    z = math.log(0.91) / math.log(0.7)

    def X(a):
        return x0 + (math.log10(a) + 1) * (x1 - x0)

    def Y(s):
        return y0 - (math.log10(s) - lo_s) / (0 - lo_s) * (y0 - y1)

    d.group('thin')
    for a in (0.1, 0.2, 0.3, 0.5, 0.7, 1.0):                              # log grid
        d.line((X(a), y0), (X(a), y1))
    for s in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
        d.line((x0, Y(s)), (x1, Y(s)))
    for zz in (0.15, 0.35):
        d.line(*[(X(a), Y(a ** zz)) for a in (0.1 * 10 ** (t / 40) for t in range(41)) if a ** zz >= 0.5])

    d.group()
    d.line((x0, y1 - 8), (x0, y0), (x1 + 10, y0))
    d.line(*[(X(a), Y(a ** z)) for a in (0.1 * 10 ** (t / 40) for t in range(41))])

    d.group('mid')
    s7 = 0.7 ** z
    d.dashed((X(0.7), y0), (X(0.7), Y(s7)), (x0, Y(s7)), dash=3, gap=3)
    d.circle(X(0.7), Y(s7), 3)
    d.circle(X(1.0), Y(1.0), 3)

    d.group('mid')
    for a, lab in ((0.1, '10%'), (0.3, '30%'), (0.7, '70%'), (1.0, '100%')):
        d.text(X(a), y0 + 12, lab, size=7)
    for s, lab in ((0.5, '50%'), (s7, '91%'), (1.0, '100%')):
        d.text(x0 - 5, Y(s) + 2.5, lab, size=7, anchor='end')
    d.text(x1, y0 + 24, 'HABITAT LEFT (LOG SCALE)', size=7, anchor='end')
    d.text(x0 + 4, y1 - 10, 'SPECIES KEPT (LOG SCALE)', size=7, anchor='start')
    d.text(X(0.15), Y(0.15 ** z) - 8, 'z = 0.26', size=7, anchor='start')
    d.text(X(0.1) + 2, Y(0.1 ** 0.15) - 6, '0.15', size=7, anchor='start')
    d.text(X(0.16), Y(0.16 ** 0.35) + 12, '0.35', size=7, anchor='start')
    d.text(200, 290, 'A SPECIES-AREA CURVE RUN BACKWARD · IPBES, 2019', size=7)
    return d


PLATES = {'island-biogeography': island_biogeography, 'biodiversity-now': biodiversity_now}
