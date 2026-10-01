"""Plates for Keeping Watch's operating-room frames of part or2 (sprint 030): asepsis, hampton-gloves,
nurse-anesthetist, aorn. See plates_for.py."""
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


def _finger(base, ang, length, w, n=10):
    """A finger's outline as points: up its left side, round its tip, down its right side.
    `base` is the middle of its root, `ang` its direction in degrees (-90 is straight up)."""
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    px, py = -uy, ux                                        # the finger's left-to-right normal
    r = w / 2
    tip = (base[0] + ux * (length - r), base[1] + uy * (length - r))
    left = (base[0] - px * r, base[1] - py * r)
    pts = [left, (tip[0] - px * r, tip[1] - py * r)]
    a0 = math.degrees(math.atan2(-py, -px))
    for k in range(1, n):
        pts.append(_pt(*tip, r, a0 + 180 * k / n))
    pts.append((tip[0] + px * r, tip[1] + py * r))
    pts.append((base[0] + px * r, base[1] + py * r))
    return pts, tip


def hampton_gloves():
    d = D()
    # Left: one of the thin rubber gloves with gauntlets that Halsted ordered from the Goodyear Rubber
    # Company in the winter of 1889-90 (his 1913 account), drawn as a schematic: no pattern survives
    # here, so the proportions are a hand's. The fingers fan from one centre, drawn as construction.
    # Right: the hand disinfection the gloves were worn over, step by step, as Hunter Robb gave it for
    # the Johns Hopkins Hospital in 1894: soap and brush, permanganate, oxalic acid, rinses, sublimate.
    pivot = (104, 236)
    fingers = [(-112, 42, 13), (-98, 56, 14), (-86, 62, 14.5), (-74, 56, 14)]   # little..index
    roots = []
    for ang, _, _ in fingers:
        roots.append(_pt(*pivot, 112, ang))
    d.group('thin')
    for ang, ln, _ in fingers:                                            # the fingers' axes from one centre
        d.line(pivot, _pt(*pivot, 112 + ln + 8, ang))
    d.arc(*pivot, 112, -122, -62, n=30)                                   # the knuckle line
    d.line((30, 52), (30, 266))                                           # the glove's length, dimensioned
    d.line((25, 52), (35, 52))
    d.line((25, 266), (35, 266))
    d.group()
    outline = []
    for (ang, ln, w), root in zip(fingers, roots):
        pts, _ = _finger(root, ang, ln, w)
        outline.extend(pts)
    # the thumb, from the palm's right side
    tpts, _ = _finger((147, 170), -40, 50, 16)
    palm_left = (56, 176)
    wrist_l, wrist_r = (66, 206), (140, 206)
    d.line(wrist_l, palm_left, *outline, *tpts, (143, 190), wrist_r)
    # the gauntlet, flaring to its rolled edge
    d.line(wrist_l, (52, 262))
    d.line(wrist_r, (156, 262))
    d.arc(104, 262, 52, 0, 180, n=30, ry=6)
    d.arc(104, 262, 52, 180, 360, n=30, ry=6)
    d.group('mid')
    d.arc(104, 262, 46, 0, 180, n=24, ry=4)                               # the bead of the rolled edge
    for (ang, ln, w), root in zip(fingers, roots):                        # creases at the finger roots
        a = _pt(*root, w / 2 - 1, ang + 90)
        b = _pt(*root, w / 2 - 1, ang - 90)
        d.line(a, b)
    d.line(wrist_l, wrist_r)                                              # the wrist
    # the basins, top to bottom, each a bowl in section with its liquid
    bx, top, step = 236, 50, 47
    for k in range(5):
        y = top + k * step
        d.line((bx - 30, y), (bx + 30, y))
        d.arc(bx, y, 30, 0, 180, n=24, ry=15)
        d.line((bx - 24, y + 5), (bx + 24, y + 5))
        if k < 4:
            _arrow(d, (bx, y + 17), (bx, y + step - 4))
            d.line((bx, y + 17), (bx, y + step - 4))
    d.group('mid')
    d.text(30, 280, '1889–90', size=7)
    d.text(104, 34, 'THIN RUBBER · GAUNTLET', size=7)
    labels = ['SOAP · BRUSH · 10 MIN', 'KMnO4 · 2 MIN', 'OXALIC ACID', 'LIME-WATER · WATER', 'HgCl2 1:500 · 2 MIN']
    for k, s in enumerate(labels):
        d.text(bx + 36, top + k * step + 10, s, size=7, anchor='start')
    d.text(bx, 284, 'ROBB 1894', size=7)
    return d


def _wave(d, x, y0, y1, amp=3, n=16):
    """A rising wisp of steam: a sine wave from y0 up to y1 about x."""
    pts = [(x + amp * math.sin(2 * math.pi * k / n * 2), y0 + (y1 - y0) * k / n) for k in range(n + 1)]
    d.line(*pts)


def asepsis():
    d = D()
    # Left: a dressing sterilizer of the kind Schimmelbusch's Guide (1892; English 1894) describes, in
    # section: a tank of boiling 1 per cent soda over gas burners, with the instrument basket in it;
    # above, a closed chamber on a perforated floor, its lid lifted, holding a tin dressing box with
    # its holes open; steam rising through the floor drives the air out under the lid. Schematic
    # proportions. Right: the box's two states, holes open in the steam and closed for carrying.
    x0, x1 = 40, 236
    d.group('thin')
    d.line((x0 - 14, 214), (x1 + 14, 214))                                 # the water line, extended
    d.line((138, 40), (138, 278))                                           # the axis
    for y in (104, 176):                                                    # the box's rows of holes, projected
        d.line((x1, y), (268, y))
    d.group()
    d.line((x0, 196), (x0, 252), (x1, 252), (x1, 196))                      # the tank
    d.line((x0 - 6, 196), (x1 + 6, 196))                                    # its rim
    d.line((x0, 196), (x0, 72))                                             # the chamber's walls
    d.line((x1, 196), (x1, 72))
    d.line((x0 - 4, 72), (x1 + 4, 72))
    d.line((x0 - 4, 72), (x1 - 20, 44), (x1 - 14, 50))                     # the lid, lifted on its hinge
    d.line((x0 - 4, 72), (x0 - 4, 66))
    for k in range(9):                                                      # the burners under the tank
        x = x0 + 14 + k * 21
        d.line((x - 6, 272), (x + 6, 272))
        d.line((x, 272), (x, 266))
    d.group('mid')
    for k in range(23):                                                     # the perforated floor
        x = x0 + 6 + k * 8.4
        d.circle(x, 190, 1.4)
    d.line((x0, 186), (x1, 186))
    # the instrument basket in the soda
    d.line((70, 222), (70, 244), (206, 244), (206, 222))
    for k in range(1, 17):
        x = 70 + k * 8
        d.line((x, 222), (x, 244))
    d.line((70, 233), (206, 233))
    # the dressing box with its holes open
    bx0, bx1, by0, by1 = 78, 198, 94, 182
    d.line((bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1), closed=True)
    d.line((bx0 - 3, by0 - 14), (bx1 + 3, by0 - 14), (bx1 + 3, by0 - 1), (bx0 - 3, by0 - 1), closed=True)
    d.line((128, by0 - 14), (128, by0 - 20), (148, by0 - 20), (148, by0 - 14))
    for k in range(6):
        x = bx0 + 12 + k * 19
        d.circle(x, 104, 3)
        d.circle(x, 176, 3)
    # the steam, rising round the box and out under the lid
    for x in (54, 222):
        _wave(d, x, 184, 84)
    for x in (100, 138, 176):
        _wave(d, x, 212, 194, amp=2, n=8)
    _arrow(d, (54, 84), (54, 76))
    _arrow(d, (222, 84), (222, 76))
    # right: the box, holes open and holes closed
    for cx, closed in ((300, False), (360, True)):
        top = 104 if not closed else 124
        d.line((cx - 22, 124), (cx - 22, 190), (cx + 22, 190), (cx + 22, 124))
        d.line((cx - 24, top - 10), (cx + 24, top - 10), (cx + 24, top + 16), (cx - 24, top + 16), closed=True)
        for k in range(3):
            d.circle(cx - 12 + 12 * k, 130, 2.6)
            d.circle(cx - 12 + 12 * k, 184, 2.6)
    d.group('mid')
    d.text(138, 290, 'SODA 1% · BOILING', size=7)
    d.text(138, 152, 'DRESSINGS', size=7)
    d.text(138, 34, 'STEAM 100 °C', size=7)
    d.text(300, 206, 'OPEN', size=7)
    d.text(360, 206, 'CLOSED', size=7)
    d.text(330, 82, 'THE BOX', size=7)
    return d


def _rot(pts, c, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def nurse_anesthetist():
    d = D()
    # Open-drop ether as Alice Magaw described it in 1906: a four-ounce ether can, its cork cut with a
    # groove on either side, one groove packed with absorbent cotton that stands out about an inch as
    # the wick; the can tipped so ether drops from the wick on to an improved Esmarch inhaler, a wire
    # frame covered with two thicknesses of stockinet. Schematic: the drop rate she gave in no figures.
    # Right: the cork enlarged in plan, its two grooves, one with the cotton.
    tilt = 220                                                              # the can's axis turned so its mouth points down
    tip = (176, 128)                                                        # where the drops leave the wick
    d.group('thin')
    d.line((tip[0], tip[1]), (tip[0], 214))                                 # the line of the drops
    axis = _rot([(tip[0] - 150, tip[1]), (tip[0] + 10, tip[1])], tip, tilt - 180)
    d.line(*axis)                                                           # the can's axis
    d.arc(176, 236, 82, 180, 360, n=40, ry=46)                              # the dome's generating ellipse
    d.line((80, 236), (272, 236))                                           # the face plane
    d.group()
    # the can: a box 34 wide and 70 long, then a neck and the cork, along the axis
    L, W = 70, 34
    body = [(tip[0] - 36 - L, tip[1] - W / 2), (tip[0] - 36, tip[1] - W / 2), (tip[0] - 36, tip[1] + W / 2), (tip[0] - 36 - L, tip[1] + W / 2)]
    d.line(*_rot(body, tip, tilt - 180), closed=True)
    shoulder = [(tip[0] - 36, tip[1] - W / 2), (tip[0] - 24, tip[1] - 7), (tip[0] - 24, tip[1] + 7), (tip[0] - 36, tip[1] + W / 2)]
    d.line(*_rot(shoulder, tip, tilt - 180))
    cork = [(tip[0] - 26, tip[1] - 6), (tip[0] - 12, tip[1] - 5), (tip[0] - 12, tip[1] + 5), (tip[0] - 26, tip[1] + 6)]
    d.line(*_rot(cork, tip, tilt - 180), closed=True)
    # the inhaler: a dome of wire over an oval rim, and its handle
    d.arc(176, 236, 70, 180, 360, n=40, ry=40)
    d.arc(176, 236, 66, 180, 360, n=40, ry=36)
    d.line((106, 236), (246, 236))
    d.line((246, 236), (300, 252), (304, 248))
    d.group('mid')
    for k in range(1, 6):                                                   # the wire ribs of the frame
        a = 180 + 30 * k
        x = 176 + 70 * math.cos(math.radians(a))
        d.line((x, 236), (176 + 70 * math.cos(math.radians(a)), 236 + 40 * math.sin(math.radians(a))))
    wick = _rot([(tip[0] - 12, tip[1] + 2), (tip[0] + 2, tip[1] + 3), (tip[0] + 6, tip[1])], tip, tilt - 180)
    d.line(*wick)                                                           # the cotton wick
    for k, y in enumerate((150, 168, 186)):                                 # the drops, falling
        d.circle(tip[0], y, 2)
    # right: the cork in plan, enlarged, with its two grooves
    cx, cy, r = 336, 96, 30
    d.circle(cx, cy, r)
    for side in (-1, 1):
        x = cx + side * r
        d.line((x, cy - 7), (x - side * 9, cy - 7), (x - side * 9, cy + 7), (x, cy + 7))
    for k in range(5):                                                      # cotton in the right groove
        d.circle(cx + r - 5, cy - 4 + 2 * k, 1.2)
    d.group('mid')
    d.text(336, 146, 'CORK · 2 GROOVES', size=7)
    d.text(336, 156, 'WICK · AIR', size=7)
    d.text(66, 128, '4-OZ ETHER CAN', size=7)
    d.text(176, 258, 'STOCKINET × 2 · WIRE FRAME', size=7)
    d.text(198, 172, 'DROP', size=7, anchor='start')
    d.text(176, 280, 'MAGAW 1906 · OPEN DROP', size=7)
    return d


def aorn():
    d = D()
    # An operating room in plan, as the scrub and circulating roles divide it: the table with the draped
    # patient, the anesthetist at the head behind the screen, the Mayo stand over the patient's legs and
    # the instrument (back) table beside it; the sterile field drawn round the gowned team and the sterile
    # tables. The scrub works inside it, the circulator outside, on paths to the supply cupboard, the
    # sterilizer and the door. A schematic, not a survey of any room.
    d.group('thin')
    _box(d, 20, 20, 360, 260)                                               # the room's walls, as construction
    d.line((200, 30), (200, 270))                                           # the table's axis
    d.line((150, 150), (370, 150))
    d.group()
    _box(d, 176, 70, 48, 150)                                               # the operating table
    d.circle(200, 92, 13)                                                   # the patient's head, under the drapes
    d.line((176, 112), (224, 112))                                          # the anesthesia screen
    _box(d, 186, 186, 52, 26)                                               # the Mayo stand over the legs
    _box(d, 252, 170, 46, 88)                                               # the instrument (back) table
    d.line((20, 130), (12, 130), (12, 166), (20, 166))                      # the door
    _box(d, 30, 200, 30, 60)                                                # supply cupboard
    _box(d, 30, 40, 30, 50)                                                 # sterilizer
    d.group('mid')
    # the sterile field: the gowned team and the sterile tables, inside one boundary
    d.line((150, 118), (310, 118), (310, 266), (150, 266), closed=True)
    for x, y in ((156, 150), (244, 150), (240, 232)):                       # surgeon, assistant, scrub
        d.circle(x, y, 9)
    d.circle(200, 50, 9)                                                    # the anesthetist at the head
    d.circle(110, 180, 9)                                                   # the circulator, outside
    # the circulator's paths
    for q in ((62, 70), (62, 228), (24, 148), (146, 222)):
        d.line((110, 180), q)
        _arrow(d, (110, 180), q)
    d.group('mid')
    d.text(230, 276, 'STERILE FIELD', size=7)
    d.text(226, 250, 'SCRUB', size=7)
    d.text(110, 198, 'CIRCULATOR', size=7)
    d.text(200, 36, 'ANESTHESIA', size=7)
    d.text(212, 202, 'MAYO', size=7)
    d.text(275, 164, 'BACK TABLE', size=7)
    d.text(45, 106, 'STERILIZER', size=7)
    d.text(45, 196, 'SUPPLY', size=7)
    d.text(36, 124, 'DOOR', size=7)
    return d


PLATES = {
    'aorn': aorn,
    'asepsis': asepsis,
    'hampton-gloves': hampton_gloves,
    'nurse-anesthetist': nurse_anesthetist,
}
