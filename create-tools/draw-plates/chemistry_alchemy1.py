"""Plates for the chemistry subject's segment Elements and alchemy, part alchemy1 (sprint 025):
the four elements, Alexandrian alchemy and iron gall ink."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _offset(a, b, c, k=3.2):
    """A second, shorter line inside a double bond ab, on the side of point c (a ring's centre)."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = c[0] - mx, c[1] - my
    n = math.hypot(dx, dy)
    ox, oy = dx / n * k, dy / n * k
    t = 0.18
    return [(a[0] + (b[0] - a[0]) * t + ox, a[1] + (b[1] - a[1]) * t + oy),
            (a[0] + (b[0] - a[0]) * (1 - t) + ox, a[1] + (b[1] - a[1]) * (1 - t) + oy)]


def _parallel(a, b, k=3.2):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * k, dx / n * k
    return [[(a[0] + ox / 2, a[1] + oy / 2), (b[0] + ox / 2, b[1] + oy / 2)],
            [(a[0] - ox / 2, a[1] - oy / 2), (b[0] - ox / 2, b[1] - oy / 2)]]


def _arrowhead(tip, a, size=5, spread=26):
    """Two short strokes making an arrowhead at `tip`, pointing in direction `a` (degrees)."""
    return [[_pt(tip, a + 180 - spread, size), tip, _pt(tip, a + 180 + spread, size)]]


def four_elements():
    """Aristotle's square of qualities, beside a Hofmann voltameter splitting water two volumes to one."""
    d = D()
    c, s = (108, 138), 60                       # the square's centre and half-side
    corners = {'HOT': (c[0] - s, c[1] - s), 'DRY': (c[0] + s, c[1] - s),
               'COLD': (c[0] + s, c[1] + s), 'WET': (c[0] - s, c[1] + s)}
    mids = {'FIRE': (c[0], c[1] - s), 'EARTH': (c[0] + s, c[1]),
            'WATER': (c[0], c[1] + s), 'AIR': (c[0] - s, c[1])}
    # the voltameter: two gas tubes and the reservoir between them
    xs = {'H': 262, 'O': 338}
    top, bot, w, unit = 64, 212, 9, 40          # tube top and bottom, half-width, one volume of gas
    rx = 300
    d.group('thin')
    d.circle(*c, s * math.sqrt(2))
    d.line(corners['HOT'], corners['COLD'])
    d.line(corners['DRY'], corners['WET'])
    for y in (top, top + unit, top + 2 * unit):      # the gas levels, one volume apart
        d.line((xs['H'] - 22, y), (xs['O'] + 22, y))
    d.line((rx, 30), (rx, 262))
    d.group()
    d.line(*corners.values(), closed=True)
    for x in xs.values():
        d.line((x - w, top - 8), (x - w, bot), (x + w, bot))
        d.line((x + w, bot), (x + w, top - 8))
        d.arc(x, top - 8, w, 180, 360, n=16)
    d.line((xs['H'] + w, bot - 14), (rx - 6, bot - 14), (rx - 6, 62))
    d.line((xs['O'] - w, bot - 14), (rx + 6, bot - 14), (rx + 6, 62))
    d.arc(rx, 50, 14, 110, 430, n=40)
    d.group('mid')
    # the cycle of transformation: fire to air to water to earth, each sharing a quality with the next
    order = ['FIRE', 'AIR', 'WATER', 'EARTH']
    for i, k in enumerate(order):
        a, b = mids[k], mids[order[(i + 1) % 4]]
        d.line(a, b)
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        d.lines(_arrowhead(m, math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))))
    for p in mids.values():
        d.circle(*p, 4.5)
    # water surfaces, stopcocks, electrodes, bubbles, and the cell that drives them
    for k, x in xs.items():
        y = top + (2 if k == 'H' else 1) * unit
        d.line((x - w, y), (x + w, y))
        d.line((x - 5, top - 14), (x + 5, top - 14))
        d.line((x, top - 16), (x, top - 24))
        d.line((x - 3, bot - 30), (x - 3, bot - 8), (x + 3, bot - 8), (x + 3, bot - 30), closed=True)
        for j, yy in enumerate(range(int(y) + 12, bot - 34, 13)):
            d.circle(x + (2 if j % 2 else -2), yy, 1.6)
    d.line((xs['H'], bot), (xs['H'], 250), (rx - 12, 250))
    d.line((xs['O'], bot), (xs['O'], 250), (rx + 12, 250))
    d.lines([[(rx - 12, 241), (rx - 12, 259)], [(rx - 4, 245), (rx - 4, 255)],
             [(rx + 4, 241), (rx + 4, 259)], [(rx + 12, 245), (rx + 12, 255)]])
    d.group('mid')
    for k, (x, y) in corners.items():
        dx, dy = (-1 if x < c[0] else 1), (-1 if y < c[1] else 1)
        d.text(x + dx * 16, y + dy * 12 + 3, k, size=8)
    d.text(mids['FIRE'][0], mids['FIRE'][1] - 9, 'FIRE', size=8)
    d.text(mids['WATER'][0], mids['WATER'][1] + 16, 'WATER', size=8)
    d.text(mids['AIR'][0] + 10, mids['AIR'][1] + 3, 'AIR', size=8, anchor='start')
    d.text(mids['EARTH'][0] - 10, mids['EARTH'][1] + 3, 'EARTH', size=8, anchor='end')
    d.text(xs['H'] - 24, top + unit + 3, '2', size=9, anchor='end')
    d.text(xs['O'] + 24, top + unit / 2 + 3, '1', size=9, anchor='start')
    d.text(xs['H'], 36, 'H₂', size=9)
    d.text(xs['O'], 36, 'O₂', size=9)
    d.text(200, 284, '2 H₂O → 2 H₂ + O₂', size=9)
    return d


def alexandrian_alchemy():
    """Maria's tribikos after Zosimos: a flask on a furnace, a copper head, and three arms to three receivers."""
    d = D()
    ax = 196
    fc, fr = (ax, 196), 30                      # the clay flask (lopas): centre and radius
    neck_top = 118
    hc, hr = (ax, 98), 24                       # the still-head (bikos)
    receivers = [(56, 214, 165), (318, 222, 20), (362, 180, 8)]   # x, y, and the arm's outlet angle on the head
    d.group('thin')
    d.line((ax, 40), (ax, 272))
    d.line((20, 268), (380, 268))
    d.circle(*hc, hr + 10)
    # the vapour's path, up the neck
    for dx in (-3, 3):
        d.line((ax + dx, 176), (ax + dx, 126))
    d.lines(_arrowheadpair(ax, 126))
    d.group()
    # the furnace
    d.line((ax - 44, 268), (ax - 40, 226), (ax + 40, 226), (ax + 44, 268))
    d.arc(ax, 268, 14, 180, 360, n=20)
    # the flask and its neck
    na = math.degrees(math.asin(7 / fr))
    d.arc(*fc, fr, -90 + na, 270 - na, n=60)
    d.line((ax - 7, fc[1] - fr * math.cos(math.radians(na))), (ax - 7, neck_top))
    d.line((ax + 7, fc[1] - fr * math.cos(math.radians(na))), (ax + 7, neck_top))
    # the head: a dome with a rim that gathers what condenses
    d.arc(*hc, hr, 180, 360, n=40)
    d.line((hc[0] - hr, hc[1]), (hc[0] - hr + 4, hc[1] + 12), (ax - 7, hc[1] + 14))
    d.line((hc[0] + hr, hc[1]), (hc[0] + hr - 4, hc[1] + 12), (ax + 7, hc[1] + 14))
    # three arms, from the head's rim down to the receivers
    arms = []
    for x, y, a in receivers:
        start = _pt(hc, a, hr)
        end = (x, y - 26)
        arms += _parallel(start, end, k=5)
    d.lines(arms)
    for x, y, a in receivers:
        d.circle(x, y, 15)
        d.line((x - 4, y - 15), (x - 4, y - 24))
        d.line((x + 4, y - 15), (x + 4, y - 24))
    d.group('mid')
    # the charge in the flask, the fire, drops falling into the receivers, and the flour-paste luting
    d.line((ax - 26, fc[1] + 12), (ax + 26, fc[1] + 12))
    for x in (ax - 18, ax, ax + 18):
        d.line((x - 6, 262), (x, 248), (x + 6, 262))
    for x, y, a in receivers:
        d.line((x - 11, y + 6), (x + 11, y + 6))
        d.circle(x, y - 10, 1.4)
    d.ellipse(ax, neck_top + 2, 10, 3)
    d.group('mid')
    d.text(ax, 28, 'TRIBIKOS, AFTER ZOSIMOS', size=8)
    d.text(ax + 40, 206, 'SULFUR', size=7, anchor='start')
    d.text(hc[0] + hr + 8, hc[1] - 16, 'COPPER HEAD', size=7, anchor='start')
    d.text(56, 246, 'GLASS', size=7)
    d.text(ax, 290, 'HgS + O₂ → Hg + SO₂', size=9)
    return d


def _arrowheadpair(x, y):
    return [[(x - 5, y + 6), (x, y), (x + 5, y + 6)]]


def iron_gall_ink():
    """A model of the pigment: iron(III) held by two gallates, each through two neighbouring oxygens."""
    d = D()
    O = (200, 128)                              # the iron atom, on the drawing's mirror line
    L, Lo, Lfe = 22, 18, 24                     # ring bond, C–O bond, O–Fe bond
    # place the left ring so that the oxygens on its carbons at -30 and +30 degrees sit Lfe from the iron
    oy = (L + Lo) * math.sin(math.radians(30))
    ox = (L + Lo) * math.cos(math.radians(30))
    cx = O[0] - ox - math.sqrt(Lfe ** 2 - oy ** 2)
    left = {}
    ring = (cx, O[1])
    for name, a in (('c4', -30), ('c5', -90), ('c6', -150), ('c1', 150), ('c2', 90), ('c3', 30)):
        left[name] = _pt(ring, a, L)
    left['ring'] = ring
    left['o4'] = _pt(left['c4'], -30, Lo)
    left['o3'] = _pt(left['c3'], 30, Lo)
    left['o5'] = _pt(left['c5'], -90, Lo)
    left['cc'] = _pt(left['c1'], 150, L)       # the carboxyl carbon
    left['oa'] = _pt(left['cc'], 90, Lo)
    left['ob'] = _pt(left['cc'], 210, Lo)

    def flip(p):
        return (2 * O[0] - p[0], p[1])

    right = {k: flip(v) for k, v in left.items()}
    d.group('thin')
    d.line((O[0], 36), (O[0], 226))
    for h in (left, right):
        d.circle(*h['ring'], L)
    d.circle(*O, Lfe)
    d.group()
    for h in (left, right):
        d.line(h['c1'], h['c2'], h['c3'], h['c4'], h['c5'], h['c6'], closed=True)
        d.line(h['c4'], h['o4'])
        d.line(h['c3'], h['o3'])
        d.line(h['c5'], h['o5'])
        d.line(h['c1'], h['cc'])
        d.lines(_parallel(h['cc'], h['oa'], k=3.4))
        d.line(h['cc'], h['ob'])
    d.circle(*O, 7)
    d.group('mid')
    for h in (left, right):
        d.lines([_offset(h['c1'], h['c2'], h['ring']), _offset(h['c3'], h['c4'], h['ring']),
                 _offset(h['c5'], h['c6'], h['ring'])])
        d.lines([[h['o4'], _pt(O, math.degrees(math.atan2(h['o4'][1] - O[1], h['o4'][0] - O[0])), 7)],
                 [h['o3'], _pt(O, math.degrees(math.atan2(h['o3'][1] - O[1], h['o3'][0] - O[0])), 7)]])
    d.group('mid')
    d.text(O[0], O[1] + 3.5, 'Fe', size=8)
    for h, s in ((left, 1), (right, -1)):
        d.text(h['o4'][0] - s * 1, h['o4'][1] - 5, 'O', size=8)
        d.text(h['o3'][0] - s * 1, h['o3'][1] + 11, 'O', size=8)
        d.text(h['o5'][0], h['o5'][1] - 5, 'OH', size=8)
        d.text(h['oa'][0], h['oa'][1] + 11, 'O', size=8)
        d.text(h['ob'][0] - s * 8, h['ob'][1] + 3, 'HO', size=8, anchor='end' if s > 0 else 'start')
    d.text(O[0], 30, 'IRON(III) HELD BY TWO GALLATES · A MODEL', size=8)
    d.text(O[0], 254, 'Fe²⁺ → Fe³⁺ + e⁻', size=9)
    d.text(O[0], 276, '4 Fe²⁺ + O₂ + 4 H⁺ → 4 Fe³⁺ + 2 H₂O', size=9)
    return d


PLATES = {'four-elements': four_elements, 'alexandrian-alchemy': alexandrian_alchemy, 'iron-gall-ink': iron_gall_ink}
