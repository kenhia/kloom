---
name: kloom-author-subject
description: Author a whole new kloom subject — a plan, a theme, one segment written by hand, then parallel authors for the rest, reviewed and committed segment by segment. The procedure sprint 006 used for the AI subject, written down in sprint 014, followed for Richard Feynman, the History of Computing (sprint 015), the History of Physics (sprint 021), the History of Mathematics (sprint 024), the History of Chemistry (sprint 025) and How We Build (sprint 026). Use when a sprint creates a subject, not for adding a few frames (that is grow).
---

# Authoring a kloom subject

A subject is a large amount of sourced content: forty to seventy frames,
each a scene, a plate and a 550–900-word reading. One author cannot write it
well in one sitting, and several authors write it badly unless they share a
bar. This is the procedure that makes the bar, then shares it.

**`skills/grow/SKILL.md` is the style guide** for every frame, in full:
the scene, the plate, the reading, the citations, and its §Authoring with
tools. This skill is only the order of work around it. Read that one first.
`docs/design.md` §Content model is the schema, and `create-tools/README.md`
names the tools.

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
- **Scale.** Match the depth asked for, not a count. For scale, western-civ
  has 16 main-spine frames and one trail; ai has 41 and four trails.
- Write the plan as `create-tools/subject-plan/<subject>.json`: the shape of
  `spine.json` plus `trails`. `subject_plan.py` writes the spine and trails
  from it holding only the frames written so far, so every commit
  validates.
- **The title and subtitle.** `subject.json` holds the title and, if the
  subject has one, a `subtitle`: one plain line of at most 60 characters
  said under the title on the start screen, in the subject list and in
  About ("creating the objects around us"). Without one, the start screen
  shows kloom's own tagline.
- **The theme.** `subject.json` holds the named palettes, in
  dark/light pairs that name each other as `counterpart`. Tie a pair to a
  part of the story (an era, a place, a mode of work). Check ink, muted,
  accent and line at **4.5:1 or better** against the background, and write
  the check down (the sprint record keeps the numbers).
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

Start the subject's plates as `create-tools/draw-plates/<subject>.py`, a
collector over `<subject>_<part>.py` modules like `ai.py`, so each author
draws in their own module.

## 3. Briefs, then parallel authors

One author per segment or trail, each a subagent with a shell and the web.
Each author gets:

- the grow skill, `docs/design.md` §Content model and this subject's plan;
- **the brief**: which frames, in which order, each with its `topic` (the
  plain title the grow skill describes, settled here so that no two
  authors reach for the same one) and a line saying what it is about and
  what it must not repeat from its neighbours; the
  palettes it uses; the headline voice; the rights and sourcing rules that
  are particular to this subject; and the accents already taken;
- the hand-written frames, to read in full before writing, with a line
  saying their marks were placed by `names.py mark` (eight of sprint 026's
  twenty-one authors typed marks by hand in a first draft, copying what
  they had read);
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
  same id for the same thing), and writes a mark spec,
  `create-tools/names/examples/<subject>-<segment>.json`, checked with
  `names.py mark <spec> --check --drafts <its drafts>` until nothing but
  "not marked yet" is left. An existing name whose description is written
  from another subject's angle only is reported, not edited. Its frames'
  `frame.json` carry their connections, each checked against the other
  frame's reading;
- the instruction to **report**: what it wrote, every claim it is unsure
  of, where sources disagreed and what it did, and every place the grow
  skill misled it.

**Check the brief before it goes out.** Its topics are validated like any
other (sprint 024's had two over 40 characters), every part gets
connection candidates, trails included, and its facts are leads, not
sources: say so in it. Sprint 024's brief, written from memory, had seven
wrong or out of date (two talks a day apart put in the wrong order, a page that holds only a
promise, a 1923 result that was 1933's, a medieval ban that was a guild's
bookkeeping rule, the Millennium Problems' count, a twin-prime bound and
the RSA records), and each was caught only because an author read the
source.

Things authors working at once cannot see, so the brief settles them:

- **Who owns a shared topic.** Where two frames touch one story (a thesis
  and the trail that explains it, a memoir and the frame on its
  reception), say which tells it and which points to it. Sprint 014 had
  three overlaps the brief left open. Give an anchor's author a line on
  what each of its trail frames covers, not only their ids (sprint 015's
  `colossus` first retold two of its trail's frames), and say who owns a
  figure two frames will want to chart.
- **Each frame's palette.** Name it in the brief, so that dark and light
  alternate along the spine however the frames are shared out.
- **Accents and images** must not repeat across the subject. Tell authors
  to grep before choosing and again before reporting, and settle clashes
  at review: in sprint 015 two authors chose FREE within minutes.
- **Order in a dated trail.** If the dates may not fit the plan's order,
  let the author say what order they need; change the plan, not the sorts.
- **Validation while others work.** The live subject fails on anyone's
  half-written frame. Authors check theirs in a copy of finished frames
  (`subject_plan.py <plan> subjects/<subject> --complete DIR
--drafts <their name drafts>`, then the subject tests with
  `KLOOM_TEST_SUBJECTS=DIR KLOOM_TEST_NAMES=DIR/.names`: the copy carries
  the other subjects and the registry, so marks and connections validate),
  and look at their plates
  with `contact_sheet.py` (`--scale 2.5` to read labels), which shows a
  plate before its `frame.json`. To check a draft before its `frame.json`
  goes live, an author keeps it beside the live tree as `frame.json.draft`,
  copies the directory into the copy as `frame.json`, re-runs
  `subject_plan.py` on the copy, and renames it live once it passes: the
  copy holds only frames with a `frame.json`, so a draft must be put there
  by hand (sprint 025's authors read this both ways). Prettier ignores the
  `.draft` extension: format it with `npx prettier --parser json --write`.
  `prose_words.py` checks the word counts.
- **A trail needs its anchor.** A trail's frames are off the spine until the
  main-spine frame it hangs from exists. If the anchor is already committed
  or live when the trail's author checks, `--only` with the anchor and its
  author's drafts is simpler than a stand-in (sprint 026's trail authors all
  found it so). Commit anchors first, or tell the
  trail's author to validate against a stand-in (the subject-plan README
  says how); the complete copy leaves such frames out and names them. The
  anchor's author finishes the anchor, `frame.json` and all, before the
  rest of their frames.
- **Dated sorts.** Give each frame of a `date` segment its year in the
  brief and check they rise along the segment: sprint 021's plan put
  1850 after 1859, and every author's copy failed on it until review.
- **Each other's drafts.** Say who drafts a name two parts will mark: the
  author whose frame is its `home`, the others passing that author's
  drafts with `--drafts` (sprint 026's authors drafting at the same moment
  collided on `reprap`, `chuck-hull` and `3d-systems` despite grepping).
  Name drafts overlap (four pairs in sprint 021):
  authors grep `.scratch/names/*/` before drafting a name, pass every
  drafts directory to `--complete` and `mark --check`, and check with
  `--only <their frames>` so no one else's half-written frame fails them.
  They write contact sheets to their own `--png`, never run
  `subject_plan.py` on the live subject, and never commit. Name their
  Prettier and plate commands by frame (`npx prettier --write
subjects/<subject>/frames/<frame>/`, `<subject>.py <frame>`): a glob
  reformatted five other authors' readings in sprint 024, and a bare
  `<subject>.py` redraws every author's plates.

## 4. Review, validate and commit, segment by segment

As each author reports:

1. Run `subject_plan.py <plan> subjects/<subject>` and Prettier, then
   `npx vitest --run engine/subjects.test.ts engine/svg.test.ts`.
2. Look at the plates on a contact sheet, in their palettes
   (`create-tools/draw-plates/contact_sheet.py <subject> --png …`).
3. Read the report's unsure claims against the cited sources, and spot
   check the surprising ones. Fix or cut; never keep a claim because it is
   good.
4. **Names.** `names.py add <drafts>` writes the author's new names into the
   registry, and refuses one whose Wikidata item is already there under
   another id: use that id in the spec instead. Where two authors drafted
   the same id, keep one file. Then `names.py mark <spec>` places the
   marks. Read a sample of the new name files: the description is shared
   by every subject, so it must not be written from this one's angle
   only, and the Wikidata item must be the thing meant. Widen, with
   `names.py add --update`, an existing name the authors report as
   described from one subject only: a new subject marks many names another
   added first (sprint 021's `aristotle`, known only by the syllogism).
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
   this for Mendeleev before `periodic-table`).
6. **Connections between the authors' frames** wait for review: each
   author lists the ones they want in this subject, and the reviewer adds
   them once both ends are committed, checking each _why_ against a
   reading. Sprint 021 added 45 this way.

When all are in: `subject_plan.py --check` names nothing still to write,
`names.py mark` finds every spec's marks, `just check` is green (its links
test refuses a connection to no frame and a mark on no name), and a
keyboard-only pass in the browser walks the main spine and every trail.

## 5. Write it down

In the sprint record: the plan's shape and why, the theme and its contrast
numbers, what the authors reported and what you did about it, the grow
skill's assumptions you found (generalise each in the grow skill or this
one, or say why not), the connections made to other subjects and any left
unmade (with the reason), and the density: `names.py density` prints names
and connections per frame for every subject. For a subject meant to link
others, `names.py reach <subject> --steps N` counts how much of each other
subject it can reach, before and after. Record the before at the start
of the sprint, before the first frame, as sprints 024 and 025 did;
`--root` on an archive of the base commit recovers it if you did not.
