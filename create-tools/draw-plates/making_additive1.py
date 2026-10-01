"""Plates for How We Build's Layer by layer segment, part additive1 (sprint 026):
stereolithography, laser sintering and fused deposition modelling."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _bead(x0, y0, w, h, n=10):
    """An extruded bead in section, as Slic3r models it: a rectangle w wide and h high
    with semicircular ends of diameter h. (x0, y0) is its top-left corner."""
    r = h / 2
    cy = y0 + r
    pts = [(x0 + r, y0), (x0 + w - r, y0)]
    pts += [(x0 + w - r + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in [-90 + 180 * i / n for i in range(1, n)]]
    pts += [(x0 + w - r, y0 + h), (x0 + r, y0 + h)]
    pts += [(x0 + r + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in [90 + 180 * i / n for i in range(1, n)]]
    return pts


def fdm():
    d = D()
    # the hot end, drawn at 9 px per mm except the layers, which are exaggerated
    s = 9
    fx = 96                               # the filament's axis
    fr = 1.75 / 2 * s                     # a 1.75 mm filament
    by0, by1 = 128, 180                   # the heater block
    tip = 222                             # the nozzle's tip
    nr = 0.4 / 2 * s                      # a 0.4 mm orifice
    lh = 6                                # one layer, drawn 30 times its 0.2 mm
    top = tip + lh                        # the top of the layer below the bead being laid
    bed = top + 3 * lh
    d.group('thin')
    d.line((fx, 14), (fx, bed + 10))                                  # the axis
    d.line((18, bed), (232, bed))                                     # the bed
    for k in range(1, 4):
        d.line((24, bed - k * lh), (226, bed - k * lh))
    # the leader to the detail: a circle round the fresh bead, and a line out to the section
    d.circle(fx - 22, tip + lh / 2, 13)
    d.line((fx - 9, tip - 6), (258, 136))
    d.group()
    # the filament, gripped between two rollers, into the block, through the nozzle
    d.lines([[(fx - fr, 10), (fx - fr, by1)], [(fx + fr, 10), (fx + fr, by1)]])
    for side in (-1, 1):
        d.circle(fx + side * (fr + 14), 62, 14)
    d.line((fx - 34, by0), (fx + 34, by0), (fx + 34, by1), (fx - 34, by1), closed=True)
    d.line((fx - 16, by1), (fx - nr, tip), (fx + nr, tip), (fx + 16, by1))
    # the bead laid behind the moving nozzle, on the three layers before it
    d.line((24, tip), (fx - nr - 2, tip), (fx - nr, tip + lh))
    d.line((24, top), (fx + nr, top))
    d.group('mid')
    # the rollers' rotation and the feed, the heater cartridge and sensor, the melt in the bore
    for side, a0, a1 in ((-1, 200, 330), (1, 210, 340)):
        cx = fx + side * (fr + 14)
        d.arc(cx, 62, 20, a0 if side < 0 else 180 - a0, a1 if side < 0 else 180 - a1, n=14)
    d.lines([[(fx, 92), (fx, 112)], [(fx - 4, 106), (fx, 112), (fx + 4, 106)]])
    d.circle(fx - 20, 154, 8)
    d.circle(fx + 22, 166, 3)
    melt = []
    for i in range(9):
        y = by0 + 34 + i * 2.6
        melt.append([(fx - fr + i * 0.8, y), (fx + fr - i * 0.8, y)])
    d.lines(melt)
    # the direction of travel
    d.lines([[(fx + 24, tip - 10), (fx + 58, tip - 10)], [(fx + 52, tip - 14), (fx + 58, tip - 10), (fx + 52, tip - 6)]])
    # the bead in section, at 150 px per mm: two layers of two beads, spaced as Slic3r spaces them
    k = 150
    w, h = 0.45 * k, 0.20 * k
    sp = (0.45 - 0.20 * (1 - math.pi / 4)) * k
    x0, y1 = 262, 196
    d.group()
    for row in range(2):
        for col in range(2):
            d.line(*_bead(x0 + col * sp, y1 - (row + 1) * h, w, h), closed=True)
    d.group('thin')
    d.line((x0 - 8, y1), (x0 + sp + w + 8, y1))
    for col in range(2):
        cx = x0 + col * sp + w / 2
        d.line((cx, y1 - 2 * h - 14), (cx, y1 + 8))
    # dimensions: the width of one bead, the height of one layer, the spacing between centres
    d.line((x0, y1 - 2 * h - 22), (x0 + w, y1 - 2 * h - 22))
    d.lines([[(x0, y1 - 2 * h - 26), (x0, y1 - 2 * h - 18)], [(x0 + w, y1 - 2 * h - 26), (x0 + w, y1 - 2 * h - 18)]])
    xr = x0 - 12
    d.line((xr, y1 - h), (xr, y1))
    d.lines([[(xr - 4, y1 - h), (xr + 4, y1 - h)], [(xr - 4, y1), (xr + 4, y1)]])
    d.line((x0 + w / 2, y1 + 16), (x0 + sp + w / 2, y1 + 16))
    d.group('mid')
    d.text(x0 + w / 2, y1 - 2 * h - 30, 'w 0.45', size=8)
    d.text(xr - 6, y1 - h / 2 + 3, 'h 0.2', size=8, anchor='end')
    d.text(x0 + sp / 2 + w / 2, y1 + 30, 'SPACING 0.41', size=8)
    d.text(fx + 46, 66, 'FILAMENT 1.75', size=8, anchor='start')
    d.text(fx + 42, by0 + 22, '210 °C', size=8, anchor='start')
    d.text(fx + 12, tip + 3, '0.4', size=8, anchor='start')
    d.text(x0 + sp / 2 + w / 2, 262, 'BEADS IN SECTION, MM', size=8)
    return d


PLATES = {'fdm': fdm}


def stereolithography():
    d = D()
    # the vat in section: resin, the elevator and its part, the laser and its scanning mirror
    vx0, vx1, vy0, vy1 = 26, 238, 120, 262       # vat walls and floor
    surf = 140                                   # the resin's surface
    lh = 7                                       # one layer, drawn about 70 times its 0.1 mm
    lx, ly = 64, 34                              # the laser
    mx, my = 150, 40                             # the scanning mirror
    spot = (176, surf)
    d.group('thin')
    d.line((vx0 - 10, surf), (vx1 + 10, surf))
    for k in range(1, 7):                        # the layers already cured, as construction
        d.line((112, surf + k * lh), (204, surf + k * lh))
    d.line((mx, my), (mx - 30, surf), )          # the mirror's sweep, one edge
    d.line((mx, my), (214, surf))                #   and the other
    d.group()
    d.line((vx0, vy0), (vx0, vy1), (vx1, vy1), (vx1, vy0))
    # the part: a block with a narrower neck, hanging under the surface from the platform
    part = [(112, surf), (204, surf), (204, surf + 3 * lh), (180, surf + 3 * lh), (180, surf + 6 * lh),
            (204, surf + 6 * lh), (204, surf + 8 * lh), (112, surf + 8 * lh), (112, surf + 6 * lh),
            (136, surf + 6 * lh), (136, surf + 3 * lh), (112, surf + 3 * lh)]
    d.line(*part, closed=True)
    py = surf + 8 * lh
    d.line((92, py), (226, py), (226, py + 6), (92, py + 6), closed=True)      # the platform
    d.line((222, py), (222, 96), (250, 96))                                    # its arm, up out of the vat
    # the laser, the beam to the mirror and down to the spot
    d.line((lx - 30, ly - 9), (lx + 22, ly - 9), (lx + 22, ly + 9), (lx - 30, ly + 9), closed=True)
    d.line((lx + 22, ly), (mx, my - 6), (mx + 6, my), *[spot])
    d.group('mid')
    d.line((mx - 9, my - 9), (mx + 9, my + 9))                                  # the mirror
    d.circle(spot[0], spot[1], 4)
    # the recoater blade, above the surface, and the resin's dashes
    d.line((60, surf - 8), (60, surf - 2), (96, surf - 2), (96, surf - 8), closed=True)
    dashes = []
    for row in range(5):
        y = surf + 14 + row * 22
        for col in range(6):
            x = vx0 + 14 + col * 34 + (row % 2) * 17
            if not (106 < x < 212 and y < py + 10):
                dashes.append([(x, y), (x + 8, y)])
    d.lines(dashes)
    d.lines([[(244, 86), (244, 104)], [(240, 90), (244, 86), (248, 90)], [(240, 100), (244, 104), (248, 100)]])
    # the working curve: log dose across, depth down, a straight line from the surface dose to Ec
    gx0, gx1, gy0 = 278, 384, 124
    zs = 0.7                                       # px per micrometre
    lo, hi = math.log10(3), math.log10(200)
    X = lambda e: gx0 + (math.log10(e) - lo) / (hi - lo) * (gx1 - gx0)
    Y = lambda z: gy0 + z * zs
    Dp, Ec, E0 = 53, 6.3, 106.8
    d.group('thin')
    d.line((gx0, gy0), (gx1, gy0))
    d.line((gx0, gy0), (gx0, Y(200)))
    for e in (10, 100):
        d.line((X(e), gy0 - 3), (X(e), gy0 + 3))
    d.line((X(Ec), gy0), (X(Ec), Y(200)))                      # Ec
    for z in (100, 150):
        d.line((gx0, Y(z)), (X(Ec) + 46, Y(z)))
    d.line((X(E0), gy0 - 8), (X(E0), gy0))
    d.group()
    d.line(*[(X(E0 * math.exp(-z / Dp)), Y(z)) for z in range(0, 151, 10)])
    d.group('mid')
    d.text(lx - 4, ly + 22, 'UV LASER', size=8)
    d.text(X(Ec) + 4, Y(190), 'Ec', size=8, anchor='start')
    d.text(gx1, Y(100) - 3, 'LAYER', size=8, anchor='end')
    d.text(gx1, Y(150) - 3, 'CURED', size=8, anchor='end')
    d.text((gx0 + gx1) / 2, gy0 - 14, 'LOG DOSE', size=8)
    d.text(gx0 - 6, gy0 + 40, 'DEPTH', size=8, anchor='end')
    d.text(200, 284, 'THE VAT IN SECTION · THE DOSE WITH DEPTH', size=8)
    return d


PLATES['stereolithography'] = stereolithography


def laser_sintering():
    d = D()
    bed = 150                                  # the powder surface in both cylinders
    fx0, fx1 = 22, 92                          # the feed cylinder
    bx0, bx1 = 112, 232                        # the build cylinder
    floor_f, floor_b = 214, 248                # their pistons: the feed's risen, the build's lowered
    lh = 6                                     # one layer, drawn 60 times its 0.1 mm
    lx, ly = 54, 32                            # the laser
    gx, gy = 172, 40                           # the scanning mirrors
    d.group('thin')
    d.line((12, bed), (244, bed))
    for k in range(1, 15):                     # the build's layers, as construction
        y = bed + k * lh
        if y < floor_b:
            d.line((bx0, y), (bx1, y))
    d.line((gx, gy), (bx0 + 10, bed))          # the reach of the mirrors
    d.line((gx, gy), (bx1 - 10, bed))
    d.group()
    # the two cylinders and their pistons
    d.line((fx0, bed - 20), (fx0, 270), (fx1, 270), (fx1, bed - 20))
    d.line((bx0, bed - 20), (bx0, 270), (bx1, 270), (bx1, bed - 20))
    d.line((fx0 + 2, floor_f), (fx1 - 2, floor_f))
    d.line((bx0 + 2, floor_b), (bx1 - 2, floor_b))
    d.lines([[(57, floor_f), (57, 268)], [(172, floor_b), (172, 268)]])
    # the part in the powder: a column carrying a wide, unsupported shelf
    part = [(140, bed + 14 * lh - 6), (166, bed + 14 * lh - 6), (166, bed + 4 * lh), (210, bed + 4 * lh),
            (210, bed + 2 * lh), (140, bed + 2 * lh)]
    d.line(*part, closed=True)
    # the laser, its beam to the mirrors and down to the bed
    d.line((lx - 32, ly - 9), (lx + 22, ly - 9), (lx + 22, ly + 9), (lx - 32, ly + 9), closed=True)
    d.line((lx + 22, ly), (gx - 6, ly), (gx, gy), (196, bed))
    d.group('mid')
    d.line((gx - 8, ly - 6), (gx + 4, ly + 6))
    d.line((gx - 4, gy + 4), (gx + 8, gy - 2))
    d.circle(196, bed, 3)
    # the roller spreading a fresh layer from the feed onto the build, and its direction
    d.circle(102, bed - 6, 6)
    d.arc(102, bed - 6, 10, 200, 330, n=10)
    d.lines([[(86, bed - 22), (118, bed - 22)], [(112, bed - 26), (118, bed - 22), (112, bed - 18)]])
    # powder: dots in the feed and around the part in the build
    dots = []
    for row in range(16):
        y = bed + 5 + row * 6
        for col in range(20):
            x = fx0 + 5 + col * 6.2 + (row % 2) * 3
            if fx0 + 2 < x < fx1 - 2 and y < floor_f - 2:
                dots.append([(x, y), (x + 0.6, y)])
            xb = bx0 + 5 + col * 6.2 + (row % 2) * 3
            inside = (140 <= xb <= 166 and bed + 2 * lh <= y <= bed + 14 * lh - 6) or \
                     (140 <= xb <= 210 and bed + 2 * lh <= y <= bed + 4 * lh)
            if bx0 + 2 < xb < bx1 - 2 and y < floor_b - 2 and not inside:
                dots.append([(xb, y), (xb + 0.6, y)])
    d.lines(dots)
    # the hatch, seen from above: scan lines h apart, the spot drawn along one, the turn at each end
    hx0, hx1, hy0 = 280, 384, 92
    h = 16
    d.group('thin')
    d.line((hx0 - 8, hy0 - 16), (hx0 - 8, hy0 + 5 * h + 8))
    d.lines([[(hx0 - 12, hy0), (hx0 - 4, hy0)], [(hx0 - 12, hy0 + h), (hx0 - 4, hy0 + h)]])
    d.group()
    path = []
    for k in range(6):
        y = hy0 + k * h
        path += [(hx0, y), (hx1, y)] if k % 2 == 0 else [(hx1, y), (hx0, y)]
    d.line(*path)
    d.group('mid')
    for k in range(7):
        d.circle(hx0 + 8 + k * 15, hy0 + 2 * h, 6)
    d.lines([[(hx1 - 12, hy0 - 4), (hx1 - 4, hy0), (hx1 - 12, hy0 + 4)]])
    d.text(hx0 - 14, hy0 + h / 2 + 3, 'h', size=8, anchor='end')
    d.text(hx1, hy0 - 10, 'v', size=8, anchor='end')
    d.text((hx0 + hx1) / 2, hy0 + 5 * h + 24, 'E = P ÷ (h · z · v)', size=8)
    d.text(lx - 5, ly + 22, 'LASER', size=8)
    d.text(57, 282, 'FEED', size=8)
    d.text(172, 282, 'BUILD', size=8)
    d.text(332, hy0 + 5 * h + 40, 'THE HATCH, FROM ABOVE', size=8)
    return d


PLATES['laser-sintering'] = laser_sintering
