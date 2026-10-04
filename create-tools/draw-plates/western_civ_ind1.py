"""Plates for western-civ's part ind1 (sprint 049): beethoven-ninth, serial-novel, factory-city.
See plates_for.py."""
import math
from plates import D


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def beethoven_ninth():
    d = D()
    # Top: the four movements to scale by a typical performance (Wikipedia: about 15, 14 with repeats,
    # 15 and 25 minutes). Middle: the finale's 940 bars as Nicholas Cook's table divides them.
    # Bottom: the first four bars of the "Joy" theme on a staff (treble clef positions), as the low
    # strings first play it at bar 92 (an octave and more lower).
    x0, x1 = 30, 370
    mins = [15, 14, 15, 25]
    forms = ['SONATA', 'SCHERZO', 'VARIATIONS', 'FINALE']
    total = sum(mins)
    sx = (x1 - x0) / total
    ty, th = 34, 26
    fy, fh = 128, 18
    bars = 940
    bx = (x1 - x0) / bars
    # Cook's divisions: (bar, key)
    cuts = [(1, 'd'), (92, 'D'), (208, 'd'), (241, 'D'), (331, 'B♭'), (431, ''), (543, 'D'),
            (595, 'G'), (627, 'g'), (655, 'D'), (730, ''), (745, ''), (763, 'D')]
    voice_from = 208
    X = lambda b: x0 + (b - 1) * bx

    d.group('thin')
    for m in list(range(0, total, 5)) + [total]:                             # a scale of minutes
        x = x0 + m * sx
        d.line((x, ty - 8), (x, ty - 4))
    d.line((x0, ty - 6), (x1, ty - 6))
    x_iv = x0 + sum(mins[:3]) * sx
    d.line((x_iv, ty + th), (x0, fy))                                       # the finale, enlarged
    d.line((x1, ty + th), (x1, fy))
    for b in range(100, bars + 1, 100):                                      # a scale of bars
        d.line((X(b), fy + fh + 4), (X(b), fy + fh + 8))
    d.line((x0, fy + fh + 6), (X(bars), fy + fh + 6))
    sy0 = 214                                                                # the staff
    for i in range(5):
        d.line((x0 + 60, sy0 + i * 7), (x1 - 20, sy0 + i * 7))

    d.group()
    x = x0
    for m in mins:
        _box(d, x, ty, m * sx, th)
        x += m * sx
    _box(d, x0, fy, x1 - x0, fh)

    d.group('mid')
    for b, _ in cuts[1:]:                                                    # the finale's sections
        d.line((X(b), fy), (X(b), fy + fh))
    d.line((X(voice_from), fy - 10), (X(bars), fy - 10))                    # voices from bar 208
    d.line((X(voice_from), fy - 13), (X(voice_from), fy - 7))
    d.line((X(bars), fy - 13), (X(bars), fy - 7))
    # the Joy theme, bars 1-4: F# F# G A | A G F# E | D D E F# | F#. E E
    # staff positions: bottom line E4 = 0, each step = half a space
    notes = [('F', 1), ('F', 1), ('G', 2), ('A', 3), ('A', 3), ('G', 2), ('F', 1), ('E', 0),
             ('D', -1), ('D', -1), ('E', 0), ('F', 1), ('F', 1), ('E', 0), ('E', 0)]
    durs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.5, 0.5, 2]
    nx0, nx1 = x0 + 78, x1 - 34
    slots = [max(du, 1) for du in durs]                                      # spacing, not strict time
    step = (nx1 - nx0) / sum(slots)
    bottom = sy0 + 28
    t = 0
    for i, ((_, pos), du) in enumerate(zip(notes, durs)):
        cx = nx0 + (t + 0.5) * step
        cy = bottom - pos * 3.5
        d.ellipse(cx, cy, 3.4, 2.4)
        d.line((cx + 3.2, cy), (cx + 3.2, cy - 20))                          # stem up
        if du == 1.5:
            d.circle(cx + 7, cy, 0.6)                                        # the dot
        if du == 0.5:
            d.line((cx + 3.2, cy - 20), (cx + 8, cy - 13))                   # the eighth's flag
        t += slots[i]
        if i in (3, 7, 11):
            bx_ = nx0 + t * step
            d.line((bx_, sy0), (bx_, sy0 + 28))
    d.line((nx1 + 6, sy0), (nx1 + 6, sy0 + 28))
    d.line((x0 + 64, sy0), (x0 + 64, sy0 + 28))
    # the key signature: two sharps (F and C)
    d.line((x0 + 68, sy0 - 2), (x0 + 68, sy0 + 6))
    d.line((x0 + 71, sy0 - 3), (x0 + 71, sy0 + 5))
    d.line((x0 + 66, sy0 + 1), (x0 + 73, sy0))
    d.line((x0 + 66, sy0 + 4), (x0 + 73, sy0 + 3))
    d.line((x0 + 74, sy0 + 8), (x0 + 74, sy0 + 16))
    d.line((x0 + 77, sy0 + 7), (x0 + 77, sy0 + 15))
    d.line((x0 + 72, sy0 + 11), (x0 + 79, sy0 + 10))
    d.line((x0 + 72, sy0 + 14), (x0 + 79, sy0 + 13))

    d.group('mid')
    x = x0
    for i, (m, fm) in enumerate(zip(mins, forms)):
        d.text(x + m * sx / 2, ty + 11, 'I II III IV'.split()[i], size=7)
        d.text(x + m * sx / 2, ty + 21, fm, size=7)
        x += m * sx
    d.text(x0, ty - 12, '0', size=7, anchor='start')
    d.text(x1, ty - 12, f'{total} MIN', size=7, anchor='end')
    for b, k in cuts:
        if k:
            d.text(X(b) + 2, fy + 12, k, size=7, anchor='start')
    for b in (92, 208, 331, 595, 763):
        d.text(X(b), fy + fh + 18, str(b), size=7)
    d.text(X(bars), fy + fh + 18, '940', size=7, anchor='end')
    d.text((X(voice_from) + X(bars)) / 2, fy - 16, 'VOICES', size=7)
    d.text(x0, sy0 + 13, 'JOY', size=7, anchor='start')
    d.text(200, 286, 'FOUR MOVEMENTS · THE FINALE IN BARS · ITS THEME', size=7)
    return d


PLATES = {'beethoven-ninth': beethoven_ninth}


def serial_novel():
    d = D()
    # Left: one printed sheet folded three times, the way an octavo was made: 16 pages to a sheet,
    # so a 24-page number was "a sheet and a half" (Chapman, in Forster's Life). Drawn as the flat
    # sheet with its fold lines, and beside it the folded gathering of 16 leaves' edges.
    # Right: the calendar of Pickwick's numbers, April 1836 to November 1837 (20 months; no number in
    # June 1837; the last a double), with Forster's two print figures on a log scale: part I, 400;
    # part XV, over 40,000.
    sx0, sy0, sw, sh = 22, 50, 150, 112                      # the flat sheet
    d.group('thin')
    d.line((sx0 + sw / 2, sy0 - 8), (sx0 + sw / 2, sy0 + sh + 8))     # first fold
    d.line((sx0 - 8, sy0 + sh / 2), (sx0 + sw + 8, sy0 + sh / 2))     # second fold
    for k in (1, 3):
        d.line((sx0 + k * sw / 4, sy0 - 4), (sx0 + k * sw / 4, sy0 + sh + 4))  # third fold
    # the log scale for the print runs
    cx0, cx1, cy = 236, 384, 212
    cw = (cx1 - cx0) / 20
    ly = lambda v: cy - 16 - (math.log10(v) - 2) * 32               # 100 at the base, 100,000 at the top
    for e in range(2, 6):
        d.line((cx0 - 4, ly(10 ** e)), (cx1, ly(10 ** e)))

    d.group()
    _box(d, sx0, sy0, sw, sh)
    # the folded gathering, in perspective below the sheet
    gx, gy, gw, gh = sx0 + 40, sy0 + sh + 28, sw / 4, sh / 2
    _box(d, gx, gy, gw, gh)
    for i in range(1, 8):
        d.line((gx + gw + i * 1.6, gy + i * 1.6), (gx + gw + i * 1.6, gy + gh + i * 1.6),
               (gx + i * 1.6, gy + gh + i * 1.6))
    # the calendar strip
    for i in range(20):
        _box(d, cx0 + i * cw, cy, cw, 12)

    d.group('mid')
    # page panels on the sheet: 4 across, 2 down, each a page with its text block
    pw, ph = sw / 4, sh / 2
    for r in range(2):
        for c in range(4):
            x, y = sx0 + c * pw, sy0 + r * ph
            d.line((x + 7, y + 9), (x + pw - 7, y + 9), (x + pw - 7, y + ph - 9), (x + 7, y + ph - 9), closed=True)
    # numbers issued: a tick in each month that had one; June 1837 (index 14) had none;
    # the last (index 19) was the double number XIX-XX
    issued = [i for i in range(20) if i != 14]
    for i in issued:
        x = cx0 + (i + 0.5) * cw
        d.line((x, cy + 3), (x, cy + 9))
    d.line((cx0 + 19 * cw + 2, cy + 6), (cx0 + 20 * cw - 2, cy + 6))
    # Forster's print runs, part I and part XV (index 0 and 15)
    for i, v in ((0, 400), (15, 40000)):
        x = cx0 + (i + 0.5) * cw
        d.line((x, cy), (x, ly(v)))
        d.circle(x, ly(v), 2.2)

    d.group('mid')
    d.text(sx0 + sw / 2, sy0 - 14, 'ONE SHEET · 8 PAGES A SIDE', size=7)
    d.text(sx0 + sw / 2, gy + gh + 22, 'FOLDED THRICE · 16 PAGES', size=7)
    d.text(sx0 + sw / 2, gy + gh + 34, 'A NUMBER · 1½ SHEETS', size=7)
    for e, s in ((2, '100'), (3, '1,000'), (4, '10,000'), (5, '100,000')):
        d.text(cx0 - 9, ly(10 ** e) + 2.5, s, size=7, anchor='end')
    d.text(cx0 + 0.5 * cw + 5, ly(400) - 5, '400', size=7, anchor='start')
    d.text(cx0 + 15.5 * cw - 5, ly(40000) - 6, '40,000', size=7, anchor='end')
    d.text(cx0 + 0.5 * cw, cy + 24, 'I', size=7)
    d.text(cx0 + 15.5 * cw, cy + 24, 'XV', size=7)
    d.text(cx0 + 19.5 * cw, cy + 24, 'XX', size=7)
    d.text(cx0, cy + 38, 'APR 1836', size=7, anchor='start')
    d.text(cx1, cy + 38, 'NOV 1837', size=7, anchor='end')
    d.text((cx0 + cx1) / 2, 286, 'COPIES PRINTED · FORSTER', size=7)
    return d


PLATES['serial-novel'] = serial_novel


def factory_city():
    d = D()
    # A steam cotton mill in section, as the Cotton mill article describes the early nineteenth-century
    # type: a low-pressure beam engine (48 hp on average in 1835) in an engine house, a main vertical
    # shaft with bevel gears to a horizontal line shaft on each floor, and belts down to the machines.
    # Floors drawn about 3 m apart (2.75-3.3 m in the source); five stories.
    gy = 262                                       # ground
    fh = 40                                        # floor height
    nf = 5
    mx0, mx1 = 118, 386                            # mill walls
    top = gy - nf * fh
    sx = 132                                       # the vertical shaft
    # engine house
    fx, fy, fr = 64, gy - 34, 26                   # flywheel
    piv = (64, 140)                                # beam pivot
    beam_l, beam_r = 24, 104
    cyl_x = 30

    d.group('thin')
    for k in range(nf + 1):                        # floor levels
        d.line((mx0 - 8, gy - k * fh), (mx1 + 8, gy - k * fh))
    d.line((sx, gy + 8), (sx, top - 8))           # shaft axis
    d.line((fx - fr - 8, fy), (sx + 6, fy))       # flywheel axis to the shaft
    d.line((beam_l, piv[1]), (beam_r, piv[1]))    # beam at mid-stroke
    for a in range(0, 360, 30):                   # spokes' construction
        d.line((fx, fy), (fx + fr * math.cos(math.radians(a)), fy + fr * math.sin(math.radians(a))))

    d.group()
    # the mill: walls and roof
    d.line((mx0, gy), (mx0, top), (mx1, top), (mx1, gy))
    d.line((mx0 - 4, top), ((mx0 + mx1) / 2, top - 18), (mx1 + 4, top))
    # engine house and chimney
    d.line((14, gy), (14, 112), (mx0, 112))
    d.line((4, gy), (4, 70), (12, 70), (12, 112))
    # the beam engine: beam, pivot column, cylinder, connecting rod, flywheel
    d.line((beam_l, piv[1] - 3), (beam_r, piv[1] - 3), (beam_r, piv[1] + 3), (beam_l, piv[1] + 3), closed=True)
    d.line((piv[0] - 5, gy), (piv[0], piv[1] + 3), (piv[0] + 5, gy))
    _box(d, cyl_x - 8, gy - 70, 16, 44)
    d.line((cyl_x, gy - 70), (cyl_x, piv[1] + 3))                     # piston rod
    d.line((beam_r, piv[1] + 3), (fx + fr * 0.55, fy - 4))            # connecting rod to the crank
    d.circle(fx, fy, fr)
    d.circle(fx, fy, 3)
    # the vertical shaft
    d.line((sx, gy - 4), (sx, top + 6))

    d.group('mid')
    # bevel gears and a line shaft with pulleys on each floor, belts down to a machine
    gear = lambda x, y, w, h: d.line((x - w, y - h), (x + w, y - h), (x + w * 0.6, y + h), (x - w * 0.6, y + h), closed=True)
    gear(sx, fy, 6, 3)
    d.circle(sx - 0.5, fy, 2)
    for k in range(nf):
        floor = gy - k * fh
        ceil = floor - fh + 6
        gear(sx, ceil, 5, 2.5)
        d.line((sx + 5, ceil), (mx1 - 8, ceil))                        # line shaft
        for i, px in enumerate(range(sx + 40, mx1 - 20, 64)):
            d.circle(px, ceil, 3.5)                                   # pulley
            mw = 44
            d.line((px - 3, ceil + 3), (px - 8, floor - 14))          # belt
            d.line((px + 3, ceil + 3), (px + 8, floor - 14))
            # a mule: headstock and carriage in outline
            _box(d, px - mw / 2, floor - 14, mw, 11)
            d.line((px - mw / 2 + 4, floor - 3), (px - mw / 2 + 4, floor))
            d.line((px + mw / 2 - 4, floor - 3), (px + mw / 2 - 4, floor))
    # the flywheel's drive to the shaft
    d.line((fx, fy), (sx - 6, fy))

    d.group('mid')
    d.text(fx, gy + 14, 'BEAM ENGINE', size=7)
    d.text(fx, gy + 24, '48 HP · 1835', size=7)
    d.text(sx, top - 24, 'MAIN SHAFT', size=7, anchor='middle')
    d.text((mx0 + mx1) / 2 + 30, gy + 14, 'LINE SHAFTS · MULES', size=7)
    return d


PLATES['factory-city'] = factory_city
