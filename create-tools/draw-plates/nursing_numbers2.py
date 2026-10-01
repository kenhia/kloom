"""Plates for the end of Keeping Watch's trail Nightingale's numbers (sprint 030, part numbers2). See plates_for.py."""
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


def _chord(cx, cy, r, y):
    """The x extent of a circle at height y, or None."""
    h = r * r - (y - cy) ** 2
    if h <= 0:
        return None
    w = math.sqrt(h)
    return cx - w, cx + w


def infection_control_nurse():
    d = D()
    # Phage typing a staphylococcus, the laboratory half of the infection control sister's count. Left: a
    # Petri dish in plan, its base ruled into a grid; the patient's strain spread as a lawn, and a drop of
    # each typing phage at its routine test dilution placed in a square. Where a phage lyses the strain the
    # lawn clears in a spot; the pattern of spots names the type. Which spots clear here is illustrative,
    # not a real strain's pattern. Right: the dish in section, lid over base, agar and lawn, drawn to scale
    # for a 90 mm dish with about 4 mm of agar (the vertical scale doubled).
    cx, cy, R = 128, 146, 104
    n, s = 5, 30                                                            # a 5 x 5 grid of 30-unit squares
    x0, y0 = cx - n * s / 2, cy - n * s / 2
    d.group('thin')
    for k in range(n + 1):                                                  # the grid ruled on the base
        d.line((x0 + k * s, y0), (x0 + k * s, y0 + n * s))
        d.line((x0, y0 + k * s), (x0 + n * s, y0 + k * s))
    d.line((cx - R - 8, cy), (cx + R + 8, cy))                              # the dish's axes
    d.line((cx, cy - R - 8), (cx, cy + R + 8))
    d.group()
    d.circle(cx, cy, R)                                                     # the dish's wall, base and lid
    d.circle(cx, cy, R - 4)
    # the section: base and lid, a 90 mm dish at 1.4 units a millimetre across, the depth doubled
    sx, sy, sw = 262, 160, 126
    d.line((sx, sy - 22), (sx, sy), (sx + sw, sy), (sx + sw, sy - 22))     # base
    d.line((sx - 5, sy - 14), (sx - 5, sy - 30), (sx + sw + 5, sy - 30), (sx + sw + 5, sy - 14))   # lid
    d.group('mid')
    # the lawn: streaks across the agar, clipped to the dish and broken where a spot has cleared
    lysed = {(0, 1), (1, 3), (2, 0), (2, 2), (3, 1), (4, 3)}
    spots = [(x0 + (i + 0.5) * s, y0 + (j + 0.5) * s) for i, j in lysed]
    for k in range(-9, 10):
        y = cy + k * 10.5
        c = _chord(cx, cy, R - 8, y)
        if not c:
            continue
        gaps = sorted(g for g in (_chord(px, py, 11, y) for px, py in spots) if g)
        x, segs = c[0], []
        for a, b in gaps:
            if a > x:
                segs.append([(x, y), (a, y)])
            x = max(x, b)
        if c[1] > x:
            segs.append([(x, y), (c[1], y)])
        d.lines(segs)
    # the agar and lawn in section, cleared under the drop at the centre
    m = sx + sw / 2
    d.line((sx + 1, sy - 9), (sx + sw - 1, sy - 9))
    d.line((sx + 1, sy - 11), (m - 10, sy - 11))
    d.line((m + 10, sy - 11), (sx + sw - 1, sy - 11))
    d.group()
    # the drops: a small ring in every square; where the phage lyses, a clear spot in the lawn
    for i in range(n):
        for j in range(n):
            px, py = x0 + (i + 0.5) * s, y0 + (j + 0.5) * s
            if (i, j) in lysed:
                d.circle(px, py, 10)
                d.circle(px, py, 2)
            else:
                d.circle(px, py, 3)
    _arrow(d, (m, sy - 62), (m, sy - 34))                                 # where the drop goes
    d.line((m, sy - 62), (m, sy - 34))
    # the legend's two marks
    d.circle(sx + 12, 214, 7)
    d.circle(sx + 12, 214, 1.5)
    d.circle(sx + 12, 234, 3)
    d.group('mid')
    d.text(m, sy - 68, 'A DROP OF PHAGE', size=7)
    d.text(m, sy + 16, 'LID · LAWN ON AGAR · BASE', size=7)
    d.text(m, sy + 28, 'IN SECTION', size=7)
    d.text(sx + 28, 216.5, 'LYSED: CLEARED', size=7, anchor='start')
    d.text(sx + 28, 236.5, 'NOT LYSED', size=7, anchor='start')
    d.text(sx + 4, 262, 'THE PATTERN NAMES', size=7, anchor='start')
    d.text(sx + 4, 274, 'THE TYPE', size=7, anchor='start')
    d.text(cx, cy + R + 22, 'ONE STRAIN · 25 PHAGES · ILLUSTRATIVE', size=7)
    return d


def hand_hygiene():
    d = D()
    # The WHO's two zones (Guidelines on Hand Hygiene in Health Care, 2009, Part I.21.4) in plan, a schematic:
    # a bed with its rails, bedside table, drip stand and monitor inside the patient zone; the room, its door
    # and a trolley outside it, in the health-care area. A nurse's path in from the door crosses the zone's edge
    # (moment 1), cleans before opening a line (2), after emptying a drain (3), on leaving the patient (4); a
    # second path takes a used tray from the bedside table out to the trolley (5).
    zx0, zy0, zx1, zy1 = 128, 46, 300, 236                                 # the patient zone
    d.group('thin')
    _box(d, 20, 24, 360, 258)                                               # the room
    for k in range(int((zx1 - zx0) / 8) + 1):                               # the zone's edge, dashed
        x = zx0 + k * 8
        d.line((x, zy0), (min(x + 4, zx1), zy0))
        d.line((x, zy1), (min(x + 4, zx1), zy1))
    for k in range(int((zy1 - zy0) / 8) + 1):
        y = zy0 + k * 8
        d.line((zx0, y), (zx0, min(y + 4, zy1)))
        d.line((zx1, y), (zx1, min(y + 4, zy1)))
    d.group()
    # the bed: frame, mattress, pillow, the rails along both sides, head to the top
    bx, by, bw, bh = 176, 70, 62, 140
    _box(d, bx, by, bw, bh)
    _box(d, bx + 4, by + 4, bw - 8, bh - 8)
    d.line((bx + 12, by + 10), (bx + bw - 12, by + 10), (bx + bw - 12, by + 30), (bx + 12, by + 30), closed=True)
    for x in (bx - 6, bx + bw + 6):
        d.line((x, by + 36), (x, by + 100))
    # the patient, a figure in plan: head and the outline of a body under the sheet
    d.circle(bx + bw / 2, by + 20, 7)
    d.line((bx + 16, by + 34), (bx + bw - 16, by + 34), (bx + bw - 18, by + 128), (bx + 18, by + 128), closed=True)
    # the bedside table, the drip stand and its line, the monitor
    _box(d, 252, 74, 34, 26)
    d.circle(152, 76, 6)
    d.curve(f'M152 82 C152 110 170 112 {bx + 14} 116')
    _box(d, 250, 136, 36, 22)
    # outside: the trolley and the door
    _box(d, 326, 74, 40, 28)
    d.line((20, 136), (20, 172))
    d.group('mid')
    d.arc(20, 136, 36, 0, 90, n=16)                                         # the door's swing
    # the nurse's path, with the moments where hands are cleaned
    path = [(34, 154), (128, 154), (162, 124), (164, 176), (128, 214), (60, 236)]

    def _leg(p, q, r0, r1):
        # a leg of the path, stopped short of the rings at either end
        L = math.dist(p, q)
        ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
        d.line((p[0] + ux * r0, p[1] + uy * r0), (q[0] - ux * r1, q[1] - uy * r1))

    for k in range(len(path) - 1):
        _leg(path[k], path[k + 1], 0 if k == 0 else 7, 0 if k == len(path) - 2 else 7)
    _arrow(d, path[-2], path[-1])
    _leg((269, 100), (300, 92), 0, 7)
    _leg((300, 92), (326, 88), 7, 0)
    _arrow(d, (300, 92), (326, 88))
    d.group()
    moments = [(128, 154), (162, 124), (164, 176), (128, 214), (300, 92)]
    for x, y in moments:
        d.circle(x, y, 7)
    d.group('mid')
    for k, (x, y) in enumerate(moments, 1):
        d.text(x, y + 2.5, str(k), size=7)
    d.text(214, 258, 'PATIENT ZONE', size=7)
    d.text(74, 46, 'HEALTH-CARE AREA', size=7)
    d.text(346, 120, 'TROLLEY', size=7)
    d.text(46, 128, 'DOOR', size=7)
    d.text(268, 172, 'MONITOR', size=7)
    d.text(152, 64, 'DRIP', size=7)
    d.text(269, 114, 'TABLE', size=7)
    return d


PLATES = {
    'infection-control-nurse': infection_control_nurse,
    'hand-hygiene': hand_hygiene,
}
