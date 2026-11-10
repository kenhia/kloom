"""Plates for Sound and Score's Tuning trail, part tune1 (sprint 058). See plates_for.py."""
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


def ptolemy_harmonics():
    d = D()
    # Two kanones, each a string of 120 parts over Ptolemy's 120-part ruler, drawn from part 84 to
    # the fixed bridge at 120 at 8.6 px a part (the string runs on, broken off, to the nut at 0).
    # Each holds one tetrachord, a fourth from 120 (hypate) to 90 (mese), its two movable notes set
    # by bridges at the computed lengths: above, Ptolemy's tense diatonic (16:15, 9:8, 10:9 rising
    # from the hypate), 120, 112.5, 100, 90; below, the Pythagorean ditonic (256:243, 9:8, 9:8),
    # 120, 113.906, 101.25, 90. A bracket marks each tetrachord's major third, parhypate to mese.
    u0, s, x0 = 84, 8.6, 46
    X = lambda u: x0 + (u - u0) * s
    rows = [
        (92, [120, 112.5, 100, 90], '5:4', 'PTOLEMY, TENSE DIATONIC: 16:15 · 9:8 · 10:9'),
        (196, [120, 243 / 256 * 120, 243 / 256 * 120 * 8 / 9, 90], '81:64', 'PYTHAGOREAN: 256:243 · 9:8 · 9:8'),
    ]
    d.group('thin')
    for y, *_ in rows:
        d.line((X(u0), y + 14), (X(120), y + 14))                      # the ruler
        for u in range(u0, 121):
            d.line((X(u), y + 14), (X(u), y + (22 if u % 10 == 0 else (19 if u % 5 == 0 else 17))))
    for u in (90, 120):                                                  # the fourth, 4:3, common to both
        d.line((X(u), 56), (X(u), 244))
    d.group()
    for y, *_ in rows:
        d.line((X(u0) - 6, y - 4), (X(120) + 8, y - 4), (X(120) + 8, y + 14), (X(u0) - 6, y + 14))   # the box
        d.line((X(u0) - 6, y - 10), (X(120), y - 10))                    # the string
        d.line((X(120) - 4, y - 4), (X(120), y - 10), (X(120) + 4, y - 4))   # the fixed bridge
        bx = X(u0) - 6                                                   # the break: string and box run on
        d.line((bx - 4, y - 14), (bx + 2, y - 6), (bx - 2, y), (bx + 4, y + 8), (bx - 2, y + 18))
    d.group('mid')
    for y, lengths, third, _ in rows:
        for u in lengths[1:3]:                                           # the movable notes' bridges
            d.line((X(u) - 3.5, y - 4), (X(u), y - 10), (X(u) + 3.5, y - 4))
            d.line((X(u), y - 10), (X(u), y - 22))
        a, b = X(lengths[1]), X(90)
        d.line((a, y - 26), (a, y - 32), (b, y - 32), (b, y - 26))      # the third's bracket
    d.group('mid')
    for y, lengths, third, title in rows:
        a = X(lengths[1])
        d.text((a + X(90)) / 2, y - 36, 'THIRD ' + third, size=7)
        d.text(200, y + 50, title, size=7)
        for u in lengths[1:3]:
            d.text(X(u), y + 32, ('%.3f' % u).rstrip('0').rstrip('.'), size=7)
    d.text(X(90), 256, 'MESE 90', size=7)
    d.text(X(120), 256, 'HYPATE 120', size=7)
    d.text(200, 290, 'ONE TETRACHORD, A FOURTH 4:3, ON A 120-PART RULER', size=7)
    return d


def meantone():
    d = D()
    # The circle of fifths as tuned in quarter-comma meantone on a twelve-note keyboard: eleven
    # fifths of 5^(1/4) = 1.4953 (each a quarter of the syntonic comma narrow) drawn as chords, and
    # the twelfth, G sharp up to E flat, which is really a diminished sixth of 1.5312, left as a
    # gap with a jagged line. Four narrowed fifths, C G D A E, land on a pure third C:E = 5:4.
    cx, cy, r = 128, 148, 100
    names = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯', 'C♯', 'G♯', 'E♭', 'B♭', 'F']
    ang = [-90 + 30 * i for i in range(12)]
    P = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in ang]
    d.group('thin')
    d.circle(cx, cy, r)
    d.circle(cx, cy, 3)
    for p in P:
        d.line((cx, cy), p)
    d.group()
    for i in range(12):
        if i == 8:
            continue                                                     # the wolf: G# to Eb
        d.line(P[i], P[(i + 1) % 12])
    for p in P:
        d.circle(p[0], p[1], 3.2)
    d.group('mid')
    # the wolf, drawn as a jagged line across the gap
    a, b = P[8], P[9]
    n = 9
    pts = []
    for k in range(n + 1):
        t = k / n
        x = a[0] + (b[0] - a[0]) * t
        y = a[1] + (b[1] - a[1]) * t
        nx, ny = -(b[1] - a[1]), (b[0] - a[0])
        ln = math.hypot(nx, ny)
        off = (6 if k % 2 else -6) if 0 < k < n else 0
        pts.append((x + nx / ln * off, y + ny / ln * off))
    d.line(*pts)
    # the pure third that four fifths make: C to E
    d.dashed(P[0], P[4], dash=4, gap=3)
    d.group('mid')
    for i, (p, nm) in enumerate(zip(P, names)):
        lx = cx + (r + 15) * math.cos(math.radians(ang[i]))
        ly = cy + (r + 15) * math.sin(math.radians(ang[i])) + 3
        d.text(lx, ly, nm, size=7)
    d.text(cx - 6, cy - 44, 'C:E = 5:4', size=7, anchor='end')
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    d.text(mx + 14, my + 4, 'WOLF', size=7, anchor='start')
    # the arithmetic, at the right
    tx = 318
    rows = [
        ('PURE FIFTH', '3:2 = 1.5000'),
        ('MEANTONE FIFTH', '1.4953'),
        ('FOUR FIFTHS', '1.4953^4 = 5'),
        ('TWO OCTAVES DOWN', '5:4, PURE'),
        ('WOLF G♯-E♭', '1.5312'),
    ]
    for k, (a_, b_) in enumerate(rows):
        d.text(tx, 66 + k * 34, a_, size=7)
        d.text(tx, 78 + k * 34, b_, size=7)
    d.text(200, 290, 'QUARTER-COMMA MEANTONE · ELEVEN NARROW FIFTHS AND A WOLF', size=7)
    return d


def equal_temperament():
    d = D()
    # A fretted string to scale, nut at the left and bridge at the right, 330 px long. Fret n stands
    # where the string left to sound is 2^(-n/12) of the whole, so each fret takes 1/1.059463 of
    # the length before it: a geometric series that reaches the octave, half the string, at fret 12
    # and closes on the bridge. Frets 13 to 24 are drawn dashed, beyond the octave. Below, Vincenzo
    # Galilei's 18:17 rule, each fret 1/18 of what is left, whose twelfth fret falls short of half.
    x0, L = 36, 330
    xb = x0 + L
    X = lambda n: x0 + L * (1 - 2 ** (-n / 12))
    G = lambda n: x0 + L * (1 - (17 / 18) ** n)
    top, bot = 92, 152
    strings = [top + 6 + k * (bot - top - 12) / 5 for k in range(6)]
    d.group('thin')
    d.line((x0, 60), (x0, 230))
    d.line((xb, 60), (xb, 230))
    d.line((X(12), 60), (X(12), 230))
    d.line((x0, 200), (xb, 200))
    d.group()
    d.line((x0, top), (xb, top))
    d.line((x0, bot), (xb, bot))
    d.line((x0, top - 3), (x0, bot + 3))                                 # the nut
    d.line((x0 + 2.5, top - 3), (x0 + 2.5, bot + 3))
    d.line((xb, top - 3), (xb, bot + 3))                                 # the bridge
    for n in range(1, 13):
        d.line((X(n), top), (X(n), bot))
    d.group('mid')
    for y in strings:
        d.line((x0, y), (xb, y))
    for n in range(13, 25):
        d.dashed((X(n), top), (X(n), bot), dash=2, gap=2)
    for n in (3, 5, 7, 9):
        d.circle((X(n - 1) + X(n)) / 2, (top + bot) / 2, 2.2)
    d.circle((X(11) + X(12)) / 2, (top + bot) / 2 - 12, 2.2)
    d.circle((X(11) + X(12)) / 2, (top + bot) / 2 + 12, 2.2)
    # Galilei's rule, as ticks on the measuring line below, beside the equal frets' ticks above it
    for n in range(1, 13):
        d.line((X(n), 200), (X(n), 192))
        d.line((G(n), 200), (G(n), 208))
    _arrow(d, (X(12) + 22, 218), (X(12), 218), 4)
    _arrow(d, (G(12) - 22, 218), (G(12), 218), 4)
    d.group('mid')
    for n in (1, 2, 3, 4, 5, 6, 7, 12, 24):
        d.text(X(n), 84, str(n), size=7)
    d.text(x0, 50, 'NUT', size=7, anchor='start')
    d.text(xb, 50, 'BRIDGE', size=7, anchor='end')
    d.text(X(12), 50, 'OCTAVE, HALF', size=7)
    d.text(X(12) + 6, 172, 'EACH FRET: LENGTH LEFT / 1.059463', size=7, anchor='start')
    d.text(xb, 188, 'EQUAL', size=7, anchor='end')
    d.text(xb, 214, '18:17 RULE', size=7, anchor='end')
    d.text(X(12) + 26, 238, 'TWELFTH FRET 0.36% SHORT', size=7, anchor='start')
    d.text(200, 290, 'TWELVE EQUAL SEMITONES · FRET N AT 1 - 2^(-N/12)', size=7)
    return d


PLATES = {
    'ptolemy-harmonics': ptolemy_harmonics,
    'meantone': meantone,
    'equal-temperament': equal_temperament,
}
