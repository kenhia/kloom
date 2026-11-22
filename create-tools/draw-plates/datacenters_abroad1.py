"""Plates for The Cloud on the Ground's trail Elsewhere, part abroad1 (sprint 059). See plates_for.py.

Both are plans whose places stand at their true relative positions: each point is its Wikipedia
coordinates (prop=coordinates, read 2026-11-22) through an equirectangular projection. The
coasts are schematic, drawn by hand through a few points and labeled so, until coastlines.py
holds a region for each.
"""
import math
from plates import D, hatch


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def _proj(lon0, lat0, lon1, lat1, x0, y0, k):
    """An equirectangular projection of the box (lon0..lon1, lat0..lat1): k plate units per degree
    of latitude, longitude shrunk by the cosine of the box's middle latitude."""
    c = math.cos(math.radians((lat0 + lat1) / 2))

    def p(lon, lat):
        return (x0 + (lon - lon0) * k * c, y0 + (lat1 - lat) * k)
    return p, k * c


def singapore_pause():
    """Singapore and southern Johor in plan: the island, the Straits of Johor and the causeway, the
    data center sites: Jurong Island, where the 2026 allocations go, and in Johor the clusters
    ISEAS names at Iskandar Puteri (Nusajaya Tech Park) and Sedenak Tech Park, and a
    10 km scale. Points at their coordinates; coasts schematic."""
    d = D()
    p, kx = _proj(103.45, 1.15, 104.10, 1.78, 40, 20, 420)
    # schematic coasts, (lon, lat)
    island = [(103.61, 1.31), (103.64, 1.35), (103.67, 1.39), (103.72, 1.43), (103.77, 1.445),
              (103.82, 1.465), (103.87, 1.43), (103.92, 1.41), (103.96, 1.39), (104.03, 1.38),
              (104.00, 1.33), (103.93, 1.305), (103.86, 1.275), (103.81, 1.265), (103.76, 1.275),
              (103.71, 1.30), (103.65, 1.295)]
    jurong = [(103.665, 1.255), (103.70, 1.25), (103.735, 1.265), (103.72, 1.29), (103.68, 1.285)]
    johor = [(103.45, 1.37), (103.52, 1.38), (103.58, 1.40), (103.63, 1.42), (103.68, 1.455),
             (103.73, 1.47), (103.77, 1.475), (103.82, 1.495), (103.88, 1.49), (103.95, 1.475),
             (104.02, 1.45), (104.10, 1.42)]
    cause_s, cause_n = (103.7686, 1.4467), (103.7686, 1.4602)
    places = {
        'SINGAPORE': (103.8333, 1.2833),
        'JURONG ISLAND': (103.6959, 1.2701),
        'JOHOR BAHRU': (103.7611, 1.4556),
        'ISKANDAR PUTERI': (103.65, 1.4222),
        'SEDENAK': (103.5248, 1.7137),
    }

    d.group('thin')
    # graticule every 0.1 degree
    for i in range(7):
        lon = 103.5 + i * 0.1
        d.line(p(lon, 1.18), p(lon, 1.76))
    for j in range(6):
        lat = 1.2 + j * 0.1
        d.line(p(103.47, lat), p(104.08, lat))

    d.group()
    d.line(*[p(*q) for q in island], closed=True)
    d.line(*[p(*q) for q in jurong], closed=True)
    d.line(*[p(*q) for q in johor])
    # the causeway, drawn a little longer than it is so it shows at this scale
    a, b = p(*cause_s), p(*cause_n)
    d.line((a[0] - 1.5, a[1] + 2), (b[0] - 1.5, b[1] - 3))
    d.line((a[0] + 1.5, a[1] + 2), (b[0] + 1.5, b[1] - 3))

    d.group('mid')
    # data center sites: a square each, hatched where Singapore allocated capacity in 2026
    for name in ('JURONG ISLAND', 'ISKANDAR PUTERI', 'SEDENAK'):
        x, y = p(*places[name])
        _box(d, x - 4, y - 4, 8, 8)
    x, y = p(*places['JURONG ISLAND'])
    d.lines(hatch([(x - 4, y - 4), (x + 4, y - 4), (x + 4, y + 4), (x - 4, y + 4)], 2.2, 45))
    for name in ('SINGAPORE', 'JOHOR BAHRU'):
        x, y = p(*places[name])
        d.circle(x, y, 2.2)
    # the move north the reading describes: an arrow from the island to the Johor sites
    s = p(103.70, 1.40)
    e = p(103.55, 1.66)
    d.dashed(s, e, dash=4, gap=3)
    _arrow(d, s, e, 5)
    # scale: 10 km = 10 / 111.32 degrees of longitude at this latitude
    sx0 = (40, 282)
    sx1 = (40 + 10 / 111.32 * kx, 282)
    d.line(sx0, sx1)
    d.line((sx0[0], 278), (sx0[0], 286))
    d.line((sx1[0], 278), (sx1[0], 286))

    d.group('labels')
    x, y = p(*places['SINGAPORE'])
    d.text(x + 8, y - 22, 'SINGAPORE', size=7, anchor='start')
    x, y = p(*places['JURONG ISLAND'])
    d.text(x, y + 14, 'JURONG ISLAND', size=7)
    x, y = p(*places['ISKANDAR PUTERI'])
    d.text(x - 8, y + 3, 'ISKANDAR PUTERI', size=7, anchor='end')
    x, y = p(*places['SEDENAK'])
    d.text(x + 8, y + 3, 'SEDENAK', size=7, anchor='start')
    x, y = p(*places['JOHOR BAHRU'])
    d.text(x - 4, y - 24, 'JOHOR BAHRU', size=7, anchor='end')
    cx, cy = p(*cause_n)
    d.line((cx + 2, cy - 4), (cx + 24, cy - 30))
    d.text(cx + 26, cy - 31, 'CAUSEWAY', size=7, anchor='start')
    d.text(p(103.95, 1.62)[0], p(103.95, 1.62)[1], 'JOHOR', size=7)
    d.text((sx0[0] + sx1[0]) / 2, 296, '10 KM', size=7)
    d.text(390, 296, 'COASTS SCHEMATIC', size=7, anchor='end')
    return d


def netherlands_pause():
    """The Netherlands in plan: the places the reading names at their coordinates, the two areas
    left open to hyperscale data centers (Eemshaven, and the Agriport by Middenmeer) hatched,
    Zeewolde's annulled site crossed, and a 50 km scale. The coast is schematic."""
    d = D()
    p, kx = _proj(4.25, 52.0, 7.25, 53.65, 26, 12, 168)
    coast = [(4.30, 52.10), (4.42, 52.25), (4.52, 52.40), (4.58, 52.55), (4.63, 52.70),
             (4.68, 52.85), (4.73, 52.95), (4.90, 52.97), (5.05, 53.0), (5.25, 53.05), (5.42, 53.17),
             (5.55, 53.28), (5.80, 53.38), (6.10, 53.42), (6.40, 53.43), (6.70, 53.45), (6.83, 53.45),
             (6.95, 53.33), (7.15, 53.25)]
    places = {
        'AMSTERDAM': (4.8936, 52.3728),
        'HAARLEMMERMEER': (4.6907, 52.3061),
        'ZEEWOLDE': (5.55, 52.3333),
        'LELYSTAD': (5.4833, 52.5),
        'MIDDENMEER': (4.9983, 52.8086),
        'EEMSHAVEN': (6.8311, 53.4483),
        'GRONINGEN': (6.5675, 53.2189),
    }

    d.group('thin')
    for i in range(7):
        lon = 4.5 + i * 0.5
        d.line(p(lon, 52.03), p(lon, 53.62))
    for j in range(4):
        lat = 52.0 + j * 0.5
        d.line(p(4.28, lat), p(7.22, lat))

    d.group()
    d.line(*[p(*q) for q in coast])
    # the two areas left open to hyperscale data centers, as circles about 6 km across
    r = 3 / 111.32 * 168
    for name in ('MIDDENMEER', 'EEMSHAVEN'):
        x, y = p(*places[name])
        d.circle(x, y, r)
        n = 24
        ring = [(x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
        d.lines(hatch(ring, 2.2, 45))
    # Zeewolde's site, crossed out
    zx, zy = p(*places['ZEEWOLDE'])
    _box(d, zx - 5, zy - 5, 10, 10)
    d.line((zx - 5, zy - 5), (zx + 5, zy + 5))
    d.line((zx - 5, zy + 5), (zx + 5, zy - 5))

    d.group('mid')
    for name in ('AMSTERDAM', 'HAARLEMMERMEER', 'LELYSTAD', 'GRONINGEN'):
        x, y = p(*places[name])
        d.circle(x, y, 2.2)
    # scale: 50 km of longitude at 52.8 degrees north
    sx0 = (270, 286)
    sx1 = (270 + 50 / 111.32 * kx, 286)
    d.line(sx0, sx1)
    d.line((sx0[0], 282), (sx0[0], 290))
    d.line((sx1[0], 282), (sx1[0], 290))

    d.group('labels')
    def lab(name, dx, dy, anchor='start', text=None):
        x, y = p(*places[name])
        d.text(x + dx, y + dy, text or name, size=7, anchor=anchor)
    lab('AMSTERDAM', 6, -4)
    lab('HAARLEMMERMEER', 4, 14)
    lab('ZEEWOLDE', 9, 3)
    lab('LELYSTAD', 6, -4)
    lab('MIDDENMEER', 11, 3)
    lab('EEMSHAVEN', -11, -8, 'end')
    lab('GRONINGEN', -6, 10, 'end')
    d.text(p(4.55, 53.25)[0], p(4.55, 53.25)[1], 'NORTH SEA', size=7)
    d.text((sx0[0] + sx1[0]) / 2, 298, '50 KM', size=7)
    d.text(26, 298, 'COAST SCHEMATIC', size=7, anchor='start')
    return d


PLATES = {
    'singapore-pause': singapore_pause,
    'netherlands-pause': netherlands_pause,
}
