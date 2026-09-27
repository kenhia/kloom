# trace-art

Turns a line engraving (a PNG) into draw-on SVG. This is how the start
screen's loom (`src/lib/start/loom.svg`) was made.

```sh
npm install --prefix .scratch/tools potrace   # once; git-ignored, not an app dependency
python3 create-tools/trace-art/trace.py loom.png src/lib/start/loom.svg
```

1. The image is flattened onto white as greyscale. This step needs Pillow.
2. It is traced with the npm `potrace` port (`potrace.mjs`). The options
   are `--threshold 150 --turdsize 6 --opttolerance 0.6`; lower the
   tolerance for smoother curves, at the cost of a larger file.
3. The contours are sorted by their left edge and split into `--bands 8`
   groups. Each group is one `<path pathLength="1">`, so the drawing sweeps
   on from left to right. Coordinates are rounded to 0.1.

Stroke the result; don't fill it. Potrace writes each line as a pair of
contours, which is the double-line wireframe look, and a hole is its own
subpath, so filling would close it solid. Expect roughly 200 KB for a
detailed 663×500 engraving. Load it lazily rather than inlining it in the
server-rendered page.

Check the source's licence before you trace it, and credit it with a `media`
citation. `src/lib/start/README.md` is the model.
