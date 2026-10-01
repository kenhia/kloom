"""Plates for the chemistry subject's frames pcr, keeling-curve and where-chemistry-is (sprint 025, part `now`)."""
import math
from plates import D


def _pt(p, a, r):
    return (p[0] + r * math.cos(math.radians(a)), p[1] + r * math.sin(math.radians(a)))


def _parallel(a, b, k=3.2):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * k, dx / n * k
    return [[(a[0] + ox / 2, a[1] + oy / 2), (b[0] + ox / 2, b[1] + oy / 2)],
            [(a[0] - ox / 2, a[1] - oy / 2), (b[0] - ox / 2, b[1] - oy / 2)]]


def pcr():
    """The thermal cycler's program over three cycles, and the doubling it drives: 1, 2, 4, 8 duplexes."""
    d = D()
    x0, x1 = 40, 372                                # the time axis of the temperature program
    ty = {95: 44, 72: 78, 55: 104}                   # temperature -> y
    cyc = (x1 - x0 - 24) / 3                         # one cycle's width, after a short initial hold
    d.group('thin')
    for t, y in ty.items():
        d.line((x0, y), (x1, y))
    for k in range(4):
        x = x0 + 24 + k * cyc
        d.line((x, 34), (x, 114))
    d.line((x0, 124), (x1, 124))
    # the program: hold at 95, fall to 55 (anneal), rise to 72 (extend), rise to 95 (denature), three times
    pts = [(x0, ty[95]), (x0 + 24, ty[95])]
    for k in range(3):
        a = x0 + 24 + k * cyc
        seq = [(0.08, 55), (0.36, 55), (0.42, 72), (0.86, 72), (0.9, 95), (1.0, 95)]
        pts += [(a + f * cyc, ty[t]) for f, t in seq]
    d.group()
    d.line(*pts)
    # the doubling: after cycle k there are 2^k copies of the stretch between the primers
    cols = [60, 150, 240, 330]
    duplexes = []
    for k, cx in enumerate(cols):
        n = 2 ** k
        for i in range(n):
            duplexes.append((cx, 214 - 10 * (n - 1) / 2 + 10 * i))
    d.group('thin')
    d.line((20, 172), (380, 172))
    for cx in cols:
        d.line((cx, 176), (cx, 260))
    d.group()
    for cx, y in duplexes:
        d.lines([[(cx - 26, y - 1.8), (cx + 26, y - 1.8)], [(cx - 26, y + 1.8), (cx + 26, y + 1.8)]])
    d.group('mid')
    # primer ends marked on each duplex, and the arrows between columns
    ticks = []
    for cx, y in duplexes:
        ticks += [[(cx - 26, y - 4.5), (cx - 26, y + 4.5)], [(cx + 26, y - 4.5), (cx + 26, y + 4.5)]]
    d.lines(ticks)
    arrows = []
    for a, b in zip(cols, cols[1:]):
        m = (a + b) / 2
        arrows += [[(m - 8, 214), (m + 8, 214)], [(m + 3, 210), (m + 8, 214), (m + 3, 218)]]
    d.lines(arrows)
    d.text(x0 - 6, ty[95] + 3, '95', size=8, anchor='end')
    d.text(x0 - 6, ty[72] + 3, '72', size=8, anchor='end')
    d.text(x0 - 6, ty[55] + 3, '55', size=8, anchor='end')
    d.text(x0 - 6, 24, '°C', size=8, anchor='end')
    for k in range(3):
        d.text(x0 + 24 + (k + 0.5) * cyc, 138, f'CYCLE {k + 1}', size=7)
    for k, cx in enumerate(cols):
        d.text(cx, 282, str(2 ** k), size=10)
    d.text(200, 164, 'DENATURE · ANNEAL · EXTEND', size=8)
    return d


# Monthly mean CO2 at Mauna Loa, March 1958 to August 2026, in tenths of a ppm above 300
# (NOAA Global Monitoring Laboratory, co2_mm_mlo.txt, file of 5 September 2026; Scripps data to April 1974).
CO2 = (
    '157,174,175,173,159,149,132,124,133,147,156,165,166,177,183,182,165,148,138,133,148,156,164,'
    '170,176,190,200,196,182,159,142,138,150,162,169,177,185,195,206,198,186,168,150,153,161,170,'
    '179,186,197,206,210,206,196,174,162,154,167,177,187,191,199,214,222,215,197,178,162,160,171,'
    '184,196,200,208,218,222,219,204,187,167,169,177,187,194,204,209,221,222,219,212,189,178,173,'
    '189,194,206,216,224,237,241,238,224,204,186,181,198,210,223,225,230,244,250,241,225,209,192,'
    '194,207,220,226,232,239,250,256,254,241,221,203,202,213,229,240,244,256,267,274,267,259,237,'
    '224,218,228,241,251,260,269,281,281,277,263,247,231,231,240,251,262,267,272,278,289,286,274,'
    '254,234,236,248,260,268,276,278,297,301,291,280,263,248,252,265,276,286,296,303,315,325,321,'
    '309,293,275,272,282,286,294,307,315,326,332,322,311,292,273,273,283,296,307,315,319,331,340,'
    '334,320,300,285,284,294,308,316,327,334,347,347,340,331,307,290,287,302,316,327,332,350,361,'
    '369,362,349,326,313,313,325,336,349,353,367,377,380,380,365,344,324,324,338,349,361,367,383,'
    '388,392,393,375,357,340,342,353,368,379,383,401,409,414,414,394,377,362,361,373,383,393,406,'
    '416,426,430,425,408,385,370,370,386,399,409,418,428,440,448,439,424,402,384,384,394,408,416,'
    '428,434,454,461,458,443,425,405,405,418,432,442,449,457,474,478,472,458,437,416,419,433,450,'
    '455,464,479,487,493,486,469,453,435,434,447,461,468,475,482,499,505,500,482,462,455,448,462,'
    '475,487,489,498,514,522,516,502,482,467,467,481,493,505,517,525,537,544,539,528,505,490,494,'
    '504,516,531,534,541,557,560,554,540,518,501,503,516,529,539,551,558,564,574,564,549,531,514,'
    '517,531,544,549,558,573,588,592,582,563,540,523,524,539,552,563,572,580,592,597,594,572,550,'
    '530,534,544,557,571,574,586,594,603,596,574,558,541,542,555,570,584,590,601,614,618,609,595,'
    '576,559,562,576,591,600,610,620,634,638,633,618,593,583,581,596,608,622,634,643,647,652,651,'
    '637,616,597,597,610,624,632,642,646,665,668,657,645,624,604,610,626,645,654,661,674,688,696,'
    '691,680,661,642,645,657,673,684,693,698,712,711,705,696,671,650,655,669,683,694,697,708,720,'
    '718,719,700,683,672,672,685,698,708,717,726,736,740,734,717,698,683,686,699,714,727,734,743,'
    '752,759,757,742,720,709,707,724,740,751,758,766,779,788,785,769,746,733,733,748,762,772,780,'
    '791,805,808,799,776,762,744,746,763,777,786,799,810,825,826,824,809,789,769,772,785,803,816,'
    '824,829,848,852,842,826,806,790,793,804,820,831,841,848,867,868,863,847,822,812,814,827,842,'
    '858,861,863,873,888,880,866,843,834,832,844,858,872,877,890,898,904,897,882,863,850,846,862,'
    '876,889,904,914,927,932,924,904,885,870,874,889,900,915,920,928,934,944,940,927,903,893,892,'
    '905,921,933,940,946,964,969,959,946,926,913,913,932,946,958,970,977,986,1000,988,975,954,'
    '937,939,954,970,980,983,999,1015,1020,1014,993,972,955,962,974,991,1002,1006,1017,1034,1042,'
    '1030,1015,991,978,985,1003,1021,1027,1042,1051,1076,1079,1070,1046,1024,1012,1018,1037,1046,'
    '1064,1067,1075,1092,1099,1091,1073,1053,1036,1038,1053,1070,1082,1085,1096,1104,1114,1110,'
    '1089,1072,1057,1062,1082,1093,1110,1120,1122,1135,1149,1142,1120,1102,1088,1087,1105,1120,'
    '1136,1143,1147,1164,1173,1166,1146,1128,1115,1115,1131,1142,1155,1167,1176,1190,1191,1189,'
    '1169,1144,1133,1139,1150,1167,1181,1192,1188,1202,1210,1209,1188,1172,1159,1157,1175,1190,'
    '1195,1203,1210,1234,1240,1237,1218,1197,1185,1188,1205,1219,1228,1246,1254,1265,1269,1269,'
    '1256,1230,1220,1224,1238,1254,1266,1271,1282,1296,1305,1296,1279,1255,1244,1249,1265,1275,'
    '1286,1294,1302,1311,1323,1314,1291,1276'
)


def keeling_curve():
    """The Keeling curve plotted month by month from 1958, with one year's sawtooth drawn large."""
    d = D()
    vals = [300 + int(v) / 10 for v in ''.join(CO2).split(',')]
    t0 = 1958 + 2 / 12                                # March 1958
    xa, xb, ya, yb = 44, 380, 272, 30                 # plot box
    lo, hi = 305, 440

    def X(t):
        return xa + (t - 1958) / (2027 - 1958) * (xb - xa)

    def Y(v):
        return ya - (v - lo) / (hi - lo) * (ya - yb)

    d.group('thin')
    d.line((xa, yb), (xa, ya), (xb, ya))
    for v in (320, 360, 400, 430):
        d.line((xa, Y(v)), (xb, Y(v)))
    for yr in (1960, 1980, 2000, 2020):
        d.line((X(yr), ya), (X(yr), ya + 5))
    # the inset's frame, and the lines that tie it to the year it enlarges
    ix, iy, iw, ih = 66, 44, 120, 78
    d.line((ix, iy), (ix + iw, iy), (ix + iw, iy + ih), (ix, iy + ih), closed=True)
    d.group()
    pts = [(X(t0 + i / 12), Y(v)) for i, v in enumerate(vals)]
    d.line(*pts)
    d.group('mid')
    # 2025, month by month, drawn large in the inset
    i25 = (2025 - 1958) * 12 - 2
    yr = vals[i25:i25 + 12]
    vmin, vmax = min(yr), max(yr)
    ins = [(ix + 8 + k * (iw - 16) / 11, iy + ih - 10 - (v - vmin) / (vmax - vmin) * (ih - 24)) for k, v in enumerate(yr)]
    d.line(*ins)
    for p in ins:
        d.circle(p[0], p[1], 1.6)
    d.lines([[(ix + iw, iy + ih), (X(2025), Y(vmax) - 4)], [(X(2025), Y(vmax) - 4), (X(2026), Y(vmax) - 4)]])
    d.text(xa - 5, Y(320) + 3, '320', size=8, anchor='end')
    d.text(xa - 5, Y(360) + 3, '360', size=8, anchor='end')
    d.text(xa - 5, Y(400) + 3, '400', size=8, anchor='end')
    d.text(xa - 5, Y(430) + 3, '430', size=8, anchor='end')
    for yr_ in (1960, 1980, 2000, 2020):
        d.text(X(yr_), ya + 16, str(yr_), size=8)
    d.text(xa + 4, yb - 8, 'CO₂ PPM', size=8, anchor='start')
    d.text(ix + iw / 2, iy + ih + 12, '2025, JAN–DEC', size=7)
    d.text(ix + 10, iy + 12, 'MAY', size=7, anchor='start')
    return d


def where_chemistry_is():
    """PFOA, the best known of the forever chemicals: a zigzag of eight carbons sheathed in fluorine."""
    d = D()
    L = 34                                            # a bond, drawn
    dx, dy = L * math.cos(math.radians(30)), L * math.sin(math.radians(30))
    x0, ym = 64, 150
    cs = [(x0 + i * dx, ym + (dy / 2 if i % 2 == 0 else -dy / 2)) for i in range(8)]
    d.group('thin')
    d.line((30, ym - dy / 2), (370, ym - dy / 2))
    d.line((30, ym + dy / 2), (370, ym + dy / 2))
    # the 120-degree bond angle at the third carbon
    c = cs[2]
    d.arc(c[0], c[1], 12, 210, 330, n=16)
    d.group()
    d.line(*cs)
    # the carboxylic acid head on the eighth carbon: C=O up, C-OH along the chain
    head = cs[7]
    up = head[1] < ym
    o1 = _pt(head, -90 if up else 90, L * 0.9)
    o2 = _pt(head, 30 if up else -30, L)
    d.lines(_parallel(head, o1))
    d.line(head, o2)
    d.group('mid')
    # two fluorines on every CF2 carbon (one towards us, one away), three on the CF3 at the tail
    wedges, hashes, singles = [], [], []
    fpos = []
    for i, p in enumerate(cs[:7]):
        out = -90 if p[1] < ym else 90
        for s, kind in ((-28, 'w'), (28, 'h')):
            f = _pt(p, out + s, L * 0.78)
            fpos.append(f)
            if kind == 'w':
                a = math.atan2(f[1] - p[1], f[0] - p[0])
                n = (-math.sin(a) * 2.6, math.cos(a) * 2.6)
                wedges.append([p, (f[0] + n[0], f[1] + n[1]), (f[0] - n[0], f[1] - n[1]), p])
            else:
                for k in range(1, 6):
                    t = k / 6
                    q = (p[0] + (f[0] - p[0]) * t, p[1] + (f[1] - p[1]) * t)
                    a = math.atan2(f[1] - p[1], f[0] - p[0])
                    w = 0.6 + 2.2 * t
                    hashes.append([(q[0] - math.sin(a) * w, q[1] + math.cos(a) * w),
                                   (q[0] + math.sin(a) * w, q[1] - math.cos(a) * w)])
    tail = cs[0]
    f3 = _pt(tail, 210, L * 0.78)
    singles.append([tail, f3])
    fpos.append(f3)
    d.lines(wedges)
    d.lines(hashes)
    d.lines(singles)
    d.group('mid')
    for f in fpos:
        d.text(f[0], f[1] + (8 if f[1] > ym else -3), 'F', size=9)
    d.text(o1[0], o1[1] - 4, 'O', size=9)
    d.text(o2[0] + 12, o2[1] + 3, 'OH', size=9)
    c = cs[2]
    d.text(c[0], c[1] - 16, '120°', size=7)
    d.text(200, 262, 'PFOA · C₈HF₁₅O₂ · M = 414 g/mol', size=8)
    d.text(200, 280, 'C–F 1.35 Å · 4 ppt ≈ 6 × 10¹² MOLECULES A LITRE', size=8)
    return d


PLATES = {'pcr': pcr, 'keeling-curve': keeling_curve, 'where-chemistry-is': where_chemistry_is}
