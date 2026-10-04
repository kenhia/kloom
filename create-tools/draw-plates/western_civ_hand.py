"""Plates for western-civ's frames written by hand in sprint 049. See plates_for.py."""
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


def hammurabi():
    d = D()
    # Left: the Louvre stele (Sb 8) in elevation, to scale from the Louvre's record: 225 cm high, 79 cm
    # wide; its girth is 1.65 m at the top and 1.9 m at the foot, so the top is drawn 1.65/1.9 as wide.
    # The relief is 65 x 60 cm. Seven columns near the foot were erased in antiquity.
    # Right: laws 196-199 as a tree of cases, one variable (the victim's rank) changed at each branch.
    s = 240 / 225                                                         # units per centimeter
    cx, top, foot = 92, 30, 270
    wb, wt = 79 * s / 2, 79 * s * 1.65 / 1.9 / 2
    crown = 14                                                            # the rounded head's rise
    ytop = top + crown                                                    # where the sides meet the head

    def half(y):                                                          # half-width at height y
        return wt + (wb - wt) * (y - ytop) / (foot - ytop)

    rel_h, rel_w = 65 * s, 60 * s
    rel_y = ytop + 4
    text_y0 = rel_y + rel_h + 6
    erased_y0 = foot - 50

    d.group('thin')
    d.line((cx, top - 8), (cx, foot + 6))                                 # the axis
    for y in (top, foot):                                                 # height, dimensioned
        d.line((cx - wb - 18, y), (cx - wb - 6, y))
    d.line((cx - wb - 12, top), (cx - wb - 12, foot))
    for m in range(0, 3):                                                 # a scale of meters at the foot
        y = foot - m * 100 * s
        d.line((cx + wb + 6, y), (cx + wb + 12, y))
    d.line((cx + wb + 9, foot), (cx + wb + 9, foot - 200 * s))
    for y in (46, 128, 206):                                              # the tree's ranks, at its margin
        d.line((176, y), (184, y))
    d.line((180, 46), (180, 206))

    d.group()
    # the stele: straight tapering sides and a rounded head
    left = [(cx - half(foot), foot), (cx - half(ytop), ytop)]
    head = [(cx + wt * math.cos(math.radians(a)), ytop - crown * math.sin(math.radians(a)))
            for a in range(180, -1, -6)]
    right = [(cx + half(ytop), ytop), (cx + half(foot), foot)]
    d.line(*left, *head[1:-1], *right, closed=True)

    d.group('mid')
    # the relief panel, with the rod and ring Shamash holds out at its center
    _box(d, cx - rel_w / 2, rel_y, rel_w, rel_h)
    rcx, rcy = cx, rel_y + rel_h * 0.42
    d.circle(rcx, rcy, 6)
    d.line((rcx, rcy + 6), (rcx, rcy + 22))
    # the text in bands, each band divided into the boxes of signs that run down it
    y = text_y0
    while y + 9 < erased_y0:
        w = half(y) - 3
        d.line((cx - w, y), (cx + w, y))
        x = cx + w - 4
        while x > cx - w + 4:
            d.line((x, y + 1.5), (x, y + 7.5))
            x -= 4.6
        y += 10
    w = half(erased_y0) - 3
    d.line((cx - w, erased_y0), (cx + w, erased_y0))
    d.line((cx - w, foot - 6), (cx + w, foot - 6))

    d.group()
    # the tree of laws 196-199
    root = (285, 46)
    leaves = [(215, 128, 'AWĪLUM'), (285, 128, 'MUŠKĒNUM'), (355, 128, 'SLAVE')]
    rulings = [(215, 206, 'HIS EYE'), (285, 206, 'A FINE'), (355, 206, 'HALF HIS PRICE')]
    _box(d, root[0] - 58, root[1] - 14, 116, 28)
    for (x, y, _), (rx, ry, _) in zip(leaves, rulings):
        d.line((root[0], root[1] + 14), (x, y - 12))
        _box(d, x - 30, y - 12, 60, 24)
        d.line((x, y + 12), (rx, ry - 14))
        _arrow(d, (x, y + 12), (rx, ry - 14))

    d.group('mid')
    d.text(root[0], root[1] - 2, 'IF HE PUT OUT', size=7)
    d.text(root[0], root[1] + 8, 'THE EYE OF', size=7)
    for x, y, s_ in leaves:
        d.text(x, y + 3, s_, size=7)
    for x, y, s_ in rulings:
        d.text(x, y + 4, s_, size=7)
    d.text(285, 236, 'LAWS 196 · 198 · 199', size=7)
    d.text(285, 250, 'ONE VARIABLE CHANGED', size=7)
    d.text(cx - wb - 16, (top + foot) / 2, '225', size=7, anchor='end')
    d.text(cx, foot - 22, 'ERASED', size=7)
    d.text(cx + wb + 14, foot - 200 * s - 4, '2 M', size=7, anchor='start')
    d.text(cx, foot + 18, 'STELE · SB 8 · CM', size=7)
    return d


PLATES = {'hammurabi': hammurabi}
