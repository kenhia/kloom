# 006 — Second subject: History and Current State of AI

## Goal

korg proposal 3400 (Ken, 2026-09-27: "the next thing to feel is a second
subject with a reasonable amount of content"). It covers three work items,
in this order:

- korg 3391: the narrative follows the spine by default. Not following
  becomes a reader setting, and the Sync Narrative button goes while its
  shortcut stays.
- korg 3396: one app serves several subjects, with a route per subject, a
  chooser, and every API scoped to a subject.
- korg 3395: the AI subject. It needs at least 36 main-spine frames and at
  least three deep trails, on a spine that moves from dates to technologies,
  with rich readings. It is authored by following `skills/grow/SKILL.md`, as
  the framework's authoring guide would be.

## Decisions

- **Premises held.** The Sync Narrative button and the `manual` default
  were in `Narrative.svelte`/`Shell.svelte`. `src/lib/server/config.ts`
  served exactly one subject (`KLOOM_SUBJECT`), and `subjects/` held only
  `western-civ`. kloom is not in the cross-project plan index.

### Narrative follows the spine (3391)

- **A registry row, not a toolbar checkbox.** `followSpine`
  (`engine/settings.ts`) is "Narrative": _Follows the spine_ (default) or
  _Stays until S_, under `kloom.followSpine`. Ken confirmed it belongs in
  the settings control, not in `kloom.config.json`. The old `kloom.sync`
  key is deliberately not read. Its stored value was mostly the old
  `manual` default, and honouring it would have kept existing readers on
  the default Ken just rejected.
- **The shell derives the mode from the setting.** While following, an
  effect keeps the pin on the spine's frame. Turning following off leaves
  the reading where it is, not on whatever frame was pinned before.
- **The toolbar keeps its status line** (`aria-live`): "Following the
  spine.", "In step with the spine." or, when the two differ, where each is
  and "S brings the reading here". The gear now follows it.
- **An ask in flight.** The answer already carried its frame (3360). With
  following on, moving the spine now moves the reading pane mid-answer, so
  the answer shows a line under its heading, "You have moved on; this
  answer stays with the frame it was asked about". Keep and Grow from this
  use the answer's own frame, as before.
- `docs/design.md` §Interaction, §Settings and §Ask were rewritten for it.

### Several subjects (3396)

- **`/<subject>` for every subject, with `/` redirecting.** The page
  moved to `src/routes/[subject]/`, and `src/routes/+server.ts` redirects
  `/` (307) to `$KLOOM_SUBJECT`, or to the first served subject if that one is gone.
  A subject is a directory under `$KLOOM_SUBJECTS_DIR` whose name matches
  `[a-z0-9][a-z0-9-]*` and that holds a readable `subject.json`
  (`listSubjects`, `src/lib/server/config.ts`). `subjectDirFor` checks an
  id against that listing, not only the pattern, so `..`, a hidden
  directory or an upper-case name is simply unknown: a 404.
- **The chooser is the start screen.** It adds an "Or open" row of links
  under Begin, inside the dialog and after Begin in tab order. The engine
  component takes resolved `{title, href}` pairs, so it never builds an app
  route. The page wraps the shell in `{#key}` by subject, and "begun" is
  remembered per subject. Opening another subject, or going Back to one,
  therefore starts at that subject's start screen with a fresh spine, not
  at the old index.
- **Every API names its subject explicitly**, in the body. The other option
  was nesting the APIs under `/[subject]/api/…`. A body field keeps
  subjects and fixed routes out of each other's namespace, and it matches
  the item's wording. Ask builds its context from the named subject. Keep
  refuses an answer asked under another subject (the negative test was
  seen failing without the check). Grow's list takes `?subject=`. Media
  moved to `/media/<subject>/<frame>/<file>`, and the loader's existing
  `mediaBase` option carries the prefix into the rendered reading.
- **Grow: a queue per subject, one runner slot for the host.** Each subject
  keeps its jobs under `<dataDir>/<subject>/grow/` as before. Every served
  subject's queue is loaded at start, so a restart resumes all of them. The
  runners share one slot, so two subjects never run `claude -p` grow jobs
  at once. A job waiting on another subject's job reports "waiting for
  another subject's grow job". The subject gate (`exclusive`) stays
  global, which is over-broad but harmless with one runner.
- **Settings stay global.** None of palette mode, narrative following, ask
  model or grow model is about a subject.
- A second request for the answer-in-flight check (3391) was made live: an
  ask on "We stole FIRE.", then → while it streamed. The answer kept its
  heading and showed the "moved on" line, and the reading moved to
  "We learned to WRITE.".

### The AI subject (3395)

- **Shape.** The plan (`create-tools/subject-plan/ai.json`) has 41 main-spine
  frames in nine segments and four trails of five to seven frames each: 66
  frames. The label kinds run `category` → `date` → `technology` →
  `category`:
  - Dreams of thinking machines: Talos, Llull and Leibniz;
  - Foundations: 1843–1950;
  - The symbolic age: 1956–72;
  - Winters and booms: 1973–87;
  - Learning from data: 1989–2012;
  - Deep learning (technologies);
  - The transformer era (technologies);
  - The frontier (technologies);
  - Open questions (categories).

  The trails are From perceptron to deep learning (at `perceptron`),
  Machines at play (at `deep-blue`), Inside a transformer (at
  `transformer`), and Alignment and safety (at `alignment`). The winters
  and neural-network history run through the main spine, so the
  "AI winters" trail candidate was not needed.

- **Its own look.** Three dark/light palette pairs track the eras: blueprint
  and drafting for the dreams and foundations, terminal and printout for
  the symbolic and statistical decades, and neural and whitepaper for the
  deep-learning era. Every ink, muted, accent and line colour was checked
  at 4.5:1 or better against its background (the lowest is 4.8). The scene
  grammar is unchanged.
- **Authoring at scale.** I wrote the first segment by hand, following the
  grow skill, to find its western-civ assumptions and to set the bar. The
  other 64 frames were written by ten authoring agents in parallel, one per
  segment or trail. Each worked from the grow skill, a written brief (the
  differences from a grow job: a shell, the web, create-tools, images,
  charts and tables, `asOf`, and the fact rule), and the two hand-written
  frames. Each wrote its own frame directories and its own plate module,
  so nothing was shared. I reviewed, validated and committed them segment
  by segment.
- **Tools added**, because the job needed them and the framework will too:
  - `create-tools/subject-plan` writes `spine.json` and the trails from a
    plan, holding only the frames written so far, so every intermediate
    commit validates, however many authors are working;
  - `create-tools/commons-media` searches Commons for freely licensed
    images, downloads a scaled copy, and prints the `media` citation from
    the file page's metadata. It refuses any licence but public domain,
    CC0 and CC BY(-SA);
  - `bar-chart` gained a log scale (`"scale": "log"`) and per-bar display
    labels, for compute and parameter counts that span orders of
    magnitude. The printing-press chart still reproduces byte for byte;
  - `draw-plates/ai.py` collects plates from `ai_<part>.py` modules, so
    several authors draw at once.
- **`asOf` (engine).** A frame may carry `asOf` (`YYYY-MM` or
  `YYYY-MM-DD`), validated. The reading pane shows "As of September 27,
  2026" beside the position, and ask's prompt tells the model the frame is
  dated and to say when an answer may have changed since. Every frame in
  the frontier, the open questions and the safety trail carries one. That
  was the item's "as of" requirement. It lives in the engine, not in a
  metadata convention, because any subject's current state dates the same
  way.
- **One test for every subject.** `engine/subjects.test.ts` loads and
  validates every directory under `subjects/`, checks that each
  illustration is inlined, and checks that each frame is cited with its
  Wikipedia links pinned to a revision. `engine/svg.test.ts` sanitises
  every SVG of every subject. The western-civ `describe` keeps only what is
  specific to that subject.
- **How the content was reviewed.** For each author's report, I checked:
  - its frames and plates on a contact sheet in their palettes;
  - the claims it flagged as unsure, and the surprising recent ones. For
    example, GPT-6 Astra's 1e27 FLOP is in Epoch AI's data, and METR's
    incident investigation, Anthropic's Glasswing and RSP pages and the
    Wikipedia incident article all exist as cited;
  - that the subject validates with only the committed frames on the
    spine.

  The authors themselves caught Wikipedia being wrong against primary
  sources: LeNet's 1989 error rate, and who commissioned the Lighthill
  report. They also left out unverified 2026 claims found in Wikipedia. A
  claim stayed in the frame when sources disagreed only where the reading
  says so. One exception to "every claim sourced": the laws-of-thought
  sentence on switches in series and parallel is textbook circuit
  behaviour, and the plate draws it.

- **What it came to:** 66 frames and about 54,000 words of reading, with
  49 images, 11 charts and 49 tables. Fifteen current-state frames carry
  `asOf`, and every accent is unique.

### The framework test: what the grow skill assumed

Authors reported every place `skills/grow/SKILL.md` assumed western-civ,
was wrong, or left them guessing. Each finding was generalised in the
skill, fixed in the engine or a tool, or filed because it needs a decision.

**Generalised in the skill:**

- "history written with a model" became "a subject": subjects can be
  current state or technical explainers, and those need invented worked
  numbers kept apart from sourced facts;
- spines that are not time: labels for technology and category segments,
  no sort there, and a span sorts by its start year;
- `asOf` for time-sensitive frames;
- palettes that alternate, and a trail's frames take their own era's
  palette;
- counters that are not counts ("$13,500", "38 of 52", "96%");
- metadata for papers: lab, authors, venue;
- plates for techniques, not only objects: trees, networks, loops,
  matrices;
- unique accents;
- many authors (`etAl`), preprints and proceedings, sources read through
  an archive;
- media citations in `citations` only, with the caption credit built
  from them;
- primary sources over Wikipedia, which is sometimes wrong, and the web
  for anything recent;
- a trail's last frame points back to its anchor, and frames are named,
  not described;
- no layout-relative wording ("the drawing on the left" is wrong on a
  phone);
- tables that stand alone;
- a section on authoring with tools: longer readings with media, the
  tools, validation, and rate limits.

**Fixed in the engine or tools:**

- `etAl` on citations, with 59 workaround citations migrated;
- unique accents enforced by `validate()`, so grow is held to them;
- `bar-chart` escapes its text;
- `commons-media` asks for widths Commons actually serves, and warns
  over 350 KB;
- `wiki-cite` waits out a 429 (see Repaired in passing).

**Noted, not changed:**

- The grow verbs still forbid images and keep 350–700 words, because a
  grow job has no tools to fetch or license an image. The skill now says
  where a tooled author differs.
- Charts are SVG images in the frame's own palette. An `<img>` cannot
  follow the reader's palette mode.

### Candidate links to other subjects (for korg 3399)

- **History of Computing:**
  - analytical-engine (Babbage, Jacquard, Hollerith);
  - laws-of-thought (Shannon's thesis as digital design);
  - turing-machine (the stored-program idea);
  - turing-test (the Manchester and Ferranti machines);
  - dartmouth and logic-theorist (the IBM 701, IPL, Lisp);
  - eliza (Project MAC time-sharing);
  - shakey (ARPANET);
  - lisp-collapse (Lisp machines as the first workstations; symbolics.com);
  - expert-systems (the VAX);
  - lenet (Bell Labs DSP chips);
  - adaline (Hoff and the Intel 4004);
  - samuel-checkers (the IBM 701 and 704);
  - alexnet and compute (GPUs to TPUs);
  - tokens (BPE as Gage's 1994 compression);
  - governance (Bletchley Park, then and now).
- **Richard Feynman:**
  - hopfield-network (Hopfield, Feynman and Mead's Physics of Computation
    course at Caltech);
  - turing-machine (Feynman's lectures on computation);
  - self-attention and next-token (softmax as the Boltzmann distribution,
    "temperature");
  - lisp-collapse (the Connection Machine, which needs sourcing);
  - reasoning-models and alignment-faking ("you must not fool
    yourself");
  - capability-evals (his Challenger appendix).

## Verification

- `just check` is green: svelte-check with no warnings, prettier, eslint,
  and 322 tests. Every subject is loaded and validated, and every SVG of
  every subject is sanitised.
- **Negative tests, each seen failing:**
  - keep under another subject (with the check removed);
  - the old `bar-chart` on a spec containing `<` and `&` (invalid XML);
  - a duplicate accent (the test failed on `interpretability`'s INSIDE
    while it was in the working tree);
  - `wiki-cite`'s retry, against a simulated 429 that recovers and one
    that does not.
- **Reproducibility:**
  - every committed chart rebuilds byte for byte from its spec in
    `bar-chart/examples/`, including western-civ's;
  - `draw-plates/ai.py` redraws all 66 plates identically under two hash
    seeds, and `western_civ.py` its 17.
- **Browser pass** (Playwright, headless Chromium, keyboard only):
  - `/` redirects to `/western-civ`, and `/nope` is a 404;
  - media is served under `/media/western-civ/…`;
  - the chooser links the other subject from each start screen;
  - with following on, → moves the reading. With "Stays until S" chosen
    in the settings panel (Tab to the gear, Enter, Tab, ↓), → leaves it
    behind, S brings it back, and the choice survives a reload;
  - S does nothing from the AI pane;
  - on `/ai`, Home and End, a walk of all 41 stops, T into all four
    trails and Esc back out all work;
  - HUD labels read "Scaling laws" and "Self-attention" in the technology
    segments, and the `asOf` line shows on the last frame;
  - 44 main-spine images load with none broken, and there are no console
    errors or failed requests;
  - at 390px, the layout has no horizontal overflow.
- **A live ask:** the answer-in-flight line appeared on moving the spine
  mid-answer (above).

## Repaired in passing

- **Tools the authors hit:**
  - `bar-chart` did not escape its text, so a `<1%` label broke the SVG;
  - `commons-media`'s `--width` was rounded up by Commons to its next
    thumbnail step, so files came back 960 px wide;
  - `wiki-cite` failed outright on a 429;
  - the logic-theorist plate iterated a Python set, so its paths came out
    in a different order on each run.
- **Stale docs:** CLAUDE.md, the justfile and README said only
  western-civ was validated or served.
- **The intermediate commits' `prettier --check` is red.** My staging
  script formatted the partial spine outside the repo's Prettier config,
  so the spine in intermediate commits is not Prettier's layout. HEAD is
  formatted, and the squash merge makes it moot.
- **Privacy.** Early in the sprint, one Commons API call of mine, and a few
  Wikipedia API calls from one authoring agent, sent Ken's email address
  in the User-Agent header. All of that stopped once noticed. The committed
  tools send a project URL, and the skill now says never to name a person
  there.

## Follow-ups

Filed in korg, each naming the decision it needs. Candidate links went to
korg 3399 as a comment.

- **korg 3404**: a way to read scanned PDFs and papers while authoring. Every author
  needed one (pypdf or pymupdf, through `uv`). The decision is whether
  create-tools may depend on a non-stdlib package, as `trace-art` does.
- **korg 3405**: the citation schema:
  - a DOI field;
  - kinds for a chapter in a proceedings volume and for a report;
  - an approximate date ("c. 1951");
  - whether `sources` should be derived from `citations` rather than
    kept in step by hand.

  This is a content-model decision that grow and the framework will both
  carry.

- **korg 3406**: charts in the reader's palette mode. A chart is an `<img>` in its
  frame's palette, so a dark chart stays dark in Light mode. The decision
  is between inline SVG charts and one rendering per scheme.
