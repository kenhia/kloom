"""Plates for The Cloud on the Ground's Elsewhere trail, part abroad2 (sprint 059). See plates_for.py."""
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


def ireland_grid():
    """The Commission for Regulation of Utilities' connection rule of December 2025 (CRU/2025236),
    as a one-line diagram and a target. Left: a data center of 10 MVA or more takes power from the
    grid, and generation or storage of the same capacity, separately metered, sells into it. Right:
    the share of a year's demand matched by new Irish renewables, which must reach 80% within six
    years of opening; the decision sets the end, not the path, so the path is drawn dashed."""
    d = D()
    bus_y = 46
    dc = (44, 150, 92, 70)          # data center box: x, y, w, h
    gen = (156, 150, 72, 70)        # generation or storage
    d.group('thin')
    # the grid's busbar ticks
    for x in range(26, 250, 16):
        d.line((x, bus_y - 4), (x, bus_y + 4))
    # the capacity bracket: the two boxes the same height
    for (x, y, w, h) in (dc, gen):
        d.line((x + w + 4, y), (x + w + 10, y))
        d.line((x + w + 4, y + h), (x + w + 10, y + h))
        d.line((x + w + 7, y), (x + w + 7, y + h))
    # the chart's axes and grid: years 0..8 after opening, share 0..100%
    ox, oy, sx, sy = 268, 236, 14, 1.7        # origin, units per year, units per percent
    for k in range(0, 9):
        d.line((ox + k * sx, oy), (ox + k * sx, oy + 4))
    for p in (20, 40, 60, 80, 100):
        d.line((ox - 4, oy - p * sy), (ox, oy - p * sy))

    d.group()
    d.line((20, bus_y), (250, bus_y))                                   # the grid
    _box(d, *dc)
    _box(d, *gen)
    # the data center's feed down from the grid, the generator's up into it
    dcx, gx = dc[0] + dc[2] / 2, gen[0] + gen[2] / 2
    d.line((dcx, bus_y), (dcx, dc[1]))
    d.line((gx, gen[1]), (gx, bus_y))
    # meters: one on each connection
    for (x, y) in ((dcx, 98), (gx, 98)):
        d.circle(x, y, 9)
    # axes of the chart
    d.line((ox, oy - 108 * sy), (ox, oy), (ox + 8 * sx, oy))
    # the target: 80% from year 6 on
    d.line((ox + 6 * sx, oy - 80 * sy), (ox + 8 * sx, oy - 80 * sy))

    d.group('mid')
    _arrow(d, (dcx, bus_y), (dcx, dc[1]), 6)
    _arrow(d, (gx, gen[1]), (gx, bus_y), 6)
    # server rows inside the data center, cells inside the storage
    for k in range(1, 5):
        d.line((dc[0] + 8, dc[1] + k * 14), (dc[0] + dc[2] - 8, dc[1] + k * 14))
    for k in range(1, 4):
        x = gen[0] + k * gen[2] / 4
        d.line((x, gen[1] + 10), (x, gen[1] + gen[3] - 10))
    # the path to the target, undetermined: dashed
    d.dashed((ox, oy), (ox + 6 * sx, oy - 80 * sy), dash=4, gap=3)
    d.dashed((ox + 6 * sx, oy), (ox + 6 * sx, oy - 80 * sy), dash=2, gap=3)

    d.group('labels')
    d.text(30, bus_y - 10, 'GRID', size=7, anchor='start')
    d.text(dcx, dc[1] + dc[3] + 13, 'DATA CENTER', size=7)
    d.text(gx, gen[1] + gen[3] + 13, 'GENERATION', size=7)
    d.text(gx, gen[1] + gen[3] + 23, 'OR STORAGE', size=7)
    d.text(dcx, 101, 'M', size=7)
    d.text(gx, 101, 'M', size=7)
    d.text(dc[0] + dc[2] + 13, dc[1] + dc[3] / 2 + 3, 'MIC', size=7, anchor='start')
    d.text(gen[0] + gen[2] + 13, gen[1] + gen[3] / 2 + 3, '= MIC', size=7, anchor='start')
    d.text(gx + 12, 74, 'SELLS', size=7, anchor='start')
    d.text(dcx - 12, 74, 'DRAWS', size=7, anchor='end')
    d.text(ox - 7, oy - 80 * sy + 3, '80%', size=7, anchor='end')
    d.text(ox - 7, oy + 3, '0', size=7, anchor='end')
    d.text(ox + 6 * sx, oy + 14, '6 YRS', size=7)
    d.text(ox + 4 * sx, oy - 108 * sy - 8, 'NEW IRISH RENEWABLES', size=7)
    d.text(ox + 4 * sx, oy + 26, 'YEARS AFTER OPENING', size=7)
    return d


def germany_efficiency_act():
    """The Energy Efficiency Act's data center requirements of 2023 (EnEfG § 11), on one time axis,
    2024 to mid-2031. Top: the PUE limit, 1.5 from July 2027 and 1.3 from July 2030 for centers
    opened before July 2026, and 1.2 for those opening from then. Middle: the share of reused heat
    planned for a new center, by when it opens: 10%, 15%, 20%. Bottom: electricity matched with
    renewables on balance, 50% from 2024 and 100% from 2027; the 2026 bill's move to 2030 is
    dashed."""
    d = D()
    x0, x1 = 54, 384                 # 2024.0 .. 2031.5
    yr = (x1 - x0) / 7.5

    def X(t):
        return x0 + (t - 2024) * yr

    bands = (
        # top of band, height, value range (lo, hi) drawn upward
        (40, 64, (1.0, 1.6)),        # PUE: lower is stricter
        (126, 58, (0, 25)),          # reused heat, %
        (206, 58, (0, 100)),         # renewables, %
    )

    def Y(band, v):
        top, h, (lo, hi) = bands[band]
        return top + h - (v - lo) / (hi - lo) * h

    d.group('thin')
    for k in range(2024, 2032):
        d.line((X(k), 30), (X(k), 270))
    for (top, h, _) in bands:
        d.line((x0, top + h), (x1, top + h))

    d.group()
    # PUE: existing centers (before July 2026), from July 2027 and July 2030
    d.line((X(2027.5), Y(0, 1.5)), (X(2030.5), Y(0, 1.5)), (X(2030.5), Y(0, 1.3)), (X(2031.5), Y(0, 1.3)))
    # PUE: new centers, from July 2026
    d.line((X(2026.5), Y(0, 1.2)), (X(2031.5), Y(0, 1.2)))
    # reused heat, by opening date
    d.line((X(2026.5), Y(1, 10)), (X(2027.5), Y(1, 10)), (X(2027.5), Y(1, 15)), (X(2028.5), Y(1, 15)),
           (X(2028.5), Y(1, 20)), (X(2031.5), Y(1, 20)))
    # renewables on balance
    d.line((X(2024), Y(2, 50)), (X(2027), Y(2, 50)), (X(2027), Y(2, 100)), (X(2031.5), Y(2, 100)))

    d.group('mid')
    # the 2026 bill: 100% from 2030 instead of 2027
    d.dashed((X(2027), Y(2, 50)), (X(2030), Y(2, 50)), (X(2030), Y(2, 100)), dash=4, gap=3)
    # July 2026, the line between old and new centers
    d.dashed((X(2026.5), 30), (X(2026.5), 270), dash=2, gap=3)
    for t, v in ((2027.5, 1.5), (2030.5, 1.3), (2026.5, 1.2)):
        d.circle(X(t), Y(0, v), 2.2)

    d.group('labels')
    for k in range(2024, 2032):
        d.text(X(k) + yr / 2, 282, str(k), size=7)
    d.text(x0, 34, 'PUE LIMIT', size=7, anchor='start')
    d.text(x0, 120, 'REUSED HEAT, NEW CENTERS', size=7, anchor='start')
    d.text(x0, 200, 'RENEWABLE, ON BALANCE', size=7, anchor='start')
    d.text(X(2029), Y(0, 1.5) - 5, 'OLDER 1.5', size=7)
    d.text(X(2031), Y(0, 1.3) - 5, '1.3', size=7)
    d.text(X(2028.2), Y(0, 1.2) + 11, 'NEW 1.2', size=7)
    d.text(X(2027), Y(1, 10) - 5, '10%', size=7)
    d.text(X(2028), Y(1, 15) - 5, '15%', size=7)
    d.text(X(2030), Y(1, 20) - 5, '20%', size=7)
    d.text(X(2025.5), Y(2, 50) - 5, '50%', size=7)
    d.text(X(2028.5), Y(2, 100) - 5, '100%', size=7)
    d.text(X(2028.5), Y(2, 50) + 11, '2026 BILL', size=7)
    d.text(X(2026.5) - 3, 258, 'JULY 2026', size=7, anchor='end')
    return d


PLATES = {'ireland-grid': ireland_grid, 'germany-efficiency-act': germany_efficiency_act}
