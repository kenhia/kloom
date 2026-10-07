"""Plates for The Story of Life's part wrong2 (sprint 055): eugenics and lysenko. See plates_for.py."""
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


def _square(d, cx, cy, s):
    _box(d, cx - s, cy - s, 2 * s, 2 * s)


def _hatch_circle(d, cx, cy, r, step=2.6):
    """Diagonal hatching inside a circle: the pedigree's 'affected' fill, as chords at 45 degrees."""
    segs = []
    k = -r * math.sqrt(2)
    while k <= r * math.sqrt(2):
        # chord of the line x - y = k (rotated 45°) through the circle
        c = k / math.sqrt(2)
        h = math.sqrt(max(r * r - c * c, 0))
        if h > 0.3:
            ux, uy = 1 / math.sqrt(2), 1 / math.sqrt(2)          # along the chord
            nx, ny = 1 / math.sqrt(2), -1 / math.sqrt(2)         # normal
            px, py = cx + nx * c, cy + ny * c
            segs.append([(px - ux * h, py - uy * h), (px + ux * h, py + uy * h)])
        k += step
    d.lines(segs)


def eugenics():
    d = D()
    # The Buck family as the 1927 opinion read it (left: three generations "feeble-minded", hatched) and
    # as the records show it (right: no one affected; the two sisters sterilized, marked with a bar).
    # Standard pedigree symbols: circle female, square male, a horizontal line a mating, a drop line to
    # children. Frederick Buck was Emma's husband; Carrie and Doris had different fathers, drawn as two
    # matings. Schematic: only the people the case turned on.
    r = 8
    rows = [78, 148, 218]
    panels = [(30, 'THE COURT, 1927'), (220, 'THE RECORDS')]

    d.group('thin')
    for y in rows:
        d.line((24, y), (392, y))
    d.line((206, 40), (206, 262))

    def family(x0, affected):
        emma, fred, other = (x0 + 56, rows[0]), (x0 + 16, rows[0]), (x0 + 112, rows[0])
        carrie, doris, garland = (x0 + 36, rows[1]), (x0 + 120, rows[1]), (x0 + 84, rows[1])
        vivian = (x0 + 60, rows[2])
        d.group()
        d.circle(*emma, r)
        _square(d, *fred, r - 1)
        _square(d, *other, r - 1)
        d.circle(*carrie, r)
        d.circle(*doris, r)
        _square(d, *garland, r - 1)
        d.circle(*vivian, r)
        # matings and descent
        d.line((fred[0] + r - 1, fred[1]), (emma[0] - r, emma[1]))
        d.line((emma[0] + r, emma[1]), (other[0] - r + 1, other[1]))
        m1 = ((fred[0] + emma[0]) / 2, rows[0])
        m2 = ((emma[0] + other[0]) / 2, rows[0])
        d.line(m1, (m1[0], rows[1] - 24), (carrie[0], rows[1] - 24), (carrie[0], rows[1] - r))
        d.line(m2, (m2[0], rows[1] - 24), (doris[0], rows[1] - 24), (doris[0], rows[1] - r))
        d.dashed((carrie[0] + r, carrie[1]), (garland[0] - r + 1, garland[1]), dash=3, gap=2.5)
        m3 = ((carrie[0] + garland[0]) / 2, rows[1])
        d.line(m3, (m3[0], rows[2] - 24), (vivian[0], rows[2] - 24), (vivian[0], rows[2] - r))
        d.group('mid')
        if affected:
            for p in (emma, carrie, vivian):
                _hatch_circle(d, p[0], p[1], r - 1.2)
        else:
            for p in (carrie, doris):                                   # sterilized: a bar under the symbol
                d.line((p[0] - r - 2, p[1] + r + 4), (p[0] + r + 2, p[1] + r + 4))
        return emma, carrie, doris, vivian

    marks = [family(x, i == 0) for i, (x, _) in enumerate(panels)]

    d.group('mid')
    for (x, title), (emma, carrie, doris, vivian) in zip(panels, marks):
        d.text(x + 84, 30, title, size=7)
        d.text(emma[0], emma[1] - 14, 'EMMA', size=7)
        d.text(carrie[0], carrie[1] + 22, 'CARRIE', size=7)
        d.text(doris[0], doris[1] + 22, 'DORIS', size=7)
        d.text(vivian[0], vivian[1] + 20, 'VIVIAN', size=7)
    d.text(14, rows[0] + 2.5, 'I', size=7)
    d.text(14, rows[1] + 2.5, 'II', size=7)
    d.text(14, rows[2] + 2.5, 'III', size=7)
    d.text(110, 284, 'HATCHED: "FEEBLE-MINDED"', size=7)
    d.text(304, 284, 'BAR: STERILIZED', size=7)
    return d


def lysenko():
    d = D()
    # Two calendars for wheat, September to August. Above, a schematic year of temperature (a cosine,
    # coldest in January) against the 1–7 °C band in which cold acts on a winter cereal. Winter wheat is
    # sown in autumn and gets its cold in the field; Lysenko's vernalized seed was moistened and chilled
    # before a spring sowing. Below, the claim he added: that the change passed to the next generation.
    x0, x1 = 64, 388
    months = 'SONDJFMAMJJA'
    mw = (x1 - x0) / 12

    def mx(m):                                                        # month index (0 = September) to x
        return x0 + m * mw

    ty0, ty1 = 40, 104                                                # temperature panel
    def ty(t):                                                        # -10..25 °C to y
        return ty1 - (t + 10) / 35 * (ty1 - ty0)

    d.group('thin')
    for m in range(13):
        d.line((mx(m), ty0 - 4), (mx(m), 236))
    d.line((x0, ty(1)), (x1, ty(1)))
    d.line((x0, ty(7)), (x1, ty(7)))

    d.group()
    pts = []
    for k in range(97):
        m = 12 * k / 96
        t = 8 - 14 * math.cos(2 * math.pi * (m - 4.5) / 12)          # coldest in mid-January
        pts.append((mx(m), ty(t)))
    d.line(*pts)
    rw, rv = 150, 200                                                 # the two crop rows
    # winter wheat: sown September, through the winter in the field, harvested July
    d.line((mx(0.3), rw), (mx(10.6), rw))
    d.circle(mx(0.3), rw, 3)
    # vernalized: moistened and chilled in store, sown April, harvested August
    _box(d, mx(5.3), rv - 7, mx(7) - mx(5.3), 14)
    d.line((mx(7.2), rv), (mx(11.6), rv))
    d.circle(mx(7.2), rv, 3)

    d.group('mid')
    for x, y in ((mx(10.6), rw), (mx(11.6), rv)):                     # an ear of wheat at harvest
        d.line((x, y), (x, y - 20))
        for j in range(5):
            yy = y - 8 - j * 3
            d.ellipse(x - 2.4, yy, 1.6, 2.4)
            d.ellipse(x + 2.4, yy - 1.2, 1.6, 2.4)
    for m in (3.2, 4.0, 4.8):                                         # snow on the winter field
        d.line((mx(m) - 3, rw - 6), (mx(m) + 3, rw - 6))
    _arrow(d, (mx(7) - 2, rv), (mx(7.2) - 4, rv), size=4)
    # the claim: the next generation inherits the change (dashed, crossed)
    d.dashed((mx(11.6), rv + 8), (mx(11.6), 232), (mx(7.2), 232), dash=3, gap=2.5)
    _arrow(d, (mx(7.6), 232), (mx(7.2), 232), size=4)
    c = (mx(9.4), 232)
    d.line((c[0] - 5, c[1] - 5), (c[0] + 5, c[1] + 5))
    d.line((c[0] - 5, c[1] + 5), (c[0] + 5, c[1] - 5))

    d.group('mid')
    for m, ch in enumerate(months):
        d.text(mx(m + 0.5), 252, ch, size=7)
    d.text(x0 - 6, ty(4) + 2.5, '1–7 °C', size=7, anchor='end')
    d.text(x0 - 6, ty(18), 'TEMP.', size=7, anchor='end')
    d.text(x0 - 6, rw + 2.5, 'WINTER', size=7, anchor='end')
    d.text(x0 - 6, rv + 2.5, 'VERNALIZED', size=7, anchor='end')
    d.text(mx(6.15), rv + 20, 'CHILLED', size=7)
    d.text(mx(9.4), 222, 'CLAIMED: INHERITED', size=7)
    d.text(200, 278, 'WINTER WHEAT TWO WAYS · VERNALIZATION, 1928', size=7)
    return d


PLATES = {'eugenics': eugenics, 'lysenko': lysenko}
