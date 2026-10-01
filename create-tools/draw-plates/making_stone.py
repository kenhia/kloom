"""Plates for How We Build's first segment, Stone and fire (sprint 026)."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def knapping():
    d = D()
    ex, ey = 214, 112                    # the core's edge: platform above, exterior face below
    epa = 72                             # exterior platform angle, degrees
    face = _dir(180 - epa)               # the exterior face runs down and back from the edge
    pd = 24                              # platform depth: the blow lands this far in from the edge
    ix, iy = ex - pd, ey                 # the point of impact
    fl = 118                             # the length of the face drawn
    fx, fy = ex + face[0] * fl, ey + face[1] * fl
    d.group('thin')
    # the platform and face produced, the impact line, and the Hertzian cone from the point of impact
    d.line((ex - 196, ey), (ex + 30, ey))
    d.line((ex - face[0] * 26, ey - face[1] * 26), (fx + face[0] * 12, fy + face[1] * 12))
    d.line((ix, ey - 70), (ix, ey + 40))
    for a in (45, 135):
        u = _dir(a)
        d.line((ix, iy), (ix + u[0] * 70, iy + u[1] * 70))
    # platform depth as a dimension line above the platform
    d.line((ix, ey - 14), (ex, ey - 14))
    d.lines([[(ix, ey - 18), (ix, ey - 10)], [(ex, ey - 18), (ex, ey - 10)]])
    # the fracture: down under the bulb, then parallel to the face, then out to meet it (a feather)
    run = fl * 0.72
    pts = []
    for i in range(41):
        t = i / 40
        along = t * run                                # distance down the face
        inset = pd * math.sin(math.radians(epa)) * (1 - t ** 3) + 3 * math.sin(math.pi * t) * (1 - t)
        bx, by = ex + face[0] * along, ey + face[1] * along
        nx, ny = -face[1], face[0]                     # into the block from the face
        pts.append((bx + nx * inset, by + ny * inset))
    pts[0] = (ix, iy)
    d.group()
    # the core in section, with the flake's volume gone from it
    back = (40, ey + 128)
    d.line((60, ey), *pts, (fx, fy), (fx - 36, back[1] + 10), back, (30, ey + 28), closed=True)
    d.group('mid')
    # the flake coming away, drawn out from the face, with its bulb and ripples
    off = (13, 4)
    flake = pts + [(ex, ey)]
    d.line(*[(x + off[0], y + off[1]) for x, y in flake], closed=True)
    d.arc(ix + off[0] + 2, iy + off[1] + 8, 6, -90, 90, n=12)
    for k in (1, 2, 3):
        d.arc(ix + off[0], iy + off[1], 16 * k, 66, 100, n=10)
    # the hammerstone, and the line of the blow
    hx, hy = ix - 2, ey - 46
    d.circle(hx, hy, 15)
    d.line((hx, hy + 17), (ix, iy - 4))
    d.lines([[(ix - 3, iy - 10), (ix, iy - 4), (ix + 3, iy - 10)]])
    # the exterior platform angle, at the edge
    a0, a1 = 180 - epa, 180
    d.arc(ex, ey, 22, a0, a1, n=20)
    d.group('mid')
    # three terminations, each a flake's profile meeting the face
    tx, ty = 300, 70
    for k, name in enumerate(('FEATHER', 'HINGE', 'STEP')):
        y0 = ty + k * 70
        d.line((tx, y0), (tx + 80, y0))                       # the face
        if name == 'FEATHER':
            d.line((tx + 4, y0 - 14), (tx + 30, y0 - 12), (tx + 60, y0 - 5), (tx + 78, y0))
        elif name == 'HINGE':
            d.line((tx + 4, y0 - 14), (tx + 30, y0 - 12), (tx + 52, y0 - 10))
            d.arc(tx + 52, y0 - 5, 5, -90, 90, n=12)
        else:
            d.line((tx + 4, y0 - 14), (tx + 30, y0 - 12), (tx + 50, y0 - 11), (tx + 50, y0))
        d.text(tx + 40, y0 + 16, name, size=8)
    d.text(ix + (ex - ix) / 2, ey - 22, 'PD', size=8)
    d.text(ex - 44, ey + 30, 'EPA', size=8)
    d.text(hx - 34, hy + 3, 'HAMMER', size=8, anchor='end')
    d.text(150, 284, 'THE CORE IN SECTION, A FLAKE COMING AWAY', size=8)
    return d


PLATES = {'knapping': knapping}


def _almond(cx, top, L, m, n=160):
    """The outline of a hand axe in plan: a point at the top, widest about two thirds down, a rounded base."""
    right, left = [], []
    for i in range(n + 1):
        u = i / n
        w = m / 2 * math.sin(math.pi * u ** 1.55) ** (0.8 - 0.42 * u)
        y = top + u * L
        right.append((cx + w, y))
        left.append((cx - w, y))
    return right + left[::-1]


def handaxe():
    d = D()
    s = 1.45                                   # px per mm: the invented hand axe of the table, 140 × 90 × 36 mm
    L, m, e = 140 * s, 90 * s, 36 * s
    cx, top = 128, 44
    outline = _almond(cx, top, L, m)
    # where the outline is widest
    wi = max(range(len(outline) // 2), key=lambda i: outline[i][0])
    wy = outline[wi][1]
    sx = 318                                   # the section, drawn beside the plan on the same horizontal
    d.group('thin')
    d.line((cx, top - 14), (cx, top + L + 14))                       # the axis of symmetry
    d.line((cx - m / 2 - 14, wy), (sx + e / 2 + 14, wy))             # projection of the widest line
    d.line((sx, top - 14), (sx, top + L + 14))
    d.lines([[(cx + 6, top), (sx + 30, top)], [(cx + 6, top + L), (sx + 30, top + L)]])
    # dimension lines: length, width, thickness
    lx = cx - m / 2 - 26
    d.line((lx, top), (lx, top + L))
    d.lines([[(lx - 4, top), (lx + 4, top)], [(lx - 4, top + L), (lx + 4, top + L)]])
    d.line((cx - m / 2, wy + 22), (cx + m / 2, wy + 22))
    d.group()
    d.line(*outline, closed=True)
    # the section: a lens, thickest at the widest line, thinning to the point and the base
    sec_r, sec_l = [], []
    for i in range(41):
        u = i / 40
        y = top + u * L
        h = e / 2 * math.sin(math.pi * u ** 1.3) ** 0.7
        sec_r.append((sx + h, y))
        sec_l.append((sx - h, y))
    d.line(*(sec_r + sec_l[::-1]), closed=True)
    d.group('mid')
    # flake scars in plan: shallow scallops taken in from the edge, all round, on this face
    scars = []
    half = len(outline) // 2
    for k in range(13):
        i = 12 + k * (half - 22) // 12
        for side in (1, -1):
            j = i if side == 1 else len(outline) - 1 - i
            (x0, y0), (x1, y1) = outline[j - 1], outline[j + 1]
            tx, ty = x1 - x0, y1 - y0
            n = math.hypot(tx, ty)
            tx, ty = tx / n, ty / n                    # along the edge
            # the inward normal points from the edge towards the axis
            px, py = -ty, tx
            if (cx - outline[j][0]) * px + (top + 0.55 * L - outline[j][1]) * py < 0:
                px, py = -px, -py
            r = 11 + 4 * math.sin(k * 1.7)
            x, y = outline[j]
            # a scallop: both ends on the edge, its deepest point taken in towards the axis
            scars.append([(x + tx * r * math.sin(math.radians(t)) + px * r * 0.7 * math.cos(math.radians(t)),
                           y + ty * r * math.sin(math.radians(t)) + py * r * 0.7 * math.cos(math.radians(t)))
                          for t in range(-90, 91, 15)])
    d.lines(scars)
    d.group('mid')
    d.text(lx - 6, top + L / 2, 'L', size=9, anchor='end')
    d.text(cx, wy + 36, 'm', size=9)
    d.text(sx + e / 2 + 8, wy - 6, 'e', size=9, anchor='start')
    d.text(cx, 18, 'PLAN', size=8)
    d.text(sx, 18, 'SECTION', size=8)
    d.text(sx, top + L + 30, 'L ÷ m = 1.56', size=8)
    d.text(sx, top + L + 44, 'm ÷ e = 2.5', size=8)
    return d


PLATES['handaxe'] = handaxe


def birch_tar():
    d = D()
    gy = 150                                   # ground line
    cx = 150                                   # the pit's centre
    pw, pd = 54, 92                            # pit half-width and depth
    d.group('thin')
    d.line((14, gy), (290, gy))
    d.line((cx, 22), (cx, gy + pd + 16))
    # temperature levels, read off the right
    for y in (gy - 62, gy - 22, gy + pd - 18):
        d.line((cx + 70, y), (300, y))
    d.group()
    # the pit, with straight sides and a flat floor
    d.line((cx - pw, gy), (cx - pw + 8, gy + pd), (cx + pw - 8, gy + pd), (cx + pw, gy))
    # the earth mound over the bark, and the fire on top of it
    mound = [(cx + 96 * math.cos(math.radians(a)), gy - 52 * math.sin(math.radians(a))) for a in range(0, 181, 6)]
    d.line(*mound)
    d.group('mid')
    # the bark cup at the bottom of the pit
    d.line((cx - 18, gy + pd - 30), (cx - 14, gy + pd - 4), (cx + 14, gy + pd - 4), (cx + 18, gy + pd - 30))
    d.line((cx - 12, gy + pd - 12), (cx + 12, gy + pd - 12))           # the tar collected
    # the mesh over the pit
    d.line((cx - pw - 4, gy - 2), (cx + pw + 4, gy - 2))
    d.lines([[(cx - pw + 6 * k, gy - 5), (cx - pw + 6 * k + 3, gy + 1)] for k in range(19)])
    # the loose roll of bark on the mesh: a spiral in section
    sp = []
    for i in range(140):
        a = i * 0.16
        r = 2 + a * 1.5
        sp.append((cx + r * math.cos(a), gy - 22 + r * 0.8 * math.sin(a)))
    d.line(*sp)
    # drips of tar from the roll into the cup
    d.lines([[(cx - 4 + 4 * k, gy + 8 + 10 * j), (cx - 4 + 4 * k, gy + 13 + 10 * j)] for k in range(3) for j in range(5)])
    # the fire: flames on the crest of the mound
    flames = []
    for k in range(5):
        x0 = cx - 40 + 20 * k
        flames.append([(x0 - 7, gy - 50 + abs(k - 2) * 4), (x0 - 2, gy - 66 + abs(k - 2) * 4),
                       (x0 + 1, gy - 58 + abs(k - 2) * 4), (x0 + 4, gy - 72 + abs(k - 2) * 4),
                       (x0 + 7, gy - 50 + abs(k - 2) * 4)])
    d.lines(flames)
    d.group('mid')
    # the hafted tool: a flake set in a split stick, bound with a collar of tar
    hx, hy = 62, 62
    d.line((hx - 54, hy + 30), (hx + 4, hy - 4))                           # the shaft
    d.line((hx - 50, hy + 36), (hx + 8, hy + 2))
    d.line((hx + 2, hy - 6), (hx + 40, hy - 32), (hx + 26, hy + 2), (hx + 8, hy + 4), closed=True)  # the flake
    d.ellipse(hx + 4, hy, 10, 7)                                           # the tar collar
    d.group('mid')
    d.text(306, gy - 66, '> 400 °C', size=8, anchor='start')
    d.text(306, gy - 26, '250–450 °C', size=8, anchor='start')
    d.text(306, gy + pd - 22, '< 150 °C', size=8, anchor='start')
    d.text(cx, 16, 'FIRE ON EARTH', size=8)
    d.text(cx - 96, gy - 8, 'BARK ROLL', size=7, anchor='end')  # at 8, off the plate's left edge
    d.text(cx - 26, gy + pd - 8, 'TAR', size=8, anchor='end')
    d.text(hx - 14, hy + 54, 'HAFTED', size=8)
    return d


PLATES['birch-tar'] = birch_tar
