"""Plates for the chemistry subject's part elements1 (sprint 025): radium, noble-gases, moseley."""
import math
from plates import D


def radium():
    """The Curies' plate condenser and quartz balance in section, and the triangle of fractional crystallisation."""
    d = D()
    # --- the condenser: plate B (charged, with the powder) below plate A (to the electrometer)
    bx, by, bw = 40, 150, 120          # plate B's left end, height, width
    ay = 118                            # plate A's height
    ex, ey, er = 92, 50, 20             # the electrometer's case
    qx = 176                            # the quartz lamina's line
    d.group('thin')
    d.line((bx + bw / 2, ey + er + 4), (bx + bw / 2, 214))      # the condenser's axis
    d.line((20, 214), (200, 214))                                 # the bench
    d.line((bx - 8, ay), (bx + bw + 8, ay))                       # guard-ring line
    d.line((qx, 60), (qx, 214))
    d.group()
    d.line((bx, by), (bx + bw, by))
    d.line((bx, by + 4), (bx + bw, by + 4))
    d.line((bx + 20, ay), (bx + bw - 20, ay))                     # plate A
    d.line((bx - 6, ay), (bx + 14, ay))                           # the guard ring, cut
    d.line((bx + bw - 14, ay), (bx + bw + 6, ay))
    d.circle(ex, ey, er)                                          # the electrometer
    d.line((bx + bw / 2, ay), (bx + bw / 2, ay - 16), (ex + 16, ay - 16), (ex, ey + er))
    # the battery under plate B: cells of long and short plates
    for k in range(4):
        x = bx + 24 + k * 22
        d.line((x, 186), (x, 204))
        d.line((x + 8, 190), (x + 8, 200))
    d.line((bx + bw / 2, by + 4), (bx + bw / 2, 176), (bx + 24, 176), (bx + 24, 186))
    # the quartz balance: a lamina hung from a hook, its pan of weights below
    d.line((qx - 4, 72), (qx + 4, 72), (qx + 4, 150), (qx - 4, 150), closed=True)
    d.line((qx, 150), (qx, 168))
    d.line((qx - 14, 168), (qx + 14, 168))
    d.line((qx, 72), (qx, 62), (ex + er, ey + 12))
    d.group('mid')
    # the powder on plate B, and the ionised air between the plates
    d.lines([[(bx + 6 + 6 * i, by), (bx + 9 + 6 * i, by - 3), (bx + 12 + 6 * i, by)] for i in range(18)])
    d.lines([[(bx + 30 + 14 * i, by - 8), (bx + 30 + 14 * i, ay + 8)] for i in range(5)])
    d.arc(ex, ey, er - 6, 200, 340, n=16)                         # the scale
    d.line((ex, ey), (ex + 9, ey - 11))                           # the needle
    d.line((qx - 7, 160), (qx - 7, 166), (qx - 2, 166), (qx - 2, 160), closed=True)
    d.line((qx + 2, 162), (qx + 2, 166), (qx + 7, 166), (qx + 7, 162), closed=True)
    # --- fractional crystallisation: each dish splits into crystals (left, richer) and liquor (right)
    tx, ty, dx, dy, rows = 306, 76, 17, 30, 5
    pos = {(r, k): (tx + (k - r / 2) * dx * 2, ty + r * dy) for r in range(rows) for k in range(r + 1)}
    d.group('thin')
    d.line((tx, ty - 22), (tx, ty + (rows - 1) * dy + 14))
    d.group()
    for (r, k), (x, y) in pos.items():
        d.arc(x, y - 3, 8, 0, 180, n=16, ry=6)
        d.line((x - 8, y - 3), (x + 8, y - 3))
    d.group('mid')
    seg = []
    for (r, k), (x, y) in pos.items():
        if r < rows - 1:
            for kk in (k, k + 1):
                x2, y2 = pos[(r + 1, kk)]
                seg.append([(x + (x2 - x) * 0.3, y + 5), (x2 - (x2 - x) * 0.3, y2 - 12)])
    d.lines(seg)
    x0, y0 = pos[(rows - 1, 0)]
    x1, y1 = pos[(rows - 1, rows - 1)]
    d.line((x0, y0 + 10), (x0 - 10, y0 + 26))
    d.line((x1, y1 + 10), (x1 + 10, y1 + 26))
    d.group('mid')
    d.text(ex, ey - er - 8, 'ELECTROMETER', size=7)
    d.text(bx + bw / 2, 228, 'CONDENSER · QUARTZ BALANCE', size=7)
    d.text(tx, ty - 28, 'BARIUM + RADIUM CHLORIDES', size=7)
    d.text(x0 - 12, y0 + 38, 'CRYSTALS', size=7)
    d.text(x1 + 12, y1 + 38, 'LIQUOR', size=7)
    d.text(200, 272, 'RaCl₂ + 2 AgNO₃ → 2 AgCl + Ra(NO₃)₂')
    return d


def _offset_poly(pts, k):
    """A polyline offset sideways by k, with mitred corners (for glass round a wire)."""
    out = []
    for i, p in enumerate(pts):
        ns = []
        segs = ([(pts[i - 1], p)] if i else []) + ([(p, pts[i + 1])] if i < len(pts) - 1 else [])
        for a, b in segs:
            dx, dy = b[0] - a[0], b[1] - a[1]
            n = math.hypot(dx, dy)
            ns.append((-dy / n, dx / n))
        nx, ny = sum(n[0] for n in ns), sum(n[1] for n in ns)
        m = math.hypot(nx, ny)
        nx, ny = nx / m, ny / m
        cos = nx * ns[0][0] + ny * ns[0][1]
        out.append((p[0] + nx * k / cos, p[1] + ny * k / cos))
    return out


def noble_gases():
    """Cavendish's sparking tube over alkali, as Rayleigh and Ramsay repeated it, and the new column."""
    d = D()
    cx = 104                          # the tube's axis
    top, mouth = 46, 200              # the tube's closed top and open mouth
    r = 16                            # the tube's radius
    lvl = 176                         # the alkali's level in the dish
    d.group('thin')
    d.line((cx, top - 16), (cx, 262))
    d.line((24, lvl), (184, lvl))
    d.line((cx - 60, top + 30), (cx + 60, top + 30))            # the spark gap's level
    d.group()
    # the test tube, upside down, its round end at the top
    d.arc(cx, top + r, r, 180, 360, n=24)
    d.line((cx - r, top + r), (cx - r, mouth))
    d.line((cx + r, top + r), (cx + r, mouth))
    # the dish of alkali
    d.line((30, 150), (36, 236), (172, 236), (178, 150))
    # two platinum wires rising through U-shaped glass sleeves to a gap near the top
    for s_ in (-1, 1):
        x = cx + s_ * 6
        d.line((x, top + 26), (x, 226), (cx + s_ * 40, 226), (cx + s_ * 40, 138), (cx + s_ * 70, 110))
    d.group('mid')
    for s_ in (-1, 1):
        x = cx + s_ * 6
        u = [(x, top + 40), (x, 226), (cx + s_ * 40, 226), (cx + s_ * 40, 150)]
        d.line(*_offset_poly(u, 3))
        d.line(*_offset_poly(u, -3))
    # the spark, and the bubble left over
    d.line((cx - 5, top + 26), (cx - 1, top + 22), (cx + 1, top + 30), (cx + 5, top + 26))
    d.circle(cx, top + 8, 4)
    # the liquid surface inside the tube, risen as the gas was absorbed
    d.line((cx - r, top + 64), (cx + r, top + 64))
    d.lines([[(40 + 12 * i, 196 + 6 * (i % 2)), (46 + 12 * i, 196 + 6 * (i % 2))] for i in range(11)])
    # --- the table: halogens, the new column, the alkali metals
    x0, y0, w, h = 250, 48, 38, 30
    cols = [['H', 'F', 'Cl', 'Br', 'I'], ['He', 'Ne', 'Ar', 'Kr', 'Xe'], ['Li', 'Na', 'K', 'Rb', 'Cs']]
    shown = {(0, 2), (2, 2)}
    d.group('thin')
    for c in (0, 2):
        for k in range(5):
            x, y = x0 + c * w, y0 + k * h
            d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)
    d.group()
    for k in range(5):
        x, y = x0 + w, y0 + k * h
        d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)
    d.group('mid')
    for c, col in enumerate(cols):
        for k, sym in enumerate(col):
            if sym and (c == 1 or (c, k) in shown):
                d.text(x0 + c * w + w / 2, y0 + k * h + h / 2 + 4, sym, size=10)
    d.text(x0 + w * 1.5, y0 - 10, 'GROUP 0', size=8)
    d.text(x0 + w * 1.5, y0 + 5 * h + 22, 'Cl 35.5 · Ar 39.9 · K 39.1', size=8)
    d.text(cx, 256, 'SPARKS · OXYGEN · ALKALI', size=8)
    d.text(cx, top - 22, '1/120 LEFT OVER', size=8)
    return d


def moseley():
    """The X-ray spectrometer in plan (slit and plate equidistant from the crystal's axis), and sqrt(nu) against N."""
    d = D()
    ax_, ay_ = 118, 160              # the spectrometer's axis, on the crystal's face
    R = 74                           # slit and plate, both this far from the axis
    th = 24                          # the glancing angle, degrees
    sx, sy = ax_ - R, ay_            # the slit
    tx, ty = 26, ay_                 # the X-ray tube's target
    face = math.radians(-th)
    out = math.radians(-2 * th)      # the reflected ray's direction
    lx, ly = ax_ + R * math.cos(out), ay_ + R * math.sin(out)
    d.group('thin')
    d.circle(ax_, ay_, R)
    d.line((tx - 12, ay_), (ax_ + R + 12, ay_))
    d.line((ax_ - 40 * math.cos(face), ay_ - 40 * math.sin(face)), (ax_ + 40 * math.cos(face), ay_ + 40 * math.sin(face)))
    d.group()
    # the tube, its target on the truck, and the lead box's window
    d.circle(tx, ty, 16)
    d.line((tx - 6, ty + 6), (tx + 4, ty + 6), (tx + 4, ty - 6), (tx - 6, ty - 6), closed=True)
    d.line((sx, sy - 12), (sx, sy - 2))
    d.line((sx, sy + 2), (sx, sy + 12))
    # the crystal, its face through the axis
    c, s_ = math.cos(face), math.sin(face)
    n = (-s_, c)
    cr = [(ax_ - 22 * c, ay_ - 22 * s_), (ax_ + 22 * c, ay_ + 22 * s_)]
    d.line(cr[0], cr[1], (cr[1][0] + 7 * n[0], cr[1][1] + 7 * n[1]), (cr[0][0] + 7 * n[0], cr[0][1] + 7 * n[1]), closed=True)
    # the photographic plate, on the circle about the axis
    d.arc(ax_, ay_, R, -2 * th - 22, -2 * th + 22, n=24)
    d.group('mid')
    d.line((tx + 16, ty), (ax_, ay_), (lx, ly))
    d.arc(ax_, ay_, 30, -th, 0, n=10)                     # theta, between face and ray
    d.arc(ax_, ay_, 44, -2 * th, -th, n=10)
    # --- the law: sqrt(frequency) against N, from Moseley's own wavelengths
    data = [(19, 3.759), (20, 3.368), (22, 2.758), (23, 2.519), (24, 2.301), (25, 2.111),
            (26, 1.946), (27, 1.798), (28, 1.662), (29, 1.549), (30, 1.445)]
    px0, py0, pw, ph = 236, 214, 146, 150
    def P(N, r):
        return (px0 + (N - 18) / 13 * pw, py0 - (r - 0.85) / 0.65 * ph)
    pts = [P(N, (2.998e10 / (lam * 1e-8)) ** 0.5 / 1e9) for N, lam in data]
    d.group('thin')
    d.line((px0, py0 - ph), (px0, py0), (px0 + pw, py0))
    d.lines([[(P(N, 0.85)[0], py0), (P(N, 0.85)[0], py0 - ph)] for N in (20, 25, 30)])
    g = P(21, 0)[0]
    d.line((g, py0), (g, py0 - ph))
    d.group()
    a, b = pts[0], pts[-1]
    d.line((a[0] - 6, a[1] + 6 * (b[1] - a[1]) / (b[0] - a[0]) * -1), (b[0] + 6, b[1] + 6 * (b[1] - a[1]) / (b[0] - a[0])))
    d.group('mid')
    d.lines([[(x - 3, y - 3), (x + 3, y + 3)] for x, y in pts] + [[(x - 3, y + 3), (x + 3, y - 3)] for x, y in pts])
    x21 = P(21, 0)[0]
    y21 = a[1] + (x21 - a[0]) * (b[1] - a[1]) / (b[0] - a[0])
    d.circle(x21, y21, 4)
    d.group('mid')
    d.text(ax_, 44, 'CRYSTAL · PLATE · SLIT', size=7)
    d.text(ax_, 252, 'nλ = 2d sin θ', size=9)
    d.text(px0 + pw / 2, py0 + 16, 'N  20 · 25 · 30', size=7)
    d.text(px0 + pw / 2, py0 - ph - 10, '√ν RISES BY STEPS', size=7)
    d.text(x21 + 2, y21 + 16, 'Sc', size=7)
    d.text(px0 + pw / 2, 252, 'ν ∝ (N − 1)²', size=9)
    return d


PLATES = {'radium': radium, 'noble-gases': noble_gases, 'moseley': moseley}
