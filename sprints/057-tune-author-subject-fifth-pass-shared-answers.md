# 057 — Author-subject tuned a fifth time, and shared answers

## Goal

korg proposal 4427, a slice of the November backlog drawdown (program
4368). It holds two items, and Ken approved every recommended default on
2026-11-09:

- korg 3576, with 3557 folded in: the authoring-tool decisions from The
  Story of Life (sprint 055) and Daily Bread (sprint 051). It runs before
  the next subject (Sound and Score, korg 3549) so that run meets fixed
  tools;
- korg 3560: a reader may share a kept answer with other readers. Ken's
  answer to the item's question is that it becomes public only after an
  agent reviews it, on the path notes and annotations already take.

It ran as an overseen karc leg on kai. The tool work went to two parallel
agents with separate files: citations, names and the skills to one;
commons_media, bar_chart and the plates to the other. The lead built the
shared answers.

## Decisions

- **Premises held**, checked at the start. Nothing enforced the 15-mark
  cap: it lived only in the grow skill's prose. `accessed` was already the
  UTC date (3557 #3), so nothing was needed. `names.py lookup --expect` read
  only the description and first line. bar_chart had no `series`. kloom is
  not in the cross-project plan index, and no grow branch was pending.
- **The brief was partly wrong in one place.** "Two authors embedded
  Natural Earth data" (3576 #7) was one: `biology_time3.py`. germ1's
  embedded data is Snow's Broad Street map, and beagle1 drew its coasts by
  hand. The shared module was built anyway, around time3's data.

### Shared answers (korg 3560)

- **On the notes' path, not a new one.** A box, **Share with other
  readers**, sits under each answer in a frame's Q&A. Ticking it asks for a
  review (`PATCH /api/reader/kept`), and the answer says it is waiting. The
  review-notes skill lists waiting shares (`review-notes.mjs shares`) and
  passes or declines each with a response the reader sees
  (`review-share`). On the public site this goes through `admin.mjs shares`
  and `review-shares` over `fly ssh`, as `handle-notes` does. A review is
  refused for a share no longer waiting, or one asked again since it was
  listed (the `asked` time, given back as `--seen`), so a review never lands
  on a request it did not read.
- **Readers' Q&A.** A frame with shared answers gets a second closed
  section after the reader's own Q&A, labelled with the count. The page
  load brings counts of other readers' shares only. The answers are fetched
  from `GET /api/reader/shared` when the section opens, and render as kept
  answers do (`engine/ui/QaAnswer.svelte`, now shared by both sections).
  Both editions have it for every reader: reading a shared answer needs no
  ask, while sharing one needs the kept answer and so ask.
- **No name.** The route returns the kept-answer format, which holds no
  reader. The skill's review checks that the question is fit for a
  stranger to read. Crediting the reader by display name was not asked
  for, and was left out as the conservative reading.
- **Unticking takes it back at once**, with no review, and so does
  removing the answer. Ticking a declined answer again asks afresh and
  clears the old response.
- **In the store**, a new table rather than columns on `kept`: migration
  11, `kept_share` (state `none`, `pending`, `shared` or `declined`, the
  response, and when it was asked and reviewed). The export leaves it out,
  because it is site state, so an import can never make an answer public.
  Deleting a reader removes their shares. The migration tests that rewind a
  file to an older schema now drop the new table too.
- **Not done**: no "unseen" count for a reviewed share, as notes have in My
  notes. The outcome shows under the answer in the frame's Q&A. If readers
  miss it, that is a follow-up.

### The tools (korg 3576, 3557)

Citations and names, the first agent:

- **Citation kinds.** A `letter` may leave out `recipients` and reads
  "Letter, December 26, 1823."; an empty list is still refused. A new
  `lecture` kind takes a required `occasion` ("Nobel Lecture") and an
  optional `place`. A modern UK act is `citeAs: "year"` with a `chapter`:
  "Human Reproductive Cloning Act 2001, c. 23". The doubled year came from
  `regnal` printing its `code` verbatim, and a four-digit year in a regnal
  `code` is now refused. DataCite DOIs were never refused, so they got a
  test and a line in the skill. **Migrated** (a change of form, not of
  source, so no `edits`, as in sprint 050): 50 Nobel lectures cited as
  `web` across seven subjects, `dolly`'s act, `mary-anning`'s invented
  recipient, and two DOIs added in `biodiversity-now`, both checked live.
- **`names.py lookup`** warns, and exits 1, on a slug that collides with
  a registry id held by another Wikidata item, or with another title in the
  same call. `--write-draft` will not write one; the author gives
  `"Title#id"`. **`--expect`** (lookup and `wiki_cite.py`, shared in
  `create-tools/lib/`) reads the whole intro and reports a redirect and its
  target.
- **`mark --skip-missing`** places the rest of a checking copy's frame and
  names what it skipped. It is refused on the live `subjects/` and with
  `--placed`. A mark landing inside a longer proper name ("East India
  Company" in "Dutch East India Company") is a warning, never a refusal.
- **The 15-mark cap is enforced**: `mark` and `mark --check` fail a frame
  over 15 marks unless its spec's `markCapOverrides` gives a reason. Twelve
  published frames were over the cap (five in ai, six in biology, and
  western-civ's `aquinas`), and each got an override whose reason comes from
  its marks.
- **Rights** (Ken's conservative rule) went into the grow skill and
  `reaching-sources.md`. A work first published after its author's death
  is not public domain until both terms have run. A press photograph
  distributed without a notice needs its basis recorded in the media
  citation. No published frame breaks either rule: `notebook-b` describes
  Darwin's tree rather than showing it. **Laboratory frames**: the
  author-subject brief asks for a method as historical narrative, never a
  protocol or a methods table.

Media, charts and plates, the second agent:

- **`commons_media`.** When a page carries both a public-domain tag and a
  Creative Commons licence (`{{Art Photo}}`, `Licensed-PD-Art`, `{{self}}`
  beside `PD-old`, a source's CC BY beside Commons' PD), fetch writes the
  CC licence, credits the photographer where the page names one, and warns,
  naming both. One consequence: BHL's Flickr scans now come out CC BY 2.0.
  It also warns, and never refuses, on:
  - several people written as one name;
  - a file's name used as a title;
  - a book's author credited for a plate;
  - an engraving firm;
  - a catalog heading;
  - a collection written as the author.

  A KB is 1,000 bytes. A Library of Congress reader gives the division as
  container and the LCCN as number, with no author when the Artist field is
  a collection. A `--width` wider than the original is refused, and the
  error names the original's width. Fetching outside a frame's directory
  warns that `file` names the copy. Nine real Commons pages are fixtures;
  no test reaches the network.

- **`bar_chart.py`**: `series` (2 to 4, grouped, with a legend in the
  heading's line, told apart by ink, accent, muted and outline, so they
  follow the palette) and signed bars (an axis `min` below zero, a true
  minus sign). A Wikipedia `url` without `oldid=` is warned of. Value
  labels keep the data's own decimals. That redrew two published charts,
  western-civ's `book-output` (217M → 217.4M) and `aircraft` (112 → 112.1).
  Their alt text and tables keep the rounded prose; it is precision, not a
  changed fact, so there are no `edits`. Every other example renders byte
  for byte as before.
- **`plates.py`**: `arc()` is documented as taking degrees. `clip`,
  `hatch`, `clip_polygon` and `inside` work on any polygon. A new
  `coastlines.py` and `coastlines.json` hold time3's Natural Earth data as
  region `wallacea`, and `add NAME --box=…` cuts a new region. `darwin-wallace`
  redraws byte-identical. Hidden-line wireframes were skipped, as decided.
- **`contact_sheet.py`** warns of labels overlapping inside a plate, past
  one unit each way. It flags none of the 966 committed SVGs, and two real
  collisions among about 1,056 drafts in `.scratch`.

## Verification

- `just check` green: svelte-check with no warnings, Prettier, eslint,
  1,725 vitest tests (68 files), `just tools-test`, `just reader-gate`
  (111 files clean), every mark spec `--check --placed`, and the spelling
  check (0 to change).
- **Negative tests, each seen failing:** the store's shared-answer tests
  and the old-schema migrations (red before migration 11), the routes' and
  the review script's tests, and every new tool test before its code.
  The exceptions are two small `article_check` tests, which were written
  with their code.
- **In a browser** (`.scratch/057/share-probe.mjs`, a dev server over a
  seeded data directory), **keyboard only**:
  - the own Q&A and "Readers' Q&A (1)" show, with a pending share neither
    counted nor shown, and no name on the shared answer;
  - Space on the share box asks for a review, and its waiting text shows;
  - Space again takes it back;
  - `review-notes.mjs shares` then lists the share made in the browser.
- The tools checked live where they read the web: the Hermitage Isis and
  PDB pages through `commons_media`, "Isabella Beeton=Household" and
  "Project MAC" through `--expect`, and the two DOIs. Every plate in every
  subject was redrawn, and all came out identical (below).

## Repaired in passing

- **12 bar-chart example specs and 25 plate modules had drifted from their
  committed SVGs.** The spelling sweeps of sprints 044 and 050 respelled
  the SVGs but not their sources, so redrawing would have undone American
  spelling on 26 plates. The sources are respelled, and all 168 charts and
  every plate now reproduce byte for byte.
- `commons_media`'s DPLA reader took a bracketed date span, "(1836 -
  1849)", for an author; it is skipped like a date now.
- `american.py` would have crashed on the new `markCapOverrides` key; it
  now skips it, with a test. The wiki-cite README said `accessed` is
  "today"; it now says it is today's UTC date.

## Follow-ups

None filed. The overseer routes these:

- `subjects/food/frames/annona/scene.svg` does not match its module. The
  module draws "PORTUS · TRAJAN'S BASIN · EARLY 2ND CENTURY AD", which
  matches the reading. The committed plate says "TRAJAN'S HARBOR, c. AD
  112". Redrawing it changes a published date label, which needs an
  `edits` entry and a call on which date is right, so it was left as it is.
- `names/cell-biology.json` is Q7868, _Cell (biology)_, not cell biology.
  The new collision warning will name it if an author looks up the
  discipline. Renaming a published id changes marks in every subject.
- BHL plates already published were cited as public domain. The new
  licence rule would write CC BY 2.0 for them. Re-auditing published media
  against the rule is a content pass, not done here.
