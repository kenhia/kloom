"""Plates for How We Build's Wood segment, part wood1 (sprint 026):
Neolithic wells, Egyptian carpentry and the Roman plane."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down)."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _teeth(x0, y0, x1, n, h, rake, toward=-1):
    """A row of saw teeth along y0 from x0 to x1, points down, each with a cutting face
    raked `rake` degrees from the perpendicular; `toward` -1 makes the cutting faces
    face -x (the teeth cut when the saw moves towards -x)."""
    p = (x1 - x0) / n
    pts = [(x0, y0)]
    off = h * math.tan(math.radians(rake))
    for i in range(n):
        a = x0 + i * p
        if toward < 0:
            tip = (a + off, y0 + h)          # the cutting face runs from the tip up to the gullet at a
            pts += [tip, (a + p, y0)]
        else:
            tip = (a + p - off, y0 + h)
            pts += [tip, (a + p, y0)]
    return pts


def egyptian_carpentry():
    d = D()
    gy = 272                                  # the workshop yard's floor
    lx0, lx1 = 108, 162                       # the log, seen square to the plane of the cut
    ltop, lbot = 64, 266
    px0, px1 = 126, 144                       # the sawing post, behind the log
    sa = 32                                   # the blade's angle below horizontal, degrees
    u = _dir(sa)
    nx, ny = -u[1], u[0]                      # the blade's normal, towards its toothed edge
    # the cut front: where the teeth are, a line across the log through (cx, cy)
    cx, cy = (lx0 + lx1) / 2, 160
    tipx, tipy = cx - u[0] * 62, cy - u[1] * 62
    bl = 150                                  # blade length
    w = 10                                    # blade depth at the heel
    hx, hy = tipx + u[0] * bl, tipy + u[1] * bl
    # the toothed edge runs from the tip to the heel; the back is offset by the blade's depth
    edge = lambda t: (tipx + u[0] * t, tipy + u[1] * t)
    back = lambda t: (tipx + u[0] * t - nx * w * (0.4 + 0.6 * t / bl), tipy + u[1] * t - ny * w * (0.4 + 0.6 * t / bl))

    def inside(pt):
        return lx0 <= pt[0] <= lx1

    d.group('thin')
    d.line((14, gy), (236, gy))
    d.line(((lx0 + lx1) / 2, 24), ((lx0 + lx1) / 2, gy + 6))          # the log's axis
    d.line((tipx - u[0] * 26, tipy - u[1] * 26), (hx + u[0] * 70, hy + u[1] * 70))   # the stroke
    # the blade where the log hides it, and the cut already made above the teeth
    t_in = [(lx0 - tipx) / u[0], (lx1 - tipx) / u[0]]
    d.line(edge(t_in[0]), edge(t_in[1]))
    d.line(back(t_in[0]), back(t_in[1]))
    d.group()
    # the post, rising behind the log, and the log itself
    d.line((px0, ltop), (px0, 34), (px1, 34), (px1, ltop))
    d.line((lx0, lbot), (lx0, ltop), (lx1, ltop), (lx1, lbot), closed=True)
    d.line((px0, lbot), (px0, gy + 6))
    d.line((px1, lbot), (px1, gy + 6))
    # the saw, drawn where it shows beyond the log: the tip end, and the heel and handle
    d.line(edge(t_in[0]), (tipx, tipy), back(0), back(t_in[0]))
    d.line(edge(t_in[1]), (hx, hy), back(bl), back(t_in[1]))
    d.line((hx, hy), (hx + u[0] * 30 + nx * 4, hy + u[1] * 30 + ny * 4), (hx + u[0] * 32 - nx * 6, hy + u[1] * 32 - ny * 6),
           back(bl))
    d.group('mid')
    # the lashings: figure-of-eight turns of cord round log and post, below the cut
    for y in (204, 244):
        d.lines([[(lx0 - 3, y - 6), (lx1 + 3, y + 6)], [(lx0 - 3, y + 6), (lx1 + 3, y - 6)],
                 [(lx0 - 3, y - 6), (lx0 - 3, y + 6)], [(lx1 + 3, y - 6), (lx1 + 3, y + 6)]])
    # the lever pushed into the top of the cut, with a stone hung from it to hold the kerf open
    lv0 = ((lx0 + lx1) / 2 + 4, ltop + 8)
    lv1 = (lx1 + 46, ltop - 38)
    d.line(lv0, lv1)
    d.line((lv1[0] - 3, lv1[1] + 3), (lv1[0] - 3, lv1[1] + 46))
    d.ellipse(lv1[0] - 3, lv1[1] + 54, 9, 8)
    # the teeth along the blade's edge where it shows, raked to cut on the pull
    segs = []
    t = 3.0
    while t < bl - 6:
        a, b = edge(t), edge(t + 6)
        if not (inside(a) or inside(b)):
            tip = (a[0] + u[0] * 4.8 + nx * 3, a[1] + u[1] * 4.8 + ny * 3)
            segs.append([a, tip, b])
        t += 6
    d.lines(segs)
    # the pull: an arrow beside the blade, towards the handle
    ax, ay = hx + nx * 22 + u[0] * 6, hy + ny * 22 + u[1] * 6
    d.line((ax - u[0] * 40, ay - u[1] * 40), (ax, ay))
    d.line((ax - u[0] * 7 + nx * 3.5, ay - u[1] * 7 + ny * 3.5), (ax, ay), (ax - u[0] * 7 - nx * 3.5, ay - u[1] * 7 - ny * 3.5))

    # inset 1: a tooth profile, enlarged, with its rake measured from the perpendicular
    ix0, ix1, iy = 262, 382, 50
    d.group('thin')
    d.line((ix0 - 6, iy), (ix1 + 6, iy))
    p = (ix1 - ix0) / 5
    for k in (1, 3):
        d.line((ix0 + k * p, iy - 6), (ix0 + k * p, iy + 26))
    d.group()
    d.line((ix0, iy - 16), (ix1, iy - 16))
    d.line((ix0, iy - 16), *_teeth(ix0, iy, ix1, 5, 18, 14, 1), (ix1, iy - 16))
    d.group('mid')
    d.line((ix0 + 40, iy + 34), (ix0 + 92, iy + 34))
    d.line((ix0 + 85, iy + 30.5), (ix0 + 92, iy + 34), (ix0 + 85, iy + 37.5))

    # inset 2: the teeth seen end on: one-sided set (punched from one side) and an alternate set
    sy = 128
    d.group('thin')
    for cx in (290, 356):
        d.line((cx - 16, sy + 44), (cx + 16, sy + 44))
    d.group()
    for cx, alt in ((290, False), (356, True)):
        t = 3                                 # blade thickness, drawn
        d.line((cx - t / 2, sy), (cx - t / 2, sy + 30))
        d.line((cx + t / 2, sy), (cx + t / 2, sy + 30))
        if alt:
            d.line((cx - t / 2, sy + 30), (cx - t / 2 - 4, sy + 38))
            d.line((cx + t / 2, sy + 30), (cx + t / 2 + 4, sy + 38))
            k0, k1 = cx - t / 2 - 4, cx + t / 2 + 4
        else:
            d.line((cx - t / 2, sy + 30), (cx - t / 2, sy + 38))
            d.line((cx + t / 2, sy + 30), (cx + t / 2 + 1.4, sy + 38))
            k0, k1 = cx - t / 2, cx + t / 2 + 1.4
        d.group('mid')
        d.lines([[(k0, sy + 40), (k0, sy + 48)], [(k1, sy + 40), (k1, sy + 48)]])
        d.group()

    # inset 3: the bow drill: shaft, stone cap, bow and its cord taken once round the shaft
    dx, dtop, dbot = 324, 204, 276
    d.group('thin')
    d.line((dx, dtop - 10), (dx, dbot + 6))
    d.line((262, dbot), (386, dbot))
    d.group()
    d.line((dx - 2.5, dtop + 6), (dx - 2.5, dbot - 8), (dx, dbot), (dx + 2.5, dbot - 8), (dx + 2.5, dtop + 6))
    d.arc(dx, dtop + 6, 11, 180, 360, n=18, ry=8)
    d.line((dx - 11, dtop + 6), (dx + 11, dtop + 6))
    by = 238
    bow = [(262 + i * 3, by - 10 * math.sin(math.pi * i / 40)) for i in range(41)]
    d.line(*bow)
    d.group('mid')
    d.line(bow[0], (dx - 2.5, by + 2))
    d.line(bow[-1], (dx + 2.5, by - 2))
    d.ellipse(dx, by, 4.5, 2.2)
    d.arc(dx, by + 18, 9, 200, 340, n=12, ry=3)
    d.line((dx + 8.5 - 3, by + 18 - 4), (dx + 8.5, by + 18 - 1), (dx + 8.5 - 4, by + 18 + 1))
    d.group('mid')
    d.text(lv1[0] + 6, lv1[1] - 4, 'WEDGE', size=8, anchor='start')
    d.text(px0 - 8, 44, 'POST', size=8, anchor='end')
    d.text(ix0 + 34, iy + 37, 'PULL', size=8, anchor='end')
    d.text(323, sy + 60, 'KERF', size=8)
    d.text(dx, dbot + 18, 'BOW DRILL', size=8)
    d.text(122, 290, 'RIPPING A LOG LASHED TO A POST', size=8)
    return d


PLATES = {'egyptian-carpentry': egyptian_carpentry}


def neolithic_wells():
    d = D()
    # the log in section: rings, bark, and the splits that turn it into planks
    cx, cy, R = 100, 132, 78
    d.group('thin')
    for r in range(12, R, 11):
        d.circle(cx, cy, r)
    d.line((cx, cy - R - 16), (cx, cy + R + 10))                    # the first split, produced
    d.group()
    # the bark: an irregular circle
    bark = [(cx + (R + 1.2 * math.sin(5 * t) + 0.8 * math.sin(11 * t)) * math.cos(t),
             cy + (R + 1.2 * math.sin(5 * t) + 0.8 * math.sin(11 * t)) * math.sin(t))
            for t in [2 * math.pi * i / 120 for i in range(121)]]
    d.line(*bark)
    d.circle(cx, cy, 2)                                              # the pith
    d.group('mid')
    # first split: in half, through the pith; then each half again, radially on the left,
    # tangentially (a chord) on the right
    d.line((cx, cy - R), (cx, cy + R))
    for a in (-135, 135, 180):
        u = (math.cos(math.radians(a)), math.sin(math.radians(a)))
        d.line((cx, cy), (cx + u[0] * R, cy + u[1] * R))
    ch = 42                                                          # the chord's distance from the pith
    hc = math.sqrt(R * R - ch * ch)
    d.line((cx + ch, cy - hc), (cx + ch, cy + hc))
    # wedges driven into the top of the first split and the chord
    for wx, wy in ((cx, cy - R), (cx + ch, cy - hc)):
        d.line((wx - 5, wy - 22), (wx, wy + 6), (wx + 5, wy - 22), closed=True)
        d.line((wx - 7, wy - 22), (wx + 7, wy - 22))
    # the corner of a log-cabin lining in elevation: planks of this wall run long,
    # the other wall's planks show their ends, half a plank higher, notched over each other
    ex, ey = 236, 150                                                # the corner's foot
    L, H, T = 130, 22, 14                                            # plank length, height, thickness
    d.group('thin')
    d.line((ex - 10, ey), (ex + L + 8, ey))
    d.line((ex + T / 2, ey + 8), (ex + T / 2, ey - 4 * H - 18))
    d.group()
    for k in range(4):
        y0 = ey - k * H
        d.line((ex + T, y0), (ex + L, y0), (ex + L, y0 - H), (ex + T, y0 - H))     # this wall's plank
        # the plank's end, overlapping the cross plank by half: the notch shows as a step
        d.line((ex + T, y0), (ex, y0), (ex, y0 - H / 2), (ex + T, y0 - H / 2))
        d.line((ex + T, y0 - H / 2), (ex + T, y0 - H))
    d.group('mid')
    # the cross planks, end on, between the courses: split timbers, so their ends are wedge-shaped
    for k in range(4):
        y0 = ey - k * H - H / 2
        d.line((ex, y0 - H / 2 + 1), (ex + T, y0 - H / 2 + 1))
        d.lines([[(ex + 2, y0 - 2), (ex + T - 3, y0 - H / 2 + 3)], [(ex + 4, y0 - 1), (ex + T - 2, y0 - H / 2 + 6)]])
    # adze marks on the long faces: short shallow scallops along the grain
    marks = []
    for k in range(4):
        for j in range(5):
            x0 = ex + T + 14 + j * 22 + (k % 2) * 9
            y0 = ey - k * H - H / 2
            marks.append([(x0 + 10 * math.cos(math.radians(t)), y0 + 3 * math.sin(math.radians(t))) for t in range(200, 341, 20)])
    d.lines(marks)
    # the adze: a stone blade lashed across the end of a handle, at 70 degrees to it
    hx0, hy0 = 256, 290                                              # the end of the handle
    ha = -50                                                         # the handle's direction, degrees
    hl = 100
    hu = (math.cos(math.radians(ha)), math.sin(math.radians(ha)))
    hx1, hy1 = hx0 + hu[0] * hl, hy0 + hu[1] * hl                    # the head
    back = ha + 180                                                  # from the head back down the handle
    ba = back - 70                                                   # the blade's direction
    bu = (math.cos(math.radians(ba)), math.sin(math.radians(ba)))
    bn = (-bu[1], bu[0])
    d.group('thin')
    d.line((hx1, hy1), (hx1 + bu[0] * 64, hy1 + bu[1] * 64))
    d.arc(hx1, hy1, 22, ba, back, n=16)
    d.group()
    n = (-hu[1], hu[0])
    d.line((hx0 + n[0] * 3, hy0 + n[1] * 3), (hx1 + n[0] * 3 + hu[0] * 8, hy1 + n[1] * 3 + hu[1] * 8))
    d.line((hx0 - n[0] * 3, hy0 - n[1] * 3), (hx1 - n[0] * 3 + hu[0] * 8, hy1 - n[1] * 3 + hu[1] * 8))
    # the blade: a flat face, a domed back, a bevel to the cutting edge
    b0 = (hx1 + bu[0] * 2, hy1 + bu[1] * 2)
    b1 = (hx1 + bu[0] * 48, hy1 + bu[1] * 48)
    dome = [(b0[0] + bu[0] * 46 * t - bn[0] * (6 + 5 * math.sin(math.pi * t)), b0[1] + bu[1] * 46 * t - bn[1] * (6 + 5 * math.sin(math.pi * t)))
            for t in [i / 12 for i in range(13)]]
    d.line((b0[0] + bn[0] * 5, b0[1] + bn[1] * 5), (b1[0] + bn[0] * 5, b1[1] + bn[1] * 5), (b1[0] + bu[0] * 5 - bn[0] * 1, b1[1] + bu[1] * 5 - bn[1] * 1),
           *dome[::-1], closed=True)
    d.group('mid')
    # the lashing round blade and head
    d.lines([[(hx1 + bu[0] * (6 + 5 * k) + bn[0] * 7, hy1 + bu[1] * (6 + 5 * k) + bn[1] * 7),
              (hx1 + bu[0] * (6 + 5 * k) - bn[0] * 13, hy1 + bu[1] * (6 + 5 * k) - bn[1] * 13)] for k in range(3)])
    d.group('mid')
    d.text(cx, 30, 'WEDGE', size=8)
    d.text(cx - 52, cy + R + 22, 'RADIAL', size=8)
    d.text(cx + 54, cy + R + 22, 'TANGENTIAL', size=8)
    d.text(ex + L / 2 + 6, ey + 16, 'CORNER, NOTCHED', size=8)
    mid = math.radians((ba + back) / 2)
    d.text(hx1 + 38 * math.cos(mid), hy1 + 38 * math.sin(mid) + 3, '70°', size=8)
    d.text(hx1 + 44, hy1 + 84, 'ADZE', size=8)
    return d


PLATES['neolithic-wells'] = neolithic_wells


def roman_plane():
    d = D()
    s = 22                                    # px per inch: the Silchester plane, by Evans's measures
    fx, sy = 40, 172                          # the front of the sole, and the sole's line
    L = 13.25 * s                             # sole length
    top = sy - 2.4 * s                        # the top of the body (the body is lost; its height is a guess)
    pitch = 70
    u = (math.cos(math.radians(pitch)), -math.sin(math.radians(pitch)))   # up the bed, leaning back
    n = (u[1] * -1, u[0])                     # normal to the blade, pointing forward-down... set below
    n = (-math.sin(math.radians(pitch)), -math.cos(math.radians(pitch)))  # towards the front of the plane
    t = 5 / 16 * s                            # blade thickness
    cut = 3.0                                 # the shaving's thickness, much exaggerated
    ex, ey = fx + 6 * s, sy + cut             # the cutting edge, standing below the sole
    il = 4.5 * s                              # blade length
    # the blade's back face lies on the bed, its front face is t in front of it
    bk0, bk1 = (ex, ey), (ex + u[0] * il, ey + u[1] * il)
    fr0, fr1 = (ex + n[0] * t * 0.35, ey + n[1] * t * 0.35), (ex + u[0] * il + n[0] * t, ey + u[1] * il + n[1] * t)
    d.group('thin')
    d.line((14, sy), (390, sy))                                         # the sole's line, produced
    d.line((ex - u[0] * 18, ey - u[1] * 18), (ex + u[0] * (il + 24), ey + u[1] * (il + 24)))   # the bed, produced
    c45 = (math.cos(math.radians(45)), -math.sin(math.radians(45)))
    d.line((ex, ey), (ex + c45[0] * 120, ey + c45[1] * 120))           # common pitch, for comparison
    d.arc(ex, ey, 34, -pitch, 0, n=16)
    d.arc(ex, ey, 52, -45, 0, n=12)
    d.group()
    # the board: planed behind the edge, not yet in front of it
    d.line((14, sy), (ex, sy), (ex, sy + cut), (390, sy + cut))
    d.line((14, sy + 30), (390, sy + 30))
    # the body: a box with a throat in front of the blade and the bed behind it
    mouth_front = ex - 0.375 * s / 1.0 + t / math.sin(math.radians(pitch)) * 0   # the mouth's front edge
    mouth_front = ex - 1.1                                                   # a gap of about a millimetre
    throat_top = (ex - 44, top)
    bed_top = (ex + u[0] * ((sy - top) / -u[1]), top)
    d.line((mouth_front, sy), (fx, sy), (fx, top), throat_top, (mouth_front - 4, sy - 8), (mouth_front, sy))
    d.line((ex, sy), (fx + L, sy), (fx + L, top), bed_top)
    d.line((ex, sy), bed_top)
    d.group('mid')
    # the iron shoe: the sole plate turned up at each end
    d.line((fx + 6, top + 10), (fx - 3, top + 14), (fx - 3, sy + 1.5), (fx + L + 3, sy + 1.5), (fx + L + 3, top + 14), (fx + L - 6, top + 10))
    # the blade
    d.line(bk0, bk1, fr1, fr0, closed=True)
    # the rivet behind the blade (with its lead roller) and the rivet in front, with the wedge between
    rb = (ex + u[0] * 58 - n[0] * 9, ey + u[1] * 58 - n[1] * 9)
    d.circle(*rb, 7.5)
    d.circle(*rb, 2.5)
    rf = (ex + u[0] * 62 + n[0] * (t + 15), ey + u[1] * 62 + n[1] * (t + 15))
    d.circle(*rf, 2.5)
    # the wedge: thin end down, between the blade's face and the front rivet
    w0 = (ex + u[0] * 30 + n[0] * t, ey + u[1] * 30 + n[1] * t)
    w1 = (ex + u[0] * 84 + n[0] * t, ey + u[1] * 84 + n[1] * t)
    d.line(w0, w1, (w1[0] + n[0] * 14, w1[1] + n[1] * 14), (w0[0] + n[0] * 3, w0[1] + n[1] * 3), closed=True)
    # the shaving: off the edge, up the blade's face, and curling forward into the throat
    sp = []
    for i in range(60):
        a = i / 59
        r = 22 * (1 - 0.75 * a)
        ang = math.radians(-90 - 300 * a)
        cx0, cy0 = ex - 10, sy - 24
        sp.append((cx0 + r * math.cos(ang) * (1 if i else 1), cy0 - r * math.sin(ang)))
    sp = [(ex + n[0] * 1.5, ey - 1)] + sp
    d.line(*sp)
    # inset: a long sole resting on the two highest points of a wavy board
    ix0, ix1, iy = 214, 388, 258
    wave = [(x, iy + 5 * math.sin((x - ix0) / 13) + 3 * math.sin((x - ix0) / 5.3)) for x in range(ix0, ix1 + 1, 2)]
    d.group('thin')
    d.line(*wave)
    d.group('mid')
    # the sole: the line through the two highest crests
    best = None
    for i, a in enumerate(wave):
        for b in wave[i + 1:]:
            if b[0] - a[0] < 70:
                continue
            kk = (b[1] - a[1]) / (b[0] - a[0])
            if all(q[1] >= a[1] + kk * (q[0] - a[0]) - 1e-6 for q in wave):
                if best is None or b[0] - a[0] > best[2]:
                    best = (a, kk, b[0] - a[0])
    p0, k = best[0], best[1]
    d.line((ix0, p0[1] + k * (ix0 - p0[0]) - 1.5), (ix1, p0[1] + k * (ix1 - p0[0]) - 1.5))
    d.group('mid')
    d.text(ex + 40, ey - 18, '70°', size=8, anchor='start')
    d.text(ex + 58, ey - 6, '45°', size=8, anchor='start')
    d.text(rf[0] - 18, rf[1] - 18, 'WEDGE', size=8, anchor='end')
    d.text(ex - 6, sy + 22, 'MOUTH', size=8, anchor='end')
    d.text(fx + L - 40, sy + 22, 'SOLE', size=8)
    d.text(ix0 - 8, iy + 4, 'A LONG SOLE', size=8, anchor='end')
    d.text(ix0 - 8, iy + 16, 'CROPS HIGH POINTS', size=8, anchor='end')
    return d


PLATES['roman-plane'] = roman_plane
