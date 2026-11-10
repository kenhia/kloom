"""Plates for Sound and Score's part script1 (sprint 058): neumes, guido-staff. See plates_for.py."""
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


# Pitches as diatonic steps from Guido's low C: C=0, D=1, E=2, F=3, G=4, a=5, b=6, c=7, d=8.
STEP = 4.5                      # half a line-gap: lines a third apart, as Guido's were


def _staff_y(base, step):
    """y of a pitch on a four-line staff whose lines are D, F, a and c, `base` the D line."""
    return base - (step - 1) * STEP


def _staff(d, x0, x1, base):
    for s in (1, 3, 5, 7):
        y = _staff_y(base, s)
        d.line((x0, y), (x1, y))


def _note(d, x, y, r=2.6):
    _box(d, x - r, y - r, 2 * r, 2 * r)


def neumes():
    d = D()
    # One set of St. Gall-style neumes over "Al-le-lu-ia" (virga, pes, clivis, torculus) and two
    # different melodies that both fit them, on four-line staves: the shapes give the direction of
    # each step, not its size, which is Hucbald's complaint of about 880. The melodies are invented.
    xs = [78, 156, 234, 312]
    syl = ['AL', 'LE', 'LU', 'IA']
    ny = 66                                   # neume baseline
    readings = [
        [[1], [1, 3], [3, 2], [2, 4, 3]],     # D | D-F | F-E | E-G-F
        [[3], [2, 7], [7, 5], [4, 6, 3]],     # F | E-c | c-a | G-b-F
    ]
    bases = [168, 240]

    d.group('thin')
    for x in xs:
        for base in bases:
            d.line((x, _staff_y(base, 8)), (x, base + 8))
    for b in bases:
        _staff(d, 40, 360, b)

    d.group()                                 # the neumes, drawn as a scribe's pen strokes
    x = xs[0]                                 # virga: a rising stroke with a small head
    d.line((x - 3, ny + 8), (x + 3, ny - 10))
    d.line((x + 1, ny - 9), (x + 3, ny - 10))
    x = xs[1]                                 # pes: a hook, then a stroke up
    d.curve(f'M{x - 7} {ny + 1} Q{x - 5} {ny + 9} {x} {ny + 5} L{x + 5} {ny - 11}')
    x = xs[2]                                 # clivis: up and over, then down
    d.curve(f'M{x - 7} {ny + 8} L{x - 2} {ny - 9} Q{x} {ny - 12} {x + 2} {ny - 8} L{x + 6} {ny + 8}')
    x = xs[3]                                 # torculus: a small rise, up, then down
    d.curve(f'M{x - 10} {ny + 2} Q{x - 8} {ny + 7} {x - 5} {ny + 3} L{x - 1} {ny - 9} '
            f'Q{x + 1} {ny - 12} {x + 3} {ny - 8} L{x + 7} {ny + 7}')

    d.group('mid')                            # the two readings, notes joined within a syllable
    for base, rd in zip(bases, readings):
        for x, notes in zip(xs, rd):
            pts = [(x - 9 * (len(notes) - 1) / 2 + 9 * i, _staff_y(base, s)) for i, s in enumerate(notes)]
            if len(pts) > 1:
                d.line(*pts)
            for p in pts:
                _note(d, *p)

    d.group('mid')
    for x, s in zip(xs, syl):
        d.text(x, 96, s, size=7)
    for x, nm in zip(xs, ['VIRGA', 'PES', 'CLIVIS', 'TORCULUS']):
        d.text(x, 32, nm, size=7)
    d.text(40, _staff_y(bases[0], 9) - 4, 'ONE READING', size=7, anchor='start')
    d.text(40, _staff_y(bases[1], 9) - 4, 'ANOTHER, SAME NEUMES', size=7, anchor='start')
    d.text(200, 288, 'NEUMES SHOW UP AND DOWN, NOT HOW FAR · INVENTED EXAMPLE', size=7)
    return d


def guido_staff():
    d = D()
    # Above: the six half-lines of Ut queant laxis begin on C, D, E, F, G and a (Guido's letters,
    # as the Epistola gives them), set on a four-line staff a third apart with the F line, which
    # Guido colored red, and the C line, yellow, marked by their letters. Below: the gamut of
    # twenty notes, Gamma to ee, and the seven six-note hexachords on G, C and F that cover it,
    # each with its one semitone, mi-fa, in the middle. Geometry computed; colors named, not drawn.
    base = 96
    x0, x1 = 60, 360
    xs = [96 + i * 50 for i in range(6)]
    steps = [0, 1, 2, 3, 4, 5]
    syl = ['UT', 'RE', 'MI', 'FA', 'SOL', 'LA']

    d.group('thin')
    d.line((xs[0], _staff_y(base, 0) + 10), (xs[-1], _staff_y(base, 5) - 10))     # the rising line
    for x in xs:
        d.line((x, _staff_y(base, 0) + 12), (x, 118))
    # the gamut: twenty positions
    gx = [30 + i * 17.8 for i in range(20)]
    gy = 168
    for x in gx:
        d.line((x, gy - 4), (x, gy + 4))
    d.line((gx[0], gy), (gx[-1], gy))

    d.group()
    _staff(d, x0, x1, base)
    for x, s in zip(xs, steps):
        _note(d, x, _staff_y(base, s), 3.2)
    # hexachords: start positions in the gamut (Gamma=0, A=1 ... ee=19) and their row
    hexa = [(0, 0), (3, 1), (6, 2), (7, 0), (10, 1), (13, 2), (14, 0)]
    rows = [196, 222, 248]
    for start, row in hexa:
        y = rows[row]
        d.line((gx[start], y), (gx[start + 5], y))
        d.line((gx[start], y - 4), (gx[start], y + 4))
        d.line((gx[start + 5], y - 4), (gx[start + 5], y + 4))

    d.group('thin')
    for start, row in hexa:
        d.line((gx[start], gy + 4), (gx[start], rows[row] - 4))
    d.group('mid')
    for start, row in hexa:                   # the semitone, mi to fa, in each
        y = rows[row]
        mx = (gx[start + 2] + gx[start + 3]) / 2
        d.line((mx - 3, y - 5), (mx, y - 1), (mx + 3, y - 5))
    mx, my = (xs[2] + xs[3]) / 2, _staff_y(base, 0) + 8
    d.line((mx - 3, my - 4), (mx, my), (mx + 3, my - 4))                           # mi-fa on the staff

    d.group('mid')
    for x, s in zip(xs, syl):
        d.text(x, 128, s, size=7)
    d.text(x0 - 4, _staff_y(base, 3) + 2.5, 'F', size=7, anchor='end')
    d.text(x0 - 4, _staff_y(base, 7) + 2.5, 'C', size=7, anchor='end')
    d.text(x1 + 4, _staff_y(base, 3) + 2.5, 'RED', size=7, anchor='start')
    d.text(x1 + 4, _staff_y(base, 7) + 2.5, 'YELLOW', size=7, anchor='start')
    for i, lab in ((0, 'Γ'), (3, 'C'), (6, 'F'), (7, 'G'), (10, 'c'), (13, 'f'), (14, 'g'), (19, 'ee')):
        d.text(gx[i], gy - 8, lab, size=7)
    for y, lab in zip(rows, ['ON G', 'ON C', 'ON F']):
        d.text(gx[-1] + 4, y + 2.5, lab, size=7, anchor='start')
    d.text(200, 288, 'UT QUEANT LAXIS · THE GAMUT, SEVEN HEXACHORDS · V: MI-FA, A SEMITONE', size=7)
    return d


PLATES = {
    'neumes': neumes,
    'guido-staff': guido_staff,
}
