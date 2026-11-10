"""Plates for The Story of Life's part time3 (sprint 055): the Origin's diagram, the Wallace Line
and the Oxford lecture room. See plates_for.py."""
import json
import math
import os
from plates import D
from coastlines import land


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


# --- On the Origin of Species: the diagram facing p. 117 ----------------------------------------

def _gy(level):
    """The y of the horizontal line for `level` thousand generations (0 is the species' row)."""
    return 246 - 15 * level


def origin_of_species():
    d = D()
    # Darwin's one figure (Origin, 1st ed., ch. IV), redrawn and simplified from his text: eleven
    # species A-L of one genus, spaced unequally; fourteen horizontals of a thousand generations
    # each; A gives eight species and I six by the fourteenth, F goes up unchanged, the rest stop
    # short; broken lines below converge on the genus's single parent. The branch positions are
    # ours, following the text's account of which forms branch from which (a10, a5 and m1).
    base = {'A': 70, 'B': 104, 'C': 120, 'D': 138, 'E': 160, 'F': 205,
            'G': 226, 'H': 246, 'I': 285, 'K': 322, 'L': 352}

    def path(*pairs):
        return [(x, _gy(l)) for l, x in pairs]

    # the lines of descent that reach the top, as (level, x) pairs
    lines = [
        path((0, 70), (1, 58), (2, 52), (3, 47), (4, 44), (5, 41), (6, 39), (7, 37), (8, 35),
             (9, 34), (10, 33), (11, 30), (12, 27), (13, 23), (14, 20)),                  # a14
        path((10, 33), (11, 33), (12, 33), (13, 33), (14, 34)),                         # q14
        path((10, 33), (11, 37), (12, 41), (13, 45), (14, 48)),                         # p14
        path((5, 41), (6, 47), (7, 53), (8, 58), (9, 62), (10, 66), (11, 66), (12, 65),
             (13, 64), (14, 63)),                                                        # b14
        path((10, 66), (11, 70), (12, 74), (13, 77), (14, 80)),                         # f14
        path((0, 70), (1, 86), (2, 98), (3, 106), (4, 111), (5, 115), (6, 118), (7, 121),
             (8, 123), (9, 125), (10, 127), (11, 120), (12, 114), (13, 108), (14, 102)),  # o14
        path((10, 127), (11, 126), (12, 124), (13, 121), (14, 118)),                    # e14
        path((10, 127), (11, 129), (12, 131), (13, 133), (14, 135)),                    # m14
        path((0, 205), (14, 205)),                                                       # F14
        path((0, 285), (1, 281), (2, 278), (3, 275), (4, 272), (5, 269), (6, 267), (7, 265),
             (8, 264), (9, 263), (10, 262), (11, 258), (12, 253), (13, 248), (14, 243)),  # n14
        path((10, 262), (11, 261), (12, 260), (13, 259), (14, 258)),                    # r14
        path((10, 262), (11, 265), (12, 268), (13, 271), (14, 273)),                    # w14
        path((2, 278), (3, 285), (4, 292), (5, 298), (6, 303), (7, 307), (8, 311), (9, 314),
             (10, 317), (11, 311), (12, 306), (13, 301), (14, 297)),                     # y14
        path((10, 317), (11, 315), (12, 314), (13, 313), (14, 312)),                    # v14
        path((10, 317), (11, 320), (12, 323), (13, 326), (14, 328)),                    # z14
    ]
    # forms that varied for a while and died out
    dead = [
        path((1, 86), (2, 80), (3, 77)),                                                 # s2
        path((3, 47), (4, 56), (5, 60)),
        path((7, 121), (8, 132), (9, 137)),
        path((4, 272), (5, 262), (6, 258)),
        path((6, 303), (7, 296), (8, 293)),
    ]
    stubs = {'B': 2, 'C': 1, 'D': 2, 'E': 1, 'G': 1, 'H': 2, 'K': 1, 'L': 2}

    d.group('thin')
    for level in range(1, 15):                                                    # the horizontals
        d.line((16, _gy(level)), (372, _gy(level)))
    d.line((16, _gy(0)), (372, _gy(0)))

    d.group()
    for pts in lines:
        d.line(*pts)

    d.group('mid')
    for pts in dead:
        d.dashed(*pts, dash=2.5, gap=2)
    for k, n in stubs.items():                                                    # not prolonged
        d.dashed((base[k], _gy(0)), (base[k], _gy(n)), dash=2.5, gap=2)
    root = (190, 292)                                                             # the one parent
    for x in base.values():
        d.dashed((x, _gy(0) + 17), root, dash=3, gap=2.5)

    d.group('mid')
    nodes = set()
    for pts in lines:
        for p in pts[1:]:
            nodes.add((round(p[0], 1), round(p[1], 1)))
    for x, y in sorted(nodes):
        d.circle(x, y, 1.4)
    d.circle(*root, 2.5)

    d.group('mid')
    for k, x in base.items():
        d.text(x, _gy(0) + 13, k, size=7)
    top = _gy(14) - 6
    for label, x in (('a14', 20), ('m14', 135), ('F14', 205), ('n14', 243), ('z14', 328)):
        d.text(x, top, label, size=7)
    for level, numeral in ((1, 'I'), (5, 'V'), (10, 'X'), (14, 'XIV')):
        d.text(394, _gy(level) + 2.5, numeral, size=7, anchor='end')
    return d


# --- Darwin, Wallace and the 1858 papers: the Wallace Line ------------------------------------

# Coastlines between 110°E and 123°E, 1°S and 10°S, from Natural Earth's 1:50m land (public
# domain), clipped to that box and simplified to 0.04°: the shared region `wallacea` (sprint 055;
# in coastlines.json since sprint 057).
_LAND = land('wallacea')


def _wx(lon):
    return 20 + (lon - 110) * 28


def _wy(lat):
    return 24 + (-1 - lat) * 28


def darwin_wallace():
    d = D()
    # An equirectangular map of Java's east end, Bali, Lombok and Sumbawa, south Borneo and southwest
    # Sulawesi, with Wallace's line as his 1863 map draws it: through the Lombok Strait between Bali
    # and Lombok, then north up the Makassar Strait between Borneo and Sulawesi. The line's course is
    # read off his map, not surveyed. Scale: 28 units a degree.
    d.group('thin')
    for lon in range(111, 123, 2):                                               # graticule
        d.line((_wx(lon), _wy(-1)), (_wx(lon), _wy(-10)))
    for lat in (-2, -4, -6, -8):
        d.line((_wx(110), _wy(lat)), (_wx(123), _wy(lat)))
    _box(d, _wx(110), _wy(-1), 13 * 28, 9 * 28)

    d.group()
    for ring in _LAND:
        d.line(*[(_wx(x), _wy(y)) for x, y in ring], closed=True)

    d.group()
    line = [(115.8, -10), (115.8, -8.85), (115.88, -8.2), (116.6, -6.5), (117.55, -4.9),
            (117.85, -3.4), (118.4, -2.2), (118.75, -1)]
    d.line(*[(_wx(x), _wy(y)) for x, y in line])

    d.group('mid')
    sx, sy = _wx(110.6), _wy(-9.55)                                               # 100 km at 8°S
    d.line((sx, sy), (sx + 25.4, sy))
    d.line((sx, sy - 2.5), (sx, sy + 2.5))
    d.line((sx + 25.4, sy - 2.5), (sx + 25.4, sy + 2.5))

    d.group('mid')
    d.text(_wx(113.6), _wy(-2.4), 'BORNEO', size=7)
    d.text(_wx(121.2), _wy(-3.0), 'SULAWESI', size=7)
    d.text(_wx(111.6), _wy(-7.0), 'JAVA', size=7)
    d.text(_wx(115.15), _wy(-9.25), 'BALI', size=7)
    d.text(_wx(116.35), _wy(-9.25), 'LOMBOK', size=7)
    d.text(_wx(117.05), _wy(-5.55), "WALLACE'S LINE", size=7, anchor='end')
    d.text(_wx(113.3), _wy(-4.6), 'BARBETS · WOODPECKERS', size=7)
    d.text(_wx(120.3), _wy(-6.9), 'COCKATOOS · HONEYEATERS', size=7)
    d.text(sx + 12.7, sy - 5, '100 KM', size=7)
    return d


# --- The Oxford debate: the room ---------------------------------------------------------------

def oxford_1860():
    d = D()
    # The long west room of the Oxford University Museum on 30 June 1860, in plan, as Leonard
    # Huxley described it in 1900 from witnesses: windows down the west side packed with ladies; the
    # platform on the east side between the two doors, Henslow in the center, the Bishop on his
    # right and Draper beyond him, Dingle at the far left with Hooker and Lubbock in front of him,
    # Beale and Huxley nearer the center; the clergy massed in the middle; undergraduates in the
    # northwest corner. Schematic: no dimensions survive in that account; north is up.
    x0, x1, y0, y1 = 110, 270, 28, 272
    door = [(92, 112), (188, 208)]                                        # gaps in the east wall

    d.group('thin')
    for y in range(44, 264, 16):                                         # bench rows
        d.line((x0 + 22, y), (x1 - 46, y))
    d.line((x1 - 22, y0), (x1 - 22, y1))                                 # the platform's edge line
    d.line((40, 60), (40, 30))                                           # north
    _arrow(d, (40, 60), (40, 30), size=5)

    d.group()
    d.line((x1, door[0][0]), (x1, y0), (x0, y0), (x0, y1), (x1, y1), (x1, door[1][1]))
    d.line((x1, door[0][1]), (x1, door[1][0]))
    for y in range(40, 250, 28):                                         # window bays, west wall
        d.line((x0, y), (x0 - 6, y + 4), (x0 - 6, y + 16), (x0, y + 20))
    _box(d, x1 - 22, door[0][1] + 6, 18, door[1][0] - door[0][1] - 12)  # the platform

    d.group('mid')
    seats = {'DRAPER': 124, 'WILBERFORCE': 138, 'HENSLOW': 152, 'DINGLE': 178}
    for name, y in seats.items():
        d.circle(x1 - 13, y, 3)
    for y in (172, 182):                                                 # Hooker and Lubbock, in front
        d.circle(x1 - 30, y, 2.5)
    d.circle(x1 - 34, 158, 2.5)                                          # Beale and Huxley, nearer the center
    d.circle(x1 - 34, 148, 2.5)
    for i in range(5):                                                   # clergy, the middle
        for j in range(5):
            d.circle(160 + i * 12, 118 + j * 12, 1.6)
    for i in range(3):                                                   # undergraduates, NW corner
        for j in range(2):
            d.circle(x0 + 14 + i * 9, y0 + 12 + j * 9, 1.6)
    for y in range(40, 250, 28):                                         # ladies in the windows
        d.circle(x0 - 3, y + 10, 1.4)

    d.group('mid')
    for name, y in seats.items():
        d.line((x1 - 9, y), (x1 + 14, y))
        d.text(x1 + 17, y + 2.5, name, size=7, anchor='start')
    d.line((x1 - 33, 186), (x1 - 40, 214), (x1 + 14, 214))
    d.line((x1 - 38, 153), (x1 - 52, 100), (x1 - 52, 70))
    d.text(x1 - 52, 64, 'BEALE · HUXLEY', size=7)
    d.text(x1 + 17, 216.5, 'HOOKER · LUBBOCK', size=7, anchor='start')
    d.text(184, 186, 'CLERGY', size=7)
    d.text(x0 + 4, y0 - 6, 'UNDERGRADUATES', size=7, anchor='start')
    d.text(x0 - 10, 150, 'WINDOWS · LADIES', size=7, anchor='end')
    d.text(x1 + 6, door[0][0] + 13, 'DOOR', size=7, anchor='start')
    d.text(x1 + 6, door[1][0] + 13, 'DOOR', size=7, anchor='start')
    d.text(40, 72, 'N', size=7)
    d.text(200, 290, 'SECTION D · OXFORD, 30 JUNE 1860 · SCHEMATIC', size=7)
    return d


PLATES = {'origin-of-species': origin_of_species, 'darwin-wallace': darwin_wallace,
          'oxford-1860': oxford_1860}
