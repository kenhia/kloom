"""Plates for the mathematics subject's part greeks2 (sprint 024): Apollonius,
Diophantus and the Nine Chapters."""
import math
from plates import D


def diophantus():
    """Arithmetica II.8: the circle x² + y² = 16 cut by lines through (0, −4).

    Diophantus's own line, y = 2x − 4, meets the circle at (16/5, 12/5); every
    other rational slope gives another rational point. Beside it, the square
    of 16 divided into the squares 256/25 and 144/25, to the same scale.
    """
    d = D()
    u = 22                                  # pixels to one unit
    ox, oy, r = 112, 150, 4
    P = lambda x, y: (ox + u * x, oy - u * y)
    def meet(k):                            # the second point of y = kx − 4 on the circle
        x = 8 * k / (k * k + 1)
        return x, k * x - 4
    others = [0.5, 1.5, 3, 4]
    d.group('thin')
    d.line(P(-5.2, 0), P(5.2, 0))
    d.line(P(0, -5.2), P(0, 5.2))
    # the other rational lines through (0, −4), each to its point and a little past it
    segs = []
    for k in others:
        x, y = meet(k)
        segs.append([P(0, -4), P(x * 1.12, k * x * 1.12 - 4)])
    d.lines(segs)
    d.group()
    d.circle(ox, oy, u * r)
    d.group()
    x0, y0 = meet(2)
    d.line(P(-0.35, -4.7), P(x0 * 1.18, 2 * x0 * 1.18 - 4))
    d.group('mid')
    # the right triangle the point makes: legs 16/5 and 12/5, hypotenuse 4
    d.line(P(0, 0), P(x0, y0), P(x0, 0))
    s = 0.22
    d.line(P(x0 - s, 0), P(x0 - s, s), P(x0, s))
    # the other points, small ticks across the circle
    ticks = []
    for k in others:
        x, y = meet(k)
        a = math.atan2(y, x)
        ticks.append([P(3.8 * math.cos(a), 3.8 * math.sin(a)), P(4.2 * math.cos(a), 4.2 * math.sin(a))])
    d.lines(ticks)
    d.circle(*P(x0, y0), 2.6)
    d.circle(*P(0, -4), 2.6)
    # the square of 16 and its two parts, side by side at one scale
    q, base = 11, 200
    sides = [4, 16 / 5, 12 / 5]
    xs = [236, 236 + q * 4 + 18, 236 + q * 4 + 18 + q * 16 / 5 + 18]
    d.group()
    for x, a in zip(xs, sides):
        d.line((x, base), (x + q * a, base), (x + q * a, base - q * a), (x, base - q * a), closed=True)
    d.group('mid')
    # a unit grid inside the whole square, to count 16 by
    d.lines([[(xs[0] + q * i, base), (xs[0] + q * i, base - q * 4)] for i in range(1, 4)] +
            [[(xs[0], base - q * i), (xs[0] + q * 4, base - q * i)] for i in range(1, 4)])
    d.group('mid')
    d.text(xs[0] + q * 2, base + 14, '16')
    d.text(xs[1] - 9, base - 18, '=')
    d.text(xs[1] + q * 8 / 5, base + 14, '256/25', size=8)
    d.text(xs[2] - 9, base - 12, '+')
    d.text(xs[2] + q * 6 / 5, base + 14, '144/25', size=8)
    bx, by = P(x0, y0)
    d.text(bx + 8, by - 8, '(16/5, 12/5)', size=8, anchor='start')
    cx, cy = P(0, -4)
    d.text(cx + 8, cy + 12, '(0, −4)', size=8, anchor='start')
    d.text(ox - u * 4 - 4, 30, 'x² + y² = 16', size=8, anchor='start')
    d.text(xs[0], 272, 'ARITHMETICA II.8', size=7, anchor='start')
    return d


def _view(p, phi=math.radians(-50), el=math.radians(14)):
    """Project a point (x, y, z), z up, turned by phi about the axis and seen from el above."""
    x, y, z = p
    x, y = x * math.cos(phi) - y * math.sin(phi), x * math.sin(phi) + y * math.cos(phi)
    # y is now depth; tilt the view down by el
    z2 = z * math.cos(el) + y * math.sin(el)
    return x, z2


def apollonius_conics():
    """One double cone, three times, each cut by a plane perpendicular to the
    plane through its axis: less steep than a side (the ellipse), parallel to a
    side (the parabola), steeper than a side (the hyperbola, on both nappes).
    The curves are computed where each plane z = m·x + c meets the cone
    x² + y² = (z·tan α)²."""
    d = D()
    alpha = math.radians(27)
    t = math.tan(alpha)
    H, s = 1.0, 74                       # half-height of the double cone, pixels per unit
    gen = 1 / t                          # the slope of a side in the axial plane
    cases = [('ELLIPSE', 0.55 * gen, 0.52), ('PARABOLA', gen, 0.42), ('HYPERBOLA', 3.2 * gen, 0.0)]
    centres = [72, 200, 328]
    cy = 128
    def S(cx, p):
        X, Y = _view(p)
        return cx + s * X, cy - s * Y
    def section(m, c):
        runs, cur = [], []
        for i in range(721):
            th = 2 * math.pi * i / 720
            den = 1 - m * t * math.cos(th)
            z = c / den if abs(den) > 1e-9 else None
            if z is None or abs(z) > H:
                if len(cur) > 1:
                    runs.append(cur)
                cur = []
                continue
            cur.append((z * t * math.cos(th), z * t * math.sin(th), z))
        if len(cur) > 1:
            runs.append(cur)
        return runs
    def hyperbola(m, x0):
        """Both branches where the steep plane z = m(x − x0) meets the double cone."""
        runs = []
        for sign in (1, -1):
            cur = []
            for i in range(401):
                z = sign * H * i / 400
                r = abs(z) * t
                # points of the circle of radius r at height z on the plane x = x0 + z/m
                x = x0 + z / m
                if r * r - x * x < 0:
                    if len(cur) > 1:
                        runs.append(cur)
                    cur = []
                    continue
                y = math.sqrt(r * r - x * x)
                cur.append((x, y, z))
            # mirror in y to complete the branch
            if len(cur) > 1:
                runs.append(list(reversed([(x, -y, z) for x, y, z in cur])) + cur)
        return runs
    d.group('thin')
    for (name, m, c), cx in zip(cases, centres):
        d.line(S(cx, (0, 0, -H - 0.12)), S(cx, (0, 0, H + 0.12)))           # the axis
        # the cutting plane, as a parallelogram
        if name == 'HYPERBOLA':
            x0 = 0.16
            f = lambda y, z: (x0 + z / m, y, z)
        else:
            f = lambda y, z, m=m, c=c: ((z - c) / m, y, z)
        w = 0.72
        zs = {'ELLIPSE': (0.22, 0.95), 'PARABOLA': (0.1, H * 0.98), 'HYPERBOLA': (-H * 0.98, H * 0.98)}[name]
        corners = [f(-w, zs[0]), f(w, zs[0]), f(w, zs[1]), f(-w, zs[1])]
        d.line(*[S(cx, p) for p in corners], closed=True)
    d.group()
    for (name, m, c), cx in zip(cases, centres):
        # the double cone: two rims and the silhouette sides
        n = 90
        for z in (H, -H):
            d.line(*[S(cx, (z * t * math.cos(2 * math.pi * i / n), z * t * math.sin(2 * math.pi * i / n), z)) for i in range(n + 1)])
        segs = []
        for z in (H, -H):
            # silhouette: the generators whose projections bound the drawing
            best = max(range(360), key=lambda k: S(cx, (abs(z) * t * math.cos(math.radians(k)), abs(z) * t * math.sin(math.radians(k)), z))[0])
            worst = min(range(360), key=lambda k: S(cx, (abs(z) * t * math.cos(math.radians(k)), abs(z) * t * math.sin(math.radians(k)), z))[0])
            for k in (best, worst):
                a = math.radians(k)
                segs.append([S(cx, (0, 0, 0)), S(cx, (abs(z) * t * math.cos(a), abs(z) * t * math.sin(a), z))])
        d.lines(segs)
    d.group()
    for (name, m, c), cx in zip(cases, centres):
        runs = hyperbola(m, 0.16) if name == 'HYPERBOLA' else section(m, c)
        d.lines([[S(cx, p) for p in run] for run in runs])
    d.group('mid')
    for (name, m, c), cx in zip(cases, centres):
        d.text(cx, 246, name, size=8)
    d.text(centres[0], 262, 'FALLS SHORT', size=6)
    d.text(centres[1], 262, 'APPLIED EXACTLY', size=6)
    d.text(centres[2], 262, 'EXCEEDS', size=6)
    return d


def _rod_digit(n, x, y, place, w=11, h=16):
    """Segments for one rod numeral, centred on (x, y). Units (place 0) stand upright
    (zong); tens (place 1) lie flat (heng); 6 to 9 put one crossing rod for five."""
    segs = []
    if n == 0:
        return segs
    ones, five = (n - 5, True) if n > 5 else (n, False)
    if place % 2 == 0:
        gap = w / 5
        xs = [x - gap * (ones - 1) / 2 + gap * i for i in range(ones)]
        top = y - h / 2 + (4 if five else 0)
        segs += [[(xx, top), (xx, y + h / 2)] for xx in xs]
        if five:
            segs.append([(x - w / 2, y - h / 2 + 1), (x + w / 2, y - h / 2 + 1)])
    else:
        gap = h / 5
        ys = [y - gap * (ones - 1) / 2 + gap * i + (2 if five else 0) for i in range(ones)]
        segs += [[(x - w / 2, yy), (x + w / 2, yy)] for yy in ys]
        if five:
            segs.append([(x, y - h / 2), (x, y - h / 2 + 5)])
    return segs


def nine_chapters():
    """Chapter 8, problem 1, on a counting board: three columns, one per
    equation, set out right to left, before and after the elimination. The
    numbers are counting-rod numerals, units upright and tens flat."""
    d = D()
    before = [[3, 2, 1, 39], [2, 3, 1, 34], [1, 2, 3, 26]]      # right, middle, left column
    after = [[3, 2, 1, 39], [0, 5, 1, 24], [0, 0, 36, 99]]
    cw, ch = 40, 38
    boards = [(40, before), (236, after)]
    y0 = 62
    d.group('thin')
    for x0, _ in boards:
        d.lines([[(x0 + i * cw, y0), (x0 + i * cw, y0 + 4 * ch)] for i in range(4)] +
                [[(x0, y0 + j * ch), (x0 + 3 * cw, y0 + j * ch)] for j in range(5)])
    # the arrow from one board to the next
    d.group('mid')
    d.line((40 + 3 * cw + 16, y0 + 2 * ch), (236 - 16, y0 + 2 * ch))
    d.line((236 - 24, y0 + 2 * ch - 5), (236 - 16, y0 + 2 * ch), (236 - 24, y0 + 2 * ch + 5))
    for x0, cols in boards:
        d.group()
        segs = []
        for k, col in enumerate(cols):
            cx = x0 + (2 - k) * cw + cw / 2            # the first column stands on the right
            for j, v in enumerate(col):
                cy = y0 + j * ch + ch / 2
                digits = [int(c) for c in str(v)] if v else []
                n = len(digits)
                for i, dgt in enumerate(digits):
                    place = n - 1 - i
                    dx = (i - (n - 1) / 2) * 15
                    segs += _rod_digit(dgt, cx + dx, cy, place)
        d.lines(segs)
    d.group('mid')
    for j, name in enumerate(['TOP', 'MID', 'LOW', 'YIELD']):
        d.text(34, y0 + j * ch + ch / 2 + 3, name, size=7, anchor='end')
    d.text(40 + 1.5 * cw, y0 - 12, 'SET OUT', size=7)
    d.text(236 + 1.5 * cw, y0 - 12, 'ELIMINATED', size=7)
    d.text(40 + 1.5 * cw, y0 + 4 * ch + 20, '3 2 1 = 39, 2 3 1 = 34, 1 2 3 = 26', size=6)
    d.text(236 + 1.5 * cw, y0 + 4 * ch + 20, '36 LOW = 99', size=7)
    d.text(236 + 1.5 * cw, y0 + 4 * ch + 36, 'LOW = 2 3/4', size=7)
    d.text(200, 282, 'NINE CHAPTERS 8.1 · FANGCHENG', size=7)
    return d


PLATES = {
    'apollonius-conics': apollonius_conics,
    'diophantus': diophantus,
    'nine-chapters': nine_chapters,
}
