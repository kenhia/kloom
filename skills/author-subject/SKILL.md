---
name: kloom-author-subject
description: Author a whole new kloom subject — a plan, a theme, one segment written by hand, then parallel authors for the rest, reviewed and committed segment by segment. The procedure sprint 006 used for the AI subject, written down in sprint 014, followed for Richard Feynman, the History of Computing (sprint 015), the History of Physics (sprint 021), the History of Mathematics (sprint 024), the History of Chemistry (sprint 025) and How We Build (sprint 026), and tuned from those three runs in sprint 027. Use when a sprint creates a subject, not for adding a few frames (that is grow).
---

# Authoring a kloom subject

A subject is a large amount of sourced content: forty to seventy frames,
each a scene, a plate and a 550–900-word reading. One author cannot write it
well in one sitting, and several authors write it badly unless they share a
bar. This is the procedure that makes the bar, then shares it.

**`skills/grow/SKILL.md` is the style guide** for every frame, in full:
the scene, the plate, the reading, the citations, and its §Authoring with
tools. This skill is only the order of work around it. Read that one first.
`skills/grow/reaching-sources.md` is how to read a source that a plain
fetch can't reach; give it to every author.
`docs/design.md` §Content model is the schema, and `create-tools/README.md`
names the tools.

## Extending a subject

Sprint 049 grew western-civ from its 25-frame proof of concept to 72 by
this procedure, and most of it applies as written. What differs:

- **Every existing id is kept**: names, connections, bookmarks, notes and
  kept answers point at them. Frames may move between segments, and the
  plan lists them with no `part`. Record the before (`names.py density`,
  `names.py reach`) as for a new subject.
- **The old frames are not the bar** if they were written before the
  tools (350–700 words, no images): say so in the brief, and write the
  hand frame as for a new subject.
- **Re-palette the old frames** to their new sections in the same commit
  as the plan; a palette is presentation, so no `edits`.
- **Read every old reading's last sentence** once the spine changes: one
  that names "the next frame" may now point at the wrong one. A wording
  fix is not an `edits` entry; a correction an author finds in an old
  frame is, in the same commit as the fix.
- **The old frames' names were described from the old frames' angle**
  (`french-revolution` "which also swept away the old units of measure"):
  list the subject's own names for widening at step 4.
- **Authors may store connections to the old frames**, which are
  committed; give them the full list of frames with the unwritten ones
  marked as planned (`.scratch/049/frames.txt`).
- **Tests that pin the subject's shape** (its palettes, its trails, the
  frames around one) change with it.

## 1. Plan

Decide the whole shape before writing a frame.

- **The spine.** Segments, each with a `labelKind` (`date`, `category`,
  `technology`) and the frames in reading order. A subject is not
  necessarily time: an era is dates, a field may run dates → technologies
  → categories, a person is the dates of a life. `labelKind` says what
  the frames' labels are, not what the segment is: the validator checks
  that sorts rise only within a segment, so a spine by craft or by place
  whose frames are dated is a run of `date` segments, each restarting time
  (sprint 026's crafts), not `category` segments.
- **The trails.** Where a topic needs depth the main spine should not
  carry, it becomes a trail of three to ten frames on one main-spine
  anchor. Prefer a trail over a `category` segment when the topic is a
  detour a reader may skip; prefer a segment when every reader needs it
  in order.
- **Scale.** Match the depth asked for, not a count. For scale, the
  subjects run 62 to 72 frames, a main spine of 40 to 58 and three to seven
  trails (western-civ, 58 and five; ai, 41 and four).
- Write the plan as `create-tools/subject-plan/<subject>.json`: the shape of
  `spine.json` plus `trails`, a `palette` on every segment (its section's,
  below), and a `frames` entry for every frame with its
  `topic`, its `palette`, in a `date` segment its `sort`, and once the
  parts are shared out its `part`, the author part that writes it
  (`making.json` is an example). The plan's `owners` gives each shared
  name its owner (§3). `subject_plan.py --check` checks them
  before anyone writes: sorts rising within each segment, topics at most
  40 characters and unique, palettes in `subject.json`, and a warning where
  a frame's palette is not its section's and its entry gives no
  `paletteWhy`. Three runs kept these only in the
  brief's prose, where nothing checked them (sprint 021 put 1850 after
  1859). `subject_plan.py` writes the spine and trails from the plan
  holding only the frames written so far, so every commit validates.
  `subject.json` and an empty `subjects/<subject>/frames/` must exist
  before it runs.
- **The title and subtitle.** `subject.json` holds the title and, if the
  subject has one, a `subtitle`: one plain line of at most 60 characters
  said under the title on the start screen, in the subject list and in
  About ("creating the objects around us"). Without one, the start screen
  shows kloom's own tagline.
- **The theme.** `subject.json` holds the named palettes, in
  dark/light pairs that name each other as `counterpart`. Tie a pair to a
  part of the story (an era, a place, a mode of work). Check ink, muted,
  accent and line at **4.5:1 or better** against the background, and write
  the check down (the sprint record keeps the numbers). The brightness
  sliders (korg 3495) dim a light background and lift a dark one; a new
  palette must keep that ratio across their range too, which
  `engine/colour.test.ts` checks for every subject.
- **A palette per section** (sprint 038, korg 3495). A segment's palette
  tracks its era or theme, the way western-civ's do, and every frame in it
  wears that palette; set it as the segment's `palette` in the plan, which
  `spine.json` keeps. Do not alternate dark and light from frame to frame:
  until sprint 038 the rules asked for that, and five subjects switched
  scheme on every step, which readers found distracting. Keep the
  subject's balance across sections instead (a dark section, a light one,
  as the story turns). A trail takes its anchor's section's palette unless
  its own era says otherwise. A frame that must stand apart (a dedication)
  is its own one-frame segment, or says why in its plan entry's
  `paletteWhy`.
- **The voice.** Decide the headline voice once. western-civ and ai use a
  collective "we"; a subject built on a person may need "he" or "she", or
  the person's own name.
- **Links to the other subjects.** Read the other subjects' spines and
  `names/`, and note the frames this one will connect to and the names it
  will share (docs/design.md §Connections). Connections are written with
  the frames, not saved up for a later sprint: sprints 006, 014 and 015
  could only list theirs, and 64 waited for sprint 017.

## 2. The first segment, by hand

Write the first segment (two to four frames) yourself, following the grow
skill in full. It does two jobs.

- **It finds the grow skill's assumptions** about the subjects before this
  one. Note every place it was wrong, silent or leading; that list is a
  deliverable (§5).
- **It sets the bar** the other authors are given. They imitate what they
  are shown, so show them your best frames.

Draw the subject's plates in `create-tools/draw-plates/<subject>_<part>.py`
modules, one per author, each exporting `PLATES`, and draw them with
`plates_for.py <subject> <frame …>`. There is no collector to write: one
serves every subject (sprint 027 replaced seven copies), and it imports
only the modules that draw the frames named, so one author's broken module
stops no one else.

## 3. Briefs, then parallel authors

One author per segment or trail, each a subagent with a shell and the web.
Each author gets:

- the grow skill, `skills/grow/reaching-sources.md`, `docs/design.md`
  §Content model and this subject's plan;
- **the brief**: which frames, in which order, each with its `topic` (the
  plain title the grow skill describes, settled here so that no two
  authors reach for the same one), its palette and its sort, quoted from
  the plan rather than written afresh, and a line saying what it is about
  and what it must not repeat from its neighbours; **at most about five
  must-tell points a frame**, the rest marked optional (the 550–900 band
  stays, and in all three runs a brief's must-tell list alone nearly
  filled it); the headline voice; the rights and sourcing rules that are
  particular to this subject; and the accents already taken;
- the hand-written frames' readings **with their marks stripped**
  (`names.py strip <subject>/<frame> … --out <dir>`), to read in full
  before writing, as the quality bar, and their `frame.json` files.
  Authors never see mark syntax: eight of sprint 026's twenty-one authors,
  and three of sprint 028's eighteen despite the brief's warning, typed
  marks by hand in a first draft, copying the marked frames they had read
  (sprint 029). `just check`'s `mark --check --placed` stays the backstop;
- **its own files only**: its frame directories, its own plate module, its
  own chart specs in `create-tools/bar-chart/examples/`, and its own names
  drafts (below). Nothing shared, so nothing collides. The author does not
  touch `spine.json`, the trails, the plan, `subject.json` or `names/`;
- **names and connections**, as the grow skill's §Names and connections
  says, with one difference: the registry is shared, so an author does
  not write into `names/` and does not mark by hand. It drafts the name
  files the registry lacks into a directory of its own
  (`.scratch/names/<subject>-<segment>/`, Wikidata IDs from `names.py
lookup`, never from memory; the id is lookup's, so two authors reach the
  same id for the same thing), with a **subject-neutral description**:
  what the thing is and why it matters anywhere, not what it did in this
  subject (each run widened 14 to 21 names another subject had written
  from its own angle), and writes a mark spec,
  `create-tools/names/examples/<subject>-<segment>.json`, checked with
  `names.py mark <spec> --check --drafts <its drafts>` until it exits 0
  (`lookup --expect` on every id it drafts, which checks the article and
  warns of a set-index page, with `--expect-item` where an article and its
  item may differ, a blood group's and its protein's),
  reading the sentence it prints for each mark and acting on any warning
  that a mark misses the bold mention. An existing name whose description
  is written from another subject's angle only is reported, not edited.
  Its frames' `frame.json` carry their connections, each checked against
  the other frame's reading;
- the instruction to **report**: what it wrote, every claim it is unsure
  of, where sources disagreed and what it did, and every place the grow
  skill misled it.

**Check the brief before it goes out.** `subject_plan.py --check` passes
on the plan it quotes (sprint 024's topics had two over 40 characters),
every part gets connection candidates, trails included, every name two
parts will mark has its owner (below), the part planned to commit first, and its facts are
leads, not sources: say so in it. Every run's brief was wrong somewhere:
sprint 024's, written from memory, had seven facts wrong or out of date
(two talks a day apart in the wrong order, a page that holds only a
promise, a 1923 result that was 1933's, a medieval ban that was a guild's
bookkeeping rule, the Millennium Problems' count, a twin-prime bound and
the RSA records), and sprints 025 and 026 had about forty more between
them. Each was caught only because an author read the source, so the
"leads, not sources" line is what makes the brief safe to be wrong.
Sprint 051's 24 paragraphs were wrong in nearly every part again (a
patent's "reciprocating blades" that were endless bands, the 1935 storm
that did not reach Washington, a "first" order that was the fifteenth).
A frame about **the present state of something** gets a lead that says
"the latest edition", not a year: sprint 051's said SOFI 2025, and SOFI
2026 had been out for ten weeks.
The brief's **"today"** is the UTC date, which `wiki_cite.py` stamps as
`accessed` (sprint 049, so that a revision is never published after it
was read): sprint 055's said the local date, and eight authors rewrote
dates by hand once UTC passed midnight.
**List the widely shared names in `owners` too**, not only the subject's
own crops or devices: the places, institutions and scholars several
parts will name (sprint 051's `chicago`, `kolkata`, `dorian-fuller`,
`anatolia`, Churchill and the vitamin names were drafted at the same
moment by two parts each, because nothing listed them). Sprint 055 listed
98 and still had three such pairs (a patron, a funder, a bacteriologist's
assistant), so tell authors to look for the file in every part's drafts
directory just before drafting a name the plan does not list. **Build each
part's checking command from what it will borrow**, every owner
directory its marks need, and say that `names.py drafts <subject> --part
<part>` finds the rest; sprint 051's commands named the wrong directories
for a third of the parts. A message to an author mid-run starts with the
part it is for: one of sprint 051's went to the wrong agent.
**Run `names.py lookup` on every name id the brief gives an author.** It
is a fact like the others, and cheaper to check than a date: sprint 028's
brief, written from memory, named thirteen ids that were wrong (`de-motu-cordis`
for a redirect, `wright-s-stain` for `wrights-stain`) or had no article
at all (Leone Lattes, Leonard Skeggs, the Armed Services Blood Program),
so those frames could not mark their own subjects. Point the brief at the
richest primary sources for the subject's kind of claim, too: sprint
028's best for bench procedure were US military manuals and DTIC reports
on the Internet Archive, which three authors found for themselves.

Things authors working at once cannot see, so the brief settles them:

- **Who owns a shared topic.** Where two frames touch one story (a thesis
  and the trail that explains it, a memoir and the frame on its
  reception), say which tells it and which points to it. Sprint 014 had
  three overlaps the brief left open. Give an anchor's author a line on
  what each of its trail frames covers, not only their ids (sprint 015's
  `colossus` first retold two of its trail's frames), and say who owns a
  figure two frames will want to chart. That includes two frames that will
  open from one event: sprint 028's `hiv-blood` and `hemophilia-hiv` both
  began from the CDC's report of July 1982, and one was rewritten after
  the other was committed.
- **Each frame's palette.** It is its section's, in the plan and quoted
  in the brief, so a section stays one palette however its frames are
  shared out.
- **Accents and images** must not repeat across the subject. Have
  authors claim an accent before writing, a line `ACCENT part frame` in
  one shared file (`.scratch/<subject>/accents.txt`), the first claim
  winning: grepping alone let four clashes through in sprint 049, each
  found only when another author's frame went live. **`subject_plan.py
<plan> subjects/<subject> --check --accents <file>`** enforces it (sprint
  050): it exits 1 on a claim of a word another claim, a written frame or
  the plan already holds, naming both. An accent the lead settles goes in
  the plan as the frame's `"accent"`, which wins over any claim; a frame's
  later claim releases its earlier one. Have each author run the check
  right after claiming, before writing a line. Settle clashes
  at review: in sprint 015 two authors chose FREE within minutes, and in
  sprint 030 CLOCK was committed while another author still held it in a
  draft. The later author changes theirs; tell them while they are still
  at work.
- **Order in a dated trail.** If the dates may not fit the plan's order,
  let the author say what order they need; change the plan, not the sorts.
- **Validation while others work.** The live subject fails on anyone's
  half-written frame. Authors check theirs in a copy of finished frames
  (`subject_plan.py <plan> subjects/<subject> --complete DIR
--drafts <their name drafts>`, then the subject tests with
  `KLOOM_TEST_SUBJECTS=DIR KLOOM_TEST_NAMES=DIR/.names`: the copy carries
  the other subjects and the registry, so marks and connections validate),
  and look at their plates with `contact_sheet.py <subject> <frames>
--png <their own file>` (`--scale 2.5` to read labels; above two plates
  it writes one PNG per plate, `<file>-<frame>.png`, so none is shrunk past
  reading), which shows a plate before its `frame.json`, in the palette
  `--palette <frame>=<name>` gives it. To check a draft before its
  `frame.json` goes live, an author keeps it beside the live tree as
  `frame.json.draft` and adds `--with-drafts` to `--complete`, which puts
  it in the copy as `frame.json`; it renames it live once it passes
  (sprint 029: three of sprint 028's authors wrote wrappers to copy drafts
  in by hand). Prettier ignores the `.draft` extension: format it with
  `npx prettier --parser json --write`.
  `prose_words.py` checks the word counts.
- **A trail needs its anchor.** A trail's frames are off the spine until the
  main-spine frame it hangs from exists. If the anchor is already committed
  or live when the trail's author checks, `--only` with the anchor and its
  author's drafts is simpler than a stand-in (sprint 026's trail authors all
  found it so). Put the anchor in the brief's own checking command for a
  trail part, too: sprint 030's brief gave `--only <your frames>`, and two
  trail authors built stand-ins by hand for anchors already live. Commit
  anchors first, or give the trail's author `--stand-in <anchor>` in the
  checking command, which puts a placeholder for the anchor in the copy
  from the plan (sprint 033; authors in sprints 025 to 030 built one by
  hand); without either, the complete copy leaves such frames out and
  names them. The
  anchor's author finishes the anchor, `frame.json` and all, before the
  rest of their frames.
- **Dated sorts.** Each frame of a `date` segment has its year in the
  plan, which `--check` keeps rising along the segment: sprint 021's plan
  put 1850 after 1859, and every author's copy failed on it until review.
  If an author finds a date was wrong, change the plan and re-check.
- **One owner for each shared name** (sprint 029; in the plan since sprint
  033). **The plan's `"owners": {"<name id>": "<part>"}`** lists every
  name two or more parts will mark, and assigns each to **the part planned
  to commit first** among them; the brief quotes it, as it quotes topics.
  `subject_plan.py --check` refuses an owner that is not a part of the
  plan, and **`names.py drafts <subject>`** lists who has drafted what
  (id, item, home, part) and exits 1 on a name two parts drafted or a
  draft by a part that does not own it. Run it before the brief goes out,
  and before each part is committed (sprint 030's authors found owners by
  grepping `.scratch/names/*`, and two names were drafted twice because the
  brief's prose and the commit order disagreed). That part drafts it, home or not; the
  others only borrow, passing the owner's drafts directory with `--drafts`
  and never drafting it themselves. If the name's `home` is a frame in a
  later part, the owner drafts it without `home`, and the home frame's
  author adds `home` with `names.py add --update` when that frame is
  committed. Sprint 026's authors drafting at the same moment collided on
  `reprap`, `chuck-hull` and `3d-systems` despite grepping, and sprint 028,
  which gave each name to its home's author, had twelve reach the registry
  first from a borrower's draft, without `home`, before their owner's
  frame landed. The owners are a plan, and the drafts are the fact: where a
  part due to commit earlier has already drafted a name the plan gives to a
  later one, the earlier draft stands, the listed owner borrows it, and the
  plan's `owners` is changed to match, so `names.py drafts` passes again
  (sprint 030: two names drafted twice that way). **A name the plan does
  not list, drafted by a part due to commit later**, is borrowed all the
  same: the reviewer adds that draft to the registry with the earlier
  part, without `home` (sprint 049's `edward-gibbon`). An owner drafts a
  name only if a frame of its own marks it; one that no spec marks is
  dropped before commit. `names.py drafts` refuses such a draft once its
  part's spec (`create-tools/names/examples/<subject>-<part>.json`) exists,
  and notes it until then (sprint 050; sprint 049's `late2` drafted a name
  and never marked it). Draft from the lookup, never by hand: **`names.py
lookup "Title" … --write-draft .scratch/names/<subject>-<part>`** writes
  each draft with its id, Wikidata item and name, and leaves `kind` and
  `description` empty for the author, so `add` refuses it until they are
  written (one of 049's authors typed a Wikidata id wrong). Give the brief's checking command every owner's
  drafts directory, not a placeholder. A name the plan does not
  list goes to the part chiefly about it, its home, unless an earlier part
  already drafted it. Authors run `names.py drafts <subject>` before
  drafting a name the plan does not list, pass every drafts directory to
  `--complete` and `mark --check`, and check with `--only <their frames>`
  so no one else's half-written frame fails them.
  An author's copy grows as the reviewer commits other parts, so a later
  commit (a clashing accent) can fail a frame that passed: check again
  just before reporting. `--complete` ends by counting the copy, not the
  live tree ("the copy at DIR/<subject> holds N of M planned frames";
  three of sprint 049's authors read the old count as theirs).
  They write contact sheets to their own `--png`, never run
  `subject_plan.py` on the live subject, and never commit. Name their
  Prettier and plate commands by frame (`npx prettier --write
subjects/<subject>/frames/<frame>/`, `plates_for.py <subject> <frame>`):
  a glob reformatted five other authors' readings in sprint 024, and
  `plates_for.py` refuses to run without frames (`--all` redraws every
  author's).

## 4. Review, validate and commit, segment by segment

As each author reports:

1. Run `subject_plan.py <plan> subjects/<subject> --check` (a frame that
   differs from its plan is a warning to settle: change the frame or the
   plan), then `subject_plan.py <plan> subjects/<subject>` and Prettier,
   then `npx vitest --run engine/subjects.test.ts engine/svg.test.ts`.
2. Look at the plates on a contact sheet, in their palettes
   (`create-tools/draw-plates/contact_sheet.py <subject> <frames> --png …`,
   a PNG per plate above two).
3. Read the report's unsure claims against the cited sources, and spot
   check the surprising ones. Fix or cut; never keep a claim because it is
   good.
4. **Names.** `names.py add <drafts>` writes the author's new names into the
   registry, and refuses one whose Wikidata item is already there under
   another id: use that id in the spec instead. Where two authors drafted
   the same id, keep one file. Then `names.py mark <spec>` places the
   marks and prints the sentence each landed in: read them. Read a sample of the new name files: the description is shared
   by every subject, so it must not be written from this one's angle
   only, and the Wikidata item must be the thing meant. Then **widen the
   shared names**, as its own step, every part: each existing name the
   authors report as described from one subject only, rewritten for any
   subject with `names.py add --update`. A new subject marks many names
   another added first (sprint 021's `aristotle`, known only by the
   syllogism), and each run widened 14 to 21.
5. Commit that segment on its own, so a bad one can be reverted alone.
   Stage it with `create-tools/subject-plan/stage_segment.py`, which stages
   the frames with a spine and trails holding only committed frames (the
   working tree's spine names everyone's), and validate the index before
   committing, with its new names and its mark spec: export it
   (`git checkout-index -a --prefix=DIR/`) and run the subject tests with
   `KLOOM_TEST_SUBJECTS=DIR/subjects KLOOM_TEST_NAMES=DIR/names`, and stop
   if they fail, unstaging what you staged (`git reset`): sprint 025 left
   four failed parts staged, and the next part's commit took all of them.
   Stage by path: `git add` on a directory other authors
   write in takes their work with it (sprint 021 swept five authors'
   unfinished specs into a commit that way). Stage every name changed since
   the last commit, not only the untracked ones, and add with a part any
   other author's draft its marks use: sprint 024's index check failed
   on a draft whose `home` named a frame not yet committed, and passed
   once that name went in with the frame. When that frame belongs to a
   part still to come, add the borrowed name without its `home` and give it
   back with `names.py add --update` when the frame lands (sprint 025 did
   this for Mendeleev before `periodic-table`). A shared name comes in
   with its owner's part, which the brief made the first to commit, so a
   borrower's part never carries one. When a later part holds the name's
   home frame, add `home` with `--update` as that part is committed. If
   parts land out of the planned order, commit the owner's draft of the
   name with whichever part needs it first, still the owner's, and say so
   in the record.
6. **A frame already committed is published.** Revising one later in the
   run, or another subject's frame (a neighbour the new subject corrects),
   means a fact, date, attribution, quotation or source changed, or a
   section rewritten: add an entry to its `edits`, as
   `skills/grow/SKILL.md` §Edits and corrections says. Adding a connection
   or a name mark is not an edit, and neither is respelling to American
   English.
7. **Connections between the authors' frames** wait for review: each
   author lists the ones they want in this subject, and the reviewer adds
   them once both ends are committed, checking each _why_ against a
   reading. Sprint 021 added 45 this way.

When all are in: `subject_plan.py --check` names nothing still to write
and no problem, `just check` is green (it runs every mark spec with `mark
--check --placed`, so a spec's mark not placed or a mark typed by hand
fails it, and its links test refuses a connection to no frame and a mark
on no name), `just scene-fit <subject>` reports no scene running into the
HUD at desktop and phone sizes, and a keyboard-only pass in the browser
walks the main spine and every trail.

## 5. Write it down

In the sprint record: the plan's shape and why, the theme and its contrast
numbers, what the authors reported and what you did about it, the grow
skill's assumptions you found (generalise each in the grow skill or this
one, or say why not), the connections made to other subjects and any left
unmade (with the reason), and the density: `names.py density` prints names
and connections per frame for every subject. For a subject meant to link
others, `names.py reach <subject> --steps N` counts how much of each other
subject it can reach, before and after. Record the before at the start
of the sprint, before the first frame, as sprints 024 to 026 did;
`--root` on an archive of the base commit recovers it if you did not.
