"""Plates for The Story of Life's part mol1 (sprint 055): griffith, avery, hershey-chase. See plates_for.py."""
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


def _mouse(d, cx, cy, dead=False):
    """A mouse in profile, as geometry: an elliptical body, a head circle, an ear, a tail on a sine.
    A dead one lies on its back, feet up."""
    s = -1 if dead else 1
    d.ellipse(cx, cy, 22, 11)                                             # body
    hx, hy = cx + 25, cy - s * 3
    d.circle(hx, hy, 7)                                                   # head
    d.line((hx + 6, hy - s * 1), (hx + 12, hy + s * 1), (hx + 6, hy + s * 4))  # snout
    d.circle(hx - 2, hy - s * 8, 3.5)                                     # ear
    tail = [(cx - 22 - k * 3, cy + s * (2 + 4 * math.sin(k / 2.2))) for k in range(13)]
    d.line(*tail)                                                         # tail
    for fx in (cx - 12, cx - 4, cx + 6, cx + 14):                         # legs
        y0 = cy + s * 9
        d.line((fx, y0), (fx + (1 if dead else 0), y0 + s * 7))
    if dead:                                                              # crossed eye
        ex, ey = hx + 2, hy + 1
        d.line((ex - 2, ey - 2), (ex + 2, ey + 2))
        d.line((ex - 2, ey + 2), (ex + 2, ey - 2))
    else:
        d.circle(hx + 2, hy - 1, 0.8)


def _dish(d, cx, cy, kind):
    """A plate of colonies: rough (small, ragged), smooth (large, round) or none."""
    d.ellipse(cx, cy, 20, 6)
    d.ellipse(cx, cy - 2, 20, 6)
    if kind == 'R':
        for k, (dx, dy) in enumerate(((-9, -1), (-2, 1), (6, -2), (11, 1), (2, -3))):
            pts = []
            for j in range(9):
                a = 2 * math.pi * j / 8
                r = 2.2 + 0.7 * ((j + k) % 2)
                pts.append((cx + dx + r * math.cos(a), cy - 2 + dy + 0.5 * r * math.sin(a)))
            d.line(*pts)
    elif kind == 'S':
        for dx, dy in ((-8, -1), (3, 0), (11, -2)):
            d.ellipse(cx + dx, cy - 2 + dy, 4.5, 2)


def griffith():
    d = D()
    # Griffith's mice as the textbooks group them: four cells, each an injection and its outcome, with the
    # plate of colonies from the mouse. Live R and heated S each harmless; together the mouse dies and its
    # blood grows smooth (capsulated) pneumococci of the heated strain's type. Types as in his Table VII.
    cols, rows = (106, 300), (90, 212)
    d.group('thin')
    d.line((200, 40), (200, 272))                                         # the grid
    d.line((20, 152), (380, 152))
    for x in cols:
        for y in rows:
            d.line((x + 40, y - 4), (x + 54, y - 4))                      # mouse to dish
    d.group()
    cells = [(cols[0], rows[0], False, 'R'), (cols[1], rows[0], True, 'S'),
             (cols[0], rows[1], False, None), (cols[1], rows[1], True, 'S')]
    for x, y, dead, colonies in cells:
        _mouse(d, x - 20, y, dead)
    d.group('mid')
    for x, y, dead, colonies in cells:
        _dish(d, x + 76, y - 2, colonies)
        _arrow(d, (x + 40, y - 4), (x + 54, y - 4), size=3)
    d.group('mid')
    labels = [('LIVE R  (FROM TYPE II)', 'LIVES · R ONLY, LOCAL'),
              ('LIVE S  TYPE I', 'DIES · S TYPE I'),
              ('S TYPE I  HEATED 60 °C', 'LIVES · STERILE'),
              ('LIVE R + HEATED S I', 'DIES · S TYPE I IN BLOOD')]
    for (x, y, dead, colonies), (inj, out) in zip(cells, labels):
        d.text(x, y - 34, inj, size=7)
        d.text(x, y + 34, out, size=7)
    d.text(200, 22, 'FOUR GROUPS OF MICE · AFTER GRIFFITH 1928', size=7)
    d.text(200, 292, 'INJECTED UNDER THE SKIN · COLONIES FROM THE MOUSE', size=7)
    return d


def _tube(d, cx, top, h=30, w=10):
    d.line((cx - w / 2, top), (cx - w / 2, top + h - w / 2))
    d.line((cx + w / 2, top), (cx + w / 2, top + h - w / 2))
    d.arc(cx, top + h - w / 2, w / 2, 0, 180, n=16)


def avery():
    d = D()
    # The purification of the transforming principle as Avery, MacLeod and McCarty (1944) give it, as a
    # flow: Type III culture to fibrous fraction; then the fraction split three ways among enzymes, each
    # tube seeded with the R strain and read as transformed (S III) or not (R only).
    steps = [('75 L', 'TYPE III'), ('HEAT', '65 °C'), ('DEOXY-', 'CHOLATE'), ('CHLORO-', 'FORM'),
             ('SUGAR', 'ENZYME'), ('ALCOHOL', '×5')]
    x0, dx, y = 36, 66, 70
    xs = [x0 + i * dx for i in range(len(steps))]
    d.group('thin')
    d.line((20, y + 22), (390, y + 22))
    for x in xs:
        d.line((x, y + 18), (x, y + 26))
    d.line((xs[-1], y + 26), (xs[-1], 150))
    d.line((90, 150), (310, 150))
    d.group()
    for x in xs:
        _box(d, x - 28, y - 14, 56, 28)
    for a, b in zip(xs, xs[1:]):
        d.line((a + 28, y), (b - 28, y))
        _arrow(d, (a + 28, y), (b - 28, y), size=4)
    # the fibrous fraction winding on the rod
    rx = xs[-1]
    d.line((rx, y - 40), (rx, y - 18))
    d.group('mid')
    for k in range(7):
        yy = y - 38 + k * 3
        d.ellipse(rx, yy, 4, 1.2)
    tubes = [(90, 'TRYPSIN', 'S III'), (200, 'RIBONUCLEASE', 'S III'), (310, 'DNA DEPOLYMERASE', 'R ONLY')]
    for x, enz, res in tubes:
        d.line((x, 150), (x, 168))
        _arrow(d, (x, 150), (x, 168), size=4)
    d.group()
    for x, enz, res in tubes:
        _tube(d, x, 176, h=50, w=16)
    d.group('mid')
    for x, enz, res in tubes:
        if res == 'S III':                                               # diffuse growth: S cells
            for k in range(9):
                d.circle(x - 4 + (k % 3) * 4, 196 + (k // 3) * 8, 1.2)
        else:                                                            # agglutinated R settle out
            for k in range(5):
                d.circle(x - 4 + k * 2, 219 - (k % 2) * 2, 1.2)
    d.group('mid')
    for x, (a, b) in zip(xs, steps):
        d.text(x, y - 2, a, size=7)
        d.text(x, y + 8, b, size=7)
    d.text(rx, y - 46, 'FIBERS', size=7)
    for x, enz, res in tubes:
        d.text(x, 244, enz, size=7)
        d.text(x, 256, res, size=7)
    d.text(200, 22, 'PURIFICATION, THEN THE ENZYME TESTS · 1944', size=7)
    d.text(200, 286, 'R CELLS FROM TYPE II IN EVERY TUBE', size=7)
    return d


def _phage(d, ax, ay, ang, full=True, scale=1.0):
    """A T-even phage drawn by geometry: an elongated hexagonal head, a tail tube and splayed fibers.
    (ax, ay) is the tail tip; ang is the direction from tip to head, in degrees."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)                                    # along the phage
    vx, vy = -uy, ux                                                     # across it
    s = scale
    tail = 22 * s
    hx, hy = ax + ux * tail, ay + uy * tail                              # head base
    d.line((ax + vx * 2.5 * s, ay + vy * 2.5 * s), (hx + vx * 2.5 * s, hy + vy * 2.5 * s))
    d.line((ax - vx * 2.5 * s, ay - vy * 2.5 * s), (hx - vx * 2.5 * s, hy - vy * 2.5 * s))
    w, h1, h2 = 11 * s, 9 * s, 28 * s                                    # head half-width, shoulders, length
    pts = [(0, 0), (w, h1), (w, h2 - h1), (0, h2), (-w, h2 - h1), (-w, h1)]
    head = [(hx + ux * p + vx * q, hy + uy * p + vy * q) for q, p in pts]
    d.line(*head, closed=True)
    for side in (-1, 1):                                                 # tail fibers
        k = (ax + vx * side * 2 * s, ay + vy * side * 2 * s)
        m = (k[0] + vx * side * 9 * s + ux * 6 * s, k[1] + vy * side * 9 * s + uy * 6 * s)
        e = (m[0] + vx * side * 5 * s - ux * 8 * s, m[1] + vy * side * 5 * s - uy * 8 * s)
        d.line(k, m, e)
    if full:                                                             # DNA packed in the head
        cx, cy = hx + ux * h2 / 2, hy + uy * h2 / 2
        pts = []
        for j in range(40):
            t = j / 39 * 6 * math.pi
            r = 6 * s * (1 - j / 60)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t) * 1.5))
        d.line(*pts)
    return head


def hershey_chase():
    d = D()
    # A bacterium in section with T2 phages on its wall. Two are still whole, DNA packed in their heads. Two
    # have injected their DNA (the P-32 label), which coils inside the cell, and the blender has sheared their
    # empty protein coats (the S-35 label) off the wall. Right: the tube after spinning, the coats in the
    # fluid, the infected cells in the pellet. Schematic; not to scale (a T2 is about a fifth of a micron).
    cx, cy, rx, ry = 138, 206, 112, 56

    def wall(t):
        a = math.radians(t)
        return cx + rx * math.cos(a), cy + ry * math.sin(a)

    def normal(t):                                                       # outward normal at parameter t
        a = math.radians(t)
        nx, ny = math.cos(a) / rx, math.sin(a) / ry
        n = math.hypot(nx, ny)
        return math.degrees(math.atan2(ny / n, nx / n))

    d.group('thin')
    d.line((290, 40), (290, 284))
    d.line((cx - rx - 8, cy), (cx + rx + 8, cy))
    d.line((cx, cy - ry - 6), (cx, cy + ry + 6))
    whole, emptied = (-146, -118), (-80, -46)
    for t in emptied:                                                    # where each coat sat on the wall
        x, y = wall(t)
        n = math.radians(normal(t))
        d.line((x, y), (x + 30 * math.cos(n), y + 30 * math.sin(n)))
    d.group()
    d.ellipse(cx, cy, rx, ry)                                            # the cell wall
    d.ellipse(cx, cy, rx - 5, ry - 5)
    for t in whole:
        x, y = wall(t)
        _phage(d, x, y, normal(t), full=True, scale=0.9)
    for t in emptied:                                                    # the sheared coats, lifted off
        x, y = wall(t)
        n = normal(t)
        a = math.radians(n)
        _phage(d, x + 30 * math.cos(a), y + 30 * math.sin(a), n + 18, full=False, scale=0.9)
    d.group('mid')
    for t in emptied:                                                    # injected DNA coiling into the cell
        x, y = wall(t)
        a = math.radians(normal(t) + 180)
        pts = []
        for j in range(70):
            u = j / 69
            bx, by = x + math.cos(a) * 44 * u, y + math.sin(a) * 44 * u
            r = 2 + 6 * u
            pts.append((bx + r * math.cos(10 * math.pi * u), by + r * math.sin(10 * math.pi * u)))
        d.line(*pts)
    for t in emptied:                                                    # shear arrows
        x, y = wall(t)
        a = math.radians(normal(t) + 90)
        p = (x - 14 * math.cos(a) + 8, y - 14 * math.sin(a) - 16)
        q = (x + 14 * math.cos(a) + 8, y + 14 * math.sin(a) - 16)
        d.line(p, q)
        _arrow(d, p, q, size=3.5)
    # the tube after spinning
    tx, top, bot, w = 340, 62, 250, 22
    d.group()
    d.line((tx - w, top), (tx - w, bot - w))
    d.line((tx + w, top), (tx + w, bot - w))
    d.arc(tx, bot - w, w, 0, 180, n=24)
    d.group('mid')
    d.line((tx - w, 90), (tx + w, 90))                                   # fluid surface
    for k in range(7):                                                   # coats in the fluid
        _phage(d, tx - 9 + (k % 2) * 17, 104 + k * 13, -90 + (k % 3 - 1) * 30, full=False, scale=0.32)
    for k in range(9):                                                   # infected cells in the pellet
        row = k // 3
        d.ellipse(tx - 10 + (k % 3) * 10, bot - 30 + row * 6 - (k % 3 == 1) * 1, 4.5, 2.2)
    d.group('mid')
    d.text(cx, 32, 'T2 ON E. COLI · AFTER THE BLENDER', size=7)
    d.text(196, 58, 'EMPTY COATS · S-35', size=7)
    d.text(cx - 6, cy + 30, 'DNA · P-32', size=7)
    d.text(cx, cy + ry + 18, 'BACTERIUM IN SECTION', size=7)
    d.text(tx, 50, 'SPUN', size=7)
    d.text(314, 150, 'S-35', size=7, anchor='end')
    d.text(314, bot - 22, 'P-32', size=7, anchor='end')
    d.text(tx, 268, 'FLUID · PELLET', size=7)
    return d


PLATES = {'griffith': griffith, 'avery': avery, 'hershey-chase': hershey_chase}
