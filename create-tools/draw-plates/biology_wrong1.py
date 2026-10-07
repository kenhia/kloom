"""Plates for The Story of Life's part wrong1 (sprint 055): preformation, pangenesis, piltdown. See plates_for.py."""
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


def _teardrop(cx, cy, r, tip=1.9, n=40):
    """A sperm's head: a circle of radius r with tangents to a point tip*r below its centre."""
    t = math.degrees(math.acos(1 / tip))
    a0, a1 = 90 + t, 90 - t + 360            # from the left tangent point over the top to the right one
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return pts + [(cx, cy + tip * r), pts[0]]


def _homunculus(d, cx, cy, r):
    """Hartsoeker's curled figure, schematic and in profile, inside a head of radius r: a bowed head, a
    curved back, the thigh drawn up to the chest and the shin folded under it."""
    hx, hy = cx - 0.08 * r, cy - 0.42 * r
    d.circle(hx, hy, 0.2 * r)                                                    # head, bowed
    back = [(cx + 0.42 * r * math.cos(math.radians(a)), cy + 0.08 * r + 0.42 * r * math.sin(math.radians(a)))
            for a in range(-70, 101, 10)]
    d.line(*back)                                                                # the curled back
    knee = (cx - 0.3 * r, cy - 0.05 * r)
    foot = (cx - 0.12 * r, cy + 0.48 * r)
    d.line(back[-1], knee, foot, back[-1])                                       # thigh up, shin down
    d.line((cx + 0.05 * r, cy - 0.22 * r), (knee[0] + 0.06 * r, knee[1] + 0.02 * r))   # arm round the knee


def preformation():
    d = D()
    # Emboitement as a geometric series. Each generation's sperm is drawn 0.6 the size of the one before
    # and placed so that tops and tail tips lie on straight rays to one vanishing point: a series shrinking
    # by a constant ratio. Below, the true sizes on a log axis: a man of 1.7 m, a homunculus the length of a
    # sperm's head (5.1 um), and the next one down, 5.1 um x (5.1 um / 1.7 m) = 15 pm, smaller than an atom.
    r_draw, gens = 0.6, 6
    vx, vy = 376, 116
    heads = []
    for k in range(gens):
        s = r_draw ** k
        heads.append((vx - 300 * s, vy - 44 * s, 22 * s, 96 * s))   # centre x, centre y, head radius, tail length

    # log axis: 10^1 m at x0 to 10^-12 m at x1
    x0, x1, ay = 30, 380, 236
    dec = (x1 - x0) / 13

    def ax(metres):
        return x0 + (1 - math.log10(metres)) * dec

    d.group('thin')
    top0 = (heads[0][0], heads[0][1] - heads[0][2])
    tip0 = (heads[0][0], heads[0][1] + 1.9 * heads[0][2] + heads[0][3])
    d.line(top0, (vx, vy))                                          # the rays the series converges on
    d.line(tip0, (vx, vy))
    d.line((x0, ay), (x1, ay))
    for i in range(14):
        x = x0 + i * dec
        d.line((x, ay - 3), (x, ay + 3))
    d.line((ax(5.2e-10), ay - 10), (ax(5.2e-10), ay - 6), (ax(6.2e-11), ay - 6), (ax(6.2e-11), ay - 10))

    d.group()
    for cx, cy, r, tail in heads:
        d.line(*_teardrop(cx, cy, r))
        y0 = cy + 1.9 * r
        n = 30
        amp = 0.18 * r
        d.line(*[(cx + amp * math.sin(i / n * 3 * math.pi), y0 + tail * i / n) for i in range(n + 1)])

    d.group('mid')
    for cx, cy, r, tail in heads[:4]:
        _homunculus(d, cx, cy + 0.05 * r, 1.3 * r)
    for m in (1.7, 5.1e-6, 1.53e-11):                              # the three sizes on the axis
        x = ax(m)
        d.circle(x, ay, 2.5)

    d.group('mid')
    d.text(heads[0][0], 26, 'GENERATION 1 · 5 µM', size=7)
    for k in (1, 2, 3):
        d.text(heads[k][0], heads[k][1] - heads[k][2] - 8, str(k + 1), size=7)
    d.text(318, 196, 'EACH DRAWN 0.6 OF THE LAST', size=7)
    d.text(318, 206, 'TRUE RATIO ABOUT 1 : 330,000', size=7)
    for m, lab in ((10, '10 M'), (1e-3, '1 MM'), (1e-6, '1 µM'), (1e-9, '1 NM'), (1e-12, '1 PM')):
        d.text(ax(m), ay + 14, lab, size=7)
    d.text(ax(1.7) + 4, ay - 10, 'MAN 1.7 M', size=7, anchor='start')
    d.text(ax(5.1e-6), ay + 26, 'HOMUNCULUS 5 µM', size=7)
    d.text(ax(1.53e-11), ay + 26, 'NEXT 15 PM', size=7)
    d.text((ax(5.2e-10) + ax(6.2e-11)) / 2, ay - 14, 'ATOMS', size=7)
    d.text(200, 288, 'EMBOÎTEMENT · BOXES IN BOXES', size=7)
    return d


def pangenesis():
    d = D()
    # Left, Darwin's pangenesis (1868): every part of the body throws off gemmules, which travel to the
    # gonad and into the next generation. Right, Weismann's germ plasm (1883-92): a germ line runs on from
    # generation to generation, each body grows from it, and nothing passes back from body to germ.
    # Both are diagrams of the ideas, not of any animal; positions are chosen, not measured.
    g = (110, 176)                                                    # the gonad
    parts = [(62, 72), (110, 58), (158, 72), (52, 150), (170, 150), (82, 214), (140, 214)]

    d.group('thin')
    d.line((200, 30), (200, 270))                                      # the divide
    for x in (250, 310, 370):
        d.line((x, 40), (x, 250))                                      # one column per generation

    d.group()
    # a body as geometry: a head circle, a trunk ellipse and four limbs
    d.circle(110, 62, 16)
    d.ellipse(110, 145, 44, 62)
    d.line((70, 110), (48, 76))
    d.line((150, 110), (172, 76))
    d.line((90, 202), (80, 232))
    d.line((130, 202), (140, 232))
    # the germ line and the bodies grown from it
    ys = 220
    for x in (250, 310, 370):
        d.circle(x, ys, 7)
        d.ellipse(x, 104, 20, 30)
    for x0, x1 in ((257, 303), (317, 363)):
        d.line((x0, ys), (x1, ys))
        _arrow(d, (x0, ys), (x1, ys))
    d.line((226, ys), (243, ys))

    d.group('mid')
    d.circle(*g, 9)
    for p in parts:
        for t in (0.25, 0.5, 0.75):                                    # gemmules on their way
            d.circle(p[0] + (g[0] - p[0]) * t, p[1] + (g[1] - p[1]) * t, 1.6)
        q = (g[0] + (p[0] - g[0]) * 0.17, g[1] + (p[1] - g[1]) * 0.17)
        d.line((p[0] + (g[0] - p[0]) * 0.08, p[1] + (g[1] - p[1]) * 0.08), q)
        _arrow(d, p, q, size=4)
    d.line((g[0], g[1] + 9), (g[0], 262))
    _arrow(d, (g[0], g[1]), (g[0], 262))
    for x in (250, 310, 370):
        d.line((x, ys - 7), (x, 138))                                  # germ to body
        _arrow(d, (x, ys), (x, 138), size=4)
        d.dashed((x + 8, 134), (x + 8, ys - 12), dash=3, gap=3)        # body to germ: the way that is shut
        d.line((x + 3, 176), (x + 13, 186))
        d.line((x + 13, 176), (x + 3, 186))

    d.group('mid')
    d.text(110, 26, 'DARWIN 1868', size=7)
    d.text(310, 26, 'WEISMANN 1885', size=7)
    d.text(130, 179, 'GONAD', size=7, anchor='start')
    d.text(20, 192, 'GEMMULES', size=7, anchor='start')
    d.text(110, 276, 'NEXT GENERATION', size=7)
    d.text(310, 60, 'BODY', size=7)
    d.text(310, 244, 'GERM PLASM', size=7)
    d.text(284, 160, 'NO RETURN', size=7)
    for i, x in enumerate((250, 310, 370)):
        d.text(x, 262, str(i + 1), size=7)
    return d


def _hatch(d, poly, step=5, angle=45):
    """Parallel hatching clipped to a convex polygon, for the parts that did not belong."""
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)                         # hatch direction
    nx, ny = -uy, ux                                          # its normal
    ds = [x * nx + y * ny for x, y in poly]
    k = math.ceil(min(ds) / step)
    while k * step < max(ds):
        c = k * step
        hits = []
        for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
            d0, d1 = x0 * nx + y0 * ny - c, x1 * nx + y1 * ny - c
            if d0 * d1 < 0:
                t = d0 / (d0 - d1)
                hits.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0)))
        if len(hits) >= 2:
            hits.sort(key=lambda p: p[0] * ux + p[1] * uy)
            d.line(hits[0], hits[-1])
        k += 1


def _band(cx, cy, rx, ry, t, a0, a1, n=16):
    """A fragment of the vault: the band between two concentric ellipses, from angle a0 to a1."""
    outer = [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
              cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    inner = [(cx + (rx - t) * math.cos(math.radians(a1 - (a1 - a0) * i / n)),
              cy + (ry - t) * math.sin(math.radians(a1 - (a1 - a0) * i / n))) for i in range(n + 1)]
    return outer + inner + [outer[0]]


def piltdown():
    d = D()
    # Piltdown I as found (1912-13), in left side view: the pieces of a thick human braincase set on
    # Woodward's reconstruction (dashed), and the parts that did not belong, hatched: the orangutan jaw,
    # broken at the chin and at the joint so it could not be tried against the skull, its molars filed
    # flat, and the canine found in 1913. Schematic; fragment extents follow the published descriptions
    # only roughly.
    cx, cy, rx, ry, t = 182, 128, 118, 80, 9

    d.group('thin')
    vault = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in range(170, 371, 5)]
    d.dashed(*vault, dash=4, gap=3)
    face = [(66, 142), (58, 150), (62, 162), (56, 176), (68, 190), (92, 198), (160, 196)]
    d.dashed(*face, dash=4, gap=3)
    jaw = [(92, 204), (96, 236), (150, 240), (206, 232), (220, 196), (226, 168)]
    d.dashed(*jaw, dash=4, gap=3)
    d.dashed((300, 128), (300, 168), (226, 168), dash=4, gap=3)        # back of the skull to the joint
    d.line((cx - 6, cy), (cx + 6, cy))
    d.line((cx, cy - 6), (cx, cy + 6))

    d.group()
    for a0, a1 in ((196, 236), (250, 298), (316, 346)):                # frontal, parietal, occipital pieces
        d.line(*_band(cx, cy, rx, ry, t, a0, a1))
    temporal = [(214, 142), (246, 138), (258, 156), (238, 170), (216, 164)]
    d.line(*temporal, closed=True)
    mand = [(132, 206), (176, 205), (204, 196), (214, 186), (217, 214), (206, 229), (138, 232), (128, 220)]
    d.line(*mand, closed=True)
    canine = [(318, 196), (326, 178), (334, 196), (332, 228), (326, 240), (320, 228)]
    d.line(*canine, closed=True)

    d.group('mid')
    _hatch(d, mand)
    _hatch(d, canine, step=4)
    for x in (140, 158):                                               # the two molars, planed flat
        d.line((x, 205), (x, 199), (x + 15, 199), (x + 15, 205))
    d.line((214, 186), (210, 191), (216, 196), (212, 201), (217, 206))  # broken ramus
    d.line((132, 206), (128, 211), (133, 215), (128, 220))              # broken chin

    d.group('mid')
    d.text(182, 32, 'HUMAN BRAINCASE · STAINED', size=7)
    d.text(150, 254, 'ORANGUTAN JAW · FILED, STAINED', size=7)
    d.text(326, 256, 'CANINE · 1913', size=7)
    d.text(340, 104, 'DASHED: THE', size=7)
    d.text(340, 114, 'RECONSTRUCTION', size=7)
    d.text(200, 286, 'PILTDOWN I AS FOUND · 1912–13', size=7)
    return d


PLATES = {
    'preformation': preformation,
    'pangenesis': pangenesis,
    'piltdown': piltdown,
}
