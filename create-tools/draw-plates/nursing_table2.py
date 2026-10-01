"""Plates for Keeping Watch's trail At the table, its last two frames (sprint 030): the count and the
checklist. See plates_for.py."""
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


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def _rounded(d, x, y, w, h, r):
    """A rectangle with rounded corners, as one path of lines and quarter arcs."""
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        pts += [_pt(cx, cy, r, a0 + 90 * i / 8) for i in range(9)]
    d.line(*pts, closed=True)


def surgical_count():
    d = D()
    # The count laid out in plan: the operating table with the draped patient and the wound, the Mayo
    # stand across the legs, the back table and the basins inside the sterile field, and outside it,
    # on the circulating nurse's side, the rack where discarded sponges hang in tens. The arrows give the order the WHO's 2009 guidelines set for a count: the wound,
    # the instrument stand, the back table, then the discards. Inset: a 4 x 4 sponge with the
    # radiopaque thread woven into it. Proportions are schematic, not to a scale.
    table = (64, 40, 70, 222)                                             # x, y, w, h
    wound = (99, 150)
    mayo = (52, 196, 108, 30)
    back = (196, 168, 120, 64)
    basins = [(280, 128), (312, 128)]
    rack = (204, 34, 120, 40)
    d.group('thin')
    _rounded(d, 42, 104, 290, 142, 14)                                   # the sterile field, from the screen down
    d.line((99, 22), (99, 276))                                           # the table's axis
    d.line((30, wound[1]), (180, wound[1]))                               # the wound's cross-line
    d.group()
    _box(d, *table)                                                       # the operating table
    d.line((table[0] - 8, 98), (table[0] + table[2] + 8, 98))             # the anesthesia screen
    d.ellipse(99, 64, 13, 16)                                             # the head, beyond the screen
    d.line((80, 112), (118, 112), (124, 250), (74, 250), closed=True)     # the drape over the body
    d.ellipse(*wound, 12, 4.5)                                            # the wound
    _box(d, *mayo)                                                        # the Mayo stand across the legs
    _box(d, *back)                                                        # the back table
    for bx, by in basins:                                                 # the ring stand's basins
        d.circle(bx, by, 13)
        d.circle(bx, by, 8)
    _box(d, *rack)                                                        # the sponge rack, outside the field: ten pockets in two rows
    d.group('mid')
    for i in range(5):
        for j in range(2):
            _box(d, rack[0] + 6 + i * 23, rack[1] + 5 + j * 17, 17, 13)
    for i in range(6):                                                    # instruments laid on the Mayo stand
        x = mayo[0] + 8 + i * 7
        d.line((x, mayo[1] + 5), (x, mayo[1] + 25))
    for i in range(4):                                                    # the back table's trays and packs
        _box(d, back[0] + 8 + i * 28, back[1] + 10, 22, 18)
    _box(d, back[0] + 8, back[1] + 36, 104, 18)
    # the count's path, numbered: wound, Mayo stand, back table, then the discards on the rack
    stops = [(wound[0] + 18, wound[1] + 10), (mayo[0] + mayo[2] + 10, mayo[1] + 15),
             (back[0] + 10, back[1] - 8), (rack[0] + 60, rack[1] + rack[3] + 10)]
    for p, q in zip(stops, stops[1:]):
        a = math.atan2(q[1] - p[1], q[0] - p[0])
        p2 = (p[0] + 9 * math.cos(a), p[1] + 9 * math.sin(a))
        q2 = (q[0] - 9 * math.cos(a), q[1] - 9 * math.sin(a))
        d.line(p2, q2)
        _arrow(d, p2, q2)
    for x, y in stops:
        d.circle(x, y, 7)
    # inset: a 4 x 4 gauze sponge, its weave and its radiopaque thread
    sx, sy, s = 340, 192, 46
    _box(d, sx, sy, s, s)
    d.lines([[(sx + k, sy), (sx + k, sy + s)] for k in range(6, s, 6)] +
            [[(sx, sy + k), (sx + s, sy + k)] for k in range(6, s, 6)])
    d.group()
    d.line(*[(sx + 2 + i * (s - 4) / 40, sy + s / 2 + 5 * math.sin(i * math.pi / 5)) for i in range(41)])
    d.group('mid')
    for n, (x, y) in enumerate(stops, 1):
        d.text(x, y + 2.5, str(n), size=7)
    d.text(99, 284, 'TABLE', size=7)
    d.text(147, mayo[1] + 17.5, 'MAYO', size=7)
    d.text(back[0] + back[2] / 2, back[1] + back[3] + 10, 'BACK TABLE', size=7)
    d.text(rack[0] + rack[2] / 2, rack[1] - 5, 'SPONGE RACK', size=7)
    d.text(sx + s / 2, sy + s + 11, 'X-RAY THREAD', size=7)
    d.text(187, 258, 'STERILE FIELD', size=7)
    d.text(rack[0] + 72, rack[1] + rack[3] + 12.5, 'DISCARDS', size=7, anchor='start')
    return d


def surgical_checklist():
    d = D()
    # The WHO Surgical Safety Checklist (2009 revision) on the time line of an operation: the patient's
    # course from arrival to leaving the room, with induction, incision and closure marked, and the
    # three pauses as gates across it. Each gate carries one box for each of its items, 7, 7 and 5,
    # nineteen in all; the bars beneath say who must be present at each.
    y0 = 150                                                              # the time line
    x0, x1 = 30, 372
    gates = [(92, 7, 'SIGN IN'), (196, 7, 'TIME OUT'), (318, 5, 'SIGN OUT')]
    events = [(128, 'INDUCTION'), (232, 'INCISION'), (288, 'CLOSURE')]
    d.group('thin')
    for x in range(x0, x1 + 1, 18):                                       # the time scale's ticks
        d.line((x, y0 - 3), (x, y0 + 3))
    for x, _, _ in gates:                                                 # each gate's centre line
        d.line((x, 34), (x, 252))
    for x, _ in events:
        d.line((x, y0), (x, y0 + 40))
    d.line((x0, 252), (x1, 252))                                          # the base of the who-is-present bars
    d.group()
    d.line((x0, y0), (x1, y0))                                            # the operation, left to right
    _arrow(d, (x1 - 10, y0), (x1, y0), size=7)
    for x, n, _ in gates:                                                 # the gates
        h = 12 * n + 8
        _box(d, x - 14, y0 - h / 2, 28, h)
    for x, _ in events:                                                   # the events, as triangles on the line
        d.line((x - 6, y0 + 40), (x + 6, y0 + 40), (x, y0 + 30), closed=True)
    d.group('mid')
    for x, n, _ in gates:                                                 # one box per item
        h = 12 * n + 8
        for i in range(n):
            _box(d, x - 4.5, y0 - h / 2 + 5.5 + 12 * i, 9, 9)
    # who must be present: nurse and anesthetist at sign in; nurse, anesthetist and surgeon after
    rows = [(226, 'NURSE'), (236, 'ANESTHETIST'), (246, 'SURGEON')]
    spans = [(gates[0][0] - 14, gates[0][0] + 14, 2), (gates[1][0] - 14, gates[1][0] + 14, 3), (gates[2][0] - 14, gates[2][0] + 14, 3)]
    for a, b, k in spans:
        for y, _ in rows[:k]:
            d.line((a, y), (b, y))
    d.group('mid')
    for x, n, label in gates:
        h = 12 * n + 8
        d.text(x, y0 - h / 2 - 8, label, size=7)
        d.text(x, y0 + h / 2 + 11, str(n), size=7)
    for x, label in events:
        d.text(x, y0 + 56, label, size=7)
    for y, label in rows:
        d.text(8, y + 2.5, label, size=7, anchor='start')
    d.text(x0 + 8, y0 - 8, 'ARRIVE', size=7, anchor='start')
    d.text(x1 - 6, y0 - 8, 'LEAVE', size=7, anchor='end')
    return d


PLATES = {
    'surgical-count': surgical_count,
    'surgical-checklist': surgical_checklist,
}
