# 008 — Content model and authoring: citation schema, palette-aware charts, a PDF source reader

## Goal

korg proposal 3417, second in the 2026-09-28 plan. It lands three decisions
from sprint 006 before the next subject (Feynman, 3397) is written, which
will lean on papers. Ken decided each one on 2026-09-28, and each decision
is a comment on its item:

- korg 3405: the citation schema gains a structured `doi`, kinds for
  proceedings/symposium papers and chapters and for reports, and
  approximate dates. **Sources are derived from citations**: a citation
  carries a key-source flag, and the frame's Sources list is built from the
  flagged ones. "Every frame carries sources" becomes "every frame flags at
  least one key-source citation", and validation enforces it.
- korg 3406: charts follow the reader's palette mode. Option (a): inline
  SVG through the allowlist sanitiser, using `currentColor` and the palette
  variables, which relaxes "charts are media files served with a no-script
  policy".
- korg 3404: a create-tool may depend on a non-stdlib package, pulled in by
  uv outside the app. Build `create-tools/read-source`.

The scope includes migrating both subjects (western-civ and ai, 89 frames
in all) and keeping the framework seed in step: `skills/grow/SKILL.md` and
the create-tools READMEs.

## Decisions

- **Premises held.** `CITATION_KINDS` had no chapter or report kind,
  `published` took `YYYY[-MM[-DD]]` only, and two media citations carried
  "c. 1951" and "c. 1840" in `container`. Every one of the 89 frames kept
  both lists by hand: 668 of its 671 sources matched a citation by URL.
  `create-tools/` had no PDF tool. Charts were `<img>`s of files with the
  frame's colours baked in: 12 charts, 11 in ai and 1 in western-civ. kloom
  is not in the cross-project plan index.

### Citations (3405)

- **`key: true` and `note`.** The flag is a boolean on the citation.
  `keySources()` in `engine/citation.ts` builds the Sources list from the
  key citations in the order they are written. Each entry is "Authors,
  Title", linked, with the container (or, for a book or report, the
  publisher) and the date. Wikipedia reads "Title — Wikipedia", as the
  curated frames always wrote it. A key citation may carry a `note`, a
  remark shown only in that list (a page, why it matters). About 380 of the
  old source notes were only where and when, which the entry now derives;
  17 said more, and became notes.
- **One list, enforced both ways.** Validation requires `citations` and at
  least one key. It also refuses a `sources` field outright, so a frame in
  the old form (a stale grow output, an unmerged branch) fails loudly
  instead of silently losing its list.
- **The Sources link is the URL that was read.** A Wikipedia source now
  links its pinned `oldid=` revision, not the live article. This follows
  from deriving it, and it is the more honest link.
- **More than three authors, or `etAl`, reads "First et al."** in the
  Sources list. The Chicago entry is unchanged: up to ten are listed.
- **`doi`** holds the bare DOI, and the entry links `https://doi.org/<doi>`
  in place of the url. A `url` becomes optional when there is a `doi`. A
  doi.org `url` is refused, so there is one way to write it. 67 citations
  moved.
- **`chapter`** covers a chapter in an edited volume or a paper in a
  proceedings or symposium volume: "In _Volume_, edited by …, pages. Place:
  Publisher, Year." It needs `container`, and takes `editors`. **`report`**
  covers technical, committee and institutional reports and lab system
  cards: title in italics, `number`, series, and "Place: Publisher, Date".
  36 citations became chapters (NeurIPS, ICLR, ICML, CVPR, ACL, ISCA, the
  Lighthill paper symposium) and 24 became reports (OpenAI's GPT papers,
  DeepSeek-V3, system cards, the Nobel scientific background, the
  International AI Safety Report, METR's risk report). Journals named
  "Proceedings of …" (the IEEE, the NAS, the London Mathematical Society)
  stay `article`.
- **`circa: true`** beside `published` renders "ca. 1951", in Chicago's
  abbreviation. The HUD's own position labels keep "c." because they are
  prose, not citations.
- **Ask.** With every source a citation, the prompt numbers the citations
  alone, and `AskContext.frame` no longer carries `sources`. A kept answer's
  `sources` stays in the format, always empty, so the answers already kept
  still read as version 1.
- **Repaired in the formatter:** a suffix written after the given names
  (`"given": "Mark U., Jr."`) now goes last in natural order ("Mark U.
  Edwards Jr."). It used to read "Mark U., Jr. Edwards", which the derived
  Sources list would have shown.

### Migration

`sprints/008-migrate.py` is kept with this record, not in the app. It
matches each source to its citation (a Wikipedia article by title, any
other page by URL), flags it and drops `sources`. Key citations move to the
front in the old Sources order, since the list is now derived in citation
order. It also moves doi.org URLs into `doi`, reclassifies chapters and
reports, and turns the two "c." containers into `circa`. Three sources
matched no citation. RoFormer was cited at its journal DOI and listed at
arXiv, so the citation is flagged. The Mark I Perceptron manual had only a
media credit, so it gained a `report` citation. Ken Alder's _The Measure of
All Things_ had no citation, so it gained a `book` citation at its Open
Library record. The derived lists were compared with the old ones word by
word (`.scratch`, not kept). Every difference left is presentation: "et
al." past three authors, dates in full, and an organisation named once when
it is also the site. A frame already in the new form is skipped, so the
script can run over the service's content clone (Deploy, below).

### Charts (3406)

- **Inlined through the sanitiser.** The loader inlines an `.svg` image in
  a reading, re-serialised by `sanitiseSvg`, in place of the `<img>`.
  Validation runs the same allowlist and reports `image "x.svg": …`. A
  raster image is unchanged.
- **Two options on `sanitiseSvg`.** `idPrefix` prefixes every id and every
  reference to one (`url(#…)`, `aria-labelledby`, `aria-describedby`), so
  two drawings inlined in one page cannot collide. The loader uses
  `<frame>-<file>-`. `decorative` makes the root `aria-hidden` and drops
  its role and labels.
- **Named by the alt text, as before.** The wrapper is
  `<span class="figure chart" role="img" aria-label="…">`, carrying the
  markdown alt text the `<img>` had. The SVG's own title and desc serve
  only someone opening the file alone.
- **Palette hooks.** `bar_chart.py` draws in `currentColor` with no
  background, and marks `class="muted"` (axis, sublabels) and
  `class="accent"` (the highlighted bar). The reading pane sets `color` to
  `--ink`, `--muted` and `--accent`. So a chart follows the palette mode and
  fades with the page. The spec's `colours` is gone.
- **Reproducible.** The old `bar_chart.py` reproduced all 12 committed
  charts byte for byte before the change. After it, all 12 were re-rendered
  from their specs. The bar-chart README now maps each spec to its chart.
- **Checked in Chromium 151** (Playwright against the dev server): the
  Dartmouth budget in Mixed (terminal, green on near-black) and Light
  (printout, dark on pale), AlexNet's ILSVRC chart in both, and the
  printing-press chart in Dark mode (formerly a parchment block on a dark
  page). The computed colours followed the mode each time, the chart
  filled the column (511px), and there were no console errors.

### read-source (3404)

- **pypdfium2 and Pillow**, declared as PEP 723 inline metadata and run
  with `uv run`. pypdfium2 does both the text and the rendering, under
  Apache-2.0/BSD. PyMuPDF would too, but it is AGPL. `pypdf` can't render.
  The machine still has no `pdftoppm`, and doesn't need one.
- **Text by default, pages on request.** It prints each page under
  `--- page N ---` and reports pages with under 20 characters of text as
  scans, naming them in the `--pages` form. `--png DIR` renders pages at
  144 dpi.
- **Tested:** the Attention paper by URL (text); McCulloch and Pitts 1943
  (an OCR'd scan: text, and page 2 rendered and read back as an image); a
  text-less PDF made from that image (both pages reported as scans); DTIC's
  403 and an HTML body saved as `.pdf` (both exit 1 with a message saying
  what to do).
- The create-tools convention now reads "standard library where possible;
  a package when a tool needs one", naming both routes (uv inline metadata
  for Python, `.scratch/tools` for npm).

## What shipped

- `engine/citation.ts`: the `chapter` and `report` kinds; `doi`, `key`,
  `note`, `editors`, `number` and `circa`; `citationHref`, `keySource` and
  `keySources`; and validation of each.
- `engine/validate.ts`: key sources required, `sources` refused, and an SVG
  image through the sanitiser. `engine/load.ts`: `Frame.sources` derived,
  and an SVG image inlined. `engine/svg.ts`: `idPrefix` and `decorative`.
  `engine/markdown.ts`: an inlined drawing in place of an `<img>`.
  `engine/ui/Narrative.svelte`: the chart palette hooks.
- `engine/ai/`: the prompt numbers the citations alone, and a kept answer's
  `sources` is empty.
- `create-tools/read-source/` (new), plus `bar_chart.py` and the 12 charts
  re-rendered in currentColor.
- Both subjects migrated: 89 `frame.json` files, 671 key citations.
- Docs: `docs/design.md` §Content model (Citations, Authoring tools), §Ask,
  §Illustration sanitiser, a new §Charts, and §Risks. Also
  `skills/grow/SKILL.md` (frame example, §Sources and citations, the
  checklist, §Authoring with tools), the create-tools and bar-chart READMEs,
  `CLAUDE.md`, and the roadmap.
- Tests: 357 (from 341). The gate was negative-tested on real content by
  unflagging a frame's keys, putting `style` in a chart, writing a doi.org
  url and a "c. 1951" date, and adding a `sources` list. Each was caught
  and named.

## Repaired in passing

- `.github/copilot-instructions.md` mirrors CLAUDE.md's Project section,
  and it had drifted since sprint 006. It was missing the 006 and 007
  status, the "every subject" test line and the reader-gate rule. It is a
  copy again, with this sprint's changes.
- The Chicago formatter's name-suffix order (above).

## Deploy

**The ship's deploy needs one step after it, in the service's content clone.**
`grow/kai` carries an unmerged grown frame, `faraday-induction` (commit
`6407ac8`), written in the old form. When the new app restarts,
`syncContent` rebases that commit onto the new main. The new validator then
refuses western-civ: the frame has `sources` and no key citation. The fix
is mechanical, and was tested on a copy of `grow/kai` overlaid on this
branch: `sprints/008-migrate.py` migrates that one frame, skips the other
23, and the result loads.

**Ken's call (2026-09-28): migrate the clone at deploy**, rather than hold
the ship for his review of the Faraday frame. Straight after `just deploy`,
from this checkout on merged main:

```sh
C=~/.local/share/kloom/content
git -C $C branch --show-current                  # grow/kai
python3 sprints/008-migrate.py $C/subjects       # "migrated 1 of …"
npx prettier --write $C/subjects/western-civ/frames/faraday-induction/frame.json
git -C $C commit -qam 'grow(western-civ): faraday-induction to key citations (sprint 008)'
git -C $C push -q origin grow/kai
systemctl --user restart kloom.service && just verify
```

The migration commit then rides along into Ken's eventual grow/kai PR.

## Deployed

- **2026-09-28, kai, `just deploy` from merged main `1d377c9`** (sprint-ship
  Phase 7). As predicted in §Deploy, the recipe's `just verify` failed
  after the restart: both doors returned 500 on read. `syncContent` had
  rebased the unmerged Faraday commit onto the new main as `ee62767`, and
  its old-form frame made western-civ invalid.
- **The content-clone step, as Ken chose:** `sprints/008-migrate.py` over
  the clone migrated 1 of 90 frames (`faraday-induction`), and Prettier
  left it unchanged. Committed `2b14f34` on `grow/kai` as `kloom grow` and
  pushed. Then the unit was restarted and `just verify` passed: both doors
  read, the tailnet door refuses an anonymous write, and the ssh door lets
  one through.
- **The sprint's own behaviour, live on :4891.** western-civ inlines 1
  chart and ai inlines 11, with no `<img>` of an SVG left. The Sources list
  links pinned `oldid=` revisions (derived from key citations). The
  migrated Faraday frame is served. `/media/ai/dartmouth/budget.svg` still
  serves the file (200). The service was down for about a minute, between
  the deploy's restart and the clone migration.
