"""Plates for Sound and Score's frames written by hand in sprint 058. See plates_for.py."""
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


def hohle_fels_flute():
    d = D()
    # The vulture-bone flute in plan, to scale: 218 mm preserved, about 8 mm across, at 1.3 px a mm.
    # The hole positions and the bone's swell are schematic (the paper's measured drawing is not
    # public); the count, the two V notches at the blown end and the broken far end are the find's.
    s = 1.3
    x0, y0, L = 30, 104, 218 * s
    def r(t):                      # half-width along the bone: an ulna-like taper, swelling at both ends
        return (4.0 + 1.6 * math.exp(-((t - 0.0) / 0.08) ** 2) + 1.2 * math.exp(-((t - 1.0) / 0.1) ** 2)) * s
    ts = [i / 60 for i in range(61)]
    top = [(x0 + t * L, y0 - r(t)) for t in ts]
    bot = [(x0 + t * L, y0 + r(t)) for t in ts]
    holes = [0.36, 0.47, 0.58, 0.69, 0.80]
    missing = 2.5 * 25.4 * s     # "two or three inches are missing"

    d.group('thin')
    d.line((x0, y0), (x0 + L + missing, y0))                                   # axis
    for t in holes:
        x = x0 + t * L
        d.line((x, y0 - 22), (x, y0 + 22))
    d.line((x0, y0 + 30), (x0, y0 + 44)); d.line((x0 + L, y0 + 30), (x0 + L, y0 + 44))
    d.line((x0, y0 + 38), (x0 + L, y0 + 38))
    _arrow(d, (x0 + 20, y0 + 38), (x0, y0 + 38), 4); _arrow(d, (x0 + L - 20, y0 + 38), (x0 + L, y0 + 38), 4)

    d.group()
    d.line(*top); d.line(*bot)
    # the blown end with its two V notches, the far end a break
    d.line(top[0], (x0 + 7, y0 - 1.5), (x0, y0), (x0 + 7, y0 + 1.5), bot[0])
    jag = [(x0 + L, y0 - r(1)), (x0 + L - 3, y0 - 3), (x0 + L + 2, y0), (x0 + L - 2, y0 + 3), (x0 + L, y0 + r(1))]
    d.line(*jag)
    for t in holes:
        d.ellipse(x0 + t * L, y0, 2.4, 1.7)

    d.group('mid')
    d.dashed((x0 + L, y0 - r(1)), (x0 + L + missing, y0 - 4.5), (x0 + L + missing, y0 + 4.5), (x0 + L, y0 + r(1)), dash=3, gap=3)
    for t in holes:                                                         # the fine lines around each hole
        x = x0 + t * L
        for dx in (-5, 5):
            d.line((x + dx, y0 - r(t) + 0.5), (x + dx, y0 - r(t) + 2.5))

    # below: the ivory flute's making, in section: a tusk split, hollowed and rejoined
    cy = 214
    d.group('thin')
    for cx in (70, 200, 330):
        d.line((cx - 40, cy), (cx + 40, cy))
    d.group()
    d.circle(70, cy, 26)                                                     # 1 the rod of ivory
    d.line((44, cy), (96, cy))
    for cx, gap in ((200, 7),):                                              # 2 split and hollowed halves
        d.arc(cx, cy - gap, 26, 180, 360); d.line((cx - 26, cy - gap), (cx + 26, cy - gap))
        d.arc(cx, cy - gap, 16, 180, 360)
        d.arc(cx, cy + gap, 26, 0, 180); d.line((cx - 26, cy + gap), (cx + 26, cy + gap))
        d.arc(cx, cy + gap, 16, 0, 180)
    d.circle(330, cy, 26); d.circle(330, cy, 16)                             # 3 rejoined, a bore
    d.group('mid')
    d.line((304, cy), (314, cy)); d.line((346, cy), (356, cy))               # the seam
    for a, b in (((112, cy), (158, cy)), ((242, cy), (288, cy))):
        d.line(a, b); _arrow(d, a, b)

    d.group('mid')
    d.text(x0, 62, 'BLOWN END · TWO V NOTCHES', size=7, anchor='start')
    d.text(x0 + L + 4, 62, 'BROKEN END', size=7, anchor='middle')
    d.text(x0 + (holes[0] + holes[-1]) / 2 * L, y0 - 28, 'FIVE FINGER HOLES', size=7)
    d.text(x0 + L / 2, y0 + 52, '218 MM PRESERVED · ABOUT 8 MM ACROSS', size=7)
    d.text(x0 + L + missing / 2, y0 + 22, 'MISSING', size=7)
    d.text(70, 258, 'IVORY ROD', size=7)
    d.text(200, 258, 'SPLIT · HOLLOWED', size=7)
    d.text(330, 258, 'REJOINED', size=7)
    d.text(200, 286, 'GRIFFON VULTURE RADIUS · HOHLE FELS · SCHEMATIC', size=7)
    return d


def lyres_of_ur():
    d = D()
    # The Queen's Lyre in side elevation, from the British Museum's dimensions: 112.5 cm high, the
    # top bar 95.5 cm, the sound box 73 cm long, at 2.2 px a cm. The arms' lean and the head are
    # schematic; the eleven strings run from the bar to a holder on the box, as a box lyre's do.
    k = 2.0
    bx0, by0 = 150, 248                         # sound box: front-bottom corner at (bx0, by0)
    blen, bh = 73 * k * 0.95, 30 * k            # box drawn a touch shorter so the head fits
    top_y = by0 - 112.5 * k + 12
    back = (bx0 + blen, by0)
    d.group('thin')
    d.line((20, by0), (390, by0))                                         # ground line
    d.line((24, top_y), (24, by0)); d.line((18, top_y), (30, top_y)); d.line((18, by0), (30, by0))
    # arms: rising from the box top to the bar ends
    a1b, a2b = (bx0 + 18, by0 - bh), (bx0 + blen - 14, by0 - bh)
    bar_l, bar_r = (bx0 - 22, top_y + 14), (bx0 + blen + 30, top_y)
    for p_, q_ in ((a1b, bar_l), (a2b, bar_r)):
        d.line(p_, q_)
    d.group()
    d.line((bx0, by0), back, (back[0], by0 - bh), (bx0, by0 - bh), closed=True)  # sound box
    d.line((bx0 + 6, by0), (bx0 + 6, by0 + 6)); d.line((back[0] - 6, by0), (back[0] - 6, by0 + 6))
    # arms as tapered staves
    for (ax, ay), (tx, ty) in ((a1b, bar_l), (a2b, bar_r)):
        ang = math.atan2(ty - ay, tx - ax); nx, ny = -math.sin(ang), math.cos(ang)
        w0, w1 = 7, 4
        d.line((ax + nx * w0, ay + ny * w0), (tx + nx * w1, ty + ny * w1))
        d.line((ax - nx * w0, ay - ny * w0), (tx - nx * w1, ty - ny * w1))
    # the bar, with eleven peg points along it
    d.line((bar_l[0] - 6, bar_l[1] + 1.5), (bar_r[0] + 8, bar_r[1] - 1.5))
    d.line((bar_l[0] - 6, bar_l[1] + 7.5), (bar_r[0] + 8, bar_r[1] + 4.5))
    holder = [(bx0 + 40 + i * 6.2, by0 - bh + 22) for i in range(11)]
    pegs = []
    for i in range(11):
        t = 0.16 + i * 0.062
        pegs.append((bar_l[0] + t * (bar_r[0] - bar_l[0]), bar_l[1] + 4 + t * (bar_r[1] - bar_l[1])))
    d.group('mid')
    for p_, h_ in zip(pegs, holder):
        d.line(p_, h_)
    d.line((holder[0][0] - 4, holder[0][1] + 3), (holder[-1][0] + 4, holder[-1][1] + 3))  # string holder
    for p_ in pegs:
        d.line((p_[0], p_[1] - 7), (p_[0], p_[1] + 4))
    # the head on the front of the box: a bull's mask as a wedge, horns, beard
    d.group()
    hx, hy = bx0 - 4, by0 - bh - 6
    d.line((hx, hy), (hx - 26, hy + 8), (hx - 30, hy + 22), (hx - 18, hy + 30), (hx, hy + 24))
    d.line((hx - 6, hy + 2), (hx - 16, hy - 16), (hx - 26, hy - 12))
    d.line((hx - 24, hy + 30), (hx - 22, hy + 52), (hx - 10, hy + 54), (hx - 6, hy + 30))
    for yy in range(36, 54, 6):
        d.line((hx - 21, hy + yy), (hx - 9, hy + yy))
    d.circle(hx - 18, hy + 14, 2.5)
    d.group('mid')
    d.text(36, top_y + 40, '112.5 CM', size=7, anchor='start')
    d.text(bar_r[0] - 10, top_y + 26, 'BAR · ELEVEN PEGS', size=7)
    d.text(back[0] - 4, by0 - bh / 2 + 3, 'SOUND BOX', size=7, anchor='end')
    d.text(hx - 36, hy + 20, 'GOLD BULL', size=7, anchor='end')
    d.text(hx - 36, hy + 30, 'LAPIS BEARD', size=7, anchor='end')
    d.text(200, 290, "THE QUEEN'S LYRE · PG 800 · AS REBUILT 1971-72", size=7)
    return d


def hurrian_hymn():
    d = D()
    # The sammum's nine strings, numbered as the Babylonian texts number them (1 to 5, then back,
    # "behind"), and the fourteen named pairs among strings 1-7 as arcs below them. The five pairs
    # that open the hymn's notation (h.6, line 1) are drawn at full weight; the rest are thin.
    xs = [44 + i * 39 for i in range(9)]
    top, bot = 46, 140
    names = ['1', '2', '3', '4', '5', '4B', '3B', '2B', '1B']
    pairs = [(1, 5), (7, 5), (2, 6), (1, 6), (3, 7), (2, 7), (4, 1), (1, 3), (5, 2), (2, 4), (6, 3), (3, 5), (7, 4), (4, 6)]
    line1 = [(5, 2), (2, 7), (7, 5), (2, 6)]
    def arc(a, b, depth, cls=None):
        x1, x2 = xs[a - 1], xs[b - 1]
        cx, r = (x1 + x2) / 2, abs(x2 - x1) / 2
        pts = [(cx + r * math.cos(math.radians(t)), bot + 14 + depth * (12 + r * 0.55) * math.sin(math.radians(t))) for t in range(0, 181, 6)]
        d.line(*pts, cls=cls)
    d.group('thin')
    for (a, b) in pairs:
        if (a, b) not in line1:
            arc(a, b, 1.0)
    d.line((xs[0] - 14, top - 8), (xs[-1] + 14, top - 8))                  # crossbar
    d.line((xs[0] - 14, bot + 6), (xs[-1] + 14, bot + 6))                  # string holder
    d.group()
    for x in xs:
        d.line((x, top - 8), (x, bot + 6))
    for x in xs:
        d.circle(x, top - 8, 2.2)
    d.group()
    for (a, b) in line1:
        arc(a, b, 1.0)
    d.group('mid')
    for x, n in zip(xs, names):
        d.text(x, top - 18, n, size=7)
    d.text(200, 262, 'QABLITE 3 · IRBUTE 1 · QABLITE 3 · SAHRI 1 · ISARTE 10', size=7)
    d.text(200, 276, 'H.6, NOTATION LINE 1: PAIRS 5-2 · 2-7 · 7-5 · 2-6', size=7)
    d.text(200, 292, 'NINE STRINGS · FOURTEEN NAMED PAIRS · UGARIT, C. 1400 BC', size=7)
    return d


PLATES = {
    'hohle-fels-flute': hohle_fels_flute,
    'lyres-of-ur': lyres_of_ur,
    'hurrian-hymn': hurrian_hymn,
}
