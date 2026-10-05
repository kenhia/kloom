"""Plates for Daily Bread's part table2 (sprint 051): the supermarket and fast food. See plates_for.py."""
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


def supermarket():
    d = D()
    # Clarence Saunders's "Self-Serving Store", U.S. Patent 1,242,872 (filed 1916, granted 1917), Fig. 2,
    # turned so the street is on the left. Positions are read off the patent's plan (a 1,200 by 375 unit
    # store, measured on the sheet) and scaled into the plate: X runs from the street front (30) to the
    # rear wall (360), Y from the left wall (85) to the right wall (215). The plan's own proportions are
    # kept only roughly (the plate is shorter); the arrangement is the patent's.
    def P(px, py):                                     # patent sheet units (x across, y front=1230, rear=30)
        return (360 - (py - 30) / 1200 * 330, 85 + (px - 180) / 375 * 130)

    front, rear = 1230, 30
    p6, p5 = 235, 660                                  # rear and front partitions
    left, right = 180, 555

    d.group('thin')
    for py in (p6, p5):                                # the partitions' center lines, across the store
        d.line(P(left - 25, py), P(right + 25, py))
    d.line(P((left + right) / 2, front), P((left + right) / 2, rear - 15))        # the store's axis

    d.group()
    d.line(P(330, front), P(left, front), P(left, rear), P(right, rear), P(right, front), P(400, front))
    # rear partition, with the two stockroom doors
    d.line(P(left, p6), P(250, p6))
    d.line(P(300, p6), P(435, p6))
    d.line(P(485, p6), P(right, p6))
    # front partition, open at the entrance (aisle 1) and at the exit (last aisle)
    d.line(P(255, p5), P(480, p5))
    # cabinets: wall shelving, two rows joined to the front partition, one to the rear
    for px, y0, y1 in ((198, 270, p5), (537, 270, p5)):
        d.line(P(px, y0), P(px, y1))
    d.line(P(198, 270), P(537, 270))                   # shelving across the rear of the salesroom
    for px in (265, 450):                              # cabinets 12, open at the rear end
        _x0, _y0 = P(px - 9, 300)
        _x1, _y1 = P(px + 9, p5)
        _box(d, _x1, _y0, _x0 - _x1, _y1 - _y0)
    _x0, _y0 = P(351, 270)                             # cabinet 16, open at the front end
    _x1, _y1 = P(369, 625)
    _box(d, _x1, _y0, _x0 - _x1, _y1 - _y0)
    # the checkout: partition 34 and the counter 38 in the lobby's right side
    d.line(P(470, p5 + 20), P(470, 1150))
    _x0, _y0 = P(400, 720)
    _x1, _y1 = P(430, 1180)
    _box(d, _x1, _y0, _x0 - _x1, _y1 - _y0)
    # the fruit counter (32) at the front of the lobby's left side
    _x0, _y0 = P(215, 1000)
    _x1, _y1 = P(255, 1190)
    _box(d, _x1, _y0, _x0 - _x1, _y1 - _y0)

    d.group('mid')
    # the shopper's path: in at the door, round to aisle 1, up and down four aisles, out to the checkout
    path = [P(365, front + 25), P(365, 1050), P(300, 900), P(228, 760), P(228, p5 + 5),
            P(228, 300), P(232, 285), P(305, 285), P(308, 300), P(308, 640),
            P(312, 655), P(405, 655), P(408, 640), P(408, 300), P(412, 285), P(490, 285),
            P(494, 300), P(494, p5), P(510, 700), P(510, 1190), P(488, 1205), P(450, 1190),
            P(448, 720), P(420, 690), P(370, 900), P(365, front + 25)]
    d.dashed(*path, dash=4, gap=3)
    for i in (5, 9, 13, 17, 20, 23):                   # arrowheads along the way
        a, b = path[i - 1], path[i]
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        _arrow(d, a, m, size=4)
    # the one-way gates
    for px, py in ((228, p5 + 12), (440, 705)):
        x, y = P(px, py)
        d.line((x - 1, y - 7), (x + 1, y + 7))

    d.group('mid')
    x, _ = P(0, (rear + p6) / 2)
    d.text(x, 152, 'STOCKROOM', size=7)
    x, _ = P(0, (p5 + front) / 2 + 40)
    d.text(x - 8, 72, 'LOBBY', size=7)
    x, _ = P(0, (p6 + p5) / 2)
    d.text(x, 232, 'SALESROOM · FOUR AISLES', size=7)
    d.text(15, 153, 'STREET', size=7, anchor='middle')
    x, y = P(228, p5 + 12)
    d.text(x - 6, 72, 'IN', size=7)
    x, y = P(430, 950)
    d.text(x, 232, 'CHECKOUT', size=7)
    d.text(200, 262, 'U.S. PATENT 1,242,872 · PLAN, TURNED', size=7)
    d.text(200, 276, 'ONE PATH FROM DOOR TO DOOR', size=7)
    return d


def fast_food():
    d = D()
    # A self-service hamburger kitchen of the McDonald brothers' kind, in plan, with the path of an order.
    # Schematic: the stations are the ones the histories name (Love's crew of nine: three window men, a grill
    # man, two bun men, a fry man, a shake man, a cleanup man), set out on a plan of our own, not a surviving
    # drawing. Customers walk up to the windows at the front; the food comes forward from the grill.
    x0, x1, yb, yf = 60, 340, 52, 196                  # building: back wall and front (window) wall
    wins = [130, 200, 270]                             # the three order windows
    d.group('thin')
    d.line((200, 52), (200, 108))                      # the axis, grill to bun table
    for x in wins:                                     # each window's line of sight
        d.line((x, yf - 70), (x, 262))
    d.line((x0 - 15, yf), (x1 + 15, yf))

    d.group()
    d.line((x0, yf), (x0, yb), (x1, yb), (x1, yf))
    pts = [(x0, yf)]
    for x in wins:                                     # the front wall, open at each window
        pts += [(x - 13, yf)]
        d.line(*pts)
        pts = [(x + 13, yf)]
    d.line(pts[0], (x1, yf))
    _box(d, 125, 60, 150, 20)                          # the grill along the back wall
    _box(d, 140, 112, 120, 18)                         # the bun table: dress and wrap
    _box(d, 70, 92, 34, 58)                            # the fryers
    _box(d, 296, 92, 34, 58)                           # shakes and drinks
    _box(d, 110, 168, 180, 12)                         # the counter behind the windows

    d.group('mid')
    for i in range(6):                                 # patties in rows on the grill
        for j in range(2):
            d.circle(140 + i * 24, 66 + j * 8, 3)
    for i in range(4):                                 # wrapped burgers on the bun table
        _box(d, 152 + i * 26, 117, 14, 8)
    for x in (80, 94):                                 # fry baskets
        _box(d, x - 5, 104, 10, 14)
    for y in (104, 124):                               # mixers
        d.circle(313, y + 6, 5)

    d.group('mid')
    # the order: up to the window, food forward from grill to bun table to counter, and back out
    flows = [((200, 86), (200, 108)), ((200, 134), (200, 164)),
             ((108, 140), (150, 170)), ((292, 140), (250, 170))]
    for a, b in flows:
        d.line(a, b)
        _arrow(d, a, b, size=4)
    for x in wins:
        d.line((x - 5, 244), (x - 5, 204))
        _arrow(d, (x - 5, 244), (x - 5, 204), size=4)
        d.line((x + 5, 204), (x + 5, 244))
        _arrow(d, (x + 5, 204), (x + 5, 244), size=4)
        d.circle(x, 254, 4)

    d.group('mid')
    d.text(200, 44, 'GRILL', size=7)
    d.text(200, 146, 'DRESS · WRAP', size=7)
    d.text(87, 162, 'FRIES', size=7)
    d.text(313, 162, 'SHAKES', size=7)
    d.text(330, 220, 'ORDER IN', size=7, anchor='end')
    d.text(330, 232, 'FOOD OUT', size=7, anchor='end')
    d.text(70, 226, 'WINDOWS', size=7, anchor='start')
    d.text(200, 284, 'SCHEMATIC · NO COOKING TO ORDER', size=7)
    return d


PLATES = {'supermarket': supermarket, 'fast-food': fast_food}
