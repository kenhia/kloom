"""computing plates, the transistor and the trail "Transistor to Moore's law" (sprint 015). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _zigzag(x, y0, y1, w, n):
    """A spring: n zigzags between y0 and y1 about the line x."""
    pts = [(x, y0)]
    step = (y1 - y0) / (2 * n)
    for i in range(1, 2 * n):
        pts.append((x + (w if i % 2 else -w), y0 + step * i))
    pts.append((x, y1))
    return pts


def transistor():
    """Bardeen and Brattain's point-contact transistor in section: a gold-faced plastic wedge, split at its
    tip, pressed by a spring onto n-type germanium on a metal base; holes injected at the emitter point
    cross to the collector point. The gap is drawn wide; Bardeen gave it as about 0.005 cm."""
    d = D()
    cx, top, tip = 200, 58, 168          # the wedge's axis, its top face and its tip
    half = 62                            # half-width of the wedge's top face
    gap = 7                              # half the split at the tip (drawn, not to scale)
    gx0, gx1, gy0, gy1 = 92, 308, tip, 228   # the germanium block
    # construction: the wedge's axis, the faces produced to the tip, the surface line, the base plane
    d.group('thin')
    d.line((cx, 22), (cx, 262))
    d.line((cx - half, top), (cx, tip))
    d.line((cx + half, top), (cx, tip))
    d.line((60, gy0), (340, gy0))
    d.line((60, gy1 + 10), (340, gy1 + 10))
    for r in (16, 30, 44):              # hole paths as circles centred between the contacts
        d.arc(cx, gy0, r, 0, 180, n=36)
    # the object: block, base, wedge
    d.group()
    d.line((gx0, gy0), (gx1, gy0), (gx1, gy1), (gx0, gy1), closed=True)
    d.line((gx0 - 10, gy1), (gx1 + 10, gy1), (gx1 + 10, gy1 + 10), (gx0 - 10, gy1 + 10), closed=True)
    # the wedge is cut off short of the tip where the gold is split
    t = (tip - 4 - top) / (tip - top)
    lx, rx = cx - half * (1 - t), cx + half * (1 - t)
    d.line((cx - half, top), (cx + half, top), (rx, tip - 4), (lx, tip - 4), closed=True)
    # the gold foil on both faces, ending in the two contact points on the surface
    d.group('mid')
    off = 3.5
    ex, cxp = cx - gap, cx + gap
    d.line((cx - half - off, top + 6), (ex - 1, tip - 3), (ex, tip))
    d.line((cx + half + off, top + 6), (cxp + 1, tip - 3), (cxp, tip))
    # the spring, pressing the wedge down
    d.line(*_zigzag(cx, 22, top, 9, 5))
    d.line((cx - 20, 22), (cx + 20, 22))
    # the leads and the batteries: emitter biased forward (+), collector reverse (-)
    d.line((cx - half - off, top + 6), (40, top + 6), (40, 120))
    d.line((cx + half + off, top + 6), (360, top + 6), (360, 120))
    for x in (40, 360):
        d.line((x - 9, 120), (x + 9, 120))
        d.line((x - 5, 126), (x + 5, 126))
        d.line((x, 126), (x, gy1 + 30), (cx, gy1 + 30), (cx, gy1 + 10))
    # holes: arcs from the emitter point to the collector point through the germanium
    d.group('mid')
    for r in (16, 30, 44):
        d.arc(cx, gy0, r, 172, 8, n=30)
        _arrow(d, cx + r * math.cos(math.radians(22)), gy0 + r * math.sin(math.radians(22)), math.radians(22 - 90), 3.5)
    # labels
    d.group()
    d.text(cx, 90, 'WEDGE', size=7)
    d.text(ex - 12, gy0 - 8, 'E', size=8, anchor='end')
    d.text(cxp + 12, gy0 - 8, 'C', size=8, anchor='start')
    d.text(cx, gy0 + 52, 'n-GERMANIUM', size=8)
    d.text(cx, gy1 + 22, 'BASE', size=7)
    d.text(40, 142, '+', size=10)
    d.text(360, 142, '−', size=10)
    d.text(24, 100, 'EMITTER', size=7, anchor='start')
    d.text(376, 100, 'COLLECTOR', size=7, anchor='end')
    d.text(cx, 284, 'POINTS ≈ 0.005 CM APART · HOLES FROM E TO C', size=8)
    return d


def _diffused(cx, w, depth, y0, n=24):
    """The edge of a region diffused through a mask window of width w centred on cx: flat at `depth`
    under the window, and a quarter circle of radius `depth` about each mask edge (lateral diffusion)."""
    a, b = cx - w / 2, cx + w / 2
    pts = [(a + depth * math.cos(math.radians(180 - 90 * i / n)), y0 + depth * math.sin(math.radians(180 - 90 * i / n)))
           for i in range(n + 1)]
    pts = [(a - depth, y0)] + pts[1:]
    pts += [(b + depth * math.cos(math.radians(90 - 90 * i / n)), y0 + depth * math.sin(math.radians(90 - 90 * i / n)))
            for i in range(n + 1)]
    return pts


def silicon_valley():
    """Hoerni's planar transistor in section: base and emitter diffused through windows in the oxide,
    each junction curving up to the surface under the oxide that masked it, and the oxide left there as
    a seal, opened only where the aluminium contacts go down."""
    d = D()
    y0, ox = 150, 8                  # the silicon surface; oxide thickness, drawn
    bx, bw, bd = 200, 150, 44        # base window: centre, width, diffusion depth
    ex, ew, ed = 180, 56, 20         # emitter window
    windows = {'E': (160, 200), 'B': (250, 290), 'C': (336, 366)}   # contact windows in the final oxide
    # construction: the diffusion mask edges carried down, the lateral-diffusion arcs about them
    d.group('thin')
    for x in (bx - bw / 2, bx + bw / 2, ex - ew / 2, ex + ew / 2):
        d.line((x, 96), (x, y0 + 60))
    d.arc(bx - bw / 2, y0, bd, 90, 180, n=24)
    d.arc(bx + bw / 2, y0, bd, 0, 90, n=24)
    d.arc(ex - ew / 2, y0, ed, 90, 180, n=16)
    d.arc(ex + ew / 2, y0, ed, 0, 90, n=16)
    d.line((24, y0 + bd), (376, y0 + bd))
    # the wafer and the two junctions
    d.group()
    d.line((30, y0), (380, y0), (380, 262), (30, 262), closed=True)
    d.line(*_diffused(bx, bw, bd, y0))
    d.line(*_diffused(ex, ew, ed, y0))
    # the oxide, left in place everywhere but the three contact windows
    d.group('mid')
    edges = [30] + [v for k in ('E', 'B', 'C') for v in windows[k]] + [380]
    for a, b in zip(edges[0::2], edges[1::2]):
        d.line((a, y0), (a, y0 - ox), (b, y0 - ox), (b, y0))
    # aluminium: a pad down through each window, and its lead
    d.group()
    for k, (a, b) in windows.items():
        m = (a + b) / 2
        d.line((a - 4, y0 - ox - 5), (a - 4, y0 - ox), (a, y0 - ox), (a, y0), (b, y0), (b, y0 - ox), (b + 4, y0 - ox),
               (b + 4, y0 - ox - 5), (m + 3, y0 - ox - 5), (m + 3, 108), (m - 3, 108), (m - 3, y0 - ox - 5), closed=True)
    # labels
    d.group()
    for k, (a, b) in windows.items():
        d.text((a + b) / 2, 98, k, size=9)
    d.text(236, y0 + 28, 'p BASE', size=8)
    d.text(ex, y0 + 14, 'n⁺', size=8)
    d.text(200, 244, 'n COLLECTOR', size=8)
    d.text(60, y0 - 14, 'SiO₂', size=8)
    d.text(200, 60, 'OXIDE AS MASK, THEN AS SEAL', size=8)
    d.text(200, 284, 'JUNCTIONS END UNDER THE OXIDE THAT MASKED THEM', size=8)
    return d


def _catenary(x0, x1, y, sag, n=24, k=1.6):
    """A wire between (x0, y) and (x1, y), arched `sag` above them: an inverted catenary, cosh-shaped."""
    a, m = (x1 - x0) / 2, (x0 + x1) / 2
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        u = (math.cosh(k * (x - m) / a) - 1) / (math.cosh(k) - 1)
        pts.append((x, y - sag * (1 - u)))
    return pts


def integrated_circuit():
    """Two answers to wiring a chip. Above, Kilby's germanium bar (1958): mesa regions joined by gold
    wires in the air. Below, Noyce's planar chip (1959): diffused regions under oxide, joined by a
    metal line laid on the oxide and dropped through windows."""
    d = D()
    # --- Kilby: a bar in elevation, three mesas, flying wires
    ya = 118
    d.group('thin')
    d.line((30, ya), (370, ya))
    d.line((30, 234), (370, 234))
    mesas = [(90, 30), (190, 40), (300, 30)]
    for x, w in mesas:
        d.line((x, 44), (x, ya + 20))
    d.group()
    d.line((50, ya), (350, ya), (350, ya + 22), (50, ya + 22), closed=True)
    for x, w in mesas:
        d.line((x - w / 2 - 6, ya), (x - w / 2, ya - 10), (x + w / 2, ya - 10), (x + w / 2 + 6, ya))
    d.group('mid')
    d.line(*_catenary(96, 184, ya - 10, 44))
    d.line(*_catenary(200, 294, ya - 10, 52))
    d.line(*_catenary(306, 344, ya - 10, 26))
    d.line(*_catenary(58, 84, ya - 10, 22))
    for x in (58, 84, 96, 184, 200, 294, 306, 344):
        d.circle(x, ya - 10, 2)
    # --- Noyce: a section, three diffused wells under oxide, an aluminium line over the oxide
    yb = 234
    d.group()
    d.line((50, yb), (350, yb), (350, 272), (50, 272), closed=True)
    wells = [(110, 50), (200, 60), (295, 50)]
    for x, w in wells:
        d.line(*_diffused(x, w, 14, yb, n=12))
    d.group('mid')
    ox = 6
    opens = [(x + dx, x + dx + 10) for x, w in wells for dx in (-w / 2 + 4, w / 2 - 14)]
    edges = [50] + [v for o in opens for v in o] + [350]
    for a, b in zip(edges[0::2], edges[1::2]):
        d.line((a, yb), (a, yb - ox), (b, yb - ox), (b, yb))
    d.group()
    for (a1, b1), (a2, b2) in zip(opens[1::2], opens[2::2]):
        t = 4
        d.line((a1, yb), (a1, yb - ox - t), (b2, yb - ox - t), (b2, yb), (a2, yb), (a2, yb - ox), (b1, yb - ox), (b1, yb), closed=True)
    # labels
    d.group()
    d.text(200, 30, '1958 · GERMANIUM · WIRES IN THE AIR', size=8)
    d.text(200, 196, '1959 · SILICON · METAL ON THE OXIDE', size=8)
    d.text(200, 292, 'THE SECOND COULD BE PRINTED; THE FIRST HAD TO BE BONDED', size=7)
    return d


def apollo_guidance():
    """Core rope: eight cores on a set line; four sense wires, each threading a core for a 1 and passing
    outside it for a 0. Reading core k puts its column of bits on the sense wires."""
    d = D()
    bits = ['1011', '0110', '1100', '0011', '1001', '0101', '1110', '0001']   # an invented pattern, a column per core
    n = len(bits)
    xs = [60 + 40 * i for i in range(n)]
    ys = [92, 124, 156, 188]            # the four sense wires' rest heights
    ry, rx = 60, 11                     # a core seen edge-on as a tall ellipse spanning the wires
    ymid = 140
    # construction: the cores' centre lines, the sense wires' rest lines
    d.group('thin')
    d.lines([[(x, 60), (x, 226)] for x in xs])
    d.lines([[(26, y), (374, y)] for y in ys])
    # the cores
    d.group()
    for x in xs:
        d.ellipse(x, ymid, rx, ry)
        d.ellipse(x, ymid, rx - 5, ry - 6)
    # the set line through every core
    d.group('mid')
    d.line((26, 232), (374, 232))
    d.lines([[(x, 232), (x, ymid + ry)] for x in xs])
    # the sense wires: through the hole (a 1) or out and around the core (a 0)
    d.group()
    for j, y in enumerate(ys):
        pts = [(26, y)]
        for x, col in zip(xs, bits):
            if col[j] == '1':
                pts += [(x - 16, y), (x + 16, y)]
            else:
                side = -1 if y < ymid else 1
                out = ymid + side * (ry + 8 + 5 * (j if side > 0 else 3 - j))
                pts += [(x - 17, y), (x - 13, out), (x + 13, out), (x + 17, y)]
        pts.append((374, y))
        d.line(*pts)
    # labels
    d.group()
    for x, col in zip(xs, bits):
        d.text(x, 262, col, size=8)
    for j, y in enumerate(ys):
        d.text(386, y + 3, f'S{j}', size=7, anchor='middle')
    d.text(14, 235, 'SET', size=7, anchor='start')
    d.text(200, 34, 'THROUGH THE CORE = 1 · AROUND IT = 0', size=8)
    d.text(200, 286, 'AGC: 192 SENSE WIRES, 12 WORDS PER CORE', size=8)
    return d


def moores_law():
    """Moore's two 1965 graphs, redrawn. Left: cost per component against components per circuit, a
    minimum at about 50 in 1965 and about 1,000 in 1970 at a tenth the cost (the curves' shapes are a
    simple model; the minima are Moore's). Right: log₂ of components per circuit against year, doubling
    each year from 1959 to 1975."""
    d = D()
    # left panel: log-log axes, n from 1 to 10^5, cost from 10^-2 to 10^2 (relative)
    L0, L1, T0, T1 = 34, 190, 60, 236
    X = lambda n: L0 + (L1 - L0) * math.log10(n) / 5
    Y = lambda c: T1 - (T1 - T0) * (math.log10(c) + 2) / 4
    # right panel: years 1959 to 1975, log2 from 0 to 16
    R0, R1 = 222, 380
    YX = lambda yr: R0 + (R1 - R0) * (yr - 1959) / 16
    YY = lambda k: T1 - (T1 - T0) * k / 16
    d.group('thin')
    d.lines([[(X(10 ** k), T0), (X(10 ** k), T1)] for k in range(6)])
    d.lines([[(L0, Y(10 ** k)), (L1, Y(10 ** k))] for k in range(-2, 3)])
    d.lines([[(YX(y), T0), (YX(y), T1)] for y in range(1959, 1976, 4)])
    d.lines([[(R0, YY(k)), (R1, YY(k))] for k in range(0, 17, 4)])
    d.group()
    d.line((L0, T0), (L0, T1), (L1, T1))
    d.line((R0, T0), (R0, T1), (R1, T1))
    # cost curves: c(n) = (N·cmin/e)/n · exp(n/N), minimum cmin at n = N
    d.group('mid')
    for N, cmin in ((50, 1.0), (1000, 0.1)):
        pts = []
        for i in range(0, 201):
            n = 10 ** (5 * i / 200)
            if n / N > 20:
                break
            c = N * cmin / math.e / n * math.exp(n / N)
            if 10 ** -2 <= c <= 10 ** 2:
                pts.append((X(n), Y(c)))
        d.line(*pts)
        d.circle(X(N), Y(cmin), 2.2)
    # the doubling line, one step a year
    d.group()
    d.line(*[(YX(1959 + k), YY(k)) for k in range(17)])
    for k in (0, 6, 16):
        d.circle(YX(1959 + k), YY(k), 2.2)
    # labels
    d.group()
    d.text(X(50), Y(1.0) - 10, '1965', size=7)
    d.text(X(1000), Y(0.1) + 16, '1970', size=7)
    d.text((L0 + L1) / 2, T1 + 16, 'COMPONENTS PER CIRCUIT', size=7)
    d.text((L0 + L1) / 2, 44, 'COST PER COMPONENT', size=7)
    d.text((R0 + R1) / 2, 44, 'LOG₂ COMPONENTS', size=7)
    for y in (1959, 1967, 1975):
        d.text(YX(y), T1 + 16, str(y), size=7)
    d.text(YX(1965) + 6, YY(6) - 6, '64', size=7, anchor='end')
    d.text(YX(1975) - 10, YY(16) + 16, '65,000', size=7, anchor='end')
    d.text(200, 282, 'ELECTRONICS · 19 APRIL 1965 · DOUBLING EACH YEAR', size=8)
    return d


def end_of_scaling():
    """The gate closes round the channel. Three sections across the channel: a planar transistor (gate
    on one side), a FinFET (three sides of a fin) and a nanosheet or gate-all-around transistor (every
    side of three stacked sheets)."""
    d = D()
    base = 214
    cols = [70, 200, 330]
    # construction: the silicon surface, the column axes, the gate's reach
    d.group('thin')
    d.line((14, base), (386, base))
    d.lines([[(x, 58), (x, 250)] for x in cols])
    # the silicon: a flat top, a fin, three sheets over a stub
    d.group()
    x = cols[0]
    d.line((x - 52, base), (x - 52, base + 30), (x + 52, base + 30), (x + 52, base))
    d.line((x - 30, base), (x + 30, base))
    x = cols[1]
    d.line((x - 52, base + 30), (x - 52, base), (x - 9, base), (x - 9, 120), (x + 9, 120), (x + 9, base), (x + 52, base), (x + 52, base + 30))
    x = cols[2]
    d.line((x - 52, base + 30), (x - 52, base), (x - 10, base), (x - 10, base - 10), (x + 10, base - 10), (x + 10, base), (x + 52, base), (x + 52, base + 30))
    sheets = [base - 34, base - 64, base - 94]
    for y in sheets:
        d.line((x - 26, y), (x + 26, y), (x + 26, y + 10), (x - 26, y + 10), closed=True)
    # oxide and gate
    d.group('mid')
    x = cols[0]
    d.line((x - 30, base), (x - 30, base - 5), (x + 30, base - 5), (x + 30, base))
    d.line((x - 36, base - 5), (x - 36, base - 40), (x + 36, base - 40), (x + 36, base - 5), closed=True)
    x = cols[1]
    d.line((x - 15, base), (x - 15, 114), (x + 15, 114), (x + 15, base))
    d.line((x - 40, base), (x - 40, 94), (x + 40, 94), (x + 40, base))
    x = cols[2]
    for y in sheets:
        d.line((x - 31, y - 5), (x + 31, y - 5), (x + 31, y + 15), (x - 31, y + 15), closed=True)
    d.line((x - 40, base), (x - 40, sheets[-1] - 16), (x + 40, sheets[-1] - 16), (x + 40, base))
    # labels
    d.group()
    d.text(cols[0], 48, 'PLANAR', size=8)
    d.text(cols[1], 48, 'FINFET', size=8)
    d.text(cols[2], 48, 'NANOSHEET', size=8)
    d.text(cols[0], 64, 'GATE ON 1 SIDE', size=7)
    d.text(cols[1], 64, '3 SIDES · 2011', size=7)
    d.text(cols[2], 64, '4 SIDES · 2022', size=7)
    d.text(cols[0], base - 18, 'GATE', size=7)
    d.text(200, 284, 'SECTIONS ACROSS THE CHANNEL · SILICON, OXIDE, GATE', size=8)
    return d


PLATES = {
    'transistor': transistor,
    'silicon-valley': silicon_valley,
    'integrated-circuit': integrated_circuit,
    'apollo-guidance': apollo_guidance,
    'moores-law': moores_law,
    'end-of-scaling': end_of_scaling,
}
