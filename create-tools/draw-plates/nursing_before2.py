"""Plates for the rest of Keeping Watch's first segment, Care before nursing (sprint 030, part before2).
See plates_for.py."""
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


def beguines():
    d = D()
    # A court beguinage of the "courtyard" type (ICOMOS 1998: Bruges, Turnhout), as a schematic, not a
    # survey of any one court: a walled and moated enclosure with one gate, a green with the church at its
    # centre, a ring of small houses each with a garden, and the community buildings the evaluation names:
    # the infirmary with its chapel, the Grande Dame's house, the Table of the Holy Spirit, a convent
    # (community house) and the farm.
    x0, y0, x1, y1 = 46, 28, 354, 252
    gx = (x0 + x1) / 2
    d.group('thin')
    d.line((gx, y0 - 14), (gx, y1 + 18))                                     # the court's axis
    d.line((x0 - 14, (y0 + y1) / 2), (x1 + 14, (y0 + y1) / 2))
    # the moat, offset outside the wall
    d.line((x0 - 9, y0 - 9), (x1 + 9, y0 - 9), (x1 + 9, y1 + 9), (gx + 9, y1 + 9))
    d.line((gx - 9, y1 + 9), (x0 - 9, y1 + 9), (x0 - 9, y0 - 9))
    # the green
    gl, gt, gr, gb = 112, 90, 288, 202
    d.line((gl, gt), (gr, gt), (gr, gb), (gl, gb), closed=True)
    d.group()
    # the wall, broken by the gate
    d.line((gx - 9, y1), (x0, y1), (x0, y0), (x1, y0), (x1, y1), (gx + 9, y1))
    _box(d, gx - 9, y1 - 8, 18, 16)                                           # the gatehouse
    d.line((gx - 5, y1 + 8), (gx - 5, y1 + 18))                               # the bridge over the moat
    d.line((gx + 5, y1 + 8), (gx + 5, y1 + 18))
    # the church: nave, crossing and apse, its apse to the east (up the page)
    cx, cy = gx, 150
    d.line((cx - 10, cy + 30), (cx - 10, cy - 4), (cx - 24, cy - 4), (cx - 24, cy - 16), (cx - 10, cy - 16),
           (cx - 10, cy - 24), (cx + 10, cy - 24), (cx + 10, cy - 16), (cx + 24, cy - 16), (cx + 24, cy - 4),
           (cx + 10, cy - 4), (cx + 10, cy + 30), closed=True)
    d.arc(cx, cy - 24, 10, 180, 360, n=16)
    # the infirmary, a long range on the east side, with its chapel
    _box(d, 292, 76, 54, 88)
    _box(d, 307, 164, 24, 22)
    d.arc(319, 186, 12, 0, 180, n=14)
    d.group('mid')
    # houses round the green: each a small house and a garden in front of it
    for k in range(8):                                                        # along the north wall
        x = 62 + k * 30
        _box(d, x, y0 + 6, 20, 13)
        _box(d, x + 2, y0 + 19, 16, 10)
    for k in range(4):                                                        # along the west wall
        y = 70 + k * 30
        _box(d, x0 + 6, y, 13, 20)
        _box(d, x0 + 19, y + 2, 10, 16)
    for x in (292, 320):                                                      # along the south wall
        _box(d, x, y1 - 19, 20, 13)
    # the Grande Dame's house, the Table of the Holy Spirit and a convent, by the gate
    _box(d, 132, 222, 40, 20)
    _box(d, 228, 222, 40, 20)
    _box(d, 62, 218, 50, 26)                                                  # a convent, by the south-west corner
    d.line((87, 218), (87, 244))
    # the farm and brewhouse in the north-east corner
    _box(d, 312, 34, 34, 28)
    d.line((312, 48), (346, 48))
    # trees on the green, on a grid, clear of the church
    for i in range(4):
        for j in range(3):
            tx, ty = gl + 18 + i * 47, gt + 16 + j * 40
            if abs(tx - cx) < 34 and abs(ty - cy) < 44:
                continue
            d.circle(tx, ty, 5)
    d.group('mid')
    d.text(cx, cy + 44, 'CHURCH', size=7)
    d.text(319, 124, 'INFIRMARY', size=7)
    d.text(319, 208, 'CHAPEL', size=7)
    d.text(152, 216, 'GRANDE DAME', size=7)
    d.text(248, 216, 'POOR TABLE', size=7)
    d.text(87, 212, 'CONVENT', size=7)
    d.text(329, 72, 'FARM', size=7)
    d.text(gx, 290, 'A COURT BEGUINAGE · SCHEMATIC', size=7)
    return d


def daughters_of_charity():
    d = D()
    # Left: the round in the rule of Châtillon (1617), as a schematic: from the sisters' lodging down the
    # street to five sick houses, visited in the rule's order, those who have someone to help them first
    # and those who have no one last. Right: the tray as the rule sets it on the bed, in plan: napkin,
    # glass, spoon and bread roll, then the soup and the meat on a plate.
    sy = 160                                                                  # the street's centre line
    d.group('thin')
    d.line((20, sy - 8), (190, sy - 8))                                       # the street
    d.line((20, sy + 8), (190, sy + 8))
    d.line((52, 100), (52, sy - 8))                                           # the lane from the lodging
    d.line((68, 100), (68, sy - 8))
    d.line((210, 30), (210, 270))                                             # the divide between the two
    d.group()
    _box(d, 38, 70, 44, 30)                                                   # the sisters' lodging
    d.line((38, 70), (60, 56), (82, 70))
    _box(d, 110, 72, 44, 24)                                                  # the parish church
    d.arc(154, 84, 12, -90, 90, n=12)
    doors = []
    for hx, above in [(64, False), (92, True), (110, False), (140, True), (156, False)]:
        hy = sy - 40 if above else sy + 18                                    # houses on both sides, in plan
        _box(d, hx, hy, 26, 22)
        _box(d, hx + 2, hy + 2, 22, 18)
        doors.append((hx + 13, hy + 22 if above else hy))
    # the bed and tray, in plan
    bx, by, bw, bh = 236, 50, 130, 216
    _box(d, bx, by, bw, bh)
    _box(d, bx + 14, by + 6, bw - 28, 24)                                     # the pillow
    d.line((bx, by + 180), (bx + bw, by + 180))                               # the turned-down sheet
    tx, ty, tw, th = 250, 104, 102, 84
    _box(d, tx, ty, tw, th)                                                   # the tray
    d.group('mid')
    # the round along the street, with a stub to each door in the rule's order
    d.line((60, 100), (60, sy), (176, sy))
    _arrow(d, (60, sy), (176, sy), size=4)
    for x, y in doors:
        d.line((x, sy), (x, y))
    # the napkin spread over the tray, one corner turned back
    _box(d, tx + 4, ty + 4, tw - 8, th - 8)
    d.line((tx + tw - 26, ty + th - 4), (tx + tw - 4, ty + th - 26))
    d.circle(tx + 20, ty + 22, 8)                                             # the glass
    d.circle(tx + 20, ty + 22, 5)
    d.ellipse(tx + 20, ty + 62, 4, 7)                                         # the spoon
    d.line((tx + 20, ty + 54), (tx + 20, ty + 36))
    d.ellipse(tx + 80, ty + 20, 12, 7)                                        # the bread roll
    d.line((tx + 70, ty + 20), (tx + 90, ty + 20))
    d.circle(tx + 48, ty + 46, 16)                                            # the soup bowl
    d.circle(tx + 48, ty + 46, 11)
    d.circle(tx + 80, ty + 56, 13)                                            # the plate, with the meat
    d.ellipse(tx + 80, ty + 56, 6, 4)
    d.group('mid')
    for k, (x, y) in enumerate(doors, 1):
        d.text(x, y - 8 if y < sy else y + 15, str(k), size=7)
    d.text(60, 114, 'LODGING', size=7)
    d.text(132, 110, 'CHURCH', size=7)
    d.text(105, 240, '1 HAS HELP · 5 HAS NONE', size=7)
    d.text(tx + 20, ty - 6, 'GLASS', size=7)
    d.text(tx + 80, ty - 6, 'BREAD', size=7)
    d.text(tx + 50, ty + th + 12, 'SOUP · PLATE · SPOON', size=7)
    d.text(105, 280, 'THE ROUND', size=7)
    d.text(301, 280, 'THE TRAY ON THE BED', size=7)
    return d


# The first page of Martha Ballard's diary, 1-22 January 1785, from the transcription at dohistory.org:
# (day of month, day of week as she numbered it, Sunday 1, the entry's length in characters, a delivery?)
_PAGE_1785 = [
    (1, 7, 140, False), (2, 1, 93, False), (3, 2, 35, False), (4, 3, 92, False), (5, 4, 39, False),
    (6, 5, 45, False), (7, 6, 34, False), (8, 7, 67, False), (9, 1, 94, True), (10, 2, 32, False),
    (11, 3, 38, False), (12, 4, 43, False), (13, 5, 41, False), (14, 6, 45, False), (16, 1, 47, False),
    (17, 2, 37, False), (18, 3, 36, False), (19, 4, 38, False), (20, 5, 158, True), (21, 6, 35, False),
    (22, 7, 70, False),
]


def martha_ballard():
    d = D()
    # A construction of the diary's first page, 1-22 January 1785 (14 and 15 January share an entry), as
    # the transcription gives it: a ruled page with her two columns, the day of the month and the day of the
    # week (Sunday 1), and each entry drawn as a line whose length is the entry's length in characters.
    # The two deliveries, 9 and 20 January, are bracketed. Lengths are counted from the transcription.
    x0, x1, y0 = 70, 360, 38
    step = 10
    scale = (x1 - x0 - 24) / 160                                              # 160 characters fill the line
    d.group('thin')
    for k in range(len(_PAGE_1785) + 1):                                      # the ruling
        y = y0 + k * step
        d.line((x0 - 34, y), (x1, y))
    d.line((x0 - 34, y0), (x0 - 34, y0 + len(_PAGE_1785) * step))             # the page's margin
    d.line((x0 - 14, y0), (x0 - 14, y0 + len(_PAGE_1785) * step))             # her two columns
    d.line((x0 + 4, y0), (x0 + 4, y0 + len(_PAGE_1785) * step))
    for v in (0, 50, 100):                                                    # a scale of characters
        x = x0 + 14 + v * scale
        d.line((x, y0 + len(_PAGE_1785) * step + 6), (x, y0 + len(_PAGE_1785) * step + 12))
    d.line((x0 + 14, y0 + len(_PAGE_1785) * step + 9), (x0 + 14 + 100 * scale, y0 + len(_PAGE_1785) * step + 9))
    d.group('mid')
    for k, (day, wd, n, birth) in enumerate(_PAGE_1785):
        y = y0 + k * step + step / 2
        d.text(x0 - 24, y + 2.5, str(day), size=7)
        d.text(x0 - 5, y + 2.5, str(wd), size=7)
    d.group()
    for k, (day, wd, n, birth) in enumerate(_PAGE_1785):
        y = y0 + k * step + step / 2
        d.line((x0 + 14, y), (x0 + 14 + n * scale, y))
    d.group('mid')
    for k, (day, wd, n, birth) in enumerate(_PAGE_1785):
        if not birth:
            continue
        y = y0 + k * step + step / 2
        d.line((x0 - 40, y - 5), (x0 - 46, y - 5), (x0 - 46, y + 5), (x0 - 40, y + 5))
        d.circle(x0 - 54, y, 3)
    d.group('mid')
    yb = y0 + len(_PAGE_1785) * step
    d.text(x0 - 24, y0 - 6, 'DAY', size=7)
    d.text(x0 - 5, y0 - 6, 'WK', size=7)
    d.text(x0 + 14 + 50 * scale, y0 - 6, 'THE ENTRY', size=7)
    d.text(x0 + 14 + 100 * scale, yb + 22, '100 CHARACTERS', size=7)
    d.circle(x0 - 54, yb + 19.5, 3)
    d.text(x0 - 46, yb + 22, 'DELIVERY', size=7, anchor='start')
    d.text(200, 292, 'THE FIRST PAGE · 1–22 JANUARY 1785', size=7)
    return d


def kaiserswerth():
    d = D()
    # Left: the sisters' day and night at Kaiserswerth on a 24-hour dial, midnight at the top: rising at
    # five, the meals of Nightingale's letter of 1851 as ticks, bed at ten, and outside the dial the two
    # night watches of her pamphlet, 22:00-01:30 and 01:30-05:00, three and a half hours each.
    # Right: the hospital's four departments as a schematic, not a survey, with the watcher's hourly round
    # through every ward but the men's, starting from her station in the children's room.
    cx, cy, R = 104, 150, 72
    ang = lambda h: -90 + h * 15                                              # an hour on the 24-hour dial
    d.group('thin')
    d.circle(cx, cy, R)
    d.circle(cx, cy, R - 14)
    for h in range(24):
        d.line(_pt(cx, cy, R - 4 if h % 6 else R - 14, ang(h)), _pt(cx, cy, R, ang(h)))
    d.line((cx, cy - R - 6), (cx, cy + R + 6))
    d.line((cx - R - 6, cy), (cx + R + 6, cy))
    d.line((214, 40), (214, 262))
    d.group()
    d.arc(cx, cy, R - 7, ang(22), ang(29), n=30)                              # asleep, 22:00 to 05:00
    d.arc(cx, cy, R + 9, ang(22), ang(25.5), n=20)                            # the first watch
    d.arc(cx, cy, R + 15, ang(25.5), ang(29), n=20)                           # the second watch
    for h in (22, 25.5, 29):
        d.line(_pt(cx, cy, R, ang(h)), _pt(cx, cy, R + 18, ang(h)))
    # the hospital: a corridor with four departments off it
    wards = [('MEN', 226, 52), ('WOMEN', 300, 52), ('BOYS', 226, 160), ('CHILDREN', 300, 160)]
    for name, x, y in wards:
        _box(d, x, y, 66, 86)
    d.line((226, 144), (366, 144))
    d.line((226, 154), (366, 154))
    d.group('mid')
    for h in (5.75, 11, 12, 14.5, 19):                                        # rising breakfast, dinners, rye, supper
        d.circle(*_pt(cx, cy, R - 7, ang(h)), 2.4)
    for name, x, y in wards:                                                  # beds: four to a small ward
        for i in range(2):
            for j in range(2):
                _box(d, x + 8 + i * 30, y + 10 + j * 38, 20, 11)
    # the watcher's round, from the children's room through women's and boys' and back
    d.line((333, 232), (333, 149), (259, 149))                                # from the station to the corridor
    d.line((333, 149), (333, 124))                                            # into the women's ward
    _arrow(d, (333, 149), (333, 124), size=4)
    d.line((259, 149), (259, 174))                                            # into the boys' ward
    _arrow(d, (259, 149), (259, 174), size=4)
    d.circle(333, 236, 4)
    d.group('mid')
    d.text(cx, cy - R + 24, '0:00', size=7)
    d.text(cx + R + 16, cy + 3, '6', size=7)
    d.text(cx, cy + R + 14, '12:00', size=7)
    d.text(cx - R - 14, cy + 3, '18', size=7)
    d.text(*_pt(cx, cy, R + 24, ang(23.75)), 'WATCH 1', size=7)
    d.text(*_pt(cx, cy, R + 30, ang(27.6)), 'WATCH 2', size=7)
    d.text(cx, cy + 3, 'ASLEEP 22–5', size=7)
    for name, x, y in wards:
        d.text(x + 33, y + 98 if y > 100 else y - 4, name, size=7)
    d.text(296, 286, 'HOURLY ROUND · NOT THE MEN’S WARD', size=7)
    return d


PLATES = {
    'beguines': beguines,
    'daughters-of-charity': daughters_of_charity,
    'martha-ballard': martha_ballard,
    'kaiserswerth': kaiserswerth,
}
