"""physics plates, segment "The cosmos", first part (sprint 021). See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


# Hubble 1929, Table 1: distance r (10^6 parsecs) and velocity v (km/s) of the
# 24 nebulae whose distances he estimated (PNAS 15: 168-173, p. 169).
HUBBLE_1929 = [
    (0.032, 170), (0.034, 290), (0.214, -130), (0.263, -70), (0.275, -185), (0.275, -220),
    (0.45, 200), (0.5, 290), (0.5, 270), (0.63, 200), (0.8, 300), (0.9, -30),
    (0.9, 650), (0.9, 150), (0.9, 500), (1.0, 920), (1.1, 450), (1.1, 500),
    (1.4, 500), (1.7, 960), (2.0, 500), (2.0, 850), (2.0, 800), (2.0, 1090),
]


def expanding_universe():
    """Hubble's velocity-distance diagram of 1929, from the 24 nebulae of his Table 1.

    The points are his, the full line his slope of 500 km/s per megaparsec; the
    construction line beside it is today's slope of about 70, which his distances,
    too small by a factor of about seven, could not show."""
    d = D()
    x0, y0 = 60, 230                  # origin: distance 0, velocity 0
    sx = 150                          # plate units per megaparsec
    sy = 0.17                         # plate units per km/s
    X = lambda r: x0 + sx * r
    Y = lambda v: y0 - sy * v
    # construction: the grid, every 0.5 Mpc and every 250 km/s
    d.group('thin')
    d.lines([[(X(r / 2), Y(-250)), (X(r / 2), Y(1250))] for r in range(1, 5)])
    d.lines([[(X(0), Y(v)), (X(2.2), Y(v))] for v in (-250, 250, 500, 750, 1000, 1250)])
    # today's slope, about 70 km/s per megaparsec, as a construction line
    d.line((X(0), Y(0)), (X(2.2), Y(70 * 2.2)))
    # the axes
    d.group()
    d.line((X(0), Y(-250)), (X(0), Y(1300)))
    d.line((X(0), Y(0)), (X(2.25), Y(0)))
    _arrow(d, X(0), Y(1300), -math.pi / 2, 5)
    _arrow(d, X(2.25), Y(0), 0, 5)
    # Hubble's line: K = 500 km/s per megaparsec, through the origin
    d.line((X(0), Y(0)), (X(2.2), Y(500 * 2.2)))
    # the 24 nebulae
    d.group('mid')
    for r, v in HUBBLE_1929:
        d.circle(X(r), Y(v), 2.6)
    # the four in the Virgo cluster, ringed
    d.group('thin')
    d.circle(X(2.0), Y(810), 36)
    # labels
    d.group()
    for r in (0.5, 1, 1.5, 2):
        d.text(X(r), Y(0) + 13, f'{r:g}', size=7)
    for v in (500, 1000):
        d.text(X(0) - 6, Y(v) + 3, f'{v}', size=7, anchor='end')
    d.text(X(0) - 6, Y(0) + 3, '0', size=7, anchor='end')
    d.text(X(1.1), Y(-250) + 22, 'DISTANCE · MILLIONS OF PARSECS', size=7)
    d.text(X(0) + 6, Y(1300) + 4, 'KM/S', size=7, anchor='start')
    d.text(X(1.48), Y(500 * 1.62), 'K = 500', size=8, anchor='end')
    d.text(X(2.2), Y(70 * 2.2) - 7, 'TODAY ≈ 70', size=7, anchor='end')
    d.text(X(2.0) - 42, Y(810) + 30, 'VIRGO', size=7, anchor='end')
    d.text(200, 20, 'HUBBLE 1929 · 24 NEBULAE', size=8)
    return d


def cmb():
    """The Bell Labs horn-reflector antenna at Crawford Hill, in section, and the 1965 noise budget.

    The horn's apex is at the focus of a paraboloid; rays from the apex meet an
    offset piece of it and leave parallel, so the horn looks at the sky through
    its side. Beside it, the 6.7 K that Penzias and Wilson measured at the
    zenith, stacked: 2.3 K of air, 0.9 K of antenna, and 3.5 K from nowhere."""
    d = D()
    f = 58                            # focal length of the paraboloid, plate units
    vx, vy = 60, 262                  # its vertex (the axis runs up the plate)
    P = lambda x: (vx + x, vy - x * x / (4 * f))
    F = (vx, vy - f)                  # the focus: the horn's apex
    # the offset reflector: the piece of the parabola between two rays from the focus
    xs = [1.25 * f + (3.15 * f - 1.25 * f) * i / 40 for i in range(41)]
    # construction: the axis, the whole parabola, the focus
    d.group('thin')
    d.line((vx, vy + 6), (vx, 24))
    d.line(*[P(x) for x in [i * 3.4 * f / 60 for i in range(61)]])
    d.line((vx - 6, F[1]), (vx + 6, F[1]))
    # the horn: from the apex out to the reflector, and the aperture it looks through
    a, b = P(xs[0]), P(xs[-1])
    d.group()
    c = (a[0], F[1] + (b[1] - F[1]) * (a[0] - F[0]) / (b[0] - F[0]))   # the upper wall meets the aperture
    d.line(F, a)
    d.line(F, c)
    d.line(*[P(x) for x in xs])
    d.line(c, (a[0], 26))
    d.line(b, (b[0], 26))
    d.line((a[0], 26), (b[0], 26))
    # rays: from the apex to the reflector, then straight up out of the aperture
    d.group('mid')
    for x in (xs[8], xs[20], xs[32]):
        p = P(x)
        d.line(F, p, (p[0], 34))
        _arrow(d, p[0], 34, -math.pi / 2, 4)
    # the noise budget, stacked in kelvin
    bx, by, k = 300, 258, 30          # base of the column, plate units per kelvin
    parts = [(2.3, 'AIR 2.3 K'), (0.9, 'ANTENNA 0.9 K'), (3.5, 'EXCESS 3.5 K')]
    d.group('thin')
    d.lines([[(bx - 26, by - k * t), (bx - 20, by - k * t)] for t in range(0, 8)])
    d.line((bx - 23, by), (bx - 23, by - k * 7))
    d.group()
    top = by
    for t, _ in parts:
        d.line((bx - 14, top), (bx + 14, top), (bx + 14, top - k * t), (bx - 14, top - k * t), closed=True)
        top -= k * t
    d.group('mid')
    t0 = by - k * 3.2
    d.lines([[(bx - 14, t0 - k * 3.5 * i / 7), (bx + 14, t0 - k * 3.5 * (i + 1) / 7)] for i in range(7)])
    # labels
    d.group()
    top = by
    for t, name in parts:
        d.text(bx + 20, top - k * t / 2 + 3, name, size=7, anchor='start')
        top -= k * t
    for t in (0, 5):
        d.text(bx - 28, by - k * t + 3, str(t), size=7, anchor='end')
    d.text(bx, by + 16, '6.7 K AT THE ZENITH', size=7)
    d.text(F[0] - 4, F[1] + 16, 'APEX AT FOCUS', size=7, anchor='start')
    d.text((a[0] + b[0]) / 2, 18, 'TO THE SKY', size=7)
    d.text(130, 292, 'HORN-REFLECTOR · 20 FT · 4080 MC/S', size=8)
    return d


def dark_matter():
    """A spiral galaxy's rotation curve: what its stars and gas alone predict, and what is measured.

    Drawn from a model, not from data: an exponential disc (scale length 3 kpc)
    gives the falling curve; add a halo whose speed levels off at 200 km/s and
    the sum stays flat, as Rubin and Ford found in galaxy after galaxy."""
    d = D()
    x0, y0 = 58, 250
    sx, sy = 11, 0.72                 # plate units per kpc and per km/s
    X = lambda r: x0 + sx * r
    Y = lambda v: y0 - sy * v
    h, vd = 3.0, 180.0                # disc scale length (kpc) and its peak-ish speed
    def v_disc(r):
        # a spherical stand-in for an exponential disc: M(<r) ∝ 1 - (1 + r/h) e^(-r/h)
        m = 1 - (1 + r / h) * math.exp(-r / h)
        return vd * math.sqrt(max(m, 0) / (r / h)) * 1.25 if r > 0 else 0
    def v_halo(r, V=200.0, a=5.0):
        return V * math.sqrt(max(1 - (a / r) * math.atan(r / a), 0)) if r > 0 else 0
    rs = [i * 0.25 for i in range(1, 121)]
    # construction: the grid, every 5 kpc and every 50 km/s
    d.group('thin')
    d.lines([[(X(r), Y(0)), (X(r), Y(250))] for r in range(5, 31, 5)])
    d.lines([[(X(0), Y(v)), (X(30), Y(v))] for v in range(50, 251, 50)])
    # the halo's own share, as a construction line
    d.line(*[(X(r), Y(v_halo(r))) for r in rs])
    # axes
    d.group()
    d.line((X(0), Y(270)), (X(0), Y(0)), (X(31), Y(0)))
    _arrow(d, X(0), Y(270), -math.pi / 2, 5)
    _arrow(d, X(31), Y(0), 0, 5)
    # expected from the visible disc alone
    d.group('mid')
    d.line(*[(X(r), Y(v_disc(r))) for r in rs])
    # measured: disc and halo together
    d.group()
    d.line(*[(X(r), Y(math.hypot(v_disc(r), v_halo(r)))) for r in rs])
    d.group('mid')
    for r in range(2, 30, 2):
        v = math.hypot(v_disc(r), v_halo(r))
        d.circle(X(r), Y(v), 2.2)
    # a galaxy seen edge-on at the top, with the spectrograph's slit along it
    d.group('thin')
    d.line((X(0), 32), (X(30), 32))
    d.group('mid')
    d.ellipse(X(15), 32, 150, 8)
    d.ellipse(X(15), 32, 30, 6)
    # labels
    d.group()
    for r in (10, 20, 30):
        d.text(X(r), Y(0) + 13, str(r), size=7)
    for v in (100, 200):
        d.text(X(0) - 6, Y(v) + 3, str(v), size=7, anchor='end')
    d.text(X(15), Y(0) + 26, 'DISTANCE FROM CENTRE · KPC', size=7)
    d.text(X(0) + 6, Y(270) + 4, 'KM/S', size=7, anchor='start')
    d.text(X(24), Y(math.hypot(v_disc(24), v_halo(24))) - 9, 'MEASURED', size=7, anchor='end')
    d.text(X(29), Y(v_disc(29)) + 13, 'STARS AND GAS ALONE', size=7, anchor='end')
    d.text(X(22), Y(v_halo(22)) + 12, 'HALO', size=7)
    d.text(X(15), 16, 'A SPIRAL, EDGE ON · THE SLIT ALONG ITS DISC', size=7)
    return d


PLATES = {'expanding-universe': expanding_universe, 'cmb': cmb, 'dark-matter': dark_matter}
