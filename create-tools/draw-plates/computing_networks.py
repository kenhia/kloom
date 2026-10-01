"""computing plates, segment "Networks" and the "Security" frame of "Open questions" (sprint 015). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def packet_switching():
    """Circuit against packet switching on a space-time diagram: four stations, three hops, time running down.

    Circuit: a set-up signal crosses and is confirmed (each switch takes s to set), then the whole message
    flows as one band. Packet: the same message as three packets, each stored at a node until it has all
    arrived, then forwarded, so that the three hops are pipelined. p is the propagation time of a hop,
    t a packet's transmission time; both are in drawing units, invented for the drawing.
    """
    d = D()
    p, t, s = 8, 22, 6
    gap = 46
    top = 56
    panels = [(52, 'CIRCUIT'), (232, 'PACKET')]
    # construction: the station lines, and ticks of time
    d.group('thin')
    for x0, _ in panels:
        d.lines([[(x0 + gap * i, top - 12), (x0 + gap * i, 262)] for i in range(4)])
        d.lines([[(x0 - 6, y), (x0 + 3 * gap + 6, y)] for y in range(top, 263, 22)])
    xs_c = [panels[0][0] + gap * i for i in range(4)]
    xs_p = [panels[1][0] + gap * i for i in range(4)]
    # circuit: the set-up signal forward, held at each switch while it sets, and the confirmation back
    d.group('mid')
    y = top
    pts = [(xs_c[0], y)]
    for i in range(3):
        y += p
        pts.append((xs_c[i + 1], y))
        if i < 2:
            y += s
            pts.append((xs_c[i + 1], y))
    d.line(*pts)
    back = [(xs_c[3], y)]
    for i in range(3, 0, -1):
        y += p
        back.append((xs_c[i - 1], y))
        if i > 1:
            y += s
            back.append((xs_c[i - 1], y))
    d.line(*back)
    _arrow(d, xs_c[3], pts[-1][1], math.atan2(p, gap), 4)
    _arrow(d, xs_c[0], back[-1][1], math.atan2(p, -gap), 4)
    y_data = y + 4
    # circuit: the whole message as one band across the reserved path
    d.group()
    msg = 3 * t
    d.line((xs_c[0], y_data), (xs_c[3], y_data + 3 * p), (xs_c[3], y_data + 3 * p + msg), (xs_c[0], y_data + msg),
           closed=True)
    circuit_end = y_data + 3 * p + msg
    # packet: three packets, stored and forwarded hop by hop
    d.group()
    packet_end = 0
    for k in range(3):
        for h in range(3):
            start = top + k * t + h * (t + p)
            d.line((xs_p[h], start), (xs_p[h + 1], start + p), (xs_p[h + 1], start + p + t), (xs_p[h], start + t),
                   closed=True)
            packet_end = max(packet_end, start + t + p)
    # the arrival of each method's last bit, carried across both panels
    d.group('mid')
    d.line((xs_c[3], circuit_end), (xs_p[3] + 10, circuit_end))
    d.line((xs_p[3], packet_end), (xs_p[3] + 10, packet_end))
    _arrow(d, xs_p[3] + 10, circuit_end, 0, 3)
    _arrow(d, xs_p[3] + 10, packet_end, 0, 3)
    # labels
    d.group()
    for xs in (xs_c, xs_p):
        for x, name in zip(xs, ('A', 'N₁', 'N₂', 'B')):
            d.text(x, top - 18, name, size=8)
    d.text((xs_c[0] + xs_c[3]) / 2, 28, 'CIRCUIT SWITCHING', size=8)
    d.text((xs_p[0] + xs_p[3]) / 2, 28, 'PACKET SWITCHING', size=8)
    d.text(xs_c[0] - 8, top + 30, 'SET UP', size=7, anchor='end')
    d.text(xs_c[0] - 8, y_data + msg / 2 + 3, 'DATA', size=7, anchor='end')
    for k in range(3):
        d.text(xs_p[0] + 10, top + k * t + t / 2 + 4, str(k + 1), size=7)
    d.text(200, 284, 'TIME RUNS DOWN · STORE, THEN FORWARD', size=8)
    return d


# the four sites of December 1969: (name, host, latitude, longitude)
_SITES = [('UCLA', 'SIGMA 7', 34.07, -118.44), ('SRI', 'SDS 940', 37.46, -122.17),
          ('UCSB', '360/75', 34.41, -119.85), ('UTAH', 'PDP-10', 40.76, -111.85)]
_LINKS = [('UCLA', 'SRI'), ('UCLA', 'UCSB'), ('SRI', 'UCSB'), ('SRI', 'UTAH')]


def arpanet():
    """The ARPANET of December 1969, its four sites placed by latitude and longitude, and RFC 1's message:
    at most 8,080 bits behind a 16-bit header, cut by the IMP into packets of at most 1,010 bits."""
    d = D()
    lat0 = 37.5
    k = 20.0  # drawing units per degree of latitude
    cx, cy = -117.0, 37.4  # the map's centre

    def P(lat, lon):
        return (180 + k * math.cos(math.radians(lat0)) * (lon - cx), 114 - k * (lat - cy))

    pos = {n: P(la, lo) for n, _, la, lo in _SITES}
    # construction: a graticule every two degrees
    d.group('thin')
    lats = range(34, 42, 2)
    lons = range(-124, -108, 2)
    d.lines([[P(la, -124.5), P(la, -109.5)] for la in lats])
    d.lines([[P(33, lo), P(41.6, lo)] for lo in lons])
    # the leased 50-kilobit lines
    d.group()
    for a, b in _LINKS:
        d.line(pos[a], pos[b])
    # the IMPs, as squares, and each site's host hung from its IMP
    d.group()
    host_off = {'UCLA': (18, 12), 'SRI': (-18, -14), 'UCSB': (-20, 12), 'UTAH': (18, -12)}
    for n in pos:
        x, y = pos[n]
        _box(d, x - 5, y - 5, 10, 10)
    d.group('mid')
    for n in pos:
        x, y = pos[n]
        dx, dy = host_off[n]
        d.line((x + (5 if dx > 0 else -5), y), (x + dx, y + dy))
        d.circle(x + dx, y + dy, 4)
    # RFC 1's message and packets, as a bar of bits
    d.group('thin')
    bx, bw, by = 30, 340, 232
    per_bit = bw / 8080
    d.lines([[(bx + per_bit * 1010 * i, by - 6), (bx + per_bit * 1010 * i, by + 20)] for i in range(9)])
    d.group()
    hw = 16 * per_bit * 30  # the 16-bit header, drawn thirty times its width so its fields can be seen
    _box(d, bx - hw - 4, by, hw, 12)
    _box(d, bx, by, bw, 12)
    d.group('mid')
    fx = bx - hw - 4
    for bits in (5, 8, 1):
        fx += bits * per_bit * 30
        d.line((fx, by), (fx, by + 12))
    for i in range(8):
        d.line((bx + per_bit * 1010 * i + 3, by + 18), (bx + per_bit * 1010 * (i + 1) - 3, by + 18))
    # labels
    d.group()
    for n, host, _, _ in _SITES:
        x, y = pos[n]
        dx, dy = host_off[n]
        anchor = 'start' if dx > 0 else 'end'
        tx = x + dx + (7 if dx > 0 else -7)
        d.text(tx, y + dy + 3, n, size=8, anchor=anchor)
        d.text(tx, y + dy + 12, host, size=6, anchor=anchor)
    mx, my = (pos['UCLA'][0] + pos['SRI'][0]) / 2, (pos['UCLA'][1] + pos['SRI'][1]) / 2
    d.text(mx + 16, my + 2, 'L O', size=9, anchor='start')
    d.text(30, 20, 'ARPA NETWORK · DECEMBER 1969 · FOUR IMPS', size=8, anchor='start')
    d.text(bx - hw / 2 - 4, by - 6, 'HEADER', size=6)
    d.text(bx + bw / 2, by - 10, 'MESSAGE ≤ 8,080 BITS', size=7)
    d.text(bx + bw / 2, by + 32, 'EIGHT PACKETS OF ≤ 1,010 BITS · RFC 1, 7 APRIL 1969', size=7)
    return d


def _net_ring(d, cx, cy, r, n, rot=0):
    pts = [(cx + r * math.cos(rot + 2 * math.pi * i / n), cy + r * math.sin(rot + 2 * math.pi * i / n)) for i in range(n)]
    return pts


def internet():
    """Cerf and Kahn's 1974 picture: three unlike networks joined by two gateways, and one internetwork packet
    crossing them, its internet header and text untouched while each network's local header changes, and
    split in two by the gateway into the third network, whose packets are smaller."""
    d = D()
    cy = 92
    centres = [(62, cy), (200, cy), (338, cy)]
    r = 42
    # construction: each network's boundary circle, and the path's centre line
    d.group('thin')
    for x, y in centres:
        d.circle(x, y, r + 8)
    d.line((22, cy), (378, cy))
    # network A: a packet radio net (a star of radio links); B: a mesh like the ARPANET; C: a ring
    d.group('mid')
    ax, ay = centres[0]
    rim = _net_ring(d, ax, ay, r - 6, 5, -math.pi / 2)
    for q in rim:
        d.line((ax, ay), q)
        d.circle(q[0], q[1], 3)
    d.circle(ax, ay, 4)
    bx, by = centres[1]
    mesh = _net_ring(d, bx, by, r - 6, 6, 0)
    for i in range(6):
        d.line(mesh[i], mesh[(i + 1) % 6])
    for i in (0, 1, 3):
        d.line(mesh[i], mesh[i + 2 if i + 2 < 6 else 0])
    for q in mesh:
        _box(d, q[0] - 3, q[1] - 3, 6, 6)
    cx_, cy_ = centres[2]
    d.circle(cx_, cy_, r - 8)
    for q in _net_ring(d, cx_, cy_, r - 8, 6, math.pi / 6):
        d.circle(q[0], q[1], 3)
    # the gateways, one foot in each network, and the hosts
    d.group()
    g1 = ((centres[0][0] + centres[1][0]) / 2, cy)
    g2 = ((centres[1][0] + centres[2][0]) / 2, cy)
    for gx, gy in (g1, g2):
        _box(d, gx - 8, gy - 10, 16, 20)
        d.line((gx, gy - 10), (gx, gy + 10))
    d.line((ax - r + 6, cy), (g1[0] - 8, cy))
    d.line((g1[0] + 8, cy), (g2[0] - 8, cy))
    d.line((g2[0] + 8, cy), (cx_ + r - 8, cy))
    d.circle(ax - r + 2, cy, 4)
    d.circle(cx_ + r - 4, cy, 4)
    # the packet in each network: local header, internet header, text, checksum
    d.group('mid')
    rows = [(160, 'A'), (190, 'B'), (220, 'C')]
    x0 = 70
    widths = {'local': 30, 'inet': 40, 'text': 150, 'sum': 14}
    for y, net in rows[:2]:
        x = x0
        for key in ('local', 'inet', 'text', 'sum'):
            _box(d, x, y, widths[key], 14)
            x += widths[key]
    # in C the text is split in two fragments, each with its own local and internet header
    y = rows[2][0]
    x = x0
    half = widths['text'] / 2
    for frag in range(2):
        for key, w in (('local', 16), ('inet', 40), ('text', half - 12)):
            _box(d, x, y, w, 14)
            x += w
        x += 6
    _box(d, x - 6, y, widths['sum'], 14)
    # labels
    d.group()
    for (x, y), name in zip(centres, ('NET A', 'NET B', 'NET C')):
        d.text(x, y - r - 14, name, size=8)
    d.text(g1[0], cy + 24, 'G', size=8)
    d.text(g2[0], cy + 24, 'G', size=8)
    d.text(ax - r + 2, cy + 16, 'X', size=8)
    d.text(cx_ + r - 4, cy + 16, 'Y', size=8)
    for y, net in rows:
        d.text(x0 - 8, y + 10, net, size=8, anchor='end')
    d.text(x0 + 15, 154, 'LOCAL', size=6)
    d.text(x0 + 50, 154, 'INTERNET', size=6)
    d.text(x0 + 145, 154, 'TEXT', size=6)
    d.text(x0 + 241, 154, 'SUM', size=6)
    d.text(200, 262, 'GATEWAYS PASS THE INTERNET HEADER THROUGH,', size=8)
    d.text(200, 275, 'AND SPLIT A PACKET TOO BIG FOR THE NEXT NETWORK', size=8)
    return d


def world_wide_web():
    """The web's three inventions at once: pages of HTML whose anchors point at other pages, on two servers;
    an address in parts (scheme, host, path); and the HTTP of 1991, one GET line out and HTML back."""
    d = D()
    # the two servers' pages: a grid of lines per page
    pages = [(40, 40, 'info.cern.ch'), (40, 118, None), (150, 70, None), (290, 44, 'other host'), (290, 124, None)]
    pw, ph = 70, 58
    d.group('thin')
    d.line((24, 30), (232, 30), (232, 190), (24, 190), closed=True)
    d.line((274, 30), (376, 30), (376, 190), (274, 190), closed=True)
    d.group()
    for x, y, _ in pages:
        _box(d, x, y, pw, ph)
    d.group('mid')
    anchors = {}
    for i, (x, y, _) in enumerate(pages):
        for j in range(5):
            ly = y + 10 + j * 9
            w = pw - 16 - (j * 7) % 20
            d.line((x + 8, ly), (x + 8 + w, ly))
        anchors[i] = (x + 8 + 22, y + 10 + 2 * 9)
    # the links: from an anchor on one page to the top of another, as arcs
    d.group()
    links = [(0, 2), (2, 3), (1, 2), (2, 4), (4, 1)]
    for a, b in links:
        x1, y1 = anchors[a]
        x2, y2 = pages[b][0] + pw / 2, pages[b][1]
        if b == 1:
            x2, y2 = pages[b][0] + pw, pages[b][1] + ph / 2
        mx, my = (x1 + x2) / 2, min(y1, y2) - 18
        pts = [((1 - u) ** 2 * x1 + 2 * (1 - u) * u * mx + u * u * x2, (1 - u) ** 2 * y1 + 2 * (1 - u) * u * my + u * u * y2)
               for u in [i / 20 for i in range(21)]]
        d.line(*pts)
        ex, ey = pts[-1]
        px, py = pts[-2]
        _arrow(d, ex, ey, math.atan2(ey - py, ex - px), 4)
        d.circle(x1, y1, 1.6)
    # the exchange, client to server
    d.group('mid')
    d.line((40, 216), (360, 216))
    _arrow(d, 360, 216, 0)
    d.line((360, 230), (40, 230))
    _arrow(d, 40, 230, math.pi)
    # the address, bracketed into its parts
    d.group('thin')
    ay = 262
    parts = [(40, 84, 'SCHEME'), (96, 190, 'HOST'), (190, 360, 'PATH')]
    for x1, x2, _ in parts:
        d.line((x1, ay + 3), (x1, ay + 8), (x2, ay + 8), (x2, ay + 3))
    # labels
    d.group()
    d.text(75, 204, 'CLIENT', size=7)
    d.text(325, 204, 'SERVER', size=7)
    d.text(200, 212, 'GET /hypertext/WWW/TheProject.html', size=7)
    d.text(200, 242, 'HTML · The World Wide Web project …', size=7)
    d.text(40, ay, 'http://info.cern.ch/hypertext/WWW/TheProject.html', size=8, anchor='start')
    for x1, x2, name in parts:
        d.text((x1 + x2) / 2, ay + 18, name, size=6)
    d.text(128, 24, 'SERVER 1', size=7)
    d.text(325, 24, 'SERVER 2', size=7)
    return d


def security():
    """Diffie–Hellman on a clock of 23: the powers of 5 modulo 23 visit every residue in a scrambled order,
    which is easy to compute forwards and hard to run backwards. Numbers invented for the drawing:
    a = 6, b = 15 give A = 8, B = 19 and the shared key 2."""
    d = D()
    p, g, a, b = 23, 5, 6, 15
    A, B = pow(g, a, p), pow(g, b, p)
    key = pow(B, a, p)
    assert key == pow(A, b, p)
    cx, cy, r = 200, 138, 92

    def pt(v, rr=r):
        ang = -math.pi / 2 + 2 * math.pi * (v - 1) / (p - 1)
        return (cx + rr * math.cos(ang), cy + rr * math.sin(ang))

    # construction: the clock face and its 22 hour marks (residues 1 to 22)
    d.group('thin')
    d.circle(cx, cy, r)
    d.lines([[pt(v, r - 4), pt(v, r + 4)] for v in range(1, p)])
    d.circle(cx, cy, 2)
    # the walk g¹, g², g³ … round the clock: a closed star, since 5 generates every residue
    d.group('mid')
    walk = [pow(g, k, p) for k in range(1, p)]
    d.line(*[pt(v) for v in walk], closed=True)
    # Alice's and Bob's public numbers, and the key both reach
    d.group()
    for v in (A, B):
        x, y = pt(v)
        d.circle(x, y, 5)
    kx, ky = pt(key)
    d.circle(kx, ky, 5)
    d.circle(kx, ky, 8)
    # the exchange across the open line
    d.group('mid')
    d.line((24, 262), (376, 262))
    for x in (40, 360):
        _box(d, x - 18, 240, 36, 18)
    _arrow(d, 346, 262, 0)
    _arrow(d, 54, 262, math.pi)
    # labels
    d.group()
    for v in range(1, p):
        x, y = pt(v, r + 12)
        d.text(x, y + 3, str(v), size=6)
    for v, name in ((A, 'A'), (B, 'B'), (key, 'KEY')):
        x, y = pt(v, r - 16)
        d.text(x, y + 3, name, size=7)
    d.text(40, 252, 'a = 6', size=7)
    d.text(360, 252, 'b = 15', size=7)
    d.text(200, 256, f'A = 5⁶ mod 23 = {A}  →   ←  B = 5¹⁵ mod 23 = {B}', size=7)
    d.text(200, 278, f'B⁶ = A¹⁵ = {key} mod 23 · THE LINE CARRIES 5, 23, {A}, {B}, NEVER {key}', size=7)
    d.text(200, 24, 'POWERS OF 5 ROUND A CLOCK OF 23', size=8)
    return d


PLATES = {
    'packet-switching': packet_switching,
    'arpanet': arpanet,
    'internet': internet,
    'world-wide-web': world_wide_web,
    'security': security,
}
