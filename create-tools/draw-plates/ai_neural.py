"""ai plates, trail "From perceptron to deep learning" (sprint 006). See plates_for.py."""
import math

from plates import D


def arrow(d, a, b, head=5):
    """A line from a to b with an open arrowhead at b."""
    (x0, y0), (x1, y1) = a, b
    t = math.atan2(y1 - y0, x1 - x0)
    d.line(a, b)
    d.line((x1 - head * math.cos(t - .45), y1 - head * math.sin(t - .45)), b,
           (x1 - head * math.cos(t + .45), y1 - head * math.sin(t + .45)))


def soma(d, cx, cy, r, dendrites, rnd_len=24):
    """A cell body with branching dendrites at the given angles (degrees)."""
    d.circle(cx, cy, r)
    segs = []
    for a in dendrites:
        t = math.radians(a)
        x0, y0 = cx + r * math.cos(t), cy + r * math.sin(t)
        x1, y1 = cx + (r + rnd_len) * math.cos(t), cy + (r + rnd_len) * math.sin(t)
        segs.append([(x0, y0), (x1, y1)])
        for s in (-28, 28):
            u = math.radians(a + s)
            segs.append([(x1, y1), (x1 + 11 * math.cos(u), y1 + 11 * math.sin(u))])
    d.lines(segs)


def hebbian_learning():
    """Cell A's axon ending on cell B, the spike trains that show A firing just before B,
    and the synaptic knob Hebb supposed would grow."""
    d = D()
    ya, yb, x0, x1 = 44, 76, 40, 360
    spikes = [70, 128, 186, 244, 302]
    lag = 9
    # construction: the two time axes and the lines that pair each A spike with the B spike after it
    d.group('thin')
    d.lines([[(x0, ya), (x1, ya)], [(x0, yb), (x1, yb)]])
    d.lines([[(t, ya - 16), (t, yb + 6)] for t in spikes])
    # the spike trains: A, and B just after
    d.group('mid')
    d.lines([[(t, ya), (t, ya - 14)] for t in spikes] + [[(t + lag, yb), (t + lag, yb - 14)] for t in spikes])
    # the object: two neurons, A's axon ending in a knob on B's body
    ax, ay, bx, by = 88, 186, 292, 190
    d.group()
    soma(d, ax, ay, 16, [130, 180, 230, 270])
    soma(d, bx, by, 22, [300, 350, 40, 90])
    d.curve(f'M{ax + 16} {ay} C{ax + 70} {ay - 26} {bx - 110} {by + 22} {bx - 32} {by - 2}')
    d.circle(bx - 27.5, by - 3, 5)
    # the inset: the knob magnified, before and after
    ix, iy, ir = 196, 250, 34
    d.group('thin')
    d.circle(bx - 27.5, by - 3, 11)
    d.line((bx - 36, by + 6), (ix + ir * math.cos(math.radians(-40)), iy + ir * math.sin(math.radians(-40))))
    d.group('mid')
    d.circle(ix, iy, ir)
    # B's membrane as an arc, the axon coming in from the left, a small knob (before, thin) and a grown one
    d.arc(ix + 70, iy, 58, 150, 210)
    d.line((ix - 32, iy - 4), (ix - 10, iy - 4))
    d.group()
    d.arc(ix - 6, iy, 8, -90, 90, ry=10)
    d.line((ix - 10, iy - 10), (ix - 6, iy - 10))
    d.line((ix - 10, iy + 10), (ix - 6, iy + 10))
    d.group()
    d.text(x0 - 10, ya - 3, 'A', size=9, anchor='end')
    d.text(x0 - 10, yb - 3, 'B', size=9, anchor='end')
    d.text(ax, ay + 44, 'CELL A', size=8)
    d.text(bx + 30, by + 58, 'CELL B', size=8)
    d.text(ix + ir + 12, iy + 26, 'KNOB GROWS', size=8, anchor='start')
    d.text(x1, yb + 20, 'A FIRES JUST BEFORE B', size=8, anchor='end')
    return d


def adaline():
    """Widrow and Hoff's adaptive linear element: weighted inputs, a sum, a quantizer, and the
    error taken before the quantizer and fed back to every weight; beside it, the bowl of
    squared error that the LMS rule walks down."""
    d = D()
    xs = 40
    ys = [60, 100, 140, 180]
    wx, sx, sy = 110, 180, 120
    qx = 236
    # construction: input rails and the error bowl's axes
    d.group('thin')
    d.lines([[(xs + 8, y), (wx - 10, y)] for y in ys])
    bx, by, bw = 300, 262, 80
    d.lines([[(bx - bw / 2 - 6, by), (bx + bw / 2 + 6, by)], [(bx, by + 4), (bx, by - 76)]])
    # the element: inputs, weight knobs with pointers, the summing junction, the quantizer
    d.group()
    for y in ys:
        d.circle(xs, y, 7)
        d.circle(wx, y, 10)
    d.circle(sx, sy, 14)
    d.line((qx, sy - 14), (qx + 36, sy - 14), (qx + 36, sy + 14), (qx, sy + 14), closed=True)
    d.group('mid')
    for k, y in enumerate(ys):
        t = math.radians(-60 + 35 * k)
        d.line((wx, y), (wx + 8 * math.cos(t), y + 8 * math.sin(t)))
        d.line((wx + 10, y), (sx - 14 * math.cos(math.atan2(y - sy, sx - wx)), sy + 14 * math.sin(math.atan2(y - sy, wx - sx)) * -1))
    d.line((sx + 5, sy - 7), (sx - 6, sy - 7), (sx, sy), (sx - 6, sy + 7), (sx + 5, sy + 7))
    d.line((qx + 8, sy + 6), (qx + 18, sy + 6), (qx + 18, sy - 6), (qx + 28, sy - 6))
    arrow(d, (sx + 14, sy), (qx, sy))
    arrow(d, (qx + 36, sy), (qx + 70, sy))
    # the error loop: s taken off before the quantizer, compared with the desired response d
    ex, ey = 206, 196
    d.group()
    d.circle(ex, ey, 9)
    d.line((ex - 4, ey), (ex + 4, ey))
    arrow(d, (sx + 12, sy + 8), (ex - 5, ey - 7))
    arrow(d, (ex, ey + 44), (ex, ey + 9))
    d.line((ex - 9, ey), (wx, ey), (wx, ys[-1] + 10))
    for y in ys[:-1]:
        arrow(d, (wx - 14, y + 26), (wx - 7, y + 7), head=4)
    d.line((wx, ey), (wx - 14, ey), (wx - 14, ys[0] + 26))
    # the bowl: mean squared error against one weight, and the steps down it
    d.group()
    bowl = lambda u: by - 6 - 62 * (u / (bw / 2)) ** 2
    pts = [(bx + u, bowl(u)) for u in [i - bw / 2 for i in range(0, bw + 1, 4)]]
    d.line(*pts)
    d.group('mid')
    w = -34
    steps = []
    for _ in range(5):
        e = bowl(w)
        steps.append((bx + w, e))
        w *= .55
    for (px, py) in steps:
        d.circle(px, py, 2.5)
    d.lines([[steps[i], steps[i + 1]] for i in range(len(steps) - 1)])
    d.group()
    d.text(xs, ys[0] - 14, 'x', size=9)
    d.text(wx, ys[0] - 16, 'w', size=9)
    d.text(qx + 18, sy - 22, 'SGN', size=8)
    d.text(ex + 14, ey + 3, 'ε = d − s', size=8, anchor='start')
    d.text(ex, ey + 56, 'd', size=9)
    d.text(bx, by + 18, 'ERROR² · ONE WEIGHT', size=8)
    return d


def perceptrons_book():
    """XOR on the unit square: two classes at opposite corners, and the lines that try and fail
    to separate them; beside it, AND, which one line does separate."""
    d = D()
    ox, oy, s = 50, 250, 190
    corners = {(0, 0): 0, (1, 1): 0, (0, 1): 1, (1, 0): 1}
    P = lambda u, v: (ox + u * s, oy - v * s)
    # construction: axes, the unit square's grid, and a fan of candidate lines, all failing
    d.group('thin')
    d.lines([[(ox - 10, oy), (ox + s + 24, oy)], [(ox, oy + 10), (ox, oy - s - 24)]])
    d.lines([[P(.5, 0), P(.5, 1)], [P(0, .5), P(1, .5)]])
    fan = []
    for k in range(7):
        t = math.radians(-20 + k * 30)
        cx, cy = P(.5, .5)
        L = s * .78
        fan.append([(cx - L * math.cos(t), cy + L * math.sin(t)), (cx + L * math.cos(t), cy - L * math.sin(t))])
    d.lines(fan)
    # the object: the square and its four points; open circles output 0, crosses output 1
    d.group()
    d.line(P(0, 0), P(1, 0), P(1, 1), P(0, 1), closed=True)
    for (u, v), c in corners.items():
        x, y = P(u, v)
        if c:
            d.lines([[(x - 7, y - 7), (x + 7, y + 7)], [(x - 7, y + 7), (x + 7, y - 7)]])
        else:
            d.circle(x, y, 7)
    # AND, small, on the right: one line is enough
    ax, ay, a = 290, 170, 80
    Q = lambda u, v: (ax + u * a, ay - v * a)
    d.group('thin')
    d.lines([[(ax - 6, ay), (ax + a + 12, ay)], [(ax, ay + 6), (ax, ay - a - 12)]])
    d.group('mid')
    d.line(Q(0, 0), Q(1, 0), Q(1, 1), Q(0, 1), closed=True)
    for (u, v) in [(0, 0), (1, 0), (0, 1)]:
        d.circle(*Q(u, v), 5)
    x, y = Q(1, 1)
    d.lines([[(x - 5, y - 5), (x + 5, y + 5)], [(x - 5, y + 5), (x + 5, y - 5)]])
    d.group()
    d.line(Q(.45, 1.25), Q(1.25, .45))
    d.group()
    d.text(ox + s / 2, oy + 26, 'XOR · NO LINE SEPARATES', size=8)
    d.text(ax + a / 2, ay + 24, 'AND · ONE LINE DOES', size=8)
    d.text(ox - 8, oy + 14, '0', size=8)
    d.text(ox + s, oy + 14, '1', size=8)
    d.text(ox - 18, oy - s + 12, '1', size=8)
    return d


def neocognitron():
    """The 1980 simulation's seven layers in oblique projection, from the 16 x 16 input to one
    cell per plane, with a 5 x 5 receptive field on the input converging on one S-cell."""
    d = D()
    # layer side lengths in cells (Fukushima 1980, section 5), drawn at a common scale
    layers = [('U0', 16), ('S1', 16), ('C1', 10), ('S2', 8), ('C2', 6), ('S3', 2), ('C3', 1)]
    k = 7.2           # units per cell
    dx, sh = 52, .5   # spacing between layers; the oblique shear of a plane's depth
    base_y = 170

    def plane(x, n, off=0):
        w = n * k
        h = w * .9
        # a vertical square seen obliquely: depth axis sheared up and right
        p0 = (x + off, base_y + h / 2 - off)
        p1 = (x + off + w * sh, base_y + h / 2 - w * sh - off)
        p2 = (p1[0], p1[1] - h)
        p3 = (p0[0], p0[1] - h)
        return [p0, p1, p2, p3]

    xs = [22 + i * dx for i in range(len(layers))]
    # construction: the cell grid on the input plane, and the axis the layers stand on
    d.group('thin')
    p0, p1, p2, p3 = plane(xs[0], 16)
    grid = []
    for i in range(17):
        f = i / 16
        grid.append([(p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f),
                     (p3[0] + (p2[0] - p3[0]) * f, p3[1] + (p2[1] - p3[1]) * f)])
        grid.append([(p0[0] + (p3[0] - p0[0]) * f, p0[1] + (p3[1] - p0[1]) * f),
                     (p1[0] + (p2[0] - p1[0]) * f, p1[1] + (p2[1] - p1[1]) * f)])
    d.lines(grid)
    d.line((12, base_y + 70), (388, base_y + 70))
    # the object: each layer as a plane; S- and C-layers drawn as a stack of cell-planes
    d.group()
    for (name, n), x in zip(layers, xs):
        d.line(*plane(x, n), closed=True)
    d.group('mid')
    for (name, n), x in zip(layers[1:], xs[1:]):
        for j in (1, 2):
            d.line(*plane(x, n, off=3.5 * j)[:3])
    # a 5 x 5 receptive field on the input, converging on one S1 cell; then on to C1
    def at(pl, u, v):
        q0, q1, q2, q3 = pl
        return (q0[0] + (q1[0] - q0[0]) * u + (q3[0] - q0[0]) * v, q0[1] + (q1[1] - q0[1]) * u + (q3[1] - q0[1]) * v)
    inp = plane(xs[0], 16)
    rf = [at(inp, u, v) for u, v in [(4 / 16, 6 / 16), (9 / 16, 6 / 16), (9 / 16, 11 / 16), (4 / 16, 11 / 16)]]
    s1 = at(plane(xs[1], 16), 6.5 / 16, 8.5 / 16)
    c1 = at(plane(xs[2], 10), 4.5 / 10, 5.5 / 10)
    d.group()
    d.line(*rf, closed=True)
    d.group('thin')
    d.lines([[p, s1] for p in rf] + [[s1, c1]])
    d.group()
    d.circle(*s1, 2.5)
    d.circle(*c1, 2.5)
    d.group()
    for (name, n), x in zip(layers, xs):
        d.text(x + n * k * sh / 2, base_y + 86, name, size=8)
    d.text(200, 34, 'S EXTRACTS · C TOLERATES SHIFT', size=8)
    return d


def hopfield_network():
    """An energy landscape as a wireframe surface: stored patterns are its valleys, and a
    distorted input rolls down into the nearest one. Beside it, a fully connected net."""
    d = D()
    wells = [(-1.1, -.4, 1.0), (.9, .6, 1.2), (.7, -.9, .8), (-.5, 1.0, .7)]

    def z(u, v):
        return -sum(a * math.exp(-((u - x) ** 2 + (v - y) ** 2) / .28) for x, y, a in wells)

    cx, cy, sx, sy, sz = 176, 176, 70, 30, 46

    def proj(u, v):
        return (cx + sx * u + 22 * v, cy + sy * v - sz * z(u, v))

    us = [-2 + i * .1 for i in range(41)]
    vs = [-1.6 + j * .533 for j in range(7)]
    # construction: the energy axis and the base plane's outline
    d.group('thin')
    corners = [(cx + sx * u + 22 * v, cy + sy * v) for u, v in [(-2, -1.6), (2, -1.6), (2, 1.6), (-2, 1.6)]]
    d.line(*corners, closed=True)
    # Beside the back-left corner, but on the plate: that corner is at its edge, and 14 units left of it
    # the axis was drawn off the plate (sprint 050).
    ax, ay = max(corners[0][0] - 14, 8), corners[0][1]
    d.line((ax, ay + 40), (ax, ay - 70))
    # the object: the surface, as lines of constant v
    d.group()
    d.lines([[proj(u, v) for u in us] for v in vs])
    # secondary: cross lines of constant u, sparser
    d.group('mid')
    d.lines([[proj(u, -1.6 + j * .1) for j in range(33)] for u in [-2 + i * .8 for i in range(6)]])
    # the ball's path: gradient descent from a start point to the well it belongs to
    u, v = .15, .05
    path = [(u, v)]
    for _ in range(60):
        e = 1e-3
        gu = (z(u + e, v) - z(u - e, v)) / (2 * e)
        gv = (z(u, v + e) - z(u, v - e)) / (2 * e)
        u, v = u - .06 * gu, v - .06 * gv
        path.append((u, v))
    d.group()
    pts = [proj(a, b) for a, b in path]
    d.line(*pts)
    bx, by = pts[0]
    d.circle(bx, by - 5, 5)
    ex, ey = pts[-1]
    d.circle(ex, ey, 2.5)
    # a small Hopfield net: six units, every pair joined
    nx, ny, nr = 340, 48, 26
    nodes = [(nx + nr * math.cos(math.radians(90 + 60 * i)), ny - nr * math.sin(math.radians(90 + 60 * i))) for i in range(6)]
    d.group('mid')
    d.lines([[nodes[i], nodes[j]] for i in range(6) for j in range(i + 1, 6)])
    d.group()
    for p in nodes:
        d.circle(*p, 4)
    d.group()
    d.text(ax, ay - 76, 'E', size=9)
    d.text(bx - 10, by - 12, 'INPUT', size=8, anchor='end')
    d.text(nx - nr - 10, ny + 3, 'EVERY PAIR JOINED', size=8, anchor='end')
    d.text(200, 286, 'MEMORIES ARE VALLEYS', size=8)
    return d


def boltzmann_machine():
    """A restricted Boltzmann machine: visible and hidden layers joined only across, never within;
    beside it, the Boltzmann distribution at a high and a low temperature."""
    d = D()
    nv, nh = 6, 4
    vy, hy = 230, 90
    vxs = [40 + i * 44 for i in range(nv)]
    hxs = [84 + i * 44 for i in range(nh)]
    # construction: the two layers' rails, and the forbidden within-layer links, faint
    d.group('thin')
    d.lines([[(20, vy), (280, vy)], [(20, hy), (280, hy)]])
    d.curve(' '.join(f'M{vxs[i]} {vy + 8} Q{(vxs[i] + vxs[i + 1]) / 2} {vy + 26} {vxs[i + 1]} {vy + 8}' for i in range(nv - 1)))
    # every visible unit to every hidden unit
    d.group('mid')
    d.lines([[(x, vy - 9), (h, hy + 9)] for x in vxs for h in hxs])
    d.group()
    for x in vxs:
        d.circle(x, vy, 9)
    for h in hxs:
        d.circle(h, hy, 9)
    # the Boltzmann distribution p ∝ exp(-E/T) for T = 1 and T = 3
    px, py, pw, ph = 300, 250, 84, 150
    d.group('thin')
    d.lines([[(px, py), (px + pw + 6, py)], [(px, py + 4), (px, py - ph - 6)]])
    d.group()
    d.line(*[(px + e * pw / 4, py - ph * math.exp(-e / .8)) for e in [i * .1 for i in range(41)]])
    d.group('mid')
    d.line(*[(px + e * pw / 4, py - ph * math.exp(-e / 3)) for e in [i * .1 for i in range(41)]])
    d.group()
    d.text(20, hy - 16, 'HIDDEN', size=8, anchor='start')
    d.text(20, vy + 38, 'VISIBLE · NO LINKS WITHIN A LAYER', size=8, anchor='start')
    d.text(px + pw / 2, py + 16, 'ENERGY', size=8)
    d.text(px + 6, py - ph - 10, 'p ∝ e^(−E/T)', size=8, anchor='start')
    d.text(px + 50, py - 80, 'HOT', size=8, anchor='start')
    d.text(px + 56, py - 12, 'COLD', size=8, anchor='start')
    return d


def deep_belief_nets():
    """The 2006 digit network: a 28 x 28 image, two layers of 500, a top layer of 2000 joined to
    ten label units; each pair of layers is an RBM trained greedily, one on top of the last."""
    d = D()
    rows = [('28 × 28 PIXELS', 784, 262), ('500', 500, 196), ('500', 500, 130), ('2000', 2000, 58)]
    cx = 170
    width = lambda n: 60 + 180 * math.log10(n) / math.log10(2000)
    # construction: the centre line and the brackets that mark each greedy stage
    d.group('thin')
    d.line((cx, 40), (cx, 286))
    for i in range(3):
        y0, y1 = rows[i][2], rows[i + 1][2]
        x = cx + width(2000) / 2 + 22 + i * 12
        d.line((x - 6, y0), (x, y0), (x, y1), (x - 6, y1))
    # the object: each layer as a row of units (sampled), the image as a grid
    d.group()
    for name, n, y in rows[1:]:
        w = width(n)
        m = int(w / 11)
        for i in range(m):
            d.circle(cx - w / 2 + (i + .5) * w / m, y, 3.5)
    gw = width(784)
    d.line((cx - gw / 2, rows[0][2] - 12), (cx + gw / 2, rows[0][2] - 12), (cx + gw / 2, rows[0][2] + 12), (cx - gw / 2, rows[0][2] + 12), closed=True)
    # labels: ten units beside the top layer
    lx = 30
    for i in range(10):
        d.circle(lx + i * 9, 24, 3)
    d.group('thin')
    d.lines([[(cx - gw / 2 + i * gw / 14, rows[0][2] - 12), (cx - gw / 2 + i * gw / 14, rows[0][2] + 12)] for i in range(1, 14)])
    # connections: lower layers directed downwards (generative), top pair undirected
    d.group('mid')
    for i in range(3):
        (_, n0, y0), (_, n1, y1) = rows[i], rows[i + 1]
        w0, w1 = width(n0), width(n1)
        segs = []
        for f in [j / 6 for j in range(7)]:
            for g in [j / 4 for j in range(5)]:
                segs.append([(cx - w1 / 2 + f * w1, y1 + 5), (cx - w0 / 2 + g * w0, y0 - (13 if i == 0 else 5))])
        d.lines(segs[::3])
        if i < 2:
            arrow(d, (cx - w1 / 2 - 14, y1 + 4), (cx - w0 / 2 - 14, y0 - 6), head=5)
    d.lines([[(lx + i * 9, 27), (cx - width(2000) / 2 + 20 + i * 18, rows[3][2] - 5)] for i in range(0, 10, 3)])
    d.group()
    for name, n, y in rows[1:]:
        d.text(cx + width(2000) / 2 + 64, y + 3, name, size=8, anchor='start')
    # The image's label is longer than the others: it ends at the plate's edge rather than past it (sprint 050).
    d.text(396, rows[0][2] + 3, rows[0][0], size=8, anchor='end')
    d.text(lx + 40, 12, '10 LABELS', size=8)
    return d


PLATES = {
    'hebbian-learning': hebbian_learning,
    'adaline': adaline,
    'perceptrons-book': perceptrons_book,
    'neocognitron': neocognitron,
    'hopfield-network': hopfield_network,
    'boltzmann-machine': boltzmann_machine,
    'deep-belief-nets': deep_belief_nets,
}
