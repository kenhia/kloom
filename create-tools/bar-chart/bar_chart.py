"""A reading-pane bar chart as a standalone, accessible SVG.

    python3 create-tools/bar-chart/bar_chart.py spec.json out.svg

The chart is inlined into the reading pane through the illustration
sanitiser, so it takes the reader's palette: it draws in currentColor (the
page's ink), and the page colours its `muted` and `accent` classes. It
carries <title> and <desc> for anyone opening the file on its own; in the
page, the markdown image's alt text names it. Put the same numbers in a
markdown table under the image too. A spec with a `source` also prints the
chart's `media` citation, its data's DOI in `doi` (sprint 033), and warns of
a Wikipedia url not cited by revision. Since sprint 057 a value may be
negative (on a linear axis with a `min` below zero), a spec with `series`
draws grouped bars with a legend, and a value's label keeps the data's own
decimals. Standard library only. See README.md.
"""
import datetime, decimal, json, math, os, re, sys
from xml.sax.saxutils import escape


def esc(v):
    """Spec text is plain text: escaped here, so a "<1%" label cannot break the SVG."""
    return escape(str(v))


def label(v, unit):
    """A value's label, with the decimals the data gives it and none for a whole number (12, not
    12.0: sprint 015). Sprint 057 (korg 3557): a value over 100 was rounded whole, 159.7 shown as 160,
    beside 94.6 shown as written. A negative value takes a true minus sign."""
    places = 0 if v == int(v) else max(0, -decimal.Decimal(repr(float(v))).as_tuple().exponent)
    return f'{"−" if v < 0 else ""}{abs(v):,.{places}f}{unit}'


def scaler(spec, y0, y1):
    """Map a value to a y coordinate: linear from the axis `min` (0 unless a value is negative), or
    log10 between min and max."""
    axis = spec['axis']
    if spec.get('scale') == 'log':
        lo, hi = math.log10(axis['min']), math.log10(axis['max'])
        return lambda v: y1 - (math.log10(v) - lo) / (hi - lo) * (y1 - y0)
    lo, hi = axis.get('min', 0), axis['max']
    return lambda v: y1 - (v - lo) * (y1 - y0) / (hi - lo)


def zero_at(spec, at, y1):
    """Where a bar starts: the axis's zero on a linear axis, its foot on a log one."""
    return y1 if spec.get('scale') == 'log' else at(0)


# A grouped chart's series are told apart by fill, in this order: the ink, the accent, the muted
# color, then an outline. Each is its own palette hook, so each follows the palette mode.
SERIES_STYLE = ['fill-opacity="0.85"', 'class="accent" fill="currentColor"', 'class="muted" fill="currentColor"',
                'fill="none" stroke="currentColor" stroke-width="1.2"']


def placed(spec):
    """Every bar as (group index, x center, width, value, its label, its label's font size): one a
    group without `series`, len(series) side by side with them."""
    W = spec.get('width', 480)
    x0, x1 = 64, W - 20
    groups = spec['bars']
    slot = (x1 - x0) / len(groups)
    unit = spec.get('unit', '')
    out = []
    series = spec.get('series')
    for i, b in enumerate(groups):
        cx = x0 + slot * (i + 0.5)
        if not series:
            out.append((i, cx, spec.get('barWidth', 56), b['value'], b.get('display', label(b['value'], unit)), 11))
            continue
        n = len(series)
        bw = spec.get('barWidth', min(56, round(slot * 0.8 / n, 1)))
        total = n * bw + (n - 1) * 2
        shown = b.get('displays') or [label(v, unit) for v in b.get('values', [])]
        for k, v in enumerate(b.get('values', [])):
            out.append((i, cx - total / 2 + bw / 2 + k * (bw + 2), bw, v, shown[k] if k < len(shown) else '', 9))
    return out


def legend(spec):
    """A grouped chart's legend, on the heading's line and ending at the plot's right edge: its left
    edge, and each key as (x, series label, style)."""
    W = spec.get('width', 480)
    keys, x = [], W - 20
    for k, s in reversed(list(enumerate(spec.get('series') or []))):
        x -= 12 + len(s['label']) * ADVANCE * 9
        keys.insert(0, (x, s['label'], SERIES_STYLE[k % len(SERIES_STYLE)]))
        x -= 12
    return x + 12, keys


# Monospace glyphs advance about 0.6 em. Text nothing clips or crops still has to fit (sprint 021:
# three headings ran off the right edge and six labels overlapped, and no author could see it).
ADVANCE = 0.6


def problems(spec):
    """What would not fit: a heading wider than the chart, or a bar's labels wider than its slot; and
    what cannot be drawn: a value outside the axis, a group whose values do not match its series."""
    W = spec.get('width', 480)
    x0, x1 = 64, W - 20
    H = spec.get('height', 300)
    y1 = H - 50
    out = []
    heading = x0 + len(spec['heading']) * (ADVANCE * 12 + 1)
    if heading > W:
        out.append(f'heading is ~{heading - W:.0f} units wider than the chart ({W}): shorten it or widen the chart')
    series = spec.get('series')
    log = spec.get('scale') == 'log'
    if series:
        if len(series) > len(SERIES_STYLE):
            out.append(f'{len(series)} series: at most {len(SERIES_STYLE)} can be told apart')
        for b in spec['bars']:
            if len(b.get('values', [])) != len(series):
                out.append(f'"{b["label"]}" has {len(b.get("values", []))} values for {len(series)} series')
            if 'displays' in b and len(b['displays']) != len(b.get('values', [])):
                out.append(f'"{b["label"]}" has {len(b["displays"])} displays for {len(b.get("values", []))} values')
            if 'value' in b or b.get('highlight'):
                out.append(f'"{b["label"]}": a grouped chart\'s bars take `values`, one a series, and no highlight')
        left, _ = legend(spec)
        if heading + 8 > left:
            out.append(f'the legend meets the heading by ~{heading + 8 - left:.0f} units: shorten either, or widen the chart')
        if out:
            return out
    lo = spec['axis'].get('min', 0)
    for _, _, _, v, _, _ in placed(spec):
        if log and v <= 0:
            out.append(f'{v} cannot be drawn on a log axis: chart it on a linear one')
        elif not log and v < lo:
            out.append(f'{v} is below the axis min ({lo}): give the axis a min of {v} or lower')
    if out:
        return out
    at = scaler(spec, 36, y1)
    zero = zero_at(spec, at, y1)
    for i, cx, _, v, shown, size in placed(spec):
        name = spec['bars'][i]['label']
        half = len(shown) * ADVANCE * size / 2
        # the value's label (baseline at the bar's top − 6, ~8 tall) against the heading (baseline 20)
        if v >= 0 and at(v) - 6 - 8 < 23 and cx - half < heading:
            out.append(f'the label of "{name}" meets the heading: raise the axis max above {v}')
        # a negative bar's label hangs under its end, and must clear the bars' own labels (baseline y1 + 16)
        if v < 0 and at(v) + 14 + 3 > y1 + 16 - 8:
            out.append(f'the label of "{name}" ({shown}) meets the bars\' labels: lower the axis min below {v}')
    # A tick's label ends 8 units left of the axis (x 56) and runs left from there (sprint 025: a
    # "1,000,000" tick was cut off at the chart's edge).
    room = x0 - 8 - 2
    for _, tick in spec['axis']['ticks']:
        wide = len(str(tick)) * ADVANCE * 11
        if wide > room:
            out.append(f'tick label "{tick}" is ~{wide - room:.0f} units wider than the {room} left of the axis: '
                       'shorten it ("1M", "10⁶")')
    slot = (x1 - x0) / len(spec['bars'])
    keys = ((11, 'label'), (9, 'sublabel')) if series else ((11, 'label'), (11, 'display'), (9, 'sublabel'))
    for size, key in keys:
        texts = [b.get(key, '') for b in spec['bars']]
        for a, b in zip(texts, texts[1:]):
            if (len(a) + len(b)) / 2 * ADVANCE * size > slot - 4:
                out.append(f'"{a}" and "{b}" overlap at {slot:.0f} units a bar: shorten them or widen the chart')
    if series:  # neighboring values' labels, across a group and from one group to the next
        bars = placed(spec)
        for (_, ca, _, va, a, size), (_, cb, _, vb, b, _) in zip(bars, bars[1:]):
            if a and b and (len(a) + len(b)) / 2 * ADVANCE * size > cb - ca - 1 and abs(at(va) - at(vb)) < 10:
                out.append(f'the values "{a}" and "{b}" overlap: widen the chart, or give a group `displays` '
                           'with "" for a label not needed')
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
    zero = zero_at(spec, at, y1)
    series = spec.get('series')
    every = placed(spec)
    slot = (x1 - x0) / len(bars)
    for i, b in enumerate(bars):
        for k, (_, cx, bw, v, shown, size) in enumerate(p for p in every if p[0] == i):
            top = at(v)
            if v >= 0:
                h = zero - top
                y, ly = zero - h, zero - h - 6
            else:  # a negative bar hangs from zero, its value under its end (sprint 057)
                h = top - zero
                y, ly = zero, zero + h + 14
            if series:
                style = SERIES_STYLE[k % len(SERIES_STYLE)]
            else:
                style = 'class="accent" fill="currentColor"' if b.get('highlight', False) else 'fill-opacity="0.85"'
            out.append(f'<rect x="{cx - bw / 2:.1f}" y="{y:.1f}" width="{bw}" height="{max(h, 1):.1f}" {style}/>')
            if shown:
                sized = '' if size == 11 else f' font-size="{size}"'
                out.append(f'<text x="{cx:.1f}" y="{ly:.1f}" text-anchor="middle"{sized}>{esc(shown)}</text>')
        cx = x0 + slot * (i + 0.5)
        out.append(f'<text x="{cx:.1f}" y="{y1 + 16}" text-anchor="middle">{esc(b["label"])}</text>')
        if b.get('sublabel'):
            out.append(f'<text x="{cx:.1f}" y="{y1 + 30}" text-anchor="middle" font-size="9" class="muted" fill="currentColor">{esc(b["sublabel"])}</text>')
    if series:
        for x, name, style in legend(spec)[1]:
            out.append(f'<rect x="{x:.1f}" y="12" width="8" height="8" {style}/>')
            out.append(f'<text x="{x + 12:.1f}" y="20" font-size="9">{esc(name)}</text>')
    out.append(f'<text x="{x0}" y="20" font-size="12" letter-spacing="1">{esc(spec["heading"])}</text>')
    out.append('</g></svg>')
    return '\n'.join(out) + '\n'


def media_citation(spec, out, today=None):
    """The chart's `media` citation, from the spec's `source` ({container, doi and/or url, accessed?}):
    a chart drawn here, MIT, by kloom contributors, crediting its data. None without a source."""
    src = spec.get('source')
    if not src:
        return None
    today = today or datetime.datetime.now(datetime.timezone.utc).date()  # UTC, as wiki_cite (sprint 058)
    c = {'kind': 'media', 'title': spec['title'], 'authors': [{'name': 'kloom contributors'}],
         'published': str(today.year), 'container': src['container']}
    for k in ('url', 'doi'):
        if src.get(k):
            c[k] = src[k]
    c.update(accessed=src.get('accessed', today.isoformat()), licence='MIT', file=os.path.basename(out))
    return c


def source_warnings(spec):
    """What a `source` should say better (sprint 057, korg 3576: a Wikipedia table cited by its live
    page): a Wikipedia url is cited by revision, `oldid=`, as every Wikipedia citation is."""
    url = str((spec.get('source') or {}).get('url', ''))
    if re.match(r'https?://[a-z-]+\.(m\.)?wikipedia\.org/', url) and 'oldid=' not in url:
        return [f'source.url {url} is a live Wikipedia page: cite the revision you read, '
                '…/w/index.php?title=…&oldid=N (wiki_cite.py prints it)']
    return []


def source_problems(spec):
    """What a `source` lacks: where the data is from, and a link to it."""
    src = spec.get('source')
    if src is None:
        return []
    out = []
    if not src.get('container'):
        out.append('source needs its container: "Chart drawn for kloom from …"')
    if not (src.get('doi') or src.get('url')):
        out.append('source needs the data\'s doi (bare, 10.…) or url')
    if str(src.get('doi', '')).startswith(('http', 'doi.org')):
        out.append('source.doi is the bare DOI, 10.…, not a link')
    return out


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1]) as fh:
        spec = json.load(fh)
    wrong = problems(spec) + source_problems(spec)
    if wrong:
        sys.exit('\n'.join(f'bar_chart: {w}' for w in wrong))
    for w in source_warnings(spec):
        print(f'bar_chart: warning: {w}', file=sys.stderr)
    svg = chart(spec)
    with open(sys.argv[2], 'w') as fh:
        fh.write(svg)
    cited = media_citation(spec, sys.argv[2])
    if cited:
        print(json.dumps(cited, ensure_ascii=False, indent='\t'))
