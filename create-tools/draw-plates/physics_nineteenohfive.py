"""physics plates, part "nineteen-oh-five" (sprint 021): black-body, atoms-real, special-relativity. See physics.py."""
import math
import random

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


# physical constants (SI), for the black-body curves
H, C, K = 6.62607015e-34, 299792458.0, 1.380649e-23


def _planck(lam_um, T):
    """Planck's spectral radiance per unit wavelength, arbitrary scale."""
    lam = lam_um * 1e-6
    return 1 / (lam ** 5 * (math.exp(H * C / (lam * K * T)) - 1))


def _wien(lam_um, T):
    """Wien's 1896 law: Planck's without the -1, right at short wavelengths only."""
    lam = lam_um * 1e-6
    return 1 / (lam ** 5 * math.exp(H * C / (lam * K * T)))


def _rj(lam_um, T):
    """The Rayleigh-Jeans law, the classical answer: right at long wavelengths, infinite at short."""
    lam = lam_um * 1e-6
    return lam ** -4 * K * T / (H * C)


def black_body():
    """Black-body spectra at 1,200, 1,500 and 1,800 K, computed from Planck's law.

    The hottest curve carries its two failed rivals as construction lines:
    Wien's law, which falls below it at long wavelengths, and the classical
    Rayleigh-Jeans law, which runs off the top towards the ultraviolet. A
    thin line joins the peaks (Wien's displacement law). Inset: the cavity
    with a small hole that makes a black body, a ray going in and not out."""
    d = D()
    x0, y0, x1, y1 = 48, 262, 372, 52      # plot area: wavelength 0-8 um across, radiance up
    lmax = 8.0
    Ts = [1200, 1500, 1800]
    top = _planck(2897.77 / 1800, 1800) * 1.08
    X = lambda lam: x0 + (x1 - x0) * lam / lmax
    Y = lambda b: y0 - (y0 - y1) * b / top
    lams = [0.25 + i * (lmax - 0.25) / 240 for i in range(241)]
    # construction: axes, wavelength ticks, the locus of peaks, and the two older laws for 1,800 K
    d.group('thin')
    d.lines([[(x, y0), (x, y0 + 4)] for x in (X(l) for l in range(0, 9))])
    peaks = [(X(2897.77 / T), Y(_planck(2897.77 / T, T))) for T in range(1100, 1901, 50)]
    d.line(*peaks)
    rj = [(X(l), Y(_rj(l, 1800))) for l in lams if Y(_rj(l, 1800)) > y1 - 30]
    d.line(*rj)
    wien = [(X(l), Y(_wien(l, 1800))) for l in lams]
    d.line(*wien)
    # the axes
    d.group()
    d.line((x0, y1 - 18), (x0, y0), (x1 + 6, y0))
    _arrow(d, x1 + 6, y0, 0, 4)
    _arrow(d, x0, y1 - 18, -math.pi / 2, 4)
    # Planck's curves
    d.group()
    for T in Ts:
        d.line(*[(X(l), Y(_planck(l, T))) for l in lams])
    # inset: the cavity, its hole and a ray trapped inside
    d.group('mid')
    cx, cy, w, h = 318, 92, 70, 44
    hole = 6
    d.line((cx - w / 2, cy - hole), (cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2),
           (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2), (cx - w / 2, cy + hole))
    ray = [(cx - w / 2 - 22, cy - 10), (cx - w / 2, cy - 2), (cx + w / 2, cy + 12),
           (cx + 6, cy + h / 2), (cx - 16, cy - h / 2), (cx + w / 2, cy - 4), (cx + 12, cy + h / 2)]
    d.line(*ray)
    _arrow(d, *ray[1], math.atan2(ray[1][1] - ray[0][1], ray[1][0] - ray[0][0]), 4)
    # labels
    d.group()
    for T in Ts:
        lp = 2897.77 / T
        d.text(X(lp) + 10, Y(_planck(lp, T)) - 4, f'{T} K', size=7, anchor='start')
    d.text(X(1.05), y1 - 8, 'RAYLEIGH–JEANS', size=7, anchor='start')
    d.text(X(5.2), Y(_wien(5.2, 1800)) + 12, 'WIEN', size=7, anchor='start')
    d.text(X(6.1), Y(_planck(6.1, 1800)) - 8, 'PLANCK', size=7, anchor='start')
    for l in (0, 2, 4, 6, 8):
        d.text(X(l), y0 + 14, str(l), size=7)
    d.text(x1, y0 + 26, 'WAVELENGTH, μm', size=7, anchor='end')
    d.text(cx, cy + h / 2 + 12, 'THE CAVITY', size=7)
    return d


def atoms_real():
    """Perrin's sedimentation cell (1908-09): gamboge grains of radius 0.212 um in a cell 100 um deep.

    The grains thin out upward exponentially, halving every 30 um, as a gas
    does under gravity every 6 km. The four planes at 5, 35, 65 and 95 um
    are where he counted them (100 : 47 : 22.6 : 12). Beside the cell, the
    exponential law as a construction curve, with his four counts on it."""
    d = D()
    bx0, bx1 = 70, 210                 # the cell, in plan units
    by0, by1 = 265, 45                  # bottom and top (100 um)
    um = (by0 - by1) / 100
    Y = lambda z: by0 - z * um
    planes = [5, 35, 65, 95]
    counts = [100, 47, 22.6, 12]
    # construction: the counting planes, carried across to the curve, and the halving heights
    d.group('thin')
    d.lines([[(bx0 - 6, Y(z)), (360, Y(z))] for z in planes])
    cx0, cx1 = 250, 360                 # the curve's axis: concentration 0-100 across
    d.line((cx0, by0), (cx0, by1 - 6))
    d.line(*[(cx0 + (cx1 - cx0) * 2 ** (-(z - 5) / 30), Y(z)) for z in range(0, 101, 2)])
    # the cell
    d.group()
    d.line((bx0, by1 - 10), (bx0, by0), (bx1, by0), (bx1, by1 - 10))
    d.line((bx0 - 10, by1 - 10), (bx1 + 10, by1 - 10))
    # the grains: a seeded sample of the exponential distribution
    d.group('mid')
    rng = random.Random(1908)
    lam = math.log(2) / 30
    n = 0
    while n < 150:
        z = -math.log(1 - rng.random()) / lam
        if z > 99:
            continue
        x = rng.uniform(bx0 + 4, bx1 - 4)
        d.circle(x, Y(z), 1.3)
        n += 1
    # the counts on the curve
    d.group()
    for z, c in zip(planes, counts):
        d.circle(cx0 + (cx1 - cx0) * c / 100, Y(z), 2.5)
    # the microscope's objective above, looking down through a pinhole
    d.group('mid')
    ox = (bx0 + bx1) / 2
    d.line((ox - 14, 8), (ox - 14, 20), (ox - 8, 28), (ox + 8, 28), (ox + 14, 20), (ox + 14, 8))
    # labels
    d.group()
    for z in planes:
        d.text(bx0 - 10, Y(z) + 3, f'{z} μm', size=7, anchor='end')
    d.text(cx0 + 4, by0 + 14, 'GRAINS COUNTED, 100 AT FOOT', size=7, anchor='start')
    d.text((bx0 + bx1) / 2, by0 + 14, 'GAMBOGE IN WATER', size=7)
    d.text(362, Y(50) - 26, 'HALF', size=7, anchor='end')
    d.text(362, Y(50) - 17, 'EVERY 30 μm', size=7, anchor='end')
    return d


def special_relativity():
    """The light clock: time dilation from Pythagoras, for a clock moving at 0.6 c.

    A pulse of light bounces between two mirrors. In the clock's own frame it
    goes straight up and down; seen by someone the clock passes at 0.6 c it
    runs on a slant, so each tick takes longer. The triangle is 3-4-5: while
    light travels 5 units the clock moves 3 and, in its own frame, the light
    has crossed only 4, so the moving clock runs at 4/5 of the rate of one at
    rest (1/gamma = 0.8)."""
    d = D()
    s = 32                              # plate units per unit of the 3-4-5 triangle
    base, top = 244, 244 - 4 * 32       # the mirrors are 4 units apart
    x0 = 56
    xs = [x0 + 3 * s * k for k in range(4)]   # the clock at each bounce, 3 units on
    ys = [base, top, base, top]
    # construction: the track, the first triangle's two legs and its right angle
    d.group('thin')
    d.line((30, base + 20), (386, base + 20))
    d.lines([[(x, base + 16), (x, base + 24)] for x in xs])
    d.line((xs[0], base), (xs[1], base), (xs[1], top))
    d.line((xs[1] - 8, base), (xs[1] - 8, base - 8), (xs[1], base - 8))
    # the moving clock at each bounce: two mirrors and the sides of its case
    d.group('mid')
    for x in xs:
        d.line((x - 14, top - 4), (x + 14, top - 4))
        d.line((x - 14, base + 4), (x + 14, base + 4))
        d.lines([[(x - 14, top - 4), (x - 14, base + 4)], [(x + 14, top - 4), (x + 14, base + 4)]])
    # the light's path, seen from the ground
    d.group()
    pts = list(zip(xs, ys))
    d.line(*pts)
    for a, b in zip(pts, pts[1:]):
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        _arrow(d, *m, math.atan2(b[1] - a[1], b[0] - a[0]), 5)
    # the clock's motion
    d.group('mid')
    d.line((x0 - 14, top - 26), (x0 + 40, top - 26))
    _arrow(d, x0 + 40, top - 26, 0, 4)
    # labels
    d.group()
    d.text((xs[0] + xs[1]) / 2 - 10, (top + base) / 2 - 2, '5', size=9, anchor='end')
    d.text(xs[1] + 18, (top + base) / 2 + 26, '4', size=9, anchor='start')
    d.text((xs[0] + xs[1]) / 2, base + 14, '3', size=9)
    d.text(x0 + 46, top - 23, '0.6 c', size=8, anchor='start')
    d.text(200, base + 40, 'LIGHT GOES 5 · CLOCK MOVES 3 · CLOCK TICKS 4', size=7)
    d.text(200, 30, 'THE LIGHT CLOCK · √(1 − v²/c²) = 0.8', size=7)
    return d


PLATES = {'black-body': black_body, 'atoms-real': atoms_real, 'special-relativity': special_relativity}
