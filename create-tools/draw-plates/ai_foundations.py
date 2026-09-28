"""ai plates, segment "Foundations" (sprint 006). See ai.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=5):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def analytical_engine():
    """Plan of the 1838 engine: the mill's ring of axes, the long store, and the chain of cards."""
    d = D()
    mx, my, pr = 108, 188, 72  # the mill: centre and pitch circle of its ring of axes
    axes = [(mx + pr * math.cos(2 * math.pi * i / 12), my + pr * math.sin(2 * math.pi * i / 12)) for i in range(12)]
    store_y, x0, x1 = 188, 196, 384
    cols = [x0 + 12 + i * 22 for i in range(9)]
    # construction: centre lines, the pitch circle, radii to each axis, the store's rack line
    d.group('thin')
    d.line((mx - 96, my), (x1 + 6, my))
    d.line((mx, my - 96), (mx, my + 96))
    d.circle(mx, my, pr)
    d.lines([[(mx, my), p] for p in axes])
    d.lines([[(x, store_y - 34), (x, store_y + 34)] for x in cols])
    # the object: the central wheel, the axes round it, the store's two rows of figure-wheel columns
    d.group()
    d.circle(mx, my, 30)
    d.lines([[(mx + 30 * math.cos(math.radians(a)), my + 30 * math.sin(math.radians(a))),
              (mx + 36 * math.cos(math.radians(a)), my + 36 * math.sin(math.radians(a)))]
             for a in range(0, 360, 15)])
    for x, y in axes:
        d.circle(x, y, 9)
    d.line((x0, store_y - 8), (x1, store_y - 8))
    d.line((x0, store_y + 8), (x1, store_y + 8))
    for x in cols:
        d.circle(x, store_y - 22, 8)
        d.circle(x, store_y + 22, 8)
    # detail: the chain of operation cards, laced together, each with its row of holes
    d.group('mid')
    cw, ch, cy = 30, 20, 34
    patterns = [0b1011, 0b0110, 0b1101, 0b0011, 0b1110, 0b0101, 0b1001]
    for i, bits in enumerate(patterns):
        cx = 150 + i * 34
        d.line((cx, cy), (cx + cw, cy), (cx + cw, cy + ch), (cx, cy + ch), closed=True)
        for k in range(4):
            if bits >> (3 - k) & 1:
                d.circle(cx + 6 + k * 6, cy + ch / 2, 1.6)
        if i:
            d.line((cx - 4, cy + 4), (cx, cy + 4))
            d.line((cx - 4, cy + ch - 4), (cx, cy + ch - 4))
    # the chain turns down over its prism into the mill's card reader
    d.group('mid')
    d.line((150, cy + ch / 2), (126, cy + ch / 2), (mx, my - pr - 16))
    _arrow(d, mx, my - pr - 16, math.atan2(my - pr - 16 - (cy + ch / 2), mx - 126))
    d.group()
    d.text(mx, my + pr + 26, 'MILL', size=8)
    d.text((x0 + x1) / 2, store_y + 48, 'STORE · 1,000 × 40 DIGITS', size=8)
    d.text(270, cy + ch + 16, 'OPERATION CARDS', size=8)
    return d


def laws_of_thought():
    """x² = x: the parabola and the line meet only at 0 and 1; beside it, Shannon's two ways to join switches."""
    d = D()
    ox, oy, u = 44, 236, 150  # origin and unit length of the graph
    P = lambda x, y: (ox + u * x, oy - u * y)
    d.group('thin')
    d.lines([[P(i / 4, -0.12), P(i / 4, 1.2)] for i in range(-1, 6) if i != 0])
    d.lines([[P(-0.25, j / 4), P(1.3, j / 4)] for j in range(1, 5)])
    d.line(P(1, 0), P(1, 1), P(0, 1))
    d.group()
    d.line(P(-0.25, 0), P(1.35, 0))
    d.line(P(0, -0.12), P(0, 1.3))
    _arrow(d, *P(1.35, 0), 0)
    _arrow(d, *P(0, 1.3), -math.pi / 2)
    d.group()
    xs = [-0.2 + 1.3 * i / 60 for i in range(61)]
    d.line(*[P(x, x * x) for x in xs if x * x <= 1.26])
    d.line(P(-0.12, -0.12), P(1.22, 1.22))
    d.group('mid')
    d.circle(*P(0, 0), 5)
    d.circle(*P(1, 1), 5)
    # Shannon: two contacts in series (both must close) and in parallel (either may)
    sx, sy = 238, 72

    def contact(x, y):
        d.circle(x, y, 2.5)
        d.circle(x + 26, y, 2.5)
        d.line((x + 2.5, y), (x + 24, y - 11))

    py = sy + 150
    d.group('thin')
    d.line((sx, sy - 24), (sx, py + 34))
    d.line((sx + 140, sy - 24), (sx + 140, py + 34))
    d.group()
    d.line((sx, sy), (sx + 20, sy))
    contact(sx + 20, sy)
    d.line((sx + 48, sy), (sx + 68, sy))
    contact(sx + 68, sy)
    d.line((sx + 96, sy), (sx + 140, sy))
    d.line((sx, py), (sx + 30, py), (sx + 30, py - 22), (sx + 44, py - 22))
    contact(sx + 44, py - 22)
    d.line((sx + 72, py - 22), (sx + 90, py - 22), (sx + 90, py + 22), (sx + 72, py + 22))
    d.line((sx + 30, py), (sx + 30, py + 22), (sx + 44, py + 22))
    contact(sx + 44, py + 22)
    d.line((sx + 90, py), (sx + 140, py))
    d.group()
    d.text(P(0, 0)[0] - 10, P(0, 0)[1] + 16, '0', size=9)
    d.text(P(1, 0)[0], P(1, 0)[1] + 15, '1', size=9)
    d.text(P(0.62, 1.1)[0], P(0.62, 1.1)[1], 'x² = x', size=10)
    d.text(sx + 70, sy + 26, 'SERIES · x AND y', size=8)
    d.text(sx + 70, py + 48, 'PARALLEL · x OR y', size=8)
    return d


def turing_machine():
    """Turing's first machine: a tape of squares, the scanned square, and the four m-configurations it cycles through."""
    d = D()
    ty, h, w = 206, 26, 26
    xs = [8 + i * w for i in range(15)]
    scanned = 8
    symbols = {1: '0', 3: '1', 5: '0', 7: '1'}  # figures on alternate squares, as the machine leaves them
    d.group('thin')
    d.line((0, ty), (400, ty))
    d.line((0, ty + h), (400, ty + h))
    d.line((xs[scanned] + w / 2, ty - 60), (xs[scanned] + w / 2, ty + h + 30))
    cx, cy, r = 200, 88, 54
    d.circle(cx, cy, r)
    d.line((cx - r - 14, cy), (cx + r + 14, cy))
    d.line((cx, cy - r - 14), (cx, cy + r + 14))
    d.group()
    d.lines([[(x, ty), (x, ty + h)] for x in xs + [xs[-1] + w]])
    d.line((xs[0], ty), (xs[-1] + w, ty))
    d.line((xs[0], ty + h), (xs[-1] + w, ty + h))
    # the head, over the scanned square
    hx = xs[scanned] + w / 2
    d.line((hx - 16, ty - 40), (hx + 16, ty - 40), (hx + 16, ty - 16), (hx, ty - 6), (hx - 16, ty - 16), closed=True)
    # the four m-configurations on a circle, each joined to the next
    d.group('mid')
    names = ['b', 'c', 'e', 'f']
    angs = [-90, 0, 90, 180]
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in angs]
    for x, y in pts:
        d.circle(x, y, 11)
    for i in range(4):
        a0, a1 = angs[i] + 14, angs[i] + 76
        d.arc(cx, cy, r, a0, a1, n=24)
        end = math.radians(a1)
        ex, ey = cx + r * math.cos(end), cy + r * math.sin(end)
        _arrow(d, ex, ey, end + math.pi / 2)
    d.lines([[(x + 6, ty + h + 8), (x + w - 6, ty + h + 8)] for x in xs[scanned + 1:scanned + 4]])
    d.group()
    for (x, y), n in zip(pts, names):
        d.text(x, y + 3, n, size=9)
    for i, s in symbols.items():
        d.text(xs[i] + w / 2, ty + h / 2 + 4, s, size=10)
    d.text(hx, ty - 25, 'f', size=8)
    d.text(cx, 16, 'P0,R · R · P1,R · R', size=8)
    d.text(xs[scanned + 2] + w / 2, ty + h + 22, 'R', size=8)
    return d


def mcculloch_pitts():
    """Three threshold neurons as AND, OR and NOT: excitatory endings as arrowheads, the inhibitory as a ring."""
    d = D()
    ny, rr = 156, 20
    xs = [70, 200, 330]
    d.group('thin')
    d.line((20, ny), (380, ny))
    for x in xs:
        d.line((x, 40), (x, 262))
    d.lines([[(20, y), (380, y)] for y in (64, 240)])
    d.group()
    for x in xs:
        d.circle(x, ny, rr)
        d.line((x, ny + rr), (x, 240))
        _arrow(d, x, 240, math.pi / 2, 6)
    d.group('mid')
    # AND and OR: two excitatory fibres; NOT: one inhibitory fibre (and a constant clock of zero threshold)
    for x in xs[:2]:
        for sgn in (-1, 1):
            sx, sy = x + sgn * 34, 64
            ang = math.atan2(ny - rr - sy, x + sgn * 8 - sx)
            ex, ey = x + sgn * 8 - 6 * math.cos(ang), ny - rr - 2 - 6 * math.sin(ang)
            d.line((sx, sy), (ex, ey))
            _arrow(d, ex, ey, ang, 6)
    x = xs[2]
    d.line((x, 64), (x, ny - rr - 10))
    d.circle(x, ny - rr - 6, 4)
    d.group()
    labels = [('AND', 'θ = 2'), ('OR', 'θ = 1'), ('NOT', 'θ = 0')]
    for x, (g, t) in zip(xs, labels):
        d.text(x, ny + 4, t, size=8)
        d.text(x, 282, g, size=9)
    d.text(xs[0] - 34, 56, 'x', size=8)
    d.text(xs[0] + 34, 56, 'y', size=8)
    d.text(xs[1] - 34, 56, 'x', size=8)
    d.text(xs[1] + 34, 56, 'y', size=8)
    d.text(xs[2], 56, 'x', size=8)
    d.text(390, 60, 't', size=8, anchor='end')
    d.text(390, 236, 't+1', size=8, anchor='end')
    return d


def turing_test():
    """The imitation game in plan: the interrogator's room, two hidden rooms, the teleprinter lines, five minutes."""
    d = D()
    C = (24, 92, 140, 212)
    A = (262, 28, 380, 128)
    B = (262, 176, 380, 276)

    def room(r):
        x0, y0, x1, y1 = r
        d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)

    d.group('thin')
    d.line((200, 10), (200, 290))
    d.lines([[(10, y), (390, y)] for y in (78, 152, 226)])
    d.group()
    for r in (C, A, B):
        room(r)
    # teleprinters: one at each end of each line
    d.group('mid')
    tps = [(112, 128), (112, 176), (276, 78), (276, 226)]
    for x, y in tps:
        d.line((x - 10, y - 7), (x + 10, y - 7), (x + 10, y + 7), (x - 10, y + 7), closed=True)
        d.line((x - 6, y - 7), (x - 6, y - 12), (x + 6, y - 12), (x + 6, y - 7))
    d.line((122, 128), (200, 128), (200, 78), (266, 78))
    d.line((122, 176), (200, 176), (200, 226), (266, 226))
    # the clock: five minutes of questioning, a twelfth of the dial
    kx, ky, kr = 58, 46, 24
    d.group('thin')
    d.lines([[(kx + kr * math.cos(math.radians(a)), ky + kr * math.sin(math.radians(a))),
              (kx + (kr - 4) * math.cos(math.radians(a)), ky + (kr - 4) * math.sin(math.radians(a)))]
             for a in range(0, 360, 30)])
    d.group()
    d.circle(kx, ky, kr)
    d.line((kx, ky), (kx, ky - kr + 5))
    d.line((kx, ky), (kx + (kr - 5) * math.cos(math.radians(-60)), ky + (kr - 5) * math.sin(math.radians(-60))))
    d.arc(kx, ky, kr + 5, -90, -60, n=12)
    d.group()
    d.text(58, 196, 'C', size=11)
    d.text(330, 112, 'A', size=11)
    d.text(330, 260, 'B', size=11)
    d.text(228, 72, 'X', size=9)
    d.text(228, 244, 'Y', size=9)
    d.text(kx + 34, ky + 4, '5 MIN', size=8, anchor='start')
    d.text(321, 58, 'MACHINE', size=8)
    d.text(321, 206, 'HUMAN', size=8)
    return d


PLATES = {
    'analytical-engine': analytical_engine,
    'laws-of-thought': laws_of_thought,
    'turing-machine': turing_machine,
    'mcculloch-pitts': mcculloch_pitts,
    'turing-test': turing_test,
}
