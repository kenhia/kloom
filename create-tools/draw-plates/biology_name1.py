"""Plates for The Story of Life, part name1 (gesner, cabinet), sprint 055. See plates_for.py."""
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


def gesner():
    d = D()
    # One animal's history in the Historiae animalium (1551), as Gessner's preface ("Ordinis ratio")
    # lays it out: eight chapters lettered A to H in a fixed order, the woodcut at the head, the last
    # chapter (philology) cut again into parts a to h. A single page stands for a history that often ran
    # to many; the chapters' lengths are schematic.
    px0, px1, py0, py1 = 40, 196, 24, 272
    cut = (54, 46, 128, 60)                                               # the woodcut's frame: x, y, w, h
    col0, col1 = 58, 188
    ly0, step = 124, 5.5
    blocks = [('A', 2), ('B', 4), ('C', 4), ('D', 2), ('E', 3), ('F', 2), ('G', 2), ('H', 2)]
    names = ['NAMES', 'REGION · BODY', 'ACTIONS OF THE BODY', 'MIND · CHARACTER', 'USES TO PEOPLE',
             'AS FOOD', 'AS REMEDY', 'PHILOLOGY']
    rows, y = [], ly0
    for letter, n in blocks:
        rows.append((letter, y, y + (n - 1) * step))
        y += n * step + 4
    ys = [y0 + (y1 - y0) / 2 for _, y0, y1 in rows]
    lx = 236
    lys = [ly0 + 2 + i * 17 for i in range(len(rows))]

    d.group('thin')
    d.line((px0 - 6, py0), (px0 - 6, py1))                                # the page's height
    d.line((px0 - 10, py0), (px0 - 2, py0))
    d.line((px0 - 10, py1), (px0 - 2, py1))
    x, y, w, h = cut                                                      # the woodcut's construction
    d.line((x, y), (x + w, y + h))
    d.line((x + w, y), (x, y + h))
    d.line((x + w / 2, y - 4), (x + w / 2, y + h + 4))
    for (_, y0, y1), m, ly in zip(rows, ys, lys):                         # leaders to the headings
        d.line((col1 + 4, m), (lx - 8, ly - 2.5))

    d.group()
    _box(d, px0, py0, px1 - px0, py1 - py0)                               # the folio page
    _box(d, *cut)
    d.line((col0, 38), (col1, 38))                                        # the running head's rule

    d.group('mid')
    for letter, y0, y1 in rows:                                           # the text, chapter by chapter
        yy = y0
        first = True
        while yy <= y1 + 0.1:
            d.line((col0 + (8 if first else 0), yy), (col1 - (18 if yy == y1 else 0), yy))
            first = False
            yy += step
    for _, y0, y1 in rows:                                                # brackets in the margin
        d.line((col1 + 2, y0), (col1 + 4, y0), (col1 + 4, y1), (col1 + 2, y1))
    hx = lx
    hy = lys[-1] + 10                                                     # H's own parts, a to h
    for k in range(8):
        _box(d, hx + k * 16, hy, 13, 9)

    d.group('mid')
    d.text((col0 + col1) / 2, 35, 'DE RHINOCEROTE. A. LIB. I.', size=7)
    d.text(x + w / 2, y + h + 13, 'WOODCUT', size=7)
    for (letter, y0, _), ly, name in zip(rows, lys, names):
        d.text(col0 - 6, y0 + 2.5, letter, size=7)
        d.text(lx, ly, letter, size=7, anchor='start')
        d.text(lx + 12, ly, name, size=7, anchor='start')
    for k, ch in enumerate('abcdefgh'):
        d.text(hx + k * 16 + 6.5, hy + 7, ch, size=7)
    d.text(lx, 48, 'ONE ANIMAL,', size=7, anchor='start')
    d.text(lx, 60, 'EIGHT CHAPTERS', size=7, anchor='start')
    d.text(lx, 84, 'LETTERS, NOT NUMBERS:', size=7, anchor='start')
    d.text(lx, 96, 'A MISSING CHAPTER', size=7, anchor='start')
    d.text(lx, 108, 'LEAVES A GAP', size=7, anchor='start')
    d.text(200, 290, 'HISTORIAE ANIMALIUM · ZURICH, 1551 · SCHEMATIC', size=7)
    return d


def cabinet():
    d = D()
    # A narwhal's skull in plan, snout to the right, with the tusk set in its socket in the left side of
    # the upper jaw, as Ole Worm measured one in 1636 (Museum Wormianum, 1655: skull two Roman feet long and
    # one and a half wide, socket one foot four inches deep), and the tusk eight feet long with "about
    # seven Rounds" of spiral furrow, as Nehemiah Grew measured the Royal Society's (1681). Two specimens
    # combined at one scale, 36 units to the foot; the tusk's width is drawn twice true.
    ft = 36
    cy = 136
    sx0 = 22                                                              # back of the skull
    sx1 = sx0 + 2 * ft                                                    # tip of the snout
    ty = cy - 9                                                           # the tusk's axis, on the left
    tx1 = sx1 + 8 * ft - 6                                                # the tusk's tip
    tl = tx1 - sx1
    r0, r1 = 7.0, 1.2                                                     # half-widths at base and tip, x2

    def half(x):
        """The skull's half-width at x, from the occiput to the snout."""
        t = (x - sx0) / (sx1 - sx0)
        if t < 0.3:
            return 20 + 7 * math.sin(math.pi / 2 * t / 0.3)
        return 27 - 18 * ((t - 0.3) / 0.7) ** 0.8

    def tr(x):
        return r0 + (r1 - r0) * (x - sx1) / tl

    d.group('thin')
    d.line((sx0 - 8, cy), (tx1 + 6, cy))                                  # the skull's midline
    d.line((sx1 - 1.33 * ft, ty), (tx1 + 6, ty))                          # the tusk's axis
    for x in (sx0, sx1, tx1):
        d.line((x, 186), (x, 196))
    d.line((sx0, 191), (sx1, 191))
    d.line((sx1, 191), (tx1, 191))
    for k in range(11):                                                   # a scale in feet
        x = sx0 + k * ft
        d.line((x, 236), (x, 240 if k % 2 else 243))
    d.line((sx0, 236), (sx0 + 10 * ft, 236))

    d.group()
    n = 40
    up = [(sx0 + (sx1 - sx0) * k / n, cy - half(sx0 + (sx1 - sx0) * k / n)) for k in range(n + 1)]
    dn = [(x, 2 * cy - y) for x, y in reversed(up)]
    d.line(*up, *dn, closed=True)                                         # the skull's outline
    m = 60
    top = [(sx1 + tl * k / m, ty - tr(sx1 + tl * k / m)) for k in range(m + 1)]
    bot = [(x, 2 * ty - y) for x, y in reversed(top)]
    d.line(*top, (tx1 + 3, ty), *bot, closed=True)                        # the tusk

    d.group('mid')
    for sgn in (-1, 1):                                                   # the blowhole and the orbits
        d.ellipse(sx0 + 12, cy + sgn * 4, 3, 2.2)
        d.ellipse(sx0 + 24, cy + sgn * 19, 6, 4)
    d.dashed((sx1 - 1.33 * ft, ty - r0), (sx1, ty - r0), dash=3, gap=2)  # the socket, inside the jaw
    d.dashed((sx1 - 1.33 * ft, ty + r0), (sx1, ty + r0), dash=3, gap=2)
    d.dashed((sx1 - 1.33 * ft, ty - r0), (sx1 - 1.33 * ft, ty + r0), dash=2, gap=2)
    turns = 7                                                             # spiral furrows, three starts
    for start in range(3):
        pts = []
        steps = 420
        for k in range(steps + 1):
            x = sx1 + tl * k / steps
            th = 2 * math.pi * (turns * (x - sx1) / tl + start / 3)
            if math.sin(th) > 0:                                          # the near face only
                pts.append((x, ty - tr(x) * math.cos(th)))
            elif pts:
                if len(pts) > 1:
                    d.line(*pts)
                pts = []
        if len(pts) > 1:
            d.line(*pts)

    d.group('mid')
    d.text((sx0 + sx1) / 2, 206, 'SKULL 2 FT', size=7)
    d.text((sx1 + tx1) / 2, 206, 'TUSK 8 FT · ABOUT 7 TURNS', size=7)
    d.text(sx1 + 14, ty - 16, 'SOCKET, DASHED: 1 FT 4 IN DEEP', size=7, anchor='start')
    d.text(sx1 + 14, cy + 20, 'TUSK FROM THE LEFT SIDE OF THE UPPER JAW', size=7, anchor='start')
    d.text(sx0, cy + 42, 'NO SOCKET ON THE RIGHT', size=7, anchor='start')
    for k in (0, 2, 4, 6, 8, 10):
        d.text(sx0 + k * ft, 253, f'{k}', size=7)
    d.text(sx0 + 10 * ft + 4, 239, 'FT', size=7, anchor='start')
    d.text(200, 48, 'NOT A HORN BUT A TOOTH', size=7)
    d.text(200, 60, 'WORM 1636 · GREW 1681', size=7)
    d.text(200, 286, 'A NARWHAL SKULL IN PLAN · TUSK WIDTH DRAWN 2x · SCHEMATIC', size=7)
    return d


PLATES = {'gesner': gesner, 'cabinet': cabinet}
