"""Plates for Daily Bread's part agri2 (sprint 051): malthus, reaper. See plates_for.py."""
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


# World population as a multiple of 1800's (983 million), at Malthus's 25-year steps from 1798
# (Our World in Data's series; 1800 stands in for 1798).
ACTUAL = [1, 1.13, 1.29, 1.38, 1.63, 1.98, 2.48, 3.99, 6.11, 8.23]


def malthus():
    d = D()
    # Malthus's two series of 1798 on one log (base 2) axis, one step per 25 years from 1798 to 2023:
    # people 1, 2, 4 ... 512 (a straight line on a log axis) and food 1, 2, 3 ... 10 (a curve that
    # flattens). The world's actual population, as a multiple of 1800's, is dashed beside them.
    x0, x1, y0, y1 = 60, 300, 250, 50                                    # plot box: steps 0-9, 1-512

    def px(i):
        return x0 + (x1 - x0) * i / 9

    def py(v):
        return y0 - (y0 - y1) * math.log2(v) / 9

    d.group('thin')
    for i in range(10):                                                   # a line every 25 years
        d.line((px(i), y0), (px(i), y1))
    for k in range(10):                                                   # doublings
        d.line((x0, py(2 ** k)), (x1, py(2 ** k)))

    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))                                  # the axes
    d.line(*[(px(i), py(2 ** i)) for i in range(10)])                     # geometrical
    d.line(*[(px(i), py(i + 1)) for i in range(10)])                      # arithmetical

    d.group('mid')
    for i in range(10):
        d.circle(px(i), py(2 ** i), 2.2)
        d.circle(px(i), py(i + 1), 2.2)
    d.dashed(*[(px(i), py(v)) for i, v in enumerate(ACTUAL)], dash=4, gap=3)

    d.group('mid')
    gap = (py(512), py(10))                                               # the gap at 2023
    d.line((px(9) + 12, gap[0] + 4), (px(9) + 12, gap[1] - 4))
    _arrow(d, (px(9) + 12, gap[1] - 4), (px(9) + 12, gap[0] + 4), size=4)
    _arrow(d, (px(9) + 12, gap[0] + 4), (px(9) + 12, gap[1] - 4), size=4)

    d.group('mid')
    d.text(px(9) - 6, py(512) - 8, 'PEOPLE 512', size=7, anchor='end')
    d.text(px(9) + 5, py(10) + 3, 'FOOD 10', size=7, anchor='start')
    d.text(px(9) + 5, py(8.23) + 13, 'WORLD 8.2', size=7, anchor='start')
    d.text(px(9) + 18, (gap[0] + gap[1]) / 2 + 3, '512 TO 10', size=7, anchor='start')
    d.text(px(4) + 4, py(16) - 8, '1, 2, 4, 8 …', size=7, anchor='end')
    d.text(px(6) - 4, py(7) - 9, '1, 2, 3, 4 …', size=7, anchor='end')
    for k in (0, 3, 6, 9):
        d.text(x0 - 6, py(2 ** k) + 3, str(2 ** k), size=7, anchor='end')
    for i, y in ((0, '1798'), (4, '1898'), (9, '2023')):
        d.text(px(i), y0 + 12, y, size=7)
    d.text((x0 + x1) / 2, y0 + 26, 'ONE STEP EVERY 25 YEARS', size=7)
    d.text((x0 + x1) / 2, 30, 'THE TWO RATIOS OF 1798 · LOG SCALE', size=7)
    return d


def reaper():
    d = D()
    # Top: the cutter bar in plan, Hussey's pattern: triangular knife sections riveted to a bar that slides
    # right and left through pointed guards (fingers); the sections are drawn half a pitch along, mid-stroke.
    # Bottom: the machine in side elevation, schematic: the main (bull) wheel drives a crank through
    # gearing, the crank's rod drives the knife, and the reel turns above the bar. Proportions are placed.
    pitch, bx0, bx1, by = 30, 80, 320, 92                                 # guard spacing, bar ends, bar line
    d.group('thin')
    for x in range(bx0 + 15, bx1, pitch):                                 # guard centre lines
        d.line((x, by + 12), (x, 30))
    d.line((60, by), (340, by))
    gx, gy, r = 110, 222, 50                                              # main wheel
    cx, cy = 210, 236                                                     # crank
    rx, ry, rr = 316, 178, 38                                             # reel
    d.line((gx - r - 8, gy), (gx + r + 8, gy))
    d.line((gx, gy - r - 8), (gx, gy + r + 8))
    d.line((rx - rr - 8, ry), (rx + rr + 8, ry))
    d.line((rx, ry - rr - 8), (rx, ry + rr + 8))
    d.line((20, 272), (380, 272))                                         # the ground

    d.group()
    d.line((bx0, by), (bx1, by), (bx1, by + 8), (bx0, by + 8), closed=True)   # the bar
    for x in range(bx0 + 15, bx1, pitch):                                 # guards, pointed forward
        d.line((x - 7, by + 8), (x - 4, 44), (x, 34), (x + 4, 44), (x + 7, by + 8))
    d.circle(gx, gy, r)                                                   # main wheel
    d.circle(gx, gy, 6)
    for k in range(8):
        a = math.pi * k / 4
        d.line((gx + 6 * math.cos(a), gy + 6 * math.sin(a)), (gx + (r - 2) * math.cos(a), gy + (r - 2) * math.sin(a)))
    d.circle(rx, ry, 5)
    for k in range(6):                                                    # reel arms and bats
        a = math.pi * k / 3 + 0.3
        e = (rx + rr * math.cos(a), ry + rr * math.sin(a))
        d.line((rx, ry), e)
        d.line((e[0] - 6 * math.sin(a), e[1] + 6 * math.cos(a)), (e[0] + 6 * math.sin(a), e[1] - 6 * math.cos(a)))
    _box(d, 296, 262, 40, 8)                                              # cutter bar, end on

    d.group('mid')
    for i, x in enumerate(range(bx0 + 15 + pitch // 2, bx1 - 10, pitch)):  # knife sections, mid-stroke
        d.line((x - 14, by + 4), (x - 5, 56), (x + 5, 56), (x + 14, by + 4))
        d.circle(x, by + 2, 1.4)                                          # the rivet
    d.circle(gx, gy, 20)                                                  # gear on the wheel
    d.circle(cx - 18, cy, 7)                                              # pinion
    d.circle(cx, cy, 10)                                                  # crank disc
    pin = (cx + 7, cy - 7)
    d.line(pin, (296, 266))                                               # the rod to the knife
    d.line((gx + 20, gy), (cx - 25, cy))                                  # the drive, schematic
    left, right = (150, 18), (250, 18)
    d.line(left, right)
    _arrow(d, right, left, size=4)
    _arrow(d, left, right, size=4)

    d.group('mid')
    d.text(200, 13 + 14, 'STROKE', size=7)
    d.text(76, 70, 'GUARD', size=7, anchor='end')
    d.text(324, 70, 'SECTION', size=7, anchor='start')
    d.text(200, 118, "THE KNIFE IN PLAN · HUSSEY'S PATTERN", size=7)
    d.text(gx, gy + r + 14, 'MAIN WHEEL', size=7)
    d.text(cx + 4, cy + 22, 'CRANK', size=7)
    d.text(rx - rr - 12, ry - rr + 4, 'REEL', size=7, anchor='end')
    d.text(316, 286, 'CUTTER BAR', size=7)
    return d


PLATES = {'malthus': malthus, 'reaper': reaper}
