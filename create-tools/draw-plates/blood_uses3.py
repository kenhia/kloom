"""Plates for In the Blood, the end of What we do with blood and Today (sprint 028, part uses3).

See plates_for.py. Every plate is a schematic: the geometry is computed, the sizes are not to scale.
"""
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


def _dashed(d, p, q, dash=4, gap=3):
    """A dashed straight line from p to q, as one path of short segments."""
    length = math.dist(p, q)
    ux, uy = (q[0] - p[0]) / length, (q[1] - p[1]) / length
    segs, s = [], 0.0
    while s < length:
        e = min(s + dash, length)
        segs.append([(p[0] + ux * s, p[1] + uy * s), (p[0] + ux * e, p[1] + uy * e)])
        s = e + gap
    d.lines(segs)


def _y(d, tip_r, fork_r, stem_r, cx, cy, a, spread=7):
    """An antibody, a Y, lying along the radius at angle `a`: its two arms reach out to `tip_r`
    (spread a few degrees either side), they fork at `fork_r`, and the stem runs in to `stem_r`."""
    fork = _pt(cx, cy, fork_r, a)
    d.lines([[_pt(cx, cy, tip_r, a - spread), fork, _pt(cx, cy, tip_r, a + spread)],
             [fork, _pt(cx, cy, stem_r, a)]])


def hiv_blood():
    d = D()
    # Left: one well of a microtitre plate in section, enlarged. HIV antigen is fixed to the plastic;
    # the donor's antibody (if any) binds it; an enzyme-linked anti-human antibody binds that; the enzyme
    # turns a colourless substrate coloured. Right: a strip of eight wells and their colour, read
    # against a cut-off. Every height in the strip is invented, to show the reading, not a result.
    cx, cy, R = 110, 172, 80                  # the well's rounded bottom
    top = 52
    angles = [48, 90, 132]                    # where the antibodies stand on the bottom
    d.group('thin')
    d.line((cx, top - 8), (cx, cy + R + 10))                     # the well's axis
    for r in (74, 47, 24):                                       # the three layers, as arcs
        d.arc(cx, cy, r, 20, 160, n=32)
    x0, x1, base, cut = 232, 388, 262, 196                       # the strip's reading
    d.line((x0, base), (x1, base))
    d.line((x0, base), (x0, 150))
    d.group()
    # the well: two walls and a rounded bottom, the plate's top surface either side
    d.line((cx - R - 14, top), (cx - R, top), (cx - R, cy))
    d.arc(cx, cy, R, 180, 0, n=48)
    d.line((cx + R, cy), (cx + R, top), (cx + R + 14, top))
    # the strip of eight wells, seen from above
    wells = [x0 + 12 + 20 * i for i in range(8)]
    for x in wells:
        d.circle(x, 72, 7)
    d.group('mid')
    # the liquid's surface in the well
    d.line((cx - R, 84), (cx + R, 84))
    # antigen on the plastic, the donor's antibody on it, the anti-human antibody on that, its enzyme
    for a in angles:
        x, y = _pt(cx, cy, 77, a)
        d.circle(x, y, 3)
        _y(d, 73, 63, 50, cx, cy, a)
        _y(d, 49, 40, 29, cx, cy, a, spread=9)
        ex, ey = _pt(cx, cy, 25, a)
        d.line((ex - 2.5, ey - 2.5), (ex + 2.5, ey - 2.5), (ex + 2.5, ey + 2.5), (ex - 2.5, ey + 2.5), closed=True)
    for a in (20, 69, 111, 160):                                 # antigen with nothing on it
        x, y = _pt(cx, cy, 77, a)
        d.circle(x, y, 3)
    # coloured product, made by the enzymes, spreading into the liquid
    for i in range(11):
        x = cx - 50 + 10 * i
        y = 112 + 14 * math.sin(i * 1.7)
        d.circle(x, y, 1.6)
    # the strip's colour as bars: two controls, then six donations, one above the cut-off
    heights = [8, 92, 10, 12, 7, 78, 11, 9]
    for x, h in zip(wells, heights):
        d.line((x - 4, base), (x - 4, base - h), (x + 4, base - h), (x + 4, base))
        d.line((x, 80), (x, base - h - 4))
    _dashed(d, (x0, cut), (x1, cut))
    d.group('mid')
    d.text(cx - R - 16, top - 6, 'PLATE', size=7, anchor='start')
    d.text(cx + R + 5, 210, 'ANTIGEN', size=7, anchor='start')
    d.text(cx, 290, 'DONOR ANTIBODY + ENZYME-LINKED ANTI-HUMAN', size=7)
    d.text(cx, 76, 'COLOUR', size=7)
    d.text(wells[0], 58, 'NEG', size=7)
    d.text(wells[1], 58, 'POS', size=7)
    d.text(x1, cut - 5, 'CUT-OFF', size=7, anchor='end')
    d.text((x0 + x1) / 2, 278, 'SIX DONATIONS', size=7)
    return d


def _kidney(cx, cy, s):
    """A kidney's outline: an ellipse with its hilum pressed in on the side facing +x."""
    pts = []
    for i in range(73):
        t = 2 * math.pi * i / 72
        x, y = 0.62 * math.cos(t), math.sin(t)
        x -= 0.28 * math.exp(-((t % (2 * math.pi)) ** 2) / 0.18)          # the notch at t = 0
        x -= 0.28 * math.exp(-((t - 2 * math.pi) ** 2) / 0.18)
        pts.append((cx + s * x, cy + s * y))
    return pts


def epo():
    d = D()
    # The feedback loop: cells in the kidney sense oxygen; when it falls they make erythropoietin; the
    # hormone reaches the marrow, which makes more red cells; the red cells carry more oxygen, and the
    # kidney makes less. An inset shows the drug's source: the human gene in a hamster ovary cell.
    cx, cy, R = 206, 146, 104
    kid, mar, red = 180, 300, 60                         # the stations' angles on the loop
    d.group('thin')
    d.circle(cx, cy, R)
    for a in (kid, mar, red):
        d.line((cx, cy), _pt(cx, cy, R, a))
    d.group()
    # the kidney, with its hilum facing the loop's centre
    kx, ky = _pt(cx, cy, R, kid)
    d.line(*_kidney(kx, ky, 40), closed=True)
    # a length of long bone in section, its marrow cavity inside, at the second station
    mx, my = _pt(cx, cy, R, mar)
    d.line((mx - 46, my - 13), (mx + 46, my - 13))
    d.line((mx - 46, my + 13), (mx + 46, my + 13))
    d.arc(mx - 46, my, 17, 90, 270, n=20)
    d.arc(mx + 46, my, 17, -90, 90, n=20)
    # red cells, face on, leaving the marrow at the third station
    rx, ry = _pt(cx, cy, R, red)
    cells = [(rx - 18, ry - 6), (rx + 4, ry + 8), (rx + 24, ry - 8)]
    for x, y in cells:
        d.circle(x, y, 9)
    # the inset: a hamster ovary cell with the human gene on a plasmid, its nucleus, and its product
    ix, iy = 50, 46
    d.ellipse(ix, iy, 34, 22)
    d.group('mid')
    d.line((mx - 40, my - 6), (mx + 40, my - 6))                     # the marrow cavity's walls
    d.line((mx - 40, my + 6), (mx + 40, my + 6))
    for i in range(9):                                               # cells in the marrow
        d.circle(mx - 32 + 8 * i, my + (2 if i % 2 else -2), 1.4)
    for x, y in cells:                                               # each red cell's pale centre
        d.circle(x, y, 3.5)
    for i in range(5):                                               # blood vessels at the hilum
        a = -40 + 20 * i
        d.line(_pt(kx + 10, ky, 6, a), _pt(kx + 10, ky, 18, a))
    # the loop's three arcs, each with an arrowhead where it arrives
    for a0, a1 in ((kid + 22, mar - 18), (mar + 22, 360 + red - 20), (red + 20, kid - 24)):
        d.arc(cx, cy, R, a0, a1, n=36)
        _arrow(d, _pt(cx, cy, R, a1 - 4), _pt(cx, cy, R, a1), size=6)
    d.ellipse(ix + 4, iy, 11, 8)                                    # the nucleus
    d.circle(ix - 20, iy - 6, 6)                                    # the plasmid carrying the gene
    tip = _pt(cx, cy, R - 4, 222)
    d.line((ix + 36, iy + 6), tip)
    _arrow(d, (ix + 36, iy + 6), tip)
    d.group('mid')
    d.text(kx, ky + 54, 'KIDNEY', size=7)
    d.text(mx, my - 22, 'MARROW', size=7)
    d.text(rx + 4, ry + 30, 'RED CELLS', size=7)
    lx, ly = _pt(cx, cy, R + 10, 262)
    d.text(lx, ly, 'EPO', size=7, anchor='end')
    lx, ly = _pt(cx, cy, R + 14, 120)
    d.text(lx - 6, ly + 6, 'MORE O₂, LESS EPO', size=7, anchor='middle')
    d.text(cx, cy + 3, 'O₂ SENSED IN KIDNEY', size=7)
    d.text(ix + 44, iy - 6, 'rhEPO', size=7, anchor='start')
    d.text(ix, iy + 34, 'CHO CELL + GENE', size=7)
    return d


def nat():
    d = D()
    # Minipool testing: a sample from each of sixteen donations goes into one pool; the pool's viral RNA
    # is amplified; a pool that crosses the threshold is taken apart, and each of its sixteen samples is
    # tested alone until the one donation that carried the virus is found. The curves are a sketch.
    d.group('thin')
    lx, ly, rx, pitch = 34, 56, 318, 18
    for i in range(4):                                            # both racks' grid lines
        for gx in (lx, rx):
            d.line((gx + pitch * i, ly - 10), (gx + pitch * i, ly + 3 * pitch + 10))
    ax0, ay0, ax1, ay1 = 120, 266, 288, 168                       # the amplification plot's axes
    d.line((ax0, ay0), (ax1, ay0))
    d.line((ax0, ay0), (ax0, ay1))
    d.group()
    # the sixteen donation samples, in a 4 by 4 rack seen from above
    for i in range(4):
        for j in range(4):
            d.circle(lx + pitch * i, ly + pitch * j, 6)
    # the pool: one tube in elevation
    px, py = 200, 52
    d.line((px - 12, py), (px - 12, py + 62))
    d.arc(px, py + 62, 12, 180, 0, n=16)
    d.line((px + 12, py + 62), (px + 12, py))
    d.line((px - 16, py), (px + 16, py))
    # the same sixteen samples, tested one by one
    for i in range(4):
        for j in range(4):
            d.circle(rx + pitch * i, ly + pitch * j, 6)
    d.group('mid')
    # sixteen lines gathering into the pool
    for j in range(4):
        d.line((lx + 3 * pitch + 8, ly + pitch * j), (px - 18, py + 24 + 4 * j))
    _arrow(d, (px - 40, py + 34), (px - 18, py + 36))
    # the reactive pool sent back to be taken apart
    d.line((px + 18, py + 30), (rx - 12, py + 30))
    _arrow(d, (px + 18, py + 30), (rx - 12, py + 30))
    # the amplification: a reactive pool's signal rising through the threshold, a clean pool's flat
    pos, neg = [], []
    for k in range(41):
        t = k / 40
        x = ax0 + (ax1 - ax0) * t
        pos.append((x, ay0 - 86 / (1 + math.exp(-14 * (t - 0.45)))))
        neg.append((x, ay0 - 4 - 2 * t))
    d.line(*pos)
    d.line(*neg)
    _dashed(d, (ax0, ay0 - 40), (ax1, ay0 - 40))
    # the one donation found: its circle doubled and crossed
    fx, fy = rx + pitch * 2, ly + pitch * 1
    d.circle(fx, fy, 3)
    d.lines([[(fx - 9, fy - 9), (fx + 9, fy + 9)], [(fx - 9, fy + 9), (fx + 9, fy - 9)]])
    # the pool's liquid
    d.line((px - 12, py + 20), (px + 12, py + 20))
    d.group('mid')
    d.text(lx + 27, ly - 18, '16 DONATIONS', size=7)
    d.text(px, py - 8, 'POOL', size=7)
    d.text(rx + 27, ly - 18, 'EACH ALONE', size=7)
    d.text(rx + 27, ly + 4 * pitch + 6, '1 OF 16', size=7)
    d.text(ax1, ay0 - 44, 'THRESHOLD', size=7, anchor='end')
    d.text(ax1, ay0 + 14, 'AMPLIFICATION TIME', size=7, anchor='end')
    d.text(ax0 + 6, ay1 + 4, 'SIGNAL', size=7, anchor='start')
    d.text(px + 64, py + 24, 'RESOLVE', size=7)
    return d


def _bag(d, x, y, w, h, r=10):
    """A blood bag in elevation: a rounded rectangle, with two ports at the top."""
    d.line((x + r, y), (x + w - r, y))
    d.arc(x + w - r, y + r, r, -90, 0, n=8)
    d.line((x + w, y + r), (x + w, y + h - r))
    d.arc(x + w - r, y + h - r, r, 0, 90, n=8)
    d.line((x + w - r, y + h), (x + r, y + h))
    d.arc(x + r, y + h - r, r, 90, 180, n=8)
    d.line((x, y + h - r), (x, y + r))
    d.arc(x + r, y + r, r, 180, 270, n=8)


def where_blood_is():
    d = D()
    # One donation, three products: the whole-blood bag after a hard spin, plasma above, a thin buffy
    # coat, red cells below, and the tubing that carries the plasma (and the platelets in it) off to
    # satellite bags. Layer heights are a sketch, near a normal hematocrit, not a measurement.
    bx, by, bw, bh = 46, 70, 92, 168
    plasma_y, buffy_y = by + 72, by + 80
    d.group('thin')
    d.line((bx - 18, by + bh), (bx + bw + 18, by + bh))                 # the bag's bench line
    d.line((bx - 10, plasma_y), (bx - 10, by + bh))                     # height of the packed cells
    d.line((bx - 14, plasma_y), (bx - 6, plasma_y))
    d.line((bx - 14, by + bh), (bx - 6, by + bh))
    d.line((bx + bw / 2, by - 8), (bx + bw / 2, by + bh + 8))           # the bag's axis
    d.group()
    _bag(d, bx, by, bw, bh)
    # the satellite bags: plasma, and platelets
    s1 = (262, 64, 70, 92)
    s2 = (262, 180, 70, 76)
    _bag(d, *s1)
    _bag(d, *s2)
    # tubing from the primary bag's top port, branching to each satellite
    t0 = (bx + 30, by)
    d.line(t0, (bx + 30, by - 30), (220, by - 30), (220, 168), (s2[0] + 14, 168), (s2[0] + 14, s2[1]))
    d.line((220, by - 30), (s1[0] + 14, by - 30), (s1[0] + 14, s1[1]))
    # the donor line, cut and sealed, from the other port
    d.line((bx + 62, by), (bx + 62, by - 22), (bx + 86, by - 40))
    d.group('mid')
    # the layers after the spin
    d.line((bx, plasma_y), (bx + bw, plasma_y))
    d.line((bx, buffy_y), (bx + bw, buffy_y))
    for i in range(10):                                                 # red cells packed below
        y = buffy_y + 10 + 14 * i
        if y < by + bh - 6:
            d.line((bx + 8, y), (bx + bw - 8, y))
    # what each satellite will hold, sketched as a level
    d.line((s1[0], s1[1] + 30), (s1[0] + s1[2], s1[1] + 30))
    d.line((s2[0], s2[1] + 50), (s2[0] + s2[2], s2[1] + 50))
    # the clamp and the flow towards the satellites
    _arrow(d, (220, 120), (220, 136))
    _arrow(d, (s1[0] - 20, by - 30), (s1[0] + 4, by - 30))
    d.lines([[(bx + 22, by - 36), (bx + 38, by - 24)], [(bx + 22, by - 24), (bx + 38, by - 36)]])
    d.group('mid')
    d.text(bx + bw + 8, plasma_y - 30, 'PLASMA', size=7, anchor='start')
    d.text(bx + bw + 8, buffy_y + 2, 'BUFFY COAT', size=7, anchor='start')
    d.text(bx + bw + 8, by + bh - 40, 'RED CELLS', size=7, anchor='start')
    d.text(s1[0] + s1[2] / 2, s1[1] + s1[3] + 14, 'PLASMA', size=7)
    d.text(s2[0] + s2[2] / 2, s2[1] + s2[3] + 14, 'PLATELETS', size=7)
    d.text(bx + 90, by - 44, 'DONOR LINE', size=7, anchor='start')
    d.text(bx + bw / 2, by + bh + 20, 'ONE DONATION, SPUN', size=7)
    return d


PLATES = {
    'hiv-blood': hiv_blood,
    'epo': epo,
    'nat': nat,
    'where-blood-is': where_blood_is,
}
