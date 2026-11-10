"""Plates for Sound and Score's part piano2 (sprint 058): the iron frame, the player piano and the
Rhodes. See plates_for.py."""
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


def _bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, e = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + e * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + e * p3[1]))
    return out


def _hit(p, q, poly):
    """Where the ray from p through q first crosses the polyline poly."""
    best = None
    for a, b in zip(poly, poly[1:]):
        dx, dy = q[0] - p[0], q[1] - p[1]
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = dx * ey - dy * ex
        if abs(den) < 1e-9:
            continue
        t = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / den
        u = ((a[0] - p[0]) * dy - (a[1] - p[1]) * dx) / den
        if t > 0 and 0 <= u <= 1 and (best is None or t < best):
            best = t
    return (p[0] + best * (q[0] - p[0]), p[1] + best * (q[1] - p[1]))


def _offset(poly, k):
    """The polyline moved k units to its left (inward, for a curve drawn tail to keyboard)."""
    out = []
    for i, (x, y) in enumerate(poly):
        a, b = poly[max(i - 1, 0)], poly[min(i + 1, len(poly) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        n = math.hypot(tx, ty) or 1
        out.append((x + k * ty / n, y - k * tx / n))
    return out


def iron_frame():
    d = D()
    # A grand in plan, keyboard to the left, bass side along the top, after the layout of Henry
    # Steinway Jr.'s patent 26,532 (1859): treble strings square to the hammer line, the tenor strings
    # of the lower tier fanned toward the bass side at their far ends, and the covered bass strings
    # in an upper tier crossing over them toward a second bridge near the middle of the soundboard.
    # Proportions are a modern 2.7 m concert grand's, about 128 px a metre; one line is drawn for
    # several unisons, so the string counts are schematic. Strings end where they meet the bridges.
    x0, yb, yt, tail = 30, 46, 252, 378
    hl = 66                                                                 # hammer line
    # the treble side, from the tail round the bentside to the keyboard
    side = _bez((tail, 60), (tail, 120), (250, 180), (200, 236), n=30) + _bez((200, 236), (170, 252), (130, yt), (112, yt), n=12)[1:]
    outline = [(x0, yb), (tail - 10, yb), (tail, 52)] + side + [(x0, yt)]
    plate = _offset(side, -7)
    bridge = [(tail - 40, yb + 14)] + _offset(side, -20)

    d.group('thin')
    d.line((hl, yb - 10), (hl, yt + 10))
    d.line((x0 - 6, yb), (x0 - 16, yb)); d.line((x0 - 6, yt), (x0 - 16, yt))
    d.line((x0 - 11, yb), (x0 - 11, yt))
    d.line((x0, 272), (tail, 272)); d.line((x0, 266), (x0, 278)); d.line((tail, 266), (tail, 278))

    d.group()
    d.line(*outline, closed=True)                                           # the case
    d.line((x0, yb + 4), (x0 + 20, yb + 4), (x0 + 20, yt - 4), (x0, yt - 4))  # keybed and pinblock

    d.group('mid')                                                          # the plate's rim
    d.line((x0 + 24, yt - 6), (x0 + 24, yb + 6), (tail - 14, yb + 6), *plate, (x0 + 24, yt - 6))

    d.group()
    lower = []
    for i in range(10):                                                     # treble: square to the hammer line
        y = yt - 26 - i * 7.6
        p = (hl - 10, y)
        lower.append((p, _hit(p, (p[0] + 10, y), bridge)))
    for i in range(9):                                                      # tenor: fanned toward the bass side
        y = 148 - i * 6.2
        p = (hl - 10, y)
        lower.append((p, _hit(p, (p[0] + 100, y - 2 - i * 1.0), bridge)))
    bb0, bb1 = (232, 150), (322, 104)                                       # the bass bridge, mid-board
    upper = []
    for i in range(8):                                                      # bass: upper tier, crossing over
        p = (hl - 10, 56 + i * 5.4)
        t = 1 - i / 7
        q = (bb0[0] + t * (bb1[0] - bb0[0]), bb0[1] + t * (bb1[1] - bb0[1]))
        upper.append((p, q))
    d.lines([list(s) for s in lower])
    d.lines([list(s) for s in upper])

    d.group('mid')
    d.line(*sorted([s[1] for s in lower], key=lambda p: -p[1]))             # main bridge, through the string ends
    d.line((bb0[0] - 4, bb0[1] + 4), (bb1[0] + 4, bb1[1] - 4))              # bass bridge
    for s in lower + upper:                                                 # tuning pins
        d.circle(s[0][0] - 3, s[0][1], 1.2)
    for x, y in ((160, 84), (178, 206), (300, 70)):                         # holes in the plate
        d.circle(x, y, 6)

    d.group('mid')
    d.text(hl, 36, 'HAMMER LINE', size=7)
    d.text(214, 62, 'BASS · UPPER TIER', size=7)
    d.text(318, 222, 'TENOR FAN', size=7)
    d.line((306, 214), (236, 140))
    d.text(118, 240, 'TREBLE', size=7)
    d.text(296, 140, 'BASS BRIDGE', size=7, anchor='start')
    d.text(204, 286, 'GRAND IN PLAN · AFTER US PATENT 26,532, 1859 · 2.7 M', size=7)
    return d


def player_piano():
    d = D()
    # One note of a pneumatic player in section, as a flow, after William Braid White's account of
    # the double-valve action (1914): a hole in the roll opens a duct in the tracker bar; air at room
    # pressure lifts the primary pouch; that lets air under the secondary pouch, whose valve connects
    # the striking pneumatic to the reduced-pressure chest; the pneumatic collapses and lifts the
    # piano's action. Proportions are schematic. Above, a strip of roll at 9 holes to the inch.
    # the roll: spools in section and the paper between them over the tracker bar
    s1, s2, r = (40, 96), (178, 96), 18
    tb = (109, 76)                       # tracker-bar face, centre
    d.group('thin')
    d.line((s1[0], 70), (s1[0], 128)); d.line((s2[0], 70), (s2[0], 128))
    d.line((20, 210), (390, 210))                                           # chest's top board line
    # strip of roll: 88 channels at 9 to the inch, drawn as a short window of 14 channels
    d.group('mid')
    for k in range(15):
        x = 22 + k * 11.4
        d.line((x, 16), (x, 44))
    d.group()
    d.line((s1[0] + r * 0.2, s1[1] - r), (tb[0] - 14, tb[1] - 2), (tb[0] + 14, tb[1] - 2), (s2[0] - r * 0.2, s2[1] - r))
    d.circle(*s1, r); d.circle(*s1, 5)
    d.circle(*s2, r - 4); d.circle(*s2, 5)
    _box(d, tb[0] - 16, tb[1], 32, 12)                                      # tracker bar
    d.line((tb[0] - 2, tb[1]), (tb[0] - 2, tb[1] + 12)); d.line((tb[0] + 2, tb[1]), (tb[0] + 2, tb[1] + 12))
    # holes punched in the strip, a few notes of a chord and a run
    holes = [(0, 0), (4, 0), (7, 0), (2, 1), (5, 1), (9, 1), (12, 2), (11, 2), (3, 2), (8, 2)]
    for k, row in holes:
        d.line((22 + k * 11.4 + 3, 18 + row * 8.6), (22 + k * 11.4 + 8.4, 18 + row * 8.6),
               (22 + k * 11.4 + 8.4, 23.4 + row * 8.6), (22 + k * 11.4 + 3, 23.4 + row * 8.6), closed=True)
    _box(d, 20, 14, 174, 32)

    # tube down to the primary valve
    p = (60, 196)                        # primary pouch chamber centre
    q = (150, 196)                       # secondary pouch chamber centre
    d.group()
    d.line((tb[0] - 2, tb[1] + 12), (tb[0] - 2, 146), (16, 146), (16, 200), (30, 200))
    d.line((tb[0] + 2, tb[1] + 12), (tb[0] + 2, 150), (20, 150), (20, 204), (30, 204))
    # chests: the primary and secondary valve boxes, the reduced-pressure chest below
    _box(d, 30, 176, 60, 34); _box(d, 116, 176, 70, 34)
    _box(d, 24, 210, 230, 36)
    # pouches (leather diaphragms, as shallow arcs) and valve stems with their discs
    for c, w in ((p, 22), (q, 28)):
        d.arc(c[0], c[1] + 10, w, 200, 340, n=24)
        d.line((c[0], c[1] + 4), (c[0], c[1] - 14))
        d.line((c[0] - 8, c[1] - 14), (c[0] + 8, c[1] - 14))
        d.line((c[0] - 6, c[1] + 18), (c[0] + 6, c[1] + 18))
    # channel primary -> secondary; secondary -> striking pneumatic
    d.line((90, 186), (116, 186))
    d.line((186, 186), (232, 186), (232, 168))
    # the striking pneumatic: a hinged wedge, open, and its collapsed position dashed
    h = (226, 168)
    d.line(h, (300, 168)); d.line(h, (300, 140)); d.line((300, 168), (300, 140))
    d.group('mid')
    d.dashed(h, (300, 156), dash=3, gap=3)
    # the lifter and the piano action: wippen, hammer on its shank, a string
    d.group()
    d.line((292, 140), (292, 118))
    d.line((282, 118), (330, 112))                                          # wippen
    d.line((326, 112), (326, 78))                                           # hammer shank
    d.ellipse(326, 72, 7, 5)                                                # hammer head
    d.line((290, 58), (390, 58))                                            # string
    d.group('mid')
    d.line((tb[0], 60), (tb[0], 74)); _arrow(d, (tb[0], 60), (tb[0], 74), 4)          # air in through the hole
    
    _arrow(d, (326, 86), (326, 79), 4)
    d.line((230, 248), (230, 274)); _arrow(d, (230, 248), (230, 274), 4)
    d.text(40, 128, 'SUPPLY', size=7)
    d.text(178, 128, 'TAKE-UP', size=7)
    d.text(118, 66, 'TRACKER BAR', size=7, anchor='start')
    d.text(107, 9, 'A STRIP OF ROLL · 9 HOLES TO THE INCH', size=7)
    d.text(60, 172, 'PRIMARY', size=7)
    d.text(151, 172, 'SECONDARY', size=7)
    d.text(139, 238, 'REDUCED-PRESSURE CHEST', size=7)
    d.text(262, 186, 'STRIKING', size=7, anchor='start')
    d.text(262, 194, 'PNEUMATIC', size=7, anchor='start')
    d.text(344, 92, 'HAMMER', size=7, anchor='start')
    d.text(236, 282, 'TO THE PEDAL BELLOWS', size=7, anchor='start')
    d.text(200, 296, 'ONE NOTE · DOUBLE-VALVE PNEUMATIC ACTION · AFTER WHITE, 1914', size=7)
    return d


def rhodes():
    d = D()
    # One Rhodes tone generator in elevation, after Harold Rhodes's patent 2,972,922 (1961): a tine
    # of piano wire pressed into a block, with a heavier tone bar above it as the other prong of an
    # asymmetric tuning fork; a coiled spring on the tine sets its pitch; the hammer strikes the tine
    # near its root from below; an electromagnetic pickup faces the tine's free tip. The tine's
    # dashed swing is the first mode of a cantilever, computed; the trace below is a decaying tone.
    bx, by = 70, 120                     # the block where tine and bar join
    L = 210                              # tine length drawn
    ty = by + 18                         # tine axis
    d.group('thin')
    d.line((bx - 30, ty), (bx + L + 60, ty))                               # tine axis
    d.line((bx + L, ty - 40), (bx + L, ty + 40))
    # first cantilever mode, beta L = 1.8751
    bl = 1.8751
    sg = (math.cosh(bl) + math.cos(bl)) / (math.sinh(bl) + math.sin(bl))
    def mode(s):
        z = bl * s
        return (math.cosh(z) - math.cos(z)) - sg * (math.sinh(z) - math.sin(z))
    m1 = mode(1.0)
    amp = 9
    for sgn in (1, -1):
        pts = [(bx + L * i / 40, ty + sgn * amp * mode(i / 40) / m1) for i in range(41)]
        d.dashed(*pts, dash=3, gap=3)

    d.group()
    # the tone bar's heel, into which the tine is pressed, and its mounting screw
    _box(d, bx - 22, by - 30, 26, 58)
    d.line((bx - 9, by + 28), (bx - 9, by + 44))
    # tone bar: a twisted cast bar above the tine, drawn with its twist as a narrowing band
    tb_y = by - 18
    d.line((bx + 4, tb_y - 8), (bx + 170, tb_y - 8), (bx + 186, tb_y - 2), (bx + 186, tb_y + 6), (bx + 170, tb_y + 8), (bx + 4, tb_y + 8))
    d.line((bx + 90, tb_y - 8), (bx + 100, tb_y + 8))
    d.line((bx + 100, tb_y - 8), (bx + 90, tb_y + 8))
    # tine: piano wire from the block
    d.line((bx + 4, ty - 1.6), (bx + L, ty - 0.8)); d.line((bx + 4, ty + 1.6), (bx + L, ty + 0.8))
    d.line((bx + L, ty - 0.8), (bx + L, ty + 0.8))
    # tuning spring on the tine, a helix seen side on
    sx0, n = bx + 120, 7
    pts = []
    for i in range(n * 12 + 1):
        a = 2 * math.pi * i / 12
        pts.append((sx0 + i * 0.25 + 1.2 * math.sin(a), ty + 4 * math.cos(a)))
    d.line(*pts)
    # pickup: coil around a pole piece facing the tine tip, with leads to the amplifier
    px = bx + L + 14
    _box(d, px, ty - 14, 26, 28)
    for k in range(6):
        d.line((px + 3 + k * 4, ty - 14), (px + 3 + k * 4, ty + 14))
    d.line((px - 6, ty - 3), (px, ty - 3)); d.line((px - 6, ty + 3), (px, ty + 3)); d.line((px - 6, ty - 3), (px - 6, ty + 3))
    d.line((px + 26, ty - 6), (px + 46, ty - 6), (px + 46, ty - 40))
    d.line((px + 26, ty + 6), (px + 52, ty + 6), (px + 52, ty - 40))
    # the hammer: a lever from the key, its tip under the tine near the root
    hx = bx + 26
    d.line((hx - 84, by + 103), (hx + 10, by + 91))                        # key lever
    d.line((hx - 84, by + 103), (hx - 84, by + 95))                       # the key's front, where it is pressed
    d.line((hx - 4, by + 92), (hx, ty + 10))                                # hammer arm
    _box(d, hx - 6, ty + 4, 12, 7)                                          # hammer tip
    d.line((hx - 36, by + 108), (hx - 30, by + 97), (hx - 24, by + 108), closed=True)  # balance rail
    # damper above the tine
    _box(d, bx + 52, ty - 12, 18, 6)

    d.group('mid')
    d.line((hx + 14, ty + 30), (hx + 14, ty + 14)); _arrow(d, (hx + 14, ty + 30), (hx + 14, ty + 14), 4)
    d.line((hx - 84, by + 76), (hx - 84, by + 90)); _arrow(d, (hx - 84, by + 76), (hx - 84, by + 90), 4)
    # a decaying tone: strike, fast fall, slow fall (illustrative)
    gx, gy, gw = 210, 250, 170
    d.line((gx, gy - 22), (gx, gy + 22)); d.line((gx, gy), (gx + gw, gy))
    pts = []
    for i in range(400):
        t = i / 399
        env = 0.55 * math.exp(-t * 18) + 0.45 * math.exp(-t * 2.4)
        pts.append((gx + t * gw, gy - 20 * env * math.sin(2 * math.pi * 26 * t)))
    d.line(*pts)
    d.text(bx + 94, tb_y - 14, 'TONE BAR', size=7)
    d.text(bx + 138, ty + 20, 'TUNING SPRING', size=7)
    d.text(bx + 160, ty - 14, 'TINE', size=7)
    d.text(px + 13, ty + 26, 'PICKUP', size=7)
    d.text(px + 49, ty - 46, 'TO AMP', size=7)
    d.text(hx + 20, ty + 40, 'HAMMER', size=7, anchor='start')
    d.text(bx - 6, by - 36, 'ROOT · TINE PRESSED IN', size=7)
    d.text(gx + gw / 2, gy + 34, 'STRIKE · DECAY (ILLUSTRATIVE)', size=7)
    d.text(110, 282, 'AFTER US PATENT 2,972,922', size=7)
    d.text(110, 292, 'H. B. RHODES, 1961', size=7)
    return d


PLATES = {
    'iron-frame': iron_frame,
    'player-piano': player_piano,
    'rhodes': rhodes,
}
