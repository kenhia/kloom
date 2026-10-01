"""Plates for How We Build's Joinery trail (sprint 026): the mortise and tenon, the dovetail, nails and screws."""
import math
from plates import D


def mortise_and_tenon():
    """A pegged through tenon, exploded in elevation, and a section through the drawbored peg."""
    d = D()
    # elevation: the stile upright, the rail drawn out to the right of it
    sx0, sx1 = 34, 94             # the stile's face, 60 wide
    ry0, ry1 = 150, 210           # the rail's width, 60
    pull = 80                     # how far the rail is drawn out, the tenon clear of the stile
    sh = sx1 + pull               # the rail's shoulder line, exploded
    ty0, ty1 = ry0 + 10, ry1 - 10  # the tenon's width, inside the haunch lines
    peg = sx0 + 30                # the peg hole in the stile, 30 from its face
    off = 6                       # the drawbore offset, exaggerated for the plate
    d.group('thin')
    # the mortise, hidden in the stile; the tenon's lines carried across; the peg's centres projected down
    d.lines([[(sx0, ty0), (sx1, ty0)], [(sx0, ty1), (sx1, ty1)]])
    d.line((sx1 - 4, ry0 - 18), (sh + 90, ry0 - 18))
    d.line((sx1 - 4, ry1 + 18), (sh + 90, ry1 + 18))
    d.line((peg, 36), (peg, 262))
    d.line((peg + pull, ry0 - 30), (peg + pull, 262))
    d.line((peg + pull + off, ry0 - 30), (peg + pull + off, 262))
    # the offset as a dimension
    d.line((peg + pull - 14, 250), (peg + pull + off + 14, 250))
    d.lines([[(peg + pull, 245), (peg + pull, 255)], [(peg + pull + off, 245), (peg + pull + off, 255)]])
    # the tenon's thickness, a third of the stock, in the section
    d.group()
    # the stile
    d.line((sx0, 30), (sx1, 30), (sx1, 270), (sx0, 270), closed=True)
    # the rail, its shoulder and its through tenon
    d.line((sh + 80, ry0), (sh, ry0), (sh, ty0), (sh - (sx1 - sx0), ty0), (sh - (sx1 - sx0), ty1),
           (sh, ty1), (sh, ry1), (sh + 80, ry1))
    d.group('mid')
    # peg holes: through the stile's cheeks, and in the tenon nearer the shoulder
    d.circle(peg, (ty0 + ty1) / 2, 5)
    d.circle(peg + pull + off, (ty0 + ty1) / 2, 5)
    # the peg itself, tapered, waiting
    px, py = peg, 84
    d.line((px - 4, py - 30), (px + 4, py - 30), (px + 2, py + 4), (px - 2, py + 4), closed=True)
    # section through the joint at the peg: cheek, tenon, cheek, then the rail beyond the shoulder
    x0, x1, x2 = 274, 334, 386    # the stile's back, its face (the shoulder), the rail running on
    y0 = 48
    t = 20                        # each layer a third of 60
    d.group()
    d.line((x0, y0), (x1, y0), (x1, y0 + t), (x2, y0 + t))
    d.line((x0, y0 + 3 * t), (x1, y0 + 3 * t), (x1, y0 + 2 * t), (x2, y0 + 2 * t))
    d.line((x0, y0), (x0, y0 + 3 * t))
    d.line((x2, y0 + t - 12), (x2, y0 + 2 * t + 12))
    d.group('mid')
    d.line((x0, y0 + t), (x1, y0 + t))
    d.line((x0, y0 + 2 * t), (x1, y0 + 2 * t))
    # the holes: through the cheeks at 30 from the face, through the tenon at 30 less the offset
    hx = x1 - 30
    d.lines([[(hx - 5, y0), (hx - 5, y0 + t)], [(hx + 5, y0), (hx + 5, y0 + t)],
             [(hx - 5, y0 + 2 * t), (hx - 5, y0 + 3 * t)], [(hx + 5, y0 + 2 * t), (hx + 5, y0 + 3 * t)]])
    so = 2 * off
    d.lines([[(hx - 5 + so, y0 + t), (hx - 5 + so, y0 + 2 * t)], [(hx + 5 + so, y0 + t), (hx + 5 + so, y0 + 2 * t)]])
    # the peg driven through, bowed where it meets the tenon's hole, and the pull on the tenon
    d.line((hx, y0 - 14), (hx, y0 + t), (hx + so / 2, y0 + 1.5 * t), (hx, y0 + 2 * t), (hx, y0 + 3 * t + 14))
    ay = y0 + 3 * t + 30
    d.line((x1 + 10, ay), (x1 - 30, ay))
    d.lines([[(x1 - 24, ay - 4), (x1 - 30, ay), (x1 - 24, ay + 4)]])
    d.group('thin')
    # the stock divided in thirds, beside the section
    d.lines([[(x2 + 6, y0 + t), (x2 + 12, y0 + t)], [(x2 + 6, y0 + 2 * t), (x2 + 12, y0 + 2 * t)]])
    d.line((x0 - 10, y0), (x0 - 10, y0 + 3 * t))
    d.lines([[(x0 - 14, y0), (x0 - 6, y0)], [(x0 - 14, y0 + 3 * t), (x0 - 6, y0 + 3 * t)],
             [(x0 - 14, y0 + t), (x0 - 6, y0 + t)], [(x0 - 14, y0 + 2 * t), (x0 - 6, y0 + 2 * t)]])
    d.group('mid')
    d.text(sx0 + 30, 284, 'STILE', size=8)
    d.text(sh + 50, ry1 + 34, 'RAIL', size=8)
    d.text(sh - 30, ry0 - 24, 'TENON', size=8)
    d.text(peg + pull + off / 2, 268, 'OFFSET', size=8)
    d.text((x0 + x2) / 2, 30, 'SECTION AT THE PEG', size=8)
    d.text(x0 - 18, y0 + 1.5 * t + 3, '⅓', size=9, anchor='end')
    d.text((x0 + x2) / 2, ay + 16, 'DRAWN TIGHT', size=8)
    return d


PLATES = {'mortise-and-tenon': mortise_and_tenon}


def dovetail():
    """A through dovetail laid out at 1 in 8, the pin board drawn up off the tails, and the bevel's construction."""
    d = D()
    s = 1 / 8                     # the slope: 1 across in 8 along
    x0, x1 = 50, 290              # the boards' width
    top = 150                     # the tail board's end
    depth = 48                    # the gauge line: the pin board's thickness
    base = top + depth
    lift = 76                     # how far the pin board is drawn up
    # pins and tails along the end: half-pin, tail, pin, tail, pin, tail, half-pin, widths at the gauge line
    tail_w, pin_w = 52, 18
    n = 3
    half = (x1 - x0 - n * tail_w - (n - 1) * pin_w) / 2
    tails = []
    x = x0 + half
    for k in range(n):
        tails.append((x, x + tail_w))
        x += tail_w + pin_w
    flare = depth * s             # each side of a tail spreads this much from gauge line to end
    d.group('thin')
    # the gauge line on both boards, the bevel's lines carried down to it
    d.line((x0 - 16, base), (x1 + 16, base))
    d.line((x0 - 16, top - lift + depth), (x1 + 16, top - lift + depth))
    for a, b in tails:
        d.line((a - flare, top - lift - 8), (a - flare, base + 14))
        d.line((b + flare, top - lift - 8), (b + flare, base + 14))
    # the bevel's construction: 8 along, 1 across, as Fairham sets it out
    cx, cy, L = 316, 252, 64
    d.line((cx, cy), (cx + L * s * 0 + 0, cy - L))
    d.line((cx, cy - L), (cx + L * s, cy - L))
    for k in range(9):
        d.line((cx - 3, cy - k * L / 8), (cx + 3, cy - k * L / 8))
    d.group()
    # the tail board: face, the tails wide at the end and narrow at the gauge line, the pin sockets between
    pts = [(x0, 284), (x0, base)]
    for a, b in tails:
        pts += [(a, base), (a - flare, top), (b + flare, top), (b, base)]
    pts += [(x1, base), (x1, 284)]
    d.line(*pts)
    # the pin board, seen end on, drawn up off the tails: each pin fills a socket, narrow at the end
    py = top - lift
    edges = [(x0, x0)] + [(a - flare, a) for a, b in tails]
    rights = [(b + flare, b) for a, b in tails] + [(x1, x1)]
    pins = []
    for (lt, lb), (rt, rb) in zip([(x0, x0)] + rights[:-1], edges[1:] + [(x1, x1)]):
        pins.append(((lt, lb), (rt, rb)))
        d.line((lt, py), (rt, py), (rb, py + depth), (lb, py + depth), closed=True)
    d.group('mid')
    # the pins' end grain hatched, and the grain of the tail board
    hatch = []
    for (lt, lb), (rt, rb) in pins:
        for k in range(1, 4):
            f = k / 4
            y = py + depth * f
            l = lt + (lb - lt) * f
            r = rt + (rb - rt) * f
            hatch.append([(l + 2, y), (r - 2, y)])
    d.lines(hatch)
    grain = []
    for k in range(1, 6):
        gx = x0 + k * (x1 - x0) / 6
        grain.append([(gx + 3 * math.sin(t / 6), base + 6 + t * 5) for t in range(12)])
    d.lines(grain)
    # the bevel's angle
    d.arc(cx, cy, 30, -90, -90 + math.degrees(math.atan(s)), n=8)
    d.line((cx, cy), (cx + L * s, cy - L))
    d.group('mid')
    d.text((x0 + x1) / 2, py - 10, 'PINS, END ON', size=8)
    d.text(x0 - 8, base + 3, 'GAUGE', size=8, anchor='end')
    d.text(cx + 14, cy - L / 2, '8', size=9, anchor='start')
    d.text(cx + L * s / 2, cy - L - 8, '1', size=9)
    d.text(cx + 4, cy + 16, '7.1°', size=8)
    d.text((tails[1][0] + tails[1][1]) / 2, top + 28, 'TAIL', size=8)
    d.text((x0 + x1) / 2, 296, 'TAIL BOARD', size=8)
    return d


PLATES['dovetail'] = dovetail


def wood_screws():
    """Two boards in section: a nail, and a screw in its clearance and pilot holes, with its thread's geometry."""
    d = D()
    y0, y1, y2 = 78, 128, 262     # top of the upper board, the joint, the bottom of the lower board
    xa, xb = 30, 370
    sx = 230                      # the screw's axis
    D_, r = 13, 8.5               # half the shank (major) diameter, half the root diameter
    pitch = 13
    pilot = r * 0.7               # the pilot hole: 70% of the root, the softwood rule
    tip = y2 - 40
    d.group('thin')
    d.line((sx, 40), (sx, y2 + 14))
    # the holes bored first: clearance through the top board, pilot into the bottom one
    d.lines([[(sx - D_ - 1, y0 + 10), (sx - D_ - 1, y1)], [(sx + D_ + 1, y0 + 10), (sx + D_ + 1, y1)]])
    d.lines([[(sx - pilot, y1), (sx - pilot, tip - 10)], [(sx + pilot, y1), (sx + pilot, tip - 10)]])
    # leaders to a crest and a root on the right; the pitch, crest to crest, on the left
    yc = y1 + 6 + 2 * pitch
    yr = yc + 1.5 * pitch
    dx = sx + 64
    d.line((sx + D_ + 2, yc), (dx + 30, yc))
    d.line((sx + r + 2, yr), (dx + 30, yr))
    px_ = sx - D_ - 10
    d.line((px_, yc), (px_, yc + pitch))
    d.lines([[(px_ - 4, yc), (sx - D_ - 1, yc)], [(px_ - 4, yc + pitch), (sx - D_ - 1, yc + pitch)]])
    d.group()
    # the boards
    d.line((xa, y0), (xb, y0), (xb, y1), (xa, y1), closed=True)
    d.line((xa, y1), (xa, y2), (xb, y2), (xb, y1))
    # the screw: a countersunk head, a plain shank through the top board, a thread in the bottom one
    d.line((sx - 2 * D_, y0), (sx - D_, y0 + 10), (sx - D_, y1 + 6))
    d.line((sx + 2 * D_, y0), (sx + D_, y0 + 10), (sx + D_, y1 + 6))
    d.line((sx - 2 * D_, y0), (sx + 2 * D_, y0))
    for side in (-1, 1):
        prof = [(sx + side * D_, y1 + 6)]
        y = y1 + 6
        k = 0
        while y + pitch < tip:
            prof += [(sx + side * r, y + pitch / 2), (sx + side * D_, y + pitch)]
            y += pitch
            k += 1
        # the point: the same pitch, the thread shallowing to nothing (Sloan's patent of 1846)
        n = 3
        for i in range(n):
            f = 1 - (i + 1) / n
            ya = y + pitch / 2
            yb = y + pitch
            prof += [(sx + side * r * f, ya), (sx + side * (r + (D_ - r) * f) * f, yb)]
            y += pitch
        prof.append((sx, y))
        d.line(*prof)
    d.group('mid')
    # the slot in the head
    d.line((sx - 2, y0 - 1), (sx - 2, y0 + 5), (sx + 2, y0 + 5), (sx + 2, y0 - 1))
    # the nail: a head and a plain shank, wood fibres bent down beside it
    nx = 92
    d.line((nx - 11, y0 - 4), (nx + 11, y0 - 4), (nx + 11, y0), (nx - 11, y0), closed=True)
    d.line((nx - 3, y0), (nx - 3, 220), (nx, 230), (nx + 3, 220), (nx + 3, y0))
    fib = []
    for side in (-1, 1):
        for k in range(6):
            yy = 140 + k * 14
            fib.append([(nx + side * 22, yy - 6), (nx + side * 10, yy - 2), (nx + side * 4, yy + 4)])
    d.lines(fib)
    d.group('mid')
    d.text(nx, 284, 'NAIL', size=8)
    d.text(sx, 284, 'SCREW', size=8)
    d.text(sx - 2 * D_ - 6, y0 + 32, 'CLEARANCE', size=8, anchor='end')
    d.text(sx - 2 * D_ - 6, y1 + 80, 'PILOT', size=8, anchor='end')
    d.text(dx + 34, yc + 3, 'SHANK', size=8, anchor='start')
    d.text(dx + 34, yr + 3, 'ROOT', size=8, anchor='start')
    d.text(px_ - 6, yc + pitch / 2 + 3, 'P', size=8, anchor='end')
    d.text(sx, 30, 'ROOT ≈ ⅔ SHANK · PILOT ≈ 0.7 ROOT', size=8)
    return d


PLATES['wood-screws'] = wood_screws
