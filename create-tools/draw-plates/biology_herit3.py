"""Plates for The Story of Life's part herit3 (sprint 055): beadle-tatum, mcclintock. See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def _tube(d, cx, top, h, w):
    """A test tube, open at the top, with a round bottom (a half circle computed as a polyline)."""
    r = w / 2
    bottom = top + h - r
    pts = [(cx - r, top)]
    for k in range(13):
        a = math.pi - math.pi * k / 12
        pts.append((cx + r * math.cos(a), bottom + r * math.sin(a)))
    pts.append((cx + r, top))
    d.line(*pts)
    d.line((cx - r - 2, top), (cx + r + 2, top))                         # the lip


def _mycelium(d, cx, y, w):
    """A tuft of hyphae on the surface of the medium: short branching strokes, computed, not random."""
    n = 5
    for i in range(n):
        x = cx - w / 2 + 2 + i * (w - 4) / (n - 1)
        h = 7 + 3 * math.sin(i * 1.7)
        lean = (i - (n - 1) / 2) * 1.2
        tip = (x + lean, y - h)
        d.line((x, y), tip)
        d.line((x + lean * 0.5, y - h * 0.55), (x + lean * 0.5 + (2.2 if i % 2 else -2.2), y - h * 0.8))


def beadle_tatum():
    d = D()
    # Srb and Horowitz's arginine mutants (J. Biol. Chem. 154, 1944, Table I and text): each class of
    # mutant grown on minimal medium alone and with ornithine, citrulline or arginine added. A tuft is
    # growth; an empty surface is none. Below, the chain the pattern implies, with each class's block.
    cols = ['MINIMAL', '+ ORNITHINE', '+ CITRULLINE', '+ ARGININE']
    rows = [('WILD TYPE', 0), ('CLASS I · 4', 1), ('CLASS II · 2', 2), ('CLASS III · 1', 3)]
    # first column a strain grows in: wild type grows on all; class I needs ornithine or later, etc.
    x0, dx = 144, 70
    y0, dy = 46, 44
    tw, th = 16, 34
    level = 20                                                            # medium surface below the lip

    d.group('thin')
    for i in range(len(cols)):                                            # column guides
        x = x0 + i * dx
        d.line((x, y0 - 14), (x, y0 + 3 * dy + th + 4))
    for j in range(len(rows)):                                            # row rules
        y = y0 + j * dy + th + 6
        d.line((20, y), (392, y))
    d.line((40, 248), (372, 248))                                         # the chain's axis

    d.group()
    for j, (_, first) in enumerate(rows):
        for i in range(len(cols)):
            _tube(d, x0 + i * dx, y0 + j * dy, th, tw)
    # the chain: precursor -> ornithine -> citrulline -> arginine
    nodes = [(52, 'PRECURSOR'), (150, 'ORNITHINE'), (250, 'CITRULLINE'), (350, 'ARGININE')]
    for (xa, _), (xb, _) in zip(nodes, nodes[1:]):
        d.line((xa + 14, 248), (xb - 14, 248))
        _arrow(d, (xa + 14, 248), (xb - 14, 248), size=4)
    for x, _ in nodes:
        d.circle(x, 248, 5)

    d.group('mid')
    for j, (_, first) in enumerate(rows):
        for i in range(len(cols)):
            x, top = x0 + i * dx, y0 + j * dy
            surf = top + 19
            d.line((x - tw / 2 + 1, surf), (x + tw / 2 - 1, surf))       # the medium's surface
            if i >= first:
                _mycelium(d, x, surf, tw)
    for k, xm in enumerate((101, 200, 300)):                               # the blocks, class I, II, III
        d.line((xm - 5, 241), (xm + 5, 255))
        d.line((xm - 5, 255), (xm + 5, 241))

    d.group('mid')
    for i, c in enumerate(cols):
        d.text(x0 + i * dx, y0 - 18, c, size=7)
    for j, (r, _) in enumerate(rows):
        d.text(24, y0 + j * dy + 20, r, size=7, anchor='start')
    for x, n in nodes:
        d.text(x, 266, n, size=7)
    for xm, n in ((101, 'I'), (200, 'II'), (300, 'III')):
        d.text(xm, 236, n, size=7)
    d.text(200, 288, 'ARGININELESS NEUROSPORA · SRB AND HOROWITZ, 1944', size=7)
    return d


def mcclintock():
    d = D()
    # Above: the short arm of maize chromosome 9 as Creighton and McClintock (1931) and McClintock (1950)
    # give it, the knob at the tip and the order knob, C, Sh, Wx toward the centromere; Ds sits inserted
    # at C (the mutable c-m1 of 1950) and, with Ac present, leaves. Spacing schematic, not to map scale.
    # Below: a kernel, its aleurone colorless where Ds stays at C and spotted where it left; spot size
    # is how early in the kernel's growth the cell that founded it lost Ds. Spot positions are computed.
    y, h = 62, 14
    x_tip, x_cen, x_end = 46, 330, 372
    loci = [('C', 128), ('SH', 196), ('WX', 262)]

    d.group('thin')
    d.line((x_tip - 12, y), (x_end + 8, y))                              # the chromosome's axis
    for _, x in loci:
        d.line((x, y - 22), (x, y + 22))
    d.line((x_cen, y - 22), (x_cen, y + 22))
    cx, cy, rx, ry = 150, 200, 92, 66                                     # the kernel
    d.line((cx - rx - 10, cy), (cx + rx + 10, cy))
    d.line((cx, cy - ry - 10), (cx, cy + ry + 10))

    d.group()
    # the arm: a rounded bar pinched at the centromere, the knob a bulge at the tip
    top = [(x, y - h / 2) for x in range(x_tip + 8, x_cen - 6, 4)]
    d.line(*top, (x_cen - 6, y - h / 2), (x_cen, y - 3), (x_cen + 6, y - h / 2), (x_end, y - h / 2))
    bot = [(x, y + h / 2) for x in range(x_tip + 8, x_cen - 6, 4)]
    d.line(*bot, (x_cen - 6, y + h / 2), (x_cen, y + 3), (x_cen + 6, y + h / 2), (x_end, y + h / 2))
    d.arc(x_end, y, h / 2, -90, 90)
    d.ellipse(x_tip, y, 14, 11)                                           # the knob
    # the kernel: a rounded wedge, broad at the crown, narrowing to the tip cap
    pts = []
    for k in range(73):
        a = 2 * math.pi * k / 72
        sx = math.cos(a)
        sy = math.sin(a)
        w = rx * (1 - 0.36 * sy) if sy > 0 else rx                        # narrowing smoothly to the tip
        pts.append((cx + w * sx, cy + ry * sy))
    d.line(*pts, closed=True)

    d.group('mid')
    for k in range(6):                                                    # hatching on the knob
        xx = x_tip - 9 + k * 3.6
        d.line((xx, y - 7), (xx + 3, y + 7))
    _box(d, loci[0][1] - 9, y - h / 2 - 1, 18, h + 2)                     # Ds, inserted at C
    d.curve(f"M{loci[0][1]},{y - h / 2 - 2} Q{loci[0][1] + 20},{y - 40} {loci[0][1] + 44},{y - 30}")
    _arrow(d, (loci[0][1] + 30, y - 38), (loci[0][1] + 44, y - 30), size=4)
    _box(d, loci[0][1] + 46, y - 38, 18, 12)                              # Ds, having left
    # spots: three founded early (large), then progressively later and smaller, on a golden-angle spiral
    spots = []
    for k in range(34):
        r = 0.86 * math.sqrt((k + 0.5) / 34)
        a = k * 2.39996
        px, py = cx + r * rx * 0.8 * math.cos(a), cy + r * ry * 0.85 * math.sin(a)
        size = 9 if k % 11 == 0 else (5 if k % 4 == 0 else 2)
        spots.append((px, py, size))
    for px, py, s in spots:
        d.circle(px, py, s)
    d.arc(cx, cy, rx - 6, 200, 340, ry=ry - 6)                            # the aleurone layer, inside the skin

    d.group('mid')
    d.text(x_tip, y + 26, 'KNOB', size=7)
    for name, x in loci:
        d.text(x, y + 26, name, size=7)
    d.text(x_cen, y + 26, 'CENTROMERE', size=7)
    d.text(loci[0][1], y + 2.5, 'DS', size=7)
    d.text(loci[0][1] + 55, y - 29.5, 'DS', size=7)
    d.text(loci[0][1] + 55, y - 44, 'DS LEAVES · AC PRESENT', size=7)
    lx = cx + rx + 26
    big, small = spots[11], spots[26]                                     # a spot founded early, one late
    targets = [('ALEURONE', 150, (cx + (rx - 6) * math.cos(math.radians(320)), cy + (ry - 6) * math.sin(math.radians(320)))),
               ('SMALL SPOT · LATE', 176, (small[0] + small[2], small[1])),
               ('LARGE SPOT · EARLY', 204, (big[0] + big[2], big[1])),
               ('COLORLESS · DS AT C', 236, (cx + 62, cy + 40))]
    for label, ly, (tx, ty) in targets:
        d.text(lx + 4, ly + 2.5, label, size=7, anchor='start')
        d.line((lx, ly), (tx + 2, ty))
    d.text(200, 292, 'CHROMOSOME 9, SHORT ARM, AND A SPOTTED KERNEL · ZEA MAYS', size=7)
    return d


PLATES = {'beadle-tatum': beadle_tatum, 'mcclintock': mcclintock}
