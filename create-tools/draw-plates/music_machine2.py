"""Plates for Sound and Score's part machine2 (sprint 058): the gramophone and music on the radio.
See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _signal(t):
    """A made-up sound: a tone with two overtones, the same in both halves of the gramophone plate."""
    return (math.sin(t) + 0.35 * math.sin(2 * t + 0.6) + 0.18 * math.sin(3 * t + 1.1)) / 1.4


def gramophone():
    d = D()
    # Two grooves carrying the same made-up wave. Left, Berliner's lateral groove: the wave moves the
    # groove from side to side in plan, and its section is the same V everywhere, of even depth.
    # Right, the cylinder's vertical (hill-and-dale) groove: in plan only its width changes, and in a
    # section along it the floor rises and falls with the wave. Schematic, not to scale.
    xs = [i * 2 for i in range(81)]          # 160 px of groove in plan, each half
    amp, half = 9.0, 6.0                      # wiggle amplitude, groove half-width (px)
    lx0, rx0, py = 24, 216, 70                # plan views: left origin, right origin, centre line
    k = 2 * math.pi / 64                      # one cycle every 64 px

    d.group('thin')
    d.line((lx0, py), (lx0 + 160, py))                                      # left centre line
    d.line((rx0, py), (rx0 + 160, py))                                      # right centre line
    d.line((200, 26), (200, 280))                                           # divider
    sy = 196                                                                # sections' surface line
    d.line((40, sy), (170, sy))
    d.line((rx0, sy), (rx0 + 160, sy))

    # plan views
    d.group()
    left_a = [(lx0 + x, py - half + amp * _signal(k * x)) for x in xs]
    left_b = [(lx0 + x, py + half + amp * _signal(k * x)) for x in xs]
    d.line(*left_a); d.line(*left_b)
    depth = lambda x: 0.55 + 0.45 * _signal(k * x)                          # 0.1 .. 1.0 of full depth
    right_a = [(rx0 + x, py - (2 + 7 * depth(x))) for x in xs]
    right_b = [(rx0 + x, py + (2 + 7 * depth(x))) for x in xs]
    d.line(*right_a); d.line(*right_b)

    # stylus tips sitting in each groove, with the way each moves
    d.group('mid')
    sx = 80
    cy = py + amp * _signal(k * sx)
    d.circle(lx0 + sx, cy, 3.2)
    ay = py + 26                                                            # its sideways swing, below
    d.line((lx0 + sx, cy + 4), (lx0 + sx, ay - 3))
    d.line((lx0 + sx - 20, ay), (lx0 + sx + 20, ay))
    _arrow(d, (lx0 + sx, ay), (lx0 + sx - 20, ay), 4); _arrow(d, (lx0 + sx, ay), (lx0 + sx + 20, ay), 4)
    d.circle(rx0 + sx, py, 3.2)
    for x in (lx0 + 4, rx0 + 4):                                            # direction of travel
        d.line((x, py - 30), (x + 30, py - 30)); _arrow(d, (x, py - 30), (x + 30, py - 30), 4)

    # sections. Left: across the groove, a V of even depth with the stylus moving sideways.
    d.group()
    gx, gw, gd = 105, 26, 22
    d.line((40, sy), (gx - gw / 2, sy), (gx, sy + gd), (gx + gw / 2, sy), (170, sy))
    d.line((40, sy), (40, sy + 40), (170, sy + 40), (170, sy))              # the disc's thickness
    # the stylus: a tapered needle whose rounded tip rests on the groove walls
    tip = (gx, sy + gd - 7)
    d.line((gx - 3.5, tip[1] - 2), (gx - 9, sy - 46)); d.line((gx + 3.5, tip[1] - 2), (gx + 9, sy - 46))
    d.arc(tip[0], tip[1], 4, 0, 180)
    # right: along the groove, the floor rising and falling under a stylus that moves up and down
    floor = [(rx0 + x, sy + 8 + 14 * depth(x)) for x in xs]
    d.line(*floor)
    d.line((rx0, sy + 40), (rx0 + 160, sy + 40))
    d.line((rx0, sy), (rx0, sy + 40)); d.line((rx0 + 160, sy), (rx0 + 160, sy + 40))
    fx = 80
    fy = sy + 8 + 14 * depth(fx)
    d.line((rx0 + fx - 3.5, fy - 6), (rx0 + fx - 9, sy - 46)); d.line((rx0 + fx + 3.5, fy - 6), (rx0 + fx + 9, sy - 46))
    d.arc(rx0 + fx, fy - 4, 4, 0, 180)

    d.group('mid')
    for s in (-1, 1):                                                       # lateral motion
        d.line((gx + s * 14, sy - 30), (gx + s * 30, sy - 30)); _arrow(d, (gx + s * 14, sy - 30), (gx + s * 30, sy - 30), 4)
    x0 = rx0 + fx + 26                                                      # vertical motion
    d.line((x0, sy - 40), (x0, sy - 12)); _arrow(d, (x0, sy - 26), (x0, sy - 40), 4); _arrow(d, (x0, sy - 26), (x0, sy - 12), 4)
    # depth gauge under the lateral section: the same depth at every turn of the wave
    d.line((gx + gw / 2 + 8, sy), (gx + gw / 2 + 8, sy + gd)); _arrow(d, (gx + gw / 2 + 8, sy + 10), (gx + gw / 2 + 8, sy + gd), 3)

    d.group('mid')
    d.text(104, 22, 'LATERAL · BERLINER DISC', size=7)
    d.text(296, 22, 'VERTICAL · CYLINDER', size=7)
    d.text(104, 112, 'PLAN: THE GROOVE SWINGS', size=7)
    d.text(296, 112, 'PLAN: ONLY ITS WIDTH CHANGES', size=7)
    d.text(104, 254, 'SECTION ACROSS: EVEN DEPTH', size=7)
    d.text(296, 254, 'SECTION ALONG: HILL AND DALE', size=7)
    d.text(200, 290, 'ONE WAVE, TWO WAYS OF CUTTING IT · SCHEMATIC', size=7)
    return d


def radio_music():
    d = D()
    # Amplitude modulation, computed: an audio wave (top), a carrier (middle) and the carrier with
    # its amplitude shaped by the audio (bottom), its envelope dashed. The carrier is drawn far slower
    # than a real one: KDKA's of 1920, at 545 kHz, turned over about 1,240 times for each cycle of a
    # 440 Hz A, which no drawing could show.
    x0, x1 = 30, 370
    n = 680
    audio = lambda u: math.sin(2 * math.pi * 2 * u) * 0.75 + 0.25 * math.sin(2 * math.pi * 5 * u + 0.8)
    carrier = lambda u: math.sin(2 * math.pi * 46 * u)
    m = 0.7                                                                  # modulation depth
    ys = (52, 128, 222)                                                      # rows' centre lines
    a1, a2, a3 = 20, 18, 34

    d.group('thin')
    for y in ys:
        d.line((x0, y), (x1, y))
    d.line((x0, 24), (x0, 270))

    d.group()
    pts = [(x0 + (x1 - x0) * i / n, ys[0] - a1 * audio(i / n)) for i in range(n + 1)]
    d.line(*pts)
    pts = [(x0 + (x1 - x0) * i / n, ys[1] - a2 * carrier(i / n)) for i in range(n + 1)]
    d.line(*pts)

    d.group()
    pts = [(x0 + (x1 - x0) * i / n, ys[2] - a3 / (1 + m) * (1 + m * audio(i / n)) * carrier(i / n)) for i in range(n + 1)]
    d.line(*pts)

    d.group('mid')
    up = [(x0 + (x1 - x0) * i / 170, ys[2] - a3 / (1 + m) * (1 + m * audio(i / 170))) for i in range(171)]
    dn = [(x, 2 * ys[2] - y) for x, y in up]
    d.dashed(*up, dash=3, gap=3)
    d.dashed(*dn, dash=3, gap=3)
    # arrows from the two inputs down to the product
    for x in (x1 - 6,):
        d.line((x, ys[0] + 26), (x, ys[1] - 24)); _arrow(d, (x, ys[0] + 26), (x, ys[1] - 24), 4)
        d.line((x, ys[1] + 24), (x, ys[2] - 40)); _arrow(d, (x, ys[1] + 24), (x, ys[2] - 40), 4)

    d.group('mid')
    d.text(x0 + 4, 24, 'THE MUSIC · AUDIO', size=7, anchor='start')
    d.text(x0 + 4, 102, 'THE CARRIER · DRAWN FAR TOO SLOW', size=7, anchor='start')
    d.text(x0 + 4, 176, 'AM: THE CARRIER SHAPED BY THE MUSIC', size=7, anchor='start')
    d.text(200, 276, 'THE DASHED ENVELOPE IS WHAT A CRYSTAL SET HEARS', size=7)
    d.text(200, 291, 'AMPLITUDE MODULATION · COMPUTED', size=7)
    return d


PLATES = {
    'gramophone': gramophone,
    'radio-music': radio_music,
}
