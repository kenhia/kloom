"""Plates for the chemistry subject's chemical revolution, part 1: Boyle, phlogiston, fixed air (sprint 025)."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


# Boyle's table of the condensation of the air (A Defence of the Doctrine touching the
# Spring and Weight of the Air, 1662, p. 60): column A, the equal spaces (quarter inches)
# the trapped air filled, and column D, the pressure on it in inches of mercury.
BOYLE_A = [48, 46, 44, 42, 40, 38, 36, 34, 32, 30, 28, 26, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12]
BOYLE_D = [29 + 2 / 16, 30 + 9 / 16, 31 + 15 / 16, 33 + 8 / 16, 35 + 5 / 16, 37, 39 + 5 / 16, 41 + 10 / 16,
           44 + 3 / 16, 47 + 1 / 16, 50 + 5 / 16, 54 + 5 / 16, 58 + 13 / 16, 61 + 5 / 16, 64 + 1 / 16,
           67 + 1 / 16, 70 + 11 / 16, 74 + 2 / 16, 77 + 14 / 16, 82 + 12 / 16, 87 + 14 / 16, 93 + 1 / 16,
           100 + 7 / 16, 107 + 13 / 16, 117 + 9 / 16]


def boyle():
    """Boyle's J-tube in section at half the air's first volume, and his 25 readings on the hyperbola PV = k."""
    d = D()
    s = 4.0                                   # px per inch on the tube
    bx, by, r = 62, 262, 16                   # the bend's centre, and its radius to the tube's axis
    w = 5                                     # half the bore, drawn
    xs, xl = bx - r, bx + r                   # axes of the short (sealed) leg and the long (open) leg
    top_s, zero = 150, 198                    # the sealed end; the mercury's level when the air was shut in
    air_in = 6                                # the drawing's moment: the air squeezed from 12 inches to 6
    lvl_s = zero - (12 - air_in) * s
    lvl_l = lvl_s - (29 + 11 / 16) * s        # Boyle's B for 24 spaces: 29 11/16 inches above the short leg
    # the graph: volume in Boyle's spaces across, pressure in inches of mercury up
    gx0, gx1, gy0, gy1 = 168, 380, 262, 36
    vmax, pmax = 50, 120
    X = lambda a: gx0 + (gx1 - gx0) * a / vmax
    Y = lambda p: gy0 - (gy0 - gy1) * p / pmax
    k = 48 * BOYLE_D[0]
    d.group('thin')
    # the tube's scale: twelve inches on the short leg; the level lines across to the long leg
    d.lines([[(xs - w - 4, zero - i * s), (xs - w - (11 if i % 3 == 0 else 8), zero - i * s)]
             for i in range(13)])
    d.line((xs - w - 3, lvl_s), (xl + w + 10, lvl_s))
    d.line((xl - w - 6, lvl_l), (xl + w + 10, lvl_l))
    d.line((xs, top_s - 10), (xs, by + r + 8))
    d.line((xl + 14, lvl_l), (xl + 14, lvl_s))
    d.line((xl, 10), (xl, by + r + 8))
    # the graph's axes, ticks and the curve PV = k through Boyle's first reading
    d.line((gx0, gy1 - 6), (gx0, gy0), (gx1 + 6, gy0))
    d.lines([[(X(a), gy0), (X(a), gy0 + 4)] for a in (12, 24, 36, 48)])
    d.lines([[(gx0 - 4, Y(p)), (gx0, Y(p))] for p in (30, 60, 90, 120)])
    d.line(*[(X(a), Y(k / a)) for a in [11.5 + i * 0.25 for i in range(int((48.5 - 11.5) / 0.25) + 1)]])
    d.lines([[(X(24), gy0), (X(24), Y(k / 24))], [(gx0, Y(k / 24)), (X(24), Y(k / 24))],
             [(X(48), gy0), (X(48), Y(k / 48))], [(gx0, Y(k / 48)), (X(48), Y(k / 48))]])
    d.group()
    # the J-tube: two walls of each leg and the bend between them, sealed at the short end
    d.line((xs - w, top_s + w), (xs - w, by))
    d.line((xs + w, top_s + w), (xs + w, by))
    d.arc(xs, top_s + w, w, 180, 360, n=12)
    d.line((xl - w, 14), (xl - w, by))
    d.line((xl + w, 14), (xl + w, by))
    d.arc(bx, by, r + w, 0, 180, n=36)
    d.arc(bx, by, r - w, 0, 180, n=24)
    d.group('mid')
    # the mercury: its surfaces in each leg, and hatching through the column that holds the air
    d.lines([[(xs - w, lvl_s), (xs + w, lvl_s)], [(xl - w, lvl_l), (xl + w, lvl_l)]])
    hatch = []
    y = lvl_s + 6
    while y < by:
        hatch.append([(xs - w, y), (xs + w, y - 4)])
        y += 9
    y = lvl_l + 6
    while y < by:
        hatch.append([(xl - w, y), (xl + w, y - 4)])
        y += 9
    d.lines(hatch)
    # Boyle's 25 readings, as he printed them
    for a, p in zip(BOYLE_A, BOYLE_D):
        d.circle(X(a), Y(p), 1.9)
    d.group('mid')
    d.text(xs - 34, (top_s + lvl_s) / 2 + 3, 'AIR', size=7)
    d.text(xs - 30, zero + 3, '0', size=7)
    d.text(xs - 30, top_s + 3, '12', size=7)
    d.text(xl + 19, lvl_l + (lvl_s - lvl_l) / 2 - 2, '29 11/16', size=7, anchor='start')
    d.text(xl + 19, lvl_l + (lvl_s - lvl_l) / 2 + 8, 'INCHES', size=7, anchor='start')
    d.text(X(24), gy0 + 13, '24', size=7)
    d.text(X(48), gy0 + 13, '48', size=7)
    d.text(X(12), gy0 + 13, '12', size=7)
    d.text(gx0 - 7, Y(60) + 3, '60', size=7, anchor='end')
    d.text(gx0 - 7, Y(120) + 3, '120', size=7, anchor='end')
    d.text((gx0 + gx1) / 2 + 20, gy0 + 28, 'VOLUME · SPACES OF ¼ INCH', size=7)
    d.text(gx0 + 8, gy1 - 8, 'PRESSURE · INCHES OF MERCURY', size=7, anchor='start')
    d.text(X(30), Y(k / 18), 'P × V ≈ 1,400', size=8, anchor='start')
    return d


def phlogiston():
    """A beam balance with tin on one pan and its calx on the other: the calx, which should have lost
    phlogiston, is heavier. 100 parts of tin give about 127 of calx (Sn + O2 -> SnO2, by our arithmetic)."""
    d = D()
    fx, fy = 200, 70                          # the fulcrum
    L = 120                                   # half the beam
    tilt = math.radians(9)                    # the calx side goes down
    a = (fx - L * math.cos(tilt), fy - L * math.sin(tilt))   # the tin's end, raised
    b = (fx + L * math.cos(tilt), fy + L * math.sin(tilt))   # the calx's end, lowered
    hang = 92
    pw, ph = 46, 10
    d.group('thin')
    # the level line, the arc the beam's ends sweep, the verticals of the hangers, and the pillar's axis
    d.line((fx - L - 30, fy), (fx + L + 30, fy))
    d.arc(fx, fy, L, 180 - 16, 180 + 16, n=20)
    d.arc(fx, fy, L, -16, 16, n=20)
    d.line((a[0], a[1] - 10), (a[0], a[1] + hang + 30))
    d.line((b[0], b[1] - 10), (b[0], b[1] + hang + 30))
    d.line((fx, fy - 26), (fx, 262))
    d.arc(fx, fy, 40, 0, 9, n=6)
    d.group()
    # the pillar and its foot, the beam, the pointer, the knife-edge
    d.line((fx - 5, fy + 8), (fx - 5, 250))
    d.line((fx + 5, fy + 8), (fx + 5, 250))
    d.line((fx - 60, 262), (fx - 50, 250), (fx + 50, 250), (fx + 60, 262), closed=True)
    d.line((fx - 8, fy + 8), (fx, fy - 2), (fx + 8, fy + 8), closed=True)
    d.line(a, b)
    px = (fx + 34 * math.sin(tilt), fy - 34 * math.cos(tilt))
    d.line((fx, fy), px)
    # the pans on their three cords (two seen), each a shallow dish
    for e in (a, b):
        cx, cy = e[0], e[1] + hang
        d.lines([[e, (cx - pw / 2, cy)], [e, (cx + pw / 2, cy)]])
        d.arc(cx, cy, pw / 2, 0, 180, n=24, ry=ph)
        d.line((cx - pw / 2, cy), (cx + pw / 2, cy))
    d.group('mid')
    # on the tin's pan a small ingot; on the calx's pan a heap of powder
    cx, cy = a[0], a[1] + hang
    d.line((cx - 12, cy), (cx - 9, cy - 8), (cx + 9, cy - 8), (cx + 12, cy), closed=True)
    cx, cy = b[0], b[1] + hang
    d.arc(cx, cy, 15, 180, 360, n=24, ry=11)
    d.lines([[(cx - 7, cy - 4), (cx - 5, cy - 4)], [(cx + 2, cy - 7), (cx + 4, cy - 7)], [(cx + 8, cy - 3), (cx + 10, cy - 3)]])
    d.group('mid')
    d.text(a[0], a[1] + hang + 24, 'TIN · 100', size=8)
    d.text(b[0], b[1] + hang + 24, 'CALX · 127', size=8)
    d.text(fx + 46, fy - 6, '9°', size=7, anchor='start')
    d.text(100, 284, 'PHLOGISTON · TIN → CALX + φ', size=7)
    d.text(300, 284, 'OXYGEN · Sn + O₂ → SnO₂', size=7)
    return d


def fixed_air():
    """Air from magnesia alba, caught over water: a flask, a bent tube, a jar inverted in a trough;
    and Black's ounce of magnesia (480 grains) before and after the fire (200 grains), drawn to scale."""
    d = D()
    # the flask: a round body on a flat foot, a neck, and the stopper through which the tube runs
    fx, fy, fr = 92, 150, 34
    neck_w, neck_top = 9, fy - fr - 26
    # the trough and the jar
    tx0, tx1, ty0, ty1, wl = 200, 372, 112, 212, 132        # trough walls, floor, and the water line
    jx, jw, jtop, jmouth = 300, 26, 58, 176                 # jar axis, half width, closed top, open mouth
    gas = 104                                               # the gas has pushed the water down to here
    d.group('thin')
    d.line((fx, neck_top - 16), (fx, fy + fr + 10))
    d.line((jx, jtop - 14), (jx, ty1 + 10))
    d.line((tx0 - 10, wl), (tx1 + 10, wl))
    d.line((jx - jw - 8, gas), (jx + jw + 8, gas))
    d.circle(fx, fy, fr + 6)
    d.group()
    # flask body (an arc from one side of the neck round to the other), neck and foot
    a0 = math.degrees(math.asin(neck_w / fr))
    d.arc(fx, fy, fr, -90 + a0, 270 - a0, n=64)
    d.line((fx - neck_w, fy - fr * math.cos(math.radians(a0))), (fx - neck_w, neck_top))
    d.line((fx + neck_w, fy - fr * math.cos(math.radians(a0))), (fx + neck_w, neck_top))
    d.line((fx - 22, fy + fr - 4), (fx - 26, fy + fr + 6), (fx + 26, fy + fr + 6), (fx + 22, fy + fr - 4))
    # the trough in section
    d.line((tx0, ty0), (tx0, ty1), (tx1, ty1), (tx1, ty0))
    # the jar, closed at the top and open at the mouth, hung from a cord
    d.line((jx - jw, jmouth), (jx - jw, jtop + 8))
    d.arc(jx, jtop + 8, jw, 180, 360, n=24, ry=8)
    d.line((jx + jw, jtop + 8), (jx + jw, jmouth))
    d.line((jx, jtop), (jx, 20))
    # the delivery tube: up from the flask, over the trough's rim, down through the water and up under the jar's mouth
    tube = [(fx, neck_top + 6), (fx, 64), (206, 64), (216, 74), (216, 196), (224, 204), (jx - 10, 204), (jx - 6, jmouth - 6)]
    d.line(*tube)
    d.group('mid')
    # the water: its surface in the trough outside the jar, and inside the jar pushed down by the gas
    d.lines([[(tx0, wl), (jx - jw, wl)], [(jx + jw, wl), (tx1, wl)], [(jx - jw, gas), (jx + jw, gas)]])
    d.lines([[(tx0 + 8 + 14 * i, wl + 12 + 20 * (i % 3)), (tx0 + 16 + 14 * i, wl + 12 + 20 * (i % 3))]
             for i in range(12) if not (jx - jw - 8 < tx0 + 8 + 14 * i < jx + jw)])
    # bubbles rising from the tube's end into the jar
    for k, (bx, by, br) in enumerate([(jx - 5, jmouth - 16, 2.5), (jx - 1, jmouth - 34, 3), (jx + 3, jmouth - 52, 3.5)]):
        d.circle(bx, by, br)
    # the charge in the flask: powder under the acid, and the level of the acid
    d.line((fx - fr + 5, fy + 8), (fx + fr - 5, fy + 8))
    for i in range(7):
        x = fx - 21 + 7 * i
        d.circle(x, fy + fr - 12 - (i % 2) * 4, 2)
    # Black's weighing, to scale: an ounce of magnesia alba, and what the fire left of it
    sx, sy, sw = 40, 262, 0.62                                # 0.62 px per grain
    d.group()
    d.line((sx, sy - 12), (sx + 480 * sw, sy - 12), (sx + 480 * sw, sy - 4), (sx, sy - 4), closed=True)
    d.line((sx, sy + 8), (sx + 200 * sw, sy + 8), (sx + 200 * sw, sy + 16), (sx, sy + 16), closed=True)
    d.group('thin')
    d.lines([[(sx + 200 * sw, sy - 16), (sx + 200 * sw, sy + 20)], [(sx + 480 * sw, sy - 16), (sx + 480 * sw, sy + 20)]])
    d.group('mid')
    d.text(sx + 480 * sw + 6, sy - 5, '480 GRAINS', size=7, anchor='start')
    d.text(sx + 200 * sw + 6, sy + 15, '200 AFTER THE FIRE · 7/12 LOST', size=7, anchor='start')
    d.text(fx, 30, 'MAGNESIA ALBA + ACID', size=7)
    d.text(jx, 238, 'FIXED AIR OVER WATER', size=7)
    return d


PLATES = {'boyle': boyle, 'phlogiston': phlogiston, 'fixed-air': fixed_air}
