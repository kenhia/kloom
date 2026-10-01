"""Plates for In the Blood's trail Beyond ABO, its first two frames (sprint 028, part groups1). See plates_for.py."""
import math
import random
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


def _ring(cx, cy, r, n=8):
    """A small closed polygon standing in for a circle, so many cells can share one path."""
    pts = [_pt(cx, cy, r, 360 * i / n) for i in range(n)]
    return pts + [pts[0]]


def _crust(cx, cy, r, seed):
    """An irregular flake of dried blood: a circle with a seeded wobble."""
    rnd = random.Random(seed)
    k = [rnd.uniform(0.75, 1.15) for _ in range(11)]
    pts = []
    for i in range(45):
        a = 2 * math.pi * i / 44
        j = (i * 11 / 44)
        lo, hi = int(j) % 11, (int(j) + 1) % 11
        t = j - int(j)
        rr = r * (k[lo] * (1 - t) + k[hi] * t)
        pts.append((cx + rr * math.cos(a), cy + 0.8 * rr * math.sin(a)))
    return pts


def forensic_typing():
    d = D()
    # The Lattes cover-slip test, as Wiener's 1946 manual sets it out: three slides, each with an
    # equal flake of the dried crust, a drop of 2% suspension of known O, A1 and B cells, and a
    # cover slip. The stain drawn here is invented and is group B: its serum carries anti-A, so the
    # A cells clump at the edge of the crust and the B and O cells stay free. Above, one slide in
    # section. Cell positions are seeded, not data.
    rnd = random.Random(1915)
    cols = [(80, 'O CELLS', False), (200, 'A CELLS', True), (320, 'B CELLS', False)]
    cy, half = 196, 46                                   # each cover slip is a square 92 wide
    d.group('thin')
    d.line((20, cy), (380, cy))                          # the axis the three crusts sit on
    for cx, _, _ in cols:
        d.line((cx, 118), (cx, 258))
    d.line((40, 64), (360, 64))                          # the section's centre line
    d.line((200, 40), (200, 88))
    d.group()
    # the section: slide, crust and cover slip, the drop filling the gap between them
    d.line((40, 76), (360, 76), (360, 86), (40, 86), closed=True)          # glass slide
    d.line((154, 62), (246, 62), (246, 66), (154, 66), closed=True)        # cover slip
    d.line((186, 76), (190, 71), (200, 70), (210, 71.5), (214, 76))        # the crust, lying on the slide
    # the three slides in plan: a cover slip each, and the crust under it
    for k, (cx, _, _) in enumerate(cols):
        d.line((cx - half, cy - half), (cx + half, cy - half), (cx + half, cy + half),
               (cx - half, cy + half), closed=True)
        d.line(*_crust(cx, cy, 11, 28 + k), closed=True)
    d.group('mid')
    # the drop spread under the cover slip, ending at the glass
    d.line((158, 66), (162, 70), (186, 74))
    d.line((242, 66), (238, 70), (214, 74))
    # cells: free and scattered, or, on the A slide, clumped in a ring at the crust's edge
    for cx, _, clumped in cols:
        segs = []
        if clumped:
            for c in range(9):
                a = 360 * c / 9 + rnd.uniform(-12, 12)
                gx, gy = _pt(cx, cy, rnd.uniform(18, 26), a)
                for _ in range(rnd.randint(5, 8)):
                    segs.append(_ring(gx + rnd.uniform(-4.5, 4.5), gy + rnd.uniform(-4.5, 4.5), 1.8))
            for _ in range(10):
                x, y = cx + rnd.uniform(-40, 40), cy + rnd.uniform(-40, 40)
                if math.hypot(x - cx, y - cy) > 34:
                    segs.append(_ring(x, y, 1.8))
        else:
            n = 0
            while n < 46:
                x, y = cx + rnd.uniform(-41, 41), cy + rnd.uniform(-41, 41)
                if math.hypot(x - cx, (y - cy) / 0.8) > 15:
                    segs.append(_ring(x, y, 1.8))
                    n += 1
        d.lines(segs)
    # the clear zone where the crust is dissolving, on each slide
    for cx, _, _ in cols:
        d.arc(cx, cy, 15, 0, 360, n=40, ry=12)
    d.group('mid')
    for cx, label, _ in cols:
        d.text(cx, 258, label, size=7)
    d.text(200, 30, 'CRUST UNDER A COVER SLIP, IN SECTION', size=7)
    d.text(200, 278, 'A STAIN OF GROUP B CLUMPS A CELLS ONLY', size=7)
    d.text(200, 100, 'SLIDE', size=7)
    return d


def bernstein():
    d = D()
    # Two hypotheses drawn to scale for the 502 Japanese in Bernstein's data (Crow 1993).
    # Left, one gene with three alleles: a square whose sides are divided in the allele
    # frequencies p, q and r found from the counts (our arithmetic, scaled to sum to one); each
    # rectangle's area is a genotype's frequency under Hardy-Weinberg proportions, and the two
    # pq rectangles together are AB. Right, two independent genes: a square divided at the share
    # carrying A (A + AB = 0.500) and the share carrying B (B + AB = 0.284); the corner they share
    # is the AB the two-gene model must predict.
    O, A, B, AB = 0.294, 0.422, 0.206, 0.078
    pa, pb, r = 1 - math.sqrt(O + B), 1 - math.sqrt(O + A), math.sqrt(O)
    s = pa + pb + r
    p, q, r = pa / s, pb / s, r / s
    x0, y0, side = 30, 70, 150
    cuts = [0, p, p + q, 1]
    xs = [x0 + side * c for c in cuts]
    ys = [y0 + side * c for c in cuts]
    X0, Y0 = 230, 70
    ta, tb = A + AB, B + AB
    d.group('thin')
    for x in xs[1:-1]:
        d.line((x, y0 - 12), (x, y0 + side))
    for y in ys[1:-1]:
        d.line((x0 - 12, y), (x0 + side, y))
    d.line((X0 + side * ta, Y0 - 12), (X0 + side * ta, Y0 + side))
    d.line((X0 - 12, Y0 + side * (1 - tb)), (X0 + side, Y0 + side * (1 - tb)))
    d.group()
    d.line((x0, y0), (x0 + side, y0), (x0 + side, y0 + side), (x0, y0 + side), closed=True)
    d.line((X0, Y0), (X0 + side, Y0), (X0 + side, Y0 + side), (X0, Y0 + side), closed=True)
    d.group('mid')
    # hatch the AB cells: on the left the two p-by-q rectangles, on the right the shared corner
    segs = []
    for (ax, bx, ay, by) in ((xs[0], xs[1], ys[1], ys[2]), (xs[1], xs[2], ys[0], ys[1])):
        k = ax - (by - ay)
        while k < bx:
            p0 = (max(ax, k), ay + max(0, ax - k))
            p1 = (min(bx, k + (by - ay)), ay + min(by - ay, bx - k))
            if p1[0] > p0[0]:
                segs.append([p0, p1])
            k += 5
    ax, bx = X0, X0 + side * ta
    ay, by = Y0 + side * (1 - tb), Y0 + side
    k = ax - (by - ay)
    while k < bx:
        p0 = (max(ax, k), ay + max(0, ax - k))
        p1 = (min(bx, k + (by - ay)), ay + min(by - ay, bx - k))
        if p1[0] > p0[0]:
            segs.append([p0, p1])
        k += 5
    d.lines(segs)
    d.group('mid')
    for i, a in enumerate('ABO'):
        d.text((xs[i] + xs[i + 1]) / 2, y0 - 16, a, size=7)
        d.text(x0 - 16, (ys[i] + ys[i + 1]) / 2 + 3, a, size=7)
    names = [['A', 'AB', 'A'], ['AB', 'B', 'B'], ['A', 'B', 'O']]
    for i in range(3):
        for j in range(3):
            if names[i][j] != 'AB':
                d.text((xs[j] + xs[j + 1]) / 2, (ys[i] + ys[i + 1]) / 2 + 3, names[i][j], size=7)
    d.text(X0 + side * ta / 2, Y0 + side * (1 - tb) / 2 + 3, 'A ONLY', size=7)
    d.text(X0 + side * (1 + ta) / 2, Y0 + side * (1 - tb) / 2 + 3, 'O', size=7)
    d.text(X0 + side * (1 + ta) / 2, Y0 + side * (1 - tb / 2) + 3, 'B ONLY', size=7)
    d.text(X0 + side * ta / 2, Y0 - 16, 'A 0.500', size=7)
    d.text(X0 - 5, Y0 + side * (1 - tb / 2) + 3, '0.284', size=7, anchor='end')
    d.text(X0 - 5, Y0 + side * (1 - tb / 2) - 7, 'B', size=7, anchor='end')
    d.text(x0 + side / 2, y0 + side + 22, 'ONE GENE: AB 0.092', size=7)
    d.text(X0 + side / 2, Y0 + side + 22, 'TWO GENES: AB 0.142', size=7)
    d.text(200, y0 + side + 44, 'OBSERVED AB 0.078', size=7)
    return d


PLATES = {'forensic-typing': forensic_typing, 'bernstein': bernstein}
