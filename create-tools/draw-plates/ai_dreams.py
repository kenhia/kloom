"""ai plates, segment "Dreams of thinking machines" (sprint 006). See ai.py."""
import math

from plates import D


def talos():
    """A bronze man on an eight-head canon, his one vein, and the nail that stops it."""
    d = D()
    cx, top, head = 130, 30, 30  # eight heads of 30: 30..270
    # construction: the canon's head-lines and the axis
    d.group('thin')
    d.lines([[(cx - 70, top + i * head), (cx + 70, top + i * head)] for i in range(9)])
    d.line((cx, top - 8), (cx, top + 8 * head + 6))
    for i in range(1, 9):
        d.text(cx - 80, top + i * head + 3, str(i), size=7, anchor='end')
    # the figure, drawn as a draughtsman's mannequin
    d.group()
    d.circle(cx, top + head / 2, head / 2 - 1)
    neck, sh, hip, knee, ank = top + head, top + 1.5 * head, top + 4 * head, top + 6 * head, top + 7.8 * head
    d.line((cx - 6, neck), (cx - 6, neck + 8), (cx - 34, sh), (cx - 24, hip), (cx - 28, hip + 10))
    d.line((cx + 6, neck), (cx + 6, neck + 8), (cx + 34, sh), (cx + 24, hip), (cx + 28, hip + 10))
    d.line((cx - 28, hip + 10), (cx - 20, knee), (cx - 18, ank), (cx - 30, ank + 10), (cx - 10, ank + 10), (cx - 8, ank))
    d.line((cx + 28, hip + 10), (cx + 20, knee), (cx + 18, ank), (cx + 30, ank + 10), (cx + 10, ank + 10), (cx + 8, ank))
    d.line((cx - 8, ank), (cx - 4, knee), (cx, hip + 16), (cx + 4, knee), (cx + 8, ank))
    # arms: one down, one raised with a stone
    d.line((cx - 34, sh), (cx - 46, top + 3 * head), (cx - 50, hip + 6))
    d.line((cx + 34, sh), (cx + 58, top + 1.2 * head), (cx + 66, top + 0.2 * head))
    d.circle(cx + 70, top - 4, 9)
    # the one vein, neck to ankle
    d.group('mid')
    d.curve(f'M{cx - 2} {neck + 6} C{cx - 10} {sh + 20} {cx - 14} {hip - 20} {cx - 16} {hip + 20} '
            f'S{cx - 18} {knee + 20} {cx - 14} {ank - 4}')
    # the inset: the ankle, magnified
    ix, iy, ir = 300, 196, 58
    d.group('thin')
    d.line((cx - 14, ank - 4), (ix - ir * math.cos(math.radians(35)), iy + ir * math.sin(math.radians(35))))
    d.circle(cx - 14, ank - 4, 7)
    d.group()
    d.circle(ix, iy, ir)
    d.curve(f'M{ix - 50} {iy - 30} C{ix - 20} {iy - 26} {ix - 8} {iy - 12} {ix + 2} {iy + 4}')
    d.curve(f'M{ix - 52} {iy - 18} C{ix - 24} {iy - 14} {ix - 16} {iy - 2} {ix - 8} {iy + 12}')
    d.group('mid')
    # the nail: head and shaft, stopping the vein
    d.line((ix - 3, iy + 8), (ix + 30, iy + 34))
    d.line((ix + 24, iy + 38), (ix + 36, iy + 30))
    d.circle(ix - 3, iy + 8, 6)
    # the circuit of Crete: three loops of one route
    d.group('thin')
    for k, (rx, ry) in enumerate([(62, 26), (54, 21), (46, 16)]):
        d.ellipse(300, 70, rx, ry)
    d.group()
    d.curve('M362 70 l-5 -6 M362 70 l5 -6')
    d.group()
    d.text(300, 74, '×3', size=10)
    d.text(ix, iy + ir + 14, 'ICHOR · NAIL', size=8)
    d.text(300, 30, 'CIRCUIT OF CRETE', size=8)
    return d


def leibniz():
    """Llull's wheel of nine letters with every pairing drawn, beside Leibniz's stepped drum."""
    d = D()
    cx, cy, r = 150, 150, 104
    letters = 'BCDEFGHIK'
    pts = [(cx + r * math.sin(2 * math.pi * i / 9), cy - r * math.cos(2 * math.pi * i / 9)) for i in range(9)]
    # construction: the concentric rings of a Lullian figure
    d.group('thin')
    d.circle(cx, cy, r + 26)
    d.circle(cx, cy, r + 12)
    d.lines([[(cx + (r + 12) * math.sin(2 * math.pi * (i + .5) / 9), cy - (r + 12) * math.cos(2 * math.pi * (i + .5) / 9)),
              (cx + (r + 26) * math.sin(2 * math.pi * (i + .5) / 9), cy - (r + 26) * math.cos(2 * math.pi * (i + .5) / 9))]
             for i in range(9)])
    # the object: every pair of the nine principles joined (36 chords)
    d.group('mid')
    d.lines([[pts[i], pts[j]] for i in range(9) for j in range(i + 1, 9)])
    d.group()
    d.circle(cx, cy, r)
    for x, y in pts:
        d.circle(x, y, 7)
    # Leibniz's stepped drum: nine teeth of increasing length, and the gear it drives
    x0, y0, w, h = 290, 70, 74, 150
    d.group('thin')
    d.line((x0 + w / 2, y0 - 18), (x0 + w / 2, y0 + h + 18))
    d.group()
    d.line((x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), closed=True)
    d.group('mid')
    for i in range(9):
        length = h * (i + 1) / 9
        x = x0 + 5 + i * (w - 10) / 8
        d.line((x, y0 + h), (x, y0 + h - length))
    d.group()
    d.circle(x0 + w / 2, y0 - 34, 16)
    d.lines([[(x0 + w / 2 + 16 * math.cos(math.radians(a)), y0 - 34 + 16 * math.sin(math.radians(a))),
              (x0 + w / 2 + 21 * math.cos(math.radians(a)), y0 - 34 + 21 * math.sin(math.radians(a)))]
             for a in range(0, 360, 36)])
    d.group()
    for (x, y), ch in zip(pts, letters):
        d.text(x, y + 3, ch, size=8)
    d.text(cx, cy + r + 44, 'ARS BREVIS · 9 PRINCIPLES · 36 PAIRS', size=8)
    d.text(x0 + w / 2, y0 + h + 34, 'STAFFELWALZE', size=8)
    return d


PLATES = {'talos': talos, 'leibniz': leibniz}
