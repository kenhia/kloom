"""Plates for In the Blood's first segment, What we believed (sprint 028). See plates_for.py."""
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


def humours():
    d = D()
    # A glass of drawn blood left to stand, in section (Fåhræus's suggestion): clot at the bottom,
    # red cells over it, a thin white layer, clear yellow serum on top. Heights are a sketch, not data.
    gx0, gx1, top, base = 40, 104, 44, 262
    layers = [('SERUM', 120), ('WHITE', 128), ('RED', 186), ('CLOT', base)]   # the bottom of each layer
    d.group('thin')
    d.line((gx0 - 14, top), (gx0 - 14, base))                       # a height scale beside the glass
    for y in range(top, base + 1, 18):
        d.line((gx0 - 18, y), (gx0 - 14, y))
    for y in (120, 128, 186):                                       # the layer boundaries carried across
        d.line((gx0 - 22, y), (gx1 + 10, y))
    # the square of qualities: hot and cold across, wet and dry up and down, a circle for the year
    cx, cy, r = 296, 150, 70
    d.line((cx - r - 12, cy), (cx + r + 12, cy))
    d.line((cx, cy - r - 12), (cx, cy + r + 12))
    d.circle(cx, cy, r)
    d.group()
    # the glass: a straight tube with a lip and a rounded foot
    d.line((gx0 - 4, top - 6), (gx0, top), (gx0, base - 10))
    d.arc((gx0 + gx1) / 2, base - 10, (gx1 - gx0) / 2, 180, 0, n=24, ry=10)
    d.line((gx1, base - 10), (gx1, top), (gx1 + 4, top - 6))
    d.line((gx0, 112), (gx1, 112))                                  # the meniscus of the serum
    # the square, its corners on the circle
    sq = [_pt(cx, cy, r, a) for a in (-135, -45, 45, 135)]
    d.line(*sq, closed=True)
    d.group('mid')
    # the clot, hatched dark; the red layer, hatched open; the white layer, a pair of lines
    for x in range(gx0 + 4, gx1, 6):
        d.line((x, 190), (x - 4, base - 6 if gx0 + 8 < x < gx1 - 8 else base - 14))
    for k, y in enumerate(range(134, 184, 8)):
        d.line((gx0 + 4 + (k % 2) * 6, y), (gx1 - 4, y))
    d.line((gx0, 120), (gx1, 120))
    d.line((gx0, 128), (gx1, 128))
    # a quadrant mark for each humour: its two qualities meet in it
    d.group('mid')
    d.text(gx1 + 14, 116, 'YELLOW BILE', size=7, anchor='start')
    d.text(gx1 + 14, 132, 'PHLEGM', size=7, anchor='start')
    d.text(gx1 + 14, 160, 'BLOOD', size=7, anchor='start')
    d.text(gx1 + 14, 226, 'BLACK BILE', size=7, anchor='start')
    d.text(cx + r + 14, cy - 4, 'HOT', size=7, anchor='start')
    d.text(cx - r - 14, cy - 4, 'COLD', size=7, anchor='end')
    d.text(cx, cy - r - 16, 'WET', size=7)
    d.text(cx, cy + r + 22, 'DRY', size=7)
    for a, s in ((-45, 'SPRING'), (45, 'SUMMER'), (135, 'AUTUMN'), (-135, 'WINTER')):
        x, y = _pt(cx, cy, r * 0.5, a)
        d.text(x, y + 3, s, size=7)
    return d


def galen():
    d = D()
    # Galen's two systems in plan: the liver makes blood and sends it out through the veins to be
    # used up; a little seeps through pits in the septum to the left ventricle, meets pneuma from
    # the lung, and leaves through the arteries. Not to scale.
    liver = (96, 232)
    rv, lv = (178, 150), (240, 150)
    d.group('thin')
    d.line((40, 150), (360, 150))                                   # the heart's axis
    d.line((209, 70), (209, 230))                                   # the septum's line
    d.group()
    # the liver: a lobed outline
    pts = []
    for i in range(49):
        t = 2 * math.pi * i / 48
        rr = 34 + 6 * math.sin(2 * t) + 3 * math.sin(5 * t)
        pts.append((liver[0] + 1.6 * rr * math.cos(t), liver[1] + 0.8 * rr * math.sin(t)))
    d.line(*pts, closed=True)
    # the two ventricles, either side of a thick septum
    d.arc(rv[0], rv[1], 30, 90, 270, n=24, ry=46)
    d.line((rv[0], rv[1] - 46), (204, rv[1] - 46), (204, rv[1] + 46), (rv[0], rv[1] + 46))
    d.arc(lv[0], lv[1], 30, -90, 90, n=24, ry=46)
    d.line((lv[0], lv[1] - 46), (214, lv[1] - 46), (214, lv[1] + 46), (lv[0], lv[1] + 46))
    # the vena cava from the liver up into the right ventricle
    d.line((liver[0] + 34, liver[1] - 22), (150, 190), (162, 176))
    # the lung, above, and the "venous artery" bringing pneuma down to the left ventricle
    d.ellipse(300, 52, 52, 26)
    d.line((282, 76), (256, 108))
    # the aorta out of the left ventricle, branching to the body
    d.line((262, 180), (300, 220), (350, 236))
    d.line((300, 220), (318, 262))
    d.group('mid')
    # veins from the liver, each ending in the tissue that uses its blood (open ends, no return)
    for a in (150, 185, 215, 250):
        x0, y0 = _pt(liver[0], liver[1], 46, a)
        x1, y1 = _pt(liver[0], liver[1], 78, a)
        d.line((x0, y0), (x1, y1))
        d.lines([[(x1 - 3, y1 - 3), (x1 + 3, y1 + 3)], [(x1 - 3, y1 + 3), (x1 + 3, y1 - 3)]])
    # the pits in the septum: funnels with wide mouths on the right, narrowing out of sight
    for y in (124, 142, 160, 178):
        d.line((204, y - 5), (209, y - 1))
        d.line((204, y + 5), (209, y + 1))
        d.line((209, y), (213, y), cls=None)
    # the direction of each flow
    _arrow(d, (150, 190), (162, 176))
    _arrow(d, (282, 76), (256, 108))
    _arrow(d, (300, 220), (350, 236))
    d.line((196, 196), (222, 196))
    _arrow(d, (196, 196), (222, 196))
    d.group('mid')
    d.text(liver[0], liver[1] + 4, 'LIVER', size=7)
    d.text(rv[0] - 6, rv[1] + 3, 'RV', size=7)
    d.text(lv[0] + 6, lv[1] + 3, 'LV', size=7)
    d.text(300, 55, 'LUNG', size=7)
    d.text(209, 62, 'SEPTUM PITS', size=7)
    d.text(46, 292, 'VEINS: BLOOD MADE, SENT OUT, USED UP', size=7, anchor='start')
    return d


def ibn_al_nafis():
    d = D()
    # The heart in section with a solid septum: the right ventricle's blood can reach the left only
    # through the lung, by the pulmonary artery, small passages, and the pulmonary vein. Galen's
    # route through the septum is drawn dashed and struck through. Not to scale.
    rv, lv = (150, 196), (250, 196)
    lung = (200, 58)
    d.group('thin')
    d.line((40, 196), (360, 196))
    d.line((200, 30), (200, 270))
    d.group()
    # the ventricles and a thick, solid septum between them
    d.arc(rv[0], rv[1], 40, 90, 270, n=28, ry=56)
    d.line((rv[0], rv[1] - 56), (188, rv[1] - 56), (188, rv[1] + 56), (rv[0], rv[1] + 56))
    d.arc(lv[0], lv[1], 40, -90, 90, n=28, ry=56)
    d.line((lv[0], lv[1] - 56), (212, lv[1] - 56), (212, lv[1] + 56), (lv[0], lv[1] + 56))
    # the lung above, and the two vessels that join it to the heart
    d.ellipse(lung[0], lung[1], 120, 34)
    d.line((150, 140), (128, 104), (120, 82))                        # pulmonary artery, up from the RV
    d.line((280, 82), (272, 104), (250, 140))                        # pulmonary vein, down to the LV
    d.group('mid')
    # the septum's substance, hatched solid
    for y in range(146, 250, 7):
        d.line((188, y), (212, y - 6))
    # the small passages between artery and vein in the lung: a net of branches
    for k in range(6):
        x = 132 + k * 27
        d.line((x, 70), (x + 13, 52), (x + 27, 70))
        d.line((x + 13, 52), (x + 13, 42))
    d.line((120, 82), (132, 70))
    d.line((267, 70), (280, 82))
    _arrow(d, (128, 104), (120, 82))
    _arrow(d, (272, 104), (250, 140))
    # Galen's way through the septum, dashed, and struck out
    for x0 in range(160, 240, 10):
        d.line((x0, 222), (x0 + 5, 222))
    d.lines([[(192, 212), (208, 232)], [(192, 232), (208, 212)]])
    d.group('mid')
    d.text(rv[0] - 8, rv[1] + 3, 'RV', size=7)
    d.text(lv[0] + 8, lv[1] + 3, 'LV', size=7)
    d.text(lung[0], 102, 'LUNG', size=7)
    d.text(200, 258, 'NO PASSAGE', size=7)
    d.text(112, 124, 'ARTERY', size=7, anchor='end')
    d.text(288, 124, 'VEIN', size=7, anchor='start')
    return d


PLATES = {'humours': humours, 'galen': galen, 'ibn-al-nafis': ibn_al_nafis}
