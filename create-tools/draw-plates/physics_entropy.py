"""physics plates, part "entropy" (sprint 021): the entropy frame and the first
three frames of the trail "Heat and information". See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def entropy():
    """Heat leaking along a bar from a body at 400 K to one at 300 K (the reading's
    invented example), over the total entropy of the pair rising towards its maximum.

    The bar's steady temperature falls linearly from end to end (drawn as a
    construction line above it). Below, S(t) = S0 + ΔS(1 − e^(−t/τ)), with the
    ceiling it approaches; the step from S0 to the ceiling is 0.83 J/K in the example."""
    d = D()
    # the two bodies and the bar
    hx0, hx1, cx0, cx1, by0, by1 = 40, 118, 282, 360, 42, 128
    bar_y0, bar_y1 = 80, 90
    # the curve's axes
    ox, oy, ax1, ay1 = 60, 268, 362, 158
    s0, smax = 248, 180
    tau = 60.0
    # construction: the bar's temperature profile, the bodies' centre lines, the ceiling
    d.group('thin')
    d.line((hx1, 54), (cx0, 66))
    d.lines([[(hx1, 50), (hx1, 70)], [(cx0, 60), (cx0, 70)]])
    d.line((ox, smax), (ax1, smax))
    d.lines([[(ox + k * 60, oy), (ox + k * 60, oy + 4)] for k in range(1, 6)])
    d.line((ox - 4, s0), (ox + 6, s0))
    # the bodies, the bar and the axes
    d.group()
    d.line((hx0, by0), (hx1, by0), (hx1, by1), (hx0, by1), closed=True)
    d.line((cx0, by0), (cx1, by0), (cx1, by1), (cx0, by1), closed=True)
    d.line((hx1, bar_y0), (cx0, bar_y0))
    d.line((hx1, bar_y1), (cx0, bar_y1))
    d.line((ox, ay1 - 6), (ox, oy), (ax1, oy))
    _arrow(d, ox, ay1 - 6, -math.pi / 2, 4)
    _arrow(d, ax1, oy, 0, 4)
    # the entropy of the pair, rising towards its ceiling
    pts = [(ox + t, s0 - (s0 - smax) * (1 - math.exp(-t / tau))) for t in range(0, int(ax1 - ox) - 6, 3)]
    d.line(*pts)
    # details: the heat's arrows along the bar, hatching for the hot body, a sparse one for the cold
    d.group('mid')
    for x in (150, 200, 250):
        d.line((x - 14, 108), (x + 14, 108))
        _arrow(d, x + 14, 108, 0, 4)
    d.lines([[(hx0 + k, by0), (hx0, by0 + k)] for k in range(10, 78, 10)] +
            [[(hx1, by0 + k - 78 + 10), (hx0 + k - 78 + 10, by1)] for k in range(78, 150, 10) if k - 78 + 10 < 78])
    d.lines([[(cx0 + k, by0), (cx0, by0 + k)] for k in range(20, 78, 20)] +
            [[(cx1, by0 + k - 78), (cx0 + k - 78, by1)] for k in range(98, 156, 20)])
    # labels
    d.group()
    d.text((hx0 + hx1) / 2, by1 + 14, '400 K', size=8)
    d.text((cx0 + cx1) / 2, by1 + 14, '300 K', size=8)
    d.text(200, 124, 'Q', size=9)
    d.text(200, 30, 'ΔS = Q/300 − Q/400 > 0', size=8)
    d.text(ox - 8, ay1 + 2, 'S', size=9, anchor='end')
    d.text(ax1, oy + 16, 't', size=9, anchor='end')
    d.text(ax1 - 2, smax - 6, 'S MAX', size=7, anchor='end')
    d.text(ox + 8, oy + 16, 'THE ENTROPY OF THE PAIR', size=7, anchor='start')
    return d


def maxwells_demon():
    """Maxwell's vessel as Theory of Heat (1871) states it: two halves, a and b, a
    hole with a massless slide, swift molecules let through from a to b and slow
    ones from b to a. Below, the speed distributions of the two halves after some
    sorting, f(v) ∝ (v²/c³) e^(−v²/c²), each normalised, with c larger in b (the hotter side)."""
    import random
    rnd = random.Random(1867)
    d = D()
    x0, x1, y0, y1 = 36, 364, 34, 176
    wx = 200
    hole0, hole1 = 96, 116
    # construction: the wall's centre line through the hole, and the curves' axes' ticks
    ox, oy, w = 60, 272, 300
    d.group('thin')
    d.line((wx, y0 - 10), (wx, y1 + 10))
    d.lines([[(ox + k * 50, oy), (ox + k * 50, oy + 4)] for k in range(1, 7)])
    # the vessel, the dividing wall with its hole, the axes
    d.group()
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)
    d.line((wx, y0), (wx, hole0))
    d.line((wx, hole1), (wx, y1))
    d.line((ox, 196), (ox, oy), (ox + w + 8, oy))
    _arrow(d, ox + w + 8, oy, 0, 4)
    # the slide, drawn open beside the hole, and the demon's eye
    d.line((wx - 3, hole0 - 22), (wx + 3, hole0 - 22), (wx + 3, hole0 - 2), (wx - 3, hole0 - 2), closed=True)
    d.circle(wx + 16, hole0 - 26, 4)
    d.circle(wx + 16, hole0 - 26, 1.2)
    # the molecules: slow ones gathered in a, swift ones in b, each with its velocity
    d.group('mid')
    def place(n, xa, xb, speeds):
        out = []
        while len(out) < n:
            x, y = rnd.uniform(xa, xb), rnd.uniform(y0 + 14, y1 - 26)
            if all(math.dist((x, y), q) > 22 for q in out):
                out.append((x, y))
        for (x, y) in out:
            v = rnd.choice(speeds)
            ang = rnd.uniform(0, 2 * math.pi)
            d.circle(x, y, 2.6)
            ex, ey = x + v * math.cos(ang), y + v * math.sin(ang)
            d.line((x + 2.6 * math.cos(ang), y + 2.6 * math.sin(ang)), (ex, ey))
            _arrow(d, ex, ey, ang, 3)
    place(11, x0 + 14, wx - 26, [5, 6, 7, 8, 9, 14])
    place(10, wx + 34, x1 - 30, [16, 20, 24, 28, 30, 11])
    # a swift molecule passing through the hole from a to b
    d.circle(wx - 6, (hole0 + hole1) / 2, 2.6)
    d.line((wx - 3, (hole0 + hole1) / 2), (wx + 22, (hole0 + hole1) / 2))
    _arrow(d, wx + 22, (hole0 + hole1) / 2, 0, 3)
    # the two speed distributions
    d.group()
    for c, n in ((70, 'a'), (120, 'b')):
        pts = []
        for i in range(0, w + 1, 3):
            v = i
            f = v * v / c ** 3 * math.exp(-(v / c) ** 2)   # normalised: the same number of molecules under each
            pts.append((ox + v, oy - 70 * 70 * math.e * f))
        d.line(*pts)
    # labels
    d.group()
    d.text((x0 + wx) / 2, y1 - 6, 'a · COOLER', size=8)
    d.text((wx + x1) / 2, y1 - 6, 'b · WARMER', size=8)
    d.text(wx + 6, y0 - 8, 'SLIDE AND DEMON', size=7, anchor='start')
    d.text(ox + 70, oy - 78, 'a', size=9)
    d.text(ox + 124, oy - 50, 'b', size=9)
    d.text(ox + w + 8, oy + 16, 'SPEED', size=7, anchor='end')
    d.text(ox - 6, 204, 'f', size=9, anchor='end')
    return d


BOLTZMANN_1877 = [  # Boltzmann's table (1877, section I): 7 molecules sharing 7 units, and each distribution's complexions
    ('0000007', 7), ('0000016', 42), ('0000025', 42), ('0000034', 42), ('0000115', 105),
    ('0000124', 210), ('0000133', 105), ('0000223', 105), ('0001114', 140), ('0001123', 420),
    ('0001222', 140), ('0011113', 105), ('0011122', 210), ('0111112', 42), ('1111111', 1)]


def boltzmann_entropy():
    """Boltzmann's example of 1877: seven molecules sharing seven units of energy.

    Left, the energy ladder with the likeliest state distribution (0001123) on
    it, and the exponential e^(−E/kT) its occupancy approaches (fitted by eye
    to the rungs, as a construction line). Right, the number of complexions
    for each of the fifteen distributions, from his table; they sum to 1,716."""
    import math as m
    assert sum(n for _, n in BOLTZMANN_1877) == 1716
    d = D()
    lx, ly0, step = 44, 252, 25          # the ladder: rung E at y = ly0 − E·step
    lw = 118
    bx, by, bw, gap, hmax = 180, 252, 10, 3.4, 190
    # construction: the ladder's rungs above those used, the exponential, the chart's gridlines
    d.group('thin')
    occupancy = {0: 3, 1: 2, 2: 1, 3: 1}
    d.line(*[(lx + 12 + 18 * (3.2 * m.exp(-e / 1.3) - 1) + 8, ly0 - e * step - 5) for e in [i / 10 for i in range(-2, 46)]])
    d.lines([[(bx - 4, by - hmax * v / 420), (bx + 15 * (bw + gap), by - hmax * v / 420)] for v in (105, 210, 315)])
    # the ladder and the chart's baseline
    d.group()
    d.line((lx, ly0 + 12), (lx, ly0 - 7 * step - 8))
    d.lines([[(lx, ly0 - e * step), (lx + lw, ly0 - e * step)] for e in range(8)])
    d.line((bx - 4, by), (bx + 15 * (bw + gap), by))
    # the molecules on their rungs, and the bars
    for e, k in occupancy.items():
        for i in range(k):
            d.circle(lx + 12 + 18 * i, ly0 - e * step - 5, 4.5)
    for i, (label, n) in enumerate(BOLTZMANN_1877):
        x = bx + i * (bw + gap)
        h = hmax * n / 420
        if n == 420:
            d.line((x, by), (x, by - h), (x + bw, by - h), (x + bw, by), closed=True)
    d.group('mid')
    for i, (label, n) in enumerate(BOLTZMANN_1877):
        x = bx + i * (bw + gap)
        h = max(hmax * n / 420, 1.5)
        if n != 420:
            d.line((x, by), (x, by - h), (x + bw, by - h), (x + bw, by), closed=True)
    # labels
    d.group()
    for e in range(8):
        d.text(lx - 6, ly0 - e * step + 3, str(e), size=7, anchor='end')
    d.text(lx + lw / 2, ly0 + 26, '0 0 0 1 1 2 3', size=8)
    d.text(bx + 9 * (bw + gap) + bw / 2, by - hmax - 6, '420', size=8)
    d.text(bx + 7.5 * (bw + gap), by + 16, 'THE FIFTEEN DISTRIBUTIONS', size=7)
    d.text(bx + 7.5 * (bw + gap), by + 28, '1,716 COMPLEXIONS', size=7)
    d.text(lx - 6, ly0 - 7 * step - 16, 'E', size=8, anchor='end')
    d.text(lx + 30, ly0 - 3.5 * step + 3, 'e^(−E/kT)', size=7, anchor='start')
    return d


def szilard_engine():
    """Szilard's one-molecule engine (1929): the four steps of the cycle in a row,
    and below them the isotherm p = kT/V for one molecule, with the work of the
    expansion from V/2 to V, kT ln 2, hatched under it. The weight the piston
    lifts in step 3 is left out; its rod leaves through the end wall."""
    d = D()
    pw, ph, px0, py0, gap = 78, 58, 22, 34, 18
    xs = [px0 + i * (pw + gap) for i in range(4)]
    # the p-V diagram
    ox, oy, vx1, vtop = 110, 262, 330, 138
    V = 180                     # plate units for the full volume
    k = (oy - 212) * V          # p·V = constant: p(V) = k/V, so that p(V) sits 50 above the axis
    def P(v):
        return oy - k / v
    # construction: the cylinders' midlines, the volumes V/2 and V, hatching under the isotherm
    d.group('thin')
    d.lines([[(x + pw / 2, py0 - 4), (x + pw / 2, py0 + ph + 4)] for x in xs])
    d.lines([[(ox + V / 2, oy), (ox + V / 2, P(V / 2))], [(ox + V, oy), (ox + V, P(V))]])
    for i in range(1, 18):
        v = V / 2 + i * V / 36
        d.line((ox + v, oy), (ox + v, P(v)))
    # the cylinders and the diagram's axes
    d.group()
    for x in xs:
        d.line((x, py0), (x + pw, py0), (x + pw, py0 + ph), (x, py0 + ph), closed=True)
    d.line((ox, vtop), (ox, oy), (vx1 + 20, oy))
    _arrow(d, ox, vtop, -math.pi / 2, 4)
    _arrow(d, vx1 + 20, oy, 0, 4)
    d.line(*[(ox + v, P(v)) for v in range(int(V * 0.4), V + 24, 3)])
    # details: partition, molecule, piston and weight in each step
    d.group('mid')
    cy = py0 + ph / 2
    # 1: partition sliding in, molecule somewhere
    x = xs[0]
    d.line((x + pw / 2, py0 - 10), (x + pw / 2, py0 + ph * 0.7))
    d.circle(x + 20, cy + 8, 3)
    # 2: partition in, the eye looking at the left half
    x = xs[1]
    d.line((x + pw / 2, py0), (x + pw / 2, py0 + ph))
    d.circle(x + 20, cy + 8, 3)
    d.circle(x + 20, py0 - 12, 4)
    d.circle(x + 20, py0 - 12, 1.2)
    d.line((x + 20, py0 - 7), (x + 20, cy + 2))
    # 3: the partition as a piston, pushed right, its rod out through the end wall to the load
    x = xs[2]
    d.line((x + pw * 0.72, py0), (x + pw * 0.72, py0 + ph))
    d.line((x + pw * 0.72, cy), (x + pw + 6, cy))
    d.circle(x + 30, cy - 6, 3)
    d.line((x + pw * 0.72 + 2, cy - 12), (x + pw * 0.72 + 12, cy - 12))
    _arrow(d, x + pw * 0.72 + 12, cy - 12, 0, 3)
    # 4: the partition out, the cylinder as it began
    x = xs[3]
    d.circle(x + 58, cy - 10, 3)
    # labels
    d.group()
    for i, x in enumerate(xs):
        d.text(x + pw / 2, py0 + ph + 16, str(i + 1), size=8)
    d.text(xs[0] + pw / 2, py0 - 16, 'INSERT', size=6)
    d.text(xs[1] + pw / 2, py0 - 16, 'LOOK', size=6)
    d.text(xs[2] + pw / 2, py0 - 16, 'EXPAND', size=6)
    d.text(xs[3] + pw / 2, py0 - 16, 'RESET', size=6)
    d.text(ox - 6, vtop + 4, 'p', size=9, anchor='end')
    d.text(vx1 + 20, oy + 16, 'V', size=9, anchor='end')
    d.text(ox + V / 2, oy + 12, 'V/2', size=7)
    d.text(ox + V, oy + 12, 'V', size=7)
    d.text(ox + V + 8, oy - 14, '← kT ln 2', size=8, anchor='start')
    d.text(ox + V * 0.5 + 8, P(V * 0.5) - 6, 'pV = kT', size=7, anchor='start')
    return d


PLATES = {'szilard-engine': szilard_engine,
          'entropy': entropy, 'maxwells-demon': maxwells_demon,
          'boltzmann-entropy': boltzmann_entropy}
