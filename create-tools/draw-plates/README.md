# draw-plates

Scene illustrations as draw-on SVG: engineering plates with their geometry
showing, in the style docs/design.md §Illustrations describes.

- `plates.py`: the primitives. `D` is a drawing (default 400×300 viewBox,
  stroke 1.25). `group(kind)` starts a top-level group, and groups are drawn
  on in order. `kind` is `'thin'` (construction lines: 0.6 wide, 55%
  opacity), `'mid'` (secondary detail) or the default, the object at full
  weight. Then add paths with `line`, `lines` (many polylines as one
  stroke), `circle`, `ellipse`, `arc`, `curve` (raw path data) and `text` (a
  small monospace label that fades in; write it as plain text, since `&`, `<`
  and `>` are escaped for you). `wire` draws a convex solid's
  wireframe from its vertices, and `SOLIDS` holds the five Platonic solids.
  `D.svg()` returns the markup and `D.save(path)` writes it.
- `ai.py` and `ai_<part>.py` (sprint 006): the ai subject's plates. Each
  `ai_<part>.py` exports `PLATES = {frame: function}`, where a function
  returns its `D`. `ai.py` collects them and saves each one, so several
  authors can draw at once without sharing a file.
- `feynman.py` and `feynman_<part>.py` (sprint 014): the feynman subject's
  plates, collected the same way.
- `computing.py` and `computing_<part>.py` (sprint 015): the computing
  subject's plates, collected the same way.
- `contact_sheet.py` (sprint 014): every plate of a subject, or the frames
  named, on one page in its own palette with its title under it; `--png`
  screenshots the page with a headless Chromium (Playwright's, or
  `$CHROME`). `python3 create-tools/draw-plates/contact_sheet.py feynman --png .scratch/sheet.png`. `--scale 2.5`
  renders it large enough to read the labels (sprint 015).
- `western_civ.py`: the 17 western-civ plates, one function per frame. It
  is the worked example: the Pantheon section, the globe with its route,
  the helix and the honeycomb show how the geometry is computed rather than
  placed by hand.

## Usage

```sh
python3 create-tools/draw-plates/western_civ.py              # redraw every frame
python3 create-tools/draw-plates/western_civ.py pantheon dna # just these
```

Each plate is written to `subjects/western-civ/frames/<frame>/scene.svg`.
Standard library only.

## Drawing a new subject

Start a `<subject>.py` collector beside `ai.py` and `feynman.py`, with a
`<subject>_<part>.py` module per author that imports from `plates`.
Iterate on a contact sheet (`contact_sheet.py`) rather than one plate at a
time in the app. Look for:

- a lone object with nothing to measure it against (clip-art)
- edges that coincide at an unlucky projection angle
- routes that wrap the long way around a globe

Then check the plates in the running app, where the scene sizes and staggers
them.
