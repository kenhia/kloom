"""Plates for In the Blood's What we learned, first half: Harvey, Malpighi, Leeuwenhoek (sprint 028). See plates_for.py."""
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


def harvey():
    d = D()
    # Above: a forearm in elevation, bound above the elbow (left, towards the heart) as for
    # bloodletting, a vein swollen below the cord with knots at its valves. Below: that vein
    # enlarged in section, its valve cusps opening towards the heart; a finger has pressed the
    # blood out from H up to the valve O, and the stretch between stays empty. Not to scale.
    valves = [120, 220, 300]
    y0, y1 = 186, 234                                               # the vein's walls in section
    yc = (y0 + y1) / 2
    d.group('thin')
    for x in valves:                                                # each knot carried down to its valve
        d.line((x, 92), (x, y0 - 8))
    d.line((30, yc), (372, yc))                                     # the vein's axis
    d.group()
    # the arm: upper and lower outlines tapering to the wrist, and a fist round a staff
    top = [(x, 52 + 0.045 * (x - 40) + 3 * math.sin((x - 40) / 46)) for x in range(40, 336, 8)]
    bot = [(x, 120 - 0.06 * (x - 40) - 2 * math.sin((x - 40) / 52)) for x in range(40, 336, 8)]
    d.line(*top)
    d.line(*bot)
    d.arc(352, 86, 20, -100, 250, n=36, ry=24)                      # the fist
    d.line((360, 52), (366, 124))                                   # the staff it grips
    d.line((356, 52), (362, 124))
    # the vein in section, its walls broken where the pressed stretch has collapsed (O to H)
    d.line((30, y0), (224, y0), (234, yc - 4), (276, yc - 4), (286, y0), (372, y0))
    d.line((30, y1), (224, y1), (234, yc + 4), (276, yc + 4), (286, y1), (372, y1))
    d.group('mid')
    # the cord above the elbow: a band with its knot
    d.line((60, 52), (60, 120))
    d.line((70, 52), (70, 119))
    d.line((65, 52), (58, 42), (72, 40), (65, 52))
    # the swollen vein along the forearm, with a knot at each valve
    vein = [(x, 92 + 4 * math.sin((x - 72) / 30)) for x in range(72, 330, 6)]
    d.line(*vein)
    for x in valves:
        y = 92 + 4 * math.sin((x - 72) / 30)
        d.ellipse(x, y, 5, 3.4)
    # valve cusps: from each wall, free edges pointing left, towards the heart
    for x in valves:
        h = (y1 - y0) / 2 - 2
        d.line((x + 4, y0), (x - 6, y0 + h * 0.6), (x - 18, yc - 2))
        d.line((x + 4, y1), (x - 6, y1 - h * 0.6), (x - 18, yc + 2))
    # the finger pressing at H
    d.arc(281, yc - 14, 9, 0, 180, n=12)
    d.line((272, yc - 14), (272, y0 - 30))
    d.line((290, yc - 14), (290, y0 - 30))
    # the flow towards the heart in the full stretches
    d.line((360, yc), (330, yc))
    _arrow(d, (360, yc), (330, yc))
    d.line((200, yc), (140, yc))
    _arrow(d, (200, yc), (140, yc))
    d.group('mid')
    d.text(65, 34, 'CORD', size=7)
    d.text(220, y1 + 16, 'O', size=7)
    d.text(281, y1 + 16, 'H', size=7)
    d.text(254, y1 - 8, 'EMPTY', size=7)
    d.text(120, y1 + 16, 'VALVE', size=7)
    d.text(30, y0 - 10, 'TO HEART', size=7, anchor='start')
    return d


def malpighi():
    d = D()
    # Left: Malpighi's second way to look, in section: a lamp below, its light sent up a tube,
    # the dried lung on a crystal plate, and a microscope of two lenses above. Right: what the
    # glass showed, the air sacs as a honeycomb of polygons, each ringed by small vessels, between
    # a branch of the artery coming in and a branch of the vein going out. Not to scale.
    cx, cy, rf = 288, 150, 88                                       # the field of view
    ax = 92                                                         # the apparatus's optical axis
    d.group('thin')
    for dx in (-10, -4, 4, 10):                                     # light rising from the flame
        d.line((ax + dx * 0.3, 236), (ax + dx, 150))
        d.line((ax + dx, 150), (ax + dx * 0.2, 64))
    d.line((ax, 280), (ax, 24))
    d.circle(cx, cy, rf)                                            # the field's edge
    d.line((ax + 20, 54), (cx - rf, cy))                            # from the eyepiece to the view
    d.group()
    # the lamp: a bowl, a wick and a flame
    d.arc(ax, 262, 26, 0, 180, n=20, ry=12)
    d.line((ax - 26, 262), (ax + 26, 262))
    d.curve(f'M{ax} 258 C {ax - 7} 250 {ax - 4} 240 {ax} 232 C {ax + 4} 240 {ax + 7} 250 {ax} 258')
    # the tube that carries the light up to the plate
    d.line((ax - 14, 228), (ax - 14, 160))
    d.line((ax + 14, 228), (ax + 14, 160))
    # the crystal plate on its stand, and the lung laid on it
    d.line((ax - 46, 156), (ax + 46, 156), (ax + 46, 150), (ax - 46, 150), closed=True)
    d.line((ax - 40, 156), (ax - 40, 240))
    d.line((ax + 40, 156), (ax + 40, 240))
    # the microscope: a tube with an objective lens below and an eye lens above
    d.line((ax - 12, 132), (ax - 12, 50))
    d.line((ax + 12, 132), (ax + 12, 50))
    d.ellipse(ax, 128, 12, 3.5)
    d.ellipse(ax, 54, 12, 3.5)
    # the honeycomb of air sacs inside the field
    s = 15
    cells = []
    for q in range(-7, 8):
        for r in range(-7, 8):
            x = cx + s * math.sqrt(3) * (q + r / 2)
            y = cy + s * 1.5 * r
            if math.hypot(x - cx, y - cy) < rf - s:
                cells.append((x, y))
    for x, y in cells:
        d.line(*[_pt(x, y, s, 30 + 60 * k) for k in range(6)], closed=True)
    d.group('mid')
    # the lung on the plate, and the vessels ringing each air sac
    d.ellipse(ax, 147, 26, 3)
    for x, y in cells:
        d.line(*[_pt(x, y, s * 0.72, 30 + 60 * k + 8 * ((k % 2) * 2 - 1)) for k in range(6)], closed=True)
    # an artery's branch coming in from the left and a vein's leaving to the right, both
    # running along the cell walls
    art = [(cx - rf - 6, cy + 8), (cx - 62, cy + 6), (cx - 39, cy - 7), (cx - 13, cy - 7)]
    vein = [(cx + rf + 6, cy - 4), (cx + 64, cy - 8), (cx + 39, cy + 7), (cx + 13, cy + 7)]
    d.line(*art)
    d.line((cx - 62, cy + 6), (cx - 52, cy + 22), (cx - 39, cy + 30))
    d.line(*vein)
    d.line((cx + 64, cy - 8), (cx + 52, cy - 22), (cx + 39, cy - 30))
    _arrow(d, art[0], (cx - 74, cy + 7))
    _arrow(d, (cx + 70, cy - 6), vein[0])
    d.group('mid')
    d.text(ax, 290, 'LAMP', size=7)
    d.text(ax + 52, 146, 'PLATE', size=7, anchor='start')
    d.text(ax - 18, 92, 'TWO LENSES', size=7, anchor='end')
    d.text(cx - rf + 4, cy + 28, 'ARTERY', size=7, anchor='end')
    d.text(cx + rf - 4, cy - 22, 'VEIN', size=7, anchor='start')
    d.text(cx, cy + rf + 16, 'AIR SACS RINGED BY VESSELS', size=7)
    return d


def red_cells():
    d = D()
    # Left: one of Leeuwenhoek's microscopes as Henry Baker drew it in 1753, from the side the
    # specimen is on: two riveted plates holding a single lens, a pin on a stage before it, a long
    # screw to raise the stage. Below it, a glass tube as thin as a hair, holding blood. Right:
    # his measure. A fine grain of sand and, across its diameter, the 29 globules that a volume
    # ratio of 25,000 gives (the cube root of 25,000 is 29.2), drawn to scale with each other.
    px0, px1, py0, py1 = 40, 112, 30, 160                           # the plate
    lens = ((px0 + px1) / 2, 52)
    gx, gy, gr = 292, 140, 72                                       # the grain of sand
    n = 29
    d.group('thin')
    d.line((lens[0], 18), (lens[0], 250))                           # the lens's axis
    d.line((gx - gr - 14, gy), (gx + gr + 14, gy))                  # the grain's diameter
    for x in (gx - gr, gx + gr):
        d.line((x, gy - gr - 10), (x, gy + gr + 22))
    d.group()
    # the plate and the lens's hole
    d.line((px0, py0), (px1, py0), (px1, py1), (px0, py1), closed=True)
    d.circle(lens[0], lens[1], 7)
    d.circle(lens[0], lens[1], 2.5)
    # the long screw from below, through the bracket, up to the stage
    d.line((lens[0] - 3, 240), (lens[0] - 3, 92))
    d.line((lens[0] + 3, 240), (lens[0] + 3, 92))
    d.line((lens[0] - 6, 210), (lens[0] + 6, 210), (lens[0] + 6, 218), (lens[0] - 6, 218), closed=True)
    d.ellipse(lens[0], 246, 6, 8)
    # the stage, and the pin rising from it to the lens
    d.line((px0 + 8, 92), (px1 + 12, 92), (px1 + 12, 80), (px0 + 8, 80), closed=True)
    d.line((lens[0], 80), (lens[0], 60))
    # the grain of sand: a round grain with a slightly irregular edge
    grain = [_pt(gx, gy, gr * (1 + 0.03 * math.sin(3 * t * math.pi / 24) + 0.02 * math.sin(7 * t * math.pi / 24)), t * 7.5)
             for t in range(48)]
    d.line(*grain, closed=True)
    d.group('mid')
    for x, y in ((px0 + 6, py0 + 6), (px1 - 6, py0 + 6), (px0 + 6, 96), (px1 - 6, 96), (px0 + 6, py1 - 6), (px1 - 6, py1 - 6)):
        d.circle(x, y, 1.6)                                         # the rivets
    for y in range(100, 206, 6):                                    # the screw's thread
        d.line((lens[0] - 3, y), (lens[0] + 3, y + 3))
    # the thin glass tube of blood, with globules in it
    d.line((24, 270), (150, 270))
    d.line((24, 276), (150, 276))
    for k in range(18):
        d.circle(30 + k * 6.6, 273, 2)
    # the globules across the grain, each 2r/29 wide
    g = 2 * gr / n
    for k in range(n):
        d.circle(gx - gr + g / 2 + k * g, gy, g / 2)
    d.group('mid')
    d.text(lens[0] + 12, 50, 'LENS', size=7, anchor='start')
    d.text(px1 + 16, 88, 'STAGE', size=7, anchor='start')
    d.text(lens[0] + 10, 230, 'SCREW', size=7, anchor='start')
    d.text(160, 276, 'BLOOD IN A GLASS HAIR', size=7, anchor='start')
    d.text(gx, gy - gr - 16, 'A FINE GRAIN OF SAND', size=7)
    d.text(gx, gy + gr + 18, '29 GLOBULES ACROSS', size=7)
    d.text(gx, gy + gr + 30, '25,000 TO ONE BY VOLUME', size=7)
    return d


PLATES = {'harvey': harvey, 'malpighi': malpighi, 'red-cells': red_cells}
