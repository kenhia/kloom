"""Plates for Sound and Score's part digital1 (sprint 058): computer-music, fm-synthesis. See plates_for.py."""
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


def _bessel(n, x):
    return sum((-1) ** k / (math.factorial(k) * math.factorial(k + n)) * (x / 2) ** (2 * k + n) for k in range(40))


def computer_music():
    d = D()
    # Above: one and a half cycles of a sine wave sampled at 16 equal steps a cycle, and the
    # converter's held output (a stair-step) before the low-pass filter smooths it back to the
    # sine. Below: Mathews's chain of 1961 (BSTJ 40, fig. 1): computer, tape, converter, filter,
    # loudspeaker. The sampling rate is schematic.
    x0, x1, y0, amp = 30, 370, 92, 52
    cycles, per = 1.5, 16
    n = int(cycles * per)
    step = (x1 - x0) / n
    def y(x):
        return y0 - amp * math.sin(2 * math.pi * cycles * (x - x0) / (x1 - x0))
    d.group('thin')
    d.line((x0, y0), (x1 + 6, y0))                                           # time axis
    d.line((x0, y0 - amp - 12), (x0, y0 + amp + 12))                          # amplitude axis
    for i in range(n + 1):
        x = x0 + i * step
        d.line((x, y0), (x, y(x)))                                            # sample stems
    d.line(*[(x0 + i * (x1 - x0) / 300, y(x0 + i * (x1 - x0) / 300)) for i in range(301)])  # the wave
    d.group()
    pts = []
    for i in range(n):
        x = x0 + i * step
        v = y(x)
        pts += [(x, v), (x + step, v)]
    d.line(*pts)                                                              # held output
    d.group('mid')
    for i in range(n + 1):
        x = x0 + i * step
        d.circle(x, y(x), 1.8)                                                # the samples
    # the interval between two samples
    xa, xb = x0 + 2 * step, x0 + 3 * step
    d.line((xa, y0 + amp + 4), (xa, y0 + amp + 14)); d.line((xb, y0 + amp + 4), (xb, y0 + amp + 14))
    d.line((xa, y0 + amp + 9), (xb, y0 + amp + 9))

    # the chain
    labels = ['COMPUTER', 'TAPE', 'CONVERTER', 'FILTER', 'SPEAKER']
    bw, bh, by = 56, 26, 214
    gap = (400 - 2 * 18 - 5 * bw) / 4
    xs = [18 + i * (bw + gap) for i in range(5)]
    d.group()
    for i, x in enumerate(xs[:4]):
        _box(d, x, by, bw, bh)
    sx = xs[4]                                                                # a loudspeaker in section
    d.line((sx + 6, by + 8), (sx + 18, by + 8), (sx + 18, by + 18), (sx + 6, by + 18), closed=True)
    d.line((sx + 18, by + 8), (sx + 34, by - 2), (sx + 34, by + 28), (sx + 18, by + 18))
    d.group('mid')
    for i in range(4):
        a, b = (xs[i] + bw, by + bh / 2), (xs[i + 1] - 2, by + bh / 2)
        d.line(a, b); _arrow(d, a, b, 4)
    for r in (8, 14):
        d.arc(sx + 36, by + 13, r, -40, 40)
    # inside the boxes: numbers, a tape reel, pulses, a smooth wave
    d.circle(xs[1] + bw / 2, by + bh / 2, 8); d.circle(xs[1] + bw / 2, by + bh / 2, 2)
    cx = xs[2] + 8
    for k, h in enumerate((6, 10, 4, -5, -9, -3)):
        d.line((cx + k * 7, by + bh / 2), (cx + k * 7, by + bh / 2 - h))
    d.line(*[(xs[3] + 6 + t * 44 / 40, by + bh / 2 - 8 * math.sin(2 * math.pi * t / 40)) for t in range(41)])
    d.group('mid')
    d.text(x0 + 4, y0 - amp - 16, 'SAMPLES · HELD BY THE CONVERTER · SMOOTHED BY THE FILTER', size=7, anchor='start')
    d.text(xa - 4, y0 + amp + 24, 'ONE SAMPLE APART', size=7, anchor='start')
    d.text(x1 + 4, y0 + 12, 'TIME', size=7, anchor='end')
    for x, s in zip(xs, labels):
        d.text(x + bw / 2, by + bh + 14, s, size=7)
    d.text(xs[0] + bw / 2, by + bh / 2 + 3, '3172', size=7)
    d.text(200, 286, 'MUSIC III · 20,000 SAMPLES A SECOND · BELL LABS 1961', size=7)
    return d


def fm_synthesis():
    d = D()
    # Chowning's bassoon-like tone (JAES 1973): carrier c = 500 Hz, modulator m = 100 Hz, index 1.5.
    # Above, two periods of the modulator: the modulator, the plain carrier, and the modulated wave
    # e = sin(2pi c t + I sin 2pi m t), each computed. Below, its spectrum: components at c +- n m
    # with heights |J_n(1.5)|, drawn to scale.
    c, m, I = 500.0, 100.0, 1.5
    x0, x1 = 34, 380
    T = 2 / m
    rows = [(46, 'MODULATOR · 100 HZ'), (100, 'CARRIER · 500 HZ'), (154, 'MODULATED · INDEX 1.5')]
    amp = 16
    N = 700
    def wave(k, t):
        if k == 0:
            return math.sin(2 * math.pi * m * t)
        if k == 1:
            return math.sin(2 * math.pi * c * t)
        return math.sin(2 * math.pi * c * t + I * math.sin(2 * math.pi * m * t))
    d.group('thin')
    for yy, _ in rows:
        d.line((x0, yy), (x1, yy))
    for q in range(5):                                                        # quarter periods of m
        x = x0 + q * (x1 - x0) / 4
        d.line((x, rows[0][0] - amp - 4), (x, rows[2][0] + amp + 4))
    # spectrum axes
    sy, sh = 262, 70
    fx = lambda f: 46 + (f / 1000.0) * 320
    d.line((fx(0) - 6, sy), (fx(1000) + 10, sy))
    for f in range(0, 1001, 100):
        d.line((fx(f), sy), (fx(f), sy + 4))
    d.group()
    for k, (yy, _) in enumerate(rows):
        d.line(*[(x0 + i * (x1 - x0) / N, yy - amp * wave(k, i * T / N)) for i in range(N + 1)])
    d.group()
    for n in range(0, 5):
        h = abs(_bessel(n, I)) * sh / 0.6
        for f in ({c - n * m, c + n * m}):
            d.line((fx(f), sy), (fx(f), sy - h))
            d.line((fx(f) - 3, sy - h), (fx(f) + 3, sy - h))
    d.group('mid')
    for yy, s in rows:
        d.text(x0, yy - amp - 6, s, size=7, anchor='start')
    d.text(fx(c), sy - 0.512 * sh / 0.6 - 14, 'C', size=7)
    d.text(fx(c - m), sy - 0.558 * sh / 0.6 - 8, 'C-M', size=7)
    d.text(fx(c + m), sy - 0.558 * sh / 0.6 - 8, 'C+M', size=7)
    d.text(fx(0), sy + 14, '0', size=7)
    d.text(fx(500), sy + 14, '500', size=7)
    d.text(fx(1000), sy + 14, '1000 HZ', size=7)
    d.text(fx(860), sy - 46, 'HEIGHT |Jn(1.5)|', size=7)
    return d


PLATES = {
    'computer-music': computer_music,
    'fm-synthesis': fm_synthesis,
}
