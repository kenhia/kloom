"""Plates for The Story of Life's germ2 part (sprint 055): Ross's malaria cycle, the porcelain filter.
See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def _on(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def _rod(d, x, y, ang, length=7, w=2.2):
    """A bacterium drawn as a capsule: two sides and rounded ends, centered on (x, y)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    h = length / 2
    p1 = (x - ux * h + nx * w, y - uy * h + ny * w)
    p2 = (x + ux * h + nx * w, y + uy * h + ny * w)
    p3 = (x + ux * h - nx * w, y + uy * h - ny * w)
    p4 = (x - ux * h - nx * w, y - uy * h - ny * w)
    end1 = [(x + ux * h + w * math.cos(a + math.pi / 2 - t), y + uy * h + w * math.sin(a + math.pi / 2 - t))
            for t in [k * math.pi / 6 for k in range(7)]]
    end2 = [(x - ux * h + w * math.cos(a - math.pi / 2 - t), y - uy * h + w * math.sin(a - math.pi / 2 - t))
            for t in [k * math.pi / 6 for k in range(7)]]
    d.line(p1, p2, *end1[1:-1], p3, p4, *end2[1:-1], closed=True)


def ross_malaria():
    d = D()
    # The malaria parasite's cycle as a loop between its two hosts, after Ross's Nobel lecture
    # (1902) and the liver stage found in 1948: the human half on the left, the mosquito's on the right. Stages sit on a circle at
    # computed angles; the arcs between them carry the arrows. Each stage is a schematic glyph.
    cx, cy, r = 200, 150, 92
    stages = [  # angle (degrees, y down), key
        (-118, 'liver'), (-158, 'ring'), (162, 'schizont'), (122, 'crescent'),
        (58, 'gametes'), (18, 'zygote'), (-22, 'oocyst'), (-62, 'gland')]
    gap = 13                                                             # degrees kept clear round a glyph
    order = [a for a, _ in stages]

    d.group('thin')
    d.circle(cx, cy, r)
    d.dashed((cx, 34), (cx, 266), dash=3, gap=3)
    for a in order:
        p, q = _on(cx, cy, r - 6, a), _on(cx, cy, r + 6, a)
        d.line(p, q)
    d.circle(cx, cy, 3)

    d.group()
    # arcs, run from each stage to the next round the loop: down the left side, up the right
    seq = order + [order[0] + 360 * 0]                                   # liver ... gland, then back to liver
    path = [-118, -158, -198, -238, -302, -342, -382, -422, -478]        # the same angles, made monotonic
    for a0, a1 in zip(path, path[1:]):
        s, e = a0 - gap, a1 + gap
        pts = [_on(cx, cy, r, s + (e - s) * k / 24) for k in range(25)]
        d.line(*pts)
        _arrow(d, pts[-2], pts[-1], size=5)
    # the repeated round in the blood: ring to schizont and back, an inner loop
    ib = [_on(cx - 40, cy, 26, 200 + k * 13) for k in range(26)]
    d.line(*ib)
    _arrow(d, ib[-2], ib[-1], size=4)

    d.group('mid')
    g = {k: _on(cx, cy, r, a) for a, k in stages}
    x, y = g['liver']                                                    # a liver cell, hexagonal
    d.line(*[(x + 9 * math.cos(math.radians(30 + 60 * k)), y + 9 * math.sin(math.radians(30 + 60 * k)))
             for k in range(6)], closed=True)
    for k in range(5):
        d.circle(x - 4 + 2 * k, y + (k % 2) * 2 - 1, 0.8)
    x, y = g['ring']                                                     # a red cell with a ring stage
    d.circle(x, y, 9)
    d.circle(x + 2, y - 1, 3.2)
    x, y = g['schizont']                                                 # a red cell full of merozoites
    d.circle(x, y, 9)
    for k in range(8):
        d.circle(*_on(x, y, 5, k * 45), 1.3)
    x, y = g['crescent']                                                 # Laveran's crescent
    d.arc(x, y, 9, 200, 340)
    d.arc(x, y + 9, 13, 225, 315)
    d.line(_on(x, y, 9, 200), _on(x, y + 9, 13, 225))
    d.line(_on(x, y, 9, 340), _on(x, y + 9, 13, 315))
    for k in range(3):
        d.circle(x - 3 + 3 * k, y - 4.5, 0.8)
    x, y = g['gametes']                                                  # a male cell throwing out filaments
    d.circle(x, y, 5)
    for k in range(5):
        a = math.radians(30 + 72 * k)
        pts = [(x + (5 + t) * math.cos(a) + 1.8 * math.sin(t / 2) * -math.sin(a),
                y + (5 + t) * math.sin(a) + 1.8 * math.sin(t / 2) * math.cos(a)) for t in range(0, 11, 2)]
        d.line(*pts)
    x, y = g['zygote']                                                   # the moving zygote, elongated
    d.ellipse(x, y, 10, 4)
    d.circle(x + 3, y, 1.5)
    x, y = g['oocyst']                                                   # the pigmented cell on the stomach wall
    d.line((x - 13, y + 9), (x + 13, y + 9))
    d.line((x - 13, y + 12), (x + 13, y + 12))
    d.circle(x, y + 1, 8)
    for k in range(6):
        d.circle(*_on(x, y + 1, 4, k * 60 + 15), 0.9)
    x, y = g['gland']                                                    # a lobe of the salivary gland, threads within
    d.ellipse(x, y, 7, 10)
    for k in range(5):
        d.line((x - 4 + 2 * k, y - 6), (x - 2 + 2 * k, y + 6))

    d.group('mid')
    lab = {
        'liver': ('LIVER', 'FOUND 1948'),
        'ring': ('RED CELL', ''),
        'schizont': ('DIVIDES', 'BURSTS'),
        'crescent': ('CRESCENT', 'LAVERAN 1880'),
        'gametes': ('SEXES MEET', 'IN STOMACH'),
        'zygote': ('ZYGOTE', ''),
        'oocyst': ('PIGMENTED CELL', '20 AUG 1897'),
        'gland': ('SALIVARY GLAND', 'JULY 1898'),
    }
    for a, k in stages:
        x, y = _on(cx, cy, r + 17, a)
        anchor = 'start' if math.cos(math.radians(a)) > 0 else 'end'
        top, bottom = lab[k]
        y0 = y - 1 if bottom else y + 2.5
        d.text(x, y0, top, size=7, anchor=anchor)
        if bottom:
            d.text(x, y0 + 9, bottom, size=7, anchor=anchor)
    d.text(cx, 28, 'BITE', size=7)
    d.text(cx, 280, 'MOSQUITO FEEDS', size=7)
    d.text(cx - 40, cy + 3, 'BLOOD', size=7)
    d.text(24, 28, 'HUMAN', size=7, anchor='start')
    d.text(376, 28, 'MOSQUITO', size=7, anchor='end')
    d.text(200, 294, "THE MALARIA PARASITE'S CYCLE, AS KNOWN NOW", size=7)
    return d


def virus():
    d = D()
    # A Chamberland filter in section, schematic: sap pressed in round an unglazed porcelain candle;
    # bacteria held on its outer face, the infectious agent passing the wall into the bore and out to
    # the filtrate, which still gives a healthy leaf the mosaic. Inset: the wall magnified.
    vx0, vx1, vy0, vy1 = 40, 160, 46, 196                                # the pressure vessel
    cx0, cx1, ix0, ix1 = 82, 118, 92, 108                                 # candle outer and bore
    ctop, cbot = 70, 214
    icx, icy, ir = 268, 104, 62                                          # the inset

    d.group('thin')
    d.line((100, 30), (100, 240))                                        # the candle's axis
    for y in (vy0, vy1):
        d.line((vx0 - 8, y), (vx0 - 2, y))
    d.circle(icx, icy, ir)
    d.line((cx1 + 2, 120), _on(icx, icy, ir, 160))                       # leader to the inset
    d.line((cx1 + 2, 140), _on(icx, icy, ir, 135))
    for k in range(5):                                                    # sap level hatching
        d.line((vx0 + 4, vy0 + 12 + k * 3), (cx0 - 4, vy0 + 12 + k * 3))

    d.group()
    d.line((vx0, vy0), (vx0, vy1), (cx0, vy1))                           # vessel walls
    d.line((cx1, vy1), (vx1, vy1), (vx1, vy0))
    d.line((vx0 - 4, vy0), (vx1 + 4, vy0))                               # the lid
    d.line((70, vy0), (70, 30), (40, 30))                                # inlet pipe
    # the candle: outer wall closed at the top with a round end, the bore likewise
    d.line((cx0, cbot), (cx0, ctop + 18))
    d.arc(100, ctop + 18, 18, 180, 360)
    d.line((cx1, ctop + 18), (cx1, cbot))
    d.line((ix0, cbot + 18), (ix0, ctop + 26))
    d.arc(100, ctop + 26, 8, 180, 360)
    d.line((ix1, ctop + 26), (ix1, cbot + 18))
    d.line((cx0, cbot), (ix0, cbot))
    d.line((cx1, cbot), (ix1, cbot))
    # the receiving flask
    fy = 238
    d.line((ix0 - 2, fy), (ix0 - 2, fy + 12), (70, 292), (130, 292), (ix1 + 2, fy + 12), (ix1 + 2, fy))
    # the inset: the porcelain wall as a band crossed by winding channels
    wy0, wy1 = icy - 14, icy + 14
    left = icx - ir
    d.line(_on(icx, icy, ir, 180 + math.degrees(math.asin(14 / ir))), _on(icx, icy, ir, -math.degrees(math.asin(14 / ir))))
    d.line(_on(icx, icy, ir, 180 - math.degrees(math.asin(14 / ir))), _on(icx, icy, ir, math.degrees(math.asin(14 / ir))))
    # a leaf, mottled, fed by the filtrate
    lx, ly = 300, 246
    pts = []
    for k in range(25):
        t = k / 24
        w = math.sin(math.pi * t) * 20 * (1 - 0.25 * t)
        pts.append((lx - 46 + 92 * t, ly - w))
    back = [(lx - 46 + 92 * (k / 24), ly + math.sin(math.pi * k / 24) * 18) for k in range(24, -1, -1)]
    d.line(*pts, *back, closed=True)
    d.line((lx - 58, ly + 4), (lx - 46, ly), (lx + 46, ly))

    d.group('mid')
    for k in range(7):                                                    # channels through the wall
        x = icx - 42 + k * 14
        d.line(*[(x + 3 * math.sin(j * 1.3 + k), wy1 - j * 4) for j in range(8)])
    import random
    rng = random.Random(1898)
    for k in range(9):                                                    # bacteria in the sap
        _rod(d, rng.uniform(vx0 + 10, cx0 - 8), rng.uniform(vy0 + 34, vy1 - 10), rng.uniform(0, 180))
    for k in range(4):
        _rod(d, rng.uniform(cx1 + 8, vx1 - 10), rng.uniform(vy0 + 34, vy1 - 10), rng.uniform(0, 180))
    for y in range(96, 196, 16):                                          # bacteria held on the candle's face
        _rod(d, cx0 - 4, y, 90, length=6, w=1.8)
        _rod(d, cx1 + 4, y + 8, 90, length=6, w=1.8)
    for k in range(6):                                                    # bacteria held at the inset's face
        _rod(d, icx - 38 + k * 15, wy1 + 9, rng.uniform(-20, 20) + (90 if k % 2 else 0), length=9, w=2.6)
    for k in range(18):                                                   # the agent: dots, everywhere it goes
        d.circle(rng.uniform(vx0 + 8, cx0 - 6), rng.uniform(vy0 + 30, vy1 - 6), 0.7)
    for y in range(110, 230, 10):
        d.circle(100 + rng.uniform(-4, 4), y, 0.7)
    for k in range(10):
        d.circle(rng.uniform(80, 120), rng.uniform(268, 288), 0.7)
    for k in range(7):
        x = icx - 42 + k * 14
        d.circle(x + 2, wy1 + 4, 0.8)
        d.circle(x - 1, wy0 - 6, 0.8)
        d.circle(x + 3, icy, 0.8)
    for k in range(9):                                                    # the mosaic on the leaf
        d.circle(lx - 34 + k * 8.5, ly - 6 + 9 * ((k * 7) % 3) / 2, 2.6 + (k % 3))
    d.line((ix1 + 8, fy + 30), (lx - 64, ly + 4))
    _arrow(d, (ix1 + 8, fy + 30), (lx - 64, ly + 4), size=5)
    _arrow(d, (70, 38), (70, vy0 - 2), size=4)

    d.group('mid')
    d.text(40, 24, 'SAP, UNDER PRESSURE', size=7, anchor='start')
    d.text(vx1 + 6, 208, 'PORCELAIN CANDLE', size=7, anchor='start')
    d.text(icx, icy - ir - 6, 'THE WALL, MAGNIFIED', size=7)
    d.text(icx, icy + ir + 11, 'BACTERIA HELD · AGENT PASSES', size=7)
    d.text(140, 290, 'FILTRATE', size=7, anchor='start')
    d.text(lx, ly + 34, 'STILL INFECTIOUS', size=7)
    d.text(lx + 52, ly + 3, 'LEAF', size=7, anchor='start')
    return d


PLATES = {'ross-malaria': ross_malaria, 'virus': virus}
