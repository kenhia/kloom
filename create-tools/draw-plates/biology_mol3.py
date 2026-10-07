"""Plates for The Story of Life's part mol3 (sprint 055): the genetic code and the lac operon. See plates_for.py."""
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


BASES = 'UCAG'
# The standard code, codon by codon in UCAG order (first base, then second, then third).
_AA = ('Phe Phe Leu Leu Ser Ser Ser Ser Tyr Tyr Stop Stop Cys Cys Stop Trp '
       'Leu Leu Leu Leu Pro Pro Pro Pro His His Gln Gln Arg Arg Arg Arg '
       'Ile Ile Ile Met Thr Thr Thr Thr Asn Asn Lys Lys Ser Ser Arg Arg '
       'Val Val Val Val Ala Ala Ala Ala Asp Asp Glu Glu Gly Gly Gly Gly').split()


def _pol(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def genetic_code():
    d = D()
    # The codon wheel: the first base at the center, the second in the middle ring, the third outside,
    # each ring dividing its parent's angle by four (90°, 22.5°, 5.625°), clockwise from the top in UCAG
    # order. The outer arcs join codons that name the same amino acid, so the code's degeneracy shows as
    # their length. UUU, the first codon read (poly-U, May 1961), is hatched.
    cx, cy = 200, 148
    r0, r1, r2, r3, ra = 16, 44, 74, 104, 112
    start = -90
    step3 = 360 / 64

    def ang(i, n):
        return start + i * 360 / n

    d.group('thin')
    for r in (r0, r1, r2, r3):
        d.circle(cx, cy, r)
    for k in range(4):                                                    # the quarter lines, run long
        d.line(_pol(cx, cy, 6, ang(k, 4)), _pol(cx, cy, 128, ang(k, 4)))
    for k in range(64):                                                   # angle ticks outside the code
        d.line(_pol(cx, cy, 124, ang(k, 64)), _pol(cx, cy, 127 if k % 4 else 131, ang(k, 64)))

    d.group()
    d.circle(cx, cy, r3)
    for k in range(16):                                                   # second-base divisions
        d.line(_pol(cx, cy, r1, ang(k, 16)), _pol(cx, cy, r2, ang(k, 16)))
    for k in range(4):                                                    # first-base divisions
        d.line(_pol(cx, cy, r0, ang(k, 4)), _pol(cx, cy, r3, ang(k, 4)))
    # one arc per run of codons with the same amino acid
    runs, i = [], 0
    while i < 64:
        j = i
        while j + 1 < 64 and _AA[j + 1] == _AA[i]:
            j += 1
        runs.append((i, j))
        i = j + 1
    for i, j in runs:
        a0, a1 = start + i * step3 + 0.9, start + (j + 1) * step3 - 0.9
        d.arc(cx, cy, ra, a0, a1, n=max(2, (j - i + 1) * 3))

    d.group('mid')
    for k in range(64):                                                   # third-base divisions
        d.line(_pol(cx, cy, r2, ang(k, 64)), _pol(cx, cy, r3, ang(k, 64)))
    a0, a1 = start, start + step3                                         # hatch UUU
    for t in range(1, 6):
        r = r2 + (r3 - r2) * t / 6
        d.line(_pol(cx, cy, r, a0), _pol(cx, cy, r, a1))

    d.group('mid')
    for k, b in enumerate(BASES):
        p = _pol(cx, cy, (r0 + r1) / 2, ang(k, 4) + 45)
        d.text(p[0], p[1] + 2.5, b, size=7)
    for k in range(16):
        p = _pol(cx, cy, (r1 + r2) / 2, ang(k, 16) + 360 / 32)
        d.text(p[0], p[1] + 2.5, BASES[k % 4], size=7)
    for k in range(64):
        p = _pol(cx, cy, (r2 + r3) / 2 + 2, ang(k, 64) + step3 / 2)
        d.text(p[0], p[1] + 2.2, BASES[k % 4], size=6)

    d.group('mid')
    notes = [(0, 'UUU = PHE, MAY 1961', 'start'), (35, 'AUG = MET, START', 'end'),
             (10, 'STOP', 'start'), (14, 'STOP', 'start')]
    for idx, label, anchor in notes:
        mid = start + (idx + 0.5) * step3
        p = _pol(cx, cy, ra + 2, mid)
        q = _pol(cx, cy, 138, mid)
        x2 = q[0] + (24 if anchor == 'start' else -24)
        d.line(p, q, (x2, q[1]))
        d.text(x2 + (3 if anchor == 'start' else -3), q[1] + 2.5, label, size=7, anchor=anchor)
    d.text(200, 292, 'FIRST BASE AT THE CENTER, THIRD OUTSIDE · ARCS JOIN SYNONYMS', size=7)
    return d


# lac genes in base pairs (E. coli K-12): lacI, then lacZ, lacY, lacA; promoter and operator schematic.
_GENES = [('lacI', 1083), ('gap', 80), ('P', 0), ('O', 0), ('lacZ', 3075), ('lacY', 1254), ('lacA', 612)]


def _dna(d, x0, x1, y):
    d.line((x0, y - 3), (x1, y - 3))
    d.line((x0, y + 3), (x1, y + 3))


def _repressor(d, cx, cy):
    """The repressor as four lobes, a tetramer drawn as geometry."""
    for dx in (-7, 7):
        for dy in (-5, 5):
            d.ellipse(cx + dx, cy + dy, 7.5, 5.5)


def lac_operon():
    d = D()
    # The lac operon in two states, drawn to one scale of base pairs for the genes (promoter and operator
    # widened to be seen). Off: the repressor, made all the time from lacI, sits on the operator and no
    # messenger is made. On: an inducer (allolactose, or a stand-in such as IPTG) binds the repressor,
    # which lets go, and one messenger is copied across lacZ, lacY and lacA.
    s = 0.05
    x = 26
    seg = {}
    for name, bp in _GENES:
        w = bp * s if bp else 16
        seg[name] = (x, x + w)
        x += w
    xe = x
    rows = {'off': 92, 'on': 214}
    bh = 16

    d.group('thin')
    for name in ('lacI', 'P', 'O', 'lacZ', 'lacY', 'lacA'):
        for xx in seg[name]:
            d.line((xx, 40), (xx, 262))
    d.line((seg['lacZ'][0], 276), (seg['lacZ'][0] + 1000 * s, 276))       # scale bar, 1,000 base pairs
    for xx in (seg['lacZ'][0], seg['lacZ'][0] + 1000 * s):
        d.line((xx, 272), (xx, 280))

    d.group()
    for y in rows.values():
        _dna(d, 14, xe + 14, y)
        for name in ('lacI', 'P', 'O', 'lacZ', 'lacY', 'lacA'):
            a, b = seg[name]
            _box(d, a, y - bh / 2, b - a, bh)
    # off: repressor seated on the operator
    ox = (seg['O'][0] + seg['O'][1]) / 2
    _repressor(d, ox, rows['off'] - bh / 2 - 9)
    # on: repressor lifted away, holding inducer
    rx, ry = ox + 4, rows['on'] - 64
    _repressor(d, rx, ry)

    d.group('mid')
    ix = (seg['lacI'][0] + seg['lacI'][1]) / 2
    for y, tx, ty in ((rows['off'], ox - 16, rows['off'] - bh / 2 - 14), (rows['on'], rx - 16, ry)):
        d.curve(f"M{ix:.1f},{y - bh / 2:.1f} Q{ix:.1f},{ty - 18:.1f} {tx:.1f},{ty:.1f}")
        _arrow(d, (ix + 10, ty - 14), (tx, ty), size=4)
    for dx, dy in ((-7, -5), (7, -5), (-7, 5), (7, 5)):                  # inducer diamonds on the lifted repressor
        px, py = rx + dx * 2.1, ry + dy * 2.3
        d.line((px, py - 3), (px + 3, py), (px, py + 3), (px - 3, py), closed=True)
    # the messenger: one wave from the promoter across lacZ, lacY, lacA
    my = rows['on'] - bh / 2 - 12
    xa, xb = seg['P'][0] + 4, seg['lacA'][1]
    n = int((xb - xa) / 3)
    pts = [(xa + (xb - xa) * k / n, my + 2.5 * math.sin(k * math.pi / 2)) for k in range(n + 1)]
    d.line(*pts)
    _arrow(d, pts[-2], (xb + 6, my), size=5)
    # the three proteins under the 'on' strand
    for name, shape in (('lacZ', 4), ('lacY', 3), ('lacA', 2)):
        a, b = seg[name]
        mx = (a + b) / 2
        for k in range(shape):
            d.circle(mx - (shape - 1) * 4 + k * 8, rows['on'] + 24, 3.2)
    # off: a bar across the start of the genes, no messenger
    d.line((seg['P'][0], rows['off'] - bh / 2 - 22), (seg['lacA'][1], rows['off'] - bh / 2 - 22))
    d.line((seg['lacA'][1] - 6, rows['off'] - bh / 2 - 28), (seg['lacA'][1] + 6, rows['off'] - bh / 2 - 16))

    d.group('mid')
    for y in rows.values():
        for name, lab in (('lacI', 'I'), ('P', 'P'), ('O', 'O'), ('lacZ', 'Z'), ('lacY', 'Y'), ('lacA', 'A')):
            a, b = seg[name]
            d.text((a + b) / 2, y + 2.5, lab, size=7)
    d.text(14, 30, 'NO LACTOSE · OFF', size=7, anchor='start')
    d.text(14, 126, 'LACTOSE · ON', size=7, anchor='start')
    d.text(ox + 22, rows['off'] - bh / 2 - 8, 'REPRESSOR ON THE OPERATOR', size=7, anchor='start')
    d.text(seg['lacZ'][0] + 6, rows['off'] - bh / 2 - 26, 'NO MESSENGER', size=7, anchor='start')
    d.text(rx + 26, ry + 2.5, 'INDUCER HOLDS THE REPRESSOR', size=7, anchor='start')
    d.text(seg['lacZ'][0] + 6, my - 7, 'MESSENGER RNA', size=7, anchor='start')
    d.text((seg['lacZ'][0] + seg['lacA'][1]) / 2, rows['on'] + 40, 'β-GALACTOSIDASE · PERMEASE · TRANSACETYLASE', size=7)
    d.text(seg['lacZ'][0] + 1000 * s + 6, 278.5, '1,000 BASE PAIRS', size=7, anchor='start')
    return d


PLATES = {'genetic-code': genetic_code, 'lac-operon': lac_operon}
