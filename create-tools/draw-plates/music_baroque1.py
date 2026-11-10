"""Plates for Sound and Score's part baroque1 (sprint 058): monteverdi-orfeo, cremona-violins.
See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def monteverdi_orfeo():
    """A figured bass, C E F G G C, on a staff, with the chord each figure asks for stacked above
    its note as intervals counted up from the bass (1 is the bass itself, 8 its octave). The figures
    are the reading's table: none (3 and 5 understood), 6, none, 4 falling to 3 (shown as 4, then 7
    with its 3), none. The notes are an example, not a passage from Peri or Monteverdi."""
    d = D()
    step_staff = 4                       # a diatonic step on the staff (half a line gap)
    bottom = 238                         # the staff's lowest line, G2 in the bass clef
    def staff_y(step):                   # step 0 = G2, 3 = C3, 5 = E3, 6 = F3, 7 = G3
        return bottom - step * step_staff
    names = 'GABCDEFG'
    cols = [(3, '', (1, 3, 5, 8)), (5, '6', (1, 3, 6, 8)), (6, '', (1, 3, 5, 8)),
            (7, '4', (1, 4, 5, 8)), (7, '7', (1, 3, 5, 7)), (3, '', (1, 3, 5, 8))]
    xs = [96 + i * 50 for i in range(len(cols))]
    base, rung = 170, 12                 # interval 1 sits at y=170; each interval step up is 12
    def iv_y(n):
        return base - (n - 1) * rung

    # construction: the interval levels, across every column, and each column's ladder of steps
    d.group('thin')
    for n in (1, 3, 5, 8):
        d.line((70, iv_y(n)), (xs[-1] + 22, iv_y(n)))
    for x in xs:
        d.line((x, iv_y(1)), (x, iv_y(8)))
        d.lines([[(x - 3, iv_y(n)), (x + 3, iv_y(n))] for n in range(1, 9)])
    for x, (st, _, _) in zip(xs, cols):          # each note's line up to its column
        d.dashed((x, staff_y(st) - 6), (x, iv_y(1) + 6), dash=2, gap=2)

    # the object: the staff and the bass's notes
    d.group()
    d.lines([[(56, staff_y(2 * k)), (380, staff_y(2 * k))] for k in range(5)])
    d.line((56, staff_y(0)), (56, staff_y(8)))
    d.line((380, staff_y(0)), (380, staff_y(8)))
    d.line((377, staff_y(0)), (377, staff_y(8)))
    for x, (st, _, _) in zip(xs, cols):
        d.ellipse(x, staff_y(st), 5.2, 3.6)
    # the chords, stacked: a filled-looking ring for each note the figure asks for
    for x, (_, _, tones) in zip(xs, cols):
        for n in tones:
            d.circle(x, iv_y(n), 4.2 if n == 1 else 3.6)

    # detail: the 4 that falls to the 3, and the bass clef's two dots and curl, drawn plainly
    d.group('mid')
    p, q = (xs[3] + 6, iv_y(4)), (xs[4] - 6, iv_y(3))
    d.line(p, q)
    _arrow(d, p, q, 4)
    cy = staff_y(6)                       # the F line, which the bass clef names
    d.arc(70, cy, 6, 200, 380)
    d.line((76, cy + 1), (72, cy + 12), (64, cy + 18))
    d.circle(80, cy - 3, 0.9)
    d.circle(80, cy + 3, 0.9)

    d.group('mid')
    for n in (1, 3, 5, 8):
        d.text(64, iv_y(n) + 2.5, str(n), size=7, anchor='end')
    for x, (st, fig, _) in zip(xs, cols):
        if fig:
            d.text(x, staff_y(8) - 8, fig, size=7)
        d.text(x, bottom + 16, names[st], size=7)
    d.text(200, 62, 'EACH FIGURE COUNTS UP FROM THE BASS NOTE', size=7)
    d.text(200, 286, 'FIGURED BASS · THE CHORD EACH FIGURE ASKS FOR', size=7)
    return d


def _violin_outline():
    """Half the outline of a violin's body, in mm, x outward from the center line and y down from
    the top block, as a list of points from the top center to the bottom center. Body length 356 mm
    (a full-size violin); bout widths about 168, 112 and 206 mm (the Met's two violins are 202 and
    203 mm wide). The bouts are ellipse arcs and the C-bout a circular arc through its corners and
    its narrowest point: a schematic outline, not a maker's pattern."""
    L = 356.0
    pts = []
    # upper bout: ellipse centered on the axis
    cu, au, bu = 82.0, 84.0, 82.0
    yc1 = 128.0
    t_end = math.asin((yc1 - cu) / bu)
    for i in range(0, 31):
        t = -math.pi / 2 + (t_end + math.pi / 2) * i / 30
        pts.append((au * math.cos(t), cu + bu * math.sin(t)))
    corner1 = (pts[-1][0] + 6, pts[-1][1] + 3)
    # lower bout
    cl, al, bl = L - 104.0, 103.0, 104.0
    yc2 = 206.0
    t_start = math.asin((yc2 - cl) / bl)
    lower = []
    for i in range(0, 31):
        t = t_start + (math.pi / 2 - t_start) * i / 30
        lower.append((al * math.cos(t), cl + bl * math.sin(t)))
    corner2 = (lower[0][0] + 6, lower[0][1] - 3)
    # C-bout: the circle through corner1, the waist (56, ym) and corner2
    p1, p3 = (corner1[0] - 4, corner1[1] + 4), (corner2[0] - 4, corner2[1] - 4)
    ym = (p1[1] + p3[1]) / 2
    p2 = (56.0, ym)
    ax, ay = p1; bx, by = p2; cx_, cy_ = p3
    dd = 2 * (ax * (by - cy_) + bx * (cy_ - ay) + cx_ * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy_) + (bx * bx + by * by) * (cy_ - ay) + (cx_ * cx_ + cy_ * cy_) * (ay - by)) / dd
    uy = ((ax * ax + ay * ay) * (cx_ - bx) + (bx * bx + by * by) * (ax - cx_) + (cx_ * cx_ + cy_ * cy_) * (bx - ax)) / dd
    r = math.dist((ux, uy), p1)
    a1, a3 = math.atan2(p1[1] - uy, p1[0] - ux), math.atan2(p3[1] - uy, p3[0] - ux)
    if a3 < a1:
        a3 += 2 * math.pi
    cb = [(ux + r * math.cos(a1 + (a3 - a1) * i / 20), uy + r * math.sin(a1 + (a3 - a1) * i / 20)) for i in range(21)]
    if math.dist(cb[10], p2) > 1:     # the other way round the circle
        a1 += 2 * math.pi
        cb = [(ux + r * math.cos(a1 + (a3 - a1) * i / 20), uy + r * math.sin(a1 + (a3 - a1) * i / 20)) for i in range(21)]
    return pts + [corner1] + cb + [corner2] + lower


def cremona_violins():
    """Left: a violin's top in plan, from the computed outline, with its f-holes, the bridge, and
    (dashed, hidden inside) the bass bar under the bass foot and the soundpost behind the treble
    foot. Right: the body cut across at the bridge, schematic and to a larger scale: arched spruce
    top, arched maple back, ribs, the bass bar glued under the top and the soundpost standing loose
    between top and back. Arching about 15 mm, ribs about 30 mm: typical figures, not one violin's."""
    d = D()
    half = _violin_outline()
    s, X0, Y0 = 0.70, 112, 26           # plan: 0.70 px per mm, center line x=112, top at y=26
    def P(x, y):
        return (X0 + x * s, Y0 + y * s)
    right = [P(x, y) for x, y in half]
    left = [P(-x, y) for x, y in reversed(half)]
    bridge_y = 196.0                    # the bridge stands between the f-holes' inner notches

    d.group('thin')
    d.line(P(0, -6), P(0, 362))                                      # center line
    d.line(P(-118, bridge_y), (226, Y0 + bridge_y * s))                # the cut, carried across
    d.line(P(-112, 0), P(-104, 0)); d.line(P(-112, 356), P(-104, 356))
    d.line(P(-108, 0), P(-108, 356))
    sec_x, sec_y, k = 304, Y0 + bridge_y * s, 0.88    # section: center x, rib mid-height on the cut, px per mm
    d.line((sec_x, sec_y - 52), (sec_x, sec_y + 46))

    d.group()
    d.line(*(left + right))
    # the f-holes: an upper and a lower eye joined by a stem, and the notches that set the bridge
    for sx in (-1, 1):
        up, lo = P(sx * 26, 162), P(sx * 40, 228)
        d.circle(up[0], up[1], 2.0)
        d.circle(lo[0], lo[1], 2.6)
        c1, c2 = P(sx * 22, 182), P(sx * 46, 206)
        d.curve(f'M{up[0]:.1f} {up[1] + 2:.1f} C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {lo[0]:.1f} {lo[1] - 2.6:.1f}')
        n0, n1 = P(sx * 30, bridge_y), P(sx * 27, bridge_y)
        d.line(n0, n1)
    d.line(P(-21, bridge_y - 2), P(21, bridge_y - 2), P(21, bridge_y + 2), P(-21, bridge_y + 2), closed=True)

    d.group('mid')
    d.dashed(P(-18, 60), P(-18, 330), dash=3, gap=2.5)                # bass bar, under the top
    sp = P(19, bridge_y + 6)
    d.circle(sp[0], sp[1], 2.2)                                      # soundpost, seen from above

    # the section at the bridge
    W = 92.0                            # half-width of the body there, mm
    rib = 30.0
    def arch(x, A):                     # a smooth arch falling to a flat edge
        u = min(1.0, abs(x) / (W - 4))
        return A * (1 - u * u) ** 1.6
    xs = [-W + i * (2 * W) / 60 for i in range(61)]
    top_out = [(sec_x + x * k, sec_y - (rib / 2 + arch(x, 15.5)) * k) for x in xs]
    top_in = [(sec_x + x * k, sec_y - (rib / 2 + arch(x, 15.5) - 3.2) * k) for x in xs[3:-3]]
    back_out = [(sec_x + x * k, sec_y + (rib / 2 + arch(x, 14.5)) * k) for x in xs]
    back_in = [(sec_x + x * k, sec_y + (rib / 2 + arch(x, 14.5) - 3.5) * k) for x in xs[3:-3]]
    d.group()
    d.line(*top_out); d.line(*back_out)
    d.line(*top_in); d.line(*back_in)
    for sx in (-1, 1):                  # the ribs
        x = sec_x + sx * W * k
        d.line((x, sec_y - (rib / 2) * k), (x, sec_y + (rib / 2) * k))
        d.line((x - sx * 1.5, sec_y - (rib / 2) * k), (x - sx * 1.5, sec_y + (rib / 2) * k))
    # bridge: two feet on the top, 41 mm apart, about 33 mm tall, the strings on its curved crown
    def top_at(x):
        return sec_y - (rib / 2 + arch(x, 15.5)) * k
    fl, fr = -20.5, 20.5
    crown = [(sec_x + x * k, top_at(0) - 33 * k + (x / 17) ** 2 * 3) for x in [-17 + i * 34 / 16 for i in range(17)]]
    d.line((sec_x + fl * k, top_at(fl)), (sec_x - 17 * k, crown[0][1]))
    d.line(*crown)
    d.line((sec_x + fr * k, top_at(fr)), (sec_x + 17 * k, crown[-1][1]))
    d.group('mid')
    for i in range(4):
        x = -12.75 + i * 8.5
        d.circle(sec_x + x * k, top_at(0) - 33 * k + (x / 17) ** 2 * 3 - 1.6, 1.2)
    # bass bar under the bass foot, soundpost just inside the treble foot
    bb = fl
    y0 = sec_y - (rib / 2 + arch(bb, 15.5) - 3.2) * k
    d.line((sec_x + (bb - 2.5) * k, y0), (sec_x + (bb - 2.5) * k, y0 + 9 * k),
           (sec_x + (bb + 2.5) * k, y0 + 9 * k), (sec_x + (bb + 2.5) * k, y0))
    spx = fr + 2
    ya = sec_y - (rib / 2 + arch(spx, 15.5) - 3.2) * k
    yb = sec_y + (rib / 2 + arch(spx, 14.5) - 3.5) * k
    d.line((sec_x + (spx - 3) * k, ya), (sec_x + (spx - 3) * k, yb))
    d.line((sec_x + (spx + 3) * k, ya), (sec_x + (spx + 3) * k, yb))

    d.group('thin')
    d.line((sec_x - 44, sec_y + 38), (sec_x + fl * k, y0 + 9 * k + 1))
    d.line((sec_x + 44, sec_y + 38), (sec_x + spx * k, sec_y))
    d.line((sec_x + W * k + 2, sec_y - 26), (sec_x + W * k, sec_y - 8))
    d.group('mid')
    d.text(P(-108, 0)[0] - 3, Y0 + 180 * s, '356 MM', size=7, anchor='end')
    d.text(X0, 288, 'THE TOP IN PLAN', size=7)
    d.text(sec_x, 288, 'CUT ACROSS AT THE BRIDGE', size=7)
    d.text(sec_x, sec_y - 62, 'BRIDGE', size=7)
    d.text(sec_x - 54, sec_y - 32, 'TOP · SPRUCE', size=7, anchor='end')
    d.text(sec_x, sec_y + 62, 'BACK · MAPLE', size=7)
    d.text(sec_x - 44, sec_y + 46, 'BASS BAR', size=7)
    d.text(sec_x + 44, sec_y + 46, 'SOUNDPOST', size=7)
    d.text(sec_x + W * k - 4, sec_y - 30, 'RIB', size=7, anchor='start')
    d.text(X0 + 46, Y0 + 238 * s, 'F-HOLE', size=7, anchor='start')
    return d


PLATES = {
    'monteverdi-orfeo': monteverdi_orfeo,
    'cremona-violins': cremona_violins,
}
