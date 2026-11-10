"""Plates for Sound and Score's part voice2 (sprint 058): the crooner and Auto-Tune. See plates_for.py."""
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


def crooner():
    d = D()
    # Left: a ribbon microphone's motor in front elevation (the ribbon hung between two pole
    # pieces, the field across the gap) and, below, its figure-eight pickup seen from above.
    # Schematic proportions, after Olson's "essential elements of a velocity microphone" (1940).
    # Right: the proximity effect, computed. A pressure-gradient (ribbon) microphone's output
    # against a pressure microphone's, for a point source at distance r, is sqrt(1 + 1/(kr)^2),
    # k = 2*pi*f/c; plotted in dB for r = 5, 15 and 60 cm, c = 343 m/s.
    cx, top, bot = 100, 30, 150
    gap = 7
    pw = 34
    d.group('thin')
    d.line((cx, top - 10), (cx, bot + 10))                                    # the ribbon's axis
    for y in range(44, 140, 16):                                                 # field lines across the gap
        d.line((cx - gap - pw + 6, y), (cx + gap + pw - 6, y))
    # the polar pattern's construction: its axis and the singer's line
    py = 212
    d.line((cx - 66, py), (cx + 66, py))
    d.line((cx, py - 38), (cx, py + 38))

    d.group()
    # pole pieces, tapering toward the gap
    _box(d, cx - gap - pw, top, pw, bot - top)
    _box(d, cx + gap, top, pw, bot - top)
    # the corrugated ribbon: a zigzag in the gap
    pts = []
    n = 40
    for i in range(n + 1):
        y = top + 4 + i * (bot - top - 8) / n
        pts.append((cx + (2.6 if i % 2 else -2.6), y))
    d.line(*pts)
    d.line((cx - 4, top + 2), (cx + 4, top + 2)); d.line((cx - 4, bot - 2), (cx + 4, bot - 2))
    # figure eight: two circles touching at the microphone, along the singer's axis
    rr = 28
    d.arc(cx - rr, py, rr, 0, 360)
    d.arc(cx + rr, py, rr, 0, 360)

    d.group('mid')
    for y in range(44, 140, 16):                                                 # field direction
        _arrow(d, (cx + gap + pw - 16, y), (cx + gap + pw - 8, y), 3)
    # sound arriving from the singer, from the left
    d.line((cx - 88, py), (cx - 70, py))
    _arrow(d, (cx - 88, py), (cx - 70, py), 4)
    d.circle(cx, py, 2.2)
    # the null at the sides
    d.line((cx - 3, py - 34), (cx + 3, py - 34)); d.line((cx - 3, py + 34), (cx + 3, py + 34))

    # the proximity effect
    x0, x1, y0, y1 = 236, 384, 230, 40
    fmin, fmax, dbmax = 50.0, 5000.0, 30.0

    def X(f):
        return x0 + (math.log10(f) - math.log10(fmin)) / (math.log10(fmax) - math.log10(fmin)) * (x1 - x0)

    def Y(db):
        return y0 - db / dbmax * (y0 - y1)

    d.group('thin')
    for f in (50, 100, 200, 500, 1000, 2000, 5000):
        d.line((X(f), y0), (X(f), y1))
    for db in (0, 10, 20, 30):
        d.line((x0, Y(db)), (x1, Y(db)))
    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))
    curves = {}
    for r in (0.05, 0.15, 0.60):
        pts = []
        for i in range(81):
            f = fmin * (fmax / fmin) ** (i / 80)
            k = 2 * math.pi * f / 343.0
            db = 10 * math.log10(1 + 1 / (k * r) ** 2)
            pts.append((X(f), Y(min(db, dbmax))))
        curves[r] = pts
        d.line(*pts)
    d.group('mid')
    d.text(cx, top - 14, 'RIBBON BETWEEN POLES', size=7)
    d.text(cx - gap - pw / 2, bot + 14, 'N', size=7)
    d.text(cx + gap + pw / 2, bot + 14, 'S', size=7)
    d.text(cx - 88, py - 7, 'VOICE', size=7, anchor='start')
    d.text(cx, py + 50, 'FIGURE-EIGHT PICKUP, FROM ABOVE', size=7)
    for f, s in ((50, '50'), (100, '100'), (500, '500'), (1000, '1K'), (5000, '5K')):
        d.text(X(f), y0 + 11, s, size=7)
    d.text((x0 + x1) / 2, y0 + 22, 'FREQUENCY, HZ', size=7)
    for db in (10, 20, 30):
        d.text(x0 - 4, Y(db) + 2.5, str(db), size=7, anchor='end')
    d.text(x0, y1 - 8, 'BASS LIFT, DB', size=7, anchor='start')
    # label each curve just above where it starts, at 50 Hz
    for r, s in ((0.05, '5 CM'), (0.15, '15 CM'), (0.60, '60 CM')):
        k = 2 * math.pi * fmin / 343.0
        db = min(10 * math.log10(1 + 1 / (k * r) ** 2), dbmax)
        d.text(x0 + 5, Y(db) - 4, s, size=7, anchor='start')
    d.text(200, 292, 'A RIBBON MICROPHONE AND ITS PROXIMITY EFFECT · COMPUTED', size=7)
    return d


def _sung(t):
    """An invented sung line, in semitones above the lowest grid line: a B held about a third
    of a semitone flat with a 5.5 Hz vibrato, then a slide up to a C held a third sharp."""
    vib = 0.18 * math.sin(2 * math.pi * 5.5 * t)
    if t < 0.55:
        base = 1.68
    elif t < 0.78:
        u = (t - 0.55) / 0.23
        base = 1.68 + (3.3 - 1.68) * (0.5 - 0.5 * math.cos(math.pi * u))
    else:
        base = 3.3
    onset = min(1.0, t / 0.12)
    return base + vib * onset


def _retuned(ts, half):
    """The corrected line: each instant's target is the nearest semitone of the sung pitch,
    and the correction closes half its gap every `half` seconds (Hildebrand's description of
    the retune speed, Time, 2009); half = 0 gives the instant, stepped line."""
    out, c = [], 0.0
    prev = ts[0]
    for t in ts:
        s = _sung(t)
        want = round(s) - s
        if half <= 0:
            c = want
        else:
            a = 1 - 0.5 ** ((t - prev) / half)
            c += (want - c) * a
        prev = t
        out.append(s + c)
    return out


def auto_tune():
    d = D()
    # Two panels, one above the other: a sung line (invented, dashed) against a grid of
    # semitones, and the line Auto-Tune returns, slow above and at a retune speed of zero
    # below. The pitch detection itself (autocorrelation) is assumed exact.
    T0, T1 = 0.0, 1.1
    n = 440
    ts = [T0 + (T1 - T0) * i / n for i in range(n + 1)]
    x0, x1 = 52, 384
    names = ['A', 'A#', 'B', 'C', 'C#']
    panels = ((26, 0.06, 'RETUNE SLOW · HALFWAY IN 60 MS'), (156, 0.0, 'RETUNE SPEED 0 · INSTANT'))
    step = 22

    def X(t):
        return x0 + (t - T0) / (T1 - T0) * (x1 - x0)

    for top, half, label in panels:
        def Y(s, top=top):
            return top + 4 * step - s * step + 8

        d.group('thin')
        for k in range(5):
            d.line((x0, Y(k)), (x1, Y(k)))
        d.line((x0, Y(-0.4)), (x0, Y(4.4)))
        d.group('mid')
        d.dashed(*[(X(t), Y(_sung(t))) for t in ts], dash=3, gap=2.5)
        d.group()
        d.line(*[(X(t), Y(v)) for t, v in zip(ts, _retuned(ts, half))])
        d.group('mid')
        for k, nm in enumerate(names):
            d.text(x0 - 8, Y(k) + 2.5, nm, size=7, anchor='end')
        d.text(x1, top + 2, label, size=7, anchor='end')
    d.group('mid')
    d.text(x0 + 2, 292, 'SUNG (DASHED) AND RETUNED · SEMITONES · INVENTED LINE', size=7, anchor='start')
    _arrow(d, (x1 - 40, 268), (x1, 268), 4)
    d.line((x1 - 40, 268), (x1, 268))
    d.text(x1 - 46, 270.5, 'TIME', size=7, anchor='end')
    return d


PLATES = {'crooner': crooner, 'auto-tune': auto_tune}
