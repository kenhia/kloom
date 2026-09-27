"""The western-civ scene plates (sprint 002): one function per frame.

    python3 create-tools/draw-plates/western_civ.py [frame ...]

Writes subjects/western-civ/frames/<frame>/scene.svg; with no arguments,
redraws every frame. A worked example of plates.py, and the reference for
drawing a new subject's plates.
"""
import math, os, random, sys

sys.path.insert(0, os.path.dirname(__file__))
from plates import D, SOLIDS, f, wire  # noqa: E402

FRAMES = os.path.join(os.path.dirname(__file__), '..', '..', 'subjects', 'western-civ', 'frames')


def out(frame):
    return os.path.join(FRAMES, frame, 'scene.svg')


# ---------------------------------------------------------------------------
def prometheus():
    d = D()
    cx, cy = 200, 150
    d.group('thin')
    d.circle(cx, cy, 128)
    d.circle(cx, cy, 118)
    d.lines([[(cx + 118 * math.cos(math.radians(a)), cy + 118 * math.sin(math.radians(a))),
              (cx + (128 if a % 30 == 0 else 123) * math.cos(math.radians(a)),
               cy + (128 if a % 30 == 0 else 123) * math.sin(math.radians(a)))] for a in range(0, 360, 6)])
    d.circle(cx, cy, 84)
    d.group('mid')
    d.lines([[(cx + 92 * math.cos(math.radians(a)), cy - 20 + 92 * math.sin(math.radians(a))),
              (cx + 108 * math.cos(math.radians(a)), cy - 20 + 108 * math.sin(math.radians(a)))]
             for a in range(-165, -10, 15)])
    d.group()
    # fennel stalk
    d.curve('M195 272 C196 240 196 205 197 176 M205 272 C204 240 204 205 203 176')
    for y in (252, 226, 200):
        d.ellipse(200, y, 6.5, 2.2)
    d.curve('M197 238 C188 230 180 228 172 230 M203 214 C212 206 220 204 228 206')
    d.group()
    # flame
    d.curve('M200 178 C172 168 164 140 178 116 C182 132 190 136 194 128 C198 110 190 92 204 66 '
            'C208 90 226 100 230 122 C236 106 232 96 238 88 C250 116 246 162 200 178 Z')
    d.curve('M200 170 C186 162 184 146 192 132 C196 142 202 142 204 134 C208 122 204 110 210 100 '
            'C216 120 228 134 220 154 C216 164 208 168 200 170 Z')
    d.group('mid')
    d.curve('M184 96 l-4 -8 M226 76 l3 -9 M246 104 l7 -5 M166 124 l-8 -3 M214 52 l1 -8')
    d.save(out('prometheus'))


def writing():
    d = D()
    rnd = random.Random(3200)
    d.group('thin')
    # tablet thickness
    d.curve('M96 58 L110 44 Q200 34 290 44 L304 58 M304 58 L312 50 Q318 150 312 244 L304 252')
    d.group()
    d.curve('M96 58 Q200 46 304 58 Q314 155 304 252 Q200 264 96 252 Q86 155 96 58 Z')
    d.group('mid')
    rows = [96, 136, 176, 216]
    d.lines([[(106, y), (296, y)] for y in rows])
    d.group()
    segs = []
    def wedge(x, y, a, s=1.0):
        ca, sa = math.cos(a), math.sin(a)
        R = lambda px, py: (x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s)
        segs.append([R(0, -4), R(6, 0), R(0, 4), R(0, -4)])
        segs.append([R(6, 0), R(18, 0)])
    for top in [58] + rows:
        y = top + 20
        if y > 245:
            continue
        x = 112
        while x < 285:
            k = rnd.random()
            if k < 0.45:
                wedge(x, y - 6, 0)
                x += 22
            elif k < 0.75:
                wedge(x + 6, y - 14, math.pi / 2, 0.8)
                x += 12
            else:
                wedge(x, y - 10, math.pi / 4, 0.8)
                x += 18
            x += rnd.choice([0, 4, 10])
    d.lines(segs)
    d.group()
    # reed stylus
    d.curve('M330 274 L262 196 L256 186 L270 190 L338 268 Z M262 196 L270 190')
    d.save(out('writing'))


def greek():
    d = D()
    cx, cy = 200, 128
    d.group('thin')
    d.circle(cx, cy, 86)
    d.circle(cx, cy, 70)
    d.lines([[(cx - 150, cy), (cx + 150, cy)], [(cx, cy - 104), (cx, cy + 104)]])
    d.group()
    wire(d, SOLIDS['dodeca'], cx, cy, 70 / math.sqrt(3), 0.33, 0.71, 0.18)
    d.group()
    xs = [60, 150, 250, 340]
    for x, (name, scale) in zip(xs, [('tetra', 18), ('octa', 26), ('icosa', 17), ('cube', 17)]):
        wire(d, SOLIDS[name], x, 256, scale, 0.45, 0.6, 0.15)
    d.group('mid')
    for x, lab in zip(xs, ['FIRE', 'AIR', 'WATER', 'EARTH']):
        d.text(x, 296, lab, 9)
    d.save(out('greek-inquiry'))


def eratosthenes():
    d = D()
    cx, cy, r = 190, 205, 92
    ang = math.radians(24)  # 7.2° exaggerated for legibility
    sy = (cx, cy - r)
    al = (cx - r * math.sin(ang), cy - r * math.cos(ang))
    d.group('thin')
    d.circle(cx, cy, r)
    d.lines([[(cx - r - 20, cy), (cx + r + 20, cy)]])
    d.group('mid')
    # sun rays, parallel, from above: to the ground, or to the gnomon's tip
    gt0 = (al[0] - 20 * math.sin(ang), al[1] - 20 * math.cos(ang))
    rays = [[(gt0[0], 4), gt0]]
    for x in (cx - 44, cx, cx + 44, cx + 80):
        y = cy - math.sqrt(max(r * r - (x - cx) ** 2, 0)) if abs(x - cx) < r else 150
        rays.append([(x, 4), (x, y)])
    d.lines(rays)
    # the shadow the gnomon casts
    d.line(al, (gt0[0], al[1] - 1))
    d.group()
    d.circle(cx, cy, r)
    # radii and gnomon
    d.line((cx, cy), sy)
    d.line((cx, cy), al)
    gt = (al[0] - 20 * math.sin(ang), al[1] - 20 * math.cos(ang))
    d.line(al, gt)
    # the well at Syene
    d.line((cx - 5, sy[1] - 6), (cx - 5, sy[1] + 10), (cx + 5, sy[1] + 10), (cx + 5, sy[1] - 6))
    d.group()
    # angle arcs: at the centre and at the gnomon
    d.arc(cx, cy, 30, -90 - 24, -90, 16)
    d.arc(gt[0], gt[1], 16, 90 - 24, 90, 12)
    # arc along the surface
    d.arc(cx, cy, r + 12, -90 - 24, -90, 20)
    d.group()
    # sun
    d.circle(330, 40, 16)
    d.lines([[(330 + 21 * math.cos(math.radians(a)), 40 + 21 * math.sin(math.radians(a))),
              (330 + 28 * math.cos(math.radians(a)), 40 + 28 * math.sin(math.radians(a)))] for a in range(0, 360, 30)])
    d.group('mid')
    d.text(cx + 10, sy[1] + 22, 'SYENE', 9, 'start')
    d.text(al[0] - 10, al[1] + 12, 'ALEXANDRIA', 9, 'end')
    d.text(cx - 8, cy - 36, '7°12′', 9, 'end')
    d.save(out('eratosthenes'))


def pantheon():
    d = D()
    g = 262
    L, R = 172, 352
    rr = (R - L) / 2
    cx = (L + R) / 2
    cy = g - rr
    d.group('thin')
    d.circle(cx, cy, rr)  # the inscribed sphere
    d.lines([[(L - 150, cy), (R + 20, cy)], [(cx, cy - rr - 18), (cx, g + 6)]])
    d.group()
    d.line((10, g), (392, g))
    # drum walls (section)
    d.line((L, g), (L, cy))
    d.line((R, g), (R, cy))
    d.line((L - 16, g), (L - 16, cy + 6))
    d.line((R + 16, g), (R + 16, cy + 6))
    # dome inner and outer, with the oculus
    oc = 12
    a_oc = math.degrees(math.asin(oc / rr))
    d.arc(cx, cy, rr, 180, 270 - a_oc, 40)
    d.arc(cx, cy, rr, 270 + a_oc, 360, 40)
    d.curve(f'M{f(L - 16)} {f(cy + 6)} L{f(L - 16)} {f(cy - 8)} L{f(L - 4)} {f(cy - 8)} L{f(L - 4)} {f(cy - 22)} '
            f'L{f(L + 8)} {f(cy - 22)} L{f(L + 8)} {f(cy - 36)} Q{f(cx - 70)} {f(cy - rr - 14)} {f(cx - oc)} {f(cy - rr - 8)}')
    d.curve(f'M{f(R + 16)} {f(cy + 6)} L{f(R + 16)} {f(cy - 8)} L{f(R + 4)} {f(cy - 8)} L{f(R + 4)} {f(cy - 22)} '
            f'L{f(R - 8)} {f(cy - 22)} L{f(R - 8)} {f(cy - 36)} Q{f(cx + 70)} {f(cy - rr - 14)} {f(cx + oc)} {f(cy - rr - 8)}')
    d.group('mid')
    # coffers: notches along the inner dome
    segs = []
    for a in range(196, 262, 12):
        for sgn in (1, -1):
            aa = math.radians(270 + sgn * (270 - a))
            p = (cx + rr * math.cos(aa), cy + rr * math.sin(aa))
            q = (cx + (rr - 7) * math.cos(aa), cy + (rr - 7) * math.sin(aa))
            segs.append([p, q])
    d.lines(segs)
    # niches in the drum
    d.lines([[(L, g - 10), (L + 10, g - 10), (L + 10, g - 60), (L, g - 60)],
             [(R, g - 10), (R - 10, g - 10), (R - 10, g - 60), (R, g - 60)]])
    d.group()
    # portico: columns, entablature, pediment
    cols = [26, 58, 90, 122]
    segs = []
    for x in cols:
        segs += [[(x - 5, g), (x - 5, 146)], [(x + 5, g), (x + 5, 146)], [(x - 8, 146), (x + 8, 146)],
                 [(x - 8, g), (x + 8, g)]]
    d.lines(segs)
    d.line((12, 146), (L - 16, 146))
    d.line((12, 146), (12, 132), (L - 16, 132))
    d.line((8, 132), (74, 92), (140, 132))
    d.line((140, 132), (L - 16, 120), (L - 16, 146))
    d.group('thin')
    d.lines([[(L, g + 14), (R, g + 14)], [(L, g + 10), (L, g + 18)], [(R, g + 10), (R, g + 18)]])
    d.group('mid')
    d.text(cx, g + 30, '43 M', 9)
    d.save(out('pantheon'))


def scriptorium():
    d = D()
    d.group('thin')
    d.circle(70, 70, 44)
    d.circle(70, 70, 30)
    d.group()
    # candle
    d.line((58, 170), (58, 96), (82, 96), (82, 170))
    d.ellipse(70, 96, 12, 3)
    d.line((70, 93), (70, 88))
    d.curve('M70 88 C62 80 64 68 70 56 C76 68 78 80 70 88 Z')
    d.curve('M44 170 L96 170 M50 170 L54 178 L86 178 L90 170')
    d.group()
    # open codex
    d.curve('M120 212 C170 196 214 204 240 222 C266 204 310 196 370 212 L370 96 C310 80 266 88 240 106 '
            'C214 88 170 80 120 96 Z M240 106 L240 222')
    d.curve('M120 212 L118 224 C170 208 214 216 240 232 C266 216 310 208 372 224 L370 212')
    d.group('mid')
    rnd = random.Random(800)
    segs = []
    for i in range(12):
        y0 = 112 + i * 7.6
        x = 142 if i > 2 else 164
        while x < 224:
            w = rnd.uniform(5, 16)
            if x + w > 226:
                break
            t = (x - 120) / 120
            segs.append([(x, y0 - 10 * (1 - t) * 0 + 2 * t), (x + w, y0 + 2 * (t + w / 120))])
            x += w + 3
    d.lines(segs)
    d.line((140, 104), (158, 104), (158, 124), (140, 124), closed=True)
    d.curve('M144 120 C146 108 152 108 154 120 M146 115 L152 115')
    segs = []
    for i in range(7):
        y0 = 112 + i * 7.6
        x = 256
        end = 350 if i < 6 else 300
        while x < end:
            w = rnd.uniform(5, 16)
            if x + w > end:
                break
            t = (x - 240) / 130
            segs.append([(x, y0 + 2 * (1 - t) - 1), (x + w, y0 + 2 * (1 - t) - 1 - w / 80)])
            x += w + 3
    d.lines(segs)
    d.group()
    # quill
    d.curve('M300 164 C330 120 356 70 392 36 C380 70 356 116 306 162 Z M300 164 L292 176')
    d.lines([[(310 + i * 8, 150 - i * 12), (318 + i * 9.4, 140 - i * 12.6)] for i in range(7)])
    d.save(out('scriptorium'))


def magna_carta():
    d = D()
    x0, y0, x1, y1 = 60, 64, 340, 226
    d.group('thin')
    d.lines([[(x0 + (x1 - x0) / 3, y0), (x0 + (x1 - x0) / 3, y1)], [(x0 + 2 * (x1 - x0) / 3, y0), (x0 + 2 * (x1 - x0) / 3, y1)],
             [(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)]])
    d.group()
    d.curve(f'M{x0} {y0} L{x1} {y0 + 2} L{x1 - 2} {y1} L{x0 + 2} {y1 - 1} Z')
    d.curve(f'M{x0 + 2} {y1 - 1} L{x0 + 2} {y1 + 12} L{x1 - 2} {y1 + 12} L{x1 - 2} {y1}')
    d.group('thin')
    rnd = random.Random(1215)
    segs = []
    y = y0 + 10
    while y < y1 - 8:
        x = x0 + 10 + (14 if y == y0 + 10 else 0)
        while x < x1 - 12:
            w = rnd.uniform(4, 14)
            if x + w > x1 - 10:
                break
            segs.append([(x, y), (x + w, y)])
            x += w + 2.2
        y += 5.2
    d.lines(segs)
    d.group()
    # seal on cords
    d.curve('M196 238 C194 250 190 258 188 266 M204 238 C206 250 210 258 212 266')
    d.circle(200, 280, 16)
    d.circle(200, 280, 11)
    d.curve('M194 286 L196 276 L200 272 L204 276 L206 286 M200 272 L200 268')
    d.group()
    # the crown, bowed
    cx, cy, a = 200, 30, math.radians(-16)
    pts = [(-30, 12), (-30, -6), (-18, 4), (-10, -14), (0, 2), (10, -14), (18, 4), (30, -6), (30, 12)]
    R = lambda p: (cx + p[0] * math.cos(a) - p[1] * math.sin(a), cy + p[0] * math.sin(a) + p[1] * math.cos(a))
    d.line(*[R(p) for p in pts], closed=True)
    d.line(R((-30, 6)), R((30, 6)))
    for p in [(-10, -18), (10, -18), (-30, -10), (30, -10)]:
        c = R(p)
        d.circle(c[0], c[1], 2.2)
    d.save(out('magna-carta'))


def florence():
    d = D()
    span = 170
    L, R = 200 - span / 2, 200 + span / 2
    spring = 196
    rad = 0.8 * span
    cL = (L + rad, spring)
    cR = (R - rad, spring)
    top = spring - math.sqrt(rad ** 2 - (rad - span / 2) ** 2)
    d.group('thin')
    # quinto acuto: the two compass centres and their circles
    d.arc(cL[0], cL[1], rad, 180, 250, 30)
    d.arc(cR[0], cR[1], rad, -70, 0, 30)
    d.lines([[(L - 20, spring), (R + 20, spring)], [(200, top - 50), (200, 292)]])
    for c in (cL, cR):
        d.lines([[(c[0] - 4, c[1]), (c[0] + 4, c[1])], [(c[0], c[1] - 4), (c[0], c[1] + 4)]])
    d.group()
    def profile(k, n=40):
        pts = []
        a0 = 180
        a1 = math.degrees(math.atan2(top - spring, 200 - cL[0])) % 360
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            x = cL[0] + rad * math.cos(a)
            y = cL[1] + rad * math.sin(a)
            pts.append((200 + k * (x - 200), y))
        return pts
    outer = profile(1)
    d.line(*outer)
    d.line(*[(400 - x, y) for x, y in outer])
    d.group('mid')
    for k in (0.42,):
        p = profile(k)
        d.line(*p)
        d.line(*[(400 - x, y) for x, y in p])
    # rings of the dome (the horizontal courses)
    segs = []
    for i in range(1, 6):
        y = spring - (spring - top) * i / 6.4
        # half-width of silhouette at y
        xw = min(abs(x - 200) for x, yy in [(x, yy) for x, yy in outer if abs(yy - y) < 4] or [(L, 0)])
        segs.append([(200 - xw, y), (200 - 0.42 * xw, y + 3), (200 + 0.42 * xw, y + 3), (200 + xw, y)])
    d.lines(segs)
    d.group()
    # lantern
    d.line((190, top + 2), (190, top - 22), (210, top - 22), (210, top + 2))
    d.line((186, top - 22), (214, top - 22))
    d.line((188, top - 22), (200, top - 44), (212, top - 22))
    d.line((200, top - 44), (200, top - 54))
    d.circle(200, top - 57, 3)
    # drum with oculi
    d.line((L - 8, spring), (R + 8, spring))
    d.line((L - 8, spring), (L - 8, spring + 40), (R + 8, spring + 40), (R + 8, spring))
    d.line((L + 34, spring), (L + 34, spring + 40))
    d.line((R - 34, spring), (R - 34, spring + 40))
    d.circle(L + 13, spring + 20, 8)
    d.circle(200, spring + 20, 10)
    d.circle(R - 13, spring + 20, 8)
    d.group('mid')
    # nave roofs
    d.line((20, spring + 40), (L - 8, spring + 22))
    d.line((380, spring + 40), (R + 8, spring + 22))
    d.line((20, spring + 40), (20, 290), (380, 290), (380, spring + 40))
    d.lines([[(L - 8, spring + 40), (L - 8, 290)], [(R + 8, spring + 40), (R + 8, 290)]])
    d.group('thin')
    # herringbone hint on the right shell
    segs = []
    for i in range(6):
        y = spring - 12 - i * 16
        x = 200 + 0.72 * min(abs(xx - 200) for xx, yy in outer if abs(yy - y) < 6)
        segs.append([(x - 8, y + 4), (x, y), (x - 4, y - 6)])
    d.lines(segs)
    d.save(out('florence-dome'))


def press():
    d = D()
    g = 272
    d.group('thin')
    d.lines([[(10, g), (390, g)]])
    d.group()
    # cheeks, head, cap, feet
    d.line((70, g), (70, 22))
    d.line((90, g), (90, 22))
    d.line((190, g), (190, 22))
    d.line((210, g), (210, 22))
    d.line((60, 22), (220, 22), (220, 10), (60, 10), closed=True)
    d.line((70, 58), (210, 58))
    d.line((70, 80), (210, 80))
    d.line((56, g), (104, g))
    d.line((176, g), (224, g))
    d.group()
    # the screw, its thread, the bar
    d.line((132, 80), (132, 132))
    d.line((148, 80), (148, 132))
    d.lines([[(132, y), (148, y + 6)] for y in range(84, 128, 8)])
    d.line((140, 104), (226, 90))
    d.circle(229, 89.5, 4)
    d.group()
    # hose and platen
    d.line((120, 132), (160, 132), (160, 144), (120, 144), closed=True)
    d.line((104, 144), (176, 144), (176, 156), (104, 156), closed=True)
    d.group()
    # carriage and rails running out to the right
    d.line((56, 176), (374, 176))
    d.line((56, 184), (374, 184))
    d.line((100, 168), (180, 168), (180, 176), (100, 176), closed=True)
    d.line((350, 184), (350, g))
    d.line((340, g), (360, g))
    d.group('mid')
    # the forme of type on the bed
    d.lines([[(106 + i * 6, 170), (106 + i * 6, 174)] for i in range(13)])
    d.group()
    # tympan and frisket, hinged open
    d.line((180, 168), (258, 110), (318, 150), (240, 208 - 40), closed=False)
    d.line((180, 168), (240, 168))
    d.group('mid')
    d.lines([[(200 + i * 7, 150 - i * 5.2), (238 + i * 7, 176 - i * 5.2 - 20)] for i in range(7)])
    d.save(out('printing-press'))


def voyages():
    d = D()
    cx, cy, r = 190, 152, 118
    lat0, lon0 = math.radians(-10), math.radians(-28)
    def proj(lat, lon):
        lat, lon = math.radians(lat), math.radians(lon)
        x = math.cos(lat) * math.sin(lon - lon0)
        y = math.cos(lat0) * math.sin(lat) - math.sin(lat0) * math.cos(lat) * math.cos(lon - lon0)
        c = math.sin(lat0) * math.sin(lat) + math.cos(lat0) * math.cos(lat) * math.cos(lon - lon0)
        return (cx + r * x, cy - r * y, c > 0)
    def poly(coords, closed=False):
        segs, cur = [], []
        pts = list(coords)
        if closed:
            pts.append(pts[0])
        # densify
        dense = []
        for (a, b), (c, e) in zip(pts, pts[1:]):
            for i in range(6):
                dense.append((a + (c - a) * i / 6, b + (e - b) * i / 6))
        dense.append(pts[-1])
        for la, lo in dense:
            x, y, vis = proj(la, lo)
            if vis:
                cur.append((x, y))
            elif cur:
                segs.append(cur)
                cur = []
        if cur:
            segs.append(cur)
        return segs
    d.group('thin')
    segs = []
    for la in range(-60, 90, 30):
        segs += poly([(la, lo) for lo in range(-180, 181, 10)])
    for lo in range(-180, 180, 30):
        segs += poly([(la, lo) for la in range(-90, 91, 10)])
    d.lines(segs)
    d.group()
    d.circle(cx, cy, r)
    d.group('mid')
    samerica = [(12, -72), (10, -62), (5, -52), (-2, -44), (-5, -35), (-8, -35), (-13, -38), (-23, -42),
                (-28, -48), (-34, -53), (-39, -57), (-42, -64), (-47, -66), (-52, -69), (-55, -68), (-54, -72),
                (-47, -75), (-38, -73), (-30, -71), (-18, -70), (-14, -76), (-5, -81), (1, -80), (7, -78), (9, -76)]
    africa = [(35, -6), (37, 10), (32, 20), (31, 32), (22, 37), (12, 44), (11, 51), (2, 45), (-5, 39),
              (-15, 40), (-25, 35), (-34, 26), (-34, 18), (-28, 15), (-17, 12), (-9, 13), (-1, 9), (4, 7),
              (5, -2), (4, -8), (8, -13), (13, -17), (21, -17), (28, -13), (33, -9)]
    europe = [(36, -9), (43, -9), (44, -1), (48, -5), (51, 2), (54, 8), (57, 8), (59, 11), (63, 5),
              (70, 20), (65, 25)]
    namerica = [(9, -76), (15, -83), (18, -88), (21, -87), (21, -90), (19, -96), (26, -97), (30, -89),
                (30, -84), (25, -81), (30, -81), (35, -76), (41, -72), (45, -66), (47, -60), (52, -56), (60, -64)]
    segs = poly(samerica) + poly(africa, closed=True) + poly(europe) + poly(namerica)
    d.lines(segs)
    d.group()
    # longitudes kept continuous (westward) so no leg wraps the wrong way
    route = [(37, -6), (28, -16), (14, -24), (-5, -32), (-23, -43), (-33, -52), (-49, -67), (-52, -70),
             (-53, -75), (-45, -80), (-30, -85), (-10, -110), (5, -140), (13, -215), (10, -235), (-1, -233),
             (-9, -236), (-20, -260), (-30, -300), (-35, -340), (-25, -350), (0, -365), (15, -380), (30, -374), (37, -366)]
    d.lines(poly(route))
    d.group()
    # compass rose, portolan style
    rx, ry = 342, 246
    segs = []
    for i in range(16):
        a = math.radians(i * 22.5)
        L = 36 if i % 4 == 0 else (24 if i % 2 == 0 else 16)
        segs.append([(rx, ry), (rx + L * math.sin(a), ry - L * math.cos(a))])
    d.lines(segs)
    d.circle(rx, ry, 10)
    d.group('mid')
    d.text(rx, ry - 42, 'N', 9)
    d.save(out('voyages'))


def globe_theatre():
    d = D()
    cx = 200
    n = 20
    ytop, ybot, rx, ry = 112, 238, 136, 34
    def pt(i, y, rxx=rx, ryy=ry):
        a = 2 * math.pi * i / n + math.pi / n
        return (cx + rxx * math.cos(a), y + ryy * math.sin(a))
    front = [i for i in range(n + 1) if math.sin(2 * math.pi * i / n + math.pi / n) > -0.05]
    d.group('thin')
    d.line(*[pt(i, ytop) for i in range(n + 1)])
    d.group()
    # roof ring: outer eave and inner edge (the open yard)
    d.line(*[pt(i, ytop - 14, rx + 6, ry + 2) for i in range(n + 1)])
    d.line(*[pt(i, ytop + 2, rx - 30, ry - 8) for i in range(n + 1)])
    # walls: front half, three galleries
    for y in (ytop, ytop + 42, ytop + 84, ybot):
        d.line(*[pt(i, y) for i in range(n + 1) if math.sin(2 * math.pi * i / n + math.pi / n) >= -0.01])
    d.group('mid')
    segs = []
    for i in range(n):
        s = math.sin(2 * math.pi * i / n + math.pi / n)
        if s >= -0.01:
            segs.append([pt(i, ytop), pt(i, ybot)])
    d.lines(segs)
    d.group('thin')
    # timber framing, braced in alternate bays
    segs = []
    for i in range(n):
        s0 = math.sin(2 * math.pi * i / n + math.pi / n)
        s1 = math.sin(2 * math.pi * (i + 1) / n + math.pi / n)
        if s0 > 0.1 and s1 > 0.1 and i % 2 == 0:
            for y in (ytop, ytop + 42, ytop + 84):
                a, b = pt(i, y), pt(i + 1, y + 42)
                segs.append([a, b])
    d.lines(segs)
    d.group()
    # the hut with its flag
    hx, hy = 172, ytop - 18
    d.line((hx - 16, hy), (hx - 16, hy - 26), (hx + 16, hy - 26), (hx + 16, hy))
    d.line((hx - 20, hy - 26), (hx, hy - 42), (hx + 20, hy - 26))
    d.line((hx, hy - 42), (hx, hy - 78))
    d.curve(f'M{hx} {hy - 78} C{hx + 14} {hy - 84} {hx + 24} {hy - 70} {hx + 40} {hy - 76} '
            f'L{hx + 40} {hy - 58} C{hx + 24} {hy - 52} {hx + 14} {hy - 66} {hx} {hy - 60}')
    # the doorway
    dx, dy = pt(5, ybot)
    d.line((dx - 10, dy), (dx - 10, dy - 28), (dx + 10, dy - 28), (dx + 10, dy))
    d.save(out('shakespeare'))


def steam():
    d = D()
    g = 282
    d.group('thin')
    d.lines([[(10, g), (390, g)]])
    # the engine house wall the beam rests on
    d.lines([[(170, g), (170, 96)], [(230, g), (230, 96)], [(164, 96), (236, 96)]])
    d.group()
    # the beam on its pivot
    d.curve('M52 66 Q200 44 348 66 Q200 88 52 66 Z')
    d.circle(200, 66, 5)
    d.line((188, 96), (200, 66), (212, 96))
    d.group()
    # cylinder with its piston rod and the parallel motion
    d.line((58, 150), (106, 150), (106, 262), (58, 262), closed=True)
    d.line((52, 150), (112, 150))
    d.line((52, 262), (112, 262))
    d.line((82, 150), (82, 104))
    d.line((82, 104), (70, 66))
    d.line((82, 104), (110, 104), (100, 70))
    d.circle(82, 104, 2.5)
    d.group('mid')
    # air pump and condenser beneath, in the cold well
    d.line((122, 212), (148, 212), (148, 272), (122, 272), closed=True)
    d.line((106, 240), (122, 240))
    d.line((135, 212), (135, 76))
    d.group()
    # connecting rod, sun-and-planet gear, flywheel
    fx, fy, fr = 314, 204, 62
    d.line((342, 68), (314 + 17, 204 - 9))
    d.circle(fx, fy, fr)
    d.circle(fx, fy, fr - 8)
    d.lines([[(fx + 12 * math.cos(math.radians(a)), fy + 12 * math.sin(math.radians(a))),
              (fx + (fr - 8) * math.cos(math.radians(a)), fy + (fr - 8) * math.sin(math.radians(a)))] for a in range(22, 382, 45)])
    d.circle(fx, fy, 12)
    d.circle(fx + 17, fy - 9, 7)
    d.line((fx - 34, g), (fx, fy), (fx + 34, g))
    d.group('mid')
    # centrifugal governor
    gx, gy = 256, 150
    d.line((gx, g), (gx, gy - 10))
    d.line((gx, gy), (gx - 20, gy + 26))
    d.line((gx, gy), (gx + 20, gy + 26))
    d.circle(gx - 22, gy + 30, 5)
    d.circle(gx + 22, gy + 30, 5)
    d.line((gx - 10, gy + 13), (gx, gy + 34), (gx + 10, gy + 13))
    d.line((gx - 6, gy + 34), (gx + 6, gy + 34))
    d.save(out('steam'))


def maxwell():
    d = D()
    x0, y0, x1, y1 = 30, 196, 380, 136
    L = math.dist((x0, y0), (x1, y1))
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    # "depth" direction for B, drawn obliquely
    bx, by = -0.55, 0.42
    d.group('thin')
    d.line((x0, y0), (x1, y1))
    d.lines([[(x0 + ux * t, y0 + uy * t), (x0 + ux * t, y0 + uy * t - 70)] for t in range(0, int(L), 28)][:0])
    d.group()
    E, B, stemsE, stemsB = [], [], [], []
    for i in range(0, 241):
        t = i / 240 * (L - 20)
        px, py = x0 + ux * t, y0 + uy * t
        s = math.sin(t / (L - 20) * 2 * math.pi * 2.25)
        E.append((px, py - 76 * s))
        B.append((px + 70 * s * bx, py + 70 * s * by))
        if i % 8 == 0:
            stemsE.append([(px, py), (px, py - 76 * s)])
            stemsB.append([(px, py), (px + 70 * s * bx, py + 70 * s * by)])
    d.line(*E)
    d.group()
    d.line(*B)
    d.group('mid')
    d.lines(stemsE)
    d.group('thin')
    d.lines(stemsB)
    d.group()
    # arrow along the axis
    d.line((x1 - 10 * ux - 5 * uy, y1 - 10 * uy + 5 * ux), (x1, y1), (x1 - 10 * ux + 5 * uy, y1 - 10 * uy - 5 * ux))
    d.group('mid')
    d.text(E[30][0] - 8, E[30][1] - 8, 'E', 11)
    d.text(B[30][0] - 10, B[30][1] + 14, 'B', 11)
    d.text(x1 - 8, y1 - 12, 'c', 11)
    d.save(out('maxwell'))


def dna():
    d = D()
    cx = 170
    y0, y1 = 16, 284
    amp = 58
    turns = 2.2
    ph = 2.3
    def x(th, p):
        return cx + amp * math.sin(th + p)
    def depth(th, p):
        return math.cos(th + p)
    d.group('thin')
    d.lines([[(cx, y0 - 4), (cx, y1 + 4)]])
    n = 400
    for p in (0, ph):
        back, cur = [], []
        front = []
        curf = []
        for i in range(n + 1):
            th = 2 * math.pi * turns * i / n
            y = y0 + (y1 - y0) * i / n
            pt = (x(th, p), y)
            if depth(th, p) < 0:
                cur.append(pt)
                if curf:
                    front.append(curf); curf = []
            else:
                curf.append(pt)
                if cur:
                    back.append(cur); cur = []
        if cur: back.append(cur)
        if curf: front.append(curf)
        d.lines(back)
        d.group()
        d.lines(front)
        d.group('thin')
    d.group('mid')
    segs = []
    for i in range(0, n + 1, 16):
        th = 2 * math.pi * turns * i / n
        y = y0 + (y1 - y0) * i / n
        segs.append([(x(th, 0), y), (x(th, ph), y)])
    d.lines(segs)
    d.group('thin')
    # a turn measured
    tlen = (y1 - y0) / turns
    d.lines([[(cx + 84, y0 + 20), (cx + 84, y0 + 20 + tlen)], [(cx + 79, y0 + 20), (cx + 89, y0 + 20)],
             [(cx + 79, y0 + 20 + tlen), (cx + 89, y0 + 20 + tlen)]])
    d.group('mid')
    d.text(cx + 94, y0 + 24 + tlen / 2, '3.4 NM', 9, 'start')
    d.group('thin')
    # photo 51: the X of diffraction spots
    px, py = 330, 230
    d.circle(px, py, 40)
    d.circle(px, py, 30)
    d.group('mid')
    segs = []
    for k in range(1, 6):
        for sx in (-1, 1):
            for sy in (-1, 1):
                x0_, y0_ = px + sx * k * 4.2, py + sy * k * 5.2
                segs.append([(x0_ - 1.6, y0_), (x0_ + 1.6, y0_)])
    segs += [[(px - 4, py - 36), (px + 4, py - 36)], [(px - 4, py + 36), (px + 4, py + 36)]]
    d.lines(segs)
    d.save(out('dna'))


def saturn():
    d = D(sw=1.1)
    cx = 132
    d.group('thin')
    # earth's limb and the trajectory to the moon
    d.arc(200, 1060, 800, 250, 290, 60)
    d.curve('M150 40 C220 -10 300 10 340 60')
    d.group()
    d.circle(352, 72, 18)
    d.curve('M352 54 A18 18 0 0 0 352 90 A11 18 0 0 1 352 54 Z')
    d.group()
    # Saturn V, stage by stage (not to scale in width)
    w1, w2, w3 = 20, 20, 13
    stages = [
        ('S-IC', 290, 214, w1),
        ('S-II', 214, 150, w2),
        ('S-IVB', 138, 100, w3),
    ]
    segs = []
    for _, yb, yt, w in stages:
        segs.append([(cx - w, yb), (cx - w, yt), (cx + w, yt), (cx + w, yb)])
    segs.append([(cx - w2, 150), (cx - w3, 138)])
    segs.append([(cx + w2, 150), (cx + w3, 138)])
    segs.append([(cx - w3, 150), (cx + w3, 150)])
    # SLA, service module, command module, escape tower
    segs.append([(cx - w3, 100), (cx - 9, 78), (cx + 9, 78), (cx + w3, 100)])
    segs.append([(cx - 9, 78), (cx - 9, 70), (cx + 9, 70), (cx + 9, 78)])
    segs.append([(cx - 9, 70), (cx - 3, 58), (cx + 3, 58), (cx + 9, 70)])
    segs.append([(cx, 58), (cx, 34)])
    segs.append([(cx - 3, 50), (cx, 44), (cx + 3, 50)])
    d.lines(segs)
    d.group()
    # fins and engines
    d.lines([[(cx - w1, 272), (cx - w1 - 10, 290), (cx - w1, 290)], [(cx + w1, 272), (cx + w1 + 10, 290), (cx + w1, 290)],
             [(cx - 12, 290), (cx - 16, 298), (cx - 4, 298), (cx - 8, 290)], [(cx + 8, 290), (cx + 4, 298), (cx + 16, 298), (cx + 12, 290)]])
    d.group('mid')
    d.lines([[(cx - w1, y), (cx + w1, y)] for y in (230, 250)] + [[(cx - w2, 180), (cx + w2, 180)], [(cx - w3, 120), (cx + w3, 120)]])
    d.group('thin')
    # launch umbilical tower
    tx = 180
    segs = [[(tx, 298), (tx, 40)], [(tx + 14, 298), (tx + 14, 40)]]
    for y in range(298, 40, -14):
        segs += [[(tx, y), (tx + 14, y - 14)], [(tx, y), (tx + 14, y)]]
    for y in (96, 150, 214):
        segs.append([(tx, y), (cx + 22, y)])
    d.lines(segs)
    d.group('mid')
    for lab, y in [('T–10', 262), ('T–9', 234), ('T–8', 206)][:0]:
        d.text(240, y, lab, 9, 'start')
    d.save(out('moon-landing'))


def webb():
    d = D()
    cx, cy, s = 200, 128, 24
    def hexagon(x, y, k=0.94):
        return [(x + s * k * math.cos(math.radians(60 * i + 30)), y + s * k * math.sin(math.radians(60 * i + 30))) for i in range(7)]
    # axial coordinates for rings 1 and 2 (pointy-top)
    def axial(q, r):
        return (cx + s * math.sqrt(3) * (q + r / 2), cy + s * 1.5 * r)
    cells = []
    for q in range(-2, 3):
        for r in range(-2, 3):
            if max(abs(q), abs(r), abs(-q - r)) in (1, 2):
                cells.append(axial(q, r))
    d.group('thin')
    # sunshield: five layers seen from the front, below and behind
    for k in range(5):
        dy = k * 5
        d.line((cx - 176 + k * 4, 246 + dy), (cx, 196 + dy), (cx + 176 - k * 4, 246 + dy), (cx, 292 - k * 1.5), closed=True)
    d.group()
    for x, y in sorted(cells, key=lambda p: (p[1], p[0])):
        d.line(*hexagon(x, y))
    d.group('mid')
    # struts to the secondary mirror
    rim = [(cx, cy - 5 * s), (cx - 4.3 * s, cy + 2.4 * s), (cx + 4.3 * s, cy + 2.4 * s)]
    d.lines([[(cx, cy), p] for p in rim][:0])
    d.lines([[rim[0], (cx, cy - 12)], [rim[1], (cx - 10, cy + 6)], [rim[2], (cx + 10, cy + 6)]])
    d.group()
    d.circle(cx, cy, 10)
    d.circle(cx, cy, 4)
    d.save(out('jwst'))


def gutenberg():
    d = D()
    x0, y0, x1, y1 = 104, 16, 296, 286
    d.group('thin')
    d.lines([[(x0 + 20, y0 + 22), (x1 - 20, y0 + 22)], [(x0 + 20, y1 - 26), (x1 - 20, y1 - 26)],
             [(x0 + 20, y0 + 14), (x0 + 20, y1 - 16)], [(x1 - 20, y0 + 14), (x1 - 20, y1 - 16)],
             [((x0 + x1) / 2 - 5, y0 + 14), ((x0 + x1) / 2 - 5, y1 - 16)], [((x0 + x1) / 2 + 5, y0 + 14), ((x0 + x1) / 2 + 5, y1 - 16)]])
    d.group()
    d.line((x0, y0), (x1, y0), (x1, y1), (x0, y1), closed=True)
    d.group('mid')
    rnd = random.Random(1455)
    top, bot = y0 + 22, y1 - 26
    step = (bot - top) / 41
    for col, (a, b) in enumerate([(x0 + 20, (x0 + x1) / 2 - 5), ((x0 + x1) / 2 + 5, x1 - 20)]):
        segs = []
        for i in range(42):
            y = top + i * step
            x = a + (28 if col == 0 and i < 6 else 0)
            while x < b - 2:
                w = rnd.uniform(3, 11)
                w = min(w, b - x)
                segs.append([(x, y), (x + w, y)])
                x += w + 1.8
        d.lines(segs)
    d.group()
    # illuminated initial and its vine in the margin
    d.line((x0 + 20, top - 3), (x0 + 44, top - 3), (x0 + 44, top + 5 * step + 2), (x0 + 20, top + 5 * step + 2), closed=True)
    d.curve(f'M{x0 + 26} {top + 5 * step - 2} L{x0 + 32} {top + 2} L{x0 + 38} {top + 5 * step - 2} M{x0 + 28} {top + 3 * step} L{x0 + 36} {top + 3 * step}')
    d.curve(f'M{x0 + 14} {top} C{x0 + 4} {top + 40} {x0 + 18} {top + 70} {x0 + 8} {top + 110} '
            f'C{x0 + 2} {top + 140} {x0 + 16} {top + 170} {x0 + 10} {top + 220}')
    d.curve(f'M{x0 + 8} {top + 50} c-6 -4 -6 -12 0 -14 M{x0 + 12} {top + 90} c6 -4 6 -12 0 -14 '
            f'M{x0 + 6} {top + 136} c-6 -4 -6 -12 0 -14 M{x0 + 12} {top + 180} c6 -4 6 -12 0 -14')
    d.save(out('gutenberg-bible'))


ALL = {
    'prometheus': prometheus, 'writing': writing, 'greek-inquiry': greek, 'eratosthenes': eratosthenes,
    'pantheon': pantheon, 'scriptorium': scriptorium, 'magna-carta': magna_carta, 'florence-dome': florence,
    'printing-press': press, 'voyages': voyages, 'shakespeare': globe_theatre, 'steam': steam,
    'maxwell': maxwell, 'dna': dna, 'moon-landing': saturn, 'jwst': webb, 'gutenberg-bible': gutenberg,
}

if __name__ == '__main__':
    for name in sys.argv[1:] or ALL:
        ALL[name]()
        print('drew', name)
