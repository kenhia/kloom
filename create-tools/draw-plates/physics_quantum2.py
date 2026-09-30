"""physics plates, the end of the trail "The quantum revolution" and the frame on entanglement (sprint 021). See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def matrix_mechanics():
    """Heisenberg's tables as Born read them: hydrogen's levels, with the jumps
    between them, and the product of two arrays, row into column.

    The ladder is drawn to scale (E ∝ −1/n²). Each entry X(n, m) of a table
    belongs to one jump, n to m; the product's entry (3, 2) sums X(3, k) P(k, 2)
    over every intermediate state k, so the jumps chain 3 → k → 2."""
    d = D()
    # the ladder: E_n = -1/n², from n = 1 at the foot to the ionisation limit at the top
    top, foot = 50, 262
    def ly(n):
        return foot - (foot - top) * (1 - 1 / n ** 2)
    x0, x1 = 26, 108
    cell = 20
    Px, Py = 250, 52           # P, top right
    Xx, Xy = 140, 172          # X, bottom left
    Cx, Cy = 250, 172          # the product, bottom right
    r, c = 3, 2                # the entry drawn: row 3, column 2
    # construction: the ionisation limit, the grid lines of the three tables, and the row and column carried across
    d.group('thin')
    d.line((x0, top), (x1, top))
    for gx, gy in ((Px, Py), (Xx, Xy), (Cx, Cy)):
        d.lines([[(gx + i * cell, gy), (gx + i * cell, gy + 4 * cell)] for i in range(1, 4)] +
                [[(gx, gy + i * cell), (gx + 4 * cell, gy + i * cell)] for i in range(1, 4)])
    ry = Xy + (r - 0.5) * cell
    cx = Px + (c - 0.5) * cell
    d.line((Xx + 4 * cell, ry), (Cx + (c - 1) * cell, ry))
    d.line((cx, Py + 4 * cell), (cx, Cy + (r - 1) * cell))
    # the object: the levels, and the three tables' frames
    d.group()
    for n in range(1, 5):
        d.line((x0, ly(n)), (x1, ly(n)))
    for gx, gy in ((Px, Py), (Xx, Xy), (Cx, Cy)):
        d.line((gx, gy), (gx + 4 * cell, gy), (gx + 4 * cell, gy + 4 * cell), (gx, gy + 4 * cell), closed=True)
    # the jumps on the ladder, each an entry in a table
    d.group('mid')
    for (a, b, x) in ((3, 2, 44), (2, 1, 62), (3, 1, 80), (4, 2, 98)):
        d.line((x, ly(a)), (x, ly(b) - 3))
        _arrow(d, x, ly(b), math.pi / 2, 3.5)
    # the diagonal of each table left empty (no jump), and the row, column and entry of the product
    for gx, gy in ((Px, Py), (Xx, Xy), (Cx, Cy)):
        d.lines([[(gx + i * cell + 7, gy + i * cell + 10), (gx + i * cell + 13, gy + i * cell + 10)] for i in range(4)])
    d.line((Xx + 2, Xy + (r - 1) * cell + 2), (Xx + 4 * cell - 2, Xy + (r - 1) * cell + 2),
           (Xx + 4 * cell - 2, Xy + r * cell - 2), (Xx + 2, Xy + r * cell - 2), closed=True)
    d.line((Px + (c - 1) * cell + 2, Py + 2), (Px + c * cell - 2, Py + 2),
           (Px + c * cell - 2, Py + 4 * cell - 2), (Px + (c - 1) * cell + 2, Py + 4 * cell - 2), closed=True)
    ex, ey = Cx + (c - 0.5) * cell, Cy + (r - 0.5) * cell
    d.circle(ex, ey, 6)
    for k in range(4):
        d.circle(Xx + (k + 0.5) * cell, ry, 2)
        d.circle(cx, Py + (k + 0.5) * cell, 2)
    # labels
    d.group()
    for n in range(1, 5):
        d.text(x1 + 6, ly(n) + 3, f'n={n}', size=7, anchor='start')
    d.text(x0, top - 6, 'IONISED', size=7, anchor='start')
    d.text(Px + 2 * cell, Py - 8, 'P', size=10)
    d.text(Xx - 10, Xy + 2 * cell + 4, 'X', size=10, anchor='end')
    d.text(Cx + 2 * cell, Cy + 4 * cell + 16, 'XP', size=10)
    d.text(Xx + 2 * cell, Xy + 4 * cell + 16, 'ROW 3', size=7)
    d.text(Px - 8, Py + 2 * cell + 3, 'COL 2', size=7, anchor='end')
    d.text(200, 292, 'PQ − QP = h/2πi', size=9)
    d.text(Xx + 2 * cell, 60, 'Σ X(3,k) P(k,2)', size=8)
    return d


def wave_mechanics():
    """Hydrogen as Schrödinger solved it. Left, to scale: the Coulomb well
    V = −1/r and the levels E_n = −1/(2n²) in atomic units. Right: the radial
    wave u(r) = r·R(r) of each level's s state, drawn on its own line to one
    scale in r, with its n − 1 nodes marked: the whole numbers are the
    numbers of nodes."""
    d = D()
    # the well, left
    X0, sx = 34, 9.0           # r = 0 at X0; plate units per Bohr radius
    Y0, sy = 60, 400           # E = 0 at Y0; plate units per hartree
    rw = 12
    def P(r, E):
        return (X0 + sx * r, Y0 - sy * E)
    levels = {1: -0.5, 2: -0.125, 3: -1 / 18}
    waves = {
        1: (lambda r: r * math.exp(-r), []),
        2: (lambda r: r * (1 - r / 2) * math.exp(-r / 2), [2]),
        3: (lambda r: r * (1 - 2 * r / 3 + 2 * r * r / 27) * math.exp(-r / 3), [(9 - 3 * math.sqrt(3)) / 2, (9 + 3 * math.sqrt(3)) / 2]),
    }
    # the waves, right: r from 0 to 24 Bohr radii
    WX0, wsx = 176, 8.4
    base = {3: 88, 2: 162, 1: 238}
    amp = 26
    # construction: the well's axes, E = 0, the waves' baselines, and lines from each level to its wave
    d.group('thin')
    d.line(P(0, 0.03), P(0, -0.6))
    d.line(P(0, 0), P(rw, 0))
    for n, E in levels.items():
        d.line(P(2 * n * n if 2 * n * n < rw else rw, E), (WX0 - 6, base[n]))
        d.line((WX0, base[n]), (WX0 + wsx * 24, base[n]))
    # the object: the well, and the levels inside it
    d.group()
    d.line(*[P(r, -1 / r) for r in [1.7 + 0.1 * i for i in range(int((rw - 1.7) / 0.1) + 1)]])
    d.group('mid')
    for n, E in levels.items():
        d.line(P(0, E), P(min(2 * n * n, rw), E))
    # the waves
    d.group()
    for n, (f, nodes) in waves.items():
        rs = [24 * i / 300 for i in range(301)]
        peak = max(abs(f(r)) for r in rs)
        d.line(*[(WX0 + wsx * r, base[n] - amp * f(r) / peak) for r in rs])
    d.group('mid')
    for n, (f, nodes) in waves.items():
        for r in nodes:
            d.circle(WX0 + wsx * r, base[n], 2.5)
    # labels
    d.group()
    for n in levels:
        d.text(WX0 + wsx * 24, base[n] + 14, f'n={n}  {n - 1} NODE' + ('' if n == 2 else 'S'), size=7, anchor='end')
    d.text(X0 + 4, Y0 - 8, 'E = 0', size=7, anchor='start')
    d.text(X0 + 36, 284, 'V = −e²/4πε₀r', size=7, anchor='start')
    d.text(WX0 + wsx * 24, 292, 'Eₙ = −13.6 eV / n²', size=8, anchor='end')
    d.text(WX0, 40, 'u(r) = r·R(r)', size=7, anchor='start')
    return d


def uncertainty():
    """Heisenberg's gamma-ray microscope, and Kennard's form of what it shows.

    A photon from the left strikes the electron at the focus; to be seen it
    must scatter into the lens, somewhere inside the cone of half-angle ε, so
    the electron's recoil is uncertain within the mirrored cone. Beside it, a
    Gaussian packet narrow in x and its transform, wide in p, drawn with equal
    areas (height ∝ 1/σ) and σx·σp fixed."""
    d = D()
    ex, ey = 128, 214           # the electron, at the focus
    ly, rx, ryl = 96, 62, 9     # the lens
    eps = math.atan2(rx, ey - ly)
    # construction: the axis, the cone the lens accepts, and its mirror below the electron
    d.group('thin')
    d.line((ex, 22), (ex, 286))
    d.line((ex - rx, ly), (ex, ey), (ex + rx, ly))
    m = 58
    d.line((ex - m * math.tan(eps), ey + m), (ex, ey), (ex + m * math.tan(eps), ey + m))
    # the object: the lens and the microscope tube
    d.group()
    d.ellipse(ex, ly, rx, ryl)
    d.line((ex - 22, ly - ryl + 1), (ex - 22, 30), (ex + 22, 30), (ex + 22, ly - ryl + 1))
    d.line((ex - 14, 30), (ex - 14, 22), (ex + 14, 22), (ex + 14, 30))
    # the photons and the recoil
    d.group('mid')
    x_in, x_hit = 16, ex - 8
    d.line(*[(x, ey + 4 * math.sin((x - x_in) * 2 * math.pi / 9)) for x in [x_in + 0.5 * i for i in range(int((x_hit - x_in) / 0.5) + 1)]])
    _arrow(d, x_hit, ey, 0, 4)
    sa = eps * 0.55              # the scattered photon, somewhere inside the cone
    qx, qy = ex + (ey - ly - 6) * math.tan(sa), ly + 6
    d.line((ex, ey), (qx, qy))
    _arrow(d, qx, qy, math.atan2(qy - ey, qx - ex), 4)
    kx, ky = ex - 30 * math.tan(sa), ey + 30
    d.line((ex, ey), (kx, ky))
    _arrow(d, kx, ky, math.atan2(ky - ey, kx - ex), 4)
    d.circle(ex, ey, 3)
    # the two Gaussians, x above and p below
    d.group('thin')
    gx0, gx1, cxg = 236, 384, 310
    for base in (138, 262):
        d.line((gx0, base), (gx1, base))
    for s, base in ((7, 138), (26, 262)):
        d.lines([[(cxg - s, base + 4), (cxg - s, base - 6)], [(cxg + s, base + 4), (cxg + s, base - 6)]])
    d.group()
    area = 7 * 72
    for s, base in ((7, 138), (26, 262)):
        h = area / s
        xs = [gx0 + (gx1 - gx0) * i / 200 for i in range(201)]
        d.line(*[(x, base - h * math.exp(-((x - cxg) / s) ** 2 / 2)) for x in xs])
    # labels
    d.group()
    d.text(ex + 11, ey - 26, 'ε', size=9)
    d.text(x_in, ey - 10, 'γ', size=9, anchor='start')
    d.text(ex + 8, ey + 12, 'e', size=8, anchor='start')
    d.text(ex - 32, ey + 50, 'RECOIL', size=7, anchor='end')
    d.text(gx1, 152, 'x  Δx', size=7, anchor='end')
    d.text(gx1, 276, 'p  Δp', size=7, anchor='end')
    d.text(cxg, 292, 'Δx Δp ≥ ħ/2', size=8)
    return d


def entanglement():
    """A Bell test and what it measures.

    Above: a source sends two photons to polarisers set at angles a and b,
    each followed by a two-way detector (+1 or −1). Below: the correlation
    E between the two sides against the angle θ between the polarisers, for
    quantum mechanics (cos 2θ) and for the best local model (a straight line
    from +1 to −1). They agree at 0°, 45° and 90°; the gap is widest at 22.5°
    and 67.5°, the angles a CHSH test uses."""
    d = D()
    sy_ = 64
    src = (200, sy_)
    pa, pb = (96, sy_), (304, sy_)
    da, db = (40, sy_), (360, sy_)
    gx0, gx1 = 70, 350           # θ from 0 to 90 degrees
    gy_mid, gyh = 202, 66        # E = 0 at gy_mid; E = ±1 at ±gyh
    def G(th, E):
        return (gx0 + (gx1 - gx0) * th / 90, gy_mid - gyh * E)
    # construction: the beam line, the graph's axes and the CHSH angles
    d.group('thin')
    d.line((da[0] + 12, sy_), (db[0] - 12, sy_))
    d.line(G(0, 1.15), G(0, -1.15))
    d.line(G(0, 0), G(90, 0))
    d.lines([[G(0, e), G(90, e)] for e in (1, -1)])
    d.lines([[G(t, 1.1), G(t, -1.1)] for t in (22.5, 45, 67.5)])
    # the apparatus: the source, two polarisers and two detectors
    d.group()
    d.circle(*src, 7)
    for (px, py), ang in ((pa, 60), (pb, 105)):
        d.circle(px, py, 13)
        a = math.radians(ang)
        d.line((px - 11 * math.cos(a), py - 11 * math.sin(a)), (px + 11 * math.cos(a), py + 11 * math.sin(a)))
    for (qx, qy) in (da, db):
        d.line((qx - 11, qy - 11), (qx + 11, qy - 11), (qx + 11, qy + 11), (qx - 11, qy + 11), closed=True)
    # the photons leaving the source, and the two outputs of each detector
    d.group('mid')
    for sgn in (-1, 1):
        x0 = src[0] + sgn * 12
        x1 = (pa if sgn < 0 else pb)[0] - sgn * 18
        d.line(*[(x, sy_ + 3 * math.sin((x - x0) * 2 * math.pi / 10)) for x in [min(x0, x1) + 0.5 * i for i in range(int(abs(x1 - x0) / 0.5) + 1)]])
        _arrow(d, x1, sy_, 0 if sgn > 0 else math.pi, 4)
    for (qx, qy), sgn in ((da, -1), (db, 1)):
        d.lines([[(qx, qy - 11), (qx, qy - 24)], [(qx, qy + 11), (qx, qy + 24)]])
    # the two curves
    d.group()
    d.line(*[G(t, math.cos(math.radians(2 * t))) for t in [90 * i / 180 for i in range(181)]])
    d.group('mid')
    d.line(G(0, 1), G(90, -1))
    for t in (22.5, 67.5):
        d.circle(*G(t, math.cos(math.radians(2 * t))), 2.5)
        d.circle(*G(t, 1 - t / 45), 2.5)
    # labels
    d.group()
    d.text(pa[0], sy_ + 28, 'a', size=8)
    d.text(pb[0], sy_ + 28, 'b', size=8)
    d.text(da[0], sy_ - 28, '+1', size=7)
    d.text(db[0], sy_ - 28, '+1', size=7)
    d.text(da[0], sy_ + 34, '−1', size=7)
    d.text(db[0], sy_ + 34, '−1', size=7)
    d.text(src[0], sy_ - 14, 'SOURCE', size=7)
    d.text(gx0 - 6, gy_mid - gyh + 3, '+1', size=7, anchor='end')
    d.text(gx0 - 6, gy_mid + gyh + 3, '−1', size=7, anchor='end')
    d.text(gx0 - 6, gy_mid + 3, 'E', size=8, anchor='end')
    for t in (0, 22.5, 45, 67.5, 90):
        d.text(G(t, 0)[0], gy_mid + gyh + 16, f'{t:g}°', size=7)
    d.text(G(50, 0.9)[0], G(50, 0.9)[1], 'cos 2θ', size=7, anchor='start')
    d.text(G(33, -0.55)[0], G(33, -0.55)[1], 'LOCAL', size=7, anchor='end')
    d.text(200, 296, 'θ = b − a', size=8)
    return d


PLATES = {
    'matrix-mechanics': matrix_mechanics,
    'wave-mechanics': wave_mechanics,
    'uncertainty': uncertainty,
    'entanglement': entanglement,
}
