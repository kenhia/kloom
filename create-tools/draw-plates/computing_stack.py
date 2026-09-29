"""computing plates, trail "The internet stack" (sprint 015). See computing.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _message(d, p0, p1, size=4):
    """A line from p0 to p1 with an arrowhead at p1."""
    d.line(p0, p1)
    _arrow(d, p1[0], p1[1], math.atan2(p1[1] - p0[1], p1[0] - p0[0]), size)


def _box(d, x0, y0, x1, y1):
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)


def ethernet():
    """CSMA/CD on a shared cable, as a space–time diagram: distance along the cable across, time down.

    A starts; B, still hearing silence, starts just before A's signal reaches it. The two fronts
    meet, each station hears the other, jams, and stops. The overlap is hatched.
    """
    d = D()
    xa, xb = 70, 330            # the two stations' taps on the cable
    y_cable, t0 = 44, 62        # the cable, and time zero on the diagram
    tau = 70                    # one end-to-end propagation time, in drawing units (A to B)
    k = tau / (xb - xa)         # time per unit of distance
    tb = t0 + 0.7 * tau         # B starts at 0.7 τ: carrier sense has not yet heard A
    jam = 10                    # the jam, drawn long enough to see
    a_hears = tb + tau          # B's front reaches A
    b_hears = t0 + tau          # A's front reaches B
    a_stop, b_stop = a_hears + jam, b_hears + jam
    front_a = lambda x: t0 + (x - xa) * k       # A's leading edge
    front_b = lambda x: tb + (xb - x) * k       # B's leading edge
    tail_a = lambda x: a_stop + (x - xa) * k    # A's trailing edge
    tail_b = lambda x: b_stop + (xb - x) * k    # B's trailing edge
    xm = (tb - t0 + (xa + xb) * k) / (2 * k)    # where the fronts meet
    # construction: the stations' world lines, time ticks in units of τ, the meeting point
    d.group('thin')
    d.lines([[(x, y_cable), (x, 266)] for x in (xa, xb)])
    d.lines([[(12, t0 + i * tau / 2), (20, t0 + i * tau / 2)] for i in range(7)])
    d.line((16, t0), (16, t0 + 3 * tau))
    d.lines([[(xm, y_cable), (xm, front_a(xm))], [(40, front_a(xm)), (360, front_a(xm))]])
    # the cable, its terminators and the two taps
    d.group()
    d.line((30, y_cable), (370, y_cable))
    d.lines([[(30, y_cable - 6), (30, y_cable + 6)], [(370, y_cable - 6), (370, y_cable + 6)]])
    for x in (xa, xb):
        _box(d, x - 9, y_cable - 16, x + 9, y_cable - 6)
        d.line((x, y_cable - 6), (x, y_cable))
    # the transmissions on each station's own line, heavy while it sends
    d.line((xa, t0), (xa, a_stop))
    d.line((xb, tb), (xb, b_stop))
    # the signal fronts spreading both ways along the cable
    d.group('mid')
    d.lines([
        [(xa, t0), (xb, front_a(xb))], [(xa, t0), (30, t0 + (xa - 30) * k)],
        [(xb, tb), (xa, front_b(xa))], [(xb, tb), (370, tb + (370 - xb) * k)],
        [(xa, a_stop), (xa + (266 - a_stop) / k, 266)],
        [(xb, b_stop), (xa, tail_b(xa))],
    ])
    # the collision: every point of the cable where both signals are present, hatched
    d.group('thin')
    hatch = []
    for i in range(1, 60):
        c = t0 + 4 * i                          # hatch lines of slope -1 in (x, t): x + t = const
        seg = []
        for x in range(xa, xb + 1):
            t = c + (x - xa) * 0.35
            lo = max(front_a(x), front_b(x))
            hi = min(tail_a(x), tail_b(x))
            if lo <= t <= hi:
                seg.append((x, t))
        if len(seg) > 1:
            hatch.append([seg[0], seg[-1]])
    d.lines(hatch)
    # labels
    d.group()
    d.text(xa - 14, y_cable - 8, 'A', size=9, anchor='end')
    d.text(xb + 14, y_cable - 8, 'B', size=9, anchor='start')
    d.text(24, t0 + 3, '0', size=7, anchor='start')
    d.text(24, t0 + tau + 3, 'τ', size=8, anchor='start')
    d.text(24, t0 + 2 * tau + 3, '2τ', size=8, anchor='start')
    d.text(24, t0 + 3 * tau + 3, '3τ', size=8, anchor='start')
    d.text(xm - 8, front_a(xm) - 8, 'FRONTS MEET', size=7, anchor='end')
    d.text(xb + 6, b_hears + 3, 'B HEARS A', size=7, anchor='start')
    d.text(xb + 6, b_stop + 6, 'JAMS', size=7, anchor='start')
    d.text(xa - 6, a_hears + 3, 'A HEARS B', size=7, anchor='end')
    d.text(xa - 6, a_stop + 6, 'JAMS', size=7, anchor='end')
    d.text(262, 178, 'COLLISION', size=8)
    d.text(xb + 6, tb - 8, 'B SENDS', size=7, anchor='start')
    d.text(xa + 6, t0 - 4, 'A SENDS', size=7, anchor='start')
    d.text(200, 26, 'COAXIAL CABLE · SPACE ACROSS · TIME DOWN', size=7)
    d.text(200, 288, 'CARRIER SENSE · COLLISION DETECT · BACK OFF', size=8)
    return d


IPV4_ROWS = [
    [('VER 4', 4), ('IHL 5', 4), ('TOS', 8), ('TOTAL LENGTH', 16)],
    [('IDENTIFICATION', 16), ('FLG', 3), ('FRAGMENT OFFSET', 13)],
    [('TTL 64', 8), ('PROTO 6', 8), ('HEADER CHECKSUM', 16)],
    [('SOURCE 192.0.2.10', 32)],
    [('DESTINATION 198.51.100.7', 32)],
]


def ip_routing():
    """The IPv4 header of RFC 791, five 32-bit words, filled in for an invented TCP datagram."""
    d = D()
    x0, bw = 64, 9               # left edge; one bit is 9 units wide, so a word is 288
    y0, rh = 72, 32              # the first word's top; a word's height
    rows = len(IPV4_ROWS)
    # construction: a tick for every bit, carried down the whole header, and the octet boundaries
    d.group('thin')
    d.lines([[(x0 + b * bw, y0 - (8 if b % 8 == 0 else 4)), (x0 + b * bw, y0)] for b in range(33)])
    d.lines([[(x0 + b * bw, y0 + r * rh + e), (x0 + b * bw, y0 + r * rh + e + 5 * (1 if e == 0 else -1))]
             for b in (8, 16, 24) for r in range(rows) for e in (0, rh)])  # octet marks inside each word
    d.line((x0 - 14, y0), (x0 - 14, y0 + rows * rh))
    # the header's outline and its words
    d.group()
    _box(d, x0, y0, x0 + 32 * bw, y0 + rows * rh)
    d.lines([[(x0, y0 + r * rh), (x0 + 32 * bw, y0 + r * rh)] for r in range(1, rows)])
    # the field boundaries within each word
    d.group('mid')
    seps = []
    for r, fields in enumerate(IPV4_ROWS):
        b = 0
        for _, w in fields[:-1]:
            b += w
            seps.append([(x0 + b * bw, y0 + r * rh), (x0 + b * bw, y0 + (r + 1) * rh)])
    d.lines(seps)
    # the payload, the TCP segment the header carries, running off the plate
    d.line((x0, y0 + rows * rh), (x0, y0 + rows * rh + 30))
    d.line((x0 + 32 * bw, y0 + rows * rh), (x0 + 32 * bw, y0 + rows * rh + 30))
    d.lines([[(x0 + i * 16, y0 + rows * rh + 30), (x0 + i * 16 + 8, y0 + rows * rh + 30)] for i in range(18)])
    # labels: the bit ruler, each field, the size
    d.group()
    for b in (0, 8, 16, 24, 31):
        d.text(x0 + b * bw + bw / 2, y0 - 12, str(b), size=7)
    for r, fields in enumerate(IPV4_ROWS):
        b = 0
        for name, w in fields:
            d.text(x0 + (b + w / 2) * bw, y0 + r * rh + rh / 2 + 3, name, size=7 if w >= 8 else 6)
            b += w
    d.text(x0 - 18, y0 + rows * rh / 2 + 3, '20 BYTES', size=7, anchor='end')
    d.text(x0 + 16 * bw, y0 + rows * rh + 20, 'DATA · A TCP SEGMENT', size=7)
    d.text(x0 + 16 * bw, 32, 'IPv4 HEADER · RFC 791 · 1981', size=9)
    d.text(x0 + 16 * bw, 286, 'TTL − 1 AT EVERY ROUTER · DROPPED AT 0', size=7)
    return d


def tcp():
    """The three-way handshake of RFC 793 (its own sequence numbers), then a lost segment and its retransmission."""
    d = D()
    xa, xb = 136, 300
    top, drop = 48, 28            # the first send; how far time runs while a segment crosses
    msgs = [  # (from A?, send time, label, lost?)
        (True, top, 'SYN SEQ=100', False),
        (False, top + drop, 'SYN+ACK SEQ=300 ACK=101', False),
        (True, top + 2 * drop, 'ACK SEQ=101 ACK=301', False),
        (True, top + 3 * drop + 8, 'SEQ=101 · 100 BYTES', True),
        (True, top + 6 * drop + 8, 'SEQ=101 · 100 BYTES', False),
        (False, top + 7 * drop + 8, 'ACK=201', False),
    ]
    rto0, rto1 = msgs[3][1], msgs[4][1]
    # construction: the two ends' time lines, and the round-trip and timeout brackets
    d.group('thin')
    d.lines([[(x, top - 12), (x, 280)] for x in (xa, xb)])
    for t0, t1 in ((top, top + 2 * drop), (rto0, rto1)):
        d.lines([[(46, t0), (58, t0)], [(46, t1), (58, t1)], [(52, t0), (52, t1)]])
    # the two hosts
    d.group()
    _box(d, xa - 20, top - 32, xa + 20, top - 14)
    _box(d, xb - 20, top - 32, xb + 20, top - 14)
    # the segments
    d.group('mid')
    for from_a, t, _, lost in msgs:
        p0 = (xa, t) if from_a else (xb, t)
        p1 = (xb, t + drop) if from_a else (xa, t + drop)
        if lost:
            pm = (p0[0] + 0.6 * (p1[0] - p0[0]), p0[1] + 0.6 * (p1[1] - p0[1]))
            d.line(p0, pm)
            d.lines([[(pm[0] - 4, pm[1] - 4), (pm[0] + 4, pm[1] + 4)], [(pm[0] - 4, pm[1] + 4), (pm[0] + 4, pm[1] - 4)]])
        else:
            _message(d, p0, p1)
    # labels: hosts, segments (above each, from its sender), states, brackets
    d.group()
    d.text(xa, top - 20, 'A', size=8)
    d.text(xb, top - 20, 'B', size=8)
    for from_a, t, label, lost in msgs:
        f = 0.35 if lost else 0.5 if from_a else 0.6   # clear of the arrow arriving where a reply leaves
        d.text(xa + f * (xb - xa) if from_a else xb - f * (xb - xa), t + f * drop - 8, label, size=6)
    for t, name in ((top, 'SYN-SENT'), (top + 2 * drop, 'ESTABLISHED')):
        d.text(xa - 6, t + 3, name, size=6, anchor='end')
    for t, name in ((top, 'LISTEN'), (top + drop, 'SYN-RECEIVED'), (top + 3 * drop, 'ESTABLISHED')):
        d.text(xb + 6, t + 3, name, size=6, anchor='start')
    d.text(44, top + drop + 3, 'RTT', size=6, anchor='end')
    d.text(44, (rto0 + rto1) / 2 + 3, 'RTO', size=6, anchor='end')
    d.text(xa - 6, (rto0 + rto1) / 2 + 3, 'NO ACK', size=6, anchor='end')
    d.text(xa - 6, (rto0 + rto1) / 2 + 12, 'SEND AGAIN', size=6, anchor='end')
    d.text(210, 294, 'THREE-WAY HANDSHAKE · RFC 793 · 1981', size=8)
    return d


def _pair(d, p0, p1, gap=3):
    """A question from p0 to p1 and its reply back, as two parallel arrows `gap` apart."""
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    nx, ny = -math.sin(ang) * gap, math.cos(ang) * gap
    _message(d, (p0[0] - nx, p0[1] - ny), (p1[0] - nx, p1[1] - ny), 3.5)
    _message(d, (p1[0] + nx, p1[1] + ny), (p0[0] + nx, p0[1] + ny), 3.5)


def dns():
    """The domain tree, and an iterative lookup of www.example.org walked down it from a resolver."""
    d = D()
    root = (272, 54)
    tlds = [('org', 176), ('com', 232), ('edu', 282), ('net', 330), ('uk', 374)]
    ytld, y2, y3 = 128, 192, 252
    org, example, www = (176, ytld), (176, y2), (176, y3)
    res = (58, 100)
    # construction: the levels of the hierarchy
    d.group('thin')
    d.lines([[(120, y), (390, y)] for y in (root[1], ytld, y2, y3)])
    # the tree
    d.group()
    d.circle(*root, 8)
    for _, x in tlds:
        ang = math.atan2(ytld - root[1], x - root[0])
        d.line((root[0] + 8 * math.cos(ang), root[1] + 8 * math.sin(ang)),
               (x - 8 * math.cos(ang), ytld - 8 * math.sin(ang)))
        d.circle(x, ytld, 8)
    d.line((org[0], org[1] + 8), (example[0], example[1] - 8))
    d.circle(*example, 8)
    d.line((example[0], example[1] + 8), (www[0], www[1] - 6))
    d.circle(*www, 6)
    _box(d, res[0] - 32, res[1] - 14, res[0] + 32, res[1] + 14)
    # the queries and the referrals: each goes to a server one level further down, and comes back
    d.group('mid')
    ends = []
    for node in (root, org, example):
        start = (res[0] + 32, res[1] - 6 + 6 * len(ends))
        ang = math.atan2(node[1] - start[1], node[0] - start[0])
        end = (node[0] - 12 * math.cos(ang), node[1] - 12 * math.sin(ang))
        _pair(d, start, end)
        ends.append((start, end))
    # labels
    d.group()
    d.text(root[0], root[1] - 14, '“.” ROOT', size=8)
    for name, x in tlds:
        d.text(x + (0 if name != 'org' else -14), ytld + 20, name, size=8, anchor='middle' if name != 'org' else 'end')
    d.text(example[0] + 14, example[1] + 3, 'example', size=8, anchor='start')
    d.text(www[0] + 12, www[1] + 3, 'www', size=8, anchor='start')
    d.text(res[0], res[1] + 3, 'RESOLVER', size=7)
    d.text(res[0], res[1] + 28, 'www.example.org?', size=7)
    for (s0, e0), lab in zip(ends, ('1 · 2', '3 · 4', '5 · 6')):
        mx, my = (s0[0] + e0[0]) / 2, (s0[1] + e0[1]) / 2
        d.text(mx - 4, my - 8 if lab == '1 · 2' else my + 14, lab, size=7)
    d.text(390, root[1] - 4, 'ROOT ZONE', size=6, anchor='end')
    d.text(390, ytld + 34, 'TOP LEVEL', size=6, anchor='end')
    d.text(390, y2 - 4, 'SECOND LEVEL', size=6, anchor='end')
    d.text(200, 284, 'A NAME IS READ RIGHT TO LEFT, ONE REFERRAL PER DOT', size=7)
    return d


def tls():
    """A certificate chain (root signs intermediate signs leaf) and TLS 1.3's hybrid key share."""
    d = D()
    x, cw, ch = 34, 124, 54
    certs = [('ROOT CA', 'SELF-SIGNED · IN THE TRUST STORE', 38), ('INTERMEDIATE CA', 'SIGNED BY THE ROOT', 120), ('example.org', 'SIGNED BY THE INTERMEDIATE', 202)]
    key_y = lambda y: y + 40      # a certificate's public key, bottom left
    sig_y = lambda y: y + 26      # its signature block, right
    xr = x + cw + 14              # the rail the signing arrows run down
    # construction: the key and signature levels carried out to the rail
    d.group('thin')
    d.lines([[(x, sig_y(y)), (xr + 6, sig_y(y))] for _, _, y in certs])
    d.line((xr, sig_y(certs[0][2]) - 10), (xr, sig_y(certs[-1][2]) + 10))
    d.lines([[(252, 64), (252, 252)], [(368, 64), (368, 252)]])
    # the three certificates
    d.group()
    for _, _, y in certs:
        _box(d, x, y, x + cw, y + ch)
    # each certificate's contents: a rule under its name, a key, a signature block
    d.group('mid')
    for _, _, y in certs:
        d.line((x + 8, y + 16), (x + cw - 8, y + 16))
        d.circle(x + 16, key_y(y), 5)
        d.line((x + 21, key_y(y)), (x + 40, key_y(y)), (x + 40, key_y(y) + 5))
        d.line((x + 33, key_y(y)), (x + 33, key_y(y) + 4))
        _box(d, x + cw - 34, sig_y(y) - 7, x + cw - 8, sig_y(y) + 7)
    # the signatures: each issuer's key signs the next certificate, and the root signs itself
    for i, (_, _, y) in enumerate(certs[:-1]):
        ny = certs[i + 1][2]
        d.line((x + 45, key_y(y)), (x + cw + 6, key_y(y)), (xr, key_y(y)))
        d.line((xr, key_y(y)), (xr, sig_y(ny)))
        _message(d, (xr, sig_y(ny)), (x + cw - 8, sig_y(ny)), 3.5)
    y = certs[0][2]
    d.line((xr, key_y(y)), (xr + 8, key_y(y)), (xr + 8, sig_y(y)))
    _message(d, (xr + 8, sig_y(y)), (x + cw - 8, sig_y(y)), 3.5)
    # the hybrid key share: two shared secrets into one key derivation
    d.group()
    _box(d, 226, 76, 278, 102)
    _box(d, 342, 76, 394, 102)
    _box(d, 280, 152, 340, 178)
    _box(d, 286, 222, 334, 244)
    d.group('mid')
    _message(d, (252, 102), (300, 152), 3.5)
    _message(d, (368, 102), (320, 152), 3.5)
    _message(d, (310, 178), (310, 222), 3.5)
    # labels
    d.group()
    for name, sub, y in certs:
        d.text(x + cw / 2, y + 11, name, size=7)
        d.text(x, y + ch + 10, sub, size=6, anchor='start')
    d.text(x + cw - 21, sig_y(certs[0][2]) + 20, 'SIG', size=6)
    d.text(x + 30, key_y(certs[-1][2]) - 8, 'KEY', size=6)
    d.text(252, 93, 'X25519', size=7)
    d.text(368, 93, 'ML-KEM', size=7)
    d.text(310, 168, 'HKDF', size=7)
    d.text(310, 236, 'KEYS', size=7)
    d.text(310, 60, 'TLS 1.3 HYBRID KEY SHARE', size=7)
    d.text(310, 128, 'CLASSICAL + POST-QUANTUM', size=6)
    d.text(200, 290, 'WHO YOU ARE TALKING TO · A KEY NOBODY ELSE HAS', size=7)
    return d


PLATES = {'ethernet': ethernet, 'ip-routing': ip_routing, 'tcp': tcp, 'dns': dns, 'tls': tls}
