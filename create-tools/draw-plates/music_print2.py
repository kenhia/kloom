"""Plates for Sound and Score's part print2 (sprint 058): luther-chorale and palestrina. See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def luther_chorale():
    d = D()
    # Ein feste Burg's first phrase as a pitch line against time, from Zahn no. 7377a (Klug's
    # Wittenberg hymnal of 1535), F major, one unit a quarter note of Zahn's reduced values. Pitches
    # are diatonic steps above E4 (E4 0, F4 1, ... F5 8), so the staff's five lines fall on 0, 2, 4, 6, 8.
    notes = [  # (step, length in quarters, syllable)
        (8, 1, 'Ein'), (8, 2, 'fe-'), (8, 2, 'ste'), (5, 2, 'Burg'), (6, 1, 'ist'), (8, 2, 'un-'),
        (7, 1, ''), (6, 2, 'ser'), (5, 2, 'Gott'),
    ]
    total = sum(n[1] for n in notes)
    x0, x1 = 44, 384
    u = (x1 - x0) / total
    top, step = 84, 10                       # F5 at y=70; a diatonic step is 9 px
    def y(s):
        return top + (8 - s) * step
    d.group('thin')
    t = 0
    for s, n, _ in notes:                   # a tick at each quarter
        for k in range(n):
            xx = x0 + (t + k) * u
            d.line((xx, y(0) + 4), (xx, y(0) + 8))
        t += n
    for s in (1, 3, 5, 7):                  # the spaces, as faint guides
        d.line((x0, y(s)), (x1, y(s)))
    d.group('mid')
    for s in (0, 2, 4, 6, 8):               # the five staff lines
        d.line((x0, y(s)), (x1, y(s)))
    d.group()
    t, pts = 0, []
    for s, n, _ in notes:
        xa, xb = x0 + t * u, x0 + (t + n) * u
        pts += [(xa, y(s)), (xb - 1.5, y(s))]
        t += n
    d.line(*pts)
    d.group()
    t = 0
    for s, n, _ in notes:
        if s is not None:
            d.circle(x0 + t * u + 3, y(s), 3)
        t += n
    # the drop of a fourth, F to C, on "Burg", as a bracket
    d.group('mid')
    xb = x0 + 5 * u
    d.line((xb - 6, y(8)), (xb - 10, y(8)), (xb - 10, y(5)), (xb - 6, y(5)))
    d.group('mid')
    t = 0
    for s, n, syl in notes:
        if syl:
            d.text(x0 + t * u + 2, y(0) + 22, syl, size=7, anchor='start')
        t += n
    for s, name in ((8, 'F'), (6, 'D'), (4, 'B♭'), (2, 'G'), (0, 'E')):
        d.text(x0 - 8, y(s) + 2.5, name, size=7, anchor='end')
    d.text(xb - 14, (y(8) + y(5)) / 2 + 2.5, '4TH', size=7, anchor='end')
    d.text(x0 + 2, y(8) - 14, 'PITCH', size=7, anchor='start')
    d.text(x1, y(0) + 36, 'TIME, IN QUARTER NOTES →', size=7, anchor='end')
    d.text(214, 262, 'EIN FESTE BURG IST UNSER GOTT · THE FIRST PHRASE', size=7)
    d.text(214, 276, 'ZAHN NO. 7377A, FROM KLUG, WITTENBERG 1535 · F MAJOR', size=7)
    return d


def palestrina():
    d = D()
    # Fux's first exercise in first species (Gradus ad Parnassum, 1725, p. 47): a cantus firmus in
    # the Dorian mode, D F E D G F A G F E D, and Joseph's counterpoint above it, note against note,
    # A A G A B C C# B D C# D. Steps are diatonic above D4; C# is drawn at C's height with a sharp.
    cf = [0, 2, 1, 0, 3, 2, 4, 3, 2, 1, 0]
    cp = [4, 4, 3, 4, 5, 6, 6, 5, 7, 6, 7]
    sharp = {9}
    iv = [b - a + 1 for a, b in zip(cf, cp)]       # 5 3 3 5 3 5 3 3 6 6 8, as Fux prints them
    x0, x1 = 66, 376
    dx = (x1 - x0) / (len(cf) - 1)
    base, step = 214, 17
    def y(s):
        return base - s * step
    xs = [x0 + i * dx for i in range(len(cf))]
    d.group('thin')
    for s in range(0, 8):
        d.line((x0 - 14, y(s)), (x1 + 10, y(s)))
    for x in xs:
        d.line((x, y(0) + 6), (x, y(0) + 12))
    d.group()
    d.line(*[(x, y(s)) for x, s in zip(xs, cf)])
    d.line(*[(x, y(s)) for x, s in zip(xs, cp)])
    for x, s in zip(xs, cf):
        d.circle(x, y(s), 3.2)
    for x, s in zip(xs, cp):
        d.circle(x, y(s), 3.2)
    d.group('mid')
    for i, (x, a, b) in enumerate(zip(xs, cf, cp)):  # the interval between the voices
        d.dashed((x, y(a) - 4), (x, y(b) + 4), dash=2, gap=2)
    for i in sharp:                                    # the raised leading note, C#
        x, yy = xs[i] - 11, y(cp[i]) + 9
        d.line((x - 2, yy - 4), (x - 2, yy + 4)); d.line((x + 1, yy - 4), (x + 1, yy + 4))
        d.line((x - 4, yy - 0.5), (x + 3, yy - 2.5)); d.line((x - 4, yy + 2.5), (x + 3, yy + 0.5))
    for x, v in zip(xs, iv):                           # perfect consonances ringed
        if v in (5, 8):
            d.circle(x, 52, 6.5)
    d.group('mid')
    for x, v in zip(xs, iv):
        d.text(x, 55, str(v), size=7)
    for s, name in ((0, 'D'), (2, 'F'), (4, 'A'), (6, 'C'), (7, 'D')):
        d.text(x0 - 18, y(s) + 2.5, name, size=7, anchor='end')
    d.text(x0 - 24, 55, 'INTERVAL', size=7, anchor='end')
    d.text(x1 - 6, y(7) - 14, 'COUNTERPOINT', size=7, anchor='end')
    d.text(x1 - 6, y(0) + 20, 'CANTUS FIRMUS', size=7, anchor='end')
    d.text(214, 270, 'FIRST SPECIES · NOTE AGAINST NOTE · DORIAN', size=7)
    d.text(214, 284, 'FUX, GRADUS AD PARNASSUM, 1725 · 5 AND 8 RINGED', size=7)
    return d


PLATES = {
    'luther-chorale': luther_chorale,
    'palestrina': palestrina,
}
