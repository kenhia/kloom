"""Plates for part bond2 of the chemistry subject (sprint 025): NMR, computational chemistry, AlphaFold."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _toward(a, b, ra, rb):
    """The segment from a to b, shortened by ra at a and rb at b (a bond between two drawn atoms)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    return [(a[0] + dx / n * ra, a[1] + dy / n * ra), (b[0] - dx / n * rb, b[1] - dy / n * rb)]


def nmr():
    """Ethanol, atoms in circles as in Purcell's 1952 figure, above the proton spectrum it gives:
    a singlet, a quartet and a triplet, whose integral climbs in steps of 1, 2 and 3."""
    d = D()
    base = 236                                   # the spectrum's baseline
    J = 7.5                                      # line spacing of a multiplet, in plate units
    k = 44                                       # height per unit of area
    w = 1.6                                      # half-width of one line
    # centres (shift runs right to left, as on a spectrum), hydrogens, and neighbours that split them
    groups = [('OH', 96, 1, 0), ('CH₂', 196, 2, 3), ('CH₃', 304, 3, 2)]

    def lines(x0, n_h, n_nb):
        coef = [math.comb(n_nb, i) for i in range(n_nb + 1)]
        return [(x0 + (i - n_nb / 2) * J, n_h * c / sum(coef)) for i, c in enumerate(coef)]

    sticks = [l for _, x0, h, nb in groups for l in lines(x0, h, nb)]
    xs = [28 + i * 0.5 for i in range(int((372 - 28) / 0.5) + 1)]

    def spec(x):
        return sum(a * w * w / (w * w + (x - x0) ** 2) for x0, a in sticks)

    def integral(x):
        return sum(a * (0.5 + math.atan((x0 - x) / w) / math.pi) for x0, a in sticks)

    iy0, iu = 158, 9                             # the integral's foot and its rise per hydrogen
    # the molecule: H-O-C-C as a zigzag of 120 degree turns, the atoms drawn as circles
    L = 38
    O = (176, 74)
    Ho = _pt(O, 150, L * 0.8)
    Ca = _pt(O, -30, L)
    Cb = _pt(Ca, 30, L)
    Ha = [_pt(Ca, -90, L * 0.8), _pt(Ca, 90, L * 0.8)]
    Hb = [_pt(Cb, -30, L * 0.8), _pt(Cb, 90, L * 0.8), _pt(Cb, 30, L * 0.8)]
    rC, rH = 9, 7
    d.group('thin')
    d.line((24, base), (376, base))
    for _, x0, h, _ in groups:
        d.line((x0, base + 4), (x0, iy0 + 4))
    d.line((24, iy0), (376, iy0))
    d.line((24, iy0 - 6 * iu), (60, iy0 - 6 * iu))
    d.group()
    for p in (O, Ca, Cb):
        d.circle(*p, rC)
    for p in [Ho] + Ha + Hb:
        d.circle(*p, rH)
    d.lines([_toward(Ho, O, rH, rC), _toward(O, Ca, rC, rC), _toward(Ca, Cb, rC, rC)]
            + [_toward(Ca, h, rC, rH) for h in Ha] + [_toward(Cb, h, rC, rH) for h in Hb])
    d.line(*[(x, base - k * spec(x)) for x in xs])
    d.group('mid')
    d.line(*[(x, iy0 - iu * integral(x)) for x in reversed(xs)])
    d.group('mid')
    for p, s in ((O, 'O'), (Ca, 'C'), (Cb, 'C')):
        d.text(p[0], p[1] + 3, s, size=8)
    for p in [Ho] + Ha + Hb:
        d.text(p[0], p[1] + 2.5, 'H', size=6)
    for name, x0, h, nb in groups:
        d.text(x0, base + 15, name, size=8)
    done = 0
    for name, x0, h, nb in reversed(groups):
        done += h
        d.text(x0 - 26, iy0 - iu * done - 4, str(h), size=8)
    d.text(200, 276, '← CHEMICAL SHIFT, δ', size=8)
    d.text(330, 40, 'CH₃CH₂OH', size=9)
    return d


def computational_chemistry():
    """Kohn's exponential wall: log10 of the numbers a wavefunction of N electrons needs, p to the 3N,
    for p = 3 and p = 10, against the density's fixed 10 cubed; with his 10 to the 9, and 3 to the 300 for a hundred electrons."""
    d = D()
    x0, x1, y0, y1 = 62, 360, 248, 40              # plot box: N from 0 to 100, log10 from 0 to 160
    X = lambda n: x0 + (x1 - x0) * n / 100
    Y = lambda e: y0 - (y0 - y1) * e / 160
    d.group('thin')
    for n in range(0, 101, 25):
        d.line((X(n), y0), (X(n), y1))
    for e in range(0, 151, 50):
        d.line((x0, Y(e)), (x1, Y(e)))
    d.line((x0, Y(9)), (X(100), Y(9)))           # Kohn's feasible machine, 10 to the 9 numbers
    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))
    l3 = math.log10(3)
    d.line((X(0), Y(0)), (X(100), Y(300 * l3)))  # p = 3
    d.line((X(0), Y(3)), (X(100), Y(3)))          # the density on a 10-point grid: 10 cubed, whatever N
    d.group('mid')
    d.line((X(0), Y(0)), (X(160 / 3), Y(160)))   # p = 10
    n6 = 9 / (3 * l3)
    d.circle(X(n6), Y(9), 3)
    d.circle(X(100), Y(300 * l3), 3)
    d.group('mid')
    for n in (0, 50, 100):
        d.text(X(n), y0 + 13, str(n), size=8)
    for e, s in ((0, '10⁰'), (50, '10⁵⁰'), (100, '10¹⁰⁰'), (150, '10¹⁵⁰')):
        d.text(x0 - 6, Y(e) + 3, s, size=8, anchor='end')
    d.text(200, y0 + 27, 'ELECTRONS, N', size=8)
    d.text(X(56), Y(160) + 10, 'p = 10', size=8, anchor='start')
    d.text(X(72), Y(300 * l3 * 0.72) + 18, 'p = 3', size=8, anchor='start')
    d.text(X(70), Y(3) - 6, 'DENSITY, 10³', size=8)
    d.text(X(n6) + 8, Y(9) - 6, '10⁹ → N ≈ 6', size=8, anchor='start')
    d.text(X(100) - 4, Y(300 * l3) - 20, '3³⁰⁰ ≈ 10¹⁴³', size=8, anchor='end')
    return d


def alphafold():
    """Levinthal's tree of three choices per residue; a helical hairpin drawn as its alpha-carbon trace;
    and the hairpin's contact map, the table of pairs that AlphaFold 2's Evoformer works on."""
    d = D()
    # the tree: four residues, three choices each, 81 leaves; one path drawn at full weight
    tx, ty, dy = 22, 150, 30
    levels = [[(tx, ty)]]
    for lv in range(1, 5):
        n = 3 ** lv
        span = 210
        levels.append([(tx + 28 * lv, ty - span / 2 + span * (i + 0.5) / n) for i in range(n)])
    segs, path = [], [0]
    for lv in range(1, 5):
        for i, q in enumerate(levels[lv]):
            segs.append([levels[lv - 1][i // 3], q])
    for lv in range(1, 5):
        path.append(path[-1] * 3 + (1, 0, 2, 1)[lv - 1])
    # the hairpin: helix A up, a turn, helix B down, 3.6 residues a turn, rise 1.5 A, radius 2.3 A
    s = 5.6                                          # plate units per angstrom
    ca = []
    for i in range(12):
        th = math.radians(100 * i)
        ca.append((2.3 * math.cos(th), 1.5 * i, 2.3 * math.sin(th)))
    top = ca[-1]
    ca.append((top[0] + 3.2, top[1] + 2.0, 0))
    ca.append((top[0] + 6.6, top[1] + 1.2, 0))
    for i in range(12):
        th = math.radians(100 * i + 40)
        ca.append((9.6 + 2.3 * math.cos(th), top[1] - 1.5 * i, 2.3 * math.sin(th)))
    hx, hy = 176, 238
    P = [(hx + s * x + 1.2 * z, hy - s * y - 0.6 * z) for x, y, z in ca]
    n = len(ca)
    cx0, cy0, c = 282, 96, 3.6                       # the contact map, n by n cells
    contacts = [(i, j) for i in range(n) for j in range(n)
                if abs(i - j) > 2 and math.dist(ca[i], ca[j]) < 8.0]
    d.group('thin')
    d.lines(segs)
    d.line((hx, hy + 8), (hx, hy - s * 18.5))                       # helix A's axis
    d.line((hx + s * 9.6, hy + 8 - s * 0), (hx + s * 9.6, hy - s * 18.5))  # helix B's axis
    d.line((cx0, cy0), (cx0 + n * c, cy0), (cx0 + n * c, cy0 + n * c), (cx0, cy0 + n * c), closed=True)
    d.line((cx0, cy0), (cx0 + n * c, cy0 + n * c))
    d.group()
    d.line(*[levels[lv][path[lv]] for lv in range(5)])
    d.line(*P)
    d.group('mid')
    for p in P:
        d.circle(*p, 1.8)
    for i, j in contacts:
        x, y = cx0 + j * c, cy0 + i * c
        d.line((x + 0.6, y + 0.6), (x + c - 0.6, y + c - 0.6))
        d.line((x + c - 0.6, y + 0.6), (x + 0.6, y + c - 0.6))
    d.group('mid')
    d.text(tx + 56, 262, '3 × 3 × 3 × 3 = 81', size=8)
    d.text(tx + 56, 276, '3¹⁰⁰ ≈ 5 × 10⁴⁷', size=8)
    d.text(hx + s * 4.8, 262, 'Cα TRACE', size=8)
    d.text(cx0 + n * c / 2, cy0 - 10, 'PAIRS i, j', size=8)
    d.text(cx0 + n * c / 2, cy0 + n * c + 16, 'CONTACTS < 8 Å', size=8)
    return d


PLATES = {'nmr': nmr, 'computational-chemistry': computational_chemistry, 'alphafold': alphafold}
