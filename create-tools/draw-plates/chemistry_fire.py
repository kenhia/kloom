"""Plates for the chemistry subject's first segment, Fire and earth (sprint 025)."""
import math
from plates import D


def copper_smelting():
    d = D()
    cx, gy, rx, ry = 130, 138, 72, 58          # the pit, in section, below the ground line gy
    px, py, pr = 322, 112, 30                   # the same pit in plan
    d.group('thin')
    # ground line, the pit's centre line, and the projection from section to plan
    d.line((18, gy), (242, gy))
    d.line((cx, gy - 70), (cx, gy + ry + 10))
    d.line((px, py - 78), (px, py + 78))
    d.line((px - 78, py), (px + 78, py))
    d.circle(px, py, 70)
    d.group()
    # the pit and its lining of broken pots, laid as sherds with gaps between
    d.arc(cx, gy, rx, 0, 180, n=60, ry=ry)
    segs = []
    for k in range(9):
        a0, a1 = 4 + k * 19.5, 4 + k * 19.5 + 16
        segs.append([(cx + (rx + 6) * math.cos(math.radians(a)), gy + (ry + 6) * math.sin(math.radians(a)))
                     for a in [a0 + (a1 - a0) * i / 8 for i in range(9)]])
    d.lines(segs)
    d.circle(px, py, pr)
    d.circle(px, py, pr + 5)
    # six blowpipes, drawn in plan at sixty degrees; two of them cut by the section
    pipes = []
    for k in range(6):
        a = math.radians(30 + 60 * k)
        pipes.append([(px + (pr + 8) * math.cos(a), py + (pr + 8) * math.sin(a)),
                      (px + 68 * math.cos(a), py + 68 * math.sin(a))])
    d.lines(pipes)
    d.lines([[(22, 84), (78, 130)], [(238, 84), (182, 130)]])
    d.group('mid')
    # the charge: lumps of charcoal and ore, packed in the pit
    rnd = [(0.31, 0.2), (0.62, 0.35), (0.12, 0.55), (0.45, 0.6), (0.8, 0.62), (0.28, 0.85), (0.6, 0.88),
           (0.9, 0.3), (0.05, 0.25), (0.72, 0.05), (0.4, 0.05), (0.95, 0.85)]
    for i, (u, v) in enumerate(rnd):
        x = cx - rx + 18 + u * (2 * rx - 36)
        y = gy + 8 + v * (ry - 26)
        if abs(x - cx) / rx + (y - gy) / ry < 1.05:
            if i % 3:
                d.circle(x, y, 5.5 if i % 2 else 4)
            else:
                d.line((x - 5, y + 3), (x - 1, y - 5), (x + 5, y - 1), (x + 3, y + 4), closed=True)
    # ceramic nozzles on the pipe tips, and the blast
    d.lines([[(74, 126), (84, 135)], [(186, 126), (176, 135)]])
    d.lines([[(90, 142), (106, 154)], [(170, 142), (154, 154)]])
    # the bead of copper collecting at the bottom
    d.arc(cx, gy + ry - 10, 14, 0, 180, n=24, ry=6)
    d.line((cx - 14, gy + ry - 10), (cx + 14, gy + ry - 10))
    d.group('mid')
    d.text(cx, 30, 'SECTION', size=8)
    d.text(px, 30, 'PLAN', size=8)
    d.text(cx, gy + ry + 26, 'CHARCOAL AND ORE · c. 1100 °C', size=8)
    d.text(px, py + 92, 'SIX BLOWPIPES', size=8)
    d.text(200, 262, 'Cu₂CO₃(OH)₂ → 2 CuO + CO₂ + H₂O')
    d.text(200, 280, 'CuO + CO → Cu + CO₂')
    return d


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


def tyrian_purple():
    """6,6'-dibromoindigo, drawn from regular rings, and its 1:2:1 mass-spectrum triplet."""
    d = D()
    L, O = 24, (200, 126)                           # bond length; the molecule's centre of inversion
    r5 = L / (2 * math.sin(math.radians(36)))
    c2 = (O[0] - L / 2, O[1])
    p5 = (c2[0] - r5, O[1])                          # the five-membered ring's centre
    c3, c3a, c7a, n1 = (_pt(p5, a, r5) for a in (-72, -144, 144, 72))
    h6 = (c3a[0] - L * math.cos(math.radians(30)), O[1])   # the benzene ring's centre
    c4, c5, c6, c7 = (_pt(h6, a, L) for a in (-90, -150, 150, 90))
    ox = _pt(c3, -72, L)
    hn = _pt(n1, 72, L * 0.7)
    br = _pt(c6, 150, L * 1.1)

    def flip(p):                                     # the other half is the same, turned through 180 degrees
        return (2 * O[0] - p[0], 2 * O[1] - p[1])

    halves = [dict(c2=c2, c3=c3, c3a=c3a, c7a=c7a, n1=n1, c4=c4, c5=c5, c6=c6, c7=c7, ox=ox, hn=hn, br=br, p5=p5, h6=h6)]
    halves.append({k: flip(v) for k, v in halves[0].items()})
    d.group('thin')
    for h in halves:
        d.circle(*h['p5'], r5)
        d.circle(*h['h6'], L)
    d.line((O[0], O[1] - 62), (O[0], O[1] + 62))
    d.circle(*O, 2.5)
    d.group()
    for h in halves:
        d.line(h['c2'], h['c3'], h['c3a'], h['c4'], h['c5'], h['c6'], h['c7'], h['c7a'], h['n1'], h['c2'])
        d.line(h['c3a'], h['c7a'])
        d.lines(_parallel(h['c3'], h['ox']))
        d.line(h['n1'], h['hn'])
        d.line(h['c6'], h['br'])
    d.lines(_parallel(halves[0]['c2'], halves[1]['c2']))
    d.group('mid')
    for h in halves:
        d.lines([_offset(h['c4'], h['c5'], h['h6']), _offset(h['c6'], h['c7'], h['h6']),
                 _offset(h['c7a'], h['c3a'], h['h6'])])
    # the mass spectrum: two bromines, each 79 or 81 about equally, give 1 : 2 : 1
    bx, by = 150, 272
    d.group('thin')
    d.line((bx - 10, by), (bx + 110, by))
    d.group()
    d.lines([[(bx + 20 + 40 * i, by), (bx + 20 + 40 * i, by - 18 * k)] for i, k in enumerate((1, 2, 1))])
    d.group('mid')
    for h in halves:
        d.text(*_pt(h['ox'], -72 if h is halves[0] else 108, 9), 'O', size=10)
        d.text(*_pt(h['hn'], 72 if h is halves[0] else -108, 8), 'H', size=9)
        d.text(*_pt(h['br'], 150 if h is halves[0] else -30, 13), 'Br', size=10)
    for h, a in ((halves[0], 72), (halves[1], -108)):
        n = h['n1']
        d.text(n[0] + (9 if a == 72 else -9), n[1] + (3 if a == 72 else 3), 'N', size=9)
    for i, m in enumerate((418, 420, 422)):
        d.text(bx + 20 + 40 * i, by + 12, str(m), size=8)
    d.text(bx + 124, by - 4, 'm/z', size=8, anchor='start')
    d.text(200, 222, 'C₁₆H₈Br₂N₂O₂ · 6,6′-DIBROMOINDIGO', size=8)
    return d


def clay_recipes():
    """A glassmaker's kiln in section, and the Nineveh recipe's three weighed heaps."""
    d = D()
    kx, fy, r = 104, 170, 62                     # the kiln's axis, the chamber floor, the dome's radius
    d.group('thin')
    d.line((kx, fy - r - 14), (kx, 250))
    d.line((20, 232), (380, 232))
    d.circle(kx, fy, r)
    d.line((kx - r - 12, fy), (kx + r + 12, fy))
    d.group()
    # the dome, the firebox beneath it, and the floor between them
    d.arc(kx, fy, r, 180, 360, n=60)
    d.arc(kx, fy, r + 7, 180, 360, n=60)
    d.line((kx - r - 7, fy), (kx - r - 7, 232))
    d.line((kx + r + 7, fy), (kx + r + 7, 232))
    d.line((kx - r, fy), (kx + r, fy))
    d.line((kx - r, fy + 6), (kx + r, fy + 6))
    d.group('mid')
    # the stoke-hole, and the four openings in the dome (two cut by the section, two seen beyond)
    d.arc(kx, 232, 16, 180, 360, n=24)
    for a in (205, 335):
        x0, y0 = kx + r * math.cos(math.radians(a)), fy + r * math.sin(math.radians(a))
        d.arc(x0, y0, 6, 0, 360, n=20)
    for a in (235, 305):
        x0, y0 = kx + (r - 14) * math.cos(math.radians(a)), fy + (r - 14) * math.sin(math.radians(a))
        d.ellipse(x0, y0, 5, 7)
    # logs burning under the floor
    for x in (kx - 34, kx - 12, kx + 10, kx + 32):
        d.circle(x, 216, 7)
    # the crucible on the floor, and the melt in it
    d.line((kx - 20, fy - 30), (kx - 15, fy), (kx + 15, fy), (kx + 20, fy - 30))
    d.line((kx - 18.5, fy - 20), (kx + 18.5, fy - 20))
    d.group()
    # the recipe's three heaps, as cones whose volume goes with the minas weighed
    heaps = [(226, 10, 'QUARTZ'), (293, 15, 'PLANT ASH'), (358, 1 + 2 / 3, 'WHITE PLANT')]
    for x, m, name in heaps:
        h = 22 * m ** (1 / 3)
        w = h * 1.15
        d.line((x - w / 2, 232), (x, 232 - h), (x + w / 2, 232))
    d.group('mid')
    for x, m, name in heaps:
        d.text(x, 246, {10: '10', 15: '15'}.get(m, '1⅔'), size=9)
        d.text(x, 258, name, size=7)
    d.text(293, 274, 'MINAS', size=7)
    d.text(kx, fy - r - 22, 'KILN WITH FOUR OPENINGS', size=8)
    return d


PLATES = {'copper-smelting': copper_smelting, 'tyrian-purple': tyrian_purple, 'clay-recipes': clay_recipes}
