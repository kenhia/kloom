"""Plates for Daily Bread's part empire2 (sprint 051): the heavy plow, and a chinampa. See plates_for.py."""
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


def _add(p, v, s=1.0):
    return (p[0] + s * v[0], p[1] + s * v[1])


def open_fields():
    d = D()
    # Above: a heavy wheeled plow in elevation, drawn moving left, the oxen off the plate to the left.
    # Its parts and their order (coulter, share, moldboard, wheeled fore-carriage, beam, handles) follow
    # the descriptions in the Plough and Carruca articles; the proportions are schematic.
    # Below: the furrow in section, looking along it. The slice is cut three parts wide by two deep
    # (the general-purpose proportion in the Plough article), turned over and laid at 45 degrees
    # against the slice before it; with w = 1.5 d each slice just meets the next (0.707 w ~ d).
    ground, sole = 150, 166                                               # surface and furrow bottom
    wheel_c, wheel_r = (88, ground - 22), 22

    d.group('thin')
    d.line((14, ground), (386, ground))                                   # the land's surface
    d.dashed((120, sole), (300, sole), dash=4, gap=3)                     # depth of the furrow
    d.line((wheel_c[0], wheel_c[1] - wheel_r - 8), (wheel_c[0], ground + 6))  # wheel's center line
    d.line((wheel_c[0] - wheel_r - 8, wheel_c[1]), (wheel_c[0] + wheel_r + 8, wheel_c[1]))
    d.line((150, 60), (162, sole))                                        # the coulter's line of cut

    d.group()
    d.circle(*wheel_c, wheel_r)                                           # fore-carriage wheel
    beam_a, beam_b = (52, 104), (262, 82)                                 # the beam, hitch to handles
    d.line(beam_a, beam_b)
    d.line((beam_a[0], beam_a[1] + 5), (beam_b[0], beam_b[1] + 5))
    d.line(wheel_c, (wheel_c[0] + 10, 100))                               # axle post up to the beam
    # coulter: a knife hung from the beam, slanting forward, its point just ahead of the share
    d.line((148, 96), (160, sole - 4), (165, sole - 6), (154, 95))
    # the body: sole along the furrow bottom, share at its point, standard up to the beam
    share_tip, heel = (162, sole), (246, sole)
    d.line(share_tip, heel)
    d.line(share_tip, (186, sole - 7), (188, sole))                       # the share
    d.line((214, sole), (214, 88))                                        # the standard
    # moldboard: rising from behind the share up and back, the slice riding up it
    d.line((186, sole - 7), (240, ground - 26), (250, ground - 18), (246, sole), closed=False)
    # handles
    d.line((240, sole), (312, 56))
    d.line((250, sole - 2), (322, 62))
    d.line((312, 56), (322, 62))

    d.group('mid')
    for k in range(8):                                                    # wheel spokes
        a = math.pi * k / 4
        d.line(wheel_c, (wheel_c[0] + wheel_r * math.cos(a), wheel_c[1] + wheel_r * math.sin(a)))
    d.line((beam_a[0], beam_a[1] + 2), (22, 108))                         # draft chain to the oxen
    _arrow(d, (beam_a[0], beam_a[1] + 2), (22, 108))
    for t in (0.25, 0.5, 0.75):                                           # the slice riding the moldboard
        p = (188 + t * 52, sole - 7 - t * (sole - 7 - (ground - 26)))
        d.line((p[0] - 8, p[1] + 6), p)

    # the section
    w, dep = 30, 20                                                       # slice 3 wide by 2 deep
    top, bot = 236, 256
    land_x = 96
    th = math.radians(45)
    u = (math.cos(th), -math.sin(th))                                     # along the slice, up and right
    n = (-math.sin(th), -math.cos(th))                                    # its thickness, up and left

    d.group('thin')
    d.line((14, top), (land_x, top))
    d.line((land_x, bot), (386, bot))                                     # furrow bottoms, one level

    d.group()
    d.line((14, top), (land_x, top), (land_x, bot), (land_x + w, bot))    # the land, and the open furrow
    slices = []
    for i in range(5):
        a = (land_x + w + i * w, bot)
        b = _add(a, u, w)
        c = _add(b, n, dep)
        e = _add(a, n, dep)
        if i == 0:
            continue                                                      # the open furrow holds none
        slices.append((a, b, c, e))
        d.line(a, b, c, e, closed=True)

    d.group('mid')
    for a, b, c, e in slices:                                             # the buried sod, now underneath
        for t in (0.2, 0.45, 0.7):
            p = _add(a, u, w * t)
            d.line(p, _add(p, (0.707, 0.707), 4))
    d.line((land_x, top - 14), (land_x, top - 4))                         # where the coulter cuts
    _arrow(d, (land_x, top - 14), (land_x, top - 4), size=4)

    d.group('mid')
    d.text(150, 52, 'COULTER', size=7)
    d.text(176, 178, 'SHARE', size=7)
    d.text(272, 140, 'MOLDBOARD', size=7, anchor='start')
    d.text(88, 180, 'WHEELS', size=7)
    d.text(330, 52, 'HANDLES', size=7, anchor='start')
    d.text(120, 82, 'BEAM', size=7)
    d.text(22, 98, 'TO THE OXEN', size=7, anchor='start')
    d.text(55, 228, 'UNPLOWED', size=7)
    d.text(land_x + w / 2, 268, 'OPEN', size=7)
    d.text(land_x + w / 2, 277, 'FURROW', size=7)
    d.text(268, 268, 'SLICES TURNED, SOD UNDER', size=7)
    d.text(200, 292, 'THE FURROW IN SECTION · SLICE 3 WIDE BY 2 DEEP', size=7)
    d.text(200, 22, 'THE HEAVY PLOW IN ELEVATION', size=7)
    return d


def chinampas():
    d = D()
    # A chinampa in section between two canals. Scale: 20 units to the meter across, 40 up, so the
    # height is drawn twice its width. The bed rises 60 cm above the water (50-70 cm, Armillas 1971, in
    # Ebel 2019) and is 7 m wide (5-10 m in Tenochtitlan, Wikipedia "Chinampa"); the canals are 2 m (the
    # ditches between beds, 1-2 m, Ebel 2019). The water's depth, 1.5 m, and the layers' thicknesses
    # are schematic. Willows (ahuejote) stand at the edges, roots in the fill; water rises by capillarity.
    mx, my = 20, 40
    water, bed = 150, 210                                                 # 1.5 m of water
    top = water - 0.6 * my                                                # 60 cm above it
    x0, x1 = 130, 130 + 7 * mx                                            # the bed, 7 m
    cl, cr = (x0 - 2 * mx, x0), (x1, x1 + 2 * mx)                         # canals, 2 m each

    d.group('thin')
    d.line((14, water), (386, water))                                     # water level
    d.line((14, bed), (386, bed))                                         # lake bottom
    d.dashed((x0 + 6, water), (x1 - 6, water), dash=3, gap=3)             # water table in the bed
    d.line((x1 + 54, top), (x1 + 54, water))                              # height above water
    d.line((x1 + 48, top), (x1 + 60, top))
    d.line((x0, 250), (x1, 250))                                          # width
    d.line((x0, 244), (x0, 256))
    d.line((x1, 244), (x1, 256))

    d.group()
    d.line((x0, bed + 8), (x0, top), (x1, top), (x1, bed + 8))            # the bed's walls and surface
    d.line((14, top + 6), (cl[0], top + 6), (cl[0], bed + 8))             # the next beds, cut off
    d.line((386, top + 6), (cr[1], top + 6), (cr[1], bed + 8))
    for x in (x0, x1):                                                    # stakes driven into the bottom
        d.line((x, top - 2), (x, bed + 12))

    d.group('mid')
    layers = 6
    for k in range(1, layers):                                            # layers: mud, then plants, alternately
        y = bed - k * (bed - top) / layers
        if k % 2:
            pts = [(x0 + 2 + i * 4, y + (1.5 if i % 2 else -1.5)) for i in range((x1 - x0 - 4) // 4 + 1)]
            d.line(*pts)
        else:
            d.line((x0 + 2, y), (x1 - 2, y))
    for x in (x0, x1):                                                    # the wattle woven on the stakes
        pts = [(x + (2 if i % 2 else -2), top + 2 + i * 6) for i in range(int((bed - top) / 6))]
        d.line(*pts)
    for x in (x0 + 34, x0 + 60, x0 + 86, x0 + 112):                       # capillary rise to the roots
        d.line((x, water - 2), (x, top + 8))
        _arrow(d, (x, water - 2), (x, top + 8), size=3)

    d.group()
    for x in (x0 + 8, x1 - 8):                                            # ahuejote willows, narrow crowns
        d.line((x, top), (x, 58))
        d.ellipse(x, 52, 9, 34)
        for dx in (-10, -4, 4, 10):                                       # roots into the fill
            d.line((x, top), (x + dx, top + 16 + abs(dx)))
    for x in range(int(x0 + 30), int(x1 - 22), 18):                       # maize on the bed
        d.line((x, top), (x, top - 30))
        d.line((x, top - 12), (x - 7, top - 18))
        d.line((x, top - 18), (x + 7, top - 24))
        d.line((x, top - 24), (x - 6, top - 30))
    hull = [(cl[0] + 4 + i * 4, water - 3 + 4 * math.sin(math.pi * i / 8)) for i in range(9)]
    d.line((cl[0] + 2, water - 6), *hull, (cl[1] - 2, water - 6))         # a canoe in the canal

    d.group('mid')
    p, q = (cr[0] + 26, bed - 4), (cr[0] + 26, top + 18)                  # mud dredged from the canal
    d.line(p, (cr[0] + 26, water + 6))
    d.dashed((cr[0] + 26, water + 6), (x1 - 14, top + 6), dash=3, gap=3)
    _arrow(d, (cr[0] + 26, water + 6), (x1 - 14, top + 6), size=4)

    d.text(x1 + 62, (top + water) / 2 + 3, '60 CM', size=7, anchor='start')
    d.text((x0 + x1) / 2, 266, 'BED 5–10 M WIDE', size=7)
    d.text((cl[0] + cl[1]) / 2, water + 28, 'CANAL', size=7)
    d.text(cr[1] + 4, bed - 18, 'MUD DREDGED', size=7, anchor='start')
    d.text(cr[1] + 4, bed - 9, 'ONTO THE BED', size=7, anchor='start')
    d.text((x0 + x1) / 2, bed - 6, 'MUD AND PLANTS IN LAYERS', size=7)
    d.text(x0 + 22, 24, 'AHUEJOTE WILLOW', size=7, anchor='start')
    d.text(x0 - 6, bed + 22, 'STAKES AND WATTLE', size=7)
    d.text(14, bed + 22, 'LAKE BED', size=7, anchor='start')
    d.text((x0 + x1) / 2, water + 13, 'WATER RISES TO THE ROOTS', size=7)
    d.text(200, 292, 'A CHINAMPA IN SECTION · HEIGHT DRAWN AT TWICE THE WIDTH', size=7)
    return d


PLATES = {'open-fields': open_fields, 'chinampas': chinampas}
