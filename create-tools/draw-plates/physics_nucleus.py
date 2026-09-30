"""physics plates, segment "The nucleus" (sprint 021). See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _coulomb_path(x0, b, cx, cy, k, xmax=390, ymin=34, ymax=276, dt=0.25, steps=6000):
    """An alpha particle's path past a fixed repulsive point charge at (cx, cy).

    It starts at x0, moving right at unit speed, `b` above or below the
    nucleus (the impact parameter), and is pushed with force k/r² directly
    away from the nucleus: the hyperbola of Rutherford's 1911 paper,
    integrated numerically (velocity Verlet)."""
    x, y, vx, vy = x0, cy + b, 1.0, 0.0
    pts = [(x, y)]

    def acc(x, y):
        dx, dy = x - cx, y - cy
        r = math.hypot(dx, dy)
        return k * dx / r ** 3, k * dy / r ** 3

    ax, ay = acc(x, y)
    for _ in range(steps):
        x += vx * dt + ax * dt * dt / 2
        y += vy * dt + ay * dt * dt / 2
        nax, nay = acc(x, y)
        vx += (ax + nax) * dt / 2
        vy += (ay + nay) * dt / 2
        ax, ay = nax, nay
        pts.append((x, y))
        if x > xmax or x < 8 or y < ymin or y > ymax:
            break
    return pts[::6] + [pts[-1]]


def nucleus():
    """Alpha particles past a gold nucleus, as Rutherford's 1911 paper has them.

    Parallel paths come in from the left at a range of impact parameters; each
    bends on a hyperbola, a little when it passes wide, and one aimed almost
    straight at the nucleus comes back. The circle of closest approach for a
    head-on hit is drawn as construction."""
    d = D()
    cx, cy = 232, 150
    k = 5.0                         # sets the distance of closest approach (2k for unit speed, head on)
    impacts = [-104, -76, -50, -30, -17, -9, -4, 2, 6, 12, 22, 38, 62, 92]
    # construction: the axis through the nucleus, the circle of closest approach, and the impact parameters marked at the left
    d.group('thin')
    d.line((20, cy), (392, cy))
    d.circle(cx, cy, 4 * k)
    d.lines([[(26, cy + b), (40, cy + b)] for b in impacts])
    d.line((30, cy - 106), (30, cy + 94))
    # the paths, the head-on one drawn at full weight
    d.group('mid')
    for b in impacts:
        if b == 2:
            continue
        pts = _coulomb_path(40, b, cx, cy, k)
        d.line(*pts)
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        _arrow(d, x2, y2, math.atan2(y2 - y1, x2 - x1), 3.5)
    d.group()
    pts = _coulomb_path(40, 2, cx, cy, k)
    d.line(*pts)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    _arrow(d, x2, y2, math.atan2(y2 - y1, x2 - x1), 4.5)
    # the nucleus, and the edge of the foil's atom drawn as a faint boundary
    d.circle(cx, cy, 4)
    d.group('thin')
    d.arc(cx, cy, 128, 0, 360, n=120)
    # labels
    d.group()
    d.text(cx + 8, cy + 16, 'NUCLEUS', size=7, anchor='start')
    d.text(30, cy - 112, 'b', size=8)
    d.text(cx + 128 * math.cos(math.radians(-50)) + 4, cy + 128 * math.sin(math.radians(-50)) - 4, 'ATOM', size=7, anchor='start')
    d.text(200, 292, 'ALPHA PARTICLES PAST A GOLD NUCLEUS', size=8)
    return d


def _cassini(cx, cy, a, c, n=240):
    """A Cassini oval: points whose distances from two foci (cx ± a, cy) multiply to c².

    Below c = a it pinches into two drops; at c = a it is a lemniscate; well
    above it is nearly a circle. Returned as one or two closed point lists."""
    loops = []
    if c > a:
        pts = []
        for i in range(n):
            t = 2 * math.pi * i / n
            c2t = math.cos(2 * t)
            r2 = a * a * c2t + math.sqrt(c ** 4 - a ** 4 * math.sin(2 * t) ** 2)
            r = math.sqrt(r2)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        loops.append(pts)
    else:
        tmax = 0.5 * math.asin((c / a) ** 2)
        for side in (1, -1):
            upper, lower = [], []
            for i in range(n // 2 + 1):
                t = -tmax + 2 * tmax * i / (n // 2)
                s = math.sqrt(max(c ** 4 - a ** 4 * math.sin(2 * t) ** 2, 0))
                c2t = a * a * math.cos(2 * t)
                ro = math.sqrt(c2t + s)
                ri = math.sqrt(max(c2t - s, 0))
                upper.append((cx + side * ro * math.cos(t), cy + ro * math.sin(t)))
                lower.append((cx + side * ri * math.cos(t), cy + ri * math.sin(t)))
            loops.append(upper + lower[::-1])
    return loops


def fission():
    """Meitner and Frisch's picture of fission: the uranium nucleus as a charged liquid drop.

    A neutron strikes it; it stretches, necks and splits in two, the halves
    flying apart with two or three new neutrons. The shapes are Cassini ovals
    with the pinch parameter stepped down, on a common axis."""
    d = D()
    cy = 128
    stages = [(62, 0.0, 30), (150, 20, 1.45), (238, 26, 1.06), (326, 30, 0.97)]
    # construction: the common axis, the stage centres, and each drop's foci
    d.group('thin')
    d.line((14, cy), (392, cy))
    d.lines([[(x, cy - 46), (x, cy + 46)] for x, _, _ in stages])
    for x, a, _ in stages[1:]:
        d.lines([[(x - a, cy - 3), (x - a, cy + 3)], [(x + a, cy - 3), (x + a, cy + 3)]])
    # the drop at each stage
    d.group()
    d.circle(stages[0][0], cy, 30)
    for x, a, ratio in stages[1:]:
        for loop in _cassini(x, cy, a, a * ratio):
            d.line(*loop, closed=True)
    # the incoming neutron, and the neutrons and fragments that fly out
    d.group('mid')
    d.circle(14, cy - 44, 3)
    d.line((18, cy - 41), (38, cy - 25))
    _arrow(d, 38, cy - 25, math.atan2(16, 20), 4)
    x4 = stages[3][0]
    for ang in (-80, -100, 90):
        r = math.radians(ang)
        sx, sy = x4 + 14 * math.cos(r), cy + 14 * math.sin(r)
        ex, ey = x4 + 42 * math.cos(r), cy + 42 * math.sin(r)
        d.line((sx, sy), (ex, ey))
        _arrow(d, ex, ey, r, 3.5)
        d.circle(ex + 4 * math.cos(r), ey + 4 * math.sin(r), 2.5)
    d.line((x4 + 58, cy), (x4 + 66, cy))
    _arrow(d, x4 + 66, cy, 0, 4)
    # the energy bookkeeping below: masses before and after, as bars
    d.group('thin')
    d.line((60, 214), (340, 214))
    d.line((60, 258), (340, 258))
    d.group()
    d.line((80, 206), (80, 222), (318, 222), (318, 206), closed=True)
    d.line((80, 250), (80, 266), (314, 266), (314, 250), closed=True)
    d.lines([[(200, 250), (200, 266)]])
    # labels
    d.group()
    d.text(62, cy + 50, 'U-236', size=7)
    d.text(326, cy + 58, 'BA + KR', size=7)
    d.text(14, cy - 52, 'n', size=8)
    d.text(200, 200, 'URANIUM + NEUTRON', size=7)
    d.text(200, 282, 'TWO FRAGMENTS: ABOUT 1/5 OF A PROTON MASS LIGHTER = 200 MEV', size=7)
    d.text(200, 26, 'THE LIQUID DROP DIVIDES', size=8)
    return d


def manhattan_project():
    """The two bomb designs in section, from the Smyth-era public descriptions.

    Left, the gun: a uranium projectile fired down a barrel into a target of
    uranium rings. Right, implosion: a plutonium core inside a tamper, inside
    a shell of 32 explosive lenses (a truncated icosahedron in section shows
    as a ring of alternating lens faces), squeezed inward from every side."""
    d = D()
    # --- the gun, left: axis horizontal
    gy = 118
    # construction: the gun's axis, and the barrel's length ticked
    d.group('thin')
    d.line((14, gy), (196, gy))
    d.lines([[(x, gy - 30), (x, gy + 30)] for x in (30, 150)])
    # --- implosion, right: concentric spheres
    ix, iy = 292, 150
    d.lines([[(ix - 100, iy), (ix + 100, iy)], [(ix, iy - 100), (ix, iy + 100)]])
    for k in range(20):
        a = 2 * math.pi * k / 20
        d.line((ix + 40 * math.cos(a), iy + 40 * math.sin(a)), (ix + 96 * math.cos(a), iy + 96 * math.sin(a)))
    # the objects
    d.group()
    # the gun: breech, barrel, target assembly
    d.line((30, gy - 12), (150, gy - 12))
    d.line((30, gy + 12), (150, gy + 12))
    d.line((20, gy - 18), (30, gy - 18), (30, gy + 18), (20, gy + 18), closed=True)
    d.line((150, gy - 24), (190, gy - 24), (190, gy + 24), (150, gy + 24), closed=True)
    # the implosion sphere: outer case, lens shell, tamper, core
    d.circle(ix, iy, 96)
    d.circle(ix, iy, 66)
    d.circle(ix, iy, 40)
    d.circle(ix, iy, 16)
    # details: the projectile's rings and the charge; the lens faces
    d.group('mid')
    d.lines([[(40 + 6 * k, gy - 9), (40 + 6 * k, gy + 9)] for k in range(7)])
    d.line((38, gy - 9), (80, gy - 9), (80, gy + 9), (38, gy + 9), closed=True)
    d.line((22, gy - 6), (29, gy - 6), (29, gy + 6), (22, gy + 6), closed=True)
    d.line((160, gy - 9), (182, gy - 9), (182, gy + 9), (160, gy + 9), closed=True)
    _arrow(d, 96, gy, 0, 5)
    d.line((84, gy), (96, gy))
    for k in range(20):
        a0 = 2 * math.pi * k / 20
        a1 = 2 * math.pi * (k + 1) / 20
        am = (a0 + a1) / 2
        # a lens: a curved inner face bowing inward, from the outer shell to the tamper
        p0 = (ix + 66 * math.cos(a0), iy + 66 * math.sin(a0))
        p1 = (ix + 66 * math.cos(a1), iy + 66 * math.sin(a1))
        q = (ix + 80 * math.cos(am), iy + 80 * math.sin(am))
        d.path(f'M{p0[0]:.1f} {p0[1]:.1f} Q{q[0]:.1f} {q[1]:.1f} {p1[0]:.1f} {p1[1]:.1f}')
    for k in range(8):
        a = 2 * math.pi * k / 8 + math.pi / 8
        s = (ix + 36 * math.cos(a), iy + 36 * math.sin(a))
        e = (ix + 22 * math.cos(a), iy + 22 * math.sin(a))
        d.line(s, e)
        _arrow(d, *e, a + math.pi, 3.5)
    # labels
    d.group()
    d.text(105, 78, 'GUN · URANIUM-235', size=7)
    d.text(55, gy + 30, 'PROJECTILE', size=7)
    d.text(170, gy + 38, 'TARGET', size=7)
    d.text(292, 38, 'IMPLOSION · PLUTONIUM-239', size=7)
    d.text(292, 154, 'CORE', size=6)
    d.text(ix + 100, iy + 92, 'LENSES', size=7, anchor='end')
    d.text(105, 200, 'LITTLE BOY', size=8)
    d.text(105, 214, 'HIROSHIMA · 6 AUG 1945', size=7)
    d.text(292, 268, 'FAT MAN', size=8)
    d.text(292, 282, 'TRINITY 16 JUL · NAGASAKI 9 AUG', size=7)
    return d


def fusion():
    """A tokamak in cross-section, at ITER's proportions (R 6.2 m, a 2.0 m, elongation 1.85, triangularity 0.49).

    Nested magnetic flux surfaces in the D-shaped plasma, drawn with Miller's
    parametrisation (R = R₀ + r cos(θ + δ sin θ), Z = κ r sin θ); the vacuum
    vessel and a toroidal-field coil outside them; the central solenoid on the
    machine's axis. Only the right half of the machine is drawn."""
    d = D()
    s = 20.0                      # plate units per metre
    ax_x, base = 44, 150            # the machine's vertical axis and midplane
    R0, a, kap, dlt = 6.2, 2.0, 1.85, 0.49

    def surface(r, k=kap, dl=dlt, n=160):
        pts = []
        for i in range(n):
            th = 2 * math.pi * i / n
            R = R0 + r * math.cos(th + dl * (r / a) * math.sin(th))
            Z = k * r * math.sin(th)
            pts.append((ax_x + s * R, base - s * Z))
        return pts
    # construction: the machine axis, the midplane, the plasma's major radius
    d.group('thin')
    d.line((ax_x, 12), (ax_x, 288))
    d.line((ax_x - 20, base), (392, base))
    d.line((ax_x + s * R0, base - s * 4.6), (ax_x + s * R0, base + s * 4.6))
    # the plasma boundary
    d.group()
    d.line(*surface(a), closed=True)
    # nested flux surfaces
    d.group('mid')
    for f in (0.25, 0.5, 0.75):
        d.line(*surface(a * f, k=1 + (kap - 1) * f, dl=dlt * f), closed=True)
    d.circle(ax_x + s * (R0 + 0.12), base, 2)
    # vessel, coil and central solenoid
    d.group()
    d.line(*surface(a + 0.55, k=1.75, dl=0.45), closed=True)
    tf = []
    for i in range(121):
        th = 2 * math.pi * i / 120
        R = R0 + 0.3 + 4.0 * math.cos(th + 0.35 * math.sin(th))
        Z = 1.6 * 3.5 * math.sin(th)
        tf.append((ax_x + s * max(R, 2.3), base - s * Z))
    d.line(*tf, closed=True)
    d.line((ax_x + s * 1.3, base - s * 6.2), (ax_x + s * 2.1, base - s * 6.2),
           (ax_x + s * 2.1, base + s * 6.2), (ax_x + s * 1.3, base + s * 6.2), closed=True)
    d.group('thin')
    d.lines([[(ax_x + s * 1.3, base + s * (-6.2 + 2.067 * k)), (ax_x + s * 2.1, base + s * (-6.2 + 2.067 * k))] for k in range(1, 6)])
    # labels
    d.group()
    d.text(ax_x + s * R0, base - s * 4.6 - 6, 'R 6.2 M', size=7)
    d.text(ax_x + s * 1.7, base + s * 6.2 + 14, 'SOLENOID', size=7)
    d.text(ax_x + s * (R0 + a) + 16, base + 16, 'PLASMA', size=7, anchor='start')
    d.text(ax_x + s * (R0 + 4.3) + 6, base - s * 3.6, 'COIL', size=7, anchor='start')
    d.text(ax_x - 4, 24, 'AXIS', size=7, anchor='end')
    d.text(250, 292, 'A TOKAMAK IN SECTION · ITER PROPORTIONS', size=8)
    return d


PLATES = {'nucleus': nucleus, 'fission': fission, 'manhattan-project': manhattan_project, 'fusion': fusion}
