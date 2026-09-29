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

    def circle(self, cx, cy, r, cls=None):
        self.path(f'M{f(cx - r)} {f(cy)} a{f(r)} {f(r)} 0 1 0 {f(2 * r)} 0 a{f(r)} {f(r)} 0 1 0 {f(-2 * r)} 0', cls)

    def ellipse(self, cx, cy, rx, ry, cls=None):
        self.path(f'M{f(cx - rx)} {f(cy)} a{f(rx)} {f(ry)} 0 1 0 {f(2 * rx)} 0 a{f(rx)} {f(ry)} 0 1 0 {f(-2 * rx)} 0', cls)

    def arc(self, cx, cy, r, a0, a1, n=48, cls=None, ry=None):
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


