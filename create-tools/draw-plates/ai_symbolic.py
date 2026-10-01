"""ai plates, segment "The symbolic age" (sprint 006). See plates_for.py."""
import heapq
import math
import random

from plates import D


def dartmouth():
    """The summer of 1956 as a Gantt chart: the eleven names McCarthy sent the Rockefeller
    Foundation on 26 May 1956, planned for the full period, four weeks or two weeks, against
    the eight weeks Solomonoff's notes record (about 18 June to 17 August)."""
    d = D()
    x0, wk, weeks = 96, 34, 8  # eight weeks, 34 units each: 96..368
    y0, row = 58, 17
    plan = [8] * 6 + [4] * 3 + [2] * 2  # full period, four weeks, first two weeks
    xs = [x0 + i * wk for i in range(weeks + 1)]
    ys = [y0 + i * row for i in range(len(plan) + 1)]
    # construction: the week grid and the row rules
    d.group('thin')
    d.lines([[(x, y0 - 16), (x, ys[-1] + 6)] for x in xs])
    d.lines([[(x0 - 8, y), (xs[-1], y)] for y in ys])
    # the object: the frame of the summer
    d.group()
    d.line((x0, y0), (xs[-1], y0), (xs[-1], ys[-1]), (x0, ys[-1]), closed=True)
    # each planned attendance as a bar
    d.group('mid')
    for i, w in enumerate(plan):
        y = ys[i] + row / 2
        d.line((x0 + 4, y - 4), (x0 + w * wk - 4, y - 4), (x0 + w * wk - 4, y + 4), (x0 + 4, y + 4), closed=True)
    # the dimension line below: the eight weeks Solomonoff's notes record
    yd = ys[-1] + 26
    d.group()
    d.line((x0, yd), (xs[-1], yd))
    d.lines([[(x0, yd - 6), (x0, yd + 6)], [(xs[-1], yd - 6), (xs[-1], yd + 6)]])
    d.lines([[(x0 + 8, yd - 4), (x0, yd), (x0 + 8, yd + 4)], [(xs[-1] - 8, yd - 4), (xs[-1], yd), (xs[-1] - 8, yd + 4)]])
    # the brace grouping the rows: six, three, two
    d.group('mid')
    for a, b in ((0, 6), (6, 9), (9, 11)):
        d.line((x0 - 10, ys[a] + 3), (x0 - 14, ys[a] + 3), (x0 - 14, ys[b] - 3), (x0 - 10, ys[b] - 3))
    d.group()
    for i in range(weeks):
        d.text(x0 + (i + .5) * wk, y0 - 6, str(i + 1), size=7)
    d.text(x0 - 20, (ys[0] + ys[6]) / 2 + 3, 'FULL', size=7, anchor='end')
    d.text(x0 - 20, (ys[6] + ys[9]) / 2 + 3, '4 WK', size=7, anchor='end')
    d.text(x0 - 20, (ys[9] + ys[11]) / 2 + 3, '2 WK', size=7, anchor='end')
    d.text((x0 + xs[-1]) / 2, yd + 16, 'JUNE 18 · HANOVER NH · AUGUST 17', size=8)
    d.text((x0 + xs[-1]) / 2, 22, 'SUMMER RESEARCH PROJECT · 1956', size=8)
    return d


def logic_theorist():
    """Proof as search: a tree grown backward from the theorem. Every node has three possible
    moves; the heuristic expands only the promising ones and cuts the rest, and one path runs
    down to the axioms."""
    d = D()
    top, dy = 44, 50
    # the expanded nodes, as paths of child indices from the root; every expanded node shows
    # all three children, and the proof runs 1, 0, 2, 1
    expanded = sorted({(), (0,), (1,), (2,), (1, 0), (1, 2), (1, 0, 2), (1, 0, 0)})  # sorted: a set's order varies by run
    proof = (1, 0, 2, 1)
    nodes = {()}
    for e in expanded:
        nodes |= {e + (k,) for k in range(3)}
    # a tidy layout: leaves of the visible tree take equal slots, parents sit over their children
    leaves = sorted(n for n in nodes if n not in expanded)
    slot = 336 / len(leaves)
    xpos = {n: 32 + (i + .5) * slot for i, n in enumerate(leaves)}
    for n in sorted(expanded, key=len, reverse=True):
        xpos[n] = sum(xpos[n + (k,)] for k in range(3)) / 3
    P = lambda n: (xpos[n], top + len(n) * dy)
    depth = max(len(n) for n in nodes)
    # construction: the level rules and the root's axis
    d.group('thin')
    d.lines([[(22, top + lv * dy), (378, top + lv * dy)] for lv in range(depth + 1)])
    d.line((xpos[()], top - 24), (xpos[()], top + depth * dy + 10))
    # the tree as searched
    d.group('mid')
    d.lines([[P(n), P(n + (k,))] for n in expanded for k in range(3)])
    for n in sorted(expanded):
        d.circle(*P(n), 4)
    # the cuts the heuristic made: a bar across each leaf that is not on the proof
    d.group()
    for n in leaves:
        if n != proof[:len(n)]:
            x, y = P(n)
            d.line((x - 5, y + 5), (x + 5, y + 5))
    # the proof: one path from theorem to axioms, at full weight
    d.group()
    d.line(*[P(proof[:i]) for i in range(len(proof) + 1)])
    d.circle(*P(()), 9)
    x, y = P(proof)
    d.line((x - 7, y - 7), (x + 7, y - 7), (x + 7, y + 7), (x - 7, y + 7), closed=True)
    d.group()
    d.text(xpos[()] + 16, top - 12, '*2·85', size=8, anchor='start')
    d.text(x, y + 24, 'AXIOMS', size=8)
    d.text(378, top + 3 * dy - 6, 'SUBPROBLEMS', size=7, anchor='end')
    return d


def perceptron():
    """The Mark I's three layers: a 20 x 20 retina of photocells, random fixed wiring to the
    association units, and adjustable weights (motor-driven potentiometers) into the response units."""
    d = D()
    rnd = random.Random(1958)
    gx, gy, cell, n = 26, 60, 9, 20  # retina: 20 x 20 at 9 units, 26..206
    na, ax = 12, 272
    ays = [44 + i * 212 / (na - 1) for i in range(na)]
    nr, rx = 3, 360
    rys = [110 + i * 40 for i in range(nr)]
    # construction: the retina's grid lines
    d.group('thin')
    d.lines([[(gx + i * cell, gy), (gx + i * cell, gy + n * cell)] for i in range(n + 1)] +
            [[(gx, gy + j * cell), (gx + n * cell, gy + j * cell)] for j in range(n + 1)])
    # random fixed connections from photocells to association units (a table of random numbers)
    d.group('thin')
    segs = []
    for k, ay in enumerate(ays):
        for _ in range(3):
            i, j = rnd.randrange(n), rnd.randrange(n)
            segs.append([(gx + (i + .5) * cell, gy + (j + .5) * cell), (ax - 6, ay)])
    d.lines(segs)
    # the object: retina frame, a figure projected on it, the units
    d.group()
    d.line((gx, gy), (gx + n * cell, gy), (gx + n * cell, gy + n * cell), (gx, gy + n * cell), closed=True)
    for ay in ays:
        d.circle(ax, ay, 6)
    for ry in rys:
        d.circle(rx, ry, 10)
    # the stimulus: a letter E, as the manual's experiments used, lit on the retina
    d.group('mid')
    e = [(5, 4), (5, 16)] + [(c, 4) for c in range(6, 14)] + [(c, 10) for c in range(6, 12)] + [(c, 15) for c in range(6, 14)]
    e += [(5, r) for r in range(5, 16)]
    for i, j in set(e):
        x, y = gx + i * cell, gy + j * cell
        d.line((x + 1.5, y + 1.5), (x + cell - 1.5, y + 1.5), (x + cell - 1.5, y + cell - 1.5), (x + 1.5, y + cell - 1.5), closed=True)
    # adjustable weights: every association unit to every response unit, each with a potentiometer tick
    d.group('mid')
    segs, ticks = [], []
    for ay in ays:
        for ry in rys:
            segs.append([(ax + 6, ay), (rx - 10, ry)])
    d.lines(segs)
    # thresholds: a step drawn inside each response unit
    d.group()
    for ry in rys:
        d.line((rx - 6, ry + 4), (rx, ry + 4), (rx, ry - 4), (rx + 6, ry - 4))
        d.line((rx + 10, ry), (rx + 26, ry))
        d.line((rx + 21, ry - 4), (rx + 26, ry), (rx + 21, ry + 4))
    d.group()
    d.text(gx + n * cell / 2, gy + n * cell + 18, 'S · 20 × 20 PHOTOCELLS', size=8)
    d.text(ax, 28, 'A', size=9)
    d.text(rx, 90, 'R', size=9)
    return d


def eliza():
    """One ELIZA transformation, Weizenbaum's own example: the template (0 YOU 0 ME) cuts the input
    into four numbered parts, and the reassembly rule (WHAT MAKES YOU THINK I 3 YOU) throws part 1
    away, swaps the pronouns and puts part 3 back into a stock sentence."""
    d = D()
    ch = 6.4  # width of one 8-unit monospace character, with letter-spacing
    parts = ['IT SEEMS THAT', 'YOU', 'HATE', 'ME']
    rule = ['WHAT MAKES YOU THINK I', '3', 'YOU']
    w_in = [len(s) * ch + 14 for s in parts]
    w_out = [len(s) * ch + 14 for s in rule]
    gap = 10
    y_in, y_out, h = 86, 196, 28

    def row(ws):
        x = 200 - (sum(ws) + gap * (len(ws) - 1)) / 2
        xs = []
        for w in ws:
            xs.append(x)
            x += w + gap
        return xs

    xs_in, xs_out = row(w_in), row(w_out)
    mid = (y_in + h + y_out) / 2
    # construction: the mirror axis between what was said and what is said back, and the cuts
    d.group('thin')
    d.line((24, mid), (376, mid))
    d.lines([[(x - gap / 2, y_in - 26), (x - gap / 2, y_in + h + 8)] for x in xs_in[1:]])
    d.lines([[(x - gap / 2, y_out - 8), (x - gap / 2, y_out + h + 8)] for x in xs_out[1:]])
    # the object: the four parts of the input and the three of the reply
    d.group()
    for a, w in zip(xs_in, w_in):
        d.line((a, y_in), (a + w, y_in), (a + w, y_in + h), (a, y_in + h), closed=True)
    for a, w in zip(xs_out, w_out):
        d.line((a, y_out), (a + w, y_out), (a + w, y_out + h), (a, y_out + h), closed=True)
    # part 1 is thrown away; parts 2 and 4 are the keywords, swapped into the reply
    d.group('mid')
    a, w = xs_in[0], w_in[0]
    d.line((a + 4, y_in + h - 4), (a + w - 4, y_in + 4))
    for k in (1, 3):
        d.line((xs_in[k] + 3, y_in + 3), (xs_in[k] + w_in[k] - 3, y_in + 3),
               (xs_in[k] + w_in[k] - 3, y_in + h - 3), (xs_in[k] + 3, y_in + h - 3), closed=True)
    # the reassembly: part 3 carried across the mirror into the slot
    d.group()
    sx, tx = xs_in[2] + w_in[2] / 2, xs_out[1] + w_out[1] / 2
    d.curve(f'M{sx:.1f} {y_in + h} C{sx:.1f} {mid} {tx:.1f} {mid} {tx:.1f} {y_out - 2}')
    d.line((tx - 4, y_out - 9), (tx, y_out - 2), (tx + 4, y_out - 9))
    # the part numbers over the cut
    d.group('mid')
    for a, w in zip(xs_in, w_in):
        d.circle(a + w / 2, y_in - 14, 7)
    d.group()
    for k, (a, w) in enumerate(zip(xs_in, w_in)):
        d.text(a + w / 2, y_in - 11, str(k + 1), size=7)
        d.text(a + w / 2, y_in + h / 2 + 3, parts[k], size=8)
    for a, w, s in zip(xs_out, w_out, rule):
        d.text(a + w / 2, y_out + h / 2 + 3, s, size=8)
    d.text(200, 42, '(0 YOU 0 ME)', size=8)
    d.text(200, y_out + h + 24, 'WHAT MAKES YOU THINK I HATE YOU', size=8)
    return d


def _astar(free, start, goal):
    """A* on a 4-connected grid with the Manhattan heuristic. Returns (path, closed set in order)."""
    h = lambda p: abs(p[0] - goal[0]) + abs(p[1] - goal[1])
    openq = [(h(start), 0, start)]
    g = {start: 0}
    came = {}
    closed = []
    seen = set()
    while openq:
        _, gc, cur = heapq.heappop(openq)
        if cur in seen:
            continue
        seen.add(cur)
        closed.append(cur)
        if cur == goal:
            break
        x, y = cur
        for nb in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if nb in free and gc + 1 < g.get(nb, 1e9):
                g[nb] = gc + 1
                came[nb] = cur
                heapq.heappush(openq, (gc + 1 + h(nb), gc + 1, nb))
    path = [goal]
    while path[-1] != start:
        path.append(came[path[-1]])
    return path[::-1], closed


def shakey():
    """Shakey's world in plan: rooms joined by doorways, a block in the way, and the path A* finds,
    with the cells it had to look at on the way."""
    d = D()
    cols, rows, c = 22, 14, 15
    x0, y0 = 35, 32
    # walls on the grid: a vertical wall at column 8 with a door at rows 10-11,
    # a vertical wall at column 15 with a door at rows 2-3, and a block in the right room
    wall = set()
    for r in range(rows):
        if r not in (10, 11):
            wall.add((8, r))
        if r not in (2, 3):
            wall.add((15, r))
    block = {(x, y) for x in (11, 12) for y in (5, 6, 7)}
    free = {(x, y) for x in range(cols) for y in range(rows)} - wall - block
    start, goal = (2, 3), (19, 10)
    path, closed = _astar(free, start, goal)
    ctr = lambda p: (x0 + (p[0] + .5) * c, y0 + (p[1] + .5) * c)
    # construction: the grid model
    d.group('thin')
    d.lines([[(x0 + i * c, y0), (x0 + i * c, y0 + rows * c)] for i in range(cols + 1)] +
            [[(x0, y0 + j * c), (x0 + cols * c, y0 + j * c)] for j in range(rows + 1)])
    # the object: the outer walls, the two partition walls with their doorways, the block
    d.group()
    d.line((x0, y0), (x0 + cols * c, y0), (x0 + cols * c, y0 + rows * c), (x0, y0 + rows * c), closed=True)
    for wx, door in ((8, (10, 12)), (15, (2, 4))):
        xl, xr = x0 + wx * c, x0 + (wx + 1) * c
        for a, b in ((0, door[0]), (door[1], rows)):
            d.line((xl, y0 + a * c), (xr, y0 + a * c), (xr, y0 + b * c), (xl, y0 + b * c), closed=True)
    bx, by = x0 + 11 * c, y0 + 5 * c
    d.line((bx, by), (bx + 2 * c, by), (bx + 2 * c, by + 3 * c), (bx, by + 3 * c), closed=True)
    d.line((bx, by), (bx + 2 * c, by + 3 * c))
    d.line((bx + 2 * c, by), (bx, by + 3 * c))
    # the cells A* closed on its way, as small dots
    d.group('thin')
    for p in closed:
        if p not in path:
            x, y = ctr(p)
            d.circle(x, y, 1.4)
    # the path
    d.group()
    d.line(*[ctr(p) for p in path])
    sx, sy = ctr(start)
    d.circle(sx, sy, 6)
    gx, gy = ctr(goal)
    d.lines([[(gx - 6, gy - 6), (gx + 6, gy + 6)], [(gx - 6, gy + 6), (gx + 6, gy - 6)]])
    d.circle(gx, gy, 8)
    d.group()
    d.text(x0, y0 + rows * c + 16, f'f(n) = g(n) + h(n) · {len(closed)} CELLS CLOSED · PATH {len(path) - 1}', size=8, anchor='start')
    d.text(sx, sy - 12, 'START', size=7)
    d.text(gx, gy + 20, 'GOAL', size=7)
    return d


PLATES = {
    'dartmouth': dartmouth,
    'logic-theorist': logic_theorist,
    'perceptron': perceptron,
    'eliza': eliza,
    'shakey': shakey,
}
