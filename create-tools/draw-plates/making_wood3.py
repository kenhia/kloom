"""Plates for How We Build's Wood segment, part wood3: Thonet's chair and moulded plywood (sprint 026)."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _pt(cx, cy, r, a):
    u = _dir(a)
    return cx + r * u[0], cy + r * u[1]


def thonet_chair():
    """A rod strapped and bent round a form, as a chair back is, with the strain across its thickness."""
    d = D()
    cx, cy = 140, 150            # the centre of the bend
    R = 84                       # the form's radius, the rod's inner face: t/R = 1/6, the 25 mm rod on 150 mm
    t = 14                       # the rod's thickness
    leg = 112                    # the straight run below the bend, down to the end stops
    ro = R + t
    rs = ro + 3                  # the strap, just outside the rod
    d.group('thin')
    d.line((cx, cy - ro - 22), (cx, cy + leg + 14))                  # the axis of the bend
    d.line((cx - ro - 24, cy), (cx + ro + 24, cy))                   # the line the bend starts from
    d.line((cx, cy), _pt(cx, cy, R, 230))                            # the radius R
    d.arc(cx, cy, R + t / 2, 180, 360, n=60)                         # the rod's middle line: free, it keeps its length
    d.group()
    # the form: a half disc on a block
    d.line(_pt(cx, cy, R, 180), *[_pt(cx, cy, R, a) for a in range(180, 361, 4)],
           (cx + R, cy + leg), (cx - R, cy + leg), closed=True)
    # the rod: inner and outer faces round the bend and down both legs
    d.line((cx - R, cy + leg), *[_pt(cx, cy, R, a) for a in range(180, 361, 4)], (cx + R, cy + leg))
    d.line((cx - ro, cy + leg), *[_pt(cx, cy, ro, a) for a in range(180, 361, 4)], (cx + ro, cy + leg))
    d.lines([[(cx - ro, cy + leg), (cx - R, cy + leg)], [(cx + R, cy + leg), (cx + ro, cy + leg)]])
    d.group('mid')
    # the steel strap along the outer face, and its end stops bearing on the rod's ends
    d.line((cx - rs, cy + leg + 6), *[_pt(cx, cy, rs, a) for a in range(180, 361, 4)], (cx + rs, cy + leg + 6))
    for s in (-1, 1):
        x0 = cx + s * rs
        d.line((x0, cy + leg + 6), (x0 - s * (t + 7), cy + leg + 6), (x0 - s * (t + 7), cy + leg + 12),
               (x0, cy + leg + 12), closed=True)
    # the inner face wrinkling where it is squeezed: short ticks into the rod
    ticks = []
    for a in range(196, 345, 12):
        p0, p1 = _pt(cx, cy, R, a), _pt(cx, cy, R + 4, a)
        ticks.append([p0, p1])
    d.lines(ticks)
    # the thickness t, dimensioned at the crown
    d.lines([[(cx + 10, cy - R), (cx + 26, cy - R)], [(cx + 10, cy - ro), (cx + 26, cy - ro)]])
    d.line((cx + 22, cy - R), (cx + 22, cy - ro))
    d.group('mid')
    # strain across the thickness: free (stretched outside) and strapped (none outside)
    ax = 330
    for k, (name, outer, inner) in enumerate((('FREE', 1, -1), ('STRAPPED', 0, -2))):
        y0 = 70 + k * 104
        top, bot = y0, y0 + 56                  # outer face at top, inner face below
        d.line((ax, top - 8), (ax, bot + 8))    # zero strain
        d.lines([[(ax - 34, top), (ax + 34, top)], [(ax - 34, bot), (ax + 34, bot)]])
        s = 16                                   # px per unit of t/2R
        d.line((ax, top), (ax + outer * s, top), (ax + inner * s, bot), (ax, bot))
        d.text(ax, bot + 22, name, size=8)
    d.group('mid')
    d.text(cx - R + 30, cy + 34, 'FORM', size=8)
    d.text(cx - 58, cy - 36, 'R', size=9)
    d.text(cx + 30, cy - R - 3, 't', size=9, anchor='start')
    d.text(cx + rs + 8, cy + 40, 'STRAP', size=8, anchor='start')
    d.text(ax + 38, 73, 'OUT', size=8, anchor='start')
    d.text(ax + 38, 129, 'IN', size=8, anchor='start')
    d.text(ax - 38, 177, '0%', size=8, anchor='end')
    d.text(ax - 38, 233, '−t/R', size=8, anchor='end')
    return d


PLATES = {'thonet-chair': thonet_chair}


def moulded_plywood():
    """Three veneers exploded with their grain crossed, and the bag press that moulds a sheaf over a die."""
    d = D()
    # --- the exploded plies, in oblique projection: x along the grain of the faces, y receding at 30 degrees
    ox, oy = 20, 70
    L, W = 104, 62
    k = math.cos(math.radians(30)) * 0.55, -math.sin(math.radians(30)) * 0.55
    def P(x, y, z):
        return ox + x + y * k[0], oy + y * k[1] + z

    plies = (0, 46, 92)                           # the drop between plies
    d.group('thin')
    # the stack's corners projected down through the gaps
    for x, y in ((0, 0), (L, 0), (0, W), (L, W)):
        d.line(P(x, y, plies[0]), P(x, y, plies[-1]))
    d.group()
    for z in plies:
        d.line(P(0, 0, z), P(L, 0, z), P(L, W, z), P(0, W, z), closed=True)
    d.group('mid')
    # the grain: along the faces, across the core
    for j, z in enumerate(plies):
        segs = []
        if j % 2 == 0:
            for i in range(1, 9):
                y = W * i / 9
                segs.append([P(5, y, z), P(L - 5, y, z)])
        else:
            for i in range(1, 14):
                x = L * i / 14
                segs.append([P(x, 4, z), P(x, W - 4, z)])
        d.lines(segs)
    # --- the bag press in section
    px, py = 292, 178                             # the die's crown
    dw = 58                                       # half the die's width
    hw = 90                                       # half the chamber's width
    d.group('thin')
    d.line((px, 56), (px, 262))                   # the die's axis
    d.group()
    # the chamber
    d.line((px - hw, 250), (px - hw, 70), (px + hw, 70), (px + hw, 250), closed=True)
    # the die: a low dome on a block
    dome = [(px + dw * math.cos(math.radians(a)), py + 38 - 38 * math.sin(math.radians(a))) for a in range(0, 181, 6)]
    d.line((px + dw + 16, py + 38), *dome, (px - dw - 16, py + 38), (px - dw - 16, 250))
    d.line((px + dw + 16, py + 38), (px + dw + 16, 250))
    d.group('mid')
    # the sheaf of veneers over the dome, and the bladder pressing down on it
    for i in range(1, 5):
        r = 38 + 2.6 * i
        d.line(*[(px + (dw + 2.6 * i) * math.cos(math.radians(a)), py + 38 - r * math.sin(math.radians(a)))
                 for a in range(0, 181, 6)])
    bw = hw - 8
    bl = [(px + bw * math.cos(math.radians(a)), py + 30 - 62 * math.sin(math.radians(a))) for a in range(0, 181, 6)]
    d.line((px + bw, py + 38), *bl, (px - bw, py + 38))
    d.line((px - bw, py + 38), (px - bw, 78), (px + bw, 78), (px + bw, py + 38))
    # the heating element in the die, and the air line up through the roof to the pump
    d.lines([[(px - 40 + 10 * i, py + 46), (px - 35 + 10 * i, py + 54), (px - 30 + 10 * i, py + 46)] for i in range(8)])
    d.line((px + 30, 78), (px + 30, 44), (px + 60, 44))
    d.line((px + 60, 36), (px + 60, 52))
    d.group('mid')
    d.text(ox + 70, 196, 'FACE · CORE · BACK', size=8)
    d.text(px - 40, 40, 'BAG PRESS', size=8)
    d.text(px, 104, 'BLADDER', size=8)
    d.text(px, 244, 'DIE 165 °C', size=8)
    d.text(px + 64, 47, '30 PSI', size=8, anchor='start')
    return d


PLATES['moulded-plywood'] = moulded_plywood
