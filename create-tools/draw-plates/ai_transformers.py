"""ai plates, segment "The transformer era" (sprint 006). See plates_for.py."""
import math, random

from plates import D


def _arrow(d, x0, y0, x1, y1, head=5):
    """A line from (x0, y0) to (x1, y1) with an open arrowhead at the end."""
    a = math.atan2(y1 - y0, x1 - x0)
    d.line((x0, y0), (x1, y1))
    d.line((x1 - head * math.cos(a - 0.45), y1 - head * math.sin(a - 0.45)), (x1, y1),
           (x1 - head * math.cos(a + 0.45), y1 - head * math.sin(a + 0.45)))


def _softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    s = sum(e)
    return [v / s for v in e]


def transformer():
    """Self-attention: one query fanned out to every key, the n-by-n score matrix, and the sine waves of position."""
    d = D()
    n = 6
    xs = [34 + i * 36 for i in range(n)]
    yq, yk = 70, 200
    # construction: every query joined to every key, the token rails, the matrix grid
    d.group('thin')
    d.lines([[(x, yq + 9), (xk, yk - 9)] for x in xs for xk in xs])
    d.line((18, yq), (232, yq))
    d.line((18, yk), (232, yk))
    mx, my, cell = 262, 62, 20
    d.lines([[(mx + i * cell, my), (mx + i * cell, my + n * cell)] for i in range(n + 1)] +
            [[(mx, my + i * cell), (mx + n * cell, my + i * cell)] for i in range(n + 1)])
    # the tokens, as queries (top) and keys (bottom), and the matrix frame
    d.group()
    for x in xs:
        d.circle(x, yq, 9)
        d.circle(x, yk, 9)
    d.line((mx, my), (mx + n * cell, my), (mx + n * cell, my + n * cell), (mx, my + n * cell), closed=True)
    # one query's attention: the fan to every key, and its row of weights as squares sized by softmax
    q = 3
    scores = [math.cos((k - q) * 0.9) * 2.2 - 0.25 * abs(k - q) for k in range(n)]
    w = _softmax(scores)
    d.group('mid')
    for k, x in enumerate(xs):
        d.line((xs[q], yq + 9), (x, yk - 9))
    for r in range(n):
        wr = _softmax([math.cos((k - r) * 0.9) * 2.2 - 0.25 * abs(k - r) for k in range(n)])
        for k in range(n):
            s = (cell - 4) * math.sqrt(wr[k] / max(wr))
            cx, cy = mx + k * cell + cell / 2, my + r * cell + cell / 2
            if s > 2:
                d.line((cx - s / 2, cy - s / 2), (cx + s / 2, cy - s / 2), (cx + s / 2, cy + s / 2),
                       (cx - s / 2, cy + s / 2), closed=True)
    # the highlighted row, and the weight bars under the keys
    d.group()
    d.line((mx - 3, my + q * cell - 3), (mx + n * cell + 3, my + q * cell - 3),
           (mx + n * cell + 3, my + (q + 1) * cell + 3), (mx - 3, my + (q + 1) * cell + 3), closed=True)
    for k, x in enumerate(xs):
        d.line((x - 6, yk + 16), (x - 6, yk + 16 + 50 * w[k]), (x + 6, yk + 16 + 50 * w[k]), (x + 6, yk + 16))
    # positional encoding: three sine waves of doubling wavelength, sampled at each token
    d.group('thin')
    for j, (amp, per) in enumerate([(6, 36), (6, 72), (6, 144)]):
        y0 = 26 + j * 12
        d.line(*[(18 + t, y0 - amp * math.sin(2 * math.pi * (t - 16) / per)) for t in range(0, 215, 3)])
    d.group()
    d.text(xs[q], yq + 3, 'q', size=9)
    for x in xs:
        d.text(x, yk + 3, 'k', size=8)
    d.text(mx + n * cell / 2, my + n * cell + 18, 'n × n SCORES', size=8)
    d.text(mx + n * cell / 2, my - 12, 'softmax(QKᵀ/√d)V', size=8)
    d.text(125, 290, 'ONE QUERY · EVERY KEY · ONE STEP', size=8)
    return d


def pretraining():
    """Two objectives on one sentence: next-token prediction (causal arcs) and a masked token read from both sides."""
    d = D()
    n = 7
    xs = [40 + i * 52 for i in range(n)]
    y1, y2 = 104, 204
    d.group('thin')
    d.line((20, y1), (380, y1))
    d.line((20, y2), (380, y2))
    for x in xs:
        d.line((x, 24), (x, 280))
    # the token boxes, twice
    d.group()
    for y in (y1, y2):
        for i, x in enumerate(xs):
            if y == y2 and i == 3:
                continue
            d.line((x - 16, y - 11), (x + 16, y - 11), (x + 16, y + 11), (x - 16, y + 11), closed=True)
    d.line((xs[3] - 20, y2 - 14), (xs[3] + 20, y2 - 14), (xs[3] + 20, y2 + 14), (xs[3] - 20, y2 + 14), closed=True)
    # causal: every token sees only those before it; arcs above the row, drawn to the last token
    d.group('mid')
    t = n - 1
    for i in range(t):
        x0, x1 = xs[i], xs[t]
        r = (x1 - x0) / 2
        d.arc((x0 + x1) / 2, y1 - 11, r, 180, 360, ry=min(r * 0.5, 58), n=36)
    # masked: the hidden token reads from both sides, arcs below the row
    for i in range(n):
        if i == 3:
            continue
        x0, x1 = sorted((xs[i], xs[3]))
        r = (x1 - x0) / 2
        d.arc((x0 + x1) / 2, y2 + 14, r, 0, 180, ry=min(r * 0.5, 50), n=36)
    d.group()
    d.line((xs[t] + 20, y1), (xs[t] + 30, y1))
    d.line((xs[t] + 26, y1 - 4), (xs[t] + 30, y1), (xs[t] + 26, y1 + 4))
    d.group()
    d.text(xs[3], y2 + 3, '[M]', size=8)
    d.text(xs[t] + 4, y1 + 3, '?', size=9)
    d.text(200, 20, 'GPT · LEFT TO RIGHT', size=8)
    d.text(200, 292, 'BERT · BOTH SIDES', size=8)
    return d


def scaling_laws():
    """Log-log axes: learning curves for five model sizes, their power-law envelope, and an inset of IsoFLOP valleys."""
    d = D()
    x0, y0, x1, y1 = 40, 30, 250, 250  # plot box: log10 compute 0..6 across, loss down
    def X(lc):
        return x0 + (x1 - x0) * lc / 6
    def Y(ll):
        return y1 - (y1 - y0) * (ll + 0.2) / 1.0
    d.group('thin')
    d.lines([[(X(i), y0), (X(i), y1)] for i in range(7)] + [[(x0, Y(v / 5 - 0.2)), (x1, Y(v / 5 - 0.2))] for v in range(6)])
    d.group()
    d.line((x0, y0 - 6), (x0, y1), (x1 + 6, y1))
    # learning curves: loss falls with compute for each size, then flattens at its own floor
    d.group('mid')
    floors = [0.66 - 0.095 * i for i in range(8)]
    starts = [0.55 * i for i in range(8)]
    grid = [i * 0.1 for i in range(61)]
    curves = []
    for s0, fl in zip(starts, floors):
        pts = {lc: fl + 0.34 * math.exp(-(lc - s0) * 1.5) for lc in grid if lc >= s0}
        curves.append(pts)
        d.line(*[(X(lc), Y(ll)) for lc, ll in pts.items() if ll <= 0.8])
    # the compute-efficient frontier: the lower envelope of every curve, near straight on log-log axes
    d.group()
    env = [(X(lc), Y(min(c[lc] for c in curves if lc in c))) for lc in grid]
    d.line(*[p for p in env if p[1] >= y0])
    # inset: IsoFLOP curves, loss against model size at fixed compute; each has one minimum
    ix, iy, iw, ih = 272, 60, 110, 150
    d.group('thin')
    d.line((ix, iy), (ix, iy + ih), (ix + iw, iy + ih))
    mins = []
    for j, (c, depth) in enumerate([(0.30, 0.25), (0.50, 0.45), (0.72, 0.65)]):
        pts = [(ix + iw * u, iy + ih * (depth + 0.2 - 2.2 * (u - c) ** 2)) for u in [k / 40 for k in range(41)]]
        pts = [(x, y) for x, y in pts if y >= iy]
        mins.append((ix + iw * c, iy + ih * (depth + 0.2)))
        d.group('mid')
        d.line(*pts)
    d.group()
    for mx, my in mins:
        d.circle(mx, my, 3)
    d.line(mins[0], mins[-1])
    d.group()
    d.text(145, 272, 'COMPUTE (LOG)', size=8)
    d.text(24, 140, 'LOSS', size=8, anchor='middle')
    d.text(ix + iw / 2, iy + ih + 16, 'PARAMETERS (LOG)', size=7)
    d.text(ix + iw / 2, iy - 10, 'ISOFLOP', size=8)
    return d


def in_context_learning():
    """A few-shot prompt as a stack of demonstrations above an open query, beside a sharp and a smooth scaling curve."""
    d = D()
    bx, bw, bh = 30, 170, 30
    rows = [48, 90, 132, 186]
    d.group('thin')
    d.line((bx + bw / 2 + 4, 30), (bx + bw / 2 + 4, 250))
    d.lines([[(bx - 8, y), (bx + bw + 8, y)] for y in (74, 116, 158)])
    # the demonstrations (input → output) and the query
    d.group()
    for i, y in enumerate(rows):
        d.line((bx, y - bh / 2), (bx + 76, y - bh / 2), (bx + 76, y + bh / 2), (bx, y + bh / 2), closed=True)
        if i < 3:
            d.line((bx + 94, y - bh / 2), (bx + bw, y - bh / 2), (bx + bw, y + bh / 2), (bx + 94, y + bh / 2), closed=True)
    d.group('mid')
    for i, y in enumerate(rows):
        _arrow(d, bx + 78, y, bx + 92, y, head=4)
    # the open answer, dashed
    y = rows[3]
    segs = []
    for x, xe, ya, yb in [(bx + 94, bx + bw, y - bh / 2, y - bh / 2), (bx + bw, bx + bw, y - bh / 2, y + bh / 2),
                          (bx + bw, bx + 94, y + bh / 2, y + bh / 2), (bx + 94, bx + 94, y + bh / 2, y - bh / 2)]:
        L = math.hypot(xe - x, yb - ya)
        k = int(L // 6)
        for j in range(0, k, 2):
            segs.append([(x + (xe - x) * j / k, ya + (yb - ya) * j / k), (x + (xe - x) * (j + 1) / k, ya + (yb - ya) * (j + 1) / k)])
    d.lines(segs)
    # the scaling plot: accuracy against log parameters, one sharp (exact match), one smooth (per token)
    px, py, pw, ph = 236, 40, 140, 180
    d.group('thin')
    d.lines([[(px + pw * i / 4, py), (px + pw * i / 4, py + ph)] for i in range(5)])
    d.line((px, py + ph * 0.9), (px + pw, py + ph * 0.9))
    d.group()
    d.line((px, py - 6), (px, py + ph), (px + pw + 6, py + ph))
    d.group('mid')
    smooth = [(px + pw * u, py + ph * (0.9 - 0.8 * (1 / (1 + math.exp(-5 * (u - 0.45)))))) for u in [k / 50 for k in range(51)]]
    d.line(*smooth)
    d.group()
    sharp = [(px + pw * u, py + ph * (0.9 - 0.8 * (1 / (1 + math.exp(-5 * (u - 0.45)))) ** 6)) for u in [k / 50 for k in range(51)]]
    d.line(*sharp)
    d.group()
    d.text(bx + 38, rows[3] + 3, 'x', size=9)
    d.text(bx + 132, rows[3] + 3, '?', size=10)
    d.text(bx + bw / 2, 272, 'K = 3 EXAMPLES · NO UPDATES', size=8)
    d.text(px + pw / 2, py + ph + 18, 'SCALE (LOG)', size=8)
    d.text(px + pw / 2, 272, 'SHARP OR SMOOTH?', size=8)
    return d


def _swiss_roll(n, rng):
    pts = []
    for _ in range(n):
        t = 1.5 * math.pi * (1 + 2 * rng.random())
        pts.append((t * math.cos(t) / 15, t * math.sin(t) / 15))
    return pts


def diffusion():
    """Sohl-Dickstein's swiss roll dissolving into a Gaussian over forward steps, with the learned reverse arrow beneath."""
    d = D()
    rng = random.Random(2015)
    data = _swiss_roll(150, rng)
    noise = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in data]
    panels = [(70, 0.0), (200, 0.55), (330, 1.0)]
    cy, half = 130, 52
    d.group('thin')
    for cx, _ in panels:
        d.line((cx - half, cy - half), (cx + half, cy - half), (cx + half, cy + half), (cx - half, cy + half), closed=True)
        d.line((cx - half, cy), (cx + half, cy))
        d.line((cx, cy - half), (cx, cy + half))
    d.circle(330, cy, 22)
    d.circle(330, cy, 44)
    # the points at each noise level: x_t = sqrt(1 - b) x_0 + sqrt(b) e
    for (cx, b) in panels:
        d.group('main' if b == 0 else 'mid')
        for (x, y), (ex, ey) in zip(data, noise):
            px = math.sqrt(1 - b) * x + math.sqrt(b) * ex * 0.45
            py = math.sqrt(1 - b) * y + math.sqrt(b) * ey * 0.45
            X, Y = cx + px * 46, cy - py * 46
            if abs(X - cx) < half - 2 and abs(Y - cy) < half - 2:
                d.circle(X, Y, 1.1)
    # forward (noising) above, reverse (learned denoising) below
    d.group()
    _arrow(d, 126, 62, 144, 62)
    _arrow(d, 256, 62, 274, 62)
    _arrow(d, 274, 200, 256, 200)
    _arrow(d, 144, 200, 126, 200)
    d.group('mid')
    d.line((40, 232), (360, 232))
    for i in range(33):
        x = 40 + i * 10
        d.line((x, 229), (x, 235) if i % 4 else (x, 238))
    d.group()
    d.text(200, 50, 'q · ADD NOISE', size=8)
    d.text(200, 216, 'pθ · REMOVE NOISE (LEARNED)', size=8)
    d.text(70, 262, 't = 0', size=8)
    d.text(330, 262, 't = T', size=8)
    d.text(200, 286, 'MANY SMALL STEPS', size=8)
    return d


def rlhf():
    """Two answers, one human preference, a reward model's logistic, and the policy held to its reference by a KL tether."""
    d = D()
    d.group('thin')
    d.line((20, 150), (380, 150))
    d.line((200, 20), (200, 280))
    # the prompt and two answers
    d.group()
    d.line((30, 40), (170, 40), (170, 64), (30, 64), closed=True)
    d.line((30, 90), (92, 90), (92, 130), (30, 130), closed=True)
    d.line((108, 90), (170, 90), (170, 130), (108, 130), closed=True)
    d.group('mid')
    _arrow(d, 80, 64, 61, 88, head=4)
    _arrow(d, 120, 64, 139, 88, head=4)
    d.circle(100, 110, 8)
    # the reward model: P(A preferred) = sigmoid(r_A - r_B)
    px, py, pw, ph = 230, 30, 140, 100
    d.group('thin')
    d.line((px, py + ph / 2), (px + pw, py + ph / 2))
    d.line((px + pw / 2, py), (px + pw / 2, py + ph))
    d.line((px, py), (px + pw, py))
    d.group()
    d.line((px, py - 4), (px, py + ph), (px + pw + 4, py + ph))
    d.line(*[(px + pw * u, py + ph - ph / (1 + math.exp(-10 * (u - 0.5)))) for u in [k / 60 for k in range(61)]])
    # the policy loop: sample, score, update; tethered to the reference model
    d.group('mid')
    cx, cy, r = 110, 215, 46
    d.arc(cx, cy, r, 200, 500, n=60)
    a0, a1 = math.radians(494), math.radians(500)
    _arrow(d, cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1), head=6)
    d.group()
    d.circle(cx, cy, 14)
    d.circle(300, 215, 14)
    d.group('thin')
    springs = [(cx + 14, cy)]
    for i in range(1, 16):
        springs.append((cx + 14 + i * (300 - 14 - cx - 14) / 16, cy + (7 if i % 2 else -7)))
    springs.append((300 - 14, 215))
    d.line(*springs)
    d.group()
    d.text(100, 56, 'PROMPT', size=8)
    d.text(61, 114, 'A', size=9)
    d.text(139, 114, 'B', size=9)
    d.text(100, 113, '>', size=9)
    d.text(px + pw / 2, py + ph + 16, 'r(A) − r(B)', size=8)
    d.text(cx, cy + 3, 'π', size=10)
    d.text(300, 218, 'π₀', size=10)
    d.text(205, 205, 'KL', size=8)
    d.text(200, 290, 'PREFER · SCORE · UPDATE', size=8)
    return d


def chat_assistants():
    """A conversation as alternating turns inside one context window, each answer conditioned on everything above it."""
    d = D()
    turns = [('u', 34, 22), ('a', 70, 34), ('u', 118, 22), ('a', 154, 42), ('u', 210, 22)]
    xl, xr, w = 40, 360, 200
    d.group('thin')
    d.line((xl, 20), (xl, 280))
    d.line((xr, 20), (xr, 280))
    d.line((xl + 20, 20), (xl + 20, 280))
    d.line((xr - 20, 20), (xr - 20, 280))
    # the context window bracket
    d.line((20, 24), (14, 24), (14, 262), (20, 262))
    d.group()
    for who, y, h in turns:
        if who == 'u':
            x0 = xr - 20 - 150
            d.line((x0, y), (xr - 20, y), (xr - 20, y + h), (xr - 30, y + h), (xr - 20, y + h + 8), (xr - 42, y + h), (x0, y + h), closed=True)
        else:
            x0 = xl + 20
            d.line((x0, y), (x0 + w, y), (x0 + w, y + h), (x0 + 22, y + h), (x0 + 10, y + h + 8), (x0 + 12, y + h), (x0, y + h), closed=True)
    # lines of text inside each turn
    d.group('mid')
    for who, y, h in turns:
        x0 = xr - 20 - 150 + 10 if who == 'u' else xl + 30
        width = 130 if who == 'u' else w - 20
        k = int((h - 6) // 9)
        d.lines([[(x0, y + 9 + j * 9), (x0 + width * (0.6 if j == k - 1 else 1.0), y + 9 + j * 9)] for j in range(k)])
    # the next answer, not yet written: a cursor after one line
    d.group()
    y = 246
    d.line((xl + 20, y), (xl + 20 + w, y))
    d.line((xl + 30, y + 10), (xl + 100, y + 10))
    d.line((xl + 106, y + 4), (xl + 106, y + 14))
    # attention from the new token up to every earlier turn
    d.group('thin')
    for who, yy, h in turns:
        cx = xr - 95 if who == 'u' else xl + 20 + w / 2
        d.line((xl + 106, y + 2), (cx, yy + h))
    d.group()
    d.text(xr - 95, 16, 'USER', size=8)
    d.text(xl + 120, 16, 'ASSISTANT', size=8)
    d.text(200, 292, 'EVERY TURN READS ALL THE TURNS BEFORE IT', size=8)
    return d


PLATES = {
    'transformer': transformer,
    'pretraining': pretraining,
    'scaling-laws': scaling_laws,
    'in-context-learning': in_context_learning,
    'diffusion': diffusion,
    'rlhf': rlhf,
    'chat-assistants': chat_assistants,
}
