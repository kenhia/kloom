"""Plates for Sound and Score's part machine3 (sprint 058): electrical recording, magnetic tape and
the long-playing record. See plates_for.py."""
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


def electrical_recording():
    d = D()
    # Above: the Western Electric recording chain of 1925 as a flow, from Maxfield and Harrison
    # (1926): condenser transmitter, valve amplifier, electromagnetic recorder, wax. Below: the band
    # each stage of the story could carry, on a log axis of frequency: the acoustic horn (about
    # 100-2,500 Hz, Library of Congress), the electrical system (60-6,000 Hz, Maxfield and Harrison),
    # the Orthophonic Victrola (100-5,000 Hz, New York Times 1925), and the 16-10,000 Hz they wanted.
    cy = 74
    # stage centres
    xs = [52, 148, 248, 344]

    d.group('thin')
    d.line((20, cy), (380, cy))                                   # the signal's axis
    x0, x1 = 60, 370                                               # log axis 10 Hz .. 20 kHz
    def fx(hz):
        return x0 + (math.log10(hz) - 1) / (math.log10(20000) - 1) * (x1 - x0)
    ax = 268
    for hz in (10, 100, 1000, 10000):
        d.line((fx(hz), 150), (fx(hz), ax + 4))
    for dec in (10, 100, 1000):
        for m in range(2, 10):
            if dec * m <= 20000:
                d.line((fx(dec * m), ax), (fx(dec * m), ax + 2.5))

    d.group()
    # 1 condenser microphone: a stretched diaphragm close to a fixed back plate, in section
    mx = xs[0]
    _box(d, mx - 16, cy - 26, 32, 52)
    d.line((mx - 9, cy - 20), (mx - 9, cy + 20))                   # diaphragm
    d.line((mx - 4, cy - 18), (mx - 4, cy + 18))                   # back plate
    # 2 amplifier: a box holding a triode
    ax2 = xs[1]
    _box(d, ax2 - 24, cy - 26, 48, 52)
    d.circle(ax2, cy, 14)
    d.line((ax2 - 7, cy + 8), (ax2 + 7, cy + 8))                   # cathode
    d.dashed((ax2 - 9, cy), (ax2 + 9, cy), dash=2, gap=2)          # grid
    d.line((ax2 - 7, cy - 8), (ax2 + 7, cy - 8))                   # plate
    # 3 the electromagnetic recorder: magnet poles, armature, and the stylus down to the wax
    rx = xs[2]
    _box(d, rx - 24, cy - 26, 48, 40)
    d.line((rx - 16, cy - 18), (rx - 16, cy + 6), (rx - 6, cy + 6))
    d.line((rx + 16, cy - 18), (rx + 16, cy + 6), (rx + 6, cy + 6))
    d.line((rx, cy - 12), (rx, cy + 30))                            # armature and stylus
    d.line((rx - 3, cy + 26), (rx, cy + 32), (rx + 3, cy + 26))
    # 4 the wax master, edge-on, with the stylus's groove
    wx = xs[3]
    d.ellipse(wx, cy + 10, 34, 9)
    d.line((wx - 34, cy + 10), (wx - 34, cy + 16))
    d.line((wx + 34, cy + 10), (wx + 34, cy + 16))
    d.arc(wx, cy + 16, 34, 0, 180, ry=9)

    d.group('mid')
    for a, b in ((xs[0] + 16, xs[1] - 24), (xs[1] + 24, xs[2] - 24)):
        d.line((a + 3, cy), (b - 3, cy))
        _arrow(d, (a, cy), (b - 3, cy))
    d.line((rx + 4, cy + 30), (wx - 38, cy + 14))
    _arrow(d, (rx + 4, cy + 30), (wx - 38, cy + 14), 4)
    for i in range(3):                                              # coil turns on the poles
        for sx in (-16, 16):
            d.line((rx + sx - 4, cy - 14 + i * 6), (rx + sx + 4, cy - 10 + i * 6))
    for k in range(1, 4):                                           # grooves on the wax
        d.arc(wx, cy + 10, 34 - k * 7, 0, 360, ry=9 - k * 1.9)

    # the bands
    d.group()
    rows = [
        (100, 2500, 'ACOUSTIC HORN', False),
        (60, 6000, 'WESTERN ELECTRIC, 1925', False),
        (100, 5000, 'ORTHOPHONIC VICTROLA', False),
        (16, 10000, 'WANTED: 16-10,000 HZ', True),
    ]
    ys = [172, 196, 220, 244]
    for (lo, hi, _, dash), y in zip(rows, ys):
        if dash:
            d.dashed((fx(lo), y), (fx(hi), y), dash=4, gap=3)
        else:
            d.line((fx(lo), y - 4), (fx(hi), y - 4), (fx(hi), y + 4), (fx(lo), y + 4), closed=True)
    d.line((x0, ax), (x1, ax))

    d.group('mid')
    d.text(xs[0], cy - 34, 'MICROPHONE', size=7)
    d.text(xs[1], cy - 34, 'VALVE AMPLIFIER', size=7)
    d.text(xs[2], cy - 34, 'CUTTER', size=7)
    d.text(xs[3], cy - 34, 'WAX MASTER', size=7)
    for (lo, hi, lab, dash), y in zip(rows, ys):
        if dash:
            d.text((fx(lo) + fx(hi)) / 2, y - 5, lab, size=7)
        elif fx(hi) < 300:
            d.text(fx(hi) + 5, y + 2.5, lab, size=7, anchor='start')
        else:
            d.text(fx(lo) - 5, y + 2.5, lab, size=7, anchor='end')
    for hz, lab in ((10, '10'), (100, '100'), (1000, '1,000'), (10000, '10,000 HZ')):
        d.text(fx(hz), ax + 14, lab, size=7)
    d.text(200, 292, 'THE WESTERN ELECTRIC CHAIN · BANDS ON A LOG SCALE', size=7)
    return d


PLATES = {
    'electrical-recording': electrical_recording,
}


def magnetic_tape():
    d = D()
    # A ring head in section over a moving tape, after the ring head Eduard Schueller patented in
    # 1933 (Engel and Hammar): a core of magnetic metal with a coil and a narrow gap at its foot, the
    # tape's oxide coat on its plastic base passing beneath, and the magnetization the gap leaves
    # behind as arrows whose length follows the signal. Proportions are schematic: a real gap is a few
    # micrometers and the coat 20. Above left, the current in the coil with bias: a slow audio wave
    # with the fast bias tone added to it, as Weber found in 1940.
    cx, cy, ro, ri = 200, 104, 52, 34
    gap = 5                                         # half-angle of the gap, degrees
    tape_y = cy + ro + 2                            # top of the oxide
    ox, base = 14, 12

    d.group('thin')
    d.line((cx, cy - ro - 14), (cx, tape_y + ox + base + 10))           # centre line through the gap
    for k in range(3):                                                  # the fringe field out of the gap
        r = 7 + k * 6
        d.arc(cx, tape_y - 2, r, 0, 180, ry=r * 0.8)
    # the bias inset's axes
    bx0, bx1, by = 24, 128, 44
    d.line((bx0, by), (bx1, by))
    d.line((bx0, by - 22), (bx0, by + 22))

    d.group()
    # the ring core: outer and inner arcs, broken at the gap at the foot (90 degrees is straight down)
    d.arc(cx, cy, ro, 90 + gap, 450 - gap)
    d.arc(cx, cy, ri, 90 + gap * 1.6, 450 - gap * 1.6)
    for s in (-1, 1):
        a_o = math.radians(90 + s * gap)
        a_i = math.radians(90 + s * gap * 1.6)
        d.line((cx + ro * math.cos(a_o), cy + ro * math.sin(a_o)), (cx + ri * math.cos(a_i), cy + ri * math.sin(a_i)))
    # the tape: oxide coat over the base
    d.line((16, tape_y), (384, tape_y))
    d.line((16, tape_y + ox), (384, tape_y + ox))
    d.line((16, tape_y + ox + base), (384, tape_y + ox + base))

    d.group('mid')
    # the coil wound round the top of the core
    for i in range(9):
        a = math.radians(225 + i * 10)
        p = (cx + (ro + 3) * math.cos(a), cy + (ro + 3) * math.sin(a))
        q = (cx + (ri - 3) * math.cos(a + 0.06), cy + (ri - 3) * math.sin(a + 0.06))
        d.line(p, q)
    # the recorded magnetization, right of the gap (the tape runs left to right)
    lam = 56
    for i in range(24):
        x = cx + 10 + i * 7.5
        if x > 378:
            break
        m = math.sin(2 * math.pi * (x - cx - 10) / lam)
        L = 9 * m
        if abs(L) < 1.5:
            continue
        y = tape_y + ox / 2
        d.line((x - L / 2, y), (x + L / 2, y))
        _arrow(d, (x - L / 2, y), (x + L / 2, y), 2.6)
    # the unrecorded oxide, left of the gap: short random-looking dashes for the grains
    for i in range(18):
        x = 24 + i * 9
        if x > cx - 12:
            break
        d.line((x, tape_y + ox / 2 + (1.5 if i % 2 else -1.5)), (x + 2.5, tape_y + ox / 2 + (1.5 if i % 2 else -1.5)))
    # motion arrow under the tape
    ym = tape_y + ox + base + 16
    # below: the magnetization left in the coat, as a curve under the arrows
    py = 252
    d.line((cx + 10, py), (380, py), cls=None)
    mp = [(x, py - 14 * math.sin(2 * math.pi * (x - cx - 10) / lam)) for x in [cx + 10 + k for k in range(0, 171)]]
    d.line(*mp)
    for k in range(4):
        xx = cx + 10 + lam / 4 + k * lam / 2
        d.dashed((xx, tape_y + ox + base + 2), (xx, py - 14 * math.sin(2 * math.pi * (xx - cx - 10) / lam) - 2 * (1 if k % 2 == 0 else -1)), dash=2, gap=3)
    d.line((60, ym), (150, ym))
    _arrow(d, (60, ym), (150, ym))
    # the bias inset: audio plus bias
    pts = []
    for i in range(301):
        t = i / 300
        v = 9 * math.sin(2 * math.pi * 1.5 * t) + 9 * math.sin(2 * math.pi * 22 * t)
        pts.append((bx0 + 4 + t * (bx1 - bx0 - 8), by - v))
    d.line(*pts)

    d.group('mid')
    d.text(cx + ro + 10, cy - 30, 'COIL', size=7, anchor='start')
    d.text(cx + ro + 10, cy + 10, 'CORE', size=7, anchor='start')
    d.text(cx + 14, tape_y - 14, 'GAP', size=7, anchor='start')
    d.text(380, tape_y - 4, 'IRON OXIDE', size=7, anchor='end')
    d.text(380, tape_y + ox + base + 9, 'PLASTIC BASE', size=7, anchor='end')
    d.text(20, tape_y + ox + base + 9, 'UNRECORDED', size=7, anchor='start')
    d.text(105, ym + 14, 'TAPE MOTION', size=7)
    d.text((bx0 + bx1) / 2, by + 34, 'SIGNAL + BIAS IN THE COIL', size=7)
    d.text(cx + 4, py + 4, 'MAGNETIZATION', size=7, anchor='end')
    d.text(200, 292, 'RING HEAD AND TAPE IN SECTION · SCHEMATIC', size=7)
    return d


PLATES['magnetic-tape'] = magnetic_tape


def long_playing_record():
    d = D()
    # Grooves in cross-section, a 78 above an LP at one scale (4 units a thousandth of an inch):
    # pitches from Radio-Electronics, October 1948 (about 90 grooves an inch against 224-300; 260
    # drawn), stylus tips of 0.003 and 0.001 inch (the article's "1 to 3"). The grooves are drawn as
    # 90-degree V's whose width is a third of the pitch's share each way, schematic. Below, Blumlein's
    # stereo groove of 1931 enlarged: each wall at 45 degrees carries one channel, so motion in step
    # moves the stylus sideways and motion against it moves it up and down.
    k = 4.0                                   # units per mil
    x0, x1 = 30, 250

    def grooves(y, pitch_mil, width_mil, tip_mil, n_max):
        p, w = pitch_mil * k, width_mil * k
        h = w / 2                              # a 90-degree V is half as deep as it is wide
        pts = [(x0, y)]
        x = x0 + p / 2
        centres = []
        while x + w / 2 < x1 and len(centres) < n_max:
            pts += [(x - w / 2, y), (x, y + h), (x + w / 2, y)]
            centres.append(x)
            x += p
        pts.append((x1, y))
        d.line(*pts)
        return centres, h

    y78, ylp = 90, 182
    d.group('thin')
    for y in (y78, ylp):
        d.line((x0 - 6, y + 22), (x1 + 6, y + 22))                     # the disc's body, schematic
    c78p = 1000 / 90
    clpp = 1000 / 260
    for xx in (x0 + c78p * k * 2.5, x0 + c78p * k * 3.5):
        d.line((xx, y78 - 18), (xx, y78 - 8))
    for xx in (x0 + clpp * k * 6.5, x0 + clpp * k * 7.5):
        d.line((xx, ylp - 18), (xx, ylp - 8))

    d.group()
    c78, h78 = grooves(y78, c78p, 9, 3, 9)
    clp, hlp = grooves(ylp, clpp, 3, 1, 40)

    d.group('mid')
    # the styli resting in one groove each, tips as circles touching both walls
    for (cs, h, r) in ((c78, h78, 3 * k), (clp, hlp, 1 * k)):
        cx = cs[1]
        yb = (y78 if cs is c78 else ylp)
        cy = yb + h - r * math.sqrt(2) + 0.0
        d.circle(cx, cy, r)
        d.line((cx - r * 0.9, cy - r * 0.4), (cx - r * 1.4, yb - 30), (cx + r * 1.4, yb - 30), (cx + r * 0.9, cy - r * 0.4))
    # pitch dimension marks
    for (y, p) in ((y78, c78p), (ylp, clpp)):
        a, b = (x0 + p * k * 2.5, x0 + p * k * 3.5) if y == y78 else (x0 + p * k * 6.5, x0 + p * k * 7.5)
        d.line((a, y - 13), (b, y - 13))

    # the stereo groove, enlarged
    sx, sy, s = 330, 140, 40
    d.group('thin')
    d.line((sx, sy - 44), (sx, sy + s + 10))                         # the normal
    d.line((sx - s - 8, sy), (sx + s + 8, sy))                       # the record's surface
    d.group()
    d.line((sx - s - 8, sy), (sx - s, sy), (sx, sy + s), (sx + s, sy), (sx + s + 8, sy))
    d.group('mid')
    for sgn in (-1, 1):                                              # each wall's motion, normal to it
        mx, my = sx + sgn * s / 2, sy + s / 2
        nx, ny = -sgn * math.sqrt(0.5), -math.sqrt(0.5)
        a, b = (mx - nx * 14, my - ny * 14), (mx + nx * 14, my + ny * 14)
        d.line(a, b)
        _arrow(d, a, b, 4)
        _arrow(d, b, a, 4)
    # in step: sideways; against: up and down
    d.line((sx - 22, sy + s + 22), (sx + 22, sy + s + 22))
    _arrow(d, (sx, sy + s + 22), (sx + 22, sy + s + 22), 4)
    _arrow(d, (sx, sy + s + 22), (sx - 22, sy + s + 22), 4)

    d.group('mid')
    d.text(x0, y78 - 34, '78 RPM · ABOUT 90 GROOVES AN INCH · TIP 0.003 IN', size=7, anchor='start')
    d.text(x0, ylp - 34, 'LP · 224-300 GROOVES AN INCH · TIP 0.001 IN', size=7, anchor='start')
    d.text(sx - s / 2 - 16, sy + s / 2 + 18, 'L', size=7)
    d.text(sx + s / 2 + 16, sy + s / 2 + 18, 'R', size=7)
    d.text(x0 + c78p * k * 3, y78 - 22, 'PITCH', size=7)
    d.text(sx, sy - 52, 'STEREO, 45/45', size=7)
    d.text(sx, sy + s + 36, 'L+R SIDEWAYS', size=7)
    d.text(sx, sy + s + 46, 'L-R UP AND DOWN', size=7)
    d.text(140, 240, 'ONE SCALE: 4 UNITS = 0.001 INCH', size=7)
    d.text(200, 292, 'GROOVES IN SECTION · WIDTHS SCHEMATIC', size=7)
    return d


PLATES['long-playing-record'] = long_playing_record
