"""feynman plates, trail "The diagrams" (sprint 014). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians, page coordinates)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _mid_arrow(d, a, b, size=5, at=0.55):
    """An arrowhead part-way along the segment a→b, pointing from a to b."""
    x, y = a[0] + (b[0] - a[0]) * at, a[1] + (b[1] - a[1]) * at
    _arrow(d, x, y, math.atan2(b[1] - a[1], b[0] - a[0]), size)


def _wave(a, b, amp=3.5, waves=5, n=120):
    """A photon line: a sine wiggle from a to b with a whole number of waves, so it meets both ends."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    px, py = -dy / length, dx / length
    return [(a[0] + dx * i / n + px * amp * math.sin(2 * math.pi * waves * i / n),
             a[1] + dy * i / n + py * amp * math.sin(2 * math.pi * waves * i / n)) for i in range(n + 1)]


def _wave_arc(cx, cy, r, a0, a1, amp=3.0, waves=6, n=160):
    """A photon line wiggling along a circular arc (angles in degrees, page coordinates)."""
    pts = []
    for i in range(n + 1):
        t = math.radians(a0 + (a1 - a0) * i / n)
        rr = r + amp * math.sin(2 * math.pi * waves * i / n)
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    return pts


def _dot(d, p, r=2.3):
    d.circle(p[0], p[1], r)


# --- lamb-shift: the n = 2 levels of hydrogen, as Dirac had them and as Lamb found them ---------

FINE = 10969.0   # 2P3/2 − 2P1/2 in hydrogen, MHz
LAMB = 1057.8    # 2S1/2 − 2P1/2, MHz


def lamb_shift():
    """Hydrogen's n = 2 levels to scale: Dirac's degenerate pair, the measured split, and the split magnified."""
    d = D()
    px = 150 / FINE             # pixels per MHz on the main scale
    base, top = 214, 214 - FINE * px
    lamb = LAMB * px            # the shift at that scale: about 14 px
    mag = 6                     # the inset's magnification
    ix0, ix1, ib = 300, 382, 250  # the inset: its level lines and its baseline
    # construction: the energy scale in 1,000 MHz steps, the ties across columns, the zoom lines
    d.group('thin')
    d.lines([[(22, base - k * 1000 * px), (27, base - k * 1000 * px)] for k in range(0, 12)])
    d.line((24, base + 6), (24, top - 12))
    d.lines([[(128, top), (186, top)], [(128, base), (186, base)], [(128, base), (186, base - lamb)]])
    d.line((180, base - lamb - 10), (276, base - lamb - 10), (276, base + 8), (180, base + 8), closed=True)
    d.lines([[(276, base - lamb - 10), (ix0 - 4, ib - LAMB * px * mag - 14)], [(276, base + 8), (ix0 - 4, ib + 10)]])
    # the levels: Dirac's theory (1928) on the left, Lamb and Retherford's hydrogen (1947) on the right
    d.group()
    d.line((48, top), (128, top))
    d.line((48, base), (128, base))
    d.line((186, top), (266, top))
    d.line((186, base), (266, base))
    d.line((186, base - lamb), (266, base - lamb))
    # the inset, six times larger: the shift, the microwave that drives across it, the 2P decay
    d.group('mid')
    s_y = ib - LAMB * px * mag
    d.line((ix0, ib), (ix1, ib))
    d.line((ix0, s_y), (ix1, s_y))
    d.line(*_wave((ix0 + 22, s_y + 2), (ix0 + 22, ib - 2), amp=3, waves=6))
    _arrow(d, ix0 + 22, ib - 2, math.pi / 2, 4)
    d.line((ix0 + 58, ib), (ix0 + 58, s_y))
    _arrow(d, ix0 + 58, s_y, -math.pi / 2, 4)
    _arrow(d, ix0 + 58, ib, math.pi / 2, 4)
    d.line((ix0 + 40, ib), (ix0 + 40, 284))
    _arrow(d, ix0 + 40, 284, math.pi / 2, 4)
    # the measured shift, marked on the main drawing too
    d.group()
    d.line((272, base - lamb), (272, base))
    # labels
    d.group()
    d.text(200, 20, 'HYDROGEN · n = 2 · TO SCALE', size=8)
    d.text(88, 44, 'DIRAC 1928', size=7)
    d.text(226, 44, 'MEASURED 1947', size=7)
    d.text(88, top - 5, '2P3/2', size=7)
    d.text(226, top - 5, '2P3/2', size=7)
    d.text(88, base + 12, '2S1/2 = 2P1/2', size=7)
    d.text(226, base - lamb - 5, '2S1/2', size=7)
    d.text(226, base + 12, '2P1/2', size=7)
    d.text(32, (top + base) / 2 + 3, '10,969 MHz', size=7, anchor='start')
    d.text(341, s_y - 6, '× 6', size=7)
    d.text(ix1, s_y - 6, '2S1/2', size=7, anchor='end')
    d.text(ix1, ib + 11, '2P1/2', size=7, anchor='end')
    d.text(ix0 + 62, (ib + s_y) / 2 + 3, '1,058', size=7, anchor='start')
    d.text(ix0 + 36, 292, 'TO 1S', size=7, anchor='end')
    return d


# --- propagators: the pieces, and why two more vertices cost a factor of alpha ----------------

def propagators():
    """The three pieces and their factors, then one-photon and two-photon exchange between two electrons."""
    d = D()
    # construction: the legend's row, the two panels' time lines and centre lines
    d.group('thin')
    d.line((20, 100), (380, 100))
    d.lines([[(40, y), (180, y)] for y in (128, 170, 212, 254)])
    d.lines([[(220, y), (380, y)] for y in (128, 170, 212, 254)])
    d.line((200, 108), (200, 272))
    # the legend: an electron line, a photon line, a vertex
    d.group()
    d.line((34, 58), (104, 58))
    _mid_arrow(d, (34, 58), (104, 58), 5, 0.6)
    d.line(*_wave((160, 58), (230, 58), amp=3.5, waves=5))
    v = (318, 60)
    d.line((282, 76), v, (354, 76))
    _mid_arrow(d, (282, 76), v, 4, 0.55)
    _mid_arrow(d, v, (354, 76), 4, 0.55)
    d.line(*_wave(v, (318, 30), amp=3, waves=3))
    _dot(d, v)
    # panel 1: one photon exchanged, two vertices
    a0, a1 = (74, 262), (74, 118)
    b0, b1 = (146, 262), (146, 118)
    va, vb = (74, 190), (146, 190)
    d.line(a0, a1)
    d.line(b0, b1)
    for s, e in ((a0, va), (va, a1), (b0, vb), (vb, b1)):
        _mid_arrow(d, s, e, 5, 0.55)
    # panel 2: two photons exchanged, four vertices (the box)
    c0, c1 = (256, 262), (256, 118)
    e0, e1 = (344, 262), (344, 118)
    w = [(256, 222), (344, 222), (256, 158), (344, 158)]
    d.line(c0, c1)
    d.line(e0, e1)
    for s, e in ((c0, w[0]), (w[2], c1), (e0, w[1]), (w[3], e1)):
        _mid_arrow(d, s, e, 5, 0.55)
    # the virtual photons and the vertices
    d.group('mid')
    d.line(*_wave(va, vb, amp=3.5, waves=6))
    d.line(*_wave(w[0], w[1], amp=3.5, waves=7))
    d.line(*_wave(w[2], w[3], amp=3.5, waves=7))
    for p in (va, vb, *w):
        _dot(d, p)
    # labels
    d.group()
    d.text(69, 80, 'ELECTRON', size=7)
    d.text(195, 80, 'PHOTON', size=7)
    d.text(318, 90, 'VERTEX', size=7)
    d.text(69, 46, 'i / (p̸ − m)', size=7)
    d.text(195, 46, '−i g / q²', size=7)
    d.text(352, 40, '−ieγ', size=7, anchor='start')
    d.text(110, 284, '2 VERTICES · e² · α', size=7)
    d.text(300, 284, '4 VERTICES · e⁴ · α²', size=7)
    d.text(110, 114, 'ONE PHOTON', size=7)
    d.text(300, 114, 'TWO PHOTONS', size=7)
    d.text(200, 20, 'EACH LINE A FACTOR · EACH DIAGRAM ONE TERM', size=8)
    return d


# --- backwards-in-time: one world line, cut by three moments ---------------------------------

def _rounded(pts, r=14, n=10):
    """A polyline with each inner corner replaced by a quadratic curve r pixels either side of it."""
    out = [pts[0]]
    for k in range(1, len(pts) - 1):
        a, b, c = pts[k - 1], pts[k], pts[k + 1]
        la, lc = math.dist(a, b), math.dist(b, c)
        p0 = (b[0] + (a[0] - b[0]) * r / la, b[1] + (a[1] - b[1]) * r / la)
        p2 = (b[0] + (c[0] - b[0]) * r / lc, b[1] + (c[1] - b[1]) * r / lc)
        for i in range(n + 1):
            u = i / n
            out.append(((1 - u) ** 2 * p0[0] + 2 * u * (1 - u) * b[0] + u * u * p2[0],
                        (1 - u) ** 2 * p0[1] + 2 * u * (1 - u) * b[1] + u * u * p2[1]))
    out.append(pts[-1])
    return out


def backwards_in_time():
    """A single world line that doubles back in time, and the moments that cut it once, three times, once."""
    d = D()
    t_lo, t_hi = 252, 40             # early at the bottom, late at the top
    c0, e2, e1, a1 = (300, t_lo), (236, 100), (176, 204), (128, t_hi)   # C rises to 2; B runs back to 1; A rises
    line = _rounded([c0, e2, e1, a1], r=16)
    slices = [(230, 'ONE'), (152, 'THREE'), (70, 'ONE')]
    # construction: the moments, the two events' times, light-cone lines through each event
    d.group('thin')
    d.lines([[(40, y), (380, y)] for y, _ in slices])
    for (x, y) in (e1, e2):
        d.lines([[(x - 40, y - 40), (x + 40, y + 40)], [(x - 40, y + 40), (x + 40, y - 40)]])
    # the world line, with the direction it runs: up, back down, up
    d.group()
    d.line(*line)
    _mid_arrow(d, c0, e2, 6, 0.45)
    _mid_arrow(d, e2, e1, 6, 0.55)
    _mid_arrow(d, e1, a1, 6, 0.55)
    # where each moment meets it
    d.group('mid')
    for y, _ in slices:
        for k in range(len(line) - 1):
            (xa, ya), (xb, yb) = line[k], line[k + 1]
            if (ya - y) * (yb - y) < 0:
                d.circle(xa + (xb - xa) * (y - ya) / (yb - ya), y, 3.2)
    # axes
    d.group()
    d.line((24, t_lo), (24, t_hi - 4))
    _arrow(d, 24, t_hi - 4, -math.pi / 2, 5)
    d.line((24, t_lo), (384, t_lo))
    _arrow(d, 384, t_lo, 0, 5)
    # labels
    d.group()
    d.text(200, 20, 'ONE LINE, READ ONE MOMENT AT A TIME', size=8)
    d.text(32, t_hi + 2, 'TIME', size=7, anchor='start')
    d.text(380, t_lo + 14, 'SPACE', size=7, anchor='end')
    for y, n in slices:
        d.text(380, y - 5, n, size=7, anchor='end')
    d.text(e2[0] + 46, e2[1] + 4, '2 · ANNIHILATION', size=7, anchor='start')
    d.text(e1[0] - 46, e1[1] + 4, '1 · PAIR MADE', size=7, anchor='end')
    d.text(288, 206, 'e⁻', size=8, anchor='start')
    d.text(214, 160, 'e⁺', size=8, anchor='start')
    d.text(138, 110, 'e⁻', size=8, anchor='end')
    return d


# --- dyson: two time orders are one diagram ----------------------------------------------------

def dyson():
    """The two time orders of old perturbation theory, emitted by a or by b, summed into one Feynman diagram."""
    d = D()
    y0, y1 = 236, 78
    panels = [60, 180, 318]
    lo, hi = 188, 128            # the two event times
    # construction: equal-time lines in the two ordered panels, the time axis ticks
    d.group('thin')
    d.lines([[(22, y), (242, y)] for y in (lo, hi)])
    d.lines([[(270, y), (380, y)] for y in range(int(y1), int(y0) + 1, 26)])
    # the electrons: two straight world lines in each panel
    d.group()
    ev = []
    for i, cx in enumerate(panels):
        ax, bx = cx - 30, cx + 30
        d.line((ax, y0), (ax, y1))
        d.line((bx, y0), (bx, y1))
        for x in (ax, bx):
            _mid_arrow(d, (x, y0), (x, y1), 5, 0.2)
            _mid_arrow(d, (x, y0), (x, y1), 5, 0.88)
        if i == 0:
            ev.append(((ax, lo), (bx, hi)))      # a emits first
        elif i == 1:
            ev.append(((bx, lo), (ax, hi)))      # b emits first
        else:
            ev.append(((ax, 158), (bx, 158)))    # no order: the Feynman propagator
    # the photons: slanted in time in the ordered panels, level in the diagram
    d.group('mid')
    for (p, q) in ev:
        d.line(*_wave(p, q, amp=3.2, waves=6))
        _dot(d, p)
        _dot(d, q)
    # the sum
    d.group()
    d.lines([[(114, 158), (126, 158)], [(120, 152), (120, 164)]])
    d.lines([[(244, 154), (258, 154)], [(244, 162), (258, 162)]])
    d.line((12, y0), (12, y1 - 6))
    _arrow(d, 12, y1 - 6, -math.pi / 2, 5)
    # labels
    d.group()
    d.text(200, 22, 'TWO ORDERINGS IN TIME = ONE DIAGRAM', size=8)
    d.text(20, y1 - 4, 'TIME', size=7, anchor='start')
    for cx in panels:
        d.text(cx - 30, y0 + 13, 'a', size=8)
        d.text(cx + 30, y0 + 13, 'b', size=8)
    d.text(60, 262, 'a EMITS FIRST', size=7)
    d.text(180, 262, 'b EMITS FIRST', size=7)
    d.text(318, 262, 'FEYNMAN', size=7)
    d.text(120, 280, 'SCHWINGER · TOMONAGA: TERM BY TERM', size=7)
    d.text(318, 280, 'ONE PROPAGATOR', size=7)
    return d


# --- magnetic-moment: Schwinger's vertex, and the next order's seven -----------------------------

def magnetic_moment():
    """Schwinger's one-loop vertex, large, and the seven two-loop diagrams of the next order, small."""
    d = D()
    cx, cy = 200, 118
    a, v, b = (cx - 92, cy + 58), (cx, cy - 20), (cx + 92, cy + 58)
    p0 = (a[0] + (v[0] - a[0]) * 0.42, a[1] + (v[1] - a[1]) * 0.42)
    p1 = (v[0] + (b[0] - v[0]) * 0.58, v[1] + (b[1] - v[1]) * 0.58)
    cells = [(28 + 49 * i, 240) for i in range(7)]
    # construction: the magnet's pole face and its hatching, the small diagrams' cells
    d.group('thin')
    d.lines([[(cx - 60 + 8 * k, 30), (cx - 52 + 8 * k, 22)] for k in range(15)])
    d.lines([[(x - 21, y - 24), (x + 21, y - 24), (x + 21, y + 22), (x - 21, y + 22), (x - 21, y - 24)] for x, y in cells])
    d.group()
    d.line((cx - 62, 30), (cx + 62, 30))
    # the electron line and the photon from the field
    d.line(a, v, b)
    _mid_arrow(d, a, p0, 5, 0.5)
    _mid_arrow(d, p1, b, 5, 0.6)
    d.line(*_wave(v, (cx, 32), amp=3.5, waves=5))
    # the virtual photon, emitted before the kick and absorbed after it
    d.group('mid')
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    r = math.dist(p0, p1) / 2
    ang0 = math.degrees(math.atan2(p0[1] - my, p0[0] - mx))
    d.line(*_wave_arc(mx, my, r, ang0, ang0 - 180, amp=3, waves=8))
    for p in (p0, p1, v):
        _dot(d, p)
    # the seven fourth-order vertex diagrams: two photons placed along the line (t from 0 in to 1 out)
    d.group('mid')
    kinds = [((0.12, 0.88), (0.3, 0.7)),     # one photon inside the other
             ((0.12, 0.62), (0.38, 0.88)),   # crossed
             ((0.08, 0.3), (0.7, 0.92)),     # a self-energy on each side
             ((0.05, 0.45), (0.18, 0.32)),   # nested, before the kick
             ((0.55, 0.95), (0.68, 0.82)),   # nested, after the kick
             ((0.05, 0.3), (0.2, 0.45)),     # overlapping, before the kick
             ((0.15, 0.85), 'loop')]         # the photon carries an electron loop
    for (x, y), (ph0, ph1) in zip(cells, kinds):
        aa, vv, bb = (x - 17, y + 14), (x, y - 8), (x + 17, y + 14)
        d.line(aa, vv, bb)
        d.line(*_wave(vv, (x, y - 22), amp=1.2, waves=3, n=40))

        def at(t, aa=aa, vv=vv, bb=bb):
            if t <= 0.5:
                u = t / 0.5
                return (aa[0] + (vv[0] - aa[0]) * u, aa[1] + (vv[1] - aa[1]) * u)
            u = (t - 0.5) / 0.5
            return (vv[0] + (bb[0] - vv[0]) * u, vv[1] + (bb[1] - vv[1]) * u)
        for k, ph in enumerate((ph0, ph1)):
            if ph == 'loop':
                continue
            q0, q1 = at(ph[0]), at(ph[1])
            m = ((q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2)
            depth = 7 if ph1 == 'loop' else 5 + 3 * (1 - k)
            # a quadratic curve that sags `depth` pixels below the chord at its middle
            d.line(*[((1 - u) ** 2 * q0[0] + 2 * u * (1 - u) * m[0] + u * u * q1[0],
                      (1 - u) ** 2 * q0[1] + 2 * u * (1 - u) * (m[1] + 2 * depth) + u * u * q1[1])
                     for u in (i / 20 for i in range(21))])
        if ph1 == 'loop':
            q0, q1 = at(ph0[0]), at(ph0[1])
            d.circle((q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2 + 7, 3.2)
    # labels
    d.group()
    d.text(200, 288, 'NEXT ORDER · 7 DIAGRAMS · α²', size=7)
    d.text(cx + 10, 48, 'MAGNET', size=7, anchor='start')
    d.text(cx, 208, 'α / 2π', size=9)
    d.text(a[0] - 4, a[1] + 12, 'IN', size=7)
    d.text(b[0] + 4, b[1] + 12, 'OUT', size=7)
    d.text(320, 104, 'SCHWINGER 1948', size=7)
    d.text(320, 116, '1 DIAGRAM · α', size=7)
    return d


# --- diagrams-spread: the postdoc cascade, drawn as a diagram -----------------------------------

CASCADE = [
    # (name, angle in degrees from the Institute, carried there by)
    ('COLUMBIA', 200, 'KROLL'),
    ('CORNELL', 232, 'ROHRLICH'),
    ('IOWA', 262, 'ROHRLICH'),
    ('BERKELEY', 292, 'WATSON'),
    ('INDIANA', 318, 'WATSON'),
    ('MADISON', 344, 'WATSON'),
    ('HARVARD', 160, 'KARPLUS'),
    ('STANFORD', 18, 'YENNIE'),
]


def diagrams_spread():
    """The Institute for Advanced Study at the centre; postdocs carry the diagrams outward, students take them further."""
    d = D()
    c = (200, 152)
    r1, r2, sq = 78, 118, 0.78   # the two generations' radii, and the vertical squash of the rings

    def at(ang, r):
        t = math.radians(ang)
        return (c[0] + r * math.cos(t), c[1] + r * math.sin(t) * sq)
    # construction: the generations as rings, and a ray to each department
    d.group('thin')
    d.ellipse(*c, r1, r1 * sq)
    d.ellipse(*c, r2, r2 * sq)
    for _, ang, _ in CASCADE:
        d.line(at(ang, 10), at(ang, r2 + 6))
    # the postdocs: arrowed lines from the Institute to each department
    d.group()
    d.ellipse(*c, 10, 10)
    for _, ang, _ in CASCADE:
        s, p = at(ang, 10), at(ang, r1)
        d.line(s, p)
        _mid_arrow(d, s, p, 5, 0.6)
    # their students: two lines out from each department
    d.group('mid')
    for _, ang, _ in CASCADE:
        p = at(ang, r1)
        _dot(d, p, 3)
        for dt in (-8, 8):
            q = at(ang + dt, r2)
            d.line(p, q)
            _mid_arrow(d, p, q, 4, 0.7)
            d.circle(q[0], q[1], 2)
    # labels, outside the students
    d.group()
    d.text(c[0], c[1] + 3, 'IAS', size=7)
    for name, ang, _ in CASCADE:
        x, y = at(ang, r2 + 16)
        cs = math.cos(math.radians(ang))
        anchor = 'start' if cs > 0.25 else ('end' if cs < -0.25 else 'middle')
        d.text(x, y + 3, name, size=7, anchor=anchor)
    d.text(200, 18, 'PRINCETON → POSTDOCS → THEIR STUDENTS · 1949–54', size=8)
    d.text(200, 290, '114 AUTHORS · 139 PAPERS IN PHYSICAL REVIEW', size=7)
    return d


PLATES = {
    'lamb-shift': lamb_shift,
    'propagators': propagators,
    'backwards-in-time': backwards_in_time,
    'dyson': dyson,
    'magnetic-moment': magnetic_moment,
    'diagrams-spread': diagrams_spread,
}
