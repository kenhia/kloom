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
- Its JSON is not Prettier's layout, so run Prettier over the subject
  afterwards.
- Standard library only.

`ai.json` is the plan for `subjects/ai`. Once every frame is written, the
plan and the subject's own files say the same thing. Grow edits
`spine.json` directly and never reads a plan.
