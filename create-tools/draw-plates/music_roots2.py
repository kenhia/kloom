"""Plates for Sound and Score's part roots2 (sprint 058): the blues on record and the Hot Five.
See plates_for.py."""
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


def blues_record():
    d = D()
    # The twelve-bar blues as a grid: three lines of four bars, each bar of four beats, over the
    # chords of the common form (I I I I / IV IV I I / V V I I, the tonic, subdominant and dominant
    # seventh Handy names). Each line of the AAB verse is sung over about the first two and a half
    # bars and answered by the band over the rest. The sung contours are schematic, a phrase that
    # rises to the blue third and falls to the tonic; the lyric is Handy's, from St. Louis Blues (1914).
    x0, bw, bh = 62, 76, 40
    tops = [34, 104, 174]
    chords = [['I', 'I', 'I', 'I7'], ['IV', 'IV', 'I', 'I'], ['V7', 'V7', 'I', 'I']]
    lines = ['A', 'A', 'B']
    lyric = ["I HATE TO SEE DE EVE'NIN SUN GO DOWN",
             "HATE TO SEE DE EVE'NIN SUN GO DOWN",
             "'CAUSE MY BABY, HE DONE LEF' DIS TOWN"]

    d.group('thin')
    for y in tops:
        for b in range(4):
            for beat in range(1, 4):                       # beat ticks inside each bar
                x = x0 + b * bw + beat * bw / 4
                d.line((x, y + bh - 6), (x, y + bh))
        d.line((x0, y + bh / 2), (x0 + 4 * bw, y + bh / 2))  # the singer's reference line
    d.group()
    for y in tops:
        for b in range(4):
            _box(d, x0 + b * bw, y, bw, bh)
    d.group('mid')
    for y in tops:
        # the sung phrase: bars 1 to 2.5, up to the blue third and down to the tonic
        pts = []
        for i in range(41):
            t = i / 40
            x = x0 + 4 + t * (2.5 * bw - 8)
            h = math.sin(math.pi * min(1, t * 1.6)) * (1 - 0.6 * t) * 11 + 3 * math.sin(t * 9 * math.pi) * (1 - t)
            pts.append((x, y + bh / 2 - h))
        d.line(*pts)
        # the band's answer: bars 2.5 to 4, dashed
        d.dashed((x0 + 2.5 * bw + 4, y + bh / 2 - 4), (x0 + 4 * bw - 6, y + bh / 2 - 4), dash=3, gap=3)
        _arrow(d, (x0 + 4 * bw - 16, y + bh / 2 - 4), (x0 + 4 * bw - 6, y + bh / 2 - 4), 4)
    d.group('mid')
    for r, y in enumerate(tops):
        d.text(x0 - 14, y + bh / 2 + 3, lines[r], size=9)
        for b in range(4):
            d.text(x0 + b * bw + 5, y + bh - 8, chords[r][b], size=7, anchor='start')
        d.text(x0, y + bh + 13, lyric[r], size=7, anchor='start')
        d.text(x0 + 3 * bw + 5, y + 10, 'ANSWER', size=7, anchor='start')
    d.text(x0 + 4, tops[0] - 5, 'SUNG', size=7, anchor='start')
    d.text(200, 266, 'TWELVE BARS · THREE LINES, AAB · CHORDS I, IV, V', size=7)
    d.text(200, 282, "LYRIC: W. C. HANDY, ST. LOUIS BLUES, 1914", size=7)
    return d


def hot_five():
    d = D()
    # "West End Blues" (Okeh 8597, Chicago, June 28, 1928) as a score of who plays when, from the
    # bar-by-bar analysis in Pearson's anthology notes: a free cadenza (bars 1-6), five twelve-bar
    # choruses, a coda. A solo is drawn as a band, an accompanying part as a line, silence as
    # nothing. The bars are the transcription's, numbered at each section's start.
    x0, x1, nbar = 76, 384, 68
    sx = (x1 - x0) / nbar
    X = lambda b: x0 + b * sx
    lanes = ['TRUMPET', 'CLARINET', 'TROMBONE', 'VOICE', 'PIANO', 'BANJO, DRUMS']
    ly = {n: 62 + i * 28 for i, n in enumerate(lanes)}
    bounds = [0, 6, 18, 30, 42, 54, 62, 68]
    names = ['CAD.', '1', '2', '3', '4', '5', 'CODA']
    # (lane, from bar, to bar, solo?)
    parts = [
        ('TRUMPET', 0, 6, True), ('TRUMPET', 6, 18, True), ('TRUMPET', 54, 62, True), ('TRUMPET', 64, 68, False),
        ('CLARINET', 6, 18, False), ('CLARINET', 30, 42, True), ('CLARINET', 54, 62, False), ('CLARINET', 66, 68, False),
        ('TROMBONE', 6, 18, False), ('TROMBONE', 18, 30, True), ('TROMBONE', 54, 62, False), ('TROMBONE', 66, 68, False),
        ('VOICE', 30, 42, True),
        ('PIANO', 6, 42, False), ('PIANO', 42, 54, True), ('PIANO', 54, 62, False), ('PIANO', 62, 68, True),
        ('BANJO, DRUMS', 6, 42, False), ('BANJO, DRUMS', 54, 62, False), ('BANJO, DRUMS', 66, 68, False),
    ]

    d.group('thin')
    for b in bounds:
        d.line((X(b), 40), (X(b), 222))
    for n in lanes:
        d.line((x0, ly[n]), (x1, ly[n]))
    d.line((x0, 232), (x1, 232))
    for b in range(nbar + 1):
        d.line((X(b), 232), (X(b), 234 if b not in bounds else 237))
    d.group()
    for n, a, b, solo in parts:
        if solo:
            _box(d, X(a) + 1, ly[n] - 4, X(b) - X(a) - 2, 8)
    # the held high B-flat, bars 55 to 58, lifted above the trumpet's band
    d.line((X(54) + 1, ly['TRUMPET'] - 11), (X(58), ly['TRUMPET'] - 11))
    d.group('mid')
    for n, a, b, solo in parts:
        if not solo:
            d.line((X(a) + 1, ly[n]), (X(b) - 1, ly[n]))
    d.line((X(54) + 1, ly['TRUMPET'] - 11), (X(54) + 1, ly['TRUMPET'] - 4))
    d.circle(X(68) - 1, ly['BANJO, DRUMS'] - 9, 2.5)                       # the closing cymbal click
    d.group('mid')
    for n in lanes:
        d.text(x0 - 6, ly[n] + 3, n, size=7, anchor='end')
    for a, b, nm in zip(bounds, bounds[1:], names):
        d.text((X(a) + X(b)) / 2, 36, nm, size=7)
    for b in bounds:
        d.text(X(b), 246, str(b + 1) if b < 68 else '68', size=7)
    d.text(X(54) - 3, ly['TRUMPET'] - 9, 'HELD B♭', size=7, anchor='end')
    d.text(200, 270, 'WEST END BLUES · OKEH 8597 · CHICAGO, JUNE 28, 1928', size=7)
    d.text(200, 284, 'SOLO: BAND · ACCOMPANYING: LINE · BARS', size=7)
    return d


PLATES = {
    'blues-record': blues_record,
    'hot-five': hot_five,
}
