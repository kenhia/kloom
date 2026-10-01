"""Plates for Keeping Watch's operating room, part or1: ether, Semmelweis, Lister (sprint 030). See plates_for.py."""
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


def _neck(d, cx, cy, r, a, w, length):
    """A glass neck leaving a globe of radius r at angle a: two walls of half-width w, open at the end.
    Each wall starts where it meets the circle, at a +/- asin(w/r)."""
    da = math.degrees(math.asin(w / r))
    ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
    nx, ny = -uy, ux
    ends = []
    for s, off in ((1, da), (-1, -da)):
        p = _pt(cx, cy, r, a + off)
        # the wall runs parallel to the neck's axis, w from it
        base = (cx + nx * w * s, cy + ny * w * s)
        t1 = (p[0] - base[0]) * ux + (p[1] - base[1]) * uy
        q = (base[0] + ux * (t1 + length), base[1] + uy * (t1 + length))
        d.line(p, q)
        ends.append(q)
    return ends, da


def ether():
    d = D()
    # Morton's inhaler of October 1846 as Bigelow described it in November: "a small two-necked glass
    # globe" holding the vapour "together with sponges to enlarge the evaporating surface"; air enters by
    # one neck and is drawn out through the other to the lungs, while a valve in the mouthpiece turns the
    # breath out into the room. A schematic in section, not a survey of the surviving replicas: Warren
    # wrote that Morton came late that morning because he was still modifying the apparatus.
    cx, cy, r = 168, 150, 66
    a_in, a_out = -128, 0
    d.group('thin')
    d.line((cx - r - 30, cy), (cx + r + 150, cy))                          # the axis of the breath
    d.line((cx, cy - r - 20), (cx, cy + r + 18))
    d.line((cx, cy), _pt(cx, cy, r + 60, a_in))                             # the inlet's axis
    d.circle(cx, cy, r + 8)                                                 # the glass's outer face
    level = cy + 34                                                         # the liquid ether's level
    half = math.sqrt(r * r - 34 * 34)
    d.line((cx - half - 14, level), (cx + half + 14, level))
    d.group()
    # the globe, broken where the two necks leave it
    (in_ends, da_in) = _neck(d, cx, cy, r, a_in, 11, 46)
    (out_ends, da_out) = _neck(d, cx, cy, r, a_out, 9, 40)
    d.arc(cx, cy, r, a_out + da_out, a_in + 360 - da_in, n=80)
    d.arc(cx, cy, r, a_in + da_in, a_out - da_out, n=40)
    # the mouthpiece tube, the valve chest and the flared mouthpiece
    x0 = cx + r + 40
    d.line((x0, cy - 9), (x0 + 22, cy - 9))
    d.line((x0, cy + 9), (x0 + 22, cy + 9))
    _box(d, x0 + 22, cy - 18, 34, 36)                                       # the valve chest
    d.line((x0 + 56, cy - 9), (x0 + 86, cy - 9), (x0 + 100, cy - 16))
    d.line((x0 + 56, cy + 9), (x0 + 86, cy + 9), (x0 + 100, cy + 16))
    d.line((x0 + 30, cy + 18), (x0 + 30, cy + 44))                          # the side port for the breath out
    d.line((x0 + 48, cy + 18), (x0 + 48, cy + 44))
    d.group('mid')
    # the liquid ether and the sponges lying in it
    d.line((cx - half, level), (cx + half, level))
    for k, (sx, sy, sr) in enumerate([(-30, 30, 15), (-2, 36, 17), (27, 30, 14), (-14, 14, 12), (14, 15, 12)]):
        pts = [_pt(cx + sx, cy + sy, sr * (1 + 0.12 * math.sin(math.radians(5 * t * 15) + k)), t * 15) for t in range(24)]
        d.line(*pts, closed=True)
    # the valve: a flap hinged at the top of the chest's port, shut against inspiration, open to the breath out
    hinge = (x0 + 30, cy + 18)
    d.line(hinge, _pt(*hinge, 18, 20))
    d.circle(*hinge, 2)
    # the air's path: in at the inlet, over the sponges, out to the patient; the breath back and out of the port
    p_in = _pt(cx, cy, r + 54, a_in)
    _arrow(d, p_in, _pt(cx, cy, r + 14, a_in), 6)
    d.line(p_in, _pt(cx, cy, r + 14, a_in))
    d.curve(f'M{cx - 34:.1f} {cy - 34:.1f} Q{cx - 10:.1f} {cy + 12:.1f} {cx + 40:.1f} {cy - 6:.1f}')
    _arrow(d, (cx + 20, cy - 2), (cx + 40, cy - 6), 6)
    d.line((x0 - 6, cy - 3), (x0 + 16, cy - 3))
    _arrow(d, (x0 - 6, cy - 3), (x0 + 16, cy - 3), 5)
    d.line((x0 + 39, cy + 22), (x0 + 39, cy + 52))
    _arrow(d, (x0 + 39, cy + 22), (x0 + 39, cy + 52), 5)
    d.group('mid')
    tx, ty = _pt(cx, cy, r + 64, a_in)
    d.text(tx - 2, ty - 6, 'AIR IN', size=7)
    d.text(cx, cy + r + 30, 'SPONGES IN ETHER', size=7)
    d.text(x0 + 39, cy - 26, 'VALVE', size=7)
    d.text(x0 + 92, cy - 24, 'TO PATIENT', size=7)
    d.text(x0 + 39, cy + 64, 'BREATH OUT', size=7)
    d.text(200, 286, "MORTON'S INHALER AFTER BIGELOW, 1846 · SCHEMATIC", size=7)
    return d


def semmelweis():
    d = D()
    # Left: the week's admissions to the Vienna maternity hospital as Semmelweis set them out (1861,
    # pp. 2-3). Admission passed between the two clinics every 24 hours at four in the afternoon, and once
    # a week the First Clinic took 48: so four days to the doctors' clinic and three to the midwives'.
    # The ring starts at Monday 4 p.m. at the top; each day is 360/7 degrees. Right: the path his finger
    # took on a morning in April 1847, from the dead-house to the labor ward, and the basin of
    # chlorinated lime solution put across it from the second half of May.
    cx, cy, R, r0 = 112, 150, 82, 50
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    first = [True, False, True, False, True, True, False]                 # 24 h from 4 p.m. each day
    step = 360 / 7
    d.group('thin')
    for k in range(7):
        a = -90 + k * step
        d.line(_pt(cx, cy, r0 - 12, a), _pt(cx, cy, R + 8, a))
    d.circle(cx, cy, r0 - 12)
    d.line((206, 150), (390, 150))
    d.group()
    d.circle(cx, cy, R)
    d.circle(cx, cy, r0)
    for k in range(7):
        a = -90 + k * step
        if first[k] != first[k - 1]:
            d.line(_pt(cx, cy, r0, a), _pt(cx, cy, R, a))
    # the dead-house: a slab on trestles; the basin in section; the labor ward's beds
    bx = 300
    _box(d, bx - 40, 34, 80, 8)
    d.line((bx - 30, 42), (bx - 34, 62))
    d.line((bx + 30, 42), (bx + 34, 62))
    d.arc(bx, 132, 36, 0, 180, n=36, ry=26)
    d.line((bx - 44, 132), (bx + 44, 132))
    for k in range(4):
        _box(d, bx - 78 + k * 42, 226, 30, 46)
        d.line((bx - 78 + k * 42, 236), (bx - 48 + k * 42, 236))
    d.group('mid')
    # the First Clinic's days hatched
    for k in range(7):
        if not first[k]:
            continue
        a0 = -90 + k * step
        for j in range(1, 6):
            a = a0 + j * step / 6
            d.line(_pt(cx, cy, r0 + 4, a), _pt(cx, cy, R - 4, a))
    d.line((bx - 32, 140), (bx + 32, 140))                                # the solution's surface
    d.line((bx - 26, 147), (bx + 26, 147))
    d.line((bx, 70), (bx, 100))
    _arrow(d, (bx, 70), (bx, 100), 6)
    d.line((bx, 166), (bx, 212))
    _arrow(d, (bx, 166), (bx, 212), 6)
    d.group('mid')
    for k, s in enumerate(days):
        x, y = _pt(cx, cy, R + 14, -90 + (k + 0.5) * step)
        d.text(x, y + 3, s, size=7)
    d.text(cx, cy - 4, 'FIRST 4', size=7)
    d.text(cx, cy + 8, 'SECOND 3', size=7)
    d.text(bx, 24, 'DEAD-HOUSE', size=7)
    d.text(bx + 64, 128, 'CHLORINATED', size=7)
    d.text(bx + 64, 138, 'LIME', size=7)
    d.text(bx, 288, 'LABOR WARD', size=7)
    d.text(cx, 288, 'ADMISSIONS FROM 4 P.M.', size=7)
    return d


def lister():
    d = D()
    # Lister's dressing for a compound fracture of the leg as his 1867 papers give it, in section along
    # the limb: the tibia broken under a wound; lint dipped in carbolic acid on the wound, which sets with
    # the blood into a crust; over it a putty of carbolic acid in boiled linseed oil (1 to 4) worked up
    # with whiting, a quarter of an inch thick, on a sheet of block tin about six inches square, held by
    # adhesive plaster. Proportions are a schematic's, not a survey's.
    cx = 200
    skin_t, skin_b = 190, 262
    p_top, tin = skin_t - 14, skin_t - 17                                  # the putty's face and the tin over it
    d.group('thin')
    d.line((cx, 112), (cx, 280))                                          # the wound's centre line
    d.line((20, (skin_t + skin_b) / 2), (380, (skin_t + skin_b) / 2))     # the limb's axis
    d.line((110, 132), (110, 146))                                        # the tin's six inches, dimensioned
    d.line((290, 132), (290, 146))
    d.line((110, 139), (290, 139))
    d.line((300, tin), (326, tin))                                        # the putty's quarter inch
    d.line((300, skin_t), (326, skin_t))
    d.line((320, tin), (320, skin_t))
    d.group()
    # the limb's skin, open at the wound
    d.line((24, skin_t + 6), (60, skin_t), (cx - 16, skin_t))
    d.line((cx + 16, skin_t), (340, skin_t), (376, skin_t + 6))
    d.line((24, skin_b - 6), (60, skin_b), (340, skin_b), (376, skin_b - 6))
    # the tibia, broken obliquely, the fragments' ends jagged
    bt, bb = 212, 238
    zig = [(cx - 8, bt), (cx - 2, bt + 6), (cx - 7, bt + 12), (cx + 1, bt + 18), (cx - 4, bb)]
    d.line((40, bt), zig[0])
    d.line(*zig)
    d.line(zig[-1], (40, bb))
    zig2 = [(x + 9, y + (3 if i % 2 else -2)) for i, (x, y) in enumerate(zig)]
    d.line((360, bt), (zig2[0][0], bt), *zig2[1:-1], (zig2[-1][0], bb), (360, bb))
    # the wound's track down to the fracture
    d.line((cx - 16, skin_t), (cx - 6, bt - 2))
    d.line((cx + 16, skin_t), (cx + 8, bt - 2))
    # the block tin, the putty spread on its underside lying on the skin
    d.line((110, tin), (290, tin))
    d.line((114, tin), (114, skin_t))
    d.line((286, tin), (286, skin_t))
    d.group('mid')
    # the lint and blood crust in the wound's mouth, under the putty
    d.line((cx - 14, skin_t), (cx + 14, skin_t), (cx + 6, skin_t + 10), (cx - 6, skin_t + 10), closed=True)
    # the putty's body, hatched
    for k in range(19):
        x = 117 + k * 9
        d.line((x, tin + 2), (x + 6, skin_t - 1))
    # adhesive plaster over the tin's edges onto the skin, each side
    for s in (-1, 1):
        x = cx + s * 90
        d.line((x - s * 22, tin - 3), (x + s * 4, tin - 3), (x + s * 14, skin_t - 1), (x + s * 44, skin_t - 1))
    # the medullary canal
    d.line((50, 225), (cx - 10, 225))
    d.line((cx + 12, 225), (350, 225))
    d.line((cx + 10, skin_t + 6), (cx + 52, 160))                         # leader to the lint
    d.group('mid')
    d.text(cx, 128, 'BLOCK TIN ABOUT 6 IN', size=7)
    d.text(352, skin_t - 5, '1/4 IN', size=7)
    d.text(cx, 72, 'PASTE: CARBOLIC ACID 1, LINSEED OIL 4,', size=7)
    d.text(cx, 84, 'WORKED UP WITH WHITING, UNDER TIN', size=7)
    d.text(cx + 82, 157, 'CARBOLIC RAG + CRUST', size=7)
    d.text(80, 252, 'TIBIA', size=7)
    d.text(320, 280, 'SKIN', size=7)
    d.text(64, 166, 'PLASTER', size=7)
    d.text(cx, 294, 'COMPOUND FRACTURE DRESSING · LISTER 1867 · SCHEMATIC', size=7)
    return d


PLATES = {
    'ether': ether,
    'semmelweis': semmelweis,
    'lister': lister,
}
