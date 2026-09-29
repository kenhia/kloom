---
name: kloom-author-subject
description: Author a whole new kloom subject — a plan, a theme, one segment written by hand, then parallel authors for the rest, reviewed and committed segment by segment. The procedure sprint 006 used for the AI subject, written down in sprint 014 and first followed for Richard Feynman. Use when a sprint creates a subject, not for adding a few frames (that is grow).
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
  → categories, a person is the dates of a life.
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
- **The theme.** `subject.json` holds the title and named palettes, in
  dark/light pairs that name each other as `counterpart`. Tie a pair to a
  part of the story (an era, a place, a mode of work). Check ink, muted,
  accent and line at **4.5:1 or better** against the background, and write
  the check down (the sprint record keeps the numbers).
- **The voice.** Decide the headline voice once. western-civ and ai use a
  collective "we"; a subject built on a person may need "he" or "she", or
  the person's own name.
- Grep the other subjects' sprint records for **candidate links** to this
  one, and note the reciprocal ones as you plan.

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
- **the brief**: which frames, in which order, with a line for each saying
  what it is about and what it must not repeat from its neighbours; the
  palettes it uses; the headline voice; the rights and sourcing rules that
  are particular to this subject; and the accents already taken;
- the hand-written frames, to read in full before writing;
- **its own files only**: its frame directories, its own plate module, its
  own chart specs in `create-tools/bar-chart/examples/`. Nothing shared, so
  nothing collides. The author does not touch `spine.json`, the trails, the
  plan or `subject.json`;
- the instruction to **report**: what it wrote, every claim it is unsure
  of, where sources disagreed and what it did, and every place the grow
  skill misled it.

Things authors working at once cannot see, so the brief settles them:

- **Who owns a shared topic.** Where two frames touch one story (a thesis
  and the trail that explains it, a memoir and the frame on its
  reception), say which tells it and which points to it. Sprint 014 had
  three overlaps the brief left open.
- **Accents and images** must not repeat across the subject. Tell authors
  to grep before choosing, and settle clashes at review.
- **Order in a dated trail.** If the dates may not fit the plan's order,
  let the author say what order they need; change the plan, not the sorts.
- **Validation while others work.** The live subject fails on anyone's
  half-written frame. Authors check theirs in a copy of finished frames
  (`subject_plan.py <plan> subjects/<subject> --complete DIR`, then the
  subject tests with `KLOOM_TEST_SUBJECTS=DIR`), and look at their plates
  with `contact_sheet.py`, which shows a plate before its `frame.json`.
- **A trail needs its anchor.** A trail's frames are off the spine until the
  main-spine frame it hangs from exists. Commit anchors first, or tell the
  trail's author to validate against a stand-in.

## 4. Review, validate and commit, segment by segment

As each author reports:

1. Run `subject_plan.py <plan> subjects/<subject>` and Prettier, then
   `npx vitest --run engine/subjects.test.ts engine/svg.test.ts`.
2. Look at the plates on a contact sheet, in their palettes
   (`create-tools/draw-plates/contact_sheet.py <subject> --png …`).
3. Read the report's unsure claims against the cited sources, and spot
   check the surprising ones. Fix or cut; never keep a claim because it is
   good.
4. Commit that segment on its own, so a bad one can be reverted alone.
   Stage it with `create-tools/subject-plan/stage_segment.py`, which stages
   the frames with a spine and trails holding only committed frames (the
   working tree's spine names everyone's), and validate the index before
   committing.

When all are in: `subject_plan.py --check` names nothing still to write,
`just check` is green, and a keyboard-only pass in the browser walks the
main spine and every trail.

## 5. Write it down

In the sprint record: the plan's shape and why, the theme and its contrast
numbers, what the authors reported and what you did about it, the grow
skill's assumptions you found (generalise each in the grow skill or this
one, or say why not), and the candidate links to other subjects.
