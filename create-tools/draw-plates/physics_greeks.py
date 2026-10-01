"""physics plates, segment "The Greeks" (sprint 021). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def aristotle_motion():
    """A sector of Aristotle's cosmos: the shells of earth, water, air and fire about the centre, under the Moon's sphere.

    A stone falls along a radius to the centre, fire rises along another, and
    a thrown stone's path runs out and then drops, with the parabola that
    later physics gives it as a construction line beside it."""
    d = D()
    cx, cy = 200, 400          # the centre of the universe, below the plate
    shells = [(150, 'EARTH'), (185, 'WATER'), (250, 'AIR'), (300, 'FIRE')]
    moon = 345
    a0, a1 = 235, 305           # the sector, in degrees (SVG angles: 270 is straight up)
    # construction: radii to the centre and the sector's edges
    d.group('thin')
    d.lines([[(cx, cy), (cx + (moon + 8) * math.cos(math.radians(a)), cy + (moon + 8) * math.sin(math.radians(a)))]
             for a in (a0, 255, 270, 285, a1)])
    # the shells of the four elements, and the Moon's sphere above them
    d.group()
    for r, _ in shells:
        d.arc(cx, cy, r, a0, a1, n=60)
    d.arc(cx, cy, moon, a0, a1, n=60)
    # natural motions: a stone falls along a radius, a flame rises along another
    d.group('mid')
    ra = math.radians(255)
    p0 = (cx + 238 * math.cos(ra), cy + 238 * math.sin(ra))
    p1 = (cx + 160 * math.cos(ra), cy + 160 * math.sin(ra))
    d.line(p0, p1)
    _arrow(d, *p1, ra + math.pi, 5)
    d.circle(p0[0], p0[1], 3.5)
    rb = math.radians(285)
    q0 = (cx + 196 * math.cos(rb), cy + 196 * math.sin(rb))
    q1 = (cx + 290 * math.cos(rb), cy + 290 * math.sin(rb))
    d.line(q0, q1)
    _arrow(d, *q1, rb, 5)
    fx, fy = q0
    d.line((fx - 4, fy + 2), (fx - 2, fy - 6), (fx, fy - 2), (fx + 2, fy - 8), (fx + 4, fy + 2), closed=True)
    # a thrown stone: forced motion out along a straight line, then natural motion down
    d.group('thin')
    x0, y0, vx, vy, g = 150, 160, 2.2, -1.9, 0.045
    d.line(*[(x0 + vx * t, y0 + vy * t + g * t * t / 2) for t in range(0, 92, 2)])
    d.group()
    k = 22
    corner = (x0 + vx * k, y0 + vy * k)
    d.line((x0, y0), corner)
    d.path(f'M{corner[0]:.1f} {corner[1]:.1f} Q{corner[0] + 16:.1f} {corner[1] - 6:.1f} {corner[0] + 20:.1f} {corner[1] + 14:.1f}')
    drop = (corner[0] + 20, 196)
    d.line((corner[0] + 20, corner[1] + 14), drop)
    _arrow(d, *drop, math.pi / 2, 4)
    d.circle(x0, y0, 2.5)
    # labels
    d.group()
    a = math.radians(a1 - 2)
    for r, name in shells + [(moon, 'MOON')]:
        d.text(cx + (r - 9) * math.cos(a), cy + (r - 9) * math.sin(a) + 3, name, size=7, anchor='end')
    d.text(200, 20, 'THE SUBLUNARY SPHERES · CENTRE BELOW', size=7)
    d.text(corner[0] - 18, corner[1] - 8, 'FORCED', size=7)
    d.text(drop[0] + 6, drop[1] - 18, 'NATURAL', size=7, anchor='start')
    return d


def archimedes():
    """The law of the lever as Archimedes proves it (On the Equilibrium of Planes I.6).

    Weights of 3 and 4 units balance at 4 and 3 units from the fulcrum. Split
    into seven equal weights spaced one unit apart, they are a row whose centre
    of gravity is the fulcrum, which is the whole of the proof."""
    d = D()
    u = 36                          # one unit of length
    fx, by = 200, 150                # the fulcrum under the beam
    xa, xb = fx - 3 * u, fx + 4 * u   # 4 units at 3 to the left, 3 units at 4 to the right
    row = [fx + u * (k - 3) for k in range(7)]
    # construction: the unit ticks along the beam, and verticals dropped from each weight of the row
    d.group('thin')
    d.lines([[(fx + u * k, by - 5), (fx + u * k, by + 5)] for k in range(-4, 5)])
    d.lines([[(x, by + 10), (x, 250)] for x in row])
    d.line((row[0] - 10, 250), (row[-1] + 10, 250))
    d.lines([[(xa, by), (xa, 250)], [(xb, by), (xb, 250)]])
    # the beam, the fulcrum and the two weights
    d.group()
    d.line((fx - 4.5 * u, by - 3), (fx + 4.5 * u, by - 3), (fx + 4.5 * u, by + 3), (fx - 4.5 * u, by + 3), closed=True)
    d.line((fx - 14, by + 28), (fx, by + 3), (fx + 14, by + 28), closed=True)
    def weight(x, n, w=11, h=10):
        top = by + 3
        d.line((x, top), (x, top + 14))
        d.line((x - w, top + 14), (x + w, top + 14), (x + w, top + 14 + n * h), (x - w, top + 14 + n * h), closed=True)
        d.lines([[(x - w, top + 14 + k * h), (x + w, top + 14 + k * h)] for k in range(1, n)])
    weight(xa, 4)
    weight(xb, 3)
    # the proof's row: seven equal weights one unit apart, centred on the fulcrum
    d.group('mid')
    for x in row:
        d.circle(x, 262, 6)
    d.lines([[(row[0], 275), (row[3], 275)], [(row[3], 275), (row[-1], 275)]])
    # labels
    d.group()
    d.text(xa - 18, by + 40, '4', size=10, anchor='end')
    d.text(xb + 18, by + 35, '3', size=10, anchor='start')
    d.text((xa + fx) / 2, by - 12, '3', size=8)
    d.text((xb + fx) / 2, by - 12, '4', size=8)
    d.text(fx, 40, 'WEIGHTS INVERSELY AS THEIR DISTANCES', size=8)
    d.text(fx, 292, 'THE SAME WEIGHT AS SEVEN EQUAL PARTS', size=7)
    return d


def ptolemy():
    """Ptolemy's model of a superior planet, with Mars's parameters from the Almagest (R = 60, e = 6, r = 39.5).

    The epicycle's centre moves round the deferent uniformly as seen from the
    equant; the planet moves round the epicycle; the trace is the planet's path
    as seen from the Earth, with its retrograde loops."""
    d = D()
    s = 1.35                        # plate units per Ptolemaic part
    cx, cy = 200, 152
    R, e, r = 60, 6, 39.5
    earth = (cx, cy + e * s)          # the Earth, the eccentre and the equant on one line
    equant = (cx, cy - e * s)
    ecc = (cx, cy)
    # construction: the line of apsides, the deferent, and one sight line from the equant
    d.group('thin')
    d.line((cx, cy - (R + r) * s - 6), (cx, cy + (R + r) * s + 6))
    d.circle(cx, cy, R * s)
    # the planet's path: the epicycle's centre at uniform angle M about the equant,
    # the planet at the mean-sun direction on its epicycle (superior planet)
    def centre(M):
        # solve for the point C on the deferent seen from the equant at angle M
        ux, uy = math.cos(M), math.sin(M)
        ox, oy = equant[0] - ecc[0], equant[1] - ecc[1]
        b = ox * ux + oy * uy
        c = ox * ox + oy * oy - (R * s) ** 2
        t = -b + math.sqrt(b * b - c)
        return (equant[0] + t * ux, equant[1] + t * uy)
    n_mean = 2 * math.pi / 686.98    # Mars's mean motion about the equant, per day
    n_sun = 2 * math.pi / 365.25
    pts = []
    for day in range(0, 2 * 687 + 1, 3):
        M = -math.pi / 2 + n_mean * day
        C = centre(M)
        A = -math.pi / 2 + n_sun * day + 0.6
        pts.append((C[0] + r * s * math.cos(A), C[1] + r * s * math.sin(A)))
    d.group('mid')
    d.line(*pts)
    # one moment drawn in full: the equant's sight line, the epicycle and the planet on it
    M = -math.pi / 2 + n_mean * 540
    C = centre(M)
    A = -math.pi / 2 + n_sun * 540 + 0.6
    P = (C[0] + r * s * math.cos(A), C[1] + r * s * math.sin(A))
    d.group('thin')
    d.line(equant, C)
    d.line(earth, P)
    d.group()
    d.circle(C[0], C[1], r * s)
    d.line(C, P)
    d.circle(P[0], P[1], 3)
    d.circle(earth[0], earth[1], 4.5)
    d.lines([[(equant[0] - 3, equant[1] - 3), (equant[0] + 3, equant[1] + 3)],
             [(equant[0] - 3, equant[1] + 3), (equant[0] + 3, equant[1] - 3)]])
    d.circle(ecc[0], ecc[1], 1.5)
    # labels
    d.group()
    d.text(earth[0] + 8, earth[1] + 12, 'EARTH', size=7, anchor='start')
    d.text(equant[0] + 7, equant[1] - 5, 'EQUANT', size=7, anchor='start')
    d.text(C[0], C[1] + 3, 'EPICYCLE', size=7)
    d.text(cx + R * s * 0.72 + 6, cy - R * s * 0.72, 'DEFERENT', size=7, anchor='start')
    d.text(200, 292, 'MARS · R 60 · e 6 · r 39;30', size=8)
    return d


PLATES = {'aristotle-motion': aristotle_motion, 'archimedes': archimedes, 'ptolemy': ptolemy}
