"""Plates for How We Build's Layer by layer segment, part additive2 (sprint 026):
RepRap, OpenSCAD and printing in metal."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _iso(x, y, z, ox, oy, s):
    """A dimetric projection: x to the right and a little down, y back and to the left, foreshortened, z up."""
    ax, ay = math.radians(12), math.radians(40)
    return (ox + (x * math.cos(ax) - 0.55 * y * math.cos(ay)) * s,
            oy + (x * math.sin(ax) - 0.55 * y * math.sin(ay)) * s - z * s)


def _cube_edges(ox, oy, s, a=1.0):
    """The twelve edges of a cube of side `a`, projected."""
    v = {(x, y, z): _iso(x * a, y * a, z * a, ox, oy, s) for x in (0, 1) for y in (0, 1) for z in (0, 1)}
    edges = []
    for p in v:
        for q in v:
            if p < q and sum(abs(i - j) for i, j in zip(p, q)) == 1:
                edges.append((p, q, v[p], v[q]))
    return v, edges


def reprap():
    d = D()
    # Darwin: a cube of threaded rods held at its corners by printed blocks (about 500 mm a side)
    ox, oy, s = 76, 236, 120
    v, edges = _cube_edges(ox, oy, s)
    d.group('thin')
    # the isometric axes from the near-bottom corner, and the build platform's level
    o = v[(0, 0, 0)]
    for end in ((1.35, 0, 0), (0, 1.35, 0), (0, 0, 1.3)):
        d.line(o, _iso(*end, ox, oy, s))
    plat = [_iso(x, y, 0.42, ox, oy, s) for x, y in ((0.12, 0.12), (0.88, 0.12), (0.88, 0.88), (0.12, 0.88))]
    d.line(*plat, closed=True)
    # the generation tree's guide lines: one machine, two, four, eight
    gx = [250, 290, 330, 370]
    for x in gx:
        d.line((x, 40), (x, 262))
    d.group('mid')
    # the rods: each edge drawn as a pair of lines, the bought steel
    for p, q, a, b in edges:
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        nx, ny = -dy / n * 1.6, dx / n * 1.6
        sh = 0.1                                   # stop short of the corner blocks
        a2 = (a[0] + dx * sh, a[1] + dy * sh)
        b2 = (b[0] - dx * sh, b[1] - dy * sh)
        d.lines([[(a2[0] + nx, a2[1] + ny), (b2[0] + nx, b2[1] + ny)],
                 [(a2[0] - nx, a2[1] - ny), (b2[0] - nx, b2[1] - ny)]])
    d.group()
    # the printed corner blocks: small cubes at every corner, the parts the machine makes for itself
    for (x, y, z), (px, py) in v.items():
        bv, be = _cube_edges(0, 0, 13)
        cx, cy = _iso(0.5, 0.5, 0.5, 0, 0, 13)
        d.lines([[(px + a[0] - cx, py + a[1] - cy), (px + b[0] - cx, py + b[1] - cy)] for _, _, a, b in be])
    # the tree of machines: each one prints the parts for another
    rows = [[151], [101, 201], [64, 126, 176, 238], [46, 82, 108, 144, 158, 194, 220, 256]]
    for k, (x, ys) in enumerate(zip(gx, rows)):
        for y in ys:
            r = 7 - k
            d.line((x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r), closed=True)
    d.group('mid')
    links = []
    for k in range(3):
        for i, y in enumerate(rows[k]):
            for y2 in rows[k + 1][2 * i:2 * i + 2]:
                links.append([(gx[k] + 8 - k, y), (gx[k + 1] - 7 + k, y2)])
    d.lines(links)
    d.group('mid')
    d.text(gx[0], 28, '1', size=8)
    d.text(gx[1], 28, '2', size=8)
    d.text(gx[2], 28, '4', size=8)
    d.text(gx[3], 28, '8', size=8)
    d.text(310, 284, 'EACH PRINTS THE NEXT', size=8)
    d.text(118, 284, 'RODS BOUGHT, CORNERS PRINTED', size=8)
    return d


PLATES = {'reprap': reprap}


def openscad():
    """The left edge of Ken Hiatt's drawer nameplate in section, at true scale, with the cubes
    turned 45° that `difference()` takes away to leave the chamfers."""
    d = D()
    k = 30                                        # px per mm
    x0, z0 = 92, 236                              # the plate's bottom-left corner
    P = lambda x, z: (x0 + x * k, z0 - z * k)
    base, plate, inset, text = 0.6, 1.4, 2.75, 0.4
    os_b = math.sqrt(2) * base + 2                # the cube's side, as the program computes it
    os_p = math.sqrt(2) * plate + 2
    d.group('thin')
    # the bed, and the two cubes turned on edge: diamonds standing on the corners they cut
    d.line(P(-2.6, 0), P(9.4, 0))
    for (cx, cz), a in (((0, 0), os_b), ((inset, base), os_p)):
        h = a / math.sqrt(2)
        d.line(P(cx, cz), P(cx + h, cz + h), P(cx, cz + 2 * h), P(cx - h, cz + h), closed=True)
    # dimension lines: the base's thickness and the plate's
    d.line(P(-1.2, 0), P(-1.2, base))
    d.lines([[P(-1.35, 0), P(-1.05, 0)], [P(-1.35, base), P(-1.05, base)]])
    d.line(P(8.9, base), P(8.9, base + plate))
    d.lines([[P(8.75, base), P(9.05, base)], [P(8.75, base + plate), P(9.05, base + plate)]])
    d.group()
    # what is left: the base with its 45° edge, the raised plate with its own, the letters' layer on top
    d.line(P(9.4, 0), P(0, 0), P(base, base), P(inset, base), P(inset + plate, base + plate), P(9.4, base + plate))
    d.line(P(inset, base), P(9.4, base))
    d.group('mid')
    # the raised letters, 0.4 mm proud, in section where a stroke of a letter is cut
    for x in (5.3, 6.6, 7.7):
        d.line(P(x, base + plate), P(x, base + plate + text), P(x + 0.7, base + plate + text), P(x + 0.7, base + plate))
    # the 45° marks at both chamfers
    d.arc(*P(0, 0), 26, -45, 0, n=10)
    d.arc(*P(inset, base), 34, -45, 0, n=10)
    # a small CSG tree: difference of a cube and a turned cube
    tx, ty = 312, 64
    d.line((tx - 4, ty + 6), (tx - 40, ty + 34))
    d.line((tx + 4, ty + 6), (tx + 40, ty + 34))
    d.line((tx - 54, ty + 40), (tx - 28, ty + 40), (tx - 28, ty + 58), (tx - 54, ty + 58), closed=True)
    d.line((tx + 40, ty + 34), (tx + 52, ty + 46), (tx + 40, ty + 58), (tx + 28, ty + 46), closed=True)
    d.group('mid')
    d.text(tx, ty, 'difference()', size=8)
    d.text(tx - 41, ty + 72, 'cube', size=8)
    d.text(tx + 40, ty + 72, 'rotate 45°', size=8)
    d.text(P(-1.3, base / 2)[0] - 6, P(0, base / 2)[1] + 3, '0.6', size=8, anchor='end')
    d.text(P(9.0, 0)[0] + 6, P(0, base + plate / 2)[1] + 3, '1.4', size=8, anchor='start')
    d.text(P(0, 0)[0] + 30, P(0, 0)[1] - 5, '45°', size=8, anchor='start')
    d.text(200, 284, 'THE NAMEPLATE’S EDGE IN SECTION, MM × 30', size=8)
    return d


PLATES['openscad'] = openscad


def metal_printing():
    """A laser powder bed fusion machine in section, and a bridge specimen curling when cut off its plate."""
    d = D()
    bx0, bx1 = 34, 238                            # the build well's walls
    top = 150                                     # the powder's surface
    pt = 222                                      # the top of the build plate
    d.group('thin')
    # the well, the gas flow across the bed, the scanner's two rays
    d.line((bx0, 70), (bx0, 262))
    d.line((bx1, 70), (bx1, 262))
    d.lines([[(bx0 + 8, 112 + 10 * j), (bx1 - 8, 112 + 10 * j)] for j in range(2)])
    d.lines([[(bx1 - 16, 108 + 10 * j), (bx1 - 8, 112 + 10 * j), (bx1 - 16, 116 + 10 * j)] for j in range(2)])
    mx, my = 136, 26                              # the scanning mirror
    pool = (164, top)
    d.line((mx, my), (88, top))
    d.line((mx, my), (200, top))
    # the layer lines of the powder bed, 40 µm each in the drawing's world, drawn many times larger
    for j in range(1, 12):
        y = top + j * 6
        d.line((bx0, y), (bx1, y))
    d.group()
    # the build plate, and the part grown on it: a bridge on two legs, with a lattice of supports under its span
    d.line((bx0 + 2, pt), (bx1 - 2, pt), (bx1 - 2, pt + 30), (bx0 + 2, pt + 30), closed=True)
    part = [(70, pt), (70, top), (210, top), (210, pt), (186, pt), (186, top + 30), (94, top + 30), (94, pt)]
    d.line(*part, closed=True)
    d.line((mx, my), pool)                        # the beam itself
    d.group('mid')
    # supports under the span: thin struts from the plate to the bridge's underside
    d.lines([[(100 + 9 * i, pt), (100 + 9 * i, top + 30)] for i in range(10)])
    # the melt pool where the beam lands, and the recoater blade at the edge of the bed
    d.arc(pool[0], pool[1], 7, 0, 180, n=16, ry=4)
    d.line((bx0 + 10, top - 30), (bx0 + 22, top - 30), (bx0 + 22, top - 2), (bx0 + 16, top), (bx0 + 10, top - 2), closed=True)
    d.ellipse(mx, my, 10, 3)
    # the same bridge after cutting: its legs freed, it curls up (bridge curvature method)
    cx, cy, w = 318, 200, 100
    ang = 6                                       # the curl-up angle, exaggerated
    a = math.radians(ang)
    span = [(cx - w / 2 + i * w / 20, cy - 30 - abs(i - 10) * math.tan(a) * w / 20) for i in range(21)]
    d.line(*span)
    l0, r0 = span[0], span[-1]
    d.line(l0, (l0[0] + math.sin(2 * a) * 40, l0[1] + math.cos(2 * a) * 40))
    d.line(r0, (r0[0] - math.sin(2 * a) * 40, r0[1] + math.cos(2 * a) * 40))
    d.group('thin')
    # where it stood on the plate: the flat top and the upright legs
    d.line((cx - w / 2, cy + 12), (cx - w / 2, cy - 30), (cx + w / 2, cy - 30), (cx + w / 2, cy + 12))
    d.line((cx - w / 2 - 12, cy + 12), (cx + w / 2 + 12, cy + 12))
    d.group('mid')
    d.text(mx + 16, my + 3, 'LASER', size=8, anchor='start')
    d.text(136, 104, 'ARGON', size=8)
    d.text(140, pt + 46, 'BUILD PLATE', size=8)
    d.text(318, 236, 'CUT FREE, IT CURLS', size=8)
    d.text(pool[0] + 10, top - 8, 'MELT POOL', size=8, anchor='start')
    return d


PLATES['metal-printing'] = metal_printing
