"""computing plates, segments "The microprocessor", "Computing everywhere" (arm, smartphone)
and the last frame of "Open questions" (sprint 015). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _box(d, x0, y0, x1, y1):
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)


def _cells(d, x0, y0, x1, y1, cols, rows):
    """The inner grid lines of a register array: `cols` × `rows` cells."""
    segs = [[(x0 + (x1 - x0) * i / cols, y0), (x0 + (x1 - x0) * i / cols, y1)] for i in range(1, cols)]
    segs += [[(x0, y0 + (y1 - y0) * j / rows), (x1, y0 + (y1 - y0) * j / rows)] for j in range(1, rows)]
    d.lines(segs)


def _alu(d, xc, ytop, w, h, notch=0.28):
    """The usual ALU symbol: a trapezoid with a notch in its wide (upper) edge, the two inputs above it."""
    n = w * notch / 2
    d.line((xc - w / 2, ytop), (xc - n, ytop), (xc, ytop + h * 0.3), (xc + n, ytop), (xc + w / 2, ytop),
           (xc + w * 0.25, ytop + h), (xc - w * 0.25, ytop + h), closed=True)


def microprocessor():
    """The 4004's data path on its one 4-bit internal bus, and the eight clock periods of an instruction cycle
    that carry a 12-bit address, an 8-bit instruction and 4-bit data over the same four pins."""
    d = D()
    bus_y = 128
    bx0, bx1 = 64, 372
    # construction: a column grid for the blocks, and the bus line carried to the pins
    d.group('thin')
    d.lines([[(x, 30), (x, 214)] for x in (84, 150, 216, 290, 352)])
    d.line((20, bus_y), (384, bus_y))
    slot0, slot_w, ty = 58, 38, 244
    d.lines([[(slot0 + slot_w * i, 222), (slot0 + slot_w * i, 282)] for i in range(9)])
    # the internal bus, four wires wide, and the pins D0–D3 through the bus buffer
    d.group()
    for k in range(4):
        y = bus_y - 4.5 + 3 * k
        d.line((bx0, y), (bx1, y))
    _box(d, 38, bus_y - 16, 64, bus_y + 16)
    d.lines([[(20, bus_y - 9 + 6 * k), (38, bus_y - 9 + 6 * k)] for k in range(4)])
    # above the bus: accumulator, temporary register, ALU, flags; instruction register and decoder
    _box(d, 70, 78, 104, 96)
    _box(d, 132, 78, 166, 96)
    _alu(d, 118, 34, 76, 26)
    _box(d, 176, 44, 196, 58)
    _box(d, 216, 70, 272, 96)
    _box(d, 216, 36, 272, 60)
    # below the bus: the address stack (program counter and three levels, 12 bits each),
    # the sixteen 4-bit index registers, timing and control
    _box(d, 72, 156, 144, 204)
    _box(d, 164, 156, 232, 204)
    _box(d, 262, 156, 366, 204)
    # details: register cells, the wires between blocks and the bus
    d.group('mid')
    _cells(d, 72, 156, 144, 204, 3, 4)
    _cells(d, 164, 156, 232, 204, 2, 8)
    d.lines([[(87, 96), (87, bus_y - 5)], [(149, 96), (149, bus_y - 5)], [(87, 78), (87, 61)], [(149, 78), (149, 61)],
             [(118, 60), (118, 66), (60, 66), (60, 112)], [(196, 51), (206, 51)],
             [(244, 96), (244, bus_y - 5)], [(244, 70), (244, 60)],
             [(108, 156), (108, bus_y + 5)], [(198, 156), (198, bus_y + 5)], [(314, 156), (314, bus_y + 5)],
             [(272, 48), (300, 48), (300, 140), (314, 140), (314, 156)]])
    _arrow(d, 118, 66, math.pi / 2, 3)
    for x in (87, 149):
        _arrow(d, x, 61, -math.pi / 2, 3)
    _arrow(d, 244, 60, -math.pi / 2, 3)
    # the instruction cycle: eight clock periods, three for the address, two for the instruction, three to execute
    d.group()
    names = ['A1', 'A2', 'A3', 'M1', 'M2', 'X1', 'X2', 'X3']
    d.line((slot0, ty), (slot0 + slot_w * 8, ty))
    d.line((slot0, ty + 18), (slot0 + slot_w * 8, ty + 18))
    sync = []
    for i in range(8):
        x = slot0 + slot_w * i
        sync += [(x, 272 if i else 262), (x + 4, 272 if i else 262), (x + 4, 272), (x + slot_w, 272)]
    d.line(*sync)
    d.group('mid')
    d.lines([[(slot0 + slot_w * i, ty), (slot0 + slot_w * i, ty + 18)] for i in (3, 5)])
    # labels
    d.group()
    d.text(87, 90, 'ACC', size=7)
    d.text(149, 90, 'TEMP', size=7)
    d.text(118, 30, 'ALU', size=7)
    d.text(186, 40, 'C', size=7)
    d.text(244, 87, 'INSTR REG', size=6)
    d.text(244, 51, 'DECODE', size=6)
    d.text(108, 214, 'PC + 3-LEVEL STACK', size=6)
    d.text(198, 214, '16 × 4-BIT REGS', size=6)
    d.text(314, 184, 'TIMING · CONTROL', size=6)
    d.text(22, bus_y - 18, 'D0–D3', size=6, anchor='start')
    for i, n in enumerate(names):
        d.text(slot0 + slot_w * (i + 0.5), ty + 12, n, size=7)
    d.text(slot0 + slot_w * 1.5, ty - 5, 'ADDRESS 3 × 4 BITS', size=6)
    d.text(slot0 + slot_w * 4, ty - 5, 'INSTRUCTION', size=6)
    d.text(slot0 + slot_w * 6.5, ty - 5, 'EXECUTE', size=6)
    d.text(slot0 - 4, 272, 'SYNC', size=6, anchor='end')
    return d


def altair():
    """The Altair 8800's front panel: 36 lamps, 16 address and data switches and 8 control switches, with the switches set to octal 076,
    the 8080's MVI A (load the accumulator with the next byte), ready to DEPOSIT."""
    d = D()
    x0, x1, y0, y1 = 18, 382, 54, 246
    pitch = 20.5
    ax = [x1 - 20 - pitch * i for i in range(16)][::-1]  # index 0 = A15 at the left
    y_status, y_addr, y_sw, y_ctl = 84, 134, 170, 212
    # construction: the columns of the address bits, and the octal grouping of the switches (1, 3, 3, 3, 3, 3)
    d.group('thin')
    d.lines([[(x, 70), (x, 190)] for x in ax])
    groups = [(0, 0), (1, 3), (4, 6), (7, 9), (10, 12), (13, 15)]
    for a, b in groups:
        d.line((ax[a] - 8, 151), (ax[a] - 8, 148), (ax[b] + 8, 148), (ax[b] + 8, 151))
    d.line((x0 + 10, y_ctl), (x1 - 10, y_ctl))
    # the panel
    d.group()
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)
    d.line((x0 + 6, y0 + 6), (x1 - 6, y0 + 6), (x1 - 6, y1 - 6), (x0 + 6, y1 - 6), closed=True)
    # lamps: 12 status, 8 data (D7 … D0 over A7 … A0), 16 address
    d.group('mid')
    status_x = [x0 + 24 + 13.5 * i for i in range(12)]
    for x in status_x:
        d.circle(x, y_status, 3)
    for i in range(8, 16):
        d.circle(ax[i], y_status, 3)
    for x in ax:
        d.circle(x, y_addr, 3)
    # the byte set on the switches and shown on the data lamps after DEPOSIT: 076 octal = 0011 1110
    word = [int(c) for c in '0000000000111110']  # A15 … A0; the low eight double as data D7 … D0
    d.group()
    for i in range(8, 16):
        if word[i]:
            d.circle(ax[i], y_status, 5.5)
    # the switches: a bushing and a lever, up for 1
    for x, bit in zip(ax, word):
        d.circle(x, y_sw, 3.5)
        d.line((x, y_sw + (-3.5 if bit else 3.5)), (x, y_sw + (-15 if bit else 15)))
    # the control switches, each with a lever centred (momentary, spring-loaded)
    ctl = ['STOP', 'STEP', 'EXAM', 'DEP', 'RESET', 'PROT', 'AUX', 'AUX']
    cx = [x0 + 38 + (x1 - x0 - 76) * i / 7 for i in range(8)]
    for x in cx:
        d.circle(x, y_ctl, 3.5)
        d.line((x - 2, y_ctl - 12), (x + 2, y_ctl - 12), (x + 2, y_ctl + 12), (x - 2, y_ctl + 12), closed=True)
    d.circle(cx[3], y_ctl, 7.5)
    # labels
    d.group()
    d.text(status_x[5], y_status - 10, 'STATUS', size=6)
    d.text((ax[8] + ax[15]) / 2, y_status - 10, 'DATA D7–D0', size=6)
    d.text(ax[0] - 12, y_addr + 3, 'A15', size=6, anchor='end')
    d.text(ax[15] + 10, y_addr + 3, 'A0', size=6, anchor='start')
    for i, (a, b) in enumerate(groups[1:]):
        d.text((ax[a] + ax[b]) / 2, 145.5, '0' if i < 3 else ('7' if i == 3 else '6'), size=7)
    d.text(ax[0], 145.5, '0', size=7)
    for x, n in zip(cx, ctl):
        d.text(x, y_ctl + 22, n, size=6)
    d.text(200, 34, 'SET 076 · DEPOSIT · THE 8080 LOADS MVI A', size=8)
    d.text(200, 272, 'ALTAIR 8800 FRONT PANEL · 36 LAMPS · 16 + 8 SWITCHES', size=7)
    return d


def arm():
    """The ARM1's data path: a register bank on two read buses, a barrel shifter on one of them, the ALU,
    the result written back; under it the 32-bit data-processing instruction, every one conditional."""
    d = D()
    rb = (36, 34, 92, 190)      # register bank
    xa, xb = 118, 150           # the A and B buses
    sh = (136, 118, 164, 142)   # barrel shifter on the B bus
    alu_x, alu_y = 134, 158
    # construction: the bank's 25 rows, the bus centre lines
    d.group('thin')
    d.lines([[(rb[0], rb[1] + (rb[3] - rb[1]) * j / 25), (rb[2], rb[1] + (rb[3] - rb[1]) * j / 25)] for j in range(1, 25)])
    d.lines([[(xa, 30), (xa, 150)], [(xb, 30), (xb, 150)]])
    d.lines([[(20, 214), (382, 214)]])
    # the object: bank, shifter, ALU, address register and incrementer, data registers
    d.group()
    _box(d, *rb)
    _box(d, *sh)
    _alu(d, alu_x, alu_y, 58, 22)
    _box(d, 206, 40, 262, 60)
    _box(d, 206, 84, 262, 104)
    _box(d, 206, 128, 262, 148)
    _box(d, 206, 168, 262, 188)
    # the buses: A and B read out of the bank, the ALU result back into it
    d.group('mid')
    d.lines([[(rb[2], 60), (xa, 60), (xa, alu_y)], [(rb[2], 70), (xb, 70), (xb, sh[1])], [(xb, sh[3]), (xb, alu_y)],
             [(alu_x, alu_y + 22), (alu_x, 200), (20, 200), (20, 112), (rb[0], 112)],
             [(alu_x, 200), (180, 200), (180, 50), (206, 50)],
             [(234, 60), (234, 84)], [(262, 94), (280, 94), (280, 30), (180, 30), (180, 50)],
             [(262, 50), (300, 50)], [(206, 138), (180, 138)], [(262, 178), (300, 178)], [(206, 178), (xb + 10, 178), (xb + 10, 110), (xb, 110)]])
    # the shifter's crossing wires
    d.lines([[(sh[0] + 4 + 5 * k, sh[1] + 2), (sh[0] + 9 + 5 * k, sh[3] - 2)] for k in range(4)])
    _arrow(d, 300, 50, 0, 3)
    _arrow(d, rb[0], 112, 0, 3)
    _arrow(d, xa, alu_y, math.pi / 2, 3)
    _arrow(d, xb, alu_y, math.pi / 2, 3)
    # the instruction word: 32 cells, fields cond | 00 | I | opcode | S | Rn | Rd | operand 2
    d.group()
    wx0, wx1, wy0, wy1 = 30, 370, 232, 250
    cw = (wx1 - wx0) / 32
    _box(d, wx0, wy0, wx1, wy1)
    fields = [(31, 28, 'COND'), (27, 26, '00'), (25, 25, 'I'), (24, 21, 'OPCODE'), (20, 20, 'S'),
              (19, 16, 'Rn'), (15, 12, 'Rd'), (11, 0, 'OPERAND 2')]
    bounds = [wx0 + cw * (31 - hi) for hi, lo, n in fields[1:]]
    d.lines([[(x, wy0), (x, wy1)] for x in bounds])
    d.group('thin')
    d.lines([[(wx0 + cw * i, wy1 - 4), (wx0 + cw * i, wy1)] for i in range(1, 32)])
    # labels
    d.group()
    d.text((rb[0] + rb[2]) / 2, rb[1] - 6, 'REGISTERS', size=6)
    d.text((rb[0] + rb[2]) / 2, rb[3] + 10, '25 × 32 BITS', size=6)
    d.text(xa, 26, 'A', size=7)
    d.text(xb, 26, 'B', size=7)
    d.text(sh[2] + 4, 133, 'SHIFT', size=6, anchor='start')
    d.text(alu_x, alu_y + 14, 'ALU', size=6)
    d.text(234, 53, 'ADDRESS', size=6)
    d.text(234, 97, '+4', size=7)
    d.text(234, 141, 'DATA IN', size=6)
    d.text(234, 181, 'DATA OUT', size=6)
    d.text(304, 53, 'TO MEMORY', size=6, anchor='start')
    for hi, lo, n in fields:
        xm = wx0 + cw * (31 - (hi + lo) / 2)
        d.text(xm, wy1 + 12, n, size=6)
        d.text(wx0 + cw * (31 - hi) + 1.5, wy0 - 3, str(hi), size=5, anchor='start')
    d.text(200, 286, 'ARM1 · 1985 · EVERY INSTRUCTION CARRIES ITS OWN CONDITION', size=7)
    return d


def smartphone():
    """A multi-touch phone at the first iPhone's size (115 × 61 mm, a 3.5-inch 320 × 480 screen), with the
    touch sensor's rows and columns over the screen and two fingers; beside it, the map the controller reads:
    two separate peaks where the fingers change the capacitance between rows and columns."""
    d = D()
    s = 2.15  # px per mm
    W, H = 61 * s, 115 * s
    px0, py0 = 30, 150 - H / 2
    r = 9 * s
    diag = 3.5 * 25.4
    sw, shh = diag * 2 / math.hypot(2, 3) * s, diag * 3 / math.hypot(2, 3) * s  # 2:3 screen
    sx0, sy0 = px0 + (W - sw) / 2, py0 + (H - shh) / 2
    pitch = 5 * s
    cols = int(sw // pitch)
    rows = int(shh // pitch)
    gx = [sx0 + (sw - cols * pitch) / 2 + pitch * (i + 0.5) for i in range(cols)]
    gy = [sy0 + (shh - rows * pitch) / 2 + pitch * (j + 0.5) for j in range(rows)]
    touches = [(gx[2], gy[4]), (gx[5], gy[10])]
    # construction: the sensor's drive rows and sense columns over the screen
    d.group('thin')
    d.lines([[(x, sy0), (x, sy0 + shh)] for x in gx])
    d.lines([[(sx0, y), (sx0 + sw, y)] for y in gy])
    # the phone: rounded body, screen, home button
    d.group()
    pts = []
    for cx, cy, a0 in ((px0 + W - r, py0 + r, -90), (px0 + W - r, py0 + H - r, 0), (px0 + r, py0 + H - r, 90), (px0 + r, py0 + r, 180)):
        for k in range(10):
            a = math.radians(a0 + 9 * k + 9 * (k == 9) * 0)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(*pts, closed=True)
    _box(d, sx0, sy0, sx0 + sw, sy0 + shh)
    d.circle(px0 + W / 2, sy0 + shh + (py0 + H - sy0 - shh) / 2, 5.5 * s)
    d.line((px0 + W / 2 - 5 * s, py0 + (sy0 - py0) / 2), (px0 + W / 2 + 5 * s, py0 + (sy0 - py0) / 2))
    # the fingers, each a disc of changed field over the crossings under it
    d.group('mid')
    for tx, ty in touches:
        for rr in (4, 9, 14):
            d.circle(tx, ty, rr)
    # the map the controller reads: the same grid, a contour of the capacitance change at each touch
    mx0, my0, mp = 226, 44, 13
    mcols, mrows = cols, rows
    d.group('thin')
    d.lines([[(mx0 + mp * i, my0), (mx0 + mp * i, my0 + mp * mrows)] for i in range(mcols + 1)])
    d.lines([[(mx0, my0 + mp * j), (mx0 + mp * mcols, my0 + mp * j)] for j in range(mrows + 1)])
    d.group()
    for tx, ty in touches:
        i, j = gx.index(tx), gy.index(ty)
        cx, cy = mx0 + mp * (i + 0.5), my0 + mp * (j + 0.5)
        for k, rr in enumerate((5, 11, 17)):
            d.ellipse(cx, cy, rr * 1.1, rr * 0.9)
    d.group('mid')
    for tx, ty in touches:
        i, j = gx.index(tx), gy.index(ty)
        d.line((tx + 16, ty), (mx0 - 6, my0 + mp * (j + 0.5)))
        _arrow(d, mx0 - 6, my0 + mp * (j + 0.5), math.atan2(my0 + mp * (j + 0.5) - ty, mx0 - 6 - tx - 16), 3)
    # labels
    d.group()
    d.text(mx0 + mp * mcols / 2, my0 - 8, 'CAPACITANCE CHANGE', size=6)
    yb = my0 + mp * mrows
    d.text(mx0, yb + 12, 'ROWS DRIVEN · COLUMNS SENSED', size=6, anchor='start')
    d.text(mx0, yb + 22, 'TWO FINGERS · TWO PEAKS', size=6, anchor='start')
    d.text(px0 + W / 2, py0 - 8, '115 × 61 MM', size=6)
    return d


def where_computing_is():
    """Energy per floating-point operation of each TOP500 No. 1 whose power was reported, 2002–2026, on a log
    axis reaching down to Landauer's bound for erasing one bit at room temperature, kT ln 2 at 300 K."""
    d = D()
    # (year, Rmax in flop/s, power in W) from the TOP500 lists
    pts = [(2002.5, 35.86e12, 3.2e6), (2008.5, 1.026e15, 2.345e6), (2011.5, 8.162e15, 9.899e6),
           (2016.5, 93.01459e15, 15.371e6), (2020.5, 415.53e15, 28.335e6), (2022.5, 1.102e18, 21.1e6),
           (2024.9, 1.742e18, 29.581e6), (2026.5, 2.1984e18, 42.22e6)]
    landauer = 1.380649e-23 * 300 * math.log(2)
    x0, x1, y0, y1 = 64, 372, 36, 250
    yr0, yr1 = 2000, 2030
    e_hi, e_lo = -6, -22  # log10 joules
    X = lambda yr: x0 + (x1 - x0) * (yr - yr0) / (yr1 - yr0)
    Y = lambda e: y0 + (y1 - y0) * (e_hi - math.log10(e)) / (e_hi - e_lo)
    # construction: decade lines and the year grid
    d.group('thin')
    d.lines([[(x0, Y(10.0 ** k)), (x1, Y(10.0 ** k))] for k in range(e_lo, e_hi + 1, 2)])
    d.lines([[(X(yr), y0), (X(yr), y1)] for yr in range(yr0, yr1 + 1, 5)])
    # the axes
    d.group()
    d.line((x0, y0), (x0, y1), (x1, y1))
    # the limit: kT ln 2
    d.group('mid')
    d.line((x0, Y(landauer)), (x1, Y(landauer)))
    # the machines, joules per flop = power / Rmax, joined in order
    d.group()
    xy = [(X(yr), Y(p / r)) for yr, r, p in pts]
    d.line(*xy)
    for x, y in xy:
        d.circle(x, y, 2.6)
    # the gap still open, as a dimension line from the last machine down to the limit
    d.group('mid')
    xg = X(2028.5)
    d.line((xg, xy[-1][1]), (xg, Y(landauer)))
    _arrow(d, xg, xy[-1][1], -math.pi / 2, 3)
    _arrow(d, xg, Y(landauer), math.pi / 2, 3)
    # labels
    d.group()
    for k in range(e_lo, e_hi + 1, 4):
        d.text(x0 - 5, Y(10.0 ** k) + 3, f'10{str(k).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))}', size=7, anchor='end')
    for yr in (2000, 2010, 2020, 2030):
        d.text(X(yr), y1 + 12, str(yr), size=7)
    d.text(x0 + 4, y0 - 8, 'JOULES PER FLOP · TOP500 NO. 1', size=7, anchor='start')
    d.text(X(2001), Y(landauer) - 5, 'kT ln 2 AT 300 K · ONE BIT ERASED', size=6, anchor='start')
    d.text(xg - 4, (xy[-1][1] + Y(landauer)) / 2, '~10 DECADES', size=6, anchor='end')
    d.text(xy[0][0] + 4, xy[0][1] - 6, 'EARTH SIMULATOR', size=6, anchor='start')
    d.text(xy[-1][0] - 4, xy[-1][1] - 8, 'LINESHINE', size=6, anchor='end')
    return d


PLATES = {'microprocessor': microprocessor, 'altair': altair, 'arm': arm, 'smartphone': smartphone,
          'where-computing-is': where_computing_is}
