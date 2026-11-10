"""Plates for Sound and Score's part classic1 (sprint 058): mozart-vienna, haydn-london. See plates_for.py."""
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


def mozart_vienna():
    d = D()
    # Mozart's list of engagements for Lent 1784, from his letter of 3 March 1784 (Bauer/Deutsch 778),
    # drawn as a calendar: one column a day from Thursday 26 February to Saturday 3 April (1784 was a
    # leap year, so 38 days), one row a host. Circles are evenings played in others' houses or series;
    # squares are his own concerts. The dates and hosts are the letter's; nothing else is.
    feb = 31 + 29                                       # day of year of 29 Feb 1784
    def doy(m, dd):
        return {2: 31, 3: feb, 4: feb + 31}[m] + dd
    start = doy(2, 26)
    rows = [
        ('GOLITSYN', [(2, 26), (3, 4), (3, 11), (3, 18), (3, 25)], 'c'),
        ('ESTERHAZY', [(3, 1), (3, 5), (3, 8), (3, 12), (3, 15), (3, 19), (3, 22), (3, 26), (3, 29)], 'c'),
        ('RICHTER', [(3, 20), (3, 27), (4, 3)], 'c'),
        ('TRATTNERHOF', [(3, 17), (3, 24), (3, 31)], 's'),
        ('THEATER', [(3, 21), (4, 1)], 's'),
    ]
    x0, step, n = 98, 7.4, 38
    ys = [92, 124, 156, 188, 220]
    xs = [x0 + i * step for i in range(n)]
    sundays = [i for i in range(n) if (i + 4) % 7 == 0]   # 26 Feb 1784 was a Thursday; 29 Feb a Sunday

    d.group('thin')
    for y in ys:
        d.line((x0 - 4, y), (xs[-1] + 4, y))
    for i in range(n):
        d.line((xs[i], 236), (xs[i], 240))
    for i in sundays:
        d.line((xs[i], 70), (xs[i], 236))
    d.line((x0 - 4, 236), (xs[-1] + 4, 236))

    d.group()
    for (name, dates, kind), y in zip(rows, ys):
        for m, dd in dates:
            x = xs[doy(m, dd) - start]
            if kind == 'c':
                d.circle(x, y, 2.9)
            else:
                _box(d, x - 3.2, y - 3.2, 6.4, 6.4)

    d.group('mid')
    for (name, dates, kind), y in zip(rows, ys):
        d.text(x0 - 10, y + 2.5, name, size=7, anchor='end')
        d.text(xs[-1] + 12, y + 2.5, str(len(dates)), size=7, anchor='middle')
    for label, (m, dd) in (('FEB 26', (2, 26)), ('MAR 7', (3, 7)), ('MAR 21', (3, 21)), ('APR 3', (4, 3))):
        d.text(xs[doy(m, dd) - start], 252, label, size=7)
    d.text(xs[sundays[0]], 64, 'SUNDAYS', size=7)
    d.text(200, 276, 'CIRCLE: PLAYING FOR OTHERS · SQUARE: HIS OWN CONCERTS', size=7)
    d.text(200, 290, "22 ENGAGEMENTS, LENT 1784, AS MOZART LISTED THEM ON 3 MARCH", size=7)
    return d


def haydn_london():
    d = D()
    # The first sixteen bars of the Andante of Haydn's Symphony No. 94, first violins, from the
    # movement's opening as Wikipedia's article prints it (2/4, C major): eight bars piano, the same
    # eight bars pianissimo with the lower strings plucked, then the fortissimo chord on the second
    # beat of bar 16, with the timpani. Each eighth note is a point on a pitch line over a treble
    # staff (line art, not engraving), with middle C as a dashed line; below, the dynamic level
    # against time. Pitches are counted in diatonic steps from middle C.
    step = {'G3': -3, 'B3': -1, 'C4': 0, 'D4': 1, 'E4': 2, 'F4': 3, 'F#4': 3, 'G4': 4, 'B4': 6,
            'C5': 7, 'G5': 11}
    half = [('C4', 1), ('C4', 1), ('E4', 1), ('E4', 1), ('G4', 1), ('G4', 1), ('E4', 2),
            ('F4', 1), ('F4', 1), ('D4', 1), ('D4', 1), ('B3', 1), ('B3', 1), ('G3', 2),
            ('C4', 1), ('C4', 1), ('E4', 1), ('E4', 1), ('G4', 1), ('G4', 1), ('E4', 2),
            ('C5', 1), ('C5', 1), ('F#4', 1), ('F#4', 1)]
    first = half + [('G4', 2), ('G3', 1), (None, 1)]
    second = half + [('G4', 1), (None, 1), ('CHORD', 2)]
    x0, w = 34, 336
    xw = w / 64.0                                       # 16 bars of 2/4: 64 eighth notes
    yc, dy = 160, 6.0                                   # middle C, and one diatonic step
    def y_of(s):
        return yc - s * dy

    d.group('thin')
    for s in (2, 4, 6, 8, 10):                          # the treble staff: E4 G4 B4 D5 F5
        d.line((x0, y_of(s)), (x0 + w, y_of(s)))
    for b in range(17):
        x = x0 + b * 4 * xw
        d.line((x, y_of(10)), (x, y_of(2)))
    d.dashed((x0, y_of(0)), (x0 + w, y_of(0)), dash=2, gap=3)
    base = 256
    d.line((x0, base), (x0 + w, base))
    for b in (0, 8, 16):
        x = x0 + b * 4 * xw
        d.line((x, base), (x, base + 4))

    d.group()
    t, pts, chord_x = 0, [], None
    for p, dur in first + second:
        x = x0 + (t + 0.5) * xw
        if p == 'CHORD':
            chord_x = x0 + (t + 0.6) * xw
        elif p is not None:
            y = y_of(step[p])
            d.circle(x, y, 2.0)
            pts.append((x, y))
        t += dur
    cy = [y_of(1), y_of(6), y_of(11)]
    for y in cy:
        d.ellipse(chord_x, y, 3.0, 2.3)
    d.line((chord_x + 3.0, cy[2] - 1), (chord_x + 3.0, cy[2] - 20))

    d.group('mid')
    d.lines([pts[:27], pts[27:]])                       # the pitch line through each half
    lvl = {'p': 16, 'pp': 8, 'ff': 54}
    xm = x0 + 32 * xw
    d.line((x0, base - lvl['p']), (xm, base - lvl['p']), (xm, base - lvl['pp']), (chord_x - 2.5, base - lvl['pp']),
           (chord_x, base - lvl['ff']), (chord_x + 2.5, base - lvl['pp']), (x0 + w, base - lvl['pp']))

    d.group('mid')
    d.text(x0, y_of(12) - 8, 'ANDANTE · 2/4 · C MAJOR · FIRST VIOLINS', size=7, anchor='start')
    d.text(chord_x - 6, y_of(11) - 10, 'BAR 16: FF CHORD', size=7, anchor='end')
    d.text(x0 + 26 * xw, y_of(0) + 11, 'MIDDLE C', size=7)
    d.text(x0 + 16 * xw, base - lvl['p'] - 6, 'P', size=7)
    d.text(x0 + 48 * xw, base - lvl['pp'] - 6, 'PP · LOWER STRINGS PLUCKED', size=7)
    d.text(chord_x - 6, base - lvl['ff'] + 4, 'FF + TIMPANI', size=7, anchor='end')
    for b, lab in ((0, 'BAR 1'), (8, '9'), (16, '17')):
        d.text(x0 + b * 4 * xw, base + 14, lab, size=7)
    d.text(200, 292, 'HAYDN · SYMPHONY NO. 94 · LONDON, 23 MARCH 1792', size=7)
    return d


PLATES = {
    'mozart-vienna': mozart_vienna,
    'haydn-london': haydn_london,
}
