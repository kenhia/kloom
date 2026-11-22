"""Plates for The Cloud on the Ground's part decide2 (sprint 059): tax-breaks and community-benefits.
See plates_for.py."""
import math
from plates import D, hatch


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def tax_breaks():
    """A schematic of one data center's equipment purchases over time under Virginia's rules: a
    build, then a refresh every five years (VEDP's rule of thumb), each purchase a bar with its sales
    tax drawn above it at scale (about 6%: the 4.3% state share, 1% local and a regional share of
    0.7% to 1.7%, JLARC 2024). Before the 2035 sunset the tax is waived (hatched, dashed); after it,
    paid (solid), unless the project is large enough for the 2040 or 2050 extensions."""
    d = D()
    x0, x1 = 40, 384             # 2025 .. 2055
    y_base = 250
    y0, y1 = 2025, 2055

    def X(year):
        return x0 + (year - y0) * (x1 - x0) / (y1 - y0)

    rate = 0.06                  # sales tax as a share of the price, about 6%
    build_h, refresh_h = 150, 112
    purchases = [(2026, build_h)] + [(2026 + 5 * k, refresh_h) for k in range(1, 6)]
    w = 18

    d.group('thin')
    d.line((x0, y_base), (x1, y_base))
    for yr in range(y0, y1 + 1, 5):
        d.line((X(yr), y_base), (X(yr), y_base + 5))
    for yr in range(y0, y1 + 1):
        d.line((X(yr), y_base), (X(yr), y_base + 2))
    d.line((x0, y_base), (x0, 60))
    for k in range(0, 5):
        d.line((x0 - 3, y_base - k * 40), (x0, y_base - k * 40))

    d.group()
    for (yr, h) in purchases:
        _box(d, X(yr) - w / 2, y_base - h, w, h)

    d.group('mid')
    for (yr, h) in purchases:
        t = h * rate * 2.0       # the tax slice, drawn at twice its share so it can be seen
        top = y_base - h - t
        poly = [(X(yr) - w / 2, top), (X(yr) + w / 2, top), (X(yr) + w / 2, top + t), (X(yr) - w / 2, top + t)]
        if yr < 2035:
            d.dashed(*poly, poly[0], dash=2.5, gap=2)
            d.lines(hatch(poly, 2.5, 45))
        else:
            d.line(*poly, closed=True)
    # the sunsets: 2035 for all; 2040 and 2050 for the largest projects
    for yr, top in ((2035, 56), (2040, 74), (2050, 92)):
        d.dashed((X(yr), y_base), (X(yr), top), dash=4, gap=3)

    d.group('labels')
    for yr in range(y0, y1 + 1, 10):
        d.text(X(yr), y_base + 15, str(yr), size=7)
    d.text(X(2026), y_base - build_h - 24, 'BUILD', size=7)
    d.text(X(2031), y_base - refresh_h - 22, 'REFRESH', size=7)
    d.text(X(2036), y_base - refresh_h - 22, 'PAID', size=7)
    d.text(X(2035) + 4, 54, 'SUNSET 2035', size=7, anchor='start')
    d.text(X(2040) + 4, 72, '2040: $35B, 1,000 JOBS', size=7, anchor='start')
    d.text(X(2050) + 4, 90, '2050: $100B', size=7, anchor='start')
    d.text(x0 + 4, 26, 'HATCHED: SALES TAX WAIVED', size=7, anchor='start')
    d.text(x0 + 4, 36, 'TAX ABOUT 6%, DRAWN DOUBLE', size=7, anchor='start')
    d.text(200, 292, 'SCHEMATIC · VIRGINIA RULES', size=7)
    return d


# One deal's terms, from the agreements WIRED read (2025) and Meta's fact sheet (2024): what
# Meta's subsidiary Laidley LLC took on, and what Louisiana gave. Solid: in a signed agreement;
# dashed: a voluntary pledge.
META = [
    ('INVEST $10B BY 2032', True),
    ('500 JOBS BY END OF 2034', True),
    ('AVERAGE PAY $82,000', True),
    ('PILOT: 20-40% OF TAX', True),
    ('RENT $732,000 A YEAR', True),
    ('GAS PLANTS PAID, 15 YR', True),
    ('$200M ROADS AND WATER', False),
    ('$1M A YEAR BILL AID', False),
]
LOUISIANA = [
    ('SALES TAX EXEMPTION', True),
    ('PROPERTY TAX CUT 60-80%', True),
    ('1,400 ACRES FOR $12M', True),
]


def community_benefits():
    """A ledger of one deal: Meta's Richland Parish data center in Louisiana. Two columns of
    entries, each a box; the solid ones are terms of a signed agreement, the dashed ones pledges."""
    d = D()
    top, row, n = 50, 24, len(META)
    lx, rx, cw = 14, 210, 176           # column x and width
    bottom = top + n * row + 6

    d.group('thin')
    for k in range(n + 1):                                   # ruled lines
        d.line((lx, top + k * row), (lx + cw, top + k * row))
        d.line((rx, top + k * row), (rx + cw, top + k * row))
    d.line((200, 22), (200, bottom + 10))                    # the center fold
    d.line((lx, top - 4), (lx + cw, top - 4))
    d.line((rx, top - 4), (rx + cw, top - 4))

    d.group()
    for col, items in ((lx, META), (rx, LOUISIANA)):
        for k, (_, signed) in enumerate(items):
            y = top + k * row + 4
            if signed:
                _box(d, col, y, cw, row - 8)
            else:
                d.dashed((col, y), (col + cw, y), (col + cw, y + row - 8), (col, y + row - 8), (col, y), dash=4, gap=3)
    for col in (lx, rx):                                     # the double rule closing each column
        d.line((col, bottom + 4), (col + cw, bottom + 4))
        d.line((col, bottom + 7), (col + cw, bottom + 7))

    d.group('mid')
    for col, items in ((lx, META), (rx, LOUISIANA)):
        for k in range(len(items)):
            y = top + k * row + 4 + (row - 8) / 2
            d.circle(col + 8, y, 2.4)
    # the legend
    _box(d, 30, 274, 16, 8)
    d.dashed((214, 274), (230, 274), (230, 282), (214, 282), (214, 274), dash=3, gap=2)

    d.group('labels')
    d.text(lx + cw / 2, 30, 'META · LAIDLEY LLC', size=7)
    d.text(lx + cw / 2, 40, 'TAKES ON', size=7)
    d.text(rx + cw / 2, 30, 'LOUISIANA', size=7)
    d.text(rx + cw / 2, 40, 'GIVES', size=7)
    for col, items in ((lx, META), (rx, LOUISIANA)):
        for k, (s, _) in enumerate(items):
            y = top + k * row + 4 + (row - 8) / 2 + 2.5
            d.text(col + 16, y, s, size=7, anchor='start')
    d.text(50, 281, 'SIGNED TERMS', size=7, anchor='start')
    d.text(234, 281, 'VOLUNTARY PLEDGE', size=7, anchor='start')
    d.text(rx + cw / 2, top + 3 * row + row / 2 + 6, 'RICHLAND PARISH', size=7)
    d.text(rx + cw / 2, top + 4 * row + row / 2 + 6, 'DATA CENTER, 2024-25', size=7)
    return d


PLATES = {'tax-breaks': tax_breaks, 'community-benefits': community_benefits}
