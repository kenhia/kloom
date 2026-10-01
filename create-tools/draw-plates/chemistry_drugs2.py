"""Plates for the chemistry subject's part drugs2 (sprint 025): the end of the trail
From dyes to drugs (prontosil, penicillin) and the first frame of The chemistry of
life (enzymes)."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _offset(a, b, c, k=3.2):
    """A second, shorter line inside a double bond ab, on the side of point c (a ring's centre)."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = c[0] - mx, c[1] - my
    n = math.hypot(dx, dy)
    ox, oy = dx / n * k, dy / n * k
    t = 0.18
    return [(a[0] + (b[0] - a[0]) * t + ox, a[1] + (b[1] - a[1]) * t + oy),
            (a[0] + (b[0] - a[0]) * (1 - t) + ox, a[1] + (b[1] - a[1]) * (1 - t) + oy)]


def _parallel(a, b, k=3.2):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * k, dx / n * k
    return [[(a[0] + ox / 2, a[1] + oy / 2), (b[0] + ox / 2, b[1] + oy / 2)],
            [(a[0] - ox / 2, a[1] - oy / 2), (b[0] - ox / 2, b[1] - oy / 2)]]


def _ring(c, r, a0):
    """A regular hexagon's six vertices about centre c, the first at angle a0."""
    return [_pt(c, a0 + 60 * k, r) for k in range(6)]


def _trim(a, b, ra=0.0, rb=0.0):
    """The segment ab, cut back by ra pixels at a and rb at b (to clear an atom's label)."""
    n = math.dist(a, b)
    return [(a[0] + (b[0] - a[0]) * ra / n, a[1] + (b[1] - a[1]) * ra / n),
            (b[0] - (b[0] - a[0]) * rb / n, b[1] - (b[1] - a[1]) * rb / n)]


def _double(a, b, ra=0.0, rb=0.0, k=3.2):
    return _parallel(*_trim(a, b, ra, rb), k)


def prontosil():
    """Prontosil, the azo bond cut, and sulfanilamide beside the PABA it imitates."""
    d = D()
    L = 21
    ca = (158, 78)                                # ring A's centre; its para bonds run level
    ra = _ring(ca, L, 0)                          # vertex 0 right (to the azo), vertex 3 left (to S)
    n1 = _pt(ra[0], 0, L)
    n2 = _pt(n1, 60, L)
    c1b = _pt(n2, 0, L)
    cb = _pt(c1b, 0, L)
    rb = _ring(cb, L, 0)                          # vertex 3 is c1b
    s = _pt(ra[3], 180, L)
    o1, o2 = _pt(s, 270, L * 0.85), _pt(s, 90, L * 0.85)
    ns = _pt(s, 180, L)
    nb4 = _pt(rb[0], 0, L)                        # ring B's para amine
    nb2 = _pt(rb[2], 120, L)                      # and its ortho amine
    m = ((n1[0] + n2[0]) / 2, (n1[1] + n2[1]) / 2)
    d.group('thin')
    d.circle(*ca, L)
    d.circle(*cb, L)
    d.line(_pt(m, 150, 24), _pt(m, 330, 24))     # the cut through N=N
    d.line((24, 150), (376, 150))
    # the amine end and the acid end of the two small molecules below lie level
    d.line((104, 179), (296, 179))
    d.line((104, 240), (296, 240))
    d.group()
    d.line(*ra, ra[0])
    d.line(*rb, rb[0])
    d.line(*_trim(ra[0], n1, 0, 5))
    d.lines(_double(n1, n2, 5, 5))
    d.line(*_trim(n2, c1b, 5, 0))
    d.line(*_trim(ra[3], s, 0, 6))
    d.lines(_double(s, o1, 6, 6) + _double(s, o2, 6, 6))
    d.line(*_trim(s, ns, 6, 9))
    d.line(*_trim(rb[0], nb4, 0, 7))
    d.line(*_trim(rb[2], nb2, 0, 7))
    d.group('mid')
    d.lines([_offset(ra[k], ra[(k + 1) % 6], ca) for k in (1, 3, 5)])
    d.lines([_offset(rb[k], rb[(k + 1) % 6], cb) for k in (1, 3, 5)])
    # below: sulfanilamide and para-aminobenzoic acid, drawn upright to the same scale
    M = 17
    lows = {}
    for x, acid in ((150, 'S'), (250, 'C')):
        c = (x, 208)
        v = _ring(c, M, -90)                      # vertex 0 at the top, vertex 3 at the bottom
        top = _pt(v[0], -90, M)
        low = _pt(v[3], 90, M)
        lows[acid] = low
        d.group()
        d.line(*v, v[0])
        d.line(*_trim(v[0], top, 0, 7))
        if acid == 'S':
            d.line(*_trim(v[3], low, 0, 6))
            oa, ob, nx = _pt(low, 180, M), _pt(low, 0, M), _pt(low, 90, M)
            d.lines(_double(low, oa, 6, 6) + _double(low, ob, 6, 6))
            d.line(*_trim(low, nx, 6, 7))
        else:
            d.line(v[3], low)
            oa, ob = _pt(low, 150, M), _pt(low, 30, M)
            d.lines(_double(low, oa, 0, 6))
            d.line(*_trim(low, ob, 0, 7))
        d.group('mid')
        d.lines([_offset(v[k], v[(k + 1) % 6], c) for k in (1, 3, 5)])
        d.text(x, top[1] - 2, 'H₂N', size=8)
    d.group('mid')
    d.text(s[0], s[1] + 3.5, 'S', size=10)
    d.text(o1[0], o1[1] + 3.5, 'O', size=9)
    d.text(o2[0], o2[1] + 3.5, 'O', size=9)
    d.text(ns[0] - 4, ns[1] + 3, 'H₂N', size=8)
    d.text(n1[0], n1[1] + 3.5, 'N', size=9)
    d.text(n2[0], n2[1] + 3.5, 'N', size=9)
    d.text(nb4[0] + 6, nb4[1] + 3, 'NH₂', size=8)
    d.text(nb2[0] - 2, nb2[1] + 6, 'NH₂', size=8)
    d.text(200, 26, 'PRONTOSIL · C₁₂H₁₃N₅O₂S', size=8)
    lo = _pt(m, 150, 24)
    d.text(lo[0] - 4, lo[1] + 10, 'CUT', size=7)
    low = lows['S']
    d.text(low[0], low[1] + 3.5, 'S', size=9)
    d.text(low[0] - M, low[1] + 3.5, 'O', size=8)
    d.text(low[0] + M, low[1] + 3.5, 'O', size=8)
    d.text(low[0] + 1, low[1] + M + 4, 'NH₂', size=7)
    low = lows['C']
    oa, ob = _pt(low, 150, M), _pt(low, 30, M)
    d.text(oa[0] - 2, oa[1] + 5, 'O', size=8)
    d.text(ob[0] + 6, ob[1] + 5, 'OH', size=8)
    d.text(150, 290, 'SULFANILAMIDE', size=7)
    d.text(250, 290, 'PABA', size=7)
    d.text(200, 212, '≈', size=12)
    return d


def penicillin():
    """Benzylpenicillin: the four-membered β-lactam fused to the thiazolidine, its square corner
    against the tetrahedral angle, and the enzyme's serine that opens it."""
    d = D()
    L = 32
    c5 = (178, 128)                               # the bridgehead carbon, top of the shared edge
    n4 = (178, 128 + L)
    c6 = (178 - L, 128)
    c7 = (178 - L, 128 + L)
    # the thiazolidine: a regular pentagon on the shared edge n4-c5, to its right
    R = L / (2 * math.sin(math.radians(36)))
    pc = (178 + L / 2 / math.tan(math.radians(36)), 128 + L / 2)
    ang = math.degrees(math.atan2(c5[1] - pc[1], c5[0] - pc[0]))
    s1, c2, c3 = (_pt(pc, ang + 72 * k, R) for k in (1, 2, 3))
    o7 = _pt(c7, 135, L * 0.8)                    # the lactam carbonyl oxygen
    me1, me2 = _pt(c2, ang + 144 - 35, L * 0.7), _pt(c2, ang + 144 + 35, L * 0.7)
    cc = _pt(c3, ang + 216, L * 0.8)              # the carboxyl carbon
    cco1, cco2 = _pt(cc, 30, L * 0.75), _pt(cc, 150, L * 0.75)
    # the side chain on c6: NH-C(=O)-CH2-phenyl, zigzag up and to the left
    na = _pt(c6, 240, L * 0.85)
    cam = _pt(na, 180, L * 0.85)
    oa = _pt(cam, 120, L * 0.75)
    ch2 = _pt(cam, 240, L * 0.85)
    ph = _pt(ch2, 180, L * 0.8)
    phc = _pt(ph, 180, L * 0.6)
    phv = _ring(phc, L * 0.6, 0)
    d.group('thin')
    d.circle(*pc, R)
    d.arc(*c7, 10, 270, 360, n=12)
    # beside it: the angle a carbon with four single bonds prefers, and the ring's corner
    tx, ty = 292, 118
    d.line((tx, ty), _pt((tx, ty), 0, 44))
    d.line((tx, ty), _pt((tx, ty), -109.5, 40))
    d.arc(tx, ty, 13, -109.5, 0, n=16)
    ux, uy = 292, 204
    d.line((ux, uy), _pt((ux, uy), 0, 44))
    d.line((ux, uy), _pt((ux, uy), -90, 40))
    d.arc(ux, uy, 13, -90, 0, n=12)
    d.group()
    d.line(c6, c5)
    d.line(*_trim(c5, n4, 0, 6))
    d.line(*_trim(n4, c7, 6, 0))
    d.line(c7, c6)
    d.line(*_trim(c5, s1, 0, 6))
    d.line(*_trim(s1, c2, 6, 0))
    d.line(c2, c3)
    d.line(*_trim(c3, n4, 0, 6))
    d.lines(_double(c7, o7, 0, 6))
    d.line(c2, me1)
    d.line(c2, me2)
    d.line(c3, cc)
    d.lines(_double(cc, cco2, 0, 6))
    d.line(*_trim(cc, cco1, 0, 8))
    d.line(*_trim(c6, na, 0, 8))
    d.line(*_trim(na, cam, 8, 0))
    d.lines(_double(cam, oa, 0, 6))
    d.line(cam, ch2, ph)
    d.line(*phv, phv[0])
    d.group('mid')
    d.lines([_offset(phv[k], phv[(k + 1) % 6], phc) for k in (0, 2, 4)])
    # the enzyme's serine, its oxygen reaching for the lactam carbon, and the C-N bond it breaks
    sx, sy = 84, 246
    ex, ey = c7[0] + 3, c7[1] + 8
    d.curve(f'M{sx + 26} {sy - 4} Q {ex + 4} {sy + 2} {ex} {ey}')
    d.line((ex - 4, ey + 7), (ex, ey), (ex + 4, ey + 7))
    mid = ((c7[0] + n4[0]) / 2, (c7[1] + n4[1]) / 2)
    d.line((mid[0] - 4, mid[1] - 9), (mid[0] + 4, mid[1] + 9))
    d.group('mid')
    d.text(s1[0], s1[1] + 3.5, 'S', size=10)
    d.text(n4[0], n4[1] + 3.5, 'N', size=10)
    d.text(o7[0], o7[1] + 3.5, 'O', size=10)
    d.text(na[0], na[1] + 3, 'NH', size=8)
    d.text(oa[0], oa[1] + 3.5, 'O', size=9)
    d.text(cco1[0] + 3, cco1[1] + 3, 'OH', size=8)
    d.text(cco2[0], cco2[1] + 3.5, 'O', size=9)
    d.text(sx, sy + 3, 'SER–OH', size=8)
    d.text(c7[0] + L / 2, c7[1] - L / 2 + 3, '90°', size=7)
    d.text(tx + 26, ty - 18, '109.5°', size=8)
    d.text(tx + 22, ty + 14, 'C, 4 BONDS', size=6)
    d.text(ux + 24, uy - 18, '90°', size=8)
    d.text(ux + 22, uy + 14, 'THE RING', size=6)
    d.text(200, 288, 'BENZYLPENICILLIN · C₁₆H₁₈N₂O₄S · β-LACTAM', size=8)
    return d


def enzymes():
    """Michaelis and Menten's saturation curve for invertase, plotted as they plotted it, against
    the logarithm of the sucrose concentration, with their tangent of slope 0.576 at half speed."""
    d = D()
    K = 16.7                                        # mM, Michaelis and Menten's constant for sucrose
    x0, x1, y0, y1 = 60, 360, 236, 56               # the plot's box: log10 [S] from 0 to 3, rate 0 to 1
    lx = lambda s: x0 + (math.log10(s) - 0) / 3 * (x1 - x0)
    ly = lambda v: y0 - v * (y0 - y1)
    d.group('thin')
    for k in range(4):
        d.line((lx(10 ** k), y0), (lx(10 ** k), y1))
    for v in (0.5, 1.0):
        d.line((x0, ly(v)), (x1, ly(v)))
    # the tangent at the half-speed point, slope 0.576 per decade: d/dlog10 of S/(S+K) at S = K
    xm = lx(K)
    run = 0.5 / 0.576 * (x1 - x0) / 3               # the tangent crosses 0 and 1 this far either side
    d.line((xm - run, ly(0)), (xm + run, ly(1)))
    d.line((xm, y0), (xm, ly(0.5)))
    d.group()
    d.line((x0, y1 - 6), (x0, y0), (x1 + 6, y0))
    pts = []
    for i in range(121):
        ls = i / 120 * 3
        s = 10 ** ls
        pts.append((lx(s), ly(s / (s + K))))
    d.line(*pts)
    d.group('mid')
    # the five starting sucrose concentrations of their experiments, on the curve
    for s in (20.8, 41.6, 83.3, 166.7, 333.0):
        d.circle(lx(s), ly(s / (s + K)), 3.2)
    d.circle(xm, ly(0.5), 2)
    for k, t in enumerate(('1', '10', '100', '1000')):
        d.text(lx(10 ** k), y0 + 13, t, size=8)
    d.text(210, y0 + 28, '[SUCROSE] · mM · LOG SCALE', size=7)
    d.text(x0 - 12, ly(1) + 3, '1', size=8)
    d.text(x0 - 14, ly(0.5) + 3, '½', size=9)
    d.text(x0 - 12, ly(0) + 3, '0', size=8)
    d.text(x0 + 4, y1 - 12, 'RATE / MAXIMUM', size=7, anchor='start')
    d.text(xm + 6, y0 - 8, 'Kₘ = 16.7 mM', size=8, anchor='start')
    xt = xm + 0.8 * run
    d.text(xt - 8, ly(0.9) + 2, 'SLOPE 0.576', size=7, anchor='end')
    d.text(266, 196, 'v = V[S]/([S]+Kₘ)', size=7, anchor='start')
    d.text(266, 210, 'INVERTASE · 1913', size=7, anchor='start')
    return d


PLATES = {'prontosil': prontosil, 'penicillin': penicillin, 'enzymes': enzymes}
