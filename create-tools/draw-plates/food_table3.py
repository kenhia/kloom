"""Plates for Daily Bread's part table3 (sprint 051): julia-child, ultra-processed. See plates_for.py."""
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


def julia_child():
    d = D()
    # Left: a page of Mastering the Art of French Cooking as a schematic, not the book's text. A master recipe's
    # heading, then steps in two columns: each step's ingredients and its pan on the left, the paragraph of
    # instruction on the right, ruled so that one step reads across in "one sweep of the eye" (the foreword).
    # Right: the book's plan of themes and variations, a master recipe branching into variations that each
    # change one ingredient or step. The counts of steps and variations are illustrative.
    px0, px1, py0, py1 = 24, 214, 44, 266                                   # the page
    split = px0 + (px1 - px0) * 0.36                                        # the column rule
    steps = [(78, 38), (116, 52), (168, 34), (202, 50)]                     # (top, height) of each step

    d.group('thin')
    for x in (px0 + 10, split, px1 - 10):                                   # margins and the column rule
        d.line((x, py0 + 6), (x, py1 - 6))
    for top, h in steps:                                                    # each step's rule
        d.line((px0 + 4, top), (px1 - 4, top))
    tx0, tx1 = 256, 380                                                     # the tree's frame
    d.line((tx0 - 8, 58), (tx1 + 8, 58))
    d.line((tx0 - 8, 150), (tx1 + 8, 150))

    d.group()
    _box(d, px0, py0, px1 - px0, py1 - py0)                                 # the page
    d.line((px0 + 10, 56), (px1 - 60, 56))                                  # master recipe's heading
    d.line((px0 + 10, 64), (px1 - 100, 64))
    # the tree: master and four variations
    mx, my = (tx0 + tx1) / 2, 92
    _box(d, mx - 44, my - 16, 88, 32)
    vx = [tx0 + i * (tx1 - tx0) / 3 for i in range(4)]
    for x in vx:
        _box(d, x - 14, 196, 28, 40)

    d.group('mid')
    for top, h in steps:
        n = max(2, int(h / 12))
        for i in range(n):                                                  # ingredients, short lines
            y = top + 10 + i * 9
            d.line((px0 + 14, y), (px0 + 14 + 22 + (i * 7) % 18, y))
        for i in range(int((h - 8) / 7)):                                   # instructions, a paragraph
            y = top + 9 + i * 7
            end = px1 - 14 if i < int((h - 8) / 7) - 1 else split + 50
            d.line((split + 6, y), (end, y))
    for top, h in steps[1::2]:                                              # a pan beside two of the steps
        d.ellipse(px0 + 28, top + h - 8, 12, 3)
        d.line((px0 + 40, top + h - 8), (px0 + 52, top + h - 10))
    for x in vx:                                                            # branches
        d.line((mx, my + 16), (mx, 150), (x, 172), (x, 196))
        _arrow(d, (x, 172), (x, 196))
    for x in vx:                                                            # inside each variation, the
        for i in range(3):                                                  # master's lines, one changed
            y = 206 + i * 9
            d.line((x - 8, y), (x + 8, y))
        d.circle(x + 8, 215, 2.2)

    d.group('mid')
    yb = steps[1][0] + 19                                                   # the eye's sweep across one step
    d.dashed((px0 + 12, yb + 6), (px1 - 12, yb + 6), dash=3, gap=3)
    _arrow(d, (px1 - 30, yb + 6), (px1 - 12, yb + 6), size=4)

    d.group('mid')
    d.text((px0 + split) / 2, 36, 'WHAT', size=7)
    d.text((split + px1) / 2, 36, 'HOW', size=7)
    d.text((px0 + px1) / 2, 282, 'ONE STEP, READ ACROSS', size=7)
    d.text(mx, my + 3, 'MASTER RECIPE', size=7)
    d.text(mx, 50, 'THEME', size=7)
    d.text(mx, 254, 'VARIATIONS', size=7)
    d.text(mx, 268, 'EACH CHANGES ONE THING', size=7)
    return d


def ultra_processed():
    d = D()
    # The four Nova groups as a flow, after Monteiro et al. (2019): group 1 foods; group 2 substances pressed,
    # refined or milled from them (or mined); group 3, group 1 foods with group 2 added and canned, bottled or
    # fermented; group 4, whole foods fractioned into substances, some chemically modified, assembled with
    # additives by extrusion, molding or pre-frying, and packaged. Positions are schematic.
    cx = [58, 150, 250, 342]                                                # column centers
    top, bot = 70, 200

    d.group('thin')
    for x in cx:                                                            # column centers, above and below
        d.line((x, 64), (x, 78))
        d.line((x, 236), (x, 258))
    d.line((20, top - 16), (380, top - 16))
    d.line((20, bot + 30), (380, bot + 30))

    d.group()
    # group 1: a whole plant, a grain of wheat drawn as an ellipse with its crease
    d.ellipse(cx[0], 110, 16, 26)
    d.line((cx[0], 88), (cx[0], 132))
    # group 2: a bottle of oil and a heap of salt
    b = cx[1]
    d.line((b - 6, 92), (b - 6, 84), (b + 6, 84), (b + 6, 92), (b + 14, 104), (b + 14, 140), (b - 14, 140), (b - 14, 104), closed=True)
    # group 3: a can, with the grain and the bottle's contents
    c = cx[2]
    d.ellipse(c, 92, 20, 6)
    d.line((c - 20, 92), (c - 20, 138))
    d.line((c + 20, 92), (c + 20, 138))
    d.arc(c, 138, 20, 0, 180, ry=6)
    # group 4: a sealed packet
    p = cx[3]
    d.line((p - 22, 86), (p + 22, 86), (p + 22, 140), (p - 22, 140), closed=True)
    for x in range(int(p - 22), int(p + 23), 4):                            # crimped seals
        d.line((x, 86), (x + 2, 82), (x + 4, 86))
        d.line((x, 140), (x + 2, 144), (x + 4, 140))

    d.group('mid')
    # flows: 1 -> 2 (pressed, refined), 1 + 2 -> 3, 1 -> fractions -> 4
    _arrowline = [((cx[0] + 20, 104), (cx[1] - 18, 104)), ((cx[1] + 18, 116), (cx[2] - 24, 116))]
    for p0, p1 in _arrowline:
        d.line(p0, p1)
        _arrow(d, p0, p1)
    d.line((cx[0], 136), (cx[0], 176), (cx[2] - 6, 176), (cx[2] - 6, 148))
    _arrow(d, (cx[2] - 6, 176), (cx[2] - 6, 148))
    # fractions for group 4: whole food split into substances, then assembled
    fy = 214
    d.line((cx[0], 176), (cx[0], fy))
    for i, x in enumerate((180, 214, 248, 282)):
        d.circle(x, fy, 5 + (i % 2))
    d.line((cx[0], fy), (172, fy))
    d.line((288, fy), (p, fy), (p, 148))
    _arrow(d, (p, fy), (p, 148))
    d.dashed((300, 166), (318, 156), dash=2, gap=2)
    d.dashed((376, 166), (362, 156), dash=2, gap=2)
    d.circle(304, 170, 3)
    d.circle(372, 170, 3)

    d.group('mid')
    for i, (x, s) in enumerate(zip(cx, ('1 WHOLE', '2 CULINARY', '3 PROCESSED', '4 ULTRA-'))):
        d.text(x, 48, s, size=7)
    d.text(cx[0] - 6, 160, 'FOOD', size=7, anchor='end')
    d.text(cx[1], 160, 'OIL · SALT', size=7)
    d.text(cx[2] + 2, 160, 'CANNED', size=7, anchor='start')
    d.text(cx[3], 60, 'PROCESSED', size=7)
    d.text((cx[0] + cx[1]) / 2, 98, 'PRESS', size=7)
    d.text(231, 200, 'FRACTIONED SUBSTANCES', size=7)
    d.text(340, 186, 'ADDITIVES', size=7)
    d.text(200, 282, 'NOVA · BY THE EXTENT AND PURPOSE OF PROCESSING', size=7)
    return d


PLATES = {
    'julia-child': julia_child,
    'ultra-processed': ultra_processed,
}
