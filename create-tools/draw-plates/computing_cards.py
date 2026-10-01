"""computing plates, segment "Cards, gears and relays" (sprint 015). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _spring(x, y0, y1, turns=5, w=3):
    """A coil spring seen from the side, as a zigzag from (x, y0) to (x, y1)."""
    n = 2 * turns
    pts = [(x, y0)]
    for i in range(1, n):
        pts.append((x + (w if i % 2 else -w), y0 + (y1 - y0) * i / n))
    pts.append((x, y1))
    return pts


def hollerith():
    """Hollerith's press in section: spring pins over a card, mercury cups under it; a pin through a hole
    closes a circuit that steps a counter one division of a hundred."""
    d = D()
    n, pitch, x0 = 8, 22, 44          # eight hole positions of one row, at the card's quarter-inch pitch
    xs = [x0 + pitch * i for i in range(n)]
    holes = {1, 4, 6}                  # the positions punched in this card
    box_top, box_bot = 44, 92          # the press's pin box, brought down by the handle
    card_y = 118                       # the card, lying on the hard-rubber bed plate
    bed_top, bed_bot = 122, 170
    cup_top, cup_bot = 124, 150
    merc = 132                         # the mercury level in the cups
    # construction: the centre line of each hole position, carried from the box to the binding posts;
    # the card plane and the mercury level
    d.group('thin')
    d.lines([[(x, box_top - 8), (x, bed_bot + 14)] for x in xs])
    d.line((x0 - 22, card_y), (xs[-1] + 22, card_y))
    d.line((x0 - 22, merc), (xs[-1] + 22, merc))
    # the press: the pin box above, the bed plate with its cups below, and the card between
    d.group()
    d.line((x0 - 16, box_top), (xs[-1] + 16, box_top), (xs[-1] + 16, box_bot), (x0 - 16, box_bot), closed=True)
    d.line((x0 - 16, bed_top), (xs[-1] + 16, bed_top), (xs[-1] + 16, bed_bot), (x0 - 16, bed_bot), (x0 - 16, bed_top))
    for x in xs:
        d.line((x - 6, bed_top), (x - 6, cup_bot), (x + 6, cup_bot), (x + 6, bed_top))
    # the card: a thin strip broken at each punched hole
    edges = [x0 - 20]
    for i in sorted(holes):
        edges += [xs[i] - 4, xs[i] + 4]
    edges.append(xs[-1] + 20)
    d.lines([[(edges[k], card_y - 2), (edges[k + 1], card_y - 2), (edges[k + 1], card_y + 2),
              (edges[k], card_y + 2), (edges[k], card_y - 2)] for k in range(0, len(edges), 2)])
    # the pins and their springs: a pin over a hole passes through into the mercury; the rest are pushed back
    d.group('mid')
    L = 56
    for i, x in enumerate(xs):
        tip = merc + 6 if i in holes else card_y - 3
        top = tip - L
        d.line(*_spring(x, box_top + 2, top - 2))
    d.group()
    for i, x in enumerate(xs):
        tip = merc + 6 if i in holes else card_y - 3
        top = tip - L
        d.line((x - 1.5, top), (x - 1.5, tip - 2), (x, tip), (x + 1.5, tip - 2), (x + 1.5, top))
        d.line((x - 5, top - 2), (x + 5, top - 2), (x + 5, top), (x - 5, top), closed=True)
    # the mercury in each cup, its surface standing a little proud, and the nail and wire under each cup
    d.group('mid')
    for i, x in enumerate(xs):
        d.arc(x, merc + 2, 6, 180, 360, n=12, ry=3)
        d.line((x, cup_bot), (x, bed_bot))
    # the circuit: the punched positions wired to three counters, a battery back to the pins
    d.group()
    cy, r = 244, 18
    cxs = [96, 176, 256]
    for i, cx in zip(sorted(holes), cxs):
        d.line((xs[i], bed_bot), (xs[i], bed_bot + 14), (cx, bed_bot + 14 + (i + 1) * 3), (cx, cy - r - 12))
        # the counter's electromagnet, a coil in front of its dial
        d.line(*[(cx - 6 + 12 * k / 16, cy - r - 12 + (3 if k % 2 else 0)) for k in range(17)])
        d.circle(cx, cy, r)
    d.line((xs[-1] + 16, box_top + 20), (340, box_top + 20), (340, cy - 14))
    d.line((332, cy - 14), (348, cy - 14))
    d.line((336, cy - 8), (344, cy - 8))
    d.line((340, cy - 8), (340, cy + r + 10), (cxs[0], cy + r + 10), (cxs[0], cy + r))
    d.lines([[(cx, cy + r + 10), (cx, cy + r)] for cx in cxs[1:]])
    # each dial's hundred divisions and its two hands: units, and hundreds
    d.group('mid')
    for j, cx in enumerate(cxs):
        ticks = []
        for k in range(100):
            a = 2 * math.pi * k / 100 - math.pi / 2
            ln = 4 if k % 10 == 0 else 2
            ticks.append([(cx + r * math.cos(a), cy + r * math.sin(a)),
                          (cx + (r - ln) * math.cos(a), cy + (r - ln) * math.sin(a))])
        d.lines(ticks)
        count = [3721, 1405, 862][j]
        for val, ln in ((count % 100, r - 3), (count // 100, r - 8)):
            a = 2 * math.pi * val / 100 - math.pi / 2
            d.line((cx, cy), (cx + ln * math.cos(a), cy + ln * math.sin(a)))
    # labels
    d.group()
    d.text(x0 - 22, box_top - 12, 'PIN BOX', size=7, anchor='start')
    d.text(xs[-1] + 26, card_y + 3, 'CARD', size=7, anchor='start')
    d.text(xs[-1] + 26, merc + 11, 'MERCURY', size=7, anchor='start')
    d.text(xs[-1] + 26, bed_bot - 4, 'BED PLATE', size=7, anchor='start')
    d.text(352, cy - 9, 'BATTERY', size=7, anchor='start')
    d.text(176, 290, 'A PIN THROUGH A HOLE STEPS ITS COUNTER BY ONE', size=8)
    return d


def differential_analyzer():
    """A wheel-and-disc integrator in perspective, and the curve it draws when its output is fed back to
    set its own wheel: dy/dx = y, Bush's simplest back-coupling."""
    d = D()
    cx, cy, R, k = 112, 176, 64, 0.34   # the disc: its centre, radius and the foreshortening of its plane
    P = lambda u, v: (cx + u, cy + k * v)  # a point on the disc's plane, u across and v into the page
    wr = 40                             # the wheel's distance from the disc's centre: the integrand y
    wheel_r = 18
    wx, wy = P(wr, 0)
    hub = wy - wheel_r                  # the wheel's hub, on an axle along the radius
    amp_x0, amp_x1 = 214, 244           # the torque amplifier's case
    screw_y = 112                       # the lead screw that carries the wheel across the disc
    fb_x = 262                          # the feedback shaft, from the amplifier back to the screw
    # construction: the disc's axis and the radius the wheel sits on, with the radius dimensioned
    d.group('thin')
    d.line((cx, cy - 56), (cx, cy + 72))
    d.line(P(-R - 12, 0), P(R + 16, 0))
    d.line(P(0, -R - 6), P(0, R + 6))
    d.line((wx, screw_y), (wx, wy + 18))
    d.lines([[(cx, cy + 20), (cx, cy + 40)], [(wx, cy + 18), (wx, cy + 40)]])
    d.line((cx, cy + 33), (wx, cy + 33))
    _arrow(d, cx, cy + 33, math.pi, 3)
    _arrow(d, wx, cy + 33, 0, 3)
    # the disc on its spindle, and the bevel that turns it from the x shaft
    d.group()
    d.ellipse(cx, cy, R, R * k)
    d.arc(cx, cy + 7, R, 0, 180, ry=R * k)
    d.line((cx - R, cy), (cx - R, cy + 7))
    d.line((cx + R, cy), (cx + R, cy + 7))
    d.line((cx - 4, cy + 7 + R * k), (cx - 4, cy + 58), (cx + 4, cy + 58), (cx + 4, cy + 7 + R * k))
    d.ellipse(cx, cy + 62, 11, 4)
    d.line((cx + 11, cy + 62), (cx + 92, cy + 62))
    # the wheel, standing on the disc at radius y (its plane across the radius, so seen foreshortened),
    # its axle along the radius into the torque amplifier
    d.ellipse(wx, hub, wheel_r * k, wheel_r)
    d.line((wx, hub), (amp_x0, hub))
    d.line((amp_x0, hub - 16), (amp_x1, hub - 16), (amp_x1, hub + 16), (amp_x0, hub + 16), closed=True)
    # the lead screw and the fork that sets the wheel's radius; the amplifier's two drums
    d.group('mid')
    d.line((78, screw_y), (fb_x, screw_y))
    d.lines([[(x, screw_y - 3), (x + 3, screw_y + 3)] for x in range(82, fb_x - 4, 5)])
    d.line((wx - 4, screw_y), (wx - 4, hub - wheel_r - 4), (wx + 4, hub - wheel_r - 4), (wx + 4, screw_y))
    d.circle((amp_x0 + amp_x1) / 2, hub - 7, 5)
    d.circle((amp_x0 + amp_x1) / 2, hub + 7, 5)
    # the back-coupling: the amplified output led round to the screw that sets the wheel
    d.group()
    d.line((amp_x1, hub), (fb_x, hub), (fb_x, screw_y))
    _arrow(d, fb_x, screw_y + 8, -math.pi / 2)
    _arrow(d, cx + 70, cy + 62, 0)
    # the output table: y against x, the curve the machine draws, e to the x
    d.group('thin')
    gx0, gy0, gw, gh = 290, 236, 94, 186
    xm = 2.0
    ym = math.exp(xm)
    d.line((gx0, gy0), (gx0 + gw, gy0))
    d.line((gx0, gy0), (gx0, gy0 - gh))
    d.lines([[(gx0 + gw * t / 4, gy0), (gx0 + gw * t / 4, gy0 + 4)] for t in range(5)])
    d.lines([[(gx0 - 4, gy0 - gh * v / ym), (gx0, gy0 - gh * v / ym)] for v in range(1, 8)])
    d.group()
    d.line(*[(gx0 + gw * i / 60, gy0 - gh * math.exp(xm * i / 60) / ym) for i in range(61)])
    # labels
    d.group()
    d.text(cx - R - 6, cy + 16, 'DISC', size=7, anchor='end')
    d.text(wx + 8, hub - wheel_r - 10, 'WHEEL', size=7, anchor='start')
    d.text((amp_x0 + amp_x1) / 2, hub + 28, 'TORQUE', size=7)
    d.text((amp_x0 + amp_x1) / 2, hub + 37, 'AMPLIFIER', size=7)
    d.text((cx + wx) / 2, cy + 46, 'r = y', size=8)
    d.text(150, 56, 'ONE INTEGRATOR, BACK-COUPLED', size=8)
    d.text(cx + 96, cy + 65, 'x', size=9, anchor='start')
    d.text(fb_x - 6, screw_y - 10, '∫y dx → y', size=8, anchor='end')
    d.text(78, screw_y - 8, 'LEAD SCREW', size=7, anchor='start')
    d.text(gx0 + gw, gy0 + 14, 'x', size=8)
    d.text(gx0 - 8, gy0 - gh + 4, 'y', size=8, anchor='end')
    d.text(gx0 + 8, gy0 - gh + 10, 'y = eˣ', size=8, anchor='start')
    d.text(200, 286, 'dy/dx = y · THE OUTPUT SETS ITS OWN WHEEL', size=8)
    return d


# The Z3's opcodes, as Rojas read them from Zuse's 1941 patent application (IEEE Annals 19:2, 1997, table 1).
Z3_OPS = {'Lu': '01110000', 'Ld': '01111000', 'Lm': '01001000', 'Li': '01010000', 'Lw': '01011000',
          'Ls1': '01100000', 'Ls2': '01101000'}


def _z3_code(op, addr=None):
    if op == 'Pr':
        return '11' + format(addr, '06b')
    if op == 'Ps':
        return '10' + format(addr, '06b')
    return Z3_OPS[op]


def z3():
    """A strip of punched film carrying a Z3 program (z4 = z1 × z2 + z3, then display it), each row one
    eight-bit instruction, beside the 22-bit floating-point word the program works on."""
    d = D()
    prog = [('Pr', 1, 'LOAD z1'), ('Pr', 2, 'LOAD z2'), ('Lm', None, 'MULTIPLY'), ('Pr', 3, 'LOAD z3'),
            ('Ls1', None, 'ADD'), ('Ps', 4, 'STORE z4'), ('Ld', None, 'DISPLAY')]
    fx0, fw = 28, 98             # the film strip's left edge and width
    bit = 9                      # the pitch of the eight data holes across the strip
    bx0 = fx0 + (fw - 7 * bit) / 2
    row0, rp = 46, 28            # the first instruction row and the row pitch
    top, bot = 22, row0 + rp * len(prog) - 4
    # construction: the eight bit columns down the strip, and a line through each row carried to its label
    d.group('thin')
    d.lines([[(bx0 + bit * b, top), (bx0 + bit * b, bot)] for b in range(8)])
    d.lines([[(fx0 - 6, row0 + rp * i), (fx0 + fw + 34, row0 + rp * i)] for i in range(len(prog))])
    # the film: its edges and its sprocket holes, four to a row as on 35 mm film
    d.group()
    d.line((fx0, top), (fx0, bot))
    d.line((fx0 + fw, top), (fx0 + fw, bot))
    d.group('mid')
    for yy in range(int(top) + 4, int(bot) - 4, 7):
        for sx in (fx0 + 5, fx0 + fw - 9):
            d.line((sx, yy), (sx + 4, yy), (sx + 4, yy + 4), (sx, yy + 4), closed=True)
    # the punched holes: a 1 is a hole
    d.group()
    for i, (op, addr, _) in enumerate(prog):
        code = _z3_code(op, addr)
        for b, c in enumerate(code):
            if c == '1':
                d.circle(bx0 + bit * b, row0 + rp * i, 2.6)
    # the word the program works on: sign, seven exponent bits, fourteen significand bits after the
    # hidden leading 1
    d.group('thin')
    wx0, wy, cw, ch = 184, 222, 8.0, 16
    d.lines([[(wx0 + cw * c, wy - 6), (wx0 + cw * c, wy + ch + 6)] for c in (0, 1, 8, 22)])
    d.group()
    d.line((wx0, wy), (wx0 + cw * 22, wy), (wx0 + cw * 22, wy + ch), (wx0, wy + ch), closed=True)
    d.group('mid')
    d.lines([[(wx0 + cw * c, wy), (wx0 + cw * c, wy + ch)] for c in range(1, 22)])
    hx = wx0 + cw * 8
    d.line((hx - 3, wy - 12), (hx + 3, wy - 12))
    d.line((hx - 3, wy - 20), (hx + 3, wy - 20), (hx + 3, wy - 12))
    d.line((hx - 3, wy - 20), (hx - 3, wy - 12))
    # the two registers the instructions work through, and the arithmetic unit that combines them and
    # returns its result to R1
    rx0, rx1 = wx0, wx0 + cw * 22
    r1y, r2y, rh = 72, 104, 14
    au_top, au_bot = 140, 164
    amid = (rx0 + rx1) / 2
    d.group()
    for ry in (r1y, r2y):
        d.line((rx0, ry), (rx1, ry), (rx1, ry + rh), (rx0, ry + rh), closed=True)
    d.line((amid - 50, au_top), (amid + 50, au_top), (amid + 26, au_bot), (amid - 26, au_bot), closed=True)
    d.group('mid')
    d.lines([[(rx0 + cw * c, ry), (rx0 + cw * c, ry + rh)] for ry in (r1y, r2y) for c in range(1, 22)])
    d.line((rx1, r1y + rh / 2), (rx1 + 10, r1y + rh / 2), (rx1 + 10, au_top - 10), (amid + 30, au_top - 10),
           (amid + 30, au_top))
    d.line((amid - 30, r2y + rh), (amid - 30, au_top))
    d.line((amid, au_bot), (amid, au_bot + 10), (rx0 - 12, au_bot + 10), (rx0 - 12, r1y + rh / 2), (rx0, r1y + rh / 2))
    _arrow(d, rx0, r1y + rh / 2, 0)
    _arrow(d, amid - 30, au_top, math.pi / 2)
    _arrow(d, amid + 30, au_top, math.pi / 2)
    # labels
    d.group()
    for i, (op, addr, gloss) in enumerate(prog):
        name = f'{op} {addr}' if addr else op
        d.text(fx0 + fw + 8, row0 + rp * i + 3, name, size=7, anchor='start')
    d.text(rx1 + 14, r1y + rh - 3, 'R1', size=8, anchor='start')
    d.text(rx1 + 14, r2y + rh - 3, 'R2', size=8, anchor='start')
    d.text(amid, au_top + 15, '+ − × ÷ √', size=8)
    d.text(amid, 52, 'z4 = z1 × z2 + z3', size=8)
    d.text(wx0 + 4, wy + ch + 16, '±', size=8)
    d.text(wx0 + cw * 4.5, wy + ch + 16, 'EXP 7', size=7)
    d.text(wx0 + cw * 15, wy + ch + 16, 'SIGNIFICAND 14', size=7)
    d.text(hx + 8, wy - 13, 'HIDDEN 1', size=7, anchor='start')
    d.text(wx0 + cw * 11, wy - 30, '22-BIT FLOATING-POINT WORD', size=7)
    d.text(fx0 + fw / 2, 288, 'ONE ROW, ONE INSTRUCTION', size=7)
    return d


PLATES = {'hollerith': hollerith, 'differential-analyzer': differential_analyzer, 'z3': z3}
