"""physics plates, segment "Cracks in the classical" (sprint 021). See plates_for.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _mirror(d, x, y, ang, half=5):
    """A short mirror through (x, y) at angle `ang` (degrees)."""
    a = math.radians(ang)
    d.line((x - half * math.cos(a), y - half * math.sin(a)), (x + half * math.cos(a), y + half * math.sin(a)))


def _fold(d, a, b, c, half=4):
    """The mirror at b that turns light arriving from a towards c: its normal bisects the turn."""
    ux, uy = b[0] - a[0], b[1] - a[1]
    vx, vy = c[0] - b[0], c[1] - b[1]
    lu, lv = math.hypot(ux, uy), math.hypot(vx, vy)
    nx, ny = vx / lv - ux / lu, vy / lv - uy / lu
    _mirror(d, b[0], b[1], math.degrees(math.atan2(ny, nx)) + 90, half)


def michelson_morley():
    """The 1887 interferometer in plan, and the fringe shift expected against what was found.

    Left: the sandstone slab (1.5 m square) on its float in a ring of mercury,
    the half-silvered plate at the centre, and the two arms folded by mirrors
    (schematic: the real paths bounced between four mirrors at each corner for
    about 11 m). Right: one turn of the stone. The ether wind should have moved
    the fringes as 0.2·cos 2θ, 0.4 of a fringe from peak to trough; the paper
    says the shift "cannot be much greater than 0.01", drawn as a band."""
    d = D()
    cx, cy = 118, 150
    s = 80                       # half the stone's side
    # construction: the stone's centre lines and diagonals, and the arms' axes
    d.group('thin')
    d.lines([[(cx - s - 8, cy), (cx + s + 8, cy)], [(cx, cy - s - 8), (cx, cy + s + 8)],
             [(cx - s, cy - s), (cx + s, cy + s)], [(cx - s, cy + s), (cx + s, cy - s)]])
    # the graph's axes and quarter-turn ticks
    gx0, gx1, gy = 248, 388, 150
    amp = 50                     # plate units per 0.2 fringe
    d.line((gx0, gy), (gx1, gy))
    d.line((gx0, gy - amp - 12), (gx0, gy + amp + 12))
    d.lines([[(gx0 + (gx1 - gx0) * k / 4, gy - 3), (gx0 + (gx1 - gx0) * k / 4, gy + 3)] for k in range(1, 5)])
    # the trough of mercury and the stone square on its float
    d.group('mid')
    d.circle(cx, cy, s + 6)
    d.circle(cx, cy, s * 0.47)
    d.group()
    d.line((cx - s, cy - s), (cx + s, cy - s), (cx + s, cy + s), (cx - s, cy + s), closed=True)
    # the light: in from the source, split at the centre, out and back along each folded arm
    d.group('mid')
    d.line((12, cy), (cx, cy))
    _arrow(d, cx - 58, cy, 0)
    east = [(cx, cy), (cx + 70, cy), (cx + 70, cy + 9), (cx + 22, cy + 9), (cx + 22, cy + 18), (cx + 70, cy + 18)]
    north = [(cx, cy), (cx, cy - 70), (cx - 9, cy - 70), (cx - 9, cy - 22), (cx - 18, cy - 22), (cx - 18, cy - 70)]
    d.line(*east)
    d.line(*north)
    d.line((cx, cy), (cx, 292))
    _arrow(d, cx, 272, math.pi / 2)
    d.group()
    _mirror(d, cx, cy, -45, 7)                       # the half-silvered plate
    for path in (east, north):
        for a, b, c in zip(path, path[1:], path[2:]):
            _fold(d, a, b, c)
    _mirror(d, east[5][0] + 1.5, east[5][1], 90)      # the end mirror sends the light back
    _mirror(d, north[5][0], north[5][1] - 1.5, 0)
    d.line((4, cy - 6), (12, cy - 6), (12, cy + 6), (4, cy + 6), closed=True)      # the lamp
    d.line((cx - 6, 292), (cx + 6, 292))                                          # the telescope
    # the graph: expected shift over one turn, and the band the paper allows
    d.group('mid')
    pts = [(gx0 + (gx1 - gx0) * i / 120, gy - amp * math.cos(2 * math.radians(3 * i))) for i in range(121)]
    d.line(*pts)
    d.group()
    band = amp * 0.01 / 0.2
    d.lines([[(gx0, gy - band), (gx1, gy - band)], [(gx0, gy + band), (gx1, gy + band)]])
    # labels
    d.group()
    d.text(cx, 18, 'STONE ON MERCURY · 1.5 M', size=7)
    d.text(cx + 30, 290, 'TELESCOPE', size=7, anchor='start')
    d.text(8, cy - 12, 'LAMP', size=7, anchor='start')
    d.text((gx0 + gx1) / 2, gy - amp - 20, 'EXPECTED · 0.4 FRINGE', size=7)
    d.text((gx0 + gx1) / 2, gy + amp + 26, 'FOUND · UNDER 0.01', size=7)
    d.text((gx0 + gx1) / 2, 286, 'ONE TURN OF THE STONE', size=7)
    return d


def x_rays():
    """Röntgen's experiment in elevation, after the first paragraph of his paper.

    A pear-shaped discharge tube in a close-fitting black paper shield; the
    cathode rays (construction lines) strike the glass at the wide end, and
    from there the new rays fan out, through a book, to a screen painted with
    barium platinocyanide, which glows except where a piece of lead casts its
    shadow. The shadow is projected from the glass's glow, not placed."""
    d = D()
    cy = 130
    kx = 40                      # the cathode disc
    def radius(x):
        """The tube's profile: a neck, then a cone to the bulb."""
        if x <= 78:
            return 7
        return 7 + (x - 78) * 0.45
    xs = list(range(34, 151, 2))
    end_x, end_r = 150, radius(150)
    sx = end_x + end_r * 0.35     # where the cathode rays strike the glass: the new rays' source
    # construction: the cathode rays, and the edges of the fan the source throws on the screen
    d.group('thin')
    d.lines([[(kx + 2, cy + dy * 0.3), (sx - 2, cy + dy)] for dy in (-24, -12, 0, 12, 24)])
    scr = 372
    d.lines([[(sx, cy), (scr, 38)], [(sx, cy), (scr, 262)]])
    lead = (292, 160, 304, 180)   # x0, y0, x1, y1 of the lead
    shadow = [cy + (y - cy) * (scr - sx) / (x - sx) for x, y in ((lead[2], lead[1]), (lead[0], lead[3]))]
    d.lines([[(sx, cy), (scr, shadow[0])], [(sx, cy), (scr, shadow[1])]])
    # the tube: neck, cone, the domed end, the cathode and the anode on its side arm
    d.group()
    d.line(*[(x, cy - radius(x)) for x in xs])
    d.line(*[(x, cy + radius(x)) for x in xs])
    d.arc(end_x, cy, end_r * 0.35, -90, 90, ry=end_r)
    d.arc(34, cy, 3, 90, 270, n=12, ry=7)
    d.line((kx, cy - 5), (kx, cy + 5))
    d.line((kx, cy), (20, cy))
    ax = 104
    d.line((ax - 3, cy - radius(ax) + 1), (ax - 3, cy - radius(ax) - 16), (ax + 3, cy - radius(ax) - 16), (ax + 3, cy - radius(ax) + 1))
    d.line((ax, cy - radius(ax) - 16), (ax, cy - radius(ax) - 26))
    # the black paper shield, the book, the lead and the screen
    d.group('mid')
    top, bot = cy - end_r - 5, cy + end_r + 5
    d.line((26, top), (end_x + end_r * 0.35 + 5, top), (end_x + end_r * 0.35 + 5, bot), (26, bot), closed=True)
    bx0, by0, bx1, by1 = 238, 70, 266, 122
    d.line((bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1), closed=True)
    d.lines([[(bx0 + 3 + 3 * k, by0 + 2), (bx0 + 3 + 3 * k, by1 - 2)] for k in range(8)])
    d.group()
    d.line((lead[0], lead[1]), (lead[2], lead[1]), (lead[2], lead[3]), (lead[0], lead[3]), closed=True)
    d.line((scr, 36), (scr, 264))
    d.group('mid')
    ticks = [y for y in range(40, 262, 6) if not (shadow[0] - 1 <= y <= shadow[1] + 1)]
    d.lines([[(scr + 3, y), (scr + 9, y - 3)] for y in ticks])
    # labels
    d.group()
    d.text(22, cy + 18, 'CATHODE', size=7, anchor='start')
    d.text(ax + 8, cy - radius(ax) - 20, 'ANODE', size=7, anchor='start')
    d.text(88, bot + 14, 'BLACK PAPER', size=7)
    d.text((bx0 + bx1) / 2, by0 - 8, 'BOOK', size=7)
    d.text((lead[0] + lead[2]) / 2, lead[3] + 14, 'LEAD', size=7)
    d.text(scr - 4, 282, 'SCREEN · BARIUM PLATINOCYANIDE', size=7, anchor='end')
    d.text(200, 20, 'STILL GLOWING AT TWO METRES', size=7)
    return d


def electron():
    """Thomson's tube of 1897 for m/e, in elevation.

    Cathode rays from the cathode pass slits in the anode and a plug, then
    between two plates; an electric field between them bends the beam on a
    parabola, and it runs on straight to a scale on the far end. Coils outside
    the tube give a magnetic field across the same stretch, set to bring the
    beam back to the middle; the two settings give the speed and m/e. The
    undeflected beam is a construction line."""
    d = D()
    cy = 140
    px0, px1 = 176, 244           # the plates
    screen = 352
    k = 0.0013                   # the parabola's curvature, plate units
    def beam_y(x):
        if x <= px0:
            return cy
        if x <= px1:
            return cy - k * (x - px0) ** 2
        slope = 2 * k * (px1 - px0)
        return cy - k * (px1 - px0) ** 2 - slope * (x - px1)
    # construction: the tube's axis, the undeflected beam, and the tangent back to the plates' middle
    d.group('thin')
    d.line((20, cy), (screen + 8, cy))
    mid = (px0 + px1) / 2
    d.line((mid, cy), (screen, beam_y(screen)))
    # the tube: the cathode bulb, the long neck, and the wide end with its scale
    d.group()
    d.arc(52, cy, 26, 20, 340, n=60)
    ends = (52 + 26 * math.cos(math.radians(20)), 26 * math.sin(math.radians(20)))
    d.line((ends[0], cy - ends[1]), (292, cy - ends[1]))
    d.line((ends[0], cy + ends[1]), (292, cy + ends[1]))
    d.line((292, cy - ends[1]), (screen, cy - 58))
    d.line((292, cy + ends[1]), (screen, cy + 58))
    d.line((screen, cy - 58), (screen, cy + 58))
    d.line((40, cy - 6), (40, cy + 6))
    d.line((40, cy), (22, cy))
    # the anode, the plug, the plates and the magnet coils
    d.group('mid')
    for x in (96, 118):
        d.lines([[(x, cy - ends[1]), (x, cy - 1.5)], [(x, cy + 1.5), (x, cy + ends[1])]])
    d.lines([[(px0, cy - 8), (px1, cy - 8)], [(px0, cy + 8), (px1, cy + 8)]])
    d.lines([[(px0 + 8, cy - 8), (px0 + 8, cy - 30)], [(px1 - 8, cy + 8), (px1 - 8, cy + 30)]])
    for yc in (cy - 52, cy + 52):
        d.ellipse(mid, yc, 34, 10)
        d.ellipse(mid, yc, 22, 5)
    d.lines([[(screen - 1, cy - 50 + 6 * i), (screen - (6 if i % 5 == 0 else 3), cy - 50 + 6 * i)] for i in range(17)])
    # the beam: straight through the slits, bent between the plates, straight to the scale
    d.group()
    d.line(*[(x, beam_y(x)) for x in range(42, screen + 1, 2)])
    # labels
    d.group()
    d.text(52, cy + 42, 'CATHODE', size=7)
    d.text(107, cy + 34, 'SLITS', size=7)
    d.text(px0 + 4, cy - 34, 'PLATES', size=7, anchor='end')
    d.text(mid, cy + 78, 'MAGNET COILS', size=7)
    d.text(screen + 6, cy - 62, 'SCALE', size=7, anchor='end')
    d.text(200, 22, 'm/e ≈ A THOUSANDTH OF THE HYDROGEN ION’S', size=7)
    d.text(200, 286, 'CAVENDISH LABORATORY · 1897', size=7)
    return d


PLATES = {'michelson-morley': michelson_morley, 'x-rays': x_rays, 'electron': electron}
