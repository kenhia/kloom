"""ai plates, trail "Machines at play" (sprint 006). See ai.py."""
import math

from plates import D


def gear(d, cx, cy, r, teeth, depth=3):
    """A spur gear: a toothed rim as one closed polyline."""
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4)
        rr = r + (depth if i % 4 in (1, 2) else 0)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.line(*pts, closed=True)


def mechanical_turk():
    """The Turk's cabinet cut away: clockwork for show on the left, the hidden
    player on his sliding seat on the right, magnets under the board and the
    pantograph that works the figure's arm."""
    d = D()
    x0, x1, y0, y1 = 70, 300, 128, 262  # the cabinet, 3.5 ft by 2.5 ft at ~66 px/ft
    bx0, bx1 = 176, 272  # the board on the lid: eight squares of 12
    # construction: dimension lines, and the magnet strings under the squares
    d.group('thin')
    d.line((x0, y1 + 14), (x1, y1 + 14))
    d.lines([[(x, y1 + 9), (x, y1 + 19)] for x in (x0, x1)])
    d.line((x1 + 14, y0), (x1 + 14, y1))
    d.lines([[(x1 + 9, y), (x1 + 19, y)] for y in (y0, y1)])
    d.lines([[(bx0 + 6 + 12 * i, y0), (bx0 + 6 + 12 * i, y0 + 16 + 4 * (i % 2))] for i in range(8)])
    # the object: cabinet, partition, lid and board, and the figure above it
    d.group()
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)
    d.line((x0 + 78, y0), (x0 + 78, y1))
    d.line((x0 - 6, y0), (x1 + 6, y0))
    d.line((bx0, y0 - 3), (bx1, y0 - 3))
    fx = 150  # the figure's axis
    d.circle(fx, 44, 11)
    d.ellipse(fx, 33, 15, 6)  # turban: the wound band and its crown
    d.curve(f'M{fx - 11} 30 C{fx - 9} 14 {fx + 9} 14 {fx + 11} 30')
    d.line((fx - 8, 55), (fx - 30, 66), (fx - 26, y0))
    d.line((fx + 8, 55), (fx + 30, 66), (fx + 26, y0))
    d.line((fx + 30, 66), (fx + 58, 96), (fx + 86, y0 - 8))  # the working arm, reaching to the board
    d.line((fx - 30, 66), (fx - 52, 100), (fx - 70, 92))  # the pipe arm
    d.line((fx - 70, 92), (fx - 96, 72))
    # clockwork shown to the audience, a third of the way back
    d.group('mid')
    gear(d, x0 + 30, y0 + 40, 17, 12)
    gear(d, x0 + 54, y0 + 70, 11, 8)
    gear(d, x0 + 28, y0 + 96, 13, 10)
    d.circle(x0 + 30, y0 + 40, 3)
    d.circle(x0 + 54, y0 + 70, 2)
    d.circle(x0 + 28, y0 + 96, 3)
    d.lines([[(x0 + 8, y1 - 18), (x0 + 70, y1 - 18)], [(x0 + 8, y1 - 10), (x0 + 70, y1 - 10)]])
    # the magnets hanging under the squares
    d.lines([[(bx0 + 6 + 12 * i - 2, y0 + 18 + 4 * (i % 2)), (bx0 + 6 + 12 * i + 2, y0 + 18 + 4 * (i % 2))]
             for i in range(8)])
    # the hidden player on his sliding seat, the peg board and the pantograph
    d.group()
    px, py = 216, 196
    d.circle(px, py - 22, 8)
    d.line((px, py - 14), (px + 2, py + 14), (px + 22, py + 16), (px + 24, y1 - 6))
    d.line((px, py - 6), (px - 20, py + 2), (px - 34, py - 2))
    d.line((px - 4, py + 18), (px + 40, py + 18))  # sliding seat
    d.line((px - 70, py + 2), (px - 30, py + 2))  # peg board
    d.group('mid')
    # pantograph: a parallelogram from the peg board up to the figure's arm
    a, b, c = (px - 34, py - 2), (px - 14, y0 + 30), (fx + 44, y0 + 14)
    e = (a[0] + c[0] - b[0], a[1] + c[1] - b[1])
    d.line(a, b, c, e, closed=True)
    d.line(c, (fx + 50, 104))
    # the candle and its vent to the turban
    d.group('thin')
    d.line((px + 44, y1 - 20), (px + 44, y1 - 8))
    d.line((px + 44, y1 - 24), (px + 44, y0 + 8), (fx + 10, y0 + 8), (fx + 10, 60), (fx + 4, 20))
    d.group()
    d.text(x0 + 39, y0 + 12, 'SHOW', size=7)
    d.text(px + 4, y1 - 26, 'OPERATOR', size=7, anchor='end')
    d.text((x0 + x1) / 2, y1 + 28, '3½ FT', size=7)
    d.text(x1 + 30, (y0 + y1) / 2, '2½', size=7)
    return d


def shannon_chess():
    """Shannon's figure 2: three White moves, three Black replies to each, the
    minimum taken over each fan and the maximum over those; behind it, faintly,
    the thirty-odd moves a real position offers."""
    d = D()
    rx, ry = 50, 150
    mx, lx = 190, 320
    # construction: the fan of about thirty legal moves, and the ply lines
    d.group('thin')
    d.lines([[(rx, ry), (mx + 20, ry + (i - 14.5) * 8.6)] for i in range(30)])
    d.lines([[(x, 24), (x, 276)] for x in (rx, mx, lx)])
    white = [ry - 80, ry, ry + 80]
    mins = ['+1', '−7', '−6']
    # the object: White's three moves (solid) and Black's nine replies
    d.group()
    d.lines([[(rx, ry), (mx, y)] for y in white])
    d.circle(rx, ry, 5)
    for y in white:
        d.circle(mx, y, 4)
    d.group('mid')
    leaves = []
    for y in white:
        for j in (-1, 0, 1):
            ly = y + j * 24
            leaves.append((lx, ly))
            # Black's replies, as short dashes (Shannon drew them dashed)
            n = 7
            segs = []
            for k in range(n):
                t0, t1 = k / n, (k + 0.55) / n
                segs.append([(mx + (lx - mx) * t0, y + (ly - y) * t0), (mx + (lx - mx) * t1, y + (ly - y) * t1)])
            d.lines(segs)
    for x, y in leaves:
        d.circle(x, y, 2.5)
    # the chosen line: White's best move and Black's best reply
    d.group()
    d.line((rx, ry), (mx, white[0]), (lx, white[0] + 24))
    d.circle(lx, white[0] + 24, 5)
    d.group()
    for y, m in zip(white, mins):
        d.text(mx, y - 9, m, size=9)
    d.text(rx, ry - 12, '+1', size=9)
    d.text(rx, 290, 'MAX', size=8)
    d.text(mx, 290, 'MIN', size=8)
    d.text(lx, 290, 'f(P)', size=8)
    return d


def samuel_checkers():
    """Samuel's board as the IBM 704 held it (one bit per playing square, 32 of
    a 36-bit word), and his learning signal: the score of a position now set
    against the score backed up from the look-ahead. The difference, delta,
    retunes the sixteen active terms of the scoring polynomial."""
    d = D()
    bx, by, s = 24, 26, 15  # the board: 8 squares of 15
    wx, wy, ww = 24, 190, 5  # the word: 36 cells of 5
    dark = [(r, c) for r in range(8) for c in range(8) if (r + c) % 2 == 1]
    # construction: the board grid, and the leads from the near row to its bits
    d.group('thin')
    d.lines([[(bx + i * s, by), (bx + i * s, by + 8 * s)] for i in range(9)])
    d.lines([[(bx, by + i * s), (bx + 8 * s, by + i * s)] for i in range(9)])
    near = [k for k, (r, c) in enumerate(dark) if r == 7]
    d.lines([[(bx + dark[k][1] * s + s / 2, by + 8 * s), (wx + k * ww + ww / 2, wy)] for k in near])
    # the object: the board's edge and the machine word
    d.group()
    d.line((bx, by), (bx + 8 * s, by), (bx + 8 * s, by + 8 * s), (bx, by + 8 * s), closed=True)
    d.line((wx, wy), (wx + 36 * ww, wy), (wx + 36 * ww, wy + 12), (wx, wy + 12), closed=True)
    d.group('mid')
    hatch = []
    for r, c in dark:
        x, y = bx + c * s, by + r * s
        hatch += [[(x, y + s * f), (x + s * f, y)] for f in (0.5, 1)] + [[(x + s * 0.5, y + s), (x + s, y + s * 0.5)]]
    d.lines(hatch)
    d.lines([[(wx + i * ww, wy), (wx + i * ww, wy + 12)] for i in range(1, 36)])
    d.lines([[(wx + i * ww, wy + 12), (wx + (i + 1) * ww, wy)] for i in range(32, 36)])  # four spare bits
    d.group()
    for r, c in [(5, 0), (5, 2), (6, 1), (7, 4), (2, 3), (0, 5), (1, 6), (3, 6)]:
        d.circle(bx + c * s + s / 2, by + r * s + s / 2, 5)
    # the look-ahead tree: the position now, three ply down
    tx, ty = 280, 36
    l1 = [tx - 66, tx, tx + 66]
    l2 = [x + o for x in l1 for o in (-22, 0, 22)]
    ys = [ty, ty + 56, ty + 112]
    d.group('thin')
    d.lines([[(tx, ty), (x, ys[1])] for x in l1])
    d.lines([[(l1[i // 3], ys[1]), (x, ys[2])] for i, x in enumerate(l2)])
    d.group()
    d.circle(tx, ty, 6)
    for x in l1:
        d.circle(x, ys[1], 4)
    for x in l2:
        d.circle(x, ys[2], 3)
    # delta: the backed-up value carried up the side to the static score, and down to the terms
    ax = tx + 104
    box = (tx - 70, 214, tx + 70, 240)
    d.group('mid')
    d.line((l2[-1] + 6, ys[2]), (ax, ys[2]), (ax, ty), (tx + 10, ty))
    d.curve(f'M{tx + 16} {ty - 4} L{tx + 10} {ty} L{tx + 16} {ty + 4}')
    d.line((ax, ys[2]), (ax, (box[1] + box[3]) / 2), (box[2] + 6, (box[1] + box[3]) / 2))
    d.curve(f'M{box[2] + 12} {(box[1] + box[3]) / 2 - 4} L{box[2] + 6} {(box[1] + box[3]) / 2} '
            f'L{box[2] + 12} {(box[1] + box[3]) / 2 + 4}')
    d.group()
    d.line((box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3]), closed=True)
    d.lines([[(box[0] + (box[2] - box[0]) * i / 16, box[1]), (box[0] + (box[2] - box[0]) * i / 16, box[3])]
             for i in range(1, 16)])
    d.group()
    d.text(ax + 8, (ty + ys[2]) / 2 + 4, 'δ', size=12, anchor='start')
    d.text(wx + 18 * ww, wy + 26, '36-BIT WORD · 32 SQUARES', size=7)
    d.text(tx, box[3] + 16, '16 ACTIVE TERMS', size=7)
    d.text(l2[0] - 10, ys[2] + 3, '3 PLY', size=7, anchor='end')
    return d


def td_gammon():
    """TD-Gammon's network (198 inputs, 80 hidden units, 4 outputs) above the
    course of one self-play game: each prediction pulled toward the next, and
    the last toward the result."""
    d = D()
    cols = [(60, 12), (150, 8), (240, 4)]
    top, bot = 20, 150

    def ys(n):
        return [top + (bot - top) * (i + 0.5) / n for i in range(n)]

    # construction: every connection, input to hidden to output
    d.group('thin')
    for (xa, na), (xb, nb) in zip(cols, cols[1:]):
        d.lines([[(xa, ya), (xb, yb)] for ya in ys(na) for yb in ys(nb)])
    # the object: the three layers
    d.group()
    for x, n in cols:
        for y in ys(n):
            d.circle(x, y, 4 if n > 4 else 5)
    d.line((cols[0][0] - 12, top), (cols[0][0] - 12, bot))
    # the game: predictions Y_t along the time axis, drifting toward a win
    gx0, gx1, gy = 40, 330, 280
    n = 14
    vals = [0.5 + 0.34 * math.sin(i / (n - 1) * math.pi * 0.9) * (i / (n - 1)) + 0.07 * math.sin(i * 1.7)
            for i in range(n)]
    pts = [(gx0 + (gx1 - gx0) * i / (n - 1), gy - 90 * v) for i, v in enumerate(vals)]
    d.group('thin')
    d.line((gx0, gy), (gx1 + 30, gy))
    d.line((gx0, gy - 90), (gx1 + 30, gy - 90))
    d.lines([[(x, gy), (x, gy + 4)] for x, _ in pts])
    d.group()
    d.line(*pts)
    for x, y in pts:
        d.circle(x, y, 2.5)
    zx, zy = gx1 + 30, gy - 90
    d.circle(zx, zy, 5)
    # the TD error: each estimate pulled toward the one after it, and back into the weights
    d.group('mid')
    for (xa, ya), (xb, yb) in zip(pts[8:], pts[9:]):
        d.curve(f'M{xa} {ya - 6} Q{(xa + xb) / 2} {min(ya, yb) - 22} {xb} {yb - 6}')
    d.curve(f'M{pts[-1][0]} {pts[-1][1] - 6} Q{(pts[-1][0] + zx) / 2} {zy - 20} {zx} {zy - 6}')
    ox, oy = cols[2][0] + 10, ys(4)[3]
    d.curve(f'M{330} {158} C{330} {120} {300} {oy} {ox} {oy}')
    d.curve(f'M{ox + 7} {oy - 4} L{ox} {oy} L{ox + 7} {oy + 4}')
    d.group()
    d.text(cols[0][0], bot + 16, '198', size=8)
    d.text(cols[1][0], bot + 16, '80', size=8)
    d.text(cols[2][0], bot + 16, '4', size=8)
    d.text(zx + 12, zy + 3, 'z', size=10, anchor='start')
    d.text(gx0 - 4, gy - 88, '1', size=7, anchor='end')
    d.text(gx0 - 4, gy + 2, '0', size=7, anchor='end')
    d.text(330, 172, 'Yt+1 − Yt', size=8)
    return d


def chinook():
    """The shape of the checkers proof: the space of positions by the number
    of pieces on the board (schematic), a forward proof tree from the start,
    and the endgame databases of every position with ten pieces or fewer,
    worked backward from the end."""
    d = D()
    cx, ytop, ybot = 170, 28, 278

    def y(p):  # pieces: 24 at the top, 2 at the bottom
        return ytop + (ybot - ytop) * (24 - p) / 22

    def half(p):  # a schematic width, widest in the middle game
        t = (24 - p) / 22
        return 10 + 140 * math.sin(math.pi * t) ** 0.7 * (1 - 0.35 * t)

    # construction: one rung for every second piece count
    d.group('thin')
    d.lines([[(cx - half(p), y(p)), (cx + half(p), y(p))] for p in range(24, 1, -2)])
    # the object: the envelope of the search space
    d.group()
    left = [(cx - half(p), y(p)) for p in range(24, 1, -1)]
    right = [(cx + half(p), y(p)) for p in range(2, 25)]
    d.line(*(left + right), closed=True)
    # the databases: hatched below the ten-piece line
    d.group('mid')
    y10 = y(10)
    d.line((cx - half(10), y10), (cx + half(10), y10))
    hatch = []
    for k in range(-40, 40):
        x0 = cx + k * 8
        seg = []
        for j in range(60):
            yy = y10 + j * (ybot - y10) / 59
            xx = x0 + (yy - y10) * 0.6
            p = 24 - (yy - ytop) / (ybot - ytop) * 22
            if abs(xx - cx) <= half(max(2, min(24, p))) - 1:
                seg.append((xx, yy))
            elif seg:
                break
        if len(seg) > 1:
            hatch.append([seg[0], seg[-1]])
    d.lines(hatch)
    # the forward proof tree: every reply to a move, one move to each reply
    d.group()
    offs = [44, 24, 13, 8, 5]
    nodes = [(cx, y(24))]
    segs = []
    for lvl, o in enumerate(offs):
        yy = y(24 - (lvl + 1) * 2.8)
        nxt = []
        for i, (px, py) in enumerate(nodes):
            kids = (-o, o) if lvl % 2 == 0 else (o * (1 if i % 2 else -1) * 0.3,)
            for k in kids:
                nxt.append((px + k, yy))
                segs.append([(px, py), (px + k, yy)])
        nodes = nxt
    d.lines(segs)
    for px, py in nodes:
        d.circle(px, py, 2)
    # the proof's leaves reach down into the databases
    d.group('mid')
    d.lines([[(px, py + 2), (px, y10)] for px, py in nodes])
    d.group()
    d.text(cx, y(24) - 8, 'START · 24 PIECES', size=7)
    d.text(cx + half(10) + 6, y10 + 3, '10 PIECES', size=7, anchor='start')
    d.text(cx + half(5) + 10, y(5), 'ENDGAME', size=7, anchor='start')
    d.text(cx + half(5) + 10, y(5) + 10, 'DATABASES', size=7, anchor='start')
    return d


def alphazero():
    """AlphaZero's loop: a search that goes deep on a few lines, guided by one
    network's move probabilities p and value v; the network trained on the
    games the search plays against itself. Behind it, faintly, the
    full-width tree a brute-force search visits."""
    d = D()
    rx, ry = 34, 150
    # construction: the full-width tree
    d.group('thin')
    full = []
    for i in range(7):
        y1 = ry + (i - 3) * 38
        full.append([(rx, ry), (rx + 46, y1)])
        for j in range(5):
            full.append([(rx + 46, y1), (rx + 92, y1 + (j - 2) * 7)])
    d.lines(full)
    # the object: a selective search, deep along the lines the network favours
    d.group()
    path = [(rx, ry)]
    x, y = rx, ry
    for dy in [-38, 12, -6, 10, -4, 6, -3]:
        x, y = x + 28, y + dy
        path.append((x, y))
    d.line(*path)
    alt = [(rx, ry), (rx + 28, ry + 38), (rx + 56, ry + 30), (rx + 84, ry + 44), (rx + 112, ry + 38)]
    d.line(*alt)
    for px, py in path + alt[1:]:
        d.circle(px, py, 3)
    d.group('mid')
    side = [[(px, py), (px + 18, py + (12 if i % 2 else -12))] for i, (px, py) in enumerate(path[:-1])]
    side.append([alt[2], (alt[2][0] + 18, alt[2][1] + 14)])
    d.lines(side)
    # the network in the middle of its loop
    lx, ly, lr = 318, 150, 58
    d.group('thin')
    d.circle(lx, ly, lr)
    d.line((lx, ly - lr), (lx, ly - 16))
    d.line((lx, ly + 16), (lx, ly + lr))
    d.group()
    d.line((lx - 22, ly - 16), (lx + 22, ly - 16), (lx + 22, ly + 16), (lx - 22, ly + 16), closed=True)
    d.circle(lx, ly - lr, 6)
    d.circle(lx, ly + lr, 6)
    d.group('mid')
    for a in (30, 210):  # arrowheads on the loop, clockwise
        t = math.radians(a)
        ax, ay = lx + lr * math.cos(t), ly + lr * math.sin(t)
        tx, ty = -math.sin(t), math.cos(t)
        nx, ny = math.cos(t), math.sin(t)
        d.line((ax - 6 * tx + 4 * nx, ay - 6 * ty + 4 * ny), (ax, ay), (ax - 6 * tx - 4 * nx, ay - 6 * ty - 4 * ny))
    d.curve(f'M{x + 6} {y} C{x + 30} {y} {lx - 60} {ly} {lx - 22} {ly}')
    d.group()
    d.text(lx, ly + 3, 'p, v', size=9)
    d.text(lx, ly - lr - 12, 'TRAIN', size=7)
    d.text(lx, ly + lr + 18, 'SELF-PLAY', size=7)
    return d


def pluribus():
    """Poker as a game of hidden information: a chance node deals, the player
    to act cannot tell apart the states in one information set, and the
    search stops at a depth limit, where each frontier node is valued by four
    continuation strategies."""
    d = D()
    rx, ry = 200, 30
    lim = 212
    # construction: the depth limit
    d.group('thin')
    d.line((20, lim), (380, lim))
    # the object: chance node, the deals, the player's decisions
    d.group()
    d.line((rx - 7, ry), (rx, ry - 7), (rx + 7, ry), (rx, ry + 7), closed=True)  # chance: a diamond
    deals = [rx - 105, rx - 35, rx + 35, rx + 105]
    y1, y2 = 96, 160
    d.lines([[(rx, ry + 7), (x, y1 - 5)] for x in deals])
    for x in deals:
        d.circle(x, y1, 5)
    kids = [x + o for x in deals for o in (-20, 0, 20)]
    d.lines([[(deals[i // 3], y1 + 5), (x, y2)] for i, x in enumerate(kids)])
    for x in kids:
        d.circle(x, y2, 3)
    # information sets: the deals the player cannot tell apart, ringed
    d.group('mid')
    d.ellipse(rx - 70, y1, 56, 12)
    d.ellipse(rx + 70, y1, 56, 12)
    # below the limit: four ways to play on from each frontier node
    fronts = kids[::2]
    d.lines([[(x, y2 + 3), (x + (k - 1.5) * 7, lim + 26)] for x in fronts for k in range(4)])
    d.group()
    for x in fronts:
        for k in range(4):
            d.circle(x + (k - 1.5) * 7, lim + 28, 1.5)
    d.group()
    d.text(rx + 14, ry + 3, 'DEAL', size=7, anchor='start')
    d.text(24, 70, 'INFORMATION SETS', size=7, anchor='start')
    d.text(376, lim - 6, 'DEPTH LIMIT', size=7, anchor='end')
    d.text(rx, 284, 'BLUEPRINT · FOLD · CALL · RAISE', size=7)
    return d


PLATES = {
    'mechanical-turk': mechanical_turk,
    'shannon-chess': shannon_chess,
    'samuel-checkers': samuel_checkers,
    'td-gammon': td_gammon,
    'chinook': chinook,
    'alphazero': alphazero,
    'pluribus': pluribus,
}
