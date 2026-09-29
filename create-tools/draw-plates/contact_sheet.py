"""A contact sheet of a subject's plates, each in its own palette (sprint 014).

    python3 create-tools/draw-plates/contact_sheet.py SUBJECT [frame ...] [--out FILE] [--png FILE] [--scale N]

Writes an HTML page (default `.scratch/contact-<subject>.html`) showing each
frame's scene.svg in its palette's background, line and accent colours, with
its headline and accent word under it. With `--png`, a headless Chromium
screenshots the page: the one Playwright installed under
~/.cache/ms-playwright, or `$CHROME`. `--scale 2.5` renders the PNG at that
many device pixels per CSS pixel, to read a plate's labels (sprint 015). Standard library only.
"""
import argparse, glob, html, json, os, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')


def chrome():
    if os.environ.get('CHROME'):
        return os.environ['CHROME']
    found = sorted(glob.glob(os.path.expanduser('~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell')))
    if not found:
        sys.exit('contact_sheet: no headless Chromium found; set $CHROME')
    return found[-1]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('subject')
    ap.add_argument('frames', nargs='*')
    ap.add_argument('--out')
    ap.add_argument('--png')
    ap.add_argument('--scale', type=float, default=1, help='device pixels per CSS pixel in the PNG')
    a = ap.parse_args()
    sdir = os.path.join(ROOT, 'subjects', a.subject)
    palettes = json.load(open(os.path.join(sdir, 'subject.json')))['palettes']
    frames = a.frames or sorted(os.listdir(os.path.join(sdir, 'frames')))
    cells = []
    for fid in frames:
        fdir = os.path.join(sdir, 'frames', fid)
        try:
            if os.path.exists(os.path.join(fdir, 'frame.json')):
                s = json.load(open(os.path.join(fdir, 'frame.json')))['scene']
            else:  # a frame still being written: its plate, in the first palette, untitled
                s = {'illustration': 'scene.svg', 'palette': next(iter(palettes)), 'headline': '(no frame.json yet)', 'accent': ''}
            svg = open(os.path.join(fdir, s['illustration'])).read()
        except (OSError, KeyError, ValueError) as e:
            print(f'contact_sheet: skipping {fid}: {e}', file=sys.stderr)
            continue
        p = palettes[s['palette']]
        cells.append(
            f'<figure style="background:{p["background"]};color:{p["line"]}">{svg}'
            f'<figcaption style="color:{p["ink"]}">{html.escape(s["headline"])} '
            f'<b style="color:{p["accent"]}">{html.escape(s["accent"])}</b>'
            f'<small style="color:{p["muted"]}">{html.escape(fid)} · {html.escape(s["palette"])}</small></figcaption></figure>')
    page = ('<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#888;display:grid;'
            'grid-template-columns:repeat(4,400px);gap:6px;padding:6px;font:13px system-ui}'
            'figure{margin:0;padding:8px}svg{width:384px;height:288px;display:block}'
            'figcaption b{font-weight:800}small{display:block;margin-top:2px}</style>' + ''.join(cells))
    out = a.out or os.path.join(ROOT, '.scratch', f'contact-{a.subject}.html')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w') as fh:
        fh.write(page)
    print(f'contact_sheet: {len(cells)} plates → {out}')
    if a.png:
        rows = (len(cells) + 3) // 4
        subprocess.run([chrome(), '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                        f'--window-size=1636,{rows * 352 + 12}', f'--force-device-scale-factor={a.scale:g}', f'--screenshot={os.path.abspath(a.png)}',
                        'file://' + os.path.abspath(out)], check=True, capture_output=True)
        print(f'contact_sheet: → {a.png}')


if __name__ == '__main__':
    main()
