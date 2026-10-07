"""Plates for The Story of Life, part mol2 (sprint 055): photo-51, meselson-stahl. See plates_for.py."""
import math
from plates import D

# First maxima of the Bessel functions J1..J5 (the first zero of each derivative, j'_{n,1}).
# For a helix of radius r and pitch P, the innermost maximum on layer line n lies at a radial
# reciprocal distance R_n = j'_{n,1} / (2 pi r), and the layer line at height Z_n = n / P.
BESSEL_FIRST_MAX = {1: 1.8412, 2: 3.0542, 3: 4.2012, 4: 5.3176, 5: 6.4156}


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p (copied from biology_hand.py)."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def photo_51():
    d = D()
    # Left: the geometry of Photo 51 (structure B), computed from Franklin and Gosling's numbers
    # (Nature 171, 740, 1953): pitch P = 34 A, phosphate radius r = 10 A, ten bases a turn. Layer
    # line n sits n units from the equator; its innermost spot sits out at j'_n P / (2 pi r) units,
    # so spots 1, 2, 3, 5 fall near the arms of a cross. The fourth is missing because the second
    # chain is displaced 3/8 of the pitch: on line n the two chains differ by 3n/8 of a wave, and
    # 4 x 3/8 = 1.5 waves cancels. The strong 3.4 A reflection is on the meridian at line 10.
    # Right: the double helix that makes it, side on, at the same P and r, the second chain 3/8 on.
    P, r = 34.0, 10.0
    cx, cy, h = 118, 150, 10.5                                            # pattern center, px per layer line
    unit = P * h / (2 * math.pi * r)                                      # px per unit of j'
    spots = {n: (BESSEL_FIRST_MAX[n] * unit, n * h) for n in range(1, 6)}
    hx, base, s = 318, 262, 3.0                                           # helix axis x, its foot, px per A
    rad = r * s

    d.group('thin')
    d.circle(cx, cy, 110)                                                 # the edge of the film
    d.line((cx, cy - 116), (cx, cy + 116))                                # meridian
    d.line((cx - 104, cy), (cx + 104, cy))                                # equator
    for n in range(1, 6):
        for sg in (-1, 1):
            d.line((cx - 62, cy + sg * n * h), (cx + 62, cy + sg * n * h))
    x5, y5 = spots[5]
    for sx in (-1, 1):                                                    # the arms of the cross
        for sy in (-1, 1):
            d.line((cx, cy), (cx + sx * x5 * 1.35, cy + sy * y5 * 1.35))
    d.line((hx, base + 8), (hx, base - 2 * P * s - 8))                    # helix axis
    for z in (0, P, 2 * P):
        d.line((hx - rad - 10, base - z * s), (hx + rad + 10, base - z * s))

    d.group()
    d.circle(cx, cy, 4)                                                   # beam stop
    for n, (x, y) in spots.items():
        for sx in (-1, 1):
            for sy in (-1, 1):
                if n == 4:
                    continue
                d.ellipse(cx + sx * x, cy + sy * y, 4.2, 1.8)
    for sy in (-1, 1):                                                    # the 3.4 A meridional arcs
        for rr in (10 * h - 2, 10 * h + 2):
            a0, a1 = (-104, -76) if sy < 0 else (76, 104)
            d.arc(cx, cy, rr, a0, a1, n=16)
    shift = 3 / 8
    for k in range(2):                                                    # the two chains
        pts = []
        for i in range(161):
            z = 2 * P * i / 160
            th = 2 * math.pi * (z / P - k * shift)
            pts.append((hx + rad * math.sin(th), base - z * s))
        d.line(*pts)

    d.group('mid')
    x4, y4 = spots[4]
    for sx in (-1, 1):                                                    # where the fourth spots would be
        for sy in (-1, 1):
            d.dashed(*[(cx + sx * x4 + 4.2 * math.cos(t * math.pi / 12), cy + sy * y4 + 2.4 * math.sin(t * math.pi / 12))
                       for t in range(25)], dash=1.5, gap=1.5)
    for j in range(20):                                                   # base pairs every 3.4 A
        z = 3.4 * (j + 0.5)
        x1 = hx + rad * math.sin(2 * math.pi * z / P)
        x2 = hx + rad * math.sin(2 * math.pi * (z / P - shift))
        d.line((x1, base - z * s), (x2, base - z * s))
    xr = hx + rad + 18                                                    # dimension: one turn
    d.line((xr, base), (xr, base - P * s))
    _arrow(d, (xr, base - P * s / 2), (xr, base))
    _arrow(d, (xr, base - P * s / 2), (xr, base - P * s))
    yd = base - 2 * P * s - 12                                            # dimension: diameter
    d.line((hx - rad, yd), (hx + rad, yd))
    _arrow(d, (hx, yd), (hx - rad, yd), size=4)
    _arrow(d, (hx, yd), (hx + rad, yd), size=4)

    d.group('mid')
    for n in (1, 2, 3, 4, 5):
        d.text(cx - 70, cy - n * h + 2.5, str(n), size=7, anchor='end')
    d.text(cx + x4 + 12, cy - y4 + 2.5, '4: NONE', size=7, anchor='start')
    d.text(cx + 14, cy - 10 * h - 6, '3.4 Å', size=7, anchor='start')
    d.text(xr + 5, base - P * s / 2 + 2.5, '34 Å', size=7, anchor='start')
    d.text(hx, yd - 6, '20 Å', size=7)
    d.text(hx, 24, 'THE HELIX', size=7)
    d.text(cx, 290, 'THE PATTERN · LAYER LINES 1–5', size=7)
    d.text(hx, 290, 'CHAINS ⅜ OF A TURN APART', size=7)
    return d


def meselson_stahl():
    d = D()
    # The bands of Meselson and Stahl's Fig. 4 (PNAS 44, 671, 1958), as microdensitometer peaks over
    # each centrifuge cell, density rising to the right. Band positions: light (N-14) DNA, hybrid
    # halfway (measured at 50 +/- 2 per cent) and heavy (N-15), 0.014 g/cm3 apart. Peak heights are
    # the fractions semiconservative copying predicts in an exponentially growing culture, by our
    # arithmetic: with N = 2^t molecules per original after t generations, heavy (2 - N)/N and hybrid
    # 2(N - 1)/N for t < 1, then hybrid 2/N and light 1 - 2/N. The generations are the paper's samples.
    gens = [0.0, 0.7, 1.0, 1.9, 3.0, 4.1]
    xL, xM, xH = 176, 236, 296
    x0, x1 = 120, 352
    top, row, peak, sig = 44, 36, 20, 5.5

    def fractions(t):
        n = 2 ** t
        if t < 1:
            return {xH: (2 - n) / n, xM: 2 * (n - 1) / n, xL: 0.0}
        return {xH: 0.0, xM: 2 / n, xL: 1 - 2 / n}

    d.group('thin')
    for x in (xL, xM, xH):
        d.line((x, top + 4), (x, top + row * len(gens) - 4))
    d.line((x0, top + row * len(gens) + 6), (x1, top + row * len(gens) + 6))
    _arrow(d, (x0, top + row * len(gens) + 6), (x1, top + row * len(gens) + 6))

    d.group()
    for i, t in enumerate(gens):
        yb = top + i * row + peak + 4                                     # baseline of the tracing
        _box(d, x0, yb + 2, x1 - x0, 6)                                   # the cell, seen edge on
        fr = fractions(t)
        pts = []
        for k in range(0, 117):
            x = x0 + 2 * k
            yv = sum(f * math.exp(-((x - c) ** 2) / (2 * sig ** 2)) for c, f in fr.items())
            pts.append((x, yb - peak * yv))
        d.line(*pts)

    d.group('mid')
    for i, t in enumerate(gens):
        yb = top + i * row + peak + 4
        for c, f in fractions(t).items():
            if f > 0.02:
                d.line((c, yb + 2), (c, yb + 8))                          # the band in the cell

    d.group('mid')
    d.text(60, top - 12, 'GENERATIONS', size=7)
    d.text(60, top - 3, 'IN N-14', size=7)
    for i, t in enumerate(gens):
        d.text(60, top + i * row + peak + 7, f'{t:.1f}', size=7)
    d.text(xL, top - 12, 'LIGHT', size=7)
    d.text(xM, top - 12, 'HYBRID', size=7)
    d.text(xH, top - 12, 'HEAVY', size=7)
    d.text(xL, top - 3, 'N-14', size=7)
    d.text(xM, top - 3, 'HALF', size=7)
    d.text(xH, top - 3, 'N-15', size=7)
    d.text((x0 + x1) / 2, top + row * len(gens) + 18, 'DENSITY IN CsCl · 0.014 g/cm³ LIGHT TO HEAVY', size=7)
    return d


PLATES = {'photo-51': photo_51, 'meselson-stahl': meselson_stahl}
