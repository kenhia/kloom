"""Plates for Keeping Watch's Nurses at war, its middle part (sprint 030): the First World War,
Pearl Harbor and Bataan. See plates_for.py."""
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


def _cross(d, cx, cy, w, h, t):
    """A Red Cross outline, `w` wide and `h` tall, its arms `t` thick, centred on (cx, cy)."""
    a, b, c = w / 2, h / 2, t / 2
    d.line((cx - c, cy - b), (cx + c, cy - b), (cx + c, cy - c), (cx + a, cy - c), (cx + a, cy + c),
           (cx + c, cy + c), (cx + c, cy + b), (cx - c, cy + b), (cx - c, cy + c), (cx - a, cy + c),
           (cx - a, cy - c), (cx - c, cy - c), closed=True)


def wwi_nurses():
    d = D()
    # The Carrel-Dakin apparatus, after Carrel and Dehelly's manual (1917). Right, in elevation: a
    # one-litre flask of Dakin's solution hung on a wooden standard 50 cm to 1 m above the bed, a
    # pinchcock 10 cm below it, and the tube running down to a wound of the thigh. Left, enlarged:
    # the wound in section, with four red-rubber tubes, closed at the end and pierced with small
    # holes, laid into its recesses and joined above the skin by a glass distributor like a comb.
    # The elevation is drawn at about 1 m to 115 units; the detail is not to scale.
    bed = 215                                                    # the top of the mattress
    px = 344                                                     # the standard
    fx, fy, fr = 318, 74, 15                                     # the flask's body
    out = fy + fr + 12                                           # the flask's outlet
    w = (286, 204)                                               # the wound on the main drawing
    dc, dr = (100, 150), 80                                      # the detail circle
    d.group('thin')
    d.circle(*dc, dr)
    d.circle(*w, 8)
    for a in (-30, 30):                                          # leaders from the wound to its detail
        d.line(_pt(*w, 8, 180 + a), _pt(*dc, dr, -a * 0.8))
    d.line((372, out), (372, bed))                               # the height, dimensioned
    d.line((366, out), (378, out))
    d.line((366, bed), (378, bed))
    d.line((296, out), (366, out))
    d.line((196, bed), (380, bed))                               # the bed's level, run out
    d.group()
    # the bed: mattress, rail and legs, and the leg lying on it
    _box(d, 204, bed, 144, 12)
    d.line((204, bed + 22), (348, bed + 22))
    d.line((210, bed + 12), (210, 274))
    d.line((342, bed + 12), (342, 274))
    d.line((214, bed), (214, 200), (230, 194), (300, 196), (322, 200), (330, bed))
    # the standard and its bracket, and the flask hung neck down
    d.line((px - 3, 36), (px + 3, 36), (px + 3, bed + 22), (px - 3, bed + 22), closed=True)
    d.line((px - 3, 44), (fx - 4, 44), (fx - 4, 50))
    d.line((fx, 50), (fx, fy - fr))
    d.circle(fx, fy, fr)
    d.line((fx - 4, fy + fr - 1), (fx - 3, out), (fx + 3, out), (fx + 4, fy + fr - 1))
    # the tube: down through the pinchcock and over the bed to the wound
    d.curve(f'M{fx} {out} L{fx} {out + 40} C{fx} {out + 80} {w[0] + 30} {w[1] - 40} {w[0]} {w[1]}')
    # the detail: the skin, the wound's cavity, the distributor and four perforated tubes
    cx, cy = dc
    d.line((cx - 70, cy - 4), (cx - 40, cy), (cx + 40, cy), (cx + 70, cy - 4))
    d.curve(f'M{cx - 40} {cy} C{cx - 44} {cy + 30} {cx - 20} {cy + 58} {cx} {cy + 52} '
            f'C{cx + 18} {cy + 48} {cx + 46} {cy + 40} {cx + 40} {cy}')
    gy = cy - 46                                                 # the glass distributor
    d.line((cx - 32, gy - 3), (cx + 30, gy - 3), (cx + 34, gy), (cx + 30, gy + 3), (cx - 32, gy + 3), closed=True)
    d.line((cx + 34, gy), (cx + 52, gy - 26), (cx + 66, gy - 34))
    tubes = [(-24, 34), (-8, 50), (8, 46), (24, 30)]             # branch offset, depth below the skin
    for k, (dx, depth) in enumerate(tubes):
        x0 = cx + dx
        x1 = cx + dx * 0.7
        d.line((x0, gy + 3), (x0, gy + 12), (x1, cy - 4), (x1, cy + depth))
    d.group('mid')
    # the liquid in the flask, the pinchcock's jaws and spring, the holes along each tube
    d.line(_pt(fx, fy, fr, 200), _pt(fx, fy, fr, 340))
    pc = out + 14
    d.line((fx - 7, pc - 2), (fx + 7, pc - 2))
    d.line((fx - 7, pc + 2), (fx + 7, pc + 2))
    d.line((fx + 7, pc - 2), (fx + 11, pc), (fx + 7, pc + 2))
    for dx, depth in tubes:
        x1 = cx + dx * 0.7
        for y in range(int(cy + 6), int(cy + depth), 7):
            d.circle(x1, y, 1.1)
        d.line((x1 - 2.5, cy + depth), (x1 + 2.5, cy + depth))
    # the solution bathing the cavity
    for k in range(3):
        y = cy + 14 + 12 * k
        d.line((cx - 36 + 4 * k, y), (cx + 36 - 4 * k, y))
    d.group('mid')
    d.text(fx - 22, fy - 2, '1 L FLASK', size=7, anchor='end')
    d.text(fx - 22, fy + 8, 'DAKIN 0.5%', size=7, anchor='end')
    d.text(fx - 12, pc + 3, 'PINCHCOCK', size=7, anchor='end')
    d.text(377, bed + 14, '50 CM–1 M', size=7)
    d.text(cx - 14, gy - 12, 'GLASS DISTRIBUTOR', size=7)
    d.text(cx, cy + dr + 14, 'PERFORATED TUBES IN THE WOUND', size=7)
    d.text(282, 290, 'EVERY 2 H · 20–100 CC', size=7)
    return d


def pearl_harbor():
    d = D()
    # The burn routine aboard Solace (Eckert and Mader, 1942), as apparatus. Left: a Flit gun, the
    # household insecticide sprayer the nurses filled with tannic acid, in section: a pump cylinder
    # whose piston drives air out of a nozzle, across the top of a siphon tube rising from a tank
    # below, which draws the liquid up and breaks it into a cone of spray. Right: a bed cradle in end
    # section, the hoops that held the sheet off a burned man, warmed when need be by one bulb.
    # Proportions are a typical sprayer's, not a measured one.
    ay = 108                                                       # the pump's axis
    x0, x1, r = 52, 200, 11                                        # the pump cylinder
    nz = (216, ay)                                                 # the nozzle's tip
    tx, tw, ty, th = 196, 48, 136, 70                              # the tank
    sx = 220                                                       # the siphon tube
    cone = 44                                                      # the spray's axis, degrees below +x
    cx, cy, R = 326, 236, 52                                       # the cradle's hoops
    d.group('thin')
    d.line((26, ay), (300, ay))                                    # the pump's axis, run out
    for a in (cone - 11, cone + 11):                               # the cone's edges
        d.line(nz, _pt(nz[0], nz[1], 118, a))
    d.line((sx, ty + th - 6), (sx, ay - 14))                       # the siphon's axis
    d.line((cx, cy), (cx, cy - R - 18))                            # the cradle's centre line
    d.line((cx - R - 22, cy), (cx + R + 22, cy))
    d.arc(cx, cy, R, 180, 360, n=40)
    d.group()
    # the pump: cylinder, front cap tapering to the nozzle, the rod and its T-handle
    d.line((x0, ay - r), (x1, ay - r), (nz[0] - 4, ay - 3), nz, (nz[0] - 4, ay + 3), (x1, ay + r), (x0, ay + r))
    d.line((x0, ay - r), (x0, ay + r))
    d.line((x0, ay - 2), (22, ay - 2))
    d.line((x0, ay + 2), (22, ay + 2))
    d.line((18, ay - 16), (18, ay + 16), (24, ay + 16), (24, ay - 16), closed=True)
    # the tank under the nozzle, and the neck that joins it to the cylinder
    _box(d, tx, ty, tw, th)
    d.line((tx + 10, ty), (tx + 10, ay + r))
    d.line((tx + 18, ty), (tx + 18, ay + r))
    # the siphon tube, from near the tank's floor to just ahead of the nozzle
    d.line((sx - 1.5, ty + th - 6), (sx - 1.5, ay + 4))
    d.line((sx + 1.5, ty + th - 6), (sx + 1.5, ay + 4))
    # the cradle: mattress, bed frame, two hoops, the sheet over them
    _box(d, cx - R - 14, cy, 2 * R + 28, 12)
    d.line((cx - R - 10, cy + 12), (cx - R - 10, cy + 40))
    d.line((cx + R + 10, cy + 12), (cx + R + 10, cy + 40))
    d.arc(cx, cy, R + 4, 180, 360, n=40)
    d.group('mid')
    # the piston, its leather cup, and the air driven forward
    _box(d, 92, ay - r + 2, 8, 2 * r - 4)
    d.line((100, ay - r + 2), (106, ay - r + 2))
    d.line((100, ay + r - 2), (106, ay + r - 2))
    _arrow(d, (130, ay), (160, ay))
    # the liquid in the tank
    lev = ty + 22
    d.line((tx, lev), (tx + tw, lev))
    for k in range(1, 6):
        y = lev + k * (th - 22) / 6
        d.line((tx + 4, y), (sx - 6, y))
        d.line((sx + 6, y), (tx + tw - 4, y))
    # the spray: rays and droplets along the cone
    for a in (cone - 7, cone, cone + 7):
        d.line(_pt(nz[0], nz[1], 14, a), _pt(nz[0], nz[1], 60, a))
    for k, a in enumerate(range(cone - 9, cone + 10, 3)):
        for rr in (70 + 6 * (k % 3), 88 + 5 * (k % 2)):
            x, y = _pt(nz[0], nz[1], rr, a)
            d.circle(x, y, 0.9)
    # the man under the cradle: a body in section on the mattress
    d.ellipse(cx, cy - 11, 30, 11)
    # the bulb hung from the hoop's crown, and its warmth
    d.line((cx, cy - R), (cx, cy - R + 14))
    d.circle(cx, cy - R + 19, 5)
    for a in range(20, 170, 30):
        d.line(_pt(cx, cy - R + 19, 9, a), _pt(cx, cy - R + 19, 15, a))
    d.group('mid')
    d.text(126, ay - r - 8, 'PUMP', size=7)
    d.text(18, ay + 28, 'HANDLE', size=7)
    d.text(tx + tw / 2, ty + th + 12, 'TANK · TANNIC ACID', size=7)
    d.text(sx + 26, ay - 18, 'NOZZLE', size=7)
    d.text(tx - 24, ty + 40, 'SIPHON', size=7)
    d.text(cx, cy + 56, 'BED CRADLE · ONE BULB', size=7)
    d.text(122, 262, 'SPRAYED EVERY HOUR', size=7)
    d.text(122, 272, 'UNTIL A CRUST FORMED · ABOUT 24 H', size=7)
    return d


def bataan():
    d = D()
    # General Hospital No. 2 on Bataan, a schematic from the Army's medical history (Condon-Rall and
    # Cowdrey, 1998): wards strung for about 1,500 yards along the south bank of the Real River,
    # inside three red crosses, each 40 by 60 feet, laid at the corners of an equilateral triangle a
    # mile from apex to base. Drawn at 1 mile to 200 units (so the triangle's side is 2/sqrt(3) mile);
    # the river's course and the triangle's orientation are not known, and the crosses are enlarged.
    k = 200 / 1760                                               # units per yard
    h = 1760 * k
    side = 2 * h / math.sqrt(3)
    apex, by = (200, 44), 44 + h                                 # the apex and the base's line
    A, B, C = apex, (200 - side / 2, by), (200 + side / 2, by)
    ry = 196                                                     # the river's mean line
    half = 750 * k                                               # half the hospital's length

    def river(x, off=0):
        return ry + off + 6 * math.sin((x - 30) / 34) + 3 * math.sin((x - 30) / 13)
    d.group('thin')
    d.line(A, B, C, closed=True)                                 # the triangle
    d.line(A, (200, by))                                         # its altitude, a mile
    for p in (A, B, C):
        d.circle(*p, 12)
    d.line((200 - half, ry + 34), (200 + half, ry + 34))         # the hospital's length
    for x in (200 - half, 200 + half):
        d.line((x, ry + 28), (x, ry + 40))
    d.line((40, 286), (40 + 500 * k, 286))                       # a scale of 500 yards
    for x in (40, 40 + 250 * k, 40 + 500 * k):
        d.line((x, 282), (x, 290))
    d.group()
    # the river, its two banks
    for off in (-5, 5):
        d.line(*[(x, river(x, off)) for x in range(30, 372, 4)])
    # the three crosses
    for p in (A, B, C):
        _cross(d, p[0], p[1], 15, 15, 5)
    d.group('mid')
    # the wards along the south bank: cots in rows, and the trees over them
    x = 200 - half
    while x < 200 + half - 6:
        y = river(x + 5, 5) + 5
        _box(d, x, y, 10, 6)
        d.line((x + 2, y + 2), (x + 8, y + 2))
        x += 14
    for i in range(26):
        tx = 200 - half + 4 + i * 2 * half / 26
        ty = river(tx, 5) + 18 + 4 * math.sin(i * 1.7)
        d.circle(tx, ty, 3.4)
    d.group('mid')
    d.text(200, by + 16, 'A MILE FROM APEX TO BASE', size=7)
    d.text(208, 118, '1 MILE', size=7, anchor='start')
    d.text(200, ry + 46, 'WARDS ALONG 1,500 YD OF BANK', size=7)
    d.text(352, ry - 12, 'REAL RIVER', size=7)
    d.text(apex[0] + 18, apex[1] + 3, 'RED CROSS 40 × 60 FT', size=7, anchor='start')
    d.text(40 + 250 * k, 278, '500 YD', size=7)
    d.text(330, 286, 'A SCHEMATIC', size=7)
    return d


PLATES = {
    'wwi-nurses': wwi_nurses,
    'pearl-harbor': pearl_harbor,
    'bataan': bataan,
}
