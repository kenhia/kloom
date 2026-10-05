"""Plates for Daily Bread's famine2 frames (sprint 051): the Holodomor, Bengal 1943 and the Great
Chinese Famine. See plates_for.py."""
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


def holodomor():
    d = D()
    # The grain procurement of 1932-33 as a flow. The quota came down the chain of command
    # (Politburo plan, republic, oblast, raion, collective farm); the grain went out of the village to
    # the state's reserves, the towns and the army, and export. Three measures closed the village:
    # the law of 7 August 1932 on collective-farm property (gleaning punished as theft), the
    # "black board" (no goods into a blacklisted village), and the directive of 22 January 1933
    # (no peasant to leave Ukraine or the North Caucasus). Positions are schematic.
    cx, w, h = 80, 120, 20
    chain = [(22, 'POLITBURO PLAN'), (62, 'UKRAINIAN SSR'), (102, 'OBLAST'), (142, 'RAION')]
    vx, vy, vw, vh = 20, 188, 130, 46                                     # the village

    d.group('thin')
    d.line((cx, 12), (cx, vy))                                            # the chain of command
    d.line((vx + vw, vy + vh / 2), (388, vy + vh / 2))                    # the grain's line
    d.line((222, 120), (222, 280))                                        # the split

    d.group()
    for y, _ in chain:
        _box(d, cx - w / 2, y, w, h)
    _box(d, vx, vy, vw, vh)
    outs = [(262, 132, 'STATE RESERVES'), (262, 201, 'TOWNS · ARMY'), (262, 262, 'EXPORT')]
    for x, y, _ in outs:
        _box(d, x, y - 10, 120, 20)

    d.group('mid')
    for (y0, _), (y1, _) in zip(chain, chain[1:] + [(vy, '')]):          # the quota, down
        d.line((cx, y0 + h), (cx, y1))
        _arrow(d, (cx, y0 + h), (cx, y1), size=4)
    gy = vy + vh / 2                                                      # the grain, out
    d.line((vx + vw, gy), (222, gy))
    for x, y, _ in outs:
        d.line((222, gy), (222, y), (x, y))
        _arrow(d, (222, y), (x, y), size=4)
    d.dashed((vx - 10, vy - 10), (vx + vw + 18, vy - 10), (vx + vw + 18, vy + vh + 10),
             (vx - 10, vy + vh + 10), (vx - 10, vy - 10), dash=4, gap=3)  # the closed border
    gx = 186                                                              # the law: a gate on the line
    d.line((gx, gy - 9), (gx, gy + 9))
    d.line((gx + 4, gy - 9), (gx + 4, gy + 9))
    bx, by = 140, 168                                                     # goods in, barred
    d.line((bx + 50, by - 22), (bx + 8, by))
    _arrow(d, (bx + 50, by - 22), (bx + 8, by), size=4)
    d.line((bx + 24, by - 17), (bx + 34, by - 7))
    d.line((bx + 24, by - 7), (bx + 34, by - 17))

    d.group('mid')
    for y, s in chain:
        d.text(cx, y + 13, s, size=7)
    d.text(vx + vw / 2, vy + 20, 'COLLECTIVE FARM', size=7)
    d.text(vx + vw / 2, vy + 32, 'VILLAGE', size=7)
    for x, y, s in outs:
        d.text(x + 60, y + 3, s, size=7)
    d.text(cx + 8, 174, 'QUOTA', size=7, anchor='start')
    d.text(gx + 2, gy - 14, 'LAW 7·VIII·32', size=7)
    d.text(bx + 52, by - 26, 'BLACK BOARD', size=7, anchor='end')
    d.text(vx + vw / 2 + 4, 266, 'NO EXIT · 22·I·33', size=7)
    d.text(330, 22, 'UKRAINE 1932–33', size=7)
    d.text(330, 34, 'PLAN 5.83 → 3.77 MT', size=7)
    d.text(330, 46, 'TAKEN 3.53 MT', size=7)
    return d


# Sen (1977), table 4: Birbhum district around Bolpur, from the log books of the Sriniketan farm
# and dairy. Index, December 1941 = 100. (months after Dec 1941, rice price, wage, exchange rate)
SEN_T4 = [
    (0, 100, 100, 100),
    (9, 114, 100, 88), (10, 179, 100, 56), (11, 221, 84, 38), (12, 179, 119, 66),
    (13, 193, 135, 70), (14, 179, 135, 75), (15, 271, 119, 44), (16, 371, 135, 36),
    (17, 557, 135, 24), (18, 514, 135, 26), (19, 521, 143, 27), (20, 536, 168, 31),
    (21, 357, 135, 38), (22, 400, 151, 38), (23, 314, 151, 48), (24, 236, 186, 79),
    (25, 257, 168, 65),
]


def bengal_1943():
    d = D()
    # Amartya Sen's wage and rice series for Birbhum, December 1941 to January 1944 (Sen 1977, table 4):
    # the price of rice, the day wage of a male unskilled laborer, and the exchange rate between them
    # (how much rice a day's work bought), each indexed to December 1941 = 100. Linear axes; the
    # gap from December 1941 to September 1942, where Sen has no wage record, is drawn dashed.
    x0, x1, y0, y1 = 52, 382, 250, 40
    vmax = 600

    def px(m):
        return x0 + (x1 - x0) * m / 25

    def py(v):
        return y0 - (y0 - y1) * v / vmax

    d.group('thin')
    for v in range(0, vmax + 1, 100):
        d.line((x0, py(v)), (x1, py(v)))
    for m in (0, 13, 25):                                                 # Dec 41, Jan 43, Jan 44
        d.line((px(m), y0), (px(m), y1))
    d.line((x0, py(100)), (x1, py(100)))

    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))
    for col in (1, 2, 3):
        pts = [(px(r[0]), py(r[col])) for r in SEN_T4]
        d.dashed(pts[0], pts[1], dash=3, gap=3)
        if col == 1:
            d.line(*pts[1:])

    d.group('mid')
    for col in (2, 3):
        d.line(*[(px(r[0]), py(r[col])) for r in SEN_T4[1:]])
    m, v = 17, 24                                                         # May 1943
    d.circle(px(m), py(v), 3)
    d.circle(px(m), py(557), 3)

    d.group('mid')
    for v in (0, 100, 200, 300, 400, 500, 600):
        d.text(x0 - 6, py(v) + 3, str(v), size=7, anchor='end')
    for m, s in ((0, 'DEC 41'), (13, 'JAN 43'), (25, 'JAN 44')):
        d.text(px(m), y0 + 12, s, size=7)
    d.text(px(17) + 6, py(557) - 4, 'RICE 557', size=7, anchor='start')
    d.text(px(24) + 2, py(186) - 7, 'WAGE', size=7, anchor='middle')
    d.text(px(17) - 6, py(24) + 3, 'DAY’S WORK IN RICE 24', size=7, anchor='end')
    d.text((x0 + x1) / 2, 24, 'BIRBHUM · INDEX, DEC 1941 = 100 · SEN 1977', size=7)
    return d


def great_chinese_famine():
    d = D()
    # China's grain output as announced and as later counted, million tonnes. Announced: 375 for 1958
    # (State Statistical Bureau, April 1959), cut to 250 at Lushan (August 1959); 525 set as the target
    # for 1959 (Sixth Plenum, November 1958); 270 claimed for 1959 (Li Fuchun, March 1960). Counted
    # since: 200 (1958), 170 (1959), 143.5 (1960). Claims are drawn dashed, counts solid.
    x0, x1, y0, y1 = 48, 384, 252, 44
    vmax = 550
    bw = 26

    def py(v):
        return y0 - (y0 - y1) * v / vmax

    groups = [
        (110, [('CLAIM', 375, True), ('LUSHAN', 250, True), ('COUNT', 200, False)]),
        (230, [('TARGET', 525, True), ('CLAIM', 270, True), ('COUNT', 170, False)]),
        (335, [('COUNT', 143.5, False)]),
    ]

    d.group('thin')
    for v in range(0, vmax + 1, 100):
        d.line((x0, py(v)), (x1, py(v)))

    d.group()
    d.line((x0, y1 - 4), (x0, y0), (x1, y0))
    for gx, bars in groups:
        n = len(bars)
        for i, (_, v, claim) in enumerate(bars):
            x = gx + (i - (n - 1) / 2) * (bw + 6) - bw / 2
            if not claim:
                _box(d, x, py(v), bw, y0 - py(v))

    d.group('mid')
    for gx, bars in groups:
        n = len(bars)
        for i, (_, v, claim) in enumerate(bars):
            x = gx + (i - (n - 1) / 2) * (bw + 6) - bw / 2
            if claim:
                d.dashed((x, y0), (x, py(v)), (x + bw, py(v)), (x + bw, y0), dash=4, gap=3)

    d.group('mid')
    for v in range(0, vmax + 1, 100):
        d.text(x0 - 6, py(v) + 3, str(v), size=7, anchor='end')
    for gx, bars in groups:
        n = len(bars)
        for i, (name, v, _) in enumerate(bars):
            x = gx + (i - (n - 1) / 2) * (bw + 6)
            d.text(x, py(v) - 5, f'{v:g}', size=7)
            d.text(x, y0 + 11, name, size=6)
    for gx, year in ((110, '1958'), (230, '1959'), (335, '1960')):
        d.text(gx, y0 + 24, year, size=7)
    d.text((x0 + x1) / 2 + 20, 24, 'GRAIN OUTPUT · MILLION TONNES', size=7)
    return d


PLATES = {
    'holodomor': holodomor,
    'bengal-1943': bengal_1943,
    'great-chinese-famine': great_chinese_famine,
}
