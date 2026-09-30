"""Plates for the mathematics subject's last segment, Mathematics now (sprint 024)."""
import math
from plates import D


def _hatch(poly, angle, gap, box):
    """Parallel hatch lines at `angle` degrees, `gap` apart, clipped to a polygon (even-odd)."""
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    nx, ny = -sa, ca                                   # the lines' normal
    x0, y0, x1, y1 = box
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    lo = min(nx * x + ny * y for x, y in corners)
    hi = max(nx * x + ny * y for x, y in corners)
    segs = []
    k = math.ceil(lo / gap)
    while k * gap <= hi:
        c = k * gap
        ts = []
        for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
            da, db = nx * ax + ny * ay - c, nx * bx + ny * by - c
            if (da < 0) != (db < 0):
                u = da / (da - db)
                px, py = ax + u * (bx - ax), ay + u * (by - ay)
                ts.append(ca * px + sa * py)
        ts.sort()
        for t0, t1 in zip(ts[::2], ts[1::2]):
            p = lambda t: (t * ca + c * nx, t * sa + c * ny)
            if t1 - t0 > 1.5:
                segs.append([p(t0 + 0.8), p(t1 - 0.8)])
        k += 1
    return segs


def computer_proof():
    """A map that needs four colours: a centre region ringed by five neighbours.

    The ring is an odd cycle, so it takes three colours (1, 2, 1, 2, 3); the
    centre touches all five and takes a fourth. Left, the map with each colour
    as a hatching; right, the same map as its graph (a wheel), as Kempe and
    Appel and Haken worked with it.
    """
    d = D()
    cx, cy, R, r = 128, 148, 104, 40
    n = 5
    rot = -90
    inner = [(cx + r * math.cos(math.radians(rot + 72 * i)), cy + r * math.sin(math.radians(rot + 72 * i))) for i in range(n)]
    # the ring's dividers run out from the centre's corners, bent a little, as borders are
    def border(i):
        a = math.radians(rot + 72 * i)
        pts = []
        for k in range(9):
            t = k / 8
            rr = r + (R - r) * t
            wob = math.radians(9 * math.sin(math.pi * t) * (1 if i % 2 else -1))
            pts.append((cx + rr * math.cos(a + wob), cy + rr * math.sin(a + wob)))
        return pts
    borders = [border(i) for i in range(n)]
    def outer_arc(i):
        a0 = math.degrees(math.atan2(borders[i][-1][1] - cy, borders[i][-1][0] - cx))
        a1 = math.degrees(math.atan2(borders[(i + 1) % n][-1][1] - cy, borders[(i + 1) % n][-1][0] - cx))
        if a1 < a0:
            a1 += 360
        return [(cx + R * math.cos(math.radians(a0 + (a1 - a0) * k / 24)), cy + R * math.sin(math.radians(a0 + (a1 - a0) * k / 24))) for k in range(25)]
    regions = []
    for i in range(n):
        j = (i + 1) % n
        regions.append(borders[i] + outer_arc(i)[1:-1] + list(reversed(borders[j])))
    colours = [1, 2, 1, 2, 3]

    # the graph: a wheel, one vertex per region
    gx, gy, gr = 312, 148, 62
    ring = [(gx + gr * math.cos(math.radians(rot + 36 + 72 * i)), gy + gr * math.sin(math.radians(rot + 36 + 72 * i))) for i in range(n)]

    d.group('thin')
    # construction: the centre's circumcircle, the spokes' directions, the graph's guide circle,
    # and the dual edges drawn across the map from region to region
    d.circle(cx, cy, r)
    for i in range(n):
        a = math.radians(rot + 72 * i)
        d.line((cx + (r - 14) * math.cos(a), cy + (r - 14) * math.sin(a)), (cx + (R + 8) * math.cos(a), cy + (R + 8) * math.sin(a)))
    d.circle(gx, gy, gr)
    seeds = [(cx + 0.64 * (R + r) * math.cos(math.radians(rot + 36 + 72 * i)), cy + 0.64 * (R + r) * math.sin(math.radians(rot + 36 + 72 * i))) for i in range(n)]
    d.lines([[seeds[i], seeds[(i + 1) % n]] for i in range(n)] + [[(cx, cy), s] for s in seeds])

    d.group()
    # the map: its coast, the centre region and the ring's borders
    d.circle(cx, cy, R)
    d.line(*inner, closed=True)
    d.lines(borders)

    d.group('mid')
    # the colours as hatchings: 1 plain, 2 level, 3 slanting, 4 crossed
    box = (cx - R, cy - R, cx + R, cy + R)
    segs = []
    for poly, c in zip(regions, colours):
        if c == 2:
            segs += _hatch(poly, 0, 6, box)
        elif c == 3:
            segs += _hatch(poly, 45, 5, box)
    segs += _hatch(inner, 45, 5, box) + _hatch(inner, -45, 5, box)
    # leave a clear disc round each colour's numeral
    keep = []
    for sg in segs:
        (x0, y0), (x1, y1) = sg
        pts = [(x0 + (x1 - x0) * t / 30, y0 + (y1 - y0) * t / 30) for t in range(31)]
        run = []
        for p in pts:
            if min(math.hypot(p[0] - q[0], p[1] - q[1]) for q in seeds + [(cx, cy)]) > 10:
                run.append(p)
            elif run:
                keep.append(run); run = []
        if run:
            keep.append(run)
    d.lines([[k[0], k[-1]] for k in keep if len(k) > 1])

    d.group()
    # the graph: rim and spokes
    def edge(p, q, cut=9):
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
        return [(p[0] + cut * ux, p[1] + cut * uy), (q[0] - cut * ux, q[1] - cut * uy)]
    d.lines([edge(ring[i], ring[(i + 1) % n]) for i in range(n)] + [edge((gx, gy), p) for p in ring])
    for x, y in ring + [(gx, gy)]:
        d.circle(x, y, 9)

    d.group('mid')
    for (x, y), c in zip(ring, colours):
        d.text(x, y + 3.2, str(c))
    d.text(gx, gy + 3.2, '4')
    for s, c in zip(seeds, colours):
        d.text(s[0], s[1] + 3.2, str(c), size=8)
    d.text(cx, cy + 3.2, '4', size=8)
    d.text(cx, 272, 'THE MAP', size=7)
    d.text(gx, 272, 'ITS GRAPH', size=7)
    d.text(gx, 52, 'ODD RING · 3 COLOURS', size=7)
    return d


def where_mathematics_is():
    """Circle packing in the plane: squares (π/4) against triangles (π/√12).

    Each packing is drawn with its cell, and the pieces of circle inside the
    cell are hatched. In the square cell, four quarter circles make one whole
    circle in a square of side 2r: π r² / 4r² = π/4. In the triangular cell,
    three sixth-circles make half a circle in a triangle of side 2r, whose
    area is √3 r²: (π r²/2) / √3 r² = π/√12.
    """
    d = D()
    r = 21
    h = math.sqrt(3) * r
    sx0, sy0 = 52, 112                      # square packing, 3 by 3
    sq = [(sx0 + 2 * r * i, sy0 + 2 * r * j) for j in range(3) for i in range(3)]
    hx0, hy0 = 232, 112                     # triangular packing, rows of 3, offset alternately
    hexs = [(hx0 + 2 * r * i + (r if j % 2 else 0), hy0 + h * j) for j in range(3) for i in range(3)]
    cs = sq[0]                              # the square cell's corner
    ta, tb, tc = hexs[0], hexs[1], hexs[3]  # the triangle cell

    def sector(x, y, a0, a1, rad):
        return [(x, y)] + [(x + rad * math.cos(math.radians(a0 + (a1 - a0) * k / 16)),
                            y + rad * math.sin(math.radians(a0 + (a1 - a0) * k / 16))) for k in range(17)]

    d.group('thin')
    # the rows and columns through the centres, and the construction of each cell's corners
    d.lines([[(sx0 - r - 6, sy0 + 2 * r * j), (sx0 + 5 * r + 6, sy0 + 2 * r * j)] for j in range(3)] +
            [[(sx0 + 2 * r * i, sy0 - r - 6), (sx0 + 2 * r * i, sy0 + 5 * r + 6)] for i in range(3)])
    d.lines([[(hx0 - r - 6, hy0 + h * j), (hx0 + 6 * r + 6, hy0 + h * j)] for j in range(3)])
    tri = [(3, 0), (3, 1), (4, 1), (4, 2), (5, 2), (6, 3), (7, 3), (7, 4), (8, 4), (8, 5)]
    d.lines([[hexs[i], hexs[j]] for i, j in tri])
    d.group()
    for x, y in sq + hexs:
        d.circle(x, y, r)
    d.group()
    d.line(cs, (cs[0] + 2 * r, cs[1]), (cs[0] + 2 * r, cs[1] + 2 * r), (cs[0], cs[1] + 2 * r), closed=True)
    d.line(ta, tb, tc, closed=True)
    d.group('mid')
    # the pieces of circle inside each cell, hatched: four quarters, three sixths
    segs = []
    x, y = cs
    for px, py, a0 in [(x, y, 0), (x + 2 * r, y, 90), (x + 2 * r, y + 2 * r, 180), (x, y + 2 * r, 270)]:
        segs += _hatch(sector(px, py, a0, a0 + 90, r), 45, 4, (x - r, y - r, x + 3 * r, y + 3 * r))
    for (px, py), a0 in [(ta, 0), (tb, 120), (tc, 240)]:
        segs += _hatch(sector(px, py, a0, a0 + 60, r), 45, 4, (hx0 - r, hy0 - r, hx0 + 6 * r, hy0 + 3 * h))
    d.lines(segs)
    d.group('mid')
    d.line((sq[8][0], sq[8][1]), (sq[8][0] + r, sq[8][1]))
    d.text(sq[8][0] + r / 2, sq[8][1] - 4, 'r', size=8)
    d.text(sx0 + 2 * r, 64, 'SQUARES', size=7)
    d.text(hx0 + 2.5 * r, 64, 'TRIANGLES', size=7)
    d.text(sx0 + 2 * r, 256, 'π/4 ≈ 0.785')
    d.text(hx0 + 2.5 * r, 256, 'π/√12 ≈ 0.907')
    return d


PLATES = {
    'computer-proof': computer_proof,
    'where-mathematics-is': where_mathematics_is,
}
