"""Plates for Keeping Watch's trail Nightingale's numbers, its first three frames (sprint 030,
part numbers1): farr, notes-on-hospitals, hospital-statistics. See plates_for.py."""
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


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


# The Registrar-General's rates, deaths a year per 1,000 men, in Nightingale's evidence to the Royal
# Commission (1857; Notes on Hospitals, 1859, p. 36): Englishmen and soldiers at home, by age.
CIVIL = [(20, 8.4), (25, 9.2), (30, 10.2), (35, 11.6)]
SOLDIER = [(20, 17.0), (25, 18.3), (30, 18.4), (35, 19.2)]


def _survivors(rates):
    """Survivors of 1,000 men at 20, year by year to 40, each age band's rate held for five years."""
    out, n = [(20, 1000.0)], 1000.0
    for a0, m in rates:
        for k in range(1, 6):
            n *= 1 - m / 1000
            out.append((a0 + k, n))
    return out


def farr():
    d = D()
    # A life table's construction: a thousand men of twenty followed to forty at the 1857 rates, the
    # survivors of each year carried into the next. Age runs across (13 px a year), survivors down
    # from 1,000 (0.55 px a man). The upper curve is Englishmen, the lower soldiers at home, marked
    # with a tick each year; their ends, 820 and 692, are the reading's arithmetic.
    x0, y0, px_yr, px_man = 66, 34, 13, 0.55

    def P(age, n):
        return x0 + (age - 20) * px_yr, y0 + (1000 - n) * px_man

    civ, sol = _survivors(CIVIL), _survivors(SOLDIER)
    d.group('thin')
    for age in range(20, 41, 5):                                      # the five-year bands
        d.line(P(age, 1000), P(age, 600))
    for n in range(1000, 599, -100):                                  # survivors, by the hundred
        d.line(P(20, n), P(40, n))
    d.line(P(40, civ[-1][1]), P(42.5, civ[-1][1]))                    # leaders to the end values
    d.line(P(40, sol[-1][1]), P(42.5, sol[-1][1]))
    d.group()
    d.line(P(20, 1000), P(20, 600), P(40, 600))                       # the axes
    d.line(*[P(a, n) for a, n in civ])
    d.line(*[P(a, n) for a, n in sol])
    d.group('mid')
    for a, n in sol[1:]:                                              # the soldiers' curve, ticked yearly
        x, y = P(a, n)
        d.line((x, y - 3), (x, y + 3))
    for a, n in civ[1:]:                                              # the civilians', dotted yearly
        x, y = P(a, n)
        d.circle(x, y, 1.2)
    for age in range(20, 41, 5):                                      # ticks on the age axis
        x, y = P(age, 600)
        d.line((x, y), (x, y + 4))
    for n in range(1000, 599, -100):
        x, y = P(20, n)
        d.line((x - 4, y), (x, y))
    d.group('mid')
    for age in range(20, 41, 5):
        x, y = P(age, 600)
        d.text(x, y + 14, str(age), size=7)
    for n in range(1000, 599, -100):
        x, y = P(20, n)
        d.text(x - 8, y + 2.5, f'{n:,}', size=7, anchor='end')
    d.text(P(30, 600)[0], P(30, 600)[1] + 27, 'AGE', size=7)
    cx, cy = P(42.6, civ[-1][1])
    d.text(cx + 2, cy + 2.5, f'{round(civ[-1][1])}', size=7, anchor='start')
    sx, sy = P(42.6, sol[-1][1])
    d.text(sx + 2, sy + 2.5, f'{round(sol[-1][1])}', size=7, anchor='start')
    ex, ey = P(30, dict(civ)[30])
    d.text(ex + 4, ey - 9, 'ENGLISHMEN', size=7, anchor='start')
    sx, sy = P(31, dict(sol)[31])
    d.text(sx - 2, sy + 25, 'SOLDIERS AT HOME', size=7, anchor='end')
    return d


def notes_on_hospitals():
    d = D()
    # Nightingale's model ward for twenty beds (Notes on Hospitals, 3rd ed., 1863, pp. 65-67), drawn
    # to scale at 3.6 px a foot: 80 by 25 feet in plan, 16 feet high in section. A window at least
    # 4 ft 8 in wide to every two beds, the pair of beds flanking it, ten beds to a side; windows face
    # each other across the ward, so the air crosses it (the thin lines). Beds 3 ft by 6 ft 3 in,
    # set 9 in off the wall, which leaves 11 ft between the feet of opposite beds.
    s = 3.6
    L, W, H = 80, 25, 16
    x0, y0 = 200 - L * s / 2, 34
    win, bed_w, bed_l, off = 4 + 8 / 12, 3, 6.25, 0.75
    centres = [8 + 16 * k for k in range(5)]                            # windows every 16 ft

    def X(ft):
        return x0 + ft * s

    def Y(ft):
        return y0 + ft * s

    d.group('thin')
    d.line((X(-3), Y(W / 2)), (X(L + 3), Y(W / 2)))                    # the ward's axis
    for c in centres:                                                   # air across, window to window
        d.line((X(c), Y(-4)), (X(c), Y(W + 4)))
    d.line((X(0), Y(W + 5)), (X(0), Y(W + 9)))                          # length, dimensioned
    d.line((X(L), Y(W + 5)), (X(L), Y(W + 9)))
    d.line((X(0), Y(W + 7)), (X(L), Y(W + 7)))
    d.line((X(L + 5), Y(0)), (X(L + 9), Y(0)))                          # width, dimensioned
    d.line((X(L + 5), Y(W)), (X(L + 9), Y(W)))
    d.line((X(L + 7), Y(0)), (X(L + 7), Y(W)))
    d.group()
    t = 1.5                                                             # wall thickness, feet
    edges = [-t] + [e for c in centres for e in (c - win / 2, c + win / 2)] + [L + t]
    for y, yo in ((0, -t), (W, W + t)):                                 # the long walls, broken by windows
        for a, b in zip(edges[::2], edges[1::2]):
            d.line((X(max(a, 0) if a > -t else 0), Y(y)), (X(min(b, L)), Y(y)))
            d.line((X(a), Y(yo)), (X(b), Y(yo)))
        for c in centres:                                               # the window's reveals
            for e in (c - win / 2, c + win / 2):
                d.line((X(e), Y(y)), (X(e), Y(yo)))
    for x, xo in ((0, -t), (L, L + t)):                                 # the end walls
        d.line((X(x), Y(0)), (X(x), Y(W)))
        d.line((X(xo), Y(-t)), (X(xo), Y(W + t)))
    for c in centres:                                                   # two beds at each window
        for side in (-1, 1):
            bx = c + side * (win / 2 + 0.6 + bed_w / 2)
            for y, sgn in ((0, 1), (W, -1)):
                top = y + sgn * off
                yy = (top, top + sgn * bed_l)
                d.line((X(bx - bed_w / 2), Y(yy[0])), (X(bx + bed_w / 2), Y(yy[0])),
                       (X(bx + bed_w / 2), Y(yy[1])), (X(bx - bed_w / 2), Y(yy[1])), closed=True)
    d.group('mid')
    for c in centres:                                                   # the glazing, in the wall's middle
        for y in (-t / 2, W + t / 2):
            d.line((X(c - win / 2), Y(y)), (X(c + win / 2), Y(y)))
    for c in centres:                                                   # the pillow ends
        for side in (-1, 1):
            bx = c + side * (win / 2 + 0.6 + bed_w / 2)
            for y, sgn in ((0, 1), (W, -1)):
                py = y + sgn * (off + 1.2)
                d.line((X(bx - bed_w / 2 + 0.4), Y(py)), (X(bx + bed_w / 2 - 0.4), Y(py)))

    # the section across the ward, below: same scale
    sx0, sy0 = 200 - W * s / 2, 262                                     # floor's left end
    def SX(ft):
        return sx0 + ft * s

    def SY(ft):
        return sy0 - ft * s

    d.group('thin')
    for k in range(4):                                                  # the air across the ward
        h = 4 + 3 * k
        d.line((SX(-6), SY(h)), (SX(W + 6), SY(h)))
    d.line((SX(W + 5), SY(0)), (SX(W + 9), SY(0)))                      # height, dimensioned
    d.line((SX(W + 5), SY(H)), (SX(W + 9), SY(H)))
    d.line((SX(W + 7), SY(0)), (SX(W + 7), SY(H)))
    d.group()
    d.line((SX(-2), SY(0)), (SX(W + 2), SY(0)))                         # the floor
    for x, xo in ((0, -1.5), (W, W + 1.5)):                             # walls, with the window opening
        for a, b in ((0, 2.5), (H - 1, H)):
            d.line((SX(x), SY(a)), (SX(x), SY(b)))
            d.line((SX(xo), SY(a)), (SX(xo), SY(b)))
        d.line((SX(x), SY(2.5)), (SX(xo), SY(2.5)))                     # sill and head
        d.line((SX(x), SY(H - 1)), (SX(xo), SY(H - 1)))
    d.line((SX(0), SY(H)), (SX(W), SY(H)))                              # the ceiling
    d.line((SX(-2.5), SY(H)), (SX(W / 2), SY(H + 6)), (SX(W + 2.5), SY(H)))  # the roof
    for x, sgn in ((0, 1), (W, -1)):                                    # a bed against each wall
        a, b = x + sgn * off, x + sgn * (off + bed_l)
        d.line((SX(a), SY(2)), (SX(b), SY(2)))
        d.line((SX(a), SY(0)), (SX(a), SY(3)))
        d.line((SX(b), SY(0)), (SX(b), SY(2)))
    d.group('mid')
    for x in (-0.75, W + 0.75):                                         # the glazing
        d.line((SX(x), SY(2.5)), (SX(x), SY(H - 1)))
    for k in range(4):
        h = 4 + 3 * k
        _arrow(d, (SX(W - 2), SY(h)), (SX(W + 4), SY(h)), size=3.5)
    d.group('mid')
    d.text(X(L / 2), Y(W + 7) + 10, '80 FT · 20 BEDS', size=7)
    d.text(X(L + 7) + 4, Y(W / 2) + 2.5, '25 FT', size=7, anchor='start')
    d.text(SX(W + 7) + 4, SY(H / 2) + 2.5, '16 FT', size=7, anchor='start')
    d.text(SX(-6) - 6, SY(H / 2) + 2.5, '1,600 CU FT A BED', size=7, anchor='end')
    return d


def hospital_statistics():
    d = D()
    # Nightingale's plan of 1860 (Notes on Hospitals, 3rd ed., 1863, pp. 159-63). Left: one ruled form,
    # ages across and diseases down, filled in seven times a year, once for each element. Right: the
    # first six elements balance through the hospital: those remaining on 1 January and those admitted
    # come in; the recovered, the discharged, the dead and those remaining on 31 December go out.
    # The seventh, the mean days in hospital, belongs to the box. Each flow lies on a ray from the
    # box's centre, drawn thin beyond the arrow.
    sw, sh, step = 104, 140, 5
    fx, fy = 22, 120                                                    # the front sheet's corner
    cx, cy, bw, bh = 274, 150, 84, 44                                   # the hospital, as a box
    ins = [(224, 64, '1 · 1 JAN', 'REMAINING'), (324, 64, '2', 'ADMITTED')]
    outs = [(186, 238, '3', 'RECOVERED'), (245, 238, '4', 'DISCHARGED'),
            (304, 238, '5', 'DIED'), (362, 238, '6 · 31 DEC', 'REMAINING')]
    cols, colw = 8, 9.25

    def edge(x, y):
        """Where the ray from the centre to (x, y) leaves the box."""
        dx, dy = x - cx, y - cy
        k = min((bw / 2) / abs(dx) if dx else 9e9, (bh / 2) / abs(dy) if dy else 9e9)
        return cx + dx * k, cy + dy * k

    def toward(p, q, dist):
        """The point `dist` along the line from p toward q."""
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        return p[0] + (q[0] - p[0]) * dist / L, p[1] + (q[1] - p[1]) * dist / L

    d.group('thin')
    for x, y, *_ in ins + outs:                                         # the rays, out to their labels
        d.line(edge(x, y), (x, y))
    d.line((cx - bw / 2 - 16, cy), (cx - bw / 2, cy))                   # the box's axes, outside it
    d.line((cx + bw / 2, cy), (cx + bw / 2 + 16, cy))
    for k in range(1, cols):                                            # the front sheet's columns, ruled
        x = fx + 30 + k * colw
        d.line((x, fy - 4), (x, fy))
        d.line((x, fy + sh), (x, fy + sh + 4))
    d.group()
    for k in range(6, 0, -1):                                           # the six sheets behind: top and right
        x, y = fx + k * step, fy - k * step
        d.line((x, y + step), (x, y), (x + sw, y), (x + sw, y + sh), (x + sw - step, y + sh))
    _box(d, fx, fy, sw, sh)                                             # the front sheet
    _box(d, cx - bw / 2, cy - bh / 2, bw, bh)                           # the hospital
    for x, y, *_ in ins:
        e = edge(x, y)
        a = toward(e, (x, y), 4)
        b = toward(e, (x, y), 62)
        d.line(b, a)
        _arrow(d, b, a)
    for x, y, *_ in outs:
        s = edge(x, y)
        a = toward(s, (x, y), 4)
        b = toward(s, (x, y), math.hypot(x - s[0], y - s[1]) - 14)
        d.line(a, b)
        _arrow(d, a, b)
    d.group('mid')
    d.line((fx, fy + 16), (fx + sw, fy + 16))                           # the age heading
    d.line((fx + 30, fy), (fx + 30, fy + sh))                           # the disease column
    for k in range(1, cols):
        x = fx + 30 + k * colw
        d.line((x, fy), (x, fy + sh))
    for k in range(1, 14):                                              # disease rows
        y = fy + 16 + k * 9
        d.line((fx + 3, y), (fx + 27, y))
    for k in (4, 9):                                                    # orders, ruled across
        y = fy + 16 + k * 9 + 4.5
        d.line((fx, y), (fx + sw, y))
    for r, c in [(1, 0), (1, 3), (2, 5), (3, 2), (5, 6), (6, 1), (7, 3), (10, 4), (11, 0), (12, 7), (13, 2)]:
        x, y = fx + 30 + c * colw + colw / 2, fy + 16 + r * 9 - 4.5     # a few strokes, one a patient
        d.line((x - 2, y + 2.5), (x + 2, y - 2.5))
    d.group('mid')
    d.text(fx + sw / 2 + 15, fy + sh + 18, 'SEVEN SHEETS', size=7)
    d.text(fx + sw / 2 + 15, fy + sh + 28, 'AGES ACROSS · DISEASES DOWN', size=7)
    d.text(cx, cy + 2.5, 'HOSPITAL', size=7)
    d.text(cx, cy + 12, '7 · MEAN DAYS', size=7)
    for x, y, n, w in ins:
        d.text(x, y - 12, n, size=7)
        d.text(x, y - 3, w, size=7)
    for x, y, n, w in outs:
        d.text(x, y + 6, n, size=7)
        d.text(x, y + 15, w, size=7)
    return d

PLATES = {
    'farr': farr,
    'notes-on-hospitals': notes_on_hospitals,
    'hospital-statistics': hospital_statistics,
}
