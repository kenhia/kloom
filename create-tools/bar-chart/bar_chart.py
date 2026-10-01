"""A reading-pane bar chart as a standalone, accessible SVG.

    python3 create-tools/bar-chart/bar_chart.py spec.json out.svg

The chart is inlined into the reading pane through the illustration
sanitiser, so it takes the reader's palette: it draws in currentColor (the
page's ink), and the page colours its `muted` and `accent` classes. It
carries <title> and <desc> for anyone opening the file on its own; in the
page, the markdown image's alt text names it. Put the same numbers in a
markdown table under the image too. Standard library only. See README.md.
"""
import json, math, sys
from xml.sax.saxutils import escape


def esc(v):
    """Spec text is plain text: escaped here, so a "<1%" label cannot break the SVG."""
    return escape(str(v))


def label(v, unit):
    """A value's label: one decimal under 100, unless it is a whole number (12, not 12.0)."""
    return f'{v:,.1f}{unit}' if v < 100 and v != int(v) else f'{v:,.0f}{unit}'


def scaler(spec, y0, y1):
    """Map a value to a y coordinate: linear from 0, or log10 between min and max."""
    axis = spec['axis']
    if spec.get('scale') == 'log':
        lo, hi = math.log10(axis['min']), math.log10(axis['max'])
        return lambda v: y1 - (math.log10(v) - lo) / (hi - lo) * (y1 - y0)
    return lambda v: y1 - v * (y1 - y0) / axis['max']


# Monospace glyphs advance about 0.6 em. Text nothing clips or crops still has to fit (sprint 021:
# three headings ran off the right edge and six labels overlapped, and no author could see it).
ADVANCE = 0.6


def problems(spec):
    """What would not fit: a heading wider than the chart, or a bar's labels wider than its slot."""
    W = spec.get('width', 480)
    x0, x1 = 64, W - 20
    out = []
    heading = x0 + len(spec['heading']) * (ADVANCE * 12 + 1)
    if heading > W:
        out.append(f'heading is ~{heading - W:.0f} units wider than the chart ({W}): shorten it or widen the chart')
    at = scaler(spec, 36, spec.get('height', 300) - 50)
    unit = spec.get('unit', '')
    slot = (x1 - x0) / len(spec['bars'])
    for i, b in enumerate(spec['bars']):
        # the value's label (baseline at the bar's top − 6, ~8 tall) against the heading (baseline 20)
        cx, half = x0 + slot * (i + 0.5), len(b.get('display', label(b['value'], unit))) * ADVANCE * 11 / 2
        if at(b['value']) - 6 - 8 < 23 and cx - half < heading:
            out.append(f'the label of "{b["label"]}" meets the heading: raise the axis max above {b["value"]}')
    # A tick's label ends 8 units left of the axis (x 56) and runs left from there (sprint 025: a
    # "1,000,000" tick was cut off at the chart's edge).
    room = x0 - 8 - 2
    for _, tick in spec['axis']['ticks']:
        wide = len(str(tick)) * ADVANCE * 11
        if wide > room:
            out.append(f'tick label "{tick}" is ~{wide - room:.0f} units wider than the {room} left of the axis: '
                       'shorten it ("1M", "10⁶")')
    for size, key in ((11, 'label'), (11, 'display'), (9, 'sublabel')):
        texts = [b.get(key, '') for b in spec['bars']]
        for a, b in zip(texts, texts[1:]):
            if (len(a) + len(b)) / 2 * ADVANCE * size > slot - 4:
                out.append(f'"{a}" and "{b}" overlap at {slot:.0f} units a bar: shorten them or widen the chart')
    return out


def chart(spec):
    W, H = spec.get('width', 480), spec.get('height', 300)
    x0, y0, x1, y1 = 64, 36, W - 20, H - 50
    at = scaler(spec, y0, y1)
    base = spec['axis']['min'] if spec.get('scale') == 'log' else 0
    unit = spec.get('unit', '')
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">',
           f'<title id="t">{esc(spec["title"])}</title>',
           f'<desc id="d">{esc(spec["description"])}</desc>',
           '<g font-family="ui-monospace, Menlo, Consolas, monospace" font-size="11" fill="currentColor">',
           '<g class="muted">']
    for v, lab in spec['axis']['ticks']:
        y = at(v)
        out.append(f'<line x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="currentColor" '
                   f'stroke-opacity="{0.9 if v == base else 0.3}" stroke-width="{1 if v == base else 0.6}"/>')
        out.append(f'<text x="{x0 - 8}" y="{y + 4:.1f}" text-anchor="end">{esc(lab)}</text>')
    out.append('</g>')
    bars = spec['bars']
    bw = spec.get('barWidth', 56)
    slot = (x1 - x0) / len(bars)
    for i, b in enumerate(bars):
        cx = x0 + slot * (i + 0.5)
        h = y1 - at(b['value'])
        hi = b.get('highlight', False)
        shown = b.get('display', label(b['value'], unit))
        out.append(f'<rect x="{cx - bw / 2:.1f}" y="{y1 - h:.1f}" width="{bw}" height="{max(h, 1):.1f}" '
                   + ('class="accent" fill="currentColor"/>' if hi else 'fill-opacity="0.85"/>'))
        out.append(f'<text x="{cx:.1f}" y="{y1 - h - 6:.1f}" text-anchor="middle">{esc(shown)}</text>')
        out.append(f'<text x="{cx:.1f}" y="{y1 + 16}" text-anchor="middle">{esc(b["label"])}</text>')
        if b.get('sublabel'):
            out.append(f'<text x="{cx:.1f}" y="{y1 + 30}" text-anchor="middle" font-size="9" class="muted" fill="currentColor">{esc(b["sublabel"])}</text>')
    out.append(f'<text x="{x0}" y="20" font-size="12" letter-spacing="1">{esc(spec["heading"])}</text>')
    out.append('</g></svg>')
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1]) as fh:
        spec = json.load(fh)
    wrong = problems(spec)
    if wrong:
        sys.exit('\n'.join(f'bar_chart: {w}' for w in wrong))
    svg = chart(spec)
    with open(sys.argv[2], 'w') as fh:
        fh.write(svg)
