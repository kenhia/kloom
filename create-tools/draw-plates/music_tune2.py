"""Plates for Sound and Score's part tune2 (sprint 058): well-temperament, helmholtz-tone, ellis-cents.

See plates_for.py. Run this file with --charts to write helmholtz-tone's roughness chart, which is
drawn here by hand (a curve, not bars) in currentColor with the muted and accent classes.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plates import D  # noqa: E402


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _sector(d, cx, cy, r0, r1, a0, a1, n=12):
    """A closed annular sector between radii r0 and r1, angles a0..a1 in degrees (clockwise from east)."""
    pts = [(cx + r1 * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            cy + r1 * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    pts += [(cx + r0 * math.cos(math.radians(a1 - (a1 - a0) * i / n)),
             cy + r0 * math.sin(math.radians(a1 - (a1 - a0) * i / n))) for i in range(n + 1)]
    d.line(*pts, closed=True)


FIFTHS = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'Eb', 'Bb', 'F']
# Werckmeister III (1691; Barbour 1951, table 140): the share of the Pythagorean comma taken off each
# fifth, starting C-G and going round. Lehman's 2005 reading of the 1722 title page: from F-C, five
# fifths by 1/6, three pure, three by 1/12, and Bb-F (A#-F) 1/12 wide (his site, 2005).
WERCKMEISTER_III = [1 / 4, 1 / 4, 1 / 4, 0, 0, 1 / 4, 0, 0, 0, 0, 0, 0]


def _lehman():
    # indices follow FIFTHS: fifth i runs from FIFTHS[i] to FIFTHS[i+1]
    share = {'F-C': 1 / 6, 'C-G': 1 / 6, 'G-D': 1 / 6, 'D-A': 1 / 6, 'A-E': 1 / 6,
             'E-B': 0, 'B-F#': 0, 'F#-C#': 0, 'C#-G#': 1 / 12, 'G#-Eb': 1 / 12, 'Eb-Bb': 1 / 12, 'Bb-F': -1 / 12}
    return [share[f'{FIFTHS[i]}-{FIFTHS[(i + 1) % 12]}'] for i in range(12)]


def well_temperament():
    d = D()
    cx, cy = 200, 152
    ro, ri = 92, 58                      # Werckmeister's ring, Lehman's ring
    k = 72                               # pixels for a whole comma
    ang = [-90 + 30 * i for i in range(12)]
    mid = [a + 15 for a in ang]
    lehman = _lehman()

    d.group('thin')
    d.circle(cx, cy, ro)
    d.circle(cx, cy, ri)
    for a in ang:
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        d.line((cx + (ri - 22) * c, cy + (ri - 22) * s), (cx + (ro + 26) * c, cy + (ro + 26) * s))
    d.line((cx - 6, cy), (cx + 6, cy)); d.line((cx, cy - 6), (cx, cy + 6))

    d.group()
    for i, w in enumerate(WERCKMEISTER_III):          # outward: Werckmeister III's narrowed fifths
        if w:
            _sector(d, cx, cy, ro, ro + w * k, mid[i] - 9, mid[i] + 9)
    for a in ang:                                      # the twelve notes on the outer ring
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        d.circle(cx + ro * c, cy + ro * s, 2.2)

    d.group('mid')
    for i, w in enumerate(lehman):                     # inward: Lehman's reading; the wide fifth outward
        if w > 0:
            _sector(d, cx, cy, ri - w * k, ri, mid[i] - 8, mid[i] + 8)
        elif w < 0:
            _sector(d, cx, cy, ri, ri - w * k, mid[i] - 8, mid[i] + 8)
    for a in ang:
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        d.circle(cx + ri * c, cy + ri * s, 1.6)

    d.group('mid')
    for i, a in enumerate(ang):
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        name = FIFTHS[i].replace('#', '♯').replace('b', '♭') if len(FIFTHS[i]) > 1 else FIFTHS[i]
        d.text(cx + (ro + 36) * c, cy + (ro + 36) * s + 2.5, name, size=7)
    d.text(18, 22, 'OUTER · WERCKMEISTER III · 1691', size=7, anchor='start')
    d.text(18, 33, 'FOUR FIFTHS EACH 1/4 COMMA NARROW', size=7, anchor='start')
    d.text(382, 268, 'INNER · LEHMAN 2005', size=7, anchor='end')
    d.text(382, 279, '1/6 · 0 · 1/12 · ONE 1/12 WIDE', size=7, anchor='end')
    return d


def helmholtz_tone():
    d = D()
    # Left: a spherical resonator in section, after Helmholtz's figs. 16a, 16b (1863; Ellis 1885, p. 43):
    # a sphere with a sharp-edged opening, and opposite it a funnel-shaped nipple for the ear.
    cx, cy, R, t = 112, 150, 54, 3.2
    mo = 14                                   # half-width of the mouth, in degrees seen from the centre
    no = 5                                    # half-width of the nipple's root
    d.group('thin')
    d.line((cx - R - 30, cy), (cx + R + 52, cy))
    d.line((cx, cy - R - 16), (cx, cy + R + 16))
    d.line((cx - R, cy + R + 22), (cx + R, cy + R + 22))
    _arrow(d, (cx, cy + R + 22), (cx - R, cy + R + 22), 4); _arrow(d, (cx, cy + R + 22), (cx + R, cy + R + 22), 4)
    for r in (R * 0.33, R * 0.66):
        d.circle(cx, cy, r)

    d.group()
    # outer and inner walls, broken at the mouth (west) and at the nipple (east)
    d.arc(cx, cy, R, 180 + mo, 360 - no, n=60); d.arc(cx, cy, R, no, 180 - mo, n=60)
    d.arc(cx, cy, R - t, 180 + mo + 1, 360 - no - 1, n=60); d.arc(cx, cy, R - t, no + 1, 180 - mo - 1, n=60)
    # sharp lips of the mouth
    for sgn in (1, -1):
        a = math.radians(180 + sgn * mo)
        p = (cx + R * math.cos(a), cy + R * math.sin(a))
        q = (cx + (R - t) * math.cos(a + sgn * math.radians(1)), cy + (R - t) * math.sin(a + sgn * math.radians(1)))
        d.line(q, (p[0] - 3, p[1]), p)
    # the nipple: a cone narrowing to the ear
    y0 = R * math.sin(math.radians(no))
    x0 = cx + R * math.cos(math.radians(no))
    tip = x0 + 34
    d.line((x0, cy - y0), (tip, cy - 2.2), (tip + 4, cy - 2.2))
    d.line((x0, cy + y0), (tip, cy + 2.2), (tip + 4, cy + 2.2))
    d.line((x0 - 1, cy - y0 + t * 0.6), (tip - 2, cy - 1.0))
    d.line((x0 - 1, cy + y0 - t * 0.6), (tip - 2, cy + 1.0))

    d.group('mid')
    # the air in the neck moving in and out: arrows at the mouth
    mx = cx - R * math.cos(math.radians(mo))
    for dy in (-8, 0, 8):
        d.line((mx - 18, cy + dy), (mx - 4, cy + dy)); _arrow(d, (mx - 18, cy + dy), (mx - 4, cy + dy), 3)
    # sealing wax around the nipple's end
    d.ellipse(tip + 1, cy, 4, 6)

    # Right: a string's first six modes, the harmonics, as standing waves
    xa, xb = 250, 388
    top, step, amp = 50, 38, 9
    d.group('thin')
    for k in range(6):
        y = top + k * step
        d.line((xa, y), (xb, y))
        for j in range(1, k + 1):
            x = xa + (xb - xa) * j / (k + 1)
            d.line((x, y - amp - 3), (x, y + amp + 3))
    d.group()
    for k in range(6):
        n, y = k + 1, top + k * step
        for sgn in (1, -1):
            pts = [(xa + (xb - xa) * i / 120, y - sgn * amp * math.sin(n * math.pi * i / 120)) for i in range(121)]
            d.line(*pts)
        d.line((xa, y - amp - 4), (xa, y + amp + 4)); d.line((xb, y - amp - 4), (xb, y + amp + 4))

    d.group('mid')
    for k in range(6):
        d.text(xa - 10, top + k * step + 2.5, str(k + 1), size=7, anchor='end')
    d.text(303, 22, 'HARMONICS 1 TO 6 · 1:2:3:4:5:6', size=7)
    d.text(cx - 8, cy - R - 24, 'RESONATOR IN SECTION', size=7)
    d.text(14, cy - 14, 'MOUTH', size=7, anchor='start')
    d.text(tip - 28, cy + 20, 'TO THE EAR', size=7, anchor='start')
    d.text(cx, cy + R + 36, 'ONE SPHERE · ONE TONE', size=7)
    return d


def ellis_cents():
    d = D()
    x0, x1 = 34, 366
    L = x1 - x0                                    # one octave, 1200 cents
    X = lambda c: x0 + L * c / 1200
    rows = {'freq': 52, 'et': 102, 'just': 154, 'slendro': 208, 'pelog': 260}
    et = [100 * i for i in range(13)]
    just = [('9:8', 9 / 8), ('6:5', 6 / 5), ('5:4', 5 / 4), ('4:3', 4 / 3), ('3:2', 3 / 2), ('5:3', 5 / 3), ('15:8', 15 / 8)]
    slendro = [0, 228, 484, 728, 960, 1200]          # Ellis 1885, p. 510: the Aquarium gamelan's mean
    pelog = [0, 137, 446, 575, 687, 820, 1098, 1200]  # Ellis 1885, p. 512: the seven pelog notes

    d.group('thin')
    for c in et:                                   # equal-semitone guides through every row
        d.line((X(c), rows['freq'] - 6), (X(c), rows['pelog'] + 8))
    d.group()
    for key in ('freq', 'et', 'just', 'slendro', 'pelog'):
        d.line((x0, rows[key]), (x1, rows[key]))
    # top row: frequency ratio 1.0 to 2.0 in tenths, on the logarithmic line, crowding to the right
    for i in range(11):
        r = 1 + i / 10
        x = X(1200 * math.log2(r))
        h = 7 if i in (0, 5, 10) else 4
        d.line((x, rows['freq'] - h), (x, rows['freq'] + h))
    for c in et:
        d.line((X(c), rows['et'] - 6), (X(c), rows['et'] + 6))
    for _, r in just:
        x = X(1200 * math.log2(r))
        d.line((x, rows['just'] - 8), (x, rows['just'] + 3))
    d.group('mid')
    for c in slendro:
        d.circle(X(c), rows['slendro'], 3)
    for c in pelog:
        d.circle(X(c), rows['pelog'], 3)
    for a, b in zip(slendro, slendro[1:]):        # step brackets under the slendro line
        d.line((X(a) + 4, rows['slendro'] + 9), (X(b) - 4, rows['slendro'] + 9))

    d.group('mid')
    d.text(x0, rows['freq'] - 12, '1.0', size=7, anchor='middle')
    d.text(X(1200 * math.log2(1.5)), rows['freq'] - 12, '1.5', size=7)
    d.text(x1, rows['freq'] - 12, '2.0', size=7, anchor='middle')
    d.text(x0, rows['freq'] + 18, 'RATIO', size=7, anchor='start')
    d.text(x0, rows['et'] + 18, 'EQUAL · 100 CENTS A STEP', size=7, anchor='start')
    d.text(X(1200 * math.log2(5 / 4)), rows['just'] - 12, '5:4', size=7)
    d.text(X(1200 * math.log2(3 / 2)), rows['just'] - 12, '3:2', size=7)
    d.text(x0, rows['just'] + 16, 'JUST', size=7, anchor='start')
    for a, b in zip(slendro, slendro[1:]):
        d.text((X(a) + X(b)) / 2, rows['slendro'] + 20, str(b - a), size=7)
    d.text(x0, rows['slendro'] - 10, 'SLENDRO · ELLIS 1885', size=7, anchor='start')
    d.text(x0, rows['pelog'] + 18, 'PELOG · ITS SEVEN NOTES', size=7, anchor='start')
    d.text(x1, rows['pelog'] + 18, '1200', size=7, anchor='end')
    return d


PLATES = {
    'well-temperament': well_temperament,
    'helmholtz-tone': helmholtz_tone,
    'ellis-cents': ellis_cents,
}


# The roughness chart for helmholtz-tone -------------------------------------------------------
def roughness(ratio, f0=264.0, b0=33.0, partials=6):
    """Our computation from Helmholtz's rule (1863; Ellis 1885, pp. 192-193, app. XV): every pair of
    partials of the two tones beats; each pair's strength is 1/(m*n), as he took for a violin's
    partials; and roughness is nothing for no beats, greatest at about 33 beats a second, and falls
    away for faster ones. The shape of that fall, 4u/(1+u)^2 with u=(b/b0)^2, is ours, as his was
    'somewhat arbitrary'. The lower tone is his c' of 264 vibrations a second."""
    f = f0 * ratio
    s = 0.0
    for m in range(1, partials + 1):
        for n in range(1, partials + 1):
            b = abs(n * f - m * f0)
            u = (b / b0) ** 2
            s += 4 * u / (1 + u) ** 2 / (m * n)
    return s


def roughness_chart():
    W, H = 480, 300
    px0, px1, py0, py1 = 56, 456, 252, 54
    cents = list(range(0, 1201, 2))
    ys = [roughness(2 ** (c / 1200)) for c in cents]
    top = 1.5
    X = lambda c: px0 + (px1 - px0) * c / 1200
    Y = lambda v: py0 - (py0 - py1) * v / top
    marks = [('1:1', 1), ('6:5', 6 / 5), ('5:4', 5 / 4), ('4:3', 4 / 3), ('3:2', 3 / 2), ('5:3', 5 / 3), ('2:1', 2)]
    names = {'1:1': 'UNISON', '6:5': 'MIN 3', '5:4': 'MAJ 3', '4:3': '4TH', '3:2': '5TH', '5:3': 'MAJ 6', '2:1': 'OCTAVE'}
    desc = ('A curve of roughness, computed by us from Helmholtz\'s rule, for two tones of six partials each, the lower '
            'fixed at 264 vibrations a second and the upper sliding through one octave. Roughness is high for small '
            'intervals such as the semitone and whole tone, falls past shoulders at the minor and major thirds to a small '
            'dip at the fourth, a deep valley at the fifth and a smaller one at the major sixth, and drops almost to zero '
            'at the octave.')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">',
         '<title id="t">Roughness of two tones across an octave, computed from Helmholtz\'s rule</title>',
         f'<desc id="d">{desc}</desc>',
         '<g font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="currentColor">',
         '<g class="muted">',
         f'<text x="{px0}" y="24">ROUGHNESS OF TWO TONES, SIX PARTIALS EACH</text>',
         f'<line x1="{px0}" x2="{px1}" y1="{py0}" y2="{py0}" stroke="currentColor" stroke-opacity="0.9" stroke-width="1"/>',
         f'<line x1="{px0}" x2="{px0}" y1="{py0}" y2="{py1}" stroke="currentColor" stroke-opacity="0.9" stroke-width="1"/>',
         f'<text x="{px0 - 8}" y="{py0 + 4}" text-anchor="end">0</text>',
         f'<text x="{px0 - 8}" y="{py1 + 4}" text-anchor="end">MORE</text>']
    for lab, r in marks:
        x = X(1200 * math.log2(r))
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{py0}" y2="{py1}" stroke="currentColor" stroke-opacity="0.3" stroke-width="0.6"/>')
        anchor, dx = {'6:5': ('end', 3), '4:3': ('start', -3)}.get(lab, ('middle', 0))
        o.append(f'<text x="{x + dx:.1f}" y="{py0 + 16}" text-anchor="{anchor}" font-size="10">{lab}</text>')
        o.append(f'<text x="{x + dx:.1f}" y="{py0 + 29}" text-anchor="{anchor}" font-size="9">{names[lab]}</text>')
    o.append(f'<text x="{px1}" y="40" text-anchor="end" font-size="9">OUR COMPUTATION FROM HIS RULE · LOWER TONE 264 VIB.</text>')
    o.append('</g>')
    pts = ' '.join(f'{X(c):.1f},{Y(v):.1f}' for c, v in zip(cents, ys))
    o.append(f'<polyline points="{pts}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>')
    o.append('<g class="accent">')
    for lab, r in marks:
        c = 1200 * math.log2(r)
        o.append(f'<circle cx="{X(c):.1f}" cy="{Y(roughness(r)):.1f}" r="3" fill="currentColor"/>')
    o.append('</g>')
    o.append('</g>')
    o.append('</svg>')
    return '\n'.join(o) + '\n'


if __name__ == '__main__' and '--charts' in sys.argv:
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'subjects', 'music', 'frames')
    out = os.path.join(root, 'helmholtz-tone', 'roughness.svg')
    with open(out, 'w') as fh:
        fh.write(roughness_chart())
    print('wrote', os.path.relpath(out))
    for lab, r in [('6:5', 6 / 5), ('5:4', 5 / 4), ('4:3', 4 / 3), ('3:2', 3 / 2), ('5:3', 5 / 3), ('2:1', 2), ('9:8', 9 / 8), ('16:15', 16 / 15)]:
        print(lab, round(roughness(r), 2))
