"""Plates for The Story of Life's part small1 (sprint 055): Hooke, Redi, Leeuwenhoek. See plates_for.py."""
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


# --- ray optics, in plate units ------------------------------------------------------------------

def _refract(dx, dy, nx, ny, n1, n2):
    """Snell's law in 2D: unit direction (dx, dy) meets a surface with unit normal (nx, ny) facing
    the incoming ray; returns the refracted unit direction."""
    cos_i = -(dx * nx + dy * ny)
    eta = n1 / n2
    k = 1 - eta * eta * (1 - cos_i * cos_i)
    cos_t = math.sqrt(max(k, 0.0))
    return (eta * dx + (eta * cos_i - cos_t) * nx, eta * dy + (eta * cos_i - cos_t) * ny)


def _hit_circle(p, v, c, r, far=False):
    """Where the ray p + t v (v a unit vector) meets the circle (c, r): the near hit, or the far one."""
    ox, oy = p[0] - c[0], p[1] - c[1]
    b = ox * v[0] + oy * v[1]
    disc = b * b - (ox * ox + oy * oy - r * r)
    if disc < 0:
        return None
    t = -b + math.sqrt(disc) if far else -b - math.sqrt(disc)
    return (p[0] + t * v[0], p[1] + t * v[1])


def _through_ball(p, v, c, r, n):
    """A ray through a solid sphere of index n in air: returns (entry, exit, outgoing direction)."""
    a = _hit_circle(p, v, c, r)
    nx, ny = (a[0] - c[0]) / r, (a[1] - c[1]) / r
    v1 = _refract(v[0], v[1], nx, ny, 1.0, n)
    b = _hit_circle(a, v1, c, r, far=True)
    nx, ny = (c[0] - b[0]) / r, (c[1] - b[1]) / r                          # normal facing the ray, inside
    v2 = _refract(v1[0], v1[1], nx, ny, n, 1.0)
    return a, b, v2


def _lens_shape(d, x, y, half, bulge, vertical=True):
    """A biconvex lens outline centred at (x, y): half its height, and how far each face bulges."""
    pts_a, pts_b = [], []
    for k in range(13):
        t = -1 + 2 * k / 12
        w = bulge * (1 - t * t)
        if vertical:
            pts_a.append((x + w, y + t * half))
            pts_b.append((x - w, y - t * half))
        else:
            pts_a.append((x + t * half, y + w))
            pts_b.append((x - t * half, y - w))
    d.line(*pts_a, *pts_b, closed=True)


def hooke_cells():
    d = D()
    # Micrographia's preface and Scheme I, figures 5 and 6: an oil lamp K behind a glass globe G of
    # brine, a deep plano-convex glass I throwing the gathered light onto the specimen on pin M, and
    # the compound microscope over it (object glass, middle glass, eye glass). Rays are traced: Snell's
    # law through the globe (brine, n = 1.34), then the glass I as a thin lens. Proportions schematic;
    # Hooke's own figure sets the microscope at a slant over the stage, drawn upright here.
    axis = 196                                       # height of the light path
    lamp = (34, axis)
    globe_c, globe_r = (96, axis), 30
    lens_x = 166
    pin_x = 236

    d.group('thin')
    d.line((20, axis), (pin_x + 6, axis))                                 # the optical axis
    d.line((pin_x, 30), (pin_x, 252))                                     # the microscope's axis
    d.line((20, 252), (390, 252))                                         # the table
    for x in (globe_c[0], lens_x):
        d.line((x, axis - 44), (x, 252))

    d.group()
    # the lamp: a reservoir and its flame
    _box(d, lamp[0] - 14, axis + 14, 20, 30)
    d.line((lamp[0] - 4, axis + 14), (lamp[0] - 4, axis + 8))
    d.curve(f"M{lamp[0] - 4},{axis + 8} Q{lamp[0] - 10},{axis} {lamp[0]},{axis - 10} "
            f"Q{lamp[0] + 4},{axis} {lamp[0] - 4},{axis + 8}")
    # the globe of brine on its stand
    d.circle(*globe_c, globe_r)
    d.line((globe_c[0], axis + globe_r), (globe_c[0], 252))
    d.line((globe_c[0] - 16, 252), (globe_c[0] + 16, 252))
    # the plano-convex glass I on its arm
    pts = [(lens_x - 3, axis - 22), (lens_x - 3, axis + 22)]
    for k in range(13):
        t = 1 - 2 * k / 12
        pts.append((lens_x - 3 + 9 * (1 - t * t), axis + 22 * t))
    d.line(*pts, closed=True)
    d.line((lens_x, axis + 22), (lens_x + 10, 230), (lens_x + 10, 252))
    # the stage, its pillar and pin M
    d.line((pin_x - 30, 252), (pin_x + 60, 252))
    d.line((pin_x - 2, 252), (pin_x - 2, axis + 3), (pin_x + 2, axis + 3), (pin_x + 2, 252))
    d.circle(pin_x, axis, 2.5)
    # the microscope tube in section, with its three glasses
    obj_y, mid_y, eye_y = axis - 26, 112, 52
    for s in (-1, 1):
        d.line((pin_x + s * 6, obj_y + 4), (pin_x + s * 12, obj_y - 16), (pin_x + s * 18, 40))
    d.line((pin_x - 22, 40), (pin_x + 22, 40))
    d.line((pin_x - 22, 34), (pin_x + 22, 34))
    _lens_shape(d, pin_x, obj_y, 5, 2.5, vertical=False)
    _lens_shape(d, pin_x, eye_y, 15, 3.5, vertical=False)
    d.line((pin_x + 18, 140), (pin_x + 40, 140), (pin_x + 40, 252))       # the pillar and its arm

    d.group('mid')
    # light from the flame, through the globe, through the glass I, onto the pin: the glass's focal
    # length is the one that brings these rays together at the pin, found by trying lengths
    start = (lamp[0], axis)
    rays = []
    for h in (-0.62, -0.42, -0.22, 0.22, 0.42, 0.62):
        aim = (globe_c[0] - globe_r * math.cos(h), axis + globe_r * math.sin(h))
        v = (aim[0] - start[0], aim[1] - start[1])
        L = math.hypot(*v)
        a, b, v2 = _through_ball(start, (v[0] / L, v[1] / L), globe_c, globe_r, 1.34)
        t = (lens_x - b[0]) / v2[0]
        rays.append((a, b, (lens_x, b[1] + t * v2[1]), v2[1] / v2[0]))
    def spread(fl):
        ys = [at[1] + (sl - (at[1] - axis) / fl) * (pin_x - 3 - lens_x) for _, _, at, sl in rays]
        return max(ys) - min(ys)
    lens_f = min((fl / 4 for fl in range(40, 400)), key=spread)
    for a, b, at, sl in rays:
        slope = sl - (at[1] - axis) / lens_f
        d.line(start, a, b, at, (pin_x - 3, at[1] + slope * (pin_x - 3 - lens_x)))
    # rays from the specimen up the tube: object glass to an image, then the eye glass
    img_y = 86
    for dx in (-4, 4):
        top = (pin_x + dx, obj_y)
        d.line((pin_x, axis - 3), top, (pin_x - dx * 1.6, img_y + 4))
        d.line((pin_x - dx * 1.6, img_y + 4), (pin_x - dx * 3.2, eye_y))
        d.line((pin_x - dx * 3.2, eye_y), (pin_x - dx * 3.2, 24))
    d.dashed((pin_x - 14, mid_y), (pin_x + 14, mid_y), dash=3, gap=2)  # the middle glass, taken out

    d.group('mid')
    d.text(lamp[0] - 2, axis - 22, 'LAMP K', size=7)
    d.text(globe_c[0], axis - 38, 'GLOBE G · BRINE', size=7)
    d.text(lens_x + 4, axis - 30, 'GLASS I', size=7)
    d.text(pin_x - 8, axis + 34, 'PIN M', size=7, anchor='end')
    d.text(pin_x + 46, obj_y + 3, 'OBJECT GLASS', size=7, anchor='start')
    d.text(pin_x + 46, mid_y + 3, 'MIDDLE GLASS', size=7, anchor='start')
    d.text(pin_x + 46, eye_y + 3, 'EYE GLASS', size=7, anchor='start')
    d.text(pin_x + 46, mid_y + 13, '(TAKEN OUT)', size=7, anchor='start')
    d.text(130, 30, "HOOKE'S LAMP AND MICROSCOPE", size=7)
    d.text(130, 41, 'MICROGRAPHIA · SCHEME I', size=7)
    d.text(200, 272, 'A CONSTANT LIGHT, AT ANY HOUR', size=7)
    return d


# --- Redi ----------------------------------------------------------------------------------------

def _flask(cx, base, w, h, neck_w, neck_h):
    """A wide-mouthed flask: a rounded body and a short neck, as a closed outline."""
    pts = []
    body_top = base - h
    for k in range(17):                                                   # right side, bottom to shoulder
        t = k / 16
        y = base - t * h
        x = cx + w / 2 * (1 - 0.18 * (t ** 6)) * (0.92 + 0.08 * math.sin(math.pi * t))
        pts.append((x, y))
    pts += [(cx + neck_w / 2, body_top - 4), (cx + neck_w / 2, body_top - neck_h),
            (cx + neck_w / 2 + 3, body_top - neck_h - 3)]
    left = [(2 * cx - x, y) for x, y in reversed(pts)]
    return pts + left


def _fly(d, x, y, s=1.0, ang=0):
    """A fly seen from above: a head, a long body and two narrow wings swept back."""
    def ell(cx, cy, rx, ry, rot):
        cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        return [(cx + s * (rx * math.cos(t) * cr - ry * math.sin(t) * sr),
                 cy + s * (rx * math.cos(t) * sr + ry * math.sin(t) * cr))
                for t in [2 * math.pi * k / 16 for k in range(17)]]
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    d.line(*ell(x, y, 3.6, 1.5, ang))
    d.circle(x + s * 4.4 * ca, y + s * 4.4 * sa, 1.1 * s)
    for side in (-1, 1):
        w = ang + 180 + side * 32
        cx = x + s * (0.8 * ca + 3.0 * math.cos(math.radians(w)))
        cy = y + s * (0.8 * sa + 3.0 * math.sin(math.radians(w)))
        d.line(*ell(cx, cy, 3.4, 1.2, w))


def _maggot(d, x, y, s=1.0, ang=0):
    """A maggot: a tapered segmented body."""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    def P(u, v):
        return (x + s * (u * ca - v * sa), y + s * (u * sa + v * ca))
    top = [P(u, -1.4 * math.sin(math.pi * (u + 4) / 8) - 0.2) for u in range(-4, 5)]
    bot = [P(u, 1.4 * math.sin(math.pi * (u + 4) / 8) + 0.2) for u in range(4, -5, -1)]
    d.line(*top, *bot, closed=True)


def redi_flies():
    d = D()
    # Redi's flasks (Esperienze, 1668; Bigelow's translation of the 1688 edition, pp. 33-37): meat in
    # an open flask, flies coming and going and maggots on the meat; the same in a sealed flask, a
    # maggot now and then on the paper cover outside, none within; and meat under a fine Naples veil,
    # flies on the veil and worms dropped on it, none on the meat. Redi set the veiled vessel inside a
    # net-covered frame as well; that frame is left out. Flies and maggots are drawn far larger than life.
    base = 236
    xs = (78, 200, 322)
    bw, bh, nw, nh = 86, 104, 54, 22

    d.group('thin')
    d.line((20, base), (380, base))
    for x in xs:
        d.line((x, base + 4), (x, 40))
    d.line((24, base - bh - nh - 3), (376, base - bh - nh - 3))           # the mouths' level

    d.group()
    for x in xs:
        d.line(*_flask(x, base, bw, bh, nw, nh), closed=False)
        d.line((x - bw / 2 * 0.92, base), (x + bw / 2 * 0.92, base))
        # the meat: a slab with a cut face
        m = [(x - 28, base - 4), (x - 30, base - 20), (x - 14, base - 30), (x + 18, base - 27),
             (x + 30, base - 14), (x + 27, base - 4)]
        d.line(*m, closed=True)
    mouth = base - bh - nh - 3
    # the sealed flask's cover, tied round the neck
    x = xs[1]
    d.curve(f"M{x - nw / 2 - 6},{mouth + 8} Q{x},{mouth - 8} {x + nw / 2 + 6},{mouth + 8}")
    d.line((x - nw / 2 - 1, mouth + 12), (x + nw / 2 + 1, mouth + 12))
    # the veil over the third flask
    x = xs[2]
    d.line((x - nw / 2 - 5, mouth + 1), (x + nw / 2 + 5, mouth + 1))
    d.line((x - nw / 2 - 1, mouth + 12), (x + nw / 2 + 1, mouth + 12))

    d.group('mid')
    x = xs[2]
    for k in range(-6, 7):                                                # the veil's mesh
        u = x + k * 4.6
        d.line((u, mouth - 1), (u, mouth + 3))
    for x in xs:                                                          # grain of the meat
        for k in range(3):
            d.line((x - 18 + k * 10, base - 24 + k * 2), (x - 8 + k * 10, base - 8))
    # open flask: flies coming and going, maggots on the meat
    x = xs[0]
    for (u, v, a) in ((x - 14, mouth - 18, -30), (x + 20, mouth - 34, 40), (x - 4, mouth + 30, 80),
                      (x + 10, mouth - 52, 10)):
        _fly(d, u, v, 1.5, a)
    for (u, v, a) in ((x - 16, base - 30, 10), (x - 2, base - 33, -8), (x + 12, base - 31, 15),
                      (x + 22, base - 22, 50), (x - 24, base - 20, -40)):
        _maggot(d, u, v, 1.3, a)
    # sealed flask: flies outside on the cover, nothing within
    x = xs[1]
    for (u, v, a) in ((x - 12, mouth - 12, 20), (x + 16, mouth - 26, -40)):
        _fly(d, u, v, 1.5, a)
    _maggot(d, x + 4, mouth - 2, 1.2, 0)
    # veiled flask: flies on the veil, worms dropped on it, none on the meat
    x = xs[2]
    for (u, v, a) in ((x + 26, mouth - 10, -20), (x + 14, mouth - 34, 30), (x + 2, mouth - 56, 0)):
        _fly(d, u, v, 1.5, a)
    for (u, a) in ((x - 4, 0), (x + 6, 20), (x + 15, -10)):
        _maggot(d, u, mouth - 3, 1.1, a)

    x = xs[2]
    d.curve(f"M{x - 12},{mouth - 40} Q{x - 6},{mouth - 24} {x - 12},{mouth - 10} Q{x - 18},{mouth + 4} {x - 12},{mouth + 24}")
    _arrow(d, (x - 13, mouth + 16), (x - 12, mouth + 24), size=4)

    d.group('mid')
    d.text(xs[2] - 18, mouth - 46, 'AIR', size=7, anchor='end')
    names = (('OPEN', 'MAGGOTS IN THE MEAT'), ('SEALED', 'NONE WITHIN'), ('VEILED', 'NONE IN THE MEAT'))
    for x, (a, b) in zip(xs, names):
        d.text(x, base + 18, a, size=7)
        d.text(x, base + 29, b, size=7)
    d.text(200, 30, "REDI'S FLASKS · FLORENCE, 1668", size=7)
    return d


# --- Leeuwenhoek ---------------------------------------------------------------------------------

def leeuwenhoek_animalcules():
    d = D()
    # Left: a Leeuwenhoek microscope cut through its lens, side on (after Baker's description and the
    # 2021 neutron study): two brass plates riveted together with the lens between them in a small
    # hole; the specimen on a pin before the lens; a long screw to raise the pin's stage and a short
    # one through the stage's arm to bring it nearer the lens. Schematic, about three times life.
    # Right: the Utrecht instrument's ball lens, 1.3 mm across (Cocquyt et al. 2021), at 60 units a
    # millimetre, held between the plates' holes (taken as 0.6 mm across; the paper gives 0.5 to 1.0),
    # with rays traced by Snell's law (glass, n = 1.5) from a point at the ball's back focal distance,
    # nD/4(n-1) - D/2 = 0.325 mm in front of it. They leave nearly parallel, for a relaxed eye.
    pl_x, top, bot = 104, 52, 244
    lens_y = 112
    pin_x = 74

    mm = 60.0
    D_mm, n = 1.3, 1.5
    r = D_mm / 2 * mm
    bfl = (n * D_mm / (4 * (n - 1)) - D_mm / 2) * mm
    c = (306, 150)
    obj = (c[0] - r - bfl, c[1])
    ap = 0.3 * mm
    face = math.sqrt(r * r - ap * ap)

    d.group('thin')
    d.line((pin_x - 22, lens_y), (pl_x + 30, lens_y))                     # the axis through the lens
    d.line((24, bot + 10), (176, bot + 10))
    d.line((obj[0] - 34, c[1]), (392, c[1]))                              # the inset's axis
    d.circle(pl_x, lens_y, 9)                                             # what the inset enlarges
    d.line((pl_x + 9, lens_y), (obj[0] - 40, c[1] - 52))

    d.group()
    # the two plates, side on, with the lens between them
    for dx in (-3, 3):
        d.line((pl_x + dx, top), (pl_x + dx, lens_y - 4))
        d.line((pl_x + dx, lens_y + 4), (pl_x + dx, bot))
    d.line((pl_x - 3, top), (pl_x + 3, top))
    d.line((pl_x - 3, bot), (pl_x + 3, bot))
    d.circle(pl_x, lens_y, 2.2)
    # the stage: a block on the long screw, its arm carrying the pin
    _box(d, 46, 150, 22, 30)
    d.line((57, 180), (57, bot - 6), (pl_x - 3, bot - 6))                 # the long screw to the plate
    d.line((52, 150), (52, 126), (pin_x - 2, 126), (pin_x - 2, lens_y + 2))
    d.line((pin_x - 2, lens_y + 2), (pin_x + 2, lens_y - 1))              # the pin's point
    d.line((68, 165), (pl_x - 3, 165))                                    # the short focusing screw
    d.line((pl_x + 3, 165), (pl_x + 14, 165))
    _box(d, pl_x + 14, 160, 6, 10)
    # inset: the ball between the plates' holes
    d.circle(*c, r)
    for s in (-1, 1):
        for x0, x1 in ((c[0] - face - 7, c[0] - face), (c[0] + face, c[0] + face + 7)):
            d.line((x0, c[1] + s * ap), (x1, c[1] + s * ap))
            d.line((x0, c[1] + s * ap), (x0, c[1] + s * (r + 14)))
            d.line((x1, c[1] + s * ap), (x1, c[1] + s * (r + 14)))

    d.group('mid')
    for h in (-0.16, -0.1, -0.04, 0.04, 0.1, 0.16):
        aim = (c[0] - math.sqrt(r * r - (h * mm) ** 2), c[1] + h * mm)
        v = (aim[0] - obj[0], aim[1] - obj[1])
        L = math.hypot(*v)
        a, b, v2 = _through_ball(obj, (v[0] / L, v[1] / L), c, r, n)
        end = (392, b[1] + v2[1] / v2[0] * (392 - b[0]))
        d.line(obj, a, b, end)
    d.circle(*obj, 2)
    d.line((obj[0] - 30, obj[1] + 6), (obj[0] - 2, obj[1] + 1))           # the pin's point, enlarged
    d.line((356, c[1] - 52), (392, c[1] - 52))
    _arrow(d, (356, c[1] - 52), (392, c[1] - 52), size=4)

    d.group('mid')
    d.text(pl_x, top - 10, 'BRASS PLATES', size=7)
    d.text(pin_x - 8, lens_y - 8, 'PIN', size=7, anchor='end')
    d.text(57, 194, 'STAGE', size=7)
    d.text(pl_x + 24, 182, 'FOCUS SCREW', size=7, anchor='start')
    d.text(pl_x + 10, bot - 3, 'LONG SCREW', size=7, anchor='start')
    d.text(c[0] - 20, c[1] - r - 24, 'GLASS BEAD 1.3 MM', size=7)
    d.text(obj[0] + 6, c[1] + 42, 'OBJECT 0.33 MM', size=7, anchor='end')
    d.text(obj[0] + 6, c[1] + 52, 'FROM THE GLASS', size=7, anchor='end')
    d.text(394, c[1] - 60, 'TO THE EYE', size=7, anchor='end')
    d.text(c[0], c[1] + r + 32, 'UTRECHT LENS, ABOUT 266 TIMES', size=7)
    d.text(200, 286, 'A SINGLE LENS · DELFT, 1670s', size=7)
    return d


PLATES = {'hooke-cells': hooke_cells, 'redi-flies': redi_flies, 'leeuwenhoek-animalcules': leeuwenhoek_animalcules}
