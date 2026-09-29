# Sprint 018 — Connections 2: names across every subject, and skills that write links

korg proposal 3444, covering 3440. Branch `018-connections-2`. Phase 2 of
the connections design (korg 3399), after phase 1 (sprint 017).

## Goal

Phase 1 built the name registry, the marks, connections and the jumps, and
marked western-civ fully. The other three subjects carried only the seven
shared names. This sprint:

- backfills name marks across AI, Feynman and Computing, one agent per
  subject;
- looks for the connections earlier sprints missed, above all between
  western-civ and the rest;
- teaches grow and `skills/author-subject` to write names and connections
  as they write frames;
- reports the density per subject, for the map's defaults (phase 3, 3441).

## Premise check

- **The lookup tool drifted.** `create-tools/names/names.py lookup` shipped
  in phase 1. What 3440 asked for that it lacked: writing a registry
  entry, and flagging an ambiguous name. The work shrank to those.
- **Backfill holds.** AI 66 frames, Feynman 62, Computing 70 (3440 said
  73). Outside western-civ, only the seven shared names were marked.
- **Validation rules are gone.** Unknown name, repeated mark, a connection
  without a `why`, and a dangling target were all enforced by phase 1
  (`validate`, `graphProblems`). Nothing to build.
- **Skills hold.** Grow refused an unregistered mark and could not add a
  name. Ken decided on 3440 (2026-09-29): grow may add names.
- **3442** (the grown-content review path) is undecided, so the
  proposal's note on it does not apply: the backfill goes through this
  sprint's own PR.
- No cross-project plan lists kloom.

## Decisions

- **`names.py` gains `add` and `density`**, rather than a second tool
  beside it. `lookup` already did the Wikidata half of 3440's
  "name-lookup". `add` writes drafts into the registry and refuses a
  Wikidata item another file holds (naming it), all or nothing; `--update`
  to rewrite. `lookup` now prints `ambiguous` for a disambiguation page
  and `missing` for no article, instead of the disambiguation page's own
  item.
- **Grow may add names, never change them.** The job gets the registry as
  `names/` and a list of every served frame as `reference/frames.md`.
  `linkGrowthProblems` (engine/ai/grow.ts) refuses an existing name
  changed or removed, a new name that is invalid, holds another name's
  Wikidata item, or is marked in no frame the job wrote, and a new
  frame's connection (or a new name's home) to a frame not listed and not
  added. A name no frame marks would be clutter the job cannot justify.
  The new name files are committed with the frames (`Names:` trailer),
  and taken back out if the commit fails. The registry must be in the
  subject's repository, which it is in the checkout and the content clone.
- **A grown connection lives on the new frame.** Existing frames stay
  unchanged, and a connection shows on both ends anyway.
- **A grown Wikidata ID must be read, not remembered.** Without the web the
  skill says `null`. The gate cannot check an ID's truth, so the skill
  says it plainly.
- **Parallel authors don't write `names/`.** For the backfill and in
  author-subject, each author drafts name files into its own directory
  and writes a mark spec, with ids taken from `lookup` so two authors
  reach the same id for the same thing. The reviewer merges with
  `names.py add` and marks with `names.py mark`.

## What shipped

- `create-tools/names/names.py`: `lookup` flags `ambiguous` and `missing`;
  `add`; `density`. README updated.
- Grow: `linkGrowthProblems`, the registry copied in and committed out,
  `reference/frames.md`, the `Names:` trailer, `result.names`. Four new
  grow tests (a name added and committed; a name changed, unmarked or
  duplicated refused; a connection to a listed frame kept and to a
  missing one refused; a new name taken back out when the commit fails).
- `skills/grow/SKILL.md` §Names and connections, and the checklist.
- `skills/author-subject/SKILL.md`: links planned up front, authors
  drafting names and specs, the reviewer's `add` and `mark` step, density
  in the record.
- design.md §Grow and §Connections.

## Verification

- `just check` green after the grow change: 678 tests.
- Negative tests, each seen failing: dropping `linkGrowthProblems`'
  problems fails the two refusal tests; skipping the "must be marked"
  rule fails the refusal test; `names.py add` refuses a duplicate
  Wikidata item (exit 1, nothing written) and a malformed draft.
