"""Plates for Sound and Score's part modern1 (sprint 058): twelve-tone, electric-guitar. See plates_for.py."""
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


NAMES = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']
ROW = [4, 5, 7, 1, 6, 3, 8, 2, 11, 0, 9, 10]          # Op. 25: E F G D♭ G♭ E♭ A♭ D B C A B♭


def twelve_tone():
    d = D()
    # The 12 x 12 matrix of the Suite's row: the top row is the prime P0, the left column its
    # inversion I0, and each row below is P0 transposed to start on that column's note, so the
    # columns read down are the inversions. Rows read right to left are retrogrades, columns read
    # up retrograde inversions. P0 ends on B-flat, a tritone from its first note, so P6 is the
    # bottom row and I6 the right column: the eight forms the Suite uses lie round the border.
    inv = [(2 * ROW[0] - p) % 12 for p in ROW]
    cell = 17
    x0, y0 = 98, 38
    n = 12
    W = cell * n
    d.group('thin')
    d.lines([[(x0 + i * cell, y0), (x0 + i * cell, y0 + W)] for i in range(1, n)])
    d.lines([[(x0, y0 + i * cell), (x0 + W, y0 + i * cell)] for i in range(1, n)])
    d.group()
    _box(d, x0, y0, W, W)
    d.group('mid')
    _box(d, x0 + 1.5, y0 + 1.5, W - 3, cell - 3)                      # P0 / R0
    _box(d, x0 + 1.5, y0 + W - cell + 1.5, W - 3, cell - 3)           # P6 / R6
    _box(d, x0 + 1.5, y0 + 1.5, cell - 3, W - 3)                      # I0 / RI0
    _box(d, x0 + W - cell + 1.5, y0 + 1.5, cell - 3, W - 3)           # I6 / RI6
    # direction arrows outside the border
    ya, yb = y0 + cell / 2, y0 + W - cell / 2
    for y in (ya, yb):
        d.line((x0 - 34, y), (x0 - 6, y)); _arrow(d, (x0 - 34, y), (x0 - 6, y), 4)
        d.line((x0 + W + 34, y), (x0 + W + 6, y)); _arrow(d, (x0 + W + 34, y), (x0 + W + 6, y), 4)
    xa, xb = x0 + cell / 2, x0 + W - cell / 2
    for x in (xa, xb):
        d.line((x, y0 - 22), (x, y0 - 5)); _arrow(d, (x, y0 - 22), (x, y0 - 5), 4)
        d.line((x, y0 + W + 22), (x, y0 + W + 5)); _arrow(d, (x, y0 + W + 22), (x, y0 + W + 5), 4)
    d.group('mid')
    for i in range(n):
        for j in range(n):
            pc = (ROW[j] + inv[i] - ROW[0]) % 12
            d.text(x0 + j * cell + cell / 2, y0 + i * cell + cell / 2 + 2.5, NAMES[pc], size=7)
    d.text(x0 - 38, ya + 2.5, 'P0', size=7, anchor='end')
    d.text(x0 - 38, yb + 2.5, 'P6', size=7, anchor='end')
    d.text(x0 + W + 38, ya + 2.5, 'R0', size=7, anchor='start')
    d.text(x0 + W + 38, yb + 2.5, 'R6', size=7, anchor='start')
    d.text(xa, y0 - 26, 'I0', size=7)
    d.text(xb, y0 - 26, 'I6', size=7)
    d.text(xa, y0 + W + 31, 'RI0', size=7)
    d.text(xb, y0 + W + 31, 'RI6', size=7)
    d.text(200, 292, 'OP. 25 ROW · 12 TRANSPOSITIONS × 4 FORMS · THE SUITE USES THE BORDER', size=7)
    return d


def electric_guitar():
    d = D()
    # Left: a single-coil pickup in section across one string, which is seen end-on. The pole
    # piece is the magnet; its field is drawn as a dipole's lines (r = k sin^2 theta about the
    # magnet's centre), clipped where they would pass through the magnet. Right: the ideal
    # signal, schematic: a plucked string's decaying displacement (dashed) and the coil's voltage,
    # which follows the rate of change of flux and so the string's velocity (solid, its
    # derivative). Real pickups add distortion of their own (Horton and Moore 2009).
    cx, cy = 100, 172                 # magnet centre
    top, bot = 132, 212               # pole piece ends
    sy = 118                          # string centre, just above the pole
    d.group('thin')
    # field lines, both sides
    segs = []
    for k in (44, 60, 76, 90):
        for side in (1, -1):
            seg = []
            for i in range(1, 180):
                th = math.radians(i)
                r = k * math.sin(th) ** 2
                x = cx + side * r * math.sin(th)
                y = cy - r * math.cos(th)
                if abs(x - cx) < 7 and top - 1 < y < bot + 1:
                    if len(seg) > 1:
                        segs.append(seg)
                    seg = []
                    continue
                seg.append((x, y))
            if len(seg) > 1:
                segs.append(seg)
    d.lines(segs)
    d.line((cx, 84), (cx, 250))                                     # axis
    d.line((40, sy), (160, sy))                                     # string's rest line
    d.group()
    _box(d, cx - 6, top, 12, bot - top)                             # pole piece (magnet)
    d.line((cx - 36, top + 8), (cx + 36, top + 8))                  # bobbin flanges
    d.line((cx - 36, bot - 4), (cx + 36, bot - 4))
    _box(d, cx - 32, top + 10, 24, bot - top - 16)                  # coil, either side
    _box(d, cx + 8, top + 10, 24, bot - top - 16)
    d.circle(cx, sy, 3.2)                                           # the string, end-on
    d.group('mid')
    for side in (-1, 1):                                            # windings
        x1, x2 = (cx - 32, cx - 8) if side < 0 else (cx + 8, cx + 32)
        d.lines([[(x1, y), (x2, y)] for y in range(top + 14, bot - 6, 5)])
    for dy in (-8, 8):
        d.dashed(*[(cx + 3.2 * math.cos(math.radians(a)), sy + dy + 3.2 * math.sin(math.radians(a))) for a in range(0, 361, 20)], dash=1.5, gap=1.5)
    d.line((cx + 14, sy - 12), (cx + 14, sy + 8))
    _arrow(d, (cx + 14, sy), (cx + 14, sy - 12), 4); _arrow(d, (cx + 14, sy), (cx + 14, sy + 8), 4)
    d.line((cx - 32, bot + 12), (cx - 32, bot + 26), (cx - 50, bot + 26))   # leads to the jack
    d.line((cx + 32, bot + 12), (cx + 32, bot + 30), (cx - 50, bot + 30))

    # the graph
    gx0, gx1, gy = 214, 388, 150
    amp = 44
    d.group('thin')
    d.line((gx0, gy), (gx1, gy))
    d.line((gx0, gy - amp - 12), (gx0, gy + amp + 12))
    _arrow(d, (gx1 - 10, gy), (gx1, gy), 4)
    d.group('mid')
    T = 52.0                                                        # one period, in units
    tau = 120.0                                                     # decay
    xs = [gx0 + i * 0.5 for i in range(int((gx1 - 8 - gx0) / 0.5))]
    disp = [(x, gy - amp * math.exp(-(x - gx0) / tau) * math.cos(2 * math.pi * (x - gx0) / T)) for x in xs]
    d.dashed(*disp, dash=3, gap=2.5)
    d.group()
    w = 2 * math.pi / T
    def vel(t):                                                     # d/dt of exp(-t/tau) cos(wt)
        e = math.exp(-t / tau)
        return -e * (w * math.sin(w * t) + math.cos(w * t) / tau)
    peak = max(abs(vel(x - gx0)) for x in xs)
    d.line(*[(x, gy - amp * 0.9 * vel(x - gx0) / peak) for x in xs])
    d.group('mid')
    d.text(cx - 10, sy - 12, 'STRING, END-ON', size=7, anchor='end')
    d.text(cx + 22, sy - 6, 'VIBRATES', size=7, anchor='start')
    d.text(cx - 44, top + 4, 'COIL', size=7, anchor='end')
    d.text(cx + 40, bot + 14, 'MAGNET POLE', size=7, anchor='start')
    d.text(cx - 54, bot + 31, 'TO AMP', size=7, anchor='end')
    d.text(gx0 + 4, gy - amp - 16, 'STRING POSITION (DASHED)', size=7, anchor='start')
    d.text(gx0 + 4, gy + amp + 22, 'COIL VOLTAGE (SOLID)', size=7, anchor='start')
    d.text(gx1, gy + 30, 'TIME', size=7, anchor='end')
    d.text(200, 292, 'SINGLE-COIL PICKUP · VOLTAGE FOLLOWS THE CHANGE IN FLUX', size=7)
    return d


PLATES = {
    'twelve-tone': twelve_tone,
    'electric-guitar': electric_guitar,
}
