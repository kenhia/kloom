"""physics plates, segment "Heat, light and charge": Young, Carnot, energy, spectra (sprint 021). See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def young_slits():
    """Two slits as Young described them: crests spreading from S1 and S2, and the fringes on a far screen.

    The slits are d apart and the screen L away; a point at height y on the
    screen lies farther from one slit than the other by about d·y/L, and the
    brightness there goes as cos²(π d y / λ L). The rays drawn run to the
    central bright fringe, the first dark one and the first bright one beside it."""
    d = D()
    sx, cy = 118, 150            # the slit screen and the axis
    half = 20                     # half the slit spacing, in plate units
    s1, s2 = (sx, cy - half), (sx, cy + half)
    wx = 306                      # the viewing screen
    lam = 17                      # the wavelength, in plate units
    L = wx - sx
    fringe = lam * L / (2 * half)  # fringe spacing on the screen
    # construction: the axis, the rays from both slits to three points, and the source
    d.group('thin')
    d.line((24, cy), (wx + 8, cy))
    for y in (cy, cy - fringe / 2, cy - fringe):
        d.lines([[s1, (wx, y)], [s2, (wx, y)]])
    d.line((40, cy), s1)
    d.line((40, cy), s2)
    # the object: the source slit, the screen with two slits, the viewing screen
    d.group()
    d.line((40, cy - 40), (40, cy - 3))
    d.line((40, cy + 3), (40, cy + 40))
    d.line((sx, 40), (sx, s1[1] - 3))
    d.line((sx, s1[1] + 3), (sx, s2[1] - 3))
    d.line((sx, s2[1] + 3), (sx, 260))
    d.line((wx, 44), (wx, 256))
    # the crests: circles about each slit, one wavelength apart, on the far side only
    d.group('mid')
    for k in range(1, int((L - 10) / lam) + 1):
        r = k * lam
        a = min(62, math.degrees(math.asin(min(1, 108 / r))))
        for (x0, y0) in (s1, s2):
            d.arc(x0, y0, r, -a, a, n=24)
    # the fringes: brightness against height on the screen, drawn outward from it
    d.group()
    pts = []
    for i in range(0, 211):
        y = 45 + i
        b = math.cos(math.pi * (y - cy) / fringe) ** 2
        pts.append((wx + 4 + 44 * b, y))
    d.line(*pts)
    # labels
    d.group()
    d.text(sx - 6, s1[1] - 4, 'S1', size=7, anchor='end')
    d.text(sx - 6, s2[1] + 10, 'S2', size=7, anchor='end')
    d.text(40, cy + 54, 'S0', size=7)
    d.text(wx + 52, cy + 3, 'LIGHT', size=7, anchor='start')
    d.text(wx + 8, cy - fringe / 2 + 3, 'DARK', size=7, anchor='start')
    d.text(200, 22, 'PATHS DIFFER BY 0, ½, 1 WAVE', size=8)
    d.text(200, 288, 'FRINGE SPACING = λ L / d', size=8)
    return d


def carnot():
    """Carnot's cycle on Clapeyron's diagram of pressure against volume, for a monatomic ideal gas (γ = 5/3).

    Two isotherms (pV constant) and two adiabats (pV^γ constant) bound the
    cycle; the hatched area inside it is the work done in one turn. The
    isotherms and adiabats run on past the cycle as construction lines."""
    d = D()
    x0, y0 = 60, 262              # the origin of the axes
    sx, sy = 46, 27               # plate units per unit of volume and of pressure
    g = 5 / 3
    Th, Tc = 1.0, 0.5             # the two temperatures, as pV for one unit of gas
    vA, vB = 1.0, 2.1             # the hot isotherm runs from A to B
    vC = vB * (Th / Tc) ** (1 / (g - 1))
    vD = vA * (Th / Tc) ** (1 / (g - 1))
    P = lambda v, T: T * 8 / v    # pressure on an isotherm (scaled so the plate fills)
    Pad = lambda v, v1, T1: P(v1, T1) * (v1 / v) ** g
    xy = lambda v, p: (x0 + sx * v, y0 - sy * p)
    # construction: the axes' ticks, and the four curves carried on beyond the cycle
    d.group('thin')
    d.lines([[(x0 + sx * v, y0), (x0 + sx * v, y0 + 4)] for v in range(1, 7)])
    d.lines([[(x0 - 4, y0 - sy * p), (x0, y0 - sy * p)] for p in range(1, 9)])
    d.line(*[xy(0.95 + i * 0.05, P(0.95 + i * 0.05, Th)) for i in range(0, 115)])
    d.line(*[xy(0.6 + i * 0.05, P(0.6 + i * 0.05, Tc)) for i in range(0, 122)])
    d.line(*[xy(vB * 0.8 + i * 0.05, Pad(vB * 0.8 + i * 0.05, vB, Th)) for i in range(0, int((vC * 1.12 - vB * 0.8) / 0.05))])
    d.line(*[xy(vA * 0.85 + i * 0.05, Pad(vA * 0.85 + i * 0.05, vA, Th)) for i in range(0, int((vD * 1.15 - vA * 0.85) / 0.05))])
    # the axes
    d.group()
    d.line((x0, 30), (x0, y0), (372, y0))
    _arrow(d, x0, 30, -math.pi / 2, 5)
    _arrow(d, 372, y0, 0, 5)
    # the cycle, A to B to C to D and back
    d.group()
    seg = lambda a, b, f: [xy(a + (b - a) * i / 40, f(a + (b - a) * i / 40)) for i in range(41)]
    ab = seg(vA, vB, lambda v: P(v, Th))
    bc = seg(vB, vC, lambda v: Pad(v, vB, Th))
    cd = seg(vC, vD, lambda v: P(v, Tc))
    da = seg(vD, vA, lambda v: Pad(v, vA, Th))
    d.line(*(ab + bc[1:] + cd[1:] + da[1:]), closed=True)
    for pts in (ab, bc, cd, da):
        (xa, ya), (xb, yb) = pts[19], pts[21]
        _arrow(d, pts[20][0], pts[20][1], math.atan2(yb - ya, xb - xa), 5)
    # the work: vertical hatching inside the cycle
    d.group('mid')
    hatch = []
    v = vA + 0.12
    while v < vC:
        top = P(v, Th) if v <= vB else Pad(v, vB, Th)
        bot = Pad(v, vA, Th) if v <= vD else P(v, Tc)
        if top - bot > 0.08:
            hatch.append([xy(v, bot + 0.03), xy(v, top - 0.03)])
        v += 0.12
    d.lines(hatch)
    # labels
    d.group()
    for name, (v, p) in (('A', (vA, P(vA, Th))), ('B', (vB, P(vB, Th))), ('C', (vC, P(vC, Tc))), ('D', (vD, P(vD, Tc)))):
        x, y = xy(v, p)
        d.text(x + (7 if name in 'BC' else -7), y - 6, name, size=8, anchor='start' if name in 'BC' else 'end')
    hx, hy = xy(1.5, P(1.5, Th))
    d.text(hx + 10, hy - 4, 'HOT · T1', size=7, anchor='start')
    kx, ky = xy(4.2, P(4.2, Tc))
    d.text(kx, ky + 16, 'COLD · T2', size=7)
    d.text(x0 - 10, 26, 'p', size=9)
    d.text(376, y0 + 16, 'V', size=9, anchor='end')
    d.text(220, 22, 'ISOTHERMS pV · ADIABATS pVᵞ', size=8)
    d.text(220, 292, 'WORK PER CYCLE = AREA ENCLOSED', size=8)
    return d


def energy():
    """Joule's paddle-wheel experiment of 1845–50: a falling weight in elevation, and the wheel in plan.

    Weights falling a measured height turn, by a cord round a roller, a brass
    paddle-wheel whose eight revolving arms work between four sets of fixed
    vanes (Joule 1850, Plate VII, figs. 1–2). The water it churns warms."""
    d = D()
    # the elevation, left: a pulley, the cord and the weight, with the fall measured beside it
    px, py, pr = 78, 70, 20
    wx = px + pr
    d.group('thin')
    d.lines([[(40, y), (46, y)] for y in range(100, 261, 16)])
    d.line((43, 100), (43, 260))
    d.line((wx, 176), (wx, 250))
    d.line((wx - 18, 262), (wx + 18, 262))
    d.line((px - pr, py), (150, py))
    d.group()
    d.circle(px, py, pr)
    d.circle(px, py, 3)
    d.line((wx, py), (wx, 150))
    d.line((wx - 12, 150), (wx + 12, 150), (wx + 12, 176), (wx - 12, 176), closed=True)
    d.line((px - pr, py), (158, py))
    _arrow(d, wx, 244, math.pi / 2, 5)
    # the plan, right: the copper vessel, the axis and its eight revolving arms, the four fixed vanes
    cx, cy, R = 272, 160, 92
    d.group('thin')
    d.lines([[(cx - R - 10, cy), (cx + R + 10, cy)], [(cx, cy - R - 10), (cx, cy + R + 10)]])
    d.circle(cx, cy, 72)
    d.circle(cx, cy, 30)
    d.group()
    d.circle(cx, cy, R)
    d.circle(cx, cy, R - 5)
    d.circle(cx, cy, 8)
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        c, s = math.cos(a), math.sin(a)
        n = (-s * 5, c * 5)
        r0, r1 = 12, 66
        d.line((cx + c * r0 + n[0], cy + s * r0 + n[1]), (cx + c * r1 + n[0], cy + s * r1 + n[1]),
               (cx + c * r1 - n[0], cy + s * r1 - n[1]), (cx + c * r0 - n[0], cy + s * r0 - n[1]), closed=True)
    d.group('mid')
    for k in range(4):
        a = math.radians(90 * k)
        for off in (-9, 9):
            b = a + math.radians(off)
            d.line((cx + math.cos(b) * 36, cy + math.sin(b) * 36), (cx + math.cos(b) * (R - 5), cy + math.sin(b) * (R - 5)))
    d.arc(cx, cy, 80, 200, 250, n=20)
    e = math.radians(250)
    _arrow(d, cx + 80 * math.cos(e), cy + 80 * math.sin(e), e + math.pi / 2, 5)
    # labels
    d.group()
    d.text(wx + 20, 166, 'W', size=8, anchor='start')
    d.text(30, 184, 'h', size=9, anchor='end')
    d.text(88, 284, 'FALL', size=7)
    d.text(cx, 284, 'PLAN · 8 ARMS · 4 VANE SETS', size=7)
    d.text(200, 22, 'WORK W·h BECOMES HEAT IN WATER', size=8)
    return d


def spectra():
    """A prism spectroscope in plan, and the Balmer lines of hydrogen on a scale of wavelength.

    The prism (60°, flint glass, n ≈ 1.64 at the D line, with a Cauchy
    dispersion drawn four times too strong to be seen) bends red least and violet most; the rays are traced by
    Snell's law. Below, the lines λ = 364.56 nm × n²/(n² − 4) for n = 3 to 30
    close up on the series limit."""
    d = D()
    # the prism: equilateral, apex up
    cx, cy, side = 200, 118, 90
    hgt = side * math.sqrt(3) / 2
    A = (cx, cy - hgt * 2 / 3)
    B = (cx - side / 2, cy + hgt / 3)
    C = (cx + side / 2, cy + hgt / 3)
    n_of = lambda lam: 1.55 + 32800 / lam ** 2     # a Cauchy fit, its dispersion drawn four times too strong

    def unit(v):
        m = math.hypot(*v)
        return (v[0] / m, v[1] / m)

    def refract(u, nrm, n1, n2):
        """Snell's law in vector form: u the ray, nrm the unit normal against it."""
        c1 = -(u[0] * nrm[0] + u[1] * nrm[1])
        r = n1 / n2
        k = 1 - r * r * (1 - c1 * c1)
        c2 = math.sqrt(k)
        return unit((r * u[0] + (r * c1 - c2) * nrm[0], r * u[1] + (r * c1 - c2) * nrm[1]))

    def hit(p, u, a, b):
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = u[0] * ey - u[1] * ex
        t = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / den
        return (p[0] + u[0] * t, p[1] + u[1] * t)

    nl = unit((-(B[1] - A[1]), B[0] - A[0]))        # the left face's normal
    if nl[0] > 0:
        nl = (-nl[0], -nl[1])
    nr = unit((C[1] - A[1], -(C[0] - A[0])))        # the right face's normal
    if nr[0] < 0:
        nr = (-nr[0], -nr[1])
    # the beam: at minimum deviation for the D line, symmetric about the prism's axis
    nD = n_of(589)
    th = math.asin(nD * math.sin(math.radians(30)))
    base = math.atan2(nl[1], nl[0]) + math.pi         # pointing into the glass along the normal
    u0 = (math.cos(base - th), math.sin(base - th))
    M1 = ((A[0] * 0.45 + B[0] * 0.55), (A[1] * 0.45 + B[1] * 0.55))

    def trace(lam):
        n = n_of(lam)
        u1 = refract(u0, nl, 1.0, n)
        P2 = hit(M1, u1, A, C)
        u2 = refract(u1, (-nr[0], -nr[1]), n, 1.0)
        return P2, u2
    src = (M1[0] - 120 * u0[0], M1[1] - 120 * u0[1])
    # construction: the normals to both faces, and the incoming beam carried on undeviated
    d.group('thin')
    d.line((M1[0] + 22 * nl[0], M1[1] + 22 * nl[1]), (M1[0] - 22 * nl[0], M1[1] - 22 * nl[1]))
    d.line(M1, (M1[0] + 150 * u0[0], M1[1] + 150 * u0[1]))
    P2, _ = trace(589)
    d.line((P2[0] + 22 * nr[0], P2[1] + 22 * nr[1]), (P2[0] - 22 * nr[0], P2[1] - 22 * nr[1]))
    # the object: the slit and its beam, the prism
    d.group()
    d.line(src, M1)
    d.line(A, B, C, closed=True)
    pa = (-u0[1], u0[0])
    d.line((src[0] + 9 * pa[0], src[1] + 9 * pa[1]), (src[0] + 2 * pa[0], src[1] + 2 * pa[1]))
    d.line((src[0] - 9 * pa[0], src[1] - 9 * pa[1]), (src[0] - 2 * pa[0], src[1] - 2 * pa[1]))
    # the dispersed rays: red, the D line, blue, violet
    d.group('mid')
    ends = []
    for lam in (656, 589, 486, 410):
        Pin, u2 = trace(lam)
        e = (Pin[0] + 120 * u2[0], Pin[1] + 120 * u2[1])
        ends.append(e)
        d.line(M1, Pin, e)
    # the scale of wavelength, and the Balmer lines on it
    y0, x_lo, x_hi, lam_lo, lam_hi = 236, 30, 370, 350, 700
    X = lambda lam: x_lo + (lam - lam_lo) / (lam_hi - lam_lo) * (x_hi - x_lo)
    d.group('thin')
    d.lines([[(X(l), y0 + 18), (X(l), y0 + 22)] for l in range(350, 701, 50)])
    d.line((X(364.56), y0 - 26), (X(364.56), y0 + 18))
    d.group()
    d.line((x_lo, y0 + 18), (x_hi, y0 + 18))
    lines = []
    for n in range(3, 31):
        lam = 364.56 * n * n / (n * n - 4)
        h = 22 if n <= 6 else max(6, 22 - (n - 6) * 0.8)
        lines.append([(X(lam), y0 + 18 - h), (X(lam), y0 + 18)])
    d.lines(lines)
    # labels
    d.group()
    for n, name in ((3, 'Hα'), (4, 'Hβ'), (5, 'Hγ'), (6, 'Hδ')):
        lam = 364.56 * n * n / (n * n - 4)
        d.text(X(lam), y0 - 8, name, size=7)
    d.text(X(364.56) + 2, y0 - 30, 'LIMIT 364.6', size=7, anchor='start')
    for l in (400, 500, 600, 700):
        d.text(X(l), y0 + 32, str(l), size=7)
    d.text(370, 290, 'NM', size=7, anchor='end')
    d.text(src[0], src[1] + 16, 'SLIT', size=7)
    d.text(ends[0][0] + 4, ends[0][1] - 4, 'RED', size=7, anchor='start')
    d.text(ends[-1][0] + 4, ends[-1][1] + 9, 'VIOLET', size=7, anchor='start')
    d.text(200, 22, 'λ = 364.56 · n² / (n² − 4)', size=8)
    return d


PLATES = {'young-slits': young_slits, 'carnot': carnot, 'energy': energy, 'spectra': spectra}
