# draw-plates

Scene illustrations as draw-on SVG: engineering plates with their geometry
showing, in the style docs/design.md §Illustrations describes.

- `plates.py`: the primitives. `D` is a drawing (default 400×300 viewBox,
  stroke 1.25). `group(kind)` starts a top-level group, and groups are drawn
  on in order. `kind` is `'thin'` (construction lines: 0.6 wide, 55%
  opacity), `'mid'` (secondary detail) or the default, the object at full
  weight. Then add paths with `line`, `lines` (many polylines as one
  stroke), `dashed` (a polyline as dashes, one path, for a hypothetical
  link or a projection; `dash` and `gap` in units, sprint 050), `circle`, `ellipse`, `arc`, `curve` (raw path data) and `text` (a
  small monospace label that fades in; write it as plain text, since `&`, `<`
  and `>` are escaped for you). `wire` draws a convex solid's
  wireframe from its vertices, and `SOLIDS` holds the five Platonic solids.
  `D.svg()` returns the markup and `D.save(path)` writes it.
- `plates_for.py <subject> <frame …>` (sprint 027): draws a subject's
  plates from its `<subject>_<part>.py` modules (a dash in the subject id
  is an underscore: `western_civ_`). Each module exports `PLATES = {frame:
function}`, where a function returns its `D`, so several authors can draw
  at once without sharing a file. It reads which module draws a frame
  without importing it and imports only the modules that draw the frames
  named, so another author's half-written module cannot stop yours; a
  module that fails to import is named and skipped, and the run exits 1.
  A bare run is refused: `--all` redraws every plate of the subject. It
  replaced seven identical `<subject>.py` collectors (ai, feynman,
  computing, physics, mathematics, chemistry, making).
- `contact_sheet.py` (sprint 014): every plate of a subject, or the frames
  named, on one page in its own palette with its title under it; `--png`
  screenshots the page with a headless Chromium (Playwright's, or
  `$CHROME`). `python3 create-tools/draw-plates/contact_sheet.py feynman --png .scratch/sheet.png`. `--scale 2.5`
  renders it large enough to read the labels (sprint 015). `--charts` adds
  each frame's other SVGs, its inlined charts, in the frame's palette;
  `--palette` names the palette for a plate whose `frame.json` is not
  written yet; and the page is written beside its PNG, so authors working
  at once don't overwrite one another's (sprint 021). Since sprint 027 a
  plate is shown at its own size (400 by 300), the PNG is as wide as its
  plates (one plate, 428 pixels at `--scale 1`; it was always four plates
  wide, 4,090 pixels at `--scale 2.5`), and `--palette FRAME=NAME`
  (repeatable) colours one frame, where a bare `--palette NAME` coloured
  every plate named. Above two plates, `--png FILE.png` writes one PNG
  per plate, `FILE-<frame>.png` (a chart's `FILE-<frame>-<chart>.png`),
  each one plate wide, beside the one page of them all (sprint 029: four
  plates at `--scale 2.5` made a PNG over 4,000 pixels wide that the image
  reader shrank past reading, and four of sprint 028's authors cropped by
  hand); `--per-plate` and `--one-sheet` ask for either at any count.
  It warns, on stderr, of text that runs off a plate's or a chart's edge
  and by about how far, estimated as `bar_chart.py` estimates a chart's
  (monospace at 0.6 em; a turned label is not estimated). Sprint 050 found
  two plates in the AI subject with a label off the edge that way.
  `test_contact_sheet.py` is its test.
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
Every other subject's plates are drawn with `plates_for.py`:

```sh
python3 create-tools/draw-plates/plates_for.py making knapping handaxe
python3 create-tools/draw-plates/plates_for.py making --all   # every author's
```

Standard library only. `test_plates_for.py` is its test (`just check`
runs every `test_*.py` under `create-tools/`).

## Drawing a new subject

Give each author a `<subject>_<part>.py` module that imports from
`plates` and exports `PLATES`, and draw with `plates_for.py <subject>
<frame …>`; there is no per-subject collector to write.
Iterate on a contact sheet (`contact_sheet.py`) rather than one plate at a
time in the app. Look for:

- a lone object with nothing to measure it against (clip-art)
- edges that coincide at an unlucky projection angle
- routes that wrap the long way around a globe

Then check the plates in the running app, where the scene sizes and staggers
them.
