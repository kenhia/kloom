"""Plates for Sound and Score's part modern2 (sprint 058): cage-silence, rock-and-roll, moog.
See plates_for.py."""
import cmath
import math
import random
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def cage_silence():
    d = D()
    # 4'33" as a time line to scale, 273 seconds across 330 units. Top: the movements as the Woodstock
    # program and the Kremen manuscript give them (30", 2'23", 1'40"); bottom, as Cage's 1960 Tacet
    # edition says the premiere ran (33", 2'40", 1'20"). Both sum to 273 s. The middle band is the
    # Kremen manuscript's proportional notation, a page every 56 seconds ("1 PAGE = 7 INCHES = 56"").
    # The trace in each movement is schematic: wind, then rain, then the audience, as Cage told it.
    x0, W, T = 40, 330, 273.0
    X = lambda s: x0 + s * W / T
    a = [0, 30, 173, 273]
    b = [0, 33, 193, 273]
    ya, yt, yk, yb = 52, 92, 160, 222

    d.group('thin')
    for s in range(0, 271, 30):                               # a tick every 30 s
        d.line((X(s), 40), (X(s), 250))
    d.line((X(273), 40), (X(273), 250))
    d.line((x0, ya), (X(T), ya)); d.line((x0, yb), (X(T), yb)); d.line((x0, yt), (X(T), yt))
    for p in range(0, 5):                                     # Kremen pages, 56 s each
        d.line((X(p * 56), yk + 12), (X(p * 56), yk + 18))

    d.group()
    for ts, y in ((a, ya), (b, yb)):                          # the three movements as spans
        for t0, t1 in zip(ts, ts[1:]):
            d.line((X(t0) + 1.5, y - 7), (X(t0) + 1.5, y + 7))
            d.line((X(t1) - 1.5, y - 7), (X(t1) - 1.5, y + 7))
            d.line((X(t0) + 5, y - 12), (X(t1) - 5, y - 12))  # the lid, lowered over the span
    for s in a:                                               # Kremen's vertical strokes
        d.line((X(s), yk - 12), (X(s), yk + 12))
    d.line((x0, yk + 12), (X(T), yk + 12))

    d.group('mid')
    rnd = random.Random(1952)
    for i, (t0, t1) in enumerate(zip(a, a[1:])):              # schematic room sound, per movement
        pts = []
        n = int((t1 - t0) * 1.4)
        for k in range(n + 1):
            s = t0 + 1 + (t1 - t0 - 2) * k / n
            if i == 0:                                        # wind: slow swell
                v = 5 * math.sin(s / 4.0) * math.sin(s / 13.0)
            elif i == 1:                                      # rain: sparse drops
                v = (rnd.random() - 0.5) * 2 + (8 if rnd.random() < 0.12 else 0) * rnd.choice((-1, 1))
            else:                                             # the audience: bursts of talk
                v = (rnd.random() - 0.5) * (14 if math.sin(s / 3.0) > 0.3 else 3)
            pts.append((X(s), yt + v))
        d.line(*pts)
    d.dashed((X(30), ya + 7), (X(33), yb - 14), dash=3, gap=3)
    d.dashed((X(173), ya + 7), (X(193), yb - 14), dash=3, gap=3)

    d.group('mid')
    d.text(x0, 30, 'WOODSTOCK PROGRAM · KREMEN MS', size=7, anchor='start')
    for t0, t1, lab in ((0, 30, 'I 30″'), (30, 173, 'II 2′23″'), (173, 273, 'III 1′40″')):
        d.text((X(t0) + X(t1)) / 2, ya + 16, lab, size=7)
    for t0, t1, lab in ((0, 30, 'WIND'), (30, 173, 'RAIN'), (173, 273, 'TALK, WALKING OUT')):
        d.text((X(t0) + X(t1)) / 2, yt + 22, lab, size=7)
    d.text(x0, yk - 18, 'PROPORTIONAL NOTATION · 1 PAGE = 56″', size=7, anchor='start')
    d.text(x0, yb - 20, 'TACET EDITION 1960 · THE PREMIERE', size=7, anchor='start')
    for t0, t1, lab in ((0, 33, 'I 33″'), (33, 193, 'II 2′40″'), (193, 273, 'III 1′20″')):
        d.text((X(t0) + X(t1)) / 2, yb + 16, lab, size=7)
    for s, lab in ((0, '0'), (60, '1′'), (120, '2′'), (180, '3′'), (240, '4′')):
        d.text(X(s), 262, lab, size=7)
    d.text(X(273), 262, '4′33″', size=7)
    d.text(200, 288, 'LID LOWERED FOR EACH MOVEMENT · ROOM SOUND SCHEMATIC', size=7)
    return d


def rock_and_roll():
    d = D()
    # Top: two bars of a rock and roll beat on a grid of eighth notes: the kick on 1 and 3, the
    # snare's backbeat on 2 and 4 (drawn larger), eighths on the ride or the guitar's chop.
    # Bottom: slapback echo as a signal: a plucked note's decaying wave and its copy one tape delay
    # later, quieter, at 135 ms (Halmrast's measurement of Sun records, 134-137 ms).
    gx, gy, cw, rh = 60, 46, 40.0, 26
    rows = ['EIGHTHS', 'SNARE', 'KICK']
    d.group('thin')
    for i in range(9):
        x = gx + i * cw
        d.line((x, gy - 6), (x, gy + 3 * rh))
    for j in range(4):
        d.line((gx, gy + j * rh), (gx + 8 * cw, gy + j * rh))
    d.group()
    d.line((gx, gy - 10), (gx, gy + 3 * rh + 4)); d.line((gx + 4 * cw, gy - 10), (gx + 4 * cw, gy + 3 * rh + 4))
    d.line((gx + 8 * cw, gy - 10), (gx + 8 * cw, gy + 3 * rh + 4))
    for i in range(8):                                        # eighths
        d.circle(gx + (i + 0.5) * cw / 1, gy + rh / 2, 3)
    for beat in range(8):                                     # quarter beats, 4 a bar
        cx = gx + beat * cw + cw / 2
        if beat % 2 == 1:                                     # 2 and 4: the backbeat
            d.circle(cx, gy + 1.5 * rh, 8); d.circle(cx, gy + 1.5 * rh, 4.5)
        else:
            d.circle(cx, gy + 2.5 * rh, 7)
    d.group('mid')
    for i, r in enumerate(rows):
        d.text(gx - 6, gy + i * rh + rh / 2 + 3, r, size=7, anchor='end')
    for beat in range(8):
        d.text(gx + beat * cw + cw / 2, gy - 12, str(beat % 4 + 1), size=7)

    # slapback
    ax, ay, aw = 60, 228, 320
    ms = lambda t: ax + t * aw / 400.0
    d.group('thin')
    d.line((ax, ay), (ax + aw, ay))
    for t in range(0, 401, 100):
        d.line((ms(t), ay + 26), (ms(t), ay + 32))
    d.line((ax, ay + 29), (ax + aw, ay + 29))
    d.group()
    def burst(t0, amp):
        pts = []
        for k in range(181):
            t = k * 0.9
            env = amp * math.exp(-t / 45.0) * (1 - math.exp(-t / 2.0))
            pts.append((ms(t0 + t), ay - env * math.sin(2 * math.pi * t / 9.0)))
        return pts
    d.line(*burst(0, 30))
    d.group('mid')
    d.line(*burst(135, 14))
    d.line((ms(0), ay - 60), (ms(0), ay - 52)); d.line((ms(135), ay - 60), (ms(135), ay - 52))
    d.line((ms(0), ay - 56), (ms(135), ay - 56))
    _arrow(d, (ms(20), ay - 56), (ms(0), ay - 56), 4); _arrow(d, (ms(115), ay - 56), (ms(135), ay - 56), 4)
    for t in range(0, 401, 100):
        d.text(ms(t), ay + 42, str(t) + (' MS' if t == 400 else ''), size=7, anchor='end' if t == 400 else 'middle')
    d.text(ms(67), ay - 62, '≈135 MS', size=7)
    d.text(ms(24), ay - 38, 'DRY', size=7, anchor='start')
    d.text(ms(170), ay - 20, 'TAPE ECHO', size=7, anchor='start')
    d.text(200, 140, 'TWO BARS OF 4/4 · BACKBEAT ON 2 AND 4', size=7)
    d.text(200, 292, 'SLAPBACK · ONE REPEAT, QUIETER · SCHEMATIC WAVE', size=7)
    return d


def _ladder_db(w, k):
    """Gain in dB of an ideal four-pole ladder low-pass with feedback k, at w = f/fc, normalized to 0 dB at DC."""
    s = 1j * w
    h = (1 + k) / ((1 + s) ** 4 + k)
    return 20 * math.log10(abs(h))


def moog():
    d = D()
    # Top: a patch, as cords between modules: the keyboard's control voltage (1 V an octave) sets the
    # oscillator's pitch and gates the envelope; the oscillator's sawtooth goes through the ladder
    # filter to the amplifier, whose loudness the envelope's voltage shapes. Bottom: the ladder
    # filter's response, computed for an ideal four-pole ladder, H(s) = (1+k)/((1+s)^4 + k), on a
    # log-frequency axis, with no feedback (k = 0, falling 24 dB an octave) and with k = 3.5.
    bw, bh = 56, 26
    boxes = {'KEYS': (20, 30), 'VCO': (110, 30), 'VCF': (200, 30), 'VCA': (290, 30), 'ENV': (200, 84)}
    c = lambda n, dx=0.5, dy=0.5: (boxes[n][0] + bw * dx, boxes[n][1] + bh * dy)
    d.group('thin')
    d.line((370, 43), (388, 43))
    d.group()
    for n, (x, y) in boxes.items():
        _box(d, x, y, bw, bh)
        for jx in (x + 8, x + bw - 8):                        # jacks
            d.circle(jx, y + bh - 6, 2.2)
    d.group('mid')
    # audio path: straight cords
    for a_, b_ in (('VCO', 'VCF'), ('VCF', 'VCA')):
        p, q = c(a_, 1, 0.5), c(b_, 0, 0.5)
        d.line(p, q); _arrow(d, p, q, 4)
    p = c('VCA', 1, 0.5); d.line(p, (370, p[1])); _arrow(d, p, (370, p[1]), 4)
    # control path: sagging cords
    def cord(p, q, sag=18):
        m = ((p[0] + q[0]) / 2, max(p[1], q[1]) + sag)
        pts = [((1 - t) ** 2 * p[0] + 2 * (1 - t) * t * m[0] + t * t * q[0],
                (1 - t) ** 2 * p[1] + 2 * (1 - t) * t * m[1] + t * t * q[1]) for t in [i / 20 for i in range(21)]]
        d.dashed(*pts, dash=3, gap=2)
    cord(c('KEYS', 1, 0.75), c('VCO', 0, 0.75), 10)
    cord(c('KEYS', 0.5, 1), c('ENV', 0, 0.5), 30)
    cord(c('ENV', 1, 0.5), c('VCA', 0.5, 1), 4)
    cord(c('ENV', 0.5, 0), c('VCF', 0.5, 1), 0)

    # response curve
    px, py, pw, ph = 60, 150, 300, 110
    lo, hi = -1.0, 1.0                                        # log10(f/fc) from 0.1 to 10
    top, bot = 20.0, -60.0
    X = lambda lw: px + (lw - lo) / (hi - lo) * pw
    Y = lambda db: py + (top - max(bot, min(top, db))) / (top - bot) * ph
    d.group('thin')
    for db in (20, 0, -20, -40, -60):
        d.line((px, Y(db)), (px + pw, Y(db)))
    for lw in (-1, 0, 1):
        d.line((X(lw), py), (X(lw), py + ph))
    for lw in (math.log10(2), math.log10(4)):                 # octaves above cutoff
        d.line((X(lw), Y(0)), (X(lw), py + ph))
    d.group()
    for k in (0.0, 3.5):
        pts = []
        for i in range(201):
            lw = lo + (hi - lo) * i / 200
            pts.append((X(lw), Y(_ladder_db(10 ** lw, k))))
        d.line(*pts)
    d.group('mid')
    d.text(px - 4, Y(0) + 3, '0', size=7, anchor='end')
    d.text(px - 4, Y(-20) + 3, '-20', size=7, anchor='end')
    d.text(px - 4, Y(-40) + 3, '-40', size=7, anchor='end')
    d.text(px - 4, Y(20) + 3, '+20', size=7, anchor='end')
    d.text(px - 4, Y(-60) + 3, 'DB', size=7, anchor='end')
    d.text(X(-1), py + ph + 11, '0.1', size=7)
    d.text(X(0), py + ph + 11, 'CUTOFF', size=7)
    d.text(X(1), py + ph + 11, '10×', size=7)
    d.text(X(0.62), Y(-24) - 4, '−24 DB AN OCTAVE', size=7, anchor='start')
    d.text(X(0.05), Y(14), 'RESONANCE', size=7, anchor='start')
    for n, (x, y) in boxes.items():
        d.text(x + bw / 2, y + 12, n, size=7)
    d.text(c('KEYS')[0] + 34, 68, '1 V / OCTAVE', size=7, anchor='start')
    d.text(380, 36, 'OUT', size=7)
    d.text(200, 292, 'A PATCH · THE LADDER FILTER, COMPUTED', size=7)
    return d


PLATES = {
    'cage-silence': cage_silence,
    'rock-and-roll': rock_and_roll,
    'moog': moog,
}
