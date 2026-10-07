"""Plates for The Story of Life's part time1 (sprint 055): Steno, Cuvier, Lamarck. See plates_for.py."""
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


def _rot(p, o, deg):
    """Point p turned about o by deg degrees, clockwise on the page."""
    a = math.radians(deg)
    x, y = p[0] - o[0], p[1] - o[1]
    return (o[0] + x * math.cos(a) - y * math.sin(a), o[1] + x * math.sin(a) + y * math.cos(a))


def _tooth(d, cx, base, w, h):
    """A shark's tooth in outline: a triangular blade with finely serrated edges over a two-lobed root."""
    tip = (cx, base - h)
    left, right = (cx - w / 2, base), (cx + w / 2, base)
    pts = [left]
    for k in range(1, 8):                                                  # serrations up the left edge
        t = k / 8
        pts.append((left[0] + (tip[0] - left[0]) * t - 0.7 * (k % 2), left[1] + (tip[1] - left[1]) * t))
    pts.append(tip)
    for k in range(7, 0, -1):
        t = k / 8
        pts.append((right[0] + (tip[0] - right[0]) * t + 0.7 * (k % 2), right[1] + (tip[1] - right[1]) * t))
    pts += [right, (cx + w * 0.55, base + h * 0.12), (cx + w * 0.45, base + h * 0.28), (cx + w * 0.12, base + h * 0.24),
            (cx, base + h * 0.12), (cx - w * 0.12, base + h * 0.24), (cx - w * 0.45, base + h * 0.28),
            (cx - w * 0.55, base + h * 0.12)]
    d.line(*pts, closed=True)
    d.line((cx - w / 2, base), (cx + w / 2, base))                        # where the enamel meets the root


def _clip(p, q, poly):
    """The part of segment pq inside the convex polygon poly (Cyrus-Beck), or None."""
    t0, t1 = 0.0, 1.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = len(poly)
    area = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        nx, ny = (b[1] - a[1], a[0] - b[0]) if area > 0 else (a[1] - b[1], b[0] - a[0])  # outward normal
        num = nx * (p[0] - a[0]) + ny * (p[1] - a[1])
        den = nx * dx + ny * dy
        if abs(den) < 1e-12:
            if num > 0:
                return None
            continue
        t = -num / den
        if den > 0:
            t1 = min(t1, t)
        else:
            t0 = max(t0, t)
        if t0 > t1:
            return None
    return (p[0] + dx * t0, p[1] + dy * t0), (p[0] + dx * t1, p[1] + dy * t1)


def steno_fossils():
    d = D()
    # Steno's rules of strata (Prodromus, 1669) in one section: beds laid flat, older below (superposition);
    # a valley cut through them, the same beds sought on its far side (lateral continuity); beds fallen and
    # tilted beyond a fracture, which must once have lain level (original horizontality); a tooth enclosed
    # in a bed, hard before the mud around it. Schematic, not a section of a real place.
    top, base = 74, 234
    beds = [top + k * 32 for k in range(6)]                               # 74 … 234, five beds
    xl, vl0, vl1, vr1, vr0, fault = 52, 148, 180, 202, 234, 270
    floor = 186

    def side(x_top, x_bot, y):                                             # x on a valley side at depth y
        return x_top + (x_bot - x_top) * (y - top) / (floor - top)

    fault_foot = fault + 10
    tilt = [(fault, top + 18), (fault_foot, base), (372, base), (372, top + 52)]  # the fallen block
    deg = 24
    s = math.tan(math.radians(deg))

    d.group('thin')
    for y in beds[1:]:
        if y < floor:                                                      # the beds sought across the valley
            d.dashed((side(vl0, vl1, y), y), (side(vr0, vr1, y), y), dash=3, gap=3)
    d.line((xl - 14, base), (384, base))                                   # the floor of the section
    d.line((300, 150), (366, 150))                                         # the horizon, against a tilted bed
    d.arc(300, 150, 40, -deg, 0, n=12)
    d.line((xl - 22, top + 8), (xl - 22, base - 8))
    _arrow(d, (xl - 22, top + 8), (xl - 22, base - 8), size=4)

    d.group()
    d.line((xl, base), (xl, top), (vl0, top), (vl1, floor), (vr1, floor), (vr0, top), (fault, top),
           (fault_foot, base))
    d.line((fault, top + 18), (372, top + 52), (372, base))
    for y in beds[1:5]:
        x_fault = fault + (fault_foot - fault) * (y - top) / (base - top)
        if y < floor:
            d.line((xl, y), (side(vl0, vl1, y), y))
            d.line((side(vr0, vr1, y), y), (x_fault, y))
        else:
            d.line((xl, y), (x_fault, y))
    for k in range(-6, 8):                                                 # the fallen beds, dipping at deg
        c = 150 + k * 30
        seg = _clip((240, c - s * 60), (400, c + s * 100), tilt)
        if seg:
            d.line(*seg)

    d.group('mid')
    _tooth(d, 92, 192, 24, 19)
    for x, y in ((128, 156), (252, 124)):                                  # shells in the beds
        d.arc(x, y, 6, 180, 360, n=12)
        d.line((x - 6, y), (x + 6, y))
        for s2 in (-3, 0, 3):
            d.line((x, y), (x + s2, y - 5.5))
    for k in range(8):                                                     # sediment in the top bed
        d.line((62 + k * 11, 88 + (k % 3) * 4), (64 + k * 11, 88 + (k % 3) * 4))

    d.group('mid')
    d.text(100, 64, 'SUPERPOSITION', size=7)
    d.text(191, 64, 'CONTINUITY', size=7)
    d.text(322, 64, 'HORIZONTALITY', size=7)
    d.text(xl - 22, top - 6, 'YOUNGER', size=7)
    d.text(xl - 22, base + 13, 'OLDER', size=7)
    d.text(92, 228, 'TOOTH', size=7)
    d.text(200, 272, "STRATA IN SECTION · STENO'S PRODROMUS, 1669", size=7)
    return d


def _crown(d, cx, cy, w, h):
    """A molar's crown in plan: a long rounded outline, flatter at the sides."""
    pts = []
    for k in range(48):
        a = 2 * math.pi * k / 48
        c, s = math.cos(a), math.sin(a)
        x = cx + w / 2 * math.copysign(abs(c) ** 0.6, c)
        y = cy + h / 2 * math.copysign(abs(s) ** 0.8, s)
        pts.append((x, y))
    d.line(*pts, closed=True)


def _half_width(cy, w, h, y):
    """The crown's half-width at height y, from the outline _crown draws."""
    s = min(1.0, abs(2 * (y - cy) / h)) ** (1 / 0.8)
    return w / 2 * max(0.0, 1 - s * s) ** 0.3


def _band(d, cx, cy, w, h, waves, amp):
    """A plate of enamel worn flat: a closed band across the crown, its edges scalloped (amp) or plain."""
    n = 40
    top = [(cx - w / 2 + w * k / n, cy - h / 2 + amp * math.sin(waves * math.pi * k / n)) for k in range(n + 1)]
    bot = [(cx + w / 2 - w * k / n, cy + h / 2 - amp * math.sin(waves * math.pi * (n - k) / n)) for k in range(n + 1)]
    d.line(*top, *bot, closed=True)


def cuvier_extinction():
    d = D()
    # The worn grinding teeth Cuvier compared in 1796 (Memoire sur les especes d'elephans, read 1 Pluviose
    # an IV), each crown in plan, front at the top. Cape (African): lozenges 2.5 to 3 times as wide as long,
    # 8 or 9 a tooth. Ceylon (Asian): narrow transverse ribbons, scalloped, up to 12. Mammoth: like Ceylon's
    # but thinner, closer, more numerous, less scalloped (drawn with 16; Cuvier gives no count). Ohio animal
    # (mastodon): three or four pairs of blunt cusps. Schematic: proportions follow his words, not a specimen.
    cy, h, w = 132, 176, 62
    xs = [62, 160, 258, 350]

    d.group('thin')
    for x in xs:
        d.line((x, cy - h / 2 - 12), (x, cy + h / 2 + 12))                 # long axis of each crown
    # the Cape lozenge's proportions, measured: transverse 40, longitudinal 16, 2.5 to 1
    d.line((xs[0] - 20, 34), (xs[0] + 20, 34))
    for x in (xs[0] - 20, xs[0] + 20):
        d.line((x, 30), (x, 38))

    d.group()
    for x in xs:
        _crown(d, x, cy, w, h)

    d.group('mid')
    for k in range(8):                                                     # Cape: eight lozenges
        y = cy - h / 2 + 20 + k * (h - 40) / 7
        d.line((xs[0] - 20, y), (xs[0], y - 8), (xs[0] + 20, y), (xs[0], y + 8), closed=True)
    for k in range(12):                                                    # Ceylon: twelve scalloped ribbons
        y = cy - h / 2 + 14 + k * (h - 28) / 11
        _band(d, xs[1], y, min(46, 2 * _half_width(cy, w, h, y) - 10), 5, 9, 1.2)
    for k in range(16):                                                    # mammoth: thinner, closer, straighter
        y = cy - h / 2 + 12 + k * (h - 24) / 15
        _band(d, xs[2], y, min(48, 2 * _half_width(cy, w, h, y) - 10), 3.4, 5, 0.4)
    for k in range(3):                                                     # Ohio animal: pairs of blunt cusps
        y = cy - h / 2 + 38 + k * 50
        for s in (-1, 1):
            d.circle(xs[3] + s * 13, y, 11)
            d.line((xs[3] + s * 13, y - 6), (xs[3] + s * 19, y), (xs[3] + s * 13, y + 6), (xs[3] + s * 7, y),
                   closed=True)

    d.group('mid')
    names = [('CAPE', '8-9 LOZENGES'), ('CEYLON', 'UP TO 12 BANDS'), ('MAMMOTH', 'MORE, THINNER'),
             ('OHIO', 'PAIRS OF CUSPS')]
    for x, (a, b) in zip(xs, names):
        d.text(x, cy + h / 2 + 26, a, size=7)
        d.text(x, cy + h / 2 + 37, b, size=7)
    d.text(xs[0], 26, '2.5 : 1', size=7)
    d.text(xs[1], 30, 'LIVING', size=7)
    d.text(xs[2] + 46, 30, 'FOSSIL ONLY', size=7)
    d.text(200, 288, 'WORN MOLAR CROWNS IN PLAN · CUVIER, 1796', size=7)
    return d


def lamarck():
    d = D()
    # Lamarck's "Tableau servant a montrer l'origine des differens animaux" (Philosophie zoologique, 1809,
    # Additions), turned on its side: his page runs top to bottom, this plate left to right. Two roots, worms
    # and infusorians, arising by spontaneous generation; his dotted lines of descent drawn dotted. The order
    # within each run (insects, arachnids, crustaceans; annelids, cirripedes, mollusks) is his; positions are ours.
    N = {
        'WORMS': (34, 112), 'INFUSORIANS': (34, 230), 'POLYPS': (98, 230), 'RADIARIANS': (162, 230),
        'INSECTS': (116, 56), 'ARACHNIDS': (172, 56), 'CRUSTACEANS': (228, 56),
        'ANNELIDS': (116, 140), 'CIRRIPEDES': (168, 140), 'MOLLUSKS': (220, 140),
        'FISHES': (250, 170), 'REPTILES': (300, 170),
        'BIRDS': (322, 104), 'MONOTREMES': (370, 104),
        'AMPHIBIOUS': (330, 212), 'CETACEANS': (378, 180), 'UNGULATES': (378, 232),
        'UNGUICULATES': (344, 254),
    }
    fork = (76, 112)
    links = [('WORMS', fork), (fork, 'INSECTS'), ('INSECTS', 'ARACHNIDS'), ('ARACHNIDS', 'CRUSTACEANS'),
             (fork, 'ANNELIDS'), ('ANNELIDS', 'CIRRIPEDES'), ('CIRRIPEDES', 'MOLLUSKS'),
             ('MOLLUSKS', 'FISHES'), ('FISHES', 'REPTILES'), ('REPTILES', 'BIRDS'), ('BIRDS', 'MONOTREMES'),
             ('REPTILES', 'AMPHIBIOUS'), ('AMPHIBIOUS', 'CETACEANS'), ('AMPHIBIOUS', 'UNGULATES'),
             ('AMPHIBIOUS', 'UNGUICULATES'),
             ('INFUSORIANS', 'POLYPS'), ('POLYPS', 'RADIARIANS')]

    def pt(k):
        return N[k] if isinstance(k, str) else k

    def trim(a, b, r=4.5):
        (x0, y0), (x1, y1) = a, b
        L = math.dist(a, b)
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        r0 = r if a in N.values() else 0
        return (x0 + ux * r0, y0 + uy * r0), (x1 - ux * r, y1 - uy * r)

    d.group('thin')
    d.line((20, 276), (390, 276))                                          # the direction of increasing complexity
    _arrow(d, (20, 276), (390, 276), size=4)

    d.group()
    for k, (x, y) in N.items():
        d.circle(x, y, 4.5 if k not in ('WORMS', 'INFUSORIANS') else 6)

    d.group('mid')
    for a, b in links:
        p0, p1 = trim(pt(a), pt(b))
        d.dashed(p0, p1, dash=0.8, gap=3.2)
    d.circle(*fork, 1.6)

    d.group('mid')
    above = {'INSECTS', 'CRUSTACEANS', 'CIRRIPEDES', 'BIRDS', 'MONOTREMES', 'WORMS', 'CETACEANS'}
    left = {'AMPHIBIOUS', 'UNGUICULATES'}
    for k, (x, y) in N.items():
        label = 'AMPHIBIOUS MAMMALS' if k == 'AMPHIBIOUS' else k
        if k == 'WORMS':
            d.text(x - 4, y - 11, label, size=7, anchor='start')
        elif k in left:
            d.text(x - 9, y + 2.5, label, size=7, anchor='end')
        elif k in above:
            d.text(x, y - 9, label, size=7)
        else:
            d.text(x, y + 14, label, size=7)
    d.text(386, 270, 'MORE COMPLEX', size=7, anchor='end')
    d.text(20, 270, 'SIMPLER', size=7, anchor='start')
    d.text(200, 292, "LAMARCK'S TABLE OF THE ORIGIN OF ANIMALS, 1809", size=7)
    return d


PLATES = {'steno-fossils': steno_fossils, 'cuvier-extinction': cuvier_extinction, 'lamarck': lamarck}
