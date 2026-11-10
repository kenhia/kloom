"""Plates for Sound and Score's part digital2 (sprint 058): the compact disc and MIDI. See plates_for.py."""
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


def _stadium(d, x0, x1, y, r):
    """A pit seen from above: a slot of half-width r from x0 to x1, with round ends."""
    pts = []
    for i in range(13):
        a = math.radians(90 + 180 * i / 12)
        pts.append((x0 + r + r * math.cos(a), y + r * math.sin(a)))
    for i in range(13):
        a = math.radians(-90 + 180 * i / 12)
        pts.append((x1 - r + r * math.cos(a), y + r * math.sin(a)))
    d.line(*pts, closed=True)


def compact_disc():
    d = D()
    # Left: the 120 mm disc in plan at 0.9 px a mm: the 15 mm hole, the program area from 25 to
    # 58 mm radius, and a spiral drawn with a few schematic turns (the real one has about 20,600).
    # Right: a patch of the track magnified to 20 px a micrometer, from ECMA-130 and the Red Book's
    # numbers: track pitch 1.6, pit width 0.5, and pits and lands 3T to 11T long, where T, one
    # channel bit, is 1.2 m/s over 4.3218 MHz = 0.278 um. The laser spot is the Airy disc of
    # 780 nm light through a 0.45 lens, 2 x 0.61 x 0.78 / 0.45 = 2.1 um across to its first dark ring.
    cx, cy, k = 74, 124, 0.95
    T = 1.2 / 4.3218 * 20                         # px per channel bit
    s = 20                                        # px per um
    bx, by, bw, bh = 168, 58, 220, 132            # the magnified window
    tracks = [by + bh / 2 - 1.6 * s, by + bh / 2, by + bh / 2 + 1.6 * s]
    # run lengths, pit first then land, each 3T..11T (invented, as on any disc)
    runs = [
        [4, 3, 7, 5, 3, 4, 9, 3, 5, 6, 3, 8, 4, 3],
        [5, 4, 3, 3, 11, 4, 6, 3, 3, 5, 8, 3, 4, 6],
        [3, 6, 4, 8, 3, 3, 5, 4, 10, 3, 4, 5, 3, 7],
    ]
    offs = [30, 26, 34]
    spot_x = bx + 186
    probe = (cx + 42 * k, cy - 0.0)

    d.group('thin')
    d.line((cx - 64, cy), (cx + 64, cy)); d.line((cx, cy - 64), (cx, cy + 64))
    d.circle(cx, cy, 25 * k); d.circle(cx, cy, 58 * k)
    _box(d, bx, by, bw, bh)
    d.line((probe[0] + 4, probe[1] - 4), (bx, by)); d.line((probe[0] + 4, probe[1] + 4), (bx, by + bh))
    for y in tracks:
        d.line((bx, y), (bx + bw, y))

    d.group()
    d.circle(cx, cy, 60 * k)                                                   # rim
    d.circle(cx, cy, 7.5 * k)                                                  # the 15 mm hole
    sp = []                                                                    # schematic spiral, inside out
    for i in range(0, 721):
        a = math.radians(i * 3.0)
        r = (25 + (58 - 25) * i / 720) * k
        sp.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(*sp)
    _box(d, probe[0] - 4, probe[1] - 4, 8, 8)
    # the pits, clipped to whole pits inside the window
    for y, seq, off in zip(tracks, runs, offs):
        x = bx + off
        pit = True
        for n in seq:
            ln = n * T
            if pit and x + ln < bx + bw - 2:
                _stadium(d, x, x + ln, y, 0.25 * s)
            x += ln
            pit = not pit

    d.group('mid')
    d.circle(spot_x, tracks[1], 1.05 * s)                                     # Airy disc, first dark ring
    d.line((spot_x - 4, tracks[1]), (spot_x + 4, tracks[1])); d.line((spot_x, tracks[1] - 4), (spot_x, tracks[1] + 4))
    # dimensions: pitch at the right edge, a pit's width, a 3T and the 11T pit's length
    xr = bx + 12
    d.line((xr, tracks[1]), (xr, tracks[2])); d.line((xr - 3, tracks[1]), (xr + 3, tracks[1])); d.line((xr - 3, tracks[2]), (xr + 3, tracks[2]))
    # the read signal along the middle track: high over a pit, low over land; each edge is a 1
    y0, hi = by + bh + 22, 10
    x = bx + offs[1]
    sig = [(bx, y0)]
    pit = True
    for n in runs[1]:
        ln = n * T
        if x + ln > bx + bw:
            break
        lvl = y0 - hi if pit else y0
        sig += [(x, sig[-1][1]), (x, lvl), (x + ln, lvl)]
        x += ln
        pit = not pit
    sig.append((bx + bw, sig[-1][1]))
    d.line(*sig)
    # where the 11T pit is, for its dimension
    x11 = bx + offs[1] + sum(runs[1][:4]) * T
    yd = tracks[1] - 0.25 * s - 6
    d.line((x11, yd), (x11 + 11 * T, yd)); _arrow(d, (x11 + 8, yd), (x11, yd), 3); _arrow(d, (x11 + 11 * T - 8, yd), (x11 + 11 * T, yd), 3)

    d.group('mid')
    d.text(cx, cy + 76, '120 MM DISC', size=7)
    d.text(cx, cy - 72, 'PROGRAM AREA R 25-58 MM', size=7)
    d.text(x11 + 11 * T / 2, yd - 4, '11T = 3.05', size=7)
    d.text(xr + 5, (tracks[1] + tracks[2]) / 2 + 3, '1.6', size=7, anchor='start')
    d.text(spot_x, tracks[1] - 1.05 * s - 4, 'SPOT 780 NM', size=7)
    d.text(bx + bw / 2, by - 8, 'PITS 0.5 WIDE · 3T TO 11T LONG · MICRONS', size=7)
    d.text(bx, y0 + 14, 'READ SIGNAL · EACH EDGE A 1', size=7, anchor='start')
    d.text(200, 290, 'THE TRACK AT 1.2 M/S · ONE CHANNEL BIT T = 0.28 MICRON', size=7)
    return d


def midi():
    d = D()
    # Top: a MIDI socket, front view, at 6 px a mm: a 180-degree five-pin DIN (DIN 41524), its pins
    # on a 7 mm circle 45 degrees apart and numbered 3-5-2-4-1 across the socket's face (the plug,
    # facing it, reads 1-4-2-5-3). MIDI 1.0 uses pins 4 and 5 for the current loop and 2 for the
    # shield; 1 and 3 are unused. To its right the loop itself: 5 mA through the receiver's
    # opto-isolator. Bottom: one Note On, 90 3C 40 (channel 1, key 60, velocity 64), as it goes
    # down the wire: each byte a start bit (0), eight data bits least significant first, a stop
    # bit (1); 10 bits a byte at 31,250 bits a second is 320 microseconds, 960 for the message.
    k = 6.0
    cx, cy = 76, 92
    pins = {3: 180, 5: 135, 2: 90, 4: 45, 1: 0}

    d.group('thin')
    d.line((cx - 52, cy), (cx + 52, cy)); d.line((cx, cy - 52), (cx, cy + 52))
    d.circle(cx, cy, 3.5 * k)
    for n, a in pins.items():
        x, y = cx + 3.5 * k * math.cos(math.radians(a)), cy + 3.5 * k * math.sin(math.radians(a))
        d.line((cx, cy), (x, y))

    d.group()
    d.circle(cx, cy, 7.8 * k)                                                  # shell
    # the face, with the key notch at the top
    notch = 1.2 * k
    face_r = 6.6 * k
    a0 = math.degrees(math.asin(notch / face_r))
    pts = [(cx + face_r * math.cos(math.radians(270 + a0 + (360 - 2 * a0) * i / 60)),
            cy + face_r * math.sin(math.radians(270 + a0 + (360 - 2 * a0) * i / 60))) for i in range(61)]
    d.line(*pts)
    d.line(pts[-1], (cx - notch, cy - face_r + 1.6 * k), (cx + notch, cy - face_r + 1.6 * k), pts[0])
    for n, a in pins.items():
        x, y = cx + 3.5 * k * math.cos(math.radians(a)), cy + 3.5 * k * math.sin(math.radians(a))
        d.circle(x, y, 0.6 * k)
        if n in (4, 5, 2):
            d.circle(x, y, 0.25 * k)

    # the current loop, OUT to IN
    lx0, lx1, ly0, ly1 = 186, 380, 64, 112
    d.group('mid')
    _box(d, lx0, ly0 - 14, 46, 76)                                            # sender
    _box(d, lx1 - 70, ly0 - 14, 70, 76)                                       # receiver
    d.line((lx0 + 46, ly0), (lx1 - 70, ly0)); d.line((lx0 + 46, ly1), (lx1 - 70, ly1))
    # the receiver's LED, pointing down the loop, and its photo-transistor beside it
    ex, ey = lx1 - 48, (ly0 + ly1) / 2
    d.line((lx1 - 70, ly0), (ex, ly0), (ex, ey - 8)); d.line((lx1 - 70, ly1), (ex, ly1), (ex, ey + 8))
    d.line((ex - 7, ey - 8), (ex + 7, ey - 8), (ex, ey + 4), closed=True); d.line((ex - 7, ey + 4), (ex + 7, ey + 4))
    for dy in (-5, 1):
        _arrow(d, (ex + 9, ey + dy), (ex + 19, ey + dy + 4), 3); d.line((ex + 9, ey + dy), (ex + 19, ey + dy + 4))
    d.line((ex + 26, ey - 12), (ex + 26, ey + 12)); d.line((ex + 26, ey - 4), (ex + 38, ey - 14)); d.line((ex + 26, ey + 4), (ex + 38, ey + 14))
    _arrow(d, (lx0 + 90, ly0), (lx0 + 104, ly0), 4); _arrow(d, (lx0 + 104, ly1), (lx0 + 90, ly1), 4)

    # the message on the wire
    msg = [0x90, 0x3C, 0x40]
    bits = []
    for b in msg:
        bits += [0] + [(b >> i) & 1 for i in range(8)] + [1]
    x0, cw, yh, yl = 26, 12, 212, 234
    d.group('thin')
    for i in range(0, 31):
        d.line((x0 + i * cw, yh - 4), (x0 + i * cw, yl + 4))
    for j in range(4):
        x = x0 + j * 10 * cw
        d.line((x, yl + 4), (x, yl + 30))
    d.group()
    sig = [(x0 - 12, yh)]
    for i, b in enumerate(bits):
        y = yh if b else yl
        sig += [(x0 + i * cw, sig[-1][1]), (x0 + i * cw, y), (x0 + (i + 1) * cw, y)]
    sig += [(x0 + 30 * cw, yh), (x0 + 30 * cw + 10, yh)]
    d.line(*sig)
    d.group('mid')
    for j in range(3):
        xa, xb = x0 + j * 10 * cw + 2, x0 + (j + 1) * 10 * cw - 2
        d.line((xa, yh - 14), (xa, yh - 18), (xb, yh - 18), (xb, yh - 14))

    d.group('mid')
    for n, a in pins.items():
        rr = 3.5 * k + 10
        d.text(cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a)) + 3, str(n), size=7)
    d.text(cx, cy + 62, 'SOCKET, FRONT', size=7)
    d.text(lx0 + 23, ly0 + 28, 'OUT', size=7)
    d.text(lx1 - 35, ly1 + 24, 'IN', size=7)
    d.text((lx0 + 46 + lx1 - 70) / 2, ly0 - 6, 'PIN 4', size=7)
    d.text((lx0 + 46 + lx1 - 70) / 2, ly1 + 12, 'PIN 5 · 5 MA', size=7)
    d.text(ex + 2, ly0 - 22, 'OPTO-ISOLATOR', size=7)
    for j, lab in enumerate(['90 NOTE ON CH 1', '3C KEY 60', '40 VELOCITY 64']):
        d.text(x0 + j * 10 * cw + 5 * cw, yh - 24, lab, size=7)
    for j, lab in enumerate(['0', '320', '640', '960']):
        d.text(x0 + j * 10 * cw + (3 if j < 3 else -3), yl + 28, lab, size=7, anchor='start' if j < 3 else 'end')
    d.text(200, 278, 'MICROSECONDS · 31,250 BITS A SECOND', size=7)
    d.text(200, 292, 'EACH BYTE: START 0 · 8 BITS, LEAST FIRST · STOP 1', size=7)
    return d


PLATES = {
    'compact-disc': compact_disc,
    'midi': midi,
}
