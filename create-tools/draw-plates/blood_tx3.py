"""Plates for In the Blood's Transfusion segment, its end: the Rh factor, the Coombs test and the
plastic blood bag (sprint 028, part tx3). See plates_for.py."""
import math
from plates import D


def _pt(cx, cy, r, a):
    """The point at `a` degrees on a circle (clockwise from +x; SVG's y runs down)."""
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _cell(d, cx, cy, r, ticks=0, start=0):
    """A red cell seen edge-on as a disc: a circle and its pale centre. `ticks` antigens on its rim."""
    d.circle(cx, cy, r)
    d.circle(cx, cy, r * 0.45)
    for k in range(ticks):
        a = start + 360 * k / ticks
        d.line(_pt(cx, cy, r, a), _pt(cx, cy, r + 3, a))


def _y(d, base, ang, stem=7, arm=6, spread=32):
    """An antibody: a Y whose arms end at `base` and open towards angle `ang` + 180, the stem pointing
    away along `ang`. Returns the tip of the stem (the Fc end)."""
    fork = _pt(base[0], base[1], arm, ang)
    tip = _pt(fork[0], fork[1], stem, ang)
    a1 = _pt(fork[0], fork[1], arm, ang + 180 - spread)
    a2 = _pt(fork[0], fork[1], arm, ang + 180 + spread)
    d.line(a1, fork, a2)
    d.line(fork, tip)
    return tip


def rh_factor():
    d = D()
    # Hemolytic disease of the newborn in two panels, each a strip of placenta between the mother's
    # blood (left) and the baby's (right). At the first birth, D-positive cells from the baby cross into
    # a D-negative mother and she makes anti-D; in a later pregnancy her IgG anti-D crosses the
    # placenta, coats the baby's cells and they are destroyed. Not to scale.
    panels = [(20, 'FIRST BIRTH'), (210, 'NEXT PREGNANCY')]
    top, bot = 60, 240
    d.group('thin')
    d.line((10, 260), (390, 260))
    d.line((200, 40), (200, 270))
    for x0, _ in panels:
        d.line((x0 + 85, 46), (x0 + 85, 254))                    # the placenta's midline
    d.group()
    # the placental barrier: a column of villi, semicircles bulging into the mother's side
    for x0, _ in panels:
        cx = x0 + 85
        for k in range(9):
            y = top + 10 + k * 20
            d.arc(cx, y, 10, 90, 270, n=12)
    # a break in the first panel's barrier: the bleed at delivery
    d.group('mid')
    for x0, _ in panels:
        cx = x0 + 85
        d.line((cx + 6, top), (cx + 6, bot))                     # the fetal side of the membrane
    # first panel: the baby's D-positive cells, one crossing at the break, and the mother's response
    x0 = panels[0][0]
    for (cx, cy) in ((x0 + 140, 100), (x0 + 150, 150), (x0 + 132, 200)):
        _cell(d, cx, cy, 14, ticks=8, start=10)
    _cell(d, x0 + 60, 150, 14, ticks=8, start=10)                # one has crossed into the mother
    d.line((x0 + 118, 150), (x0 + 80, 150))
    _arrow(d, (x0 + 118, 150), (x0 + 80, 150))
    # the mother's B cell, larger, turning out anti-D, arms outward
    bc = (x0 + 40, 100)
    d.circle(bc[0], bc[1], 16)
    d.circle(bc[0], bc[1], 6)
    for a in (130, 180, 230):
        _y(d, _pt(bc[0], bc[1], 36, a), a + 180)
    # second panel: maternal anti-D everywhere on the mother's side, crossing, coating the baby's cells
    x0 = panels[1][0]
    for (bx, by, ang) in ((x0 + 30, 80, 200), (x0 + 50, 120, 160), (x0 + 28, 160, 220),
                          (x0 + 55, 200, 170), (x0 + 35, 228, 140), (x0 + 60, 70, 120)):
        _y(d, (bx, by), ang)
    for y in (110, 170, 215):
        d.line((x0 + 64, y), (x0 + 112, y))
        _arrow(d, (x0 + 64, y), (x0 + 112, y))
    coated = ((x0 + 145, 95), (x0 + 152, 160))
    for cx, cy in coated:
        _cell(d, cx, cy, 14)
        for ang in (150, 200, 250, 300, 30, 90):
            _y(d, _pt(cx, cy, 14, ang), ang)
    # a destroyed cell: the rim broken into fragments
    cx, cy = x0 + 140, 222
    for a0 in range(0, 360, 45):
        d.arc(cx, cy, 14, a0 + 8, a0 + 30, n=4)
    d.group('mid')
    for x0, title in panels:
        d.text(x0 + 85, 32, title, size=7)
        d.text(x0 + 40, 275, 'MOTHER D−', size=7)
        d.text(x0 + 140, 275, 'BABY D+', size=7)
    d.text(panels[0][0] + 40, 70, 'ANTI-D MADE', size=7)
    d.text(panels[1][0] + 40, 50, 'IgG ANTI-D', size=7)
    d.text(panels[1][0] + 166, 250, 'CELLS DESTROYED', size=7, anchor='end')
    return d


def coombs():
    d = D()
    # The antiglobulin test. Left, its three tubes as Coombs, Mourant and Race laid it out in 1945:
    # cells and serum at 37 °C, the cells washed three times, then the rabbit serum added and the cells
    # read. Right, the mechanism: two red cells coated with human antibody (anti-D) that cannot reach
    # across the gap between them, joined by one rabbit anti-globulin molecule that binds the tails of
    # two. Not to scale.
    tubes = [30, 75, 120]
    tw, ttop, tbot = 26, 70, 220
    d.group('thin')
    d.line((14, 250), (170, 250))
    d.line((190, 30), (190, 270))
    ca, cb, r = (230, 160), (330, 160), 36
    d.line((ca[0], ca[1]), (cb[0], cb[1]))                          # the line of centres
    d.circle(ca[0], ca[1], r + 15)                                   # the reach of the bound antibody
    d.circle(cb[0], cb[1], r + 15)
    d.group()
    for x in tubes:                                                  # three glass tubes, 50 x 7 mm drawn large
        d.line((x - tw / 2, ttop), (x - tw / 2, tbot - tw / 2))
        d.arc(x, tbot - tw / 2, tw / 2, 180, 0, n=16)
        d.line((x + tw / 2, tbot - tw / 2), (x + tw / 2, ttop))
        d.line((x - tw / 2 - 3, ttop), (x + tw / 2 + 3, ttop))
    _cell(d, ca[0], ca[1], r)
    _cell(d, cb[0], cb[1], r)
    d.group('mid')
    # tube 1: cells and serum, a level, the cells settling; tube 2: washing, saline in and out;
    # tube 3: agglutinates, clumps rather than a smooth button
    d.line((tubes[0] - tw / 2, 150), (tubes[0] + tw / 2, 150))
    for k in range(6):
        d.circle(tubes[0] - 8 + (k % 3) * 8, 175 + (k // 3) * 14, 2.5)
    d.line((tubes[1] - tw / 2, 120), (tubes[1] + tw / 2, 120))
    for k in range(3):
        y = 40 - k * 6
        d.line((tubes[1] - 4 + k * 4, y + 22), (tubes[1] - 4 + k * 4, y + 10))
    _arrow(d, (tubes[1], 36), (tubes[1], 58))
    d.line((tubes[1], 36), (tubes[1], 58))
    for k in range(4):
        d.circle(tubes[1] - 6 + (k % 2) * 12, 196 + (k // 2) * 8, 2.5)
    d.line((tubes[2] - tw / 2, 150), (tubes[2] + tw / 2, 150))
    for (cx, cy, rr) in ((tubes[2] - 4, 178, 6), (tubes[2] + 5, 196, 7), (tubes[2] - 3, 200, 4)):
        d.circle(cx, cy, rr)
        d.circle(cx - rr * 0.3, cy - rr * 0.2, rr * 0.35)
    # human anti-D bound all round each cell, tails outward
    tails = {}
    for (c, angs) in ((ca, (-145, -90, 0, 35, 90, 145, -35)), (cb, (-90, -35, 35, 90, 145, 180, 215))):
        for ang in angs:
            tails[(c, ang)] = _y(d, _pt(c[0], c[1], r, ang), ang, stem=8, arm=7)
    # one rabbit anti-globulin bridging the two cells' nearest tails
    p, q = tails[(ca, -35)], tails[(cb, 215)]
    mid = ((p[0] + q[0]) / 2, min(p[1], q[1]) - 14)
    d.line(p, mid, q)
    d.line(mid, (mid[0], mid[1] - 14))
    d.group('mid')
    for x, s in zip(tubes, ('37 °C', 'WASH ×3', 'ANTI-HG')):
        d.text(x, 240, s, size=7)
    d.text(tubes[1], 26, 'SALINE', size=7)
    d.text(ca[0], ca[1] + 3, 'CELL', size=7)
    d.text(cb[0], cb[1] + 3, 'CELL', size=7)
    d.line((280, 112), (280, 84))
    d.text(280, 78, 'RABBIT ANTI-GLOBULIN', size=7)
    d.text(280, 236, 'HUMAN ANTI-D ON EACH CELL', size=7)
    return d


def blood_bag():
    d = D()
    # A triple bag after the light spin, in a plasma expressor: red cells packed at the bottom of the
    # primary bag, platelet-rich plasma above them. The expressor's front plate, pulled by a spring,
    # squeezes the bag, and the plasma runs up the attached tubing to the first satellite bag; the second
    # waits behind a closed clamp. Inset: a swing-out rotor, where the force depends on the radius r as
    # well as the speed, RCF = 1.118 × 10⁻⁵ × r (cm) × rpm². Not to scale.
    bx0, bx1, btop, bbot = 50, 130, 70, 250
    d.group('thin')
    d.line((20, 262), (380, 262))
    d.line(((bx0 + bx1) / 2, 40), ((bx0 + bx1) / 2, 262))           # the bag's axis
    rc, rr = (322, 222), 34                                           # the rotor inset
    d.circle(rc[0], rc[1], rr)
    d.line((rc[0] - rr - 8, rc[1]), (rc[0] + rr + 8, rc[1]))
    d.line((rc[0], rc[1] - rr - 8), (rc[0], rc[1] + rr + 8))
    d.group()
    # the primary bag: a rounded rectangle, its port at the top
    rad = 10
    d.line((bx0 + rad, btop), (bx1 - rad, btop))
    d.arc(bx1 - rad, btop + rad, rad, -90, 0, n=8)
    d.line((bx1, btop + rad), (bx1, bbot - rad))
    d.arc(bx1 - rad, bbot - rad, rad, 0, 90, n=8)
    d.line((bx1 - rad, bbot), (bx0 + rad, bbot))
    d.arc(bx0 + rad, bbot - rad, rad, 90, 180, n=8)
    d.line((bx0, bbot - rad), (bx0, btop + rad))
    d.arc(bx0 + rad, btop + rad, rad, 180, 270, n=8)
    # the expressor: a back plate, a front plate hinged at the bottom and leaning on the bag
    d.line((bx0 - 12, 40), (bx0 - 12, 262))
    hinge = (bx1 + 10, 262)
    d.line(hinge, (bx1 + 4, 50))
    # tubing from the port, up and over to a Y, then to two satellite bags
    port = ((bx0 + bx1) / 2, btop)
    y_junction = (200, 54)
    d.line(port, (port[0], 34), (170, 34), y_junction)
    sats = [(230, 70, 290, 150), (300, 70, 360, 150)]
    d.line(y_junction, (260, 54), (260, sats[0][1]))
    d.line(y_junction, (200, 44), (330, 44), (330, sats[1][1]))
    for x0, y0, x1, y1 in sats:
        d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)
    # the rotor's arm and a swinging bucket at radius rr, swung out horizontal
    bucket = _pt(rc[0], rc[1], rr, -30)
    d.line(rc, bucket)
    a = math.radians(-30)
    ux, uy = math.cos(a), math.sin(a)
    corners = [(bucket[0] + ux * s + -uy * t, bucket[1] + uy * s + ux * t) for s, t in ((0, -7), (16, -7), (16, 7), (0, 7))]
    d.line(*corners, closed=True)
    d.group('mid')
    # red cells hatched in the bottom 45 per cent; a thin buffy coat; plasma open above
    split = bbot - 0.45 * (bbot - btop)
    for k, y in enumerate(range(int(split) + 6, bbot - 2, 7)):
        d.line((bx0 + 4 + (k % 2) * 4, y), (bx1 - 4, y))
    d.line((bx0, split), (bx1, split))
    d.line((bx0, split - 3), (bx1, split - 3))
    # the spring that pulls the front plate shut
    sx0, sx1, sy = bx1 + 6, bx1 + 50, 200
    pts = [(sx0 + (sx1 - sx0) * i / 12, sy + (5 if i % 2 else -5) * (0 < i < 12)) for i in range(13)]
    d.line(*pts)
    d.line((sx1, sy - 10), (sx1, sy + 10))
    # flow along the tubing; the closed clamp on the second line
    _arrow(d, (port[0], 50), (port[0], 38))
    _arrow(d, (230, 54), (252, 54))
    d.lines([[(312, 40), (320, 48)], [(312, 48), (320, 40)]])
    # plasma arriving in the first satellite
    d.line((232, 128), (288, 128))
    # rotation about the rotor's axis
    d.arc(rc[0], rc[1], rr + 12, -150, -60, n=12)
    _arrow(d, _pt(rc[0], rc[1], rr + 12, -66), _pt(rc[0], rc[1], rr + 12, -60))
    d.group('mid')
    d.text(bx0 + 40, 120, 'PLASMA', size=7)
    d.text(bx0 + 40, 132, 'AND PLATELETS', size=7)
    d.text(bx0 + 40, 230, 'RED CELLS', size=7)
    d.text(295, 166, 'SATELLITE BAGS', size=7)
    d.text(bx1 + 54, 215, 'SPRING', size=7, anchor='start')
    m = _pt(rc[0], rc[1], rr / 2, -30)
    d.text(m[0] - 4, m[1] - 4, 'r', size=7)
    d.text(rc[0], 284, 'RCF ∝ r × rpm²', size=7)
    return d


PLATES = {'rh-factor': rh_factor, 'coombs': coombs, 'blood-bag': blood_bag}
