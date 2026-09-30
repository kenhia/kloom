"""Plates for part of the chemistry subject's second segment, Elements and alchemy (sprint 025):
Jabir and al-Razi, gunpowder, and the mineral acids."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _along(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _normal(a, b, k):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    return (-dy / n * k, dx / n * k)


def _tube(a, b, w0, w1):
    """The two walls of a tube from a to b, tapering from width w0 to w1."""
    n0, n1 = _normal(a, b, w0 / 2), _normal(a, b, w1 / 2)
    return ([(a[0] + n0[0], a[1] + n0[1]), (b[0] + n1[0], b[1] + n1[1])],
            [(a[0] - n0[0], a[1] - n0[1]), (b[0] - n1[0], b[1] - n1[1])])


def _crystal(d, x, y, s):
    """A small cubic crystal of sal ammoniac, seen corner on."""
    d.line((x, y - s), (x + s * 0.87, y - s / 2), (x + s * 0.87, y + s / 2), (x, y + s),
           (x - s * 0.87, y + s / 2), (x - s * 0.87, y - s / 2), closed=True)


def jabir():
    """Sal ammoniac subliming in a cucurbit and crystallising in the alembic's cap: NH4Cl ⇌ NH3 + HCl."""
    d = D()
    cx, cy, r = 128, 186, 44                    # the cucurbit's body
    nw, ny = 15, 128                             # half-width of its neck, and where the neck ends
    hx, hy, hr = cx, ny, 32                      # the alembic's cap, a dome on the neck
    gy = 262                                     # the furnace floor
    tip = _pt((hx, hy), 0, hr)                   # the cap's rim, where the spout leaves
    rc, rr = (318, 212), 26                      # the receiver
    ra = 208                                     # the direction its neck points, back towards the cap
    spout_end = _pt(rc, ra, rr + 10)
    d.group('thin')
    d.line((cx, 60), (cx, gy + 6))
    d.circle(cx, cy, r)
    d.line((hx - hr - 14, hy), (hx + hr + 14, hy))
    d.line(tip, _along(tip, spout_end, 1.18))
    d.line((24, gy), (376, gy))
    d.line((rc[0], rc[1] - rr - 40), (rc[0], gy))
    d.group()
    # the cucurbit, open at the top into its neck
    a0 = math.degrees(math.asin(nw / r))
    d.arc(cx, cy, r, -90 + a0, 270 - a0, n=72)
    top = cy - r * math.cos(math.radians(a0))
    d.lines([[(cx - nw, top), (cx - nw, ny + 6)], [(cx + nw, top), (cx + nw, ny + 6)]])
    # the cap: a dome whose rim turns in to a gutter that runs out through the spout
    d.arc(hx, hy, hr, 180, 360, n=48)
    d.line((hx - hr, hy), (hx - nw - 3, hy + 8))
    d.line((hx + hr, hy), (hx + nw + 3, hy + 8))
    w1, w2 = _tube(tip, spout_end, 7, 4)
    d.lines([w1, w2])
    # the receiver and its neck, which takes the spout
    d.arc(rc[0], rc[1], rr, ra + 14, ra + 360 - 14, n=60)
    for s in (1, -1):
        a = _pt(rc, ra + s * 14, rr)
        o = _pt((0, 0), ra, 18)
        d.line(a, (a[0] + o[0], a[1] + o[1]))
    # the furnace under the cucurbit
    d.line((cx - 62, gy), (cx - 62, cy + 18), (cx - r - 4, cy + 18))
    d.line((cx + 62, gy), (cx + 62, cy + 18), (cx + r + 4, cy + 18))
    d.group('mid')
    # the charge of salt in the bottom, and the fire
    d.arc(cx, cy, r - 6, 50, 130, n=20)
    for x in (cx - 30, cx - 10, cx + 10, cx + 30):
        d.line((x - 6, gy - 2), (x, gy - 22), (x + 6, gy - 2))
    # the two gases rising (drawn as paired wavy paths) and the crystals where they meet the cool cap
    for dx in (-8, 8):
        pts = [(cx + dx + 3 * math.sin(i / 3), cy + 18 - i * 2.2) for i in range(0, 34)]
        d.line(*pts)
    for a in range(200, 345, 18):
        x, y = _pt((hx, hy), a, hr - 5)
        _crystal(d, x, y, 3)
    for x in (rc[0] - 10, rc[0], rc[0] + 10, rc[0] - 5, rc[0] + 5):
        _crystal(d, x, rc[1] + rr - 7 - (4 if x in (rc[0] - 5, rc[0] + 5) else 0), 3)
    d.group('mid')
    d.text(hx, hy - hr - 10, 'AL-INBĪQ', size=8)
    d.text(cx - r - 26, cy + 4, 'HOT', size=8)
    d.text(hx + hr + 24, hy - 22, 'COOL', size=8)
    d.text(rc[0], rc[1] - rr - 48, 'RECEIVER', size=8)
    d.text(290, 70, 'NH₄Cl ⇌ NH₃ + HCl', size=10)
    d.text(290, 88, '53.5 g ⇌ 17 g + 36.5 g', size=8)
    return d


def gunpowder():
    """Gunpowder recipes on a triangle of saltpetre, sulfur and charcoal, closing in on the equation's mixture."""
    d = D()
    s, by = 250, 246
    top = (200, by - s * math.sqrt(3) / 2)       # 100% saltpetre
    sul = (200 - s / 2, by)                      # 100% sulfur
    cha = (200 + s / 2, by)                      # 100% charcoal

    def at(k, su, ch):
        t = k + su + ch
        k, su, ch = k / t, su / t, ch / t
        return (k * top[0] + su * sul[0] + ch * cha[0], k * top[1] + su * sul[1] + ch * cha[1])

    d.group('thin')
    grid = []
    for i in range(1, 10):
        f = i / 10
        grid.append([at(f, 1 - f, 0), at(f, 0, 1 - f)])          # lines of equal saltpetre
        grid.append([at(0, f, 1 - f), at(1 - f, f, 0)])          # equal sulfur
        grid.append([at(0, 1 - f, f), at(1 - f, 0, f)])          # equal charcoal
    d.lines(grid)
    d.group()
    d.line(top, sul, cha, closed=True)
    recipes = [
        ((6, 6, 1), '808', 'end', (-9, 4)),
        ((40, 20, 5), '1044', 'end', (-9, 4)),
        ((6, 1, 2), 'c. 1300', 'start', (8, 8)),
        ((7, 5, 5), 'HIME', 'start', (9, 4)),
        ((74.8, 11.9, 13.3), 'EQUATION', 'end', (-9, -5)),
        ((75, 10, 15), '1780', 'start', (8, -5)),
    ]
    d.group('mid')
    # the path the recipes take, from the alchemist's mixture to the equation's
    d.line(*[at(*r[0]) for r in recipes if r[1] in ('808', '1044', 'c. 1300', '1780')])
    d.group()
    for (k, su, ch), name, anchor, off in recipes:
        x, y = at(k, su, ch)
        d.circle(x, y, 3.2 if name != 'EQUATION' else 4.5)
    d.group('mid')
    for (k, su, ch), name, anchor, off in recipes:
        x, y = at(k, su, ch)
        d.text(x + off[0], y + off[1], name, size=7, anchor=anchor)
    d.text(top[0], top[1] - 8, 'SALTPETRE KNO₃', size=8)
    d.text(sul[0] - 4, by + 14, 'SULFUR', size=8)
    d.text(cha[0] + 4, by + 14, 'CHARCOAL', size=8)
    d.text(200, 286, '2 KNO₃ + S + 3 C → K₂S + N₂ + 3 CO₂', size=9)
    return d


def mineral_acids():
    """Aqua fortis distilled from a retort into a receiver, and the parting flask where it takes the silver from gold."""
    d = D()
    gy = 256
    bc, br = (92, 150), 38                       # the retort's bulb
    rc, rr = (230, 206), 24                      # the receiver
    neck_a = _pt(bc, -28, br)
    neck_b = _pt(rc, 222, rr - 3)                # the retort's beak, just inside the receiver's mouth
    pc, pr = (336, 210), 30                      # the parting flask
    pn, ptop = 9, 96                             # its neck's half-width and top
    d.group('thin')
    d.line((20, gy), (380, gy))
    d.circle(*bc, br)
    d.line(_along(neck_b, neck_a, 1.5), _along(neck_a, neck_b, 1.2))
    d.line((bc[0], bc[1] - br - 20), (bc[0], gy))
    d.line((pc[0], ptop - 14), (pc[0], gy))
    d.circle(*rc, rr)
    d.group()
    # the retort: a bulb whose neck bends down and tapers to a beak
    d.arc(bc[0], bc[1], br, -12, 318, n=72)
    up = _pt(bc, -44, br)
    lo = _pt(bc, -12, br)
    n0 = _normal(neck_a, neck_b, 2.5)
    d.line(up, (neck_b[0] - n0[0], neck_b[1] - n0[1]))
    d.line(lo, (neck_b[0] + n0[0], neck_b[1] + n0[1]))
    # the receiver, its mouth taking the beak
    d.arc(rc[0], rc[1], rr, 222 + 16, 222 + 344, n=60)
    # the furnace round the bulb's lower half, and its fire
    d.line((bc[0] - br - 12, gy), (bc[0] - br - 12, bc[1]), (bc[0] - br - 2, bc[1]))
    d.line((bc[0] + br + 12, gy), (bc[0] + br + 12, bc[1]), (bc[0] + br + 2, bc[1]))
    # the parting flask: a round body and a long neck
    a0 = math.degrees(math.asin(pn / pr))
    d.arc(pc[0], pc[1], pr, -90 + a0, 270 - a0, n=72)
    t0 = pc[1] - pr * math.cos(math.radians(a0))
    d.lines([[(pc[0] - pn, t0), (pc[0] - pn, ptop)], [(pc[0] + pn, t0), (pc[0] + pn, ptop)]])
    d.group('mid')
    # the charge in the bulb and the acid in the receiver and the flask
    d.line(_pt(bc, 150, br - 3), _pt(bc, 30, br - 3))
    d.line(_pt(rc, 160, rr - 2), _pt(rc, 20, rr - 2))
    d.line(_pt(pc, 200, pr - 1), _pt(pc, 340, pr - 1))
    for x in (bc[0] - 24, bc[0] - 8, bc[0] + 8, bc[0] + 24):
        d.line((x - 6, gy - 2), (x, gy - 24), (x + 6, gy - 2))
    # the rolled strip of silver-gold alloy, an Archimedean spiral, and the bubbles off it
    sp = [(pc[0] + 1.1 * t * math.cos(t), pc[1] + 12 + 1.1 * t * math.sin(t)) for t in [i * 0.25 for i in range(0, 50)]]
    d.line(*sp)
    for k, (dx, dy) in enumerate([(-8, -8), (6, -12), (-3, -20), (9, -26), (-6, -34), (2, -44), (-2, -60), (3, -80)]):
        d.circle(pc[0] + dx * (0.5 if dy < -40 else 1), pc[1] + 8 + dy, 1.8 if k < 5 else 1.4)
    # the fumes rising off the beak's joint
    d.line(*[(neck_b[0] - 6 + 3 * math.sin(i / 2.2), neck_b[1] - 10 - i * 2) for i in range(12)])
    d.group('mid')
    d.text(bc[0], bc[1] - br - 26, 'RETORT', size=8)
    d.text(rc[0], rc[1] + rr + 16, 'AQUA FORTIS', size=8)
    d.text(pc[0], ptop - 20, 'PARTING', size=8)
    d.text(pc[0] + 40, pc[1] + 16, 'Au', size=9)
    d.text(200, 282, '3 Ag + 4 HNO₃ → 3 AgNO₃ + NO + 2 H₂O', size=9)
    return d


PLATES = {'jabir': jabir, 'gunpowder': gunpowder, 'mineral-acids': mineral_acids}
