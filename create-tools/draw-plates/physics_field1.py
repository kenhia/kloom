"""physics plates, part "field1": the field and the start of its trail (sprint 021). See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _clip(p, q, box=(12, 26, 388, 274)):
    """Clip the segment p→q to the rectangle `box` (Liang–Barsky); None if it misses."""
    x0, y0, x1, y1 = box
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pk == 0:
            if qk < 0:
                return None
            continue
        r = qk / pk
        if pk < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
    if t0 > t1:
        return None
    return (p[0] + t0 * dx, p[1] + t0 * dy), (p[0] + t1 * dx, p[1] + t1 * dy)


def the_field():
    """The field takes time: a charge that was moving steadily is stopped at S.

    The news of the stop spreads from S at the speed of light, so at a moment
    later the field inside a sphere of radius ct about S points from S, where
    the charge is, and the field outside still points from G, where the charge
    would have been had it kept going. A thin shell joins the two, and the kinks
    in the lines are the pulse of radiation. (Non-relativistic sketch: lines
    spread evenly from both centres.)"""
    d = D()
    S = (150, 158)                 # where the charge stopped
    vt = 64                        # how far it would have gone since
    G = (S[0] + vt, S[1])          # where the old field still says it is
    R1, R2 = 92, 104               # the shell: the news of the stop, c·t and c·(t + Δt)
    n = 12
    angles = [2 * math.pi * (k + 0.5) / n for k in range(n)]
    # construction: the charge's path, the two light-spheres about S, and G's cross
    d.group('thin')
    d.line((24, S[1]), (G[0] + 14, S[1]))
    d.circle(*S, R1)
    d.circle(*S, R2)
    d.lines([[(G[0] - 5, G[1] - 5), (G[0] + 5, G[1] + 5)], [(G[0] - 5, G[1] + 5), (G[0] + 5, G[1] - 5)]])
    # the new field: radial from S, out to the inner sphere
    d.group()
    d.lines([[(S[0] + 7 * math.cos(a), S[1] + 7 * math.sin(a)),
              (S[0] + R1 * math.cos(a), S[1] + R1 * math.sin(a))] for a in angles])
    d.circle(*S, 4)
    # the kinks: across the shell, from the new line's end to the old line's start
    def outer_start(a):
        # the point on the ray from G at angle a that lies on the sphere R2 about S
        ux, uy = math.cos(a), math.sin(a)
        ox, oy = G[0] - S[0], G[1] - S[1]
        b = ox * ux + oy * uy
        c = ox * ox + oy * oy - R2 * R2
        t = -b + math.sqrt(b * b - c)
        return (G[0] + t * ux, G[1] + t * uy)
    kinks = []
    for a in angles:
        kinks.append([(S[0] + R1 * math.cos(a), S[1] + R1 * math.sin(a)), outer_start(a)])
    d.lines(kinks)
    # the old field: radial from G, outside the outer sphere, out to the plate's edge
    segs = []
    for a in angles:
        p = outer_start(a)
        q = (G[0] + 400 * math.cos(a), G[1] + 400 * math.sin(a))
        c = _clip(p, q)
        if c:
            segs.append(list(c))
    d.lines(segs)
    # details: the pulse's direction of travel, and the charge's old motion
    d.group('mid')
    for a in (math.radians(-60), math.radians(60), math.radians(180)):
        r = (R1 + R2) / 2
        x, y = S[0] + r * math.cos(a), S[1] + r * math.sin(a)
        x2, y2 = S[0] + (R2 + 14) * math.cos(a), S[1] + (R2 + 14) * math.sin(a)
        d.line((x, y), (x2, y2))
        _arrow(d, x2, y2, a, 3.5)
    d.line((34, S[1] - 10), (70, S[1] - 10))
    _arrow(d, 70, S[1] - 10, 0, 3.5)
    # labels
    d.group()
    d.text(S[0] - 10, S[1] + 16, 'S', size=8)
    d.text(G[0] + 10, G[1] + 16, 'G', size=8)
    d.text(52, S[1] - 16, 'v', size=8)
    d.text(S[0] - R2 - 4, S[1] + 40, 'r = ct', size=7, anchor='end')
    d.text(200, 18, 'A CHARGE STOPPED AT S · THE NEWS SPREADS AT c', size=7)
    d.text(200, 292, 'INSIDE: THE NEW FIELD · OUTSIDE: THE OLD', size=7)
    return d


def oersted():
    """Ørsted's experiment, in plan and in section.

    Plan: the wire stretched along the magnetic meridian over a compass, and the
    needle turned out of the meridian. Section: the wire end-on, the circles of
    what he called the electric conflict round it, and needles above and below
    it turned opposite ways, which is how he saw that the conflict "performs
    circles"."""
    d = D()
    # plan view, left: the compass at (110, 160)
    cx, cy, r = 108, 162, 62
    dev = math.radians(38)          # an illustrative deflection
    d.group('thin')
    d.line((cx, 40), (cx, 280))                 # the meridian
    d.lines([[(cx + (r - 6) * math.cos(math.radians(a)), cy + (r - 6) * math.sin(math.radians(a))),
              (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))] for a in range(0, 360, 15)])
    d.arc(cx, cy, 44, -90, -90 + math.degrees(dev), n=16)
    # section view, right: the wire end-on at (292, 160), circles about it
    wx, wy = 292, 162
    d.lines([[(wx - 70, wy), (wx + 70, wy)], [(wx, wy - 100), (wx, wy + 100)]])
    # the compass and the needle, plan
    d.group()
    d.circle(cx, cy, r)
    nx, ny = math.sin(dev), -math.cos(dev)      # the needle's north end direction
    L, w = 50, 6
    tip, tail = (cx + L * nx, cy + L * ny), (cx - L * nx, cy - L * ny)
    side = (-ny * w, nx * w)
    d.line(tip, (cx + side[0], cy + side[1]), tail, (cx - side[0], cy - side[1]), closed=True)
    d.circle(cx, cy, 2.5)
    # the wire over it, along the meridian, drawn as a double line
    d.lines([[(cx - 3, 30), (cx - 3, 290)], [(cx + 3, 30), (cx + 3, 290)]])
    # the section: the wire end-on, and the circles
    d.circle(wx, wy, 6)
    d.lines([[(wx - 3, wy - 3), (wx + 3, wy + 3)], [(wx - 3, wy + 3), (wx + 3, wy - 3)]])
    d.group('mid')
    for rr in (26, 46, 70):
        d.circle(wx, wy, rr)
        # an arrow on each circle, clockwise seen with the current going in
        a = math.radians(-30)
        x, y = wx + rr * math.cos(a), wy + rr * math.sin(a)
        _arrow(d, x, y, a + math.pi / 2, 3.5)
    # small needles above and below the wire, pointing along the circles, opposite ways
    for yy, s in ((wy - 88, 1), (wy + 88, -1)):
        d.line((wx - 12 * s, yy), (wx + 12 * s, yy))
        _arrow(d, wx + 12 * s, yy, 0 if s > 0 else math.pi, 4)
    # labels
    d.group()
    d.text(cx, 24, 'N', size=8)
    d.text(cx + L * nx + 8, cy + L * ny - 4, 'N', size=7, anchor='start')
    d.text(cx, 292, 'PLAN · WIRE OVER NEEDLE', size=7)
    d.text(wx, 300 - 8, 'SECTION · CURRENT INTO PAGE', size=7)
    d.text(wx + 16, wy - 92, 'ABOVE', size=7, anchor='start')
    d.text(wx + 16, wy + 84, 'BELOW', size=7, anchor='start')
    return d


def ampere():
    """Two parallel currents, in section, and the electrodynamic molecule.

    Top: two wires one metre apart carrying equal currents the same way, each
    ringed by its own circles, pulled together; the 1948 ampere is the current
    that makes that pull 2 × 10⁻⁷ newton per metre. Bottom: a magnet in
    section as a lattice of molecular currents, all turning the same way, whose
    neighbours cancel inside and add up round the edge."""
    d = D()
    y0 = 92
    ax, bx = 120, 280
    # construction: the line joining the wires, the one-metre dimension
    d.group('thin')
    d.line((ax, y0), (bx, y0))
    d.lines([[(ax, y0 + 50), (ax, y0 + 62)], [(bx, y0 + 50), (bx, y0 + 62)], [(ax, y0 + 56), (bx, y0 + 56)]])
    _arrow(d, ax, y0 + 56, math.pi, 3)
    _arrow(d, bx, y0 + 56, 0, 3)
    # the magnet's outline in section
    mx0, my0, cols, rows, cell = 110, 188, 6, 3, 30
    d.line((mx0 - 8, my0 - 8), (mx0 + cols * cell + 8, my0 - 8),
           (mx0 + cols * cell + 8, my0 + rows * cell + 8), (mx0 - 8, my0 + rows * cell + 8), closed=True)
    # the two wires, end-on, currents out of the page
    d.group()
    for x in (ax, bx):
        d.circle(x, y0, 7)
        d.circle(x, y0, 1.6)
    # each wire's field circles, and the pull between them
    d.group('mid')
    for x in (ax, bx):
        for rr in (20, 36, 54):
            d.circle(x, y0, rr)
    d.line((ax + 10, y0 - 14), (ax + 34, y0 - 14))
    _arrow(d, ax + 34, y0 - 14, 0, 4)
    d.line((bx - 10, y0 - 14), (bx - 34, y0 - 14))
    _arrow(d, bx - 34, y0 - 14, math.pi, 4)
    # the molecular currents: small loops, all turning clockwise on the page, and the surface current round the edge
    d.group()
    for i in range(cols):
        for j in range(rows):
            x, y = mx0 + cell * (i + 0.5), my0 + cell * (j + 0.5)
            d.arc(x, y, 10, 20, 340, n=24)
            a = math.radians(340)
            _arrow(d, x + 10 * math.cos(a), y + 10 * math.sin(a), a + math.pi / 2, 3)
    d.group('mid')
    ex = [(mx0 + cols * cell + 3, my0 + rows * cell + 3), (mx0 - 3, my0 + rows * cell + 3),
          (mx0 - 3, my0 - 3), (mx0 + cols * cell + 3, my0 - 3)]
    d.line(*ex, closed=True)
    for (x1, y1), (x2, y2) in zip(ex, ex[1:] + ex[:1]):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        _arrow(d, mx, my, math.atan2(y2 - y1, x2 - x1), 4)
    # labels
    d.group()
    d.text(200, y0 + 70, '1 m', size=8)
    d.text(200, 20, 'LIKE CURRENTS ATTRACT · 2 × 10⁻⁷ N PER METRE', size=7)
    d.text(200, 296, 'A MAGNET AS MOLECULAR CURRENTS', size=7)
    return d


PLATES = {'the-field': the_field, 'oersted': oersted, 'ampere': ampere}
