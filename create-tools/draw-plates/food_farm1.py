"""Plates for Daily Bread's part farm1 (sprint 051): gobekli-tepe, founder-crops, first-herds.
See plates_for.py."""
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


def _slab(d, cx, cy, a, length, width):
    """A rectangle `length` along direction a (radians), `width` across it, centered on (cx, cy)."""
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    hl, hw = length / 2, width / 2
    pts = [(cx + sx * hl * ux + sy * hw * vx, cy + sx * hl * uy + sy * hw * vy)
           for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    d.line(*pts, closed=True)


def gobekli_tepe():
    d = D()
    # Left: a round enclosure in plan, schematic, after the published plans of enclosure D: a ring wall
    # about 20 m across with T-pillars set radially into it at equal angles, and the two taller central
    # pillars standing parallel in the middle. Pillar count and spacing are schematic.
    # Right: a central pillar in elevation, 5.5 m high (Dietrich et al. 2019), the T a stylized body with
    # arms, hands, belt and loincloth carved on the shaft. Proportions of head and shaft are schematic.
    cx, cy = 118, 146
    m = 8.6                                                               # plan units per meter
    ri, ro = 10 * m, 11.4 * m                                             # inner and outer wall faces
    n = 12

    d.group('thin')
    d.line((cx - ro - 10, cy), (cx + ro + 10, cy))
    d.line((cx, cy - ro - 10), (cx, cy + ro + 10))
    for k in range(n):                                                    # radial setting-out lines
        a = 2 * math.pi * k / n + math.pi / n
        d.line((cx + 14 * math.cos(a), cy + 14 * math.sin(a)),
               (cx + (ri - 9) * math.cos(a), cy + (ri - 9) * math.sin(a)))
    px, gy = 300, 262                                                     # pillar axis and ground
    e = 36.4                                                              # elevation units per meter
    d.line((px, gy - 5.5 * e - 8), (px, gy + 6))                          # pillar's axis

    d.group()
    d.circle(cx, cy, ri)
    d.circle(cx, cy, ro)
    for k in range(n):                                                    # pillars set in the wall
        a = 2 * math.pi * k / n + math.pi / n
        r = ri - 2
        _slab(d, cx + r * math.cos(a), cy + r * math.sin(a), a, 1.6 * m, 0.45 * m)
    for s in (-1, 1):                                                     # the central pair
        _slab(d, cx + s * 1.5 * m, cy, math.pi / 2, 1.9 * m, 0.45 * m)
    # the pillar in elevation: a shaft and a wider head
    sw, hw = 1.2 * e, 2.1 * e
    top_shaft = gy - 4.6 * e
    top = gy - 5.5 * e
    d.line((px - sw / 2, gy), (px - sw / 2, top_shaft), (px - hw / 2, top_shaft), (px - hw / 2, top),
           (px + hw / 2, top), (px + hw / 2, top_shaft), (px + sw / 2, top_shaft), (px + sw / 2, gy))
    d.line((px - 70, gy), (px + 70, gy))                                  # ground

    d.group('mid')
    # arms carved on the shaft: down each edge from the shoulder, bending in to hands above the belt
    belt = gy - 2.5 * e
    for s in (-1, 1):
        x_edge = px + s * (sw / 2 - 6)
        x_in = px + s * 5
        d.line((x_edge, top_shaft + 10), (x_edge, belt - 32), (x_in + s * 6, belt - 12))
        for j in range(4):                                                # fingers
            fy = belt - 15 + j * 3
            d.line((x_in + s * 6, fy), (x_in, fy + 1))
    d.line((px - sw / 2, belt), (px + sw / 2, belt))                      # the belt
    d.line((px - sw / 2, belt - 5), (px + sw / 2, belt - 5))
    d.line((px - 9, belt), (px - 7, belt + 40), (px + 7, belt + 40), (px + 9, belt))   # loincloth
    # dimension line for the height
    dx = px + hw / 2 + 14
    d.line((dx, top), (dx, gy))
    d.line((dx - 4, top), (dx + 4, top))
    d.line((dx - 4, gy), (dx + 4, gy))
    # 10 m scale bar for the plan
    d.line((cx - 5 * m, 286), (cx + 5 * m, 286))
    d.line((cx - 5 * m, 282), (cx - 5 * m, 290))
    d.line((cx + 5 * m, 282), (cx + 5 * m, 290))

    d.group('mid')
    d.text(cx, 30, 'ENCLOSURE IN PLAN · SCHEMATIC', size=7)
    d.text(cx + 5 * m + 8, 289, '10 M', size=7, anchor='start')
    d.text(dx + 6, (top + gy) / 2 + 3, '5.5 M', size=7, anchor='start')
    d.text(px, 30, 'CENTRAL PILLAR', size=7)
    d.text(px, 41, 'ELEVATION', size=7)
    d.text(px, gy + 16, 'ARMS · BELT · LOINCLOTH', size=7)
    return d


def _spikelet(d, x, y, side, h=16, w=9):
    """A wheat spikelet attached at (x, y), leaning out to `side` (-1 left, 1 right): two glumes as a lens."""
    tip = (x + side * w, y - h)
    mid = (x + side * w * 0.2, y - h * 0.55)
    d.curve(f'M{x:.1f} {y:.1f} Q{x + side * w * 1.2:.1f} {y - h * 0.35:.1f} {tip[0]:.1f} {tip[1]:.1f} '
            f'Q{mid[0]:.1f} {mid[1]:.1f} {x:.1f} {y:.1f}')
    return tip


def founder_crops():
    d = D()
    # Left: an ear of einkorn, its spikelets alternating up a zigzag rachis, each joined to the rachis
    # at a node. Proportions schematic. Right: two rachis segments, magnified, after the criterion
    # archaeobotanists use (Fuller 2007; Tanno and Willcox 2006): a wild ear shatters at ripeness and
    # each segment leaves a smooth abscission scar where it parted from the one below; a domestic ear
    # stays whole until it is threshed, and the segment is torn off, leaving a rough, jagged break.
    ex, base, top = 92, 258, 78
    n = 9
    step = (base - top) / n
    details = ((300, 95, True), (300, 222, False))
    R = 40

    d.group('thin')
    d.line((ex, base + 26), (ex, top - 20))                               # the ear's axis
    for (dx_, dy_, _), sy in zip(details, (base - 7 * step, base - 2 * step)):
        d.circle(ex, sy, 16)
        a = math.atan2(dy_ - sy, dx_ - ex)
        d.line((ex + 16 * math.cos(a), sy + 16 * math.sin(a)), (dx_ - R * math.cos(a), dy_ - R * math.sin(a)))
    for dx_, dy_, _ in details:
        d.circle(dx_, dy_, R)

    d.group()
    nodes = []
    for i in range(n + 1):
        x = ex + (4 if i % 2 else -4)
        nodes.append((x, base - i * step))
    d.line((ex, base + 26), *nodes)                                       # stem and zigzag rachis
    for i, (x, y) in enumerate(nodes[1:], start=1):
        side = 1 if i % 2 else -1
        tip = _spikelet(d, x, y, side, h=20, w=11)
        d.line(tip, (tip[0] + side * 4, tip[1] - 16))                     # an awn

    for dx_, dy_, wild in details:
        # a rachis segment: a wedge, wider at the node above, its spikelet leaning off to the right
        yt, yb = dy_ - 12, dy_ + 26
        tl, tr, bl, br = (dx_ - 9, yt), (dx_ + 9, yt), (dx_ - 6, yb), (dx_ + 6, yb)
        d.line(bl, tl, tr, br)
        if wild:
            d.arc(dx_, yb, 6, 180, 0, n=16, ry=-4)                        # smooth concave scar
        else:
            pts = [bl]
            for k in range(1, 6):
                pts.append((dx_ - 6 + 12 * k / 6, yb + (4 if k % 2 else -1)))
            pts.append(br)
            d.line(*pts)                                                  # torn, jagged break
        _spikelet(d, dx_ + 7, yt + 2, 1, h=20, w=16)

    d.group('mid')
    d.text(ex, 24, 'EAR OF EINKORN', size=7)
    d.text(ex, 296, 'RACHIS NODES', size=7)
    d.text(300, 47, 'WILD · SHATTERS', size=7)
    d.text(300, 147, 'SMOOTH SCAR', size=7)
    d.text(300, 174, 'DOMESTIC · THRESHED', size=7)
    d.text(300, 274, 'TORN BREAK', size=7)
    return d


def first_herds():
    d = D()
    # Left: a Neolithic sieve vessel in section, as found in Linear Pottery sites in Kuyavia, Poland,
    # whose milk-fat residues show it was used to strain curds from whey (Salque et al. 2013). A bowl
    # below catches the whey. Shape and hole spacing schematic.
    # Right: a schematic harvest profile, after Zeder and Hesse (2000): herders kill most young males
    # and keep females to breed, so the share of each sex still alive falls apart with age. The curves
    # show the pattern, not the published figures.
    cx = 104
    d.group('thin')
    d.line((cx, 40), (cx, 272))                                           # the vessel's axis
    x0, x1, y0, y1 = 236, 382, 230, 70                                    # chart box
    for k in range(5):
        x = x0 + (x1 - x0) * k / 4
        d.line((x, y0), (x, y1))
    for k in range(5):
        y = y0 - (y0 - y1) * k / 4
        d.line((x0, y), (x1, y))

    d.group()
    # the sieve: a deep bowl with a flared rim, wall drawn as two profiles, holes through the wall
    rim, foot = 70, 178
    def prof(t, r_rim, r_foot):
        y = rim + (foot - rim) * t
        r = r_foot + (r_rim - r_foot) * (1 - t) ** 0.8
        return r, y
    outer = [prof(i / 20, 58, 30) for i in range(21)]
    inner = [prof(i / 20, 52, 25) for i in range(21)]
    d.line(*[(cx - r, y) for r, y in outer], *[(cx + r, y) for r, y in reversed(outer)])
    d.line(*[(cx - r, y) for r, y in inner], (cx - 25, foot - 6), (cx + 25, foot - 6),
           *[(cx + r, y) for r, y in reversed(inner)])
    # the catch bowl below
    d.arc(cx, 216, 66, 0, 180, n=40, ry=40)
    d.line((cx - 66, 216), (cx + 66, 216))
    # chart axes and the two curves
    d.line((x0, y1), (x0, y0), (x1, y0))
    def cpx(age):
        return x0 + (x1 - x0) * age / 8
    def cpy(share):
        return y0 - (y0 - y1) * share
    females = [(cpx(a), cpy(math.exp(-a / 9.5))) for a in [i * 0.25 for i in range(33)]]
    males = [(cpx(a), cpy(1 / (1 + math.exp(3.2 * (a - 1.6))))) for a in [i * 0.25 for i in range(33)]]
    d.line(*females)
    d.dashed(*males, dash=4, gap=3)

    d.group('mid')
    for i in range(6):                                                    # holes through the wall
        for side in (-1, 1):
            r, y = prof(0.25 + i * 0.11, 55, 27.5)
            d.circle(cx + side * r, y, 1.8)
    for k in range(5):                                                    # curd inside
        d.arc(cx, 140 - k * 9, 22 + k * 4, 0, 180, n=24, ry=4)
    for hx in (-14, 0, 14):                                               # holes through the base
        d.circle(cx + hx, 175, 1.6)
    for k, dy in enumerate((190, 200, 208)):                              # whey drops
        d.circle(cx - 8 + k * 8, dy, 1.6)

    d.group('mid')
    d.text(cx, 30, 'SIEVE VESSEL · SECTION', size=7)
    d.text(cx, 160, 'CURDS', size=7)
    d.text(cx, 244, 'WHEY', size=7)
    d.text(cx, 284, 'KUYAVIA · SIXTH MILLENNIUM BC', size=7)
    d.text((x0 + x1) / 2, 50, 'HERDED GOATS ALIVE', size=7)
    d.text((x0 + x1) / 2, 61, 'BY AGE · SCHEMATIC', size=7)
    d.text(cpx(5.6), cpy(0.42) + 4, 'FEMALES', size=7)
    d.text(cpx(3.1), cpy(0.08) - 6, 'MALES', size=7, anchor='start')
    for a in (0, 4, 8):
        d.text(cpx(a), y0 + 12, str(a), size=7)
    d.text((x0 + x1) / 2, y0 + 24, 'AGE · YEARS', size=7)
    return d


PLATES = {'gobekli-tepe': gobekli_tepe, 'founder-crops': founder_crops, 'first-herds': first_herds}
