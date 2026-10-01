"""Plates for Keeping Watch's first segment, Care before nursing (sprint 030). See plates_for.py."""
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


def basiliad():
    d = D()
    # The new city outside Caesarea as the sources describe it, a schematic and not a plan: no plan
    # survives and the site is unknown. The old city walled at left; a road a mile or two (Ramsay's
    # survey, 1892) to a church and monastery with the houses the letters and Gregory name around them.
    city, nc = (62, 150), (268, 150)
    d.group('thin')
    d.line((city[0] + 46, 150), (nc[0] - 70, 150))                        # the road's axis
    for a in range(0, 360, 60):                                           # the new city's six directions
        d.line(_pt(*nc, 18, a), _pt(*nc, 98, a))
    d.circle(*nc, 98)
    d.line((108, 236), (198, 236))                                        # the distance, dimensioned
    d.line((108, 230), (108, 242))
    d.line((198, 230), (198, 242))
    d.group()
    # the old city: a ring of wall with towers
    d.circle(*city, 44)
    for a in range(0, 360, 30):
        x, y = _pt(*city, 44, a)
        d.circle(x, y, 3.2)
    # the road out of the gate
    d.line((city[0] + 44, 146), (nc[0] - 72, 146))
    d.line((city[0] + 44, 154), (nc[0] - 72, 154))
    # the church at the centre: a cross in a square
    _box(d, nc[0] - 16, nc[1] - 16, 32, 32)
    d.line((nc[0], nc[1] - 10), (nc[0], nc[1] + 10))
    d.line((nc[0] - 10, nc[1]), (nc[0] + 10, nc[1]))
    d.group('mid')
    # the houses round it, each a range of rooms about a court
    houses = [(-90, 'MONASTERY'), (-30, 'HOSTEL'), (30, 'SICK'), (90, 'POOR'), (150, 'LEPERS'), (210, 'WORKSHOPS')]
    for a, _ in houses:
        x, y = _pt(*nc, 62, a)
        _box(d, x - 17, y - 11, 34, 22)
        d.line((x - 11, y - 5), (x + 11, y - 5), (x + 11, y + 5), (x - 11, y + 5), closed=True)
    for a, _ in houses:                                                   # paths in from the church
        d.line(_pt(*nc, 24, a), _pt(*nc, 46, a))
    _arrow(d, (nc[0] - 100, 150), (nc[0] - 72, 150))
    d.group('mid')
    d.text(city[0], 210, 'CAESAREA', size=7)
    d.text(153, 252, '1–2 MILES (1892)', size=7)
    d.text(nc[0], 262, 'THE NEW CITY · A SCHEMATIC', size=7)
    for a, s in houses:
        x, y = _pt(*nc, 62, a)
        d.text(x, y + 22 if 0 < a < 180 else y - 15, s, size=7)
    return d


def monastic_infirmary():
    d = D()
    # The infirmary on the Plan of Saint Gall (c. 820-830), redrawn from the manuscript in plan, turned
    # so its script reads upright: the sick monks' cloister with its ranges of rooms, half of the
    # church it shares with the novices, the physicians' house and the sixteen-bed herb garden.
    # Proportions follow the parchment loosely; the plan itself has no scale.
    cx, cy = 150, 150                                                     # the cloister garth
    d.group('thin')
    d.line((cx - 112, cy), (cx + 112, cy))                                # the cloister's axes
    d.line((cx, cy - 104), (cx, cy + 104))
    d.line((270, 40), (270, 262))                                         # the line between infirmary and physicians
    d.group()
    # the ranges round the cloister: outer and inner walls
    _box(d, cx - 96, cy - 96, 208, 192)
    _box(d, cx - 54, cy - 54, 108, 108)
    for y in (cy - 70, cy + 70):                                          # the ranges' inner walls
        d.line((cx - 96, y), (cx + 112, y))
    d.line((cx + 70, cy - 70), (cx + 70, cy + 70))
    d.line((cx + 70, cy), (cx + 112, cy))                                 # master's house | very sick
    d.line((cx, cy - 96), (cx, cy - 70))                                  # dormitory | warming room
    d.line((cx, cy + 70), (cx, cy + 96))                                  # refectory | store
    # the church's half: a long room with an apse, at the cloister's west
    d.line((cx - 96, cy - 70), (cx - 120, cy - 70), (cx - 120, cy + 70), (cx - 96, cy + 70))
    d.arc(cx - 120, cy, 22, 90, 270, n=24)
    d.group('mid')
    # the arcade: arches along each walk of the garth
    for k in range(5):
        for side in (-1, 1):
            x = cx - 40 + 20 * k
            d.arc(x, cy + side * 54, 6, 0 if side < 0 else 180, 180 if side < 0 else 360, n=10)
            y = cy - 40 + 20 * k
            d.arc(cx + side * 54, y, 6, 90 if side > 0 else -90, 270 if side > 0 else 90, n=10)
    d.circle(cx, cy, 8)                                                    # the garth's centre
    # the physicians' house: a square of rooms round a hearth
    px, py = 276, 52
    _box(d, px, py, 112, 96)
    d.line((px, py + 26), (px + 112, py + 26))
    d.line((px, py + 70), (px + 112, py + 70))
    d.line((px + 80, py + 26), (px + 80, py + 70))
    _box(d, px + 36, py + 40, 16, 16)
    # the herb garden: sixteen beds, eight down the middle and eight round the edge
    hx, hy = 276, 168
    _box(d, hx, hy, 112, 92)
    for row in range(4):
        for col in range(2):
            _box(d, hx + 18 + col * 42, hy + 18 + row * 15, 34, 9)
    for x in (hx + 6, hx + 60):
        _box(d, x, hy + 4, 46, 7)
        _box(d, x, hy + 81, 46, 7)
    for x in (hx + 4, hx + 101):
        _box(d, x, hy + 16, 7, 28)
        _box(d, x, hy + 48, 7, 28)
    d.group('mid')
    d.text(cx - 48, cy - 80, 'DORMITORY', size=7)
    d.text(cx + 56, cy - 80, 'WARMING', size=7)
    d.text(cx - 48, cy + 86, 'REFECTORY', size=7)
    d.text(cx + 56, cy + 86, 'STORE', size=7)
    d.text(cx + 91, cy - 32, 'MASTER', size=7)
    d.text(cx + 91, cy + 30, 'VERY', size=7)
    d.text(cx + 91, cy + 40, 'SICK', size=7)
    d.text(cx - 108, cy + 104, 'CHURCH', size=7)
    d.text(px + 56, py + 16, 'VERY SICK', size=7)
    d.text(px + 96, py + 51, 'DRUGS', size=7)
    d.text(px + 56, py + 86, 'PHYSICIAN', size=7)
    d.text(hx + 56, hy + 106, 'HERB GARDEN · 16 BEDS', size=7)
    return d


def hospitallers():
    d = D()
    # Left: the order's eight-pointed cross on its construction. Its eight points lie on one circle,
    # 45 degrees apart and 22.5 degrees off the arms' axes; each arm is a V from the centre to two
    # points, notched at 0.55 of the radius. Right: a hospital ward as a schematic, not a survey: a
    # vaulted hall of bays on a row of columns, a bed along each wall in every bay.
    cx, cy, R = 112, 148, 82
    notch = 0.55 * R
    d.group('thin')
    d.circle(cx, cy, R)
    d.circle(cx, cy, notch)
    for a in range(0, 360, 45):
        d.line((cx, cy), _pt(cx, cy, R, a + 22.5))
    d.line((cx - R - 10, cy), (cx + R + 10, cy))
    d.line((cx, cy - R - 10), (cx, cy + R + 10))
    d.group()
    for a in (0, 90, 180, 270):
        d.line((cx, cy), _pt(cx, cy, R, a - 22.5), _pt(cx, cy, notch, a), _pt(cx, cy, R, a + 22.5), closed=True)
    # the ward: a hall of five bays with a central row of columns
    wx, wy, ww, wh = 240, 40, 132, 220
    _box(d, wx, wy, ww, wh)
    d.group('thin')
    for k in range(1, 5):
        y = wy + k * wh / 5
        d.line((wx, y), (wx + ww, y))
    for k in range(5):                                                       # the cross vaults' diagonals
        y0, y1 = wy + k * wh / 5, wy + (k + 1) * wh / 5
        for x0, x1 in ((wx, wx + ww / 2), (wx + ww / 2, wx + ww)):
            d.line((x0, y0), (x1, y1))
            d.line((x1, y0), (x0, y1))
    d.group('mid')
    for k in range(1, 5):                                                    # the columns
        d.circle(wx + ww / 2, wy + k * wh / 5, 3.5)
    for k in range(5):                                                       # two beds a bay on each wall
        for j in (0, 1):
            y = wy + k * wh / 5 + 6 + j * 19
            _box(d, wx + 4, y, 30, 13)
            _box(d, wx + ww - 34, y, 30, 13)
            d.line((wx + 10, y + 2), (wx + 10, y + 11))                      # the pillow end
            d.line((wx + ww - 10, y + 2), (wx + ww - 10, y + 11))
    d.group('mid')
    d.text(cx, cy + R + 26, 'EIGHT POINTS ON ONE CIRCLE', size=7)
    d.text(wx + ww / 2, wy + wh + 16, 'A WARD · SCHEMATIC', size=7)
    return d


PLATES = {
    'basiliad': basiliad,
    'monastic-infirmary': monastic_infirmary,
    'hospitallers': hospitallers,
}
