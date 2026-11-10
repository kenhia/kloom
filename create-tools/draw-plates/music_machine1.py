"""Plates for Sound and Score's part machine1 (sprint 058): the phonautograph and Edison's
tinfoil phonograph. See plates_for.py."""
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


def phonautograph():
    d = D()
    # Above: Scott's phonautograph of 1859 in section along the horn's axis, the drum seen end-on.
    # The barrel's profile is a computed swell narrowing to a throat the size of a five-franc piece
    # (Scott, 1857); proportions are schematic. Below: the trace as it lies on the unrolled sheet,
    # a voice line and the tuning fork's line under it. The voice is invented (a fundamental with
    # two harmonics under a swelling envelope); the fork runs at 250 Hz, Scott's "500 simple
    # vibrations", against a voice near 125 Hz, so two fork waves to each voice wave.
    ax, x0, x1 = 112, 22, 182                    # horn axis, mouth, throat
    def r(t):                                    # half-height of the barrel, t from mouth (0) to throat (1)
        return 14 + 50 * math.sin(math.pi * (0.18 + 0.7 * t)) * (1 - 0.85 * t ** 2)
    ts = [i / 40 for i in range(41)]
    top = [(x0 + t * (x1 - x0), ax - r(t)) for t in ts]
    bot = [(x0 + t * (x1 - x0), ax + r(t)) for t in ts]
    lin_top = [(x, y + 5) for x, y in top]       # the plaster lining
    lin_bot = [(x, y - 5) for x, y in bot]
    mx = x1 + 8                                  # the membrane
    cx, cy, R = 292, ax, 52                      # the drum, end-on
    tip = (cx - R, ax)

    d.group('thin')
    d.line((x0 - 8, ax), (cx + R + 20, ax))                            # the axis
    d.line((cx, cy - R - 14), (cx, cy + R + 14))
    for a in (30, 150, 210, 330):
        rad = math.radians(a)
        d.line((cx, cy), (cx + R * math.cos(rad), cy + R * math.sin(rad)))
    d.line((x0, ax - r(0) - 10), (x0, ax + r(0) + 10))
    d.line((x1, ax - 34), (x1, ax + 34))

    d.group()
    d.line(*top); d.line(*bot)
    d.line(top[0], bot[0])
    d.line(top[-1], (mx, top[-1][1]))
    d.line(bot[-1], (mx, bot[-1][1]))
    d.line((mx, top[-1][1] - 6), (mx, bot[-1][1] + 6))                 # membrane on its ring
    d.circle(cx, cy, R)
    d.circle(cx, cy, 5)
    d.line((mx, ax), tip)                                              # the bristle

    d.group('mid')
    d.line(*lin_top); d.line(*lin_bot)
    d.line((mx - 4, top[-1][1] - 8), (mx + 4, top[-1][1] - 8))         # ring clamps
    d.line((mx - 4, bot[-1][1] + 8), (mx + 4, bot[-1][1] + 8))
    d.circle(cx, cy, R + 3)                                            # paper and soot
    # the tuning fork, standing above the throat, writing its own line on the drum by the bristle
    fx, fy_top, fy_tip = 228, 40, 74
    d.line((fx, fy_tip), (fx, fy_top), (fx + 9, fy_top), (fx + 9, fy_tip))   # two prongs
    d.line((fx + 4.5, fy_top), (fx + 4.5, fy_top - 18))                     # stem
    a = math.radians(205)
    fork_tip = (cx + R * math.cos(a), cy + R * math.sin(a))
    d.line((fx + 9, fy_tip), fork_tip)
    d.arc(cx, cy, R + 12, 120, 160)                                    # the drum's turn
    p = (cx + (R + 12) * math.cos(math.radians(160)), cy + (R + 12) * math.sin(math.radians(160)))
    q = (cx + (R + 12) * math.cos(math.radians(163)), cy + (R + 12) * math.sin(math.radians(163)))
    _arrow(d, p, q, 4)

    # below: the unrolled sheet
    y1, y2, xa, xb = 228, 262, 30, 370
    d.group('thin')
    d.line((xa, y1), (xb, y1)); d.line((xa, y2), (xb, y2))
    for i in range(5):
        x = xa + i * (xb - xa) / 4
        d.line((x, y1 - 20), (x, y2 + 8))
    d.group()
    voice, fork = [], []
    n = 340
    for i in range(n + 1):
        x = xa + i * (xb - xa) / n
        s = i / n
        env = 0.25 + 0.75 * math.sin(math.pi * min(1.0, s * 1.25)) ** 0.7
        ph = 2 * math.pi * 8 * s
        v = math.sin(ph) + 0.55 * math.sin(2 * ph + 0.6) + 0.3 * math.sin(3 * ph + 1.3)
        voice.append((x, y1 - 9 * env * v))
        fork.append((x, y2 - 4.5 * math.sin(2 * math.pi * 16 * s)))
    d.line(*voice)
    d.group('mid')
    d.line(*fork)

    d.group('mid')
    d.text(x0 + 4, 28, 'BARREL, LINED WITH PLASTER', size=7, anchor='start')
    d.text(mx + 2, ax + 52, 'MEMBRANE', size=7, anchor='middle')
    d.text(216, ax + 15, 'BRISTLE', size=7, anchor='middle')
    d.text(fx - 6, fy_top + 4, 'TUNING FORK', size=7, anchor='end')
    d.text(cx, cy + R + 24, 'DRUM · LAMPBLACKED PAPER', size=7)
    d.text(xa, y1 - 22, 'VOICE', size=7, anchor='start')
    d.text(xa, y2 + 18, 'FORK · 250 WAVES A SECOND', size=7, anchor='start')
    d.text(200, 292, 'SCOTT DE MARTINVILLE · PHONAUTOGRAPH OF 1859 · SCHEMATIC', size=7)
    return d


def edison_phonograph():
    d = D()
    # Edison's tinfoil phonograph in plan, after his patent's Fig. 2 (US 200,521, 1878): the brass
    # cylinder on a shaft cut ten threads to the inch, turning in a threaded bearing so that each
    # turn carries it one groove along; the recording mouthpiece on the near side, the lighter
    # reproducing diaphragm on the far side. Below: the foil across one groove, indented to a
    # depth that follows the voice ("hill and dale"); the indentations are invented, the
    # mechanism is the patent's. The cylinder is drawn about 2.5 times its pitch scale.
    ay = 98
    cx0, cx1, cr = 128, 268, 42                  # cylinder ends, half-height in plan
    sx0, sx1 = 34, 372                           # the shaft
    pitch = 7.0                                  # one groove, drawn
    d.group('thin')
    d.line((sx0 - 6, ay), (sx1 + 6, ay))                                # axis
    for x in (cx0, cx1):
        d.line((x, ay - cr - 10), (x, ay + cr + 10))
    d.line((198, ay + cr + 6), (198, ay + 70))                          # the mouthpiece's line
    d.line((198, ay - cr - 6), (198, ay - 66))

    d.group()
    _box(d, cx0, ay - cr, cx1 - cx0, 2 * cr)                            # the cylinder in plan
    d.line((sx0, ay - 4), (cx0, ay - 4)); d.line((sx0, ay + 4), (cx0, ay + 4))
    d.line((cx1, ay - 4), (sx1, ay - 4)); d.line((cx1, ay + 4), (sx1, ay + 4))
    _box(d, 64, ay - 22, 14, 44)                                        # threaded bearing (nut)
    _box(d, 318, ay - 22, 14, 44)                                       # plain bearing
    d.line((sx0, ay - 4), (sx0, ay - 30), (sx0 - 14, ay - 30))          # the crank
    d.circle(sx0 - 14, ay - 30, 3)
    # the recording tube on the near side, the reproducer on the far side
    d.line((190, ay + 70), (190, ay + cr + 12)); d.line((206, ay + 70), (206, ay + cr + 12))
    d.line((184, ay + cr + 12), (212, ay + cr + 12))                    # diaphragm
    d.line((180, ay + 70), (216, ay + 70))
    d.line((192, ay - 66), (192, ay - cr - 12)); d.line((204, ay - 66), (204, ay - cr - 12))
    d.line((187, ay - cr - 12), (209, ay - cr - 12))                    # lighter diaphragm

    d.group('mid')
    # helical grooves across the cylinder: lines leaning by one pitch over the visible half-turn
    x = cx0 + 2
    while x < cx1 - pitch:
        d.line((x, ay + cr), (x + pitch / 2, ay - cr))
        x += pitch
    # the screw thread on the shaft between the crank and the cylinder
    x = sx0 + 6
    while x < cx0 - 6:
        d.line((x, ay + 4), (x + 2.5, ay - 4))
        x += 3.5
    d.line((198, ay + cr + 12), (198, ay + cr))                         # recording point
    d.line((198, ay - cr - 12), (198, ay - cr))                         # playback point
    d.line((209, ay - cr - 12), (214, ay - cr - 6), (199, ay - cr - 2)) # its spring

    # below: the foil across one groove, in section along the groove, indented
    y0, xa, xb = 236, 40, 360
    d.group('thin')
    d.line((xa, y0), (xb, y0))
    d.line((xa, y0 + 16), (xb, y0 + 16))
    d.group()
    pts = []
    n = 320
    for i in range(n + 1):
        s = i / n
        x = xa + s * (xb - xa)
        ph = 2 * math.pi * 6 * s
        v = 0.5 + 0.5 * math.sin(ph) * (0.6 + 0.4 * math.sin(2 * math.pi * 1.3 * s)) + 0.12 * math.sin(3 * ph)
        pts.append((x, y0 + 2 + 10 * max(0.0, min(1.0, v))))
    d.line(*pts)
    d.group('mid')
    d.text(sx0 - 18, ay - 44, 'CRANK', size=7, anchor='start')
    d.text(71, ay + 34, 'NUT', size=7)
    d.text(96, ay - 30, '10 THREADS TO THE INCH', size=7, anchor='middle')
    d.text(198, ay + 84, 'RECORDING DIAPHRAGM', size=7)
    d.text(198, ay - 74, 'REPRODUCING DIAPHRAGM ON A SPRING', size=7)
    d.text(cx1 + 6, ay + cr + 14, 'TINFOIL ON BRASS', size=7, anchor='start')
    d.text(xa, y0 - 10, 'THE FOIL ALONG ONE GROOVE, INDENTED', size=7, anchor='start')
    d.text(200, 292, 'EDISON · TINFOIL PHONOGRAPH IN PLAN · AFTER US 200,521', size=7)
    return d


PLATES = {
    'phonautograph': phonautograph,
    'edison-phonograph': edison_phonograph,
}
