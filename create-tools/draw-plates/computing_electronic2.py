"""computing plates: the Manchester Baby, EDSAC, UNIVAC I and Whirlwind (sprint 015). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _span(d, x0, x1, y):
    """A horizontal dimension line from x0 to x1 at height y, arrowed at both ends."""
    d.line((x0, y), (x1, y))
    _arrow(d, x0, y, math.pi)
    _arrow(d, x1, y, 0)


def _bits_lsb_first(n, width):
    """n as `width` binary digits, least significant first: the Manchester machines wrote numbers that way."""
    return [(n >> i) & 1 for i in range(width)]


def manchester_baby():
    """A Williams-Kilburn tube: the CRT in section with its pick-up plate, the screen face holding
    three words as dots (0) and dashes (1), least significant digit on the left, and the timing of
    one digit period: the bright-up for a dot and for a dash, and the pulse the plate sees."""
    d = D()
    # --- the CRT in side section: neck, flare and face, on its axis
    ax_y = 104
    x_gun, x_neck, x_flare, x_face = 22, 96, 150, 176
    r_neck, r_face = 11, 50
    d.group('thin')
    d.line((14, ax_y), (x_face + 22, ax_y))                        # the tube's axis
    spot_y = ax_y - 30                                             # the addressed spot on the face
    d.line((x_face, spot_y), (x_face + 30, spot_y))                # the spot projected to the face view
    d.lines([[(x_face + 12, ax_y - r_face - 4), (x_face + 12, ax_y + r_face + 4)]])
    # the envelope: a neck, a conical flare, a slightly domed face
    d.group()
    top = [(x_gun, ax_y - r_neck), (x_neck, ax_y - r_neck), (x_flare, ax_y - r_face + 6)]
    bot = [(x, 2 * ax_y - y) for x, y in top]
    d.line(*top)
    d.line(*bot)
    d.line((x_gun, ax_y - r_neck), (x_gun, ax_y + r_neck))
    face = [(x_face - 6 + 6 * math.cos(math.radians(a)), ax_y + r_face * math.sin(math.radians(a)))
            for a in range(-90, 91, 6)]
    d.line((x_flare, ax_y - r_face + 6), (x_face - 6, ax_y - r_face), *face, (x_face - 6, ax_y + r_face),
           (x_flare, ax_y + r_face - 6))
    # the pick-up plate, just in front of the face, and its lead
    d.line((x_face + 12, ax_y - r_face + 4), (x_face + 12, ax_y + r_face - 4))
    d.line((x_face + 12, ax_y + r_face - 4), (x_face + 12, ax_y + r_face + 14), (x_face - 30, ax_y + r_face + 14))
    # the gun and the deflection plates
    d.group('mid')
    d.line((x_gun + 6, ax_y - 5), (x_gun + 6, ax_y + 5))           # cathode
    d.lines([[(x_gun + 14, ax_y - 8), (x_gun + 14, ax_y - 2)], [(x_gun + 14, ax_y + 2), (x_gun + 14, ax_y + 8)]])  # grid
    d.lines([[(x_gun + 24, ax_y - 7), (x_gun + 24, ax_y - 2)], [(x_gun + 24, ax_y + 2), (x_gun + 24, ax_y + 7)]])  # anode
    d.lines([[(62, ax_y - 8), (74, ax_y - 8)], [(62, ax_y + 8), (74, ax_y + 8)]])   # Y plates
    d.lines([[(80, ax_y - 9), (90, ax_y - 9)], [(80, ax_y + 9), (90, ax_y + 9)]])   # X plates (edge-on)
    # the beam, bent by the plates up to the spot
    d.group()
    pts = [(x_gun + 6, ax_y), (68, ax_y)]
    for k in range(1, 9):
        t = k / 8
        pts.append((68 + (x_face - 6 - 68) * t, ax_y - 30 * t ** 1.15))
    d.line(*pts)
    # --- the face seen from the front: 8 of its 32 lines, 20 of its 32 digits
    fx0, fy0, px, py = 236, 48, 7.4, 11
    rows = [262144, 262143, 131072, 0, 0, 0, 0, 0]
    d.group('thin')
    d.line((fx0 - 8, fy0 - 10), (fx0 + 20 * px + 2, fy0 - 10), (fx0 + 20 * px + 2, fy0 + 8 * py + 2),
           (fx0 - 8, fy0 + 8 * py + 2), closed=True)
    d.lines([[(fx0 + i * px, fy0 - 6), (fx0 + i * px, fy0 - 3)] for i in range(0, 20, 4)])
    d.group()
    dashes = []
    for r, n in enumerate(rows):
        y = fy0 + r * py
        for i, b in enumerate(_bits_lsb_first(n, 20)):
            x = fx0 + i * px
            if b:
                dashes.append([(x - 0.6, y), (x + 4.2, y)])
            else:
                d.circle(x, y, 0.9)
    d.lines(dashes)
    # --- one digit period: the bright-up signal and the plate's pulse
    tx0, tw = 30, 150
    d.group('thin')
    d.lines([[(tx0, 232), (tx0 + 2 * tw + 40, 232)], [(tx0, 270), (tx0 + 2 * tw + 40, 270)]])
    d.lines([[(tx0 + tw * k + 20 * (k > 0), 222), (tx0 + tw * k + 20 * (k > 0), 282)] for k in range(3)])
    d.group()
    z = [(tx0, 232), (tx0 + 30, 232), (tx0 + 30, 216), (tx0 + 52, 216), (tx0 + 52, 232),     # a dot
         (tx0 + tw + 20, 232), (tx0 + tw + 50, 232), (tx0 + tw + 50, 216), (tx0 + tw + 118, 216),  # a dash
         (tx0 + tw + 118, 232), (tx0 + 2 * tw + 40, 232)]
    d.line(*z)
    # the plate: no change of charge at a dot, a positive pulse where a dash had been
    d.group('mid')
    sig = [(tx0, 270), (tx0 + tw + 50, 270)]
    for k in range(13):
        t = k / 12
        sig.append((tx0 + tw + 50 + 20 * t, 270 - 18 * math.sin(math.pi * t) * math.exp(-1.2 * t)))
    sig.append((tx0 + 2 * tw + 40, 270))
    d.line(*sig)
    # labels
    d.group()
    d.text(x_gun + 12, ax_y + 30, 'GUN', size=7)
    d.text(76, ax_y + 30, 'X · Y', size=7)
    d.text(x_face + 16, ax_y - r_face - 8, 'PICK-UP PLATE', size=7, anchor='end')
    d.text(fx0 - 12, fy0 + 3, '2¹⁸', size=7, anchor='end')
    d.text(fx0 - 12, fy0 + py + 3, 'b', size=7, anchor='end')
    d.text(fx0 - 12, fy0 + 2 * py + 3, '2¹⁷', size=7, anchor='end')
    d.text(fx0 + 80, fy0 + 8 * py + 16, 'DOT = 0 · DASH = 1 · LSD LEFT', size=7)
    d.text(tx0 - 6, 229, 'Z', size=8, anchor='end')
    d.text(tx0 - 6, 267, 'P', size=8, anchor='end')
    d.text(tx0 + 75, 212, 'DOT', size=7)
    d.text(tx0 + tw + 95, 212, 'DASH', size=7)
    d.text(tx0 + tw + 95, 286, 'NEXT SCAN: PULSE → 1', size=7)
    d.text(tx0 + 75, 286, 'NEXT SCAN: NONE → 0', size=7)
    d.text(200, 22, 'WILLIAMS–KILBURN TUBE · 32 WORDS OF 32 DIGITS', size=8)
    return d


def edsac():
    """A mercury delay-line tank with its recirculation loop, and the pulse train inside it:
    32 words of 18 digit periods at 500 kHz, so 576 pulses in flight, back every 1.152 ms."""
    d = D()
    x0, x1, y = 40, 360, 92
    r = 13
    # construction: the tank's axis, the dimension, the digit-period grid over the pulse train
    d.group('thin')
    d.line((x0 - 16, y), (x1 + 16, y))
    d.lines([[(x0, y - r - 16), (x0, y - r - 4)], [(x1, y - r - 16), (x1, y - r - 4)]])
    pulse_y, px0, pitch = 262, 34, 6.6
    d.lines([[(px0 + i * pitch, pulse_y - 22), (px0 + i * pitch, pulse_y + 3)] for i in range(0, 47)])
    # the tank, its end caps and the crystals
    d.group()
    d.line((x0, y - r), (x1, y - r))
    d.line((x0, y + r), (x1, y + r))
    for xe, s in ((x0, -1), (x1, 1)):
        d.line((xe, y - r - 4), (xe + s * 10, y - r - 4), (xe + s * 10, y + r + 4), (xe, y + r + 4), closed=True)
    d.group('mid')
    d.lines([[(x0 + 2, y - 8), (x0 + 2, y + 8)], [(x1 - 2, y - 8), (x1 - 2, y + 8)]])
    # the sound in the mercury: packets of compression moving left to right
    bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]
    seg = (x1 - x0 - 20) / len(bits)
    for i, b in enumerate(bits):
        if b:
            xc = x0 + 10 + seg * (i + 0.5)
            d.lines([[(xc + dx, y - 6), (xc + dx, y + 6)] for dx in (-2.4, 0, 2.4)])
    # the recirculation loop: out of the receiving crystal, amplify, reshape and retime, gate, back in
    d.group()
    ly = 170
    boxes = [(300, 'AMP'), (218, 'RETIME'), (136, 'GATE')]
    for bx, _ in boxes:
        d.line((bx - 26, ly - 12), (bx + 26, ly - 12), (bx + 26, ly + 12), (bx - 26, ly + 12), closed=True)
    d.line((x1 + 10, y), (x1 + 26, y), (x1 + 26, ly), (326, ly))
    _arrow(d, 326, ly, math.pi)
    d.line((274, ly), (244, ly))
    _arrow(d, 244, ly, math.pi)
    d.line((192, ly), (162, ly))
    _arrow(d, 162, ly, math.pi)
    d.line((110, ly), (x0 - 26, ly), (x0 - 26, y), (x0 - 10, y))
    _arrow(d, x0 - 10, y, 0)
    # the clock into the retimer, and the write and read lines at the gate
    d.group('mid')
    d.line((218, ly + 12), (218, ly + 34))
    _arrow(d, 218, ly + 12, -math.pi / 2)
    d.line((124, ly + 12), (124, ly + 34))
    _arrow(d, 124, ly + 12, -math.pi / 2)
    d.line((148, ly + 12), (148, ly + 34))
    _arrow(d, 148, ly + 34, math.pi / 2)
    # the pulse train: one word of 18 digit periods, then the start of the next
    d.group()
    word = [0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0] + [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0] + [1] * 14
    pts = [(px0, pulse_y)]
    for i, b in enumerate(word[:46]):
        xa = px0 + i * pitch
        if b:
            pts += [(xa + 1.4, pulse_y), (xa + 1.4, pulse_y - 14), (xa + 4.4, pulse_y - 14), (xa + 4.4, pulse_y)]
    pts.append((px0 + 46 * pitch, pulse_y))
    d.line(*pts)
    d.group('mid')
    _span(d, px0, px0 + 18 * pitch, pulse_y + 12)
    _span(d, x0, x1, y - r - 10)
    # labels
    d.group()
    d.text(200, y - r - 14, 'ABOUT 5 FT OF MERCURY', size=7)
    d.text(x0 + 2, y + r + 16, 'QUARTZ', size=7)
    d.text(x1 - 2, y + r + 16, 'QUARTZ', size=7)
    for bx, name in boxes:
        d.text(bx, ly + 3, name, size=7)
    d.text(218, ly + 44, 'CLOCK 500 kHz', size=7)
    d.text(112, ly + 44, 'IN', size=7, anchor='end')
    d.text(154, ly + 44, 'OUT', size=7, anchor='start')
    d.text(px0 + 12 * pitch, pulse_y + 24, 'ONE WORD: 17 DIGITS + 1 GAP', size=7)
    d.text(368, pulse_y - 4, '… × 32', size=8)
    d.text(200, 26, '32 WORDS × 18 DIGIT PERIODS = 576 · 1.152 ms A LAP', size=8)
    return d


def univac():
    """UNISERVO tape: blocks of 720 digits in about 6 inches with 2.5-inch gaps, and a close-up of
    eight digits across the tape's eight channels: excess-3 numeric bits, zone bits (00 for a
    digit), an odd check pulse and the sprocket. The digits are the 9:15 prediction, 32915049."""
    d = D()
    # the tape at full length: block, gap, block, at 30 px to the inch
    s = 30
    ty, th = 54, 16
    xa = 20
    b1 = (xa, xa + 6 * s)
    g = (b1[1], b1[1] + 2.5 * s)
    b2 = (g[1], g[1] + 6 * s)
    d.group('thin')
    d.lines([[(x, ty - 18), (x, ty + th + 18)] for x in (b1[0], b1[1], g[1])])
    d.group()
    d.line((xa - 8, ty), (400, ty))
    d.line((xa - 8, ty + th), (400, ty + th))
    d.group('mid')
    for lo, hi in (b1, (b2[0], 396)):
        d.lines([[(x, ty + 3), (x, ty + th - 3)] for x in [lo + 2 + 3.2 * k for k in range(int((hi - lo - 2) / 3.2))]])
    _span(d, b1[0], b1[1], ty - 10)
    _span(d, g[0], g[1], ty - 10)
    # the close-up: eight digit columns across eight channels
    digits = '32915049'
    rows = ['SPROCKET', 'CHECK', 'ZONE', 'ZONE', '8', '4', '2', '1']
    cx0, cy0, cp, rp = 118, 116, 30, 17
    d.group('thin')
    d.lines([[(cx0 - 14, cy0 + j * rp), (cx0 + 7 * cp + 14, cy0 + j * rp)] for j in range(8)])
    d.lines([[(cx0 + i * cp, cy0 - 12), (cx0 + i * cp, cy0 + 7 * rp + 8)] for i in range(8)])
    # the magnified strip, and leader lines back to the block it came from
    d.line((b1[0] + 40, ty + th), (cx0 - 24, cy0 - 20))
    d.line((b1[0] + 52, ty + th), (cx0 + 7 * cp + 24, cy0 - 20))
    d.group()
    d.line((cx0 - 24, cy0 - 20), (cx0 + 7 * cp + 24, cy0 - 20), (cx0 + 7 * cp + 24, cy0 + 7 * rp + 12),
           (cx0 - 24, cy0 + 7 * rp + 12), closed=True)
    d.group()
    for i, ch in enumerate(digits):
        v = int(ch) + 3                                # excess-3
        num = [(v >> k) & 1 for k in (3, 2, 1, 0)]     # 8 4 2 1
        zone = [0, 0]                                   # every digit has 00 zones
        check = 1 - (sum(num) + sum(zone)) % 2          # make the count of ones odd
        col = [1, check] + zone + num
        x = cx0 + i * cp
        for j, b in enumerate(col):
            if b:
                d.line((x - 5, cy0 + j * rp - 3), (x + 5, cy0 + j * rp - 3), (x + 5, cy0 + j * rp + 3),
                       (x - 5, cy0 + j * rp + 3), closed=True)
    d.group()
    for j, name in enumerate(rows):
        d.text(cx0 - 30, cy0 + j * rp + 3, name, size=7, anchor='end')
    for i, ch in enumerate(digits):
        d.text(cx0 + i * cp, cy0 + 7 * rp + 26, ch, size=9)
    d.text((b1[0] + b1[1]) / 2, ty - 14, '720 DIGITS · ≈6 IN', size=7)
    d.text((g[0] + g[1]) / 2, ty - 14, '2.5 IN', size=7)
    d.text(200, 22, 'UNISERVO TAPE · 128 DIGITS TO THE INCH', size=8)
    d.text(200, 286, 'EXCESS-3 · ODD CHECK · 9:15 PM, 4 NOV 1952', size=7)
    return d


def whirlwind():
    """A 4 × 4 core plane with its X, Y, inhibit and diagonal sense wires; the core at X1, Y2 is
    selected by two half currents; beside it the square hysteresis loop, where I/2 stays on the
    flat and only I reaches the knee."""
    d = D()
    n, x0, y0, p = 4, 40, 64, 42
    cores = [(x0 + i * p, y0 + j * p) for j in range(n) for i in range(n)]
    sel = (2, 1)
    # construction: the grid the cores sit on
    d.group('thin')
    d.lines([[(cx - 12, cy - 12), (cx + 12, cy + 12)] for cx, cy in cores])
    # X wires (rows) and Y wires (columns)
    d.group('mid')
    d.lines([[(x0 - 22, y0 + j * p), (x0 + (n - 1) * p + 22, y0 + j * p)] for j in range(n)])
    d.lines([[(x0 + i * p, y0 - 22), (x0 + i * p, y0 + (n - 1) * p + 22)] for i in range(n)])
    # the cores, each a ring at 45° threaded by its X and Y wires
    d.group()
    for (cx, cy) in cores:
        pts = []
        a = math.radians(45)
        for k in range(0, 361, 15):
            t = math.radians(k)
            ex, ey = 9 * math.cos(t), 3.6 * math.sin(t)
            pts.append((cx + ex * math.cos(a) - ey * math.sin(a), cy + ex * math.sin(a) + ey * math.cos(a)))
        d.line(*pts)
    # the sense wire, diagonal through every core, and the inhibit wire, parallel to the X wires
    d.group('mid')
    sense = []
    for j in range(n):
        row = [(x0 - 18, y0 + j * p + 4)] + [(x0 + i * p, y0 + j * p) for i in range(n)] + [(x0 + (n - 1) * p + 18, y0 + j * p - 4)]
        sense += row if j % 2 == 0 else row[::-1]
    d.line(*sense)
    d.lines([[(x0 - 22, y0 + j * p + 7), (x0 + (n - 1) * p + 22, y0 + j * p + 7)] for j in range(n)])
    # the selected core, ringed, with its half currents
    d.group()
    sx, sy = x0 + sel[0] * p, y0 + sel[1] * p
    d.circle(sx, sy, 13)
    _arrow(d, x0 - 10, sy, 0, 5)
    _arrow(d, sx, y0 - 10, math.pi / 2, 5)
    # the hysteresis loop: H across, B up, square
    hx, hy, hw, hh = 312, 150, 62, 50
    d.group('thin')
    d.line((hx - hw - 12, hy), (hx + hw + 12, hy))
    d.line((hx, hy - hh - 16), (hx, hy + hh + 16))
    d.lines([[(hx + s * hw * 0.5, hy - 6), (hx + s * hw * 0.5, hy + 6)] for s in (-1, 1)])
    d.lines([[(hx + s * hw, hy - hh - 8), (hx + s * hw, hy + hh + 8)] for s in (-1, 1)])
    d.group()
    kx = hw * 0.75                                   # the coercive field, between I/2 and I
    d.line((hx - hw - 8, hy + hh), (hx + kx, hy + hh), (hx + kx + 4, hy - hh), (hx + hw + 8, hy - hh))
    d.line((hx + hw + 8, hy - hh), (hx - kx, hy - hh), (hx - kx - 4, hy + hh), (hx - hw - 8, hy + hh))
    d.group('mid')
    d.circle(hx, hy - hh, 2.5)
    d.circle(hx, hy + hh, 2.5)
    # labels
    d.group()
    for j in range(n):
        d.text(x0 - 28, y0 + j * p + 3, f'X{j}', size=7, anchor='end')
    for i in range(n):
        d.text(x0 + i * p, y0 + (n - 1) * p + 34, f'Y{i}', size=7)
    d.text(x0 - 10, sy - 8, 'I/2', size=7)
    d.text(sx + 10, y0 - 16, 'I/2', size=7, anchor='start')
    d.text(x0 + (n - 1) * p + 26, y0 + 3 * p - 6, 'S', size=7, anchor='start')
    d.text(x0 + (n - 1) * p + 26, y0 + 3 * p + 10, 'Z', size=7, anchor='start')
    d.text(hx + 6, hy - hh - 8, '1', size=8, anchor='start')
    d.text(hx + 6, hy + hh + 14, '0', size=8, anchor='start')
    d.text(hx + hw * 0.5, hy + 16, 'I/2', size=7)
    d.text(hx + hw, hy + hh + 22, 'I', size=7)
    d.text(hx + hw + 12, hy - 4, 'H', size=7, anchor='start')
    d.text(hx - 4, hy - hh - 18, 'B', size=7, anchor='end')
    d.text(200, 22, 'COINCIDENT CURRENT · ONE CORE IN SIXTEEN FLIPS', size=8)
    d.text(200, 286, 'X, Y DRIVE · S SENSE · Z INHIBIT', size=7)
    return d


PLATES = {'manchester-baby': manchester_baby, 'edsac': edsac, 'univac': univac, 'whirlwind': whirlwind}
