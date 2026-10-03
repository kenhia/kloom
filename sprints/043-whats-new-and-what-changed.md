# 043 — What's new and what changed: added dates, a filterable Changelog, "new to you" marks, and Edits & corrections

## Goal

korg proposal 3527, covering 3525 and 3526, run directly with `/start-sprint`.
kloom grows (grow, new subjects, sprints) and is corrected, and nothing told
a reader so. That matters most to the family readers on the public site.
Ken's decisions are recorded on both items:

- **3525.** Added dates come from git, with an override. Both ways of
  reading are supported: a Changelog filtered by subject and date for
  browsing, and "new to you" marks for reading a subject straight through.
  "I'm caught up" and "Mark all as seen" clear the marks.
- **3526.** Revisions are recorded in the frame itself, written by the
  skills, and shown under Citations and as a second Changelog tab.

## Premise, checked at start

- **3525 holds.** Nothing in the model, the compiler or the reader store
  knew when a frame arrived. There was no first visit, no record of opened
  frames and no watermark.
- **3526 holds.** There was no `edits` field. Both backfill sources are on
  `main`: kloom#35 (`3e4f0e4`, three reader-note revisions) and the Guam
  rewrite (`6b071b8`, sprint 036, korg 3487).
- **Nothing pending.** `just grow-pending` listed nothing, and kloom is not
  in the cross-project plan index.

## Decisions

- **The history is the checkout's first-parent line** (`engine/history.ts`,
  one `git log --first-parent --diff-filter=A --no-renames`). On `main`,
  that dates a frame by the squash merge that reviewed it in. In the
  service's content clone, which is on `grow/kai`, a grown frame dates
  from its grow commit, so it shows as new on Ken's instance as soon as it
  is grown. And the public site's library is staged from the published
  commit, so its history ends there: the cap the item asked for comes free,
  with no extra code.
- **An override is the day's noon UTC.** `added: "YYYY-MM-DD"` would
  otherwise read as the day before anywhere west of Greenwich.
- **The dates are applied when the library is derived, not with the
  subject.** A merge changes history without necessarily changing a file,
  so the dates live in their own table and a digest in the meta. A build
  whose files are unchanged still notices new history, and re-derives
  without recompiling any subject. `ContentDb.head` puts the dates in
  force into the head it serves.
- **A first publish is one entry.** Everything a subject came with is one
  line ("First published · 64 frames"), and a trail with the frames it
  came with is one entry. Without this, the Changelog's first screen would
  have been 616 frames.
- **"Opened" is the place write.** It happens 800 ms after the reader
  stops on a frame, and it already ran for every reader. The store's
  `visit` now also starts the subject, marks the frame seen and records
  activity, in one transaction, so the client needed no new call for
  this.
- **"New to you" counts from the later of the first visit and the
  watermark.** That makes "I'm caught up" clear the marks as well as set
  the Changelog's preset, which is Ken's case ("if I've read all of Blood,
  anything since I finished is new").
- **A subject never visited has nothing new.** All of it is new, so none
  of it is marked. "Since I caught up" in the Changelog counts from each
  subject's own watermark, or its first visit before one exists, and shows
  everything in a subject never visited.
- **"Since my last visit": a visit ends after a two-hour pause.** The
  store keeps the last activity, and the last activity before the latest
  pause.
- **Readers from before it** are taken to have started each subject with
  their earliest record in it (a place, bookmark, note or kept answer), and
  to have opened every frame those records name (migration 7).
- **The spark is a fourth row under the line**, first, so the reader's
  marks stay one vocabulary. The timeline is 0.4rem taller to hold it.
- **Edits are body, not head.** They show only in the reading pane, and
  the Changelog reads them from their own table. The page's head stays the
  size it was.
- **Grow writes no edits.** Its skill forbids changing an existing frame.
  The definition of "meaningful" lives once, in `skills/grow/SKILL.md`
  §Edits and corrections, and review-notes, review-grown, author-subject
  and CLAUDE.md point at it.

## What shipped

- **Content model.** `added` (a frame or trail override), `edits`
  (`{date, kind: correction | revision, summary}`, newest first, at most
  400 characters), validated, and `created` on a served subject.
  `FrameBody.edits`.
- **The compiler** (`CONTENT_SCHEMA` 2): `edit` and `added` tables, the
  dates digest, `datedHead`, `addedFrames()`, and `changelog` beside
  `map` and `stats`. Every caller passes `gitAddedDates`: the app's build,
  `just build-content`, `stage-public` and the gate.
- **`engine/whats-new.ts`**: `changelogOf`, `newToYou`, `readingFrom`, the
  filters and presets, and day/subject grouping.
- **The reader store**: migration 7 (`reading`, `seen`, `activity`,
  backfilled), `readings`, `seenFrames`, `markSeen`, `catchUp` and
  `lastVisit`, and export version 4 (readings and seen frames, with
  versions 1–3 still read). `deleteReader` removes them.
- **Routes**: `GET /api/changelog`, `POST /api/reader/seen` and
  `POST /api/reader/caught-up`, both behind the reader gate. The page's
  load carries `news` (`readerNews`).
- **UI.**
  - `engine/ui/Changelog.svelte`: two tabs, subject checkboxes, _When_,
    "Mark all as seen", and "I'm caught up on X" when one subject is
    filtered. ↑/↓ move between entries.
  - The HUD's What's new button, with a count.
  - The start screen's What's new in the corner, "N new" in the subject
    list, and "N new since you started" under Begin.
  - The spark on the spine.
  - "new to you" in Contents and on trail markers, with "I'm caught up on
    this subject" in Contents.
  - "Edits and corrections" below Citations.
- **Backfill.** Revisions on `harrison-chronometer`, `antikythera` and
  `logarithms` (kloom#35, 2026-10-01), and the correction on `navy-pow`
  (3487's Guam rewrite, 2026-10-02).
- **Docs and skills.** design.md §What's new, and its Content model,
  Serving, Reader data, Marks and Start screen sections. The User's
  Guide's What's new part. The skills: grow (the definition),
  review-notes, review-grown, author-subject. CLAUDE.md.

## Verified

- `just check`: the gate, with new tests for:
  - date derivation, against a squash-merged fixture repository: merge
    dates, a capped checkout, a rename, re-addition, and no repository;
  - the override, trails and the Changelog, in the compiler;
  - the "new to you" rule, the watermark, the filters and the grouping;
  - the store's records, migration and export;
  - the routes against the gate's real, git-dated library;
  - the page's marks and the edits section;
  - edits validation.
- **The manual test.** This ran in a scratch clone of the repository,
  served by a dev server with tailnet readers.
  - Reader A visited Keeping Watch. Then a frame (`test-ward`) was added
    on a scratch branch and squash-merged into the clone's `main`.
  - For A, the HUD said "1 new to you here", test-ward's tick said "new to
    you", and Contents marked it and offered "I'm caught up".
  - The Changelog opened with focus on its tab. Its newest entry was
    test-ward, marked new to you, and each of the ten subjects' first
    publish was one entry.
  - Filtered to Keeping Watch "since I caught up", the Changelog showed
    test-ward alone. Enter on it went there with a Back chip. Once it was
    opened it was no longer new, and Esc returned focus to the button.
  - Reader B, who had never visited Keeping Watch, saw nothing new.
- **390 px.** The Changelog fits (16 to 374 px) and its list never scrolls
  sideways. The start screen's corner holds three icons.
- **The browser checks.**
  - `just scene-fit`: 0 misfits in 616 frames at 1280×800, 1400×900 and
    390×844. The taller timeline costs no frame its fit.
  - `just keys-check`: 70/70.
  - `just colours-check`: 92/92.
  - `just home-check`: 11/11, after the repair below.
- **The public stage.** `just stage-public` dated 657 frames and trails,
  the newest being `royal-society`, the last addition on `main`. Its
  Changelog had 29 entries and 4 edits.

## Repaired in passing

- **The start screen's drawing took Begin's clicks.** With the reader's
  real data, the new "8 new since you started" line pushed the column
  down, and the loom's ring of drawings (`.stage`, decorative and
  `aria-hidden`) then lay over Begin and took its clicks. `just home-check`
  failed 3 of 12 on this, and `main` passed it. The stage is now
  `pointer-events: none`: it handles no input, so nothing it overlaps can
  lose a click.

## Notes

- **The dev `data/reader.db` on kai is at schema 7.** The browser checks
  opened it, so the migration ran on Ken's dev data. An app from before
  this sprint refuses a newer file, so a dev server started from an older
  checkout (`main`, until this ships) would refuse it. This is by design
  (§Reader data). It is noted here so it is not a surprise.

## Follow-ups

- None filed.

## Deployed

2026-10-03, from merged `main` at `5c9d652` (PR #50).

- **kai** (`just deploy`, declared in `.sprint-deploy`). The service's
  `reader.db` was copied first, at schema 6, to `reader.db.pre-043` beside
  it. `just verify` passed all 10 checks.
  - Live, `/api/changelog` serves 29 entries and 4 edits. Its newest entry
    is `royal-society` (2026-10-02T22:49Z), and navy-pow's body carries its
    correction.
  - The store is at schema 7, and its counts are unchanged: 19 places, 1
    bookmark, 3 kept answers. The backfill made 19 readings, 23 seen frames
    and 2 activity rows.
- **kloom.kenhiatt.us** (`just publish-public`, after Ken approved it in
  session).
  - Before: the site's store (schema 6: 4 accounts, 2 places, no notes or
    bookmarks) was copied to `public/reader-20261003-1705.db` and passed
    `integrity_check`.
  - Published as release v6, image `kloom-reader:5c9d65234-202610031712`.
    `verify-public` passed every check, with 0 notes and 0 detached.
  - After (`public/reader-20261003-1713.db`): schema 7, with 4 accounts and
    2 places intact. The backfill made 2 readings, 2 seen frames and 1
    activity row.
  - On the machine, `/app/content.db`'s source is `5c9d652` and its
    Changelog's newest entry is `royal-society`: nothing after the
    published commit.
