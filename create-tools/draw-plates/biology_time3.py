"""Plates for The Story of Life's part time3 (sprint 055): the Origin's diagram, the Wallace Line
and the Oxford lecture room. See plates_for.py."""
import json
import math
import os
from plates import D


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
# domain), clipped to that box and simplified to 0.04° (sprint 055).
_LAND = [[(122.78, -8.61), (122.47, -8.73), (122.09, -8.74), (121.65, -8.9), (121.58, -8.82), (121.41, -8.81), (121.33, -8.92), (121.04, -8.94), (120.55, -8.8), (120.12, -8.78), (119.91, -8.86), (119.81, -8.7), (119.87, -8.42), (119.96, -8.44), (120.35, -8.26), (120.61, -8.24), (121.44, -8.58), (121.97, -8.46), (122.32, -8.63), (122.43, -8.6), (122.56, -8.43), (122.85, -8.3), (122.92, -8.22), (122.76, -8.19), (122.85, -8.09), (122.98, -8.15), (123, -8.33), (122.81, -8.48), (122.85, -8.56)], [(120.01, -9.37), (120.22, -9.51), (120.29, -9.65), (120.5, -9.67), (120.81, -10), (119.96, -10), (119.6, -9.77), (119.47, -9.76), (119.09, -9.71), (118.96, -9.52), (119.03, -9.44), (119.3, -9.37), (119.8, -9.38), (119.94, -9.3)], [(118.24, -8.32), (118.34, -8.35), (118.49, -8.27), (118.61, -8.28), (118.71, -8.41), (118.75, -8.33), (118.93, -8.3), (119.04, -8.46), (119.1, -8.71), (118.75, -8.74), (118.83, -8.83), (118.43, -8.86), (118.38, -8.67), (118.19, -8.84), (117.39, -9.03), (117.06, -9.1), (116.79, -9.01), (116.84, -8.53), (117.16, -8.37), (117.57, -8.43), (117.81, -8.71), (117.97, -8.73), (118.21, -8.65), (118.23, -8.59), (117.81, -8.34), (117.76, -8.15), (117.92, -8.09), (118.12, -8.12)], [(116.64, -8.61), (116.51, -8.82), (116.59, -8.89), (116.38, -8.93), (116.03, -8.87), (115.86, -8.79), (115.87, -8.74), (116.03, -8.77), (116.08, -8.74), (116.06, -8.44), (116.4, -8.2), (116.72, -8.34)], [(115.45, -8.16), (115.7, -8.41), (115.33, -8.62), (115.22, -8.82), (115.09, -8.83), (115.14, -8.7), (114.95, -8.5), (114.57, -8.35), (114.48, -8.12), (114.94, -8.19), (115.15, -8.07)], [(120.47, -1), (120.67, -1.37), (121.03, -1.41), (121.15, -1.34), (121.38, -1), (122.78, -1), (122.51, -1.35), (122.25, -1.56), (121.86, -1.69), (121.65, -1.9), (121.39, -1.83), (121.35, -1.95), (121.77, -2.24), (122.08, -2.75), (122.29, -2.91), (122.4, -3.2), (122.32, -3.28), (122.25, -3.62), (122.58, -3.88), (122.69, -4.08), (122.85, -4.06), (122.9, -4.35), (122.82, -4.39), (122.72, -4.34), (122.72, -4.41), (122.47, -4.42), (122.11, -4.54), (122.04, -4.83), (121.75, -4.82), (121.51, -4.68), (121.49, -4.58), (121.62, -4.09), (121.42, -3.98), (120.89, -3.52), (121.05, -3.17), (121.05, -2.75), (120.99, -2.67), (120.65, -2.67), (120.34, -2.87), (120.25, -3.05), (120.39, -3.35), (120.44, -3.71), (120.36, -4.09), (120.42, -4.62), (120.28, -5.15), (120.43, -5.59), (120.31, -5.54), (119.95, -5.58), (119.72, -5.69), (119.38, -5.42), (119.36, -5.31), (119.59, -4.52), (119.62, -4.03), (119.48, -3.73), (119.47, -3.51), (119.36, -3.46), (118.99, -3.54), (118.87, -3.4), (118.81, -3.16), (118.86, -2.93), (118.78, -2.72), (119.09, -2.48), (119.17, -2.14), (119.32, -1.93), (119.31, -1.41), (119.47, -1)], [(110, -6.91), (110.43, -6.95), (110.58, -6.81), (110.74, -6.47), (110.97, -6.44), (111.18, -6.69), (111.54, -6.65), (112.09, -6.89), (112.54, -6.93), (112.65, -7.22), (112.79, -7.3), (112.79, -7.55), (113.25, -7.72), (114.07, -7.63), (114.38, -7.77), (114.44, -7.9), (114.39, -8.41), (114.48, -8.6), (114.6, -8.68), (114.58, -8.77), (114.28, -8.61), (113.94, -8.57), (113.25, -8.29), (112.68, -8.41), (111.51, -8.31), (110.61, -8.15), (110, -7.88)], [(117.16, -1), (116.91, -1.22), (116.8, -1.18), (116.74, -1.04), (116.75, -1.33), (116.28, -1.78), (116.42, -1.78), (116.42, -2.05), (116.31, -2.14), (116.53, -2.21), (116.55, -2.41), (116.53, -2.51), (116.32, -2.55), (116.31, -2.6), (116.38, -2.58), (116.33, -2.9), (116.15, -2.98), (116.26, -3.13), (116.06, -3.35), (115.96, -3.6), (114.69, -4.17), (114.63, -4.11), (114.53, -3.38), (114.45, -3.48), (114.3, -3.36), (114.34, -3.24), (114.24, -3.36), (114.08, -3.28), (113.96, -3.39), (113.71, -3.46), (113.63, -3.42), (113.61, -3.2), (113.34, -3.25), (113.03, -2.93), (112.97, -3.19), (112.76, -3.32), (112.6, -3.4), (112.28, -3.32), (111.86, -3.55), (111.82, -3.06), (111.69, -2.89), (111.63, -2.98), (111.37, -2.93), (110.93, -3.07), (110.83, -3.0), (110.9, -2.91), (110.7, -3.02), (110.57, -2.89), (110.26, -2.97), (110.1, -2.0), (110, -1.89), (110.0, -1)], [(113.84, -7.11), (113.66, -7.11), (113.47, -7.22), (113.13, -7.22), (112.76, -7.14), (112.73, -7.07), (112.87, -6.9), (113.07, -6.88), (113.97, -6.87), (114.08, -6.99)], [(123, -4.94), (123, -5.4), (122.81, -5.67), (122.65, -5.66), (122.59, -5.49), (122.77, -5.21), (122.85, -4.62), (123, -4.41)], [(122.65, -5.27), (122.56, -5.39), (122.39, -5.34), (122.31, -5.38), (122.33, -5.14), (122.4, -5.07), (122.33, -4.85), (122.37, -4.77), (122.7, -4.62), (122.76, -4.93), (122.61, -5.14)], [(122.04, -5.44), (121.98, -5.46), (121.81, -5.26), (121.87, -5.1), (121.97, -5.08), (122.04, -5.16)], [(123, -1.49), (122.89, -1.59), (122.81, -1.43), (122.91, -1.18), (123, -1.18)], [(120.53, -6.3), (120.49, -6.46), (120.45, -6.09), (120.48, -5.78), (120.53, -5.9)], [(119.46, -8.74), (119.39, -8.74), (119.38, -8.59), (119.45, -8.43), (119.48, -8.47), (119.55, -8.48), (119.56, -8.55), (119.44, -8.67)], [(119.07, -8.24), (119.02, -8.2), (119.1, -8.14), (119.13, -8.2)], [(115.61, -8.77), (115.58, -8.8), (115.48, -8.72), (115.54, -8.68)], [(115.38, -6.97), (115.3, -6.99), (115.22, -6.91), (115.41, -6.84), (115.55, -6.94)], [(112.72, -5.81), (112.6, -5.84), (112.65, -5.73), (112.73, -5.75)], [(116.42, -3.46), (116.39, -3.64), (116.33, -3.54), (116.4, -3.42)], [(116.3, -3.87), (116.09, -4.05), (116.02, -3.7), (116.12, -3.34), (116.27, -3.25)], [(120.77, -7.12), (120.64, -7.12), (120.63, -7.02), (120.78, -7.06)], [(122.98, -8.55), (122.89, -8.59), (122.93, -8.5), (123, -8.45)], [(117.56, -8.37), (117.49, -8.35), (117.49, -8.18), (117.67, -8.15)]]


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
