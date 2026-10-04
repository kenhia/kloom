"""Plates for western-civ's part mid1 (sprint 049): house-of-wisdom, crusades. See plates_for.py."""
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


def _pt(cx, cy, r, a):
    return (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))


def house_of_wisdom():
    """Al-Mansur's Round City of Baghdad (762-766) in plan, after Le Strange's reconstruction (1900).

    Left: the plan. Le Strange, from al-Ya'qubi: a water-filled ditch; an outer wall; an empty ring
    (50 yards); the main wall; a ring of houses; an inner wall round a central area holding the
    palace of the Golden Gate and the Great Mosque. Four equidistant gates (Kufa SW, Basra SE,
    Khurasan NE, Syria NW), each joined to the center by an arcaded street. Between the Kufa and
    Basra gates the outer wall had 29 bastions, between the others 28 each (113 in all). The rings
    are drawn wider than to scale so they can be told apart; the sources disagree about the size.
    Right: a section through the two ramparts to Le Strange's figures in feet: the outer wall 75 at
    its foot, 30 at the top, about 60 high; the empty ring 150; the main wall 105 at its foot, 37.5
    at the top, 90 high. The ditch's width is not given: it is drawn schematic.
    """
    d = D()
    cx, cy = 132, 150
    r_ditch_o, r_ditch_i = 124, 117
    r_outer = 112
    r_main_o, r_main_i = 100, 94
    r_inner = 66
    gates = {-45: 'KHURASAN', 45: 'BASRA', 135: 'KUFA', -135: 'SYRIA'}
    gap = 5                                                              # half a gate's opening, degrees

    d.group('thin')
    for a in gates:                                                      # the four roads, through the center
        d.line(_pt(cx, cy, 136, a), _pt(cx, cy, 0, a))
    d.circle(cx, cy, r_ditch_o)                                          # the ditch's outer edge

    # the section's construction: ground line and the heights
    s = 0.3                                                              # units per foot
    gx0, gy = 262, 214
    d.line((gx0, gy), (396, gy))
    for h in (60, 90):
        d.line((gx0, gy - h * s), (396, gy - h * s))

    d.group()
    # the walls in plan, broken at the four gates
    for r in (r_ditch_i, r_outer, r_main_o, r_main_i, r_inner):
        for a in (-45, 45, 135, 225):
            d.arc(cx, cy, r, a + gap, a + 90 - gap, n=40)
    # the section: ditch, outer wall, empty ring, main wall
    x = gx0 + 4
    d.line((gx0, gy), (x, gy + 9), (x + 10, gy + 9), (x + 14, gy))       # the ditch, schematic
    x += 18
    ow = [(x, gy), (x + (75 - 30) / 2 * s, gy - 60 * s), (x + (75 + 30) / 2 * s, gy - 60 * s), (x + 75 * s, gy)]
    d.line(*ow)
    x += 75 * s + 150 * s
    mw = [(x, gy), (x + (105 - 37.5) / 2 * s, gy - 90 * s), (x + (105 + 37.5) / 2 * s, gy - 90 * s), (x + 105 * s, gy)]
    d.line(*mw)
    x_main_end = x + 105 * s

    d.group('mid')
    # the gate passages: the street runs through each ring, and arcades line it between the main and inner walls
    for a in gates:
        for side in (-1, 1):
            off = side * gap * 0.75
            d.line(_pt(cx, cy, r_ditch_o + 4, a + off), _pt(cx, cy, r_inner, a + off))
        for i in range(1, 9):                                            # the arcades, a few of their 53 arches
            r = r_inner + 3 + i * (r_main_i - r_inner - 6) / 9
            for side in (-1, 1):
                p = _pt(cx, cy, r, a + side * gap * 0.75)
                q = _pt(cx, cy, r, a + side * gap * 1.6)
                d.line(p, q)
    # bastions on the outer wall: 29 between Kufa and Basra, 28 between each other pair
    for a0 in (-45, 45, 135, 225):
        n = 29 if a0 == 45 else 28                                       # Basra (45) to Kufa (135)
        for i in range(1, n + 1):
            a = a0 + gap + (90 - 2 * gap) * i / (n + 1)
            d.line(_pt(cx, cy, r_outer, a), _pt(cx, cy, r_outer + 3, a))
    # the houses: short radial party walls in the ring between the main and inner walls
    for k in range(4):
        for i in range(1, 12):
            a = -45 + 90 * k + gap * 1.8 + (90 - 3.6 * gap) * i / 12
            d.line(_pt(cx, cy, r_inner + 6, a), _pt(cx, cy, r_main_i - 6, a))
        d.arc(cx, cy, (r_inner + r_main_i) / 2, -45 + 90 * k + gap * 1.8, 45 + 90 * k - gap * 1.8, n=24)
    # the palace and its green dome at the center, the mosque beside it
    _box(d, cx - 13, cy - 13, 26, 26)
    d.circle(cx, cy, 7)
    _box(d, cx + 15, cy + 5, 16, 16)
    # the section's water in the ditch and the walls' battlements, as short ticks
    d.line((gx0 + 6, gy + 5), (gx0 + 16, gy + 5))
    for xx, top in ((ow[1][0], ow[2][0]), (mw[1][0], mw[2][0])):
        y = gy - (60 if xx == ow[1][0] else 90) * s
        k = xx
        while k < top - 1:
            d.line((k, y), (k, y - 2.5))
            k += 2.6
    _arrow(d, (x_main_end - 105 * s - 150 * s + 2, gy + 14), (x_main_end - 105 * s - 2, gy + 14), size=3)
    _arrow(d, (x_main_end - 105 * s - 2, gy + 14), (x_main_end - 105 * s - 150 * s + 2, gy + 14), size=3)
    d.line((x_main_end - 105 * s - 150 * s + 2, gy + 14), (x_main_end - 105 * s - 2, gy + 14))
    # north arrow
    _arrow(d, (cx + 120, 40), (cx + 120, 24), size=4)
    d.line((cx + 120, 40), (cx + 120, 24))

    d.group('mid')
    for a, name in gates.items():
        x_, y_ = _pt(cx, cy, 135, a)
        d.text(x_, y_ + 3, name, size=7, anchor='start' if math.cos(math.radians(a)) > 0 else 'end')
    d.text(cx + 120, 19, 'N', size=7)
    d.text(cx, cy + 34, 'PALACE · MOSQUE', size=7)
    d.text(x_main_end - 105 * s - 75 * s, gy + 26, '150 FT', size=7)
    d.text(x_main_end - 52 * s, gy - 90 * s - 8, '90 FT', size=7)
    d.text(gx0 + 22 + 37 * s, gy - 60 * s - 8, '60 FT', size=7)
    d.text(329, 46, 'THE ROUND CITY', size=7)
    d.text(329, 58, 'AD 762–766', size=7)
    d.text(329, 70, 'AFTER LE STRANGE, 1900', size=7)
    d.text(329, gy + 40, 'SECTION, OUTER WALL', size=7)
    d.text(329, gy + 50, 'TO MAIN WALL', size=7)
    return d


def crusades():
    """Jerusalem, 7 June to 15 July 1099: the city's walls in plan, schematic, and a siege tower at the wall in section.

    Left: the walls as a rough quadrilateral about a kilometer on a side (the circuit was about four
    kilometers, Wikipedia's "Siege of Jerusalem (1099)"), with the Temple Mount at the east, the Tower
    of David at the west, and the two siege towers' positions from the Gesta Francorum: Godfrey's,
    moved by night to the east end of the north wall, and Raymond of Toulouse's on the plain to the
    south. Right: a section to scale of the wall (15 m high, 3 m thick) with the filled ditch before
    it and a wheeled tower whose drawbridge, hinged at its middle, swings down onto the wall top, as
    Raymond of Aguilers describes. The tower's own height is not recorded; it is drawn to carry the
    hinge at the wall's top.
    """
    d = D()
    # the plan: kilometers to units, origin at the north-west corner
    k = 150
    ox, oy = 30, 72
    P = lambda x, y: (ox + x * k, oy + y * k)
    wall = [P(0, 0.02), P(0.98, 0), P(1.02, 0.88), P(0.6, 0.98), P(0.08, 0.9)]
    temple = [P(0.68, 0.38), P(0.98, 0.36), P(1.0, 0.84), P(0.71, 0.86)]
    david = P(0.04, 0.46)
    god = P(0.86, 0.0)
    ray = P(0.3, 0.94)

    d.group('thin')
    # a kilometer grid behind the plan, and the section's ground and wall-top lines
    for i in range(0, 5):
        d.line(P(i * 0.25, -0.08), P(i * 0.25, 1.06))
        d.line(P(-0.08, i * 0.25), P(1.1, i * 0.25))
    s = 4.0                                                              # section: units per meter
    gx0, gy = 232, 236
    d.line((gx0, gy), (396, gy))
    d.line((gx0, gy - 15 * s), (396, gy - 15 * s))

    d.group()
    d.line(*wall, closed=True)
    # the section: the wall, 3 m thick and 15 m high, with its ditch in front
    wx = 352
    d.line((wx, gy), (wx, gy - 15 * s), (wx + 3 * s, gy - 15 * s), (wx + 3 * s, gy))
    d.line((wx - 2, gy), (wx - 4, gy + 10), (wx - 26, gy + 10), (wx - 28, gy))

    d.group('mid')
    d.line(*temple, closed=True)
    d.circle(*david, 4)
    for x, y in (god, ray):                                              # the two towers' stations, and their attacks
        d.line((x - 4, y - 4), (x + 4, y - 4), (x + 4, y + 4), (x - 4, y + 4), closed=True)
    _arrow(d, (god[0], god[1] - 26), (god[0], god[1] - 7), size=4)
    d.line((god[0], god[1] - 26), (god[0], god[1] - 7))
    _arrow(d, (ray[0], ray[1] + 24), (ray[0], ray[1] + 7), size=4)
    d.line((ray[0], ray[1] + 24), (ray[0], ray[1] + 7))
    # the section: the ditch filled with stones, a few drawn
    for i in range(6):
        cx_ = wx - 24 + i * 4
        d.circle(cx_, gy + 5, 1.6)
    # the tower on its wheels, its frame in stages, the bridge hinged at its middle
    tw, th = 9 * s, 30 * s * 0.92
    tx = wx - 3 - tw
    d.line((tx, gy - 2), (tx, gy - th), (tx + tw, gy - th), (tx + tw, gy - 2), closed=True)
    for j in range(1, 4):
        y = gy - th * j / 4
        d.line((tx, y), (tx + tw, y))
    d.line((tx, gy - 2), (tx + tw, gy - th / 4))
    d.line((tx + tw, gy - 2), (tx, gy - th / 4))
    for wxx in (tx + 6, tx + tw - 6):
        d.circle(wxx, gy - 3, 3)
    hinge = (tx + tw, gy - 15 * s)
    blen = 3 * s + 3
    d.line(hinge, (hinge[0] + blen, hinge[1]))                           # the bridge, down on the wall
    d.arc(hinge[0], hinge[1], blen, -90, 0, n=16, cls=None)              # its swing, from upright

    d.group('mid')
    d.text(god[0], god[1] - 31, 'GODFREY', size=7)
    d.text(ray[0], ray[1] + 33, 'RAYMOND', size=7)
    d.text(david[0] + 7, david[1] + 2.5, 'TOWER OF DAVID', size=7, anchor='start')
    tcx = (temple[0][0] + temple[2][0]) / 2
    tcy = (temple[0][1] + temple[2][1]) / 2
    d.text(tcx, tcy, 'TEMPLE', size=7)
    d.text(tcx, tcy + 9, 'MOUNT', size=7)
    d.text(ox + 0.5 * k, oy + 1.06 * k + 30, 'JERUSALEM, 1099 · GRID 250 M', size=7)
    d.text(wx + 3 * s + 6, gy - 7.5 * s, '15 M', size=7, anchor='start')
    d.text(tx + tw / 2, gy + 24, 'SIEGE TOWER · WALL', size=7)
    d.text(tx + tw / 2, gy - th - 8, '15 JULY', size=7)
    d.text(ox + 1.1 * k, oy - 26, 'N', size=7)
    _arrow(d, (ox + 1.1 * k, oy - 6), (ox + 1.1 * k, oy - 20), size=3)
    d.line((ox + 1.1 * k, oy - 6), (ox + 1.1 * k, oy - 20))
    return d


PLATES = {'house-of-wisdom': house_of_wisdom, 'crusades': crusades}
