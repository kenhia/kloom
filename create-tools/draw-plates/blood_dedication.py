"""The plate for In the Blood's dedication frame (sprint 028). See plates_for.py.

Not computed geometry, for once: two official drawings, placed. The colonel's eagle is the
Defense Logistics Agency's drawing (Wikimedia Commons, File:US-O6 insignia.svg), its silhouette
stroked and its detail filled with currentColor; the Medical Service Corps insignia is The
Institute of Heraldry's image 13862 traced by trace-art/msc_insignia.py (korg 3466). Both are
in art/. A hand-drawn first pass looked wrong (Ken, 2026-09-30), so neither is redrawn here.
"""
import os, re
from plates import D

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'art')


class Placed(D):
    """A D whose svg() also writes placed artwork: (transform, [(d, how)]) groups after the drawn ones."""

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
    # Side by side, as Ken's mockup has them (korg 3475): the eagle on the left, the branch insignia
    # on the right, both sitting on one line, each named beneath.
    base = 236
    d.group('thin')
    d.line((8, base + 10), (392, base + 10))
    d.group('mid')
    d.text(102, base + 34, 'COLONEL · O-6', size=10)
    d.text(300, base + 34, 'MEDICAL SERVICE CORPS', size=10)
    eagle = open(os.path.join(ART, 'us-o6-insignia.svg')).read()
    silhouette, detail = re.findall(r'<path d="([^"]+)"', eagle)
    s = 0.205                                         # 950 by 475 drawn 195 wide, its foot on the line
    d.placed.append((f'translate({102 - 475 * s:.2f} {base - 475 * s:.2f}) scale({s})',
                     [(silhouette, 'stroke'), (detail, 'fill')], 6.5))
    msc = open(os.path.join(ART, 'msc-insignia-trace.txt')).read().strip()
    s = 0.235                                         # 822 by 674 drawn 193 wide, 158 high
    d.placed.append((f'translate({300 - 411 * s:.2f} {base - 674 * s:.2f}) scale({s})', [(msc, 'fill')], 5))
    return d


PLATES = {'dedication': dedication}
