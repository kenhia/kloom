"""Plates for The Cloud on the Ground's power1 part (sprint 059): power-demand, who-pays-grid. See plates_for.py."""
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


def power_demand():
    """US data center electricity use, 2014-2030, on linear axes: LBNL's estimates of the past
    (December 2024 report, and its June 2026 update for 2024), then the projections as ranges:
    LBNL 2024's 325-580 TWh in 2028, LBNL 2026's 521-843 TWh in 2030 (reference 649), and
    EPRI 2026's 383-793 TWh in 2030. Every point is a sourced figure; the fan joins them."""
    d = D()
    x0, x1, y0, y1 = 48, 372, 262, 34          # plot box: 2014..2030, 0..900 TWh
    X = lambda yr: x0 + (yr - 2014) * (x1 - x0) / 16
    Y = lambda twh: y0 - twh * (y0 - y1) / 900

    d.group('thin')
    for twh in (300, 600, 900):                 # gridlines
        d.line((x0, Y(twh)), (x1, Y(twh)))
    for yr in range(2014, 2031, 2):             # year ticks
        d.line((X(yr), y0), (X(yr), y0 + 4))
    d.line((X(2023.5), y1), (X(2023.5), y0))    # the line between estimate and projection

    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))        # axes
    past = [(2014, 60), (2015, 60), (2016, 60), (2018, 76), (2023, 176), (2024, 192)]
    d.line(*[(X(a), Y(b)) for a, b in past])
    for a, b in past:
        if a != 2015:
            d.circle(X(a), Y(b), 2.2)

    d.group('mid')
    # the fan: from 2024's estimate out to each range's ends
    for (yr, lo, hi, dx) in ((2028, 325, 580, 0), (2030, 521, 843, -7), (2030, 383, 793, 7)):
        x = X(yr) + dx
        d.dashed((X(2024), Y(192)), (x, Y(lo)), dash=4, gap=3)
        d.dashed((X(2024), Y(192)), (x, Y(hi)), dash=4, gap=3)
        d.line((x, Y(lo)), (x, Y(hi)))           # the range as an I-beam
        d.line((x - 4, Y(lo)), (x + 4, Y(lo)))
        d.line((x - 4, Y(hi)), (x + 4, Y(hi)))
    d.circle(X(2030) - 7, Y(649), 2.6)           # LBNL 2026's reference case

    d.group('labels')
    d.text(x0 - 6, Y(300) + 3, '300', size=7, anchor='end')
    d.text(x0 - 6, Y(600) + 3, '600', size=7, anchor='end')
    d.text(x0 - 6, Y(900) + 3, '900', size=7, anchor='end')
    d.text(x0 - 6, y1 - 8, 'TWh', size=7, anchor='start')
    for yr in (2014, 2018, 2022, 2026, 2030):
        d.text(X(yr), y0 + 14, str(yr), size=7)
    d.text(X(2018.5), Y(250), 'ESTIMATED', size=7)
    d.text(X(2026.6), Y(150), 'PROJECTED', size=7)
    d.text(X(2028) + 6, Y(580) - 6, 'LBNL 2024', size=7, anchor='end')
    d.text(X(2030) - 12, Y(843) + 3, 'LBNL 2026', size=7, anchor='end')
    d.text(X(2030) + 10, Y(383) + 22, 'EPRI 2026', size=7, anchor='end')
    return d


def who_pays_grid():
    """How a new line and substation reach customers' bills, as a schematic split flow: the cost
    enters a rate case as part of the revenue requirement, which is divided among customer classes;
    a large-load tariff's minimum charge is drawn as a floor under the large-load share. The band
    widths are a schematic, not any utility's numbers."""
    d = D()
    # the source: a substation and a line of pylons, left
    py = 92
    d.group('thin')
    d.line((14, 150), (122, 150))                       # ground under the source
    d.line((150, 40), (150, 262))                       # the rate case's datum
    for x in (200, 318):
        d.line((x, 30), (x, 272))                       # construction: split and class columns

    d.group()
    for x in (22, 62):                                  # two lattice pylons
        d.line((x - 9, 150), (x, py), (x + 9, 150))
        d.line((x - 12, py + 12), (x + 12, py + 12))
        d.line((x - 8, py + 24), (x + 8, py + 24))
    d.curve(f'M22 {py + 12} Q42 {py + 20} 62 {py + 12}')  # the conductor sags between them
    _box(d, 84, 126, 34, 24)                            # substation
    _box(d, 150, 110, 50, 80)                           # the rate case: the revenue requirement
    # the split flow: four bands from the rate case to the classes
    classes = [('RESIDENTIAL', 38), ('COMMERCIAL', 22), ('INDUSTRIAL', 14), ('LARGE LOAD', 26)]
    top, total_h = 110.0, 80.0
    ys = [44, 104, 164, 214]                            # where each band arrives
    bands = []
    for (name, share), ya in zip(classes, ys):
        h = total_h * share / 100
        a0, a1 = top, top + h                           # leaving the rate case
        b0, b1 = ya, ya + h                             # arriving at the class
        d.curve(f'M200 {a0:.1f} C259 {a0:.1f} 259 {b0:.1f} 318 {b0:.1f}')
        d.curve(f'M200 {a1:.1f} C259 {a1:.1f} 259 {b1:.1f} 318 {b1:.1f}')
        d.line((318, b0), (328, b0), (328, b1), (318, b1))
        bands.append((name, b0, b1))
        top = a1

    d.group('mid')
    d.line((118, 138), (146, 138)); _arrow(d, (136, 138), (148, 138))   # the cost goes in
    for i in range(1, 4):                               # the substation's bays
        d.line((84 + i * 8.5, 128), (84 + i * 8.5, 148))
    # the large-load tariff's floor: 85% of the band's height, drawn as a dashed line and hatched
    name, b0, b1 = bands[-1]
    floor = b1 - 0.85 * (b1 - b0)
    d.dashed((296, floor), (328, floor), dash=3, gap=2)
    d.lines(hatch([(300, floor), (328, floor), (328, b1), (300, b1)], 4, 45))

    d.group('labels')
    d.text(66, 174, 'NEW LINE AND', size=7)
    d.text(66, 183, 'SUBSTATION', size=7)
    d.text(175, 148, 'RATE', size=7)
    d.text(175, 157, 'CASE', size=7)
    d.text(175, 206, 'REVENUE', size=7)
    d.text(175, 215, 'REQUIREMENT', size=7)
    for nm, b0, b1 in bands:
        d.text(332, (b0 + b1) / 2 + 3, nm, size=7, anchor='start')
    d.text(332, b1 + 12, 'MINIMUM: 85%', size=7, anchor='start')
    d.text(200, 292, 'SCHEMATIC: BAND WIDTHS ILLUSTRATIVE', size=7)
    return d


PLATES = {'power-demand': power_demand, 'who-pays-grid': who_pays_grid}
