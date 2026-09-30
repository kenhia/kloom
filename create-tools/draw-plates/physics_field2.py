"""physics plates, trail "The field, Ørsted to Hertz", part field2 (sprint 021). See physics.py."""
import math

from plates import D


def _arrow(d, x, y, ang, size=4):
    """An open arrowhead at (x, y) pointing along angle `ang` (radians)."""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.line((x + size * math.cos(a1), y + size * math.sin(a1)), (x, y),
           (x + size * math.cos(a2), y + size * math.sin(a2)))


def _field_line(poles, x, y, step, n, stop):
    """Trace a line of force from (x, y) through the field of point poles [(px, py, q)], following +E."""
    pts = [(x, y)]
    for _ in range(n):
        ex = ey = 0.0
        for px, py, q in poles:
            dx, dy = x - px, y - py
            r3 = (dx * dx + dy * dy) ** 1.5 or 1e-9
            ex += q * dx / r3
            ey += q * dy / r3
        m = math.hypot(ex, ey) or 1e-9
        x, y = x + step * ex / m, y + step * ey / m
        pts.append((x, y))
        if stop(x, y):
            break
    return pts


def faraday_lines():
    """Faraday's experiment of 13 September 1845 (Experimental Researches §2150-2153), in plan.

    A ray, polarised in one plane, passes along the axis between the opposite
    poles of an electromagnet, through a block of heavy glass. The lines of
    force from pole to pole are traced from two point poles, as iron filings
    would lie; the plane of polarisation is drawn as a diameter of a small
    circle before and after the glass, turned by the field. Above, a bar of the
    same glass hung between the poles sets itself across the lines (§2253)."""
    d = D()
    cy = 168
    xn, xs = 118, 282                     # the pole faces
    poles = [(xn, cy, 1.0), (xs, cy, -1.0)]
    # construction: lines of force traced from the north face to the south, above and below the axis
    d.group('thin')
    segs = []
    for k in range(1, 9):
        a = math.radians(9 + k * 19)
        for sgn in (1, -1):
            x0, y0 = xn + 3 * math.cos(a), cy - sgn * 3 * math.sin(a)
            pts = _field_line(poles, x0, y0, 2.0, 400,
                              lambda x, y: math.hypot(x - xs, y - cy) < 4 or y < 26 or y > 292 or x < 16 or x > 384)
            segs.append(pts)
    d.lines(segs)
    d.line((20, cy), (380, cy))           # the ray's axis
    # the object: the two pole pieces (cores wound with coils) and the block of heavy glass
    d.group()
    for x0, x1 in ((42, xn), (xs, 358)):
        d.line((x0, cy - 22), (x1, cy - 22), (x1, cy + 22), (x0, cy + 22), closed=True)
    d.lines([[(x, cy - 26), (x, cy + 26)] for x in list(range(52, 108, 8)) + list(range(292, 350, 8))])
    gx0, gx1, gh = 178, 222, 16            # the glass, 2 in. long and 0.5 in. thick, drawn larger
    d.line((gx0, cy - gh), (gx1, cy - gh), (gx1, cy + gh), (gx0, cy + gh), closed=True)
    # details: the ray, the plane of polarisation before and after, and the hanging bar set across the lines
    d.group('mid')
    d.line((24, cy - 44), (70, cy - 44))
    _arrow(d, 70, cy - 44, 0, 4)
    for x, ang in ((150, 90), (250, 90 - 32)):
        d.circle(x, cy, 12)
        a = math.radians(ang)
        d.line((x - 12 * math.cos(a), cy - 12 * math.sin(a)), (x + 12 * math.cos(a), cy + 12 * math.sin(a)))
    a = math.radians(90)
    d.line((250 - 12 * math.cos(a), cy - 12 * math.sin(a)), (250 + 12 * math.cos(a), cy + 12 * math.sin(a)), cls=None)
    bx, by = 200, 78                       # the diamagnetic bar, hung by a thread, lying across the lines
    d.line((bx, 34), (bx, by - 20))
    d.line((bx - 3, by - 20), (bx + 3, by - 20), (bx + 3, by + 20), (bx - 3, by + 20), closed=True)
    # labels
    d.group()
    d.text(80, cy + 4, 'N', size=10)
    d.text(320, cy + 4, 'S', size=10)
    d.text(200, cy + gh + 14, 'HEAVY GLASS', size=7)
    d.text(24, cy - 50, 'POLARISED RAY', size=7, anchor='start')
    d.text(250, cy - 18, 'θ', size=9)
    d.text(bx + 10, by + 3, 'BAR SETS ACROSS', size=7, anchor='start')
    d.text(200, 292, 'MAGNETISM TURNS THE PLANE OF LIGHT · 1845', size=7)
    return d


def displacement_current():
    """Maxwell's model of 1861-62 (On Physical Lines of Force, Part II fig. 2, Part III), in section.

    Hexagonal cells of the medium spin about axes along the magnetic lines;
    between them lie layers of small particles, the 'idle wheels', each turning
    the other way so that neighbouring cells can turn together. Where a row of
    particles is pushed along (the arrow), the elastic cells strain: the
    displacement that Maxwell counted as a current."""
    d = D()
    R = 30                                  # the hexagon's circumradius
    w = math.sqrt(3) * R                    # flat-topped rows: pointy-topped hexagons, width w
    cells = []
    for row in range(4):
        for col in range(-1, 5):
            cx = 58 + col * w + (w / 2 if row % 2 else 0)
            cy = 62 + row * 1.5 * R
            if 22 < cx < 378:
                cells.append((cx, cy, row))

    def hexagon(cx, cy, r, skew=0.0):
        pts = []
        for k in range(6):
            a = math.radians(60 * k - 90)
            x, y = cx + r * math.cos(a), cy + r * math.sin(a)
            pts.append((x + skew * (y - cy), y))
        return pts
    # construction: each cell's axis (seen end-on as a centre) and the rows' centre lines
    d.group('thin')
    d.lines([[(20, 62 + row * 1.5 * R), (380, 62 + row * 1.5 * R)] for row in range(4)])
    for cx, cy, row in cells:
        d.circle(cx, cy, 1.2)
    # the object: the cells, those in the row next to the displaced layer drawn strained (sheared)
    d.group()
    for cx, cy, row in cells:
        d.line(*hexagon(cx, cy, R - 4, skew=0.22 if row == 2 else 0.0), closed=True)
    # details: the idle-wheel particles along the cell walls, and each cell's sense of rotation
    d.group('mid')
    for cx, cy, row in cells:
        pts = hexagon(cx, cy, R, skew=0.22 if row == 2 else 0.0)
        for k in (0, 1, 2):                 # three walls per cell, so shared walls are drawn once
            (x0, y0), (x1, y1) = pts[k], pts[k + 1]
            for t in (0.25, 0.75):
                d.circle(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 2.6)
    for cx, cy, row in cells:
        r = 11
        d.arc(cx, cy, r, 200, 320, n=12)
        a = math.radians(320)
        _arrow(d, cx + r * math.cos(a), cy + r * math.sin(a), a + math.pi / 2, 3)
    # the displacement: the layer of particles between rows 1 and 2 pushed along
    d.group()
    yl = 62 + 1.75 * R + 4
    d.line((34, yl + 6), (362, yl + 6))
    _arrow(d, 362, yl + 6, 0, 6)
    # labels
    d.group()
    d.text(200, 22, 'VORTEX CELLS · IDLE WHEELS', size=8)
    d.text(30, 272, 'THE ARROW: PARTICLES DISPLACED, CELLS STRAINED', size=7, anchor='start')
    d.text(200, 292, 'v = 310,740 km/s ≈ LIGHT', size=8)
    return d


def hertz():
    """Hertz's experiment on waves in air and their reflection (Karlsruhe, March 1888), to scale in plan.

    The primary oscillator, two rods with a spark gap between, stands 13 metres
    from a zinc sheet on the lecture-room wall. Wave and reflection make a
    standing wave; the envelope of the electric force is drawn with Hertz's
    half wave-length of 4.8 m and the first node 0.68 m behind the wall. The
    ring, a circle of 35 cm radius with a spark gap, is the detector."""
    d = D()
    x_osc, x_wall, y0 = 34, 364, 176        # 13 m from oscillator to wall
    s = (x_wall - x_osc) / 13.0              # plate units per metre
    half, behind = 4.8, 0.68
    amp = 58
    # construction: a scale of metres along the normal, and the nodes of the standing wave
    d.group('thin')
    d.line((x_osc, 262), (x_wall, 262))
    d.lines([[(x_wall - m * s, 258), (x_wall - m * s, 266)] for m in range(0, 14)])
    nodes = [-behind + k * half for k in range(1, 4)]       # metres in front of the wall
    nodes = [n for n in nodes if 0 < n < 13]
    d.lines([[(x_wall - n * s, y0 - amp - 12), (x_wall - n * s, 266)] for n in nodes])
    d.line((x_osc, y0), (x_wall, y0))
    # the object: the oscillator (rods, plates, spark gap) and the zinc sheet on the wall
    d.group()
    d.line((x_osc, y0 - 70), (x_osc, y0 - 6))
    d.line((x_osc, y0 + 6), (x_osc, y0 + 70))
    d.line((x_osc - 9, y0 - 88), (x_osc + 9, y0 - 88), (x_osc + 9, y0 - 70), (x_osc - 9, y0 - 70), closed=True)
    d.line((x_osc - 9, y0 + 70), (x_osc + 9, y0 + 70), (x_osc + 9, y0 + 88), (x_osc - 9, y0 + 88), closed=True)
    d.circle(x_osc, y0 - 4, 2.2)
    d.circle(x_osc, y0 + 4, 2.2)
    d.line((x_wall, 40), (x_wall, 250))
    d.lines([[(x_wall, y), (x_wall + 8, y - 8)] for y in range(48, 252, 12)])
    # details: the envelope of the standing wave, from the oscillator to the wall
    d.group('mid')
    for sgn in (1, -1):
        pts = []
        for i in range(0, 261):
            m = 13.0 * i / 260               # metres in front of the wall
            a = abs(math.sin(math.pi * (m + behind) / half))
            pts.append((x_wall - m * s, y0 - sgn * amp * a))
        d.line(*pts)
    # the ring detector at an antinode, its spark gap at the top
    xr = x_wall - (nodes[0] + half / 2) * s
    rr = 14
    d.arc(xr, y0 - amp - 30, rr, -80, 260, n=40)
    d.circle(xr - 2.4, y0 - amp - 30 - rr, 1.4)
    d.circle(xr + 2.4, y0 - amp - 30 - rr, 1.4)
    # labels
    d.group()
    d.text(x_osc + 12, y0 - 92, 'OSCILLATOR', size=7, anchor='start')
    d.text(x_wall - 6, 34, 'ZINC SHEET', size=7, anchor='end')
    d.text(xr + rr + 6, y0 - amp - 27, 'RING', size=7, anchor='start')
    d.text((x_wall - nodes[0] * s + x_wall - nodes[1] * s) / 2, 252, 'λ/2 = 4.8 m', size=7)
    d.text(x_wall - 13 * s, 280, '13 m', size=7, anchor='start')
    d.text(x_wall, 280, '0', size=7)
    d.text(200, 296, 'KARLSRUHE · MARCH 1888', size=7)
    return d


PLATES = {'faraday-lines': faraday_lines, 'displacement-current': displacement_current, 'hertz': hertz}
