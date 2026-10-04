"""A contact sheet of a subject's plates, each in its own palette (sprint 014).

    python3 create-tools/draw-plates/contact_sheet.py SUBJECT [frame ...] [--out FILE] [--png FILE] [--scale N]
        [--per-plate | --one-sheet]

Writes an HTML page (default `.scratch/contact-<subject>.html`) showing each
frame's scene.svg at its own size (400 by 300) in its palette's background,
line and accent colours, with its headline and accent word under it, four to
a row. With `--png`, a headless Chromium screenshots the page: the one
Playwright installed under ~/.cache/ms-playwright, or `$CHROME`. The PNG is
as wide as its plates, so one plate is one plate wide (sprint 027; it was
always four, 4,090 pixels at `--scale 2.5`). `--scale 2.5` renders it at
that many device pixels per CSS pixel, to read a plate's labels (sprint 015);
`--scale 1`, the default, is the plate at its real size. `--palette NAME`
colours a plate whose frame.json is not written yet, and `--palette
FRAME=NAME` (repeatable) one frame's, written or not.

Above two plates, `--png FILE.png` writes one PNG per plate,
`FILE-<frame>.png` (a chart's `FILE-<frame>-<chart>.png`), each one plate
wide: four plates at `--scale 2.5` made a sheet over 4,000 pixels wide that
an image reader shrank past reading, and four of sprint 028's authors
cropped by hand (sprint 029). `--per-plate` asks for that at any count,
`--one-sheet` for the single sheet at any count. Standard library only.
"""
import argparse, glob, html, json, os, re, subprocess, sys, tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')


def chrome():
    if os.environ.get('CHROME'):
        return os.environ['CHROME']
    found = sorted(glob.glob(os.path.expanduser('~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell')))
    if not found:
        sys.exit('contact_sheet: no headless Chromium found; set $CHROME')
    return found[-1]


# A cell: the plate (400 by 300) and its caption, padded; the page's gaps between and around.
CELL_W, CELL_H, GAP, COLUMNS = 416, 360, 6, 4


def window(cells):
    """The CSS pixel size of a page of `cells` plates: as wide as its widest row, as tall as its rows."""
    cols = max(1, min(COLUMNS, cells))
    rows = max(1, (cells + COLUMNS - 1) // COLUMNS)
    return cols * CELL_W + (cols + 1) * GAP, rows * (CELL_H + GAP) + GAP


def per_plate(cells, asked=None):
    """Whether to write a PNG per plate: as asked, else above two plates."""
    return asked if asked is not None else cells > 2


def plate_png(png, fid, name=None, illustration=None):
    """FILE.png's name for one plate (FILE-<frame>.png) or one chart (FILE-<frame>-<chart>.png)."""
    stem, ext = os.path.splitext(png)
    chart = '' if name is None or name == illustration else '-' + os.path.splitext(name)[0]
    return f'{stem}-{fid}{chart}{ext or ".png"}'


def page(cells):
    """The sheet's HTML for these cells, four to a row."""
    return ('<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#888;display:grid;'
            f'grid-template-columns:repeat({max(1, min(COLUMNS, len(cells)))},{CELL_W}px);'
            f'grid-auto-rows:{CELL_H}px;gap:{GAP}px;padding:{GAP}px;width:max-content;font:13px system-ui}}'
            'figure{margin:0;padding:8px;box-sizing:border-box;overflow:hidden}svg{width:400px;height:300px;display:block}'
            'figcaption b{font-weight:800}figcaption{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
            'small{display:block;margin-top:2px}'
            '.muted{color:var(--muted)}.accent{color:var(--accent)}</style>' + ''.join(cells))


def shoot(html_path, png, cells, scale):
    """Screenshot a page of `cells` plates to `png`; returns its size in pixels."""
    w, h = window(cells)
    subprocess.run([chrome(), '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                    f'--window-size={w},{h}', f'--force-device-scale-factor={scale:g}', f'--screenshot={os.path.abspath(png)}',
                    'file://' + os.path.abspath(html_path)], check=True, capture_output=True)
    return round(w * scale), round(h * scale)


# Monospace glyphs advance about 0.6 em, as bar_chart.py estimates a chart's text (sprint 021); a
# capital stands about 0.75 em above its baseline, and a descender 0.25 em below.
ADVANCE, ASCENT, DESCENT = 0.6, 0.75, 0.25
TEXT = re.compile(r'<text\b([^>]*)>(.*?)</text>', re.S)


def text_overflows(svg):
    """Where a plate's text runs off its viewBox: one line each, by how far (korg 3554: bar_chart
    warns of a chart's text, and a plate's labels ran off unseen in sprint 049). A turned label
    (a `transform` or `rotate`) is not estimated."""
    box = re.search(r'viewBox="\s*([-\d.]+)[\s,]+([-\d.]+)[\s,]+([-\d.]+)[\s,]+([-\d.]+)', svg)
    if not box:
        return []
    x0, y0, w, h = map(float, box.groups())
    out = []
    for m in TEXT.finditer(svg):
        attrs, body = m.group(1), html.unescape(re.sub(r'<[^>]+>', '', m.group(2)))
        attr = lambda k, d=None: (re.search(rf'\b{k}="([^"]*)"', attrs) or [None, d])[1]  # noqa: E731
        if attr('transform') or attr('rotate') or not body.strip():
            continue
        try:
            x, y = float(attr('x', 0)), float(attr('y', 0))
            size, spacing = float(attr('font-size', 9)), float(attr('letter-spacing', 0))
        except ValueError:
            continue
        n = len(body)
        wide = n * ADVANCE * size + (n - 1) * spacing
        left = {'middle': x - wide / 2, 'end': x - wide}.get(attr('text-anchor', 'start'), x)
        said = f'"{body}" runs ~{{:.0f}} units past the {{}}'
        for over, edge in ((x0 - left, 'left edge'), (left + wide - (x0 + w), f'right edge ({x0 + w:g})'),
                           (y0 - (y - ASCENT * size), 'top edge'), (y + DESCENT * size - (y0 + h), f'bottom edge ({y0 + h:g})')):
            if over >= 1:
                out.append(said.format(over, edge))
    return out


def palettes_for(args, known):
    """(the palette for an unwritten plate, {frame: palette}) from repeated --palette values."""
    default, per_frame = None, {}
    for value in args or []:
        frame, _, name = value.rpartition('=')
        if name not in known:
            sys.exit(f'contact_sheet: no palette "{name}" (the subject has {", ".join(known)})')
        if frame:
            per_frame[frame] = name
        else:
            default = name
    return default, per_frame


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('subject')
    ap.add_argument('frames', nargs='*')
    ap.add_argument('--out')
    ap.add_argument('--png')
    ap.add_argument('--scale', type=float, default=1, help='device pixels per CSS pixel in the PNG')
    ap.add_argument('--charts', action='store_true',
                    help="also show each frame's other SVGs (its inlined charts), in the frame's palette")
    one = ap.add_mutually_exclusive_group()
    one.add_argument('--per-plate', dest='per_plate', action='store_true', default=None,
                     help='with --png: one PNG per plate, FILE-<frame>.png (the default above two plates)')
    one.add_argument('--one-sheet', dest='per_plate', action='store_false',
                     help='with --png: one sheet of every plate, at any count')
    ap.add_argument('--palette', action='append', metavar='[FRAME=]NAME',
                    help="a palette for plates whose frame.json is not written yet, or FRAME=NAME for one "
                         "frame's (repeatable)")
    a = ap.parse_args()
    sdir = os.path.join(ROOT, 'subjects', a.subject)
    palettes = json.load(open(os.path.join(sdir, 'subject.json')))['palettes']
    default_palette, frame_palette = palettes_for(a.palette, palettes)
    frames = a.frames or sorted(os.listdir(os.path.join(sdir, 'frames')))
    cells, named = [], []
    for fid in frames:
        fdir = os.path.join(sdir, 'frames', fid)
        try:
            if os.path.exists(os.path.join(fdir, 'frame.json')):
                s = json.load(open(os.path.join(fdir, 'frame.json')))['scene']
            else:  # a frame still being written: its plate, in the first palette, untitled
                s = {'illustration': 'scene.svg', 'palette': default_palette or next(iter(palettes)),
                     'headline': '(no frame.json yet)', 'accent': ''}
            if fid in frame_palette:  # sprint 024: one --palette coloured every frame named
                s = {**s, 'palette': frame_palette[fid]}
            svgs = [(s['illustration'], open(os.path.join(fdir, s['illustration'])).read())]
            if a.charts:  # sprint 021: authors had no way to see a chart before its frame went live
                svgs += [(f, open(os.path.join(fdir, f)).read()) for f in sorted(os.listdir(fdir))
                         if f.endswith('.svg') and f != s['illustration']]
        except (OSError, KeyError, ValueError) as e:
            print(f'contact_sheet: skipping {fid}: {e}', file=sys.stderr)
            continue
        p = palettes[s['palette']]
        for name, svg in svgs:
            for line in text_overflows(svg):
                print(f'contact_sheet: warning: {fid}/{name}: {line}', file=sys.stderr)
            title = (f'{html.escape(s["headline"])} <b style="color:{p["accent"]}">{html.escape(s["accent"])}</b>'
                     if name == s['illustration'] else html.escape(name))
            named.append(plate_png(a.png or 'plate.png', fid, name, s['illustration']))
            cells.append(
                f'<figure style="background:{p["background"]};color:{p["line"]};--muted:{p["muted"]};--accent:{p["accent"]}">{svg}'
                f'<figcaption style="color:{p["ink"]}">{title}'
                f'<small style="color:{p["muted"]}">{html.escape(fid)} · {html.escape(s["palette"])}</small></figcaption></figure>')
    # Beside its PNG by default, so authors drawing at once don't overwrite one page (sprint 021).
    out = a.out or (os.path.splitext(a.png)[0] + '.html' if a.png else os.path.join(ROOT, '.scratch', f'contact-{a.subject}.html'))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w') as fh:
        fh.write(page(cells))
    print(f'contact_sheet: {len(cells)} plates → {out}')
    if a.png and per_plate(len(cells), a.per_plate):
        with tempfile.TemporaryDirectory() as tmp:
            for i, (cell, png) in enumerate(zip(cells, named)):
                one = os.path.join(tmp, f'{i}.html')
                with open(one, 'w') as fh:
                    fh.write(page([cell]))
                w, h = shoot(one, png, 1, a.scale)
                print(f'contact_sheet: → {png} ({w} by {h} pixels)')
    elif a.png:
        w, h = shoot(out, a.png, len(cells), a.scale)
        print(f'contact_sheet: → {a.png} ({w} by {h} pixels)')


if __name__ == '__main__':
    main()
