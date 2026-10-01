"""feynman plates, segment "Far Rockaway" (sprint 014). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _dim(d, x0, y0, x1, y1, off, label, size=8):
    """A dimension line between two points, offset sideways, with its extension lines and label."""
    ang = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(ang) * off, math.cos(ang) * off
    a, b = (x0 + nx, y0 + ny), (x1 + nx, y1 + ny)
    d.lines([[(x0, y0), (a[0] + nx * 0.2, a[1] + ny * 0.2)], [(x1, y1), (b[0] + nx * 0.2, b[1] + ny * 0.2)]])
    d.line(a, b)
    _arrow(d, *a, ang + math.pi, 4)
    _arrow(d, *b, ang, 4)
    return (a[0] + b[0]) / 2 + nx * 0.6, (a[1] + b[1]) / 2 + ny * 0.6


def far_rockaway():
    """The father's lesson from the encyclopedia: a 20-foot dinosaur's head at a second-floor window."""
    d = D()
    g = 240          # ground line
    ft = 9.2         # pixels per foot
    hx0, hx1 = 214, 352  # the house's walls
    story = 10 * ft
    # construction: the ground, a ten-foot scale down the side, the storey lines carried across
    d.group('thin')
    d.line((20, g), (384, g))
    d.lines([[(372, g - k * ft), (378, g - k * ft)] for k in range(0, 25)])
    d.line((375, g), (375, g - 24 * ft))
    d.lines([[(hx0 - 170, g - story), (hx1, g - story)], [(hx0 - 170, g - 2 * story), (hx1, g - 2 * story)]])
    # the house: two storeys and a pitched roof, the upstairs window
    d.group()
    d.line((hx0, g), (hx0, g - 2 * story), (hx1, g - 2 * story), (hx1, g))
    d.line((hx0 - 8, g - 2 * story), ((hx0 + hx1) / 2, g - 2 * story - 46), (hx1 + 8, g - 2 * story))
    d.line((hx0, g - story), (hx1, g - story))
    wx, wy, ww, wh = hx0, g - story - 58, 3, 42  # the window opening in the gable wall, seen edge-on
    d.line((hx0 + 30, g - story - 16), (hx0 + 30, g - story - 58), (hx0 + 74, g - story - 58),
           (hx0 + 74, g - story - 16), closed=True)
    d.line((hx0 + 52, g - story - 58), (hx0 + 52, g - story - 16))
    d.line((hx0 + 30, g - story - 37), (hx0 + 74, g - story - 37))
    d.line((hx0 + 104, g), (hx0 + 104, g - 34), (hx0 + 124, g - 34), (hx0 + 124, g))
    # the dinosaur, standing in the front yard: a theropod in profile, its head level with the window
    d.group('mid')
    top = g - 20 * ft
    skull = [(hx0 - 6, top + 26), (hx0 - 14, top + 14), (hx0 - 30, top + 6), (hx0 - 58, top + 2),
             (hx0 - 82, top + 8), (hx0 - 92, top + 20), (hx0 - 90, top + 38), (hx0 - 74, top + 44),
             (hx0 - 40, top + 40), (hx0 - 12, top + 36), (hx0 - 6, top + 26)]
    d.line(*skull)
    d.line((hx0 - 12, top + 30), (hx0 - 44, top + 32))  # the jaw line
    d.lines([[(hx0 - 16 - 6 * k, top + 30), (hx0 - 18 - 6 * k, top + 35)] for k in range(5)])
    d.circle(hx0 - 66, top + 16, 3)
    neck = [(hx0 - 84, top + 40), (hx0 - 100, top + 70), (hx0 - 108, top + 100)]
    back = [(hx0 - 88, top + 12), (hx0 - 116, top + 44), (hx0 - 132, top + 80)]
    d.line(*neck)
    d.line(*back)
    body = [(hx0 - 108, top + 100), (hx0 - 112, top + 124), (hx0 - 130, top + 140), (hx0 - 160, top + 136),
            (hx0 - 190, top + 128), (hx0 - 210, top + 116)]
    d.line(*body)
    d.line((hx0 - 132, top + 80), (hx0 - 150, top + 96), (hx0 - 180, top + 104), (hx0 - 210, top + 116))
    d.line((hx0 - 112, top + 110), (hx0 - 100, top + 120), (hx0 - 96, top + 128))  # the small arm
    d.line((hx0 - 150, top + 136), (hx0 - 144, g - 30), (hx0 - 132, g - 8), (hx0 - 116, g))
    d.line((hx0 - 172, top + 132), (hx0 - 170, g - 28), (hx0 - 160, g - 6), (hx0 - 146, g))
    # dimensions: the head's height and the storeys
    d.group('thin')
    lx, ly = _dim(d, 30, g, 30, top + 6, 0, '')
    sx, sy = _dim(d, hx1 + 2, g, hx1 + 2, g - story, -14, '')
    # labels
    d.group()
    d.text(lx + 6, (g + top) / 2 + 30, '20 FT', size=8, anchor='start')
    d.text(hx1 - 14, g - story / 2 + 3, '10 FT', size=8, anchor='end')
    d.text(hx0 + 52, g - story - 64, 'BEDROOM', size=7)
    d.text(200, 272, 'ENCYCLOPAEDIA BRITANNICA · READ ALOUD', size=8)
    return d


def radio_boy():
    """A tuned circuit: the coil and the variable condenser, the crystal and the phones, and the resonance they pick."""
    d = D()
    # construction: the resonance curve's axes and grid, frequency across, response up
    ox, oy, w, h = 226, 236, 150, 120
    f0 = 0.5
    curve = []
    for i in range(121):
        x = i / 120
        q = 7.0
        r = 1 / math.sqrt(1 + (q * (x / f0 - f0 / max(x, 1e-3))) ** 2)
        curve.append((ox + w * x, oy - h * r))
    d.group('thin')
    d.lines([[(ox + w * k / 6, oy), (ox + w * k / 6, oy - h - 6)] for k in range(1, 7)])
    d.lines([[(ox, oy - h * k / 4), (ox + w, oy - h * k / 4)] for k in range(1, 5)])
    d.line((ox + w * f0, oy), (ox + w * f0, oy - h - 12))
    # the circuit: aerial, coil (a helix in section), condenser, crystal, phones, ground
    d.group()
    cx, top, bot = 60, 70, 236
    d.line((cx, 30), (cx, top))
    d.lines([[(cx - 14, 30), (cx, 44), (cx + 14, 30)]])
    turns = 7
    pts = []
    for i in range(turns * 24 + 1):
        t = i / 24
        pts.append((cx + 12 * math.sin(2 * math.pi * t), top + 10 + t * 16))
    d.line(*pts)
    coil_end = top + 10 + turns * 16
    d.line((cx, coil_end), (cx, bot))
    d.line((cx, top + 4), (132, top + 4), (132, 140))
    d.line((118, 140), (146, 140))
    d.line((118, 148), (146, 148))
    d.line((132, 148), (132, bot))
    d.line((cx, bot), (180, bot))
    d.lines([[(170 + k * 4, bot + 6 + k * 5), (190 - k * 4, bot + 6 + k * 5)] for k in range(3)])
    d.line((180, bot), (180, bot + 6))
    # detail: the condenser's tuning arrow, the cat's whisker on its crystal, the phones
    d.group('mid')
    d.line((110, 160), (154, 128))
    _arrow(d, 154, 128, math.atan2(128 - 160, 154 - 110))
    d.line((132, top + 4), (180, top + 4), (180, 96))
    d.line((172, 96), (188, 96), (188, 108), (172, 108), closed=True)
    d.line((180, 96), (184, 86), (178, 80))
    d.line((180, 108), (180, 150))
    d.circle(172, 166, 12)
    d.circle(196, 166, 12)
    d.arc(184, 166, 18, 180, 360)
    d.line((180, 150), (184, 148))
    d.line((180, 178), (180, bot))
    # the curve: the one station the tuning picks out
    d.group()
    d.line((ox, oy), (ox + w + 6, oy))
    d.line((ox, oy), (ox, oy - h - 10))
    d.line(*curve)
    d.group()
    d.text(ox + w * f0, oy - h - 16, 'f = 1/2π√LC', size=8)
    d.text(ox + w / 2, oy + 16, 'FREQUENCY', size=7)
    d.text(cx + 22, top + 64, 'L', size=9, anchor='start')
    d.text(154, 150, 'C', size=9, anchor='start')
    d.text(200, 100, 'CRYSTAL', size=7, anchor='start')
    d.text(184, 196, 'PHONES', size=7)
    return d


def least_action():
    """A ball thrown up and caught: the true path in time, the paths it did not take, and the action each one costs."""
    d = D()
    ox, oy, w, h = 48, 252, 310, 158  # time runs right, height runs up
    T = 1.0
    true = lambda t: 4 * t * (T - t)  # the parabola, height in units of its peak
    P = lambda t, y: (ox + w * t, oy - h * y)
    # construction: time and height grids, the endpoints fixed
    d.group('thin')
    d.lines([[P(k / 8, 0), P(k / 8, 1.3)] for k in range(1, 9)])
    d.lines([[P(0, k / 4), P(1.02, k / 4)] for k in range(1, 5)])
    # the paths it did not take: the true path plus a wiggle that vanishes at both ends
    d.group('mid')
    for a, n in ((0.28, 1), (-0.22, 2), (0.14, 3)):
        d.line(*[P(i / 80, true(i / 80) + a * math.sin(n * math.pi * i / 80)) for i in range(81)])
    # axes and the true path
    d.group()
    d.line(P(0, 0), P(1.06, 0))
    d.line(P(0, 0), P(0, 1.36))
    _arrow(d, *P(1.06, 0), 0)
    _arrow(d, *P(0, 1.36), -math.pi / 2)
    d.line(*[P(i / 80, true(i / 80)) for i in range(81)])
    d.circle(*P(0, 0), 3.5)
    d.circle(*P(1, 0), 3.5)
    # the ball, at five equal instants along its true path
    d.group('mid')
    for k in range(1, 8, 2):
        d.circle(*P(k / 8, true(k / 8)), 4)
    d.group()
    d.text(210, 24, 'S = ∫ (KE − PE) dt  ·  LEAST ON THE TRUE PATH', size=8)
    d.text(*P(1.04, -0.09), 'TIME', size=7)
    d.text(ox + 8, oy - h * 1.33, 'HEIGHT', size=7, anchor='start')
    d.text(*P(0, -0.09), 'THROWN', size=7)
    d.text(*P(0.96, -0.09), 'CAUGHT', size=7, anchor='end')
    return d


PLATES = {
    'far-rockaway': far_rockaway,
    'radio-boy': radio_boy,
    'least-action': least_action,
}
