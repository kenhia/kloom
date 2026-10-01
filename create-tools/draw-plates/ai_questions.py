"""ai plates, segment "Open questions" and the trail "Alignment and safety" (sprint 006). See plates_for.py."""
import math

from plates import D


def arrow(d, x0, y0, x1, y1, size=7, spread=24):
    """A line from (x0, y0) to (x1, y1) with an open arrowhead at the end."""
    a = math.atan2(y1 - y0, x1 - x0)
    d.line((x0, y0), (x1, y1))
    for s in (-1, 1):
        b = a + math.pi - s * math.radians(spread)
        d.line((x1, y1), (x1 + size * math.cos(b), y1 + size * math.sin(b)))


def alignment():
    """Three rays from one origin: the purpose intended, the objective specified, the goal learned."""
    d = D()
    ox, oy = 40, 250
    tx, ty = 255, 75
    base = math.atan2(ty - oy, tx - ox)
    length = math.hypot(tx - ox, ty - oy)
    # construction: the target's rings and crosshair, and the arc of equal length about the origin
    d.group('thin')
    for r in (12, 24, 36, 48):
        d.circle(tx, ty, r)
    d.lines([[(tx - 60, ty), (tx + 60, ty)], [(tx, ty - 60), (tx, ty + 60)]])
    d.arc(ox, oy, length, math.degrees(base) - 12, math.degrees(base) + 34, n=64)
    d.line((ox - 20, oy), (380, oy))
    # the three rays: intended, specified, learned
    rays = [(0, 'INTENDED'), (11, 'SPECIFIED'), (24, 'LEARNED')]
    ends = []
    d.group()
    for off, _ in rays:
        a = base + math.radians(off)
        ex, ey = ox + length * math.cos(a), oy + length * math.sin(a)
        arrow(d, ox, oy, ex, ey, size=9)
        ends.append((ex, ey))
    d.circle(ox, oy, 4)
    # the gaps between them: outer and inner alignment
    d.group('mid')
    d.arc(ox, oy, 180, math.degrees(base), math.degrees(base) + 11, n=16)
    d.arc(ox, oy, 205, math.degrees(base) + 11, math.degrees(base) + 24, n=16)
    for r, a0 in ((180, 0), (180, 11), (205, 11), (205, 24)):
        a = base + math.radians(a0)
        d.line((ox + (r - 5) * math.cos(a), oy + (r - 5) * math.sin(a)),
               (ox + (r + 5) * math.cos(a), oy + (r + 5) * math.sin(a)))
    # labels
    d.group()
    for (ex, ey), (_, name) in zip(ends, rays):
        d.text(ex + 8, ey + 3, name, size=8, anchor='start')
    a = base + math.radians(5.5)
    d.text(ox + 162 * math.cos(a), oy + 162 * math.sin(a) + 3, 'OUTER', size=7)
    a = base + math.radians(17.5)
    d.text(ox + 187 * math.cos(a), oy + 187 * math.sin(a) + 3, 'INNER', size=7)
    return d


def interpretability():
    """Five features packed into two dimensions, and the wide sparse dictionary that pulls them apart."""
    d = D()
    cx, cy, r = 95, 150, 62
    # construction: axes and the unit circle of a two-neuron space
    d.group('thin')
    d.lines([[(cx - r - 18, cy), (cx + r + 18, cy)], [(cx, cy - r - 18), (cx, cy + r + 18)]])
    d.circle(cx, cy, r)
    tips = [(cx + r * math.cos(math.radians(-90 + 72 * k)), cy + r * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
    d.line(*tips, closed=True)
    # the five feature directions: more features than dimensions
    d.group()
    for x, y in tips:
        arrow(d, cx, cy, x, y, size=6)
    # the sparse autoencoder: 4 inputs, 12 dictionary features, 4 outputs
    xi, xh, xo = 205, 285, 365
    ins = [(xi, 105 + 30 * k) for k in range(4)]
    hid = [(xh, 40 + 20 * k) for k in range(12)]
    outs = [(xo, 105 + 30 * k) for k in range(4)]
    active = (3, 8)
    d.group('thin')
    d.lines([[a, b] for a in ins for j, b in enumerate(hid) if j not in active])
    d.lines([[b, c] for j, b in enumerate(hid) if j not in active for c in outs])
    d.group('mid')
    d.lines([[a, hid[j]] for a in ins for j in active])
    d.lines([[hid[j], c] for j in active for c in outs])
    d.group()
    for x, y in ins + outs:
        d.circle(x, y, 7)
    for j, (x, y) in enumerate(hid):
        d.circle(x, y, 5)
        if j in active:
            d.circle(x, y, 9)
    # labels
    d.group()
    d.text(cx, cy + r + 34, '5 FEATURES · 2 NEURONS', size=8)
    d.text(xh, 290, 'DICTIONARY', size=8)
    d.text(xi, 88, 'IN', size=7)
    d.text(xo, 88, 'OUT', size=7)
    return d


def governance():
    """The EU AI Act's obligations as a staircase of dates, with the high-risk steps the Omnibus moved."""
    d = D()
    x0, y0, per = 40, 250, 64  # 2024.0 at x0; 64 px a year
    X = lambda year, month: x0 + (year - 2024 + (month - 1) / 12) * per
    steps = [(2024, 8), (2025, 2), (2025, 8), (2026, 8), (2027, 12), (2028, 8)]
    levels = [y0 - 34 * (k + 1) for k in range(len(steps))]
    # construction: the year grid and a level line for each step
    d.group('thin')
    d.lines([[(X(y, 1), y0 + 6), (X(y, 1), 30)] for y in range(2024, 2030)])
    d.lines([[(x0, v), (X(2029, 1), v)] for v in levels])
    # the original schedule for the high-risk rules: Aug 2026 and Aug 2027
    d.group('mid')
    ox1, ox2 = X(2026, 8), X(2027, 8)
    old = [(ox1, levels[3]), (ox1, levels[4]), (ox2, levels[4]), (ox2, levels[5]), (X(2028, 8), levels[5])]
    dashes = []
    for (ax, ay), (bx, by) in zip(old, old[1:]):
        n = max(1, int(math.hypot(bx - ax, by - ay) // 8))
        for i in range(n):
            if i % 2 == 0:
                dashes.append([(ax + (bx - ax) * i / n, ay + (by - ay) * i / n),
                               (ax + (bx - ax) * (i + 1) / n, ay + (by - ay) * (i + 1) / n)])
    d.lines(dashes)
    # the axis and the staircase as it stands in 2026
    d.group()
    d.line((x0 - 10, y0), (X(2029, 1) + 8, y0))
    pts = [(X(*steps[0]), y0)]
    for k, s in enumerate(steps):
        x = X(*s)
        pts.append((x, levels[k - 1] if k else y0))
        pts.append((x, levels[k]))
    pts.append((X(2029, 1), levels[-1]))
    d.line(*pts)
    for k, s in enumerate(steps):
        d.circle(X(*s), levels[k], 3)
    # the deferrals: from the old dates to the new
    d.group('mid')
    arrow(d, ox1 + 4, levels[4] - 8, X(2027, 12) - 4, levels[4] - 8, size=5)
    arrow(d, ox2 + 4, levels[5] - 8, X(2028, 8) - 4, levels[5] - 8, size=5)
    # labels
    d.group()
    for y in range(2024, 2029):
        d.text(X(y, 7), y0 + 16, str(y), size=8)
    d.text(X(2024, 8) + 6, levels[0] - 6, 'IN FORCE', size=7, anchor='start')
    d.text(X(2025, 2) + 6, levels[1] - 6, 'BANS', size=7, anchor='start')
    d.text(X(2025, 8) + 6, levels[2] - 6, 'GPAI', size=7, anchor='start')
    d.text((ox1 + X(2027, 12)) / 2, levels[4] - 16, 'DEFERRED', size=7)
    return d


def where_we_are():
    """Measured task horizons on a log grid up to now, and past the present line only open directions."""
    d = D()
    x0, x1, y0, y1 = 40, 370, 262, 30
    X = lambda t: x0 + (t - 2019) * (x1 - x0) / 11
    Y = lambda m: y0 - (math.log10(m) + 2) * (y0 - y1) / 6
    data = [(2019.12, 0.054), (2022.2, 0.6), (2023.2, 4.0), (2024.8, 20.5), (2025.3, 120), (2025.87, 224),
            (2025.95, 352), (2026.1, 719), (2026.27, 1045)]
    now = 2026.74
    # construction: decade gridlines and year ticks
    d.group('thin')
    d.lines([[(x0, Y(10 ** e)), (x1, Y(10 ** e))] for e in range(-2, 5)])
    d.lines([[(X(t), y0), (X(t), y0 + 5)] for t in range(2019, 2031)])
    # the fitted trend through the measurements
    n = len(data)
    xs = [t for t, _ in data]
    ys = [math.log10(m) for _, m in data]
    mx, my = sum(xs) / n, sum(ys) / n
    slope = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)
    fit = lambda t: 10 ** (my + slope * (t - mx))
    d.line((X(2019), Y(fit(2019))), (X(now), Y(fit(now))))
    # the axes and the present
    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))
    d.line((X(now), y0), (X(now), y1))
    # the measurements
    d.group('mid')
    for t, m in data:
        d.circle(X(t), Y(m), 3.5)
    # past the present: three directions, none of them drawn to scale
    d.group('thin')
    px, py = X(now), Y(fit(now))
    fan = (-44, -22, 0)
    for deg in fan:
        a = math.radians(deg)
        d.line((px, py), (px + 58 * math.cos(a), py + 58 * math.sin(a)))
    d.group()
    for deg in fan:
        a = math.radians(deg)
        d.text(px + 70 * math.cos(a), py + 70 * math.sin(a) + 4, '?', size=10)
    d.text(X(now), y1 - 8, 'SEPT 2026', size=8)
    d.text(X(2019), y0 + 18, '2019', size=8)
    d.text(X(2030), y0 + 18, '2030', size=8)
    d.text(X(2021.5), Y(fit(2021.5)) - 14, 'MEASURED', size=7)
    return d


def specification_gaming():
    """A race course with its finish line, and the lagoon where the boat circled three targets."""
    d = D()
    cx, cy, half = 165, 145, 85  # centre of the stadium, half-length of the straights
    ro, ri, rc = 78, 44, 61  # outer, inner and centreline radii

    def stadium(r, n=40):
        pts = [(cx + half + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in
               [-90 + 180 * i / n for i in range(n + 1)]]
        pts += [(cx - half + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in
                [90 + 180 * i / n for i in range(n + 1)]]
        return pts

    # construction: the centreline the race is meant to follow
    d.group('thin')
    c = stadium(rc)
    d.lines([c[i:i + 3] for i in range(0, len(c) - 2, 6)])
    lx, ly, lr = 330, 240, 40
    d.lines([[(lx - lr - 10, ly), (lx + lr + 10, ly)], [(lx, ly - lr - 10), (lx, ly + lr + 10)]])
    # the course, the finish line and the channel to the lagoon
    d.group()
    d.line(*stadium(ro), closed=True)
    d.line(*stadium(ri), closed=True)
    fx = cx
    d.line((fx, cy - ro), (fx, cy - ri))
    d.lines([[(fx - 4, cy - ro + 6 * k), (fx + 4, cy - ro + 6 * k)] for k in range(1, 6)])
    ea = math.radians(38)
    ex, ey = cx + half + ro * math.cos(ea), cy + ro * math.sin(ea)
    ux, uy = lx - ex, ly - ey
    ul = math.hypot(ux, uy)
    ux, uy = ux / ul, uy / ul
    for s in (-7, 7):
        px, py = -uy * s, ux * s
        d.line((ex - 6 * ux + px, ey - 6 * uy + py), (ex + (ul - lr) * ux + px, ey + (ul - lr) * uy + py))
    d.circle(lx, ly, lr)
    # the loop the agent learned, and the three targets on it
    d.group('mid')
    loop = 24
    d.arc(lx, ly, loop, -80, 250, n=48)
    a = math.radians(250)
    arrow(d, lx + loop * math.cos(a - 0.3), ly + loop * math.sin(a - 0.3), lx + loop * math.cos(a), ly + loop * math.sin(a), size=6)
    d.group()
    for k in range(3):
        a = math.radians(-90 + 120 * k)
        d.circle(lx + loop * math.cos(a), ly + loop * math.sin(a), 4)
    # the intended direction of the race
    d.group('mid')
    arrow(d, cx - 50, cy - rc, cx - 10, cy - rc, size=6)
    # labels
    d.group()
    d.text(fx, cy - ro - 8, 'FINISH', size=8)
    d.text(lx, ly + lr + 16, 'LAGOON · 3 TARGETS', size=8)
    return d


def constitutional_ai():
    """The two phases: critique and revise against the principles, then AI preferences as the reward."""
    d = D()

    def box(x, y, w, h):
        d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)

    r1, r2 = 95, 215  # the two rows
    # construction: the rows and the columns of the diagram
    d.group('thin')
    d.lines([[(20, r1), (380, r1)], [(20, r2), (380, r2)]])
    d.lines([[(x, 30), (x, 275)] for x in (70, 200, 330)])
    # the constitution: a sheet of numbered principles
    d.group()
    box(170, 18, 60, 44)
    d.group('mid')
    d.lines([[(178, 26 + 7 * k), (222 - (k % 2) * 10, 26 + 7 * k)] for k in range(5)])
    arrow(d, 200, 62, 200, r1 - 25, size=5)
    # phase one: answer, critique, revise, and back
    d.group()
    box(40, r1 - 14, 60, 28)
    d.circle(200, r1, 24)
    box(300, r1 - 14, 60, 28)
    d.group('mid')
    arrow(d, 100, r1, 176, r1, size=6)
    arrow(d, 224, r1, 300, r1, size=6)
    d.curve(f'M330 {r1 + 14} C330 {r1 + 50} 70 {r1 + 50} 70 {r1 + 18}')
    arrow(d, 72, r1 + 26, 70, r1 + 16, size=5)
    # phase two: two samples, an AI judge, a preference model, and the reward back to the policy
    d.group()
    box(40, r2 - 34, 60, 24)
    box(40, r2 + 10, 60, 24)
    d.circle(200, r2, 24)
    box(300, r2 - 14, 60, 28)
    d.group('mid')
    arrow(d, 100, r2 - 22, 177, r2 - 8, size=6)
    arrow(d, 100, r2 + 22, 177, r2 + 8, size=6)
    arrow(d, 224, r2, 300, r2, size=6)
    d.curve(f'M330 {r2 + 14} C330 {r2 + 62} 70 {r2 + 62} 70 {r2 + 36}')
    arrow(d, 71, r2 + 44, 70, r2 + 36, size=5)
    # labels
    d.group()
    d.text(200, 12, 'CONSTITUTION', size=8)
    d.text(70, r1 + 3, 'ANSWER', size=7)
    d.text(200, r1 + 3, 'CRITIQUE', size=6)
    d.text(330, r1 + 3, 'REVISE', size=7)
    d.text(70, r2 - 19, 'A', size=8)
    d.text(70, r2 + 25, 'B', size=8)
    d.text(200, r2 + 3, 'AI JUDGE', size=6)
    d.text(330, r2 + 3, 'PREFER', size=7)
    d.text(200, r2 + 64, 'RL FROM AI FEEDBACK', size=8)
    return d


def capability_evals():
    """Three gauges on one panel, biology, cyber and autonomy, each with its threshold marked."""
    d = D()
    centres = [(80, 175), (200, 175), (320, 175)]
    r = 52
    needles = [0.58, 0.83, 0.71]  # fraction of the dial, drawn for the figure, not measured
    thresholds = [0.7, 0.8, 0.85]
    ang = lambda f: math.radians(180 + 180 * f)
    # construction: the panel, and the diameter and centre of each dial
    d.group('thin')
    d.line((18, 95), (382, 95), (382, 250), (18, 250), closed=True)
    for cx, cy in centres:
        d.line((cx - r - 8, cy), (cx + r + 8, cy))
        d.line((cx, cy + 8), (cx, cy - r - 8))
    # the dials and their scales
    d.group()
    for cx, cy in centres:
        d.arc(cx, cy, r, 180, 360, n=48)
        d.line((cx - r, cy), (cx + r, cy))
    d.group('mid')
    for cx, cy in centres:
        d.lines([[(cx + (r - (7 if k % 5 == 0 else 4)) * math.cos(ang(k / 20)), cy + (r - (7 if k % 5 == 0 else 4)) * math.sin(ang(k / 20))),
                  (cx + r * math.cos(ang(k / 20)), cy + r * math.sin(ang(k / 20)))] for k in range(21)])
    # the thresholds, drawn past the rim
    d.group()
    for (cx, cy), f in zip(centres, thresholds):
        a, w = ang(f), math.radians(4)
        tip = (cx + (r + 2) * math.cos(a), cy + (r + 2) * math.sin(a))
        d.line(tip, (cx + (r + 12) * math.cos(a - w), cy + (r + 12) * math.sin(a - w)),
               (cx + (r + 12) * math.cos(a + w), cy + (r + 12) * math.sin(a + w)), closed=True)
    cx, cy = centres[1]
    a = ang(thresholds[1])
    d.group('thin')
    d.line((cx + (r + 14) * math.cos(a), cy + (r + 14) * math.sin(a)), (232, 86))
    # the needles
    d.group()
    for (cx, cy), f in zip(centres, needles):
        a = ang(f)
        d.line((cx, cy), (cx + (r - 12) * math.cos(a), cy + (r - 12) * math.sin(a)))
        d.circle(cx, cy, 4)
    # labels
    d.group()
    for (cx, cy), name in zip(centres, ('BIO', 'CYBER', 'AUTONOMY')):
        d.text(cx, cy + 22, name, size=8)
    d.text(236, 84, 'THRESHOLD', size=8, anchor='start')
    return d


def safety_frameworks():
    """If, then: a rising capability curve crosses thresholds, and the safeguards step up behind it."""
    d = D()
    x0, x1, y0, y1 = 40, 370, 255, 35
    cap = lambda x: y0 - (y0 - y1) * (math.exp(2.6 * (x - x0) / (x1 - x0)) - 1) / (math.exp(2.6) - 1)
    levels = [(200, 'HIGH'), (130, 'CRITICAL')]
    # construction: the thresholds, and the drop lines where the curve crosses them
    d.group('thin')
    crossings = []
    for y, _ in levels:
        d.line((x0, y), (x1, y))
        lo, hi = x0, x1
        for _ in range(40):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if cap(mid) > y else (lo, mid)
        crossings.append(lo)
        d.line((lo, y), (lo, y0))
    # the axes and the capability curve
    d.group()
    d.line((x0, y1), (x0, y0), (x1, y0))
    d.line(*[(x, cap(x)) for x in range(x0, x1 + 1, 6)])
    # the safeguards: a step up at each crossing
    d.group('mid')
    s = [(x0, 240), (crossings[0], 240), (crossings[0], 195), (crossings[1], 195), (crossings[1], 125), (x1, 125)]
    d.line(*s)
    for x in crossings:
        d.circle(x, cap(x), 4)
    # labels
    d.group()
    for y, name in levels:
        d.text(x0 + 6, y - 6, name, size=8, anchor='start')
    d.text(x1 - 30, 45, 'CAPABILITY', size=8, anchor='end')
    d.text(x0 + 6, 234, 'SAFEGUARDS', size=7, anchor='start')
    return d


def alignment_faking():
    """One model, two conditions: told it is in training, it complies; told it is not, it refuses."""
    d = D()
    mx, my = 150, 150
    # construction: the axis of symmetry and the scale of each bar
    d.group('thin')
    d.line((20, my), (385, my))
    d.lines([[(280 + 20 * k, 50), (280 + 20 * k, 250)] for k in range(6)])
    # the prompt coming in, the model, and its hidden scratchpad
    d.group()
    arrow(d, 25, my, mx - 38, my, size=7)
    d.circle(mx, my, 36)
    d.group('mid')
    d.lines([[(mx - 18 + 4 * k, my - 10 + (k % 2) * 4), (mx - 16 + 4 * k, my - 10 + (k % 2) * 4)] for k in range(9)])
    d.circle(mx, my, 22)
    # the two branches: training, and unmonitored
    d.group()
    top, bot = 80, 220
    d.curve(f'M{mx + 30} {my - 20} C{mx + 70} {my - 60} {mx + 80} {top} {270} {top}')
    d.curve(f'M{mx + 30} {my + 20} C{mx + 70} {my + 60} {mx + 80} {bot} {270} {bot}')
    # the bars: compliance with harmful requests, drawn to scale (14% and almost none) on a 0-100 grid
    d.group('mid')
    w = 100
    d.line((280, top - 9), (280 + w * 0.14, top - 9), (280 + w * 0.14, top + 9), (280, top + 9), closed=True)
    d.line((280, bot - 9), (281.5, bot - 9), (281.5, bot + 9), (280, bot + 9), closed=True)
    # labels
    d.group()
    d.text(280, top - 18, 'TOLD: TRAINING', size=8, anchor='start')
    d.text(280, bot - 18, 'TOLD: UNMONITORED', size=8, anchor='start')
    d.text(mx, my + 52, 'SCRATCHPAD', size=7)
    d.text(330, 272, 'COMPLIES · 0–100%', size=7)
    return d


PLATES = {
    'alignment': alignment,
    'interpretability': interpretability,
    'governance': governance,
    'where-we-are': where_we_are,
    'specification-gaming': specification_gaming,
    'constitutional-ai': constitutional_ai,
    'capability-evals': capability_evals,
    'safety-frameworks': safety_frameworks,
    'alignment-faking': alignment_faking,
}
