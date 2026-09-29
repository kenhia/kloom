"""feynman plates, segment "The wider world" (sprint 014). See feynman.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _vector(d, x0, y0, x1, y1, size=5):
    """A straight arrow from (x0, y0) to (x1, y1)."""
    d.line((x0, y0), (x1, y1))
    _arrow(d, x1, y1, math.atan2(y1 - y0, x1 - x0), size)


def _wavy(d, x0, y0, x1, y1, waves=6, amp=4):
    """A photon line: a sine wave laid along the segment."""
    L = math.dist((x0, y0), (x1, y1))
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    n = waves * 16
    d.line(*[(x0 + ux * L * i / n - uy * amp * math.sin(2 * math.pi * waves * i / n),
              y0 + uy * L * i / n + ux * amp * math.sin(2 * math.pi * waves * i / n)) for i in range(n + 1)])


def partons():
    """An electron strikes one parton of a proton flattened by its speed; beside it, scaling: one curve for every q²."""
    d = D()
    # the proton, seen in a frame where it moves very fast: a disc flattened along its motion
    pcx, pcy, prx, pry = 132, 196, 13, 66
    ps = [(pcx + prx * 0.7 * math.cos(2.4 * k) * ((k % 3) / 3 + 0.2), pcy + pry * 0.85 * (k / 8.5 - 1))
          for k in range(18)]
    struck = ps[5]
    # construction: the proton's axis, its momentum line, the dimension of the fraction x
    d.group('thin')
    d.line((pcx, pcy - pry - 14), (pcx, pcy + pry + 10))
    d.line((40, pcy), (pcx - prx - 6, pcy))
    d.lines([[(300 + 16 * k, 262), (300 + 16 * k, 176)] for k in range(0, 6)])
    d.lines([[(292, 262 - 18 * k), (382, 262 - 18 * k)] for k in range(1, 5)])
    # the electron comes in, gives up a virtual photon, goes out
    d.group()
    vx, vy = 150, 74
    _vector(d, 22, 30, vx - 2, vy - 1)
    d.line((vx, vy), (268, 36))
    _arrow(d, 268, 36, math.atan2(36 - vy, 268 - vx))
    d.ellipse(pcx, pcy, prx, pry)
    _vector(d, 50, pcy + pry + 18, 110, pcy + pry + 18, 5)
    # the photon down to one parton, which is knocked forward
    d.group('mid')
    _wavy(d, vx, vy, struck[0] + 2, struck[1] - 3, waves=5, amp=3.5)
    for x, y in ps:
        d.circle(x, y, 2.2)
    d.circle(struck[0], struck[1], 5.5)
    _vector(d, struck[0] + 6, struck[1] - 2, 232, struck[1] - 36, 5)
    # the scaling plot: F2 against x, points at three momentum transfers on one curve
    d.group()
    ox, oy, w, h = 292, 262, 92, 80
    d.line((ox, oy), (ox + w, oy))
    d.line((ox, oy), (ox, oy - h - 6))
    F = lambda x: 3.2 * x ** 0.7 * (1 - x) ** 2.6
    d.line(*[(ox + w * i / 60, oy - h * F(i / 60)) for i in range(1, 60)])
    d.group('mid')
    for j, q in enumerate((0.07, 0.12, 0.18)):
        for i in range(3):
            x = q + 0.2 * i + 0.05 * j
            px, py = ox + w * x, oy - h * F(x)
            if j == 0:
                d.circle(px, py, 2.4)
            elif j == 1:
                d.line((px - 2.6, py - 2.6), (px + 2.6, py + 2.6))
                d.line((px - 2.6, py + 2.6), (px + 2.6, py - 2.6))
            else:
                d.line((px - 2.8, py + 2.2), (px, py - 2.8), (px + 2.8, py + 2.2), closed=True)
    d.group()
    d.text(36, 24, 'e⁻', size=9, anchor='start')
    d.text(158, 128, 'γ*', size=9, anchor='start')
    d.text(80, pcy + pry + 30, 'P', size=9)
    d.text(238, struck[1] - 40, 'xP', size=9, anchor='start')
    d.text(pcx, 290, 'PROTON · PARTONS', size=7)
    d.text(ox + w / 2, oy + 14, 'x', size=8)
    d.text(ox + 4, oy - h - 12, 'F₂', size=8, anchor='start')
    d.text(ox + w / 2, oy + 28, 'SAME CURVE · ANY q²', size=7)
    return d


def cargo_cult():
    """Millikan's oil drop between the condenser plates, and the plan of Young's rat corridor, laid in sand."""
    d = D()
    # Millikan: two plates, a pinhole, a drop, the forces on it
    cx, top, bot, half = 100, 92, 196, 84
    d.group('thin')
    d.line((cx, 40), (cx, 250))
    d.line((cx - half - 12, (top + bot) / 2), (cx + half + 30, (top + bot) / 2))
    d.lines([[(cx - half + 12 * k, top + 4), (cx - half + 12 * k, bot - 4)] for k in range(1, 14) if k != 7])
    d.group()
    d.line((cx - half, top - 8), (cx - 4, top - 8), (cx - 4, top), (cx - half, top), closed=True)
    d.line((cx + 4, top - 8), (cx + half, top - 8), (cx + half, top), (cx + 4, top), closed=True)
    d.line((cx - half, bot), (cx + half, bot), (cx + half, bot + 8), (cx - half, bot + 8), closed=True)
    d.line((cx - half - 20, top - 4), (cx - half, top - 4))
    d.line((cx - half - 20, bot + 4), (cx - half, bot + 4))
    d.lines([[(cx - half - 26, top - 4), (cx - half - 20, top - 4)], [(cx - half - 23, top - 7), (cx - half - 23, top - 1)]])
    d.line((cx - half - 26, bot + 4), (cx - half - 20, bot + 4))
    # the atomizer's mist above the pinhole, the drop, and its forces
    d.group('mid')
    for k in range(9):
        a = math.radians(200 + 140 * k / 8)
        d.circle(cx + 26 * math.cos(a) * (0.5 + (k % 3) / 4), top - 28 + 10 * math.sin(a), 1.6)
    dy = 140
    d.circle(cx, dy, 4)
    _vector(d, cx, dy - 5, cx, dy - 40)
    _vector(d, cx, dy + 5, cx, dy + 34)
    _vector(d, cx + 7, dy - 3, cx + 26, dy - 22, 4)
    # Young: the corridor in plan, doors in along one side, food doors along the other, in a bed of sand
    gx0, gx1, gy0, gy1 = 236, 384, 110, 170
    d.group('thin')
    d.lines([[(gx0 - 10 + 9 * k, gy1 + 30), (gx0 - 2 + 9 * k, gy0 - 30)] for k in range(0, 19)])
    d.group()
    d.line((gx0, gy0), (gx1, gy0), (gx1, gy1), (gx0, gy1), closed=True)
    n = 6
    door = lambda k: gx0 + 12 + (gx1 - gx0 - 24) * k / (n - 1)
    d.lines([[(door(k) - 7, gy1), (door(k) - 7, gy1 + 12)] for k in range(n)]
            + [[(door(k) + 7, gy1), (door(k) + 7, gy1 + 12)] for k in range(n)])
    d.lines([[(door(k) - 7, gy0), (door(k) - 7, gy0 - 12)] for k in range(n)]
            + [[(door(k) + 7, gy0), (door(k) + 7, gy0 - 12)] for k in range(n)])
    d.group('mid')
    start = 1
    d.line((door(start), gy1 + 8), (door(start), gy1 - 12), (door(start + 3) - 10, gy0 + 14), (door(start + 3), gy0 + 4))
    _arrow(d, door(start + 3), gy0 + 4, math.atan2(-10, 10))
    d.circle(door(start + 3), gy0 - 18, 4)
    d.group()
    d.text(cx, 30, 'MILLIKAN · THE OIL DROP', size=7)
    d.text(cx + 6, dy - 44, 'qE', size=8, anchor='start')
    d.text(cx + 6, dy + 44, 'mg', size=8, anchor='start')
    d.text(cx + 30, dy - 24, 'η', size=9, anchor='start')
    d.text(cx, 232, 'DRAG · η OF AIR TOO LOW', size=7)
    d.text((gx0 + gx1) / 2, 64, 'YOUNG · THE CORRIDOR', size=7)
    d.text(door(start), gy1 + 24, 'IN', size=7)
    d.text(door(start + 3), gy0 - 28, 'FOOD', size=7)
    d.text((gx0 + gx1) / 2, 222, 'LAID ON SAND', size=7)
    return d


def tuva():
    """Throat singing as a filter: the voice's harmonics, and a resonance in the mouth that picks out one of them."""
    d = D()
    ox, oy, w, h = 34, 244, 350, 180
    f0, nh, fmax = 150, 18, 2850
    X = lambda f: ox + w * f / fmax
    src = lambda n: 1 / n ** 0.55                     # the glottal source, falling with harmonic number
    peak = lambda f, fc, bw: 1 / math.sqrt(1 + ((f - fc) / bw) ** 2)
    tract = lambda f, fc: 0.10 + 0.9 * peak(f, fc, 70) + 0.25 * peak(f, 500, 260)
    fc = 8 * f0
    amp = lambda f, fc: src(f / f0) * tract(f, fc)
    top = max(amp(n * f0, fc) for n in range(1, nh + 1))
    Y = lambda a: oy - h * a / top
    # construction: the harmonic grid and the source's slope
    d.group('thin')
    d.lines([[(X(n * f0), oy), (X(n * f0), oy - h - 6)] for n in range(1, nh + 1)])
    d.line(*[(X(f), Y(src(f / f0) * 0.62 * top / src(1))) for f in range(f0, nh * f0 + 1, 25)])
    # the resonance at the eighth harmonic, and where the singer can move it
    d.group('mid')
    d.line(*[(X(f), Y(tract(f, fc) * top * 0.98)) for f in range(40, fmax, 15)])
    d.line(*[(X(f), Y(tract(f, 10 * f0) * top * 0.5)) for f in range(900, fmax, 15)])
    # the spectrum the listener hears: one line per harmonic
    d.group()
    d.line((ox, oy), (ox + w + 6, oy))
    d.line((ox, oy), (ox, oy - h - 12))
    _arrow(d, ox + w + 6, oy, 0)
    for n in range(1, nh + 1):
        d.line((X(n * f0), oy), (X(n * f0), Y(amp(n * f0, fc))))
    d.circle(X(fc), Y(amp(fc, fc)) - 7, 5)
    d.group()
    d.text(X(f0), oy + 14, 'f₀', size=8)
    d.text(X(fc), oy + 14, '8f₀', size=8)
    d.text(X(10 * f0), oy + 14, '10f₀', size=8)
    d.text(X(fc) + 12, Y(amp(fc, fc)) - 2, 'THE WHISTLE', size=7, anchor='start')
    d.text(X(10 * f0) + 10, Y(tract(10 * f0, 10 * f0) * top * 0.5) - 6, 'MOVE THE TONGUE', size=7, anchor='start')
    d.text(ox + w / 2, 282, 'KHÖÖMEI · ONE DRONE, ONE HARMONIC LIFTED', size=8)
    d.text(ox + w, oy + 14, 'Hz', size=7, anchor='end')
    return d


def simulating_physics():
    """Feynman's 1981 argument: six directions, a fixed answer at each, and the agreement at 30° no such scheme can reach."""
    d = D()
    cx, cy, r = 96, 150, 64
    pattern = [1, 1, 0, 1, 0, 0]  # an example: O or E fixed in advance at 0°, 30°, ... 150°
    ends = []
    for k in range(6):
        a = math.radians(-90 + 30 * k)
        ends.append((a, (cx + r * math.cos(a), cy + r * math.sin(a)), (cx - r * math.cos(a), cy - r * math.sin(a))))
    d.group('thin')
    d.circle(cx, cy, r)
    d.circle(cx, cy, r + 14)
    for a, p, q in ends:
        d.line(q, p)
    # the pattern: each direction's answer, O (open) or E (ringed), set before the photon is measured
    d.group()
    for (a, p, q), o in zip(ends, pattern):
        for (x, y) in (p, q):
            d.circle(x, y, 5)
            if not o:
                d.circle(x, y, 2)
    d.group('mid')
    a0, a1 = ends[0][0], ends[1][0]
    d.arc(cx, cy, r + 14, math.degrees(a0), math.degrees(a1), n=12)
    # the graph: probability that two observers agree, against the angle between their calcites
    ox, oy, w, h = 214, 236, 160, 150
    X = lambda deg: ox + w * deg / 90
    Y = lambda p: oy - h * p
    d.group('thin')
    d.lines([[(X(t), oy), (X(t), oy - h - 6)] for t in (30, 60, 90)])
    d.lines([[(ox, Y(p)), (ox + w, Y(p))] for p in (0.25, 0.5, 0.75, 1)])
    d.line((X(30), Y(2 / 3)), (ox - 4, Y(2 / 3)))
    d.group()
    d.line((ox, oy), (ox + w + 8, oy))
    d.line((ox, oy), (ox, oy - h - 10))
    d.line(*[(X(t), Y(math.cos(math.radians(t)) ** 2)) for t in range(0, 91, 2)])
    d.group('mid')
    d.line((X(0), Y(1)), (X(90), Y(0)))
    d.circle(X(30), Y(0.75), 3.5)
    d.circle(X(30), Y(2 / 3), 3.5)
    d.group()
    d.text(cx, 44, 'O OR E, FIXED AT EVERY 30°', size=7)
    d.text(cx + 30, cy - r - 20, '30°', size=8, anchor='start')
    d.text(X(30) + 7, Y(0.75) - 6, 'cos²30° = 3/4', size=8, anchor='start')
    d.text(ox - 8, Y(2 / 3) + 3, '2/3', size=8, anchor='end')
    d.text(ox - 8, Y(1) + 3, '1', size=8, anchor='end')
    d.text(ox + w / 2, oy + 16, 'ANGLE BETWEEN CALCITES', size=7)
    d.text(ox + 6, oy - h - 14, 'P(AGREE)', size=7, anchor='start')
    d.text(200, 286, 'QUANTUM 3/4 · ANY LOCAL CLASSICAL SCHEME ≤ 2/3', size=8)
    return d


def surely_joking():
    """A cassette in plan: two reels, the tape's path past the head, the capstan that sets its speed."""
    d = D()
    x0, y0, x1, y1 = 40, 50, 360, 253  # the shell, 100.4 × 63.8 mm at about 3.2 px per mm
    s = (x1 - x0) / 100.4
    hub = 21.3 * s / 2
    lx, rx, cy = 200 - 21.0 * s, 200 + 21.0 * s, y0 + 29 * s
    rl, rr = 19 * s, 13 * s                            # the tape packs: supply fuller than take-up
    ty = y1 - 16                                       # the tape's run across the opening
    gl, gr = (x0 + 26, ty), (x1 - 26, ty)              # the guide rollers
    cap = (x1 - 78, ty + 7)

    def tangent(c, rad, p, side):
        """The point where a line from p touches the circle (c, rad), on the given side."""
        dx, dy = p[0] - c[0], p[1] - c[1]
        dist = math.hypot(dx, dy)
        a = math.atan2(dy, dx) + side * math.acos(rad / dist)
        return c[0] + rad * math.cos(a), c[1] + rad * math.sin(a)

    d.group('thin')
    d.lines([[(lx, y0 + 6), (lx, y1 - 40)], [(rx, y0 + 6), (rx, y1 - 40)], [(x0 + 8, cy), (x1 - 8, cy)]])
    d.circle(lx, cy, 21 * s)
    d.circle(rx, cy, 21 * s)
    d.group()
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)
    d.line((x0 + 44, y1), (x0 + 60, y1 - 30), (x1 - 60, y1 - 30), (x1 - 44, y1))
    d.line((lx + 24, cy - 20), (rx - 24, cy - 20), (rx - 24, cy + 20), (lx + 24, cy + 20), closed=True)
    d.group('mid')
    for c, rad in ((lx, rl), (rx, rr)):
        d.circle(c, cy, rad)
        d.circle(c, cy, hub)
        d.lines([[(c + hub * math.cos(math.radians(60 * k)), cy + hub * math.sin(math.radians(60 * k))),
                  (c + (hub - 4) * math.cos(math.radians(60 * k)), cy + (hub - 4) * math.sin(math.radians(60 * k)))]
                 for k in range(6)])
    # the tape: off the supply pack, round a roller, across the head and the capstan, round a roller, onto the take-up
    d.group()
    t1 = tangent((lx, cy), rl, (gl[0] - 4, gl[1]), 1)
    t2 = tangent((rx, cy), rr, (gr[0] + 4, gr[1]), -1)
    d.line(t1, (gl[0] - 4, gl[1]), (gr[0] + 4, gr[1]), t2)
    d.circle(gl[0], gl[1] - 4, 4)
    d.circle(gr[0], gr[1] - 4, 4)
    d.circle(*cap, 3.5)
    d.circle(cap[0], cap[1] - 13, 6)
    d.line((200 - 12, ty + 1), (200 + 12, ty + 1), (200 + 9, ty + 16), (200 - 9, ty + 16), closed=True)
    _vector(d, 200 - 60, y1 + 12, 200 + 60, y1 + 12, 4)
    d.group()
    d.text(lx, y0 - 8, 'SUPPLY', size=7)
    d.text(rx, y0 - 8, 'TAKE-UP', size=7)
    d.text(200, y1 + 28, 'HEAD · CAPSTAN · 1⅞ IN/S', size=7)
    d.text(200, 24, 'A VOICE ON TAPE, TOLD AND RETOLD', size=8)
    return d


def qed_book():
    """Partial reflection by a sheet of glass: two surfaces, two little arrows, and the sum that depends on the thickness."""
    d = D()
    gx0, gx1, gt, gb = 30, 196, 170, 214    # the glass in section
    S, A = (70, 40), (150, 40)             # the source and the photomultiplier above it
    mid = (S[0] + A[0]) / 2
    d.group('thin')
    d.line((mid, 30), (mid, 250))
    d.lines([[(gx0, gt + 6 * k), (gx0 + 6 * k + 30, gt)] for k in range(1, 8)])
    d.lines([[(gx0 + 6 * k, gb), (min(gx1, gx0 + 6 * k + 44), gb - 44)] for k in range(1, 22)])
    d.group()
    d.line((gx0, gt), (gx1, gt), (gx1, gb), (gx0, gb), closed=True)
    d.circle(*S, 5)
    d.line((A[0] - 9, A[1] - 7), (A[0] + 9, A[1] - 7), (A[0] + 9, A[1] + 5), (A[0] - 9, A[1] + 5), closed=True)
    d.group('mid')
    d.line(S, (mid - 4, gt), A)
    d.line((S[0] + 3, S[1] + 4), (mid + 4, gb), (A[0] - 3, A[1] + 4))
    # the arrows: front surface (reversed), back surface (turned by the thickness), their sum
    ox, oy, u = 300, 150, 190  # u px per unit amplitude: each arrow is 0.2
    L = 0.2 * u
    theta = math.radians(62)   # how far the back arrow's clock has turned more than the front's
    fx, fy = ox - L, oy        # front arrow, reversed, points left
    bx, by = fx + L * math.cos(math.pi - theta), fy - L * math.sin(math.pi - theta)
    d.group('thin')
    d.circle(fx, fy, L)
    d.line((ox - 2 * L - 8, oy), (ox + 8, oy))
    d.group()
    _vector(d, ox, oy, fx, fy, 6)
    _vector(d, fx, fy, bx, by, 6)
    d.group('mid')
    _vector(d, ox, oy, bx, by, 6)
    d.group()
    d.text(S[0], S[1] - 10, 'S', size=9)
    d.text(A[0], A[1] - 12, 'A', size=9)
    d.text(gx1 - 4, gb + 14, 'GLASS', size=7, anchor='end')
    d.text(ox - L / 2, oy + 14, 'FRONT 0.2', size=7)
    d.text((fx + bx) / 2 - 10, (fy + by) / 2, 'BACK 0.2', size=7, anchor='end')
    d.text(ox - L, oy + L + 20, 'SUM: 0 TO 0.4', size=7)
    d.text(ox - L, oy + L + 32, 'SQUARED: 0 TO 16%', size=7)
    d.text(200, 284, 'PARTIAL REFLECTION · ADD THE ARROWS, THEN SQUARE', size=8)
    return d


PLATES = {
    'partons': partons,
    'cargo-cult': cargo_cult,
    'tuva': tuva,
    'simulating-physics': simulating_physics,
    'surely-joking': surely_joking,
    'qed-book': qed_book,
}
