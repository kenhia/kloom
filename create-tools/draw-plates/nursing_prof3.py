"""Plates for Keeping Watch's part prof3: the end of The modern profession and Today (sprint 030).
See plates_for.py. Helpers copied from nursing_before.py, as the brief asks."""
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


def _dashes(d, p, q, dash=4, gap=3):
    """A dashed line from p to q, as one path of short segments."""
    length = math.dist(p, q)
    ux, uy = (q[0] - p[0]) / length, (q[1] - p[1]) / length
    segs, s = [], 0.0
    while s < length:
        e = min(s + dash, length)
        segs.append([(p[0] + ux * s, p[1] + uy * s), (p[0] + ux * e, p[1] + uy * e)])
        s = e + gap
    d.lines(segs)


def ward_5b():
    d = D()
    # Ward 5B as the infection-control committee's memo of 23 February 1983 asks for it: a double-loaded
    # corridor of twelve private rooms, each with its own sink and toilet (or hopper) and a puncture-proof
    # needle box; a temporary partial barrier across the entry; knee-operated sinks at the entrance and at
    # two places in the hall. A schematic, not a survey: the ward's real plan is not in the sources.
    x0, x1 = 78, 372                        # the rooms' run along the corridor
    cy0, cy1 = 136, 164                     # the corridor's walls
    top, bot = 46, 254                      # the rooms' outer walls
    n = 6
    w = (x1 - x0) / n
    d.group('thin')
    d.line((24, 150), (390, 150))                                       # the corridor's axis
    for k in range(n + 1):                                              # the room module, carried across
        x = x0 + k * w
        d.line((x, top - 10), (x, bot + 10))
    d.line((x0, 30), (x1, 30))                                          # the run, dimensioned
    d.line((x0, 25), (x0, 35))
    d.line((x1, 25), (x1, 35))
    d.group()
    # the outer walls and the corridor walls, with a door gap into each room
    _box(d, x0, top, x1 - x0, bot - top)
    door = 12
    for wall_y in (cy0, cy1):
        segs = []
        for k in range(n):
            xa = x0 + k * w + w - door - 6
            segs.append([(x0 + k * w, wall_y), (xa, wall_y)])
            segs.append([(xa + door, wall_y), (x0 + (k + 1) * w, wall_y)])
        d.lines(segs)
    for k in range(1, n):                                               # the party walls
        x = x0 + k * w
        d.line((x, top), (x, cy0))
        d.line((x, cy1), (x, bot))
    # the entry hall and the nurses' station
    d.line((24, cy0), (x0, cy0))
    d.line((24, cy1), (x0, cy1))
    d.line((x0, top), (x0, cy0))
    d.line((x0, cy1), (x0, bot))
    _box(d, 30, 90, 40, 34)                                             # the station, off the entry
    d.line((50, 124), (50, cy0))
    d.group('mid')
    # in each room: a bed along the party wall, a toilet in the back corner, a sink by the door,
    # and a sharps box by the bed
    for k in range(n):
        xl = x0 + k * w
        for up in (True, False):
            if up:
                yb, yw = top + 8, top
                bed = (xl + 6, top + 10, 16, 30)
                wc = (xl + w - 18, top + 2, 15, 15)
                sink = (xl + w - 12, cy0 - 8)
                sharps = (xl + 24, top + 14, 6, 6)
            else:
                bed = (xl + 6, bot - 40, 16, 30)
                wc = (xl + w - 18, bot - 17, 15, 15)
                sink = (xl + w - 12, cy1 + 8)
                sharps = (xl + 24, bot - 20, 6, 6)
            _box(d, *bed)
            d.line((bed[0] + 2, bed[1] + (4 if up else bed[3] - 4)), (bed[0] + bed[2] - 2, bed[1] + (4 if up else bed[3] - 4)))
            _box(d, *wc)
            d.circle(wc[0] + wc[2] / 2, wc[1] + wc[3] / 2, 4)
            d.circle(*sink, 3)
            _box(d, *sharps)
    d.group()
    # the temporary barrier across the entry, and the knee-operated sinks
    _dashes(d, (40, cy0 + 2), (40, cy1 - 2), dash=3, gap=2)
    for x, y in ((32, cy0 + 5), (32, cy1 - 5), (x0 + 2 * w, cy0 + 5), (x0 + 4 * w, cy1 - 5)):
        d.circle(x, y, 2.6)
    _arrow(d, (8, 150), (26, 150))
    d.group('mid')
    d.text((x0 + x1) / 2, 21, '12 PRIVATE ROOMS', size=7)
    d.text(50, 84, 'STATION', size=7)
    d.text(36, 182, 'BARRIER', size=7)
    d.text(36, 191, '+ SINKS', size=7)
    d.text((x0 + x1) / 2, 275, 'SINK · TOILET · NEEDLE BOX IN EACH ROOM', size=7)
    d.text((x0 + x1) / 2, 286, 'A SCHEMATIC, FROM THE 1983 MEMO', size=7)
    return d


def magnet():
    d = D()
    # A hospital's nursing service as the Medicare rules and the Magnet program describe it, laid out on
    # a grid of levels: the governing body with the chief nursing officer sitting on it; under the CNO,
    # directors; under each, nurse managers answering round the clock for a unit; under each manager a
    # unit's registered nurses, one of whom is charge nurse on each shift. Spans are fanned on their
    # construction rays.
    levels = [44, 104, 164, 226]
    d.group('thin')
    for y in levels:                                                    # the levels
        d.line((20, y), (380, y))
    board = (200, levels[0])
    cno = (200, levels[1])
    dirs = [(104, levels[2]), (200, levels[2]), (296, levels[2])]
    mgrs = []
    for i, (dx, dy) in enumerate(dirs):
        for j in (-1, 1):
            mgrs.append((dx + j * 26, levels[3]))
    for p in dirs:                                                      # the spans, as rays
        d.line(cno, p)
    for i, m in enumerate(mgrs):
        d.line(dirs[i // 2], m)
    d.group()
    _box(d, board[0] - 70, board[1] - 14, 140, 28)                      # the governing body
    for k in range(5):                                                  # its seats, the CNO's among them
        d.circle(board[0] - 48 + 24 * k, board[1], 6)
    d.line((board[0], board[1] + 6), (cno[0], cno[1] - 13))
    _box(d, cno[0] - 26, cno[1] - 13, 52, 26)
    for p in dirs:
        _box(d, p[0] - 20, p[1] - 11, 40, 22)
    for m in mgrs:
        d.circle(m[0], m[1], 9)
    d.group('mid')
    # each unit's nurses, in a row under its manager, the charge nurse ringed
    for m in mgrs:
        xs = [m[0] - 12 + 8 * k for k in range(4)]
        for k, x in enumerate(xs):
            d.circle(x, m[1] + 30, 3)
            d.line((m[0], m[1] + 9), (x, m[1] + 27))
        d.circle(xs[0], m[1] + 30, 5.5)
    d.group('mid')
    d.text(board[0], board[1] - 20, 'GOVERNING BODY', size=7)
    d.text(cno[0] + 38, cno[1] + 3, 'CNO', size=7, anchor='start')
    d.text(dirs[0][0] - 26, dirs[0][1] + 3, 'DIRECTORS', size=7, anchor='end')
    d.text(mgrs[0][0] - 14, levels[3] + 3, 'MANAGERS', size=7, anchor='end')
    d.text(mgrs[-1][0] + 26, levels[3] + 33, 'NURSES', size=7, anchor='start')
    d.text(200, 286, 'A NURSING SERVICE · UNITS ROUND THE CLOCK', size=7)
    return d


# UPC-A, the symbol that carries a ten-digit National Drug Code with the number-system digit 3.
_L = ['0001101', '0011001', '0010011', '0111101', '0100011',
      '0110001', '0101111', '0111011', '0110111', '0001011']


def _upc_modules(digits):
    """The 95 modules of a UPC-A symbol for eleven digits, with the check digit appended."""
    odd = sum(digits[0::2])
    even = sum(digits[1::2])
    check = (10 - (3 * odd + even) % 10) % 10
    ds = digits + [check]
    bits = '101'
    bits += ''.join(_L[x] for x in ds[:6])
    bits += '01010'
    bits += ''.join(''.join('1' if c == '0' else '0' for c in _L[x]) for x in ds[6:])
    bits += '101'
    return bits, ds


def bcma():
    d = D()
    # A UPC-A bar code of the kind the FDA's 2004 rule put on drug labels, encoding an invented number in
    # the National Drug Code's form (number system 3, then ten digits), its modules computed from the
    # symbology: start, six left digits in odd parity, center, six right digits, end. A scanner above
    # reads it along its beam; below, the wristband the nurse scans first, on a computed loop.
    digits = [3, 9, 9, 9, 9, 9, 1, 2, 3, 4, 5]
    bits, ds = _upc_modules(digits)
    m = 2.6                                                             # one module, in plate units
    x0 = 200 - 95 * m / 2
    ytop, ybar, ylong = 92, 156, 166
    guards = set(range(0, 3)) | set(range(45, 50)) | set(range(92, 95))
    d.group('thin')
    for edge in [0, 3] + [3 + 7 * i for i in range(1, 7)] + [50 + 7 * i for i in range(0, 7)] + [95]:
        x = x0 + edge * m                                               # digit boundaries
        d.line((x, ytop - 8), (x, ylong + 4))
    d.line((x0 - 12, (ytop + ybar) / 2), (x0 + 95 * m + 12, (ytop + ybar) / 2))   # the scan line
    sx, sy = 200, 34                                                    # the scanner's window
    for t in (0.0, 0.25, 0.5, 0.75, 1.0):                               # its beam fanned across the code
        d.line((sx, sy + 12), (x0 + t * 95 * m, (ytop + ybar) / 2))
    d.group()
    segs = []
    for k, b in enumerate(bits):
        if b == '1':
            x = x0 + (k + 0.5) * m
            segs.append([(x, ytop), (x, ylong if k in guards else ybar)])
    d.lines(segs)
    # the scanner head above
    d.line((sx - 22, sy - 14), (sx + 22, sy - 14), (sx + 14, sy + 12), (sx - 14, sy + 12), closed=True)
    d.line((sx - 8, sy - 14), (sx - 8, sy - 26), (sx + 8, sy - 26), (sx + 8, sy - 14))
    d.group('mid')
    # the wristband below: a strip seen curving round a wrist, two elliptical edges, its own short code
    # and a snap
    wx, wy, wr, wry = 200, 242, 150, 26
    d.arc(wx, wy, wr, 200, 340, n=60, ry=wry)
    d.arc(wx, wy + 16, wr, 200, 340, n=60, ry=wry)
    ticks = []
    for k in range(18):
        a = math.radians(238 + k * 3.6)
        x, y = wx + wr * math.cos(a), wy + 8 + wry * math.sin(a)
        ticks.append([(x, y - 3), (x, y + (3 if k % 3 else 5))])
    d.lines(ticks)
    a = math.radians(322)
    d.circle(wx + wr * math.cos(a), wy + 8 + wry * math.sin(a), 3)
    d.group('mid')
    for i, x in enumerate(ds):                                          # the human-readable digits
        if i == 0:
            xx = x0 - 8
        elif i == 11:
            xx = x0 + 95 * m + 8
        elif i < 6:
            xx = x0 + (3 + 7 * i + 3.5) * m
        else:
            xx = x0 + (50 + 7 * (i - 6) + 3.5) * m
        d.text(xx, ybar + 12, str(x), size=7)
    d.text(x0 - 6, ytop - 12, 'START', size=7, anchor='start')
    d.text(200, ytop - 12, 'CENTER', size=7)
    d.text(x0 + 95 * m + 6, ytop - 12, 'CHECK', size=7, anchor='end')
    d.text(200, 196, 'AN INVENTED NUMBER IN THE NDC FORM', size=7)
    d.text(200, 280, 'THE WRISTBAND, SCANNED FIRST', size=7)
    return d


def where_nursing_is():
    d = D()
    # Left: a day as two shifts on a 24-hour dial, its hours ticked. Right: one registered nurse and the
    # most patients a medical-surgical unit may give her under California's rule, five, set on a circle
    # 72 degrees apart, each bed on its ray from the nurse.
    cx, cy, R = 104, 150, 76
    nx, ny, r = 286, 150, 74
    d.group('thin')
    d.circle(cx, cy, R + 8)
    for h in range(24):                                                 # the hours
        a = h * 15 - 90
        d.line(_pt(cx, cy, R, a), _pt(cx, cy, R + 8 if h % 6 else R + 14, a))
    d.circle(nx, ny, r)
    beds = [_pt(nx, ny, r, -90 + 72 * k) for k in range(5)]
    for b in beds:                                                      # the rays to each bed
        d.line((nx, ny), b)
    d.group()
    d.arc(cx, cy, R - 10, -90 + 7 * 15 + 3, -90 + 19 * 15 - 3, n=48)    # the day shift, 07 to 19
    d.arc(cx, cy, R - 10, -90 + 19 * 15 + 3, -90 + 31 * 15 - 3, n=48)   # the night shift, 19 to 07
    d.circle(cx, cy, 3)
    d.line(_pt(cx, cy, R - 18, -90 + 7 * 15), _pt(cx, cy, R + 2, -90 + 7 * 15))      # the changes of shift
    d.line(_pt(cx, cy, R - 18, -90 + 19 * 15), _pt(cx, cy, R + 2, -90 + 19 * 15))
    d.circle(nx, ny, 9)                                                 # the nurse
    for k, b in enumerate(beds):                                        # five beds, head to the ring
        a = -90 + 72 * k
        ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
        vx, vy = -uy, ux
        hw, hl = 8, 14
        c = (b[0] + ux * 6, b[1] + uy * 6)
        corners = [(c[0] + sx * vx * hw + sl * ux * hl, c[1] + sx * vy * hw + sl * uy * hl)
                   for sx, sl in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        d.line(*corners, closed=True)
    d.group('mid')
    for k, b in enumerate(beds):                                        # each bed's pillow
        a = -90 + 72 * k
        ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
        vx, vy = -uy, ux
        c = (b[0] + ux * 16, b[1] + uy * 16)
        d.line((c[0] - vx * 5, c[1] - vy * 5), (c[0] + vx * 5, c[1] + vy * 5))
    d.group('mid')
    d.text(cx, cy - R - 20, '24 HOURS', size=7)
    d.text(cx, cy + 34, 'DAY', size=7)
    d.text(cx, cy - 26, 'NIGHT', size=7)
    d.text(nx, ny + r + 34, '1 NURSE : 5 PATIENTS', size=7)
    return d


PLATES = {
    'ward-5b': ward_5b,
    'magnet': magnet,
    'bcma': bcma,
    'where-nursing-is': where_nursing_is,
}
