"""Plates for How We Build's Metal by fire segment, part forge1 (sprint 026):
lost-wax casting, the bloomery and Chinese cast iron."""
import math
from plates import D


def _dir(a):
    """A unit vector at `a` degrees, measured clockwise from +x (SVG's y runs down). Copied from making_stone."""
    return math.cos(math.radians(a)), math.sin(math.radians(a))


def _blob(cx, cy, rx, ry, n=36, wob=0.12, seed=1.0):
    """A closed lumpy outline, for a bloom, a lump of ore or a casting's rough skin."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = 1 + wob * math.sin(3 * t + seed) + wob * 0.6 * math.sin(7 * t + 2 * seed)
        pts.append((cx + rx * r * math.cos(t), cy + ry * r * math.sin(t)))
    return pts


PLATES = {}


def bloomery():
    """A slag-tapping shaft bloomery in section, scaled from Sauder and Williams's smelt 25
    (350 mm bore, tuyere 230 mm above the floor, 1.0 m of shaft above it), with the temperature
    up the shaft plotted beside it."""
    d = D()
    s = 0.19                                   # px per mm
    floor = 262                                # the furnace floor
    cx = 128                                   # the furnace's axis
    bore = 350 * s / 2                         # inner half-width
    wall = 95 * s                              # wall thickness
    ty = floor - 230 * s                       # tuyere height
    top = ty - 1000 * s                        # the top of the shaft
    flare = 6                                  # the shaft narrows a little upwards
    d.group('thin')
    d.line((cx, top - 16), (cx, floor + 10))                          # axis
    d.line((18, floor), (250, floor))                                 # ground
    d.line((cx - bore - wall - 40, ty), (cx + bore + wall + 46, ty))  # the tuyere's level, carried across
    # the temperature graph's axes: height up the shaft against temperature
    gx0, gx1 = 262, 384                        # 800 °C to 1,700 °C
    T = lambda t: gx0 + (t - 800) / 900 * (gx1 - gx0)
    d.line((gx0, top), (gx0, floor))
    d.line((gx0, floor), (gx1, floor))
    for t in (1000, 1200, 1400, 1600):
        d.line((T(t), floor), (T(t), floor + 4))
    # iron's melting point, and that of iron with 4.3 % carbon, as verticals on the graph
    d.line((T(1538), top + 8), (T(1538), floor))
    d.line((T(1146), top + 8), (T(1146), floor))
    d.group()
    # the furnace walls in section: clay, with the tap arch through the left wall at the floor
    # and the tuyere through the right wall
    tap_h = 150 * s
    d.line((cx - bore - wall + flare, top), (cx - bore - wall, floor - tap_h), (cx - bore, floor - tap_h),
           (cx - bore + flare, top), closed=True)
    hole = 50 * s / 2 + 4                      # the tuyere's hole through the wall, half
    d.line((cx + bore - flare, top), (cx + bore, ty - hole), (cx + bore + wall, ty - hole),
           (cx + bore + wall - flare, top), closed=True)
    d.line((cx + bore, ty + hole), (cx + bore, floor), (cx + bore + wall, floor), (cx + bore + wall, ty + hole), closed=True)
    # the tuyere pipe, sloping down into the hearth
    xo = cx + bore + wall + 34
    for dy in (-hole + 1.5, hole - 1.5):
        d.line((xo, ty + dy - 5), (cx + bore - 6, ty + dy + 0.8))
    d.group('mid')
    # the burden: alternating charges of charcoal (open lumps) and ore (small dots), in layers
    for k in range(9):
        y0 = top + 6 + k * 15.5
        if y0 > ty - 16:
            break
        half = bore - flare * (1 - (y0 - top) / (ty - top)) - 3
        if k % 2 == 0:
            lumps = []
            for j in range(5):
                x = cx - half + 5 + j * (2 * half - 10) / 4
                lumps.append([(x - 4, y0 + 7), (x - 2, y0 + 2), (x + 3, y0 + 1), (x + 5, y0 + 6), (x + 1, y0 + 10), (x - 4, y0 + 7)])
            d.lines(lumps)
        else:
            d.lines([[(cx - half + 3 + j * 4.4, y0 + 5 + (j % 3)), (cx - half + 3.8 + j * 4.4, y0 + 5 + (j % 3))]
                     for j in range(int(2 * half / 4.4))])
    # the slag bowl, frozen against the floor, and the bloom sitting in its pool below the tuyere
    d.line((cx - bore, floor - 6), (cx - bore * 0.5, floor - 10), (cx, floor - 11), (cx + bore * 0.5, floor - 10), (cx + bore, floor - 6))
    d.line(*_blob(cx + 4, ty + 18, bore * 0.62, 11, seed=0.7), closed=True)
    d.line((cx - bore + 1, ty + 4), (cx + bore - 1, ty + 4))           # the top of the liquid slag
    # slag running out of the tap arch to the left
    d.line((cx - bore, floor - 4), (cx - bore - wall - 6, floor - 2), (cx - bore - wall - 20, floor))
    # the air: arrows down the tuyere into the hot zone
    d.line((xo - 4, ty - 4.4), (cx + bore - 2, ty + 0.4))
    d.line((cx + bore + 4, ty - 3.2), (cx + bore - 2, ty + 0.4), (cx + bore + 4.6, ty + 2.6))
    # the temperature up the shaft: Sauder and Williams's two readings, 1,000-1,050 °C in the stack
    # 400 mm above the tuyere and 1,450-1,650 °C seen through the tuyere, joined by a smooth curve
    # (an exponential through the two, schematic above them)
    k = 400 / math.log(650 / 125)
    curve = [(T(900 + 650 * math.exp(-(ty - top) * i / 40 / s / k)), ty - (ty - top) * i / 40) for i in range(41)]
    d.line(*curve)
    d.circle(T(1025), ty - 400 * s, 2.5)
    d.circle(T(1550), ty, 2.5)
    d.group('mid')
    d.text(cx, top - 22, 'BLOOMERY IN SECTION', size=8)
    d.text(cx + bore + wall + 38, ty - 14, 'TUYERE', size=8, anchor='start')
    d.text(cx - bore - wall - 4, top + 40, 'ORE AND', size=8, anchor='end')
    d.text(cx - bore - wall - 4, top + 51, 'CHARCOAL', size=8, anchor='end')
    d.text(cx - bore - wall - 4, ty + 22, 'BLOOM', size=8, anchor='end')
    d.text(cx - bore - wall - 20, floor + 12, 'SLAG', size=8, anchor='start')
    d.text(T(1538) + 3, top + 4, '1538', size=8, anchor='start')
    d.text(T(1146) - 3, top + 4, '1146', size=8, anchor='end')
    d.text((gx0 + gx1) / 2, floor + 16, '°C', size=8)
    d.text((gx0 + gx1) / 2, top - 22, 'HEAT UP THE SHAFT', size=8)
    return d


PLATES['bloomery'] = bloomery


def _ell(cx, cy, rx, ry, a0=0, a1=360, n=48, flip=1):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + flip * ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def lost_wax():
    """A cored mace head of the Nahal Mishmar kind, in section, at four stages: the wax on its core,
    the mould built over it, the wax burned out with the mould upside down, and the pour.
    Sized after Rose, Fabian and Goren's 2023 reconstruction: a core about 47 mm across with an
    18 mm shaft hole, 3-5 mm of wax, and a mould 10-19 mm thick."""
    d = D()
    s = 1.05                                    # px per mm
    R, H = 27 * s, 23 * s                       # the wax model's outer half-width and half-height
    rc, hc = 23.5 * s, 20 * s                   # the core
    hole = 9 * s                                # half the shaft hole
    mould = 13 * s                              # mould thickness
    cxs = [52, 148, 248, 346]
    cy = 150
    up = [1, 1, -1, 1]                          # the third stage stands on its head

    d.group('thin')
    d.line((14, cy + 92), (390, cy + 92))                     # a common ground line
    for cx in cxs:
        d.line((cx, cy - 84), (cx, cy + 84))                  # each stage's axis
    for x in (100, 198, 297):
        d.line((x, 34), (x, cy + 88))                         # panel dividers
    d.group()
    for k, cx in enumerate(cxs):
        f = up[k]
        top = cy - f * (H + 14 * s)                           # where the sprue meets the cup
        if k == 0:
            # the wax model: an egg of wax over the core, a wax sprue to a cup on top
            d.line(*_ell(cx, cy, R, H), closed=True)
            d.line((cx - 3, cy - H), (cx - 3, top), (cx - 8, top - 8), (cx + 8, top - 8), (cx + 3, top), (cx + 3, cy - H))
        else:
            # the mould: an outer shell following the model at a distance, opening into the pouring cup
            o = _ell(cx, cy, R + mould, H + mould, -90 + 8, 270 - 8, n=60)
            if f < 0:
                o = [(x, 2 * cy - y) for x, y in o]
            ct = cy - f * (H + mould + 10)                    # the cup's mouth
            d.line(*o)
            d.line(o[0], (cx + 4, cy - f * (H + mould)), (cx + 12, ct))
            d.line(o[-1], (cx - 4, cy - f * (H + mould)), (cx - 12, ct))
            # the cavity left by the wax (stages 3, 4) or the wax itself (stage 2)
            d.line(*_ell(cx, cy, R, H), closed=True)
            d.line((cx - 3, cy - f * H), (cx - 3, cy - f * (H + mould)))
            d.line((cx + 3, cy - f * H), (cx + 3, cy - f * (H + mould)))
        # the core, with its shaft hole through it
        d.line(*_ell(cx, cy, rc, hc, -90 + 24, 90 - 24, n=24))
        d.line(*_ell(cx, cy, rc, hc, 90 + 24, 270 - 24, n=24))
        d.line((cx - hole, cy - hc * 0.9), (cx - hole, cy + hc * 0.9))
        d.line((cx + hole, cy - hc * 0.9), (cx + hole, cy + hc * 0.9))
    d.group('mid')
    # stage 2: the mould's three layers, drawn as two inner contours
    for frac in (0.12, 0.55):
        d.line(*_ell(cxs[1], cy, R + mould * frac, H + mould * frac, -90 + 10, 270 - 10, n=50))
    # stage 3: heat below the upturned mould, and wax running out of the cup
    cx = cxs[2]
    flames = []
    for x0 in (cx - 36, cx - 22, cx + 22, cx + 36):
        flames.append([(x0 - 6, cy + 88), (x0 - 2, cy + 72), (x0 + 1, cy + 79), (x0 + 4, cy + 66), (x0 + 7, cy + 88)])
    d.lines(flames)
    d.lines([[(cx, cy + H + mould + 14 + 7 * j), (cx, cy + H + mould + 17 + 7 * j)] for j in range(3)])
    # stage 4: the crucible tipped over the cup, and the stream of metal
    cx = cxs[3]
    ct = cy - (H + mould + 10)
    cr = [(cx + 12, ct - 50), (cx + 32, ct - 40), (cx + 22, ct - 20), (cx + 2, ct - 30)]
    d.line(*cr, closed=True)
    d.line((cx + 2, ct - 30), (cx - 1, ct - 26), (cx, ct - 14), (cx, ct + 6))   # the lip and the stream
    d.line((cx + 32, ct - 40), (cx + 46, ct - 50))           # the tongs' handle
    # the metal filling the cavity: hatching between model and core
    hatch = []
    for j in range(-6, 7):
        y = cy + j * 3.6
        if abs(j * 3.6) < hc:
            xi = rc * math.sqrt(max(0, 1 - (j * 3.6 / hc) ** 2))
            xo = R * math.sqrt(max(0, 1 - (j * 3.6 / H) ** 2))
            for side in (-1, 1):
                hatch.append([(cx + side * xi, y), (cx + side * xo, y)])
    d.lines(hatch)
    d.group('mid')
    labels = ['WAX ON CORE', 'MOULD', 'BURN OUT', 'POUR']
    for k, cx in enumerate(cxs):
        d.text(cx, cy + 108, f'{k + 1} · {labels[k]}', size=8)
    d.text(cxs[0], cy + H + 14, 'CORE', size=8)
    d.text(cxs[3] - 8, ct - 40, 'METAL', size=8, anchor='end')
    return d


PLATES['lost-wax'] = lost_wax


def chinese_cast_iron():
    """Iron's melting point against its carbon: the line falling from 1,538 °C for pure iron to the
    eutectic, 1,146 °C at 4.3 % carbon (the figures of Liu et al. 2019), drawn straight between them,
    with the bloomery's and the blast furnace's working heats across it, the two analyses of the
    Cangzhou Lion marked on it, and a blast furnace tapping iron into a mould beside it."""
    d = D()
    x0, x1 = 44, 262                            # 0 % to 5 % carbon
    y0, y1 = 252, 52                            # 1,050 °C to 1,600 °C
    X = lambda c: x0 + c / 5 * (x1 - x0)
    Y = lambda t: y0 - (t - 1050) / 550 * (y0 - y1)
    d.group('thin')
    d.line((x0, y1 - 8), (x0, y0), (x1 + 6, y0))
    for c in range(1, 6):
        d.line((X(c), y0), (X(c), y0 + 4))
    for t in (1100, 1200, 1300, 1400, 1500, 1600):
        d.line((x0 - 4, Y(t)), (x0, Y(t)))
    d.line((x0, Y(1538)), (X(0.5), Y(1538)))                  # pure iron's melting point
    d.line((x0, Y(1146)), (x1, Y(1146)))                      # the eutectic temperature
    d.line((X(4.3), Y(1146)), (X(4.3), y0))                   # the eutectic composition
    d.line((X(2.11), Y(1146) - 6), (X(2.11), y0))             # where cast iron begins
    d.group()
    # the liquidus: above it the iron is all liquid
    d.line((X(0), Y(1538)), (X(4.3), Y(1146)))
    d.group('mid')
    # the furnaces' working heats, about 1,200 °C and about 1,400 °C, as bands with ticks
    for t in (1200, 1400):
        d.lines([[(X(c), Y(t)), (X(c + 0.12), Y(t))] for c in [i * 0.2 for i in range(25)]])
    # where each furnace's line meets the liquidus: the least carbon that melts at that heat
    for t in (1200, 1400):
        c = (1538 - t) / (1538 - 1146) * 4.3
        d.circle(X(c), Y(t), 2.6)
    # the Cangzhou Lion's two analyses, 3.96 % and 4.3 % carbon
    for c in (3.96, 4.3):
        d.line((X(c) - 3, Y(1146) - 9), (X(c), Y(1146) - 4), (X(c) + 3, Y(1146) - 9))
    # a blast furnace in section, tapping iron down a channel into an open mould
    fx, fb = 348, 226                           # the furnace's axis and hearth floor
    d.group()
    d.line((fx - 18, 74), (fx - 30, fb), (fx - 30, fb + 12), (fx + 30, fb + 12), (fx + 30, fb), (fx + 18, 74))
    d.line((fx - 18, 74), (fx - 12, 74))
    d.line((fx + 12, 74), (fx + 18, 74))
    d.group('mid')
    d.line((fx + 30, fb - 26), (fx + 46, fb - 31))           # the tuyere from the bellows
    d.line((fx + 30, fb - 20), (fx + 46, fb - 25))
    d.line((fx - 22, fb - 4), (fx + 22, fb - 4))               # the pool of molten iron
    d.line((fx - 30, fb + 6), (fx - 44, fb + 16), (fx - 48, fb + 16))   # the tap channel
    d.line((fx - 66, fb + 16), (fx - 66, fb + 26), (fx - 40, fb + 26), (fx - 40, fb + 16))   # the mould
    d.line((fx - 64, fb + 22), (fx - 42, fb + 22))                       # iron in the mould
    for k in range(6):                                         # the charge, in layers
        y = 86 + k * 20
        w = 18 + (y - 74) / (fb - 74) * 12 - 3
        d.line((fx - w, y), (fx + w, y))
    d.group('mid')
    d.text(x0 - 6, Y(1538) + 3, '1538', size=8, anchor='end')
    d.text(x0 - 6, Y(1146) + 3, '1146', size=8, anchor='end')
    d.text(X(4.3), y0 + 14, '4.3', size=8)
    d.text(X(2.11), y0 + 14, '2.1', size=8)
    d.text((x0 + x1) / 2, y0 + 30, '% CARBON IN IRON', size=8)
    d.text(X(4.95), Y(1200) - 5, 'BLOOMERY', size=8, anchor='end')
    d.text(X(4.95), Y(1400) - 5, 'BLAST FURNACE', size=8, anchor='end')
    d.text(x0, y1 - 14, '°C', size=8)
    return d


PLATES['chinese-cast-iron'] = chinese_cast_iron
