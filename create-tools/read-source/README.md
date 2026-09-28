# read-source

Reads a primary source that is a PDF, so you can check a claim against the
paper itself before you cite it. It prints the text layer, and renders pages
to PNG when a page is a scan with no text layer. Many of the papers a
subject leans on are scans: McCulloch and Pitts 1943, Shannon 1938, the
Lighthill report, the Mark I Perceptron manual.

```sh
uv run create-tools/read-source/read_source.py paper.pdf                  # every page's text
uv run create-tools/read-source/read_source.py https://arxiv.org/pdf/1706.03762 --pages 1-3
uv run create-tools/read-source/read_source.py scan.pdf --pages 2-4 --png .scratch/pages
```

- **Text.** Each page prints under `--- page N ---`. A page with less than
  20 characters in its text layer is reported as a scan. The summary on
  stderr names the scanned pages in the form `--pages` takes.
- **Scans.** `--png DIR` writes `DIR/page-NNN.png` (144 dpi; `--scale 1`
  for 72, `3` for 216). Read those images; put them in `.scratch/`, which is
  git-ignored, not in a frame.
- **URLs** are fetched into memory, never saved. Some archives refuse a
  script: DTIC answers 403. Download the file in a browser and pass the path.

## Dependencies

It needs two packages outside the standard library: `pypdfium2` (PDFium's
Python binding, Apache-2.0/BSD) for the text and the rendering, and Pillow to
write the PNGs. They are declared as inline script metadata (PEP 723) at the
top of `read_source.py`, so `uv run` installs them into uv's own cache. They
never touch `package.json` or the app. The machine has no `pdftoppm`, and
this doesn't need one.

## Not for grow

A grow job has no shell (sprint 005), so it can't run this or any tool. It
reads sources with WebFetch, when the job allows the web. This tool is for a
tooled author: an agent writing a subject in a session, or a person.
