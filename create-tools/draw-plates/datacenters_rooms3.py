"""Plates for The Cloud on the Ground's part rooms3 (sprint 059): the AI training cluster and the
gigawatt campus. See plates_for.py."""
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


def ai_cluster():
    """Meta's Llama 3 training network (Llama Team 2024, section 3.3.1) as a three-layer Clos:
    racks of 16 GPUs in two 8-GPU servers under a top-of-rack switch, 192 racks to a pod under its
    cluster switches, eight pods joined by aggregation switches. Two pods of four racks stand for
    eight of 192; the rack's 11.2 kW is the GPUs' rated 700 W each, our arithmetic."""
    d = D()
    y_agg, y_clu, y_tor = 44, 120, 186          # switch rows
    rack_top, floor = 196, 266
    pods = [(64, 188), (228, 372)]              # x extent of each pod
    racks_per_pod = 4
    rw = 26                                      # rack width

    def rack_xs(x0, x1):
        step = (x1 - x0 - rw) / (racks_per_pod - 1)
        return [x0 + i * step for i in range(racks_per_pod)]

    def clu_xs(x0, x1):
        return [x0 + 14 + i * (x1 - x0 - 28) / 3 for i in range(4)]

    agg_xs = [92 + i * 72 for i in range(4)]

    d.group('thin')
    d.line((10, floor), (390, floor))                                   # floor
    for y in (y_agg, y_clu, y_tor):                                     # layer datums
        d.dashed((10, y), (390, y), dash=2, gap=4)
    for (x0, x1) in pods:                                               # pod outlines
        d.dashed((x0 - 8, y_clu - 14), (x1 + 8, y_clu - 14), (x1 + 8, floor + 6),
                 (x0 - 8, floor + 6), (x0 - 8, y_clu - 14), dash=5, gap=4)

    d.group()
    for (x0, x1) in pods:
        for x in rack_xs(x0, x1):
            _box(d, x, rack_top, rw, floor - rack_top)                   # rack
            _box(d, x + 3, y_tor - 5, rw - 6, 10)                        # top-of-rack switch
        for cx in clu_xs(x0, x1):
            _box(d, cx - 8, y_clu - 5, 16, 10)                           # cluster switch
    for ax in agg_xs:
        _box(d, ax - 10, y_agg - 6, 20, 12)                              # aggregation switch

    d.group('mid')
    for (x0, x1) in pods:
        for x in rack_xs(x0, x1):
            # two servers of eight GPUs each
            for k, sy in enumerate((rack_top + 6, rack_top + 38)):
                _box(d, x + 3, sy, rw - 6, 26)
                for g in range(4):
                    for row in range(2):
                        d.line((x + 6 + g * 5, sy + 6 + row * 10), (x + 6 + g * 5, sy + 12 + row * 10))
            d.line((x + rw / 2, y_tor + 5), (x + rw / 2, rack_top))
            # every top-of-rack switch to every cluster switch in its pod
            for cx in clu_xs(x0, x1):
                d.line((x + rw / 2, y_tor - 5), (cx, y_clu + 5))
        # each cluster switch to two of the aggregation switches: the pod-to-pod layer is
        # oversubscribed, 1:7 in the paper
        for i, cx in enumerate(clu_xs(x0, x1)):
            for ax in agg_xs[i % 2::2]:
                d.line((cx, y_clu - 5), (ax, y_agg + 6))
        # ellipsis: the pod's other 188 racks
        for k in range(3):
            d.circle(x1 + 6, floor - 12 - k * 6, 0.8)
    for k in range(3):                                                  # the other six pods
        d.circle(208 - 4 + k * 4, 230, 1.0)

    d.group('labels')
    d.text(392, y_agg - 10, 'AGGREGATION', size=7, anchor='end')
    d.text(392, y_clu - 18, 'CLUSTER', size=7, anchor='end')
    d.text(10, y_tor - 8, 'TOP OF RACK', size=7, anchor='start')
    d.text(126, 280, 'POD: 192 RACKS, 3,072 GPUS', size=7)
    d.text(300, 280, '8 PODS IN ONE BUILDING', size=7)
    d.text(10, y_agg - 10, 'RACK: 16 GPUS, 11.2 KW', size=7, anchor='start')
    d.text(200, 296, 'LLAMA 3 405B: UP TO 16,384 H100s AT 700 W', size=7)
    return d


# The gigawatt campus: land and power, to one scale.
# Land: Hyperion 2,250 acres (Meta, as reported 2025); Abilene, the 1,045 acres Lancium owned in
# 2022 (Abilene Reporter-News); Fairwater, Wisconsin, 315 acres (Microsoft, 2025); a square mile,
# 640 acres, for scale. Power: dashed bars are what the company stated (Hyperion 5 GW, Meta 2025-26;
# Abilene 1.2 GW, Crusoe 2025); solid bars are IT power operating as Epoch AI estimated it in 2026
# (Abilene 824 MW, Fairwater 369 MW, Hyperion none yet).
CAMPUSES = [
    # name, acres, stated GW (or None), estimated running GW
    ('HYPERION', 2250, 5.0, 0.0),
    ('ABILENE', 1045, 1.2, 0.824),
    ('1 SQ MI', 640, None, None),
    ('FAIRWATER', 315, None, 0.369),
]


def gigawatt_campus():
    """Three AI campuses' land drawn to one scale in plan, as squares of their published acreage,
    with a square mile beside them; under each, its power as a bar: dashed for what the company
    stated, hatched for what Epoch AI estimated was running in 2026. A schematic of areas, not of
    the sites' shapes."""
    d = D()
    k = 112 / math.sqrt(2250)           # plate units per square root of an acre
    gap = 16
    base = 140                          # squares stand on this line
    sides = [k * math.sqrt(a) for (_, a, _, _) in CAMPUSES]
    total = sum(sides) + gap * (len(sides) - 1)
    x = (400 - total) / 2
    xs = []
    for s in sides:
        xs.append(x)
        x += s + gap
    gw = 18                             # plate units per gigawatt
    bar_base = 270
    bw = 14

    d.group('thin')
    d.line((8, base), (392, base))
    d.line((8, bar_base), (392, bar_base))
    for g in range(1, 6):               # gigawatt gridlines
        d.dashed((8, bar_base - g * gw), (392, bar_base - g * gw), dash=2, gap=5)

    d.group()
    for (name, acres, stated, running), x0, s in zip(CAMPUSES, xs, sides):
        if name == '1 SQ MI':
            continue
        _box(d, x0, base - s, s, s)

    d.group('mid')
    for (name, acres, stated, running), x0, s in zip(CAMPUSES, xs, sides):
        if name == '1 SQ MI':
            d.dashed((x0, base - s), (x0 + s, base - s), (x0 + s, base), (x0, base), (x0, base - s),
                     dash=4, gap=3)
            continue
        cx = x0 + s / 2
        if stated:
            h = stated * gw
            d.dashed((cx - bw, bar_base), (cx - bw, bar_base - h), (cx, bar_base - h), (cx, bar_base),
                     dash=3, gap=2)
        if running:
            h = running * gw
            poly = [(cx, bar_base), (cx + bw, bar_base), (cx + bw, bar_base - h), (cx, bar_base - h)]
            d.line(*poly, closed=True)
            d.lines(hatch(poly, 2.5, 45))
        else:
            d.line((cx, bar_base), (cx + bw, bar_base))

    d.group('labels')
    for (name, acres, stated, running), x0, s in zip(CAMPUSES, xs, sides):
        cx = x0 + s / 2
        d.text(cx, base + 11, name, size=7)
        d.text(cx, base + 20, f'{acres:,} AC', size=7)
    d.text(10, bar_base - 5 * gw - 4, '5 GW', size=7, anchor='start')
    d.text(10, bar_base - 1 * gw - 4, '1 GW', size=7, anchor='start')
    d.text(200, 286, 'DASHED: STATED · HATCHED: RUNNING, EST. 2026', size=7)
    d.text(200, 12, 'LAND TO ONE SCALE, AS SQUARES OF PUBLISHED ACREAGE', size=7)
    return d


PLATES = {'ai-cluster': ai_cluster, 'gigawatt-campus': gigawatt_campus}
