"""Plates for The Story of Life's "Reading and writing life" frames, part read1. See plates_for.py."""
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


def _ring(d, cx, cy, r, gap_a=None, gap_w=18, inner=3.0, cls=None):
    """A plasmid drawn as two concentric strands, optionally open over an arc of gap_w degrees
    centred on gap_a (the staggered cut: the outer strand is cut gap_w/2 ahead of the inner)."""
    for k, rr in ((0, r + inner / 2), (1, r - inner / 2)):
        if gap_a is None:
            d.circle(cx, cy, rr, cls=cls)
        else:
            off = gap_w / 2 if k == 0 else -gap_w / 2         # the four-base stagger
            d.arc(cx, cy, rr, gap_a + gap_w / 2 + off, gap_a - gap_w / 2 + off + 360, n=96, cls=cls)


def recombinant_dna():
    d = D()
    # Cohen, Chang, Boyer and Helling 1973: a plasmid carrying one EcoRI site is opened, a fragment
    # with ends of the same kind pairs into the gap, and the ring closes carrying both parents'
    # genes. Three states left to right, on true circles; schematic, since the ring of the paper is
    # about 9,000 base pairs long and no drawing shows them.
    cys, r = 110, 33
    xs = [74, 200, 326]

    d.group('thin')
    d.line((20, cys), (380, cys))                                             # the axis of the three states
    for x in xs:
        d.line((x, cys - r - 13), (x, cys + r + 13))
        d.circle(x, cys, r + 9)                                               # a construction circle
    d.line((130, cys), (152, cys))
    d.line((256, cys), (278, cys))

    d.group()
    _ring(d, xs[0], cys, r)                                                   # closed, before the cut
    _ring(d, xs[1], cys, r, gap_a=-90, gap_w=30)                              # opened at its one site
    _ring(d, xs[2], cys, r)                                                   # closed again, with the insert

    d.group('mid')
    _arrow(d, (132, cys), (152, cys))
    _arrow(d, (258, cys), (278, cys))
    for s in (-1, 1):                                                         # the site, as two radial ticks
        aa = math.radians(-90) + s * math.radians(5)
        d.line((xs[0] + (r - 8) * math.cos(aa), cys + (r - 8) * math.sin(aa)),
               (xs[0] + (r + 8) * math.cos(aa), cys + (r + 8) * math.sin(aa)))
    d.arc(xs[2], cys, r + 6, -145, -35, n=48)                                 # the insert, as its arc
    for a in (-145, -35):                                                     # the two sealed joins
        aa = math.radians(a)
        d.line((xs[2] + (r - 9) * math.cos(aa), cys + (r - 9) * math.sin(aa)),
               (xs[2] + (r + 9) * math.cos(aa), cys + (r + 9) * math.sin(aa)))

    # the two cut ends, drawn large below: each duplex ends in four unpaired bases that pair with
    # the other's. Each base is one step wide; the pieces are drawn apart to show the overhangs.
    step, by, h = 12, 212, 15
    lx, rx = 64, 240                                                          # the two fragments' left edges

    d.group('thin')
    d.line((lx - 8, by), (lx + 9 * step + 6, by))
    d.line((lx - 8, by + h), (lx + 9 * step + 6, by + h))
    d.line((rx - 6, by), (rx + 9 * step + 8, by))
    d.line((rx - 6, by + h), (rx + 9 * step + 8, by + h))

    d.group()
    d.line((lx, by), (lx + 5 * step, by))                                     # left piece: top strand
    d.line((lx, by + h), (lx + 9 * step, by + h))                             # left piece: bottom strand, longer
    d.line((rx + 4 * step, by), (rx + 9 * step, by))                          # right piece: top strand, longer
    d.line((rx + 4 * step, by + h), (rx + 9 * step, by + h))
    d.line((rx + 4 * step, by + h), (rx, by + h))
    d.line((rx, by + h), (rx + 4 * step, by + h))
    for k in range(5):                                                        # paired bases, left piece
        d.line((lx + k * step, by + 2), (lx + k * step, by + h - 2))
    for k in range(4, 9):                                                     # paired bases, right piece
        d.line((rx + k * step, by + 2), (rx + k * step, by + h - 2))

    d.group('mid')
    for k, ch in enumerate('AATT'):                                           # the overhangs, base by base
        d.text(lx + (5 + k) * step, by + h + 11, ch, size=7)
        d.text(rx + k * step, by - 4, ch, size=7)
    d.line((lx + 5 * step - 6, by + h + 18), (lx + 9 * step - 6, by + h + 18))
    for x in (lx + 5 * step - 6, lx + 9 * step - 6):
        d.line((x, by + h + 15), (x, by + h + 21))

    d.group('mid')
    d.text(xs[0], cys - r - 21, 'VECTOR', size=7)
    d.text(xs[1], cys - r - 21, 'CUT AT ITS ONE SITE', size=7)
    d.text(xs[2], cys - r - 21, 'CLOSED ON AN INSERT', size=7)
    d.text(xs[2], cys + r + 24, 'TWO JOINS', size=7)
    d.text(lx + 7 * step - 6, by + h + 31, '4 BASES', size=7)
    d.text(lx - 14, by + 4, "5'", size=7, anchor='end')
    d.text(lx - 14, by + h + 4, "3'", size=7, anchor='end')
    d.text(rx + 9 * step + 16, by + 4, "3'", size=7, anchor='start')
    d.text(rx + 9 * step + 16, by + h + 4, "5'", size=7, anchor='start')
    d.text(276, 276, 'THE CUT ENDS PAIR WITH EACH OTHER', size=7)
    d.text(200, 292, 'COHEN, CHANG, BOYER AND HELLING, 1973', size=7)
    return d


def asilomar():
    d = D()
    # The February 1975 recommendations as nested boundaries: four bands of containment, each
    # enclosing the one before, with the deferred experiments outside them all, and the enfeebled
    # host and vector at the centre. The rectangles are concentric, each inset 24 units from the
    # last, and each band's name and measures sit on its own top edge.
    cx, cy = 200, 148
    bands = [('MINIMAL', 'CLINICAL PRACTICE'), ('LOW', 'LIMITED ACCESS, CABINET'),
             ('MODERATE', 'GLOVES, NEGATIVE PRESSURE'), ('HIGH', 'AIR LOCK, SHOWER, TREATED AIR')]
    w0, h0, inset = 352, 212, 24

    d.group('thin')
    for k in range(len(bands) + 1):                                           # the inset, measured once
        x = cx - w0 / 2 + k * inset
        d.line((x, cy + h0 / 2 + 4), (x, cy + h0 / 2 + 10))
    d.line((cx - w0 / 2, cy + h0 / 2 + 7), (cx - w0 / 2 + len(bands) * inset, cy + h0 / 2 + 7))
    d.line((cx, cy + 36), (cx, cy + h0 / 2))                                  # the centre line, below the labels

    d.group()
    for k in range(len(bands)):
        w, h = w0 - 2 * k * inset, h0 - 2 * k * inset
        _box(d, cx - w / 2, cy - h / 2, w, h)

    d.group('mid')
    d.ellipse(cx, cy - 6, 17, 10)                                             # the enfeebled host
    d.ellipse(cx, cy - 6, 6, 4)                                               # its crippled vector
    for s in (-1, 1):                                                         # the mutations, as cut marks
        d.line((cx + s * 10, cy - 12), (cx + s * 14, cy - 8))
        d.line((cx + s * 14, cy - 12), (cx + s * 10, cy - 8))

    d.group('mid')
    for k, (name, how) in enumerate(bands):
        y = cy - h0 / 2 + k * inset - 4                                       # on the band's own top edge
        d.text(cx - w0 / 2 + k * inset + 6, y, name, size=7, anchor='start')
        d.text(cx + w0 / 2 - k * inset - 6, y, how, size=7, anchor='end')
    d.text(cx, cy + 14, 'ENFEEBLED HOST AND VECTOR', size=7)
    d.text(cx, cy + 26, 'ESCAPE UNDER 1 IN 100,000,000', size=7)
    d.text(cx - w0 / 2 + len(bands) * inset / 2, cy + h0 / 2 + 20, 'FOUR BANDS', size=7)
    d.text(cx, 290, 'DEFERRED: PATHOGENS, TOXIN GENES, OVER 10 LITERS', size=7)
    d.text(cx, 18, 'CONTAINMENT MATCHED TO RISK, ASILOMAR 1975', size=7)
    return d


def sanger_sequencing():
    d = D()
    # A chain-terminating gel: four lanes, one per terminating base, the bands sorted by length and
    # the sequence read from the bottom up. The ladder is the invented sequence of the reading,
    # GATTACAG, repeated to fill the gel; band spacing narrows with length, as a real gel's does.
    lanes = ['G', 'A', 'T', 'C']
    seq = 'GATTACAGTCCAGATTACAG'                                              # read bottom to top
    x0, pitch = 104, 48
    bottom, top = 252, 44
    n = len(seq)

    d.group('thin')
    for k in range(len(lanes) + 1):                                           # the lane rules
        x = x0 + (k - 0.5) * pitch
        d.line((x, 36), (x, bottom + 10))
    d.line((x0 - 0.5 * pitch, bottom + 10), (x0 + 3.5 * pitch, bottom + 10))
    d.line((x0 - 0.5 * pitch, 36), (x0 + 3.5 * pitch, 36))
    for i in range(n):                                                        # where each band sits
        t = i / (n - 1)
        y = bottom - (bottom - top) * (t ** 0.78)
        d.line((x0 - 0.5 * pitch - 8, y), (x0 - 0.5 * pitch, y))

    d.group()
    ys = []
    for i, ch in enumerate(seq):
        t = i / (n - 1)
        y = bottom - (bottom - top) * (t ** 0.78)
        ys.append(y)
        x = x0 + lanes.index(ch) * pitch
        d.line((x - 15, y), (x + 15, y))                                      # the band

    d.group('mid')
    d.line((x0 + 3.5 * pitch + 22, bottom), (x0 + 3.5 * pitch + 22, top - 4)) # the reading direction
    _arrow(d, (x0 + 3.5 * pitch + 22, bottom), (x0 + 3.5 * pitch + 22, top - 4))
    for i, ch in enumerate(seq[:8]):                                          # the sequence, read off
        d.text(x0 + 3.5 * pitch + 36, ys[i] + 3, ch, size=7, anchor='start')

    d.group('mid')
    for k, ch in enumerate(lanes):
        d.text(x0 + k * pitch, 30, 'dd' + ch, size=7)
    d.text(x0 - 0.5 * pitch - 12, bottom + 4, 'SHORT', size=7, anchor='end')
    d.text(x0 - 0.5 * pitch - 12, top, 'LONG', size=7, anchor='end')
    d.text(x0 + 3.5 * pitch + 36, top - 10, 'READ UP', size=7, anchor='start')
    d.text(200, 274, 'FOUR REACTIONS, ONE LANE EACH · SANGER 1977', size=7)
    d.text(200, 290, 'EACH BAND A CHAIN STOPPED AT THAT BASE', size=7)
    return d


PLATES = {
    'recombinant-dna': recombinant_dna,
    'asilomar': asilomar,
    'sanger-sequencing': sanger_sequencing,
}
