"""Plates for The Cloud on the Ground's What comes next, part next1 (sprint 059): rebound, heat-reuse
and hardware-churn. See plates_for.py."""
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


def rebound():
    """A schematic, not data: a demand curve for computing, Q = P^-e with an elasticity e of 1.6
    (above 1, so demand is elastic), and the cost of a unit of computing halved. Use moves along the
    curve from Q1 = 1 to Q2 = 2^1.6, about 3.0, and spending, P x Q, grows from 1 to about 1.5: the
    case in which an efficiency gain raises the total. With e below 1 it would shrink."""
    d = D()
    e = 1.6
    ox, oy = 52, 262                  # origin
    sx, sy = 86.0, 100.0              # plate units per unit of Q and of P
    qmax, pmax = 3.6, 2.2
    X = lambda q: ox + q * sx
    Y = lambda p: oy - p * sy
    p1, p2 = 1.0, 0.5
    q1, q2 = p1 ** -e, p2 ** -e
    d.group('thin')
    for k in range(1, 4):                                   # light grid
        d.line((X(k), oy), (X(k), Y(pmax)))
    for p in (0.5, 1.0, 1.5, 2.0):
        d.line((ox, Y(p)), (X(qmax), Y(p)))
    d.dashed((X(q1), Y(p1)), (X(q1), oy), dash=4, gap=3)    # drop lines to the quantity axis
    d.dashed((X(q2), Y(p2)), (X(q2), oy), dash=4, gap=3)

    d.group()
    d.line((ox, Y(pmax) - 6), (ox, oy), (X(qmax) + 8, oy))  # axes
    _arrow(d, (ox, oy - 10), (ox, Y(pmax) - 6))
    _arrow(d, (X(qmax), oy), (X(qmax) + 8, oy))
    pts = []
    q = 0.34
    while q <= qmax + 1e-9:
        pts.append((X(q), Y(q ** (-1 / e))))
        q += 0.04
    d.line(*pts)                                            # the demand curve
    d.line((ox, Y(p1)), (X(qmax), Y(p1)))                   # cost of a unit, before
    d.line((ox, Y(p2)), (X(qmax), Y(p2)))                   # and after the gain

    d.group('mid')
    d.curve(f'M{X(q1) + 4:.1f} {Y(p1) + 10:.1f} Q {X(1.9):.1f} {Y(0.95):.1f} {X(q2) - 6:.1f} {Y(p2) - 8:.1f}')
    _arrow(d, (X(q2) - 20, Y(p2) - 16), (X(q2) - 6, Y(p2) - 8))
    for (x, y) in ((X(q1), Y(p1)), (X(q2), Y(p2))):
        d.circle(x, y, 3)

    d.group('labels')
    d.text(X(0.08), Y(p1) - 5, 'UNIT COST', size=7, anchor='start')
    d.text(X(0.08), Y(p2) - 5, 'COST HALVED', size=7, anchor='start')
    d.text(X(0.5), Y(2.05), 'DEMAND', size=7, anchor='start')
    d.text(X(q1), oy + 12, 'USE', size=7)
    d.text(X(q2), oy + 12, 'USE x3', size=7)
    d.text(ox - 6, Y(pmax) + 4, 'PRICE', size=7, anchor='end')
    d.text(X(qmax) + 6, oy - 6, 'QUANTITY', size=7, anchor='end')
    d.text(X(2.4), Y(2.05), 'SCHEMATIC', size=7)
    return d


def heat_reuse():
    """A heat pump between a data center's warm-water loop and a district heating loop, as a
    schematic: the evaporator takes heat from the data center's water (at most about 50 C, by the
    UNEP Copenhagen Centre's description of Odense), the compressor, driven by electricity, raises
    the refrigerant's pressure and temperature, the condenser gives the heat to the network's
    water at 70-75 C (Ramboll, Odense), and the expansion valve drops the pressure again."""
    d = D()
    # the cycle: a rectangle with the evaporator on the left, condenser on the right
    lx, rx, ty, by = 150, 250, 92, 212
    d.group('thin')
    d.line((200, 60), (200, 248))                      # centre line of the machine
    d.line((40, 152), (360, 152))                      # datum through the coils
    d.group()
    # refrigerant circuit
    d.line((lx, by - 30), (lx, ty + 30))               # evaporator leg
    d.line((lx, ty + 30), (lx, ty), (188, ty))         # to the compressor
    d.circle(200, ty, 12)                              # compressor
    d.line((212, ty), (rx, ty), (rx, ty + 30))         # hot gas to the condenser
    d.line((rx, ty + 30), (rx, by - 30))               # condenser leg
    d.line((rx, by - 30), (rx, by), (208, by))         # liquid to the valve
    d.line((208, by - 8), (192, by + 8), (192, by - 8), (208, by + 8), closed=True)   # expansion valve
    d.line((192, by), (lx, by), (lx, by - 30))         # back to the evaporator
    # the two coils, as zigzags inside the legs
    for x, sgn in ((lx, -1), (rx, 1)):
        pts = []
        for k in range(9):
            pts.append((x + sgn * (0 if k % 2 == 0 else 10), ty + 32 + k * 7))
        d.line(*pts)
    # data center and homes, as boxes
    _box(d, 20, 112, 62, 80)
    _box(d, 318, 112, 62, 80)
    for k in range(1, 4):                              # racks in the data center
        d.line((20 + k * 15.5, 128), (20 + k * 15.5, 192))
    d.line((318, 140), (349, 118), (380, 140))         # a pitched roof over the homes
    d.group('mid')
    # water loops: data center to evaporator; condenser to the network
    d.line((82, 132), (lx - 16, 132), (lx - 16, 140))
    d.line((lx - 16, 166), (lx - 16, 176), (82, 176))
    _arrow(d, (110, 132), (122, 132))
    _arrow(d, (110, 176), (98, 176))
    d.line((rx + 16, 140), (rx + 16, 132), (318, 132))
    d.line((318, 176), (rx + 16, 176), (rx + 16, 166))
    _arrow(d, (290, 132), (302, 132))
    _arrow(d, (290, 176), (278, 176))
    # electricity into the compressor
    d.line((200, 40), (200, 54), (194, 62), (206, 70), (200, 80))
    _arrow(d, (200, 72), (200, 80))
    # flow direction in the refrigerant
    _arrow(d, (lx, ty + 50), (lx, ty + 40))
    _arrow(d, (rx, by - 50), (rx, by - 40))
    d.group('labels')
    d.text(200, 34, 'ELECTRICITY', size=7)
    d.text(200, ty - 18, 'COMPRESSOR', size=7)
    d.text(lx, by + 20, 'EVAPORATOR', size=7)
    d.text(rx, by + 20, 'CONDENSER', size=7)
    d.text(200, by + 34, 'VALVE', size=7)
    d.text(51, 106, 'DATA CENTER', size=7)
    d.text(349, 106, 'HOMES', size=7)
    d.text(112, 124, '≤50 °C', size=7)
    d.text(286, 124, '70–75 °C', size=7)
    d.text(200, 286, 'SCHEMATIC', size=7)
    return d


# Google's life-cycle study of its TPU v6e (Schneider et al., 2025, table 1), kg CO2e per chip over
# six years: data center construction 109, CPU host manufacturing and transport 260, TPU
# manufacturing and transport 323; operation 5,759 on the grid's mix (location-based) or 2,141 after
# its clean-energy contracts (market-based). End of life is not given separately.
TPU_V6E = {'build': 109, 'cpu': 260, 'tpu': 323, 'use_lb': 5759, 'use_mb': 2141}


def hardware_churn():
    """A server's life as a loop of stages (mine and refine, fabricate chips, assemble and ship, run,
    then refurbish and reuse or recycle back into materials), around two rings drawn to scale from
    Google's TPU v6e study: the outer ring with operation on the grid's mix, the inner with
    operation after clean-energy contracts. Each ring's dark arc is the making (chips, host and
    building); the rest is running it."""
    d = D()
    cx, cy = 200, 152
    v = TPU_V6E
    made = v['build'] + v['cpu'] + v['tpu']
    rings = ((86, made / (made + v['use_lb'])), (64, made / (made + v['use_mb'])))
    stages = [(-90, 'MINE'), (-18, 'FABRICATE'), (54, 'ASSEMBLE'), (126, 'RUN'), (198, 'RECYCLE')]
    d.group('thin')
    for r, _ in rings:
        d.circle(cx, cy, r)
    for a, _ in stages:                                  # radial ticks at each stage
        t = math.radians(a)
        d.line((cx + 96 * math.cos(t), cy + 96 * math.sin(t)), (cx + 104 * math.cos(t), cy + 104 * math.sin(t)))
    d.group()
    # the loop of stages, an arc with arrowheads between stations
    R = 112
    for i, (a, _) in enumerate(stages):
        b = stages[(i + 1) % len(stages)][0]
        if b < a:
            b += 360
        d.arc(cx, cy, R, a + 7, b - 7, n=24)
        t = math.radians(b - 7)
        t0 = math.radians(b - 12)
        _arrow(d, (cx + R * math.cos(t0), cy + R * math.sin(t0)), (cx + R * math.cos(t), cy + R * math.sin(t)), 4)
    # each ring's making share, a heavy arc starting at the top (the mine)
    for r, share in rings:
        d.arc(cx, cy, r, -90, -90 + 360 * share, n=24)
        d.arc(cx, cy, r - 3, -90, -90 + 360 * share, n=24)
    d.group('mid')
    # reuse: a short loop from RECYCLE back to RUN, inside the outer path
    a0, a1 = math.radians(190), math.radians(134)
    p0 = (cx + 100 * math.cos(a0), cy + 100 * math.sin(a0))
    p1 = (cx + 100 * math.cos(a1), cy + 100 * math.sin(a1))
    d.curve(f'M{p0[0]:.1f} {p0[1]:.1f} Q {cx - 58:.1f} {cy + 30:.1f} {p1[0]:.1f} {p1[1]:.1f}')
    _arrow(d, (p1[0] - 6, p1[1] - 8), p1, 4)
    d.group('labels')
    for a, name in stages:
        t = math.radians(a)
        x, y = cx + 128 * math.cos(t), cy + 128 * math.sin(t) + 3
        anchor = 'middle' if abs(math.cos(t)) < 0.3 else ('start' if math.cos(t) > 0 else 'end')
        d.text(x, y, name, size=7, anchor=anchor)
    outer, inner = rings[0][1], rings[1][1]
    d.text(cx, cy - 4, f'MAKING {round(outer * 100)}%', size=7)
    d.text(cx, cy + 6, f'OR {round(inner * 100)}%', size=7)
    d.text(cx - 34, cy + 42, 'REUSE', size=7)
    return d


PLATES = {
    'rebound': rebound,
    'heat-reuse': heat_reuse,
    'hardware-churn': hardware_churn,
}
