"""Plates for The Story of Life, part read3 (sprint 055): ancient DNA and CRISPR. See plates_for.py."""
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


def neanderthal_genome():
    d = D()
    # Above: one ancient DNA fragment, a short duplex whose damaged cytosines (U, read as T) sit
    # mostly near its ends. Below: the damage profile, the share of C read as T at each position
    # from the 5' end, and of G read as A from the 3' end (the mirror, from the fill-in of
    # single-stranded ends). Green et al. (2010) give about 40% at the first position, falling
    # away inward; the decay here, 0.39·e^(-(i-1)/2.3) + 1%, is a schematic fit to that shape.
    fx0, fx1, fy, gap = 70, 330, 62, 12              # the fragment
    n = 26
    step = (fx1 - fx0) / (n - 1)
    damaged_top = [0, 1, 4]                          # positions from the 5' end of the top strand
    damaged_bot = [n - 1, n - 2, n - 5]              # positions near the 3' end, on the other strand
    px0, px1, py0, py1 = 60, 360, 252, 132           # the profile's axes (y up: 0% at py0)
    ymax = 0.5

    def ypos(v):
        return py0 - (py0 - py1) * v / ymax

    def prof(i):
        return 0.39 * math.exp(-(i - 1) / 2.3) + 0.01

    half = 15                                         # positions shown from each end
    xl = [px0 + 6 + (i - 1) * 8.4 for i in range(1, half + 1)]
    xr = [px1 - 6 - (i - 1) * 8.4 for i in range(1, half + 1)]

    d.group('thin')
    d.line((px0, py1 - 6), (px0, py0), (px1, py0), (px1, py1 - 6))
    for v in (0.1, 0.2, 0.3, 0.4):                    # gridlines
        d.line((px0, ypos(v)), (px1, ypos(v)))
    d.line((200, py0 + 4), (200, py1 - 6))            # the fragment's two halves
    for x in (fx0, fx1):
        d.line((x, fy - 20), (x, fy + gap + 20))

    d.group()
    d.line((fx0, fy), (fx1, fy))                      # the two strands
    d.line((fx0 + step, fy + gap), (fx1 - step, fy + gap))
    for k in range(n):
        x = fx0 + k * step
        if 1 <= k <= n - 2:
            d.line((x, fy), (x, fy + gap))
    d.line(*[(x, ypos(prof(i))) for i, x in zip(range(1, half + 1), xl)])
    d.line(*[(x, ypos(prof(i))) for i, x in zip(range(1, half + 1), xr)])

    d.group('mid')
    for k in damaged_top:
        d.circle(fx0 + k * step, fy - 7, 3.2)
    for k in damaged_bot:
        d.circle(fx0 + k * step, fy + gap + 7, 3.2)
    for i, x in zip(range(1, half + 1), xl):
        d.circle(x, ypos(prof(i)), 1.6)
    for i, x in zip(range(1, half + 1), xr):
        d.circle(x, ypos(prof(i)), 1.6)

    d.group('mid')
    d.text(fx0 - 6, fy + 3, "5'", size=7, anchor='end')
    d.text(fx1 + 6, fy + 3, "3'", size=7, anchor='start')
    d.text(200, 34, 'A SHORT FRAGMENT · CIRCLED: DAMAGED BASES', size=7)
    for v in (0.2, 0.4):
        d.text(px0 - 4, ypos(v) + 2.5, f'{int(v * 100)}%', size=7, anchor='end')
    d.text(px0 + 70, py1 - 2, 'C READ AS T', size=7)
    d.text(px1 - 70, py1 - 2, 'G READ AS A', size=7)
    d.text(px0 + 70, py0 + 14, "POSITION FROM 5' END", size=7)
    d.text(px1 - 70, py0 + 14, "FROM 3' END", size=7)
    d.text(200, 288, 'ANCIENT DNA DAMAGE · AFTER GREEN ET AL. 2010 · SCHEMATIC', size=7)
    return d


def crispr():
    d = D()
    # Cas9 on its target, after Jinek et al. (2012) and the Nobel committee's background (2020):
    # the target DNA opened into an R-loop; the 20-letter guide of the single guide RNA paired with
    # the target strand; the PAM, NGG, on the other strand just past the guide's 3' end; both
    # strands cut 3 base pairs before the PAM (the HNH domain cuts the paired strand, RuvC the
    # other); the guide's scaffold, from the tracrRNA, folded in stem-loops inside the protein.
    # Schematic; the protein's outline is two lobes, not its structure.
    y_top, y_bot = 198, 212                           # the two DNA strands, outside the loop
    xa, xb = 112, 262                                 # the protospacer (20 bp)
    n = 20
    step = (xb - xa) / n
    pam0, pam1 = xb, xb + 3 * step                    # NGG
    cut_x = xb - 3 * step
    loop_top = 162                                    # the displaced strand's height
    guide_y = y_bot - 7

    d.group('thin')
    d.ellipse(150, 150, 84, 62)                       # recognition lobe
    d.ellipse(262, 170, 88, 68)                       # nuclease lobe
    d.line((cut_x, 120), (cut_x, 248))                # the cut line
    for x in (xa, xb, pam1):
        d.line((x, 225), (x, 240))
    d.line((xa, 236), (xb, 236))

    d.group()
    # the outer DNA, left and right of the loop
    d.line((20, y_top), (xa, y_top))
    d.line((20, y_bot), (xa, y_bot))
    d.line((pam1, y_top), (380, y_top))
    d.line((xb, y_bot), (380, y_bot))
    for k in range(9):
        x = 26 + k * 10
        d.line((x, y_top), (x, y_bot))
    for k in range(10):
        x = pam1 + 6 + k * 10
        d.line((x, y_top), (x, y_bot))
    # the displaced (non-target) strand, lifted over the protospacer, then the PAM
    pts = []
    for k in range(41):
        t = k / 40
        x = xa + (xb - xa) * t
        pts.append((x, y_top - (y_top - loop_top) * math.sin(math.pi * t) ** 0.6))
    d.line(*pts)
    d.line((xb, y_top), (pam1, y_top))
    # the target strand, straight through
    d.line((xa, y_bot), (xb, y_bot))
    # the guide RNA paired with it, then the scaffold rising into the protein
    d.line((xa - 10, guide_y), (xb, guide_y))
    scaffold = [(xb, guide_y), (xb + 6, guide_y - 14), (xb + 4, guide_y - 40)]
    d.line(*scaffold)
    for (cx, cy, h) in ((xb + 4, guide_y - 40, 22), (xb + 24, guide_y - 62, 18), (xb + 46, guide_y - 52, 14)):
        d.line((cx - 3, cy), (cx - 3, cy - h))
        d.line((cx + 3, cy), (cx + 3, cy - h))
        d.arc(cx, cy - h, 3, 180, 360, n=12)
    d.line((xb + 7, guide_y - 40), (xb + 21, guide_y - 62))
    d.line((xb + 27, guide_y - 62), (xb + 43, guide_y - 52))

    d.group('mid')
    for k in range(n):                               # base pairs, guide to target strand
        x = xa + (k + 0.5) * step
        d.line((x, guide_y), (x, y_bot))
    for k in range(3):                               # the PAM's three pairs, thickened
        x = pam0 + (k + 0.5) * step
        d.line((x, y_top), (x, y_bot))
        d.line((x + 1.2, y_top), (x + 1.2, y_bot))
    # the cut, on both strands
    yt = y_top - (y_top - loop_top) * math.sin(math.pi * (cut_x - xa) / (xb - xa)) ** 0.6
    for (x, y) in ((cut_x, yt), (cut_x, y_bot)):
        d.line((x - 5, y - 5), (x + 5, y + 5))
        d.line((x - 5, y + 5), (x + 5, y - 5))
    d.line((cut_x - 30, 132), (cut_x - 4, yt - 7))
    _arrow(d, (cut_x - 30, 132), (cut_x - 4, yt - 7))

    d.group('mid')
    d.text(150, 104, 'CAS9', size=7)
    d.text(cut_x - 34, 126, 'CUT', size=7, anchor='end')
    d.text((xa + xb) / 2, 250, 'GUIDE · 20 LETTERS', size=7)
    d.text((pam0 + pam1) / 2, 250, 'PAM NGG', size=7)
    d.text(xb + 70, 108, 'SCAFFOLD', size=7, anchor='start')
    d.text(xb + 70, 117, '(TRACRRNA)', size=7, anchor='start')
    d.text(20, y_top - 6, "5'", size=7, anchor='start')
    d.text(20, y_bot + 12, "3'", size=7, anchor='start')
    d.text(200, 288, 'CAS9 ON ITS TARGET · AFTER JINEK ET AL. 2012 · SCHEMATIC', size=7)
    return d


PLATES = {
    'neanderthal-genome': neanderthal_genome,
    'crispr': crispr,
}
