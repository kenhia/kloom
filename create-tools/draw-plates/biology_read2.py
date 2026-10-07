"""Plates for The Story of Life's part read2 (sprint 055): Woese's archaea, Dolly, the human genome.
See plates_for.py."""
import math
import random
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


# Woese and Fox 1977, Table 1: association coefficients S_AB between 16S (18S) rRNA catalogs,
# read off the printed page. Order as printed: three eukaryotes, five bacteria and a chloroplast,
# four methanogens.
WF_NAMES = ['YEAST', 'DUCKWEED', 'MOUSE L CELL', 'E. COLI', 'CHLOROBIUM', 'BACILLUS',
            'CORYNEBACTERIUM', 'APHANOCAPSA', 'CHLOROPLAST', 'M. THERMOAUTOTROPHICUM',
            'M. RUMINANTIUM', 'METHANOBACTERIUM JR-1', 'METHANOSARCINA']
WF_TABLE = """- .29 .33 .05 .06 .08 .09 .11 .08 .11 .11 .08 .08
.29 - .36 .10 .05 .06 .10 .09 .11 .10 .10 .13 .07
.33 .36 - .06 .06 .07 .07 .09 .06 .10 .10 .09 .07
.05 .10 .06 - .24 .25 .28 .26 .21 .11 .12 .07 .12
.06 .05 .06 .24 - .22 .22 .20 .19 .06 .07 .06 .09
.08 .06 .07 .25 .22 - .34 .26 .20 .11 .13 .06 .12
.09 .10 .07 .28 .22 .34 - .23 .21 .12 .12 .09 .10
.11 .09 .09 .26 .20 .26 .23 - .31 .11 .11 .10 .10
.08 .11 .06 .21 .19 .20 .21 .31 - .14 .12 .10 .12
.11 .10 .10 .11 .06 .11 .12 .11 .14 - .51 .25 .30
.11 .10 .10 .12 .07 .13 .12 .11 .12 .51 - .25 .24
.08 .13 .09 .07 .06 .06 .09 .10 .10 .25 .25 - .32
.08 .07 .07 .12 .09 .12 .10 .10 .12 .30 .24 .32 -"""


def _average_linkage(S):
    """Average-linkage clustering on similarities (the method Woese's lab used): repeatedly join the
    two clusters whose members are, on average, most alike. Returns the root as nested tuples
    (similarity, left, right), with leaves as integers."""
    members = {i: [i] for i in range(len(S))}
    node = {i: i for i in range(len(S))}
    active = list(range(len(S)))
    nxt = len(S)
    while len(active) > 1:
        best = None
        for x in range(len(active)):
            for y in range(x + 1, len(active)):
                a, b = active[x], active[y]
                s = sum(S[i][j] for i in members[a] for j in members[b]) / (len(members[a]) * len(members[b]))
                if best is None or s > best[0]:
                    best = (s, a, b)
        s, a, b = best
        members[nxt] = members[a] + members[b]
        node[nxt] = (s, node[a], node[b])
        active = [c for c in active if c not in (a, b)] + [nxt]
        nxt += 1
    return node[active[0]]


def woese_archaea():
    d = D()
    # The tree Woese and Fox's 1977 table gives by average linkage, computed here from the printed
    # coefficients (the paper itself drew no tree). x is the similarity S at which two groups join;
    # the leaves sit at the right, beyond the highest join (0.51). Leaf spacing is even.
    S = [[None if v == '-' else float(v) for v in r.split()] for r in WF_TABLE.splitlines()]
    root = _average_linkage(S)
    order = [0, 1, 2, 4, 7, 8, 3, 5, 6, 9, 10, 11, 12]                   # eukaryotes, bacteria, archaea
    groups = [(0, 3), (3, 9), (9, 13)]
    ys, y = {}, 44
    for k, leaf in enumerate(order):
        if k in (3, 9):
            y += 8
        ys[leaf] = y
        y += 15
    x0, k = 46, 360

    def X(s):
        return x0 + s * k
    leaf_x = X(0.565)

    def place(n):
        """(x, y) of a node: a leaf at the right, a join at its similarity, midway between its children."""
        if isinstance(n, int):
            return leaf_x, ys[n]
        s, a, b = n
        (_, ya), (_, yb) = place(a), place(b)
        return X(s), (ya + yb) / 2

    base = 262
    d.group('thin')
    for t in range(6):                                                    # similarity grid
        d.line((X(t / 10), 36), (X(t / 10), base))
    d.line((X(0), base), (leaf_x, base))
    for t in range(6):
        d.line((X(t / 10), base), (X(t / 10), base + 4))

    d.group()

    def draw(n):
        if isinstance(n, int):
            return
        s, a, b = n
        x, _ = place(n)
        pa, pb = place(a), place(b)
        d.line((pa[0], pa[1]), (x, pa[1]), (x, pb[1]), (pb[0], pb[1]))
        draw(a)
        draw(b)
    draw(root)
    rx, ry = place(root)
    d.line((rx, ry), (rx - 14, ry))

    d.group('mid')
    for leaf in order:
        d.circle(leaf_x + 2.5, ys[leaf], 2.2)
    for n, label in ((root, '0.08'), (root[2], '0.10')):
        x, yy = place(n)
        d.circle(x, yy, 2.8)
        d.text(x + 4, yy - 4, label, size=7, anchor='start')

    d.group('mid')
    for leaf in order:
        d.text(leaf_x + 9, ys[leaf] + 2.5, WF_NAMES[leaf], size=7, anchor='start')
    for (a, b), name in zip(groups, ('EUCARYA', 'BACTERIA', 'ARCHAEA')):
        sub = [order[i] for i in range(a, b)]
        top = min(ys[i] for i in sub)
        d.text(leaf_x - 6, top - 5, name, size=7, anchor='end')
    for t in range(6):
        d.text(X(t / 10), base + 13, f'{t / 10:.1f}', size=7)
    d.text(X(0.28), base + 24, 'SIMILARITY S AT WHICH GROUPS JOIN', size=7)
    d.text(200, 20, '16S rRNA CATALOGS · WOESE AND FOX 1977 · AVERAGE LINKAGE', size=7)
    return d


def _sheep(d, cx, cy, s, black_face):
    """A sheep in elevation, schematic: body, head, legs; the face hatched for a Blackface."""
    d.ellipse(cx, cy, 26 * s, 13 * s)                                     # body
    hx, hy = cx + 36 * s, cy - 18 * s
    d.ellipse(hx, hy, 8 * s, 5.5 * s)                                     # head
    d.line((cx + 20 * s, cy - 8 * s), (hx - 5 * s, hy + 3 * s))           # neck
    d.line((cx + 25 * s, cy - 2 * s), (hx - 3 * s, hy + 5 * s))
    d.line((hx - 4 * s, hy - 5 * s), (hx - 8 * s, hy - 9 * s))            # ear
    for dx in (-17, -9, 11, 18):                                          # legs
        d.line((cx + dx * s, cy + 11 * s), (cx + dx * s, cy + 27 * s))
    if black_face:
        for t in range(-3, 4):
            d.line((hx + t * 2 * s - 1.5 * s, hy - 4 * s), (hx + t * 2 * s + 1.5 * s, hy + 4 * s))


def dolly():
    d = D()
    # Somatic cell nuclear transfer as Roslin did it (Wilmut et al. 1997; Wilmut, Bai and Taylor 2015):
    # udder cells from a Finn Dorset ewe, starved of serum; an egg from a Scottish Blackface ewe with its
    # chromosomes drawn out; the two fused between electrodes; the embryo grown about a week; then a
    # Blackface surrogate, and a white-faced lamb. Sizes schematic, not to scale.
    dish, egg, fuse, emb = (62, 78), (62, 196), (178, 137), (266, 137)
    ewe, lamb = (336, 112), (336, 226)

    d.group('thin')
    d.line((20, 137), (390, 137))                                         # the flow's axis
    d.line((fuse[0], 40), (fuse[0], 250))
    d.line((dish[0], 40), (dish[0], 250))

    d.group()
    d.ellipse(*dish, 36, 13)                                              # culture dish
    d.ellipse(dish[0], dish[1] - 4, 36, 13)
    rng = random.Random(55)
    for _ in range(9):                                                    # resting donor cells
        x = dish[0] + rng.uniform(-26, 26)
        y = dish[1] - 4 + rng.uniform(-6, 6)
        d.circle(x, y, 3.2)
    d.circle(*egg, 22)                                                    # the egg
    d.circle(*egg, 25)                                                    # its zona
    # holding pipette at left, enucleation pipette at right
    d.line((egg[0] - 52, egg[1] - 7), (egg[0] - 27, egg[1] - 7))
    d.line((egg[0] - 52, egg[1] + 7), (egg[0] - 27, egg[1] + 7))
    d.line((egg[0] + 50, egg[1] - 9), (egg[0] + 12, egg[1] - 3))
    d.line((egg[0] + 50, egg[1] - 3), (egg[0] + 12, egg[1] + 1))
    d.circle(*fuse, 22)                                                   # egg and donor cell together
    d.circle(fuse[0] + 22, fuse[1] - 11, 5)
    for sx in (-38, 38):                                                  # electrodes
        d.line((fuse[0] + sx, fuse[1] - 30), (fuse[0] + sx, fuse[1] + 30))
    d.circle(*emb, 18)                                                    # blastocyst
    d.circle(*emb, 15)
    d.ellipse(emb[0] - 6, emb[1] - 4, 7, 5)                               # inner cell mass
    _sheep(d, ewe[0], ewe[1], 0.95, black_face=True)
    _sheep(d, lamb[0], lamb[1], 0.7, black_face=False)

    d.group('mid')
    for p, q in (((dish[0] + 40, dish[1] + 2), (fuse[0] - 42, fuse[1] - 18)),
                 ((egg[0] + 54, egg[1] - 8), (fuse[0] - 42, fuse[1] + 18)),
                 ((fuse[0] + 42, fuse[1]), (emb[0] - 22, emb[1])),
                 ((emb[0] + 21, emb[1] - 6), (ewe[0] - 30, ewe[1] + 2)),
                 ((ewe[0] - 4, ewe[1] + 30), (lamb[0] - 4, lamb[1] - 14))):
        d.line(p, q)
        _arrow(d, p, q, size=4)
    for t in range(-3, 4):                                                # the pulse
        d.line((fuse[0] - 34, fuse[1] + t * 7), (fuse[0] - 29, fuse[1] + t * 7))
    for k in range(5):                                                    # chromosomes drawn out
        d.line((egg[0] + 16 + k * 3, egg[1] - 4 + (k % 2)), (egg[0] + 18 + k * 3, egg[1] - 1 + (k % 2)))

    d.group('mid')
    d.text(dish[0], 52, 'UDDER CELLS', size=7)
    d.text(dish[0], 104, 'FINN DORSET · STARVED', size=7)
    d.text(egg[0], 160, 'EGG', size=7)
    d.text(egg[0], 237, 'BLACKFACE · EMPTIED', size=7)
    d.text(fuse[0], 96, 'ELECTRIC PULSE', size=7)
    d.text(fuse[0], 183, 'FUSED', size=7)
    d.text(emb[0], 168, 'ABOUT A WEEK', size=7)
    d.text(ewe[0], 74, 'SURROGATE · BLACKFACE', size=7)
    d.text(lamb[0], 268, 'DOLLY · WHITE FACE', size=7)
    d.text(200, 20, 'SOMATIC CELL NUCLEAR TRANSFER · ROSLIN, 1996', size=7)
    return d


def human_genome():
    d = D()
    # The two ways of reading the genome in 1998–2001. Above, the public project's hierarchical
    # shotgun: BAC clones of 100–200 kb mapped along a chromosome, one chosen, broken into short
    # reads and assembled on its own. Below, Celera's whole-genome shotgun: reads from the whole
    # genome at once, paired ends tying distant reads together. Lengths schematic, positions random.
    rng = random.Random(2001)
    L, R = 34, 370

    d.group('thin')
    d.line((20, 152), (390, 152))                                         # divides the two methods
    zl, zr = 150, 214                                                     # the chosen BAC
    d.line((zl, 76), (L + 30, 98))
    d.line((zr, 76), (R - 30, 98))

    d.group()
    d.line((L, 48), (R, 48))                                              # chromosome, public
    for i in range(9):                                                    # BAC tiling path
        x = L + i * 38
        y = 60 if i % 2 == 0 else 68
        d.line((x, y), (min(x + 64, R), y))
    d.line((zl, 76), (zr, 76))
    d.line((L, 128), (R, 128))                                            # its assembled sequence
    d.line((L, 180), (R, 180))                                            # chromosome, Celera
    d.line((L, 252), (150, 252))                                          # scaffold with gaps
    d.line((158, 252), (268, 252))
    d.line((276, 252), (R, 252))

    d.group('mid')
    for r in range(4):                                                    # reads from one BAC, overlapping
        x = L + 30 + r * 10 + rng.uniform(0, 6)
        while x + 26 <= R - 30:
            d.line((x, 104 + r * 6), (x + 26, 104 + r * 6))
            x += 26 + rng.uniform(10, 18)
    pairs = []
    for r in range(5):                                                    # paired-end reads, whole genome
        x = L + r * 17 + rng.uniform(0, 8)
        while x + 60 <= R:
            span = rng.uniform(38, 48)
            y = 194 + r * 8
            d.line((x, y), (x + 10, y))
            d.line((x + span, y), (x + span + 10, y))
            pairs.append((x + 10, x + span, y))
            x += span + 10 + rng.uniform(14, 26)
    for a, b, y in pairs:
        d.dashed((a, y), (b, y), dash=2, gap=2)
    for x in (150, 158, 268, 276):
        d.line((x, 248), (x, 256))

    d.group('mid')
    d.text(L, 40, 'PUBLIC PROJECT · HIERARCHICAL SHOTGUN', size=7, anchor='start')
    d.text(R, 40, 'CHROMOSOME', size=7, anchor='end')
    d.text(R, 84, 'BAC CLONES, MAPPED', size=7, anchor='end')
    d.text(L, 142, 'ONE CLONE ASSEMBLED', size=7, anchor='start')
    d.text(L, 172, 'CELERA · WHOLE-GENOME SHOTGUN', size=7, anchor='start')
    d.text(R, 172, 'WHOLE GENOME', size=7, anchor='end')
    d.text(L, 240, 'PAIRED READS', size=7, anchor='start')
    d.text(L, 268, 'ASSEMBLED, PAIRS SPANNING GAPS', size=7, anchor='start')
    d.text(200, 20, 'READING THE HUMAN GENOME · 1998–2001', size=7)
    return d


PLATES = {'woese-archaea': woese_archaea, 'dolly': dolly, 'human-genome': human_genome}
