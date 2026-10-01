"""Plates for In the Blood's What we do with blood, part uses2 (sprint 028): rhogam,
gift-relationship, hepatitis. See plates_for.py."""
import math
from plates import D


def _pt(cx, cy, r, a):
    """The point at `a` degrees on a circle (clockwise from +x; SVG's y runs down)."""
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _hatch_circle(d, cx, cy, r, step=2.6, angle=45):
    """Parallel hatching clipped to a circle, as one path."""
    t = math.radians(angle)
    ux, uy = math.cos(t), math.sin(t)          # along the hatch
    nx, ny = -uy, ux                            # across it
    segs = []
    k = -r + step / 2
    while k < r:
        h = math.sqrt(max(r * r - k * k, 0))
        px, py = cx + nx * k, cy + ny * k
        segs.append([(px - ux * h, py - uy * h), (px + ux * h, py + uy * h)])
        k += step
    d.lines(segs)


def rhogam():
    d = D()
    # Left: a field of an acid-eluted film at x400, with a Miller square in the eyepiece. Adult cells
    # are ghosts (outline only); fetal cells keep their haemoglobin and take the stain (hatched).
    # Ghosts are counted in the small square (1/9 of the area), fetal cells in the large one.
    # Right: one fetal red cell coated with anti-D, each IgG a Y whose two arms hold D sites.
    fx, fy, fr = 128, 150, 112
    cr = 8.2                                    # a cell's radius; cells touch but do not overlap
    big = 132                                   # the Miller square's side; the small one is a third of it
    bx0, by0 = fx - big / 2, fy - big / 2
    small = big / 3
    fetal = {(2, 1), (-3, 3), (4, -2)}          # which lattice cells are fetal (illustrative)
    cells = []
    step = 2 * cr + 0.6
    for j in range(-9, 10):
        for i in range(-9, 10):
            x = fx + (i + (j % 2) * 0.5) * step
            y = fy + j * step * math.sqrt(3) / 2
            if math.hypot(x - fx, y - fy) < fr - cr - 2:
                cells.append(((i, j), x, y))
    d.group('thin')
    d.line((fx - fr - 10, fy), (fx + fr + 10, fy))
    d.line((fx, fy - fr - 10), (fx, fy + fr + 10))
    for k in range(1, 3):                       # thirds of the large square, the small square's grid
        d.line((bx0 + k * small, by0), (bx0 + k * small, by0 + big))
        d.line((bx0, by0 + k * small), (bx0 + big, by0 + k * small))
    d.line((250, 150), (350, 150))
    d.line((300, 100), (300, 200))
    d.group()
    d.circle(fx, fy, fr)                         # the field stop
    d.line((bx0, by0), (bx0 + big, by0), (bx0 + big, by0 + big), (bx0, by0 + big), closed=True)
    d.line((bx0, by0), (bx0 + small, by0), (bx0 + small, by0 + small), (bx0, by0 + small), closed=True)
    d.group('mid')
    for key, x, y in cells:                     # the ghosts
        if key not in fetal:
            d.circle(x, y, cr)
    d.group()
    for key, x, y in cells:                     # the fetal cells, solid and hatched
        if key in fetal:
            d.circle(x, y, cr)
            _hatch_circle(d, x, y, cr - 0.8, step=2.2)
    # the coated cell
    cx, cy, r = 300, 150, 42
    d.circle(cx, cy, r)
    d.circle(cx, cy, r - 12)                     # the biconcave dip, seen face on
    d.group('mid')
    for a in range(0, 360, 30):
        sx, sy = _pt(cx, cy, r + 22, a)          # the stem's free end (the Fc tail)
        kx, ky = _pt(cx, cy, r + 10, a)          # the hinge
        l1 = _pt(cx, cy, r + 1, a - 7)
        l2 = _pt(cx, cy, r + 1, a + 7)
        d.line((sx, sy), (kx, ky))
        d.line(l1, (kx, ky), l2)
        for p in (l1, l2):                       # the D sites the arms hold
            d.circle(p[0], p[1], 1.4)
    d.group('mid')
    d.line((bx0 + small / 2, by0 + small / 2), (24, 30))
    d.text(10, 24, 'SMALL SQUARE', size=7, anchor='start')
    d.line((bx0 + big, by0 + big), (236, 244))
    d.text(238, 248, 'LARGE SQUARE', size=7, anchor='start')
    d.text(fx - 20, 290, 'GHOSTS AND FETAL CELLS, x400', size=7)
    d.text(cx, 82, 'ANTI-D (IgG)', size=7)
    d.text(cx, 222, 'D+ FETAL CELL', size=7)
    d.text(cx + 10, 274, 'CLEARED BEFORE', size=7)
    d.text(cx + 10, 285, 'IT SENSITIZES', size=7)
    return d


def gift_relationship():
    d = D()
    # Left: a unit of whole blood in its bag with the label the FDA required from May 1978, naming
    # the donor "paid" or "volunteer". Right: where the blood came from, as two stacked columns of
    # the same height: England and Wales, all voluntary; the United States in 1965-67 by Titmuss's
    # estimates (about a third paid, a little over half exchanged for blood, about 5% from captive
    # donors, about 10% voluntary), as Solow summarized them. Shares are approximate.
    # the bag: a rounded rectangle with two ports above and a tube below
    x0, y0, w, h, rr = 36, 46, 112, 176, 14
    pts = []
    for (ccx, ccy, a0) in ((x0 + w - rr, y0 + rr, -90), (x0 + w - rr, y0 + h - rr, 0),
                           (x0 + rr, y0 + h - rr, 90), (x0 + rr, y0 + rr, 180)):
        for k in range(7):
            pts.append(_pt(ccx, ccy, rr, a0 + k * 15))
    base, top = 250, 70
    cols = [(222, [(1.0, 'VOLUNTARY')], 'E. AND W.'),
            (296, [(0.33, 'PAID'), (0.52, 'EXCHANGED'), (0.05, 'CAPTIVE'), (0.10, 'VOLUNTARY')], 'US 1965-67')]
    cw = 46
    d.group('thin')
    for y in range(top, base + 1, 18):           # a tenth of the column, every 18 units
        d.line((188, y), (192, y))
    d.line((190, top), (190, base))
    d.line((x0 + w / 2, 20), (x0 + w / 2, 286))
    d.group()
    d.line(*pts, closed=True)
    d.line((x0 + 34, y0), (x0 + 34, y0 - 16), (x0 + 44, y0 - 16), (x0 + 44, y0))      # a port
    d.line((x0 + 68, y0), (x0 + 68, y0 - 16), (x0 + 78, y0 - 16), (x0 + 78, y0))      # a port
    d.line((x0 + w / 2, y0 + h), (x0 + w / 2 - 4, y0 + h + 30), (x0 + w / 2 + 14, y0 + h + 52))  # the tube
    for cxl, parts, name in cols:
        d.line((cxl - cw / 2, top), (cxl + cw / 2, top), (cxl + cw / 2, base), (cxl - cw / 2, base), closed=True)
    d.group('mid')
    # the label on the bag
    lx0, ly0, lw, lh = x0 + 14, y0 + 40, w - 28, 92
    d.line((lx0, ly0), (lx0 + lw, ly0), (lx0 + lw, ly0 + lh), (lx0, ly0 + lh), closed=True)
    d.line((lx0, ly0 + 22), (lx0 + lw, ly0 + 22))
    d.line((lx0, ly0 + 64), (lx0 + lw, ly0 + 64))
    d.line((lx0 + 6, ly0 + 46), (lx0 + 12, ly0 + 52), (lx0 + 18, ly0 + 40))             # a tick in the box
    d.line((lx0 + 4, ly0 + 38), (lx0 + 20, ly0 + 38), (lx0 + 20, ly0 + 56), (lx0 + 4, ly0 + 56), closed=True)
    # the columns' divisions, from the base up, with hatching for paid blood
    for cxl, parts, name in cols:
        y = base
        for share, lab in parts:
            y2 = y - share * (base - top)
            d.line((cxl - cw / 2, y2), (cxl + cw / 2, y2))
            if lab == 'PAID':
                segs = []
                for k in range(0, int(y - y2) + cw, 7):
                    a = (cxl - cw / 2, y - k)
                    b = (cxl - cw / 2 + k, y)
                    # clip the 45-degree line to the band
                    ax, ay = a
                    if ay < y2:
                        ax, ay = ax + (y2 - ay), y2
                    bx, by = b
                    if bx > cxl + cw / 2:
                        by, bx = by - (bx - (cxl + cw / 2)), cxl + cw / 2
                    if ay <= by and ax <= bx:
                        segs.append([(ax, ay), (bx, by)])
                d.lines(segs)
            y = y2
    d.group('mid')
    d.text(lx0 + lw / 2, ly0 + 14, 'WHOLE BLOOD', size=7)
    d.text(lx0 + 24, ly0 + 50, 'VOLUNTEER', size=7, anchor='start')
    d.text(lx0 + lw / 2, ly0 + 80, 'DONOR', size=7)
    for cxl, parts, name in cols:
        d.text(cxl, base + 14, name, size=7)
    y = base
    for share, lab in cols[1][1]:
        y2 = y - share * (base - top)
        if share >= 0.1:
            d.text(cols[1][0] + cw / 2 + 4, (y + y2) / 2 + 3, lab, size=7, anchor='start')
        y = y2
    d.text(cols[0][0], (top + base) / 2 + 3, 'ALL', size=7)
    d.text(x0 + w / 2, 292, 'LABEL REQUIRED FROM MAY 1978', size=7)
    return d


def hepatitis():
    d = D()
    # Ouchterlony double diffusion as Alter and Blumberg ran it: a lantern slide (3 1/4 by 4 in)
    # coated with 0.9% agar, a "7 cup" pattern cut in it. The antiserum from a transfused hemophilia
    # patient sits in the centre well; panel sera in the six around it. Where antigen and antibody
    # meet in proportion a precipitin line forms between the wells: here against one serum only.
    # Right: the line in section across the gel, two diffusion fronts meeting.
    sx, sy, sw, sh = 24, 44, 200, 246 * 200 / 300   # the slide, 82.5 x 101.6 mm, drawn landscape
    sw, sh = 246, 200
    cx, cy = sx + sw / 2, sy + sh / 2
    R, rw = 62, 11                                   # well spacing and well radius
    wells = [_pt(cx, cy, R, a) for a in range(-90, 270, 60)]
    d.group('thin')
    for wx, wy in wells:
        d.line((cx, cy), (wx, wy))
    d.circle(cx, cy, R)
    d.line((300, 92), (300, 248))
    d.line((300, 248), (390, 248))
    d.group()
    d.line((sx, sy), (sx + sw, sy), (sx + sw, sy + sh), (sx, sy + sh), closed=True)
    d.line((sx + 8, sy + 8), (sx + sw - 8, sy + 8), (sx + sw - 8, sy + sh - 8), (sx + 8, sy + sh - 8), closed=True)
    d.circle(cx, cy, rw)
    for wx, wy in wells:
        d.circle(wx, wy, rw)
    d.group('mid')
    # the precipitin line against the first well: an arc nearer the antigen well, bowed toward it
    wx, wy = wells[1]
    ang = math.degrees(math.atan2(wy - cy, wx - cx))
    arc_c = _pt(cx, cy, R * 0.58 - 30, ang)         # a centre behind the line, toward the antiserum
    d.arc(arc_c[0], arc_c[1], 30, ang - 32, ang + 32, n=18)
    d.arc(arc_c[0], arc_c[1], 31.2, ang - 30, ang + 30, n=18)
    # the Ag (lipoprotein) lines that most sera gave, fainter, against two wells
    for k in (3, 5):
        wx2, wy2 = wells[k]
        a2 = math.degrees(math.atan2(wy2 - cy, wx2 - cx))
        c2 = _pt(cx, cy, R * 0.45 - 30, a2)
        d.arc(c2[0], c2[1], 30, a2 - 22, a2 + 22, n=14)
    # the section: concentration falling away from each well, the line where they cross
    xs = [300 + k * 3 for k in range(31)]
    up = [(x, 248 - 140 * math.exp(-((x - 300) / 38) ** 2)) for x in xs]
    down = [(x, 248 - 140 * math.exp(-((x - 390) / 38) ** 2)) for x in xs]
    d.line(*up)
    d.line(*down)
    d.line((345, 248), (345, 120))
    d.group('mid')
    d.text(cx, sy - 8, 'LANTERN SLIDE, 0.9% AGAR', size=7)
    d.text(cx, cy + 3, 'AB', size=7)
    d.text(wells[1][0] + 16, wells[1][1] + 3, 'AU+', size=7, anchor='start')
    d.text(300, 262, 'ANTISERUM', size=7, anchor='middle')
    d.text(390, 262, 'SERUM', size=7, anchor='end')
    d.text(345, 112, 'LINE', size=7)
    return d


PLATES = {'rhogam': rhogam, 'gift-relationship': gift_relationship, 'hepatitis': hepatitis}
