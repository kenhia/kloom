"""Plates for The Cloud on the Ground's part decide3 (sprint 059): moratoriums, federal-push. See plates_for.py."""
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


# Months counted from January 2023 (0) to the plate's right edge, January 2027 (48).
X0, X1, M0, M1 = 36, 384, 0, 48


def _mx(month):
    return X0 + (X1 - X0) * (month - M0) / (M1 - M0)


def _m(year, month, day=1):
    """A date as months since January 2023, with the day as a fraction."""
    return (year - 2023) * 12 + (month - 1) + (day - 1) / 30.4


def moratoriums():
    """A timeline, January 2023 to January 2027: the pauses in the reading's table as bars of their
    stated length (the open-ended Texas pause dashed), and the recalls, elections and ballot votes
    the reading names as marks on a line below. Dates and lengths are the sources'; the layout is a
    schematic."""
    d = D()
    axis_y, votes_y = 236, 214
    pauses = [   # (label, start, length in months or None for open-ended)
        ('GA', _m(2025, 7, 9), 100 / 30.4),
        ('WI', _m(2026, 6, 4), 18),
        ('MD', _m(2026, 7, 29), 18),
        ('MT', _m(2026, 7, 9), 12),
        ('NY', _m(2026, 7, 14), 12),
        ('TX', _m(2026, 8, 3), None),
        ('AZ', _m(2026, 9, 22), 120 / 30.4),
    ]
    votes = [    # (date, size): recalls and council elections small, the November ballots large
        (_m(2023, 6, 13), 4), (_m(2024, 11, 5), 4), (_m(2026, 4, 7), 4),
        (_m(2026, 9, 1), 4), (_m(2026, 11, 3), 7),
    ]
    now = _m(2026, 11, 22)

    d.group('thin')
    for k in range(M0, M1 + 1):                       # month ticks; years longer
        h = 7 if k % 12 == 0 else 3
        d.line((_mx(k), axis_y), (_mx(k), axis_y + h))
    for k in range(M0, M1 + 1, 12):                   # year rules up the plate
        d.dashed((_mx(k), 40), (_mx(k), axis_y), dash=3, gap=4)
    d.line((X0, votes_y), (X1, votes_y))              # the line of votes
    rows = [52 + 20 * i for i in range(len(pauses))]

    d.group()
    d.line((X0, axis_y), (X1, axis_y))                # the time axis
    for (label, start, length), y in zip(pauses, rows):
        x0 = _mx(start)
        if length is None:
            d.line((x0, y - 5), (x0, y + 5))
            d.dashed((x0, y), (X1, y), dash=4, gap=3)
            _arrow(d, (X1 - 8, y), (X1, y), 4)
            continue
        end = start + length
        x1 = _mx(min(end, M1))
        _box(d, x0, y - 4, x1 - x0, 8)
        if end > M1:                                  # runs past the plate's edge
            _arrow(d, (X1 - 8, y), (X1 + 2, y), 4)

    d.group('mid')
    for (date, r) in votes:
        x = _mx(date)
        d.circle(x, votes_y, r)
        d.line((x, votes_y + r), (x, axis_y))
    d.line((_mx(now), 36), (_mx(now), axis_y + 10))  # today

    d.group('labels')
    for k, yr in zip(range(M0, M1, 12), (2023, 2024, 2025, 2026)):
        d.text(_mx(k + 6), axis_y + 16, str(yr), size=7)
    for (label, start, length), y in zip(pauses, rows):
        d.text(_mx(start) - 5, y + 2.5, label, size=7, anchor='end')
    d.text(X0, 46, 'PAUSES', size=7, anchor='start')
    d.text(X0, votes_y - 8, 'VOTES', size=7, anchor='start')
    d.text(_mx(now) - 3, 32, 'NOV 2026', size=7, anchor='end')
    return d


def federal_push():
    """A federal permit as a flow, from the text of Executive Order 14318 (2025): a project with no
    federal nexus goes to the state and county alone; one with a nexus meets the Army Corps' wetland
    permit, NEPA review and species consultation, each with the shorter route the order points to
    (a nationwide permit, a categorical exclusion, a programmatic consultation), drawn as a dashed
    bypass. Only the Corps row is to scale: its two bars are the average days to decide in 2024,
    253 for an individual permit and 55 for a nationwide one, as POLITICO reported them. The other
    two rows are schematic, with no lengths."""
    d = D()
    px, py, pw, ph = 14, 128, 54, 30           # the project
    bx = 112                                   # where the federal reviews start
    rows = [84, 160, 226]                      # Corps, NEPA, species
    scale = 230 / 253                          # plate units a day, so 253 days spans 230 units
    full = 253 * scale
    short = 55 * scale
    sch = 150                                  # a schematic review's length
    ex = bx + full + 22                        # the end, where building may start

    d.group('thin')
    y = rows[0]
    d.line((bx, y + 30), (bx + full, y + 30))  # the Corps row's day scale
    for k in range(0, 254, 50):
        d.line((bx + k * scale, y + 28), (bx + k * scale, y + 32))
    d.dashed((px + pw / 2, py + ph), (px + pw / 2, 262), dash=3, gap=3)
    d.dashed((bx - 10, 62), (bx - 10, 246), dash=2, gap=4)   # the federal threshold

    d.group()
    _box(d, px, py, pw, ph)
    _box(d, px - 12, 262, pw + 24, 20)         # state and county only
    _box(d, ex, py, 32, ph)                    # build
    d.line((px + pw, py + ph / 2), (bx - 20, py + ph / 2))
    d.line((bx - 20, rows[0] + 6), (bx - 20, rows[2] + 6))
    for y, w in zip(rows, (full, sch, sch)):
        d.line((bx - 20, y + 6), (bx, y + 6))
        _box(d, bx, y, w, 12)                  # the full review
        d.line((bx + w, y + 6), (ex - 6, y + 6))
    d.line((ex - 6, rows[0] + 6), (ex - 6, rows[2] + 6))
    d.line((ex - 6, py + ph / 2), (ex, py + ph / 2))
    _arrow(d, (ex - 10, py + ph / 2), (ex, py + ph / 2), 4)

    d.group('mid')
    y = rows[0]                                # the nationwide permit, to scale, below the individual one
    d.dashed((bx, y + 6), (bx, y + 18), dash=2, gap=2)
    _box(d, bx, y + 14, short, 8)
    d.dashed((bx + short, y + 18), (bx + full + 8, y + 18), (bx + full + 8, y + 6), dash=3, gap=2)
    for y in rows[1:]:                         # an exclusion or a programmatic consultation: a bypass
        d.curve(f'M{bx - 4} {y + 2} C {bx + 30} {y - 22} {bx + sch - 30} {y - 22} {bx + sch + 4} {y + 2}')
        _arrow(d, (bx + sch - 2, y - 4), (bx + sch + 4, y + 2), 4)

    d.group('labels')
    d.text(px + pw / 2, py + 18, 'PROJECT', size=7)
    d.text(px + pw / 2, 275, 'STATE, COUNTY', size=7)
    d.text(ex + 16, py + 18, 'BUILD', size=7)
    d.text(bx, rows[0] - 6, 'ARMY CORPS WETLAND PERMIT: 253 DAYS', size=7, anchor='start')
    d.text(bx + short + 4, rows[0] + 25, 'NATIONWIDE: 55', size=7, anchor='start')
    d.text(bx + sch / 2, rows[1] + 8.5, 'NEPA REVIEW', size=7)
    d.text(bx + sch / 2, rows[2] + 8.5, 'SPECIES CONSULTATION', size=7)
    d.text(bx + sch / 2, rows[1] - 21, 'CATEGORICAL EXCLUSION', size=7)
    d.text(bx + sch / 2, rows[2] - 21, 'PROGRAMMATIC', size=7)
    d.text(bx - 10, 56, 'FEDERAL NEXUS', size=7)
    return d


PLATES = {
    'moratoriums': moratoriums,
    'federal-push': federal_push,
}
