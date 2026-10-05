"""Plates for Daily Bread's part keep3 (sprint 051): pure-food and birdseye. See plates_for.py."""
import math
import random
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def _oval(cx, cy, rx, ry, angle, n=20):
    """Points round a turned ellipse."""
    c, s = math.cos(angle), math.sin(angle)
    return [(cx + rx * math.cos(t) * c - ry * math.sin(t) * s,
             cy + rx * math.cos(t) * s + ry * math.sin(t) * c)
            for t in (2 * math.pi * i / n for i in range(n))]


def _hexagon(cx, cy, r, turn=0.0):
    return [(cx + r * math.cos(turn + math.pi * i / 3), cy + r * math.sin(turn + math.pi * i / 3)) for i in range(6)]


def pure_food():
    d = D()
    # Two fields under the microscope at 140 diameters, after Hassall, Food and Its Adulterations (1855),
    # figs. 1-5: roasted coffee, a mass of angular cells that adhere and break into pieces, holding drops
    # of oil; roasted chicory root, loose oil-free cells that separate readily, crossed by a bundle of
    # dotted ("interrupted spiral") vessels. The cell layouts are generated (seeded), not traced.
    rng = random.Random(51)
    R = 82
    left, right, cy = (108, 140), (292, 140), 140

    d.group('thin')
    for cx, _ in (left, right):
        d.line((cx - R - 8, cy), (cx + R + 8, cy))
        d.line((cx, cy - R - 8), (cx, cy + R + 8))

    d.group()
    for cx, _ in (left, right):
        d.circle(cx, cy, R)

    # coffee: a jittered grid of shared vertices, so the cells adhere in one mass
    d.group('mid')
    step = 15
    n = int(2 * R / step) + 2
    x0, y0 = left[0] - R, cy - R
    vert = {(i, j): (x0 + i * step + rng.uniform(-4, 4), y0 + j * step + rng.uniform(-4, 4))
            for i in range(n) for j in range(n)}
    inside = lambda p: math.dist(p, (left[0], cy)) < R - 3
    segs = []
    for (i, j), p in vert.items():
        for q in (vert.get((i + 1, j)), vert.get((i, j + 1))):
            if q and inside(p) and inside(q):
                segs.append([p, q])
    d.lines(segs)

    d.group('mid')
    for i in range(n - 1):                                                 # drops of oil in some cells
        for j in range(n - 1):
            corners = [vert[(i, j)], vert[(i + 1, j)], vert[(i + 1, j + 1)], vert[(i, j + 1)]]
            if all(inside(c) for c in corners) and rng.random() < 0.45:
                mx = sum(c[0] for c in corners) / 4
                my = sum(c[1] for c in corners) / 4
                d.circle(mx + rng.uniform(-2, 2), my + rng.uniform(-2, 2), rng.uniform(1.2, 2.2))

    # chicory: a band of dotted vessels across the field, and loose cells either side of it
    d.group()
    ang = math.radians(-28)
    ux, uy = math.cos(ang), math.sin(ang)                                  # along the vessels
    nx, ny = -uy, ux                                                       # across them
    cxr = right[0]
    half = R - 4
    walls = []
    for off in (-14, -5, 5, 14):
        a = (cxr + off * nx - half * ux, cy + off * ny - half * uy)
        b = (cxr + off * nx + half * ux, cy + off * ny + half * uy)
        # clip to the field
        pts = [(a[0] + (b[0] - a[0]) * t / 40, a[1] + (b[1] - a[1]) * t / 40) for t in range(41)]
        pts = [p for p in pts if math.dist(p, (cxr, cy)) < R - 3]
        walls.append(pts)
    d.lines(walls)

    d.group('mid')
    pits = []
    for lo, hi in ((-14, -5), (5, 14)):                                    # the "dotted" walls: short bars
        for t in range(-70, 71, 5):
            p = (cxr + t * ux + lo * nx + 1.5 * nx, cy + t * uy + lo * ny + 1.5 * ny)
            q = (cxr + t * ux + hi * nx - 1.5 * nx, cy + t * uy + hi * ny - 1.5 * ny)
            if math.dist(p, (cxr, cy)) < R - 4 and math.dist(q, (cxr, cy)) < R - 4:
                pits.append([p, q])
    d.lines(pits)
    placed = []
    for _ in range(4000):                                                  # loose cells, kept apart
        a = rng.uniform(0, 2 * math.pi)
        rho = math.sqrt(rng.random()) * (R - 12)
        x, y = cxr + rho * math.cos(a), cy + rho * math.sin(a)
        across = (x - cxr) * nx + (y - cy) * ny
        if abs(across) < 22:
            continue
        rx, ry = rng.uniform(7, 11), rng.uniform(3.5, 5)
        if all(math.dist((x, y), (px, py)) > rx + prx + 3 for px, py, prx in placed):
            placed.append((x, y, rx))
            d.line(*_oval(x, y, rx, ry, ang + rng.uniform(-0.5, 0.5)), closed=True)
        if len(placed) >= 30:
            break

    d.group('mid')
    d.text(left[0], 248, 'ROASTED COFFEE', size=7)
    d.text(left[0], 259, 'CELLS ADHERE · OIL DROPS', size=7)
    d.text(right[0], 248, 'ROASTED CHICORY', size=7)
    d.text(right[0], 259, 'LOOSE CELLS · DOTTED VESSELS', size=7)
    d.text(200, 34, 'GROUND "COFFEE" UNDER THE MICROSCOPE · ×140', size=7)
    d.text(200, 284, 'AFTER HASSALL · THE LANCET · 1851–54', size=7)
    return d


def birdseye():
    d = D()
    # Left: a multiplate freezer in section, after Hall and Birdseye's patent (US 1,822,123, 1931) and the
    # Library of Congress's account: hollow metal plates chilled to -25 F by evaporating ammonia, cartons
    # about two inches thick pressed between them and frozen from both faces. Plate count and proportions
    # are schematic. Right: cells frozen slowly (large crystals outside the cells, which shrink and tear)
    # and quickly (many small crystals within and between them), drawn schematically.
    x0, x1 = 52, 228
    tops = [70, 112, 154, 196, 238]                                        # plate tops
    th = 10                                                                # plate thickness
    d.group('thin')
    d.line((x0 - 22, 34), (x0 - 22, 262))                                  # ammonia header
    d.line((40, 262), (240, 262))                                          # floor
    for t in tops:
        d.line((x0 - 10, t + th / 2), (x1 + 6, t + th / 2))                # each plate's centerline

    d.group()
    d.line((x0 - 14, 52), (x0 - 14, 262))                                  # the frame's columns
    d.line((x1 + 14, 52), (x1 + 14, 262))
    _box(d, x0 - 18, 46, x1 - x0 + 36, 6)                                  # the crosshead
    _box(d, 120, 22, 40, 24)                                               # the press cylinder
    d.line((140, 52), (140, tops[0]))                                      # the ram
    for t in tops:
        _box(d, x0, t, x1 - x0, th)                                        # hollow plates

    d.group('mid')
    for t in tops:                                                         # the coolant channel in each plate
        pts = []
        for k in range(11):
            x = x0 + 8 + k * (x1 - x0 - 16) / 10
            pts += [(x, t + 2.5), (x, t + th - 2.5)] if k % 2 == 0 else [(x, t + th - 2.5), (x, t + 2.5)]
        d.line(*pts)
    for t in tops[:-1]:                                                    # cartons between the plates
        for k in range(3):
            _box(d, x0 + 6 + k * 57, t + th, 50, 32)
    for t in tops:                                                         # hoses from the header
        d.curve(f'M{x0 - 22} {t - 4} C{x0 - 12} {t - 4} {x0 - 12} {t + th / 2} {x0} {t + th / 2}')
    _arrow(d, (140, 56), (140, 66), size=5)
    d.line((x0 - 22, 30), (x0 - 22, 40))
    _arrow(d, (x0 - 22, 30), (x0 - 22, 40), size=4)

    # right: two magnified groups of cells
    def cells(ox, oy, shrink):
        out = []
        for i in range(3):
            for j in range(2):
                cx, cy = ox + 18 + i * 34, oy + 16 + j * 30
                w, h = 15 - shrink, 12 - shrink
                bow = shrink * 0.35
                out.append([(cx - w, cy - h), (cx, cy - h + bow), (cx + w, cy - h), (cx + w - bow, cy),
                            (cx + w, cy + h), (cx, cy + h - bow), (cx - w, cy + h), (cx - w + bow, cy),
                            (cx - w, cy - h)])
        return out

    d.group()
    d.lines(cells(268, 66, 4))                                             # slow: shrunken, pinched cells
    d.lines(cells(268, 178, 0))                                            # quick: whole cells

    d.group('mid')
    for gx in (268 + 35, 268 + 69):                                        # slow: large crystals between cells
        for gy in (66 + 16, 66 + 46, 66 + 31):
            d.line(*_hexagon(gx, gy, 7.5, turn=0.3), closed=True)
    rng = random.Random(1924)
    for _ in range(70):                                                    # quick: many small crystals
        x, y = rng.uniform(272, 366), rng.uniform(182, 234)
        d.line(*_hexagon(x, y, 1.3), closed=True)

    d.group('mid')
    d.text(140, 18, 'PRESS', size=7)
    d.text(x0 - 22, 280, 'AMMONIA', size=7)
    d.text(140, 280, 'PLATES −25 °F · CARTONS 2 IN', size=7)
    d.text(318, 58, 'FROZEN SLOWLY', size=7)
    d.text(318, 140, 'LARGE CRYSTALS', size=7)
    d.text(318, 170, 'FROZEN QUICKLY', size=7)
    d.text(318, 252, 'SMALL CRYSTALS', size=7)
    return d


PLATES = {'pure-food': pure_food, 'birdseye': birdseye}
