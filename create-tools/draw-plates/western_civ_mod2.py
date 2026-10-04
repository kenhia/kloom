"""Plates for western-civ's part mod2 (sprint 049): holocaust, udhr, fall-of-the-wall. See plates_for.py."""
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


def holocaust():
    """Left: the six killing centers in occupied Poland, placed by latitude and longitude on an
    equirectangular grid (longitude scaled by the cosine of 51.3 degrees), with three cities for
    reference. Right: the Hoefle telegram's cumulative 'arrivals' to 31 December 1942 for the four
    Operation Reinhard camps (L 24,733, B 434,508, S 101,370, T 713,555), bars to scale."""
    d = D()
    lon0, lon1, lat0, lat1 = 18.0, 24.0, 49.8, 53.0
    k = math.cos(math.radians(51.3))
    s = 218 / ((lon1 - lon0) * k)                                        # units per degree of latitude
    x0, y0 = 40, 46

    def P(lat, lon):
        return (x0 + (lon - lon0) * k * s, y0 + (lat1 - lat) * s)

    camps = [('CHEŁMNO', 52.156, 18.727, 'end'), ('TREBLINKA', 52.631, 22.052, 'middle'),
             ('SOBIBÓR', 51.447, 23.594, 'end'), ('BEŁŻEC', 50.372, 23.457, 'middle'),
             ('MAJDANEK', 51.220, 22.600, 'end'), ('AUSCHWITZ', 50.036, 19.178, 'middle')]
    cities = [('WARSAW', 52.230, 21.012), ('ŁÓDŹ', 51.759, 19.456), ('KRAKÓW', 50.061, 19.938)]

    d.group('thin')
    for lon in range(18, 25):                                            # meridians
        d.line(P(lat0, lon), P(lat1, lon))
    for lat in (50, 51, 52, 53):                                         # parallels
        d.line(P(lat, lon0), P(lat, lon1))
    bx, by, top = 286, 252, 72                                           # the chart's frame
    d.line((bx - 8, by), (392, by))
    for v in (0, 250000, 500000, 750000):
        y = by - v / 750000 * (by - top)
        d.line((bx - 8, y), (bx - 4, y))
    d.line((bx - 6, by), (bx - 6, top))

    d.group()
    for name, lat, lon, _ in camps:                                      # each camp: two rings
        x, y = P(lat, lon)
        d.circle(x, y, 4.5)
        d.circle(x, y, 1.5)
    hoefle = [('L', 24733), ('B', 434508), ('S', 101370), ('T', 713555)]
    for i, (_, v) in enumerate(hoefle):                                  # the telegram's bars
        x = bx + 4 + i * 26
        h = v / 750000 * (by - top)
        _box(d, x, by - h, 16, h)

    d.group('mid')
    for _, lat, lon in cities:
        x, y = P(lat, lon)
        _box(d, x - 2.5, y - 2.5, 5, 5)
    _box(d, x0, y0, (lon1 - lon0) * k * s, (lat1 - lat0) * s)

    d.group('mid')
    for name, lat, lon, anchor in camps:
        x, y = P(lat, lon)
        dx = {'end': -8, 'middle': 0}[anchor]
        dy = 14 if anchor == 'middle' else 3
        if name in ('TREBLINKA', 'AUSCHWITZ'):
            dy = -9
        d.text(x + dx, y + dy, name, size=7, anchor=anchor)
    for name, lat, lon in cities:
        x, y = P(lat, lon)
        d.text(x + 6, y + 3, name, size=7, anchor='start')
    for lat in (50, 52):
        x, y = P(lat, lon0)
        d.text(x - 3, y + 3, f'{lat}°N', size=7, anchor='end')
    for lon in (19, 21, 23):
        x, y = P(lat0, lon)
        d.text(x, y + 11, f'{lon}°E', size=7)
    for i, (c, v) in enumerate(hoefle):
        x = bx + 12 + i * 26
        d.text(x, by + 11, c, size=7)
    for v, lab in ((250000, '250K'), (500000, '500K'), (750000, '750K')):
        d.text(bx - 10, by - v / 750000 * (by - top) + 3, lab, size=7, anchor='end')
    d.text(334, top - 22, 'HÖFLE TELEGRAM', size=7)
    d.text(334, top - 12, 'TO 31 DEC 1942', size=7)
    d.text(x0 + (lon1 - lon0) * k * s / 2, y0 - 12, 'KILLING CENTERS · OCCUPIED POLAND', size=7)
    return d


def udhr():
    """Rene Cassin's figure of the Declaration as the portico of a Greek temple: seven steps (the
    preamble's seven paragraphs), a foundation (Articles 1-2), four columns (3-11, 12-17, 18-21,
    22-27) and an entablature with its pediment (28-30). Columns are drawn in Doric proportion, about
    5.5 lower diameters high, with an entasis computed as a gentle curve; the pediment rises at 13
    degrees, as in classical Greek temples."""
    d = D()
    cx = 200
    base_y = 270                                                          # ground line
    step_h, step_w0, step_in = 3.5, 316.0, 4.0                            # seven steps, each set in
    steps = [(cx - (step_w0 / 2 - i * step_in), base_y - (i + 1) * step_h,
              step_w0 - 2 * i * step_in) for i in range(7)]
    stylo_y = base_y - 7 * step_h                                        # top of the steps
    found_h = 14                                                          # the foundation course
    col_base = stylo_y - found_h
    dia = 26.0
    col_h = 5.5 * dia
    col_top = col_base - col_h
    span = 216                                                            # axis of first to last column
    xs = [cx - span / 2 + i * span / 3 for i in range(4)]
    arch_h, frieze_h, cornice_h = 12, 12, 6
    ent_top = col_top - 6 - arch_h - frieze_h - cornice_h
    ent_w = span + dia + 24
    pitch = math.tan(math.radians(13))
    apex = ent_top - pitch * ent_w / 2

    d.group('thin')
    d.line((cx, apex - 12), (cx, base_y + 8))                             # the axis
    for x in xs:                                                          # column axes, broken for labels
        d.line((x, col_top - 4), (x, col_base - col_h / 2 - 9))
        d.line((x, col_base - col_h / 2 + 5), (x, col_base + 4))
    d.line((cx - ent_w / 2 - 14, ent_top), (cx + ent_w / 2 + 14, ent_top))
    d.line((cx - ent_w / 2 - 14, base_y), (cx + ent_w / 2 + 14, base_y))
    r = 40                                                                # the pediment's angle
    d.arc(cx - ent_w / 2, ent_top, r, -13, 0, n=12)

    d.group()
    for x, y, w in steps:                                                 # the seven steps
        d.line((x, y + step_h), (x, y), (x + w, y), (x + w, y + step_h))
    d.line((steps[0][0], base_y), (steps[0][0] + steps[0][2], base_y))
    fw = steps[-1][2]
    _box(d, cx - fw / 2, col_base, fw, found_h)                           # the foundation
    for x in xs:                                                          # the columns, with entasis
        left, right = [], []
        n = 16
        for i in range(n + 1):
            u = i / n
            y = col_base - u * col_h
            half = dia / 2 * (1 - 0.18 * u) + 0.9 * math.sin(math.pi * u)
            left.append((x - half, y))
            right.append((x + half, y))
        d.line(*left)
        d.line(*right)
        top_half = dia / 2 * 0.82
        _box(d, x - top_half - 4, col_top - 6, 2 * top_half + 8, 6)       # abacus
    ex = cx - ent_w / 2
    _box(d, ex, col_top - 6 - arch_h, ent_w, arch_h)                      # architrave
    _box(d, ex, col_top - 6 - arch_h - frieze_h, ent_w, frieze_h)         # frieze
    _box(d, ex - 4, ent_top, ent_w + 8, cornice_h)                        # cornice
    d.line((ex - 4, ent_top), (cx, apex), (ex + ent_w + 4, ent_top))     # pediment

    d.group('mid')
    for i in (1, 2, 4, 5):                                                # joints of the foundation
        jx = cx - fw / 2 + i * fw / 6
        d.line((jx, col_base), (jx, col_base + found_h))
    for i in range(1, 9):                                                 # triglyphs on the frieze
        tx = ex + i * ent_w / 9
        d.line((tx, col_top - 6 - arch_h), (tx, col_top - 6 - arch_h - frieze_h))

    d.group('mid')
    d.text(cx, apex + (ent_top - apex) * 0.72, '28–30', size=7)
    d.text(cx, col_top - 6 - 3, 'ARTICLES', size=7)
    for x, lab in zip(xs, ('3–11', '12–17', '18–21', '22–27')):
        d.text(x, col_base - col_h / 2, lab, size=7)
    d.text(cx, col_base + 10, 'ARTICLES 1–2', size=7)
    d.text(cx - steps[0][2] / 2, base_y + 16, 'STEPS · PREAMBLE’S 7 PARAGRAPHS', size=7, anchor='start')
    d.text(cx - ent_w / 2 - 6, ent_top - 12, '13°', size=7, anchor='end')
    d.text(cx + steps[0][2] / 2, base_y + 16, 'CASSIN’S PORTICO', size=7, anchor='end')
    return d


def fall_of_the_wall():
    """A section through the Berlin border strip of the 1980s, West Berlin on the left. Heights are
    to scale at 16 units a meter, widths at 4 (heights shown four times), and the widths are
    schematic, since the strip ran from five to several hundred meters wide. Sourced dimensions: the
    border wall 3.6 m high (Border Wall 75, a precast retaining-wall element with a pipe on top), the
    outer strip up to 4 m, the patrol road 7 m. The rest (trench, lamps, tower, fence, inner wall)
    is drawn at plausible size and not dimensioned."""
    d = D()
    g = 244                                                               # ground line
    hx, vy = 4.0, 16.0                                                    # units per meter
    x0 = 30
    X = lambda m: x0 + m * hx
    H = lambda m: g - m * vy
    wall_m, trench_m, sand_m, lamp_m, road_m, tower_m, fence_m, inner_m = 4, 8, 14, 26, 28, 39, 47, 66

    d.group('thin')
    d.line((X(-3), g), (X(80), g))                                        # the ground
    d.line((X(wall_m) - 14, H(0)), (X(wall_m) - 14, H(3.6)))              # 3.6 m, dimensioned
    for y in (H(0), H(3.6)):
        d.line((X(wall_m) - 18, y), (X(wall_m) - 10, y))
    d.line((X(road_m), g + 8), (X(road_m + 7), g + 8))                    # 7 m road, dimensioned
    for m in (road_m, road_m + 7):
        d.line((X(m), g + 4), (X(m), g + 12))
    d.line((X(0), g - 80), (X(0), g + 12))                               # the legal border
    for i in range(4):                                                    # a scale of meters, vertical
        d.line((X(80) + 4, H(i)), (X(80) + 8, H(i)))
    d.line((X(80) + 6, H(0)), (X(80) + 6, H(3)))

    d.group()
    # the border wall: a slab 3.6 m high with an L-shaped foot toward the East, and a pipe on top
    wx = X(wall_m)
    d.line((wx, g), (wx, H(3.6) + 3), (wx + 4, H(3.6) + 3), (wx + 4, g - 3),
           (wx + 2.2 * hx, g - 3), (wx + 2.2 * hx, g))
    d.circle(wx + 2, H(3.6), 3.5)
    # the anti-vehicle trench
    tx = X(trench_m)
    d.line((tx, g), (tx + 1.0 * hx, g), (tx + 2.0 * hx, H(-1.2)), (tx + 3.2 * hx, H(-1.2)),
           (tx + 4.4 * hx, g))
    # the patrol road, as a slab
    d.line((X(road_m), g), (X(road_m), g - 3), (X(road_m + 7), g - 3), (X(road_m + 7), g))
    # the watchtower: a shaft and a cabin
    tw = X(tower_m)
    d.line((tw - 5, g), (tw - 4, H(7.0)), (tw + 4, H(7.0)), (tw + 5, g))
    d.line((tw - 9, H(7.0)), (tw - 9, H(9.0)), (tw + 9, H(9.0)), (tw + 9, H(7.0)), (tw - 9, H(7.0)))
    d.line((tw - 10, H(9.0)), (tw + 10, H(9.0)), (tw + 8, H(9.4)), (tw - 8, H(9.4)), closed=True)
    # the inner wall
    iw = X(inner_m)
    d.line((iw, g), (iw, H(3.0)), (iw + 3, H(3.0)), (iw + 3, g))

    d.group('mid')
    for m in range(sand_m, sand_m + 11):                                  # raked sand of the control strip
        d.line((X(m), g - 1.5), (X(m) + 2, g - 3))
    lx = X(lamp_m)                                                        # a lamp post, its arm toward the wall
    d.line((lx, g), (lx, H(5.0)), (lx - 8, H(5.0)))
    d.line((lx - 10, H(5.0) + 1), (lx - 6, H(5.0) + 1))
    fx = X(fence_m)                                                       # the signal fence on its posts
    for k in range(3):
        d.line((fx + k * 6, g), (fx + k * 6, H(2.0)))
    for y in (H(0.6), H(1.2), H(1.8)):
        d.line((fx, y), (fx + 12, y))
    for k in range(4):                                                    # the dog run's line
        d.line((X(fence_m - 6) + k * 4, g - 1), (X(fence_m - 6) + k * 4 + 2, g - 1))

    d.group('mid')
    d.text(X(-2), g - 86, 'WEST', size=7, anchor='start')
    d.text(X(80), g - 86, 'EAST', size=7, anchor='end')
    d.text(wx - 16, H(1.8) + 3, '3.6 M', size=7, anchor='end')
    d.text(X(road_m + 3.5), g + 22, 'ROAD 7 M', size=7)
    d.text(wx + 2, H(3.6) - 9, 'WALL', size=7)
    d.text(X(trench_m) + 9, g + 30, 'TRENCH', size=7)
    d.text(X(sand_m + 5), g - 12, 'SAND', size=7)
    d.text(tw, H(9.4) - 6, 'TOWER', size=7)
    d.text(fx + 6, H(2.0) - 6, 'SIGNAL FENCE', size=7)
    d.text(iw + 2, H(3.0) - 6, 'INNER WALL', size=7)
    d.text(X(40), g + 38, 'SECTION · HEIGHTS ×4 · WIDTHS SCHEMATIC', size=7)
    return d


PLATES = {'holocaust': holocaust, 'udhr': udhr, 'fall-of-the-wall': fall_of_the_wall}
