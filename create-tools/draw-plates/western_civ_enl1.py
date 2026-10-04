"""Plates for western-civ's part enl1 (sprint 049): locke, encyclopedie, wealth-of-nations. See plates_for.py."""
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


def locke():
    """The Second Treatise's argument as a cycle: power leaves the people only by consent, is held
    by the legislative in trust, and on a breach of trust returns to the people (§§ 4, 27, 95, 149, 222).
    Five stations on a circle, computed; property (lives, liberties, estates) at the center, which
    every station guards."""
    d = D()
    cx, cy, R = 200, 150, 104
    stations = [  # angle (degrees, 0 = east, clockwise on screen), label, section
        (-90, 'STATE OF NATURE', '§ 4'),
        (-18, 'LABOR · PROPERTY', '§ 27'),
        (54, 'CONSENT', '§ 95'),
        (126, 'LEGISLATIVE IN TRUST', '§ 149'),
        (198, 'BREACH OF TRUST', '§ 222'),
    ]
    pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a, _, _ in stations]

    d.group('thin')
    d.circle(cx, cy, R)                                                    # the cycle's circle
    d.circle(cx, cy, R + 16)
    d.line((cx - R - 24, cy), (cx + R + 24, cy))                           # axes
    d.line((cx, cy - R - 24), (cx, cy + R + 24))
    for p in pts:                                                          # radii to each station
        d.line((cx, cy), p)

    d.group()
    d.circle(cx, cy, 34)                                                   # property, at the center
    for (x, y) in pts:
        d.circle(x, y, 9)

    d.group('mid')
    # arcs between stations, each ending in an arrow; the last (breach -> nature) is the return
    for i in range(len(stations)):
        a0 = stations[i][0] + 9
        a1 = stations[(i + 1) % len(stations)][0] - 9
        if a1 <= a0:
            a1 += 360
        d.arc(cx, cy, R, a0, a1, n=24)
        q = (cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1)))
        p = (cx + R * math.cos(math.radians(a1 - 4)), cy + R * math.sin(math.radians(a1 - 4)))
        _arrow(d, p, q)
    # each station guards the center: short ticks inward
    for (x, y) in pts:
        ux, uy = (cx - x) / R, (cy - y) / R
        d.line((x + ux * 13, y + uy * 13), (x + ux * 22, y + uy * 22))

    d.group('mid')
    d.text(cx, cy - 6, 'LIVES', size=7)
    d.text(cx, cy + 3, 'LIBERTIES', size=7)
    d.text(cx, cy + 12, 'ESTATES', size=7)
    offsets = {-90: (0, -26, 'middle'), -18: (14, -4, 'start'), 54: (12, 16, 'start'),
               126: (-12, 16, 'end'), 198: (-14, -4, 'end')}
    for (a, label, sec), (x, y) in zip(stations, pts):
        dx, dy, anc = offsets[a]
        d.text(x + dx, y + dy, label, size=7, anchor=anc)
        d.text(x + dx, y + dy + 9, sec, size=7, anchor=anc)
    d.text(cx, 292, 'SECOND TREATISE · POWER RETURNS TO THE PEOPLE', size=7)
    return d


def encyclopedie():
    """The 'figurative system of human knowledge' of 1751 as a tree, root to the left: the understanding,
    its three faculties and their branches (history, philosophy, poetry), each divided in three, with
    natural history's third part, nature put to use, carried out to the crafts. Laid out level by level."""
    d = D()
    xr, xf, xl, xa = 30, 118, 238, 330                                     # the levels' x
    root = (xr, 150)
    fac = [('MEMORY', 'HISTORY', 62), ('REASON', 'PHILOSOPHY', 150), ('IMAGINATION', 'POETRY', 238)]
    leaves = {
        'MEMORY': ['SACRED', 'CIVIL', 'NATURAL'],
        'REASON': ['OF GOD', 'OF MAN', 'OF NATURE'],
        'IMAGINATION': ['NARRATIVE', 'DRAMATIC', 'PARABOLIC'],
    }
    gap = 24

    d.group('thin')
    for x in (xr, xf, xl, xa):                                              # level guides
        d.line((x, 20), (x, 272))
    for _, _, y in fac:                                                     # each faculty's baseline
        d.line((xr, y), (392, y))
    # the rays from the root to every leaf, as a fan of construction lines
    for _, _, fy in fac:
        for k in (-1, 0, 1):
            d.line(root, (xl, fy + k * gap))

    d.group()
    d.circle(*root, 7)
    for name, branch, fy in fac:
        d.circle(xf, fy, 5)
        # elbow from root to faculty
        mx = (xr + xf) / 2
        d.line((root[0] + 7, root[1]), (mx, root[1]), (mx, fy), (xf - 5, fy))
        for k in (-1, 0, 1):
            ly = fy + k * gap
            mx2 = (xf + xl) / 2
            d.line((xf + 5, fy), (mx2, fy), (mx2, ly), (xl - 4, ly))
            d.circle(xl, ly, 4)

    d.group('mid')
    # natural history -> the uses of nature -> the crafts
    ny = fac[0][2] + gap
    d.line((xl + 44, ny), (xa - 4, ny))
    _arrow(d, (xl + 44, ny), (xa - 4, ny), size=4)
    d.circle(xa, ny, 4)
    d.circle(xa, ny, 7)

    d.group('mid')
    d.text(root[0] - 8, root[1] + 20, 'UNDERSTANDING', size=7, anchor='start')
    for name, branch, fy in fac:
        d.text(xf, fy - 17, name, size=7)
        d.text(xf, fy - 9, branch, size=7)
        for k, leaf in zip((-1, 0, 1), leaves[name]):
            d.text(xl + 8, fy + k * gap + 2.5, leaf, size=7, anchor='start')
    d.text(xa + 11, ny + 2.5, 'CRAFTS', size=7, anchor='start')
    d.text(xa, ny - 11, 'USES', size=7)
    d.text(200, 292, 'SYSTÈME FIGURÉ DES CONNOISSANCES HUMAINES · 1751', size=7)
    return d


def wealth_of_nations():
    """Smith's pin workshop: about eighteen operations shared among ten men (Book I, chapter 1), drawn
    as a row of operations above a row of men, each man taking his share in order (two men one each,
    eight men two each); below, a pin in elevation, its stations marked along it."""
    d = D()
    n_ops, n_men = 18, 10
    x0, x1 = 30, 370
    yo, ym, yp = 52, 128, 214                                               # rows: operations, men, pin
    ox = [x0 + (x1 - x0) * (i + 0.5) / n_ops for i in range(n_ops)]
    mx = [x0 + (x1 - x0) * (j + 0.5) / n_men for j in range(n_men)]
    share = [1, 2, 2, 2, 2, 2, 2, 2, 2, 1]                                  # 18 among 10, in order
    owner = [j for j, s in enumerate(share) for _ in range(s)]

    d.group('thin')
    d.line((x0, yo), (x1, yo))
    d.line((x0, ym), (x1, ym))
    d.line((x0 - 8, yp), (x1 + 8, yp))                                      # the pin's axis
    for x in ox:
        d.line((x, yo + 8), (x, yp - 14))                                   # each operation's station, down to the pin
    for x in (x0, x1):                                                      # the pin's length, dimensioned
        d.line((x, yp + 14), (x, yp + 30))
    d.line((x0, yp + 24), (x1, yp + 24))

    d.group()
    # the pin in elevation: a coiled-wire head at the left, the shank, the ground point at the right
    r = 3.2
    d.line((x0 + 18, yp - r), (x1 - 26, yp - r), (x1, yp), (x1 - 26, yp + r), (x0 + 18, yp + r))
    for k in range(5):                                                      # the head: turns of wire
        cx = x0 + 3 + k * 3.4
        d.ellipse(cx, yp, 2.2, 7.5)

    d.group('mid')
    w = (x1 - x0) / n_ops * 0.7
    for x in ox:                                                            # the operations
        _box(d, x - w / 2, yo - 8, w, 16)
    for x in mx:                                                            # the men
        d.circle(x, ym, 7)
    for i, x in enumerate(ox):                                              # who does which
        j = owner[i]
        d.line((x, yo + 8), (mx[j], ym - 7))

    d.group('mid')
    d.text(200, yo - 16, 'ABOUT EIGHTEEN DISTINCT OPERATIONS', size=7)
    d.text(200, ym + 22, 'TEN MEN · SOME DO TWO OR THREE', size=7)
    for i, lab in ((0, 'DRAW'), (3, 'POINT'), (8, 'HEAD'), (15, 'WHITEN'), (17, 'PAPER')):
        d.text(ox[i], yp - 18, lab, size=7)
    d.text(200, yp + 40, 'ONE PIN · BOOK I, CHAPTER 1', size=7)
    return d


PLATES = {'locke': locke, 'encyclopedie': encyclopedie, 'wealth-of-nations': wealth_of_nations}
