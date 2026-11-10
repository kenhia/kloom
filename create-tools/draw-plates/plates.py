"""Primitives for drawing kloom scene plates as draw-on SVG.

Every drawable element is a <path pathLength="1"> so the engine's draw-on
animation works; each top-level <g> is drawn after the one before it. Groups
come in three weights: 'thin' (construction lines), 'mid' (secondary detail)
and 'main' (the object). See README.md and docs/design.md §Illustrations.
Standard library only.
"""
import math, os
from xml.sax.saxutils import escape

def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s

class D:
    def __init__(self, w=400, h=300, sw=1.25):
        self.w, self.h, self.sw = w, h, sw
        self.groups = []
        self.cur = None

    def group(self, kind='main'):
        self.cur = []
        self.groups.append((kind, self.cur))
        return self

    def path(self, d, cls=None):
        self.cur.append(('path', d, cls))

    def text(self, x, y, s, size=9, anchor='middle'):
        """A label, written as plain text: `&`, `<` and `>` are escaped here (sprint 015)."""
        self.cur.append(('text', (x, y, escape(s), size, anchor), None))

    # primitives -------------------------------------------------------
    def line(self, *pts, closed=False, cls=None):
        d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + (' Z' if closed else '')
        self.path(d, cls)

    def lines(self, segs, cls=None):
        """Many polylines in one path (drawn as one stroke)."""
        d = ' '.join('M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in s) for s in segs if len(s) > 1)
        if d:
            self.path(d, cls)

    def dashed(self, *pts, dash=4, gap=3, cls=None):
        """A polyline drawn as dashes, every dash in one path so it draws on as one stroke: a
        hypothetical link, a projection (sprint 050; sprint 049 drew a stemma's dash by dash).
        A dash carries on round a corner; the last is cut short where the line ends."""
        out, on, left, pen = [], True, dash, None
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            length, done = math.dist((x0, y0), (x1, y1)), 0.0
            while length - done > 1e-9:
                step = min(left, length - done)
                t0, t1 = done / length, (done + step) / length
                a = (x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0)
                b = (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)
                if on:
                    if pen != a:
                        out.append(f'M{f(a[0])} {f(a[1])}')
                    out.append(f'L{f(b[0])} {f(b[1])}')
                    pen = b
                done += step
                left -= step
                if left <= 1e-9:
                    on = not on
                    left = dash if on else gap
        if out:
            self.path(' '.join(out), cls)

    def circle(self, cx, cy, r, cls=None):
        self.path(f'M{f(cx - r)} {f(cy)} a{f(r)} {f(r)} 0 1 0 {f(2 * r)} 0 a{f(r)} {f(r)} 0 1 0 {f(-2 * r)} 0', cls)

    def ellipse(self, cx, cy, rx, ry, cls=None):
        self.path(f'M{f(cx - rx)} {f(cy)} a{f(rx)} {f(ry)} 0 1 0 {f(2 * rx)} 0 a{f(rx)} {f(ry)} 0 1 0 {f(-2 * rx)} 0', cls)

    def arc(self, cx, cy, r, a0, a1, n=48, cls=None, ry=None):
        """An arc about (cx, cy) from angle a0 to a1, in DEGREES (not radians: sprint 051 passed
        radians and drew a sliver), measured from east (+x) and turning clockwise on the page, since
        y runs down: 90 is straight down. `ry` makes it elliptical; `n` is its number of segments."""
        ry = r if ry is None else ry
        pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        self.line(*pts, cls=cls)

    def curve(self, d, cls=None):
        self.path(d, cls)

    def svg(self):
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" fill="none" '
               f'stroke="currentColor" stroke-width="{self.sw}" stroke-linecap="round" '
               f'stroke-linejoin="round" aria-hidden="true">']
        for kind, items in self.groups:
            if not items:
                continue
            attrs = ' stroke-width="0.6" opacity="0.55"' if kind == 'thin' else (
                ' stroke-width="0.9" opacity="0.8"' if kind == 'mid' else '')
            out.append(f'\t<g{attrs}>')
            for t, a, cls in items:
                if t == 'path':
                    out.append(f'\t\t<path pathLength="1" d="{a}"/>')
                else:
                    x, y, s, size, anchor = a
                    out.append(f'\t\t<text x="{f(x)}" y="{f(y)}" font-size="{size}" text-anchor="{anchor}" '
                               f'fill="currentColor" stroke="none" font-family="ui-monospace, monospace" '
                               f'letter-spacing="1">{s}</text>')
            out.append('\t</g>')
        out.append('</svg>')
        return '\n'.join(out) + '\n'

    def save(self, path):
        """Write the SVG to `path`, creating its directory."""
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w') as fh:
            fh.write(self.svg())


# clipping --------------------------------------------------------------
# Sprint 057 (korg 3576, 3557): four authors wrote their own Cyrus-Beck to clip hatching to a convex
# polygon, and sprint 051's enclosure fields went empty for want of one that took any polygon.

def inside(pt, poly):
    """Whether a point is inside a polygon (even-odd, so either winding, convex or not)."""
    x, y = pt
    hit = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


def _crossings(a, b, poly):
    """Where segment a-b crosses the polygon's edges, as fractions of the way from a to b."""
    rx, ry = b[0] - a[0], b[1] - a[1]
    out = []
    for q, q1 in zip(poly, poly[1:] + poly[:1]):
        sx, sy = q1[0] - q[0], q1[1] - q[1]
        den = rx * sy - ry * sx
        if abs(den) < 1e-12:
            continue
        qx, qy = q[0] - a[0], q[1] - a[1]
        t, u = (qx * sy - qy * sx) / den, (qx * ry - qy * rx) / den
        if 0 <= t <= 1 and -1e-12 <= u <= 1 + 1e-12:
            out.append(t)
    return out


def clip(pts, poly):
    """The parts of a polyline inside a polygon, any polygon (convex or not, either winding): a list
    of polylines, a piece kept whole while it stays inside. Draw them with `D.lines`."""
    pieces, cur = [], None
    for a, b in zip(pts, pts[1:]):
        ts = sorted({0.0, 1.0, *_crossings(a, b, poly)})
        for t0, t1 in zip(ts, ts[1:]):
            if t1 - t0 < 1e-9:
                continue
            at = lambda t: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)  # noqa: E731
            if not inside(at((t0 + t1) / 2), poly):
                cur = None
                continue
            p0, p1 = at(t0), at(t1)
            if cur and math.dist(cur[-1], p0) < 1e-9:
                cur.append(p1)
            else:
                cur = [p0, p1]
                pieces.append(cur)
    return pieces


def hatch(poly, step=5, angle=45):
    """Parallel lines `step` apart at `angle` degrees, clipped to a polygon (any polygon): a list of
    segments for `D.lines`. A line that would lie along the polygon's edge is left out."""
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    offs = [x * nx + y * ny for x, y in poly]
    along = [x * ux + y * uy for x, y in poly]
    lo, hi = min(along) - 1, max(along) + 1
    segs = []
    k = math.floor(min(offs) / step)
    while k * step < max(offs) - 1e-9:
        c = k * step
        k += 1
        if c <= min(offs) + 1e-9:
            continue
        p, q = (nx * c + ux * lo, ny * c + uy * lo), (nx * c + ux * hi, ny * c + uy * hi)
        segs.extend(clip([p, q], poly))
    return segs


def clip_polygon(poly, window):
    """A polygon cut to a convex window (Sutherland-Hodgman): the part inside, [] if none. A coast cut
    to a map's frame, a field cut to a parish."""
    area = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(window, window[1:] + window[:1]))
    sign = 1 if area > 0 else -1
    out = list(poly)
    for e0, e1 in zip(window, window[1:] + window[:1]):
        side = lambda p: sign * ((e1[0] - e0[0]) * (p[1] - e0[1]) - (e1[1] - e0[1]) * (p[0] - e0[0]))  # noqa: E731
        src, out = out, []
        for i, p in enumerate(src):
            prev = src[i - 1]
            sp, sq = side(p), side(prev)
            if sp >= 0:
                if sq < 0:
                    out.append(_meet(prev, p, sq, sp))
                out.append(p)
            elif sq >= 0:
                out.append(_meet(prev, p, sq, sp))
        if not out:
            return []
    clean = [p for i, p in enumerate(out) if math.dist(p, out[i - 1]) > 1e-9] if len(out) > 1 else out
    return clean if len(clean) >= 3 else []


def _meet(p, q, sp, sq):
    t = sp / (sp - sq)
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def rot(p, ax, ay, az=0):
    x, y, z = p
    ca, sa = math.cos(ax), math.sin(ax)
    y, z = y * ca - z * sa, y * sa + z * ca
    cb, sb = math.cos(ay), math.sin(ay)
    x, z = x * cb + z * sb, -x * sb + z * cb
    cc, sc = math.cos(az), math.sin(az)
    x, y = x * cc - y * sc, x * sc + y * cc
    return x, y, z


def wire(d, verts, cx, cy, s, ax, ay, az=0, cls=None):
    """Wireframe of a convex solid: edges are pairs at the minimum distance."""
    pts = [rot(v, ax, ay, az) for v in verts]
    dist = lambda a, b: math.dist(verts[a], verts[b])
    n = len(verts)
    m = min(dist(i, j) for i in range(n) for j in range(i + 1, n))
    segs = []
    for i in range(n):
        for j in range(i + 1, n):
            if abs(dist(i, j) - m) < 1e-3:
                a, b = pts[i], pts[j]
                segs.append([(cx + s * a[0], cy - s * a[1]), (cx + s * b[0], cy - s * b[1])])
    d.lines(segs, cls)


PHI = (1 + 5 ** 0.5) / 2
SOLIDS = {
    'tetra': [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)],
    'cube': [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)],
    'octa': [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)],
    'icosa': [p for a in (-1, 1) for b in (-PHI, PHI) for p in ((0, a, b), (a, b, 0), (b, 0, a))],
    'dodeca': [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    + [p for a in (-1 / PHI, 1 / PHI) for b in (-PHI, PHI) for p in ((0, a, b), (a, b, 0), (b, 0, a))],
}


