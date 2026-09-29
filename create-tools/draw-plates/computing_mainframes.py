"""computing plates, segment "Transistors and mainframes": fortran, time-sharing, ibm-360, minicomputer (sprint 015). See computing.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _edge(d, a, b, ra, rb, off=0.0):
    """A line from circle a to circle b (centres, radii), clipped to both rims, shifted `off` sideways."""
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy * off, ux * off
    d.line((x0 + ux * ra + nx, y0 + uy * ra + ny), (x1 - ux * rb + nx, y1 - uy * rb + ny))


def fortran():
    """Backus's first example, ROOT = (-(B/2.0)+SQRTF((B/2.0)**2-A*C))/A, as the compiler saw it:
    a graph in which B/2.0 is one node used twice, and the square is B/2.0 times itself."""
    d = D()
    r = 11
    N = {  # node: (x, level, label)
        'div': (170, 0, '/'), 'plus': (115, 1, '+'), 'A1': (235, 1, 'A'),
        'neg': (55, 2, '−'), 'sqrt': (170, 2, '√'), 'sub': (170, 3, '−'),
        'sq': (110, 4, '×'), 'ac': (235, 4, '×'), 't': (70, 5, '/'),
        'A2': (210, 5, 'A'), 'C': (262, 5, 'C'), 'B': (40, 6, 'B'), 'two': (100, 6, '2.0'),
    }
    y0, dy = 34, 38
    P = {k: (x + 50, y0 + dy * lv) for k, (x, lv, _) in N.items()}
    leaves = {'A1', 'A2', 'C', 'B', 'two'}
    # construction: the seven levels of the expression, and the store into ROOT
    d.group('thin')
    d.lines([[(62, y0 + dy * lv), (340, y0 + dy * lv)] for lv in range(7)])
    d.lines([[(P['div'][0], 8), (P['div'][0], P['div'][1] - r)]])
    # the edges, parent to child; the square takes its shared operand twice
    d.group('mid')
    for a, b in [('div', 'plus'), ('div', 'A1'), ('plus', 'neg'), ('plus', 'sqrt'), ('sqrt', 'sub'),
                 ('sub', 'sq'), ('sub', 'ac'), ('neg', 't'), ('ac', 'A2'), ('ac', 'C'),
                 ('t', 'B'), ('t', 'two')]:
        _edge(d, P[a], P[b], r, r)
    _edge(d, P['sq'], P['t'], r, r + 3, off=-3)
    _edge(d, P['sq'], P['t'], r, r + 3, off=3)
    # the nodes: operators as circles, variables and constants as boxes
    d.group()
    for k, (x, y) in P.items():
        if k in leaves:
            w = 13 if k == 'two' else 10
            d.line((x - w, y - 9), (x + w, y - 9), (x + w, y + 9), (x - w, y + 9), closed=True)
        else:
            d.circle(x, y, r)
    # the shared node, ringed, and the note that it is computed once
    d.group()
    d.circle(P['t'][0], P['t'][1], r + 3)
    # labels
    d.group()
    for k, (x, y) in P.items():
        d.text(x, y + 3, N[k][2], size=8 if k != 'two' else 7)
    d.text(P['div'][0] + 8, 12, 'ROOT', size=8, anchor='start')
    d.text(P['t'][0] + r + 8, P['t'][1] + 3, 'ONCE', size=7, anchor='start')
    d.text(P['sq'][0] + r + 5, P['sq'][1] + 9, 'SQUARED', size=7, anchor='start')
    d.text(200, 292, 'ROOT = (-(B/2.0)+SQRTF((B/2.0)**2-A*C))/A', size=8)
    return d


def time_sharing():
    """Corbató's 1962 scheduler: round-robin quanta among three consoles and a background job,
    and the multi-level queue in which a program still running at level ℓ gets 2^ℓ quanta, then drops a level."""
    d = D()
    x0, u = 44, 10  # the time axis and one quantum
    n = 33
    rows = [52, 68, 84, 100]  # three consoles and the background
    # round robin: consoles take turns while they are busy; the background runs when all three are thinking
    slots, turn = [], 0
    for t in range(n):
        ready = [k for k, (a, b) in enumerate([(0, 18), (0, 9), (0, 18)]) if a <= t < b or 22 <= t < 27 and k != 1]
        if ready:
            slots.append(ready[turn % len(ready)])
            turn += 1
        else:
            slots.append(3)
    levels = [150, 172, 194, 216, 238]
    # construction: the quantum ticks, the rows, the queue levels
    d.group('thin')
    d.lines([[(x0 + u * i, 40), (x0 + u * i, 110)] for i in range(n + 1)])
    d.lines([[(x0, y), (x0 + u * n, y)] for y in rows])
    d.lines([[(x0, y), (x0 + u * n, y)] for y in levels])
    d.lines([[(x0 + u * i, 140), (x0 + u * i, 248)] for i in (0, 1, 3, 7, 15, 31)])
    # the axes
    d.group('mid')
    d.line((x0, 112), (x0 + u * n + 6, 112))
    _arrow(d, x0 + u * n + 6, 112, 0)
    d.line((x0, 254), (x0 + u * n + 6, 254))
    _arrow(d, x0 + u * n + 6, 254, 0)
    # round robin: one bar a quantum long in the row that owns it
    d.group()
    for i, k in enumerate(slots):
        y = rows[k]
        d.line((x0 + u * i + 1, y - 4), (x0 + u * (i + 1) - 1, y - 4), (x0 + u * (i + 1) - 1, y + 4),
               (x0 + u * i + 1, y + 4), closed=True)
    # the multi-level queue: one long program runs 1, 2, 4, 8, 16 quanta, dropping a level each time
    d.group()
    start = 0
    for lv, y in enumerate(levels):
        q = 2 ** lv
        xa, xb = x0 + u * start + 1, x0 + u * (start + q) - 1
        d.line((xa, y - 5), (xb, y - 5), (xb, y + 5), (xa, y + 5), closed=True)
        if lv < len(levels) - 1:
            d.line((xb, y + 5), (xb, levels[lv + 1] - 7))
            _arrow(d, xb, levels[lv + 1] - 7, math.pi / 2, 3)
        start += q
    # labels
    d.group()
    for y, s in zip(rows, ('1', '2', '3', 'BG')):
        d.text(x0 - 6, y + 3, s, size=7, anchor='end')
    for lv, y in enumerate(levels):
        d.text(x0 - 6, y + 3, f'ℓ{lv}', size=7, anchor='end')
    d.text(200, 28, 'THREE CONSOLES AND A BACKGROUND JOB', size=8)
    d.text(x0 + u * n, 124, 'QUANTA', size=7, anchor='end')
    d.text(x0 + u * n, 266, 'q = 16 ms', size=7, anchor='end')
    d.text(200, 138, 'A LONG RUN SINKS: 2^ℓ QUANTA AT LEVEL ℓ', size=8)
    d.text(200, 286, 'CTSS · IBM 7090 · MIT 1961–62', size=8)
    return d


def ibm_360():
    """One architecture over six models (Amdahl, Blaauw and Brooks 1964, fig. 1): the programmer's
    registers are the same in all; the data path is 8, 8, 32, 64, 64 and 64 bits wide, one stroke a byte;
    five models are controlled by a read-only store of microcode, the Model 70 by wired logic."""
    d = D()
    models = [('30', 8, 'ros'), ('40', 8, 'ros'), ('50', 32, 'ros'), ('60', 64, 'ros'), ('62', 64, 'ros'),
              ('70', 64, 'wired')]
    xs = [48 + 61 * i for i in range(6)]
    top, arch_y0, arch_y1 = 22, 34, 96
    # the architecture: sixteen 32-bit general registers and four 64-bit floating-point registers
    gx0, gy0, gw, gh = 70, 42, 80, 2.5
    fx0, fy0, fw, fh = 248, 42, 80, 10
    # construction: the fan from the one architecture to each model, and the model centre lines
    d.group('thin')
    d.lines([[(200, arch_y1), (x, 136)] for x in xs])
    d.lines([[(x, 136), (x, 272)] for x in xs])
    d.lines([[(20, 150), (380, 150)], [(20, 222), (380, 222)]])
    # the architecture block
    d.group()
    d.line((30, arch_y0), (370, arch_y0), (370, arch_y1), (30, arch_y1), closed=True)
    d.group('mid')
    d.lines([[(gx0, gy0 + gh * i), (gx0 + gw, gy0 + gh * i)] for i in range(17)])
    d.lines([[(gx0, gy0), (gx0, gy0 + gh * 16)], [(gx0 + gw, gy0), (gx0 + gw, gy0 + gh * 16)]])
    d.lines([[(fx0, fy0 + fh * i), (fx0 + fw, fy0 + fh * i)] for i in range(5)])
    d.lines([[(fx0 + fw * j / 8, fy0), (fx0 + fw * j / 8, fy0 + fh * 4)] for j in range(9)])
    # the models: a data path as one stroke per byte, and the control store beneath it
    d.group()
    for x, (name, bits, ctl) in zip(xs, models):
        nb = bits // 8
        w = 3 * nb
        d.lines([[(x - w / 2 + 3 * i + 1.5, 156), (x - w / 2 + 3 * i + 1.5, 212)] for i in range(nb)])
        d.line((x - 22, 228), (x + 22, 228), (x + 22, 262), (x - 22, 262), closed=True)
    d.group('mid')
    for x, (name, bits, ctl) in zip(xs, models):
        if ctl == 'ros':
            d.lines([[(x - 16 + 4 * i, 233), (x - 16 + 4 * i, 257)] for i in range(9)])
            d.lines([[(x - 18, 233 + 4 * j), (x + 18, 233 + 4 * j)] for j in range(7)])
        else:  # wired logic: gates drawn as a small tree
            for gx, gy in ((x - 10, 240), (x + 4, 240), (x - 3, 252)):
                d.line((gx - 5, gy - 4), (gx, gy - 4))
                d.arc(gx, gy, 4, -90, 90, n=12)
                d.line((gx, gy + 4), (gx - 5, gy + 4), closed=False)
                d.line((gx - 5, gy - 4), (gx - 5, gy + 4))
    # labels
    d.group()
    d.text(200, top, 'ONE ARCHITECTURE', size=9)
    d.text(gx0 + gw / 2, 91, '16 × 32 GENERAL', size=7)
    d.text(fx0 + fw / 2, 91, '4 × 64 FLOATING', size=7)
    for x, (name, bits, ctl) in zip(xs, models):
        d.text(x, 146, name, size=9)
        d.text(x, 219, f'{bits}', size=7)
        d.text(x, 275, 'ROS' if ctl == 'ros' else 'WIRED', size=7)
    d.text(200, 292, 'DATA PATH, BITS · CONTROL', size=7)
    return d


def minicomputer():
    """The PDP-8's memory-reference instruction: a 3-bit opcode, an indirect bit, a page bit and a
    7-bit address; and its 4,096 words of core as 32 pages of 128, the address reaching page 0 or
    the page the instruction sits in."""
    d = D()
    bx0, by, bw, bh = 40, 36, 26, 26
    bits = '001011010101'  # an example, TAD on the current page: opcode 1, I 0, Z 1, address 1010101
    fields = [(0, 3, 'OPCODE'), (3, 4, 'I'), (4, 5, 'Z'), (5, 12, 'ADDRESS')]
    # the core: 32 pages of 128 words, four rows of eight
    mx0, my0, pw, ph = 40, 150, 40, 26
    cur = 13  # the page the instruction sits in (an example)
    def page_xy(p):
        return mx0 + pw * (p % 8), my0 + ph * (p // 8)
    # construction: bit boundaries carried down, octal digit groups, the page grid's extent
    d.group('thin')
    d.lines([[(bx0 + bw * i, by - 8), (bx0 + bw * i, by + bh + 8)] for i in range(13)])
    d.lines([[(bx0 + bw * i, by + bh + 8), (bx0 + bw * i, by + bh + 22)] for i in (0, 3, 6, 9, 12)])
    d.lines([[(mx0 - 8, my0 + ph * j), (mx0 + pw * 8 + 8, my0 + ph * j)] for j in range(5)])
    # the instruction word
    d.group()
    d.line((bx0, by), (bx0 + bw * 12, by), (bx0 + bw * 12, by + bh), (bx0, by + bh), closed=True)
    d.lines([[(bx0 + bw * i, by), (bx0 + bw * i, by + bh)] for i in (3, 4, 5)])
    d.group('mid')
    d.lines([[(bx0 + bw * i, by + 4), (bx0 + bw * i, by + bh - 4)] for i in range(1, 12) if i not in (3, 4, 5)])
    # the field braces
    for a, b, _ in fields:
        xa, xb = bx0 + bw * a + 3, bx0 + bw * b - 3
        d.line((xa, by + bh + 6), (xa, by + bh + 10), (xb, by + bh + 10), (xb, by + bh + 6))
    # the memory: 32 pages
    d.group()
    d.line((mx0, my0), (mx0 + pw * 8, my0), (mx0 + pw * 8, my0 + ph * 4), (mx0, my0 + ph * 4), closed=True)
    d.lines([[(mx0 + pw * i, my0), (mx0 + pw * i, my0 + ph * 4)] for i in range(1, 8)])
    d.lines([[(mx0, my0 + ph * j), (mx0 + pw * 8, my0 + ph * j)] for j in range(1, 4)])
    # page 0 and the current page, hatched; the reach of the address field into each
    d.group('mid')
    for p in (0, cur):
        x, y = page_xy(p)
        d.lines([[(x + 4 + 6 * k, y + 3), (x + 4 + 6 * k, y + ph - 3)] for k in range(6)])
    zx = bx0 + bw * 4.5
    ax = bx0 + bw * 8.5
    x0p, y0p = page_xy(0)
    xc, yc = page_xy(cur)
    d.line((zx, by + bh + 12), (zx, 120), (x0p + pw / 2, 120), (x0p + pw / 2, y0p - 3))
    _arrow(d, x0p + pw / 2, y0p - 3, math.pi / 2)
    d.line((ax, by + bh + 12), (ax, 128), (xc + pw / 2, 128), (xc + pw / 2, yc - 3))
    _arrow(d, xc + pw / 2, yc - 3, math.pi / 2)
    # labels
    d.group()
    for i, ch in enumerate(bits):
        d.text(bx0 + bw * i + bw / 2, by + bh / 2 + 3, ch, size=9)
    for i in (0, 11):
        d.text(bx0 + bw * i + bw / 2, by - 12, str(i), size=7)
    for a, b, name in fields:
        d.text(bx0 + bw * (a + b) / 2, by + bh + 32, name, size=7)
    d.text(200, 20, '12-BIT WORD · ONE INSTRUCTION', size=8)
    d.text(x0p + pw / 2, my0 + ph * 4 + 14, 'PAGE 0', size=7)
    d.text(xc + pw / 2, my0 + ph * 4 + 14, 'THIS PAGE', size=7)
    d.text(200, 288, '4,096 WORDS = 32 PAGES × 128', size=8)
    return d


PLATES = {
    'fortran': fortran,
    'time-sharing': time_sharing,
    'ibm-360': ibm_360,
    'minicomputer': minicomputer,
}
