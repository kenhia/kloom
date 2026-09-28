# /// script
# requires-python = ">=3.11"
# dependencies = ["pypdfium2>=4.30", "pillow>=10"]
# ///
"""Read a primary source that is a PDF: print its text, or render pages to PNG.

    uv run create-tools/read-source/read_source.py SOURCE [--pages 1-3,7] [--png DIR] [--scale 2]

SOURCE is a path or an http(s) URL (fetched into memory, never kept).
Without --png it prints each page's text layer under a `--- page N ---`
marker, and says which pages have none: a scan, with no text layer to
extract. For those, --png DIR renders the chosen pages to
DIR/page-NNN.png, which a model that reads images can then read.

The two packages (pypdfium2, Apache-2.0/BSD; Pillow) come from the inline
metadata above: `uv run` installs them into its own cache, outside the app
and never into package.json. See README.md.
"""
import argparse, io, os, sys, urllib.error, urllib.request

import pypdfium2 as pdfium

# A page with fewer characters than this in its text layer is treated as a scan.
MIN_TEXT = 20


def pages(spec, count):
    """'1-3,7' → [0, 1, 2, 6]: one-based and inclusive, clipped to the document."""
    if not spec:
        return list(range(count))
    out = []
    for part in spec.split(','):
        a, _, b = part.strip().partition('-')
        lo, hi = int(a), int(b or a)
        out.extend(n - 1 for n in range(lo, hi + 1) if 1 <= n <= count)
    return out


def ranges(numbers):
    """[1, 2, 3, 7] → '1-3,7', the form --pages takes."""
    out, start = [], None
    for i, n in enumerate(numbers):
        if start is None:
            start = n
        if i + 1 == len(numbers) or numbers[i + 1] != n + 1:
            out.append(str(start) if start == n else f'{start}-{n}')
            start = None
    return ','.join(out)


def load(source):
    """The document, or exit with what went wrong and what to do about it."""
    try:
        if source.startswith(('http://', 'https://')):
            req = urllib.request.Request(source, headers={'User-Agent': 'kloom read-source'})
            with urllib.request.urlopen(req, timeout=60) as r:
                return pdfium.PdfDocument(io.BytesIO(r.read()))
        return pdfium.PdfDocument(source)
    except urllib.error.URLError as e:
        # Some archives (DTIC among them) refuse anything but a browser.
        sys.exit(f'{source}: could not fetch it ({getattr(e, "code", None) or e.reason}). '
                 'Download it in a browser and pass the file.')
    except pdfium.PdfiumError as e:
        sys.exit(f'{source}: not a PDF pdfium can open ({e}). A URL may have served a web page.')


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('source', help='a PDF: a path or an http(s) URL')
    ap.add_argument('--pages', help='one-based pages, e.g. 1-3,7 (default: all)')
    ap.add_argument('--png', metavar='DIR', help='render the pages to DIR/page-NNN.png instead')
    ap.add_argument('--scale', type=float, default=2.0,
                    help='render scale; 1 is 72 dpi, the default 2 is 144 dpi')
    args = ap.parse_args()

    pdf = load(args.source)
    chosen = pages(args.pages, len(pdf))
    if args.png:
        os.makedirs(args.png, exist_ok=True)
        for i in chosen:
            path = os.path.join(args.png, f'page-{i + 1:03d}.png')
            pdf[i].render(scale=args.scale).to_pil().save(path)
            print(path)
        return

    scans = []
    for i in chosen:
        text = pdf[i].get_textpage().get_text_range().replace('\r\n', '\n').strip()
        print(f'--- page {i + 1} ---')
        if len(text) < MIN_TEXT:
            scans.append(i + 1)
            print('(no text layer: a scan; render it with --png)')
        else:
            print(text)
    print(f'\n{len(chosen)} of {len(pdf)} pages read.', file=sys.stderr)
    if scans:
        print(f'{len(scans)} with no text layer ({ranges(scans)}): '
              f'read them as images with --png DIR --pages {ranges(scans)}.', file=sys.stderr)


if __name__ == '__main__':
    main()
