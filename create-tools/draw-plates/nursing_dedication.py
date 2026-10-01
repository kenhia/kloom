"""The plate for Keeping Watch's dedication frame (sprint 030). See plates_for.py.

Laid out as In the Blood's dedication is (blood_dedication.py): two pieces of insignia side by
side on one line, each named beneath. On the left a Navy captain's sleeve: four half-inch gold
stripes a quarter inch apart, the lowest two inches above the cuff, drawn here at twelve units to
the inch, and above them the Nurse Corps' single oak leaf in place of the line officer's star
(korg 3470). On the right the seal of the Navy Nurse Corps. The leaf and the seal are the US
Navy's own seal (Wikimedia Commons, public domain), traced by trace-art/navy_nurse_seal.py; both
traces are in art/.
"""
import os
from plates import D

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'art')


class Placed(D):
    """A D whose svg() also writes placed artwork: (transform, [(d, how)], stroke) groups after the drawn ones."""

    def __init__(self):
        super().__init__()
        self.placed = []

    def svg(self):
        head, tail = super().svg().rsplit('</svg>', 1)
        out = [head.rstrip('\n')]
        for transform, paths, sw in self.placed:
            out.append(f'\t<g transform="{transform}" stroke-width="{sw}">')
            for d, how in paths:
                attrs = 'fill="currentColor" stroke="none" fill-rule="evenodd"' if how == 'fill' else 'fill="none"'
                out.append(f'\t\t<path pathLength="1" {attrs} d="{d}"/>')
            out.append('\t</g>')
        out.append('</svg>')
        return '\n'.join(out) + '\n'


def dedication():
    d = Placed()
    base = 236
    u = 12                                              # units to the inch on the sleeve
    sx0, sx1 = 46, 158                                  # the sleeve's edges at the cuff
    d.group('thin')
    d.line((8, base + 10), (392, base + 10))
    d.line((sx1 + 10, base), (sx1 + 10, base - 2 * u))  # two inches from cuff to the lowest stripe
    d.line((sx1 + 6, base), (sx1 + 14, base))
    d.line((sx1 + 6, base - 2 * u), (sx1 + 14, base - 2 * u))
    d.group()
    # the sleeve: a forearm narrowing a little toward the elbow, closed at the cuff
    d.line((sx0 + 10, 40), (sx0, base), (sx1, base), (sx1 - 10, 40))
    # four stripes, each half an inch, a quarter inch apart
    tops, stripes = [], []
    for k in range(4):
        y1 = base - 2 * u - k * (u // 2 + u // 4)
        y0 = y1 - u // 2
        tops.append(y0)
        x0, x1 = sx0 + (base - y1) * 10 / (base - 40) + 1, sx1 - (base - y1) * 10 / (base - 40) - 1
        stripes.append(f'M{x0:.1f} {y0}H{x1:.1f}V{y1}H{x0:.1f}Z')
    d.group('mid')
    d.text((sx0 + sx1) / 2, base + 34, 'CAPTAIN · O-6', size=10)
    d.text(300, base + 34, 'NAVY NURSE CORPS', size=10)
    d.placed.append(('translate(0 0)', [(''.join(stripes), 'fill')], 1))   # the stripes, solid as gold braid is
    # the oak leaf, centred over the stripes a quarter inch above the top one: 140 by 151 traced, drawn 44 high
    leaf = open(os.path.join(ART, 'navy-nurse-leaf-trace.txt')).read().strip()
    s = 44 / 151
    top = min(tops) - u // 4
    d.placed.append((f'translate({(sx0 + sx1) / 2 - 70 * s:.2f} {top - 151 * s:.2f}) scale({s:.4f})', [(leaf, 'fill')], 4))
    # the seal: 418 square, drawn 190 across, sitting on the line
    seal = open(os.path.join(ART, 'navy-nurse-seal-trace.txt')).read().strip()
    s = 190 / 418
    d.placed.append((f'translate({300 - 209 * s:.2f} {base - 418 * s:.2f}) scale({s:.4f})', [(seal, 'fill')], 4))
    return d


PLATES = {'dedication': dedication}
