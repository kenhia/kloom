"""Plates for Sound and Score's Number and harmony part harm2 (sprint 058): seikilos, boethius.

See plates_for.py. Helpers copied from music_hand.py, as the brief asks.
"""
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


# The Seikilos song as the stone writes it: per line, (sign, beats, stigme).
# Signs and stigmai are Jan's (Musici scriptores graeci, Supplementum, 1899, p. 38); the lengths are
# the usual modern reading of the diseme and triseme, twelve beats a line. The signs are degrees of
# Alypius's Iastian diatonic, lowest first: reversed gamma (written 'G'), X, Phi, C, O, K, I, Z.
SEIKILOS = [
    [('C', 1, 0), ('Z', 2, 0), ('Z', 3, 1), ('K', 1, 0), ('I', 1, 0), ('Z', 1, 0), ('I', 3, 1)],
    [('K', 2, 0), ('I', 1, 0), ('Z', 1, 1), ('I', 1, 1), ('K', 1, 0), ('O', 1, 0), ('C', 2, 0),
     ('O', 1, 0), ('F', 2, 1)],
    [('C', 1, 0), ('K', 1, 0), ('Z', 1, 0), ('I', 1, 1), ('K', 1, 1), ('I', 1, 0), ('K', 1, 0),
     ('C', 2, 0), ('O', 1, 0), ('F', 2, 1)],
    [('C', 1, 0), ('K', 1, 0), ('O', 1, 0), ('I', 1, 1), ('Z', 1, 1), ('K', 1, 0), ('C', 1, 0),
     ('C', 2, 0), ('C', 1, 0), ('X', 1, 0), ('G', 1, 1)],
]
LEVEL = {'G': 0, 'X': 1, 'F': 2, 'C': 3, 'O': 4, 'K': 5, 'I': 6, 'Z': 7}
LABEL = {'X': 'X', 'F': 'Φ', 'C': 'C', 'O': 'O', 'K': 'K', 'I': 'I', 'Z': 'Z'}


def seikilos():
    d = D()
    # The melody as pitch against time: 48 beats across, the eight degrees up the side, each note a
    # level line as long as it lasts, the four lines of the song between the heavy rules.
    x0, x1, ybase, step = 46, 386, 188, 18
    bw = (x1 - x0) / 48

    def y(level):
        return ybase - level * step

    d.group('thin')
    for lv in range(8):
        d.line((x0, y(lv)), (x1, y(lv)))
    for b in range(0, 49, 6):
        top = y(7) - 10 if b % 12 == 0 else y(7) - 2
        d.line((x0 + b * bw, top), (x0 + b * bw, y(0) + (6 if b % 12 == 0 else 2)))

    notes, t = [], 0
    for row in SEIKILOS:
        for sign, beats, dot in row:
            notes.append((t, beats, LEVEL[sign], dot))
            t += beats
    assert t == 48

    d.group()
    pts = []
    for t0, beats, lv, _ in notes:
        a, b = x0 + t0 * bw, x0 + (t0 + beats) * bw
        pts += [(a, y(lv)), (b, y(lv))]
    d.line(*pts)

    d.group('mid')
    for t0, beats, lv, dot in notes:                       # each note's onset, and its stigme
        a = x0 + t0 * bw
        d.line((a, y(lv) - 3), (a, y(lv) + 3))
        if dot:
            d.circle(a + beats * bw / 2, y(lv) - 6, 1.1)

    # below: the three lengths as the stone marks them, over a ruler of beats
    ly = 246
    d.group('thin')
    for i, beats in enumerate((1, 2, 3)):
        cx = 96 + i * 104
        for k in range(beats + 1):
            d.line((cx + k * 14, ly + 10), (cx + k * 14, ly + 15))
        d.line((cx, ly + 12.5), (cx + beats * 14, ly + 12.5))
    d.group()
    for i, beats in enumerate((1, 2, 3)):
        cx = 96 + i * 104
        mx = cx + beats * 7
        d.line((mx - 3, ly - 6), (mx + 3, ly - 6))         # the letter's stand-in: a short stem
        d.line((mx, ly - 6), (mx, ly + 4))
        if beats >= 2:
            d.line((mx - 7, ly - 11), (mx + 7, ly - 11))      # diseme: a bar over the sign
        if beats == 3:
            d.line((mx + 7, ly - 11), (mx + 7, ly - 16))      # triseme: the bar with a rising stroke

    d.group('mid')
    for lv in range(1, 8):
        sign = [k for k, v in LEVEL.items() if v == lv][0]
        d.text(x0 - 10, y(lv) + 2.5, LABEL[sign], size=7, anchor='end')
    gx, gy = x0 - 14, y(0)                                    # the reversed gamma, drawn: a bar to the left
    d.line((gx - 4, gy - 3.5), (gx, gy - 3.5), (gx, gy + 3.5))
    for i in range(4):
        d.text(x0 + (i * 12 + 6) * bw, y(7) - 14, str(i + 1), size=7)
    for i, word in enumerate(('1 BEAT', 'DISEME 2', 'TRISEME 3')):
        d.text(96 + i * 104 + (i + 1) * 7, ly + 27, word, size=7)
    d.text(200, 288, 'THE SEIKILOS SONG · IASTIAN KEY · 4 LINES OF 12 BEATS', size=7)
    return d


def boethius():
    d = D()
    # The figure two of Friedlein's manuscripts add to De institutione musica I.10: the four hammers'
    # numbers at the corners of a square, sides and diagonals named for their consonances. Below, the
    # same numbers as lengths of one string on a monochord's rule, to scale.
    L, T, S = 135, 36, 130                     # square: left, top, side
    tl, tr, bl, br = (L, T), (L + S, T), (L, T + S), (L + S, T + S)
    d.group('thin')
    d.line((L - 30, T + S / 2), (L + S + 30, T + S / 2))
    d.line((L + S / 2, T - 14), (L + S / 2, T + S + 14))
    d.circle(L + S / 2, T + S / 2, S / 2 * math.sqrt(2))

    d.group()
    d.line(tl, tr, br, bl, closed=True)
    d.line(tl, br)
    d.line(tr, bl)
    d.group('mid')
    for (x, yy) in (tl, tr, bl, br):
        d.circle(x, yy, 4)

    # the monochord: a string of 12 units over a rule, bridges where 9, 8 and 6 units sound
    y0, sx, u = 250, 52, 25                     # string height, its left end, px a unit
    d.group('thin')
    for k in range(13):
        d.line((sx + k * u, y0 + 10), (sx + k * u, y0 + (18 if k % 3 == 0 else 14)))
    d.line((sx, y0 + 10), (sx + 12 * u, y0 + 10))
    d.group()
    d.line((sx - 6, y0 + 4), (sx + 12 * u + 6, y0 + 4), (sx + 12 * u + 6, y0 + 10), (sx - 6, y0 + 10), closed=True)
    d.line((sx, y0), (sx + 12 * u, y0))
    for x in (sx, sx + 12 * u):                 # the fixed bridges at the ends
        d.line((x - 3, y0 + 4), (x, y0 - 3), (x + 3, y0 + 4))
    d.group('mid')
    for n in (9, 8, 6):                         # the sounding lengths, measured from the right
        x = sx + (12 - n) * u
        d.line((x - 3, y0 + 4), (x, y0 - 2), (x + 3, y0 + 4))
        d.line((x, y0 - 6), (x, y0 - 14 - (12 - n) * 5))
    for n in (9, 8, 6):
        x = sx + (12 - n) * u
        top = y0 - 14 - (12 - n) * 5
        _arrow(d, (sx + 12 * u, top), (x, top), 4)
        d.line((x, top), (sx + 12 * u, top))

    d.group('mid')
    d.text(tl[0] - 8, tl[1] - 6, 'XII', size=7, anchor='end')
    d.text(tr[0] + 8, tr[1] - 6, 'VIIII', size=7, anchor='start')
    d.text(bl[0] - 8, bl[1] + 10, 'VI', size=7, anchor='end')
    d.text(br[0] + 8, br[1] + 10, 'VIII', size=7, anchor='start')
    d.text(L + S / 2, T - 4, 'DIATESSARON 4:3', size=7)
    d.text(L + S / 2, T + S + 11, 'DIATESSARON 4:3', size=7)
    d.text(L - 34, T + S / 2 + 2.5, 'DIAPASON 2:1', size=7, anchor='end')
    d.text(L + S + 34, T + S / 2 + 2.5, 'TONUS 9:8', size=7, anchor='start')
    d.text(L + S / 2, T + 20, 'DIAPENTE 3:2', size=7)
    d.text(sx + 12 * u + 12, y0 + 3, '12', size=7, anchor='start')
    for n in (9, 8, 6):
        d.text(sx + (12 - n) * u - 5, y0 - 12 - (12 - n) * 5, str(n), size=7, anchor='end')
    d.text(200, 290, 'DE INSTITUTIONE MUSICA I.10 · THE SAME NUMBERS ON THE RULE', size=7)
    return d


PLATES = {
    'seikilos': seikilos,
    'boethius': boethius,
}
