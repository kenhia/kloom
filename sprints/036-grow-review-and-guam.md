# 036 — Grown content reviewed into main, a safe grow under dev reloads, and the Guam section re-sourced

## Goal

korg proposal 3492, covering three items Ken decided on 2026-10-02, ahead of
the public reader site (3458):

- **3487:** Keeping Watch's navy-pow Guam section rewritten from Chief Nurse
  Marion Olds's 1943 account. The details that rested only on Internet
  Archive snippets of Leona Jackson's article are cut or re-sourced.
- **3486:** a grow job survives a dev server's module reload. One queue on
  `globalThis`, and a lock per job.
- **3442:** grown content reaches `main` only through review. Dev grows go
  to `grow/dev-<host>`, `skills/review-grown` reviews them, and every
  sprint first checks for an unreviewed grow branch.

## Decisions

- **Premise, checked at start.** It held for all three.
  - **3487:** the reading still said "an old Army barracks, cold and long
    unused", "their patients' beds", and "a fourth-rate hotel with sprung
    beds". Jackson's citation was supporting, not key.
  - **3486:** `grow-service.ts` kept its queues in a module-level map.
  - **3442:** there was no `review-grown`, no `Validated` trailer and no
    dev grow branch. `growBranch()` is null unless `KLOOM_GROW_BRANCH` is
    set.
  - The service's `grow/kai` was not ahead of `main`. An old remote branch,
    `grow-kai-faraday`, is not an ancestor of `main`, but its frame has been
    in `main` since sprint 008. So the sprint-start check must ask whether a
    branch's _content_ is in `main`, not only its commits (below).
  - kloom is not in the cross-project plan index.

### 3487: the Guam section

- **Olds read in full, through WebFetch,** since Mansell's site refuses a
  script from kai. Every phrase quoted in the reading was checked word for
  word in a second pass that asked only for whole sentences. A first pass
  had returned "The barracks, fully 250 feet long" where the korg comment
  had "an enormous soldiers' barracks". Both turned out to be Olds's, in
  different sentences, and the reading quotes each as she wrote it.
- **What changed in the reading:**
  - Cut "old" and "long unused", which no source supports.
  - Replaced "patients' beds" with the nurses' own straw mattresses,
    "scarcely two feet wide, and hard as wood". They slept "fully dressed
    even to our coats and gloves", and were forbidden to speak to the men
    held with them.
  - Cut the "fourth-rate hotel with sprung beds", which rested only on the
    snippets. Kobe is now Olds's "decidedly larger and warmer" room and
    better food.
  - Added what Olds and Guampedia both give: the march to Piti, the
    _Argentina Maru_, and Zentsuji on Shikoku.
  - Replaced "on 17 June they boarded". The timeline's 17 June entry is
    about Ambassador Grew's party, not the nurses. The reading now has the
    train to Yokohama, eight days at anchor, and sailing at half past one
    in the morning of 25 June, all from Olds.
  - Replaced "reached New York on 25 August" with "in late August". Olds
    writes "that morning of August 29", 25 August is the date usually given
    for the _Gripsholm_, and none of the frame's sources gives 25. "Late
    August" is true by either.
  - The Kobe hotel's name (the Eastern Lodge, from Mansell's timeline) is
    left out. The timeline is an untitled text file, and naming it would
    mean inventing a title for a detail the reading does not need.
- **Citations:**
  - **Olds** is added as a `key` article (_Sensation_, February 1943), with
    `mirror: true`. It renders "(copy at mansell.com)".
  - **The NHHC page** still does not connect from kai, but the Wayback
    Machine now has a snapshot (8 December 2025), read in its `id_` form.
    Its only Guam content is the Navy's nursing school there, founded in
    1911, which is what the frame cites it for. Its `url` is now the
    snapshot, as physics/solids does for a gone page.
  - **Guampedia** gains its author, Shannon J. Murphy. It was read again
    and supports the _Argentina Maru_, 10 January, five nurses and
    Zentsuji.
  - **The pinned Battle of Guam revision** says "271 personnel and four
    nurses", so the parenthetical about Wikipedia's count stands. The pinned
    Wilma Leona Jackson revision has "Jackson and three other nurses, under
    the supervision of Chief Nurse Marian Olds".
- **Shown to Ken before merging**, as the proposal asks: it is his mother's
  subject.

### 3486: one queue, and a lock per job

- **The queues and the runner slot live on `globalThis`** (`kloomGrow`), as
  `subject.ts` already does for its change listener. A reloaded
  `grow-service` finds the queue running its jobs, whose `load()` is
  memoised, so nothing resumes. The old module's runner finishes the job,
  and new code takes over at the next restart.
- **A lock per job,** `<id>.lock` beside the record. It holds
  `{server, child}`: the server's pid, and the model process's once the
  provider reports it through a new optional `onSpawn` on `GrowRequest`.
  `ClaudeCliProvider` calls it after spawning. Lock writes go through one
  chain, so a late write of the child's pid can never land after the unlock
  and leave a lock behind.
- **What "live" means.** A lock is live if its model process is alive, or if
  this same process wrote it (another queue instance, mid-job). A server
  pid from an earlier run is not trusted on its own: a restart may reuse it,
  and a reused pid must never hold a job forever.
- **What a loading queue does with a `running` or `applying` job:**
  - **Live lock:** it waits, polling every second. It runs nothing else
    meanwhile, since the host still runs one job at a time. When the lock
    clears it takes what the record says: the other instance's outcome, or,
    if the job was left mid-run, the restart rules as before.
  - **Stale lock or none:** it resumes as before.
- **Tests,** each seen to fail with its bug planted:
  - A second queue adopts a job in flight. The first queue's job runs a
    real `sleep` as its model; the second never calls its runner and ends
    with the first one's commit. That's one child and one commit.
  - A stale lock (model and server gone) resumes.
  - A model process that outlived its server is waited on, then the job
    resumes.
  - `lockLive`'s rule.
  - Two fresh imports of `grow-service` (`vi.resetModules`) return the same
    queue.

  Making every lock read as dead fails three of them. Putting the state back
  in module scope fails the reload test.

### 3442: grown content reviewed into main

- **`Validated: yes`** ends every grow commit's message. The job commits
  only what passed `validate()`, so it is always true. The grow skill now
  says the job runs the validator after the model, so the model doesn't
  write "not validated" as `8dfc521` did. It also says a reviewer checks
  the facts after it.
- **Dev grows go to `grow/dev-<host>`, in a worktree** (`growWorktree`, in a
  new `src/lib/server/grow-branches.ts`). There were two ways to commit to a
  branch the checkout isn't on:
  - **Plumbing:** write the commit into the branch and leave the files in
    the checkout. That leaves grown frames untracked in the author's working
    tree, ready to be swept into the sprint branch, and makes the next grow
    refuse a dirty subject.
  - **A worktree:** the one the job uses. It copies from the worktree,
    applies to it and commits in it, exactly as the service does in its
    content clone. The author's checkout is never touched.

  The worktree's details:

  - It lives under `~/.cache/kloom/grow-<repo>` (or `$KLOOM_GROW_WORKTREE`),
    not under `data/`. A worktree inside the checkout would be seen by
    vitest, prettier and Vite's watcher as a second copy of the repo.
  - It is made from `main` the first time. Before each job it is reset to
    `main` once main has all its content and it has no changes of its own,
    so the next grow starts from what was reviewed.
  - It is pushed, as `grow/kai` is.
  - The dev server goes on showing the checkout. The AI pane's done line
    says where a dev grow went ("to grow/dev-kai, for review; it shows here
    once merged"), from a new `result.branch`.
  - Formatting resolves the repo's Prettier config in the checkout
    (`formatAs`), since the worktree has no `node_modules` for the Svelte
    plugin the config names.

- **Reviewed state is a git fact.**
  - `lastMerged` moved from `content.ts` into `grow-branches.ts`, shared by
    the service's sync and the new check.
  - It gained the review trailer, `Grow-reviewed: <tip sha> (<ref>)`. A
    review may repair grown files on the way into `main`, so `main` then
    never holds the grow branch's exact files. Without the trailer, the
    content test would call such a branch pending forever, and the
    service's sync would try to rebase the original over the repair and
    stop on "diverged". With it, the sync resets `grow/kai` onto `main`.
  - A test with the trailer left out shows a repaired merge is otherwise
    not recognised.
- **`just grow-pending`** is the sprint-start check. It fetches, lists every
  grow branch local and on origin (`grow/*`, and the older `grow-*`), and
  exits 1 when one holds content `main` lacks. Run at the start of this
  sprint, it found `origin/grow/kai` and `origin/grow-kai-faraday` both
  merged. The faraday branch's commits are not in `main`'s history, but its
  content is, from sprint 008's squash.
- **`skills/review-grown/SKILL.md`** gives the procedure:
  1. Cherry-pick the pending commits onto a review branch from
     `origin/main`.
  2. Check them against the definition of "correct" that Ken's comment on
     3442 sets out: validation, the fact rule with the tools the job
     lacked, the Wikidata items of grown names, connections against the
     other frame, house style and plates, an accurate message.
  3. Repair in commits of its own, and flag what it can't repair.
  4. Open a PR listing both.
  5. Squash-merge by default, under korg:3422's rule, with the trailer as
     the message's last paragraph.

  It never pushes to a grow branch.

- **CLAUDE.md** tells every sprint to run `just grow-pending` first, and to
  ship any review as its own PR. The rules list gains "grown content
  reaches main only through review-grown". `docs/design.md` gains §Reviewing
  grown content, and §The content clone and §Grow are updated.
  `docs/deploying.md`'s "Bringing grown content back" now describes the
  review.
- **Ken approved the Guam rewrite** as shown (2026-10-02), and asked for
  the proof run to be a real grow, leaning to western-civ, which is the
  shallowest subject.

### The proof run

western-civ's spine had nothing between Shakespeare's First Folio (1623)
and Watt's engine (1776). Its frames are about how knowledge is made, kept
and spread: writing, the scriptorium, the press, Erasmus. So the request was
one frame on the Royal Society and _Philosophical Transactions_ (1665), the
first scientific journal.

The job went to a dev server already running on :5416 from this checkout,
left over from sprint 034's session, with
`KLOOM_DATA_DIR=.scratch/mynotes/data`. A fresh `vite dev` meant for the run
could not take the port. Vite loads server modules on request, so the job
ran the sprint's current code:

- It made the worktree `~/.cache/kloom/grow-kloom` on `grow/dev-kai` from
  `main`.
- It wrote `{server, child}` to the job's lock.
- It left the checkout on `036-grow-review-and-guam`.

How the proof run went:

- **The grow** (about 12 minutes, Opus 5.5, with web) committed `72b49aa`,
  `grow(western-civ): add royal-society`, on `grow/dev-kai`.
  - It added one frame, the name `christopher-wren`, and connections to
    `physics/prism` and `western-civ/harrison-chronometer`.
  - Its message ends `Validated: yes`, and the AI pane's result carries
    `branch: grow/dev-kai`.
  - It pushed with no error, and released its lock.
  - The checkout stayed on the sprint branch, and its subjects were
    untouched.
  - `just grow-pending` then exited 1, listing `grow/dev-kai` and
    `origin/grow/dev-kai`.

  The job's summary still says "the validator runs after I finish, so I
  haven't seen it pass". The grow skill's new paragraph wasn't in effect
  yet, since the job read the skill as `main` had it.

- **The review** followed the skill: a branch from `origin/main`,
  `review-grown/grow-dev-kai-20261002`, with `72b49aa` cherry-picked onto it.
  - **Checked against volume 1** (the frame's own Project Gutenberg
    citation):
    - the date line;
    - the introduction's quotation, word for word;
    - Hooke's note on Jupiter, word for word;
    - the contents as the reading lists them;
    - sixteen pages (issue 2 begins on page 17).
  - **Checked against the Royal Society's history pages:**
    - the 1660 meeting;
    - the 1662 charter and the motto's gloss, word for word;
    - the shilling;
    - the journal's losses;
    - 1752, and the 1830s.
  - **Checked against the pinned revisions:**
    - the twelve men and the "Colledge" quotation;
    - the 1663 charter and its arms;
    - Hooke's curatorship;
    - the Council's 1 March 1664/5 order;
    - Oldenburg's letter to Boyle, word for word.
  - **Wren's** Wikidata item is right (Q170373, by `names.py lookup`).
  - **Both connections** are true against the other frames' readings.
  - **The plate,** rendered at 1400×900, draws what the reading says, and
    `just scene-fit western-civ` reports 0 misfits.
- **What the review repaired,** in its own commit:
  - Horace's line was misquoted inside quotation marks ("of any master";
    the source has "of a master").
  - "Wikipedia gives its print run as 1,000 copies" sat in the 1665
    paragraph, but the pinned revision gives that run for the 1850s.

  Neither is something `validate()` could catch, and neither was caught by
  the model that read the same pages. That is the case for the review.

- **PR #42** listed what was checked, what was repaired and nothing flagged.
  Ken approved the merge, and it was squash-merged as `c6df465` with
  `Grow-reviewed: 72b49aa62e7cfbc0a11d8382e3b2338cfdcc239a (grow/dev-kai)`
  as its last paragraph. `just grow-pending` then read all four grow
  branches as merged, `grow/dev-kai` included: `main` holds the repaired
  text, and only the trailer makes it count. The sprint branch was rebased
  onto it.
- A dev server left running from sprint 034's session held :5416 with a
  scratch data directory. It ran the job correctly, and was stopped
  afterwards.

## What shipped

- **navy-pow's Guam passage, rewritten from Marion Olds's own account.**
  Olds is now a key source, marked `mirror`. The NHHC page points at its
  Wayback snapshot, and Guampedia names its author.
- **A grow job keeps one running copy under a dev reload** (`globalThis`
  state). Each job has a lock (`{server, child}`), with adoption on load and
  a stale-lock resume. `onSpawn` on `GrowRequest` and `GrowHost` carries the
  child's pid.
- **The review path for grown content:**
  - dev grows go to `grow/dev-<host>` in a worktree;
  - every grow commit ends `Validated: yes`;
  - `src/lib/server/grow-branches.ts` holds `growWorktree`, `growBranches`,
    `contentMerged` and the shared `lastMerged`, which now honours the
    `Grow-reviewed` trailer;
  - `just grow-pending` is the sprint-start check;
  - `skills/review-grown/SKILL.md` is the procedure;
  - the AI pane says where a dev grow went;
  - CLAUDE.md, `docs/design.md` (§Grow, §The content clone, a new
    §Reviewing grown content) and `docs/deploying.md` are updated, and the
    grow skill says the job validates after it.
- **western-civ gains `royal-society`** (merged separately as PR #42, the
  proof run).

## Verified

- `just check`: svelte-check, lint, and 1,285 tests, including the new
  lock, reload, worktree, pending-branch and trailer tests. Each of the new
  gates was seen to fail with its bug planted:
  - **lock liveness off:** three tests fail;
  - **queue state back in module scope:** the reload test fails;
  - **content check off:** the squash test fails;
  - **no trailer:** a repaired merge isn't recognised.
- **The Guam frame** validates, and Olds's citation renders "(copy at
  mansell.com)".
- **The proposal's 3442 gate, live:**
  - a real dev grow landed on `grow/dev-kai`, not the current branch;
  - `review-grown` produced PR #42, which merged;
  - `just grow-pending` found nothing pending afterwards.

## Follow-ups

- None filed. Two notes for later:
  - **The worktree's catch-up compares against local `main`.** Until a
    checkout pulls, the next dev grow starts from the reviewed grow commit
    rather than from `main`. That's harmless: the review takes only the
    commits `main` lacks.
  - **The grow skill's new paragraph** shows its effect from the next grow
    onwards.

## Deployed

2026-10-02, `6b071b8` to the kloom service on kai, by `just deploy`. The
review PR, #42 (`c6df465`), was already on `main`. The deploy built from
merged `main`, restarted the unit and passed its own ten checks. The service
journal shows `content: grow/kai fast-forwarded to origin/main`, then the
library rebuilt (build `519e7c`).

Verified live for this sprint:

- `/western-civ/royal-society` serves, with the review's repair ("of a
  master").
- navy-pow's body has the rewritten Guam passage ("_Argentina Maru_",
  "hard as wood"), and "fourth-rate" is gone.
- The page's Sources list renders Olds's citation "(copy at mansell.com)".

The grow lock, the dev worktree and `just grow-pending` are dev- and
review-side. The service gets the lock with this deploy, and nothing in its
behaviour changes without a grow.
