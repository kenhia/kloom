"""ai plates, trail "Inside a transformer" (sprint 006). See ai.py.

The numbers drawn here are the trail's worked examples: the BPE merges from
Sennrich et al.'s toy dictionary, the sinusoidal and rotary encodings, the
toy attention example of the self-attention frame, and the softmax at three
temperatures of the next-token frame.
"""
import math

from plates import D


def _softmax(xs, t=1.0):
    m = max(xs)
    e = [math.exp((x - m) / t) for x in xs]
    z = sum(e)
    return [v / z for v in e]


def tokens():
    """BPE as a merge tree: the characters of 'newest·' joined, pair by pair, into one token."""
    d = D()
    chars = ['n', 'e', 'w', 'e', 's', 't', '·']
    w, x0, base, step = 40, 60, 236, 22
    cx = [x0 + w * (i + 0.5) for i in range(7)]
    lvl = lambda n: base - 34 - step * (n - 1)
    # the merges of Sennrich et al.'s code, numbered as learned: (left, right, merge number)
    merges = [((3,), (4,), 1), ((3, 4), (5,), 2), ((3, 4, 5), (6,), 3),
              ((0,), (1,), 6), ((0, 1), (2,), 7), ((0, 1, 2), (3, 4, 5, 6), 8)]
    # construction: the merge levels, and a guide up from each character
    d.group('thin')
    d.lines([[(x0 - 14, lvl(n)), (x0 + 7 * w + 14, lvl(n))] for n in range(1, 9)])
    d.lines([[(x, base - 6), (x, lvl(8) - 8)] for x in cx])
    # the object: one cell per character, and the end-of-word mark
    d.group()
    for i in range(7):
        d.line((x0 + i * w, base), (x0 + (i + 1) * w, base), (x0 + (i + 1) * w, base + 30),
               (x0 + i * w, base + 30), closed=True)
    # the tree: each merge joins its two parts at its own level
    d.group('mid')
    top = {}
    for i in range(7):
        top[(i,)] = (cx[i], base)
    for a, b, n in merges:
        (xa, ya), (xb, yb) = top[a], top[b]
        y = lvl(n)
        d.line((xa, ya), (xa, y), (xb, y), (xb, yb))
        top[a + b] = ((xa + xb) / 2, y)
    # the finished token, and the integer it becomes
    d.group()
    xt, yt = top[(0, 1, 2, 3, 4, 5, 6)]
    d.line((xt, yt), (xt, yt - 14))
    d.line((xt - 46, yt - 14), (xt + 46, yt - 14), (xt + 46, yt - 36), (xt - 46, yt - 36), closed=True)
    d.group()
    for x, ch in zip(cx, chars):
        d.text(x, base + 19, ch, size=10)
    for n in (1, 2, 3, 6, 7, 8):
        d.text(x0 - 22, lvl(n) + 3, str(n), size=7, anchor='end')
    d.text(xt, yt - 22, 'newest·', size=9)
    return d


def token_embeddings():
    """Sinusoidal position codes as clocks of growing wavelength, and RoPE's rotation of one vector."""
    d = D()
    # left: four sinusoids, wavelengths in a geometric series, sampled at positions 0..8
    x0, x1, px = 24, 214, 8
    xs = [x0 + (x1 - x0) * p / px for p in range(px + 1)]
    rows = [(62, 1.0), (116, 2.2), (170, 4.8), (224, 10.6)]  # (centre y, wavelength factor)
    amp = 18
    d.group('thin')
    d.lines([[(x, 34), (x, 250)] for x in xs])
    d.lines([[(x0, y), (x1, y)] for y, _ in rows])
    d.group()
    for y, k in rows:
        pts = [(x0 + (x1 - x0) * s / 200, y - amp * math.sin(2 * math.pi * (px * s / 200) / (k * 2.2)))
               for s in range(201)]
        d.line(*pts)
    # the code of one position (pos 5) is the column of values the waves take there
    d.group('mid')
    p = 5
    d.line((xs[p], 30), (xs[p], 254))
    for y, k in rows:
        d.circle(xs[p], y - amp * math.sin(2 * math.pi * p / (k * 2.2)), 3.2)
    # right: RoPE turns a query or key by m·θ at position m
    cx, cy, r, th = 312, 146, 66, 30
    d.group('thin')
    d.circle(cx, cy, r)
    d.line((cx - r - 10, cy), (cx + r + 10, cy))
    d.line((cx, cy - r - 10), (cx, cy + r + 10))
    d.lines([[(cx, cy), (cx + r * math.cos(math.radians(m * th)), cy - r * math.sin(math.radians(m * th)))]
             for m in range(12)])
    d.group()
    for m in (1, 4):
        a = math.radians(m * th)
        tip = (cx + r * math.cos(a), cy - r * math.sin(a))
        d.line((cx, cy), tip)
        d.circle(*tip, 3)
    d.group('mid')
    d.arc(cx, cy, 30, -4 * th, -1 * th, n=24)
    d.arc(cx, cy, 18, -1 * th, 0, n=12)
    d.group()
    d.text(xs[p], 272, 'POS 5', size=8)
    a1, a4 = math.radians(th), math.radians(4 * th)
    d.text(cx + (r + 14) * math.cos(a1), cy - (r + 14) * math.sin(a1) + 3, 'k', size=10)
    d.text(cx + (r + 14) * math.cos(a4), cy - (r + 14) * math.sin(a4) + 3, 'q', size=10)
    d.text(cx, cy + r + 30, 'ROTATE BY mθ', size=8)
    return d


# The self-attention frame's toy example: five tokens, two-dimensional q, k, v.
TOY = ['The', 'cat', 'sat', '.', 'It']
TOY_Q = [(0, 1), (1, 0), (2, 0), (0, 1), (2, 0)]
TOY_K = [(0, 1), (2, 0), (1, 1), (0, 0), (1, 0)]


def toy_weights():
    rows = []
    for i, q in enumerate(TOY_Q):
        s = [(q[0] * k[0] + q[1] * k[1]) / math.sqrt(2) for k in TOY_K[:i + 1]]
        rows.append(_softmax(s))
    return rows


def self_attention():
    """The toy example's keys in the plane, projected onto the query of 'It'; and its causal weight matrix."""
    d = D()
    # left: keys as vectors, the query of "It" as a ray, each key's projection onto it
    ox, oy, u = 34, 200, 58
    d.group('thin')
    d.line((ox - 12, oy), (ox + 2.6 * u, oy))
    d.line((ox, oy + 12), (ox, oy - 1.6 * u))
    for k in TOY_K:
        if k != (0, 0) and k[1]:
            d.line((ox + k[0] * u, oy - k[1] * u), (ox + k[0] * u, oy))
    d.group()
    for k in TOY_K:
        if k == (0, 0):
            continue
        d.line((ox, oy), (ox + k[0] * u, oy - k[1] * u))
        d.circle(ox + k[0] * u, oy - k[1] * u, 3)
    d.group('mid')
    d.circle(ox, oy, 3)
    for k in TOY_K:
        d.line((ox + k[0] * u - 3, oy + 7), (ox + k[0] * u + 3, oy + 7))
    # right: the 5x5 weight matrix; above the diagonal masked out
    mx, my, c = 196, 56, 36
    w = toy_weights()
    d.group('thin')
    d.lines([[(mx, my + i * c), (mx + 5 * c, my + i * c)] for i in range(6)])
    d.lines([[(mx + i * c, my), (mx + i * c, my + 5 * c)] for i in range(6)])
    d.group('mid')
    hatch = []
    for i in range(5):
        for j in range(i + 1, 5):
            x, y = mx + j * c, my + i * c
            hatch += [[(x + 6, y + c - 6), (x + c - 6, y + 6)]]
    d.lines(hatch)
    d.group()
    for i, row in enumerate(w):
        for j, v in enumerate(row):
            d.circle(mx + (j + .5) * c, my + (i + .5) * c, max(1.2, 15 * math.sqrt(v)))
    d.group()
    for i, t in enumerate(TOY):
        d.text(mx - 8, my + (i + .5) * c + 3, t, size=8, anchor='end')
        d.text(mx + (i + .5) * c, my - 10, t, size=8)
    d.text(ox + 2 * u, oy + 24, 'q · k', size=8)
    d.text(mx + 2.5 * c, my + 5 * c + 26, 'CAUSAL MASK', size=8)
    return d


def multi_head_attention():
    """Three heads over one sequence: previous-token, broad, and an induction head copying B after A."""
    d = D()
    toks = ['A', 'B', 'C', 'D', 'A', 'B', '?']
    x0, dx = 70, 46
    xs = [x0 + i * dx for i in range(7)]
    bands = [92, 176, 260]

    def arc(xa, xb, y, lift):
        m = (xa + xb) / 2
        return f'M{xa:.1f} {y} Q{m:.1f} {y - lift:.1f} {xb:.1f} {y}'

    d.group('thin')
    for y in bands:
        d.line((x0 - 22, y), (xs[-1] + 22, y))
        d.lines([[(x, y - 4), (x, y + 4)] for x in xs])
    d.lines([[(x, bands[0] - 60), (x, bands[-1])] for x in xs])
    # head 1: every token looks one step back
    d.group()
    for i in range(1, 6):
        d.curve(arc(xs[i], xs[i - 1], bands[0], 26))
    # head 2: the last real token spreads its attention over all before it
    d.group('mid')
    for j in range(5):
        d.curve(arc(xs[5], xs[j], bands[1], 14 + 11 * (5 - j)))
    # head 3: at the second B, look for what followed the earlier B (C), and copy it forward
    d.group()
    d.curve(arc(xs[5], xs[2], bands[2], 58))
    d.curve(arc(xs[2], xs[6], bands[2], 34))
    d.circle(xs[6], bands[2], 6)
    d.group('mid')
    d.curve(arc(xs[5], xs[1], bands[2], 18))
    d.group()
    for x, t in zip(xs, toks):
        d.text(x, bands[-1] + 18, t, size=10)
    for y, lab in zip(bands, ['H1', 'H2', 'H3']):
        d.text(x0 - 30, y + 3, lab, size=8, anchor='end')
    d.text(xs[6], bands[2] - 30, 'COPY', size=7)
    return d


def residual_stream():
    """Four token streams, three layers: attention moves between streams, each MLP reads and writes one."""
    d = D()
    xs = [96, 170, 244, 318]
    y_in, y_out = 272, 30
    layers = [(226, 196), (152, 122), (78, 48)]  # (attention y, MLP y) per layer
    d.group('thin')
    for ya, ym in layers:
        d.line((40, ya), (370, ya))
        d.line((40, ym), (370, ym))
    # the streams themselves: each token's vector, carried up unchanged except by addition
    d.group()
    for x in xs:
        d.line((x, y_in), (x, y_out))
        d.line((x - 12, y_in), (x + 12, y_in))
        d.line((x - 12, y_out), (x + 12, y_out))
    # attention: reads from earlier streams, writes into later ones (causal: left to right only)
    d.group('mid')
    for li, (ya, _) in enumerate(layers):
        pairs = [(0, 1), (1, 3), (0, 3)] if li % 2 == 0 else [(0, 2), (2, 3), (1, 2)]
        for a, b in pairs:
            lift = 8 + 5 * (b - a)
            d.curve(f'M{xs[a]} {ya} Q{(xs[a] + xs[b]) / 2} {ya - lift} {xs[b] - 6} {ya}')
        for x in xs[1:]:
            d.circle(x, ya, 4.5)
    # MLP: each stream branches out, through a two-layer block, and adds back in
    d.group()
    for _, ym in layers:
        for x in xs:
            d.line((x, ym + 14), (x + 20, ym + 14), (x + 20, ym + 6))
            d.line((x + 14, ym + 6), (x + 26, ym + 6), (x + 30, ym - 6), (x + 10, ym - 6), closed=True)
            d.line((x + 20, ym - 6), (x + 20, ym - 12), (x + 4.5, ym - 12))
            d.circle(x, ym - 12, 4.5)
    d.group()
    d.text(40, y_in + 4, 'EMBED', size=7, anchor='start')
    d.text(40, y_out - 8, 'UNEMBED', size=7, anchor='start')
    for ya, ym in layers[:1]:
        d.text(40, ya - 4, 'ATTN', size=7, anchor='start')
        d.text(40, ym - 4, 'MLP', size=7, anchor='start')
    return d


# The next-token frame's toy logits for "The cat sat on the …".
LOGITS = [4.0, 3.0, 2.5, 1.5, 0.0]


def next_token():
    """The same five logits through softmax at three temperatures, and the wheel sampling rolls at T = 1."""
    d = D()
    x0, y0, bw, h = 30, 236, 34, 180
    d.group('thin')
    d.lines([[(x0 - 6, y0 - h * f), (x0 + 5 * bw + 6, y0 - h * f)] for f in (0.25, 0.5, 0.75, 1.0)])
    d.lines([[(x0 + i * bw, y0), (x0 + i * bw, y0 - h)] for i in range(6)])
    d.group()
    d.line((x0 - 8, y0), (x0 + 5 * bw + 8, y0))

    def steps(ps):
        pts = [(x0, y0)]
        for i, p in enumerate(ps):
            pts += [(x0 + i * bw, y0 - h * p), (x0 + (i + 1) * bw, y0 - h * p)]
        return pts + [(x0 + 5 * bw, y0)]

    d.line(*steps(_softmax(LOGITS, 0.5)))
    d.group('mid')
    d.line(*steps(_softmax(LOGITS, 1.0)))
    d.line(*steps(_softmax(LOGITS, 2.0)))
    # the wheel: sectors in proportion to the T = 1 probabilities, and the pointer
    cx, cy, r = 302, 146, 70
    ps = _softmax(LOGITS, 1.0)
    d.group('thin')
    d.circle(cx, cy, r + 12)
    d.group()
    d.circle(cx, cy, r)
    a, spokes = -90.0, []
    for p in ps:
        spokes.append([(cx, cy), (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))])
        a += 360 * p
    d.lines(spokes)
    d.group('mid')
    pa = math.radians(-90 + 360 * 0.37)
    d.line((cx, cy), (cx + (r + 18) * math.cos(pa), cy + (r + 18) * math.sin(pa)))
    d.circle(cx, cy, 4)
    d.group()
    d.text(x0 + 0.5 * bw, y0 - h * _softmax(LOGITS, 0.5)[0] - 8, 'T 0.5', size=7)
    d.text(x0 + 4.5 * bw, y0 + 16, 'moon', size=7)
    d.text(x0 + 0.5 * bw, y0 + 16, 'mat', size=7)
    d.text(cx, cy + r + 32, 'SAMPLE', size=8)
    return d


PLATES = {
    'tokens': tokens,
    'token-embeddings': token_embeddings,
    'self-attention': self_attention,
    'multi-head-attention': multi_head_attention,
    'residual-stream': residual_stream,
    'next-token': next_token,
}
