# 014 — Third subject: Richard Feynman

## Goal

korg proposal 3426 (Ken, 2026-09-28), covering korg 3397: the third subject,
and the first built around a person. Richard Feynman's life runs on a dated
spine, with deep trails for the physics, Los Alamos, computation and
Challenger. It is authored with sprint 006's method, which is first written
down as a reusable skill, so that this subject tests the skill. The proposal
also asks for rich readings, and for candidate links to the AI subject and to
a future History of Computing.

## Decisions

- **Premises held.** There was no `subjects/feynman` and no
  `skills/author-subject`. All seven create-tools the proposal names
  existed. kloom is not in the cross-project plan index.

### The method, written down (step 0)

- **`skills/author-subject/SKILL.md`** is the procedure, in five steps:
  1. plan, including the theme, the voice and the contrast check;
  2. write the first segment by hand;
  3. brief the parallel authors;
  4. review, validate and commit each segment;
  5. write the record.

  It is short on purpose. `skills/grow/SKILL.md` stays the style guide for
  every frame, and the new skill only orders the work around it.

- **The brief.** The one shared by every author is kept, with the plan, in
  the sprint's working notes. Its substance is in this record, in the
  sections below. Each author also got a paragraph naming its frames, their
  palettes, its plate module, and what the neighbouring frames cover, so
  that no two authors wrote the same story.

### Shape

- **A life on dated segments, and the depth in trails.** The plan is
  `create-tools/subject-plan/feynman.json`. Its 34 main-spine frames run in
  seven `date` segments:
  1. Far Rockaway, 1918–35;
  2. MIT and Princeton;
  3. Los Alamos;
  4. Cornell;
  5. Caltech;
  6. The wider world, 1969–85;
  7. The last years.

  A closing `category` segment, Afterlife, holds the legend and the legacy.
  It is a category because those two frames describe the reception, not
  events in the life.

- **Five trails, 28 frames:**

  | Trail              | Anchor               | Frames | Label kind |
  | ------------------ | -------------------- | ------ | ---------- |
  | Sum over histories | `thesis`             | 6      | technology |
  | The diagrams       | `diagrams`           | 6      | technology |
  | The Hill           | `los-alamos`         | 5      | date       |
  | Computing          | `simulating-physics` | 5      | date       |
  | The commission     | `challenger`         | 6      | date       |

  The two physics trails are labelled by idea, not date. Their frames
  explain one idea after another, so a year would be the wrong label.

- **Candidates not made trails.** Teaching and the Lectures stay on the
  main spine (`lectures`, `character-of-law`, `qed-book`). They are
  episodes of his Caltech years, and every reader should pass them. Bongos,
  safecracking and Tuva are split between the frames they belong to:
  - safecracking goes to The Hill;
  - drumming goes to `brazil` and `tuva`;
  - Tuva is a main-spine frame.

  Ten frames of anecdote would have been memoir, retold at length.

- **The voice is "he".** western-civ and ai use a collective "we". A
  life needs the third person ("He fixed radios by THINKING."). A frame
  about a thing may make the thing its subject.

### Theme

Three pairs of palettes, each the other's counterpart. Every ink, muted,
accent and line colour was checked against its background:

| Palette    | Scheme | For                              | Ink  | Muted | Accent | Line |
| ---------- | ------ | -------------------------------- | ---- | ----- | ------ | ---- |
| lamplight  | dark   | the life                         | 14.5 | 7.5   | 8.4    | 11.0 |
| manila     | light  | the life                         | 13.0 | 5.4   | 5.5    | 10.7 |
| chalkboard | dark   | physics and teaching             | 12.8 | 7.1   | 10.4   | 11.1 |
| graphpaper | light  | physics and teaching             | 15.0 | 5.9   | 6.1    | 12.1 |
| blueprint  | dark   | Los Alamos, Challenger, machines | 12.7 | 7.0   | 6.2    | 9.7  |
| vellum     | light  | Los Alamos, Challenger, machines | 14.5 | 5.8   | 5.8    | 11.1 |

The lowest contrast is 5.4:1, against a floor of 4.5.

### Accuracy and rights

- **His stories are his telling.** Frames that rest on the two memoirs say
  so in the reading. Claims of fact rest on documented sources where they
  exist: papers, the Nobel lecture, the Rogers Commission report, Caltech's
  archives and letters.
- **The AIP oral history** (Charles Weiner, 1966–73) is the best source for
  his early life. aip.org refuses fetches, so it was read through the
  Wayback Machine. Its terms forbid quoting without AIP's permission, so it
  is paraphrased everywhere and never quoted. It is cited by its own URL.
  The first draft of `least-action` quoted it, and the quotation was
  rewritten as a paraphrase before commit.
- **The Feynman Lectures** site blocks both fetches and the Wayback Machine.
  The Lectures are cited as the book, with the chapter's page URL.
- **Books** are cited by their Open Library work page, because a citation
  needs a URL.
- **Quotations** from anything still in copyright are a sentence at most.

### The first segment, by hand

Far Rockaway has three frames:

- `far-rockaway` (1918): his father, the encyclopedia and the dinosaur at
  the window;
- `radio-boy` (c. 1930): the laboratory, the radios, and the π in a tuned
  circuit;
- `least-action` (c. 1934): Abram Bader, and a worked example of the action
  of a thrown ball.

**What writing them found:**

- **An unsupported claim.** The draft said his father had wanted to be a
  scientist. None of the sources read said so, and it was cut.
- **Images need no caption line.** The page builds the credit from the
  `media` citation, which the AI frames already relied on. Three
  hand-written caption lines duplicated it and were removed (their facts
  moved into the alt text). The brief now says so.
- **The sources disagree about Columbia.** The usual story is its quota on
  Jewish students. Feynman in 1966 remembered only failing its entrance
  exam. `least-action` gives both accounts.
- **Spelling.** Weiner's transcript spells the teacher "Bater". The
  Lectures spell him "Bader", which the frames follow.

### Authoring at scale

- **Eleven authors in parallel**, one per segment or trail, with the
  author of an anchor frame also writing its trail (Los Alamos and The
  Hill; Challenger and The commission). Each worked from the grow skill,
  the author-subject skill, the shared brief, its own paragraph and the
  three hand-written frames. Each wrote only its own frame directories,
  its own plate module (`create-tools/draw-plates/feynman_<part>.py`) and
  its own chart specs. Each reported its unsure claims, where sources
  disagreed, where the skills misled it, and candidate links.
- **Review, per segment.** For each report:
  - the plates were checked on a contact sheet in their palettes;
  - the flagged claims were spot-checked;
  - the segment was committed on its own, with a spine holding only
    committed frames (`stage_segment.py`), after validating the index
    exported to a scratch directory.

  There are twelve commits of content. The Computing trail waited for its
  anchor, `simulating-physics`.

- **What review changed:**
  - `the-legend` had the 2014 argument backwards: Francis answered
    Jogalekar, not the other way round.
  - The Baffler quotation in `the-legend` was checked against the page
    (read through the Wayback Machine).
  - Rabi's Shelter Island report in `lamb-shift` was tightened to the
    hyperfine anomaly.
  - Three overlaps the brief left open were settled by trimming one side
    to a pointer: `thesis` and `dirac-hint` (the Nassau Tavern), `cornell`
    and `trinity`/`arline-death` (the bridges and the 1946 letter), and
    `surely-joking` and `the-legend` (the criticism, trimmed by its
    author).
  - The Hill was reordered by date, so that censorship and safecracking
    come before Oak Ridge.
  - The Lectures on Computation's editors moved into `editors` once the
    engine rendered them.
- **The brief was wrong once.** It called Mary Louise Bell his first wife.
  She was his second, and the author corrected it.
- **The records correct his tellings,** and the readings say so:
  - the wobbling plate's ratio is backwards in both of his tellings; it is
    2:1 wobble to spin (Tuleja et al. 2007), checked with Euler's equations
    and a simulation;
  - the Los Alamos IBM throughput (Lewis and Archer 2021);
  - who ran the IBM machines (Nelson and Livesay, not he);
  - the Water Boiler's critical mass (Christy);
  - his 1/273 for 1/243;
  - Millikan's charge and "Mr. Young's" rats in _Cargo Cult Science_.
- **Where sources disagreed, the readings give both**, among them:
  - Arline's prognosis;
  - Pauli's and Einstein's remarks at the first seminar;
  - whether _Physical Review_ turned down the 1948 paper;
  - the Brazil year;
  - Carl Feynman's birth year;
  - the Kutyna hint (his telephone call, or the garage and Sally Ride);
  - Feynman's last words;
  - the Tuva invitation's timing;
  - the dates of the Physics of Computation course.
- **What it came to:**
  - 62 frames and about 43,700 words of prose;
  - 62 images, all public domain, CC0 or CC BY(-SA), each looked at before
    use;
  - 12 charts and 67 tables;
  - four frames dated with `asOf`: path integrals today, the magnetic
    moment, quantum computing now, and the legacy;
  - every accent unique.

  Every chart rebuilds byte for byte from its spec, and every plate
  redraws identically under two hash seeds.

### The method test: what the skills assumed

The authors reported every place the grow skill, the new skill or the brief
was wrong, silent or misleading. As in sprint 006, each finding was
generalised in a skill, fixed in the engine or a tool, or noted.

**Generalised in `skills/grow/SKILL.md`:**

- the headline voice is the subject's, not always a collective "we";
- a span that follows later frames in a trail sorts by where its story
  lands, and its label carries the span;
- disagreeing sources are given in the reading. That includes the subject
  disagreeing with himself, or being wrong on a checkable fact;
- a person's own stories are marked as their telling;
- a source seen only quoted in another is cited as the work that quotes
  it;
- quotations are a sentence at most, and US government records are public
  domain;
- word counts are of prose, not tables or alt text;
- mathematics is written in Unicode;
- images are grepped for reuse before use, and Commons dates, authors and
  file names can be wrong;
- an image that is not free is described in the reading, not shown;
- an edited book carries `editors`;
- how to validate while others are mid-write;
- a grow job's "no images" rule was worded as if it bound every author,
  contradicting §Authoring with tools. It is now scoped to grow jobs.

**Added to `skills/author-subject/SKILL.md`:** what a brief must settle
because parallel authors cannot see each other, namely:

- who owns a shared topic;
- accents and images;
- the order of a dated trail;
- validating a copy of finished frames;
- landing anchors before their trails.

It also covers staging a segment with `stage_segment.py`.

**Fixed in the engine or tools:**

- **Validating one author's frames.** Every author found the live subject
  failing on others' half-written frames, and three dropped temporary tests
  into `engine/` to work around it. `subject_plan.py --complete DIR` now
  writes a copy holding only finished frames, and the two subject tests
  read `$KLOOM_TEST_SUBJECTS`. The check was seen catching a real error:
  The Hill's order.
- **`contact_sheet.py`** (new) shows a plate before its `frame.json`
  exists.
- **`stage_segment.py`** (new) stages a segment with a spine of committed
  frames only.
- **An edited book's editors now render** ("Edited by …"). They had been
  dropped outside chapters (`engine/citation.ts`). The test was seen
  failing first.
- **`commons-media`:**
  - it creates the frame directory;
  - it keeps the year when Wikidata writes an unknown month as `00`;
  - it drops Commons' doubled "Unknown authorUnknown author";
  - its README no longer says to write a caption credit.
- **`wiki-cite`** prints the citations it found when one title is missing,
  and still exits 1.

**Noted, not changed:**

- **Duplicate images.** The validator does not refuse the same image in
  two frames. Reuse can be deliberate, so authors grep for it instead.
- **`commons-media` and large files.** It keeps a PNG as PNG, and returns
  the original when that is narrower than the width asked for. Large PNGs
  were converted to JPEG by hand, and adding Pillow to the tool is
  not worth it.
- **Links between frames.** A reading cannot link to another frame
  (http(s) links only). Pointing onward by name works, and in-subject links
  are part of the cross-subject links question (3399).
- **Blocked sources.** Several primary sources refuse fetches: APS, aip.org
  and the Feynman Lectures site. The workarounds were the Wayback Machine,
  CaltechAUTHORS scans (many of his papers are free there) and Kaiser's own
  PDFs. The brief named some of these, and the authors found the rest.
- **The AIP transcripts' own errors.** Speech-to-text mangles names
  (Tiomno, Leite Lopes, Welton, "Bater"), and the transcripts disagree on
  small facts with his later tellings. They were checked against other
  sources.

### Candidate links to other subjects (for korg 3399)

Reciprocal to sprint 006's list from the AI side:

- **To `ai`:**
  - `physics-of-computation` and `connection-machine` → `hopfield-network`.
    Feynman co-taught with Hopfield, and mapped Hopfield's network onto
    the CM-1.
  - `cargo-cult` → `reasoning-models`, `alignment-faking` and
    `capability-evals`: "you must not fool yourself", and benchmark cargo
    cults.
  - `reliability` and `appendix-f` → `capability-evals`: estimating rare
    failures, and independent verification. `return-to-flight` →
    `alignment`: the normalisation of deviance.
  - `path-integrals-today` and `every-path` → `self-attention` and
    `next-token`: Boltzmann weights and temperature. Also → `diffusion`,
    through the Feynman–Kac formula's averages over random paths.
  - `lectures-on-computation` → `turing-machine`; `punched-cards` →
    `analytical-engine`: punched cards as instructions.
  - `the-legend` → how models repeat misattributed quotations (weak).
- **To a History of Computing:**
  - `punched-cards`: human computers, the IBM 601s, Frankel and Metropolis
    on to ENIAC and MANIAC, Livesay and Kemeny;
  - `princeton`: the Frankford Arsenal gun director, an analogue computer
    of non-circular gears;
  - `connection-machine`: massively parallel SIMD machines;
    `physics-of-computation`: Mead–Conway VLSI;
  - `quantum-computers` and `lectures-on-computation`: reversible
    computing and Landauer's principle; `quantum-computing-now`: Shor's
    algorithm and post-quantum cryptography;
  - `diagrams`, `magnetic-moment` and `nobel`: computer algebra (REDUCE,
    Kinoshita's programs), grown out of evaluating diagrams;
  - `path-integrals-today`: lattice QCD as a driver of supercomputers;
    `thesis`: Monte Carlo from Los Alamos;
  - `plenty-of-room`: miniaturising the computer, the prehistory of
    Moore's law;
  - `appendix-f`: the shuttle's AP-101 computers voting four ways, and
    NASA's software verification;
  - `partons`: SLAC, which ran the first web server in the US;
  - `dyson` and `cornell`: the Institute for Advanced Study in the years
    of von Neumann's computer.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint,
  and 540 tests. Every subject is loaded and validated, and every SVG of
  every subject is sanitised.
- **Every content commit validated on its own.** The index was exported to
  a scratch directory and the subject tests were run there, so each
  commit's subject is valid as committed.
- **Negative tests, each seen failing:**
  - the edited-book test, before the renderer fix;
  - the review-notes test with its clock frozen (9 failures in 10 runs);
  - the complete-copy check, which caught The Hill out of order before the
    plan was changed.
- **Reproducibility:** all twelve Feynman charts rebuild byte for byte from
  their specs, and `draw-plates/feynman.py` redraws all 62 plates
  identically under two hash seeds.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on a
  scratch data directory):
  - `/feynman`, Enter to begin;
  - → through all 34 main-spine frames in plan order, with the right HUD
    label and chapter at each;
  - T into each of the five trails at its anchor, → through every trail
    frame in order, and Esc back to the anchor;
  - Home and End reach the two ends;
  - no broken images, no console errors, no failed requests;
  - no horizontal overflow at 390px;
  - the start screen lists Richard Feynman, rings the loom with its
    plates in lamplight, and offers the last place back.

## Repaired in passing

- **A flaky test.** `src/lib/server/review-notes.test.ts` failed once in
  `just check`: notes saved in the same millisecond tie on `created` and
  list in the order of their random ids. The test now gives the store a
  clock that steps a second per write, and the diagnosis was confirmed by
  freezing the clock (9 failures in 10 runs). The store's ordering is
  unchanged.
- **Tools:** `commons-media` (a missing frame directory, the `00` month,
  the doubled unknown author) and `wiki-cite` (one missing title lost the
  whole batch), above.
- **Stale docs:**
  - the commons-media README's caption credit;
  - the grow skill's unscoped "Do not add images";
  - the README, CLAUDE.md, the design doc and the roadmap still said there
    were two subjects.

## Follow-ups

None filed. Every finding above was fixed here or is noted with its reason.
The candidate links go to korg 3399 as a comment.

## Deployed

2026-09-28, by `just deploy` (the `recipe: deploy` in `.sprint-deploy`),
from merged `main` at `ca28af6`, to the kloom service on kai. The
service's content clone is at the same commit.

- `just verify` passed all eight door checks. The tailnet door refuses
  anonymous writes and reader-data reads, and the ssh door lets its reader
  through.
- **The sprint's work, live on both doors (:4890 and :4891), each 200:**
  - `/feynman`;
  - `/feynman/least-action` (main spine), whose page carries "least
    ACTION.";
  - `/feynman/magnetic-moment` (a trail frame);
  - `/media/feynman/far-rockaway/grand-view-avenue.jpg`;
  - `/api/start/feynman` (the start screen's look).

  The start page lists Richard Feynman among the subjects.
