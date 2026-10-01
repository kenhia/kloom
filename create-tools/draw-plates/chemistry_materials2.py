"""Plates for the chemistry subject's Materials and Chemistry now frames by part materials2 (sprint 025):
photolithography, lithium-battery and ozone-hole."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _offset(a, b, c, k=3.2):
    """A second, shorter line inside a double bond ab, on the side of point c (a ring's centre)."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = c[0] - mx, c[1] - my
    n = math.hypot(dx, dy)
    ox, oy = dx / n * k, dy / n * k
    t = 0.18
    return [(a[0] + (b[0] - a[0]) * t + ox, a[1] + (b[1] - a[1]) * t + oy),
            (a[0] + (b[0] - a[0]) * (1 - t) + ox, a[1] + (b[1] - a[1]) * (1 - t) + oy)]


def _parallel(a, b, k=3.2):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * k, dx / n * k
    return [[(a[0] + ox / 2, a[1] + oy / 2), (b[0] + ox / 2, b[1] + oy / 2)],
            [(a[0] - ox / 2, a[1] - oy / 2), (b[0] - ox / 2, b[1] - oy / 2)]]


def _head(p, ang, s=5):
    """An arrowhead at p pointing along angle ang (degrees)."""
    return [_pt(p, ang + 150, s), p, _pt(p, ang - 150, s)]


def _shorten(a, b, s0, s1):
    """The segment ab with s0 cut from its start and s1 from its end (to clear atom labels)."""
    d = math.dist(a, b)
    ux, uy = (b[0] - a[0]) / d, (b[1] - a[1]) / d
    return (a[0] + ux * s0, a[1] + uy * s0), (b[0] - ux * s1, b[1] - uy * s1)


def _ring(c, L, start=0):
    return [_pt(c, start + 60 * k, L) for k in range(6)]


def photolithography():
    """Projection printing in section (mask, lens, the half-angle that sets NA, the resist on the wafer),
    and the acid-catalysed deprotection of IBM's t-BOC resist, drawn from regular rings."""
    d = D()
    ax, my, ly, wy = 104, 62, 136, 222          # optical axis; mask, lens and wafer heights
    slits = [-40, -8, 24]                         # openings in the mask, relative to the axis
    img = [(-s * 0.6) for s in slits]            # the lens reduces and inverts the pattern
    d.group('thin')
    d.line((ax, 22), (ax, wy + 22))
    d.line((ax - 66, ly), (ax + 66, ly))
    # rays: from each opening through the lens edges to its image on the resist
    rays = []
    for s, i in zip(slits, img):
        for e in (-50, 50):
            rays.append([(ax + s, my + 3), (ax + e, ly), (ax + i, wy - 6)])
    d.lines(rays)
    # the half-angle of the marginal rays at the wafer
    th = math.degrees(math.atan2(50, wy - 6 - ly))
    d.arc(ax + img[1], wy - 6, 30, -90, -90 + th, n=16)
    d.group()
    # the mask: a chromium line with three openings
    xs = [ax - 64] + [v for s in slits for v in (ax + s - 5, ax + s + 5)] + [ax + 64]
    d.lines([[(xs[k], my), (xs[k + 1], my)] for k in range(0, len(xs), 2)])
    d.lines([[(xs[k], my + 5), (xs[k + 1], my + 5)] for k in range(0, len(xs), 2)])
    # the lens, a biconvex section
    R = (58 ** 2 + 11 ** 2) / 22                  # radius of a surface with chord 116 and sagitta 11
    half = math.degrees(math.asin(58 / R))
    d.arc(ax, ly + R - 11, R, -90 - half, -90 + half, n=40)
    d.arc(ax, ly - R + 11, R, 90 - half, 90 + half, n=40)
    # wafer and resist, with the exposed windows through the resist
    d.line((ax - 70, wy + 8), (ax + 70, wy + 8), (ax + 70, wy + 20), (ax - 70, wy + 20), closed=True)
    wins = sorted(ax + i for i in img)
    edge = [ax - 70] + [v for w in wins for v in (w - 3, w + 3)] + [ax + 70]
    d.lines([[(edge[k], wy), (edge[k + 1], wy)] for k in range(0, len(edge), 2)])
    d.lines([[(w - 3, wy), (w - 3, wy + 8)] for w in wins] + [[(w + 3, wy), (w + 3, wy + 8)] for w in wins])
    d.group('mid')
    # light coming down onto the mask
    for x in (ax - 48, ax - 16, ax + 16, ax + 48):
        d.line((x, 26), (x, 48))
        d.line(*_head((x, 48), 90, 4))

    # the resist chemistry: an aryl t-BOC carbonate, and the phenol the acid leaves
    L = 15
    top, bot = (262, 66), (262, 214)
    for c, capped in ((top, True), (bot, False)):
        v = _ring(c, L, start=0)                        # vertices at 0, 60, ... degrees
        d.group()
        d.line(*v, closed=True)
        d.line(v[3], _pt(v[3], 180, L))                 # the bond to the polymer backbone
        chain = _pt(v[3], 180, L)
        d.line(_pt(chain, -90, L * 0.8), chain, _pt(chain, 90, L * 0.8))
        o1 = _pt(v[0], -30, L)
        d.line(v[0], _shorten(v[0], o1, 0, 5)[1])
        if capped:
            c1 = _pt(o1, 30, L)
            o2 = _pt(c1, -30, L)
            cq = _pt(o2, 30, L)
            ox = _pt(c1, 90, L)
            d.line(*_shorten(o1, c1, 5, 0))
            d.line(*_shorten(c1, o2, 0, 5))
            d.line(*_shorten(o2, cq, 5, 0))
            d.lines(_parallel(*_shorten(c1, ox, 0, 5)))
            d.lines([[cq, _pt(cq, a, L * 0.8)] for a in (-60, 60, 0)])
        d.group('mid')
        d.lines([_offset(v[0], v[1], c), _offset(v[2], v[3], c), _offset(v[4], v[5], c)])
        d.text(o1[0], o1[1] + 3.5, 'O' if capped else 'OH', size=9, anchor='middle' if capped else 'start')
        if capped:
            d.text(o2[0], o2[1] + 3.5, 'O', size=9)
            d.text(ox[0], ox[1] + 1, 'O', size=9)
    # the step between them
    d.group('thin')
    d.line((262, 118), (262, 184))
    d.group()
    d.line(*_head((262, 184), 90, 5))
    d.group('mid')
    d.text(272, 150, 'H⁺ · BAKE', size=8, anchor='start')
    d.text(300, 238, '+ CO₂ + C₄H₈ + H⁺', size=8, anchor='start')
    d.text(ax, 14, 'LIGHT', size=8)
    d.text(ax - 72, my + 4, 'MASK', size=7, anchor='end')
    d.text(ax + img[1] + 20, wy - 30, 'θ', size=9)
    d.text(ax, wy + 36, 'RESIST ON SILICON', size=7)
    d.text(ax, 276, 'LINE ≈ k₁ λ / NA · NA = n sin θ', size=8)
    return d


def lithium_battery():
    """A lithium-ion cell discharging, in section: graphite layers edge-on, the separator, lithium cobalt
    oxide's slabs of edge-sharing octahedra, the lithium ions between, and the outer circuit."""
    d = D()
    gx0, gx1 = 28, 160                 # graphite electrode
    cx0, cx1 = 236, 372                # cobalt oxide electrode
    sep = (190, 206)
    ys = [96, 126, 156, 186, 216]      # graphene sheets, 30 apart
    d.group('thin')
    d.line((gx0, 80), (gx1, 80), (gx1, 232), (gx0, 232), closed=True)
    d.line((cx0, 80), (cx1, 80), (cx1, 232), (cx0, 232), closed=True)
    for y in ys:
        d.line((gx0, y), (gx1, y))
    slabs = [106, 156, 206]            # CoO2 slab centres; lithium lies between them
    for y in slabs:
        d.line((cx0, y), (cx1, y))
    d.group()
    # graphene sheets edge-on: zigzags with 120 degree bond angles
    b = 8.0
    for y in ys:
        pts, x, k = [], gx0 + 2, 0
        while x <= gx1 - 2:
            pts.append((x, y + (-2.3 if k % 2 else 2.3)))
            x += b * math.cos(math.radians(30))
            k += 1
        d.line(*pts)
    # CoO2 slabs: edge-sharing octahedra seen edge-on, as a row of squares standing on their corners
    h = 13
    for y in slabs:
        segs = []
        x = cx0 + h
        while x + h <= cx1:
            segs.append([(x - h, y), (x, y - h), (x + h, y), (x, y + h), (x - h, y)])
            x += 2 * h
        d.lines(segs)
    # the separator
    d.lines([[(sep[0], y), (sep[0], y + 8)] for y in range(84, 228, 14)] +
            [[(sep[1], y + 7), (sep[1], y + 15)] for y in range(84, 222, 14)])
    # the outer circuit, with a load
    d.line((94, 80), (94, 40), (170, 40))
    zig = [(170, 40)] + [(176 + 6 * k, 40 + (6 if k % 2 == 0 else -6)) for k in range(9)] + [(230, 40)]
    d.line(*zig)
    d.line((230, 40), (304, 40), (304, 80))
    d.group('mid')
    # lithium between the graphene sheets (a few left) and between the oxide slabs
    for y in (111, 171):
        for x in (60, 100, 132):
            d.circle(x, y, 3.2)
    for y in (131, 181):
        for x in range(cx0 + 13, cx1 - 6, 26):
            d.circle(x, y, 3.2)
    # cobalt at the centre of each octahedron
    for y in slabs:
        x = cx0 + h
        while x + h <= cx1:
            d.circle(x, y, 1.6)
            x += 2 * h
    # ions crossing the separator; electrons round the circuit
    for y in (141, 201):
        d.line((150, y), (226, y))
        d.line(*_head((226, y), 0, 5))
    d.line(*_head((150, 40), 0, 5))
    d.line(*_head((270, 40), 0, 5))
    d.text(94, 252, 'GRAPHITE', size=8)
    d.text(304, 252, 'LiCoO₂', size=8)
    d.text(198, 252, 'SEPARATOR', size=7)
    d.text(170, 134, 'Li⁺', size=8)
    d.text(122, 32, 'e⁻', size=9)
    d.text(200, 282, 'LiC₆ + CoO₂ → C₆ + LiCoO₂', size=9)
    return d


def ozone_hole():
    """The chlorine catalytic cycle, and ozone columns drawn to scale in Dobson units (100 DU = 1 mm)."""
    d = D()
    c, r = (124, 138), 64
    top, bot = _pt(c, -90, r), _pt(c, 90, r)
    d.group('thin')
    d.circle(*c, r)
    d.line((c[0] - 8, c[1]), (c[0] + 8, c[1]))
    d.line((c[0], c[1] - 8), (c[0], c[1] + 8))
    d.group()
    # the two steps, as arcs round the cycle: step 1 down the right, step 2 up the left
    d.arc(*c, r, -72, 72, n=40)
    d.line(*_head(_pt(c, 72, r), 72 + 90, 6))
    d.arc(*c, r, 108, 252, n=40)
    d.line(*_head(_pt(c, 252, r), 252 + 90, 6))
    d.group('mid')
    # what goes in and comes out at each step
    for a, inward in ((-20, True), (20, False)):
        p0, p1 = _pt(c, a, r + 34), _pt(c, a, r + 6)
        if inward:
            d.line(p0, p1)
            d.line(*_head(p1, a + 180, 4))
        else:
            d.line(p1, p0)
            d.line(*_head(p0, a, 4))
    for a, inward in ((200, True), (160, False)):
        p0, p1 = _pt(c, a, r + 34), _pt(c, a, r + 6)
        if inward:
            d.line(p0, p1)
            d.line(*_head(p1, a + 180, 4))
        else:
            d.line(p1, p0)
            d.line(*_head(p0, a, 4))
    # ozone columns, to scale: 300 DU (a normal column), 220 (the hole's edge) and 122 (Halley, October 1993)
    base, k = 236, 0.5                           # pixels per Dobson unit
    cols = [(290, 300), (350, 122)]
    d.group('thin')
    d.line((258, base), (384, base))
    d.line((258, base - 220 * k), (384, base - 220 * k))
    d.group()
    for x, du in cols:
        hgt = du * k
        d.line((x - 14, base), (x - 14, base - hgt))
        d.line((x + 14, base), (x + 14, base - hgt))
        d.ellipse(x, base - hgt, 14, 4)
        d.arc(x, base, 14, 0, 180, n=24, ry=4)
    d.group('mid')
    d.text(top[0], top[1] + 4, 'Cl', size=11)
    d.text(bot[0], bot[1] + 4, 'ClO', size=11)
    d.text(*_pt(c, -20, r + 44), 'O₃', size=9)
    d.text(*_pt(c, 20, r + 44), 'O₂', size=9)
    d.text(*_pt(c, 200, r + 44), 'O', size=9)
    d.text(*_pt(c, 160, r + 44), 'O₂', size=9)
    d.text(124, 262, 'NET · O₃ + O → 2 O₂', size=9)
    d.text(290, base + 16, '300 DU', size=8)
    d.text(350, base + 16, '122 DU', size=8)
    d.text(290, base + 28, '3 mm', size=7)
    d.text(350, base + 28, 'HALLEY 1993', size=7)
    d.text(386, base - 220 * k - 4, '220', size=7, anchor='end')
    return d


PLATES = {'photolithography': photolithography, 'lithium-battery': lithium_battery, 'ozone-hole': ozone_hole}
