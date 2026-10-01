"""computing plates, trail "Bletchley and Colossus" (sprint 015). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _toward(p, q, r):
    """The point at distance r from p along the line to q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    return p[0] + dx * r / L, p[1] + dy * r / L


def _xor(d, x, y, r=4):
    """A modulo-2 adder: a circle with a cross."""
    d.circle(x, y, r)
    d.lines([[(x - r, y), (x + r, y)], [(x, y - r), (x, y + r)]])


def bombe():
    """The bombe menu for the crib ATTACKATDAWN against WSNPNLKLSTCS: each pairing is an Enigma
    equivalent (a drum triplet) offset by its place in the crib, and the loops ATLK, TNS and TAWCN
    are what let the bombe reject a rotor position by contradiction."""
    d = D()
    crib, cipher = 'ATTACKATDAWN', 'WSNPNLKLSTCS'
    pos = {'A': (138, 150), 'T': (248, 150), 'L': (248, 238), 'K': (138, 238), 'W': (104, 72),
           'C': (190, 38), 'N': (284, 72), 'S': (338, 150), 'P': (46, 150), 'D': (360, 238)}
    edges = [(i + 1, p, c) for i, (p, c) in enumerate(zip(crib, cipher))]
    rn, rd = 11, 9  # letter circle and drum radii
    loops = [['A', 'T', 'L', 'K'], ['T', 'N', 'S'], ['T', 'A', 'W', 'C', 'N']]
    # construction: each loop traced inside itself, towards its centroid, so the closures read
    d.group('thin')
    for loop in loops:
        cx = sum(pos[k][0] for k in loop) / len(loop)
        cy = sum(pos[k][1] for k in loop) / len(loop)
        pts = [_toward(pos[k], (cx, cy), 20) for k in loop]
        d.line(*pts, closed=True)
    # the plugboard letters: each node is a 26-way cable's worth of test wires
    d.group()
    for k, (x, y) in pos.items():
        d.circle(x, y, rn)
    # the cables from each letter to each Enigma equivalent it meets
    d.group('mid')
    segs = []
    for _, a, b in edges:
        pa, pb = pos[a], pos[b]
        m = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)
        segs.append([_toward(pa, pb, rn), _toward(m, pa, rd)])
        segs.append([_toward(m, pb, rd), _toward(pb, pa, rn)])
    d.lines(segs)
    # the Enigma equivalents: a drum face at each pairing, its rotors stepped on by the crib position
    d.group()
    for i, a, b in edges:
        pa, pb = pos[a], pos[b]
        m = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)
        d.circle(m[0], m[1], rd)
        ang = 2 * math.pi * (i - 1) / 26 - math.pi / 2  # the fast drum's offset, one step per crib letter
        d.line((m[0], m[1]), (m[0] + (rd - 2) * math.cos(ang), m[1] + (rd - 2) * math.sin(ang)))
    # labels: letters, crib positions, the key
    d.group()
    for k, (x, y) in pos.items():
        d.text(x, y + 3.5, k, size=10)
    for i, a, b in edges:
        pa, pb = pos[a], pos[b]
        m = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)
        dx, dy = pb[0] - pa[0], pb[1] - pa[1]
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        d.text(m[0] + nx * 16, m[1] + ny * 16 + 3, str(i), size=7)
    d.text(200, 278, 'CRIB ATTACKATDAWN · CIPHER WSNPNLKLSTCS', size=8)
    d.text(200, 291, 'THREE LOOPS: ATLK · TNS · TAWCN', size=7)
    return d


def _cams(n, seed):
    """A repeatable cam pattern of n cams, about half raised (a small linear congruential generator)."""
    out, s = [], seed
    for _ in range(n):
        s = (1103515245 * s + 12345) % (1 << 31)
        out.append((s >> 16) & 1)
    return out


def _wheel(d, x, y, n, k, seed):
    """A pin wheel of n cams seen face on, radius proportional to n; raised cams stand out further."""
    r = k * n
    d.circle(x, y, r)
    segs = []
    for i, up in enumerate(_cams(n, seed)):
        a = 2 * math.pi * i / n - math.pi / 2
        r1 = r + (3.2 if up else 1.2)
        segs.append([(x + r * math.cos(a), y + r * math.sin(a)), (x + r1 * math.cos(a), y + r1 * math.sin(a))])
    d.lines(segs)
    return r


def tunny():
    """The Lorenz SZ42's twelve wheels as Tutte reconstructed them: five chi wheels that step with
    every letter, five psi wheels that step together only when the motor wheels allow, and the two
    additions, modulo 2, of chi and psi into each of the five impulses."""
    d = D()
    k = 0.3
    chi = [41, 31, 29, 26, 23]
    psi = [43, 47, 51, 53, 59]
    yw = 118
    chi_x, x = [], 22
    for n in chi:
        x += k * n + 3.5
        chi_x.append(x)
        x += k * n + 3.5 + 6
    psi_x, x = [], 196
    for n in psi:
        x += k * n + 3.5
        psi_x.append(x)
        x += k * n + 3.5 + 3
    lanes = [196 + 13 * i for i in range(5)]
    mu = [(61, 250, 44), (37, 318, 44)]
    # construction: wheel centre lines and the two axles; the impulse lanes' guide lines
    d.group('thin')
    d.lines([[(x, yw - 26), (x, lanes[i] - 6)] for i, x in enumerate(chi_x)])
    d.lines([[(x, yw - 26), (x, lanes[i] - 6)] for i, x in enumerate(psi_x)])
    d.line((12, yw), (388, yw))
    d.lines([[(mx, my), (mx, yw - 24)] for _, mx, my in mu])
    # the wheels
    d.group()
    for i, (n, x) in enumerate(zip(chi, chi_x)):
        _wheel(d, x, yw, n, k, 7 + i)
    for i, (n, x) in enumerate(zip(psi, psi_x)):
        _wheel(d, x, yw, n, k, 17 + i)
    for j, (n, mx, my) in enumerate(mu):
        _wheel(d, mx, my, n, k, 29 + j)
    # the impulse lanes: plain text in, cipher out, through a chi adder and a psi adder each
    d.group('mid')
    d.lines([[(16, y), (384, y)] for y in lanes])
    for i, y in enumerate(lanes):
        _arrow(d, 384, y, 0, 3)
    # the adders
    d.group()
    for i, y in enumerate(lanes):
        _xor(d, chi_x[i], y)
        _xor(d, psi_x[i], y)
    # the motor: mu61 steps mu37, mu37 releases the psi wheels, all five at once
    d.group('mid')
    d.line((250 + 18.3 + 2, 44), (318 - 11.1 - 2, 44))
    d.line((318, 44 + 11.1 + 3), (318, 76), (psi_x[0] - 12, 76), (psi_x[0] - 12, yw - 22))
    d.line((psi_x[-1] + 12, 76), (psi_x[-1] + 12, yw - 22))
    d.line((psi_x[0] - 12, 76), (psi_x[-1] + 12, 76))
    # labels
    d.group()
    d.text(8, lanes[2] + 3, 'P', size=9, anchor='end')
    d.text(392, lanes[2] + 3, 'Z', size=9, anchor='start')
    for i, y in enumerate(lanes):
        d.text(18, y - 3, str(i + 1), size=6, anchor='start')
    for n, x in zip(chi, chi_x):
        d.text(x, yw + 4 * 0 - k * n - 9, str(n), size=7)
    for n, x in zip(psi, psi_x):
        d.text(x, yw + k * n + 13, str(n), size=7)
    d.text(250, 44 - 18.3 - 7, 'μ 61', size=7)
    d.text(318, 44 - 11.1 - 7, 'μ 37', size=7)
    d.text(sum(chi_x) / 5, 84, 'χ · EVERY LETTER', size=7)
    d.text(sum(psi_x) / 5, 88, 'ψ · TOGETHER, WHEN THE MOTOR SAYS', size=7)
    d.text(200, 288, 'Z = P ⊕ χ ⊕ ψ′ · FIVE IMPULSES, MODULO 2', size=8)
    return d


def _tangent(c1, c2):
    """The outer common tangent from circle c1 to circle c2 (x, y, r) with both on its right,
    walking a loop clockwise on screen (y down)."""
    (x1, y1, r1), (x2, y2, r2) = c1, c2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    th = math.atan2(dy, dx)
    a = math.acos((r1 - r2) / L)
    ang = th - a
    return ((x1 + r1 * math.cos(ang), y1 + r1 * math.sin(ang)),
            (x2 + r2 * math.cos(ang), y2 + r2 * math.sin(ang)))


def heath_robinson():
    """The bedstead: two paper tape loops, the message and the chi-stream, driven round their pulleys
    past one photoelectric gate by sprocket wheels on a common shaft; the combining unit adds them
    and a counter scores each relative position."""
    d = D()
    # two bays, each loop a convex run round four pulleys (x, y, r), traversed clockwise
    bays = [
        [(40, 48, 10), (132, 40, 12), (150, 150, 10), (60, 186, 9)],
        [(176, 48, 10), (262, 36, 12), (282, 150, 10), (194, 186, 9)],
    ]
    gate_y = 208
    sprocket = [(98, gate_y + 4, 7), (234, gate_y + 4, 7)]
    loops = [b[:3] + [sprocket[i]] + b[3:] for i, b in enumerate(bays)]
    # construction: pulley centres and the loop's polygon of centres; the common shaft's line
    d.group('thin')
    for loop in loops:
        d.line(*[(x, y) for x, y, _ in loop], closed=True)
    d.line((20, gate_y + 4), (300, gate_y + 4))
    d.lines([[(x, y - r - 4), (x, y + r + 4)] for loop in loops for x, y, r in loop])
    # the bedstead's frame, upended, as the Wrens saw it
    d.group('mid')
    d.line((24, 22), (24, 238), (300, 238), (300, 22), closed=True)
    d.line((162, 22), (162, 238))
    d.line((24, 22), (300, 22))
    # the pulleys and sprockets
    d.group()
    for loop in loops:
        for x, y, r in loop:
            d.circle(x, y, r)
            d.circle(x, y, 1.5)
    for x, y, r in sprocket:
        d.lines([[(x + r * math.cos(2 * math.pi * i / 12), y + r * math.sin(2 * math.pi * i / 12)),
                  (x + (r + 2.5) * math.cos(2 * math.pi * i / 12), y + (r + 2.5) * math.sin(2 * math.pi * i / 12))]
                 for i in range(12)])
    # the tapes: outer tangents from pulley to pulley
    d.group()
    for loop in loops:
        n = len(loop)
        d.lines([list(_tangent(loop[i], loop[(i + 1) % n])) for i in range(n)])
    # the gate with its photocells, the combining unit and the counter
    d.group('mid')
    gates = []
    for loop in loops:
        a, b = _tangent(loop[3], loop[4])  # the run from the sprocket back up to the last pulley
        gates.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))
    for x, y in gates:
        d.line((x - 9, y - 6), (x + 9, y - 6), (x + 9, y + 6), (x - 9, y + 6), closed=True)
        for j in range(5):
            d.circle(x - 6 + 3 * j, y, 1)
    d.line((316, 96), (382, 96), (382, 136), (316, 136), closed=True)
    d.line((316, 170), (382, 170), (382, 210), (316, 210), closed=True)
    d.line((gates[0][0], gates[0][1] - 6), (gates[0][0], 12), (349, 12), (349, 94))
    d.line((gates[1][0], gates[1][1] - 6), (gates[1][0], 16), (345, 16), (345, 94))
    _arrow(d, 349, 95, math.pi / 2, 3)
    d.line((349, 136), (349, 168))
    _arrow(d, 349, 169, math.pi / 2, 3)
    for j in range(4):
        d.circle(330 + 13 * j, 196, 4.5)
    # labels
    d.group()
    d.text(93, 118, 'Z', size=10)
    d.text(229, 114, 'χ', size=10)
    d.text(349, 112, 'ΔZ₁⊕ΔZ₂', size=7)
    d.text(349, 124, '⊕Δχ₁⊕Δχ₂', size=7)
    d.text(349, 184, 'COUNT DOTS', size=7)
    d.text(162, 258, 'MESSAGE LOOP · KEY LOOP ONE LETTER LONGER', size=8)
    d.text(162, 272, 'SPROCKETS ON ONE SHAFT · 41 × 31 = 1,271 POSITIONS', size=7)
    return d


def colossus_d_day():
    """The Mark 2's parallel reading: the tape read once into a shift register of six characters,
    the chi pattern from a ring of thyratrons, and five processors each testing a different starting
    place at every sprocket pulse, each with its own counter."""
    d = D()
    # the tape: five channels and the sprocket row, read from right to left
    ty, pitch = 30, 9
    holes = _cams(40, 5) + _cams(40, 6) + _cams(40, 7) + _cams(40, 8) + _cams(40, 9)
    rows = [ty - 12, ty - 7, ty + 3, ty + 8, ty + 13]  # sprocket holes between channels 2 and 3
    gate_x = 44
    regs = [96 + 48 * i for i in range(6)]
    ry, pw = 88, 17
    procs = [120 + 48 * i for i in range(5)]
    py = 168
    ring = (50, 172, 26)
    # construction: the gate line, the register's centre line, the five taps
    d.group('thin')
    d.line((gate_x, ty - 20), (gate_x, ry))
    d.line((gate_x, ry), (regs[-1] + 22, ry))
    d.lines([[(regs[i], ry + 12), (procs[i], py - 14)] for i in range(5)])
    d.lines([[(regs[i + 1], ry + 12), (procs[i], py - 14)] for i in range(5)])
    # the tape
    d.group('mid')
    d.line((20, ty - 17), (384, ty - 17))
    d.line((20, ty + 18), (384, ty + 18))
    for c in range(40):
        x = 26 + pitch * c
        d.circle(x, ty - 2, 1)
        for ch in range(5):
            if holes[ch * 40 + c]:
                d.circle(x, rows[ch], 1.8)
    _arrow(d, 20, ty - 26, math.pi, 4)
    d.line((20, ty - 26), (60, ty - 26))
    # the shift register
    d.group()
    for x in regs:
        d.line((x - 20, ry - 12), (x + 20, ry - 12), (x + 20, ry + 12), (x - 20, ry + 12), closed=True)
    for a, b in zip(regs, regs[1:]):
        d.line((a + 20, ry), (b - 20, ry))
        _arrow(d, b - 20, ry, 0, 3)
    # the thyratron ring: 41 stores for chi 1
    d.group('mid')
    cx, cy, r = ring
    for i in range(41):
        a = 2 * math.pi * i / 41
        d.circle(cx + r * math.cos(a), cy + r * math.sin(a), 1.4)
    d.line((cx + r + 4, cy), (procs[0] - pw - 6, cy), (procs[0] - pw - 6, py + 22), (procs[-1], py + 22))
    d.lines([[(p, py + 22), (p, py + 14)] for p in procs])
    # the processors and counters
    d.group()
    for p in procs:
        d.line((p - pw, py - 14), (p + pw, py - 14), (p + pw, py + 14), (p - pw, py + 14), closed=True)
        _xor(d, p, py, 5)
        d.line((p, py + 14), (p, 234))
        d.line((p - pw, 234), (p + pw, 234), (p + pw, 258), (p - pw, 258), closed=True)
        for j in range(4):
            d.circle(p - 10.5 + 7 * j, 246, 2.6)
    # labels
    d.group()
    d.text(gate_x, ty + 30, 'GATE', size=7)
    for i, x in enumerate(regs):
        d.text(x, ry + 3, f'Z{"₀₁₂₃₄₅"[i]}', size=8)
    d.text(cx, cy + 3, 'χ₁', size=9)
    d.text(cx, cy + r + 14, '41 RING', size=7)
    for i, p in enumerate(procs):
        d.text(p + pw + 3, py - 16, str(i + 1), size=7, anchor='start')
    d.text(200, 280, 'ONE PASS OF THE TAPE · FIVE STARTING PLACES TESTED', size=8)
    d.text(200, 293, '5,000 LETTERS A SECOND · 200 μs A SPROCKET', size=7)
    return d


def the_silence():
    """How many Colossi existed, 1943 to 2009: one in February 1944, the Mark 2 on 1 June 1944, about
    one a month to ten by May 1945; two kept by GCHQ, broken up in 1959 and 1960; the rebuild working
    from 1996 and finished in 2007. The years of official silence are hatched."""
    d = D()
    x0, y0 = 38, 246
    X = lambda yr: x0 + (yr - 1943) * 5.2
    Y = lambda n: y0 - n * 16
    # construction: year ticks every five years, the count grid, the silence hatched
    d.group('thin')
    d.lines([[(X(yr), y0), (X(yr), y0 + 4)] for yr in range(1945, 2010, 5)])
    d.lines([[(x0 - 4, Y(n)), (x0, Y(n))] for n in (0, 2, 4, 6, 8, 10)])
    d.lines([[(x0, Y(n)), (X(2009), Y(n))] for n in (2, 10)])
    hatch = []
    left, right, top = X(1945.6), X(1975.8), Y(10.6)
    for i in range(-40, 60):
        # lines of slope 1 (rising to the right), 6 apart, clipped to the band of the silence
        xa = left + 6 * i
        pts = []
        for x in (xa, xa + (y0 - top)):
            pts.append((x, y0 - (x - xa)))
        (xs, ys), (xe, ye) = pts
        if xs < left:
            ys -= left - xs
            xs = left
        if xe > right:
            ye += xe - right
            xe = right
        if xs < xe:
            hatch.append([(xs, ys), (xe, ye)])
    d.lines(hatch)
    # the axes
    d.group('mid')
    d.line((x0, Y(11)), (x0, y0), (X(2009), y0))
    # the count of machines: a step line
    d.group()
    pts = [(X(1943.9), Y(0)), (X(1944.1), Y(0)), (X(1944.1), Y(1)), (X(1944.42), Y(1)), (X(1944.42), Y(2))]
    months = [1944.42 + (1945.35 - 1944.42) * i / 8 for i in range(1, 9)]
    n = 2
    for t in months:
        pts += [(X(t), Y(n)), (X(t), Y(n + 1))]
        n += 1
    pts += [(X(1945.6), Y(10)), (X(1945.6), Y(2)), (X(1959.5), Y(2)), (X(1959.5), Y(1)),
            (X(1960.5), Y(1)), (X(1960.5), Y(0)), (X(1996.4), Y(0))]
    d.line(*pts)
    d.line((X(1996.4), Y(0)), (X(1996.4), Y(1)), (X(2009), Y(1)))
    # the markers: the photographs of 1975, the report of 2000, the challenge of 2007
    d.group('mid')
    for yr in (1975.8, 2000.8, 2007.9):
        d.line((X(yr), y0), (X(yr), Y(5)))
        d.circle(X(yr), Y(5) - 3, 2.5)
    # labels
    d.group()
    for yr in (1945, 1960, 1975, 1990, 2005):
        d.text(X(yr), y0 + 14, str(yr), size=7)
    for nn in (0, 2, 10):
        d.text(x0 - 7, Y(nn) + 3, str(nn), size=7, anchor='end')
    d.text(X(1960.6), Y(7.2), 'SECRET', size=8)
    d.text(X(1975.8), Y(5) - 10, 'PHOTOS', size=6)
    d.text(X(2000.8), Y(5) - 10, 'REPORT', size=6)
    d.text(X(2007.9) - 2, Y(6.2) - 10, 'CHALLENGE', size=6)
    d.text(X(1996.4) + 3, Y(1) - 5, 'REBUILD', size=6, anchor='start')
    d.text(200, 290, 'COLOSSI IN EXISTENCE, 1943–2009', size=8)
    return d


PLATES = {'bombe': bombe, 'tunny': tunny, 'heath-robinson': heath_robinson,
          'colossus-d-day': colossus_d_day, 'the-silence': the_silence}
