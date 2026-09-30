"""physics plates, part "now": dark energy, cosmology today, open questions (sprint 021). See physics.py.

Run on its own (`python3 create-tools/draw-plates/physics_now.py`) it also
writes the cosmology-now frame's Hubble-constant chart, a dot-and-whisker
plot that bar_chart.py cannot draw, in the same palette hooks (`muted`,
`accent`, currentColor) as a bar chart.
"""
import math, os
from xml.sax.saxutils import escape

from plates import D, rot


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


# ---------------------------------------------------------------- dark energy

def _a_lcdm(tau, om, ol):
    """Scale factor of a flat universe of matter and Λ at time tau (units of 1/H0 since the Big Bang)."""
    return (om / ol) ** (1 / 3) * math.sinh(1.5 * math.sqrt(ol) * tau) ** (2 / 3)


def dark_energy():
    """The size of the universe against time, for three flat histories that share today's size and expansion rate.

    Matter alone (Einstein–de Sitter) decelerates and is youngest; an empty
    universe coasts; matter with a cosmological constant, at Planck 2018's
    Ωm = 0.315, decelerates and then accelerates. The time axis is in units
    of 1/H0 measured from today, so all three curves touch the same tangent
    at today. The flat line is Einstein's static universe of 1917."""
    d = D()
    om, ol = 0.315, 0.685
    t0_l = 2 / (3 * math.sqrt(ol)) * math.asinh(math.sqrt(ol / om))   # age in 1/H0, about 0.95
    x0, y0 = 60, 262                     # the plot's origin: time -1.1/H0, size 0
    sx, sy = 118, 88                    # pixels per 1/H0, and per today's size
    tmin, tmax, amax = -1.1, 1.2, 2.45
    X = lambda t: x0 + (t - tmin) * sx
    Y = lambda a: y0 - a * sy
    clip = lambda pts: [p for p in pts if p[1] >= Y(amax) and p[0] <= X(tmax)]
    # construction: axes, today's time, and Einstein's static size
    d.group('thin')
    d.line((X(tmin), Y(amax)), (X(tmin), y0), (X(tmax), y0))
    d.line((X(0), y0), (X(0), Y(amax)))
    d.line((X(tmin), Y(1)), (X(tmax), Y(1)))
    # the two histories with matter in them
    d.group()
    ts = [t0_l * k / 160 for k in range(1, 161)] + [t0_l + 1.25 * k / 60 for k in range(1, 61)]
    lam = clip([(X(-t0_l), y0)] + [(X(t - t0_l), Y(_a_lcdm(t, om, ol))) for t in ts])
    d.line(*lam)
    t0_m = 2 / 3
    mat = clip([(X(t - t0_m), Y((1.5 * t) ** (2 / 3))) for t in [(t0_m + 1.25) * k / 160 for k in range(0, 161)]])
    d.line(*mat)
    # the empty universe: a straight line, the tangent the other two share today
    d.group('mid')
    emp = clip([(X(t), Y(1 + t)) for t in (-1.0, min(amax - 1, tmax))])
    d.line(*emp)
    # today, and the Big Bang of each history on the time axis
    d.group()
    d.circle(X(0), Y(1), 3.5)
    for t in (-t0_l, -t0_m, -1.0):
        d.line((X(t), y0 - 4), (X(t), y0 + 4))
    d.group()
    for pts, lab in ((lam, 'MATTER + Λ'), (emp, 'EMPTY'), (mat, 'MATTER ONLY')):
        d.text(pts[-1][0] + 6, pts[-1][1] + 3, lab, size=7, anchor='start')
    d.text(X(tmin) + 4, Y(1) - 5, 'STATIC · 1917', size=7, anchor='start')
    d.text(X(0) + 6, Y(1) + 14, 'TODAY', size=7, anchor='start')
    d.text(X(tmax), y0 + 16, 'TIME →', size=7, anchor='end')
    d.text(X(tmin) - 6, Y(amax) + 4, 'SIZE', size=7, anchor='end')
    d.text(200, 24, 'THREE HISTORIES WITH TODAY\u2019S EXPANSION RATE', size=7)
    return d


# ---------------------------------------------------------------- cosmology now

def cosmology_now():
    """The two routes to the Hubble constant.

    Above, the distance ladder as three rungs: parallax fixes the distance to
    nearby Cepheids, whose period gives their true brightness; Cepheids in
    galaxies that host type Ia supernovae fix the supernovae's brightness;
    supernovae far off in the expansion give the rate. Below, the early
    universe's route: the acoustic peaks of the cosmic microwave background,
    drawn as a damped oscillation (illustrative, not fitted)."""
    d = D()
    w = 112
    rungs = [(32, 176), (32 + w, 136), (32 + 2 * w, 96)]    # each rung's left end and floor
    # construction: the ladder's staircase and the lower plot's axes
    d.group('thin')
    stair = [(rungs[0][0], rungs[0][1] + 18), (rungs[0][0], rungs[0][1])]
    for x, y in rungs:
        stair += [(x, y), (x + w, y)]
    d.line(*stair)
    d.line((32, 206), (32, 282), (370, 282))
    # rung 1: parallax. The Sun, the Earth's orbit seen at a slant, and the sight lines to a star
    d.group()
    sx, sy = 88, 160
    d.ellipse(sx, sy, 30, 7)
    d.circle(sx, sy, 2.5)
    star = (sx, 104)
    d.line((sx - 30, sy), star, (sx + 30, sy))
    d.circle(*star, 2.5)
    # rung 2: a Cepheid's light curve, a fast rise and a slow fall, two and a half cycles
    cep = []
    for k in range(0, 121):
        ph = (k / 120 * 2.5 + 0.85) % 1
        b = 1 - ph / 0.8 if ph < 0.8 else (ph - 0.8) / 0.2
        cep.append((rungs[1][0] + 10 + k * 0.78, rungs[1][1] - 14 - 30 * b))
    d.line(*cep)
    # rung 3: a type Ia supernova's light curve, a rise over about three weeks and a long decline
    sn = []
    for k in range(0, 121):
        t = k / 120 * 90 - 18          # days from peak
        m = math.exp(-(t / 9) ** 2) if t < 0 else 0.25 + 0.75 * math.exp(-t / 14) - 0.2 * t / 90
        sn.append((rungs[2][0] + 10 + k * 0.78, rungs[2][1] - 12 - 50 * m))
    d.line(*sn)
    # the early route: acoustic peaks, a damped oscillation rising from a plateau
    d.group('mid')
    pk = []
    for k in range(0, 241):
        l = k / 240
        amp = math.exp(-2.2 * l) * (0.35 + 0.65 * math.sin(math.pi * l * 4.2 + 0.35) ** 2)
        pk.append((38 + k * 1.38, 278 - 60 * amp * min(1, l * 12)))
    d.line(*pk)
    # arrows up each riser: each rung calibrates the next
    d.group()
    for (x, y), (_, y2) in zip(rungs, rungs[1:]):
        d.line((x + w + 8, y - 4), (x + w + 8, y2 + 6))
        _arrow(d, x + w + 8, y2 + 6, -math.pi / 2, 4)
    d.group()
    d.text(88, 192, 'PARALLAX', size=7)
    d.text(rungs[1][0] + w / 2, rungs[1][1] + 16, 'CEPHEIDS', size=7)
    d.text(rungs[2][0] + w / 2, rungs[2][1] + 16, 'SUPERNOVAE', size=7)
    d.text(200, 24, 'LATE UNIVERSE · THE DISTANCE LADDER', size=7)
    d.text(368, 214, 'EARLY UNIVERSE · CMB PEAKS', size=7, anchor='end')
    return d


# ---------------------------------------------------------------- where physics is

def where_physics_is():
    """The cGh cube of Bronstein and Gamow: each corner a theory, each axis a constant switched on.

    From classical mechanics at the origin, 1/c (special relativity), G
    (Newton's gravity) and ħ (quantum mechanics); the faces' far corners are
    general relativity, quantum field theory and quantum mechanics in
    Newtonian gravity; the corner with all three is quantum gravity, which
    nobody has. Its three edges are drawn as construction lines."""
    d = D()
    ax, ay = math.radians(-20), math.radians(34)
    s, cx, cy = 66, 200, 166
    # axes: x = 1/c, y = G, z = ħ; a corner (i, j, k) sits at coordinates -1 or 1
    V = {(i, j, k): (2 * i - 1, 2 * j - 1, 2 * k - 1) for i in (0, 1) for j in (0, 1) for k in (0, 1)}
    P = {key: (cx + s * rot(v, ax, ay)[0], cy - s * rot(v, ax, ay)[1]) for key, v in V.items()}
    top = (1, 1, 1)
    edges = [(a, b) for a in V for b in V if a < b and sum(abs(p - q) for p, q in zip(a, b)) == 1]
    known = [e for e in edges if top not in e]
    unknown = [e for e in edges if top in e]
    o = P[(0, 0, 0)]
    ext = lambda key, f: (o[0] + f * (P[key][0] - o[0]), o[1] + f * (P[key][1] - o[1]))
    # construction: the three axes run on past the cube, and the unfinished edges
    d.group('thin')
    for key in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        d.line(P[key], ext(key, 1.3))
    d.lines([[P[a], P[b]] for a, b in unknown])
    # the cube's known edges
    d.group()
    d.lines([[P[a], P[b]] for a, b in known])
    # corners: a dot for each theory we have, an open ring for the one we don't
    d.group('mid')
    for key, p in P.items():
        d.circle(*p, 7 if key == top else 2.2)
    d.group()
    names = {  # label, dx, dy, anchor
        (0, 0, 0): ('NEWTON', -8, 12, 'end'),
        (1, 0, 0): ('SPECIAL RELATIVITY', 8, 14, 'start'),
        (0, 1, 0): ('GRAVITY', -8, 3, 'end'),
        (0, 0, 1): ('QUANTUM MECHANICS', -6, 14, 'end'),
        (1, 1, 0): ('GENERAL RELATIVITY', 8, -6, 'start'),
        (1, 0, 1): ('QFT', 8, 3, 'start'),
        (0, 1, 1): ('G + ħ', -8, -6, 'end'),
        (1, 1, 1): ('QUANTUM GRAVITY?', 12, -8, 'start'),
    }
    for key, (lab, dx, dy, anc) in names.items():
        d.text(P[key][0] + dx, P[key][1] + dy, lab, size=7, anchor=anc)
    for key, lab in (((1, 0, 0), '1/c'), ((0, 1, 0), 'G'), ((0, 0, 1), 'ħ')):
        x, y = ext(key, 1.4)
        d.text(x, y + 3, lab, size=9)
    d.text(200, 22, 'THE cGh CUBE', size=7)
    return d


PLATES = {
    'dark-energy': dark_energy,
    'cosmology-now': cosmology_now,
    'where-physics-is': where_physics_is,
}


# ---------------------------------------------------------------- the H0 chart

H0 = [  # label, sublabel, value, ±, early universe?
    ('Planck', 'CMB, 2018', 67.4, 0.5, True),
    ('SPT + ACT + Planck', 'CMB, 2025', 67.19, 0.38, True),
    ('CCHP', 'red giants, HST + JWST, 2024', 70.39, 1.94, False),
    ('SH0ES', 'Cepheids, HST + JWST, 2025', 73.49, 0.93, False),
    ('SH0ES', 'Cepheids + red giants, 2025', 73.18, 0.88, False),
]


def h0_chart():
    """Dot-and-whisker chart of five Hubble-constant measurements, 64 to 76 km/s/Mpc."""
    w, h = 480, 312
    lo, hi = 64, 76
    left, right = 190, 460
    X = lambda v: left + (v - lo) / (hi - lo) * (right - left)
    desc = ('Dot-and-whisker chart of the Hubble constant in km/s/Mpc. From the early universe, with the '
            'standard model: Planck 2018, 67.4 ± 0.5; SPT-3G, ACT and Planck combined, 2025, 67.19 ± 0.38. '
            'From the distance ladder: the Chicago-Carnegie Hubble Program, red giants with HST and JWST, '
            '70.39 ± 1.94 (its statistical and systematic errors combined here in quadrature); SH0ES, '
            'Cepheids with HST and JWST, 73.49 ± 0.93; SH0ES, Cepheids and red giants, 73.18 ± 0.88. '
            'Data: Planck Collaboration 2020; Camphuis et al. 2025; Freedman et al. 2024; Riess et al. 2025.')
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">',
           '<title id="t">The Hubble constant: early universe against the distance ladder</title>',
           f'<desc id="d">{escape(desc)}</desc>',
           '<g font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="currentColor">',
           '<g class="muted">']
    base = 44 + 44 * len(H0)
    for v in range(lo, hi + 1, 2):
        op = '0.9' if v == lo else '0.3'
        out.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="40" y2="{base}" stroke="currentColor" stroke-opacity="{op}" stroke-width="0.6"/>')
        out.append(f'<text x="{X(v):.1f}" y="{base + 16}" text-anchor="middle">{v}</text>')
    out.append('</g>')
    for i, (lab, sub, v, e, early) in enumerate(H0):
        y = 62 + 44 * i
        cls = '' if early else ' class="accent"'
        stroke = 'currentColor'
        out.append(f'<text x="{left - 12}" y="{y - 2}" text-anchor="end">{escape(lab)}</text>')
        out.append(f'<text x="{left - 12}" y="{y + 11}" text-anchor="end" font-size="9" class="muted" fill="currentColor">{escape(sub)}</text>')
        out.append(f'<line x1="{X(v - e):.1f}" x2="{X(v + e):.1f}" y1="{y}" y2="{y}" stroke="{stroke}" stroke-width="2"{cls}/>')
        for xe in (X(v - e), X(v + e)):
            out.append(f'<line x1="{xe:.1f}" x2="{xe:.1f}" y1="{y - 5}" y2="{y + 5}" stroke="{stroke}" stroke-width="1.5"{cls}/>')
        out.append(f'<circle cx="{X(v):.1f}" cy="{y}" r="5" fill="currentColor"{cls}/>')
        out.append(f'<text x="{X(v):.1f}" y="{y - 10}" text-anchor="middle" font-size="10">{v:g}</text>')
    out.append(f'<text x="{left}" y="{base + 34}" font-size="9" class="muted" fill="currentColor">km/s/Mpc · plain: CMB · accent: distance ladder</text>')
    out.append(f'<text x="16" y="22" font-size="12" letter-spacing="1">THE HUBBLE CONSTANT · TWO ROUTES</text>')
    out.append('</g></svg>')
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, '..', '..', 'subjects', 'physics', 'frames', 'cosmology-now', 'hubble-constant.svg')
    with open(path, 'w') as fh:
        fh.write(h0_chart())
    print('wrote', os.path.normpath(path))
