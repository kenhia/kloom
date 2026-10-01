# 027 — Tune author-subject from three runs of feedback

## Goal

korg proposal 3467, covering korg 3461: fold what three back-to-back
runs of `skills/author-subject/SKILL.md` reported (Mathematics, sprint
024; Chemistry, 025; How We Build, 026) into the skill and its tools.
The direction comment on 3461 (2026-10-01) sorts every finding into **A**
(fix here, no decision needed), **B** (the citation schema extension Ken
decided on 2026-10-01) and **C** (not changing). Ken amended it the same
day: fix everything in A and B in this sprint, even if it runs long.
_In the Blood_ (korg 3466) and the nursing subject (3470) need A1–A5 and B
next.

Order of work: A1–A5 (the authoring loop), B (the citation schema),
A6–A10 (the tools), A11 (the skill read-through).

## Decisions

- **Premises held** (checked at start). Seven collectors existed, six
  identical and `making.py` with sprint 026's skip-on-failure. The plan
  JSON held only ids. `mark --check` exited 1 on "not marked yet", and
  nothing in `just check` ran it. `published` took four-digit years only.
  One sub-claim had drifted: `mark` already matched on word boundaries
  (`(?<![\w-])…(?![\w-])`), so "electron" never landed inside
  "electrons". Chemistry's case was a spec saying "electron" for a reading
  that bolded "electrons" later, and the bold-mention warning (A3) is what
  catches that. kloom is not in the cross-project plan index.
- **The create-tools get a test gate.** No Python tool had a test.
  `just check` now runs `just tools-test`, which runs each tool
  directory's `test_*.py` with the standard library's `unittest`: no
  dependency added.

## A1. One plate collector

`create-tools/draw-plates/plates_for.py <subject> <frame …>` replaces the
seven `<subject>.py` collectors, which are deleted (the modules'
docstrings now say "See plates_for.py"). It reads which module draws a
frame from the module's `PLATES` keys with `ast`, without importing it,
including the `PLATES['frame'] = fn` lines sprint 026's modules grew by.
It imports only the modules that draw the frames named, so another
author's half-written module costs nothing unless it draws one of yours.
A module that fails to import is named and skipped, and the run exits 1.
A bare run is refused, because `--all` is the way to say "every author's
plates". Tested in `test_plates_for.py`.

Checked: `plates_for.py <s> --all` for all seven subjects, and
`western_civ.py`, redraw every committed plate byte for byte, with one
exception that was not the collector's (below).

## A2. Topic, sort and palette in the plan

A plan takes an optional `"frames": {"<id>": {"topic", "sort",
"palette"}}`. The spine and trails keep exactly the shape of `spine.json`,
so nothing that writes them changed. `subject_plan.py --check` now checks:

- sorts rise within each `date` segment, and only a `date` segment sorts;
- topics are titles of at most 40 characters, and unique;
- palettes are in `subject.json`;
- no `frames` entry names an id that is on no spine.

It warns, without failing, where a palette repeats from one frame to the
next down a segment, and where a written frame's topic, sort or palette
differs from its plan. It exits 1 on a problem and never on a warning.
The author-subject skill makes all three fields required for a new
subject, and the brief quotes the plan rather than being the only copy.
`making.json` is backfilled from its frames as the example, and passes
with no warnings: its palettes already alternate. A copy with two sorts
swapped and an unknown palette exits 1, naming both.

## A3–A5. Marks and names

- **`mark --check` exits 0 on success.** "N marks would place" is
  success; it exits 1 only on a mention it cannot find, an unknown name,
  or a mark no spec lists. `--placed` adds "not placed yet" as a problem,
  for the gate. `mark` takes several specs.
- **It shows where each mark lands**: the sentence, with the marked words
  in brackets, for every mark it places or would place.
- **It warns when a mark misses the bold mention.** A bold run that is
  the spec's words, in any case or as a plural, and holds no mark of its
  own is the mention the author meant. A first version counted any bold
  run that _contained_ the words and flagged 85 of the 4,199 existing
  marks, most of them wrongly (a bold "IBM 701" is not the IBM mention).
  The tightened rule flags 32, each a genuine mark on a passing mention
  before the bold one. It warns only on marks it places now, so it does
  not re-raise those 32.
- **`just check` runs every spec** (`mark examples/*.json --check
--placed`, about 4.5 s). All 90 specs pass. A mark typed into
  `making/knapping` fails it; the first plant reused an id the spec
  already lists, which is the validator's "marked again" warning rather
  than this check's, so the second plant used an unlisted id.
- **Stale drafts**: `mark --drafts` warns about a draft whose id or
  Wikidata item the registry already holds. `add --check` already named
  both cases (sprint 026, and its refusal).
- **`lookup`** prints the article's first line beside Wikidata's
  description (20 titles to a request, the API's limit for extracts),
  with a formula's TeX fallback stripped, and `--expect WORD` warns, and
  exits 1, for an article whose description and first line lack WORD.
  Ids spell Greek letters (`leibniz-formula-for-pi`) and a bare number in
  words. The registry's one digits-only id, `names/0.json`, is now
  `names/zero.json`, with its one mark (`mathematics/brahmagupta-zero`)
  and spec updated. Nothing else names it: reader data keys frames, not
  names, and the service's `grow/kai` branch had no other mark of it.
- Tested in `test_names.py`, with no network.

## B. The citation schema

Every addition is optional, so no existing citation changed meaning;
`engine/citation.ts` renders and validates them, and design.md
§Citations records them. Tests first: thirteen new cases failed before
the code went in.

- **Early dates.** `published` (and a letter's `written`) take a year AD
  of one to three digits without leading zeros (`888`) and a year BC
  (`1550 BC`), with `circa` ("ca. 1550 BC"). A string that reads as it
  renders was chosen over a signed number, which would have needed a
  second field for display. `publishedYear` gives the signed year (-1550,
  as `position.sort` writes it) for comparison. `0888` was already
  accepted as ISO 8601's four-digit form and still is: narrowing a shipped
  rule was not this sprint's call.
- **Roles**: `translators` ("Translated by …"), `engravers` ("Engraved by
  …"), and a letter's `recipients`.
- **Fields**: `edition`; `volumeYear` for an article whose volume came out
  late ("(2016; published 2017)", refused if later than `published`);
  `language`, rendered "In German.", required on a non-English Wikipedia,
  whose key source reads "Title — German Wikipedia".
- **Kinds**: `letter` and `encyclopedia` (an entry, set like a chapter).
  A chapter of a numbered report is a `chapter` with its report's
  `number`.
- **Seen, not read**: `citedIn` ("Cited in …") and `abstractOnly` ("Read in
  its abstract."), shown in the bibliography and the Sources line. The
  fifteen notes that were exactly the old convention ("Read in its
  abstract", with "only", or followed by what was read) moved to
  `abstractOnly`, keeping any remainder as the note. Eight notes that
  mention an abstract in other words ("the figures are from its
  abstract") were left as written. The first pass re-serialised the JSON,
  and Prettier kept `anzan`'s one-line authors expanded, so that file was
  redone as a text edit.
- **The new language rule found two citations of Dutch Wikipedia**
  (`making/wind-sawmill`) with no language. They now say `"nl"`, and
  their container, which their author had written in Dutch, is the
  English one `wiki_cite --lang` writes.
- The grow skill's citation rules say all of this, and drop the old
  advice to cite a translation with `editors`.

## A8–A9. wiki_cite and the validator

- **`wiki_cite`**: a title that lands on a disambiguation page is named and
  left out, like a missing one; `--lang` cites another Wikipedia with its
  `language`; `--text` writes a formula once as its TeX (`$…$`) rather
  than its MathML a token to a line. One premise had drifted: a missing
  title in a batch already reported and carried on, exiting 1 at the end.
  Tested offline in `test_wiki_cite.py`.
- **Validator**: a `media` citation may credit an en.wikipedia.org file
  page (`/wiki/File:…`) without `oldid`; any other wikipedia.org url still
  needs one.

## A6–A7, A10. The tools

- **`commons_media`**:
  - `fetch` names the exact licence tags the file page carries (`PD-Art,
PD-US-expired, PD-old-100`), read from its templates with their
    machinery (`-text`, `/layout`, `-category`) dropped;
  - it writes no `container`, where it wrote "Via Wikimedia Commons", and
    says to add where the work is from;
  - authors: a plain personal name becomes family and given, with life
    dates dropped; boilerplate (an unknown author in several templates and
    languages, "Own work", a scanner's make) writes none and says so;
  - dates: `circa` for "c." or "circa", and a date BC as `"1504 BC"` now
    that `published` takes it. A first pattern read the "C." of "b.C." as
    circa; a circa word must now stand alone before a number;
  - `--page N` takes a page of a PDF or DjVu as a JPEG;
  - `--jpeg`, and a `jpeg` command for a page cropped by hand, composite a
    PNG's transparency onto white. Pillow is the first package this tool
    uses, declared as PEP 723 metadata for `uv run` (korg 3404); the rest
    still runs on `python3`.
- **`contact_sheet.py`** shows a plate at its own 400 by 300, and the PNG
  is as wide as its plates: one plate is 428 by 372 at `--scale 1`, where
  every sheet was 1,636 wide (4,090 at `--scale 2.5`). `--palette
FRAME=NAME` colours one frame. Five plates, one of them recoloured, were
  looked at to check it.
- **`bar_chart.py`** refuses a tick label wider than the space left of
  the axis (about eight characters). Every committed spec still passes.
- **`prose_words.py`** counts a frame's directory, a `reading.md`, or a
  directory of frame directories, as well as a subject.

Each has a `test_*.py` beside it; none needs the network or a browser.

## A11. The skills

- **One "reaching sources" reference**, `skills/grow/reaching-sources.md`:
  every route the three runs found, gathered from the grow skill's
  "Read the primary source" bullet, where they had piled up as repairs.
  The bullet now names the file and what it covers, and the
  author-subject skill gives it to every author. It sits beside the grow
  skill but is not copied into a grow job's `reference/`, because a grow
  job has no shell to use the routes with. One claim was not repeated:
  arXiv's 406 to `read_source` (sprint 024) did not happen again on
  2026-10-01, so the file says it happened once.
- **A frame that marks its own subject's name must say it in prose**, as
  its own bullet in the grow skill. It counts the cases honestly: two
  runs (the Ishango bone, Tyrian purple), not three.
- **The brief's budget**: at most about five must-tell points a frame,
  the rest marked optional. The 550–900 band stays (C).
- **Shared names**: a draft's description is subject-neutral (what the
  thing is, not what it did in this subject), in both skills; widening
  is its own reviewer step in §4, every part.
- **Read-through.** Both skills read end to end as one text. Fixed seams:
  the author's kit now includes the reference; §4's first step runs
  `--check`; the finish line says what `just check` now enforces; the
  scanned-book bullet no longer says `commons_media` cannot fetch a PDF
  page; the no-article rule moved out of the middle of the id rule; two
  paragraphs left badly wrapped by earlier repairs were rewritten.

## The gate and the dry run

- `just check` is green: svelte-check, Prettier and ESLint, 1,054 vitest
  tests, `just tools-test` (54 tests in six tool directories), and every
  mark spec with `--check --placed`.
- Negative tests: a hand-typed mark in `making/knapping` fails the spec
  check; a planted failing assertion in `test_bar_chart.py` fails
  `tools-test`; a plan with two sorts swapped and an unknown palette fails
  `subject_plan.py --check`.
- **Dry run on How We Build:**
  - its plan, backfilled with topics, sorts and palettes, passes the new
    `--check` with no warnings;
  - all 490 marks were stripped from a copy of its readings, and
    `names.py mark` over its 22 specs put back a copy identical to the
    committed readings. `--check` first showed 68 frames as "would place"
    and exited 0, and it warned on two frames whose mark lands on a
    passing mention before the bold one (`handaxe`'s Acheulean,
    `ornamental-turning`'s rose engine). Both follow the first-mention
    rule as written, so they stand; whether to reword them is an
    editorial call about those readings, not one for this sprint;
  - every plate of all seven subjects regenerated byte for byte through
    `plates_for.py`, and western-civ's through `western_civ.py`.

## Repaired in passing

- **`bessemer-steel`'s plate did not reproduce.** Its committed SVG put
  the PIG IRON label at `P(4.2, 1290)`, but `chemistry_materials1.py`
  drew it at `P(4.3, 1312)`: the label was moved in the SVG and not in
  the module. The module now matches, and `plates_for.py chemistry --all`
  reproduces every chemistry plate.
- **`birch-tar`'s "BARK ROLL" ran off the plate's left edge** (anchored at
  its end at x 50, about 52 units wide at size 8), in the app as on the
  contact sheet. It is now size 7 and ends at x 54.
- **`making/wind-sawmill`** cited Dutch Wikipedia with no language, and
  with its container in Dutch (found by B's new rule).
- **`names/0.json` is now `zero.json`** (found by A5's lookup fix).

## Not changed (C)

As the direction comment says: Commons metadata being often wrong (A6
narrows it), Wikipedia being sometimes wrong, the 550–900 band, sites
refusing scripts (A11 gathers the routes), briefs' facts being wrong (the
leads-not-sources rule held in all three runs), `read_source`'s two-page
spreads, the IDEALS User-Agent, nobelprize.org's file names (now noted
in the reference), and the scene counter's overlap (korg 3469).

## Follow-ups

None filed. Everything in A and B is done, as Ken's amendment asked.

## Deployed

2026-10-01, by `just deploy` (the `recipe: deploy` in `.sprint-deploy`),
from merged `main` at `4fae7fe`, to the kloom service on kai. The
service's content clone is at the same commit.

- `just verify` passed all eight door checks: the tailnet door refuses
  anonymous writes and reader-data reads, and the ssh door lets its reader
  through.
- **The sprint's work, live on the ssh door (:4891), each 200:**
  - `/making/wind-sawmill` renders its Dutch Wikipedia citations with "In
    Dutch." (the new `language` field);
  - `/chemistry/pcr` renders "Read in its abstract" in its citations (the
    new `abstractOnly` field);
  - `/mathematics/brahmagupta-zero` carries the renamed `zero` name card;
  - the deployed app holds `skills/grow/reaching-sources.md` beside the
    grow skill.
