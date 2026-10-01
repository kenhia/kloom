"""Plates for In the Blood's What we learned, second half (sprint 028): Hales, hemoglobin's spectrum,
sickle cell electrophoresis and Perutz's heavy atoms. See plates_for.py."""
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


def hales():
    d = D()
    # Hales's two tubes in elevation against one height scale: the crural artery's column (8 ft 3 in
    # of blood above the heart, Experiment I) and the jugular vein's (about a foot, Experiment III).
    # The right-hand scale converts to mm of mercury by our arithmetic (blood 1.05, mercury 13.6).
    base, ft = 256, 25.0                    # the level of the left ventricle, and pixels per foot
    top = base - 9 * ft
    mm_per_ft = 304.8 * 1.05 / 13.6         # about 23.5 mm of mercury per foot of blood
    ax, vx = 150, 262                       # the artery's tube and the vein's
    d.group('thin')
    d.line((40, base), (360, base))         # heart level
    d.line((62, top), (62, base))
    for k in range(10):
        d.line((58, base - k * ft), (62, base - k * ft))
    d.line((338, top), (338, base))
    for mm in range(0, 201, 50):
        y = base - mm / mm_per_ft * ft
        d.line((338, y), (342, y))
    hy = base - 8.25 * ft                   # the arterial column's height, carried across
    for x0 in range(64, 336, 8):
        d.line((x0, hy), (x0 + 4, hy))
    vy = base - 1.0 * ft
    for x0 in range(vx + 8, 336, 8):
        d.line((x0, vy), (x0 + 4, vy))
    d.group()
    # the artery and vein in section below heart level, each with its brass pipe and glass tube
    for x, y, w in ((ax, 282, 9), (vx, 282, 7)):
        d.line((x - 44, y - w), (x - 6, y - w))
        d.line((x + 6, y - w), (x + 44, y - w))
        d.line((x - 44, y + w), (x + 44, y + w))
    d.line((ax - 4, 273), (ax - 4, top))
    d.line((ax + 4, 273), (ax + 4, top))
    d.line((vx - 3, 275), (vx - 3, base - (4 + 2 / 12) * ft))
    d.line((vx + 3, 275), (vx + 3, base - (4 + 2 / 12) * ft))
    d.group('mid')
    # the brass pipes, and the blood in each tube, hatched
    d.line((ax - 6, 273), (ax - 6, 262), (ax + 6, 262), (ax + 6, 273))
    d.line((vx - 5, 275), (vx - 5, 266), (vx + 5, 266), (vx + 5, 275))
    y = 270
    while y > hy:
        d.line((ax - 4, y), (ax + 4, y - 3))
        y -= 6
    y = 272
    while y > vy:
        d.line((vx - 3, y), (vx + 3, y - 3))
        y -= 6
    # the beat: the column rising and falling two to four inches
    for s in (-1, 1):
        p = (ax + 16, hy + s * 3)
        q = (ax + 16, hy + s * 9)
        d.line(p, q)
        _arrow(d, p, q, size=3)
    d.group('mid')
    for k in (0, 3, 6, 9):
        d.text(54, base - k * ft + 3, str(k), size=7, anchor='end')
    d.text(62, top - 8, 'FT', size=7)
    for mm in (0, 100, 200):
        d.text(346, base - mm / mm_per_ft * ft + 3, str(mm), size=7, anchor='start')
    d.text(338, top - 8, 'MMHG', size=7)
    d.text(ax + 26, hy - 5, '8 FT 3 IN', size=7, anchor='start')
    d.text(vx + 10, vy - 5, 'ABOUT 1 FT', size=7, anchor='start')
    d.text(ax, 298, 'ARTERY', size=7)
    d.text(vx, 298, 'VEIN', size=7)
    d.text(200, base - 5, 'HEART LEVEL', size=7)
    return d


def hemoglobin():
    d = D()
    # Stokes's test tube (1864, section 5): reduced blood left standing, oxidised by the air at the top
    # only, set behind a slit and viewed through a prism. The spectrum, right, is drawn row by row
    # against Fraunhofer's lines, the band positions taken from his woodcut (D to F only): two bands
    # above, one below, the "tuning-fork".
    tx, t0, t1 = 70, 70, 232                # the tube: centre, liquid surface, bottom of the straight wall
    split = 128                              # where the oxygenated layer gives way to the reduced
    sx = 118                                 # the slit
    px = 170                                 # the prism's centre
    X = lambda c: 240 + (c - 250) * 0.2333   # woodcut position to plate x
    lines = {'D': X(315), 'E': X(545), 'b': X(615), 'F': X(785)}
    y0, y1 = 70, 232
    d.group('thin')
    for x in lines.values():
        d.line((x, y0 - 6), (x, y1))
    d.line((236, y0), (382, y0))
    d.line((236, y1), (382, y1))
    d.line((tx + 22, split), (382, split))   # the layer boundary carried across to the spectrum
    for y in (112, 188):                      # light through the tube, the slit and the prism
        d.line((20, y), (sx, 150), (px - 12, 150))
    d.line((px + 12, 150), (236, 132))
    d.line((px + 12, 150), (236, 168))
    d.group()
    # the tube with its rounded foot
    d.line((tx - 14, 50), (tx - 14, t1))
    d.arc(tx, t1, 14, 180, 0, n=20)
    d.line((tx + 14, t1), (tx + 14, 50))
    d.line((tx - 14, t0), (tx + 14, t0))
    # the slit: two jaws
    d.line((sx, 60), (sx, 146))
    d.line((sx, 154), (sx, 240))
    # the prism, an equilateral triangle
    r = 22
    d.line(*[_pt(px, 154, r, a) for a in (-90, 30, 150)], closed=True)
    # the spectrum's frame
    d.line((236, y0), (236, y1))
    d.line((382, y0), (382, y1))
    d.group('mid')
    # the blood in the tube: sparse hatching where it is scarlet, dense where it is purple
    for y in range(t0 + 6, split, 9):
        d.line((tx - 12, y), (tx + 12, y))
    for y in range(split + 4, t1 + 10, 4):
        w = 12 if y <= t1 else math.sqrt(max(0, 14 ** 2 - (y - t1) ** 2)) - 2
        d.line((tx - w, y), (tx + w, y))
    # the bands: two narrow ones above the boundary, one broad one below
    def band(xa, xb, ya, yb):
        x = xa
        while x <= xb:
            d.line((x, ya), (x, yb))
            x += 2.2
    band(X(320), X(400), y0, split)
    band(X(445), X(548), y0, split)
    band(X(345), X(455), split + 8, y1)
    d.group('mid')
    for k, x in lines.items():
        d.text(x, y0 - 10, k, size=7)
    d.text(tx, 42, 'AIR', size=7)
    d.text(tx - 18, 92, 'SCARLET', size=7, anchor='end')
    d.text(tx - 18, 222, 'PURPLE', size=7, anchor='end')
    d.text(sx, 252, 'SLIT', size=7)
    d.text(px, 192, 'PRISM', size=7)
    d.text(309, 250, 'TWO BANDS, THEN ONE', size=7)
    return d


def sickle_cell():
    d = D()
    # Left: a moving-boundary cell in outline, a U of glass with an electrode above each limb. Right:
    # four scans after 20 hours at pH 6.9 drawn after Pauling, Itano, Singer and Wells's Fig. 3: the
    # normal protein, a negative ion, moves towards +; the sickle protein, a positive ion, towards -.
    # Peak heights and shifts are a sketch, not their data; the trait's sickle share is 40 per cent.
    lx, rx, ytop, ybot = 52, 102, 70, 210
    d.group('thin')
    d.line((lx, ytop - 18), (lx, ybot + 30))
    d.line((rx, ytop - 18), (rx, ybot + 30))
    x0, x1, start = 150, 385, 290           # the scans' baseline, and the starting boundary
    d.line((start, 54), (start, 270))
    d.group()
    # the U-tube: two limbs and the bend
    for x in (lx, rx):
        d.line((x - 9, ytop), (x - 9, ybot))
        d.line((x + 9, ytop), (x + 9, ybot))
    c = ((lx + rx) / 2, ybot)
    d.arc(c[0], c[1], (rx - lx) / 2 + 9, 180, 0, n=24, ry=34)
    d.arc(c[0], c[1], (rx - lx) / 2 - 9, 180, 0, n=24, ry=18)
    # the electrodes
    for x in (lx, rx):
        d.line((x, ytop - 2), (x, ytop - 22))
        d.line((x - 6, ytop - 22), (x + 6, ytop - 22))
    # the four scans: a baseline and gaussian peaks for each
    def g(x, mu, h, s=9):
        return h * math.exp(-((x - mu) ** 2) / (2 * s * s))
    shift = 34
    traces = [
        ('NORMAL', [(start + shift, 34)]),
        ('SICKLE CELL ANEMIA', [(start - shift * 0.4, 34)]),
        ('SICKLE CELL TRAIT', [(start + shift, 21), (start - shift * 0.4, 14)]),
        ('50-50 MIXTURE', [(start + shift, 17.5), (start - shift * 0.4, 17.5)]),
    ]
    baselines = [100, 152, 204, 256]
    for (name, peaks), yb in zip(traces, baselines):
        pts = []
        x = x0
        while x <= x1:
            pts.append((x, yb - sum(g(x, mu, h) for mu, h in peaks)))
            x += 2
        d.line(*pts)
    d.group('mid')
    # the boundaries in the limbs, displaced up one side and down the other, and the direction of travel
    d.line((lx - 9, 120), (lx + 9, 120))
    d.line((rx - 9, 150), (rx + 9, 150))
    for yb in baselines:
        _arrow(d, (start, yb + 12), (start, yb + 4), size=3)
    p, q = (start + 14, 46), (start + 54, 46)
    d.line(p, q)
    _arrow(d, p, q, size=4)
    p, q = (start - 14, 46), (start - 54, 46)
    d.line(p, q)
    _arrow(d, p, q, size=4)
    d.group('mid')
    d.text(lx, ytop - 28, '-', size=9)
    d.text(rx, ytop - 28, '+', size=9)
    d.text(start + 60, 49, 'TO +', size=7, anchor='start')
    d.text(start - 60, 49, 'TO -', size=7, anchor='end')
    for (name, peaks), yb in zip(traces, baselines):
        d.text(x0, yb - 30, name, size=7, anchor='start')
    d.text(77, 272, 'PH 6.9', size=7)
    return d


def perutz_hemoglobin():
    d = D()
    # Harker's construction for one reflection, in the complex plane. The protein's wave has a known
    # strength |FP| but unknown phase: a circle. Each heavy-atom crystal gives |FPH| and, once the metal
    # is placed, the vector FH, so FP must lie on a circle of radius |FPH| about the tip of -FH. One
    # derivative leaves two crossings; a second picks one. Lengths and the phase are invented.
    o = (190, 152)
    s = 1.0
    fp, phi = 78, -35                         # |FP| and the true phase, in degrees (SVG's y down)
    fh1 = (30, 200)                           # |FH1| and its phase
    fh2 = (26, 95)

    def vec(r, a):
        return r * math.cos(math.radians(a)), r * math.sin(math.radians(a))

    P = vec(fp, phi)

    def deriv(fh):
        H = vec(*fh)
        PH = (P[0] + H[0], P[1] + H[1])
        return (o[0] - H[0], o[1] - H[1]), math.hypot(*PH)

    c1, r1 = deriv(fh1)
    c2, r2 = deriv(fh2)

    def crossings(c, r):
        # where the circle about c of radius r meets the protein circle about o
        dx, dy = c[0] - o[0], c[1] - o[1]
        dd = math.hypot(dx, dy)
        a = (fp * fp - r * r + dd * dd) / (2 * dd)
        h = math.sqrt(max(0, fp * fp - a * a))
        mx, my = o[0] + a * dx / dd, o[1] + a * dy / dd
        return [(mx + h * dy / dd, my - h * dx / dd), (mx - h * dy / dd, my + h * dx / dd)]

    d.group('thin')
    d.line((o[0] - 150, o[1]), (o[0] + 160, o[1]))
    d.line((o[0], o[1] - 135), (o[0], o[1] + 135))
    d.circle(o[0], o[1], fp)
    d.group()
    d.circle(c1[0], c1[1], r1)
    d.circle(c2[0], c2[1], r2)
    d.group('mid')
    # the heavy-atom vectors, reversed, from the origin to each circle's centre
    for c in (c1, c2):
        d.line(o, c)
        _arrow(d, o, c, size=4)
    # the protein vector to the crossing all three circles share
    tip = (o[0] + P[0], o[1] + P[1])
    d.line(o, tip)
    _arrow(d, o, tip, size=6)
    for c, r in ((c1, r1), (c2, r2)):
        for q in crossings(c, r):
            d.circle(q[0], q[1], 3)
    d.arc(o[0], o[1], 26, phi, 0, n=12)
    d.group('mid')
    d.text(tip[0] + 8, tip[1] - 4, 'FP', size=7, anchor='start')
    d.text(c1[0] - 6, c1[1] + 14, '-FH1', size=7, anchor='end')
    d.text(c2[0] + 6, c2[1] + 12, '-FH2', size=7, anchor='start')
    d.text(o[0] + 30, o[1] - 6, 'PHASE', size=7, anchor='start')
    d.text(o[0] - fp - 4, o[1] - 6, '|FP|', size=7, anchor='end')
    d.text(c1[0] - r1 * 0.72, c1[1] - r1 * 0.72, '|FPH1|', size=7, anchor='end')
    d.text(c2[0] + r2 * 0.74, c2[1] + r2 * 0.72 + 14, '|FPH2|', size=7, anchor='start')
    return d


PLATES = {
    'hales': hales,
    'hemoglobin': hemoglobin,
    'sickle-cell': sickle_cell,
    'perutz-hemoglobin': perutz_hemoglobin,
}
