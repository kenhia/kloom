"""Plates for The Cloud on the Ground's carbon-accounting and flexible-load frames (part power3,
sprint 059). See plates_for.py. Both are schematics: their curves are invented to show a method,
not measured at any place."""
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


# carbon-accounting -----------------------------------------------------------------------------
# One day, hour by hour. A data center draws a flat load L. A solar contract sized to match the day's
# use in total generates A sin(pi (h - 6) / 12) from 6:00 to 18:00, with A = pi L, so its daily total
# (24 A / pi) equals the load's (24 L). Annual (here daily) matching counts all of it: 100%. Hourly
# matching counts only min(solar, load) in each hour.
SOLAR_A = math.pi


def solar(h):
    return SOLAR_A * math.sin(math.pi * (h - 6) / 12) if 6 <= h <= 18 else 0.0


def hourly_share(n=24 * 60):
    """The share of the day's load that the solar contract covers hour by hour (load = 1)."""
    return sum(min(solar((i + 0.5) * 24 / n), 1.0) for i in range(n)) / n


def grid_intensity(h):
    """An invented grid's carbon intensity through a day, relative: lowest at midday, when solar on
    the grid is high, highest in the evening peak."""
    return 0.62 - 0.22 * math.sin(math.pi * (h - 6) / 12) * (6 <= h <= 18) + 0.12 * math.exp(-((h - 19.5) / 2.2) ** 2)


def carbon_accounting():
    """One day in schematic: a flat data center load, a solar contract's generation sized to match it
    over the day, the part matched hour by hour hatched, and the grid's carbon intensity above."""
    d = D()
    x0, x1 = 44, 372            # hour 0 and hour 24
    yb = 248                    # zero load
    unit = 34                   # plate units per unit of load
    X = lambda h: x0 + (x1 - x0) * h / 24
    Y = lambda v: yb - unit * v
    yi = lambda v: 112 - 120 * (v - 0.4)   # intensity panel, top band
    steps = [i / 4 for i in range(24 * 4 + 1)]

    d.group('thin')
    d.line((x0, yb), (x1, yb))                       # time axis
    d.line((x0, yb), (x0, Y(3.4)))                   # power axis
    for h in range(0, 25, 3):
        d.line((X(h), yb), (X(h), yb + 4))
    for h in (6, 12, 18):
        d.dashed((X(h), yb), (X(h), 30), dash=2, gap=3)

    d.group()
    sol = [(X(h), Y(solar(h))) for h in steps]
    d.line(*sol)                                     # the solar contract's generation
    d.line((X(0), Y(1)), (X(24), Y(1)))              # the data center's flat load

    d.group('mid')
    # the part matched hour by hour: under both the load and the solar curve
    lo, hi = 6.0, 18.0
    poly = [(X(lo), yb)] + [(X(h), Y(min(solar(h), 1.0))) for h in steps if lo <= h <= hi] + [(X(hi), yb)]
    d.lines(hatch(poly, 4, 45))
    # the grid's carbon intensity through the day
    d.line(*[(X(h), yi(grid_intensity(h))) for h in steps])
    d.line((X(10.6), Y(1.95) + 3), (X(10.6), Y(0.75)))                 # leader to the hatched part
    _arrow(d, (X(10.6), Y(1.95) + 3), (X(10.6), Y(0.75)), 4)
    d.line((X(17.3), Y(1.75) + 2), (X(14.6), Y(1.45)))                 # leader to the surplus

    d.group('labels')
    for h in (0, 6, 12, 18, 24):
        d.text(X(h), yb + 14, f'{h:02d}:00', size=7)
    d.text(X(12), 276, 'ONE DAY, HOUR BY HOUR', size=7)
    d.text(X(12), Y(SOLAR_A) - 6, 'SOLAR CONTRACT', size=7)
    d.text(X(21.6), Y(1) - 5, 'DATA CENTER', size=7)
    d.text(X(12), Y(2.25), 'HOURLY', size=7)
    d.text(X(12), Y(2.25) + 9, 'MATCH', size=7)
    d.text(X(16.9), Y(1.75), 'SURPLUS:', size=7, anchor='start')
    d.text(X(16.9), Y(1.75) + 9, 'COUNTS YEARLY', size=7, anchor='start')
    d.text(X(2.6), Y(1) + 12, 'GRID', size=7)
    d.text(x0 + 2, 70, 'GRID CO2 PER KWH', size=7, anchor='start')
    d.text(x1, 20, 'SCHEMATIC', size=7, anchor='end')
    return d


# flexible-load ---------------------------------------------------------------------------------
# A week of a grid's hourly demand (invented: a daily cycle, a weekend dip and a hot spell late in the
# week), the peak it was planned for, and a new data center added on top at a constant draw. Where
# the two together would pass the planned peak, the data center cuts back by the excess: the method
# of Norris and colleagues (2025), drawn on one invented week.
PEAK = 1.0          # the planned peak, as the unit of demand
NEW = 0.08          # the data center, as a share of the planned peak


def demand(t):
    """Grid demand at hour t of the week (0 = Monday 00:00), relative to the planned peak."""
    day, h = divmod(t, 24)
    daily = ((1 - math.cos(2 * math.pi * (h - 4) / 24)) / 2) ** 1.6      # trough at 04:00, peak at 16:00
    weekend = 0.06 if day >= 5 else 0.0
    heat = 0.08 * math.exp(-((t - 88) / 30) ** 2)                         # a hot Thursday
    return 0.62 + 0.28 * daily - weekend + heat


def curtailment():
    """(hours curtailed, share of the data center's energy curtailed) over the week, by the hour."""
    hours, cut = 0, 0.0
    for t in range(168):
        over = demand(t + 0.5) + NEW - PEAK
        if over > 0:
            hours += 1
            cut += min(over, NEW)
    return hours, cut / (NEW * 168)


def flexible_load():
    """A week of grid demand with its planned peak, a data center drawn on top at a constant load,
    and the hours in which it curtails hatched, labeled with their share of its week."""
    d = D()
    x0, x1 = 30, 386
    yb, ytop = 250, 40
    lo, hi = 0.5, 1.12          # the demand axis's range, relative to the planned peak
    X = lambda t: x0 + (x1 - x0) * t / 168
    Y = lambda v: yb - (yb - ytop) * (v - lo) / (hi - lo)
    ts = [i / 2 for i in range(168 * 2 + 1)]

    d.group('thin')
    d.line((x0, yb), (x1, yb))
    d.line((x0, yb), (x0, ytop))
    for k in range(8):
        d.line((X(24 * k), yb), (X(24 * k), yb + 4))
    for k in range(1, 7):
        d.dashed((X(24 * k), yb), (X(24 * k), Y(1.1)), dash=2, gap=4)

    d.group()
    d.line(*[(X(t), Y(demand(t))) for t in ts])                         # the grid's own demand
    d.line((X(0), Y(PEAK)), (X(168), Y(PEAK)))                          # the planned peak

    d.group('mid')
    # the grid with the data center on top, dashed where it would be if it never cut back
    d.dashed(*[(X(t), Y(demand(t) + NEW)) for t in ts], dash=3, gap=2)
    # the curtailed energy: between the planned peak and demand + new load, where that passes the peak
    runs, run = [], []
    for t in ts:
        if demand(t) + NEW > PEAK:
            run.append(t)
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    for r in runs:
        poly = [(X(t), Y(PEAK)) for t in r] + [(X(t), Y(demand(t) + NEW)) for t in reversed(r)]
        d.lines(hatch(poly, 2, 45))
        d.line(*poly, closed=True)
    d.line((X(16), Y(1.075) + 3), (X(16), Y(NEW + demand(16)) - 2))      # leader to the dashed curve
    d.line((X(103), Y(1.1) - 2), (X(92), Y(1.02)))                       # leader to the hatched peak

    hours, share = curtailment()
    d.group('labels')
    for k, name in enumerate(('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')):
        d.text(X(24 * k + 12), yb + 14, name, size=7)
    d.text(x1, Y(PEAK) + 11, 'PLANNED PEAK', size=7, anchor='end')
    d.text(X(4), Y(0.545), 'GRID DEMAND', size=7, anchor='start')
    d.text(X(16), Y(1.075), 'WITH DATA CENTER', size=7)
    d.text(X(104), Y(1.1) - 4, f'CURTAILED {hours} H,', size=7, anchor='start')
    d.text(X(104), Y(1.1) + 5, f'{share * 100:.1f}% OF ITS WEEK', size=7, anchor='start')
    d.text(x0 + 4, 30, 'SCHEMATIC', size=7, anchor='start')
    return d


PLATES = {'carbon-accounting': carbon_accounting, 'flexible-load': flexible_load}

if __name__ == '__main__':
    print('hourly share', round(hourly_share(), 3))
    print('curtailment', curtailment())
