"""Plates for Sound and Score's part script2 (sprint 058): hildegard, notre-dame, ars-nova.
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


def hildegard():
    d = D()
    # The Riesencodex (Wiesbaden, Hs. 2), about 30 cm wide and 45 tall, at 5.4 px a cm: a music page
    # in two columns, each a run of staves over lines of text, and one staff enlarged. In the codex
    # the F line is ruled in red and the C line in a faint yellow ink (Weston 2022); the number of
    # lines, the neumes and their pitches here are schematic.
    k = 5.4
    px, py, pw, ph = 22, 24, 30 * k, 45 * k
    m = 2.6 * k                                       # margins
    colw = (pw - 2 * m - 1.2 * k) / 2
    rows = 15
    rh = (ph - 2 * m) / rows
    d.group('thin')
    for c in range(2):
        x = px + m + c * (colw + 1.2 * k)
        d.line((x, py + m), (x, py + ph - m)); d.line((x + colw, py + m), (x + colw, py + ph - m))
    d.line((px, py + ph + 10), (px + pw, py + ph + 10))
    d.line((px, py + ph + 6), (px, py + ph + 14)); d.line((px + pw, py + ph + 6), (px + pw, py + ph + 14))
    d.group()
    _box(d, px, py, pw, ph)
    d.group('mid')
    for c in range(2):
        x = px + m + c * (colw + 1.2 * k)
        for r in range(rows):
            y = py + m + r * rh
            if c == 0 and r == 0:
                _box(d, x, y + 1, rh * 0.9, rh * 0.9)            # a painted initial
                xs = x + rh
            else:
                xs = x
            for j in range(3):                                   # staff lines, tight above the text
                d.line((xs, y + 1.5 + j * 2.1), (x + colw, y + 1.5 + j * 2.1))
            d.line((x, y + rh - 2.5), (x + colw * (0.95 if r % 4 else 0.7), y + rh - 2.5))   # text
    # the enlarged staff and its lines, with a callout from the page
    ex, ey, ew = 226, 92, 124
    sp = 14
    d.group('thin')
    d.dashed((px + m + colw, py + m + rh * 3 + 3), (ex, ey + 2 * sp), dash=3, gap=3)
    d.group('mid')
    d.line((ex, ey), (ex + ew, ey)); d.line((ex, ey + sp), (ex + ew, ey + sp)); d.line((ex, ey + 3 * sp), (ex + ew, ey + 3 * sp))
    d.dashed((ex, ey - sp * 0.5), (ex + ew, ey - sp * 0.5), dash=2, gap=2)   # C line, faint yellow
    d.group()
    d.line((ex, ey + 2 * sp), (ex + ew, ey + 2 * sp))           # the F line, red in the codex
    d.group('mid')
    # schematic neumes: virga (stem and head), punctum, pes (two notes rising), climacus (falling)
    def head(x, y):
        d.line((x - 2, y), (x, y - 2), (x + 2, y), (x, y + 2), closed=True)
    steps = [3, 4, 5, 5, 6, 7, 8, 7, 6, 5, 4, 3]                 # half-spaces above the bottom line
    for i, h in enumerate(steps):
        x = ex + 8 + i * 10
        y = ey + 3 * sp - h * sp / 2
        head(x, y)
        if i % 3 == 0:
            d.line((x + 2, y), (x + 2, y - 10))
    d.line((ex, ey + 3 * sp + 26), (ex + ew * 0.8, ey + 3 * sp + 26))  # a text line under the staff
    d.group('mid')
    d.text(px + pw / 2, py + ph + 24, '30 CM', size=7)
    d.text(ex + ew + 4, ey + 2 * sp + 3, 'F LINE', size=7, anchor='start')
    d.text(ex + ew + 4, ey - sp * 0.5 + 3, 'C LINE', size=7, anchor='start')
    d.text(ex + ew / 2, ey + 3 * sp + 40, 'TEXT UNDER THE NEUMES', size=7)
    d.text(ex + ew / 2, ey - 34, 'ONE STAFF, ENLARGED', size=7)
    d.text(ex + ew / 2 + 20, 276, 'RIESENCODEX · 45 BY 30 CM · 15 KG', size=7)
    d.text(ex + ew / 2 + 20, 290, 'F RED, C YELLOW · NEUMES SCHEMATIC', size=7)
    return d


def notre_dame():
    d = D()
    # Organum in discant: the chant tenor held in long notes below, the upper voice above it in the
    # first rhythmic mode, long-short (two units, then one), three units to a perfection. Time runs
    # left to right in units; pitch up the page in diatonic steps. The pitches are schematic; the
    # rhythm, the tenor's held notes and the ligature groups (3, 2, 2, 2) are the mode's.
    x0, u = 40, 13.0                 # 24 units across
    ybase, st = 230, 9.0             # pitch steps
    def X(t):
        return x0 + t * u
    def Y(p):
        return ybase - p * st
    # duplum: mode 1, long (2) short (1), eight perfections; pitches schematic, rising and falling
    pitches = [12, 13, 14, 12, 15, 14, 13, 12, 16, 15, 14, 13, 15, 14, 12, 13]
    notes = []
    t = 0
    for i, p in enumerate(pitches):
        dur = 2 if i % 2 == 0 else 1
        notes.append((t, dur, p))
        t += dur
    tenor = [(0, 12, 3), (12, 12, 5)]                                   # two chant notes, held
    d.group('thin')
    for k in range(0, 25, 3):                                            # perfections
        d.line((X(k), Y(18) - 4), (X(k), Y(1) + 8))
    for k in range(0, 25):                                               # units
        d.line((X(k), Y(1) + 8), (X(k), Y(1) + 12))
    d.line((X(0), Y(1) + 8), (X(24), Y(1) + 8))
    d.group()
    for t0, dur, p in notes:                                             # the moving upper voice
        d.line((X(t0) + 1.5, Y(p)), (X(t0 + dur) - 1.5, Y(p)))
    for t0, dur, p in tenor:                                             # the held tenor
        _box(d, X(t0) + 1.5, Y(p) - 3, (dur * u) - 3, 6)
    d.group('mid')
    for (a, _, pa), (b, _, pb) in zip(notes, notes[1:]):                 # the line's joins
        d.line((X(b) - 1.5, Y(pa)), (X(b) + 1.5, Y(pb)))
    # ligature brackets over the duplum: 3, 2, 2, 2, 2, 2, 2, 1
    groups = [3, 2, 2, 2, 2, 2, 2, 1]
    i = 0
    for g in groups:
        a, b = notes[i], notes[i + g - 1]
        top = Y(max(n[2] for n in notes[i:i + g])) - 8
        d.line((X(a[0]) + 1.5, top + 3), (X(a[0]) + 1.5, top), (X(b[0] + b[1]) - 1.5, top), (X(b[0] + b[1]) - 1.5, top + 3))
        i += g
    d.group('mid')
    d.text(X(0), Y(18) - 12, 'DUPLUM · MODE 1: LONG-SHORT · LIGATURES 3-2-2-2', size=7, anchor='start')
    d.text(X(6), Y(3) - 8, 'TENOR · THE CHANT, HELD', size=7)
    d.text(X(18), Y(5) - 8, 'NEXT CHANT NOTE', size=7)
    d.text(X(1.5), Y(1) + 24, 'ONE PERFECTION = 3 UNITS', size=7, anchor='start')
    d.text(200, 292, 'ORGANUM IN DISCANT · PITCHES SCHEMATIC', size=7)
    return d


def ars_nova():
    d = D()
    # The four mensurations as trees: a breve divided into semibreves (tempus: three, perfect, a
    # circle; two, imperfect, a half circle), each semibreve into minims (prolatio: three, major, a
    # dot; two, minor, no dot). The minims counted under each are 9, 6, 6 and 4.
    cols = [(52, True, True), (148, True, False), (252, False, True), (348, False, False)]
    ysign, yb, ys, ym = 40, 92, 158, 222
    d.group('thin')
    d.line((20, ys), (380, ys))
    d.line((20, ym), (380, ym))
    for cx, *_ in cols:
        d.line((cx, ysign + 18), (cx, yb - 8))
    d.group()
    for cx, perf, maj in cols:                                          # the signs
        r = 13
        if perf:
            d.circle(cx, ysign, r)
        else:
            d.arc(cx, ysign, r, 40, 320)
        if maj:
            d.circle(cx, ysign, 1.6)
    d.group('mid')
    leaves = {}
    for cx, perf, maj in cols:
        nsb, nmin = (3 if perf else 2), (3 if maj else 2)
        span_sb = 27 if perf else 26
        sbx = [cx + (i - (nsb - 1) / 2) * span_sb for i in range(nsb)]
        _box(d, cx - 8, yb - 5, 16, 10)
        mins = []
        for sx in sbx:
            d.line((cx, yb + 6), (sx, ys - 7))
            pts = [(sx, ys - 6), (sx + 5, ys), (sx, ys + 6), (sx - 5, ys)]   # a lozenge semibreve
            d.line(*pts, closed=True)
            span_m = 8 if nmin == 3 else 10
            for j in range(nmin):
                mx = sx + (j - (nmin - 1) / 2) * span_m
                d.line((sx, ys + 7), (mx, ym - 6))
                mins.append(mx)
        leaves[cx] = mins
    d.group()
    for cx, mins in leaves.items():
        for mx in mins:                                                  # minims: lozenge and stem
            d.line((mx, ym - 4), (mx + 3, ym), (mx, ym + 4), (mx - 3, ym), closed=True)
            d.line((mx, ym - 4), (mx, ym - 14))
    d.group('mid')
    labels = [('PERF · MAJOR', '9'), ('PERF · MINOR', '6'), ('IMPERF · MAJOR', '6'), ('IMPERF · MINOR', '4')]
    for (cx, *_), (lab, n) in zip(cols, labels):
        d.text(cx, ym + 22, n + ' MINIMS', size=7)
        d.text(cx, ym + 34, lab, size=7)
    d.text(4, yb + 3, 'B', size=7, anchor='start')
    d.text(4, ys + 3, 'SB', size=7, anchor='start')
    d.text(4, ym + 3, 'M', size=7, anchor='start')
    d.text(200, 292, 'TEMPUS (B TO SB) · PROLATIO (SB TO M) · THE HALF CIRCLE BECAME C', size=7)
    return d


PLATES = {
    'hildegard': hildegard,
    'notre-dame': notre_dame,
    'ars-nova': ars_nova,
}
