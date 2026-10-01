"""Plates for How We Build's Making many segment, part mass2 (sprint 026):
injection moulding, the Lego brick and Unimate."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _dashed_circle(d, cx, cy, r, dashes=16):
    """A hidden outline: a circle drawn as short arcs, for a stud seen through the brick."""
    segs = []
    for k in range(dashes):
        a0 = 360 * k / dashes
        a1 = a0 + 360 / dashes * 0.55
        segs.append([(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / 4)),
                      cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / 4))) for i in range(5)])
    d.lines(segs)


def injection_moulding():
    """A reciprocating-screw injection unit and a two-plate mould in section, and the cavity
    pressure through one cycle plotted beneath."""
    d = D()
    cy = 100                                   # the barrel's axis
    x0, x1 = 24, 222                           # the barrel's back and front
    bore, wall = 15, 8                         # bore radius, barrel wall thickness
    tip = 196                                  # the screw has backed off to here, leaving the shot in front
    pf, pa = 270, 318                          # parting line and the back of the moving plate
    fa = 236                                   # the face of the fixed plate, against the nozzle
    my0, my1 = 34, 166                         # mould plates' top and bottom
    d.group('thin')
    d.line((x0 - 10, cy), (pa + 60, cy))                               # the machine's axis
    d.line((pf, my0 - 14), (pf, my1 + 14))                             # the parting line
    # tie bars of the clamp, above and below the mould
    d.lines([[(fa - 6, my0 - 6), (390, my0 - 6)], [(fa - 6, my1 + 6), (390, my1 + 6)]])
    # the plot's axes: cavity pressure against time
    px0, py0, pw, ph = 40, 278, 330, 62
    d.line((px0, py0 - ph - 6), (px0, py0), (px0 + pw, py0))
    # phase boundaries on the plot
    bounds = [0, 0.16, 0.42, 0.82, 1.0]
    d.lines([[(px0 + pw * b, py0), (px0 + pw * b, py0 - ph)] for b in bounds[1:-1]])
    d.group()
    # the barrel in section: two walls, open at the back under the hopper, closed by the nozzle
    for s in (-1, 1):
        d.line((x0, cy + s * bore), (x1, cy + s * bore))
        d.line((x0, cy + s * (bore + wall)), (x1, cy + s * (bore + wall)))
    d.line((x0, cy - bore - wall), (x0, cy + bore + wall))
    # the nozzle: a cone from the barrel's head to the sprue bush
    d.line((x1, cy - bore - wall), (fa - 2, cy - 5), (fa - 2, cy + 5), (x1, cy + bore + wall))
    # the screw: root growing from the feed zone to the metering zone, a conical tip
    def root(x):
        u = min(max((x - x0) / (tip - 18 - x0), 0), 1)
        return 6 + 6 * min(max((u - 0.35) / 0.35, 0), 1)           # feed, compression, metering
    xs = list(range(x0 + 4, tip - 18 + 1, 2))
    d.line(*[(x, cy - root(x)) for x in xs])
    d.line(*[(x, cy + root(x)) for x in xs])
    d.line((xs[-1], cy - root(xs[-1])), (tip, cy), (xs[-1], cy + root(xs[-1])))
    # the mould: fixed plate, moving plate, the cavity of a lid with drafted walls, the core
    d.line((fa, my0), (pa, my0), (pa, my1), (fa, my1), closed=True)
    depth, half = 30, 46                                       # cavity depth (into the fixed plate) and half-width
    dr = math.tan(math.radians(4))                             # draft, drawn at 4° so that it shows
    t = 5                                                      # the lid's wall
    cav = [(pf, cy - half), (pf - depth, cy - half + depth * dr),
           (pf - depth, cy + half - depth * dr), (pf, cy + half)]
    d.line(*cav)
    core = [(pf, cy - half + t), (pf - depth + t, cy - half + t + (depth - t) * dr),
            (pf - depth + t, cy + half - t - (depth - t) * dr), (pf, cy + half - t)]
    d.line(*core)
    # the sprue: a tapered channel from the nozzle to the cavity's back
    d.lines([[(fa, cy - 3), (pf - depth, cy - 4.5)], [(fa, cy + 3), (pf - depth, cy + 4.5)]])
    d.group('mid')
    # heater bands on the barrel
    d.lines([[(x, cy - bore - wall - 4), (x + 22, cy - bore - wall - 4), (x + 22, cy - bore - wall),
              (x, cy - bore - wall), (x, cy - bore - wall - 4)] for x in (78, 118, 158)]
            + [[(x, cy + bore + wall + 4), (x + 22, cy + bore + wall + 4), (x + 22, cy + bore + wall),
                (x, cy + bore + wall), (x, cy + bore + wall + 4)] for x in (78, 118, 158)])
    # the hopper over the feed throat
    d.line((30, cy - bore - wall - 36), (70, cy - bore - wall - 36), (56, cy - bore - wall), (44, cy - bore - wall))
    # the screw's flights, at the helix angle of a square-pitch screw
    p = 2 * bore                                                # pitch equal to the diameter
    lead = math.degrees(math.atan(p / (math.pi * 2 * bore)))    # about 17.7°
    flights = []
    x = x0 + 10
    while x + p / 2 < tip - 22:
        flights.append([(x, cy - bore + 1), (x + 2 * bore * math.tan(math.radians(lead)), cy + bore - 1)])
        x += p / 2 * 1.0
    d.lines(flights)
    # the clamp's moving platen and ram
    d.line((pa, my0 - 10), (pa + 12, my0 - 10), (pa + 12, my1 + 10), (pa, my1 + 10))
    d.lines([[(pa + 12, cy - 9), (390, cy - 9)], [(pa + 12, cy + 9), (390, cy + 9)]])
    # ejector pins through the moving plate, and cooling channels
    d.lines([[(pf + 1, cy + yy), (pa - 4, cy + yy)] for yy in (-24, 24)])
    for (xx, yy) in ((252, my0 + 14), (252, my1 - 14), (296, my0 + 14), (296, my1 - 14)):
        d.circle(xx, yy, 4)
    # the cavity pressure through a cycle: fill, pack and hold, cool, open
    curve = []
    for i in range(121):
        u = i / 120
        if u < bounds[1]:
            v = 0.15 * u / bounds[1] + 0.85 * (u / bounds[1]) ** 3            # rising as the cavity fills
        elif u < bounds[2]:
            v = 0.72                                                          # held while the part shrinks
        elif u < bounds[2] + 0.06:
            v = 0.72 * (1 - (u - bounds[2]) / 0.06)                           # the gate freezes
        else:
            v = 0
        curve.append((px0 + pw * u, py0 - ph * v))
    d.line(*curve)
    d.group('mid')
    d.text(50, cy - bore - wall - 42, 'HOPPER', size=8)
    d.text(126, cy + bore + wall + 16, 'SCREW', size=8)
    d.text(fa + 40, my0 - 12, 'MOULD', size=8)
    d.text(pf - depth - 4, cy - half - 6, 'DRAFT', size=7, anchor='end')
    for k, name in enumerate(('FILL', 'PACK', 'COOL', 'OPEN')):
        d.text(px0 + pw * (bounds[k] + bounds[k + 1]) / 2, py0 + 12, name, size=7)
    d.text(px0 + 6, py0 - ph - 10, 'CAVITY PRESSURE', size=7, anchor='start')
    return d


def lego_brick():
    """A 2 × 4 brick from below, its tubes touching the studs' projected outlines; one tube and
    its four studs enlarged with the 1961 rule worked; and a section on the diagonal."""
    d = D()
    s = 5.6                                    # px per mm for the plan
    ox, oy = 26, 34                            # the brick's grid origin (the clearance is inside it)
    L, Wd, c, w = 32, 16, 0.1, 1.5             # grid length and width, clearance a side, wall
    studs = [(4 + 8 * i, 4 + 8 * j) for i in range(4) for j in range(2)]
    tubes = [(8 + 8 * i, 8) for i in range(3)]
    rs, rt, ri = 2.4, (8 * math.sqrt(2) - 4.8) / 2, 2.4      # stud radius, tube outer radius, tube bore
    P = lambda x, y: (ox + s * x, oy + s * y)
    d.group('thin')
    # the 8 mm grid, and the diagonals from each tube's centre to its four studs
    d.lines([[P(x, -2), P(x, Wd + 2)] for x in range(0, L + 1, 8)]
            + [[P(-2, y), P(L + 2, y)] for y in range(0, Wd + 1, 8)])
    d.lines([[P(*t), P(t[0] + dx, t[1] + dy)] for t in tubes for dx in (-4, 4) for dy in (-4, 4)])
    d.group()
    # the brick's outer wall, set in by the clearance, and its inner face
    d.line(P(c, c), P(L - c, c), P(L - c, Wd - c), P(c, Wd - c), closed=True)
    d.line(P(c + w, c + w), P(L - c - w, c + w), P(L - c - w, Wd - c - w), P(c + w, Wd - c - w), closed=True)
    for t in tubes:
        d.circle(*P(*t), rt * s)
        d.circle(*P(*t), ri * s)
    d.group('mid')
    # the studs on top, seen through the brick: each tangent to a tube and to the wall
    for st in studs:
        _dashed_circle(d, *P(*st), rs * s)
    # the enlarged detail: one tube, four studs, 12 px per mm
    k = 11
    cx, cy = 306, 92
    Q = lambda x, y: (cx + k * x, cy + k * y)
    d.group('thin')
    d.lines([[Q(-4, -4), Q(4, 4)], [Q(-4, 4), Q(4, -4)], [Q(-4, -6.6), Q(-4, 6.6)], [Q(4, -6.6), Q(4, 6.6)]])
    d.group()
    d.circle(cx, cy, rt * k)
    for dx in (-4, 4):
        for dy in (-4, 4):
            d.circle(*Q(dx, dy), rs * k)
    d.group('mid')
    d.circle(cx, cy, ri * k)
    d.line(Q(-4, 6.6), Q(4, 6.6))
    d.lines([[Q(-4, 6.2), Q(-4, 7.0)], [Q(4, 6.2), Q(4, 7.0)]])
    # the section on the diagonal: two studs of the lower brick, the tube of the upper one between them
    k2 = 9
    sx, base = 112, 262                        # the section's centre line and the lower brick's top face
    S = lambda u, z: (sx + k2 * u, base - k2 * z)
    e = 8 * math.sqrt(2) / 2                   # stud centre from tube centre along the diagonal
    d.group('thin')
    d.line(S(0, -1.6), S(0, 8.2))
    d.lines([[S(-e, -1), S(-e, 3)], [S(e, -1), S(e, 3)]])
    d.group()
    d.line(S(-11, 0), S(11, 0))                                        # the lower brick's top
    d.line(S(-11, -1.2), S(11, -1.2))
    for u0 in (-e, e):
        d.line(S(u0 - rs, 0), S(u0 - rs, 1.7), S(u0 + rs, 1.7), S(u0 + rs, 0))
    for side in (-1, 1):                                               # the tube's wall, cut through
        d.line(S(side * rt, 0.05), S(side * rt, 7))
        d.line(S(side * ri, 0.05), S(side * ri, 7))
        d.line(S(side * ri, 0.05), S(side * rt, 0.05))
    # a break line across the top of the tube
    d.line(S(-rt - 1, 7.2), S(-1, 7.6), S(1, 6.8), S(rt + 1, 7.2))
    d.group('mid')
    d.text(cx, cy - 6.9 * k, '8 × √2 − 4.8 = 6.51', size=8)
    d.text(cx, cy + 7.6 * k, '8', size=8)
    d.text(cx + 4 * k + rs * k + 4, cy + 4 * k + 3, '4.8', size=8, anchor='start')
    d.text(ox + s * 16, oy - 12, 'FROM BELOW', size=8)
    d.text(sx, base + 26, 'ON THE DIAGONAL', size=8)
    d.text(S(e + rs + 1.6, 0.6)[0], S(e + rs + 1.6, 0.6)[1], 'STUD', size=7, anchor='start')
    d.text(S(rt + 0.6, 4.6)[0], S(rt + 0.6, 4.6)[1], 'TUBE', size=7, anchor='start')
    return d


def unimate():
    """A polar arm in elevation, with its swing axis, the arc of its lift and the reach of its
    telescoping boom, the envelope they sweep in section, and the program drum."""
    d = D()
    ax, ay = 112, 128                          # the shoulder pivot
    rmin, rmax = 120, 236                      # the gripper's reach from the pivot, boom in and out
    lo, hi = -20, 22                           # lift limits, degrees above the horizontal
    lift = 8                                   # the boom as drawn
    gy = 280                                   # floor
    d.group('thin')
    d.line((ax, 20), (ax, gy + 8))                                     # swing axis
    d.line((20, gy), (392, gy))
    # the envelope in section: the annular sector the gripper can reach
    d.arc(ax, ay, rmin, -hi, -lo, n=40)
    d.arc(ax, ay, rmax, -hi, -lo, n=60)
    for a in (lo, hi):
        u = _dir(-a)
        d.line((ax + u[0] * rmin, ay + u[1] * rmin), (ax + u[0] * rmax, ay + u[1] * rmax))
        d.line((ax, ay), (ax + u[0] * rmin, ay + u[1] * rmin))
    # the swing, as an ellipse round the axis seen nearly edge on
    d.arc(ax, 50, 46, 200, 340, ry=9, n=30)
    d.group()
    # the base: a box on the floor, the column, and the head that tilts on the pivot
    d.line((44, gy), (44, 206), (180, 206), (180, gy))
    d.line((92, 206), (92, ay + 26), (132, ay + 26), (132, 206))
    u = _dir(-lift)
    n = (-u[1], u[0])
    hl, hb = 64, 26                            # the head's length back and forward of the pivot, half-height
    head = [(ax - u[0] * 40 + n[0] * hb * s1 + u[0] * hl * s0, ay - u[1] * 40 + n[1] * hb * s1 + u[1] * hl * s0)
            for s0, s1 in ((0, -1), (1, -1), (1, 1), (0, 1))]
    d.line(*head, closed=True)
    d.circle(ax, ay, 6)
    # the twin rods of the boom, out from the head's front
    front = 24
    reach = 196
    for off in (-7, 7):
        a0 = (ax + u[0] * front + n[0] * off, ay + u[1] * front + n[1] * off)
        a1 = (ax + u[0] * reach + n[0] * off, ay + u[1] * reach + n[1] * off)
        d.line(a0, a1)
    # the wrist block and a gripper with two jaws
    wx, wy = ax + u[0] * reach, ay + u[1] * reach
    d.line((wx + n[0] * 12, wy + n[1] * 12), (wx + n[0] * 12 + u[0] * 16, wy + n[1] * 12 + u[1] * 16),
           (wx - n[0] * 12 + u[0] * 16, wy - n[1] * 12 + u[1] * 16), (wx - n[0] * 12, wy - n[1] * 12), closed=True)
    g = _dir(-lift + 40)                       # the wrist bent down 40°
    gx, gy2 = wx + u[0] * 16, wy + u[1] * 16
    tipx, tipy = gx + g[0] * 22, gy2 + g[1] * 22
    gn = (-g[1], g[0])
    d.line((gx, gy2), (tipx, tipy))
    jw, jl = 10, 16                            # the jaws' half-spread and length
    d.lines([[(tipx + gn[0] * jw, tipy + gn[1] * jw), (tipx - gn[0] * jw, tipy - gn[1] * jw)],
             [(tipx + gn[0] * jw, tipy + gn[1] * jw), (tipx + gn[0] * jw + g[0] * jl, tipy + gn[1] * jw + g[1] * jl)],
             [(tipx - gn[0] * jw, tipy - gn[1] * jw), (tipx - gn[0] * jw + g[0] * jl, tipy - gn[1] * jw + g[1] * jl)]])
    d.group('mid')
    # the lift arc and the reach, as dimension arrows
    d.arc(ax, ay, 70, -hi, -lo, n=24)
    r0 = (ax + u[0] * (front + 4) + n[0] * 22, ay + u[1] * (front + 4) + n[1] * 22)
    r1 = (ax + u[0] * reach + n[0] * 22, ay + u[1] * reach + n[1] * 22)
    d.line(r0, r1)
    d.lines([[(r1[0] - u[0] * 6 + n[0] * 3, r1[1] - u[1] * 6 + n[1] * 3), r1,
              (r1[0] - u[0] * 6 - n[0] * 3, r1[1] - u[1] * 6 - n[1] * 3)]])
    # the program drum: a cylinder with tracks round it and slots along it
    dx0, dx1, dcy, dr = 250, 350, 242, 16
    d.ellipse(dx0, dcy, 6, dr)
    d.arc(dx1, dcy, 6, -90, 90, ry=dr, n=20)
    d.line((dx0, dcy - dr), (dx1, dcy - dr))
    d.line((dx0, dcy + dr), (dx1, dcy + dr))
    d.lines([[(x, dcy - dr), (x, dcy + dr)] for x in range(dx0 + 12, dx1, 12)])
    d.lines([[(dx0 + 2, dcy + yy), (dx1 + 2, dcy + yy)] for yy in (-9, -3, 3, 9)])
    d.group('mid')
    d.text(ax, 16, 'SWING', size=8)
    d.text(ax + 70 * math.cos(math.radians(hi)) - 4, ay - 70 * math.sin(math.radians(hi)) - 8, 'LIFT', size=8, anchor='start')
    d.text((r0[0] + r1[0]) / 2, (r0[1] + r1[1]) / 2 + 22, 'REACH', size=8)
    d.text((dx0 + dx1) / 2, dcy + dr + 12, 'DRUM: A SLOT A STEP', size=7)
    return d


PLATES = {
    'injection-moulding': injection_moulding,
    'lego-brick': lego_brick,
    'unimate': unimate,
}
