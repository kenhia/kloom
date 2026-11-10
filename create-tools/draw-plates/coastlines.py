"""Coastlines for a plate's map, from Natural Earth's land (public domain), shared by every subject's
plates (sprint 057, korg 3576: sprint 055 embedded 1:50m land in one plate's module, and another
author, with nothing to take it from, entered coasts by hand).

    from coastlines import land, project
    rings = project(land('wallacea'), lambda lon: 20 + (lon - 110) * 28, lambda lat: 24 + (-1 - lat) * 28)
    for ring in rings:
        d.line(*ring, closed=True)

A region is a box of land cut once and kept in `coastlines.json`: its rings of (lon, lat) points,
clipped to the box, simplified to a tolerance in degrees and rounded to 0.01 degrees. `land(name)`
returns them; `project` maps them to the plate with your own projection. To cut a new region (the
only step that needs the network; the plates never do):

    python3 create-tools/draw-plates/coastlines.py add NAME --box=WEST,SOUTH,EAST,NORTH \
        [--tolerance 0.04] [--scale 50m] [--note "what it is for"]

It downloads Natural Earth's land at that scale (110m, 50m or 10m) once into `.scratch/`, cuts the
box and adds the region, refusing a name already there. Draw a ring as a closed line: where land
runs off the box, its ring runs along the box's edge, which the map's frame covers. Natural Earth
is public domain, so a plate drawn from it needs no credit, but say in a comment where the data is
from. Standard library only.
"""
import argparse, json, math, os, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plates import clip_polygon  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'coastlines.json')
ROOT = os.path.join(HERE, '..', '..')
SOURCE = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_{scale}_land.geojson'


def regions():
    with open(DATA) as fh:
        return json.load(fh)


def land(name):
    """A region's rings of (lon, lat) points."""
    known = regions()
    if name not in known:
        raise KeyError(f'no coastline region "{name}" (there are {", ".join(sorted(known))}); cut one with '
                       '`coastlines.py add`')
    return [[tuple(p) for p in ring] for ring in known[name]['rings']]


def project(rings, x, y):
    """Rings of (lon, lat) as rings of plate points, through your projection's x(lon) and y(lat)."""
    return [[(x(lon), y(lat)) for lon, lat in ring] for ring in rings]


def _simplify(pts, tolerance):
    """Douglas-Peucker on an open polyline."""
    if len(pts) < 3:
        return list(pts)
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    norm = math.hypot(dx, dy)
    far, at = -1.0, 0
    for i, (x, y) in enumerate(pts[1:-1], 1):
        dist = abs(dy * (x - x0) - dx * (y - y0)) / norm if norm else math.hypot(x - x0, y - y0)
        if dist > far:
            far, at = dist, i
    if far <= tolerance:
        return [pts[0], pts[-1]]
    return _simplify(pts[:at + 1], tolerance)[:-1] + _simplify(pts[at:], tolerance)


def _simplify_ring(ring, tolerance):
    """A closed ring simplified, split at its first point and at the point farthest from it."""
    if len(ring) < 4:
        return list(ring)
    far = max(range(len(ring)), key=lambda i: math.dist(ring[0], ring[i]))
    a = _simplify(ring[:far + 1], tolerance)
    b = _simplify(ring[far:] + [ring[0]], tolerance)
    return a[:-1] + b[:-1]


def _area(ring):
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]))) / 2


def region(geojson, box, tolerance=0.04):
    """The rings of a GeoJSON's land inside a box (west, south, east, north), clipped, simplified to
    `tolerance` degrees and rounded to 0.01; an island that simplifies away is left out."""
    west, south, east, north = box
    window = [(west, south), (east, south), (east, north), (west, north)]
    out = []
    for f in geojson['features']:
        g = f['geometry']
        polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
        for poly in polys:
            for ring in poly:
                pts = [(float(x), float(y)) for x, y in ring]
                if pts and pts[0] == pts[-1]:
                    pts = pts[:-1]
                xs, ys = [p[0] for p in pts], [p[1] for p in pts]
                if not pts or max(xs) < west or min(xs) > east or max(ys) < south or min(ys) > north:
                    continue
                cut = clip_polygon(pts, window)
                if not cut:
                    continue
                simple = _simplify_ring(cut, tolerance)
                rounded = []
                for x, y in simple:
                    p = (_num(x), _num(y))
                    if not rounded or rounded[-1] != p:
                        rounded.append(p)
                if len(rounded) > 1 and rounded[0] == rounded[-1]:
                    rounded.pop()
                if len(rounded) >= 3 and _area(rounded) >= tolerance * tolerance:
                    out.append(rounded)
    return out


def _num(v):
    v = round(v, 2)
    return int(v) if v == int(v) else v


def natural_earth(scale):
    """Natural Earth's land at a scale, downloaded once into .scratch/."""
    cache = os.path.join(ROOT, '.scratch', 'natural-earth', f'ne_{scale}_land.geojson')
    if not os.path.exists(cache):
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        req = urllib.request.Request(SOURCE.format(scale=scale), headers={'User-Agent': 'kloom-create-tools/1.0'})
        with urllib.request.urlopen(req, timeout=120) as r, open(cache, 'wb') as fh:
            fh.write(r.read())
    with open(cache) as fh:
        return json.load(fh)


def write(known):
    """coastlines.json, as Prettier writes it (`just check` runs Prettier over every JSON file): a
    point a line."""
    parts = []
    for name, r in known.items():
        head = ''.join(f'\t\t{json.dumps(k)}: {json.dumps(r[k], ensure_ascii=False)},\n'
                       for k in ('source', 'box', 'tolerance', 'note'))
        rings = ',\n'.join('\t\t\t[\n' + ',\n'.join(f'\t\t\t\t{json.dumps(list(p))}' for p in ring)
                           + '\n\t\t\t]' for ring in r['rings'])
        parts.append(f'\t{json.dumps(name)}: {{\n{head}\t\t"rings": [\n{rings}\n\t\t]\n\t}}')
    with open(DATA, 'w') as fh:
        fh.write('{\n' + ',\n'.join(parts) + '\n}\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('list', help='the regions there are')
    a = sub.add_parser('add', help="cut a region from Natural Earth's land")
    a.add_argument('name')
    a.add_argument('--box', required=True, metavar='WEST,SOUTH,EAST,NORTH',
                   help='degrees, west and south negative; write it --box=-92,-2,-89,1 so a minus is not read as an option')
    a.add_argument('--tolerance', type=float, default=0.04, help='simplify to this many degrees (default 0.04)')
    a.add_argument('--scale', choices=('110m', '50m', '10m'), default='50m')
    a.add_argument('--note', default='')
    args = ap.parse_args()
    known = regions()
    if args.cmd == 'list':
        for name, r in known.items():
            print(f'{name}: box {r["box"]}, {len(r["rings"])} rings, {r["source"]}. {r.get("note", "")}')
        return
    if args.name in known:
        sys.exit(f'coastlines: there is already a region "{args.name}"; name the new one differently')
    box = [float(v) for v in args.box.split(',')]
    if len(box) != 4 or box[0] >= box[2] or box[1] >= box[3]:
        sys.exit('coastlines: --box is WEST,SOUTH,EAST,NORTH in degrees, east of west and north of south')
    rings = region(natural_earth(args.scale), box, args.tolerance)
    known[args.name] = {'source': f'Natural Earth 1:{args.scale} land (public domain)', 'box': [_num(v) for v in box],
                        'tolerance': args.tolerance, 'note': args.note, 'rings': rings}
    write(known)
    print(f'coastlines: {args.name}: {len(rings)} rings, {sum(map(len, rings))} points → {DATA}')


if __name__ == '__main__':
    main()
