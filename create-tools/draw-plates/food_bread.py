"""Plates for Daily Bread's Bread trail (part `bread`, sprint 051). See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def pompeii_bakery():
    d = D()
    # A Pompeian mill in section on its axis, after Mau, Pompeii: Its Life and Art (1902), figs. 220-221:
    # the lava meta (a cone on a cylinder) in a masonry ring whose top is the flour trough; the catillus,
    # a double funnel whose lower cone fits over the meta and whose upper cone is the hopper; a wooden post
    # in a square hole in the cone's top carrying the iron pivot on which the crossbeam turns; shafts in
    # the catillus's shoulders, tied to the crossbeam by curved straps. Proportions are schematic.
    cx, ground = 200, 266
    apex, base_y, r_meta = 104, 206, 56                     # meta: cone from base_y up to apex
    def meta_r(y):
        return r_meta * (y - apex) / (base_y - apex)
    gap = 2.5                                               # the catillus barely touches the cone
    waist_lo, waist_hi, rim = 132, 120, 46                  # catillus: waist, then hopper up to the rim
    cat_bot = 200

    d.group('thin')
    d.line((cx, 24), (cx, ground + 8))                      # the axis
    d.line((20, ground), (380, ground))                     # the floor
    for s in (-1, 1):                                       # the meta's generators, carried to the apex
        d.line((cx + s * r_meta, base_y), (cx, apex - 14))
    d.arc(cx, apex, 26, 90 - math.degrees(math.atan(r_meta / (base_y - apex))),
          90 + math.degrees(math.atan(r_meta / (base_y - apex))))

    d.group()
    # the masonry ring with its trough, both halves of the section
    for s in (-1, 1):
        x_in, x_out = cx + s * (r_meta + 4), cx + s * (r_meta + 44)
        d.line((x_in, ground), (x_in, base_y + 22), (cx + s * (r_meta + 10), base_y + 22),
               (cx + s * (r_meta + 10), base_y + 30), (cx + s * (r_meta + 34), base_y + 30),
               (cx + s * (r_meta + 34), base_y + 14), (x_out, base_y + 14), (x_out, ground))
    # the meta: cylinder and cone
    d.line((cx - r_meta, ground), (cx - r_meta, base_y), (cx - 4, apex + 6), (cx + 4, apex + 6),
           (cx + r_meta, base_y), (cx + r_meta, ground))
    # the catillus: inner and outer profiles, each side
    for s in (-1, 1):
        w = meta_r(waist_lo) + gap
        inner = [(cx + s * (meta_r(cat_bot) + gap), cat_bot), (cx + s * w, waist_lo),
                 (cx + s * w, waist_hi), (cx + s * 60, rim)]
        outer = [(cx + s * 76, cat_bot), (cx + s * 34, waist_lo + 4), (cx + s * 34, waist_hi - 4),
                 (cx + s * 74, rim)]
        d.line(inner[0], outer[0])
        d.line(*inner)
        d.line(*outer)
        d.line(inner[-1], outer[-1])

    d.group('mid')
    # the post, the iron pivot and the crossbeam
    d.line((cx - 3, apex + 6), (cx - 3, 62), (cx + 3, 62), (cx + 3, apex + 6))
    d.line((cx, 62), (cx, 40))
    _box(d, cx - 86, 34, 172, 6)
    for s in (-1, 1):
        # shoulders with the shafts' sockets, and a strap from the beam's end down to each
        _box(d, cx + s * 34 - (14 if s < 0 else 0), waist_hi - 2, 14, 12)
        d.line((cx + s * 48, waist_hi + 4), (cx + s * 132, waist_hi + 4))
        d.line((cx + s * 48, waist_hi + 8), (cx + s * 132, waist_hi + 8))
        pts = [(cx + s * (84 - 36 * t * t), 40 + 78 * t) for t in [i / 12 for i in range(13)]]
        d.line(*pts)
    # grain down the hopper, flour out at the foot of the cone
    for s in (-1, 1):
        a, b = (cx + s * 40, 60), (cx + s * 18, 100)
        d.line(a, b)
        _arrow(d, a, b, 4)
        a, b = (cx + s * (r_meta + 8), base_y - 2), (cx + s * (r_meta + 20), base_y + 24)
        d.line(a, b)
        _arrow(d, a, b, 4)
    for i, (x, y) in enumerate([(-34, 54), (-26, 58), (-30, 64), (26, 56), (34, 60), (29, 66)]):
        d.ellipse(cx + x, y, 2.2, 1.1)

    d.group('mid')
    d.text(cx - 132, waist_hi - 6, 'SHAFT', size=7, anchor='start')
    d.text(cx + 132, waist_hi - 6, 'SHAFT', size=7, anchor='end')
    d.text(cx + 92, 30, 'CROSSBEAM ON PIVOT', size=7, anchor='start')
    d.text(cx - 84, 66, 'HOPPER', size=7, anchor='end')
    d.text(cx - 90, 172, 'CATILLUS', size=7, anchor='end')
    d.text(cx + 8, 180, 'META', size=7, anchor='start')
    d.text(cx + 104, 236, 'FLOUR TROUGH', size=7, anchor='start')
    d.text(cx - 104, 236, 'MASONRY', size=7, anchor='end')
    d.text(cx, 284, 'A POMPEIAN MILL IN SECTION · AFTER MAU', size=7)
    return d


# The Assize of Bread's table for the farthing wastel loaf, Statutes of the Realm vol. 1 (1810), pp. 199-200:
# wheat price a quarter in pence, loaf weight in shillings of the Tower pound (20 s. to the pound). Where the
# printed text gives a bracketed reading off the rule (3s., 3s. 6d., 4s.) the footnoted variant is used.
ASSIZE = [(12, 136), (18, 90 + 8 / 12), (24, 68), (30, 54 + 4.75 / 12), (36, 45 + 4 / 12),
          (42, 38 + 10.5 / 12), (48, 34), (54, 30), (60, 27 + 2.5 / 12), (66, 24 + 8.25 / 12),
          (72, 22 + 8 / 12), (78, 20 + 11 / 12), (84, 19 + 1 / 12), (90, 18 + 1.5 / 12), (96, 17),
          (102, 16), (108, 15 + 0.25 / 12), (114, 14 + 4.75 / 12), (120, 13 + 7 / 12),
          (126, 12 + 11.25 / 12), (132, 12 + 4.25 / 12), (138, 11 + 10 / 12), (144, 11 + 4 / 12),
          (240, 6 + 9.75 / 12)]


def assize_of_bread():
    d = D()
    # Loaf weight against the price of wheat: the statute's rows as points, and the rule they follow,
    # weight x price = 1,632 shilling-pence (our arithmetic), as a curve. Two rectangles from the origin show
    # the rule's meaning: the same area, the same bread for the same money.
    x0, x1, y0, y1 = 64, 380, 250, 36
    pmax, wmax = 252, 144

    def px(p):
        return x0 + (x1 - x0) * p / pmax

    def py(w):
        return y0 - (y0 - y1) * w / wmax

    d.group('thin')
    for p in (60, 120, 180, 240):
        d.line((px(p), y0), (px(p), y1))
    for w in (34, 68, 136):
        d.line((x0, py(w)), (x1, py(w)))
    for p, w in ((12, 136), (24, 68), (48, 34)):
        d.dashed((px(p), y0), (px(p), py(w)), (x0, py(w)), dash=3, gap=3)

    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))
    curve = [(px(p), py(1632 / p)) for p in [11.4 + i * 0.5 for i in range(int((250 - 11.4) / 0.5))]]
    d.line(*curve)

    d.group('mid')
    for p, w in ASSIZE:
        d.circle(px(p), py(w), 1.8)

    d.group('mid')
    for p, lab in ((60, '5s.'), (120, '10s.'), (180, '15s.'), (240, '20s.')):
        d.text(px(p), y0 + 12, lab, size=7)
    for w, lab in ((34, '0.6 KG'), (68, '1.2 KG'), (136, '2.4 KG')):
        d.text(x0 - 6, py(w) + 3, lab, size=7, anchor='end')
    d.text((x0 + x1) / 2, y0 + 26, 'PRICE OF A QUARTER OF WHEAT', size=7)
    d.text(px(12) + 8, py(136) - 5, '12d. · 6 L. 16 S.', size=7, anchor='start')
    d.text(px(240), py(6.8) - 10, '20s. · 6 S. 9¾d.', size=7, anchor='end')
    d.text(px(150), py(84), 'WEIGHT × PRICE = 1,632', size=7, anchor='start')
    d.text(px(150), py(84) + 11, 'EQUAL AREAS, EQUAL BREAD', size=7, anchor='start')
    d.text((x0 + x1) / 2, 24, 'THE FARTHING LOAF, BY THE ASSIZE OF BREAD', size=7)
    return d


def sliced_bread():
    d = D()
    # Rohwedder's slicing head in elevation, schematic after US patent 1,867,377 (filed 1928), fig. 4:
    # endless bands with their cutting runs in one vertical plane cross the rectangular opening the loaf is
    # pushed through; each loops over an idler pulley on an inverted V above and a V below, and back to the
    # central columns of driving rollers; adjacent bands run in opposite directions. Band count and spacing
    # are schematic.
    cx = 200
    n, pitch = 13, 16
    xs = [cx + (i - (n - 1) / 2) * pitch for i in range(n)]
    o_top, o_bot = 128, 186                                  # the opening
    o_l, o_r = xs[0] - 18, xs[-1] + 18

    def y_up(x):
        return 44 + 0.62 * abs(x - cx)

    def y_dn(x):
        return 272 - 0.62 * abs(x - cx)

    d.group('thin')
    d.line((cx, 22), (cx, 290))                              # the center line
    d.line((xs[0] - 30, y_up(xs[0] - 30)), (cx, 44), (xs[-1] + 30, y_up(xs[-1] + 30)))
    d.line((xs[0] - 30, y_dn(xs[0] - 30)), (cx, 272), (xs[-1] + 30, y_dn(xs[-1] + 30)))
    d.line((o_l - 30, (o_top + o_bot) / 2), (o_r + 30, (o_top + o_bot) / 2))

    d.group()
    _box(d, o_l, o_top, o_r - o_l, o_bot - o_top)            # the opening in the back plate
    for x in xs:                                             # the cutting runs
        d.line((x, y_up(x)), (x, y_dn(x)))

    d.group('mid')
    rollers_up = [52 + 7 * k for k in range((n + 1) // 2 + 1)]
    rollers_dn = [264 - 7 * k for k in range((n + 1) // 2 + 1)]
    for x in xs:
        d.circle(x, y_up(x), 3.2)                            # idler pulleys
        d.circle(x, y_dn(x), 3.2)
        k = int(round(abs(x - cx) / pitch))                  # return runs to the driving rollers
        if x != cx:
            d.line((x, y_up(x) - 3), (cx, rollers_up[k]))
            d.line((x, y_dn(x) + 3), (cx, rollers_dn[k]))
    for y in rollers_up + rollers_dn:
        d.circle(cx, y, 3.4)
    # the loaf's end in the opening: a tin loaf with a domed top
    lx0, lx1, lb, lt = xs[1] - 4, xs[-2] + 4, o_bot - 6, o_top + 18
    dome = [(lx0 + (lx1 - lx0) * i / 24, lt - 12 * math.sin(math.pi * i / 24)) for i in range(25)]
    d.line((lx0, lb), *dome, (lx1, lb), closed=True)
    # opposed motion on neighbouring bands
    for i, x in enumerate(xs):
        if i % 2:
            a, b = (x, 200), (x, 214)
        else:
            a, b = (x, 214), (x, 200)
        _arrow(d, a, b, 3.5)

    d.group('mid')
    d.text(o_l - 8, (o_top + o_bot) / 2 + 3, 'OPENING', size=7, anchor='end')
    d.text(o_r + 8, (o_top + o_bot) / 2 - 6, 'LOAF PUSHED', size=7, anchor='start')
    d.text(o_r + 8, (o_top + o_bot) / 2 + 5, 'THROUGH', size=7, anchor='start')
    d.text(xs[-1] + 12, y_up(xs[-1]) + 3, 'IDLER PULLEYS', size=7, anchor='start')
    d.text(cx + 12, 30, 'DRIVING ROLLERS', size=7, anchor='start')
    d.text(xs[-1] + 12, 210, 'NEIGHBORS RUN', size=7, anchor='start')
    d.text(xs[-1] + 12, 221, 'OPPOSITE WAYS', size=7, anchor='start')
    d.text(xs[0] - 12, 222, 'ENDLESS BANDS', size=7, anchor='end')
    d.text(cx, 296, 'AFTER US PATENT 1,867,377, FIG. 4 · SCHEMATIC', size=7)
    return d


def chorleywood():
    d = D()
    # Two schedules from mixing to the wrapped loaf, on one time axis (hours). Chorleywood's stages are
    # Cherfas (2020): mix 2-5 min, rest about 8 min, proof 45-50 min, bake 17-25 min, cool about 2 h,
    # 3-3.5 h in all. The old way: bulk fermentation about 3 hours, 5-6 hours in all; its other stages
    # are drawn schematically as one block, since the sources give only the total.
    x0, x1 = 50, 374
    hmax = 6

    def px(h):
        return x0 + (x1 - x0) * h / hmax

    y_old, y_cbp, bh = 96, 196, 26

    d.group('thin')
    for h in range(hmax + 1):
        d.line((px(h), 60), (px(h), 252))
    d.line((x0, 252), (x1, 252))

    d.group()
    # the old way: mix, bulk fermentation, then the rest
    _box(d, px(0), y_old, px(0.25) - px(0), bh)
    _box(d, px(0.25), y_old, px(3.25) - px(0.25), bh)
    d.dashed((px(3.25), y_old), (px(5.5), y_old), (px(5.5), y_old + bh), (px(3.25), y_old + bh), dash=4, gap=3)
    # Chorleywood: mix, rest, proof, bake, cool
    stages = [(0, 0.06), (0.06, 0.2), (0.2, 1.0), (1.0, 1.35), (1.35, 3.35)]
    for a, b in stages:
        _box(d, px(a), y_cbp, px(b) - px(a), bh)

    d.group('mid')
    for y, h in ((y_old + bh + 14, 5.5), (y_cbp + bh + 14, 3.35)):
        d.line((px(0), y), (px(h), y))
        _arrow(d, (px(0), y), (px(h), y), 4)
        _arrow(d, (px(h), y), (px(0), y), 4)
    a, b = (px(1.7), y_old + bh + 4), (px(0.1), y_cbp - 4)
    d.line(a, b)
    _arrow(d, a, b, 4)

    d.group('mid')
    d.text(x0, y_old - 8, 'THE OLD WAY', size=7, anchor='start')
    d.text(px(1.75), y_old + 16, 'BULK FERMENTATION · ABOUT 3 H', size=7)
    d.text(px(4.375), y_old + 16, 'PROOF, BAKE, COOL', size=7)
    d.text(px(2.75), y_old + bh + 24, '5 TO 6 HOURS', size=7)
    d.text(x0, y_cbp - 8, 'CHORLEYWOOD, 1961', size=7, anchor='start')
    d.text(px(0.6), y_cbp + 16, 'PROOF', size=7)
    d.text(px(2.35), y_cbp + 16, 'COOL', size=7)
    d.text(px(1.68), y_cbp + bh + 24, '3 TO 3½ HOURS', size=7)
    d.text(px(1.9), (y_old + y_cbp) / 2 + 12, 'MIX 2–5 MIN AT ABOUT 11 WH PER KG', size=7, anchor='start')
    d.text(px(1.9), (y_old + y_cbp) / 2 + 23, 'IN PLACE OF THE FERMENTATION', size=7, anchor='start')
    for h in range(hmax + 1):
        d.text(px(h), 266, f'{h} H', size=7)
    d.text((x0 + x1) / 2, 284, "THE OLD WAY'S LATER STAGES ARE SCHEMATIC", size=7)
    d.text((x0 + x1) / 2, 40, 'FLOUR TO WRAPPED LOAF, IN HOURS', size=7)
    return d


PLATES = {'pompeii-bakery': pompeii_bakery, 'assize-of-bread': assize_of_bread,
          'sliced-bread': sliced_bread, 'chorleywood': chorleywood}
