"""ai plates, segments "Winters and booms" and the start of "Learning from data" (sprint 006). See ai.py."""
import math

from plates import D


def _arrow(d, x, y, ang, s=5):
    """A small open arrowhead at (x, y) pointing along `ang` degrees."""
    a = math.radians(ang)
    for da in (150, -150):
        b = a + math.radians(da)
        d.line((x + s * math.cos(b), y + s * math.sin(b)), (x, y))


def lighthill():
    """The combinatorial explosion: a search tree of branching factor 3, and its growth plotted beside it."""
    d = D()
    top, dy, depth, b = 40, 52, 4, 3
    x0, x1 = 20, 236
    # construction: depth lines and the tree's envelope
    d.group('thin')
    d.lines([[(x0, top + k * dy), (x1, top + k * dy)] for k in range(depth + 1)])
    apex = ((x0 + x1) / 2, top)
    d.line((x0 + 2, top + depth * dy), apex, (x1 - 2, top + depth * dy))
    # the tree: node positions per level, evenly spread
    levels = []
    for k in range(depth + 1):
        n = b ** k
        w = (x1 - x0 - 4) * (k / depth) if k else 0
        cx = (x0 + x1) / 2
        levels.append([(cx - w / 2 + (w * (i + 0.5) / n if n > 1 else w / 2), top + k * dy) for i in range(n)])
    d.group()
    segs = []
    for k in range(depth - 1):
        for i, p in enumerate(levels[k]):
            for j in range(b):
                segs.append([p, levels[k + 1][i * b + j]])
    d.lines(segs)
    for k in range(depth):
        for x, y in levels[k]:
            if k < 3:
                d.circle(x, y, 3.2 - 0.6 * k)
    # the leaves: 81 short strokes, too many to draw as nodes
    d.group('mid')
    d.lines([[p, (p[0] + (q[0] - p[0]) * 0.55, p[1] + dy * 0.55)]
             for i, p in enumerate(levels[depth - 1]) for q in levels[depth][i * b:i * b + b]])
    # the plot: 3^d against d, and a straight line for comparison
    px, py, pw, ph = 268, 248, 112, 196
    d.group('thin')
    d.lines([[(px + pw * k / 4, py), (px + pw * k / 4, py - ph)] for k in range(5)])
    d.lines([[(px, py - ph * k / 4), (px + pw, py - ph * k / 4)] for k in range(5)])
    d.group()
    d.line((px, py - ph - 6), (px, py), (px + pw + 6, py))
    pts = [(px + pw * t / 40, py - ph * (3 ** (4 * t / 40) - 1) / 80) for t in range(41)]
    d.line(*pts)
    d.group('mid')
    d.line((px, py), (px + pw, py - ph * 12 / 80))
    for k in range(5):
        d.circle(px + pw * k / 4, py - ph * (3 ** k - 1) / 80, 2)
    d.group()
    for k in range(depth + 1):
        d.text(x0 - 6, top + k * dy + 3, str(k), size=7, anchor='end')
    for k in range(5):
        d.text(px + pw * k / 4, py + 12, str(k), size=7)
    d.text(px + pw - 4, py - ph + 12, '3ⁿ', size=9, anchor='end')
    d.text(px + pw / 2, py + 26, 'DEPTH', size=7)
    d.text((x0 + x1) / 2, top + depth * dy + 26, '1 · 3 · 9 · 27 · 81', size=8)
    return d


def expert_systems():
    """A rule-based system: the rule base, the inference engine's match–select–act cycle, working memory."""
    d = D()
    # construction: the axis the three parts sit on, and their centres
    d.group('thin')
    cy = 140
    d.line((20, cy), (380, cy))
    d.lines([[(x, 40), (x, 250)] for x in (80, 200, 320)])
    ex, ey, er = 200, cy, 46
    d.circle(ex, ey, er + 14)
    # the rule base: a stack of rule cards, the back ones showing only their top and right edges
    d.group()
    for k in range(4, 0, -1):
        x, y = 40 + k * 5, 70 - k * 5 + 20
        d.line((x, y), (x + 80, y), (x + 80, y + 52))
    fx, fy = 40, 90
    d.line((fx, fy), (fx + 80, fy), (fx + 80, fy + 52), (fx, fy + 52), closed=True)
    d.group('mid')
    d.lines([[(fx + 8, fy + 12 + 10 * i), (fx + 66 - 14 * (i % 2), fy + 12 + 10 * i)] for i in range(4)])
    # the inference engine: three arcs of one cycle, each with its arrowhead
    d.group()
    d.circle(ex, ey, er)
    d.group('mid')
    for a0 in (-80, 40, 160):
        d.arc(ex, ey, er - 12, a0, a0 + 100, n=30)
        a = math.radians(a0 + 100)
        _arrow(d, ex + (er - 12) * math.cos(a), ey + (er - 12) * math.sin(a), a0 + 190, s=5)
    # working memory: a grid of facts, some set
    wx, wy, cs = 282, 96, 19
    d.group()
    d.line((wx, wy), (wx + 4 * cs, wy), (wx + 4 * cs, wy + 5 * cs), (wx, wy + 5 * cs), closed=True)
    d.group('thin')
    d.lines([[(wx + i * cs, wy), (wx + i * cs, wy + 5 * cs)] for i in range(1, 4)]
            + [[(wx, wy + j * cs), (wx + 4 * cs, wy + j * cs)] for j in range(1, 5)])
    d.group('mid')
    for (i, j) in [(0, 0), (2, 1), (1, 2), (3, 2), (0, 4), (2, 3)]:
        d.line((wx + i * cs + 5, wy + j * cs + 10), (wx + i * cs + 8, wy + j * cs + 14), (wx + i * cs + 14, wy + j * cs + 5))
    # the flows: rules and facts in, new facts out
    d.group()
    d.line((140, cy - 8), (ex - er - 4, cy - 8))
    _arrow(d, ex - er - 4, cy - 8, 0)
    d.line((wx - 4, cy - 8), (ex + er + 4, cy - 8))
    _arrow(d, ex + er + 4, cy - 8, 180)
    d.line((ex + er + 4, cy + 10), (wx - 4, cy + 10))
    _arrow(d, wx - 4, cy + 10, 0)
    d.group()
    d.text(90, 58, 'RULE BASE', size=8)
    d.text(ex, 64, 'INFERENCE ENGINE', size=8)
    d.text(wx + 2 * cs, 86, 'WORKING MEMORY', size=8)
    d.text(ex, ey - 2, 'MATCH', size=7)
    d.text(ex, ey + 8, 'SELECT · ACT', size=7)
    d.text(80, 160, 'IF … THEN …', size=8)
    d.text(ex, 262, 'KNOWLEDGE, NOT SEARCH', size=8)
    return d


def backprop():
    """A layered network: activity forward, error derivatives backward, and the sigmoid whose slope carries them."""
    d = D()
    layers = [(40, 4), (130, 3), (220, 2)]
    ys = lambda n: [136 + (i - (n - 1) / 2) * 56 for i in range(n)]
    nodes = [[(x, y) for y in ys(n)] for x, n in layers]
    # construction: the layer axes
    d.group('thin')
    d.lines([[(x, 30), (x, 270)] for x, _ in layers])
    d.line((20, 136), (240, 136))
    # forward connections
    d.group('mid')
    d.lines([[a, b] for k in range(2) for a in nodes[k] for b in nodes[k + 1]])
    # the units
    d.group()
    for layer in nodes:
        for x, y in layer:
            d.circle(x, y, 9)
    # the backward pass: curved arrows beneath the net, output to input
    d.group()
    for (xa, _), (xb, _) in [(layers[2], layers[1]), (layers[1], layers[0])]:
        mx = (xa + xb) / 2
        d.curve(f'M{xa - 8} 252 Q{mx} 276 {xb + 8} 252')
        _arrow(d, xb + 8, 252, 215)
    d.curve('M60 22 Q130 4 200 22')
    _arrow(d, 200, 22, 20)
    # the sigmoid, with a tangent at one point: its slope is y(1 - y)
    sx, sy, sw, sh = 268, 210, 112, 112
    sig = lambda x: 1 / (1 + math.exp(-x))
    d.group('thin')
    d.line((sx, sy), (sx + sw, sy))
    d.line((sx, sy - sh), (sx + sw, sy - sh))
    d.line((sx + sw / 2, sy + 6), (sx + sw / 2, sy - sh - 6))
    d.group()
    pts = [(sx + sw * t / 60, sy - sh * sig((t / 60 - 0.5) * 12)) for t in range(61)]
    d.line(*pts)
    x0 = -1.0
    y0 = sig(x0)
    slope = y0 * (1 - y0) * sh * 12 / sw
    px, py = sx + sw * (x0 / 12 + 0.5), sy - sh * y0
    d.group('mid')
    d.line((px - 34, py + 34 * slope), (px + 34, py - 34 * slope))
    d.circle(px, py, 2.5)
    d.group()
    d.text(sx + sw / 2, sy + 20, 'y = 1/(1+e⁻ˣ)', size=8)
    d.text(sx + sw / 2, sy - sh - 12, "y' = y(1−y)", size=8)
    d.text(130, 290, '∂E/∂w · BACKWARD', size=8)
    d.text(130, 14, 'FORWARD', size=8)
    for (x, _), s in zip(layers, ('IN', 'HIDDEN', 'OUT')):
        d.text(x, 240, s, size=7)
    return d


def lisp_collapse():
    """A Lisp machine's tagged word and the cons cells it was built to chase."""
    d = D()
    x0, y0, cw, ch = 30, 56, 9.4, 26
    # construction: bit ticks and the word's bounds
    d.group('thin')
    d.lines([[(x0 + i * cw, y0 - 6), (x0 + i * cw, y0)] for i in range(37)])
    d.line((x0, y0 + ch + 20), (x0 + 36 * cw, y0 + ch + 20))
    # the 36-bit word: 4 tag bits, 32 data bits
    d.group()
    d.line((x0, y0), (x0 + 36 * cw, y0), (x0 + 36 * cw, y0 + ch), (x0, y0 + ch), closed=True)
    d.line((x0 + 4 * cw, y0), (x0 + 4 * cw, y0 + ch))
    d.group('mid')
    d.lines([[(x0 + i * cw, y0 + ch - 7), (x0 + i * cw, y0 + ch)] for i in range(5, 36)])
    d.lines([[(x0 + i * cw * 0.5, y0 + ch), (x0 + i * cw * 0.5 + 8, y0)] for i in range(0, 8)])
    # brackets
    d.group('thin')
    for a, b_ in ((0, 4), (4, 36)):
        xa, xb = x0 + a * cw, x0 + b_ * cw
        d.line((xa, y0 + ch + 6), (xa, y0 + ch + 12), (xb, y0 + ch + 12), (xb, y0 + ch + 6))
    # a list of three cons cells, the last cdr NIL
    cx, cy, bw, bh, gap = 40, 176, 34, 28, 42
    d.group()
    cells = []
    for k in range(3):
        x = cx + k * (2 * bw + gap)
        cells.append(x)
        d.line((x, cy), (x + 2 * bw, cy), (x + 2 * bw, cy + bh), (x, cy + bh), closed=True)
        d.line((x + bw, cy), (x + bw, cy + bh))
    d.group('mid')
    for k, x in enumerate(cells):
        # car points down to an atom
        d.line((x + bw / 2, cy + bh / 2), (x + bw / 2, cy + bh + 34))
        _arrow(d, x + bw / 2, cy + bh + 34, 90)
        d.circle(x + bw / 2, cy + bh + 46, 11)
        if k < 2:
            d.line((x + 1.5 * bw, cy + bh / 2), (cells[k + 1] - 2, cy + bh / 2))
            _arrow(d, cells[k + 1] - 2, cy + bh / 2, 0)
        else:
            d.line((x + bw, cy + bh), (x + 2 * bw, cy))
        d.circle(x + bw / 2, cy + bh / 2, 1.8)
        if k < 2:
            d.circle(x + 1.5 * bw, cy + bh / 2, 1.8)
    d.group()
    d.text(x0 + 2 * cw, y0 - 14, 'TAG', size=8)
    d.text(x0 + 20 * cw, y0 - 14, 'DATA · 32 BITS', size=8)
    d.text(x0 + 18 * cw, y0 + ch + 36, '36-BIT WORD · SYMBOLICS 3600', size=8)
    for x in cells:
        d.text(x + bw / 2, cy - 8, 'CAR', size=7)
        d.text(x + 1.5 * bw, cy - 8, 'CDR', size=7)
    d.text(cells[2] + 2 * bw + 8, cy + bh / 2 + 3, 'NIL', size=8, anchor='start')
    for x, s in zip(cells, 'ABC'):
        d.text(x + bw / 2, cy + bh + 49, s, size=8)
    return d


def lenet():
    """The 1989 zip-code network: a 5×5 kernel sliding over a 16×16 digit, feature maps shrinking to ten outputs."""
    d = D()
    gx, gy, gs, n = 24, 70, 128, 16
    c = gs / n
    # construction: the input grid
    d.group('thin')
    d.lines([[(gx + i * c, gy), (gx + i * c, gy + gs)] for i in range(n + 1)]
            + [[(gx, gy + j * c), (gx + gs, gy + j * c)] for j in range(n + 1)])
    # the input: a hand-drawn 3 sampled on the grid
    d.group()
    d.line((gx, gy), (gx + gs, gy), (gx + gs, gy + gs), (gx, gy + gs), closed=True)
    d.curve(f'M{gx + 38} {gy + 30} C{gx + 62} {gy + 12} {gx + 98} {gy + 22} {gx + 84} {gy + 52} '
            f'C{gx + 76} {gy + 64} {gx + 62} {gy + 64} {gx + 56} {gy + 64} '
            f'C{gx + 100} {gy + 64} {gx + 104} {gy + 108} {gx + 72} {gy + 110} C{gx + 56} {gy + 112} {gx + 42} {gy + 104} {gx + 36} {gy + 96}')
    # the kernel window, 5×5 cells
    kx, ky = gx + 8 * c, gy
    d.group('mid')
    d.line((kx, ky), (kx + 5 * c, ky), (kx + 5 * c, ky + 5 * c), (kx, ky + 5 * c), closed=True)
    # feature maps: H1 12 maps of 8×8, drawn as a stack of 4, and H2 12 of 4×4 as a stack of 3
    stacks = [(196, 104, 56, 4, 8), (290, 124, 30, 3, 4)]
    fronts = []
    for x, y, s, m, cells in stacks:
        d.group()
        for k in range(m - 1, -1, -1):
            ox, oy = x + k * 6, y - k * 6
            d.line((ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s), closed=True)
        fronts.append((x, y, s, cells))
        d.group('thin')
        cc = s / cells
        d.lines([[(x + i * cc, y), (x + i * cc, y + s)] for i in range(1, cells)]
                + [[(x, y + j * cc), (x + s, y + j * cc)] for j in range(1, cells)])
    # projection lines: the kernel window to one unit of H1, a patch of H1 to one unit of H2
    (hx, hy, hs, hc), (h2x, h2y, h2s, h2c) = fronts
    ux, uy = hx + 3 * hs / hc, hy + 2 * hs / hc
    d.group('thin')
    for px, py in ((kx, ky), (kx + 5 * c, ky), (kx, ky + 5 * c), (kx + 5 * c, ky + 5 * c)):
        d.line((px, py), (ux + hs / hc / 2, uy + hs / hc / 2))
    v = (h2x + h2s / h2c * 1.5, h2y + h2s / h2c * 1.5)
    for px, py in ((ux - 4, uy - 4), (ux + 20, uy - 4), (ux - 4, uy + 20), (ux + 20, uy + 20)):
        d.line((px, py), v)
    # H3: 30 units as a column, and 10 outputs
    d.group('mid')
    for i in range(10):
        d.circle(356, 76 + i * 16, 2.6)
    d.group()
    for i in range(10):
        d.circle(384, 76 + i * 16, 4.2)
    d.group('thin')
    d.lines([[(h2x + h2s + 14, h2y + h2s / 2 - 10), (356, 76 + i * 16)] for i in range(0, 10, 3)]
            + [[(356, 76 + i * 16), (384, 76 + j * 16)] for i in (0, 9) for j in (0, 3, 6, 9)])
    d.group()
    d.text(gx + gs / 2, gy + gs + 16, '16×16', size=8)
    d.text(hx + hs / 2 + 9, hy + hs + 16, '12 @ 8×8', size=8)
    d.text(h2x + h2s / 2 + 6, h2y + h2s + 16, '12 @ 4×4', size=8)
    d.text(370, 250, '30 → 10', size=8)
    d.text(kx + 2.5 * c, ky - 6, '5×5', size=7)
    d.text(200, 280, 'SHARED WEIGHTS · LEARNED KERNELS', size=8)
    return d


def lstm():
    """The 1997 memory cell: a self-loop of weight 1.0 guarded by two multiplicative gates, and why it matters."""
    d = D()
    cx, cy, r = 200, 92, 26
    # construction: the signal axis and the cell's centre lines
    d.group('thin')
    d.line((20, cy), (380, cy))
    d.line((cx, 20), (cx, 150))
    d.circle(cx, cy, r + 18)
    # the cell: the constant error carousel, a unit feeding itself with weight 1.0
    d.group()
    d.circle(cx, cy, r)
    d.arc(cx, cy - r - 16, 16, 150, 390, n=40)
    _arrow(d, cx + 16 * math.cos(math.radians(30)), cy - r - 16 + 16 * math.sin(math.radians(30)), 120)
    # the gates: input on the left, output on the right, each a × on the line
    gates = [(100, cy), (300, cy)]
    for gxp, gyp in gates:
        d.circle(gxp, gyp, 13)
        d.line((gxp - 7, gyp - 7), (gxp + 7, gyp + 7))
        d.line((gxp - 7, gyp + 7), (gxp + 7, gyp - 7))
    d.group('mid')
    d.line((30, cy), (100 - 13, cy))
    d.line((100 + 13, cy), (cx - r, cy))
    _arrow(d, cx - r, cy, 0)
    d.line((cx + r, cy), (300 - 13, cy))
    _arrow(d, 300 - 13, cy, 0)
    d.line((300 + 13, cy), (370, cy))
    _arrow(d, 370, cy, 0)
    # gate controls, from below
    for gxp, gyp in gates:
        d.line((gxp, gyp + 50), (gxp, gyp + 13))
        _arrow(d, gxp, gyp + 13, 270)
        d.circle(gxp, gyp + 56, 6)
    # below: an error signal carried back through 60 steps, decaying without the carousel
    px, py, pw, ph = 40, 270, 320, 80
    d.group('thin')
    d.lines([[(px + pw * k / 6, py), (px + pw * k / 6, py - ph)] for k in range(7)])
    d.line((px, py - ph), (px + pw, py - ph))
    d.group()
    d.line((px, py - ph - 4), (px, py), (px + pw + 4, py))
    d.line(*[(px + pw * t / 60, py - ph * 0.9 ** t) for t in range(61)])
    d.group('mid')
    d.line((px, py - ph), (px + pw, py - ph))
    d.group()
    d.text(cx, cy + 4, 'CEC', size=8)
    d.text(cx, cy - r - 38, '1.0', size=8)
    d.text(100, cy - 22, 'IN GATE', size=7)
    d.text(300, cy - 22, 'OUT GATE', size=7)
    d.text(px + pw, py - ph - 8, 'ERROR, CONSTANT', size=7, anchor='end')
    d.text(px + 90, py - 30, '0.9ⁿ', size=8, anchor='start')
    d.text(px + pw / 2, py + 16, 'STEPS BACK IN TIME', size=7)
    return d


PLATES = {
    'lighthill': lighthill,
    'expert-systems': expert_systems,
    'backprop': backprop,
    'lisp-collapse': lisp_collapse,
    'lenet': lenet,
    'lstm': lstm,
}
