"""Plates for How We Build's trail At the forge (sprint 026)."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _arrow(d, x0, y0, x1, y1, head=5):
    """A line from (x0, y0) to (x1, y1) with an open head at the far end."""
    d.line((x0, y0), (x1, y1))
    a = math.degrees(math.atan2(y1 - y0, x1 - x0))
    l, r = _dir(a + 150), _dir(a - 150)
    d.line((x1 + l[0] * head, y1 + l[1] * head), (x1, y1), (x1 + r[0] * head, y1 + r[1] * head))


def _polygon(cx, cy, r, n, rot=0.0):
    return [(cx + r * math.cos(math.radians(rot + 360 * k / n)), cy + r * math.sin(math.radians(rot + 360 * k / n)))
            for k in range(n)]


def drawing_out():
    d = D()
    # Bottom: the worked taper at 1 px to the millimetre. A 20 mm square bar; 62 mm of it
    # becomes a square taper 150 mm long, 4 mm square at the tip (the reading's invented numbers).
    x0, xs = 34, 104                 # the bar's cut end on the left; where the drawn part starts
    yb, ya = 252, 196                # centre lines of the bar as stock (below) and as drawn (above)
    h = 20
    stock, taper, tip = 62, 150, 4
    d.group('thin')
    d.line((x0 - 8, yb), (xs + taper + 14, yb))
    d.line((x0 - 8, ya), (xs + taper + 14, ya))
    # projection of where the drawing starts, through both bars
    d.line((xs, ya - 22), (xs, yb + 22))
    d.line((xs + stock, yb - 16), (xs + stock, yb + 22))
    d.line((xs + taper, ya - 16), (xs + taper, ya + 22))
    # dimension lines under the stock and over the taper
    d.line((xs, yb + 18), (xs + stock, yb + 18))
    d.lines([[(xs, yb + 14), (xs, yb + 22)], [(xs + stock, yb + 14), (xs + stock, yb + 22)]])
    d.line((xs, ya - 18), (xs + taper, ya - 18))
    d.lines([[(xs, ya - 22), (xs, ya - 14)], [(xs + taper, ya - 22), (xs + taper, ya - 14)]])
    # Top left: the horn seen end on, a circle, and the face beside it, with their centre lines
    hx, hy, hr = 92, 104, 22
    fx, fy = 214, 104                # the face view: the bar's section on a flat face
    d.line((hx, hy - 70), (hx, hy + hr + 14))
    d.line((hx - 70, hy), (hx + 70, hy))
    d.line((fx, fy - 70), (fx, fy + 30))
    d.line((334, 88), (334, 254))     # the sections' centre line
    d.group()
    # the stock bar, with the part to be drawn closed off
    d.line((x0, yb - h / 2), (xs + stock, yb - h / 2), (xs + stock, yb + h / 2), (x0, yb + h / 2))
    d.line((xs, yb - h / 2), (xs, yb + h / 2))
    # the drawn bar: the same parent bar, then the taper
    d.line((x0, ya - h / 2), (xs, ya - h / 2), (xs + taper, ya - tip / 2), (xs + taper, ya + tip / 2),
           (xs, ya + h / 2), (x0, ya + h / 2))
    # the horn end on, the bar lying across it, and the face with the bar's section on it
    d.circle(hx, hy, hr)
    d.line((hx - 66, hy - hr - 12), (hx + 66, hy - hr - 12), (hx + 66, hy - hr), (hx - 66, hy - hr), closed=True)
    d.line((fx - 50, fy + 10), (fx + 50, fy + 10))                   # the anvil's face
    d.line((fx - 50, fy + 10), (fx - 50, fy + 34))
    d.line((fx + 50, fy + 10), (fx + 50, fy + 34))
    d.line((fx - 10, fy + 10), (fx - 10, fy - 10), (fx + 10, fy - 10), (fx + 10, fy + 10))   # the bar's section before
    d.group('mid')
    # hammers coming down on each
    for cx, top in ((hx, hy - hr - 12), (fx, fy - 10)):
        d.line((cx - 13, top - 14), (cx + 13, top - 14), (cx + 13, top - 40), (cx - 13, top - 40), closed=True)
        d.line((cx + 13, top - 27), (cx + 58, top - 31))
        _arrow(d, cx, top - 52, cx, top - 44, head=4)
    # on the horn the metal goes along the bar; on the face, as much sideways as along
    _arrow(d, hx - 8, hy - hr - 6, hx - 46, hy - hr - 6)
    _arrow(d, hx + 8, hy - hr - 6, hx + 46, hy - hr - 6)
    d.line((fx - 16, fy + 10), (fx - 16, fy - 3), (fx + 16, fy - 3), (fx + 16, fy + 10))   # the section after a blow
    _arrow(d, fx - 20, fy + 3, fx - 38, fy + 3)
    _arrow(d, fx + 20, fy + 3, fx + 38, fy + 3)
    # sections down the taper on the right: square, octagon, round
    sx = 334
    q = 1.6                          # the sections drawn larger than the bars
    for k, (y, kind) in enumerate(((112, 4), (172, 8), (232, 0))):
        if kind == 4:
            d.line(*_polygon(sx, y, 14.14 * q, 4, 45), closed=True)
        elif kind == 8:
            d.line(*_polygon(sx, y, 10.82 * q, 8, 22.5), closed=True)
            d.line(*_polygon(sx, y, 14.14 * q, 4, 45), closed=True)
        else:
            d.circle(sx, y, 10 * q)
    d.group('mid')
    d.text(xs + stock / 2, yb + 32, '62', size=8)
    d.text(xs + taper / 2, ya - 24, '150', size=8)
    d.text(x0 + 34, yb - 16, '20 × 20', size=8)
    d.text(hx, hy + hr + 26, 'ON THE HORN', size=8)
    d.text(fx, fy + 48, 'ON THE FACE', size=8)
    d.text(sx, 78, 'SQUARE', size=8)
    d.text(sx, 204, 'OCTAGON', size=8)
    d.text(sx, 266, 'ROUND', size=8)
    return d


PLATES = {'drawing-out': drawing_out}


def _scarf(x_end, y_bot, t, T, L, n=16, bulge=2.5, flip=False, back=120):
    """A bar end upset and scarfed for a lap weld, as a closed outline.

    The bar is t thick, upset to T over its last L * 1.4, and its end drawn to a wedge L long
    whose face bows outward by `bulge` (convex). With flip, the piece is turned over and
    points the other way, as the smith lays it on top.
    """
    s = -1 if flip else 1                         # +1: the end points right, scarf on the top face
    xu = x_end - s * L * 1.4                      # where the upset begins
    xs = x_end - s * L                            # where the scarf begins
    pts = [(x_end - s * back, y_bot), (x_end, y_bot)]
    for i in range(n + 1):                        # the scarf face, from the thin edge back up to full upset thickness
        u = i / n
        x = x_end - s * L * u
        y = y_bot - T * u - bulge * math.sin(math.pi * u)
        pts.append((x, y))
    pts += [(xs - s * 2, y_bot - T), (xu, y_bot - t), (x_end - s * back, y_bot - t)]
    if flip:                                      # turn it over about its own mid-thickness
        pts = [(x, 2 * y_bot - T - y) for x, y in pts]
    return pts


def forge_welding():
    d = D()
    t, T, L = 20, 26, 30                          # bar 20 thick, upset to 26, scarf 1.5 × 20 = 30 long
    jx = 150                                      # the joint's centre, x
    ya = 238                                      # the anvil's face in the welding view
    yl = 126                                      # bottom face of the lower piece in the exploded view
    d.group('thin')
    d.line((20, yl), (300, yl))
    d.line((20, yl - T - 20), (300, yl - T - 20))
    d.line((jx - L / 2, 40), (jx - L / 2, ya + 14))
    d.line((jx + L / 2, 40), (jx + L / 2, ya + 14))
    # the scarf's length as a dimension, between the projection lines
    d.line((jx - L / 2, 46), (jx + L / 2, 46))
    d.lines([[(jx - L / 2, 42), (jx - L / 2, 50)], [(jx + L / 2, 42), (jx + L / 2, 50)]])
    # the thickness the scarf is measured from
    d.line((28, yl), (28, yl - t))
    d.lines([[(24, yl), (32, yl)], [(24, yl - t), (32, yl - t)]])
    d.group()
    # exploded: the helper's piece scarf up, the smith's piece turned over above it
    d.line(*_scarf(jx + L / 2, yl, t, T, L), closed=False)
    d.line(*_scarf(jx - L / 2, yl - T - 20, t, T, L, flip=True), closed=False)
    # laid together on the anvil: the smith's piece rests on the helper's, scarf on scarf
    d.line((40, ya), (260, ya))                   # the anvil face
    d.line((40, ya), (40, ya + 34))
    d.line((260, ya), (260, ya + 34))
    d.line(*_scarf(jx + L / 2, ya, t, T, L, back=100))
    d.line(*_scarf(jx - L / 2, ya, t, T, L, flip=True, back=100))
    d.group('mid')
    # the hammer and the line of the blow, and slag squeezed out at both ends of the seam
    d.line((jx - 14, ya - T - 22), (jx + 14, ya - T - 22), (jx + 14, ya - T - 52), (jx - 14, ya - T - 52), closed=True)
    d.line((jx + 14, ya - T - 37), (jx + 66, ya - T - 44))
    _arrow(d, jx, ya - T - 66, jx, ya - T - 58, head=4)
    for k in range(3):
        d.circle(jx - L / 2 - 5 - 5 * k, ya - T - 2 - 4 * k, 1.2)
        d.circle(jx + L / 2 + 5 + 5 * k, ya - 2 - 4 * k, 1.2)
    # the lay: an arrow from the upper piece down onto the lower
    _arrow(d, jx + 70, yl - T - 20 + t + 6, jx + 70, yl - 4, head=4)
    # right: the scarf faces meeting, convex and concave, in section
    cx = 340
    for k, (y, conv) in enumerate(((116, True), (206, False))):
        b = 5 if conv else -5
        top = [(cx - 32 + 64 * i / 20, y - b * math.sin(math.pi * i / 20)) for i in range(21)]
        bot = [(cx - 32 + 64 * i / 20, y + b * math.sin(math.pi * i / 20)) for i in range(21)]
        d.line(*top)
        d.line(*bot)
        d.line((cx - 32, y - 14), (cx - 32, y))
        d.line((cx + 32, y + 14), (cx + 32, y))
        if conv:
            _arrow(d, cx - 6, y + 9, cx - 26, y + 9, head=3)
            _arrow(d, cx + 6, y - 9, cx + 26, y - 9, head=3)
        else:
            d.lines([[(cx - 12 + 6 * i, y - 1), (cx - 9 + 6 * i, y + 1)] for i in range(5)])
    d.group('mid')
    d.text(jx, 36, '1.5 t', size=8)
    d.text(36, yl - 6, 't', size=8, anchor='start')
    d.text(cx, 146, 'CONVEX', size=8)
    d.text(cx, 236, 'CONCAVE', size=8)
    d.text(150, 290, 'A LAP WELD: SCARFED, LAID, STRUCK', size=8)
    return d


PLATES['forge-welding'] = forge_welding


def pattern_welding():
    d = D()
    # Top left: a billet of seven strips, drawn out and folded into fourteen (the reading's table)
    bx0, bx1, by0, bh = 30, 104, 34, 56
    cx0, cx1 = 150, 224
    # Middle left: a laminated rod twisted, seen from the side; layers at offsets z turn with x
    rx0, rx1, ry, rw, pitch = 30, 224, 146, 13, 46
    # Bottom left: the blade's section, three welded rods between two steel edges, drawn large
    sy, ss = 238, 26
    sx = [127 - ss * 1.5 + ss * k for k in range(3)]
    # Right: the blade's face after grinding, three bands of stripes between plain edges
    fx0, fband, fedge, fy0, fy1 = 276, 18, 9, 34, 228
    d.group('thin')
    d.line((bx0 - 8, by0 + bh / 2), (cx1 + 10, by0 + bh / 2))
    d.line((rx0 - 8, ry), (rx1 + 8, ry))                        # the rod's axis, and where it is ground
    d.line((30, sy), (226, sy))
    d.line((fx0 + fedge + 1.5 * fband, fy0 - 10), (fx0 + fedge + 1.5 * fband, fy1 + 44))
    d.lines([[(sx[0] - ss / 2, sy - 30), (sx[0] - ss / 2, sy + 30)], [(sx[2] + ss / 2, sy - 30), (sx[2] + ss / 2, sy + 30)]])
    d.group()
    # the two billets
    d.line((bx0, by0), (bx1, by0), (bx1, by0 + bh), (bx0, by0 + bh), closed=True)
    d.line((cx0, by0), (cx1, by0), (cx1, by0 + bh), (cx0, by0 + bh), closed=True)
    # the rod's outline
    d.line((rx0, ry - rw), (rx1, ry - rw))
    d.line((rx0, ry + rw), (rx1, ry + rw))
    d.line((rx0, ry - rw), (rx0, ry + rw))
    d.line((rx1, ry - rw), (rx1, ry + rw))
    # the section: a flat lens, the core of three rods, the edges welded on
    w = ss * 1.5
    d.line((sx[0] - ss / 2 - 40, sy), (sx[0] - ss / 2, sy - ss / 2), (sx[2] + ss / 2, sy - ss / 2),
           (sx[2] + ss / 2 + 40, sy), (sx[2] + ss / 2, sy + ss / 2), (sx[0] - ss / 2, sy + ss / 2), closed=True)
    for x in sx[1:]:
        d.line((x - ss / 2, sy - ss / 2), (x - ss / 2, sy + ss / 2))
    # the face of the blade, its edges and point
    fx1 = fx0 + 2 * fedge + 3 * fband
    mid = (fx0 + fx1) / 2
    d.line((fx0, fy0), (fx0, fy1), (mid, fy1 + 34), (fx1, fy1), (fx1, fy0))
    d.line((fx0 - 8, fy0), (fx1 + 8, fy0))
    d.group('mid')
    # the strips of the billets, steel and iron in turn (the steel shaded with short strokes)
    for k in range(1, 7):
        y = by0 + bh * k / 7
        d.line((bx0, y), (bx1, y))
    d.lines([[(bx0 + 4 + 6 * i, by0 + bh * k / 7 + 2), (bx0 + 7 + 6 * i, by0 + bh * (k + 1) / 7 - 2)]
             for k in range(0, 7, 2) for i in range(12)])
    for k in range(1, 14):
        y = by0 + bh * k / 14
        d.line((cx0, y), (cx1, y))
    _arrow(d, bx1 + 10, by0 + bh / 2 - 10, cx0 - 10, by0 + bh / 2 - 10)
    # the twisted rod: each layer boundary is a sine as it turns, clipped to the rod's faces
    for z in (-9, -5, -1, 3, 7, 11):
        pts = []
        for i in range(161):
            x = rx0 + (rx1 - rx0) * i / 160
            y = ry + z * math.cos(2 * math.pi * (x - rx0) / pitch)
            pts.append((x, max(ry - rw + 0.5, min(ry + rw - 0.5, y))))
        d.line(*pts)
    # the section's rods: layers run differently in each, cut where the twist happened to stand
    for k, x in enumerate(sx):
        a = math.radians((30, -30, 30)[k])
        for j in range(-2, 3):
            o = j * ss / 6
            nx, ny = -math.sin(a), math.cos(a)
            ux, uy = math.cos(a), math.sin(a)
            p0 = (x + nx * o - ux * ss, sy + ny * o - uy * ss)
            p1 = (x + nx * o + ux * ss, sy + ny * o + uy * ss)
            # clip the line to the rod's square
            ts = []
            for (px, py, qx, qy) in ((p0[0], p0[1], p1[0], p1[1]),):
                for tt in [i / 200 for i in range(201)]:
                    X, Y = px + (qx - px) * tt, py + (qy - py) * tt
                    if abs(X - x) <= ss / 2 and abs(Y - sy) <= ss / 2:
                        ts.append((X, Y))
            if len(ts) > 1:
                d.line(ts[0], ts[-1])
    # the face: stripes slanting one way in the outer bands and the other way in the middle
    for b in range(3):
        x0 = fx0 + fedge + b * fband
        s = 1 if b != 1 else -1
        segs = []
        y = fy0 + 4
        while y < fy1 - 10:
            segs.append([(x0 + 2, y + (5 if s < 0 else 0)), (x0 + fband - 2, y + (0 if s < 0 else 5))])
            y += 7
        d.lines(segs)
        d.line((x0, fy0), (x0, fy1))
    d.line((fx1 - fedge, fy0), (fx1 - fedge, fy1))
    d.group('mid')
    d.text((bx0 + bx1) / 2, by0 - 8, '7', size=8)
    d.text((cx0 + cx1) / 2, by0 - 8, '14', size=8)
    d.text((bx1 + cx0) / 2, by0 + bh / 2 - 16, 'FOLD', size=8)
    d.text((rx0 + rx1) / 2, ry + rw + 16, 'A TWISTED ROD', size=8)
    d.text(127, sy + 36, 'SECTION', size=8)
    d.text(mid, fy1 + 52, 'FACE', size=8)
    return d


PLATES['pattern-welding'] = pattern_welding


def heat_treatment():
    d = D()
    # A cold chisel tempered from its own heat, as Bacon describes: the end quenched, the shank
    # still red-hot, and the heat running back down towards the edge. Below, the temperature along
    # the chisel at two moments (an invented profile, decaying from the quench line), with
    # Bacon's temper temperatures as levels; where each level meets the later curve, that colour stands.
    x0, xq, xe = 30, 150, 362         # the chisel's shank end, the quench line, the cutting edge
    cy, half = 74, 13                 # the chisel's centre line and half-thickness
    gy0, gy1 = 272, 132               # the graph: 150 °C at gy0, 400 °C at gy1
    T0, T1 = 150, 400

    def gy(T):
        return gy0 + (gy1 - gy0) * (T - T0) / (T1 - T0)

    def profile(x, lam):
        return 150 + 650 * math.exp(-(x - xq) / lam)

    levels = [(221, 'PALE YELLOW'), (260, ''), (288, ''), (304, 'BLUE')]
    lam_late = 64
    cross = {T: xq - lam_late * math.log((T - 150) / 650) for T, _ in levels}
    d.group('thin')
    d.line((x0 - 6, cy), (xe + 12, cy))
    d.line((xq, cy - 30), (xq, gy0 + 6))
    d.line((xe, cy - 30), (xe, gy0 + 6))
    d.line((x0, gy0), (xe + 6, gy0))                              # the graph's axes
    d.line((x0, gy0), (x0, gy1 - 8))
    for T, _ in levels:
        d.line((x0, gy(T)), (xe, gy(T)))
        d.line((cross[T], gy(T)), (cross[T], cy + half + 4))     # up from the crossing to the chisel
    d.group()
    # the chisel: a bar, then a long taper to the edge
    d.line((x0, cy - half), (282, cy - half), (xe, cy - 1.5), (xe, cy + 1.5), (282, cy + half), (x0, cy + half), (x0, cy - half))
    # the later temperature curve
    d.line(*[(x, gy(min(T1, profile(x, lam_late)))) for x in [xq + (xe - xq) * i / 80 for i in range(81)]
             if profile(x, lam_late) <= T1 + 1])
    d.group('mid')
    # the shank, still red-hot, marked by short strokes; the colour bands on the chisel's face
    d.lines([[(x0 + 6 + 8 * i, cy - half + 3), (x0 + 10 + 8 * i, cy + half - 3)] for i in range(int((xq - x0 - 8) / 8))])
    for T, _ in levels:
        x = cross[T]
        top = cy - half if x < 282 else cy - half + (half - 1.5) * (x - 282) / (xe - 282)
        d.line((x, top), (x, 2 * cy - top))
    # the earlier curve, and the heat running towards the edge
    d.line(*[(x, gy(min(T1, profile(x, 34)))) for x in [xq + (xe - xq) * i / 80 for i in range(81)]
             if profile(x, 34) <= T1 + 1])
    _arrow(d, 216, cy - half - 14, 300, cy - half - 14)
    d.group('mid')
    for T, name in levels:
        d.text(x0 - 4, gy(T) + 3, str(T), size=7, anchor='end')
        if name:
            d.text(cross[T] + 4, gy(T) - 4, name, size=7, anchor='start')
    d.text(x0 - 4, gy1 - 10, '°C', size=7, anchor='end')
    d.text((x0 + xq) / 2, cy - half - 8, 'RED-HOT', size=8)
    d.text(xe, cy - 34, 'EDGE', size=8)
    d.text(xq, cy - 34, 'QUENCHED TO HERE', size=8)
    return d


PLATES['heat-treatment'] = heat_treatment
