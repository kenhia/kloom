"""ai plates, segments "Learning from data" (from Deep Blue) and "Deep learning" (sprint 006). See plates_for.py."""
import math

from plates import D

GO_COLS = 'ABCDEFGHJKLMNOPQRST'  # Go boards skip the letter I


def deep_blue():
    """Alpha-beta search: a game tree cut back by pruning, beside the chess chip's 8x8 move generator."""
    d = D()
    x0, x1, top, ply = 20, 250, 44, 64
    levels = 4  # the root and three plies
    # construction: one line per ply
    d.group('thin')
    d.lines([[(x0, top + i * ply), (x1, top + i * ply)] for i in range(levels)])
    for i in range(1, levels):
        d.text(x0 - 4, top + i * ply + 3, str(i), size=7, anchor='end')
    # the tree, branching three ways: the first line is searched in full, and later
    # siblings are cut once a refutation is found (the last child of each later node)
    kept, cut, marks = [], [], []

    def node(path, lo, hi):
        x, y = (lo + hi) / 2, top + len(path) * ply
        if len(path) == levels - 1:
            return (x, y)
        w = (hi - lo) / 3
        for k in range(3):
            kp = path + (k,)
            kid = node(kp, lo + k * w, lo + (k + 1) * w)
            pruned = any(c == 2 for c in kp[1:]) and kp[0] != 0
            (cut if pruned else kept).append([(x, y), kid])
            if pruned and kp[-1] == 2 and not any(c == 2 for c in kp[1:-1]):
                mx, my = x + (kid[0] - x) * 0.4, y + (kid[1] - y) * 0.4
                marks.append([(mx - 6, my - 3), (mx + 6, my + 3)])
        return (x, y)

    root = node((), x0, x1)
    d.group()
    d.lines(kept)
    d.circle(root[0], root[1], 5)
    d.group('thin')
    d.lines(cut)
    d.group('mid')
    d.lines(marks)
    # the chess chip: a die with its 8x8 move generator, "a chess board in miniature"
    cx, cy, s = 318, 150, 104
    d.group('thin')
    d.line((cx - s / 2 - 16, cy), (cx + s / 2 + 16, cy))
    d.line((cx, cy - s / 2 - 16), (cx, cy + s / 2 + 16))
    d.group()
    d.line((cx - s / 2, cy - s / 2), (cx + s / 2, cy - s / 2), (cx + s / 2, cy + s / 2), (cx - s / 2, cy + s / 2), closed=True)
    g = s * 0.72
    d.line((cx - g / 2, cy - g / 2), (cx + g / 2, cy - g / 2), (cx + g / 2, cy + g / 2), (cx - g / 2, cy + g / 2), closed=True)
    d.group('mid')
    step = g / 8
    d.lines([[(cx - g / 2 + i * step, cy - g / 2), (cx - g / 2 + i * step, cy + g / 2)] for i in range(1, 8)]
            + [[(cx - g / 2, cy - g / 2 + i * step), (cx + g / 2, cy - g / 2 + i * step)] for i in range(1, 8)])
    pins = []
    for i in range(10):
        t = -s / 2 + (i + 0.5) * s / 10
        pins += [[(cx + t, cy - s / 2), (cx + t, cy - s / 2 - 6)], [(cx + t, cy + s / 2), (cx + t, cy + s / 2 + 6)],
                 [(cx - s / 2, cy + t), (cx - s / 2 - 6, cy + t)], [(cx + s / 2, cy + t), (cx + s / 2 + 6, cy + t)]]
    d.lines(pins)
    d.group()
    d.text(135, top + (levels - 1) * ply + 26, 'ALPHA–BETA · CUTOFFS', size=8)
    d.text(cx, cy + s / 2 + 34, '8×8 MOVE GENERATOR', size=8)
    d.text(cx, 30, '× 480 CHIPS', size=8)
    return d


def imagenet():
    """WordNet's noun hierarchy with a stack of labelled images hung from each leaf synset."""
    d = D()
    top, gap = 40, 52
    # construction: the depth levels of the hierarchy
    d.group('thin')
    d.lines([[(24, top + i * gap), (376, top + i * gap)] for i in range(4)])
    for i in range(4):
        d.text(18, top + i * gap + 3, str(i + 1), size=7, anchor='end')
    # the tree: 1 -> 2 -> 4 -> 8 synsets
    xs = [[200], [110, 290], [65, 155, 245, 335], [42, 88, 132, 178, 222, 268, 312, 358]]
    edges = []
    for lvl in range(3):
        for i, x in enumerate(xs[lvl]):
            for c in (2 * i, 2 * i + 1):
                edges.append([(x, top + lvl * gap + 5), (xs[lvl + 1][c], top + (lvl + 1) * gap - 5)])
    d.group()
    d.lines(edges)
    for lvl, row in enumerate(xs):
        for x in row:
            d.circle(x, top + lvl * gap, 5)
    # each leaf holds a stack of images, and each image is checked three times
    d.group('mid')
    ly = top + 3 * gap
    for x in xs[3]:
        d.line((x, ly + 5), (x, ly + 16))
        for k in range(3):
            ox, oy = x - 14 + k * 3, ly + 16 + k * 5
            d.line((ox, oy), (ox + 22, oy), (ox + 22, oy + 16), (ox, oy + 16), closed=True)
    d.group('thin')
    for x in xs[3]:
        d.line((x - 11, ly + 38), (x - 4, ly + 30), (x + 1, ly + 35), (x + 6, ly + 28), (x + 11, ly + 38))
    d.group()
    d.text(200, top - 12, 'MAMMAL', size=8)
    d.text(200, 276, 'SYNSETS · IMAGES · CHECKED BY VOTE', size=8)
    return d


def alexnet():
    """The network as volumes in oblique projection, split across two GPUs, narrowing into the classifier."""
    d = D()
    k = (math.cos(math.radians(35)) * 0.5, -math.sin(math.radians(35)) * 0.5)  # oblique depth axis

    def box(x, y, w, h, depth):
        """Front face at (x, y) of w by h, receding `depth` along the oblique axis; returns its edge paths."""
        dx, dy = depth * k[0], depth * k[1]
        f = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        b = [(px + dx, py + dy) for px, py in f]
        return [f + [f[0]], [f[0], b[0], b[1], b[2], f[2]], [f[1], b[1]]]

    mid = 150
    # five convolutional stages: (x, width, half-height, depth)
    stages = [(20, 8, 70, 60), (78, 12, 48, 44), (134, 14, 30, 34), (182, 14, 30, 34), (228, 14, 24, 30)]
    # construction: the split between the GPUs, and the projection lines between stages
    d.group('thin')
    d.line((12, mid), (390, mid))
    proj = []
    for (xa, wa, ha, da), (xb, wb, hb, db) in zip(stages, stages[1:]):
        for sgn in (-1, 1):
            proj.append([(xa + wa, mid + sgn * ha), (xb, mid + sgn * hb)])
    d.lines(proj)
    # the object: each stage drawn twice, one half per GPU
    d.group()
    for x, w, h, dep in stages:
        for y in (mid - h - 3, mid + 3):
            d.lines(box(x, y, w, h, dep))
    # detail: the kernels sampled from one stage into the next
    d.group('mid')
    for (xa, wa, ha, da), (xb, wb, hb, db) in zip(stages, stages[1:]):
        for y0 in (mid - ha * 0.6, mid + ha * 0.4):
            d.lines(box(xa + wa + 2, y0, 5, 5, 6))
    # the classifier: two dense layers and the 1000-way output, as columns of units
    d.group()
    cols = [(300, 26), (330, 26), (362, 20)]
    for x, n in cols:
        d.line((x, mid - 100), (x, mid + 100))
        d.lines([[(x - 3, mid - 100 + i * 200 / n), (x + 3, mid - 100 + i * 200 / n)] for i in range(n + 1)])
    d.group('thin')
    d.lines([[(270, mid - 30), (300, mid - 100)], [(270, mid + 30), (300, mid + 100)],
             [(300, mid - 100), (330, mid - 100)], [(300, mid + 100), (330, mid + 100)],
             [(330, mid - 100), (362, mid - 100)], [(330, mid + 100), (362, mid + 100)]])
    d.group()
    d.text(160, 40, 'GPU 1', size=8)
    d.text(160, 268, 'GPU 2', size=8)
    d.text(24, 238, '224²', size=8, anchor='start')
    d.text(362, 268, '1000', size=8)
    return d


def word2vec():
    """Four words in a vector space: king - man + woman lands next to queen."""
    d = D()
    ox, oy = 70, 250
    # construction: a grid and the axes of two of the space's hundreds of dimensions
    d.group('thin')
    d.lines([[(ox + i * 30, 40), (ox + i * 30, oy)] for i in range(1, 11)]
            + [[(ox, oy - i * 30), (380, oy - i * 30)] for i in range(1, 8)])
    d.group()
    d.line((ox, 30), (ox, oy), (390, oy))
    d.lines([[(ox - 4, 36), (ox, 30), (ox + 4, 36)], [(384, oy - 4), (390, oy), (384, oy + 4)]])
    man, woman = (150, 200), (205, 150)
    king, queen = (285, 170), (340, 120)
    offset = (woman[0] - man[0], woman[1] - man[1])
    guess = (king[0] + offset[0] + 4, king[1] + offset[1] + 3)  # the arithmetic lands near, not on, queen

    def arrow(a, b):
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        h = [(b[0] - 7 * math.cos(ang - 0.4), b[1] - 7 * math.sin(ang - 0.4)),
             (b[0] - 7 * math.cos(ang + 0.4), b[1] - 7 * math.sin(ang + 0.4))]
        d.lines([[a, b], [h[0], b, h[1]]])

    # detail: the vectors from the origin, and the two parallel gender offsets
    d.group('thin')
    d.lines([[(ox, oy), p] for p in (man, woman, king, queen)])
    d.group('mid')
    arrow(man, woman)
    arrow(king, guess)
    d.line(man, king)
    d.line(woman, queen)
    d.group()
    for p in (man, woman, king, queen):
        d.circle(p[0], p[1], 4)
    d.circle(guess[0], guess[1], 9)
    d.group()
    d.text(man[0] - 8, man[1] + 16, 'MAN', size=8)
    d.text(woman[0] - 16, woman[1] - 10, 'WOMAN', size=8)
    d.text(king[0] + 6, king[1] + 16, 'KING', size=8)
    d.text(queen[0] - 6, queen[1] - 16, 'QUEEN', size=8)
    d.text(ox, 22, 'KING − MAN + WOMAN ≈ QUEEN', size=8, anchor='start')
    return d


def gans():
    """The one-dimensional picture of the GAN paper: z mapped to x, the data, the generator, and D at one half."""
    d = D()
    x0, x1 = 30, 370
    zy, xy, base = 270, 200, 190  # the z line, the x line, and the density baseline
    h = 120  # height of a density peak

    def gauss(x, mu, sig):
        return math.exp(-0.5 * ((x - mu) / sig) ** 2)

    mu_d, sd_d = 230, 34  # the data
    mu_g, sd_g = 170, 44  # the generator, still learning
    xs = [x0 + i * (x1 - x0) / 120 for i in range(121)]
    # construction: the two lines, and the level of one half
    d.group('thin')
    d.line((x0, zy), (x1, zy))
    d.line((x0, xy), (x1, xy))
    d.line((x0, base - h / 2), (x1, base - h / 2))
    # the mapping x = G(z): evenly spaced z carried through the generator's inverse CDF
    maps = []
    for i in range(1, 16):
        u = i / 16
        # inverse normal CDF by bisection on erf
        lo, hi = -4.0, 4.0
        for _ in range(40):
            m = (lo + hi) / 2
            if 0.5 * (1 + math.erf(m / math.sqrt(2))) < u:
                lo = m
            else:
                hi = m
        gx = mu_g + sd_g * (lo + hi) / 2
        zx = x0 + (x1 - x0) * u
        maps.append([(zx, zy), (gx, xy)])
    d.group('mid')
    d.lines(maps)
    # the data distribution, and the generator's
    d.group()
    d.line(*[(x, base - h * gauss(x, mu_d, sd_d)) for x in xs])
    d.group('mid')
    d.line(*[(x, base - h * gauss(x, mu_g, sd_g) * sd_d / sd_g) for x in xs])
    # the discriminator: D = p_data / (p_data + p_g), dashed
    dvals = []
    for x in xs:
        pd, pg = gauss(x, mu_d, sd_d) / sd_d, gauss(x, mu_g, sd_g) / sd_g
        dvals.append((x, base - h * pd / (pd + pg + 1e-12)))
    d.group()
    d.lines([dvals[i:i + 3] for i in range(0, len(dvals) - 2, 5)])
    d.group()
    d.text(x0 - 10, zy + 3, 'z', size=9)
    d.text(x0 - 10, xy + 3, 'x', size=9)
    d.text(x1, base - h / 2 - 6, 'D = ½', size=8, anchor='end')
    d.text(mu_d, base - h - 10, 'DATA', size=8)
    d.text(mu_g - 62, base - h * sd_d / sd_g - 4, 'G', size=9)
    return d


def resnet():
    """A residual block, x carried round the layers and added back, beside a deep stack of such blocks."""
    d = D()
    cx, y_in, y_out = 120, 272, 28
    # construction: the axis of the block
    d.group('thin')
    d.line((cx, y_out - 6), (cx, y_in + 6))
    d.line((cx - 90, 150), (cx + 90, 150))
    # the object: two weight layers and the addition
    d.group()
    layers = [(cx, 200), (cx, 120)]
    for x, y in layers:
        d.line((x - 50, y - 14), (x + 50, y - 14), (x + 50, y + 14), (x - 50, y + 14), closed=True)
    d.circle(cx, 62, 10)
    d.lines([[(cx - 6, 62), (cx + 6, 62)], [(cx, 56), (cx, 68)]])
    d.lines([[(cx, y_in), (cx, 214)], [(cx, 186), (cx, 134)], [(cx, 106), (cx, 72)], [(cx, 52), (cx, y_out)]])
    # the skip: x goes round the layers
    d.group('mid')
    d.curve(f'M{cx} 250 C{cx + 110} 250 {cx + 110} 62 {cx + 10} 62')
    d.lines([[(cx + 16, 58), (cx + 10, 62), (cx + 16, 66)]])
    # the stack: many blocks, each with its skip, drawn as a ladder
    x = 300
    d.group('thin')
    d.line((x, 24), (x, 276))
    d.group()
    n = 17
    ys = [276 - i * (252 / n) for i in range(n + 1)]
    d.lines([[(x - 22, y), (x + 22, y)] for y in ys])
    d.group('mid')
    skips = []
    for a, b in zip(ys[::2], ys[2::2]):
        pts = [(x + 22 + 18 * math.sin(math.pi * t / 12), a + (b - a) * t / 12) for t in range(13)]
        skips.append(pts)
    d.lines(skips)
    d.group()
    d.text(cx, 204, 'WEIGHT', size=8)
    d.text(cx, 124, 'WEIGHT', size=8)
    d.text(cx - 14, 286, 'x', size=9)
    d.text(cx + 76, 160, 'x', size=9, anchor='start')
    d.text(cx + 30, 22, 'F(x) + x', size=8)
    d.text(x, 292, '152 LAYERS', size=8)
    return d


def alphago():
    """The board after move 37 of game 2 against Lee Sedol, and the shoulder hit on the fifth line."""
    d = D()
    n, s, x0, y0 = 19, 14, 24, 24  # 19 lines, 14 apart
    size = s * (n - 1)

    def at(p):
        col, row = GO_COLS.index(p[0]), int(p[1:])
        return x0 + col * s, y0 + (n - row) * s

    # construction: the grid
    d.group('thin')
    d.lines([[(x0, y0 + i * s), (x0 + size, y0 + i * s)] for i in range(n)]
            + [[(x0 + i * s, y0), (x0 + i * s, y0 + size)] for i in range(n)])
    # the board edge and the star points
    d.group()
    d.line((x0, y0), (x0 + size, y0), (x0 + size, y0 + size), (x0, y0 + size), closed=True)
    for c in 'DKQ':
        for r in (4, 10, 16):
            x, y = at(f'{c}{r}')
            d.circle(x, y, 1.2)
    # the stones of moves 1-37 (Lee Sedol white, AlphaGo black)
    black = 'Q16 C16 P4 O3 C6 N4 J17 Q5 C4 B3 B4 D5 D3 D2 K4 E16 R15 O16'.split()
    white = 'D4 R4 P3 Q3 F3 R6 D10 R5 C3 C5 B5 B6 E4 C7 C13 R14 Q14 Q11'.split()
    d.group('mid')
    for p in white:
        x, y = at(p)
        d.circle(x, y, 6)
    d.group()
    for p in black:
        x, y = at(p)
        d.circle(x, y, 6)
        d.circle(x, y, 3)
    # move 37, on the fifth line, and the line it reads from the edge
    mx, my = at('P10')
    d.group()
    d.circle(mx, my, 6)
    d.circle(mx, my, 3)
    d.circle(mx, my, 11)
    # a dimension line from the edge to the stone: the fifth line
    d.group('thin')
    dy = my + 22
    d.lines([[(mx, my + 8), (mx, dy + 4)], [(x0 + size, y0 + size), (x0 + size, dy + 4)], [(mx, dy), (x0 + size, dy)]])
    d.lines([[(x0 + size - i * s, dy - 2), (x0 + size - i * s, dy + 2)] for i in range(1, 4)])
    # the policy's estimate of a human playing it
    d.group()
    d.text(x0 + size + 18, my - 26, 'MOVE 37', size=8, anchor='start')
    d.text(x0 + size + 18, my - 14, 'GAME 2', size=8, anchor='start')
    d.text(x0 + size + 18, dy + 3, '5TH LINE', size=8, anchor='start')
    d.text(x0 + size + 18, y0 + size, 'B · ALPHAGO', size=8, anchor='start')
    d.text(x0 + size + 18, y0 + size - 12, 'W · LEE SEDOL', size=8, anchor='start')
    return d


PLATES = {
    'deep-blue': deep_blue,
    'imagenet': imagenet,
    'alexnet': alexnet,
    'word2vec': word2vec,
    'gans': gans,
    'resnet': resnet,
    'alphago': alphago,
}
