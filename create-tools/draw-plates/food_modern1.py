"""Plates for Daily Bread's part modern1 (sprint 051): fertilizer, vitamins, tractor. See plates_for.py.

Run as a script to write the tractor frame's line chart of horses and mules against tractors.
"""
import math
import os
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def fertilizer():
    d = D()
    # Liebig's barrel in elevation: the staves are the nutrients, and the barrel holds water only up to the
    # shortest. The barrel's bulge is a sine profile; each stave edge is drawn at its angle round the barrel, so
    # the staves foreshorten towards the sides. The stave heights are schematic, with nitrogen the shortest.
    cx, yb, yt = 150, 255, 95                                             # centre, base, nominal top

    def radius(y):
        t = (yb - y) / (yb - yt)
        return 50 + 16 * math.sin(math.pi * t)

    def x_at(theta, y):
        return cx + radius(y) * math.sin(math.radians(theta))

    edges = [-90 + 20 * j for j in range(10)]                             # 9 staves across the front
    tops = [120, 104, 128, 110, 178, 100, 122, 108, 134]
    names = [None, 'K', 'MG', 'P', 'N', 'H2O', 'CA', 'S', None]
    level = tops[4]

    d.group('thin')
    d.line((cx, 60), (cx, yb + 18))                                       # axis
    d.line((40, yb + 8), (390, yb + 8))                                   # ground
    d.line((cx - 80, level), (392, level))                                # the level
    for side in (-1, 1):                                                  # the bulge's profile
        d.line(*[(cx + side * radius(y), y) for y in range(yt - 10, yb + 1, 5)])

    d.group()
    for j, th in enumerate(edges):                                        # stave edges
        if j == 0:
            top = tops[0]
        elif j == 9:
            top = tops[8]
        else:
            top = min(tops[j - 1], tops[j])
        d.line(*[(x_at(th, y), y) for y in range(yb, top - 1, -4)] + [(x_at(th, top), top)])
    for i in range(9):                                                    # stave tops
        d.line((x_at(edges[i], tops[i]), tops[i]), (x_at(edges[i + 1], tops[i]), tops[i]))
    d.line(*[(x_at(th, yb), yb + 6 * math.cos(math.radians(th))) for th in range(-90, 91, 6)])

    d.group('mid')
    for yh in (238, 205):                                                 # hoops
        d.line(*[(x_at(th, yh), yh + 6 * math.cos(math.radians(th))) for th in range(-90, 91, 6)])
    for k in range(4):                                                    # water spilling over N
        x0 = cx - 9 + 6 * k
        d.line(*[(x0 + (x0 - cx) * 0.25 * t, level + 2 + 30 * t + 3 * math.sin(4 * t)) for t in
                 [i / 8 for i in range(9)]])

    d.group('mid')
    for i, name in enumerate(names):
        if name:
            xm = (x_at(edges[i], tops[i]) + x_at(edges[i + 1], tops[i])) / 2
            d.text(xm, tops[i] - 5, name, size=7)
    d.text(300, level - 6, 'WATER STOPS AT THE SHORTEST', size=7)
    d.text(300, level + 12, 'NITROGEN, FOR MOST CROPS', size=7)
    d.text(300, 120, 'LIEBIG\'S LAW OF THE MINIMUM', size=7)
    d.text(cx, 284, 'THE BARREL OF NUTRIENTS · SCHEMATIC', size=7)
    return d


def _ellipse_pts(cx, cy, rx, ry, a0=0, a1=360, step=6):
    return [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
            for a in range(a0, a1 + 1, step)]


def vitamins():
    d = D()
    # A grain of rice cut lengthwise, before and after milling. Whole (brown) rice keeps its bran layers, the
    # pericarp and aleurone that Eijkman called the "silver skin", and its germ; polishing removes both and leaves
    # the starchy endosperm. Proportions are schematic: the bran layers are drawn far thicker than life.
    cy = 132
    lx, rx_ = 108, 296
    a, b = 70, 30                                                         # outer grain
    t = 6                                                                 # bran thickness, exaggerated
    germ = (lx - a + 13, cy + 10)

    d.group('thin')
    d.line((20, cy), (385, cy))                                           # long axis
    for x in (lx, rx_):
        d.line((x, cy - b - 16), (x, cy + b + 16))

    d.group()
    d.line(*_ellipse_pts(lx, cy, a, b))                                   # whole grain
    d.line(*_ellipse_pts(lx, cy, a - t, b - t))                           # bran / endosperm boundary
    d.ellipse(germ[0], germ[1], 11, 13)                                   # germ, at the base

    d.group()
    # the polished grain: endosperm only, with the hollow the germ left
    pts = []
    for ang in range(0, 361, 4):
        x = rx_ + (a - t) * math.cos(math.radians(ang))
        y = cy + (b - t) * math.sin(math.radians(ang))
        gx, gy = rx_ - a + 13, cy + 10
        if (x - gx) ** 2 / 11 ** 2 + (y - gy) ** 2 / 13 ** 2 < 1:        # inside where the germ was
            continue
        pts.append((x, y))
    # close the hollow with the germ's own outline
    start, end = pts[-1], pts[0]
    hollow = [(rx_ - a + 13 + 11 * math.cos(math.radians(u)), cy + 10 + 13 * math.sin(math.radians(u)))
              for u in range(-70, 71, 10)]
    hollow = [p for p in hollow if (p[0] - rx_) ** 2 / (a - t) ** 2 + (p[1] - cy) ** 2 / (b - t) ** 2 <= 1.0]
    d.line(*pts)
    d.line(*hollow)

    d.group('mid')
    for cxg in (lx, rx_):                                                 # starch cells of the endosperm
        for i in range(-3, 4):
            for j in range(-1, 2):
                x, y = cxg + 14 * i + (7 if j % 2 else 0), cy + 12 * j
                if (x - cxg) ** 2 / (a - t - 8) ** 2 + (y - cy) ** 2 / (b - t - 6) ** 2 < 1:
                    d.line(*[(x + 5 * math.cos(math.radians(k)), y + 5 * math.sin(math.radians(k)))
                             for k in range(30, 391, 60)])
    d.line((lx + a + 12, cy - 4), (rx_ - a - 6, cy - 4))                  # milling arrow
    _arrow(d, (lx + a + 12, cy - 4), (rx_ - a - 6, cy - 4))
    for k in range(5):                                                    # bran flakes falling away
        x = lx + a + 18 + 6 * k
        d.line((x, cy + 8 + 5 * k), (x + 3, cy + 12 + 5 * k))

    d.group('mid')
    d.text(lx, cy - b - 24, 'WHOLE RICE', size=7)
    d.text(rx_, cy - b - 24, 'POLISHED RICE', size=7)
    d.text(lx + 24, cy - b - 6, 'SILVER SKIN', size=7)
    d.line((lx + 24, cy - b - 3), (lx + 20, cy - b + 3))
    d.text(germ[0] - 4, cy + b + 22, 'GERM', size=7)
    d.line((germ[0] - 4, cy + b + 14), (germ[0], germ[1] + 13))
    d.text(rx_ + 14, cy + b + 22, 'ENDOSPERM, MOSTLY STARCH', size=7)
    d.text((lx + rx_) / 2 + 2, cy - 12, 'MILLING', size=7)
    d.text(lx, 238, 'HENS STAYED WELL', size=7)
    d.text(rx_, 238, 'HENS FELL ILL IN 3–4 WEEKS', size=7)
    d.text(200, 272, 'A GRAIN OF RICE IN SECTION · BATAVIA, 1890s', size=7)
    return d


def _intersect(p1, p2, p3, p4):
    """Where the line p1-p2 meets the line p3-p4."""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def tractor():
    d = D()
    # Ferguson's three-point hitch in side elevation, schematic. Two lower links and a top link join the plow to
    # the tractor; the lines of the links, extended forward, meet near the front axle, so the plow pulls as if
    # hitched there, and its draft presses the rear wheels down instead of lifting the front. The meeting point is
    # computed from the link ends drawn here.
    ground = 262
    rw, rr = (150, ground - 62), 62                                       # rear wheel
    fw, fr = (52, ground - 26), 26                                        # front wheel
    L1, L2 = (220, 236), (292, 246)                                       # lower link: tractor end, plow end
    T1, T2 = (214, 182), (296, 168)                                       # top link
    meet = _intersect(L1, L2, T1, T2)

    d.group('thin')
    d.line((10, ground), (390, ground))
    d.dashed(L1, meet, dash=5, gap=3)
    d.dashed(T1, meet, dash=5, gap=3)
    d.line((rw[0], rw[1] - rr - 8), (rw[0], ground + 6))
    d.line((fw[0], fw[1] - fr - 8), (fw[0], ground + 6))

    d.group()
    d.circle(rw[0], rw[1], rr)                                            # rear wheel
    d.circle(rw[0], rw[1], 14)
    d.circle(fw[0], fw[1], fr)                                            # front wheel
    d.circle(fw[0], fw[1], 7)
    d.line((fw[0] - 22, 170), (fw[0] - 22, 204), (rw[0] - 64, 204), (rw[0] - 64, 170), closed=True)  # engine
    d.line((rw[0] - 64, 176), (rw[0] - 36, 164), (rw[0] + 30, 160))     # body over the wheel
    d.line((rw[0] + 6, 150), (rw[0] + 36, 150))                           # seat
    d.line((rw[0] + 20, 150), (rw[0] + 30, 160))
    d.line(L1, L2)                                                        # lower link
    d.line(T1, T2)                                                        # top link
    d.line((rw[0], rw[1]), L1)                                             # link mounts
    d.line((rw[0] + 30, 160), T1)
    # the plow: a mast on the links' ends, a beam, a share below ground
    d.line(T2, L2, (318, 252), (330, ground + 22), (352, ground + 22))
    d.line(T2, (318, 252))

    d.group('mid')
    d.line((rw[0] + 40, 158), (rw[0] + 92, 150))                          # hydraulic lift arm
    d.line((rw[0] + 92, 150), ((L1[0] + L2[0]) / 2, (L1[1] + L2[1]) / 2))   # lift rod
    d.circle(meet[0], meet[1], 3)
    p_from = (330, ground + 22)                                           # the plow's pull, along the links
    p_to = (p_from[0] - 0.42 * (p_from[0] - meet[0]), p_from[1] - 0.42 * (p_from[1] - meet[1]))
    d.line(p_from, p_to)
    _arrow(d, p_from, p_to)
    d.line((rw[0], ground - 28), (rw[0], ground - 4))                     # load on the rear wheel
    _arrow(d, (rw[0], ground - 28), (rw[0], ground - 4))
    for k in range(9):                                                    # soil
        x = 236 + 16 * k
        d.line((x, ground + 4), (x - 6, ground + 12))

    d.group('mid')
    d.text(T2[0] - 10, T2[1] - 30, 'TOP LINK SENSES THE DRAFT', size=7, anchor='middle')
    d.text(L2[0] + 34, L2[1] - 14, 'LOWER LINKS', size=7, anchor='start')
    d.text(meet[0], meet[1] - 44, 'LINES MEET', size=7, anchor='middle')
    d.line((meet[0], meet[1] - 38), (meet[0], meet[1] - 6))
    d.text(366, ground + 34, 'PLOW', size=7)
    d.text(rw[0] - 30, ground + 18, 'MORE WEIGHT ON THE REAR WHEELS', size=7, anchor='middle')
    d.text(200, 22, 'THREE-POINT HITCH · SIDE ELEVATION · SCHEMATIC', size=7)
    return d


PLATES = {'fertilizer': fertilizer, 'vitamins': vitamins, 'tractor': tractor}


# The tractor frame's chart -------------------------------------------------------------------------------------

# Horses and mules on farms (Series K 570, K 572) and tractors on farms (K 184), thousands, Historical Statistics
# of the United States, Colonial Times to 1970, pp. 469 and 519. From 1951 the horse series counts horses and
# mules together, and the mule series stops.
HORSES = {1910: 19972, 1915: 21431, 1918: 21238, 1920: 20091, 1925: 16651, 1930: 13742, 1935: 11861,
          1940: 10444, 1945: 8715, 1950: 5548, 1955: 4309, 1960: 3089}
MULES = {1910: 4239, 1915: 5062, 1918: 5485, 1920: 5651, 1925: 5918, 1930: 5382, 1935: 4822, 1940: 4034,
         1945: 3235, 1950: 2233, 1955: 0, 1960: 0}
TRACTORS = {1910: 1, 1915: 25, 1918: 85, 1920: 246, 1925: 549, 1930: 920, 1935: 1048, 1940: 1567, 1945: 2354,
            1950: 3394, 1955: 4345, 1960: 4685}


def horses_tractors_chart():
    w, h = 520, 300
    x0, x1, y0, y1 = 64, 500, 250, 40
    vmax = 30

    def px(year):
        return x0 + (x1 - x0) * (year - 1910) / 50

    def py(millions):
        return y0 - (y0 - y1) * millions / vmax

    years = sorted(HORSES)
    animals = [(y, (HORSES[y] + MULES[y]) / 1000) for y in years]
    tractors = [(y, TRACTORS[y] / 1000) for y in years]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">',
           '<title id="t">Horses and mules against tractors on American farms, 1910 to 1960</title>',
           '<desc id="d">Line chart, in millions. Horses and mules: 24.2 in 1910, 26.5 in 1915, a peak of 26.7 in '
           '1918, 25.7 in 1920, 22.6 in 1925, 19.1 in 1930, 16.7 in 1935, 14.5 in 1940, 12.0 in 1945, 7.8 in 1950, '
           '4.3 in 1955 and 3.1 in 1960. Tractors: about 0.001 in 1910, 0.03 in 1915, 0.25 in 1920, 0.55 in 1925, '
           '0.92 in 1930, 1.05 in 1935, 1.57 in 1940, 2.35 in 1945, 3.39 in 1950, 4.35 in 1955 and 4.69 in 1960. '
           'Data: Historical Statistics of the United States, Colonial Times to 1970, series K 184, K 570 and '
           'K 572.</desc>',
           '<g font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="currentColor">',
           '<g class="muted">']
    for v in range(0, vmax + 1, 10):
        op, sw = ('0.9', '1') if v == 0 else ('0.3', '0.6')
        out.append(f'<line x1="{x0}" x2="{x1}" y1="{py(v):.1f}" y2="{py(v):.1f}" stroke="currentColor" '
                   f'stroke-opacity="{op}" stroke-width="{sw}"/>')
        out.append(f'<text x="{x0 - 8}" y="{py(v) + 4:.1f}" text-anchor="end">{v}</text>')
    for yr in range(1910, 1961, 10):
        out.append(f'<line x1="{px(yr):.1f}" x2="{px(yr):.1f}" y1="{y0}" y2="{y0 + 4}" stroke="currentColor" '
                   'stroke-width="1"/>')
        out.append(f'<text x="{px(yr):.1f}" y="{y0 + 17}" text-anchor="middle">{yr}</text>')
    out.append(f'<text x="{x0 - 8}" y="26" text-anchor="end">million</text>')
    out.append('<text x="260" y="22" text-anchor="middle">HORSES AND MULES · TRACTORS · US FARMS</text>')
    out.append('</g>')

    def poly(pts, cls):
        s = ' '.join(f'{px(y):.1f},{py(v):.1f}' for y, v in pts)
        c = f' class="{cls}"' if cls else ''
        return f'<polyline{c} points="{s}" fill="none" stroke="currentColor" stroke-width="2"/>'

    out.append(poly(animals, None))
    for y, v in animals:
        out.append(f'<circle cx="{px(y):.1f}" cy="{py(v):.1f}" r="2.5"/>')
    out.append('<g class="accent">')
    out.append(poly(tractors, None))
    for y, v in tractors:
        out.append(f'<circle cx="{px(y):.1f}" cy="{py(v):.1f}" r="2.5"/>')
    out.append(f'<text x="{px(1934):.1f}" y="{py(3.4):.1f}" text-anchor="middle">tractors</text>')
    out.append('</g>')
    out.append(f'<text x="{px(1925) + 4:.1f}" y="{py(25.5):.1f}" text-anchor="start">horses and mules</text>')
    out.append(f'<text x="{px(1918):.1f}" y="{py(26.7) - 8:.1f}" text-anchor="middle">26.7</text>')
    out.append(f'<text x="{px(1960):.1f}" y="{py(4.69) - 8:.1f}" text-anchor="end">4.7</text>')
    out.append('</g>')
    out.append('</svg>')
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, '..', '..', 'subjects', 'food', 'frames', 'tractor', 'horses-tractors.svg')
    with open(path, 'w') as fh:
        fh.write(horses_tractors_chart())
    print('wrote', os.path.normpath(path))
