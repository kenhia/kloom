"""Plates for Keeping Watch's Nightingale segment, first half (sprint 030, part night1). See plates_for.py."""
import math
from plates import D


def _pt(cx, cy, r, a):
    """The point at `a` degrees on a circle (clockwise from +x; SVG's y runs down)."""
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def _arrow(d, p, q, size=5):
    """An arrowhead at q, pointing from p."""
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    l = (q[0] - size * math.cos(a - 0.45), q[1] - size * math.sin(a - 0.45))
    r = (q[0] - size * math.cos(a + 0.45), q[1] - size * math.sin(a + 0.45))
    d.line(l, q, r)


def _box(d, x, y, w, h):
    d.line((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)


def _wedge(d, cx, cy, r, a0, a1, n=10):
    """A wedge from the centre, radius r, between a0 and a1 degrees."""
    if r <= 0.3:
        return
    pts = [(cx, cy)] + [_pt(cx, cy, r, a0 + (a1 - a0) * k / n) for k in range(n + 1)]
    d.line(*pts, closed=True)


# The first year of the war, April 1854 to March 1855: annual rates of mortality per 1,000 in the
# hospitals of the army in the East (zymotic, wounds, other), from Table K, fig. 1, of Nightingale's
# Mortality of the British Army (1858).
YEAR1 = [
    (1.4, 0, 7.0), (6.2, 0, 4.6), (4.7, 0, 2.5), (150.0, 0, 9.6), (328.5, 0.4, 11.9),
    (312.2, 32.1, 27.7), (197.0, 51.7, 50.1), (340.6, 115.8, 42.8), (631.5, 41.7, 48.0),
    (1022.8, 30.7, 120.0), (822.8, 16.3, 140.1), (480.3, 12.8, 68.6),
]


def rose_diagram():
    d = D()
    # The first year's wheel on its construction, as Nightingale drew it: twelve 30-degree wedges,
    # April 1854 starting at nine o'clock and running clockwise, each wedge's AREA equal to the month's
    # rate, so its radius goes as the square root. The rings are drawn at rates 100, 250, 500 and
    # 1,000 and crowd together outwards. Blue (zymotic) at full weight; wounds and other causes,
    # measured from the same centre, at mid weight.
    cx, cy = 182, 136
    k = 126 / math.sqrt(1000)                                           # pixels per root-rate
    d.group('thin')
    for rate in (100, 250, 500, 1000):
        d.circle(cx, cy, k * math.sqrt(rate))
    for m in range(12):
        d.line((cx, cy), _pt(cx, cy, 130, 180 + 30 * m))
    d.line((cx, cy), _pt(cx, cy, 168, -14))                              # the ray the ring scale is read on
    d.group()
    for m, (z, w, o) in enumerate(YEAR1):
        a0 = 180 + 30 * m
        _wedge(d, cx, cy, k * math.sqrt(z), a0, a0 + 30)
    d.group('mid')
    for m, (z, w, o) in enumerate(YEAR1):
        a0 = 180 + 30 * m
        _wedge(d, cx, cy, k * math.sqrt(w), a0 + 3, a0 + 27, n=6)
        _wedge(d, cx, cy, k * math.sqrt(o), a0 + 6, a0 + 24, n=6)
    # the worked wedge, January 1855, dimensioned: its radius against the 1,000 ring
    rj = k * math.sqrt(1022.8)
    p0, p1 = _pt(cx, cy, 12, 105), _pt(cx, cy, rj - 2, 105)
    d.line(p0, p1)
    _arrow(d, p0, p1, 4)
    _arrow(d, p1, p0, 4)
    d.group('mid')
    for rate in (100, 250, 500, 1000):
        x, y = _pt(cx, cy, k * math.sqrt(rate), -14)
        d.text(x + 3, y - 4, f'{rate:,}', size=7, anchor='start')
    d.text(150, 292, 'JANUARY 1855 · ZYMOTIC 1,022.8', size=7)
    d.text(36, 124, 'APRIL', size=7)
    d.text(36, 133, '1854', size=7)
    d.text(330, 230, 'AREA = RATE', size=7)
    d.text(330, 240, 'r ∝ √RATE', size=7)
    d.text(330, 256, 'ZYMOTIC · WOUNDS · OTHER', size=7)
    d.text(330, 266, 'PER 1,000 A YEAR', size=7)
    return d


def scutari():
    d = D()
    # Left: the Barrack Hospital at Scutari (the Selimiye Barracks) in plan, a schematic at about
    # 0.6 px to the metre: a rectangle of about 267 by 200 metres round a parade ground, three-storey
    # ranges, a tower at each corner. Right: a schematic section through one range, as the 1855
    # Sanitary Commission described it: wards and a corridor over sewers "loaded with filth", whose
    # air rose up the privy pipes into the corridors where the sick lay.
    x0, y0, W, H, dep = 22, 70, 160, 120, 18
    d.group('thin')
    d.line((x0, y0 - 14), (x0 + W, y0 - 14))                              # the long side, dimensioned
    d.line((x0, y0 - 19), (x0, y0 - 9))
    d.line((x0 + W, y0 - 19), (x0 + W, y0 - 9))
    d.line((x0 - 12, y0), (x0 - 12, y0 + H))                              # the short side
    d.line((x0 - 17, y0), (x0 - 7, y0))
    d.line((x0 - 17, y0 + H), (x0 - 7, y0 + H))
    d.line((x0 + W / 2, y0 + dep), (x0 + W / 2, y0 + H - dep))            # the parade ground's axes
    d.line((x0 + dep, y0 + H / 2), (x0 + W - dep, y0 + H / 2))
    d.group()
    _box(d, x0, y0, W, H)
    _box(d, x0 + dep, y0 + dep, W - 2 * dep, H - 2 * dep)
    for tx, ty in ((x0, y0), (x0 + W, y0), (x0, y0 + H), (x0 + W, y0 + H)):
        _box(d, tx - 8, ty - 8, 16, 16)
    d.group('mid')
    # a corridor along the inner face of every range, and the beds laid in it two deep
    c = 6
    _box(d, x0 + dep - c, y0 + dep - c, W - 2 * dep + 2 * c, H - 2 * dep + 2 * c)
    for i in range(14):
        x = x0 + dep + 4 + i * (W - 2 * dep - 8) / 13
        d.line((x, y0 + 4), (x, y0 + 9))
        d.line((x, y0 + H - 9), (x, y0 + H - 4))
    # the section
    sx0, sx1, g = 222, 384, 222
    floors = [g, g - 40, g - 80, g - 120]
    d.group('thin')
    d.line((sx0 - 8, g), (sx1 + 8, g))                                    # the ground
    for y in floors[1:]:
        d.line((sx0, y), (sx1, y))
    d.group()
    d.line((sx0, g), (sx0, floors[3]), (sx1, floors[3]), (sx1, g))
    d.line((sx0 - 4, floors[3]), ((sx0 + sx1) / 2, floors[3] - 22), (sx1 + 4, floors[3]))
    d.line((300, g), (300, floors[3]))                                    # ward | corridor wall
    # the sewer under the building: a brick barrel, seen along its length, with its end in section
    d.line((sx0 + 22, g + 22), (sx1 + 2, g + 22))
    d.line((sx0 + 22, g + 40), (sx1 + 2, g + 40))
    d.circle(sx0 + 13, g + 31, 9)
    d.line((sx0 + 4, g + 31), (sx0 + 4, g + 42), (sx0 + 22, g + 42), (sx0 + 22, g + 31))
    d.group('mid')
    # the privy pipe at the corridor's end, from every floor down to the sewer
    px = 370
    d.line((px, floors[3] + 6), (px, g + 22))
    d.line((px + 6, floors[3] + 6), (px + 6, g + 22))
    for y in floors[:3]:
        _box(d, px - 10, y - 14, 8, 8)                                    # the privy seat on each floor
    for y in floors[:3]:                                                  # beds: two in the ward, one in the corridor
        for bx in (sx0 + 10, sx0 + 46):
            _box(d, bx, y - 9, 30, 7)
        _box(d, 314, y - 9, 26, 7)
    # foul air: up the pipe and out into each corridor
    for y in floors[:3]:
        _arrow(d, (px + 3, y + 20), (px + 3, y + 4), 4)
        d.line((px - 2, y - 24), (346, y - 24))
        _arrow(d, (px - 2, y - 24), (346, y - 24), 4)
    d.group('mid')
    d.text(x0 + W / 2, y0 - 20, '267 M', size=7)
    d.text(x0 - 2, y0 + H + 16, '200 M', size=7)
    d.text(x0 + W / 2, y0 + H / 2 + 3, 'PARADE GROUND', size=7)
    d.text(x0 + W / 2, y0 + H + 22, 'BARRACK HOSPITAL · PLAN', size=7)
    d.text(x0 + W / 2, y0 + H + 32, '200 × 267 M · SCHEMATIC', size=7)
    d.text(261, 64, 'WARD', size=7)
    d.text(330, 64, 'CORRIDOR', size=7)
    d.text(290, g + 54, 'SEWER', size=7)
    d.text(303, 290, 'SECTION · SCHEMATIC', size=7)
    return d


def seacole():
    d = D()
    # Mary Seacole's Crimea as a schematic, not a survey: Balaclava harbour and its sick wharf, the
    # road up to Spring Hill near Kadikoi, about three and a half miles, where she built the British
    # Hotel, and on to Cathcart's Hill above the trenches before Sevastopol, three and a half miles
    # again by her own account. Inset: the hotel's compound as Wikipedia's account of it lists the
    # parts (an iron store with counters, a kitchen, two sleeping huts, outhouses, a stable yard);
    # the arrangement is ours.
    hb, sh, ch = (60, 236), (176, 168), (306, 76)
    d.group('thin')
    for p, q in ((hb, sh), (sh, ch)):                                    # straight-line distances
        d.line(p, q)
    for (x, y) in (hb, sh, ch):
        d.circle(x, y, 14)
    d.circle(ch[0], ch[1], 46)                                            # the trenches' arc round the hill
    d.group()
    # the harbour: a narrow inlet opening south to the sea
    d.curve(f'M {hb[0]-14} 292 C {hb[0]-16} 262 {hb[0]-6} 246 {hb[0]-8} 222 C {hb[0]-6} 212 {hb[0]+6} 210 {hb[0]+8} 222 '
            f'C {hb[0]+10} 246 {hb[0]+18} 262 {hb[0]+16} 292')
    _box(d, hb[0] + 10, hb[1] - 6, 14, 6)                                 # the sick wharf
    # the road, winding up
    d.curve(f'M {hb[0]+24} {hb[1]-3} C 100 230 120 196 {sh[0]-8} {sh[1]+6} '
            f'C 210 150 236 130 {ch[0]-10} {ch[1]+12}')
    # the hill and the trench lines before the town
    d.arc(ch[0], ch[1], 46, 200, 340, n=20)
    d.arc(ch[0], ch[1], 56, 210, 330, n=20)
    for a in range(210, 331, 15):
        d.line(_pt(ch[0], ch[1], 46, a), _pt(ch[0], ch[1], 56, a))
    # the compound, inset
    ix, iy = 30, 40
    d.group('mid')
    _box(d, ix, iy, 120, 84)                                              # the yard's fence
    _box(d, ix + 8, iy + 8, 60, 30)                                       # the iron store
    for k in range(3):
        d.line((ix + 14 + 16 * k, iy + 30), (ix + 24 + 16 * k, iy + 30))  # counters
    _box(d, ix + 68, iy + 8, 22, 30)                                      # the kitchen, attached
    _box(d, ix + 8, iy + 50, 26, 22)                                      # two sleeping huts
    _box(d, ix + 40, iy + 50, 26, 22)
    _box(d, ix + 96, iy + 8, 16, 14)                                      # outhouses
    for k in range(4):                                                    # stalls in the stable yard
        _box(d, ix + 74 + 10 * k, iy + 58, 8, 18)
    d.line((ix + 120, iy + 84), (sh[0] - 10, sh[1] - 10))                # leader to Spring Hill
    d.group('mid')
    d.text(hb[0] + 40, 262, 'BALACLAVA', size=7)
    d.text(hb[0] + 40, 271, 'SICK WHARF', size=7)
    d.text(sh[0] + 40, sh[1] + 20, 'SPRING HILL', size=7)
    d.text(ch[0] + 4, ch[1] + 72, "CATHCART'S HILL", size=7)
    d.text(ch[0] + 4, ch[1] - 62, 'TRENCHES', size=7)
    d.text(118, 222, '3½ MI', size=7)
    d.text(272, 140, '3½ MI', size=7)
    d.text(ix + 60, iy - 8, 'THE BRITISH HOTEL · SCHEMATIC', size=7)
    d.text(ix + 38, iy + 24, 'STORE', size=7)
    d.text(ix + 79, iy + 46, 'KITCHEN', size=7)
    d.text(ix + 37, iy + 80, 'HUTS', size=7)
    d.text(ix + 93, iy + 86, 'STABLES', size=7)
    return d


PLATES = {
    'scutari': scutari,
    'seacole': seacole,
    'rose-diagram': rose_diagram,
}
