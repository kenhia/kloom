"""Plates for The Cloud on the Ground's economic case (sprint 059, part case2): jobs and the local
tax base. See plates_for.py."""
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


def data_center_jobs():
    """Workers on the Lafayette Data Center's site, Santa Clara, as its applicant filed them with the
    California Energy Commission (data responses, 2020; draft EIR, 2023): an average of 90 over 24
    months of construction, a peak of 175 in month 10, then 30 to 35 operations staff a day. The
    filing gives only those three figures, so the plate draws only them: the average as a dashed
    band, the peak as one bar, and the operations months as bars."""
    d = D()
    x0, x1, g = 48, 382, 246            # month 0, month 36, ground (0 workers)
    mx = (x1 - x0) / 36                 # units a month
    wy = 0.9                            # units a worker
    y = lambda n: g - n * wy
    xm = lambda m: x0 + m * mx

    d.group('thin')
    for n in (50, 100, 150, 200):       # worker grid
        d.line((x0, y(n)), (x1, y(n)))
    for m in range(0, 37, 6):           # month ticks
        d.line((xm(m), g), (xm(m), g + 5))
    d.line((xm(24), y(205)), (xm(24), g))   # end of construction

    d.group()
    d.line((x0, y(212)), (x0, g), (x1, g))  # axes
    # the peak: one bar, month 10
    _box(d, xm(9) + 1, y(175), mx - 2, 175 * wy)
    # operations: a bar a month at 35, months 25 to 36
    for m in range(24, 36):
        _box(d, xm(m) + 1.5, y(35), mx - 3, 35 * wy)

    d.group('mid')
    # the average over construction, a dashed band at 90
    d.dashed((x0, y(90)), (xm(24), y(90)), dash=5, gap=3)
    d.dashed((xm(24), y(90)), (xm(24), g), dash=3, gap=3)
    # the bottom of the operations range, 30, across the operations bars
    d.dashed((xm(24), y(30)), (x1, y(30)), dash=2, gap=2)
    # hatching inside the peak bar
    bx = xm(9) + 1
    d.lines(hatch([(bx, y(175)), (bx + mx - 2, y(175)), (bx + mx - 2, g), (bx, g)], 6, 45))
    # leader from the peak's label to the bar
    d.line((xm(12) + 2, y(178)), (bx + mx - 1, y(172)))
    _arrow(d, (xm(12) + 2, y(178)), (bx + mx - 1, y(172)), 4)

    d.group('labels')
    d.text(x0 - 4, y(200) + 2.5, '200', size=7, anchor='end')
    d.text(x0 - 4, y(100) + 2.5, '100', size=7, anchor='end')
    d.text(x0 - 4, g + 2.5, '0', size=7, anchor='end')
    for m in (0, 12, 24, 36):
        d.text(xm(m), g + 14, str(m), size=7)
    d.text((x0 + x1) / 2, g + 26, 'MONTHS FROM START', size=7)
    d.text(x0 + 4, y(218), 'WORKERS ON SITE', size=7, anchor='start')
    d.text(xm(12) + 6, y(182), 'PEAK 175, MONTH 10', size=7, anchor='start')
    d.text(xm(17), y(96), 'AVERAGE 90', size=7)
    d.text(xm(30), y(58), 'OPERATIONS', size=7)
    d.text(xm(30), y(46), '30-35 A DAY', size=7)
    return d


# Prince William County's data center business tangible property tax, FY2013-FY2022, in thousands of
# dollars (County Department of Finance, in PFM's Data Center Fiscal Impact Analysis, 2022, table 4;
# FY2022 preliminary): computer equipment and peripherals, furniture and fixtures.
PW_DC_BTPP = [
    (2013, 2446, 467), (2014, 2949, 893), (2015, 4115, 3431), (2016, 6926, 5771),
    (2017, 9290, 7493), (2018, 10830, 8744), (2019, 15625, 10228), (2020, 20879, 11419),
    (2021, 24876, 16676), (2022, 34118, 20266),
]


def tax_base():
    """Prince William County's tax on data centers' business property, FY2013 to FY2022, as stacked
    bars: computer equipment below, hatched, and furniture and fixtures above, from the county's
    finance department as its consultants PFM tabled it in 2022."""
    d = D()
    x0, x1, g = 54, 384, 246
    k = 3.7 / 1000                      # units per thousand dollars
    y = lambda v: g - v * k
    n = len(PW_DC_BTPP)
    step = (x1 - x0) / n
    bw = step * 0.62

    d.group('thin')
    for v in (10000, 20000, 30000, 40000, 50000):
        d.line((x0, y(v)), (x1, y(v)))

    d.group()
    d.line((x0, y(58000)), (x0, g), (x1, g))
    for i, (fy, cep, ff) in enumerate(PW_DC_BTPP):
        bx = x0 + i * step + (step - bw) / 2
        _box(d, bx, y(cep + ff), bw, (cep + ff) * k)
        d.line((bx, y(cep)), (bx + bw, y(cep)))

    d.group('mid')
    for i, (fy, cep, ff) in enumerate(PW_DC_BTPP):
        bx = x0 + i * step + (step - bw) / 2
        poly = [(bx, y(cep)), (bx + bw, y(cep)), (bx + bw, g), (bx, g)]
        d.lines(hatch(poly, 4, 45))

    d.group('labels')
    for v, s in ((0, '0'), (20000, '20'), (40000, '40')):
        d.text(x0 - 4, y(v) + 2.5, s, size=7, anchor='end')
    d.text(x0 + 4, y(60000), '$ MILLIONS A YEAR', size=7, anchor='start')
    for i, (fy, cep, ff) in enumerate(PW_DC_BTPP):
        if i in (0, 3, 6, 9):
            d.text(x0 + i * step + step / 2, g + 13, f'FY{fy % 100:02d}', size=7)
    last = x0 + (n - 1) * step + step / 2
    d.text(last, y(54384) - 5, '54.4', size=7)
    d.text(x0 + step / 2, y(2913) - 5, '2.9', size=7)
    d.text(x0 + 8, y(47200), 'ABOVE: FURNITURE, FIXTURES', size=7, anchor='start')
    d.text(x0 + 8, y(47200) + 11, 'HATCHED: COMPUTERS', size=7, anchor='start')
    return d


PLATES = {'data-center-jobs': data_center_jobs, 'tax-base': tax_base}
