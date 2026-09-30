"""Plates for the chemistry subject's Industry segment, part two (sprint 025):
chemical-warfare, polymers and leaded-petrol."""
import math, random
from plates import D, rot


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def chemical_warfare():
    """A beam balance weighing a litre of chlorine against a litre of air, and a
    section through the ground where the heavier gas pours into a trench."""
    d = D()
    # ---- the balance: densities at 0 °C, 3.21 g/L for Cl2 and 1.29 g/L for air
    px, py, arm = 200, 44, 88
    tilt = math.degrees(math.atan((3.21 - 1.29) / (3.21 + 1.29) * 0.5))   # a gentle tilt, drawn to the ratio
    lx, ly = px - arm * math.cos(math.radians(tilt)), py + arm * math.sin(math.radians(tilt))
    rx, ry = px + arm * math.cos(math.radians(tilt)), py - arm * math.sin(math.radians(tilt))
    gy = 214                                       # ground line of the section
    d.group('thin')
    d.line((px, py - 8), (px, 128))
    d.line((px - arm - 20, py), (px + arm + 20, py))
    d.line((12, gy), (388, gy))
    # the wind's direction, and the layering of the cloud: lines of equal concentration
    for k, h in enumerate((10, 20, 30)):
        pts = []
        for i in range(61):
            x = 40 + i * 5.6
            base = gy - h * (1 - 0.35 * i / 60)
            # the cloud slumps into the trench, centred at x = 262
            dip = (h + 38 - 12 * k) * math.exp(-((x - 262) / 20) ** 4)
            pts.append((x, base + dip))
        d.line(*pts)
    d.group()
    # the balance: pillar, beam, two pans on their hangers
    d.line((px - 16, 128), (px + 16, 128))
    d.line((px, 128), (px, py))
    d.line((lx, ly), (rx, ry))
    for (x, y) in ((lx, ly), (rx, ry)):
        d.line((x, y), (x - 16, y + 30))
        d.line((x, y), (x + 16, y + 30))
        d.arc(x, y + 30, 20, 0, 180, n=24, ry=6)
        d.line((x - 20, y + 30), (x + 20, y + 30))
    # the ground in section, and the trench cut into it
    tx, tw, td = 262, 26, 44
    d.line((12, gy), (tx - tw, gy), (tx - tw + 4, gy + td), (tx + tw - 4, gy + td), (tx + tw, gy), (388, gy))
    # the gas cylinder, dug in at the left with its siphon pipe
    cx0, cw, ch = 34, 16, 40
    d.line((cx0, gy + 4), (cx0, gy + 4 + ch), (cx0 + cw, gy + 4 + ch), (cx0 + cw, gy + 4))
    d.arc(cx0 + cw / 2, gy + 4, cw / 2, 180, 360, n=16)
    d.line((cx0 + cw / 2, gy - 4), (cx0 + cw / 2, gy - 12), (cx0 + cw / 2 + 22, gy - 12))
    d.group('mid')
    # the two litres on the pans: a flask on each, drawn the same size
    for (x, y) in ((lx, ly), (rx, ry)):
        d.circle(x, y + 20, 9)
    # sandbags on the trench's lip
    for x in (tx - tw - 18, tx - tw - 6, tx + tw + 6, tx + tw + 18):
        d.ellipse(x, gy - 4, 6, 4)
    # the wind
    d.lines([[(66, gy - 58), (106, gy - 58)], [(98, gy - 63), (106, gy - 58), (98, gy - 53)]])
    d.group('mid')
    d.text(lx, ly + 52, 'Cl₂ · 70.9', size=8)
    d.text(rx, ry + 52, 'AIR · ≈ 29', size=8)
    d.text(px, 146, '1 LITRE EACH · 3.2 g AGAINST 1.3 g', size=7)
    d.text(60, gy - 55.5, 'WIND', size=7, anchor='end')
    d.text(tx, gy + td + 16, 'TRENCH', size=7)
    d.text(cx0 + cw / 2, gy + ch + 20, 'CYLINDER', size=7)
    d.text(200, 290, 'Cl₂ + H₂O ⇌ HCl + HOCl', size=9)
    return d


def polymers():
    """A polyethylene chain: a stretch of its zigzag drawn to its bond angle,
    and the whole chain as a random coil."""
    d = D()
    # ---- the zigzag: C–C bonds of 1.54 Å at 112°, drawn at 22 px per ångström
    s, ang = 1.54 * 16, 112
    half = math.radians(ang / 2)
    dx, dy = s * math.sin(half), s * math.cos(half)
    x0, y0 = 60, 70
    n = 12
    pts = [(x0 + i * dx, y0 + (dy if i % 2 else 0)) for i in range(n + 1)]
    d.group('thin')
    d.line((x0 - 10, y0), (x0 + n * dx + 10, y0))
    d.line((x0 - 10, y0 + dy), (x0 + n * dx + 10, y0 + dy))
    # the repeat unit, -CH2-CH2-, boxed by its two cuts
    ux0, ux1 = x0 + 4 * dx - dx / 2, x0 + 6 * dx - dx / 2
    for x in (ux0, ux1):
        d.line((x, y0 - 30), (x, y0 + dy + 30))
    d.group()
    d.line(*pts)
    d.group('mid')
    # the hydrogens: two on each carbon, splayed away from the chain
    hs = []
    for i, (x, y) in enumerate(pts):
        up = -1 if i % 2 == 0 else 1
        for side in (-1, 1):
            hs.append([(x, y), (x + side * 7, y + up * 12)])
    d.lines(hs)
    # square brackets round the repeat unit
    for x, sgn in ((ux0, 1), (ux1, -1)):
        d.line((x + sgn * 5, y0 - 24), (x, y0 - 24), (x, y0 + dy + 24), (x + sgn * 5, y0 + dy + 24))
    # ---- the coil: a freely rotating chain, each step turned 68° from the last, seeded
    rnd = random.Random(25)
    cx, cy = 200, 196
    L = 5.2
    heading = 0.0
    x, y = 0.0, 0.0
    coil = [(x, y)]
    for i in range(420):
        heading += math.radians(68) * rnd.choice((-1, 1)) * (0.6 + 0.4 * rnd.random())
        x += L * math.cos(heading)
        y += L * math.sin(heading)
        coil.append((x, y))
    mx = sum(p[0] for p in coil) / len(coil)
    my = sum(p[1] for p in coil) / len(coil)
    span = max(max(abs(p[0] - mx) for p in coil) / 150, max(abs(p[1] - my) for p in coil) / 62)
    coil = [(cx + (p[0] - mx) / span, cy + (p[1] - my) / span) for p in coil]
    rg = math.sqrt(sum((p[0] - cx) ** 2 + (p[1] - cy) ** 2 for p in coil) / len(coil))
    d.group('thin')
    d.circle(cx, cy, rg)
    d.line((cx, cy), (cx + rg, cy))
    d.group()
    d.line(*coil)
    d.group('mid')
    d.circle(*coil[0], 2.5)
    d.circle(*coil[-1], 2.5)
    d.text((ux0 + ux1) / 2, y0 - 34, 'C₂H₄ · 28', size=8)
    d.text(ux1 + 14, y0 + dy + 30, 'n', size=10)
    d.text(x0 + n * dx + 6, y0 + dy / 2 + 3, '112°', size=7, anchor='start')
    d.text(cx + rg / 2, cy - 4, 'Rg', size=7)
    d.text(200, 290, 'n ≈ 3,565 FOR 100,000 g/mol', size=8)
    return d


def leaded_petrol():
    """Tetraethyllead, Pb(C2H5)4, drawn from tetrahedral directions; an engine
    cylinder in section with the spark's flame front and the end gas that knocks;
    and the cylinder's pressure against crank angle, smooth and knocking."""
    d = D()
    # ---- the molecule: lead at the centre, four ethyls along the tetrahedron's axes
    c, rpb = (104, 128), 11
    tet = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    ax, ay = math.radians(18), math.radians(28)
    s1, s2 = 34, 26
    arms = []
    for v in tet:
        n = math.sqrt(3)
        u = rot((v[0] / n, v[1] / n, v[2] / n), ax, ay)
        c1 = (c[0] + s1 * u[0] * 1.6, c[1] - s1 * u[1] * 1.6)
        # the second carbon bends off the axis at the tetrahedral angle, in the drawing's plane
        a = math.atan2(c1[1] - c[1], c1[0] - c[0]) + math.radians(180 - 109.5) * (1 if u[2] > 0 else -1)
        c2 = (c1[0] + s2 * math.cos(a), c1[1] + s2 * math.sin(a))
        arms.append((u, c1, c2))
    d.group('thin')
    d.circle(*c, 62)
    for u, c1, c2 in arms:
        d.line(c, (c[0] + (c1[0] - c[0]) * 1.8, c[1] + (c1[1] - c[1]) * 1.8))
    d.group()
    for u, c1, c2 in sorted(arms, key=lambda t: t[0][2]):
        a = math.atan2(c1[1] - c[1], c1[0] - c[0])
        d.line((c[0] + rpb * math.cos(a), c[1] + rpb * math.sin(a)), c1, c2)
    d.circle(*c, rpb)
    d.group('mid')
    for u, c1, c2 in arms:
        d.circle(*c1, 3)
        d.circle(*c2, 3)
    # ---- the cylinder: bore, head, piston near the top of its stroke, spark plug off-centre
    bx, bw, top, bot = 262, 104, 50, 200
    py = 128
    sp = (bx + 26, top + 10)
    d.group('thin')
    d.line((bx + bw / 2, top - 16), (bx + bw / 2, bot + 6))
    for r in (22, 44, 66):                          # flame fronts, circles about the spark
        pts = []
        for i in range(81):
            a = math.radians(i * 180 / 80)
            q = (sp[0] + r * math.cos(a), sp[1] + r * math.sin(a))
            if bx <= q[0] <= bx + bw and top <= q[1] <= py:
                pts.append(q)
        if len(pts) > 1:
            d.line(*pts)
    d.group()
    d.line((bx, top), (bx, bot))
    d.line((bx + bw, top), (bx + bw, bot))
    d.line((bx - 10, top), (bx + bw + 10, top))
    d.line((bx + 4, py), (bx + 4, py + 34), (bx + bw - 4, py + 34), (bx + bw - 4, py), closed=True)
    d.line((bx + bw / 2, py + 17), (bx + bw / 2 + 12, bot - 2))
    d.circle(bx + bw / 2, py + 17, 4)
    d.group('mid')
    d.line((sp[0], top - 16), (sp[0], top + 6))
    d.line((sp[0] - 6, top - 16), (sp[0] + 6, top - 16))
    d.lines([[(sp[0] - 4, top + 8), (sp[0], top + 4), (sp[0] + 4, top + 8)]])
    ex, ey = bx + bw - 18, py - 18                  # the end gas, self-igniting before the flame arrives
    rays = []
    for k in range(8):
        a = math.radians(k * 45)
        rays.append([(ex + 4 * math.cos(a), ey + 4 * math.sin(a)), (ex + 9 * math.cos(a), ey + 9 * math.sin(a))])
    d.lines(rays)
    # ---- pressure against crank angle: a smooth burn, and a knocking one that rings
    gx0, gx1, gy0, gh = 226, 386, 284, 46
    d.group('thin')
    d.line((gx0, gy0 - gh - 6), (gx0, gy0), (gx1, gy0))
    d.group('mid')
    smooth, knock = [], []
    for i in range(121):
        t = i / 120
        base = math.exp(-((t - 0.42) / 0.16) ** 2)
        ring = 0.0 if t < 0.44 else 0.35 * math.exp(-(t - 0.44) / 0.1) * math.sin((t - 0.44) * 2 * math.pi * 16)
        x = gx0 + t * (gx1 - gx0)
        smooth.append((x, gy0 - gh * 0.8 * base))
        knock.append((x, gy0 - gh * (0.8 * base + ring)))
    d.line(*smooth)
    d.group()
    d.line(*knock)
    d.group('mid')
    d.text(c[0], c[1] + 3, 'Pb', size=8)
    d.text(c[0], 208, 'Pb(C₂H₅)₄', size=9)
    d.text(c[0], 224, '64% LEAD BY WEIGHT', size=7)
    d.text(sp[0], top - 22, 'SPARK', size=7)
    d.text(ex - 6, py - 32, 'END GAS', size=7)
    d.text(gx1, gy0 + 12, 'CRANK ANGLE', size=7, anchor='end')
    d.text(gx0 - 4, gy0 - gh, 'p', size=8, anchor='end')
    d.text(gx0 + 100, gy0 - gh + 2, 'KNOCK', size=7, anchor='start')
    return d


PLATES = {'chemical-warfare': chemical_warfare, 'polymers': polymers, 'leaded-petrol': leaded_petrol}
