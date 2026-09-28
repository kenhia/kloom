# create-tools

Tools for authoring a kloom subject: the scripts that made the western-civ
frames, kept so their output can be regenerated, changed and imitated. The
skills and instructions for creating a new subject, and for grow, point
here.

| Tool                            | What it makes                                                                                |
| ------------------------------- | -------------------------------------------------------------------------------------------- |
| [draw-plates](draw-plates/)     | Scene illustrations: engineering-plate line drawings as draw-on SVG, from computed geometry. |
| [wiki-cite](wiki-cite/)         | `wikipedia` citations for a frame, pinned to each article's current revision (`oldid=`).     |
| [bar-chart](bar-chart/)         | A reading-pane bar chart: an SVG inlined into the reading, in the reader's palette.          |
| [trace-art](trace-art/)         | A traced line engraving as banded draw-on SVG (the start screen's loom).                     |
| [commons-media](commons-media/) | A freely licensed image from Wikimedia Commons, with its `media` citation.                   |
| [subject-plan](subject-plan/)   | `spine.json` and trails from a plan, holding only the frames written so far.                 |
| [read-source](read-source/)     | A PDF source's text, or its scanned pages as PNG, to read before citing it.                  |

## Conventions

- **One directory per tool**, with a `README.md` giving its usage, inputs
  and outputs, and an `examples/` directory when it reads a spec.
- **Python standard library where possible; a package when a tool needs
  one.** Ken decided in sprint 008 (korg 3404) that a create-tool may depend
  on a package outside the standard library, as long as it is installed
  outside the app and never into `package.json`. For Python, declare it as
  inline script metadata (PEP 723) and run the tool with `uv run`, which
  installs into uv's own cache. `read-source` does this (pypdfium2,
  Pillow). An npm package goes into the git-ignored `.scratch/tools` prefix,
  as `trace-art` does with `potrace`. Name the dependency in the tool's
  README.
- **Output is content; the tool is not the source of truth.** What a tool
  writes is committed and may be edited by hand afterwards. Re-running a tool
  over a hand-edited file replaces it, so check `git diff` before you commit.
- **Reproducible.** Running a tool on the committed inputs reproduces the
  committed output byte for byte (sprint 002 checked all four this way).
  Keep it so when you change a tool, or say in the commit why the output
  changed.
- Output still has to pass `just check`: illustrations and charts the
  sanitiser (a chart is inlined too), illustrations `pathLength="1"`, and
  media a `media` citation with a licence (docs/design.md §Citations,
  §Charts, §Illustrations).

## Adding a tool

An agent creating a new subject may add a tool here when the subject needs
something these don't do (a timeline strip, a map projection, a family
tree). Put general primitives in the tool and subject-specific use in a
separate file, as `draw-plates` does with `plates.py` and `western_civ.py`,
and add a row to the table above.

Grow jobs do not run or add tools (decided in sprint 005, korg 3364). A
grow job has no shell, because running model-written code on the host is
not something a reader's request should be able to cause. Grow reads these
READMEs and `plates.py` as references and computes its geometry itself.
