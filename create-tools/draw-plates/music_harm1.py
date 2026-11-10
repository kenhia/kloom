"""Plates for Sound and Score's part harm1 (sprint 058): Pythagoras's ratios and Aristoxenus's genera.
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


def pythagoras_ratios():
    d = D()
    # A monochord in elevation. The string between the fixed bridges is 12 units long, ruled below,
    # and the movable bridge stands at 8: the longer part sounds a fifth (3:2) above the open string.
    # The octave (6) and fourth (9) are marked on the rule. The string's sag and the lobes of its
    # vibration are schematic; the divisions are exact.
    x0, x1 = 58, 338                      # the fixed bridges
    u = (x1 - x0) / 12                    # one unit of the rule
    sy = 128                              # the string
    top, bot = 146, 178                   # the sound box
    ry = 214                              # the rule
    xb = x0 + 8 * u                       # the movable bridge

    d.group('thin')
    for x in (x0, x1):
        d.line((x, bot), (x, ry + 10))
    for n in (6, 8, 9):
        x = x0 + n * u
        d.line((x, sy - 4), (x, top)); d.line((x, bot), (x, ry - 12))
    # the open string's fundamental, one lobe over all twelve units
    lobe = [(x0 + t * (x1 - x0), sy - 40 * math.sin(math.pi * t)) for t in [i / 48 for i in range(49)]]
    d.line(*lobe)

    d.group()
    _box(d, 28, top, 344, bot - top)                                      # sound box
    d.line((40, bot), (40, bot + 6)); d.line((360, bot), (360, bot + 6))   # feet
    for x in (x0, x1):                                                    # fixed bridges
        d.line((x - 6, top), (x, sy), (x + 6, top))
    d.line((x0 - 22, sy + 4), (x0, sy), (x1, sy), (x1 + 20, sy + 6))       # the string, tied off
    d.circle(x1 + 24, sy + 7, 3.5)                                        # tuning peg
    d.line((xb - 7, top), (xb - 2, sy + 1), (xb + 2, sy + 1), (xb + 7, top), closed=True)  # movable bridge
    d.circle(x0 - 24, sy + 4.3, 2)                                               # the string's knot

    d.group('mid')
    # the stopped string's two parts, each vibrating in a lobe of its own
    for a, b in ((x0, xb), (xb, x1)):
        n = 36
        pts = [(a + (b - a) * i / n, sy + 22 * math.sin(math.pi * i / n) * (b - a) / (x1 - x0)) for i in range(n + 1)]
        d.line(*pts)
    # the rule
    d.line((x0, ry), (x1, ry))
    for n in range(13):
        h = 8 if n in (0, 6, 8, 9, 12) else 4
        d.line((x0 + n * u, ry), (x0 + n * u, ry + h))
    _arrow(d, (xb, ry + 24), (xb, ry + 12), 4)

    d.group('mid')
    d.text(x0 + 6 * u, 76, 'OPEN STRING', size=7)
    d.text(x0, ry + 20, '0', size=7)
    d.text(x1, ry + 20, '12', size=7)
    for n, r, name in ((6, '2:1', 'OCTAVE'), (8, '3:2', 'FIFTH'), (9, '4:3', 'FOURTH')):
        d.text(x0 + n * u, ry - 8 if n != 8 else ry - 8, str(n), size=7)
    d.text(x0 + 6 * u, ry + 40, 'OCTAVE 2:1', size=7)
    d.text(x0 + 8 * u, ry + 52, 'FIFTH 3:2', size=7)
    d.text(x0 + 9 * u + 14, ry + 40, 'FOURTH 4:3', size=7, anchor='start')
    d.text(x0 + 3 * u, top + 19, 'SOUND BOX', size=7)
    d.text(xb + 10, top + 19, 'MOVABLE BRIDGE AT 8', size=7, anchor='start')
    d.text(200, 292, 'THE MONOCHORD · KANON · STRING OF 12 UNITS', size=7)
    return d


def aristoxenus():
    d = D()
    # The tetrachord from hypate (low) to mese (high), a fourth of 30 twelfths of a tone, divided as
    # Aristoxenus gives his six named shades (Macran's table, 1902). The two outer notes are fixed;
    # the two movable notes, parhypate and lichanos, are marked on each line, low notes on the left.
    shades = [
        ('ENHARMONIC', 3, 3),
        ('SOFT CHROMATIC', 4, 4),
        ('HEMIOLIC CHROMATIC', 4.5, 4.5),
        ('TONIC CHROMATIC', 6, 6),
        ('SOFT DIATONIC', 6, 9),
        ('SHARP DIATONIC', 6, 12),
    ]
    xa, xm = 150, 380
    u = (xm - xa) / 30
    y0, dy = 70, 30

    d.group('thin')
    for k in range(31):
        x = xa + k * u
        h = 6 if k % 6 == 0 else 3
        d.line((x, 38), (x, 38 + h))
    d.line((xa, 38), (xm, 38))
    for k in range(0, 31, 6):
        d.line((xa + k * u, 46), (xa + k * u, y0 + 5 * dy + 8))

    d.group()
    for i, _ in enumerate(shades):
        y = y0 + i * dy
        d.line((xa, y), (xm, y))
        for x in (xa, xm):
            d.line((x, y - 7), (x, y + 7))

    d.group('mid')
    for i, (_, a, b) in enumerate(shades):
        y = y0 + i * dy
        for x in (xa + a * u, xa + (a + b) * u):
            d.circle(x, y, 2.6)
            d.line((x, y - 5), (x, y + 5))

    d.group('mid')
    d.text(xa, 32, '0', size=7)
    d.text(xa + 12 * u, 32, '12 = A TONE', size=7)
    d.text(xm, 32, '30', size=7)
    for i, (name, a, b) in enumerate(shades):
        y = y0 + i * dy
        d.text(xa - 10, y + 2.5, name, size=7, anchor='end')
        c = 30 - a - b
        d.text(xm - 4, y - 6, f'{c:g}', size=7, anchor='end')
    d.text(xa, y0 + 5 * dy + 22, 'HYPATE', size=7)
    d.text(xm, y0 + 5 * dy + 22, 'MESE', size=7)
    d.text(xa + 15 * u, y0 + 5 * dy + 22, 'PARHYPATE · LICHANOS MOVE', size=7)
    d.text(200, 292, 'A FOURTH IN TWELFTHS OF A TONE · SIX SHADES', size=7)
    return d


PLATES = {
    'pythagoras-ratios': pythagoras_ratios,
    'aristoxenus': aristoxenus,
}
