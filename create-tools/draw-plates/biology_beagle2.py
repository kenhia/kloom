"""Plates for The Story of Life's part beagle2 (sprint 055): coral-reefs, notebook-b. See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def coral_reefs():
    d = D()
    # Darwin's subsidence theory (Coral Reefs, 1842, ch. V, woodcuts 4 and 5) as three sections of one
    # island: a volcano drawn as a Gaussian profile, sinking 0, 30 and 62 units while the reef, which
    # can live only near the surface, grows straight up from where it first took hold. Vertical scale
    # much exaggerated, as Darwin's own woodcuts were. Panel 3 adds the 1952 drill hole to basalt.
    sea, floor = 112, 248
    peak = 46                       # first height of the summit above the sea
    w = 40                          # the volcano's width parameter
    h0 = floor - sea + peak         # the volcano's height above the floor
    cxs, sinks = [70, 200, 330], [0, 30, 62]
    r_out = 30                      # the outer edge of the first, fringing reef, from the axis
    r_in = w * math.sqrt(math.log(h0 / (floor - sea)))                     # the first shoreline

    def ground(cx, x, s):
        return floor - h0 * math.exp(-((x - cx) / w) ** 2) + s

    def profile(cx, s, half=60):
        pts = [(cx + k / 2, ground(cx, cx + k / 2, s)) for k in range(-2 * half, 2 * half + 1, 3)]
        return [p for p in pts if p[1] <= floor + 0.01]

    def reef(cx, side, s):
        # top at the sea from the first shoreline out to the reef's edge, its foot on the sunken slope
        xs = [cx + side * (r_in + (r_out - r_in) * k / 8) for k in range(9)]
        foot = [(x, ground(cx, x, s)) for x in reversed(xs)]
        return [(xs[0], sea), (xs[-1], sea)] + foot

    d.group('thin')
    d.line((14, sea), (390, sea))                                          # sea level
    d.line((14, floor), (390, floor))                                      # sea floor
    for x in (135, 265):
        d.line((x, 40), (x, floor))
    for cx in cxs[1:]:                                                     # where the island stood
        d.dashed(*profile(cx, 0), dash=3, gap=3)
    for cx in cxs:
        d.line((cx, 52), (cx, floor))                                      # each island's axis

    d.group()
    for cx, s in zip(cxs, sinks):
        d.line(*profile(cx, s))
        for side in (-1, 1):
            d.line(*reef(cx, side, s), closed=True)

    d.group('mid')
    for cx, s in zip(cxs, sinks):
        for side in (-1, 1):                                               # growth lines in each reef
            for k in range(1, 20):
                y = sea + 6 * k
                xa, xb = cx + side * r_in, cx + side * r_out
                if y >= ground(cx, xb, s) - 1:
                    break
                xin = xa
                while side * (xin - xb) < 0 and ground(cx, xin, s) < y:
                    xin += side * 0.5
                d.line((xin, y), (xb, y))
    for cx, s in zip(cxs[1:], sinks[1:]):                                  # sinking, and growing
        d.line((cx - 44, 60), (cx - 44, 60 + s * 0.6))
        _arrow(d, (cx - 44, 60), (cx - 44, 60 + s * 0.6), size=4)
    hole = cxs[2] + (r_in + r_out) / 2                                     # the 1952 drill hole
    d.dashed((hole, sea - 10), (hole, ground(cxs[2], hole, sinks[2]) + 10), dash=2, gap=2)

    d.group('mid')
    for cx, n in zip(cxs, ('FRINGING', 'BARRIER', 'ATOLL')):
        d.text(cx, 30, n, size=7)
    d.text(18, sea - 4, 'SEA LEVEL', size=7, anchor='start')
    d.text(cxs[2] - 6, sea - 5, 'LAGOON', size=7)
    d.text(hole - 12, sea - 26, 'DRILL, 1952', size=7, anchor='start')
    d.text(cxs[1] - 44, 48, 'SINKS', size=7)
    d.text(200, 272, 'ONE ISLAND SINKING, ITS REEF GROWING UP · AFTER DARWIN, 1842', size=7)
    d.text(200, 284, 'VERTICAL SCALE EXAGGERATED', size=7)
    return d


# The "I think" tree, Notebook B p. 36 (July 1837), redrawn as a schematic: the branching is read off the
# sketch and simplified, the lengths are not Darwin's. Nodes, then branches; a tip is (point, living),
# living tips carry Darwin's short crossbar, and the others are lines that died out.
_NODES = {
    'root': (128, 250), 'n1': (140, 202), 'n2': (138, 128), 'n3': (198, 188), 'n4': (226, 206),
    'n5': (244, 230), 'n6': (134, 92), 'n7': (102, 136), 'n8': (186, 148), 'n9': (176, 108),
}
_EDGES = [('root', 'n1'), ('n1', 'n2'), ('n1', 'n3'), ('n3', 'n4'), ('n4', 'n5'), ('n2', 'n6'),
          ('n2', 'n7'), ('n2', 'n8'), ('n6', 'n9')]
_TIPS = [
    ('n5', (232, 262), True), ('n5', (252, 260), True), ('n5', (276, 248), True),        # A's group
    ('n4', (262, 196), False), ('n3', (214, 168), False), ('n3', (238, 176), False),
    ('n4', (230, 226), False),
    ('n7', (70, 140), True), ('n7', (80, 160), True), ('n7', (76, 120), True),         # D's group
    ('n2', (98, 108), False), ('n8', (208, 132), False), ('n8', (200, 160), False),
    ('n6', (112, 76), True), ('n6', (134, 66), True), ('n9', (156, 80), True),          # B and C
    ('n9', (182, 84), True), ('n9', (190, 104), True), ('n9', (196, 116), True),
    ('n1', (116, 186), False),
]


def notebook_b():
    d = D()
    d.group('thin')
    for y in range(60, 271, 30):                                           # the notebook's ruled lines
        d.line((40, y), (296, y))
    d.line((300, 40), (300, 280))

    d.group()
    for a, b in _EDGES:
        d.line(_NODES[a], _NODES[b])
    for a, tip, _ in _TIPS:
        d.line(_NODES[a], tip)

    d.group('mid')
    for a, tip, living in _TIPS:
        if living:                                                         # the crossbar: living now
            ang = math.atan2(tip[1] - _NODES[a][1], tip[0] - _NODES[a][0]) + math.pi / 2
            dx, dy = 4 * math.cos(ang), 4 * math.sin(ang)
            d.line((tip[0] - dx, tip[1] - dy), (tip[0] + dx, tip[1] + dy))
    d.circle(*_NODES['root'], 7)
    for k, n in _NODES.items():
        if k != 'root':
            d.circle(*n, 1.6)

    d.group('mid')
    d.text(_NODES['root'][0], _NODES['root'][1] + 2.5, '1', size=7)
    d.text(286, 252, 'A', size=7)
    d.text(166, 64, 'B', size=7)
    d.text(204, 104, 'C', size=7)
    d.text(58, 150, 'D', size=7)
    d.text(60, 46, 'I THINK', size=7, anchor='start')
    d.line((312, 104), (326, 104))
    d.line((326, 100), (326, 108))
    d.text(332, 106.5, 'LIVING', size=7, anchor='start')
    d.line((312, 124), (326, 124))
    d.text(332, 126.5, 'EXTINCT', size=7, anchor='start')
    d.circle(319, 146, 5)
    d.text(332, 148.5, 'ANCESTOR', size=7, anchor='start')
    d.text(312, 176, 'A–B: IMMENSE GAP', size=7, anchor='start')
    d.text(312, 190, 'B–C: FINEST', size=7, anchor='start')
    d.text(312, 204, 'B–D: GREATER', size=7, anchor='start')
    d.text(200, 290, 'NOTEBOOK B, P. 36, JULY 1837 · REDRAWN, SCHEMATIC', size=7)
    return d


PLATES = {'coral-reefs': coral_reefs, 'notebook-b': notebook_b}
