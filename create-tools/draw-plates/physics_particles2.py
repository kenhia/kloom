"""physics plates, trail "The Standard Model", its last four frames (sprint 021). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _wavy(d, a, b, waves=6, amp=4):
    """A wavy line from a to b, the way a diagram draws a boson."""
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    n = waves * 16
    pts = []
    for i in range(n + 1):
        t = i / n
        w = amp * math.sin(2 * math.pi * waves * t)
        pts.append((x0 + ux * L * t - uy * w, y0 + uy * L * t + ux * w))
    d.line(*pts)


def electroweak():
    """The weak mixing angle, and the neutral current it predicted.

    Left: the electroweak theory's two neutral fields, W3 and B, as axes, and
    the photon and the Z as the same axes turned through the weak mixing
    angle, sin²θ_W = 0.231 (θ_W ≈ 28.7°). Under them, the couplings as a right
    triangle: legs g and g′ with g′/g = tan θ_W, and the electric charge e as
    its altitude, e = g sin θ_W = g′ cos θ_W. Right: the leptonic neutral
    current Gargamelle saw in 1973, a muon antineutrino scattering off an
    electron by exchanging a Z, drawn as a diagram."""
    d = D()
    th = math.asin(math.sqrt(0.231))          # the weak mixing angle
    cx, cy, R = 104, 118, 82
    # construction: the unit circle, the W3 and B axes, and the projections of the photon axis
    d.group('thin')
    d.circle(cx, cy, R)
    d.lines([[(cx - R - 8, cy), (cx + R + 8, cy)], [(cx, cy + R + 8), (cx, cy - R - 8)]])
    gx, gy = cx + R * math.sin(th), cy - R * math.cos(th)      # the photon axis, turned from W3 towards B
    d.lines([[(gx, gy), (gx, cy)], [(gx, gy), (cx, gy)]])
    # the rotated axes: the photon and the Z
    d.group()
    d.line((cx - R * math.sin(th), cy + R * math.cos(th)), (gx, gy))
    zx, zy = cx + R * math.cos(th), cy + R * math.sin(th)
    d.line((cx - R * math.cos(th), cy - R * math.sin(th)), (zx, zy))
    _arrow(d, gx, gy, math.atan2(gy - cy, gx - cx), 5)
    _arrow(d, zx, zy, math.atan2(zy - cy, zx - cx), 5)
    # the angle, marked twice: between W3 and the photon, and between B and the Z
    d.group('mid')
    d.arc(cx, cy, 30, -90, -90 + math.degrees(th), n=20)
    d.arc(cx, cy, 36, 0, math.degrees(th), n=20)
    # the coupling triangle: legs g (up) and g' (across), hypotenuse, and e as the altitude
    g, gp = 0.652, 0.652 * math.tan(th)
    ox, oy = 42, 282                          # the right angle; legs drawn 62 units per g, keeping g'/g
    A = (ox, oy - 62)
    B = (ox + 62 * gp / g, oy)
    d.group()
    d.line(A, (ox, oy), B, A, closed=True)
    ax_, ay_ = B[0] - A[0], B[1] - A[1]
    t = ((ox - A[0]) * ax_ + (oy - A[1]) * ay_) / (ax_ * ax_ + ay_ * ay_)
    foot = (A[0] + t * ax_, A[1] + t * ay_)
    d.group('mid')
    d.line((ox, oy), foot)
    d.line((ox + 5, oy), (ox + 5, oy - 5), (ox, oy - 5))
    # the diagram: antineutrino in and out along the top, electron in and out along the bottom, a Z between
    v1, v2 = (296, 96), (296, 212)
    d.group()
    d.line((222, 44), v1, (370, 44))
    d.line((222, 264), v2, (370, 264))
    _arrow(d, 259, 70, math.atan2(v1[1] - 44, v1[0] - 222), 5)
    _arrow(d, 333, 70, math.atan2(44 - v1[1], 370 - v1[0]), 5)
    _arrow(d, 259, 238, math.atan2(v2[1] - 264, v2[0] - 222), 5)
    _arrow(d, 333, 238, math.atan2(264 - v2[1], 370 - v2[0]), 5)
    d.group('mid')
    _wavy(d, v1, v2, waves=7, amp=5)
    d.circle(v1[0], v1[1], 2.5)
    d.circle(v2[0], v2[1], 2.5)
    # labels
    d.group()
    d.text(cx, cy - R - 12, 'W3', size=8)
    d.text(cx + R + 12, cy + 3, 'B', size=8, anchor='start')
    d.text(gx + 4, gy - 8, 'PHOTON', size=7, anchor='start')
    d.text(zx + 6, zy + 10, 'Z', size=8, anchor='start')
    d.text(cx + 14, cy - 36, 'θW', size=7, anchor='start')
    d.text(ox - 5, oy - 30, 'g', size=8, anchor='end')
    d.text((ox + B[0]) / 2, oy + 11, "g′", size=8)
    d.text(foot[0] + 7, foot[1] - 2, 'e', size=8, anchor='start')
    d.text(118, 270, 'sin²θW = 0.231', size=7, anchor='start')
    d.text(216, 40, 'ν̄μ', size=8, anchor='end')
    d.text(216, 268, 'e⁻', size=8, anchor='end')
    d.text(306, 158, 'Z⁰', size=8, anchor='start')
    d.text(296, 292, 'NO CHARGE CHANGES HANDS', size=7)
    return d


def asymptotic_freedom():
    """The strong coupling α_s against the energy of the collision, on a log scale.

    One-loop running from the 2025 world average α_s(M_Z) = 0.1180, with five
    quark flavours throughout: α_s(Q) = α_s(M_Z) / (1 + b₀ α_s(M_Z) ln(Q²/M_Z²)),
    b₀ = 23/12π. The curve is this plate's own computation, not a fit to data,
    and one loop understates the rise below a few GeV. Inset: a three-jet
    event, a quark, an antiquark and a gluon flying apart in one plane."""
    d = D()
    x0, x1 = 44, 380                          # 1 GeV to 1000 GeV
    y0, y1 = 262, 30                          # alpha_s 0 to 0.4
    X = lambda q: x0 + (x1 - x0) * math.log10(q) / 3
    Y = lambda a: y0 - (y0 - y1) * a / 0.4
    a_z, mz = 0.1180, 91.188
    b0 = 23 / (12 * math.pi)
    alpha = lambda q: a_z / (1 + b0 * a_z * math.log(q * q / (mz * mz)))
    # construction: axes, decade ticks and gridlines, and the level of the Z
    d.group('thin')
    d.line((x0, y1 - 6), (x0, y0), (x1 + 6, y0))
    d.lines([[(X(10 ** k), y0), (X(10 ** k), y0 + 5)] for k in range(4)])
    d.lines([[(X(m * 10 ** k), y0), (X(m * 10 ** k), y0 + 2.5)] for k in range(3) for m in range(2, 10)])
    d.lines([[(x0 - 4, Y(a)), (x0, Y(a))] for a in (0.1, 0.2, 0.3, 0.4)])
    d.lines([[(X(mz), y0), (X(mz), Y(a_z))], [(x0, Y(a_z)), (X(mz), Y(a_z))]])
    # the running coupling
    d.group()
    pts = [(X(10 ** (3 * i / 150)), Y(alpha(10 ** (3 * i / 150)))) for i in range(151)]
    d.line(*pts)
    d.circle(X(mz), Y(a_z), 3)
    # inset: three jets in a plane, the gluon's the softest
    ix, iy = 300, 92
    d.group('thin')
    d.circle(ix, iy, 40)
    d.group()
    for ang, L in ((200, 36), (-25, 34), (95, 26)):
        a = math.radians(ang)
        for off in (-7, 0, 7):
            b = math.radians(ang + off)
            d.line((ix, iy), (ix + L * math.cos(b), iy + L * math.sin(b)))
    # labels
    d.group()
    for k, lab in enumerate(('1', '10', '100', '1000')):
        d.text(X(10 ** k), y0 + 15, lab, size=7)
    d.text(x1, y0 + 26, 'GeV', size=7, anchor='end')
    for a in (0.1, 0.2, 0.3):
        d.text(x0 - 7, Y(a) + 3, f'{a:.1f}', size=7, anchor='end')
    d.text(x0 + 6, y1 + 4, 'αs', size=8, anchor='start')
    d.text(X(mz) + 6, Y(a_z) - 7, 'Z MASS · 0.118', size=7, anchor='start')
    d.text(X(1.5) + 10, Y(alpha(1.5)) - 4, '← CONFINED', size=7, anchor='start')
    d.text(X(400), Y(alpha(400)) + 16, 'FREER →', size=7)
    d.text(ix, iy + 54, 'q · q̄ · g', size=7)
    return d


def w_and_z():
    """The proton–antiproton collider in plan, and stochastic cooling in the accumulator.

    Left: the SPS ring (7 km round, not to scale against the rest) with protons
    and antiprotons running opposite ways in one pipe, colliding in UA1 and UA2.
    Right: the Antiproton Accumulator. A pickup senses how far the antiprotons
    passing it stray from the ideal orbit; the signal is amplified and sent
    across the ring by a shortcut, so that it reaches a kicker at the same time
    as the particles that made it, and the kicker nudges them back. The drawn
    particle's excursion about the orbit shrinks after each kick."""
    d = D()
    # the SPS
    sx, sy, sr = 108, 150, 82
    d.group('thin')
    d.circle(sx, sy, sr + 10)
    d.circle(sx, sy, sr - 10)
    d.group()
    d.circle(sx, sy, sr)
    d.group('mid')
    d.arc(sx, sy, sr + 5, 200, 250, n=20)
    _arrow(d, sx + (sr + 5) * math.cos(math.radians(250)), sy + (sr + 5) * math.sin(math.radians(250)),
           math.radians(250 + 90), 5)
    d.arc(sx, sy, sr - 5, 340, 290, n=20)
    _arrow(d, sx + (sr - 5) * math.cos(math.radians(290)), sy + (sr - 5) * math.sin(math.radians(290)),
           math.radians(290 - 90), 5)
    for ang in (70, 135):                     # the two collision halls
        a = math.radians(ang)
        px, py = sx + sr * math.cos(a), sy + sr * math.sin(a)
        d.line((px - 8, py - 8), (px + 8, py - 8), (px + 8, py + 8), (px - 8, py + 8), closed=True)
    # the accumulator: a rounded square ring, a pickup on one side, a kicker on the other,
    # and the signal's shortcut straight across between them
    ax, ay, h = 300, 150, 62
    def at(s):
        """The point s units round the ring from its left-hand side, with the outward normal there."""
        ang = math.pi + s / h
        return (ax + h * math.cos(ang), ay + h * math.sin(ang)), (math.cos(ang), math.sin(ang))
    total = 2 * math.pi * h
    d.group('thin')
    d.circle(ax, ay, h)
    # one antiproton's excursion about the orbit: undamped as far as the kicker, then shrinking
    d.group('mid')
    n = 400
    pts = []
    for i in range(n + 1):
        (px, py), (nx, ny) = at(total * 0.97 * i / n)
        frac = i / n / 0.97
        amp = 8 if frac < 0.5 else 8 * math.exp(-(frac - 0.5) / 0.14)
        w = amp * math.sin(2 * math.pi * 9.5 * i / n)
        pts.append((px + nx * w, py + ny * w))
    d.line(*pts)
    # the pickup, the kicker, the shortcut and its amplifier
    d.group()
    pick, kick = (ax - h, ay), (ax + h, ay)
    for x, y in (pick, kick):
        d.line((x - 5, y - 9), (x + 5, y - 9), (x + 5, y + 9), (x - 5, y + 9), closed=True)
    d.line((pick[0] + 5, ay), (ax - 9, ay))
    d.line((ax + 9, ay), (kick[0] - 5, ay))
    d.line((ax - 9, ay - 10), (ax + 9, ay), (ax - 9, ay + 10), closed=True)
    _arrow(d, kick[0] - 6, ay, 0, 4)
    # labels
    d.group()
    d.text(sx, sy - 4, 'SPS', size=8)
    d.text(sx, sy + 8, '270 + 270 GeV', size=7)
    d.text(sx + sr * math.cos(math.radians(70)) + 12, sy + sr * math.sin(math.radians(70)) + 10, 'UA1', size=7, anchor='start')
    d.text(sx + sr * math.cos(math.radians(135)) - 12, sy + sr * math.sin(math.radians(135)) + 10, 'UA2', size=7, anchor='end')
    d.text(sx - 40, sy - sr - 16, 'p', size=8)
    d.text(sx + 44, sy - sr - 16, 'p̄', size=8)
    d.text(ax, ay - h - 12, 'ANTIPROTON ACCUMULATOR', size=7)
    d.text(pick[0] + 9, pick[1] - 14, 'PICKUP', size=7, anchor='start')
    d.text(kick[0] - 9, kick[1] + 20, 'KICKER', size=7, anchor='end')
    d.text(ax, ay + h + 22, 'STOCHASTIC COOLING', size=7)
    return d


def higgs():
    """The Higgs potential, V(φ) = λ(|φ|² − v²)², in perspective.

    The field's lowest energy is not at φ = 0 but round a circle of radius v,
    so the field settles somewhere on the rim. Motion round the trough costs
    nothing (the would-be Goldstone mode, taken up by the W and Z as their
    third polarisation); motion across it, up the walls, is the massive mode,
    the Higgs boson."""
    d = D()
    cx, cy = 200, 200
    k = 0.3                                   # perspective: a circle of radius r is an ellipse r by k·r
    v, rmax = 98, 142
    hscale = 130
    def V(r):
        u = r / v
        return (u * u - 1) ** 2
    def P(r, ang):
        return (cx + r * math.cos(ang), cy + k * r * math.sin(ang) - hscale * min(V(r), 1.25) / 1.25 * 1.0)
    # construction: the axis of symmetry, the floor plane's circle of radius v, and its radius
    d.group('thin')
    d.line((cx, cy + 40), (cx, cy - hscale - 36))
    d.ellipse(cx, cy, v, k * v)
    d.ellipse(cx, cy, rmax, k * rmax)
    d.line((cx, cy), (cx + v, cy))
    # the surface: rings at constant radius and radial profiles
    d.group('mid')
    for r in (22, 46, 72, 118, rmax):
        d.line(*[P(r, 2 * math.pi * i / 72) for i in range(73)])
    for j in range(12):
        ang = 2 * math.pi * j / 12
        d.line(*[P(rmax * i / 60, ang) for i in range(61)])
    # the profile at the front, drawn full weight, and the trough
    d.group()
    d.line(*[(cx - rmax + 2 * rmax * i / 120, cy - hscale * min(V(abs(-rmax + 2 * rmax * i / 120)), 1.25) / 1.25)
             for i in range(121)])
    d.line(*[P(v, 2 * math.pi * i / 90) for i in range(91)])
    bx, by = P(v, math.pi / 2)
    d.circle(bx, by - 6, 6)
    # the two modes: round the trough and across it
    d.group('mid')
    d.line(*[P(v, math.pi / 2 + 0.42 + 0.45 * i / 20) for i in range(21)])
    e = P(v, math.pi / 2 + 0.87)
    e0 = P(v, math.pi / 2 + 0.85)
    _arrow(d, e[0], e[1], math.atan2(e[1] - e0[1], e[0] - e0[0]), 5)
    d.line((bx + 16, by - 30), (bx + 16, by + 14))
    _arrow(d, bx + 16, by - 30, -math.pi / 2, 5)
    _arrow(d, bx + 16, by + 14, math.pi / 2, 5)
    # labels
    d.group()
    d.text(cx + 6, cy - hscale - 30, 'V(φ)', size=8, anchor='start')
    d.text(cx + v / 2, cy - 4, 'v', size=8)
    d.text(bx + 24, by - 10, 'HIGGS', size=7, anchor='start')
    d.text(e[0] - 6, e[1] + 14, 'EATEN BY W, Z', size=7, anchor='end')
    d.text(200, 290, 'v = 246 GeV', size=8)
    return d


PLATES = {'electroweak': electroweak, 'asymptotic-freedom': asymptotic_freedom, 'w-and-z': w_and_z, 'higgs': higgs}


def z_lineshape_chart():
    """The w-and-z reading's chart: the hadronic cross-section near the Z peak for 2, 3 and 4 light neutrinos.

    A Born-level Breit–Wigner (no radiative corrections) computed from the PDG
    2025 Z parameters: M_Z = 91.188 GeV, Γ(ℓℓ) = 83.984 MeV, Γ(hadrons) =
    1744.4 MeV, Γ(invisible) = 499.3 MeV shared by three neutrinos (166.4 MeV
    each). Each extra neutrino widens the Z and lowers its peak. Run this file
    with the argument `z-lineshape` to write the SVG into the frame."""
    M, Gee, Gh, Gnu = 91.188, 0.083984, 1.7444, 0.4993 / 3
    GEV2_NB = 389379.0
    def sigma(E, N):
        G = Gh + 3 * Gee + N * Gnu
        s = E * E
        return 12 * math.pi / M ** 2 * Gee * Gh * s * G * G / ((s - M * M) ** 2 + M * M * G * G) / G ** 2 * GEV2_NB
    x0, x1, y0, y1 = 56, 384, 236, 24
    e0, e1, smax = 88.0, 94.5, 50.0
    X = lambda e: x0 + (x1 - x0) * (e - e0) / (e1 - e0)
    Y = lambda v: y0 - (y0 - y1) * v / smax
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 280" role="img" aria-labelledby="t d">',
           '<title id="t">The Z peak for two, three and four kinds of light neutrino</title>',
           '<desc id="d">Line chart of the cross-section for electron–positron collisions to make hadrons, '
           'in nanobarns, against collision energy from 88 to 94.5 GeV. Three curves peak at 91.19 GeV: '
           'with two light neutrinos at 47.7 nanobarns, with three at 41.5, with four at 36.5. '
           'Born-level curves computed for kloom from the Particle Data Group 2025 Z parameters.</desc>',
           '<g font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="currentColor">',
           '<g class="muted">']
    for v in (0, 10, 20, 30, 40, 50):
        op, w = ('0.9', '1') if v == 0 else ('0.3', '0.6')
        out.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="currentColor" stroke-opacity="{op}" stroke-width="{w}"/>')
        out.append(f'<text x="{x0 - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    for e in (88, 89, 90, 91, 92, 93, 94):
        out.append(f'<line x1="{X(e):.1f}" x2="{X(e):.1f}" y1="{y0}" y2="{y0 + 4}" stroke="currentColor" stroke-width="1"/>')
        out.append(f'<text x="{X(e):.1f}" y="{y0 + 17}" text-anchor="middle">{e}</text>')
    out.append(f'<text x="{x1}" y="{y0 + 32}" text-anchor="end">collision energy, GeV</text>')
    out.append(f'<text x="{x0 - 44}" y="{y1 - 8}" text-anchor="start">nb</text>')
    out.append('</g>')
    for N, cls, w in ((2, 'muted', '1.2'), (4, 'muted', '1.2'), (3, 'accent', '2')):
        pts = ' '.join(f'{X(e0 + (e1 - e0) * i / 200):.1f},{Y(sigma(e0 + (e1 - e0) * i / 200, N)):.1f}' for i in range(201))
        dash = ' stroke-dasharray="4 3"' if N != 3 else ''
        out.append(f'<polyline class="{cls}" points="{pts}" fill="none" stroke="currentColor" stroke-width="{w}"{dash}/>')
        pk = sigma(M, N)
        out.append(f'<text class="{cls}" x="{X(92.3):.1f}" y="{Y(pk) + 4:.1f}" text-anchor="start">{N} ν · {pk:.1f}</text>')
    out += ['</g>', '</svg>']
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    import os, sys
    if sys.argv[1:] == ['z-lineshape']:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, '..', '..', 'subjects', 'physics', 'frames', 'w-and-z', 'z-peak.svg')
        with open(path, 'w') as fh:
            fh.write(z_lineshape_chart())
        print('wrote', os.path.normpath(path))
