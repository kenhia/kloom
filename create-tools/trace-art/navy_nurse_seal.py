# /// script
# dependencies = ["pillow", "numpy", "potracer"]
# ///
"""Trace the seal of the US Navy Nurse Corps (US Navy, public domain) to currentColor paths.
Only the gold is traced (the rope, the lettering, the stars, the oak leaf and the 1908 scroll),
so on a dark ground the seal reads as gold on navy. The image is enlarged three times first,
since the source is only 418 pixels wide. Writes two files: the whole seal, and the oak leaf
alone (the Nurse Corps device, for the sleeve).

    curl -L -o seal.png 'https://upload.wikimedia.org/wikipedia/commons/…/Seal_of_the_United_States_Navy_Nurse_Corps.png'
    uv run create-tools/trace-art/navy_nurse_seal.py seal.png create-tools/draw-plates/art/navy-nurse-seal-trace.txt create-tools/draw-plates/art/navy-nurse-leaf-trace.txt

Keeping Watch's dedication plate (draw-plates/nursing_dedication.py) draws the result (korg 3470)."""
import sys
import numpy as np, potrace
from PIL import Image

K = 3
im = Image.open(sys.argv[1]).convert('RGB')
im = im.resize((im.width * K, im.height * K), Image.LANCZOS)
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
gold = (r > 140) & (r - b > 25)                  # gold, and the leaf's pale cream highlights; not the blue or the white
yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
disc = (xx - 209 * K) ** 2 + (yy - 209 * K) ** 2 < (118 * K) ** 2
gold |= disc & (r > 225) & (g > 225) & (b > 190)  # the leaf's near-white highlight, inside the inner disc only


def f(v): return f'{v / K:.1f}'.rstrip('0').rstrip('.')


def trace(mask, dx=0, dy=0):
    plist = potrace.Bitmap(~mask).trace(turdsize=12, alphamax=1.0, opticurve=True, opttolerance=0.4)
    parts = []
    for curve in plist:
        s = curve.start_point
        d = [f'M{f(s.x + dx)} {f(s.y + dy)}']
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f'L{f(seg.c.x + dx)} {f(seg.c.y + dy)}L{f(seg.end_point.x + dx)} {f(seg.end_point.y + dy)}')
            else:
                d.append(f'C{f(seg.c1.x + dx)} {f(seg.c1.y + dy)} {f(seg.c2.x + dx)} {f(seg.c2.y + dy)} '
                         f'{f(seg.end_point.x + dx)} {f(seg.end_point.y + dy)}')
        d.append('Z')
        parts.append(''.join(d))
    return ''.join(parts), len(plist)


seal, n = trace(gold)
open(sys.argv[2], 'w').write(seal)
print('seal', n, 'curves', len(seal), 'bytes', a.shape[:2])
# the leaf: the gold inside the seal's inner disc, above the scroll (in source pixels, 418 square)
x0, y0, x1, y1 = (140 * K, 105 * K, 280 * K, 256 * K)
leaf_mask = np.zeros_like(gold)
leaf_mask[y0:y1, x0:x1] = gold[y0:y1, x0:x1]
leaf, n = trace(leaf_mask[y0:y1, x0:x1])
open(sys.argv[3], 'w').write(leaf)
print('leaf', n, 'curves', len(leaf), 'bytes', (y1 - y0, x1 - x0))
