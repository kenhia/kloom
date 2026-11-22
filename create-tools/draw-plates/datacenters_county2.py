"""Plates for The Cloud on the Ground's frames written by part county2 in sprint 059. See plates_for.py."""
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


def ashburn_power():
    """A double-circuit transmission structure in elevation, looking along the line, drawn to scale
    from the Aspen-Golden filing (PUR-2024-00032): a 500 kV circuit on one side and a 230 kV circuit on
    the other, about 171 feet high on average, in a 150-foot right-of-way; and beside it a substation
    in schematic elevation, where a transformer steps 500 kV down to 230 kV."""
    d = D()
    g = 262                      # ground
    k = 1.15                     # plate units per foot
    tx = 128                     # the structure's centerline
    top = g - 171 * k            # its average height, 171 ft
    row = 150 * k                # the right-of-way, 150 ft
    arms = [140, 118, 96]        # crossarm heights, in feet (schematic)

    d.group('thin')
    d.line((8, g), (392, g))
    d.line((tx, g + 6), (tx, top - 10))                                 # centerline
    x0, x1 = tx - row / 2, tx + row / 2                                 # right-of-way edges
    d.dashed((x0, g), (x0, 96), dash=4, gap=3)
    d.dashed((x1, g), (x1, 96), dash=4, gap=3)
    d.line((x0, g + 18), (x1, g + 18))                                  # its dimension
    _arrow(d, (x0 + 10, g + 18), (x0, g + 18), 4)
    _arrow(d, (x1 - 10, g + 18), (x1, g + 18), 4)
    hx = tx - 92                                                        # height dimension
    d.line((hx, g), (hx, top))
    d.line((hx - 4, top), (tx - 6, top))
    _arrow(d, (hx, g - 10), (hx, g), 4)
    _arrow(d, (hx, top + 10), (hx, top), 4)
    for ft in (50, 100, 150):                                           # ticks every 50 ft
        y = g - ft * k
        d.line((hx - 3, y), (hx + 3, y))
    for h in arms:                                                      # arm datums
        y = g - h * k
        d.line((tx - 62, y), (tx + 52, y))

    d.group()
    # the tapered steel monopole
    d.line((tx - 7, g), (tx - 2.5, top), (tx + 2.5, top), (tx + 7, g))
    _box(d, tx - 12, g, 24, 5)                                          # foundation
    # crossarms: 500 kV to the left, longer; 230 kV to the right
    for h in arms:
        y = g - h * k
        d.line((tx - 3, y), (tx - 48, y), (tx - 3, y + 6))
        d.line((tx + 3, y), (tx + 36, y), (tx + 3, y + 5))
    # the shield wire peak
    d.line((tx - 2.5, top), (tx, top - 8), (tx + 2.5, top))
    # substation, in schematic elevation: a gantry, a transformer, and the 230 kV bus out
    sx0, sx1, sg = 250, 372, g
    beam = g - 92
    for x in (sx0 + 6, sx1 - 6):                                        # two A-frame gantry legs
        d.line((x - 7, sg), (x, beam), (x + 7, sg))
    d.line((sx0 - 4, beam), (sx1 + 4, beam))                            # the beam
    _box(d, 292, g - 42, 46, 36)                                        # transformer tank
    _box(d, 300, g - 6, 30, 6)                                          # its plinth
    for x in (sx0 - 10, sx1 + 10):                                      # the fence, at each end
        d.line((x, sg), (x, sg - 24))

    d.group('mid')
    # insulator strings and bundled conductors: three conductors to a phase at 500 kV, two at 230 kV
    for h in arms:
        y = g - h * k
        lx, rx = tx - 44, tx + 32
        d.line((lx, y), (lx, y + 14))
        for (dx, dy) in ((-3, 17), (3, 17), (0, 21.5)):
            d.circle(lx + dx, y + dy, 1.6)
        d.line((rx, y), (rx, y + 12))
        for dx in (-2.6, 2.6):
            d.circle(rx + dx, y + 15, 1.6)
    # transformer radiator fins and bushings
    for i in range(6):
        x = 294 + i * 8.4
        d.line((x, g - 38), (x, g - 12))
    for x in (302, 315, 328):
        d.line((x, g - 42), (x, g - 56))
        d.circle(x, g - 58, 2)
    # 500 kV in from the gantry, down to the bushings; 230 kV out the other side
    d.line((sx0 - 4, beam), (sx0 - 22, beam - 18))
    d.line((sx0 + 20, beam), (302, g - 60))
    d.line((sx0 + 34, beam), (315, g - 60))
    d.line((sx0 + 48, beam), (328, g - 60))
    d.line((338, g - 28), (352, g - 28), (352, beam + 14), (sx1 + 22, beam + 14))
    _arrow(d, (sx1 + 12, beam + 14), (sx1 + 22, beam + 14), 4)
    # gravel yard
    d.lines(hatch([(sx0 - 10, g), (sx1 + 10, g), (sx1 + 10, g + 6), (sx0 - 10, g + 6)], 6, 45))

    d.group('labels')
    d.text(tx - 46, g - arms[0] * k - 19, '500 KV', size=7)
    d.text(tx - 46, g - arms[0] * k - 10, '4,357 MVA', size=7)
    d.text(tx + 34, g - arms[0] * k - 19, '230 KV', size=7)
    d.text(tx + 34, g - arms[0] * k - 10, '1,573 MVA', size=7)
    d.text(hx - 2, top - 6, '171 FT', size=7, anchor='start')
    d.text(tx, g + 30, 'RIGHT-OF-WAY 150 FT', size=7)
    d.text((sx0 + sx1) / 2, beam - 10, 'SUBSTATION', size=7)
    d.text(315, g + 18, '500 TO 230 KV', size=7)
    return d


def loudoun_by_right():
    """The two paths a data center application takes in Loudoun County: by right, approved by staff
    against the zoning ordinance's standards (until March 2025, and still for grandfathered
    applications), and by special exception, with public hearings before the Planning Commission and
    the Board of Supervisors and a vote that may deny it."""
    d = D()
    bw, bh, gap = 120, 22, 12
    lx, rx = 30, 236                  # the two columns' left edges
    ytop = 46
    left = ['APPLICATION', 'STAFF REVIEW', 'SITE PLAN APPROVED', 'BUILD']
    right = ['APPLICATION', 'STAFF REVIEW', 'PLANNING COMMISSION', 'BOARD OF SUPERVISORS',
             'BOARD VOTE', 'SITE PLAN APPROVED', 'BUILD']
    hearings = {2, 3}
    ly = [ytop + i * (bh + gap) for i in range(len(left))]
    ry = [ytop + i * (bh + gap) for i in range(len(right))]

    d.group('thin')
    d.line((200, 24), (200, 292))                                       # the divide between paths
    # the twelve-month clock, from the Planning Commission hearing to the Board's final action
    cx = rx + bw + 14
    y0, y1 = ry[2] + bh / 2, ry[4] + bh / 2
    d.line((cx, y0), (cx, y1))
    d.line((cx - 4, y0), (cx + 4, y0))
    d.line((cx - 4, y1), (cx + 4, y1))
    # the grandfathering resolution: an application filed before the cutoff crosses back
    d.dashed((rx, ry[0] + bh / 2), (lx + bw + 20, ry[0] + bh / 2), (lx + bw + 20, ly[1] + bh / 2),
             (lx + bw + 2, ly[1] + bh / 2), dash=4, gap=3)
    _arrow(d, (lx + bw + 12, ly[1] + bh / 2), (lx + bw + 2, ly[1] + bh / 2), 4)

    d.group()
    for y in ly:
        _box(d, lx, y, bw, bh)
    for i, y in enumerate(ry):
        _box(d, rx, y, bw, bh)
        if i in hearings:
            _box(d, rx - 3, y - 3, bw + 6, bh + 6)                      # a hearing: drawn double

    d.group('mid')
    for ys, x in ((ly, lx), (ry, rx)):
        for a, b in zip(ys, ys[1:]):
            d.line((x + bw / 2, a + bh), (x + bw / 2, b - 1))
            _arrow(d, (x + bw / 2, b - 8), (x + bw / 2, b - 1), 4)
    # a vote may deny: a branch out to the side
    vy = ry[4] + bh / 2
    d.line((rx, vy), (rx - 18, vy), (rx - 18, vy + 26))
    _arrow(d, (rx - 18, vy + 16), (rx - 18, vy + 26), 4)

    d.group('labels')
    d.text(lx + bw / 2, 30, 'BY RIGHT', size=7)
    d.text(rx + bw / 2, 30, 'SPECIAL EXCEPTION', size=7)
    for t, y in zip(left, ly):
        d.text(lx + bw / 2, y + bh / 2 + 2.5, t, size=7)
    for i, (t, y) in enumerate(zip(right, ry)):
        if i in hearings:
            d.text(rx + bw / 2, y + bh / 2 - 1.5, t, size=7)
            d.text(rx + bw / 2, y + bh / 2 + 7, 'PUBLIC HEARING', size=6)
        else:
            d.text(rx + bw / 2, y + bh / 2 + 2.5, t, size=7)
    d.text(cx + 4, (y0 + y1) / 2 - 3, '12', size=7, anchor='start')
    d.text(cx + 4, (y0 + y1) / 2 + 6, 'MO.', size=7, anchor='start')
    d.text(rx - 18, vy + 34, 'DENY', size=7)
    for j, t in enumerate(('FILED', 'BEFORE', '2/12/25')):
        d.text(lx + bw + 30, ly[1] + bh / 2 + 14 + j * 8, t, size=6)
    return d


PLATES = {'ashburn-power': ashburn_power, 'loudoun-by-right': loudoun_by_right}
