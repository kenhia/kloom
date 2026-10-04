"""Plates for western-civ's Rebirth frames (sprint 049, part reb1): humanism,
renaissance-painting, machiavelli. See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def _dashed(d, p, q, dash=4, gap=3):
    """A dashed line as short segments, in one path (the plates have no stroke-dasharray)."""
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    segs, t = [], 0.0
    while t < L:
        e = min(t + dash, L)
        segs.append([(p[0] + ux * t, p[1] + uy * t), (p[0] + ux * e, p[1] + uy * e)])
        t = e + gap
    d.lines(segs)


def humanism():
    """The stemma of Lucretius's De rerum natura, as Wikipedia's article gives it (after
    Butterfield): a lost archetype; O copied from it in the early ninth century; Q and S from a
    lost Psi, itself from a damaged state of the archetype; and Poggio's lost manuscript of 1417,
    whose place in the tree is left open, copied by Niccoli (Laur. 35.30), the model of more than
    fifty fifteenth-century copies and of the first printed edition, Brescia 1473.
    Surviving manuscripts are drawn as books, lost ones as circles, as a stemma marks them."""
    d = D()
    d.group('thin')
    _dashed(d, (120, 29), (290, 120))                                    # Poggio's copy: place unknown
    for y in (24, 74, 120, 180):                                         # the generations of copying
        d.line((24, y), (36, y))
    d.line((30, 24), (30, 180))

    d.group()
    lost = {'Ω': (110, 24), 'ΩI': (180, 74), 'Ψ': (180, 120), 'π': (300, 124)}
    for x, y in lost.values():
        d.circle(x, y, 10)
    books = {'O': (60, 140), 'Q': (150, 180), 'S': (210, 180), 'L': (300, 196)}
    for x, y in books.values():                                          # a codex, in elevation
        _box(d, x - 11, y - 14, 22, 28)
        d.line((x - 8, y - 14), (x - 8, y + 14))

    d.group('mid')
    def edge(a, b):
        d.line(a, b)
        _arrow(d, a, b, 4)
    ox, oy = lost['Ω']
    edge((ox - 6, oy + 8), (books['O'][0] + 4, books['O'][1] - 16))
    edge((ox + 9, oy + 5), (lost['ΩI'][0] - 9, lost['ΩI'][1] - 4))
    edge((180, 84), (180, 108))
    edge((175, 129), (books['Q'][0] + 4, books['Q'][1] - 16))
    edge((185, 129), (books['S'][0] - 4, books['S'][1] - 16))
    edge((300, 134), (300, 180))
    # Niccoli's copy fans out into the fifteenth-century copies, then the press
    fan = []
    for i in range(13):
        a = math.radians(-60 + 120 * i / 12)
        fan.append([(300 + 16 * math.sin(a), 212 + 4 * math.cos(a)), (300 + 62 * math.sin(a), 236 + 6 * math.cos(a))])
    d.lines(fan)
    _box(d, 284, 254, 32, 18)                                            # the printed book, 1473
    d.line((300, 244), (300, 254))

    d.group('mid')
    for k, (x, y) in lost.items():
        d.text(x, y + 3, k, size=8)
    for k, (x, y) in books.items():
        d.text(x + 2, y + 3, k, size=8)
    d.text(306, 116, '?', size=8, anchor='start')
    d.text(180, 208, 'IX C.', size=7)
    d.text(60, 166, 'C. 825', size=7)
    d.text(342, 128, 'POGGIO 1417', size=7)
    d.text(345, 200, 'NICCOLI', size=7)
    d.text(338, 225, '50+', size=7, anchor='start')
    d.text(300, 284, 'BRESCIA 1473', size=7)
    d.text(110, 284, 'DE RERUM NATURA', size=7)
    return d


def renaissance_painting():
    """Alberti's construction (De pictura I, Leoni's English of 1755). The window's ground line is
    divided into braccia; the centric point stands as high as a man, three braccia; orthogonals run
    from each division to it. The transversals come from the side figure: the eye at the same height,
    at a chosen distance (here three braccia) from the picture, rays to the same divisions, cut by
    the perpendicular that stands for the picture. Height above the ground line of the n-th
    transversal: h = H * n*u / (D + n*u). The proof is the diagonal through the tiles' corners; it
    meets the horizon at the distance point, D from the centric point."""
    d = D()
    x0, x1, g = 20, 240, 250                                             # the window's ground line
    n = 6
    u = (x1 - x0) / n                                                    # one braccio
    H = 3 * u                                                            # a man: three braccia
    Dd = 3 * u                                                           # the viewing distance
    cx, cy = (x0 + x1) / 2, g - H                                        # the centric point
    top = 40

    def trans(k):                                                        # the k-th transversal's y
        return g - H * k * u / (Dd + k * u)

    def orth_x(xk, y):                                                   # an orthogonal at height y
        return xk + (cx - xk) * (g - y) / H

    # the side figure, at half scale
    s = 0.5
    sx0, sg = 262, 250
    ex, ey = sx0, sg - H * s                                             # the eye
    pp = sx0 + Dd * s                                                    # the picture, edge on
    floor = [pp + k * u * s for k in range(0, 5)]

    d.group('thin')
    for k in range(n + 1):                                               # orthogonals to the centric point
        xk = x0 + k * u
        d.line((xk, g), (cx, cy))
    d.line((x0, cy), (x1, cy))                                           # the horizon, a man high
    d.line((ex, ey), (pp + 4 * u * s + 6, ey))
    for fx in floor[1:]:
        d.line((ex, ey), (fx, sg))                                       # rays from the eye

    d.group()
    _box(d, x0, top, x1 - x0, g - top)                                   # the window
    k = 1
    while k <= 10:                                                       # the pavement's first ten transversals
        y = trans(k)
        d.line((orth_x(x0, y), y), (orth_x(x1, y), y))
        k += 1
    d.line((sx0 - 4, sg), (floor[-1] + 6, sg))                           # the side figure's ground
    d.line((pp, sg), (pp, sg - H * s - 14))                              # the perpendicular: the picture
    d.line((ex, sg), (ex, ey))                                           # the man who sees

    d.group('mid')
    d.line((x0, g), (x1, cy))                                            # the proof: one diagonal
    d.circle(cx, cy, 2.5)
    d.circle(x1, cy, 2.5)
    for k in range(1, 5):                                                # the cuts give the heights
        hy = sg - H * s * k * u / (Dd + k * u)
        d.line((pp - 4, hy), (pp + 4, hy))
    for k in range(n + 1):                                               # the braccia, ticked
        d.line((x0 + k * u, g), (x0 + k * u, g + 5))
    for fx in floor:
        d.line((fx, sg), (fx, sg + 4))
    d.circle(ex, ey, 2.5)

    d.group('mid')
    d.text(cx, cy - 6, 'CENTRIC POINT', size=7)
    d.text(x1 - 4, cy - 8, 'DISTANCE', size=7, anchor='end')
    d.text(cx, g + 16, 'GROUND LINE · 6 BRACCIA', size=7)
    d.text(cx, top - 6, 'THE WINDOW', size=7)
    d.text(ex - 2, ey - 8, 'EYE', size=7, anchor='start')
    d.text(pp + 2, sg - H * s - 18, 'PICTURE', size=7)
    d.text(330, sg + 16, 'SIDE · 1/2', size=7)
    return d


def machiavelli():
    """Chapter I of The Prince as a tree (Marriott's English): states are republics or
    principalities; principalities hereditary or new; new ones wholly new or annexed; and
    acquired by one's own arms or others', by fortune or by ability (virtù). Below, chapter XXV's
    balance: Fortune the arbiter of one-half of our actions, leaving our free will the other half."""
    d = D()
    nodes = {
        'states': (200, 26, 'STATES'),
        'rep': (110, 72, 'REPUBLICS'),
        'pri': (290, 72, 'PRINCIPALITIES'),
        'her': (215, 118, 'HEREDITARY'),
        'new': (345, 118, 'NEW'),
        'whol': (290, 164, 'WHOLLY NEW'),
        'mix': (372, 164, 'MIXED'),
    }
    widths = {'states': 56, 'rep': 66, 'pri': 92, 'her': 70, 'new': 36, 'whol': 70, 'mix': 46}
    edges = [('states', 'rep'), ('states', 'pri'), ('pri', 'her'), ('pri', 'new'), ('new', 'whol'), ('new', 'mix')]

    d.group('thin')
    for y in (26, 72, 118, 164):                                         # the levels of division
        d.line((14, y), (30, y))
    d.line((22, 26), (22, 164))
    # the balance's construction: the beam's level and the fulcrum's axis
    bx, by = 200, 236
    d.line((60, by), (340, by))
    d.line((bx, 196), (bx, 286))

    d.group()
    for k, (x, y, _) in nodes.items():
        w = widths[k]
        _box(d, x - w / 2, y - 9, w, 18)
    # the balance: beam, fulcrum, two pans
    half = 120
    d.line((bx - half, by), (bx + half, by))
    d.line((bx, by), (bx - 10, by + 22), (bx + 10, by + 22), closed=True)
    for sgn in (-1, 1):
        px = bx + sgn * half
        d.line((px, by), (px - 22, by + 22))
        d.line((px, by), (px + 22, by + 22))
        d.arc(px, by + 22, 22, 0, 180, n=24, ry=8)

    d.group('mid')
    for a, b in edges:
        ax_, ay_, _ = nodes[a]
        bx_, by_, _ = nodes[b]
        p, q = (ax_, ay_ + 9), (bx_, by_ - 9)
        d.line(p, q)
        _arrow(d, p, q, 4)

    d.group('mid')
    for k, (x, y, s_) in nodes.items():
        d.text(x, y + 3, s_, size=7)
    d.text(331, 188, "BY OWN ARMS OR OTHERS'", size=7)
    d.text(bx - half, by + 44, 'FORTUNA', size=7)
    d.text(bx + half, by + 44, 'FREE WILL', size=7)
    d.text(bx - half, by - 8, '1/2', size=7)
    d.text(bx + half, by - 8, '1/2', size=7)
    d.text(110, 118, 'CH. I', size=7)
    d.text(bx, 206, 'CH. XXV', size=7)
    return d


PLATES = {
    'humanism': humanism,
    'renaissance-painting': renaissance_painting,
    'machiavelli': machiavelli,
}
