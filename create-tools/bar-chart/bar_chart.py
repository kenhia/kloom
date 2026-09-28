"""A reading-pane bar chart as a standalone, accessible SVG.

    python3 create-tools/bar-chart/bar_chart.py spec.json out.svg

The chart is shown with <img>, so it cannot inherit the page's palette: the
spec names its colours (use the frame's palette). It carries <title> and
<desc> for screen readers; put the same numbers in a markdown table under
the image too. Standard library only. See README.md for the spec.
"""
import json, math, sys


def label(v, unit):
    return f'{v:,.1f}{unit}' if v < 100 else f'{v:,.0f}{unit}'


def scaler(spec, y0, y1):
    """Map a value to a y coordinate: linear from 0, or log10 between min and max."""
    axis = spec['axis']
    if spec.get('scale') == 'log':
        lo, hi = math.log10(axis['min']), math.log10(axis['max'])
        return lambda v: y1 - (math.log10(v) - lo) / (hi - lo) * (y1 - y0)
    return lambda v: y1 - v * (y1 - y0) / axis['max']


def chart(spec):
    W, H = spec.get('width', 480), spec.get('height', 300)
    x0, y0, x1, y1 = 64, 36, W - 20, H - 50
    c = spec['colours']
    at = scaler(spec, y0, y1)
    base = spec['axis']['min'] if spec.get('scale') == 'log' else 0
    unit = spec.get('unit', '')
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">',
           f'<title id="t">{spec["title"]}</title>',
           f'<desc id="d">{spec["description"]}</desc>',
           f'<rect width="{W}" height="{H}" fill="{c["background"]}"/>',
           f'<g font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="{c["muted"]}">']
    for v, lab in spec['axis']['ticks']:
        y = at(v)
        out.append(f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{c["muted"]}" '
                   f'stroke-opacity="{0.9 if v == base else 0.3}" stroke-width="{1 if v == base else 0.6}"/>')
        out.append(f'<text x="{x0 - 8}" y="{y + 4:.1f}" text-anchor="end">{lab}</text>')
    bars = spec['bars']
    bw = spec.get('barWidth', 56)
    slot = (x1 - x0) / len(bars)
    for i, b in enumerate(bars):
        cx = x0 + slot * (i + 0.5)
        h = y1 - at(b['value'])
        hi = b.get('highlight', False)
        shown = b.get('display', label(b['value'], unit))
        out.append(f'<rect x="{cx - bw / 2:.1f}" y="{y1 - h:.1f}" width="{bw}" height="{max(h, 1):.1f}" '
                   f'fill="{c["accent"] if hi else c["ink"]}" fill-opacity="{1 if hi else 0.85}"/>')
        out.append(f'<text x="{cx:.1f}" y="{y1 - h - 6:.1f}" text-anchor="middle" fill="{c["ink"]}">{shown}</text>')
        out.append(f'<text x="{cx:.1f}" y="{y1 + 16}" text-anchor="middle" fill="{c["ink"]}">{b["label"]}</text>')
        if b.get('sublabel'):
            out.append(f'<text x="{cx:.1f}" y="{y1 + 30}" text-anchor="middle" font-size="9">{b["sublabel"]}</text>')
    out.append(f'<text x="{x0}" y="20" font-size="12" fill="{c["ink"]}" letter-spacing="1">{spec["heading"]}</text>')
    out.append('</g></svg>')
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1]) as fh:
        svg = chart(json.load(fh))
    with open(sys.argv[2], 'w') as fh:
        fh.write(svg)
