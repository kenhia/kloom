"""Plates for Sound and Score's part roots1 (sprint 058): the Fisk Jubilee Singers and ragtime.
See plates_for.py."""
from plates import D


def _box(d, x, y, w, h, cls=None):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True, cls=cls)


def fisk_jubilee():
    d = D()
    # "Swing low, sweet chariot" as printed in Seward's Jubilee Songs (1872), p. 6: F major, 2/4,
    # the first four bars. Pitch (in semitones, MIDI numbers) against time (in beats), each voice a
    # stepped line with a tick at every attack. Bars 1-2 are the treble staff alone, soprano and
    # alto in unison (the bass staff rests); bars 3-4 are the four parts, all on an F major chord.
    # Read from the page image: unison A4 F4 A4 | F4 F4 D4 C4; then S F4x4 A4 C5 C5 | C5,
    # A F4x5 A4 A4 | A4, T A3x4 C4 C4 C4 | C4, B F3 throughout.
    x0, x1 = 66, 384
    bw = (x1 - x0) / 8                      # one beat
    p_hi, p_lo, y_hi, y_lo = 72, 53, 44, 222
    def X(b):
        return x0 + b * bw
    def Y(p):
        return y_hi + (p_hi - p) * (y_lo - y_hi) / (p_hi - p_lo)
    pitches = [(72, 'C5'), (69, 'A4'), (65, 'F4'), (62, 'D4'), (60, 'C4'), (57, 'A3'), (53, 'F3')]
    unison = [(0, .5, 69), (.5, 1.5, 65), (1.5, 2, 69), (2, 2.75, 65), (2.75, 3, 65), (3, 3.25, 62), (3.25, 4, 60)]
    sop = [(4, 4.25, 65), (4.25, 4.5, 65), (4.5, 4.75, 65), (4.75, 5, 65), (5, 5.25, 69), (5.25, 5.5, 72), (5.5, 6, 72), (6, 8, 72)]
    alt = [(4, 4.25, 65), (4.25, 4.5, 65), (4.5, 4.75, 65), (4.75, 5, 65), (5, 5.25, 65), (5.25, 5.5, 69), (5.5, 6, 69), (6, 8, 69)]
    ten = [(4, 4.25, 57), (4.25, 4.5, 57), (4.5, 4.75, 57), (4.75, 5, 57), (5, 5.25, 60), (5.25, 5.5, 60), (5.5, 6, 60), (6, 8, 60)]
    bas = [(4, 4.25, 53), (4.25, 4.5, 53), (4.5, 4.75, 53), (4.75, 5, 53), (5, 5.25, 53), (5.25, 5.5, 53), (5.5, 6, 53), (6, 8, 53)]

    def voice(notes, dy=0.0, cls=None):
        pts = []
        for (a, b, p) in notes:
            y = Y(p) + dy
            if pts and abs(pts[-1][1] - y) > 0.01:
                pts.append((X(a), y))
            elif not pts:
                pts.append((X(a), y))
            pts.append((X(b), y))
        d.line(*pts, cls=cls)

    def ticks(notes, dy=0.0):
        for (a, b, p) in notes:
            y = Y(p) + dy
            d.line((X(a), y - 3.5), (X(a), y + 3.5))

    d.group('thin')
    for p, _ in pitches:
        d.line((x0, Y(p)), (x1, Y(p)))
    for b in range(0, 9, 2):
        d.line((X(b), y_hi - 12), (X(b), y_lo + 10))
    for b in range(1, 8, 2):
        d.dashed((X(b), y_hi - 4), (X(b), y_lo + 4), dash=2, gap=3)

    d.group()
    voice(unison)
    voice(sop, -1.6)
    d.group('mid')
    voice(alt, 1.6)
    voice(ten)
    voice(bas)
    d.group('mid')
    ticks(unison)
    ticks(sop, -1.6)
    ticks(alt, 1.6)
    ticks(ten)
    ticks(bas)
    d.circle(X(.5) + bw * 0.5, Y(65) - 10, 1.3)                 # the fermata on "low"
    d.arc(X(.5) + bw * 0.5, Y(65) - 9, 5, 180, 360)

    d.group('mid')
    for p, name in pitches:
        d.text(x0 - 8, Y(p) + 2.5, name, size=7, anchor='end')
    d.text(X(2), y_hi - 18, 'SOPRANO AND ALTO IN UNISON', size=7)
    d.text(X(6), y_hi - 18, 'FOUR PARTS', size=7)
    d.text(X(8) - 2, Y(72) - 5, 'S', size=7, anchor='end')
    d.text(X(8) - 2, Y(69) + 9, 'A', size=7, anchor='end')
    d.text(X(8) - 2, Y(60) - 5, 'T', size=7, anchor='end')
    d.text(X(8) - 2, Y(53) - 5, 'B', size=7, anchor='end')
    d.text(X(2), y_lo + 22, 'SWING LOW, SWEET CHARIOT', size=7)
    d.text(X(6), y_lo + 22, 'COMING FOR TO CARRY ME HOME', size=7)
    d.text(225, 270, 'F MAJOR · 2/4 · EACH COLUMN ONE BEAT', size=7)
    d.text(225, 288, 'SEWARD, JUBILEE SONGS (1872), P. 6', size=7)
    return d


def ragtime():
    d = D()
    # Bar 1 of the Maple Leaf Rag as printed in Stark's first edition (1899): A-flat major, 2/4,
    # drawn as a piano roll would punch it. Columns are sixteenths; each note is a bar as long as
    # it sounds, at its pitch (MIDI numbers, A-flat 2 = 44 to E-flat 5 = 75). Read from the page:
    # left hand in eighths, A-flat octave, chord E-flat A-flat C twice, A-natural octave; right
    # hand rest, A-flat, E-flat octave, A-flat, C, E-flat octave (an eighth), G.
    x0, x1 = 70, 378
    cw = (x1 - x0) / 8
    p_hi, p_lo, y_hi, y_lo = 76, 43, 36, 226
    def X(s):
        return x0 + s * cw
    def Y(p):
        return y_hi + (p_hi - p) * (y_lo - y_hi) / (p_hi - p_lo)
    h = (y_lo - y_hi) / (p_hi - p_lo) * 0.9
    rh = [(1, 1, 68), (2, 1, 63), (2, 1, 75), (3, 1, 68), (4, 1, 72), (5, 2, 63), (5, 2, 75), (7, 1, 67)]
    lh = [(0, 2, 44), (0, 2, 56), (2, 2, 51), (2, 2, 56), (2, 2, 60), (4, 2, 51), (4, 2, 56), (4, 2, 60), (6, 2, 45), (6, 2, 57)]

    d.group('thin')
    for s in range(9):
        d.line((X(s), y_hi - 4), (X(s), y_lo + 4))
    for p in (44, 51, 56, 60, 63, 68, 72, 75):
        d.line((x0 - 4, Y(p)), (x0, Y(p)))

    d.group()
    d.line((X(0), y_hi - 10), (X(0), y_lo + 10))
    d.line((X(4), y_hi - 10), (X(4), y_lo + 10))
    d.line((X(8), y_hi - 10), (X(8), y_lo + 10))
    d.group()
    for (s, n, p) in lh:
        _box(d, X(s) + 2, Y(p) - h / 2, n * cw - 4, h)
    d.group()
    for (s, n, p) in rh:
        _box(d, X(s) + 2, Y(p) - h / 2, n * cw - 4, h)

    d.group('mid')
    # accents: the right hand's attacks that fall between the left hand's eighths
    for s in (1, 3, 5, 7):
        top = min(Y(p) for (ss, n, p) in rh if ss == s) - h / 2 - 4
        cx = X(s) + cw / 2
        d.line((cx - 4, top - 6), (cx + 4, top - 3), (cx - 4, top))

    d.group('mid')
    for s, c in enumerate(['1', 'E', '&', 'A', '2', 'E', '&', 'A']):
        d.text(X(s) + cw / 2, y_lo + 18, c, size=7)
    for p, name in ((75, 'E♭5'), (68, 'A♭4'), (60, 'C4'), (51, 'E♭3'), (44, 'A♭2')):
        d.text(x0 - 7, Y(p) + 2.5, name, size=7, anchor='end')
    d.text(X(8) + 6, Y(70), 'RH', size=7, anchor='start')
    d.text(X(8) + 6, Y(52), 'LH', size=7, anchor='start')
    d.text(224, 264, 'ACCENTS BETWEEN THE LEFT HAND EIGHTHS', size=7)
    d.text(224, 280, 'MAPLE LEAF RAG · BAR 1 · A♭ MAJOR · 2/4', size=7)
    d.text(224, 294, 'STARK, 1899 · EACH COLUMN A SIXTEENTH', size=7)
    return d


PLATES = {
    'fisk-jubilee': fisk_jubilee,
    'ragtime': ragtime,
}
