"""Plates for How We Build's trail Slicers and supports (sprint 026)."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _polygon(cx, cy, r, n, start=-90):
    """The corners of a regular n-gon inscribed in a circle of radius r, first corner at `start` degrees."""
    return [(cx + r * math.cos(math.radians(start + 360 * k / n)),
             cy + r * math.sin(math.radians(start + 360 * k / n))) for k in range(n)]


def _stadium(cx, cy, w, h, n=8):
    """A bead in section: a rectangle w wide and h high with a semicircle at each end (Slic3r's model)."""
    r = h / 2
    pts = []
    for i in range(n + 1):                                   # right end, top to bottom
        a = -90 + 180 * i / n
        pts.append((cx + w / 2 - r + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))
    for i in range(n + 1):                                   # left end, bottom to top
        a = 90 + 180 * i / n
        pts.append((cx - w / 2 + r + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))
    return pts


def stl_meshes():
    d = D()
    cx, cy, r = 118, 150, 96                   # the true circle: Ken's magnet pocket, drawn at about 7.6 px per mm
    n = 12                                     # an exaggerated tessellation, so the chord error shows
    poly = _polygon(cx, cy, r, n, start=-90 - 180 / n)
    k = 0                                      # the facet enlarged: the one at the top
    a0, a1 = -90 - 180 / n, -90 + 180 / n
    p0, p1 = poly[0], poly[1]
    mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    d.group('thin')
    d.circle(cx, cy, r)                                                  # the curve the CAD model holds
    for p in (p0, p1):
        d.line((cx, cy), p)                                              # the radii to the facet's corners
    d.line((cx, cy), (cx, cy - r - 10))                                  # the bisector through the sagitta
    d.line((cx - r - 12, cy), (cx + r + 12, cy))
    # the detail: the top facet and its arc, enlarged four times beside the circle
    s = 4.0
    dx, dy = 300, 92                            # where the facet's midpoint lands in the detail
    arc = [(dx + s * (cx + r * math.cos(math.radians(a)) - mid[0]),
            dy + s * (cy + r * math.sin(math.radians(a)) - mid[1]))
           for a in [a0 + (a1 - a0) * i / 40 for i in range(41)]]
    d.line(*arc)
    d.line((cx + 30, cy - r + 10), (dx - 70, dy - 6))                    # a leader from the facet to its detail
    d.group()
    d.line(*poly, closed=True)                                           # the facets an STL file stores
    q0 = (dx + s * (p0[0] - mid[0]), dy + s * (p0[1] - mid[1]))
    q1 = (dx + s * (p1[0] - mid[0]), dy + s * (p1[1] - mid[1]))
    d.line(q0, q1)
    d.group('mid')
    # the sagitta in the detail, from the chord's midpoint up to the arc, with ticks
    top = (dx, dy - s * (r - (cy - mid[1])))
    d.line((dx, dy), top)
    d.lines([[(dx - 4, dy), (dx + 4, dy)], [(dx - 4, top[1]), (dx + 4, top[1])]])
    # the half-angle π/n at the centre
    d.arc(cx, cy, 26, -90, -90 + 180 / n, n=12)
    # one facet of a mesh in perspective, its corners numbered anticlockwise and its normal standing out of it
    tx, ty = 300, 222
    tri = [(tx - 46, ty + 34), (tx + 50, ty + 22), (tx + 6, ty - 26)]
    d.line(*tri, closed=True)
    c = (sum(p[0] for p in tri) / 3, sum(p[1] for p in tri) / 3)
    d.line(c, (c[0] - 10, c[1] - 56))
    d.lines([[(c[0] - 15, c[1] - 47), (c[0] - 10, c[1] - 56), (c[0] - 4, c[1] - 48)]])
    d.arc(c[0], c[1] + 4, 14, 200, 470, n=24)                             # the winding, anticlockwise from outside
    d.group('mid')
    d.text(dx + 10, (dy + top[1]) / 2 + 3, 's', size=9, anchor='start')
    d.text(dx, dy + 18, 'CHORD', size=8)
    d.text(dx, top[1] - 8, 'ARC', size=8)
    d.text(cx + 14, cy - 32, 'π/n', size=8, anchor='start')
    d.text(cx, cy + r + 22, 'r = 12.625 MM · n = 12', size=8)
    for (x, y), lab in zip(tri, ('1', '2', '3')):
        d.text(x + (-8 if lab == '1' else 8 if lab == '2' else 0), y + (10 if lab != '3' else -6), lab, size=8)
    d.text(c[0] - 14, c[1] - 60, 'N', size=9, anchor='end')
    d.text(dx, 30, 's = r(1 − cos π/n)', size=8)
    return d


PLATES = {'stl-meshes': stl_meshes}


def slicing():
    d = D()
    # elevation: a faceted cone frustum, standing on the bed, cut by evenly spaced planes
    bx, by = 104, 250                           # centre of the base on the bed
    rb, rt, H = 74, 34, 170                     # base and top half-widths, height
    zs = [by - H * i / 14 for i in range(15)]  # fourteen layers, exaggerated
    cut = 9                                     # the layer drawn in plan
    zc = zs[cut]
    half = lambda z: rb + (rt - rb) * (by - z) / H
    d.group('thin')
    d.line((14, by), (196, by))                                      # the bed
    for z in zs[1:]:
        d.line((bx - half(z) - 10, z), (bx + half(z) + 10, z))       # the slicing planes
    d.line((bx, by + 8), (bx, by - H - 14))
    # projection from the cut plane across to the plan
    d.line((bx + half(zc) + 10, zc), (226, zc))
    d.group()
    # the frustum's outline and its facet edges seen in elevation (eight facets round)
    d.line((bx - rb, by), (bx - rt, by - H), (bx + rt, by - H), (bx + rb, by), closed=True)
    fe = []
    for k in range(1, 4):
        u = math.cos(math.pi * k / 4)
        fe.append([(bx + rb * u, by), (bx + rt * u, by - H)])
    d.lines(fe)
    d.group('mid')
    d.line((bx - half(zc), zc), (bx + half(zc), zc))                 # the plane that is cut, heavier
    # plan of that layer: the octagon the plane cuts from the facets, two perimeters and 45° infill
    px, py, R = 300, 150, 72
    oct_ = _polygon(px, py, R, 8, start=-90 + 22.5)
    d.group()
    d.line(*oct_, closed=True)
    d.group('mid')
    inner = []
    for off in (7, 14):
        loop = _polygon(px, py, R - off / math.cos(math.pi / 8), 8, start=-90 + 22.5)
        d.line(*loop, closed=True)
        inner = loop
    # infill: lines at 45° clipped to the inner perimeter (an octagon: clip by its half-planes)
    ri = R * math.cos(math.pi / 8) - 14 - 3        # inradius of the inner loop, less a little overlap
    segs = []
    for j in range(-6, 7):
        c = j * 11.0                                   # offset of the line x − y = c, through the centre
        # parametrise along the line's direction (1, 1)/√2, from a point on it nearest the centre
        ox, oy = px + c / 2, py - c / 2
        ux, uy = 1 / math.sqrt(2), 1 / math.sqrt(2)
        tmin, tmax = -200, 200
        for k in range(8):
            a = math.radians(-90 + 45 * k)             # the inner octagon's side normals
            nx, ny = math.cos(a), math.sin(a)
            dn = ux * nx + uy * ny
            base = (ox - px) * nx + (oy - py) * ny
            if abs(dn) < 1e-9:
                if base > ri:
                    tmin, tmax = 1, 0
                continue
            t = (ri - base) / dn
            if dn > 0:
                tmax = min(tmax, t)
            else:
                tmin = max(tmin, t)
        if tmax > tmin:
            segs.append([(ox + ux * tmin, oy + uy * tmin), (ox + ux * tmax, oy + uy * tmax)])
    d.lines(segs)
    # the nozzle, above the start of the outer perimeter
    nx0, ny0 = oct_[0]
    d.line((nx0 - 6, ny0 - 20), (nx0 + 6, ny0 - 20), (nx0 + 2, ny0 - 6), (nx0 - 2, ny0 - 6), closed=True)
    d.group('mid')
    d.text(bx, 24, 'ELEVATION', size=8)
    d.text(px, 24, 'PLAN OF ONE LAYER', size=8)
    d.text(px, py + R + 26, 'PERIMETERS · INFILL', size=8)
    d.text(bx, by + 22, 'BED', size=8)
    return d


PLATES['slicing'] = slicing


def supports():
    d = D()
    s = 130                                     # px per mm in the bead section: a 0.45 mm bead is 58.5 px wide
    w, h = 0.45 * s, 0.2 * s
    off = w / 2                                 # each layer steps out by half a bead
    x0, y0 = 30, 250                            # the first bead's left end, on the layer below
    n = 5
    d.group('thin')
    # the layer lines and the line of the overhang through the beads' outer edges
    for i in range(n + 1):
        y = y0 - i * h
        d.line((x0 - 10, y), (x0 + w + n * off + 12, y))
    xa, ya = x0 + w, y0                         # the outer edge of the first bead, at its foot
    xb, yb = x0 + w + (n - 1) * off, y0 - (n - 1) * h - h
    d.line((xa, ya), (xa + (xb - xa) * 1.12, ya + (yb - ya) * 1.12))
    d.line((xa, ya), (xa, yb - 14))                                  # the vertical, from which the angle is read
    d.group()
    for i in range(n):
        cx = x0 + w / 2 + i * off
        cy = y0 - i * h - h / 2
        d.line(*_stadium(cx, cy, w, h), closed=True)
    d.group('mid')
    ang = math.degrees(math.atan(off / h))     # 48.4° from the vertical
    d.arc(xa, ya, 52, -90, -90 + ang, n=16)
    # dimension: the step of half a bead, above the top bead
    yt = y0 - n * h - 10
    xs = x0 + w + (n - 2) * off
    d.line((xs, yt), (xs + off, yt))
    d.lines([[(xs, yt - 4), (xs, yt + 4)], [(xs + off, yt - 4), (xs + off, yt + 4)]])
    # a part with a flat ceiling, held up by a tree of supports from the bed
    gx, gy = 292, 266
    d.group('thin')
    d.line((214, gy), (392, gy))                                     # the bed
    d.group()
    d.line((228, gy), (228, 96), (384, 96), (384, 124), (252, 124), (252, gy))   # an L: the arm overhangs
    d.group('mid')
    # the tree: a trunk from the bed, branching to tips under the arm, each branch no steeper than 40° from vertical
    tips = [(278, 128), (308, 128), (338, 128), (368, 128)]
    fork = (323, 190)
    trunk = (323, gy)
    d.line(trunk, fork)
    mids = [(298, 158), (353, 158)]
    d.lines([[fork, mids[0]], [fork, mids[1]]])
    d.lines([[mids[0], tips[0]], [mids[0], tips[1]], [mids[1], tips[2]], [mids[1], tips[3]]])
    d.line((trunk[0] - 9, gy), (trunk[0] - 3, gy - 10), (trunk[0] + 3, gy - 10), (trunk[0] + 9, gy))   # its foot
    d.group('mid')
    d.text(xa + 44, ya - 10, f'{ang:.0f}°', size=8, anchor='start')
    d.text(xs + off / 2, yt - 8, 'w/2', size=8)
    d.text(x0 - 14, y0 - h / 2 + 3, 'h', size=8, anchor='end')
    d.text(112, 24, 'BEADS IN SECTION', size=8)
    d.text(306, 24, 'A TREE SUPPORT', size=8)
    d.text(306, 86, 'ARM', size=8)
    return d


PLATES['supports'] = supports


def printed_fits():
    d = D()
    # left: a 3 mm hole as an STL draws it (inscribed polygon) and as nophead's polyhole (circumscribed hexagon)
    s = 28                                      # px per mm
    cx, cy, r = 104, 132, 1.5 * s               # the hole wanted: 3 mm
    d.group('thin')
    d.line((cx - 3.2 * s, cy), (cx + 3.2 * s, cy))
    d.line((cx, cy - 3.2 * s), (cx, cy + 3.2 * s))
    hexr = r / math.cos(math.pi / 6)
    for p in _polygon(cx, cy, hexr, 6, start=0):
        d.line((cx, cy), p)
    d.circle(cx, cy, r)                                                  # the circle a 3 mm pin needs
    d.group()
    d.line(*_polygon(cx, cy, hexr, 6, start=0), closed=True)             # the polyhole: flats tangent to the circle
    d.group('mid')
    d.line(*_polygon(cx, cy, r, 12, start=0), closed=True)               # what an STL holds: corners on the circle
    # the pin, 0.2 mm smaller a side, drawn inside
    d.circle(cx, cy, r - 0.2 * s, )
    # right: a print-in-place hinge in section along its pin: three knuckles, two gaps, one clearance all round
    hx, hy = 290, 150                           # the pin's axis runs across at hy
    pr, kr = 22, 40                             # pin radius and knuckle radius, px
    c = 6                                       # the clearance, exaggerated
    xs = [214, 262, 266 + 2 * c, 314 + 2 * c, 318 + 4 * c, 366 + 4 * c]
    d.group('thin')
    d.line((200, hy), (392, hy))                                         # the axis
    d.group()
    for i in range(3):
        a, b = xs[2 * i], xs[2 * i + 1]
        if i == 1:
            # the middle knuckle: the moving leaf, bored to the pin's radius plus the clearance
            d.line((a, hy - kr), (b, hy - kr), (b, hy - pr - c), (a, hy - pr - c), closed=True)
            d.line((a, hy + pr + c), (b, hy + pr + c), (b, hy + kr), (a, hy + kr), closed=True)
        else:
            d.line((a, hy - kr), (b, hy - kr), (b, hy + kr), (a, hy + kr), closed=True)
    # the pin, joined to the outer knuckles, passing through the middle one
    d.line((xs[1], hy - pr), (xs[4], hy - pr))
    d.line((xs[1], hy + pr), (xs[4], hy + pr))
    d.group('mid')
    # dimension the radial and the axial clearance
    d.line((xs[2] + 22, hy - pr), (xs[2] + 22, hy - pr - c))
    d.lines([[(xs[1], hy + kr + 10), (xs[1], hy + kr + 18)], [(xs[2], hy + kr + 10), (xs[2], hy + kr + 18)]])
    d.text(cx, 40, 'A 3 MM HOLE', size=8)
    d.text(cx, cy + 3.2 * s + 26, 'POLYGON · POLYHOLE', size=8)
    d.text(hx, 40, 'A PRINT-IN-PLACE HINGE', size=8)
    d.text(xs[1] - 4, hy + kr + 32, 'GAP', size=8)
    d.text(xs[2] + 28, hy - pr - 8, 'c', size=8, anchor='start')
    d.text(hx, hy + kr + 52, 'PIN FIXED · MIDDLE KNUCKLE TURNS', size=8)
    return d


PLATES['printed-fits'] = printed_fits
