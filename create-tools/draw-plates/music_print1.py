"""Plates for Sound and Score's part print1 (sprint 058): Petrucci's printed music and Josquin.
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


# The opening of Josquin's Ave Maria ... virgo serena, superius, as white mensural notes on a staff
# with a soprano C clef (C on the bottom line): G, C (a breve), C, D, E, C (a breve). Staff steps
# above the bottom line: C4 = 0, E4 = 2, G4 = 4, B4 = 6, D5 = 8; so G4 = 4, C5 = 7, D5 = 8, E5 = 9.
# Pitches and values from the Josquin Research Project's encoding of the New Josquin Edition (Jos2306).
_AVE = [(4, 'sb', 'A-'), (7, 'b', 've'), (7, 'sb', 'Ma-'), (8, 'sb', 'ri-'), (9, 'sb', ''), (7, 'b', 'a')]
_GAP = 3.2          # half the distance between staff lines
_DX = 21            # spacing of notes along the staff


def _staff(d, x, y, w):
    """Five lines, bottom line at y."""
    d.lines([[(x, y - 2 * _GAP * k), (x + w, y - 2 * _GAP * k)] for k in range(5)])


def _notes(d, x, y):
    """The clef and the notes, for a staff whose bottom line is at y, starting at x."""
    # a C clef on the bottom line: two short bars and a bracket
    d.line((x + 2, y - 2 * _GAP * 4 - 1), (x + 2, y + 1))
    d.line((x + 6, y - 3.2), (x + 2, y - 3.2), (x + 2, y + 3.2), (x + 6, y + 3.2))
    for i, (step, kind, _) in enumerate(_AVE):
        cx, cy = x + 20 + i * _DX, y - _GAP * step
        if kind == 'sb':             # semibreve: a hollow diamond
            d.line((cx - 3.4, cy), (cx, cy - 3.4), (cx + 3.4, cy), (cx, cy + 3.4), closed=True)
        else:                        # breve: a hollow square with short side strokes
            d.line((cx - 3.6, cy - 2.6), (cx + 3.6, cy - 2.6), (cx + 3.6, cy + 2.6), (cx - 3.6, cy + 2.6), closed=True)
            d.line((cx - 3.6, cy - 4.2), (cx - 3.6, cy + 4.2))
            d.line((cx + 3.6, cy - 4.2), (cx + 3.6, cy + 4.2))


def _words(d, x, y):
    """The syllables, under where their notes stand."""
    for i, (_, _, syl) in enumerate(_AVE):
        if syl:
            d.text(x + 20 + i * _DX, y, syl.upper(), size=7)


def _cross(d, x, y, r=4):
    d.line((x - r, y), (x + r, y)); d.line((x, y - r), (x, y + r)); d.circle(x, y, r * 0.55)


def petrucci():
    d = D()
    # Left: the three impressions as three layers of one sheet, each pass drawn on its own strip and
    # offset a little to the right, as a pass out of register would land. Right: the three registered.
    # Each strip carries the sheet's registration crosses; the dashed lines are where they must meet.
    W, H = 150, 60                       # a strip: the sheet as the plate shows it
    lx, rx = 22, 232                     # left column, right column
    tops = [28, 110, 192]                # the strips' tops
    offs = [0, 7, 14]                    # how far out of register each pass is drawn
    base = 46                            # staff bottom line within a strip

    d.group('thin')
    for k, (t, o) in enumerate(zip(tops, offs)):
        _box(d, lx + o, t, W, H)
    _box(d, rx, 110, W, H)
    # where the crosses must land: the registered sheet's corners, carried left
    for xx in (lx + 7, lx + W - 7):
        d.dashed((xx, 14), (xx, tops[-1] + H + 6), dash=3, gap=3)
    for t, o in zip(tops, offs):
        d.line((lx + W + o + 6, t + H / 2), (rx - 10, 110 + H / 2))

    d.group()
    _staff(d, lx + offs[0] + 12, tops[0] + base, W - 24)          # pass 1, staves
    _staff(d, rx + 12, 110 + base, W - 24)                        # registered: staves
    _notes(d, rx + 12, 110 + base)                                # registered: notes

    d.group('mid')
    _notes(d, lx + offs[1] + 12, tops[1] + base)                  # pass 2, notes alone
    for t, o in zip(tops, offs):
        _cross(d, lx + o + 7, t + 7); _cross(d, lx + o + W - 7, t + 7)
    _cross(d, rx + 7, 117); _cross(d, rx + W - 7, 117)
    for t, o in zip(tops, offs):
        _arrow(d, (lx + W + o + 6, t + H / 2), (rx - 10, 110 + H / 2), 4)

    d.group('mid')
    _words(d, lx + offs[2] + 12, tops[2] + base + 11)             # pass 3, words alone
    _words(d, rx + 12, 110 + base + 11)                           # registered: words
    d.text(lx + 14, 20, '1 STAVES', size=7, anchor='start')
    d.text(lx + 14 + offs[1], tops[1] - 6, '2 NOTES', size=7, anchor='start')
    d.text(lx + 14 + offs[2], tops[2] - 6, '3 WORDS', size=7, anchor='start')
    d.text(rx + W / 2, 100, 'REGISTERED', size=7)
    d.text(rx + W / 2, 186, 'ONE SHEET · THREE PASSES', size=7)
    d.text(200, 284, 'TRIPLE IMPRESSION · VENICE 1501 · AFTER BOORMAN', size=7)
    return d


# The first eleven bars of Ave Maria ... virgo serena, all four voices, as (start, length, MIDI pitch),
# times in semibreves (a bar of the edition is a breve, two semibreves). From the Josquin Research
# Project's encoding of the New Josquin Edition (Jos2306). 'Ave Maria' is each voice's first six notes.
_VOICES = [
    ('S', [(0, 1, 67), (1, 2, 72), (3, 1, 72), (4, 1, 74), (5, 1, 76), (6, 2, 72),
           (14, 1.5, 72), (15.5, .5, 71), (16, 1, 69), (17, 1, 67), (18, .5, 69), (18.5, .5, 67),
           (19, 1.5, 72), (20.5, .25, 71), (20.75, .25, 69), (21, 1, 71)]),
    ('A', [(4, 1, 55), (5, 2, 60), (7, 1, 60), (8, 1, 62), (9, 1, 64), (10, 2, 60),
           (18, 1.5, 60), (19.5, .5, 59), (20, 1, 57), (21, 1, 55)]),
    ('T', [(8, 1, 55), (9, 2, 60), (11, 1, 60), (12, 1, 62), (13, 1, 64), (14, 2, 60)]),
    ('B', [(12, 1, 43), (13, 2, 48), (15, 1, 48), (16, 1, 50), (17, 1, 52), (18, 2, 48)]),
]


def josquin():
    d = D()
    # Four lanes, soprano at the top, on one time axis: each voice's notes as a pitch line, drawn
    # within its own lane (2.6 px a semitone above the lane's G). The motif enters every two bars.
    x0, sx = 44, 15.2                    # 22 semibreves across
    lane_h, top = 56, 30
    T = 22
    def X(t):
        return x0 + t * sx
    lane_y = [top + (i + 1) * lane_h - 12 for i in range(4)]      # each lane's G line
    gs = [67, 55, 55, 43]                                          # each voice's G

    d.group('thin')
    for b in range(0, T + 1, 2):                                   # barlines, a breve apart
        d.line((X(b), top + 2), (X(b), top + 4 * lane_h + 2))
    for y in lane_y:
        d.line((X(0), y), (X(T), y))
    entries = [(X(4 * i), lane_y[i]) for i in range(4)]
    d.dashed(*entries, dash=3, gap=3)

    for i, (name, notes) in enumerate(_VOICES):
        g = gs[i]
        def Y(m):
            return lane_y[i] - (m - g) * 2.6
        motif, rest = notes[:6], notes[6:]
        for grp, seq in (('main', motif), ('mid', rest)):
            if not seq:
                continue
            d.group(grp)
            segs, cur = [], []
            for (t, L, m) in seq:
                if cur and abs(cur[-1][0] - X(t)) > 0.5:          # a rest: break the line
                    segs.append(cur); cur = []
                if cur:
                    cur.append((X(t), Y(m)))
                cur += [(X(t), Y(m)), (X(t + L), Y(m))]
            segs.append(cur)
            d.lines([[p for k, p in enumerate(s) if k == 0 or p != s[k - 1]] for s in segs])

    d.group('mid')
    for (x, y) in entries:
        d.circle(x, y, 2.2)

    d.group('mid')
    for i, (name, _) in enumerate(_VOICES):
        d.text(x0 - 12, lane_y[i] + 3, name, size=7)
    labels = ['G4', 'G3', 'G3', 'G2']
    for i, (x, y) in enumerate(entries):
        d.text(x, y + 11, labels[i], size=7)
    for b in range(1, 12, 2):
        d.text(X(2 * (b - 1)) + sx, top - 4, str(b), size=7)
    d.text(X(0) + 4 * sx, lane_y[0] - 26, 'AVE MARIA', size=7)
    d.text(X(17), lane_y[0] - 26, 'GRATIA PLENA', size=7)
    d.text(200, 290, 'AVE MARIA … VIRGO SERENA · BARS 1-11 · FOUR ENTRIES', size=7)
    return d


PLATES = {'petrucci': petrucci, 'josquin': josquin}
