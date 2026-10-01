"""Plates for the chemistry subject's part alchemy3: type metal, Paracelsus and Agricola (sprint 025)."""
import math
from plates import D

R = 8.314
PB = (600.61, 4770.0, 207.2)      # melting point (K), heat of melting (J/mol), atomic weight
SB = (903.78, 19790.0, 121.76)


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _liquidus(x, metal):
    """Ideal-solution freezing point (K) of a metal present at mole fraction x."""
    tm, h, _ = metal
    return 1 / (1 / tm - R * math.log(x) / h)


def _x_sb(w):
    """Mole fraction of antimony from its weight fraction."""
    return (w / SB[2]) / (w / SB[2] + (1 - w) / PB[2])


def _eutectic():
    lo, hi = 1e-4, 0.9
    for _ in range(80):
        m = (lo + hi) / 2
        if _liquidus(1 - m, PB) > _liquidus(m, SB):
            lo = m
        else:
            hi = m
    x = lo
    w = x * SB[2] / (x * SB[2] + (1 - x) * PB[2])
    return w, _liquidus(1 - x, PB) - 273.15


def type_metal():
    """The lead-antimony phase diagram from ideal-solution liquidus curves, and a piece of type in elevation."""
    d = D()
    x0, x1, y0, y1 = 46, 286, 246, 36          # plot box: 0-100 % antimony, 150-700 degrees C
    t0, t1 = 150, 700
    X = lambda w: x0 + (x1 - x0) * w
    Y = lambda t: y0 - (y0 - y1) * (t - t0) / (t1 - t0)
    we, te = _eutectic()
    d.group('thin')
    for t in (200, 300, 400, 500, 600, 700):
        d.line((x0, Y(t)), (x1, Y(t)))
    for w in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        d.line((X(w), y0), (X(w), y0 + 4))
    d.line((X(we), Y(te)), (X(we), y0))
    d.group()
    d.line((x0, y1 - 6), (x0, y0), (x1, y0), (x1, y1 - 6))
    # the two liquidus curves, each metal's freezing point falling as the other dissolves in it
    pb = [(X(i * we / 60), Y(_liquidus(1 - _x_sb(i * we / 60 + 1e-9), PB) - 273.15)) for i in range(61)]
    sb = [(X(we + i * (1 - we) / 80), Y(_liquidus(_x_sb(we + i * (1 - we) / 80) - 1e-12, SB) - 273.15))
          for i in range(81)]
    d.line(*pb)
    d.line(*sb)
    d.line((x0, Y(te)), (x1, Y(te)))           # the eutectic line: below it, all solid
    d.group('mid')
    d.circle(X(we), Y(te), 3)
    d.line((X(0.13) - 3.5, Y(247) - 3.5), (X(0.13) + 3.5, Y(247) + 3.5))   # measured, 1936: 13 %, 247 C
    d.line((X(0.13) - 3.5, Y(247) + 3.5), (X(0.13) + 3.5, Y(247) - 3.5))
    # a piece of type, drawn in elevation beside the diagram: body, shoulder, face, nick and foot groove
    sx, sw, top, foot = 322, 34, 70, 246
    d.group()
    d.line((sx, foot), (sx, top + 14), (sx + 6, top + 6), (sx + 6, top), (sx + sw - 6, top),
           (sx + sw - 6, top + 6), (sx + sw, top + 14), (sx + sw, foot), closed=True)
    d.group('mid')
    d.line((sx + sw / 2 - 5, foot), (sx + sw / 2, foot - 8), (sx + sw / 2 + 5, foot))       # the groove
    d.arc(sx + sw, 196, 4, 90, 270, n=12)                                                  # the nick
    d.group('thin')
    d.line((sx + sw + 12, top), (sx + sw + 12, foot))
    d.line((sx + sw + 8, top), (sx + sw + 16, top))
    d.line((sx + sw + 8, foot), (sx + sw + 16, foot))
    d.group('mid')
    for t in (200, 300, 400, 500, 600, 700):
        d.text(x0 - 6, Y(t) + 3, str(t), size=7, anchor='end')
    for w in (0, 20, 40, 60, 80, 100):
        d.text(X(w / 100), y0 + 14, str(w), size=7)
    d.text((x0 + x1) / 2, y0 + 28, '% ANTIMONY BY WEIGHT', size=7)
    d.text(x0 + 4, Y(327) - 6, 'Pb 327', size=8, anchor='start')
    d.text(x1 - 4, Y(631) - 8, 'Sb 631', size=8, anchor='end')
    d.text(X(0.5), Y(560), 'LIQUID', size=8)
    d.text(X(we) + 30, Y(te) + 16, f'{te:.0f} °C · {we * 100:.1f} %', size=7, anchor='start')
    d.text(x0 - 6, y1 - 12, '°C', size=7, anchor='end')
    d.text(sx + sw / 2 + 6, foot + 14, '25 mm HIGH', size=7)
    d.text(sx + sw / 2 + 6, top - 10, 'TYPE', size=7)
    return d


def paracelsus():
    """White arsenic fired with saltpetre in a crucible, and the doses on a log scale: his drachm and his ten pounds."""
    d = D()
    # the furnace and crucible, in section
    cx, fy = 118, 132                           # crucible axis; the grate
    d.group('thin')
    d.line((cx, 22), (cx, 170))
    d.line((40, 170), (196, 170))
    d.group()
    d.line((58, 170), (58, 60), (178, 60), (178, 170))           # furnace walls
    d.line((50, 170), (50, 52), (186, 52), (186, 170))
    d.line((58, fy), (178, fy))                                  # grate
    top_w, bot_w, h = 46, 30, 52
    d.line((cx - top_w / 2, fy - h), (cx - bot_w / 2, fy), (cx + bot_w / 2, fy), (cx + top_w / 2, fy - h))
    d.group('mid')
    d.line((cx - top_w / 2 + 5, fy - h + 16), (cx + top_w / 2 - 5, fy - h + 16))   # the melt's surface
    for x in (74, 94, 142, 162):                                                   # coals under the grate
        d.circle(x, fy + 16, 7)
    for x in (82, 118, 154):
        d.circle(x, fy + 30, 6)
    # fumes of NO and NO2 rising from the melt, as damped sine waves
    for k, x0 in enumerate((cx - 10, cx, cx + 10)):
        pts = [(x0 + 5 * math.sin(i / 3 + k) * (1 - i / 60), fy - h - 2 - i * 1.3) for i in range(0, 40)]
        d.line(*pts)
    # the log dose scale, mg per kg of a 500 kg horse, as white arsenic
    x0, x1, lo, hi = 40, 372, -1, 5
    X = lambda v: x0 + (x1 - x0) * (math.log10(v) - lo) / (hi - lo)
    ya, yb = 222, 256                             # the arsenite row and the arsenate row
    d.group('thin')
    for e in range(lo, hi + 1):
        d.line((X(10 ** e), 238), (X(10 ** e), 268))
        for m in range(2, 10):
            if e < hi:
                d.line((X(m * 10 ** e), 266), (X(m * 10 ** e), 268))
    d.group()
    d.line((x0, 268), (x1, 268))
    # lethal bands: arsenite 1-25 mg/kg (Merck); arsenate four to ten times less toxic, 4-250
    for y, a, b in ((ya, 1, 25), (yb, 4, 250)):
        d.line((X(a), y - 5), (X(b), y - 5), (X(b), y + 5), (X(a), y + 5), closed=True)
    d.group('mid')
    drachm = 3890 / 500
    pounds = 960 * drachm
    for y, v in ((ya, drachm), (yb, pounds)):
        d.line((X(v), y - 12), (X(v), y + 12))
        d.line((X(v) - 4, y - 16), (X(v), y - 12), (X(v) + 4, y - 16))
    d.group('mid')
    for e in range(lo, hi + 1):
        d.text(X(10 ** e), 280, f'{10 ** e:g}', size=7)
    d.text(x1, 294, 'mg PER kg', size=7, anchor='end')
    d.text(X(drachm) + 8, ya - 10, '1 DRACHM', size=7, anchor='start')
    d.text(X(pounds), yb - 22, '10 POUNDS', size=7)
    d.text(x0, ya - 8, 'As₂O₃', size=7, anchor='start')
    d.text(x0, yb - 8, 'ARSENATE', size=7, anchor='start')
    d.text(290, 90, 'As₂O₃ + 2 KNO₃', size=8)
    d.text(290, 106, '→ 2 KAsO₃ + NO + NO₂', size=8)
    d.text(cx, 186, 'FIRED WITH SALTPETRE', size=7)
    return d


def agricola():
    """An assay furnace's muffle with its cupels, one cupel in section with the bead, and the lesser weights."""
    d = D()
    # the muffle furnace, in section: an arched muffle over the fire, cupels standing inside it
    mx, my, mw, mh = 110, 118, 128, 46        # the muffle's centre-bottom, width, height
    cyc0 = my - mh + mw / 2
    d.group('thin')
    d.line((mx, 20), (mx, 196))
    d.line((24, 176), (196, 176))
    d.group()
    d.line((30, 176), (30, 40), (190, 40), (190, 176))                  # the furnace
    r = mw / 2
    cyc = my - mh + r
    arc = [(mx + r * math.cos(math.radians(a)), cyc + r * math.sin(math.radians(a))) for a in range(180, 361, 5)]
    arc = [(x, min(y, my)) for x, y in arc]
    d.line((mx - r, my), *[p for p in arc if p[1] <= my], (mx + r, my))
    d.line((mx - r, my), (mx + r, my))
    d.group('mid')
    for x in (mx - 40, mx, mx + 40):                                     # three cupels on the muffle floor
        d.line((x - 14, my), (x - 11, my - 10), (x + 11, my - 10), (x + 14, my))
        d.arc(x, my - 10, 7, 0, 180, n=12, ry=3)
    for x in (58, 82, 110, 138, 162):                                   # charcoal packed over and round the muffle
        d.circle(x, my + 22, 7)
    for x in (70, 96, 124, 150):
        d.circle(x, my + 38, 6)
    # the cupel in section, large: ash body, the hollow, the bead, litharge soaking outward
    cx, cy, R = 300, 110, 50
    d.group('thin')
    d.line((cx, cy - 60), (cx, cy + 36))
    for k in range(1, 4):                                               # soak fronts, spreading into the ash
        d.arc(cx, cy - 20, 22 + 9 * k, 20, 160, n=24, ry=(22 + 9 * k) * 0.55)
    d.group()
    d.line((cx - R - 10, cy + 30), (cx - R, cy - 20), (cx + R, cy - 20), (cx + R + 10, cy + 30), closed=True)
    d.arc(cx, cy - 20, 30, 0, 180, n=36, ry=18)
    d.group('mid')
    d.circle(cx, cy - 7, 4)                                             # the bead
    # the lesser weights: 100, 50, 25, 16, 8, 4, 2, 1 "pounds", each drawn with volume to scale
    xs = 44
    weights = (100, 50, 25, 16, 8, 4, 2, 1)
    d.group()
    for w in weights:
        s = 26 * (w / 100) ** (1 / 3)
        d.line((xs, 262), (xs, 262 - s), (xs + s, 262 - s), (xs + s, 262))
        d.ellipse(xs + s / 2, 262 - s, s / 2, s / 7)
        xs += s + 12
    d.group('thin')
    d.line((30, 262), (xs, 262))
    d.group('mid')
    xs = 44
    for w in weights:
        s = 26 * (w / 100) ** (1 / 3)
        d.text(xs + s / 2, 276, str(w), size=7)
        xs += s + 12
    d.text(mx, 32, 'ASSAY FURNACE AND MUFFLE', size=7)
    d.text(cx, 30, 'CUPEL OF ASH, IN SECTION', size=7)
    d.text(cx + 40, cy - 30, 'Ag', size=8, anchor='start')
    d.line((cx + 5, cy - 10), (cx + 37, cy - 30))
    d.text(cx, cy + 52, '2 Pb + O₂ → 2 PbO', size=8)
    d.text(cx, 190, 'LITHARGE SOAKS INTO THE ASH', size=7)
    d.text(xs + 4, 262, 'LESSER WEIGHTS', size=7, anchor='start')
    d.text(xs + 4, 274, '100 = 1 DRACHMA', size=7, anchor='start')
    return d


PLATES = {'type-metal': type_metal, 'paracelsus': paracelsus, 'agricola': agricola}
