"""computing plates, trail "The personal computer" (sprint 015). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _rect(d, x0, y0, x1, y1):
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)


def _bezier(p0, p1, p2, p3, n=24):
    """Points along a cubic Bézier curve."""
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def _inside(poly, x, y):
    """Even-odd point-in-polygon test."""
    c = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            c = not c
    return c


def xerox_alto():
    """The Alto's display: a bitmap of 30,704 words in the 64K-word memory, clocked out through a
    16-bit shift register to a portrait screen of 606 × 808 dots, with overlapping windows and a mouse."""
    d = D()
    mx0, mx1, my0, my1 = 22, 56, 36, 256          # memory column: 65,536 words
    words = 65536
    per = (my1 - my0) / words
    b0 = my0 + 0x2000 * per                        # the bitmap placed from word 8K (any even address will do)
    b1 = b0 + 30704 * per
    sx0, sy0, sw, sh = 226, 40, 150, 200           # the screen, 606 : 808 = 0.75
    rx0, ry, cell = 78, 140, 8                     # the 16-bit shift register
    # construction: 4K-word ticks, projections of the bitmap onto the screen, scan lines
    d.group('thin')
    d.lines([[(mx0 - 4, my0 + k * 4096 * per), (mx0, my0 + k * 4096 * per)] for k in range(17)])
    d.lines([[(mx1, b0), (sx0, sy0)], [(mx1, b1), (sx0, sy0 + sh)]])
    d.lines([[(sx0, sy0 + k * 10), (sx0 + sw, sy0 + k * 10)] for k in range(1, 20)])
    # the memory, the register and the screen
    d.group()
    _rect(d, mx0, my0, mx1, my1)
    _rect(d, rx0, ry, rx0 + 16 * cell, ry + cell)
    _rect(d, sx0, sy0, sx0 + sw, sy0 + sh)
    _rect(d, sx0 - 6, sy0 - 6, sx0 + sw + 6, sy0 + sh + 6)
    # the bitmap region, hatched, and the register's cells with a word's bits
    d.group('mid')
    _rect(d, mx0, b0, mx1, b1)
    d.lines([[(mx0, y), (mx1, y - 6)] for y in [b0 + 6 + 6 * k for k in range(int((b1 - b0 - 6) / 6))]])
    d.lines([[(rx0 + k * cell, ry), (rx0 + k * cell, ry + cell)] for k in range(1, 16)])
    word = 0b1011001110001101
    for k in range(16):
        if word >> (15 - k) & 1:
            d.circle(rx0 + k * cell + cell / 2, ry + cell / 2, 1.6)
    # the data path: memory to register to screen, one scan line at a time
    d.group()
    ym = (b0 + b1) / 2
    d.line((mx1, ym), (rx0 - 4, ym), (rx0 - 4, ry + cell / 2), (rx0, ry + cell / 2))
    _arrow(d, rx0, ry + cell / 2, 0)
    scan = sy0 + 90
    d.line((rx0 + 16 * cell, ry + cell / 2), (214, ry + cell / 2), (214, scan), (sx0, scan))
    _arrow(d, sx0, scan, 0)
    # on the screen: two overlapping windows, text in the front one, the cursor
    d.group('mid')
    bx0, by0, bx1, by1 = sx0 + 14, sy0 + 20, sx0 + 104, sy0 + 110
    fx0, fy0, fx1, fy1 = sx0 + 50, sy0 + 64, sx0 + 138, sy0 + 176
    d.line((bx0, by1), (bx0, by0), (bx1, by0), (bx1, fy0))
    d.line((bx0, by1), (fx0, by1))
    d.line((bx0, by0 + 9), (bx1, by0 + 9))
    _rect(d, fx0, fy0, fx1, fy1)
    d.line((fx0, fy0 + 9), (fx1, fy0 + 9))
    d.lines([[(fx0 + 6, fy0 + 18 + 8 * k), (fx0 + 6 + (70 if k % 4 != 3 else 38), fy0 + 18 + 8 * k)] for k in range(11)])
    d.lines([[(bx0 + 6, by0 + 18 + 8 * k), (fx0 - 4, by0 + 18 + 8 * k)] for k in range(9)])
    cx, cy = sx0 + 118, sy0 + 44
    d.line((cx, cy), (cx, cy + 13), (cx + 3.5, cy + 10), (cx + 6, cy + 15), (cx + 8, cy + 14), (cx + 5.5, cy + 9),
           (cx + 10, cy + 9), closed=True)
    # the mouse: three bar buttons, top to bottom, and its cable
    d.group()
    mox, moy = 104, 196
    _rect(d, mox, moy, mox + 44, moy + 56)
    for k in range(3):
        _rect(d, mox + 30, moy + 8 + 12 * k, mox + 40, moy + 16 + 12 * k)
    d.curve(f'M{mox} {moy + 20} C{mox - 20} {moy + 20} {mx1 + 20} {my1 - 20} {mx1} {my1 - 20}')
    # labels
    d.group()
    d.text((mx0 + mx1) / 2, my0 - 8, '64K', size=8)
    d.text((mx0 + mx1) / 2, my1 + 14, 'WORDS', size=7)
    d.text(mx1 + 6, b0 - 4, 'BITMAP', size=7, anchor='start')
    d.text(rx0 + 64, ry - 22, '30,704 WORDS', size=8)
    d.text(rx0 + 64, ry - 10, '38 A LINE × 808', size=7)
    d.text(rx0 + 64, ry + 22, '16-BIT SHIFT REGISTER', size=7)
    d.text(sx0 + sw / 2, sy0 + sh + 20, '606 × 808 DOTS · PORTRAIT', size=8)
    d.text(mox + 22, moy + 70, 'MOUSE', size=7)
    return d


def apple_ii():
    """Wozniak's shared timing, over two CPU cycles: one 14.318 MHz oscillator divided by 14 for the 6502
    (video owns memory in one half of each cycle, the processor in the other), by 4 for the 3.58 MHz colour
    subcarrier; hi-res dots come two to a colour cycle, and which ones are lit sets the hue."""
    d = D()
    x0, x1 = 84, 378
    ticks = 28
    p = (x1 - x0) / ticks
    rows = {'osc': 58, 'phi': 104, 'sub': 156, 'even': 210, 'odd': 250}
    h = 9
    # construction: a line at every oscillator tick, heavier at the CPU cycle boundaries
    d.group('thin')
    d.lines([[(x0 + k * p, 40), (x0 + k * p, 268)] for k in range(ticks + 1)])
    d.lines([[(x0 - 6, y), (x1 + 4, y)] for y in (rows['sub'],)])
    d.group('mid')
    d.lines([[(x0 + k * 14 * p, 34), (x0 + k * 14 * p, 272)] for k in range(3)])
    # the oscillator: 28 periods
    d.group()
    pts = []
    for k in range(ticks):
        xa = x0 + k * p
        pts += [(xa, rows['osc'] + h), (xa, rows['osc'] - h), (xa + p / 2, rows['osc'] - h), (xa + p / 2, rows['osc'] + h)]
    pts.append((x1, rows['osc'] + h))
    d.line(*pts)
    # the CPU clock: high while video reads memory, low while the 6502 does
    pts = []
    for k in range(2):
        xa = x0 + k * 14 * p
        pts += [(xa, rows['phi'] + h), (xa, rows['phi'] - h), (xa + 7 * p, rows['phi'] - h), (xa + 7 * p, rows['phi'] + h)]
    pts.append((x1, rows['phi'] + h))
    d.line(*pts)
    # the colour subcarrier: a sine of period 4 ticks, 7 cycles
    n = 280
    d.line(*[(x0 + (x1 - x0) * i / n, rows['sub'] - h * math.sin(2 * math.pi * (i / n) * 7)) for i in range(n + 1)])
    # the dots: 14 of them, two to a colour cycle; even-column dots lit, then odd
    for key, first in (('even', 0), ('odd', 1)):
        y = rows[key]
        pts = [(x0, y + h)]
        for k in range(first, 14, 2):
            xa = x0 + k * 2 * p
            pts += [(xa, y + h), (xa, y - h), (xa + 2 * p, y - h), (xa + 2 * p, y + h)]
        pts.append((x1, y + h))
        d.line(*pts)
    # labels
    d.group()
    d.text(x0 - 8, rows['osc'] + 3, '14.318', size=8, anchor='end')
    d.text(x0 - 8, rows['osc'] + 13, 'MHz', size=7, anchor='end')
    d.text(x0 - 8, rows['phi'] + 3, 'φ 1.023', size=8, anchor='end')
    d.text(x0 - 8, rows['phi'] + 13, 'MHz ÷14', size=7, anchor='end')
    d.text(x0 - 8, rows['sub'] + 3, '3.58 MHz', size=8, anchor='end')
    d.text(x0 - 8, rows['sub'] + 13, 'COLOUR ÷4', size=7, anchor='end')
    d.text(x0 - 8, rows['even'] + 3, 'EVEN DOTS', size=8, anchor='end')
    d.text(x0 - 8, rows['even'] + 13, 'VIOLET', size=7, anchor='end')
    d.text(x0 - 8, rows['odd'] + 3, 'ODD DOTS', size=8, anchor='end')
    d.text(x0 - 8, rows['odd'] + 13, 'GREEN', size=7, anchor='end')
    for k in range(2):
        xa = x0 + k * 14 * p
        d.text(xa + 3.5 * p, rows['phi'] - h - 5, 'VIDEO', size=7)
        d.text(xa + 10.5 * p, rows['phi'] - h - 5, '6502', size=7)
    d.text((x0 + x1) / 2, 26, 'TWO CPU CYCLES · 28 TICKS · 7 COLOUR CYCLES · 14 DOTS', size=7)
    d.text((x0 + x1) / 2, 290, 'ONE CLOCK FOR PROCESSOR, MEMORY, REFRESH AND COLOUR', size=7)
    return d


def visicalc():
    """A small sheet (the frame's invented example), its formulas' dependencies drawn as arrows, and
    VisiCalc's recalculation order, row by row: B1 reads B4 and B5 before they are recomputed."""
    d = D()
    x0, y0, rh = 44, 58, 26
    cw = [74, 64, 74, 74]
    xs = [x0]
    for w in cw:
        xs.append(xs[-1] + w)
    nrows = 7
    ys = [y0 + k * rh for k in range(nrows + 1)]
    cy = lambda r: (ys[r - 1] + ys[r]) / 2           # centre of row r (1-based)
    bx = (xs[1] + xs[2]) / 2
    # construction: the grid, and the order of recalculation sweeping row by row
    d.group('thin')
    d.lines([[(x, y0 - 16), (x, ys[-1])] for x in xs])
    d.lines([[(x0 - 18, y), (xs[-1], y)] for y in ys])
    order = []
    for r in range(1, 6):
        order += [(x0 + 8, cy(r) + 7), (xs[-1] - 8, cy(r) + 7)]
    d.line(*order)
    # the sheet's frame and its borders
    d.group()
    _rect(d, x0 - 18, y0 - 16, xs[-1], ys[-1])
    d.line((x0 - 18, y0), (xs[-1], y0))
    d.line((x0, y0 - 16), (x0, ys[-1]))
    # the cells' contents: labels in A, numbers in B, as strokes of their width
    d.group('mid')
    widths_a = [34, 30, 30, 30, 30]
    widths_b = [30, 18, 26, 36, 36]
    d.lines([[(xs[0] + 8, cy(r) - 2), (xs[0] + 8 + widths_a[r - 1], cy(r) - 2)] for r in range(1, 6)])
    d.lines([[(xs[2] - 8 - widths_b[r - 1], cy(r) - 2), (xs[2] - 8, cy(r) - 2)] for r in range(1, 6)])
    _rect(d, xs[1] + 2, ys[0] + 2, xs[2] - 2, ys[1] - 2)            # the cursor on B1
    # dependencies: each formula cell's inputs, as arrows drawn to the right of column B
    d.group()

    def dep(r_from, r_to, bulge):
        xa, ya, yb = xs[2] + 2, cy(r_from), cy(r_to)
        xm = xa + bulge
        d.curve(f'M{xa:.1f} {ya:.1f} C{xm:.1f} {ya:.1f} {xm:.1f} {yb:.1f} {xa + 4:.1f} {yb:.1f}')
        _arrow(d, xa + 4, yb, math.pi)

    dep(2, 4, 16)   # UNITS → SALES
    dep(3, 4, 9)    # PRICE → SALES
    dep(2, 5, 28)   # UNITS → COSTS
    dep(4, 1, 44)   # SALES → PROFIT, a reference forward
    dep(5, 1, 58)   # COSTS → PROFIT
    # labels
    d.group()
    for i, c in enumerate('ABCD'):
        d.text((xs[i] + xs[i + 1]) / 2, y0 - 5, c, size=8)
    for r in range(1, nrows + 1):
        d.text(x0 - 9, cy(r) + 3, str(r), size=8)
    d.text(xs[3] + 6, cy(1) + 3, 'B1 = B4 − B5', size=7, anchor='start')
    d.text(xs[3] + 6, cy(4) + 3, 'B4 = B2 × B3', size=7, anchor='start')
    d.text(xs[3] + 6, cy(5) + 3, 'B5 = 200 + 1.25 × B2', size=7, anchor='start')
    d.text(200, 268, 'RECALCULATED ROW BY ROW · B1 COMES FIRST', size=8)
    d.text(200, 282, 'SO IT READS B4 AND B5 BEFORE THEY CHANGE', size=7)
    return d


def ibm_pc():
    """The 8088's 20-bit address: a 16-bit segment shifted four bits left, plus a 16-bit offset. The
    reset address FFFF:0000 is FFFF0, 16 bytes below the top of the PC's 1 MB map, in the BIOS ROM."""
    d = D()
    bw = 18                                     # a hex digit's box
    lx = 40
    rows = {'seg': 70, 'off': 104, 'sum': 146}
    # the memory map: 1 MB, 16 blocks of 64 KB
    mx0, mx1, mtop, mbot = 300, 340, 34, 274
    blk = (mbot - mtop) / 16
    yaddr = lambda a: mbot - (mbot - mtop) * a / 0x100000
    d.group('thin')
    d.lines([[(mx0 - 5, mbot - k * blk), (mx0, mbot - k * blk)] for k in range(17)])
    d.lines([[(lx + k * bw, rows['seg'] - 14), (lx + k * bw, rows['sum'] + 10)] for k in range(6)])
    # the DIP package of the 8088: 40 pins
    px0, py0, pw, ph = 52, 196, 118, 30
    d.lines([[(px0 + 6 + k * 5.6, py0), (px0 + 6 + k * 5.6, py0 - 5)] for k in range(20)] +
            [[(px0 + 6 + k * 5.6, py0 + ph), (px0 + 6 + k * 5.6, py0 + ph + 5)] for k in range(20)])
    d.group()
    _rect(d, mx0, mtop, mx1, mbot)
    _rect(d, px0, py0, px0 + pw, py0 + ph)
    d.arc(px0, py0 + ph / 2, 5, -90, 90)
    # the three rows of digit boxes: segment (shifted left one digit), offset, sum
    for key, start, n in (('seg', 0, 4), ('off', 1, 4), ('sum', 0, 5)):
        for k in range(n):
            _rect(d, lx + (start + k) * bw, rows[key] - 11, lx + (start + k + 1) * bw, rows[key] + 7)
    d.line((lx - 8, rows['sum'] - 20), (lx + 5 * bw + 8, rows['sum'] - 20))
    d.group('mid')
    _rect(d, lx + 4 * bw, rows['seg'] - 11, lx + 5 * bw, rows['seg'] + 7)   # the appended zero
    # the map's regions
    for a in (0xA0000, 0xC0000, 0xF0000):
        d.line((mx0, yaddr(a)), (mx1, yaddr(a)))
    d.lines([[(mx0, yaddr(a)), (mx0 + 8, yaddr(a) - 8)] for a in range(0xF0000 + 0x2000, 0x100000, 0x2000)])
    # the sum's path to the map: FFFF0, the reset address
    d.group()
    ya = yaddr(0xFFFF0)
    xa = lx + 5 * bw + 4
    d.line((xa, rows['sum'] - 2), (262, rows['sum'] - 2), (262, ya), (mx0 - 2, ya))
    _arrow(d, mx0 - 2, ya, 0)
    # labels
    d.group()
    for key, start, digits in (('seg', 0, 'FFFF'), ('off', 1, '0000'), ('sum', 0, 'FFFF0')):
        for k, ch in enumerate(digits):
            d.text(lx + (start + k + 0.5) * bw, rows[key] + 1, ch, size=9)
    d.text(lx + 4.5 * bw, rows['seg'] + 1, '0', size=9)
    d.text(lx + 0.5 * bw, rows['off'] + 1, '+', size=9)
    d.text(lx, rows['seg'] - 18, 'SEGMENT × 16', size=7, anchor='start')
    d.text(lx + 5 * bw + 8, rows['off'] + 1, 'OFFSET', size=7, anchor='start')
    d.text(lx, rows['sum'] + 22, '20-BIT ADDRESS', size=7, anchor='start')
    d.text(px0 + pw / 2, py0 + ph / 2 + 3, '8088', size=9)
    d.text(px0 + pw / 2, py0 + ph + 20, '40 PINS · 20 ADDRESS LINES', size=7)
    d.text(mx1 + 6, (yaddr(0) + yaddr(0xA0000)) / 2, '640 KB', size=8, anchor='start')
    d.text(mx1 + 6, (yaddr(0) + yaddr(0xA0000)) / 2 + 11, 'RAM', size=7, anchor='start')
    d.text(mx1 + 6, (yaddr(0xA0000) + yaddr(0xC0000)) / 2 + 3, 'VIDEO', size=7, anchor='start')
    d.text(mx1 + 6, (yaddr(0xF0000) + yaddr(0x100000)) / 2 + 3, 'BIOS', size=7, anchor='start')
    d.text((mx0 + mx1) / 2, mtop - 6, 'FFFFF', size=7)
    d.text(mx0 - 8, mbot + 3, '00000', size=7, anchor='end')
    d.text(mx0 - 8, yaddr(0xA0000) + 3, 'A0000', size=7, anchor='end')
    d.text(258, ya + 3, 'RESET', size=7, anchor='end')
    d.text((mx0 + mx1) / 2, mbot + 16, '1 MB', size=8)
    return d


def macintosh():
    """One glyph, a D drawn with cubic Béziers as PostScript draws type, filled twice: on the Mac's
    72-dpi screen, a dot lit where its centre falls inside; and at the LaserWriter's 300 dpi, as spans."""
    d = D()
    H = 176
    base = 238

    def glyph(ox):
        """The outer contour and the counter, in drawing units, with their control points."""
        P = lambda u, v: (ox + H * u, base - H * v)
        outer = [P(0, 0), P(0, 1), P(0.36, 1)]
        c1 = (P(0.36, 1), P(0.78, 1), P(0.86, 0.76), P(0.86, 0.5))
        c2 = (P(0.86, 0.5), P(0.86, 0.24), P(0.78, 0), P(0.36, 0))
        outer += _bezier(*c1)[1:] + _bezier(*c2)[1:]
        inner = [P(0.19, 0.15), P(0.36, 0.15)]
        c3 = (P(0.36, 0.15), P(0.62, 0.15), P(0.67, 0.3), P(0.67, 0.5))
        c4 = (P(0.67, 0.5), P(0.67, 0.7), P(0.62, 0.85), P(0.36, 0.85))
        inner += _bezier(*c3)[1:] + _bezier(*c4)[1:] + [P(0.19, 0.85)]
        return outer, inner, (c1, c2, c3, c4)

    lo, ro = 26, 214
    coarse = H / 10                          # the glyph is ten screen dots tall
    fine = coarse * 72 / 300                 # the same length at 300 dpi
    L_out, L_in, L_ctrl = glyph(lo)
    R_out, R_in, _ = glyph(ro)
    # construction: the 72-dpi grid, and the Bézier control polygons
    d.group('thin')
    top = base - H - coarse
    d.lines([[(lo - coarse + k * coarse, top), (lo - coarse + k * coarse, base + coarse)] for k in range(12)])
    d.lines([[(lo - coarse, top + k * coarse), (lo + 10 * coarse, top + k * coarse)] for k in range(13)])
    for c in L_ctrl:
        d.line(*c)
        for q in c[1:3]:
            d.circle(q[0], q[1], 1.6)
    # the lit dots at 72 dpi: a cell is black when its centre is inside the outline
    d.group('mid')
    for i in range(-1, 11):
        for j in range(-1, 11):
            x, y = lo + (i + 0.5) * coarse, base - (j + 0.5) * coarse
            if _inside(L_out, x, y) and not _inside(L_in, x, y):
                xa, ya = lo + i * coarse, base - (j + 1) * coarse
                _rect(d, xa + 1.5, ya + 1.5, xa + coarse - 1.5, ya + coarse - 1.5)
    # the 300-dpi fill, as horizontal spans at each row's centre
    spans = []
    rowsn = int(H / fine) + 1
    for j in range(rowsn):
        y = base - (j + 0.5) * fine
        run = None
        for i in range(-1, int(0.9 * H / fine) + 2):
            x = ro + (i + 0.5) * fine
            on = _inside(R_out, x, y) and not _inside(R_in, x, y)
            if on and run is None:
                run = ro + i * fine
            if not on and run is not None:
                spans.append([(run, y), (ro + i * fine, y)])
                run = None
    d.lines(spans)
    # the outlines, drawn over both
    d.group()
    for o, n in ((L_out, L_in), (R_out, R_in)):
        d.line(*o, closed=True)
        d.line(*n, closed=True)
    # labels
    d.group()
    d.text(lo + 4.5 * coarse, 28, '72 DPI · MACINTOSH SCREEN', size=7)
    d.text(ro + 0.43 * H, 28, '300 DPI · LASERWRITER', size=7)
    d.text(lo + 4.5 * coarse, base + 30, '10 DOTS TALL', size=7)
    d.text(ro + 0.43 * H, base + 30, '42 DOTS TALL', size=7)
    d.text(200, 290, 'ONE OUTLINE · FOUR CUBIC BÉZIERS · ANY RESOLUTION', size=7)
    return d


PLATES = {'xerox-alto': xerox_alto, 'apple-ii': apple_ii, 'visicalc': visicalc, 'ibm-pc': ibm_pc,
          'macintosh': macintosh}
