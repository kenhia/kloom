"""Plates for Keeping Watch's trail Navy nurses, part navy1 (sprint 030): hospital ships, the
prisoners of war, and commissioned rank. See plates_for.py."""
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
    """A Greek cross of arm length s from the centre, its arms s/3 wide, as one outline."""
    w = s / 3
    d.line((cx - w, cy - s), (cx + w, cy - s), (cx + w, cy - w), (cx + s, cy - w), (cx + s, cy + w),
           (cx + w, cy + w), (cx + w, cy + s), (cx - w, cy + s), (cx - w, cy + w), (cx - s, cy + w),
           (cx - s, cy - w), (cx - w, cy - w), closed=True)


def hospital_ships():
    d = D()
    # A Haven-class hospital ship (520 ft overall, 71 ft 6 in beam, 24 ft draft) as a schematic, in
    # profile above and in plan below, to one scale: 340 px for 520 ft. The superstructure is
    # simplified; what is drawn to the conventions is the marking: a white hull with red crosses on
    # its sides and on its horizontal surfaces (Geneva II, 1949, art. 43), and the helicopter deck
    # aft, 60 ft long, fitted to Consolation in 1951.
    x0, L = 30, 340.0
    s = L / 520                                                            # px per foot
    wl, keel = 118, 118 + 24 * s                                           # waterline and keel, profile
    deck = wl - 19 * s                                                     # main deck at its lowest
    cy = 232                                                               # plan centreline
    hb = 71.5 / 2 * s                                                      # half-beam in the plan

    def sheer(x):                                                          # deck line, rising to the bow
        u = (x - x0) / L
        return deck - 10 * s * (1 - u) ** 2 - 22 * s * u ** 3

    d.group('thin')
    d.line((x0 - 14, wl), (x0 + L + 14, wl))                               # waterline
    d.line((x0 - 14, keel), (x0 + L + 14, keel))                           # baseline
    for k in range(11):                                                    # stations every 52 ft
        x = x0 + k * L / 10
        d.line((x, deck - 50), (x, keel + 4))
        d.line((x, cy - hb - 6), (x, cy + hb + 6))
    d.line((x0 - 14, cy), (x0 + L + 14, cy))                               # plan centreline
    d.line((x0, 286), (x0 + L, 286))                                       # scale, 0 to 520 ft
    for k in range(11):
        d.line((x0 + k * L / 10, 283), (x0 + k * L / 10, 289))
    d.group()
    # profile: counter stern at left, raked bow at right
    pts = [(x0 + L * i / 40, sheer(x0 + L * i / 40)) for i in range(41)]
    bow_top = pts[-1]
    hull = [(x0 + 4, keel - 6)] + [(x0, sheer(x0) + 2)] + pts + [(x0 + L - 18, keel), (x0 + 10, keel)]
    d.line(*hull, closed=True)
    # superstructure amidships: three tiers, a funnel and two masts
    yb = max(sheer(x0 + 0.30 * L), sheer(x0 + 0.78 * L))                  # the superstructure's foot
    t1, t2, t3 = yb - 9, yb - 17, yb - 24
    d.line((x0 + 0.30 * L, sheer(x0 + 0.30 * L)), (x0 + 0.30 * L, t1), (x0 + 0.78 * L, t1), (x0 + 0.78 * L, sheer(x0 + 0.78 * L)))
    _box(d, x0 + 0.36 * L, t2, 0.36 * L, 8)
    _box(d, x0 + 0.50 * L, t3, 0.18 * L, 7)
    fx = x0 + 0.44 * L
    d.line((fx, t2), (fx + 3, t2 - 22), (fx + 19, t2 - 22), (fx + 18, t2))   # funnel
    d.line((x0 + 0.86 * L, sheer(x0 + 0.86 * L)), (x0 + 0.86 * L, deck - 52))   # foremast
    d.line((x0 + 0.24 * L, sheer(x0 + 0.24 * L)), (x0 + 0.24 * L, deck - 46))   # mainmast
    # helicopter deck aft: 60 ft, raised one deck over the stern
    hx1, hx2, hy = x0 + 2, x0 + 2 + 60 * s, deck - 9
    d.line((hx1, hy), (hx2, hy))
    d.line((hx1 + 3, hy), (hx1 + 3, sheer(hx1 + 3)))
    d.line((hx2 - 3, hy), (hx2 - 3, sheer(hx2 - 3)))
    # plan: the hull's waterplane, fine at the bow, full aft
    top, bot = [], []
    for i in range(41):
        u = i / 40
        x = x0 + L * u
        w = hb * (1 - max(0, (u - 0.62) / 0.38) ** 1.8) ** 0.55 * (0.82 + 0.18 * min(1, u / 0.12))
        top.append((x, cy - w))
        bot.append((x, cy + w))
    d.line(*(top + bot[::-1]), closed=True)
    d.group('mid')
    # the crosses, as large as the surface allows: on the hull side, the funnel, and the decks
    _cross(d, x0 + 0.58 * L, (deck + wl) / 2 + 0.5, 4.2)
    _cross(d, x0 + 0.14 * L, (sheer(x0 + 0.14 * L) + wl) / 2 + 1, 4.2)
    _cross(d, fx + 10, t2 - 11, 5)
    _cross(d, x0 + 0.56 * L, cy, 11)
    _cross(d, x0 + 0.82 * L, cy, 9)
    # the helicopter deck in plan, with its landing circle
    _box(d, hx1, cy - hb + 2, 60 * s, 2 * hb - 4)
    d.circle(hx1 + 30 * s, cy, 10)
    # the superstructure's outline in plan
    _box(d, x0 + 0.30 * L, cy - hb + 5, 0.48 * L, 2 * hb - 10)
    # a helicopter's approach to the deck, and a boat's to the side
    hc = hx1 + 30 * s                                                       # the deck's centre
    path = [_pt(hc + 44, deck - 40, 44, a) for a in range(-60, -181, -6)]
    d.line(*path)
    d.line((hc, deck - 40), (hc, hy - 4))
    _arrow(d, (hc, hy - 20), (hc, hy - 4))
    d.line((x0 + 0.5 * L, wl + 30), (x0 + 0.5 * L, wl + 6))
    _arrow(d, (x0 + 0.5 * L, wl + 20), (x0 + 0.5 * L, wl + 6))
    d.group('mid')
    d.text(x0 + L + 4, wl - 3, 'WL', size=7, anchor='start')
    d.text(hc + 72, deck - 76, 'HELO DECK · 60 FT', size=7, anchor='start')
    d.text(x0 + 0.5 * L, wl + 40, 'BOATS ALONGSIDE', size=7)
    d.text(x0 + L / 2, 298, '0 · 520 FT · HAVEN CLASS · SCHEMATIC', size=7)
    return d


def _dashed(d, p, q, dash=4, gap=3):
    """A dashed line from p to q, as many short strokes in one path."""
    L = math.dist(p, q)
    n = max(1, int(L // (dash + gap)))
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    segs = []
    for i in range(n + 1):
        a = i * (dash + gap)
        b = min(L, a + dash)
        if a >= L:
            break
        segs.append([(p[0] + ux * a, p[1] + uy * a), (p[0] + ux * b, p[1] + uy * b)])
    d.lines(segs)


def navy_pow():
    d = D()
    # The raid on Los Banos, 23 February 1945, as a schematic of its four parts (not to scale; the
    # ground is simplified from the published accounts): the amphibious tractors cross Laguna de Bay
    # from Mamatid to Mayondon Point and drive about two miles overland to the camp; nine aircraft in
    # three Vs drop a company beside the camp at 07:00; guerrillas and the reconnaissance platoon close
    # on the guard posts round the wire; a task force down Highway 1 holds the San Juan River crossing.
    d.group('thin')
    # the lake shore, a computed curve from upper right to lower left
    shore = [(400 - 400 * u, 40 + 70 * u + 22 * math.sin(math.pi * u)) for u in [i / 40 for i in range(41)]]
    for k in range(1, 4):                                                   # depth hatching on the lake
        d.line(*[(x, y - 14 * k) for x, y in shore if y - 14 * k > 8])
    cx, cy, w, h = 262, 186, 96, 64                                         # the camp
    for a in range(0, 360, 30):                                             # guard posts on a ring
        d.line(_pt(cx, cy, 70, a), _pt(cx, cy, 86, a))
    d.circle(cx, cy, 86)
    d.group()
    d.line(*shore)
    # the camp: a double fence of wire, with barbs
    _box(d, cx - w / 2, cy - h / 2, w, h)
    _box(d, cx - w / 2 - 5, cy - h / 2 - 5, w + 10, h + 10)
    # Highway 1 and the San Juan River
    d.line((20, 268), (390, 250))
    river = [(92 + 9 * math.sin(i / 3), 226 + i * 3.6) for i in range(21)]
    d.line(*river)
    d.group('mid')
    for i in range(12):                                                     # barbs on the wire
        x = cx - w / 2 - 5 + (w + 10) * (i + 0.5) / 12
        d.line((x - 2, cy - h / 2 - 7), (x + 2, cy - h / 2 - 3))
        d.line((x - 2, cy + h / 2 + 3), (x + 2, cy + h / 2 + 7))
    # barracks inside, and the hospital
    for i in range(5):
        _box(d, cx - 40 + i * 17, cy - 24, 11, 26)
    _box(d, cx + 18, cy + 10, 24, 14)
    _cross(d, cx + 30, cy + 17, 4)
    # the drop zone beside the camp, and nine aircraft in three Vs
    dz = (cx - 120, cy + 4)
    d.circle(*dz, 18)
    for v, (vx, vy) in enumerate([(dz[0] - 70, dz[1] - 70), (dz[0] - 40, dz[1] - 86), (dz[0] - 100, dz[1] - 54)]):
        for j, (ox, oy) in enumerate([(0, 0), (-9, -6), (-6, 9)]):
            x, y = vx + ox, vy + oy
            d.line((x - 4, y - 3), (x, y), (x - 4, y + 3))
    _arrow(d, (dz[0] - 40, dz[1] - 40), (dz[0] - 14, dz[1] - 14))
    d.line((dz[0] - 40, dz[1] - 40), (dz[0] - 14, dz[1] - 14))
    # the tractors' route: Mamatid across the lake to Mayondon Point, then overland to the gate
    mam = (40, 30)
    may = shore[14]
    _dashed(d, mam, may)
    _arrow(d, mam, may)
    gate = (cx - w / 2 - 5, cy - 10)
    _dashed(d, may, gate)
    _arrow(d, may, gate)
    # the diversion down the highway to the river
    _arrow(d, (330, 254), (108, 265))
    d.group('mid')
    d.text(150, 20, 'LAGUNA DE BAY', size=7)
    d.text(mam[0] + 6, mam[1] - 6, 'MAMATID', size=7, anchor='start')
    d.text(may[0] + 8, may[1] + 14, 'MAYONDON PT', size=7, anchor='start')
    d.text(dz[0], dz[1] + 30, 'DROP ZONE', size=7)
    d.text(cx, cy + h / 2 + 20, 'CAMP · HOSPITAL', size=7)
    d.text(330, 244, 'HIGHWAY 1', size=7)
    d.text(104, 236, 'SAN JUAN R.', size=7, anchor='start')
    d.text(380, 296, 'SCHEMATIC', size=7, anchor='end')
    return d


def nurse_rank():
    d = D()
    # Left: the Navy's sleeve stripes for each rank from ensign to rear admiral, drawn to their widths
    # (1/2-inch stripes, 1/4-inch for the half stripe, a 2-inch stripe for flag rank, 1/4-inch gaps),
    # at 6 px to the inch. Middle: the highest rank the law let a Navy nurse hold, by year, as relative
    # rank (dashed) and as rank (solid). Right: the 1947 act's pyramid, a triangle cut so that the
    # top slices hold 0.7 and 1.6 per cent of its area (cut at the square roots of 0.007 and 0.023).
    ranks = ['ENS', 'LTJG', 'LT', 'LCDR', 'CDR', 'CAPT', 'RADM']
    stripes = [['W'], ['W', 'N'], ['W', 'W'], ['W', 'N', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W', 'W'], ['B', 'W']]
    u = 6.0                                                                 # px per inch
    size = {'W': 0.5 * u, 'N': 0.25 * u, 'B': 2 * u}
    y0, dy = 252, 32                                                        # ensign's rung, rung spacing
    rung = lambda i: y0 - i * dy
    X0, X1 = 92, 292                                                        # years 1908 to 1972
    bp = [(1908, X0), (1942, 140), (1948, 220), (1967, 250), (1972, X1)]   # a broken time axis
    def yx(yr):
        for (a, xa), (b, xb) in zip(bp, bp[1:]):
            if yr <= b:
                return xa + (yr - a) * (xb - xa) / (b - a)
        return X1
    none = y0 + 22                                                          # below the ladder: no rank
    d.group('thin')
    for i in range(len(ranks)):
        d.line((X0 - 6, rung(i)), (X1 + 4, rung(i)))
    d.line((X0 - 6, none), (X1 + 4, none))
    for yr in (1908, 1942, 1944, 1947, 1967, 1972):
        d.line((yx(yr), 26), (yx(yr), none + 6))
    # the pyramid's construction: its axis
    px, ptop, pbase, phw = 350, 70, 262, 38
    d.line((px, ptop - 8), (px, pbase + 6))
    d.group()
    # the stripes, each a sleeve band 30 px long, built up from the cuff
    for i, st in enumerate(stripes):
        y = rung(i) + 7
        for s in st:
            hgt = size[s]
            _box(d, 16, y - hgt, 30, hgt)
            y -= hgt + 0.25 * u
    # the ceiling over a Navy nurse: no rank to July 1942
    d.line((yx(1908), none), (yx(1942.5), none))
    # relative rank: lieutenant commander from July 1942, captain for the superintendent from December
    _dashed(d, (yx(1942.5), none), (yx(1942.5), rung(3)))
    _dashed(d, (yx(1942.5), rung(3)), (yx(1942.97), rung(3)))
    _dashed(d, (yx(1942.97), rung(3)), (yx(1942.97), rung(5)))
    _dashed(d, (yx(1942.97), rung(5)), (yx(1944.15), rung(5)))
    # rank: temporary from February 1944, permanent from April 1947 (commander; the Director a captain
    # while she serves), the ceilings lifted in November 1967, rear admiral in 1972
    d.line((yx(1944.15), rung(5)), (yx(1947.3), rung(5)), (yx(1947.3), rung(4)), (yx(1967.85), rung(4)),
           (yx(1967.85), rung(5)), (yx(1972), rung(5)), (yx(1972), rung(6)))
    _dashed(d, (yx(1947.3), rung(5)), (yx(1967.85), rung(5)), dash=2, gap=3)   # the Director's captaincy
    # the pyramid, cut at sqrt(0.007) and sqrt(0.023) of its height
    H = pbase - ptop
    d.line((px, ptop), (px + phw, pbase), (px - phw, pbase), closed=True)
    d.group('mid')
    for f in (0.007, 0.023):
        y = ptop + math.sqrt(f) * H
        hw = phw * math.sqrt(f)
        d.line((px - hw, y), (px + hw, y))
    for yr in (1942, 1944, 1947, 1967):
        d.circle(yx(yr + (0.5 if yr == 1942 else 0.15 if yr == 1944 else 0.3 if yr == 1947 else 0.85)), rung(5) if yr != 1942 else rung(3), 2)
    d.group('mid')
    for i, r in enumerate(ranks):
        d.text(X0 - 10, rung(i) + 3, r, size=7, anchor='end')
    d.text(X0 - 10, none + 3, 'NONE', size=7, anchor='end')
    for yr in (1908, 1942, 1944, 1947, 1967, 1972):
        d.text(yx(yr), 20, str(yr), size=7)
    d.text(px, ptop - 24, 'CDR 0.7%', size=7)
    d.text(px, ptop - 14, 'LCDR 1.6%', size=7)
    d.text(px, pbase + 18, '1947 CEILING', size=7)
    return d


PLATES = {
    'hospital-ships': hospital_ships,
    'navy-pow': navy_pow,
    'nurse-rank': nurse_rank,
}
