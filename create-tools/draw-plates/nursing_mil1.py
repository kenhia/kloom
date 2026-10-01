"""Plates for the start of Keeping Watch's Nurses at war (sprint 030, part mil1). See plates_for.py."""
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


def _oak_leaf(cx, cy, length, width, lobes=4, tilt=-90, n=160):
    """An oak leaf's outline: a lanceolate blade whose half-width is modulated by |sin| lobes,
    so each side has `lobes` rounded lobes with sinuses between them. Returns the points, with the
    leaf's axis along `tilt` degrees from its base at (cx, cy)."""
    pts = []
    for side in (1, -1):
        rng = range(n + 1) if side == 1 else range(n, -1, -1)
        for i in rng:
            t = i / n                                                   # 0 at the base, 1 at the tip
            blade = math.sin(math.pi * t ** 0.85)                       # the blade's envelope
            lobe = 0.55 + 0.45 * abs(math.sin(math.pi * lobes * t))     # lobes and sinuses
            u = length * t
            v = side * 0.5 * width * blade * lobe
            a = math.radians(tilt)
            x = cx + u * math.cos(a) - v * math.sin(a)
            y = cy + u * math.sin(a) + v * math.cos(a)
            pts.append((x, y))
    return pts


def sacred_twenty():
    d = D()
    # Left: the Corps pin of 1908 as Hasson described it in January 1909, "about the size of a silver
    # quarter" (24.26 mm), an anchor combined with a caduceus over the letters U.S.N., drawn at about
    # 5 px to the mm on its centre lines. Right: the collar device, the gold oak leaf, with the
    # Medical Corps' silver acorn faint (worn with NNC, 1918-47) and the leaf alone (from 1947).
    cx, cy, R = 120, 138, 24.26 / 2 * 5.2
    d.group('thin')
    d.circle(cx, cy, R)
    d.line((cx - R - 16, cy), (cx + R + 16, cy))
    d.line((cx, cy - R - 16), (cx, cy + R + 16))
    d.line((cx - R, cy + R + 22), (cx + R, cy + R + 22))                 # the diameter, dimensioned
    d.line((cx - R, cy + R + 16), (cx - R, cy + R + 28))
    d.line((cx + R, cy + R + 16), (cx + R, cy + R + 28))
    lx, ly = 290, 222                                                    # the leaf's base
    d.line((lx, ly + 10), (lx, 50))                                      # its axis
    for k in range(1, 5):                                                # the lobes' stations
        y = ly - 150 * k / 4.4
        d.line((lx - 48, y), (lx + 48, y))
    d.group()
    d.circle(cx, cy, R)
    d.circle(cx, cy, R - 5)
    # the anchor: shank, stock, crown arc and flukes
    top, bot = cy - R + 14, cy + R - 22
    d.line((cx, top), (cx, bot))
    d.circle(cx, top - 4, 4)
    d.line((cx - 16, top + 7), (cx + 16, top + 7))
    d.arc(cx, bot - 20, 22, 20, 160)
    for s in (-1, 1):
        x, y = _pt(cx, bot - 20, 22, 90 - s * 70)
        _arrow(d, (cx, bot - 20), (x, y), size=7)
    d.group('mid')
    # the caduceus over the shank: two serpents as phase-shifted sines, and the wings
    s1, s2 = [], []
    for i in range(41):
        y = top + 12 + i * (bot - top - 26) / 40
        w = 9 * math.sin(i / 40 * 3 * math.pi)
        s1.append((cx + w, y))
        s2.append((cx - w, y))
    d.line(*s1)
    d.line(*s2)
    for s in (-1, 1):
        d.line((cx, top + 10), (cx + s * 12, top + 2), (cx + s * 26, top - 4), (cx + s * 20, top + 4), (cx + s * 8, top + 10))
    # the oak leaf and its veins
    leaf = _oak_leaf(lx, ly, 160, 92, lobes=4)
    d.group()
    d.line(*leaf, closed=True)
    d.line((lx, ly + 10), (lx, ly - 150))
    d.group('mid')
    for k in range(4):
        t = (k + 0.5) / 4
        y0 = ly - 160 * t
        for s in (-1, 1):
            d.line((lx, y0 + 10), (lx + s * 30, y0 - 6))
    d.group('thin')                                                      # the acorn of 1918-47
    d.ellipse(lx + 62, ly - 8, 9, 12)
    d.arc(lx + 62, ly - 12, 10, 180, 360)
    d.line((lx + 62, ly - 22), (lx + 62, ly - 27))
    d.group('mid')
    d.text(cx, cy + R + 40, 'ABOUT 24 MM · A QUARTER', size=7)
    d.text(cx, cy + R + 52, 'THE PIN, 1908', size=7)
    d.text(cx, cy + R - 10, 'U.S.N.', size=7)
    d.text(lx + 62, ly + 16, 'ACORN 1918–47', size=7)
    d.text(lx - 10, ly + 30, 'THE OAK LEAF, 1947', size=7)
    return d


def civil_war_nurses():
    d = D()
    # A general hospital ward by the Surgeon General's circular of 14 July 1862: one nurse to every
    # ten beds, one woman nurse to two men. Thirty beds in two rows along the long walls of a ward
    # 30 m by 7.5 m (a schematic, not a survey), two stoves on the axis, and the three nurses it
    # allows placed at their sections, the woman's marked W.
    x0, y0, L, B = 30, 70, 340, 120
    beds = 15
    pitch = L / beds
    d.group('thin')
    d.line((x0 - 10, y0 + B / 2), (x0 + L + 10, y0 + B / 2))            # the ward's axis
    for k in (1, 2):                                                     # sections of ten beds
        x = x0 + k * L / 3
        d.line((x, y0 - 14), (x, y0 + B + 14))
    for k in range(beds + 1):
        x = x0 + k * pitch
        d.line((x, y0), (x, y0 + 6))
        d.line((x, y0 + B), (x, y0 + B - 6))
    d.group()
    _box(d, x0, y0, L, B)
    d.line((x0 - 6, y0 + B / 2 - 9), (x0, y0 + B / 2 - 9))               # the door
    d.line((x0 - 6, y0 + B / 2 + 9), (x0, y0 + B / 2 + 9))
    d.group('mid')
    for k in range(beds):
        x = x0 + k * pitch + 3
        _box(d, x, y0 + 3, pitch - 6, 34)
        _box(d, x, y0 + B - 37, pitch - 6, 34)
        d.line((x + 2, y0 + 9), (x + pitch - 8, y0 + 9))                 # pillows
        d.line((x + 2, y0 + B - 9), (x + pitch - 8, y0 + B - 9))
    for k in (1, 2):                                                     # stoves
        d.circle(x0 + k * L / 3, y0 + B / 2, 6)
    d.group()
    marks = ['W', 'M', 'M']
    for k, m in enumerate(marks):
        x = x0 + (k + 0.5) * L / 3
        d.circle(x, y0 + B / 2, 9)
    d.group('mid')
    for k, m in enumerate(marks):
        x = x0 + (k + 0.5) * L / 3
        d.text(x, y0 + B / 2 + 3, m, size=7)
        d.text(x, y0 + B + 28, '10 BEDS', size=7)
    d.text(200, 50, '30 BEDS · 3 NURSES · 1 WOMAN TO 2 MEN', size=7)
    d.text(200, 238, 'A WARD BY THE CIRCULAR OF 14 JULY 1862 · SCHEMATIC', size=7)
    return d


def army_nurse_corps():
    d = D()
    # The Brand bath for typhoid as Isabel Hampton gave it in 1893. Left: the portable tub in section,
    # two-thirds full of water at 70 F, the head on a ring at the raised end. Right: a fever chart
    # with readings every three hours over two days, the line at 102.5 F above which a bath was
    # ordered, and a mark at each bath. The readings are invented, to show the rule.
    tx, ty, tw, th = 24, 120, 150, 62                                    # the tub's rim
    d.group('thin')
    d.line((tx - 6, ty + th * (1 - 2 / 3)), (tx + tw + 6, ty + th * (1 - 2 / 3)))   # water line, 2/3 full
    gx, gy, gw, gh = 210, 60, 170, 170                                   # the chart
    tmin, tmax = 98, 106
    Y = lambda t: gy + gh - (t - tmin) / (tmax - tmin) * gh
    for t in range(tmin, tmax + 1):
        d.line((gx, Y(t)), (gx + gw, Y(t)))
    for k in range(17):
        x = gx + k * gw / 16
        d.line((x, gy), (x, gy + gh))
    d.group()
    # the tub: a trough wider at the rim, a higher head end, on four wheels
    d.line((tx, ty), (tx + 14, ty + th), (tx + tw - 22, ty + th), (tx + tw, ty - 12), closed=False)
    d.line((tx, ty), (tx + tw, ty - 12))
    for wx in (tx + 30, tx + tw - 40):
        d.circle(wx, ty + th + 10, 9)
    d.circle(tx + tw - 10, ty - 6, 6)                                    # the head ring
    _box(d, gx, gy, gw, gh)
    temps = [101.2, 102.0, 103.1, 101.6, 102.2, 103.4, 101.8, 102.4, 102.9,
             101.4, 101.9, 102.7, 101.2, 101.6, 102.1, 101.0, 100.8]
    pts = [(gx + k * gw / 16, Y(t)) for k, t in enumerate(temps)]
    d.line(*pts)
    d.group('mid')
    d.line((gx, Y(102.5)), (gx + gw, Y(102.5)))
    for (x, y), t in zip(pts, temps):
        d.circle(x, y, 2)
        if t > 102.5:
            d.line((x, y + 4), (x, Y(102.5) + 18))
            _arrow(d, (x, y + 4), (x, Y(102.5) + 18), size=4)
    d.text(tx + tw / 2 - 4, ty + 44, 'WATER 70 °F', size=7)
    d.text(tx + tw / 2, ty + th + 34, 'THE TUB · 2/3 FULL', size=7)
    d.text(gx - 4, Y(102.5) + 3, '102.5', size=7, anchor='end')
    d.text(gx - 4, Y(104) + 3, '104', size=7, anchor='end')
    d.text(gx - 4, Y(100) + 3, '100', size=7, anchor='end')
    d.text(gx + gw / 2, gy + gh + 14, 'EVERY 3 HOURS · 2 DAYS', size=7)
    d.text(gx + gw / 2, gy - 8, 'BATH ABOVE 102.5 °F · INVENTED READINGS', size=7)
    return d


PLATES = {
    'sacred-twenty': sacred_twenty,
    'civil-war-nurses': civil_war_nurses,
    'army-nurse-corps': army_nurse_corps,
}
