"""Plates for the mathematics subject's Analysis segment, part two (sprint 024):
gradient descent and chaos."""
import math
from plates import D


def gradient_descent():
    """Descent on the bowl f(x, y) = x² + 4y² from (4, 1), with a step of 0.2 and of 0.3."""
    d = D()
    ox, oy, s = 196, 146, 38            # the minimum, and pixels per unit
    P = lambda x, y: (ox + s * x, oy - s * y)
    def path(theta, n):
        x, y, pts = 4.0, 1.0, []
        for _ in range(n + 1):
            pts.append((x, y))
            x, y = x - theta * 2 * x, y - theta * 8 * y
        return pts
    good, bad = path(0.2, 8), path(0.3, 3)
    d.group('thin')
    # the axes through the minimum, and the level curves f = 1, 4, 9, 16, 20 (the start's)
    d.line(P(-4.3, 0), P(4.6, 0))
    d.line(P(0, -3.0), P(0, 3.3))
    for c in (1, 4, 9, 16, 20):
        a, b = math.sqrt(c), math.sqrt(c) / 2
        d.line(*[P(a * math.cos(t * math.pi / 60), b * math.sin(t * math.pi / 60)) for t in range(121)])
    d.group()
    # the step of 0.2 zig-zags down the valley to the bottom
    d.line(*[P(x, y) for x, y in good])
    d.group('mid')
    # the step of 0.3 overshoots the valley further each time
    d.line(*[P(x, y) for x, y in bad])
    for x, y in good[:5] + bad[1:]:
        px, py = P(x, y)
        d.circle(px, py, 2)
    # the gradient at the start, (8, 8), drawn a quarter as long; the step goes the other way
    sx, sy = P(4, 1)
    gx, gy = P(4 + 8 * 0.07, 1 + 8 * 0.07)
    d.line((sx, sy), (gx, gy))
    d.line((gx - 7, gy + 1), (gx, gy), (gx - 1, gy + 7))
    d.group('mid')
    mx, my = P(0, 0)
    d.text(sx + 10, sy + 14, '(4, 1)', size=7, anchor='start')
    d.text(gx - 6, gy - 2, '∇f', size=8, anchor='end')
    d.text(P(1.6, -1.4)[0] + 8, P(1.6, -1.4)[1] + 4, 'θ = 0.3', size=7, anchor='start')
    d.text(P(2.4, -0.6)[0] + 8, P(2.4, -0.6)[1] + 12, 'θ = 0.2', size=7, anchor='start')
    d.text(mx - 6, my + 12, 'MIN', size=7, anchor='end')
    d.text(16, 22, 'f(x, y) = x² + 4y²', size=8, anchor='start')
    return d


def lorenz(x, y, z, n, dt=0.01, sigma=10.0, r=28.0, b=8.0 / 3.0):
    """n fourth-order Runge–Kutta steps of Lorenz's 1963 equations, from (x, y, z)."""
    def f(x, y, z):
        return sigma * (y - x), r * x - y - x * z, x * y - b * z
    out = [(x, y, z)]
    for _ in range(n):
        k1 = f(x, y, z)
        k2 = f(x + dt / 2 * k1[0], y + dt / 2 * k1[1], z + dt / 2 * k1[2])
        k3 = f(x + dt / 2 * k2[0], y + dt / 2 * k2[1], z + dt / 2 * k2[2])
        k4 = f(x + dt * k3[0], y + dt * k3[1], z + dt * k3[2])
        x += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        z += dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        out.append((x, y, z))
    return out


def chaos():
    """The Lorenz attractor (σ = 10, r = 28, b = 8/3) seen on the X–Z plane, and below it
    X against time for two runs whose starts differ by 0.00001."""
    d = D()
    cx, zb, sx, sz = 200, 200, 4.8, 3.6      # the attractor: X across, Z up
    A = lambda x, z: (cx + sx * x, zb - sz * z)
    run = lorenz(1.0, 1.0, 20.0, 5000)[2500::2]  # a stretch well past the start
    t0, tx, ty, ts, ys = 20, 12, 252, 360 / 25, 1.2   # the strip: t from 0 to 25
    a = lorenz(1.0, 1.0, 20.0, 2500)
    b = lorenz(1.00001, 1.0, 20.0, 2500)
    T = lambda i, x: (t0 + ts * i * 0.01, ty - ys * x)
    c = 6 * math.sqrt(2)
    d.group('thin')
    # axes of the attractor, the level of the two steady states, and the strip's time axis
    d.line(A(-24, 0), A(24, 0))
    d.line(A(0, 0), A(0, 52))
    d.line(A(-c - 6, 27), A(c + 6, 27))
    d.line((t0, ty), (t0 + ts * 25, ty))
    d.line((t0, ty - 26), (t0, ty + 26))
    for k in range(0, 26, 5):
        x = t0 + ts * k
        d.line((x, ty - 3), (x, ty + 3))
    d.group()
    d.line(*[A(x, z) for x, y, z in run])
    d.group('mid')
    # the two states of steady convection, C and C′, round which the path winds
    for sgn in (1, -1):
        px, py = A(sgn * c, 27)
        d.lines([[(px - 4, py), (px + 4, py)], [(px, py - 4), (px, py + 4)]])
    d.group('mid')
    d.line(*[T(3 * i, p[0]) for i, p in enumerate(a[::3])])
    d.group()
    d.line(*[T(3 * i, p[0]) for i, p in enumerate(b[::3])])
    d.group('mid')
    px, py = A(c, 27)
    d.text(px + 7, py - 5, 'C', size=7, anchor='start')
    px, py = A(-c, 27)
    d.text(px - 7, py - 5, "C′", size=7, anchor='end')
    d.text(A(24, 0)[0] + 4, A(24, 0)[1] + 3, 'X', size=7, anchor='start')
    d.text(A(0, 52)[0], A(0, 52)[1] - 5, 'Z', size=7)
    d.text(t0 + ts * 25 + 4, ty + 3, 't', size=7, anchor='start')
    for k in (0, 5, 10, 15, 20, 25):
        d.text(t0 + ts * k, ty + 34, str(k), size=6)
    d.text(392, 20, 'σ = 10  r = 28  b = 8/3', size=7, anchor='end')
    return d


PLATES = {
    'gradient-descent': gradient_descent,
    'chaos': chaos,
}
