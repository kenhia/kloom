"""Plates for The Cloud on the Ground's trail Water, measured, part wtrail1 (sprint 059):
withdrawal-consumption, cooling-tower and wue. See plates_for.py."""
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


def withdrawal_consumption():
    """Google's Council Bluffs, Iowa campus in 2025, as three flows drawn to scale: 1,746.4 million
    gallons withdrawn, 1,346.0 consumed (to the air as vapor), 400.4 discharged (Google 2026
    Environmental Report, p. 97). Band widths are proportional to the volumes; the upper part of
    the withdrawal turns up and leaves as vapor, the lower part runs on and is discharged."""
    d = D()
    W, C, Q = 1746.4, 1346.0, 400.4
    k = 64 / W                        # plate units per million gallons
    w, c, q = W * k, C * k, Q * k     # 64, 49.3, 14.7
    yin = 200                         # centre line of the withdrawal band
    top_in, bot_in = yin - w / 2, yin + w / 2
    split = top_in + c                # the upper c units turn up, the lower q run on
    r = 10                            # inner radius of the turn
    x0 = 210                          # west edge of the rising band
    x1 = x0 + c
    cx, cy = x0 - r, top_in - r       # centre of the turn
    ytop = 52                         # where the rising band ends, as vapor
    sx0, sx1, sy0, sy1 = 150, 300, 110, 252   # the site's boundary
    xm = x0 + c / 2
    yq = split + q / 2
    d.group('thin')
    d.line((20, 268), (380, 268))                         # ground
    d.line((20, yin), (cx, yin))                          # centre line of the withdrawal
    d.line((xm, ytop - 6), (xm, cy))                      # centre line of the consumption
    d.line((cx, yq), (385, yq))                           # centre line of the discharge
    d.arc(cx, cy, r + c / 2, 0, 90)
    sb = 500 * k                                          # a scale bar: 500 million gallons
    d.line((30, 284), (30 + sb, 284))
    d.line((30, 280), (30, 288)); d.line((30 + sb, 280), (30 + sb, 288))

    d.group()
    # withdrawal: both edges from the river to the turn
    d.line((40, top_in), (cx, top_in))
    d.line((40, bot_in), (370, bot_in))                   # the lower edge runs on as the discharge's
    # the turn: inner and outer edges, then the rising band
    d.arc(cx, cy, r, 0, 90)
    d.arc(cx, cy, r + c, 0, 90)
    d.line((x0, cy), (x0, ytop))
    d.line((x1, cy), (x1, ytop))
    # discharge: its upper edge starts where the turn leaves it
    d.line((cx, split), (370, split))

    d.group('mid')
    d.dashed((sx0, sy0), (sx1, sy0), (sx1, sy1), (sx0, sy1), (sx0, sy0), dash=4, gap=3)
    _arrow(d, (60, yin), (80, yin), 6)
    _arrow(d, (xm, 90), (xm, 72), 6)
    _arrow(d, (340, yq), (358, yq), 6)
    for dx in (-16, 0, 16):                               # vapor above the rising band
        d.curve(f'M{xm + dx:.1f} {ytop - 4} q 5 -6 0 -12 q -5 -6 0 -12')
    for yy in (top_in + 10, yin, bot_in - 10):            # the river at the left
        d.curve(f'M20 {yy:.1f} q 4 -3 8 0 q 4 3 8 0')

    d.group('labels')
    d.text(95, top_in - 8, 'WITHDRAWN 1,746', size=7)
    d.text(x1 + 8, 96, 'CONSUMED 1,346', size=7, anchor='start')
    d.text(x1 + 8, 106, 'TO THE AIR', size=7, anchor='start')
    d.text(335, split - 8, 'DISCHARGED 400', size=7)
    d.text(sx0 + 6, sy1 - 6, 'SITE', size=7, anchor='start')
    d.text(30 + sb + 6, 287, '500 MILLION GALLONS', size=7, anchor='start')
    d.text(380, 287, 'COUNCIL BLUFFS 2025', size=7, anchor='end')
    return d


def cooling_tower():
    """A mechanical-draft counterflow cooling tower in section: warm water sprayed from a header over
    fill, air drawn in at the louvers and up by the fan, evaporation and drift leaving the stack,
    the basin with make-up in and blowdown out, and the cooled water returning to the chillers.
    A schematic, not any one tower."""
    d = D()
    x0, x1 = 110, 290          # casing
    yt, yb = 70, 250           # casing top, basin floor
    fill_t, fill_b = 125, 175  # fill pack
    spray_y = 112
    elim_y = 98
    louver_t = 190
    basin_t = 225
    d.group('thin')
    d.line((20, yb + 8), (380, yb + 8))                    # ground
    d.line((200, 18), (200, basin_t))                      # axis of the tower
    d.line((x0, fill_t), (x1, fill_t)); d.line((x0, fill_b), (x1, fill_b))
    d.line((x0 - 40, basin_t + 6), (x1 + 40, basin_t + 6))  # water level datum

    d.group()
    # casing and fan stack
    d.line((x0, basin_t), (x0, yt), (x1, yt), (x1, basin_t))
    d.line((165, yt), (170, 40), (230, 40), (235, yt))     # fan stack (velocity recovery)
    # basin
    d.line((x0 - 6, basin_t), (x0 - 6, yb), (x1 + 6, yb), (x1 + 6, basin_t))
    # fan blades seen edge-on, and the motor
    d.line((172, 52), (228, 52))
    _box(d, 194, 52, 12, 10)
    # spray header with nozzles
    d.line((x0, spray_y), (x1, spray_y))
    for x in range(124, 290, 22):
        d.line((x, spray_y), (x, spray_y + 4))
    # drift eliminator: a row of chevrons
    pts = []
    for i in range(19):
        x = x0 + i * 10
        pts.append((x, elim_y if i % 2 == 0 else elim_y - 5))
    d.line(*pts)

    d.group('mid')
    # fill: hatched
    poly = [(x0, fill_t), (x1, fill_t), (x1, fill_b), (x0, fill_b)]
    d.lines(hatch(poly, 7, 60))
    # louvers on both sides
    for y in range(louver_t, basin_t - 2, 7):
        d.line((x0 - 10, y), (x0, y + 5))
        d.line((x1 + 10, y), (x1, y + 5))
    # water falling from the fill to the basin: short dashes
    for x in range(126, 290, 16):
        d.dashed((x, fill_b + 4), (x, basin_t - 4), dash=3, gap=5)
    # water surface in the basin
    d.curve(f'M{x0 - 6} {basin_t + 6} ' + ' '.join(f'q 4.5 -3 9 0' if i % 2 == 0 else f'q 4.5 3 9 0' for i in range(21)))
    # warm water in, up to the header
    d.line((330, 150), (310, 150), (310, spray_y), (x1, spray_y))
    _arrow(d, (310, 130), (310, 118), 5)
    # cooled water out to the chillers
    d.line((x1 + 6, 240), (350, 240))
    _arrow(d, (330, 240), (346, 240), 5)
    # make-up in at the left
    d.line((40, 232), (x0 - 6, 232))
    _arrow(d, (80, 232), (96, 232), 5)
    # blowdown out at the bottom left
    d.line((x0 + 10, yb), (x0 + 10, yb + 20), (60, yb + 20))
    _arrow(d, (80, yb + 20), (64, yb + 20), 5)
    # air in at the louvers, up through the fill
    for (a, b) in (((60, 205), (100, 205)), ((340, 205), (300, 205))):
        d.line(a, b); _arrow(d, a, b, 5)
    for x in (150, 250):
        d.line((x, 200), (x, 182)); _arrow(d, (x, 196), (x, 182), 5)
    # evaporation and drift out of the stack
    for dx in (-18, 0, 18):
        d.curve(f'M{200 + dx} 34 q 5 -5 0 -10 q -5 -5 0 -10')
    d.circle(244, 24, 1.2); d.circle(250, 30, 1.2); d.circle(256, 22, 1.2)

    d.group('labels')
    d.text(270, 18, 'EVAPORATION', size=7, anchor='start')
    d.text(262, 32, 'DRIFT', size=7, anchor='start')
    d.text(250, 48, 'FAN', size=7, anchor='start')
    d.text(x1 + 4, elim_y - 4, 'ELIMINATOR', size=7, anchor='start')
    d.text(340, 160, 'WARM WATER', size=7)
    d.text(x0 - 6, 152, 'FILL', size=7, anchor='end')
    d.text(48, 199, 'AIR', size=7)
    d.text(352, 199, 'AIR', size=7)
    d.text(56, 226, 'MAKE-UP', size=7)
    d.text(48, yb + 24, 'BLOWDOWN', size=7, anchor='end')
    d.text(150, yb - 6, 'BASIN', size=7)
    d.text(360, 234, 'TO CHILLERS', size=7)
    return d


# LBNL 2024, figure 4.4: medians as read from the figure (rendered at 216 dpi, measured to the
# pixel against its gridlines). (size, label, PUE, WUE in L/kWh)
LBNL_44 = [
    ('mid', 'AIR-COOLED CHILLER', 1.83, 0.05),
    ('mid', 'DRY COOLER', 1.59, 0.05),
    ('mid', 'AIRSIDE ECON.', 1.58, 0.02),
    ('mid', 'TOWERS', 1.52, 2.89),
    ('mid', 'AIRSIDE ECON. + TOWERS', 1.45, 1.32),
    ('mid', 'WATERSIDE ECON.', 1.38, 2.49),
    ('large', 'WATERSIDE ECON.', 1.12, 2.18),
    ('large', 'LIQUID IT, TOWERS', 1.13, 1.96),
    ('large', 'AIR + ADIABATIC', 1.14, 0.42),
    ('large', 'DRY + ADIABATIC', 1.20, 0.23),
    ('large', 'LIQUID IT, DRY', 1.09, 0.01),
]


def wue():
    """Simulated site WUE against PUE for cooling designs in midsize and large data centers, the
    medians of Lawrence Berkeley National Laboratory's 2024 report, figure 4.4, as read from the
    figure. Midsize designs are circles, large ones squares."""
    d = D()
    ox, oy = 60, 250            # origin: PUE 1.0, WUE 0
    px = lambda p: ox + (p - 1.0) * 330        # PUE 1.0..1.9 -> 60..357
    py = lambda w: oy - w * 66                 # WUE 0..3.2 -> 250..39
    d.group('thin')
    for p in (1.0, 1.2, 1.4, 1.6, 1.8):
        d.line((px(p), py(0)), (px(p), py(3.2)))
    for w in (0, 1, 2, 3):
        d.line((px(1.0), py(w)), (px(1.9), py(w)))

    d.group()
    d.line((px(1.0), py(3.2)), (px(1.0), py(0)), (px(1.9), py(0)))
    for p in (1.0, 1.2, 1.4, 1.6, 1.8):
        d.line((px(p), py(0)), (px(p), py(0) + 4))
    for w in (0, 1, 2, 3):
        d.line((px(1.0) - 4, py(w)), (px(1.0), py(w)))

    d.group('mid')
    for size, _, p, w in LBNL_44:
        x, y = px(p), py(w)
        if size == 'mid':
            d.circle(x, y, 3.5)
        else:
            _box(d, x - 3.2, y - 3.2, 6.4, 6.4)
    # the legend's marks
    d.circle(px(1.9) - 96, py(3.2) - 10.5, 3)
    _box(d, px(1.9) - 38, py(3.2) - 13.5, 6, 6)
    d.line((px(1.09), py(0.01) - 5), (px(1.09), py(0.8)))
    # the trade, drawn as a line from the midsize air-cooled chiller to the midsize towers
    a = (px(1.83), py(0.05)); b = (px(1.52), py(2.89))
    d.dashed(a, b, dash=4, gap=3)

    d.group('labels')
    d.text(px(1.45), 282, 'PUE (SIMULATED MEDIAN)', size=7)
    d.text(14, py(3.2) - 8, 'WUE L/KWH', size=7, anchor='start')
    for p in (1.0, 1.2, 1.4, 1.6, 1.8):
        d.text(px(p), py(0) + 14, f'{p:.1f}', size=7)
    for w in (0, 1, 2, 3):
        d.text(px(1.0) - 8, py(w) + 2.5, str(w), size=7, anchor='end')
    d.text(px(1.83) + 7, py(0.05) + 2.5, 'AIR-COOLED', size=7, anchor='start')
    d.text(px(1.52) + 7, py(2.89) + 2.5, 'TOWERS', size=7, anchor='start')
    d.text(px(1.45) + 7, py(1.32) + 2.5, 'ECONOMIZER + TOWERS', size=7, anchor='start')
    d.text(px(1.12) + 8, py(2.18) - 8, 'LARGE, TOWERS', size=7, anchor='start')
    d.text(px(1.09) + 3, py(0.8) - 4, 'LARGE, LIQUID + DRY', size=7, anchor='start')
    d.text(px(1.9), py(3.2) - 8, 'LARGE', size=7, anchor='end')
    d.text(px(1.9) - 48, py(3.2) - 8, 'MIDSIZE', size=7, anchor='end')
    return d


PLATES = {
    'withdrawal-consumption': withdrawal_consumption,
    'cooling-tower': cooling_tower,
    'wue': wue,
}
