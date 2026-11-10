"""Plates for Sound and Score's part digital3 (sprint 058): mp3, streaming, ai-music. See plates_for.py."""
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


# --- mp3: a masking threshold around a loud tone ---------------------------------------------
# The threshold in quiet is Terhardt's approximation (1979), as perceptual coders use it; the
# masker's spread is a simple two-slope function on the Bark scale (Zwicker's critical bands):
# 25 dB a Bark below the masker, 10 dB a Bark above it (the upward spread of masking), its peak
# 10 dB under the masker. The curve is computed; the quieter tones are an invented example.

def _bark(f):
    return 13 * math.atan(0.00076 * f) + 3.5 * math.atan((f / 7500) ** 2)


def _quiet(f):
    k = f / 1000
    return 3.64 * k ** -0.8 - 6.5 * math.exp(-0.6 * (k - 3.3) ** 2) + 1e-3 * k ** 4


def mp3():
    d = D()
    x0, x1, y0, y1 = 46, 384, 250, 40          # plot box: 50 Hz .. 16 kHz, -10 .. 90 dB
    lf0, lf1 = math.log10(50), math.log10(16000)
    X = lambda f: x0 + (math.log10(f) - lf0) / (lf1 - lf0) * (x1 - x0)
    Y = lambda db: y0 - (db + 10) / 100 * (y0 - y1)
    fm, lm = 1000, 72                          # the masker
    zm = _bark(fm)

    def spread(f):
        dz = _bark(f) - zm
        return lm - 10 - (25 * -dz if dz < 0 else 10 * dz)

    def masked(f):
        return max(_quiet(f), spread(f))

    fs = [10 ** (lf0 + i / 240 * (lf1 - lf0)) for i in range(241)]

    d.group('thin')
    d.line((x0, y1), (x0, y0), (x1, y0))
    for f in (100, 1000, 10000):
        d.line((X(f), y0), (X(f), y1))
    for db in (0, 20, 40, 60, 80):
        d.line((x0, Y(db)), (x1, Y(db)))
    for f in (50, 200, 500, 2000, 5000):
        d.line((X(f), y0), (X(f), y0 + 3))

    d.group('mid')
    d.dashed(*[(X(f), Y(min(_quiet(f), 90))) for f in fs if _quiet(f) < 92], dash=3, gap=3)

    d.group()
    d.line(*[(X(f), Y(min(masked(f), 90))) for f in fs if masked(f) < 92])
    d.line((X(fm), y0), (X(fm), Y(lm)))
    d.circle(X(fm), Y(lm), 2.2)

    # quieter tones: heard where they stand above the curve, hidden (dashed) under it
    tones = [(400, 30), (900, 38), (1200, 44), (1500, 42), (2000, 12), (5000, 20)]
    d.group('mid')
    for f, l in tones:
        top = (X(f), Y(l))
        if l > masked(f):
            d.line((X(f), y0), top)
            d.circle(top[0], top[1], 1.6)
        else:
            d.dashed((X(f), y0), top, dash=2.5, gap=2.5)

    d.group('mid')
    d.text(X(fm), Y(lm) - 7, 'MASKER 1 kHz', size=7)
    d.text(X(2050), Y(28), 'THRESHOLD IN QUIET', size=7, anchor='start')
    d.text(X(1600), Y(64), 'MASKED THRESHOLD', size=7, anchor='start')
    d.text(X(56), Y(2), 'DASHED TONES ARE HIDDEN', size=7, anchor='start')
    for f, s in ((100, '100 Hz'), (1000, '1 kHz'), (10000, '10 kHz')):
        d.text(X(f), y0 + 12, s, size=7)
    for db in (0, 20, 40, 60, 80):
        d.text(x0 - 4, Y(db) + 2.5, f'{db}', size=7, anchor='end')
    d.text(x0 - 4, y1 + 2.5, 'dB', size=7, anchor='end')
    return d


# --- streaming: where a £9.99 subscription goes, and the pool split by streamshare -------------
# The shares are the House of Commons DCMS Committee's (2021): VAT £1.67; of the rest, about 30%
# to the service, 55% to the recording's rights holders, 15% to the song's. The royalty pool is
# divided by each act's share of all streams (the slices are illustrative), and an artist on a
# standard major-label deal is paid 20 to 24% of the recording's share (22% drawn).

def streaming():
    d = D()
    x0, w, y, h = 30, 340, 56, 24
    total, vat = 9.99, 1.67
    rest = total - vat
    parts = [('VAT', vat), ('SERVICE', rest * 0.30), ('RECORDING', rest * 0.55), ('SONG', rest * 0.15)]
    xs = [x0]
    for _, v in parts:
        xs.append(xs[-1] + v / total * w)
    py, ph = 142, 22                       # the pool
    zy, zh = 222, 22                       # one act's slice, opened out

    shares = [1 / (k + 1) ** 1.1 for k in range(14)]
    s = sum(shares)
    segs, x = [], x0
    for v in shares:
        segs.append((x, v / s * w))
        x += v / s * w
    sx, sw = segs[0]

    d.group('thin')
    d.line((x0, y - 14), (x0 + w, y - 14))
    for xx in (x0, x0 + w):
        d.line((xx, y - 18), (xx, y - 10))
    d.line((xs[2], y + h + 4), (xs[2], y + h + 12), (xs[4], y + h + 12), (xs[4], y + h + 4))
    d.line((sx, py + ph), (x0, zy))
    d.line((sx + sw, py + ph), (x0 + w, zy))

    d.group()
    _box(d, x0, y, w, h)
    for xx in xs[1:-1]:
        d.line((xx, y), (xx, y + h))
    mid = (xs[2] + xs[4]) / 2
    d.line((mid, y + h + 12), (mid, py - 3))
    _arrow(d, (mid, y + h + 12), (mid, py - 2))
    _box(d, x0, py, w, ph)
    _box(d, x0, zy, w, zh)

    d.group('mid')
    for xx, ww in segs[1:]:
        d.line((xx, py), (xx, py + ph))
    tail = segs[-1][0] + segs[-1][1]
    for k in range(10):
        d.line((tail - 4 - k * 2.2, py + 4), (tail - 4 - k * 2.2, py + ph - 4))
    rec = 0.55 / 0.70
    lab = w * rec * 0.78
    art = w * rec * 0.22
    d.line((x0 + lab, zy), (x0 + lab, zy + zh))
    d.line((x0 + lab + art, zy), (x0 + lab + art, zy + zh))

    d.group('mid')
    d.text(x0 + w / 2, y - 20, '£9.99 A MONTH', size=7)
    for (name, v), a, b in zip(parts, xs, xs[1:]):
        d.text((a + b) / 2, y + h / 2 + 2.5, name, size=7)
        d.text((a + b) / 2, y - 4, f'£{v:.2f}', size=7)
    d.text(x0, py - 6, 'THE ROYALTY POOL', size=7, anchor='start')
    d.text(x0, py + ph + 12, 'SPLIT BY SHARE OF ALL STREAMS', size=7, anchor='start')
    d.text(x0 + lab / 2, zy + zh / 2 + 2.5, 'LABEL', size=7)
    d.text(x0 + lab + art / 2, zy + zh / 2 + 2.5, 'ARTIST', size=7)
    d.text(x0 + lab + art + (w - lab - art) / 2, zy + zh / 2 + 2.5, 'SONG', size=7)
    d.text(x0, zy + zh + 12, "ONE ACT'S SLICE", size=7, anchor='start')
    return d


# --- ai-music: a text-to-music model's pipeline, after MusicLM (Agostinelli et al. 2023) -------
# Text to a joint music-text embedding (MuLan), quantized to 12 tokens; a semantic stage writes
# 25 tokens a second; an acoustic stage writes SoundStream's tokens, 600 a second in 12 levels
# of residual quantization (4 coarse and 8 fine rows); a decoder turns them into a
# 24 kHz waveform. Token positions and the waveform's partials are drawn, not taken from a run.

def ai_music():
    d = D()
    rows = [40, 98, 156, 214]
    bx, bw, bh = 16, 112, 34
    tx0, tx1 = 146, 384

    d.group('thin')
    for y in rows:
        d.line((tx0, y + bh / 2), (tx1, y + bh / 2))
    for t in range(0, 4):
        x = tx0 + t / 3 * (tx1 - tx0)
        d.line((x, rows[1] - 6), (x, rows[2] + bh + 6))

    d.group()
    for y in rows:
        _box(d, bx, y, bw, bh)
    for a, b in zip(rows, rows[1:]):
        d.line((bx + bw / 2, a + bh), (bx + bw / 2, b - 2))
        _arrow(d, (bx + bw / 2, a + bh), (bx + bw / 2, b - 1), 4)

    # row 0: the prompt's 12 conditioning tokens
    d.group('mid')
    y = rows[0] + bh / 2
    for k in range(12):
        x = tx0 + k * 9
        _box(d, x, y - 4, 6, 8)
    # row 1: semantic tokens, 25 a second over three seconds
    y = rows[1] + bh / 2
    segs = []
    for k in range(75):
        x = tx0 + (k + 0.5) / 75 * (tx1 - tx0)
        hgt = 3 + 6 * abs(math.sin(k * 1.7) * math.cos(k * 0.31))
        segs.append([(x, y - hgt), (x, y + hgt)])
    d.lines(segs)
    # row 2: acoustic tokens, coarse rows dense, fine rows denser (schematic)
    segs = []
    for lev in range(12):
        yy = rows[2] + 4.5 + lev * 2.3
        n = 80 if lev < 4 else 120
        for k in range(n):
            x = tx0 + (k + 0.5) / n * (tx1 - tx0)
            segs.append([(x, yy - 0.8), (x, yy + 0.8)])
    d.lines(segs)

    # row 3: the decoded waveform
    d.group()
    y = rows[3] + bh / 2
    pts = []
    for i in range(481):
        t = i / 480
        x = tx0 + t * (tx1 - tx0)
        env = 0.15 + 0.85 * math.exp(-3.5 * ((t * 6) % 1))
        s = (math.sin(2 * math.pi * 44 * t) + 0.4 * math.sin(2 * math.pi * 88 * t + 1) + 0.2 * math.sin(2 * math.pi * 132 * t + 2)) / 1.4
        pts.append((x, y - 14 * env * s))
    d.line(*pts)

    d.group('mid')
    labels = [('TEXT PROMPT', 'MuLan · 12 TOKENS'), ('SEMANTIC STAGE', '25 TOKENS A SECOND'),
              ('ACOUSTIC STAGE', '600 TOKENS A SECOND'), ('DECODER', '24 kHz AUDIO')]
    for (a, b), y in zip(labels, rows):
        d.text(bx + bw / 2, y + 14, a, size=7)
        d.text(bx + bw / 2, y + 25, b, size=7)
    for t in range(0, 4):
        x = tx0 + t / 3 * (tx1 - tx0)
        d.text(x, rows[2] + bh + 16, f'{t} s', size=7)
    return d


PLATES = {'mp3': mp3, 'streaming': streaming, 'ai-music': ai_music}
