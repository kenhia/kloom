# 050 — Author-subject tuned a fourth time, "per cent", and the contents in view

## Goal

korg proposal 3556, three small items that share no code, run ahead of
the three subject sprints (3547 Daily Bread, 3548 The Story of Life, 3549
Sound and Score) so their authors get the tools and the gate:

- korg 3554: the tool changes sprint 049's seventeen authors asked for
  (`sprints/049-western-civ-full-weight.md` §What the tools and skills
  assumed); the proposal settled "build every candidate";
- korg 3553: the spelling gate respelled word by word, so the two-word
  British "per cent" passed it in nine subjects;
- korg 3552: the table of contents clipped at the window's left edge on
  kbook2's smaller screen.

## Decisions

- **Premises held** (checked at start): "per cent" was still in every
  subject but western-civ, and more than the work item counted (about 376
  hits, with two `PER CENT` chart headings); `american.py`'s tokenizer was
  `[A-Za-z]+`; the 049 record listed every 3554 candidate. kloom is not in
  the cross-project plan index. No grow branch was pending.

### "per cent" (korg 3553)

- `american.py` gained `PHRASES`, a British spelling written as two words,
  matched case-insensitively and across a wrapped line, never inside a
  longer word: `per cent` → `percent`, and "per century" and "percent"
  left alone. A phrase goes through the same protection as a word
  (quotations, titles, names; a capitalized "Per Cent" mid-sentence is a
  name). The first pattern also matched "percent" itself, a no-op hit
  that would have kept `check` failing forever; a test now holds that
  an American spelling is no hit at all.
- **One sweep**: 356 respelled in 160 files (readings, names'
  descriptions, the chemistry and physics chart headings), 170 kept as
  quoted, a title or a name. One italic caption in `race-serology` ("in
  per cent", read as a title by the italic-with-a-capital rule) was
  respelled by hand. Joining wrapped "per\ncent" changed eleven readings'
  line lengths; Prettier rewrapped them. No `edits` entry: spelling is not
  a revision.

### The tools (korg 3554)

- **Accent claims enforced.** `subject_plan.py --check --accents FILE`
  reads `ACCENT part frame` lines and exits 1 on a word another claim, a
  written frame or the plan already holds, naming both and the line. A
  plan's frame entry may carry `accent`, which the lead settles and which
  wins over any claim. The first claim wins, and a frame's later claim
  releases its earlier one, so an author who changes their mind frees
  the word rather than holding two.
- **`--complete` counts the copy.** "the copy at DIR/<subject> holds N of
  M planned frames": the old line counted every frame in the copy,
  including ones it then left out, and three authors read it as theirs.
- **`names.py drafts`** refuses a draft no spec marks once its part's
  spec (`examples/<subject>-<part>.json`) exists, and notes it before
  then, so a part still writing is not failed. **`lookup --write-draft
DIR`** writes each found title's draft with its id, Wikidata item and
  name, and `kind` and `description` empty, so `add` refuses it until the
  author writes them; a missing, ambiguous or warned-of title is not
  written, nor one already there.
- **`commons_media`**, checked live against every Commons citation in
  western-civ: a group, a trust or partners are organisations ("Classical
  Numismatic Group" was split into family and given); a catalog's
  "Family, Given (dates). Role" is a person with the role dropped (the
  BnF's "Auteur du texte"); a title loses a Wikidata label's text (`label
QS:Les,…`, a variant the old pattern missed), a DPLA identifier and an
  `LCCN` number; and a DPLA upload (a `{{DPLA metadata}}` page, whose
  Artist is an agency's path and a date) gets the last unit as author,
  and, when its credit line says NARA, NARA as container and its NAID.
  A period after a lone initial ("U.S. Senate") does not end a unit.
- **`contact_sheet`** warns of text that runs off a plate's or a chart's
  edge, by about how far, estimated as `bar_chart.py` does (monospace at
  0.6 em; a turned label is skipped). Across ~600 plates it found four:
  two real (below), two within a unit, and the threshold is one unit so
  neither prints. **`plates.py`** gains `dashed()`, a polyline as dashes
  in one path, so it draws on as one stroke, a dash carried round a
  corner.
- **`read_source`**: `--png` says each page's size in pixels at its
  `--scale`, and `--crop L,T,R,B` writes that region, the box in those
  pixels, refusing one past the page with the page's size and scale. Its
  pdfium import moved into `load`, so `tools-test`'s plain python3 tests
  the argument helpers (a first `test_read_source.py`).
- **Citation kinds.** A statute that is not a US one says how it is
  cited in `citeAs`: `regnal` ("Bill of Rights [1688], 1 Will. & Mar.
  Sess. 2, c. 2", where the workaround rendered "… Sess. 2 ch. 2") or
  `gazette` ("…, Reichsgesetzblatt 1935, Teil I, p. 1146", where it
  rendered "Teil I 1146"); neither takes a `publicLaw`. A `treaty` kind:
  its name, `parties` joined by an en dash, left out for a treaty among
  many states as legal form leaves them out, the date signed (required)
  and a treaty series in `code` when there is one. **content.db's shape
  is untouched**: citations live in the frame's JSON body, which the
  proposal named as the condition for landing this rather than raising
  it. Migrated: the four statutes in `glorious-revolution` and
  `holocaust`, and six treaties cited as `web` pages (Westphalia,
  Versailles twice, the 1939 secret protocol, Geneva 1864, Hague X).
  The Berlin General Act (an `article` in the journal that printed it)
  and Geneva II (a `chapter` in a volume) cite a printing with its pages
  and stay. A change of form, not of source, so no `edits` entries.

### The contents in view (korg 3552)

- **Reproduced first**, on kai with a headless-browser probe
  (`.scratch/050/probe.mjs`): in `blood/hepatitis` the contents panel's
  left edge sat at −35 to −146 px at every width from 700 to 1280. The
  HUD is at the spine pane's right, 300 to 415 px from the window's left,
  and the panel, 26rem wide, hangs from its button's right edge. The
  bookmarks clipped at 800. The zoom icon was one more push left, not
  the cause, as Ken suspected; cleo's wider window hid it.
- **The fix is a rule, not a nudge**: `use:inView`
  (`engine/ui/inView.ts`, with the arithmetic in `engine/in-view.ts`,
  unit-tested) moves a shown panel sideways just enough to stay in the
  window, as its `hidden` flips or it or the window resizes, before
  paint. On both HUD pop-ups. A fixed-position phone sheet is left
  alone.
- **The guard** the proposal asked for: `just hud-check` opens both
  panels at seven widths from 700 to 1920 and fails one outside the
  window; design.md §Contents says a new HUD pop-up takes the action and
  a line in that check.

## Verification

- `just check` green: svelte-check with no warnings, Prettier, eslint,
  1,530 vitest tests, `just tools-test` (ten tools' suites), `just
reader-gate`, every mark spec `--check --placed`, and the spelling check
  (0 to change, 170 kept).
- `just hud-check`: 145/145. `just scene-fit`: 0 misfits in 663 frames at
  1280×800, 1400×900 and 390×844.
- **Negative tests, each seen failing:** a planted "per cent" in a
  reading fails `american.py check`; the in-view check with `use:inView`
  taken off the contents fails five widths (−146 to 304 at 900); every
  new tool test was written and run red before its code.
- `read_source` run on a real PDF: page size reported, a crop written, a
  box past the page refused. `commons_media`'s parsing re-run against
  western-civ's live Commons metadata.
- The two redrawn AI plates looked at on a contact sheet.

## Repaired in passing

- **Two AI plates had a label off the edge**, found by the new
  `contact_sheet` check: `hopfield-network`'s whole energy axis and its
  "E" were drawn at x −13 to −19, invisible, and `deep-belief-nets`'s "28
  × 28 PIXELS" ran 34 units past the right edge. The axis now stands just
  inside the plate's left edge beside the back corner, as drawn to be,
  and the image's label ends at the right edge (`ai_neural.py`).

## Follow-ups

- None filed. The italic-caption heuristic in `american.py` (a capital in
  an italic span reads as a title) met one caption; a caption convention
  is a design question only if it recurs.

## Deployed

2026-10-04, to the service on kai, by `just deploy` (`.sprint-deploy`'s
`recipe: deploy`) from merged `main` at `ca7ac02b` (PR #57). The recipe's
own checks passed: both doors read, the tailnet door refuses an anonymous
write and keeps reader data and notes from an anonymous read, the ssh
door reads and writes, a frame's body comes from the library, pages go
compressed; library `ff6ee8`, content `ca7ac02b`.

Verified live at `https://kai.encke-wahoo.ts.net:4890`: `westphalia`'s
key source renders as a treaty ("…, Holy Roman Empire–France, October 24,
1648"); `haber-bosch`'s chart heading reads PERCENT; and the contents
panel in `blood/hepatitis` opens inside the window at every width from
700 to 1280 (left edge 8 to 89 px, where it was −35 to −146). `just
hud-check` is a dev-server check: on the live tailnet door a headless
browser has no reader, so it has no bookmarks button and stops there.

Not published to the public reader site: `just publish-public` is a
separate step.
