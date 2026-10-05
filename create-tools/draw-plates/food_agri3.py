"""Plates for Daily Bread's agri3 part (sprint 051): the Irish famine and the Corn Laws. See plates_for.py."""
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


# The island's population at each census, in millions ("Historical population of Ireland", Wikipedia,
# from the census returns): 1841 is 8,175,124 and 1851 is 6,552,385.
CENSUS = [(1821, 6.80), (1831, 7.77), (1841, 8.18), (1851, 6.55), (1861, 5.80), (1871, 5.40),
          (1881, 5.18), (1891, 4.70), (1901, 4.46), (1911, 4.38)]


def irish_famine():
    d = D()
    # Population against census year, on a linear scale from zero. The dashed line is the 1851 census
    # commissioners' estimate that, at the earlier rate of growth, the population would have reached
    # just over nine million by 1851. The hatched band is the famine, 1845-52.
    x0, x1, y0, y1 = 62, 372, 252, 42                                     # 1821-1911, 0-9 million

    def px(year):
        return x0 + (x1 - x0) * (year - 1821) / 90

    def py(m):
        return y0 - (y0 - y1) * m / 9

    d.group('thin')
    for m in range(0, 10):                                                # a line every million
        d.line((x0, py(m)), (x1, py(m)))
    for year, _ in CENSUS:
        d.line((px(year), y0), (px(year), y1))
    for i in range(16):                                                   # the famine band, hatched
        xa = px(1845) + i * (px(1852) - px(1845)) / 15
        d.line((xa, py(0.35)), (xa - 5, py(0)))

    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))                                  # the axes
    d.line(*[(px(y), py(m)) for y, m in CENSUS])                          # the census line

    d.group('mid')
    for y, m in CENSUS:
        d.circle(px(y), py(m), 2.6)
    d.line((px(1845), py(0.35)), (px(1845), y0))                          # the famine band's edges
    d.line((px(1852), py(0.35)), (px(1852), y0))
    d.dashed((px(1841), py(8.18)), (px(1851), py(9.0)), dash=4, gap=3)    # the expected 1851
    d.circle(px(1851), py(9.0), 2.6)
    gap_x = px(1851) + 9                                                  # the shortfall, 1851
    d.line((gap_x, py(9.0)), (gap_x, py(6.55)))
    _arrow(d, (gap_x, py(7.9)), (gap_x, py(6.55)))
    _arrow(d, (gap_x, py(7.6)), (gap_x, py(9.0)))

    d.group('mid')
    d.text(px(1852) + 5, py(0.35) - 3, 'FAMINE 1845–52', size=7, anchor='start')
    d.text(px(1841) - 6, py(8.18) - 7, '8.18 M', size=7, anchor='end')
    d.text(px(1851) - 6, py(6.55) + 4, '6.55 M', size=7, anchor='end')
    d.text(px(1851) - 6, py(9.0) - 6, 'EXPECTED 9 M', size=7, anchor='end')
    d.text(gap_x + 6, py(7.75), '2.5 M SHORT', size=7, anchor='start')
    d.text(px(1911), py(4.38) - 9, '4.38 M', size=7)
    for year in (1821, 1841, 1861, 1881, 1901):
        d.text(px(year), y0 + 12, str(year), size=7)
    for m in (0, 3, 6, 9):
        d.text(x0 - 6, py(m) + 3, f'{m} M', size=7, anchor='end')
    d.text((x0 + x1) / 2, y0 + 27, 'POPULATION OF IRELAND AT EACH CENSUS', size=7)
    return d


# Duty in shillings on a quarter of foreign wheat entered for home consumption, against the Gazette
# average price in shillings, read from the Acts' own tables (legislation.gov.uk's King's and Queen's
# Printer copies): 9 Geo. 4 c. 60 (1828), 5 & 6 Vict. c. 14 (1842) and 9 & 10 Vict. c. 22 (1846).

def duty_1828(p):
    table = {61: 25 + 8 / 12, 62: 24 + 8 / 12, 63: 23 + 8 / 12, 64: 22 + 8 / 12, 65: 21 + 8 / 12,
             66: 20 + 8 / 12, 67: 18 + 8 / 12, 68: 16 + 8 / 12, 69: 13 + 8 / 12, 70: 10 + 8 / 12,
             71: 6 + 8 / 12, 72: 2 + 8 / 12}
    if p >= 73:
        return 1
    if p in table:
        return table[p]
    return 25 + 8 / 12 + (61 - p)                                         # 1s more for each 1s under 61s


def duty_1842(p):
    if p < 51:
        return 20
    steps = {51: 19, 52: 18, 53: 18, 54: 18, 55: 17, 56: 16, 57: 15, 58: 14, 59: 13, 60: 12, 61: 11,
             62: 10, 63: 9, 64: 8, 65: 7, 66: 6, 67: 6, 68: 6, 69: 5, 70: 4, 71: 3, 72: 2}
    return steps.get(p, 1)


def duty_1846(p):
    if p < 48:
        return 10
    return {48: 9, 49: 8, 50: 7, 51: 6, 52: 5}.get(p, 4)


def corn_laws():
    d = D()
    # Each scale is drawn as steps: the duty is constant across each shilling of price (each band the
    # Acts name), and the 1828 scale rises by a shilling for each shilling under 61s. The 1815 law had
    # no duty: below 80s foreign wheat could not be sold at all, and above it came in free.
    x0, x1, y0, y1 = 60, 372, 248, 46                                     # 40s-86s, duty 0-50s

    def px(s):
        return x0 + (x1 - x0) * (s - 40) / 46

    def py(s):
        return y0 - (y0 - y1) * s / 50

    def steps(fn, lo, hi):
        pts = []
        for p in range(lo, hi):
            pts += [(px(p), py(fn(p))), (px(p + 1), py(fn(p)))]
        return pts

    d.group('thin')
    for s in range(0, 51, 10):
        d.line((x0, py(s)), (x1, py(s)))
    for s in range(40, 87, 10):
        d.line((px(s), y0), (px(s), y1))
    for i in range(14):                                                   # 1815: the closed ports, hatched
        xa = px(40) + 6 + i * (px(80) - px(40) - 10) / 13
        d.line((xa, py(48.5)), (xa + 6, py(50)))

    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))                                  # the axes
    d.line((px(80), py(50)), (px(80), y0))                                # 1815: the gate at 80s
    d.line(*steps(duty_1828, 40, 80))
    d.line(*steps(duty_1842, 40, 80))

    d.group('mid')
    d.line(*steps(duty_1846, 40, 80))
    d.dashed((px(40), py(1)), (px(86), py(1)), dash=4, gap=3)             # from 1849: a shilling

    d.group('mid')
    d.text((px(40) + px(80)) / 2, py(50) - 6, '1815: NOTHING ADMITTED BELOW 80s', size=7)
    d.text(px(80) + 5, py(30), 'FREE', size=7, anchor='start')
    d.text(px(80) + 5, py(30) + 10, 'ABOVE', size=7, anchor='start')
    d.text(px(44) + 2, py(duty_1828(44)) - 6, '1828', size=7, anchor='start')
    d.text(px(44) + 2, py(20) - 6, '1842', size=7, anchor='start')
    d.text(px(44) + 2, py(10) - 6, '1846', size=7, anchor='start')
    d.text(px(84), py(1) - 6, '1849', size=7)
    for s in (40, 50, 60, 70, 80):
        d.text(px(s), y0 + 12, f'{s}s', size=7)
    for s in (0, 10, 20, 30, 40, 50):
        d.text(x0 - 6, py(s) + 3, f'{s}s', size=7, anchor='end')
    d.text((x0 + x1) / 2, y0 + 27, 'PRICE OF A QUARTER OF BRITISH WHEAT', size=7)
    d.text(14, (y0 + y1) / 2, 'DUTY', size=7, anchor='start')
    return d


PLATES = {
    'irish-famine': irish_famine,
    'corn-laws': corn_laws,
}
