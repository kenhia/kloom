"""ai plates, segment "The frontier" (sprint 006). See ai.py."""
import math

from plates import D


def multimodal():
    """CLIP's contrastive matrix: an image encoder and a text encoder, and the diagonal they learn."""
    d = D()
    n, cell = 6, 26
    x0, y0 = 170, 104  # top-left of the N x N similarity matrix
    xs = [x0 + i * cell for i in range(n + 1)]
    ys = [y0 + j * cell for j in range(n + 1)]
    # construction: the matrix grid, and the projection lines from each vector into it
    d.group('thin')
    d.lines([[(x, y0), (x, ys[-1])] for x in xs] + [[(x0, y), (xs[-1], y)] for y in ys])
    d.lines([[(x0 + (i + .5) * cell, 72), (x0 + (i + .5) * cell, y0)] for i in range(n)])
    d.lines([[(138, y0 + (j + .5) * cell), (x0, y0 + (j + .5) * cell)] for j in range(n)])
    # the object: two encoders as trapezoids, and the matrix frame
    d.group()
    d.line((x0, 18), (xs[-1], 18), (xs[-1] - 26, 58), (x0 + 26, 58), closed=True)  # text encoder
    d.line((52, y0), (52, ys[-1]), (112, ys[-1] - 30), (112, y0 + 30), closed=True)  # image encoder
    d.line((x0, y0), (xs[-1], y0), (xs[-1], ys[-1]), (x0, ys[-1]), closed=True)
    # the two sets of embedding vectors, one per caption and per image
    d.group('mid')
    for i in range(n):
        cx = x0 + (i + .5) * cell
        d.line((cx - 6, 64), (cx + 6, 64), (cx + 6, 72), (cx - 6, 72), closed=True)
        cy = y0 + (j := i) * cell + cell / 2
        d.line((122, cy - 6), (130, cy - 6), (130, cy + 6), (122, cy + 6), closed=True)
    d.line((82, 60), (82, y0 - 4))  # the image goes in from above
    d.line((x0 + n * cell / 2, 8), (x0 + n * cell / 2, 18))
    # the diagonal: the matching pairs the loss pulls together
    d.group()
    for i in range(n):
        cx, cy = x0 + (i + .5) * cell, y0 + (i + .5) * cell
        d.circle(cx, cy, 8)
    d.line((x0 + 4, y0 + 4), (xs[-1] - 4, ys[-1] - 4))
    # an image, as a picture frame with a horizon, feeding the image encoder
    d.group('mid')
    d.line((58, 22), (106, 22), (106, 58), (58, 58), closed=True)
    d.line((58, 50), (72, 38), (82, 46), (94, 32), (106, 44))
    d.circle(70, 30, 3)
    d.group()
    d.text(x0 + n * cell / 2, 42, 'TEXT ENCODER', size=8)
    d.text(84, ys[-1] + 16, 'IMAGE ENCODER', size=8)
    d.text(x0 + n * cell / 2, ys[-1] + 16, 'IMAGE · TEXT PAIRS', size=8)
    d.text(xs[-1] + 12, y0 + 3 * cell + 3, 'I·T', size=8, anchor='start')
    return d


def agents():
    """The agent loop: a model at the hub, tools on the rim, and think, act, observe going round."""
    d = D()
    cx, cy = 200, 150
    r_tool, r_loop = 118, 62
    tools = ['SHELL', 'EDITOR', 'TESTS', 'BROWSER', 'SEARCH', 'FILES']
    ang = [-90 + 60 * k for k in range(6)]
    pos = [(cx + r_tool * math.cos(math.radians(a)) * 1.25, cy + r_tool * math.sin(math.radians(a)) * .95) for a in ang]
    # construction: the orbit of the tools and the spokes of the protocol
    d.group('thin')
    d.ellipse(cx, cy, r_tool * 1.25, r_tool * .95)
    d.circle(cx, cy, r_loop)
    d.lines([[(cx + 30 * math.cos(math.radians(a)), cy + 30 * math.sin(math.radians(a))), p] for a, p in zip(ang, pos)])
    # the model at the hub
    d.group()
    d.line((cx - 30, cy - 18), (cx + 30, cy - 18), (cx + 30, cy + 18), (cx - 30, cy + 18), closed=True)
    # the tools on the rim, each a port on the same interface
    d.group('mid')
    for x, y in pos:
        d.line((x - 30, y - 11), (x + 30, y - 11), (x + 30, y + 11), (x - 30, y + 11), closed=True)
    # the loop: three arcs, each ending in an arrowhead
    d.group()
    for a0 in (-80, 40, 160):
        a1 = a0 + 100
        d.arc(cx, cy, r_loop, a0, a1, n=30)
        t = math.radians(a1)
        ex, ey = cx + r_loop * math.cos(t), cy + r_loop * math.sin(t)
        tx, ty = -math.sin(t), math.cos(t)  # direction of travel
        nx, ny = math.cos(t), math.sin(t)
        d.line((ex - 7 * tx + 4 * nx, ey - 7 * ty + 4 * ny), (ex, ey), (ex - 7 * tx - 4 * nx, ey - 7 * ty - 4 * ny))
    d.group()
    d.text(cx, cy + 3, 'MODEL', size=9)
    for (x, y), name in zip(pos, tools):
        d.text(x, y + 3, name, size=7)
    for a, word in ((-30, 'THINK'), (90, 'ACT'), (210, 'OBSERVE')):
        t = math.radians(a)
        d.text(cx + (r_loop + 14) * math.cos(t) * 1.1, cy + (r_loop + 14) * math.sin(t) + 3, word, size=7)
    return d


def reasoning_models():
    """Test-time compute: a search tree of thoughts, one path kept, over a log-linear accuracy curve."""
    d = D()
    # the chart on the left: accuracy against thinking compute, on a log axis
    ax, ay, aw, ah = 34, 262, 150, 170
    d.group('thin')
    d.lines([[(ax + aw * k / 4, ay), (ax + aw * k / 4, ay - ah)] for k in range(5)]
            + [[(ax, ay - ah * k / 4), (ax + aw, ay - ah * k / 4)] for k in range(5)])
    for k in range(5):  # minor log ticks between decades
        for m in range(2, 10):
            x = ax + aw * (k + math.log10(m)) / 4
            if x < ax + aw:
                d.line((x, ay), (x, ay + 3))
    d.group()
    d.line((ax, ay - ah - 6), (ax, ay), (ax + aw + 6, ay))
    d.line((ax + 6, ay - 22), (ax + aw - 6, ay - ah + 18))
    d.group('mid')
    for k in range(6):
        x = ax + 6 + (aw - 12) * k / 5
        y = ay - 22 - (ah - 40) * k / 5
        d.circle(x, y, 3)
    # the tree on the right: branching thoughts, most abandoned
    root = (292, 34)
    levels = [[root]]
    widths = [0, 104, 52, 26]
    d.group('thin')
    for depth in range(1, 4):
        nxt = []
        for (px, py) in levels[-1]:
            for s in (-1, 1):
                nxt.append((px + s * widths[depth] / 2, py + 62))
        levels.append(nxt)
    d.lines([[p, c] for depth in range(3) for i, p in enumerate(levels[depth]) for c in levels[depth + 1][2 * i:2 * i + 2]])
    d.group('mid')
    for depth in range(1, 4):
        for (x, y) in levels[depth]:
            d.circle(x, y, 2.5)
    # the kept chain of thought: one path, drawn heavy, to the answer
    path = [0, 1, 2, 5]  # indices by depth
    pts = [levels[depth][i] for depth, i in enumerate(path)]
    d.group()
    d.line(*pts)
    for x, y in pts:
        d.circle(x, y, 5)
    lx, ly = pts[-1]
    d.line((lx - 12, ly + 14), (lx + 12, ly + 14), (lx + 12, ly + 30), (lx - 12, ly + 30), closed=True)
    d.line((lx, ly + 5), (lx, ly + 14))
    d.group()
    d.text(ax + aw / 2, ay + 16, 'THINKING COMPUTE (LOG)', size=7)
    d.text(ax - 8, ay - ah / 2, 'ACC', size=7, anchor='end')
    d.text(root[0], root[1] - 10, 'PROBLEM', size=8)
    d.text(lx + 18, ly + 26, 'ANSWER', size=8, anchor='start')
    return d


def open_weights():
    """A network whose weights are the release, inside the nested frames of code and data."""
    d = D()
    cols = [(52, 4), (110, 6), (168, 6), (226, 3)]
    cy = 150
    nodes = [[(x, cy + (i - (n - 1) / 2) * 34) for i in range(n)] for x, n in cols]
    # construction: the layer axes and the nested outlines of what can be released
    d.group('thin')
    d.lines([[(x, 30), (x, 270)] for x, _ in cols])
    d.line((260, 30), (386, 30), (386, 270), (260, 270), closed=True)
    d.line((274, 64), (372, 64), (372, 256), (274, 256), closed=True)
    # the weights: every connection between layers
    d.group('mid')
    d.lines([[a, b] for k in range(3) for a in nodes[k] for b in nodes[k + 1]])
    # the neurons
    d.group()
    for layer in nodes:
        for x, y in layer:
            d.circle(x, y, 7)
    # the innermost frame, a tensor file: a grid of numbers, and the brace from the network to it
    d.group()
    gx, gy, gw, gh = 288, 112, 70, 108
    d.line((gx, gy), (gx + gw, gy), (gx + gw, gy + gh), (gx, gy + gh), closed=True)
    d.group('mid')
    d.lines([[(gx + gw * k / 5, gy), (gx + gw * k / 5, gy + gh)] for k in range(1, 5)]
            + [[(gx, gy + gh * k / 8), (gx + gw, gy + gh * k / 8)] for k in range(1, 8)])
    top, bot = nodes[1][0][1], nodes[1][-1][1]
    d.curve(f'M238 {top} C246 {top} 240 {cy} 250 {cy} C240 {cy} 246 {bot} 238 {bot}')
    d.line((252, cy), (gx - 4, cy))
    d.line((gx - 10, cy - 4), (gx - 4, cy), (gx - 10, cy + 4))
    d.group()
    d.text(gx + gw / 2, gy - 10, 'WEIGHTS', size=8)
    d.text(323, 80, 'CODE', size=8)
    d.text(323, 46, 'DATA', size=8)
    return d


def compute():
    """A GPU package in plan: the die of streaming multiprocessors, flanked by stacks of HBM."""
    d = D()
    px, py, pw, ph = 40, 40, 320, 220  # the package substrate
    ix, iy, iw, ih = 70, 66, 260, 168  # the interposer
    dx, dy, dw, dh = 136, 80, 128, 140  # the die
    # construction: centre lines and dimension lines
    d.group('thin')
    d.line((200, 20), (200, 280))
    d.line((20, 150), (380, 150))
    d.line((dx, dy + dh + 30), (dx + dw, dy + dh + 30))
    d.lines([[(dx, dy + dh + 24), (dx, dy + dh + 36)], [(dx + dw, dy + dh + 24), (dx + dw, dy + dh + 36)]])
    # the package and interposer
    d.group()
    d.line((px, py), (px + pw, py), (px + pw, py + ph), (px, py + ph), closed=True)
    d.group('mid')
    d.line((ix, iy), (ix + iw, iy), (ix + iw, iy + ih), (ix, iy + ih), closed=True)
    # the die
    d.group()
    d.line((dx, dy), (dx + dw, dy), (dx + dw, dy + dh), (dx, dy + dh), closed=True)
    # the streaming multiprocessors: a grid of blocks, and the cache strip across the middle
    d.group('mid')
    cols, rows = 8, 8
    m = 6
    cw, ch = (dw - 2 * m) / cols, (dh - 2 * m - 10) / rows
    for r in range(rows):
        for c in range(cols):
            x = dx + m + c * cw
            y = dy + m + r * ch + (10 if r >= rows // 2 else 0)
            d.line((x + 1, y + 1), (x + cw - 1, y + 1), (x + cw - 1, y + ch - 1), (x + 1, y + ch - 1), closed=True)
    # the memory stacks: three a side, each a stack of layers
    d.group()
    for side in (-1, 1):
        sx = dx - 50 if side < 0 else dx + dw + 10
        for k in range(3):
            sy = dy + 4 + k * 46
            d.line((sx, sy), (sx + 40, sy), (sx + 40, sy + 40), (sx, sy + 40), closed=True)
            d.lines([[(sx + 4, sy + 8 + 6 * j), (sx + 36, sy + 8 + 6 * j)] for j in range(5)])
    d.group()
    d.text(200, dy - 5, 'GPU DIE', size=8)
    d.text(dx - 30, dy + dh + 20, 'HBM', size=8)
    d.text(dx + dw + 30, dy + dh + 20, 'HBM', size=8)
    d.text(200, py + ph + 14, 'PACKAGE · INTERPOSER', size=8)
    return d


PLATES = {
    'multimodal': multimodal,
    'agents': agents,
    'reasoning-models': reasoning_models,
    'open-weights': open_weights,
    'compute': compute,
}
