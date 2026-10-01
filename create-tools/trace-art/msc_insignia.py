# /// script
# dependencies = ["pillow", "numpy", "potracer"]
# ///
"""Trace the Medical Service Corps insignia (TIOH image 13862) to one currentColor path.
Only the mid-grey line tones are traced, so the dark M and S fill drops out (Ken's choice, korg 3466).

    curl -k -o msc.jpg 'https://tioh.army.mil/Handlers/ImageHandler.ashx?id=13862&size=original'
    uv run create-tools/trace-art/msc_insignia.py msc.jpg create-tools/draw-plates/art/msc-insignia-trace.txt

(-k because the Institute of Heraldry serves a DoD certificate chain the system store lacks.)
In the Blood's dedication plate (draw-plates/blood_dedication.py) draws the result."""
import sys
import numpy as np, potrace
from PIL import Image
a = np.array(Image.open(sys.argv[1]).convert('L'))
mask = (a >= 68) & (a < 185)
bm = potrace.Bitmap(~mask)          # potracer traces the False pixels
plist = bm.trace(turdsize=6, alphamax=1.0, opticurve=True, opttolerance=0.4)
def f(v): return f'{v:.1f}'.rstrip('0').rstrip('.')
parts = []
for curve in plist:
    s = curve.start_point
    d = [f'M{f(s.x)} {f(s.y)}']
    for seg in curve.segments:
        if seg.is_corner:
            d.append(f'L{f(seg.c.x)} {f(seg.c.y)}L{f(seg.end_point.x)} {f(seg.end_point.y)}')
        else:
            d.append(f'C{f(seg.c1.x)} {f(seg.c1.y)} {f(seg.c2.x)} {f(seg.c2.y)} {f(seg.end_point.x)} {f(seg.end_point.y)}')
    d.append('Z')
    parts.append(''.join(d))
open(sys.argv[2], 'w').write(''.join(parts))
print(len(plist), 'curves', len(''.join(parts)), 'bytes', a.shape)
