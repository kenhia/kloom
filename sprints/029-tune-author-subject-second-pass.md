# 029 — Tune author-subject, second pass: In the Blood's findings

## Goal

korg proposal 3476, covering korg 3473: fold the eleven findings of
_In the Blood_ (sprint 028, the first author-subject run after sprint
027's tuning) into the schema, the tools and the skills, before the
nursing subject (korg 3471), whose sources are exactly these cases:
letters and diaries, articles held only on JSTOR, and records known only
from another work's references. Ken decided all eleven on 2026-10-01 (the
decisions comment on 3473), and, as for 027, asked for everything to be
fixed here even if it ran long.

Order of work: A1–A5 (the citation schema, its renderer and validator,
the migration, and re-validating In the Blood), C10–C11 (`names.py strip`
and name ownership), B6–B9 (the tools), then the grow and author-subject
text.

## Decisions

- **Premises held** (checked at start). `abstractOnly` was live in 35
  frames across five subjects, and Pepys was cited as `web`. `citedIn`
  still required a url or doi. `subject_plan.py` had no draft option,
  `contact_sheet.py` wrote one sheet whatever the count, and `names.py`
  had no `strip` and no set-index or class check. One sub-claim had
  drifted: `commons_media` already carried PEP 723 metadata (sprint 027,
  korg 3404). What it lacked was a shebang to use it, and any way to
  convert under a plain `python3`. kloom is not in the cross-project plan
  index.
- **The three dropped citations have chains.** Crow 1993 (cited on
  `bernstein`) lists von Dungern and Hirszfeld 1910 in its references.
  Farr 1980 (`early-transfusion`) cites Sprat's _History_ of 1667 at p. 317. Farr 1979 (`abo`) cites Bernheim's _Adventure in Blood
  Transfusion_ (1942). Each was checked in the copy the author had read.
- **The diary's date reads as the house style's other dates do**
  ("November 14, 1666"), where the decision's sketch wrote "2 January
  1666". The sketch's date order was illustration. A `letter` already
  renders its date this way, and a bibliography with two date styles
  would be the inconsistency.
- **A kept answer saved before this sprint is not refused.** Reader data
  (a kept answer's copy of a frame's citations) is validated on import
  and by grow. Refusing `abstractOnly` there would have broken an export
  and a grow job for any reader who kept an answer citing one. So
  `citationProblems(c, { legacy: true })` accepts the old field for kept
  answers only, and the renderer still says "Read in its abstract." for
  it. Frames refuse it.

## A1. `read` replaces `abstractOnly`

`read: "abstract" | "first-page" | "excerpt"`, rendered "Read in its
abstract.", "Read in its first page.", "Read in an excerpt.", in the
bibliography and in the key source's line. All 77 `abstractOnly: true`
became `read: "abstract"`, by text edit so no file was re-serialised.
Then four corrections:

- **In the Blood's four Nature letters** (`hla`'s Terasaki 1964 and the
  1958 leucocyte antibodies, `more-antigens`'s 1950 and 1951 antigens)
  became `first-page`: an old Nature letter has no abstract, and
  nature.com shows its first paragraph. This is A1's own case.
- **Eight notes that meant exactly a read extent** were folded into the
  field, keeping any remainder as the note: `first-page` for
  `autoanalyzer` ("Read on its first page only"), `cryoprecipitate` (its
  opening paragraph in a free preview, where it had been `abstract`) and
  `x-rays` (only its first paragraph); `excerpt` for `enzymes`,
  `periodic-table` (two) and `jinkoki`; `abstract` for `rsa` (an arXiv
  abstract). The result: 73 `abstract`, 7 `first-page`, 4 `excerpt`.
- Left as written: `solids` (the cited work is itself an excerpt),
  `haber-bosch` (an executive summary), and the notes naming the copy a
  work was read in.

## A2–A5. The other citation forms

- **`citedIn` by chain.** A citation with no url and no doi stands when
  its `citedIn` names, by title, a work the same frame cites with a url or
  doi. `citedInProblems` checks that per frame, matching titles loosely
  (case, quotation marks and punctuation set aside). Such a citation
  needs no `accessed`, renders no link, and cannot be `key`, because the
  Sources list links what was read. Restored: von Dungern & Hirszfeld 1910
  (`bernstein`), Sprat 1667 (`early-transfusion`), Bernheim 1942 (`abo`).
- **`diary`**: `title` is the diary, `written` the entry (required), and
  the edition is set as a chapter's volume is: "Pepys, Samuel. Diary
  entry, November 14, 1666, in _The Diary of Samuel Pepys_, edited by
  Henry B. Wheatley. pepysdiary.com. London: George Bell & Sons, 1893."
  pepysdiary.com's text is Wheatley's 1893 edition, its "About the text"
  says. The three Pepys entries are re-cited. The key source's line says
  "entry of November 14, 1666".
- **`mirror: true`**, refused with a `doi`, adds "(copy at host)" after
  the url and "Copy at host" to the key source's line. The 2011 Joint
  Blood Program Handbook (`asbp`) is re-cited with it, and its note
  loses "read in the copy at generalstaff.org". Ten other notes name a
  copy of a work that does have an official copy, and stay: there the
  rule is still to cite the work.
- **JSTOR.** No validator ever resolved a DOI, so the decision's "must not
  require a JSTOR DOI to resolve" holds as it stands. What changed: a
  www.jstor.org url must be the stable form, `/stable/N` (daily.jstor.org,
  a magazine, is another site). Arrow's "Gifts and Exchanges"
  (`gift-relationship`) was cited by its PhilPapers record. It is now
  cited by `https://www.jstor.org/stable/2265097`, the suffix of the
  10.2307 DOI that AcaWiki gives. JSTOR answers a script with a challenge
  page, and Crossref finds only the 1981 reprint.
- design.md §Citations records all of it.

## C10–C11. What authors see, and who owns a name

- **`names.py strip <subject>/<frame> … [--out DIR]`** prints or writes
  readings with every mark taken out and its words left. The
  author-subject brief now gives authors the hand-written frames this
  way. `mark --check --placed` in `just check` stays the backstop.
- **One owner per shared name**: the brief assigns each name two or more
  parts will mark to the part planned to commit first. That part drafts
  it, home or not; borrowers pass its drafts with `--drafts`; the home
  frame's author adds `home` with `--update` when that frame lands. §4's
  "apply the owner's draft with `--update`" workaround is gone, and
  "Check the brief" now includes an owner for every shared name.

## B6–B9. The tools

- **`subject_plan.py --complete --with-drafts`** copies each frame's
  `frame.json.draft` into the checking copy as its `frame.json`. Over a
  live `frame.json` it says that it did. Its README and the author-subject
  skill describe the new workflow, and a test covers both paths.
- **`contact_sheet.py`** writes one PNG per plate above two plates,
  `FILE-<frame>.png` (a chart's `FILE-<frame>-<chart>.png`), each 1,070 by
  930 at `--scale 2.5`. `--per-plate` and `--one-sheet` force either.
  The HTML page of them all is still written. Three blood plates were
  looked at to check it.
- **`commons_media`**:
  - Flickr's "No restrictions" is written as public domain, with a
    warning and an empty `note`. The gate refuses an empty note ("note
    must be text"), so the public-domain basis has to be written in. The
    tag is named, and the Internet Archive Book Images account is not
    written as an author. Checked live on an 1890 Manchester _Memoirs_
    scan.
  - A `PD-self` file with no author credits the uploader of its first
    version, `"Name (uploader)"`.
  - A `uv run --script` shebang, and a converting command (`--jpeg`,
    `jpeg`, `crop`) run under a `python3` without Pillow runs itself again
    under `uv`. That path was checked with `python3 -S`, which hides
    site-packages.
  - `crop SRC DEST --box L,T,R,B [--width 960]` for a page image from
    outside Commons.
- **`names.py lookup`**:
  - A set-index page (in the hidden "All set index articles" category,
    which carries no disambiguation flag) is `ambiguous`.
  - Every row gives the item's Wikidata `instance_of` and description, and
    `--expect` checks those too. Live: "Sodium citrate" is ambiguous, and
    "Duffy antigen system" with `--expect blood` warns that Q205042 is a
    protein.
- Tests for each, none needing the network.

## The skills

- **grow**: `read`, `citedIn` without a link, `diary`, `mirror` and
  JSTOR in the citation rules; Flickr and PD-self in the Commons bullet;
  `crop` for a page from outside Commons; lookup's new checks.
- **reaching-sources**: `read` in the rules; Nature's old letters as
  `first-page`; a PubMed-record-only paper and a lending-only book cited
  through `citedIn`; a JSTOR entry.
- **author-subject**: C10 and C11 as above, `--with-drafts`, a PNG per
  plate, and `lookup --expect` on drafted ids.

## The gate and the dry runs

- `just check` is green: svelte-check, Prettier and ESLint, 1,140 vitest
  tests, `just tools-test` and every mark spec with `--check --placed`.
- **In the Blood re-validated** under the new forms, with its restored,
  re-cited and migrated citations: the subject tests pass.
- **Negative tests**, each planted in a blood frame and watched to fail
  with its own message, then restored:
  - a `citedIn` naming a work the frame does not cite;
  - `abstractOnly` back on `hla`;
  - a JSTOR PDF url;
  - a `mirror` with a doi;
  - a diary entry without `written`;
  - an empty note.
- **`--with-drafts` dry run on In the Blood**: `hla`'s `frame.json`
  renamed to `frame.json.draft`. `--complete --only hla` left it out (61
  of 62). With `--with-drafts` it was in the copy as `frame.json`, and the
  copy's subject and svg tests passed (712). It was restored after.
- **`strip` dry run on In the Blood**: all 62 readings stripped, with no
  mark left. A copy of the subject was given the stripped readings, and
  `names.py mark` over its specs put back a copy byte-for-byte identical
  to the committed readings.

## Repaired in passing

- **`names.py`'s command count was stale.** The README said five commands
  and the docstring listed four, while `reach` (sprint 021) went
  undescribed in the docstring. There are six with `strip`, and both now
  say so.
- **Internet Archive Book Images was written as an author** by
  `commons_media` (it is the Flickr account). It is boilerplate now, with
  the other non-authors.

## Not changed

- **`duffy-antigen-system` keeps Q205042**, the ACKR1 protein's item.
  Wikidata has no item for the blood group system: the English article
  links to the protein, and the one other "Duffy Blood Group System"
  (Q108778698) is a scholarly article. The new lookup warning is what an
  author needs here; the registry's item is the only one there is.

## Follow-ups

None filed. All eleven are done, as Ken asked. Nursing (korg 3471) is the
third run of the tuned skill, and reports its findings in a new feedback
item.
