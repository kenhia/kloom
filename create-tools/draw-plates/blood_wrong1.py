"""Plates for In the Blood's trail What we got wrong, first half (sprint 028, part wrong1). See plates_for.py."""
import math
from plates import D


def _pt(cx, cy, r, a):
    """The point at `a` degrees on a circle (clockwise from +x; SVG's y runs down)."""
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _sector(d, cx, cy, r0, r1, a0, a1, n=12):
    """A ring sector between radii r0 and r1, from a0 to a1 degrees, as one closed outline."""
    outer = [_pt(cx, cy, r1, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    inner = [_pt(cx, cy, r0, a1 - (a1 - a0) * i / n) for i in range(n + 1)]
    d.line(*(outer + inner), closed=True)


def purity_of_blood():
    d = D()
    # A genealogical fan: the candidate at the centre, then 2 parents, 4 grandparents, 8 and 16
    # ancestors in rings, paternal side left, maternal right. Each generation back doubles the
    # people the witnesses must vouch for; one stained sector in the outer ring condemns the whole.
    cx, cy = 200, 258
    radii = [26, 64, 102, 140, 178]                                  # the candidate, then four rings
    d.group('thin')
    d.line((cx - 196, cy), (cx + 196, cy))                           # the base line
    for k in range(1, 16):                                           # the sixteen sector rays, carried in
        x0, y0 = _pt(cx, cy, radii[0], 180 + 180 * k / 16)
        x1, y1 = _pt(cx, cy, radii[-1] + 10, 180 + 180 * k / 16)
        d.line((x0, y0), (x1, y1))
    d.line((cx, cy), (cx, cy - radii[-1] - 14))                      # the axis between the two sides
    d.group()
    d.arc(cx, cy, radii[0], 180, 360, n=24)
    for r in radii[1:]:
        d.arc(cx, cy, r, 180, 360, n=64)
    d.line((cx - radii[-1], cy), (cx + radii[-1], cy))
    # the divisions of each ring: 2, 4, 8, 16 sectors
    for g, r in enumerate(radii[1:], start=1):
        n = 2 ** g
        for k in range(1, n):
            a = 180 + 180 * k / n
            d.line(_pt(cx, cy, radii[g - 1], a), _pt(cx, cy, r, a))
    d.group('mid')
    # the stained ancestor: one sector of the outer ring, hatched
    s0, s1 = 180 + 180 * 11 / 16, 180 + 180 * 12 / 16
    _sector(d, cx, cy, radii[3], radii[4], s0, s1)
    for t in range(1, 7):
        a = s0 + (s1 - s0) * t / 7
        d.line(_pt(cx, cy, radii[3] + 3, a), _pt(cx, cy, radii[4] - 3, a + 1))
    # the line of descent from that sector to the candidate: one child in each ring
    path = [_pt(cx, cy, (radii[4] + radii[3]) / 2, (s0 + s1) / 2)]
    for g in (3, 2, 1):
        n = 2 ** g
        k = int(((s0 + s1) / 2 - 180) / (180 / n))
        a = 180 + 180 * (k + 0.5) / n
        path.append(_pt(cx, cy, (radii[g] + radii[g - 1]) / 2, a))
    path.append((cx, cy - radii[0] / 2))
    d.line(*path)
    _arrow(d, path[-2], path[-1])
    for p in path[1:-1]:
        d.circle(p[0], p[1], 2.5)
    d.group('mid')
    d.text(cx, cy - 6, 'CANDIDATE', size=7)
    d.text(cx - 182, cy + 30, 'FATHER’S LINE', size=7, anchor='start')
    d.text(cx + 182, cy + 30, 'MOTHER’S LINE', size=7, anchor='end')
    for g, r in enumerate(radii[1:], start=1):
        d.text(cx - (r + radii[g - 1]) / 2, cy + 14, str(2 ** g), size=7)
        d.text(cx + (r + radii[g - 1]) / 2, cy + 14, str(2 ** g), size=7)
    x, y = _pt(cx, cy, radii[4] + 12, (s0 + s1) / 2)
    d.text(x + 4, y - 4, 'ONE STAINED', size=7, anchor='start')
    d.text(cx, 30, 'EACH GENERATION BACK DOUBLES THE ANCESTORS TO VOUCH FOR', size=7)
    return d


def bloodletting():
    d = D()
    # Left: venesection at the elbow in elevation: a cord round the upper arm, the swollen vein
    # opened with a lancet, the stream caught in a bowl graduated in ounces. Right: a column for
    # Washington's blood (about 7.3 litres, from 70 mL/kg at 230 lb), with the day's bleedings
    # stacked from the top: the first and last as recorded, the two "copious" ones dashed, and the
    # two estimates of the total marked. Scale: 26 px a litre.
    d.group('thin')
    # the arm's axis and the bowl's centre line
    d.line((22, 96), (214, 96))
    d.line((150, 150), (150, 270))
    # the column's scale, a tick a litre
    colx0, colx1, top, px = 300, 340, 50, 26.0
    base = top + 7.3 * px
    for i in range(8):
        y = top + i * px
        d.line((colx1 + 2, y), (colx1 + 8, y))
    d.line((colx1 + 5, top), (colx1 + 5, base))
    d.group()
    # the arm: upper arm on the left, forearm on the right, bent slightly at the elbow
    d.line((22, 72), (110, 76), (130, 80), (214, 84))
    d.line((22, 120), (110, 116), (130, 112), (214, 106))
    # the cord round the upper arm
    d.line((66, 70), (66, 122))
    d.line((72, 70), (72, 122))
    # the bowl, in section, with its graduations
    d.line((112, 214), (118, 256), (182, 256), (188, 214))
    d.line((106, 214), (194, 214))
    # the column for the body's blood
    d.line((colx0, top), (colx0, base), (colx1, base), (colx1, top), closed=True)
    d.group('mid')
    # the swollen vein along the inner arm, and the opening
    d.curve('M 78 101 C 100 99 116 100 132 98 C 150 96 170 95 206 92')
    d.line((126, 96), (132, 102))
    # the lancet: a narrow double-edged blade on its handle
    d.line((132, 98), (150, 80), (176, 54))
    d.line((150, 80), (154, 84))
    d.line((150, 80), (146, 76))
    # the stream from the opening to the bowl, a falling parabola
    pts = [(132 + 18 * (t / 16), 102 + 132 * (t / 16) ** 2) for t in range(17)]
    d.line(*pts)
    d.line((150, 236), (182, 236))                                   # the blood's surface in the bowl
    for k, y in enumerate((246, 236, 226, 218)):
        d.line((184 - (y - 214) * 0.14, y), (190 - (y - 214) * 0.14, y))
    # the bleedings, stacked down from the top of the column
    first = 13 * 0.0296 * px                                         # 12 or 14 ounces
    last = 32 * 0.0296 * px                                          # about 32 ounces
    y1 = top + first
    d.line((colx0, y1), (colx1, y1))
    brick = top + 82 * 0.0296 * px                                   # Brickell's total
    vad = top + 125 * 0.0296 * px                                    # Vadakan's total
    y4 = brick - last
    for x in range(colx0 + 2, colx1, 6):                             # the two unrecorded bleedings, dashed
        d.line((x, (y1 + y4) / 2), (x + 3, (y1 + y4) / 2))
    d.line((colx0, y4), (colx1, y4))
    d.line((colx0, brick), (colx1, brick))
    for x in range(colx0 - 6, colx1 + 1, 6):
        d.line((x, vad), (x + 3, vad))
    for k in range(1, 6):                                            # hatch the last bleeding
        y = y4 + (brick - y4) * k / 6
        d.line((colx0 + 2, y), (colx1 - 2, y - 4))
    d.group('mid')
    d.text(66, 62, 'CORD', size=7)
    d.text(180, 48, 'LANCET', size=7, anchor='start')
    d.text(150, 270, 'BOWL, IN OUNCES', size=7)
    d.text(colx0 - 6, y1 - 3, '1', size=7, anchor='end')
    d.text(colx0 - 6, (y1 + y4) / 2 + 3, '2, 3', size=7, anchor='end')
    d.text(colx0 - 6, (y4 + brick) / 2 + 3, '4', size=7, anchor='end')
    d.text(colx1 + 12, brick + 3, '82 OZ', size=7, anchor='start')
    d.text(colx1 + 12, vad + 3, '125 OZ', size=7, anchor='start')
    d.text((colx0 + colx1) / 2, base + 14, 'ABOUT 7.3 L', size=7)
    d.text((colx0 + colx1) / 2, top - 8, 'HIS BLOOD', size=7)
    return d


def louis_numerical():
    d = D()
    # Louis's 77 pneumonia patients laid out by the day of the first bleeding, from his two tables:
    # an open circle for each who recovered, a crossed circle for each who died. Days 1-4 against
    # days 5-9, the comparison he made.
    rec = [3, 3, 6, 11, 6, 5, 6, 6, 4]
    died = [1, 5, 6, 6, 3, 3, 1, 1, 1]
    x0, dx, base, dy, r = 52, 36, 236, 10, 3.6
    d.group('thin')
    d.line((x0 - 22, base + 8), (x0 + 8 * dx + 22, base + 8))        # the base line
    for i in range(9):
        d.line((x0 + i * dx, base + 8), (x0 + i * dx, base - 18 * dy))
    for k in range(0, 19, 5):                                        # a count scale, every five patients
        y = base - k * dy
        d.line((x0 - 26, y), (x0 - 22, y))
    d.line((x0 - 24, base), (x0 - 24, base - 18 * dy))
    d.group()
    # the dividing line between day 4 and day 5
    xm = x0 + 3.5 * dx
    for y in range(int(base - 18 * dy), int(base + 26), 8):
        d.line((xm, y), (xm, y + 4))
    # brackets under the two groups
    for a, b in ((x0 - 10, xm - 6), (xm + 6, x0 + 8 * dx + 10)):
        d.line((a, base + 30), (a, base + 36), (b, base + 36), (b, base + 30))
    d.group('mid')
    for i in range(9):
        x = x0 + i * dx
        for k in range(rec[i] + died[i]):
            y = base - k * dy
            d.circle(x, y, r)
            if k >= rec[i]:                                          # the deaths, stacked above
                d.lines([[(x - r * 0.7, y - r * 0.7), (x + r * 0.7, y + r * 0.7)],
                         [(x - r * 0.7, y + r * 0.7), (x + r * 0.7, y - r * 0.7)]])
    d.group('mid')
    for i in range(9):
        d.text(x0 + i * dx, base + 22, str(i + 1), size=7)
    d.text((x0 - 10 + xm - 6) / 2, base + 48, 'DAYS 1–4: 18 OF 41 DIED', size=7)
    d.text((xm + 6 + x0 + 8 * dx + 10) / 2, base + 48, 'DAYS 5–9: 9 OF 36', size=7)
    d.text(x0 - 30, base - 15 * dy + 3, '15', size=7, anchor='end')
    d.text(x0 - 30, base + 3, '0', size=7, anchor='end')
    d.text(x0 + 6 * dx, 40, 'DAY OF FIRST BLEEDING', size=7)
    d.text(x0 + 6 * dx, 52, 'O RECOVERED  X DIED', size=7)
    return d


PLATES = {'purity-of-blood': purity_of_blood, 'bloodletting': bloodletting, 'louis-numerical': louis_numerical}
