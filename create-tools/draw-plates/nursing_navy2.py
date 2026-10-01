"""Plates for the end of Keeping Watch's Navy nurses trail (sprint 030, part navy2). See plates_for.py."""
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


def _cross(d, cx, cy, s):
    """A Greek cross in outline, arms of width s/3 inside a square of side s."""
    a, b = s / 2, s / 6
    d.line((cx - b, cy - a), (cx + b, cy - a), (cx + b, cy - b), (cx + a, cy - b), (cx + a, cy + b),
           (cx + b, cy + b), (cx + b, cy + a), (cx - b, cy + a), (cx - b, cy + b), (cx - a, cy + b),
           (cx - a, cy - b), (cx - b, cy - b), closed=True)


def saigon_1964():
    d = D()
    # Station Hospital Saigon as Herman (2010) describes it, in section across the compound, a schematic
    # and not a survey: the five-storey main building on Tran Hung Dao, the five-storey annex behind it
    # joined by stairways, the one-storey block in the courtyard (central supply, emergency room,
    # operating room), and the perimeter wall with its wire grenade screen. The ambulances came from a
    # helicopter pad on a soccer field five minutes away.
    g = 214                                           # ground line
    fl = 24                                           # one storey
    mx, mw = 70, 92                                   # the main building
    ax, aw = 262, 70                                  # the annex
    cx, cw = 186, 52                                  # the courtyard block
    wl, wr, wh = 46, 352, 30                          # the walls and their height
    d.group('thin')
    d.line((14, g), (388, g))                         # ground
    for k in range(1, 6):                             # storey lines carried across
        d.line((mx - 6, g - k * fl), (ax + aw + 6, g - k * fl))
    d.line((mx + mw / 2, g + 10), (mx + mw / 2, g - 5 * fl - 14))  # the main building's axis
    d.group()
    _box(d, mx, g - 5 * fl, mw, 5 * fl)               # main building
    _box(d, ax, g - 5 * fl, aw, 5 * fl)               # annex
    d.line((mx - 4, g - 5 * fl), (mx + mw + 4, g - 5 * fl))   # roof slabs
    d.line((ax - 4, g - 5 * fl), (ax + aw + 4, g - 5 * fl))
    _box(d, cx, g - fl, cw, fl)                       # the courtyard block
    for x in (wl, wr):                                # perimeter walls
        _box(d, x - 3, g - wh, 6, wh)
    d.group('mid')
    for k in range(1, 5):                             # floors
        d.line((mx, g - k * fl), (mx + mw, g - k * fl))
        d.line((ax, g - k * fl), (ax + aw, g - k * fl))
    for k in range(5):                                # windows, three a floor in the main building, two in the annex
        y = g - k * fl - 17
        for j in range(3):
            _box(d, mx + 14 + j * 26, y, 12, 9)
        for j in range(2):
            _box(d, ax + 14 + j * 30, y, 12, 9)
    for k in range(1, 5):                             # the stairways joining main building and annex
        y0, y1 = g - k * fl, g - (k + 1) * fl + 6
        d.line((mx + mw, y0), (mx + mw + 14, y0), (ax - 14, y1), (ax, y1))
    for x in (wl, wr):                                # the grenade screen on each wall: posts and mesh
        top = g - wh
        d.line((x, top), (x, top - 22))
        for j in range(5):
            y = top - 4 - j * 4
            d.line((x - 4, y), (x + 4, y - 4))
            d.line((x - 4, y - 4), (x + 4, y))
    _box(d, cx + 8, g - fl + 6, 14, 18)               # the block's doors
    _box(d, cx + 30, g - fl + 6, 14, 18)
    d.group('mid')
    # the ambulance's way in: from the street, through the gate, to the emergency room
    # (dashed where it passes through the main building's ground floor)
    p0, p1, p2 = (6, g - 8), (wl - 6, g - 8), (cx + 4, g - 8)
    d.line(p0, p1)
    d.line((wl + 6, g - 8), (mx, g - 8))
    for k in range(0, int(mw), 8):
        d.line((mx + k, g - 8), (mx + min(k + 4, mw), g - 8))
    d.line((mx + mw, g - 8), p2)
    _arrow(d, (cx - 20, g - 8), p2)
    d.text(mx + mw / 2, g - 5 * fl - 22, 'WARDS · 100 BEDS', size=7)
    d.text(ax + aw / 2, g - 5 * fl - 22, 'ANNEX · ISOLATION', size=7)
    d.text(cx + cw / 2, g - fl - 8, 'ER · OR · SUPPLY', size=7)
    d.text(wl, g - wh - 30, 'SCREEN', size=7)
    d.text(26, g + 16, 'TRAN HUNG DAO', size=7, anchor='start')
    d.text(200, g + 36, 'AMBULANCES FROM THE HELICOPTER PAD · 5 MINUTES', size=7)
    d.text(200, g + 62, 'STATION HOSPITAL SAIGON · A SCHEMATIC', size=7)
    return d


def repose():
    d = D()
    # USS Repose (AH-16) in profile, from Herman (2010) and DANFS: a Haven-class hull of 520 feet on a
    # C-4 cargo design, eight decks with three below the waterline, the machinery aft so that the
    # hospital is one unit forward, the surgical suite amidships where the ship moves least, wards on
    # the three decks above the waterline, the helicopter deck aft and triage beside it, reached by a
    # sloping ramp; three red crosses along the hull and one (of four) on the funnel. The length is to
    # scale (0.68 px a foot); the decks and superstructure are a schematic.
    L = 520.0
    x0, x1 = 22, 376                                   # bow, stern
    s = (x1 - x0) / L
    top, wl, keel = 160, 196, 222                      # upper deck, waterline, keel
    rake = 24                                          # the bow's rake, from upper deck to keel
    bowx = lambda y: x0 + (y - (top - 8)) / (keel - (top - 8)) * rake
    mid = (x0 + x1) / 2
    d.group('thin')
    d.line((8, wl), (392, wl))                         # the waterline, carried past the hull
    for k in range(11):                                # stations every 52 feet
        x = x0 + k * 52 * s
        d.line((x, keel + 6), (x, keel + 12))
    d.line((x0, keel + 9), (x1, keel + 9))             # the length, dimensioned
    d.line((mid, 70), (mid, keel + 4))                 # amidships
    d.group()
    # the hull: a raked bow rising to a short forecastle sheer, a rounded stern
    d.line((x0, top - 8), (x0 + 34, top), (x1, top))
    d.line((x0, top - 8), (bowx(keel), keel), (x1 - 16, keel))
    d.line(*[(x1 - 16 + 16 * math.cos(math.radians(a)), keel - 16 + 16 * math.sin(math.radians(a)))
             for a in range(90, -1, -15)], (x1, top))
    # the superstructure, two decks, and the funnel aft over the machinery
    sx0, sx1 = 96, 298
    d.line((sx0, top), (sx0, 142), (sx1, 142), (sx1, top))
    d.line((sx0 + 18, 142), (sx0 + 18, 126), (sx1 - 44, 126), (sx1 - 44, 142))
    fx = 282
    d.line((fx - 12, 142), (fx - 10, 98), (fx + 10, 98), (fx + 12, 142))
    # the helicopter deck aft, over the stern, on its pillars
    hd = 144
    d.line((sx1, hd), (x1 + 6, hd))
    d.line((sx1, hd + 3), (x1 + 6, hd + 3))
    for x in (sx1 + 40, x1 - 4):
        d.line((x, hd + 3), (x, top))
    d.group('mid')
    for y in (172, 184, 205, 214):                     # decks inside the hull (the waterline is a third)
        d.line((bowx(y) + 2, y), (x1 - (2 if y < 200 else 6), y))
    _box(d, 236, wl, 90, keel - wl)                    # machinery spaces, aft and below
    for y in (166, 178, 190):                          # the wards' portholes, forward, on three decks
        for i in range(6):
            d.circle(68 + i * 18, y, 1.6)
    _box(d, mid - 22, 172, 44, 12)                     # the surgical suite, amidships
    _box(d, sx1 + 3, hd + 3, 34, top - hd - 3)         # triage, beside the deck
    d.line((x1 - 6, hd + 3), (sx1 + 40, top - 2))      # the ramp down from the deck
    _arrow(d, (x1 - 6, hd + 3), (sx1 + 40, top - 2))
    for cx_ in (44, mid, 336):                         # red crosses along the hull
        _cross(d, cx_, 166 if cx_ == mid else 178, 10)
    _cross(d, fx, 116, 12)                             # and on the funnel
    # a helicopter coming in over the stern
    hx, hy = 360, 104
    d.line((hx - 22, hy - 9), (hx + 22, hy - 9))       # rotor
    d.line((hx, hy - 9), (hx, hy - 5))
    d.ellipse(hx, hy, 11, 5.5)
    d.line((hx - 11, hy - 1), (hx - 34, hy - 4))       # tail boom
    d.line((hx - 34, hy - 8), (hx - 34, hy))
    _arrow(d, (hx, hy + 10), (hx, hd - 6))
    d.line((hx, hy + 10), (hx, hd - 6))
    d.group('mid')
    for (lx, ly), (tx, ty) in (((77, 178), (77, 92)), ((mid + 16, 172), (mid + 16, 84)), ((310, 152), (310, 76))):
        d.line((lx, ly), (tx, ty + 4))                 # leaders to the labels
    d.text(77, 88, 'WARDS', size=7)
    d.text(mid + 16, 80, 'OR', size=7)
    d.text(310, 72, 'TRIAGE', size=7)
    d.text(281, 211, 'ENGINES', size=7)
    d.text(10, wl - 3, 'WL', size=7, anchor='start')
    d.text(mid, keel + 22, '520 FT', size=7)
    d.text(200, 272, 'USS REPOSE (AH-16) · PROFILE · SCHEMATIC', size=7)
    return d


def duerk():
    d = D()
    # Alene Duerk's career on its years, from the Navy's official biography: every posting as a bar on a
    # time axis from 1940 to 1976 (9.8 px a year), stepping down the plate as she moved, with the years
    # out of uniform (June 1946 to June 1951) left as a gap; above, the three grades the sources date
    # (ensign 1943, captain 1967, rear admiral 1972), joined by a dashed line, since the steps between
    # are not given.
    y0, y1 = 1940, 1976
    x0, x1 = 34, 386
    X = lambda yr: x0 + (yr - y0) / (y1 - y0) * (x1 - x0)
    base = 252                                         # the time axis
    posts = [  # (start, end) in years, as the biography gives them
        (1943.2, 1944.0), (1944.0, 1945.4), (1945.4, 1946.0), (1946.0, 1946.5),     # Portsmouth, Bethesda, Benevolence, Great Lakes
        (1951.45, 1951.7), (1951.7, 1956.8), (1956.8, 1958.45), (1958.45, 1961.4),  # Portsmouth, Corps School, Philadelphia, Chicago
        (1961.4, 1962.3), (1962.3, 1963.4), (1963.4, 1965.45), (1965.45, 1966.4),   # Subic Bay, Yokosuka, Long Beach, San Diego
        (1966.4, 1967.4), (1967.4, 1968.15), (1968.15, 1970.4), (1970.4, 1975.5),  # Washington, BUPERS, Great Lakes, Director
    ]
    d.group('thin')
    for yr in range(1940, 1977, 5):                    # year lines
        d.line((X(yr), 70), (X(yr), base))
    for y in (92, 56, 32):                             # the three dated grades' levels
        d.line((x0, y), (x1, y))
    d.group()
    d.line((x0, base), (x1, base))                     # the axis
    for yr in range(1940, 1977, 5):
        d.line((X(yr), base), (X(yr), base + 5))
    # the postings, stepping down as she moved
    for i, (a, b) in enumerate(posts):
        y = 116 + i * 7.6
        d.line((X(a), y), (X(b), y))
        d.line((X(a), y - 2.5), (X(a), y + 2.5))
    d.group('mid')
    # the gap, out of uniform
    xa, xb = X(1946.5), X(1951.45)
    for k in range(int((xb - xa) / 6)):
        if k % 2 == 0:
            d.line((xa + k * 6, 142.6), (min(xa + k * 6 + 6, xb), 142.6))
    for x in (xa, xb):
        d.line((x, 139), (x, 146))
    # the three dated grades, and the dashed path between them
    pts = [(X(1943.06), 92), (X(1967.5), 56), (X(1972.42), 32)]   # 23 Jan 1943, 1 Jul 1967, 1 Jun 1972
    for p in pts:
        d.circle(p[0], p[1], 3)
    for (ax_, ay), (bx, by) in zip(pts, pts[1:]):      # dashes along each leg
        n = int(math.hypot(bx - ax_, by - ay) / 8)
        for k in range(0, n, 2):
            t0, t1 = k / n, (k + 1) / n
            d.line((ax_ + (bx - ax_) * t0, ay + (by - ay) * t0), (ax_ + (bx - ax_) * t1, ay + (by - ay) * t1))
    d.group('mid')
    for yr in range(1940, 1977, 10):
        d.text(X(yr), base + 16, str(yr), size=7)
    d.text(X(1943.06) + 6, 102, 'ENSIGN 1943', size=7, anchor='start')
    d.text(X(1967.5) - 6, 52, 'CAPTAIN 1967', size=7, anchor='end')
    d.text(X(1972.42) - 6, 28, 'REAR ADMIRAL 1972', size=7, anchor='end')
    d.text(X(1946.9), 136, 'OUT OF UNIFORM', size=7, anchor='start')
    d.text(X(1945.4) - 6, 133.5, 'BENEVOLENCE', size=7, anchor='end')
    d.text(X(1973), 242, 'DIRECTOR', size=7)
    d.text(200, 288, 'ALENE DUERK · POSTINGS 1943–75', size=7)
    return d


PLATES = {
    'saigon-1964': saigon_1964,
    'repose': repose,
    'duerk': duerk,
}
