"""physics plates, segment "Relativity": gravity (sprint 021). See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _ray(b, rs=1.0, phi_max=2 * math.pi, steps=4000):
    """A light ray past a Schwarzschild mass, in units of rs, coming in from the left along y = b.

    Integrates the orbit equation u'' = -u + (3/2) rs u^2 (u = 1/r) in the angle phi,
    starting far away. Returns (points, captured)."""
    r0 = 40.0
    phi0 = math.pi - math.asin(b / r0)  # far to the left, at height b
    u, phi = 1 / r0, phi0
    # du/dphi at the start, from (du/dphi)^2 = 1/b^2 - u^2 (1 - rs u); moving in, u increases as phi decreases
    du = -math.sqrt(max(1 / b ** 2 - u * u * (1 - rs * u), 0))
    h = -phi_max / steps
    pts = []
    for _ in range(steps):
        r = 1 / u
        pts.append((r * math.cos(phi), r * math.sin(phi)))
        if u >= 1 / rs:
            return pts, True
        if u <= 1 / r0 and len(pts) > 10:
            return pts, False
        # RK4 on (u, du) with respect to phi (step h, negative so the ray runs left to right below)
        def f(uu, vv):
            return vv, -uu + 1.5 * rs * uu * uu
        k1 = f(u, du)
        k2 = f(u + h / 2 * k1[0], du + h / 2 * k1[1])
        k3 = f(u + h / 2 * k2[0], du + h / 2 * k2[1])
        k4 = f(u + h * k3[0], du + h * k3[1])
        u += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        du += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        phi += h
    return pts, False


def general_relativity():
    """Starlight bent by the Sun, as the 1919 eclipse expeditions measured it.

    A grid of straight lines pulled towards the Sun (each point displaced
    inward by an amount falling off as 1/r, a picture of the deflection, not
    a metric) stands for curved space. The ray from a star grazes the Sun and
    bends towards it; seen from the Earth, the star appears along the ray's
    final direction, displaced outward from its true place. The bend is
    exaggerated about 100,000 times."""
    d = D()
    sx, sy, R = 200, 170, 34            # the Sun (and the Moon's disc over it)
    k = 900.0                           # the grid's pull, in plate units squared

    def pull(x, y):
        dx, dy = x - sx, y - sy
        r = math.hypot(dx, dy)
        if r < 1:
            return x, y
        s = min(k / (r * r), 0.8 * (r - R * 0.6) / r) if r > R * 0.6 else 0
        return x - dx * s, y - dy * s

    # construction: the pulled grid, stopping short of the Sun
    d.group('thin')
    segs = []
    for gx in range(40, 361, 20):
        # split where the Sun interrupts the line
        run = []
        for gy in range(40, 281, 4):
            if math.hypot(gx - sx, gy - sy) > R + 6:
                run.append(pull(gx, gy))
            elif run:
                segs.append(run)
                run = []
        if run:
            segs.append(run)
    for gy in range(50, 291, 20):
        run = []
        for gx in range(40, 361, 4):
            if math.hypot(gx - sx, gy - sy) > R + 6:
                run.append(pull(gx, gy))
            elif run:
                segs.append(run)
                run = []
        if run:
            segs.append(run)
    d.lines(segs)
    # the Sun under the Moon's disc, and its corona's first ring
    d.group()
    d.circle(sx, sy, R)
    # the ray: from a star at the left, bent where it grazes the Sun, on to the Earth at the right
    star = (24, 110)
    g = (sx, sy - R - 5)                 # where the ray grazes the limb
    s_in = (g[1] - star[1]) / (g[0] - star[0])
    s_out = s_in + 0.19                  # the bend, towards the Sun
    earth = (376, g[1] + s_out * (376 - g[0]))
    k0, k1 = (g[0] - 24, g[1] - 24 * s_in), (g[0] + 24, g[1] + 24 * s_out)
    d.path(f'M{star[0]} {star[1]} L{k0[0]:.1f} {k0[1]:.1f} Q{g[0]:.1f} {g[1]:.1f} {k1[0]:.1f} {k1[1]:.1f} '
           f'L{earth[0]:.1f} {earth[1]:.1f}')
    d.circle(earth[0], earth[1], 5)
    d.lines([[(star[0] - 5, star[1]), (star[0] + 5, star[1])], [(star[0], star[1] - 5), (star[0], star[1] + 5)]])
    # secondary: the line of sight back from the Earth along the ray's last direction, to the apparent star
    d.group('mid')
    app = (star[0], g[1] - s_out * (g[0] - star[0]))
    d.line(k1, app)
    d.circle(app[0], app[1], 3)
    a_app = math.atan2(app[1] - earth[1], app[0] - earth[0])
    a_true = math.atan2(star[1] - earth[1], star[0] - earth[0])
    d.arc(earth[0], earth[1], 120, math.degrees(a_app), math.degrees(a_true), n=8)
    # construction: the star's true direction from the Earth
    d.group('thin')
    d.line(earth, star)
    # labels
    d.group()
    d.text(star[0] + 8, star[1] + 14, 'TRUE', size=7, anchor='start')
    d.text(app[0] + 8, app[1] - 7, 'APPARENT', size=7, anchor='start')
    d.text(earth[0] - 2, earth[1] + 18, 'EARTH', size=7, anchor='end')
    d.text(sx, sy + 3, 'SUN', size=7)
    d.text(200, 292, 'DEFLECTION AT THE LIMB 1.75″ · SHOWN ×100,000', size=7)
    return d


def black_holes():
    """Light rays past a non-rotating black hole, integrated from the Schwarzschild orbit equation.

    Rays come in from the left at impact parameters b (in units of the
    Schwarzschild radius rs). Those with b below 3√3/2 rs, about 2.6 rs, fall
    through the horizon; those just above it wind round the photon sphere at
    1.5 rs before escaping. The captured band is the shadow the Event Horizon
    Telescope imaged."""
    d = D()
    cx, cy, s = 212, 150, 30.0            # plate units per rs
    bc = 1.5 * math.sqrt(3)

    def P(x, y):
        return (cx + s * x, cy - s * y)

    def inside(p):
        return 8 <= p[0] <= 392 and 8 <= p[1] <= 280

    # construction: the axis, the photon sphere, the critical impact parameter and the ISCO
    d.group('thin')
    d.line(P(-6.7, 0), P(6.0, 0))
    d.circle(cx, cy, 1.5 * s)
    d.circle(cx, cy, 3 * s)
    d.lines([[P(-6.7, bc), P(0, bc)], [P(-6.7, -bc), P(0, -bc)]])
    # the rays
    d.group('mid')
    for b in (0.8, 1.7, 2.4, 2.58, 2.64, 3.2, 4.3):
        for sign in (1, -1):
            pts, _ = _ray(b)
            runs, run = [], []
            for x, y in pts:        # split where the ray leaves the plate
                p = P(x, sign * y)
                if inside(p):
                    run.append(p)
                elif run:
                    runs.append(run)
                    run = []
            runs.append(run)
            for q in runs:
                if len(q) > 1:
                    # keep a point once it is 1.5 units from the last kept: the integration's steps are far finer
                    kept = [q[0]]
                    for x, y in q[1:-1]:
                        if math.hypot(x - kept[-1][0], y - kept[-1][1]) >= 1.5:
                            kept.append((x, y))
                    d.line(*kept + [q[-1]])
    # the horizon
    d.group()
    d.circle(cx, cy, s)
    # labels
    d.group()
    d.text(cx, cy + 3, 'rₛ', size=8)
    d.text(cx + 1.06 * s + 4, cy - 1.06 * s - 4, '1.5 rₛ', size=7, anchor='start')
    d.text(cx + 2.2 * s, cy - 2.2 * s - 6, 'ISCO 3 rₛ', size=7, anchor='start')
    d.text(20, cy - bc * s - 4, 'b = 2.6 rₛ', size=7, anchor='start')
    d.text(200, 292, 'SCHWARZSCHILD · LIGHT RAYS · THE SHADOW', size=7)
    return d


def gravitational_waves():
    """A chirp and the detector that heard it.

    Above, the strain of an inspiral in the leading (Newtonian) order: frequency
    rising as (tc − t)^(−3/8) and amplitude as f^(2/3), to the merger, then a
    ringdown. Below, an L-shaped interferometer; a ring of free test masses at
    its corner (the construction circle) is squeezed into an ellipse by a wave
    of plus polarisation passing through the page, one arm lengthening while
    the other shortens. The stretch is exaggerated about 10²⁰ times."""
    d = D()
    # the chirp, along the top
    x0, x1, yb = 30, 370, 64
    tc = 1.0
    pts = []
    phase = 0.0
    n = 900
    t_end = 0.985
    dt = t_end / n
    for i in range(n + 1):
        t = i * dt
        f = 3.2 * (tc - t) ** (-3 / 8)
        amp = 5.5 * (f / 3.2) ** (2 / 3)
        pts.append((x0 + (x1 - x0 - 50) * t / t_end, yb - amp * math.sin(phase)))
        phase += 2 * math.pi * f * dt * 6
    xm = pts[-1][0]
    fr, a0 = 3.2 * (tc - t_end) ** (-3 / 8), 5.5 * (3.2 * (tc - t_end) ** (-3 / 8) / 3.2) ** (2 / 3)
    for i in range(1, 121):
        t = i / 120 * 0.06
        pts.append((xm + t / 0.06 * 50, yb - a0 * math.exp(-t / 0.012) * math.sin(phase)))
        phase += 2 * math.pi * fr * (0.06 / 120) * 6
    # construction: the time axis, the envelope, and the test masses at rest
    d.group('thin')
    d.line((x0, yb), (x1, yb))
    d.line((xm, yb - 40), (xm, yb + 40))
    env = [(x0 + (x1 - x0 - 50) * i / 60, 5.5 * (tc - t_end * i / 60) ** (-1 / 4)) for i in range(61)]
    d.line(*[(x, yb - a) for x, a in env])
    d.line(*[(x, yb + a) for x, a in env])
    cx, cy = 110, 230                   # the corner station
    d.circle(cx, cy, 28)
    # the detector: laser, beam splitter, two arms with their end mirrors
    d.group()
    ex, ny = 360, 112                  # end stations
    d.line((cx, cy), (ex, cy))
    d.line((cx, cy), (cx, ny))
    d.line((cx - 7, cy + 7), (cx + 7, cy - 7))
    d.line((ex, cy - 9), (ex, cy + 9))
    d.line((cx - 9, ny), (cx + 9, ny))
    d.line((cx - 70, cy - 5), (cx - 52, cy - 5), (cx - 52, cy + 5), (cx - 70, cy + 5), closed=True)
    d.line((cx - 52, cy), (cx, cy))
    d.line((cx, cy), (cx, cy + 40))
    d.line((cx - 6, cy + 40), (cx + 6, cy + 40), (cx + 6, cy + 50), (cx - 6, cy + 50), closed=True)
    d.line(*pts)
    # secondary: the ring squeezed, the masses on it, and the arms' stretch
    d.group('mid')
    d.ellipse(cx, cy, 34, 22)
    for k in range(8):
        a = 2 * math.pi * k / 8
        d.circle(cx + 34 * math.cos(a), cy + 22 * math.sin(a), 2.2)
    _arrow(d, ex + 14, cy, 0, 4)
    d.line((ex + 4, cy), (ex + 14, cy))
    _arrow(d, cx, ny + 14, math.pi / 2, 4)
    d.line((cx, ny + 4), (cx, ny + 14))
    # labels
    d.group()
    d.text(x0, yb - 30, 'INSPIRAL', size=7, anchor='start')
    d.text(xm + 4, yb - 30, 'MERGER', size=7, anchor='start')
    d.text(ex, cy + 22, '4 KM', size=7, anchor='end')
    d.text(cx + 14, ny + 4, '4 KM', size=7, anchor='start')
    d.text(cx - 61, cy + 18, 'LASER', size=7, anchor='middle')
    d.text(200, 292, 'ONE ARM STRETCHES AS THE OTHER SQUEEZES · ×10²⁰', size=7)
    return d


PLATES = {
    'general-relativity': general_relativity,
    'black-holes': black_holes,
    'gravitational-waves': gravitational_waves,
}
