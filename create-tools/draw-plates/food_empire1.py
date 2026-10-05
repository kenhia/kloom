"""Plates for Daily Bread's part empire1 (sprint 051): Egypt's granaries, Rome's annona, China's
ever-normal granary. See plates_for.py."""
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


def _bedja(cx, rim, a, h, t, up=True, n=28):
    """Outer and inner profiles of a bedja, a thick bell-shaped bread mold with a rounded foot.
    rim is the y of its mouth; up=True opens upward (the foot below), False opens downward."""
    sgn = 1 if up else -1

    def prof(half, depth):
        return [(cx + half * s, rim + sgn * depth * (1 - abs(s) ** 2.2))
                for s in (-1 + 2 * i / n for i in range(n + 1))]

    return prof(a, h), prof(a - t, h - t)


def _draw_bedja(d, cx, rim, a, h, t, up=True):
    outer, inner = _bedja(cx, rim, a, h, t, up)
    d.line(*outer)
    d.line(*inner)
    d.line(outer[0], inner[0])                                         # the rim, wall thickness
    d.line(outer[-1], inner[-1])
    return outer, inner


def egypt_grain():
    d = D()
    # Bread baked in bedja, after AERAGRAM 1 (1996) on the Giza bakeries of 1990-91 and the Old Kingdom
    # tomb reliefs it cites: molds stacked mouth down over an open fire to heat; then set upright in a hollow
    # in the floor, filled with dough, capped with a second mold mouth down, and banked with hot ash.
    # The molds' proportions are schematic (no measured profile is given); the steps are the article's.
    floor = 206
    a, h, t = 32, 36, 6                                                # half-width, depth, wall

    d.group('thin')
    d.line((14, floor), (386, floor))                                  # the bakery floor
    for cx in (74, 142, 300):
        d.line((cx, 50), (cx, floor + 44))                             # axes of the molds
    d.line((205, 40), (205, 262))                                      # between the two steps

    d.group()
    # 1. heating: three molds mouth down, two on hearth stones over the fire, one across them
    stone_y = floor - 12
    for cx in (74, 142):
        _draw_bedja(d, cx, stone_y, a, h, t, up=False)
    _draw_bedja(d, 108, stone_y - h + 4, a, h, t, up=False)
    # 2. baking: a hollow in the floor holding a filled mold, capped by another
    cx, r_h = 300, 40
    d.line(*[(cx + r_h * math.cos(math.radians(th)), floor + 0.95 * r_h * math.sin(math.radians(th)))
             for th in range(0, 181, 6)])
    _draw_bedja(d, cx, floor - 4, a, h, t, up=True)                    # the filled mold, sunk in the hollow
    _draw_bedja(d, cx, floor - 4, a, h, t, up=False)                   # the cap

    d.group('mid')
    for x in (44, 92, 124, 172):                                       # hearth stones
        d.ellipse(x, floor - 6, 9, 6)
    for x0 in range(56, 166, 13):                                      # flames under the stack
        d.line((x0, floor - 2), (x0 + 3, floor - 8), (x0 + 6, floor - 4), (x0 + 9, floor - 11))
    lvl = floor + 6                                                    # the dough, a level in the mold
    d.line((cx - 20, lvl), (cx + 20, lvl))
    for k in range(-3, 4):
        d.line((cx + k * 6 - 2, lvl + 4), (cx + k * 6 + 2, lvl + 8))
    # hot ash banked round the pair, a low mound on each side
    for sgn in (-1, 1):
        mound = [(cx + sgn * (a - 1 + 32 * u), floor - 4 - 30 * (1 - u) ** 1.5) for u in (i / 12 for i in range(13))]
        d.line(*mound)
        for k in range(6):
            u = (k + 0.5) / 6
            d.circle(cx + sgn * (a + 4 + 26 * u), floor - 6 - 18 * (1 - u) ** 1.5 + (k % 2) * 4, 0.8)

    d.group('mid')
    d.line((cx + 16, floor - 36), (cx + 52, floor - 62))
    d.text(cx + 54, floor - 65, 'CAP', size=7, anchor='start')
    d.line((cx + 22, floor + 12), (cx + 62, floor + 34))
    d.text(cx + 64, floor + 37, 'DOUGH', size=7, anchor='start')
    d.line((cx - 52, floor - 14), (cx - 70, floor - 54))
    d.text(cx - 70, floor - 58, 'HOT ASH', size=7)
    d.text(108, 270, '1 · HEAT THE MOLDS MOUTH DOWN', size=7)
    d.text(108, 281, 'OVER AN OPEN FIRE', size=7)
    d.text(300, 270, '2 · FILL, SET IN A HOLLOW,', size=7)
    d.text(300, 281, 'CAP AND BANK WITH ASH', size=7)
    d.text(200, 24, 'BREAD IN BEDJA · THE GIZA BAKERIES · SCHEMATIC', size=7)
    return d


def annona():
    d = D()
    # Trajan's hexagonal basin at Portus in plan, a regular hexagon 358 m on a side (Italian Wikipedia,
    # "Porto (citta antica)"), drawn to the scale bar, with a grain ship of 55 m (Lucian's Isis, the largest
    # reported) to the same scale. The warehouse ring is drawn as a band 60 m deep, and the channel to
    # Claudius's harbor and the canal to the Tiber are placed schematically.
    s = 0.25                                                           # units per meter
    side = 358 * s
    cx, cy = 225, 140

    def hexagon(r):
        return [(cx + r * math.cos(math.radians(60 * i)), cy + r * math.sin(math.radians(60 * i)))
                for i in range(6)]

    inner = hexagon(side)
    outer = hexagon(side + 60 * s / math.cos(math.radians(30)))

    d.group('thin')
    for p in inner:
        d.line((cx, cy), p)                                            # the six radii, equal to the side
    d.circle(cx, cy, side)                                             # the circumscribed circle
    d.circle(cx, cy, side * math.sqrt(3) / 2)                          # the inscribed circle

    d.group()
    d.line(*inner, closed=True)                                        # the quay line of the basin
    d.line(*outer, closed=True)                                        # the back of the warehouses

    d.group('mid')
    for i in range(6):                                                 # warehouse cells: cross walls in the band
        p0, p1, q0, q1 = inner[i], inner[(i + 1) % 6], outer[i], outer[(i + 1) % 6]
        for k in range(1, 9):
            u = k / 9
            d.line((p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u),
                   (q0[0] + (q1[0] - q0[0]) * u, q0[1] + (q1[1] - q0[1]) * u))
    w = outer[3]                                                       # the west corner
    d.line((w[0], w[1] - 6), (w[0] - 70, w[1] - 6))                    # channel to Claudius's harbor
    d.line((w[0], w[1] + 6), (w[0] - 70, w[1] + 6))
    _arrow(d, (w[0] - 40, w[1]), (w[0] - 66, w[1]), size=5)
    d.line((w[0] - 40, w[1]), (w[0] - 66, w[1]))
    m = ((outer[1][0] + outer[2][0]) / 2, (outer[1][1] + outer[2][1]) / 2)   # middle of the south-west side
    d.line((m[0] - 6, m[1] - 4), (m[0] - 22, m[1] + 36))               # canal to the Tiber
    d.line((m[0] + 6, m[1] + 2), (m[0] - 10, m[1] + 42))
    sx, sy, L = cx - 6, cy + 36, 55 * s                               # the ship, 55 m
    d.line((sx - L / 2, sy - 2.5), (sx + L / 2 - 3, sy - 2.5), (sx + L / 2, sy), (sx + L / 2 - 3, sy + 2.5),
           (sx - L / 2, sy + 2.5), closed=True)

    d.group('mid')
    bar_x, bar_y = 290, 278
    d.line((bar_x, bar_y), (bar_x + 200 * s, bar_y))
    for k, hgt in ((0, 4), (1, 3), (2, 4)):
        d.line((bar_x + 100 * s * k, bar_y - hgt), (bar_x + 100 * s * k, bar_y + hgt))
    d.text(bar_x + 200 * s + 6, bar_y + 3, '200 M', size=7, anchor='start')
    d.text(cx, outer[4][1] - 8, 'SIDE 358 M', size=7)
    d.text(cx, cy - 8, 'TRAJAN’S BASIN', size=7)
    d.text(sx, sy + 13, 'GRAIN SHIP, 55 M', size=7)
    d.text(w[0] - 70, w[1] - 24, 'TO CLAUDIUS’S', size=7, anchor='start')
    d.text(w[0] - 70, w[1] - 13, 'HARBOR', size=7, anchor='start')
    d.text(m[0] - 28, m[1] + 42, 'CANAL TO THE TIBER', size=7, anchor='end')
    d.text(382, 52, 'WAREHOUSES', size=7, anchor='end')
    d.text(382, 63, 'SCHEMATIC', size=7, anchor='end')
    d.text(200, 20, 'PORTUS · TRAJAN’S BASIN · EARLY 2ND CENTURY AD', size=7)
    return d


def ever_normal_granary():
    d = D()
    # The rule of the ever-normal granary as a price band: buy when the market price falls below the band,
    # sell when it rises above it, and the granary's stock rises and falls in turn. The prices are invented
    # (a slow wave with a bad year and a glut), not sourced: the rule is the Book of Han's (54 BC).
    x0, x1 = 50, 375
    py0, py1 = 40, 170                                                  # price panel, top and bottom
    sy0, sy1 = 200, 262                                                 # stock panel
    n = 13
    xs = [x0 + 14 + (x1 - x0 - 24) * i / (n - 1) for i in range(n)]
    price = [0.50, 0.36, 0.30, 0.44, 0.55, 0.60, 0.82, 0.92, 0.60, 0.48, 0.30, 0.32, 0.50]
    lo, hi = 0.40, 0.68                                                 # the band

    def yp(v):
        return py1 - (py1 - py0) * v

    d.group('thin')
    d.line((x0, py0), (x0, py1), (x1, py1))
    d.line((x0, sy0), (x0, sy1), (x1, sy1))
    for x in xs:
        d.line((x, py1), (x, py1 + 3))
    d.dashed((x0, yp(lo)), (x1, yp(lo)), dash=5, gap=3)
    d.dashed((x0, yp(hi)), (x1, yp(hi)), dash=5, gap=3)

    d.group()
    pts = [(x, yp(v)) for x, v in zip(xs, price)]
    d.line(*pts)                                                        # the market price, invented
    stock, s = [], 0.30
    for v in price:
        if v < lo:
            s += (lo - v) * 1.5
        elif v > hi:
            s -= (v - hi) * 1.5
        stock.append(max(0.05, min(1.0, s)))
    bw = 14
    for x, v in zip(xs, stock):
        _box(d, x - bw / 2, sy1 - (sy1 - sy0) * v, bw, (sy1 - sy0) * v)  # the granary's stock

    d.group('mid')
    for (x, y), v in zip(pts, price):
        if v < lo:                                                      # buy: grain goes into store
            d.circle(x, y, 3)
            d.line((x, y + 6), (x, sy0 - 6))
            _arrow(d, (x, y + 6), (x, sy0 - 6), size=4)
        elif v > hi:                                                    # sell: grain comes out
            d.circle(x, y, 3)
            d.line((x, sy0 - 6), (x, y + 6))
            _arrow(d, (x, sy0 - 6), (x, y + 6), size=4)

    d.group('mid')
    d.text(x0 + 8, yp(hi) - 5, 'CEILING · SELL', size=7, anchor='start')
    d.text(xs[4] - 6, yp(lo) + 11, 'FLOOR · BUY', size=7, anchor='start')
    d.text(x0 - 6, yp(1) + 3, 'DEAR', size=7, anchor='end')
    d.text(x0 - 6, py1, 'CHEAP', size=7, anchor='end')
    d.text(x0 - 6, sy0 + 3, 'STORE', size=7, anchor='end')
    d.text((x0 + x1) / 2, sy1 + 14, 'YEARS · PRICES INVENTED, RULE OF 54 BC', size=7)
    d.text((x0 + x1) / 2, 22, 'THE EVER-NORMAL GRANARY · BUY CHEAP, SELL DEAR', size=7)
    return d


PLATES = {'egypt-grain': egypt_grain, 'annona': annona, 'ever-normal-granary': ever_normal_granary}
