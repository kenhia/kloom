"""Plates for western-civ's trail The idea of rights (sprint 049, part rights). See plates_for.py."""
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


def us_bill_of_rights():
    """Left: the Constitution as a column of its seven articles, with Madison's plan of June 1789
    (amendments inserted at Art. I s. 9, Art. I s. 10 and Art. III) against what was done (ten
    articles appended at the end). Right: the number of articles at each stage, one square each:
    about 20 proposed, 17 passed by the House, 12 by the Senate and Congress, 10 ratified in 1791,
    one more in 1992."""
    d = D()
    # the document: seven articles, Article I the longest (proportions are schematic)
    x0, w, top = 46, 70, 34
    heights = [62, 22, 22, 10, 8, 8, 6]                                   # Articles I-VII
    ys = [top]
    for h in heights:
        ys.append(ys[-1] + h + 3)
    app_top = ys[-1] + 10                                                 # the appended amendments
    app_h = 10 * 6

    d.group('thin')
    for y in ys[:-1]:                                                     # article rules, ruled across
        d.line((x0 - 6, y), (x0 + w + 6, y))
    d.line((x0 - 6, app_top), (x0 + w + 6, app_top))
    # the funnel's grid: one square per article, columns at each stage
    cols = [(175, 20), (225, 17), (275, 12), (325, 10), (365, 1)]
    s, gap, base = 7, 2.5, 262
    for cx, _ in cols:
        d.line((cx, 40), (cx, base + 4))
    d.line((160, base + 4), (382, base + 4))

    d.group()
    for i, h in enumerate(heights):                                       # the seven articles
        _box(d, x0, ys[i], w, h)
    _box(d, x0, app_top, w, app_h)                                        # the ten, appended

    d.group('mid')
    # lines of text inside each article
    for i, h in enumerate(heights):
        y = ys[i] + 4
        while y < ys[i] + h - 2:
            d.line((x0 + 6, y), (x0 + w - 6, y))
            y += 4
    for k in range(10):                                                   # ten amendments, a band each
        y = app_top + k * 6
        d.line((x0, y), (x0 + w, y))
        d.line((x0 + 6, y + 3), (x0 + w - 18, y + 3))
    # Madison's insertions, from the margin into the text: Art. I s. 9, Art. I s. 10, Art. III
    for y in (ys[0] + 40, ys[0] + 52, ys[2] + 12):
        d.line((x0 - 30, y), (x0 - 2, y))
        _arrow(d, (x0 - 30, y), (x0 - 2, y), 4)
    # the funnel: stacked squares, bottom up
    for cx, n in cols:
        for k in range(n):
            y = base - (k + 1) * (s + gap) + gap
            _box(d, cx - s / 2, y, s, s)
    for (ax, an), (bx, bn) in zip(cols[:-2], cols[1:-1]):                 # tops joined, falling
        ya = base - an * (s + gap) + gap
        yb = base - bn * (s + gap) + gap
        d.line((ax + s / 2, ya), (bx - s / 2, yb))

    d.group('mid')
    d.text(x0 + w / 2, top - 10, 'CONSTITUTION', size=7)
    d.text(x0 + w / 2, app_top + app_h + 12, 'I–X ADDED ON', size=7)
    d.text(x0 - 34, ys[0] + 24, 'WOVEN', size=7, anchor='start')
    d.text(x0 - 34, ys[0] + 34, 'IN', size=7, anchor='start')
    for (cx, n), lab in zip(cols, ['~20', '17', '12', '10', '+1']):
        d.text(cx, base - n * (s + gap) - 4, lab, size=7)
    for (cx, _), lab in zip(cols, ['JUN 89', 'HOUSE', 'SENATE', '1791', '1992']):
        d.text(cx, base + 16, lab, size=7)
    d.text(270, 30, 'ARTICLES AT EACH STAGE', size=7)
    return d


def vindication():
    """Two plans for a nation's schools, drawn on one axis of age. Above, Talleyrand's report of
    September 1791: primary schools from six, girls admitted only until eight and then sent home.
    Below, Wollstonecraft's chapter 12: free day schools for all from five to nine, girls and boys
    together; after nine two schools by destination (trades, or learning), the sexes still together."""
    d = D()
    def X(age):
        return 70 + (age - 4) * 25                                        # ages 4 to 16 across

    d.group('thin')
    for a in range(4, 17):                                                # the age axis and its ticks
        d.line((X(a), 268), (X(a), 272))
    d.line((X(4), 270), (X(16), 270))
    for a in (5, 6, 8, 9):                                                # the ages the plans turn on
        d.line((X(a), 40), (X(a), 124))
        d.line((X(a), 152), (X(a), 262))
    d.line((40, 132), (390, 132))                                         # the two plans divided

    d.group()
    # Talleyrand: boys' lane from six on, girls' lane six to eight
    yb, yg, h = 58, 92, 14
    d.line((X(6), yb), (X(16), yb), (X(16), yb + h), (X(6), yb + h), closed=True)
    d.line((X(6), yg), (X(8), yg), (X(8), yg + h), (X(6), yg + h), closed=True)
    # Wollstonecraft: one shared band five to nine, then two bands, each holding both lanes
    y0, H = 168, 30
    d.line((X(5), y0), (X(9), y0), (X(9), y0 + H), (X(5), y0 + H), closed=True)
    ya, yb2 = 156, 214
    for y in (ya, yb2):
        d.line((X(9), y), (X(16), y), (X(16), y + H), (X(9), y + H), closed=True)

    d.group('mid')
    # the girls sent home: a dashed run after eight
    x = X(8) + 4
    while x < X(16) - 4:
        d.line((x, yg + h / 2), (min(x + 6, X(16)), yg + h / 2))
        x += 11
    # lanes inside Wollstonecraft's bands: girls and boys side by side throughout
    for y in (y0, ya, yb2):
        x1 = X(5) if y == y0 else X(9)
        d.line((x1, y + H / 2), (X(16) if y != y0 else X(9), y + H / 2))

    d.group('mid')
    d.text(215, 26, 'TALLEYRAND · SEPTEMBER 1791', size=7)
    d.text(X(6) + 5, yb + 10, 'BOYS', size=7, anchor='start')
    d.text(X(6) + 5, yg + 10, 'GIRLS', size=7, anchor='start')
    d.text((X(8) + X(16)) / 2, yg + h + 12, 'GIRLS AT HOME', size=7)
    d.text(215, 146, 'WOLLSTONECRAFT · JANUARY 1792', size=7)
    d.text(X(5) - 6, y0 + 12, 'FREE', size=7, anchor='end')
    d.text(X(5) - 6, y0 + 22, 'TO ALL', size=7, anchor='end')
    d.text(X(7), y0 + 12, 'GIRLS', size=7)
    d.text(X(7), y0 + H - 4, 'BOYS', size=7)
    d.text((X(9) + X(16)) / 2 + 10, ya + 12, 'LANGUAGES · SCIENCE', size=7)
    d.text((X(9) + X(16)) / 2 + 10, yb2 + 12, 'TRADES · DOMESTIC', size=7)
    for a in (4, 6, 8, 10, 12, 14, 16):
        d.text(X(a), 284, str(a), size=7)
    d.text(215, 296, 'AGE', size=7)
    return d


def womens_suffrage():
    """The Cat and Mouse Act of April 1913 as a mechanism: four stations on a circle (prison,
    hunger strike, release on license, recovery outside), joined by arcs with arrowheads; the old
    remedy, force-feeding, as a spur off the strike. Below, one sentence as a schematic timeline:
    days served in prison solid, days out on licence open and not counted, so the sentence runs
    on (the proportions are illustrative, not one woman's record)."""
    d = D()
    cx, cy, R = 200, 112, 70
    stations = [(-90, 'PRISON'), (0, 'HUNGER STRIKE'), (90, 'RELEASED'), (180, 'RECOVERY')]
    bw, bh = 86, 22

    def pt(a, r=R):
        return (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))

    d.group('thin')
    for a, _ in stations:                                                 # radii from the act to each station
        inner = pt(a, 22)
        outer = pt(a, R - (bh / 2 if a in (-90, 90) else bw / 2))
        d.line(inner, outer)
    d.line((40, 248), (360, 248))                                         # the timeline's baseline

    d.group()
    for a, _ in stations:
        x, y = pt(a)
        d.line((x - bw / 2, y - bh / 2), (x + bw / 2, y - bh / 2), (x + bw / 2, y + bh / 2),
               (x - bw / 2, y + bh / 2), closed=True)
    # arcs between stations, clockwise, clear of the boxes, with arrowheads
    for a0 in (-90, 0, 90, 180):
        a1 = a0 + 90
        s, e = a0 + 24, a1 - 24
        pts = [pt(s + (e - s) * k / 16) for k in range(17)]
        d.line(*pts)
        _arrow(d, pts[-2], pts[-1], 5)
    # the sentence: in prison (solid), out on licence (open), again and again
    x = 40
    for days, inside in [(70, True), (40, False), (50, True), (45, False), (45, True), (30, False), (40, True)]:
        if inside:
            d.line((x, 236), (x + days, 236), (x + days, 248), (x, 248), closed=True)
        x += days

    d.group('mid')
    # force-feeding, the remedy the act replaced: a spur off the strike
    sx, sy = pt(0)
    d.line((sx + bw / 2, sy), (sx + bw / 2 + 22, sy))
    d.line((sx + bw / 2 + 22, sy - 30), (sx + bw / 2 + 22, sy + 30))
    x = 40
    for days, inside in [(70, True), (40, False), (50, True), (45, False), (45, True), (30, False), (40, True)]:
        if not inside:                                                    # days out, ticked but empty
            d.line((x, 242), (x + days, 242))
            for k in range(0, days + 1, 10):
                d.line((x + k, 239), (x + k, 245))
        x += days

    d.group('mid')
    for a, s in stations:
        x, y = pt(a)
        d.text(x, y + 2.5, s, size=7)
    d.text(sx + bw / 2 + 26, sy - 36, 'BEFORE 1913', size=7, anchor='start')
    d.text(sx + bw / 2 + 26, sy + 3, 'FORCE-', size=7, anchor='start')
    d.text(sx + bw / 2 + 26, sy + 13, 'FED', size=7, anchor='start')
    d.text(cx, cy + 3, 'ACT 1913', size=7)
    d.text(40, 228, 'ONE SENTENCE · DAYS OUT NOT COUNTED', size=7, anchor='start')
    d.text(40, 262, 'IN', size=7, anchor='start')
    d.text(110, 262, 'OUT', size=7, anchor='start')
    return d


PLATES = {'us-bill-of-rights': us_bill_of_rights, 'vindication': vindication, 'womens-suffrage': womens_suffrage}
