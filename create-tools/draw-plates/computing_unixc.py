"""computing plates, trail "Unix and C" (sprint 015). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _arrow_line(d, p, q, size=4):
    """A line from p to q with an arrowhead at q."""
    d.line(p, q)
    _arrow(d, q[0], q[1], math.atan2(q[1] - p[1], q[0] - p[0]), size)


def multics():
    """Multics's protection rings: eight concentric rings, a call from ring 4 down through a gate into
    ring 0 and the return, and one segment's access brackets on the ring scale (Schroeder and Saltzer, 1972)."""
    d = D()
    cx, cy, step = 116, 152, 13.5
    R = [step * (k + 1) for k in range(8)]           # outer boundary of ring k
    mid = [step * (k + 0.5) for k in range(8)]       # the middle of ring k
    # construction: the centre lines, and the ray the ring numbers are read along
    d.group('thin')
    d.line((cx - R[-1] - 10, cy), (cx + R[-1] + 10, cy))
    d.line((cx, cy - R[-1] - 10), (cx, cy + R[-1] + 10))
    a = math.radians(-50)
    d.line((cx, cy), (cx + (R[-1] + 16) * math.cos(a), cy + (R[-1] + 16) * math.sin(a)))
    # the rings
    d.group()
    for r in R:
        d.circle(cx, cy, r)
    # the call: from ring 4 inward through a gate into ring 0, and the return outward
    d.group('mid')
    ac, ar = math.radians(188), math.radians(248)
    pc = [(cx + r * math.cos(ac), cy + r * math.sin(ac)) for r in (mid[5], mid[0] + 3)]
    _arrow_line(d, pc[0], pc[1])
    pr = [(cx + r * math.cos(ar), cy + r * math.sin(ar)) for r in (mid[0] + 3, mid[5])]
    _arrow_line(d, pr[0], pr[1])
    # the gate: a notch across ring 0's boundary where the call enters
    g = R[0]
    for da in (-7, 7):
        aa = ac + math.radians(da)
        d.line((cx + (g - 4) * math.cos(aa), cy + (g - 4) * math.sin(aa)),
               (cx + (g + 4) * math.cos(aa), cy + (g + 4) * math.sin(aa)))
    # a segment's brackets on the ring scale: read and write brackets start at ring 0; the execute
    # bracket is one ring, and the gate extension lets rings above it call in
    x0, dx, y0 = 262, 15, 76
    X = lambda k: x0 + dx * k
    d.group('thin')
    d.lines([[(X(k), y0 - 8), (X(k), y0 + 118)] for k in range(9)])
    d.group()
    d.line((X(0), y0), (X(8), y0))
    rows = [('W', 0, 0), ('R', 0, 5), ('E', 0, 0), ('GATE', 1, 5)]
    for i, (_, lo, hi) in enumerate(rows):
        y = y0 + 26 + 24 * i
        d.line((X(lo) + 2, y - 5), (X(hi + 1) - 2, y - 5), (X(hi + 1) - 2, y + 5), (X(lo) + 2, y + 5), closed=True)
    # labels
    d.group()
    for k in range(8):
        d.text(cx + mid[k] * math.cos(a) + 1, cy + mid[k] * math.sin(a) + 3, str(k), size=7)
    d.text(cx, cy + R[-1] + 22, 'RING 0 · SUPERVISOR · RING 4 · USER', size=7)
    d.text(pc[0][0] - 4, pc[0][1] + 3, 'CALL', size=7, anchor='end')
    d.text(pr[1][0] - 4, pr[1][1] - 5, 'RETURN', size=7, anchor='end')
    for k in range(8):
        d.text(X(k) + dx / 2, y0 - 12, str(k), size=7)
    for i, (name, _, _) in enumerate(rows):
        d.text(X(0) - 6, y0 + 29 + 24 * i, name, size=7, anchor='end')
    d.text(X(4), y0 - 24, 'ONE SEGMENT’S BRACKETS', size=7)
    d.text(X(4), y0 + 136, 'CALLS FROM RINGS 1–5', size=7)
    d.text(X(4), y0 + 147, 'ENTER ONLY AT THE GATE', size=7)
    d.text(200, 22, 'MULTICS · EIGHT RINGS OF PROTECTION', size=8)
    return d


def c_language():
    """C's arrays and pointers: two early-Unix directory entries, struct { int inumber; char name[14]; },
    laid out byte by byte in PDP-11 memory, with p pointing at the first and p+1, scaled by the
    struct's size, at the second."""
    d = D()
    x0, w, y, h = 24, 11, 150, 24
    X = lambda b: x0 + w * b
    names = ['unix', 'bin']
    # construction: word boundaries carried up and down, the offsets' projection lines
    d.group('thin')
    d.lines([[(X(b), y - 12), (X(b), y + h + 12)] for b in range(0, 33, 2)])
    d.lines([[(X(b), y + h), (X(b), y + h + 40)] for b in (0, 16, 32)])
    # the memory: 32 bytes in a row
    d.group()
    d.line((X(0), y), (X(32), y), (X(32), y + h), (X(0), y + h), closed=True)
    d.lines([[(X(b), y), (X(b), y + h)] for b in range(1, 32)])
    # the fields: a brace over each inumber and name
    d.group('mid')
    for e in range(2):
        for lo, hi in ((0, 2), (2, 16)):
            a, b = X(16 * e + lo) + 1, X(16 * e + hi) - 1
            m = (a + b) / 2
            d.line((a, y - 4), (a, y - 9), (m - 3, y - 9), (m, y - 13), (m + 3, y - 9), (b, y - 9), (b, y - 4))
    # the pointers: p at the first entry, p+1 sixteen bytes on
    d.group()
    for e, (bx, label_x) in enumerate(((60, X(0)), (228, X(16)))):
        d.line((bx - 18, 54), (bx + 18, 54), (bx + 18, 74), (bx - 18, 74), closed=True)
        _arrow_line(d, (bx, 74), (label_x + 1, y - 24))
    # the size: a dimension line under the first entry
    d.group('mid')
    yy = y + h + 32
    d.line((X(0), yy), (X(16), yy))
    _arrow(d, X(0), yy, math.pi)
    _arrow(d, X(16), yy, 0)
    d.line((X(16), yy), (X(32), yy))
    _arrow(d, X(32), yy, 0)
    # labels
    d.group()
    for e, nm in enumerate(names):
        for i, ch in enumerate(nm):
            d.text(X(16 * e + 2 + i) + w / 2, y + 16, ch, size=8)
        d.text(X(16 * e + 2 + len(nm)) + w / 2, y + 16, '0', size=6)
        d.text(X(16 * e + 1), y + h + 11, 'inum', size=6)
        d.text((X(16 * e + 2) + X(16 * e + 16)) / 2, y - 16, 'name[14]', size=7)
    d.text(60, 67, 'p', size=9)
    d.text(228, 67, 'p+1', size=9)
    for b in (0, 16, 32):
        d.text(X(b), y + h + 52, str(b), size=7)
    d.text(X(8), yy - 5, 'sizeof = 16', size=7)
    d.text(X(24), yy - 5, 'd[1]', size=7)
    d.text(200, 26, 'struct { int inumber; char name[14]; } d[2], *p = d;', size=7)
    d.text(200, 250, 'ONE UNIX DIRECTORY ENTRY: 2 BYTES OF I-NUMBER, 14 OF NAME', size=7)
    d.text(200, 264, 'PDP-11 · 16-BIT WORDS, BYTE ADDRESSES', size=7)
    return d


def pipes():
    """sort input | pr | opr: three processes joined by two pipes, each a kernel buffer that the writer
    fills and the reader drains, with the standard error streams going to the terminal."""
    d = D()
    y, h = 118, 44
    boxes = [(34, 104, 'sort'), (158, 228, 'pr'), (282, 352, 'opr')]
    term_y = 238
    # construction: the stream axis, and the error streams' drops
    d.group('thin')
    d.line((12, y + h / 2), (388, y + h / 2))
    d.lines([[((a + b) / 2, y + h), ((a + b) / 2, term_y)] for a, b, _ in boxes])
    # the processes
    d.group()
    for a, b, _ in boxes:
        d.line((a, y), (b, y), (b, y + h), (a, y + h), closed=True)
    # the pipes: hoses between the boxes, drawn as cylinders
    d.group()
    pipes_x = [(boxes[0][1], boxes[1][0]), (boxes[1][1], boxes[2][0])]
    for a, b in pipes_x:
        d.line((a, y + h / 2 - 7), (b, y + h / 2 - 7))
        d.line((a, y + h / 2 + 7), (b, y + h / 2 + 7))
        d.ellipse(b - 2, y + h / 2, 3, 7)
    # the input file, the terminal
    d.group('mid')
    d.line((12, y + h / 2), (boxes[0][0], y + h / 2))
    _arrow(d, boxes[0][0], y + h / 2, 0)
    d.line((24, term_y), (376, term_y), (376, term_y + 18), (24, term_y + 18), closed=True)
    for a, b, _ in boxes:
        _arrow(d, (a + b) / 2, term_y, math.pi / 2)
    # one pipe's buffer, enlarged: a ring of slots, written at one pointer and read at the other
    d.group('mid')
    bx, by, r0, r1 = (pipes_x[0][0] + pipes_x[0][1]) / 2, 58, 16, 30
    n = 12
    full = 7
    d.circle(bx, by, r0)
    d.circle(bx, by, r1)
    d.lines([[(bx + r0 * math.cos(2 * math.pi * k / n), by + r0 * math.sin(2 * math.pi * k / n)),
              (bx + r1 * math.cos(2 * math.pi * k / n), by + r1 * math.sin(2 * math.pi * k / n))] for k in range(n)])
    # the filled slots, hatched
    hatch = []
    for k in range(full):
        for t in (0.3, 0.55, 0.8):
            ang = 2 * math.pi * (k + t) / n - math.pi / 2
            hatch.append([(bx + (r0 + 3) * math.cos(ang), by + (r0 + 3) * math.sin(ang)),
                          (bx + (r1 - 3) * math.cos(ang), by + (r1 - 3) * math.sin(ang))])
    d.lines(hatch)
    d.group('thin')
    d.line((bx - 10, by + r1), (pipes_x[0][0] + 4, y + h / 2 - 7))
    d.line((bx + 10, by + r1), (pipes_x[0][1] - 4, y + h / 2 - 7))
    d.group()
    for k, ln in ((0, 'R'), (full, 'W')):
        ang = 2 * math.pi * k / n - math.pi / 2
        _arrow_line(d, (bx + (r1 + 14) * math.cos(ang), by + (r1 + 14) * math.sin(ang)),
                    (bx + (r1 + 2) * math.cos(ang), by + (r1 + 2) * math.sin(ang)), 3)
    # labels
    d.group()
    for a, b, name in boxes:
        d.text((a + b) / 2, y + h - 8, name, size=9)
        d.text(a + 6, y + 10, '0', size=6)
        d.text(b - 6, y + 10, '1', size=6)
        d.text((a + b) / 2 + 6, y + h + 12, '2', size=6)
    d.text(6, y + h / 2 - 6, 'input', size=6, anchor='start')
    d.text(200, term_y + 12, 'TERMINAL', size=7)
    ang = 2 * math.pi * full / n - math.pi / 2
    d.text(bx + (r1 + 20) * math.cos(ang) - 2, by + (r1 + 20) * math.sin(ang) + 3, 'WRITE', size=6, anchor='end')
    d.text(bx + 6, by - r1 - 16, 'READ', size=6, anchor='start')
    d.text(300, 50, 'THE KERNEL HOLDS', size=7)
    d.text(300, 61, 'WHAT sort HAS WRITTEN', size=7)
    d.text(300, 72, 'AND pr HAS NOT READ', size=7)
    d.text(200, 206, 'sort input | pr | opr', size=9)
    d.text(200, 284, 'FIRST NOTATION: sort input >pr>opr>', size=7)
    return d


def bsd():
    """The Berkeley sockets calls of 4.2BSD, as two processes' timelines: a server that listens and
    accepts, a client that connects, and the bytes that then pass between two file descriptors."""
    d = D()
    xs, xc, top, bot = 104, 296, 44, 266
    t = {'s_socket': 66, 's_bind': 86, 's_listen': 106, 's_accept': 132, 's_read': 184, 's_write': 208, 's_close': 246,
         'c_socket': 112, 'c_connect': 132, 'c_write': 176, 'c_read': 216, 'c_close': 250}
    # construction: the time grid
    d.group('thin')
    d.lines([[(40, yy), (360, yy)] for yy in range(60, 262, 20)])
    # the two lifelines and their heads
    d.group()
    for x, name in ((xs, 'SERVER'), (xc, 'CLIENT')):
        d.line((x - 36, top - 22), (x + 36, top - 22), (x + 36, top - 4), (x - 36, top - 4), closed=True)
        d.line((x, top - 4), (x, bot))
    # the calls, as ticks on each lifeline
    d.group('mid')
    for k, yy in t.items():
        x = xs if k.startswith('s_') else xc
        d.line((x - 6, yy), (x + 6, yy))
    # the server blocks in accept until the connection arrives: a thick bar
    d.line((xs - 3, t['s_accept']), (xs - 3, 158), (xs + 3, 158), (xs + 3, t['s_accept']), closed=True)
    # the exchanges between them
    d.group()
    _arrow_line(d, (xc - 6, t['c_connect']), (xs + 6, 156))
    _arrow_line(d, (xs + 6, 160), (xc - 6, 164))
    _arrow_line(d, (xc - 6, t['c_write']), (xs + 6, t['s_read']))
    _arrow_line(d, (xs + 6, t['s_write']), (xc - 6, t['c_read']))
    # labels
    d.group()
    d.text(xs, top - 10, 'SERVER', size=8)
    d.text(xc, top - 10, 'CLIENT', size=8)
    for k, yy in t.items():
        name = k.split('_')[1] + '()'
        if k.startswith('s_'):
            d.text(xs - 12, yy + 3, name, size=7, anchor='end')
        else:
            d.text(xc + 12, yy + 3, name, size=7, anchor='start')
    d.text(xs - 12, 146, '(BLOCKS)', size=6, anchor='end')
    d.text(xs - 12, 156, 'NEW FD', size=6, anchor='end')
    d.text(200, 136, 'CONNECT', size=6)
    d.text(200, 176, 'BYTES', size=6)
    d.text(200, 206, 'BYTES', size=6)
    d.text(200, 286, '4.2BSD · 1983 · A CONNECTION IS A FILE DESCRIPTOR', size=7)
    return d


def unix_wars():
    """The Unix family as lanes on a time axis, 1969–1995: Research Unix, Berkeley, AT&T's System V, the
    free BSDs and Linux, with the SVR4 merger, the OSF/UI split and the lawsuit's two years."""
    d = D()
    y0, y1 = 1969, 1996
    xl, xr = 26, 384
    X = lambda yr: xl + (xr - xl) * (yr - y0) / (y1 - y0)
    lanes = {'research': 64, 'bsd': 116, 'sysv': 168, 'free': 208, 'linux': 244}
    axis_y = 270
    # construction: the year grid
    d.group('thin')
    d.lines([[(X(yr), 40), (X(yr), axis_y)] for yr in range(1970, 1996, 5)])
    # the lawsuit, April 1992 to January 1994, as a hatched band
    d.group('thin')
    a, b = X(1992.3), X(1994.05)
    d.line((a, 96), (b, 96), (b, 224), (a, 224), closed=True)
    d.lines([[(a, yy), (min(b, a + (224 - yy)), min(224, yy + (b - a)))] for yy in range(96, 224, 8)])
    # the lanes
    d.group()
    d.line((X(1969), lanes['research']), (X(1989.8), lanes['research']))
    d.line((X(1978.2), lanes['bsd']), (X(1995.5), lanes['bsd']))
    d.line((X(1982), lanes['sysv']), (X(1996), lanes['sysv']))
    d.line((X(1992), lanes['free']), (X(1996), lanes['free']))
    d.line((X(1991.7), lanes['linux']), (X(1996), lanes['linux']))
    # the branchings and mergers
    d.group('mid')
    _arrow_line(d, (X(1975.4), lanes['research']), (X(1978.2), lanes['bsd']))
    _arrow_line(d, (X(1979), lanes['research']), (X(1982), lanes['sysv']))
    _arrow_line(d, (X(1983.6), lanes['bsd']), (X(1988.8), lanes['sysv']))
    _arrow_line(d, (X(1991.5), lanes['bsd']), (X(1992), lanes['free']))
    _arrow_line(d, (X(1994.5), lanes['bsd']), (X(1994.9), lanes['free']))
    # the releases, as nodes
    d.group()
    nodes = {'research': [1975.4, 1979], 'bsd': [1978.2, 1983.6, 1986.5, 1989.5, 1991.5, 1994.5],
             'sysv': [1982, 1983, 1988.8], 'free': [1992, 1993.5], 'linux': [1991.7]}
    for lane, yrs in nodes.items():
        for yr in yrs:
            d.circle(X(yr), lanes[lane], 2.4)
    # the axis
    d.group('mid')
    d.line((xl, axis_y), (xr, axis_y))
    d.lines([[(X(yr), axis_y), (X(yr), axis_y + 4)] for yr in range(1970, 1996, 5)])
    # labels
    d.group()
    for yr in range(1970, 1996, 5):
        d.text(X(yr), axis_y + 14, str(yr), size=7)
    d.text(xl, lanes['research'] - 8, 'RESEARCH UNIX', size=7, anchor='start')
    d.text(X(1979), lanes['research'] + 13, 'V7', size=6)
    d.text(X(1975.4), lanes['research'] - 8, 'V6', size=6)
    d.text(X(1978.2) - 4, lanes['bsd'] - 8, 'BERKELEY', size=7, anchor='start')
    d.text(X(1983.6), lanes['bsd'] + 13, '4.2', size=6)
    d.text(X(1989.5), lanes['bsd'] + 13, 'NET/1', size=6)
    d.text(X(1994.5), lanes['bsd'] - 8, 'LITE', size=6)
    d.text(X(1982) - 4, lanes['sysv'] + 14, 'AT&T SYSTEM V', size=7, anchor='start')
    d.text(X(1988.8), lanes['sysv'] - 8, 'SVR4', size=6)
    d.text(X(1990.2), lanes['sysv'] + 14, 'OSF | UI', size=6, anchor='start')
    d.text(X(1992) - 4, lanes['free'] + 14, '386BSD · NETBSD · FREEBSD', size=6, anchor='end')
    d.text(X(1991.7) - 6, lanes['linux'] + 3, 'LINUX · NO AT&T CODE', size=7, anchor='end')
    d.text((a + b) / 2, 90, 'USL v. BSDi', size=6)
    d.text(200, 24, 'ONE SYSTEM, MANY OWNERS · 1969–1995', size=8)
    return d


PLATES = {'multics': multics, 'c-language': c_language, 'pipes': pipes, 'bsd': bsd, 'unix-wars': unix_wars}
