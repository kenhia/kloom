"""Plates for the chemistry subject's Materials segment, part one (sprint 025):
Bessemer steel, aluminium by electrolysis, and ultrapure silicon."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _arrow(d, a, b, k=6):
    """An open arrowhead at b, pointing from a."""
    ang = math.degrees(math.atan2(a[1] - b[1], a[0] - b[0]))
    d.line(_pt(b, ang + 25, k), b, _pt(b, ang - 25, k))


# ---------------------------------------------------------------- Bessemer steel

def _fe_c(x0, y0, sx, sy, t0):
    """Map (% carbon, °C) on the iron-carbon diagram to the page."""
    return lambda c, t: (x0 + c * sx, y0 - (t - t0) * sy)


def bessemer_steel():
    """A tilting converter in section, blowing; and the blow's path on the iron-carbon diagram."""
    d = D()
    ax, by = 100, 238                       # the converter's axis and the underside of its bottom
    # the shell's half-width at each height, bottom to mouth: a cylinder on a rounded base, then a cone
    prof = []
    for i in range(13):                     # the rounded bottom, a quarter ellipse
        a = math.radians(90 * i / 12)
        prof.append((52 * math.sin(a), by - 26 * (1 - math.cos(a))))
    prof += [(52, 150), (22, 92), (22, 80)]
    inner = [(w - 10, y - (6 if y > 200 else 0)) for w, y in prof[3:-1]] + [(13, 80)]
    ty = 172                                # the trunnions' axis
    P = _fe_c(236, 250, 30, 0.19, 650)      # the diagram: 5 % carbon across, 650-1650 °C up
    d.group('thin')
    d.line((ax, 58), (ax, 262))
    d.line((ax - 76, ty), (ax + 76, ty))
    d.lines([[P(0, 650), P(5, 650)], [P(0, 650), P(0, 1650)]])
    d.lines([[P(c, 650), P(c, 644)] for c in (1, 2, 3, 4, 5)])
    d.lines([[P(0, t), P(-0.15, t)] for t in (800, 1000, 1200, 1400, 1600)])
    d.line(P(2.1, 650), P(2.1, 1148))
    d.group()
    # the shell, drawn round from mouth to mouth through the bottom
    right = [(ax + w, y) for w, y in reversed(prof)]
    left = [(ax - w, y) for w, y in prof]
    d.line(*(left + right))
    d.line(*([(ax - w, y) for w, y in reversed(inner)] + [(ax + w, y) for w, y in inner]))
    # the trunnions and the band that carries them
    for s in (-1, 1):
        d.circle(ax + s * 64, ty, 7)
        d.line((ax + s * 52, ty - 8), (ax + s * 58, ty - 8), (ax + s * 58, ty + 8), (ax + s * 52, ty + 8))
    # the tuyere box under the bottom, and the blast pipe
    d.line((ax - 30, by + 2), (ax - 30, by + 14), (ax + 30, by + 14), (ax + 30, by + 2))
    d.line((ax + 30, by + 8), (ax + 70, by + 8), (ax + 70, ty + 8))
    # the iron-carbon diagram: liquidus, solidus, eutectic and eutectoid lines (the metastable Fe-Fe3C system)
    d.line(P(0, 1538), P(0.53, 1495), P(4.3, 1148), P(5, 1171))
    d.line(P(0, 1538), P(0.09, 1495), P(0.17, 1495), P(2.14, 1148))
    d.line(P(0.17, 1495), P(0.53, 1495))
    d.line(P(2.14, 1148), P(5, 1148))
    d.line(P(0, 912), P(0.76, 727), P(2.14, 1148))
    d.line(P(0.02, 727), P(5, 727))
    d.group('mid')
    # the bath, its surface, the tuyeres through the bottom lining, and bubbles rising from them
    d.line((ax - 46, 200), (ax + 46, 200))
    d.lines([[(ax + x, by + 2), (ax + x, by - 16)] for x in (-24, -12, 0, 12, 24)])
    bub = [(-24, 222, 2.5), (-12, 212, 3), (0, 226, 2.2), (12, 208, 3.2), (24, 218, 2.6),
           (-18, 204, 2), (6, 214, 2.4), (18, 230, 1.8), (-6, 232, 2)]
    for x, y, r in bub:
        d.circle(ax + x, y, r)
    # the flame from the mouth: three tongues, each a pointed arch
    for dx, h, w in ((-8, 30, 7), (0, 44, 9), (8, 34, 7)):
        tongue = [(ax + dx - w + 2 * w * i / 16 + 3 * math.sin(math.pi * i / 16) * (i / 16 - 0.5),
                   76 - h * math.sin(math.pi * i / 16) ** 0.7) for i in range(17)]
        d.line(*tongue)
    # the path of a blow: from pig iron at 4 % carbon and 1250 °C to soft metal at 0.1 % and 1600 °C
    path = [P(4 - 3.9 * u, 1250 + 350 * (1 - (1 - u) ** 1.6)) for u in [i / 24 for i in range(25)]]
    d.lines([path[i:i + 2] for i in range(0, 24, 2)])
    _arrow(d, path[-2], path[-1])
    d.circle(*path[0], 2.5)
    d.group('mid')
    d.text(*P(2.6, 1480), 'LIQUID', size=8)
    d.text(*P(1.05, 640 - 55), 'STEEL', size=7)
    d.text(*P(3.55, 640 - 55), 'CAST IRON', size=7)
    d.text(*P(5, 650 + 16), '% C', size=7, anchor='end')
    d.text(*P(-0.3, 1540 - 18), '1540 °C', size=7, anchor='end')
    d.text(*P(2.3, 1148 - 50), '1148', size=7, anchor='start')
    d.text(*P(5, 727 + 22), '727', size=7, anchor='end')
    d.text(*P(4.3, 1250 + 62), 'PIG IRON', size=7)
    d.text(ax, 276, 'CONVERTER, BLOWING', size=8)
    return d


# ---------------------------------------------------------------- aluminium

def aluminium():
    """A Hall-Héroult cell in section: carbon anodes in a cryolite bath over a pool of liquid aluminium."""
    d = D()
    x0, x1 = 44, 356                          # the steel shell, outside
    top, bot = 128, 246
    lin = 14                                  # the carbon lining's thickness
    bath_top, metal_top, floor = 152, 206, bot - lin
    anodes = [(116 + 84 * i, 58) for i in range(3)]   # centre and width of each anode block
    a_top, a_bot = 98, 190
    bus = 54
    d.group('thin')
    d.line((200, 30), (200, 262))
    for y in (bath_top, metal_top, floor):
        d.line((x0 - 16, y), (x1 + 16, y))
    d.group()
    # the steel shell and the carbon lining (the cathode)
    d.line((x0, top), (x0, bot), (x1, bot), (x1, top))
    d.line((x0 + lin, top), (x0 + lin, floor), (x1 - lin, floor), (x1 - lin, top))
    # the anodes, their stems and the busbar they hang from
    for cx, w in anodes:
        d.line((cx - w / 2, a_top), (cx - w / 2, a_bot), (cx + w / 2, a_bot), (cx + w / 2, a_top), closed=True)
        d.line((cx, a_top), (cx, bus))
    d.line((anodes[0][0] - 14, bus), (anodes[-1][0] + 14, bus))
    d.line((anodes[0][0] - 14, bus - 6), (anodes[-1][0] + 14, bus - 6))
    d.group('mid')
    # the bath's surface under its frozen crust, broken where the anodes pass, and the metal pool's surface
    gaps = [(cx - w / 2 - 4, cx + w / 2 + 4) for cx, w in anodes]
    edges = [x0 + lin] + [g for pair in gaps for g in pair] + [x1 - lin]
    crust = []
    for a, b in zip(edges[0::2], edges[1::2]):
        n = max(2, int((b - a) / 5))
        crust.append([(a + (b - a) * i / n, bath_top - 3 - 2.5 * math.sin(i * 2.1)) for i in range(n + 1)])
    d.lines(crust)
    d.lines([[(a, bath_top + 3), (b, bath_top + 3)] for a, b in zip(edges[0::2], edges[1::2])])
    d.line((x0 + lin, metal_top), (x1 - lin, metal_top))
    # bubbles of carbon dioxide rising round each anode's foot
    for cx, w in anodes:
        for k, (dx, dy, r) in enumerate(((-w / 2 - 5, -8, 2.4), (w / 2 + 5, -14, 2), (-w / 2 - 4, -24, 1.6),
                                          (w / 2 + 6, -30, 2.2), (-8, 5, 1.8), (9, 6, 2))):
            d.circle(cx + dx, a_bot + dy, r)
    # the collector bars through the lining, carrying current out of the cathode
    for x in (120, 200, 280):
        d.line((x - 10, floor + 4), (x + 10, floor + 4), (x + 10, floor + 10), (x - 10, floor + 10), closed=True)
    # the current: down each stem, through the bath, into the metal
    for cx, w in anodes:
        d.line((cx, a_bot + 2), (cx, metal_top - 3))
        d.line((cx - 3.5, metal_top - 9), (cx, metal_top - 3), (cx + 3.5, metal_top - 9))
    d.group('mid')
    d.text(200, 40, '+', size=10)
    d.text(x1 + 22, bath_top + 28, 'BATH', size=7, anchor='start')
    d.text(x1 + 22, a_top + 10, 'C +', size=8, anchor='start')
    d.text(x1 + 22, metal_top + 14, 'Al', size=8, anchor='start')
    d.text(x1 + 22, floor + 16, 'C −', size=8, anchor='start')
    d.text(200, 274, 'Na₃AlF₆ + Al₂O₃ AT 960 °C', size=7)
    d.text(200, 290, '2 Al₂O₃ + 3 C → 4 Al + 3 CO₂', size=9)
    return d


# ---------------------------------------------------------------- silicon

def silicon():
    """A Czochralski puller in section, and silicon's diamond-cubic unit cell."""
    d = D()
    ax = 104                                  # the puller's axis
    melt = 206                                # the melt's surface
    cr_w, cr_b = 58, 246                      # the crucible's half-width and its floor
    # the crystal's half-width, top to bottom: seed, thin neck, shoulder, then the body
    prof = [(3, 44), (3, 60), (1.6, 66), (1.6, 82), (8, 90), (22, 100), (30, 110), (32, 118), (32, 194), (30, melt - 2)]
    d.group('thin')
    d.line((ax, 26), (ax, 266))
    d.line((ax - 86, melt), (ax + 86, melt))
    d.group()
    # the crucible of quartz in its graphite susceptor
    d.line((ax - cr_w, 176), (ax - cr_w, cr_b - 10), (ax - cr_w + 10, cr_b), (ax + cr_w - 10, cr_b),
           (ax + cr_w, cr_b - 10), (ax + cr_w, 176))
    d.line((ax - cr_w - 7, 170), (ax - cr_w - 7, cr_b - 8), (ax - cr_w + 8, cr_b + 7), (ax + cr_w - 8, cr_b + 7),
           (ax + cr_w + 7, cr_b - 8), (ax + cr_w + 7, 170))
    # the crystal, drawn down one side and up the other
    d.line(*([(ax - w, y) for w, y in prof] + [(ax + w, y) for w, y in reversed(prof)]))
    # the pull rod and the seed chuck
    d.line((ax, 20), (ax, 36))
    d.line((ax - 6, 36), (ax + 6, 36), (ax + 6, 44), (ax - 6, 44), closed=True)
    d.group('mid')
    # the heater, cut through on each side
    for s in (-1, 1):
        for y in range(184, 244, 12):
            d.circle(ax + s * (cr_w + 19), y, 4)
    # the melt, its meniscus against the crystal, and the rotation of rod and crucible
    d.line((ax - cr_w + 1, melt), (ax - 34, melt), (ax - 30, melt - 2))
    d.line((ax + 30, melt - 2), (ax + 34, melt), (ax + cr_w - 1, melt))
    for y, r, a0, a1 in ((28, 14, 200, 340), (cr_b + 20, 30, 20, 160)):
        pts = [(ax + r * math.cos(math.radians(a)), y + 0.3 * r * math.sin(math.radians(a))) for a in range(a0, a1 + 1, 10)]
        d.line(*pts)
        _arrow(d, pts[-2], pts[-1], 5)
    d.line((ax + 22, 70), (ax + 22, 48))
    _arrow(d, (ax + 22, 70), (ax + 22, 48), 5)
    # silicon's unit cell: diamond cubic, drawn in an oblique projection
    O, s = (252, 214), 88                     # the cell's front lower-left corner, and its edge on the page
    k = (0.52, -0.2)                          # the receding axis

    def P(x, y, z):
        return (O[0] + s * (x + k[0] * z), O[1] - s * (y - k[1] * 0) + s * k[1] * z)

    corners = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    faces = [(0.5, 0.5, 0), (0.5, 0.5, 1), (0.5, 0, 0.5), (0.5, 1, 0.5), (0, 0.5, 0.5), (1, 0.5, 0.5)]
    inside = [(0.25, 0.25, 0.25), (0.75, 0.75, 0.25), (0.75, 0.25, 0.75), (0.25, 0.75, 0.75)]
    lattice = corners + faces
    d.group('thin')
    edges = [(a, b) for a in corners for b in corners if a < b and sum(abs(i - j) for i, j in zip(a, b)) == 1]
    d.lines([[P(*a), P(*b)] for a, b in edges])
    d.group()
    # each atom inside the cell bonds to its four nearest neighbours, a quarter of a body diagonal away
    bonds = []
    for p in inside:
        for q in lattice:
            if abs(math.dist(p, q) - math.sqrt(3) / 4) < 1e-6:
                bonds.append([P(*p), P(*q)])
    d.lines(bonds)
    d.group('mid')
    for p in lattice:
        d.circle(*P(*p), 3.2)
    for p in inside:
        d.circle(*P(*p), 4.2)
    d.group('mid')
    d.text(ax, 284, 'CZOCHRALSKI PULLER', size=8)
    d.text(ax + 38, 150, 'Si', size=9, anchor='start')
    d.text(ax + cr_w + 28, melt - 30, '1414 °C', size=7, anchor='start')
    d.text(*(lambda p: (p[0], p[1] + 20))(P(0.5, 0, 0)), 'a = 543.1 pm', size=8)
    d.text(*(lambda p: (p[0], p[1] - 16))(P(0.5, 1, 1)), '8 ATOMS PER CELL', size=7)
    return d


PLATES = {'bessemer-steel': bessemer_steel, 'aluminium': aluminium, 'silicon': silicon}
