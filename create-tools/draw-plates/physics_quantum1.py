"""physics plates, part "quantum1" (sprint 021): quantum mechanics and the first
half of the trail "The quantum revolution". See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _wave(d, p0, p1, wavelength, amp, phase=0.0, step=1.5):
    """A sine wave along the straight line p0 -> p1."""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    n = max(2, int(L / step))
    pts = []
    for i in range(n + 1):
        s = L * i / n
        a = amp * math.sin(2 * math.pi * s / wavelength + phase)
        pts.append((x0 + ux * s + nx * a, y0 + uy * s + ny * a))
    d.line(*pts)


def quantum_mechanics():
    """A Mach–Zehnder interferometer, the textbook picture of superposition and the Born rule.

    The first half-silvered mirror splits one photon's amplitude into two
    paths of equal length, each 1/√2; the second recombines them. At one
    detector the two contributions (each 1/2) point the same way and add to
    1; at the other they point opposite ways and cancel. Squared, that is
    probability 1 and 0. The ticks along the paths are wavelengths: the same
    number on each path."""
    d = D()
    src = (34, 232)
    bs1, ma, mb, bs2 = (110, 232), (110, 82), (290, 232), (290, 82)
    d1, d2 = (366, 82), (290, 22)
    # construction: the square of the two paths' centre lines and the diagonal through both splitters
    d.group('thin')
    d.line(bs1, bs2)
    d.lines([[(bs1[0] - 22, bs1[1] + 22), (bs1[0] + 22, bs1[1] - 22)],
             [(bs2[0] - 22, bs2[1] + 22), (bs2[0] + 22, bs2[1] - 22)]])
    # wavelength ticks: equal numbers along the two arms
    ticks = []
    for k in range(1, 12):
        t = k / 12
        y = bs1[1] + (ma[1] - bs1[1]) * t
        ticks.append([(bs1[0] - 4, y), (bs1[0] + 4, y)])
        x = bs1[0] + (mb[0] - bs1[0]) * t
        ticks.append([(x, bs1[1] - 4), (x, bs1[1] + 4)])
        x = ma[0] + (bs2[0] - ma[0]) * t
        ticks.append([(x, ma[1] - 4), (x, ma[1] + 4)])
        y = mb[1] + (bs2[1] - mb[1]) * t
        ticks.append([(mb[0] - 4, y), (mb[0] + 4, y)])
    d.lines(ticks)
    # the beams: in, the two arms, and the two ways out
    d.group('mid')
    d.line(src, bs1)
    d.line(bs1, ma, bs2)
    d.line(bs1, mb, bs2)
    d.line(bs2, (d1[0] - 12, d1[1]))
    d.line(bs2, (d2[0], d2[1] + 12))
    _arrow(d, 70, 232, 0, 4)
    _arrow(d, 110, 150, -math.pi / 2, 4)
    _arrow(d, 200, 232, 0, 4)
    _arrow(d, 200, 82, 0, 4)
    _arrow(d, 290, 150, -math.pi / 2, 4)
    _arrow(d, 330, 82, 0, 4)
    # the instruments: source, two half-silvered mirrors, two mirrors, two detectors
    d.group()
    d.line((src[0] - 18, src[1] - 9), (src[0], src[1] - 9), (src[0], src[1] + 9), (src[0] - 18, src[1] + 9), closed=True)
    for (x, y), silvered in ((bs1, True), (bs2, True), (ma, False), (mb, False)):
        d.line((x - 13, y + 13), (x + 13, y - 13))
        if silvered:
            d.line((x - 13 + 2.5, y + 13 + 2.5), (x + 13 + 2.5, y - 13 + 2.5))
        else:
            d.lines([[(x - 13 + 4.5 * i, y + 13 - 4.5 * i), (x - 13 + 4.5 * i + 4, y + 13 - 4.5 * i + 4)]
                     for i in range(6)])
    d.arc(d1[0], d1[1], 12, 90, 270)
    d.line((d1[0], d1[1] - 12), (d1[0] + 12, d1[1] - 12), (d1[0] + 12, d1[1] + 12), (d1[0], d1[1] + 12))
    d.arc(d2[0], d2[1] + 2, 12, 0, 180)
    d.line((d2[0] - 12, d2[1] + 2), (d2[0] - 12, d2[1] - 10), (d2[0] + 12, d2[1] - 10), (d2[0] + 12, d2[1] + 2))
    # the arithmetic inside the square: two halves that add, two that cancel
    d.group('mid')
    ox, oy, u = 182, 192, 20
    d.line((ox, oy), (ox + u, oy))
    _arrow(d, ox + u, oy, 0, 3.5)
    d.line((ox + u, oy), (ox + 2 * u, oy))
    _arrow(d, ox + 2 * u, oy, 0, 3.5)
    ox2, oy2 = 182, 214
    d.line((ox2, oy2), (ox2 + u, oy2))
    _arrow(d, ox2 + u, oy2, 0, 3.5)
    d.line((ox2 + u, oy2 + 5), (ox2, oy2 + 5))
    _arrow(d, ox2, oy2 + 5, math.pi, 3.5)
    # labels
    d.group()
    d.text(ox - 6, oy + 3, 'D1', size=7, anchor='end')
    d.text(ox + 2 * u + 8, oy + 3, '½ + ½ = 1', size=7, anchor='start')
    d.text(ox2 - 6, oy2 + 5, 'D2', size=7, anchor='end')
    d.text(ox2 + u + 8, oy2 + 6, '½ − ½ = 0', size=7, anchor='start')
    d.text(96, 160, '1/√2', size=7, anchor='end')
    d.text(200, 250, '1/√2', size=7)
    d.text(d1[0], d1[1] + 26, 'D1', size=7)
    d.text(d2[0] + 20, d2[1] + 2, 'D2', size=7, anchor='start')
    d.text(src[0] - 9, src[1] + 22, 'ONE PHOTON', size=7, anchor='start')
    d.text(200, 292, 'PROBABILITY = |AMPLITUDE|²', size=8)
    return d


def photon():
    """Compton scattering drawn to scale for a photon of 511 keV (λ = h/mc) scattered through 90°.

    The scattered wave is twice as long, as λ' − λ = (h/mc)(1 − cos θ)
    gives; the momentum triangle beside it (incoming = outgoing + recoil)
    fixes the recoiling electron's direction, 26.6° below the beam."""
    d = D()
    e = (200, 150)                     # the electron
    lam = 22                           # the incoming wavelength, in plate units
    th = math.radians(90)
    lam2 = lam * (1 + (1 - math.cos(th)))
    # momenta in units of the incoming photon's; SVG y runs downward
    p_in = (1.0, 0.0)
    p_out = (math.cos(-th) * lam / lam2, math.sin(-th) * lam / lam2)
    p_e = (p_in[0] - p_out[0], p_in[1] - p_out[1])
    phi = math.atan2(p_e[1], p_e[0])
    # construction: the beam's axis, the scattering angle, and the momentum triangle to scale
    d.group('thin')
    d.line((24, e[1]), (380, e[1]))
    d.arc(e[0], e[1], 30, -90, 0, n=24)
    d.arc(e[0], e[1], 44, 0, math.degrees(phi), n=12)
    s = 90                              # plate units per unit momentum
    t0 = (270, 250)
    t1 = (t0[0] + s * p_in[0], t0[1] + s * p_in[1])
    t2 = (t0[0] + s * p_out[0], t0[1] + s * p_out[1])
    d.line(t0, t1)
    d.line(t0, t2)
    d.line(t2, t1)
    # the waves: in from the left, out upward at twice the wavelength
    d.group('mid')
    _wave(d, (30, e[1]), (e[0] - 10, e[1]), lam, 7, phase=math.pi / 2)
    _wave(d, (e[0], e[1] - 10), (e[0], 24), lam2, 7)
    _arrow(d, e[0] - 10, e[1], 0, 5)
    _arrow(d, e[0], 24, -math.pi / 2, 5)
    # the electron and its recoil
    d.group()
    d.circle(e[0], e[1], 4.5)
    r0, r1 = 12, 150
    d.line((e[0] + r0 * math.cos(phi), e[1] + r0 * math.sin(phi)), (e[0] + r1 * math.cos(phi), e[1] + r1 * math.sin(phi)))
    _arrow(d, e[0] + r1 * math.cos(phi), e[1] + r1 * math.sin(phi), phi, 5)
    _arrow(d, *t1, 0, 4)
    _arrow(d, *t2, -math.pi / 2, 4)
    _arrow(d, *t1, math.atan2(t1[1] - t2[1], t1[0] - t2[0]), 4)
    # labels
    d.group()
    d.text(60, e[1] - 14, 'λ', size=8)
    d.text(e[0] + 14, 60, "λ' = 2λ", size=8, anchor='start')
    d.text(e[0] + 22, e[1] - 22, 'θ', size=8, anchor='start')
    d.text(e[0] + 50, e[1] + 14, 'φ', size=8, anchor='start')
    d.text(e[0] - 10, e[1] + 18, 'e⁻', size=8, anchor='end')
    d.text(t0[0] - 6, t0[1] + 4, 'p', size=7, anchor='end')
    d.text(t0[0] + 2, t2[1] + 2, "p'", size=7, anchor='start')
    d.text(40, 290, "λ' − λ = (h/mc)(1 − cos θ)", size=8, anchor='start')
    return d


def bohr_atom():
    """Bohr's hydrogen atom: the energy levels, −13.6 eV/n², with the Balmer jumps to n = 2, and the orbits, radius ∝ n².

    The ladder is to scale in energy; the orbits to scale in radius for
    n = 1 to 3, with the jump from 3 to 2 that gives the red line."""
    d = D()
    x0, x1 = 46, 176                   # the ladder's width
    top, bot = 36, 262                 # energy 0 at the top, −13.6 eV at the bottom
    def y(n):
        return top + (bot - top) * (1 / n ** 2)
    # construction: the ionisation limit, the energy axis, and the orbits' centre lines
    d.group('thin')
    d.line((x0 - 8, top), (x1 + 8, top))
    d.line((x0 - 8, top - 6), (x0 - 8, bot + 6))
    cx, cy, a = 290, 170, 11           # the orbits: radius a·n²
    d.lines([[(cx - 9 * a - 10, cy), (cx + 9 * a + 10, cy)], [(cx, cy - 9 * a - 10), (cx, cy + 9 * a + 10)]])
    # the levels
    d.group()
    d.lines([[(x0, y(n)), (x1, y(n))] for n in range(1, 7)])
    # the jumps: Lyman-α down to 1, Balmer down to 2
    d.group('mid')
    xs = {3: 84, 4: 106, 5: 128, 6: 150}
    for n, x in xs.items():
        d.line((x, y(n)), (x, y(2)))
        _arrow(d, x, y(2), math.pi / 2, 3.5)
    d.line((62, y(2)), (62, y(1)))
    _arrow(d, 62, y(1), math.pi / 2, 3.5)
    # the atom: nucleus, orbits n = 1, 2, 3, the electron jumping from 3 to 2 and the light it gives off
    d.group()
    d.circle(cx, cy, 2.5)
    for n in (1, 2, 3):
        d.circle(cx, cy, a * n * n)
    ang = math.radians(-50)
    p3 = (cx + 9 * a * math.cos(ang), cy + 9 * a * math.sin(ang))
    p2 = (cx + 4 * a * math.cos(ang), cy + 4 * a * math.sin(ang))
    d.circle(*p3, 3)
    d.group('mid')
    d.line(p3, (p2[0] + 4 * math.cos(ang), p2[1] + 4 * math.sin(ang)))
    _arrow(d, p2[0] + 4 * math.cos(ang), p2[1] + 4 * math.sin(ang), ang + math.pi, 4)
    _wave(d, (p2[0] - 6, p2[1] - 16), (p2[0] - 58, p2[1] - 70), 9, 3.5)
    _arrow(d, p2[0] - 58, p2[1] - 70, math.atan2(-54, -52), 4)
    # labels
    d.group()
    for n in range(1, 7):
        if n <= 4:
            d.text(x1 + 12, y(n) + 3, f'n = {n}', size=7, anchor='start')
    d.text(x1 + 12, top + 3, '∞', size=7, anchor='start')
    d.text(x0 - 12, top + 3, '0', size=7, anchor='end')
    d.text(x0 - 12, bot + 3, '−13.6', size=7, anchor='end')
    d.text(111, bot + 22, 'eV = −13.6/n²', size=7)
    d.text(xs[3] + 1, (y(3) + y(2)) / 2 + 3, ' Hα', size=6, anchor='start')
    d.text(p2[0] - 64, p2[1] - 70, '656 nm', size=7, anchor='end')
    d.text(cx, cy + 9 * a + 22, 'r ∝ n²', size=7)
    return d


def de_broglie():
    """De Broglie's condition for Bohr's orbits, and electrons diffracted by a crystal.

    Left: an electron wave closing on itself round an orbit, four wavelengths
    in the circumference (n = 4), so 2πr = nλ. Right: a row of atoms in a
    nickel surface (spacing 2.15 Å) and the Davisson–Germer peak at 50°,
    where the path difference d sin θ is one wavelength, 1.65 Å."""
    d = D()
    cx, cy, R = 110, 150, 72
    n = 4
    # construction: the orbit's circle and the radii at each node
    d.group('thin')
    d.circle(cx, cy, R)
    d.lines([[(cx, cy), (cx + (R + 14) * math.cos(k * math.pi / n), cy + (R + 14) * math.sin(k * math.pi / n))]
             for k in range(2 * n)])
    # the standing wave: r = R + A sin(nθ)
    d.group()
    pts = [(cx + (R + 11 * math.sin(n * t)) * math.cos(t), cy + (R + 11 * math.sin(n * t)) * math.sin(t))
           for t in [2 * math.pi * i / 240 for i in range(241)]]
    d.line(*pts)
    d.circle(cx, cy, 3)
    # the crystal: a row of atoms, the beam straight down, the diffracted beam at 50°
    ax0, ay, sp = 232, 232, 36
    atoms = [ax0 + sp * i for i in range(5)]
    th = math.radians(50)
    d.group('thin')
    d.line((atoms[0] - 16, ay), (atoms[-1] + 16, ay))
    # parallel rays from two neighbouring atoms, and the foot of the path difference
    A, B = atoms[1], atoms[2]
    Ln = 110
    ux, uy = -math.sin(th), -math.cos(th)
    d.lines([[(A, ay), (A + Ln * ux, ay + Ln * uy)], [(B, ay), (B + Ln * ux, ay + Ln * uy)]])
    # the foot of the perpendicular from A to B's outgoing ray: the path difference d sin θ
    proj = (A - B) * ux
    fx, fy = B + proj * ux, ay + proj * uy
    d.line((A, ay), (fx, fy))
    d.line((B, ay), (B, ay - 120))
    d.group('mid')
    for x in atoms:
        d.circle(x, ay, 5)
    d.group()
    d.line((B, 40), (B, ay - 8))
    _arrow(d, B, ay - 8, math.pi / 2, 4)
    d.line((B + 10 * ux, ay + 10 * uy), (B + 130 * ux, ay + 130 * uy))
    _arrow(d, B + 130 * ux, ay + 130 * uy, math.atan2(uy, ux), 4)
    d.arc(B, ay, 40, -90, -90 - 50, n=16)
    # labels
    d.group()
    d.text(cx, cy + R + 34, '2πr = 4λ', size=8)
    d.text(cx, 32, 'λ = h/p', size=9)
    d.text(B - 22, ay - 44, '50°', size=7, anchor='end')
    d.text((A + B) / 2, ay + 18, 'd', size=7)
    d.text(B + 8, 50, '54 eV', size=7, anchor='start')
    d.text(300, 280, 'NICKEL · d 2.15 Å', size=7)
    d.text(300, 292, 'd sin θ = λ = 1.65 Å', size=7)
    return d


PLATES = {
    'quantum-mechanics': quantum_mechanics,
    'photon': photon,
    'bohr-atom': bohr_atom,
    'de-broglie': de_broglie,
}
