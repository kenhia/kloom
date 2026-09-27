"""Trace a line engraving into draw-on SVG bands (how the start-screen loom was made).

    python3 create-tools/trace-art/trace.py in.png out.svg [--bands 8]
        [--threshold 150] [--turdsize 6] [--opttolerance 0.6]
        [--tools .scratch/tools]

1. Flattens the image onto white, as greyscale (needs Pillow).
2. Traces it with the npm `potrace` port, installed once into the git-ignored
   tools prefix: `npm install --prefix .scratch/tools potrace`.
3. Sorts the contours by their left edge, splits them into bands, and writes
   one <path pathLength="1"> per band in its own <g>, coordinates to 0.1.
   Stroke the result, don't fill it: the contours come in pairs, which is
   the double-line wireframe look, and holes would fill solid.
"""
import argparse, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def flatten(src, dst):
    try:
        from PIL import Image
    except ImportError:
        sys.exit('trace.py: needs Pillow (pip install pillow) to flatten the image')
    im = Image.open(src).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    bg.convert('L').save(dst)


def rnd(t):
    return re.sub(r'-?\d+\.\d+', lambda m: ('%.1f' % float(m.group())).rstrip('0').rstrip('.'), t)


def bands(traced, n):
    d = re.search(r' d="([^"]+)"', traced).group(1)
    w, h = map(float, re.search(r'width="(\d+)" height="(\d+)"', traced).groups())
    subs = [m.strip() for m in re.split(r'(?=M)', d) if m.strip()]
    x0 = lambda p: float(re.match(r'M\s*(-?[\d.]+)', p).group(1))
    subs.sort(key=x0)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(w)} {int(h)}" fill="none" '
           f'stroke="currentColor" stroke-width="0.7" stroke-linejoin="round" aria-hidden="true">']
    for b in range(n):
        part = [p for p in subs if int(x0(p) / w * n) == b or (b == n - 1 and x0(p) >= w)]
        if part:
            out.append(f'\t<g><path pathLength="1" d="{rnd(" ".join(part))}"/></g>')
    out.append('</svg>')
    return '\n'.join(out) + '\n', len(subs)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('input')
    ap.add_argument('output')
    ap.add_argument('--bands', type=int, default=8)
    ap.add_argument('--threshold', type=int, default=150)
    ap.add_argument('--turdsize', type=int, default=6)
    ap.add_argument('--opttolerance', type=float, default=0.6)
    ap.add_argument('--tools', default='.scratch/tools')
    a = ap.parse_args()
    if not os.path.isdir(os.path.join(a.tools, 'node_modules', 'potrace')):
        sys.exit(f'trace.py: potrace not found; run: npm install --prefix {a.tools} potrace')
    with tempfile.TemporaryDirectory() as tmp:
        flat = os.path.join(tmp, 'flat.png')
        flatten(a.input, flat)
        traced = subprocess.run(
            ['node', os.path.join(HERE, 'potrace.mjs'), a.tools, flat,
             str(a.threshold), str(a.turdsize), str(a.opttolerance)],
            check=True, capture_output=True, text=True).stdout
    svg, count = bands(traced, a.bands)
    with open(a.output, 'w') as fh:
        fh.write(svg)
    print(f'{count} contours in {a.bands} bands -> {a.output} ({len(svg):,} bytes)')


if __name__ == '__main__':
    main()
