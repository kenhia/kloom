"""Plates for the chemistry subject's trail Alchemy's last century (sprint 025)."""
import math, random
from plates import D, wire, SOLIDS


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _band(a, b, wa, wb):
    """The two walls of a tube whose axis runs from a to b, wa wide at a and wb wide at b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n, dx / n
    return ([(a[0] + ox * wa / 2, a[1] + oy * wa / 2), (b[0] + ox * wb / 2, b[1] + oy * wb / 2)],
            [(a[0] - ox * wa / 2, a[1] - oy * wa / 2), (b[0] - ox * wb / 2, b[1] - oy * wb / 2)])


def _chord(c, r, y):
    """The chord of a circle at height y."""
    h = math.sqrt(r * r - (y - c[1]) ** 2)
    return [(c[0] - h, y), (c[0] + h, y)]


def brand_phosphorus():
    """Boyle's arrangement of 1680: a retort in the fire, its nose almost touching the water in a
    receiver; and the P4 tetrahedron that comes over."""
    d = D()
    B, rb = (92, 150), 32                      # the retort's bulb
    C, rc = (300, 204), 40                     # the receiver
    gy = 252                                   # the hearth
    a0 = -58                                   # where the neck leaves the bulb
    root = _pt(B, a0, rb)
    nose = (C[0] - 6, C[1] + 4)                # almost touching the water at y = C + 10
    water = C[1] + 10
    ux, uy = nose[0] - root[0], nose[1] - root[1]
    un = math.hypot(ux, uy)
    ang = math.degrees(math.atan2(uy, ux))
    # where the neck's axis crosses the receiver's wall, for the receiver's own mouth
    t = ((C[0] - root[0]) * ux + (C[1] - root[1]) * uy) / un ** 2
    foot = (root[0] + t * ux, root[1] + t * uy)
    off = math.hypot(foot[0] - C[0], foot[1] - C[1])
    back = math.sqrt(rc * rc - off * off)
    entry = (foot[0] - back * ux / un, foot[1] - back * uy / un)

    d.group('thin')
    d.line((20, gy), (380, gy))
    d.line((B[0], B[1] - 58), (B[0], gy))
    d.line((C[0], C[1] - 58), (C[0], gy))
    d.line(_pt(B, a0, 0), _pt(root, ang, un + 18))           # the neck's axis, from the bulb's centre
    d.circle(*B, rb + 12)
    d.circle(*C, rc + 12)
    d.group()
    # the furnace: a brick box with the bulb set in its top
    d.line((34, B[1] + 6), (34, gy), (150, gy), (150, B[1] + 6))
    d.line((34, B[1] + 6), (B[0] - rb - 2, B[1] + 6))
    d.line((B[0] + rb + 2, B[1] + 6), (150, B[1] + 6))
    # the retort: the bulb, and its neck tapering to the nose
    d.arc(*B, rb, a0 + 14, 360 + a0 - 14, n=72)
    for wall in _band(root, nose, 15, 5):
        d.line(*wall)
    # the receiver, with an opening where the neck goes in
    ea = math.degrees(math.atan2(entry[1] - C[1], entry[0] - C[0]))
    d.arc(*C, rc, ea + 13, ea + 347, n=72)
    d.line(_pt(C, ea + 13, rc), _pt(C, ea + 13, rc + 7))
    d.line(_pt(C, ea - 13, rc), _pt(C, ea - 13, rc + 7))
    d.group('mid')
    # bricks, the fire, the charge of syrup and sand, the water, the fumes and the falling drops
    for y in range(int(B[1] + 20), gy, 16):
        d.line((34, y), (B[0] - rb - 2 if y < B[1] + rb else 150, y))
        if y < B[1] + rb:
            d.line((B[0] + rb + 2, y), (150, y))
    d.arc(B[0], gy - 6, 26, 180, 360, n=24, ry=18)
    d.arc(B[0] - 12, gy - 6, 10, 180, 360, n=16, ry=12)
    d.arc(B[0] + 12, gy - 6, 10, 180, 360, n=16, ry=12)
    d.line(*_chord(B, rb, B[1] + 8))
    rnd = random.Random(1669)
    for _ in range(14):
        x = B[0] + rnd.uniform(-24, 24)
        y = B[1] + rnd.uniform(12, 26)
        if math.hypot(x - B[0], y - B[1]) < rb - 4:
            d.circle(x, y, 1.2)
    d.line(*_chord(C, rc, water))
    for k in range(3):
        y = water + 8 + 7 * k
        d.line(*[(x, y + 1.5 * math.sin((x - C[0]) / 5)) for x in _frange(C[0] - math.sqrt(rc * rc - (y - C[1]) ** 2) + 6,
                                                                            C[0] + math.sqrt(rc * rc - (y - C[1]) ** 2) - 6, 2.5)])
    for (x, y, r) in ((nose[0] + 4, water + 14, 2.6), (nose[0] + 12, water + 22, 2.2), (C[0] + 4, C[1] + rc - 6, 4)):
        d.circle(x, y, r)
    for k in range(3):
        cx = nose[0] + 14 + 9 * k
        d.line(*[(cx + 3 * math.sin(i / 2.2), C[1] - 6 - i * 2.2) for i in range(10)])
    # P4: four atoms at the corners of a tetrahedron
    tx, ty, ts = 330, 70, 20
    d.group('thin')
    d.circle(tx, ty, ts * math.sqrt(3) + 6)
    d.group()
    wire(d, SOLIDS['tetra'], tx, ty, ts, 0.5, 0.35)
    d.group('mid')
    from plates import rot
    for v in SOLIDS['tetra']:
        x, y, _ = rot(v, 0.5, 0.35)
        d.circle(tx + ts * x, ty - ts * y, 4)
    d.group('mid')
    d.text(B[0] - 20, B[1] - 50, 'RETORT', size=8)
    d.text(C[0] + 6, C[1] + rc + 20, 'RECEIVER · WATER', size=8)
    d.text(tx, ty + 50, 'P₄', size=9)
    d.text(200, 284, '4 NaPO₃ + 2 SiO₂ + 10 C → 2 Na₂SiO₃ + 10 CO + P₄', size=8)
    return d


def _frange(a, b, s):
    out, x = [], a
    while x <= b:
        out.append(x)
        x += s
    return out


def newton_alchemy():
    """The star regulus of antimony: a crucible in section, the regulus under its slag, and the
    star on the regulus's face in plan."""
    d = D()
    cx, top, bot = 108, 70, 214                   # the crucible's axis, rim and floor
    rt, rbot = 50, 30                             # half-widths at the rim and above the floor's curve
    px, py, pr = 292, 138, 66                     # the regulus in plan
    slag_y, reg_y = 150, 186                      # the melt's surface, and the top of the regulus

    def half(y):                                  # the crucible's inner half-width at height y
        return rt + (rbot - rt) * (y - top) / (bot - top)

    d.group('thin')
    d.line((cx, top - 20), (cx, bot + 30))
    d.line((24, bot + 20), (190, bot + 20))
    d.circle(px, py, pr + 12)
    for k in range(6):
        a = math.radians(30 * k)
        d.line((px - (pr + 16) * math.cos(a), py - (pr + 16) * math.sin(a)),
               (px + (pr + 16) * math.cos(a), py + (pr + 16) * math.sin(a)))
    d.line((cx + 58, reg_y), (px - pr - 4, reg_y))   # projection from the section to the plan
    d.group()
    # the crucible: its walls, rounded floor, and rim
    d.line((cx - rt - 6, top), (cx - rbot - 6, bot))
    d.line((cx + rt + 6, top), (cx + rbot + 6, bot))
    d.arc(cx, bot, rbot + 6, 0, 180, n=30, ry=14)
    d.line((cx - rt, top), (cx - rbot, bot))
    d.line((cx + rt, top), (cx + rbot, bot))
    d.arc(cx, bot, rbot, 0, 180, n=30, ry=8)
    d.line((cx - rt - 6, top), (cx - rt, top))
    d.line((cx + rt, top), (cx + rt + 6, top))
    # the regulus in plan
    d.circle(px, py, pr)
    d.group('mid')
    # the melt: slag above, the regulus below it
    d.line((cx - half(slag_y), slag_y), (cx + half(slag_y), slag_y))
    d.line((cx - half(reg_y), reg_y), (cx + half(reg_y), reg_y))
    rnd = random.Random(1680)
    for _ in range(18):
        y = rnd.uniform(slag_y + 5, reg_y - 5)
        x = cx + rnd.uniform(-1, 1) * (half(y) - 6)
        d.circle(x, y, 1.1)
    for k in range(4):
        y = reg_y + 7 + 6 * k
        w = half(y) - 5
        if w > 6:
            d.line((cx - w, y), (cx + w, y))
    # the star: six main rays, each feathered with side branches at sixty degrees
    segs = []
    for k in range(6):
        a = 30 + 60 * k
        tip = _pt((px, py), a, pr - 6)
        segs.append([(px, py), tip])
        for j in range(1, 8):
            s = j / 8
            base = _pt((px, py), a, (pr - 6) * s)
            ln = (pr - 6) * (1 - s) * 0.42
            segs.append([base, _pt(base, a + 60, ln)])
            segs.append([base, _pt(base, a - 60, ln)])
    d.lines(segs)
    d.group('mid')
    d.text(cx, 40, 'SECTION', size=8)
    d.text(px, 40, 'PLAN', size=8)
    d.text(cx + rt + 20, slag_y + 16, 'SLAG', size=7, anchor='start')
    d.text(cx + rbot + 22, reg_y + 20, 'REGULUS', size=7, anchor='start')
    d.text(200, 270, 'Sb₂S₃ + 3 Fe → 2 Sb + 3 FeS', size=9)
    d.text(200, 286, '100 g STIBNITE + 49 g IRON → 72 g ANTIMONY', size=7)
    return d


def bottger_porcelain():
    """Kaolinite fired: three windows on the clay as it heats, over a temperature scale."""
    d = D()
    x0, x1, ay = 36, 364, 236                     # the scale, 0 to 1,500 degrees
    tx = lambda T: x0 + (x1 - x0) * T / 1500
    wins = [(tx(150), 'KAOLINITE'), (tx(750), 'METAKAOLIN'), (tx(1400), 'MULLITE + GLASS')]
    wy, wr = 116, 50
    d.group('thin')
    for x, _ in wins:
        d.line((x, wy + wr + 4), (x, ay - 4))
        d.circle(x, wy, wr + 6)
    for T in range(0, 1501, 100):
        d.line((tx(T), ay), (tx(T), ay + (7 if T % 500 == 0 else 4)))
    d.group()
    d.line((x0, ay), (x1, ay))
    for x, _ in wins:
        d.circle(x, wy, wr)
    d.group('mid')
    # 1: kaolinite, stacked hexagonal plates, seen edge-on and in outline
    c = wins[0][0]
    for k in range(6):
        y = wy - 26 + 10 * k
        d.line((c - 30 + 3 * (k % 2), y), (c + 30 - 3 * (k % 2), y))
        d.line((c - 30 + 3 * (k % 2), y + 4), (c + 30 - 3 * (k % 2), y + 4))
    # 2: metakaolin, the layers broken into disorder
    c = wins[1][0]
    rnd = random.Random(1708)
    segs = []
    while len(segs) < 34:
        x, y = c + rnd.uniform(-40, 40), wy + rnd.uniform(-40, 40)
        a = math.radians(rnd.uniform(-35, 35))
        e = (x + 12 * math.cos(a), y + 12 * math.sin(a))
        if math.hypot(x - c, y - wy) < wr - 6 and math.hypot(e[0] - c, e[1] - wy) < wr - 6:
            segs.append([(x, y), e])
    d.lines(segs)
    # 3: mullite needles set in glass
    c = wins[2][0]
    rnd = random.Random(1710)
    segs = []
    while len(segs) < 26:
        x, y = c + rnd.uniform(-40, 40), wy + rnd.uniform(-40, 40)
        a = math.radians(rnd.uniform(0, 180))
        L = rnd.uniform(16, 30)
        p, q = (x - L / 2 * math.cos(a), y - L / 2 * math.sin(a)), (x + L / 2 * math.cos(a), y + L / 2 * math.sin(a))
        if math.hypot(p[0] - c, p[1] - wy) < wr - 5 and math.hypot(q[0] - c, q[1] - wy) < wr - 5:
            segs.append([p, q])
    d.lines(segs)
    d.group('mid')
    for x, name in wins:
        d.text(x, wy - wr - 14, name, size=7)
    for T in (0, 500, 1000, 1500):
        d.text(tx(T), ay + 42, f'{T:,}', size=7)
    d.text(x1 + 4, ay + 4, '°C', size=7, anchor='start')
    d.text(200, 292, '3 Al₂Si₂O₅(OH)₄ → 3Al₂O₃·2SiO₂ + 4 SiO₂ + 6 H₂O', size=8)
    return d


PLATES = {'brand-phosphorus': brand_phosphorus, 'newton-alchemy': newton_alchemy,
          'bottger-porcelain': bottger_porcelain}
