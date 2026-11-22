"""Plates for The Cloud on the Ground's neighbors frames written by part neigh2 in sprint 059. See plates_for.py."""
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


# Published coordinates (latitude, longitude): Wikipedia's for the Colossus article, Boxtown and the
# Allen Fossil Plant; OpenStreetMap's for 3231 Paul R. Lowry Road (Colossus 1), 5420 Tulane Road
# (Colossus 2) and 2875 Stanton Road, Southaven (the turbine site). The state line is drawn at 34.995 N,
# its approximate latitude here.
SITES = {
    'c1': (35.0600, -90.1520),
    'c2': (34.9980, -90.0349),
    'sv': (34.9844, -90.0433),
    'allen': (35.0736, -90.1486),
    'boxtown': (35.048, -90.124),
}
LON0, LAT0 = -90.175, 35.085
K = 21.0                      # plate units per kilometre
KM_LON = 111.32 * math.cos(math.radians(35.03))
KM_LAT = 111.0


def _xy(lat, lon):
    return (30 + (lon - LON0) * KM_LON * K, 22 + (LAT0 - lat) * KM_LAT * K)


def memphis_turbines():
    """South Memphis and Southaven in plan, to scale from published coordinates: Colossus 1 in the old
    Electrolux plant with rings at one and two miles, the TVA Allen site beside it, Boxtown to the
    south-east, and Colossus 2 at the state line with its turbine site across it in Mississippi."""
    d = D()
    c1, c2, sv = _xy(*SITES['c1']), _xy(*SITES['c2']), _xy(*SITES['sv'])
    al, bx = _xy(*SITES['allen']), _xy(*SITES['boxtown'])
    mile = 1.609344 * K
    line_y = _xy(34.995, LON0)[1]

    d.group('thin')
    # a two-kilometre grid
    for i in range(0, 15, 2):
        x = 30 + i * K
        d.line((x, 18), (x, 276))
    for j in range(0, 13, 2):
        y = 22 + j * K
        if y <= 276:
            d.line((26, y), (30 + 14 * K, y))
    # distance rings about Colossus 1, and one mile about the Southaven site
    d.circle(c1[0], c1[1], mile)
    d.circle(c1[0], c1[1], 2 * mile)
    d.circle(sv[0], sv[1], mile)

    d.group()
    # the state line
    d.dashed((20, line_y), (380, line_y), dash=8, gap=4)
    # Colossus 1, Colossus 2 and the Allen site as buildings to rough scale (about 0.5 km)
    _box(d, c1[0] - 6, c1[1] - 5, 12, 10)
    _box(d, c2[0] - 6, c2[1] - 6, 12, 9)
    _box(d, al[0] - 5, al[1] - 4, 10, 8)
    # Boxtown: the neighborhood, drawn as a dotted ring about its centroid
    d.dashed(*[(bx[0] + 22 * math.cos(t * math.pi / 18), bx[1] + 11 * math.sin(t * math.pi / 18))
               for t in range(37)], dash=2, gap=3)
    # the turbine site: a row of trailers
    for k in range(6):
        _box(d, sv[0] - 11 + k * 4, sv[1] - 2, 3, 5)

    d.group('mid')
    hatch_poly = [(al[0] - 5, al[1] - 4), (al[0] + 5, al[1] - 4), (al[0] + 5, al[1] + 4), (al[0] - 5, al[1] + 4)]
    d.lines(hatch(hatch_poly, 2.5, 45))
    # power from the turbine site to Colossus 2
    d.line((sv[0], sv[1] - 3), (c2[0] - 2, c2[1] + 4))
    _arrow(d, (sv[0], sv[1] - 3), (c2[0] - 2, c2[1] + 4), 4)
    # a 2 km scale bar and a north arrow
    sx, sy = 300, 86
    d.line((sx, sy), (sx + 2 * K, sy))
    for t in (0, 1, 2):
        d.line((sx + t * K, sy - 3), (sx + t * K, sy + 3))
    d.line((372, 60), (372, 36))
    _arrow(d, (372, 60), (372, 36), 5)

    d.group('labels')
    d.text(c1[0] - 9, c1[1] + 3, 'COLOSSUS 1', size=7, anchor='end')
    d.text(al[0] + 8, al[1] + 3, 'TVA ALLEN', size=7, anchor='start')
    d.text(bx[0], bx[1] + 2.5, 'BOXTOWN', size=7)
    d.text(c2[0] + 9, c2[1] - 2, 'COLOSSUS 2', size=7, anchor='start')
    d.text(sv[0] - 14, sv[1] + 3, 'TURBINE SITE', size=7, anchor='end')
    d.text(c1[0], c1[1] + mile + 9, '1 MI', size=7)
    d.text(c1[0], c1[1] + 2 * mile + 9, '2 MI', size=7)
    d.text(24, line_y - 4, 'TENNESSEE', size=7, anchor='start')
    d.text(24, line_y + 10, 'MISSISSIPPI', size=7, anchor='start')
    d.text(sx + K, sy + 12, '2 KM', size=7)
    d.text(372, 30, 'N', size=7)
    return d


# Project Blue, from Arizona Luminaria's reporting and the City of Tucson's archive page: months from
# June 2024 (the county under an NDA by then) to December 2025; the 2023 project profile sits before the bar.
EVENTS = [
    # (month index from June 2024, label, above?, leader height)
    (0.0, 'NDA IN PLACE', True, 34),
    (12.55, 'SALE VOTE 3–2', True, 62),
    (13.65, 'AWS NAMED IN PRESS', False, 34),
    (14.2, 'CITY ENDS TALKS', True, 30),
    (15.05, 'COUNTY NDA RULES', False, 62),
    (18.5, 'SALE APPROVED', True, 96),
]


def secrecy():
    """Project Blue as a bar of months, June 2024 to December 2025: the stretch under a nondisclosure
    agreement hatched, then the vote to sell the land, the press report naming the user, the city's vote
    and the county's new rules, each on a leader from its date."""
    d = D()
    x0, step = 54, 17.5
    y, h = 150, 14
    nda_end = 13.65                      # the end user named in the press, July 21, 2025

    def mx(m):
        return x0 + m * step

    d.group('thin')
    for m in range(0, 20):               # month ticks, June 2024 .. January 2026
        d.line((mx(m), y + h), (mx(m), y + h + 4))
    for m in (7, 19):                    # year boundaries: January 2025, January 2026
        d.line((mx(m), y - 6), (mx(m), y + h + 10))
    # the stub for 2023, broken off before the bar
    d.line((18, y + h / 2), (38, y + h / 2))
    d.line((40, y - 2), (44, y + h + 2))
    d.line((44, y - 2), (48, y + h + 2))

    d.group()
    _box(d, mx(0), y, mx(19) - mx(0), h)
    for m in range(1, 19):
        d.line((mx(m), y), (mx(m), y + h))

    d.group('mid')
    poly = [(mx(0), y), (mx(nda_end), y), (mx(nda_end), y + h), (mx(0), y + h)]
    d.lines(hatch(poly, 4, 45))
    d.circle(24, y + h / 2, 2.5)
    for (m, _, above, lead) in EVENTS:
        x = mx(m)
        if above:
            d.line((x, y), (x, y - lead))
        else:
            d.line((x, y + h), (x, y + h + lead))
        d.circle(x, y if above else y + h, 1.8)

    d.group('labels')
    for (m, label, above, lead) in EVENTS:
        x = mx(m)
        anchor = 'start' if m < 10 else 'end' if m > 17 else 'middle'
        if above:
            d.text(x, y - lead - 4, label, size=7, anchor=anchor)
        else:
            d.text(x, y + h + lead + 9, label, size=7, anchor=anchor)
    d.text(24, y + h + 14, '2023', size=7)
    d.text(24, y + h + 23, 'PROFILE', size=7)
    d.text(mx(3.5), y + h + 32, '2024', size=7)
    d.text(mx(10), y + h + 32, '2025', size=7)
    d.text(mx(nda_end / 2 + 1), y + 30, 'UNDER AN NDA', size=7)
    return d


PLATES = {'memphis-turbines': memphis_turbines, 'secrecy': secrecy}
