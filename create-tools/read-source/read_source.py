# /// script
# requires-python = ">=3.11"
# dependencies = ["pypdfium2>=4.30", "pillow>=10"]
# ///
"""Read a primary source that is a PDF: print its text, or render pages to PNG.

    uv run create-tools/read-source/read_source.py SOURCE [--pages 1-3,7] [--png DIR] [--scale 2] [--crop L,T,R,B]

SOURCE is a path or an http(s) URL (fetched into memory, never kept).
Without --png it prints each page's text layer under a `--- page N ---`
marker, and says which pages have none: a scan, with no text layer to
extract. For those, --png DIR renders the chosen pages to
DIR/page-NNN.png, which a model that reads images can then read, and says
each page's size in pixels at that scale. `--crop L,T,R,B` writes only that
region of each page (DIR/page-NNN-crop.png), the box in the pixels of the
page rendered at the same --scale (sprint 050: in sprint 049 an author
measured a box on one render and cut it from another at a different scale).

The two packages (pypdfium2, Apache-2.0/BSD; Pillow) come from the inline
metadata above: `uv run` installs them into its own cache, outside the app
and never into package.json. See README.md.
"""
import argparse, io, os, sys, urllib.error, urllib.request

# pypdfium2 is imported where a PDF is read, so the argument helpers are tested without it.

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


def box_arg(text):
    """'L,T,R,B' → (left, top, right, bottom) in pixels, right of left and below top."""
    parts = [int(round(float(v))) for v in text.split(',')]
    if len(parts) != 4 or parts[2] <= parts[0] or parts[3] <= parts[1]:
        raise ValueError(f'a box is left,top,right,bottom with right > left and bottom > top: {text}')
    return tuple(parts)


def box_problem(box, size, scale):
    """Why `box` cannot be cut from a page `size` (width, height) pixels at `scale`, or None."""
    w, h = size
    if box[0] < 0 or box[1] < 0 or box[2] > w or box[3] > h:
        return (f'the box runs past the page, which is {w} by {h} pixels at --scale {scale:g}: '
                'measure the box on a page rendered at the same scale')
    return None


def load(source):
    """The document, or exit with what went wrong and what to do about it."""
    import pypdfium2 as pdfium
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
    ap.add_argument('--crop', metavar='L,T,R,B',
                    help='with --png: write only this region of each page, in the pixels of the page at --scale')
    args = ap.parse_args()
    try:
        box = box_arg(args.crop) if args.crop else None
    except ValueError as e:
        ap.error(str(e))
    if box and not args.png:
        ap.error('--crop writes a PNG: give --png DIR')

    pdf = load(args.source)
    chosen = pages(args.pages, len(pdf))
    if args.png:
        os.makedirs(args.png, exist_ok=True)
        for i in chosen:
            image = pdf[i].render(scale=args.scale).to_pil()
            if box:
                why = box_problem(box, image.size, args.scale)
                if why:
                    sys.exit(f'read_source: page {i + 1}: {why}')
                path = os.path.join(args.png, f'page-{i + 1:03d}-crop.png')
                image.crop(box).save(path)
                print(f'{path}  ({box[2] - box[0]} by {box[3] - box[1]} pixels, cut from {image.size[0]} by '
                      f'{image.size[1]} at --scale {args.scale:g})')
            else:
                path = os.path.join(args.png, f'page-{i + 1:03d}.png')
                image.save(path)
                print(f'{path}  ({image.size[0]} by {image.size[1]} pixels at --scale {args.scale:g})')
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
