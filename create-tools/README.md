# create-tools

Tools for authoring a kloom subject: the scripts that made the western-civ
frames, kept so their output can be regenerated, changed and imitated. The
skills and instructions for creating a new subject, and for grow, point
here.

| Tool                        | What it makes                                                                                |
| --------------------------- | -------------------------------------------------------------------------------------------- |
| [draw-plates](draw-plates/) | Scene illustrations: engineering-plate line drawings as draw-on SVG, from computed geometry. |
| [wiki-cite](wiki-cite/)     | `wikipedia` citations for a frame, pinned to each article's current revision (`oldid=`).     |
| [bar-chart](bar-chart/)     | A reading-pane bar chart: a standalone, accessible SVG in the frame's colours.               |
| [trace-art](trace-art/)     | A traced line engraving as banded draw-on SVG (the start screen's loom).                     |

## Conventions

- **One directory per tool**, with a `README.md` giving its usage, inputs
  and outputs, and an `examples/` directory when it reads a spec.
- **Python standard library where possible.** A tool that needs more says
  so in its README and installs it outside the app: into the git-ignored
  `.scratch/tools` prefix, never `package.json`. `trace-art` is the one
  exception so far (Pillow and the npm `potrace` port).
- **Output is content; the tool is not the source of truth.** What a tool
  writes is committed and may be edited by hand afterwards. Re-running a tool
  over a hand-edited file replaces it, so check `git diff` before you commit.
- **Reproducible.** Running a tool on the committed inputs reproduces the
  committed output byte for byte (sprint 002 checked all four this way).
  Keep it so when you change a tool, or say in the commit why the output
  changed.
- Output still has to pass `just check`: illustrations the tripwire and
  `pathLength="1"`, media a `media` citation with a licence
  (docs/design.md §Citations, §Illustrations).

## Adding a tool

An agent creating a new subject may add a tool here when the subject needs
something these don't do (a timeline strip, a map projection, a family
tree). Put general primitives in the tool and subject-specific use in a
separate file, as `draw-plates` does with `plates.py` and `western_civ.py`,
and add a row to the table above.

Whether grow jobs may add or run tools is not decided. It would mean running
model-written code on the host, so it belongs to grow's design (korg 3364)
and its sanitiser (3365).
