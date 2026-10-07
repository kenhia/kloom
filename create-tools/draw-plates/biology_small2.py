"""Plates for The Story of Life's frames written by part small2 in sprint 055 (Seeing small:
the achromatic microscope, cell theory, Virchow). See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _lens_face(cx, h, sag, side, n=16):
    """Points down one face of a lens: a circular arc of half-height h bulging by sag to side."""
    r = (h * h + sag * sag) / (2 * sag)
    pts = []
    for k in range(n + 1):
        y = -h + 2 * h * k / n
        x = math.sqrt(r * r - y * y) - (r - sag)
        pts.append((cx + side * x, y))
    return pts


def achromatic_microscope():
    d = D()
    # Two ray diagrams on one axis each. Above, a single convex lens: parallel light splits, the blue
    # rays (solid) meeting nearer the lens than the red (dashed), so no screen catches a point. Below,
    # a cemented doublet, a convex crown lens and a plano-concave flint lens behind it: the flint's
    # greater dispersion undoes the crown's, and the two colors meet at one focus. Thin-lens geometry;
    # the spread of the colors is exaggerated many times to be seen.
    rows = [(92, 'single'), (212, 'doublet')]
    lx, x0 = 120, 30
    heights = (-26, -14, 14, 26)

    d.group('thin')
    for cy, _ in rows:
        d.line((x0 - 6, cy), (392, cy))                                  # optical axis
    fb, fr, fa = lx + 150, lx + 196, lx + 176
    for x in (fb, fr):
        d.line((x, rows[0][0] - 34), (x, rows[0][0] + 34))
    d.line((fa, rows[1][0] - 34), (fa, rows[1][0] + 34))

    d.group()
    cy = rows[0][0]                                                       # the single lens
    front = [(x, y + cy) for x, y in _lens_face(lx, 34, 7, -1)]
    back = [(x, y + cy) for x, y in _lens_face(lx, 34, 7, 1)][::-1]
    d.line(*front, *back, closed=True)
    cy = rows[1][0]                                                       # crown, then flint
    front = [(x, y + cy) for x, y in _lens_face(lx - 4, 34, 7, -1)]
    joint = [(x, y + cy) for x, y in _lens_face(lx - 4, 34, 7, 1)]
    d.line(*front, *joint[::-1], closed=True)
    d.line(*joint, (lx + 12, cy + 34), (lx + 12, cy - 34), joint[0])

    d.group('mid')
    for y in heights:                                                     # incoming white light
        for cy, _ in rows:
            d.line((x0, cy + y), (lx - 8, cy + y))
            _arrow(d, (x0, cy + y), (x0 + 22, cy + y), size=3.5)
    cy = rows[0][0]
    for y in heights:
        d.line((lx + 6, cy + y), (fb, cy), (fb + (fb - lx) * 0.35, cy - y * 0.35))
        d.dashed((lx + 6, cy + y), (fr, cy), (fr + (fr - lx) * 0.25, cy - y * 0.25), dash=3, gap=2)
    cy = rows[1][0]
    for y in heights:
        d.line((lx + 12, cy + y), (fa, cy), (fa + (fa - lx) * 0.35, cy - y * 0.35))
        d.dashed((lx + 12, cy + y * 0.98), (fa, cy), (fa + (fa - lx) * 0.33, cy - y * 0.33), dash=3, gap=2)

    d.group('mid')
    cy = rows[0][0]
    d.text(lx, cy - 44, 'ONE LENS', size=7)
    d.text(fb - 8, cy + 46, 'BLUE, SOLID', size=7)
    d.text(fr + 14, cy + 46, 'RED, DASHED', size=7)
    cy = rows[1][0]
    d.text(lx - 22, cy - 44, 'CROWN', size=7)
    d.text(lx + 26, cy - 44, 'FLINT', size=7)
    d.text(fa, cy + 46, 'ONE FOCUS', size=7)
    d.text(46, rows[0][0] - 36, 'WHITE LIGHT', size=7)
    d.text(200, 290, 'CHROMATIC ABERRATION AND ITS CURE · SCHEMATIC', size=7)
    return d


def _blob(cx, cy, r, wobble, phase, n=40):
    """A closed rounded outline: a circle of radius r with a gentle wobble, for a cell or a nucleus."""
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        rr = r * (1 + wobble * math.sin(3 * t + phase) + wobble * 0.6 * math.cos(2 * t + phase * 1.7))
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    return pts


def cell_theory():
    d = D()
    # Schwann's comparison (Microscopical Researches, Plate I, figs. 1 and 4), redrawn as geometry.
    # Left, onion parenchyma: polygonal plant cells from a Voronoi-like set of centers, each wall
    # straight, a nucleus with its nucleolus lying against a wall. Right, cells of the notochord of a
    # fish: larger, rounder, packed, each with its nucleus on the wall. Between them, what Schwann
    # matched: the nucleus, drawn large, the same in both.
    d.group('thin')
    d.line((200, 40), (200, 250))
    for cx in (100, 300):
        d.circle(cx, 140, 92)
    d.line((140, 270), (260, 270))

    # plant cells: a hexagonal tiling, slightly sheared, clipped to the circle
    d.group()
    s = 30
    for row in range(-3, 4):
        for col in range(-3, 4):
            cx = 100 + col * s * 1.5
            cy = 140 + row * s * math.sqrt(3) + (col % 2) * s * math.sqrt(3) / 2
            if math.hypot(cx - 100, cy - 140) > 62:
                continue
            hexa = [(cx + s * 0.98 * math.cos(math.pi / 3 * k), cy + s * 0.98 * math.sin(math.pi / 3 * k) * 0.92)
                    for k in range(6)]
            d.line(*hexa, closed=True)
    # animal (notochord) cells: rounded, packed in a ring of five round one
    chord = [(300, 140, 27)] + [(300 + 58 * math.cos(a), 140 + 54 * math.sin(a), 24)
                               for a in [math.radians(t) for t in (18, 90, 162, 234, 306)]]
    for i, (cx, cy, r) in enumerate(chord):
        d.line(*_blob(cx, cy, r, 0.06, i), closed=True)

    d.group('mid')
    for row in range(-3, 4):                                              # plant nuclei, against a wall
        for col in range(-3, 4):
            cx = 100 + col * s * 1.5
            cy = 140 + row * s * math.sqrt(3) + (col % 2) * s * math.sqrt(3) / 2
            if math.hypot(cx - 100, cy - 140) > 62:
                continue
            nx, ny = cx + 9 * math.cos(row + col), cy + 9 * math.sin(row + col)
            d.ellipse(nx, ny, 5, 4)
            d.circle(nx + 1, ny - 0.5, 1.2)
    for i, (cx, cy, r) in enumerate(chord):                               # notochord nuclei, on the wall
        a = 0.7 + i * 1.3
        nx, ny = cx + (r - 8) * math.cos(a), cy + (r - 8) * math.sin(a)
        d.ellipse(nx, ny, 5.5, 4.5)
        d.circle(nx + 1, ny - 0.5, 1.3)

    d.group()
    for cx in (176, 224):                                                 # the matched nucleus, enlarged
        d.ellipse(cx, 268, 14, 11)
        d.circle(cx + 2, 266, 3.5)
    d.line((192, 268), (208, 268))

    d.group('mid')
    d.text(100, 30, 'ONION · PLANT', size=7)
    d.text(300, 30, 'NOTOCHORD · FISH', size=7)
    d.text(100, 252, 'PLATE I, FIG. 1', size=7)
    d.text(300, 252, 'PLATE I, FIG. 4', size=7)
    d.text(120, 271, 'NUCLEUS', size=7, anchor='end')
    d.text(280, 271, 'NUCLEUS', size=7, anchor='start')
    d.text(200, 292, 'SCHWANN · MIKROSKOPISCHE UNTERSUCHUNGEN · 1839', size=7)
    return d


def _thread(cx, cy, r, seed, n=7, pts=9):
    """Coiled chromatin threads inside radius r: smooth random walks, the same every run."""
    out = []
    for k in range(n):
        a = seed * 1.7 + k * 2.399
        x, y = cx + r * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a)
        path = [(x, y)]
        h = a + 1.5
        for j in range(pts):
            h += 1.1 * math.sin(seed + k * 3.1 + j * 1.9)
            x2, y2 = x + 5 * math.cos(h), y + 5 * math.sin(h)
            if math.hypot(x2 - cx, y2 - cy) > r * 0.85:
                h += math.pi * 0.8
                x2, y2 = x + 5 * math.cos(h), y + 5 * math.sin(h)
            x, y = x2, y2
            path.append((x, y))
        out.append(path)
    return out


def virchow():
    d = D()
    # Above: omnis cellula e cellula as a lineage, one cell becoming two becoming four. Below: one
    # division in the stages Flemming drew in salamander cells (1882): the resting nucleus, the coiled
    # threads, the threads gathered at the equator, the two halves drawn apart, two daughter nuclei
    # and a furrow between them. Schematic; the threads are drawn as computed coils, not counted.
    xs = [44, 122, 200, 278, 356]
    cy, R = 212, 30

    d.group('thin')
    d.line((20, cy), (380, cy))
    d.line((200, 26), (200, 98))
    for x in xs:
        d.line((x, cy - R - 10), (x, cy + R + 10))

    d.group()
    gens = [[(200, 40)], [(150, 76), (250, 76)], [(122, 116), (178, 116), (222, 116), (278, 116)]]
    for g, nxt in zip(gens, gens[1:]):
        for i, (x, y) in enumerate(g):
            for (x2, y2) in nxt[2 * i:2 * i + 2]:
                d.line((x, y + 9), (x2, y2 - 9))
    for g in gens:
        for x, y in g:
            d.circle(x, y, 9)
    for k, x in enumerate(xs):                                            # cell outlines through division
        if k < 4:
            rx = R * (1 + 0.08 * k)
            d.ellipse(x, cy, rx, R)
        else:
            d.curve(f'M{x - 2},{cy - R} C{x - 40},{cy - R - 2} {x - 40},{cy + R + 2} {x - 2},{cy + R}'
                    f' C{x - 6},{cy + 8} {x - 6},{cy - 8} {x - 2},{cy - R}')
            d.curve(f'M{x + 2},{cy - R} C{x + 40},{cy - R - 2} {x + 40},{cy + R + 2} {x + 2},{cy + R}'
                    f' C{x + 6},{cy + 8} {x + 6},{cy - 8} {x + 2},{cy - R}')

    d.group('mid')
    for g in gens:                                                        # nuclei in the lineage
        for x, y in g:
            d.circle(x, y, 3)
    d.circle(xs[0], cy, 15)                                               # 1: resting nucleus, fine net
    for p in _thread(xs[0], cy, 15, 1, n=6, pts=5):
        d.line(*p)
    d.circle(xs[1], cy, 17)                                               # 2: coiled threads (skein)
    for p in _thread(xs[1], cy, 17, 2, n=7, pts=10):
        d.line(*p)
    for k in range(9):                                                    # 3: threads at the equator
        y = cy - 18 + k * 4.5
        d.line((xs[2] - 6, y - 2), (xs[2], y), (xs[2] - 6, y + 2))
        d.line((xs[2] + 6, y - 2), (xs[2], y), (xs[2] + 6, y + 2))
    for s in (-1, 1):                                                     # spindle poles
        d.circle(xs[2] + s * 24, cy, 1.8)
        d.circle(xs[3] + s * 30, cy, 1.8)
        for k in range(5):
            y = cy - 16 + k * 8
            d.line((xs[2] + s * 24, cy), (xs[2] + s * 4, y))
    for s in (-1, 1):                                                     # 4: two halves drawn apart
        for k in range(6):
            y = cy - 12 + k * 4.8
            d.line((xs[3] + s * 16, y), (xs[3] + s * 24, cy + (y - cy) * 0.4))
    for s in (-1, 1):                                                     # 5: two daughter nuclei
        d.circle(xs[4] + s * 18, cy, 10)
        for p in _thread(xs[4] + s * 18, cy, 10, 5 + s, n=4, pts=5):
            d.line(*p)

    d.group('mid')
    for x, t in zip(xs, ('RESTING', 'SKEIN', 'EQUATOR', 'APART', 'TWO CELLS')):
        d.text(x, cy + R + 22, t, size=7)
    d.text(318, 44, 'ONE', size=7, anchor='start')
    d.text(318, 80, 'TWO', size=7, anchor='start')
    d.text(318, 120, 'FOUR', size=7, anchor='start')
    d.text(200, 290, 'OMNIS CELLULA E CELLULA · DIVISION AS FLEMMING DREW IT, 1882', size=7)
    return d


PLATES = {
    'achromatic-microscope': achromatic_microscope,
    'cell-theory': cell_theory,
    'virchow': virchow,
}
