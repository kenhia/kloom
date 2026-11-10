"""Plates for Sound and Score's part classic3 (sprint 058): Bayreuth and the New World. See plates_for.py."""
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


def bayreuth():
    d = D()
    # Above, the auditorium in plan: rows as arcs about one center, cut to a wedge, with no side
    # boxes, the stage beyond the pit. Below, the house in long section: the raked floor rising
    # away from the stage, the pit stepped down in six levels under the stage's lip, and two hoods
    # over it, so that every sight line from the seats passes over the orchestra to the stage.
    # Proportions are schematic: the auditorium is drawn about 35 m deep (THEATRON), at 6 px a m;
    # the pit's depth and the hoods' curves are not from a measured drawing.

    # ---- plan (top) ----
    cx, cy = 300, 66
    half = math.radians(21)
    radii = [44 + i * 7.6 for i in range(17)]

    def pol(r, a):
        return (cx - r * math.cos(a), cy + r * math.sin(a))

    d.group('thin')
    for a in (-half, half):
        d.line(pol(24, a), pol(radii[-1] + 6, a))
    d.line((cx, cy - 46), (cx, cy + 46))                              # the stage line
    d.group()
    for r in radii:
        pts = [pol(r, -half + 2 * half * i / 16) for i in range(17)]
        d.line(*pts)
    for s in (-1, 1):                                                 # six receding side walls
        for k in range(6):
            a = pol(62 + k * 20, s * half)
            d.line(a, (a[0], a[1] + s * 7))
    _box(d, cx + 8, cy - 32, 82, 64)                                   # the stage
    d.group('mid')
    d.arc(cx, cy, 30, 180 - 21, 180 + 21)                              # the pit's curve
    d.arc(cx, cy, 16, 180 - 26, 180 + 26)

    # ---- long section (bottom) ----
    floor0, floorx0 = (232, 236), 232                                  # front of the stalls
    back = (36, 176)
    stage_y, lip_x = 222, 300
    rows = 30
    d.group('thin')
    d.line((20, 272), (390, 272))                                      # datum
    for x in (lip_x - 8, lip_x + 8):                                   # the double proscenium
        d.line((x, stage_y), (x, 136))
    d.group()
    pts = []
    for i in range(rows + 1):                                          # the raked floor, in steps
        t = i / rows
        x = floor0[0] + (back[0] - floor0[0]) * t
        y = floor0[1] + (back[1] - floor0[1]) * t
        pts.append((x, y))
    step = []
    for i in range(rows):
        step += [pts[i], (pts[i + 1][0], pts[i][1])]
    step.append(pts[-1])
    d.line(*step)
    d.line(back, (back[0], 150), (back[0] + 26, 150))                  # back wall and gallery
    d.line((floor0[0], floor0[1]), (floor0[0], 230), (240, 230))       # the front parapet
    # the hood over the pit's front, curling toward the stage
    hood = [(240 + 22 * t, 230 - 7 * math.sin(math.pi * t * 0.8)) for t in [i / 12 for i in range(13)]]
    d.line(*hood)
    # the pit: six levels stepping down under the stage
    px, py = 244, 240
    pit = [(px, 230), (px, py)]
    for k in range(6):
        x1 = px + 12 + k * 9
        y1 = py + 4 + k * 4.2
        pit += [(x1, pit[-1][1]), (x1, y1)]
    pit += [(lip_x + 36, pit[-1][1]), (lip_x + 36, stage_y + 6)]
    d.line(*pit)
    d.line((lip_x - 22, stage_y), (390, stage_y))                      # stage floor
    lip = [(lip_x - 22 + 10 * t, stage_y - 6 * math.sin(math.pi * t)) for t in [i / 8 for i in range(9)]]
    d.line(*lip)                                                       # the stage-side hood
    d.line((lip_x + 36, stage_y + 6), (390, stage_y + 6))
    d.group('mid')
    for k in range(6):                                                 # players on the steps
        x = px + 6 + k * 9
        y = py + k * 4.2
        d.circle(x + 3, y - 3, 1.6)
    eye = []
    for i in (2, 14, 28):
        x, y = pts[i]
        eye.append((x - 3, y - 8))
    target = (lip_x + 24, stage_y - 2)
    for e in eye:
        d.dashed(e, target, dash=3, gap=3)
    for e in eye:
        d.circle(e[0], e[1], 1.4)
    _arrow(d, (268, 238), (268, 222), 4)                               # sound rises between the hoods
    d.line((268, 252), (268, 238))

    d.group('mid')
    d.text(cx + 49, cy + 46, 'PLAN · NO BOXES', size=7)
    d.text(cx + 49, cy + 3, 'STAGE', size=7)
    d.text(96, 214, 'RAKED STALLS', size=7)
    d.text(388, 140, 'DOUBLE', size=7, anchor='end')
    d.text(388, 149, 'PROSCENIUM', size=7, anchor='end')
    d.text(366, 242, 'PIT IN', size=7)
    d.text(366, 251, 'SIX STEPS', size=7)
    d.text(214, 216, 'HOOD', size=7)
    d.text(150, 254, 'SIGHT LINES CLEAR THE PIT', size=7)
    d.text(200, 288, 'BAYREUTH FESTSPIELHAUS, 1876 · SCHEMATIC', size=7)
    return d


# Dvořák, Largo, bars 7-10: the cor anglais theme in concert pitch, D-flat major, from the 1903
# Eulenburg score (pp. 55-56). Each note: (semitones above D-flat, beats).
LARGO = [
    (4, .75), (7, .25), (7, 1), (4, .75), (2, .25), (0, 1),           # bar 7
    (2, .75), (4, .25), (7, .75), (4, .25), (2, 2),                   # bar 8
    (4, .75), (7, .25), (7, 1), (4, .75), (2, .25), (0, 1),           # bar 9
    (2, .5), (4, .5), (2, .75), (0, .25), (0, 2),                      # bar 10
]


def new_world():
    d = D()
    # Above, one octave of a keyboard from C, with the D-flat pentatonic scale's five keys ringed
    # (D-flat, E-flat, F, A-flat, B-flat) and the two the scale leaves out crossed (G-flat, the
    # fourth, and C, the seventh). Below, the Largo's theme as a pitch line against time: a line
    # for each note's length, on rules at the scale's pitches; it never touches the fourth or
    # seventh, and uses four of the five notes.
    kx, ky, kw, kh = 82, 22, 30, 74
    whites = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    blacks = {0: 'C#', 1: 'D#', 3: 'F#', 4: 'G#', 5: 'A#'}            # after white index
    pent_white = {'F'}
    pent_black = {0, 1, 4, 5}                                          # D-flat, E-flat, A-flat, B-flat
    d.group('thin')
    d.line((kx - 10, ky + kh + 10), (kx + 7 * kw + 10, ky + kh + 10))
    d.group()
    for i in range(7):
        _box(d, kx + i * kw, ky, kw, kh)
    for i in blacks:
        _box(d, kx + (i + 1) * kw - 9, ky, 18, kh * 0.6)
    d.group('mid')
    for i, w in enumerate(whites):
        x = kx + i * kw + kw / 2
        if w in pent_white:
            d.circle(x, ky + kh - 12, 6)
        if w == 'C':
            d.line((x - 4, ky + kh - 16), (x + 4, ky + kh - 8)); d.line((x - 4, ky + kh - 8), (x + 4, ky + kh - 16))
    for i in blacks:
        x = kx + (i + 1) * kw
        if i in pent_black:
            d.circle(x, ky + kh * 0.6 - 10, 5)
        if i == 3:
            d.line((x - 4, ky + kh * 0.6 - 14), (x + 4, ky + kh * 0.6 - 6)); d.line((x - 4, ky + kh * 0.6 - 6), (x + 4, ky + kh * 0.6 - 14))

    # the pitch line
    x0, x1, base, unit = 44, 384, 248, 11                             # unit: px a semitone
    beats = sum(b for _, b in LARGO)
    bx = (x1 - x0) / beats
    d.group('thin')
    for s in (0, 2, 4, 7, 9):
        d.line((x0, base - s * unit), (x1, base - s * unit))
    for bar in range(5):
        x = x0 + bar * 4 * bx
        d.line((x, base + 8), (x, base - 9 * unit - 6))
    d.group()
    t = 0
    prev = None
    for s, b in LARGO:
        xa, xb = x0 + t * bx, x0 + (t + b) * bx
        y = base - s * unit
        if prev is not None:
            d.line((xa, prev), (xa, y))
        d.line((xa, y), (xb - 1.2, y))
        prev = y
        t += b
    d.group('mid')
    t = 0
    for s, b in LARGO:
        d.circle(x0 + t * bx, base - s * unit, 1.8)
        t += b
    d.group('mid')
    for s, n in ((0, 'D♭'), (2, 'E♭'), (4, 'F'), (7, 'A♭'), (9, 'B♭')):
        d.text(x0 - 6, base - s * unit + 2.5, n, size=7, anchor='end')
    for bar in range(4):
        d.text(x0 + (bar * 4 + 2) * bx, base + 16, str(7 + bar), size=7)
    d.text(kx + 3.5 * kw, 14, 'ONE OCTAVE: THE D♭ PENTATONIC RINGED', size=7)
    d.text(kx + 7 * kw + 14, ky + 30, 'G♭, C', size=7, anchor='start')
    d.text(kx + 7 * kw + 14, ky + 40, 'LEFT OUT', size=7, anchor='start')
    d.text(200, 288, 'LARGO, BARS 7-10 · COR ANGLAIS · CONCERT PITCH', size=7)
    return d


PLATES = {
    'bayreuth': bayreuth,
    'new-world': new_world,
}
