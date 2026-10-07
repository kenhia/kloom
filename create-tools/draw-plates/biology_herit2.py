"""Plates for The Story of Life's part herit2 (sprint 055): the fly room and the modern synthesis.
See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def fly_room():
    d = D()
    # Sturtevant's map of 1913 (Journal of Experimental Zoology 14, Diagram 1): the X chromosome as a
    # bar, scaled in his units (percent crossing over), with his five loci: yellow 0.0, white and eosin
    # 1.0, vermilion 30.7, miniature 33.7, rudimentary 57.6. Above, the neighboring distances he built
    # it from (B(C,O) 1.0, (C,O)P 29.7, PR 3.0, PM 26.9, Table 2). Below, yellow to rudimentary measured
    # directly, 37.6, against the map's 57.6: the shortfall double crossovers make.
    x0, x1, units = 44, 364, 60
    sx = (x1 - x0) / units
    X = lambda u: x0 + u * sx
    y, h = 168, 7                                                          # bar center, half height
    loci = [('y', 0.0), ('w', 1.0), ('v', 30.7), ('m', 33.7), ('r', 57.6)]
    spans = [(0.0, 1.0, '1.0'), (1.0, 30.7, '29.7'), (30.7, 33.7, '3.0'), (30.7, 57.6, '26.9')]

    d.group('thin')
    d.line((X(0), 236), (X(units), 236))                                  # the scale
    for u in range(0, units + 1, 10):
        d.line((X(u), 232), (X(u), 240))
    for u in range(0, units + 1, 2):
        d.line((X(u), 234), (X(u), 238))
    for _, u in loci:
        d.line((X(u), y - h - 4), (X(u), 232))                            # each locus down to the scale

    d.group()
    r = h
    d.line((x0 - 4, y - h), (x1 + 6, y - h))
    d.line((x0 - 4, y + h), (x1 + 6, y + h))
    d.arc(x0 - 4, y, r, 90, 270)
    d.arc(x1 + 6, y, r, -90, 90)
    for _, u in loci:
        d.line((X(u), y - h), (X(u), y + h))

    d.group('mid')
    for a, b, _ in spans:                                                 # the measured neighbors
        xa, xb = X(a), X(b)
        top = y - h - 6 - min(70, 6 + (xb - xa) * 0.42)
        d.curve(f"M{xa:.1f},{y - h - 3} Q{(xa + xb) / 2:.1f},{2 * top - (y - h - 3):.1f} {xb:.1f},{y - h - 3}")
    d.line((X(0), 204), (X(37.6), 204))                                   # yellow to rudimentary, observed
    d.line((X(0), 200), (X(0), 208))
    d.line((X(37.6), 200), (X(37.6), 208))
    d.dashed((X(37.6), 204), (X(57.6), 204), dash=3, gap=3)
    _arrow(d, (X(50), 204), (X(57.6), 204), size=4)

    d.group('mid')
    for a, b, label in spans:
        xa, xb = X(a), X(b)
        top = y - h - 6 - min(70, 6 + (xb - xa) * 0.42)
        lx = (xa + xb) / 2
        if label == '1.0':
            d.text(xa + 9, top - 4, label, size=7)
        elif label == '3.0':                                              # under the long arc, right of m
            d.text(xb + 4, y - h - 5, label, size=7, anchor='start')
        else:
            d.text(lx, top - 4, label, size=7)
    for name, u in loci:
        dx = {'y': -3, 'w': 3}.get(name, 0)
        d.text(X(u) + dx, y + h + 13, name, size=7)
    for u in range(0, units + 1, 10):
        d.text(X(u), 250, str(u), size=7)
    d.text(X(37.6) / 2 + X(0) / 2, 198, 'OBSERVED, y TO r: 37.6', size=7)
    d.text((X(37.6) + X(57.6)) / 2, 198, 'MAP: 57.6', size=7)
    d.text(200, 266, 'y YELLOW · w WHITE · v VERMILION · m MINIATURE · r RUDIMENTARY', size=7)
    d.text(200, 34, 'THE X CHROMOSOME, 1913 · UNITS: PERCENT CROSSING OVER', size=7)
    return d


def modern_synthesis():
    d = D()
    # An invented worked example: one allele whose carriers leave 1 + s offspring for every 1 of the
    # others (genic selection, no dominance), from 1 percent of the population to 99. Its odds p/(1-p)
    # multiply by 1 + s each generation, so t generations take it to odds (1/99)(1 + s)^t. Three values
    # of s; the 99 percent mark falls at about 96, 924 and 1,843 generations.
    gx0, gx1, gy0, gy1 = 62, 370, 236, 58                                 # plot box: left, right, p=0, p=1
    gmax = 2000
    X = lambda g: gx0 + (gx1 - gx0) * g / gmax
    Y = lambda p: gy0 - (gy0 - gy1) * p

    def p_at(s, g):
        o = (1 / 99) * (1 + s) ** g
        return o / (1 + o)

    curves = [(0.1, '0.1'), (0.01, '0.01'), (0.005, '0.005')]

    d.group('thin')
    for g in range(0, gmax + 1, 250):
        d.line((X(g), gy0), (X(g), gy1))
    for p in (0.01, 0.5, 0.99):
        d.line((gx0, Y(p)), (gx1, Y(p)))

    d.group()
    d.line((gx0, gy1 - 6), (gx0, gy0), (gx1 + 6, gy0))
    for s, _ in curves:
        pts = []
        g, step = 0.0, 2.0
        while g <= gmax:
            pts.append((X(g), Y(p_at(s, g))))
            g += step
        d.line(*pts)

    d.group('mid')
    for s, _ in curves:
        g50 = math.log(99) / math.log(1 + s)
        g99 = 2 * g50
        d.circle(X(g50), Y(0.5), 2.5)
        if g99 <= gmax:
            d.line((X(g99), Y(0.99) - 4), (X(g99), gy0 + 4))
    for g in range(0, gmax + 1, 500):
        d.line((X(g), gy0), (X(g), gy0 + 5))

    d.group('mid')
    for g in range(0, gmax + 1, 500):
        d.text(X(g), gy0 + 15, f'{g:,}', size=7)
    for p, lab in ((0.01, '1%'), (0.5, '50%'), (0.99, '99%')):
        d.text(gx0 - 6, Y(p) + 2.5, lab, size=7, anchor='end')
    for s, lab in curves:
        g50 = math.log(99) / math.log(1 + s)
        d.text(X(g50) + 6, Y(0.5) + 12, f's = {lab}', size=7, anchor='start')
    d.text((gx0 + gx1) / 2, gy0 + 28, 'GENERATIONS', size=7)
    d.text(216, 38, 'AN ALLELE WITH ADVANTAGE s, FROM 1% TO 99% · INVENTED NUMBERS', size=7)
    return d


PLATES = {'fly-room': fly_room, 'modern-synthesis': modern_synthesis}
