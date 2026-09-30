"""Plates for the chemistry trail From dyes to drugs, part drugs1: synthetic indigo, aspirin, Salvarsan (sprint 025)."""
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


def _dashes(a, b, n=6, fill=0.5):
    """A dotted line from a to b, as n short dashes (for a hydrogen bond)."""
    segs = []
    for i in range(n):
        t0, t1 = i / n, (i + fill) / n
        segs.append([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                     (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)])
    return segs


def _arrow(d, a, b, head=5):
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    l = (b[0] - head * math.cos(ang - 0.45), b[1] - head * math.sin(ang - 0.45))
    r = (b[0] - head * math.cos(ang + 0.45), b[1] - head * math.sin(ang + 0.45))
    d.lines([[a, b], [l, b, r]])


def _indigoid(O, L):
    """Both halves of indigo's skeleton about the centre of inversion O, with bond length L."""
    r5 = L / (2 * math.sin(math.radians(36)))
    c2 = (O[0] - L / 2, O[1])
    p5 = (c2[0] - r5, O[1])
    c3, c3a, c7a, n1 = (_pt(p5, a, r5) for a in (-72, -144, 144, 72))
    h6 = (c3a[0] - L * math.cos(math.radians(30)), O[1])
    c4, c5, c6, c7 = (_pt(h6, a, L) for a in (-90, -150, 150, 90))
    ox = _pt(c3, -72, L)
    hn = _pt(n1, 72, L * 0.7)

    def flip(p):
        return (2 * O[0] - p[0], 2 * O[1] - p[1])

    h = dict(c2=c2, c3=c3, c3a=c3a, c7a=c7a, n1=n1, c4=c4, c5=c5, c6=c6, c7=c7, ox=ox, hn=hn, p5=p5, h6=h6)
    return [h, {k: flip(v) for k, v in h.items()}], r5


def synthetic_indigo():
    """Indigo and leuco-indigo, one above the other, and the dyer's cycle between them."""
    d = D()
    L = 21
    top, bot = (165, 88), (165, 212)
    indigo, r5 = _indigoid(top, L)
    leuco, _ = _indigoid(bot, L)
    d.group('thin')
    for halves, O in ((indigo, top), (leuco, bot)):
        for h in halves:
            d.circle(*h['p5'], r5)
            d.circle(*h['h6'], L)
        d.circle(*O, 2.2)
    d.line((165, 40), (165, 262))
    # indigo's two hydrogen bonds, N-H of one half to C=O of the other
    d.lines(_dashes(indigo[0]['hn'], indigo[1]['ox']) + _dashes(indigo[1]['hn'], indigo[0]['ox']))
    d.group()
    for halves in (indigo, leuco):
        for h in halves:
            d.line(h['c2'], h['c3'], h['c3a'], h['c4'], h['c5'], h['c6'], h['c7'], h['c7a'], h['n1'], h['c2'])
            d.line(h['c3a'], h['c7a'])
            d.line(h['n1'], h['hn'])
    for h in indigo:                                    # blue: C=O on each half, C=C across the middle
        d.lines(_parallel(h['c3'], h['ox']))
    d.lines(_parallel(indigo[0]['c2'], indigo[1]['c2']))
    for h in leuco:                                     # reduced: C-O(-) on each half, a single bond across the middle
        d.line(h['c3'], h['ox'])
    d.line(leuco[0]['c2'], leuco[1]['c2'])
    d.group('mid')
    for h in indigo + leuco:
        d.lines([_offset(h['c4'], h['c5'], h['h6']), _offset(h['c6'], h['c7'], h['h6']),
                 _offset(h['c7a'], h['c3a'], h['h6'])])
    for h in leuco:                                     # the five-membered ring gains its own double bond
        d.lines([_offset(h['c2'], h['c3'], h['p5'])])
    # the vat and the air: two arrows between the forms
    ax = 318
    _arrow(d, (ax - 12, 104), (ax - 12, 196))
    _arrow(d, (ax + 12, 196), (ax + 12, 104))
    d.group('mid')
    for halves, top_form in ((indigo, True), (leuco, False)):
        for i, h in enumerate(halves):
            up = -72 if i == 0 else 108
            d.text(*_pt(h['ox'], up, 9 if top_form else 11), 'O' if top_form else 'O⁻', size=9)
            n = h['n1']
            d.text(n[0] + (9 if i == 0 else -9), n[1] + 3, 'N', size=8)
            d.text(*_pt(h['hn'], 72 if i == 0 else -108, 7), 'H', size=8)
    d.text(ax - 18, 154, 'VAT', size=8, anchor='end')
    d.text(ax + 18, 154, 'AIR', size=8, anchor='start')
    d.text(165, 22, 'INDIGO · C₁₆H₁₀N₂O₂ · BLUE', size=8)
    d.text(165, 284, 'LEUCO-INDIGO · 2 Na⁺ · YELLOW', size=8)
    return d


def _benzene(d, c, L, start=-90):
    pts = [_pt(c, start + 60 * k, L) for k in range(6)]
    d.line(*pts, closed=True)
    return pts


def aspirin():
    """Salicylic acid acetylated to aspirin: the phenol's OH becomes an ester."""
    d = D()
    L = 20
    sa, asp = (88, 128), (262, 128)
    d.group('thin')
    d.circle(*sa, L)
    d.circle(*asp, L)
    d.line((20, 214), (380, 214))
    d.line((150, 128), (200, 128))
    d.group()
    ring_sa = _benzene(d, sa, L)
    ring_as = _benzene(d, asp, L)
    subs = {}
    for name, ring in (('sa', ring_sa), ('as', ring_as)):
        top, ur = ring[0], ring[1]
        cc = _pt(top, -90, L)                           # the carboxyl carbon, straight up
        o1, o2 = _pt(cc, -150, L), _pt(cc, -30, L)
        d.line(top, cc)
        d.lines(_parallel(cc, o1))
        d.line(cc, o2)
        oe = _pt(ur, -30, L)                            # the phenol oxygen, up and to the right
        d.line(ur, oe)
        subs[name] = dict(cc=cc, o1=o1, o2=o2, oe=oe)
    oe = subs['as']['oe']                               # aspirin only: the acetyl group on that oxygen
    ca = _pt(oe, 30, L)
    oc, me = _pt(ca, 90, L), _pt(ca, -30, L)
    d.line(oe, ca, me)
    d.lines(_parallel(ca, oc))
    d.group('mid')
    for c, ring in ((sa, ring_sa), (asp, ring_as)):
        d.lines([_offset(ring[k], ring[(k + 1) % 6], c) for k in (0, 2, 4)])
    _arrow(d, (152, 128), (198, 128))
    # the recipe of Hoffmann's patent, as weighed parts
    for x, parts, w in ((110, 50, 'SALICYLIC ACID'), (290, 75, 'ACETIC ANHYDRIDE')):
        d.line((x - parts * 0.9, 236), (x + parts * 0.9, 236))
        d.lines([[(x - parts * 0.9, 232), (x - parts * 0.9, 240)], [(x + parts * 0.9, 232), (x + parts * 0.9, 240)]])
    d.group('mid')
    s, a = subs['sa'], subs['as']
    d.text(*_pt(s['o1'], -150, 8), 'O', size=9)
    d.text(*_pt(s['o2'], -30, 9), 'OH', size=9)
    d.text(*_pt(s['oe'], -30, 10), 'OH', size=9)
    d.text(*_pt(a['o1'], -150, 8), 'O', size=9)
    d.text(*_pt(a['o2'], -30, 9), 'OH', size=9)
    d.text(a['oe'][0], a['oe'][1] - 6, 'O', size=9)
    d.text(*_pt(oc, 90, 10), 'O', size=9)
    d.text(*_pt(me, -30, 12), 'CH₃', size=9)
    d.text(175, 118, '(CH₃CO)₂O', size=8)
    d.text(88, 186, 'C₇H₆O₃ · 138', size=8)
    d.text(262, 186, 'C₉H₈O₄ · 180', size=8)
    d.text(110, 256, '50 PARTS', size=7)
    d.text(290, 256, '75 PARTS', size=7)
    d.text(200, 280, '2 HOURS AT 150 °C · US PATENT 644,077', size=7)
    return d


def _ring_of_arsenic(d_groups, C, n, side, bond, rl, label_ring=False):
    """An (RAs)n ring: n arsenic atoms on a regular polygon, each carrying a 3-amino-4-hydroxyphenyl ring."""
    ra = side / (2 * math.sin(math.pi / n))
    start = -90
    ats = [_pt(C, start + 360 * k / n, ra) for k in range(n)]
    rings = []
    for k, a in enumerate(ats):
        ang = start + 360 * k / n
        c1 = _pt(a, ang, bond)                         # the ring's carbon bonded to arsenic
        hc = _pt(c1, ang, rl)                          # the ring's centre
        pts = [_pt(hc, ang + 180 + 60 * j, rl) for j in range(6)]   # pts[0] is c1, pts[3] is para
        oh = _pt(pts[3], ang, rl * 0.8)
        nh = _pt(pts[2], ang - 60, rl * 0.8)
        rings.append(dict(a=a, c1=c1, hc=hc, pts=pts, oh=oh, nh=nh, ang=ang))
    thin, main, mid = d_groups
    thin.append(('circle', C, ra))
    for r in rings:
        thin.append(('circle', r['hc'], rl))
    main.append(('poly', ats))
    for r in rings:
        main.append(('line', [r['a'], r['c1']]))
        main.append(('poly', r['pts']))
        main.append(('line', [r['pts'][3], r['oh']]))
        main.append(('line', [r['pts'][2], r['nh']]))
        mid.append(('lines', [_offset(r['pts'][j], r['pts'][(j + 1) % 6], r['hc'], k=2.4) for j in (1, 3, 5)]))
    return ats, rings


def salvarsan():
    """Salvarsan as it is: rings of three and of five arsenic atoms (Lloyd and others, 2005)."""
    d = D()
    thin, main, mid = [], [], []
    ats3, rings3 = _ring_of_arsenic((thin, main, mid), (100, 120), 3, 22, 11, 11)
    ats5, rings5 = _ring_of_arsenic((thin, main, mid), (290, 120), 5, 22, 11, 11)

    def emit(items):
        for kind, *args in items:
            if kind == 'circle':
                d.circle(*args[0], args[1])
            elif kind == 'poly':
                d.line(*args[0], closed=True)
            elif kind == 'line':
                d.line(*args[0])
            else:
                d.lines(args[0])

    d.group('thin')
    emit(thin)
    d.line((20, 222), (380, 222))
    d.group()
    emit(main)
    d.group('mid')
    emit(mid)
    # the formula printed for a century: R-As=As-R, drawn small and faint
    y = 252
    a1, a2 = (184, y), (216, y)
    d.lines(_parallel(a1, a2, k=3))
    for a, s in ((a1, -1), (a2, 1)):
        c1 = (a[0] + s * 12, y)
        hc = (c1[0] + s * 10, y)
        d.line(a, c1)
        d.line(*[_pt(hc, (180 if s > 0 else 0) + 60 * j, 10) for j in range(6)], closed=True)
    d.group('mid')
    d.text(100, 123, 'As', size=7)
    d.text(290, 123, 'As', size=7)
    d.text(100, 206, '(RAs)₃ · m/z 550', size=8)
    d.text(290, 206, '(RAs)₅ · m/z 916', size=8)
    d.text(200, 280, 'As=As · THE FORMULA DRAWN 1910–2005', size=7)
    d.text(200, 24, 'R = 3-AMINO-4-HYDROXYPHENYL', size=7)
    return d


PLATES = {'synthetic-indigo': synthetic_indigo, 'aspirin': aspirin, 'salvarsan': salvarsan}
