"""computing plates, segment "The electronic machine", first four frames (sprint 015). See computing.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _flow(d, *pts, size=4):
    """A polyline with an arrowhead at its last point."""
    d.line(*pts)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    _arrow(d, x1, y1, math.atan2(y1 - y0, x1 - x0), size)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def colossus():
    """Tutte's 1+2 break as Colossus ran it: the looped cipher tape read by photocells, the chi-1 and chi-2
    wheels as thyratron rings of 41 and 31 stages, each stream differenced, combined, and counted."""
    d = D()
    # the tape: five data channels and the sprocket row between channels 2 and 3, as on teleprinter tape
    tx0, tx1, ty = 22, 250, 30
    rows = [ty + 8 * k for k in range(6)]  # channels 1, 2, sprocket, 3, 4, 5
    ch_y = {1: rows[0], 2: rows[1], 3: rows[3], 4: rows[4], 5: rows[5]}
    pitch = 9.5
    cols = [tx0 + 10 + pitch * i for i in range(int((tx1 - tx0 - 14) / pitch))]
    # a fixed pseudo-random tape (a linear congruential sequence, so the plate redraws identically)
    seq, s = [], 7
    for _ in range(len(cols)):
        s = (s * 1103515245 + 12345) % 2 ** 31
        seq.append(s >> 16)
    reader_x = cols[13]
    # construction: the channel lines and the reader's optical axis
    d.group('thin')
    d.lines([[(tx0, y), (tx1, y)] for y in ch_y.values()])
    d.line((reader_x, ty - 14), (reader_x, ty + 58))
    # ring centres and their rays to the start positions
    r1c, r2c = (78, 170), (178, 170)
    d.lines([[(r1c[0] - 44, r1c[1]), (r1c[0] + 44, r1c[1])], [(r2c[0] - 36, r2c[1]), (r2c[0] + 36, r2c[1])]])
    # the tape and its holes
    d.group()
    d.line((tx0, ty - 7), (tx1, ty - 7))
    d.line((tx0, ty + 47), (tx1, ty + 47))
    d.group('mid')
    for x, v in zip(cols, seq):
        d.circle(x, rows[2], 0.9)  # sprocket hole
        for c in range(1, 6):
            if v >> c & 1:
                d.circle(x, ch_y[c], 2.1)
    # the reader: a lamp above, a photocell block below
    d.group()
    _box(d, reader_x - 7, ty - 22, 14, 10)
    _box(d, reader_x - 9, ty + 52, 18, 12)
    # the thyratron rings: chi-1 (41 stages) and chi-2 (31 stages), one stage struck at the start position
    d.group('mid')
    for (cx, cy), n, r in ((r1c, 41, 38), (r2c, 31, 30)):
        for k in range(n):
            a = -math.pi / 2 + 2 * math.pi * k / n
            d.circle(cx + r * math.cos(a), cy + r * math.sin(a), 1.6)
    d.group()
    for (cx, cy), n, r in ((r1c, 41, 38), (r2c, 31, 30)):
        d.circle(cx, cy, r + 5)
        d.circle(cx, cy, r - 5)
        a = -math.pi / 2
        d.circle(cx + r * math.cos(a), cy + r * math.sin(a), 3.4)
    # the data path: tape channels 1 and 2 and the two rings into the delta circuits, the combining gate,
    # the counter and the typewriter
    d.group('mid')
    dx = 272
    ys = {'Z1': 64, 'Z2': 90, 'C1': 150, 'C2': 190}
    for y in ys.values():
        _box(d, dx, y - 8, 22, 16)
    _flow(d, (reader_x + 9, ty + 58), (reader_x + 40, ty + 58), (reader_x + 40, 64), (dx, 64))
    _flow(d, (reader_x + 9, ty + 62), (reader_x + 32, ty + 62), (reader_x + 32, 90), (dx, 90))
    _flow(d, (r1c[0], r1c[1] - 43), (r1c[0], 122), (230, 122), (230, 150), (dx, 150))
    _flow(d, (r2c[0] + 35, r2c[1] + 20), (240, 190), (dx, 190))
    gx, gy = 318, 128
    d.circle(gx + 12, gy, 12)
    d.line((gx, gy), (gx + 24, gy))
    d.line((gx + 12, gy - 12), (gx + 12, gy + 12))
    for y in ys.values():
        _flow(d, (dx + 22, y), (dx + 30, y), (gx + 3, gy + (y - gy) * 0.18))
    _box(d, 312, 176, 36, 22)
    _flow(d, (gx + 12, gy + 12), (gx + 12, 176))
    _box(d, 312, 222, 36, 18)
    _flow(d, (330, 198), (330, 222))
    # labels
    d.group()
    d.text(reader_x, ty - 26, 'LAMP', size=6)
    d.text(reader_x, ty + 74, 'PHOTOCELLS', size=6)
    d.text(tx0 - 2, ch_y[1] + 2, '1', size=6, anchor='end')
    d.text(tx0 - 2, ch_y[5] + 2, '5', size=6, anchor='end')
    d.text(tx1 + 4, ty + 22, 'Z', size=8, anchor='start')
    for k, y in ys.items():
        d.text(dx + 11, y + 3, 'Δ', size=8)
    d.text(dx - 4, 60, 'Z1', size=6, anchor='end')
    d.text(dx - 4, 86, 'Z2', size=6, anchor='end')
    d.text(r1c[0], r1c[1] + 3, 'χ1 · 41', size=8)
    d.text(r2c[0], r2c[1] + 3, 'χ2 · 31', size=8)
    d.text(330, 190, 'COUNT', size=7)
    d.text(330, 234, 'PRINT', size=7)
    d.text(306, 213, 'IF ≥ SET TOTAL', size=6, anchor='end')
    d.text(200, 264, 'ΔZ1 ⊕ ΔZ2 ⊕ Δχ1 ⊕ Δχ2 = • · COUNTED OVER THE WHOLE TAPE', size=7)
    d.text(200, 278, '41 × 31 = 1,271 START POSITIONS TO TRY', size=7)
    return d


def harvard_mark_i():
    """The control tape: 24 hole positions a line, three groups of eight (out, in, operation), and the two lines
    of coding the manual gives for adding and subtracting counter 3 into counter 71."""
    d = D()
    pitch = 7.2
    x0 = 44
    gap = 7
    xs = []
    for g in range(3):
        for h in range(8):
            xs.append(x0 + g * (8 * pitch + gap) + h * pitch)
    tape_l, tape_r = x0 - 12, xs[-1] + 12
    y0, dy = 70, 17
    lines = 10
    ys = [y0 + dy * k for k in range(lines)]
    # the codes are hole numbers within each group; group order on the tape: A (out), B (in), C (misc.)
    coded = {3: ('21', '7321', '7'), 6: ('21', '7321', '732')}

    def holes(code):
        return {int(c) for c in code}

    # construction: the hole columns and the line pitch
    d.group('thin')
    d.lines([[(x, y0 - 22), (x, ys[-1] + 12)] for x in xs])
    d.lines([[(tape_l - 8, y), (tape_r + 8, y)] for y in (ys[3], ys[6])])
    # the tape, running past the sensing pins
    d.group()
    d.line((tape_l, y0 - 26), (tape_l, ys[-1] + 16))
    d.line((tape_r, y0 - 26), (tape_r, ys[-1] + 16))
    # sprocket holes, between groups: the drum's teeth drive the tape a line at a time
    d.group('mid')
    for gx in (xs[7] + (xs[8] - xs[7]) / 2, xs[15] + (xs[16] - xs[15]) / 2):
        for y in ys:
            d.circle(gx, y, 1.2)
    # the unpunched positions of every line, as faint rings; then the punched ones
    for k, y in enumerate(ys):
        punched = set()
        if k in coded:
            for g, code in enumerate(coded[k]):
                for h in holes(code):
                    punched.add(g * 8 + (h - 1))
        for i, x in enumerate(xs):
            if i not in punched:
                d.circle(x, y, 0.6)
    d.group()
    for k, codes in coded.items():
        for g, code in enumerate(codes):
            for h in holes(code):
                d.circle(xs[g * 8 + h - 1], ys[k], 2.6)
    # the bus: counter 3's out-relay and counter 71's in-relay, as in the manual's figure 1
    d.group('mid')
    bx = 262
    d.line((bx, 58), (bx, 226))
    for (y, name) in ((96, '3'), (178, '71')):
        _box(d, 300, y - 14, 60, 28)
        d.line((bx, y), (286, y))
        d.line((286, y), (292, y - 6))
        d.line((294, y), (300, y))
    _flow(d, (bx + 10, 110), (bx + 10, 164))
    # the line being read: the sensing crosshead
    d.group()
    d.line((tape_l - 6, ys[3] - 6), (tape_r + 6, ys[3] - 6))
    d.line((tape_l - 6, ys[3] + 6), (tape_r + 6, ys[3] + 6))
    # labels
    d.group()
    for g, name in enumerate(('A · OUT', 'B · IN', 'C · MISC.')):
        d.text((xs[g * 8] + xs[g * 8 + 7]) / 2, y0 - 32, name, size=7)
        for h in (1, 8):
            d.text(xs[g * 8 + h - 1], y0 - 12, str(h), size=5)
    d.text(tape_r + 12, ys[3] + 3, 'ADD', size=7, anchor='start')
    d.text(tape_r + 12, ys[6] + 3, 'SUB', size=7, anchor='start')
    d.text(330, 99, 'CTR 3', size=8)
    d.text(330, 181, 'CTR 71', size=8)
    d.text(bx, 50, 'BUS', size=7)
    d.text(200, 262, '21 · 7321 · 7  ADD CTR 3 INTO CTR 71', size=7)
    d.text(200, 276, '21 · 7321 · 732  THE SAME, THROUGH THE INVERT RELAY', size=7)
    return d


def eniac():
    """A decade ring counter of an ENIAC accumulator: ten flip-flop stages in a ring, standing at 5, taking
    seven digit pulses and passing 9 to 0, which sends one carry to the next decade; and the pulses on a
    200-microsecond addition time of twenty 10-microsecond pulse times."""
    d = D()
    cx, cy, R = 104, 118, 62
    start, add = 5, 7
    ang = lambda k: -math.pi / 2 + 2 * math.pi * k / 10
    pos = lambda k, r=R: (cx + r * math.cos(ang(k)), cy + r * math.sin(ang(k)))
    # construction: the ring's centre lines and the rays to the stages
    d.group('thin')
    d.circle(cx, cy, R)
    d.lines([[(cx, cy), pos(k, R + 20)] for k in range(10)])
    # the stages: each a flip-flop, drawn as a pair of triodes (two small circles) on a board
    d.group()
    for k in range(10):
        x, y = pos(k)
        a = ang(k) + math.pi / 2
        ux, uy = math.cos(a), math.sin(a)
        d.circle(x - 5 * ux, y - 5 * uy, 4)
        d.circle(x + 5 * ux, y + 5 * uy, 4)
    # the steps the pulses take round the ring: 5 → 6 → … → 9 → 0 → 1 → 2
    d.group('mid')
    for j in range(add):
        a0 = ang(start + j) + 0.16
        a1 = ang(start + j + 1) - 0.16
        pts = [(cx + (R - 18) * math.cos(a0 + (a1 - a0) * i / 12), cy + (R - 18) * math.sin(a0 + (a1 - a0) * i / 12))
               for i in range(13)]
        _flow(d, *pts, size=3)
    # the stage that holds the digit before and after: the neon lamp that shows it
    d.group()
    for k in (start, (start + add) % 10):
        x, y = pos(k, R + 13)
        d.circle(x, y, 3)
    # the carry: from the 9-to-0 passage to the next decade's input
    nx = 250
    _flow(d, pos(0, R + 8), (cx, 34), (nx, 34), (nx, 58))
    _box(d, nx - 28, 58, 56, 34)
    d.group('mid')
    for k in range(10):
        a = -math.pi / 2 + 2 * math.pi * k / 10
        d.circle(nx + 12 * math.cos(a) - 0, 75 + 12 * math.sin(a), 1.4)
    # the timing: twenty 10-microsecond pulse times make one 200-microsecond addition time
    d.group('thin')
    tx0, tx1, ty = 30, 370, 250
    step = (tx1 - tx0) / 20
    d.lines([[(tx0 + step * i, ty - 34), (tx0 + step * i, ty + 6)] for i in range(21)])
    d.group()
    d.line((tx0, ty), (tx1, ty))
    pulses = []
    for i in range(20):
        x = tx0 + step * (i + 0.5)
        if i < add:
            pulses.append([(x - 3, ty), (x - 3, ty - 14), (x + 3, ty - 14), (x + 3, ty)])
    d.lines(pulses)
    xc = tx0 + step * (11.5)
    d.line((xc - 3, ty), (xc - 3, ty - 24), (xc + 3, ty - 24), (xc + 3, ty))
    # labels
    d.group()
    for k in range(10):
        x, y = pos(k, R + 28)
        d.text(x, y + 3, str(k), size=8)
    d.text(cx, cy - 2, '5 + 7', size=9)
    d.text(cx, cy + 11, '= 2, CARRY 1', size=7)
    d.text(nx, 108, 'NEXT DECADE', size=7)
    d.text(180, 28, 'CARRY', size=7)
    d.text(tx0 + step * 3.5, ty - 20, '7 DIGIT PULSES', size=7)
    d.text(xc, ty - 28, 'CARRY', size=7)
    d.text(200, ty + 18, '20 PULSE TIMES × 10 μs = ONE ADDITION TIME, 200 μs', size=7)
    d.text(200, ty + 32, '5,000 ADDITIONS A SECOND', size=7)
    return d


def edvac_report():
    """The First Draft's organs (CA, CC, M, I, O and the outside medium R) and its memory: a delay line dl
    with its amplifier A and its switching and gating station SG, holding 32 minor cycles of 32 units."""
    d = D()
    # the organs, laid out as the report describes: every transfer from R goes through I into M, and out through O
    B = {'R': (20, 34, 56, 34), 'I': (104, 18, 44, 26), 'O': (104, 58, 44, 26),
         'M': (196, 22, 70, 58), 'CA': (316, 18, 60, 30), 'CC': (316, 58, 60, 30)}
    mid = lambda k: (B[k][0] + B[k][2] / 2, B[k][1] + B[k][3] / 2)
    # construction: the report's grid, M at the centre
    d.group('thin')
    d.line((20, 100), (380, 100))
    d.line((231, 10), (231, 110))
    d.group()
    for k in B:
        _box(d, *B[k])
    d.group('mid')
    _flow(d, (76, 44), (104, 31))
    _flow(d, (148, 31), (196, 38))
    _flow(d, (196, 64), (148, 71))
    _flow(d, (104, 71), (76, 58))
    _flow(d, (266, 36), (316, 33))
    _flow(d, (316, 40), (266, 44))
    _flow(d, (266, 66), (316, 73))
    _flow(d, (346, 58), (346, 48))
    # the delay line: a tank, the pulses in it (one minor cycle of 32 units drawn), the amplifier and SG
    lx0, lx1, ly = 60, 300, 172
    d.group('thin')
    d.line((lx0 - 20, ly), (lx1 + 60, ly))
    d.group()
    d.line((lx0, ly - 16), (lx1, ly - 16))
    d.line((lx0, ly + 16), (lx1, ly + 16))
    d.line((lx0, ly - 16), (lx0, ly + 16))
    d.line((lx1, ly - 16), (lx1, ly + 16))
    d.group('mid')
    # 32 minor cycles along the line, each marked; within one of them, 32 unit pulses
    n = 32
    w = (lx1 - lx0) / n
    d.lines([[(lx0 + w * i, ly - 16), (lx0 + w * i, ly - 11)] for i in range(1, n)])
    bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]
    zx0, zx1, zy = 60, 300, 228
    uw = (zx1 - zx0) / 32
    segs = []
    for i, b in enumerate(bits):
        x = zx0 + uw * i
        if b:
            segs.append([(x + 1.5, zy), (x + 1.5, zy - 10), (x + uw - 1.5, zy - 10), (x + uw - 1.5, zy)])
    d.lines(segs)
    d.line((zx0, zy), (zx1, zy))
    # the enlargement: one minor cycle of the line, opened out below
    d.group('thin')
    d.line((lx0 + w * 9, ly + 16), (zx0, zy - 14))
    d.line((lx0 + w * 10, ly + 16), (zx1, zy - 14))
    # the feedback: out of the line, through A and SG, back into its input
    d.group()
    _box(d, 314, 160, 22, 24)
    _box(d, 346, 160, 26, 24)
    _flow(d, (lx1, ly), (314, ly))
    _flow(d, (336, ly), (346, ly))
    _flow(d, (372, ly), (382, ly), (382, 132), (40, 132), (40, ly), (lx0, ly))
    _flow(d, (359, 132), (359, 112), size=3)
    # labels
    d.group()
    for k in B:
        x, y = mid(k)
        d.text(x, y + 3, k, size=9)
    d.text(lx0 + (lx1 - lx0) / 2, ly + 3, 'dl · 1,024 UNITS = 32 MINOR CYCLES', size=7)
    d.text(325, ly + 3, 'A', size=8)
    d.text(359, ly + 3, 'SG', size=8)
    d.text(zx0 - 4, zy - 2, '32', size=6, anchor='end')
    d.text(200, zy + 14, 'ONE MINOR CYCLE: 30 DIGITS, A SIGN, A NUMBER-OR-ORDER MARK', size=7)
    d.text(200, zy + 28, '256 LINES × 32 MINOR CYCLES = 8,192 WORDS', size=7)
    d.text(210, 126, 'TO CA AND CC', size=6, anchor='start')
    return d


PLATES = {'colossus': colossus, 'harvard-mark-i': harvard_mark_i, 'eniac': eniac, 'edvac-report': edvac_report}
