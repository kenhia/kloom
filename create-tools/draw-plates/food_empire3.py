"""Plates for Daily Bread's part empire3 (sprint 051): the Columbian exchange and the sugar boiling house.
See plates_for.py."""
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


def _globe(d, cx, cy, r, tilt=0.35):
    """A globe's graticule: meridians as ellipses every 30 degrees, parallels as chords every 30."""
    for lon in (30, 60):
        rx = r * math.sin(math.radians(lon))
        d.ellipse(cx, cy, rx, r)
    d.line((cx, cy - r), (cx, cy + r))
    for lat in (-60, -30, 0, 30, 60):
        y = cy - r * math.sin(math.radians(lat))
        half = r * math.cos(math.radians(lat))
        d.line((cx - half, y), (cx + half, y))


def _arc(cx, cy, rx, ry, a0, a1, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def columbian_exchange():
    d = D()
    # Two hemispheres as globes with their graticules, the New World left and the Old World right, and the
    # exchange drawn as three arcs between them: crops west to east above, crops and livestock east to west
    # below, and disease, dashed, east to west beneath that. Schematic: no coastlines are drawn.
    r, cy = 60, 150
    west, east = (78, cy), (322, cy)

    d.group('thin')
    _globe(d, *west, r)
    _globe(d, *east, r)
    d.line((10, cy), (390, cy))                                           # the equator carried across

    d.group()
    d.circle(*west, r)
    d.circle(*east, r)

    d.group('mid')
    top = _arc(200, cy - 40, 118, 52, 205, 335)                            # west to east, over the top
    d.line(*top)
    _arrow(d, top[-3], top[-1], size=6)
    low = _arc(200, cy + 40, 118, 42, 25, 155)                             # east to west, underneath
    d.line(*low)
    _arrow(d, low[-3], low[-1], size=6)
    dis = _arc(200, cy + 52, 118, 74, 28, 152)                             # disease, dashed
    d.dashed(*dis, dash=5, gap=4)
    _arrow(d, dis[-3], dis[-1], size=6)

    d.group('mid')
    d.text(200, 50, 'MAIZE · POTATO · CASSAVA · CACAO', size=7)
    d.text(200, 200, 'WHEAT · SUGARCANE · CATTLE', size=7)
    d.text(200, 240, 'SMALLPOX · MEASLES', size=7)
    d.text(west[0] - 14, cy + r + 16, 'THE AMERICAS', size=7)
    d.text(east[0] + 14, cy + r + 16, 'AFRO-EURASIA', size=7)
    d.text(200, 286, 'THE COLUMBIAN EXCHANGE · FROM 1493', size=7)
    return d


def sugar_slavery():
    d = D()
    # The boiling house of a Barbados sugar works in section, after Ligon (1657): cane juice runs from the
    # cistern by a gutter to the clarifying copper, the largest, and is ladled from copper to copper, five in
    # a row, each smaller, to the tache, where it is struck and ladled out to the cooler. Furnaces under the
    # coppers are fed from the fire room below. Skimmings of the three lesser coppers run to the still-house.
    # Proportions are schematic; the order and the diminishing sizes are Ligon's.
    floor, rim = 236, 128
    coppers = [(92, 30), (152, 26), (206, 23), (254, 20), (297, 17)]       # (centre x, radius)

    d.group('thin')
    d.line((20, rim), (380, rim))                                          # the level of the rims
    d.line((20, floor), (380, floor))                                      # the fire-room floor
    for x, rr in coppers:
        d.line((x, rim - rr - 14), (x, floor))                             # each copper's axis

    d.group()
    d.line((62, rim), (62, 196), (330, 196), (330, rim))                   # the masonry frame
    for x, rr in coppers:                                                  # each copper, a bowl in section
        pts = [(x + rr * math.cos(math.radians(a)), rim + rr * 0.9 * math.sin(math.radians(a)))
               for a in range(0, 181, 6)]
        d.line(*pts)
    for x, rr in coppers:                                                  # a furnace arch under each
        d.line(*_arc(x, 196, rr * 0.6, 16, 180, 360, n=16))
    _box(d, 18, 100, 34, 28)                                               # the cistern of cane juice
    _box(d, 344, 112, 40, 16)                                              # the cooler

    d.group('mid')
    d.line((52, 106), (62, 112), (66, rim - 2))                            # gutter, cistern to first copper
    _arrow(d, (62, 112), (66, rim - 2), size=4)
    for (x0, r0), (x1, r1) in zip(coppers, coppers[1:]):                   # ladled from copper to copper
        p, q = (x0 + 6, rim - 8), (x1 - 6, rim - 8)
        mid = ((p[0] + q[0]) / 2, rim - 26)
        pts = [((1 - t) ** 2 * p[0] + 2 * (1 - t) * t * mid[0] + t * t * q[0],
                (1 - t) ** 2 * p[1] + 2 * (1 - t) * t * mid[1] + t * t * q[1]) for t in (i / 12 for i in range(13))]
        d.line(*pts)
        _arrow(d, pts[-2], pts[-1], size=4)
    x5 = coppers[-1][0]
    d.line((x5 + 8, rim - 8), (350, rim - 22), (360, 110))                 # struck sugar to the cooler
    _arrow(d, (350, rim - 22), (360, 110), size=4)
    for x, rr in coppers:                                                  # flames in each furnace
        for k in (-1, 0, 1):
            d.line((x + k * 5, 212), (x + k * 5 + 2, 204), (x + k * 5, 198))
    d.dashed((206, 150), (206, 160), (300, 160), (360, 172), (360, 226), dash=3, gap=3)  # skimmings
    _arrow(d, (360, 216), (360, 226), size=4)

    d.group('mid')
    d.text(35, 92, 'CISTERN', size=7)
    d.text(92, 72, 'CLARIFYING', size=7)
    d.text(92, 82, 'COPPER', size=7)
    d.text(297, 98, 'TACHE', size=7)
    d.text(364, 104, 'COOLER', size=7)
    d.text(196, 252, 'FIRE ROOM', size=7)
    d.text(352, 244, 'TO STILL-HOUSE', size=7)
    d.text(200, 50, 'LADLED FROM COPPER TO COPPER', size=7)
    d.text(200, 286, 'BOILING HOUSE · BARBADOS · AFTER LIGON 1657', size=7)
    return d


PLATES = {'columbian-exchange': columbian_exchange, 'sugar-slavery': sugar_slavery}
