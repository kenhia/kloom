# draw-plates

Scene illustrations as draw-on SVG: engineering plates with their geometry
showing, in the style docs/design.md §Illustrations describes.

- `plates.py`: the primitives. `D` is a drawing (default 400×300 viewBox,
  stroke 1.25). `group(kind)` starts a top-level group, and groups are drawn
  on in order. `kind` is `'thin'` (construction lines: 0.6 wide, 55%
  opacity), `'mid'` (secondary detail) or the default, the object at full
  weight. Then add paths with `line`, `lines` (many polylines as one
  stroke), `circle`, `ellipse`, `arc`, `curve` (raw path data) and `text` (a
  small monospace label that fades in). `wire` draws a convex solid's
  wireframe from its vertices, and `SOLIDS` holds the five Platonic solids.
  `D.svg()` returns the markup and `D.save(path)` writes it.
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

Start a `<subject>.py` beside `western_civ.py` that imports from `plates`.
Iterate on a contact sheet — screenshot every plate at once, in its
palette's colours — rather than one at a time in the app. Look for:

- a lone object with nothing to measure it against (clip-art)
- edges that coincide at an unlucky projection angle
- routes that wrap the long way around a globe

Then check the plates in the running app, where the scene sizes and staggers
them.
