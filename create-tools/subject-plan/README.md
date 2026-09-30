# subject-plan

Author a subject from a plan: the whole intended spine and trails up front,
the frames written segment by segment, or by several authors at once
(sprint 006).

```sh
python3 create-tools/subject-plan/subject_plan.py create-tools/subject-plan/ai.json subjects/ai
python3 create-tools/subject-plan/subject_plan.py create-tools/subject-plan/ai.json subjects/ai --check
npx prettier --write subjects/ai
```

- A plan is `{"spine": {"segments": [...]}, "trails": [...]}`, in exactly
  the shape of `spine.json` and `trails/<id>.json`.
- Running it writes `spine.json` and the trail files holding **only the
  frames whose directories have a `frame.json`**. It leaves out an empty
  segment, and a trail whose anchor or every frame is missing. So the
  subject validates at every step (`npx vitest --run engine/subjects.test.ts`),
  and every commit on the way is green.
- `--check` writes nothing. It counts the frames written and lists the
  planned frames still to write, plus any frame directory the plan does not
  name.
- `--complete DIR` writes a copy of the subject at `DIR/<subject>` holding
  only the frames that have a `frame.json`, with its spine and trails. With
  several authors at work, the live subject fails validation on whoever is
  mid-frame; this lets one author check their own finished frames:
  `KLOOM_TEST_SUBJECTS=DIR KLOOM_TEST_NAMES=DIR/.names npx vitest --run engine/subjects.test.ts engine/svg.test.ts`
  (the tests read their subjects from `$KLOOM_TEST_SUBJECTS` and the
  registry from `$KLOOM_TEST_NAMES` when they are set). The copy holds the
  other subjects too, which connections may name, and the registry at
  `DIR/.names`, into which `--drafts DIR` (repeatable) merges an author's
  name drafts, so marks on names not yet added validate (sprint 021: since
  connections arrived in sprint 017, a copy without them failed every
  author). `--only FRAME …` keeps only those frames and the ones already
  committed, so another author's half-written frame cannot fail this
  one's check, and a draft's `home` on a frame not in the copy is dropped
  (sprint 021). Never run `subject_plan.py` without `--complete` on a
  subject others are writing: it rewrites the live spine, and sprint 021
  lost the working tree's trails to it twice. Sprint 014's authors each improvised this. A finished trail frame
  whose anchor is not written yet is on no spine, so the copy leaves it out
  and names it rather than failing every author on it (sprint 015). To check such a trail before its anchor lands, copy any finished main-spine
  frame into `DIR/<subject>/frames/<anchor>` as a stand-in (change its `id`
  and accent, and strip its name marks), copy your trail frames in beside
  it, run `subject_plan.py <plan> DIR/<subject>` on the copy (the rule
  against running it without `--complete` is about the live subject), and
  re-run the tests on the copy. To test marks as well, place them in the
  copy: `names.py mark <spec> --root DIR --names DIR/.names` (sprint 024;
  without `--root`, `mark` writes into the live subject).
- Its JSON is not Prettier's layout, so run Prettier over the subject
  afterwards.
- Standard library only.

`ai.json` is the plan for `subjects/ai`. Once every frame is written, the
plan and the subject's own files say the same thing. Grow edits
`spine.json` directly and never reads a plan.

`prose_words.py SUBJECT_DIR [FRAME …]` counts each reading's prose as the
grow skill counts it (not tables, image lines, chart lines or headings), marks those
outside 550–900 (`--min`, `--max`), and exits 1 if any is (sprint 015).
