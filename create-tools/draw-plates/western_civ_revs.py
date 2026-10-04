"""Plates for western-civ's Revolutions trail (sprint 049, part revs). See plates_for.py."""
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


def glorious_revolution():
    # The Bill of Rights as an argument: the thirteen heads charged against James II ("By ...")
    # on the left, the thirteen rights declared ("That ...") on the right, in the order the act
    # gives them, joined where a right answers a charge. Bail, fines and punishments, three
    # charges, become one right; frequent parliaments answers no charge. Below, the two lists
    # read on 13 February 1689 lead to the crown offered after them.
    d = D()
    n = 13
    y0, dy, h = 40, 14.6, 9
    lx, lw = 34, 96
    rx, rw = 262, 104
    ys = [y0 + i * dy for i in range(n)]
    # charge i -> right j (0-based, in the act's order)
    links = [(0, 0), (0, 1), (1, 4), (2, 2), (3, 3), (4, 5), (5, 6), (6, 7), (7, 8),
             (8, 10), (9, 9), (10, 9), (11, 9), (12, 11)]
    rights = ['SUSPENDING', 'DISPENSING', 'CHURCH COURTS', 'TAXATION', 'PETITION', 'STANDING ARMY',
              'ARMS', 'FREE ELECTIONS', 'FREE SPEECH', 'BAIL · CRUELTY', 'JURIES', 'FORFEITURES',
              'PARLIAMENTS']
    yb = ys[-1] + h + 12                                                  # the bracket under the lists
    crown = (200, 266)

    d.group('thin')
    for y in ys:                                                          # the ruled lines of the text
        d.line((lx - 8, y + h / 2), (lx - 3, y + h / 2))
        d.line((rx + rw + 3, y + h / 2), (rx + rw + 8, y + h / 2))
    d.line((200, 24), (200, yb - 4))                                       # the fold between the lists
    d.line((lx, yb), (rx + rw, yb))

    d.group()
    for y in ys:
        _box(d, lx, y, lw, h)
        _box(d, rx, y, rw, h)

    d.group('mid')
    for i, j in links:                                                    # each charge to its right
        p, q = (lx + lw, ys[i] + h / 2), (rx, ys[j] + h / 2)
        c1, c2 = (p[0] + 50, p[1]), (q[0] - 50, q[1])
        d.curve(f'M{p[0]:.1f} {p[1]:.1f} C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {q[0]:.1f} {q[1]:.1f}')
    # rule lines of writing inside each charge
    for y in ys:
        d.line((lx + 6, y + h / 2), (lx + lw - 6 - 18 * ((int(y) * 7) % 3), y + h / 2))

    d.group()
    # the bracket and the crown, offered after the reading
    d.line((lx + lw / 2, ys[-1] + h), (lx + lw / 2, yb))
    d.line((rx + rw / 2, ys[-1] + h), (rx + rw / 2, yb))
    d.line((200, yb), (200, crown[1] - 16))
    _arrow(d, (200, yb), (200, crown[1] - 16))
    cx, cy = crown
    w, hh = 22, 12
    pts = [(cx - w, cy + hh)]
    for k in range(5):                                                    # five points on the rim
        x = cx - w + k * w / 2
        pts.append((x, cy - hh + (0 if k % 2 == 0 else 6)))
        if k < 4:
            pts.append((x + w / 4, cy + 1))
    pts.append((cx + w, cy + hh))
    d.line(*pts, closed=True)
    d.line((cx - w, cy + hh - 4), (cx + w, cy + hh - 4))

    d.group('mid')
    d.text(lx + lw / 2, 30, 'BY · CHARGED', size=7)
    d.text(rx + rw / 2, 30, 'THAT · DECLARED', size=7)
    for y, s in zip(ys, rights):
        d.text(rx + rw / 2, y + 7, s, size=7)
    for i, y in enumerate(ys):
        d.text(lx - 12, y + 7, str(i + 1), size=7, anchor='end')
    d.text(200, 296, 'CROWN OFFERED · 13 FEB 1689', size=7)
    return d



def haitian_revolution():
    # Left: Saint-Domingue in 1789 as a unit chart, one square to 5,000 people: more than 450,000
    # enslaved (90 squares), about 40,000 whites (8) and some 28,000 free people of color (6,
    # rounded up from 5.6). Right: the indemnity of 1825 to scale, 150 million francs in five
    # installments of 30 million, beside the 90 million it was cut to in 1838, and the Haitian
    # government's revenue in 1825, about a sixth of the first installment (the Times's figure).
    d = D()
    cols, s, g = 10, 13, 2.6                                              # squares per row, size, gap
    x0, y0 = 24, 40
    counts = [('slave', 90), ('free', 6), ('white', 8)]
    cells = []
    for kind, n in counts:
        cells += [kind] * n
    rows = (len(cells) + cols - 1) // cols
    k = 1.2                                                               # px per million francs
    base = 262
    bx = [266, 346]

    d.group('thin')
    for r in range(rows + 1):                                             # the grid's rules
        y = y0 + r * (s + g) - g / 2
        d.line((x0 - 4, y), (x0 + cols * (s + g) + 2, y))
    d.line((250, base), (390, base))
    for m in range(0, 151, 30):                                           # a scale of millions
        y = base - m * k
        d.line((254, y), (260, y))
    d.line((257, base), (257, base - 150 * k))

    d.group()
    for i, kind in enumerate(cells):
        r, c = divmod(i, cols)
        x, y = x0 + c * (s + g), y0 + r * (s + g)
        d.line((x, y), (x + s, y), (x + s, y + s), (x, y + s), closed=True)
    # the indemnity: five installments, then the 1838 sum
    for j in range(5):
        y = base - (j + 1) * 30 * k
        d.line((bx[0], y), (bx[0] + 36, y), (bx[0] + 36, y + 30 * k), (bx[0], y + 30 * k), closed=True)
    for j in range(3):
        y = base - (j + 1) * 30 * k
        d.line((bx[1], y), (bx[1] + 36, y), (bx[1] + 36, y + 30 * k), (bx[1], y + 30 * k), closed=True)

    d.group('mid')
    for i, kind in enumerate(cells):                                      # marks for the free
        r, c = divmod(i, cols)
        x, y = x0 + c * (s + g), y0 + r * (s + g)
        if kind == 'white':
            d.line((x + 2, y + 2), (x + s - 2, y + s - 2))
            d.line((x + s - 2, y + 2), (x + 2, y + s - 2))
        elif kind == 'free':
            d.line((x + 2, y + s - 2), (x + s - 2, y + 2))
    rv = 30 / 6 * k                                                       # the revenue of 1825
    rx0 = bx[0] + 54
    d.line((rx0, base - rv), (rx0 + 8, base - rv), (rx0 + 8, base), (rx0, base), closed=True)
    d.line((rx0 + 4, base + 2), (rx0 + 4, base + 16))

    d.group('mid')
    gx = x0 + cols * (s + g) / 2
    d.text(gx, 28, 'SAINT-DOMINGUE 1789', size=7)
    d.text(gx, y0 + rows * (s + g) + 12, '1 SQUARE = 5,000 PEOPLE', size=7)
    d.text(gx, y0 + rows * (s + g) + 24, 'PLAIN: ENSLAVED', size=7)
    d.text(gx, y0 + rows * (s + g) + 36, '/ FREE OF COLOR · X WHITE', size=7)
    d.text(bx[0] + 18, base + 12, '1825', size=7)
    d.text(bx[1] + 18, base + 12, '1838', size=7)
    d.text(320, 28, 'INDEMNITY · M FRANCS', size=7)
    d.text(bx[0] + 18, base - 150 * k - 6, '150', size=7)
    d.text(bx[1] + 18, base - 90 * k - 6, '90', size=7)
    d.text(rx0 + 4, base + 24, 'REVENUE 1825', size=7)
    return d


def revolutions_of_1848():
    # Left: St. Paul's Church, Frankfurt, in plan, schematic and not to a measured scale: the oval
    # outer wall, the ring of columns that carries the gallery (2,000 spectators), the tribune at
    # one end of the long axis, and rows of seats for the 600 deputies as arcs about it.
    # Right: the vote of 28 March 1849 that made Frederick William IV emperor, to scale:
    # 290 for, 248 abstaining.
    d = D()
    cx, cy, rx, ry = 150, 150, 128, 96
    trib = (cx + rx - 44, cy)

    def ell(a, b, n=96, off=0.0):
        return [(cx + a * math.cos(2 * math.pi * (k + off) / n), cy + b * math.sin(2 * math.pi * (k + off) / n)) for k in range(n)]

    d.group('thin')
    d.line((cx - rx - 10, cy), (cx + rx + 10, cy))                        # the axes
    d.line((cx, cy - ry - 10), (cx, cy + ry + 10))
    k = 0.42                                                              # px per vote
    base = 236
    d.line((292, base), (388, base))
    for v in (0, 100, 200, 300):
        d.line((294, base - v * k), (299, base - v * k))
    d.line((296.5, base), (296.5, base - 300 * k))

    d.group()
    d.line(*ell(rx, ry), closed=True)                                     # the outer wall
    d.line(*ell(rx - 6, ry - 6), closed=True)
    # the tribune and the president's dais at the east end
    tx, ty = trib
    d.line((tx - 6, ty - 14), (tx + 8, ty - 14), (tx + 8, ty + 14), (tx - 6, ty + 14), closed=True)
    # the vote, to scale
    for x, v in ((312, 290), (350, 248)):
        d.line((x, base), (x, base - v * k), (x + 26, base - v * k), (x + 26, base))

    d.group('mid')
    for (x, y) in ell(rx - 26, ry - 22, 20, 0.5):                              # the ring of columns
        d.circle(x, y, 2.6)
    # rows of seats: arcs about the tribune, clipped to the floor inside the columns
    for r in range(36, 200, 13):
        pts = []
        for a in range(100, 261, 4):
            x = tx + r * math.cos(math.radians(a))
            y = ty + r * math.sin(math.radians(a))
            if ((x - cx) / (rx - 34)) ** 2 + ((y - cy) / (ry - 30)) ** 2 <= 1:
                pts.append((x, y))
            elif pts:
                break
        if len(pts) > 2:
            d.line(*pts)

    d.group('mid')
    d.text(cx, cy + ry + 22, 'ST. PAUL\'S CHURCH · PLAN · SCHEMATIC', size=7)
    d.text(cx, cy - ry - 14, 'GALLERY ABOVE THE COLUMNS', size=7)
    d.text(325, base + 12, 'FOR', size=7)
    d.text(363, base + 12, 'ABST.', size=7)
    d.text(325, base - 290 * k - 6, '290', size=7)
    d.text(363, base - 248 * k - 6, '248', size=7)
    d.text(340, base + 26, '28 MARCH 1849', size=7)
    return d


PLATES = {
    'glorious-revolution': glorious_revolution,
    'haitian-revolution': haitian_revolution,
    'revolutions-of-1848': revolutions_of_1848,
}
