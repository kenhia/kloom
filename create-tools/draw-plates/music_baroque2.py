"""Plates for Sound and Score's part baroque2 (sprint 058): the Well-Tempered Clavier, Vivaldi's
Four Seasons and Handel's Messiah. See plates_for.py."""
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


def well_tempered_clavier():
    """The order of Book I: twelve tonics round a chromatic circle, majors on the outer ring and
    minors on the inner, and the book's path from C major to B minor zigzagging between them."""
    d = D()
    cx, cy, R1, R2 = 200, 138, 104, 64
    names = ['C', 'C♯', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B']

    def at(r, i):
        a = math.radians(-90 + 30 * i)
        return (cx + r * math.cos(a), cy + r * math.sin(a))

    d.group('thin')
    d.circle(cx, cy, R1)
    d.circle(cx, cy, R2)
    for i in range(12):
        d.line(at(10, i), at(R1 + 8, i))

    path = []
    for i in range(12):
        path += [at(R1, i), at(R2, i)]
    d.group()
    d.line(*path)
    _arrow(d, path[-2], path[-1], 6)

    d.group('mid')
    for i in range(12):
        x, y = at(R1, i)
        d.circle(x, y, 4.2)
        x, y = at(R2, i)
        d.circle(x, y, 3)
    x, y = at(R1, 0)
    d.circle(x, y, 7.5)

    d.group('mid')
    for i, n in enumerate(names):
        x, y = at(R1 + 20, i)
        d.text(x, y + 2.5, n, size=7)
    x, y = at(R1, 0)
    d.text(x + 12, y + 14, 'START', size=7, anchor='start')
    x, y = at(R2, 11)
    d.text(x + 9, y + 13, 'END', size=7, anchor='start')
    d.text(cx, cy + 4, 'BOOK I', size=7)
    d.text(46, 282, 'OUTER RING · MAJOR', size=7, anchor='start')
    d.text(354, 282, 'INNER RING · MINOR', size=7, anchor='end')
    d.text(200, 296, 'KÖTHEN 1722 · 24 KEYS · EACH PAIR UP A SEMITONE', size=7)
    return d


# Spring's first movement in ritornello form, by bar (82 bars): from José Rodríguez Alvira's
# analysis at teoria.com. 'T' is a ritornello for the whole band, 'S' an episode for the soloist.
SPRING = [
    ('T', 1, 13, 'E', 'A'), ('S', 13, 27, 'E', 'B'), ('T', 27, 30, 'E', ''), ('S', 31, 40, 'E', 'C'),
    ('T', 40, 44, 'B', ''), ('S', 44, 55, '', 'D'), ('T', 55, 59, 'C♯m', ''), ('S', 59, 65, 'C♯m', 'E'),
    ('T', 66, 70, 'C♯m', ''), ('X', 70, 82, 'E', ''),
]


def vivaldi_seasons():
    """Spring, first movement: ritornellos for the band above, the solo violin's episodes below,
    each the length of its bars, with the key each ritornello stands in and the sonnet's letters."""
    d = D()
    x0, x1, nb = 40, 376, 82
    sx = (x1 - x0) / nb
    def X(bar):
        return x0 + (bar - 1) * sx
    yt, ys, h = 80, 132, 30

    d.group('thin')
    for b in range(1, nb + 2, 10):
        d.line((X(b), 66), (X(b), 222))
    d.line((x0, 222), (x1, 222))
    d.line((x0, yt + h + 13), (x1, yt + h + 13))

    d.group()
    for kind, a, b, key, letter in SPRING:
        w = X(b) - X(a)
        if kind == 'T':
            _box(d, X(a), yt, w, h)
        elif kind == 'S':
            _box(d, X(a), ys, w, h)
        else:
            _box(d, X(a), yt, w, ys + h - yt)

    d.group('mid')
    for kind, a, b, key, letter in SPRING:
        if kind == 'S':                             # the soloist's figuration as a wave
            n = max(3, int((X(b) - X(a)) / 6))
            pts = [(X(a) + 3 + (X(b) - X(a) - 6) * k / (n * 4), ys + h / 2 + 7 * math.sin(k * math.pi / 2)) for k in range(n * 4 + 1)]
            d.line(*pts)
        if kind == 'T':                             # the full band as stacked lines
            for k in range(1, 4):
                d.line((X(a) + 2, yt + k * h / 4), (X(b) - 2, yt + k * h / 4))
    # the stepped line of keys under it: E, then B, through the storm to C sharp minor, home to E
    lv = {'E': 198, 'B': 186, 'C♯m': 210}
    # (the storm, bars 44-55, passes through E and B to C sharp minor: drawn as one slope)
    pts = [(X(1), lv['E']), (X(40), lv['E']), (X(40), lv['B']), (X(44), lv['B']), (X(55), lv['C♯m']),
           (X(70), lv['C♯m']), (X(70), lv['E']), (X(83), lv['E'])]
    d.line(*pts)

    d.group('mid')
    for kind, a, b, key, letter in SPRING:
        if letter:
            yy = yt - 8 if kind == 'T' else ys + h + 11
            d.text((X(a) + X(b)) / 2, yy, letter, size=7)
    d.text(x0, 56, 'TUTTI · RITORNELLO', size=7, anchor='start')
    d.text(x0 + 0, ys - 5, 'SOLO VIOLIN', size=7, anchor='start')
    for k in ('E', 'B', 'C♯m'):
        d.text(x0 - 4, lv[k] + 2.5, k, size=7, anchor='end')
    for b in (1, 21, 41, 61, 81):
        d.text(X(b), 233, str(b), size=7)
    d.text(200, 252, 'BARS', size=7)
    d.text(200, 286, 'SPRING · FIRST MOVEMENT · LETTERS A–E FROM THE SONNET', size=7)
    return d


# Messiah's 53 numbers, Novello's numbering, by kind: C chorus, A air or duet, R recitative or
# arioso, I instrumental. From the table of movements in Wikipedia's "Structure of Handel's Messiah".
MESSIAH = [
    'IRACRACRARACIRRRCARAC',          # Part I, 1-21
    'CACCCRCRRRACRCACARACRAC',        # Part II, 22-44
    'ACRARACAC',                      # Part III, 45-53
]


def handel_messiah():
    """Messiah's three parts as rows of numbers, each a stem whose height says what it is: tall for
    a chorus, middle for an air, short for a recitative, a ring for the two instrumental pieces."""
    d = D()
    x0, step = 40, 14.5
    ys = [92, 172, 252]
    H = {'C': 34, 'A': 20, 'R': 9}
    first = [1, 22, 45]

    d.group('thin')
    for y, row in zip(ys, MESSIAH):
        d.line((x0 - 10, y), (x0 + step * (len(row) - 1) + 10, y))
        d.line((x0 - 10, y - H['C']), (x0 - 6, y - H['C']))
        d.line((x0 - 10, y - H['A']), (x0 - 6, y - H['A']))

    d.group()
    for y, row, n0 in zip(ys, MESSIAH, first):
        for i, k in enumerate(row):
            x = x0 + step * i
            if k == 'I':
                d.circle(x, y - 5, 4)
            else:
                d.line((x, y), (x, y - H[k]))

    d.group('mid')
    for y, row, n0 in zip(ys, MESSIAH, first):
        for i, k in enumerate(row):
            x = x0 + step * i
            if k == 'C':
                d.circle(x, y - H['C'] - 3, 3)
            if k == 'A':
                d.line((x - 3, y - H['A']), (x + 3, y - H['A']))
    # the two endings: Hallelujah closing Part II, Worthy is the Lamb and Amen closing Part III
    xh = x0 + step * 22
    d.line((xh, ys[1] - H['C'] - 8), (xh, ys[1] - H['C'] - 18))
    xa = x0 + step * 8
    d.line((xa, ys[2] - H['C'] - 8), (xa, ys[2] - H['C'] - 18))

    d.group('mid')
    d.text(x0 - 10, ys[0] + 14, 'PART I · PROPHECY AND NATIVITY · 1–21', size=7, anchor='start')
    d.text(x0 - 10, ys[1] + 14, 'PART II · PASSION · 22–44', size=7, anchor='start')
    d.text(x0 - 10, ys[2] + 14, 'PART III · RESURRECTION · 45–53', size=7, anchor='start')
    d.text(xh, ys[1] - H['C'] - 22, 'HALLELUJAH', size=7, anchor='end')
    d.text(xa, ys[2] - H['C'] - 22, 'AMEN', size=7)
    d.text(392, ys[2] - 44, 'TALL · CHORUS', size=7, anchor='end')
    d.text(392, ys[2] - 32, 'MIDDLE · AIR', size=7, anchor='end')
    d.text(392, ys[2] - 20, 'SHORT · RECITATIVE', size=7, anchor='end')
    d.text(392, ys[2] - 8, 'RING · SINFONY, PIFA', size=7, anchor='end')
    return d


PLATES = {
    'well-tempered-clavier': well_tempered_clavier,
    'vivaldi-seasons': vivaldi_seasons,
    'handel-messiah': handel_messiah,
}
