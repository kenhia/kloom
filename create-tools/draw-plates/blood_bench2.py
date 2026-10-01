"""Plates for In the Blood's bench segment, second half: coulter, autoanalyzer, lis, gel-card
(sprint 028). See plates_for.py."""
import math
from plates import D


def _pt(cx, cy, r, a):
    """The point at `a` degrees on a circle (clockwise from +x; SVG's y runs down)."""
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _pulse(x0, base, h, w=5.0, n=14):
    """A pulse as a Gaussian bump of height h centred at x0, rising above the baseline `base`."""
    pts = []
    for i in range(n + 1):
        x = x0 - 2.6 * w + 5.2 * w * i / n
        pts.append((x, base - h * math.exp(-((x - x0) / w) ** 2)))
    return pts


def coulter():
    d = D()
    # The aperture in section, to scale at 0.9 px per micrometre: Coulter's standard orifice of
    # 1956 was 1/10 mm across and about 1/15 mm long (Coulter 1956, p. 1036); the production
    # jewel was 75-80 um long (Graham 2020). Drawn 100 um by 75 um. Red cells about 7.5 um
    # across. Below, the pulse train: height proportional to the volume swept out; one
    # coincidence (two cells at once) makes a single taller pulse. Pulse heights are invented.
    s = 0.9
    cx, cy = 150, 105
    dia, ln = 100 * s, 75 * s
    x0, x1 = cx - ln / 2, cx + ln / 2
    y0, y1 = cy - dia / 2, cy + dia / 2
    d.group('thin')
    d.line((20, cy), (300, cy))                                     # the aperture's axis
    # current lines converging on the orifice from either side (from points on a half circle)
    for a in range(-50, 51, 25):
        for side in (-1, 1):
            ex = x0 if side < 0 else x1
            p = _pt(ex, cy, 66, 180 + a if side < 0 else -a)
            q = (ex, cy - (dia / 2 - 6) * math.sin(math.radians(a)))
            d.line(p, q)
    # dimension lines: the diameter and the length
    d.line((x1 + 4, y0), (x1 + 136, y0))
    d.line((x1 + 4, y1), (x1 + 136, y1))
    d.line((x1 + 128, y0), (x1 + 128, y1))
    d.line((x0, y1 + 30), (x0, y1 + 46))
    d.line((x1, y1 + 30), (x1, y1 + 46))
    d.line((x0, y1 + 40), (x1, y1 + 40))
    d.group()
    # the wall of the aperture tube (glass or a ruby jewel), cut through: above and below the bore
    d.line((x0, 36), (x0, y0), (x1, y0), (x1, 36))
    d.line((x0, 196), (x0, y1), (x1, y1), (x1, 196))
    # the two electrodes: one in the beaker outside, one inside the tube
    d.line((34, 40), (34, 170))
    d.line((266, 40), (266, 170))
    d.line((34, 40), (34, 24), (266, 24), (266, 40))                 # the circuit over the top
    d.group('mid')
    # hatching in the cut wall
    for yb, ye in ((36, y0), (y1, 196)):                            # 45-degree hatching, clipped
        for k in range(-80, 80, 9):
            a, b = (x0, yb + k), (x1, yb + k - ln)
            pts = []
            for t in [i / 40 for i in range(41)]:
                x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                if yb < y < ye:
                    pts.append((x, y))
            if len(pts) > 1:
                d.line(pts[0], pts[-1])
    # cells drawn on the axis's neighbourhood, edge-on discs, moving left to right
    for (x, y) in ((58, 92), (78, 120), (96, 101), (128, 108), (214, 98), (240, 116)):
        d.ellipse(x, y, 3.4, 1.6)
    d.ellipse(cx, cy - 4, 3.4, 1.6)                                # the cell in the orifice now
    _arrow(d, (40, 150), (60, 150))
    d.line((40, 150), (60, 150))
    _arrow(d, (236, 150), (256, 150))
    d.line((236, 150), (256, 150))
    # the battery and meter in the circuit, as a gap with two plates
    d.line((146, 18), (146, 30))
    d.line((154, 21), (154, 27))
    # the pulse train
    base = 278
    d.line((20, base), (380, base))
    hs = [30, 26, 34, 22, 28, 58, 31, 25, 29]                       # invented heights; the 6th is two cells
    for i, h in enumerate(hs):
        d.line(*_pulse(40 + i * 34, base, h))
    d.group('thin')
    d.line((20, base - 18), (380, base - 18))                       # the threshold
    d.group('mid')
    d.text(x1 + 134, cy + 3, '100 µm', size=7, anchor='start')
    d.text(cx, y1 + 56, '75 µm', size=7)
    d.text(34, 186, '−', size=9)
    d.text(266, 186, '+', size=9)
    d.text(40, 60, 'SALINE', size=7, anchor='start')
    d.text(330, 222, '≈ 3,300 CELLS/S', size=7)
    d.text(384, base - 21, 'THRESHOLD', size=7, anchor='end')
    d.text(210, base - 64, 'TWO AT ONCE', size=7)
    return d


def _coil(d, x, y, w, h, turns):
    """A mixing coil seen from the side: a helix of `turns` turns, w long and h high."""
    pts = []
    n = turns * 24
    for i in range(n + 1):
        t = 2 * math.pi * turns * i / n
        pts.append((x + w * i / n + 3 * math.sin(t), y + h / 2 * math.cos(t)))
    d.line(*pts)


def autoanalyzer():
    d = D()
    # Skeggs's flow diagram for blood urea (Clinical Chemistry 2000, Fig. 8): sample and urease
    # pumped through a mixing coil in a warm bath; the stream passes the dialyser and goes to
    # waste; the ammonia crosses the membrane into a stream of water segmented by air, which is
    # mixed with Nessler's reagent, debubbled and read in the colorimeter's flow cell; the
    # recorder draws a plateau for each sample. Not to scale.
    d.group('thin')
    for x in range(20, 381, 40):                                     # a drafting grid
        d.line((x, 18), (x, 282))
    for y in range(18, 283, 44):
        d.line((20, y), (380, y))
    d.group()
    # the proportioning pump: a platen and rollers pressing the tubes
    px, py = 30, 40
    d.line((px, py), (px + 60, py), (px + 60, py + 100), (px, py + 100), closed=True)
    for i in range(5):
        d.circle(px + 12 + i * 9, py + 50, 3)
    # four tubes through the pump: sample, urease, air, water
    ys = [py + 18, py + 38, py + 62, py + 82]
    for y in ys:
        d.line((14, y), (px + 74, y))
    # the warm bath with its coil (sample + urease)
    d.line((110, 30), (190, 30), (190, 90), (110, 90), closed=True)
    d.line((px + 74, ys[0]), (100, ys[0]), (100, 54), (114, 54))
    d.line((px + 74, ys[1]), (100, ys[1]), (100, 54))
    _coil(d, 114, 60, 64, 22, 8)
    # the dialyser: two channels with a membrane between them
    d.line((210, 120), (300, 120), (300, 168), (210, 168), closed=True)
    d.line((178, 60), (200, 60), (200, 132), (210, 132), (290, 132), (318, 132), (330, 110))  # donor channel, to waste
    d.line((px + 74, ys[2]), (100, ys[2]), (100, 156))
    d.line((px + 74, ys[3]), (96, ys[3]), (96, 156))
    d.line((96, 156), (210, 156), (300, 156), (318, 156), (318, 206))                          # recipient channel
    # Nessler's reagent joining, a second coil, the debubbler, the flow cell
    d.line((250, 206), (318, 206))
    _coil(d, 210, 230, 70, 18, 7)
    d.line((318, 206), (318, 230), (280, 230))
    d.line((210, 230), (196, 230), (196, 262), (226, 262))
    d.line((226, 262), (226, 250), (256, 250), (256, 274), (226, 274), (226, 262))           # the flow cell
    d.group('mid')
    # the membrane, dashed
    for x in range(212, 300, 8):
        d.line((x, 144), (x + 4, 144))
    # air bubbles segmenting the recipient stream
    for x in range(110, 205, 14):
        d.ellipse(x, 156, 4, 2.2)
    # the colorimeter's light path through the flow cell, and the recorder's plateaus
    d.line((214, 262), (222, 262))
    d.line((260, 262), (270, 262))
    base, rx = 282, 290
    trace = [(rx, base)]
    for k, h in enumerate((10, 22, 34, 22, 10)):
        x = rx + k * 18
        trace += [(x + 3, base - h), (x + 12, base - h), (x + 15, base)]
    d.line(*trace)
    _arrow(d, (318, 132), (330, 110))
    _arrow(d, (318, 190), (318, 206))
    _arrow(d, (14, ys[0]), (24, ys[0]))
    d.group('mid')
    d.text(60, 152, 'PUMP', size=7)
    d.text(150, 24, 'UREASE BATH', size=7)
    d.text(10, ys[0] - 6, 'SAMPLE', size=7, anchor='start')
    d.text(10, ys[2] - 6, 'AIR', size=7, anchor='start')
    d.text(10, ys[3] - 6, 'WATER', size=7, anchor='start')
    d.text(255, 116, 'DIALYSER', size=7)
    d.text(338, 104, 'WASTE', size=7, anchor='start')
    d.text(250, 202, 'NESSLER', size=7, anchor='end')
    d.text(241, 288, 'FLOW CELL', size=7)
    d.text(334, 236, 'RECORDER', size=7)
    return d


# ISBT 128 Donation Identification Number data structure 001, "=G12341765432100": the
# specification's own worked example DIN, G1234 17 654321 (ISBT 128 Technical Specification
# v6.2.2, Appendix A), with flag characters 00. Encoded as Code 128 (start B, "=G", code C,
# 12 34 17 65 43 21 00, check, stop); the modules were generated with python-barcode in a
# scratch script and are kept here so that this module needs only the standard library.
_DIN_MODULES = ('11010010000111001100101101000100010111011110101100111001000101100010011100'
                '11010010110000101100011101101110010011011001100100101100001100011101011')


def _iso7064_k(din):
    """The ISBT 128 keyboard check character K: ISO 7064 mod 37-2 over the 13 characters."""
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ*'
    total = sum(chars.index(c) * 2 ** (len(din) - i) for i, c in enumerate(din))
    return chars[(38 - total % 37) % 37]


def lis():
    d = D()
    # A donation identification number as an ISBT 128 label prints it: the Code 128 symbol,
    # its eye-readable characters split into facility, year and serial, and the boxed keyboard
    # check character K. The modules are the real encoding of the specification's example.
    din = 'G123417654321'
    k = _iso7064_k(din)                                              # 'A', as Appendix A works it
    mods = _DIN_MODULES
    x0, top, bot = 54, 70, 150
    m = 2.0                                                          # one module, in px
    width = len(mods) * m
    d.group('thin')
    d.line((x0 - 20, top - 20), (x0 + width + 20, top - 20), (x0 + width + 20, 230), (x0 - 20, 230), closed=True)
    d.line((x0, top - 28), (x0, bot + 8))                            # quiet zone either side
    d.line((x0 + width, top - 28), (x0 + width, bot + 8))
    # every eleventh module: one Code 128 symbol character
    for i in range(0, len(mods) - 12, 11):
        d.line((x0 + i * m, bot + 4), (x0 + i * m, bot + 12))
    d.line((x0, bot + 8), (x0 + width, bot + 8))
    d.group()
    # the bars: each run of 1s is one bar, drawn as vertical strokes a module apart
    segs = []
    i = 0
    while i < len(mods):
        if mods[i] == '1':
            j = i
            while j < len(mods) and mods[j] == '1':
                j += 1
            for q in range(i, j):
                x = x0 + (q + 0.5) * m
                segs.append([(x, top), (x, bot)])
            i = j
        else:
            i += 1
    d.lines(segs)
    # the boxed check character
    bx = x0 + width - 22
    d.line((bx, 184), (bx + 16, 184), (bx + 16, 204), (bx, 204), closed=True)
    d.group('mid')
    # brackets under the three fields of the printed number
    fx = [(x0 + 4, x0 + 92), (x0 + 104, x0 + 132), (x0 + 144, x0 + 250)]
    for a, b in fx:
        d.line((a, 214), (a, 220), (b, 220), (b, 214))
    d.group('mid')
    d.text(x0 + 48, 200, 'G1234', size=12)
    d.text(x0 + 118, 200, '17', size=12)
    d.text(x0 + 197, 200, '654321', size=12)
    d.text(bx + 8, 199, k, size=11)
    d.text(x0 + 48, 238, 'FACILITY', size=7)
    d.text(x0 + 118, 238, 'YEAR', size=7)
    d.text(x0 + 197, 238, 'SERIAL', size=7)
    d.text(bx + 8, 226, 'K', size=7)
    d.text(x0, top - 34, 'QUIET', size=7, anchor='start')
    d.text(x0 + width / 2, bot + 24, '11 MODULES A CHARACTER', size=7)
    d.text(200, 274, 'DATA: =G12341765432100', size=7)
    return d


def gel_card():
    d = D()
    # Six microtubes of a gel card in section after the spin, one for each reading grade as the
    # manufacturers' instructions describe them: 4+ a solid band on top of the gel, 3+ mostly in
    # the upper half, 2+ through the whole column, 1+ mostly in the lower half with a button,
    # 0 a button at the bottom, and mixed field (a band and a button). Not to scale.
    tops = [48 + 58 * i for i in range(6)]
    grades = ['4+', '3+', '2+', '1+', '0', 'MF']
    ytop, ycham, ygel, ybot = 40, 96, 120, 246
    rw, cw = 20, 7                                                   # half widths: chamber, column
    d.group('thin')
    d.line((20, ygel), (380, ygel))                                  # the top of the gel
    d.line((20, (ygel + ybot) / 2), (380, (ygel + ybot) / 2))         # half the column
    d.line((20, ybot), (380, ybot))
    d.group()
    for cx in tops:
        # the reaction chamber, a funnel, and the column with its rounded tip
        d.line((cx - rw, ytop), (cx - rw, ycham), (cx - cw, ycham + 16), (cx - cw, ybot - cw))
        d.arc(cx, ybot - cw, cw, 180, 0, n=12)
        d.line((cx + cw, ybot - cw), (cx + cw, ycham + 16), (cx + rw, ycham), (cx + rw, ytop))
    d.line((24, ytop - 6), (376, ytop - 6))                           # the card's top edge
    d.group('thin')
    for cx in tops:
        # the gel, stippled with short ticks
        for y in range(ygel + 6, ybot - 10, 10):
            d.line((cx - 3, y), (cx - 1, y))
            d.line((cx + 2, y + 5), (cx + 4, y + 5))
    # the red cells after the spin, by grade, at full weight
    d.group()
    def band(cx, y):
        for k in range(4):
            d.line((cx - cw + 1, y + 1.6 * k), (cx + cw - 1, y + 1.6 * k))
    def clumps(cx, y0, y1, n):
        for i in range(n):
            y = y0 + (y1 - y0) * (i + 0.5) / n
            d.circle(cx + (-2.5 if i % 2 else 2.5), y, 2)
    def button(cx):
        for r in (cw - 2, cw - 3.5, cw - 5):
            d.arc(cx, ybot - cw, r, 180, 0, n=10)
        d.line((cx - cw + 2, ybot - cw), (cx + cw - 2, ybot - cw))
    band(tops[0], ygel + 2)
    clumps(tops[1], ygel + 4, (ygel + ybot) / 2, 6)
    clumps(tops[2], ygel + 8, ybot - 12, 9)
    clumps(tops[3], (ygel + ybot) / 2, ybot - 14, 4)
    button(tops[3])
    button(tops[4])
    band(tops[5], ygel + 2)
    button(tops[5])
    # the liquid over the gel, and the centrifugal force down the column
    d.group('mid')
    for cx in tops:
        d.line((cx - cw, 108), (cx + cw, 108))
    d.line((392, 70), (392, 230))
    _arrow(d, (392, 70), (392, 230))
    d.group('mid')
    for cx, g in zip(tops, grades):
        d.text(cx, 270, g, size=9)
    d.text(16, ygel - 3, 'GEL', size=7, anchor='start')
    d.text(200, 26, '50 µL CELLS + 25 µL PLASMA · 37 °C · SPIN', size=7)
    d.text(392, 246, 'g', size=9)
    d.text(200, 290, 'AGGLUTINATED CELLS STAY HIGH; FREE CELLS SINK', size=7)
    return d


PLATES = {
    'coulter': coulter,
    'autoanalyzer': autoanalyzer,
    'lis': lis,
    'gel-card': gel_card,
}
