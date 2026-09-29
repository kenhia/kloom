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

- **The backfill ran as drafts, merged centrally.** Three agents (one
  per subject) wrote name drafts and a mark spec into `.scratch/`, never
  into `names/` or a reading. One pass merged them: the same id from two
  subjects became one file (aliases joined), a Wikidata item already
  registered took the registry's id, and each subject's spec was rewritten
  to the final ids. Then `add`, `mark` and the gate, and a commit, per
  subject.
- **Density above the brief's 4–8 a frame is kept.** AI came in at 11,
  Computing at 10 and Feynman at 9, against western-civ's 7. The readings
  are longer (Computing's near 940 words, western-civ's about half), so
  it is about the same per word, and each agent had already cut passing
  mentions.
- **A fourth agent searched for missed connections** across all four
  subjects, reading both ends of each. It proposed 60, with quotes from
  both readings, and I spot-checked the numbers against the readings (the
  1,100 errata, Vlacq's six errors, the 3,183 printings, Kepler and
  Plato's solids). One _why_ was reworded. Two more came from the name
  agents' notes. The rest of those notes were the same name in two frames
  (Turing, Hoff, XCON on the VAX), which the registry now carries, or
  analogies (lab safety frameworks and Feynman's Appendix F, Talos and
  Prometheus), which 017 already ruled are not connections.

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
- **Content:**
  - **984 new names** (1,111 in the registry). Every Wikidata ID came from
    `lookup` (a few from Wikidata search where the title redirected to a
    wider article, as phase 1 did for Project MAC), and all 977 non-null
    IDs were checked against their item's English label in one batch
    read: 104 labels differ from the name, and every one is the same thing
    under a fuller or older label (Al Hibbs, Kyber, Pascal's calculator).
    Seven are `null`: no item (Gweneth and Carl Feynman, Lawrence Mulloy,
    the Cranmer abacus, the General Report on Tunny, Epoch AI,
    constitutional AI).
  - **Marks:** 742 in AI, 723 in Computing, 536 in Feynman. The specs are
    `create-tools/names/examples/{ai,computing,feynman}.json`. Every frame
    of every subject now marks at least one name.
  - **62 new connections** (107 in all): 21 new ones touch western-civ,
    which had one.
- **Density** (`names.py density`, after the sprint):

  | subject     | frames | marks | names | marks/frame | connections (either end) | per frame |
  | ----------- | -----: | ----: | ----: | ----------: | -----------------------: | --------: |
  | ai          |     66 |   742 |   375 |       11.24 |                       46 |      0.70 |
  | computing   |     70 |   723 |   457 |       10.33 |                       54 |      0.77 |
  | feynman     |     62 |   536 |   269 |        8.65 |                       44 |      0.71 |
  | western-civ |     24 |   169 |   120 |        7.04 |                       23 |      0.96 |

  **For the map (3441):**
  - **The names graph is dense and hub-heavy.** One step through a shared
    name reaches a median of 22 frames (p90 67, max 90); in another
    subject, a median of 4 (p90 13). Richard Feynman is marked in 63
    frames, OpenAI 19, IBM 17, Los Alamos 16. A name neighbourhood needs
    a cap or hub damping, or it is the whole Feynman subject.
  - **The connections graph is sparse.** One step: a median of 1 (p90 3,
    max 6), and 98 of 222 frames have none. Two steps: a median of 2 (p90
    8, max 18). Two steps of connections is a readable default; one step
    of names is not, without a threshold.
  - **678 of the 1,111 names appear in one frame only**, so their card
    lists only "you are here". 95 appear in two or more subjects, 14 in
    three, and one (London) in all four. The map's name view should start
    from the 95.

## Verification

- `just check` green after the grow change: 678 tests.
- Negative tests, each seen failing: dropping `linkGrowthProblems`'
  problems fails the two refusal tests; skipping the "must be marked"
  rule fails the refusal test; `names.py add` refuses a duplicate
  Wikidata item (exit 1, nothing written) and a malformed draft.
- The gate after each subject's commit: 678 tests, every subject valid
  against the registry with no warnings, and every connection finds its
  frame. `names.py mark --check` passes on every spec, `shared.json` and
  `western-civ.json` included.
- Dev server: `/ai/eliza`, `/computing/ethernet`, `/feynman/nobel`,
  `/western-civ/dna` and `/western-civ/moon-landing` render their marks
  and connections (the moon landing shows the guidance computer's
  incoming one), with no errors in the log.

## Repaired in passing

- **`names.py`'s slug dropped accented letters** (`kurt-g-del`,
  `fran-ois-chollet`) and split on apostrophes (`moore-s-law`). It now
  transliterates (Ø and Æ by hand, since NFKD keeps them) and drops
  apostrophes, and so reproduces every hand-chosen id in western-civ's
  registry but the deliberate disambiguations (`pantheon-rome`,
  `victoria-ship`). The merge renamed the agents' mangled ids.
- **`lookup` lost a title** when two in one batch redirected to the same
  page (Cargo cult science and Carl Feynman): it now follows each title
  to its page.

## Follow-ups

- **3442 decides how grown content reaches `main`.** Grow now writes
  names too, so a reviewer should check a grown name's Wikidata ID
  against the item. That belongs in 3442's definition of "correct".
- The map (3441) takes the density figures above. Physics (3428) is
  written with the author-subject skill's new names and connections steps.
